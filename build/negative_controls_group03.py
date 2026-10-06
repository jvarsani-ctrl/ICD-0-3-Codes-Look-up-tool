#!/usr/bin/env python3
"""Negative controls for Group III's brain marker gates (check_brain_marker_cutoffs; registrar's
ruling of 6 October 2026: alpha-fetoprotein above 25 ng/mL and beta human chorionic
gonadotropin above 50 IU/L, in serum and in cerebrospinal fluid, refer to Group X).

Each control mutates an in-memory copy of group_03_dt.json, runs the check, and expects a FAIL
whose message carries every expected fragment; a FAIL for another reason is WRONG REASON. The
probe runs the check on the unmutated data first and expects it to pass. One control per gate
moves its cut-off to 250; one flips the boundary convention; one swaps a unit; one runs the
data as it stood before the ruling, pinned to commit PRE_SIOP and never to HEAD (CLAUDE.md
rule 13). Nothing on disk is changed.

    python3 build/negative_controls_group03.py

Exit status 1 if any control is not caught for its reason or the probe fails.
"""
import copy, json, subprocess, sys
from pathlib import Path
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "build"))
import build_database as bd
DT_PATH = REPO / "data/database/group_03_dt.json"
base = json.loads(DT_PATH.read_text())
PRE_SIOP = "689d610"
CHECK = bd.check_brain_marker_cutoffs


def node(d, nid):
    return next(n for t in d["decision_trees"] for n in t["nodes"] if n["node_id"] == nid)


def recut(nid, old, new):
    def mutate(d):
        for b in node(d, nid)["bands"]:
            if b["range"] in (">" + old, "<=" + old):
                b["range"] = b["range"].replace(old, new)
    return mutate


def flip_convention(d):
    for b in node(d, "md_gct_afp_serum")["bands"]:
        b["range"] = {">25": ">=25", "<=25": "<25"}.get(b["range"], b["range"])


def wrong_unit(d):
    for b in node(d, "md_gct_hcg_csf")["bands"]:
        b["unit"] = "ng_per_ml"


def at_pre_siop(d):
    old = json.loads(subprocess.run(
        ["git", "show", PRE_SIOP + ":data/database/group_03_dt.json"], cwd=REPO,
        capture_output=True, text=True, check=True).stdout)
    d.clear(); d.update(old)


def run(data):
    return CHECK(bd.DTContext(DT_PATH, data, bd.GROUP3))


controls = []
res = run(copy.deepcopy(base))
controls.append(("PROBE correct data: check_brain_marker_cutoffs", None,
                 [m for l, m in res if l == bd.FAIL], res[0][1]))


def ctl(name, expect, mutate):
    d = copy.deepcopy(base)
    mutate(d)
    res = run(d)
    controls.append((name, expect, [m for l, m in res if l == bd.FAIL],
                     res[0][1] if res else "(no finding)"))


ctl("G3-A md_gct_afp_serum cut-off 25 -> 250 ng/mL",
    ["md_gct_afp_serum: 25.01 ng/mL does not refer to Group X", "above 25 ng/mL"],
    recut("md_gct_afp_serum", "25", "250"))
ctl("G3-B md_gct_afp_csf cut-off 25 -> 250 ng/mL",
    ["md_gct_afp_csf: 25.01 ng/mL does not refer to Group X", "above 25 ng/mL"],
    recut("md_gct_afp_csf", "25", "250"))
ctl("G3-C md_gct_hcg_csf cut-off 50 -> 250 IU/L",
    ["md_gct_hcg_csf: 50.01 IU/L does not refer to Group X", "above 50 IU/L"],
    recut("md_gct_hcg_csf", "50", "250"))
ctl("G3-D md_gct_hcg_serum cut-off 50 -> 250 IU/L",
    ["md_gct_hcg_serum: 50.01 IU/L does not refer to Group X", "above 50 IU/L"],
    recut("md_gct_hcg_serum", "50", "250"))
ctl("G3-E md_gct_afp_serum reads 'at or above' 25",
    ["md_gct_afp_serum: 25 ng/mL refers to Group X", "(band '>=25')"], flip_convention)
ctl("G3-F md_gct_hcg_csf bands read in ng/mL",
    ["md_gct_hcg_csf bands[0]", "is read in 'ng_per_ml'", "hcg_csf_iu_l is 50 IU/L"],
    wrong_unit)
ctl("G3-G Group III at %s, Hu 2016's cut-offs" % PRE_SIOP,
    ["md_gct_hcg_serum: 50 IU/L refers to Group X", "(band '>=2.5')"], at_pre_siop)

wrong = caught = probes = 0
for name, expect, fails, first in controls:
    if expect is None:
        ok = not fails
        probes += ok
        verdict, msg = ("PASSES", first) if ok else ("*** WRONG ***", fails[0])
    else:
        hit = next((m for m in fails if all(x in m for x in expect)), None)
        ok = hit is not None
        caught += ok
        verdict = "CAUGHT" if ok else ("*** WRONG REASON ***" if fails else "*** MISSED ***")
        msg = hit or (fails[0] if fails else first)
    wrong += not ok
    print("%-56s %s | %s" % (name, verdict, msg[:170]))
n_ctl = sum(1 for c in controls if c[1] is not None)
print("\n%d of %d controls caught for the expected reason; %d of %d probes pass"
      % (caught, n_ctl, probes, len(controls) - n_ctl))
sys.exit(1 if wrong else 0)
