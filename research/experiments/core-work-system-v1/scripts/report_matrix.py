from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("matrix")
    args = parser.parse_args()
    value = json.loads(Path(args.matrix).read_text("utf-8"))
    print(json.dumps(value["summary"], indent=2, sort_keys=True))
    print("\nvariant\tpackage\taccepted\tdisposition\thard_failures")
    for trial in value["trials"]:
        spec = trial["spec"]
        print(
            f"{spec['variant']}\t{spec['workPackage']}\t{trial['acceptedOutcome']}\t"
            f"{trial['disposition']}\t{','.join(trial['hardFailures'])}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
