#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import urllib.request
from typing import Any

RUNTIME_ROOT = Path('/root/projects/ordivon-runtime')
HOST_ROOT = Path('/root/projects/ordivon-host')
RUNTIME_ENV = Path('/etc/ordivon/ordivon-runtime.env')
HOST_TOKEN_FILE = Path('/etc/ordivon/host-mcp.token')
RUNTIME_ENDPOINT = 'http://127.0.0.1:8897/mcp'
HOST_ENDPOINT = 'http://127.0.0.1:8898/mcp'


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def git_head(root: Path) -> str:
    return subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()


def git_dirty(root: Path) -> bool:
    return bool(subprocess.check_output(['git', '-C', str(root), 'status', '--porcelain'], text=True).strip())


def service_state(unit: str) -> dict[str, Any]:
    output = subprocess.check_output(
        ['systemctl', 'show', unit, '-p', 'ActiveState', '-p', 'SubState', '-p', 'MainPID'],
        text=True,
    )
    values: dict[str, str] = {}
    for line in output.splitlines():
        if '=' in line:
            key, value = line.split('=', 1)
            values[key] = value
    return {
        'unit': unit,
        'activeState': values.get('ActiveState'),
        'subState': values.get('SubState'),
        'mainPidPresent': values.get('MainPID', '0') not in {'', '0'},
    }


def load_runtime_probe():
    path = RUNTIME_ROOT / 'scripts' / 'mcp_probe.py'
    spec = importlib.util.spec_from_file_location('p1b_runtime_mcp_probe', path)
    if spec is None or spec.loader is None:
        raise RuntimeError('cannot load Runtime MCP probe')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def key_occurrences(value: Any, target: str, prefix: str = '') -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            path = f'{prefix}.{key}' if prefix else key
            if key == target:
                found.append({'path': path, 'schema': item})
            found.extend(key_occurrences(item, target, path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(key_occurrences(item, target, f'{prefix}[{index}]'))
    return found


def canonical_digest(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
    return 'sha256:' + hashlib.sha256(raw).hexdigest()


def runtime_catalog() -> dict[str, Any]:
    probe = load_runtime_probe()
    environment = probe.load_environment_file(RUNTIME_ENV)
    token = probe.load_bearer_token(environment)
    client = probe.McpClient(RUNTIME_ENDPOINT, token, 'ordivon-p1b-runtime-probe')
    discovery = client.discover()
    tools = client.request('tools/list').get('tools')
    if not isinstance(tools, list):
        raise RuntimeError('Runtime tools/list omitted tools')
    workspace_exec = next(tool for tool in tools if tool.get('name') == 'workspace.exec')
    input_schema = workspace_exec.get('inputSchema', {})
    meta = discovery.get('_meta', {}) if isinstance(discovery, dict) else {}
    return {
        'endpointClass': 'loopback-owner-native',
        'protocolVersion': '2026-07-28',
        'toolCount': len(tools),
        'toolNames': sorted(tool['name'] for tool in tools if isinstance(tool, dict) and isinstance(tool.get('name'), str)),
        'toolCatalogDigest': meta.get('com.ordivon/runtime/toolCatalogDigest'),
        'workspaceExecInputSchemaDigest': canonical_digest(input_schema),
        'executionTarget': key_occurrences(input_schema, 'executionTarget'),
        'windowsAuthority': key_occurrences(input_schema, 'windowsAuthority'),
    }


def host_exchange(token: str, payload: dict[str, Any], *, body: bool = True) -> Any:
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/event-stream',
        'MCP-Protocol-Version': '2025-11-25',
    }
    request = urllib.request.Request(
        HOST_ENDPOINT,
        data=json.dumps(payload, separators=(',', ':')).encode('utf-8'),
        method='POST',
        headers=headers,
    )
    with urllib.request.urlopen(request, timeout=5.0) as response:
        raw = response.read()
        return response.status if not body else json.loads(raw)


def host_catalog() -> dict[str, Any]:
    token = HOST_TOKEN_FILE.read_text(encoding='utf-8').strip()
    if not token or any(character.isspace() for character in token):
        raise RuntimeError('Host token file does not contain one non-whitespace token')
    initialized = host_exchange(
        token,
        {
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'initialize',
            'params': {
                'protocolVersion': '2025-11-25',
                'capabilities': {},
                'clientInfo': {'name': 'ordivon-p1b-host-probe', 'version': '1'},
            },
        },
    )
    host_exchange(token, {'jsonrpc': '2.0', 'method': 'notifications/initialized'}, body=False)
    listed = host_exchange(token, {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list', 'params': {}})
    result = listed.get('result', {}) if isinstance(listed, dict) else {}
    tools = result.get('tools')
    if not isinstance(tools, list):
        raise RuntimeError('Host tools/list omitted tools')
    checkpoint = next(tool for tool in tools if tool.get('name') == 'task.checkpoint')
    input_schema = checkpoint.get('inputSchema', {})
    initialize_result = initialized.get('result', {}) if isinstance(initialized, dict) else {}
    return {
        'endpointClass': 'loopback-owner-native',
        'protocolVersion': initialize_result.get('protocolVersion'),
        'toolCount': len(tools),
        'toolNames': sorted(tool['name'] for tool in tools if isinstance(tool, dict) and isinstance(tool.get('name'), str)),
        'taskCheckpointInputSchemaDigest': canonical_digest(input_schema),
        'continuityDisposition': key_occurrences(input_schema, 'continuityDisposition'),
    }


def run() -> dict[str, Any]:
    runtime = runtime_catalog()
    host = host_catalog()
    if not runtime['executionTarget'] or not runtime['windowsAuthority']:
        raise RuntimeError('live Runtime workspace.exec lacks expected Windows fields')
    if not host['continuityDisposition']:
        raise RuntimeError('live Host task.checkpoint lacks continuityDisposition')
    return {
        'schemaVersion': 1,
        'kind': 'ordivon.p1b-live-mcp-catalog-observation',
        'createdAt': now_iso(),
        'privacy': {
            'credentialsIncluded': False,
            'credentialValuesPrinted': False,
            'rawEnvironmentIncluded': False,
        },
        'owners': {
            'runtime': {
                'repositoryRevision': git_head(RUNTIME_ROOT),
                'repositoryDirty': git_dirty(RUNTIME_ROOT),
                'service': service_state('ordivon-runtime.service'),
                'catalog': runtime,
            },
            'host': {
                'repositoryRevision': git_head(HOST_ROOT),
                'repositoryDirty': git_dirty(HOST_ROOT),
                'service': service_state('ordivon-host-mcp.service'),
                'catalog': host,
            },
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description='Safely observe current owner-native Host/Runtime MCP catalogs')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        receipt = run()
        rendered = json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + '\n'
        if args.output is not None:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding='utf-8')
        print(rendered, end='')
        return 0
    except Exception as error:
        print(f'P1-B live catalog probe: {type(error).__name__}: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
