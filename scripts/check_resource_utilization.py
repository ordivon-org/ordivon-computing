#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "research" / "resource-utilization-ru0-ru10-v1.json"


def main() -> None:
    value = json.loads(DATA.read_text())
    assert value["schemaVersion"] == 1
    assert value["kind"] == "ordivon.computing.resource-utilization-audit"
    assert value["series"] == [f"RU{i}" for i in range(11)]

    p = value["principles"]
    assert p["globalRegistryPromoted"] is False
    assert p["capabilityManagerPromoted"] is False
    assert p["universalScorePromoted"] is False
    assert p["resourceCountIsCapability"] is False
    assert p["nodeCountIsRedundancy"] is False
    assert p["availableCapabilityIsExpandedUsefulWork"] is False
    assert p["ownerNativeTruthRequired"] is True

    cards = value["resourceCards"]
    assert len(cards) >= 8
    required = {"id","owner","stage","consumer","evidence","deletionEffect","bottleneck","complements","revalidateAtUse"}
    ids = set()
    for card in cards:
        assert required <= card.keys()
        assert card["id"] not in ids
        ids.add(card["id"])
        assert card["owner"] and card["stage"] and card["consumer"]
        assert isinstance(card["evidence"], list) and card["evidence"]
        assert card["deletionEffect"] and card["bottleneck"]
        assert isinstance(card["complements"], list)
        assert isinstance(card["revalidateAtUse"], bool)

    priorities = value["priorities"]
    assert priorities
    assert [x["rank"] for x in priorities] == list(range(1, len(priorities) + 1))
    assert all(x["level"] in {"P0", "P1", "P2", "P3"} for x in priorities)
    assert all("repair Runtime Windows" not in x["action"] for x in priorities)
    assert all("restore one current finance-okx" not in x["action"] for x in priorities)

    forbidden = {
        "Global Resource Registry",
        "Capability Manager",
        "universal resource value score",
    }
    assert forbidden <= set(value["nonPromotions"])

    print(json.dumps({
        "ok": True,
        "series": len(value["series"]),
        "resourceCards": len(cards),
        "priorities": len(priorities),
        "globalRegistryPromoted": p["globalRegistryPromoted"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
