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

def parse_redcap_options(layer1: Path):
    """
    Parse RedCap Options/Group N- ….md into {group: {code: {"option": str, "name": str}}}.

    Filenames in that directory are irregular (double spaces, varying case, some groups
    split across two files) — so we glob and read the group number out of the filename.
    Option lines live inside fenced blocks and are shaped:
        9811, 9811 - B lymphoblastic leukemia/lymphoma, NOS
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
    line_re = re.compile(r"^\s*(\d+)\s*,\s*(.+?)\s*$")
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
        in_fence = False
        for raw in text.splitlines():
            if raw.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if not in_fence:
                continue
            lm = line_re.match(raw)
            if not lm:
                continue
            code, rest = lm.group(1), lm.group(2)
            # rest is normally "9811 - B lymphoblastic leukemia/lymphoma, NOS"
            nm = re.match(r"^\s*(\d+)\s*-\s*(.+?)\s*$", rest)
            name = nm.group(2) if nm else rest
            rec = bucket.setdefault(code, {"option": rest, "name": name,
                                           "names": [], "options": [],
                                           "source": md.name})
            if name not in rec["names"]:
                rec["names"].append(name)
                rec["options"].append(rest)
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


def check_marker_intensity_tokens(ctx: DTContext):
    """positive[] tokens are "MARKER" or "MARKER:strong" / "MARKER:weak" — nothing else."""
    out = []
    tokens = 0
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
                    if ":" not in token:
                        continue
                    parts = token.split(":")
                    if len(parts) != 2 or parts[1] not in MARKER_INTENSITIES:
                        out.append((FAIL, "node %s (%s): %s[] token %r — the only allowed "
                                          "suffixes are ':strong' and ':weak' "
                                          "(Pathway §7.3 item 2)"
                                    % (node_id, where or "(node level)", field, token)))
    if not out:
        out.append((OK, "%d marker token(s) use only the allowed intensity suffixes"
                    % tokens))
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
    NEW CHECK 4 — MPAL rule-ordering lint (Pathway §7.3 item 3, §7.5).

    resolution_logic is flat and first-match-wins, so a rule with no `when` placed before a
    conditioned rule silently swallows it — the MPAL genetics-first ordering (9806/9807
    before 9808) would never fire. Within every resolution_logic[], every rule carrying a
    `when` must precede every rule that has none.
    """
    out = []
    rulesets = 0
    for node_id, node in sorted(ctx.nodes.items()):
        rules = node.get("resolution_logic")
        if not isinstance(rules, list) or not rules:
            continue
        rulesets += 1
        first_unconditioned = None
        for i, rule in enumerate(rules):
            if not isinstance(rule, dict):
                out.append((FAIL, "node %s: resolution_logic[%d] is not an object"
                            % (node_id, i)))
                continue
            has_when = isinstance(rule.get("when"), dict) and bool(rule["when"])
            if not has_when and first_unconditioned is None:
                first_unconditioned = i
            elif has_when and first_unconditioned is not None:
                out.append((FAIL, "node %s: resolution_logic[%d] carries a 'when' but "
                                  "follows the unconditioned rule at index %d — "
                                  "first match wins, so the conditioned rule can never "
                                  "fire (Pathway §7.5)"
                            % (node_id, i, first_unconditioned)))
    if not out:
        out.append((OK, "rule ordering correct in %d resolution_logic ruleset(s)"
                    % rulesets))
    return out


# --------------------------------------------------------------------------------------
# B4. Against the source of truth
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
        report.run(check_detection_method, ctx)
        report.run(check_classification_system, ctx)
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
