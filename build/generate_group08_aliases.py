#!/usr/bin/env python3
"""Generate data/aliases/aliases_group_08.json for ICCC-3 Group VIII.

Group 8 build contract §6. Three sources, merged by alias string (first source wins):

  1. ICD-O-3.2 terms on the group's 48 usable (code, behaviour) records, read from
     group_08_dt.json's entries and icdo32.sqlite. Generic VIIIe synonyms that would send a
     search to the wrong group are excluded (EXCLUDED_TERMS).
  2. viii_morph option strings that ICD-O-3.2 does not carry verbatim (contract §2).
  3. WHO 2020 / WHO 2022 names and clinical wordings, CURATED below, taken from
     'Group 8 — Alias Build Instructions.md' (14 May 2026) with that file's NCIt concept
     IDs, and corrected where it predates ICD-O-3.2: every Ewing sarcoma alias maps to
     9364, never 9260 (design D1), and 'Conventional osteosarcoma' maps to 9180 (D9).

Benign and intermediate terms are not aliased: the express lane is for codes this group
emits. Run after build/generate_group08_entries.py:

    python3 build/generate_group08_aliases.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_database as bd  # noqa: E402
import generate_group_inventory as gi  # noqa: E402
import group08_tree  # noqa: E402

DT = REPO / "data" / "database" / "group_08_dt.json"
OUT = REPO / "data" / "aliases" / "aliases_group_08.json"
ICDO_PATH = Path(os.environ.get("ICDO_DB", str(gi.DEFAULT_ICDO)))
TREE, ENTRY = group08_tree.TREE_ID, group08_tree.ENTRY

# ICD-O-3.2 terms on Group VIII stems that would mislead in a bone search.
EXCLUDED_TERMS = {
    "Osteosarcoma, extraskeletal": "extraskeletal osteosarcoma is ICCC-3 IXd9, not Group VIII",
    "Soft tissue sarcoma": "a soft tissue term; at a bone site the code is VIIIe but the "
                           "wording would pull soft-tissue searches into Group VIII",
    "Soft tissue tumor, malignant": "as above",
    "Mesenchymal tumor, malignant": "generic; reached through the tree",
    "Cancer": "generic; matches every group",
    "Malignancy": "generic; matches every group",
    "Tumor, malignant, NOS": "generic; matches every group",
    "Unclassified tumor, malignant": "generic; matches every group",
    "Blastoma, NOS": "generic; a blastoma in a child is almost never a bone tumour",
    "Malignant tumor, fusiform cell type": "generic descriptor",
    "Fibroxanthoma, malignant": "a soft tissue term",
}

# Appended to every ICD-O-3.2-term alias on the code.
NOTE_SUFFIX = {
    "9364": " Not 9260: ICD-O-3.2 moved Ewing sarcoma to 9364, and 9260 now means aneurysmal "
            "bone cyst, a benign lesion.",
    "9310": " An odontogenic (jaw) tumour. Adamantinoma of the long bones is a different code, "
            "9261/3.",
}

# alias, codes, alias_type, origin_system, nci_concept_id, who_version, notes
CURATED = [
    ("Osteosarcoma", ["9180"], "descriptive", "WHO Classification 2020", "NCIT:C9145", "WHO 2020",
     "The commonest malignant bone tumour of adolescence. Coded Osteosarcoma, NOS (9180/3) "
     "unless the report names a subtype that has its own code."),
    ("OS", ["9180"], "abbreviation", "Clinical abbreviation", "NCIT:C9145", "WHO 2020",
     "Clinical shorthand for osteosarcoma. Confirm the report means osteosarcoma before using "
     "it: OS also abbreviates overall survival."),
    ("Osteogenic sarcoma", ["9180"], "who_historical", "Historical nomenclature", "NCIT:C9145",
     "historical", "The older name for osteosarcoma; coded Osteosarcoma, NOS (9180/3)."),
    ("Conventional osteosarcoma", ["9180"], "who_preferred", "WHO Classification 2020",
     "NCIT:C35870", "WHO 2020",
     "WHO 2020 codes conventional osteosarcoma 9180/3. A report that says central or medullary "
     "osteosarcoma is coded as written, 9186/3."),
    ("Secondary osteosarcoma", ["9184"], "who_preferred", "WHO Classification 2020",
     "NCIT:C6469", "WHO 2020",
     "WHO 2020's name for 9184/3, the code ICD-O-3.2 calls Osteosarcoma in Paget disease of "
     "bone."),
    ("Chondrosarcoma", ["9220"], "descriptive", "WHO Classification 2020", "NCIT:C2946",
     "WHO 2020",
     "Chondrosarcoma grade 2 or 3, or with no grade stated, is 9220/3. Chondrosarcoma grade 1 "
     "is not coded here: ICD-O-3.2 puts it with atypical cartilaginous tumour at 9222/1, "
     "outside Group VIII, and the registrar has the question."),
    ("Ewing tumour", ["9364"], "eponym", "UK/East African clinical spelling", "NCIT:C4817",
     "WHO 2020",
     "Ewing sarcoma, coded 9364/3 since ICD-O-3.2. Not 9260: that number now means aneurysmal "
     "bone cyst, a benign lesion."),
    ("ES", ["9364"], "abbreviation", "Clinical abbreviation", "NCIT:C4817", "WHO 2020",
     "Clinical shorthand for Ewing sarcoma, 9364/3."),
    ("Ewing sarcoma family of tumours", ["9364", "9365"], "descriptive", "Clinical descriptive",
     "NCIT:C27291", "historical",
     "An older umbrella for Ewing sarcoma, Askin tumour and peripheral neuroectodermal tumour. "
     "Ewing sarcoma and peripheral neuroectodermal tumour are 9364/3; a report using the term "
     "Askin tumour is 9365/3."),
    ("PNET of bone", ["9364"], "abbreviation", "Clinical abbreviation", "NCIT:C9341",
     "historical",
     "Peripheral neuroectodermal tumour of bone is Ewing sarcoma, 9364/3. PNET without "
     "'peripheral' in a brain or spinal cord report is a different, Group III code."),
    ("Peripheral primitive neuroectodermal tumor of bone", ["9364"], "who_historical",
     "ICD-O-3.2 synonym", "NCIT:C9341", "historical",
     "An ICD-O-3.2 term on 9364/3, Ewing sarcoma."),
    ("Askin tumour", ["9365"], "eponym", "UK/East African clinical spelling", "NCIT:C7542",
     "historical",
     "Coded as written, 9365/3. A chest-wall tumour the report calls Ewing sarcoma is 9364/3."),
    ("Fibrosarcoma of bone", ["8810"], "descriptive", "WHO Classification 2020", "NCIT:C3043",
     "WHO 2020", "Fibrosarcoma, NOS (8810/3), VIIId1 at a bone site."),
    ("Malignant fibrous histiocytoma of bone", ["8830"], "who_historical",
     "Historical nomenclature", "NCIT:C8563", "historical",
     "The older name for undifferentiated pleomorphic sarcoma of bone; coded 8830/3."),
    ("MFH of bone", ["8830"], "abbreviation", "Clinical abbreviation", "NCIT:C8563", "historical",
     "Malignant fibrous histiocytoma of bone, coded 8830/3."),
    ("Undifferentiated pleomorphic sarcoma of bone", ["8830"], "who_preferred",
     "WHO Classification 2020", "NCIT:C8563", "WHO 2020",
     "Coded 8830/3, the ICD-O-3.2 code carrying 'Undifferentiated high grade pleomorphic "
     "sarcoma of bone'. WHO 2020 prints 8802/3, which ICCC-3 has no bone range for; the "
     "registrar has the question."),
    ("UPS of bone", ["8830"], "abbreviation", "Clinical abbreviation", "NCIT:C8563", "WHO 2020",
     "Undifferentiated pleomorphic sarcoma of bone, coded 8830/3."),
    ("Chordoma", ["9370"], "descriptive", "WHO Classification 2020", "NCIT:C2947", "WHO 2020",
     "Chordoma, NOS (9370/3)."),
    ("Conventional chordoma", ["9370"], "who_preferred", "WHO Classification 2020", None,
     "WHO 2020", "WHO 2020 Table 1, 9370/3."),
    ("Poorly differentiated chordoma", ["9370"], "who_preferred", "WHO Classification 2020",
     None, "WHO 2020",
     "WHO 2020 codes poorly differentiated chordoma 9370/3. It occurs in children at the skull "
     "base and upper neck, with SMARCB1 (INI1) loss."),
    ("Malignant odontogenic tumour", ["9270"], "descriptive",
     "UK/East African clinical spelling", "NCIT:C4812", "WHO 2022",
     "Odontogenic tumor, malignant (9270/3)."),
    ("Sclerosing odontogenic carcinoma", ["9270"], "who_preferred",
     "WHO Classification of Head and Neck Tumours 2022", None, "WHO 2022",
     "ICD-O-3.2 has no term for it; coded 9270/3 through the synonym Odontogenic carcinoma. "
     "The registrar has the question."),
    ("Metastasizing ameloblastoma", ["9310"], "who_preferred",
     "WHO Classification of Head and Neck Tumours 2022", "NCIT:C54297", "WHO 2022",
     "Coded 9310/3, Ameloblastoma, metastasizing. Ordinary ameloblastoma is benign, 9310/0, "
     "and is not a Group VIII cancer."),
    ("Giant cell tumour of bone, malignant", ["9250"], "descriptive",
     "UK/East African clinical spelling", "NCIT:C4304", "WHO 2020",
     "Malignant giant cell tumour of bone, 9250/3. Giant cell tumour of bone without "
     "'malignant' is 9250/1, outside Group VIII."),
    ("Malignant giant cell tumour of bone", ["9250"], "descriptive", "Clinical descriptive",
     "NCIT:C4304", "WHO 2020", "9250/3."),
    ("Dedifferentiated adamantinoma", ["9261"], "who_preferred", "WHO Classification 2020",
     None, "WHO 2020", "WHO 2020 lists it under adamantinoma of long bones, 9261/3."),
    ("CIC-rearranged sarcoma", ["8803"], "who_preferred", "WHO Classification 2020", None,
     "WHO 2020",
     "ICD-O-3.2 has no code for it. Coded Small cell sarcoma (8803/3), whose synonym is Round "
     "cell sarcoma, NOS. The registrar has the question."),
    ("Sarcoma with BCOR genetic alterations", ["8803"], "who_preferred",
     "WHO Classification 2020", None, "WHO 2020",
     "ICD-O-3.2 has no code for it. Coded Small cell sarcoma (8803/3)."),
    ("BCOR-rearranged sarcoma", ["8803"], "molecular", "Molecular / cytogenetic notation", None,
     "WHO 2020", "Sarcoma with BCOR genetic alterations; coded Small cell sarcoma (8803/3)."),
    ("Round cell sarcoma with EWSR1-non-ETS fusions", ["8803"], "who_preferred",
     "WHO Classification 2020", None, "WHO 2020",
     "ICD-O-3.2 has no code for it. Coded Small cell sarcoma (8803/3)."),
    ("Undifferentiated small round cell sarcoma of bone", ["8803"], "descriptive",
     "Clinical descriptive", None, "WHO 2020",
     "Coded Small cell sarcoma (8803/3) at a bone site."),
    ("Bone cancer", ["8000"], "local", "Local referral letter terminology", None, "N/A",
     "Not a diagnosis. Work through the Group VIII tree from the evidence in the file; with no "
     "imaging or pathology it records only Neoplasm, malignant (8000/3)."),
    ("Bone tumour", ["8000"], "descriptive", "Clinical descriptive", None, "N/A",
     "Not a diagnosis, and may be benign. Work through the Group VIII tree from the evidence "
     "in the file."),
    ("Malignant bone tumour", ["8000"], "descriptive", "Clinical descriptive", None, "N/A",
     "Not a specific diagnosis. Work through the Group VIII tree from the evidence in the "
     "file."),
    ("Bone sarcoma", ["8800"], "descriptive", "Clinical descriptive", "NCIT:C9312", "N/A",
     "Sarcoma, NOS (8800/3) when the report names no type; work through the tree if it does."),
]
NEEDS_TREE = {"Bone cancer", "Bone tumour", "Malignant bone tumour", "Bone sarcoma"}

# viii_morph strings ICD-O-3.2 does not carry verbatim (contract §2).
REDCAP_ONLY = [
    ("Central osteosarcoma", "9186",
     "The viii_morph option string for 9186. ICD-O-3.2's term is Central osteosarcoma, NOS."),
]


def main() -> int:
    dt = json.loads(DT.read_text(encoding="utf-8"))
    entries = {(e["morphology_code"], e["behavior_code"]): e for e in dt["morphology_entries"]}
    by_code = {c: e for (c, _), e in entries.items()}
    # The express lane enters the tree, so an alias is useful only for a code the tree can
    # emit. Codes kept off the tree (design D14) get no alias.
    ctx = bd.DTContext(DT, dt, 8)
    emitted = {code for code, *_ in ctx.emissions()} | {
        bd.as_code(n["nos_fallback"].get("code")) for n in ctx.nodes.values()
        if isinstance(n.get("nos_fallback"), dict)}
    index, err = bd.load_icdo32(ICDO_PATH.parent.parent)
    if err:
        raise SystemExit("ERROR: %s" % err)
    terms = {key: [(level, term, obs) for term, (level, obs) in index[key].items()]
             for key in entries if key in index}

    out, seen = [], set()

    def add(alias, codes, alias_type, origin, nci, who, notes, coding_note, aka=None):
        if not set(codes) <= emitted or alias.lower() in seen:
            return
        seen.add(alias.lower())
        e0 = by_code[codes[0]]
        names = " / ".join("%s (%s)" % (by_code[c]["morphology_name"], c) for c in codes)
        out.append({
            "alias": alias,
            "full_form": "%s -> %s" % (alias, names),
            "also_known_as": aka or [],
            "alias_type": alias_type,
            "origin_system": origin,
            "nci_concept_id": nci,
            "who_version_current": who,
            "maps_to_morphology_codes": codes,
            "maps_to_iccc3_subgroup_id": e0["iccc3_subgroup_id"],
            "needs_ihc_tree": alias in NEEDS_TREE,
            "ihc_tree_id": TREE,
            "tree_entry_node": ENTRY,
            "clinical_alert": None,
            "notes": notes,
            "coding_note": coding_note,
        })

    # 1. ICD-O-3.2 terms.
    for (code, beh), e in sorted(entries.items()):
        for level, term, obs in terms.get((code, beh), []):
            if term in EXCLUDED_TERMS:
                continue
            preferred = level == "Preferred"
            add(term, [code],
                "who_historical" if obs else ("who_preferred" if preferred else "descriptive"),
                "ICD-O-3.2" if preferred else "ICD-O-3.2 synonym",
                None, "historical" if obs else e["who_version"],
                (("%s, %s/%s." % (e["morphology_name"], code, beh)) if preferred else
                ("An ICD-O-3.2 %s term for %s (%s/%s)." % (level.lower(), e["morphology_name"],
                                                           code, beh)))
                + NOTE_SUFFIX.get(code, ""),
                "ICD-O-3.2 %s term on %s/%s, read from icdo32.sqlite%s."
                % (level, code, beh, " ([obs])" if obs else ""))
    # 2. REDCap-only strings.
    for alias, code, notes in REDCAP_ONLY:
        add(alias, [code], "local", "Local registry option list", None, "N/A", notes,
            "viii_morph option string with no verbatim ICD-O-3.2 match (contract §2).")
    # 3. Curated WHO and clinical names.
    for alias, codes, at, origin, nci, who, notes in CURATED:
        add(alias, codes, at, origin, nci, who, notes,
            "Curated from 'Group 8 — Alias Build Instructions.md' (14 May 2026)%s, corrected "
            "to ICD-O-3.2 by the Group 8 build (design D1-D15)."
            % (", NCIt " + nci if nci else ""))
    # The express-lane search is a substring match, so 'X, NOS' adds nothing to an index
    # that already holds 'X' for the same code; it only grows the startup index (TODO §23).
    bare = {(a["alias"].lower(), tuple(a["maps_to_morphology_codes"])) for a in out}
    out = [a for a in out if not (a["alias"].endswith(", NOS") and
                                  (a["alias"][:-5].lower(), tuple(a["maps_to_morphology_codes"]))
                                  in bare)]
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote %s (%d aliases)" % (OUT, len(out)), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
