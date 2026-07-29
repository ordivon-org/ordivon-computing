from __future__ import annotations

from anc_core_work_system.cli import main


if __name__ == "__main__":
    raise SystemExit(main(["matrix", *__import__("sys").argv[1:]]))
