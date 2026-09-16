#!/usr/bin/env python3
"""Generate the Group III code inventory by joining ICCC-2017.sqlite to icdo32.sqlite.

Pathway Revision 2 §1.1 / §1.1b: `morphology_entries[]` for Group 3 is GENERATED from the
two databases, never transcribed from an option file. This script is that generation.

ICCC-2017.sqlite supplies subgroup, code range, topography constraint and behaviour range.
icdo32.sqlite supplies existence, available behaviours and the preferred/related/synonym
term strings.

Output: JSON on stdout (or --out), one record per (code, behaviour) that ICD-O-3.2 actually
carries, restricted to the behaviours ICCC-3 declares for the group.

    python3 build/generate_group03_inventory.py --out /tmp/g3_inventory.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_LAYER1 = REPO.parents[1] / "ICD coding"
DEFAULT_ICCC = REPO.parents[1] / "ICCC-2017.sqlite"

MAIN_GROUP = "III"


def parse_behaviour_declaration(raw: str) -> set[str]:
    """'0-1,3' -> {'0','1','3'}. Ranges are inclusive over single digits."""
    out: set[str] = set()
    for token in str(raw or "").split(","):
        token = token.strip()
        if not token:
            continue
        m = re.fullmatch(r"(\d)\s*-\s*(\d)", token)
        if m:
            lo, hi = int(m.group(1)), int(m.group(2))
            out.update(str(d) for d in range(lo, hi + 1))
        elif re.fullmatch(r"\d", token):
            out.add(token)
        else:
            raise ValueError("unparsable behaviour declaration token: %r" % token)
    return out


def load_iccc(path: Path) -> dict:
    con = sqlite3.connect("file:%s?mode=ro" % path, uri=True)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        """
        SELECT mc.code            AS code,
               g.group_code       AS subgroup_id,
               g.group_label      AS subgroup_name,
               cr.icdo3_behavior  AS behaviour_decl,
               cr.range_id        AS range_id
        FROM morphology_codes mc
        JOIN groups g       ON g.group_id = mc.group_id
        JOIN code_ranges cr ON cr.range_id = mc.range_id
        WHERE g.main_group = ?
        ORDER BY mc.code, g.group_code
        """,
        (MAIN_GROUP,),
    ).fetchall()

    topo: dict[int, list[str]] = {}
    for r in con.execute(
        "SELECT range_id, display FROM topography_segments ORDER BY range_id, id"
    ):
        topo.setdefault(r["range_id"], []).append(r["display"])
    con.close()

    out = []
    for r in rows:
        out.append(
            {
                "code": r["code"],
                "iccc3_subgroup_id": r["subgroup_id"],
                "iccc3_subgroup_name": r["subgroup_name"],
                "behaviour_declaration": r["behaviour_decl"],
                "behaviours_allowed": sorted(parse_behaviour_declaration(r["behaviour_decl"])),
                "topography": topo.get(r["range_id"], []),
            }
        )
    return out


def load_icdo(path: Path) -> dict:
    con = sqlite3.connect("file:%s?mode=ro" % path, uri=True)
    con.row_factory = sqlite3.Row
    terms: dict[tuple[str, str], dict[str, list[str]]] = {}
    for r in con.execute(
        "SELECT code4, behaviour, level, term FROM icd_o_3_2_morphology "
        "WHERE code4 IS NOT NULL AND behaviour IS NOT NULL"
    ):
        key = (str(r["code4"]), str(r["behaviour"]))
        terms.setdefault(key, {}).setdefault(str(r["level"] or "").strip(), []).append(
            str(r["term"] or "")
        )
    con.close()
    return terms


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--iccc", default=os.environ.get("ICCC_DB", str(DEFAULT_ICCC)))
    ap.add_argument("--icdo", default=os.environ.get(
        "ICDO_DB", str(DEFAULT_LAYER1 / "ICD-O-3.2" / "icdo32.sqlite")))
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)

    iccc_path, icdo_path = Path(args.iccc), Path(args.icdo)
    for p in (iccc_path, icdo_path):
        if not p.exists():
            print("missing database: %s" % p, file=sys.stderr)
            return 2

    iccc_rows = load_iccc(iccc_path)
    icdo_terms = load_icdo(icdo_path)

    records = []
    absent_codes = []
    for row in iccc_rows:
        code = row["code"]
        present = {b for (c, b) in icdo_terms if c == code}
        if not present:
            absent_codes.append(code)
            continue
        usable = sorted(present & set(row["behaviours_allowed"]))
        if not usable:
            absent_codes.append(code)
            continue
        for behaviour in usable:
            bucket = icdo_terms[(code, behaviour)]
            preferred = bucket.get("Preferred", [])
            records.append(
                {
                    "morphology_code": code,
                    "behavior_code": behaviour,
                    "preferred_term": preferred[0] if preferred else None,
                    "related_terms": bucket.get("Related", []),
                    "synonyms": bucket.get("Synonym", []),
                    "other_levels": {
                        k: v for k, v in bucket.items()
                        if k not in ("Preferred", "Related", "Synonym")
                    },
                    "iccc3_subgroup_id": row["iccc3_subgroup_id"],
                    "iccc3_subgroup_name": row["iccc3_subgroup_name"],
                    "topography": row["topography"],
                    "behaviour_declaration": row["behaviour_declaration"],
                    "behaviours_in_icdo32": sorted(present),
                    "behaviours_outside_declaration": sorted(
                        present - set(row["behaviours_allowed"])
                    ),
                }
            )

    distinct_codes = sorted({r["morphology_code"] for r in records})
    payload = {
        "_generated_by": "build/generate_group03_inventory.py",
        "_sources": {
            "iccc": str(iccc_path),
            "icdo": str(icdo_path),
        },
        "summary": {
            "iccc_code_range_entries": len(iccc_rows),
            "iccc_distinct_codes": len({r["code"] for r in iccc_rows}),
            "codes_absent_from_icdo32": sorted(set(absent_codes)),
            "usable_distinct_codes": len(distinct_codes),
            "morphology_entry_records": len(records),
            "behaviour_declarations": sorted({r["behaviour_declaration"] for r in iccc_rows}),
        },
        "records": records,
    }

    text = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print("wrote %s" % args.out, file=sys.stderr)
    else:
        print(text)

    s = payload["summary"]
    print(
        "ICCC range entries %d · distinct codes %d · absent from ICD-O-3.2 %d · usable %d · "
        "(code,behaviour) records %d"
        % (
            s["iccc_code_range_entries"],
            s["iccc_distinct_codes"],
            len(s["codes_absent_from_icdo32"]),
            s["usable_distinct_codes"],
            s["morphology_entry_records"],
        ),
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
