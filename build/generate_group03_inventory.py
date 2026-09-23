#!/usr/bin/env python3
"""Generate the Group III code inventory by joining ICCC-2017.sqlite to icdo32.sqlite.

Thin shim over `build/generate_group_inventory.py`, which holds the actual join logic and
serves any main group I-XII. This file exists only so that nothing already invoking it by
name breaks, and it fixes the group to III **by construction**: it has no `--group` option
on its own command line at all, and calls `generate_group_inventory.build_inventory()`
directly with `group="III"` as a Python argument, not as a value threaded through another
parser's argv. A flag forwarded through argv can be overridden by a same-named flag the
caller supplies (argparse keeps the last occurrence of a repeated option), which would
silently swap the group while keeping this script's own provenance string. There is nothing
here for that kind of override to land on.

`_generated_by` in the output is pinned to this file's own path (not the generalised
module's default), so Group III's inventory stays byte-identical to what this script produced
before the generalisation.

    python3 build/generate_group03_inventory.py --out /tmp/g3_inventory.json
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_group_inventory as _impl  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--iccc", default=os.environ.get("ICCC_DB", str(_impl.DEFAULT_ICCC)))
    ap.add_argument("--icdo", default=os.environ.get("ICDO_DB", str(_impl.DEFAULT_ICDO)))
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)

    iccc_path, icdo_path = Path(args.iccc), Path(args.icdo)
    for p in (iccc_path, icdo_path):
        if not p.exists():
            print("missing database: %s" % p, file=sys.stderr)
            return 2

    payload = _impl.build_inventory(
        iccc_path, icdo_path, group="III", generated_by="build/generate_group03_inventory.py"
    )
    _impl.emit(payload, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
