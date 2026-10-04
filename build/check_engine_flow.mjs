/* ============================================================================
   check_engine_flow.mjs — the guided flow must deliver what it promises.

   `induce_flow.py` proves every rule has a WITNESS: an answer vector under
   which that rule, and nothing earlier, matches. It proves it against
   `first_match`, which mirrors `matchRules()` — the test the Continue button
   applies. Nothing proved a clerk can ever ENTER such a vector, because what
   gets asked is decided by `nextMarker()`, and `nextMarker()` was in no proof.

   That gap cost a code. Answer a four-marker renal panel negative, negative,
   negative, and the fourth rule was the only one left alive — so the flow
   stopped, with its marker never asked. The screen read "One outcome remains.
   Continue to record it." above a specific code, and Continue recorded the
   node's fallback. The rule had a witness. The flow chart was well formed. The
   data was correct. Every existing check passed.

   Two invariants, both read off the engine's own functions rather than off any
   flag the engine sets:

     A  STRANDING.  When the flow stops with no rule satisfied, no unanswered
        marker may remain that could still satisfy a live rule — or the clerk
        was denied the question that would have changed the code.

     B  HONEST SCREEN.  What the clerk reads when the flow stops must agree
        with what Continue then records. The screen may promise a settled
        outcome only when `matchRules()` actually returns a rule.

   Coverage is two sweeps, because neither alone is enough. The WITNESS sweep
   aims one walk at each rule and so reaches the deep, heavily conditioned rules
   a random walk never would; the EXHAUSTIVE sweep takes every branch of small
   nodes, where the stranding shape lives. Large nodes are sampled to a budget
   and say so — a partial sweep is reported as partial, never as OK.

   Run:  node build/check_engine_flow.mjs
   ========================================================================= */

import fs from 'node:fs';
import path from 'node:path';
import url from 'node:url';
import vm from 'node:vm';

const HERE = path.dirname(url.fileURLToPath(import.meta.url));
const ROOT = path.dirname(HERE);
const DB = path.join(ROOT, 'data', 'database');

const STOP_BUDGET = 3000;      /* stops explored per node, exhaustive sweep */
const COMBO_CAP = 24;
const SHOW = Number(process.env.SHOW || 2);   /* failures printed in full per group */          /* `when` combinations tried per node */

/* ------------------------------------------------------------------ engine */
/* app.js is a browser script with no exports and no dependencies, so it loads
   into a vm context whole and its top-level functions come back as properties
   of that context. The DOM shim exists only to survive the DOMContentLoaded
   listener at the foot of the file; nothing here renders to a screen. */
/* APP= points the check at another copy of the engine. That is how the
   negative control runs: the pre-fix engine is put in a scratch file and swept
   with the same fixtures, which must then FAIL. A check only proved against
   code that passes has not been proved at all. */
const APP = process.env.APP || path.join(ROOT, 'app.js');

function loadEngine() {
  const src = fs.readFileSync(APP, 'utf8');
  const ctx = vm.createContext({
    document: { addEventListener() {}, querySelector: () => null, getElementById: () => null },
    window: {}, console,
    fetch: () => Promise.reject(new Error('the flow check runs offline')),
  });
  vm.runInContext(src, ctx, { filename: APP });
  return ctx;
}

/* ------------------------------------------------------------- the two tests */

/* Could this rule still fire if the clerk were asked the rest of its markers?
   `when` is fixed by the time the node is reached, so an unmatched `when` puts
   the rule out of reach for good. A positive token is reachable while its
   marker is unanswered or already answered the way the token wants; a negative
   name is reachable while that marker is off, which an unanswered marker is. */
function ruleReachable(ctx, r) {
  if (!ctx.whenOk(r.when)) return false;
  const pos = (r.positive || []).every((tok) => {
    const t = ctx.splitToken(tok), have = ctx.state.markers[t.name];
    if (have === undefined) return true;                    /* still askable */
    if (have === 'neg' || have === 'nd') return false;
    return t.want ? have === t.want : true;
  });
  return pos && (r.negative || []).every((name) => ctx.markerOff(name));
}

function fallbackName(ctx, n) {
  try {
    const f = ctx.fallbackTarget(n);
    return f.morphology_code ? f.morphology_code + '/' + (f.behavior_code || '') : 'node ' + f.next_node;
  } catch (e) { return 'NOTHING (' + e.message + ')'; }
}

const hintOf = (html) => { const m = /class="node__hint">([\s\S]*?)<\/p>/.exec(html); return m ? m[1].replace(/<[^>]+>/g, '') : ''; };
const countOf = (html) => { const m = /class="flow__count">([^<]*)</.exec(html); return m ? m[1] : ''; };

/* One stopped flow, judged. Returns failure strings. */
function judge(ctx, n, captured, trail) {
  const fails = [];
  const rule = ctx.matchRules(n.resolution_logic);
  const html = ctx.markerFlow(n);
  const where = n.node_id + '\n       captured ' + (Object.keys(captured).length ? JSON.stringify(captured) : '(none)') +
    '\n       answers  ' + (trail.length ? trail.map((s) => s[0] + '=' + s[1]).join(', ') : '(none)');

  if (!rule) {
    const stranded = ctx.arr(n.resolution_logic).filter((r) => ruleReachable(ctx, r));
    if (stranded.length) {
      fails.push('A  ' + where +
        '\n       flow stopped with no rule satisfied, yet ' + stranded.length + ' rule(s) still reachable: ' +
        stranded.map((r) => (r.morphology_code || r.next_node || r.refer_group || 'rule') + ' needs ' +
          JSON.stringify((r.positive || []).concat((r.negative || []).map((x) => x + ' off')))).join('; ') +
        '\n       Continue records ' + fallbackName(ctx, n));
    }
    if (/One outcome remains/.test(html)) {
      fails.push('B  ' + where +
        '\n       screen reads "' + countOf(html) + '" then "' + hintOf(html) + '"' +
        '\n       but no rule is satisfied — Continue records ' + fallbackName(ctx, n));
    }
  }
  return fails;
}

/* ---------------------------------------------------------------- the sweeps */

function setState(ctx, captured, trail) {
  ctx.state.captured = Object.assign({}, captured);
  ctx.state.markers = {};
  trail.forEach((s) => { ctx.state.markers[s[0]] = s[1]; });
}

/* Every path the clerk can take, to a budget. `nextMarker` picks the question,
   so the branching factor is the answers the node itself offers. */
function sweepExhaustive(ctx, n, captured, budget) {
  const fails = [];
  let stops = 0, capped = false, questions = 0;
  const visit = (trail) => {
    if (stops >= budget) { capped = true; return; }
    setState(ctx, captured, trail);
    const m = ctx.nextMarker(n);
    if (m === null) { stops++; questions += trail.length; fails.push(...judge(ctx, n, captured, trail)); return; }
    if (trail.some((s) => s[0] === m)) { stops++; fails.push('LOOP  ' + n.node_id + ' re-asks ' + m); return; }
    for (const a of ctx.markerAnswers(n, m)) {
      visit(trail.concat([[m, a.v]]));
      if (stops >= budget) { capped = true; return; }
    }
  };
  visit([]);
  return { fails, stops, capped, questions };
}

/* One walk aimed at each rule: answer what the flow asks the way that rule
   needs it, and anything it does not name negative. This is the walk that
   `induce_flow.py`'s witness asserts is possible; here the flow has to produce
   it. Deep conditioned rules are reached this way and no other. */
function sweepWitness(ctx, n) {
  const fails = [];
  let walks = 0;
  for (const r of ctx.arr(n.resolution_logic)) {
    const captured = {};
    for (const [k, v] of Object.entries(r.when || {})) captured[k] = Array.isArray(v) ? v[0] : v;
    const want = {};
    for (const tok of r.positive || []) { const t = ctx.splitToken(tok); want[t.name] = t.want || 'pos'; }
    for (const name of r.negative || []) if (!(name in want)) want[name] = 'neg';

    const trail = [];
    for (let i = 0; i < 64; i++) {
      setState(ctx, captured, trail);
      const m = ctx.nextMarker(n);
      if (m === null) break;
      if (trail.some((s) => s[0] === m)) { fails.push('LOOP  ' + n.node_id + ' re-asks ' + m); break; }
      trail.push([m, want[m] || 'neg']);
    }
    setState(ctx, captured, trail);
    walks++;
    fails.push(...judge(ctx, n, captured, trail));
  }
  return { fails, walks };
}

/* The `when` states a node's own rules name, so the sweep exercises the
   branches the author wrote rather than one empty capture set. */
function capturedCombos(ctx, n, cap) {
  const keys = new Map();
  for (const r of ctx.arr(n.resolution_logic)) {
    for (const [k, v] of Object.entries(r.when || {})) {
      if (!keys.has(k)) keys.set(k, new Set());
      (Array.isArray(v) ? v : [v]).forEach((x) => keys.get(k).add(String(x)));
    }
  }
  let combos = [{}];
  for (const [k, vals] of keys) {
    const next = [];
    /* never captured is a real state, and the one a `when` most often meets */
    for (const base of combos) for (const v of [...vals, undefined]) {
      const c = Object.assign({}, base);
      if (v !== undefined) c[k] = v;
      next.push(c);
    }
    combos = next;
    if (combos.length >= cap) return combos.slice(0, cap);
  }
  return combos;
}

/* ------------------------------------------------------------------ fixtures */
/* The reported defect reduced to the smallest node that shows it: rules that
   each turn on a DIFFERENT single marker, in an order that leaves the
   conditioned one last. Nothing here is Group VI — the shape is the bug. */
const STRANDED = {
  node_id: 'fx_stranded', node_type: 'ihc_checklist', step_label: 'Fixture',
  marker_groups: [{ group_label: 'Panel', markers: ['MARK_A', 'MARK_B', 'MARK_C', 'MARK_GATED'] }],
  branch_sequence: { order: ['MARK_A', 'MARK_B', 'MARK_C', 'MARK_GATED'], intensity_markers: [], rule_count: 4 },
  resolution_logic: [
    { when: { gate: ['on'] }, positive: ['MARK_GATED'], morphology_code: '8311', behavior_code: '3' },
    { positive: ['MARK_A'], morphology_code: '8960', behavior_code: '3' },
    { positive: ['MARK_B'], morphology_code: '8964', behavior_code: '3' },
    { positive: ['MARK_C'], morphology_code: '8510', behavior_code: '3' },
  ],
  nos_fallback: { code: '8000', behavior_code: '3', name: 'Neoplasm, malignant', reason: 'fixture' },
};

/* Two rules, one outcome, neither satisfied — the same defect through the
   other half of the guard, `outcomeCount(live) <= 1`. */
const ONE_OUTCOME = {
  node_id: 'fx_one_outcome', node_type: 'ihc_checklist', step_label: 'Fixture',
  marker_groups: [{ group_label: 'Panel', markers: ['MARK_P', 'MARK_Q'] }],
  branch_sequence: { order: ['MARK_P', 'MARK_Q'], intensity_markers: [], rule_count: 2 },
  resolution_logic: [
    { positive: ['MARK_P'], morphology_code: '8960', behavior_code: '3' },
    { positive: ['MARK_Q'], morphology_code: '8960', behavior_code: '3' },
  ],
  nos_fallback: { code: '8000', behavior_code: '3', name: 'Neoplasm, malignant', reason: 'fixture' },
};

/* A node that IS decided on its first answer. The control that fails if a fix
   buys invariant A by asking every marker every time. */
const SETTLED = {
  node_id: 'fx_settled', node_type: 'ihc_checklist', step_label: 'Fixture',
  marker_groups: [{ group_label: 'Panel', markers: ['MARK_A', 'MARK_B', 'MARK_C', 'MARK_D'] }],
  branch_sequence: { order: ['MARK_A', 'MARK_B', 'MARK_C', 'MARK_D'], intensity_markers: [], rule_count: 4 },
  resolution_logic: [
    { positive: ['MARK_A'], morphology_code: '8960', behavior_code: '3' },
    { positive: ['MARK_B'], morphology_code: '8964', behavior_code: '3' },
    { positive: ['MARK_C'], morphology_code: '8510', behavior_code: '3' },
    { positive: ['MARK_D'], morphology_code: '8311', behavior_code: '3' },
  ],
  nos_fallback: { code: '8000', behavior_code: '3', name: 'Neoplasm, malignant', reason: 'fixture' },
};

/* One scripted walk: answer what the engine asks, then read the screen and
   press Continue. */
function scripted(ctx, n, captured, answers) {
  const trail = [];
  for (let i = 0; i < 40; i++) {
    setState(ctx, captured, trail);
    const m = ctx.nextMarker(n);
    if (m === null) break;
    if (!(m in answers)) throw new Error('asked for unscripted marker ' + m);
    trail.push([m, answers[m]]);
  }
  setState(ctx, captured, trail);
  const rule = ctx.matchRules(n.resolution_logic);
  const target = rule || ctx.fallbackTarget(n);
  const html = ctx.markerFlow(n);
  return {
    asked: trail.map((s) => s[0]),
    code: target.morphology_code + '/' + target.behavior_code,
    viaFallback: !rule,
    promisesOutcome: /One outcome remains/.test(html),
    hint: hintOf(html), count: countOf(html),
  };
}

function fixtures(ctx) {
  const out = [];
  const t = (name, ok, detail) => out.push({ name, ok, detail });
  const eq = (a, b) => JSON.stringify(a) === JSON.stringify(b);

  /* 1 — the defect. Eliminate A, B and C; the gated rule is all that is left
     alive and its marker has never been offered. */
  let r = scripted(ctx, STRANDED, { gate: 'on' }, { MARK_A: 'neg', MARK_B: 'neg', MARK_C: 'neg', MARK_GATED: 'pos' });
  t('the surviving rule\'s marker is asked, not stranded',
    r.asked.includes('MARK_GATED'), 'asked ' + JSON.stringify(r.asked));

  /* 2 — and answering it positive gives the specific code. */
  t('positive on that marker resolves to the specific code',
    r.code === '8311/3' && !r.viaFallback, 'got ' + r.code + (r.viaFallback ? ' via fallback' : ''));

  /* 3 — negative gives the fallback. A fix must not buy invariant A by
     assuming the survivor fires. */
  r = scripted(ctx, STRANDED, { gate: 'on' }, { MARK_A: 'neg', MARK_B: 'neg', MARK_C: 'neg', MARK_GATED: 'neg' });
  t('negative on that marker falls back',
    r.code === '8000/3' && r.viaFallback, 'got ' + r.code + (r.viaFallback ? ' via fallback' : ''));

  /* 4 — and the screen must not have promised otherwise. */
  t('the screen promises no outcome when none is satisfied',
    !r.promisesOutcome, 'screen read "' + r.count + '" then "' + r.hint + '" while Continue records ' + r.code);

  /* 5 — not done or not readable is not a negative test, and resolves no code. */
  r = scripted(ctx, STRANDED, { gate: 'on' }, { MARK_A: 'neg', MARK_B: 'neg', MARK_C: 'neg', MARK_GATED: 'nd' });
  t('not done on that marker falls back',
    r.code === '8000/3' && r.viaFallback && !r.promisesOutcome,
    'got ' + r.code + ', screen "' + r.hint + '"');

  /* 6 — out of gate, the rule is dead and its marker is not worth asking. */
  r = scripted(ctx, STRANDED, { gate: 'off' }, { MARK_A: 'neg', MARK_B: 'neg', MARK_C: 'neg' });
  t('a rule outside its gate is not asked about',
    !r.asked.includes('MARK_GATED') && r.code === '8000/3',
    'asked ' + JSON.stringify(r.asked) + ', got ' + r.code);

  /* 7 — two rules, one outcome, neither satisfied. */
  r = scripted(ctx, ONE_OUTCOME, {}, { MARK_P: 'neg', MARK_Q: 'pos' });
  t('rules sharing one outcome are still asked about',
    r.asked.includes('MARK_Q') && r.code === '8960/3' && !r.viaFallback,
    'asked ' + JSON.stringify(r.asked) + ', got ' + r.code);

  /* 8 — the settled control: first rule satisfied, nothing below it can win,
     so the flow must stop on one question and not walk the panel. */
  r = scripted(ctx, SETTLED, {}, { MARK_A: 'pos' });
  t('a satisfied first rule stops the flow on one question',
    eq(r.asked, ['MARK_A']) && r.code === '8960/3' && !r.viaFallback,
    'asked ' + JSON.stringify(r.asked) + ', got ' + r.code);

  /* 9 — and there the screen must NOT warn of a fallback, because Continue
     delivers a real rule. The control against a fix that makes every stopped
     flow read as unresolved. */
  t('a satisfied rule is not reported as unresolved',
    !/match no rule/.test(r.hint) && !/Continue records 8000/.test(r.hint),
    'screen read "' + r.hint + '"');

  return out;
}

/* ------------------------------------------------------------ express lane */
/* A term the alias index files under more than one group is settled by the
   primary site, never by the index's order and never by asking the clerk for
   a group (registrar, 4 October 2026). Before that day the engine took
   `hit.groups[0]`, so "PPNET" entered Group IV and "RCC" entered Group I
   whatever the site.

   The expected outcome of every (term, topography) pair is computed here
   from alias_index.json and topography_codes.json — the sources of truth —
   and never read off a flag the engine sets. The term's groups that also
   appear in the site's candidate_groups decide it: exactly one enters that
   group with the topography captured; none or several stop the case with
   nothing entered. Each pair is tapped through `handleOption` — alias, organ
   system, region — the handlers the rendered buttons call. The single-group
   terms are the control: a fix that asks every term for its site passes the
   rest and fails this. */
async function expressLane(ctx, out) {
  const SHARED = path.join(ROOT, 'data', 'shared');
  const router = JSON.parse(fs.readFileSync(path.join(SHARED, 'presentation_router.json'), 'utf8'));
  const topo = JSON.parse(fs.readFileSync(path.join(SHARED, 'topography_codes.json'), 'utf8'));
  const index = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'aliases', 'alias_index.json'), 'utf8'));
  for (const name of fs.readdirSync(DB)) {
    const m = /^group_(\d+)_dt\.json$/.exec(name);
    if (m) ctx.groupCache.set(Number(m[1]), { dt: JSON.parse(fs.readFileSync(path.join(DB, name), 'utf8')), aliases: [] });
  }
  const rows = topo.coarse_organ_crosswalk;
  const codes = Object.keys(topo.topography_lookup).filter((c) => rows.some((r) => r.codes.includes(c)));
  const tap = (act, i) => ctx.handleOption(act, { getAttribute: (k) => (k === 'data-i' ? String(i) : null), value: '' });
  const enter = async (term) => {
    ctx.reset();
    ctx.state.router = router; ctx.state.topography = topo; ctx.state.aliasIndex = index; ctx.state.query = term;
    const i = ctx.searchAlias(term).findIndex((h) => h.alias === term);
    if (i < 0) return false;
    await tap('alias', i);
    return true;
  };
  const pickSite = async (code) => {
    const r = ctx.systemRows().findIndex((row) => row.codes.includes(code));
    await tap('site', r);
    if (ctx.state.stage === 'site_region') {
      await tap('site_region', ctx.regionOptions(ctx.state.organSystem).findIndex((o) => o.topography === code));
    }
  };
  const fail = (m) => out.fails.push(m);
  for (const term of Object.keys(index).sort()) {
    const groups = index[term];
    /* A term outranked in the top eight by shorter matches cannot be tapped.
       A single-group one is counted; a multi-group one would go untested, so
       it fails. */
    if (!(await enter(term))) {
      out.skipped++;
      if (groups.length > 1) fail('"' + term + '" ' + JSON.stringify(groups) + ' cannot be reached from the search results');
      continue;
    }
    if (groups.length === 1) {
      out.single++;
      if (ctx.state.stage === 'site' || ctx.state.group !== groups[0]) {
        fail('"' + term + '" ' + JSON.stringify(groups) + ' was asked the site or entered group ' + ctx.state.group);
      }
      continue;
    }
    out.terms++;
    if (ctx.state.stage !== 'site' || ctx.state.group !== null) {
      fail('"' + term + '" ' + JSON.stringify(groups) + ' reached stage ' + ctx.state.stage + ', group ' + ctx.state.group + ', not the site question');
      continue;
    }
    let screen = '';
    try { screen = ctx.renderSite(); } catch (e) { fail('"' + term + '" site screen throws: ' + e.message); continue; }
    if (screen.indexOf(ctx.esc(term)) < 0) fail('"' + term + '" site screen does not name the term');
    for (const code of codes) {
      await enter(term);
      try { await pickSite(code); } catch (e) { fail('"' + term + '" at ' + code + ' throws: ' + e.message); continue; }
      const cg = topo.topography_lookup[code].candidate_groups;
      const expect = Array.isArray(cg) ? groups.filter((g) => cg.includes(g)) : groups.slice();
      const st = ctx.state, at = '"' + term + '" ' + JSON.stringify(groups) + ' at ' + code + ' ' + JSON.stringify(cg);
      if (st.captured.topography !== code) { fail(at + ': topography captured as ' + st.captured.topography); continue; }
      if (expect.length === 1) {
        out.routed++;
        if (st.group !== expect[0] || st.stage === 'search_unresolved') {
          fail(at + ': expected Group ' + expect[0] + ', got stage ' + st.stage + ', group ' + st.group);
        } else if (!st.trail.some((t) => t.label === 'Group')) {
          fail(at + ': entered Group ' + expect[0] + ' with no trail entry');
        }
        continue;
      }
      expect.length ? out.tie++ : out.mismatch++;
      if (st.stage !== 'search_unresolved' || st.group !== null) {
        fail(at + ': expected a stop (' + (expect.length ? 'tie ' + JSON.stringify(expect) : 'no group') + '), got stage ' + st.stage + ', group ' + st.group);
        continue;
      }
      const html = ctx.renderSearchUnresolved();
      if (html.indexOf(ctx.esc(term)) < 0 || html.indexOf(code) < 0) fail(at + ': stop screen does not name the term and the site');
    }
  }

  /* Stepping back. A trail entry restores the snapshot taken when it was
     pushed, and the Tree entry's snapshot is taken after the express lane has
     set its term and group. Two faults lived there, both found by review on
     4 Oct 2026 and both invisible to the walks above, which start every case
     clean:
       R1  rewind a routed express-lane case to its Tree entry and pick a site
           that stops: the stop screen must hold no group, the app bar must
           not name one, and the trail must not keep the earlier site, group
           or tree;
       R2  rewind a single-group express-lane case to its Tree entry and take
           the guided route instead: the case must not carry the search term,
           or the guided site step becomes the express lane's. */
  const expectAt = (groups, code) => {
    const cg = topo.topography_lookup[code].candidate_groups;
    return Array.isArray(cg) ? groups.filter((g) => cg.includes(g)) : groups.slice();
  };
  const rewindTo = async (label) => {
    const i = ctx.state.trail.map((t) => t.label).lastIndexOf(label);
    if (i < 0) return false;
    await tap('rewind', i);
    return true;
  };
  for (const term of Object.keys(index).sort()) {
    const groups = index[term];
    if (groups.length < 2) continue;
    for (const row of rows) {
      const routed = row.codes.find((c) => expectAt(groups, c).length === 1 && ctx.groupMeta(expectAt(groups, c)[0]).tree_routing);
      if (!routed) continue;
      /* Back at the Tree entry the clerk is on this row's region screen, or
         on the organ-system screen when the row holds one code. */
      for (const code of row.codes.length > 1 ? row.codes : codes) {
        await enter(term); await pickSite(routed);
        if (!(await rewindTo('Tree'))) { fail('R1 "' + term + '" at ' + routed + ': routed with no Tree entry'); break; }
        if (ctx.state.stage === 'site_region') {
          await tap('site_region', ctx.regionOptions(ctx.state.organSystem).findIndex((o) => o.topography === code));
        } else {
          await pickSite(code);
        }
        out.rewinds++;
        const expect = expectAt(groups, code), st = ctx.state;
        const at = 'R1 "' + term + '" ' + JSON.stringify(groups) + ' at ' + routed + ', back to Tree, then ' + code;
        /* The trail must describe this case only: the site answered once, and
           no group or tree left over from the case before the step back. */
        const labels = st.trail.map((t) => t.label);
        const twice = ['Organ system', 'Topography'].filter((l) => labels.filter((x) => x === l).length > 1);
        const stale = expect.length === 1 ? [] : labels.filter((l) => l === 'Group' || l === 'Tree');
        if (twice.length || stale.length) {
          fail(at + ': the trail still carries the case before the step back: ' + JSON.stringify(st.trail.map((t) => t.label + ': ' + t.value)));
        }
        if (expect.length === 1) {
          if (st.group !== expect[0]) fail(at + ': expected Group ' + expect[0] + ', got group ' + st.group);
        } else if (st.stage !== 'search_unresolved' || st.group !== null || ctx.contextLabel() !== 'New case') {
          fail(at + ': expected a stop with no group, got stage ' + st.stage + ', group ' + st.group + ', app bar "' + ctx.contextLabel() + '"');
        }
      }
    }
  }
  const singles = Object.keys(index).sort().filter((t) => index[t].length === 1);
  const routedGroups = new Set();
  for (const term of singles) {
    const g = index[term][0];
    if (routedGroups.has(g) || !ctx.groupMeta(g).tree_routing) continue;
    if (!(await enter(term)) || !(await rewindTo('Tree'))) continue;
    routedGroups.add(g);
    await tap('guided', 0);
    for (let k = 0; k < 8 && ['archetype', 'discriminator', 'site', 'site_region'].includes(ctx.state.stage); k++) {
      await tap(ctx.state.stage, 0);
    }
    out.rewinds++;
    if (ctx.state.searchTerm || ctx.state.stage === 'search_unresolved') {
      fail('R2 "' + term + '" [' + g + '], back to Tree, then the guided route: the case still carries the search term (stage ' +
        ctx.state.stage + ', term ' + JSON.stringify(ctx.state.searchTerm) + ')');
    }
  }
  if (!routedGroups.size) fail('R2 found no single-group term whose group routes its tree — the scenario did not run');

  /* R3  the guided route, same defect: a tree routed from the topography is
         an automatic trail entry. Every presentation × organ system is walked
         (first option wherever a choice remains); where a Tree entry appears,
         the clerk steps back to it and answers again, and the trail must not
         hold the earlier answers twice. */
  let guidedRewinds = 0;
  /* A screen with an option to tap. An unbuilt group's handoff is a banner. */
  const asks = (st) => ['discriminator', 'site_region', 'group'].includes(st) ||
    (st === 'handoff' && ctx.groupMeta(ctx.state.group).built && !!ctx.groupMeta(ctx.state.group).tree_selection);
  const walk = async (a, r) => {
    ctx.reset(); ctx.state.router = router; ctx.state.topography = topo; ctx.state.aliasIndex = index;
    await tap('guided', 0); await tap('archetype', a);
    for (let k = 0; k < 8 && ctx.state.stage !== 'node'; k++) {
      const st = ctx.state.stage;
      if (st === 'site') await tap('site', r);
      else if (asks(st)) await tap(st, 0);
      else break;
    }
  };
  for (let a = 0; a < router.archetypes.length; a++) {
    await walk(a, 0);
    const nrows = ctx.state.archetype ? ctx.systemRows().length : 0;
    for (let r = 0; r < nrows; r++) {
      await walk(a, r);
      const trail = ctx.state.trail, t = trail.map((x) => x.label).lastIndexOf('Tree');
      /* Routed, by the router's own declaration — not by any flag the engine
         keeps on the trail entry. */
      if (t < 0 || !ctx.groupMeta(ctx.state.group).tree_routing) continue;
      await tap('rewind', t);
      for (let k = 0; k < 8 && ctx.state.stage !== 'node'; k++) {
        const st = ctx.state.stage;
        if (st === 'site' || asks(st)) await tap(st, st === 'site' ? r : 0);
        else break;
      }
      guidedRewinds++;
      const labels = ctx.state.trail.map((x) => x.label);
      const twice = [...new Set(labels)].filter((l) => labels.filter((x) => x === l).length > 1);
      if (twice.length) {
        fail('R3 guided, presentation ' + a + ', organ system ' + r + ', back to Tree and answered again: the trail holds ' +
          twice.join(', ') + ' twice: ' + JSON.stringify(ctx.state.trail.map((x) => x.label + ': ' + x.value)));
      }
    }
  }
  if (!guidedRewinds) fail('R3 found no guided case with a routed tree — the scenario did not run');
  out.rewinds += guidedRewinds;
  return out;
}

/* ---------------------------------------------------------------------- main */
const ctx = loadEngine();
let bad = 0, partial = 0;

console.log('Fixtures — the defect, and the controls that keep a fix honest\n');
for (const r of fixtures(ctx)) {
  console.log('  %s  %s', r.ok ? 'OK  ' : 'FAIL', r.name);
  if (!r.ok) { console.log('        ' + r.detail); bad++; }
}

console.log('\nExpress lane — a term filed under several groups is settled by the site\n');
{
  /* An engine that throws inside a scenario fails the section by name rather
     than ending the run with a stack trace. */
  const r = { routed: 0, mismatch: 0, tie: 0, single: 0, terms: 0, skipped: 0, rewinds: 0, fails: [] };
  try { await expressLane(ctx, r); } catch (e) { r.fails.push('the engine threw: ' + e.message); }
  console.log('  %s  %d multi-group term(s) x every site: %d routed to one group, %d stopped (no group), %d stopped (tie); %d single-group term(s) enter their group; %d stepped-back case(s); %d term(s) not reachable from the results',
    r.fails.length ? 'FAIL' : 'OK  ', r.terms, r.routed, r.mismatch, r.tie, r.single, r.rewinds, r.skipped);
  for (const f of r.fails.slice(0, Math.max(SHOW, 5))) console.log('        ' + f);
  if (r.fails.length > Math.max(SHOW, 5)) console.log('        ... and ' + (r.fails.length - Math.max(SHOW, 5)) + ' more');
  bad += r.fails.length;
}

console.log('\nSweep — every ihc_checklist node in every group\n');
for (const name of fs.readdirSync(DB).sort()) {
  if (!name.endsWith('_dt.json')) continue;
  const data = JSON.parse(fs.readFileSync(path.join(DB, name), 'utf8'));
  ctx.state.dt = data;
  let nodes = 0, stops = 0, walks = 0, fails = [], capped = [];
  for (const tree of data.decision_trees || []) {
    for (const n of tree.nodes || []) {
      if (n.node_type !== 'ihc_checklist') continue;
      nodes++;
      const w = sweepWitness(ctx, n);
      walks += w.walks; fails = fails.concat(w.fails);
      const combos = capturedCombos(ctx, n, COMBO_CAP);
      const per = Math.max(50, Math.floor(STOP_BUDGET / combos.length));
      let nodeCapped = false;
      for (const captured of combos) {
        const e = sweepExhaustive(ctx, n, captured, per);
        stops += e.stops; fails = fails.concat(e.fails); nodeCapped = nodeCapped || e.capped;
      }
      if (nodeCapped) capped.push(n.node_id);
    }
  }
  const uniq = [...new Set(fails)];
  const byInv = (k) => uniq.filter((f) => f.startsWith(k)).length;
  const nodesTouched = [...new Set(uniq.map((f) => (/^\w+\s+(\S+)/.exec(f) || [])[1]))];
  console.log('  ' + name.padEnd(20) + String(nodes).padStart(3) + ' node(s)  ' +
    String(walks).padStart(4) + ' witness walk(s)  ' + String(stops).padStart(6) + ' stop(s)  ' +
    (uniq.length ? 'FAIL  A:' + byInv('A') + '  B:' + byInv('B') : 'OK'));
  if (uniq.length) console.log('     nodes affected: ' + nodesTouched.join(', '));
  for (const f of uniq.slice(0, SHOW)) console.log('     FAIL  ' + f);
  if (uniq.length > SHOW) console.log('     ... and ' + (uniq.length - SHOW) + ' more of the same shape');
  if (capped.length) {
    console.log('     note: sampled to budget, coverage partial: ' + capped.join(', '));
    partial += capped.length;
  }
  bad += uniq.length;
}

console.log('');
if (partial) console.log(partial + ' node(s) swept to a budget rather than exhaustively.');
console.log(bad ? bad + ' failure(s).' : 'Every stopped flow delivers what the screen promised.');
process.exit(bad ? 1 : 0);
