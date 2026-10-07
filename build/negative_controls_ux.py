#!/usr/bin/env python3
"""
negative_controls_ux.py — prove the UX checks fail when the thing they guard is broken.

Standing rule 10: break the engine or the data on purpose, watch the check fail for the
right reason, restore, watch it pass. This script does that for the checks added with the
tick lists, Home, the filter box, the coding block and the referral hop (spec
docs/superpowers/specs/2026-10-06-ux-overall-fixes-design.md).

ENGINE controls. Each one copies app.js to a scratch file, applies ONE edit that undoes a
feature, and runs the engine gate against that copy (APP=<copy>). The gate must exit
non-zero and the named check must be among the lines it prints as FAIL. The edit is
refused if it matches nothing, so a control cannot pass by changing nothing.

DATA controls. Each one hands check_tick_lists() a small node broken one way and expects
a FAIL naming that way. A sound node is the positive control.

Run:  python3 build/negative_controls_ux.py        (exit 0 when every control behaves)
"""
import importlib.util
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "app.js"

# (name, text that must be in app.js, replacement, the check whose FAIL line must appear)
ENGINE_CONTROLS = [
    ("fit ignores `excludes`",
     "&& !arr(t.excludes).some(has);", "&& true;",
     "imaging alone takes the imaging tier"),
    ("fit ignores `any_of`",
     "(!any.length || any.some(has))", "true",
     "imaging alone takes the imaging tier"),
    ("first_match takes the last fit, not the first",
     "var hit = tickOffered(n, ids)[0];", "var hit = tickOffered(n, ids).slice(-1)[0];",
     "first_match: the first fitting option is the destination"),
    ("a chosen special situation is ignored",
     "var pickedCtx = Number(state.draft.ctx) || 0;", "var pickedCtx = 0;",
     "a special situation routes at once"),
    ("stepping back loses the ticks",
     "if (ticked) state.draft.ticks = ticked.slice();", "",
     "stepping back to the tier taken automatically"),
    ("the hop keeps the stains read under the old tree",
     "state.markers = {}; state.workup = []; state.pending = null; state.pendingGrade = null;\n  state.grade = null;",
     "state.workup = []; state.pending = null; state.pendingGrade = null;\n  state.grade = null;",
     "the topography and the documents ticked carry over"),
    ("the hop forgets where the evidence began",
     "state.hopFrom = state.trailAtGroupEntry;", "state.hopFrom = null;",
     "the trail shows the hop"),
    ("the hop button is never offered",
     "  return r.recaptureSite === true || !(groupMeta(r.group).tree_routing && !state.captured.topography);",
     "  return false;",
     "a referral to a built group offers Continue"),
    ("an aid shows on every option, not only the selected one",
     "(it.aid && on ?", "(it.aid ?",
     "a list with recognition aids shows none until an option is selected"),
    ("Home never asks first",
     "      state.confirmExit = true;\n      /* The safe answer takes the keyboard focus, and Escape gives it. */",
     "      return reset();\n      /* The safe answer takes the keyboard focus, and Escape gives it. */",
     "Home on a case with answers asks first"),
    ("the organ-system filter ignores region names",
     "[it.label, it.meta, it.find]", "[it.label, it.meta]",
     "typing a region name that is not in the system"),
    ("no list has a filter box",
     "var FILTER_MIN_OPTIONS = 1;", "var FILTER_MIN_OPTIONS = 99999;",
     "the context list carries its own filter box"),
    ("the benign terminal says no code is emitted again",
     "codingBlock(r.icdoTerm, r.icdoCode, r.icdoBehaviour, basisFromTrail()) +",
     "'<div class=\"orow orow--excluded\"><b>Morphology</b><span>No code emitted here.</span></div>' +",
     "a benign tumour reports Name, Morphology code"),
    ("topography prints the C-code",
     "return num + (name ? ' (' + name + ')' : '');", "return code;",
     "topography is the code without its letter and point"),
    ("the interface says Behaviour again",
     "if (state.pending) return 'Behavior';", "if (state.pending) return 'Behaviour';",
     "the interface says Behavior, never Behaviour"),
    ("the behavior meaning is dropped",
     "return '/' + d + (BEHAVIOR_MEANING[d] ? ' (' + BEHAVIOR_MEANING[d] + ')' : '');", "return '/' + d;",
     "behavior codes read /N (meaning)"),
    ("a laboratory value is also stored as a case variable a rule could read",
     ".concat(rows);\n", ".concat(rows);\n  rows.forEach(function (l) { state.captured[l.id] = l.value; });\n",
     "the values stay out of the case variables"),
    ("text that is not a number is accepted as a result",
     "} else if (!LAB_NUMBER.test(typed)) {", "} else if (false) {",
     "text that is not a number is refused"),
    ("the panel's values are written into Suggested based on",
     ".filter(function (t) { return !t.quiet; })", ".filter(function (t) { return true; })",
     "the panel is one trail entry that summarises it"),
    ("the laboratory screen offers the diagnostic escapes",
     "  if (n && n.node_type === 'lab_results') return '';\n", "",
     "the laboratory screen has a row per test"),
    ("a result in the panel no longer ticks Lab Report",
     "if (voc && rows.some(function (l) { return l.inFile; })) {", "if (false) {",
     "a result in the panel ticks Lab Report"),
    ("an empty row is no longer taken as not in the file",
     "return typed === '' || !!(r && r.absent);", "return !!(r && r.absent);",
     "an empty panel continues"),
    ("the boxes start ticked again",
     "var ticked = !!r.absent, id = 'lab-' + lab.id;", "var ticked = !String(r.value || '').trim(), id = 'lab-' + lab.id;",
     "an EMPTY Not in the file box"),
    ("the hop drops the laboratory panel",
     "  state.markers = {}; state.workup = []; state.pending = null; state.pendingGrade = null;\n  state.grade = null;",
     "  state.markers = {}; state.workup = []; state.pending = null; state.pendingGrade = null; state.labs = [];\n  state.grade = null;",
     "the laboratory panel is a fact of the case"),
    ("stepping back loses what was typed on the laboratory screen",
     "if (typedLabs) state.draft.labs = JSON.parse(JSON.stringify(typedLabs));", "",
     "stepping back reopens the panel as it was typed"),
    ("the result no longer lists the panel",
     "  var rows = arr(state.labs);\n  if (!rows.length) return '';", "  var rows = arr(state.labs);\n  return '';",
     "the result lists each test with its value and unit"),
    ("the exit bar scrolls the page around the frame again",
     "if (hidden > 0) window.scrollBy(0, hidden + 8);", "el.scrollIntoView({ block: 'nearest' });",
     "the tool opens no dialog, window or storage"),
    ("a confirm dialog replaces the exit bar",
     "      state.confirmExit = true;\n      /* The safe answer", "      if (window.confirm('Leave this case?')) return reset();\n      state.confirmExit = true;\n      /* The safe answer",
     "the tool opens no dialog, window or storage"),
    ("the unit sentence says \"entering the count\" under every unit again",
     "'and a count over the same denominator, before entering it.</p>'", "'. Check the report states the same denominator before entering the count.</p>'",
     "the unit sentence no longer says"),
    ("the second question lists every tier, not the ones that fit",
     "var offered = tickOffered(n, arr(state.captured[tl.variable]));\n  return '<p class=\"node__hint\">'",
     "var offered = tickContexts(n).concat(tickOffered(n, arr(state.captured[tl.variable])));\n  return '<p class=\"node__hint\">'",
     "two tiers fit histology with stains"),
    # ---- the review of 6 October 2026: what stepping back, a refused entry, an error screen and the keyboard do
    ("a refused number ticks the blank rows' boxes",
     "var row = { value: typed, unit: unit, absent: !!r.absent };", "var row = { value: typed, unit: unit, absent: labRowAbsent(r) };",
     "after a refused number the boxes the clerk did not tick are still empty"),
    ("stepping back to the laboratory screen ticks the blank rows' boxes",
     "var row = { value: typed, unit: unit, absent: !!r.absent };", "var row = { value: typed, unit: unit, absent: labRowAbsent(r) };",
     "stepping back shows no box ticked that the clerk did not tick"),
    ("hex, exponent and thousands marks are accepted as results",
     "} else if (!LAB_NUMBER.test(typed)) {", "} else if (!isFinite(Number(typed.replace(',', '.')))) {",
     "a result is digits with at most one decimal mark"),
    ("the number box has no length limit",
     ' type="text" inputmode="decimal" autocomplete="off" maxlength="12"', ' type="text" inputmode="decimal" autocomplete="off"',
     "the number box is length-limited"),
    ("the laboratory entry is not marked as typed text",
     "  state.trail[at].typed = true;\n", "",
     "the entry is marked as typed text"),
    ("a second laboratory panel replaces the first",
     "state.labs = arr(state.labs).filter(function (l) { return !mine[l.id]; }).concat(rows);", "state.labs = rows;",
     "a second panel replaces the tests it lists and keeps the rest"),
    ("a unit another panel held is shown though this test does not list it",
     "return r && units.indexOf(r.unit) !== -1 ? r.unit : (units[0] || '');", "return (r && r.unit) || units[0] || '';",
     "a unit held from another panel that this test does not list"),
    ("stepping back across a hop leaves the receiving group's file loaded",
     "  if (c) { state.dt = c.dt; state.aliases = c.aliases; }\n", "",
     "stepping back across the hop brings the first group's file back"),
    ("the app bar names whichever group file is in memory",
     "if (state.group && md && (md.group_id === undefined || Number(md.group_id) === Number(state.group))) {", "if (state.group && md) {",
     "the app bar names that group, not the one left"),
    ("a step back forgets where the evidence began",
     "trailAtGroupEntry: state.trailAtGroupEntry, hopFrom: state.hopFrom", "trailAtGroupEntry: state.trailAtGroupEntry, hopFrom: null",
     "stepping back to the tree question keeps where the evidence began"),
    ("a tap while a group file loads is acted on",
     "  if (state.stage === 'boot' && !state.error) return;\n", "",
     "a second tap while the group is loading does nothing"),
    ("a hop is offered into a site-routed group with no site",
     "  return r.recaptureSite === true || !(groupMeta(r.group).tree_routing && !state.captured.topography);", "  return true;",
     "a referral into a group that routes its trees by site offers no hop"),
    ("a recapture referral is refused a hop when the case has no site",
     "  return r.recaptureSite === true || !(groupMeta(r.group).tree_routing && !state.captured.topography);",
     "  return !(groupMeta(r.group).tree_routing && !state.captured.topography);",
     "a referral that asks for the primary's site offers the hop into"),
    ("the hop keeps the old tree's grade and entity",
     "state.grade = null; state.entity = null; state.firedAlert = null; state.draft = {};", "state.draft = {};",
     "the hop clears the old tree's reading"),
    ("the hop forgets the organ system and the discriminator answers",
     "  var keep = ['topography', 'organ_system', 'tumour_origin'];", "  var keep = ['topography'];",
     "the hop keeps the case"),
    ("a range of sites with an instruction is mangled into a code",
     "  if (!/^C\\d{2}(\\.\\d)?$/i.test(String(code))) return String(code);\n", "",
     "a topography written as a range with an instruction prints as written"),
    ("Home is offered on a start-up failure",
     "home.hidden = !state.router || ((state.stage", "home.hidden = false || ((state.stage",
     "Home is not offered on a start-up failure"),
    ("the Leave this case bar comes before the screen",
     "renderStage() + (state.confirmExit ? renderExitConfirm() : '')", "(state.confirmExit ? renderExitConfirm() : '') + renderStage()",
     "the Leave this case bar comes after the screen"),
    ("Home does not hand the focus to Keep Working",
     "      state.focusNext = '[data-act=\"home-no\"]';\n", "",
     "Home hands the keyboard focus to Keep Working"),
    ("Keep Working does not hand the focus back to Home",
     "case 'home-no': state.focusNext = '#appbar-home'; return;", "case 'home-no': return;",
     "Keep Working hands the focus back to Home"),
    ("a redraw drops the keyboard focus",
     "var held = sameScreen ? focusKey(document.activeElement) : null;", "var held = null;",
     "a box ticked from the keyboard keeps the focus through the redraw"),
    ("a new screen takes the old control's focus",
     "var held = sameScreen ? focusKey(document.activeElement) : null;", "var held = focusKey(document.activeElement);",
     "a new screen restores no focus"),
    ("a refused number leaves the focus where it was",
     "    state.focusNext = '.labrow__value[aria-invalid=\"true\"]';\n", "",
     "a refused number moves the focus to its box"),
    ("the error is not tied to its box",
     "(r.error ? ' aria-invalid=\"true\" aria-describedby=\"' + esc(id) + '-error\"' : '')", "(r.error ? ' aria-invalid=\"true\"' : '')",
     "a refused number moves the focus to its box, which names the error"),
    ("the filter hides the selected row of a select-then-confirm list",
     "var hit = !withBox || !typed || on || findMatch(findText(it), typed);", "var hit = !withBox || !typed || findMatch(findText(it), typed);",
     "a select-then-confirm list keeps the selected row on screen"),
    ("the filter hides the chosen radio row",
     "var hit = !withBox || !typed || Number(selected) === i || findMatch(findText(it), typed);", "var hit = !withBox || !typed || findMatch(findText(it), typed);",
     "a radio list keeps the row the clerk has chosen on screen"),
    ("typing hides the selected row on screen",
     "var hit = rowSelected(row) || findMatch(row.getAttribute('data-find'), typed);", "var hit = findMatch(row.getAttribute('data-find'), typed);",
     "typing in a filter box hides the rows that do not match and keeps the selected one"),
    ("the filter count is not announced",
     "  if (say) say.textContent = shownText(shown);\n", "",
     "typing in a filter box hides the rows that do not match"),
    ("Enter in an empty filter box answers with the first option",
     "    if (!el.value.trim()) return;\n", "",
     "Enter in an empty filter box answers nothing"),
    ("Enter takes the selected row instead of the first match",
     "      if (!findMatch(r.getAttribute('data-find'), el.value)) return false;\n", "",
     "Enter takes the first row that matches what was typed"),
    ("Escape does not answer the leave bar",
     "if (ev.key !== 'Escape' || !state.confirmExit) return;", "return;",
     "Escape answers the Leave this case bar with Keep Working"),
    ("typing a number leaves Not in the file ticked",
     "if (absentBox && el.value.trim() !== '') absentBox.checked = false;", "",
     "typing a number in a laboratory row clears"),
    ("a box cannot be unticked",
     "else if (!el.checked && at !== -1) mine.splice(at, 1);", "",
     "tick lists in the data"),
    ("the ticks are kept in the order they were ticked, not the order drawn",
     "var ids = orderedTicks(tl, ticksNow(tl));", "var ids = ticksNow(tl).slice();",
     "tick lists in the data"),
    ("a referral loses its Suggested based on row",
     "      orow('Suggested based on', basisFromTrail() || '\u2014') +\n      labResultsBlock() + hopAction(r)", "      labResultsBlock() + hopAction(r)",
     "a referral prints its rows"),
    ("a non-reportable exclusion loses its topography row",
     "      orow('Topography code', topographyText(state.captured.topography)) +\n      labResultsBlock() + outActions() + '</div>';\n  }\n  /* Group 4",
     "      labResultsBlock() + outActions() + '</div>';\n  }\n  /* Group 4",
     "a non-reportable exclusion prints its rows"),
    ("the standard terminal loses its Suggested based on row",
     "    orow('Suggested based on', basis || '\\u2014') + '</div>';", "    '</div>';",
     "a code from the standard terminal at behavior"),
    ("a tier taken by the engine is listed in Suggested based on again",
     "    state.trail[at].quiet = true;\n    return went;", "    return went;",
     "a tier the engine takes by itself stays out of"),
    ("a cytogenetics dropdown is no longer a filtered radio list",
     "choose('option', opts.map(function (o) { return { label: o.label || o.finding }; }), state.draft.option);", "choose('option', [], state.draft.option);",
     "a cytogenetics dropdown is a filtered radio list"),
]


def engine_gate(app_path: Path, only_ux=False):
    env = dict(os.environ, APP=str(app_path))
    if only_ux:
        env["ONLY"] = "ux"      # the new section alone: the unbroken run below still runs everything
    p = subprocess.run(["node", str(ROOT / "build" / "check_engine_flow.mjs")], cwd=ROOT, env=env,
                       capture_output=True, text=True, timeout=900)
    return p.returncode, p.stdout + p.stderr


def run_engine_controls():
    bad = 0
    src = APP.read_text(encoding="utf-8")
    code, out = engine_gate(APP)
    ok = code == 0
    print("  %s  the unbroken engine passes the engine gate" % ("OK  " if ok else "FAIL"))
    bad += 0 if ok else 1
    with tempfile.TemporaryDirectory() as tmp:
        for name, old, new, check in ENGINE_CONTROLS:
            if src.count(old) != 1:
                print("  FAIL  control %r: the text it edits occurs %d times in app.js (must be once)" % (name, src.count(old)))
                bad += 1
                continue
            broken = Path(tmp) / "app_broken.js"
            broken.write_text(src.replace(old, new), encoding="utf-8")
            code, out = engine_gate(broken, only_ux=True)
            fails = [l.strip() for l in out.splitlines() if l.strip().startswith("FAIL")]
            hit = any(check in l for l in fails)
            good = code != 0 and hit
            print("  %s  broken: %s -> gate %s, %s" % (
                "OK  " if good else "FAIL", name, "failed" if code else "PASSED (wrong)",
                "named '%s'" % check if hit else "did not name '%s' (it named %s)" % (check, [l[:70] for l in fails[:2]])))
            bad += 0 if good else 1
    return bad


def load_build():
    spec = importlib.util.spec_from_file_location("build_database", ROOT / "build" / "build_database.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["build_database"] = mod
    spec.loader.exec_module(mod)
    return mod


class Ctx:
    """What the checks read from a DTContext: its nodes, and the raw data to walk."""
    def __init__(self, nodes, entry=None):
        self.nodes = nodes
        self.data = {"decision_trees": [{"tree_id": "t", "entry_node": entry, "nodes": list(nodes.values())}]}


VOC = {"evidence_documents": {"variable": "documents_in_file", "items": [
    {"id": i, "label": i} for i in ("referral", "imaging", "lab", "cytology", "histology", "ihc", "genetics")]}}


def evidence_node(**over):
    node = {
        "node_id": "n", "node_type": "document_inventory", "step_label": "Evidence in file",
        "tick_list": {"vocabulary": "evidence_documents"},
        "options": [
            {"label": "referral", "ticks": {"excludes": ["imaging", "cytology", "histology", "ihc", "genetics"]}},
            {"label": "imaging", "ticks": {"requires": ["imaging"], "excludes": ["cytology", "histology", "ihc", "genetics"]}},
            {"label": "cytology", "ticks": {"requires": ["cytology"], "excludes": ["histology", "ihc", "genetics"]}},
            {"label": "histology", "ticks": {"any_of": ["histology", "ihc", "genetics"]}},
            {"label": "special", },
        ],
    }
    node.update(over)
    return node


def run_data_controls():
    bm = load_build()
    FAIL, OK = bm.FAIL, bm.OK
    bad = 0

    def verdict(nodes):
        return bm.check_tick_lists(Ctx(nodes), ROOT, vocabularies=VOC)

    def expect(name, nodes, want):
        nonlocal bad
        res = verdict(nodes)
        if want is None:
            good = all(l == OK for l, _ in res) and res
        else:
            good = any(l == FAIL and re.search(want, m) for l, m in res)
        print("  %s  %s" % ("OK  " if good else "FAIL", name))
        if not good:
            print("        got: %s" % [(l, m[:110]) for l, m in res][:3])
            bad += 1

    expect("a sound evidence gate passes", {"n": evidence_node()}, None)

    n = evidence_node(); n["options"][3]["ticks"] = {"requires": ["histology"]}        # {ihc} alone now fits nothing
    expect("broken: {ihc} alone dead-ends -> FAIL naming the stranded sets", {"n": n}, r"fit no option")

    n = evidence_node(); n["options"][1]["ticks"]["excludes"].append("imaging")        # requires and excludes share an id
    expect("broken: an id in both requires and excludes -> FAIL", {"n": n}, r"is in both ticks\.requires and ticks\.excludes")

    n = evidence_node(); n["options"][1]["ticks"]["requires"] = ["x-ray"]
    expect("broken: an id not in the list -> FAIL", {"n": n}, r"names 'x-ray'")

    n = evidence_node(); n["tick_list"] = {"vocabulary": "no_such_list"}
    expect("broken: an unknown vocabulary -> FAIL", {"n": n}, r"names vocabulary 'no_such_list'")

    n = evidence_node(); del n["tick_list"]
    expect("broken: an evidence gate with no tick list -> FAIL", {"n": n}, r"evidence gate .* no `tick_list`")

    n = evidence_node(step_label="Prior therapy"); del n["tick_list"]
    expect("broken: ticks on options of a node with no tick list -> FAIL", {"n": n}, r"declares no `tick_list`")

    n = evidence_node(); n["tick_list"]["resolve"] = "pick_one"
    expect("broken: an unknown resolve mode -> FAIL", {"n": n}, r"resolve 'pick_one'")

    n = evidence_node(); n["options"][1]["ticks"]["need"] = ["imaging"]
    expect("broken: an unknown ticks field -> FAIL", {"n": n}, r"unknown ticks field")

    n = evidence_node(); n["options"] = [o for o in n["options"] if o.get("ticks") is None]
    expect("broken: no tier at all -> FAIL", {"n": n}, r"at least one option with")

    def first_match(extra=None, drop_fallback=False):
        node = {"node_id": "m", "node_type": "histology_subclassification", "step_label": "Components",
                "tick_list": {"resolve": "first_match", "variable": "c",
                              "items": [{"id": "a", "label": "A"}, {"id": "b", "label": "B"}, {"id": "c", "label": "C"}]},
                "options": [{"label": "a", "ticks": {"requires": ["a"]}},
                            {"label": "bc", "ticks": {"requires": ["b", "c"], "excludes": ["a"]}}]}
        if not drop_fallback:
            node["options"].append({"label": "else", "ticks": {}})
        for o in extra or []:
            node["options"].append(o)
        return {"m": node}

    expect("a sound first_match list passes", first_match(), None)
    expect("broken: first_match with no fallback strands {b} -> FAIL", first_match(drop_fallback=True), r"fit no option")
    expect("broken: a shadowed first_match option -> FAIL",
           first_match(extra=[{"label": "dead", "ticks": {"requires": ["a"], "excludes": ["b"]}}]), r"never the first fit")
    m = first_match(); m["m"]["options"][1].pop("ticks")
    expect("broken: a first_match option with no ticks -> FAIL", m, r"every option carries `ticks`")

    n = evidence_node()
    n["tick_list"] = {"vocabulary": "evidence_documents", "items": [{"id": "i%d" % k, "label": "x"} for k in range(13)]}
    expect("broken: more than 12 items -> FAIL (the enumeration budget)", {"n": n}, r"13 tick items")
    # ---- the review of 6 October 2026
    def verdict_entry(nodes, entry, voc=None):
        return bm.check_tick_lists(Ctx(nodes, entry), ROOT, vocabularies=voc or VOC)

    def expect_entry(name, nodes, entry, want, voc=None):
        nonlocal bad
        res = verdict_entry(nodes, entry, voc)
        good = (all(l == OK for l, _ in res) and res) if want is None else any(l == FAIL and re.search(want, m) for l, m in res)
        print("  %s  %s" % ("OK  " if good else "FAIL", name))
        if not good:
            print("        got: %s" % [(l, m[:110]) for l, m in res][:3])
            bad += 1

    n = evidence_node(step_label="Documents on hand"); del n["tick_list"]
    expect_entry("broken: the tree's own first gate is renamed and has no tick list -> FAIL (keyed off the entry node, not the label)",
                 {"n": n}, "n", r"evidence gate .* no `tick_list`")
    lab = lab_node(next_node="n")
    n = evidence_node(step_label="Documents on hand"); del n["tick_list"]
    expect_entry("broken: the gate behind a laboratory screen at the tree's entry has no tick list -> FAIL",
                 {"labs": lab, "n": n}, "labs", r"evidence gate .* no `tick_list`")
    n = evidence_node(); n["options"][0]["ticks"] = {}
    expect_entry("broken: a tier that fits every set sits beside the others -> FAIL", {"n": n}, "n", r"`ticks: \{\}` fits every ticked set")
    n = evidence_node(); n["tick_list"] = {"vocabulary": "evidence_documents", "variable": "my_documents"}
    expect_entry("broken: a node renames the vocabulary's variable, so a second gate opens empty -> FAIL", {"n": n}, "n", r"overrides the vocabulary's variable")
    voc = {"evidence_documents": dict(VOC["evidence_documents"], prompt="Tick every next_node you hold")}
    expect_entry("broken: a vocabulary sentence names a schema field a clerk cannot see -> FAIL", {"n": evidence_node()}, "n", r"internal identifier", voc)

    # recognition aids: only a list that draws them
    def aid_node(node_type="morphology_only", tick=False):
        node = {"node_id": "a", "node_type": node_type, "step_label": "Tumour type", "nos_fallback": None,
                "options": [{"label": "x", "next_node": "b", "recognition_aid": "sheets of small round blue cells"}]}
        if tick:
            node["tick_list"] = {"items": [{"id": "i", "label": "I"}], "variable": "v"}
        return {"a": node}
    res = bm.check_recognition_aids(Ctx(aid_node()))
    print("  %s  a recognition aid on a morphology list passes" % ("OK  " if all(l == OK for l, _ in res) else "FAIL"))
    bad += 0 if all(l == OK for l, _ in res) else 1
    for name, nodes, want in [("broken: an aid on a node type that does not draw it -> FAIL", aid_node("ihc_checklist"), r"never be shown"),
                              ("broken: an aid on a node that answers by tick list -> FAIL", aid_node(tick=True), r"never be shown")]:
        res = bm.check_recognition_aids(Ctx(nodes))
        good = any(l == FAIL and re.search(want, m) for l, m in res)
        print("  %s  %s" % ("OK  " if good else "FAIL", name))
        bad += 0 if good else 1
    nodes = aid_node(); nodes["a"]["options"][0]["recognition_aid"] = "  "
    res = bm.check_recognition_aids(Ctx(nodes))
    good = any(l == FAIL and re.search(r"non-empty string", m) for l, m in res)
    print("  %s  broken: an empty aid -> FAIL" % ("OK  " if good else "FAIL"))
    bad += 0 if good else 1

    # clerk-facing text keys: a field name in a prompt or a unit reaches the clerk
    def leak(node):
        return bm.check_no_internal_identifier_leaks(Ctx({"n": node}))
    sound = {"node_id": "n", "node_type": "morphology_only", "tick_list": {"prompt": "Tick every report in the file."}, "options": []}
    res = leak(sound)
    print("  %s  a prompt with no field name passes" % ("OK  " if not any(l == FAIL for l, _ in res) else "FAIL"))
    bad += 1 if any(l == FAIL for l, _ in res) else 0
    for key, where in [("prompt", "tick_list"), ("context_prompt", "tick_list"), ("none_label", "tick_list"), ("sibling_prompt", "tick_list")]:
        node = {"node_id": "n", "node_type": "morphology_only", "tick_list": {key: "Pick the next_node you want"}, "options": []}
        good = any(l == FAIL and "next_node" in m for l, m in leak(node))
        print("  %s  broken: %s names a schema field -> FAIL" % ("OK  " if good else "FAIL", key))
        bad += 0 if good else 1
    node = {"node_id": "n", "node_type": "lab_results", "labs": [{"id": "a", "label": "A", "units": ["refer_group"]}]}
    good = any(l == FAIL and "refer_group" in m for l, m in leak(node))
    print("  %s  broken: a unit names a schema field -> FAIL" % ("OK  " if good else "FAIL"))
    bad += 0 if good else 1

    # the registrar-reviewed mapping: a swap of two tiers' rules still covers every set
    import copy, json
    gpath = ROOT / "data" / "database" / "group_05_dt.json"
    data = json.loads(gpath.read_text(encoding="utf-8"))
    ctx = bm.DTContext(gpath, data, 5)
    res = bm.check_evidence_mapping(ctx, ROOT)
    good = all(l == OK for l, _ in res) and res
    print("  %s  the unbroken group file matches its mapping" % ("OK  " if good else "FAIL"))
    bad += 0 if good else 1
    swapped = copy.deepcopy(data)
    node = next(n for t in swapped["decision_trees"] for n in t["nodes"] if n.get("tick_list"))
    tiers = [o for o in node["options"] if "ticks" in o]
    tiers[0]["ticks"], tiers[1]["ticks"] = tiers[1]["ticks"], tiers[0]["ticks"]
    res = bm.check_evidence_mapping(bm.DTContext(gpath, swapped, 5), ROOT)
    good = any(l == FAIL and node["node_id"] in m and "differs" in m for l, m in res)
    print("  %s  broken: two tiers' rules swapped -> FAIL naming the node" % ("OK  " if good else "FAIL"))
    bad += 0 if good else 1

    # the router may hand off to a laboratory screen that leads to the gate, and to nothing else
    import tempfile
    gpath5 = ROOT / "data" / "database" / "group_05_dt.json"
    base5 = json.loads(gpath5.read_text(encoding="utf-8"))

    def router_verdict(next_node):
        d = copy.deepcopy(base5)
        tree = d["decision_trees"][0]
        tree["entry_node"] = "rb_labs"
        tree["nodes"].insert(0, {"node_id": "rb_labs", "node_type": "lab_results", "step_label": "Laboratory results",
                                  "next_node": next_node, "nos_fallback": None,
                                  "labs": [{"id": "a", "label": "A", "units": ["u"]}]})
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "data" / "shared").mkdir(parents=True)
            router = {"groups": {"5": {"built": True, "trees": [{"tree_id": tree["tree_id"], "entry_node": "rb_labs"}]}}}
            (Path(tmp) / "data" / "shared" / "presentation_router.json").write_text(json.dumps(router), encoding="utf-8")
            return bm.check_presentation_router(Path(tmp), {5: bm.DTContext(gpath5, d, 5)})
    res = router_verdict("rb_document_inventory")
    good = all(l == OK for l, _ in res) and res
    print("  %s  a router entry that is a laboratory screen leading to the gate passes" % ("OK  " if good else "FAIL"))
    bad += 0 if good else 1
    res = router_verdict("rb_labs")
    good = any(l == FAIL and "lab_results" in m and "not a document_inventory" in m for l, m in res)
    print("  %s  broken: a laboratory entry that does not lead to a gate -> FAIL" % ("OK  " if good else "FAIL"))
    bad += 0 if good else 1
    return bad + run_lab_controls(bm)


def lab_node(**over):
    node = {"node_id": "labs", "node_type": "lab_results", "step_label": "Laboratory results", "next_node": "gate",
            "nos_fallback": None, "implies_ticks": {"vocabulary": "evidence_documents", "ids": ["lab"]},
            "labs": [{"id": "afp", "label": "Alpha-fetoprotein (AFP)", "units": ["ng/mL", "IU/mL"]},
                     {"id": "ldh", "label": "Lactate dehydrogenase (LDH)", "units": ["U/L"]}]}
    node.update(over)
    return node


def run_lab_controls(bm):
    FAIL, OK = bm.FAIL, bm.OK
    bad = 0

    def expect(name, node, want, extra=None):
        nonlocal bad
        nodes = {"labs": node}
        nodes.update(extra or {})
        res = bm.check_lab_results(Ctx(nodes), vocabularies=VOC, repo=ROOT)
        good = (all(l == OK for l, _ in res) and res) if want is None else any(l == FAIL and re.search(want, m) for l, m in res)
        print("  %s  %s" % ("OK  " if good else "FAIL", name))
        if not good:
            print("        got: %s" % [(l, m[:110]) for l, m in res][:3])
            bad += 1

    expect("a sound laboratory node passes", lab_node(), None)
    expect("broken: no labs -> FAIL", lab_node(labs=[]), r"non-empty list")
    n = lab_node(); n["labs"][1]["id"] = "afp"
    expect("broken: a duplicate test id -> FAIL", n, r"duplicate id")
    n = lab_node(); n["labs"][0]["id"] = "AFP level"
    expect("broken: an id that is not snake_case -> FAIL", n, r"snake_case")
    n = lab_node(); n["labs"][0]["units"] = []
    expect("broken: a test with no units -> FAIL", n, r"non-empty list of unique")
    n = lab_node(); n["labs"][0]["units"] = ["ng/mL", "ng/mL"]
    expect("broken: a repeated unit -> FAIL", n, r"non-empty list of unique")
    n = lab_node(); del n["next_node"]
    expect("broken: no next_node -> FAIL", n, r"next_node. is required")
    n = lab_node(options=[{"label": "x", "next_node": "gate"}])
    expect("broken: the node carries options, so a value could choose a route -> FAIL", n, r"never chooses the code")
    n = lab_node(resolution_logic=[{"positive": ["x"], "morphology_code": "9060"}])
    expect("broken: the node carries rules that choose a code -> FAIL", n, r"never chooses the code")
    n = lab_node(nos_fallback={"code": "8000"})
    expect("broken: a nos_fallback -> FAIL", n, r"nos_fallback must be null")
    n = lab_node(); n["implies_ticks"]["vocabulary"] = "no_such_list"
    expect("broken: implies_ticks names an unknown vocabulary -> FAIL", n, r"not a router tick vocabulary")
    n = lab_node(); n["implies_ticks"]["ids"] = ["blood_test"]
    expect("broken: implies_ticks names an id the list lacks -> FAIL", n, r"not all in vocabulary")
    other = {"g": {"node_id": "g", "node_type": "morphology_only", "captured_variables": ["afp"], "options": []}}
    expect("broken: a test id is also a captured variable, so a rule could read it -> FAIL", lab_node(), r"captured variable or a `when` key", other)
    return bad


def main():
    print("Engine controls (each breaks one feature in a copy of app.js and runs the engine gate)\n")
    bad = run_engine_controls()
    print("\nData controls (each hands check_tick_lists() a node broken one way)\n")
    bad += run_data_controls()
    print("\n%s" % ("Every control behaves." if not bad else "%d control(s) did not behave." % bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
