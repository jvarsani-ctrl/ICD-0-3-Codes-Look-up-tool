#!/usr/bin/env python3
"""Generate the Group III code inventory by joining ICCC-2017.sqlite to icdo32.sqlite.

Thin shim. The generation logic now lives in `build/generate_group_inventory.py`, which
takes `--group` as a Roman numeral and serves Groups I-XII. This file is kept, unchanged in
behaviour and output, so that nothing that already invokes it by name breaks; it forwards
every argument it receives and pins `--group III`.

`_generated_by` in the output is pinned to this file's own path (not the generalised
module's), so Group III's inventory stays byte-identical to what this script produced before
the generalisation — see `docs/group_04_build_contract.md` Deliverable A.

    python3 build/generate_group03_inventory.py --out /tmp/g3_inventory.json
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_group_inventory as _impl  # noqa: E402


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    return _impl.main(["--group", "III", "--generated-by", "build/generate_group03_inventory.py", *argv])


if __name__ == "__main__":
    raise SystemExit(main())
