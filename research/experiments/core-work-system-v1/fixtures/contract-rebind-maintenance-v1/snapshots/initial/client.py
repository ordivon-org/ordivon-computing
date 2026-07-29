from __future__ import annotations

def request_payload(steps: list[dict[str, object]]) -> dict[str, object]:
    return {'schemaVersion': 0, 'steps': steps}
