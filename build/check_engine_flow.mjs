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
const ONLY = process.env.ONLY || '';   /* ONLY=ux runs the tick-list, Home, filter, result-block and hop section alone */
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

/* A document small enough to stand in for the page. It keeps what render() writes
   into it and records where the keyboard focus was sent, so the screens the
   engine draws and the listeners it registers can be driven without a browser.
   `live` loads the real data files from disk, boots the engine and fires
   DOMContentLoaded, so the delegated listeners are registered and can be handed
   synthetic events. */
function fakeDom() {
  const dom = { focused: [], active: null, appListeners: {}, docListeners: {} };
  const mk = (id) => ({
    id, innerHTML: '', textContent: '', hidden: false, attrs: {},
    setAttribute(k, v) { this.attrs[k] = v; },
    querySelector(sel) {
      if (sel === '.exitbar') return this.innerHTML.includes('class="exitbar"') ? { getBoundingClientRect: () => ({ bottom: 0 }) } : null;
      return null;
    },
  });
  dom.els = {};
  ['app', 'appbar-context', 'appbar-home', 'rail', 'trail-rows', 'slot'].forEach((id) => { dom.els[id] = mk(id); });
  dom.appEl = { addEventListener(type, fn) { (dom.appListeners[type] = dom.appListeners[type] || []).push(fn); } };
  dom.document = {
    addEventListener(type, fn) { dom.docListeners[type] = fn; },
    getElementById: (id) => dom.els[id] || null,
    querySelector: (sel) => (sel === '.app' ? dom.appEl : { focus() { dom.focused.push(sel); } }),
    get activeElement() { return dom.active; },
  };
  return dom;
}
function loadEngine(live) {
  const src = fs.readFileSync(APP, 'utf8');
  const dom = fakeDom();
  const fromDisk = (p) => new Promise((resolve, reject) => {
    const f = path.join(ROOT, p);
    if (!fs.existsSync(f)) return reject(new Error('no such file: ' + p));
    resolve({ ok: true, json: () => Promise.resolve(JSON.parse(fs.readFileSync(f, 'utf8'))) });
  });
  const ctx = vm.createContext({
    document: dom.document,
    window: { location: { search: '' } }, console, URLSearchParams,
    fetch: live ? fromDisk : () => Promise.reject(new Error('the flow check runs offline')),
  });
  vm.runInContext(src, ctx, { filename: APP });
  ctx.__dom = dom;
  if (live) dom.docListeners.DOMContentLoaded();
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
   system, region — the handlers the rendered buttons call.

   A term filed under ONE group is asked its site too when that group's data
   reads the site — the router routes its trees from the topography, or a
   `when` in its trees names `topography` — computed here from the router and
   the group files, not from the engine (registrar, 4 October 2026). Without
   the site those rules fail open: "Rhabdoid tumour", a Group IX-only
   spelling, coded a renal rhabdoid tumour in Group IX. The single-group terms
   of a group that reads no site are the control: a fix that asks every term
   for its site passes the rest and fails this. */
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
  const hasSiteWhen = (o) => !!o && typeof o === 'object' && (Array.isArray(o) ? o.some(hasSiteWhen) :
    ((o.when && typeof o.when === 'object' && o.when.topography !== undefined) || Object.values(o).some(hasSiteWhen)));
  const readsSite = (g) => {
    const meta = (router.groups || {})[String(g)] || {};
    if (!meta.built) return false;
    if (meta.tree_routing) return true;
    const c = ctx.groupCache.get(g);
    return !!c && hasSiteWhen(c.dt.decision_trees);
  };
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
    if (groups.length === 1 && !readsSite(groups[0])) {
      out.single++;
      if (ctx.state.stage === 'site' || ctx.state.group !== groups[0]) {
        fail('"' + term + '" ' + JSON.stringify(groups) + ' was asked the site or entered group ' + ctx.state.group);
      }
      continue;
    }
    groups.length > 1 ? out.terms++ : out.siteSingles++;
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
    if (!(await enter(term))) continue;
    /* A routed group reads the site, so its term is asked it first: answer
       with a site that keeps the group, then step back to the Tree entry. */
    if (ctx.state.stage === 'site') {
      const keep = codes.find((c) => expectAt([g], c).length === 1);
      if (!keep) continue;
      await pickSite(keep);
    }
    if (!(await rewindTo('Tree'))) continue;
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

/* ------------------------------------- UX: tick lists, Home, filter, hop, result block */
/* Registrar, 6 October 2026. Everything here drives the handlers the rendered
   buttons call and reads the screens the engine draws. The expected outcome of
   every real tick-list node is computed here from the JSON by a SECOND
   implementation of the fit rule (a Set-based one, not app.js's), so the engine
   is judged against the data's own declaration and never against a flag it keeps.

   Two kinds of evidence:
     SWEEP    every tick-list node in every group, every ticked set (2^n), every
              special situation: the clerk is never stranded, the destination is
              the one the data declares, and a screen that asks a second question
              lists exactly the tiers that fit.
     FIXTURES small nodes that exercise what no group uses yet (first_match, the
              recognition aid) and the screens that belong to no group (Home, the
              filter, the coding block, the referral hop). */
async function uxScenarios(ctx) {
  const SHARED = path.join(ROOT, 'data', 'shared');
  const router = JSON.parse(fs.readFileSync(path.join(SHARED, 'presentation_router.json'), 'utf8'));
  const topo = JSON.parse(fs.readFileSync(path.join(SHARED, 'topography_codes.json'), 'utf8'));
  const dts = new Map();
  for (const name of fs.readdirSync(DB).sort()) {
    const m = /^group_(\d+)_dt\.json$/.exec(name);
    if (m) dts.set(Number(m[1]), JSON.parse(fs.readFileSync(path.join(DB, name), 'utf8')));
  }
  for (const [g, dt] of dts) ctx.groupCache.set(g, { dt, aliases: [] });
  const rows = [];
  /* A throw inside the engine is remembered and attached to the next check, which
     then fails on its own assertion. Without this the first throw ended the whole
     section and a broken engine never named the check that should have caught it
     (found by the negative controls, 6 October 2026). */
  let thrown = '';
  const t = (name, ok, detail) => { rows.push({ name, ok: !!ok, detail: ok ? '' : detail + (thrown ? ' [the engine threw: ' + thrown + ']' : '') }); thrown = ''; };
  const fakeEl = (attrs, extra) => Object.assign({ getAttribute: (k) => (attrs && k in attrs ? String(attrs[k]) : null), value: '', checked: false, type: 'button' }, extra || {});
  const tap = async (act, i, extra) => { try { return await ctx.handleOption(act, fakeEl(i === undefined ? {} : { 'data-i': i }, extra)); } catch (e) { thrown = e.message; } };
  const rend = (fn) => { try { return fn(); } catch (e) { thrown = e.message; return ''; } };
  /* A radio or text value on the draft, through the handler the control calls. */
  const draftSet = async (k, value, type) => { try { await ctx.handleOption('draft', fakeEl({ 'data-k': k }, { value, type: type || 'radio' })); } catch (e) { thrown = e.message; } };
  /* One box on a checklist, ticked or unticked, through the handler the box calls. */
  const tick = async (id, checked) => { try { await ctx.handleOption('tick', fakeEl({ 'data-id': id }, { type: 'checkbox', checked })); } catch (e) { thrown = e.message; } };
  /* The set S on screen: every box ticked in reverse order, then those outside S unticked, so
     both branches of the handler run and the order they were ticked in is not the drawn order. */
  const tickSet = async (all, S) => {
    for (const id of all.slice().reverse()) await tick(id, true);
    for (const id of all) if (!S.has(id)) await tick(id, false);
  };
  const begin = (dt, treeId, nodeId, topography) => {
    ctx.reset();
    Object.assign(ctx.state, { router, topography: topo, dt, treeId, nodeId, stage: 'node', aliasIndex: {} });
    ctx.state.captured = topography ? { topography } : {};
    ctx.state.trailAtGroupEntry = 0;
  };
  const fit = (tk, S) => {
    const r = tk.requires || [], a = tk.any_of || [], e = tk.excludes || [];
    return r.every((x) => S.has(x)) && (!a.length || a.some((x) => S.has(x))) && !e.some((x) => S.has(x));
  };
  const items = (n) => {
    const tl = n.tick_list, voc = tl.vocabulary ? router.tick_vocabularies[tl.vocabulary] : {};
    return (tl.items || voc.items).map((x) => x.id);
  };
  const behaviorTextOf = (b) => ({ '0': '/0 (Benign neoplasm)', '1': '/1 (Uncertain whether benign or malignant)', '3': '/3 (Malignant)' })[b];
  const countButtons = (html, act) => (html.match(new RegExp('data-act="' + act + '"', 'g')) || []).length;
  /* Did the case arrive where the option says it goes? A branch that parks a behaviour or grade
     question, or whose destination a resource gate diverts, is judged only on having left the gate. */
  const left = (n, o) => {
    const st = ctx.state, gone = !(st.stage === 'node' && st.nodeId === n.node_id);
    if (!gone) return false;
    if (o.behaviour_resolution) return st.stage === 'behaviour';
    if (o.grade_resolution) return st.stage === 'grade';
    if (o.resource_level_gate) return true;
    if (o.next_node) {
      const dest = (n.__tree || []).find((x) => x.node_id === o.next_node);
      if (dest && dest.resource_level_gate) return true;
      return st.stage === 'node' && st.nodeId === o.next_node;
    }
    return st.stage !== 'node';
  };

  /* ---- SWEEP: every real tick-list node -------------------------------- */
  let nodes = 0, sets = 0, failsSweep = [];
  for (const [g, dt] of dts) {
    for (const tree of dt.decision_trees) for (const n of tree.nodes) {
      if (!n.tick_list) continue;
      nodes++;
      n.__tree = tree.nodes;
      const ids = items(n), mode = n.tick_list.resolve || 'ask_siblings';
      const tiers = n.options.map((o, i) => ({ o, i })).filter((x) => x.o.ticks);
      const ctxs = n.options.map((o, i) => ({ o, i })).filter((x) => !x.o.ticks);
      const where = 'group ' + g + ' ' + n.node_id;
      for (let mask = 0; mask < (1 << ids.length); mask++) {
        const S = new Set(ids.filter((_, b) => mask >> b & 1)), list = ids.filter((x) => S.has(x));
        sets++;
        const expected = tiers.filter((x) => fit(x.o.ticks, S));
        const shown = mode === 'first_match' ? expected.slice(0, 1) : expected;
        const setText = '{' + (list.join(', ') || 'nothing') + '}';
        if (!shown.length) { failsSweep.push(where + ': ' + setText + ' fits no option'); continue; }
        try {
          begin(dt, tree.tree_id, n.node_id, 'C40.2');
          const screenA = rend(() => ctx.renderLiveNode());
          if (countButtons(screenA, 'tick-continue') !== 1) failsSweep.push(where + ': the checklist screen has no single Continue');
          await tickSet(ids, S);
          await tap('tick-continue');
          if (shown.length === 1) {
            if (!left(n, shown[0].o)) failsSweep.push(where + ': ' + setText + ' should take [' + shown[0].i + '] and did not leave the gate');
            else if (shown[0].o.next_node && ctx.state.captured[n.tick_list.variable || router.tick_vocabularies[n.tick_list.vocabulary].variable].join() !== list.join()) {
              failsSweep.push(where + ': the ticks were not kept on the case');
            }
          } else {
            const html = rend(() => ctx.renderLiveNode());
            if (ctx.state.captured.tick_gate !== n.node_id || countButtons(html, 'tickopt') !== shown.length) {
              failsSweep.push(where + ': ' + setText + ' fits ' + shown.length + ' tiers but the second screen offers ' + countButtons(html, 'tickopt'));
            } else {
              const pick = shown[shown.length - 1];
              await tap('tickopt', shown.length - 1);
              if (!left(n, pick.o)) failsSweep.push(where + ': ' + setText + ' second screen did not take [' + pick.i + ']');
            }
          }
        } catch (e) { failsSweep.push(where + ': ' + setText + ' threw ' + e.message); }
      }
      if (mode === 'ask_siblings') {
        for (let k = 0; k < ctxs.length; k++) {
          try {
            begin(dt, tree.tree_id, n.node_id, 'C40.2');
            await tickSet(ids, new Set([ids[0]]));
            await draftSet('ctx', String(k + 1));
            await tap('tick-continue');
            const kept = ctx.state.captured[n.tick_list.variable || router.tick_vocabularies[n.tick_list.vocabulary].variable];
            if (!left(n, ctxs[k].o)) failsSweep.push(where + ': special situation [' + ctxs[k].i + '] did not route');
            else if (!kept || kept.join() !== ids[0]) failsSweep.push(where + ': special situation [' + ctxs[k].i + '] did not keep the ticks on the case');
          } catch (e) { failsSweep.push(where + ': special situation [' + ctxs[k].i + '] threw ' + e.message); }
        }
      }
    }
  }
  t('tick lists in the data: ' + nodes + ' node(s), ' + sets + ' ticked set(s), every destination as declared' +
    (nodes ? '' : ' (none in the data yet)'), !failsSweep.length, failsSweep.slice(0, 4).join('\n        ') + (failsSweep.length > 4 ? '\n        ... and ' + (failsSweep.length - 4) + ' more' : ''));

  /* ---- FIXTURE: the evidence gate, Group 10's shape ---------------------- */
  const stub = (id) => ({ node_id: id, node_type: 'morphology_only', step_label: id, question: id, options: [{ label: id + ' answer', morphology_code: '8000', behavior_code: '3' }], nos_fallback: { code: '8000', behavior_code: '3', name: 'x', reason: 'x' } });
  const evid = {
    node_id: 'fx_gate', node_type: 'document_inventory', step_label: 'Evidence in file', question: 'What is in the file?', hint: 'h',
    tick_list: { vocabulary: 'evidence_documents', resolve: 'ask_siblings' }, nos_fallback: null,
    options: [
      { label: 'Referral only', next_node: 'fx_referral', ticks: { excludes: ['imaging', 'cytology', 'histology', 'ihc', 'genetics'] } },
      { label: 'Imaging and markers', next_node: 'fx_markers', ticks: { requires: ['imaging', 'lab'], excludes: ['cytology', 'histology', 'ihc', 'genetics'] } },
      { label: 'Imaging only', next_node: 'fx_imaging', ticks: { requires: ['imaging'], excludes: ['lab', 'cytology', 'histology', 'ihc', 'genetics'] } },
      { label: 'Cytology only', next_node: 'fx_cytology', ticks: { requires: ['cytology'], excludes: ['histology', 'ihc', 'genetics'] } },
      { label: 'Histology plain', next_node: 'fx_histology', ticks: { requires: ['histology'], excludes: ['ihc', 'genetics'] } },
      { label: 'Histology with stains', next_node: 'fx_stains', ticks: { any_of: ['ihc', 'genetics'] } },
      { label: 'Histology with other stains', next_node: 'fx_stains2', ticks: { any_of: ['ihc', 'genetics'] } },
      { label: 'Specimen inadequate', next_node: 'fx_inadequate' },
    ],
  };
  const fxDt = { morphology_entries: [], decision_trees: [{ tree_id: 'fx', entry_node: 'fx_gate', nodes: [evid, ...['fx_referral', 'fx_markers', 'fx_imaging', 'fx_cytology', 'fx_histology', 'fx_stains', 'fx_stains2', 'fx_inadequate'].map(stub)] }] };
  const run = async (ticks, ctxIdx) => {
    begin(fxDt, 'fx', 'fx_gate', 'C56.9');
    ctx.state.draft.ticks = ticks.slice();
    if (ctxIdx) ctx.state.draft.ctx = String(ctxIdx);
    await tap('tick-continue');
    return ctx.state;
  };
  begin(fxDt, 'fx', 'fx_gate', 'C56.9');
  const screenA = rend(() => ctx.renderLiveNode());
  const DOCS = ['Referral Letter/Clinical Note', 'Imaging Report', 'Lab Report', 'Cytology', 'Histology Report', 'IHC Report', 'Gene reports for cancer'];
  t('the checklist shows the seven documents in the registrar\'s words, and one Continue',
    DOCS.every((d) => screenA.includes('> ' + d + '</label>')) && countButtons(screenA, 'tick') === 7 && countButtons(screenA, 'tick-continue') === 1,
    'the screen is missing a document or a Continue');
  t('a special situation is offered under the boxes, defaulting to none', /None of these/.test(screenA) && /Specimen inadequate/.test(screenA), 'no context list');
  t('the context list carries its own filter box', countButtons(screenA, 'filter') === 1, 'filter boxes: ' + countButtons(screenA, 'filter'));
  let st = await run(['imaging', 'lab']);
  t('imaging and a lab report take the markers tier, automatically', st.nodeId === 'fx_markers' && st.trail[st.trail.length - 1].automatic === true, 'went to ' + st.nodeId);
  st = await run(['imaging']);
  t('imaging alone takes the imaging tier', st.nodeId === 'fx_imaging', 'went to ' + st.nodeId);
  st = await run(['ihc']);
  t('an IHC report alone still means tissue: it takes a histology tier', ['fx_stains', 'fx_histology'].includes(st.nodeId) || st.captured.tick_gate === 'fx_gate', 'went to ' + st.nodeId);
  st = await run([]);
  t('nothing ticked takes the lowest tier', st.nodeId === 'fx_referral', 'went to ' + st.nodeId);
  st = await run(['histology', 'ihc']);
  t('two tiers fit histology with stains: a second question lists exactly those two',
    st.captured.tick_gate === 'fx_gate' && countButtons(rend(() => ctx.renderLiveNode()), 'tickopt') === 2, 'gate ' + st.captured.tick_gate);
  await tap('tickopt', 1);
  t('the second question takes the tier tapped', ctx.state.nodeId === 'fx_stains2' && !ctx.state.captured.tick_gate, 'went to ' + ctx.state.nodeId);
  st = await run(['histology', 'ihc'], 1);
  t('a special situation routes at once, whatever is ticked', st.nodeId === 'fx_inadequate', 'went to ' + st.nodeId);
  await run(['imaging']);
  t('a tier the engine takes by itself stays out of "Suggested based on", which lists the documents ticked',
    /Imaging Report/.test(ctx.basisFromTrail()) && !/Imaging only/.test(ctx.basisFromTrail()) && /Imaging only/.test(ctx.state.trail.map((x) => x.value).join('|')),
    'basis: ' + ctx.basisFromTrail());
  await run(['histology', 'ihc']); await tap('tickopt', 1);
  t('a tier the clerk picks on the second screen is their answer and stays in "Suggested based on"',
    /Histology with other stains/.test(ctx.basisFromTrail()), 'basis: ' + ctx.basisFromTrail());
  {
    await run(['imaging', 'lab']);
    const trail = ctx.state.trail.map((x) => x.label + ': ' + x.value);
    t('the trail names the documents ticked, then the tier taken', /Imaging Report, Lab Report/.test(trail.join(' | ')) && ctx.state.trail.length === 2, JSON.stringify(trail));
    await tap('rewind', 1);
    const again = rend(() => ctx.renderLiveNode());
    t('stepping back to the tier taken automatically shows the checklist, with the documents ticked as they were',
      ctx.state.nodeId === 'fx_gate' && !ctx.state.captured.tick_gate && ctx.state.trail.length === 0 && (ctx.state.draft.ticks || []).join() === 'imaging,lab' && (again.match(/data-act="tick" data-id="[a-z]+" checked/g) || []).length === 2,
      'node ' + ctx.state.nodeId + ', trail ' + ctx.state.trail.length + ', draft ' + JSON.stringify(ctx.state.draft.ticks));
  }
  {
    begin(fxDt, 'fx', 'fx_gate', 'C56.9');
    ctx.state.captured.documents_in_file = ['cytology'];
    const prefilled = rend(() => ctx.renderLiveNode());
    t('a second gate in the same case opens with the documents already ticked', (prefilled.match(/data-act="tick" data-id="[a-z]+" checked/g) || []).length === 1 && /data-id="cytology" checked/.test(prefilled), 'not prefilled');
  }

  /* ---- FIXTURE: first_match, the mixed-tumour shape ---------------------- */
  const mixed = {
    node_id: 'fx_mixed', node_type: 'histology_subclassification', step_label: 'Components', question: 'Which components does the report list?', nos_fallback: null,
    tick_list: { resolve: 'first_match', variable: 'mixed_components', label: 'Components', prompt: 'Tick every component.',
      items: [{ id: 'choriocarcinoma', label: 'Choriocarcinoma' }, { id: 'embryonal', label: 'Embryonal carcinoma' }, { id: 'teratoma', label: 'Teratoma' }, { id: 'germinoma', label: 'Germinoma' }, { id: 'yolk', label: 'Yolk sac tumour' }] },
    options: [
      { label: 'Choriocarcinoma among them', next_node: 'fx_a', ticks: { requires: ['choriocarcinoma'] } },
      { label: 'Embryonal carcinoma and teratoma only', next_node: 'fx_b', ticks: { requires: ['embryonal', 'teratoma'], excludes: ['choriocarcinoma', 'germinoma', 'yolk'] } },
      { label: 'Teratoma with germinoma', next_node: 'fx_c', ticks: { requires: ['teratoma', 'germinoma'] } },
      { label: 'Anything else', next_node: 'fx_d', ticks: {} },
    ],
  };
  const mixDt = { morphology_entries: [], decision_trees: [{ tree_id: 'fx', entry_node: 'fx_mixed', nodes: [mixed, ...['fx_a', 'fx_b', 'fx_c', 'fx_d'].map(stub)] }] };
  const runMix = async (ticks) => { begin(mixDt, 'fx', 'fx_mixed', 'C62.9'); ctx.state.draft.ticks = ticks; await tap('tick-continue'); return ctx.state.nodeId; };
  const table = [[['choriocarcinoma', 'teratoma'], 'fx_a'], [['embryonal', 'teratoma'], 'fx_b'], [['embryonal', 'teratoma', 'yolk'], 'fx_d'],
    [['teratoma', 'germinoma'], 'fx_c'], [['yolk'], 'fx_d'], [[], 'fx_d'], [['embryonal', 'teratoma', 'choriocarcinoma'], 'fx_a']];
  const gotMix = [];
  for (const [ticks, want] of table) gotMix.push([ticks, want, await runMix(ticks)]);
  t('first_match: the first fitting option is the destination, in file order',
    gotMix.every((r) => r[1] === r[2]), gotMix.filter((r) => r[1] !== r[2]).map((r) => '{' + r[0].join(', ') + '} wanted ' + r[1] + ', got ' + r[2]).join('; '));
  t('first_match: no context list and no second screen', !/None of these/.test((begin(mixDt, 'fx', 'fx_mixed'), rend(() => ctx.renderLiveNode()))), 'a context list was drawn');

  /* ---- FIXTURE: the recognition aid ------------------------------------- */
  const aided = {
    node_id: 'fx_aid', node_type: 'histology_subclassification', step_label: 'Tumour type', question: 'What does the report call it?', nos_fallback: null,
    options: [
      { label: 'Seminoma', next_node: 'fx_a', recognition_aid: 'sheets of clear cells divided by fibrous septa' },
      { label: 'Embryonal carcinoma', next_node: 'fx_b', recognition_aid: 'crowded primitive cells in glands and papillae' },
      { label: 'Teratoma', next_node: 'fx_c' },
    ],
  };
  const aidDt = { morphology_entries: [], decision_trees: [{ tree_id: 'fx', entry_node: 'fx_aid', nodes: [aided, ...['fx_a', 'fx_b', 'fx_c'].map(stub)] }] };
  begin(aidDt, 'fx', 'fx_aid', 'C62.9');
  let aidHtml = rend(() => ctx.renderLiveNode());
  t('a list with recognition aids shows none until an option is selected, and Confirm is disabled',
    !/sheets of clear cells/.test(aidHtml) && /data-act="optconfirm" disabled/.test(aidHtml), 'aid shown early or Confirm enabled');
  await tap('optsel', 1);
  aidHtml = rend(() => ctx.renderLiveNode());
  t('selecting shows that option\'s aid, in bold, and only that one',
    /crowded primitive cells/.test(aidHtml) && !/sheets of clear cells/.test(aidHtml) && /opt--selected/.test(aidHtml) && !/data-act="optconfirm" disabled/.test(aidHtml) && ctx.state.nodeId === 'fx_aid',
    'selection did not show its aid alone');
  await tap('optconfirm');
  t('Confirm takes the selected option', ctx.state.nodeId === 'fx_b', 'went to ' + ctx.state.nodeId);
  begin(evid.options ? fxDt : fxDt, 'fx', 'fx_cytology');
  begin(aidDt, 'fx', 'fx_aid', 'C62.9');
  t('a list with no aids stays one tap: no Confirm', (() => { begin(fxDt, 'fx', 'fx_inadequate'); return !/optconfirm/.test(rend(() => ctx.renderLiveNode())); })(), 'Confirm drawn on a list without aids');

  /* ---- numeric_gate: one sentence for every kind of unit ----------------------- */
  {
    const gateFor = (unit) => ({ node_id: 'fx_num', node_type: 'numeric_gate', step_label: 'Reading', variable: 'v', variable_label: 'Reading',
      bands: [{ unit, range: '0-10', next_node: 'fx_a' }], nos_fallback: null });
    const say = (unit) => { begin(fxDt, 'fx', 'fx_gate'); ctx.state.draft = {}; return rend(() => ctx.numericGate(gateFor(unit))); };
    const count = say('per_mm2'), conc = say('ng_per_ml'), pct = say('percent');
    const sentence = (h) => (/<p class="node__hint">(Thresholds[^<]*)<\/p>/.exec(h) || [])[1] || '';
    t('the unit sentence no longer says "count" or "denominator" about a concentration, and still covers a count',
      /same unit/.test(sentence(conc)) && !/entering the count/.test(sentence(conc)) && /same denominator/.test(sentence(count)) && /same unit/.test(sentence(pct)),
      'conc: ' + sentence(conc) + ' | count: ' + sentence(count));
  }

  /* ---- Laboratory results ---------------------------------------------------------- */
  /* The numbers are recorded and shown and nothing more: kept outside `captured`,
     so no rule can read one, and left out of "Suggested based on". */
  {
    const labNode = {
      node_id: 'fx_labs', node_type: 'lab_results', step_label: 'Laboratory results', question: 'Which laboratory results are in the file?', hint: 'h',
      implies_ticks: { vocabulary: 'evidence_documents', ids: ['lab'] }, nos_fallback: null, next_node: 'fx_gate',
      labs: [{ id: 'afp', label: 'Alpha-fetoprotein (AFP)', units: ['ng/mL', 'IU/mL'] }, { id: 'ldh', label: 'Lactate dehydrogenase (LDH)', units: ['U/L'] }, { id: 'ca', label: 'Calcium', units: ['mmol/L', 'mg/dL'] }],
    };
    const labDt = { morphology_entries: [], decision_trees: [{ tree_id: 'fx', entry_node: 'fx_labs', nodes: [labNode, ...fxDt.decision_trees[0].nodes] }] };
    const startLabs = () => { begin(labDt, 'fx', 'fx_labs', 'C56.9'); ctx.state.trailAtGroupEntry = 0; };
    const typeRow = async (i, value, unit) => {
      await tap('labval', i, { value });
      if (unit) await tap('labunit', i, { value: unit });
    };
    startLabs();
    const screen = rend(() => ctx.renderLiveNode());
    t('the laboratory screen has a row per test, each with a unit list and an EMPTY Not in the file box, and no escapes',
      (screen.match(/class="labrow"/g) || []).length === 3 && (screen.match(/data-act="lababsent"[^>]* checked/g) || []).length === 0 &&
      /<option value="mg\/dL"/.test(screen) && !/escapes/.test(screen) && !/Malignancy excluded/.test(screen),
      'rows ' + (screen.match(/class="labrow"/g) || []).length);
    startLabs();
    await tap('labs-continue');
    t('an empty panel continues, and every test is recorded as not in the file',
      ctx.state.nodeId === 'fx_gate' && ctx.state.labs.length === 3 && ctx.state.labs.every((l) => !l.inFile) && /None of 3 in the file/.test(ctx.state.trail[0]?.value ?? ''),
      'node ' + ctx.state.nodeId + ', labs ' + JSON.stringify(ctx.state.labs));
    startLabs();
    await typeRow(0, '2.1', 'IU/mL'); await typeRow(2, '2,4');
    await tap('labs-continue');
    const afp = ctx.state.labs.find((l) => l.id === 'afp'), ca = ctx.state.labs.find((l) => l.id === 'ca'), ldh = ctx.state.labs.find((l) => l.id === 'ldh');
    t('a typed number is recorded as typed, with the unit chosen, or the first unit',
      afp?.value === '2.1' && afp?.unit === 'IU/mL' && afp?.inFile && ca?.value === '2,4' && ca?.unit === 'mmol/L' && ldh && !ldh.inFile, JSON.stringify(ctx.state.labs));
    t('the values stay out of the case variables, so no rule can read one',
      !Object.keys(ctx.state.captured).some((k) => ['afp', 'ldh', 'ca'].includes(k)) && !JSON.stringify(ctx.state.captured).includes('2.1'),
      'captured ' + JSON.stringify(ctx.state.captured));
    t('the panel is one trail entry that summarises it, and stays out of "Suggested based on"',
      ctx.state.trail.length === 1 && /Alpha-fetoprotein \(AFP\) 2\.1 IU\/mL/.test(ctx.state.trail[0].value) && /1 not in the file/.test(ctx.state.trail[0].value) && !/2\.1/.test(ctx.basisFromTrail()),
      JSON.stringify(ctx.state.trail.map((x) => x.value)) + ' | basis ' + ctx.basisFromTrail());
    t('a result in the panel ticks Lab Report on the checklist that follows',
      JSON.stringify(ctx.state.captured.documents_in_file) === '["lab"]' && /data-id="lab" checked/.test(rend(() => ctx.renderLiveNode())), 'captured ' + JSON.stringify(ctx.state.captured.documents_in_file));
    startLabs();
    await tap('labs-continue');
    t('an empty panel ticks nothing', ctx.state.captured.documents_in_file === undefined, JSON.stringify(ctx.state.captured.documents_in_file));
    startLabs();
    await typeRow(0, 'two point one');
    await tap('labs-continue');
    t('text that is not a number is refused, names the row, and the clerk stays on the screen',
      ctx.state.nodeId === 'fx_labs' && !ctx.state.labs.length && /Enter a number/.test(rend(() => ctx.renderLiveNode())) && /aria-invalid="true"/.test(rend(() => ctx.renderLiveNode())),
      'node ' + ctx.state.nodeId);
    startLabs();
    await typeRow(0, '2.1');
    await tap('lababsent', 1, { checked: true });
    await tap('labs-continue');
    t('a row left empty is recorded as not in the file whether or not its box is ticked',
      ctx.state.nodeId === 'fx_gate' && ctx.state.labs.find((l) => l.id === 'ldh')?.inFile === false && ctx.state.labs.find((l) => l.id === 'ca')?.inFile === false && ctx.state.labs.find((l) => l.id === 'afp')?.inFile === true,
      'node ' + ctx.state.nodeId + ' ' + JSON.stringify(ctx.state.labs));
    startLabs();
    await typeRow(0, '7'); await tap('lababsent', 0, { checked: true });
    await tap('labs-continue');
    t('ticking Not in the file clears the number', ctx.state.labs.find((l) => l.id === 'afp')?.inFile === false, JSON.stringify(ctx.state.labs[0]));
    startLabs();
    await typeRow(0, '2.1'); await tap('labs-continue');
    await tap('rewind', 0);
    const back = rend(() => ctx.renderLiveNode());
    t('stepping back reopens the panel as it was typed',
      ctx.state.nodeId === 'fx_labs' && /value="2\.1"/.test(back) && !ctx.state.labs.length, 'node ' + ctx.state.nodeId + ' ' + back.slice(0, 80));
    /* The boxes are the clerk's own: a refused number or a step back shows them as they were left, and a
       blank row is recorded as not in the file without a box being ticked for it. */
    const countChecked = (html, act) => (html.match(new RegExp('data-act="' + act + '"[^>]* checked', 'g')) || []).length;
    const ticked = () => countChecked(rend(() => ctx.renderLiveNode()), 'lababsent');
    startLabs(); await typeRow(0, 'two point one'); await tap('labs-continue');
    t('after a refused number the boxes the clerk did not tick are still empty', ticked() === 0, ticked() + ' box(es) ticked for them');
    startLabs(); await typeRow(0, '2.1'); await tap('labs-continue'); await tap('rewind', 0);
    t('stepping back shows no box ticked that the clerk did not tick', ctx.state.nodeId === 'fx_labs' && ticked() === 0, ticked() + ' box(es) ticked');
    startLabs(); await tap('lababsent', 1, { checked: true }); await typeRow(0, '2.1'); await tap('labs-continue'); await tap('rewind', 0);
    t('a box the clerk did tick is still ticked after stepping back, and only that one',
      ticked() === 1 && /data-i="1"[^>]* checked/.test(rend(() => ctx.renderLiveNode())), ticked() + ' ticked');
    {
      const attempt = async (text) => { startLabs(); await typeRow(0, text); await tap('labs-continue'); return ctx.state.nodeId === 'fx_gate'; };
      const wrong = [], right = [];
      for (const x of ['0x1A', '0b11', '1e3', '12abc', 'Infinity', '--5', '5%', '-5', '1,000,000', '1.2.3', '.5']) if (await attempt(x)) wrong.push(x + ' accepted');
      for (const x of ['2.1', '2,4', '10', '0.05']) if (!(await attempt(x))) right.push(x + ' refused');
      t('a result is digits with at most one decimal mark: hex, binary, exponent, signs and thousands marks are refused',
        !wrong.length && !right.length, wrong.concat(right).join(', '));
      startLabs();
      t('the number box is length-limited', /class="labrow__value"[^>]* maxlength="12"/.test(rend(() => ctx.renderLiveNode())), 'no maxlength');
      startLabs(); await typeRow(0, '2.1'); await tap('labs-continue');
      t('the entry is marked as typed text, so nothing that reports the case may print the values', ctx.state.trail[0] && ctx.state.trail[0].typed === true, JSON.stringify(ctx.state.trail[0]));
    }
    {
      const second = { ...labNode, node_id: 'fx_labs2', next_node: 'fx_gate', labs: [{ id: 'afp', label: 'Alpha-fetoprotein (AFP)', units: ['pg/mL'] }, { id: 'hcg', label: 'Beta-hCG', units: ['IU/L'] }] };
      const two = { morphology_entries: [], decision_trees: [{ tree_id: 'fx', entry_node: 'fx_labs', nodes: [{ ...labNode, next_node: 'fx_labs2' }, second, ...fxDt.decision_trees[0].nodes] }] };
      begin(two, 'fx', 'fx_labs', 'C56.9');
      await typeRow(0, '2.1', 'IU/mL'); await typeRow(2, '2,4'); await tap('labs-continue');
      const screen2 = rend(() => ctx.renderLiveNode());
      t('a unit held from another panel that this test does not list shows, and records, the test\'s own first unit',
        /<option value="pg\/mL" selected>/.test(screen2), screen2.slice(0, 120));
      await typeRow(0, '3'); await tap('labs-continue');
      const L = ctx.state.labs;
      t('a second panel replaces the tests it lists and keeps the rest',
        ctx.state.nodeId === 'fx_gate' && L.find((l) => l.id === 'ca')?.value === '2,4' && L.filter((l) => l.id === 'afp').length === 1 &&
        L.find((l) => l.id === 'afp')?.value === '3' && L.find((l) => l.id === 'afp')?.unit === 'pg/mL' && L.some((l) => l.id === 'hcg'), JSON.stringify(L));
    }
    {
      startLabs(); await typeRow(0, '2.1'); await tap('labs-continue');
      Object.assign(ctx.state, { stage: 'output', result: { referral: true, group: 9, note: 'n' }, group: 8 });
      const html = rend(() => ctx.renderOutput());
      t('the result lists each test with its value and unit, or not in the file',
        /Alpha-fetoprotein \(AFP\)<\/b><span>2\.1 ng\/mL/.test(html) && /Calcium<\/b><span>not in the file/.test(html) && /Laboratory results/.test(html), html.slice(0, 200));
    }
  }

  /* ---- the tool runs in a frame inside another page ------------------------------ */
  /* It must open no browser dialog (a sandboxed frame blocks them), scroll nothing
     but its own document, keep nothing in browser storage, and open no window. The
     two window.prompt calls are the override handler that already existed; the
     parked "Report an error" branch removes them, so the allowance only shrinks. */
  {
    const src = fs.readFileSync(APP, 'utf8');
    const code = src.replace(/\/\*[\s\S]*?\*\//g, '');       /* comments may name what the code must not do */
    const found = ['scrollIntoView', 'window.confirm(', 'window.alert(', 'window.open(', 'localStorage', 'sessionStorage', 'document.cookie', 'target="_blank"']
      .filter((w) => code.includes(w));
    const prompts = (code.match(/window\.prompt\(/g) || []).length;
    t('the tool opens no dialog, window or storage and scrolls no page but its own, as a frame needs',
      !found.length && prompts <= 2, 'found ' + JSON.stringify(found) + ', window.prompt calls ' + prompts);
  }

  /* ---- Home -------------------------------------------------------------- */
  ctx.reset(); Object.assign(ctx.state, { router, topography: topo, stage: 'archetype' });
  await tap('home');
  t('Home with nothing answered returns to the start at once', ctx.state.stage === 'landing' && !ctx.state.confirmExit, 'stage ' + ctx.state.stage);
  begin(fxDt, 'fx', 'fx_gate', 'C56.9'); ctx.state.draft.ticks = ['imaging']; await tap('tick-continue');
  const trailLen = ctx.state.trail.length;
  await tap('home');
  t('Home on a case with answers asks first and keeps the case', ctx.state.confirmExit === true && ctx.state.trail.length === trailLen && ctx.state.stage !== 'landing', 'confirm ' + ctx.state.confirmExit);
  const exitHtml = rend(() => ctx.renderExitConfirm());
  t('the question names both ways out: Discard, then Keep Working, in a quiet bar and not a yellow box',
    /data-act="home-yes">Discard<\/button><button class="btn" data-act="home-no">Keep Working</.test(exitHtml) && /class="exitbar"/.test(exitHtml) && !/banner--warn/.test(exitHtml), 'got ' + exitHtml);
  await tap('home-no');
  t('Keep working dismisses the question and keeps the case', ctx.state.confirmExit === false && ctx.state.trail.length === trailLen, 'trail ' + ctx.state.trail.length);
  await tap('home'); await tap('home-yes');
  t('Discard and go home clears the case', ctx.state.stage === 'landing' && ctx.state.trail.length === 0 && !ctx.state.confirmExit, 'stage ' + ctx.state.stage + ', trail ' + ctx.state.trail.length);
  begin(fxDt, 'fx', 'fx_gate', 'C56.9'); ctx.state.draft.ticks = ['imaging']; await tap('tick-continue'); await tap('home'); await tap('rewind', 0);
  t('any other action dismisses the question', ctx.state.confirmExit === false, 'still asking');
  ctx.reset(); ctx.state.error = 'x'; ctx.state.router = router;
  await tap('home');
  t('Home leaves an error screen', ctx.state.stage === 'landing' && !ctx.state.error, 'stage ' + ctx.state.stage);

  /* ---- the filter box ------------------------------------------------------ */
  ctx.reset(); Object.assign(ctx.state, { router, topography: topo, stage: 'site', archetype: router.archetypes.find((a) => !a.auto_topography) });
  const rowsOf = (html) => [...html.matchAll(/<button class="opt[^"]*"( hidden)? data-find="[^"]*" data-act="site"[^>]*>\s*<span class="opt__label">([^<]*)/g)].map((m) => ({ hidden: !!m[1], label: m[2] }));
  let site = rend(() => ctx.renderSite());
  t('every organ system is listed with a filter box above it', rowsOf(site).length >= 20 && countButtons(site, 'filter') === 1 && rowsOf(site).every((r) => !r.hidden), 'rows ' + rowsOf(site).length);
  ctx.state.draft['f:site'] = 'lower limb';
  const hit = rowsOf(rend(() => ctx.renderSite()));
  t('typing a region name that is not in the system\'s own name finds the system and hides the rest',
    hit.filter((r) => !r.hidden).some((r) => /Bone and joints/.test(r.label)) && !hit.filter((r) => !r.hidden).some((r) => /lower limb/i.test(r.label)) && hit.filter((r) => r.hidden).length >= 15, JSON.stringify(hit.filter((r) => !r.hidden)));
  ctx.state.draft['f:site'] = 'zzzzzz';
  t('a filter that matches nothing says so', /optbox__none">No option matches/.test(rend(() => ctx.renderSite())) && rowsOf(rend(() => ctx.renderSite())).every((r) => r.hidden), 'no empty-result line');
  t('filtering ignores accents and case', ctx.foldText('Müllerian') === 'mullerian' && ctx.findMatch(ctx.foldText('Ovary and testis'), 'TESTIS ovary'), 'fold failed');
  ctx.state.draft = {};
  t('the landing search results carry no second box', !/data-act="filter"/.test(ctx.pick('alias', [{ label: 'a' }], { filter: false })), 'box on search results');

  /* ---- the coding block ----------------------------------------------------- */
  t('topography is the code without its letter and point, then the ICD-O name', (ctx.state.topography = topo, ctx.topographyText('C56.9')) === '569 (Ovary)', ctx.topographyText('C56.9'));
  t('a code the crosswalk lacks still loses its letter and point', ctx.topographyText('C99.9') === '999', ctx.topographyText('C99.9'));
  t('behavior codes read /N (meaning)', ctx.behaviorCodeText('0') === '/0 (Benign neoplasm)' && ctx.behaviorCodeText('3') === '/3 (Malignant)' && ctx.behaviorCodeText('1') === '/1 (Uncertain whether benign or malignant)', ctx.behaviorCodeText('0'));
  t('a group that admits several behaviors lists them all', ctx.behaviorListText('0-1,3') === '/0 (Benign neoplasm), /1 (Uncertain whether benign or malignant), /3 (Malignant)', ctx.behaviorListText('0-1,3'));
  {
    ctx.reset(); Object.assign(ctx.state, { router, topography: topo, stage: 'output', group: 10 });
    ctx.state.captured = { topography: 'C56.9' };
    ctx.state.trail = [{ label: 'Evidence in file', value: 'A histology report' }, { label: 'Tumour type', value: 'Mature cystic teratoma' }];
    ctx.state.result = { behaviourExcluded: true, icdoCode: '9080', icdoBehaviour: '0', icdoTerm: 'Teratoma, benign', groupDeclares: '3', reason: 'r', registrarDecisionRequired: true, basisOfDiagnosis: 7 };
    const html = rend(() => ctx.renderOutput());
    const need = ['Name', 'Teratoma, benign', 'Morphology code', '9080', 'Behavior code', '/0 (Benign neoplasm)', 'Topography code', '569 (Ovary)', 'Suggested based on',
      'A histology report', 'Mature cystic teratoma', 'Group admits', '/3 (Malignant) only', 'Registrar decision required'];
    const missing = need.filter((x) => !html.includes(x));
    t('a benign tumour reports Name, Morphology code, Behavior code, Topography code and Suggested based on',
      !missing.length && !/No code emitted here/.test(html), 'missing ' + JSON.stringify(missing) + (/No code emitted here/.test(html) ? ' and still says no code is emitted' : ''));
    const keep = ctx.state.result;
    ctx.state.result = null; ctx.state.pending = {};
    const pendingLabel = ctx.currentLabel();
    ctx.state.pending = null; ctx.state.result = keep;
    t('the interface says Behavior, never Behaviour', !/ehaviour/.test(html) && !/ehaviour/.test(pendingLabel), 'British spelling on screen: ' + pendingLabel);
  }
  {
    const dt = dts.get(9) || [...dts.values()][0];
    const e = dt.morphology_entries.find((x) => String(x.behavior_code) === '3');
    ctx.reset(); Object.assign(ctx.state, { router, topography: topo, dt, group: 9 });
    ctx.state.captured = { topography: 'C49.2' };
    ctx.state.trail = [{ label: 'Evidence in file', value: 'A histology report' }];
    ctx.finish({ morphology_code: e.morphology_code, behavior_code: e.behavior_code }, 'x');
    const html = rend(() => ctx.renderOutput());
    const order = ['Name', 'Morphology code', 'Behavior code', 'Topography code', 'Suggested based on'].map((x) => html.indexOf(x));
    t('a malignant tumour prints the same five rows, in order, with /3 (Malignant) and its topography',
      order.every((v, i) => v >= 0 && (i === 0 || v > order[i - 1])) && html.includes('/3 (Malignant)') && /Topography code<\/b><span>\d{3} \(/.test(html) && !/>Based on</.test(html),
      'order ' + order.join(',') + ' in the standard block');
  }

  /* ---- the referral hop ------------------------------------------------------- */
  {
    const dt8 = dts.get(8), dt9 = dts.get(9);
    const hasTicks = dt8 && dt8.decision_trees.some((tr) => tr.nodes.some((n) => n.node_id === 'bn_document_inventory' && n.tick_list));
    const gate = dt8.decision_trees[0].nodes.find((n) => n.node_id === 'bn_document_inventory');
    const ref = gate.options.findIndex((o) => o.refer_group === 9 || o.refer_group === '9');
    begin(dt8, dt8.decision_trees[0].tree_id, 'bn_document_inventory', 'C40.2');
    ctx.state.group = 8; ctx.state.trailAtGroupEntry = 0;
    ctx.state.markers = { CD99: 'pos' }; ctx.state.captured.evidence_tests = ['Histology']; ctx.state.captured.documents_in_file = ['histology'];
    if (hasTicks) {
      ctx.state.draft.ticks = ['histology']; ctx.state.draft.ctx = String(gate.options.slice(0, ref).filter((o) => !o.ticks).length + 1);
      await tap('tick-continue');
    } else {
      await tap('opt', ref);
    }
    const isRef = ctx.state.stage === 'output' && ctx.state.result && ctx.state.result.referral;
    t('the soft-tissue referral out of Group VIII reaches its terminal', isRef, 'stage ' + ctx.state.stage);
    const html = isRef ? rend(() => ctx.renderOutput()) : '';
    t('a referral to a built group offers Continue in that group', /data-act="hop">Continue in Group 9/.test(html), 'no hop button');
    const before = ctx.state.trail.length;
    ctx.state.labs = [{ id: 'afp', label: 'AFP', value: '2.1', unit: 'ng/mL', inFile: true }];
    /* What the hop must clear (the old tree's reading of the case) and what it must keep (the case itself). */
    const dvar = Object.values(router.discriminators || {}).map((d) => d.variable).filter(Boolean)[0];
    Object.assign(ctx.state, { grade: { x: 1 }, entity: { name: 'x' }, searchTerm: 'a term', firedAlert: 'a', basisCodes: [7] });
    ctx.state.captured.organ_system = 'bone'; ctx.state.captured.tumour_origin = 'primary';
    if (dvar) ctx.state.captured[dvar] = 'kept';
    const refTrail = ctx.state.trail.length;
    await tap('hop');
    const st2 = ctx.state;
    t('the hop clears the old tree\'s reading: result, grade, entity, search term, alert, and shows no output label',
      st2.result === null && st2.grade === null && st2.entity === null && st2.searchTerm === null && st2.firedAlert === null && ctx.currentLabel() !== 'Output',
      'result ' + JSON.stringify(st2.result) + ', grade ' + JSON.stringify(st2.grade) + ', label ' + ctx.currentLabel());
    t('the hop keeps the case: organ system, tissue origin, a discriminator answer and the basis of diagnosis',
      st2.captured.organ_system === 'bone' && st2.captured.tumour_origin === 'primary' && (!dvar || st2.captured[dvar] === 'kept') && JSON.stringify(st2.basisCodes) === '[7]',
      'captured ' + JSON.stringify(st2.captured) + ', basis ' + JSON.stringify(st2.basisCodes));
    t('the hop enters the receiving group at its own routed tree, not at the site check',
      st2.group === 9 && st2.stage === 'node' && ['st_document_inventory', 'sk_document_inventory'].includes(st2.nodeId), 'group ' + st2.group + ', stage ' + st2.stage + ', node ' + st2.nodeId);
    t('the topography and the documents ticked carry over; the stains read do not',
      st2.captured.topography === 'C40.2' && JSON.stringify(st2.captured.documents_in_file) === '["histology"]' && !Object.keys(st2.markers).length && st2.captured.evidence_tests === undefined,
      'captured ' + JSON.stringify(st2.captured) + ', markers ' + JSON.stringify(st2.markers));
    t('the laboratory panel is a fact of the case and survives the hop', st2.labs.length === 1 && st2.labs[0].value === '2.1', 'labs ' + JSON.stringify(st2.labs));
    t('the trail shows the hop, and the evidence still counts from the first group',
      st2.trail.slice(before).some((x) => x.label === 'Referral' && /Group 9/.test(x.value)) && st2.trailAtGroupEntry === 0, JSON.stringify(st2.trail.map((x) => x.label)) + ' entry ' + st2.trailAtGroupEntry);
    await tap('rewind', st2.trail.findIndex((x) => x.label === 'Referral'));
    t('stepping back to the referral shows the referral screen again', ctx.state.stage === 'output' && ctx.state.result && ctx.state.result.referral, 'stage ' + ctx.state.stage);
    t('stepping back across the hop brings the first group\'s file back, and the screen draws',
      Number(ctx.state.dt.metadata.group_id) === 8 && (rend(() => ctx.render()), !thrown) && /Continue in Group 9/.test(ctx.__dom.els.slot.innerHTML),
      'file is group ' + ctx.state.dt.metadata.group_id + (thrown ? ', render threw: ' + thrown : ''));
    await tap('hop');
    await tap('rewind', 0);
    t('stepping back past the hop to the first answer draws that group\'s own screen',
      ctx.state.group === 8 && Number(ctx.state.dt.metadata.group_id) === 8 && (rend(() => ctx.render()), !thrown) && /Tick every/.test(ctx.__dom.els.slot.innerHTML),
      'group ' + ctx.state.group + ', file ' + ctx.state.dt.metadata.group_id + (thrown ? ', render threw: ' + thrown : ''));
    ctx.reset(); Object.assign(ctx.state, { router, topography: topo, stage: 'output', group: 4, dt: dts.get(4) });
    ctx.state.result = { referral: true, group: 12, note: 'n' };
    t('a referral to a group that is not built offers no hop', !/data-act="hop"/.test(rend(() => ctx.renderOutput())), 'hop offered for an unbuilt group');
  }
  /* ---- a hop into a group that asks its tree, a second tap while it loads, a hop with no site ---- */
  {
    const dt4 = dts.get(4), tr4 = dt4.decision_trees[0];
    const to2 = async () => {
      begin(dt4, tr4.tree_id, tr4.entry_node, 'C71.0');
      ctx.state.group = 4; ctx.state.trailAtGroupEntry = 0;
      ctx.state.trail = [{ label: 'Evidence in file', value: 'A histology report', before: ctx.snapshot(), automatic: false }];
      Object.assign(ctx.state, { stage: 'output', result: { referral: true, group: 2, note: 'n' } });
    };
    await to2();
    await tap('hop');
    t('after a hop into a group that asks its tree, the app bar names that group, not the one left',
      ctx.state.stage === 'handoff' && ctx.contextLabel() === ctx.esc(router.groups['2'].name) && !/Neuroblastoma/.test(ctx.contextLabel()), 'stage ' + ctx.state.stage + ', bar "' + ctx.contextLabel() + '"');
    await tap('handoff', 0);
    const ti = ctx.state.trail.findIndex((x) => x.label === 'Tree');
    t('the tree picked after the hop enters the group, and the evidence still counts from the first group',
      ctx.state.group === 2 && ctx.state.stage === 'node' && ctx.state.trailAtGroupEntry === 0 && ti > 0, 'group ' + ctx.state.group + ', entry ' + ctx.state.trailAtGroupEntry);
    await tap('rewind', ti);
    t('stepping back to the tree question keeps where the evidence began', ctx.state.stage === 'handoff' && ctx.state.hopFrom === 0, 'stage ' + ctx.state.stage + ', hopFrom ' + ctx.state.hopFrom);
    await tap('handoff', 1);
    t('and picking a tree again still lists the evidence from before the hop in "Suggested based on"', /A histology report/.test(ctx.basisFromTrail()), 'basis: ' + ctx.basisFromTrail());

    await to2();
    ctx.state.result = { referral: true, group: 9, note: 'n' };
    const first = ctx.handleOption('hop', fakeEl({}));
    await tap('hop');
    await first;
    t('a second tap while the group is loading does nothing, and the case is not sent to an error screen',
      !ctx.state.error && ctx.state.stage === 'node' && ctx.state.group === 9, 'error ' + ctx.state.error + ', stage ' + ctx.state.stage);

    ctx.reset(); Object.assign(ctx.state, { router, topography: topo, stage: 'output', group: 4, dt: dt4 });
    ctx.state.result = { referral: true, group: 9, note: 'n' };
    t('a referral into a group that routes its trees by site offers no hop when the case has no site',
      !/data-act="hop"/.test(rend(() => ctx.renderOutput())), 'a hop was offered');
    ctx.state.captured.topography = 'C40.2';
    t('and offers it once the case has one', /data-act="hop"/.test(rend(() => ctx.renderOutput())), 'no hop with a site');
  }
  t('a topography written as a range with an instruction prints as written, not as a mangled code',
    ctx.topographyText('C70.0-C72.9 - record the exact code documented') === 'C70.0-C72.9 - record the exact code documented', ctx.topographyText('C70.0-C72.9 - record the exact code documented'));

  /* ---- the result block on every terminal ----------------------------------- */
  {
    const entryOf = (b) => { for (const [g, dt] of dts) { const e = dt.morphology_entries.find((x) => String(x.behavior_code) === b); if (e) return { g, dt, e }; } return null; };
    const lab = [{ id: 'afp', label: 'AFP', value: '2.1', unit: 'ng/mL', inFile: true }];
    const seed = (extra) => {
      ctx.reset(); Object.assign(ctx.state, Object.assign({ router, topography: topo, stage: 'output', labs: lab }, extra));
      ctx.state.captured = { topography: 'C56.9' };
      ctx.state.trail = [{ label: 'Evidence in file', value: 'A histology report' }];
    };
    const shapes = [];
    for (const b of ['0', '1', '3']) {
      const f = entryOf(b);
      if (f) shapes.push({ name: 'a code from the standard terminal at behavior /' + b, want: ['Name', 'Morphology code', 'Behavior code', 'Topography code', 'Suggested based on', behaviorTextOf(b), '569 (Ovary)', 'A histology report'],
        make: () => { seed({ dt: f.dt, group: f.g }); ctx.finish({ morphology_code: f.e.morphology_code, behavior_code: f.e.behavior_code }, 'x'); ctx.state.labs = lab; } });
    }
    shapes.push({ name: 'the behavior exclusion', want: ['Name', 'Morphology code', 'Behavior code', 'Topography code', 'Suggested based on', '/0 (Benign neoplasm)', '569 (Ovary)', 'A histology report'],
      make: () => seed({ result: { behaviourExcluded: true, icdoCode: '9080', icdoBehaviour: '0', icdoTerm: 'Teratoma, benign', groupDeclares: '3', reason: 'r' } }) });
    shapes.push({ name: 'a referral', want: ['Topography code', 'Suggested based on', '569 (Ovary)', 'A histology report'],
      make: () => seed({ group: 4, dt: dts.get(4), result: { referral: true, group: 9, note: 'n' } }) });
    shapes.push({ name: 'a non-reportable exclusion', want: ['Topography code', '569 (Ovary)'],
      make: () => seed({ result: { excluded: true, reason: 'r' } }) });
    for (const sh of shapes) {
      sh.make();
      const html = rend(() => ctx.renderOutput()), missing = sh.want.concat(['Laboratory results', '2.1 ng/mL']).filter((x) => !html.includes(x));
      t(sh.name + ' prints its rows in the registrar\'s format and the laboratory panel', !missing.length && !/ehaviour/.test(html), 'missing ' + JSON.stringify(missing));
    }
  }

  /* ---- Home, the leave bar and the keyboard focus, through render() ------------- */
  {
    const dom = ctx.__dom;
    ctx.reset(); ctx.state.router = null; ctx.state.error = 'Could not load the shared router data.';
    rend(() => ctx.render());
    const hiddenAtStart = dom.els['appbar-home'].hidden;
    ctx.state.router = router; rend(() => ctx.render());
    t('Home is not offered on a start-up failure, where there is no case to leave, and is offered on a later error',
      hiddenAtStart === true && dom.els['appbar-home'].hidden === false, 'at start ' + hiddenAtStart + ', later ' + dom.els['appbar-home'].hidden);
    begin(fxDt, 'fx', 'fx_gate', 'C56.9'); await tick('imaging', true); await tap('tick-continue');
    dom.focused.length = 0; await tap('home'); rend(() => ctx.render());
    const slotHtml = dom.els.slot.innerHTML;
    t('the Leave this case bar comes after the screen, and Home hands the keyboard focus to Keep Working',
      slotHtml.indexOf('class="exitbar"') > slotHtml.indexOf('class="node--live"') && dom.focused.includes('[data-act="home-no"]'), JSON.stringify(dom.focused));
    dom.focused.length = 0; await tap('home-no'); rend(() => ctx.render());
    t('Keep Working hands the focus back to Home', dom.focused.includes('#appbar-home') && !/exitbar/.test(dom.els.slot.innerHTML), JSON.stringify(dom.focused));

    begin(fxDt, 'fx', 'fx_gate', 'C56.9'); rend(() => ctx.render());
    dom.active = { getAttribute: (k) => ({ 'data-act': 'tick', 'data-id': 'imaging' })[k] ?? null, closest: (sel) => (sel === '#slot' ? {} : null), type: 'checkbox', value: 'on' };
    dom.focused.length = 0; await tick('imaging', true); rend(() => ctx.render());
    t('a box ticked from the keyboard keeps the focus through the redraw', dom.focused.includes('[data-act="tick"][data-id="imaging"]'), JSON.stringify(dom.focused));
    dom.focused.length = 0; await tap('tick-continue'); rend(() => ctx.render());
    t('a new screen restores no focus', !dom.focused.length, JSON.stringify(dom.focused));
    dom.active = null;
    startLabsFocus: {
      const labNodeF = { node_id: 'fx_lf', node_type: 'lab_results', step_label: 'Laboratory results', question: 'q', hint: 'h', nos_fallback: null, next_node: 'fx_gate', labs: [{ id: 'afp', label: 'AFP', units: ['ng/mL'] }] };
      const dtF = { morphology_entries: [], decision_trees: [{ tree_id: 'fx', entry_node: 'fx_lf', nodes: [labNodeF, ...fxDt.decision_trees[0].nodes] }] };
      begin(dtF, 'fx', 'fx_lf', 'C56.9'); rend(() => ctx.render());
      await tap('labval', 0, { value: 'abc' }); await tap('labs-continue');
      dom.focused.length = 0; rend(() => ctx.render());
      const html = dom.els.slot.innerHTML;
      t('a refused number moves the focus to its box, which names the error',
        dom.focused.includes('.labrow__value[aria-invalid="true"]') && /aria-describedby="lab-afp-error"/.test(html) && /id="lab-afp-error" role="alert"/.test(html), JSON.stringify(dom.focused));
    }
  }

  /* ---- the filter box on every kind of list ------------------------------------- */
  {
    const list = [{ label: 'Ovary and testis' }, { label: 'Lower limb', meta: 'bone' }, { label: 'Brain' }];
    const vis = (html) => [...html.matchAll(/class="[^"]*"(?: hidden)? data-find|<(?:button|label) class="[^"]*"( hidden)? data-find="([^"]*)"/g)].map((m) => ({ hidden: !!m[1], find: m[2] })).filter((x) => x.find !== undefined);
    ctx.reset(); ctx.state.draft = { 'f:site': 'Lower limb' };
    let v = vis(ctx.pick('site', list));
    t('typing an option\'s own label shows that row and hides the rest', v.filter((x) => !x.hidden).length === 1 && /lower limb/.test(v.find((x) => !x.hidden).find), JSON.stringify(v));
    ctx.state.draft = { 'f:site': 'ovary testis' };
    v = vis(ctx.pick('site', list));
    t('a query of two words needs both in the row', v.filter((x) => !x.hidden).length === 1 && /ovary/.test(v.find((x) => !x.hidden).find), JSON.stringify(v));
    ctx.state.draft = { 'f:site': 'bone' };
    v = vis(ctx.pick('site', list));
    t('text found only in a row\'s meta line finds the row', v.filter((x) => !x.hidden).length === 1 && /lower limb/.test(v.find((x) => !x.hidden).find), JSON.stringify(v));
    ctx.state.draft = { 'f:ctx': 'zzz' };
    v = vis(ctx.choose('ctx', list, undefined));
    t('a radio list hides the rows a filter does not match, and says none match', v.every((x) => x.hidden) && /optbox__none">No option/.test(ctx.choose('ctx', list, undefined)), JSON.stringify(v));
    v = vis(ctx.choose('ctx', list, 2));
    t('a radio list keeps the row the clerk has chosen on screen whatever is typed', v.filter((x) => !x.hidden).length === 1 && /brain/.test(v.find((x) => !x.hidden).find), JSON.stringify(v));
    ctx.state.draft = { 'f:optsel': 'zzz' };
    v = vis(ctx.pick('optsel', list, { selected: 1 }));
    t('a select-then-confirm list keeps the selected row on screen whatever is typed', v.filter((x) => !x.hidden).length === 1 && /lower limb/.test(v.find((x) => !x.hidden).find), JSON.stringify(v));
    ctx.state.draft = {};

    let cy = null;
    for (const [g, dt] of dts) for (const tr of dt.decision_trees) for (const n of tr.nodes) if (!cy && n.node_type === 'cytogenetics_dropdown') cy = { g, dt, tr, n };
    if (!cy) t('a cytogenetics dropdown is a filtered radio list that Continue answers (none in the data)', true, '');
    else {
      begin(cy.dt, cy.tr.tree_id, cy.n.node_id, 'C42.1');
      const h0 = rend(() => ctx.renderLiveNode());
      t('a cytogenetics dropdown is a filtered radio list, with Continue disabled until a finding is chosen',
        (h0.match(/type="radio"/g) || []).length === cy.n.options.length && countButtons(h0, 'filter') === 1 && /data-act="resolve" disabled/.test(h0), 'radios ' + (h0.match(/type="radio"/g) || []).length + ' of ' + cy.n.options.length);
      await draftSet('option', '0');
      const h1 = rend(() => ctx.renderLiveNode());
      t('choosing a finding enables Continue', /data-act="resolve">/.test(h1) && !/data-act="resolve" disabled/.test(h1), 'still disabled');
      await tap('resolve');
      t('and Continue leaves the node without an error', !thrown && !ctx.state.error && (ctx.state.stage !== 'node' || ctx.state.nodeId !== cy.n.node_id), 'stage ' + ctx.state.stage + ', node ' + ctx.state.nodeId + ', error ' + ctx.state.error);
    }
  }

  /* ---- the delegated listeners: click, input, Enter, Escape ----------------------- */
  {
    const L = loadEngine(true), D = L.__dom;
    for (let k = 0; k < 400 && L.state.stage !== 'landing'; k++) await new Promise((r) => setTimeout(r, 5));
    const settle = () => new Promise((r) => setImmediate(r));
    const el = (attrs, extra) => { const e = Object.assign({ tagName: 'BUTTON', type: 'button', value: '', getAttribute: (k) => (k in attrs ? String(attrs[k]) : null) }, extra || {}); e.closest = (sel) => (sel === '[data-act]' ? e : (extra && extra.__closest && extra.__closest[sel]) || null); return e; };
    const fire = async (type, target, key) => { const ev = { target, key, preventDefault() { ev.prevented = true; } }; for (const fn of D.appListeners[type] || []) await fn(ev); await settle(); return ev; };
    t('the page boots against the data on disk and registers its listeners', L.state.stage === 'landing' && ['click', 'change', 'input', 'keydown'].every((k) => (D.appListeners[k] || []).length >= 1), 'stage ' + L.state.stage);
    t('Home is hidden on the landing screen', D.els['appbar-home'].hidden === true, 'hidden ' + D.els['appbar-home'].hidden);
    await fire('click', el({ 'data-act': 'guided' }));
    t('Home appears once a case is open', L.state.stage === 'archetype' && D.els['appbar-home'].hidden === false, 'stage ' + L.state.stage);

    const mkRow = (find, selected) => ({ tagName: 'BUTTON', hidden: false, clicks: 0, click() { this.clicks++; }, getAttribute: () => find, classList: { contains: (c) => !!selected && c === 'opt--selected' }, querySelector: () => null });
    const rows = [mkRow('bone and joints'), mkRow('ovary and testis'), mkRow('brain', true)];
    const none = { hidden: true }, say = { textContent: '' };
    const box = { querySelectorAll: () => rows, querySelector: (sel) => (sel === '.optbox__none' ? none : sel === '.optbox__status' ? say : null) };
    const filterEl = (value) => el({ 'data-act': 'filter', 'data-key': 'site' }, { tagName: 'INPUT', type: 'search', value, __closest: { '.optbox': box } });
    await fire('input', filterEl('ovary'));
    t('typing in a filter box hides the rows that do not match and keeps the selected one, and announces the count',
      rows[0].hidden === true && rows[1].hidden === false && rows[2].hidden === false && say.textContent === '2 options shown' && L.state.draft['f:site'] === 'ovary',
      JSON.stringify(rows.map((r) => r.hidden)) + ' "' + say.textContent + '"');
    const enter = await fire('keydown', filterEl('ovary'), 'Enter');
    t('Enter takes the first row that matches what was typed, not the selected row', rows[1].clicks === 1 && rows[2].clicks === 0 && enter.prevented, 'clicks ' + rows.map((r) => r.clicks).join(','));
    rows.forEach((r) => { r.clicks = 0; });
    await fire('keydown', filterEl('   '), 'Enter');
    t('Enter in an empty filter box answers nothing', rows.every((r) => r.clicks === 0), 'clicks ' + rows.map((r) => r.clicks).join(','));

    L.state.confirmExit = true; D.focused.length = 0;
    await fire('keydown', el({}), 'Escape');
    t('Escape answers the Leave this case bar with Keep Working, and the focus returns to Home', L.state.confirmExit === false && D.focused.includes('#appbar-home'), 'confirm ' + L.state.confirmExit + ' ' + JSON.stringify(D.focused));
    await fire('keydown', el({}), 'Escape');
    t('Escape with no question open does nothing', L.state.confirmExit === false, 'confirm ' + L.state.confirmExit);

    const labN = { node_id: 'fx_l', node_type: 'lab_results', step_label: 'Laboratory results', question: 'q', hint: 'h', nos_fallback: null, next_node: 'fx_l', labs: [{ id: 'afp', label: 'AFP', units: ['ng/mL'] }] };
    Object.assign(L.state, { dt: { morphology_entries: [], decision_trees: [{ tree_id: 'fx', entry_node: 'fx_l', nodes: [labN] }] }, treeId: 'fx', nodeId: 'fx_l', stage: 'node', group: null });
    const absentBox = { checked: true };
    await fire('input', el({ 'data-act': 'labval', 'data-i': 0 }, { tagName: 'INPUT', type: 'text', value: '2.1', __closest: { '.labrow': { querySelector: () => absentBox } } }));
    t('typing a number in a laboratory row clears that row\'s "Not in the file" box', absentBox.checked === false && L.state.draft.labs.afp.value === '2.1', JSON.stringify(L.state.draft.labs));
  }
  return rows;
}

/* ---------------------------------------------------------------------- main */
const ctx = loadEngine();
let bad = 0, partial = 0;

console.log('Fixtures — the defect, and the controls that keep a fix honest\n');
for (const r of (ONLY === 'ux' ? [] : fixtures(ctx))) {
  console.log('  %s  %s', r.ok ? 'OK  ' : 'FAIL', r.name);
  if (!r.ok) { console.log('        ' + r.detail); bad++; }
}

console.log('\nExpress lane — a term filed under several groups is settled by the site\n');
{
  /* An engine that throws inside a scenario fails the section by name rather
     than ending the run with a stack trace. */
  const r = { routed: 0, mismatch: 0, tie: 0, single: 0, siteSingles: 0, terms: 0, skipped: 0, rewinds: 0, fails: [] };
  if (ONLY !== 'ux') try { await expressLane(ctx, r); } catch (e) { r.fails.push('the engine threw: ' + e.message); }
  console.log('  %s  %d multi-group term(s) and %d single-group term(s) whose group reads the site, x every site: %d routed to one group, %d stopped (no group), %d stopped (tie); %d single-group term(s) of a group that reads no site enter it directly; %d stepped-back case(s); %d term(s) not reachable from the results',
    r.fails.length ? 'FAIL' : 'OK  ', r.terms, r.siteSingles, r.routed, r.mismatch, r.tie, r.single, r.rewinds, r.skipped);
  for (const f of r.fails.slice(0, Math.max(SHOW, 5))) console.log('        ' + f);
  if (r.fails.length > Math.max(SHOW, 5)) console.log('        ... and ' + (r.fails.length - Math.max(SHOW, 5)) + ' more');
  bad += r.fails.length;
}

console.log('\nTick lists, Home, filter, result block and referral hop\n');
{
  let ux = [];
  try { ux = await uxScenarios(ctx); } catch (e) { ux = [{ name: 'the scenarios ran to the end', ok: false, detail: 'the engine threw: ' + e.stack }]; }
  for (const r of ux) {
    console.log('  %s  %s', r.ok ? 'OK  ' : 'FAIL', r.name);
    if (!r.ok) { console.log('        ' + r.detail); bad++; }
  }
}

console.log('\nSweep — every ihc_checklist node in every group\n');
for (const name of (ONLY === 'ux' ? [] : fs.readdirSync(DB).sort())) {
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
