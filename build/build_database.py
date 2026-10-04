#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_database.py — ICCC-3 Lookup Tool build + validation pipeline.

Workstream E, UCI/UCCF Paediatric Cancer Registry.

What it does (Architecture & File System §9):
  1. Regenerates data/aliases/alias_index.json from every data/aliases/aliases_group_*.json.
  2. Validates every data/database/group_*_dt.json that exists — internal integrity,
     Group 1 schema extensions, cross-layer references, and the source of truth (Layer 1).
  3. Prints a grouped pass/fail report and exits 0 (pass) or 1 (fail).

Design rules:
  * Python 3 standard library only. No network. Deterministic output.
  * MISSING FILES ARE A NOTICE, NEVER A FAILURE. The script runs after each tree is
    authored (Group 1 Pathway §7.6 step 6), so on the first run only group_01_dt.json
    exists, with an empty decision_trees[], no aliases, no router and no app.js.
  * Every check is a small named function returning a list of (level, message) findings,
    so a check can be read — and added — in isolation.
  * The ONLY file written is data/aliases/alias_index.json. Everything else is stdout.

Usage:
    python3 build/build_database.py [--strict] [--repo PATH] [--layer1 PATH] [--quiet]

    --strict   promote every WARN to a FAIL
    --repo     repository root (default: the parent of this script's directory)
    --layer1   the read-only source-of-truth directory
               (default: <repo>/../../ICD coding, or $ICD_LAYER1)
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import json
import os
import re
import sqlite3
import sys
from pathlib import Path

# --------------------------------------------------------------------------------------
# Vocabularies and constants (all drawn from the specs; nothing invented here)
# --------------------------------------------------------------------------------------

# Decision Tree JSON Build master §3A — the eleven shared types — plus `numeric_gate`,
# a ratified Group 1 extension (Group 1 Pathway §7.3 item 1).
NODE_TYPES = {
    "clinical_presentation",
    "site_capture",
    "document_inventory",
    "clinical_alias",
    "morphology_only",
    "imaging_pathway",
    "ihc_checklist",
    "cytogenetics_dropdown",
    "molecular_freetext",
    "histology_subclassification",
    "site_resolution",
    "numeric_gate",  # Group 1 extension, Pathway §7.3
}

# NOS-fallback rule BY NODE TYPE (DT master §3D; nodes.md §2) — not a step-number rule.
NOS_REQUIRED_TYPES = {
    "ihc_checklist",
    "cytogenetics_dropdown",
    "molecular_freetext",
    "numeric_gate",
}
NOS_FORBIDDEN_TYPES = {
    "clinical_presentation",
    "site_capture",
    "document_inventory",
    "clinical_alias",
    "morphology_only",
    "imaging_pathway",
    "histology_subclassification",
    "site_resolution",
}

# Router-tier node types never appear inside a group_XX_dt.json (DT master §3B).
ROUTER_ONLY_TYPES = {"clinical_presentation", "site_capture"}

# Group 1 Pathway §7.3 item 4.
DETECTION_METHODS = {
    "karyotype_only",
    "fish_or_rtpcr_only",
    "karyotype_or_fish",
    "karyotype_and_fish",
    "karyotype_or_dna_index",
}

# Group 1 Pathway §7.3 item 8 / §5.4.
CLASSIFICATION_SYSTEMS = {"WHO-HAEM5", "ICC-2022"}

# Group 1 Pathway §7.3 item 2 — marker-intensity tokens.
MARKER_INTENSITIES = {"strong", "weak"}

# DT master §2 — every field is required; null is allowed where it does not apply.
MORPHOLOGY_FIELDS = [
    "morphology_code",
    "morphology_name",
    "iccc3_subgroup_id",
    "iccc3_subgroup_name",
    "who_version",
    "behavior_code",
    "diagnostic_tests_required",
    "ihc_markers_required",
    "ihc_markers_exclude",
    "imaging_sufficient",
    "imaging_features",
    "nos_fallback_code",
    "nos_fallback_name",
    "clinical_alert",
    "coding_note",
    "code_neutral_molecular",
    "redcap_value",
    "primary_sites",
    "topography_dependent",
    "topography_routing_note",
]

# Fields that may never be null (DT master §2 field rules).
MORPHOLOGY_NOT_NULL = ["morphology_code", "morphology_name", "behavior_code"]

DIAGNOSTIC_TESTS = {
    "Referral only",
    "Histology",
    "Imaging",
    "IHC",
    "Flow cytometry",
    "Cytogenetics/FISH",
    "Molecular/PCR",
    # In-situ hybridisation. NOT a synonym for IHC: Pathway §4.3 makes EBER ISH on tissue
    # the only entity-defining EBV test, says LMP1 IHC cannot substitute for it (LMP1 is
    # absent in latency I and 0), and rules that serology cannot upgrade any code. Without
    # its own member, an EBER-resolving provisional_pending cannot name its own test and
    # EBER can never appear as an outstanding-workup row anywhere in Group II.
    # DT master §2 documents this list; that file is owned elsewhere and is not edited here.
    "ISH",
    # tolerated compound forms seen in the master's own worked example
    "IHC or flow cytometry",
}

# Registrar ruling, 16 Sep 2026 — `confidence` is removed from the engine and
# `confidence_ceiling` is no longer written by any group from Group 4 on. It
# survives here only as legacy data on Groups 1-3, which the engine now
# ignores; stripping it from their files is a later migration. Where an entry
# still carries the field it must still be a real ceiling value, so the check
# stays, conditional on presence rather than required.
CONFIDENCE_CEILINGS = {"high", "medium", "low"}

# Cryptic-genetics lint (Group 1 Pathway §4.4 and §7.5).
#   9814  ETV6::RUNX1  — cryptic, needs FISH/RT-PCR, invisible on karyotype
#   9965  FIP1L1::PDGFRA — needs FISH (CHIC2 deletion) or RT-PCR
#   9910  AMKL NOS — the CBFA2T3::GLIS2 / NUP98-r / KMT2A-r AMKL fallback (RT-PCR / NGS)
#   9911  AMKL with t(1;22) RBM15::MRTFA
CRYPTIC_TERMINAL_CODES = {"9814", "9965", "9910", "9911"}

# --------------------------------------------------------------------------------------
# Group II extensions (Group II build contract §3). These are FIELDS on existing
# structures, never new node types — Group II adds nothing to NODE_TYPES (contract §0.3).
# --------------------------------------------------------------------------------------

# Contract §3.4 — the closed test-result vocabulary.
TEST_RESULT_STATES = {
    "positive",
    "negative",
    "not_assessable",
    "not_done",
    "failed",
    "not_available",
    "not_indicated",
    "adequate",
    "inadequate",
}

# Tests whose failure mode is UNINTERPRETABLE rather than negative (contract §3.4;
# Pathway §2.4, §4.3, §7.3 item 4). A node that branches on one of these must offer
# `not_assessable`, and must not send it where it sends `negative`.
UNINTERPRETABLE_TEST_VARIABLES = {"eber_status", "fish_status", "fna_adequacy"}

# Contract §3.5 / Pathway §7.5 — 9709 has no /3 half. There is no such code.
NO_SLASH3_CODES = {"9709"}

# Contract §3.5 — the comparisons an entity_boundary threshold may use.
ENTITY_BOUNDARY_OPERATORS = {">", ">=", "<", "<=", "==", "!="}

# Viral-gate lint (contract §6; Pathway §5.5). These codes are DEFINITIONALLY viral —
# the virus is part of the entity, not an association found alongside it.
VIRAL_GATED_CODES = {
    "9678": "hhv8_lana1",       # primary effusion lymphoma
    "9738": "hhv8_lana1",       # large B-cell lymphoma arising in HHV8+ Castleman disease
    "9827": "htlv1_serology",   # adult T-cell leukaemia/lymphoma
    "9719": "eber_status",      # extranodal NK/T-cell lymphoma, nasal type
    "9724": "eber_status",      # systemic EBV+ T-cell lymphoma of childhood
    "9725": "eber_status",      # hydroa vacciniforme-like lymphoproliferative disorder
    "9737": "alk_ihc",          # ALK-positive large B-cell lymphoma
}

# Spelling is not the clinical fact. Group 1 gates the very same 9827 terminal on
# `htlv1_status` where the Group II vocabulary (contract §5) says `htlv1_serology`; a
# correct file must never be failed over which of the two an author reached for.
VIRAL_GATE_VARIABLES = {
    "hhv8_lana1": {"hhv8_lana1", "hhv8_status", "hhv_8_status", "hhv8", "lana1_status",
                   "lana_1_status"},
    "htlv1_serology": {"htlv1_serology", "htlv1_status", "htlv_1_serology",
                       "htlv_1_status", "htlv1"},
    # `ebv_status` is deliberately NOT here. Every other entry names the TEST; that one
    # names the virus, and it is exactly what an author reaches for when recording a
    # serology result. Pathway §4.3 is explicit that serology cannot upgrade any code —
    # VCA IgG+/IgM-/EBNA-1 IgG+ is the near-universal state in a high-EBV-burden
    # population and supports nothing, EBNA-1 IgG is unreliable in HIV-positive patients,
    # and viral load has no agreed threshold, unit or specimen. EBER ISH on tissue is the
    # only entity-defining EBV test, so only names for that test may satisfy this gate.
    "eber_status": {"eber_status", "eber", "eber_ish", "eber_ish_status",
                    "ebv_eber_status"},
    "alk_ihc": {"alk_ihc", "alk_status", "alk", "alk_ihc_status"},
}

# The same fact recorded as a marker token in a `positive[]` list (Pathway §6 reads
# "LANA-1+ with effusion", "ALK+ / CD20- / CD30-"), intensity suffix stripped.
VIRAL_GATE_MARKERS = {
    "hhv8_lana1": {"HHV8", "HHV-8", "LANA", "LANA1", "LANA-1", "HHV8-LANA1",
                   "HHV-8 LANA-1"},
    "htlv1_serology": {"HTLV1", "HTLV-1"},
    "eber_status": {"EBER", "EBER-ISH", "EBV", "EBV-EBER"},
    "alk_ihc": {"ALK", "ALK1", "ALK-1", "ALK D5F3"},
}

VIRAL_GATE_LABELS = {
    "hhv8_lana1": "HHV-8 LANA-1",
    "htlv1_serology": "HTLV-1 serology",
    "eber_status": "EBER ISH",
    "alk_ihc": "ALK IHC",
}

# --------------------------------------------------------------------------------------
# Under-determined-code lint (Pathway §4.2; contract §3.2, §6). Two entities that are
# phenotypically INDISTINGUISHABLE from Burkitt lymphoma — high-grade/large B-cell
# lymphoma with 11q aberration, and B-ALL with MYC rearrangement — are separated from it
# only by FISH. Where FISH is unavailable they are absorbed into 9687 silently. In a
# malaria-endemic, high-EBV setting Burkitt is the commonest childhood cancer, so this is
# the highest-volume way this group can record something firmer than its evidence.
# --------------------------------------------------------------------------------------

# Variables that carry a CYTOGENETIC/MOLECULAR result. `myc_ihc_pct` is deliberately
# absent: MYC IHC is not FISH, and Pathway §4.2/§5.1 keep an explicit 30-50% indeterminate
# band precisely because the stain does not settle the question the FISH settles.
FISH_EVIDENCE_VARIABLES = {
    "fish_status", "fish_panel_performed", "fish_result", "fish_performed",
    "fish_panel", "myc_fish", "myc_fish_status", "myc_status", "myc_rearrangement",
    "cytogenetics_status", "cytogenetics_result", "karyotype_status", "molecular_result",
}

# A result that actually came back. Anything in UNRESOLVED_RESULT_TOKENS did not.
# `fish_status` in Pathway §5.1 takes done / failed / not available / not indicated, and
# `fish_panel_performed` takes panel names or "none", so the deny-list is the reliable
# half; a value outside BOTH lists is accepted but reported, so a typo is visible rather
# than a silent pass.
RESOLVED_RESULT_TOKENS = {
    "positive", "negative", "done", "performed", "completed", "detected",
    "not_detected", "present", "absent", "rearranged", "not_rearranged",
    "normal", "abnormal", "adequate", "y", "yes", "true",
}
UNRESOLVED_RESULT_TOKENS = {
    "not_done", "none", "failed", "not_available", "not_indicated", "not_assessable",
    "unknown", "pending", "inadequate", "n", "no", "false", "not_performed", "awaited",
}

# Variables whose values are PANEL NAMES, not result states — Pathway §5.1 gives
# `fish_panel_performed` the values ETV6::RUNX1 / BCR::ABL1 / KMT2A / ploidy / none. Any
# value but "none" is a panel that was run, so these are judged by the deny-list alone and
# never reported as an unrecognised result token.
FISH_PANEL_VARIABLES = {"fish_panel_performed", "fish_panel"}

# satisfies_tests values and detection_method labels that discharge the FISH requirement.
FISH_SATISFYING_TESTS = {"Cytogenetics/FISH", "Molecular/PCR"}
FISH_DETECTION_METHODS = {"fish_or_rtpcr_only", "karyotype_or_fish", "karyotype_and_fish"}

# The codes the policy covers, and what is absorbed into each when FISH never returns.
# `context` is None for an arm that applies on every route; a non-None arm fires only
# where the route establishes that clinical context.
UNDERDETERMINED_CODES = {
    "9687": {
        "label": "Burkitt lymphoma",
        "absorbed": "high-grade/large B-cell lymphoma with 11q aberration, and B-ALL with "
                    "MYC rearrangement — both phenotypically indistinguishable from Burkitt",
        "flag": "MYC status unknown; HG/LBCL-11q and HGBL-DH not excluded",
        "context": None,
        "reason_tokens": ("myc", "11q", "fish", "hgbl"),
    },
    "9680": {
        "label": "Diffuse large B-cell lymphoma, NOS",
        "absorbed": "large B-cell lymphoma with IRF4 rearrangement, a curable paediatric "
                    "head-and-neck disease that is over-treated when it is absorbed here",
        "flag": "possible LBCL-IRF4",
        "context": "localised paediatric head-and-neck disease",
        "reason_tokens": ("irf4", "mum1", "fish"),
    },
}

# The context gate for the 9680 arm. Pathway §5.1 defines NO head-and-neck site variable,
# so these names are anticipatory: if none of them is ever established in the file the arm
# reports a NOTE saying it found nothing to test, rather than passing silently.
HEAD_AND_NECK_CONTEXT_VARIABLES = {
    "primary_site_region", "site_region", "primary_compartment", "anatomic_region",
    "disease_region", "head_and_neck_site",
}
HEAD_AND_NECK_CONTEXT_VALUES = {
    "head_and_neck", "head_neck", "headandneck", "waldeyer", "waldeyers_ring",
    "cervical", "tonsil", "nasopharynx", "jaw", "maxillofacial",
}

# Values that record a test as POSITIVE. A variable merely listed as captured says the
# question was asked, not that the answer was yes — that distinction is the whole lint.
POSITIVE_RESULT_TOKENS = {
    "positive", "pos", "detected", "reactive", "confirmed", "confirmed_positive",
    "present", "y", "yes", "true",
}

# --------------------------------------------------------------------------------------
# Group III extensions (docs/group_03_build_contract.md, which reconciles Revision 2 of
# the Group 3 pathway with the DT master file).
#
# SEVEN FIELDS on existing structures. Contract §2 opens no new node type, so nothing in
# this block touches NODE_TYPES — the same discipline Groups 1 and 2 kept.
#
# Every constant below is TRANSCRIBED from the contract, section by section. Nothing here
# is recalled: rule 5 and rule 8 both say that a name or an entity string checked against
# memory is not checked at all, and the two databases (icdo32.sqlite, ICCC-2017.sqlite)
# are the anchors for everything that can be anchored.
# --------------------------------------------------------------------------------------

GROUP3 = 3

# -- §2(1) diagnosis_rendering — the two-track output -----------------------------------
CNS5_TRACKS = {"who_cns5", "adaptr_descriptive"}
DIAGNOSIS_SUFFIXES = {"nos", "nec", "none"}
GRADE_SYSTEMS = {"arabic", "roman"}

# Rule 1, the numeral invariant: track == "who_cns5"  <=>  grade_system == "arabic".
# Written as a map so both directions come off one table and cannot drift apart.
TRACK_GRADE_SYSTEM = {"who_cns5": "arabic", "adaptr_descriptive": "roman"}

# §2(1): "Arabic set includes 1 (CNS5 Table 3 grades MVNT, PLNTY, meningioma and diffuse
# astrocytoma MYB/MYBL1-altered at 1). Roman set is II, III, IV only."
ARABIC_GRADES = {"1", "2", "3", "4"}
ROMAN_GRADES = {"II", "III", "IV"}

# §2(1): the per-track shape. (required non-null, required null).
TRACK_FIELD_SHAPE = {
    "who_cns5": (("who_diagnosis",), ("descriptive_diagnosis", "comment")),
    "adaptr_descriptive": (("descriptive_diagnosis", "comment"), ("who_diagnosis",)),
}

# §2(1) / rule 9: a grade is a string or null. These two are the shapes that LOOK like a
# grade on screen and carry none — "NA" renders as a grade nobody assigned.
GRADE_NON_VALUES = {"NA", "N/A", "", "null", "None", "-", "—", "unknown", "not applicable"}

# -- §2(2) resource_level_gate — availability as reachability ---------------------------
RL_FAMILIES = {
    "ependymal", "embryonal", "diffuse_glial", "glioneuronal", "meningothelial",
    "sellar", "pineal", "choroid_plexus", "pituitary", "unspecified",
}
RL_LEVELS = {"I", "II", "III", "IV", "V"}
RL_TIERS = {"can_be_considered", "highly_recommended", "obligatory"}

# Rule 3, the tier enum BY FAMILY. Satgunaseelan's ependymoma tables use only the first
# two tiers, so a three-value enum mis-renders every ependymal node. The map is keyed by
# family and holds the tiers that family may carry; a family absent from it may use all
# three.
RL_TIERS_BY_FAMILY = {
    "ependymal": {"can_be_considered", "highly_recommended"},
}

# §2(2) last bullet — the families with no ADAPTR paper behind them. A node in one of
# these MUST carry `"rl_assignment": "by_analogy"`: presenting a borrowed resource level
# as a sourced one is the overstatement this whole field exists to prevent.
# `diffuse_glial` is deliberately ABSENT: the contract exempts only "the paediatric-type
# diffuse gliomas", and the family vocabulary has no way to say paediatric-type, so a
# blanket rule here would produce false FAILs on the adult-type nodes ADAPTR does cover.
RL_FAMILIES_WITHOUT_ADAPTR = {
    "meningothelial", "sellar", "pineal", "choroid_plexus", "pituitary", "glioneuronal",
}
RL_ASSIGNMENT_VALUES = {"by_analogy", "sourced"}

# -- §2(3) entity_annotation — the WHO CNS5 entity, recorded without a code -------------
ENTITY_CODE_STATUS = {"shares_code", "no_code", "awaiting_layer1"}
# How firmly the entity is claimed. Added 2026-09-14 on the registrar’s ruling, after
# two trees handled the same situation differently: an MYCN IHC with no published
# sensitivity, and a DLGNT with 1p untested. Without this, a `who_cns5_entity` rendered
# beside a code reads as established however weak the evidence — the one thing an
# advisory tool must never do. `suggested` REQUIRES a provisional_pending on the same
# branch naming the test that would establish it.
ENTITY_STATUS = {"established", "suggested"}

# §2(3): "The string `(provisional type)` is an extraction artefact of the source's
# italics. It must never appear inside an entity name." Matched case-insensitively and
# with flexible inner whitespace, because the artefact arrives however the extractor left
# it and an author copying it in will not normalise it first.
ENTITY_NAME_ARTEFACT_RE = r"\(\s*provisional\s+type\s*\)"

# Rule 5 — the entity strings must be checked against a TRANSCRIBED CNS5 Table 1, not
# against recall. Revision 2 §9 records that the full transcription (144 rows,
# round-trip verified) lives outside the vault and is regenerable but is NOT in this
# repo. So this constant holds only the rows Revision 2 itself prints in a Table 1
# context — §6.2(3)'s worked `entity_annotation` example and its `shared_with[]` list,
# plus the one divergence §6.2(3) pins explicitly — and the check below says so out
# loud rather than implying it validated 144 rows.
#
# Drop a full transcription at one of CNS5_TABLE1_REFERENCE_FILES and the check upgrades
# itself from "WARN, unverified" to "FAIL, not in Table 1" with no code change.
CNS5_TABLE1_ENTITIES = {
    # Revision 2 §6.2(3), the worked example and its shared_with[] list
    "Posterior fossa ependymoma, group PFA",
    "Posterior fossa ependymoma, group PFB",
    "Supratentorial ependymoma, ZFTA fusion-positive",
    "Supratentorial ependymoma, YAP1 fusion-positive",
    "Spinal ependymoma, MYCN-amplified",
    # Revision 2 §6.2(3), the divergence note: "Table 1 prints
    # `Diffuse pediatric-type high-grade glioma, H3-wildtype and IDH-wildtype`"
    "Diffuse pediatric-type high-grade glioma, H3-wildtype and IDH-wildtype",
}

CNS5_TABLE1_REFERENCE_FILES = (
    # The transcription this repo actually carries: Louis 2021 (Neuro-Oncology 23(8)),
    # Table 1, 109 type rows of the 144 printed (the other 35 are family headings), with
    # a `provisional` flag per row. It is Layer 1 for rule 5 — the same status
    # icdo32.sqlite has for rule 13.
    "data/shared/who_cns5_table1.json",
    "docs/cns5_table1_entities.txt",
    "data/shared/cns5_table1_entities.json",
)

# The divergences Revision 2 §6.2(3) records, as wrong -> right. "Table 1 wins."
# The FET-CREB pair is deliberately NOT here: §6.2(3) records what Table 7 and the prose
# print and does NOT say which spelling Table 1 uses, so encoding either one would be the
# recall rule 5 forbids.
CNS5_TABLE1_DIVERGENCES = {
    # CNS5 Table 2's spelling of the same entity — a comma before "and".
    "Diffuse pediatric-type high-grade glioma, H3-wildtype, and IDH-wildtype":
        "Diffuse pediatric-type high-grade glioma, H3-wildtype and IDH-wildtype",
}

# -- §2(5) basis_of_diagnosis — computed, ENCR ------------------------------------------
BASIS_OF_DIAGNOSIS_VALID = {0, 1, 2, 4, 5, 7, 8, 9}
BASIS_OF_DIAGNOSIS_ABSENT = {3, 6}          # "Codes 3 and 6 do not exist."
BASIS_OF_DIAGNOSIS_OVERRIDE = {0, 9}        # not part of the highest-of-1-8 computation
# §2(5): "Two gaps ENCR leaves, declared rather than inferred."
BASIS_DECLARED_GAPS = {"ihc_counts_as": 7, "methylation_counts_as": 8}
# §2(5): "No Group III terminal may emit basis code 1 — every CNS row in ENCR Table 3
# is basis 2."
BASIS_FORBIDDEN_IN_GROUP3 = 1

# -- §2(7) numeric_gate.bands[].unit ----------------------------------------------------
NUMERIC_GATE_UNITS = {
    # Density and extent — the mitotic and marker thresholds §2(7) was written for.
    "per_mm2", "per_10_hpf", "per_hpf", "percent",
    # Concentration — added 2026-09-14. §3.2 requires the AFP / β-hCG VALUE, not a
    # yes/no, because one control craniopharyngioma reached CSF β-hCG 8.0 against a
    # cut-off of 8.2. A serum marker is not a mitotic density and cannot be expressed
    # in any of the four units above.
    "ng_per_ml", "iu_per_l",
}

# -- §1.2 — the eighteen behaviour-overloaded codes -------------------------------------
GROUP3_BEHAVIOUR_SPLIT_CODES = [
    "9390", "9391", "9442", "9501", "9502", "9505", "9530", "9538", "9539",
    "8000", "8001", "8005", "8270", "8272", "8280", "8281", "8290", "8300",
]
# §1.1 — "Behaviour declaration `0-1,3` — exactly one across every Group III range."
GROUP3_BEHAVIOURS_DECLARED = {"0", "1", "3"}

# -- §1.1 / rule 7 — the codes that do not exist in ICD-O-3.2 ---------------------------
GROUP3_ABSENT_CODES = (
    [str(n) for n in range(9402, 9410)] + ["9422"]
    + [str(n) for n in range(8274, 8280)] + ["9536"]
)
# §1.1: "They are alias *inputs* only." These two alias keys are what a clerk TYPES; the
# prohibition is on what the tool EMITS, so they are not scanned.
ALIAS_INPUT_KEYS = {"alias", "also_known_as"}
# Text a clerk reads. A banned code printed here is a code the clerk can copy.
CLERK_FACING_TEXT_KEYS = {
    "reason", "hint", "label", "question", "name", "morphology_name", "nos_fallback_name",
    "descriptive_diagnosis", "who_diagnosis", "comment", "full_form", "upgrade_path",
    "criterion", "feature", "who_cns5_entity", "iccc3_subgroup_name", "notes",
}
# Author-facing per memory `uccf-lookup-tool-clerk-facing-text` — not displayed, so a
# banned code here is reported but does not block.
AUTHOR_FACING_TEXT_KEYS = {"coding_note", "topography_routing_note"}

# ----------------------------------------------------------------------------------
# Fix dated 18 Sep 2026 (branch group-04-neuroblastoma, review of commit 65444ab) — a
# clerk-facing string must never leak an internal JSON/engine identifier: neither the
# NAME of a schema field (`refer_group`, `next_node`, ...) nor the VALUE of a
# `node_id`/`tree_id` this file itself declares. See check_no_internal_identifier_leaks().
#
# CLERK_FACING_PROSE_KEYS names every key app.js renders as text or a label the clerk
# reads — verified by reading app.js directly, not inferred from the schema. This is a
# SEPARATE, larger set from CLERK_FACING_TEXT_KEYS above on purpose: that one is scoped
# to what the RULE 3/8 banned-code scanner needs, and widening it would change those
# checks' own output; this set is scoped to what THIS check needs. Citations are app.js
# line numbers as of this commit:
#   reason               target.reason in banners/orow (~1533, 1764, 1778, 1860);
#                         diversion_criteria[].reason (~1025); a grade leaf's own
#                         reason (~1718) — already in CLERK_FACING_TEXT_KEYS
#   hint, question        dispatchNode()'s node header (~397-399);
#                         biochemical_questions[].question (~1010)
#   label                 optionLabel()/pick() (~401-404, 663)
#   finding, descriptor, site   optionLabel() fallbacks when `.label` is absent (663)
#   name                  nos_fallback.name, renderEscapes() (~1036)
#   accept_label          direct-terminal button text, optionList() (~672)
#   group_label           marker group tag, markerGrid() (~942)
#   capture_label         molecular_freetext field label, freeText() (~999)
#   variable_label        numeric_gate field label, numericGate() (~986)
#   step_label            the panel heading itself — panel()/pushTrail() call sites
#                         (~579, 2008-2234) — the single most prominent clerk-facing
#                         string in the whole UI, and the "outcomes still in play"
#                         list's own label for a destination node (~884)
#   required_answer       biochemical_questions[].required_answer (~1013)
#   feature               imaging_features[] item / diversion_criteria[].feature
#                         (~1006, 1024) — already in CLERK_FACING_TEXT_KEYS
#   comment, who_diagnosis, descriptive_diagnosis   renderDiagnosisRows() (~1689-1699)
#   who_cns5_entity, evidence, shared_with   entityText() (~1734-1742)
#   defer_to              renderGradeRow(), "Deferred to X" (~1721)
#   resolving_test        provisional_pending.resolving_test, the Provisional row (~1836)
#   alternative_entities, alternative_codes   same Provisional row (~1837-1838)
#   interpretation, context   prior_probability, priorText() (~591-594)
#   upgrade_path          entry/target upgrade_path, the Upgrade row (~1863-1868)
# `iccc3_subgroup_name`, `morphology_name`, `nos_fallback_name`, `full_form`,
# `criterion`, `notes` are already in CLERK_FACING_TEXT_KEYS and carried over below.
CLERK_FACING_PROSE_KEYS = CLERK_FACING_TEXT_KEYS | {
    "finding", "descriptor", "site", "accept_label", "group_label", "capture_label",
    "variable_label", "step_label", "required_answer", "defer_to", "resolving_test",
    "alternative_entities", "shared_with", "evidence", "interpretation", "context",
    "imaging_features",
}

# The engine's OWN vocabulary — a schema field name, never a clinical fact — appearing
# in text a clerk reads. `coding_note`/`topography_routing_note` are exempt by design
# (author-facing, never displayed — memory `uccf-lookup-tool-clerk-facing-text`), same
# as AUTHOR_FACING_TEXT_KEYS above.
INTERNAL_IDENTIFIER_TOKENS = [
    "refer_group", "next_node", "nos_fallback", "resolution_logic", "morphology_code",
    "behavior_code", "captured_variables", "branch_sequence", "test_result_states",
    "node_id", "tree_id",
]


def check_no_internal_identifier_leaks(ctx: DTContext):
    """
    A clerk-facing string must never contain an internal identifier: not the NAME of a
    schema field (`INTERNAL_IDENTIFIER_TOKENS`), and not the VALUE of a `node_id` or
    `tree_id` this file itself declares.

    Found 18 September 2026 reviewing commit 65444ab: `(refer_group 11)` printed
    literally inside a `provisional_pending.reason` a clerk reads in the rendered
    Provisional panel, and bare node ids (`hn_site_resolution`, `sn_grading_staging`,
    `hn_ihc_checklist`, ...) printed inside `reason` strings that pointed a clerk at
    "the next step" by its JSON key rather than by what that step asks. A clerk cannot
    see a field name or a node id anywhere in the rendered interface — a `reason`
    string IS the field's entire content in that panel — so either leak hands them a
    token from a system they have no way to query.

    `CLERK_FACING_PROSE_KEYS` names every key app.js renders as text or a label,
    verified against app.js directly (see the citations above this function, and
    contrast `marker_groups[]` in `check_ihc_checklist_renders_a_control`'s own
    docstring — a key can document the tree for the BUILD without app.js ever
    rendering it to the CLERK, and the two must not be confused).
    `coding_note`/`topography_routing_note` are excluded on purpose: author-facing
    only, never reaching the rendered page (memory `uccf-lookup-tool-clerk-facing-text`)
    — the engine's own vocabulary is exactly where a field name belongs.

    No exemption, no group scoping: every group's file is held to this, including
    Groups 1-3, which pass at zero (verified 18 Sep 2026, before this branch's fixes
    were committed).
    """
    out = []

    node_ids, tree_ids = set(), set()
    for tree in ctx.data.get("decision_trees") or []:
        if isinstance(tree, dict) and isinstance(tree.get("tree_id"), str):
            tree_ids.add(tree["tree_id"])
        for node in tree.get("nodes") or []:
            if isinstance(node, dict) and isinstance(node.get("node_id"), str):
                node_ids.add(node["node_id"])
    # entry_node/next_node values are not tracked separately: a valid one must equal a
    # declared node_id (check_next_node_resolution, check_orphan_nodes), so the node_id
    # set already covers them.
    id_patterns = [(v, re.compile(r"\b" + re.escape(v) + r"\b"))
                   for v in sorted(node_ids | tree_ids)]

    for node_id, node in sorted(ctx.nodes.items()):
        for holder, where in walk_dicts(node):
            for key, value in holder.items():
                if key not in CLERK_FACING_PROSE_KEYS:
                    continue
                loc = "node %s (%s).%s" % (node_id, where or "(node level)", key)
                for v in (value if isinstance(value, list) else [value]):
                    if not isinstance(v, str):
                        continue
                    for tok in INTERNAL_IDENTIFIER_TOKENS:
                        if tok in v:
                            out.append((FAIL, "%s contains the internal identifier "
                                              "%r — a clerk cannot see JSON field "
                                              "names anywhere in the interface, so "
                                              "this leaks the engine's own vocabulary "
                                              "instead of a clinical fact: %r"
                                        % (loc, tok, v)))
                    for idv, rx in id_patterns:
                        if rx.search(v):
                            out.append((FAIL, "%s contains %r, a node_id/tree_id this "
                                              "file declares — a clerk cannot see "
                                              "node or tree ids anywhere in the "
                                              "interface. Name the step in words (its "
                                              "own step_label/question), or drop the "
                                              "pointer where the sentence works "
                                              "without it: %r" % (loc, idv, v)))

    if out:
        return out
    return [(OK, "no clerk-facing string names an internal schema field (%d checked) "
                "or a declared node_id/tree_id (%d checked)"
             % (len(INTERNAL_IDENTIFIER_TOKENS), len(node_ids | tree_ids)))]


# -- §3 — the six trees, the topography each owns, and the sweep ------------------------
GROUP3_TREE_TOPOGRAPHY = {
    "g3_posterior_fossa": ["C71.6", "C71.7"],
    "g3_supratentorial": ["C71.0", "C71.1", "C71.2", "C71.3", "C71.4", "C71.5", "C71.8"],
    "g3_midline": ["C72.2", "C72.3", "C72.4", "C72.5", "C75.1", "C75.2", "C75.3"],
    "g3_spinal": ["C72.0", "C72.1"],
    "g3_meninges": ["C70.0", "C70.1", "C70.9"],
    "g3_unspecified": ["C71.9", "C72.8", "C72.9", "C80.9"],
}
# The keys a tree may declare its topography under. Several spellings, because this field
# is being authored in parallel with this check and a correct file must never be failed
# over which synonym its author reached for — the same reason VIRAL_GATE_VARIABLES
# accepts `htlv1_status` and `htlv1_serology`.
TREE_TOPOGRAPHY_KEYS = ("topography", "topography_codes", "owns_topography",
                        "topography_owned", "topography_range", "topography_owns")

# Rule 12 — the sweep. C70.0–C70.9, C71.0–C71.9, C72.0–C72.9, C75.1–C75.3, C80.9.
GROUP3_TOPOGRAPHY_SWEEP = (
    ["C70.%d" % d for d in range(10)]
    + ["C71.%d" % d for d in range(10)]
    + ["C72.%d" % d for d in range(10)]
    + ["C75.1", "C75.2", "C75.3"]
    + ["C80.9"]
)

# -- §5.3 — name exemptions, and the anchors they rest on --------------------------------
# An exemption lets an entry display a name that is not verbatim in icdo32.sqlite. Each one
# names the source string it rests on, so it COLLAPSES the moment the anchor drifts: if the
# database stops carrying that exact string — because a typo was fixed upstream, or the
# database was replaced — the exemption fails rather than quietly continuing to excuse a
# name nothing verifies.
#
# 2026-09-14: the dict is EMPTY, and that is the point. Group 3 carried one exemption, for
# 9475/3, because the 2019 draft workbook (ICD-O-3.2_MFin_17042019_web.xls) printed
# 'Medullobloastoma, WNT-activated, NOS'. IARC's final workbook
# (ICD-O-3.2_final_update09102020.xls, 9 October 2020) spells it correctly. Rebuilding
# Layer 1 against the final file collapsed the exemption exactly as designed — the build
# FAILed on it rather than passing — and it was then retired, along with the entry's
# source_term anchor. Every Group 3 name now round-trips unaided.
ICDO32_SOURCE_TERM_EXEMPTIONS = {
}

# -- the ICD-O matrix rule, by registrar ruling only -------------------------------------
# ICD-O permits changing a code's behaviour digit to the behaviour the pathologist reports.
# An entry made that way names a (code, behaviour) pair icdo32.sqlite does not print, so the
# round-trip would fail it. Each pair here is a registrar ruling, and it holds only while
# its anchor holds: the SAME term must still exist in icdo32.sqlite at the source behaviour.
# (group, code, behaviour) -> (source behaviour, term).
ICDO32_MATRIX_RULE = {
    # Group 7 open question 2(b), ruled 3 October 2026: calcifying nested stromal-epithelial
    # tumour reported as malignant or metastatic. ICCC-2017 row 67 places 8975/3 in VIIa1.
    (7, "8975", "3"): ("1", "Calcifying nested stromal-epithelial tumor"),
}


# --------------------------------------------------------------------------------------
# Group 4 build contract §3, §8 — the one new field (behaviour_exclusion) and the
# nine validation rules it and the rest of the group's schema force.
# --------------------------------------------------------------------------------------

GROUP4 = 4

# §1: "Behaviour declaration `3` — exactly one, across every Group IV range." Named and
# cited here, the same way GROUP3_BEHAVIOURS_DECLARED is above, so RULE 2 below reads
# the declaration off a constant rather than comparing against a bare "3" written inline
# in the loop. It is NOT a general per-group lookup: Group III's own declaration is
# validated by check_group3_behaviour_split()'s stronger, per-code, ICD-O-3.2-computed
# rule (necessary there because Group III has eighteen behaviour-overloaded codes; Group
# IV has none — contract §1.2 — so a flat membership test is the whole rule). Extending
# this constant into a cross-group table and running the same flat check over Group III
# was considered and rejected: it cannot be verified against the real group_03_dt.json
# without running the build this task must not run, and "do not regress Groups 1-3" is
# the harder constraint. One group, one constant, one scoped check — the same shape
# every other group-specific rule in this file already takes.
GROUP4_BEHAVIOUR_DECLARED = {"3"}

# §0.2 / §8 rule 3 — the one ICCC-3-named code ICD-O-3.2 does not carry at a declared
# behaviour. 8683 exists only at /0 (Gangliocytic paraganglioma); Group IV admits /3
# only, so there is no 8683/3 and no Group IV entry for it (§0.2).
GROUP4_ABSENT_CODE = "8683"

# §2.4 / §8 rule 8, ruling D4 — 9364 is Ewing sarcoma AND the peripheral neuroectodermal
# tumour / pPNET code (IARC's own *Summary of main changes*). Group IV's pPNET aliases
# refer OUT to Group VIII/IX; 9364 must never be what a Group IV terminal emits.
GROUP4_NOT_A_GROUP_CODE = "9364"

# §2.3 / §8 rule 4, ruling D2 — authored in morphology_entries[] so an alias or a
# historical record can resolve, reachable from no tree: no current WHO entity lives on
# the stem, but ICD-O-3.2 does not mark it [obs] either, so the Group 3 obsolete_term
# precedent (thirteen entries, same shape) governs rather than §1.1's absent-code rule.
GROUP4_UNREACHABLE_CODE = "9504"

# §4.2 rule 1 (Visser Table 4, p.06) — the only two codes a no_tissue terminal may name.
GROUP4_VISSER_TABLE4_CODES = {"9500", "8700"}

# §0.6, §2.5 — the topography band ICCC-3 gives to Group III for 9501-9504. A Group IV
# tree whose OWN captured topography sits inside it may never still be able to emit one
# of the four (§8 rule 5's second clause).
GROUP4_G3_OVERLAP_CODES = {"9501", "9502", "9503", "9504"}
GROUP4_G3_OVERLAP_TOPOGRAPHY = (
    ["C70.%d" % d for d in range(10)]
    + ["C71.%d" % d for d in range(10)]
    + ["C72.%d" % d for d in range(10)]
)


# --------------------------------------------------------------------------------------
# Group 5 build contract §8 — Retinoblastoma. Seven rules, and the generalisation of
# check_behaviour_exclusion() that rule 2 asks for.
# --------------------------------------------------------------------------------------

GROUP5 = 5

# Group 6 build contract §8 — Renal Tumours. Defined here, ahead of its own constants
# block (below, near the Raw-hex ban section), because BEHAVIOUR_DECLARED_BY_GROUP
# needs the name at module load time — the same reason GROUP5 sits immediately above
# this dict rather than in Group 5's own block further down.
GROUP6 = 6

# Group 7 build contract §8 — Hepatic Tumours. Defined here for the same reason as
# GROUP6: BEHAVIOUR_DECLARED_BY_GROUP needs it at module load time.
GROUP7 = 7

# Group 8 build contract §7 — Malignant Bone Tumours. Defined here for the same reason as
# GROUP6: BEHAVIOUR_DECLARED_BY_GROUP needs the name at module load time.
GROUP8 = 8

# Group 10 build contract §5 — Germ Cell, Trophoblastic and Gonadal Tumours. Defined here for
# the same reason as GROUP6: BEHAVIOUR_DECLARED_BY_GROUP needs the name at module load time.
GROUP10 = 10

# Which groups have ADOPTED behaviour_exclusion, and what each one's ICCC-3 behaviour
# declaration actually is. Read by check_behaviour_exclusion(), whose "subtle clause"
# fails a block naming a behaviour the group DOES admit — so this table decides the
# check's meaning and a wrong row would invert it. Both values verified against
# ICCC-2017.sqlite on 2026-09-22: Group IV declares "3" across every range, Group V
# declares "3" for 9510-9514 at C00.0-C80.9.
#
# A group absent from this table is not validated by that check at all, which is the
# same position Group 4 contract §3 took in words ("no other group is obliged to adopt
# it"), now written where the code can act on it.
#
# GROUP6 added 22 September 2026 (Group 6 build contract, Task B point 1). Group VI
# writes at least three behaviour_exclusion blocks (8959/0, 8959/1, 8960/1); without
# this row check_behaviour_exclusion() silently skips all of them. Value verified
# directly against ICCC-2017.sqlite the same day — see GROUP6_BEHAVIOUR_DECLARED's own
# comment, above the Group 6 constants block, for the query and result.
BEHAVIOUR_DECLARED_BY_GROUP = {
    GROUP4: {"3"},
    GROUP5: {"3"},
    GROUP6: {"3"},
    # GROUP7 added 2 October 2026 (Group 7 build contract §8). Every ICCC-2017.sqlite
    # range for main_group='VII' (rows 67-72) declares behaviour 3 and nothing else.
    GROUP7: {"3"},
    # GROUP8 added 2 October 2026 (Group 8 build contract §0.2, §7). ICCC-2017.sqlite
    # ranges 59-71 (main_group VIII) declare icdo3_behavior "3" on every row.
    GROUP8: {"3"},
    # GROUP10 added 4 October 2026 (Group 10 build contract §5). ICCC-2017.sqlite ranges
    # 100-117 (Xb, Xc, Xd, Xe) declare behaviour 3 only; ranges 94-99 (Xa, the central
    # nervous system) also admit behaviours 0 and 1. This row is the declaration outside the
    # central nervous system, where every behaviour_exclusion sits. Behaviour per site is
    # enforced by check_group10_codes_fit_site() (rule 1), which reads the ranges themselves.
    GROUP10: {"3"},
}

# Groups whose morphology_name is checked against icdo32.sqlite by check_icdo32_round_trip()
# INSTEAD OF against the REDCap option file by check_redcap_exact_names(). Both guards read
# this one set: a group in one and not the other would get neither name check.
# GROUP10 joins on its build contract §5: morphology_name is the ICD-O-3.2 preferred term,
# and x_morph drifts from it on 64 codes.
ROUND_TRIP_GROUPS = {GROUP3, GROUP4, GROUP6, GROUP7, GROUP8, GROUP10}

ROMAN_BY_GROUP = {
    1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI",
    7: "VII", 8: "VIII", 9: "IX", 10: "X", 11: "XI", 12: "XII",
}

# §0.2 / §8 rule 4 — the ICCC-3-named code ICD-O-3.2 does not carry at a declared
# behaviour. 9514 exists only at /1 (Retinoblastoma, spontaneously regressed); Group V
# admits /3 only, so there is no 9514/3 and no Group V entry for it. Exactly the shape
# of GROUP4_ABSENT_CODE (8683, which exists only at /0).
GROUP5_ABSENT_CODE = "9514"

# §0.2 — the four codes Group V actually builds, generated by
# build/generate_group_inventory.py --group V, not transcribed.
GROUP5_CODES = {"9510", "9511", "9512", "9513"}

# §0.4 — Visser O, et al. Front Oncol 2023;13:1250549, Table 3, pp. 04-05 gives
# retinoblastoma basis "1 or 2" at C69.2 for 9510/3 AND FOR NOTHING ELSE. A terminal
# reached without pathology may name this code and no other: a subtype assigned on
# imaging or on a clinical note alone is the most consequential error available in this
# group, because it reads downstream as a graded, enucleation-confirmed tumour.
GROUP5_NO_PATHOLOGY_BASES = {1, 2}
GROUP5_NO_PATHOLOGY_CODE = "9510"

# §2.5 — 9510 is the only imaging-reachable code. 9513 diffuse infiltrating
# retinoblastoma has no discrete calcified mass and presents later, so the Track-1
# constellation would FALSELY EXCLUDE it; 9511 and 9512 are grades readable only on an
# enucleation specimen.
GROUP5_IMAGING_SUFFICIENT_CODE = "9510"

# §5 — "the map must be TOTAL and DISJOINT over every topography Group IV can carry."
#
# The ORIGINAL sweep here (retired 2026-09-18, a false-FAIL bug) generated every
# C00.0-C80.9 slot and swept it against Layer 1's REDCap topography list — which is
# the whole REGISTRY's topography universe (every code any group can carry), not
# Group IV's. C50.x breast, C34.x lung and C61.9 prostate are real, existing
# topography codes, so they came back "resolve to NO tree" — 292 of them, none a
# Group IV defect, because no Group IV tree was ever supposed to claim them.
#
# "Every topography Group IV can carry" is recorded once already, in
# data/shared/topography_codes.json's `topography_lookup`: the codes whose
# `candidate_groups` list names group 4 (34 of them, 2026-09-18).
# _group4_candidate_topography() reads that file rather than re-deriving or
# hand-transcribing the list — the same reason a Group-IV analogue of
# GROUP3_TREE_TOPOGRAPHY is not hand-built here (see check_group4_topography_map()):
# transcribing C10/C11/C30-C32/C38/C47/C48/C74/C75/C77's own subcodes from memory
# risks getting exactly the subcodes wrong that reading the shared file avoids.
#
# That 34-code universe is still not the WHOLE of what a Group IV case can carry.
# Contract §5's own table makes `g4_other_peripheral` the catch-all for "everything
# else Group IV can carry" — reached through presentation_router.json's
# groups["4"].tree_routing.default, never through an enumerated list (an unknown
# primary, C80.9, is the one member of that "everything else" the router names
# explicitly, and topography_lookup marks it `"route_by_morphology"` rather than
# handing it to group 4 by name — it is not one of the 34). So the map is swept in
# two parts: the 34 codes are checked TOTAL and DISJOINT the way Group III's sweep
# checks its own compartment, and the router's default is separately checked to
# exist and to resolve to a real tree in THIS file — see check_group4_topography_map().


# --------------------------------------------------------------------------------------
# Group 6 build contract §8 — Renal Tumours. Nine validation rules, plus the group-
# scoping extension to check_icdo32_round_trip() / check_redcap_exact_names() that
# §8's own text calls "not optional" (see those two functions). GROUP6 itself is
# defined earlier, immediately above BEHAVIOUR_DECLARED_BY_GROUP, where module load
# order requires it.
# --------------------------------------------------------------------------------------

# §0.2 — every ICCC-2017.sqlite range for main_group='VI' declares behaviour "3" and
# nothing else. Verified directly, not inherited from the contract's own table:
#   SELECT DISTINCT g.group_code, cr.icdo3_behavior FROM groups g
#   JOIN code_ranges cr ON cr.group_id = g.group_id WHERE g.main_group = 'VI'
# returns five rows (VIa1, VIa2, VIa3, VIb x2, VIc), icdo3_behavior = '3' on every one,
# 22 September 2026. A wrong value here would invert both check_behaviour_exclusion()
# (BEHAVIOUR_DECLARED_BY_GROUP, below) and check_group6_behaviour_declaration().
GROUP6_BEHAVIOUR_DECLARED = {"3"}

# §0.3 — the 90 usable (code, behaviour) records. GENERATED by running
# build/generate_group_inventory.py --group VI (joins ICCC-2017.sqlite to
# icdo32.sqlite) on 22 September 2026 and diffed against this file's own 90
# morphology_entries[] codes: identical sets, in identical count (contract's own
# pre-verified "usable 90" figure). Behaviour is uniformly "3"
# (GROUP6_BEHAVIOUR_DECLARED), so a (code, behaviour) test reduces to code membership
# here plus the behaviour-declared set. Not read back off group_06_dt.json itself —
# that would make the fabricated-code guard trivially pass on whatever the file
# already contains, which is the one thing it must not do.
GROUP6_CODES = frozenset([
    "8000", "8001", "8002", "8003", "8004", "8005", "8010", "8011", "8012", "8013",
    "8014", "8015", "8020", "8021", "8022", "8023", "8030", "8031", "8032", "8033",
    "8034", "8035", "8041", "8050", "8051", "8052", "8054", "8070", "8071", "8072",
    "8073", "8074", "8075", "8082", "8120", "8121", "8122", "8130", "8131", "8140",
    "8141", "8143", "8155", "8190", "8200", "8201", "8210", "8211", "8221", "8230",
    "8231", "8240", "8241", "8244", "8245", "8246", "8260", "8261", "8262", "8263",
    "8290", "8310", "8311", "8312", "8316", "8317", "8318", "8319", "8320", "8323",
    "8401", "8430", "8440", "8480", "8481", "8482", "8490", "8504", "8510", "8550",
    "8560", "8562", "8570", "8571", "8572", "8573", "8959", "8960", "8963", "8964",
])

# §2A — the eleven REDCap options the tool cannot emit: ten behaviour exclusions (each
# exists in icdo32.sqlite only at /0 or /1, never at Group VI's declared /3) plus one
# retired number, the first the project has met in a live REDCap option list. Verified
# directly against icdo32.sqlite on 22 September 2026: 8965 has zero rows at all
# (deleted, moved to 9013/0); the other ten exist only at behaviour 0 (8966, 8967,
# 8325, 8361, 9013, 8053, 8060, 8191, 8561) or split 0/1 (8040 — Tumorlet, not the
# "Small cell carcinoma, NOS" REDCap's label claims; that entity is 8041/3, offered
# separately).
GROUP6_ABSENT_CODES = (
    "8965", "8966", "8967", "8325", "8361", "9013",
    "8040", "8053", "8060", "8191", "8561",
)

# §0.5 — the molecular-RCC fork. 8311 is the molecularly DEFINED code (TFE3-
# rearranged, TFEB-altered, ELOC-mutated, FH-deficient, HLRCC-associated, SDH-
# deficient and ALK-rearranged renal cell carcinoma). The five codes a molecular
# result moves a case OFF, onto 8311, are the six code_neutral_molecular:false
# entries in this file minus 8311 itself: 8260, 8310, 8312, 8316, 8319 — verified by
# reading their coding_note fields directly (each states "a molecular result…
# moves a case off this code to 8311/3"), 22 September 2026.
GROUP6_MOLECULAR_DEFINED_CODE = "8311"
GROUP6_MOLECULAR_VACATED_CODES = frozenset({"8260", "8310", "8312", "8316", "8319"})

# §4.2, §0.11 point 3 — Visser Table 3 gives nephroblastoma basis 2 at C64, 8960/3,
# the only Group VI row in the table. imaging_sufficient is true on this code alone.
GROUP6_IMAGING_SUFFICIENT_CODE = "8960"

# §4.4 — anaplasia and the SIOP risk subtypes are prognostic modifiers on 8960 and
# never a code fork.
GROUP6_ANAPLASIA_CODE = "8960"

# §3.1 — 8963 is C64.9-only in this group; the dual-group code whose router branch
# was found dead and fixed during this build (see the 8963 entry's own
# topography_routing_note).
GROUP6_8963_TOPOGRAPHY = "C64.9"


# --------------------------------------------------------------------------------------
# Group 7 build contract §8 — Hepatic Tumours. Nine validation rules, plus the group-
# scoping extension to check_icdo32_round_trip() / check_redcap_exact_names() (§2E).
# GROUP7 itself is defined beside GROUP6, above BEHAVIOUR_DECLARED_BY_GROUP, where
# module load order requires it.
# --------------------------------------------------------------------------------------

# §0.2 — every ICCC-2017.sqlite range for main_group='VII' declares behaviour "3" and
# nothing else: rows 67-72, icdo3_behavior = '3' on all six, queried 2 October 2026.
GROUP7_BEHAVIOUR_DECLARED = {"3"}

# §0.3 — the 92 usable (code, behaviour) records, GENERATED by
# build/generate_group_inventory.py --group VII on 2 October 2026 and pasted here, not
# read back off group_07_dt.json — reading the file under test would make the
# fabricated-code guard pass on whatever the file already holds.
GROUP7_CODES = frozenset([
    "8000", "8001", "8002", "8003", "8004", "8005", "8010", "8011", "8012", "8013",
    "8014", "8015", "8020", "8021", "8022", "8023", "8030", "8031", "8032", "8033",
    "8034", "8035", "8041", "8050", "8051", "8052", "8054", "8070", "8071", "8072",
    "8073", "8074", "8075", "8082", "8120", "8121", "8122", "8140", "8141", "8143",
    "8155", "8158", "8160", "8161", "8162", "8170", "8171", "8172", "8173", "8174",
    "8175", "8180", "8190", "8200", "8201", "8210", "8211", "8230", "8231", "8240",
    "8241", "8244", "8245", "8246", "8260", "8261", "8262", "8263", "8310", "8320",
    "8323", "8401", "8430", "8440", "8470", "8480", "8481", "8482", "8490", "8503",
    "8504", "8510", "8550", "8560", "8562", "8570", "8571", "8572", "8573", "8963",
    "8970", "8991",
])

# §2A — the six REDCap options the tool cannot emit at behaviour 3, verified against
# icdo32.sqlite on 2 October 2026: 8975 exists only at /1; 8148 at /0 and /2; 8202,
# 8264, 8561 and 9013 at /0 only.
GROUP7_ABSENT_CODES = ("8148", "8202", "8264", "8561", "9013")

# Registrar ruling, 3 October 2026 (open question 2): calcifying nested stromal-epithelial
# tumour is registered in Group VII — 8975/1 as ICD-O-3.2 prints it, and 8975/3 under the
# ICD-O matrix rule when the report calls it malignant or describes metastases. The only
# Group VII pairs outside the generated inventory; check_group7_cnset() anchors both on
# Layer 1 and fixes which label carries which behaviour.
GROUP7_RULED_PAIRS = frozenset({("8975", "1"), ("8975", "3")})
_G7_MALIGNANT_RE = re.compile(r"\bmalignant\b|\bmetasta", re.I)

# §0.2 point 3 — the codes ICCC-2017 places in Group VII at ANY site: row 67 (8970,
# with 8975 absent at /3) and row 71 (8160-8162, 8170-8180). Every other Group VII code
# is Group VII only at C22.0/C22.1 (rows 68, 69, 70, 72).
GROUP7_ANY_SITE_CODES = frozenset({
    "8970", "8160", "8161", "8162", "8170", "8171", "8172", "8173", "8174", "8175",
    "8180",
})
GROUP7_C22_ONLY_CODES = GROUP7_CODES - GROUP7_ANY_SITE_CODES
GROUP7_C22_VALUES = {"C22", "C22.0", "C22.1"}

# §0.6, §4.2 — the only codes a no-pathology terminal may name, and at which bases.
# Visser Table 3: hepatoblastoma basis 2 at C22, hepatocellular carcinoma basis 2 at C22.0,
# cholangiocarcinoma basis 2 at C22.1; Table 4: hepatocellular carcinoma basis 4 on
# alpha-fetoprotein; rule 5: 8000/3 at basis 1 or 2. The 8170 and 8160 rows were added on
# the registrar's ruling of 3 October 2026 (open question 4, "go with Visser").
# Basis 1 is out (ruling 3 October 2026, open question 7): Visser rule 3 keeps it for cancers
# found by physical examination, and lists no internal organ. A note naming no method is
# basis 9, unknown (rule 1).
GROUP7_NO_PATHOLOGY_BASES = {0, 1, 2, 4, 9}
GROUP7_NO_PATHOLOGY_ALLOWED = {("8970", 2), ("8000", 2), ("8000", 9),
                               ("8170", 2), ("8170", 4), ("8160", 2)}
_G7_AFP_RAISED_RE = re.compile(r"alpha-fetoprotein (is )?(reported )?raised", re.I)
GROUP7_IMAGING_SUFFICIENT_CODE = "8970"

# §4.3 — the INI1 fork.
GROUP7_RHABDOID_CODE = "8963"
GROUP7_HEPATOBLASTOMA_CODE = "8970"
_G7_SCUD_RE = re.compile(r"small[- ]cell undifferentiated|\bSCUD\b|blastemal|rhabdoid", re.I)
_G7_LOSS_MARKER_RE = re.compile(r"\b(SMARCB1|INI1|SMARCA4|BRG1)\b.*\bloss\b", re.I)
# Anchored on "performed and RETAINED": every loss marker ends "internal control
# retained", which a bare RETAINED with re.I also matched.
_G7_RETAINED_MARKER_RE = re.compile(r"\b(SMARCB1|INI1)\b.*\bperformed and RETAINED\b", re.I)
_G7_SMALL_CELL_RE = re.compile(r"small[- ]cell undifferentiated|\bSCUD\b|blastemal", re.I)
_G7_MRT_DIAGNOSED_RE = re.compile(r"diagnos\w* a malignant rhabdoid tumou?r", re.I)
_G7_HB_DIAGNOSED_RE = re.compile(r"diagnos\w* hepatoblastoma", re.I)
_G7_SMARCA4_RETAINED_RE = re.compile(r"\b(SMARCA4|BRG1)\b.*\bperformed and RETAINED\b", re.I)

# §3.2 — fibrolamellar carcinoma.
GROUP7_FIBROLAMELLAR_CODE = "8171"
_G7_FIBROLAMELLAR_RE = re.compile(r"fibrolamellar(?!-like)", re.I)
_G7_FLC_MOLECULAR_RE = re.compile(r"DNAJB1::PRKACA|PRKACA rearrangement|PRKAR1A loss", re.I)

# §7.1 — the router rules this build owns, and the sites they must resolve at.
GROUP7_ROUTER_C22_CODES = ("8963", "8991", "8000", "8001", "8002", "8003", "8004", "8005")
GROUP7_ROUTER_PROBE_SITES = ("C22.0", "C22.1", "C24.0", "C80.9")


# Raw-hex ban (data.md §5) — the three front-end files, wherever they land in the repo.
HEX_SCANNED_FILENAMES = ["index.html", "app.js", "uccf-tool.css"]
HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{3,8})(?![0-9A-Za-z_-])")

ROMAN = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6,
    "VII": 7, "VIII": 8, "IX": 9, "X": 10, "XI": 11, "XII": 12,
}

FAIL, WARN, OK, NOTE = "FAIL", "WARN", "OK", "NOTE"


# --------------------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------------------

class Report:
    """Collects findings into ordered sections and prints the grouped report."""

    def __init__(self, strict: bool = False) -> None:
        self.strict = strict
        self.sections: list[tuple[str, list[tuple[str, str]]]] = []
        self._current: list[tuple[str, str]] | None = None
        self.checks_run = 0

    def section(self, title: str) -> None:
        self._current = []
        self.sections.append((title, self._current))

    def add(self, findings) -> None:
        if self._current is None:
            self.section("(general)")
        for level, message in findings:
            self._current.append((level, message))

    def run(self, fn, *args, **kwargs) -> None:
        """Run one named check function and record its findings."""
        self.checks_run += 1
        try:
            findings = fn(*args, **kwargs)
        except Exception as exc:  # a crashing check is a build failure, never a traceback
            findings = [(FAIL, "check %s crashed: %s: %s"
                         % (getattr(fn, "__name__", "?"), type(exc).__name__, exc))]
        self.add(findings or [])

    # -- counting -----------------------------------------------------------------
    @property
    def fails(self) -> int:
        return sum(1 for _, f in self.sections for lvl, _m in f if lvl == FAIL)

    @property
    def warns(self) -> int:
        return sum(1 for _, f in self.sections for lvl, _m in f if lvl == WARN)

    @property
    def notes(self) -> int:
        return sum(1 for _, f in self.sections for lvl, _m in f if lvl == NOTE)

    @property
    def oks(self) -> int:
        return sum(1 for _, f in self.sections for lvl, _m in f if lvl == OK)

    def passed(self) -> bool:
        return self.fails == 0 and not (self.strict and self.warns)

    def render(self, quiet: bool = False) -> str:
        out: list[str] = []
        for title, findings in self.sections:
            shown = findings
            if quiet:
                shown = [f for f in findings if f[0] in (FAIL, WARN)]
                if not shown:
                    continue
            out.append("")
            out.append("-- %s %s" % (title, "-" * max(4, 74 - len(title))))
            if not shown:
                out.append("   OK    nothing to check")
            for level, message in shown:
                out.append("   %-5s %s" % (level, message))
        out.append("")
        out.append("=" * 78)
        out.append("Summary")
        out.append("  checks run : %d" % self.checks_run)
        out.append("  OK         : %d" % self.oks)
        out.append("  NOTE       : %d" % self.notes)
        out.append("  WARN       : %d%s" % (self.warns,
                                            "  (promoted to FAIL by --strict)"
                                            if self.strict and self.warns else ""))
        out.append("  FAIL       : %d" % self.fails)
        out.append("")
        out.append("BUILD PASSED" if self.passed() else "BUILD FAILED")
        out.append("=" * 78)
        return "\n".join(out)


# --------------------------------------------------------------------------------------
# Generic helpers
# --------------------------------------------------------------------------------------

def load_json(path: Path):
    """Return (data, findings). data is None when the file is missing or unparseable."""
    if not path.exists():
        return None, [(NOTE, "%s not present — skipped" % path.name)]
    try:
        with path.open(encoding="utf-8") as fh:
            return json.load(fh), []
    except json.JSONDecodeError as exc:
        return None, [(FAIL, "%s is not valid JSON: line %d column %d: %s"
                       % (path.name, exc.lineno, exc.colno, exc.msg))]
    except OSError as exc:
        return None, [(FAIL, "%s could not be read: %s" % (path.name, exc))]


def walk_dicts(obj, path=""):
    """Yield (dict, dotted_path) for every dict nested anywhere inside obj."""
    if isinstance(obj, dict):
        yield obj, path
        for key, value in obj.items():
            sub = "%s.%s" % (path, key) if path else key
            yield from walk_dicts(value, sub)
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            yield from walk_dicts(value, "%s[%d]" % (path, i))


def as_code(value):
    """Normalise a morphology code to a string, or None."""
    if value is None:
        return None
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return value.strip()
    return None


def is_non_reportable(container) -> bool:
    """
    A node or option marked 'not a reportable malignancy' (nodes.md §4).
    The schema does not fix one spelling, so accept the plausible ones.
    """
    if not isinstance(container, dict):
        return False
    if container.get("non_reportable") is True:
        return True
    if container.get("reportable") is False:
        return True
    if container.get("is_reportable") is False:
        return True
    for key in ("terminal_type", "outcome", "terminal_kind", "result_type"):
        val = container.get(key)
        if isinstance(val, str) and val.strip().lower() in (
                "non_reportable", "not_reportable", "non-reportable",
                "not a reportable malignancy"):
            return True
    return False


def is_nos_fallback_object(holder, where) -> bool:
    """
    True when `holder` IS a `nos_fallback` object — {"code", "reason"}, "name" and
    "behavior_code" optional, per DT master §3C/§3D, consumed by app.js's
    fallbackTarget() — rather than some other dict that merely happens to carry a
    'reason'.

    Only 'code' is load-bearing: fallbackTarget() (app.js) reads
    `n.nos_fallback.code`/`.behavior_code`/`.reason` and never touches `.name`, and
    check_terminal_codes_exist() likewise only demands 'code'. Groups 1-3 happened to
    always author a 'name' alongside it, but that is a convention, not the schema —
    Group IV's own fallbacks (e.g. `{"code": "9500", "behavior_code": "3", "reason":
    "…"}` on `sa_ihc_checklist`) correctly omit it, and requiring it here made this
    predicate miss them, which sent every one of them into the code-less-terminal FAIL
    below (Group 4 build contract §3, §8 bug fix 2026-09-18).

    Identified by two things at once, deliberately narrow: the key it hangs off (its
    walk_dicts path ends in "nos_fallback") AND its shape ('code' present). Neither
    alone is enough — a holder could be named nos_fallback without yet having a code
    (still a shape bug worth catching, and check_terminal_codes_exist() catches it),
    or could carry an unrelated 'code' under some other key. Requiring the key AND the
    code keeps this from ever masking a real code-less-terminal violation: a
    `nos_fallback` block with no `code` at all still falls through to that check.
    """
    if not isinstance(holder, dict):
        return False
    last_key = where.rsplit(".", 1)[-1] if where else ""
    if last_key != "nos_fallback":
        return False
    return as_code(holder.get("code")) is not None


def is_provisional_pending_object(holder, where) -> bool:
    """
    True when `holder` IS a `provisional_pending` object (Group II contract §3.2) rather
    than a branch that forgot its destination.

    It matters because §3.2 REQUIRES a clerk-facing `reason` on the block, and the
    code-less-terminal shape check in check_non_reportable_terminals() reads "a `reason`
    and no destination" as an unflagged terminal. A provisional is neither a terminal nor
    a destination: it qualifies the code its own branch already emits, and that branch's
    destination is checked on the branch.

    Identified the same deliberately-narrow way as is_nos_fallback_object(): the key it
    hangs off AND its shape. A block named provisional_pending without a `resolving_test`
    is still a shape bug worth catching, and an unrelated dict carrying a `resolving_test`
    under some other key is not exempted — so this can never absorb a real code-less
    terminal.
    """
    if not isinstance(holder, dict):
        return False
    last_key = where.rsplit(".", 1)[-1] if where else ""
    if last_key != "provisional_pending":
        return False
    return bool(holder.get("resolving_test"))


def is_diversion_criterion_object(holder, where) -> bool:
    """
    True when `holder` IS a `diversion_criteria[]` entry — {"feature", "reason"} per the
    Group 3 build contract §2(6) — rather than a branch that forgot its destination.

    It matters for the same reason is_provisional_pending_object() does. §2(6) REQUIRES a
    clerk-facing `reason` on every diversion criterion, and the code-less-terminal shape
    check in check_non_reportable_terminals() reads "a `reason` and no destination" as an
    unflagged terminal. A diversion criterion is neither: it is a FEATURE that, when
    ticked, forces the case off the imaging branch and onto the tissue branch. The
    destination belongs to the branch it diverts to, not to the criterion.

    Identified the same deliberately-narrow way as the two predicates below it: the key it
    hangs off AND its shape. A block under `diversion_criteria` with no `feature` is still
    a shape bug worth catching (and check_imaging_terminals() catches it), and an
    unrelated dict carrying a `feature` under some other key is not exempted.
    """
    if not isinstance(holder, dict):
        return False
    last_key = where.rsplit(".", 1)[-1] if where else ""
    last_key = re.sub(r"\[\d+\]$", "", last_key)
    if last_key != "diversion_criteria":
        return False
    return bool(holder.get("feature"))


def is_grade_resolution_leaf(holder, where) -> bool:
    """
    True when `holder` IS a `grade_resolution` outcome — a `values[...]` entry or the
    `unresolved` half (Group 3 build contract §2(4)) — rather than a code-less terminal.

    Contract §2(4) requires every null-grade outcome to carry a `reason` saying why no
    grade was established, which is the whole point of the construct: cIMPACT-NOW update 8
    forbids grading an untested brain-invasive meningioma, and the reason is what stops
    the omission reading as an oversight. A grade outcome resolves a GRADE, not a case, so
    it has no destination and never needed one.

    Narrow in the same two ways: the path it hangs off (grade_resolution.values.* or
    grade_resolution.unresolved) AND its shape (it declares a `grade`).
    """
    if not isinstance(holder, dict) or "grade" not in holder:
        return False
    parts = where.split(".") if where else []
    if len(parts) >= 2 and parts[-1] == "unresolved" and parts[-2] == "grade_resolution":
        return True
    if len(parts) >= 3 and parts[-2] == "values" and parts[-3] == "grade_resolution":
        return True
    return False


def is_behaviour_exclusion_object(holder, where) -> bool:
    """
    True when `holder` IS a `behaviour_exclusion` object (Group 4 build contract §3,
    §8 rule 1, ruling D1) — {"icdo_code", "icdo_behaviour", "icdo_term",
    "group_declares", "reason", "registrar_decision_required"} — rather than a branch
    that forgot its destination.

    A `behaviour_exclusion` IS one of the tool's recognised terminal declarations —
    alongside `non_reportable: true` and `refer_group` — for the case where a real,
    WHO-recognised entity exists but its ICD-O-3.2 behaviour sits outside what this
    ICCC-3 group admits (a ganglioneuroma is 9490/0; Group IV admits behaviour 3 only),
    so there is no code to emit here and no other group to refer it to either (§2.1).
    Its `reason` is clerk-facing by design (app.js excludeBehaviour()/renderOutput()
    renders it), which is exactly the shape check_non_reportable_terminals()'s near-miss
    net is built to catch — "a `reason` and no destination" — so without this predicate
    every `behaviour_exclusion` block in the file reads as a code-less terminal that
    forgot to flag itself.

    This does not weaken anything: a branch carrying BOTH `behaviour_exclusion` and a
    `morphology_code` is already its own FAIL under check_behaviour_exclusion() (the two
    are mutually exclusive destinations there), so exempting the shape here can never
    mask a real code-less terminal. check_behaviour_exclusion() validates the block's
    full six-key shape; this predicate only needs to recognise it well enough not to
    double-flag it — the same deliberately narrow test as the other predicates here: the
    key it hangs off (walk_dicts path ends in "behaviour_exclusion") AND its shape (it
    declares `icdo_code`, the field that anchors it to a real ICD-O-3.2 entity).
    """
    if not isinstance(holder, dict):
        return False
    last_key = where.rsplit(".", 1)[-1] if where else ""
    if last_key != "behaviour_exclusion":
        return False
    return bool(holder.get("icdo_code"))


def is_refer_branch(container) -> bool:
    """
    True when this branch is a CROSS-GROUP REFERRAL terminal — the fourth branch
    destination app.js supports (advance() -> refer()), alongside next_node,
    morphology_code and a non-reportable exclusion.

    The case IS a malignancy, but it is not one this group codes — leukaemic Burkitt
    belongs in Group II as 9687. Emitting a code from THIS group's file would file the
    case under the wrong ICCC-3 group; marking it non_reportable would drop a real
    cancer off the registry altogether. So it emits no code here and names where the
    case belongs. Identified solely by carrying `refer_group`; whether that value is
    well formed is check_refer_terminals()'s business, not this predicate's — a
    malformed refer branch must still be RECOGNISED as one, or it falls through to the
    code-less-terminal check and gets the wrong diagnosis.
    """
    return isinstance(container, dict) and "refer_group" in container


def has_destination(container) -> bool:
    """
    True when a branch resolves to something. The four destinations app.js's advance()
    dispatches on, in its order: a morphology_code, a refer_group, a non_reportable
    exclusion, a next_node.
    """
    if not isinstance(container, dict):
        return False
    return bool(as_code(container.get("morphology_code"))
                or is_refer_branch(container)
                or is_non_reportable(container)
                or container.get("next_node"))


# --------------------------------------------------------------------------------------
# Layer 1 — source of truth parsers (read-only)
# --------------------------------------------------------------------------------------

# A REDCap option header: "9811, 9811 - " — the code, a comma, the SAME code again, a
# dash. Anchored to the start of the fenced block or to whitespace, so a code that is
# embedded in something else is not mistaken for the start of a new option. That anchor
# is load-bearing: the Group 3 file carries a bold-wrapped duplicate,
# `**9381, 9381 - Gliomatosis cerebri, NOS**`, which is deliberately NOT an option header.
OPTION_HEAD_RE = re.compile(r"(?:\A|(?<=\s))(\d+)\s*,\s*\1\s*-\s*")


def _iter_fenced_blocks(text: str):
    """Yield each ``` fenced block of a Layer 1 options file as ONE string."""
    block: list[str] = []
    in_fence = False
    for raw in text.splitlines():
        if raw.lstrip().startswith("```"):
            if in_fence:
                yield "\n".join(block)
                block = []
            in_fence = not in_fence
            continue
        if in_fence:
            block.append(raw)
    if in_fence and block:          # unterminated fence — take what is there
        yield "\n".join(block)


def _parse_option_block(block: str):
    """
    Yield (code, name) for every option in one fenced block, parsed as a single text
    rather than line by line.

    These files are hand-maintained markdown, and the Group 2 file has drifted: three
    option strings have run together onto one physical line or been split across two.

        9814, 9814 - … TEL-AML1 (ETV6-RUNX1) 9815, 9815 - … with hyperdiploidy
        9690, 9690 - Follicular lymphoma, NOS 9691, 9691 - Follicular lymphoma, grade 2
        9732, 9732 - Multiple myeloma 9733,
        9733 - Plasma cell leukemia

    A per-line parser reads the first two as ONE option each with the next option's whole
    text glued onto its name, and never sees 9815 or 9691 at all; the third it reads as an
    option named "Multiple myeloma 9733," plus a stray line it discards. That cost Group 2
    three of its 91 codes and corrupted three more names — and a code with no option string
    is a code the exact-string rule (check_redcap_exact_names) cannot enforce at all, which
    is the one thing this whole layer exists to do.

    Reading the block as one text fixes both shapes at once: the header regex tolerates the
    line break inside "9733,\n9733 - ", and every name simply runs to the next header.

    Two deliberate limits:
      * A name is truncated at the first newline. Only the HEADER may straddle a line
        break; an option string itself is one line. Without this the option before the
        Group 3 bold-wrapped duplicate would swallow it.
      * Only ASCII horizontal whitespace is collapsed. A non-breaking space is part of the
        string the clerk actually sees in REDCap — the Group 7 file has several — and
        normalising it away would manufacture exactly the drift this parser exists to
        detect.
    """
    matches = list(OPTION_HEAD_RE.finditer(block))
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(block)
        raw_name = block[match.end():end].split("\n", 1)[0]
        name = re.sub(r"[ \t\r\f\v]+", " ", raw_name).strip(" \t\r\f\v")
        if name:
            yield match.group(1), name


def parse_redcap_options(layer1: Path):
    """
    Parse RedCap Options/Group N- ….md into {group: {code: {"option": str, "name": str}}}.

    Filenames in that directory are irregular (double spaces, varying case, some groups
    split across two files) — so we glob and read the group number out of the filename.
    Options live inside fenced blocks and are shaped:
        9811, 9811 - B lymphoblastic leukemia/lymphoma, NOS
    but not reliably one per line — see _parse_option_block().
    """
    findings: list[tuple[str, str]] = []
    options: dict[int, dict[str, dict]] = {}
    if layer1 is None or not layer1.exists():
        return options, [(NOTE, "Layer 1 root not found at %s — source-of-truth checks skipped"
                          % layer1)]

    opt_dir = None
    for candidate in sorted(layer1.iterdir()):
        if candidate.is_dir() and candidate.name.lower().replace(" ", "") == "redcapoptions":
            opt_dir = candidate
            break
    if opt_dir is None:
        return options, [(NOTE, "no 'RedCap Options' directory under %s — "
                                "REDCap exact-string check skipped" % layer1)]

    name_re = re.compile(r"^\s*group\s*0*(\d{1,2})\b", re.IGNORECASE)
    files = 0
    for md in sorted(opt_dir.glob("*.md")):
        m = name_re.match(md.name)
        if not m:
            continue
        group = int(m.group(1))
        if not 1 <= group <= 12:
            findings.append((WARN, "REDCap options file %r names group %d (outside 1-12)"
                             % (md.name, group)))
            continue
        files += 1
        bucket = options.setdefault(group, {})
        try:
            text = md.read_text(encoding="utf-8")
        except OSError as exc:
            findings.append((WARN, "could not read %r: %s" % (md.name, exc)))
            continue
        for block in _iter_fenced_blocks(text):
            for code, name in _parse_option_block(block):
                option = "%s - %s" % (code, name)
                rec = bucket.setdefault(code, {"option": option, "name": name,
                                               "names": [], "options": [],
                                               "source": md.name})
                if name not in rec["names"]:
                    rec["names"].append(name)
                    rec["options"].append(option)
    # A code legitimately appears under several subgroup blocks (e.g. 9380 in Group 3),
    # sometimes with a different name each time. That is a Layer 1 fact, not a build
    # problem — record it once per group and accept any variant when matching.
    for group in sorted(options):
        multi = [c for c, r in options[group].items() if len(r["names"]) > 1]
        if multi:
            findings.append((NOTE, "REDCap group %d: %d code(s) are listed under more than "
                                   "one subgroup with differing names; any variant is "
                                   "accepted as an exact match" % (group, len(multi))))
    if files:
        total = sum(len(v) for v in options.values())
        findings.append((OK, "parsed %d REDCap options file(s), %d option strings, "
                             "groups %s" % (files, total,
                                            ",".join(str(g) for g in sorted(options)))))
    else:
        findings.append((NOTE, "no 'Group N…' files found in %s" % opt_dir.name))
    return options, findings


def parse_classification(layer1: Path):
    """
    Parse 'ICCC 2017 Cancer Classification.md' into {group: set(codes)}.

    Best effort: the file is a markdown table of code ranges per subgroup, and it
    contains at least one malformed range ('9805-9C80.9'), which we skip rather than
    guess at. Unparseable tokens are reported as a NOTE, never a failure.
    """
    findings: list[tuple[str, str]] = []
    codes: dict[int, set] = {}
    if layer1 is None or not layer1.exists():
        return codes, findings
    path = layer1 / "ICCC 2017 Cancer Classification.md"
    if not path.exists():
        return codes, [(NOTE, "%s not present — classification cross-check skipped"
                        % path.name)]
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return codes, [(NOTE, "could not read %s: %s" % (path.name, exc))]

    head_re = re.compile(r"^##\s+([IVX]+)\s*:")
    group = None
    unparsed = 0
    for raw in text.splitlines():
        hm = head_re.match(raw)
        if hm:
            group = ROMAN.get(hm.group(1).upper())
            continue
        if group is None or not raw.lstrip().startswith("|"):
            continue
        cells = raw.split("|")
        if len(cells) < 4:
            continue
        cell = cells[2].strip()
        if not cell or cell.lower() == "code" or set(cell) <= set("- :"):
            continue
        for token in cell.split(","):
            token = token.strip()
            if not token:
                continue
            if re.fullmatch(r"\d+", token):
                codes.setdefault(group, set()).add(token)
            else:
                rm = re.fullmatch(r"(\d+)\s*-\s*(\d+)", token)
                if rm and len(rm.group(1)) == len(rm.group(2)):
                    lo, hi = int(rm.group(1)), int(rm.group(2))
                    if lo <= hi and hi - lo <= 2000:
                        width = len(rm.group(1))
                        for n in range(lo, hi + 1):
                            codes.setdefault(group, set()).add(str(n).zfill(width))
                        continue
                    unparsed += 1
                else:
                    unparsed += 1
    if codes:
        findings.append((OK, "parsed ICCC classification table: %d group(s), %d codes"
                         % (len(codes), sum(len(v) for v in codes.values()))))
    if unparsed:
        findings.append((NOTE, "%d malformed code token(s) in the classification table "
                               "were skipped (e.g. '9805-9C80.9')" % unparsed))
    return codes, findings


# --------------------------------------------------------------------------------------
# A. Alias index regeneration
# --------------------------------------------------------------------------------------

def regenerate_alias_index(repo: Path):
    """Rebuild data/aliases/alias_index.json — alias string -> [group numbers]."""
    findings: list[tuple[str, str]] = []
    alias_dir = repo / "data" / "aliases"
    out_path = alias_dir / "alias_index.json"
    index: dict[str, set] = {}

    files = sorted(alias_dir.glob("aliases_group_*.json")) if alias_dir.exists() else []
    if not files:
        findings.append((NOTE, "no data/aliases/aliases_group_*.json found — "
                               "writing an empty alias index"))
    for path in files:
        gm = re.search(r"aliases_group_(\d+)\.json$", path.name)
        if not gm:
            findings.append((WARN, "%s does not match aliases_group_NN.json — skipped"
                             % path.name))
            continue
        group = int(gm.group(1))
        data, load_findings = load_json(path)
        findings.extend(load_findings)
        if data is None:
            continue
        if not 1 <= group <= 12:
            findings.append((FAIL, "%s names group %d (outside 1-12)" % (path.name, group)))
            continue
        entries = data.get("aliases") if isinstance(data, dict) else data
        if not isinstance(entries, list):
            findings.append((FAIL, "%s: expected a list of alias entries (or an "
                                   "'aliases' array)" % path.name))
            continue
        added = 0
        for i, entry in enumerate(entries):
            if not isinstance(entry, dict):
                findings.append((FAIL, "%s[%d] is not an object" % (path.name, i)))
                continue
            alias = entry.get("alias")
            if not isinstance(alias, str) or not alias.strip():
                findings.append((FAIL, "%s[%d] has no usable 'alias' string" % (path.name, i)))
                continue
            index.setdefault(alias.strip(), set()).add(group)
            added += 1
        findings.append((OK, "%s: %d alias(es) indexed" % (path.name, added)))

    payload = {k: sorted(v) for k, v in sorted(index.items())}
    try:
        alias_dir.mkdir(parents=True, exist_ok=True)
        # Lean and deterministic: sorted keys, no gratuitous whitespace (Architecture §4C
        # keeps this file under ~30 KB; it is generated, never hand-edited).
        text = json.dumps(payload, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":")) + "\n"
        out_path.write_text(text, encoding="utf-8")
    except OSError as exc:
        findings.append((FAIL, "could not write alias_index.json: %s" % exc))
        return findings

    size = len(text.encode("utf-8"))
    findings.append((OK, "wrote data/aliases/alias_index.json — %d alias(es), %d bytes"
                     % (len(payload), size)))
    if size > 30 * 1024:
        findings.append((WARN, "alias_index.json is %d bytes (Architecture §4C: keep it "
                               "under ~30 KB)" % size))
    return findings


# --------------------------------------------------------------------------------------
# The decision-tree context — parsed once, shared by every check
# --------------------------------------------------------------------------------------

class DTContext:
    """Normalised view of one group_XX_dt.json."""

    def __init__(self, path: Path, data: dict, group: int) -> None:
        self.path = path
        self.name = path.name
        self.data = data
        self.group = group
        self.shape_findings: list[tuple[str, str]] = []

        self.metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
        raw_entries = data.get("morphology_entries")
        self.entries = raw_entries if isinstance(raw_entries, list) else []

        self.codes: set = set()
        for entry in self.entries:
            if isinstance(entry, dict):
                code = as_code(entry.get("morphology_code"))
                if code:
                    self.codes.add(code)

        self.trees: list[dict] = []          # {tree_id, entry_node, nodes[]}
        self.nodes: dict[str, dict] = {}     # node_id -> node
        self.node_tree: dict[str, str] = {}  # node_id -> tree_id
        self.duplicate_node_ids: list[str] = []
        self._normalise_trees(data.get("decision_trees"))

    # -- tree shape normalisation ---------------------------------------------------
    def _normalise_trees(self, raw) -> None:
        if raw is None:
            self.shape_findings.append((FAIL, "%s: missing top-level 'decision_trees'"
                                        % self.name))
            return
        if isinstance(raw, dict):
            raw = [{"tree_id": k, "nodes": v} for k, v in sorted(raw.items())]
        if not isinstance(raw, list):
            self.shape_findings.append((FAIL, "%s: 'decision_trees' must be an array"
                                        % self.name))
            return
        if raw and all(isinstance(x, dict) and "node_id" in x for x in raw):
            # A bare array of nodes with no tree wrapper.
            self.shape_findings.append((WARN, "%s: 'decision_trees' is a bare node array "
                                              "with no tree objects; treating it as one "
                                              "unnamed tree" % self.name))
            raw = [{"tree_id": "(unnamed)", "nodes": raw}]
        for i, tree in enumerate(raw):
            if not isinstance(tree, dict):
                self.shape_findings.append((FAIL, "%s: decision_trees[%d] is not an object"
                                            % (self.name, i)))
                continue
            tree_id = tree.get("tree_id") or tree.get("id") or "(tree %d)" % i
            nodes = None
            for key in ("nodes", "decision_nodes", "tree_nodes"):
                if isinstance(tree.get(key), list):
                    nodes = tree[key]
                    break
            if nodes is None:
                self.shape_findings.append((FAIL, "%s: tree %r has no 'nodes' array"
                                            % (self.name, tree_id)))
                nodes = []
            entry_node = tree.get("entry_node") or tree.get("entry_node_id")
            self.trees.append({"tree_id": tree_id, "entry_node": entry_node, "nodes": nodes})
            for j, node in enumerate(nodes):
                if not isinstance(node, dict):
                    self.shape_findings.append(
                        (FAIL, "%s: tree %r node index %d is not an object"
                         % (self.name, tree_id, j)))
                    continue
                node_id = node.get("node_id")
                if not isinstance(node_id, str) or not node_id:
                    self.shape_findings.append(
                        (FAIL, "%s: tree %r node index %d has no 'node_id'"
                         % (self.name, tree_id, j)))
                    continue
                if node_id in self.nodes:
                    self.duplicate_node_ids.append(node_id)
                    continue
                self.nodes[node_id] = node
                self.node_tree[node_id] = tree_id

    # -- derived views --------------------------------------------------------------
    @property
    def metadata_tree_ids(self) -> list[str]:
        raw = self.metadata.get("decision_trees")
        if not isinstance(raw, list):
            return []
        out = []
        for item in raw:
            if isinstance(item, str):
                out.append(item)
            elif isinstance(item, dict):
                tid = item.get("tree_id") or item.get("id")
                if isinstance(tid, str):
                    out.append(tid)
        return out

    def entry_nodes(self) -> list[str]:
        out = []
        for tree in self.trees:
            if isinstance(tree["entry_node"], str):
                out.append(tree["entry_node"])
        return out

    def transitions(self):
        """
        Yield (from_node_id, to_node_id, detection_method, where).

        Every `next_node` anywhere inside a node counts: node level, options[],
        resolution_logic[], bands[] and override_when[].  The detection_method label
        (if any) is read off the dict that carries the next_node — that is the option
        the clerk actually clicks.

        `insufficient_next_node` IS ALSO AN EDGE, and was missing here until 2026-09-22.
        app.js's `fallbackTarget()` returns `{next_node: n.insufficient_next_node}` — the
        engine follows it exactly like any other transition, and on an `imaging_pathway`
        it is the ONLY way out that is not the confirmed constellation, so it carries the
        diverted and the incomplete case, which is most of them.

        Leaving it out cost two things, both found on the Group 5 branch:

          * `check_next_node_resolution()` never validated those targets at all. A typo'd
            `insufficient_next_node` resolves to nothing, `fallbackTarget()` throws, and
            the build passed — the same class of runtime crash docs/TODO.md §10 records.
          * `check_orphan_nodes()` could not see the edge, so a node reachable ONLY as an
            insufficient-evidence target was reported as an orphan. That is a FALSE FAIL,
            and it fired on the first correct Group 5 tree.

        The three consumers all treat a transition as "an edge the engine can follow", so
        all three want this edge. `detection_method` is read off the same holder for both
        kinds; a fallback target does not normally carry one, which yields None as before.
        """
        for node_id, node in self.nodes.items():
            for holder, where in walk_dicts(node):
                for key in ("next_node", "insufficient_next_node"):
                    target = holder.get(key)
                    if isinstance(target, str) and target:
                        loc = where or "(node level)"
                        if key != "next_node":
                            loc = "%s %s" % (loc, key)
                        yield (node_id, target, holder.get("detection_method"), loc)

    def emissions(self):
        """Yield (code, holder_dict, node_id, where) for every morphology_code in a node."""
        for node_id, node in self.nodes.items():
            for holder, where in walk_dicts(node):
                code = as_code(holder.get("morphology_code"))
                if code:
                    yield code, holder, node_id, where or "(node level)"


# --------------------------------------------------------------------------------------
# B. Internal checks
# --------------------------------------------------------------------------------------

def check_top_level_keys(ctx: DTContext):
    out = []
    for key in ("metadata", "morphology_entries", "decision_trees"):
        if key not in ctx.data:
            out.append((FAIL, "missing required top-level key %r" % key))
    if not isinstance(ctx.data.get("morphology_entries"), list):
        out.append((FAIL, "'morphology_entries' must be an array"))
    if not isinstance(ctx.data.get("metadata"), dict):
        out.append((FAIL, "'metadata' must be an object"))
    for key in ("group_id", "group_name"):
        if isinstance(ctx.metadata, dict) and key not in ctx.metadata:
            out.append((WARN, "metadata is missing %r" % key))
    gid = ctx.metadata.get("group_id") if isinstance(ctx.metadata, dict) else None
    if gid is not None and str(gid) != str(ctx.group):
        out.append((FAIL, "metadata.group_id is %r but the filename says group %d"
                    % (gid, ctx.group)))
    if not out:
        out.append((OK, "top-level structure { metadata, morphology_entries, decision_trees }"))
    return out


def check_morphology_entry_fields(ctx: DTContext):
    """DT master §2 — every field present; null allowed only where the spec allows it."""
    out = []
    missing_counts: dict[str, int] = {}
    for i, entry in enumerate(ctx.entries):
        if not isinstance(entry, dict):
            out.append((FAIL, "morphology_entries[%d] is not an object" % i))
            continue
        label = as_code(entry.get("morphology_code")) or "index %d" % i
        for field in MORPHOLOGY_FIELDS:
            if field not in entry:
                missing_counts[field] = missing_counts.get(field, 0) + 1
        for field in MORPHOLOGY_NOT_NULL:
            if entry.get(field) in (None, ""):
                out.append((FAIL, "entry %s: %r must not be null" % (label, field)))
        # No longer a required field (registrar ruling, 16 Sep 2026) — Group 4
        # onward carries none. Where a legacy Group 1-3 entry still has it, it
        # must still be a real value; that is the only thing checked here.
        conf = entry.get("confidence_ceiling")
        if conf is not None and conf not in CONFIDENCE_CEILINGS:
            out.append((FAIL, "entry %s: confidence_ceiling %r is not high/medium/low"
                        % (label, conf)))
        tests = entry.get("diagnostic_tests_required")
        if isinstance(tests, list):
            for t in tests:
                if t not in DIAGNOSTIC_TESTS:
                    out.append((WARN, "entry %s: diagnostic_tests_required %r is outside "
                                      "the DT master §2 list" % (label, t)))
        if entry.get("topography_dependent") is True and not entry.get("topography_routing_note"):
            out.append((FAIL, "entry %s: topography_dependent is true but "
                              "topography_routing_note is empty (DT master §2, §6)" % label))
        rv = entry.get("redcap_value")
        code = as_code(entry.get("morphology_code"))
        if rv is not None and code and as_code(rv) != code:
            out.append((WARN, "entry %s: redcap_value %r differs from the morphology code"
                        % (label, rv)))
    for field, n in sorted(missing_counts.items()):
        out.append((FAIL, "field %r absent from %d morphology entr%s (DT master §2 requires "
                          "every field, null where inapplicable)"
                    % (field, n, "y" if n == 1 else "ies")))
    if not out:
        out.append((OK, "%d morphology entries carry every DT master §2 field"
                    % len(ctx.entries)))
    return out


def check_morphology_code_format(ctx: DTContext):
    """
    Digits-only, NO fixed length.

    ICD-O-4 introduces 5-digit codes (DT master §2, data.md §3) — hard-coding a
    4-character check would break the build the day the registry migrates.
    """
    out = []
    for i, entry in enumerate(ctx.entries):
        if not isinstance(entry, dict):
            continue
        raw = entry.get("morphology_code")
        code = as_code(raw)
        if code is None:
            continue
        if not re.fullmatch(r"\d+", code):
            out.append((FAIL, "morphology_entries[%d]: morphology_code %r is not digits-only"
                        % (i, raw)))
        elif not isinstance(raw, str):
            out.append((WARN, "morphology_entries[%d]: morphology_code %r is a number; it "
                              "must be a string (leading zeros are significant)" % (i, raw)))
    for code, _holder, node_id, where in ctx.emissions():
        if not re.fullmatch(r"\d+", code):
            out.append((FAIL, "node %s (%s): morphology_code %r is not digits-only"
                        % (node_id, where, code)))
    if not out:
        out.append((OK, "every morphology_code is digits-only (no fixed length asserted)"))
    return out


def check_behavior_codes(ctx: DTContext):
    out = []
    for i, entry in enumerate(ctx.entries):
        if not isinstance(entry, dict):
            continue
        label = as_code(entry.get("morphology_code")) or "index %d" % i
        beh = entry.get("behavior_code")
        if beh is None or beh == "":
            out.append((FAIL, "entry %s: behavior_code must be explicit (DT master §2)"
                        % label))
            continue
        text = str(beh).strip().lstrip("/")
        if not re.fullmatch(r"[0-6]", text):
            out.append((FAIL, "entry %s: behavior_code %r is not a single ICD-O behaviour "
                              "digit" % (label, beh)))
    if not out:
        out.append((OK, "every morphology entry carries an explicit behavior_code"))
    return out


def check_duplicate_code_behavior_pairs(ctx: DTContext):
    out = []
    seen: dict[tuple, int] = {}
    for i, entry in enumerate(ctx.entries):
        if not isinstance(entry, dict):
            continue
        code = as_code(entry.get("morphology_code"))
        beh = entry.get("behavior_code")
        if code is None or beh is None:
            continue
        key = (code, str(beh).strip().lstrip("/"))
        if key in seen:
            out.append((FAIL, "duplicate (morphology_code, behavior_code) pair %s/%s at "
                              "entries %d and %d" % (key[0], key[1], seen[key], i)))
        else:
            seen[key] = i
    if not out:
        out.append((OK, "no duplicate (morphology_code, behavior_code) pairs"))
    return out


def check_fallback_chains(ctx: DTContext):
    """Every nos_fallback_code exists; chains terminate; no cycles (data.md §3)."""
    out = []
    nxt: dict[str, str] = {}
    for entry in ctx.entries:
        if not isinstance(entry, dict):
            continue
        code = as_code(entry.get("morphology_code"))
        fb = as_code(entry.get("nos_fallback_code"))
        if code is None:
            continue
        if fb is None:
            continue
        if fb not in ctx.codes:
            out.append((FAIL, "entry %s: nos_fallback_code %s is not in morphology_entries[]"
                        % (code, fb)))
            continue
        if fb == code:
            out.append((FAIL, "entry %s: nos_fallback_code points at itself" % code))
            continue
        nxt[code] = fb
    reported: set = set()
    for start in sorted(nxt):
        seen: list[str] = []
        cur = start
        while cur in nxt:
            if cur in seen:
                cycle = seen[seen.index(cur):] + [cur]
                key = tuple(sorted(set(cycle)))
                if key not in reported:
                    reported.add(key)
                    out.append((FAIL, "NOS fallback cycle: %s" % " -> ".join(cycle)))
                break
            seen.append(cur)
            cur = nxt[cur]
            if len(seen) > len(nxt) + 2:
                out.append((FAIL, "NOS fallback chain from %s does not terminate" % start))
                break
    if not out:
        out.append((OK, "every nos_fallback_code resolves; all fallback chains terminate "
                        "with no cycles"))
    return out


def check_next_node_resolution(ctx: DTContext):
    """Every next_node, wherever it appears, resolves to a node_id in the same file."""
    out = []
    count = 0
    for src, target, _dm, where in ctx.transitions():
        count += 1
        if target not in ctx.nodes:
            out.append((FAIL, "node %s (%s): next_node %r does not resolve to any node_id "
                              "in this file" % (src, where, target)))
    if not out:
        out.append((OK, "%d next_node reference(s) all resolve in-file "
                        "(cross-tree links are legal)" % count))
    return out


def check_terminal_codes_exist(ctx: DTContext):
    """Every terminal morphology_code and every nos_fallback.code is a real entry."""
    out = []
    n_terminals = n_fallbacks = 0
    for code, _holder, node_id, where in ctx.emissions():
        n_terminals += 1
        if code not in ctx.codes:
            out.append((FAIL, "node %s (%s): terminal morphology_code %s is not in "
                              "morphology_entries[]" % (node_id, where, code)))
    for node_id, node in ctx.nodes.items():
        for holder, where in walk_dicts(node):
            fb = holder.get("nos_fallback")
            if isinstance(fb, dict):
                n_fallbacks += 1
                code = as_code(fb.get("code"))
                if code is None:
                    out.append((FAIL, "node %s (%s): nos_fallback has no 'code'"
                                % (node_id, where or "(node level)")))
                elif code not in ctx.codes:
                    out.append((FAIL, "node %s (%s): nos_fallback.code %s is not in "
                                      "morphology_entries[]"
                                % (node_id, where or "(node level)", code)))
    if not out:
        out.append((OK, "%d terminal code(s) and %d nos_fallback code(s) all exist in "
                        "morphology_entries[]" % (n_terminals, n_fallbacks)))
    return out


def check_node_types(ctx: DTContext):
    out = []
    for node_id, node in sorted(ctx.nodes.items()):
        nt = node.get("node_type")
        if nt is None:
            out.append((FAIL, "node %s has no 'node_type'" % node_id))
        elif nt not in NODE_TYPES:
            out.append((FAIL, "node %s: node_type %r is not in the closed vocabulary "
                              "(DT master §3A + numeric_gate)" % (node_id, nt)))
        elif nt in ROUTER_ONLY_TYPES:
            out.append((FAIL, "node %s: node_type %r is router-tier and belongs in "
                              "presentation_router.json, never in a group dt.json "
                              "(DT master §3B)" % (node_id, nt)))
    if not out:
        out.append((OK, "all %d node_type values are in the closed vocabulary"
                    % len(ctx.nodes)))
    return out


def check_nos_fallback_by_node_type(ctx: DTContext):
    """DT master §3D / nodes.md §2 — a node-type rule, not a step-number rule."""
    out = []
    for node_id, node in sorted(ctx.nodes.items()):
        nt = node.get("node_type")
        fb = node.get("nos_fallback", "__absent__")
        present = isinstance(fb, dict)
        if nt in NOS_REQUIRED_TYPES:
            if is_non_reportable(node):
                if present:
                    out.append((FAIL, "node %s is a non-reportable terminal but carries a "
                                      "nos_fallback (nodes.md §4)" % node_id))
                continue
            if not present:
                out.append((FAIL, "node %s (%s): nos_fallback must be non-null for a "
                                  "refining node type (DT master §3D)" % (node_id, nt)))
        elif nt in NOS_FORBIDDEN_TYPES:
            if present:
                out.append((FAIL, "node %s (%s): nos_fallback must be null for an "
                                  "entry/gate/terminal-NOS node type (DT master §3D)"
                            % (node_id, nt)))
            elif fb == "__absent__":
                out.append((WARN, "node %s (%s): 'nos_fallback' key absent; the schema "
                                  "wants an explicit null" % (node_id, nt)))
    if not out:
        out.append((OK, "nos_fallback presence matches the node-type rule on every node"))
    return out


def check_captured_variables_declared(ctx: DTContext):
    """
    Every variable named in a resolution_logic[].when or an override_when[].captured_variable
    is declared in that node's captured_variables[].
    """
    out = []
    checked = 0
    for node_id, node in sorted(ctx.nodes.items()):
        declared = node.get("captured_variables")
        declared = set(declared) if isinstance(declared, list) else set()
        used: set = set()
        for rule in node.get("resolution_logic") or []:
            if isinstance(rule, dict) and isinstance(rule.get("when"), dict):
                used |= set(rule["when"].keys())
        for ov in node.get("override_when") or []:
            if isinstance(ov, dict) and isinstance(ov.get("captured_variable"), str):
                used.add(ov["captured_variable"])
        for band in node.get("bands") or []:
            if isinstance(band, dict) and isinstance(band.get("when"), dict):
                used |= set(band["when"].keys())
        checked += len(used)
        for var in sorted(used - declared):
            out.append((FAIL, "node %s: variable %r is used but not declared in "
                              "captured_variables[]" % (node_id, var)))
        gate_var = node.get("variable")
        if (node.get("node_type") == "numeric_gate" and isinstance(gate_var, str)
                and gate_var not in declared):
            out.append((WARN, "node %s: numeric_gate 'variable' %r is not declared in "
                              "captured_variables[]" % (node_id, gate_var)))
    if not out:
        out.append((OK, "%d captured-variable reference(s) all declared on their node"
                    % checked))
    return out


def check_metadata_counts(ctx: DTContext):
    out = []
    n_entries = len(ctx.entries)
    n_nodes = sum(len(t["nodes"]) for t in ctx.trees)
    meta_entries = ctx.metadata.get("total_morphology_entries")
    meta_nodes = ctx.metadata.get("total_decision_nodes")
    if meta_entries is None:
        out.append((FAIL, "metadata.total_morphology_entries is missing"))
    elif int(meta_entries) != n_entries:
        out.append((FAIL, "metadata.total_morphology_entries is %s but the file holds %d"
                    % (meta_entries, n_entries)))
    if meta_nodes is None:
        out.append((FAIL, "metadata.total_decision_nodes is missing"))
    elif int(meta_nodes) != n_nodes:
        out.append((FAIL, "metadata.total_decision_nodes is %s but the file holds %d"
                    % (meta_nodes, n_nodes)))
    listed = ctx.metadata_tree_ids
    present = [t["tree_id"] for t in ctx.trees]
    missing = sorted(set(listed) - set(present))   # declared, not yet authored
    extra = sorted(set(present) - set(listed))     # authored, but not declared
    if missing:
        # Declared ahead of authoring is the documented in-progress state (Group 1
        # Pathway §7.6: the validator runs after EACH tree is authored, so a group's
        # later trees are legitimately still missing) — the same leniency the
        # presentation_router.json tree_id check already grants via its union of
        # metadata_tree_ids and present trees.
        out.append((NOTE, "metadata.decision_trees declares %d tree(s) not yet authored: %s"
                    % (len(missing), ", ".join(missing))))
    if extra:
        out.append((FAIL, "metadata.decision_trees does not match the trees present "
                          "(present but unlisted: %s)" % ", ".join(extra)))
    if not out:
        out.append((OK, "metadata counts match: %d entries, %d nodes, %d tree(s)"
                    % (n_entries, n_nodes, len(ctx.trees))))
    return out


def check_node_ids_unique_and_prefixed(ctx: DTContext):
    """
    Node IDs are globally unique across trees, and each tree's nodes carry that tree's
    prefix (Group 1: ac_ / ml_ / mpn_ / mds_ — data.md §4, Pathway §7.1).

    The prefix is derived from the tree's own entry_node rather than hard-coded, so the
    rule generalises to every group.
    """
    out = []
    for dup in sorted(set(ctx.duplicate_node_ids)):
        out.append((FAIL, "node_id %r is declared more than once — IDs must be globally "
                          "unique across all trees in the file" % dup))
    prefixes: dict[str, str] = {}
    for tree in ctx.trees:
        entry = tree["entry_node"]
        tid = tree["tree_id"]
        if not isinstance(entry, str) or "_" not in entry:
            out.append((WARN, "tree %r has no entry_node with a '<prefix>_' shape; the "
                              "node-prefix check is skipped for this tree" % tid))
            continue
        prefix = entry.split("_", 1)[0] + "_"
        if prefix in prefixes:
            out.append((FAIL, "trees %r and %r share the node prefix %r"
                        % (prefixes[prefix], tid, prefix)))
        prefixes[prefix] = tid
        for node in tree["nodes"]:
            if not isinstance(node, dict):
                continue
            nid = node.get("node_id")
            if isinstance(nid, str) and not nid.startswith(prefix):
                out.append((FAIL, "node %s belongs to tree %r but does not carry that "
                                  "tree's prefix %r" % (nid, tid, prefix)))
    if not out:
        out.append((OK, "%d node_id(s) globally unique and correctly tree-prefixed"
                    % len(ctx.nodes)))
    return out


def check_orphan_nodes(ctx: DTContext):
    """No node unreachable from a tree entry node (cross-tree next_node is legal)."""
    out = []
    roots = [e for e in ctx.entry_nodes() if e in ctx.nodes]
    for tree in ctx.trees:
        entry = tree["entry_node"]
        if entry is None:
            out.append((FAIL, "tree %r declares no entry_node" % tree["tree_id"]))
        elif entry not in ctx.nodes:
            out.append((FAIL, "tree %r: entry_node %r does not resolve to a node in this "
                              "file" % (tree["tree_id"], entry)))
    if not roots:
        if ctx.nodes:
            out.append((FAIL, "no usable tree entry node — every node is unreachable"))
        return out or [(OK, "no trees authored yet")]
    adj: dict[str, set] = {}
    for src, target, _dm, _w in ctx.transitions():
        adj.setdefault(src, set()).add(target)
    seen = set(roots)
    stack = list(roots)
    while stack:
        cur = stack.pop()
        for nxt in adj.get(cur, ()):
            if nxt in ctx.nodes and nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    orphans = sorted(set(ctx.nodes) - seen)
    for o in orphans:
        out.append((FAIL, "orphan node %s is unreachable from any tree entry node" % o))
    if not out:
        out.append((OK, "all %d node(s) reachable from a tree entry node" % len(ctx.nodes)))
    return out


def check_non_reportable_terminals(ctx: DTContext):
    """
    A node or option marked 'not a reportable malignancy' must emit no morphology code
    and must have no NOS fallback wired to it (nodes.md §4, Pathway §7.5).
    """
    out = []
    found = 0
    for node_id, node in sorted(ctx.nodes.items()):
        for holder, where in walk_dicts(node):
            if not is_non_reportable(holder):
                continue
            found += 1
            label = "%s (%s)" % (node_id, where or "(node level)")
            if as_code(holder.get("morphology_code")):
                out.append((FAIL, "non-reportable terminal %s emits morphology_code %s — a "
                                  "non-reportable terminal must emit no malignant code"
                            % (label, as_code(holder.get("morphology_code")))))
            if isinstance(holder.get("nos_fallback"), dict):
                out.append((FAIL, "non-reportable terminal %s has a nos_fallback wired to "
                                  "it — that would record a cancer that does not exist"
                            % label))
            if as_code(holder.get("nos_fallback_code")):
                out.append((FAIL, "non-reportable terminal %s carries a nos_fallback_code"
                            % label))
    # A near-miss spelling makes is_non_reportable() return False, so the checks above
    # never run and the terminal passes silently — the check fails OPEN. Catch the shape
    # instead: a branch that names a reason but goes nowhere is a terminal, and the only
    # kind of terminal that emits no code is a non-reportable one.
    for node_id, node in sorted(ctx.nodes.items()):
        for holder, where in walk_dicts(node):
            if is_non_reportable(holder) or not isinstance(holder, dict):
                continue
            if is_nos_fallback_object(holder, where):
                # A nos_fallback object is {"code", "reason"} by design (DT master
                # §3C/§3D; "name" is a Groups 1-3 convention, not part of the schema —
                # see is_nos_fallback_object()) — a reason with no next_node/
                # morphology_code of its own is exactly its documented shape, not a
                # code-less terminal.
                continue
            if is_provisional_pending_object(holder, where):
                # A provisional_pending object is {"reason", "resolving_test", …} by
                # design (Group II contract §3.2). Its `reason` is clerk-facing text
                # ABOUT the code its branch emits; the branch carries the destination.
                continue
            if is_diversion_criterion_object(holder, where):
                # A diversion criterion is a FEATURE that forces the tissue branch, not a
                # terminal (Group 3 contract §2(6)). Its `reason` explains the diversion;
                # the branch it diverts to carries the destination.
                continue
            if is_grade_resolution_leaf(holder, where):
                # A grade_resolution outcome resolves a GRADE, not a case (Group 3
                # contract §2(4)). Its `reason` says why no grade was established.
                continue
            if is_behaviour_exclusion_object(holder, where):
                # A behaviour_exclusion block IS the recognised declaration that this
                # branch emits no code (Group 4 contract §3, ruling D1) — a real,
                # WHO-recognised entity whose behaviour sits outside what this group
                # admits, alongside non_reportable and refer_group. Its `reason` is
                # clerk-facing BY DESIGN (app.js excludeBehaviour()/renderOutput());
                # its own six-key shape is validated in full by
                # check_behaviour_exclusion(), including that it never also carries a
                # morphology_code, so this exemption can never mask a real code-less
                # terminal.
                continue
            if not holder.get("reason"):
                continue
            if is_refer_branch(holder):
                # A cross-group referral is a destination — it names another ICCC-3
                # group rather than a node or a code. A `reason` on one is its
                # DOCUMENTED shape (app.js refer() renders it as the "Why" row), not a
                # code-less terminal that forgot to flag itself. Its own rules are
                # enforced by check_refer_terminals().
                continue
            if as_code(holder.get("morphology_code")) or holder.get("next_node"):
                continue
            suspect = sorted(k for k in holder
                             if "report" in k.lower() or k in ("terminal_type", "outcome",
                                                               "terminal_kind", "result_type"))
            out.append((FAIL, "%s (%s) carries a 'reason' but no destination and no "
                              "recognised non-reportable flag%s — if this is the clean "
                              "'not a reportable malignancy' terminal it must say so with "
                              "\"non_reportable\": true; if it belongs to another ICCC-3 "
                              "group it must say so with \"refer_group\"; otherwise its "
                              "emit-no-code rule is never checked"
                        % (node_id, where or "(node level)",
                           (" (saw %s)" % ", ".join(suspect)) if suspect else "")))

    if not out:
        out.append((OK, "%d non-reportable terminal(s) emit no morphology code; no "
                        "unflagged code-less terminals" % found))
    return out


def check_refer_terminals(ctx: DTContext):
    """
    The CROSS-GROUP REFERRAL terminal — app.js's fourth branch destination (advance()
    -> refer()), previously unknown to this script.

    The case is a malignancy that this group does not code: leukaemic Burkitt is
    9687/3 in Group II, nodal-dominant CLL/SLL is 9823 but in IIb2, and so on. The
    branch emits NO code from this file and names the group the case belongs to.

    Two other checks used to misfire on this shape, because a refer branch is a
    terminal that carries an explanation and emits nothing:

      * check_non_reportable_terminals flagged "carries a 'reason' but no destination
        and no non_reportable flag" — the description of a refer branch exactly;
      * check_numeric_gate_shape demanded next_node / morphology_code / non_reportable
        on every band.

    Both now recognise refer_group as a destination, so the explanation can live in
    `reason` where the schema says it belongs (it had been displaced into coding_note
    purely to dodge the first check).

    The rules enforced here:
      * refer_group must be an INTEGER in 1..12 — it is an ICCC-3 group number, and
        app.js looks it up in the router's groups table by string key. A float, a
        numeric string or 0/13 all render a broken referral panel. bool is rejected
        explicitly: it is an int subclass in Python and True would otherwise pass as
        group 1.
      * NO morphology_code. advance() tests morphology_code BEFORE refer_group, so a
        refer branch carrying one silently emits this group's code and never refers —
        the referral is dead data and the case is filed in the wrong group. FAIL.
      * a `reason` SHOULD be present — it is the "Why" row the clerk reads. app.js
        falls back to coding_note, so its absence is a WARN, not a FAIL.
      * refer_code, where present, must be digits-only (same shape as a
        morphology_code; it is one, in the other group's file).
      * refer_code must NOT be a code this group's morphology_entries[] already owns.
        Referring a case away to a code sitting in this very file is normally a routing
        error: either the branch should have emitted it here, or the code does not
        belong in this group's entry list. FAIL.

        ONE exemption, and it is not a loophole — it is the DUAL-GROUP rule (DT master
        §6). 9823, 9827 and 9591 are legitimately codeable in BOTH Group I and Group II;
        which group applies is decided by compartment or topography, not by the code.
        Nodal-dominant CLL/SLL really is 9823 in IIb2 while leukaemic CLL is 9823 in
        Ia2. Such an entry declares itself with `topography_dependent: true` and spells
        the split out in `topography_routing_note`, so the referral is checkable rather
        than merely asserted: the exemption applies ONLY when the owning entry carries
        that flag. A refer_code owned by an entry that does NOT declare itself
        topography-dependent stays a FAIL — that is the real routing error.
    """
    out = []
    refers = 0
    dual = 0
    for node_id, node in sorted(ctx.nodes.items()):
        for holder, where in walk_dicts(node):
            if not is_refer_branch(holder):
                continue
            refers += 1
            label = "%s (%s)" % (node_id, where or "(node level)")
            grp = holder.get("refer_group")
            if isinstance(grp, bool) or not isinstance(grp, int):
                out.append((FAIL, "refer terminal %s: refer_group must be an integer "
                                  "ICCC-3 group number, got %r" % (label, grp)))
            elif not 1 <= grp <= 12:
                out.append((FAIL, "refer terminal %s: refer_group %d is outside the "
                                  "ICCC-3 range 1-12" % (label, grp)))
            elif grp == ctx.group:
                out.append((FAIL, "refer terminal %s: refer_group %d is this group — a "
                                  "referral must name a DIFFERENT group, or the branch "
                                  "should emit a code here" % (label, grp)))

            code = as_code(holder.get("morphology_code"))
            if code:
                out.append((FAIL, "refer terminal %s carries morphology_code %s — app.js "
                                  "advance() tests morphology_code before refer_group, so "
                                  "this emits a group %d code and never refers; the case "
                                  "would be filed in the wrong ICCC-3 group"
                            % (label, code, ctx.group)))

            if not holder.get("reason"):
                out.append((WARN, "refer terminal %s carries no 'reason' — the clerk sees "
                                  "no explanation for why the case leaves this group "
                                  "(app.js falls back to coding_note)" % label))

            if "refer_code" in holder:
                rc = holder.get("refer_code")
                rcs = as_code(rc)
                if not isinstance(rc, str) or not rcs or not rcs.isdigit():
                    out.append((FAIL, "refer terminal %s: refer_code must be a digits-only "
                                      "string, got %r" % (label, rc)))
                elif rcs in ctx.codes:
                    owner = next((e for e in ctx.entries
                                  if isinstance(e, dict)
                                  and as_code(e.get("morphology_code")) == rcs), None)
                    if owner is not None and owner.get("topography_dependent") is True:
                        dual += 1
                        if not owner.get("topography_routing_note"):
                            out.append((WARN, "refer terminal %s refers to dual-group code "
                                              "%s, but that entry declares "
                                              "topography_dependent without a "
                                              "topography_routing_note saying where the "
                                              "split falls" % (label, rcs)))
                    else:
                        out.append((FAIL, "refer terminal %s refers to code %s, but %s is "
                                          "in this group's morphology_entries[] and that "
                                          "entry is NOT declared topography_dependent — "
                                          "referring a case to a code this group already "
                                          "owns outright is a routing error"
                                    % (label, rcs, rcs)))
    if dual:
        out.append((NOTE, "%d referral(s) name a code this file also carries; each owning "
                          "entry declares topography_dependent, so this is the dual-group "
                          "rule (DT master §6), not a routing error" % dual))
    if not any(level == FAIL for level, _ in out):
        out.append((OK, "%d cross-group referral terminal(s) well formed: group in 1-12 "
                        "and not this group, no morphology_code, refer_code digits-only "
                        "and not owned outright here" % refers))
    return out


# --------------------------------------------------------------------------------------
# B2. Group 1 schema extensions (Pathway §7.3) — shape validation
# --------------------------------------------------------------------------------------

def check_numeric_gate_shape(ctx: DTContext):
    out = []
    gates = 0
    for node_id, node in sorted(ctx.nodes.items()):
        if node.get("node_type") != "numeric_gate":
            continue
        gates += 1
        if not isinstance(node.get("variable"), str) or not node["variable"]:
            out.append((FAIL, "numeric_gate %s: 'variable' is required" % node_id))
        if "unit" in node and node["unit"] is not None and not isinstance(node["unit"], str):
            out.append((FAIL, "numeric_gate %s: optional 'unit' must be a string" % node_id))
        bands = node.get("bands")
        if not isinstance(bands, list) or not bands:
            out.append((FAIL, "numeric_gate %s: 'bands[]' is required and must be non-empty"
                        % node_id))
            bands = []
        for i, band in enumerate(bands):
            if not isinstance(band, dict):
                out.append((FAIL, "numeric_gate %s: bands[%d] is not an object"
                            % (node_id, i)))
                continue
            if not isinstance(band.get("range"), str) or not band["range"]:
                out.append((FAIL, "numeric_gate %s: bands[%d] has no 'range'" % (node_id, i)))
            # Four destinations, matching app.js advance(): next_node, morphology_code,
            # a non-reportable exclusion, or a cross-group referral.
            if not has_destination(band):
                out.append((FAIL, "numeric_gate %s: bands[%d] (%r) has no destination — "
                                  "it needs a next_node, a morphology_code, "
                                  "\"non_reportable\": true or a refer_group"
                            % (node_id, i, band.get("range"))))
        ovs = node.get("override_when")
        if ovs is not None and not isinstance(ovs, list):
            out.append((FAIL, "numeric_gate %s: optional 'override_when' must be an array"
                        % node_id))
            ovs = []
        for i, ov in enumerate(ovs or []):
            if not isinstance(ov, dict):
                out.append((FAIL, "numeric_gate %s: override_when[%d] is not an object"
                            % (node_id, i)))
                continue
            if not isinstance(ov.get("captured_variable"), str) or not ov["captured_variable"]:
                out.append((FAIL, "numeric_gate %s: override_when[%d] has no "
                                  "'captured_variable'" % (node_id, i)))
            if "equals" not in ov:
                out.append((FAIL, "numeric_gate %s: override_when[%d] has no 'equals'"
                            % (node_id, i)))
            if not has_destination(ov):
                out.append((FAIL, "numeric_gate %s: override_when[%d] has no destination — "
                                  "it needs a next_node, a morphology_code, "
                                  "\"non_reportable\": true or a refer_group"
                            % (node_id, i)))
    if not out:
        out.append((OK, "%d numeric_gate node(s) well formed (Pathway §7.3 item 1)" % gates))
    return out


def _marker_name(token: str):
    """
    Split a positive[]/negative[] token into (name, intensity).

    A token is a marker NAME unless it ends in exactly ':strong' or ':weak', in which case
    the name is everything before that suffix. It must not be split on the first colon:
    '::' is the current fusion-gene separator and this project uses it throughout
    (ETV6::RUNX1, BCR::ABL1, NPM1::ALK), and findings are written as prose
    ('NPM1::ALK t(2;5) by FISH or RT-PCR'). Splitting on every colon read that as marker
    'NPM1' with intensity ':ALK…', which made a permanent tax on correct authoring out of
    a punctuation choice the whole project has already made.
    """
    for suffix in MARKER_INTENSITIES:
        tail = ":" + suffix
        if token.endswith(tail):
            return token[:-len(tail)], suffix
    return token, None


def check_marker_intensity_tokens(ctx: DTContext):
    """
    positive[]/negative[] tokens are "MARKER" or "MARKER:strong" / "MARKER:weak"
    (Pathway §7.3 item 2).

    This is now only a SHAPE check — tokens are strings, and a token that is nothing but
    an intensity suffix has no marker at all. It deliberately does not police colons
    anywhere else in a token, because a fusion name legitimately contains them.

    That leaves a hole on its own: with the suffix rule relaxed, a typo like 'CD30:stong'
    is simply read as a marker NAME, matches nothing, and the rule silently never fires —
    a dead rule with no signal. check_marker_tokens_declared() closes it by requiring every
    token to name a marker the node itself declares, which is a far stronger guard and
    makes the typo loud instead of silent. The two are meant to be read together.
    """
    out = []
    tokens = 0
    intensities = 0
    for node_id, node in sorted(ctx.nodes.items()):
        for holder, where in walk_dicts(node):
            for field in ("positive", "negative"):
                values = holder.get(field)
                if not isinstance(values, list):
                    continue
                for token in values:
                    if not isinstance(token, str):
                        out.append((FAIL, "node %s (%s): %s[] token %r is not a string"
                                    % (node_id, where or "(node level)", field, token)))
                        continue
                    tokens += 1
                    name, intensity = _marker_name(token)
                    if intensity is not None:
                        intensities += 1
                        if not name.strip():
                            out.append((FAIL, "node %s (%s): %s[] token %r carries an "
                                              "intensity suffix but names no marker "
                                              "(Pathway §7.3 item 2)"
                                        % (node_id, where or "(node level)", field, token)))
    if not out:
        out.append((OK, "%d marker token(s) well formed; %d carry an intensity suffix, and "
                        "a colon anywhere else in a token is a fusion name, not a suffix"
                    % (tokens, intensities)))
    return out


def check_marker_tokens_declared(ctx: DTContext):
    """
    Every positive[]/negative[] token names a marker the node itself declares in
    `marker_groups[].markers`.

    This is the guard that makes a mistyped marker LOUD. app.js matches a token against
    what the clerk ticked, so a token nothing can produce is not an error — it is a rule
    that quietly never fires, with no warning, no wrong screen and no failed build. Once
    the intensity-suffix rule is relaxed enough to allow fusion names (see
    check_marker_intensity_tokens), a typo is indistinguishable from an unusual but valid
    marker name UNLESS it is checked against the node's own declared panel. Then it is a
    one-line FAIL naming the token.

    Keyed off the node's own structure, never off a flag: the node declares the panel it
    offers, and the rules on that node may only speak about that panel.

    The real defect this caught on first run: `g2_tfh` carried "Only 1 TFH marker positive"
    in a positive[] with no such marker declared, so the rule was dead — and it is the rule
    that stops a single TFH marker being read as the ≥2 that re-routes a case out of 9702
    into 9705.

    A node carrying tokens but declaring NO marker_groups[] at all is a WARN rather than a
    FAIL: every one of its tokens is unverifiable, which is the same hole, but it is a
    different authoring shape and neither built file contains one. --strict promotes it.
    """
    out = []
    checked = 0
    undeclared_nodes = 0
    for node_id, node in sorted(ctx.nodes.items()):
        declared = set()
        groups = node.get("marker_groups")
        if isinstance(groups, list):
            for group in groups:
                if not isinstance(group, dict):
                    continue
                markers = group.get("markers")
                if isinstance(markers, list):
                    declared.update(m for m in markers if isinstance(m, str))

        node_tokens = []
        for holder, where in walk_dicts(node):
            for field in ("positive", "negative"):
                values = holder.get(field)
                if not isinstance(values, list):
                    continue
                for token in values:
                    if isinstance(token, str):
                        node_tokens.append((token, field, where or "(node level)"))

        if not node_tokens:
            continue
        if not declared:
            undeclared_nodes += 1
            out.append((WARN, "node %s carries %d marker token(s) but declares no "
                              "marker_groups[].markers — there is nothing to check them "
                              "against, so a typo in any of them is a rule that silently "
                              "never fires" % (node_id, len(node_tokens))))
            continue

        for token, field, where in node_tokens:
            checked += 1
            name, _intensity = _marker_name(token)
            if name not in declared:
                out.append((FAIL, "node %s (%s): %s[] token %r names %r, which this node "
                                  "does not declare in marker_groups[].markers. app.js "
                                  "matches tokens against what the clerk ticked, so a "
                                  "marker the node never offers can never match — the rule "
                                  "is dead, and nothing on screen or in the build says so. "
                                  "Either declare the marker or fix the token."
                            % (node_id, where, field, token, name)))

    if not [f for f in out if f[0] == FAIL]:
        out.append((OK, "%d marker token(s) all name a marker declared in their own node's "
                        "marker_groups[]" % checked))
    return out


def check_detection_method(ctx: DTContext):
    out = []
    seen = 0
    for node_id, node in sorted(ctx.nodes.items()):
        is_cyto = node.get("node_type") == "cytogenetics_dropdown"
        for holder, where in walk_dicts(node):
            if "detection_method" not in holder:
                continue
            seen += 1
            dm = holder.get("detection_method")
            if dm not in DETECTION_METHODS:
                out.append((FAIL, "node %s (%s): detection_method %r is not one of %s "
                                  "(Pathway §7.3 item 4)"
                            % (node_id, where or "(node level)", dm,
                               ", ".join(sorted(DETECTION_METHODS)))))
            elif not is_cyto:
                out.append((WARN, "node %s (%s) is a %s, not a cytogenetics_dropdown, but "
                                  "carries detection_method"
                            % (node_id, where or "(node level)", node.get("node_type"))))
    if not out:
        out.append((OK, "%d detection_method value(s) all in the ratified vocabulary" % seen))
    return out


def check_classification_system(ctx: DTContext):
    out = []
    seen = 0
    for node_id, node in sorted(ctx.nodes.items()):
        for holder, where in walk_dicts(node):
            if "classification_system" not in holder:
                continue
            cs = holder.get("classification_system")
            if cs is None:
                continue
            seen += 1
            if cs not in CLASSIFICATION_SYSTEMS:
                out.append((FAIL, "node %s (%s): classification_system %r must be "
                                  "'WHO-HAEM5' or 'ICC-2022' (Pathway §7.3 item 8)"
                            % (node_id, where or "(node level)", cs)))
    for entry in ctx.entries:
        if isinstance(entry, dict) and entry.get("classification_system") is not None:
            seen += 1
            if entry["classification_system"] not in CLASSIFICATION_SYSTEMS:
                out.append((FAIL, "entry %s: classification_system %r must be 'WHO-HAEM5' "
                                  "or 'ICC-2022'" % (as_code(entry.get("morphology_code")),
                                                     entry["classification_system"])))
    if not out:
        out.append((OK, "%d classification_system value(s) valid" % seen))
    return out


def check_outstanding_tests(ctx: DTContext):
    """
    `outstanding_tests[]` is the reverse of `satisfies_tests[]`: app.js ADDS each value
    to the outstanding-workup rows of the code a branch emits. Added for Group 7,
    3 October 2026, so that a branch reaching a code on a partial panel (INI1 retained,
    SMARCA4 never done) shows the skipped test as owed instead of "Complete — no
    outstanding tests". The same two silent failures as satisfies_tests apply: a value
    outside the closed vocabulary still renders, as a row no REDCap workup field can
    hold; and a branch that emits no code never reaches finish(), so the field is inert.
    A test listed in both fields contradicts itself; app.js shows it owed.
    """
    out, seen = [], 0
    for node_id, node in sorted(ctx.nodes.items()):
        for holder, where in walk_dicts(node):
            if "outstanding_tests" not in holder:
                continue
            ot = holder.get("outstanding_tests")
            loc = "node %s (%s)" % (node_id, where or "(node level)")
            if not isinstance(ot, list) or not ot or not all(isinstance(v, str) for v in ot):
                out.append((FAIL, "%s: outstanding_tests must be a non-empty list of strings, "
                                  "got %r" % (loc, ot)))
                continue
            if not as_code(holder.get("morphology_code")):
                out.append((FAIL, "%s: outstanding_tests on a branch that emits no "
                                  "morphology_code — app.js applies it only in finish(), so it "
                                  "is silently inert here" % loc))
                continue
            seen += 1
            for value in ot:
                if value not in DIAGNOSTIC_TESTS:
                    out.append((FAIL, "%s: outstanding_tests value %r is not in the closed "
                                      "diagnostic-test vocabulary" % (loc, value)))
            both = set(ot) & set(holder.get("satisfies_tests") or [])
            if both:
                out.append((FAIL, "%s: %s listed in both satisfies_tests and outstanding_tests"
                            % (loc, ", ".join(sorted(both)))))
    if seen and not [f for f in out if f[0] == FAIL]:
        out.append((OK, "%d outstanding_tests declaration(s): all values in the closed "
                        "vocabulary, all on code-emitting terminals, none also satisfied" % seen))
    return out


def check_non_reportable_heading(ctx: DTContext):
    """
    `non_reportable_heading` replaces the generic "Not a reportable malignancy" banner on a
    non-reportable terminal. app.js reads it only in exclude(), so on any other branch it
    is silently inert; and an empty string would fall back without saying so.
    """
    out, seen = [], 0
    for node_id, node in sorted(ctx.nodes.items()):
        for holder, where in walk_dicts(node):
            if "non_reportable_heading" not in holder:
                continue
            seen += 1
            value = holder.get("non_reportable_heading")
            loc = "node %s (%s)" % (node_id, where or "(node level)")
            if holder.get("non_reportable") is not True:
                out.append((FAIL, "%s: non_reportable_heading on a branch that is not "
                                  "non_reportable — app.js never reads it there" % loc))
            if not isinstance(value, str) or not value.strip():
                out.append((FAIL, "%s: non_reportable_heading must be a non-empty string, got %r"
                            % (loc, value)))
    if seen and not [f for f in out if f[0] == FAIL]:
        out.append((OK, "%d non_reportable_heading declaration(s), all on non-reportable "
                        "terminals" % seen))
    return out


def check_satisfies_tests(ctx: DTContext):
    """
    `satisfies_tests[]` SUPPRESSES an outstanding-workup row. That makes it the one
    field in the file that can make a case look better worked up than it is, and it
    fails silently in both directions: a typo ("FISH" for "Cytogenetics/FISH") is
    simply never matched, so the suppression quietly does nothing; and app.js only
    ever subtracts it from `diagnostic_tests_required`, so a value the code does not
    require is an inert no-op that still reads, to the next author, as a live claim.
    Neither shows up as a broken build, a stack trace or a wrong screen — which is
    exactly why it needs a check rather than care.
    """
    out = []
    by_code: dict = {}
    for entry in ctx.entries:
        if isinstance(entry, dict):
            code = as_code(entry.get("morphology_code"))
            if code:
                req = entry.get("diagnostic_tests_required")
                by_code.setdefault(code, set()).update(req if isinstance(req, list) else [])

    seen = 0
    inert = []
    for node_id, node in sorted(ctx.nodes.items()):
        for holder, where in walk_dicts(node):
            if "satisfies_tests" not in holder:
                continue
            st = holder.get("satisfies_tests")
            loc = "node %s (%s)" % (node_id, where or "(node level)")
            if not isinstance(st, list) or not st or not all(isinstance(v, str) for v in st):
                out.append((FAIL, "%s: satisfies_tests must be a non-empty list of "
                                  "strings, got %r" % (loc, st)))
                continue
            code = as_code(holder.get("morphology_code"))
            if not code:
                out.append((FAIL, "%s: satisfies_tests on a branch that emits no "
                                  "morphology_code — app.js applies it only in finish(), "
                                  "so it is silently inert here" % loc))
                continue
            seen += 1
            required = by_code.get(code, set())
            for value in st:
                if value not in DIAGNOSTIC_TESTS:
                    out.append((FAIL, "%s: satisfies_tests value %r is not in the closed "
                                      "diagnostic-test vocabulary — it can never match a "
                                      "required test, so the suppression silently does "
                                      "nothing" % (loc, value)))
                elif value not in required:
                    inert.append("%s -> %s declares %r, which %s does not require"
                                 % (loc, code, value, code))

    if inert:
        out.append((NOTE, "%d satisfies_tests value(s) name a test the terminal code does "
                          "not require. Inert today (app.js subtracts only from "
                          "diagnostic_tests_required) but it becomes a live suppression the "
                          "day that code gains the requirement:\n        %s"
                    % (len(inert), "\n        ".join(inert))))
    if not [f for f in out if f[0] == FAIL]:
        out.append((OK, "%d satisfies_tests declaration(s): all values in the closed "
                        "vocabulary, all on code-emitting terminals" % seen))
    return out


# --------------------------------------------------------------------------------------
# B3. The four checks that did not exist before (data.md §5)
# --------------------------------------------------------------------------------------

def check_redcap_exact_names(ctx: DTContext, redcap_options: dict):
    """
    NEW CHECK 1 — exact-string match of morphology_name to the REDCap options file.

    The tool is ADVISORY: the clerk finds the row in REDCap by matching the WHOLE option
    string, not four digits (redcap.md §2, §5). Any drift between morphology_name and the
    REDCap option's name half therefore breaks the model.

    This check used to key off `redcap_option_verified` alone — only entries claiming
    `true` were compared, and `false` was a bare WARN. That left a hole wide enough to
    drive six codes through: an entry could be flagged `false` while Layer 1 DID carry an
    option string for its code, so its morphology_name was free to drift from a string
    sitting right there in the source of truth, and the build still passed.

    The rule is now keyed off Layer 1, not off the flag:

        code HAS an option string in Layer 1  ->  the name must be character-identical,
                                                  and a mismatch is a FAIL, whatever the
                                                  flag says.
        code has NO option string in Layer 1  ->  WARN. There is nothing to compare
                                                  against; the registry must add the
                                                  option before the terminal is usable.

    `redcap_option_verified: true` on a code Layer 1 does not carry stays a FAIL, and a
    stale `false` on a code it does carry is reported as a WARN so the flag is corrected.

    ONE exemption, deliberately narrow — the behaviour-overloaded code. 9898 has a single
    option string and that string names one of the two entities (ML-DS, /3); the sibling
    it does not name (TAM, /1) genuinely has no option string of its own. An entry is
    exempt only when ALL of:
        * it is flagged `redcap_option_verified: false` (it makes no claim), AND
        * another entry shares its morphology_code with a DIFFERENT behavior_code, AND
        * that sibling's morphology_name IS character-identical to the option.
    i.e. the option is demonstrably spoken for by the sibling. Anything less than all
    three and the mismatch is a FAIL — the exemption can never absorb ordinary drift.

    GROUPS 3, 4 AND 6 ARE OUT OF SCOPE, and are validated by something stronger (Group 3
    build contract §5.2; Group 4 build contract §1.1a; Group 6 build contract §8, all
    three adopting the same rule for the same reason — §0.3 lists four Group IV
    divergences and §2C lists EIGHT Group VI divergences, the largest Layer 1 split of
    any group built so far, between the REDCap option strings and the ICD-O-3.2
    preferred terms). For those groups Layer 1 for code identity is ICD-O-3.2, not the
    REDCap option file: check_icdo32_round_trip() requires every (code, name, behaviour)
    triple the engine can emit to exist verbatim in icdo32.sqlite. That is a superset of
    this check's question, because the option list itself carries (code, term) pairs the
    database does not — matching them would inherit the errors rather than catch them.
    The option strings are not dropped; they move to the alias file and are checked the
    other way round (every alias resolves to a valid triple; no alias is ever emitted).

    GROUP 5 IS DELIBERATELY NOT HERE. Its four option strings are character-identical to
    both sources, so this check and check_icdo32_round_trip() agree on it and there is no
    defect to fix; whether it should also move to the round-trip is a question for the
    Group 5 branch, not this one (Group 6 build contract §8).

    Nothing about Groups 1 and 2 changes. Their Layer 1 is still the option file, the
    sibling exemption still works exactly as described above, and the scoping below is a
    single equality on the group number — which comes from the FILENAME and is
    cross-checked against metadata.group_id by check_top_level_keys(), so it is not a
    flag in the file exempting itself (rule 8).
    """
    out = []
    if ctx.group in ROUND_TRIP_GROUPS:
        return [(NOTE, "group %d: morphology_name is checked by check_icdo32_round_trip() "
                       "against icdo32.sqlite instead of against the REDCap option file "
                       "(contract §5.2 for Group 3; §1.1a for Group 4; Group 6 build "
                       "contract §8 for Group 6, whose eight REDCap-string drifts — "
                       "§2C, two of them naming a different lesion entirely — would "
                       "otherwise FAIL this check on correct data). That is the "
                       "stronger question — it rejects (code, term) pairs the option list "
                       "carries that ICD-O-3.2 does not, where this check would have "
                       "inherited them. Group 7 joins on its own contract §2E, for ten "
                       "drifts; Group 8 on its contract §2, whose viii_morph offers "
                       "Ewing sarcoma on the retired number 9260; Group 10 on its "
                       "contract §5. Groups 1 and 2 are unaffected."
                       % ctx.group)]
    options = redcap_options.get(ctx.group)
    if not options:
        return [(NOTE, "no REDCap options parsed for group %d — exact-string check skipped"
                 % ctx.group)]

    def variants_of(option):
        return option.get("names") or [option["name"]]

    # code -> [entries], so the behaviour-overload exemption can see an entry's siblings.
    by_code: dict[str, list] = {}
    for entry in ctx.entries:
        if not isinstance(entry, dict):
            continue
        code = as_code(entry.get("morphology_code"))
        if code is not None:
            by_code.setdefault(code, []).append(entry)

    def sibling_claims_option(entry, code, variants):
        """True when a DIFFERENT-behaviour entry on this code already matches the option."""
        mine = entry.get("behavior_code")
        for other in by_code.get(code, []):
            if other is entry:
                continue
            if other.get("behavior_code") == mine:
                continue
            if isinstance(other.get("morphology_name"), str) \
                    and other["morphology_name"] in variants:
                return True
        return False

    compared = matched = 0
    no_option: list[str] = []
    for entry in ctx.entries:
        if not isinstance(entry, dict):
            continue
        code = as_code(entry.get("morphology_code"))
        name = entry.get("morphology_name")
        if code is None:
            continue
        flag = entry.get("redcap_option_verified")
        option = options.get(code)

        if option is None:
            # Nothing in Layer 1 to compare against.
            if flag is True:
                out.append((FAIL, "entry %s claims redcap_option_verified: true but no "
                                  "REDCap option with that code exists for group %d"
                            % (code, ctx.group)))
            else:
                no_option.append(code)
            continue

        # Layer 1 carries an option for this code — the name MUST match it.
        variants = variants_of(option)
        compared += 1
        if isinstance(name, str) and name in variants:
            matched += 1
            if flag is not True:
                out.append((WARN, "entry %s: morphology_name matches the REDCap option but "
                                  "redcap_option_verified is %r — the flag is stale and "
                                  "should be true" % (code, flag)))
            continue

        if flag is not True and sibling_claims_option(entry, code, variants):
            # Behaviour-overloaded code: the one option string is spoken for by the
            # sibling behaviour. This entry has no option string of its own.
            compared -= 1
            out.append((NOTE, "entry %s/%s (%r) is the unnamed half of a behaviour-"
                              "overloaded code — the single REDCap option names the "
                              "%s behaviour; no option string of its own"
                        % (code, entry.get("behavior_code"), name,
                           next((o.get("behavior_code") for o in by_code.get(code, [])
                                 if o is not entry
                                 and isinstance(o.get("morphology_name"), str)
                                 and o["morphology_name"] in variants), "?"))))
            no_option.append("%s/%s" % (code, entry.get("behavior_code")))
            continue

        out.append((FAIL, "entry %s: a REDCap option EXISTS for this code and "
                          "morphology_name is not character-identical to it "
                          "(redcap_option_verified: %r — the flag does not exempt it).\n"
                          "               dt.json : %r\n"
                          "               REDCap  : %s"
                    % (code, flag, name, " | ".join(repr(v) for v in variants))))

    if no_option:
        out.append((WARN, "%d code(s) have no REDCap option string in Layer 1: %s"
                    % (len(no_option), ", ".join(sorted(set(no_option))))))
    if compared:
        out.append((OK, "%d/%d morphology_name(s) whose code HAS a REDCap option are "
                        "character-identical to it" % (matched, compared)))
    return out


def check_raw_hex_ban(repo: Path):
    """
    NEW CHECK 2 — raw-hex ban (data.md §5).

    Grep index.html, app.js and uccf-tool.css for #RGB..#RRGGBBAA occurring OUTSIDE the
    :root{…} token block. Colour literals belong in the token block and nowhere else.
    Deliberately a grep, not oxlint: oxlint lints JS literals and cannot see CSS at all.
    """
    out = []
    for filename in HEX_SCANNED_FILENAMES:
        matches = [p for p in sorted(repo.rglob(filename))
                   if ".git" not in p.parts and "node_modules" not in p.parts]
        if not matches:
            out.append((NOTE, "%s does not exist yet — raw-hex scan skipped" % filename))
            continue
        for path in matches:
            try:
                text = path.read_text(encoding="utf-8")
            except OSError as exc:
                out.append((WARN, "could not read %s: %s" % (path, exc)))
                continue
            text = _mask_comments(text)
            allowed = _root_block_spans(text)
            rel = path.relative_to(repo)
            hits = 0
            for lineno, line in enumerate(text.splitlines(), start=1):
                for m in HEX_RE.finditer(line):
                    if any(lo <= lineno <= hi for lo, hi in allowed):
                        continue
                    hits += 1
                    out.append((FAIL, "%s:%d raw hex colour %s outside the :root token "
                                      "block — use a CSS custom property"
                                % (rel, lineno, m.group(0))))
            if hits == 0:
                out.append((OK, "%s: no raw hex outside :root (%d :root block(s))"
                            % (rel, len(allowed))))
    return out


def _mask_comments(text: str) -> str:
    """
    Replace the CONTENT of /* … */ and // … comments with spaces, preserving every
    newline so line numbers still line up.

    Without this the scan is defeated by a commented-out token block: a stray
    `/* :root {` makes the brace matcher swallow every rule after it, whitelisting
    their colours. It also stops a hex written in a comment (documentation, not a
    colour in use) from being reported as a violation.
    """
    out = list(text)
    i, n = 0, len(text)
    while i < n:
        if text.startswith("/*", i):
            j = text.find("*/", i + 2)
            j = n if j == -1 else j + 2
            for k in range(i, j):
                if out[k] != "\n":
                    out[k] = " "
            i = j
        elif text.startswith("//", i) and not text.startswith("://", max(0, i - 1)):
            j = text.find("\n", i)
            j = n if j == -1 else j
            for k in range(i, j):
                out[k] = " "
            i = j
        else:
            i += 1
    return "".join(out)


def _root_block_spans(text: str):
    """
    Return [(first_line, last_line)] for every `:root … { … }` token block.

    The selector must OPEN a rule (start of file, or straight after `}` or `;`) and must
    reach its `{` without crossing a comma — so a genuine `:root {` or
    `:root:not([data-theme]) {` is whitelisted, while `html, :root, body {` is not: that
    rule also styles other elements, so its colours are not token declarations.
    """
    spans = []
    for m in re.finditer(r"(?:\A|[};])\s*:root\b[^{,]{0,120}?\{", text):
        depth = 0
        i = m.end() - 1
        while i < len(text):
            ch = text[i]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        start_line = text.count("\n", 0, m.start()) + 1
        end_line = text.count("\n", 0, min(i, len(text) - 1)) + 1
        spans.append((start_line, end_line))
    return spans


def check_cryptic_genetics(ctx: DTContext):
    """
    NEW CHECK 3 — cryptic-genetics lint (Pathway §4.4, §7.5).

    9814 (ETV6::RUNX1), 9965 (FIP1L1::PDGFRA) and the AMKL fusion terminals (9910, 9911)
    are cryptic: invisible on a normal karyotype. They must never be reachable ONLY along
    paths that pass through a `karyotype_only` option, and must never be offered ON a
    `karyotype_only` option. That JSON is perfectly valid and clinically wrong — which is
    the whole reason this lint exists.

    Method: two graph walks from the tree entry nodes — one over all edges, one over edges
    whose option is not `karyotype_only`. A terminal reachable in the first walk but not
    the second is gated exclusively behind a karyotype-only branch.
    """
    out = []
    targets = sorted(CRYPTIC_TERMINAL_CODES & {c for c, _h, _n, _w in ctx.emissions()})
    if not targets:
        return [(NOTE, "no cryptic-genetics terminal (%s) emitted in this file — lint "
                 "has nothing to check" % ", ".join(sorted(CRYPTIC_TERMINAL_CODES)))]

    roots = [e for e in ctx.entry_nodes() if e in ctx.nodes]
    all_edges: dict[str, set] = {}
    clean_edges: dict[str, set] = {}
    for src, target, dm, _w in ctx.transitions():
        all_edges.setdefault(src, set()).add(target)
        if dm != "karyotype_only":
            clean_edges.setdefault(src, set()).add(target)

    def reach(edges):
        seen = set(roots)
        stack = list(roots)
        while stack:
            cur = stack.pop()
            for nxt in edges.get(cur, ()):
                if nxt in ctx.nodes and nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        return seen

    reachable_all = reach(all_edges)
    reachable_clean = reach(clean_edges)

    ok_codes = []
    for code in targets:
        sites = [(h, n, w) for c, h, n, w in ctx.emissions() if c == code]
        clean_sites = []
        reachable_sites = []
        for holder, node_id, where in sites:
            if holder.get("detection_method") == "karyotype_only":
                out.append((FAIL, "cryptic terminal %s is offered ON a karyotype_only "
                                  "option at %s (%s) — a normal karyotype cannot detect "
                                  "it (Pathway §4.4)" % (code, node_id, where)))
                continue
            if node_id in reachable_all:
                reachable_sites.append((node_id, where))
            if node_id in reachable_clean:
                clean_sites.append((node_id, where))
        if clean_sites:
            ok_codes.append(code)
        elif reachable_sites:
            # Emitting a cryptic code behind the FISH-status guard is correct; emitting it
            # ONLY there — with no path that reaches it without a normal-karyotype branch —
            # means a normal karyotype silently closes the branch.
            out.append((FAIL, "cryptic terminal %s is reachable ONLY through a "
                              "karyotype_only option (offered at %s) — every path to it "
                              "passes a normal-karyotype branch, so a normal karyotype "
                              "closes the branch (Pathway §7.5)"
                        % (code, ", ".join("%s/%s" % (n, w) for n, w in reachable_sites))))
    if ok_codes:
        out.append((OK, "cryptic terminal(s) %s reachable without passing a karyotype_only "
                        "option" % ", ".join(ok_codes)))
    return out


def check_mpal_rule_ordering(ctx: DTContext):
    """
    NEW CHECK 4 — resolution_logic dead-rule lint (Pathway §7.3 item 3, §7.5).

    `resolution_logic` is flat and first-match-wins, so an earlier rule can make a later
    one unreachable. The MPAL case is the one this was written for: the genetics-first
    ordering puts 9806/9807 (BCR::ABL1, KMT2A) ahead of the ungenotyped 9808/9809 on the
    identical marker set, and reversing them means the genotyped codes can never fire.

    The test is SUBSUMPTION, not position. Rule R at index j is dead when some earlier
    rule E at index i < j satisfies all three of

        E.positive ⊆ R.positive    E.negative ⊆ R.negative    E.when ⊆ R.when

    (`when` compared as key/value pairs). E then asks for strictly less than R does, so
    every case that matches R has already matched E, and R can never be reached.

    The first version of this check compared only "carries a `when`" against "carries no
    `when`", positionally. That was sound on Group 1, where the rules it governed shared
    one marker set — there E was unconditioned with the same markers, so E.when = {} ⊆
    R.when and the marker sets were equal, which is this rule's special case. It is wrong
    anywhere the rules have disjoint marker sets: a Group II node routinely carries a dozen
    rules distinguished only by their panels, and an unconditioned rule earlier in the list
    swallows a later one only when it fires for every case the later one fires for. On
    Group II that heuristic produced 48 FAILs on perfectly reachable rules — a false FAIL
    at scale, which teaches the next author to work around the validator (data.md §5A).

    Deliberate limit: tokens are compared as written, so `CD19` and `CD19:strong` are
    different requirements. That is the safe direction — an intensity-qualified token is
    genuinely narrower than the bare marker, so treating them as equal would report
    reachable rules as dead.
    """
    out = []
    rulesets = 0
    checked = 0

    def token_set(rule, field):
        values = rule.get(field)
        if not isinstance(values, list):
            return frozenset()
        return frozenset(v for v in values if isinstance(v, str))

    def when_pairs(rule):
        when = rule.get("when")
        if not isinstance(when, dict):
            return frozenset()
        pairs = set()
        for key, value in when.items():
            try:
                pairs.add((key, json.dumps(value, sort_keys=True, ensure_ascii=False)))
            except (TypeError, ValueError):
                pairs.add((key, repr(value)))
        return frozenset(pairs)

    for node_id, node in sorted(ctx.nodes.items()):
        rules = node.get("resolution_logic")
        if not isinstance(rules, list) or not rules:
            continue
        rulesets += 1
        shapes = []
        for i, rule in enumerate(rules):
            if not isinstance(rule, dict):
                out.append((FAIL, "node %s: resolution_logic[%d] is not an object"
                            % (node_id, i)))
                shapes.append(None)
                continue
            shapes.append((token_set(rule, "positive"), token_set(rule, "negative"),
                           when_pairs(rule)))
        for j, later in enumerate(shapes):
            if later is None:
                continue
            checked += 1
            for i, earlier in enumerate(shapes[:j]):
                if earlier is None:
                    continue
                if (earlier[0] <= later[0] and earlier[1] <= later[1]
                        and earlier[2] <= later[2]):
                    out.append((FAIL, "node %s: resolution_logic[%d] can never fire — "
                                      "rule [%d] above it asks for strictly less "
                                      "(positive %s, negative %s, when %s vs this rule's "
                                      "positive %s, negative %s, when %s), so every case "
                                      "that matches [%d] has already matched [%d] and "
                                      "first-match-wins stops there (Pathway §7.5)"
                                % (node_id, j, i,
                                   sorted(earlier[0]) or "-", sorted(earlier[1]) or "-",
                                   sorted(k for k, _v in earlier[2]) or "-",
                                   sorted(later[0]) or "-", sorted(later[1]) or "-",
                                   sorted(k for k, _v in later[2]) or "-", j, i)))
                    break

    if not out:
        out.append((OK, "no dead rule in %d resolution_logic ruleset(s), %d rule(s) tested "
                        "for subsumption by an earlier rule" % (rulesets, checked)))
    return out


# --------------------------------------------------------------------------------------
# B4. Group II schema extensions (Group II build contract §3) and the viral-gate lint
#
# Five constructs and one path lint. Every one of them is a FIELD on an existing
# structure — Group II invents no node types (contract §0 rule 3), so nothing in this
# section touches NODE_TYPES.
# --------------------------------------------------------------------------------------

def _code_behavior_pairs(ctx: DTContext) -> set:
    """{(morphology_code, behavior_code)} exactly as authored in morphology_entries[]."""
    pairs = set()
    for entry in ctx.entries:
        if not isinstance(entry, dict):
            continue
        code = as_code(entry.get("morphology_code"))
        if code is None:
            continue
        beh = entry.get("behavior_code")
        pairs.add((code, None if beh is None else str(beh).strip()))
    return pairs


def _declared_variables(node) -> set:
    declared = node.get("captured_variables")
    return set(declared) if isinstance(declared, list) else set()


def destination_kinds(container) -> list:
    """
    Which of the four DT master §3F destinations a branch carries. Exactly one is legal:
    zero is a dead end app.js throws on, two is an ambiguity it resolves by accident of
    dispatch order rather than by anything anyone wrote down.
    """
    kinds = []
    if isinstance(container, dict):
        if as_code(container.get("morphology_code")):
            kinds.append("morphology_code")
        if is_refer_branch(container):
            kinds.append("refer_group")
        if is_non_reportable(container):
            kinds.append("non_reportable")
        if container.get("next_node"):
            kinds.append("next_node")
    return kinds


def destination_signature(container):
    """
    WHERE a branch sends the case, as a comparable tuple — the thing two branches must not
    share when one handles `not_assessable` and the other handles `negative` (§3.4).

    Deliberately ignores the prose (`reason`, `coding_note`, `label`): two branches that
    read differently on screen but land the clerk in the same place are the same
    destination, and it is the landing place this rule is about.
    """
    if not isinstance(container, dict):
        return None
    nxt = container.get("next_node")
    if isinstance(nxt, str) and nxt:
        return ("next_node", nxt)
    code = as_code(container.get("morphology_code"))
    if code:
        beh = container.get("behavior_code")
        return ("code", code, None if beh is None else str(beh).strip())
    if is_refer_branch(container):
        return ("refer", container.get("refer_group"), as_code(container.get("refer_code")))
    if is_non_reportable(container):
        return ("non_reportable",)
    return None


def _destination_text(sig) -> str:
    if sig is None:
        return "(no destination)"
    if sig[0] == "next_node":
        return "next_node %s" % sig[1]
    if sig[0] == "code":
        return "code %s/%s" % (sig[1], sig[2])
    if sig[0] == "refer":
        return "referral to group %s" % (sig[1],)
    return "a non-reportable terminal"


def _canonical(value):
    """A comparable form for an arbitrary JSON value, or None when there is nothing."""
    if value is None:
        return None
    try:
        return json.dumps(value, sort_keys=True, ensure_ascii=False)
    except (TypeError, ValueError):
        return repr(value)


def _branch_containers(node):
    """Yield (holder, where) for every BRANCH on a node — the things DT master §3F governs."""
    for field in ("options", "resolution_logic", "bands", "override_when"):
        seq = node.get(field)
        if not isinstance(seq, list):
            continue
        for i, holder in enumerate(seq):
            if isinstance(holder, dict):
                yield holder, "%s[%d]" % (field, i)


def check_behaviour_resolution(ctx: DTContext):
    """
    GROUP II CHECK 1 — `behaviour_resolution` (contract §3.1).

    For 9718, 9725 and 9751 the behaviour — and with it whether the case is in ICCC-3
    Group II at all — turns on a clinical fact the pathology report cannot supply: do the
    individual lesions regress by themselves? The construct puts that question and both
    answers into the JSON instead of leaving a coder to pick a behaviour off the slide.

    The rule this check exists for is `unresolved`. It is REQUIRED and it must name the
    `/3` half. An unresolved behaviour that quietly defaults to `/1` does not produce a
    wrong code — it produces NO reportable case, and a reportable childhood cancer leaves
    the registry with nothing on screen to say it ever arrived. There is no wording that
    makes that a warning, so it is a FAIL.

    Everything else here is shape: the required keys, the variable declared where the
    engine can read it (contract §5), exactly the two behaviour keys, one destination per
    leaf (DT master §3F), both (code, behaviour) pairs real, and — for the one deferrable
    case, 9725 — something written down about what re-opens the case.
    """
    out = []
    pairs = _code_behavior_pairs(ctx)
    seen = 0

    for node_id, node in sorted(ctx.nodes.items()):
        declared = _declared_variables(node)
        for holder, where in walk_dicts(node):
            loc = "node %s (%s)" % (node_id, where or "(node level)")

            # The US spelling is not a synonym — nothing reads it, so the block and its
            # unresolved half would be silently inert. Catch it rather than find nothing.
            if "behavior_resolution" in holder and "behaviour_resolution" not in holder:
                out.append((FAIL, "%s: the key is spelled 'behavior_resolution'; the "
                                  "contract spells it 'behaviour_resolution' (§3.1). "
                                  "Nothing reads the US spelling, so the whole block — the "
                                  "required 'unresolved' half included — is inert"
                            % loc))
            if "behaviour_resolution" not in holder:
                continue

            br = holder["behaviour_resolution"]
            if not isinstance(br, dict):
                out.append((FAIL, "%s: behaviour_resolution must be an object, got %r"
                            % (loc, br)))
                continue
            seen += 1

            for key in ("criterion", "variable"):
                val = br.get(key)
                if not isinstance(val, str) or not val.strip():
                    out.append((FAIL, "%s: behaviour_resolution.%s is required and must be "
                                      "a non-empty string (contract §3.1)" % (loc, key)))
            for key in ("clinical_only", "deferrable"):
                if not isinstance(br.get(key), bool):
                    out.append((FAIL, "%s: behaviour_resolution.%s is required and must be "
                                      "a boolean (contract §3.1)" % (loc, key)))

            var = br.get("variable")
            if isinstance(var, str) and var and var not in declared:
                out.append((FAIL, "%s: behaviour_resolution.variable %r is not declared in "
                                  "this node's captured_variables[] (contract §5) — the "
                                  "engine has nowhere to read the answer from, so the "
                                  "criterion is asked and then discarded"
                            % (loc, var)))

            values = br.get("values")
            if not isinstance(values, dict):
                out.append((FAIL, "%s: behaviour_resolution.values is required and must be "
                                  "an object keyed \"1\" and \"3\" (contract §3.1)" % loc))
                values = {}
            elif not (len(values) == 2 and set(values) <= {"0", "1", "3"}):
                # Ratified 2026-09-14. Group II required exactly {"1","3"} because there a
                # /1 puts the case OUTSIDE the group, so defaulting to it deletes a
                # reportable cancer. Group III declares 0-1,3 on every range, so /0 stays
                # in the group and on the registry — the asymmetry inverts. The pituitary
                # pairs are /0 <-> /3, and forcing a /3 default there would manufacture a
                # pituitary carcinoma out of a missing staging report, since malignancy in
                # the pituitary requires a demonstrated metastasis and no histological
                # feature qualifies (Pathway Revision 2 §4.11).
                out.append((FAIL, "%s: behaviour_resolution.values is keyed %s — exactly two "
                                  "of \"0\", \"1\", \"3\" are required, and they must be the two "
                                  "behaviours the code actually carries (contract §3.1)"
                            % (loc, ", ".join(repr(k) for k in sorted(values)) or "(empty)")))

            def check_leaf(label, leaf, expected_beh):
                if not isinstance(leaf, dict):
                    out.append((FAIL, "%s: behaviour_resolution.%s must be an object, got %r"
                                % (loc, label, leaf)))
                    return
                kinds = destination_kinds(leaf)
                if len(kinds) != 1:
                    out.append((FAIL, "%s: behaviour_resolution.%s resolves to %d "
                                      "destination(s)%s — DT master §3F requires exactly one"
                                % (loc, label, len(kinds),
                                   " (%s)" % ", ".join(kinds) if kinds else "")))
                code = as_code(leaf.get("morphology_code"))
                beh = leaf.get("behavior_code")
                beh = None if beh is None else str(beh).strip()
                if code and (code, beh) not in pairs:
                    out.append((FAIL, "%s: behaviour_resolution.%s emits %s/%s, which has no "
                                      "morphology_entries[] object in this file "
                                      "(contract §3.1)" % (loc, label, code, beh)))
                if code and beh is not None and beh != expected_beh:
                    out.append((FAIL, "%s: behaviour_resolution.%s emits behavior_code %r "
                                      "where %r is required — under values[] the key IS the "
                                      "behaviour, so a mismatch files the case under a "
                                      "behaviour nobody chose (contract §3.1)"
                                % (loc, label, beh, expected_beh)))

            for key in sorted(values):
                check_leaf('values["%s"]' % key, values[key], key)

            unresolved = br.get("unresolved")
            if unresolved is None:
                out.append((FAIL, "%s: behaviour_resolution.unresolved is REQUIRED "
                                  "(contract §3.1). Without it the engine has no answer for "
                                  "a file that never states the behaviour, and the case "
                                  "leaves the node with no code at all — a reportable "
                                  "childhood cancer dropped from the registry rather than "
                                  "coded" % loc))
            else:
                u_named = str(unresolved.get("behavior_code") or "").strip() \
                    if isinstance(unresolved, dict) else ""
                check_leaf("unresolved", unresolved, u_named or "3")
                if isinstance(unresolved, dict):
                    u_code = as_code(unresolved.get("morphology_code"))
                    u_beh = unresolved.get("behavior_code")
                    u_beh = None if u_beh is None else str(u_beh).strip()
                    if not u_code:
                        out.append((FAIL, "%s: behaviour_resolution.unresolved emits no "
                                          "morphology_code. It must name the /3 half — "
                                          "never \"no code\". An unstated behaviour is a "
                                          "gap in the file, not evidence that the disease "
                                          "is benign (contract §3.1)" % loc))
                    elif u_beh != "3" and u_beh in {k for k in values} and \
                            (u_code, u_beh) in pairs and str(unresolved.get("reason") or "").strip():
                        # Ratified 2026-09-14. The /3 requirement exists because in Group II
                        # the other half is OUTSIDE the group, so defaulting there deletes a
                        # reportable cancer. Where both halves are carried as entries in this
                        # file they are both inside the group by construction, and nothing is
                        # deleted either way. What replaces the rule is that the choice must
                        # be argued in writing on the branch: pituitary malignancy requires a
                        # demonstrated metastasis and no histological feature qualifies, so a
                        # /3 default there manufactures a carcinoma out of a missing staging
                        # report (Pathway Revision 2 §4.11).
                        pass
                    elif u_beh != "3":
                        out.append((FAIL, "%s: behaviour_resolution.unresolved names %s/%s. "
                                          "It must name the /3 half. Defaulting an "
                                          "unresolved behaviour to /1 does not mis-code the "
                                          "case — it silently deletes a reportable cancer "
                                          "from the registry, because /1 is outside ICCC-3 "
                                          "Group II entirely. Code the reportable half and "
                                          "let the clinical history downgrade it later "
                                          "(contract §3.1)" % (loc, u_code, u_beh)))

            if br.get("deferrable") is True:
                follow_up = br.get("follow_up_review")
                if not isinstance(follow_up, str) or not follow_up.strip():
                    out.append((FAIL, "%s: behaviour_resolution.deferrable is true, so a "
                                      "non-empty 'follow_up_review' saying what re-opens "
                                      "the case is required — a deferral with no stated "
                                      "trigger is an abandonment (contract §3.1)" % loc))

    if [f for f in out if f[0] == FAIL]:
        return out
    if seen:
        out.append((OK, "%d behaviour_resolution block(s) well formed; every 'unresolved' "
                        "names the /3 half (contract §3.1)" % seen))
    else:
        out.append((NOTE, "no behaviour_resolution block in this file — Group II construct, "
                          "nothing to check here"))
    return out


def check_provisional_pending(ctx: DTContext):
    """
    GROUP II CHECK 2 — `provisional_pending` (contract §3.2).

    A named, reversible provisional: this code stands, and this specific test is the one
    that would overturn it. It is a claim about one outstanding result, not a general
    statement about the whole terminal.

    The rule this check exists for is the last one. A branch may not name a test as
    `resolving_test` AND list that same test in `satisfies_tests`. `satisfies_tests`
    removes the test from the outstanding-workup list, so nobody is asked for it;
    `provisional_pending` says the code may be overturned by it. One of the two is false,
    and the screen shows the flattering one: a case that reads fully worked up while the
    file itself records the very test as outstanding. Neither field breaks a build alone,
    which is why the pairing is checked here (contract §3.2, §6).
    """
    out = []
    seen = 0
    for node_id, node in sorted(ctx.nodes.items()):
        for holder, where in walk_dicts(node):
            if "provisional_pending" not in holder:
                continue
            loc = "node %s (%s)" % (node_id, where or "(node level)")
            pp = holder["provisional_pending"]
            if not isinstance(pp, dict):
                out.append((FAIL, "%s: provisional_pending must be an object, got %r"
                            % (loc, pp)))
                continue
            seen += 1

            reason = pp.get("reason")
            if not isinstance(reason, str) or not reason.strip():
                out.append((FAIL, "%s: provisional_pending.reason is required and must be a "
                                  "non-empty string — it is clerk-facing and it is what the "
                                  "engine renders (contract §3.2)" % loc))

            test = pp.get("resolving_test")
            if not isinstance(test, str) or not test.strip():
                out.append((FAIL, "%s: provisional_pending.resolving_test is required "
                                  "(contract §3.2)" % loc))
            elif test not in DIAGNOSTIC_TESTS:
                out.append((FAIL, "%s: provisional_pending.resolving_test %r is not in the "
                                  "closed diagnostic-test vocabulary (%s). A value nothing "
                                  "can match names no real outstanding test, so the "
                                  "provisional reads as specific and resolves to nothing"
                            % (loc, test, ", ".join(sorted(DIAGNOSTIC_TESTS)))))

            if not as_code(holder.get("morphology_code")):
                out.append((FAIL, "%s: provisional_pending on a branch that emits no "
                                  "morphology_code. A provisional QUALIFIES a code; with no "
                                  "code there is nothing to overturn and nothing is rendered "
                                  "(contract §3.2)" % loc))

            alts = pp.get("alternative_codes")
            if alts is not None:
                if not isinstance(alts, list):
                    out.append((FAIL, "%s: provisional_pending.alternative_codes must be an "
                                      "array of code strings" % loc))
                else:
                    for alt in alts:
                        alt_code = as_code(alt)
                        if alt_code is None:
                            out.append((FAIL, "%s: provisional_pending.alternative_codes "
                                              "entry %r is not a code string" % (loc, alt)))
                        elif alt_code not in ctx.codes:
                            out.append((FAIL, "%s: provisional_pending.alternative_codes "
                                              "names %s, which has no morphology_entries[] "
                                              "object here — the alternative the clerk is "
                                              "told to consider cannot be coded from this "
                                              "file (contract §3.2)" % (loc, alt_code)))

            ents = pp.get("alternative_entities")
            if ents is not None and (not isinstance(ents, list)
                                     or not all(isinstance(e, str) for e in ents)):
                out.append((FAIL, "%s: provisional_pending.alternative_entities must be an "
                                  "array of strings (free text — the uncoded WHO entities "
                                  "of Pathway §5.2)" % loc))

            satisfies = holder.get("satisfies_tests")
            if isinstance(test, str) and isinstance(satisfies, list) and test in satisfies:
                out.append((FAIL, "%s: this branch names %r as provisional_pending."
                                  "resolving_test AND lists it in satisfies_tests. That "
                                  "claims one test simultaneously outstanding and "
                                  "discharged — the provisional says the code may be "
                                  "overturned by it, satisfies_tests strikes it off the "
                                  "outstanding-workup list so nobody is asked for it. The "
                                  "case then reads better evidenced than the file itself "
                                  "says it is. Drop one; they cannot both be true "
                                  "(contract §3.2, §6)" % (loc, test)))

    if [f for f in out if f[0] == FAIL]:
        return out
    if seen:
        out.append((OK, "%d provisional_pending block(s) well formed; none names a test it "
                        "also discharges via satisfies_tests (contract §3.2)" % seen))
    else:
        out.append((NOTE, "no provisional_pending block in this file — Group II construct, "
                          "nothing to check here"))
    return out


# Words that identify a modality rather than the analyte, so they cannot be what makes a
# prior and a branch condition "about the same test".
_TEST_STOPWORDS = {
    "status", "ish", "ihc", "fish", "pcr", "result", "results", "pct", "percent",
    "test", "testing", "stain", "staining", "by", "or", "and", "the", "a", "of", "on",
    "in", "tissue", "assay", "panel", "study", "studies", "value", "level",
}


def _test_key(text: str) -> set:
    """The analyte words in a test label or variable name — 'EBER ISH' -> {'eber'}."""
    words = re.split(r"[^0-9A-Za-z]+", text.lower())
    return {w for w in words if w and w not in _TEST_STOPWORDS}


def _branch_decides_on_test(holder, test: str) -> bool:
    """
    True when this branch reaches its code BY the test a prior_probability names.

    Read off the branch's own conditions — the variables it keys on and the marker tokens
    it requires. A branch that emits a code on architecture while merely displaying an
    EBER prior is not deciding on EBER; one whose `when` is {"eber_status": "positive"} is.
    """
    key = _test_key(test)
    if not key:
        return False
    for field in ("when", "captures"):
        blob = holder.get(field)
        if isinstance(blob, dict):
            for name in blob:
                if key & _test_key(str(name)):
                    return True
    for field in ("positive", "negative"):
        values = holder.get(field)
        if isinstance(values, list):
            for token in values:
                if isinstance(token, str) and key & _test_key(token):
                    return True
    return False


def check_prior_probability(ctx: DTContext):
    """
    GROUP II CHECK 3 — `prior_probability` (contract §3.3).

    The prior against which a test result is informative. A positive EBER in
    mixed-cellularity classic Hodgkin lymphoma is expected in 70-80% of cases and
    therefore says almost nothing; the block exists so that a routine result is not read
    as confirmation (Pathway §4.3).

    It is DISPLAY-ONLY, and this check enforces that twice over, because a prior that
    appears to carry a decision is worse than no prior at all:

      * the block itself may hold no destination — a prior that routes is not a prior,
        it is a rule wearing a prior's name;
      * and it may not sit on a branch that BOTH emits a morphology_code AND decides that
        code on the very test the prior is about. There the prior reads as the evidence
        for the code, which inverts the one thing it was introduced to do (contract §6).

    That second rule was first written as "not on any code-emitting branch", and real data
    showed that to be wrong: contract §3.3's own canonical example — mixed-cellularity
    classic Hodgkin lymphoma, EBER expected in 70-80% — belongs on exactly such a branch.
    `g2_chl_subtype` options[4] emits 9652 on ARCHITECTURE, and carries the EBER prior to
    say the expected positive result must not be allowed to refine the subtype. Failing
    that is failing the best authoring in the file. What matters is not whether the branch
    emits a code but whether it decides that code on the prior's own test, so the rule now
    fires only when the branch's own conditions (`when`, `captures`, `positive[]`,
    `negative[]`) name the test the prior names.

    `expected_positive_pct` is a STRING on purpose — the sources give "70-80" and "<4",
    not numbers — so a bare number is a FAIL rather than a silent coercion.
    """
    out = []
    seen = 0
    for node_id, node in sorted(ctx.nodes.items()):
        for holder, where in walk_dicts(node):
            if "prior_probability" not in holder:
                continue
            loc = "node %s (%s)" % (node_id, where or "(node level)")
            pr = holder["prior_probability"]
            if not isinstance(pr, dict):
                out.append((FAIL, "%s: prior_probability must be an object, got %r"
                            % (loc, pr)))
                continue
            seen += 1

            for key in ("test", "interpretation"):
                val = pr.get(key)
                if not isinstance(val, str) or not val.strip():
                    out.append((FAIL, "%s: prior_probability.%s is required and must be a "
                                      "non-empty string (contract §3.3)" % (loc, key)))

            if "expected_positive_pct" in pr and pr["expected_positive_pct"] is not None:
                pct = pr["expected_positive_pct"]
                if not isinstance(pct, str) or not pct.strip():
                    out.append((FAIL, "%s: prior_probability.expected_positive_pct must be a "
                                      "non-empty STRING (%r) — the sources give ranges and "
                                      "bounds (\"70-80\", \"<4\"), and a number here "
                                      "quietly asserts a precision nobody published "
                                      "(contract §3.3)" % (loc, pct)))

            if "context" in pr and pr["context"] is not None \
                    and not isinstance(pr["context"], str):
                out.append((FAIL, "%s: prior_probability.context must be a string" % loc))

            stray = destination_kinds(pr)
            if stray:
                out.append((FAIL, "%s: prior_probability carries %s. It is display-only and "
                                  "must change no destination — a prior that routes is a "
                                  "rule, and moving a routing decision into a block nobody "
                                  "reads as routing hides it (contract §3.3)"
                            % (loc, ", ".join(stray))))

            code = as_code(holder.get("morphology_code"))
            test = pr.get("test")
            if code and isinstance(test, str) and _branch_decides_on_test(holder, test):
                out.append((FAIL, "%s: prior_probability about %r sits on a branch that "
                                  "emits %s AND decides that code on %r itself. Rendered "
                                  "beside a code the branch reached BY that test, the prior "
                                  "reads as the evidence for the code — when its entire "
                                  "purpose is the opposite: to say the result was expected "
                                  "and is weakly informative. A prior belongs where the "
                                  "test is being interpreted, not where its expected answer "
                                  "picks the code (contract §3.3, §6)"
                            % (loc, test, code, test)))

    if [f for f in out if f[0] == FAIL]:
        return out
    if seen:
        out.append((OK, "%d prior_probability block(s) well formed, display-only, none on a "
                        "code-emitting branch (contract §3.3)" % seen))
    else:
        out.append((NOTE, "no prior_probability block in this file — Group II construct, "
                          "nothing to check here"))
    return out


def check_test_result_states(ctx: DTContext):
    """
    GROUP II CHECK 4 — `test_result_states` (contract §3.4).

    Some tests fail in a way that is neither positive nor negative. An EBER ISH whose
    internal control did not light up, a FISH that did not hybridise, an FNA with too few
    cells: the answer is "we could not read it", and the node has to offer that.

    The shape half is small — the declared variable exists in `captured_variables[]`, the
    states come from the closed vocabulary, and any node branching on `eber_status`,
    `fish_status` or `fna_adequacy` declares its states and includes `not_assessable`.

    The LOAD-BEARING half is the last rule. Within one node, the branch that handles
    `not_assessable` must be DISTINGUISHABLE from the branch that handles `negative` —
    either by landing somewhere else, or by carrying a `provisional_pending` that the
    negative branch does not.

    They are different findings with different consequences. `negative` means the finding
    is absent, the differential narrows and the workup is done; `not_assessable` means
    nobody knows, and a repeat on a fresh section is owed. Report them identically and an
    absent result silently becomes evidence of absence, on a screen that looks complete,
    with nothing anywhere saying the test never actually returned (contract §3.4, §6;
    Pathway §2.4, §4.3, §7.3 item 4).

    The first version demanded a different DESTINATION, full stop, and that was too narrow.
    Sometimes the same destination is the honest answer: 9719 requires EBER POSITIVITY, so
    neither a negative nor an uninterpretable EBER unlocks anything and both correctly land
    on 9702. Forcing them apart there would be false precision. What may not happen is that
    they become indistinguishable — same code, same follow-up — because
    then the clerk cannot tell that a repeat is owed. `provisional_pending` is exactly the
    field that says so, and naming it keeps the rule checkable rather than a judgement about
    prose. (Pathway §4.3 has one node where the destinations genuinely must differ: a
    genuine EBER-negative with a passing control is what separates the non-reportable
    indolent NK-cell LPD of the GI tract from 9719, and an uninterpretable result must not
    inherit that exit. That case is caught by the destination half of the same rule.)

    `test_result_states` may be one object or an array of them, so a node that branches on
    two such tests can declare both rather than being failed for the second.
    """
    out = []
    blocks_seen = 0
    compared = 0

    for node_id, node in sorted(ctx.nodes.items()):
        loc = "node %s" % node_id
        declared = _declared_variables(node)
        raw = node.get("test_result_states")
        if raw is None:
            blocks = []
        elif isinstance(raw, list):
            blocks = raw
        else:
            blocks = [raw]

        declared_vars = set()
        for i, block in enumerate(blocks):
            label = ("test_result_states" if not isinstance(raw, list)
                     else "test_result_states[%d]" % i)
            if not isinstance(block, dict):
                out.append((FAIL, "%s: %s must be an object with 'variable' and 'states[]'"
                            % (loc, label)))
                continue
            blocks_seen += 1
            var = block.get("variable")
            if not isinstance(var, str) or not var.strip():
                out.append((FAIL, "%s: %s.variable is required and must be a non-empty "
                                  "string (contract §3.4)" % (loc, label)))
                var = None
            else:
                declared_vars.add(var)
                if var not in declared:
                    out.append((FAIL, "%s: %s.variable %r is not declared in this node's "
                                      "captured_variables[] (contract §5) — the states are "
                                      "offered and the answer has nowhere to go"
                                % (loc, label, var)))

            states = block.get("states")
            if not isinstance(states, list) or not states:
                out.append((FAIL, "%s: %s.states[] is required and must be non-empty "
                                  "(contract §3.4)" % (loc, label)))
                states = []
            for state in states:
                if not isinstance(state, str) or state not in TEST_RESULT_STATES:
                    out.append((FAIL, "%s: %s state %r is not in the closed vocabulary (%s) "
                                      "(contract §3.4)"
                                % (loc, label, state,
                                   " · ".join(sorted(TEST_RESULT_STATES)))))
            if var in UNINTERPRETABLE_TEST_VARIABLES and "not_assessable" not in states:
                out.append((FAIL, "%s: %s for %r omits 'not_assessable'. This test fails in "
                                  "a way that is neither positive nor negative, and with no "
                                  "state for it the clerk has to file an unreadable result "
                                  "as one of the two real answers (contract §3.4)"
                            % (loc, label, var)))

        # Which variables does this node actually branch on, and with which state?
        #
        # A `when` naming the variable is unambiguously a branch CONDITIONED on the test.
        # A `captures` merely RECORDS the answer the clerk gave, so one option that
        # happens to capture a variable is not the node branching on it — two or more
        # branches recording DIFFERENT states of it are. Without that distinction a node
        # with a single incidental capture would be failed for not declaring states it
        # does not actually offer, which is the false-FAIL that teaches the next author
        # to route around the validator.
        branched: dict = {}
        conditioned: set = set()
        for holder, where in _branch_containers(node):
            for source in ("when", "captures"):
                blob = holder.get(source)
                if isinstance(blob, dict):
                    for name, val in blob.items():
                        if isinstance(val, str):
                            branched.setdefault(name, []).append((val, holder, where))
                            if source == "when":
                                conditioned.add(name)
            # A node that declares ONE test variable may answer it with a per-branch
            # token instead of repeating the variable name on every option.
            for owner in declared_vars if len(declared_vars) == 1 else ():
                for key in ("value", "result", "state", "result_state"):
                    val = holder.get(key)
                    if isinstance(val, str) and val in TEST_RESULT_STATES:
                        branched.setdefault(owner, []).append((val, holder, where))
                        break

        def branches_on(name) -> bool:
            if name in conditioned:
                return True
            return len({val for val, _h, _w in branched.get(name, [])}) >= 2

        for var in sorted(UNINTERPRETABLE_TEST_VARIABLES & set(branched)):
            if not branches_on(var):
                continue
            if var not in declared_vars:
                out.append((FAIL, "%s branches on %r but declares no test_result_states for "
                                  "it. Every branch on this test has to offer "
                                  "'not_assessable', and the node has to say so where the "
                                  "engine can see it (contract §3.4)" % (loc, var)))

        for var in sorted(declared_vars | (UNINTERPRETABLE_TEST_VARIABLES & set(branched))):
            by_state: dict = {}
            for val, holder, where in branched.get(var, []):
                by_state.setdefault(val, []).append((holder, where))
            # One rule can record the same variable in BOTH a `when` and a `captures`,
            # which would otherwise pair it against itself and report the finding twice.
            def unique(entries):
                seen_ids, kept = set(), []
                for holder, where in entries:
                    if id(holder) not in seen_ids:
                        seen_ids.add(id(holder))
                        kept.append((holder, where))
                return kept

            negatives = unique(by_state.get("negative") or [])
            unreadables = unique(by_state.get("not_assessable") or [])
            if not negatives or not unreadables:
                continue
            compared += 1
            neg_by_sig: dict = {}
            for holder, where in negatives:
                sig = destination_signature(holder)
                if sig is not None:
                    neg_by_sig.setdefault(sig, []).append((holder, where))
            for holder, where in unreadables:
                sig = destination_signature(holder)
                if sig is None or sig not in neg_by_sig:
                    continue                       # different destination — distinguishable
                # Compared by CONTENT, not by presence. Both branches carrying a
                # provisional is the normal shape where one code has two open questions
                # at once — g2_matureB names MYC on both halves and adds "EBER control
                # failed, so EBV status is unestablished" on the not_assessable half.
                # That is precisely the distinction being asked for, so presence alone
                # would fail correct authoring; identical text on both halves would not
                # distinguish them at all.
                mine = _canonical(holder.get("provisional_pending"))
                if mine is not None and all(_canonical(n.get("provisional_pending")) != mine
                                            for n, _w in neg_by_sig[sig]):
                    continue                       # says out loud that a repeat is owed
                twin = neg_by_sig[sig][0][1]
                out.append((FAIL, "%s: the not_assessable branch for %r (%s) is "
                                  "indistinguishable from the negative branch (%s) — both "
                                  "land on %s, and the not_assessable branch carries no "
                                  "provisional_pending that says anything the negative "
                                  "branch does not. The same destination can be right (a "
                                  "code that needs POSITIVITY is unlocked by neither "
                                  "answer), but the two must not read the same: a clean "
                                  "negative means the workup is done, a failed control "
                                  "means a repeat on a fresh section is owed. Reported "
                                  "identically, the failed control is recorded as though "
                                  "the test had returned — the case looks better evidenced "
                                  "than it is. Either send not_assessable somewhere else, "
                                  "or give it a provisional_pending naming the repeat "
                                  "(contract §3.4, §6; Pathway §2.4, §4.3, §7.3 item 4)"
                            % (loc, var, where, twin, _destination_text(sig))))

    if [f for f in out if f[0] == FAIL]:
        return out
    if blocks_seen:
        out.append((OK, "%d test_result_states block(s) well formed; %d node/variable "
                        "pair(s) route not_assessable away from negative (contract §3.4)"
                    % (blocks_seen, compared)))
    else:
        out.append((NOTE, "no test_result_states block in this file — Group II construct, "
                          "nothing to check here"))
    return out


def check_entity_boundary(ctx: DTContext):
    """
    GROUP II CHECK 5 — `entity_boundary`, and the 9709 `/3` ban (contract §3.5).

    9709 only. Crossing this line does not flip a behaviour, it changes the entity and
    therefore the code: primary cutaneous CD4+ small/medium T-cell lymphoproliferative
    disorder (9709/1) on one side, peripheral T-cell lymphoma NOS (9702/3) on the other.
    The construct keeps that judgement in the JSON — the variable, the threshold, the
    operator, both codes and both reasons — instead of in a coding_note nobody renders.

    The second half runs over the WHOLE file whether or not any entity_boundary was
    authored: 9709 may never carry behavior_code "3" anywhere — branch, terminal,
    behaviour_resolution leaf, entity_boundary side or morphology_entries object. There is
    no 9709/3 in ICD-O-3. It is the single most likely invalid code this group can produce,
    because /1 is the unfamiliar half and "it is a lymphoproliferative disorder, so /3" is
    the reflex. Pathway §7.5 is explicit: 9709 must NOT get a /3 entry; out-of-boundary
    cases become 9702/3, which is a different code and not a re-behavioured 9709.
    """
    out = []
    pairs = _code_behavior_pairs(ctx)
    seen = 0

    for node_id, node in sorted(ctx.nodes.items()):
        declared = _declared_variables(node)
        for holder, where in walk_dicts(node):
            if "entity_boundary" not in holder:
                continue
            loc = "node %s (%s)" % (node_id, where or "(node level)")
            eb = holder["entity_boundary"]
            if not isinstance(eb, dict):
                out.append((FAIL, "%s: entity_boundary must be an object, got %r"
                            % (loc, eb)))
                continue
            seen += 1

            for key in ("variable", "reason_inside", "reason_outside"):
                val = eb.get(key)
                if not isinstance(val, str) or not val.strip():
                    out.append((FAIL, "%s: entity_boundary.%s is required and must be a "
                                      "non-empty string (contract §3.5)" % (loc, key)))

            var = eb.get("variable")
            if isinstance(var, str) and var and var not in declared:
                out.append((FAIL, "%s: entity_boundary.variable %r is not declared in this "
                                  "node's captured_variables[] (contract §5) — the boundary "
                                  "is authored but never actually tested"
                            % (loc, var)))

            threshold = eb.get("threshold")
            if isinstance(threshold, bool) or not isinstance(threshold, (int, float)):
                out.append((FAIL, "%s: entity_boundary.threshold is required and must be a "
                                  "number, got %r (contract §3.5)" % (loc, threshold)))

            operator = eb.get("operator")
            if operator not in ENTITY_BOUNDARY_OPERATORS:
                out.append((FAIL, "%s: entity_boundary.operator %r is not one of %s "
                                  "(contract §3.5)"
                            % (loc, operator,
                               " ".join(sorted(ENTITY_BOUNDARY_OPERATORS)))))

            also = eb.get("also_outside_when")
            if also is not None and (not isinstance(also, dict) or not also):
                out.append((FAIL, "%s: entity_boundary.also_outside_when, when present, must "
                                  "be a non-empty object (contract §3.5)" % loc))

            inside = as_code(eb.get("inside_code"))
            outside = as_code(eb.get("outside_code"))
            in_beh = eb.get("inside_behavior_code")
            out_beh = eb.get("outside_behavior_code")
            in_beh = None if in_beh is None else str(in_beh).strip()
            out_beh = None if out_beh is None else str(out_beh).strip()

            for side, code, beh in (("inside", inside, in_beh), ("outside", outside, out_beh)):
                if not code:
                    out.append((FAIL, "%s: entity_boundary.%s_code is required "
                                      "(contract §3.5)" % (loc, side)))
                    continue
                if beh is None:
                    out.append((FAIL, "%s: entity_boundary.%s_behavior_code is required — a "
                                      "code without an explicit behaviour is half a "
                                      "decision (contract §3.5)" % (loc, side)))
                    continue
                if (code, beh) not in pairs:
                    out.append((FAIL, "%s: entity_boundary %s side emits %s/%s, which has no "
                                      "morphology_entries[] object in this file "
                                      "(contract §3.5)" % (loc, side, code, beh)))

            if inside and outside and inside == outside:
                out.append((FAIL, "%s: entity_boundary.outside_code equals inside_code (%s). "
                                  "Crossing this boundary changes the ENTITY, not the "
                                  "behaviour — if both sides carry the same code the node "
                                  "asks a question whose answer cannot matter, and the "
                                  "out-of-entity case is coded as the entity it is not "
                                  "(contract §3.5)" % (loc, inside)))

    # -- the standalone assertion: no 9709/3 anywhere in the file ---------------------
    slash3 = []
    for holder, where in walk_dicts(ctx.data):
        for code_key, beh_key in (("morphology_code", "behavior_code"),
                                  ("inside_code", "inside_behavior_code"),
                                  ("outside_code", "outside_behavior_code"),
                                  ("refer_code", "behavior_code")):
            code = as_code(holder.get(code_key))
            beh = holder.get(beh_key)
            if code in NO_SLASH3_CODES and beh is not None and str(beh).strip() == "3":
                slash3.append("%s (%s)" % (where or "(top level)", code_key))
    for code in sorted(NO_SLASH3_CODES):
        if slash3:
            out.append((FAIL, "%s appears with behavior_code \"3\" at %d site(s): %s. There "
                              "is no %s/3 — Pathway §7.5 says in terms that %s must NOT get "
                              "a /3 entry, and contract §3.5 makes it the single most likely "
                              "invalid code this group can produce. An out-of-entity case is "
                              "9702/3 via entity_boundary, which is a DIFFERENT code, not a "
                              "re-behavioured %s"
                        % (code, len(slash3), ", ".join(sorted(set(slash3))), code, code,
                           code)))

    if [f for f in out if f[0] == FAIL]:
        return out
    banned = ", ".join(sorted(NO_SLASH3_CODES))
    if seen:
        out.append((OK, "%d entity_boundary block(s) well formed; no %s/3 anywhere in the "
                        "file (contract §3.5)" % (seen, banned)))
    else:
        out.append((OK, "no entity_boundary block in this file (Group II construct); the "
                        "standalone %s/3 ban holds across the whole file (contract §3.5)"
                    % banned))
    return out


def _node_edges(node):
    """
    Yield (target_node_id, chain) for every `next_node` anywhere inside a node.

    `chain` is the holder that carries the next_node plus all of its ancestors within the
    node, outermost first. Both path lints need the ancestors, not just the holder: an
    option that captures a result and then routes through a nested block would otherwise
    look like an edge that established nothing.
    """
    def rec(obj, chain):
        if isinstance(obj, dict):
            chain = chain + [obj]
            target = obj.get("next_node")
            if isinstance(target, str) and target:
                yield target, chain
            for value in obj.values():
                yield from rec(value, chain)
        elif isinstance(obj, list):
            for value in obj:
                yield from rec(value, chain)
    yield from rec(node, [])


def _node_code_sites(node):
    """Yield (code, chain, where) for every morphology_code emitted inside a node."""
    def rec(obj, chain, where):
        if isinstance(obj, dict):
            chain = chain + [obj]
            code = as_code(obj.get("morphology_code"))
            if code:
                yield code, chain, where or "(node level)"
            for key, value in obj.items():
                yield from rec(value, chain, "%s.%s" % (where, key) if where else key)
        elif isinstance(obj, list):
            for i, value in enumerate(obj):
                yield from rec(value, chain, "%s[%d]" % (where, i))
    yield from rec(node, [], "")


def _unproven_reachable(ctx: DTContext, roots, established) -> set:
    """
    The set of nodes some route reaches with a fact NOT yet established.

    `established(chain)` answers "does traversing this edge establish the fact?". Walk
    forward from the roots following only edges that do not, and every node still reached
    is a node reachable while the fact is still unproven. Shared by check_viral_gates()
    and check_burkitt_provisional(), which differ only in what counts as established.
    """
    seen = set(roots)
    stack = list(roots)
    while stack:
        current = stack.pop()
        for target, chain in _node_edges(ctx.nodes[current]):
            if target not in ctx.nodes or target in seen:
                continue
            if established(chain):
                continue
            seen.add(target)
            stack.append(target)
    return seen


def check_viral_gates(ctx: DTContext):
    """
    GROUP II CHECK 6 — the viral-gate lint (contract §6; Pathway §5.5).

    The Group II analogue of check_cryptic_genetics(), and the same class of defect: JSON
    that validates perfectly and records a diagnosis the file cannot support.

    Seven codes are DEFINITIONALLY viral — the virus is part of the entity, not an
    association noticed alongside it:

        9678, 9738        HHV-8 LANA-1 positive
        9827              HTLV-1 serology positive
        9719, 9724, 9725  EBER ISH positive
        9737              ALK IHC positive

    Reach one of them along a route where the virus result was never established positive
    and the registry gains a confirmed-looking diagnosis nobody confirmed. That is the
    evidence-overstatement class the contract puts above everything else (§6), and it is
    not JSON-Schema-checkable: it is a property of every PATH to the terminal, not of any
    one object, so it lives here as static analysis.

    Method, mirroring check_cryptic_genetics(): once per gated variable, walk forward from
    the tree entry nodes following only edges on which that variable is NOT established
    positive. Any node still reached is a node some route reaches with the virus unproven.
    A gated code emitted there, on a branch that does not itself establish the virus, is
    reachable unproven — FAIL.

    "Established positive" is read from the three places the contract allows the fact to
    be recorded (§3F, §5): a node-level `captures`, a branch `captures` or `when`, or a
    `positive[]` marker token naming the test — and from any ancestor of the branch within
    the node, so that a captured option routing through a nested block still counts.
    Variable-name aliases are accepted so that a correct file is never failed over
    spelling: Group 1 gates this very same 9827 terminal on `htlv1_status` where the Group
    II vocabulary says `htlv1_serology`, and they are one clinical fact.

    A variable merely LISTED as captured is not a positive result. That distinction is the
    whole lint: "we asked about EBV" and "EBV is present" are the two things this check
    refuses to let collapse into each other.
    """

    def establishes(holder, var) -> bool:
        if not isinstance(holder, dict):
            return False
        aliases = VIRAL_GATE_VARIABLES[var]
        for key in ("captures", "when"):
            blob = holder.get(key)
            if isinstance(blob, dict):
                for name, val in blob.items():
                    if name in aliases and _is_positive_result(val):
                        return True
        tokens = holder.get("positive")
        if isinstance(tokens, list):
            markers = VIRAL_GATE_MARKERS[var]
            for token in tokens:
                if isinstance(token, str) \
                        and token.split(":")[0].strip().upper() in markers:
                    return True
        return False

    def establishes_chain(chain, var) -> bool:
        return any(establishes(h, var) for h in chain)

    emissions = []          # (code, var, chain, node_id, where)
    for node_id, node in sorted(ctx.nodes.items()):
        for code, chain, where in _node_code_sites(node):
            var = VIRAL_GATED_CODES.get(code)
            if var:
                emissions.append((code, var, chain, node_id, where))
        fallback = node.get("nos_fallback")
        if isinstance(fallback, dict):
            code = as_code(fallback.get("code"))
            var = VIRAL_GATED_CODES.get(code)
            if var:
                emissions.append((code, var, [node, fallback], node_id, "nos_fallback"))

    if not emissions:
        return [(NOTE, "no viral-gated terminal (%s) emitted in this file — lint has "
                 "nothing to check" % ", ".join(sorted(VIRAL_GATED_CODES)))]

    roots = [e for e in ctx.entry_nodes() if e in ctx.nodes]
    if not roots:
        return [(NOTE, "no tree entry node resolves in this file — viral-gate lint skipped "
                       "(check_orphan_nodes reports the real problem)")]

    out = []
    cache: dict = {}
    proven = []
    for code, var, chain, node_id, where in emissions:
        if var not in cache:
            cache[var] = _unproven_reachable(
                ctx, roots, lambda chain, v=var: establishes_chain(chain, v))
        if node_id in cache[var] and not establishes_chain(chain, var):
            out.append((FAIL, "viral-gated terminal %s is emitted at %s (%s) on a route "
                              "where %s was never established positive. %s is "
                              "DEFINITIONALLY viral — the virus is part of the entity, not "
                              "an association found beside it — so a case coded here "
                              "without the result reads as a confirmed diagnosis that "
                              "nothing in the file supports (contract §6; Pathway §5.5). "
                              "Capture %s positive on every route that reaches it (a node "
                              "or branch `captures`, a `when`, or a `positive[]` marker), or "
                              "send the untested case to the NOS fallback instead."
                        % (code, node_id, where, VIRAL_GATE_LABELS[var], code,
                           VIRAL_GATE_LABELS[var])))
        else:
            proven.append(code)

    if not out:
        out.append((OK, "viral-gated terminal(s) %s reachable only where %s established "
                        "positive (contract §6)"
                    % (", ".join(sorted(set(proven))),
                       "the gating test is" if len(set(proven)) == 1
                       else "their gating tests are")))
    return out


def _is_positive_result(value) -> bool:
    """A recorded test result that means POSITIVE — not merely 'this was captured'."""
    if value is True:
        return True
    if isinstance(value, str):
        return value.strip().lower().replace("-", "_") in POSITIVE_RESULT_TOKENS
    return False




def _resolved_result(value):
    """
    Classify a recorded test result: True = it came back, False = it did not, None =
    neither list recognises it.

    The three-way answer matters. A value in neither vocabulary is ACCEPTED as a result
    (failing closed here would fail correct files over an unfamiliar but honest label) and
    is reported as a NOTE naming the value, so a typo that silently discharges the
    requirement is visible instead of invisible.
    """
    if value is True:
        return True
    if value is False or value is None:
        return False
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, list):
        return any(_resolved_result(v) for v in value)
    if not isinstance(value, str):
        return None
    token = value.strip().lower().replace("-", "_").replace(" ", "_")
    if not token:
        return False
    if token in UNRESOLVED_RESULT_TOKENS:
        return False
    if token in RESOLVED_RESULT_TOKENS:
        return True
    return None


def check_burkitt_provisional(ctx: DTContext):
    """
    GROUP II CHECK 7 — the under-determined-code lint (Pathway §4.2; contract §3.2, §6).

    Pathway §4.2 states a POLICY, not a preference: "a 'morphology + IHC provisional, FISH
    pending' tier with an explicit named flag, not silent absorption. Every 9687 assigned
    without FISH carries 'MYC status unknown; HG/LBCL-11q and HGBL-DH not excluded'."

    Two entities are phenotypically indistinguishable from Burkitt lymphoma and are
    separated from it only by FISH — high-grade/large B-cell lymphoma with 11q aberration,
    and B-ALL with MYC rearrangement. Where FISH is unavailable they are absorbed into
    9687, and nothing on the screen says so. In a malaria-endemic, high-EBV setting Burkitt
    is the commonest childhood cancer, which makes this the single highest-VOLUME way this
    group can record a diagnosis firmer than its evidence. It is the same defect class as
    check_viral_gates(), at perhaps a hundred times the case count.

    The rule: 9687 may not be reachable by any route on which no FISH/molecular result was
    established, UNLESS the emitting branch carries a `provisional_pending`. A branch that
    carries one is compliant whatever its route — it has said out loud what it does not
    know, which is the whole of what the policy asks for.

    A result counts as ESTABLISHED when any of these appears on the route (the emitting
    branch, an ancestor of it within the node, or any edge traversed to reach the node):
      * a FISH_EVIDENCE_VARIABLES variable in a `captures` or a `when`, set to a value
        that came back — `not_done`, `none`, `failed`, `not_available`, `not_indicated`
        and `not_assessable` do NOT count, which is the point: a FISH that did not
        hybridise established nothing;
      * `satisfies_tests` naming Cytogenetics/FISH or Molecular/PCR;
      * an evidence-tier capture — a captured LIST containing one of those test names;
      * a cytogenetic `detection_method` that involves FISH.
    MYC IHC is deliberately not evidence: Pathway §4.2 and §5.1 keep an explicit 30-50%
    indeterminate band because the stain does not settle what the FISH settles.

    The rule is generalised over UNDERDETERMINED_CODES rather than hard-coded to 9687, so
    the same policy covers 9680, where LBCL-IRF4 is absorbed and the over-treatment of a
    curable head-and-neck disease follows. That arm is CONTEXT-GATED — Pathway §4.2 asks
    for the flag on "every 9680 in a child with localised head-and-neck disease", not on
    every 9680, and 9680 is also the mature-B NOS fallback (contract §4.2), where an
    unconditional rule would fire on every unresolved large-cell case. Pathway §5.1 defines
    no head-and-neck site variable, so that arm is armed against anticipated names; when it
    finds no such context anywhere in the file it says so as a NOTE rather than passing
    quietly, because a rule that can never fire is a hole.

    A `nos_fallback` object is covered too — contract §4.2 lets the FISH node fall back to
    "the code that entered the node", which is exactly a FISH-less 9687 — but it has no
    `provisional_pending` slot in its {code, name, reason} shape. There the named flag has
    to live in the `reason`, which app.js does render, so the reason must at least name
    what is unresolved.
    """
    out = []

    roots = [e for e in ctx.entry_nodes() if e in ctx.nodes]
    unknown_values: dict = {}

    def evidence_in(holder) -> bool:
        if not isinstance(holder, dict):
            return False
        for key in ("captures", "when"):
            blob = holder.get(key)
            if not isinstance(blob, dict):
                continue
            for name, value in blob.items():
                # an evidence-tier capture: a list naming the modality outright
                if isinstance(value, list) and any(
                        isinstance(v, str) and v in FISH_SATISFYING_TESTS for v in value):
                    return True
                if name not in FISH_EVIDENCE_VARIABLES:
                    continue
                verdict = _resolved_result(value)
                if verdict is None:
                    if name in FISH_PANEL_VARIABLES:
                        return True          # a panel name, not a result token
                    unknown_values.setdefault(name, set()).add(str(value))
                    return True
                if verdict:
                    return True
        satisfies = holder.get("satisfies_tests")
        if isinstance(satisfies, list) and any(v in FISH_SATISFYING_TESTS
                                               for v in satisfies if isinstance(v, str)):
            return True
        if holder.get("detection_method") in FISH_DETECTION_METHODS:
            return True
        return False

    def evidence_on(chain) -> bool:
        return any(evidence_in(h) for h in chain)

    def context_in(holder) -> bool:
        if not isinstance(holder, dict):
            return False
        for key in ("captures", "when"):
            blob = holder.get(key)
            if not isinstance(blob, dict):
                continue
            for name, value in blob.items():
                if name not in HEAD_AND_NECK_CONTEXT_VARIABLES:
                    continue
                values = value if isinstance(value, list) else [value]
                for v in values:
                    if isinstance(v, str) and v.strip().lower().replace("-", "_").replace(
                            " ", "_") in HEAD_AND_NECK_CONTEXT_VALUES:
                        return True
        return False

    def context_on(chain) -> bool:
        return any(context_in(h) for h in chain)

    # -- every site that emits one of the covered codes -------------------------------
    sites = []          # (code, chain, node_id, where, is_fallback)
    for node_id, node in sorted(ctx.nodes.items()):
        for code, chain, where in _node_code_sites(node):
            if code in UNDERDETERMINED_CODES:
                sites.append((code, chain, node_id, where, False))
        fallback = node.get("nos_fallback")
        if isinstance(fallback, dict):
            code = as_code(fallback.get("code"))
            if code in UNDERDETERMINED_CODES:
                sites.append((code, [node, fallback], node_id, "nos_fallback", True))

    if not sites:
        return [(NOTE, "no under-determined terminal (%s) emitted in this file — lint has "
                 "nothing to check" % ", ".join(sorted(UNDERDETERMINED_CODES)))]
    if not roots:
        return [(NOTE, "no tree entry node resolves in this file — under-determined-code "
                       "lint skipped (check_orphan_nodes reports the real problem)")]

    unproven = _unproven_reachable(ctx, roots, evidence_on)
    # Nodes some route reaches while the head-and-neck context HAS been established.
    in_context = {n for n in ctx.nodes
                  if n not in _unproven_reachable(ctx, roots, context_on)}

    context_arms_tested = set()
    compliant = []
    for code, chain, node_id, where, is_fallback in sites:
        rule = UNDERDETERMINED_CODES[code]
        if rule["context"] is not None:
            if node_id not in in_context and not context_on(chain):
                continue                       # this arm does not apply on this route
            context_arms_tested.add(code)

        if evidence_on(chain) or node_id not in unproven:
            compliant.append(code)
            continue

        if is_fallback:
            reason = chain[-1].get("reason")
            text = reason.lower() if isinstance(reason, str) else ""
            if any(tok in text for tok in rule["reason_tokens"]):
                compliant.append(code)
                continue
            out.append((FAIL, "node %s: the nos_fallback emits %s (%s) on a route where no "
                              "FISH or molecular result was established, and its 'reason' "
                              "does not name what is unresolved. %s absorbs %s when the "
                              "test never returns, and Pathway §4.2 requires an explicit "
                              "named flag rather than silent absorption. A nos_fallback has "
                              "no provisional_pending slot, so its rendered 'reason' must "
                              "carry the flag — say %r."
                        % (node_id, code, rule["label"], code, rule["absorbed"],
                           rule["flag"])))
            continue

        if isinstance(chain[-1].get("provisional_pending"), dict) or any(
                isinstance(h.get("provisional_pending"), dict) for h in chain):
            compliant.append(code)
            continue

        out.append((FAIL, "under-determined terminal %s (%s) is emitted at %s (%s) on a "
                          "route where no FISH or molecular result was established, and the "
                          "branch carries no provisional_pending. Without the test, %s "
                          "absorbs %s, and the case is recorded as a settled diagnosis with "
                          "nothing on screen saying what was never excluded — the "
                          "highest-volume version of that defect in this group "
                          "(Pathway §4.2; contract §3.2, §6). Either establish the result "
                          "on the route, or add a provisional_pending whose reason is %r "
                          "and whose resolving_test is 'Cytogenetics/FISH'."
                    % (code, rule["label"], node_id, where, code, rule["absorbed"],
                       rule["flag"])))

    if unknown_values:
        out.append((NOTE, "%d FISH-evidence value(s) are in neither the resolved nor the "
                          "unresolved vocabulary and were ACCEPTED as a returned result. "
                          "If any of these is a typo it is silently discharging the FISH "
                          "requirement: %s"
                    % (sum(len(v) for v in unknown_values.values()),
                       "; ".join("%s=%s" % (k, "/".join(sorted(v)))
                                 for k, v in sorted(unknown_values.items())))))

    for code, rule in sorted(UNDERDETERMINED_CODES.items()):
        if rule["context"] is None or code not in {c for c, *_ in sites}:
            continue
        if code not in context_arms_tested:
            out.append((NOTE, "the %s arm is context-gated on %s and no route in this file "
                              "establishes that context, so it tested nothing. Pathway §5.1 "
                              "defines no head-and-neck site variable; if the tree records "
                              "one under a name outside %s, add it to "
                              "HEAD_AND_NECK_CONTEXT_VARIABLES or this rule stays inert."
                        % (code, rule["context"],
                           ", ".join(sorted(HEAD_AND_NECK_CONTEXT_VARIABLES)))))

    if not [f for f in out if f[0] == FAIL]:
        if compliant:
            out.append((OK, "under-determined terminal(s) %s: every route either "
                            "establishes a FISH/molecular result or carries the named "
                            "provisional (Pathway §4.2)"
                        % ", ".join(sorted(set(compliant)))))
        else:
            out.append((NOTE, "no route reaches an under-determined terminal under the "
                              "conditions this lint governs — nothing to check"))
    return out


# --------------------------------------------------------------------------------------
# B4c. Group III schema extensions (docs/group_03_build_contract.md §2, §5, §6).
#
# Fourteen validation rules. Each check below names the rule it enforces.
#
# SCOPE. Every check here is a no-op on a file that does not use the field it is about:
# it returns NOTHING at all rather than an OK or a NOTE, so Groups 1 and 2 report exactly
# what they reported before this block existed. The rules that are Group III AMENDMENTS
# to an existing construct — band-level `unit` (rule 4), the behaviour split (rule 6), the
# topography map (rule 12), the ICD-O-3.2 round-trip (rule 13) — are gated on
# `ctx.group == GROUP3`, read off the FILENAME and cross-checked against metadata.group_id
# by check_top_level_keys(). That is a structural fact about which file is being read, not
# a flag inside it (rule 8).
# --------------------------------------------------------------------------------------

_ICDO32_CACHE: dict = {}
_ICCC3_CACHE: dict = {}


def _icdo32_path(layer1):
    env = os.environ.get("ICDO_DB")
    if env:
        return Path(env)
    if layer1 is None:
        return None
    return Path(layer1) / "ICD-O-3.2" / "icdo32.sqlite"


def _iccc_path(layer1):
    env = os.environ.get("ICCC_DB")
    if env:
        return Path(env)
    if layer1 is None:
        return None
    # ICCC-2017.sqlite sits beside the Layer 1 directory, not inside it.
    return Path(layer1).parent / "ICCC-2017.sqlite"


def load_icdo32(layer1):
    """
    ICD-O-3.2 as the tool must see it: {(code4, behaviour): {term: level}}.

    Read-only, cached per path. This is the ANCHOR for rule 8 — every name check keys
    off this and off nothing in the file being checked. Returns (index, error_or_None).
    """
    path = _icdo32_path(layer1)
    if path is None:
        return {}, "no Layer 1 directory, so icdo32.sqlite cannot be located"
    key = str(path)
    if key in _ICDO32_CACHE:
        return _ICDO32_CACHE[key]
    if not path.exists():
        result = ({}, "icdo32.sqlite not found at %s" % path)
        _ICDO32_CACHE[key] = result
        return result
    index: dict = {}
    try:
        con = sqlite3.connect("file:%s?mode=ro" % path, uri=True)
        try:
            for code4, behaviour, level, term, obs in con.execute(
                    "SELECT code4, behaviour, level, term, obs FROM icd_o_3_2_morphology "
                    "WHERE code4 IS NOT NULL AND behaviour IS NOT NULL AND term IS NOT NULL"):
                index.setdefault((str(code4), str(behaviour)), {})[str(term)] = (
                    str(level or ""), str(obs or ""))
        finally:
            con.close()
    except sqlite3.Error as exc:
        result = ({}, "icdo32.sqlite could not be read: %s" % exc)
        _ICDO32_CACHE[key] = result
        return result
    result = (index, None)
    _ICDO32_CACHE[key] = result
    return result


def _topo_from_raw(raw):
    """'723' -> 'C72.3'. The ICCC table stores topography as three digits."""
    n = int(raw)
    return "C%02d.%d" % (n // 10, n % 10)


def load_iccc_group3(layer1):
    """
    {code: {subgroup_id: (subgroup_name, set(topography codes))}} for ICCC main group III,
    restricted to the topography this group can carry. Returns (index, error_or_None).

    This is the anchor for `iccc3_subgroup_by_topography[]` (contract §1.3): ICCC-2017
    itself says which subgroup a (code, topography) pair belongs to, so a routing rule is
    checked against the recode table rather than against the author's intention.
    """
    path = _iccc_path(layer1)
    if path is None:
        return {}, "no Layer 1 directory, so ICCC-2017.sqlite cannot be located"
    key = str(path)
    if key in _ICCC3_CACHE:
        return _ICCC3_CACHE[key]
    if not path.exists():
        result = ({}, "ICCC-2017.sqlite not found at %s" % path)
        _ICCC3_CACHE[key] = result
        return result
    sweep = set(GROUP3_TOPOGRAPHY_SWEEP)
    index: dict = {}
    try:
        con = sqlite3.connect("file:%s?mode=ro" % path, uri=True)
        try:
            rows = con.execute(
                "SELECT mc.code, g.group_code, g.group_label, cr.range_id "
                "FROM morphology_codes mc "
                "JOIN groups g ON g.group_id = mc.group_id "
                "JOIN code_ranges cr ON cr.range_id = mc.range_id "
                "WHERE g.main_group = 'III'").fetchall()
            segs: dict = {}
            for range_id, start_raw, end_raw in con.execute(
                    "SELECT range_id, start_raw, end_raw FROM topography_segments"):
                covered = segs.setdefault(range_id, set())
                for n in range(int(start_raw), int(end_raw) + 1):
                    topo = _topo_from_raw(n)
                    if topo in sweep:
                        covered.add(topo)
        finally:
            con.close()
    except (sqlite3.Error, ValueError) as exc:
        result = ({}, "ICCC-2017.sqlite could not be read: %s" % exc)
        _ICCC3_CACHE[key] = result
        return result
    for code, subgroup_id, subgroup_label, range_id in rows:
        name, covered = index.setdefault(str(code), {}).setdefault(
            str(subgroup_id), (str(subgroup_label), set()))
        covered |= segs.get(range_id, set())
    result = (index, None)
    _ICCC3_CACHE[key] = result
    return result


def _g3_holders(ctx: DTContext):
    """
    Yield (holder, location, node) for every dict in the file that a Group III field can
    hang off — inside a node, or inside a morphology_entries[] object. `node` is the
    enclosing node or None, so a check can look at its captured_variables[].
    """
    for node_id, node in sorted(ctx.nodes.items()):
        for holder, where in walk_dicts(node):
            yield holder, "node %s (%s)" % (node_id, where or "(node level)"), node
    for i, entry in enumerate(ctx.entries):
        if not isinstance(entry, dict):
            continue
        label = as_code(entry.get("morphology_code")) or "index %d" % i
        for holder, where in walk_dicts(entry):
            yield holder, "entry %s (%s)" % (label, where or "(entry level)"), None


def _loose(text) -> str:
    """Case-, whitespace- and punctuation-insensitive form, for NEAR-MISS reporting only.

    Never for deciding whether a name matches: the whole point of rules 8 and 13 is that
    a trailing space, a hyphen written as a space and `tumour` for `tumor` are all real
    defects. This exists so that when one of them FAILs, the message can say which string
    the author almost certainly meant.
    """
    if not isinstance(text, str):
        return ""
    t = text.lower().replace("tumour", "tumor")
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return " ".join(t.split())


def _nearest(target, candidates):
    """The candidate whose loose form equals the target's, or None."""
    want = _loose(target)
    if not want:
        return None
    for cand in candidates:
        if _loose(cand) == want:
            return cand
    return None


# -- rule 1, rule 2 — diagnosis_rendering ------------------------------------------------

def _result_tokens(holder):
    """Every result-ish token a branch records, lowercased and underscored."""
    tokens = set()

    def take(value):
        if isinstance(value, str):
            tokens.add(value.strip().lower().replace(" ", "_").replace("-", "_"))
        elif isinstance(value, bool):
            tokens.add("true" if value else "false")

    for field in ("when", "captures"):
        block = holder.get(field)
        if isinstance(block, dict):
            for value in block.values():
                if isinstance(value, list):
                    for v in value:
                        take(v)
                else:
                    take(value)
    for field in ("specimen_adequacy", "result", "test_result", "adequacy"):
        take(holder.get(field))
    return tokens


def _asserts_adequate_result(holder):
    """
    (asserts, disqualifier). Rule 2: a branch may emit `suffix: "nec"` only where it also
    asserts that an adequate result was OBTAINED. cIMPACT-NOW update 1 makes NEC a
    statement that the test was done and the tumour did not fit any WHO type — so a
    registry that could not do the test can never legitimately reach it, and a branch
    reached BECAUSE the test failed reaches it wrongly.
    """
    if not isinstance(holder, dict):
        return False, None
    tokens = _result_tokens(holder)
    blocked = sorted(tokens & UNRESOLVED_RESULT_TOKENS)
    if blocked:
        return False, blocked[0]
    if holder.get("adequate_result") is True or holder.get("result_adequate") is True:
        return True, None
    if tokens & RESOLVED_RESULT_TOKENS:
        return True, None
    for field in ("positive", "negative"):
        if isinstance(holder.get(field), list) and holder[field]:
            return True, None
    st = holder.get("satisfies_tests")
    if isinstance(st, list) and st:
        return True, None
    return False, None


def check_diagnosis_rendering(ctx: DTContext):
    """
    RULES 1 and 2 — `diagnosis_rendering` (contract §2(1), §6 rules 1-2).

    Rule 1 is the numeral invariant: `track == "who_cns5"` iff `grade_system == "arabic"`.
    It is not cosmetic. The two tracks are two different CLAIMS — a WHO CNS5 diagnosis and
    an ADAPTR descriptive diagnosis — and the numeral system is the only thing on the
    printed line that distinguishes them. A Roman numeral against a `who_cns5` track, or an
    Arabic one against `adaptr_descriptive`, tells the reader the registry reached a
    diagnosis it did not reach. Contract §2(4) records where this goes wrong in practice:
    the numeral follows the TRACK, never the evidence type, and CNS5 grades meningioma and
    subependymoma on histology alone — so the two commonest histology-only branches in the
    group are exactly the ones an author will get backwards.

    Rule 2 is the NEC gate, and it is the same failure in a different field. NEC means the
    test was done and the tumour fitted no WHO type. A branch reached because the test was
    not done, failed, or was unavailable has no standing to say that.
    """
    out, seen = [], 0
    for holder, loc, node in _g3_holders(ctx):
        if "diagnosis_rendering" not in holder:
            continue
        dr = holder["diagnosis_rendering"]
        if not isinstance(dr, dict):
            out.append((FAIL, "%s: diagnosis_rendering must be an object, got %r"
                        % (loc, dr)))
            continue
        seen += 1

        track = dr.get("track")
        if track not in CNS5_TRACKS:
            out.append((FAIL, "%s: diagnosis_rendering.track is %r — required, and one of "
                              "%s (contract §2(1))"
                        % (loc, track, ", ".join(sorted(CNS5_TRACKS)))))

        gs = dr.get("grade_system")
        if gs is not None and gs not in GRADE_SYSTEMS:
            out.append((FAIL, "%s: diagnosis_rendering.grade_system is %r — one of %s"
                        % (loc, gs, ", ".join(sorted(GRADE_SYSTEMS)))))

        # RULE 1, both directions off one table.
        if track in TRACK_GRADE_SYSTEM:
            want = TRACK_GRADE_SYSTEM[track]
            if gs != want:
                out.append((FAIL, "%s: RULE 1 — track %r requires grade_system %r, got %r. "
                                  "The numeral system follows the TRACK, never the "
                                  "evidence type (contract §2(4)): a grade reached on "
                                  "histology alone is still Arabic when the diagnosis is a "
                                  "WHO CNS5 diagnosis. Printed the other way round, the "
                                  "line claims a diagnosis the registry did not reach"
                            % (loc, track, want, gs)))
        elif gs in ("arabic", "roman"):
            other = [t for t, g in TRACK_GRADE_SYSTEM.items() if g == gs]
            out.append((FAIL, "%s: RULE 1 — grade_system %r with no valid track; %s is the "
                              "only track that may carry it" % (loc, gs, other[0])))

        # §2(1) — the per-track shape.
        if track in TRACK_FIELD_SHAPE:
            required, forbidden = TRACK_FIELD_SHAPE[track]
            for field in required:
                if dr.get(field) in (None, ""):
                    out.append((FAIL, "%s: track %r requires a non-null %r (contract §2(1))"
                                % (loc, track, field)))
            for field in forbidden:
                if dr.get(field) not in (None,):
                    out.append((FAIL, "%s: track %r requires %r to be null, got %r — a "
                                      "branch that fills both halves prints two different "
                                      "diagnoses for one case (contract §2(1))"
                                % (loc, track, field, dr.get(field))))

        # §2(1) / rule 9 — grade is a string or null, never a placeholder.
        if "grade" in dr:
            grade = dr["grade"]
            if grade is None:
                pass
            elif not isinstance(grade, str):
                out.append((FAIL, "%s: diagnosis_rendering.grade must be a string or null, "
                                  "got %r (contract §2(1))" % (loc, grade)))
            elif grade.strip() in GRADE_NON_VALUES or grade != grade.strip():
                out.append((FAIL, "%s: diagnosis_rendering.grade is %r. A grade is a string "
                                  "or null — never \"NA\", never \"\". A placeholder "
                                  "renders as a grade nobody assigned (contract §2(1))"
                            % (loc, grade)))
            elif gs == "arabic" and grade not in ARABIC_GRADES:
                out.append((FAIL, "%s: grade %r is not in the Arabic set %s (contract §2(1) "
                                  "— CNS5 Table 3 grades MVNT, PLNTY, meningioma and "
                                  "diffuse astrocytoma MYB/MYBL1-altered at 1, so 1 is in "
                                  "the set)" % (loc, grade, sorted(ARABIC_GRADES))))
            elif gs == "roman" and grade not in ROMAN_GRADES:
                out.append((FAIL, "%s: grade %r is not in the Roman set %s — the ADAPTR "
                                  "descriptive scale runs II-IV only (contract §2(1))"
                            % (loc, grade, sorted(ROMAN_GRADES))))

        # RULE 2 — the NEC gate.
        suffix = dr.get("suffix")
        if suffix is not None and suffix not in DIAGNOSIS_SUFFIXES:
            out.append((FAIL, "%s: diagnosis_rendering.suffix is %r — one of %s"
                        % (loc, suffix, ", ".join(sorted(DIAGNOSIS_SUFFIXES)))))
        elif suffix == "nec":
            asserts, blocker = _asserts_adequate_result(holder)
            if not asserts and node is not None and holder is node:
                asserts, blocker = _asserts_adequate_result(node)
            if blocker:
                out.append((FAIL, "%s: RULE 2 — suffix \"nec\" on a branch reached on %r. "
                                  "NEC says the test WAS done and the tumour fitted no WHO "
                                  "type (cIMPACT-NOW update 1). A branch reached because "
                                  "the test did not return cannot say that — it is a NOS, "
                                  "and a registry that cannot do the test can never "
                                  "legitimately emit NEC (contract §2(1), §6 rule 2)"
                            % (loc, blocker)))
            elif not asserts:
                out.append((FAIL, "%s: RULE 2 — suffix \"nec\" on a branch that asserts no "
                                  "adequate result. NEC is a positive claim that the test "
                                  "was done and returned; the branch must record the "
                                  "result it rests on (a `when`/`captures` naming a "
                                  "resolved state, an `adequate_result: true`, a marker "
                                  "list, or a satisfies_tests). Without it the label is "
                                  "unearned (contract §2(1), §6 rule 2)"
                            % loc))

    # `and not out` is load-bearing. Without it a check that has found something but not
    # yet incremented its counter throws the finding away — which is how a check comes to
    # confirm the very error it exists to catch (data.md §5A). Two of the rules here fire
    # precisely when the construct is ABSENT.
    if not seen and not out:
        return []
    if [f for f in out if f[0] == FAIL]:
        return out
    out.append((OK, "%d diagnosis_rendering block(s): every track carries its own numeral "
                    "system (rule 1) and every \"nec\" suffix rests on an asserted adequate "
                    "result (rule 2)" % seen))
    return out


# -- rule 3 — resource_level_gate --------------------------------------------------------

def check_resource_level_gate(ctx: DTContext):
    """
    RULE 3 — `resource_level_gate` (contract §2(2), §6 rule 3).

    `family` is required because a resource level is computed PER TUMOUR FAMILY, never per
    site: a laboratory with GFAP, synaptophysin and INI1 is RL III for AT/RT and RL II for
    ependymoma, and a site-level RL reads one of those two as the other.

    The rule the check is named for is the tier enum. Satgunaseelan's ependymoma tables use
    only `can_be_considered` and `highly_recommended`; `obligatory` on an ependymal node is
    a third value the source does not have, and it mis-renders every node in the family.

    `rl_assignment: "by_analogy"` is the overstatement guard. Where the family has no
    ADAPTR paper the resource level is borrowed, and a borrowed level presented as a
    sourced one is the class of defect this tool exists to keep out.
    """
    out, seen = [], 0
    for holder, loc, _node in _g3_holders(ctx):
        if "resource_level_gate" not in holder:
            continue
        gate = holder["resource_level_gate"]
        if not isinstance(gate, dict):
            out.append((FAIL, "%s: resource_level_gate must be an object, got %r"
                        % (loc, gate)))
            continue
        seen += 1

        family = gate.get("family")
        if not isinstance(family, str) or not family.strip():
            out.append((FAIL, "%s: resource_level_gate.family is REQUIRED — a resource "
                              "level is computed per tumour family, never per site "
                              "(contract §2(2))" % loc))
            family = None
        elif family not in RL_FAMILIES:
            out.append((FAIL, "%s: resource_level_gate.family %r is not in the closed "
                              "vocabulary %s (contract §2(2))"
                        % (loc, family, ", ".join(sorted(RL_FAMILIES)))))
            family = None

        rl = gate.get("required_rl")
        if rl not in RL_LEVELS:
            out.append((FAIL, "%s: resource_level_gate.required_rl is %r — one of %s "
                              "(contract §2(2))"
                        % (loc, rl, ", ".join(sorted(RL_LEVELS, key=len)))))

        for key in ("tier", "referral_tier"):
            if key not in gate:
                continue
            tier = gate.get(key)
            if tier not in RL_TIERS:
                out.append((FAIL, "%s: resource_level_gate.%s is %r — one of %s "
                                  "(contract §2(2))"
                            % (loc, key, tier, ", ".join(sorted(RL_TIERS)))))
                continue
            allowed = RL_TIERS_BY_FAMILY.get(family)
            if allowed is not None and tier not in allowed:
                out.append((FAIL, "%s: RULE 3 — %s %r on a node in the %s family. "
                                  "Satgunaseelan "
                                  "uses only %s for this family, so a third value has no "
                                  "source behind it and a three-value enum mis-renders "
                                  "every %s node (contract §2(2), §6 rule 3)"
                            % (loc, key, tier, family, " and ".join(sorted(allowed)),
                               family)))

        assignment = gate.get("rl_assignment")
        if assignment is not None and assignment not in RL_ASSIGNMENT_VALUES:
            out.append((FAIL, "%s: resource_level_gate.rl_assignment is %r — one of %s"
                        % (loc, assignment, ", ".join(sorted(RL_ASSIGNMENT_VALUES)))))
        elif family in RL_FAMILIES_WITHOUT_ADAPTR and assignment != "by_analogy":
            out.append((FAIL, "%s: the %s family has no ADAPTR paper behind it, so the "
                              "node must carry \"rl_assignment\": \"by_analogy\" (it is "
                              "%r). Presenting a borrowed resource level as a sourced one "
                              "makes the case look better evidenced than it is "
                              "(contract §2(2))" % (loc, family, assignment)))

        dest = gate.get("unreachable_destination")
        if dest is not None:
            if not isinstance(dest, dict):
                out.append((FAIL, "%s: resource_level_gate.unreachable_destination must be "
                                  "an object, got %r" % (loc, dest)))
            else:
                code = as_code(dest.get("morphology_code"))
                beh = dest.get("behavior_code")
                beh = None if beh is None else str(beh).strip()
                if code and (code, beh) not in _code_behavior_pairs(ctx):
                    out.append((FAIL, "%s: resource_level_gate.unreachable_destination "
                                      "emits %s/%s, which has no morphology_entries[] "
                                      "object in this file — the branch the clerk is sent "
                                      "to when the test is unavailable does not exist"
                                % (loc, code, beh)))

        # Unavailability is a property of a DECLARED site profile, never of the
        # required level on its own. A site declared resource level V meets a
        # requirement of resource level V, so "required_rl is V" is not evidence
        # that any laboratory cannot run the test — and this tool is used by
        # registries anywhere, not built around one site's inventory. The old
        # rule here asserted the opposite and forced the engine to print "the
        # test is unavailable" at every RL V branch regardless of the site.
        # Corrected 14 September 2026; the flag it policed is now banned outright.
        if "upgrade_line_says_unavailable" in gate:
            out.append((FAIL, "%s: resource_level_gate carries "
                              "\"upgrade_line_says_unavailable\", which asserts a laboratory "
                              "cannot run a test from the required level alone. Unavailability "
                              "follows from a declared site_profile level BELOW the requirement "
                              "and from nothing else; with no profile the honest output is "
                              "\"not established\". Remove the key" % loc))

    if not seen and not out:
        return []
    if [f for f in out if f[0] == FAIL]:
        return out
    out.append((OK, "%d resource_level_gate(s): every one names its family, no ependymal "
                    "node carries tier \"obligatory\" (rule 3), and every family without "
                    "an ADAPTR paper declares rl_assignment \"by_analogy\"" % seen))
    return out


# -- rule 5 — entity_annotation ----------------------------------------------------------

def _cns5_reference_list(repo: Path):
    """
    (entities, provisional_flags, source). The transcribed CNS5 Table 1 this repo carries.

    `provisional_flags` is {entity: bool} where the transcription records it, so §2(3)'s
    `provisional` field can be checked against Table 1 rather than against the author's
    reading of the italics that produced the "(provisional type)" artefact in the first
    place.
    """
    for rel in CNS5_TABLE1_REFERENCE_FILES:
        path = Path(repo) / rel
        if not path.exists():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if path.suffix != ".json":
            lines = [ln.rstrip("\n") for ln in text.splitlines()]
            names = {ln for ln in lines if ln.strip() and not ln.lstrip().startswith("#")}
            return names, {}, rel
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            continue
        names, flags = set(), {}
        if isinstance(data, dict):
            for family in data.get("families") or []:
                if not isinstance(family, dict):
                    continue
                for typ in family.get("types") or []:
                    if isinstance(typ, dict) and isinstance(typ.get("name"), str):
                        names.add(typ["name"])
                        if isinstance(typ.get("provisional"), bool):
                            flags[typ["name"]] = typ["provisional"]
                    elif isinstance(typ, str):
                        names.add(typ)
            for key in ("all_names", "entities", "table1"):
                for item in data.get(key) or []:
                    if isinstance(item, str):
                        names.add(item)
        elif isinstance(data, list):
            names = {x for x in data if isinstance(x, str)}
        if names:
            return names, flags, rel
    return set(), {}, None


def check_entity_annotation(ctx: DTContext, repo: Path):
    """
    RULE 5 — `entity_annotation` (contract §2(3), §6 rule 5).

    What this check CAN prove, and what it cannot, stated up front because rule 5 asks for
    something this repository does not yet carry.

    PROVES: the `(provisional type)` extraction artefact never reaches an entity name; no
    entity string carries leading, trailing or doubled whitespace; neither of the two
    CNS5-internal divergences Revision 2 records is the one authored; `code_status` is in
    the closed set; `provisional` is a boolean and not a string smuggled into the name;
    `shared_with[]` is a list of non-empty strings and never contains the entity itself.

    DOES NOT PROVE, unless this repo carries a transcription: that an entity string matches
    CNS5 Table 1. Revision 2 §9 records the 144-row transcription as living outside the
    vault. Where it is absent, an unrecognised entity is a WARN that SAYS it is unverified,
    because the alternative — silence — is what rule 5 exists to prevent. Drop the
    transcription at docs/cns5_table1_entities.txt and every unrecognised string becomes a
    FAIL, with no change to this code.

    No spelling rule is imposed on `who_cns5_entity`. ICD-O-3.2 uses `tumor` (contract
    §5.4) and that is enforced by the round-trip on `morphology_name`; the WHO Blue Books
    do not, and inventing a spelling rule for entity names here would be exactly the recall
    rule 5 forbids.
    """
    out, seen = [], 0
    reference, table1_provisional, ref_source = _cns5_reference_list(repo)
    known = reference or CNS5_TABLE1_ENTITIES
    artefact = re.compile(ENTITY_NAME_ARTEFACT_RE, re.I)
    unverified = []

    for holder, loc, _node in _g3_holders(ctx):
        if "entity_annotation" not in holder:
            continue
        ea = holder["entity_annotation"]
        if not isinstance(ea, dict):
            out.append((FAIL, "%s: entity_annotation must be an object, got %r" % (loc, ea)))
            continue
        seen += 1

        name = ea.get("who_cns5_entity")
        if not isinstance(name, str) or not name.strip():
            out.append((FAIL, "%s: entity_annotation.who_cns5_entity is required and must "
                              "be a non-empty string (contract §2(3))" % loc))
            name = None

        if name is not None:
            if artefact.search(name):
                out.append((FAIL, "%s: entity_annotation.who_cns5_entity %r carries the "
                                  "string \"(provisional type)\". That is an extraction "
                                  "artefact of the source's italics, not part of the "
                                  "entity's name — use \"provisional\": true instead "
                                  "(contract §2(3))" % (loc, name)))
            if name != name.strip() or "  " in name:
                out.append((FAIL, "%s: entity_annotation.who_cns5_entity %r carries "
                                  "leading, trailing or doubled whitespace. An entity "
                                  "string is compared character-for-character; a space "
                                  "nobody can see is a string nothing matches "
                                  "(contract §2(3))" % (loc, name)))
            elif name in CNS5_TABLE1_DIVERGENCES:
                out.append((FAIL, "%s: entity_annotation.who_cns5_entity %r is CNS5's OTHER "
                                  "spelling of this entity. CNS5 is internally "
                                  "inconsistent and Table 1 wins (Revision 2 §6.2). "
                                  "Table 1 prints %r"
                            % (loc, name, CNS5_TABLE1_DIVERGENCES[name])))
            elif name not in known:
                near = _nearest(name, known)
                if near:
                    out.append((FAIL, "%s: entity_annotation.who_cns5_entity %r is a "
                                      "near-miss on the transcribed CNS5 Table 1 string "
                                      "%r — they differ only in case, punctuation or "
                                      "spacing, which is exactly the drift rule 5 exists "
                                      "to catch" % (loc, name, near)))
                elif name.endswith(", NEC") and ea.get("code_status") == "no_code":
                    # cIMPACT-NOW update 1: NEC means the testing WAS done and its result
                    # does not map to a WHO-defined diagnosis. Such a label therefore has
                    # no WHO type and cannot be in Table 1 — update 11 creates exactly
                    # three of them (Pathway Revision 2 §2.5). The narrow exemption is
                    # earned by the two declarations together: a name ending ", NEC" AND
                    # code_status "no_code". Either alone still FAILs.
                    pass
                elif reference:
                    out.append((FAIL, "%s: entity_annotation.who_cns5_entity %r is not in "
                                      "the transcribed CNS5 Table 1 at %s (rule 5). A "
                                      "cIMPACT-NOW NEC label is exempt only when it both "
                                      "ends \", NEC\" and declares code_status \"no_code\""
                                % (loc, name, ref_source)))
                else:
                    unverified.append("%s: %r" % (loc, name))

        status = ea.get("code_status")
        if status not in ENTITY_CODE_STATUS:
            out.append((FAIL, "%s: entity_annotation.code_status is %r — one of %s "
                              "(contract §2(3))"
                        % (loc, status, ", ".join(sorted(ENTITY_CODE_STATUS)))))

        # --- entity_annotation.status (added 2026-09-14) -------------------------------
        # `code_status` says whether the ENTITY has a code. `status` says how firmly it is
        # being CLAIMED, which is a different question and was previously unaskable. Two
        # trees hit the same situation and handled it oppositely: an MYCN IHC with no
        # published sensitivity or specificity, and a DLGNT with 1p untested. Rendered
        # without it, both read as an established WHO CNS5 diagnosis.
        est = ea.get("status", "established")
        if est not in ENTITY_STATUS:
            out.append((FAIL, "%s: entity_annotation.status is %r — one of %s. Omit it for "
                              "an established entity; it defaults to \"established\"."
                        % (loc, est, ", ".join(sorted(ENTITY_STATUS)))))
        elif est == "suggested":
            # A suggestion the clerk cannot act on is worse than no suggestion: it reads
            # as evidence. The branch must name the test that would settle it.
            if not isinstance(holder.get("provisional_pending"), dict):
                out.append((FAIL, "%s: entity_annotation.status \"suggested\" requires a "
                                  "provisional_pending on the same branch naming the test "
                                  "that would establish %r. Without one the entity renders "
                                  "beside a code with nothing saying it is unconfirmed, "
                                  "which makes the case look better evidenced than it is"
                            % (loc, name)))
            if not str(ea.get("evidence") or "").strip():
                out.append((FAIL, "%s: entity_annotation.status \"suggested\" requires a "
                                  "non-empty evidence string saying what the suggestion "
                                  "rests on" % loc))

        if "provisional" in ea and not isinstance(ea["provisional"], bool):
            out.append((FAIL, "%s: entity_annotation.provisional must be a boolean, got %r "
                              "— it is the field that replaces the \"(provisional type)\" "
                              "artefact, so a string here reintroduces the problem in a "
                              "new place (contract §2(3))" % (loc, ea["provisional"])))
        elif name in table1_provisional and isinstance(ea.get("provisional"), bool) \
                and ea["provisional"] != table1_provisional[name]:
            out.append((FAIL, "%s: entity_annotation.provisional is %r; CNS5 Table 1 marks "
                              "%r as %s a provisional type (%s). `provisional` is the field "
                              "that replaced the \"(provisional type)\" artefact, so it has "
                              "to carry what the artefact carried"
                        % (loc, ea["provisional"], name,
                           "" if table1_provisional[name] else "NOT", ref_source)))

        shared = ea.get("shared_with")
        if status == "shares_code" and not (isinstance(shared, list) and shared):
            out.append((FAIL, "%s: code_status \"shares_code\" requires a non-empty "
                              "shared_with[] naming the entities it shares the code with — "
                              "that list is the whole reason the annotation exists "
                              "(contract §2(3))" % loc))
        if isinstance(shared, list):
            for j, other in enumerate(shared):
                if not isinstance(other, str) or not other.strip():
                    out.append((FAIL, "%s: entity_annotation.shared_with[%d] must be a "
                                      "non-empty string, got %r" % (loc, j, other)))
                elif artefact.search(other):
                    out.append((FAIL, "%s: entity_annotation.shared_with[%d] %r carries the "
                                      "\"(provisional type)\" extraction artefact "
                                      "(contract §2(3))" % (loc, j, other)))
                elif name is not None and other == name:
                    out.append((FAIL, "%s: entity_annotation.shared_with[%d] repeats the "
                                      "entity itself — the list names the OTHER entities "
                                      "on the code" % (loc, j)))

    if not seen and not out:
        return []
    if unverified:
        out.append((WARN, "%d entity string(s) could not be verified against CNS5 Table 1: "
                          "this repo carries no transcription at %s, so the check proved "
                          "only the artefact, whitespace and divergence rules on them. "
                          "Rule 5 asks for a transcribed list; until one lands, Table 1 "
                          "conformance is UNVERIFIED, not verified:\n        %s"
                    % (len(unverified), " or ".join(CNS5_TABLE1_REFERENCE_FILES),
                       "\n        ".join(unverified))))
    if [f for f in out if f[0] == FAIL]:
        return out
    out.append((OK, "%d entity_annotation(s): no \"(provisional type)\" artefact, no "
                    "whitespace drift, no Table 2 spelling%s"
                % (seen, ", all matched against %s" % ref_source if reference else "")))
    return out


# -- rule 9 — grade_resolution -----------------------------------------------------------

def check_grade_resolution(ctx: DTContext):
    """
    RULE 9 — `grade_resolution` (contract §2(4), §6 rule 9).

    Modelled on Group II's `behaviour_resolution` and failing the same way if it is got
    wrong: `unresolved` is the half that runs when the evidence never arrived, and an
    `unresolved` that invents a grade puts a number on the report that no test produced.
    cIMPACT-NOW update 8 is explicit for the commonest instance — an untested
    brain-invasive meningioma has NO established grade, and the tool must omit it rather
    than guess.

    Every `values` entry is then one of exactly two shapes: a grade WITH its
    `grade_system`, or `null` WITH a `reason`. A grade with no system is a numeral whose
    scale the reader has to guess, which is rule 1's problem arriving by another route;
    and a null with no reason is a silent omission that reads as an oversight.
    """
    out, seen = [], 0
    for holder, loc, node in _g3_holders(ctx):
        if "grade_resolution" not in holder:
            continue
        gr = holder["grade_resolution"]
        if not isinstance(gr, dict):
            out.append((FAIL, "%s: grade_resolution must be an object, got %r" % (loc, gr)))
            continue
        seen += 1

        for key in ("criterion", "variable"):
            val = gr.get(key)
            if not isinstance(val, str) or not val.strip():
                out.append((FAIL, "%s: grade_resolution.%s is required and must be a "
                                  "non-empty string (contract §2(4))" % (loc, key)))

        var = gr.get("variable")
        declared = _declared_variables(node) if node is not None else set()
        if isinstance(var, str) and var and node is not None and var not in declared:
            out.append((FAIL, "%s: grade_resolution.variable %r is not declared in this "
                              "node's captured_variables[] — the engine has nowhere to read "
                              "the answer from, so the criterion is asked and then "
                              "discarded" % (loc, var)))

        dmr = gr.get("detection_method_required")
        if dmr is not None:
            if not isinstance(dmr, list) or not dmr:
                out.append((FAIL, "%s: grade_resolution.detection_method_required must be "
                                  "a non-empty list, got %r" % (loc, dmr)))
            else:
                for value in dmr:
                    if value not in DIAGNOSTIC_TESTS:
                        out.append((FAIL, "%s: grade_resolution.detection_method_required "
                                          "%r is not in the closed diagnostic-test "
                                          "vocabulary, so it can never be matched"
                                    % (loc, value)))

        def check_grade_leaf(label, leaf, allow_grade=True):
            if not isinstance(leaf, dict):
                out.append((FAIL, "%s: grade_resolution.%s must be an object, got %r"
                            % (loc, label, leaf)))
                return
            if "grade" not in leaf:
                out.append((FAIL, "%s: grade_resolution.%s has no 'grade' key. Every "
                                  "outcome names either a grade or an explicit null — an "
                                  "absent key is neither (contract §2(4))" % (loc, label)))
                return
            grade = leaf["grade"]
            if grade is None:
                if not (isinstance(leaf.get("reason"), str) and leaf["reason"].strip()) \
                        and not (isinstance(leaf.get("defer_to"), str)
                                 and leaf["defer_to"].strip()):
                    out.append((FAIL, "%s: grade_resolution.%s has grade null and no "
                                      "`reason` (or, on `unresolved`, a `defer_to`). A "
                                      "null with nothing said about it reads as an "
                                      "oversight rather than a finding (contract §2(4))"
                                % (loc, label)))
                return
            if not allow_grade:
                out.append((FAIL, "%s: RULE 9 — grade_resolution.unresolved carries grade "
                                  "%r. `unresolved` must NEVER invent a grade: where the "
                                  "grade cannot be established it is omitted, which is "
                                  "what cIMPACT-NOW update 8 requires for an untested "
                                  "brain-invasive meningioma. A number here is one no test "
                                  "produced (contract §2(4), §6 rule 9)" % (loc, grade)))
                return
            if not isinstance(grade, str):
                out.append((FAIL, "%s: grade_resolution.%s grade must be a string or null, "
                                  "got %r" % (loc, label, grade)))
                return
            if grade.strip() in GRADE_NON_VALUES or grade != grade.strip():
                out.append((FAIL, "%s: RULE 9 — grade_resolution.%s grade is %r. \"NA\" and "
                                  "\"\" are errors, not grades: they render as a grade "
                                  "nobody assigned. Use null with a reason "
                                  "(contract §2(4), §6 rule 9)" % (loc, label, grade)))
                return
            system = leaf.get("grade_system")
            if system not in GRADE_SYSTEMS:
                out.append((FAIL, "%s: RULE 9 — grade_resolution.%s names grade %r with "
                                  "grade_system %r. A grade must name its system: a bare "
                                  "numeral leaves the reader to guess the scale, which is "
                                  "rule 1's failure reached by another route "
                                  "(contract §2(4), §6 rule 9)" % (loc, label, grade, system)))
            elif system == "arabic" and grade not in ARABIC_GRADES:
                out.append((FAIL, "%s: grade_resolution.%s grade %r is not in the Arabic "
                                  "set %s" % (loc, label, grade, sorted(ARABIC_GRADES))))
            elif system == "roman" and grade not in ROMAN_GRADES:
                out.append((FAIL, "%s: grade_resolution.%s grade %r is not in the Roman set "
                                  "%s" % (loc, label, grade, sorted(ROMAN_GRADES))))

        values = gr.get("values")
        if not isinstance(values, dict) or not values:
            out.append((FAIL, "%s: grade_resolution.values is required and must be a "
                              "non-empty object (contract §2(4))" % loc))
        else:
            for key in sorted(values):
                check_grade_leaf("values[%r]" % key, values[key], allow_grade=True)

        if "unresolved" not in gr:
            out.append((FAIL, "%s: grade_resolution.unresolved is REQUIRED. Without it the "
                              "engine has no answer for a case the test never resolved, "
                              "and the branch falls through to whatever the renderer does "
                              "by default (contract §2(4))" % loc))
        else:
            check_grade_leaf("unresolved", gr["unresolved"], allow_grade=False)

    if not seen and not out:
        return []
    if [f for f in out if f[0] == FAIL]:
        return out
    out.append((OK, "%d grade_resolution block(s): no `unresolved` invents a grade, and "
                    "every outcome names a grade with its system or a null with a reason "
                    "(rule 9)" % seen))
    return out


# -- rule 10 — basis_of_diagnosis --------------------------------------------------------

def check_basis_of_diagnosis(ctx: DTContext):
    """
    RULE 10 — `basis_of_diagnosis` (contract §2(5), §6 rule 10).

    ENCR's scale has no 3 and no 6. They are not reserved and they are not deprecated —
    they do not exist, so a 3 in this field is a value the receiving registry will read as
    something else entirely.

    Code 1 is banned outright in this group: every CNS row in ENCR Table 3 is basis 2, so a
    Group III terminal claiming "clinical, physical examination only" is claiming a basis
    the classification does not give any tumour in the group.

    The two ENCR gaps are declared rather than inferred (`ihc_counts_as: 7`,
    `methylation_counts_as: 8`), and where a holder writes down the component codes it
    derived from, the declared value must be the HIGHEST of them — with 0 and 9 overriding,
    which is the only way those two can be reached at all.
    """
    out, seen = [], 0
    for holder, loc, _node in _g3_holders(ctx):
        for key, want in BASIS_DECLARED_GAPS.items():
            if key in holder and holder[key] != want:
                out.append((FAIL, "%s: %s is %r; ENCR leaves this gap and contract §2(5) "
                                  "closes it at %d. Declaring it differently silently "
                                  "re-scales every case that reaches it"
                            % (loc, key, holder[key], want)))

        if "basis_of_diagnosis" not in holder:
            continue
        value = holder["basis_of_diagnosis"]
        seen += 1
        if isinstance(value, bool) or not isinstance(value, int):
            if isinstance(value, str) and value.strip().isdigit():
                out.append((FAIL, "%s: basis_of_diagnosis is the string %r — ENCR basis is "
                                  "an integer, and a string sorts and compares differently "
                                  "from the number it looks like" % (loc, value)))
            else:
                out.append((FAIL, "%s: basis_of_diagnosis must be an integer, got %r"
                            % (loc, value)))
            continue
        if value in BASIS_OF_DIAGNOSIS_ABSENT:
            out.append((FAIL, "%s: RULE 10 — basis_of_diagnosis %d does not exist. The ENCR "
                              "scale is %s; 3 and 6 are not values in it, so a receiving "
                              "registry reads this as something else entirely "
                              "(contract §2(5), §6 rule 10)"
                        % (loc, value, sorted(BASIS_OF_DIAGNOSIS_VALID))))
            continue
        if value not in BASIS_OF_DIAGNOSIS_VALID:
            out.append((FAIL, "%s: RULE 10 — basis_of_diagnosis %d is outside the ENCR set "
                              "%s (contract §2(5))"
                        % (loc, value, sorted(BASIS_OF_DIAGNOSIS_VALID))))
            continue
        if ctx.group == GROUP3 and value == BASIS_FORBIDDEN_IN_GROUP3:
            out.append((FAIL, "%s: RULE 10 — no Group III terminal may emit basis code 1 "
                              "(clinical, physical examination only). Every CNS row in ENCR "
                              "Table 3 is basis 2: an intracranial tumour is not diagnosed "
                              "by physical examination (contract §2(5), §6 rule 10)" % loc))

        components = None
        for key in ("basis_components", "basis_of_diagnosis_components",
                    "basis_derived_from"):
            if isinstance(holder.get(key), list):
                components = [c for c in holder[key] if isinstance(c, int)
                              and not isinstance(c, bool)]
                break
        if components and value not in BASIS_OF_DIAGNOSIS_OVERRIDE:
            highest = max(components)
            graded = [c for c in components if c not in BASIS_OF_DIAGNOSIS_OVERRIDE]
            if graded:
                highest = max(graded)
            if value != highest:
                out.append((FAIL, "%s: basis_of_diagnosis is %d but the components it "
                                  "declares (%s) make the highest %d. §2(5) computes the "
                                  "basis as the highest of codes 1-8, with 0 and 9 "
                                  "overriding — a lower value understates and a higher one "
                                  "overstates the evidence on the case"
                            % (loc, value, ", ".join(str(c) for c in components), highest)))

    if not seen and not out:
        return []
    if [f for f in out if f[0] == FAIL]:
        return out
    out.append((OK, "%d basis_of_diagnosis value(s) in the ENCR set %s; none is 3, 6 or "
                    "(in Group III) 1 (rule 10)"
                % (seen, sorted(BASIS_OF_DIAGNOSIS_VALID))))
    return out


# -- rule 11 — imaging terminals ---------------------------------------------------------

def check_imaging_terminals(ctx: DTContext):
    """
    RULE 11 — the imaging-only endpoints (contract §2(6), §3.5, §6 rule 11).

    Two endpoints in this group are reached with no tissue at all: NF1 optic pathway
    glioma, and DIPG. The second has κ = 0.297 interobserver agreement and an explicit
    finding that imaging-only diagnosis "does not reach the appropriate threshold to be
    considered a standard of care" — so every terminal behind an `imaging_pathway` that
    never reaches histology has to SAY so in all four of the fields that carry that fact:
    `no_tissue`, `endpoint_verification`, `basis_of_diagnosis` and `diversion_criteria[]`.

    The empty list is the one the contract calls out as a build error, and it is the
    interesting one. `"diversion_criteria": []` is not "no diversions apply" — it is an
    imaging endpoint with every safety catch removed, rendering identically to one that was
    never gated. An absent list at least reads as unfinished; an empty one reads as
    considered and cleared. Both FAIL here.
    """
    out, seen = [], 0
    for node_id, node in sorted(ctx.nodes.items()):
        if node.get("node_type") != "imaging_pathway":
            continue
        seen += 1
        holders = [(node, "(node level)")]
        for holder, where in _branch_containers(node):
            holders.append((holder, where))

        # A branch inherits what its node declares and vice versa. Both placements are
        # legitimate and the trees use both: one node may carry several endpoints that
        # differ per option, while a single shared diversion list belongs on the node.
        # Rule 11 is about whether the FACT is recorded, not about which object records it.
        def eff(holder, key):
            v = holder.get(key)
            return node.get(key) if v is None else v

        for holder, where in holders:
            loc = "imaging_pathway %s (%s)" % (node_id, where)
            # A branch that continues to a histology node is not an imaging-only terminal.
            if holder is not node and holder.get("next_node"):
                continue
            emits = as_code(holder.get("morphology_code"))
            declares = any(k in holder for k in
                           ("no_tissue", "endpoint_verification", "diversion_criteria",
                            "basis_of_diagnosis"))
            # A node that declares ONLY diversion_criteria is publishing a shared list for
            # its own branches, not being a terminal itself. The terminal fields then live
            # on the branches, which is where the endpoints differ. Treating the node as a
            # terminal here would demand no_tissue/basis on an object that emits nothing.
            node_is_terminal = as_code(node.get("morphology_code")) is not None or any(
                k in node for k in ("no_tissue", "endpoint_verification", "basis_of_diagnosis"))
            if holder is node and not node_is_terminal:
                continue
            if holder is not node and not emits and not declares:
                continue

            if eff(holder, "no_tissue") is not True:
                out.append((FAIL, "%s: RULE 11 — an imaging terminal reached without "
                                  "histology must carry \"no_tissue\": true (it is %r). "
                                  "The field is what stops the case being counted as "
                                  "microscopically verified (contract §6 rule 11)"
                            % (loc, eff(holder, "no_tissue"))))
            if eff(holder, "endpoint_verification") != "not_verified":
                out.append((FAIL, "%s: RULE 11 — endpoint_verification must be "
                                  "\"not_verified\" on an imaging-only terminal, got %r "
                                  "(contract §6 rule 11)"
                            % (loc, eff(holder, "endpoint_verification"))))
            basis = eff(holder, "basis_of_diagnosis")
            # 2 is clinical investigation without tissue. 4 is specific tumour markers,
            # which also records no tissue and which ENCR ranks ABOVE 2 under its own
            # "take the highest of 1-8" rule — the two pituitary marker routes of ENCR
            # Table 4 are basis 4 and forcing them to 2 would understate them.
            if basis not in (2, 4):
                out.append((FAIL, "%s: RULE 11 — basis_of_diagnosis must be 2 (clinical "
                                  "investigation without tissue) on an imaging-only "
                                  "terminal, got %r. 4 (specific tumour markers) is also "
                                  "permitted; anything else records tissue that was never "
                                  "taken (contract §2(5), §6 rule 11)"
                            % (loc, basis)))

            if "diversion_criteria" not in holder and "diversion_criteria" not in node:
                out.append((FAIL, "%s: RULE 11 — an imaging-only terminal carries no "
                                  "diversion_criteria[]. These are the features that force "
                                  "the tissue branch even when the imaging constellation is "
                                  "met; without them the endpoint is ungated "
                                  "(contract §2(6), §6 rule 11)" % loc))
            else:
                dc = eff(holder, "diversion_criteria")
                if not isinstance(dc, list):
                    out.append((FAIL, "%s: diversion_criteria must be an array, got %r"
                                % (loc, dc)))
                elif not dc:
                    out.append((FAIL, "%s: RULE 11 — diversion_criteria[] is EMPTY. An "
                                      "empty list is a build error, not \"no diversions "
                                      "apply\": it renders exactly like a terminal that "
                                      "was never gated, while reading to the next author "
                                      "as considered and cleared. DIPG's imaging-only "
                                      "endpoint has κ = 0.297 agreement and is explicitly "
                                      "below standard of care — the six diversion criteria "
                                      "are what make it safe to offer at all "
                                      "(contract §2(6), §6 rule 11)" % loc))
                else:
                    for j, crit in enumerate(dc):
                        if not isinstance(crit, dict):
                            out.append((FAIL, "%s: diversion_criteria[%d] is not an object"
                                        % (loc, j)))
                            continue
                        for key in ("feature", "reason"):
                            val = crit.get(key)
                            if not isinstance(val, str) or not val.strip():
                                out.append((FAIL, "%s: diversion_criteria[%d] has no "
                                                  "non-empty %r — a diversion the clerk "
                                                  "cannot read is a diversion nobody takes "
                                                  "(contract §2(6))" % (loc, j, key)))

    if not seen and not out:
        return []
    if [f for f in out if f[0] == FAIL]:
        return out
    out.append((OK, "%d imaging_pathway node(s): every imaging-only terminal carries "
                    "no_tissue, endpoint_verification \"not_verified\", basis 2 and a "
                    "NON-EMPTY diversion_criteria[] (rule 11)" % seen))
    return out


# -- rule 4 — numeric_gate band units and the per-unit domain sweep ----------------------

_BAND_POINT_RE = re.compile(r"^\s*(>=|<=|=>|=<|>|<|=)?\s*(-?\d+(?:\.\d+)?)\s*$")
_BAND_SPAN_RE = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*[-–—]\s*(-?\d+(?:\.\d+)?)\s*$")
_INF = float("inf")


def _band_step(token: str) -> float:
    """The precision a band was authored at. '19' -> 1; '19.5' -> 0.1; '0.99' -> 0.01."""
    if "." in token:
        return 10.0 ** -len(token.split(".", 1)[1])
    return 1.0


def _band_interval(raw):
    """
    A band's half-open [lo, hi) interval, or None when the range is not numeric.

    DT master §4: a range is INCLUSIVE at the precision written, so "10-19" covers
    [10, 20) and ">=20" covers [20, inf). Sweeping at one decimal finer than the finest
    band is what turns "no gap" into something a machine can answer.
    """
    if not isinstance(raw, str):
        return None
    span = _BAND_SPAN_RE.match(raw)
    if span:
        lo, hi = float(span.group(1)), float(span.group(2))
        return (lo, hi + _band_step(span.group(2)))
    point = _BAND_POINT_RE.match(raw)
    if not point:
        return None
    op, num = point.group(1) or "=", point.group(2)
    value, step = float(num), _band_step(num)
    if op in (">=", "=>"):
        return (value, _INF)
    if op == ">":
        return (value + step, _INF)
    if op in ("<=", "=<"):
        return (-_INF, value + step)
    if op == "<":
        return (-_INF, value)
    return (value, value + step)


def check_numeric_gate_units(ctx: DTContext):
    """
    RULE 4 — `unit` on every `numeric_gate.bands[]`, and the domain sweep PER UNIT
    (contract §2(7), §6 rule 4).

    This group states mitotic thresholds in five incompatible units — 4 per 10 HPF of
    0.16 mm², 2.5/mm², 2 per 10 HPF of 0.23 mm², 3 per 2.4 mm², under 1 per 20 HPF. An HPF
    is not a fixed area, so a band list with no denominator is not a threshold, it is a
    number. That is why the unit is required on the BAND rather than on the node: one gate
    can legitimately carry bands in two units, and the moment it does, a single node-level
    unit is wrong for at least one of them.

    The sweep then runs per unit, because comparing a `per_mm2` band to a `per_10_hpf` band
    manufactures both gaps and overlaps that are not there. A gap is the dangerous half: an
    uncovered value falls silently to NOS and reads as a clinical decision rather than a
    hole in the file.

    Band-level `unit` is a GROUP III amendment. Groups 1 and 2 carry a node-level `unit` in
    free text (`%`, `months`, `×10⁹/L`) and are untouched here — check_numeric_gate_shape()
    still validates them exactly as before.
    """
    if ctx.group != GROUP3:
        return []
    out, gates, swept = [], 0, 0
    for node_id, node in sorted(ctx.nodes.items()):
        if node.get("node_type") != "numeric_gate":
            continue
        gates += 1
        bands = node.get("bands")
        if not isinstance(bands, list) or not bands:
            continue                       # check_numeric_gate_shape() owns this
        by_unit: dict = {}
        for i, band in enumerate(bands):
            if not isinstance(band, dict):
                continue
            unit = band.get("unit")
            rng = str(band.get("range") or "")
            # A sentinel band ("not_documented") carries no number, so a denominator on it
            # would be meaningless. Rule 4 exists because the same COUNT means different
            # things under different denominators; "not documented" is not a count.
            if unit is None and not any(ch.isdigit() for ch in rng):
                continue
            if unit is None:
                out.append((FAIL, "numeric_gate %s: bands[%d] (%r) has no `unit`. RULE 4 — "
                                  "this group states thresholds in five incompatible units "
                                  "and an HPF is not a fixed area, so a band list without a "
                                  "denominator is a build error (contract §2(7), §6 rule 4)"
                            % (node_id, i, band.get("range"))))
                continue
            if unit not in NUMERIC_GATE_UNITS:
                out.append((FAIL, "numeric_gate %s: bands[%d] unit %r is not in the closed "
                                  "set %s (contract §2(7))"
                            % (node_id, i, unit, ", ".join(sorted(NUMERIC_GATE_UNITS)))))
                continue
            if unit in ("per_10_hpf", "per_hpf") and band.get("hpf_area_mm2") is None \
                    and node.get("hpf_area_mm2") is None \
                    and _band_interval(band.get("range")) is not None:
                out.append((WARN, "numeric_gate %s: bands[%d] is stated per HPF with no "
                                  "`hpf_area_mm2`. An HPF is not a fixed area — without "
                                  "the denominator this threshold cannot be compared with "
                                  "any other in the group (contract §2(7))"
                            % (node_id, i)))
            by_unit.setdefault(unit, []).append((i, band))

        for unit, items in sorted(by_unit.items()):
            intervals, sentinels = [], []
            for i, band in items:
                span = _band_interval(band.get("range"))
                if span is None:
                    sentinels.append((i, band.get("range")))
                else:
                    intervals.append((span, i, band.get("range")))
            if not intervals:
                continue
            swept += 1
            intervals.sort()
            floor = 0.0 if unit == "percent" else 0.0
            ceiling = 100.0 if unit == "percent" else _INF
            cursor = floor
            for (lo, hi), i, raw in intervals:
                # A band may legitimately reach below the floor ("<2.5" on a count that
                # cannot be negative). Clamp before comparing, or every such band reads as
                # an overlap with a region the domain does not contain — a false FAIL, and
                # the corrosive kind: it teaches the next author to write "0-2.4" instead
                # of the threshold the paper actually states.
                lo = max(lo, floor)
                if lo > cursor:
                    out.append((FAIL, "numeric_gate %s [%s]: no band covers %g to %g — the "
                                      "next band is bands[%d] (%r). DT master §4: bands "
                                      "cover their domain with no gap at the authored "
                                      "precision. An uncovered value falls silently to NOS "
                                      "and reads as a clinical decision rather than a hole "
                                      "in the file" % (node_id, unit, cursor, lo, i, raw)))
                elif hi > cursor and lo < cursor:
                    out.append((FAIL, "numeric_gate %s [%s]: bands[%d] (%r) overlaps the "
                                      "band before it below %g — two bands claiming one "
                                      "value leave the answer to whichever the engine reads "
                                      "first" % (node_id, unit, i, raw, cursor)))
                cursor = max(cursor, hi)
            if cursor < ceiling:
                out.append((FAIL, "numeric_gate %s [%s]: the bands stop at %g and the "
                                  "domain runs to %s — every value above the last band "
                                  "falls through uncovered"
                            % (node_id, unit, cursor, "100" if ceiling == 100.0 else "∞")))
            for i, raw in sentinels:
                out.append((NOTE, "numeric_gate %s [%s]: bands[%d] (%r) is a non-numeric "
                                  "sentinel and is outside the domain sweep"
                            % (node_id, unit, i, raw)))

    if not gates and not out:
        return []
    if [f for f in out if f[0] == FAIL]:
        return out
    out.append((OK, "%d numeric_gate node(s): every band names a unit from the closed set, "
                    "and %d unit-partition(s) cover their domain with no gap and no overlap "
                    "(rule 4)" % (gates, swept)))
    return out


# -- rule 6 — the behaviour split --------------------------------------------------------

def check_group3_behaviour_split(ctx: DTContext, layer1: Path):
    """
    RULE 6 — the eighteen behaviour-overloaded codes (contract §1.2, §6 rule 6).

    One `morphology_entries[]` object per behaviour, each with its own explicit
    `behavior_code` and its own ICD-O-3.2 preferred term. Most of the eighteen carry a
    benign term at /0-/1 against a carcinoma at /3, so a table printing only the lowest
    behaviour reads "adenoma" where the data says "carcinoma".

    WHICH behaviours each code needs is not transcribed here — it is COMPUTED, as the
    behaviours ICD-O-3.2 actually carries for the code intersected with the group's one
    behaviour declaration, `0-1,3`. That is rule 8 applied to a count: the expected set
    comes from the source of truth, so it cannot be got wrong from memory and it moves on
    its own if ICD-O-3.2 does. It also settles `8000` without a special case — ICD-O-3.2
    carries /0, /1, /3, /6 and /9, the declaration admits three of them, and /6 and /9
    correctly fall outside the group.
    """
    if ctx.group != GROUP3:
        return []
    out = []
    index, err = load_icdo32(layer1)
    by_code: dict = {}
    for entry in ctx.entries:
        if not isinstance(entry, dict):
            continue
        code = as_code(entry.get("morphology_code"))
        if code is None:
            continue
        beh = entry.get("behavior_code")
        by_code.setdefault(code, []).append(None if beh is None else str(beh).strip())

    if err:
        out.append((WARN, "RULE 6 is running WITHOUT its anchor: %s. The expected behaviour "
                          "set per code is computed from ICD-O-3.2, so with the database "
                          "absent this check falls back to 'at least two distinct explicit "
                          "behaviours', which is weaker than the rule" % err))

    divergent = 0
    for code in GROUP3_BEHAVIOUR_SPLIT_CODES:
        authored = by_code.get(code)
        if authored is None:
            out.append((FAIL, "RULE 6 — code %s is one of the eighteen behaviour-overloaded "
                              "codes of contract §1.2 and has no morphology_entries[] "
                              "object at all (§6 rule 6)" % code))
            continue
        if any(b in (None, "") for b in authored):
            out.append((FAIL, "RULE 6 — code %s has an entry with no explicit "
                              "behavior_code. On an overloaded code the behaviour is the "
                              "whole difference between a benign term and a carcinoma "
                              "(contract §1.2, §6 rule 6)" % code))
        present = {b for b in authored if b}
        if len(authored) != len(present):
            out.append((FAIL, "RULE 6 — code %s has %d entries across %d distinct "
                              "behaviour(s) (%s): one object PER BEHAVIOUR, no duplicates "
                              "(contract §1.2)"
                        % (code, len(authored), len(present), ", ".join(sorted(present)))))
        if index:
            expected = {b for (c, b) in index if c == code} & GROUP3_BEHAVIOURS_DECLARED
            if expected and present != expected:
                missing = sorted(expected - present)
                extra = sorted(present - expected)
                out.append((FAIL, "RULE 6 — code %s is authored at %s; ICD-O-3.2 carries it "
                                  "at %s within the group's \"0-1,3\" declaration.%s%s "
                                  "(contract §1.2, §6 rule 6)"
                            % (code, "/" + ", /".join(sorted(present)) if present else "no "
                               "behaviour", "/" + ", /".join(sorted(expected)),
                               "  Missing: /%s." % ", /".join(missing) if missing else "",
                               "  Not in ICD-O-3.2 for this code (or outside the "
                               "declaration): /%s." % ", /".join(extra) if extra else "")))
        elif len(present) < 2:
            out.append((FAIL, "RULE 6 — code %s is authored at a single behaviour (/%s). "
                              "Contract §1.2 lists it as behaviour-overloaded: it needs one "
                              "entry per behaviour (§6 rule 6)"
                        % (code, ", /".join(sorted(present)) or "none")))

    if index:
        listed = set(GROUP3_BEHAVIOUR_SPLIT_CODES)
        for code, authored in sorted(by_code.items()):
            if code in listed:
                continue
            expected = {b for (c, b) in index if c == code} & GROUP3_BEHAVIOURS_DECLARED
            if expected and {b for b in authored if b} != expected:
                divergent += 1
        if divergent:
            out.append((NOTE, "%d code(s) outside the eighteen carry a behaviour set that "
                              "differs from ICD-O-3.2 ∩ \"0-1,3\". That is legal — §1.2 "
                              "names only eighteen as overloaded — but it is where the "
                              "108-entry target of §1.1 will diverge if it does" % divergent))

    if [f for f in out if f[0] == FAIL]:
        return out
    out.append((OK, "all %d behaviour-overloaded codes of contract §1.2 are authored one "
                    "entry per behaviour, each with an explicit behavior_code, against the "
                    "behaviour set ICD-O-3.2 carries (rule 6)"
                % len(GROUP3_BEHAVIOUR_SPLIT_CODES)))
    return out


# -- rule 7 — the codes that do not exist ------------------------------------------------

def _code_token_re(code):
    return re.compile(r"(?<![0-9])%s(?![0-9])" % re.escape(code))


def check_group3_absent_codes(ctx: DTContext, repo: Path):
    """
    RULE 7 — `9402`-`9409`, `9422`, `8274`-`8279`, `9536` appear NOWHERE (contract §1.1,
    §6 rule 7).

    Sixteen of the codes ICCC-3's Group III ranges name do not exist in ICD-O-3.2. Seven of
    those sixteen are nevertheless offered by the REDCap option list, which is how they get
    into circulation: an author reading the option list rather than the database picks one
    up, and the tool then tells a clerk to enter a code the registry's own coding standard
    does not have.

    Checked in three places, because the code reaches the screen from three: the decision
    tree itself, an alias TARGET (`maps_to_morphology_codes`, and the code an alias prints
    in its `full_form`), and free text. `alias` and `also_known_as` are deliberately NOT
    scanned — those are what the clerk TYPES, and §1.1 keeps them as alias inputs.

    A banned code in clerk-facing text FAILs: it is a code the clerk can read and copy. In
    author-facing text (`coding_note`, `topography_routing_note` — never displayed) it is a
    WARN, because a note explaining that a code does not exist is useful work, and the
    honest fix is to name the range rather than print the digits.
    """
    patterns = [(code, _code_token_re(code)) for code in GROUP3_ABSENT_CODES]
    out, hits = [], 0

    def scan(container, where, source):
        nonlocal hits
        for holder, path in walk_dicts(container):
            for key, value in holder.items():
                if key in ALIAS_INPUT_KEYS:
                    continue
                loc = "%s%s.%s" % (where, ("." + path) if path else "", key)
                if key in ("morphology_code", "nos_fallback_code", "code", "refer_code",
                           "maps_to_morphology_codes"):
                    candidates = value if isinstance(value, list) else [value]
                    for cand in candidates:
                        cs = as_code(cand)
                        if cs and any(cs == code for code, _rx in patterns):
                            hits += 1
                            out.append((FAIL, "RULE 7 — %s carries code %s, which does not "
                                              "exist in ICD-O-3.2. Contract §1.1 lists the "
                                              "sixteen; seven of them are offered by the "
                                              "REDCap option list anyway, which is exactly "
                                              "how they get into circulation (§6 rule 7)"
                                        % (loc, cs)))
                    continue
                if not isinstance(value, str):
                    continue
                for code, rx in patterns:
                    if not rx.search(value):
                        continue
                    hits += 1
                    if key in AUTHOR_FACING_TEXT_KEYS:
                        out.append((WARN, "RULE 7 — %s mentions %s, a code that does not "
                                          "exist in ICD-O-3.2. This field is author-facing "
                                          "and is not displayed, so it does not reach a "
                                          "clerk — but §6 rule 7 says nowhere. Name the "
                                          "range, not the digits" % (loc, code)))
                    else:
                        out.append((FAIL, "RULE 7 — %s prints %s, a code that does not exist "
                                          "in ICD-O-3.2, in text a clerk reads. A code on "
                                          "screen is a code that gets entered "
                                          "(contract §1.1, §6 rule 7)" % (loc, code)))
                    break

    scan(ctx.data, ctx.name, "dt")
    alias_path = Path(repo) / "data" / "aliases" / ("aliases_group_%02d.json" % ctx.group)
    if alias_path.exists():
        data, findings = load_json(alias_path)
        out.extend(findings)
        if data is not None:
            entries = data.get("aliases") if isinstance(data, dict) else data
            if isinstance(entries, list):
                for i, entry in enumerate(entries):
                    if isinstance(entry, dict):
                        scan(entry, "%s[%d]" % (alias_path.name, i), "alias")

    if [f for f in out if f[0] == FAIL]:
        return out
    if ctx.group != GROUP3 and not hits:
        return []
    out.append((OK, "none of the %d codes that ICCC-3 names but ICD-O-3.2 does not carry "
                    "(%s) appears as a code, a fallback, an alias target or in clerk-facing "
                    "text (rule 7)"
                % (len(GROUP3_ABSENT_CODES),
                   "9402-9409, 9422, 8274-8279, 9536")))
    return out


# -- rule 12 — the topography map is total and disjoint ----------------------------------

_TOPO_RE = re.compile(r"^C\d{2}\.\d$")


def _topo_index(code):
    return int(code[1:3]) * 10 + int(code[4])


def _topo_from_index(n):
    return "C%02d.%d" % (n // 10, n % 10)


def _expand_topography(tokens):
    """['C71.0-C71.5', 'C71.8'] -> ['C71.0', ..., 'C71.5', 'C71.8']. (codes, bad_tokens)."""
    if isinstance(tokens, str):
        tokens = [t for t in re.split(r"[,;]", tokens) if t.strip()]
    codes, bad = [], []
    for token in tokens or []:
        if not isinstance(token, str):
            bad.append(repr(token))
            continue
        token = token.strip()
        parts = [p.strip() for p in re.split(r"[-–—]", token) if p.strip()]
        if len(parts) == 1 and _TOPO_RE.match(parts[0]):
            codes.append(parts[0])
        elif len(parts) == 2 and _TOPO_RE.match(parts[0]) and _TOPO_RE.match(parts[1]):
            lo, hi = _topo_index(parts[0]), _topo_index(parts[1])
            if lo > hi:
                bad.append(token)
                continue
            codes.extend(_topo_from_index(n) for n in range(lo, hi + 1))
        else:
            bad.append(token)
    return codes, bad


def _existing_topography(layer1):
    """
    The topography codes Layer 1 can actually RECORD, from the REDCap topography option
    list. (codes, source_or_None).

    Rule 12's sweep is written as four ranges — C70.0-C70.9, C71.0-C71.9, C72.0-C72.9,
    C75.1-C75.3 and C80.9 — and read literally that is 34 codes, nine of which do not
    exist in ICD-O-3 topography at all (C70.2-C70.8, C72.6, C72.7). Demanding a tree for
    a code no case can carry is a false FAIL, and the corrosive kind: the only way to
    clear it is to invent an assignment, after which the check has taught the author to
    write something untrue.

    So existence is read off Layer 1 rather than asserted here. Every code the sweep drops
    is REPORTED, so the reduction is visible rather than silent.
    """
    if layer1 is None:
        return set(), None
    path = Path(layer1) / "RedCap Options" / "Topography Redcap.md"
    if not path.exists():
        return set(), None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return set(), None
    codes = set()
    for m in re.finditer(r"^(\d{3}),\s", text, re.M):
        try:
            codes.add(_topo_from_raw(m.group(1)))
        except ValueError:
            continue
    return codes, "RedCap Options/Topography Redcap.md"


def _load_topography_lookup(repo: Path):
    """(topography_lookup dict, findings) from data/shared/topography_codes.json."""
    path = Path(repo) / "data" / "shared" / "topography_codes.json"
    data, findings = load_json(path)
    if data is None:
        return {}, findings
    lookup = data.get("topography_lookup") if isinstance(data, dict) else None
    if not isinstance(lookup, dict):
        return {}, findings + [(FAIL, "%s: no 'topography_lookup' object" % path.name)]
    return lookup, findings


def _group4_candidate_topography(repo: Path):
    """
    (group4_codes, all_topography_codes, findings) — the topography codes GROUP IV can
    actually carry, and the full universe of real topography codes, both read from
    `data/shared/topography_codes.json` rather than hand-transcribed or swept from the
    whole registry's topography list (see the retired GROUP4_TOPOGRAPHY_SWEEP comment,
    above check_group4_topography_map()).

    A code is Group IV's when its own `topography_lookup` entry's `candidate_groups`
    list names group 4 (34 of them, 2026-09-18). The special value
    `"route_by_morphology"` (currently only C80.9, Unknown Primary Site) is NOT a
    member of this set on purpose: it is not a site Group IV owns by candidacy, it is a
    site every group can reach depending on morphology, and it is the router's declared
    catch-all target — the "everything else" half of rule 5 checks for that separately,
    by reading presentation_router.json's own `tree_routing.default`, not by folding it
    into this universe.
    """
    lookup, findings = _load_topography_lookup(repo)
    codes = set()
    for code, entry in lookup.items():
        if not isinstance(entry, dict):
            continue
        cg = entry.get("candidate_groups")
        if isinstance(cg, list) and 4 in cg:
            codes.add(code)
    return codes, set(lookup), findings


def check_group3_topography_map(ctx: DTContext, layer1: Path):
    """
    RULE 12 — the topography map is TOTAL and DISJOINT (contract §3, §6 rule 12).

    Group III keys its six trees to anatomical compartment, and the router picks the tree
    from the topography already captured at Stage 1 — so this map, and nothing else,
    decides which tree a case enters. Both ways of getting it wrong are invisible until a
    case hits them, and Revision 2 records that the FIRST DRAFT of this table had both:
    C72.9 assigned to two trees, and C72.2, C72.4 and C72.5 assigned to none. An unrouted
    code dead-ends a real case; a duplicated one silently picks whichever row the engine
    reads first, which is not a decision anybody made.

    So the check is a sweep, not an inspection: every one of the 34 topography codes this
    group can carry is looked up, and the answer must be exactly one tree.
    """
    if ctx.group != GROUP3:
        return []
    out = []
    declared: dict = {}
    sources: dict = {}

    def take(tree_id, holder, origin):
        for key in TREE_TOPOGRAPHY_KEYS:
            if key not in holder:
                continue
            codes, bad = _expand_topography(holder[key])
            for token in bad:
                out.append((FAIL, "tree %r: %s carries %s, which is not a topography code "
                                  "or an ascending range of them (expected e.g. \"C71.6\" "
                                  "or \"C71.0-C71.5\")" % (tree_id, key, token)))
            if codes:
                declared.setdefault(tree_id, set()).update(codes)
                sources[tree_id] = "%s.%s" % (origin, key)
            return

    for item in ctx.metadata.get("decision_trees") or []:
        if isinstance(item, dict):
            tid = item.get("tree_id") or item.get("id")
            if isinstance(tid, str):
                take(tid, item, "metadata.decision_trees")
    for tree in ctx.trees:
        raw = None
        for candidate in ctx.data.get("decision_trees") or []:
            if isinstance(candidate, dict) and \
                    (candidate.get("tree_id") or candidate.get("id")) == tree["tree_id"]:
                raw = candidate
                break
        if isinstance(raw, dict) and tree["tree_id"] not in declared:
            take(tree["tree_id"], raw, "decision_trees[]")

    if not declared:
        return [(FAIL, "RULE 12 — no tree in this file declares the topography it owns, so "
                       "the map cannot be swept. The router picks the Group III tree from "
                       "the topography captured at Stage 1 and from nothing else; with no "
                       "map, every case enters whichever tree the engine reads first. "
                       "Declare it on metadata.decision_trees[] or on the tree object, "
                       "under one of: %s (contract §3, §6 rule 12)"
                 % ", ".join(TREE_TOPOGRAPHY_KEYS))]

    owners: dict = {}
    for tree_id, codes in declared.items():
        for code in codes:
            owners.setdefault(code, []).append(tree_id)

    existing, topo_source = _existing_topography(layer1)
    contract_union = set().union(*GROUP3_TREE_TOPOGRAPHY.values())
    if existing:
        sweep = [c for c in GROUP3_TOPOGRAPHY_SWEEP
                 if c in existing or c in contract_union]
        only_contract = sorted(c for c in sweep if c not in existing)
    else:
        sweep = [c for c in GROUP3_TOPOGRAPHY_SWEEP if c in contract_union]
        only_contract = []
        out.append((WARN, "the REDCap topography option list could not be read, so the "
                          "rule 12 sweep falls back to the codes contract §3 itself "
                          "assigns. A real topography code that NO tree owns and the "
                          "contract table also omits would not be caught"))
    dropped = [c for c in GROUP3_TOPOGRAPHY_SWEEP if c not in sweep]
    if dropped:
        out.append((NOTE, "%d code(s) in rule 12's literal sweep are not in Layer 1's "
                          "topography option list and are not assigned by contract §3, so "
                          "no case can carry them and no tree is required to own them: %s"
                    % (len(dropped), ", ".join(dropped))))
    if only_contract:
        out.append((WARN, "%d topography code(s) are assigned a tree by contract §3 but are "
                          "MISSING from %s: %s. That is a Layer 1 gap, not a tool one — a "
                          "case at one of these cannot be recorded in REDCap at all"
                    % (len(only_contract), topo_source, ", ".join(only_contract))))

    unrouted = [c for c in sweep if not owners.get(c)]
    duplicated = [(c, owners[c]) for c in sweep if len(owners.get(c, [])) > 1]
    outside = sorted(set(owners) - set(sweep))

    if unrouted:
        out.append((FAIL, "RULE 12 — %d topography code(s) in the Group III sweep resolve to "
                          "NO tree: %s. A case at one of these reaches the router, finds no "
                          "handoff and dead-ends (contract §3, §6 rule 12)"
                    % (len(unrouted), ", ".join(unrouted))))
    for code, trees in duplicated:
        out.append((FAIL, "RULE 12 — topography %s resolves to %d trees (%s). The map must "
                          "be disjoint: a duplicate does not fail, it silently picks "
                          "whichever row the engine reads first — which is not a decision "
                          "anybody made (contract §3, §6 rule 12)"
                    % (code, len(trees), ", ".join(sorted(trees)))))
    if outside:
        out.append((WARN, "%d topography code(s) are owned by a tree but are outside the "
                          "Group III sweep: %s" % (len(outside), ", ".join(outside))))

    for tree_id, expected in sorted(GROUP3_TREE_TOPOGRAPHY.items()):
        got = declared.get(tree_id)
        if got is None:
            out.append((WARN, "contract §3 names tree %r, which declares no topography in "
                              "this file" % tree_id))
            continue
        if got != set(expected):
            out.append((WARN, "tree %r owns %s; contract §3 gives it %s. The sweep above is "
                              "the binding rule, but a divergence from the contract table "
                              "means one of the two documents is now wrong"
                        % (tree_id, ", ".join(sorted(got)) or "nothing",
                           ", ".join(expected))))

    if [f for f in out if f[0] == FAIL]:
        return out
    out.append((OK, "topography map is total and disjoint: all %d recordable code(s) in "
                    "the Group III sweep (C70.0-C70.9, C71.0-C71.9, C72.0-C72.9, "
                    "C75.1-C75.3, C80.9, less the %d that Layer 1 does not carry) resolve "
                    "to exactly one of %d tree(s) (rule 12)"
                % (len(sweep), len(dropped), len(declared))))
    return out


# -- rule 13 / rule 8 — the ICD-O-3.2 round-trip -----------------------------------------

def check_icdo32_round_trip(ctx: DTContext, layer1: Path):
    """
    RULES 13 and 8 — every (morphology_code, morphology_name, behavior_code) triple the
    engine can emit exists VERBATIM in icdo32.sqlite (contract §5.2, §6 rules 8 and 13).

    This SUPERSEDES check_redcap_exact_names() for Group 3, and it is strictly stronger.
    The REDCap check asks "does this name match the option string" and therefore inherits
    whatever the option list carries — including the 28 (code, term) pairs in circulation
    that ICD-O-3.2 does not have. This one asks "is this a real ICD-O-3.2 term for this
    code at this behaviour", which the option list cannot answer for itself. Groups 1 and 2
    keep the REDCap check exactly as it was; nothing here runs on them.

    EXTENDED TO GROUP 4 (Group 4 build contract §1.1a): "Groups 1 and 2 keep their
    current check_redcap_exact_names behaviour — this must not regress them" is §8 rule
    7's own wording, so the extension is the group-scoping guard below admitting GROUP4
    alongside GROUP3 — nothing else in this function changes, and §0.3's four REDCap/
    ICD-O-3.2 divergences (Middle ear paraganglioma, Carotid body paraganglioma,
    Ganglioneuroblastoma vs Ganglioneuroma, Teratoid medulloepithelioma) are exactly the
    kind of drift this check exists to catch instead of inherit.

    EXTENDED TO GROUP 6 (Group 6 build contract §8, 22 September 2026): the same move,
    for the same reason, at greater scale. §2C names eight REDCap-string drifts —
    8122, 8130, 8131, 8155, 8240, 8311, 8504, 8963 — the largest Layer 1 split of any
    group built so far, and two of the eight (8311, 8504) name a DIFFERENT lesion from
    the one the code now carries under ICD-O-3.2 (§0.5's own correction is the 8311
    case: REDCap's option string is the obsolete 8311/1 "Hypernephroid tumor", a
    different disease from the 8311/3 molecularly defined renal cell carcinoma this
    entry now carries). Under check_redcap_exact_names() correct data cannot pass for
    this group; under this check it does, because the question is "is this a real
    ICD-O-3.2 term", not "does this match a REDCap string that may itself be stale."
    GROUP6 joins GROUP3 and GROUP4 in the guard below — again, nothing else in this
    function changes.

    EXTENDED TO GROUP 7 (Group 7 build contract §2E, 2 October 2026): ten REDCap-string
    drifts (8122, 8155, 8158, 8162, 8170, 8240, 8482, 8504, 8963, 8970), among them an
    [obs] synonym as the label for 8162 and for 8482, and a string ICD-O-3.2 does not
    carry at any level for 8970 ("Hepatoblastoma"; the term is "Hepatoblastoma, NOS").
    GROUP7 joins the guard, nothing else changes. Group 5 is explicitly NOT added here: its four option strings
    already match both sources, so extending it would change nothing it validates and
    the contract for this branch says leave that decision to Group 5's own branch.

    Rule 8: the comparison keys off the database and off NOTHING in the file. No flag
    exempts a name. `redcap_option_verified`, whatever it says, is not read here — that
    flag was authored to mean "not yet checked" and was read as "exempt from checking",
    and six drifted names passed a green build on the strength of it.

    THE ONE EXEMPTION, and how it collapses. ICD-O-3.2 misspells 9475/3's preferred term
    ("Medullobloastoma"). The entry displays the corrected spelling and carries the source
    string in `source_term`; the round-trip runs against `source_term`. That exemption
    rests on three things, all re-checked on every build:
        * only the (code, behaviour) pairs named in ICDO32_SOURCE_TERM_EXEMPTIONS may carry
          a `source_term` at all — otherwise it is a general escape hatch, which is a hole;
        * the `source_term` must be the exact string the contract names AND must still
          exist in icdo32.sqlite for that pair;
        * the corrected `morphology_name` must still be ABSENT from icdo32.sqlite.
    Fix the typo upstream and the third condition fails, so the exemption FAILS rather than
    quietly outliving its reason. An exemption that cannot collapse is a hole (data.md §5A).
    """
    # GROUP8 joins the guard (Group 8 build contract §1, §7): morphology_name is the
    # ICD-O-3.2 preferred term and viii_morph drifts from it on nine codes (§2).
    # GROUP10 joins on the same ground (Group 10 build contract §5).
    if ctx.group not in ROUND_TRIP_GROUPS:
        return []
    index, err = load_icdo32(layer1)
    if err:
        return [(WARN, "RULE 13 could not run: %s. morphology_name is NOT validated for "
                       "this group — check_redcap_exact_names() steps aside for Group 3, "
                       "Group 4 and Group 6 (contract §5.2, §1.1a, Group 6 build "
                       "contract §8) on the understanding that this check replaces it, "
                       "so with the database absent nothing is checking the names at all"
                 % err)]

    out, checked, matched = [], 0, 0
    exempt_pairs = set(ICDO32_SOURCE_TERM_EXEMPTIONS)

    def verify(code, beh, name, what, extra_terms=None):
        nonlocal checked, matched
        if code is None or name is None:
            return
        checked += 1
        terms = index.get((code, str(beh).strip() if beh is not None else None))
        if terms is None and beh is None:
            terms = {}
            for (c, b), bucket in index.items():
                if c == code:
                    terms.update(bucket)
        matrix = ICDO32_MATRIX_RULE.get((ctx.group, code, str(beh).strip() if beh is not None else None))
        if not terms and matrix:
            source = index.get((code, matrix[0])) or {}
            if name == matrix[1] and name in source:
                matched += 1
            else:
                out.append((FAIL, "%s: %s/%s is a matrix-rule entry anchored on %r at %s/%s, "
                                  "which icdo32.sqlite no longer carries under that name (or the "
                                  "entry's name %r differs) — the ruling has lost its anchor"
                            % (what, code, beh, matrix[1], code, matrix[0], name)))
            return
        if not terms:
            out.append((FAIL, "%s: ICD-O-3.2 carries no term at all for %s/%s — the triple "
                              "cannot round-trip because the pair does not exist "
                              "(contract §6 rule 13)" % (what, code, beh)))
            return
        if name in terms:
            matched += 1
            level, obs = terms[name]
            if obs:
                out.append((WARN, "%s: %r is an OBSOLETE ICD-O-3.2 term for %s/%s (marked "
                                  "%s, level %s). It round-trips, but it is not what the "
                                  "tool should be putting on screen"
                            % (what, name, code, beh, obs, level or "?")))
            return
        near = _nearest(name, terms)
        detail = ""
        if near:
            detail = ("\n               ICD-O-3.2 has  : %r\n"
                      "               the two differ only in case, punctuation, spacing or "
                      "tumour/tumor" % near)
        out.append((FAIL, "%s: the triple (%s, %r, %s) does not exist in ICD-O-3.2. RULE 13 "
                          "— every name the engine can emit must be a real term for that "
                          "code at that behaviour, checked against the database and not "
                          "against the REDCap option list, which carries 28 (code, term) "
                          "pairs ICD-O-3.2 does not (contract §5.2, §6 rule 13).%s"
                    % (what, code, name, beh, detail)))

    # code -> {name: behaviour} as THIS FILE authors it. A nos_fallback names a code and
    # a name but carries no behaviour of its own, and guessing one — taking the first
    # entry on the code, say — invents a triple nobody wrote and then fails it. The
    # behaviour comes from the entry the fallback's own name identifies; a name that
    # matches no entry on that code is the real defect, because the fallback would print
    # a name this file does not carry.
    entry_names: dict = {}
    for entry in ctx.entries:
        if not isinstance(entry, dict):
            continue
        c = as_code(entry.get("morphology_code"))
        n = entry.get("morphology_name")
        b = entry.get("behavior_code")
        if c and isinstance(n, str) and b is not None:
            entry_names.setdefault(c, {})[n] = str(b).strip()

    def verify_fallback(code, name, declared_beh, what):
        if code is None or not isinstance(name, str):
            return
        if declared_beh is not None:
            verify(code, str(declared_beh).strip(), name, what)
            return
        known = entry_names.get(code) or {}
        if name in known:
            verify(code, known[name], name, what)
            return
        out.append((FAIL, "%s: names %s %r, which is not the morphology_name of any "
                          "morphology_entries[] object on that code in this file (this "
                          "file carries %s). A fallback that prints a name the file does "
                          "not itself carry cannot round-trip, and the clerk is shown a "
                          "string that appears nowhere else (contract §6 rule 13)"
                    % (what, code, name,
                       ", ".join("%r at /%s" % (n, b) for n, b in sorted(known.items()))
                       or "no entry")))

    for i, entry in enumerate(ctx.entries):
        if not isinstance(entry, dict):
            continue
        code = as_code(entry.get("morphology_code"))
        beh = entry.get("behavior_code")
        beh = None if beh is None else str(beh).strip()
        name = entry.get("morphology_name")
        label = "entry %s/%s" % (code or "index %d" % i, beh)

        source_term = entry.get("source_term")
        pair = (code, beh)
        if source_term is not None:
            if pair not in exempt_pairs:
                out.append((FAIL, "%s: carries a `source_term`, but %s/%s is not the one "
                                  "declared name exemption (contract §5.3 exempts only %s). "
                                  "A `source_term` that any entry may add is a general "
                                  "escape hatch from rule 13 — and a flag that exempts a "
                                  "name is exactly what rule 8 forbids"
                            % (label, code, beh,
                               ", ".join("%s/%s" % p for p in sorted(exempt_pairs)))))
            else:
                spec = ICDO32_SOURCE_TERM_EXEMPTIONS[pair]
                if source_term != spec["source_term"]:
                    out.append((FAIL, "%s: source_term is %r; the exemption is declared "
                                      "against %r (contract §5.3). %s"
                                % (label, source_term, spec["source_term"], spec["why"])))
                if name != spec["morphology_name"]:
                    out.append((WARN, "%s: the §5.3 exemption exists so this entry can "
                                      "display %r; it displays %r"
                                % (label, spec["morphology_name"], name)))
                terms = index.get(pair) or {}
                if spec["source_term"] not in terms:
                    out.append((FAIL, "%s: THE EXEMPTION HAS COLLAPSED — its anchor is that "
                                      "ICD-O-3.2 carries %r for %s/%s, and it does not. "
                                      "Re-read the database and either drop the exemption "
                                      "or re-declare it against what is actually there "
                                      "(contract §5.3, §6 rule 8)"
                                % (label, spec["source_term"], code, beh)))
                elif isinstance(name, str) and name in terms:
                    out.append((FAIL, "%s: THE EXEMPTION IS NO LONGER NEEDED — ICD-O-3.2 now "
                                      "carries %r for %s/%s, so the misspelling it works "
                                      "around has been fixed upstream. Drop `source_term` "
                                      "and let the name round-trip on its own "
                                      "(contract §5.3)" % (label, name, code, beh)))
                else:
                    checked += 1
                    matched += 1
            continue

        verify(code, beh, name, label)

        fb_code = as_code(entry.get("nos_fallback_code"))
        fb_name = entry.get("nos_fallback_name")
        if fb_code and isinstance(fb_name, str):
            verify_fallback(fb_code, fb_name, entry.get("nos_fallback_behavior_code"),
                            "%s nos_fallback_name" % label)

    for node_id, node in sorted(ctx.nodes.items()):
        for holder, where in walk_dicts(node):
            if not is_nos_fallback_object(holder, where):
                continue
            verify_fallback(as_code(holder.get("code")), holder.get("name"),
                            holder.get("behavior_code"),
                            "node %s (%s) nos_fallback" % (node_id, where))

    if [f for f in out if f[0] == FAIL]:
        return out
    out.append((OK, "%d/%d (code, name, behaviour) triple(s) exist verbatim in "
                    "icdo32.sqlite; %d declared name exemption(s), each still anchored to a "
                    "string the database actually carries (rules 8 and 13)"
                % (matched, checked, len(exempt_pairs))))
    return out


# -- contract §1.3 — iccc3_subgroup_by_topography[] --------------------------------------

def check_iccc3_subgroup_by_topography(ctx: DTContext, layer1: Path):
    """
    Contract §1.3 — the one intra-group topography split, checked against ICCC-2017.

    ICCC-3 puts `9380/3` in IIIb at C72.3 and in IIId2 everywhere else. That is one
    (code, behaviour) pair with two subgroups, and the schema allows one entry per pair, so
    the subgroup moves into an ordered, first-match-wins rule list with the entry's own
    `iccc3_subgroup_id` as the default.

    The check is a sweep against ICCC-2017.sqlite, for the same reason rule 12 is a sweep:
    the alternative — pinning 9380 to IIId2 and accepting that an optic nerve glioma
    reports the wrong subgroup — is silently wrong for exactly the cases IIIb exists to
    catch. So for every code in the file, at every one of the 34 topography codes the group
    can carry, the subgroup the rules resolve to must be the subgroup ICCC-2017 assigns.
    That catches the missing rule as well as the wrong one.
    """
    if ctx.group != GROUP3:
        return []
    out, seen = [], 0
    index, err = load_iccc_group3(layer1)

    entries_with_rules = [e for e in ctx.entries
                          if isinstance(e, dict) and "iccc3_subgroup_by_topography" in e]
    if err:
        if entries_with_rules:
            return [(WARN, "iccc3_subgroup_by_topography[] could not be checked against the "
                           "recode table: %s. Shape is validated below, but whether a rule "
                           "names the subgroup ICCC-2017 actually assigns is UNVERIFIED"
                     % err)]
        return [(WARN, "iccc3_subgroup_by_topography[] could not be checked: %s" % err)]

    for i, entry in enumerate(ctx.entries):
        if not isinstance(entry, dict):
            continue
        code = as_code(entry.get("morphology_code"))
        label = "entry %s/%s" % (code or "index %d" % i, entry.get("behavior_code"))
        default_id = entry.get("iccc3_subgroup_id")
        rules = entry.get("iccc3_subgroup_by_topography")
        assigned = index.get(code) or {}

        if rules is None:
            if len(assigned) > 1:
                where = {sid: sorted(t)[:3] for sid, (_n, t) in assigned.items()}
                out.append((FAIL, "%s: ICCC-2017 assigns this code to %d subgroups by "
                                  "topography (%s) and the entry carries no "
                                  "iccc3_subgroup_by_topography[]. One of them is being "
                                  "reported for every case, and it is wrong for exactly the "
                                  "cases the other subgroup exists to catch "
                                  "(contract §1.3)"
                            % (label, len(assigned),
                               "; ".join("%s at %s…" % (sid, ", ".join(t))
                                         for sid, t in sorted(where.items())))))
            continue

        seen += 1
        if not isinstance(rules, list) or not rules:
            out.append((FAIL, "%s: iccc3_subgroup_by_topography must be a non-empty array "
                              "of ordered rules (contract §1.3)" % label))
            continue
        if entry.get("topography_dependent") is not True:
            out.append((FAIL, "%s: carries iccc3_subgroup_by_topography[] but "
                              "topography_dependent is %r. The two say the same thing and "
                              "the renderer reads the flag"
                        % (label, entry.get("topography_dependent"))))
        note = entry.get("topography_routing_note")
        if not isinstance(note, str) or not note.strip():
            out.append((FAIL, "%s: topography_dependent routing requires a "
                              "topography_routing_note saying which way the split runs "
                              "(DT master §6)" % label))

        claimed: dict = {}
        for j, rule in enumerate(rules):
            if not isinstance(rule, dict):
                out.append((FAIL, "%s: iccc3_subgroup_by_topography[%d] is not an object"
                            % (label, j)))
                continue
            codes, bad = _expand_topography(rule.get("topography_in"))
            if bad:
                out.append((FAIL, "%s: iccc3_subgroup_by_topography[%d].topography_in "
                                  "carries %s, which is not a topography code or range"
                            % (label, j, ", ".join(bad))))
            if not codes:
                out.append((FAIL, "%s: iccc3_subgroup_by_topography[%d] has an empty "
                                  "topography_in[] — a rule that matches nothing is inert "
                                  "and reads as live" % (label, j)))
            sid = rule.get("iccc3_subgroup_id")
            sname = rule.get("iccc3_subgroup_name")
            if not isinstance(sid, str) or not sid.strip():
                out.append((FAIL, "%s: iccc3_subgroup_by_topography[%d] has no "
                                  "iccc3_subgroup_id" % (label, j)))
            if not isinstance(sname, str) or not sname.strip():
                out.append((FAIL, "%s: iccc3_subgroup_by_topography[%d] has no "
                                  "iccc3_subgroup_name" % (label, j)))
            elif isinstance(sid, str) and sid in assigned and assigned[sid][0] != sname:
                out.append((FAIL, "%s: iccc3_subgroup_by_topography[%d] names subgroup %s "
                                  "%r; ICCC-2017 labels %s %r"
                            % (label, j, sid, sname, sid, assigned[sid][0])))
            for topo in codes:
                if topo in claimed:
                    out.append((FAIL, "%s: topography %s is claimed by rules[%d] and "
                                      "rules[%d]. The list is first-match-wins, so a "
                                      "duplicate makes rule ORDER decide a subgroup — which "
                                      "is not a decision anybody wrote down "
                                      "(contract §1.3)" % (label, topo, claimed[topo], j)))
                else:
                    claimed[topo] = j

        if not assigned:
            out.append((WARN, "%s: ICCC-2017 has no Group III assignment for this code, so "
                              "the routing rules cannot be checked against the recode table"
                        % label))
            continue

        for topo in GROUP3_TOPOGRAPHY_SWEEP:
            expected = {sid for sid, (_n, covered) in assigned.items() if topo in covered}
            if not expected:
                continue
            resolved = default_id
            for j, rule in enumerate(rules):
                if not isinstance(rule, dict):
                    continue
                codes, _bad = _expand_topography(rule.get("topography_in"))
                if topo in codes:
                    resolved = rule.get("iccc3_subgroup_id")
                    break
            if resolved not in expected:
                which = ("rule %d" % claimed[topo]) if topo in claimed else "the entry's "\
                    "own default"
                out.append((FAIL, "%s at %s resolves to subgroup %r via %s; ICCC-2017 "
                                  "assigns it to %s. A subgroup the recode table does not "
                                  "agree with does not classify — `iccc_code` never "
                                  "populates (contract §1.3)"
                            % (label, topo, resolved, which, "/".join(sorted(expected)))))
                break

    if not seen and not out:
        return []
    if [f for f in out if f[0] == FAIL]:
        return out
    out.append((OK, "%d iccc3_subgroup_by_topography[] rule list(s): every rule names a "
                    "subgroup ICCC-2017 assigns to that code at that topography, and so "
                    "does every entry's own default (contract §1.3)" % seen))
    return out


# --------------------------------------------------------------------------------------
# B4b. Group 4 schema extension (build contract §3) and its nine validation rules (§8).
# Each check is scoped to GROUP4 only, the same way every Group III check above is
# scoped to GROUP3 only — a check that has not been verified against the real file of
# another group must not run over it (this task's own standing rule: do not run the
# real build). Several of these pass VACUOUSLY on a file with no trees yet, or no
# tree yet: an empty decision_trees[] contains no violation of "9504 is unreachable"
# or "no no_tissue terminal breaks the Visser gate", and the functions say so with an
# empty return rather than manufacturing an OK line for something they never looked at.
# --------------------------------------------------------------------------------------

def check_behaviour_exclusion(ctx: DTContext, layer1: Path):
    """
    RULE 1 (contract §3, §8 rule 1, ruling D1) — the `behaviour_exclusion` field.

    It exists because the schema had no way to say "this histological entity exists,
    has a real ICD-O code, and that code's behaviour sits outside the group's own
    declaration" — a ganglioneuroma is 9490/0, and ICCC-3 Group IV admits behaviour 3
    only, so it is not a registrable Group IV cancer and there is no other ICCC-3 group
    to refer it to (§2.1). Six checks on every `behaviour_exclusion` block found
    anywhere in the tree:

        1. all six keys present and non-null (non-empty for the strings);
        2. icdo_code/icdo_behaviour/icdo_term round-trip to icdo32.sqlite, and the term
           must be the database's own PREFERRED term at that (code, behaviour) pair —
           a Synonym or a Related term is a real string but not what the field promises;
        3. icdo_behaviour is NOT a member of the group's own declaration
           (GROUP4_BEHAVIOUR_DECLARED). THIS IS THE SUBTLE ONE: a behaviour_exclusion
           naming an ADMITTED behaviour would hide a code that should have been emitted
           as a real Group IV entry — the field is an escape hatch for behaviours the
           group cannot code, not a second way to skip coding one it can;
        4. the branch does not ALSO carry morphology_code — the two are mutually
           exclusive destinations (app.js's advance() checks morphology_code first, so
           an author who wrote both would never notice the exclusion silently doing
           nothing at runtime);
        5. reason is non-empty — it is CLERK-FACING and rendered on the output panel
           (app.js excludeBehaviour()/renderOutput()), never a coding_note.

    Scoped to `behaviour_exclusion` objects found by walk_dicts() over every node in
    the file of a group that has ADOPTED the field — Group 4 contract §3's last line
    ("Group 4 only. The engine supports it; no other group is obliged to adopt it")
    plus every group that later adopts it on its own evidence.

    GENERALISED 2026-09-22, on the Group 5 branch. Group 5 is the first other adopter
    (Group 5 build contract §2.1, §2.2, §3): ICD-O-3.2 carries `9510/0 Retinocytoma`
    and `9514/1 Retinoblastoma, spontaneously regressed` on stems whose `/3` IS in the
    group, and ICCC-3 Group V admits behaviour 3 only — the same shape as Group IV's
    `9490/0 Ganglioneuroma`. The check was hard-guarded `if ctx.group != GROUP4`, so a
    Group 5 block would have been written and never validated. Generalising was chosen
    over forking for the reason the Group 4 inventory generator was generalised rather
    than copied: a fix made here reaches every adopter at once.

    The group's own declared behaviour set is now read from
    BEHAVIOUR_DECLARED_BY_GROUP rather than from a Group-4-only constant. That set is
    what the subtle clause below tests against, so getting it from the wrong group
    would invert the check. A group NOT in the table is not validated here at all —
    which is the same "no group is obliged to adopt it" position, made explicit.
    """
    declared_behaviours = BEHAVIOUR_DECLARED_BY_GROUP.get(ctx.group)
    if declared_behaviours is None:
        return []
    group_label = ROMAN_BY_GROUP.get(ctx.group, str(ctx.group))
    out = []
    seen = 0
    index, err = load_icdo32(layer1)
    if err:
        out.append((WARN, "RULE 1 could not round-trip icdo_code/icdo_behaviour/"
                          "icdo_term against icdo32.sqlite: %s. The shape, behaviour-"
                          "declaration and reason checks still ran" % err))

    required = ("icdo_code", "icdo_behaviour", "icdo_term", "group_declares",
                "reason", "registrar_decision_required")
    for node_id, node in sorted(ctx.nodes.items()):
        for holder, where in walk_dicts(node):
            be = holder.get("behaviour_exclusion")
            if not isinstance(be, dict):
                continue
            seen += 1
            loc = "node %s (%s) behaviour_exclusion" % (node_id, where)

            missing = []
            for key in required:
                if key not in be or be[key] is None:
                    missing.append(key)
                elif isinstance(be[key], str) and not be[key].strip():
                    missing.append(key)
            if missing:
                out.append((FAIL, "%s is missing, null or empty for %s — all six keys "
                                  "are REQUIRED (contract §3, §8 rule 1)"
                            % (loc, ", ".join(missing))))
            rdr = be.get("registrar_decision_required")
            if rdr is not None and not isinstance(rdr, bool):
                out.append((FAIL, "%s: registrar_decision_required must be a boolean, "
                                  "got %r" % (loc, rdr)))

            code = as_code(be.get("icdo_code"))
            beh = be.get("icdo_behaviour")
            beh_s = None if beh is None else str(beh).strip()
            term = be.get("icdo_term")
            if code and beh_s is not None and isinstance(term, str) and index:
                terms = index.get((code, beh_s))
                if not terms:
                    out.append((FAIL, "%s: ICD-O-3.2 carries no term at all for %s/%s "
                                      "— icdo_code/icdo_behaviour do not round-trip "
                                      "(contract §3, §8 rule 1)" % (loc, code, beh_s)))
                elif term not in terms:
                    near = _nearest(term, terms)
                    out.append((FAIL, "%s: icdo_term %r is not a term ICD-O-3.2 "
                                      "carries for %s/%s.%s (contract §3, §8 rule 1)"
                                % (loc, term, code, beh_s,
                                   ("\n               ICD-O-3.2 has  : %r" % near)
                                   if near else "")))
                else:
                    level, obs = terms[term]
                    if level != "Preferred":
                        out.append((FAIL, "%s: icdo_term %r is a %s term for %s/%s, "
                                          "not the PREFERRED one. Contract §3 requires "
                                          "the Preferred term at that (code, "
                                          "behaviour) pair" % (loc, term, level or "?",
                                                               code, beh_s)))
                    elif obs:
                        out.append((WARN, "%s: icdo_term %r is marked %s in "
                                          "icdo32.sqlite even though it is the "
                                          "Preferred term for %s/%s" % (loc, term, obs,
                                                                        code, beh_s)))

            if beh_s is not None and beh_s in declared_behaviours:
                out.append((FAIL, "%s: icdo_behaviour %r IS in Group %s's own "
                                  "declaration (behaviour %s). A behaviour_exclusion "
                                  "may only name a behaviour the group does NOT "
                                  "admit — naming an admitted one would HIDE a code "
                                  "that should have been emitted as a real Group %s "
                                  "entry instead of excluded (contract §3, §8 rule 1 "
                                  "— the subtle one)"
                            % (loc, beh_s, group_label,
                               "/".join(sorted(declared_behaviours)), group_label)))

            if as_code(holder.get("morphology_code")) is not None:
                out.append((FAIL, "%s: this branch ALSO carries morphology_code %r. "
                                  "behaviour_exclusion and morphology_code are "
                                  "mutually exclusive destinations — app.js's "
                                  "advance() checks morphology_code first, so this "
                                  "exclusion would never fire at runtime (contract "
                                  "§3, §8 rule 1)"
                            % (loc, holder.get("morphology_code"))))

    if not seen and not out:
        return []
    if [f for f in out if f[0] == FAIL]:
        return out
    out.append((OK, "%d behaviour_exclusion block(s) well formed: all six keys "
                    "present, icdo_code/icdo_behaviour/icdo_term round-trip to the "
                    "Preferred ICD-O-3.2 term, the named behaviour is outside the "
                    "group's own declaration, no branch also carries morphology_code, "
                    "and reason is non-empty (rule 1)" % seen))
    return out


def check_group4_behaviour_declaration(ctx: DTContext):
    """
    RULE 2 (contract §1, §8 rule 2) — every `morphology_entries[]` object carries
    `behavior_code` "3", the group's own declaration, and nothing else.

    Unlike Group III (eighteen behaviour-overloaded codes, checked by
    check_group3_behaviour_split() against a per-code set computed from ICD-O-3.2),
    Group IV has NO behaviour-overloaded codes at all (contract §1.2): one entry per
    code, one behaviour for the whole group. So this is a flat membership test, not a
    per-code computation.

    READS the group's declaration rather than hardcoding a bare "3" inline: the
    expected set is GROUP4_BEHAVIOUR_DECLARED, a named constant declared once, above,
    and cited to contract §1 ("Behaviour declaration `3` — exactly one, across every
    Group IV range"). This function itself never writes the literal "3" — it compares
    against that constant, so extending Group IV's own declaration later (it will
    not, contract §1 is explicit that it is exactly one behaviour, but the shape does
    not assume that) is a one-line change here.

    NOT generalised into a cross-group lookup keyed by ctx.group, on purpose. A single
    constant reused as a per-group table would ALSO run this flat membership test over
    Group III, and while Group III's own declaration (GROUP3_BEHAVIOURS_DECLARED,
    {"0","1","3"}) should already hold for every one of its entries as an inherent
    consequence of check_group3_behaviour_split() passing, that has not been verified
    here against the real group_03_dt.json — this task must not run the real build —
    and "do not regress Groups 1-3" is the harder constraint than a marginal reuse of
    one comparison. So: scoped to GROUP4 only, exactly like every other group-specific
    check in this file.
    """
    if ctx.group != GROUP4:
        return []
    out = []
    seen = 0
    declared_label = "/".join(sorted(GROUP4_BEHAVIOUR_DECLARED))
    for i, entry in enumerate(ctx.entries):
        if not isinstance(entry, dict):
            continue
        code = as_code(entry.get("morphology_code"))
        if code is None:
            continue
        seen += 1
        beh = entry.get("behavior_code")
        beh_s = None if beh is None else str(beh).strip()
        if beh_s not in GROUP4_BEHAVIOUR_DECLARED:
            out.append((FAIL, "RULE 2 — morphology_entries[%d] (code %s) carries "
                              "behavior_code %r; Group IV's own declaration is "
                              "behaviour %s and nothing else (contract §1, §8 rule "
                              "2). Any other value files the entry under a "
                              "behaviour ICCC-3 does not register for this group"
                        % (i, code, beh, declared_label)))
    if not seen and not out:
        return []
    if [f for f in out if f[0] == FAIL]:
        return out
    out.append((OK, "%d Group IV morphology_entries[] object(s) all carry "
                    "behavior_code %s, the group's own declaration (rule 2)"
                % (seen, declared_label)))
    return out


def _scan_banned_code(ctx: DTContext, repo: Path, code, scan_nos_fallback,
                              scan_alias_targets, rule, cite, what):
    """
    Shared scanner for RULE 3 (8683) and RULE 8 (9364) — bound to CODE FIELDS by name,
    never to a substring search of the file. Both rules ban the code as something this
    file EMITS — a `morphology_code` (RULE 8), plus a `nos_fallback_code` or an alias
    TARGET (RULE 3 only, per its own wider wording) — never as a string that merely
    appears somewhere in it.

    Prose is exempt, author-facing OR clerk-facing, and that is deliberate, not an
    oversight: neither contract §0.2 (8683) nor §2.4/ruling D4 (9364) says anything
    about text, only about what gets EMITTED (contract §8 rules 3 and 8, each read
    literally — "must not appear as a morphology_code", nothing about `reason`). Both
    codes are real, valid ICD-O-3.2 codes that this group legitimately talks ABOUT: a
    `coding_note` explains why 8683 has no Group IV entry, and a `refer_group` branch's
    `reason` is exactly where 9364 belongs, because Group IV's own pPNET aliases refer
    OUT to Group VIII/IX and the clerk needs to be told what they will find there —
    Group 3 sets the same precedent, naming its own referral targets' codes in its
    `refer_group` `reason` text. Withholding the digits from prose would leave a
    referral with no answer, so a banned code in CLERK-FACING text is a WARN — recorded
    so it can be reviewed, never blocking the build — and author-facing text (never
    displayed at all) is a WARN for the same reason it always was. This split is
    NARROWER than check_group3_absent_codes()'s (rule 7), which does fail clerk-facing
    text: rule 7's codes do not exist in ICD-O-3.2 at all, so naming one in prose can
    only be a mistake with nothing legitimate to protect; 8683 and 9364 are real codes
    with a real, correct reason to be named. `alias`/`also_known_as` are never scanned
    — those are what a clerk TYPES, not what the tool emits.
    """
    out, hits = [], 0
    rx = _code_token_re(code)
    code_keys = ["morphology_code"]
    if scan_nos_fallback:
        code_keys.append("nos_fallback_code")
    if scan_alias_targets:
        code_keys.append("maps_to_morphology_codes")

    scope_bits = ["a morphology_code"]
    if scan_nos_fallback:
        scope_bits.append("a nos_fallback_code")
    if scan_alias_targets:
        scope_bits.append("an alias target")
    scope_label = (scope_bits[0] if len(scope_bits) == 1 else
                   ", ".join(scope_bits[:-1]) + " or " + scope_bits[-1])

    def scan(container, where):
        nonlocal hits
        for holder, path in walk_dicts(container):
            for key, value in holder.items():
                if key in ALIAS_INPUT_KEYS:
                    continue
                loc = "%s%s.%s" % (where, ("." + path) if path else "", key)
                if key in code_keys:
                    candidates = value if isinstance(value, list) else [value]
                    for cand in candidates:
                        if as_code(cand) == code:
                            hits += 1
                            out.append((FAIL, "%s — %s carries code %s. %s (%s)"
                                        % (rule, loc, code, what, cite)))
                    continue
                if not isinstance(value, str) or not rx.search(value):
                    continue
                if key in AUTHOR_FACING_TEXT_KEYS:
                    out.append((WARN, "%s — %s mentions %s in author-facing text. "
                                      "That is fine and expected — this field is "
                                      "never displayed, so no clerk reads it, and "
                                      "the contract's own reasoning for excluding "
                                      "the code is written in exactly these terms "
                                      "(%s)" % (rule, loc, code, cite)))
                elif key in CLERK_FACING_TEXT_KEYS:
                    out.append((WARN, "%s — %s prints %s in text a clerk reads. That "
                                      "is fine and expected — %s bans %s only as %s, "
                                      "never in prose, and naming the destination "
                                      "code in a `reason`/`hint` is how a referral or "
                                      "an exclusion tells the clerk what to expect "
                                      "(%s)" % (rule, loc, code, rule, code, scope_label,
                                                cite)))

    scan(ctx.data, ctx.name)
    if scan_alias_targets:
        alias_path = Path(repo) / "data" / "aliases" / ("aliases_group_%02d.json" % ctx.group)
        if alias_path.exists():
            data, findings = load_json(alias_path)
            out.extend(findings)
            if data is not None:
                entries = data.get("aliases") if isinstance(data, dict) else data
                if isinstance(entries, list):
                    for i, entry in enumerate(entries):
                        if isinstance(entry, dict):
                            scan(entry, "%s[%d]" % (alias_path.name, i))

    if [f for f in out if f[0] == FAIL]:
        return out
    if hits:
        return out
    return out + [(OK, "%s — %s appears nowhere as %s in group_04_dt.json%s (%s)"
                   % (rule, code, scope_label,
                      " or its alias file" if scan_alias_targets else "", cite))]


def check_group4_absent_codes(ctx: DTContext, repo: Path):
    """
    RULE 3 (contract §0.2, §8 rule 3) — `8683` appears NOWHERE as a `morphology_code`,
    a `nos_fallback_code`, or an alias TARGET.

    ICD-O-3.2 carries 8683 only at behaviour /0 (Gangliocytic paraganglioma); ICCC-3
    Group IV admits behaviour 3 only, so there is no 8683/3 and no Group IV entry for
    it at all (§0.2 — IARC's own *Summary of main changes* names 8683/0 as the single
    deliberate survivor of the whole 868-870 block, and WHO 2022 independently renamed
    the entity CoGNET). It remains legitimate as an ALIAS INPUT and, in ANY prose —
    author-facing or clerk-facing — explaining the exclusion; the contract bans 8683
    only from the three EMITTING fields named above, never from text. See
    _scan_banned_code().
    """
    if ctx.group != GROUP4:
        return []
    return _scan_banned_code(
        ctx, repo, GROUP4_ABSENT_CODE,
        scan_nos_fallback=True, scan_alias_targets=True,
        rule="RULE 3", cite="contract §0.2, §8 rule 3",
        what="ICD-O-3.2 carries 8683 only at /0 (Gangliocytic paraganglioma); ICCC-3 "
             "Group IV admits behaviour 3 only, so there is no Group IV entry for it")


def check_group4_not_a_group_code(ctx: DTContext, repo: Path):
    """
    RULE 8 (contract §2.4, §8 rule 8, ruling D4) — `9364` is not a Group IV code and
    must not appear as a `morphology_code` in `group_04_dt.json`.

    IARC's *Summary of main changes* states plainly that Ewing sarcoma moved to
    9364/3 and that 9364 is now also the code for peripheral neuroectodermal tumour /
    pPNET. Group IV's own "peripheral PNET" aliases (alias-instruction entries 30, 31,
    33) resolve through a CROSS-GROUP REFERRAL — Group VIII at bone, Group IX at soft
    tissue — never through a Group IV `morphology_code`. Narrower scope than rule 3:
    9364 is a real, valid code that `refer_code`, `reason`, `hint` and D4's own
    `coding_note` reasoning may all legitimately carry — the contract's own wording
    ("must not appear as a `morphology_code`") binds one field, not the file's prose —
    so only the emitting field is bound, and neither nos_fallback_code nor the alias
    file is scanned (a Group IV alias file entry naming 9364 as WHERE THE CASE GOES,
    via refer_group/refer_code, is exactly D4's design, not a violation of it).
    """
    if ctx.group != GROUP4:
        return []
    return _scan_banned_code(
        ctx, repo, GROUP4_NOT_A_GROUP_CODE,
        scan_nos_fallback=False, scan_alias_targets=False,
        rule="RULE 8", cite="contract §2.4, §8 rule 8",
        what="ICD-O-3.2 moved Ewing sarcoma to 9364/3 and made it the peripheral "
             "neuroectodermal tumour / pPNET code too (ruling D4); Group IV's pPNET "
             "aliases refer OUT to Group VIII/IX rather than emitting it here")


def check_group4_9504_unreachable(ctx: DTContext):
    """
    RULE 4 (contract §2.3, ruling D2, §8 rule 4) — `9504` Spongioneuroblastoma is
    authored in `morphology_entries[]` (so an alias on the string, or a historical
    record carrying the code, can resolve) and REACHABLE FROM NO TREE. ICD-O-3.2 does
    not mark it `[obs]`, so the Group III absent-code test does not remove it — but no
    current WHO entity lives on the stem, so the Group 3 `obsolete_term` precedent
    (thirteen entries, same shape) governs instead.

    Checked at every place a case could actually be handed the code: a direct
    `morphology_code` emission anywhere in the tree (ctx.emissions(), which already
    walks every node's options, resolution_logic[], bands[] and branches — "no
    next_node, resolution rule, option, branch or terminal" in the contract's own
    words), a NODE-level nos_fallback (the {"code","name","reason"} object hung off a
    node's own `nos_fallback` key), and an ENTRY-level `nos_fallback_code` (some other
    code's fallback destination named on the morphology_entries[] object itself). Any
    of the three would hand a clerk 9504 from a live path.
    """
    if ctx.group != GROUP4:
        return []
    out = []
    for code, holder, node_id, where in ctx.emissions():
        if code == GROUP4_UNREACHABLE_CODE:
            out.append((FAIL, "RULE 4 — node %s (%s) emits morphology_code %s. "
                              "Spongioneuroblastoma is authored in "
                              "morphology_entries[] and reachable from NO tree — no "
                              "current WHO entity lives on the stem (contract §2.3, "
                              "ruling D2, §8 rule 4)" % (node_id, where, code)))
    for node_id, node in sorted(ctx.nodes.items()):
        for holder, where in walk_dicts(node):
            if is_nos_fallback_object(holder, where) and \
                    as_code(holder.get("code")) == GROUP4_UNREACHABLE_CODE:
                out.append((FAIL, "RULE 4 — node %s (%s) nos_fallback names code %s. "
                                  "Same rule as a direct emission: %s is reachable "
                                  "from no tree (contract §2.3, ruling D2, §8 rule 4)"
                            % (node_id, where, GROUP4_UNREACHABLE_CODE,
                               GROUP4_UNREACHABLE_CODE)))
    for i, entry in enumerate(ctx.entries):
        if isinstance(entry, dict) and \
                as_code(entry.get("nos_fallback_code")) == GROUP4_UNREACHABLE_CODE:
            out.append((FAIL, "RULE 4 — morphology_entries[%d] (code %s) declares "
                              "nos_fallback_code %s. An entry-level fallback IS a "
                              "live path to the code, and %s must be reachable from "
                              "no tree at all (contract §2.3, ruling D2, §8 rule 4)"
                        % (i, as_code(entry.get("morphology_code")),
                           GROUP4_UNREACHABLE_CODE, GROUP4_UNREACHABLE_CODE)))
    if out:
        return out
    if not ctx.nodes:
        return []
    return [(OK, "%s (Spongioneuroblastoma) is unreachable: no morphology_code "
                 "emission, node-level nos_fallback or entry-level nos_fallback_code "
                 "anywhere in the file names it (rule 4)" % GROUP4_UNREACHABLE_CODE)]


def check_group4_topography_map(ctx: DTContext, repo: Path):
    """
    RULE 5 (contract §5, §8 rule 5) — the four-tree topography map is TOTAL and
    DISJOINT over every topography Group IV can carry, 9501-9504 are unreachable from
    any tree whose declared topography sits inside C70.0-C72.9 — that band belongs to
    Group III (contract §0.6, §2.5) — and the router names a working catch-all for
    everything the map does not enumerate.

    REVISED 2026-09-18 — the original sweep here generated every C00.0-C80.9 slot and
    swept it against Layer 1's REDCap topography list, which is the whole REGISTRY's
    topography universe, not Group IV's: C50.x breast, C34.x lung and C61.9 prostate
    all came back "resolve to NO tree", 292 of them, none a Group IV defect, because no
    Group IV tree was ever meant to claim them. Two things that sweep got wrong, now
    fixed:

    1. Group IV's four trees positively claim only the codes `topography_codes.json`'s
       `topography_lookup` names for group 4 (34 of them) — read by
       _group4_candidate_topography() rather than hand-transcribed, for the same
       reason a Group-IV analogue of GROUP3_TREE_TOPOGRAPHY is not hand-built here:
       transcribing C10/C11/C30-C32/C38/C47/C48/C74/C75/C77's own subcodes from memory
       is exactly the kind of recall this file's own design note (top of file) says
       never to trust for a check. That 34-code universe, not the whole topography
       space, is what "TOTAL and DISJOINT" is swept over below.
    2. Everything else Group IV can carry — contract §5's own words — is NOT covered
       by an enumerated list at all: it reaches `g4_other_peripheral` through
       presentation_router.json's `groups["4"].tree_routing.default`, exactly the
       mechanism app.js's own `routedTree()` refuses to run without (it throws
       "declares no default tree" when `tr.default` is missing). So the second half of
       this check reads that same `default` and fails if it is missing or names a tree
       this file does not declare — a group whose trees do not cover everything and
       which declares no catch-all IS a dead end, and it has to fail exactly like an
       unrouted code does. (The generic cross-layer check_presentation_router() already
       verifies an EXISTING default's entry_node resolves to a document_inventory node
       and that its tree_id is declared in metadata — this check adds the one thing
       that check cannot: that a default exists at all, and, as a Group-4-scoped
       sanity check tied to the disjoint/total sweep above, that it names a tree this
       file actually has.)

    The C70-72 cross-check is unchanged: it reuses the SAME `declared` map — any tree
    whose own declared topography intersects C70.0-C72.9 must never still emit 9501,
    9502, 9503 or 9504 from a node inside it. Bound to direct morphology_code emissions
    (ctx.emissions()), matching the contract's own, simpler wording here (unlike rule
    4, this clause does not separately name nos_fallback paths).
    """
    if ctx.group != GROUP4:
        return []
    out = []
    declared: dict = {}

    def take(tree_id, holder):
        for key in TREE_TOPOGRAPHY_KEYS:
            if key not in holder:
                continue
            codes, bad = _expand_topography(holder[key])
            for token in bad:
                out.append((FAIL, "RULE 5 — tree %r: %s carries %s, which is not a "
                                  "topography code or an ascending range of them "
                                  "(expected e.g. \"C74.9\" or \"C38.1-C38.3\")"
                            % (tree_id, key, token)))
            if codes:
                declared.setdefault(tree_id, set()).update(codes)
            return

    for item in ctx.metadata.get("decision_trees") or []:
        if isinstance(item, dict):
            tid = item.get("tree_id") or item.get("id")
            if isinstance(tid, str):
                take(tid, item)
    for tree in ctx.trees:
        raw = None
        for candidate in ctx.data.get("decision_trees") or []:
            if isinstance(candidate, dict) and \
                    (candidate.get("tree_id") or candidate.get("id")) == tree["tree_id"]:
                raw = candidate
                break
        if isinstance(raw, dict) and tree["tree_id"] not in declared:
            take(tree["tree_id"], raw)

    if not declared:
        if not ctx.nodes:
            return []
        return [(FAIL, "RULE 5 — no tree in this file declares the topography it "
                       "owns, so the map cannot be swept. The router picks the "
                       "Group IV tree from the topography captured at Stage 1; with "
                       "no map, every case enters whichever tree the engine reads "
                       "first. Declare it under one of: %s (contract §5, §8 rule 5)"
                 % ", ".join(TREE_TOPOGRAPHY_KEYS))]

    owners: dict = {}
    for tree_id, codes in declared.items():
        for code in codes:
            owners.setdefault(code, []).append(tree_id)

    # -- the universe: what Group IV can actually carry (contract §5), not the whole
    # registry's topography space — see this function's own docstring and the retired
    # GROUP4_TOPOGRAPHY_SWEEP comment for why a hand-written or REDCap-wide sweep is
    # exactly the false-FAIL this rule must not reproduce.
    universe, all_topo_codes, topo_findings = _group4_candidate_topography(repo)
    out.extend(topo_findings)
    if universe:
        sweep = sorted(universe)
    else:
        sweep = sorted(set().union(*declared.values()))
        out.append((WARN, "RULE 5 — data/shared/topography_codes.json's "
                          "topography_lookup could not be read, so the sweep falls "
                          "back to the codes this file's own trees declare. A real "
                          "Group IV topography that no tree owns would not be caught"))

    unrouted = [c for c in sweep if not owners.get(c)]
    duplicated = [(c, owners[c]) for c in sweep if len(owners.get(c, [])) > 1]
    outside = sorted(set(owners) - set(sweep))
    # A code a tree claims that is not even a real topography code at all (a typo, or
    # a stale sub-code) — checked against the FULL lookup, not just Group IV's 34, so
    # this catches the mistake regardless of which group the typo happens to resemble.
    unreal = sorted(c for c in owners if all_topo_codes and c not in all_topo_codes)

    if unrouted:
        out.append((FAIL, "RULE 5 — %d topography code(s) resolve to NO tree: %s. A "
                          "case at one of these reaches the router, finds no handoff "
                          "and dead-ends (contract §5, §8 rule 5)"
                    % (len(unrouted), ", ".join(unrouted))))
    for code, trees_ in duplicated:
        out.append((FAIL, "RULE 5 — topography %s resolves to %d trees (%s). The map "
                          "must be disjoint: a duplicate does not fail, it silently "
                          "picks whichever row the engine reads first — which is not "
                          "a decision anybody made (contract §5, §8 rule 5)"
                    % (code, len(trees_), ", ".join(sorted(trees_)))))
    for code in unreal:
        out.append((FAIL, "RULE 5 — tree(s) %s declare topography %s, which is not in "
                          "data/shared/topography_codes.json at all — a case can never "
                          "actually carry it, so the code that would route it there is "
                          "untested and probably wrong (contract §5, §8 rule 5)"
                    % (", ".join(sorted(owners[code])), code)))
    if outside:
        out.append((WARN, "%d topography code(s) are owned by a tree but are "
                          "outside the sweep: %s" % (len(outside), ", ".join(outside))))

    # -- the catch-all: everything the 34-code universe above does NOT enumerate has
    # to still resolve, through presentation_router.json's own declared default —
    # never through an enumerated list (contract §5's "g4_other_peripheral is the
    # catch-all"). app.js's routedTree() itself refuses to run without one; this is
    # that same requirement, checked at build time instead of discovered by a clerk.
    router, router_findings = load_json(Path(repo) / "data" / "shared"
                                         / "presentation_router.json")
    out.extend(router_findings)
    if router is not None:
        group_meta = (router.get("groups") or {}).get(str(GROUP4))
        tr = group_meta.get("tree_routing") if isinstance(group_meta, dict) else None
        default = tr.get("default") if isinstance(tr, dict) else None
        if not isinstance(default, dict) or not default.get("tree_id"):
            out.append((FAIL, "RULE 5 — presentation_router.json "
                              "groups[\"4\"].tree_routing declares no usable "
                              "'default'. Group IV's trees claim only %d of the "
                              "topography codes it can carry (contract §5: "
                              "\"C00.0-C80.9 for fourteen of its eighteen codes\") — "
                              "without a declared catch-all, a case whose topography "
                              "is not one of those %d reaches the router, finds no "
                              "handoff and dead-ends, exactly as app.js's own "
                              "routedTree() refuses to run without one (contract §5, "
                              "§8 rule 5)" % (len(universe), len(universe))))
        else:
            known_trees = {t["tree_id"] for t in ctx.trees} | set(ctx.metadata_tree_ids)
            if ctx.nodes and default["tree_id"] not in known_trees:
                out.append((FAIL, "RULE 5 — presentation_router.json "
                                  "groups[\"4\"].tree_routing.default names tree_id "
                                  "%r, which %s does not declare. The catch-all for "
                                  "everything else Group IV can carry would route to "
                                  "a tree that does not exist in this file (contract "
                                  "§5, §8 rule 5)" % (default["tree_id"], ctx.name)))

    g3_trees = {tid for tid, codes in declared.items()
                if codes & set(GROUP4_G3_OVERLAP_TOPOGRAPHY)}
    if g3_trees:
        g3_nodes = {nid for nid, tid in ctx.node_tree.items() if tid in g3_trees}
        for code, holder, node_id, where in ctx.emissions():
            if node_id in g3_nodes and code in GROUP4_G3_OVERLAP_CODES:
                out.append((FAIL, "RULE 5 — node %s (%s) in tree %r emits %s. This "
                                  "tree declares topography inside C70.0-C72.9, "
                                  "which belongs to Group III (contract §0.6, "
                                  "§2.5) — 9501-9504 must be unreachable from any "
                                  "node there" % (node_id, where,
                                                  ctx.node_tree[node_id], code)))

    if [f for f in out if f[0] == FAIL]:
        return out
    out.append((OK, "topography map is total and disjoint: all %d Group IV "
                    "candidate topography code(s) resolve to exactly one of %d "
                    "tree(s), the router's default catch-all resolves to a tree this "
                    "file declares, and no tree declaring C70.0-C72.9 emits "
                    "9501-9504 (rule 5)" % (len(sweep), len(declared))))
    return out


def check_imaging_pathway_shape(ctx: DTContext):
    """
    GROUP 5 RULE 1 (Group 5 build contract §0.6, §8 rule 1) — an `imaging_pathway` node
    must declare `insufficient_next_node` and must NOT declare `options[]`.

    THIS IS AN ENGINE FACT, NOT A GROUP 5 FACT, so it is swept over every group.

    app.js resolves `imaging_pathway` at `case 'imaging_pathway'`: a ticked diversion
    criterion or an incomplete constellation goes to `fallbackTarget(n)`; a complete one
    advances to the node itself. `options[]` IS NEVER CONSULTED — `imagingPathway()`
    renders only `imaging_features`, `biochemical_questions` and `diversion_criteria`.
    And `fallbackTarget()` tries `insufficient_next_node`, then `nos_fallback`, then
    THROWS. `nos_fallback` is forbidden on this node type by NOS_FORBIDDEN_TYPES. So a
    node with neither crashes at runtime, on the common path — ticking any diversion
    feature is the ordinary outcome, not an edge case.

    Three Group 3 nodes are in exactly that state (`pf_imaging_no_tissue`,
    `st_imaging_pathway`, `sp_imaging_no_tissue`: 6, 4 and 4 dead options each, no
    `insufficient_next_node`), and one of the dead options is the AFP / beta-hCG germ
    cell referral the Group 3 contract calls load-bearing. docs/TODO.md §10 proposed
    this rule when it found them; this is that rule. Group 3 is merged to `main` and is
    outside the Group 5 branch, so:

        group 5  -> FAIL. The group's whole modal pathway is this node type.
        others   -> WARN. Reported, does not block a branch that cannot fix them.

    The asymmetry is deliberate and is the only thing in this check that is not uniform.
    A silent pass for Groups 1-4 would let the same defect be authored again; a FAIL
    would break a build over a file this branch does not own.
    """
    out, seen = [], 0
    level = FAIL if ctx.group == GROUP5 else WARN
    for node_id, node in sorted(ctx.nodes.items()):
        if node.get("node_type") != "imaging_pathway":
            continue
        seen += 1
        if not node.get("insufficient_next_node"):
            out.append((level, "RULE 1 — imaging_pathway %s declares no "
                               "insufficient_next_node. fallbackTarget() then falls to "
                               "nos_fallback, which is forbidden on this node type, and "
                               "THROWS 'Node has no fallback and did not resolve'. Any "
                               "ticked diversion criterion or incomplete constellation "
                               "crashes the tool (contract §0.6, §8 rule 1)" % node_id))
        opts = node.get("options")
        if isinstance(opts, list) and opts:
            out.append((level, "RULE 1 — imaging_pathway %s declares %d option(s). "
                               "app.js's imagingPathway() renders imaging_features, "
                               "biochemical_questions and diversion_criteria and NEVER "
                               "renders options[]; every one of these is dead and its "
                               "destination unreachable (contract §0.6, §8 rule 1)"
                        % (node_id, len(opts))))
    if not seen:
        return []
    if not out:
        out.append((OK, "%d imaging_pathway node(s): each declares "
                        "insufficient_next_node and none declares options[] (rule 1)"
                    % seen))
    return out


def check_group5_code_set(ctx: DTContext):
    """
    GROUP 5 RULE 3 (contract §0.4, §2.4, §8 rule 3) — two clauses, and the second is the
    one that matters most in this group.

    (a) Every code Group V emits is one of 9510, 9511, 9512, 9513. The inventory is
        GENERATED — build/generate_group_inventory.py --group V joins ICCC-2017.sqlite to
        icdo32.sqlite and returns exactly four usable (code, behaviour) records — so any
        fifth code is either fabricated or is 9514, which rule 4 handles by name.

    (b) A terminal at basis 1 or basis 2 emits 9510 AND NOTHING ELSE. Visser O, et al.
        Front Oncol 2023;13:1250549, Table 3, pp. 04-05 gives retinoblastoma basis
        "1 or 2" at C69.2 for `9510/3`; it licenses no other Group V code without
        pathology. Retinoblastoma is one of only five entities in the whole ENCR scheme
        admitting basis 1, so this group has unusual latitude — and the latitude is
        code-specific.

    WHY (b) IS THE ONE TO HAVE. 9511 differentiated and 9512 undifferentiated are
    differentiation GRADES and 9513 diffuse is a GROWTH PATTERN; all three are readable
    only on an enucleation specimen. A subtype emitted from the imaging or clinical route
    would travel downstream as a graded, enucleation-confirmed tumour when no eye was
    ever removed — a case reading as better evidenced than it is, which is the defect
    class this repository has been bitten by before.

    Keyed off the EFFECTIVE basis: a branch inherits its node's value where it declares
    none, the same rule check_imaging_terminals() uses, because both placements are
    legitimate and the trees use both.
    """
    if ctx.group != GROUP5:
        return []
    out, seen = [], 0

    for code, holder, node_id, where in ctx.emissions():
        if code not in GROUP5_CODES:
            out.append((FAIL, "RULE 3a — node %s (%s) emits %s, which is not a Group V "
                              "code. The generated inventory is exactly %s "
                              "(contract §0.2, §8 rule 3)"
                        % (node_id, where, code, ", ".join(sorted(GROUP5_CODES)))))

    for node_id, node in sorted(ctx.nodes.items()):
        holders = [(node, "(node level)")] + list(_branch_containers(node))
        nos = node.get("nos_fallback")
        if isinstance(nos, dict):
            holders.append((nos, "nos_fallback"))
        for holder, where in holders:
            code = as_code(holder.get("morphology_code")) or as_code(holder.get("code"))
            if code is None:
                continue
            basis = holder.get("basis_of_diagnosis")
            if basis is None and holder is not node:
                basis = node.get("basis_of_diagnosis")
            if not isinstance(basis, int) or isinstance(basis, bool):
                continue
            if basis not in GROUP5_NO_PATHOLOGY_BASES:
                continue
            seen += 1
            if code != GROUP5_NO_PATHOLOGY_CODE:
                out.append((FAIL, "RULE 3b — node %s (%s) emits %s at basis %d. Visser "
                                  "2023 Table 3 (pp. 04-05) licenses a no-pathology "
                                  "retinoblastoma registration for 9510/3 ONLY. %s is a "
                                  "differentiation grade or growth pattern readable only "
                                  "on an enucleation specimen, so this records a graded, "
                                  "enucleation-confirmed tumour for a case where no eye "
                                  "was removed (contract §0.4, §2.4, §8 rule 3)"
                            % (node_id, where, code, basis, code)))

    if not out:
        out.append((OK, "RULE 3 — every emitted code is in {%s}; %d terminal(s) at basis "
                        "1 or 2 emit 9510 and nothing else (Visser Table 3)"
                    % (", ".join(sorted(GROUP5_CODES)), seen)))
    return out


def check_group5_absent_codes(ctx: DTContext, repo: Path):
    """
    GROUP 5 RULE 4 (contract §0.2, §2.2, §8 rule 4) — `9514` appears NOWHERE as a
    `morphology_code`, a `nos_fallback_code`, or an alias TARGET.

    ICD-O-3.2 carries 9514 at one behaviour only: `9514/1`, Preferred term
    "Retinoblastoma, spontaneously regressed". ICCC-3 Group V declares behaviour 3, so
    there is no `9514/3` and no Group V entry for it — the same shape as Group IV's 8683,
    which exists only at /0. The generator says so itself: its summary line for --group V
    reads `codes_absent_from_icdo32: ["9514"]`, meaning absent AT A DECLARED BEHAVIOUR.

    It remains legitimate as an ALIAS INPUT and in any prose explaining the exclusion —
    and it must be there, because REDCap's `v_morph` still offers "9514 - Retinoblastoma,
    spontaneously regressed" as a selectable option (contract §1.1, docs/
    group_05_layer1_repair.md). A clerk who arrives with those words has to land
    somewhere that explains itself, which is the `behaviour_exclusion` terminal, not a
    dead end. So the ban binds the three EMITTING fields and never the text, exactly as
    Group 4's rule 3 does for 8683.
    """
    if ctx.group != GROUP5:
        return []
    return _scan_banned_code(
        ctx, repo, GROUP5_ABSENT_CODE,
        scan_nos_fallback=True, scan_alias_targets=True,
        rule="GROUP 5 RULE 4", cite="contract §0.2, §2.2, §8 rule 4",
        what="ICD-O-3.2 carries 9514 only at /1 (Retinoblastoma, spontaneously "
             "regressed); ICCC-3 Group V admits behaviour 3 only, so there is no "
             "Group V entry for it")


def check_group5_imaging_sufficient(ctx: DTContext):
    """
    GROUP 5 RULE 5 (contract §2.5, §8 rule 5) — `imaging_sufficient` is true on 9510 and
    on nothing else in this group.

    9513 is the reason this rule exists, and it is a within-group inconsistency rather
    than an oversight. Diffuse infiltrating retinoblastoma grows as a flat placoid
    infiltrate WITHOUT a discrete calcified mass, is rare (1-2%), and presents later,
    around age 6. The Track-1 constellation — intraocular mass, calcification within it,
    child under five — would therefore FALSELY EXCLUDE the one retinoblastoma variant
    that most needs tissue. Marking 9513 imaging-sufficient would assert the opposite of
    what the disease does. 9511 and 9512 are differentiation grades, readable on an
    enucleation specimen and nowhere else.
    """
    if ctx.group != GROUP5:
        return []
    out = []
    for entry in ctx.entries:
        if not isinstance(entry, dict):
            continue
        code = as_code(entry.get("morphology_code"))
        if code is None:
            continue
        flag = entry.get("imaging_sufficient")
        if code == GROUP5_IMAGING_SUFFICIENT_CODE:
            if flag is not True:
                out.append((FAIL, "RULE 5 — entry %s has imaging_sufficient %r. 9510 is "
                                  "the imaging route's only output and Visser 2023 Table "
                                  "3 licenses it by name; false here would leave the "
                                  "group's modal pathway with no reachable code "
                                  "(contract §2.5, §8 rule 5)" % (code, flag)))
        elif flag is True:
            out.append((FAIL, "RULE 5 — entry %s has imaging_sufficient true. Only 9510 "
                              "may. 9511 and 9512 are differentiation grades and 9513 is "
                              "a growth pattern, all readable only on an enucleation "
                              "specimen — and 9513 in particular has NO calcified mass "
                              "and presents later, so the imaging constellation would "
                              "falsely exclude it (contract §2.5, §8 rule 5)" % code))
    if not out:
        out.append((OK, "RULE 5 — imaging_sufficient is true on 9510 only"))
    return out


def check_group5_no_ihc(ctx: DTContext):
    """
    GROUP 5 RULE 6 (contract §0.5, §8 rule 6) — Group V has no immunohistochemistry
    anywhere: no `ihc_checklist` node, and `ihc_markers_required` /
    `ihc_markers_exclude` null on every entry.

    The Group 5 pathway document asked, at its §7.2, whether the validator and the engine
    tolerate a group with ZERO Stage-3 nodes — the centrepiece node type of the standard
    pipeline simply does not exist for this disease. They do. This check exists so that
    the absence is recorded as a decision rather than read by the next author as an
    unfinished tree: retinoblastoma is diagnosed clinically and by imaging, and subtyped
    on morphology, never by an antibody panel.
    """
    if ctx.group != GROUP5:
        return []
    out = []
    for node_id, node in sorted(ctx.nodes.items()):
        if node.get("node_type") == "ihc_checklist":
            out.append((FAIL, "RULE 6 — node %s is an ihc_checklist. Group V has no "
                              "immunohistochemistry: diagnosis is clinical and by "
                              "imaging, subtyping is morphological (contract §0.5, §8 "
                              "rule 6)" % node_id))
    for entry in ctx.entries:
        if not isinstance(entry, dict):
            continue
        code = as_code(entry.get("morphology_code")) or "(unnamed)"
        for key in ("ihc_markers_required", "ihc_markers_exclude"):
            if entry.get(key) is not None:
                out.append((FAIL, "RULE 6 — entry %s has %s %r; it must be null. No "
                                  "antibody marks a retinoblastoma into or out of this "
                                  "group (contract §0.5, §8 rule 6)"
                            % (code, key, entry.get(key))))
    if not out:
        out.append((OK, "RULE 6 — no ihc_checklist node; ihc_markers_required and "
                        "ihc_markers_exclude null on all %d entries" % len(ctx.entries)))
    return out


def check_group5_code_neutral_molecular(ctx: DTContext):
    """
    GROUP 5 RULE 7 (contract §0.5, §8 rule 7) — `code_neutral_molecular` is true on every
    Group V entry.

    Unlike every other group built so far, NO molecular finding moves a retinoblastoma
    off its code. RB1 germline status, MYCN amplification and chromosome 6p gain drive
    counselling, prognosis and family screening, and change nothing a coder writes down;
    hereditary and sporadic retinoblastoma both code 9510/3. Where a Group I t(9;22)
    buys 9812, a Group V RB1 result buys a genetics referral.

    The flag is what stops a later author authoring a cytogenetics dropdown whose options
    map to different codes, because in this disease there are none to map to.
    """
    if ctx.group != GROUP5:
        return []
    out = []
    for entry in ctx.entries:
        if not isinstance(entry, dict):
            continue
        code = as_code(entry.get("morphology_code")) or "(unnamed)"
        if entry.get("code_neutral_molecular") is not True:
            out.append((FAIL, "RULE 7 — entry %s has code_neutral_molecular %r; it must "
                              "be true. RB1, MYCN and chromosome 6p are captured and "
                              "change no code in this group (contract §0.5, §8 rule 7)"
                        % (code, entry.get("code_neutral_molecular"))))
    if not out:
        out.append((OK, "RULE 7 — code_neutral_molecular true on all %d entries"
                    % len(ctx.entries)))
    return out


def check_visser_table4_gate(ctx: DTContext):
    """
    RULE 6 (contract §4.2, §8 rule 6) — the Visser Table 4 gate, BOUND TO
    `basis_of_diagnosis`, not to `no_tissue`.

    Revised after a finished tree exposed the original binding's blind spot: a
    branch emitted `8680 Paraganglioma, NOS` off a referral-letter-only finding at
    `basis_of_diagnosis: 1`, and another emitted `9522` off an inadequate specimen
    at basis 2 — neither carrying `no_tissue: true`, because that flag reads as an
    imaging-pathway concept and the author reasonably never reached for it on a
    referral-letter or an inadequate-specimen branch. Bound to `no_tissue`, the
    check never saw either.

    Visser O, et al. Front Oncol 2023;13:1250549, rule 5 (p. 03): basis 1 or 2 means
    morphology `8000/3`, except for the entities named in the paper's Table 3.
    **ICCC-3 Group IV has no Table 3 entries** — Table 3 is Visser's list of
    entities with their OWN named exception to rule 5, and none of Group IV's
    eighteen codes is on it. So for this group, and only this group, basis 1 or 2
    always means 8000/3, which is not a Group IV code and routes to Group XII
    (the 8000-8005 dual-group rule). The one no-pathology route Group IV does have
    is Table 4 (p. 06) at basis 4, for exactly two codes — neuroblastoma (9500) and
    phaeochromocytoma (8700) — and rule 6 (p. 05) says basis 4 never stands alone:
    the marker must accompany a clinical diagnosis or investigation, recorded in
    `biochemical_questions[]` on the reaching `imaging_pathway`.

    Two independent bindings, both keyed off `basis_of_diagnosis` wherever it
    appears, at ANY node type — not only `imaging_pathway` — because the defect
    that forced this rewrite happened on ordinary clinical/histology branches:

        1. basis_of_diagnosis 1 or 2 on a branch that emits a morphology_code is a
           build error outright; the same branch, emitting no code, must carry
           `refer_group: 12`.
        2. basis_of_diagnosis 4 on a branch that emits a morphology_code: the code
           must be 9500 or 8700, and the reaching imaging_pathway's own
           biochemical_questions[] must be non-empty.

    SCOPED TO GROUP IV ONLY, and the reason is Table 3 COVERAGE, not a Group IV
    peculiarity: Visser's Table 3 carries forty-three CNS rows, so Group III
    legitimately emits its own group NOS code at basis 2 for an inadequate
    specimen (an entity Table 3 explicitly covers), and Groups 1-2 have their own
    Table rows besides. Running this rule over them would FAIL correct data; it is
    Group IV specifically that has nothing in Table 3, which is what makes basis
    1/2 unconditional here.

    Only holders that are themselves a real destination are examined — a bare
    `basis_of_diagnosis` on a branch that only continues via `next_node` is
    ordinary cumulative evidence (app.js's assertBasis() reads every branch on the
    path, and the panel reports the highest), not the terminal claim this rule is
    about, so it is not a false-FAIL target.

    This is DISTINCT from, and does not replace, check_imaging_terminals()'s rule
    11: `no_tissue`, `endpoint_verification` and non-empty `diversion_criteria[]`
    on an imaging-only terminal are still required exactly as before. That check
    asks "does this imaging endpoint say it took no tissue"; this one asks "does
    the EVIDENCE TIER actually justify the code", which is the question the 8680/
    9522 defect showed the first framing could not catch.
    """
    if ctx.group != GROUP4:
        return []
    out, seen = [], 0
    for node_id, node in sorted(ctx.nodes.items()):
        candidates = [(node, "(node level)")] + list(_branch_containers(node))
        for holder, where in candidates:
            if "basis_of_diagnosis" not in holder:
                continue
            basis = holder.get("basis_of_diagnosis")
            if isinstance(basis, bool) or not isinstance(basis, int) or basis not in (1, 2, 4):
                continue  # not one of the three bases this rule is about; shape and
                          # ENCR-membership are check_basis_of_diagnosis()'s job
            code = as_code(holder.get("morphology_code"))
            is_terminal = (code is not None or "refer_group" in holder
                           or is_non_reportable(holder) or "behaviour_exclusion" in holder)
            if not is_terminal:
                continue
            seen += 1
            loc = "node %s (%s)" % (node_id, where)

            if basis in (1, 2):
                if code is not None:
                    out.append((FAIL, "%s: RULE 6 — basis_of_diagnosis %d emits "
                                      "morphology_code %s. Visser rule 5, p. 03: "
                                      "basis 1 or 2 means 8000/3 except for Table "
                                      "3 entities, and ICCC-3 Group IV has NO "
                                      "Table 3 entries — so no Group IV code may "
                                      "be emitted at this basis at all (contract "
                                      "§4.2, §8 rule 6)" % (loc, basis, code)))
                else:
                    refer = holder.get("refer_group")
                    if refer is None:
                        refer = node.get("refer_group")
                    if str(refer) != "12":
                        out.append((FAIL, "%s: RULE 6 — basis_of_diagnosis %d "
                                          "emits no morphology_code and must "
                                          "instead carry refer_group: 12 (the "
                                          "8000-8005 dual-group rule to Group "
                                          "XII), got %r. Visser rule 5, p. 03: "
                                          "with no Table 3 entry to except it, "
                                          "everything at this basis is 8000/3, "
                                          "which is not a Group IV code (contract "
                                          "§4.2, §8 rule 6)" % (loc, basis, refer)))
            elif basis == 4 and code is not None:
                if code not in GROUP4_VISSER_TABLE4_CODES:
                    out.append((FAIL, "%s: RULE 6 — basis_of_diagnosis 4 emits %s, "
                                      "which is neither 9500 nor 8700. Visser "
                                      "Table 4 (p. 06) names exactly these two "
                                      "entities a marker constellation alone may "
                                      "establish (contract §4.2, §8 rule 6)"
                                % (loc, code)))
                else:
                    bq = holder.get("biochemical_questions")
                    if bq is None:
                        bq = node.get("biochemical_questions")
                    if not isinstance(bq, list) or not bq:
                        out.append((FAIL, "%s: RULE 6 — biochemical_questions[] "
                                          "is missing or empty on the reaching "
                                          "imaging_pathway for a basis-4 %s "
                                          "terminal. Visser rule 6, p. 05: basis "
                                          "4 never stands alone — the marker "
                                          "must accompany a clinical diagnosis "
                                          "or investigation, and this is the "
                                          "field that records it (contract "
                                          "§4.2, §8 rule 6)" % (loc, code)))
    if not seen and not out:
        return []
    if [f for f in out if f[0] == FAIL]:
        return out
    out.append((OK, "%d basis-1/2/4 terminal(s): none emits a Group IV code at "
                    "basis 1 or 2 (Visser rule 5 — Group IV has no Table 3 "
                    "entries), and every basis-4 emission is 9500 or 8700 with a "
                    "non-empty biochemical_questions[] (rule 6)" % seen))
    return out


# --------------------------------------------------------------------------------------
# Group 6 build contract §8 — Renal Tumours. Nine validation rules. decision_trees[]
# is empty while this group's tree is authored concurrently on this branch, so every
# check below that looks at NODES (not morphology_entries[]) finds nothing at first —
# and returns [] rather than an OK line, the check_imaging_pathway_shape() discipline
# (data.md §5A): a check that reports OK on zero matches is a check that would also
# report OK on a typo'd node type or an empty file, and nobody could tell the
# difference from the build log.
# --------------------------------------------------------------------------------------

# §4.3 — the marker tokens the INI1 fork keys off. Left-boundary only: a captured
# value is as likely to be written "TFE3_rearranged" or "SDH-deficient" as "TFE3"
# alone, and a trailing \b would miss the first of those (an underscore is a \w
# character, so "TFE3_rearranged" has no word boundary between "3" and "_"). The
# left boundary alone still blocks a mid-word false hit ("walk", "chalk" do not
# match \bALK because the character immediately before "alk" is a letter).
_INI1_TOKEN_RE = re.compile(r"(?<![A-Za-z0-9])(SMARCB1|INI1)", re.IGNORECASE)

# §0.5, §4.5 — the seven molecularly defined renal cell carcinoma entities (Moch
# 2022 Table 1, Cajaiba 2018), same left-boundary-only discipline as above.
_MOLECULAR_ENTITY_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9])(TFE3|TFEB|ELOC|TCEB1|HLRCC|ALK"
    r"|fumarate[ _-]?hydratase|succinate[ _-]?dehydrogenase|SDH)",
    re.IGNORECASE)

# §4.4 — anaplasia / SIOP-risk vocabulary, deliberately narrower than the SIOP list's
# own words. See check_group6_anaplasia_code_neutral()'s docstring for why
# "epithelial", "stromal" and "mixed" are excluded on purpose.
_ANAPLASIA_TOKEN_RE = re.compile(
    r"anaplas|nuclear unrest|nuclear enlargement|blastemal|completely necrotic"
    r"|siop risk",
    re.IGNORECASE)


def _holder_text(holder):
    """Every string leaf anywhere inside a branch holder (recursing into nested dicts
    and lists), for a token search that must not depend on which specific field an
    author put a finding in — `when`, `label`, `hint`, a nested `equals`, all read
    the same way. Used by the Group 6 marker/entity/anaplasia scans, none of which
    can assume a fixed field name for a captured finding before the tree exists."""
    texts: list = []

    def collect(value):
        if isinstance(value, str):
            texts.append(value)
        elif isinstance(value, list):
            for v in value:
                collect(v)
        elif isinstance(value, dict):
            for v in value.values():
                collect(v)

    collect(holder)
    return texts


# A molecular marker named as ABSENT is not a molecular finding. Group 6 rule 5 scans
# prose for entity tokens, and prose says "TFE3" both when the rearrangement was found
# and when it was looked for and was not. Without this, the check FAILS on the one case
# 8312/3 exists for -- a carcinoma still unclassified after a complete NEGATIVE workup --
# which is a false FAIL on correct data, and a false FAIL is the more corrosive kind: it
# teaches the next author to restructure correct data to appease the validator.
#
# Found 22 Sep 2026 by probing the check with a legitimate branch rather than a broken
# one. Negation cues are matched within a window ending at the marker, so "no TFE3
# rearrangement" is negated and "TFE3 rearranged, therefore not 8312" is not.
_NEGATION_CUE_RE = re.compile(
    r"(?:\bnot\b|\bno\b|\bnone\b|\bnegative\b|\bnegatives?\b|\babsent\b|"
    r"\bexcluded?\b|\bexclusion\b|\bwild[- ]?type\b|\bretained\b|\bintact\b|"
    r"\bnormal\b|\bunremarkable\b|\bwithout\b|\bfails? to\b|\bnever\b|"
    r"\bnot demonstrated\b|\bundetected\b)",
    re.I)
_NEGATION_WINDOW = 90


def _marker_asserted(text, marker_re):
    """True when `marker_re` matches `text` at least once WITHOUT a negation cue in the
    90 characters before it. The window is clause-sized on purpose: it catches "no TFE3
    rearrangement demonstrated" and "TFE3, TFEB and ALK were all negative" (the cue
    follows, so a trailing-cue check runs too), while a marker asserted in one clause is
    not silenced by a negation belonging to another sentence."""
    for m in marker_re.finditer(text or ""):
        before = text[max(0, m.start() - _NEGATION_WINDOW):m.start()]
        after = text[m.end():m.end() + _NEGATION_WINDOW]
        if _NEGATION_CUE_RE.search(before) or _NEGATION_CUE_RE.search(after):
            continue
        return True
    return False


def check_group6_code_set(ctx: DTContext):
    """
    GROUP 6 RULE 1 (contract §0.3, §8 rule 1) — the fabricated-code guard, in both
    places a fabricated code can enter this file: a `morphology_entries[]` object
    whose (code, behaviour) is not one of the 90 generated records, and a decision-
    tree node that EMITS one.

    GROUP6_CODES / GROUP6_BEHAVIOUR_DECLARED were produced by
    build/generate_group_inventory.py --group VI joining ICCC-2017.sqlite to
    icdo32.sqlite (contract §0.3) — re-run on 22 September 2026 and diffed against
    this file's own 90 morphology_entries[]: identical sets. Every ICCC-2017.sqlite
    range for main_group='VI' declares behaviour 3 and nothing else, checked
    directly the same day (GROUP6_BEHAVIOUR_DECLARED's own comment has the query).
    Neither constant is read back off the file under test, so the anchor cannot be
    satisfied by whatever the file happens to already contain — the one thing a
    fabricated-code guard must not do.

    Tree side, this is Group 5 rule 3(a)'s own shape: `ctx.emissions()`, which walks
    every node's options[], resolution_logic[], bands[] and branches, so an author
    typing 8319 as 8139 fails here rather than passing every other check that exists
    once a real-looking (code, behaviour) is on screen. Empty while decision_trees[]
    is empty — silently, per this section's own header note.
    """
    if ctx.group != GROUP6:
        return []
    out = []
    seen_entries = 0
    for i, entry in enumerate(ctx.entries):
        if not isinstance(entry, dict):
            continue
        code = as_code(entry.get("morphology_code"))
        if code is None:
            continue
        seen_entries += 1
        beh = entry.get("behavior_code")
        beh_s = None if beh is None else str(beh).strip()
        if code not in GROUP6_CODES or beh_s not in GROUP6_BEHAVIOUR_DECLARED:
            out.append((FAIL, "RULE 1 — morphology_entries[%d] carries %s/%s, which "
                              "is not one of the 90 (code, behaviour) records "
                              "build/generate_group_inventory.py --group VI "
                              "generates from ICCC-2017.sqlite and icdo32.sqlite. "
                              "Re-run the generator and confirm the pair before "
                              "authoring it (contract §0.3, §8 rule 1)"
                        % (i, code, beh_s)))
    if not out:
        out.append((OK, "RULE 1 — all %d morphology_entries[] pairs are in the "
                        "generated 90-record Group VI inventory" % seen_entries))

    seen_emissions = 0
    emission_out = []
    for code, holder, node_id, where in ctx.emissions():
        seen_emissions += 1
        if code not in GROUP6_CODES:
            emission_out.append((FAIL, "RULE 1 — node %s (%s) emits %s, which is not "
                                       "a Group VI code. The generated inventory is "
                                       "exactly the 90 codes in GROUP6_CODES "
                                       "(contract §0.3, §8 rule 1)"
                                 % (node_id, where, code)))
    if seen_emissions and not emission_out:
        emission_out.append((OK, "RULE 1 — all %d tree emission(s) are in the "
                                 "generated Group VI inventory" % seen_emissions))
    out.extend(emission_out)
    return out


def check_group6_absent_codes(ctx: DTContext):
    """
    GROUP 6 RULE 2 (contract §2A, §8 rule 2) — none of the eleven REDCap options the
    tool cannot emit appears as a `morphology_code` anywhere in group_06_dt.json.

    Ten are behaviour exclusions — real ICD-O-3.2 codes that exist only at /0 or /1,
    never at Group VI's declared /3 (8966, 8967, 8325, 8361, 9013, 8040, 8053, 8060,
    8191, 8561) — and one is a retired number, the first this project has met in a
    live REDCap option list: 8965 Nephrogenic adenofibroma, DELETED in ICD-O-3.2 and
    moved to 9013/0, zero rows for 8965 in icdo32.sqlite. All eleven verified
    directly against icdo32.sqlite on 22 September 2026 (contract §2A).

    Scoped narrower than check_group4_absent_codes() / check_group5_absent_codes():
    the contract's own wording for this rule binds one field, `morphology_code`,
    inside this one file — unlike 8683 (Group 4) and 9514 (Group 5), the contract
    does not extend the ban to `nos_fallback_code` or an alias target for these
    eleven, so this check does not either. The same code turning up in `coding_note`
    explaining why it was excluded is expected, and a clerk-facing mention in
    `reason`/`hint` naming what was ruled out is exactly how a behaviour_exclusion
    explains itself — both stay WARN, never FAIL, matching how GROUP3/4/5's own
    absent-code checks treat prose.
    """
    if ctx.group != GROUP6:
        return []
    out = []
    for holder, path in walk_dicts(ctx.data):
        for key, value in holder.items():
            if key in ALIAS_INPUT_KEYS:
                continue
            loc = "%s.%s" % (path, key) if path else key
            if key == "morphology_code":
                cs = as_code(value)
                if cs and cs in GROUP6_ABSENT_CODES:
                    out.append((FAIL, "RULE 2 — %s carries code %s, one of the "
                                      "eleven §2A options this group cannot emit. "
                                      "Verified against icdo32.sqlite: it has no /3 "
                                      "term (or, for 8965, no term at all) (contract "
                                      "§2A, §8 rule 2)" % (loc, cs)))
                continue
            if not isinstance(value, str):
                continue
            for code in GROUP6_ABSENT_CODES:
                if not _code_token_re(code).search(value):
                    continue
                if key in AUTHOR_FACING_TEXT_KEYS:
                    out.append((WARN, "RULE 2 — %s mentions %s, one of the eleven "
                                      "§2A codes this group cannot emit. Author-"
                                      "facing and never displayed — fine, and "
                                      "expected when explaining the exclusion"
                                % (loc, code)))
                elif key in CLERK_FACING_TEXT_KEYS:
                    out.append((WARN, "RULE 2 — %s prints %s, one of the eleven §2A "
                                      "codes, in clerk-facing text. Contract §2A "
                                      "bans the code only as a morphology_code; "
                                      "naming it in a reason/hint that explains an "
                                      "exclusion is expected" % (loc, code)))
                break

    if [f for f in out if f[0] == FAIL]:
        return out
    out.append((OK, "RULE 2 — none of the eleven §2A codes (%s) appears as a "
                    "morphology_code anywhere in %s"
                % (", ".join(GROUP6_ABSENT_CODES), ctx.name)))
    return out


def check_group6_behaviour_declaration(ctx: DTContext, layer1: Path):
    """
    GROUP 6 RULE 3 (contract §0.2, §8 rule 3) — every `behaviour_exclusion` block in
    this file names `group_declares: "3"`, and its `icdo_code`/`icdo_behaviour` pair
    is a real (code, behaviour) in icdo32.sqlite.

    check_behaviour_exclusion() (generalised, keyed off BEHAVIOUR_DECLARED_BY_GROUP)
    already proves icdo_behaviour is NOT a member of the group's declared set, and
    that icdo_code/icdo_behaviour/icdo_term round-trip to the PREFERRED ICD-O-3.2
    term. Neither of those tests reads the `group_declares` STRING itself — it is
    checked only for presence and non-emptiness, one of six required keys. An author
    who pastes a sibling group's block keeps a well-formed, round-tripping exclusion
    whose group_declares still reads "0-1,3" or "1" — Group III's or Group V's own
    words — and every existing check passes it, because none of them compares that
    field's VALUE against anything. This closes that gap for Group VI specifically:
    group_declares must be the literal string "3", Group VI's own declaration
    (GROUP6_BEHAVIOUR_DECLARED, verified directly against ICCC-2017.sqlite on 22
    September 2026 — every main_group='VI' range declares behaviour 3 and nothing
    else).

    The icdo_code/icdo_behaviour re-check queries load_icdo32() itself rather than
    trusting that check_behaviour_exclusion() already ran and passed — so a defect
    here does not silently depend on read order, and this check stays meaningful
    even in a build where Task B's BEHAVIOUR_DECLARED_BY_GROUP row was somehow
    reverted and the general check stopped looking at Group VI at all.
    """
    if ctx.group != GROUP6:
        return []
    out = []
    seen = 0
    index = None
    err = None

    for node_id, node in sorted(ctx.nodes.items()):
        for holder, where in walk_dicts(node):
            be = holder.get("behaviour_exclusion")
            if not isinstance(be, dict):
                continue
            if index is None and err is None:
                index, err = load_icdo32(layer1)
            seen += 1
            loc = "node %s (%s) behaviour_exclusion" % (node_id, where)

            gd = be.get("group_declares")
            if gd != "3":
                out.append((FAIL, "%s: group_declares is %r; Group VI's own "
                                  "declaration is the single behaviour \"3\" "
                                  "(verified directly against ICCC-2017.sqlite — "
                                  "contract §0.2, §8 rule 3). A block naming any "
                                  "other value is either copied from a sibling "
                                  "group or wrong about this one" % (loc, gd)))

            code = as_code(be.get("icdo_code"))
            beh = be.get("icdo_behaviour")
            beh_s = None if beh is None else str(beh).strip()
            if index:
                terms = index.get((code, beh_s)) if code and beh_s is not None else None
                if not terms:
                    out.append((FAIL, "%s: icdo_code/icdo_behaviour %s/%s is not a "
                                      "real pair in icdo32.sqlite (contract §8 "
                                      "rule 3)" % (loc, code, beh_s)))
            elif err:
                out.append((WARN, "%s: could not verify icdo_code/icdo_behaviour "
                                  "against icdo32.sqlite: %s. group_declares was "
                                  "still checked" % (loc, err)))

    if not seen:
        return []
    if [f for f in out if f[0] == FAIL]:
        return out
    out.append((OK, "RULE 3 — %d behaviour_exclusion block(s) all declare "
                    "group_declares \"3\" and round-trip icdo_code/icdo_behaviour "
                    "to icdo32.sqlite" % seen))
    return out


def check_group6_ini1_fork(ctx: DTContext):
    """
    GROUP 6 RULE 4 (contract §4.3, §8 rule 4) — THE GROUP'S SIGNATURE CHECK.

    Loss of nuclear SMARCB1 (INI1) is the defining immunohistochemical finding for
    BOTH `8963/3 Rhabdoid tumor, NOS` and `8510/3 Medullary carcinoma, NOS`. A
    resolution_logic rule that auto-resolves the marker to one of those two codes
    without also gating on age codes an adolescent's renal medullary carcinoma as an
    infant's rhabdoid tumour, or the reverse. Contract §4.3 gives the fork as three
    ordered rules, conditioned rules first:

        1. when age_band >=10, sickle_cell trait/disease, SMARCB1 lost  -> 8510/3
        2. when age_band <2 or 2-4,                       SMARCB1 lost  -> 8963/3
        3.                                                 SMARCB1 lost  -> no code; registrar

    FAILs any rule that names SMARCB1 or INI1 in `positive` or `negative` (the field
    app.js's markerOff() reads as "must be negative" — ihc_markers_exclude on both
    the 8510 and 8963 entries carries "SMARCB1 (INI1)", so loss appears here as a
    `negative` token, per the contract's own field mapping) and resolves to 8963 or
    8510 without a `when` on `age_band`, and — for 8510 specifically — without
    `sickle_cell_status` too (rule 1's own second condition; age alone is not the
    fork the contract writes).

    KEYED OFF THE MARKER TOKENS AND THE DESTINATION, never off a flag in the file.
    No field is trusted to mean "this rule has already been age-gated" — a flag
    authored to carry that meaning is exactly the failure mode this project has been
    bitten by before (`redcap_option_verified`'s history, and the router's own
    `topography_equals` dead branches found on this same build): a hurried author
    sets it, the fork silently stops working, and nothing downstream notices. The
    rule's own `when` object is the only thing read, and only for the two keys the
    contract actually names.
    """
    if ctx.group != GROUP6:
        return []
    out = []
    seen = 0
    for node_id, node in sorted(ctx.nodes.items()):
        rules = node.get("resolution_logic")
        if not isinstance(rules, list):
            continue
        for i, rule in enumerate(rules):
            if not isinstance(rule, dict):
                continue
            tokens = []
            for field in ("positive", "negative"):
                vals = rule.get(field)
                if isinstance(vals, list):
                    tokens.extend(v for v in vals if isinstance(v, str))
            if not any(_INI1_TOKEN_RE.search(t) for t in tokens):
                continue
            code = as_code(rule.get("morphology_code")) or as_code(rule.get("code"))
            if code not in ("8963", "8510"):
                continue
            seen += 1
            loc = "node %s resolution_logic[%d]" % (node_id, i)
            when = rule.get("when")
            when = when if isinstance(when, dict) else {}
            age = when.get("age_band")
            has_age = "age_band" in when and age not in (None, [], "")
            if not has_age:
                out.append((FAIL, "%s resolves SMARCB1/INI1 loss to %s/3 with no "
                                  "`when` on age_band. This single IHC finding is "
                                  "the defining result for BOTH 8963/3 Rhabdoid "
                                  "tumor, NOS and 8510/3 Medullary carcinoma, NOS — "
                                  "without an age gate this auto-resolves an "
                                  "adolescent's renal medullary carcinoma to an "
                                  "infant's rhabdoid tumour, or the reverse "
                                  "(contract §4.3, §8 rule 4 — the group's signature "
                                  "check)" % (loc, code)))
                continue
            if code == "8510":
                sickle = when.get("sickle_cell_status")
                has_sickle = ("sickle_cell_status" in when
                              and sickle not in (None, [], ""))
                if not has_sickle:
                    out.append((FAIL, "%s resolves SMARCB1/INI1 loss to 8510/3 with "
                                      "a `when` on age_band but none on "
                                      "sickle_cell_status. Contract §4.3 rule 1 "
                                      "gates 8510/3 on age >=10 AND "
                                      "sickle_cell_status in {trait, disease} — age "
                                      "alone is not the fork the contract writes "
                                      "(§8 rule 4)" % loc))
    if not seen:
        return []
    if [f for f in out if f[0] == FAIL]:
        return out
    out.append((OK, "RULE 4 — %d SMARCB1/INI1 resolution rule(s) resolving to 8963 "
                    "or 8510 all carry the required age_band (and, for 8510, "
                    "sickle_cell_status) `when`" % seen))
    return out


def check_group6_molecular_rcc_code(ctx: DTContext):
    """
    GROUP 6 RULE 5 (contract §0.5, §4.5, §8 rule 5) — the two-directional guard on
    the renal-carcinoma molecular layer.

    `8311/3` is ICD-O-3.2's molecularly DEFINED renal cell carcinoma code — TFE3-
    rearranged, TFEB-altered, ELOC-mutated, FH-deficient, HLRCC-associated, SDH-
    deficient and ALK-rearranged all sit on it (Moch 2022 Table 1). Six entries in
    this file carry `code_neutral_molecular: false` because a molecular result moves
    a case OFF each of them, onto 8311: `8260`, `8310`, `8312`, `8316`, `8319` (the
    "vacated" five) and `8311` itself, whose own false flag means the opposite thing
    — a molecular finding is what PUTS a case on this code, not what moves it off.

    BOTH DIRECTIONS FAIL, because both are the same defect wearing different faces
    (contract §0.5, project preamble): emitting 8312 (or one of its four siblings)
    for a tumour the branch names as molecularly defined understates the registry's
    own code set — 8311/3 carries 47.2% of paediatric RCC (Cajaiba 2018), so this is
    not a corner case — and emitting 8311 on a suspicion the file never states
    overstates it. Each FAIL below cites which.

    A branch is examined when it emits 8311 or one of the five vacated codes AND
    (for the vacated five) itself names one of the seven molecular entities, or (for
    8311) does not. The token search (_holder_text / _MOLECULAR_ENTITY_TOKEN_RE)
    walks every string anywhere inside the SAME branch holder that carries the
    morphology_code — the destination and the finding that justifies it are read off
    one object, not stitched together across the node — so a molecular hint on a
    DIFFERENT sibling branch of the same node cannot manufacture a false pass or a
    false FAIL here.
    """
    if ctx.group != GROUP6:
        return []
    out = []
    seen = 0
    for node_id, node in sorted(ctx.nodes.items()):
        for holder, where in [(node, "(node level)")] + list(_branch_containers(node)):
            code = as_code(holder.get("morphology_code"))
            if code != GROUP6_MOLECULAR_DEFINED_CODE and code not in GROUP6_MOLECULAR_VACATED_CODES:
                continue
            texts = _holder_text(holder)
            # Two different questions, and they are not each other's negation.
            # `mentions_marker` answers "is a molecular entity discussed here at all",
            # which is what an 8311 branch must do. `asserts_marker` answers "is one
            # recorded as FOUND", which is what makes 8312 and its four siblings wrong.
            # A complete NEGATIVE workup mentions every marker and asserts none, and is
            # exactly the case 8312/3 exists for.
            mentions_marker = any(_MOLECULAR_ENTITY_TOKEN_RE.search(t) for t in texts)
            asserts_marker = any(_marker_asserted(t, _MOLECULAR_ENTITY_TOKEN_RE)
                                 for t in texts)
            seen += 1
            loc = "node %s (%s)" % (node_id, where)
            if code == GROUP6_MOLECULAR_DEFINED_CODE and not asserts_marker:
                out.append((FAIL, "%s emits 8311/3 with no molecular finding "
                                  "recorded — none of TFE3, TFEB, ELOC, HLRCC, "
                                  "fumarate hydratase, succinate dehydrogenase/SDH "
                                  "or ALK is ASSERTED on this branch (a marker named "
                                  "only as absent, negative, excluded, retained or "
                                  "wild-type does not count). 8311/3 is "
                                  "molecularly DEFINED (contract §0.5): emitting it "
                                  "on a suspicion the file does not state overstates "
                                  "this case's evidence" % loc))
            elif code in GROUP6_MOLECULAR_VACATED_CODES and asserts_marker:
                out.append((FAIL, "%s emits %s/3 while naming a molecularly defined "
                                  "entity on the same branch. Contract §0.5: a "
                                  "molecular result moves the case OFF %s to "
                                  "8311/3 — emitting %s here understates the case, "
                                  "the mirror defect, and 8311/3 alone carries "
                                  "47.2%% of paediatric RCC (Cajaiba 2018), so this "
                                  "is not a corner case. If the workup was done and was "
                                  "NEGATIVE, say so on the branch — 'not demonstrated', "
                                  "'negative', 'excluded', 'wild-type', 'retained' — and "
                                  "this check reads it as the absence it is"
                            % (loc, code, code, code)))
    if not seen:
        return []
    if [f for f in out if f[0] == FAIL]:
        return out
    out.append((OK, "RULE 5 — %d molecular-RCC branch(es) on 8311 or {%s} correctly "
                    "record a molecular finding exactly where the code requires one"
                % (seen, ", ".join(sorted(GROUP6_MOLECULAR_VACATED_CODES)))))
    return out


def check_group6_8963_topography(ctx: DTContext):
    """
    GROUP 6 RULE 6 (contract §3.1, §8 rule 6) — every branch that emits 8963/3
    requires C64.9 in its own `when`.

    8963 is Group VI's only dual-group code (contract §3.1): the shared router's
    `dual_group_rules["8963"]` sends C64.9 to this group, CNS sites to Group III via
    9508, and everything else to Group IX IXd3. That gate protects a case that
    arrives THROUGH the router. It does nothing for a clerk who reaches this
    group's own tree directly — several VIb carcinomas are already documented as
    "reachable... only by direct code entry" (contract §0.3), and nothing in the
    engine stops 8963 being reached the same way — so the tree's own rhabdoid
    terminal has to carry its own topography gate rather than depend on the router
    having already run.

    FAILs a branch that emits 8963 with no `when`, or a `when` whose values never
    include C64.9 — the same defect CLASS as the dead router branch this build found
    and fixed (§3.1's own account: `topography_equals`, a key app.js's
    branchMatches() has never read, versus `topography_in`, which it does), but
    guarding the group's own tree instead of the shared router.
    """
    if ctx.group != GROUP6:
        return []
    out = []
    seen = 0
    for node_id, node in sorted(ctx.nodes.items()):
        for holder, where in [(node, "(node level)")] + list(_branch_containers(node)):
            code = as_code(holder.get("morphology_code"))
            if code != "8963":
                continue
            seen += 1
            loc = "node %s (%s)" % (node_id, where)
            when = holder.get("when")
            found = False
            if isinstance(when, dict):
                for v in when.values():
                    vals = v if isinstance(v, list) else [v]
                    if any(str(x) == GROUP6_8963_TOPOGRAPHY for x in vals):
                        found = True
                        break
            if not found:
                out.append((FAIL, "%s emits 8963/3 with no `when` confirming C64.9. "
                                  "8963 at a CNS site is Group III (via 9508) and at "
                                  "soft tissue Group IX (IXd3); the router's own "
                                  "C64.9 branch does not protect a case that reaches "
                                  "this tree directly, so the terminal must gate on "
                                  "topography itself (contract §3.1, §8 rule 6)"
                            % loc))
    if not seen:
        return []
    if [f for f in out if f[0] == FAIL]:
        return out
    out.append((OK, "RULE 6 — all %d branch(es) emitting 8963/3 require C64.9 in "
                    "their own `when`" % seen))
    return out


def check_group6_anaplasia_code_neutral(ctx: DTContext):
    """
    GROUP 6 RULE 7 (contract §4.4, §8 rule 7) — an anaplasia or SIOP-risk annotation
    never carries a morphology_code other than 8960.

    Hill 2003 defines nuclear unrest — nuclear enlargement resembling anaplasia with
    no abnormal multipolar mitotic figures — as favourable histology; Pfister 2022
    gives the WHO three-part true-anaplasia criterion. Both stay 8960/3, and the
    SIOP risk subtypes (Vujanić 2002) are likewise code-neutral (contract §4.4):
    anaplasia is a PROGNOSTIC modifier this tree records, never a fork to a
    different code.

    The token set is deliberately narrower than the SIOP list's own words.
    "Epithelial", "stromal" and "mixed" are three of the eight SIOP risk subtypes by
    name, but they are also, verbatim, three words inside 8959/0's own ICD-O-3.2
    related term "Mixed epithelial and stromal tumor" — scanning for them would
    false-FAIL the benign-cystic-nephroma behaviour_exclusion the moment it quotes
    its own ICD-O-3.2 term (contract §3.2). The check instead keys on vocabulary
    that is actually diagnostic of the anaplasia/SIOP-risk CONTEXT — "anaplas-",
    "nuclear unrest", "nuclear enlargement", "blastemal", "completely necrotic",
    "SIOP risk" — none of which collides with anything else this group's inventory
    names.
    """
    if ctx.group != GROUP6:
        return []
    out = []
    seen = 0
    for node_id, node in sorted(ctx.nodes.items()):
        for holder, where in [(node, "(node level)")] + list(_branch_containers(node)):
            texts = _holder_text(holder)
            if not any(_ANAPLASIA_TOKEN_RE.search(t) for t in texts):
                continue
            code = as_code(holder.get("morphology_code"))
            if code is None:
                continue
            seen += 1
            if code != GROUP6_ANAPLASIA_CODE:
                out.append((FAIL, "node %s (%s) names anaplasia or a SIOP risk "
                                  "subtype and carries morphology_code %s, not "
                                  "8960. Anaplasia and the SIOP risk subtypes are "
                                  "prognostic modifiers this tree records and never "
                                  "a code fork (contract §4.4, §8 rule 7)"
                            % (node_id, where, code)))
    if not seen:
        return []
    if [f for f in out if f[0] == FAIL]:
        return out
    out.append((OK, "RULE 7 — every anaplasia/SIOP-risk holder carries "
                    "morphology_code 8960 (%d checked)" % seen))
    return out


def check_group6_imaging_sufficient(ctx: DTContext):
    """
    GROUP 6 RULE 8 (contract §4.2, §0.11 point 3, §8 rule 8) — imaging_sufficient is
    true on 8960 and on nothing else in this group.

    Visser 2023 Table 3 gives nephroblastoma basis 2 at C64, 8960/3, Group VI — the
    ONLY Group VI row in the table. Every other Group VI code needs tissue: rhabdoid
    tumour and clear cell sarcoma of the kidney are IHC/cytogenetics diagnoses, every
    renal carcinoma needs histology (and, for 8311 versus 8260/8310/8312/8316/8319,
    molecular workup — rule 5), and 8000-8005 is the imaging route's OWN fallback for
    a case that does NOT meet the nephroblastoma constellation — marking any of those
    imaging_sufficient would assert that failing the constellation is itself
    sufficient evidence, which inverts what the field means.
    """
    if ctx.group != GROUP6:
        return []
    out = []
    for entry in ctx.entries:
        if not isinstance(entry, dict):
            continue
        code = as_code(entry.get("morphology_code"))
        if code is None:
            continue
        flag = entry.get("imaging_sufficient")
        if code == GROUP6_IMAGING_SUFFICIENT_CODE:
            if flag is not True:
                out.append((FAIL, "RULE 8 — entry %s has imaging_sufficient %r. "
                                  "8960 is the imaging route's only output and "
                                  "Visser 2023 Table 3 licenses it by name — false "
                                  "here would leave the group's dominant pathway "
                                  "with no reachable code (contract §4.2, §8 "
                                  "rule 8)" % (code, flag)))
        elif flag is True:
            out.append((FAIL, "RULE 8 — entry %s has imaging_sufficient true. Only "
                              "8960 may (contract §0.11 point 3, §4.2, §8 rule 8) — "
                              "every other Group VI code needs histology, IHC, "
                              "cytogenetics or molecular workup" % code))
    if not out:
        out.append((OK, "RULE 8 — imaging_sufficient is true on 8960 only"))
    return out


def check_group6_no_flow_cytometry(ctx: DTContext):
    """
    GROUP 6 RULE 9 (contract §0.9, §8 rule 9) — `Flow cytometry` never appears in a
    Group VI entry's diagnostic_tests_required.

    Contract §0.9: "Flow cytometry is irrelevant to this group. Do not use it."
    Renal tumours are diagnosed by imaging, histology, immunohistochemistry,
    cytogenetics/FISH and molecular/PCR; flow cytometry is a haematolymphoid tool
    (Groups I/II) with no role here, and its presence on a Group VI entry is a
    copy-paste from another group's schema, not a workup this disease uses.
    """
    if ctx.group != GROUP6:
        return []
    out = []
    seen = 0
    for entry in ctx.entries:
        if not isinstance(entry, dict):
            continue
        code = as_code(entry.get("morphology_code")) or "(unnamed)"
        tests = entry.get("diagnostic_tests_required")
        if not isinstance(tests, list):
            continue
        seen += 1
        if "Flow cytometry" in tests:
            out.append((FAIL, "RULE 9 — entry %s lists 'Flow cytometry' in "
                              "diagnostic_tests_required. Contract §0.9: flow "
                              "cytometry is irrelevant to Group VI and must not be "
                              "used (contract §8 rule 9)" % code))
    if not seen:
        return []
    if [f for f in out if f[0] == FAIL]:
        return out
    out.append((OK, "RULE 9 — no entry lists Flow cytometry in "
                    "diagnostic_tests_required (%d entries checked)" % seen))
    return out


# --------------------------------------------------------------------------------------
# B5. Against the source of truth
# --------------------------------------------------------------------------------------

def _g7_asserted(text, rx):
    """True when `rx` matches `text` with no negation cue in the 90 characters BEFORE it.

    Rule 4 reads histology labels, where a negation precedes the term it negates:
    "with no small cell undifferentiated or rhabdoid component". The shared
    _marker_asserted() also looks AFTER each match, which suits molecular prose
    ("TFE3 ... were all negative") but here cancels a term by the negation of the next
    one: "A small cell undifferentiated pattern predominates, with no rhabdoid cells"
    read as not asserting the small cell pattern at all. Found by the correct-data run
    of the negative controls, 3 October 2026, the first time that label existed."""
    for m in rx.finditer(text or ""):
        if not _NEGATION_CUE_RE.search(text[max(0, m.start() - _NEGATION_WINDOW):m.start()]):
            return True
    return False


def _g7_option_text(holder):
    """The clerk-facing words of one branch: the option label, else its reason."""
    for key in ("label", "finding", "descriptor", "site", "reason"):
        value = holder.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return ""


def check_group7_code_set(ctx: DTContext):
    """
    GROUP 7 RULE 1 (contract §0.3, §8 rule 1) — the fabricated-code guard. Every
    morphology_entries[] pair and every code a node emits must be one of the 92
    generated (code, behaviour) records in GROUP7_CODES, which is pasted from the
    generator's output and never read back off the file under test.
    """
    if ctx.group != GROUP7:
        return []
    out = []
    for i, entry in enumerate(ctx.entries):
        if not isinstance(entry, dict):
            continue
        code = as_code(entry.get("morphology_code"))
        beh = str(entry.get("behavior_code") or "").strip()
        if (code, beh) in GROUP7_RULED_PAIRS:
            continue
        if code and (code not in GROUP7_CODES or beh not in GROUP7_BEHAVIOUR_DECLARED):
            out.append((FAIL, "RULE 1 — morphology_entries[%d] carries %s/%s, which is not "
                              "one of the 92 records build/generate_group_inventory.py "
                              "--group VII generates from ICCC-2017.sqlite and "
                              "icdo32.sqlite (contract §0.3)" % (i, code, beh)))
    seen = 0
    for code, holder, node_id, where in ctx.emissions():
        seen += 1
        beh = str(holder.get("behavior_code") or "3").strip()
        if (code, beh) in GROUP7_RULED_PAIRS:
            continue
        if code not in GROUP7_CODES or beh not in GROUP7_BEHAVIOUR_DECLARED:
            out.append((FAIL, "RULE 1 — node %s (%s) emits %s/%s, which is not a Group VII "
                              "(code, behaviour) record (contract §0.3)"
                        % (node_id, where, code, beh)))
    for node_id, node in sorted(ctx.nodes.items()):
        for holder, where in walk_dicts(node):
            if is_nos_fallback_object(holder, where):
                code = as_code(holder.get("code"))
                if code and code not in GROUP7_CODES:
                    out.append((FAIL, "RULE 1 — node %s (%s) falls back to %s, which is not "
                                      "a Group VII code (contract §0.3)"
                                % (node_id, where, code)))
    if not out:
        out.append((OK, "RULE 1 — %d entries and %d tree emissions are all in the generated "
                        "92-record Group VII inventory" % (len(ctx.entries), seen)))
    return out


def check_group7_absent_codes(ctx: DTContext, repo: Path):
    """
    GROUP 7 RULE 2 (contract §2A, §8 rule 2) — none of the six REDCap options the tool
    cannot emit at behaviour 3 (8975, 8148, 8202, 8264, 8561, 9013) appears as a
    morphology_code, a nos_fallback code, an entry's nos_fallback_code, or an alias
    target. A behaviour_exclusion naming one of them at its real behaviour is how the
    tree says so, and prose naming one is expected; neither is a finding.
    """
    if ctx.group != GROUP7:
        return []
    out = []
    banned = set(GROUP7_ABSENT_CODES)
    for holder, path in walk_dicts(ctx.data):
        for key in ("morphology_code", "nos_fallback_code"):
            code = as_code(holder.get(key))
            if code in banned:
                out.append((FAIL, "RULE 2 — %s.%s is %s, a code ICD-O-3.2 has no "
                                  "behaviour-3 term for (contract §2A)" % (path, key, code)))
        if is_nos_fallback_object(holder, path):
            code = as_code(holder.get("code"))
            if code in banned:
                out.append((FAIL, "RULE 2 — %s falls back to %s, a code ICD-O-3.2 has no "
                                  "behaviour-3 term for (contract §2A)" % (path, code)))
    alias_path = repo / "data" / "aliases" / "aliases_group_07.json"
    if alias_path.exists():
        aliases, _ = load_json(alias_path)
        for i, entry in enumerate(aliases if isinstance(aliases, list) else []):
            for code in (entry.get("maps_to_morphology_codes") or []) if isinstance(entry, dict) else []:
                if as_code(code) in banned:
                    out.append((FAIL, "RULE 2 — aliases_group_07.json[%d] %r maps to %s, a "
                                      "code with no behaviour-3 term; it must map to no code "
                                      "(contract §2A, §6)" % (i, entry.get("alias"), code)))
    if not out:
        out.append((OK, "RULE 2 — none of %s is emitted, used as a fallback, or targeted by "
                        "an alias" % ", ".join(GROUP7_ABSENT_CODES)))
    return out


def check_group7_behaviour_declaration(ctx: DTContext, layer1: Path):
    """
    GROUP 7 RULE 3 (contract §0.2, §8 rule 3) — every behaviour_exclusion names
    group_declares "3", Group VII's own declaration; its icdo_code/icdo_behaviour pair
    is real in icdo32.sqlite; and its icdo_code sits on a Group VII stem (the generated
    inventory or the §2A absent codes). A benign lesion on no Group VII stem is a
    non-reportable terminal, not a behaviour exclusion: there is no Group VII code it
    could have been mistaken for. check_behaviour_exclusion() covers the preferred-term
    and declared-behaviour rules once BEHAVIOUR_DECLARED_BY_GROUP carries GROUP7; it
    reads neither group_declares nor the stem.
    """
    if ctx.group != GROUP7:
        return []
    out, seen = [], 0
    index, err = load_icdo32(layer1)
    for node_id, node in sorted(ctx.nodes.items()):
        for holder, where in walk_dicts(node):
            be = holder.get("behaviour_exclusion")
            if not isinstance(be, dict):
                continue
            seen += 1
            loc = "node %s (%s) behaviour_exclusion" % (node_id, where)
            if be.get("group_declares") != "3":
                out.append((FAIL, "RULE 3 — %s: group_declares is %r; Group VII declares "
                                  "the single behaviour \"3\" (contract §0.2)"
                            % (loc, be.get("group_declares"))))
            code = as_code(be.get("icdo_code"))
            beh = str(be.get("icdo_behaviour") or "").strip()
            if code not in GROUP7_CODES and code not in GROUP7_ABSENT_CODES:
                out.append((FAIL, "RULE 3 — %s: icdo_code %s is not on a Group VII stem; a "
                                  "benign lesion with no Group VII code is non_reportable, "
                                  "not a behaviour exclusion" % (loc, code)))
            if index and not index.get((code, beh)):
                out.append((FAIL, "RULE 3 — %s: %s/%s is not a real pair in icdo32.sqlite"
                            % (loc, code, beh)))
            elif err:
                out.append((WARN, "RULE 3 — %s: icdo32.sqlite unavailable (%s)" % (loc, err)))
    if not seen:
        return []
    if not [f for f in out if f[0] == FAIL]:
        out.append((OK, "RULE 3 — %d behaviour_exclusion block(s) declare \"3\", sit on "
                        "Group VII stems and round-trip to icdo32.sqlite" % seen))
    return out


def check_group7_ini1_fork(ctx: DTContext, repo: Path = None):
    """
    GROUP 7 RULE 4 (contract §4.3, §8 rule 4) — THE GROUP'S SIGNATURE CHECK.

    Vokuhl 2016 (p. 925): of 23 tumours first called small cell undifferentiated
    hepatoblastoma or malignant rhabdoid tumour, 22 had lost INI1. So:

      (a) every terminal emitting 8963 names a SMARCB1/INI1 or SMARCA4/BRG1 LOSS marker
          in its `positive` list — rhabdoid tumour is never reached on morphology alone;
      (b) no rule emitting 8970 names a loss marker as positive;
      (c) no terminal emitting 8970 ASSERTS a small cell undifferentiated, blastemal or
          rhabdoid tumour in its option text unless the same rule requires INI1
          RETAINED as a positive marker. "Asserts" is negation-aware: the hepatoblastoma
          option reads "with no small cell undifferentiated or rhabdoid component
          predominating", which names the pattern only to rule it out;
      (d) every option that asserts such a tumour and routes onward reaches an
          ihc_checklist carrying both an 8963 rule and an INI1-retained 8970 rule, and
          that node's nos_fallback is not 8970.

      (f) every option routing into the INI1 step from which an 8970 rule can fire —
          its captures satisfy that rule's `when` — describes a small cell
          undifferentiated pattern. Added after review, 3 October 2026: one option once
          carried both "small cell undifferentiated" and "malignant rhabdoid tumour"
          into the step, and an INI1-retained malignant rhabdoid tumour (Vokuhl 2016,
          p. 927, case 17) reached 8970 with "Workup: complete";
      (g) every INI1-step rule that codes on INI1 retained without SMARCA4 retained names
          IHC in `outstanding_tests` and SMARCA4 in its upgrade line. Registrar ruling,
          3 October 2026 (open question 18): SMARCA4 not done gives the same code as both
          retained, with SMARCA4 shown as owed. (f) also admits an option stating that the
          report diagnoses hepatoblastoma, which reaches the INI1 step when rhabdoid cells are
          described in it;
      (a') the one exemption from (a): an option whose label says the report DIAGNOSES a
          malignant rhabdoid tumour may emit 8963 on that diagnosis, because rhabdoid
          tumour is still a histomorphological diagnosis (López-Terrada 2014, p. 479). It
          must not also describe a small cell undifferentiated pattern;
      (e) no alias in aliases_group_07.json that maps to 8970 asserts a small cell
          undifferentiated, blastemal or rhabdoid tumour. Found in the browser on
          2 October 2026, not by the build: an alias mapped to both 8970 and 8963 put
          "SCUD hepatoblastoma" under "Also called" on every 8970 output, including a
          case coded on imaging alone.

    (c) would FAIL a correct option such as "hepatoblastoma with minor small cell
    undifferentiated foci" that emits 8970 directly; no such option exists today, and one
    added later should either route to the INI1 step or carry an INI1-retained marker.

    (c) is the condition, not the destination: a check that only tested "the SCUD
    option has a next_node" would pass a tree whose INI1 node codes 8970 on nothing
    (memory: checks must test conditions, not destinations).
    """
    if ctx.group != GROUP7:
        return []
    out = []

    def positives(holder):
        return [str(p) for p in (holder.get("positive") or [])]

    rhabdoid_rules = 0
    for code, holder, node_id, where in ctx.emissions():
        pos = positives(holder)
        has_loss = any(_G7_LOSS_MARKER_RE.search(p) for p in pos)
        has_retained = any(_G7_RETAINED_MARKER_RE.search(p) for p in pos)
        if code == GROUP7_RHABDOID_CODE:
            rhabdoid_rules += 1
            label = str(holder.get("label") or "")
            diagnosed = bool(_G7_MRT_DIAGNOSED_RE.search(label)) \
                and not _g7_asserted(label, _G7_SMALL_CELL_RE)
            if not has_loss and not diagnosed:
                out.append((FAIL, "RULE 4(a) — node %s (%s) emits 8963 without a SMARCB1/INI1 "
                                  "or SMARCA4/BRG1 loss marker in `positive` — malignant "
                                  "rhabdoid tumour reached on morphology alone (contract §4.3)"
                            % (node_id, where)))
        if code == GROUP7_HEPATOBLASTOMA_CODE:
            if has_loss:
                out.append((FAIL, "RULE 4(b) — node %s (%s) emits 8970 on an INI1/SMARCA4 "
                                  "loss marker; loss is malignant rhabdoid tumour (Vokuhl "
                                  "2016, p. 925)" % (node_id, where)))
            if _g7_asserted(_g7_option_text(holder), _G7_SCUD_RE) and not has_retained:
                out.append((FAIL, "RULE 4(c) — node %s (%s) emits 8970 for a branch that "
                                  "asserts a small cell undifferentiated or rhabdoid tumour "
                                  "with no INI1-retained marker required: %r (contract §4.3)"
                            % (node_id, where, _g7_option_text(holder)[:160])))
    if not rhabdoid_rules:
        out.append((FAIL, "RULE 4 — no terminal emits 8963; the INI1 fork is missing"))

    routed = 0
    for node_id, node in sorted(ctx.nodes.items()):
        for holder, where in _branch_containers(node):
            target = holder.get("next_node")
            if not target or as_code(holder.get("morphology_code")):
                continue
            if not _g7_asserted(_g7_option_text(holder), _G7_SCUD_RE):
                continue
            routed += 1
            dest = ctx.nodes.get(target) or {}
            rules = dest.get("resolution_logic") or []
            ok_8963 = any(as_code(r.get("morphology_code")) == GROUP7_RHABDOID_CODE
                          for r in rules if isinstance(r, dict))
            ok_8970 = any(as_code(r.get("morphology_code")) == GROUP7_HEPATOBLASTOMA_CODE
                          and any(_G7_RETAINED_MARKER_RE.search(p) for p in positives(r))
                          for r in rules if isinstance(r, dict))
            fb = as_code((dest.get("nos_fallback") or {}).get("code"))
            if dest.get("node_type") != "ihc_checklist" or not ok_8963 or not ok_8970:
                out.append((FAIL, "RULE 4(d) — node %s (%s) routes a small cell "
                                  "undifferentiated or rhabdoid tumour to %s, which is not an "
                                  "ihc_checklist carrying both an 8963 loss rule and an "
                                  "INI1-retained 8970 rule" % (node_id, where, target)))
            if fb == GROUP7_HEPATOBLASTOMA_CODE:
                out.append((FAIL, "RULE 4(d) — %s falls back to 8970 when INI1 is not done; "
                                  "the fallback must not be hepatoblastoma (contract §4.3)"
                            % target))
    if not routed:
        out.append((FAIL, "RULE 4(d) — no option routes a small cell undifferentiated or "
                          "rhabdoid tumour to the INI1 step"))
    for node_id, node in sorted(ctx.nodes.items()):
        for holder, where in _branch_containers(node):
            target = holder.get("next_node")
            dest = ctx.nodes.get(target) if target else None
            if not dest or dest.get("node_type") != "ihc_checklist":
                continue
            captured = dict(holder.get("captures") or {})
            captured.setdefault("primary_site", "C22")
            for r in dest.get("resolution_logic") or []:
                if not isinstance(r, dict) or as_code(r.get("morphology_code")) != GROUP7_HEPATOBLASTOMA_CODE:
                    continue
                when = r.get("when") or {}
                fires = all(str(captured.get(k)) in [str(v) for v in (w if isinstance(w, list) else [w])]
                            for k, w in when.items())
                text = _g7_option_text(holder)
                if fires and not _g7_asserted(text, _G7_SMALL_CELL_RE) \
                        and not _G7_HB_DIAGNOSED_RE.search(text):
                    out.append((FAIL, "RULE 4(f) — node %s (%s) routes into %s, whose 8970 rule "
                                      "can fire for it, but the option does not describe a small "
                                      "cell undifferentiated pattern or a report that diagnoses "
                                      "hepatoblastoma: %r. An INI1-retained "
                                      "rhabdoid tumour would be recoded as hepatoblastoma "
                                      "(Vokuhl 2016, p. 927)"
                                % (node_id, where, target, _g7_option_text(holder)[:120])))
    for code, holder, node_id, where in ctx.emissions():
        if "resolution_logic" not in where:
            continue
        pos = positives(holder)
        if not any(_G7_RETAINED_MARKER_RE.search(p) for p in pos) \
                or any(_G7_SMARCA4_RETAINED_RE.search(p) for p in pos):
            continue
        if "IHC" not in (holder.get("outstanding_tests") or []) \
                or not re.search(r"SMARCA4", str(holder.get("upgrade_path") or "")):
            out.append((FAIL, "RULE 4(g) — node %s (%s) emits %s on INI1 retained without "
                              "SMARCA4 retained, but does not show IHC as outstanding with an "
                              "upgrade line naming SMARCA4; the output would read 'Complete' "
                              "on a panel that never excluded a SMARCA4-deficient malignant "
                              "rhabdoid tumour (Fazlollahi 2019, §4.1.1; registrar ruling, "
                              "3 October 2026)" % (node_id, where, code)))
    alias_path = repo / "data" / "aliases" / "aliases_group_07.json" if repo else None
    if alias_path is not None and alias_path.exists():
        aliases, _ = load_json(alias_path)
        for i, entry in enumerate(aliases if isinstance(aliases, list) else []):
            if not isinstance(entry, dict):
                continue
            codes = [as_code(c) for c in entry.get("maps_to_morphology_codes") or []]
            if GROUP7_HEPATOBLASTOMA_CODE not in codes:
                continue
            words = [entry.get("alias") or ""] + list(entry.get("also_known_as") or [])
            if any(_g7_asserted(str(w), _G7_SCUD_RE) for w in words):
                out.append((FAIL, "RULE 4(e) — aliases_group_07.json[%d] %r maps to 8970 and "
                                  "names a small cell undifferentiated or rhabdoid tumour; it "
                                  "would be listed as another name for hepatoblastoma on "
                                  "every 8970 output, whatever INI1 showed (contract §4.3)"
                            % (i, entry.get("alias"))))
    if not [f for f in out if f[0] == FAIL]:
        out.append((OK, "RULE 4 — %d 8963 terminal(s), each on an INI1/SMARCA4 loss marker "
                        "or on a report that diagnoses malignant rhabdoid tumour; no 8970 "
                        "terminal codes a small cell undifferentiated or "
                        "rhabdoid tumour without INI1 retained; %d routing option(s) reach "
                        "a complete INI1 fork" % (rhabdoid_rules, routed)))
    return out


def check_group7_cnset(ctx: DTContext, layer1: Path):
    """
    GROUP 7 RULE 10 — calcifying nested stromal-epithelial tumour, registrar ruling of
    3 October 2026 (open question 2). Keyed off Layer 1 and off the option text:

      (a) the anchors still hold: icdo32.sqlite prints 8975/1, and ICCC-2017 places 8975
          in a Group VII range at behaviour 3. If either moves, the ruling needs revisiting;
      (b) both entries exist, 8975/1 and 8975/3, and the tree emits both;
      (c) 8975/3 is emitted only where the option says the report calls the tumour malignant
          or describes metastases — the matrix rule changes the digit to what the pathologist
          reports, so the evidence must be in the branch the clerk chose;
      (d) 8975/1 is never emitted where the option asserts malignancy or metastases.
    """
    if ctx.group != GROUP7:
        return []
    out = []
    index, err = load_icdo32(layer1)
    if err:
        return [(WARN, "RULE 10 — icdo32.sqlite unavailable (%s); the 8975 anchors are NOT "
                       "checked" % err)]
    if not index.get(("8975", "1")):
        out.append((FAIL, "RULE 10(a) — icdo32.sqlite no longer prints 8975/1; the registrar's "
                          "ruling on calcifying nested stromal-epithelial tumour has lost its anchor"))
    hits = _g7_iccc_subgroups(layer1, "8975", "C22.0")
    if hits is None:
        out.append((WARN, "RULE 10(a) — ICCC-2017.sqlite not found; the VIIa1 anchor is NOT checked"))
    elif not [sg for main, sg in hits if main == "VII"]:
        out.append((FAIL, "RULE 10(a) — ICCC-2017 no longer places 8975/3 in Group VII"))
    have = {(as_code(e.get("morphology_code")), str(e.get("behavior_code") or "").strip())
            for e in ctx.entries if isinstance(e, dict)}
    emitted = set()
    for code, holder, node_id, where in ctx.emissions():
        beh = str(holder.get("behavior_code") or "3").strip()
        if code != "8975":
            continue
        emitted.add(beh)
        text = _g7_option_text(holder)
        says_malignant = _g7_asserted(text, _G7_MALIGNANT_RE)
        if beh == "3" and not says_malignant:
            out.append((FAIL, "RULE 10(c) — node %s (%s) emits 8975/3, but the option does not say "
                              "the report calls the tumour malignant or describes metastases: %r"
                        % (node_id, where, text[:140])))
        if beh == "1" and says_malignant:
            out.append((FAIL, "RULE 10(d) — node %s (%s) emits 8975/1 on an option that asserts "
                              "malignancy or metastases: %r" % (node_id, where, text[:140])))
    for pair in sorted(GROUP7_RULED_PAIRS):
        if pair not in have:
            out.append((FAIL, "RULE 10(b) — no morphology entry for %s/%s" % pair))
        if pair[1] not in emitted:
            out.append((FAIL, "RULE 10(b) — no branch emits %s/%s" % pair))
    if not out:
        out.append((OK, "RULE 10 — 8975/1 and 8975/3 anchored on icdo32.sqlite and ICCC-2017; "
                        "8975/3 only where the report calls the tumour malignant or metastatic"))
    return out


def _g7_node_exits(node):
    """(target, holder) for every onward edge of a node, including the imaging route's
    insufficient_next_node, which _node_edges() does not follow."""
    for holder, _where in _branch_containers(node):
        if holder.get("next_node"):
            yield holder["next_node"], holder
    if node.get("insufficient_next_node"):
        yield node["insufficient_next_node"], {}


def _g7_captures_c22(holder):
    value = (holder.get("captures") or {}).get("primary_site")
    return isinstance(value, str) and value in GROUP7_C22_VALUES


def _g7_when_c22(holder):
    want = (holder.get("when") or {}).get("primary_site")
    vals = want if isinstance(want, list) else [want]
    return any(isinstance(v, str) and v in GROUP7_C22_VALUES for v in vals)


def check_group7_c22_only_codes(ctx: DTContext):
    """
    GROUP 7 RULE 5 (contract §3.4, §8 rule 5) — a code that is Group VII only at
    C22.0/C22.1 (everything except 8970, 8160-8162 and 8170-8180) is emitted only on a
    route that has established the liver: some edge on every path from the entry node
    captured primary_site C22, or the emitting branch itself captures it or carries a
    `when` on it. Every 8963 rule additionally carries `when` primary_site C22, so the
    INI1 fork names its site on the rule that decides it, the Group VI precedent.

    A walk forward from each tree's entry node, following only edges that do NOT
    capture C22, finds every node reachable with the site unproven.

    Known limit, recorded after review: `primary_site` C22 is captured by the evidence
    step on every route, because the tree is entered for a liver mass, so the `when` on
    the 8963 rules is satisfied by the file's own capture and never reads the topography
    the router recorded. The check proves the capture cannot be bypassed, not that the
    case's topography is C22 — the router's dual-group rules and rule 9 cover that.
    """
    if ctx.group != GROUP7:
        return []
    out = []
    unproven = set()
    for tree in ctx.trees:
        entry = tree.get("entry_node")
        if entry in ctx.nodes:
            unproven.add(entry)
    stack = list(unproven)
    while stack:
        current = stack.pop()
        for target, holder in _g7_node_exits(ctx.nodes[current]):
            if target in ctx.nodes and target not in unproven and not _g7_captures_c22(holder):
                unproven.add(target)
                stack.append(target)
    checked = 0
    for code, holder, node_id, where in ctx.emissions():
        if code not in GROUP7_C22_ONLY_CODES:
            continue
        checked += 1
        if node_id in unproven and not _g7_captures_c22(holder) and not _g7_when_c22(holder):
            out.append((FAIL, "RULE 5 — node %s (%s) emits %s, a Group VII code only at "
                              "C22.0/C22.1, on a route where the liver was never "
                              "established (contract §3.4)" % (node_id, where, code)))
        if code == GROUP7_RHABDOID_CODE and "resolution_logic" in where and not _g7_when_c22(holder):
            out.append((FAIL, "RULE 5 — node %s (%s) emits 8963 without `when` primary_site "
                              "C22; 8963 is VIa2 at the kidney and IXd3 elsewhere "
                              "(ICCC-2017 rows 60, 68, 102)" % (node_id, where)))
    if not out:
        out.append((OK, "RULE 5 — %d emission(s) of C22-only codes all sit on routes that "
                        "establish the liver; every 8963 rule names primary_site C22"
                        % checked))
    return out


def check_group7_no_tissue_codes(ctx: DTContext):
    """
    GROUP 7 RULE 6 (contract §0.6, §8 rule 6) — Visser 2023 Tables 3 and 4 bound what a
    terminal without pathology may name. A branch at basis 0, 1, 2 or 4, or an
    imaging_pathway / no_tissue node, may emit only 8970/3 at basis 2 (Table 3) or
    8000/3 at basis 1 or 2 (rule 5). Basis 4 is not built (registrar item §11.4), and
    basis 1 never carries a specific code.
    """
    if ctx.group != GROUP7:
        return []
    out, seen = [], 0
    for code, holder, node_id, where in ctx.emissions():
        node = ctx.nodes.get(node_id) or {}
        basis = holder.get("basis_of_diagnosis")
        no_path = (isinstance(basis, int) and basis in GROUP7_NO_PATHOLOGY_BASES) \
            or holder.get("no_tissue") is True or holder is node and node.get("node_type") == "imaging_pathway"
        if not no_path:
            continue
        seen += 1
        if (code, basis) not in GROUP7_NO_PATHOLOGY_ALLOWED:
            out.append((FAIL, "RULE 6 — node %s (%s) emits %s at basis %r without "
                              "pathology; Visser allows only 8970/3, 8170/3 and 8160/3 at basis 2 "
                              "(Table 3), 8170/3 at basis 4 (Table 4) and 8000/3 at basis 2, or at 9 "
                              "when the method is unknown (rules 1, 5); basis 1 never, since a liver "
                              "tumour is not found by physical examination (rule 3) (contract §0.6)" % (node_id, where, code, basis)))
        elif basis == 4 and not _g7_asserted(_g7_option_text(holder), _G7_AFP_RAISED_RE):
            out.append((FAIL, "RULE 6 — node %s (%s) emits %s at basis 4, but the option does not "
                              "say alpha-fetoprotein is raised; Visser Table 4 grants basis 4 on the "
                              "marker (p. 06)" % (node_id, where, code)))
    if not out:
        out.append((OK, "RULE 6 — %d no-pathology emission(s), all on Visser's Table 3, Table 4 "
                        "or rule 5 rows; basis 4 only on a raised alpha-fetoprotein" % seen))
    return out


def check_group7_imaging_constellation(ctx: DTContext):
    """
    GROUP 7 RULE 7 (contract §4.2, §8 rule 7) — imaging_sufficient is true on 8970 only,
    and every imaging_pathway node that codes 8970 asks for a raised alpha-fetoprotein
    (a biochemical question requiring "yes") and carries both age diversions: 3 years
    or older, and younger than 6 months (Design Specification §3.6; Ferraro 2019,
    PDF p. 7). Without the alpha-fetoprotein question a liver mass on imaging alone
    would code hepatoblastoma; without the lower age bound a neonate's physiological
    alpha-fetoprotein would.
    """
    if ctx.group != GROUP7:
        return []
    out = []
    for entry in ctx.entries:
        if isinstance(entry, dict) and entry.get("imaging_sufficient") is True \
                and as_code(entry.get("morphology_code")) != GROUP7_IMAGING_SUFFICIENT_CODE:
            out.append((FAIL, "RULE 7 — entry %s is imaging_sufficient; only 8970 is "
                              "(Visser Table 3)" % entry.get("morphology_code")))
    nodes = 0
    for node_id, node in sorted(ctx.nodes.items()):
        if node.get("node_type") != "imaging_pathway":
            continue
        nodes += 1
        if as_code(node.get("morphology_code")) != GROUP7_IMAGING_SUFFICIENT_CODE:
            out.append((FAIL, "RULE 7 — imaging node %s codes %s; the imaging route is "
                              "for 8970 only" % (node_id, node.get("morphology_code"))))
        afp = [q for q in node.get("biochemical_questions") or []
               if isinstance(q, dict) and re.search(r"alpha-fetoprotein|\bAFP\b",
                                                    str(q.get("question")), re.I)
               and str(q.get("required_answer")) == "yes"]
        if not afp:
            out.append((FAIL, "RULE 7 — imaging node %s has no alpha-fetoprotein question "
                              "requiring \"yes\"" % node_id))
        feats = " | ".join(str(d.get("feature")) for d in node.get("diversion_criteria") or []
                           if isinstance(d, dict))
        if not re.search(r"\b3 years\b", feats):
            out.append((FAIL, "RULE 7 — imaging node %s has no diversion for a child of 3 "
                              "years or older" % node_id))
        if not re.search(r"\b6 months\b", feats):
            out.append((FAIL, "RULE 7 — imaging node %s has no diversion for an infant "
                              "younger than 6 months" % node_id))
    if not nodes:
        out.append((FAIL, "RULE 7 — no imaging_pathway node; the hepatoblastoma imaging "
                          "route is missing"))
    if not out:
        out.append((OK, "RULE 7 — imaging_sufficient on 8970 only; %d imaging node(s) "
                        "require a raised alpha-fetoprotein and divert both age bounds"
                        % nodes))
    return out


def check_group7_fibrolamellar(ctx: DTContext):
    """
    GROUP 7 RULE 8 (contract §3.2, §8 rule 8) — fibrolamellar carcinoma codes 8171/3.

      (a) at least one terminal emits 8171 — the code must not collapse back to 8170,
          which is what the diagnostic pathway document instructed;
      (b) a histology or morphology option whose label asserts fibrolamellar carcinoma
          never emits a code other than 8171 (it may route onward);
      (c) a branch whose label asserts a DNAJB1::PRKACA fusion, a PRKACA rearrangement or
          PRKAR1A loss emits 8171 and nothing else. "Asserts" is negation-aware, so the
          option "Tested, neither alteration found ..." is not read as a finding;
      (d) inside the MOLECULAR step a fibrolamellar option routes to (a
          cytogenetics_dropdown or molecular_freetext node), every branch emits 8171 except
          one whose label says the report REVISES the diagnosis. Added after the first
          negative-control pass, 2 October 2026: an "untested" option re-pointed at 8170
          names no fibrolamellar or molecular finding in its own label, so (b) and (c) could
          not see it and (a) only asks that 8171 survive somewhere. Scoped to molecular
          nodes after the same pass raised a false FAIL on correct data: the histology
          option "Hepatocellular carcinoma, including fibrolamellar carcinoma" routes to the
          subtype node, whose scirrhous, clear cell and other options are rightly not 8171.
    """
    if ctx.group != GROUP7:
        return []
    out = []
    flc_nodes = set()
    for node_id, node in ctx.nodes.items():
        for holder, _where in _branch_containers(node):
            target = holder.get("next_node")
            if target and _marker_asserted(str(holder.get("label") or ""), _G7_FIBROLAMELLAR_RE) \
                    and (ctx.nodes.get(target) or {}).get("node_type") in (
                        "cytogenetics_dropdown", "molecular_freetext"):
                flc_nodes.add(target)
    for node_id in sorted(flc_nodes):
        for holder, where in _branch_containers(ctx.nodes.get(node_id) or {}):
            code = as_code(holder.get("morphology_code"))
            if code and code != GROUP7_FIBROLAMELLAR_CODE \
                    and not re.search(r"\brevis", str(holder.get("label") or ""), re.I):
                out.append((FAIL, "RULE 8(d) — node %s (%s), reached from a fibrolamellar "
                                  "option, emits %s on a branch that does not revise the "
                                  "diagnosis; fibrolamellar carcinoma is 8171/3 (contract "
                                  "§3.2)" % (node_id, where, code)))
    emits_8171 = 0
    for code, holder, node_id, where in ctx.emissions():
        if code == GROUP7_FIBROLAMELLAR_CODE:
            emits_8171 += 1
        node_type = (ctx.nodes.get(node_id) or {}).get("node_type")
        label = str(holder.get("label") or "")
        if node_type in ("histology_subclassification", "morphology_only") \
                and _marker_asserted(label, _G7_FIBROLAMELLAR_RE) \
                and code != GROUP7_FIBROLAMELLAR_CODE:
            out.append((FAIL, "RULE 8(b) — node %s (%s) codes fibrolamellar carcinoma as "
                              "%s; it is 8171/3 (contract §3.2)" % (node_id, where, code)))
        if _marker_asserted(label, _G7_FLC_MOLECULAR_RE) and code != GROUP7_FIBROLAMELLAR_CODE:
            out.append((FAIL, "RULE 8(c) — node %s (%s) records a fibrolamellar molecular "
                              "finding and emits %s; it is 8171/3 (Graham 2015, p. 822; "
                              "Graham 2018, PDF p. 2)" % (node_id, where, code)))
    if not emits_8171:
        out.append((FAIL, "RULE 8(a) — no terminal emits 8171; fibrolamellar carcinoma has "
                          "collapsed onto 8170 (contract §3.2, §5.1)"))
    if not out:
        out.append((OK, "RULE 8 — %d terminal(s) emit 8171; no fibrolamellar or molecular "
                        "finding is coded as anything else" % emits_8171))
    return out


def _g7_iccc_subgroups(layer1, code, topo):
    """ICCC-2017 subgroups that admit (code, topography) at behaviour 3, read straight
    from ICCC-2017.sqlite — the source of truth the router is checked against."""
    path = _iccc_path(layer1)
    if path is None or not path.exists():
        return None
    site = int(topo[1:3]) * 10 + int(topo[4])
    hits = []
    con = sqlite3.connect("file:%s?mode=ro" % path, uri=True)
    try:
        for group_code, main, hist, sites, beh in con.execute(
                "SELECT g.group_code, g.main_group, cr.icdo3_histology_raw, "
                "cr.icdo3_primary_site_raw, cr.icdo3_behavior FROM code_ranges cr "
                "JOIN groups g ON g.group_id = cr.group_id"):
            if "3" not in str(beh):
                continue

            def within(raw, value):
                for token in str(raw).split(","):
                    token = token.strip()
                    if not token:
                        continue
                    lo, _, hi = token.partition("-")
                    if int(lo) <= value <= int(hi or lo):
                        return True
                return False
            if within(hist, int(code)) and within(sites, site):
                hits.append((str(main), group_code))
    finally:
        con.close()
    return hits


def _g7_router_resolve(router, code, topo):
    """app.js resolveGroup() for the topography-keyed branch shape: first rule naming the
    code; `always`, else the first branch whose topography_in holds the site, else
    `default`.

    This is a PARTIAL transcription, and says so rather than reading as a full one.
    app.js branchMatches() also evaluates `captured_variable` branches against the
    captured state, and four live rules use that shape (9811-9819, 9823, 9827, 9260).
    Every Group VII code branches on topography alone, so the shapes agree here; a
    captured_variable branch raises instead of being silently read as "no match", which
    is what would make this helper quietly disagree with the engine it stands in for.
    Report.run() turns the raise into a FAIL."""
    for key, rule in (router.get("dual_group_rules") or {}).items():
        if not isinstance(rule, dict) or str(code) not in [str(c) for c in rule.get("codes") or []]:
            continue
        if rule.get("always"):
            return rule["always"], key
        for branch in rule.get("branches") or []:
            when = branch.get("when") or {}
            if "topography_in" in when:
                if topo in (when.get("topography_in") or []):
                    return branch.get("result"), key
            elif when.get("captured_variable"):
                raise ValueError(
                    "_g7_router_resolve: rule %r has a captured_variable branch (%r), a shape "
                    "this helper does not evaluate although app.js branchMatches() does; the "
                    "two would disagree on %s at %s"
                    % (key, when.get("captured_variable"), code, topo))
        return rule.get("default"), key
    return None, None


def check_group7_router_c22(repo: Path, layer1: Path):
    """
    GROUP 7 RULE 9 (contract §7.1, §8 rule 9) — the router agrees with ICCC-2017 for the
    rules this build owns. Keyed off ICCC-2017.sqlite, not off the router's own notes:

      * 8963, 8991 and 8000-8005 at C22.0 and C22.1 resolve to group 7 and to the very
        subgroup ICCC-2017 gives that (code, site);
      * every any-site Group VII code (8970, 8160-8162, 8170-8180) that has a rule at all
        resolves to group 7 at C22.0, C22.1, C24.0 and C80.9.
    """
    path = repo / "data" / "shared" / "presentation_router.json"
    router, _ = load_json(path) if path.exists() else (None, None)
    if not isinstance(router, dict):
        return [(NOTE, "presentation_router.json absent — Group 7 router check skipped")]
    if _iccc_path(layer1) is None or not _iccc_path(layer1).exists():
        return [(WARN, "RULE 9 — ICCC-2017.sqlite not found; the Group 7 router rules are "
                       "NOT checked against the recode")]
    out = []
    for code in GROUP7_ROUTER_C22_CODES:
        for topo in ("C22.0", "C22.1"):
            want = [sg for main, sg in _g7_iccc_subgroups(layer1, code, topo) if main == "VII"]
            got, rule = _g7_router_resolve(router, code, topo)
            if not got or got.get("group") != 7 or (want and got.get("subgroup") not in want):
                out.append((FAIL, "RULE 9 — router sends %s at %s to %r (rule %r); "
                                  "ICCC-2017 says group 7 %s (contract §7.1)"
                            % (code, topo, got, rule, "/".join(want) or "?")))
    for code in sorted(GROUP7_ANY_SITE_CODES):
        for topo in GROUP7_ROUTER_PROBE_SITES:
            got, rule = _g7_router_resolve(router, code, topo)
            if rule is not None and (not got or got.get("group") != 7):
                out.append((FAIL, "RULE 9 — router rule %r sends %s at %s to %r; ICCC-2017 "
                                  "row 67/71 places %s in Group VII at any site "
                                  "(contract §0.2 point 3)" % (rule, code, topo, got, code)))
    # The two lists above are written out by hand, so they only ever cover the codes
    # whoever wrote them thought of. 8158 'ACTH-producing tumor' is a VIIb entry that
    # ICCC-2017 range 70 puts at 220,221, and it shared the pituitary rule with 8290 and
    # took that rule's group 11 default at the liver — in neither list, so nothing here
    # saw it (found 4 October 2026, fixed by splitting the rule). This third pass asks
    # the question of EVERY Group VII entry another group's rule happens to name, keyed
    # off the entry file and the recode, so a code that acquires a rule later is covered
    # the day it does rather than when someone remembers to extend a tuple.
    dt_path = repo / "data" / "database" / "group_07_dt.json"
    dt, _ = load_json(dt_path) if dt_path.exists() else (None, None)
    swept = 0
    for entry in ((dt or {}).get("morphology_entries") or []):
        if not isinstance(entry, dict):
            continue
        code = as_code(entry.get("morphology_code"))
        if not code or code in GROUP7_ROUTER_C22_CODES or code in GROUP7_ANY_SITE_CODES:
            continue
        for topo in ("C22.0", "C22.1"):
            got, rule = _g7_router_resolve(router, code, topo)
            if rule is None:
                continue
            want = [sg for main, sg in (_g7_iccc_subgroups(layer1, code, topo) or [])
                    if main == "VII"]
            if not want:
                continue
            swept += 1
            if not got or got.get("group") != 7 or got.get("subgroup") not in want:
                out.append((FAIL, "RULE 9 — router rule %r sends %s at %s to %r, but "
                                  "ICCC-2017 places %s at that site in Group VII %s. A "
                                  "Group VII entry that another group's rule names must "
                                  "still reach Group VII (contract §7.1)"
                            % (rule, code, topo, got, code, "/".join(want))))
    if not out:
        out.append((OK, "RULE 9 — the router sends 8963, 8991 and 8000-8005 at C22.0/C22.1 "
                        "to the ICCC-2017 Group VII subgroup, every rule naming an "
                        "any-site Group VII code resolves to group 7, and %d further "
                        "(Group VII entry, liver) pair(s) that another group's rule names "
                        "resolve to the subgroup ICCC-2017 gives them" % swept))
    return out


def check_group7_subgroup_declaration(ctx: DTContext, layer1: Path):
    """
    GROUP 7 RULE 11 — every entry declares the ICCC-3 subgroup ICCC-2017 gives its code at
    the liver.

    Nothing asked this before. check_iccc_subgroup_ranges() asks it for most groups, but it
    reads the markdown table in Layer 1, which carries no rows for group 7 (nor group 5), so
    it returns a NOTE, "range report skipped", and checks nothing; check_group7_code_set()
    validates the (code, behaviour) pair against the generated inventory and never looks at
    iccc3_subgroup_id. Between them a Group VII entry could name any subgroup at all and the
    build stayed green: 8970 hepatoblastoma refiled as VIIb, hepatic carcinomas, passed all
    635 checks with 0 FAIL (negative control, 4 October 2026).

    The subgroup is what the registry records as the ICCC classification, and the recode
    disagreeing with the tool is the defect ruling 1 is about, so this is keyed off
    ICCC-2017.sqlite directly — the same source check_group7_router_c22() uses — and not off
    the entry file or the generator that wrote it.
    """
    if ctx.group != GROUP7:
        return []
    if _iccc_path(layer1) is None or not _iccc_path(layer1).exists():
        return [(WARN, "RULE 11 — ICCC-2017.sqlite not found; Group 7 subgroup declarations "
                       "are NOT checked against the recode")]
    out, seen = [], 0
    for i, entry in enumerate(ctx.entries):
        if not isinstance(entry, dict):
            continue
        code = as_code(entry.get("morphology_code"))
        if not code:
            continue
        # Behaviour 3 is what the recode classifies; the two ruled 8975 entries are
        # anchored on 8975/3's row by the same ruling that built them (contract §0.2).
        want = sorted({sg for main, sg in (_g7_iccc_subgroups(layer1, code, "C22.0") or [])
                       if main == "VII"})
        if not want:
            continue
        seen += 1
        if entry.get("iccc3_subgroup_id") not in want:
            out.append((FAIL, "RULE 11 — morphology_entries[%d] %s/%s declares ICCC-3 subgroup "
                              "%r, but ICCC-2017 places %s at C22.0 in Group VII %s — the "
                              "recode will disagree with the tool (contract §0.2)"
                        % (i, code, entry.get("behavior_code"),
                           entry.get("iccc3_subgroup_id"), code, "/".join(want))))
    if not out:
        out.append((OK, "RULE 11 — all %d Group VII entries declare the ICCC-3 subgroup "
                        "ICCC-2017 gives their code at C22.0" % seen))
    return out


# --------------------------------------------------------------------------------------
# Group 8 build contract §8 — Malignant Bone Tumours. Three rules, scoped to Group 8 and a
# no-op on every other group's file. GROUP8 is defined beside GROUP6, above
# BEHAVIOUR_DECLARED_BY_GROUP.
# --------------------------------------------------------------------------------------

# §0.6 / design D10 — Visser O, et al. Front Oncol 2023;13:1250549, Table 3 (pp. 04-05) gives
# osteosarcoma and chondrosarcoma basis 2 at C40/C41; this build uses osteosarcoma only, and
# rule 5 (p. 03) makes everything else without pathology 8000/3.
GROUP8_NO_TISSUE_CODES = {"9180", "8000"}
GROUP8_TISSUE_TESTS = {"Histology", "Cytology"}
GROUP8_RETIRED_CODE = "9260"
GROUP8_EWING_CODE = "9364"
# Markers that, with CD99, make a Ewing sarcoma immunophenotype or prove it outright
# (Kallen ME, Hornick JL. Semin Diagn Pathol 2022;39(1):29-37, p. 31 and Table 2).
GROUP8_EWING_PARTNER_TOKENS = ("NKX2-2", "FET::ETS")


def check_group8_no_retired_ewing_code(ctx: DTContext, layer1: Path, repo: Path):
    """
    GROUP 8 RULE 1 (contract §8.1) — nothing in Group VIII names 9260 at a behaviour
    ICD-O-3.2 does not carry.

    ICD-O-3.2 deleted 9260/3 Ewing sarcoma and moved it to 9364/3; 9260 survives only as
    9260/0 Aneurysmal bone cyst. viii_morph pick 33 still offers "9260 - Ewing sarcoma", so
    the number is one careless copy away from every Ewing branch. Keyed off icdo32.sqlite:
    the set of behaviours 9260 actually has is read from the database, not written here, so
    the one legitimate use — the aneurysmal bone cyst behaviour exclusion — passes because
    the database carries 9260/0, and nothing else can.

    Swept: every morphology_code, nos_fallback code, behaviour_exclusion icdo_code and
    refer_code in the tree; every entry's morphology_code and nos_fallback_code; every
    alias target in aliases_group_08.json (no alias may name 9260 at all — 9260/0 is benign
    and the alias layer carries only codes the group emits).
    """
    if ctx.group != GROUP8:
        return []
    index, err = load_icdo32(layer1)
    if err:
        return [(WARN, "GROUP 8 RULE 1 could not read icdo32.sqlite: %s" % err)]
    carried = {b for (c, b) in index if c == GROUP8_RETIRED_CODE}
    out, seen = [], 0
    pairs = (("morphology_code", "behavior_code"), ("code", "behavior_code"),
             ("icdo_code", "icdo_behaviour"), ("refer_code", None), ("nos_fallback_code", None))
    for tree in ctx.trees:
        for holder, where in walk_dicts(tree):
            for key, bkey in pairs:
                if as_code(holder.get(key)) != GROUP8_RETIRED_CODE:
                    continue
                seen += 1
                beh = holder.get(bkey) if bkey else None
                if beh is None or str(beh) not in carried:
                    out.append((FAIL, "%s: %s names %s/%s. ICD-O-3.2 carries %s only at "
                                      "behaviour(s) %s — Ewing sarcoma is %s/3 (IARC 'Deleted "
                                      "codes and their terms', 9 Oct 2020, p. 6)"
                                % (tree.get("tree_id"), where or key, GROUP8_RETIRED_CODE, beh,
                                   GROUP8_RETIRED_CODE, ", ".join(sorted(carried)) or "none",
                                   GROUP8_EWING_CODE)))
    for entry in ctx.entries:
        for key in ("morphology_code", "nos_fallback_code"):
            if as_code(entry.get(key)) == GROUP8_RETIRED_CODE:
                seen += 1
                out.append((FAIL, "morphology entry names %s in %s — no Group VIII entry may "
                                  "carry the retired Ewing sarcoma number"
                            % (GROUP8_RETIRED_CODE, key)))
    # Both alias-file shapes, as check_alias_cross_references() reads them. A missing file
    # is load_json()'s NOTE and is skipped; only a FAIL is carried.
    alias_path = Path(repo) / "data" / "aliases" / "aliases_group_08.json"
    aliases, found = load_json(alias_path)
    out.extend(f for f in found if f[0] == FAIL)
    if isinstance(aliases, dict):
        aliases = aliases.get("aliases")
    if aliases is not None and not isinstance(aliases, list):
        return out + [(FAIL, "GROUP 8 RULE 1: %s holds no alias list, so no alias could be "
                             "checked" % alias_path.name)]
    for a in aliases or []:
        if isinstance(a, dict) and GROUP8_RETIRED_CODE in [
                str(c) for c in a.get("maps_to_morphology_codes") or []]:
            seen += 1
            out.append((FAIL, "alias %r maps to %s, the retired Ewing sarcoma number; "
                              "Ewing sarcoma is %s"
                        % (a.get("alias"), GROUP8_RETIRED_CODE, GROUP8_EWING_CODE)))
    # The router held the stale 9260 rule until this build (docs/TODO.md §8.1, closed).
    router, found = load_json(Path(repo) / "data" / "shared" / "presentation_router.json")
    out.extend(f for f in found if f[0] == FAIL)
    for key, rule in sorted(((router or {}).get("dual_group_rules") or {}).items()):
        if isinstance(rule, dict) and GROUP8_RETIRED_CODE in [str(c) for c in
                                                              rule.get("codes") or []]:
            seen += 1
            out.append((FAIL, "presentation_router.json dual_group_rules[%r] routes %s, the "
                              "retired Ewing sarcoma number; Ewing sarcoma is %s"
                        % (key, GROUP8_RETIRED_CODE, GROUP8_EWING_CODE)))
    if not out:
        out.append((OK, "GROUP 8 RULE 1: %d reference(s) to %s, all at a behaviour ICD-O-3.2 "
                        "carries (%s); no entry or alias names the retired Ewing sarcoma "
                        "number" % (seen, GROUP8_RETIRED_CODE, ", ".join(sorted(carried)))))
    return out


def _group8_terminals_by_evidence(ctx: DTContext):
    """
    Walk every tree from its entry, carrying the clerk's evidence_tests the way app.js's
    capture() does (each capture REPLACES the value), and yield
    (node_id, branch, evidence_after_branch) for every code-emitting branch.

    The evidence a terminal is reached with is a property of the PATH, not of anything the
    terminal says about itself, which is why rule 2 reads it here rather than trusting the
    branch's own basis_of_diagnosis.

    The walk reads only the tree and is group-agnostic: Group 10 rule 2
    (check_group10_no_pathology_codes) uses it unchanged.
    """
    def after(holder, ev):
        cap = holder.get("captures") if isinstance(holder.get("captures"), dict) else {}
        return tuple(cap["evidence_tests"]) if "evidence_tests" in cap else ev

    for tree in ctx.trees:
        seen, stack = set(), [(tree.get("entry_node"), None)]
        while stack:
            node_id, ev = stack.pop()
            node = ctx.nodes.get(node_id)
            if node is None or (node_id, ev) in seen:
                continue
            seen.add((node_id, ev))
            for b, _ in _branch_containers(node):
                ev_b = after(b, ev)
                if as_code(b.get("morphology_code")):
                    yield node_id, b, ev_b
                if isinstance(b.get("next_node"), str):
                    stack.append((b["next_node"], ev_b))
            # imaging_pathway is its own terminal when the features hold, and falls through
            # to insufficient_next_node with the evidence it arrived with when they do not.
            if node.get("node_type") == "imaging_pathway":
                if as_code(node.get("morphology_code")):
                    yield node_id, node, after(node, ev)
                if isinstance(node.get("insufficient_next_node"), str):
                    stack.append((node["insufficient_next_node"], ev))
            fb = node.get("nos_fallback")
            if isinstance(fb, dict) and as_code(fb.get("code")):
                yield node_id, {"morphology_code": fb.get("code"), "_fallback": True}, ev


def check_group8_no_pathology_codes(ctx: DTContext):
    """
    GROUP 8 RULE 2 (contract §8.2) — a terminal reached with no tissue in the file emits
    9180/3 or 8000/3, at basis 1 or 2, and basis 1 only with 8000/3.

    Visser 2023 Table 3 licenses osteosarcoma and chondrosarcoma at C40/C41 on clinical
    investigation; this build licenses osteosarcoma only (design D10, Sharif 2021 p. 4), and
    rule 5 makes everything else 8000/3. A specific code at basis 2, or any code at basis 7
    with no tissue, makes a case look better evidenced than it is — the class of defect the
    project tests first.

    Keyed off the PATH (the evidence_tests in force when the terminal is reached), so a
    branch cannot pass by declaring a basis it was not reached with.
    """
    if ctx.group != GROUP8:
        return []
    out, checked = [], 0
    for node_id, b, ev in _group8_terminals_by_evidence(ctx):
        if ev is not None and GROUP8_TISSUE_TESTS & set(ev):
            continue
        checked += 1
        code = as_code(b.get("morphology_code"))
        basis = b.get("basis_of_diagnosis")
        label = b.get("label") or b.get("finding") or ("nos_fallback" if b.get("_fallback")
                                                       else node_id)
        if code not in GROUP8_NO_TISSUE_CODES:
            out.append((FAIL, "%s: %r emits %s with no tissue in the file. Without pathology "
                              "Group VIII may emit only %s (Visser 2023 rule 5, Table 3; "
                              "design D10)" % (node_id, label, code,
                                               " or ".join(sorted(GROUP8_NO_TISSUE_CODES)))))
        elif basis not in (1, 2):
            out.append((FAIL, "%s: %r emits %s with no tissue in the file at basis %r; a "
                              "no-tissue terminal is basis 1 or 2" % (node_id, label, code, basis)))
        elif basis == 1 and code != "8000":
            out.append((FAIL, "%s: %r emits %s at basis 1; only 8000/3 may be registered on "
                              "clinical information alone (Visser 2023 rule 5)"
                        % (node_id, label, code)))
    if not checked:
        return [(FAIL, "GROUP 8 RULE 2 found no no-tissue terminal at all — the imaging and "
                       "referral routes are missing or the walk is broken")]
    if not out:
        out.append((OK, "GROUP 8 RULE 2: %d terminal(s) reachable with no tissue, every one "
                        "emitting 9180/3 or 8000/3 at basis 1 or 2" % checked))
    return out


def check_group8_ewing_requires_partner(ctx: DTContext):
    """
    GROUP 8 RULE 3 (contract §8.3) — no marker rule emits Ewing sarcoma on CD99 alone.

    CD99 "is not specific for sarcomas such as Ewing sarcoma; it is also expressed in many
    acute leukemias" (Kallen & Hornick 2022, p. 30). A 9364 rule must also require NKX2-2 or
    a FET::ETS fusion. Keyed off the rule's own positive[] — its CONDITION — so a rule that
    reaches 9364 by a weaker condition fails even though its destination is right.
    """
    if ctx.group != GROUP8:
        return []
    out, checked = [], 0
    for node_id, node in ctx.nodes.items():
        for i, rule in enumerate(node.get("resolution_logic") or []):
            if not isinstance(rule, dict) or as_code(rule.get("morphology_code")) != GROUP8_EWING_CODE:
                continue
            checked += 1
            pos = [str(m) for m in rule.get("positive") or []]
            if not any(tok in m for m in pos for tok in GROUP8_EWING_PARTNER_TOKENS):
                out.append((FAIL, "%s resolution_logic[%d] emits %s on %s without NKX2-2 or a "
                                  "FET::ETS fusion (Kallen & Hornick 2022, pp. 30-31)"
                            % (node_id, i, GROUP8_EWING_CODE, pos or "no positive marker")))
    if not checked:
        return [(FAIL, "GROUP 8 RULE 3 found no marker rule emitting %s; the round cell panel "
                       "is missing" % GROUP8_EWING_CODE)]
    if not out:
        out.append((OK, "GROUP 8 RULE 3: %d marker rule(s) emit %s, each requiring NKX2-2 or a "
                        "FET::ETS fusion" % (checked, GROUP8_EWING_CODE)))
    return out


# --------------------------------------------------------------------------------------
# Group 10 build contract §5 — Germ Cell, Trophoblastic and Gonadal Tumours. Four rules,
# scoped to Group 10 and a no-op on every other group's file. GROUP10 is defined beside
# GROUP8, above BEHAVIOUR_DECLARED_BY_GROUP.
#
# ICCC-3 Group X places one (code, behaviour) in up to three subgroups by site: Xa in the
# central nervous system (ranges 94-99, behaviours 0, 1 and 3), Xb at every other
# extragonadal site (100-105), Xc in the gonads (106-112). The ranges are read from
# ICCC-2017.sqlite on every build; nothing below types a range.
# --------------------------------------------------------------------------------------

GROUP10_SITE_UNSTATED_TREE = "g10_site_unstated"
GROUP10_EXTRAGONADAL_TREE = "g10_extragonadal"
# Contract §3.1. ICCC-2017 fixes which topographies are Xa, Xb and Xc; the Xc topographies
# (569, 620-629) are split between the two gonad trees by their ICD-O-3 topography heading,
# C56 Ovary and C62 Testis.
GROUP10_TREE_BY_SITE_FAMILY = {"Xa": "g10_cns", "Xb": "g10_extragonadal"}
GROUP10_GONAD_TREE_BY_HEADING = {"C56": "g10_ovary", "C62": "g10_testis"}
# Contract §0.5. Visser O, et al. Front Oncol 2023;13:1250549: rule 5 (p. 03) registers a
# case without pathology as 8000/3 at basis 1 or 2; Table 4 (p. 06) registers a germ cell
# tumour with a raised human chorionic gonadotropin as 9064/3, with a raised
# alpha-fetoprotein as 9065/3, and choriocarcinoma of the placenta with a raised human
# chorionic gonadotropin as 9100/3, at basis 4; rule 6 (p. 05) makes basis 4 need a clinical
# investigation that shows the tumour.
GROUP10_TISSUE_TESTS = {"Histology", "Cytology"}
GROUP10_MARKER_EVIDENCE = {"Imaging", "Tumour markers"}
GROUP10_NO_TISSUE_CLINICAL_PAIRS = {("8000", "3")}
GROUP10_MARKER_PAIRS = {("9064", "3"), ("9065", "3")}
GROUP10_PLACENTAL_MARKER_PAIR = ("9100", "3")
# Design D21 builds "Teratoma" as the behaviour-neutral alias of 9080 and 9084. Rule 3 reads
# "Teratoma" as ICD-O-3.2's "Teratoma, NOS" (9080/1), because it reads "X" and "X, NOS" as
# one term, so without this entry D21's own built alias fails it. The key is the alias text
# with case and whitespace folded and nothing else, so it matches "Teratoma" alone and never
# "Teratoma, NOS" or "Teratomas"; the codes must be exactly these two. Any other spelling or
# code set goes through the full check.
GROUP10_D21_NEUTRAL_ALIASES = {"teratoma": frozenset({"9080", "9084"})}

_ICCC_X_CACHE: dict = {}


def _iccc_spans(raw):
    """ICCC-2017 raw token string -> [(lo, hi)]: '000-559,809' -> [(0, 559), (809, 809)]."""
    spans = []
    for token in str(raw or "").split(","):
        token = token.strip()
        if not token:
            continue
        lo, _, hi = token.partition("-")
        spans.append((int(lo), int(hi or lo)))
    return spans


def _in_spans(spans, value):
    return any(lo <= value <= hi for lo, hi in spans)


def _group10_iccc_ranges(layer1):
    """
    Every ICCC-2017 range for main group X, read from ICCC-2017.sqlite: a list of
    {range_id, subgroup, codes, sites, behaviours}, where codes and sites are (lo, hi) spans
    of the four-digit morphology and the three-digit topography, and behaviours is the set
    the range declares ('0-1,3' -> {'0', '1', '3'}). Returns (ranges, error_or_None).
    """
    path = _iccc_path(layer1)
    if path is None or not path.exists():
        return [], "ICCC-2017.sqlite not found at %s" % path
    key = str(path)
    if key in _ICCC_X_CACHE:
        return _ICCC_X_CACHE[key], None
    ranges = []
    try:
        con = sqlite3.connect("file:%s?mode=ro" % path, uri=True)
        try:
            for range_id, subgroup, hist, sites, beh in con.execute(
                    "SELECT cr.range_id, g.group_code, cr.icdo3_histology_raw, "
                    "cr.icdo3_primary_site_raw, cr.icdo3_behavior FROM code_ranges cr "
                    "JOIN groups g ON g.group_id = cr.group_id WHERE g.main_group = 'X' "
                    "ORDER BY cr.range_id"):
                behaviours = set()
                for lo, hi in _iccc_spans(beh):
                    behaviours.update(str(b) for b in range(lo, hi + 1))
                ranges.append({"range_id": range_id, "subgroup": str(subgroup),
                               "codes": _iccc_spans(hist), "sites": _iccc_spans(sites),
                               "behaviours": behaviours})
        finally:
            con.close()
    except (sqlite3.Error, ValueError) as exc:
        return [], "ICCC-2017.sqlite at %s could not be read: %s: %s" % (
            path, type(exc).__name__, exc)
    if not ranges:
        return [], "ICCC-2017.sqlite at %s holds no range for main group X" % path
    _ICCC_X_CACHE[key] = ranges
    return ranges, None


def _group10_fitting_ranges(ranges, code, behaviour, sites):
    """The Group X ranges that contain the code, declare the behaviour and cover at least one
    of the three-digit topographies in `sites`."""
    if not code or not str(code).isdigit() or behaviour is None:
        return []
    return [r for r in ranges
            if _in_spans(r["codes"], int(code)) and str(behaviour) in r["behaviours"]
            and any(_in_spans(r["sites"], s) for s in sites)]


def _group10_behaviour(value):
    return None if value is None else str(value).strip()


def _group10_emissions(ctx: DTContext):
    """
    Yield (node_id, where, code, behaviour) for every (code, behaviour) a node can emit: code
    branches on options, resolution_logic (the immunohistochemistry rules), bands and
    override_when; an imaging_pathway node's own code; and the nos_fallback code.
    """
    for node_id, node in ctx.nodes.items():
        for holder, where in _branch_containers(node):
            code = as_code(holder.get("morphology_code"))
            if code:
                what = holder.get("label") or holder.get("finding") or holder.get("positive")
                yield (node_id, "%s %r" % (where, what), code,
                       _group10_behaviour(holder.get("behavior_code")))
        if node.get("node_type") == "imaging_pathway" and as_code(node.get("morphology_code")):
            yield (node_id, "imaging_pathway", as_code(node.get("morphology_code")),
                   _group10_behaviour(node.get("behavior_code")))
        fb = node.get("nos_fallback")
        if isinstance(fb, dict) and as_code(fb.get("code")):
            yield (node_id, "nos_fallback", as_code(fb.get("code")),
                   _group10_behaviour(fb.get("behavior_code")))


def _group10_exclusions(ctx: DTContext):
    """Yield (node_id, where, code, behaviour) for every behaviour_exclusion block."""
    for node_id, node in ctx.nodes.items():
        for holder, where in walk_dicts(node):
            be = holder.get("behaviour_exclusion")
            if isinstance(be, dict):
                yield (node_id, "%s %r" % (where, holder.get("label")),
                       as_code(be.get("icdo_code")),
                       _group10_behaviour(be.get("icdo_behaviour")))


def _group10_route(tree_routing, topo):
    """app.js routedTree(): the first tree_routing rule whose topography_in holds the code,
    else the default. Matches literally, as firstTopographyMatch() does."""
    for rule in tree_routing.get("rules") or []:
        if isinstance(rule, dict) and topo in (rule.get("topography_in") or []):
            return rule.get("tree_id")
    return (tree_routing.get("default") or {}).get("tree_id")


def _group10_tree_routing(repo: Path):
    """(groups["10"].tree_routing or None, topography_lookup, findings) from the router and
    data/shared/topography_codes.json."""
    router, found = load_json(Path(repo) / "data" / "shared" / "presentation_router.json")
    lookup, found_t = _load_topography_lookup(repo)
    findings = [f for f in found + found_t if f[0] == FAIL]
    group = ((router or {}).get("groups") or {}).get(str(GROUP10)) if isinstance(router, dict) \
        else None
    tr = group.get("tree_routing") if isinstance(group, dict) else None
    return (tr if isinstance(tr, dict) else None), lookup, findings


def check_group10_codes_fit_site(ctx: DTContext, layer1: Path, repo: Path):
    """
    GROUP 10 RULE 1 (contract §5) — every code a site tree emits is a Group X code at that
    tree's site, every behaviour exclusion is not, and g10_site_unstated emits nothing.

    Source: ICCC-2017.sqlite, ranges 94-117 (main group X), read on every build. Xa admits
    behaviours 0, 1 and 3 in the central nervous system; every other range admits 3 only.
    So 9080/0 is a Group X code in g10_cns and a behaviour exclusion everywhere else, and the
    reverse of either is a defect.

    A tree's site is the set of topographies the router sends to it: every code in
    topography_codes.json's lookup, and every code a tree_routing rule names, resolved the
    way app.js routedTree() resolves it (first rule whose topography_in holds the code, else
    the default). The router is what puts a case in a tree, so the tree's own `topography`
    field is not read. Rule 4 holds the router to ICCC-2017 (Xa to g10_cns, Xb to
    g10_extragonadal), so the extragonadal tree's site is the Xb ranges.

    An emission (code branch, immunohistochemistry rule, nos_fallback) fits when some Group X
    range contains the code, declares the behaviour, and covers at least one topography of
    the tree that holds the node. A behaviour_exclusion fails when any such range exists:
    it hides a code the group registers. g10_site_unstated routes by cross-tree next_node
    and holds neither.
    """
    if ctx.group != GROUP10:
        return []
    ranges, err = _group10_iccc_ranges(layer1)
    if err:
        return [(WARN, "GROUP 10 RULE 1 could not read the ICCC-2017 Group X ranges: %s. No "
                       "emitted code is checked against its site" % err)]
    tr, lookup, out = _group10_tree_routing(repo)
    if tr is None:
        return out + [(FAIL, "GROUP 10 RULE 1: presentation_router.json has no "
                             "groups[\"10\"].tree_routing, so no tree has a site and no code "
                             "can be checked against one")]
    topos = set(lookup)
    for rule in tr.get("rules") or []:
        if isinstance(rule, dict):
            topos.update(t for t in rule.get("topography_in") or [] if isinstance(t, str))
    sites_by_tree: dict = {}
    for topo in topos:
        if _TOPO_RE.match(topo):
            sites_by_tree.setdefault(_group10_route(tr, topo), set()).add(_topo_index(topo))

    def holders(code):
        hit = [r for r in ranges if code and code.isdigit() and _in_spans(r["codes"], int(code))]
        return ", ".join("%d (%s, behaviour %s)" % (r["range_id"], r["subgroup"],
                                                    ",".join(sorted(r["behaviours"])))
                         for r in hit) or "none"

    checked, excluded = 0, 0
    for node_id, where, code, beh in _group10_emissions(ctx):
        tree = ctx.node_tree.get(node_id)
        if tree == GROUP10_SITE_UNSTATED_TREE:
            out.append((FAIL, "%s %s: %s emits %s/%s. %s routes by cross-tree next_node and "
                              "emits nothing (contract §4.5)"
                        % (tree, node_id, where, code, beh, GROUP10_SITE_UNSTATED_TREE)))
            continue
        checked += 1
        sites = sites_by_tree.get(tree, set())
        if not _group10_fitting_ranges(ranges, code, beh, sites):
            shown = [_topo_from_index(n) for n in sorted(sites)]
            out.append((FAIL, "%s %s: %s emits %s/%s, which no ICCC-2017 Group X range admits "
                              "at the %d topography code(s) the router sends to this tree "
                              "(%s). Ranges holding %s: %s"
                        % (tree, node_id, where, code, beh, len(sites),
                           ", ".join(shown[:6]) + (", ..." if len(shown) > 6 else "")
                           or "none", code, holders(code))))
    for node_id, where, code, beh in _group10_exclusions(ctx):
        tree = ctx.node_tree.get(node_id)
        if tree == GROUP10_SITE_UNSTATED_TREE:
            out.append((FAIL, "%s %s: %s excludes %s/%s. %s routes by cross-tree next_node "
                              "and holds no terminal (contract §4.5)"
                        % (tree, node_id, where, code, beh, GROUP10_SITE_UNSTATED_TREE)))
            continue
        excluded += 1
        fit = _group10_fitting_ranges(ranges, code, beh, sites_by_tree.get(tree, set()))
        if fit:
            out.append((FAIL, "%s %s: %s excludes %s/%s, but ICCC-2017 range %d (%s) admits "
                              "it at this tree's site, so the exclusion hides a Group X code"
                        % (tree, node_id, where, code, beh, fit[0]["range_id"],
                           fit[0]["subgroup"])))
    if not checked:
        out.append((FAIL, "GROUP 10 RULE 1 found no emitted code in any site tree"))
    if not [f for f in out if f[0] == FAIL]:
        out.append((OK, "GROUP 10 RULE 1: %d emission(s) each lie in an ICCC-2017 Group X "
                        "range covering the tree's routed site at that behaviour; %d behaviour "
                        "exclusion(s) lie in none; %s emits nothing"
                        % (checked, excluded, GROUP10_SITE_UNSTATED_TREE)))
    return out


def check_group10_no_pathology_codes(ctx: DTContext):
    """
    GROUP 10 RULE 2 (contract §5) — a terminal reached with neither histology nor cytology in
    the file registers what Visser 2023 allows and nothing more specific.

    Source: Visser O, et al. Front Oncol 2023;13:1250549. Rule 5 (p. 03): without pathology,
    8000/3 at basis 1 or 2. Table 4 (p. 06): a germ cell tumour with a raised human chorionic
    gonadotropin is 9064/3, with a raised alpha-fetoprotein 9065/3, and choriocarcinoma of
    the placenta with a raised human chorionic gonadotropin 9100/3, all at basis 4. Rule 6
    (p. 05): basis 4 needs a clinical investigation showing the tumour, here an imaging
    report. Rule 4 (p. 03): "possible" is not registrable.

    So on such a path: basis 1 and 2 emit only 8000/3; basis 4 emits only 9064/3 or 9065/3,
    or 9100/3 in g10_extragonadal, and only where the path's evidence holds both Imaging and
    Tumour markers; no other basis is reachable.

    Keyed off the PATH. The walk (_group8_terminals_by_evidence, which reads only the tree)
    starts at each tree's entry and carries evidence_tests the way app.js capture() does,
    each capture replacing the last, so a terminal's evidence is what the clerk said is on
    file on the way to it. Neither the branch's own basis_of_diagnosis nor the
    basis_evidence_tier flag can make a terminal pass.
    """
    if ctx.group != GROUP10:
        return []
    out, checked = [], 0
    for node_id, b, ev in _group8_terminals_by_evidence(ctx):
        if ev is not None and GROUP10_TISSUE_TESTS & set(ev):
            continue
        checked += 1
        code = as_code(b.get("morphology_code"))
        src = b
        if b.get("_fallback"):
            src = ctx.nodes[node_id].get("nos_fallback") or {}
        beh = _group10_behaviour(src.get("behavior_code"))
        basis = src.get("basis_of_diagnosis")
        try:
            basis = int(basis)
        except (TypeError, ValueError):
            pass
        tree = ctx.node_tree.get(node_id)
        label = b.get("label") or b.get("finding") or ("nos_fallback" if b.get("_fallback")
                                                       else node_id)
        held = list(ev) if ev is not None else []
        where = "%s %s: %r, reached with evidence %s" % (tree, node_id, label, held)
        if basis in (1, 2):
            if (code, beh) not in GROUP10_NO_TISSUE_CLINICAL_PAIRS:
                out.append((FAIL, "%s, emits %s/%s at basis %d. Without pathology Group X "
                                  "registers 8000/3 at basis 1 or 2 (Visser 2023 rule 5, "
                                  "p. 03)" % (where, code, beh, basis)))
        elif basis == 4:
            allowed = set(GROUP10_MARKER_PAIRS)
            if tree == GROUP10_EXTRAGONADAL_TREE:
                allowed.add(GROUP10_PLACENTAL_MARKER_PAIR)
            if (code, beh) not in allowed:
                out.append((FAIL, "%s, emits %s/%s at basis 4. Basis 4 registers 9064/3 or "
                                  "9065/3, and 9100/3 for choriocarcinoma of the placenta in "
                                  "%s only (Visser 2023 Table 4, p. 06)"
                            % (where, code, beh, GROUP10_EXTRAGONADAL_TREE)))
            elif not (GROUP10_MARKER_EVIDENCE <= set(held)):
                out.append((FAIL, "%s, emits %s/%s at basis 4 without both Imaging and Tumour "
                                  "markers on the path. Basis 4 needs a marker result and a "
                                  "clinical investigation showing the tumour (Visser 2023 "
                                  "Table 4, p. 06; rule 6, p. 05)" % (where, code, beh)))
        else:
            out.append((FAIL, "%s, emits %s/%s at basis %r with no histology or cytology in the "
                              "file. Without pathology Group X registers at basis 1, 2 or 4 "
                              "only (Visser 2023 rules 5-6, Table 4)"
                        % (where, code, beh, basis)))
    if not checked:
        return [(FAIL, "GROUP 10 RULE 2 found no terminal reachable without histology or "
                       "cytology: the referral, imaging and marker routes are missing or the "
                       "walk is broken")]
    if not out:
        out.append((OK, "GROUP 10 RULE 2: %d terminal(s) reachable without histology or "
                        "cytology, each emitting 8000/3 at basis 1 or 2, or a Visser Table 4 "
                        "code at basis 4 with Imaging and Tumour markers on the path" % checked))
    return out


def _group10_term_key(text):
    """Comparison form for an alias or an ICD-O-3.2 term: case and whitespace folded,
    'tumour' read as 'tumor', and a trailing ', NOS' dropped, so "Mature teratoma" meets
    ICD-O-3.2's "Mature teratoma, NOS"."""
    key = " ".join(str(text).lower().split()).replace("tumour", "tumor")
    return key[:-len(", nos")] if key.endswith(", nos") else key


def check_group10_alias_terms_match_icdo32(ctx: DTContext, layer1: Path, repo: Path):
    """
    GROUP 10 RULE 3 (contract §5, §6) — an alias that is an ICD-O-3.2 term says what
    ICD-O-3.2 says, at every behaviour the group emits.

    Source: icdo32.sqlite, every level (Preferred, Synonym, Related), [obs] terms included:
    an alias equal to an obsolete term still names that term's code; design D21. app.js
    lists aliases under "Also called" by four-digit code, so an alias on 9080 appears on
    every 9080 output whatever its behaviour. For every alias in
    aliases_group_10.json whose text equals an ICD-O-3.2 term (case folded, tumour/tumor
    normalised, a trailing ", NOS" dropped):

      * every code the alias maps to is a code ICD-O-3.2 files that term under;
      * the group emits that code at the term's behaviour and at no other (D21). The
        emitted set is read from the trees (code branches, immunohistochemistry rules,
        nos_fallback), not from the entries.

    And no alias containing "germinoma" but not "dysgerminoma" maps to 9060 Dysgerminoma:
    ICD-O-3.2 files Germinoma under 9064.

    One exemption, GROUP10_D21_NEUTRAL_ALIASES: D21 builds "Teratoma" on 9080 and 9084 as
    the behaviour-neutral alias. It matches that exact text (case and whitespace folded,
    before the ", NOS" step) mapped to exactly those two codes.

    With the alias file absent (Task T5 has not run) this returns a NOTE and checks nothing.
    With the file present, the rule FAILS when no alias outside the exemption equals an
    ICD-O-3.2 term: an empty list, or alias text under the wrong key, would otherwise pass
    a rule that checked nothing.
    """
    if ctx.group != GROUP10:
        return []
    path = Path(repo) / "data" / "aliases" / "aliases_group_10.json"
    if not path.exists():
        return [(NOTE, "GROUP 10 RULE 3: %s is not present (contract Task T5 writes it); no "
                       "alias is checked against icdo32.sqlite" % path.name)]
    aliases, found = load_json(path)
    out = [f for f in found if f[0] == FAIL]
    if isinstance(aliases, dict):
        aliases = aliases.get("aliases")
    if not isinstance(aliases, list):
        return out + [(FAIL, "GROUP 10 RULE 3: %s holds no alias list, so no alias could be "
                             "checked" % path.name)]
    index, err = load_icdo32(layer1)
    if err:
        return out + [(WARN, "GROUP 10 RULE 3 could not read icdo32.sqlite: %s. No alias is "
                             "checked against ICD-O-3.2" % err)]
    terms: dict = {}
    for (code, beh), bucket in index.items():
        for term, (_level, obs) in bucket.items():
            terms.setdefault(_group10_term_key(term), {})[(code, beh)] = (
                "%s %s" % (term, obs) if obs else term)
    emitted: dict = {}
    for _node, _where, code, beh in _group10_emissions(ctx):
        emitted.setdefault(code, set()).add(beh)

    matched, neutral = 0, 0
    for a in aliases:
        if not isinstance(a, dict):
            continue
        text = a.get("alias")
        maps = [str(c) for c in a.get("maps_to_morphology_codes") or []]
        low = str(text).lower()
        if "germinoma" in low and "dysgerminoma" not in low and "9060" in maps:
            out.append((FAIL, "alias %r maps to 9060 Dysgerminoma. ICD-O-3.2 files Germinoma "
                              "under 9064" % text))
        key = _group10_term_key(text)
        hits = terms.get(key)
        if not hits:
            continue
        exact = " ".join(low.split())
        if set(maps) == GROUP10_D21_NEUTRAL_ALIASES.get(exact):
            neutral += 1
            continue
        if not maps:
            continue
        matched += 1
        term_codes = {c for c, _b in hits}
        named = "; ".join("%r at %s/%s" % (t, c, b) for (c, b), t in sorted(hits.items()))
        for m in maps:
            if m not in term_codes:
                out.append((FAIL, "alias %r is the ICD-O-3.2 term %s, and maps to %s, a code "
                                  "ICD-O-3.2 does not file it under" % (text, named, m)))
        for c in sorted(term_codes & set(maps)):
            term_behs = {b for cc, b in hits if cc == c}
            em = emitted.get(c, set())
            if not em or not (em <= term_behs):
                out.append((FAIL, "D21 — alias %r is the ICD-O-3.2 term %s, and Group X emits "
                                  "%s at behaviour(s) %s. \"Also called\" lists aliases by "
                                  "four-digit code, so the alias would stand on outputs it is "
                                  "not true of (design D21)"
                            % (text, named, c,
                               ", ".join(sorted(str(b) for b in em)) or "none")))
    if not matched:
        out.append((FAIL, "GROUP 10 RULE 3: none of the %d alias(es) in %s outside the D21 "
                          "exemption equals an ICD-O-3.2 term, so the rule checked nothing. "
                          "The list is empty, or the alias text is not under the 'alias' key"
                    % (len(aliases), path.name)))
    if not [f for f in out if f[0] == FAIL]:
        out.append((OK, "GROUP 10 RULE 3: %d alias(es) in %s; %d equal an ICD-O-3.2 term and "
                        "map to its code, which Group X emits at that term's behaviour only; "
                        "%d D21 behaviour-neutral alias(es); no germinoma alias maps to 9060"
                        % (len(aliases), path.name, matched, neutral)))
    return out


def check_group10_subgroups_and_routing(ctx: DTContext, layer1: Path, repo: Path):
    """
    GROUP 10 RULE 4 (contract §5, design D16, D20) — the subgroup the tool shows and the tree
    the router picks agree with ICCC-2017 at every topography the lookup holds.

    Sources: ICCC-2017.sqlite ranges 94-117; data/shared/presentation_router.json
    groups["10"].tree_routing; data/shared/topography_codes.json topography_lookup.

    Subgroups. For every entry and every lookup topography where ICCC-2017 places the entry's
    (code, behaviour) in Group X, the subgroup app.js subgroupFor() shows (the first
    iccc3_subgroup_by_topography rule whose topography_in holds the code, else the entry's
    own iccc3_subgroup_id) is a subgroup ICCC-2017 gives that pair at that topography.

    Routing. The router, resolved as app.js routedTree() resolves it, sends every Xa
    topography (ICCC-2017 ranges 94-99) to g10_cns, every Xc topography under C56 to
    g10_ovary and under C62 to g10_testis (ranges 106-112), every Xb topography (ranges
    100-105) to g10_extragonadal, and every other lookup topography to the default, which is
    g10_site_unstated.
    """
    if ctx.group != GROUP10:
        return []
    ranges, err = _group10_iccc_ranges(layer1)
    if err:
        return [(WARN, "GROUP 10 RULE 4 could not read the ICCC-2017 Group X ranges: %s. "
                       "Subgroups and routing are NOT checked against the recode" % err)]
    tr, lookup, out = _group10_tree_routing(repo)
    topos = sorted(t for t in lookup if isinstance(t, str) and _TOPO_RE.match(t))
    if not topos:
        return out + [(FAIL, "GROUP 10 RULE 4: topography_codes.json enumerates no topography "
                             "code, so no subgroup or route can be checked")]

    pairs, entries_checked = 0, 0
    for i, entry in enumerate(ctx.entries):
        if not isinstance(entry, dict):
            continue
        code = as_code(entry.get("morphology_code"))
        beh = _group10_behaviour(entry.get("behavior_code"))
        rules = entry.get("iccc3_subgroup_by_topography") or []
        wrong, entry_pairs = [], 0
        for topo in topos:
            want = {r["subgroup"] for r in
                    _group10_fitting_ranges(ranges, code, beh, {_topo_index(topo)})}
            if not want:
                continue
            entry_pairs += 1
            got = entry.get("iccc3_subgroup_id")
            for rule in rules if isinstance(rules, list) else []:
                if isinstance(rule, dict) and topo in (rule.get("topography_in") or []):
                    got = rule.get("iccc3_subgroup_id")
                    break
            if got not in want:
                wrong.append((topo, got, "/".join(sorted(want))))
        pairs += entry_pairs
        entries_checked += bool(entry_pairs)
        if wrong:
            topo, got, want = wrong[0]
            out.append((FAIL, "morphology_entries[%d] %s/%s shows subgroup %r at %s, where "
                              "ICCC-2017 places it in %s; %d lookup topography code(s) "
                              "disagree in all (%s)"
                        % (i, code, beh, got, topo, want, len(wrong),
                           ", ".join(t for t, _g, _w in wrong[:6])
                           + (", ..." if len(wrong) > 6 else ""))))

    if tr is None:
        out.append((FAIL, "GROUP 10 RULE 4: presentation_router.json has no "
                          "groups[\"10\"].tree_routing (contract §3.1)"))
    else:
        default = (tr.get("default") or {}).get("tree_id")
        if default != GROUP10_SITE_UNSTATED_TREE:
            out.append((FAIL, "GROUP 10 RULE 4: groups[\"10\"].tree_routing.default is %r; a "
                              "case with no topography, or one outside the Group X germ cell "
                              "site ranges, goes to %s (contract §3.1, design D16)"
                        % (default, GROUP10_SITE_UNSTATED_TREE)))
        family_sites: dict = {}
        for r in ranges:
            family = r["subgroup"][:2]
            if family in ("Xa", "Xb", "Xc"):
                family_sites.setdefault(family, []).extend(r["sites"])
        for topo in topos:
            n = _topo_index(topo)
            family = next((f for f in ("Xa", "Xb", "Xc")
                           if _in_spans(family_sites.get(f, []), n)), None)
            if family == "Xc":
                want = GROUP10_GONAD_TREE_BY_HEADING.get(topo[:3])
            elif family:
                want = GROUP10_TREE_BY_SITE_FAMILY[family]
            else:
                want = GROUP10_SITE_UNSTATED_TREE
            got = _group10_route(tr, topo)
            if got != want:
                out.append((FAIL, "GROUP 10 RULE 4: the router sends %s to %r; ICCC-2017 "
                                  "makes it %s, which goes to %r (contract §3.1)"
                            % (topo, got, ("an %s topography" % family) if family
                               else "a topography outside the Group X germ cell site ranges",
                               want)))
    if not [f for f in out if f[0] == FAIL]:
        out.append((OK, "GROUP 10 RULE 4: %d of %d entries are placed in Group X by ICCC-2017 "
                        "at some lookup topography, and each shows the ICCC-2017 subgroup at "
                        "every one of the %d (entry, topography) pair(s) so placed; the router "
                        "sends all %d lookup topography codes to the tree ICCC-2017's site "
                        "ranges give them"
                        % (entries_checked, len(ctx.entries), pairs, len(topos))))
    return out


def check_codes_against_source_of_truth(ctx: DTContext, redcap_options: dict,
                                        classification: dict):
    """
    Every morphology_code appears in Layer 1 for that group.

    Absent from BOTH the REDCap options file and the ICCC classification table -> FAIL
    (Architecture §11 rule 1: never fabricate a code).
    Present in the classification table but with no REDCap option -> WARN.
    """
    out = []
    redcap = set(redcap_options.get(ctx.group, {}))
    classif = set(classification.get(ctx.group, set()))
    if not redcap and not classif:
        return [(NOTE, "no Layer 1 code list available for group %d — source-of-truth "
                 "check skipped" % ctx.group)]
    declared_awaiting = {}
    for entry in ctx.data.get("morphology_entries") or []:
        if isinstance(entry, dict) and isinstance(entry.get("awaiting_layer1"), dict):
            needs = entry["awaiting_layer1"].get("needs") or []
            declared_awaiting[str(entry.get("morphology_code"))] = ", ".join(needs) or "declared"
    no_option: list[str] = []
    for code in sorted(ctx.codes):
        in_redcap = code in redcap
        in_classif = code in classif
        if not in_redcap and not in_classif:
            # Ruling 3, 4 Sep 2026: a code the option list lacks is built, reported and put
            # on the to-do list rather than withheld — but only when the entry SAYS SO. An
            # entry that just appeared with no declaration is still a fabricated code.
            declared = declared_awaiting.get(code)
            if declared:
                out.append((WARN, "morphology_code %s is in neither Layer 1 list for group "
                                  "%d and is declared awaiting_layer1: %s"
                            % (code, ctx.group, declared)))
            else:
                out.append((FAIL, "morphology_code %s is in neither the REDCap options file "
                                  "nor the ICCC classification table for group %d — never "
                                  "fabricate a code (Architecture §11 rule 1). If it is a "
                                  "ratified ICD-O-3.2 addition, give the entry an "
                                  "`awaiting_layer1` object and list it in "
                                  "docs/codes-awaiting-redcap.md (ruling 3)."
                        % (code, ctx.group)))
        elif not in_redcap:
            no_option.append(code)
    if no_option:
        out.append((WARN, "%d code(s) verified in the ICCC classification table but with no "
                          "REDCap option yet: %s"
                    % (len(no_option), ", ".join(no_option))))
    if not out:
        out.append((OK, "all %d morphology_code(s) verified against Layer 1" % len(ctx.codes)))
    return out


# --------------------------------------------------------------------------------------
# B4b. The 4 September 2026 registrar rulings
#
# `../memory/registrar-rulings.md` holds the binding text. Each check below names the
# ruling it enforces so a future reader can tell a rule from a preference.
# --------------------------------------------------------------------------------------

def parse_classification_subgroups(layer1: Path):
    """{group: {subgroup_id: set(codes)}} from the ICCC-2017 table.

    parse_classification() above flattens the table to one code set per group, which is
    all the source-of-truth check needs. Ruling 1 asks a finer question — is this code in
    the range of the subgroup the entry CLAIMS — so the subgroup id has to survive.
    A row with an empty first cell continues the subgroup above it.
    """
    out: dict = {"_malformed": {}}
    if layer1 is None:
        return out
    path = layer1 / "ICCC 2017 Cancer Classification.md"
    if not path.exists():
        return out
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return out
    head_re = re.compile(r"^##\s+([IVX]+)\s*:")
    sub_re = re.compile(r"^([IVX]+[a-z]\d?)\b")
    group, subgroup = None, None
    for raw in text.splitlines():
        hm = head_re.match(raw)
        if hm:
            group = ROMAN.get(hm.group(1).upper())
            subgroup = None
            continue
        if group is None or not raw.lstrip().startswith("|"):
            continue
        cells = raw.split("|")
        if len(cells) < 4:
            continue
        name_cell, code_cell = cells[1].strip(), cells[2].strip()
        sm = sub_re.match(name_cell)
        if sm:
            subgroup = sm.group(1)
        if not code_cell or code_cell.lower() == "code" or set(code_cell) <= set("- :"):
            continue
        if subgroup is None:
            continue
        for token in code_cell.split(","):
            token = token.strip()
            if re.fullmatch(r"\d+", token):
                out.setdefault(group, {}).setdefault(subgroup, set()).add(token)
                continue
            rm = re.fullmatch(r"(\d+)\s*-\s*(\d+)", token)
            if rm and len(rm.group(1)) == len(rm.group(2)):
                lo, hi = int(rm.group(1)), int(rm.group(2))
                if lo <= hi and hi - lo <= 2000:
                    for n in range(lo, hi + 1):
                        out.setdefault(group, {}).setdefault(subgroup, set()).add(
                            str(n).zfill(len(rm.group(1))))
                    continue
            out["_malformed"].setdefault(group, []).append("%s (%s)" % (token, subgroup))
    return out


def check_iccc_subgroup_ranges(ctx: DTContext, subgroups: dict):
    """Ruling 1 — report a code outside its ICCC-2017 range; never block on it.

    The ruling that this replaced made the ICCC range the gate on whether a code could be
    built. It no longer is: paediatric occurrence decides that. But a code outside the
    range still fails to classify — the recode returns nothing and `iccc_code` does not
    populate — so it is reported here and it has to be on the to-do list.

    A code that IS in the group's ranges but filed under the WRONG subgroup is a
    different animal and stays a FAIL: nobody decided that, it is a mistake.
    """
    malformed = (subgroups.get("_malformed") or {}).get(ctx.group) or []
    table = subgroups.get(ctx.group) or {}
    if not table:
        return [(NOTE, "no ICCC-2017 subgroup table for group %d — range report skipped"
                 % ctx.group)]
    everything = set().union(*table.values())
    outside, misfiled = [], []
    for entry in ctx.data.get("morphology_entries") or []:
        if not isinstance(entry, dict):
            continue
        code = str(entry.get("morphology_code"))
        declared = entry.get("iccc3_subgroup_id")
        if code not in everything:
            outside.append((code, entry.get("morphology_name"), declared))
        elif declared in table and code not in table[declared]:
            actual = sorted(k for k, v in table.items() if code in v)
            misfiled.append((code, declared, actual))
    out = []
    for token in malformed:
        out.append((WARN, "the ICCC-2017 table's row for group %d carries a code range this "
                          "build cannot read: %s. Codes that the row was meant to cover will "
                          "be reported below as out-of-range, wrongly. Repairing the row is a "
                          "Layer 1 job." % (ctx.group, token)))
    for code, declared, actual in misfiled:
        out.append((FAIL, "morphology_code %s declares ICCC-3 subgroup %s but the ICCC-2017 "
                          "table puts it in %s — the recode will disagree with the tool"
                    % (code, declared, "/".join(actual))))
    for code, name, declared in outside:
        out.append((WARN, "morphology_code %s (%s) is outside every ICCC-2017 range for "
                          "group %d, so the recode returns nothing and iccc_code will not "
                          "populate. Declared %s. Extending the range is on the to-do list "
                          "(ruling 1)." % (code, name, ctx.group, declared)))
    if not out:
        out.append((OK, "all %d morphology_code(s) sit inside the ICCC-2017 range of the "
                        "subgroup they declare" % len(ctx.codes)))
    return out


def check_awaiting_layer1(ctx: DTContext, repo: Path):
    """Ruling 3 — a code REDCap cannot record is built, reported, and listed.

    The tree is allowed to run ahead of the option list. What is not allowed is running
    ahead of it silently, so the two facts have to agree: an entry carrying
    `awaiting_layer1` must appear in docs/codes-awaiting-redcap.md, and a code named there
    as open must still be carrying the flag.
    """
    todo = repo / "docs" / "codes-awaiting-redcap.md"
    if not todo.exists():
        return [(FAIL, "docs/codes-awaiting-redcap.md is missing — ruling 3 requires a "
                       "code absent from REDCap to be on a to-do list")]
    text = todo.read_text(encoding="utf-8")
    # The file carries one "## Group N — open" section per group. Only this group's
    # section governs this file, or Group I's entries answer for Group II's listings.
    head = re.compile(r"^## Group %d — open\b" % ctx.group, re.M).search(text)
    if not head:
        open_section = ""
    else:
        rest = text[head.end():]
        nxt = re.compile(r"^## ", re.M).search(rest)
        open_section = rest[:nxt.start()] if nxt else rest
    flagged, out = [], []
    for entry in ctx.data.get("morphology_entries") or []:
        if not isinstance(entry, dict) or not entry.get("awaiting_layer1"):
            continue
        code = str(entry.get("morphology_code"))
        flagged.append(code)
        aw = entry["awaiting_layer1"]
        if not isinstance(aw, dict) or not aw.get("reason"):
            out.append((FAIL, "entry %s: awaiting_layer1 must be an object carrying a "
                              "`reason` saying what Layer 1 is missing" % code))
        if entry.get("redcap_option_verified") is not False:
            out.append((FAIL, "entry %s: awaiting_layer1 is set but redcap_option_verified "
                              "is not False — the two cannot both be true" % code))
        if code not in open_section:
            out.append((FAIL, "entry %s carries awaiting_layer1 but is not listed under "
                              "'## Group %d — open' in docs/codes-awaiting-redcap.md "
                              "(ruling 3)" % (code, ctx.group)))
    for m in re.finditer(r"^### (\d{4})/", open_section, re.M):
        code = m.group(1)
        if code in ctx.codes and code not in flagged:
            out.append((FAIL, "docs/codes-awaiting-redcap.md still lists %s as open, but the "
                              "entry no longer carries awaiting_layer1 — close the item"
                        % code))
    if not out:
        out.append((OK, "%d code(s) awaiting a REDCap option are declared and listed: %s"
                    % (len(flagged), ", ".join(sorted(flagged)) or "none")))
    return out


def check_no_clinical_alerts(ctx: DTContext):
    """Ruling 9 — warnings live in docs/clinical-warnings.md, not in the tool."""
    live = []
    for holder, where in walk_dicts(ctx.data):
        value = holder.get("clinical_alert")
        if value:
            live.append(where or "(root)")
    if live:
        return [(FAIL, "%d clinical_alert value(s) still carry text (%s%s). Ruling 9: lift "
                       "them into docs/clinical-warnings.md — this is a coding tool"
                 % (len(live), ", ".join(live[:3]), " …" if len(live) > 3 else ""))]
    return [(OK, "no clinical_alert carries text; the warnings are in "
                 "docs/clinical-warnings.md (ruling 9)")]


def check_flow_charts(ctx: DTContext):
    """Ruling 13 — every checklist is a flow chart and every rule in it can fire.

    Two claims, proved rather than asserted. The order the engine walks has to be able to
    ask every marker any rule turns on, or the rule needing the missing marker is
    unreachable at runtime while looking fine in the file. And every rule has to have a
    witness: an answer vector under which it, and no earlier rule, matches.
    """
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import induce_flow
    except Exception as exc:                       # pragma: no cover
        return [(FAIL, "could not load build/induce_flow.py to verify the flow charts: %s"
                 % exc)]
    out, n_nodes, n_rules = [], 0, 0
    for tree in ctx.data.get("decision_trees") or []:
        for node in tree.get("nodes") or []:
            if not isinstance(node, dict) or node.get("node_type") != "ihc_checklist":
                continue
            n_nodes += 1
            n_rules += len(node.get("resolution_logic") or [])
            bs = node.get("branch_sequence")
            if not isinstance(bs, dict) or "order" not in bs:
                out.append((FAIL, "node %s is an ihc_checklist with no branch_sequence — "
                                  "run build/induce_flow.py (ruling 13)" % node["node_id"]))
                continue
            if not bs["order"]:
                # Legitimate: a node whose rules branch only on captured state. The state
                # selectors ARE its flow chart; there is no marker to ask.
                reads_markers = any((r.get("positive") or r.get("negative"))
                                    for r in node.get("resolution_logic") or [])
                if reads_markers:
                    out.append((FAIL, "node %s has an empty branch_sequence.order but its "
                                      "rules read markers — rerun build/induce_flow.py"
                                % node["node_id"]))
                    continue
            if bs.get("rule_count") != len(node.get("resolution_logic") or []):
                out.append((FAIL, "node %s: branch_sequence.rule_count is %s but the node "
                                  "holds %d rules — the flow chart is stale, rerun "
                                  "build/induce_flow.py"
                            % (node["node_id"], bs.get("rule_count"),
                               len(node.get("resolution_logic") or []))))
            out += [(FAIL, m) for m in induce_flow.check_order_covers(node, bs["order"])]
            out += [(FAIL, m) for m in induce_flow.check_node(node)]
    if not out:
        out.append((OK, "%d flow chart(s) ask every marker their rules read, and all %d "
                        "rule(s) have a witness that fires them (ruling 13)"
                    % (n_nodes, n_rules)))
    return out



# ----------------------------------------------------------------------------------
# Fix dated 18 Sep 2026 (branch group-04-neuroblastoma) — an ihc_checklist has to
# render a control the clerk can actually answer.
#
# app.js's nodeControl() (~line 615) routes every `ihc_checklist` node to markerFlow()
# whenever the node carries a `branch_sequence`, and to markerGrid() only when it does
# not. markerFlow() (~line 913) asks one marker at a time strictly from
# `branch_sequence.order` (via nextMarker(), ~line 846) — it does not read
# `marker_groups[]` at all. dispatchNode() (~line 613) separately prepends
# stateSelectors(), which renders one set of buttons per block in `test_result_states`
# (stateBlocks(), ~line 643) — the only OTHER control an ihc_checklist can show.
#
# check_flow_charts() (above) already tolerates an empty `branch_sequence.order` as
# "legitimate" whenever the node's rules read no markers, on the theory that
# `test_result_states` state selectors ARE the flow chart in that case. It never
# actually checks that a `test_result_states` block exists — which is exactly how
# hn_ihc_checklist and sn_ihc_checklist (Group 4) shipped with neither: an empty
# `order` and no `test_result_states`, so nothing rendered but the question, the hint
# and a bare Continue button. Both are fixed on this branch by giving them a
# `test_result_states` array, one block per status variable their `resolution_logic`
# keys off, matching op_ihc_cd99 (Group 4 build contract §3.4).
# ----------------------------------------------------------------------------------

# Group 3 carries the identical, still-open defect on two of its own nodes. Group 3 is
# already merged to main and this branch may not touch its data (see docs/TODO.md for
# the fix). Named, dated exemption, downgraded to WARN — NOT a scope carve-out for
# Group 3 generally, only for these two node IDs:
GROUP3_UNANSWERABLE_IHC_EXEMPTION = {
    "pf_mb_molecular_gate",   # Group 3, molecular_freetext gate — see docs/TODO.md
    "mn_grade_assembly",      # Group 3, meningioma grade assembly — see docs/TODO.md
}


def check_ihc_checklist_renders_a_control(ctx: DTContext):
    """
    An `ihc_checklist` node must render at least one input control.

    It needs a non-empty `branch_sequence.order` (markerFlow() asks from it), OR a
    non-empty `test_result_states` (stateSelectors() renders from it) — contract §3.4.
    A node with NEITHER presents a question, a hint and a Continue button, with
    nothing on screen the clerk can tap to answer it: exactly the defect found by
    driving hn_ihc_checklist and sn_ihc_checklist in a browser (Group 4, 18 Sep 2026).

    `marker_groups[]` alone can never satisfy this. It documents the panel for
    `check_marker_tokens_declared`/`check_marker_names_verbatim` and for
    `induce_flow.py`'s own ordering of markers actually named in
    `resolution_logic[].positive`/`.negative` — but app.js's markerFlow() (the renderer
    an ihc_checklist with a `branch_sequence` is routed to) never reads
    `marker_groups[]`. A node whose rules key off captured state variables instead of
    marker tokens (`when` clauses, not `positive`/`negative`) induces an empty `order`
    by construction, and looks identical to a rendering node right up until it is
    driven in a browser.

    Group 3 has two more instances of this exact defect — `pf_mb_molecular_gate` and
    `mn_grade_assembly` — merged to main already, out of scope for this branch to fix.
    They are named explicitly, above, and downgraded to WARN rather than excluded from
    the check or scoped around by group number. If either node is ever repaired,
    deleting it from `GROUP3_UNANSWERABLE_IHC_EXEMPTION` is required — the second half
    of this check FAILS on its own if a named node no longer has the defect, so the
    exemption cannot silently go stale.
    """
    out = []
    checked = 0
    rendered = 0
    for node_id, node in sorted(ctx.nodes.items()):
        if node.get("node_type") != "ihc_checklist":
            continue
        checked += 1
        bs = node.get("branch_sequence")
        order = bs.get("order") if isinstance(bs, dict) else None
        has_control = bool(order) or bool(node.get("test_result_states"))
        if has_control:
            rendered += 1
            continue
        msg = ("node %s is an ihc_checklist with an empty branch_sequence.order and no "
               "test_result_states — app.js's markerFlow() asks only from "
               "branch_sequence.order and never reads marker_groups[], so this node "
               "renders a question, a hint and a Continue button with nothing to "
               "answer (contract §3.4; app.js nodeControl()/markerFlow())" % node_id)
        if ctx.group == GROUP3 and node_id in GROUP3_UNANSWERABLE_IHC_EXEMPTION:
            out.append((WARN, msg + " — known Group 3 defect (pf_mb_molecular_gate, "
                               "mn_grade_assembly), tracked in docs/TODO.md, out of "
                               "scope for this branch"))
        else:
            out.append((FAIL, msg))

    # The exemption's own collapse test. A named node that no longer has the defect
    # means the exemption is describing a file that no longer exists — that has to be
    # loud, not a quietly-passing WARN nobody notices was never earned.
    if ctx.group == GROUP3:
        for node_id in sorted(GROUP3_UNANSWERABLE_IHC_EXEMPTION):
            node = ctx.nodes.get(node_id)
            if node is None:
                continue
            bs = node.get("branch_sequence")
            order = bs.get("order") if isinstance(bs, dict) else None
            if bool(order) or bool(node.get("test_result_states")):
                out.append((FAIL, "GROUP3_UNANSWERABLE_IHC_EXEMPTION names %s, which now "
                                  "renders a control (branch_sequence.order or "
                                  "test_result_states is no longer empty) — the Group 3 "
                                  "defect this exemption covers for %s is fixed. DELETE "
                                  "%s from GROUP3_UNANSWERABLE_IHC_EXEMPTION in "
                                  "build/build_database.py"
                            % (node_id, node_id, node_id)))

    if [f for f in out if f[0] == FAIL]:
        return out
    # Every no-control node still standing at this point is a WARN (a FAIL would have
    # returned above), so `checked - rendered` is exactly the exempted count. The OK
    # line must never claim more nodes render a control than actually do — a summary
    # that contradicts the WARN(s) printed immediately above it is the exact failure
    # this check exists to catch, and printing one anyway would be self-defeating.
    exempted = checked - rendered
    if not checked:
        out.append((NOTE, "no ihc_checklist node in this file — nothing to check"))
    elif exempted:
        out.append((OK, "%d of %d ihc_checklist node(s) render at least one input control "
                        "— a non-empty branch_sequence.order or test_result_states "
                        "(contract §3.4); %d exempted (see WARN above)"
                    % (rendered, checked, exempted)))
    else:
        out.append((OK, "%d ihc_checklist node(s) all render at least one input control "
                        "— a non-empty branch_sequence.order or test_result_states "
                        "(contract §3.4)" % checked))
    return out


def check_marker_names_verbatim(ctx: DTContext):
    """Ruling 10 — a gene or fusion name renders as written.

    `CD30:strong` is a marker plus an intensity. `NPM1::ALK` is a marker whose NAME
    contains colons. Splitting on the first colon turned the second into the first and
    silently broke two rules. The engine now splits only on a trailing `:strong`/`:weak`,
    so what has to be checked is that no marker NAME ends that way by accident.
    """
    bad = []
    for tree in ctx.data.get("decision_trees") or []:
        for node in tree.get("nodes") or []:
            if not isinstance(node, dict):
                continue
            for grp in node.get("marker_groups") or []:
                for marker in grp.get("markers") or []:
                    if re.search(r":(strong|weak)$", str(marker)):
                        bad.append("%s: %s" % (node.get("node_id"), marker))
    if bad:
        return [(FAIL, "%d marker name(s) end in an intensity suffix, so the engine will "
                       "read part of the name as a grade: %s"
                 % (len(bad), "; ".join(bad)))]
    return [(OK, "no marker name collides with the :strong/:weak intensity suffix, so "
                 "fusion names such as NPM1::ALK render verbatim (ruling 10)")]


def check_declared_states_consumed(ctx: DTContext):
    """Ruling 11 — a state the clerk can choose has to lead somewhere.

    `not_assessable` exists so an unreadable test is answerable. If nothing reads it the
    answer goes nowhere and the case falls to a NOS fallback with nothing on screen to say
    a state was ignored, which is the failure this construct was added to prevent.

    Two things stop this being noise. A state is captured at one node and often read
    several nodes downstream, so the search is file-wide, not node-local. And a node
    carrying a catch-all branch — a rule or option with no `when` — has somewhere for
    every remaining state to go by construction.
    """
    consumed = set()
    for holder, _ in walk_dicts(ctx.data):
        when = holder.get("when")
        if not isinstance(when, dict):
            continue
        for key, value in when.items():
            for v in (value if isinstance(value, list) else [value]):
                consumed.add((key, str(v)))
    out, checked = [], 0
    for tree in ctx.data.get("decision_trees") or []:
        for node in tree.get("nodes") or []:
            if not isinstance(node, dict):
                continue
            blocks = node.get("test_result_states")
            if not blocks:
                continue
            blocks = blocks if isinstance(blocks, list) else [blocks]
            branches = list(node.get("resolution_logic") or []) + list(node.get("options") or [])
            catch_all = any(isinstance(b, dict) and not b.get("when") for b in branches)
            for block in blocks:
                var = block.get("variable")
                for st in block.get("states") or []:
                    checked += 1
                    if (var, str(st)) in consumed or catch_all:
                        continue
                    out.append((FAIL, "node %s offers %s = %s and nothing in this file reads "
                                      "it, and the node has no catch-all branch — the answer "
                                      "goes nowhere (ruling 11)"
                                % (node["node_id"], var, st)))
    if not out:
        out.append((OK, "%d declared test-result state(s) either steer a branch or fall to a "
                        "catch-all; none is a dead end (ruling 11)" % checked))
    return out


# --------------------------------------------------------------------------------------
# B4b. The override affordance — offered on exactly the terminals that emitted a code
# --------------------------------------------------------------------------------------

# The flag names a gate must NOT be keyed off. Three of them are the `state.result`
# discriminators the no-code terminal builders set (refer() -> referral, exclude() ->
# excluded, excludeBehaviour() -> behaviourExcluded); three are the branch-level JSON
# fields advance() dispatches on. Either kind is a list somebody has to remember to
# extend, and the first terminal kind left off it silently gets the affordance back —
# which is how this defect would return. The gate is keyed off the RESOLVED OUTCOME
# instead: `state.result.code`, set in exactly one place.
OVERRIDE_GATE_FLAG_TOKENS = ("referral", "excluded", "behaviourExcluded",
                             "refer_group", "non_reportable", "behaviour_exclusion",
                             "icdoCode")

_APP_JS_CACHE: dict = {}


def _app_js_source(repo: Path):
    """Read app.js once per build. Returns (text, findings)."""
    key = str(repo)
    if key not in _APP_JS_CACHE:
        path = repo / "app.js"
        try:
            _APP_JS_CACHE[key] = (path.read_text(encoding="utf-8"), [])
        except OSError as exc:
            _APP_JS_CACHE[key] = (None, [(FAIL, "cannot read app.js (%s) — the engine "
                                                "half of this check cannot run" % exc)])
    return _APP_JS_CACHE[key]


def _terminal_outcomes(ctx: DTContext):
    """
    Every terminal this file declares, classified by the OUTCOME app.js resolves it to
    — not by which key happens to be present, and not by any flag naming the kind.

    advance() dispatches in a fixed order: morphology_code, refer_group,
    non_reportable, behaviour_exclusion, next_node. Only the first of those runs
    finish(), and finish() is the only function that sets `state.result.code`. So the
    classification here is exactly the question the renderer asks at runtime: did this
    terminal put a code on the resolved outcome, or not?

    Returns [(label, kind)] with kind in {"code", "referral", "non_reportable",
    "behaviour_exclusion"}. The three code-emitting shapes that do NOT carry a literal
    `morphology_code` key are included by name, because each still reaches finish():

      * `nos_fallback` — handleOption('escape-nos') calls
        advance({morphology_code: f.code, …}), so the escape hatch is a coded terminal;
      * `entity_boundary.inside_code` / `.outside_code` — boundary() builds a target
        carrying whichever side won, and both sides are codes;

    and the block objects that merely DESCRIBE a terminal (`behaviour_exclusion`
    itself, `provisional_pending`) carry no destination of their own, so they are
    classified through their owning branch, never twice.
    """
    out = []
    for node_id, node in sorted(ctx.nodes.items()):
        for holder, where in walk_dicts(node):
            label = "%s (%s)" % (node_id, where or "(node level)")
            if is_nos_fallback_object(holder, where):
                out.append((label, "code"))
                continue
            if is_behaviour_exclusion_object(holder, where):
                continue                      # classified through its owning branch
            if as_code(holder.get("inside_code")) and as_code(holder.get("outside_code")):
                out.append((label + " inside", "code"))
                out.append((label + " outside", "code"))
                continue
            if as_code(holder.get("morphology_code")):
                out.append((label, "code"))
            elif is_refer_branch(holder):
                out.append((label, "referral"))
            elif is_non_reportable(holder):
                out.append((label, "non_reportable"))
            elif isinstance(holder.get("behaviour_exclusion"), dict):
                out.append((label, "behaviour_exclusion"))
    return out


def _name_some(labels, limit=4):
    labels = sorted(labels)
    head = "; ".join(labels[:limit])
    return head + ("; and %d more" % (len(labels) - limit) if len(labels) > limit else "")


def check_override_affordance(ctx: DTContext, repo: Path):
    """
    "Override this code" must be offered on exactly the terminals that emitted one.

    THE DEFECT THIS CHECK EXISTS FOR (observed in a browser, 18 Sep 2026). outActions()
    rendered `Start new case | Override this code` unconditionally, on every terminal.
    Two of this tool's four terminal kinds emit no morphology code at all — a
    cross-group referral ("CODE HERE: None. Emitting a code from this group would put
    the case in the wrong ICCC-3 group") and a Group 4 behaviour exclusion
    ("MORPHOLOGY: No code emitted here") — and a third, the non-reportable exclusion,
    emits none either. On all three the button offered to override a code that does not
    exist, and the handler validated the typed code with entryFor(), which accepts only
    codes from THIS group. So the one thing a clerk could do with that button, on a
    screen that had just told them the case belongs elsewhere, was force it into this
    group: driven in a browser, the Group XI referral out of hn_ihc_checklist became
    9490 Ganglioneuroblastoma, ICCC-3 IVa. That is the exact error the terminal exists
    to prevent.

    KEYED OFF THE RESOLVED OUTCOME, NOT A FLAG. `state.result.code` is set in exactly
    one place — finish(), from the branch's own morphology_code, after entryFor() has
    proved the code is real. refer(), exclude() and excludeBehaviour() never set it
    (excludeBehaviour deliberately uses a different key, `icdoCode`: the code a benign
    tumour sits at is not a code this group emitted). So `code` is the one value that
    separates the terminals that emitted a code from those that emitted none, it is the
    same value the headline renders and the same value an override would replace, and a
    fifth terminal kind added in a later group is covered without touching anything —
    if it does not run through finish(), it carries no code.

    Both halves have to hold, and the check is two-sided:

      ENGINE — app.js must define `resultCarriesCode(r)` as a test on the resolved
      outcome's `code` (naming any terminal-kind flag instead is a FAIL, however
      correct that flag list happens to be today); `data-act="override"` must occur
      exactly ONCE in the whole file; that occurrence must sit inside outActions()
      under `if (resultCarriesCode(state.result))` — present and POSITIVE, so a gate
      that suppressed the button on coded terminals fails just as loudly as one that
      offered it on code-less ones; and handleOption's `case 'override'` must refuse on
      a code-less outcome BEFORE it prompts, so the behaviour is right regardless of
      what rendered.

      DATA — every terminal in this file is classified by the outcome advance() sends
      it to, so each FAIL names the actual terminals in this group that would gain or
      lose the button, and the OK line reports both tallies rather than asserting the
      rule in the abstract.
    """
    out = []
    src, read_findings = _app_js_source(repo)
    out += list(read_findings)

    terminals = _terminal_outcomes(ctx)
    coded = [t for t, k in terminals if k == "code"]
    referral = [t for t, k in terminals if k == "referral"]
    nonrep = [t for t, k in terminals if k == "non_reportable"]
    behex = [t for t, k in terminals if k == "behaviour_exclusion"]
    codeless = referral + nonrep + behex

    if src is None:
        return out

    # -- ENGINE half -------------------------------------------------------------------
    gate_ok = True

    m = re.search(r"\nfunction resultCarriesCode\(\s*(\w+)\s*\)\s*\{(.*?)\n\}", src, re.S)
    if not m:
        gate_ok = False
        out.append((FAIL, "app.js declares no resultCarriesCode() — the override "
                          "affordance has no gate keyed off the resolved outcome, so "
                          "every code-less terminal in %s offers \"Override this code\" "
                          "and the handler will emit a code from this group: %s"
                    % (ctx.name, _name_some(codeless) or "(none in this file)")))
    else:
        arg, body = m.group(1), m.group(2)
        flags = [t for t in OVERRIDE_GATE_FLAG_TOKENS if re.search(r"\b%s\b" % t, body)]
        if flags:
            gate_ok = False
            out.append((FAIL, "resultCarriesCode() is keyed off the terminal-kind flag(s) "
                              "%s instead of the resolved outcome's own code — that is a "
                              "list someone must remember to extend, and the first "
                              "terminal kind left off it gets \"Override this code\" back. "
                              "Test %s.code, which only finish() ever sets"
                        % (", ".join(flags), arg)))
        if not re.search(r"return\s+!!\(\s*%s\s*&&\s*%s\.code\s*\)\s*;" % (arg, arg), body):
            gate_ok = False
            out.append((FAIL, "resultCarriesCode() does not read the resolved outcome's "
                              "code — its body must be `return !!(%s && %s.code);`, the "
                              "value finish() sets and refer()/exclude()/"
                              "excludeBehaviour() never do. Body is: %s"
                        % (arg, arg, " ".join(body.split()))))

    occurrences = src.count('data-act="override"')
    if occurrences != 1:
        gate_ok = False
        out.append((FAIL, "app.js renders data-act=\"override\" in %d place(s); it must be "
                          "rendered in exactly one, inside outActions(), so there is a "
                          "single gate to hold. %d coded terminal(s) in %s depend on that "
                          "button and %d code-less terminal(s) depend on its absence"
                    % (occurrences, len(coded), ctx.name, len(codeless))))

    ma = re.search(r"\nfunction outActions\(\)\s*\{(.*?)\n\}", src, re.S)
    if not ma:
        gate_ok = False
        out.append((FAIL, "app.js declares no outActions() — the terminal action bar "
                          "cannot be checked"))
    else:
        body = ma.group(1)
        guarded = re.search(r"if\s*\(\s*resultCarriesCode\(\s*state\.result\s*\)\s*\)\s*\{"
                            r"(?:(?!\}).)*?data-act=\"override\"", body, re.S)
        if 'data-act="override"' not in body:
            gate_ok = False
            out.append((FAIL, "outActions() renders no override button at all, so the %d "
                              "coded terminal(s) in %s LOSE \"Override this code\" — the "
                              "affordance is removed from terminals that did emit a code, "
                              "not just from the ones that did not: %s"
                        % (len(coded), ctx.name, _name_some(coded) or "(none in this file)")))
        elif re.search(r"if\s*\(\s*!\s*resultCarriesCode\(\s*state\.result\s*\)\s*\)\s*\{"
                       r"(?:(?!\}).)*?data-act=\"override\"", body, re.S):
            gate_ok = False
            out.append((FAIL, "outActions() guards \"Override this code\" on "
                              "`if (!resultCarriesCode(state.result))` — the gate is "
                              "INVERTED. In %s that offers it on all %d code-less "
                              "terminal(s), where the handler can only emit a code from "
                              "THIS group, and removes it from all %d coded terminal(s), "
                              "which are the only ones that have a code to override"
                        % (ctx.name, len(codeless), len(coded))))
        elif not guarded:
            gate_ok = False
            out.append((FAIL, "outActions() renders \"Override this code\" without "
                              "`if (resultCarriesCode(state.result))` around it, so it is "
                              "offered on terminals that emitted no code. In %s that is %d "
                              "terminal(s) — %d cross-group referral, %d non-reportable, %d "
                              "behaviour-exclusion — where the handler can only emit a code "
                              "from THIS group: %s"
                        % (ctx.name, len(codeless), len(referral), len(nonrep), len(behex),
                           _name_some(codeless) or "(none in this file)")))

    mh = re.search(r"\n    case 'override':(.*?)(?=\n    case ')", src, re.S)
    if not mh:
        gate_ok = False
        out.append((FAIL, "app.js has no `case 'override':` in handleOption() — the "
                          "handler half of this gate cannot be checked"))
    else:
        hbody = mh.group(1)
        guard = re.search(r"if\s*\(\s*!\s*resultCarriesCode\(\s*state\.result\s*\)\s*\)",
                          hbody)
        prompt = re.search(r"window\.prompt\(", hbody)
        if not guard:
            gate_ok = False
            out.append((FAIL, "handleOption()'s `case 'override'` does not refuse on a "
                              "code-less outcome — it must return early on "
                              "`if (!resultCarriesCode(state.result))`, so a renderer "
                              "regression or a hand-dispatched action cannot turn one of "
                              "%s's %d code-less terminal(s) into a code from this group: %s"
                        % (ctx.name, len(codeless),
                           _name_some(codeless) or "(none in this file)")))
        elif prompt and guard.start() > prompt.start():
            gate_ok = False
            out.append((FAIL, "handleOption()'s `case 'override'` tests "
                              "resultCarriesCode() only AFTER window.prompt() — the clerk "
                              "is asked for a code on a terminal that emits none before "
                              "the refusal. Move the guard above the prompt"))
        elif guard and not re.search(r"return\s*;", hbody[guard.end():
                                                          (prompt.start() if prompt
                                                           else len(hbody))]):
            gate_ok = False
            out.append((FAIL, "handleOption()'s `case 'override'` tests "
                              "resultCarriesCode() but does not return before proceeding "
                              "— the refusal has no effect"))

    if not gate_ok:
        return out

    if not terminals:
        out.append((NOTE, "no terminal declared in this file — nothing to check"))
        return out
    out.append((OK, "\"Override this code\" is offered on exactly the terminals that "
                    "emitted one: %d coded terminal(s) keep it, %d code-less terminal(s) "
                    "suppress it (%d cross-group referral, %d non-reportable, %d "
                    "behaviour-exclusion). app.js gates both outActions() and "
                    "handleOption('override') on resultCarriesCode(state.result), and "
                    "state.result.code is set only by finish()"
                % (len(coded), len(codeless), len(referral), len(nonrep), len(behex))))
    return out


# --------------------------------------------------------------------------------------
# B5. Cross-layer checks
# --------------------------------------------------------------------------------------

def check_routing_narrows(repo: Path, contexts: dict):
    """The presentation stage must NARROW to a family, not ask for one.

    Three facts do the narrowing — the presentation's advisory list, the
    discriminator's `narrows` map, and the topography's own `candidate_groups`.
    Each has a way of failing silently that this checks for:

      * `candidate_groups` written as the string "all" rather than a list. The
        engine read it as an empty list and two of the seven presentations could
        not be used at all.
      * a crosswalk row naming a code that has no entry in topography_lookup, so
        picking that region records a code nothing knows anything about.
      * a topography entry with no candidate_groups, which narrows to nothing and
        dead-ends the case.
      * a discriminator whose answers drop every candidate, or drop nothing.
    """
    out = []
    rp = repo / "data" / "shared" / "presentation_router.json"
    tp = repo / "data" / "shared" / "topography_codes.json"
    router, f1 = load_json(rp)
    topo, f2 = load_json(tp)
    out += list(f1) + list(f2)
    if router is None or topo is None:
        return out
    lookup = topo.get("topography_lookup") or {}
    cross = topo.get("coarse_organ_crosswalk") or []

    for a in router.get("archetypes") or []:
        cg = a.get("candidate_groups")
        who = a.get("archetype_id") or a.get("label")
        if not isinstance(cg, list) or not cg:
            out.append((FAIL, "archetype %s: candidate_groups must be a non-empty list of "
                              "group numbers, not %r — the engine reads anything else as no "
                              "candidates and the presentation becomes unusable" % (who, cg)))
            continue
        bad = [g for g in cg if not (isinstance(g, int) and 1 <= g <= 12)]
        if bad:
            out.append((FAIL, "archetype %s: candidate_groups holds %r, which is not a group "
                              "number 1-12" % (who, bad)))

    for row in cross:
        if not row.get("label"):
            out.append((FAIL, "crosswalk row %s has no `label` — the engine falls back to the "
                              "key with underscores stripped, and the clerk reads "
                              "\"gonad sacrococcygeal midline\"" % row.get("organ")))
        for code in row.get("codes") or []:
            if code not in lookup:
                out.append((FAIL, "crosswalk row %s offers %s, which has no topography_lookup "
                                  "entry — picking that region records a code the engine knows "
                                  "nothing about" % (row.get("organ"), code)))

    for code, entry in sorted(lookup.items()):
        cg = entry.get("candidate_groups")
        if cg == "route_by_morphology":
            continue
        if not isinstance(cg, list) or not cg:
            out.append((FAIL, "topography %s: candidate_groups is %r — a site that narrows to "
                              "nothing dead-ends the case" % (code, cg)))
            continue
        bad = [g for g in cg if not (isinstance(g, int) and 1 <= g <= 12)]
        if bad:
            out.append((FAIL, "topography %s: candidate_groups holds %r" % (code, bad)))

    for key, d in (router.get("discriminators") or {}).items():
        narrows = d.get("narrows")
        if not narrows:
            out.append((NOTE, "discriminator %s declares no `narrows` map, so answering it "
                              "cannot reduce the candidate families — it is captured and "
                              "nothing more" % key))
            continue
        if not d.get("question") or not d.get("hint"):
            out.append((FAIL, "discriminator %s needs a clerk-facing `question` and `hint`; "
                              "`authoring_note` explains the fork to whoever maintains the "
                              "router and must not be what the abstractor reads" % key))
        for opt in d.get("options") or []:
            if isinstance(opt, dict) and not opt.get("label"):
                out.append((FAIL, "discriminator %s: option %r has no clerk-facing label"
                            % (key, opt.get("value"))))
            name = opt if isinstance(opt, str) else opt.get("value")
            if str(name) not in narrows:
                out.append((FAIL, "discriminator %s: option %r has no entry in `narrows`, so "
                                  "that answer narrows nothing" % (key, name)))
        for answer, rule in narrows.items():
            if not isinstance(rule, dict) or not isinstance(rule.get("drop"), list):
                out.append((FAIL, "discriminator %s, answer %r: `narrows` entry needs a "
                                  "`drop` list" % (key, answer)))

    n_soft = sum(1 for c in lookup if c[:3] in ("C47", "C48", "C49"))
    if not out:
        out.append((OK, "routing narrows: %d archetype(s), %d topography code(s) (%d soft "
                        "tissue), %d discriminator(s) — every candidate list is a non-empty "
                        "list of real groups and every crosswalk code resolves"
                    % (len(router.get("archetypes") or []), len(lookup), n_soft,
                       len(router.get("discriminators") or {}))))
    return out


def check_presentation_router(repo: Path, contexts: dict):
    """
    Router integrity (Architecture §8).

    Every handoff.entry_node resolves to a node_id in that group's dt.json and that node
    is a document_inventory; every handoff.group and site_to_group value is 1-12.
    """
    path = repo / "data" / "shared" / "presentation_router.json"
    data, findings = load_json(path)
    out = list(findings)
    if data is None:
        return out

    def valid_group(value):
        try:
            n = int(value)
        except (TypeError, ValueError):
            return False
        return 1 <= n <= 12

    def group_num(value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    group_path_re = re.compile(r"(?:^|\.)groups\.(\d+)(?:\.|\[|$)")

    # Handoff targets. Architecture §4C sketches a `handoff` object; the authored router
    # expresses the same fact as groups["N"].trees[].entry_node and as tree-selection
    # options. Accept every shape — what matters is that each entry_node resolves to a
    # document_inventory gate in that group's dt.json.
    n_handoffs = 0
    for holder, where in walk_dicts(data):
        loc = where or "(root)"
        handoff = holder.get("handoff")
        if isinstance(handoff, dict):
            holder, loc = handoff, "%s.handoff" % loc
        entry = holder.get("entry_node")
        if not isinstance(entry, str) or not entry:
            continue
        n_handoffs += 1
        group = holder.get("group")
        if group is None:
            m = group_path_re.search(loc)
            group = m.group(1) if m else None
        if group is None:
            out.append((WARN, "presentation_router.json %s: entry_node %r but no group "
                              "could be determined — not resolved" % (loc, entry)))
            continue
        if not valid_group(group):
            out.append((FAIL, "presentation_router.json %s: group %r is not 1-12"
                        % (loc, group)))
            continue
        gnum = group_num(group)
        ctx = contexts.get(gnum)
        if ctx is None:
            out.append((NOTE, "presentation_router.json %s -> group %d: that group's "
                              "dt.json is not present, entry_node %r not resolved"
                        % (loc, gnum, entry)))
            continue
        node = ctx.nodes.get(entry)
        if node is None and not ctx.nodes:
            out.append((NOTE, "presentation_router.json %s: entry_node %r — group %d has no "
                              "decision nodes authored yet, so it cannot be resolved"
                        % (loc, entry, gnum)))
        elif node is None:
            out.append((FAIL, "presentation_router.json %s: entry_node %r does not resolve "
                              "in %s" % (loc, entry, ctx.name)))
        elif node.get("node_type") != "document_inventory":
            out.append((FAIL, "presentation_router.json %s: entry_node %r is a %r; the "
                              "router must hand off to a document_inventory gate "
                              "(Architecture §8, DT master §3B)"
                        % (loc, entry, node.get("node_type"))))
        tid = holder.get("tree_id")
        if isinstance(tid, str) and tid:
            known = set(ctx.metadata_tree_ids) | {t["tree_id"] for t in ctx.trees}
            if known and tid not in known and ctx.nodes:
                out.append((FAIL, "presentation_router.json %s: tree_id %r is not declared "
                                  "in %s metadata.decision_trees" % (loc, tid, ctx.name)))

    groups_map = data.get("groups")
    if isinstance(groups_map, dict):
        for key in sorted(groups_map):
            if not valid_group(key):
                out.append((FAIL, "presentation_router.json groups[%r]: not a group number "
                                  "1-12" % key))

    s2g = data.get("site_to_group")
    n_sites = 0
    if isinstance(s2g, dict):
        for site, groups in sorted(s2g.items()):
            values = groups if isinstance(groups, list) else [groups]
            for g in values:
                n_sites += 1
                if not valid_group(g):
                    out.append((FAIL, "presentation_router.json site_to_group[%r]: %r is "
                                      "not a group number 1-12" % (site, g)))
    elif s2g is not None:
        out.append((FAIL, "presentation_router.json: 'site_to_group' must be an object"))

    for arche in data.get("archetypes") or []:
        if not isinstance(arche, dict):
            continue
        cg = arche.get("candidate_groups")
        if cg == "all" or cg is None:
            continue
        for g in cg if isinstance(cg, list) else [cg]:
            if not valid_group(g):
                out.append((FAIL, "presentation_router.json archetype %r: candidate_groups "
                                  "value %r is not 1-12"
                            % (arche.get("archetype_id"), g)))

    if not any(lvl == FAIL for lvl, _ in out):
        out.append((OK, "router integrity: %d entry_node handoff(s), %d site_to_group "
                        "value(s)" % (n_handoffs, n_sites)))
    return out


def check_router_branch_when_vocabulary(repo: Path, contexts: dict):
    """
    A dual-group branch's `when` may use ONLY the shapes app.js's branchMatches() reads.

    branchMatches() is eight lines and reads exactly two:

        if (when.topography_in) return arr(when.topography_in).indexOf(topo) !== -1;
        if (!when.captured_variable) return false;
        ... equals / operator+value on that captured variable

    Anything else returns false. Not an error, not a warning — false. The branch simply
    never matches, every case falls through to the rule's `default`, and nothing on
    screen says a branch was skipped.

    FOUR BRANCHES WERE IN EXACTLY THAT STATE, all writing `topography_equals` where the
    engine reads `topography_in` (found 22 Sep 2026, Group VI build):

        9380       at C72.3  ->  Group III IIIb   fell to  Group III IIId2
        8158,8290  at C75.1  ->  Group III IIIe1  fell to  GROUP XI
        8963       at C64.9  ->  Group VI VIa2    fell to  GROUP IX IXd3
        8000-8005  at C64.9  ->  Group VI VIc     fell to  GROUP XII

    Two of the four crossed an ICCC-3 group boundary. A pituitary tumour sited at the
    pituitary gland routed out of Group III; a rhabdoid tumour of the kidney could never
    reach Group VI at all, which is the group that owns the code.

    Why nothing caught it. check_presentation_router() proves every handoff resolves and
    every group number is 1-12; check_routing_narrows() proves every candidate list is a
    non-empty list of real groups and every crosswalk code resolves. Both ask whether the
    DESTINATIONS are real. Neither asks whether the CONDITION can ever be true — and a
    branch whose condition is unreadable has a perfectly valid destination it never
    reaches. The gap is the shape of the bug: valid JSON, valid groups, dead logic.

    Rule 8 discipline: this keys off the engine's source, not off anything in the data
    file. No flag exempts a branch. The vocabulary below is transcribed from
    branchMatches() and a change there must be made here in the same commit.
    """
    ALLOWED = {"topography_in", "captured_variable", "equals", "value", "operator"}
    path = repo / "data" / "shared" / "presentation_router.json"
    data, findings = load_json(path)
    out = list(findings)
    if data is None:
        return out
    rules = (data or {}).get("dual_group_rules") or {}
    if not isinstance(rules, dict):
        return out + [(FAIL, "dual_group_rules is not an object")]

    branches = 0
    for key, rule in sorted(rules.items()):
        if key.startswith("_") or not isinstance(rule, dict):
            continue
        for i, branch in enumerate(rule.get("branches") or []):
            if not isinstance(branch, dict):
                continue
            when = branch.get("when")
            if not isinstance(when, dict):
                out.append((FAIL, "dual_group_rule %r branch[%d] has no 'when' object; "
                                  "branchMatches() returns false for a missing `when`, so "
                                  "the branch is dead and every case falls to the rule's "
                                  "default" % (key, i)))
                continue
            branches += 1
            unknown = sorted(set(when) - ALLOWED)
            if unknown:
                dest = branch.get("result") or {}
                out.append((FAIL, "dual_group_rule %r branch[%d] uses %s in its `when`. "
                                  "app.js branchMatches() reads only %s, so this branch "
                                  "NEVER MATCHES: its destination (group %s, subgroup %s) "
                                  "is unreachable and every case falls to the rule's "
                                  "default (group %s). Valid JSON, valid destination, dead "
                                  "logic — the defect this check exists for"
                            % (key, i, ", ".join(repr(u) for u in unknown),
                               ", ".join(sorted(ALLOWED)),
                               dest.get("group"), dest.get("subgroup"),
                               (rule.get("default") or {}).get("group"))))
                continue
            if "captured_variable" in when:
                if "equals" not in when and not ("value" in when and "operator" in when):
                    out.append((FAIL, "dual_group_rule %r branch[%d] names captured_variable "
                                      "%r but gives neither `equals` nor `operator`+`value`. "
                                      "branchMatches() falls off its last line and returns "
                                      "false — the branch is dead"
                                % (key, i, when.get("captured_variable"))))
            elif "topography_in" not in when:
                out.append((FAIL, "dual_group_rule %r branch[%d] `when` has neither "
                                  "`topography_in` nor `captured_variable`; branchMatches() "
                                  "returns false and the branch is dead" % (key, i)))
            elif not isinstance(when.get("topography_in"), list) or not when["topography_in"]:
                out.append((FAIL, "dual_group_rule %r branch[%d] `topography_in` is not a "
                                  "non-empty list; indexOf() on it can never hit and the "
                                  "branch is dead" % (key, i)))

    if not [f for f in out if f[0] == FAIL]:
        out.append((OK, "router branch `when` vocabulary: all %d dual-group branch(es) use a "
                        "shape app.js branchMatches() actually reads, so none is dead"
                    % branches))
    return out


def check_router_cns_topography_completeness(repo: Path, contexts: dict):
    """
    A dual-group branch that names ANY CNS topography must name all 21 of them.

    Proposed by docs/TODO.md §12's own "To close" section and written here, on the Group VI
    branch, alongside the fix it guards.

    `topography_codes.json` enumerates 21 codes in C70.0-C72.9. Four router branches
    matched only the three NOS-level ones — C70.9, C71.9, C72.9 — because when they were
    written Group III was unbuilt and the finer subsites did not exist in the shared
    layer. Group III was authored on 16 September 2026 and they do. Until 22 September
    2026 three of those four branches were still short, and a case at a SPECIFIC CNS
    subsite (C71.6 cerebellum, say) missed the branch and fell to the rule's default,
    which for two of them is a group ICCC-2017 does not admit at a CNS site at all.

    This is a different failure from the one check_router_branch_when_vocabulary()
    catches, and both are needed. That one catches a branch that can NEVER match. This
    one catches a branch that matches at the NOS level and silently misses every specific
    subsite — which is worse to find, because it works in testing. A clerk who records
    "brain, NOS" is routed correctly and a clerk who records the cerebellum is not.

    THE TRIGGER IS THE NOS-LEVEL CODES, NOT ANY CNS CODE. A branch naming C70.9, C71.9 or
    C72.9 is saying "the CNS", and a branch saying that must name all of it. A branch
    naming only a SPECIFIC subsite is saying something narrower and is left alone — the
    `9380` rule names C72.3 alone because a glioma at the optic nerve is IIIb and a glioma
    anywhere else is IIId2, and demanding all 21 there would destroy the distinction the
    branch exists to draw. The first draft of this check triggered on any C70/C71/C72 code
    and failed `9380` for doing its job; this is the rule docs/TODO.md §12 actually
    proposed.

    Codes outside C70-C72 in the same list are untouched — `8000-8005` legitimately adds
    C75.1-C75.3, which match ICCC-2017 range 42's `700-729,751-753`.

    ONE NAMED EXEMPTION, and it collapses when fixed. `9473` is the third of the four
    stale branches and is the one docs/TODO.md §12 says not to repair here: extending its
    topography list would fix the CNS cases and leave the larger defect in place, because
    ICCC-2017 range 29 is the ONLY range carrying `9473`, it takes sites `000-809`, and it
    resolves to IIIc2 — so the rule's Group IX default has no basis at any topography, not
    merely at unenumerated CNS subsites. Whether `9473` is topography-dependent at all is a
    Group III/IX decision. It is downgraded to WARN by name, and if it is ever repaired
    this check FAILS on the stale exemption rather than letting it quietly outlive its
    reason.

    Keyed off topography_codes.json, not off a list written here, so enumerating a new
    CNS subsite in the shared layer makes this check demand it everywhere in the same
    build rather than in whichever build someone next remembers.
    """
    # docs/TODO.md §12 — repaired elsewhere, on its own evidence. Deleting this name once
    # the rule is fixed is required; the second clause below fails if it goes stale.
    CNS_COMPLETENESS_EXEMPTION = {"9473"}
    NOS_LEVEL = {"C70.9", "C71.9", "C72.9"}
    router_path = repo / "data" / "shared" / "presentation_router.json"
    topo_path = repo / "data" / "shared" / "topography_codes.json"
    data, findings = load_json(router_path)
    topo, topo_findings = load_json(topo_path)
    out = list(findings) + list(topo_findings)
    if data is None or topo is None:
        return out

    lookup = (topo or {}).get("topography_lookup") or {}
    cns = {c for c in lookup if str(c).startswith(("C70", "C71", "C72"))}
    if not cns:
        return out + [(WARN, "topography_codes.json enumerates no C70-C72 code; CNS "
                             "completeness cannot be checked")]

    rules = (data or {}).get("dual_group_rules") or {}
    checked = 0
    exempted = 0
    for key, rule in sorted(rules.items()):
        if key.startswith("_") or not isinstance(rule, dict):
            continue
        for i, branch in enumerate(rule.get("branches") or []):
            if not isinstance(branch, dict):
                continue
            listed = branch.get("when", {}).get("topography_in")
            if not isinstance(listed, list):
                continue
            named = {c for c in listed if str(c).startswith(("C70", "C71", "C72"))}
            if not named & NOS_LEVEL:
                continue
            missing = sorted(cns - named)
            exempt = key in CNS_COMPLETENESS_EXEMPTION
            if not (exempt and missing):
                checked += 1
            else:
                exempted += 1
            if not missing and exempt:
                out.append((FAIL, "dual_group_rule %r is named in "
                                  "CNS_COMPLETENESS_EXEMPTION but no longer has the defect "
                                  "— delete the name. An exemption that cannot collapse is "
                                  "a hole" % key))
            if missing:
                dest = branch.get("result") or {}
                out.append((WARN if exempt else FAIL,
                            ("EXEMPT (docs/TODO.md §12 — repaired on its own evidence, not "
                             "here): " if exempt else "")
                            + "dual_group_rule %r branch[%d] names %d of the %d CNS "
                                  "topography code(s) topography_codes.json enumerates, "
                                  "missing %s. A case at any of those subsites misses this "
                                  "branch and falls to the rule's default (group %s) "
                                  "instead of reaching group %s %s — and it works at the "
                                  "NOS level, so testing with 'brain, NOS' would not show "
                                  "it (docs/TODO.md §12)"
                            % (key, i, len(named), len(cns),
                               ", ".join(missing[:6]) + ("…" if len(missing) > 6 else ""),
                               (rule.get("default") or {}).get("group"),
                               dest.get("group"), dest.get("subgroup") or "")))

    if not checked and not exempted:
        return out
    if not [f for f in out if f[0] == FAIL]:
        out.append((OK, "CNS topography completeness: %d of %d branch(es) naming the CNS at "
                        "NOS level name all %d codes topography_codes.json enumerates%s"
                    % (checked, checked + exempted, len(cns),
                       "" if not exempted else
                       "; %d exempt and still short, reported above as WARN" % exempted)))
    return out


def check_redcap_banner_signal(ctx: DTContext, redcap_options: dict):
    """
    `awaiting_layer1` must mark exactly the entries Layer 1 has NO option for.

    app.js's output block renders two different warnings off one flag, and it has
    to, because two different things can be true of an entry carrying
    `redcap_option_verified: false`:

        awaiting_layer1 present  ->  "Not yet a REDCap option ... cannot be
                                      selected yet" — the tree has run ahead of
                                      the option list (ruling 3).
        awaiting_layer1 absent   ->  "The REDCap label for this code is out of
                                      date ... the case can be entered" — the row
                                      is there, its words are stale.

    Until 22 September 2026 the engine printed the FIRST message for both, so
    eleven codes with an option a clerk could select today said they could not:
    9898 (Group I), 9718 and 9725 (Group II), and Group VI's eight drifted
    strings. 8311 is the sharpest of them — its option exists and is labelled
    "Hypernephroid tumor", the obsolete 8311/1 term for a different lesion, so
    the clerk needs to be told the label is wrong, not that the row is missing.
    Sending a clerk away from a row that is there is the same class of defect as
    sending them to one that is not.

    THIS CHECK IS WHAT LETS THE ENGINE TRUST THE FLAG. It keys off the option
    file itself — Layer 1, never anything in the file being checked (rule 8) —
    and fails in both directions:

        awaiting_layer1 set   on a code Layer 1 DOES carry  -> the clerk is told
                              to go away from a usable row;
        awaiting_layer1 unset on a code Layer 1 does NOT carry -> the clerk is
                              told to match a label that is not there at all.

    Scoped to entries flagged `redcap_option_verified: false`, because that is
    the only branch app.js reads it on. Silent when a group's options cannot be
    parsed: a missing option file is already reported by parse_redcap_options()
    and guessing from its absence would invent a finding.
    """
    options = redcap_options.get(ctx.group)
    if not options:
        return []
    checked = 0
    out = []
    for entry in ctx.entries:
        if not isinstance(entry, dict):
            continue
        if entry.get("redcap_option_verified") is not False:
            continue
        code = as_code(entry.get("morphology_code"))
        if code is None:
            continue
        checked += 1
        has_option = code in options
        awaiting = bool(entry.get("awaiting_layer1"))
        if has_option and awaiting:
            out.append((FAIL, "entry %s carries awaiting_layer1, but Layer 1 DOES "
                              "offer an option for this code. app.js then tells the "
                              "clerk it 'has no option in the registry dropdown, so "
                              "it cannot be selected yet' and sends them away from a "
                              "row that is there. Drop awaiting_layer1; the label-drift "
                              "banner is the correct one" % code))
        elif not has_option and not awaiting:
            out.append((FAIL, "entry %s is flagged redcap_option_verified false with no "
                              "awaiting_layer1, but Layer 1 offers no option for this "
                              "code at all. app.js then tells the clerk the row exists "
                              "and to 'match on the four-digit code', and there is no "
                              "row to match. Add awaiting_layer1 with what it needs"
                        % code))
    if not checked:
        return []
    if not [f for f in out if f[0] == FAIL]:
        out.append((OK, "REDCap banner signal: all %d entry/entries flagged "
                        "redcap_option_verified false carry awaiting_layer1 exactly "
                        "when Layer 1 has no option for them, so both output banners "
                        "state something true" % checked))
    return out


def check_alias_cross_references(repo: Path, contexts: dict):
    """Alias -> decision-tree references (Architecture §8, Alias master §10A)."""
    out = []
    alias_dir = repo / "data" / "aliases"
    files = sorted(alias_dir.glob("aliases_group_*.json")) if alias_dir.exists() else []
    if not files:
        return [(NOTE, "no alias files present — alias cross-reference check skipped")]
    for path in files:
        gm = re.search(r"aliases_group_(\d+)\.json$", path.name)
        if not gm:
            continue
        group = int(gm.group(1))
        data, load_findings = load_json(path)
        out.extend(load_findings)
        if data is None:
            continue
        entries = data.get("aliases") if isinstance(data, dict) else data
        if not isinstance(entries, list):
            continue
        ctx = contexts.get(group)
        if ctx is None:
            out.append((NOTE, "%s: group_%02d_dt.json not present — cross-references not "
                              "resolved" % (path.name, group)))
            continue
        problems = 0
        tree_ids = set(ctx.metadata_tree_ids) | {t["tree_id"] for t in ctx.trees}
        for i, entry in enumerate(entries):
            if not isinstance(entry, dict):
                continue
            label = entry.get("alias", "index %d" % i)
            ten = entry.get("tree_entry_node")
            if isinstance(ten, str) and ten and ten not in ctx.nodes:
                out.append((FAIL, "%s: alias %r tree_entry_node %r does not resolve in %s"
                            % (path.name, label, ten, ctx.name)))
                problems += 1
            tid = entry.get("ihc_tree_id")
            if isinstance(tid, str) and tid:
                if tid.startswith("PENDING_"):
                    out.append((WARN, "%s: alias %r ihc_tree_id %r is still a PENDING_ "
                                      "placeholder" % (path.name, label, tid)))
                elif tid not in tree_ids:
                    out.append((FAIL, "%s: alias %r ihc_tree_id %r is not in "
                                      "metadata.decision_trees of %s"
                                % (path.name, label, tid, ctx.name)))
                    problems += 1
            for code in entry.get("maps_to_morphology_codes") or []:
                if as_code(code) not in ctx.codes:
                    out.append((FAIL, "%s: alias %r maps_to_morphology_codes %r is not in "
                                      "morphology_entries[] of %s"
                                % (path.name, label, code, ctx.name)))
                    problems += 1
        if problems == 0:
            out.append((OK, "%s: %d alias entr%s cross-resolve against %s"
                        % (path.name, len(entries), "y" if len(entries) == 1 else "ies",
                           ctx.name)))
    return out


# --------------------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------------------

def check_requirements(repo: Path, layer1: Path):
    """
    PREFLIGHT — everything this gate needs, checked before it checks anything else.

    Registrar's instruction, 23 September 2026: "if certain dependencies are lacking, user
    must be warned ... a verification layer, that checks for all necessary requirements
    for the tool to run before it loads."

    Two properties matter and both are deliberate.

    IT REPORTS EVERY MISSING REQUIREMENT AT ONCE, not the first one. A gate that dies on
    the first missing thing sends someone away to install it, come back, and be sent away
    again. Everything below is therefore evaluated even when an earlier item has already
    failed.

    IT NEVER SKIPS SOMETHING IT CANNOT CHECK. A requirement that cannot be verified is a
    FAIL, never a silent pass. That is the failure mode this whole layer exists against:
    the engine gate was a separate command for one day and the two defects it catches had
    already shipped, precisely because a check nobody runs looks exactly like a check that
    passed.

    Node.js is REQUIRED, by the registrar's decision of 23 September 2026. The engine gate
    is JavaScript because app.js is — testing the engine means running it — and it is the
    only thing in this repository that tests app.js at all. The dependency-free property
    that is genuinely load-bearing belongs to the TOOL (index.html, app.js, one stylesheet,
    no build step), and it is untouched: nothing here runs in the browser.
    """
    out = []
    ok = True

    def need(label, present, detail, how):
        nonlocal ok
        if present:
            out.append((OK, "requirement: %s — %s" % (label, detail)))
        else:
            ok = False
            out.append((FAIL, "MISSING REQUIREMENT: %s. %s  →  %s" % (label, detail, how)))

    need("Python 3.9 or newer", sys.version_info >= (3, 9),
         "found %d.%d.%d" % sys.version_info[:3],
         "install a newer python3; this gate uses syntax 3.8 does not parse")

    try:
        import sqlite3 as _sq
        need("sqlite3 module", True, "found, SQLite %s" % _sq.sqlite_version, "")
    except Exception as exc:
        need("sqlite3 module", False, "import failed: %s" % exc,
             "reinstall python3 with SQLite support")

    for label, path, how in [
        ("Layer 1 directory", layer1,
         "pass --layer1 PATH, or set ICD_LAYER1, or place it at <repo>/../../ICD coding"),
        ("REDCap option files", layer1 / "RedCap Options",
         "restore the 'RedCap Options' directory inside Layer 1"),
        ("icdo32.sqlite", layer1 / "ICD-O-3.2" / "icdo32.sqlite",
         "rebuild it with ICD coding/ICD-O-3.2/convert_icdo32.py"),
        ("ICCC-2017.sqlite", layer1.parent / "ICCC-2017.sqlite",
         "restore it from the registry share; the inventory generators join against it"),
    ]:
        need(label, path.exists(), str(path), how)

    # -- the engine gate, and the runtime it needs --------------------------------
    engine_check = repo / "build" / "check_engine_flow.mjs"
    need("build/check_engine_flow.mjs", engine_check.exists(), str(engine_check),
         "restore it; it is the only thing in this repository that tests app.js")

    node = shutil.which("node")
    if node:
        try:
            ver = subprocess.run([node, "--version"], capture_output=True, text=True,
                                 timeout=30).stdout.strip()
        except Exception as exc:                               # pragma: no cover
            ver = "(version query failed: %s)" % exc
        need("Node.js", True, "%s at %s" % (ver, node), "")
    else:
        need("Node.js", False, "not on PATH",
             "install Node.js (https://nodejs.org). REQUIRED since 23 Sep 2026: the engine "
             "gate is JavaScript because app.js is, and it is the only check that runs the "
             "engine. It is not skipped when Node.js is absent — a skipped engine gate is "
             "how the defects it catches shipped in the first place")

    return out, ok


def run_engine_gate(repo: Path):
    """Run build/check_engine_flow.mjs and fold its result into this report.

    Wired in by the registrar's decision of 23 September 2026. It had been a second command
    in README's "Before you push", which is exactly the shape that lets a gate be forgotten.

    A non-zero exit is a FAIL and its output is printed, because the detail — which node,
    which answers, what the screen said against what Continue records — is the whole value
    and is not reconstructible from a summary line.
    """
    script = repo / "build" / "check_engine_flow.mjs"
    node = shutil.which("node")
    if not node or not script.exists():
        # check_requirements() has already FAILed on whichever is missing. Saying it twice
        # buries the requirement list under a consequence of it.
        return [(NOTE, "engine gate not run — see the missing requirement above")]
    try:
        proc = subprocess.run([node, str(script)], capture_output=True, text=True,
                              cwd=str(repo), timeout=600)
    except subprocess.TimeoutExpired:
        return [(FAIL, "engine gate timed out after 600s — build/check_engine_flow.mjs "
                       "did not finish; it normally runs in under a minute")]
    except Exception as exc:                                   # pragma: no cover
        return [(FAIL, "engine gate could not be run: %s" % exc)]

    tail = (proc.stdout or "").rstrip().splitlines()
    if proc.returncode == 0:
        summary = next((l.strip() for l in reversed(tail) if l.strip()), "OK")
        return [(OK, "engine gate (build/check_engine_flow.mjs): %s" % summary)]

    print("\n".join(tail))
    if proc.stderr.strip():
        print(proc.stderr.rstrip())
    return [(FAIL, "engine gate FAILED (exit %d) — build_database.py validates the DATA, "
                   "check_engine_flow.mjs drives the ENGINE, and a defect in the seam "
                   "between them passes every data check while the tool tells a clerk one "
                   "code and records another. Output above" % proc.returncode)]


def run_build(repo: Path, layer1: Path, strict: bool, quiet: bool) -> int:
    report = Report(strict=strict)

    print("=" * 78)
    print(" ICCC-3 Lookup Tool — build & validation pipeline")
    print(" repo    : %s" % repo)
    print(" Layer 1 : %s" % (layer1 if layer1 and layer1.exists() else "%s (not found)"
                             % layer1))
    print(" mode    : %s" % ("strict (WARN counts as FAIL)" if strict else "normal"))
    print("=" * 78)

    # -- Preflight -----------------------------------------------------------------
    report.section("Preflight — requirements")
    req_findings, req_ok = check_requirements(repo, layer1)
    report.checks_run += 1
    report.add(req_findings)
    if not req_ok:
        print(report.render(quiet=quiet))
        print("\nSTOPPED AT PREFLIGHT. Every missing requirement is listed above, with how "
              "to satisfy it.\nNothing else was checked — a partial run here would report "
              "green sections that were never\nexercised, which is worse than reporting "
              "nothing.")
        return 1

    # -- Layer 1 -------------------------------------------------------------------
    report.section("Layer 1 — source of truth")
    classification_subgroups = parse_classification_subgroups(layer1)
    redcap_options, rc_findings = parse_redcap_options(layer1)
    report.checks_run += 1
    report.add(rc_findings)
    classification, cl_findings = parse_classification(layer1)
    report.checks_run += 1
    report.add(cl_findings)

    # -- A. alias index ------------------------------------------------------------
    report.section("A. alias_index.json regeneration")
    report.run(regenerate_alias_index, repo)

    # -- B. decision trees ---------------------------------------------------------
    db_dir = repo / "data" / "database"
    dt_files = sorted(db_dir.glob("group_*_dt.json")) if db_dir.exists() else []
    contexts: dict[int, DTContext] = {}

    if not dt_files:
        report.section("B. decision-tree validation")
        report.checks_run += 1
        report.add([(NOTE, "no data/database/group_*_dt.json present yet — nothing to "
                           "validate (this is expected before the first tree is authored)")])

    for path in dt_files:
        gm = re.search(r"group_(\d+)_dt\.json$", path.name)
        group = int(gm.group(1)) if gm else 0
        report.section("B. %s" % path.relative_to(repo))
        data, load_findings = load_json(path)
        report.checks_run += 1
        report.add(load_findings)
        if data is None:
            continue
        if not isinstance(data, dict):
            report.add([(FAIL, "%s: top level must be a JSON object" % path.name)])
            continue
        ctx = DTContext(path, data, group)
        contexts[group] = ctx
        report.add(ctx.shape_findings)

        # internal
        report.run(check_top_level_keys, ctx)
        report.run(check_morphology_entry_fields, ctx)
        report.run(check_morphology_code_format, ctx)
        report.run(check_behavior_codes, ctx)
        report.run(check_duplicate_code_behavior_pairs, ctx)
        report.run(check_fallback_chains, ctx)
        report.run(check_next_node_resolution, ctx)
        report.run(check_terminal_codes_exist, ctx)
        report.run(check_node_types, ctx)
        report.run(check_nos_fallback_by_node_type, ctx)
        report.run(check_captured_variables_declared, ctx)
        report.run(check_metadata_counts, ctx)
        report.run(check_node_ids_unique_and_prefixed, ctx)
        report.run(check_orphan_nodes, ctx)
        report.run(check_non_reportable_terminals, ctx)
        report.run(check_refer_terminals, ctx)
        # Group 1 schema extensions
        report.run(check_numeric_gate_shape, ctx)
        report.run(check_marker_intensity_tokens, ctx)
        report.run(check_marker_tokens_declared, ctx)
        report.run(check_detection_method, ctx)
        report.run(check_classification_system, ctx)
        report.run(check_satisfies_tests, ctx)
        report.run(check_outstanding_tests, ctx)
        report.run(check_non_reportable_heading, ctx)
        # Group II schema extensions (Group II build contract §3) — fields, not node types
        report.run(check_behaviour_resolution, ctx)
        report.run(check_provisional_pending, ctx)
        report.run(check_prior_probability, ctx)
        report.run(check_test_result_states, ctx)
        report.run(check_entity_boundary, ctx)
        report.run(check_viral_gates, ctx)
        report.run(check_burkitt_provisional, ctx)
        # Group III schema extensions (Group 3 build contract §2, §5, §6) — fields, not
        # node types. Each is a no-op on a file that does not use the field it is about.
        report.run(check_diagnosis_rendering, ctx)              # rules 1, 2
        report.run(check_resource_level_gate, ctx)              # rule 3
        report.run(check_numeric_gate_units, ctx)               # rule 4
        report.run(check_entity_annotation, ctx, repo)          # rule 5
        report.run(check_group3_behaviour_split, ctx, layer1)   # rule 6
        report.run(check_group3_absent_codes, ctx, repo)        # rule 7
        report.run(check_grade_resolution, ctx)                 # rule 9
        report.run(check_basis_of_diagnosis, ctx)               # rule 10
        report.run(check_imaging_terminals, ctx)                # rule 11
        report.run(check_group3_topography_map, ctx, layer1)    # rule 12
        report.run(check_icdo32_round_trip, ctx, layer1)        # rules 8, 13
        report.run(check_iccc3_subgroup_by_topography, ctx, layer1)   # contract §1.3
        # Group IV schema extension (Group 4 build contract §3) and its nine
        # validation rules (§8). Each is scoped to Group 4 only and is a no-op —
        # not even a NOTE — on any other group's file (verified below by diffing
        # a Groups-1-3-only report against itself with these checks added).
        report.run(check_behaviour_exclusion, ctx, layer1)             # rule 1
        report.run(check_group4_behaviour_declaration, ctx)            # rule 2
        report.run(check_group4_absent_codes, ctx, repo)               # rule 3
        report.run(check_group4_9504_unreachable, ctx)                 # rule 4
        report.run(check_group4_topography_map, ctx, repo)              # rule 5
        report.run(check_visser_table4_gate, ctx)                      # rule 6
        report.run(check_group4_not_a_group_code, ctx, repo)           # rule 8
        # Group 5 build contract §8 — seven rules. Rule 2 is the generalisation of
        # check_behaviour_exclusion() above (BEHAVIOUR_DECLARED_BY_GROUP), not a check
        # of its own. Rule 1 is an ENGINE fact and sweeps every group: FAIL on group 5,
        # WARN elsewhere, because the three Group 3 nodes it reports are on `main` and
        # outside this branch. The rest are scoped to Group 5 and are a no-op on any
        # other group's file.
        report.run(check_imaging_pathway_shape, ctx)                   # rule 1
        report.run(check_group5_code_set, ctx)                         # rule 3
        report.run(check_group5_absent_codes, ctx, repo)               # rule 4
        report.run(check_group5_imaging_sufficient, ctx)               # rule 5
        report.run(check_group5_no_ihc, ctx)                           # rule 6
        report.run(check_group5_code_neutral_molecular, ctx)           # rule 7
        # Group 6 build contract §8 — Renal Tumours. Nine validation rules, scoped
        # to Group 6 only and a no-op on any other group's file. check_behaviour_
        # exclusion() above already covers this group's behaviour_exclusion blocks
        # (BEHAVIOUR_DECLARED_BY_GROUP now carries GROUP6), and check_icdo32_round_
        # trip() / check_redcap_exact_names() above already carry the Group 6
        # extension described in contract §8 — neither needs a new call here.
        report.run(check_group6_code_set, ctx)                         # rule 1
        report.run(check_group6_absent_codes, ctx)                     # rule 2
        report.run(check_group6_behaviour_declaration, ctx, layer1)    # rule 3
        report.run(check_group6_ini1_fork, ctx)                        # rule 4
        report.run(check_group6_molecular_rcc_code, ctx)               # rule 5
        report.run(check_group6_8963_topography, ctx)                  # rule 6
        report.run(check_group6_anaplasia_code_neutral, ctx)           # rule 7
        report.run(check_group6_imaging_sufficient, ctx)               # rule 8
        report.run(check_group6_no_flow_cytometry, ctx)                # rule 9
        # Group 7 build contract §8 — Hepatic Tumours. Scoped to Group 7 and a no-op
        # on any other group's file. Rule 9 is cross-layer and runs in section C.
        report.run(check_group7_code_set, ctx)                         # rule 1
        report.run(check_group7_absent_codes, ctx, repo)               # rule 2
        report.run(check_group7_behaviour_declaration, ctx, layer1)    # rule 3
        report.run(check_group7_ini1_fork, ctx, repo)                  # rule 4
        report.run(check_group7_c22_only_codes, ctx)                   # rule 5
        report.run(check_group7_no_tissue_codes, ctx)                  # rule 6
        report.run(check_group7_imaging_constellation, ctx)            # rule 7
        report.run(check_group7_fibrolamellar, ctx)                    # rule 8
        report.run(check_group7_cnset, ctx, layer1)                    # rule 10
        report.run(check_group7_subgroup_declaration, ctx, layer1)     # rule 11
        # Group 8 build contract §8 — Malignant Bone Tumours. Three rules, scoped to
        # Group 8 and a no-op on any other group's file.
        report.run(check_group8_no_retired_ewing_code, ctx, layer1, repo)  # rule 1
        report.run(check_group8_no_pathology_codes, ctx)                   # rule 2
        report.run(check_group8_ewing_requires_partner, ctx)               # rule 3
        # Group 10 build contract §5 — Germ Cell, Trophoblastic and Gonadal Tumours. Four
        # rules, scoped to Group 10 and a no-op on any other group's file.
        report.run(check_group10_codes_fit_site, ctx, layer1, repo)            # rule 1
        report.run(check_group10_no_pathology_codes, ctx)                      # rule 2
        report.run(check_group10_alias_terms_match_icdo32, ctx, layer1, repo)  # rule 3
        report.run(check_group10_subgroups_and_routing, ctx, layer1, repo)     # rule 4
        # the four new checks (three of them are per-file)
        report.run(check_redcap_exact_names, ctx, redcap_options)
        report.run(check_redcap_banner_signal, ctx, redcap_options)
        report.run(check_cryptic_genetics, ctx)
        report.run(check_mpal_rule_ordering, ctx)
        # the 4 Sep 2026 registrar rulings
        report.run(check_iccc_subgroup_ranges, ctx, classification_subgroups)
        report.run(check_awaiting_layer1, ctx, repo)
        report.run(check_no_clinical_alerts, ctx)
        report.run(check_flow_charts, ctx)
        report.run(check_ihc_checklist_renders_a_control, ctx)
        report.run(check_no_internal_identifier_leaks, ctx)
        report.run(check_marker_names_verbatim, ctx)
        report.run(check_declared_states_consumed, ctx)
        # the override affordance (18 Sep 2026) — one per group's file
        report.run(check_override_affordance, ctx, repo)
        # source of truth
        report.run(check_codes_against_source_of_truth, ctx, redcap_options, classification)

    # -- C. cross-layer ------------------------------------------------------------
    report.section("C. cross-layer — presentation_router.json")
    report.run(check_presentation_router, repo, contexts)
    report.run(check_routing_narrows, repo, contexts)
    report.run(check_router_branch_when_vocabulary, repo, contexts)
    report.run(check_router_cns_topography_completeness, repo, contexts)
    report.run(check_group7_router_c22, repo, layer1)    # Group 7 contract §8 rule 9

    report.section("C. cross-layer — alias files")
    report.run(check_alias_cross_references, repo, contexts)

    # -- D. front-end --------------------------------------------------------------
    report.section("D. front-end — raw-hex ban")
    report.run(check_raw_hex_ban, repo)

    # -- E. engine -----------------------------------------------------------------
    report.section("E. engine — the guided flow")
    report.checks_run += 1
    report.add(run_engine_gate(repo))

    print(report.render(quiet=quiet))
    return 0 if report.passed() else 1


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Build and validate the ICCC-3 Lookup Tool data files.")
    parser.add_argument("--strict", action="store_true",
                        help="promote every WARN to a FAIL")
    parser.add_argument("--repo", default=None,
                        help="repository root (default: the parent of build/)")
    parser.add_argument("--layer1", default=None,
                        help="Layer 1 source-of-truth directory "
                             "(default: <repo>/../../ICD coding or $ICD_LAYER1)")
    parser.add_argument("--quiet", action="store_true",
                        help="print only FAIL and WARN lines")
    args = parser.parse_args(argv)

    repo = Path(args.repo).resolve() if args.repo else Path(__file__).resolve().parent.parent
    if args.layer1:
        layer1 = Path(args.layer1).resolve()
    elif os.environ.get("ICD_LAYER1"):
        layer1 = Path(os.environ["ICD_LAYER1"]).resolve()
    else:
        layer1 = (repo.parent.parent / "ICD coding").resolve()

    return run_build(repo, layer1, strict=args.strict, quiet=args.quiet)


if __name__ == "__main__":
    sys.exit(main())
