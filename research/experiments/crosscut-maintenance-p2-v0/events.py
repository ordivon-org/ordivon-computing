from __future__ import annotations

from typing import Any

_EVENT_TARGETS: dict[str, tuple[str, ...]] = {
    "runtime.release.result": ("source-delivery", "runtime-health"),
    "git.publish.result": ("source-delivery",),
    "workstation.temporary-equipment.acquire": ("temporary-equipment", "workstation-package-policy"),
    "workstation.temporary-equipment.release": ("temporary-equipment", "workstation-package-policy"),
    "runtime.workspace.closed": ("workspace-lifecycle",),
    "runtime.workspace.dirty-review": ("workspace-lifecycle", "dirty-aging"),
}


def targeted_reobservation(event: dict[str, Any]) -> dict[str, Any]:
    kind = str(event.get("kind", ""))
    targets = list(_EVENT_TARGETS.get(kind, ()))
    return {
        "eventKind": kind,
        "targetedSignals": targets,
        "reconcile": bool(targets),
        "fullGlobalScanRequired": False,
        "decision": "targeted_reobserve" if targets else "no_maintenance_trigger",
        "centralEffectAuthorized": False,
    }


def known_event_kinds() -> tuple[str, ...]:
    return tuple(sorted(_EVENT_TARGETS))
