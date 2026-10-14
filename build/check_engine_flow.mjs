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
   group with the topography captured; several stop the case with nothing
   entered, and so does none, unless the router declares exactly one of the
   term's groups as occurring at any site (Group II, registrar, 7 October 2026),
   which then enters. Each pair is tapped through `handleOption` — alias, organ
   system, region — the handlers the rendered buttons call.

   A term filed under ONE group is asked its site too when that group's data
   reads the site — the router routes its trees from the topography, or a
   `when` in its trees names `topography` — computed here from the router and
   the group files, not from the engine (registrar, 4 October 2026). Without
   the site those rules fail open: "Rhabdoid tumour", a Group IX-only
   spelling, coded a renal rhabdoid tumour in Group IX.

   The single-group terms of a group that reads no site are asked the site too,
   and the answer is only recorded (registrar, 7 October 2026): before that the
   output printed Topography as a dash for most typed terms. They are the
   control for the opposite fault: the recorded site must never narrow the group
   or stop the case, so each is tried at a site its group's own candidate list
   excludes, and at "the file does not state the site". */
async function expressLane(ctx, out) {
  const SHARED = path.join(ROOT, 'data', 'shared');
  const router = JSON.parse(fs.readFileSync(path.join(SHARED, 'presentation_router.json'), 'utf8'));
  const topo = JSON.parse(fs.readFileSync(path.join(SHARED, 'topography_codes.json'), 'utf8'));
  const index = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'aliases', 'alias_index.json'), 'utf8'));
  for (const name of fs.readdirSync(DB)) {
    const m = /^group_(\d+)_dt\.json$/.exec(name);
    if (m) {
      const aliasFile = path.join(ROOT, 'data', 'aliases', 'aliases_group_' + m[1] + '.json');
      ctx.groupCache.set(Number(m[1]), { dt: JSON.parse(fs.readFileSync(path.join(DB, name), 'utf8')),
        aliases: fs.existsSync(aliasFile) ? JSON.parse(fs.readFileSync(aliasFile, 'utf8')) : [] });
    }
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
  /* The site is asked in up to three taps: body system, organ, region. A screen that offers one
     answer is skipped, so each tap is made only if the case is on that screen. */
  const atSite = () => ['site_system', 'site'].includes(ctx.state.stage);
  const siteScreen = () => (ctx.state.stage === 'site_system' ? ctx.renderSiteSystem() : ctx.renderSite());
  const pickSite = async (code) => {
    if (ctx.state.stage === 'site_system') {
      const organ = ctx.systemRows().find((row) => row.codes.includes(code)).organ;
      await tap('site_system', ctx.siteSystems().findIndex((x) => x.organs.includes(organ)));
    }
    if (ctx.state.stage === 'site') await tap('site', ctx.organRows().findIndex((row) => row.codes.includes(code)));
    if (ctx.state.stage === 'site_region') {
      await tap('site_region', ctx.regionOptions(ctx.state.organSystem).findIndex((o) => o.topography === code));
    }
  };
  /* Can this code be picked from the screen the case is on? A step back restores the system the
     clerk had chosen, so the organ screen lists that system's organs only. */
  const canPick = (code) => {
    const st = ctx.state.stage;
    if (st === 'site_system') return true;
    if (st === 'site') return ctx.organRows().some((row) => row.codes.includes(code));
    if (st === 'site_region') return ctx.regionOptions(ctx.state.organSystem).some((o) => o.topography === code);
    return false;
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
  /* The groups a (term, site) pair should reach, computed from the router and the topography
     file: the term's groups that the site names; and only if it names none, the term's groups
     the router declares as occurring at any site. */
  const anySite = (g) => ((router.groups || {})[String(g)] || {}).occurs_at_any_site === true;
  /* A group that routes its trees from the topography and is marked `occurs_at_routed_sites`
     occurs at every site one of its routing rules names, read here from the rule lists. */
  /* The term must also be one the group's own entries place at the site: read here from the alias
     file and the entries' primary_sites by a second parser (split on "-", not a pattern), so a term
     ICCC-2017 places only at the gonads is expected to stop at the liver. A term filed under several
     groups has no evidence and is expected to stop. */
  const num = (c) => parseInt(c.slice(1, 3), 10) * 10 + parseInt(c.slice(4, 5), 10);
  const covers = (sites, code) => (sites || []).some((s) => {
    const ends = s.split(' ')[0].split('-');
    return num(code) >= num(ends[0]) && num(code) <= num(ends[ends.length - 1]);
  });
  const routedAt = (g, code, term) => {
    const m = (router.groups || {})[String(g)] || {};
    if (!(m.occurs_at_routed_sites === true && ((m.tree_routing || {}).rules || []).some((r) => (r.topography_in || []).includes(code)))) return false;
    if ((index[term] || []).length !== 1) return false;
    const cached = ctx.groupCache.get(g);
    const mapped = (cached.aliases || []).filter((a) => a.alias === term).flatMap((a) => a.maps_to_morphology_codes || []);
    return mapped.length > 0 && cached.dt.morphology_entries.some((e) => mapped.includes(String(e.morphology_code)) && covers(e.primary_sites, code));
  };
  const expectAt = (groups, code, term) => {
    const cg = topo.topography_lookup[code].candidate_groups;
    if (!Array.isArray(cg)) return groups.slice();
    const named = groups.filter((g) => cg.includes(g));
    return named.length ? named : groups.filter((g) => anySite(g) || routedAt(g, code, term));
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
      const g = groups[0], at0 = '"' + term + '" [' + g + ']';
      if (!(router.groups || {})[String(g)].built) {
        /* An unbuilt group stops at its handoff: no tree, so no site to record. */
        if (ctx.state.group !== g || ['site_system', 'site', 'site_region'].includes(ctx.state.stage)) fail(at0 + ' (unbuilt) reached stage ' + ctx.state.stage + ', group ' + ctx.state.group);
        continue;
      }
      if (!atSite() || ctx.state.group !== null) {
        fail(at0 + ' reached stage ' + ctx.state.stage + ', group ' + ctx.state.group + ', not the record-only site question');
        continue;
      }
      let screen = '';
      try { screen = siteScreen(); } catch (e) { fail(at0 + ' site screen throws: ' + e.message); continue; }
      if (screen.indexOf(ctx.esc(term)) < 0) fail(at0 + ' site screen does not name the term');
      if (screen.indexOf('data-act="site-unstated"') < 0) fail(at0 + ' site screen offers no "not stated" answer');
      const cgOf = (c) => topo.topography_lookup[c].candidate_groups;
      const named = (c) => !Array.isArray(cgOf(c)) || cgOf(c).includes(g);
      const probe = [...new Set([codes[0], codes.find((c) => !named(c)), codes.find((c) => named(c))].filter(Boolean))];
      for (const code of probe) {
        await enter(term);
        try { await pickSite(code); } catch (e) { fail(at0 + ' at ' + code + ' throws: ' + e.message); continue; }
        const st = ctx.state;
        out.recorded = (out.recorded || 0) + 1;
        if (st.captured.topography !== code) fail(at0 + ' at ' + code + ': topography captured as ' + st.captured.topography);
        else if (st.group !== g || ['site_system', 'site', 'site_region', 'search_unresolved'].includes(st.stage)) {
          fail(at0 + ' at ' + code + ' ' + JSON.stringify(cgOf(code)) + ': expected Group ' + g + ' entered, got stage ' + st.stage + ', group ' + st.group);
        }
      }
      await enter(term); await tap('site-unstated', 0);
      const su = ctx.state;
      if (su.group !== g || su.captured.topography !== undefined || ['site_system', 'site', 'site_region', 'search_unresolved'].includes(su.stage)) {
        fail(at0 + ' "not stated": expected Group ' + g + ' with no topography, got stage ' + su.stage + ', group ' + su.group + ', topography ' + su.captured.topography);
      }
      continue;
    }
    groups.length > 1 ? out.terms++ : out.siteSingles++;
    if (!atSite() || ctx.state.group !== null) {
      fail('"' + term + '" ' + JSON.stringify(groups) + ' reached stage ' + ctx.state.stage + ', group ' + ctx.state.group + ', not the site question');
      continue;
    }
    let screen = '';
    try { screen = siteScreen(); } catch (e) { fail('"' + term + '" site screen throws: ' + e.message); continue; }
    if (screen.indexOf(ctx.esc(term)) < 0) fail('"' + term + '" site screen does not name the term');
    if (screen.indexOf('data-act="site-unstated"') >= 0 || ctx.state.siteRecordOnly) {
      fail('"' + term + '" ' + JSON.stringify(groups) + ' site screen offers "not stated" or sets the record-only flag, which would enter a group the site did not choose');
    }
    for (const code of codes) {
      await enter(term);
      try { await pickSite(code); } catch (e) { fail('"' + term + '" at ' + code + ' throws: ' + e.message); continue; }
      const cg = topo.topography_lookup[code].candidate_groups;
      const expect = expectAt(groups, code, term);
      const st = ctx.state, at = '"' + term + '" ' + JSON.stringify(groups) + ' at ' + code + ' ' + JSON.stringify(cg);
      if (st.captured.topography !== code) { fail(at + ': topography captured as ' + st.captured.topography); continue; }
      if (expect.length === 1) {
        out.routed++;
        if (Array.isArray(cg) && !groups.some((g) => cg.includes(g))) {
          out.anySite++;
          if (routedAt(expect[0], code, term)) out.routedSites++;
        }
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
      const routed = row.codes.find((c) => expectAt(groups, c, term).length === 1 && ctx.groupMeta(expectAt(groups, c, term)[0]).tree_routing);
      if (!routed) continue;
      /* Back at the Tree entry the clerk is on the last site screen they answered: the region
         screen, the organ screen, or the system screen when the system held one organ of one
         code. An organ of another system is reached by stepping back to the system screen. */
      for (const code of row.codes.length > 1 ? row.codes : codes) {
        await enter(term); await pickSite(routed);
        if (!(await rewindTo('Tree'))) { fail('R1 "' + term + '" at ' + routed + ': routed with no Tree entry'); break; }
        if (!canPick(code) && !(await rewindTo('Site of origin'))) { fail('R1 "' + term + '" at ' + routed + ': ' + code + ' is not on the screen the Tree entry returns to, and there is no system entry to step back to'); break; }
        await pickSite(code);
        out.rewinds++;
        const expect = expectAt(groups, code, term), st = ctx.state;
        const at = 'R1 "' + term + '" ' + JSON.stringify(groups) + ' at ' + routed + ', back to Tree, then ' + code;
        /* The trail must describe this case only: the site answered once, and
           no group or tree left over from the case before the step back. */
        const labels = st.trail.map((t) => t.label);
        const twice = ['Site of origin', 'Organ', 'Topography'].filter((l) => labels.filter((x) => x === l).length > 1);
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
    if (atSite()) {
      const keep = codes.find((c) => expectAt([g], c, term).length === 1);
      if (!keep) continue;
      await pickSite(keep);
    }
    if (!(await rewindTo('Tree'))) continue;
    routedGroups.add(g);
    await tap('guided', 0);
    for (let k = 0; k < 8 && ['archetype', 'discriminator', 'site_system', 'site', 'site_region'].includes(ctx.state.stage); k++) {
      await tap(ctx.state.stage, 0);
    }
    out.rewinds++;
    if (ctx.state.searchTerm || ctx.state.stage === 'search_unresolved') {
      fail('R2 "' + term + '" [' + g + '], back to Tree, then the guided route: the case still carries the search term (stage ' +
        ctx.state.stage + ', term ' + JSON.stringify(ctx.state.searchTerm) + ')');
    }
  }
  if (!routedGroups.size) fail('R2 found no single-group term whose group routes its tree — the scenario did not run');

  /* R4  the record-only lane, stepped back from. One term of every built group that
         reads no site. Back at the Search entry the clerk takes the guided route, and
         the case must carry neither the search term nor the record-only flag. Back at
         the organ-system question the clerk answers "not stated", and the trail must
         hold that answer once and no site. */
  const recordGroups = new Set();
  for (const term of singles) {
    const g = index[term][0];
    if (recordGroups.has(g) || readsSite(g) || !(router.groups || {})[String(g)].built) continue;
    recordGroups.add(g);
    await enter(term); await pickSite(codes[0]);
    if (!(await rewindTo('Search'))) { fail('R4 "' + term + '" [' + g + ']: no Search entry to step back to'); continue; }
    await tap('guided', 0);
    for (let k = 0; k < 8 && ['archetype', 'discriminator', 'site_system', 'site', 'site_region'].includes(ctx.state.stage); k++) await tap(ctx.state.stage, 0);
    out.rewinds++;
    if (ctx.state.searchTerm || ctx.state.siteRecordOnly || ctx.state.stage === 'search_unresolved') {
      fail('R4 "' + term + '" [' + g + '], back to Search, then the guided route: term ' + JSON.stringify(ctx.state.searchTerm) +
        ', record-only ' + ctx.state.siteRecordOnly + ', stage ' + ctx.state.stage);
    }
    await enter(term); await pickSite(codes[0]);
    if (!(await rewindTo('Site of origin'))) { fail('R4 "' + term + '" [' + g + ']: no Site of origin entry to step back to'); continue; }
    await tap('site-unstated', 0);
    out.rewinds++;
    const labels = ctx.state.trail.map((x) => x.label), st = ctx.state;
    if (st.group !== g || st.captured.topography !== undefined || labels.includes('Site of origin') || labels.includes('Organ') ||
        labels.filter((l) => l === 'Topography').length !== 1) {
      fail('R4 "' + term + '" [' + g + '], back to the organ system and "not stated": group ' + st.group + ', topography ' +
        st.captured.topography + ', trail ' + JSON.stringify(st.trail.map((x) => x.label + ': ' + x.value)));
    }
  }
  if (!recordGroups.size) fail('R4 found no single-group term of a group that reads no site — the scenario did not run');

  /* R5  keep_on_site, read from the router and driven through the engine. Every answer
         that keeps a group must leave that group a candidate (or the entered group) at
         every selectable site, for every presentation that asks the question. Without
         the key the site takes Group II away at most sites. */
  for (const a of router.archetypes) {
    const d = a.dual_group_discriminator && (router.discriminators || {})[a.dual_group_discriminator];
    if (!d || !(d.ask_before_site || d.ask_when)) continue;
    const ai = router.archetypes.indexOf(a);
    for (const [answer, rule] of Object.entries(d.narrows || {})) {
      const keep = (rule.keep_on_site || []).filter((g) => (a.candidate_groups || []).includes(g));
      if (!keep.length) continue;
      const oi = d.options.findIndex((o) => String(typeof o === 'string' ? o : o.value) === answer);
      for (const code of codes) {
        ctx.reset(); ctx.state.router = router; ctx.state.topography = topo; ctx.state.aliasIndex = index;
        await tap('guided', 0); await tap('archetype', ai);
        if (d.ask_before_site) await tap('discriminator', oi);
        if (ctx.systemRows().findIndex((row) => row.codes.includes(code)) < 0) continue;
        await pickSite(code);
        /* A question asked after the site appears only where it can matter, and not at all where the
           site answers it; the sites that never ask it have nothing to protect. */
        if (d.ask_when) {
          if (ctx.state.stage !== 'discriminator') continue;
          await tap('discriminator', oi);
        }
        out.keepWalks++;
        for (const g of keep) {
          if (ctx.state.group !== g && !(ctx.state.candidates || []).includes(g)) {
            fail('R5 ' + a.archetype_id + ', answer "' + answer + '", site ' + code + ': Group ' + g + ' was kept by the router but is not a candidate (stage ' +
              ctx.state.stage + ', group ' + ctx.state.group + ', candidates ' + JSON.stringify(ctx.state.candidates) + ')');
          }
        }
      }
    }
  }
  if (!out.keepWalks) fail('R5 found no keep_on_site in the router — the scenario did not run');
  if (!out.anySite) fail('no term was routed by occurs_at_any_site — the router declares no such group, or the scenario did not run');
  if (!out.routedSites) fail('no term was routed by occurs_at_routed_sites — the router declares no such group, or the scenario did not run');

  /* R3  the guided route, same defect: a tree routed from the topography is
         an automatic trail entry. Every presentation × organ system is walked
         (first option wherever a choice remains); where a Tree entry appears,
         the clerk steps back to it and answers again, and the trail must not
         hold the earlier answers twice. */
  let guidedRewinds = 0;
  /* A screen with an option to tap. An unbuilt group's handoff is a banner. */
  const asks = (st) => ['discriminator', 'site_region', 'group'].includes(st) ||
    (st === 'handoff' && ctx.groupMeta(ctx.state.group).built && !!ctx.groupMeta(ctx.state.group).tree_selection);
  /* Row r of the presentation's organ list, reached through whichever of the system and organ
     screens the case is on. */
  const tapSite = async (st, r) => {
    const row = ctx.systemRows()[r];
    if (st === 'site_system') await tap('site_system', ctx.siteSystems().findIndex((x) => x.organs.includes(row.organ)));
    else await tap('site', ctx.organRows().findIndex((x) => x.organ === row.organ));
  };
  const walk = async (a, r) => {
    ctx.reset(); ctx.state.router = router; ctx.state.topography = topo; ctx.state.aliasIndex = index;
    await tap('guided', 0); await tap('archetype', a);
    for (let k = 0; k < 8 && ctx.state.stage !== 'node'; k++) {
      const st = ctx.state.stage;
      if (st === 'site_system' || st === 'site') await tapSite(st, r);
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
        if (st === 'site_system' || st === 'site') await tapSite(st, r);
        else if (asks(st)) await tap(st, 0);
        else break;
      }
      guidedRewinds++;
      const labels = ctx.state.trail.map((x) => x.label);
      const twice = [...new Set(labels)].filter((l) => labels.filter((x) => x === l).length > 1);
      if (twice.length) {
        fail('R3 guided, presentation ' + a + ', organ ' + r + ', back to Tree and answered again: the trail holds ' +
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
  /* The tree a node sits in, kept beside the data and not on it: the engine walks a group's nodes
     with a recursive scan, and a node that points back at its own tree sends that scan round forever. */
  const treeOfNode = new WeakMap();
  const left = (n, o) => {
    const st = ctx.state, gone = !(st.stage === 'node' && st.nodeId === n.node_id);
    if (!gone) return false;
    if (o.behaviour_resolution) return st.stage === 'behaviour';
    if (o.grade_resolution) return st.stage === 'grade';
    if (o.resource_level_gate) return true;
    if (o.next_node) {
      const dest = (treeOfNode.get(n) || []).find((x) => x.node_id === o.next_node);
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
      treeOfNode.set(n, tree.nodes);
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
  const DOCS = ['Referral letter or clinical notes', 'Imaging report', 'Laboratory results', 'Cytology report', 'Histology report', 'Immunohistochemistry (IHC) report', 'Genetic test report'];
  t('the checklist shows the seven documents by name, and one Continue',
    DOCS.every((d) => screenA.includes('<span class="check__text">' + ctx.esc(d) + '</span>')) && countButtons(screenA, 'tick') === 7 && countButtons(screenA, 'tick-continue') === 1,
    'the screen is missing a document or a Continue');
  /* The line that says what a document is shows under its name only while its box is ticked. */
  const labAbout = (router.tick_vocabularies.evidence_documents.items.find((x) => x.id === 'lab') || {}).about;
  t('no document is explained until its box is ticked', !/check__about/.test(screenA), 'an explanation shows with nothing ticked');
  await tick('lab', true);
  const screenLab = rend(() => ctx.renderLiveNode());
  t('ticking Laboratory results shows what it means, under its name and under no other', !!labAbout && screenLab.includes(ctx.esc(labAbout)) &&
    (screenLab.match(/check__about/g) || []).length === 1 && screenLab.indexOf('check__text">Laboratory results') < screenLab.indexOf(ctx.esc(labAbout)),
    'about: ' + labAbout + ', lines shown: ' + (screenLab.match(/check__about/g) || []).length);
  await tick('lab', false);
  t('unticking it takes the line away again', !/check__about/.test(rend(() => ctx.renderLiveNode())), 'the line stayed after the box was cleared');
  begin(fxDt, 'fx', 'fx_gate', 'C56.9');
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
    /Imaging report/.test(ctx.basisFromTrail()) && !/Imaging only/.test(ctx.basisFromTrail()) && /Imaging only/.test(ctx.state.trail.map((x) => x.value).join('|')),
    'basis: ' + ctx.basisFromTrail());
  await run(['histology', 'ihc']); await tap('tickopt', 1);
  t('a tier the clerk picks on the second screen is their answer and stays in "Suggested based on"',
    /Histology with other stains/.test(ctx.basisFromTrail()), 'basis: ' + ctx.basisFromTrail());
  {
    await run(['imaging', 'lab']);
    const trail = ctx.state.trail.map((x) => x.label + ': ' + x.value);
    t('the trail names the documents ticked, then the tier taken', /Imaging report, Laboratory results/.test(trail.join(' | ')) && ctx.state.trail.length === 2, JSON.stringify(trail));
    {
      /* The tier is the engine's description of the boxes ticked. Drawn as a second row it reads as
         a second question (registrar, 13 October 2026), so neither layout draws it, but it stays
         in the trail: indexes, stepping back and the case record are unchanged. */
      const rail = rend(() => ctx.renderRail()), rows = rend(() => ctx.renderTrailRows());
      const kept = ctx.state.trail.map((x) => x.value).join('|');
      t('the engine\'s own tier row is drawn in neither layout, though it stays in the trail',
        /Imaging report, Laboratory results/.test(rail) && /Imaging report, Laboratory results/.test(rows) &&
        !/Imaging and markers/.test(rail) && !/Imaging and markers/.test(rows) && /Imaging and markers/.test(kept),
        'rail: ' + rail.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').slice(0, 200));
    }
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

  /* ---- FIXTURE: a vocabulary with credits records exactly what was ticked ---------------
     The tier below overclaims on purpose: its own evidence lists five tests. The engine must
     record what the clerk ticked and nothing the tier assumed, and fall back to the tier's own
     list only when nothing ticked credits anything. */
  {
    const fc = {
      node_id: 'fc_gate', node_type: 'document_inventory', step_label: 'Evidence in file', question: 'q', hint: 'h',
      tick_list: { variable: 'fc_ticks', resolve: 'ask_siblings', items: [
        { id: 'smear', label: 'Smear', credits: ['Histology'] }, { id: 'trephine', label: 'Trephine', credits: ['Histology'] },
        { id: 'flow', label: 'Flow', credits: ['Flow cytometry'] }, { id: 'pcr', label: 'PCR', credits: ['Molecular/PCR'] },
        { id: 'note', label: 'Note', credits: ['Referral only'] }] },
      nos_fallback: null,
      options: [
        { label: 'Smear and more', next_node: 'fc_more', ticks: { requires: ['smear'] },
          captures: { evidence_tests: ['Histology', 'IHC', 'Flow cytometry', 'Cytogenetics/FISH', 'Molecular/PCR'] } },
        { label: 'No smear', next_node: 'fc_ref', ticks: { excludes: ['smear'] }, captures: { evidence_tests: ['Referral only'] } },
      ],
    };
    const fcDt = { morphology_entries: [], decision_trees: [{ tree_id: 'fc', entry_node: 'fc_gate', nodes: [fc, stub('fc_more'), stub('fc_ref')] }] };
    const runFc = async (ticks) => { begin(fcDt, 'fc', 'fc_gate', 'C42.1'); ctx.state.draft.ticks = ticks.slice(); await tap('tick-continue'); return ctx.state; };
    const ev = (st) => (st.captured.evidence_tests || []).join('|');
    let sc = await runFc(['smear', 'pcr']);
    t('credits: the evidence recorded is what was ticked, not the five tests the tier assumed',
      sc.nodeId === 'fc_more' && ev(sc) === 'Histology|Molecular/PCR', 'went to ' + sc.nodeId + ' with ' + ev(sc));
    sc = await runFc(['pcr', 'smear']);
    t('credits: the order the boxes were ticked in does not change the evidence', ev(sc) === 'Histology|Molecular/PCR', ev(sc));
    sc = await runFc(['smear', 'trephine']);
    t('credits: two boxes that prove the same test credit it once', ev(sc) === 'Histology', ev(sc));
    sc = await runFc([]);
    t('credits: nothing ticked falls back to the tier\'s own evidence', sc.nodeId === 'fc_ref' && ev(sc) === 'Referral only', 'went to ' + sc.nodeId + ' with ' + ev(sc));
    sc = await runFc(['flow']);
    t('credits: a test ticked without a smear is still recorded, and replaces the tier\'s assumption',
      sc.nodeId === 'fc_ref' && ev(sc) === 'Flow cytometry', 'went to ' + sc.nodeId + ' with ' + ev(sc));
  }

  /* One marker's result, and taking a marker back off, through the handlers the picker's buttons call.
     Shared by the fixture and the sweep below. */
  const mset = async (m, v) => { try { await ctx.handleOption('markerset', fakeEl({ 'data-m': m, 'data-v': v })); } catch (e) { thrown = e.message; } };
  const mdel = async (m) => { try { await ctx.handleOption('pickremove', fakeEl({ 'data-m': m })); } catch (e) { thrown = e.message; } };
  /* ---- FIXTURE: the marker picker (registrar, 13 October 2026) ------------------------
     The clerk adds the markers the report lists and gives each a result. A marker never added is
     not done, and the matcher already reads a marker never recorded as the same evidence as one
     recorded negative. The picker has no "not done" answer, and offers strength only where a
     rule on the node grades it. */
  {
    const pk = {
      node_id: 'fp_pick', node_type: 'ihc_checklist', step_label: 'Markers', question: 'q', hint: 'h',
      marker_entry: 'picker', marker_count_variable: 'fp_entered', captured_variables: ['fp_entered'],
      marker_groups: [{ group_label: 'Panel', markers: ['A', 'B', 'C', 'D'] }],
      branch_sequence: { order: ['A', 'B'], intensity_markers: ['A'], rule_count: 4 },
      resolution_logic: [
        { when: { fp_entered: 0 }, next_node: 'fp_none' },
        { positive: ['A:strong'], next_node: 'fp_strong' },
        { positive: ['A'], negative: ['B'], next_node: 'fp_a_not_b' },
        { next_node: 'fp_rest' },
      ],
      nos_fallback: { code: '8000', behavior_code: '3', name: 'x', reason: 'x' },
    };
    const dtp = { morphology_entries: [], decision_trees: [{ tree_id: 'fp', entry_node: 'fp_pick', nodes: [pk, ...['fp_none', 'fp_strong', 'fp_a_not_b', 'fp_rest'].map(stub)] }] };
    const screenP = () => rend(() => ctx.renderLiveNode());
    const openP = () => { begin(dtp, 'fp', 'fp_pick', 'C42.1'); return screenP(); };
    let hp = openP();
    t('picker: the screen offers the whole panel to add from, no result buttons and no "not done"',
      countButtons(hp, 'pickadd') === 4 && countButtons(hp, 'markerset') === 0 && !/not done|not read/i.test(hp.replace(/A marker you do not add is treated as not done\./, '')),
      'pickadd ' + countButtons(hp, 'pickadd') + ', markerset ' + countButtons(hp, 'markerset'));
    t('picker: the markers are a dropdown that opens from the search box, not a list standing open on the screen',
      /<div class="optbox optbox--dropdown">/.test(hp) && /placeholder="Search or choose a marker"/.test(hp), hp.slice(0, 240));
    await tap('pickadd', 0);
    t('picker: choosing a marker moves the focus to that marker\'s results, which closes the dropdown', /data-act="markerset"\]\[data-m="A"\]/.test(ctx.state.focusNext || ''), 'focusNext ' + ctx.state.focusNext);
    hp = screenP();
    t('picker: an added marker gets a row with its results and leaves the list; strength is offered only where a rule grades it',
      countButtons(hp, 'pickadd') === 3 && /aria-label="A: Positive"/.test(hp) && /aria-label="A: Strongly positive"/.test(hp) &&
      !/aria-label="A: Weakly positive"/.test(hp) && /aria-label="A: Negative"/.test(hp), 'pickadd ' + countButtons(hp, 'pickadd'));
    t('picker: Continue waits while an added marker has no result', /data-act="resolve" disabled/.test(hp), 'Continue was enabled');
    await mset('A', 'strong'); hp = screenP();
    t('picker: Continue is available once every added marker has a result', !/data-act="resolve" disabled/.test(hp), 'Continue stayed disabled');
    await tap('resolve');
    t('picker: Strongly positive A takes the rule that reads A strong, and the count is captured',
      ctx.state.nodeId === 'fp_strong' && ctx.state.captured.fp_entered === 1, 'went to ' + ctx.state.nodeId + ', count ' + ctx.state.captured.fp_entered);
    openP(); await tap('pickadd', 0); await mset('A', 'pos'); await tap('resolve');
    t('picker: a marker never added is not done, so a rule that needs it negative is met without it',
      ctx.state.nodeId === 'fp_a_not_b', 'went to ' + ctx.state.nodeId);
    openP(); await tap('resolve');
    t('picker: nothing entered is counted as zero and takes the rule that says so',
      ctx.state.nodeId === 'fp_none' && ctx.state.captured.fp_entered === 0, 'went to ' + ctx.state.nodeId + ', count ' + ctx.state.captured.fp_entered);
    openP(); await tap('pickadd', 0); await mset('A', 'strong'); await mdel('A'); await tap('resolve');
    t('picker: a marker taken back off is as if it was never added',
      ctx.state.nodeId === 'fp_none' && !ctx.state.markers.A, 'went to ' + ctx.state.nodeId + ', A ' + ctx.state.markers.A);
  }

  /* ---- SWEEP: every real marker picker --------------------------------------------- */
  {
    let nodesP = 0; const bad = [];
    for (const [g, dt] of dts) for (const tree of dt.decision_trees) for (const n of tree.nodes) {
      if (n.marker_entry !== 'picker') continue;
      nodesP++; treeOfNode.set(n, tree.nodes);
      const panel = [...new Set(n.marker_groups.flatMap((x) => x.markers))], where = 'group ' + g + ' ' + n.node_id;
      const stuck = () => ctx.state.stage === 'node' && ctx.state.nodeId === n.node_id;
      try {
        begin(dt, tree.tree_id, n.node_id, 'C42.1');
        const hh = rend(() => ctx.renderLiveNode());
        if (countButtons(hh, 'pickadd') !== panel.length) bad.push(where + ': offers ' + countButtons(hh, 'pickadd') + ' of its ' + panel.length + ' markers');
        await tap('resolve');
        if (stuck()) bad.push(where + ': Continue with nothing entered did not leave the node');
        begin(dt, tree.tree_id, n.node_id, 'C42.1');
        for (let k = 0; k < panel.length; k++) { await tap('pickadd', 0); await mset(panel[k], 'pos'); }
        await tap('resolve');
        if (stuck()) bad.push(where + ': Continue with every marker positive did not leave the node');
      } catch (e) { bad.push(where + ': threw ' + e.message); }
    }
    t('marker pickers in the data: ' + nodesP + ' node(s) offer every marker on their panel and resolve with nothing entered and with everything positive',
      nodesP > 0 && !bad.length, bad.slice(0, 4).join('\n        '));
    /* The acute lineage step: nothing entered must not ask what a panel covered when no panel was run. */
    let acute = null, acTree = null;
    for (const [g, dt] of dts) for (const tree of dt.decision_trees) for (const n of tree.nodes) if (n.node_id === 'ac_lineage_assignment') { acute = dt; acTree = tree; }
    if (acute) {
      treeOfNode.set(acTree.nodes.find((x) => x.node_id === 'ac_lineage_assignment'), acTree.nodes);
      begin(acute, acTree.tree_id, 'ac_lineage_assignment', 'C42.1');
      await tap('resolve');
      const r = ctx.state.result;
      t('acute lineage: nothing entered records 9801 as not performed, without asking what the panel covered',
        !!r && String(r.code) === '9801' && ctx.state.nodeId !== 'ac_alal_resolve' && ctx.state.captured.workup_status === 'incomplete',
        'node ' + ctx.state.nodeId + ', result ' + (r && r.code) + ', workup ' + ctx.state.captured.workup_status);
    }
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

  /* ---- the gonadal carcinoma picker: type the name and the option appears (registrar, 7 October 2026) ----
     Each gonad tree holds every subgroup Xd code its other nodes do not offer in one list. The list's filter box
     finds an option by its ICD-O-3.2 Preferred term or any ICD-O-3.2 synonym (`search_terms`, never shown), a case
     that came from the search box starts with the typed term already in the box, clearing the box shows the whole
     list and does not refill it, and taking the option records its code at the site already recorded. */
  {
    const dt10 = dts.get(10);
    const visible = (html) => (html.match(/<button class="opt[^"]*"( hidden)?/g) || []).filter((m) => !/hidden/.test(m)).length;
    const total = (html) => (html.match(/<button class="opt[^"]*"/g) || []).length;
    for (const [tree, entryNode, pickerNode, topo10, term] of [['g10_ovary', 'ov_epithelial', 'ov_carcinoma_other', 'C56.9', 'Adenosquamous carcinoma'], ['g10_testis', 'ts_histology', 'ts_carcinoma_other', 'C62.9', 'Adenosquamous carcinoma']]) {
      const nodes = dt10.decision_trees.find((x) => x.tree_id === tree).nodes;
      const picker = nodes.find((x) => x.node_id === pickerNode), entry = nodes.find((x) => x.node_id === entryNode);
      const to = entry.options.findIndex((o) => o.next_node === pickerNode);
      const want = picker.options.find((o) => o.label === term);
      const withSyn = picker.options.find((o) => (o.search_terms || []).length && !picker.options.some((q) => q !== o && q.label.toLowerCase().includes(o.search_terms[0].toLowerCase())));
      begin(dt10, tree, entryNode, topo10); ctx.state.group = 10; ctx.state.searchTerm = term;
      await tap('opt', to);
      const first = rend(() => ctx.renderLiveNode());
      t(tree + ': the entry node offers the picker, and a case from the search box starts with the typed term in the filter, showing only its match',
        to >= 0 && ctx.state.nodeId === pickerNode && first.includes('value="' + ctx.esc(term) + '"') && visible(first) >= 1 && visible(first) < total(first) && total(first) === picker.options.length,
        'to ' + to + ', node ' + ctx.state.nodeId + ', visible ' + visible(first) + ' of ' + total(first) + ' (' + picker.options.length + ' options)');
      ctx.state.draft['f:opt'] = withSyn.search_terms[0];
      const bySyn = rend(() => ctx.renderLiveNode());
      t(tree + ': an ICD-O-3.2 synonym finds the option although no label shows it', visible(bySyn) >= 1 && !bySyn.includes('>' + ctx.esc(withSyn.search_terms[0]) + '<'),
        'synonym ' + withSyn.search_terms[0] + ': visible ' + visible(bySyn));
      ctx.state.draft['f:opt'] = '';
      const cleared = rend(() => ctx.renderLiveNode());
      t(tree + ': clearing the box shows the whole list and does not refill it', visible(cleared) === picker.options.length && !cleared.includes('value="' + ctx.esc(term) + '"'),
        'visible ' + visible(cleared) + ' of ' + picker.options.length);
      await tap('opt', picker.options.indexOf(want));
      const res = ctx.state.result;
      t(tree + ': taking the option records its code and behaviour at the site already recorded',
        ctx.state.stage === 'output' && res && res.code === want.morphology_code && String(res.entry.behavior_code) === '3' && ctx.state.captured.topography === topo10,
        'stage ' + ctx.state.stage + ', code ' + (res && res.code) + ', topography ' + ctx.state.captured.topography);
    }
    /* A filter that is not asked to start from the search does not. */
    begin(dt10, 'g10_ovary', 'ov_epithelial', 'C56.9'); ctx.state.group = 10; ctx.state.searchTerm = 'Adenosquamous carcinoma';
    const plain = rend(() => ctx.renderLiveNode());
    t('a node that does not ask for it is not filtered by the searched term', !plain.includes('value="Adenosquamous carcinoma"'), 'filter prefilled on ov_epithelial');

    /* What the search box finds, the picker shows (review of 7 October 2026, finding 2). Every ICD-O-3.2 name the
       alias layer indexes (a Preferred term, a Synonym or a Related term) that maps to a code a gonad's picker offers
       must match one of that picker's options through the filter box's own matcher, or a case from the search box
       lands on a list with the typed name in the box and nothing visible. The curated names and the REDCap wording
       are not ICD-O-3.2 terms and are not held to it: a name the list cannot find starts no filter (next test). */
    const al10 = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'aliases', 'aliases_group_10.json'), 'utf8'))
      .filter((a) => String(a.origin_system || '').startsWith('ICD-O-3.2'));
    let pairs = 0; const missed = [];
    for (const [tree, pickerNode] of [['g10_ovary', 'ov_carcinoma_other'], ['g10_testis', 'ts_carcinoma_other']]) {
      const picker = dt10.decision_trees.find((x) => x.tree_id === tree).nodes.find((x) => x.node_id === pickerNode);
      for (const a of al10) {
        const own = picker.options.filter((o) => (a.maps_to_morphology_codes || []).includes(String(o.morphology_code)));
        if (!own.length) continue;
        pairs++;
        if (!own.some((o) => ctx.findMatch(ctx.findText({ label: o.label, find: (o.search_terms || []).join(' ') }), a.alias))) missed.push(tree + ': ' + a.alias);
      }
    }
    t('every ICD-O-3.2 name the search box indexes for a code a gonad picker offers is found by that picker\'s filter box', pairs > 100 && missed.length === 0,
      pairs + ' alias-by-picker pairs; not found: ' + missed.slice(0, 6).join(' | ') + (missed.length > 6 ? ' (+' + (missed.length - 6) + ')' : ''));

    /* A typed name no option matches starts no filter: the whole list shows, not an empty one. */
    {
      const nodes = dt10.decision_trees.find((x) => x.tree_id === 'g10_ovary').nodes;
      const entry = nodes.find((x) => x.node_id === 'ov_epithelial'), to = entry.options.findIndex((o) => o.next_node === 'ov_carcinoma_other');
      begin(dt10, 'g10_ovary', 'ov_epithelial', 'C56.9'); ctx.state.group = 10; ctx.state.searchTerm = 'Small cell carcinoma of the testis, hypercalcaemic type';
      await tap('opt', to);
      const none = rend(() => ctx.renderLiveNode());
      t('a typed name that matches no option starts no filter, so the whole list shows',
        ctx.state.nodeId === 'ov_carcinoma_other' && !/value="Small cell/.test(none) && visible(none) === total(none) && total(none) > 50,
        'node ' + ctx.state.nodeId + ', visible ' + visible(none) + ' of ' + total(none));
    }
  }

  /* ---- numeric_gate: "in the file, but in another unit or only described" (registrar, 7 October 2026) ----
     A gate that declares an `other_unit` band offers the answer, beside "Not documented in the file"; a gate
     that does not declare one does not ask it. The two answers exclude each other and a number excludes both.
     "Not documented" and "another unit" resolve to their own bands, and a number to its band as before. */
  {
    const stub = (id) => ({ node_id: id, node_type: 'morphology_only', step_label: id, question: id, options: [{ label: id + ' answer', morphology_code: '8000', behavior_code: '3' }], nos_fallback: { code: '8000', behavior_code: '3', name: 'x', reason: 'x' } });
    const gate = (withOther) => ({ node_id: 'fx_g', node_type: 'numeric_gate', step_label: 'Reading', variable: 'v', variable_label: 'Reading', unit: 'ng_per_ml',
      bands: [{ range: '>25', unit: 'ng_per_ml', next_node: 'fx_hi' }, { range: '<=25', unit: 'ng_per_ml', next_node: 'fx_lo' }, { range: 'not_documented', unit: 'ng_per_ml', next_node: 'fx_none' }]
        .concat(withOther ? [{ range: 'other_unit', unit: 'ng_per_ml', next_node: 'fx_other' }] : []), nos_fallback: null, insufficient_next_node: 'fx_none' });
    const gdt = (withOther) => ({ morphology_entries: [], decision_trees: [{ tree_id: 'fx', entry_node: 'fx_g', nodes: [gate(withOther), stub('fx_hi'), stub('fx_lo'), stub('fx_none'), stub('fx_other')] }] });
    const box = async (k, checked) => { try { await ctx.handleOption('draft', fakeEl({ 'data-k': k }, { type: 'checkbox', checked })); } catch (e) { thrown = e.message; } };
    const start = (withOther) => { begin(gdt(withOther), 'fx', 'fx_g'); ctx.state.trailAtGroupEntry = 0; };
    const ends = async (setup) => { start(true); await setup(); await tap('resolve'); return ctx.state.nodeId + '|' + String(ctx.state.captured.v) + '|' + (ctx.state.trail[ctx.state.trail.length - 1] || {}).value; };
    start(true);
    const withBox = rend(() => ctx.renderLiveNode());
    start(false);
    const withoutBox = rend(() => ctx.renderLiveNode());
    t('a gate that declares an other_unit band offers the answer, and one that does not, does not',
      /data-k="other_unit"/.test(withBox) && /data-k="not_documented"/.test(withBox) && !/data-k="other_unit"/.test(withoutBox) && /data-k="not_documented"/.test(withoutBox),
      'with: ' + /data-k="other_unit"/.test(withBox) + ', without: ' + /data-k="other_unit"/.test(withoutBox));
    start(true); await box('other_unit', true);
    const oBox = ctx.state.draft.other_unit === true && !ctx.state.draft.not_documented && /<input type="number"[^>]* disabled/.test(rend(() => ctx.renderLiveNode()));
    await box('not_documented', true);
    const nBox = ctx.state.draft.not_documented === true && ctx.state.draft.other_unit === false;
    await box('other_unit', true);
    const oAgain = ctx.state.draft.other_unit === true && ctx.state.draft.not_documented === false;
    t('the two "no number" answers exclude each other, and either disables the number box', oBox && nBox && oAgain, JSON.stringify([oBox, nBox, oAgain, ctx.state.draft]));
    const r = {
      other: await ends(() => box('other_unit', true)),
      none: await ends(() => box('not_documented', true)),
      high: await ends(async () => { await draftSet('value', '30', 'text'); }),
      edge: await ends(async () => { await draftSet('value', '25', 'text'); }),
      blank: await ends(async () => {}),
    };
    t('"another unit" goes to its own band, "not documented" to its own, a number to its band, and a blank reading is not documented',
      /^fx_other\|other_unit\|in another unit or only described$/.test(r.other) && /^fx_none\|null\|/.test(r.none) && /^fx_hi\|30\|/.test(r.high) && /^fx_lo\|25\|/.test(r.edge) && /^fx_none\|null\|/.test(r.blank), JSON.stringify(r));
    start(false); await box('other_unit', true); await tap('resolve');
    t('on a gate with no other_unit band the answer cannot send the case anywhere: it falls to the gate\'s own fallback', ctx.state.nodeId === 'fx_none', 'node ' + ctx.state.nodeId);
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
    t('a result in the panel ticks Laboratory results on the checklist that follows',
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
      for (const x of ['0x1A', '0b11', '1e3', '12abc', 'Infinity', '--5', '5%', '-5', '1,000,000', '1.2.3', '.5', '>', '<', '>>5', '><5', '>-5', '5>', '<1e3', '>0x1', '=5', '≥5', '> 1,000,000']) if (await attempt(x)) wrong.push(x + ' accepted');
      for (const x of ['2.1', '2,4', '10', '0.05', '>1210', '<0.5', '> 1210', '<1', '>1.5']) if (!(await attempt(x))) right.push(x + ' refused');
      t('a result is digits with at most one decimal mark, after a > or < for a limit: hex, binary, exponent, signs and thousands marks are refused',
        !wrong.length && !right.length, wrong.concat(right).join(', '));
      startLabs(); await typeRow(0, '> 1210', 'ng/mL'); await typeRow(1, '<0.5'); await tap('labs-continue');
      const afp = ctx.state.labs.find((l) => l.id === 'afp'), ldh = ctx.state.labs.find((l) => l.id === 'ldh');
      t('a limit is recorded as typed, without the space, and printed with its number and unit on the result and the trail',
        afp && afp.value === '>1210' && afp.inFile && ldh && ldh.value === '<0.5' &&
        /Alpha-fetoprotein \(AFP\)<\/b><span>&gt;1210 ng\/mL/.test(rend(() => ctx.labResultsBlock())) && /&gt;1210 ng\/mL/.test(rend(() => ctx.esc(ctx.state.trail[0].value))),
        JSON.stringify(ctx.state.labs) + ' ' + rend(() => ctx.labResultsBlock()).slice(0, 300));
      startLabs(); await typeRow(0, '>1210'); await tap('labs-continue'); await tap('rewind', 0);
      t('stepping back to a recorded limit shows it as typed', /value="&gt;1210"/.test(rend(() => ctx.renderLiveNode())), rend(() => ctx.renderLiveNode()).slice(0, 300));
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
  /* ---- a referral that recaptures the site: a deposit's site is not the primary's ---------------
     Every refer branch in the data that says `recapture_site`, to a built group, is driven: the
     referral does not print the deposit's site as the case's, the hop drops it and asks the
     primary's, the case enters the receiving group with the site the clerk gives, and stepping
     back works at both ends. The contrast is a referral that does not recapture, which keeps its site. */
  {
    const crosswalk = topo.coarse_organ_crosswalk;
    const selectable = Object.keys(topo.topography_lookup).filter((c) => crosswalk.some((r) => r.codes.includes(c)));
    const hasSiteWhen = (o) => !!o && typeof o === 'object' && (Array.isArray(o) ? o.some(hasSiteWhen) :
      ((o.when && typeof o.when === 'object' && o.when.topography !== undefined) || Object.values(o).some(hasSiteWhen)));
    const readsSite = (g) => {
      const meta = (router.groups || {})[String(g)] || {};
      return !!meta.tree_routing || (dts.get(g) ? hasSiteWhen(dts.get(g).decision_trees) : false);
    };
    const siteFor = (g) => selectable.find((c) => { const cg = topo.topography_lookup[c].candidate_groups; return Array.isArray(cg) && cg.includes(g); }) || selectable[0];
    const startSite = (g, treeId) => {
      const tr = ((router.groups || {})[String(g)] || {}).tree_routing;
      const rule = tr && tr.rules.find((r) => r.tree_id === treeId);
      return (rule && rule.topography_in.find((c) => selectable.includes(c))) || siteFor(g);
    };
    const atSiteUx = () => ['site_system', 'site'].includes(ctx.state.stage);
    const pickSiteUx = async (code) => {
      if (ctx.state.stage === 'site_system') {
        const organ = ctx.systemRows().find((row) => row.codes.includes(code)).organ;
        await tap('site_system', ctx.siteSystems().findIndex((x) => x.organs.includes(organ)));
      }
      if (ctx.state.stage === 'site') await tap('site', ctx.organRows().findIndex((row) => row.codes.includes(code)));
      if (ctx.state.stage === 'site_region') await tap('site_region', ctx.regionOptions(ctx.state.organSystem).findIndex((o) => o.topography === code));
    };
    const cases = [];
    for (const [g, dt] of dts) for (const tree of dt.decision_trees) for (const n of tree.nodes) {
      const walk = (o, path) => {
        if (!o || typeof o !== 'object') return;
        if (Array.isArray(o)) { o.forEach((x, i) => walk(x, path.concat(i))); return; }
        if (o.refer_group !== undefined && o.recapture_site === true && (router.groups[String(o.refer_group)] || {}).built) cases.push({ g, dt, tree, n, o, path });
        Object.keys(o).forEach((k) => walk(o[k], path.concat(k)));
      };
      walk(n.options, []);
    }
    const bad = [], seen = new Set();
    for (const c of cases) {
      const label = 'group ' + c.g + ' ' + c.n.node_id + ' "' + (c.o.label || c.o.finding || c.o.descriptor || ('option ' + c.n.options.indexOf(c.o))) + '" -> ' + c.o.refer_group;
      const to = c.o.refer_group, reads = readsSite(to), oi = c.n.options.indexOf(c.o);
      if (oi < 0) continue;
      seen.add(c.g + ':' + to + ':' + reads);
      begin(c.dt, c.tree.tree_id, c.n.node_id, startSite(c.g, c.tree.tree_id));
      ctx.state.group = c.g;
      const carried = ctx.state.captured.topography;
      await tap('opt', oi);
      const st = ctx.state;
      if (!(st.stage === 'output' && st.result && st.result.referral && st.result.recaptureSite === true)) { bad.push(label + ': no recapture referral, stage ' + st.stage); continue; }
      const out = rend(() => ctx.renderOutput());
      if (/Topography code/.test(out)) bad.push(label + ': the referral screen prints the deposit\'s site as the case\'s');
      if (!/data-act="hop"/.test(out)) { bad.push(label + ': no hop offered with no site on the case'); continue; }
      await tap('hop');
      if (!(atSiteUx() && st.group === to && st.recordGroup === to && st.captured.topography === undefined && st.captured.organ_system === undefined)) {
        bad.push(label + ': after the hop stage ' + st.stage + ', group ' + st.group + ', record group ' + st.recordGroup + ', topography ' + st.captured.topography); continue;
      }
      if (st.siteRecordOnly !== !reads) bad.push(label + ': record-only is ' + st.siteRecordOnly + ' for a group that ' + (reads ? 'reads' : 'does not read') + ' the site');
      const scr = rend(() => (ctx.state.stage === 'site_system' ? ctx.renderSiteSystem() : ctx.renderSite()));
      if (!/Record the site of the primary tumour/.test(scr)) bad.push(label + ': the site screen does not ask for the primary\'s site');
      if (/data-act="site-unstated"/.test(scr) === reads) bad.push(label + ': the "not stated" answer is ' + (reads ? 'offered to a group that reads the site' : 'missing for a group that does not'));
      if (/data-act="site-unstated"/.test(scr) && !reads) {
        await tap('site-unstated');
        const su = ctx.state;
        if (!(su.group === to && su.captured.topography === undefined && !['site_system', 'site'].includes(su.stage))) bad.push(label + ': "not stated" ends at stage ' + su.stage + ', group ' + su.group);
        begin(c.dt, c.tree.tree_id, c.n.node_id, startSite(c.g, c.tree.tree_id)); ctx.state.group = c.g;
        await tap('opt', oi); await tap('hop');
      }
      const code = siteFor(to);
      await pickSiteUx(code);
      const en = ctx.state, labels = en.trail.map((x) => x.label);
      /* A group that asks its tree (Group II) stops at that question, with the site recorded. */
      if (!(en.group === to && ['node', 'handoff'].includes(en.stage) && en.captured.topography === code && en.recordGroup === null)) {
        bad.push(label + ': after recording ' + code + ' stage ' + en.stage + ', group ' + en.group + ', topography ' + en.captured.topography + ', record group ' + en.recordGroup); continue;
      }
      /* An organ with one code records it without a region question, so no Topography entry. */
      if (!['Referral', 'Site of origin'].every((l) => labels.includes(l))) bad.push(label + ': the trail does not show the referral and the site: ' + labels.join(', '));
      /* Back to the site, and a different one. */
      const ti = labels.lastIndexOf('Site of origin');
      await tap('rewind', ti);
      if (!(ctx.state.stage === 'site_system' && ctx.state.recordGroup === to && ctx.state.captured.topography === undefined)) { bad.push(label + ': stepping back to the body system gave stage ' + ctx.state.stage + ', record group ' + ctx.state.recordGroup); continue; }
      const other = selectable.find((x) => x !== code && ctx.systemRows().some((row) => row.codes.includes(x)));
      await pickSiteUx(other);
      if (!(ctx.state.group === to && ['node', 'handoff'].includes(ctx.state.stage) && ctx.state.captured.topography === other)) bad.push(label + ': a second site gave stage ' + ctx.state.stage + ', topography ' + ctx.state.captured.topography);
      /* Back past the site to the referral: the first group's own screen returns with its site. */
      await tap('rewind', ctx.state.trail.findIndex((x) => x.label === 'Referral'));
      if (!(ctx.state.stage === 'output' && ctx.state.result && ctx.state.result.referral && ctx.state.recordGroup === null && ctx.state.captured.topography === carried)) bad.push(label + ': stepping back to the referral gave stage ' + ctx.state.stage + ', record group ' + ctx.state.recordGroup);
    }
    t('every referral that recaptures the site hides the deposit\'s site, drops it on the hop, asks the primary\'s, enters the group with it, and steps back (' + cases.length + ' branches to built groups)',
      cases.length > 20 && bad.length === 0, cases.length + ' branches; ' + bad.length + ' problem(s): ' + bad.slice(0, 3).join(' | '));
    t('the walk covered a receiving group that reads the site and one that does not',
      [...seen].some((k) => k.endsWith(':true')) && [...seen].some((k) => k.endsWith(':false')), [...seen].join(' '));
    /* The contrast: a referral without it keeps the site, and a leukaemia is recorded at the marrow. */
    {
      const dt10 = dts.get(10), find = (id, g, text) => {
        const node = dt10.decision_trees.flatMap((tr) => tr.nodes).find((x) => x.node_id === id);
        const tree = dt10.decision_trees.find((tr) => tr.nodes.some((x) => x.node_id === id));
        return { node, tree, i: node.options.findIndex((o) => o.refer_group === g && (!text || text.test(o.label))) };
      };
      const run = async (id, g, text, site) => {
        const f = find(id, g, text);
        begin(dt10, f.tree.tree_id, id, site); ctx.state.group = 10;
        await tap('opt', f.i);
        const out = rend(() => ctx.renderOutput());
        const hasRow = /Topography code/.test(out);
        await tap('hop');
        return { hasRow, topography: ctx.state.captured.topography, group: ctx.state.group, stage: ctx.state.stage, rec: ctx.state.recordGroup };
      };
      const lymph = await run('ov_other', 2, /Lymphoma/, 'C56.9');
      t('a referral that does not recapture keeps printing the site and takes it into the next group',
        lymph.hasRow && lymph.topography === 'C56.9' && lymph.group === 2 && lymph.rec === null, JSON.stringify(lymph));
      const leuk = await run('ov_other', 1, /^Leukaemic/, 'C56.9');
      t('leukaemic infiltration of the ovary enters Group I at the bone marrow (WHO Rule E)', leuk.topography === 'C42.1' && leuk.group === 1, JSON.stringify(leuk));
      const leukT = await run('ts_other', 1, /^Leukaemic/, 'C62.9');
      t('leukaemic infiltration of the testis enters Group I at the bone marrow (WHO Rule E)', leukT.topography === 'C42.1' && leukT.group === 1, JSON.stringify(leukT));
      const ms = await run('ov_other', 1, /^Myeloid sarcoma/, 'C56.9');
      t('a myeloid sarcoma of the ovary keeps the ovary as its site (WHO Rule E exception)', ms.topography === 'C56.9' && ms.group === 1, JSON.stringify(ms));
      /* A case opened from a presentation that fixes the site list (a blood presentation lists the marrow
         alone) is asked the primary's site from the whole list after a recapture hop. */
      {
        const blood = router.archetypes.find((a) => a.auto_topography);
        const f10 = dt10.decision_trees.flatMap((tr) => tr.nodes).find((x) => x.node_id === 'ov_deposit');
        const i4 = f10.options.findIndex((o) => o.refer_group === 4);
        begin(dt10, 'g10_ovary', 'ov_deposit', 'C56.9'); ctx.state.group = 10; ctx.state.archetype = blood;
        const before = ctx.systemRows().length;
        await tap('opt', i4); await tap('hop');
        t('after a recapture hop the primary\'s site is asked from every organ system, not only those the opening presentation fixed',
          !!blood && before < topo.coarse_organ_crosswalk.length && ctx.state.stage === 'site_system' && ctx.systemRows().length === topo.coarse_organ_crosswalk.length,
          'system rows ' + before + ' then ' + ctx.systemRows().length + ' of ' + topo.coarse_organ_crosswalk.length);
      }
      /* A recapture referral to a group that is not built hides the deposit's site and offers no hop, and a
         recapture branch on an ihc rule (resolution_logic) records the flag when the engine refers. */
      ctx.reset(); Object.assign(ctx.state, { router, topography: topo, stage: 'output', group: 3, dt: dts.get(3), captured: { topography: 'C71.0' } });
      ctx.state.result = { referral: true, group: 12, note: 'n', recaptureSite: true };
      const unbuilt = rend(() => ctx.renderOutput());
      t('a referral that asks for the primary\'s site and names a group not built hides the deposit\'s site and offers no hop', !/Topography code/.test(unbuilt) && !/data-act="hop"/.test(unbuilt), unbuilt.slice(0, 300));
      const ruleHolders = [];
      for (const [g, dt] of dts) for (const tr of dt.decision_trees) for (const n of tr.nodes) for (const r of (n.resolution_logic || [])) if (r.refer_group !== undefined && r.recapture_site === true) ruleHolders.push({ g, n: n.node_id, r });
      let ruleBad = 0;
      for (const h of ruleHolders) { ctx.reset(); Object.assign(ctx.state, { router, topography: topo, group: h.g, dt: dts.get(h.g) }); ctx.refer(h.r); if (!(ctx.state.result && ctx.state.result.recaptureSite === true && ctx.state.stage === 'output')) ruleBad++; }
      t('an ihc rule that asks for the primary\'s site records it when the engine refers (' + ruleHolders.length + ' rule(s))', ruleHolders.length > 0 && ruleBad === 0, ruleHolders.length + ' rules, ' + ruleBad + ' failed');
      /* A case with no site on it (a typed term whose site was "not stated") is offered the hop into a group
         that routes by site when the referral asks for the primary's site, and still is not when it does not. */
      ctx.reset(); Object.assign(ctx.state, { router, topography: topo, stage: 'output', group: 7, dt: dts.get(7) });
      ctx.state.result = { referral: true, group: 10, note: 'n', recaptureSite: true };
      t('a referral that asks for the primary\'s site offers the hop into a group that routes by site although the case has no site',
        /data-act="hop"/.test(rend(() => ctx.renderOutput())), 'no hop offered');
      ctx.state.result = { referral: true, group: 10, note: 'n' };
      t('and a referral that does not still offers none', !/data-act="hop"/.test(rend(() => ctx.renderOutput())), 'a hop was offered');
    }
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
  /* ---- FIXTURE: "Uncertain subtype" names the behaviour of its fallback ---- */
  {
    const entry = (b, name) => ({ morphology_code: '9391', behavior_code: b, morphology_name: name, iccc3_subgroup_id: 'IIIa', iccc3_subgroup_name: 'x' });
    const fb = { node_id: 'fx_nos', node_type: 'morphology_only', step_label: 'Subtype', question: 'q', options: [], nos_fallback: { code: '9391', behavior_code: '3', name: 'Ependymoma, NOS', reason: 'r' } };
    begin({ morphology_entries: [entry('1', 'Sellar ependymoma'), entry('3', 'Ependymoma, NOS')], decision_trees: [{ tree_id: 'fx', entry_node: 'fx_nos', nodes: [fb] }] }, 'fx', 'fx_nos', 'C72.0');
    await tap('escape-nos');
    const e = ctx.state.result && ctx.state.result.entry;
    t('"Uncertain subtype" records the behaviour its fallback names, not the first entry listed for that code', !!e && e.behavior_code === '3' && e.morphology_name === 'Ependymoma, NOS', JSON.stringify(e && [e.morphology_code, e.behavior_code, e.morphology_name]));
  }
  /* ---- FIXTURE: WHO Rule J, a compound term typed with its roots in another order ---- */
  {
    ctx.reset();
    ctx.state.aliasIndex = { Fibromyxosarcoma: [9], Osteochondrosarcoma: [8], 'Rhabdomyosarcoma, NOS': [9] };
    const found = (q, alias) => ctx.searchAlias(q).some((h) => h.alias === alias);
    t('a compound term typed with hyphens, spaces or its roots swapped finds the listed term',
      found('fibro-myxo-sarcoma', 'Fibromyxosarcoma') && found('myxo fibro sarcoma', 'Fibromyxosarcoma') && found('chondro-osteo-sarcoma', 'Osteochondrosarcoma') && found('Fibromyxosarcoma', 'Fibromyxosarcoma'),
      JSON.stringify(['fibro-myxo-sarcoma', 'myxo fibro sarcoma', 'chondro-osteo-sarcoma'].map((q) => ctx.searchAlias(q).map((h) => h.alias))));
    t('the swapped-roots search keeps the last word last and matches nothing else', !found('sarcoma-myxo-fibro', 'Fibromyxosarcoma') && ctx.searchAlias('-').length === 0,
      JSON.stringify([ctx.searchAlias('sarcoma-myxo-fibro').map((h) => h.alias), ctx.searchAlias('-').map((h) => h.alias)]));
  }
  /* ---- FIXTURE: a discriminator answer can keep a group through the site step (WHO Rule D) ---- */
  {
    const savedRouter = ctx.state.router, savedTopo = ctx.state.topography;
    const router = { discriminators: { dx: { variable: 'dx', narrows: { lymph: { drop: [1], keep_on_site: [2] }, other: { drop: [2] } } } } };
    const run = (answer, cands, siteGroups) => {
      ctx.reset();
      Object.assign(ctx.state, { router, archetype: { dual_group_discriminator: 'dx' }, candidates: cands.slice(),
        topography: { topography_lookup: { 'C64.9': { candidate_groups: siteGroups } } } });
      ctx.state.captured = { topography: 'C64.9', dx: answer };
      ctx.narrowBySite();
      return JSON.stringify(ctx.state.candidates);
    };
    t('a group the answer keeps survives the site step when the site does not list it', run('lymph', [2, 9], [6]) === '[2]', run('lymph', [2, 9], [6]));
    t('the site still narrows every other candidate', run('lymph', [2, 6, 9], [6]) === '[2,6]', run('lymph', [2, 6, 9], [6]));
    t('an answer that keeps nothing lets the site take the family away', run('other', [6, 9], [6]) === '[6]' && run('other', [1, 2, 9], [6]) === '[6]', JSON.stringify([run('other', [6, 9], [6]), run('other', [1, 2, 9], [6])]));
    t('keep_on_site never adds a group that was not already a candidate', run('lymph', [9], [6]) === '[6]', run('lymph', [9], [6]));
    ctx.reset(); ctx.state.router = savedRouter; ctx.state.topography = savedTopo;
  }
  /* ---- FIXTURE: a group that occurs at any site survives only a site that names none of the term's groups ---- */
  {
    const savedRouter = ctx.state.router, savedTopo = ctx.state.topography, savedIndex = ctx.state.aliasIndex;
    const router = { groups: { 1: { name: 'One', built: false }, 2: { name: 'Two', built: false, occurs_at_any_site: true } } };
    const topo = { topography_lookup: { X1: { candidate_groups: [1] }, X2: { candidate_groups: [2] }, X6: { candidate_groups: [6] }, X12: { candidate_groups: [1, 2] } } };
    const run = (code) => {
      ctx.reset();
      Object.assign(ctx.state, { router, topography: topo, aliasIndex: { T: [1, 2] }, searchTerm: 'T' });
      ctx.state.captured = { topography: code };
      ctx.afterSearchSite();
      return ctx.state.stage + ':' + ctx.state.group;
    };
    t('a site that names one of the term\'s groups decides, although another group occurs at any site', run('X1') === 'handoff:1' && run('X2') === 'handoff:2', JSON.stringify([run('X1'), run('X2')]));
    t('a site that names none of the term\'s groups takes the group that occurs at any site', run('X6') === 'handoff:2', run('X6'));
    t('a site that names both of the term\'s groups still stops', run('X12') === 'search_unresolved:null', run('X12'));
    ctx.reset(); ctx.state.router = savedRouter; ctx.state.topography = savedTopo; ctx.state.aliasIndex = savedIndex;
  }
  /* ---- FIXTURE: a group that occurs at its routed sites survives a site its candidate list omits, for a term its own entries place there ---- */
  {
    const savedRouter = ctx.state.router, savedTopo = ctx.state.topography, savedIndex = ctx.state.aliasIndex, savedCache = ctx.groupCache.get(2);
    const routing = { variable: 'topography', rules: [{ tree_id: 'ta', topography_in: ['C11.1', 'C22.0', 'C41.4'] }], default: { tree_id: 'td' } };
    const mk = (flag) => ({ groups: {
      1: { name: 'One', built: false },
      2: Object.assign({ name: 'Two', built: false, tree_routing: routing }, flag === undefined ? {} : { occurs_at_routed_sites: flag }) } });
    const topo = { topography_lookup: { 'C11.1': { candidate_groups: [1] }, 'C22.0': { candidate_groups: [6] }, 'C41.4': { candidate_groups: [2] }, 'C64.9': { candidate_groups: [6] }, 'C30.0': { candidate_groups: [1, 2] } } };
    /* Term T is placed by its entry at the three routed sites; term G only at C41.4, as a term ICCC places at one site is. */
    const loaded = () => ctx.groupCache.set(2, { dt: { morphology_entries: [
      { morphology_code: '1111', behavior_code: '3', primary_sites: ['C11.0-C11.9', 'C22.0', 'C41.0-C41.9'] },
      { morphology_code: '2222', behavior_code: '3', primary_sites: ['C41.4'] }] },
      aliases: [{ alias: 'T', maps_to_morphology_codes: ['1111'] }, { alias: 'G', maps_to_morphology_codes: ['2222'] }, { alias: 'N', maps_to_morphology_codes: [] }] });
    const run = (router, code, groups, term) => {
      ctx.reset();
      Object.assign(ctx.state, { router, topography: topo, aliasIndex: { T: groups || [2], G: [2], N: [2] }, searchTerm: term || 'T' });
      ctx.state.captured = { topography: code };
      ctx.afterSearchSite();
      return ctx.state.stage + ':' + ctx.state.group;
    };
    loaded();
    const on = mk(true);
    t('a site that a routing rule names and the site\'s own list omits takes the group, for a term its entries place there', run(on, 'C22.0') === 'handoff:2', run(on, 'C22.0'));
    t('a site no routing rule names still stops, although the group routes a default tree', run(on, 'C64.9') === 'search_unresolved:null', run(on, 'C64.9'));
    t('a routed site the term\'s own entries do not list stops: a term placed only at one site is not entered at another', run(on, 'C22.0', [2], 'G') === 'search_unresolved:null' && run(on, 'C41.4', [2], 'G') === 'handoff:2', JSON.stringify([run(on, 'C22.0', [2], 'G'), run(on, 'C41.4', [2], 'G')]));
    t('a term that names no entry has no evidence and stops', run(on, 'C22.0', [2], 'N') === 'search_unresolved:null', run(on, 'C22.0', [2], 'N'));
    t('a term filed under several groups is not taken by the routed-site fallback', run(on, 'C22.0', [1, 2]) === 'search_unresolved:null', run(on, 'C22.0', [1, 2]));
    ctx.groupCache.delete(2);
    t('a group whose file is not loaded has no evidence and stops', run(on, 'C22.0') === 'search_unresolved:null', run(on, 'C22.0'));
    loaded();
    t('without the flag a routed site the list omits still stops', run(mk(undefined), 'C22.0') === 'search_unresolved:null' && run(mk(false), 'C22.0') === 'search_unresolved:null', JSON.stringify([run(mk(undefined), 'C22.0'), run(mk(false), 'C22.0')]));
    t('a site that lists a group of the term decides, and the routed group does not tie with it', run(on, 'C11.1', [1, 2]) === 'handoff:1' && run(on, 'C41.4', [1, 2]) === 'handoff:2', JSON.stringify([run(on, 'C11.1', [1, 2]), run(on, 'C41.4', [1, 2])]));
    t('a site that names both of the term\'s groups still stops', run(on, 'C30.0', [1, 2]) === 'search_unresolved:null', run(on, 'C30.0', [1, 2]));
    if (savedCache) ctx.groupCache.set(2, savedCache); else ctx.groupCache.delete(2);
    ctx.reset(); ctx.state.router = savedRouter; ctx.state.topography = savedTopo; ctx.state.aliasIndex = savedIndex;
  }
  /* ---- FIXTURES on the real data: the "take the higher" decisions of 7 October 2026 ---- */
  {
    /* BAP1 loss is recorded and changes neither the code nor the behavior of a meningioma. The
       subtype, band and invasion values are read from the node's own rules. */
    begin(dts.get(3), 'g3_meninges', 'mn_grade_assembly', 'C70.0');
    const n = ctx.findNode('mn_grade_assembly');
    const vals = (k) => [...new Set(n.resolution_logic.flatMap((r) => [].concat((r.when || {})[k] === undefined ? [] : (r.when || {})[k])))];
    const subs = [undefined, ...vals('meningioma_subtype')], bands = vals('mitotic_band'), inv = [undefined, ...vals('brain_invasion')];
    const res = (sub, band, inva, bap) => {
      const c = ctx.state.captured;
      for (const k of ['meningioma_subtype', 'mitotic_band', 'brain_invasion', 'bap1_status']) delete c[k];
      if (sub) c.meningioma_subtype = sub;
      c.mitotic_band = band;
      if (inva) c.brain_invasion = inva;
      if (bap) c.bap1_status = bap;
      const r = ctx.matchRules(n.resolution_logic);
      return r ? r.morphology_code + '/' + r.behavior_code : 'none';
    };
    const diffs = [];
    for (const sub of subs) for (const band of bands) for (const inva of inv) {
      const a = res(sub, band, inva, 'altered'), z = res(sub, band, inva, undefined);
      if (a !== z) diffs.push([sub, band, inva].join('|') + ' ' + a + ' vs ' + z);
    }
    t('BAP1 loss is recorded and changes neither the code nor the behavior of a meningioma, for every subtype, mitotic band and brain-invasion answer',
      subs.length > 5 && bands.length > 2 && diffs.length === 0, diffs.length + ' differ: ' + diffs.slice(0, 3).join('; '));
    t('a rhabdoid meningioma with BAP1 loss and a grade 3 count records Papillary meningioma 9538/3', res('rhabdoid', 'g3_band', undefined, 'altered') === '9538/3', res('rhabdoid', 'g3_band', undefined, 'altered'));
  }
  {
    /* A follicular lymphoma grade ticked twice or more records the highest grade. The expected code is read
       from the digits in each marker's own words, a second reading of the same text. */
    begin(dts.get(2), 'g2_lymphoid_main', 'g2_follicular', 'C77.9');
    const n = ctx.findNode('g2_follicular');
    const grp = n.marker_groups.find((g) => /^Grade stated/.test(g.group_label));
    const names = grp ? grp.markers : [];
    const gradeOf = (m) => Math.max(...(m.match(/[123]/g) || [0]).map(Number));
    const want = { 3: '9698', 2: '9691', 1: '9695' };
    const bad = [];
    for (let mask = 1; mask < (1 << names.length); mask++) {
      const ticked = names.filter((_, i) => mask & (1 << i));
      ctx.state.markers = {};
      for (const m of ['Follicular pattern, adult type', 'BCL2 positive', 'CD10'].concat(ticked)) ctx.state.markers[m] = 'pos';
      const r = ctx.matchRules(n.resolution_logic), got = r ? r.morphology_code : 'none';
      const expect = want[Math.max(...ticked.map(gradeOf))];
      if (got !== expect) bad.push(ticked.join(' + ') + ' -> ' + got + ' (wanted ' + expect + ')');
    }
    t('a follicular lymphoma grade ticked twice or more records the highest grade, for every combination of the six grade markers',
      names.length === 6 && bad.length === 0, names.length + ' grade markers; ' + bad.slice(0, 3).join('; '));
  }
  {
    /* A retinocytomatous area does not set the code when the report states a poorer grade or a growth pattern. Since the registrar's
       ruling of 14 October 2026 (RQ2, RQ6) the area is a box on the enucleation report's own tick screen, read in file order. */
    const rb = async (ids) => {
      begin(dts.get(5), 'g5_retinoblastoma', 'rb_enucleation_report', 'C69.2');
      await tickSet(ctx.tickList(ctx.node()).items.map((x) => x.id), new Set(ids)); await tap('tick-continue');
      const e = ctx.state.result && ctx.state.result.entry;
      return e ? e.morphology_code + '/' + e.behavior_code : 'no code (stage ' + ctx.state.stage + ')';
    };
    const g3 = await rb(['area', 'g34']), dif = await rb(['area', 'diffuse']), low = await rb(['area']);
    t('a retinocytomatous area inside a tumour with a poorer grade or severe anaplasia records Retinoblastoma, undifferentiated 9512/3', g3 === '9512/3', g3);
    t('a retinocytomatous area with a stated diffuse infiltrating pattern records Retinoblastoma, diffuse 9513/3', dif === '9513/3', dif);
    t('a retinocytomatous area with nothing poorer stated still records Retinoblastoma, differentiated 9511/3', low === '9511/3', low);
  }

  /* Guided entry: presentation wording, body system, organ, and the marrow-aspirate question
     (registrar, 13 October 2026; spec 2026-10-13-guided-entry-site-flow-design.md). Driven through
     the handlers the buttons call, on the real router and crosswalk. */
  {
    const WORDS = {
      blood_marrow: 'Pale, bruising or bleeding, repeated infections or bone pain, with an abnormal blood count',
      solid_mass: 'A lump, mass or swelling',
      lymphadenopathy: 'Enlarged lymph nodes',
      organ_functional_sign: 'A symptom from an organ, such as a white pupil, a bulging eye, blood in the urine, jaundice or signs of raised pressure in the head',
      cutaneous_mucosal_lesion: 'A lesion, sore or growth on the skin or on a mucous surface',
      incidental_imaging_finding: 'An abnormal mass found by chance on a scan or X-ray',
      unsure: 'More than one of these, or not sure',
    };
    const wrongWords = router.archetypes.filter((a) => a.label !== WORDS[a.archetype_id]).map((a) => a.archetype_id);
    t('the seven presentations are worded as the registrar ruled', router.archetypes.length === 7 && wrongWords.length === 0, 'wrong: ' + wrongWords.join(', '));

    const start = async (id) => {
      ctx.reset(); Object.assign(ctx.state, { router, topography: topo, aliasIndex: {} });
      await tap('guided', 0); await tap('archetype', router.archetypes.findIndex((a) => a.archetype_id === id));
    };
    const toSite = async (systemId, organId, code) => {
      if (ctx.state.stage === 'site_system') await tap('site_system', ctx.siteSystems().findIndex((x) => x.system.system_id === systemId));
      if (ctx.state.stage === 'site') await tap('site', ctx.organRows().findIndex((r) => r.organ === organId));
      if (ctx.state.stage === 'site_region') await tap('site_region', ctx.regionOptions(ctx.state.organSystem).findIndex((o) => o.topography === code));
    };
    const answer = async (value) => { const d = ctx.discriminator(); await tap('discriminator', d.options.findIndex((o) => o.value === value)); };
    const labelsOf = () => ctx.state.trail.map((x) => x.label);
    const cands = () => JSON.stringify((ctx.state.candidates || []).slice().sort((a, b) => a - b));

    /* A blood presentation fixes the system and the organ: the clerk sees only the region screen,
       and the marrow question is answered by the site. */
    await start('blood_marrow');
    t('a blood presentation skips the system and organ screens and asks the region, in its own words',
      ctx.state.stage === 'site_region' && /Which of these does the disease arise in\?/.test(rend(() => ctx.renderSiteRegion())) &&
      labelsOf().join() === 'Presentation', ctx.state.stage + ' ' + labelsOf().join());
    await toSite('blood_haematopoietic', 'blood_marrow_haematopoietic', 'C42.1');
    t('the bone marrow answers the marrow question: no question is shown and nothing about it is on the trail',
      ctx.state.captured.primary_compartment === 'marrow' && ctx.state.group === 1 && !labelsOf().includes('Marrow blasts') &&
      !labelsOf().includes('Site of origin') && !labelsOf().includes('Organ'), ctx.state.stage + ' ' + labelsOf().join() + ' ' + ctx.state.captured.primary_compartment);
    await start('blood_marrow'); await toSite(null, null, 'C42.2');
    t('the spleen is the one blood site that is asked the marrow question', ctx.state.stage === 'discriminator' &&
      /How many blasts does the marrow aspirate show\?/.test(rend(() => ctx.renderDiscriminator())), ctx.state.stage);

    /* A leukaemia that presents in a lymph node is still Group I. */
    await start('lymphadenopathy');
    const sysScreen = rend(() => ctx.renderSiteSystem());
    t('the system screen lists every system once, with the lymph nodes among them', ctx.state.stage === 'site_system' &&
      (sysScreen.match(/data-act="site_system"/g) || []).length === router.site_systems.length && /Lymph nodes/.test(sysScreen), ctx.state.stage);
    await toSite('lymph_nodes', 'lymph_node', 'C77.0');
    t('a system holding one organ skips the organ screen, and the region of the node is asked', ctx.state.stage === 'discriminator' && labelsOf().join() === 'Presentation,Site of origin,Topography',
      ctx.state.stage + ' ' + labelsOf().join());
    const q = rend(() => ctx.renderDiscriminator());
    t('the marrow question reads as the registrar worded it, with its three answers', /How many blasts does the marrow aspirate show\?/.test(q) &&
      /More than 25% blasts/.test(q) && /25% or less/.test(q) && /No marrow aspirate yet/.test(q) && /points to leukaemia/.test(q), q.slice(0, 400));
    await answer('marrow');
    t('more than 25% blasts at a lymph node leaves Group I alone: Group II and the soft-tissue sarcomas of Group IX are dropped, and the case goes straight in',
      cands() === '[1]' && ctx.state.group === 1 && ctx.state.stage !== 'group', ctx.state.stage + ' group ' + ctx.state.group + ' ' + cands());
    t('the trail shows the answer in words, never the stored value', labelsOf().slice(0, 4).join() === 'Presentation,Site of origin,Topography,Marrow blasts' &&
      ctx.state.trail.every((x) => x.value !== 'marrow') && ctx.state.trail.slice(-1)[0].value === 'More than 25% blasts', JSON.stringify(ctx.state.trail.map((x) => x.label + ': ' + x.value)));
    /* Opening a step: its own window, locked, the earlier choice highlighted, and nothing deleted.
       Each answer is drawn before the next, as it is on the page, because the window kept for a step is
       the screen as last drawn. */
    {
      const tapR = async (act, i) => { await tap(act, i); ctx.render(); };
      ctx.reset(); Object.assign(ctx.state, { router, topography: topo, aliasIndex: {} }); ctx.render();
      await tapR('guided', 0); await tapR('archetype', router.archetypes.findIndex((a) => a.archetype_id === 'lymphadenopathy'));
      await tapR('site_system', ctx.siteSystems().findIndex((x) => x.system.system_id === 'lymph_nodes'));
      await tapR('site_region', ctx.regionOptions(ctx.state.organSystem).findIndex((o) => o.topography === 'C77.0'));
      await tapR('discriminator', ctx.discriminator().options.findIndex((o) => o.value === 'marrow'));
      const live = { stage: ctx.state.stage, trail: ctx.state.trail.length, group: ctx.state.group }, k = labelsOf().indexOf('Marrow blasts');
      await tap('review', k);
      const win = rend(() => ctx.renderStage());
      t('clicking a step opens that step\'s own window with the earlier choice highlighted, and nothing is deleted',
        ctx.state.trail.length === live.trail && ctx.state.stage === live.stage && ctx.state.group === live.group && /Reviewing · Marrow blasts/.test(win) &&
        (win.match(/opt--selected/g) || []).length === 1 && /opt--selected"[^>]*data-act="discriminator"[^>]*>\s*<span class="opt__label">More than 25% blasts/.test(win),
        'trail ' + ctx.state.trail.length + '/' + live.trail + ', highlighted ' + (win.match(/opt--selected/g) || []).length);
      t('the window is locked, and the only buttons that act are "Move back here" and "Back to where I was"',
        /<div class="review__window" inert>/.test(win) && />Move back here</.test(win) && />Back to where I was</.test(win), win.slice(0, 200));
      await tap('archetype', 0); await tap('discriminator', 1);
      t('while a step is open the case cannot be changed from its locked window', ctx.state.trail.length === live.trail &&
        ctx.state.archetype.archetype_id === 'lymphadenopathy' && ctx.state.captured.primary_compartment === 'marrow', 'the case changed under the review');
      const railOpen = rend(() => ctx.renderRail()), rowsOpen = rend(() => ctx.renderTrailRows());
      t('the current step stays on the list as a way back, and the reviewed row is marked', /rail__row--reviewing/.test(railOpen) && /trail-row--reviewing/.test(rowsOpen) &&
        /data-act="review-exit"/.test(railOpen) && /data-act="review-exit"/.test(rowsOpen), 'no way back on the list');
      await tap('review-exit');
      t('Back to where I was shows the live screen again with every step in place', ctx.state.review === null && !/Reviewing/.test(rend(() => ctx.renderStage())) &&
        ctx.state.trail.length === live.trail && ctx.state.stage === live.stage, ctx.state.stage + ' ' + ctx.state.trail.length);
      await tap('review', labelsOf().indexOf('Site of origin')); await tap('rewind', labelsOf().indexOf('Site of origin'));
      t('Move back here rewinds the case to that step and removes the steps after it', ctx.state.review === null && ctx.state.stage === 'site_system' &&
        labelsOf().join() === 'Presentation', ctx.state.stage + ' ' + labelsOf().join());
      /* The checks that follow expect the case the earlier ones left. */
      await start('lymphadenopathy'); await toSite('lymph_nodes', 'lymph_node', 'C77.0'); await answer('marrow');
    }
    await tap('rewind', labelsOf().indexOf('Site of origin'));
    t('stepping back to the site of origin shows the system screen with the earlier answers gone', ctx.state.stage === 'site_system' &&
      ctx.state.captured.primary_compartment === undefined && ctx.state.system === null && labelsOf().join() === 'Presentation' && cands() === JSON.stringify([1, 2, 9]), ctx.state.stage + ' ' + cands());
    await start('lymphadenopathy'); await toSite('lymph_nodes', 'lymph_node', 'C77.0'); await answer('not_marrow');
    t('25% or less sends a lymph node to the lymphomas and sarcomas: Group I is dropped, Groups II and IX stay (a node biopsy can show Kaposi sarcoma)', cands() === '[2,9]', cands());
    await start('lymphadenopathy'); await toSite('lymph_nodes', 'lymph_node', 'C77.0'); await answer('not_known');
    t('no marrow aspirate yet drops nothing: Groups I, II and IX all stay on offer', cands() === '[1,2,9]', cands());

    /* The question is asked only where it can change the family. */
    await start('unsure'); await toSite('urinary', 'kidney', 'C64.9');
    t('a kidney tumour is never asked the marrow question', ctx.state.stage !== 'discriminator' && ctx.state.captured.primary_compartment === undefined &&
      !labelsOf().includes('Marrow blasts'), ctx.state.stage + ' ' + labelsOf().join());
    await start('unsure'); await toSite('endocrine', 'thyroid', 'C73.9');
    t('a thyroid under "not sure" is asked, because Group I and Group II are both still possible', ctx.state.stage === 'discriminator', ctx.state.stage);
    await start('solid_mass'); await tap('discriminator', 0); await toSite('soft_tissue', 'soft_tissue_connective', 'C49.2');
    t('a presentation that cannot be a leukaemia is never asked it', !labelsOf().includes('Marrow blasts') && ctx.state.captured.primary_compartment === undefined, labelsOf().join());

    /* A system answers to the names of the organs and regions inside it. */
    const headRow = [...rend(() => (ctx.reset(), Object.assign(ctx.state, { router, topography: topo, archetype: router.archetypes[1] }), ctx.renderSiteSystem()))
      .matchAll(/data-find="([^"]*)"[^>]*data-act="site_system"/g)].map((m) => m[1]);
    t('typing parotid finds a system, because the parotid gland is inside it', headRow.some((f) => /parotid gland/.test(f)), headRow.length + ' rows');

    /* The group a code is output under, now that the question decides in one place. */
    const rg = (code, topo2, vars, group) => { ctx.reset(); Object.assign(ctx.state, { router, topography: topo, group, captured: Object.assign({ topography: topo2 }, vars) }); return ctx.resolveGroup(code, topo2); };
    const gm = rg('9811', 'C77.0', { primary_compartment: 'marrow' }, 1), gn = rg('9811', 'C77.0', { primary_compartment: 'not_marrow' }, 2);
    t('more than 25% blasts routes 9811 to Group I and 25% or less to Group II', gm.group === 1 && gn.group === 2, JSON.stringify([gm, gn]));
    const gb = rg('9811', 'C77.0', { primary_compartment: 'not_marrow', marrow_blast_percentage: 60 }, 2);
    t('a blast percentage typed later in the tree does not overrule the answer given at the question', gb.group === 2, JSON.stringify(gb));
    const g1 = rg('9811', 'C77.0', { primary_compartment: 'not_known' }, 1), g2 = rg('9811', 'C77.0', { primary_compartment: 'not_known' }, 2);
    t('no marrow aspirate yet keeps the group the clerk chose and says the group is provisional', g1.group === 1 && g2.group === 2 &&
      /provisional/.test(g1.note || '') && /no marrow aspirate/.test(g1.note || ''), JSON.stringify([g1, g2]));
    t('all three rules that read the question answer each of its three answers', ['9811', '9823', '9827'].every((code) =>
      ['marrow', 'not_marrow', 'not_known'].every((v) => rg(code, 'C77.0', { primary_compartment: v }, 1) !== null)), 'a rule has no branch for an answer');
  }

  {
    /* A marrow report with a genetic test and no flow cytometry or IHC (registrar, 13 October 2026, found by running
       an aspirate with PCR through the page). The gate used to send it down the morphology-only route, which never
       asks the genetic result, so a BCR::ABL1-positive case could not be coded. The route now asks it, and a finding
       the file cannot place stays an annotation at the lineage the smear supports. */
    const dt1 = dts.get(1), TREE = 'tree_acute_leukemia';
    const ALL = ['referral', 'marrow_aspirate', 'trephine', 'flow', 'ihc', 'karyotype', 'fish', 'pcr', 'sequencing'];
    const gate = async (ids) => {
      begin(dt1, TREE, 'ac_document_inventory', 'C42.1');
      await tickSet(ALL, new Set(ids)); await tap('tick-continue');
      return ctx.state.nodeId;
    };
    const pickBy = async (nodeId, head) => {
      const n = ctx.findNode(nodeId), i = n.options.findIndex((o) => (o.label || '').startsWith(head));
      if (i < 0) { thrown = 'no option "' + head + '" at ' + nodeId; return; }
      await tap('opt', i);
    };
    const codeNow = () => { const e = ctx.state.result && ctx.state.result.entry; return e ? e.morphology_code : 'none (stage ' + ctx.state.stage + ', node ' + ctx.state.nodeId + ')'; };
    const where = [['marrow_aspirate', 'pcr'], ['trephine', 'sequencing'], ['marrow_aspirate', 'trephine', 'fish'], ['marrow_aspirate', 'karyotype']];
    const routed = []; for (const ids of where) routed.push(await gate(ids));
    t('a marrow report with a genetic test and no flow or IHC goes to the genetics question, whichever marrow test and genetic test it is',
      routed.every((x) => x === 'ac_morph_genetics_context'), JSON.stringify(routed));
    t('a marrow report alone still goes to the morphology question, and with flow it still goes to prior therapy',
      (await gate(['marrow_aspirate'])) === 'ac_morphology_only' && (await gate(['marrow_aspirate', 'pcr', 'flow'])) === 'ac_prior_therapy_gate', 'the other routes moved');
    await gate(['marrow_aspirate', 'pcr']); await pickBy('ac_morph_genetics_context', 'BCR::ABL1 positive');
    const afterGen = ctx.state.nodeId;
    await pickBy('ac_morphology_only', 'Lymphoid blasts');
    const up = JSON.stringify(ctx.state.result && ctx.state.result.upgrade || '');
    t('lymphoid blasts with BCR::ABL1 positive and no flow or IHC stay at 9835 with the finding recorded, and the upgrade names what 9812, 9806 and 9875 need',
      afterGen === 'ac_morphology_only' && codeNow() === '9835' && /BCR::ABL1 positive/.test(ctx.state.captured.genotype_annotation || '') &&
      /9812/.test(up) && /9806/.test(up) && /9875/.test(up), 'after genetics ' + afterGen + ', code ' + codeNow() + ', annotation ' + ctx.state.captured.genotype_annotation + ', upgrade ' + up.slice(0, 160));
    t('a lineage-level code reached without flow cytometry lists flow cytometry as outstanding, and does not read "complete"',
      (ctx.state.workup || []).some((w) => w.test === 'Flow cytometry') && !/Complete — no outstanding tests/.test(rend(() => ctx.renderWorkup())), JSON.stringify(ctx.state.workup));
    await gate(['marrow_aspirate', 'pcr']); await pickBy('ac_morph_genetics_context', 'BCR::ABL1 positive'); await pickBy('ac_morphology_only', 'Myeloid blasts');
    const upM = JSON.stringify(ctx.state.result && ctx.state.result.upgrade || '');
    t('myeloid blasts with BCR::ABL1 positive and no flow or IHC stay at 9861, and the upgrade names 9912 and 9875', codeNow() === '9861' && /9912/.test(upM) && /9875/.test(upM), codeNow() + ' ' + upM.slice(0, 160));
    /* APL: the PML::RARA question settles the code itself. The free-text box that followed it decided nothing and is gone. */
    const apl = async (head) => { begin(dt1, TREE, 'ac_apl_status', 'C42.1'); await pickBy('ac_apl_status', head); return codeNow(); };
    const aPos = await apl('PML::RARA POSITIVE'), aNpm = await apl('PML::RARA NEGATIVE — NPM1 mutation found'), aNone = await apl('PML::RARA not tested');
    t('the PML::RARA question settles the code itself and no free-text box follows it: positive 9866, NPM1 mutated 9877, not tested 9861',
      aPos === '9866' && aNpm === '9877' && aNone === '9861' && !ctx.findNode('ac_apl_confirm'), [aPos, aNpm, aNone, !!ctx.findNode('ac_apl_confirm')].join(' '));
    await apl('PML::RARA NEGATIVE — NPM1 wild-type');
    t('PML::RARA negative with NPM1 wild-type returns to the AML genetics ladder', ctx.state.nodeId === 'ac_aml_genetics_upgrade', ctx.state.nodeId);
    /* PML::RARA not tested, reached from the lineage rules, must not close at AML NOS: a BCR::ABL1 result given earlier would be
       thrown away (registrar, 13 October 2026). It goes on to the AML genetics ladder. The closing question stays for the two routes
       with no earlier genetics to honour: the morphology-only route and the ladder's own "APL-like phenotype" option, which would
       otherwise loop. */
    begin(dt1, TREE, 'ac_apl_status_lineage', 'C42.1'); await pickBy('ac_apl_status_lineage', 'PML::RARA not tested');
    const fromLineage = ctx.state.nodeId;
    const closing = await apl('PML::RARA not tested');
    begin(dt1, TREE, 'ac_lineage_assignment', 'C42.1');
    for (const m of ['cMPO', 'CD33']) { const i = ctx.pickerAvailable(ctx.node()).indexOf(m); await tap('pickadd', i); await mset(m, 'pos'); }
    await tap('resolve');
    const ladderApl = (ctx.findNode('ac_aml_genetics_upgrade').options || []).filter((o) => o.next_node === 'ac_apl_status').length;
    t('PML::RARA not tested after the lineage rules goes on to the AML genetics ladder; the ladder\'s APL-like option still closes at 9861 and cannot loop',
      fromLineage === 'ac_aml_genetics_upgrade' && closing === '9861' && ctx.state.nodeId === 'ac_apl_status_lineage' && ladderApl === 1,
      'from lineage ' + fromLineage + ', closing ' + closing + ', after markers ' + ctx.state.nodeId + ', ladder options to the closing question ' + ladderApl);
  }
  return rows;
}

/* ------------------------------------------------- Group 5 question flow (14 October 2026)
   The registrar's question-flow review shortened the wording of Group 5's screens and left every route as it was; the registrar's rulings
   of the same day then changed some routes on purpose. This section keeps both true. `build/flow_golden_g05.json` holds the routes that
   stand for every answer a clerk can give on Group 5's six screens (41 recorded on `main` before the review, rewritten for the rulings);
   each is replayed through the handlers the buttons call and must end on the same code, behaviour, referral, outstanding tests, basis of
   diagnosis and evidence credited. The labels the page draws must stay at 90 characters or fewer, and no screen may carry the wording the
   review removed: shouted capitals, a double hyphen, an internal feature number, or an intensifier. The first screen's hint and row were
   pinned by docs/evidence_documents/group_05.json until the registrar released them (RQ5, 14 October 2026); the mapping now holds the new
   wording and the data gate still compares the file with it. */
async function g05Flow(ctx) {
  const SHARED = path.join(ROOT, 'data', 'shared');
  const router = JSON.parse(fs.readFileSync(path.join(SHARED, 'presentation_router.json'), 'utf8'));
  const topo = JSON.parse(fs.readFileSync(path.join(SHARED, 'topography_codes.json'), 'utf8'));
  const dt = JSON.parse(fs.readFileSync(path.join(DB, 'group_05_dt.json'), 'utf8'));
  const golden = JSON.parse(fs.readFileSync(path.join(HERE, 'flow_golden_g05.json'), 'utf8'));
  ctx.groupCache.set(5, { dt, aliases: [] });
  const rows = [];
  const t = (name, ok, detail) => rows.push({ name, ok: !!ok, detail: ok ? '' : detail });
  const el = (attrs, extra) => Object.assign({ getAttribute: (k) => (attrs && k in attrs ? String(attrs[k]) : null), value: '', checked: false, type: 'button' }, extra || {});
  const tap = (act, attrs, extra) => ctx.handleOption(act, el(attrs, extra));
  const begin = () => {
    ctx.reset();
    Object.assign(ctx.state, { router, topography: topo, dt, treeId: 'g5_retinoblastoma', nodeId: golden.entry.node, stage: 'node', aliasIndex: {} });
    ctx.state.captured = { topography: golden.entry.topography };
    ctx.state.trailAtGroupEntry = 0;
  };
  const play = async (steps) => {
    for (const k of steps) {
      if (k.m === 'opt') await tap('opt', { 'data-i': k.i });
      else if (k.m === 'tickopt') await tap('tickopt', { 'data-i': k.j });
      else if (k.m === 'tickset') {
        for (const id of k.set) await tap('tick', { 'data-id': id }, { type: 'checkbox', checked: true });
        if (k.ctxRow) await tap('draft', { 'data-k': 'ctx' }, { type: 'radio', value: String(k.ctxRow) });
        await tap('tick-continue', {});
      } else if (k.m === 'imaging') {
        for (const i of k.F) await tap('feature', { 'data-i': i }, { type: 'checkbox', checked: true });
        for (const i of k.D) await tap('diversion', { 'data-i': i }, { type: 'checkbox', checked: true });
        await tap('resolve', {});
      } else throw new Error('unknown macro ' + k.m);
    }
  };
  const endOf = () => {
    const st = ctx.state, r = st.result;
    if (st.stage !== 'output') return { kind: 'open at ' + st.stage + ' ' + st.nodeId };
    const e = { workup: (st.workup || []).map((w) => w.test), basis: r.basisOfDiagnosis === undefined ? null : r.basisOfDiagnosis };
    if (r.referral) return Object.assign(e, { kind: 'referral', group: r.group });
    if (r.excluded) return Object.assign(e, { kind: 'non_reportable' });
    if (r.behaviourExcluded) return Object.assign(e, { kind: 'behaviour_exclusion', code: r.icdoCode, behavior: r.icdoBehaviour });
    return Object.assign(e, { kind: 'code', code: r.code, behavior: r.entry.behavior_code, evidence_tests: st.captured.evidence_tests || [] });
  };
  const wrong = [];
  for (const r of golden.routes) {
    begin();
    let thrown = '';
    try { await play(r.steps); } catch (e) { thrown = e.message; }
    const got = endOf();
    const bad = Object.keys(r.expect).filter((k) => JSON.stringify(got[k]) !== JSON.stringify(r.expect[k]));
    if (bad.length || thrown) wrong.push(r.name + ' -> ' + bad.map((k) => k + ' ' + JSON.stringify(got[k]) + ' (wanted ' + JSON.stringify(r.expect[k]) + ')').join('; ') + (thrown ? ' [threw: ' + thrown + ']' : ''));
  }
  t('Group 5: every one of the ' + golden.routes.length + ' recorded routes still ends on the same code, behaviour, referral, outstanding tests, basis of diagnosis and evidence credited',
    golden.routes.length >= 50 && wrong.length === 0, wrong.length + ' differ: ' + wrong.slice(0, 3).join(' | '));

  /* The labels the page draws, read from the page's own markup. */
  const tree = dt.decision_trees[0], drawn = [];
  const grab = (html, re) => [...html.matchAll(re)].map((m) => m[1].replace(/<[^>]+>/g, '').replace(/&#39;/g, "'").replace(/&amp;/g, '&').replace(/&quot;/g, '"').trim());
  for (const n of tree.nodes) {
    ctx.reset();
    Object.assign(ctx.state, { router, topography: topo, dt, treeId: tree.tree_id, nodeId: n.node_id, stage: 'node', aliasIndex: {} });
    ctx.state.captured = { topography: golden.entry.topography };
    const html = ctx.renderLiveNode();
    const add = (kind, list) => list.forEach((text) => drawn.push({ node: n.node_id, kind, text }));
    add('answer', grab(html, /<span class="opt__label">([\s\S]*?)(?:<span class="opt__meta"|<\/span><\/button>)/g));
    add('answer row', grab(html, /<input type="radio"[^>]*> <span>([\s\S]*?)(?:<span class="opt__meta"|<\/span><\/label>)/g));
    add('feature', grab(html, /data-act="feature"[^>]*> ([\s\S]*?)<\/label>/g));
    add('diversion', grab(html, /data-act="diversion"[^>]*> ([\s\S]*?)(?:<span class="opt__meta"|<\/label>)/g));
    add('tick box', grab(html, /<span class="check__text">([\s\S]*?)<\/span>/g));
  }
  const long = drawn.filter((d) => d.text.length > 90);
  t('Group 5: every answer, row, box, feature and diversion the page draws is 90 characters or fewer',
    drawn.length >= 28 && long.length === 0, drawn.length + ' drawn; over 90: ' + long.slice(0, 3).map((d) => d.node + ' "' + d.text.slice(0, 60) + '" (' + d.text.length + ')').join('; '));

  const TEXT = [];
  for (const n of tree.nodes) {
    TEXT.push([n.node_id, 'question', n.question]);
    TEXT.push([n.node_id, 'hint', n.hint]);
    (n.options || []).forEach((o, i) => TEXT.push([n.node_id, 'option ' + i, o.label]));
    ((n.tick_list || {}).items || []).forEach((it) => { TEXT.push([n.node_id, 'box ' + it.id, it.label]); if (it.about) TEXT.push([n.node_id, 'about ' + it.id, it.about]); });
    (n.imaging_features || []).forEach((f, i) => TEXT.push([n.node_id, 'feature ' + i, f]));
    (n.diversion_criteria || []).forEach((d, i) => TEXT.push([n.node_id, 'diversion ' + i, d.feature]));
  }
  const BAD = /\bactually\b|\b[A-Z]{5,}\b|--|\b(feature|option|node|step) ?\d\b|\b(very|highly|extremely|truly|really|simply)\b/;
  const hits = TEXT.filter(([, , x]) => x && BAD.test(x));
  t('Group 5: no question, hint, answer, box, feature or diversion carries "actually", shouted capitals, a double hyphen, an internal number or an intensifier',
    TEXT.length >= 40 && hits.length === 0, hits.length + ' hit: ' + hits.slice(0, 3).map(([n, w, x]) => n + ' ' + w + ' "' + x.slice(0, 50) + '"').join('; '));

  /* The registrar's rulings of 14 October 2026, driven through the handlers the buttons call. The expected results below are the rulings'
     own precedence written a second time, not read from the data. */
  const at = (nodeId) => { begin(); ctx.state.nodeId = nodeId; };
  const tickIds = async (ids) => { for (const id of ids) await tap('tick', { 'data-id': id }, { type: 'checkbox', checked: true }); };
  const subsets = (all) => { const out = []; for (let m = 0; m < (1 << all.length); m++) out.push(all.filter((_, b) => m >> b & 1)); return out; };
  const nodeById = (id) => tree.nodes.find((n) => n.node_id === id);
  const sameList = (a, b) => JSON.stringify(a) === JSON.stringify(b);

  begin();
  const firstBoxes = ctx.tickList(ctx.node()).items.map((x) => x.id);
  const sharedIds = router.tick_vocabularies.evidence_documents.items.map((x) => x.id);
  t('Group 5 first screen: four boxes (imaging, cytology, liquid biopsy, histology); the shared list of seven is unchanged, so no other group\'s first screen moves (RQ7, RP4)',
    sameList(firstBoxes, ['imaging', 'cytology', 'liquid_biopsy', 'histology']) && sharedIds.length === 7 && !sharedIds.includes('liquid_biopsy'), firstBoxes.join(',') + ' / shared ' + sharedIds.join(','));

  const wentTo = [];
  for (const set of subsets(firstBoxes)) { begin(); await tickIds(set); await tap('tick-continue', {}); wentTo.push(set.join('+') + ' -> ' + ctx.state.nodeId + (ctx.state.captured.tick_gate ? ' (asks which tier)' : '')); }
  const want = (set) => set.includes('histology') ? 'rb_enucleation_report' : (set.includes('cytology') || set.includes('liquid_biopsy')) ? 'rb_cytology' : set.includes('imaging') ? 'rb_imaging_pathway' : 'rb_clinical_alias';
  const bad1 = wentTo.filter((x, i) => !x.endsWith('-> ' + want(subsets(firstBoxes)[i])));
  t('Group 5 first screen: each of the 16 ticked sets goes straight to histology, cytology (or liquid biopsy), imaging or the referral wording in that order, and the clerk is never asked to choose between tiers',
    bad1.length === 0, bad1.length + ' differ: ' + bad1.slice(0, 3).join('; '));

  begin();
  const inadequate = ctx.tickContexts(ctx.node()).length === 1;
  const openRow = async (ids, row) => { begin(); await tickIds(ids); if (row) await tap('draft', { 'data-k': 'ctx' }, { type: 'radio', value: String(row) }); return ctx.renderLiveNode(); };
  const warnHist = await openRow(['histology'], 1), warnCyto = await openRow(['cytology'], 1), warnNone = await openRow(['histology'], 0), warnNoTick = await openRow([], 1);
  t('Group 5 first screen: the inadequate-specimen row beside a ticked histology report shows a notice, and the notice does not show for a cytology report, for no row, or for a row with nothing ticked (RP6)',
    inadequate && /banner--warn/.test(warnHist) && /no histological diagnosis/.test(warnHist) && !/banner--warn/.test(warnCyto) && !/banner--warn/.test(warnNone) && !/banner--warn/.test(warnNoTick),
    [inadequate, /banner--warn/.test(warnHist), /banner--warn/.test(warnCyto), /banner--warn/.test(warnNone), /banner--warn/.test(warnNoTick)].join(' '));
  begin(); await tickIds(['histology']); await tap('draft', { 'data-k': 'ctx' }, { type: 'radio', value: '1' }); await tap('tick-continue', {});
  const keptTicks = JSON.stringify(ctx.state.captured.documents_in_file);
  await tap('feature', { 'data-i': 0 }, { type: 'checkbox', checked: true }); await tap('feature', { 'data-i': 1 }, { type: 'checkbox', checked: true }); await tap('feature', { 'data-i': 2 }, { type: 'checkbox', checked: true });
  await tap('resolve', {});
  const outHtml = ctx.state.stage === 'output' ? ctx.renderOutput() : '';
  t('Group 5 first screen: with a histology report ticked, the inadequate-specimen row still wins, the case goes to the imaging screen without reading the report, and the result does not list the report as the evidence it rests on (RP6)',
    keptTicks === '[]' && /9510/.test(outHtml) && !/Histology report/.test(outHtml) && /Constellation confirmed/.test(outHtml),
    'ticks kept ' + keptTicks + ', stage ' + ctx.state.stage + ', "Histology report" in the result: ' + /Histology report/.test(outHtml));

  const ins = nodeById('rb_imaging_insufficient');
  t('Group 5: the two "tissue has since been obtained" answers are gone and the retinocytoma screen is merged into the enucleation screen: six nodes, no way back to the cytology or enucleation screens from the imaging screens (RQ1, RQ2)',
    tree.nodes.length === 6 && !nodeById('rb_retinocytoma_word') && ins.options.length === 4 && !ins.options.some((o) => ['rb_cytology', 'rb_enucleation_report'].includes(o.next_node)),
    tree.nodes.length + ' nodes, ' + ins.options.length + ' answers on the fourth screen');

  const enu = [];
  for (const set of subsets(nodeById('rb_enucleation_report').tick_list.items.map((x) => x.id))) {
    at('rb_enucleation_report'); await tickIds(set); await tap('tick-continue', {});
    const got = endOf();
    const w = set.includes('diffuse') ? { kind: 'code', code: '9513' } : set.includes('g34') ? { kind: 'code', code: '9512' } : (set.includes('g12') || set.includes('area')) ? { kind: 'code', code: '9511' }
      : set.includes('whole') ? { kind: 'behaviour_exclusion', code: '9510', behavior: '0' } : set.includes('phthisis') ? { kind: 'behaviour_exclusion', code: '9514', behavior: '1' } : { kind: 'code', code: '9510' };
    const off = Object.keys(w).filter((k) => got[k] !== w[k]);
    if (off.length) enu.push('{' + set.join(',') + '} gave ' + JSON.stringify(got) + ' wanted ' + JSON.stringify(w));
  }
  t('Group 5 enucleation screen: every one of the 64 ticked sets ends where the order says (diffuse 9513, poorly differentiated or undifferentiated 9512, differentiated or a retinocytoma-grade area 9511, whole-specimen retinocytoma 9510/0, phthisis bulbi 9514/1, nothing 9510) (RQ2, RQ6)',
    enu.length === 0, enu.length + ' differ: ' + enu.slice(0, 2).join(' | '));

  const ali = [];
  for (const set of subsets(nodeById('rb_clinical_alias').tick_list.items.map((x) => x.id))) {
    at('rb_clinical_alias'); await tickIds(set); await tap('tick-continue', {});
    const got = endOf();
    const registrable = !set.includes('other_cause') && ['named', 'leukocoria', 'strabismus'].some((x) => set.includes(x));
    const ok = registrable ? (got.kind === 'code' && got.code === '9510' && got.basis === 1) : got.kind === 'non_reportable';
    if (!ok) ali.push('{' + set.join(',') + '} gave ' + JSON.stringify(got));
  }
  t('Group 5 referral wording: of the 16 ticked sets only a named retinoblastoma, leukocoria or strabismus with no non-malignant cause named records 9510/3 at basis 1; the rest are not reportable (RQ3)',
    ali.length === 0, ali.length + ' differ: ' + ali.slice(0, 2).join(' | '));

  const dia = (n) => n.diversion_criteria.map((x) => x.feature);
  const img = nodeById('rb_imaging_pathway');
  const boxLabel = (id) => ins.tick_list.items.find((x) => x.id === id).label;
  t('Group 5 imaging screen: pseudohypopyon and an anterior-segment mass are separate boxes, and the fourth screen offers a needs-tissue box that names pseudohypopyon and a mimic box that does not (RP2)',
    dia(img).includes('Pseudohypopyon') && dia(img).includes('An anterior-segment mass') && /pseudohypopyon/.test(boxLabel('tissue')) && !/pseudohypopyon/i.test(boxLabel('mimic')) &&
      ins.options[0].refer_group === 12 && ins.options[1].non_reportable === true,
    dia(img).join(' | ') + ' / ' + ins.tick_list.items.map((x) => x.label.slice(0, 40)).join(' | '));
  const fourth = [];
  for (const set of subsets(ins.tick_list.items.map((x) => x.id))) {
    at('rb_imaging_insufficient'); await tickIds(set); await tap('tick-continue', {});
    const got = endOf();
    const ok = (set.includes('tissue') || (!set.includes('mimic') && !set.includes('note'))) ? (got.kind === 'referral' && got.group === 12)
      : set.includes('mimic') ? got.kind === 'non_reportable' : (ctx.state.stage === 'node' && ctx.state.nodeId === 'rb_clinical_alias');
    if (!ok) fourth.push('{' + set.join(',') + '} gave ' + JSON.stringify(got) + ' at ' + ctx.state.nodeId);
  }
  t('Group 5 fourth screen: of the 8 ticked sets, any needs-tissue box refers Group XII even beside a mimic box or a note; a mimic box alone ends the case; a note alone reads the referral wording; nothing ticked refers Group XII (RQ4, RP1, RP3)',
    fourth.length === 0, fourth.length + ' differ: ' + fourth.slice(0, 2).join(' | '));
  const aliases = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'aliases', 'aliases_group_05.json'), 'utf8'));
  const trilateral = aliases.find((a) => a.alias === 'Trilateral retinoblastoma');
  const referring = aliases.filter((a) => 'refer_group' in a || 'refer_code' in a || 'reason' in a);
  t('Group 5 aliases: trilateral retinoblastoma maps to 9510 in Group V and no alias entry refers to another group or tells the clerk to open a Group III record (RP5: a pineal or suprasellar mass is metastatic spread)',
    !!trilateral && referring.length === 0 && JSON.stringify(trilateral.maps_to_morphology_codes) === '["9510"]' && !/Group III/.test(trilateral.full_form || ''),
    referring.map((a) => a.alias).join(', ') + ' / ' + (trilateral ? trilateral.full_form : 'no trilateral entry'));
  return rows;
}

/* ------------------------------------------------- Group 5 Pathway case table (14 October 2026, reachability review)
   `build/pathway_cases_g05.json` holds clerk walks whose result the Pathway, the registrar's rulings or the build contract fix: one ideal case
   for every emitter, the Pathway's own quick-reference rows and edge cases, and each defining result of the primary paths removed one at a time.
   Every walk is replayed through the handlers the buttons call and must end where its source says. A row marked `assert: false` is a case
   a registrar ruling is still owed on: it is replayed and must still give the `current` result, so a change is made on purpose. */
async function g05Pathway(ctx) {
  const SHARED = path.join(ROOT, 'data', 'shared');
  const router = JSON.parse(fs.readFileSync(path.join(SHARED, 'presentation_router.json'), 'utf8'));
  const topo = JSON.parse(fs.readFileSync(path.join(SHARED, 'topography_codes.json'), 'utf8'));
  const dt = JSON.parse(fs.readFileSync(path.join(DB, 'group_05_dt.json'), 'utf8'));
  const table = JSON.parse(fs.readFileSync(path.join(HERE, 'pathway_cases_g05.json'), 'utf8'));
  ctx.groupCache.set(5, { dt, aliases: [] });
  const rows = [];
  const t = (name, ok, detail) => rows.push({ name, ok: !!ok, detail: ok ? '' : detail });
  const el = (attrs, extra) => Object.assign({ getAttribute: (k) => (attrs && k in attrs ? String(attrs[k]) : null), value: '', checked: false, type: 'button' }, extra || {});
  const tap = (act, attrs, extra) => ctx.handleOption(act, el(attrs, extra));
  const play = async (steps) => {
    ctx.reset();
    Object.assign(ctx.state, { router, topography: topo, dt, treeId: 'g5_retinoblastoma', nodeId: table.entry.node, stage: 'node', aliasIndex: {} });
    ctx.state.captured = { topography: table.entry.topography }; ctx.state.trailAtGroupEntry = 0;
    for (const k of steps) {
      if (k.m === 'opt') await tap('opt', { 'data-i': k.i });
      else if (k.m === 'tickopt') await tap('tickopt', { 'data-i': k.j });
      else if (k.m === 'tickset') {
        for (const id of k.set) await tap('tick', { 'data-id': id }, { type: 'checkbox', checked: true });
        if (k.ctxRow) await tap('draft', { 'data-k': 'ctx' }, { type: 'radio', value: String(k.ctxRow) });
        await tap('tick-continue', {});
      } else if (k.m === 'imaging') {
        for (const i of k.F) await tap('feature', { 'data-i': i }, { type: 'checkbox', checked: true });
        for (const i of k.D) await tap('diversion', { 'data-i': i }, { type: 'checkbox', checked: true });
        await tap('resolve', {});
      } else throw new Error('unknown macro ' + k.m);
    }
  };
  const endOf = () => {
    const st = ctx.state, r = st.result;
    if (st.stage !== 'output') return { kind: 'open at ' + st.stage + ' ' + st.nodeId };
    const e = { workup: (st.workup || []).map((w) => w.test), basis: r.basisOfDiagnosis === undefined ? null : r.basisOfDiagnosis };
    if (r.referral) return Object.assign(e, { kind: 'referral', group: r.group });
    if (r.excluded) return Object.assign(e, { kind: 'non_reportable' });
    if (r.behaviourExcluded) return Object.assign(e, { kind: 'behaviour_exclusion', code: r.icdoCode, behavior: r.icdoBehaviour });
    return Object.assign(e, { kind: 'code', code: r.code, behavior: r.entry.behavior_code });
  };
  const differs = (got, want) => Object.keys(want).filter((k) => JSON.stringify(got[k]) !== JSON.stringify(want[k]));
  const asserted = table.cases.filter((c) => c.assert), pending = table.cases.filter((c) => !c.assert);
  const wrong = [];
  for (const c of asserted) {
    let thrown = '';
    try { await play(c.steps); } catch (e) { thrown = e.message; }
    const got = endOf(), bad = differs(got, c.expect);
    if (bad.length || thrown) wrong.push(c.id + ' ' + c.name.slice(0, 50) + ' -> ' + bad.map((k) => k + ' ' + JSON.stringify(got[k]) + ' (wanted ' + JSON.stringify(c.expect[k]) + ')').join('; ') + (thrown ? ' [threw: ' + thrown + ']' : ''));
  }
  t('Group 5 Pathway cases: all ' + asserted.length + ' walks the Pathway, the rulings or the build contract settle replay to the code, behaviour, referral, basis and outstanding tests they give',
    asserted.length >= 38 && wrong.length === 0, wrong.length + ' differ: ' + wrong.slice(0, 3).join(' | '));
  const noSource = asserted.filter((c) => !c.source || String(c.source).trim().length < 8);
  t('Group 5 Pathway cases: every asserted walk names the Pathway section, ruling or contract section that gives its result', noSource.length === 0, noSource.map((c) => c.id).join(', '));
  const kinds = new Set(asserted.map((c) => c.kind));
  const codes = new Set(asserted.filter((c) => c.expect.kind === 'code').map((c) => c.expect.code));
  t('Group 5 Pathway cases: the table holds an ideal case for each of 9510, 9511, 9512 and 9513, the two behaviour-exclusion terminals, a referral and a not-reportable terminal',
    ['9510', '9511', '9512', '9513'].every((c) => codes.has(c)) && kinds.has('ideal') &&
      asserted.some((c) => c.expect.kind === 'behaviour_exclusion' && c.expect.code === '9510') && asserted.some((c) => c.expect.kind === 'behaviour_exclusion' && c.expect.code === '9514') &&
      asserted.some((c) => c.expect.kind === 'referral') && asserted.some((c) => c.expect.kind === 'non_reportable'), 'codes ' + [...codes].join(','));
  const moved = [];
  for (const c of pending) {
    let thrown = '';
    try { await play(c.steps); } catch (e) { thrown = e.message; }
    const got = endOf(), bad = differs(got, c.current);
    if (bad.length || thrown) moved.push(c.id + ' -> ' + bad.map((k) => k + ' ' + JSON.stringify(got[k]) + ' (was ' + JSON.stringify(c.current[k]) + ')').join('; '));
  }
  t('Group 5 Pathway cases: the ' + pending.length + ' walks a registrar ruling is still owed on give the result they gave when the table was written (' + pending.map((c) => c.id).join(', ') + ')', moved.length === 0, moved.join(' | '));
  return rows;
}

/* ---------------------------------------------------------------------- main */
const ctx = loadEngine();
let bad = 0, partial = 0;

/* ONLY=g05p runs the Group 5 Pathway case table alone */
if (ONLY === 'g05p') {
  let rows = [];
  try { rows = await g05Pathway(ctx); } catch (e) { rows = [{ name: 'the Group 5 Pathway section ran to the end', ok: false, detail: 'the engine threw: ' + e.stack }]; }
  for (const r of rows) { console.log('  %s  %s', r.ok ? 'OK  ' : 'FAIL', r.name); if (!r.ok) { console.log('        ' + r.detail); bad++; } }
  process.exit(bad ? 1 : 0);
}

/* ONLY=g05 runs the Group 5 question-flow section alone */
if (ONLY === 'g05') {
  let rows = [];
  try { rows = await g05Flow(ctx); } catch (e) { rows = [{ name: 'the Group 5 section ran to the end', ok: false, detail: 'the engine threw: ' + e.stack }]; }
  for (const r of rows) { console.log('  %s  %s', r.ok ? 'OK  ' : 'FAIL', r.name); if (!r.ok) { console.log('        ' + r.detail); bad++; } }
  process.exit(bad ? 1 : 0);
}

console.log('Fixtures — the defect, and the controls that keep a fix honest\n');
for (const r of (ONLY === 'ux' ? [] : fixtures(ctx))) {
  console.log('  %s  %s', r.ok ? 'OK  ' : 'FAIL', r.name);
  if (!r.ok) { console.log('        ' + r.detail); bad++; }
}

console.log('\nExpress lane — a term filed under several groups is settled by the site\n');
{
  /* An engine that throws inside a scenario fails the section by name rather
     than ending the run with a stack trace. */
  const r = { routed: 0, mismatch: 0, tie: 0, single: 0, siteSingles: 0, terms: 0, skipped: 0, rewinds: 0, keepWalks: 0, anySite: 0, routedSites: 0, fails: [] };
  if (ONLY !== 'ux') try { await expressLane(ctx, r); } catch (e) { r.fails.push('the engine threw: ' + e.message); }
  console.log('  %s  %d multi-group term(s) and %d single-group term(s) whose group reads the site, x every site: %d routed to one group, %d stopped (no group), %d stopped (tie); %d single-group term(s) of a group that reads no site are asked the site and only record it (%d sites tried, each entering the group); %d stepped-back case(s); %d guided walk(s) that must keep a group on site; %d (term, site) pair(s) routed to a group that occurs at any site or at its routed sites (%d of them at routed sites); %d term(s) not reachable from the results',
    r.fails.length ? 'FAIL' : 'OK  ', r.terms, r.siteSingles, r.routed, r.mismatch, r.tie, r.single, r.recorded || 0, r.rewinds, r.keepWalks, r.anySite, r.routedSites, r.skipped);
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

console.log('\nGroup 5 question flow — the routes it keeps and the wording its screens carry\n');
{
  let g5 = [];
  try { g5 = await g05Flow(ctx); } catch (e) { g5 = [{ name: 'the Group 5 section ran to the end', ok: false, detail: 'the engine threw: ' + e.stack }]; }
  for (const r of g5) {
    console.log('  %s  %s', r.ok ? 'OK  ' : 'FAIL', r.name);
    if (!r.ok) { console.log('        ' + r.detail); bad++; }
  }
}

console.log('\nGroup 5 Pathway cases — the codes the Pathway, the rulings and the build contract give\n');
{
  let g5p = [];
  try { g5p = await g05Pathway(ctx); } catch (e) { g5p = [{ name: 'the Group 5 Pathway section ran to the end', ok: false, detail: 'the engine threw: ' + e.stack }]; }
  for (const r of g5p) {
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
