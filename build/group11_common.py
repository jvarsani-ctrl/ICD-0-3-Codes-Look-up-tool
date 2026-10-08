"""Shared builders for the ICCC-3 Group XI decision trees (contract docs/group_11_build_contract.md).

Every Group XI tree module (build/group11_organs/*.py, build/group11_families/*.py) builds its tree
from these functions, so the evidence gate, the tissue-free routes, the deposit question, the
picker and the trailing options of each histology screen are written once. The thyroid module,
build/group11_organs/thyroid.py, is the worked exemplar: copy its shape.

What a tree module provides
---------------------------
    build(tree_id) -> dict      the tree, made by make_tree()
    DECISIONS: dict             {"code/behaviour": (D-numbers, evidence stem, sentence[, overrides])}
                                for every pair the module emits outside its picker. The generator
                                merges every module's DECISIONS (group11_tree.decisions()) and
                                fails on an emitted pair with no entry. A pair an ihc_checklist rule
                                emits needs the override {"diagnostic_tests_required":
                                ["Histology", "IHC"], "ihc_markers_required": [markers of the
                                rules that emit it, in rule order]}.
The module's row in TREES names it (`module`); group11_tree.trees() imports every module that
exists, in TREES order.

The API, one line each
----------------------
Layer 1
    term(code, beh)                 ICD-O-3.2 Preferred term at (code, behaviour); TreeError if none
    preferred_is_obsolete(code, beh)  ICD-O-3.2 marks the Preferred term [obs] (D3)
    live_search_terms(code, beh)    the live Synonym and Related terms (picker search_terms, D2)
    iccc_status(code, site)         "XI", "other:<group>" or "none" for (code, behaviour 3) at a site
Trees
    TREES                           contract §4.1 as data; routed sites expanded from Layer 1
    tree_row(tree_id) / row_for_prefix(prefix)
Branches (Group 10 shapes)
    rec(code, beh="3", basis=None)  "Recorded as <Preferred term> (code/beh)[ at basis of diagnosis N]."
    code(label, morph, beh, basis, reason, ...)  a coded branch; /3 only, never an [obs] Preferred
    named(label, morph, extra=None, ...)         a coded branch at basis 7 whose reason starts rec()
    go(label, node_id, captures=None, note=None)
    refer(label, group, reason, ..., recapture=False, refer_code=None)
    excl(label, code, beh, reason=None, ...)     behaviour_exclusion; icdo_term read from icdo32.sqlite
    nonrep(label, reason, ...)      non_reportable
    aid(branch, text)               attach a recognition aid
    node(node_id, node_type, step, step_label, question, hint, options, captured, note, **extra)
    lab(lab_id, label, units)       one row of a lab_results screen
Common nodes (contract §4.2)
    evidence_gate(prefix, ...)      document_inventory, lab screens, _clinical, _clinical_cytology,
                                    _imaging, _imaging_markers (marker trees only), _imaging_cytology,
                                    _cytology
    marker(code, ...)               one Visser Table 4 marker code for _imaging_markers (D7)
    cyto(label, code, ...)          a cytology option naming an entity, basis 5 (D8)
    refer_unspecified(...)          the default tissue-free and type-free route: Group XII, refer_code
    tail_options(prefix, melanoma, ...)  the trailing options of every histology screen
    not_malignant_node(prefix, exclusions, ...)  the exclusion screen
    deposit_node(prefix, ...)       D10
    ihc_node(prefix, marker_groups, rules, ...)  an ihc_checklist with a NOS fallback
    rule(positive, code, reason, ...)  one ihc_checklist rule
    nut_nodes(prefix, ...)          the NUT carcinoma screens a D12 tree offers
    make_tree(tree_id, nodes, ...)  appends the picker (D2), returns the tree dict
    evidence_mapping(trees)         the docs/evidence_documents/group_11.json payload for every gate

The D-numbers this module implements, and where
-----------------------------------------------
D1   tail_options() leaves paediatric options to the module; make_tree() puts every other
     current code in the picker. A module offers an entity whose code needs a further answer
     as a histology option (the thyroid's follicular invasion screen).
D2   picker_node(), called by make_tree(): codes ICCC-2017 places in Group XI (behaviour 3) at
     EVERY routed site of the tree, plus the standing-rule-3 codes the module names (D11), less
     the [obs] Preferred terms (D3), the melanoma codes (D13) and the codes the histology screen
     and its subtype screens offer. Labels are the Preferred term; search_terms the live
     Synonym and Related terms; prefill_filter_from_search true. Codes valid at only some
     routed sites are listed in the picker's coding_note and in PICKER_REPORT, not offered.
D3   code() refuses a pair whose Preferred term ICD-O-3.2 marks [obs]; picker_node() leaves
     those pairs out (the eleven all-[obs] pairs, 8551 and 8780).
D4   no builder names a code ICD-O-3.2 lacks: term() fails on it.
D7   evidence_gate(): every tissue-free and type-free route refers to Group XII with
     refer_code 8000 or 8001 (refer_unspecified). One exception: marker() codes record at basis 4 only on
     _imaging_markers, whose every path holds Imaging and Tumour markers. "Possible" is
     non_reportable (Visser rule 4); a raised marker with no tumour on imaging is
     non_reportable (rule 6).
D8   evidence_gate(): cytology naming an entity codes it at basis 5 (cyto()); malignant cells
     with no type refer to Group XII with refer_code 8001; suspicious cytology is not
     registrable.
D10  deposit_node(): one referral per primary family, each with recapture_site; a leukaemia
     records C42.1; a carcinoma with no primary found continues in the unspecified tree's
     histology screen at C80.9 (ICCC-2017 range 136 places the shared list at C80.9 in XIf11);
     any other tumour with no primary found refers to Group XII at C80.9. A carcinoma or
     melanoma primary in another organ refers to Group XI itself only when SELF_REFERRAL is
     True: build_database.check_refer_terminals fails a referral to the file's own group, so
     until that check admits a recapture_site self-referral the option is absent and the hint
     sends the clerk back to the site step (the Group 10 n_deposit wording for its own group).
D12  tail_options(nut=True) adds the NUT carcinoma option; nut_nodes() builds its screens from
     docs/group_11_evidence/NUT_carcinoma.json.
D13  tail_options() hops to the melanoma tree: me_skin_histology, me_eye, me_mucosa or me_cns
     (MELANOMA_ENTRY). group11_tree.trees() defers a hop whose tree module does not exist yet.
D15  BASIS_DEFAULTS on every tree; basis 1, 2, 4, 5, 7 and 8 on the branches as the evidence
     tier gives it.

Departures from Group 10's shapes, and why
------------------------------------------
* No "an imaging report is in the file after all" or "a histology report is in the file"
  escape on the clinical-note and imaging screens. The document checklist decides the tier
  from the reports ticked, so each path's evidence_tests is what the clerk ticked (contract
  §9 item 5). Group 10's escapes added a report the ticks did not hold.
* The marker screen and the imaging conclusion are one node, _imaging_markers (contract §4.2).
  It has no escape option, so it can be entered from the marker tier and from non-diagnostic
  cytology without either context's evidence being overwritten.
* refer() carries refer_code: 8000 to 8005 are not Group XI entries, so check_refer_terminals
  admits it (Group 10 could not, because 8000 to 8005 are Group X entries at the gonads).

Clerk-facing text lives in question, hint, label, reason, upgrade_path and recognition_aid.
coding_note is author-facing. clinical_alert is null everywhere (ruling 9). Every reason that
names a code gives the ICD-O-3.2 Preferred term, read from icdo32.sqlite (term()), never typed.
"""
from __future__ import annotations

import copy
import os
import re
import sqlite3
from pathlib import Path

import generate_group_inventory as gi  # build/ is on sys.path for every caller

GROUP = 11
ICCC_GROUP = "XI"


class TreeError(Exception):
    """A tree cannot be built: a pair ICD-O-3.2 does not carry, a builder used against its
    contract, or Layer 1 absent. generate_group11_entries.py turns it into exit 2."""


# ------------------------------------------------------------------------------------------
# Layer 1
# ------------------------------------------------------------------------------------------
def _icdo_path() -> Path:
    return Path(os.environ.get("ICDO_DB", str(gi.DEFAULT_ICDO))).resolve()


def _iccc_path() -> Path:
    return Path(os.environ.get("ICCC_DB", str(gi.DEFAULT_ICCC))).resolve()


def _layer1_path() -> Path:
    return Path(os.environ.get("ICD_LAYER1", str(gi.DEFAULT_LAYER1))).resolve()


_TERMS: dict | None = None


def _terms() -> dict:
    """{(code, behaviour): [(level, term, obsolete), ...]} from icdo32.sqlite, read once."""
    global _TERMS
    if _TERMS is None:
        path = _icdo_path()
        if not path.exists():
            raise TreeError("icdo32.sqlite not found at %s - set ICDO_DB" % path)
        index: dict = {}
        try:
            con = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
            try:
                for c, b, level, t, obs in con.execute(
                        "SELECT code4, behaviour, level, term, obs FROM icd_o_3_2_morphology "
                        "WHERE code4 IS NOT NULL AND behaviour IS NOT NULL"):
                    index.setdefault((str(c), str(b)), []).append(
                        (str(level or "").strip(), str(t or "").strip(), bool((obs or "").strip())))
            finally:
                con.close()
        except sqlite3.Error as exc:
            raise TreeError("icdo32.sqlite at %s could not be read: %s" % (path, exc)) from None
        _TERMS = index
    return _TERMS


def icdo_terms(code_: str, beh: str) -> list:
    """Every ICD-O-3.2 term at (code, behaviour) as (level, term, obsolete)."""
    return _terms().get((str(code_), str(beh)), [])


def term(code_: str, beh: str) -> str:
    """The ICD-O-3.2 Preferred term at (code, behaviour)."""
    preferred = [t for level, t, _obs in icdo_terms(code_, beh) if level == "Preferred"]
    if not preferred:
        # A stated-behaviour pair the registrar ruled (Rule F, review A6): ICD-O-3.2 does not
        # print it, and the name is the code's Preferred term at the behaviour it does print.
        # The table is build_database.ICDO32_MATRIX_RULE, which the build checks.
        from build_database import ICDO32_MATRIX_RULE
        rule_f = ICDO32_MATRIX_RULE.get((GROUP, str(code_), str(beh)))
        if rule_f:
            return term(code_, rule_f[0])
    if len(preferred) != 1:
        raise TreeError("ICD-O-3.2 has %s Preferred term at %s/%s"
                        % ("no" if not preferred else "more than one", code_, beh))
    return preferred[0]


def preferred_is_obsolete(code_: str, beh: str) -> bool:
    """ICD-O-3.2 marks the Preferred term of (code, behaviour) [obs] (D3)."""
    return any(level == "Preferred" and obs for level, _t, obs in icdo_terms(code_, beh))


def live_search_terms(code_: str, beh: str) -> list:
    """The ICD-O-3.2 Synonym and Related terms of (code, behaviour) not marked [obs], in that
    order. The alias layer indexes the same terms, so a name the search box finds is a name
    the picker's filter finds."""
    out: list = []
    for want in ("Synonym", "Related"):
        for level, t, obs in icdo_terms(code_, beh):
            if level == want and not obs and t and t not in out:
                out.append(t)
    return out


def _topo3(text: str) -> int:
    m = re.fullmatch(r"C(\d\d)\.(\d)", text.strip())
    if not m:
        raise TreeError("not a topography code: %r" % text)
    return int(m.group(1)) * 10 + int(m.group(2))


def _c(n: int) -> str:
    return "C%02d.%d" % (n // 10, n % 10)


def _spans(raw: str) -> list:
    """ICCC-2017 '000-218,239-399' -> [(0, 218), (239, 399)]."""
    out = []
    for part in str(raw or "").split(","):
        part = part.strip()
        if not part:
            continue
        ends = part.split("-")
        out.append((int(ends[0]), int(ends[-1])))
    return out


_ICCC: dict | None = None


def _iccc_index() -> dict:
    """{code: [(main_group, subgroup, spans, behaviours)]} for every ICCC-2017 range."""
    global _ICCC
    if _ICCC is None:
        path = _iccc_path()
        if not path.exists():
            raise TreeError("ICCC-2017.sqlite not found at %s - set ICCC_DB" % path)
        index: dict = {}
        con = sqlite3.connect("file:%s?mode=ro" % path, uri=True)
        try:
            for c, main, sub, topo, beh in con.execute(
                    "SELECT code, main_group, group_code, topography_raw, behavior "
                    "FROM code_lookup"):
                index.setdefault(str(c), []).append(
                    (str(main), str(sub), _spans(topo), gi.parse_behaviour_declaration(beh)))
        finally:
            con.close()
        _ICCC = index
    return _ICCC


def iccc_status(code_: str, site: str) -> str:
    """Where ICCC-2017 places (code, behaviour 3) at a site: "XI" when a Group XI range holds
    it there, "other:<main group>" when another group's range does, "none" when no range does
    (standing rule 3 then keeps a Group XI code in Group XI: design D11)."""
    n = _topo3(site)
    hits = [main for main, _sub, spans, behs in _iccc_index().get(str(code_), [])
            if "3" in behs and any(lo <= n <= hi for lo, hi in spans)]
    if ICCC_GROUP in hits:
        return ICCC_GROUP
    return "other:%s" % hits[0] if hits else "none"


def iccc_subgroups(code_: str, site: str) -> list:
    """The Group XI subgroups ICCC-2017 gives (code, behaviour 3) at a site."""
    n = _topo3(site)
    return [sub for main, sub, spans, behs in _iccc_index().get(str(code_), [])
            if main == ICCC_GROUP and "3" in behs and any(lo <= n <= hi for lo, hi in spans)]


_XI_RECORDS: list | None = None


def xi_records() -> list:
    """The Group XI inventory records (ICCC-2017.sqlite joined to icdo32.sqlite)."""
    global _XI_RECORDS
    if _XI_RECORDS is None:
        _XI_RECORDS = gi.build_inventory(_iccc_path(), _icdo_path(), ICCC_GROUP)["records"]
    return _XI_RECORDS


def melanoma_codes() -> set:
    """Every code ICCC-2017 places in subgroup XId (range 123). The melanoma option of every
    histology screen reaches them (D13), so no picker offers them."""
    return {r["morphology_code"] for r in xi_records() if r["iccc3_subgroup_id"] == "XId"}


def redcap_topography() -> list:
    """Every code in the first fenced block of Layer 1's REDCap topography list, converted from
    the three-digit form (739) to C73.9, in file order. Same reader as the generator's."""
    path = _layer1_path() / "RedCap Options" / "Topography Redcap.md"
    if not path.exists():
        raise TreeError("Layer 1's REDCap topography list is not at %s - set ICD_LAYER1" % path)
    lines = path.read_text(encoding="utf-8").splitlines()
    fences = [i for i, line in enumerate(lines) if line.strip().startswith("```")]
    if len(fences) < 2:
        raise TreeError("%s holds no fenced code list" % path.name)
    out = []
    for line in lines[fences[0] + 1:fences[1]]:
        m = re.match(r"(\d{3}),", line.strip())
        if m:
            out.append(_c(int(m.group(1))))
    return out


# ------------------------------------------------------------------------------------------
# The trees (contract §4.1) — the single source for T3's router and T4's validator
# ------------------------------------------------------------------------------------------
# `topography` is the §4.1 routed-topography cell, written as ranges: "C11.0-C11.9" (codes),
# "C00-C06" (whole three-character categories), "C53" (one category, every subsite). It is
# expanded against Layer 1's REDCap topography list, never typed code by code, so C44.4 and
# C48.1, which that list lacks, are not routed (contract §3.1). `module` is the Python module
# group11_tree.py imports for the tree; every module exposes build(tree_id) and DECISIONS.
# `where` is the clerk-facing name of the site family, used in reasons and labels.
_TREE_TABLE = (
    ("g11_adrenal", "ad_", "Adrenocortical carcinomas", "C74.0,C74.1,C74.9",
     ("XIa_adrenal_cortex",), "group11_organs.adrenal", "the adrenal gland"),
    ("g11_thyroid", "th_", "Thyroid carcinomas", "C73.9",
     ("XIb_thyroid",), "group11_organs.thyroid", "the thyroid"),
    ("g11_nasopharynx", "np_", "Nasopharyngeal carcinomas", "C11.0-C11.9",
     ("XIc_nasopharynx",), "group11_organs.nasopharynx", "the nasopharynx"),
    ("g11_salivary", "sg_", "Carcinomas of the salivary glands", "C07.9,C08.0-C08.9",
     ("XIf1_salivary",), "group11_organs.salivary", "the salivary glands"),
    ("g11_colorectal", "cr_", "Carcinomas of the colon and rectum",
     "C18.0,C18.2-C18.9,C19.9,C20.9,C21.0-C21.8",
     ("XIf2_XIf3_digestive",), "group11_organs.colorectal", "the colon or rectum"),
    ("g11_appendix", "ap_", "Carcinomas of the appendix", "C18.1",
     ("XIf2_XIf3_digestive",), "group11_organs.colorectal", "the appendix"),
    ("g11_lung", "lu_", "Carcinomas of the lung", "C34.0-C34.9",
     ("XIf4_lung_pleura",), "group11_organs.lung", "the lung"),
    ("g11_thymus", "ty_", "Carcinomas of the thymus and mediastinum", "C37.9,C38.1,C38.2,C38.3",
     ("XIf5_thymus_mediastinum",), "group11_organs.thymus", "the thymus or mediastinum"),
    ("g11_melanoma", "me_", "Malignant melanomas", "",
     ("XId_melanoma",), "group11_organs.melanoma", "the site of the melanoma"),
    ("g11_skin", "sk_", "Skin carcinomas", "C44.0-C44.9,C51.9,C60.9,C63.2",
     ("XIe_skin_carcinoma",), "group11_families.skin", "the skin"),
    ("g11_breast", "br_", "Carcinomas of the breast", "C50.0-C50.9",
     ("XIf6_breast",), "group11_families.breast", "the breast"),
    ("g11_female_genital", "fg_", "Carcinomas of the female genital organs",
     "C51.0-C51.8,C52.9,C53,C54,C55.9,C57,C58.9",
     ("XIf7_female_genital",), "group11_families.female_genital", "the female genital organs"),
    ("g11_urinary_male_genital", "gu_", "Carcinomas of the urinary tract and male genital organs",
     "C60.0-C60.8,C61.9,C63.0,C63.1,C63.7-C63.9,C65.9,C66.9,C67,C68",
     ("XIf8_urinary_male_genital",), "group11_families.urinary_male_genital",
     "the urinary tract or male genital organs"),
    ("g11_eye", "ey_", "Carcinomas of the eye", "C69.0-C69.9",
     ("XIf9_eye",), "group11_families.eye", "the eye"),
    ("g11_head_neck", "hn_", "Carcinomas of the head and neck",
     "C00-C06,C09-C10,C12-C14,C30-C33",
     ("XIf10_head_neck", "XIc_nasopharynx"), "group11_families.head_neck", "the head and neck"),
    ("g11_digestive", "dg_", "Carcinomas of the other digestive organs",
     "C15,C16,C17,C23,C24,C25,C26",
     ("XIf2_XIf3_digestive",), "group11_families.digestive", "the digestive organs"),
    ("g11_thoracic", "tx_", "Carcinomas of the pleura, heart and other thoracic sites",
     "C38.0,C38.4,C38.8,C39",
     ("XIf4_lung_pleura",), "group11_families.thoracic", "the chest"),
    ("g11_endocrine", "en_", "Carcinomas of the parathyroid and other endocrine glands",
     "C75.0,C75.2,C75.4,C75.5,C75.8,C75.9",
     ("XIf10_parathyroid_other_unspecified",), "group11_families.endocrine", "the endocrine glands"),
    ("g11_unspecified", "un_", "Carcinomas at another or an unspecified site",
     "C76,C80.9,C70-C72,C48",
     ("XIf10_parathyroid_other_unspecified",), "group11_families.unspecified",
     "an ill-defined or unknown site"),
)


def _expand(spec: str, redcap: list) -> list:
    """Expand a §4.1 topography cell against Layer 1's REDCap list, in numeric order."""
    spans = []
    for token in (t.strip() for t in spec.split(",") if t.strip()):
        ends = [e.strip() for e in token.split("-")]

        def low(e):
            return _topo3(e) if "." in e else int(e[1:3]) * 10

        def high(e):
            return _topo3(e) if "." in e else int(e[1:3]) * 10 + 9
        spans.append((low(ends[0]), high(ends[-1])))
    return sorted((c for c in redcap if any(lo <= _topo3(c) <= hi for lo, hi in spans)), key=_topo3)


_TREES: list | None = None


def trees_table() -> list:
    """TREES, computed once: one dict per tree in §4.1 order, with `sites` expanded."""
    global _TREES
    if _TREES is None:
        redcap = redcap_topography()
        out, owner = [], {}
        for tree_id, prefix, label, spec, evidence, module, where in _TREE_TABLE:
            sites = _expand(spec, redcap) if spec else []
            for s in sites:
                if s in owner:
                    raise TreeError("%s is routed to both %s and %s" % (s, owner[s], tree_id))
                owner[s] = tree_id
            out.append({"tree_id": tree_id, "prefix": prefix, "label": label,
                        "topography_spec": spec, "sites": sites, "evidence": list(evidence),
                        "module": module, "where": where})
        _TREES = out
    return _TREES


def __getattr__(name):
    """`from group11_common import TREES` reads Layer 1 on first use (PEP 562), so importing
    the module needs no database. TREES is trees_table(): one dict per tree in §4.1 order with
    tree_id, prefix, label, topography_spec, sites (expanded C-codes), evidence, module, where."""
    if name == "TREES":
        return trees_table()
    raise AttributeError("module %r has no attribute %r" % (__name__, name))


def tree_row(tree_id: str) -> dict:
    for row in trees_table():
        if row["tree_id"] == tree_id:
            return row
    raise TreeError("no Group XI tree %r in TREES" % tree_id)


def row_for_prefix(prefix: str) -> dict:
    for row in trees_table():
        if row["prefix"] == prefix:
            return row
    raise TreeError("no Group XI tree has the prefix %r" % prefix)


def prefix_of(node_id: str) -> str:
    return node_id.split("_", 1)[0] + "_"


def _ranges(sites: list) -> list:
    """['C11.0', 'C11.1', ...] -> ['C11.0-C11.9'] over runs of consecutive REDCap codes."""
    redcap = redcap_topography()
    pos = {c: i for i, c in enumerate(sorted(redcap, key=_topo3))}
    out, run = [], []
    for s in sorted(sites, key=_topo3):
        if run and pos.get(s) == pos.get(run[-1], -9) + 1:
            run.append(s)
        else:
            if run:
                out.append(run[0] if len(run) == 1 else "%s-%s" % (run[0], run[-1]))
            run = [s]
    if run:
        out.append(run[0] if len(run) == 1 else "%s-%s" % (run[0], run[-1]))
    return out


# ------------------------------------------------------------------------------------------
# Shared wording
# ------------------------------------------------------------------------------------------
VISSER = "Visser 2023, European Network of Cancer Registries"
NOT_REGISTRABLE_POSSIBLE = (
    "Cancer is only possible on this evidence. Under the European registry rules a case that "
    "is only possibly cancer is not registered without pathology (%s, rule 4)." % VISSER)
EVIDENCE_TIER = ["evidence_tests", "workup_status", "basis_evidence_tier"]
BASIS_DEFAULTS = {"ihc_counts_as": 7, "methylation_counts_as": 8}     # D15
NO_TISSUE_BASIS = (1, 2, 4, 5)
BEH_TEXT = {"0": "behaviour 0, benign", "1": "behaviour 1, uncertain or borderline",
            "2": "behaviour 2, in situ"}
OUTSIDE_XI = ("ICCC-3 Group XI registers behaviour 3 (malignant) only, so no Group XI code is "
              "recorded.")
PENDING = " This exclusion awaits the registrar's decision."
# The upgrade line for a terminal whose report does not determine the type. Without one,
# app.js prints "None - fully subtyped at this evidence tier" (Group 10 code review).
TYPE_NOT_STATED = ("The report does not state the tumour's type. A report that names it gives "
                   "that type's own code: go back and take the option that names it.")
# A named type whose entry requires IHC because a stain panel rule emits it (the generator's
# check_ihc_overrides, Group 8 precedent). make_tree() puts this on the tree's basis-7 options
# for such a pair, so the engine does not say IHC "would yield a more specific code" on a
# report that already names the type; IHC still shows as outstanding (Group 10 IHC_CONFIRMS).
IHC_CONFIRMS = ("Immunohistochemistry, where the report does not describe it, confirms the "
                "type the report names; it does not change this code.")

# D10: a referral to Group XI itself with recapture_site. True since T4 (8 October 2026):
# build_database.check_refer_terminals admits a referral to the file's own group when the branch
# carries recapture_site true, and fails it otherwise.
SELF_REFERRAL = True

# D13: the melanoma tree's screen each histology screen hops to, by site kind. T2c builds them.
MELANOMA_ENTRY = {"skin": "me_skin_histology", "eye": "me_eye", "mucosa": "me_mucosa",
                  "cns": "me_cns"}


# ------------------------------------------------------------------------------------------
# Branch helpers (the Group 8 and Group 10 shapes)
# ------------------------------------------------------------------------------------------
def _tail(b, captures=None, note=None, negative=None, satisfies=None, upgrade=None,
          heading=None):
    """Append the optional keys every branch helper shares, in one fixed order."""
    if satisfies:
        b["satisfies_tests"] = list(satisfies)
    if upgrade:
        b["upgrade_path"] = upgrade
    if heading:
        b["non_reportable_heading"] = heading
    if note:
        b["coding_note"] = note
    if captures:
        b["captures"] = copy.deepcopy(captures)
    if negative:
        b["negative"] = list(negative)
    return b


def rec(morph: str, beh: str = "3", basis: int | None = None) -> str:
    """'Recorded as Medullary thyroid carcinoma (8345/3).' - the Preferred term, never typed.
    A tissue-free or cytology basis is named."""
    at = " at basis of diagnosis %d" % basis if basis in NO_TISSUE_BASIS else ""
    return "Recorded as %s (%s/%s)%s." % (term(morph, beh), morph, beh, at)


def code(label, morph, beh, basis, reason, captures=None, satisfies=None, note=None,
         upgrade=None, key="label", negative=None):
    """A coded branch. Group XI emits behaviour 3 only, and never a pair whose Preferred term
    ICD-O-3.2 marks [obs] (D3); either fails the build here."""
    if str(beh) != "3":
        raise TreeError("%s/%s: Group XI emits behaviour 3 only; use excl() for /%s"
                        % (morph, beh, beh))
    term(morph, beh)
    if preferred_is_obsolete(morph, beh):
        raise TreeError("%s/%s: ICD-O-3.2 marks its Preferred term [obs]; design D3 keeps it "
                        "off every screen" % (morph, beh))
    if not isinstance(basis, int) or basis not in (1, 2, 4, 5, 7, 8):
        raise TreeError("%s/%s: basis of diagnosis %r is not 1, 2, 4, 5, 7 or 8 (D15)"
                        % (morph, beh, basis))
    b = {key: label, "morphology_code": morph, "behavior_code": beh,
         "basis_of_diagnosis": basis, "reason": reason}
    return _tail(b, captures, note, negative, satisfies, upgrade)


def named(label, morph, extra=None, *, basis=7, note=None, upgrade=None, captures=None):
    """A coded option whose reason is rec() and, optionally, one more sentence."""
    reason = rec(morph, "3", basis) + (" " + extra if extra else "")
    return code(label, morph, "3", basis, reason, captures=captures, note=note, upgrade=upgrade)


def go(label, node_id, captures=None, note=None):
    return _tail({"label": label, "next_node": node_id}, captures, note)


def refer(label, group, reason, captures=None, note=None, recapture=False, refer_code=None):
    """A cross-group referral. refer_code names the code the other group records (8000 or
    8001 on a tissue-free route, D7); it is never a Group XI entry. recapture: the site on the
    case is not the primary's, so the hop asks for the primary's site (WHO Rules A and H)."""
    if group == GROUP and not (recapture and SELF_REFERRAL):
        raise TreeError("a referral to Group XI itself is built only with recapture_site and "
                        "SELF_REFERRAL (D10): %r" % label)
    b = {"label": label, "refer_group": group, "reason": reason}
    if refer_code is not None:
        b["refer_code"] = str(refer_code)
    if recapture:
        b["recapture_site"] = True
    return _tail(b, captures, note)


def excl(label, icdo, beh, reason=None, *, what=None, extra="", decision=False, note=None):
    """A behaviour exclusion. icdo_term is the ICD-O-3.2 Preferred term, read here. Without a
    reason the standard one is written: 'ICD-O-3.2 codes <what> as <term> (<code>/<beh>),
    <behaviour>. <extra> ICCC-3 Group XI registers behaviour 3 ...'."""
    if str(beh) == "3":
        raise TreeError("%s/3 is a Group XI behaviour; an exclusion names /0, /1 or /2" % icdo)
    if reason is None:
        reason = "ICD-O-3.2 codes %s as %s (%s/%s), %s. %s%s%s" % (
            what or "it", term(icdo, beh), icdo, beh, BEH_TEXT[str(beh)],
            (extra + " ") if extra else "", OUTSIDE_XI, PENDING if decision else "")
    return _tail({"label": label,
                  "behaviour_exclusion": {"icdo_code": icdo, "icdo_behaviour": str(beh),
                                          "icdo_term": term(icdo, beh), "group_declares": "3",
                                          "reason": reason,
                                          "registrar_decision_required": bool(decision)}},
                 None, note)


def nonrep(label, reason, captures=None, note=None, heading=None):
    return _tail({"label": label, "non_reportable": True, "reason": reason}, captures, note,
                 heading=heading)


def aid(branch, text):
    """Attach a recognition aid (clerk-facing, report vocabulary) to an option and return it."""
    branch["recognition_aid"] = text
    return branch


def node(node_id, node_type, step, step_label, question, hint, options, captured, note,
         **extra):
    n = {"node_id": node_id, "node_type": node_type, "step_number": step,
         "step_label": step_label, "question": question, "hint": hint,
         "clinical_alert": None, "coding_note": note, "captured_variables": list(captured)}
    if options is not None:
        n["options"] = options
    n.update(extra)
    n.setdefault("nos_fallback", None)
    return n


def lab(lab_id, label, units):
    """One row of a lab_results screen. The values are recorded and never choose a code."""
    return {"id": lab_id, "label": label, "units": list(units)}


# ------------------------------------------------------------------------------------------
# Tissue-free and type-free routes (D7, D8)
# ------------------------------------------------------------------------------------------
def refer_unspecified(label, morph, basis, why, *, where, captures=None, note=None):
    """The default route for an unspecified malignancy (8000/3 or 8001/3, D7). ICCC-2017 range
    143 places 8000-8005 in XIIb at every Group XI routed site outside the brain and spinal
    cord, so the case is referred to Group XII and refer_code names the code it records there.
    `where` is the clerk-facing site ('the thyroid')."""
    if morph not in ("8000", "8001"):
        raise TreeError("refer_unspecified records 8000 or 8001, not %s" % morph)
    at = " at basis of diagnosis %d" % basis if basis in NO_TISSUE_BASIS else ""
    reason = ("%s It is registered as %s (%s/3)%s. ICCC-3 places that code at %s in Group XII "
              "(other and unspecified malignant neoplasms), not in Group XI. Code the case from "
              "the Group XII tree." % (why, term(morph, "3"), morph, at, where))
    return refer(label, 12, reason, captures=captures, refer_code=morph,
                 note=note or "D7: ICCC-2017 range 143 (XIIb) holds 8000-8005 at this tree's "
                              "routed sites; the referral names the code (refer_code).")


def _check_unspecified_is_xii(prefix):
    """refer_unspecified() states that ICCC-2017 places 8000/8001 in Group XII at every routed
    site of the tree. Verify it, so a tree with another site (the brain, IIIf) passes its own
    route instead."""
    row = row_for_prefix(prefix)
    for site in row["sites"]:
        for morph in ("8000", "8001"):
            if iccc_status(morph, site) != "other:XII":
                raise TreeError("%s: ICCC-2017 places %s/3 at %s in %s, not Group XII; pass "
                                "evidence_gate(unspecified=...) a route that says so"
                                % (row["tree_id"], morph, site, iccc_status(morph, site)))


# ------------------------------------------------------------------------------------------
# The evidence gate (§4.2): document inventory, laboratory screens, clinical, imaging, cytology
# ------------------------------------------------------------------------------------------
TIERS = ("referral", "markers", "imaging", "cytology", "histology")
TIER_EVIDENCE = {"referral": [], "markers": ["Imaging", "Tumour markers"],
                 "imaging": ["Imaging"], "cytology": ["Cytology"], "histology": ["Histology"]}
TIER_LABELS = {
    "referral": "A referral letter or clinical note only - no imaging report, no tissue",
    "markers": "An imaging report and a tumour marker result - no tissue",
    "imaging": "An imaging report only - no tissue",
    "cytology": "Cytology only - a fine-needle aspirate or fluid; no histology report",
    "histology": "A histology report - biopsy or resection",
}
# The document ids of the router's evidence_documents vocabulary each tier needs and refuses.
# evidence_mapping() adds "lab" to a laboratory copy's requires and to the plain tier's
# excludes; it adds "lab" to the imaging tier's excludes where a marker tier takes imaging
# with a Lab Report.
TIER_TICKS = {
    "referral": {"requires": [], "excludes": ["imaging", "cytology", "histology"]},
    "markers": {"requires": ["imaging", "lab"], "excludes": ["cytology", "histology"]},
    "imaging": {"requires": ["imaging"], "excludes": ["cytology", "histology"]},
    "cytology": {"requires": ["cytology"], "excludes": ["histology"]},
    "histology": {"requires": ["histology"], "excludes": []},
}
TIER_RATIONALE = {
    "referral": "Lowest tier: fits when no imaging, cytology or histology document is ticked, "
                "so it catches nothing ticked, a lone Lab Report, and IHC or gene reports "
                "without the document they are read against (all understate, the safe "
                "direction).",
    "markers": "Needs the Imaging Report and the Lab Report (assumed to hold the marker "
               "result); 'no tissue' excludes Cytology and Histology Report. The next screen "
               "asks what the report says of the marker and the imaging (D7, Visser Table 4).",
    "imaging": "Imaging Report with no tissue; 'no tissue' excludes Cytology and Histology "
               "Report.",
    "cytology": "Needs the Cytology document itself; Histology Report excluded because the label "
                "says no histology report. IHC or genetics beside Cytology stays here.",
    "histology": "Histology Report ticked: the top tier regardless of other documents, with IHC "
                 "and genetics refining it only beside the report.",
}
LAB_HINT = ("Enter each number as the report gives it, with its unit. Put > or < before a "
            "limit the report prints, such as >2000. Leave a test the file does not hold "
            "empty.")


def _nid(prefix, name):
    return prefix + name


def _tier_captures(tier):
    return {"evidence_tests": list(TIER_EVIDENCE[tier]),
            "workup_status": "not done" if tier == "referral" else "incomplete",
            "basis_evidence_tier": tier}


def marker(morph, *, test, diagnosis, where, note, label=None, extra=None):
    """One Visser Table 4 marker code for the _imaging_markers screen (D7). The label states
    the imaging, the marker and the diagnosis Table 4 names; the code records at basis 4.
    `test`: 'serum calcitonin'; `diagnosis`: 'medullary thyroid carcinoma'; `where`: 'of the
    thyroid'; `note`: the author cite (Visser O, et al. Front Oncol 2023;13:1250549, Table 4,
    p. 06, and the evidence file's row)."""
    label = label or ("Imaging shows a tumour %s, the report calls %s raised, and the file "
                      "calls it %s" % (where, test, diagnosis))
    reason = ("%s A %s shown on imaging with a raised %s is registered to this code without "
              "tissue (%s, Table 4). A histology report confirms it.%s"
              % (rec(morph, "3", 4), diagnosis, test, VISSER, (" " + extra) if extra else ""))
    return code(label, morph, "3", 4, reason,
                captures={"workup_status": "incomplete",
                          "basis_evidence_tier": "markers_%s" % morph},
                note="D7. " + note)


def cyto(label, morph, extra=None, *, note=None):
    """A cytology option that names an entity: its code at basis 5 (D8)."""
    reason = ("%s Cytology does not give the full histological type; a histology report "
              "confirms it.%s" % (rec(morph, "3", 5), (" " + extra) if extra else ""))
    return code(label, morph, "3", 5, reason,
                captures={"workup_status": "incomplete", "basis_evidence_tier": "cytology_named"},
                note="D8. " + (note or "Coded as the cytology report names it."))


def cyto_carcinoma_nos(note=None):
    """Cytology that calls the tumour a carcinoma and names no type: 8010/3 at basis 5 (D8)."""
    return cyto("Cytology names a carcinoma without naming its type", "8010",
                note=note or "A carcinoma is an entity: 8010/3 at basis 5. Malignant cells with "
                             "no tumour type refer to Group XII with 8001 instead.")


def n_labs(prefix, tier, destination, labs):
    return node(
        _nid(prefix, "labs_" + tier), "lab_results", 2, "Laboratory results",
        "Which laboratory results are in the file?", LAB_HINT, None, [],
        "Registrar, 6 October 2026 (Group 10 registrar review E2): reached from the evidence "
        "checklist only when Lab Report is ticked, then on to the %s tier's destination. The "
        "tests are the ones the evidence file gives a diagnostic role. No value chooses a code."
        % tier,
        labs=copy.deepcopy(list(labs)), next_node=destination)


def _clinical_contexts(prefix):
    return {
        "referral": {"id": _nid(prefix, "clinical"), "evidence": [], "step": 2,
                     "hint": "No imaging report or tissue report is in the file."},
        "cytology": {"id": _nid(prefix, "clinical_cytology"), "evidence": ["Cytology"], "step": 3,
                     "hint": "The cytology report is not diagnostic, and no imaging report or "
                             "histology report is in the file."},
    }


def _imaging_contexts(prefix):
    return {
        "imaging": {"id": _nid(prefix, "imaging"), "evidence": ["Imaging"], "step": 2,
                    "question": "No tissue is in the file. What does the imaging report "
                                "conclude?"},
        "cytology": {"id": _nid(prefix, "imaging_cytology"), "evidence": ["Cytology", "Imaging"],
                     "step": 3,
                     "question": "The cytology report is not diagnostic, and no histology report "
                                 "is in the file. What does the imaging report conclude?"},
    }


def _n_clinical(prefix, ctx, where, unspecified, skin_melanoma):
    c = _clinical_contexts(prefix)[ctx]
    opts = []
    if skin_melanoma:
        opts.append(code(
            "The note diagnoses a melanoma of the skin, as the diagnosis or as probable",
            "8720", "3", 1,
            "%s Melanoma of the skin is registered on clinical information alone (%s, Table 3)."
            % (rec("8720", "3", 1), VISSER),
            captures={"workup_status": "incomplete", "basis_evidence_tier": "referral_melanoma"},
            note="D7: Visser 2023 Table 3, p. 04-05, melanoma of the skin, basis 1, C44. Skin "
                 "trees only (validator rule 2)."))
    opts += [
        unspecified("The note states a malignant tumour as the diagnosis, or as probable",
                    "8000", 1,
                    "A clinical note alone does not establish the tumour's type (%s, rule 5)."
                    % VISSER, where=where,
                    captures={"workup_status": "incomplete",
                              "basis_evidence_tier": "referral_malignant"}),
        nonrep("The note says only possible or suspected", NOT_REGISTRABLE_POSSIBLE,
               {"workup_status": "not registrable",
                "basis_evidence_tier": "referral_nondiagnostic"}),
    ]
    return node(
        c["id"], "clinical_alias", c["step"], "Referral wording",
        "What does the referral letter or clinical note say?",
        "%s A note alone never establishes a carcinoma's type." % c["hint"],
        opts, EVIDENCE_TIER,
        "Contract §4.2, D7. Visser O, et al. Frontiers in Oncology 2023;13:1250549, rules 4 and "
        "5, p. 03: 8000/3 at basis 1 when cancer is at least probable; 'possible' is not "
        "registrable. Evidence context %r: reached with evidence_tests %r, which no option "
        "changes." % (ctx, c["evidence"]))


def _n_imaging(prefix, ctx, where, unspecified):
    c = _imaging_contexts(prefix)[ctx]
    return node(
        c["id"], "morphology_only", c["step"], "Imaging conclusion", c["question"],
        "Answer from the radiologist's own conclusion. Imaging alone never establishes a "
        "carcinoma's type.",
        [
            unspecified("Imaging shows a malignant tumour, at least probable", "8000", 2,
                        "Imaging alone does not establish the tumour's type (%s, rule 5)."
                        % VISSER, where=where,
                        captures={"workup_status": "incomplete",
                                  "basis_evidence_tier": "imaging_malignant"}),
            nonrep("Imaging calls it possible only, or describes a benign lesion",
                   NOT_REGISTRABLE_POSSIBLE,
                   {"workup_status": "not registrable",
                    "basis_evidence_tier": "imaging_nondiagnostic"}),
        ],
        EVIDENCE_TIER,
        "Contract §4.2, D7. Visser 2023 rule 5, p. 03: imaging alone is 8000/3 at basis 2, a "
        "Group XII code at this tree's sites. Evidence context %r: reached with evidence_tests "
        "%r, which no option changes." % (ctx, c["evidence"]))


def _n_imaging_markers(prefix, where, unspecified, markers, test_names):
    opts = list(markers) + [
        unspecified("Imaging shows a malignant tumour, at least probable, and no marker result "
                    "above registers it", "8000", 2,
                    "Imaging alone does not establish the tumour's type, and a marker registers "
                    "a code only with the diagnosis it names (%s, rule 5 and Table 4)." % VISSER,
                    where=where,
                    captures={"workup_status": "incomplete",
                              "basis_evidence_tier": "markers_imaging_malignant"}),
        nonrep("A marker is raised, but the imaging shows no tumour",
               "A raised tumour marker is not registered unless a clinical investigation shows "
               "the tumour (%s, rule 6)." % VISSER,
               {"workup_status": "not registrable", "basis_evidence_tier": "markers_no_tumour"}),
        nonrep("Imaging calls it possible only, or describes a benign lesion",
               NOT_REGISTRABLE_POSSIBLE,
               {"workup_status": "not registrable",
                "basis_evidence_tier": "markers_nondiagnostic"}),
    ]
    return node(
        _nid(prefix, "imaging_markers"), "morphology_only", 2, "Imaging and tumour markers",
        "No tissue is in the file. What do the imaging report and the %s result show?"
        % test_names,
        "Use the reports' own words. A marker counts as raised when the report calls it raised "
        "against the laboratory's reference range. Each coded option also needs the diagnosis "
        "it names (%s, Table 4)." % VISSER,
        opts, EVIDENCE_TIER,
        "Contract §4.2, D7. The marker codes record at basis 4 only here: Visser 2023 Table 4, "
        "p. 06, with rule 6, p. 05 (basis 4 never stands alone). Reached from the marker tier "
        "(evidence_tests Imaging, Tumour markers) and from non-diagnostic cytology (Cytology, "
        "Imaging, Tumour markers); no option changes evidence_tests, so neither context is "
        "overwritten.")


def _n_cytology(prefix, where, unspecified, cytology, has_markers, test_names):
    opts = list(cytology) + [
        unspecified("Malignant cells are present, with no tumour type named", "8001", 5,
                    "Cytology establishes malignant cells but no tumour type.", where=where,
                    captures={"workup_status": "incomplete",
                              "basis_evidence_tier": "cytology_malignant"}),
        nonrep("Suspicious for malignancy, atypical, indeterminate, or benign",
               "A cytology report that calls the tumour suspicious, atypical or indeterminate "
               "does not register it: it is only possible (%s, rule 4), and a benign result "
               "registers nothing." % VISSER,
               {"workup_status": "not registrable", "basis_evidence_tier": "cytology_suspicious"}),
    ]
    if has_markers:
        opts.append(go(
            "No malignant cells, scant material, or a non-diagnostic report - and an imaging "
            "report and a %s result are in the file" % test_names,
            _nid(prefix, "imaging_markers"),
            {"evidence_tests": ["Cytology", "Imaging", "Tumour markers"],
             "workup_status": "incomplete", "basis_evidence_tier": "cytology_nondiagnostic"},
            note="Non-diagnostic cytology leaves the marker route (Visser Table 4) as the best "
                 "evidence."))
    opts += [
        go("No malignant cells, scant material, or a non-diagnostic report - and an imaging "
           "report%s is in the file" % (", with no %s result," % test_names if has_markers
                                        else ""),
           _nid(prefix, "imaging_cytology"),
           {"evidence_tests": ["Cytology", "Imaging"], "workup_status": "incomplete",
            "basis_evidence_tier": "cytology_nondiagnostic"},
           note="Non-diagnostic cytology leaves imaging as the best evidence."),
        go("No malignant cells, scant material, or a non-diagnostic report - and no imaging "
           "report is in the file", _nid(prefix, "clinical_cytology"),
           {"evidence_tests": ["Cytology"], "workup_status": "incomplete",
            "basis_evidence_tier": "cytology_nondiagnostic"},
           note="Non-diagnostic cytology and no imaging leave the note as the best evidence; "
                "Cytology stays on the case (Group 10's split)."),
    ]
    return node(
        _nid(prefix, "cytology"), "morphology_only", 2, "Cytology",
        "What does the cytology report conclude?",
        "Use the cytology report's own conclusion. Cytology gives basis of diagnosis 5; a "
        "histology report gives the full type.",
        opts, EVIDENCE_TIER,
        "Contract §4.2, D8: cytology naming an entity codes it at basis 5 (Visser 2023 Table 1, "
        "p. 03); malignant cells with no type refer to Group XII with 8001; suspicious is not "
        "registrable (rule 4).")


def evidence_gate(prefix, *, where, question=None, hint=None, labs=(), markers=(),
                  marker_tests="tumour marker", cytology=(), skin_melanoma=False,
                  unspecified=None, tier_labels=None, note=""):
    """The evidence front end of a tree (contract §4.2), in tree order:
        <p>document_inventory  document_inventory, the entry node; one option per tier, and a
                               laboratory copy of every tier a Lab Report can join
        <p>labs_<tier>         lab_results, when `labs` is given (Group 10's design)
        <p>clinical, <p>clinical_cytology          clinical_alias
        <p>imaging, <p>imaging_markers (only with `markers`), <p>imaging_cytology  morphology_only
        <p>cytology            morphology_only
    The histology tier routes to <p>histology, which the module builds.

    where           clerk-facing site, 'the thyroid'
    labs            lab() rows; the values are recorded and never choose a code
    markers         marker() codes (D7, Visser Table 4), only at sites the marker concerns
    marker_tests    clerk-facing name of the marker test(s), 'serum calcitonin'
    cytology        options placed first on <p>cytology: cyto() codes and nonrep() lines
    skin_melanoma   8720/3 at basis 1 on the clinical-note screens. No Group XI tree passes True since
                    the registrar ruled for the paediatric source (8 October 2026, review A8, E9)
    unspecified     the route for 8000/8001; default refer_unspecified (Group XII). A tree
                    with a site where ICCC-2017 places 8000 elsewhere (the brain: IIIf) passes
                    its own; the default verifies Group XII at every routed site.
    tier_labels     per-tier label overrides; the evidence mapping matches on the label's start
    """
    if markers and not labs:
        raise TreeError("%s: a marker code needs a laboratory result; give `labs`" % prefix)
    if unspecified is None:
        _check_unspecified_is_xii(prefix)
        unspecified = refer_unspecified
    labels = dict(TIER_LABELS)
    if markers:
        labels["markers"] = ("An imaging report and a %s result - no tissue" % marker_tests)
        labels["imaging"] = ("An imaging report only - no %s result, no tissue" % marker_tests)
    labels.update(tier_labels or {})
    targets = {"referral": _nid(prefix, "clinical"), "imaging": _nid(prefix, "imaging"),
               "cytology": _nid(prefix, "cytology"), "histology": _nid(prefix, "histology")}
    if markers:
        targets["markers"] = _nid(prefix, "imaging_markers")
    lab_tiers = []
    if labs:
        lab_tiers = ["referral", "markers", "cytology", "histology"] if markers else \
            ["referral", "imaging", "cytology", "histology"]
    gate_opts = []
    for t in TIERS:
        if t not in targets:
            continue
        if t in lab_tiers:
            gate_opts.append(go(labels[t], _nid(prefix, "labs_" + t), _tier_captures(t)))
        if t != "markers":
            gate_opts.append(go(labels[t], targets[t], _tier_captures(t)))
    gate = node(
        _nid(prefix, "document_inventory"), "document_inventory", 1, "Evidence in file",
        question or "What is in the file for this tumour?",
        hint or ("A radiology report counts as imaging. A pathology report on a biopsy or "
                 "resection counts as histology. A biopsy or cytology report that calls the "
                 "specimen inadequate or non-diagnostic counts as no tissue."),
        gate_opts, EVIDENCE_TIER,
        "Contract §4.2: the evidence tiers; the router's site capture chose this tree. A tier a "
        "Lab Report can join routes through a laboratory screen when Lab Report is ticked "
        "(registrar, 6 October 2026). The checklist rules are in "
        "docs/evidence_documents/group_11.json. %s" % note)
    test_names = marker_tests
    nodes = [gate]
    nodes += [n_labs(prefix, t, targets[t], labs) for t in lab_tiers]
    nodes += [_n_clinical(prefix, "referral", where, unspecified, skin_melanoma),
              _n_clinical(prefix, "cytology", where, unspecified, skin_melanoma),
              _n_imaging(prefix, "imaging", where, unspecified)]
    if markers:
        nodes.append(_n_imaging_markers(prefix, where, unspecified, markers, test_names))
    nodes += [_n_imaging(prefix, "cytology", where, unspecified),
              _n_cytology(prefix, where, unspecified, cytology, bool(markers), test_names)]
    return nodes


# ------------------------------------------------------------------------------------------
# The trailing options of every histology screen (§4.2)
# ------------------------------------------------------------------------------------------
def refer_lymphoma(where, extra=""):
    return refer("Lymphoma", 2,
                 "A lymphoma belongs to ICCC-3 Group II. A lymphoma that arises in %s keeps %s "
                 "as its site (WHO Rule D: an extranodal lymphoma is coded to its site of "
                 "origin).%s Code the case from the Group II (lymphomas) tree."
                 % (where, where, (" " + extra) if extra else ""),
                 note="ICD-O-3.1 Rule D, p. 15. The hop carries the case's site.")


def refer_leukaemia(where):
    return refer("Leukaemia, or leukaemic infiltration", 1,
                 "Leukaemic infiltration of %s is coded as the leukaemia, in ICCC-3 Group I, and "
                 "a leukaemia is recorded at the bone marrow (C42.1). Code the case from the "
                 "Group I (leukaemias) tree." % where,
                 captures={"topography": "C42.1"},
                 note="WHO Rule E (section 4.2.8): every leukaemia except myeloid sarcoma is "
                      "C42.1, so the hop carries the marrow. A myeloid sarcoma option is not "
                      "built: check_leukaemia_referrals_record_marrow admits a site-keeping "
                      "Group I referral only on the nodes it lists.")


def refer_sarcoma(where, label="A sarcoma"):
    return refer(label, 9,
                 "A soft tissue sarcoma of %s belongs to ICCC-3 Group IX. Code the case from the "
                 "Group IX (soft tissue sarcomas) tree." % where,
                 note="ICCC-2017 places 8800-8921 and 9120-9133 in Group IX at the Group XI "
                      "sites; a bone sarcoma arises in bone, which no Group XI tree routes.")


def refer_germ_cell(where):
    return refer("Teratoma or another germ cell tumour", 10,
                 "Germ cell tumours, teratomas among them, belong to ICCC-3 Group X at %s. Code "
                 "the case from the Group X (germ cell tumours) tree." % where,
                 note="ICCC-2017 range 101 (Xb2) places 9080-9084 at the extragonadal sites.")


def refer_other_named():
    return refer("Another malignant tumour the report names that is not a carcinoma or "
                 "melanoma", 12,
                 "ICCC-3 Group XII holds the specified malignant tumours no other group codes. "
                 "Code the case from the Group XII (other and unspecified malignant neoplasms) "
                 "tree.")


def melanoma_option(kind):
    """D13: the hop into the melanoma tree's screen for this site kind."""
    if kind not in MELANOMA_ENTRY:
        raise TreeError("melanoma kind %r is not one of %s" % (kind, ", ".join(MELANOMA_ENTRY)))
    return go("Melanoma", MELANOMA_ENTRY[kind],
              note="D13: cross-tree next_node into the melanoma tree (%s), which offers every "
                   "XId code. group11_tree.trees() defers this hop while g11_melanoma has no "
                   "module." % MELANOMA_ENTRY[kind])


NUT_LABEL = ("NUT carcinoma (also written NUT midline carcinoma, BRD4::NUTM1 carcinoma or "
             "carcinoma with t(15;19) translocation), or a carcinoma reported with a NUT "
             "immunostain or a NUTM1 gene result")
# NUT_carcinoma.json nut_site_option: Luo 2025, p. 2 ("as a poorly differentiated carcinoma
# with rearrangements involving NUTM1") and p. 3 ("Only a third of cases exhibit frank squamous
# differentiation"); Lemelle 2022, p. 6 ("in favour of undifferentiated or poorly
# differentiated carcinoma") and p. 7 ("diffuse nuclear positivity of tumour cells
# (microgranular staining)").
NUT_AID = ("Reports describe a poorly differentiated or undifferentiated carcinoma, sometimes "
           "with abrupt keratinization, and nuclear staining for NUT.")


def tail_options(prefix, melanoma, *, where, nut=False, referrals=None, extra_referrals=(),
                 not_malignant_label=None):
    """The standard trailing options of a histology screen, in contract §4.2 order:
        Melanoma -> the melanoma tree (D13; `melanoma` is skin, eye, mucosa or cns)
        NUT carcinoma -> <p>nut_result (D12; only with nut=True, and nut_nodes() in the tree)
        Another carcinoma the report names -> <p>picker (D2)
        A tumour the report calls benign, borderline or in situ -> <p>not_malignant
        A deposit of a tumour that began elsewhere -> <p>deposit (D10)
        Malignant tumour, type not determined -> Group XII, refer_code 8000 (D7)
        the not-a-carcinoma referrals: lymphoma (II), leukaemia (I, C42.1), sarcoma (IX), germ
        cell (X), another named tumour (XII); `referrals` replaces that list, `extra_referrals`
        adds the site's own after it. `not_malignant_label` rewords the exclusion option where
        the site's exclusion screen also holds a non-tumour line (the thyroid's goitre).
    The module puts its paediatric options and its generic carcinoma options before these."""
    opts = [melanoma_option(melanoma)]
    if nut:
        opts.append(aid(go(NUT_LABEL, _nid(prefix, "nut_result"),
                           note="D12: NUT carcinoma evidence (NUT_carcinoma.json, "
                                "nut_site_option)."), NUT_AID))
    opts += [
        go("Another carcinoma the report names - type its name to find it",
           _nid(prefix, "picker"), note="D2: the Group XI picker."),
        go(not_malignant_label or "A tumour the report calls benign, borderline or in situ",
           _nid(prefix, "not_malignant"), note="The exclusion screen (contract §4.2)."),
        go("A deposit of a tumour that began elsewhere", _nid(prefix, "deposit"),
           note="D10."),
        refer_unspecified("Malignant tumour, type not determined by the report", "8000", 7,
                          "The report establishes a malignant tumour without determining its "
                          "type.", where=where),
    ]
    if referrals is None:
        referrals = [refer_lymphoma(where), refer_leukaemia(where), refer_sarcoma(where),
                     refer_germ_cell(where), refer_other_named()]
    return opts + list(referrals) + list(extra_referrals)


# ------------------------------------------------------------------------------------------
# The exclusion screen and the deposit question
# ------------------------------------------------------------------------------------------
def not_malignant_node(prefix, exclusions, *, where, catch_all=True, note=""):
    """<p>not_malignant: the exclusions (excl()) and non-reportable lines (nonrep()) a report
    calling the tumour benign, borderline or in situ can reach. catch_all adds a last line for
    a tumour the list does not name."""
    opts = list(exclusions)
    if catch_all:
        opts.append(nonrep(
            "Another tumour the report calls benign, borderline or in situ",
            "A tumour the report calls benign, borderline or in situ is not a malignant tumour. "
            "%s" % OUTSIDE_XI,
            note="Catch-all of the exclusion screen. Rule F (registrar, 8 October 2026, review "
                 "A6): the report's stated behaviour decides."))
    return node(
        _nid(prefix, "not_malignant"), "histology_subclassification", 4,
        "Benign, borderline or in situ",
        "Which tumour does the report diagnose?",
        "These tumours of %s are benign, borderline or in situ, as ICD-O-3.2 prints them or as "
        "the report states them. ICCC-3 Group XI "
        "registers malignant tumours (behaviour 3) only, so none is recorded as a Group XI "
        "cancer." % where,
        opts, [],
        "Contract §4.2: exclusions with the ICD-O-3.2 Preferred term at each (code, behaviour), "
        "read by excl() from icdo32.sqlite. Rule F (registrar, 8 October 2026, review A6): the "
        "stated behaviour decides; a pair ICD-O-3.2 does not print is admitted only through "
        "build_database.ICDO32_MATRIX_RULE. %s" % note)


DEPOSIT_PRIMARIES = (
    ("Neuroblastoma", 4, "Neuroblastoma is ICCC-3 Group IV."),
    ("Nephroblastoma (Wilms tumour), or another kidney tumour", 6,
     "Renal tumours are ICCC-3 Group VI."),
    ("Hepatoblastoma, or another liver tumour", 7, "Hepatic tumours are ICCC-3 Group VII."),
    ("A bone sarcoma", 8, "Malignant bone tumours are ICCC-3 Group VIII."),
    ("A soft tissue sarcoma, including rhabdomyosarcoma", 9,
     "Soft tissue sarcomas are ICCC-3 Group IX."),
    ("A tumour of the brain or spinal cord", 3,
     "Central nervous system tumours are ICCC-3 Group III."),
    ("Retinoblastoma", 5, "Retinoblastoma is ICCC-3 Group V."),
    ("A germ cell tumour", 10, "Germ cell tumours are ICCC-3 Group X."),
    ("A lymphoma", 2, "Lymphomas are ICCC-3 Group II."),
)
UNSPECIFIED_HISTOLOGY = "un_histology"


def deposit_node(prefix, *, where):
    """<p>deposit (D10), Group 10's n_deposit adapted. Every referral but two asks for the
    primary's site (recapture_site). A leukaemia records C42.1. A carcinoma with no primary
    found continues in the unspecified tree's histology screen at C80.9, where ICCC-2017 range
    136 places the shared carcinoma list in XIf11; any other tumour with no primary found
    refers to Group XII at C80.9 (WHO section 4.2.2)."""
    opts = [refer(label, group, "%s Code the case at its primary." % why, recapture=True)
            for label, group, why in DEPOSIT_PRIMARIES]
    if SELF_REFERRAL:
        opts.append(refer("A carcinoma or melanoma of another organ", GROUP,
                          "Carcinomas of other organs and melanomas are ICCC-3 Group XI. Code "
                          "the case at its primary.", recapture=True,
                          note="D10: the hop re-enters Group XI at the primary's site."))
    opts += [
        refer("Leukaemia", 1,
              "A leukaemia is coded in ICCC-3 Group I and recorded at the bone marrow (C42.1). "
              "Code the case from the Group I (leukaemias) tree.",
              captures={"topography": "C42.1"}, note="D10; WHO Rule E."),
        go("A carcinoma whose primary has not been found", UNSPECIFIED_HISTOLOGY,
           captures={"topography": "C80.9"},
           note="D10 with ICCC-2017 range 136: a carcinoma of unknown primary is coded at C80.9, "
                "XIf11, from the unspecified tree's histology screen (cross-tree next_node). "
                "group11_tree.trees() defers this hop while g11_unspecified has no module."),
        refer("Another tumour, or a tumour of unstated type, whose primary has not been found",
              12,
              "A deposit with no identified primary, other than a carcinoma, belongs in ICCC-3 "
              "Group XII (other and unspecified malignant neoplasms) and is recorded at C80.9. "
              "Code the case from the Group XII tree.", captures={"topography": "C80.9"},
              note="D10; WHO section 4.2.2: an unknown primary is C80.9, not the deposit's "
                   "site."),
    ]
    own = ("" if SELF_REFERRAL else
           " A deposit of a carcinoma or melanoma that began in another organ is coded at that "
           "organ: go back to the site step and record the primary's site.")
    return node(
        _nid(prefix, "deposit"), "morphology_only", 5, "Metastatic deposit",
        "Where does the report say the primary tumour is?",
        "The tumour in %s is a deposit, not a separate registration: the case is coded at its "
        "primary site.%s A melanoma is answered at the step before, from the melanoma option."
        % (where, own),
        opts, [],
        "D10, Group 10 n_deposit adapted. SELF_REFERRAL is %s: build_database's "
        "check_refer_terminals fails a referral to Group XI from Group XI's own file."
        % SELF_REFERRAL)


# ------------------------------------------------------------------------------------------
# Immunohistochemistry
# ------------------------------------------------------------------------------------------
def rule(positive, morph, reason, *, negative=(), note, basis=7):
    """One ihc_checklist rule: every `positive` marker positive and no `negative` marker
    positive. `note` must cite the page the rule rests on."""
    if not note:
        raise TreeError("rule %s: an immunohistochemistry rule cites its page in coding_note"
                        % morph)
    return code(list(positive), morph, "3", basis, reason, satisfies=["IHC"], key="positive",
                negative=list(negative) or None, note=note)


def ihc_node(prefix, marker_groups, rules, *, fallback="8010", fallback_reason=None,
             question="Answer each stain as the report states it.", hint, note, name="ihc",
             step=4):
    """<p>ihc: an ihc_checklist. The NOS fallback is required (contract §0.4) and records
    `fallback` at the tree's own generic code. Every marker a rule reads must be declared in
    marker_groups. Run build/induce_flow.py after any change: every rule needs a witness."""
    declared = {m for g in marker_groups for m in g["markers"]}
    for r in rules:
        for m in list(r.get("positive") or []) + list(r.get("negative") or []):
            if m not in declared:
                raise TreeError("%s%s: rule %s reads %r, which marker_groups does not declare"
                                % (prefix, name, r["morphology_code"], m))
    term(fallback, "3")
    return node(
        _nid(prefix, name), "ihc_checklist", step, "Stain panel", question, hint, None, [],
        note, marker_groups=copy.deepcopy(list(marker_groups)), resolution_logic=list(rules),
        nos_fallback={"code": fallback, "behavior_code": "3", "name": term(fallback, "3"),
                      "reason": fallback_reason or ("The stains do not establish the "
                                                    "carcinoma's type. %s" % rec(fallback))})


# ------------------------------------------------------------------------------------------
# NUT carcinoma (D12) — docs/group_11_evidence/NUT_carcinoma.json, nodes nut_result, nut_basis,
# nut_ihc. Only trees whose site a source reports NUT carcinoma at offer it.
# ------------------------------------------------------------------------------------------
NUT_REASON = " Squamous features named in the same report do not change the code."


def nut_nodes(prefix, *, skin=False):
    """<p>nut_result, <p>nut_basis and <p>nut_tests. The evidence's nut_ihc is a choice
    between a NUTM1 result, a NUT immunostain over 50% and neither, so it is built as a
    histology_subclassification whose 'neither' option returns to the histology screen: an
    ihc_checklist would need a fixed fallback code, and 8010/3 would replace the report's own
    term. The evidence's deposit option goes to <p>deposit, which asks the primary (D10)."""
    hist = _nid(prefix, "histology")
    result_opts = [
        go("The sample is a deposit in a lymph node, bone, liver or another organ, and the file "
           "names a different site where the tumour began", _nid(prefix, "deposit"),
           note="NUT evidence nut_result: Luo 2025, p. 8 ('Common sites of metastasis of NUT "
                "carcinoma include bone and liver'); Lemelle 2022, p. 6. D10: the deposit "
                "question asks the primary."),
        refer("The report calls the tumour a sarcoma with a NUTM1 rearrangement (for example "
              "undifferentiated epithelioid sarcoma with CIC, BCORL1 or MXD1), and it arises in "
              "a bone", 8,
              "A NUTM1-rearranged sarcoma is not NUT carcinoma. It is coded with the malignant "
              "bone tumours (Group VIII) at the bone it arises in.", recapture=True,
              note="Luo 2025, p. 2 ('other NUTM1 fusion partners (that is, CIC, MXD4 and YAP1) "
                   "are typically WHO-unclassified sarcomas') and p. 5. recapture_site: the "
                   "bone is not this tree's site."),
        refer("The report calls the tumour a sarcoma with a NUTM1 rearrangement, at any site "
              "other than bone", 9,
              "A NUTM1-rearranged sarcoma is not NUT carcinoma. It is coded with the soft-tissue "
              "and other extraosseous sarcomas (Group IX).",
              note="Luo 2025, p. 2 and p. 5 ('most often in the abdomen, soft tissue or central "
                   "nervous system')."),
        refer("The report calls the tumour a leukaemia with a NUTM1 rearrangement", 1,
              "A NUTM1-rearranged leukaemia is not NUT carcinoma. It is coded with the "
              "leukaemias (Group I) and recorded at the bone marrow (C42.1).",
              captures={"topography": "C42.1"},
              note="Luo 2025, p. 13 and p. 5 (table image); WHO Rule E, p. 15."),
    ]
    if skin:
        result_opts.append(go(
            "The report calls a skin tumour a poroma or porocarcinoma with a YAP1::NUTM1 fusion",
            hist, note="Luo 2025, p. 5 ('NUTM1-rearranged porocarcinomas arise within the "
                       "skin') and p. 12. Skin trees only: the clerk chooses poroma or "
                       "porocarcinoma on the histology screen."))
    result_opts += [
        go("The diagnosis names NUT carcinoma or NUT midline carcinoma", _nid(prefix, "nut_basis"),
           note="Luo 2025, p. 2; Lemelle 2022, p. 4."),
        go("The diagnosis names another carcinoma (for example poorly differentiated carcinoma), "
           "and the file reports a NUT immunostain or a NUTM1 gene test",
           _nid(prefix, "nut_tests"),
           note="Luo 2025, p. 7 ('In the context of a tumour with a carcinoma histology'; "
                "'diffuse (>50% of nuclei) positive for nuclear staining by NUT IHC is 100% "
                "specific'); Lemelle 2022, p. 6."),
    ]
    gene = ("A NUTM1 rearrangement or fusion found by FISH, RT-PCR or sequencing")
    stain = ("A NUT immunostain with nuclear staining in more than half (over 50%) of the tumour "
             "cells")
    return [
        node(_nid(prefix, "nut_result"), "histology_subclassification", 4, "NUT carcinoma",
             "What does the file report for this tumour?",
             "Choose the first answer that matches the file. Keratin, p63, p40 and CD99 stains "
             "do not decide NUT carcinoma; a NUT immunostain or a NUTM1 gene test does.",
             result_opts, [],
             "D12. NUT_carcinoma.json nut_result. Lemelle 2022, p. 7 ('This epithelial "
             "epidermoid marker is nonspecific in this setting'; 'falsely suggested by tumour "
             "expression of CD99'); Luo 2025, p. 6-7."),
        node(_nid(prefix, "nut_basis"), "histology_subclassification", 5, "NUT carcinoma",
             "Does the file hold a positive NUTM1 gene result?",
             "A NUTM1 result is written as a NUTM1 (NUT) rearrangement, a translocation "
             "t(15;19), or a fusion such as BRD4::NUTM1, BRD3::NUTM1 or NSD3::NUTM1, found by "
             "FISH, RT-PCR or sequencing.",
             [
                 named("Yes: a NUTM1 rearrangement or fusion is reported", "8023", NUT_REASON.strip(),
                       basis=8,
                       note="D12, D15 (a gene test specific to the entity, basis 8). Lemelle "
                            "2022, p. 7 ('the translocation involving BRD3/4 and NUT is "
                            "specific for NC'), p. 2; Luo 2025, p. 2, p. 6."),
                 named("No: the diagnosis rests on the histology report, with or without a NUT "
                       "immunostain", "8023", NUT_REASON.strip(),
                       note="D12. Lemelle 2022, p. 2 ('The diagnosis is guided by anti-NUT "
                            "nuclear immunostaining'), p. 6; Luo 2025, p. 2, p. 6."),
             ], [],
             "D12. NUT_carcinoma.json nut_basis. D5: NUT carcinoma with squamous features is "
             "8023/3, the entity's one code."),
        node(_nid(prefix, "nut_tests"), "histology_subclassification", 5, "NUT carcinoma",
             "Which NUT results does the file report?",
             "Choose the first answer that matches. A NUT immunostain counts only when the "
             "report states nuclear staining in more than half (over 50%) of the tumour cells.",
             [
                 named(gene, "8023", NUT_REASON.strip(), basis=8,
                       note="D12, D15. NUT evidence ihc_rules order 1: Luo 2025, p. 2; Lemelle "
                            "2022, p. 6, p. 7."),
                 named(stain, "8023", NUT_REASON.strip(),
                       note="D12. NUT evidence ihc_rules order 2: Luo 2025, p. 7 ('diffuse "
                            "(>50% of nuclei) positive for nuclear staining by NUT IHC is 100% "
                            "specific'); Lemelle 2022, p. 6, p. 7."),
                 go("Neither: the NUT immunostain is negative or stains half of the tumour "
                    "cells or fewer, and no NUTM1 rearrangement is reported", hist,
                    note="NUT evidence ihc_rules order 3 (fallback: no NUT code). The clerk "
                         "returns to the histology screen and the report's own term gives the "
                         "code."),
             ], [],
             "D12. NUT_carcinoma.json nut_ihc, built as a choice (see nut_nodes())."),
    ]


# ------------------------------------------------------------------------------------------
# The picker (D2) and the tree
# ------------------------------------------------------------------------------------------
PICKER_REPORT: dict = {}


def _option_pairs(n) -> set:
    """Every code a node's options emit (not its rules or fallback)."""
    return {o["morphology_code"] for o in n.get("options") or []
            if isinstance(o, dict) and o.get("morphology_code")}


# Live ICD-O-3.2 terms a picker does not search by, each by registrar ruling. {(code, term): why}
SEARCH_TERMS_WITHHELD = {
    ("8071", "Keratoacanthoma"): "registrar, 8 October 2026 (review A9): a keratoacanthoma is not "
                                 "registered unless the pathologist calls it squamous cell "
                                 "carcinoma",
}


def picker_node(prefix, tree_id, offered, *, d11=(), keep=()):
    """<p>picker (D2). Candidates: every (code, 3) ICCC-2017 places in Group XI at a routed site
    of the tree. Offered when the code is valid at EVERY routed site (in a Group XI range, or a
    code in `d11` that no ICCC-2017 range of any group holds there: standing rule 3, D11). Left
    out: a Preferred term ICD-O-3.2 marks [obs] (D3), the XId melanoma codes the melanoma
    option reaches (D13), and `offered` (the codes the histology screen and its subtype
    screens offer) unless listed in `keep`. Codes valid at only some routed sites are reported
    (PICKER_REPORT, coding_note), not offered."""
    row = tree_row(tree_id)
    sites = row["sites"]
    if not sites:
        raise TreeError("%s routes no site; it has no picker" % tree_id)
    candidates = sorted({r["morphology_code"] for r in xi_records()
                         if r["behavior_code"] == "3"
                         and any(iccc_status(r["morphology_code"], s) == ICCC_GROUP
                                 for s in sites)} | set(d11))
    mel = melanoma_codes()
    opts, partial, held, obsolete = [], [], [], []
    for c in candidates:
        status = {s: iccc_status(c, s) for s in sites}
        ok = all(v == ICCC_GROUP or (v == "none" and c in d11) for v in status.values())
        if not ok:
            if c in d11:
                raise TreeError("%s: D11 code %s is placed in another group at %s" % (
                    tree_id, c, ", ".join(s for s, v in status.items() if v.startswith("other"))))
            partial.append(c)
            continue
        term(c, "3")
        if preferred_is_obsolete(c, "3"):
            obsolete.append(c)
            continue
        if c in mel:
            continue
        if c in offered and c not in keep:
            held.append(c)
            continue
        subs = sorted({sub for s in sites for sub in iccc_subgroups(c, s)})
        why = ("ICCC-2017 subgroup %s at this tree's sites" % "/".join(subs) if subs else
               "D11: no ICCC-2017 range holds it at this tree's sites; standing rule 3 keeps it "
               "in Group XI")
        o = named(term(c, "3"), c, note="D2 picker: %s." % why)
        found = [t for t in live_search_terms(c, "3") if (c, t) not in SEARCH_TERMS_WITHHELD]
        if found:
            o["search_terms"] = found
        opts.append(o)
    PICKER_REPORT[tree_id] = {"offered": [o["morphology_code"] for o in opts],
                              "partial": partial, "held_as_options": held,
                              "obsolete": obsolete, "d11": sorted(d11)}
    n = node(
        _nid(prefix, "picker"), "histology_subclassification", 5, "Another carcinoma",
        "Which carcinoma does the report name?",
        "Type part of the name in the box and the matching options appear. The other names "
        "ICD-O-3.2 gives a tumour find it too. Use the report's own term. A carcinoma first "
        "diagnosed outside %s is coded at its primary site." % row["where"],
        opts, [],
        "D2 (registrar, 8 October 2026: 'Picker, as in Group 10'): every code ICCC-2017 places "
        "in Group XI (behaviour 3) at all of %s's routed sites (%s), plus the standing-rule-3 "
        "codes the evidence names (D11: %s); less the [obs] Preferred terms (D3: %s), the XId "
        "melanoma codes the melanoma option reaches (D13) and the codes the histology screen and "
        "its subtype screens offer (%s); %d options in code order. Valid at only some routed "
        "sites, so not offered: %s."
        % (tree_id, ", ".join(_ranges(sites)), ", ".join(sorted(d11)) or "none",
           ", ".join(obsolete) or "none", ", ".join(held) or "none", len(opts),
           ", ".join(partial) or "none"))
    n["prefill_filter_from_search"] = True
    return n


def _checklist_pairs(nodes) -> set:
    return {r["morphology_code"] for n in nodes if n.get("node_type") == "ihc_checklist"
            for r in n.get("resolution_logic") or [] if r.get("morphology_code")}


def make_tree(tree_id, nodes, *, subtype_screens=(), d11=(), picker_keep=(), label=None):
    """Assemble a tree: check every node carries the tree's prefix, append the picker (D2),
    and put IHC_CONFIRMS on every basis-7 option whose pair a stain panel rule of this tree
    emits. `subtype_screens`: the node ids, besides <p>histology and the NUT screens, whose
    options count as offered (the picker leaves their codes out). `d11`: codes the evidence
    names that standing rule 3 keeps in Group XI at this tree's sites. `picker_keep`: offered
    codes the picker keeps because the screen offers them only under a narrower label."""
    row = tree_row(tree_id)
    prefix = row["prefix"]
    ids = [n["node_id"] for n in nodes]
    for nid_ in ids:
        if not nid_.startswith(prefix):
            raise TreeError("%s: node %s does not carry the prefix %s" % (tree_id, nid_, prefix))
    if len(set(ids)) != len(ids):
        raise TreeError("%s: a node id is declared twice" % tree_id)
    by_id = {n["node_id"]: n for n in nodes}
    screens = [_nid(prefix, "histology")] + list(subtype_screens) + [
        i for i in ids if i.startswith(_nid(prefix, "nut_"))]
    offered = set()
    for s in screens:
        if s not in by_id:
            raise TreeError("%s: screen %s is not a node of the tree" % (tree_id, s))
        offered |= _option_pairs(by_id[s])
    nodes = list(nodes) + [picker_node(prefix, tree_id, offered, d11=d11, keep=picker_keep)]
    stained = _checklist_pairs(nodes)
    for n in nodes:
        if n.get("node_type") == "ihc_checklist":
            continue
        for o in n.get("options") or []:
            if (o.get("morphology_code") in stained and o.get("basis_of_diagnosis") == 7
                    and not o.get("upgrade_path")):
                o["upgrade_path"] = IHC_CONFIRMS
    return {"tree_id": tree_id,
            "tree_label": label or "%s (%s; ICCC-3 Group XI, behaviour 3 only)"
                                   % (row["label"], ", ".join(_ranges(row["sites"])) or "no "
                                      "routed site"),
            "entry_node": _nid(prefix, "document_inventory"),
            "topography": _ranges(row["sites"]),
            "basis_of_diagnosis_defaults": dict(BASIS_DEFAULTS),
            "nodes": nodes}


# ------------------------------------------------------------------------------------------
# The evidence-document mapping (docs/evidence_documents/group_11.json)
# ------------------------------------------------------------------------------------------
def gate_mapping(gate) -> dict:
    """The mapping entry for one evidence gate, in apply_evidence_documents.py's format. Each
    option's tier is its captured basis_evidence_tier; it is a laboratory copy when it routes
    to a labs_ screen. TIER_TICKS is the source of the rules, and this file is their
    registrar-readable record: change a rule there and rewrite the file
    (python3 build/group11_tree.py --write-evidence-map)."""
    opts = gate["options"]
    tiers = [o["captures"]["basis_evidence_tier"] for o in opts]
    has_markers = "markers" in tiers
    lab_copy = {t for o, t in zip(opts, tiers) if "_labs_" in "_" + o["next_node"]}
    out = []
    for i, (o, t) in enumerate(zip(opts, tiers)):
        req = list(TIER_TICKS[t]["requires"])
        exc = list(TIER_TICKS[t]["excludes"])
        is_copy = "_labs_" in "_" + o["next_node"]
        rationale = TIER_RATIONALE[t]
        if t == "markers":
            pass
        elif is_copy:
            req = ["lab"] + req if "lab" not in req else req
            rationale = ("Registrar, 6 October 2026: the laboratory screen follows the checklist "
                         "only when Lab Report is ticked. This copy of the tier requires Lab "
                         "Report and routes through the laboratory screen; label and captures "
                         "are the tier's own. " + rationale)
        elif t in lab_copy:
            exc = exc + ["lab"]
            rationale = ("Excludes Lab Report: a ticked Lab Report takes the laboratory copy of "
                         "this tier. " + rationale)
        elif t == "imaging" and has_markers:
            exc = exc + ["lab"]
            rationale = ("Excludes Lab Report: imaging with a Lab Report is the marker tier. "
                         + rationale)
        out.append({"index": i, "label_head": o["label"][:60], "kind": "tier",
                    "requires": req, "any_of": [], "excludes": exc, "rationale": rationale,
                    "confidence": "high"})
    return {"group": GROUP, "node_id": gate["node_id"], "question_edit": "", "hint_edit": "",
            "options": out}


def evidence_mapping(trees) -> dict:
    """The docs/evidence_documents/group_11.json payload: one entry per tree's evidence gate."""
    nodes = [gate_mapping(n) for t in trees for n in t["nodes"]
             if n.get("node_type") == "document_inventory"]
    return {"group": GROUP, "nodes": nodes}
