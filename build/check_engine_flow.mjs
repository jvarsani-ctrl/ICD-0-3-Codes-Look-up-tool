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

/* ---------------------------------------------------------------------- main */
const ctx = loadEngine();
let bad = 0, partial = 0;

console.log('Fixtures — the defect, and the controls that keep a fix honest\n');
for (const r of fixtures(ctx)) {
  console.log('  %s  %s', r.ok ? 'OK  ' : 'FAIL', r.name);
  if (!r.ok) { console.log('        ' + r.detail); bad++; }
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
