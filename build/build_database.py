#!/usr/bin/env python3
"""
build_database.py
Parses Cancer Registry vault Markdown files and generates:
  - data/database/group_01_leukemias.json  (through group_12)
  - data/topography_codes.json

Usage: python3 build/build_database.py
"""

import json, re
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
VAULT       = Path("/Users/jay/Library/CloudStorage/OneDrive-UGANDACHILDCANCERFOUNDATION/Main Vault/02 Projects/Cancer Registry")
REDCAP_OPTS = VAULT / "ICD coding" / "RedCap Options"
MORPHOLOGY  = VAULT / "Morphology"
OUT_DB      = Path(__file__).parent.parent / "data" / "database"
OUT_TOPO    = Path(__file__).parent.parent / "data" / "topography_codes.json"

# ── Group catalogue ─────────────────────────────────────────────────────────────
GROUPS = [
    (1,  "I",    "Leukemias, Myeloproliferative And Myelodysplastic Diseases",
         "Group 1-  Leukemias, Myeloproliferative And Myelodysplastic Diseases.md",
         "group 1.md",  "group_01_leukemias.json"),
    (2,  "II",   "Lymphomas And Reticuloendothelial Neoplasms",
         "Group 2- Lymphomas And Reticuloendothelial Neoplasms.md",
         "group 2.md",  "group_02_lymphomas.json"),
    (3,  "III",  "CNS And Miscellaneous Intracranial And Intraspinal Neoplasms",
         "Group 3 - Cns And Miscellaneous Intracranial And Intraspinal Neoplasms.md",
         "group 3.md",  "group_03_cns.json"),
    (4,  "IV",   "Neuroblastoma And Other Peripheral Nervous Cell Tumors",
         "Group 4- Neuroblastoma And Other Peripheral Nervous Cell Tumors.md",
         "group 4.md",  "group_04_neuroblastoma.json"),
    (5,  "V",    "Retinoblastoma",
         "Group 5- Retinoblastoma.md",
         "group 5.md",  "group_05_retinoblastoma.json"),
    (6,  "VI",   "Renal Tumors",
         "Group 6 - Renal Tumors.md",
         "group 6.md",  "group_06_renal.json"),
    (7,  "VII",  "Hepatic Tumors",
         "Group 7- Hepatic Tumors.md",
         "group 7.md",  "group_07_hepatic.json"),
    (8,  "VIII", "Malignant Bone Tumors",
         "Group 8- Malignant Bone Tumors.md",
         "group 8.md",  "group_08_bone.json"),
    (9,  "IX",   "Soft Tissue And Other Extraosseous Sarcomas",
         "Group 9- Soft Tissue And Other Extraosseous Sarcomas.md",
         "group 9.md",  "group_09_soft_tissue.json"),
    (10, "X",    "Germ Cell Tumors, Trophoblastic Tumors And Neoplasms Of Gonads",
         "Group 10- Germ Cell Tumors, Trophoblastic Tumors And Neoplasms Of Gonads.md",
         "group 10.md", "group_10_germ_cell.json"),
    (11, "XI",   "Other Malignant Epithelial Neoplasms And Malignant Melanomas",
         "Group 11- Other Malignant Epithelial Neoplasms And Malignant Melanomas.md",
         "group 11.md", "group_11_epithelial.json"),
    (12, "XII",  "Other And Unspecified Malignant Neoplasms",
         "Group 12- Other And Unspecified Malignant Neoplasms.md",
         "group 12.md", "group_12_other.json"),
]

# Roman numeral pattern (order matters — longer first)
ROMAN = r'(?:XII|VIII|VII|VI|IV|IX|XI|III|II|X|V|I)'
RE_SUBGROUP_HEADER = re.compile(
    rf'^(#{{2,3}})\s+({ROMAN}[a-z]?\d*)[:.]?\s*(.*)', re.IGNORECASE
)
# Single entry: "9811, 9811 - B lymphoblastic leukemia/lymphoma, NOS"
RE_ENTRY = re.compile(r'(\d{4}),\s*\d{4}\s*-\s*(.+?)(?=\s+\d{4},\s*\d{4}\s*-|$)')


# ── Parsers ────────────────────────────────────────────────────────────────────

def parse_redcap_options(filepath: Path) -> list:
    """Parse a RedCap Options group file.

    Returns list of subgroups:
      {"subgroup_id": str, "subgroup_name": str, "level": int,
       "entries": [{"code": str, "name": str}]}
    """
    subgroups: list = []
    current = None
    in_code = False

    text = filepath.read_text(encoding='utf-8', errors='replace')

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        # Match any line that is purely backticks (handles ``` or ```` typos)
        if re.match(r'^`{3,}$', stripped):
            in_code = not in_code
            continue

        if not in_code:
            # Also handle H1 headers like "# V Retinoblastoma" (Group V has no sub-headers)
            m = RE_SUBGROUP_HEADER.match(line)
            if not m:
                # Try H1 as a group-level subgroup (e.g. Group V)
                h1 = re.match(rf'^#\s+({ROMAN})\s+(.*)', line, re.IGNORECASE)
                if h1:
                    class _FakeMatch:
                        def group(self, n):
                            return ['', '#', h1.group(1), h1.group(2)][n]
                    m = _FakeMatch()
            if m:
                hashes  = m.group(1)
                sub_id  = m.group(2)
                sub_name = m.group(3)
                current = {
                    "subgroup_id":   sub_id,
                    "subgroup_name": sub_name.strip().rstrip(':').strip(),
                    "level":         len(hashes) if isinstance(hashes, str) else 1,
                    "entries":       [],
                }
                subgroups.append(current)
        else:
            if current is None or not stripped:
                continue
            # A line may contain multiple concatenated entries (formatting artifact)
            # Split by "NNNN, NNNN -" boundaries
            for m in RE_ENTRY.finditer(stripped):
                code = m.group(1).strip()
                name = m.group(2).strip()
                if name:
                    current["entries"].append({"code": code, "name": name})

    return subgroups


def expand_code_ranges(codes_str: str) -> list:
    """'9811-9818,9837' → ['9811','9812',...,'9818','9837']"""
    codes = []
    for part in codes_str.split(','):
        part = part.strip()
        m_range = re.match(r'^(\d{4})-(\d{4})$', part)
        m_single = re.match(r'^(\d{4})$', part)
        if m_range:
            codes += [str(c) for c in range(int(m_range.group(1)), int(m_range.group(2)) + 1)]
        elif m_single:
            codes.append(part)
        # silently skip malformed tokens (e.g. "9C80.9")
    return codes


def parse_morphology_table(filepath: Path) -> dict:
    """Parse a Morphology group table file.

    Returns {subgroup_id: {"name": str,
                            "topography_rules": [{"codes": [str], "primary_sites": str}]}}
    """
    result: dict = {}
    current_id   = None
    current_name = None

    text = filepath.read_text(encoding='utf-8', errors='replace')

    for line in text.splitlines():
        if not line.startswith('|'):
            continue
        cols = [c.strip() for c in line.split('|')]
        cols = [c for c in cols if c]          # drop empty border cells

        if len(cols) < 2:
            continue
        if re.search(r'---', cols[0]) or cols[0].lower() == 'subgroup':
            continue

        subgroup_col = cols[0]
        codes_col    = cols[1] if len(cols) > 1 else ''
        sites_col    = cols[2] if len(cols) > 2 else ''

        # New subgroup row?
        if subgroup_col:
            m = re.match(
                rf'^({ROMAN}[a-zA-Z]?\d*)[\s.:]*(.*)$', subgroup_col, re.IGNORECASE
            )
            if m:
                current_id   = m.group(1)
                current_name = m.group(2).strip()

        # Collect codes + sites for current subgroup
        if codes_col and current_id:
            expanded = expand_code_ranges(codes_col)
            if expanded:
                if current_id not in result:
                    result[current_id] = {"name": current_name, "topography_rules": []}
                result[current_id]["topography_rules"].append({
                    "codes":         expanded,
                    "primary_sites": sites_col,
                })

    return result


def primary_sites_for_code(code: str, rules: list) -> list:
    """Return list of primary-site strings that apply to this code."""
    sites = [r["primary_sites"] for r in rules if code in r["codes"] and r["primary_sites"]]
    return sites if sites else ["C00.0-C80.9"]


def parse_topography(filepath: Path) -> list:
    """Parse Topography Redcap.md.

    Returns [{"code": "C71.6", "numeric": "716", "name": str, "subsites": str}]
    """
    entries = []
    in_code = False

    text = filepath.read_text(encoding='utf-8', errors='replace')

    for line in text.splitlines():
        stripped = line.strip()
        if stripped == '```':
            in_code = not in_code
            continue
        if not in_code or not stripped:
            continue

        # Format: 716, Cerebellum, NOS (subsite, subsite)
        m = re.match(r'^(\d{3}),\s*(.+)$', stripped)
        if not m:
            continue

        numeric = m.group(1)
        rest    = m.group(2).strip()

        # Split name from subsites (subsites in parentheses)
        paren_m = re.match(r'^(.+?)\s*\((.+)\)\s*$', rest)
        if paren_m:
            name     = paren_m.group(1).strip()
            subsites = paren_m.group(2).strip()
        else:
            name     = rest
            subsites = ''

        # 716 → C71.6
        c_code = f"C{numeric[:2]}.{numeric[2]}"

        entries.append({
            "code":     c_code,
            "numeric":  numeric,
            "name":     name,
            "subsites": subsites,
        })

    return entries


# ── Main build ─────────────────────────────────────────────────────────────────

def build_group(group_num, roman, group_name, opts_filename, morph_filename, out_filename):
    print(f"\n  Group {roman}: {group_name}")

    opts_path  = REDCAP_OPTS / opts_filename
    morph_path = MORPHOLOGY  / morph_filename

    subgroups_from_opts = parse_redcap_options(opts_path)
    morph_table         = parse_morphology_table(morph_path)

    output = []
    seen   = set()   # deduplicate (code + subgroup_id)

    for sg in subgroups_from_opts:
        sg_id   = sg["subgroup_id"]
        sg_name = sg["subgroup_name"]

        topo_rules = morph_table.get(sg_id, {}).get("topography_rules", [])
        # Fallback: some sub-subgroup IDs may not appear in the summary table
        # (e.g. IIIa1 vs IIIa), so walk up to parent
        if not topo_rules:
            parent_id = re.match(rf'^({ROMAN}[a-z]?)(\d*)$', sg_id, re.IGNORECASE)
            if parent_id and parent_id.group(2):
                parent_key = parent_id.group(1)
                topo_rules = morph_table.get(parent_key, {}).get("topography_rules", [])

        for entry in sg["entries"]:
            code = entry["code"]
            name = entry["name"]
            key  = (code, sg_id)
            if key in seen:
                continue
            seen.add(key)

            sites = primary_sites_for_code(code, topo_rules)
            topo_dependent = not (len(sites) == 1 and sites[0] == "C00.0-C80.9")

            output.append({
                "morphology_code":      code,
                "morphology_name":      name,
                "iccc3_group":          roman,
                "iccc3_group_name":     group_name,
                "iccc3_subgroup_id":    sg_id,
                "iccc3_subgroup_name":  sg_name,
                "primary_sites":        sites,
                "topography_dependent": topo_dependent,
                "redcap_value":         code,
            })

    out_path = OUT_DB / out_filename
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"    → {len(output)} entries  →  {out_filename}")
    return output


def main():
    OUT_DB.mkdir(parents=True, exist_ok=True)
    print("Building ICCC-3 Lookup Tool database...\n")

    total = 0
    for group_args in GROUPS:
        entries = build_group(*group_args)
        total  += len(entries)

    # Topography
    print("\n  Topography codes...")
    topo_path    = REDCAP_OPTS / "Topography Redcap.md"
    topo_entries = parse_topography(topo_path)
    OUT_TOPO.write_text(json.dumps(topo_entries, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"    → {len(topo_entries)} topography codes  →  topography_codes.json")

    print(f"\n✅  Done — {total} morphology entries + {len(topo_entries)} topography codes\n")


if __name__ == '__main__':
    main()
