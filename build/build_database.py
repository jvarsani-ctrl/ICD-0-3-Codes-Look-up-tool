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
import json
import os
import re
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
    "confidence_ceiling",
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
    True when `holder` IS a `nos_fallback` object — {"code", "name", "reason"} per DT
    master §3C/§3D, consumed by app.js's fallbackTarget() — rather than some other
    dict that merely happens to carry a 'reason'.

    Identified by two things at once, deliberately narrow: the key it hangs off (its
    walk_dicts path ends in "nos_fallback") AND its shape (both 'code' and 'name'
    present). Neither alone is enough — a holder could be named nos_fallback without
    yet having code/name (still a shape bug worth catching), or could carry an
    unrelated 'code'/'name' pair under some other key. Requiring both keeps this from
    ever masking a real code-less-terminal violation.
    """
    if not isinstance(holder, dict):
        return False
    last_key = where.rsplit(".", 1)[-1] if where else ""
    if last_key != "nos_fallback":
        return False
    return as_code(holder.get("code")) is not None and bool(holder.get("name"))


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
        """
        for node_id, node in self.nodes.items():
            for holder, where in walk_dicts(node):
                target = holder.get("next_node")
                if isinstance(target, str) and target:
                    yield (node_id, target,
                           holder.get("detection_method"),
                           where or "(node level)")

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
                # A nos_fallback object is {"code", "name", "reason"} by design (DT
                # master §3C/§3D) — a reason with no next_node/morphology_code of its
                # own is exactly its documented shape, not a code-less terminal.
                continue
            if is_provisional_pending_object(holder, where):
                # A provisional_pending object is {"reason", "resolving_test", …} by
                # design (Group II contract §3.2). Its `reason` is clerk-facing text
                # ABOUT the code its branch emits; the branch carries the destination.
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
    """
    out = []
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
            elif set(values) != {"1", "3"}:
                out.append((FAIL, "%s: behaviour_resolution.values is keyed %s — exactly "
                                  "\"1\" and \"3\" are required (contract §3.1)"
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

            for key in ("1", "3"):
                if key in values:
                    check_leaf('values["%s"]' % key, values[key], key)
                elif isinstance(br.get("values"), dict):
                    out.append((FAIL, "%s: behaviour_resolution.values[%r] is missing"
                                % (loc, key)))

            unresolved = br.get("unresolved")
            if unresolved is None:
                out.append((FAIL, "%s: behaviour_resolution.unresolved is REQUIRED "
                                  "(contract §3.1). Without it the engine has no answer for "
                                  "a file that never states the behaviour, and the case "
                                  "leaves the node with no code at all — a reportable "
                                  "childhood cancer dropped from the registry rather than "
                                  "coded" % loc))
            else:
                check_leaf("unresolved", unresolved, "3")
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
    that would overturn it. It is not a synonym for low confidence — `confidence` already
    says that, and says it about the whole terminal rather than about one outstanding
    result.

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
    they become indistinguishable — same code, same confidence, same follow-up — because
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
# B5. Against the source of truth
# --------------------------------------------------------------------------------------

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
    no_option: list[str] = []
    for code in sorted(ctx.codes):
        in_redcap = code in redcap
        in_classif = code in classif
        if not in_redcap and not in_classif:
            out.append((FAIL, "morphology_code %s is in neither the REDCap options file nor "
                              "the ICCC classification table for group %d — never fabricate "
                              "a code (Architecture §11 rule 1). If this is a ratified "
                              "post-ICCC-2017 addition (e.g. an ICD-O-3.2 code), Layer 1 "
                              "must be updated before the build can pass."
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
# B5. Cross-layer checks
# --------------------------------------------------------------------------------------

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

def run_build(repo: Path, layer1: Path, strict: bool, quiet: bool) -> int:
    report = Report(strict=strict)

    print("=" * 78)
    print(" ICCC-3 Lookup Tool — build & validation pipeline")
    print(" repo    : %s" % repo)
    print(" Layer 1 : %s" % (layer1 if layer1 and layer1.exists() else "%s (not found)"
                             % layer1))
    print(" mode    : %s" % ("strict (WARN counts as FAIL)" if strict else "normal"))
    print("=" * 78)

    # -- Layer 1 -------------------------------------------------------------------
    report.section("Layer 1 — source of truth")
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
        # Group II schema extensions (Group II build contract §3) — fields, not node types
        report.run(check_behaviour_resolution, ctx)
        report.run(check_provisional_pending, ctx)
        report.run(check_prior_probability, ctx)
        report.run(check_test_result_states, ctx)
        report.run(check_entity_boundary, ctx)
        report.run(check_viral_gates, ctx)
        report.run(check_burkitt_provisional, ctx)
        # the four new checks (three of them are per-file)
        report.run(check_redcap_exact_names, ctx, redcap_options)
        report.run(check_cryptic_genetics, ctx)
        report.run(check_mpal_rule_ordering, ctx)
        # source of truth
        report.run(check_codes_against_source_of_truth, ctx, redcap_options, classification)

    # -- C. cross-layer ------------------------------------------------------------
    report.section("C. cross-layer — presentation_router.json")
    report.run(check_presentation_router, repo, contexts)

    report.section("C. cross-layer — alias files")
    report.run(check_alias_cross_references, repo, contexts)

    # -- D. front-end --------------------------------------------------------------
    report.section("D. front-end — raw-hex ban")
    report.run(check_raw_hex_ban, repo)

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
