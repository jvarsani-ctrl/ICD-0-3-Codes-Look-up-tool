#!/usr/bin/env python3
"""Generate data/aliases/aliases_group_11.json for ICCC-3 Group XI, other malignant epithelial
neoplasms and malignant melanomas.

Group 11 build contract §6 and cross_group_B (the alias collisions C1 to C16). Modelled on
build/generate_group10_aliases.py. Two sources, merged by alias string (first source wins):

  1. ICD-O-3.2 terms (Preferred, Synonym, Related; never [obs]) of every (code, behaviour) the
     trees emit, read from the trees the way validator rule 3 of Group 10 reads them (code
     branches, immunohistochemistry rule results, imaging_pathway nodes, nos_fallback), never
     from a hand list. A British spelling of each such term that contains "tumor" is written
     beside it ("tumour"), because the trees' option labels use the British form and the
     search box does not fold the two.
  2. Curated names, CURATED below: the British spellings and WHO names the option labels use
     where they differ from ICD-O-3.2.

Design D21 (Group 10) holds. app.js aliasesFor() lists an alias under "Also called" on every
output of a four-digit code, whatever the behaviour. Group 11 emits every code at /3 only, so
the behaviour test is met by construction; the generator still reads it from ICD-O-3.2, and a
term ICD-O-3.2 files under more than one code is not aliased (the alias would name two codes).

Its site form, cross_group_B C15. One Group XI code sits in up to eighteen trees, and a term
that names one organ would print under "Also called" on that code's output at every tree that
emits it. So an organ-naming term becomes an alias of its code only when every tree that emits
the code is that organ's tree. Otherwise it is a CODE-LESS alias (maps_to_morphology_codes is
empty): the search finds it, the site decides the tree, and nothing prints under "Also called".
The ICD-O-3.2 Preferred term is exempt: it is the code's own name, which the output already
prints, and a clerk who types the name of a code must find it. A spelling variant of a Preferred
term (Adrenocortical carcinoma) is the same name and is exempt with it.

Not aliased:
  - "ACC", "NET", "NEC", "GCT", "PTC", "MEC", "NPC": abbreviations that collide (C12 to C14).
  - Any term ICD-O-3.2 files under a behaviour Group 11 does not emit (no tree emits it).
  - Any string another group's alias file already holds, except SHARED_BY_RULING. A string shared with a lower-numbered
    group would enter that group, and one shared with Group 10's gonadal carcinoma picker breaks
    Group 10 rule 8 (check_group10_picker_aliases_stay_unshared). Group 10 holds 227 of the 536
    live /3 terms on Group XI codes, Group 6 nine and Group 3 four. They stay where they are
    (contract §6: Group 11 does not duplicate them), and the generator reports every one.
  - EXCLUDED_TERMS below, one reason per string.

Each alias carries a hand-off tree and entry node, as Group 9 and Group 10 do for a group with
tree_routing: the tree that alone emits the alias's code, else the router's hand-off tree
(g11_unspecified); a code-less alias carries its organ's tree. app.js does not read the two
fields; build_database.check_alias_cross_references resolves them.

Run after build/generate_group11_entries.py and build/induce_flow.py, before
build/generate_group10_aliases.py (whose rule 8 reads this file):

    python3 build/generate_group11_aliases.py

In a git worktree set ICD_LAYER1, ICCC_DB and ICDO_DB first.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_database as bd  # noqa: E402
import generate_group_inventory as gi  # noqa: E402

GROUP = 11
DT = REPO / "data" / "database" / "group_11_dt.json"
ROUTER = REPO / "data" / "shared" / "presentation_router.json"
ALIAS_DIR = REPO / "data" / "aliases"
OUT = ALIAS_DIR / "aliases_group_11.json"
LAYER1 = Path(os.environ.get("ICD_LAYER1", str(gi.DEFAULT_LAYER1)))

LEVELS = ("Preferred", "Synonym", "Related")
_LEVEL_RANK = {name: i for i, name in enumerate(LEVELS)}

SOURCE_1 = "ICD-O-3.2 term"
SOURCE_2 = "curated"

# Abbreviations that collide (cross_group_B C12 to C14). The generator refuses to write one.
ABBREVIATIONS_NOT_ALIASED = {
    "acc": "adrenal cortical carcinoma, adenoid cystic carcinoma and acinar cell carcinoma",
    "net": "a family name; also matches DNET, PNET and PitNET",
    "nec": "a family name",
    "gct": "germ cell tumour or granulosa cell tumour; Group 10 left it out too",
    "ptc": "papillary thyroid carcinoma, and a substring of PTCL",
    "mec": "mucoepidermoid carcinoma, and a substring of MECOM-rearranged leukaemia",
    "npc": "nasopharyngeal carcinoma, and a substring of other strings",
}

# ICD-O-3.2 terms on an emitted pair that are left out of the file altogether.
EXCLUDED_TERMS = {
    "Endolymphatic sac tumor": "an ear tumour; the code is the adenocarcinoma stem and no "
                               "Group 11 tree offers the entity",
    "Pseudomyxoma peritonei with unknown primary site": "names a peritoneal or appendiceal "
        "primary; Pseudomyxoma peritonei is 8480/6, a code Group 11 does not emit",
    "Papillary renal cell carcinoma": "a kidney tumour, Group VI",
    "Clear cell renal cell carcinoma, NOS": "a kidney tumour, Group VI",
    "Mucinous tubular and spindle cell carcinoma": "a kidney tumour, Group VI",
    "Mucinous cystic neoplasm with an associated invasive carcinoma": "digestive-system "
        "(pancreatic or hepatobiliary) mucinous cystic neoplasm wording; the code is the "
        "mucinous cystadenocarcinoma stem",
    "Mucinous cystic tumor with an associated invasive carcinoma": "as above",
    "Intrapulmonary thymoma": "a lung tumour that no Group 11 tree offers as a thymoma",
    "Melanoma, meningeal": "no site where it could be entered: the brain sites do not list "
                           "Group 11",
    "Adrenal cortical adenocarcinoma": "a code-less alias cannot enter at C74.x, which lists "
        "Group 4 only; Adrenal cortical carcinoma, a code-bearing alias of the same code, "
        "enters there through occurs_at_routed_sites",
    "Adrenal cortical tumor, malignant": "as above",
    "Adenocarcinoma of anogenital mammary-like glands": "an anogenital tumour; no tree offers it",
    "Keratoacanthoma": "registrar, 8 October 2026 (review A9): not registered unless the "
                       "pathologist calls it squamous cell carcinoma, so it is a code-less "
                       "curated alias into the skin tree, not an alias of 8071/3",
}

# Strings another group's file holds that Group 11 holds as well. Registrar, 8 October 2026 (review
# E4): "Then add Oxyphilic adenocarcinoma, add other names as aliases. Synonyms are aliases by the
# way!" These are 8290/3's ICD-O-3.2 terms. Group 3 holds two at the pituitary and Group 10 four on
# its gonadal carcinoma picker. app.js asks the site of a term filed under several groups, and the
# site settles it; Group 10's generator yields a picker-only term another group holds (its rule 8).
SHARED_BY_RULING = {
    "Oxyphilic adenocarcinoma",
    "Oncocytic adenocarcinoma",
    "Oncocytic carcinoma",
    "Hurthle cell carcinoma",
    "Hurthle cell adenocarcinoma",
    "Follicular carcinoma, oxyphilic cell",
    # Review A9, E10: code-less into the skin tree, whose keratoacanthoma line is not registered.
    "Keratoacanthoma",
}

# Organ-naming ICD-O-3.2 terms that are not Preferred (cross_group_B C15): term -> organ. A term
# ICD-O-3.2 prints with one organ's site code is listed too (Rule H, a site-associated term).
# A term here becomes an alias of its code only where every tree that emits the code is the
# organ's tree; otherwise it is a code-less alias entering the organ's tree.
ORGAN_TREES = {
    "thyroid": ["g11_thyroid"],
    "prostate": ["g11_urinary_male_genital"],
    "urethral glands": ["g11_urinary_male_genital"],
    "parathyroid": ["g11_endocrine"],
    "thymus": ["g11_thymus"],
    "anus": ["g11_colorectal"],
    "lung": ["g11_lung"],
    "breast": ["g11_breast"],
    "pancreas": ["g11_digestive"],
    "nasopharynx": ["g11_nasopharynx"],
    "salivary gland": ["g11_salivary"],
    "skin": ["g11_skin"],
}
ORGAN_NAMING = {
    "Papillary carcinoma of thyroid": "thyroid",
    "Acinar adenocarcinoma of prostate": "prostate",
    "Basal cell carcinoma of prostate": "prostate",
    "Acinar adenocarcinoma, mucinous variant": "prostate",
    "Acinar adenocarcinoma, signet ring-like variant": "prostate",
    "Acinar adenocarcinoma, sarcomatoid variant": "prostate",
    "Carcinoma of Skene, Cowper and Littre glands": "urethral glands",
    "Parathyroid carcinoma": "parathyroid",
    "Thymic carcinoma with adenoid cystic carcinoma-like features": "thymus",
    "Adenocarcinoma of anal ducts": "anus",
    "Bronchial adenoma, carcinoid": "lung",
    "Small cell carcinoma, pulmonary type": "lung",
    "Adenocarcinoma of mammary gland type": "breast",
    "Basal-like carcinoma of breast": "breast",
    "Carcinoma of male breast": "breast",
    "Invasive breast carcinoma of no special type": "breast",
    "Primary cutaneous neuroendocrine carcinoma": "skin",
    "Papillary carcinoma of breast": "breast",
    "Micropapillary carcinoma of breast": "breast",
    "Juvenile carcinoma of breast": "breast",
    "Paget disease of breast": "breast",
    "Paget disease of nipple": "breast",
    "Pancreatic endocrine tumor, NOS": "pancreas",
    "Pancreatic endocrine tumor, nonfunctioning": "pancreas",
    "Mixed pancreatic endocrine and exocrine tumor, malignant": "pancreas",
    # ICD-O-3.2 prints these three Related terms of 8290/3 with C73.9 (Rule H).
    "Hurthle cell carcinoma": "thyroid",
    "Hurthle cell adenocarcinoma": "thyroid",
    "Follicular carcinoma, oxyphilic cell": "thyroid",
}

# Appended to the notes of every ICD-O-3.2-term alias on the code.
NOTE_SUFFIX = {
    "8010": " Group 11 emits 8010 wherever a report names a carcinoma and no type.",
    "8370": " Of the adrenal cortex. 8370/0 is the adenoma, a behaviour exclusion.",
    "8720": " A clinical note alone does not record it in a child (registrar, 8 October 2026).",
}

# alias, codes, alias_type, origin_system, nci_concept_id, notes
# codes is the list the alias maps to; [] with an organ in CODELESS_ORGAN makes a code-less alias.
# NCIt concept IDs are given only where this build has a confirmed entity, and none is invented.
CURATED = [
    # Spelling variants of a Preferred term (exempt from the site form with it).
    ("Adrenocortical carcinoma", ["8370"], "descriptive", "ICD-O-3.2 (wording variant)", None,
     "Wording variant of Adrenal cortical carcinoma (8370/3), the form the adrenal tree uses."),
    ("Acinic cell carcinoma", ["8550"], "descriptive", "ICD-O-3.2 (wording variant)", None,
     "Wording variant of Acinar cell carcinoma (8550/3), the form the salivary, nasopharyngeal "
     "and head and neck trees use."),
    ("Solid pseudopapillary neoplasm", ["8452"], "descriptive", "ICD-O-3.2 (wording variant)",
     None,
     "Solid pseudopapillary neoplasm of pancreas (8452/3) without the organ. ICD-O-3.2 codes "
     "the ovarian tumour 8452/1, which is not a Group XI code."),
    ("Solid pseudopapillary tumour", ["8452"], "descriptive", "ICD-O-3.2 (British spelling)",
     None, "British wording of Solid pseudopapillary neoplasm of pancreas (8452/3)."),
    # WHO names the trees' options use and ICD-O-3.2 prints differently.
    ("Polymorphous low grade adenocarcinoma", ["8525"], "descriptive", "WHO name", None,
     "The name the salivary tree's option uses for Polymorphous adenocarcinoma (8525/3)."),
    ("PLGA", ["8525"], "abbreviation", "WHO name", None,
     "Abbreviation of Polymorphous low grade adenocarcinoma (8525/3)."),
    ("Goblet cell adenocarcinoma", ["8243"], "descriptive", "WHO name", None,
     "The WHO name the appendix tree's option uses for Goblet cell carcinoid (8243/3). The "
     "current entity sits on the same stem (design D3)."),
    ("Goblet cell carcinoma", ["8243"], "descriptive", "WHO name", None,
     "A name the appendix tree's option gives for Goblet cell carcinoid (8243/3)."),
    ("Atypical carcinoid", ["8249"], "descriptive", "ICD-O-3.2 (wording variant)", None,
     "Atypical carcinoid tumor without the noun, the form the lung and colorectal trees' "
     "options use for Neuroendocrine tumor, grade 2 (8249/3)."),
    ("Invasive ductal carcinoma", ["8500"], "descriptive", "WHO name", None,
     "The name the breast tree's option uses for Infiltrating duct carcinoma, NOS (8500/3)."),
    ("Invasive carcinoma of no special type", ["8500"], "descriptive", "WHO name", None,
     "The name the breast tree's option uses for Infiltrating duct carcinoma, NOS (8500/3)."),
    ("Invasive lobular carcinoma", ["8520"], "descriptive", "ICD-O-3.2 (wording variant)", None,
     "Wording variant of Infiltrating lobular carcinoma, NOS, an ICD-O-3.2 synonym of Lobular "
     "carcinoma, NOS (8520/3), the form the breast tree's option uses."),
    ("Type C thymoma", ["8586"], "descriptive", "ICD-O-3.2 (wording variant)", None,
     "Word-order variant of the ICD-O-3.2 synonym Thymoma, type C, of Thymic carcinoma, NOS "
     "(8586/3)."),
    ("Keratinising squamous cell carcinoma", ["8071"], "descriptive",
     "ICD-O-3.2 (British spelling)", None,
     "British spelling of Squamous cell carcinoma, keratinizing, NOS (8071/3)."),
    ("Keratinizing squamous cell carcinoma", ["8071"], "descriptive",
     "ICD-O-3.2 (wording variant)", None,
     "Wording variant of Squamous cell carcinoma, keratinizing, NOS (8071/3)."),
    ("Non-keratinising squamous cell carcinoma", ["8072"], "descriptive",
     "ICD-O-3.2 (British spelling)", None,
     "British spelling of Squamous cell carcinoma, nonkeratinizing, NOS, an ICD-O-3.2 synonym "
     "of 8072/3."),
    ("Non-keratinizing squamous cell carcinoma", ["8072"], "descriptive",
     "ICD-O-3.2 (wording variant)", None,
     "Wording variant of Squamous cell carcinoma, nonkeratinizing, NOS, an ICD-O-3.2 synonym "
     "of 8072/3."),
    ("Acral lentiginous melanoma", ["8744"], "descriptive", "ICD-O-3.2 (wording variant)", None,
     "The older name of Acral melanoma (8744/3); ICD-O-3.2 keeps Acral lentiginous melanoma, "
     "malignant as a synonym."),
    ("Epithelioid melanoma", ["8771"], "descriptive", "ICD-O-3.2 (wording variant)", None,
     "Wording variant of Epithelioid cell melanoma (8771/3)."),
    ("Melanoma arising in giant congenital naevus", ["8761"], "descriptive",
     "ICD-O-3.2 (British spelling)", None,
     "British wording of Malignant melanoma arising in giant congenital nevus (8761/3)."),
    ("Melanoma arising in a congenital melanocytic naevus", ["8761"], "descriptive",
     "ICD-O-3.2 (British spelling)", None,
     "British wording of the ICD-O-3.2 synonym Malignant melanoma in congenital melanocytic "
     "nevus (8761/3), as the melanoma tree's option words it."),
    # Organ-naming WHO names: code-less (cross_group_B C15). Each names the organ whose tree
    # offers the entity; the code depends on the report and is settled in that tree.
    ("Papillary thyroid carcinoma", [], "descriptive", "WHO name", None,
     "The thyroid tree's name for Papillary adenocarcinoma, NOS (8260/3) and its subtypes."),
    ("Follicular thyroid carcinoma", [], "descriptive", "WHO name", None,
     "The thyroid tree's name for the follicular carcinomas: 8330/3, 8335/3 and 8339/3, "
     "settled by the extent of invasion."),
    ("Anaplastic thyroid carcinoma", [], "descriptive", "WHO name", None,
     "Entered in the thyroid tree, which offers Carcinoma, anaplastic, NOS (8021/3) and "
     "Carcinoma, undifferentiated, NOS (8020/3)."),
    ("Undifferentiated thyroid carcinoma", [], "descriptive", "WHO name", None,
     "Entered in the thyroid tree, which offers Carcinoma, undifferentiated, NOS (8020/3) and "
     "Carcinoma, anaplastic, NOS (8021/3)."),
    ("Nasopharyngeal carcinoma", [], "descriptive", "WHO name", None,
     "Entered in the nasopharynx tree, which settles the type: keratinising 8071/3, "
     "non-keratinising 8072/3, or carcinoma with no type named 8010/3."),
    ("Nasopharyngeal carcinoma, keratinising", [], "descriptive", "WHO name", None,
     "The nasopharynx tree's option for Squamous cell carcinoma, keratinizing, NOS (8071/3)."),
    ("Nasopharyngeal carcinoma, keratinizing", [], "descriptive", "WHO name", None,
     "The nasopharynx tree's option for Squamous cell carcinoma, keratinizing, NOS (8071/3)."),
    ("Nasopharyngeal carcinoma, non-keratinising", [], "descriptive", "WHO name", None,
     "The nasopharynx tree's option for Squamous cell carcinoma, nonkeratinizing, NOS "
     "(8072/3), differentiated or undifferentiated."),
    ("Nasopharyngeal carcinoma, non-keratinizing", [], "descriptive", "WHO name", None,
     "The nasopharynx tree's option for Squamous cell carcinoma, nonkeratinizing, NOS "
     "(8072/3), differentiated or undifferentiated."),
    ("Undifferentiated nasopharyngeal carcinoma", [], "descriptive", "WHO name", None,
     "The nasopharynx tree's older name for the non-keratinising type (8072/3)."),
    ("Salivary duct carcinoma", [], "descriptive", "WHO name", None,
     "The salivary tree's option for Infiltrating duct carcinoma, NOS (8500/3)."),
    ("Squamous cell carcinoma of skin", [], "descriptive", "WHO name", None,
     "Entered in the skin tree, which settles the squamous cell carcinoma code (8070/3 and "
     "its variants). The generic squamous cell carcinoma strings are Group 10's."),
    ("Keratoacanthoma", [], "descriptive", "ICD-O-3.2 related term", None,
     "Entered in the skin tree, where a keratoacanthoma is not registered unless the pathologist "
     "calls it squamous cell carcinoma (registrar, 8 October 2026, review A9)."),
    ("Cutaneous squamous cell carcinoma", [], "descriptive", "WHO name", None,
     "Entered in the skin tree, which settles the squamous cell carcinoma code (8070/3 and "
     "its variants). The generic squamous cell carcinoma strings are Group 10's."),
]
# organ for each code-less curated alias
CODELESS_ORGAN = {
    "Papillary thyroid carcinoma": "thyroid",
    "Follicular thyroid carcinoma": "thyroid",
    "Anaplastic thyroid carcinoma": "thyroid",
    "Undifferentiated thyroid carcinoma": "thyroid",
    "Nasopharyngeal carcinoma": "nasopharynx",
    "Nasopharyngeal carcinoma, keratinising": "nasopharynx",
    "Nasopharyngeal carcinoma, keratinizing": "nasopharynx",
    "Nasopharyngeal carcinoma, non-keratinising": "nasopharynx",
    "Nasopharyngeal carcinoma, non-keratinizing": "nasopharynx",
    "Undifferentiated nasopharyngeal carcinoma": "nasopharynx",
    "Salivary duct carcinoma": "salivary gland",
    "Squamous cell carcinoma of skin": "skin",
    "Cutaneous squamous cell carcinoma": "skin",
    "Keratoacanthoma": "skin",
}


# --------------------------------------------------------------------------------------
# What the group emits and what ICD-O-3.2 says
# --------------------------------------------------------------------------------------

def key(text: str) -> str:
    """The comparison form validator rule 3 of Group 10 uses: case and whitespace folded,
    'tumour' read as 'tumor', a trailing ', NOS' dropped."""
    k = " ".join(str(text).lower().split()).replace("tumour", "tumor")
    return k[:-len(", nos")] if k.endswith(", nos") else k


def norm(text: str) -> str:
    return " ".join(str(text).lower().split())


def british(term: str) -> str | None:
    """The British form of an American term, or None. 'tumor' becomes 'tumour' and
    'Tumor' becomes 'Tumour'; nothing else is respelt."""
    if "tumor" not in term.lower():
        return None
    return re.sub(r"(?i)tumor", lambda m: "Tumour" if m.group(0)[0] == "T" else "tumour", term)


def emissions(ctx):
    """(node_id, code, behaviour) for every pair a node can emit: code branches (options,
    immunohistochemistry rules, bands, override_when), an imaging_pathway node's own code, and
    the nos_fallback code. Mirrors build_database._group10_emissions."""
    for node_id, node in ctx.nodes.items():
        for holder, _where in bd._branch_containers(node):
            code = bd.as_code(holder.get("morphology_code"))
            if code:
                beh = holder.get("behavior_code")
                yield node_id, code, None if beh is None else str(beh).strip()
        if node.get("node_type") == "imaging_pathway" and bd.as_code(node.get("morphology_code")):
            beh = node.get("behavior_code")
            yield node_id, bd.as_code(node.get("morphology_code")), \
                None if beh is None else str(beh).strip()
        fb = node.get("nos_fallback")
        if isinstance(fb, dict) and bd.as_code(fb.get("code")):
            beh = fb.get("behavior_code")
            yield node_id, bd.as_code(fb.get("code")), None if beh is None else str(beh).strip()


def held_by_other_groups() -> dict[str, list[int]]:
    """Every alias string, whitespace-normalised and lower-cased, that another group's alias
    file holds (or alias_index.json files under a group other than 11), with the holders."""
    held: dict[str, set[int]] = {}
    for path in sorted(ALIAS_DIR.glob("aliases_group_*.json")):
        group = int(path.stem.rsplit("_", 1)[1])
        if group == GROUP:
            continue
        for a in json.loads(path.read_text(encoding="utf-8")):
            held.setdefault(norm(a["alias"]), set()).add(group)
    index_path = ALIAS_DIR / "alias_index.json"
    if index_path.exists():
        for alias, groups in json.loads(index_path.read_text(encoding="utf-8")).items():
            for g in groups:
                if g != GROUP:
                    held.setdefault(norm(alias), set()).add(g)
    return {k: sorted(v) for k, v in held.items()}


def main() -> int:
    dt = json.loads(DT.read_text(encoding="utf-8"))
    ctx = bd.DTContext(DT, dt, GROUP)
    entries = {(e["morphology_code"], e["behavior_code"]): e for e in dt["morphology_entries"]}
    emitted: dict[str, set[str]] = {}
    trees_of: dict[str, set[str]] = {}
    ihc: set[str] = set()
    for node_id, code, beh in emissions(ctx):
        emitted.setdefault(code, set()).add(beh)
        trees_of.setdefault(code, set()).add(ctx.node_tree[node_id])
        if ctx.nodes[node_id].get("node_type") == "ihc_checklist":
            ihc.add(code)
    bad_beh = {c: b for c, b in emitted.items() if b != {"3"}}
    if bad_beh:
        raise SystemExit("ERROR: Group 11 emits only /3 (BEHAVIOUR_DECLARED_BY_GROUP); the trees "
                         "emit %s" % bad_beh)
    index, err = bd.load_icdo32(LAYER1)
    if err:
        raise SystemExit("ERROR: %s" % err)
    pairs: dict[str, dict[tuple[str, str], str]] = {}
    for (code, beh), bucket in index.items():
        for term in bucket:
            pairs.setdefault(key(term), {})[(code, beh)] = term
    router = json.loads(ROUTER.read_text(encoding="utf-8"))
    g11 = router["groups"][str(GROUP)]
    handoff = g11["handoff"]
    entry_node = {t["tree_id"]: t["entry_node"] for t in g11["trees"]}
    held = held_by_other_groups()

    out: list[dict] = []
    seen: set[str] = set()
    by_source = {SOURCE_1: 0, SOURCE_2: 0}
    codeless = 0
    left_with_group: dict[str, list[int]] = {}      # string -> holders
    excluded: dict[str, str] = {}                   # string -> reason
    ambiguous: dict[str, list[str]] = {}
    held_twins: list[str] = []

    def tree_for(codes: list[str], organ_trees: list[str] | None) -> tuple[str, str]:
        if organ_trees:
            return organ_trees[0], entry_node[organ_trees[0]]
        sole = set().union(*(trees_of[c] for c in codes))
        if len(sole) == 1:
            t = next(iter(sole))
            return t, entry_node[t]
        return handoff["tree_id"], handoff["entry_node"]

    def name_of(code: str) -> str:
        return entries[(code, "3")]["morphology_name"]

    def add(source, alias, codes, alias_type, origin, nci, notes, coding_note,
            organ_trees=None, twin_of_held=False):
        nonlocal codeless
        n = norm(alias)
        if n in seen:
            return
        if alias.lower() in ABBREVIATIONS_NOT_ALIASED:
            raise SystemExit("ERROR: %r is an abbreviation that is not aliased (%s)"
                             % (alias, ABBREVIATIONS_NOT_ALIASED[alias.lower()]))
        for c in codes:
            if c not in emitted:
                raise SystemExit("ERROR: alias %r maps to %s, which no tree emits" % (alias, c))
        if n in held and alias not in SHARED_BY_RULING:
            left_with_group[alias] = held[n]
            return
        seen.add(n)
        by_source[source] += 1
        if twin_of_held:
            held_twins.append(alias)
        if not codes:
            codeless += 1
        tree_id, node_id = tree_for(codes, organ_trees)
        if codes:
            full = "%s -> %s" % (alias, " / ".join("%s (%s)" % (name_of(c), c) for c in codes))
        else:
            full = "%s -> no code attached; the %s tree settles the code" % (
                alias, tree_id.replace("g11_", "").replace("_", " "))
        out.append({
            "alias": alias,
            "full_form": full,
            "also_known_as": [],
            "alias_type": alias_type,
            "origin_system": origin,
            "nci_concept_id": nci,
            "who_version_current": "ICD-O-3.2",
            "maps_to_morphology_codes": codes,
            "maps_to_iccc3_subgroup_id":
                entries[(codes[0], "3")]["iccc3_subgroup_id"] if codes else None,
            "needs_ihc_tree": any(c in ihc for c in codes),
            "ihc_tree_id": tree_id,
            "tree_entry_node": node_id,
            "clinical_alert": None,
            "notes": notes,
            "coding_note": coding_note,
        })

    # 1. ICD-O-3.2 terms on the emitted pairs, then their British spellings.
    for code in sorted(emitted):
        bucket = index.get((code, "3"), {})
        for term, (level, obs) in sorted(
                bucket.items(), key=lambda kv: (_LEVEL_RANK.get(kv[1][0], 9), kv[0])):
            if obs or level not in LEVELS:
                continue
            if term in EXCLUDED_TERMS:
                excluded[term] = EXCLUDED_TERMS[term]
                continue
            filed = {c for (c, _b) in pairs.get(key(term), {})}
            if filed != {code}:
                ambiguous[term] = sorted(filed)
                continue
            preferred = level == "Preferred"
            organ = ORGAN_NAMING.get(term)
            organ_trees = ORGAN_TREES[organ] if organ else None
            attach = True
            if organ and not preferred and not trees_of[code] <= set(organ_trees):
                attach = False      # code-less: the code is emitted at other organs' trees
            for variant, is_twin in ((term, False), (british(term), True)):
                if variant is None:
                    continue
                if is_twin and variant in EXCLUDED_TERMS:
                    continue
                add(SOURCE_1 if not is_twin else SOURCE_2, variant,
                    [code] if attach else [],
                    "who_preferred" if (preferred and not is_twin) else "descriptive",
                    ("ICD-O-3.2" if preferred else "ICD-O-3.2 %s" % (
                        "synonym" if level == "Synonym" else "related term"))
                    if not is_twin else "ICD-O-3.2 (British spelling)",
                    None,
                    ("%s, %s/3." % (name_of(code), code) if preferred and not is_twin else
                     "An ICD-O-3.2 %s term for %s (%s/3)." % (level.lower(), name_of(code), code)
                     if not is_twin else
                     "British spelling of the ICD-O-3.2 %s term %s, %s/3." % (
                         level.lower(), term, code))
                    + NOTE_SUFFIX.get(code, "")
                    + ("" if attach else
                       " Not attached to the code: the term is a %s term, and Group 11 emits %s "
                       "at other organs' trees (design D21, site form)." % (organ, code)),
                    "ICD-O-3.2 %s term on %s/3, read from icdo32.sqlite; Group 11 emits %s at "
                    "/3 only.%s" % (level, code, code,
                                    "" if not is_twin else " British spelling for the trees' "
                                    "option labels, which the search box does not fold."),
                    organ_trees=organ_trees if not attach else None,
                    twin_of_held=is_twin and norm(term) in held)

    # 2. Curated names.
    for alias, codes, alias_type, origin, nci, notes in CURATED:
        if norm(alias) in seen:
            continue
        hit = pairs.get(key(alias), {})
        if hit and not set(codes) <= {c for (c, _b) in hit}:
            if codes:
                raise SystemExit("ERROR: curated alias %r maps to %s, but ICD-O-3.2 files that "
                                 "string under %s" % (alias, codes, sorted({c for c, _ in hit})))
        organ = CODELESS_ORGAN.get(alias)
        if bool(codes) == bool(organ):
            raise SystemExit("ERROR: curated alias %r must be code-bearing or have an organ, "
                             "not both or neither" % alias)
        add(SOURCE_2, alias, codes, alias_type, origin, nci, notes,
            "Curated: Group 11 build contract §6 (the %s of the trees' option labels or the "
            "WHO name). %s" % (
                "British spelling or wording" if codes else "organ-naming name",
                "" if codes else "Code-less (cross_group_B C15): the name says one organ, and "
                "Group 11 emits the code at other organs' trees, so no code is attached."),
            organ_trees=ORGAN_TREES[organ] if organ else None)

    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote %s (%d aliases: %s; %d code-less)"
          % (OUT, len(out), ", ".join("%d %s" % (n, s) for s, n in by_source.items()),
             codeless), file=sys.stderr)
    print("%d string(s) left with the group that already holds them (not shared):"
          % len(left_with_group), file=sys.stderr)
    by_group: dict[tuple, int] = {}
    for holders in left_with_group.values():
        by_group[tuple(holders)] = by_group.get(tuple(holders), 0) + 1
    for holders, n in sorted(by_group.items()):
        print("  held by Group %s: %d" % ("/".join(map(str, holders)), n), file=sys.stderr)
    print("%d term(s) left out: %s" % (len(excluded), "; ".join(sorted(excluded))),
          file=sys.stderr)
    print("%d term(s) filed under more than one code: %s"
          % (len(ambiguous), "; ".join("%s -> %s" % kv for kv in sorted(ambiguous.items()))),
          file=sys.stderr)
    print("%d British twin(s) whose American form another group holds: %s"
          % (len(held_twins), "; ".join(held_twins)), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
