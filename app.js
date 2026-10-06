/* ============================================================================
   app.js — the ICCC-3 Lookup engine. ONE file, identical logic for all
   12 groups.

   THE RULE (Architecture §11.2, engine.md §5):
     There is no clinical content in this file. No morphology codes, no marker
     names, no entity names, no `if (group === X)`. The engine knows node
     TYPES, not groups. Anything that varies by group lives in the JSON.
     A new *kind* of question is one new case in dispatchNode() — never a
     group-specific branch.

   No framework, no build step, no dependency (engine.md §1). The deciding
   argument was maintenance: this tool must outlive whoever writes it, and a
   successor who needs `npm install` to change a colour is a real risk.

   Model: one `state` object + one render() that rebuilds the panel from
   innerHTML on every change. At this panel size a full re-render is
   imperceptible, and it buys UI-as-a-function-of-state for ~20 lines.
   ========================================================================= */
'use strict';

/* The closed, shared vocabulary. An unrecognised node_type throws — the
   runtime half of "node types are a closed vocabulary" (nodes.md §1).
   `numeric_gate` is the ratified continuous-threshold type. `lab_results` is the
   laboratory panel (registrar, 6 October 2026): it records numbers and never
   chooses a code. */
var NODE_TYPES = [
  'clinical_presentation', 'site_capture', 'document_inventory', 'clinical_alias',
  'morphology_only', 'imaging_pathway', 'ihc_checklist', 'cytogenetics_dropdown',
  'molecular_freetext', 'histology_subclassification', 'site_resolution', 'numeric_gate', 'lab_results'
];

/* Captured per MISSING TEST, not per case: "not done" and "unavailable" are
   different registry facts (redcap.md §4). */
var WORKUP_STATES = ['pending', 'not done', 'unavailable', 'declined'];

/* A behaviour criterion is a yes/no clinical question. These are the generic
   words for the two answers — UI chrome, not clinical content — and a leaf may
   override either with its own `label`. */
var ANSWER_LABELS = { y: 'Yes', n: 'No', yes: 'Yes', no: 'No', unknown: 'Not known' };

var MARKER_CYCLE = [undefined, 'pos', 'strong', 'weak', 'neg'];
/* `nd` — recorded, but the stain was not done or could not be read. Ruling 11:
   an uninterpretable test drops the case to the nearest code rather than
   dead-ending, so `nd` behaves exactly as an absent marker does when rules are
   matched, and differs only in that the clerk said so and it reaches the
   workup list. Anything that asks "is this marker positive" must therefore
   treat `nd` the way it treats `neg`. */
var MARKER_UNREAD = 'nd';
/* Screen-reader wording for each marker state. The visible chip shows a short
   token; a marker read aloud needs the whole word. */
var MARKER_LABELS = { pos: 'positive', strong: 'strongly positive', weak: 'weakly positive',
  neg: 'negative', nd: 'not done or not readable' };

/* ---------------------------------------------------------------------------
   Closed schema vocabularies, and the wording each token is shown in.

   These sit beside NODE_TYPES, WORKUP_STATES, ANSWER_LABELS and MARKER_LABELS
   above and obey the same rule: the TOKENS are fixed by the schema, so the
   engine may hold them; the CONTENT they describe stays in the JSON. No
   morphology code, marker, entity or group name appears here, and a group that
   declares none of these fields never reaches any of it.

   RL_SCALE is ORDERED, and that order is the whole mechanism of the resource
   gate: a required level is compared against the level this site has for the
   family in question, never against a hard-coded expectation about any
   laboratory. */
var TRACK_LABELS = { who_cns5: 'WHO CNS5', adaptr_descriptive: 'ADAPTR descriptive' };
var GRADE_SYSTEM_LABELS = { roman: 'Roman numerals', arabic: 'Arabic numerals' };
var UNIT_LABELS = { per_mm2: 'per mm²', per_10_hpf: 'per 10 HPF',
  per_hpf: 'per HPF', percent: 'percent', ng_per_ml: 'ng/mL', iu_per_l: 'IU/L' };
var CODE_STATUS_LABELS = { shares_code: 'Shares its code with other entities',
  no_code: 'No code exists for this entity', own_code: 'Has its own ICD-O-3.2 code' };
var RL_SCALE = ['I', 'II', 'III', 'IV', 'V'];

/* Cleared per case. No localStorage — the iframe reloads between patients
   (Architecture §4D, §7). */
var state = {
  stage: 'boot',
  shell: 'auto', host: null,
  router: null, topography: null, aliasIndex: null,
  archetype: null, group: null, treeId: null, nodeId: null,
  organSystem: null,     /* the crosswalk row picked at Stage 1, before the region */
  labs: [],              /* the laboratory panel as recorded: values the clerk typed. Never read by a rule */
  candidates: [],        /* groups still possible — narrowed, never asked for blind */
  searchTerm: null,      /* the express-lane alias that set the candidates, if one did */
  dt: null, aliases: null,
  captured: {},          /* every resolution_logic[].when variable reads here */
  markers: {},
  draft: {},             /* in-progress input for the live node only */
  pending: null,         /* a branch parked mid-flight waiting on one answer */
  firedAlert: null,      /* alert of the branch that routed here, one hop only */
  pendingGrade: null,    /* a branch parked waiting on its grade criterion */
  grade: null,           /* the grade decision, once the criterion is answered */
  entity: null,          /* the entity annotation, carried to the output block */
  basisCodes: [],        /* ENCR basis-of-diagnosis codes asserted along the path */
  trail: [], trailAtGroupEntry: 0, workup: [], result: null, error: null, query: '',
  confirmExit: false,    /* Home was pressed on a case with answers, and the clerk has not yet said yes */
  focusNext: null,       /* a selector render() puts the keyboard focus on after the next draw, then clears */
  hopFrom: null          /* trail index the evidence starts from, after a referral hop; read once by enterGroup() */
};

var groupCache = new Map();   /* group number -> { dt, aliases } (Architecture §7) */

/* ---------------------------------------------------------------- helpers */
function esc(v) {
  return String(v === null || v === undefined ? '' : v)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}
/* Clinical alerts are authored with **markdown emphasis** on the word that
   carries the warning — "does **not** exclude", "on the **same** blast
   population". Escaped and printed raw, the asterisks show literally and the
   emphasis is lost on exactly the sentences that most need it. Bold is applied
   AFTER esc(), so the input is already inert HTML and this can only ever wrap
   text in <strong>. */
function rich(v) {
  return esc(v).replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
}
/* One closed-vocabulary token, rendered for a human. A known token gets its
   wording from the table; an unknown one still reads as words rather than as
   JSON, so a vocabulary the schema grows later degrades instead of breaking. */
function tokenLabel(map, v) {
  if (v === undefined || v === null || v === '') return '';
  return map[v] || String(v).replace(/_/g, ' ');
}
function byId(id) { return document.getElementById(id); }
function arr(v) { return Array.isArray(v) ? v : []; }

function snapshot() {
  return JSON.stringify({
    stage: state.stage, archetype: state.archetype, group: state.group,
    organSystem: state.organSystem, candidates: state.candidates,
    searchTerm: state.searchTerm || null,
    treeId: state.treeId, nodeId: state.nodeId, captured: state.captured,
    markers: state.markers, workup: state.workup, result: state.result, labs: state.labs,
    pending: state.pending || null, firedAlert: state.firedAlert || null,
    pendingGrade: state.pendingGrade || null, grade: state.grade || null,
    entity: state.entity || null, basisCodes: state.basisCodes,
    trailAtGroupEntry: state.trailAtGroupEntry, hopFrom: state.hopFrom
  });
}
function cachedGroup(g) {
  return (g === null || g === undefined) ? null : (groupCache.get(g) || groupCache.get(Number(g)) || null);
}
function restore(snap, upto) {
  var s = JSON.parse(snap);
  Object.keys(s).forEach(function (k) { state[k] = s[k]; });
  state.trail = state.trail.slice(0, upto);
  state.draft = {};
  /* The group file in memory is the one loaded last. A step back across a
     referral hop returns to a group the case left, so its file comes back with
     it: the screen reads nodes from the file and would not find them in the
     receiving group's. */
  var c = cachedGroup(state.group);
  if (c) { state.dt = c.dt; state.aliases = c.aliases; }
}
/* `before` is the snapshot taken BEFORE the answer was applied, so clicking a
   trail entry rewinds to the moment that question was asked. Trail entries are
   clickable in BOTH shells — a wrong answer is one tap from correction
   (engine.md §3).

   An AUTOMATIC entry records a step the engine took on its own — a tree routed
   from the topography, a group routed from the express-lane site — and asked
   nothing. Its snapshot is the state after the answer that triggered it, so
   rewinding to it would show that answer's screen again with the old answer
   still in the trail, and the trail would then name a group or tree the case
   is no longer in. Rewinding to an automatic entry rewinds to the clerk's
   answer that produced it instead (see 'rewind'). */
function pushTrail(label, value, before, automatic) {
  state.trail.push({ label: label, value: value, before: before, automatic: !!automatic });
}

/* --------------------------------------------------------------- fetching */
/* `no-cache` forces a revalidation against the server on every load. It does
   NOT disable caching — a 304 still serves from disk — but it guarantees the
   clerk never works from stale clinical data. Without it, a browser that has
   cached group_NN_dt.json keeps serving the old codes after the registry
   corrects one, and nothing in the UI would reveal it. */
function getJSON(path) {
  return fetch(path, { cache: 'no-cache' }).then(function (r) {
    if (!r.ok) throw new Error(path + ' → HTTP ' + r.status);
    return r.json();
  });
}
function loadRouter() {
  return Promise.all([
    getJSON('data/shared/presentation_router.json'),
    getJSON('data/shared/topography_codes.json'),
    getJSON('data/aliases/alias_index.json').catch(function () { return {}; })
  ]).then(function (r) {
    state.router = r[0]; state.topography = r[1]; state.aliasIndex = r[2];
  });
}
function loadGroupData(n) {
  if (groupCache.has(n)) { var c = groupCache.get(n); state.dt = c.dt; state.aliases = c.aliases; return Promise.resolve(); }
  var pad = String(n).length < 2 ? '0' + n : String(n);
  return Promise.all([
    getJSON('data/database/group_' + pad + '_dt.json'),
    getJSON('data/aliases/aliases_group_' + pad + '.json').catch(function () { return []; })
  ]).then(function (r) {
    groupCache.set(n, { dt: r[0], aliases: r[1] });
    state.dt = r[0]; state.aliases = r[1];
  });
}

/* ------------------------------------------------------------ tree lookup */
function trees() { return arr(state.dt && state.dt.decision_trees); }
function findNode(id) {
  var all = trees(), i, j;
  for (i = 0; i < all.length; i++) {
    var nodes = arr(all[i].nodes);
    for (j = 0; j < nodes.length; j++) if (nodes[j].node_id === id) return nodes[j];
  }
  return null;
}
function node() { return state.nodeId ? findNode(state.nodeId) : null; }
/* Behaviour-overloaded codes are separate entries, each with its own
   behavior_code, so a terminal may name one explicitly. */
function entryFor(code, behavior) {
  var list = arr(state.dt && state.dt.morphology_entries);
  var hit = null, i;
  for (i = 0; i < list.length; i++) {
    if (list[i].morphology_code !== String(code)) continue;
    if (behavior && String(list[i].behavior_code) !== String(behavior)) continue;
    hit = list[i]; break;
  }
  return hit;
}

/* --------------------------------------------- ordered topography rules
   ONE matcher, three callers. The router's `tree_routing` picks a decision
   tree from the topography captured at Stage 1; a morphology entry's
   `iccc3_subgroup_by_topography` picks the ICCC-3 subgroup at output time;
   `dual_group_rules` already uses the same shape. All three are an ordered
   list where the first match wins and a default catches the rest. Growing a
   second matcher for the second caller is how two rules that have to agree
   start disagreeing. */
function firstTopographyMatch(rules, topo) {
  var list = arr(rules), i;
  for (i = 0; i < list.length; i++) {
    if (arr(list[i].topography_in).indexOf(topo) !== -1) return list[i];
  }
  return null;
}
/* An entry's own subgroup is the DEFAULT, not the answer. One (code,
   behaviour) pair can sit in two ICCC-3 subgroups depending on where the
   tumour is, and the schema allows only one entry per pair — so the split is
   authored as rules on the entry and resolved against the captured
   topography here. Resolved at OUTPUT time, so rewinding to the site question
   and answering it differently re-resolves the subgroup with it. */
function subgroupFor(e, topo) {
  var hit = firstTopographyMatch(e && e.iccc3_subgroup_by_topography, topo);
  return {
    id: (hit && hit.iccc3_subgroup_id) || (e && e.iccc3_subgroup_id),
    name: (hit && hit.iccc3_subgroup_name) || (e && e.iccc3_subgroup_name)
  };
}

/* ----------------------------------------------------- dual-group routing */
/* Applies the router's topography-dependent rules to a resolved code
   (Architecture §6). The rules are data; only the mechanism is here — first
   matching branch wins, then `default`. */
function branchMatches(when, topo) {
  if (!when) return false;
  if (when.topography_in) return arr(when.topography_in).indexOf(topo) !== -1;
  if (!when.captured_variable) return false;
  var have = state.captured[when.captured_variable];
  if (when.equals !== undefined) return String(have) === String(when.equals);
  if (when.value !== undefined && when.operator) return numCompare(have, when.operator, when.value) === true;
  return false;
}
/* One operator table, shared by the router's dual-group branches and by an
   entity boundary. It returns **null**, not false, when the value cannot be
   read as a number: "undecidable" and "the comparison failed" are different
   facts, and a caller that collapses them states more than the file supports.
   An unknown operator throws rather than quietly failing every comparison. */
function numCompare(have, op, want) {
  var a = Number(have), b = Number(want);
  if (have === null || have === undefined || have === '' || isNaN(a)) return null;
  switch (op) {
    case '>=': return a >= b;  case '>': return a > b;
    case '<=': return a <= b;  case '<': return a < b;
    case '==': return a === b; case '!=': return a !== b;
  }
  throw new Error('Unknown operator: ' + op);
}
function resolveGroup(code, topo) {
  var rules = (state.router && state.router.dual_group_rules) || {};
  var keys = Object.keys(rules), i, j;
  for (i = 0; i < keys.length; i++) {
    var r = rules[keys[i]];
    if (!r || arr(r.codes).map(String).indexOf(String(code)) === -1) continue;
    /* A rule may assert a fixed group irrespective of site — a warning
       against re-routing rather than a split. */
    if (r.always) return { group: r.always.group, subgroup: r.always.subgroup, note: r.note };
    for (j = 0; j < arr(r.branches).length; j++) {
      var b = r.branches[j];
      if (branchMatches(b.when, topo)) {
        return { group: b.result.group, subgroup: b.result.subgroup, note: b.note || r.note };
      }
    }
    if (r.default) return { group: r.default.group, subgroup: r.default.subgroup, note: r.note };
    return null;
  }
  return null;
}

/* ============================================================================
   RENDER — one function, rebuilt from state on every change
   ========================================================================= */
var lastView = null;     /* which screen the last render drew, to tell a new screen from a re-render */
function render() {
  var app = byId('app');
  app.setAttribute('data-shell', state.shell);
  byId('appbar-context').textContent = contextLabel();
  /* A new screen starts with empty filter boxes. A re-render of the same
     screen keeps what the clerk typed, so a tick or a selection does not
     throw their search away. */
  var view = state.stage + ':' + (state.nodeId || '') + ':' + (state.pending ? 'b' : '') + (state.pendingGrade ? 'g' : '');
  var sameScreen = view === lastView;
  if (!sameScreen) {
    Object.keys(state.draft).forEach(function (k) { if (k.indexOf('f:') === 0) delete state.draft[k]; });
    lastView = view;
  }
  /* Home is the way out of a case at any point (registrar, 6 October 2026). It
     is hidden where there is no case to leave, and while the router has not
     loaded: a reset there would land on a screen with nothing to draw. */
  var home = byId('appbar-home');
  if (home) home.hidden = !state.router || ((state.stage === 'landing' || state.stage === 'boot') && !state.error);
  /* Rebuilding the screen drops the keyboard focus with the element that held
     it, so the control is noted first and found again after the swap. Only on
     a re-render of the same screen: a new screen starts with no focus. */
  var held = sameScreen ? focusKey(document.activeElement) : null;
  byId('rail').innerHTML = renderRail();
  byId('trail-rows').innerHTML = renderTrailRows();
  byId('slot').innerHTML = renderStage() + (state.confirmExit ? renderExitConfirm() : '');
  if (state.focusNext) { focusFound(state.focusNext); state.focusNext = null; }
  else if (held) focusFound(held);
  /* The question sits below the screen's content, so a long list must not hide it.
     The tool runs in a frame inside another page, so this scrolls THIS document
     only: scrollIntoView() can move the page that embeds it. */
  var bar = byId('slot').querySelector('.exitbar');
  if (bar) scrollToSee(bar);
}
/* A selector that finds the same control after a re-render: the action and the
   attributes that tell one control of that action from another. */
function focusKey(el) {
  if (!el || !el.getAttribute || !el.closest || !el.closest('#slot')) return null;
  var act = el.getAttribute('data-act');
  if (!act) return null;
  var sel = '[data-act="' + act + '"]';
  ['data-id', 'data-i', 'data-k', 'data-key'].forEach(function (a) {
    if (el.getAttribute(a) !== null) sel += '[' + a + '="' + el.getAttribute(a) + '"]';
  });
  if (el.type === 'radio') sel += '[value="' + el.value + '"]';
  return sel;
}
function focusFound(sel) {
  var el = document.querySelector(sel);
  if (!el || !el.focus) return;
  el.focus({ preventScroll: true });
  scrollToSee(el);
}
/* Scrolls this document just far enough to show the element's bottom edge. The
   tool runs in a frame, so scrollIntoView() and a plain focus() are not used:
   either can move the page that embeds it. */
function scrollToSee(el) {
  if (!el.getBoundingClientRect || !window.scrollBy) return;
  var hidden = el.getBoundingClientRect().bottom - window.innerHeight;
  if (hidden > 0) window.scrollBy(0, hidden + 8);
}
/* Leaving a case with answers in it asks first: the trail is the only copy.
   Quiet on purpose (registrar, 6 October 2026: the first version was a yellow
   box at the top and too eye-catching), and below the screen, not above it. */
function renderExitConfirm() {
  return '<div class="exitbar" role="alertdialog" aria-label="Leave this case?">' +
    '<span class="exitbar__text">Leave this case? The answers given so far will be discarded.</span>' +
    '<span class="exitbar__actions"><button class="btn btn--ghost" data-act="home-yes">Discard</button>' +
    '<button class="btn" data-act="home-no">Keep Working</button></span></div>';
}

function contextLabel() {
  if (state.error) return 'Error';
  /* Keyed to the group the case is in, not the last group file loaded: the
     file outlives a step back to the family question and a new case, and the
     bar would name a group the clerk has not chosen. */
  var md = state.dt && state.dt.metadata;
  if (state.group && md && (md.group_id === undefined || Number(md.group_id) === Number(state.group))) {
    return esc(md.group_name) + (state.result ? ' · case complete' : '');
  }
  /* The file in memory belongs to another group (a referral has just moved the
     case, and the receiving group's file is not loaded until its tree is
     entered), so the router names the group. */
  if (state.group && state.router && groupMeta(state.group).name) {
    return esc(groupMeta(state.group).name) + (state.result ? ' · case complete' : '');
  }
  return state.router ? 'New case' : 'Loading…';
}

/* The rail and the transcript are NOT two implementations. They are one
   caseTrail array rendered two ways (engine.md §3). */
function renderRail() {
  var h = '<div class="tag rail__title">This case</div>';
  state.trail.forEach(function (t, i) {
    h += '<button class="rail__row" data-act="rewind" data-i="' + i + '">' +
         '<b>' + esc(t.label) + '</b><span>' + esc(t.value) + '</span></button>';
  });
  h += '<div class="rail__row rail__row--now"><b>' + esc(currentLabel()) +
       '</b><span>' + (state.stage === 'search_unresolved' ? 'the tool stops here' : '… in progress') + '</span></div>';
  if (!state.result) h += '<div class="rail__row rail__row--todo"><b>Output</b><span>not yet</span></div>';
  return h;
}
function renderTrailRows() {
  return state.trail.map(function (t, i) {
    return '<button class="trail-row" data-act="rewind" data-i="' + i + '">' +
      '<em>' + esc(t.label) + '</em>' +
      '<b><span class="trail-row__tick">&check;</span> ' + esc(t.value) + '</b>' +
      '<u>change</u></button>';
  }).join('');
}
function currentLabel() {
  if (state.result) return 'Output';
  if (state.pendingGrade) return 'Grade';
  if (state.pending) return 'Behavior';
  var n = node();
  if (n) return n.step_label || n.node_type.replace(/_/g, ' ');
  if (state.stage === 'search_unresolved') return 'Refer to registrar';
  return state.stage.replace(/_/g, ' ');
}

function renderStage() {
  if (state.error) return banner('error', 'Cannot continue', state.error) +
    '<div class="actions"><button class="btn" data-act="retry">Retry</button></div>';
  switch (state.stage) {
    case 'boot':      return '<p class="node__hint">Loading…</p>';
    case 'landing':   return renderLanding();
    case 'archetype': return renderArchetype();
    case 'site':      return renderSite();
    case 'site_region': return renderSiteRegion();
    case 'discriminator': return renderDiscriminator();
    case 'group':     return renderGroupSelect();
    case 'search_unresolved': return renderSearchUnresolved();
    case 'handoff':   return renderHandoff();
    case 'node':      return renderLiveNode();
    case 'behaviour': return renderBehaviour();
    case 'grade':     return renderGrade();
    case 'output':    return renderOutput();
    default: throw new Error('Unknown stage: ' + state.stage);
  }
}

/* ------------------------------------------------------- Stage 0: landing */
/* Two front doors. Guided is the default; the search is the shortcut for a
   trained abstractor coding from a complete file (Design Spec §3.1). */
function renderLanding() {
  var h = '<h1 class="node__q">Code a new case</h1>' +
    '<p class="landing__lead">The tool is entered by clinical presentation, not by the ' +
    'term already written in the file. Presentation and site are captured first because ' +
    'group assignment is topography-dependent.</p><div class="doors">' +
    '<div class="door card"><h2>Guided entry</h2><p>Presentation, then site, then what ' +
    'documents are in the file.</p><button class="btn" data-act="guided">Start guided entry</button></div>' +
    '<div class="door card"><h2>Express lane</h2><p>Search the diagnostic term as written. ' +
    'Enters at the evidence gate.</p>' +
    '<label class="field"><span class="visually-hidden">Search diagnostic term</span>' +
    '<input type="search" id="q" data-act="query" value="' + esc(state.query) + '" placeholder="e.g. as written in the report"></label>' +
    '<div class="results">' + renderSearchResults() + '</div></div></div>';
  return h;
}
function renderSearchResults() {
  if (!state.query || state.query.length < 2) return '';
  var hits = searchAlias(state.query);
  if (!hits.length) return '<p class="node__hint">No match. Use guided entry.</p>';
  return pick('alias', hits.map(function (hit) {
    return { label: hit.alias, meta: 'Group ' + hit.groups.join(', ') };
  }), { filter: false });
}
/* Fuzzy-ish match against the lightweight startup index (Architecture §4C). */
function searchAlias(q) {
  var needle = q.toLowerCase(), out = [];
  Object.keys(state.aliasIndex || {}).forEach(function (k) {
    if (k.toLowerCase().indexOf(needle) !== -1) out.push({ alias: k, groups: arr(state.aliasIndex[k]) });
  });
  return out.sort(function (a, b) { return a.alias.length - b.alias.length; }).slice(0, 8);
}

/* ------------------------------------------- Stage 0/1: the router tier */
/* clinical_presentation and site_capture are ROUTER-OWNED and never appear in
   a group dt.json (DT master §3B) — so they render from the router file. */

/* Two shared builders. Every question in this tool is an overline, a question,
   an optional hint and a body — and almost every body is a list of one-tap
   options. Holding that in two functions is what keeps app.js near its size
   budget (Architecture §12) without pushing presentation into the JSON. */
function panel(over, question, hint, body) {
  return '<div class="node--live"><div class="tag node__over">' + esc(over) + '</div>' +
    '<p class="node__q" id="node-q">' + esc(question) + '</p>' +
    (hint ? '<p class="node__hint">' + esc(hint) + '</p>' : '') + body + '</div>';
}
/* ------------------------------------------------- the search box on a list */
/* Every single-choice list carries a filter box (registrar, 6 October 2026:
   every question, not only long ones). The options stay on screen, so one tap
   still answers; typing hides the options that do not match and Enter takes
   the first that does. A list this short needs no box, which is what raising
   this number buys — the registrar chose to have none removed. */
var FILTER_MIN_OPTIONS = 1;

/* Lower-cased and stripped of accents, so "Mullerian" finds "Müllerian". */
function foldText(s) {
  var t = String(s === null || s === undefined ? '' : s).toLowerCase();
  return t.normalize ? t.normalize('NFD').replace(/[̀-ͯ]/g, '') : t;
}
/* Every word the clerk typed must appear somewhere in the row's text. */
function findMatch(haystack, typed) {
  var terms = foldText(typed).split(/\s+/).filter(Boolean);
  return terms.every(function (t) { return haystack.indexOf(t) !== -1; });
}
/* The text a row answers to: its label, its meta line and anything extra the
   caller says belongs to it — an organ system also answers to its regions. */
function findText(it) {
  return foldText([it.label, it.meta, it.find].filter(Boolean).join(' '));
}
function filterBox(key) {
  return '<label class="field optbox__find"><span class="visually-hidden">Filter the options below</span>' +
    '<input type="search" data-act="filter" data-key="' + esc(key) + '" value="' + esc(state.draft['f:' + key] || '') +
    '" placeholder="Type to filter the options" autocomplete="off"></label>';
}
/* The count a screen reader hears after each keystroke in a filter box. */
function shownText(n) { return n === 1 ? '1 option shown' : n + ' options shown'; }
/* The DOM half: hide and show rows as the clerk types, with no re-render, so
   the cursor stays where it is. */
function applyFilter(input) {
  var box = input.closest('.optbox');
  if (!box) return;
  var typed = input.value, shown = 0;
  Array.prototype.forEach.call(box.querySelectorAll('[data-find]'), function (row) {
    /* The row the clerk has selected stays on screen, so what is selected is
       always what they can see: Confirm and Continue act on it. */
    var hit = rowSelected(row) || findMatch(row.getAttribute('data-find'), typed);
    row.hidden = !hit;
    if (hit) shown++;
  });
  var none = box.querySelector('.optbox__none');
  if (none) none.hidden = shown > 0;
  var say = box.querySelector('.optbox__status');
  if (say) say.textContent = shownText(shown);
}
function rowSelected(row) {
  return row.classList.contains('opt--selected') || !!row.querySelector('input:checked');
}

/* One list of one-tap options. `o.key` names the filter box (default: the
   action); `o.filter === false` leaves the box off; `o.selected` is the index
   of a row the clerk has tapped and not yet confirmed. An item may carry `aid`,
   the recognition aid, which shows beneath a SELECTED row and nowhere else. */
function pick(act, items, o) {
  o = o || {};
  var key = o.key || act;
  var typed = state.draft['f:' + key] || '';
  var withBox = o.filter !== false && items.length >= FILTER_MIN_OPTIONS;
  var shown = 0;
  var rows = items.map(function (it, i) {
    var on = o.selected !== undefined && o.selected !== null && Number(o.selected) === i;
    var hit = !withBox || !typed || on || findMatch(findText(it), typed);
    if (hit) shown++;
    return '<button class="opt' + (on ? ' opt--selected' : '') + '"' + (hit ? '' : ' hidden') +
      ' data-find="' + esc(findText(it)) + '" data-act="' + esc(act) + '" data-i="' + i + '"' +
      (o.selected !== undefined ? ' aria-pressed="' + (on ? 'true' : 'false') + '"' : '') + '>' +
      '<span class="opt__label">' + esc(it.label) +
      (it.meta ? '<span class="opt__meta">' + rich(it.meta) + '</span>' : '') +
      (it.aid && on ? '<span class="opt__aid">' + esc(it.aid) + '</span>' : '') +
      /* A CLINICAL ALERT AUTHORED ON A BRANCH IS CLERK-FACING (DT master §3E)
         — the counterpart of coding_note, which is author-facing and stays
         unrendered. On an option it must be visible BEFORE the option is
         taken: "a normal karyotype does not exclude this code" is worthless
         once the clerk has already picked "karyotype normal". Compact, not a
         banner each — several can be on screen at once. */
      (it.alert ? '<span class="opt__alert"><b>Clinical alert</b> ' + rich(it.alert) + '</span>' : '') +
      '</span></button>';
  }).join('');
  return '<div class="optbox">' + (withBox ? filterBox(key) : '') + '<div class="opts" role="group" aria-labelledby="node-q">' + rows + '</div>' +
    (withBox ? noneLine(shown) : '') + '</div>';
}
function noneLine(shown) {
  return '<p class="optbox__none"' + (shown ? ' hidden' : '') + '>No option matches. Clear the box to see them all.</p>' +
    '<span class="visually-hidden optbox__status" role="status" aria-live="polite">' + shownText(shown) + '</span>';
}
/* A single-choice list the clerk answers with Continue rather than a tap: radio
   rows under the same filter box. `name` is the draft key the choice lands in.
   Used where a tap would leave the screen before the rest of it is answered. */
function choose(name, items, selected) {
  var typed = state.draft['f:' + name] || '';
  var withBox = items.length >= FILTER_MIN_OPTIONS;
  var shown = 0;
  var rows = items.map(function (it, i) {
    var hit = !withBox || !typed || Number(selected) === i || findMatch(findText(it), typed);
    if (hit) shown++;
    return '<label class="check check--row"' + (hit ? '' : ' hidden') + ' data-find="' + esc(findText(it)) + '">' +
      '<input type="radio" name="' + esc(name) + '" data-act="draft" data-k="' + esc(name) + '" value="' + i + '"' +
      (Number(selected) === i ? ' checked' : '') + '> <span>' + esc(it.label) +
      (it.meta ? '<span class="opt__meta">' + rich(it.meta) + '</span>' : '') + '</span></label>';
  }).join('');
  return '<div class="optbox">' + (withBox ? filterBox(name) : '') + '<div class="checks" role="radiogroup" aria-labelledby="node-q">' + rows + '</div>' +
    (withBox ? noneLine(shown) : '') + '</div>';
}

function renderArchetype() {
  return panel('Stage 0 · presentation', 'What is the dominant presentation?',
    'Describe what you see in the file. If it blurs archetypes, choose "not sure".',
    pick('archetype', arr(state.router.archetypes).map(function (a) {
      return { label: a.label, meta: a.scaffold };
    })));
}

/* Site is asked in two taps, organ SYSTEM then REGION, and both come from the
   shared topography crosswalk so site is expressed in ONE vocabulary that
   site_capture, the narrowing below and the output block all consult
   (Architecture §4C).

   It used to be one tap that returned `codes[0]` for whichever row was picked,
   so "bone" always recorded C40.9 and the other six bone codes were
   unreachable — and "soft tissue" always recorded C47.9, which is the
   autonomic nervous system, for a rhabdomyosarcoma of the thigh. Layer 1 has
   twenty-one soft-tissue codes; the crosswalk carried two. */
function systemRows() {
  var a = state.archetype, cross = arr(state.topography.coarse_organ_crosswalk);
  if (a && a.auto_topography) {
    var stem = String(a.auto_topography).replace(/x$/, '');
    var only = cross.filter(function (c) {
      return arr(c.codes).some(function (code) { return code.indexOf(stem) === 0; });
    });
    if (only.length) return only;
  }
  /* A declared tissue origin does not HIDE the other systems — an abdominal
     mass is soft tissue and may still be renal or hepatic — it puts the
     systems that match the answer at the top of the list. */
  var origin = state.captured.tumour_origin;
  if (!origin) return cross;
  return cross.slice().sort(function (x, y) {
    return (x.tissue_origin === origin ? 0 : 1) - (y.tissue_origin === origin ? 0 : 1);
  });
}
function systemLabel(c) {
  return c.label || String(c.organ).replace(/_/g, ' ');
}
function regionOptions(row) {
  var look = state.topography.topography_lookup || {};
  return arr(row && row.codes).map(function (code) {
    var t = look[code] || {};
    return { topography: code, label: t.region_label || t.label || code, meta: code };
  });
}
function renderSite() {
  var origin = state.captured.tumour_origin;
  return panel('Stage 1 · organ system', 'Which organ system does the tumour arise in?',
    state.searchTerm
      ? (arr((state.aliasIndex || {})[state.searchTerm]).length > 1
          ? 'The search term “' + state.searchTerm + '” is filed under more than one group, and the primary site decides which. Code the primary, not the biopsy site.'
          : 'The primary site decides how “' + state.searchTerm + '” is coded, so it is asked first. Code the primary, not the biopsy site.')
      : state.archetype.site_capture === false
      ? 'Site is fixed for this presentation — one tap confirms which system to record.'
      : (origin
          ? 'Use the clinical examination notes and the imaging reports.'
          : 'The organ of origin, not the region of the swelling. Code the primary, not the biopsy site.'),
    pick('site', systemRows().map(function (c) {
      /* A system answers to the names of the regions inside it, so "ovary"
         finds "Ovary and testis" and "femur" finds "Bone and joints". */
      return { label: systemLabel(c), meta: c.topography_range + ' · ' + arr(c.codes).length + ' codes',
        find: regionOptions(c).map(function (r) { return r.label + ' ' + r.topography; }).join(' ') };
    })));
}
function renderSiteRegion() {
  var row = state.organSystem;
  return panel('Stage 1 · region', 'Where in ' + systemLabel(row).toLowerCase() + '?',
    'This is the topography code the registry records. Pick the one the report supports; NOS is a legitimate answer where it does not say.',
    pick('site_region', regionOptions(row).map(function (o) {
      return { label: o.label, meta: o.topography };
    })));
}

/* The discriminator topography cannot settle — asked by the router as its
   dual-group disambiguation question (DT master §3C, Architecture §6). */
function discriminator() {
  var key = state.archetype && state.archetype.dual_group_discriminator;
  return key ? (state.router.discriminators || {})[key] : null;
}
function renderDiscriminator() {
  var d = discriminator();
  /* `hint` is clerk-facing. `settles` / `authoring_note` explains the fork to
     whoever maintains the router and must never reach this screen — it names
     ICCC subgroups and JSON keys the abstractor has no use for. */
  return panel('Stage 1 · ' + String(d.variable).replace(/_/g, ' '), d.question, d.hint || null,
    pick('discriminator', arr(d.options).map(function (o) {
      return { label: typeof o === 'string' ? String(o).replace(/_/g, ' ') : o.label };
    })));
}

/* Asked ONLY when the presentation, the tissue origin and the topography
   together still leave more than one family — and never when none of the
   survivors is built, because then the only tappable row is the wrong answer.

   Until 4 Sep 2026 this fired for six of the seven presentations, because
   nothing narrowed: the archetype's advisory list went straight to the screen.
   A soft-tissue mass of the thigh was offered seven families with Group II the
   only one marked Available. */
function groupMeta(g) { return (state.router.groups || {})[String(g)] || {}; }
function renderGroupSelect() {
  var cands = arr(state.candidates);
  var built = cands.filter(function (g) { return groupMeta(g).built; });
  if (!built.length) {
    return banner('info', 'Not yet available',
        'The site and origin narrow this case to ' +
        cands.map(function (g) { return 'Group ' + g + ' — ' + (groupMeta(g).name || ''); }).join('; ') +
        '. No decision tree for ' + (cands.length > 1 ? 'either' : 'that') +
        ' group is in this build yet, so the tool cannot take the case further. ' +
        'Record the topography and refer the morphology to the registrar.') +
      '<div class="actions"><button class="btn btn--ghost" data-act="restart">Start again</button></div>';
  }
  return panel('Stage 1 · family',
    'The site narrows this to ' + cands.length + ' families. Which does the pathology report support?',
    'The tool cannot separate these from presentation and site alone. If the report does not say, stop here and refer it — do not guess.',
    pick('group', cands.map(function (g) {
      var m = groupMeta(g);
      return { label: m.name || ('Group ' + g), meta: m.built ? 'Available' : 'Not yet available in this build' };
    })));
}

/* The express lane's stop, reached when the site leaves no group or more than
   one for the search term. It names the term, its groups and the site — the
   three facts the registrar needs — and enters nothing. */
function renderSearchUnresolved() {
  var code = state.captured.topography;
  var t = (state.topography.topography_lookup || {})[code] || {};
  var siteName = code + ' ' + (t.region_label || t.label || '');
  var named = function (gs) {
    return gs.map(function (g) { return 'Group ' + g + ' — ' + (groupMeta(g).name || ''); }).join('; ');
  };
  var term = arr((state.aliasIndex || {})[state.searchTerm]);
  var none = !arr(state.candidates).length;
  var left = arr(state.candidates);
  return banner('info', none ? 'The term and the site point to different groups' : 'The site does not decide the group',
      'The search term “' + state.searchTerm + '” is filed under ' + named(term) + '. ' +
      (none
        ? 'The site recorded, ' + siteName + (term.length > 1 ? ', belongs to none of them.' : ', is not a site that group codes this term at.') + ' Check the primary site in the report and change it in the trail. If the site is right, refer the case to the registrar.'
        : (!Array.isArray(t.candidate_groups)
            ? 'The site recorded, ' + siteName + ', names no group, so the site cannot choose between them. '
            : (left.length === term.length
                ? (left.length === 2 ? 'Both occur' : 'All of them occur')
                : named(left) + (left.length === 2 ? ' both occur' : ' all occur')) +
              ' at ' + siteName + ', so the site cannot choose between them. ') +
          'Refer the case to the registrar with the topography recorded.')) +
    '<div class="actions"><button class="btn btn--ghost" data-act="restart">Start again</button></div>';
}

/* The handoff into a group tree. For a multi-tree group the router carries a
   one-tap data-level selector; each option names tree_id + that tree's
   document_inventory entry node (DT master §3B). */
function renderHandoff() {
  var meta = (state.router.groups || {})[String(state.group)] || {};
  if (!meta.built) {
    /* Name the group. "Not yet available" on its own tells the clerk nothing
       they can write down; the group and the topography are the two facts the
       case can still be registered on while the tree is missing. */
    return banner('info', 'Group ' + state.group + ' — ' + (meta.name || ''),
        (state.searchTerm ? 'The search term “' + state.searchTerm + '” places this case in Group ' :
          'The presentation, origin and site place this case in Group ') + state.group +
        (meta.name ? ', ' + meta.name : '') + '. No decision tree for that group is in this ' +
        'build yet, so the tool cannot reach a morphology code. Record the topography (' +
        esc(state.captured.topography || 'not captured') + ') and refer the morphology to the registrar.') +
      '<div class="actions"><button class="btn btn--ghost" data-act="restart">Start again</button></div>';
  }
  var sel = meta.tree_selection;
  /* Reached only for a built group that asks its tree. A group that ROUTES its
     tree never arrives here (afterGroup enters the tree directly), and a
     single-tree group never arrives here either — so a missing selector at
     this point is a router defect, and it is named rather than thrown as an
     undefined-property error three lines further down. */
  if (!sel) {
    throw new Error('Group ' + state.group + ' is built but declares neither ' +
      'tree_selection nor tree_routing nor a single tree in the router.');
  }
  return panel('Stage 1 · tree selection', sel.question, sel.default_rationale,
    pick('handoff', arr(sel.options).map(function (o) {
      return { label: o.label, meta: o.is_default ? 'Default when this is not documented' : null };
    })));
}


/* ============================================================================
   renderNode — the ONLY place the engine knows anything, and it knows node
   TYPES, not groups (Architecture §4D).
   ========================================================================= */
function renderLiveNode() {
  var n = node();
  if (!n) throw new Error('Unresolved node reference: ' + state.nodeId);
  if (NODE_TYPES.indexOf(n.node_type) === -1) throw new Error('Unknown node_type: ' + n.node_type);
  /* Ruling 9, 4 Sep 2026: clinical alerts do not render. This is a coding
     tool, not a live clinical tool, and a warning costs the clerk attention
     without changing the code that gets entered. Every alert string is kept in
     `docs/clinical-warnings.md` against the day the tool becomes clinical. */
  /* A gate on the node says whether this question is answerable HERE, so it
     is read before the question, not after it. A node the site cannot answer
     at all never renders: advance() diverts the branch routing into it. */
  return panel(n.step_label || ('Step ' + (n.step_number === undefined ? '' : n.step_number)),
    n.question || '', n.hint,
    gateNote(n.resource_level_gate) + priorNote(n.prior_probability) +
    dispatchNode(n) + renderEscapes(n));
}

/* `prior_probability` is DISPLAY-ONLY. It changes no code and no destination
   (§3.3). It is here because the same result means different things against
   different priors — a marker expected in nearly every case of one entity and
   in a handful of cases of another is not the same finding — and a clerk who
   cannot see the prior cannot weigh the result. It renders beside the thing it
   qualifies: the node's question, a marker group, or one option. */
function priorText(p) {
  if (!p) return '';
  var head = [p.test, p.context ? 'in ' + p.context : null,
    p.expected_positive_pct ? 'expected positive ' + p.expected_positive_pct + '%' : null]
    .filter(function (x) { return x; }).join(' · ');
  return head + (p.interpretation ? (head ? ' — ' : '') + p.interpretation : '');
}
function priorNote(p) {
  return p ? '<p class="node__hint">' + rich(priorText(p)) + '</p>' : '';
}

/* A node may declare the result states of the test it is asking about (§3.4).
   Those states AUGMENT the node's own control — they never replace it. The
   construct exists so an author does not have to fake a result state with a
   marker checkbox; it is one more captured fact, not the node's only answer.
   Replacing the control instead of adding to it emptied the group's entry node
   of its specimen ladder and left ten marker grids unrenderable, so no
   `positive[]` rule could ever match — a whole tree that still looked like it
   was working. The selectors render ABOVE the native control because an option
   list advances on tap: the state has to be settable before the tap that
   leaves the node. */
function dispatchNode(n) {
  return stateSelectors(n) + nodeControl(n);
}
function nodeControl(n) {
  if (n.tick_list) return tickControl(n);
  switch (n.node_type) {
    case 'clinical_presentation':
    case 'site_capture':
    case 'document_inventory':
    case 'morphology_only':
    case 'histology_subclassification':
    case 'site_resolution':
      return optionList(n);
    case 'cytogenetics_dropdown':  return cytogeneticsSelect(n);
    case 'ihc_checklist':
      return n.branch_sequence ? markerFlow(n) : markerGrid(n);
    case 'numeric_gate':           return numericGate(n);
    case 'lab_results':            return labControl(n);
    case 'molecular_freetext':     return freeText(n);
    case 'imaging_pathway':        return imagingPathway(n);
    case 'clinical_alias':         return optionList(n);
    default: throw new Error('No renderer for node_type: ' + n.node_type);
  }
}

/* The declared states of one test. The list includes `not_assessable`, which
   is why this exists at all: an unreadable test is not a negative one, and the
   two have to be separately answerable before the JSON's branches can keep
   them apart. Choosing one CAPTURES and re-renders without advancing, exactly
   as tapping a marker chip does — so a `when` on the variable is already
   satisfied by the time the node resolves, in either tap order. */
function stateLabel(s) { return String(s).replace(/_/g, ' '); }
/* One block, or several: a node may declare a state list per variable. */
function stateBlocks(n) {
  var t = n && n.test_result_states;
  return !t ? [] : (Array.isArray(t) ? t : [t]);
}
function stateSelectors(n) {
  return stateBlocks(n).map(function (b, bi) {
    var have = state.captured[b.variable];
    return '<div class="tag">' + esc(stateLabel(b.variable)) + '</div><div class="states">' +
      arr(b.states).map(function (st, i) {
        var on = have !== undefined && have !== null && String(have) === String(st);
        return '<button class="state" data-act="state" data-b="' + bi + '" data-i="' + i + '"' +
          ' aria-pressed="' + (on ? 'true' : 'false') + '"' +
          ' aria-label="' + esc(stateLabel(b.variable)) + ': ' + esc(stateLabel(st)) + '"' +
          (on ? ' data-on="1"' : '') + '>' +
          (on ? '<span class="state__tick">&check;</span> ' : '') + esc(stateLabel(st)) +
          '</button>';
      }).join('') + '</div>';
  }).join('');
}

/* An option names itself differently by node type — a finding, a descriptor,
   a site — but the engine only needs "whatever this option is called". */
function optionLabel(o) { return o.label || o.finding || o.descriptor || o.site || ''; }

function optionList(n) {
  var opts = arr(n.options);
  /* A terminal-NOS node may state its code directly instead of offering a list. */
  if (!opts.length && n.morphology_code) {
    return '<div class="actions"><button class="btn" data-act="direct">Accept ' +
      esc(n.accept_label || 'this result') + '</button></div>';
  }
  var items = opts.map(function (o) {
    /* An option carrying a gate says, before it is tapped, whether the test
       behind it can be done here — the same reason an option's clinical alert
       shows before it is taken rather than after. */
    var rl = o.resource_level_gate ? gateText(gateStatus(o.resource_level_gate)) : '';
    return { label: optionLabel(o),
             meta: [priorText(o.prior_probability), rl].filter(Boolean).join(' · ') || null,
             alert: o.clinical_alert || null,
             aid: o.recognition_aid || null };
  });
  /* A recognition aid is clerk-facing text in report vocabulary, shown under
     the option the clerk has SELECTED and nowhere else (registrar, 6 October
     2026). A list that carries any is answered select, then Confirm; every
     other list stays one tap. This is not the grey sub-line the 4 October
     ruling removed: that showed on every option, always, from coding_note. */
  if (!items.some(function (it) { return it.aid; })) return pick('opt', items);
  var sel = state.draft.sel;
  return pick('optsel', items, { selected: sel === undefined ? null : sel }) +
    '<div class="actions"><button class="btn" data-act="optconfirm"' + (sel === undefined ? ' disabled' : '') + '>Confirm</button></div>';
}

/* ============================================================================
   Tick lists (schema extension, ratified by the registrar on 6 October 2026)

   A node may declare `tick_list`. The clerk ticks which items are present and
   the engine picks a destination from the ticked set, instead of the clerk
   choosing one sentence. It is a field on an existing node_type, so the
   closed vocabulary is unchanged.

   An option may carry `ticks`: { requires, any_of, excludes }. It FITS a ticked
   set when every `requires` id is ticked, at least one `any_of` id is ticked
   (when any_of is given) and no `excludes` id is ticked. `ticks: {}` fits every
   set. The engine knows no item by name: the items are in the router
   (`tick_vocabularies`) or on the node.

     resolve "ask_siblings"  Options WITH `ticks` are tiers; options without
                             are special situations, listed under the checklist
                             and always choosable. One fitting tier is taken at
                             once; two or more are asked.
     resolve "first_match"   The first fitting option in file order is the
                             destination.

   The data gate proves, on every group, that no ticked set dead-ends and that
   every option can be reached; the engine gate drives the same sets through
   these functions.
   ========================================================================= */
function tickList(n) {
  var tl = n && n.tick_list;
  if (!tl) return null;
  var voc = null;
  if (tl.vocabulary) {
    voc = ((state.router && state.router.tick_vocabularies) || {})[tl.vocabulary];
    if (!voc) throw new Error('tick_list on ' + n.node_id + ' names an unknown vocabulary: ' + tl.vocabulary);
  }
  var out = {};
  [voc, tl].forEach(function (src) {
    Object.keys(src || {}).forEach(function (k) { out[k] = src[k]; });
  });
  out.items = arr(out.items);
  out.resolve = out.resolve || 'ask_siblings';
  if (!out.variable) throw new Error('tick_list on ' + n.node_id + ' names no variable to capture the ticks in');
  return out;
}
function tickFits(t, ids) {
  if (!t) return false;
  var has = function (x) { return ids.indexOf(x) !== -1; };
  var any = arr(t.any_of);
  return arr(t.requires).every(has) && (!any.length || any.some(has)) && !arr(t.excludes).some(has);
}
/* The options that fit, in file order, each with its index in n.options. */
function tickOffered(n, ids) {
  var out = [];
  arr(n.options).forEach(function (o, i) { if (o.ticks && tickFits(o.ticks, ids)) out.push({ i: i, o: o }); });
  return out;
}
function tickContexts(n) {
  var out = [];
  arr(n.options).forEach(function (o, i) { if (!o.ticks) out.push({ i: i, o: o }); });
  return out;
}
/* In the order the list is drawn, whatever order they were ticked in. */
function orderedTicks(tl, ids) {
  return tl.items.map(function (it) { return it.id; }).filter(function (id) { return ids.indexOf(id) !== -1; });
}
/* What is ticked on screen: this visit's draft, else what the case already
   holds — so a second gate in one case opens with the same boxes ticked. */
function ticksNow(tl) {
  return state.draft.ticks !== undefined ? state.draft.ticks : arr(state.captured[tl.variable]);
}
function tickLabels(tl, ids) {
  return ids.map(function (id) {
    var it = tl.items.filter(function (x) { return x.id === id; })[0];
    return it ? it.label : id;
  });
}
function tickControl(n) {
  var tl = tickList(n);
  if (tl.resolve === 'ask_siblings' && state.captured.tick_gate === n.node_id) return tickSiblings(n, tl);
  var on = ticksNow(tl);
  var h = '<p class="node__hint" id="tick-prompt">' + esc(tl.prompt || 'Tick every item that applies.') + '</p>' +
    '<div class="checks" role="group" aria-labelledby="tick-prompt">' + tl.items.map(function (it) {
      return '<label class="check"><input type="checkbox" data-act="tick" data-id="' + esc(it.id) + '"' +
        (on.indexOf(it.id) !== -1 ? ' checked' : '') + '> ' + esc(it.label) + '</label>';
    }).join('') + '</div>';
  var ctx = tickContexts(n);
  if (ctx.length && tl.resolve === 'ask_siblings') {
    h += '<div class="tag">' + esc(tl.context_prompt || 'Does one of these apply?') + '</div>' +
      choose('ctx', [{ label: tl.none_label || 'None of these' }].concat(ctx.map(function (c) {
        return { label: optionLabel(c.o) };
      })), Number(state.draft.ctx) || 0);
  }
  return h + '<div class="actions"><button class="btn" data-act="tick-continue">Continue</button></div>';
}
/* Two or more tiers fit the ticked documents: the clerk says which describes the file. */
function tickSiblings(n, tl) {
  var offered = tickOffered(n, arr(state.captured[tl.variable]));
  return '<p class="node__hint">' + esc(tl.sibling_prompt ||
    'More than one description fits what is in the file. Pick the one that describes it.') + '</p>' +
    pick('tickopt', offered.map(function (c) {
      return { label: optionLabel(c.o), meta: priorText(c.o.prior_probability) || null, alert: c.o.clinical_alert || null };
    }));
}
/* Continue on the checklist. The ticks go on the trail and onto the case, then
   the destination is the special situation chosen, the first fit, the one tier
   that fits, or, when several fit, a second question. */
function tickContinue(n, before) {
  var tl = tickList(n);
  var ids = orderedTicks(tl, ticksNow(tl));
  var names = tickLabels(tl, ids);
  pushTrail(tl.label || n.step_label || 'Ticked', names.length ? names.join(', ') : 'Nothing ticked', before);
  state.trail[state.trail.length - 1].ticks = ids.slice();
  state.captured[tl.variable] = ids;
  var after = snapshot(), label = n.step_label || 'Answer';
  if (tl.resolve === 'first_match') {
    var hit = tickOffered(n, ids)[0];
    if (!hit) throw new Error('No option on ' + n.node_id + ' fits the ticked set: ' + (ids.join(', ') || 'nothing'));
    return advance(hit.o, label, optionLabel(hit.o), after, true);
  }
  var pickedCtx = Number(state.draft.ctx) || 0;
  if (pickedCtx > 0) {
    var c = tickContexts(n)[pickedCtx - 1];
    if (c) return advance(c.o, label, optionLabel(c.o), after, true);
  }
  var offered = tickOffered(n, ids);
  if (!offered.length) throw new Error('No tier on ' + n.node_id + ' fits the ticked set: ' + (ids.join(', ') || 'nothing'));
  if (offered.length === 1) {
    var at = state.trail.length;
    var went = advance(offered[0].o, label, optionLabel(offered[0].o), after, true);
    /* The tier is the engine's description of the documents ticked, not the clerk's
       answer, and its wording can say more or less than they ticked ("no imaging
       report" beside an imaging report). The documents ticked are the evidence, so
       "Suggested based on" lists those and not this sentence. */
    state.trail[at].quiet = true;
    return went;
  }
  state.captured.tick_gate = n.node_id;
  state.draft = {};
}

/* ============================================================================
   Laboratory results (node_type `lab_results`, registrar, 6 October 2026)

   One screen with a row per laboratory test: the number as the report gives it,
   its unit from the test's own list, and "Not in the file". The boxes start
   empty (registrar, 6 October 2026); a row left without a number is recorded as
   not in the file, ticked or not, and ticking the box also clears a number.
   The numbers are RECORDED and
   shown on the result and nothing more: they are kept in `state.labs`, never in
   `state.captured`, so no rule, `when` or gate can read one, and a value never
   chooses a code. The tool interprets nothing here: no cut-off, no "raised".
   The node routes by its own `next_node`.
   ========================================================================= */
/* The rows as typed so far; else what the case already holds, so a clerk who
   steps back finds the panel as they left it. */
function labDraft() {
  if (state.draft.labs) return state.draft.labs;
  var held = {};
  arr(state.labs).forEach(function (l) {
    held[l.id] = { value: l.inFile ? l.value : '', unit: l.unit };
  });
  return held;
}
/* A row with no number records no result, whether or not its box is ticked. */
function labRowAbsent(r) {
  var typed = r && r.value !== undefined ? String(r.value).trim() : '';
  return typed === '' || !!(r && r.absent);
}
/* The unit the row holds when it is on the test's own list, else the list's first. */
function labUnit(lab, r) {
  var units = arr(lab.units);
  return r && units.indexOf(r.unit) !== -1 ? r.unit : (units[0] || '');
}
/* Digits with at most one decimal mark, as a report prints a result. */
var LAB_NUMBER = /^\d+(?:[.,]\d+)?$/;
function labControl(n) {
  var d = labDraft();
  var h = '<div class="labs">' + arr(n.labs).map(function (lab, i) {
    var r = d[lab.id] || {}, units = arr(lab.units), unit = labUnit(lab, r);
    var ticked = !!r.absent, id = 'lab-' + lab.id;
    return '<div class="labrow">' +
      '<label class="labrow__name" for="' + esc(id) + '">' + esc(lab.label) + '</label>' +
      '<span class="labrow__entry">' +
      '<input id="' + esc(id) + '" class="labrow__value" type="text" inputmode="decimal" autocomplete="off" maxlength="12" data-act="labval" data-i="' + i + '"' +
      ' value="' + esc(r.value === undefined ? '' : r.value) + '"' + (r.error ? ' aria-invalid="true" aria-describedby="' + esc(id) + '-error"' : '') + '>' +
      '<select class="labrow__unit" data-act="labunit" data-i="' + i + '" aria-label="Unit for ' + esc(lab.label) + '">' +
      units.map(function (u) {
        return '<option value="' + esc(u) + '"' + (u === unit ? ' selected' : '') + '>' + esc(u) + '</option>';
      }).join('') + '</select>' +
      '<label class="check labrow__absent"><input type="checkbox" data-act="lababsent" data-i="' + i + '"' +
      ' aria-label="Not in the file: ' + esc(lab.label) + '"' + (ticked ? ' checked' : '') + '> Not in the file</label></span>' +
      (r.error ? '<span class="labrow__error" id="' + esc(id) + '-error" role="alert">' + esc(r.error) + '</span>' : '') + '</div>';
  }).join('') + '</div>';
  return h + '<div class="actions"><button class="btn" data-act="labs-continue">Continue</button></div>';
}
/* The panel as one line, for the trail: "Alpha-fetoprotein 2.1 ng/mL · Lactate
   dehydrogenase 450 U/L · 6 not in the file". */
function labSummary(rows) {
  var inFile = rows.filter(function (l) { return l.inFile; });
  if (!inFile.length) return 'None of ' + rows.length + ' in the file';
  var absent = rows.length - inFile.length;
  return inFile.map(function (l) { return l.label + ' ' + l.value + ' ' + l.unit; }).join(' · ') +
    (absent ? ' · ' + absent + ' not in the file' : '');
}
function labsContinue(n, before) {
  var d = labDraft(), rows = [], typedRows = {}, bad = false, mine = {};
  arr(n.labs).forEach(function (lab) {
    var r = d[lab.id] || {}, unit = labUnit(lab, r);
    var typed = r.value === undefined ? '' : String(r.value).trim();
    /* The draft keeps what the clerk did: the number as typed and the box as
       they left it. A blank row is RECORDED as not in the file, but it is not
       ticked on their behalf, so a refused Continue or a step back shows the
       boxes as they were. */
    var row = { value: typed, unit: unit, absent: !!r.absent };
    mine[lab.id] = true;
    if (labRowAbsent(r)) {
      rows.push({ id: lab.id, label: lab.label, value: '', unit: '', inFile: false });
    } else if (!LAB_NUMBER.test(typed)) {
      row.error = 'Enter a number: digits with one decimal mark. “' + typed + '” is not one.';
      bad = true;
    } else {
      rows.push({ id: lab.id, label: lab.label, value: typed, unit: unit, inFile: true });
    }
    typedRows[lab.id] = row;
  });
  if (bad) {
    state.draft.labs = typedRows;
    state.focusNext = '.labrow__value[aria-invalid="true"]';
    return;
  }
  /* A panel replaces the rows of the tests it lists and keeps the rest, so a
     second panel in the same case does not erase the first. */
  state.labs = arr(state.labs).filter(function (l) { return !mine[l.id]; }).concat(rows);
  /* A panel with a result in it means a laboratory report is in the file, so the
     evidence checklist that follows opens with that box ticked. The node names
     the vocabulary and the ids; the engine knows neither. */
  var imp = n.implies_ticks, voc = imp && ((state.router.tick_vocabularies || {})[imp.vocabulary]);
  if (voc && rows.some(function (l) { return l.inFile; })) {
    var have = arr(state.captured[voc.variable]).slice();
    arr(imp.ids).forEach(function (id) { if (have.indexOf(id) === -1) have.push(id); });
    state.captured[voc.variable] = arr(voc.items).map(function (it) { return it.id; })
      .filter(function (id) { return have.indexOf(id) !== -1; });
  }
  var at = state.trail.length;
  advance({ next_node: n.next_node }, n.step_label || 'Laboratory results', labSummary(rows), before);
  /* The values are not what the code rests on, so they stay out of "Suggested
     based on"; and stepping back reopens the screen as it was typed. They are
     what a clerk typed, so the entry is marked typed, and nothing that reports
     the case may print them. */
  state.trail[at].quiet = true;
  state.trail[at].typed = true;
  state.trail[at].labDraft = JSON.parse(JSON.stringify(typedRows));
}
/* The recorded panel on the result: each test, its value and unit, or "not in the file". */
function labResultsBlock() {
  var rows = arr(state.labs);
  if (!rows.length) return '';
  return '<div class="labblock"><div class="tag">Laboratory results</div>' + rows.map(function (l) {
    return orow(l.label, l.inFile ? l.value + ' ' + l.unit : 'not in the file');
  }).join('') + '</div>';
}

function cytogeneticsSelect(n) {
  var opts = arr(n.options);
  var h = '<div class="tag">Reported finding</div>' +
    choose('option', opts.map(function (o) { return { label: o.label || o.finding }; }), state.draft.option);
  var chosen = state.draft.option !== undefined && state.draft.option !== '' ? opts[+state.draft.option] : null;
  /* A native <option> cannot carry markup, so a dropdown option's alert shows
     the moment it is selected — still before Continue commits it. */
  if (chosen && chosen.clinical_alert) h += banner('alert', 'Clinical alert', chosen.clinical_alert);
  /* detection_method is why a normal result cannot silently close a branch. */
  if (chosen && chosen.detection_method) {
    h += banner('info', 'Detection method', String(chosen.detection_method).replace(/_/g, ' '));
  }
  if (chosen) h += priorNote(chosen.prior_probability);
  h += '<div class="actions"><button class="btn" data-act="resolve"' + (chosen ? '' : ' disabled') + '>Continue</button></div>';
  return h;
}

/* Tap cycles a marker: off → positive → strong → weak → negative. The
   intensity tokens ("MARKER:strong") are backward-compatible with plain
   marker names — a rule that names no intensity matches any positive state. */
/* ============================================================================
   Ruling 13 — the checklist is a flow chart

   The old shape put every marker the node knew about on one screen and ran an
   ordered rule list against whatever was ticked. Two consequences, neither of
   them visible: a rule whose conditions are a subset of an earlier rule's can
   never fire, and the clerk sees every code the node can reach with nothing
   saying which are still in play.

   Now the node asks one marker at a time, in the order `branch_sequence.order`
   fixes at build time, skipping any marker no live rule turns on, and stops
   when one rule stands. The order is clinical content and comes from the JSON;
   the narrowing below is arithmetic on rules the engine already evaluates.
   ========================================================================= */

/* Live during a PARTIAL walk. Differs from matchRules in one way that matters:
   an unanswered `when` leaves the rule alive instead of killing it, because
   the clerk may not have reached that question yet. */
function whenLive(when) {
  if (!when) return true;
  return Object.keys(when).every(function (k) {
    var have = state.captured[k];
    return have === undefined || have === null || whenValueOk(have, when[k]);
  });
}
function splitToken(token) {
  var m = /^([\s\S]*):(strong|weak)$/.exec(String(token));
  return m ? { name: m[1], want: m[2] } : { name: String(token), want: null };
}
function ruleLive(r) {
  if (!whenLive(r.when)) return false;
  var ok = true;
  arr(r.positive).forEach(function (p) {
    var t = splitToken(p), have = state.markers[t.name];
    if (have === undefined) return;
    if (have === 'neg' || have === MARKER_UNREAD) ok = false;
    else if (t.want && have !== t.want) ok = false;
  });
  arr(r.negative).forEach(function (name) {
    if (state.markers[name] !== undefined && !markerOff(name)) ok = false;
  });
  return ok;
}
function liveRules(n) { return arr(n.resolution_logic).filter(ruleLive); }

/* What a rule asks of one marker, or null if it does not care. */
function markerNeed(r, name) {
  var need = null;
  arr(r.positive).forEach(function (p) {
    var t = splitToken(p);
    if (t.name === name) need = t.want || 'pos';
  });
  if (need) return need;
  return arr(r.negative).indexOf(name) === -1 ? null : 'neg';
}

/* Where a rule lands. Several rules often land in the same place, and it is the
   number of PLACES still reachable that the clerk watches shrink — so that, not
   the number of rules, is what a question is worth asking about. */
function outcomeKey(r) {
  if (r.morphology_code) return 'code:' + r.morphology_code + '/' + (r.behavior_code || '');
  if (r.next_node) return 'node:' + r.next_node;
  if (r.refer_group) return 'group:' + r.refer_group;
  if (r.exclude) return 'exclude';
  return 'continue';
}
function outcomeCount(rules) {
  var seen = {}, n = 0;
  rules.forEach(function (r) { var k = outcomeKey(r); if (!seen[k]) { seen[k] = 1; n++; } });
  return n;
}
/* Is this rule already satisfied outright by the answers so far? Same test
   matchRules() applies — factored out so the flow chart can ask it. */
function ruleSatisfied(r) {
  if (!whenOk(r.when)) return false;
  if (arr(r.positive).length && !arr(r.positive).every(markerOk)) return false;
  if (arr(r.negative).length && !arr(r.negative).every(markerOff)) return false;
  return true;
}

/* What a marker is worth asking, as [outcomes removed, rules removed], each
   averaged across the answers. Scored on the mean rather than the worst answer:
   near the top of a node almost every rule is alive, so for every marker there
   is some answer that eliminates nothing, and worst-case scoring makes every
   question score zero and the tool ask all of them in file order.

   Outcomes lead because the clerk is coding — a question that cannot change the
   code is not worth asking. Rules break the tie, because a node where nine rules
   emit one code and a tenth falls through never reduces its outcome count, and
   scoring on outcomes alone would ask nothing at all there. */
function markerWorth(m, live) {
  var hereO = outcomeCount(live), hereR = live.length;
  var opts = ['pos', 'neg'], totO = 0, totR = 0;
  live.forEach(function (r) {
    var need = markerNeed(r, m);
    if ((need === 'strong' || need === 'weak') && opts.indexOf(need) === -1) opts.push(need);
  });
  opts.forEach(function (v) {
    var keep = live.filter(function (r) {
      var need = markerNeed(r, m);
      if (!need) return true;
      if (need === 'neg') return v === 'neg';
      if (v === 'neg') return false;
      return need === 'pos' || need === v;
    });
    totO += outcomeCount(keep);
    totR += keep.length;
  });
  return [hereO - totO / opts.length, hereR - totR / opts.length];
}

/* The next question: the first marker in the authored order that is unanswered
   and still narrows the answer set. The ORDER is clinical content and comes from
   the JSON; deciding that a question would change nothing is arithmetic on rules
   the engine already evaluates. */
function nextMarker(n) {
  var rules = arr(n.resolution_logic), live = liveRules(n);
  /* Two ways the node is already decided, and asking on would be theatre: one
     rule left, or every remaining rule emitting the same outcome.

     BUT "one rule left" IS NOT "decided", AND THAT COST A WRONG CODE. A rule
     stays LIVE while a marker it requires is merely unanswered — ruleLive()
     skips an undefined marker rather than failing on it, which is what lets a
     partial walk narrow at all. So the surviving rule can be the only one left
     and still not be SATISFIED, and stopping on live.length alone stops there:
     the screen names the outcome that remains, matchRules() then matches
     nothing because the rule's marker was never asked, and the node emits its
     nos_fallback. The tool tells the clerk one code and records another.

     Nothing in the build catches it: the rule has a witness and the flow chart
     is well formed, so it is the ASKING ORDER that is wrong, not the data.
     Reproduction, sweep and negative controls:
     docs/engine_flow_negative_controls.md.

     So the node is decided only when what survives is also satisfied. When it
     is not, fall through and let markerWorth() pick the marker that settles
     it: against a single unsatisfied rule every answer still splits match from
     no-match, so the question scores above zero and gets asked. */
  if (!live.length) return null;
  if ((live.length <= 1 || outcomeCount(live) <= 1) && live.every(ruleSatisfied)) return null;

  /* Once a live rule is satisfied outright, only the rules ABOVE it can still
     change the answer — first match wins, so anything below it is settled. Ask
     about those rules and nothing else, and stop when none is left. Without this
     the tail of a long node is spent on questions that cannot move the code:
     a systemic ALCL took seventeen questions where nine decide it. */
  var settled = -1;
  for (var s = 0; s < rules.length; s++) {
    if (!ruleLive(rules[s])) continue;
    if (ruleSatisfied(rules[s])) { settled = s; break; }
  }
  var contenders = live;
  if (settled >= 0) {
    contenders = rules.slice(0, settled).filter(ruleLive);
    if (!contenders.length) return null;
  }

  var order = arr(n.branch_sequence && n.branch_sequence.order);
  for (var i = 0; i < order.length; i++) {
    var m = order[i];
    if (state.markers[m] !== undefined) continue;
    var w = markerWorth(m, contenders);
    if (w[0] <= 1e-9 && w[1] <= 1e-9) continue;
    /* First in the authored order wins among the questions worth asking at all,
       so the sequence stays the one the build wrote and the clerk can predict
       it. The scores decide WHETHER to ask, not what to ask next. */
    return m;
  }
  return null;
}

/* The answers worth offering for this marker. Intensity buttons appear only
   where a live rule actually grades it — a clerk should not be asked to grade
   a stain no rule reads that way. */
function markerAnswers(n, m) {
  var live = liveRules(n), wants = {};
  live.forEach(function (r) { var w = markerNeed(r, m); if (w) wants[w] = true; });
  var out = [{ v: 'pos', label: 'Positive' }];
  if (wants.strong) out.push({ v: 'strong', label: 'Strongly positive' });
  if (wants.weak) out.push({ v: 'weak', label: 'Weakly positive' });
  out.push({ v: 'neg', label: 'Negative' });
  out.push({ v: MARKER_UNREAD, label: 'Not done or not readable' });
  return out;
}

/* Where each live rule would land. This is the "only these codes are loaded"
   half of the ruling: the clerk watches the candidate set shrink instead of
   reading a wall of codes the branch already excluded. */
function outcomeOf(r) {
  if (r.morphology_code) {
    var e = entryFor(r.morphology_code, r.behavior_code);
    return r.morphology_code + (e ? ' ' + e.morphology_name : '');
  }
  if (r.next_node) {
    var nn = findNode(r.next_node);
    return (nn && (nn.step_label || nn.node_id)) || r.next_node;
  }
  if (r.refer_group) return 'Group ' + r.refer_group;
  if (r.exclude) return 'Not a reportable malignancy';
  return 'Continue';
}
function candidateList(n) {
  var seen = {}, out = [];
  liveRules(n).forEach(function (r) {
    var o = outcomeOf(r);
    if (!seen[o]) { seen[o] = true; out.push(o); }
  });
  return out;
}

function answeredChips(n) {
  var order = arr(n.branch_sequence && n.branch_sequence.order);
  var done = order.filter(function (m) { return state.markers[m] !== undefined; });
  if (!done.length) return '';
  return '<div class="tag">Answered</div><div class="markers">' +
    done.map(function (m) {
      var v = state.markers[m];
      return '<button class="marker" data-act="markerset" data-m="' + esc(m) + '" data-v="clear"' +
        ' data-value="' + esc(v) + '" aria-pressed="' + (v === 'neg' || v === MARKER_UNREAD ? 'false' : 'true') + '"' +
        ' aria-label="' + esc(m) + ': ' + esc(MARKER_LABELS[v]) + '. Activate to unanswer.">' +
        esc(m) + '<span class="marker__state">' + esc(v === 'nd' ? 'not read' : MARKER_LABELS[v]) + '</span></button>';
    }).join('') + '</div>';
}

/* What Continue records when no rule is satisfied, in the same words the
   candidate list uses for everything else. Empty for a node with no fallback —
   that is a data defect the build catches, and not a reason for the panel to
   stop rendering. */
function fallbackOutcome(n) {
  try { return outcomeOf(fallbackTarget(n)); } catch (e) { return ''; }
}

function markerFlow(n) {
  var live = liveRules(n), m = nextMarker(n);
  var cands = candidateList(n);
  var h = answeredChips(n);
  h += '<div class="flow__count">' + esc(String(cands.length)) +
    (cands.length === 1 ? ' outcome still in play' : ' outcomes still in play') + '</div>';
  h += '<ul class="flow__cands">' + cands.slice(0, 8).map(function (c) {
    return '<li>' + esc(c) + '</li>';
  }).join('') + (cands.length > 8 ? '<li>and ' + (cands.length - 8) + ' more</li>' : '') + '</ul>';
  if (m) {
    h += '<div class="flow__ask"><div class="flow__marker">' + esc(m) + '</div>' +
      '<div class="states">' + markerAnswers(n, m).map(function (a) {
        return '<button class="state" data-act="markerset" data-m="' + esc(m) + '" data-v="' + esc(a.v) + '"' +
          ' aria-label="' + esc(m) + ': ' + esc(a.label) + '">' + esc(a.label) + '</button>';
      }).join('') + '</div></div>';
    h += '<p class="node__hint">One marker at a time. Every answer removes the outcomes it rules out.</p>';
  } else {
    /* THE SCREEN MAY NOT PROMISE WHAT THE BUTTON WILL NOT DELIVER. This message
       used to be chosen by outcomeCount(live) alone, and liveness is not
       settlement: a rule stays live while a marker it needs is merely
       unanswered, so a node could read "One outcome remains. Continue to record
       it." above a single candidate and then record its nos_fallback, because
       matchRules() — which needs the marker actually answered — matched
       nothing. Worse where nothing was left alive at all: the count line read
       "0 outcomes still in play" and the sentence under it still promised one.
       Reachable in over a thousand states across fifteen nodes when it was
       swept — sweep and negative controls:
       docs/engine_flow_negative_controls.md.

       So the wording is chosen by the same call the Continue button makes.
       Where a rule is satisfied the old two sentences stand, and where none is
       the clerk is told plainly which code is about to be recorded instead of
       being left to infer it from a list that no longer applies. */
    var picked = matchRules(n.resolution_logic), fb = fallbackOutcome(n);
    h += '<p class="node__hint">' + (picked
      ? (cands.length <= 1
        ? 'One outcome remains. Continue to record it.'
        : 'No remaining marker separates what is left — continue, and the first rule the '
          + 'answers satisfy decides it.')
      : esc('These answers match no rule on this node' +
        (cands.length ? ', so nothing listed above is settled' : '') + '.' +
        (fb ? ' Continue records ' + fb + '.' : ''))) + '</p>';
  }
  h += '<div class="actions"><button class="btn" data-act="resolve">' +
    (m ? 'Skip the rest and resolve' : 'Continue') + '</button></div>';
  return h;
}

function markerGrid(n) {
  var h = arr(n.marker_groups).map(function (g) {
    return '<div class="tag">' + esc(g.group_label) + '</div>' + priorNote(g.prior_probability) +
      '<div class="markers">' +
      arr(g.markers).map(function (m) {
        var v = state.markers[m];
        var pressed = v && v !== 'neg' ? 'true' : 'false';
        return '<button class="marker" data-act="marker" data-m="' + esc(m) + '"' +
          ' aria-pressed="' + pressed + '"' +
          ' aria-label="' + esc(m) + ': ' + esc(v ? MARKER_LABELS[v] : 'not recorded') + '"' +
          (v ? ' data-value="' + esc(v) + '"' : '') + '>' + esc(m) +
          (v === 'strong' || v === 'weak' ? '<span class="marker__int">' + esc(v === 'strong' ? 'str' : 'wk') + '</span>' : '') +
          (v === 'neg' ? '<span class="marker__state">neg</span>' : '') +
          '</button>';
      }).join('') + '</div>';
  }).join('');
  h += '<p class="node__hint">Tap once for positive, again for strong, again for weak, again for negative.</p>';
  h += '<div class="actions"><button class="btn" data-act="resolve">Continue</button></div>';
  return h;
}

/* A continuous threshold with a genetic override — the ratified `numeric_gate`
   (Pathway §7.3 item 1). Reusable for any continuous diagnostic gate. */
/* A BAND'S UNIT IS ITS DENOMINATOR, and a count read against the wrong one is
   a different number: four mitoses per 10 HPF and four per mm² are not the
   same finding, and the same threshold answered against the wrong denominator
   is wrong in whichever direction the areas differ. So the unit reaches the
   clerk before the reading is typed, and the trail after it. Bands authored
   without a unit (every band in the groups built before this) render and
   resolve exactly as they did — the node's own `unit` still labels the field. */
function bandUnitText(b) {
  if (!b || !b.unit) return '';
  return tokenLabel(UNIT_LABELS, b.unit) +
    (b.hpf_area_mm2 ? ' (' + b.hpf_area_mm2 + ' mm²)' : '');
}
function bandUnits(n) {
  var seen = {}, out = [];
  arr(n.bands).forEach(function (b) {
    var t = bandUnitText(b);
    if (t && !seen[t]) { seen[t] = true; out.push(t); }
  });
  return out;
}
function numericGate(n) {
  var undoc = state.draft.not_documented === true;
  var units = bandUnits(n),
    label = tokenLabel(UNIT_LABELS, n.unit) || (units.length === 1 ? units[0] : '');
  return '<label class="field"><span class="field__label">' + esc(n.variable_label || n.variable) +
    (label ? ' (' + esc(label) + ')' : '') + '</span>' +
    '<input type="number" step="any" data-act="draft" data-k="value" value="' +
    esc(state.draft.value === undefined ? '' : state.draft.value) + '"' + (undoc ? ' disabled' : '') + '></label>' +
    /* One sentence for every kind of unit. It was written for counts and said
       "denominator" and "count" under a serum concentration too (Group III's
       pineal marker screens, 6 October 2026). A unit carries its own
       denominator ("per mm²" is not "per 10 HPF"), so asking for the same unit
       covers both, and a count is named in the same breath. */
    (units.length ? '<p class="node__hint">Thresholds on this question are read ' +
      esc(units.join(', and ')) + '. Check that the report gives the value in the same unit, ' +
      'and a count over the same denominator, before entering it.</p>' : '') +
    '<div class="checks"><label class="check"><input type="checkbox" data-act="draft" data-k="not_documented"' +
    (undoc ? ' checked' : '') + '> Not documented in the file</label></div>' +
    '<div class="actions"><button class="btn" data-act="resolve">Continue</button></div>';
}

function freeText(n) {
  return '<label class="field"><span class="field__label">' + esc(n.capture_label || 'Result as reported') + '</span>' +
    '<textarea data-act="draft" data-k="text">' + esc(state.draft.text || '') + '</textarea></label>' +
    '<p class="node__hint">Recorded on the case even when it does not change the code.</p>' +
    '<div class="actions"><button class="btn" data-act="resolve">Continue</button></div>';
}

function imagingPathway(n) {
  var h = '<div class="checks">' + arr(n.imaging_features).map(function (f, i) {
    return '<label class="check"><input type="checkbox" data-act="feature" data-i="' + i + '"' +
      (state.draft['f' + i] ? ' checked' : '') + '> ' + esc(f) + '</label>';
  }).join('') + '</div>';
  h += arr(n.biochemical_questions).map(function (q, i) {
    return '<div class="checks"><label class="check"><input type="checkbox" data-act="biochem" data-i="' + i + '"' +
      (state.draft['b' + i] ? ' checked' : '') + '> ' + esc(q.question) +
      ' <span class="opt__meta">(required: ' + esc(q.required_answer) + ')</span></label></div>';
  }).join('');
  /* The diversion criteria sit in the same control as the constellation they
     override, because the clerk reads them together and one of them beats all
     the others: ANY of these ticked sends the case to tissue whatever the
     imaging shows. They are rendered last so the override is the last thing
     read before Continue. */
  if (arr(n.diversion_criteria).length) {
    h += '<div class="tag">Features that require tissue whatever the imaging shows</div>';
    h += arr(n.diversion_criteria).map(function (d, i) {
      return '<div class="checks"><label class="check"><input type="checkbox" data-act="diversion" data-i="' + i + '"' +
        (state.draft['d' + i] ? ' checked' : '') + '> ' + esc(d.feature) +
        (d.reason ? ' <span class="opt__meta">' + rich(d.reason) + '</span>' : '') + '</label></div>';
    }).join('');
  }
  h += '<div class="actions"><button class="btn" data-act="resolve">Continue</button></div>';
  return h;
}

/* Two escapes on EVERY node, visually and semantically distinct. They must
   never be collapsed into one control: forcing an NOS *malignant* code on the
   second would record a cancer that does not exist (nodes.md §4). */
function renderEscapes(n) {
  /* The laboratory screen asks no diagnostic question, so it offers no way to end the case on one. */
  if (n && n.node_type === 'lab_results') return '';
  var nos = n.nos_fallback;
  return '<div class="escapes">' +
    (nos ? '<button class="escape escape--nos" data-act="escape-nos">Uncertain subtype — still a malignancy' +
      '<small>Falls back to ' + esc(nos.name) + ', flagged as discordant.</small></button>' : '') +
    '<button class="escape escape--excluded" data-act="escape-excluded">Malignancy excluded / benign / revised' +
    '<small>Clean terminal. Emits no morphology code and leaves the malignant registry.</small></button>' +
    '</div>';
}

/* ---------------------------------------------------------- §3.1 behaviour
   The behaviour of the code — and with it whether the case belongs to this
   ICCC-3 group at all — can turn on a clinical fact the pathology report
   cannot supply. The engine stops and asks the criterion rather than guessing,
   and every answer is an ordinary branch destination that goes straight back
   through advance(). Nothing here knows what any behaviour means. */
function behaviourLeaves(br) {
  var out = [];
  Object.keys((br && br.values) || {}).forEach(function (k) {
    var leaf = br.values[k];
    out.push({ key: k, leaf: leaf,
      label: leaf.label || ANSWER_LABELS[String(leaf.when).toLowerCase()] || String(leaf.when) });
  });
  /* `unresolved` is required of the author and named the reportable half.
     Defaulting an unestablished behaviour to the other half would silently
     delete a reportable cancer, so it is offered as an explicit answer the
     clerk chooses — the engine never takes it on its own. */
  if (br && br.unresolved) {
    out.push({ key: 'unresolved', leaf: br.unresolved,
      label: br.unresolved.label || 'Not established from the file' });
  }
  return out;
}
function renderBehaviour() {
  var br = state.pending, n = node();
  return panel('Behavior', br.criterion,
    br.clinical_only
      ? 'A clinical-history question. The pathology report cannot answer it — ask the notes or the clinician.'
      : null,
    priorNote(br.prior_probability) +
    pick('behaviour', behaviourLeaves(br).map(function (l) {
      return { label: l.label, meta: l.leaf.reason || null, alert: l.leaf.clinical_alert || null };
    })) +
    /* Deferrable means the answer arrives months later, so say so here as well
       as on the output block. */
    (br.deferrable ? banner('info', 'The answer may arrive later',
      br.follow_up_review || 'This answer can change after today; the case will be flagged for review.') : '') +
    renderEscapes(n || {}));
}

/* ------------------------------------------------------------- §2.4 grade
   Grade is its own decision, on exactly the model behaviour_resolution
   already set. A molecular finding can set a grade with no histological
   change, and the grade is not derivable from the code — so the engine stops
   and asks the criterion rather than guessing, and every answer goes straight
   back through advance(), where captures, gates, terminals and referrals
   behave as they do on any other branch.

   ONE difference from a behaviour leaf, and it is in the schema, not here: a
   behaviour leaf REPLACES the branch, because the behaviour decides which code
   is emitted. A grade leaf ANNOTATES it — the code is the same either way — so
   a leaf that names no destination resumes the branch that parked. */
function gradeLeafMeta(leaf) {
  var bits = [];
  if (leaf.grade !== undefined && leaf.grade !== null && leaf.grade !== '') {
    bits.push('Grade ' + leaf.grade +
      (leaf.grade_system ? ' · ' + tokenLabel(GRADE_SYSTEM_LABELS, leaf.grade_system) : ''));
  } else if (leaf.defer_to) {
    bits.push('No grade — deferred to ' + String(leaf.defer_to).replace(/_/g, ' '));
  } else {
    bits.push('No grade recorded');
  }
  if (leaf.reason) bits.push(leaf.reason);
  return bits.join(' — ');
}
function gradeLeaves(gr) {
  var out = [];
  Object.keys((gr && gr.values) || {}).forEach(function (k) {
    var leaf = gr.values[k];
    out.push({ key: k, leaf: leaf, unresolved: false,
      label: leaf.label || String(k).replace(/_/g, ' '), meta: gradeLeafMeta(leaf) });
  });
  /* Offered as an explicit answer the clerk CHOOSES, and never taken by the
     engine on its own — exactly as behaviourLeaves() does for behaviour. A
     grade that cannot be established is omitted, never invented, and this is
     the answer that says so. */
  if (gr && gr.unresolved) {
    out.push({ key: 'unresolved', leaf: gr.unresolved, unresolved: true,
      label: gr.unresolved.label || 'Not established from the file',
      meta: gradeLeafMeta(gr.unresolved) });
  }
  return out;
}
function renderGrade() {
  var gr = state.pendingGrade.rule, n = node(), methods = arr(gr.detection_method_required);
  return panel('Grade', gr.criterion,
    methods.length ? 'Answerable from: ' + methods.join(' or ') + '.' : null,
    priorNote(gr.prior_probability) +
    pick('grade', gradeLeaves(gr).map(function (l) {
      return { label: l.label, meta: l.meta || null, alert: l.leaf.clinical_alert || null };
    })) + renderEscapes(n || {}));
}
/* The parked branch, minus the criterion it has now answered, so resuming it
   cannot ask the same question a second time. */
function withoutGradeResolution(t) {
  var out = {};
  Object.keys(t).forEach(function (k) { if (k !== 'grade_resolution') out[k] = t[k]; });
  return out;
}

function banner(kind, label, text) {
  return '<div class="banner banner--' + esc(kind) + '"><span class="banner__label">' +
    esc(label) + '</span>' + rich(text) + '</div>';
}

/* ============================================================================
   Resolution — first matching rule wins. resolution_logic is FLAT: nested
   conditional logic inside a rule is not allowed, because flatness is what
   keeps it validatable and testable (DT master §3C).
   ========================================================================= */
/* Only a TRAILING ":strong" / ":weak" is an intensity suffix; every other
   colon belongs to the marker name. Splitting on the first colon broke every
   token naming a fusion gene — "::" is the current standard separator and is
   used throughout this project — because it looked up the half before the
   colons, found no such marker on the node, and the rule then SILENTLY never
   fired. A rule that never fires is not a visible failure: the case simply
   walks past the branch that was written to catch it and reaches a different
   code, which is a mis-code wearing the face of a normal answer. */
function markerOk(token) {
  var m = /^([\s\S]*):(strong|weak)$/.exec(String(token));
  var name = m ? m[1] : String(token), want = m ? m[2] : null;
  var have = state.markers[name];
  if (!have || have === 'neg' || have === MARKER_UNREAD) return false;
  if (want) return have === want;
  return true;
}
/* A `negative` requirement is met by a marker that is off, never recorded, or
   recorded as unreadable — the three are the same evidence. */
function markerOff(name) {
  var v = state.markers[name];
  return !v || v === 'neg' || v === MARKER_UNREAD;
}
/* A `when` value may name one state or a list of states that behave alike.
   The list form carries ruling 11 into the JSON: a test that could not be
   interpreted routes with one that was never done, instead of falling through
   to a definite call the evidence does not support. */
function whenValueOk(have, want) {
  if (Array.isArray(want)) {
    return want.some(function (w) { return String(have) === String(w); });
  }
  return String(have) === String(want);
}
function whenOk(when) {
  if (!when) return true;
  return Object.keys(when).every(function (k) {
    return whenValueOk(state.captured[k], when[k]);
  });
}
function matchRules(rules) {
  for (var i = 0; i < arr(rules).length; i++) {
    if (ruleSatisfied(rules[i])) return rules[i];
  }
  return null;
}
/* A written range is inclusive of both endpoints AT THE PRECISION IT IS
   WRITTEN: "10-19" covers [10, 20); "0.5-0.99" covers [0.5, 1.00).

   Reading the upper endpoint as a bare <= leaves a hole between one band and
   the next, and a value landing in that hole matches nothing and falls to the
   node's NOS fallback. A gate is the one place that failure is invisible —
   the clerk gets a plausible answer for a value that belongs in the band
   below, with nothing on screen to say a band was missed.

   Bands are still tried in array order and the first match wins. */
function bandStep(text) {
  var dot = String(text).indexOf('.');
  return dot === -1 ? 1 : Math.pow(10, -(String(text).length - dot - 1));
}
function inBand(range, v) {
  if (range === 'not_documented') return v === null;
  if (v === null || v === undefined) return false;
  var m;
  if ((m = /^>=\s*([\d.]+)$/.exec(range))) return v >= +m[1];
  if ((m = /^>\s*([\d.]+)$/.exec(range))) return v > +m[1];
  if ((m = /^<=\s*([\d.]+)$/.exec(range))) return v <= +m[1];
  if ((m = /^<\s*([\d.]+)$/.exec(range))) return v < +m[1];
  if ((m = /^([\d.]+)\s*-\s*([\d.]+)$/.exec(range))) {
    return v >= +m[1] && v < +m[2] + bandStep(m[2]);
  }
  return false;
}

/* ============================================================================
   Transitions
   ========================================================================= */
function capture(map) {
  if (!map) return;
  Object.keys(map).forEach(function (k) { state.captured[k] = map[k]; });
}

/* ======================================================================
   Availability as reachability — `resource_level_gate`

   A test's availability is a property of the LABORATORY AND THE TUMOUR
   FAMILY, not of the site as a whole: one laboratory can be resource level IV
   for one family and II for another, because the antibodies and assays that
   decide one family say nothing about the next. The gate therefore names its
   family, and the engine compares the level the branch requires against the
   level this site has FOR THAT FAMILY.

   Where the site cannot meet it the branch is not askable. It resolves to the
   gate's `unreachable_destination`, and the upgrade line says the test is
   unavailable instead of dangling it as a next step. An upgrade line that
   offers a test the laboratory cannot run reads as a plan; it is a dead end,
   and it makes the case look one step away from better evidence when it is
   not — the one thing an advisory tool must never do, in the one row the
   clerk reads as a worklist.

   The site's own level is read from captured state first (a tree may ask it,
   the router may capture it), then from a `site_profile` block on the router.
   NO NEW FILE IS FETCHED: site_profile.json is undeclared, and its template
   says in terms that it is not read by app.js until it is wired in
   deliberately. That wiring is a deployment decision, not an engine one.
   ====================================================================== */
function siteProfile() { return (state.router && state.router.site_profile) || {}; }
function siteResourceLevel(family) {
  var c = state.captured, p = siteProfile(), levels = p.resource_levels || {};
  var lv = c['resource_level_' + family] || c.resource_level ||
    levels[family] || levels['default'] || p.resource_level || null;
  lv = lv ? String(lv).toUpperCase() : null;
  return lv && RL_SCALE.indexOf(lv) !== -1 ? lv : null;
}
/* THREE states, deliberately: blocked, available, and NEITHER. A site with no
   declared level is not evidence that the test can be done and not evidence
   that it cannot, and collapsing "not recorded" into either one states more
   than the file supports — the same line boundary() holds for an undecidable
   reading. The clerk is told which of the three it is.

   There is NO exception for a requirement at the top of the scale. A site
   declared resource level V MEETS a requirement of resource level V — reaching
   the last rung is not sitting above it — so an undeclared site tells us
   nothing there either, and treating it as unavailable would be exactly the
   inference the paragraph above forbids. It would also build the tool around
   one kind of laboratory: this tool is used by registries anywhere, and a site
   at the top of the scale is as ordinary a case as one at the bottom. Until a
   site profile says otherwise, a resource level V test is NOT ESTABLISHED, not
   unavailable. (Corrected 14 September 2026: the old rule diverted all 14
   resource level V branches in Group 3 to their unreachable destination, which
   dropped the WHO CNS5 diagnosis the clerk had just evidenced and printed "the
   test is unavailable" over the top of it.) */
function gateStatus(g) {
  if (!g) return null;
  var need = RL_SCALE.indexOf(String(g.required_rl || '').toUpperCase());
  if (need === -1) throw new Error('Unknown required_rl: ' + g.required_rl);
  var site = siteResourceLevel(g.family), have = site ? RL_SCALE.indexOf(site) : -1;
  return { rule: g, site: site, known: have !== -1,
    blocked: have !== -1 && need > have };
}
function gateText(st) {
  var g = st.rule, fam = String(g.family || 'unspecified').replace(/_/g, ' ');
  var head = 'Resource level ' + g.required_rl + ' is required for the ' + fam + ' family';
  var body, tail = [];
  if (st.blocked) {
    /* `blocked` now implies `known`: only a DECLARED level below the requirement
       blocks a branch. The unknown case falls through to the third state. */
    body = head + ', and this laboratory is resource level ' + st.site +
      ' for it. The test is **unavailable** here, and is not an upgrade path.';
  } else if (st.known) {
    body = head + ', and this laboratory is resource level ' + st.site + ' for it, so the test can be done here.';
  } else {
    body = head + '. This site has no recorded resource level for that family, so whether the test can be done here is **not established** — confirm it before recording it as a next step.';
  }
  if (g.tier) tail.push('Tier: ' + String(g.tier).replace(/_/g, ' ') + '.');
  if (g.referral_tier) tail.push('If referred out: ' + String(g.referral_tier).replace(/_/g, ' ') + '.');
  /* `by_analogy` means no published tier covers this family. Saying so is the
     entire point of the flag — presenting it as sourced is the failure it
     exists to prevent. */
  if (g.rl_assignment) {
    tail.push('Level assigned ' + String(g.rl_assignment).replace(/_/g, ' ') +
      ', not from a published tier for this family.');
  }
  return [body].concat(tail).join(' ');
}
function gateNote(g) {
  var st = gateStatus(g);
  return st ? banner(st.known && !st.blocked ? 'info' : 'warn', 'Laboratory capability', gateText(st)) : '';
}
/* The branch the clerk cannot take. It carries the gate forward so the output
   block can write the unavailability line, and it deliberately inherits
   NOTHING else from the branch it replaces — above all not `satisfies_tests`,
   which would discharge a requirement using a test that by definition was not
   done, and not `basis_of_diagnosis`, which would claim evidence nobody
   obtained. */
function unreachableTarget(from, st) {
  var d = (st.rule && st.rule.unreachable_destination) || null;
  if (!d) {
    throw new Error('resource_level_gate is blocked but declares no unreachable_destination' +
      (from && from.next_node ? ' (routing to ' + from.next_node + ')' : ''));
  }
  /* The destination is an ORDINARY BRANCH and is honoured in full: whatever
     the author wrote on it — a code, a next_node, a provisional, a rendered
     diagnosis, a basis — applies, because they wrote it about this outcome.
     Nothing is copied from the branch that was blocked. The gate itself is
     attached (overriding any the destination declares, so it cannot re-gate
     itself) and supplies the default reason. */
  var out = {};
  Object.keys(d).forEach(function (k) { out[k] = d[k]; });
  out.reason = d.reason || gateText(st);
  out.resource_level_gate = st.rule;
  return out;
}

/* ======================================================================
   Basis of diagnosis (ENCR) — a REGISTRY DATA ITEM

   ENCR says a registry may register a case on imaging; it does not say the
   tool may then call that answer firm. This is the registry's record of
   what the diagnosis rests on — a fact about the evidence path, not a claim
   about how sure the tool is of its own answer.

   Computed, never authored on the output: the highest code 1-8 that any
   branch on the path asserted, with 0 and 9 overriding — 0 before 9, because
   "death certificate only" is a positive statement about the record and
   "unknown" is the absence of one. CODES 3 AND 6 DO NOT EXIST in the scheme;
   one in the data is a defect and is refused here rather than written into a
   registry field.
   ====================================================================== */
var BASIS_CODES = [0, 1, 2, 4, 5, 7, 8, 9];
var BASIS_LABELS = {
  0: 'Death certificate only', 1: 'Clinical \u2014 physical examination only',
  2: 'Clinical investigation without tissue', 4: 'Specific tumour markers',
  5: 'Cytology', 7: 'Histology', 8: 'Cytogenetic or molecular', 9: 'Unknown'
};
/* The ICD-O behaviour digit, named. Vocabulary of the classification, not clinical
   content. The behaviour-exclusion panel read "Benign" for every exclusion until
   2 October 2026, which mislabelled the /1 ones — 8975/1 calcifying nested
   stromal-epithelial tumour, 8960/1 mesoblastic nephroma, 9514/1 regressed
   retinoblastoma — as benign when ICD-O-3.2 calls them uncertain. Behaviour 0
   reads "Benign neoplasm (benign tumour)" since 3 October 2026, the registrar's
   wording: ICD-O behaviour 0 is a benign neoplasm. */
var BEHAVIOUR_LABELS = {
  '0': 'Benign neoplasm (benign tumour)', '1': 'Uncertain whether benign or malignant', '2': 'In situ',
  '3': 'Malignant', '6': 'Metastatic', '9': 'Malignant, uncertain whether primary or metastatic'
};
/* The same digit as the coding block prints it: "/3 (Malignant)". The registrar
   asked on 6 October 2026 for the code and its meaning in brackets everywhere
   behaviour is reported, and for the interface word to be "Behavior code", the
   ICD-O spelling. The meaning here is short because it sits inside brackets;
   BEHAVIOUR_LABELS keeps the registrar's longer wording for the panel heading. */
var BEHAVIOR_MEANING = {
  '0': 'Benign neoplasm', '1': 'Uncertain whether benign or malignant', '2': 'In situ',
  '3': 'Malignant', '6': 'Metastatic', '9': 'Malignant, uncertain whether primary or metastatic'
};
function behaviorCodeText(b) {
  var d = String(b);
  return '/' + d + (BEHAVIOR_MEANING[d] ? ' (' + BEHAVIOR_MEANING[d] + ')' : '');
}
/* A topography as the registry writes it: the ICD-O code without its letter and
   point, then the ICD-O name, "569 (Ovary)" for C56.9. */
function topographyText(code) {
  if (!code) return '—';
  /* A group may record a range with an instruction ("C70.0-C72.9 - record the
     exact code documented") where no one site is known. That is text, not a code,
     so it prints as the file wrote it. */
  if (!/^C\d{2}(\.\d)?$/i.test(String(code))) return String(code);
  var look = (state.topography && state.topography.topography_lookup) || {};
  var t = look[code] || {};
  var num = String(code).replace(/^C/i, '').replace('.', '');
  var name = t.label || t.region_label;
  return num + (name ? ' (' + name + ')' : '');
}
/* A schema variable, or any token, said as words. The ICD-O spelling is
   "behavior", so a variable named for behaviour reads that way on the trail. */
function words(v) {
  return String(v).replace(/_/g, ' ').replace(/ehaviour/g, 'ehavior');
}
function basisCode(v) {
  var n = Number(v);
  if (v === '' || v === null || v === undefined || isNaN(n) || BASIS_CODES.indexOf(n) === -1) {
    throw new Error('Invalid basis of diagnosis: ' + v + '. Valid codes are ' +
      BASIS_CODES.join(', ') + ' \u2014 3 and 6 do not exist.');
  }
  return n;
}
function assertBasis(v) {
  if (v === undefined || v === null) return;
  if (!Array.isArray(v) && typeof v === 'object') {
    if (v.code === undefined) throw new Error('basis_of_diagnosis object carries no code');
    v = v.code;
  }
  (Array.isArray(v) ? v : [v]).forEach(function (c) {
    var n = basisCode(c);
    if (state.basisCodes.indexOf(n) === -1) state.basisCodes.push(n);
  });
}
/* The two gaps ENCR leaves, DECLARED in the file rather than inferred here:
   which code immunohistochemistry counts as, and which one methylation counts
   as. The engine asserts a declared default only where the evidence for it is
   actually on this case — a stain that was READ (node-TYPE knowledge, which
   the engine may hold), or a test the evidence gate recorded by name. A
   default that fired on a test the case merely REQUIRES would put a basis in
   the registry that nobody performed. */
function basisDefaults() {
  var meta = (state.dt && state.dt.metadata) || {};
  var tree = trees().filter(function (t) { return t.tree_id === state.treeId; })[0] || {};
  var out = {};
  [meta.basis_of_diagnosis_defaults, tree.basis_of_diagnosis_defaults].forEach(function (src) {
    Object.keys(src || {}).forEach(function (k) { out[k] = src[k]; });
  });
  return out;
}
/* A stain was actually read on this case. `nd` is "not done or not readable",
   which is precisely not a stain that was read. */
function ihcRead() {
  return Object.keys(state.markers).some(function (m) {
    return state.markers[m] && state.markers[m] !== MARKER_UNREAD;
  });
}
function evidenceMentions(kind) {
  if (state.captured[kind] === true) return true;
  var needle = String(kind).toLowerCase().replace(/_/g, ' ');
  return arr(state.captured.evidence_tests).some(function (t) {
    return String(t).toLowerCase().indexOf(needle) !== -1;
  });
}
function declaredBasis() {
  var d = basisDefaults(), out = [];
  Object.keys(d).forEach(function (k) {
    var m = /^(.+)_counts_as$/.exec(k);
    if (!m) return;
    if (m[1] === 'ihc' ? ihcRead() : evidenceMentions(m[1])) out.push(basisCode(d[k]));
  });
  return out;
}
/* Nothing asserted means NO ROW. Defaulting to 9 would write a registry value
   onto the panel that no branch ever claimed, and would grow a row on every
   group that does not use this field at all. */
function basisOfDiagnosis() {
  var codes = state.basisCodes.concat(declaredBasis());
  if (!codes.length) return null;
  if (codes.indexOf(0) !== -1) return 0;
  if (codes.indexOf(9) !== -1) return 9;
  return codes.reduce(function (hi, c) { return c > hi ? c : hi; }, codes[0]);
}

/* Every branch ends here: another node, or a terminal. Captures are applied
   HERE rather than at each call site, so a `captures` block works identically
   on an option, an ihc_checklist rule, a numeric_gate band, an override, or a
   molecular rule. They were previously applied only for options and the
   cytogenetics dropdown, so a capture declared on a marker rule was silently
   dropped — the JSON looked right and the variable never arrived, which is
   the worst shape a bug can take here. Applied before finish() so the output
   block sees them. */
function advance(target, label, value, before, automatic) {
  /* THE GATE RUNS FIRST, before the trail entry and before captures. A branch
     whose test this laboratory cannot run is not a branch the clerk can be
     asked to take, so it resolves to the gate's `unreachable_destination`
     instead — and so does a branch routing INTO a node that is gated shut,
     which is the same fact one hop later. Running it here rather than after
     the captures means the unreachable branch's own captures never land: they
     describe a finding the test would have produced, and the test was not
     done. The trail says the branch was not takeable, so an automatic
     diversion is never silent. Bounded, because a chain of gated destinations
     is a data defect, not a loop to follow. */
  var st = gateStatus(target.resource_level_gate), diverted = false, hop = 0, dest, dst;
  if (st && st.blocked) { target = unreachableTarget(target, st); diverted = true; }
  while (target.next_node && hop++ < 8) {
    dest = findNode(target.next_node);
    dst = dest && gateStatus(dest.resource_level_gate);
    if (!dst || !dst.blocked) break;
    target = unreachableTarget(target, dst);
    diverted = true;
  }
  pushTrail(label, value + (diverted ? ' — unavailable at this laboratory' : ''), before, automatic);
  /* Leaving the node leaves its tick gate: a node reached again opens on its checklist. */
  delete state.captured.tick_gate;
  capture(target.captures);
  state.draft = {};
  state.pending = null;
  state.pendingGrade = null;
  /* Code-neutral by definition: it never changes the code. Persisted here
     rather than read off the terminal, so an entity named halfway down the
     tree still reaches the output block instead of being lost at the next hop
     — the same rule `genotype_annotation` already earns its keep by. */
  if (target.entity_annotation) state.entity = target.entity_annotation;
  assertBasis(target.basis_of_diagnosis);
  /* GRADE BEFORE BEHAVIOUR. Both park here; a behaviour leaf REPLACES the
     branch it answers for, so asking behaviour first would throw away a grade
     criterion authored on the same branch. A grade leaf annotates instead, so
     the parked branch resumes to its own destination where the leaf names
     none. */
  if (target.grade_resolution) {
    state.pendingGrade = { rule: target.grade_resolution, target: target };
    state.stage = 'grade';
    return;
  }
  /* A branch may not be able to name its behaviour yet (§3.1). It parks here
     and the engine asks the criterion; each answer comes back through this
     same function, so captures, terminals, referrals and exclusions all
     behave exactly as they do on any other branch. Routing new branch kinds
     around advance() is how captures got silently dropped once already. */
  if (target.behaviour_resolution) {
    state.pending = target.behaviour_resolution;
    state.stage = 'behaviour';
    return;
  }
  /* A TERMINAL's alert travels on the target itself — finish()/refer()/
     exclude() each read it from the branch that actually fired, so nothing has
     to be remembered. Only an onward-routing branch needs the carry below. */
  state.firedAlert = null;
  if (target.morphology_code) return finish(target, label);
  if (target.refer_group) return refer(target);
  if (target.non_reportable) return exclude(target.reason || 'Not a reportable malignancy', target.clinical_alert,
    target.non_reportable_heading);
  /* Group 4 build contract §3, ruling D1: a real ICD-O-3.2 entity whose
     BEHAVIOUR sits outside this group's own declaration — a ganglioneuroma
     is 9490/0, and ICCC-3 Group IV admits behaviour 3 only. Checked before
     next_node for the same reason morphology_code and refer_group are: it is
     a destination in its own right, not a step toward one. */
  if (target.behaviour_exclusion) return excludeBehaviour(target.behaviour_exclusion);
  if (target.next_node) {
    if (!findNode(target.next_node)) throw new Error('Unresolved next_node: ' + target.next_node);
    state.firedAlert = target.clinical_alert || null;
    state.nodeId = target.next_node;
    state.stage = 'node';
    return;
  }
  throw new Error('Branch resolves to neither a code nor a next_node');
}

/* "Based on" is the evidence chain since the case entered the group — the
   clerk has to be able to justify the code at the output block. */
function basisFromTrail() {
  return state.trail.slice(state.trailAtGroupEntry || 0).filter(function (t) { return !t.quiet; })
    .map(function (t) { return t.value; }).join(' · ');
}

function finish(target, basis) {
  var code = String(target.morphology_code);
  /* Resolved by (code, behaviour): a behaviour-overloaded code has one entry
     per behaviour, and an entry lookup that ignored the behaviour would put
     the other entity's name on the output block. */
  var entry = entryFor(code, target.behavior_code);
  if (!entry) throw new Error('Terminal code not in morphology_entries: ' + code +
    (target.behavior_code ? '/' + target.behavior_code : ''));
  var pending = target.provisional_pending || null;
  /* `diagnostic_tests_required` has no OR semantics — an entry that names both
     "Cytogenetics/FISH" and "Molecular/PCR" means "either will do", but the
     list cannot say so. A branch therefore declares `satisfies_tests[]`: the
     requirements the finding it just captured actually discharges. Without
     this the tool reports an outstanding test on a fully-subtyped case, which
     both invents an upgrade path and feeds a false pending-worklist entry.
     The engine holds no opinion on which test substitutes for which — that
     judgement stays in the JSON. */
  /* A branch cannot hold the same test both outstanding and discharged. Where
     a provisional names the test that would resolve it, that test is struck
     from what this branch claims to satisfy (§3.2). This can only ever move a
     test from "done" to "outstanding" — never the reverse. */
  var evidence = arr(state.captured.evidence_tests).concat(
    arr(target.satisfies_tests).filter(function (t) {
      return !pending || String(t) !== String(pending.resolving_test);
    }));
  var missing = arr(entry.diagnostic_tests_required).filter(function (t) { return evidence.indexOf(t) === -1; });
  /* A NAMED PROVISIONAL IS A DECLARATION THAT A SPECIFIC TEST IS OUTSTANDING,
     whether or not the entry's required-test list happens to name it. Without
     this, a code whose required tests are all present renders "Workup:
     complete — no outstanding tests" directly above a Provisional row saying
     the resolving test has not been done and two other entities are not
     excluded. That is the one thing an advisory tool must never do, and it is
     worse here than an ordinary missing test because the panel positively
     asserts completeness.

     This is not the provisional being merged into the workup list — the
     named row stays exactly as authored, alongside. The test simply joins
     the workup list under its own name, with its own status dropdown.
     Nothing here is silent: the clerk sees the test, the reason and the
     alternatives. */
  if (pending && pending.resolving_test && missing.indexOf(pending.resolving_test) === -1) {
    missing = missing.concat([pending.resolving_test]);
  }
  /* `outstanding_tests[]` is the reverse of `satisfies_tests[]`: the tests a
     branch's own finding leaves owed, whatever the entry requires. A code's
     required-test list is fixed per code, so without this a branch that
     reaches a code on a partial panel — INI1 retained, SMARCA4 never done —
     renders "Complete — no outstanding tests" above an upgrade line naming
     the test that was skipped. Added for Group 7, 3 October 2026, on the
     registrar's decision; group-agnostic, and it can only add a row. */
  arr(target.outstanding_tests).forEach(function (t) {
    if (missing.indexOf(t) === -1) missing = missing.concat([t]);
  });
  state.workup = missing.map(function (t) {
    var prior = state.workup.filter(function (w) { return w.test === t; })[0];
    return { test: t, status: prior ? prior.status : WORKUP_STATES[0] };
  });
  var discordant = !!target.discordant;
  /* THE UPGRADE LINE MUST NOT DANGLE A TEST THIS LABORATORY CANNOT RUN. The
     sentence the engine writes itself — "X would yield a more specific code"
     — is exactly that dangle, so a blocked gate replaces it with the reason
     the test is unavailable. Anything the author wrote stays either way, and
     where the gate is satisfied its line is appended so the clerk can see the
     branch was askable here. */
  var gate = gateStatus(target.resource_level_gate);
  var authored = target.upgrade_path || entry.upgrade_path || '';
  var auto = missing.length ? missing.join(', ') + ' would yield a more specific code.' : '';
  var upgrade = (gate && gate.blocked)
    ? [gateText(gate), authored].filter(Boolean).join(' ')
    : [authored || auto, gate ? gateText(gate) : ''].filter(Boolean).join(' ');
  state.result = {
    code: code, entry: entry, basis: basisFromTrail() || basis,
    discordant: discordant,
    upgrade: upgrade,
    /* The two-track output: the code and the diagnosis the report states are
       separate outputs, and both are recorded (§2.1). The entity annotation is
       the third, and changes no code (§2.3). */
    diagnosis: target.diagnosis_rendering || null,
    entity: target.entity_annotation || state.entity || null,
    gradeDecision: state.grade || null,
    /* A registry data item, computed from what the path asserted: what the
       diagnosis rests on, not a claim about how sure the tool is of its own
       answer (§2.5). */
    basisOfDiagnosis: basisOfDiagnosis(),
    gate: gate,
    classification_system: target.classification_system || state.captured.classification_system_applied || null,
    /* A NAMED, REVERSIBLE provisional with its own resolving test (§3.2).
       Collapsing "this specific test is outstanding, these specific entities
       are not excluded" into a single summary word would throw away
       everything actionable about it. It renders on complete cases too; it
       is never suppressed. */
    provisional: pending,
    /* The branch's own sentence for why THIS code rather than its neighbour —
       an entity boundary's reason_inside/reason_outside, or a behaviour leaf's
       reason. `reason`, never `coding_note`: coding_note is author-facing and
       is not rendered anywhere (registrar's ruling, Aug 2026). */
    reason: target.reason || null,
    /* The warning written on the branch that reached this code. Rendered in
       the same treatment as the entry-level alert, and only once where both
       carry the same string (several branches repeat their entry's alert). */
    alert: target.clinical_alert || null,
    followUp: state.captured.follow_up_review || null,
    routing: resolveGroup(code, state.captured.topography)
  };
  state.stage = 'output';
}

/* ------------------------------------------------------ the referral hop
   A referral to a BUILT group does not end the case: the clerk continues in
   that group's tree (registrar, 6 October 2026). The referral itself
   establishes the group, so the topography's candidate_groups are not
   consulted again; the receiving group routes its own tree from the topography
   or asks for one, exactly as it does for any case.

   What carries over is the case: where the tumour is, what is in the file, and
   the basis of diagnosis already asserted. What does not is what the old tree
   READ: stain results, workup, grade, entity, parked branches. The new tree
   interprets those afresh, and a stain read under one tree's panel must not be
   taken as answered under another's. */
function caseFacts() {
  var keep = ['topography', 'organ_system', 'tumour_origin'];
  var router = state.router || {};
  Object.keys(router.discriminators || {}).forEach(function (k) {
    if (router.discriminators[k].variable) keep.push(router.discriminators[k].variable);
  });
  Object.keys(router.tick_vocabularies || {}).forEach(function (k) {
    if (router.tick_vocabularies[k].variable) keep.push(router.tick_vocabularies[k].variable);
  });
  var out = {};
  keep.forEach(function (k) { if (state.captured[k] !== undefined) out[k] = state.captured[k]; });
  return out;
}
function canHop(r) {
  if (!(r && r.referral && r.group !== undefined && r.group !== null && groupMeta(r.group).built)) return false;
  /* A group that routes its trees from the topography cannot take a case that
     has none: it would enter that group's default tree in silence. The referral
     screen stays as it was, and the case is started again from its site. */
  return !(groupMeta(r.group).tree_routing && !state.captured.topography);
}
function hopAction(r) {
  if (!canHop(r)) return '';
  var name = groupMeta(r.group).name;
  return '<div class="actions"><button class="btn" data-act="hop">Continue in Group ' + esc(r.group) +
    (name ? ' — ' + esc(name) : '') + '</button></div>';
}
function hopToGroup(before) {
  var r = state.result;
  if (!canHop(r)) { state.error = 'This referral names no built group to continue in.'; return; }
  var target = r.group;
  pushTrail('Referral', 'Group ' + target + (groupMeta(target).name ? ' — ' + groupMeta(target).name : ''), before);
  state.captured = caseFacts();
  state.markers = {}; state.workup = []; state.pending = null; state.pendingGrade = null;
  state.grade = null; state.entity = null; state.firedAlert = null; state.draft = {};
  state.result = null; state.treeId = null; state.nodeId = null; state.searchTerm = null;
  state.group = target; state.candidates = [target];
  /* "Suggested based on" keeps the evidence that led to the hop: the new
     group's entry point is the old one. */
  state.hopFrom = state.trailAtGroupEntry;
  return afterGroup();
}

/* A terminal for a case that IS a malignancy but belongs to a DIFFERENT ICCC-3
   group. Distinct from both escape hatches: the case is neither an uncertain
   subtype of this group nor a non-malignancy. Emitting a code from this
   group's file would be wrong, and marking it non-reportable would drop a real
   cancer from the registry — so it emits no code here and names where the case
   belongs. The engine holds no view on which case goes where; the branch
   declares it. */
function refer(target) {
  state.workup = []; state.pending = null;
  state.result = {
    referral: true,
    alert: target.clinical_alert || null,
    group: target.refer_group,
    codeHint: target.refer_code || null,
    note: target.reason || null
  };
  state.stage = 'output';
}

/* A clean terminal that emits NO malignant code. Marked "not a reportable
   malignancy" and removed from the malignant registry (nodes.md §4). */
/* `non_reportable_heading` lets a branch name what the lesion IS — "Benign
   neoplasm (benign tumour)" — where the generic heading would lump a
   haemangioma with an abscess. Text only; the outcome is the same. Added for
   Group 7, 3 October 2026, on the registrar's wording. */
function exclude(reason, alert, heading) {
  state.workup = []; state.pending = null;
  state.result = { excluded: true, reason: reason, alert: alert || null, heading: heading || null };
  state.stage = 'output';
}

/* A terminal for a real ICD-O-3.2 entity whose BEHAVIOUR falls outside this
   group's own declaration (Group 4 build contract §3, ruling D1). Distinct
   from both exclude() and refer(): this case is not a non-malignancy — a
   ganglioneuroma is a genuine, named, benign entity, and the tumour it sits
   beside on the same four-digit stem (ganglioneuroblastoma, 9490/3) is a
   real Group IV cancer. And it is not a cross-group referral either — ICCC-3
   registers no group at all for a benign neurogenic tumour, so there is
   nowhere to refer it TO. No morphology_code is ever emitted here (the
   validator enforces that the two never coexist on one branch); the panel
   instead names the code the tumour actually sits at, the behaviour it
   carries, and what this group declares, and defers the case to the
   registrar. `basis_of_diagnosis` still applies — the case had histology —
   so it is carried through exactly as it is for any other terminal. */
function excludeBehaviour(be) {
  state.workup = []; state.pending = null;
  state.result = {
    behaviourExcluded: true,
    icdoCode: be.icdo_code,
    icdoBehaviour: be.icdo_behaviour,
    icdoTerm: be.icdo_term,
    groupDeclares: be.group_declares,
    reason: be.reason || null,
    registrarDecisionRequired: !!be.registrar_decision_required,
    basisOfDiagnosis: basisOfDiagnosis()
  };
  state.stage = 'output';
}

/* ============================================================================
   Output block — rows in REDCap field order so the clerk reads down both
   panels in lockstep (redcap.md §2).
   ========================================================================= */
/* §2.1, §2.3, §2.4 — the two-track output, the entity, and the grade.

   THE CODE AND THE DIAGNOSIS ARE SEPARATE OUTPUTS. Where the code cannot name
   what the report says, the code is still the code and the diagnosis is still
   recorded; a panel carrying only one of them is wrong in whichever direction
   it drops. The entity annotation is the third row of the same idea: a named
   entity that shares its code with others, or has no code at all, is recorded
   WITHOUT ever changing the code. */
function renderDiagnosisRows(r) {
  var d = r.diagnosis, g = r.gradeDecision, h = '';
  if (d) {
    var meta = [tokenLabel(TRACK_LABELS, d.track),
      (d.suffix && String(d.suffix) !== 'none') ? String(d.suffix).toUpperCase() : ''
    ].filter(Boolean).join(' · ');
    h += orow('Diagnosis', (d.who_diagnosis || d.descriptive_diagnosis || '') +
      (meta ? ' (' + meta + ')' : ''));
  }
  h += renderGradeRow(d, g);
  if (d && d.comment) h += orow('Diagnosis comment', d.comment, true);
  if (r.entity) h += orow('WHO CNS5 entity', entityText(r.entity), true);
  return h;
}
/* A NULL GRADE IS OMITTED — never "NA", never "". Where the criterion recorded
   why it could not be established, that sentence is the row: a grade that was
   asked for and not answered is a different fact from a grade nobody looked
   for, and both are different from a grade the tool made up. */
function renderGradeRow(d, g) {
  var live = function (v) { return v !== null && v !== undefined && v !== '' ? v : null; };
  var value = (g && live(g.grade)) || (d && live(d.grade)) || null;
  /* THE NUMERAL SYSTEM FOLLOWS THE TRACK, NEVER THE EVIDENCE TYPE: a grade
     reached on histology alone is still Arabic where the diagnosis is a CNS5
     diagnosis, so the track's system wins wherever one is declared. */
  var sys = (d && d.grade_system) || (g && g.grade_system) || null;
  if (value !== null) {
    return orow('Grade', String(value) +
      (sys ? ' (' + tokenLabel(GRADE_SYSTEM_LABELS, sys) + ')' : ''));
  }
  if (!g) return '';
  var why = [];
  if (g.reason) why.push(g.reason);
  if (g.defer_to) why.push('Deferred to ' + String(g.defer_to).replace(/_/g, ' ') + '.');
  if (!why.length) why.push(g.unresolved ? 'Not established from the file.' : 'No grade recorded.');
  return orow('Grade', 'Not established. ' + why.join(' '), true);
}
/* `(provisional type)` is an extraction artefact of the source's italics and
   must never sit inside an entity name. The flag is rendered as its own
   sentence instead, which is what the flag is for. */
/* `status` says how firmly the entity is CLAIMED; `code_status` says whether it
   has a code. They are different questions. A suggested entity rendered like an
   established one is the failure mode this field exists to stop: an MYCN IHC with
   no published sensitivity would otherwise print beside a code and read as a
   settled WHO CNS5 diagnosis. The qualifier leads, so it cannot be missed if the
   row is truncated, and the JSON must also carry a provisional_pending naming the
   test that would settle it (the build enforces both). */
function entityText(a) {
  var suggested = a.status === 'suggested';
  var bits = [];
  if (suggested) bits.push('**Suggested, not established** \u2014');
  bits.push(a.who_cns5_entity || '');
  if (a.provisional) bits.push('Provisional type.');
  if (a.code_status) bits.push(tokenLabel(CODE_STATUS_LABELS, a.code_status) + '.');
  if (arr(a.shared_with).length) bits.push('Shared with: ' + arr(a.shared_with).join('; ') + '.');
  if (a.evidence) bits.push((suggested ? 'Rests on: ' : 'Evidence: ') + a.evidence + '.');
  return bits.filter(Boolean).join(' ');
}

/* The four coding fields and the evidence behind them, in one block, for every
   terminal that finds a code (registrar, 6 October 2026): Name, Morphology
   code, Behavior code, Topography code, Suggested based on. The behaviour is
   printed whatever it is: a benign tumour's code is still its code. */
function codingBlock(name, code, behavior, basis) {
  var shown = behavior === undefined || behavior === null || behavior === '' ? '\u2014' : behaviorCodeText(behavior);
  return '<div class="codeblock">' +
    orow('Name', name || '\u2014') +
    '<div class="orow orow--code"><b>Morphology code</b><span>' + esc(code) + '</span></div>' +
    orow('Behavior code', shown) +
    orow('Topography code', topographyText(state.captured.topography)) +
    orow('Suggested based on', basis || '\u2014') + '</div>';
}
/* The behaviours a group admits, said as codes: "3", "0-1,3" or "0, 1 and 3". */
function behaviorListText(spec) {
  var out = [];
  String(spec).split(/[,\s]+(?:and\s+)?/).forEach(function (tok) {
    var m = /^(\d)-(\d)$/.exec(tok);
    if (m) { for (var d = +m[1]; d <= +m[2]; d++) out.push(String(d)); }
    else if (/^\d$/.test(tok)) out.push(tok);
  });
  return out.length ? out.map(behaviorCodeText).join(', ') : String(spec);
}

function renderOutput() {
  var r = state.result;
  if (r.referral) {
    var gname = ((state.router.groups || {})[String(r.group)] || {}).name;
    return '<div class="node--live">' +
      banner('warn', 'Belongs to another group',
        'This case is a malignancy, but not one this group codes. Record it under group ' +
        r.group + (gname ? ' — ' + gname : '') + '.') +
      '<div class="orow"><b>Code here</b><span>None. Emitting a code from this group would put the case in the wrong ICCC-3 group.</span></div>' +
      (r.codeHint ? orow('Code there', r.codeHint) : '') +
      (r.note ? orow('Why', r.note) : '') +
      orow('Topography code', topographyText(state.captured.topography)) +
      orow('Suggested based on', basisFromTrail() || '—') +
      labResultsBlock() + hopAction(r) + outActions() + '</div>';
  }
  if (r.excluded) {
    return '<div class="node--live">' +
      banner('info', r.heading || 'Not a reportable malignancy', r.reason) +
      '<div class="orow orow--excluded"><b>Morphology</b><span>No code emitted. This case leaves the malignant registry.</span></div>' +
      orow('Topography code', topographyText(state.captured.topography)) +
      labResultsBlock() + outActions() + '</div>';
  }
  /* Group 4 build contract §3, ruling D1. Neither the referral panel above
     nor the exclusion panel below fits: this case is a real ICD-O-3.2
     entity — not a non-malignancy — and ICCC-3 registers no group it could
     be referred TO, because Group IV's own behaviour declaration is the
     thing excluding it. The panel says which code and behaviour the tumour
     actually sits at, what this group declares instead, and (§3, §6 rule 1)
     always carries a registrar flag alongside the clerk-facing reason. */
  if (r.behaviourExcluded) {
    return '<div class="node--live">' +
      banner('info', (BEHAVIOUR_LABELS[String(r.icdoBehaviour)] || 'Behavior code ' + r.icdoBehaviour) +
        ' \u2014 outside this group\u2019s declared behavior', r.reason) +
      codingBlock(r.icdoTerm, r.icdoCode, r.icdoBehaviour, basisFromTrail()) +
      orow('Group admits', 'Behavior code ' + behaviorListText(r.groupDeclares) + ' only') +
      (r.registrarDecisionRequired
        ? banner('warn', 'Registrar decision required',
            'This code and behavior need the registrar\u2019s ruling before the case can be closed.')
        : '') +
      (r.basisOfDiagnosis !== null && r.basisOfDiagnosis !== undefined
        ? orow('Basis of diagnosis', r.basisOfDiagnosis + ' \u2014 ' + (BASIS_LABELS[r.basisOfDiagnosis] || 'Unknown'))
        : '') +
      labResultsBlock() + outActions() + '</div>';
  }
  var e = r.entry, redcap = state.host === 'redcap';
  var h = '<div class="node--live">';

  /* Rows run in REDCap FIELD ORDER — morphology → subgroup → workup — so the
     clerk reads down this panel and down the REDCap form in lockstep
     (redcap.md §2). Everything advisory follows underneath. */
  if (redcap) {
    /* The headline is the FULL option string, verbatim — not the bare code.
       Matching a whole string is self-checking; matching four digits is not,
       and it fails loudly when the tool and the options file drift apart. */
    h += '<div class="pickbox"><div class="pickbox__head">Select this option in REDCap</div>' +
      '<div class="pickbox__value">' + esc(e.redcap_value) + '&nbsp;&nbsp;' + esc(e.morphology_name) + '</div></div>';
  }
  /* No REDCap banner. The tool does not verify REDCap (standing rule 16,
     registrar, 4 October 2026): it does not connect to it, and a banner about
     what the dropdown holds costs the clerk attention without changing the
     code. Codes REDCap cannot record, and labels it holds out of date, are
     listed for the REDCap side in docs/TODO.md §7. */
  h += codingBlock(e.morphology_name, r.code, e.behavior_code, r.basis);

  /* The subgroup is RESOLVED, not read off the entry: one (code, behaviour)
     pair can belong to two ICCC-3 subgroups depending on the topography, and
     the entry's own is only the default (§2.7). */
  var sub = subgroupFor(e, state.captured.topography);
  h += '<div class="out__head">' +
    '<span class="out__subgroup">' + esc(sub.name) + ' — ICCC-3 <b>' + esc(sub.id) + '</b></span></div>';

  /* The second track. It sits next to the code it accompanies, because for
     much of a group like this there is no code for the diagnosis the
     pathologist actually reached, and a panel that shows only the code would
     report the case as less specific than the report is. */
  h += renderDiagnosisRows(r);

  /* A specific claim with a specific resolving test (§3.2). Rendered whether
     or not the case is otherwise complete. */
  if (r.provisional) {
    var pv = r.provisional, alts = arr(pv.alternative_entities), altc = arr(pv.alternative_codes);
    h += orow('Provisional', String(pv.reason || '') +
      (pv.resolving_test ? ' **Resolved by:** ' + pv.resolving_test + '.' : '') +
      (alts.length ? ' **Not excluded:** ' + alts.join('; ') + '.' : '') +
      (altc.length ? ' **Alternative codes:** ' + altc.join(', ') + '.' : ''), true, 'provisional');
  }

  h += '<div class="orow"><b>Workup</b><span>' + renderWorkup() + '</span></div>';
  /* A registry data item in its own right, next to the workup it is derived
     from: what the diagnosis RESTS ON is not a claim about how sure the tool
     is of its own answer (§2.5). */
  if (r.basisOfDiagnosis !== null && r.basisOfDiagnosis !== undefined) {
    h += orow('Basis of diagnosis', r.basisOfDiagnosis + ' — ' +
      (BASIS_LABELS[r.basisOfDiagnosis] || 'Unknown'));
  }
  /* A deferrable behaviour criterion is answered months later. The case has to
     be re-opened, and a flag nobody can see will not make that happen — so it
     is an explicit row, next to the outstanding tests it behaves like. */
  if (r.followUp) h += orow('Follow-up', r.followUp, true, 'followup');
  /* Renders even when empty. If it vanishes on complete cases the clerk stops
     trusting it as a checklist (Design Spec §5, redcap.md §4). */
  /* rich(), not esc(): an unavailable test is the one upgrade line that must
     not be skim-read as a next step, and the word carrying that is emphasised.
     rich() escapes first, so the input is already inert HTML. */
  h += '<div class="orow orow--upgrade"><b>Upgrade</b><span>' +
    rich(r.upgrade || 'None — fully subtyped at this evidence tier.') + '</span></div>';
  h += renderAliases(r.code);
  h += renderUnread();
  if (redcap) h += orow('REDCap value', e.redcap_value);
  if (r.reason) h += orow('Why', r.reason, true);
  if (r.discordant) h += orow('Discordance', 'Subtype uncertain — recorded as a quality signal.');
  if (r.classification_system) h += orow('Classification', r.classification_system);
  if (e.who_version) h += orow('WHO version', e.who_version);
  if (arr(state.captured.qualifiers).length) {
    h += '<div class="orow"><b>Qualifiers</b><span class="qualifiers">' +
      state.captured.qualifiers.map(function (q) { return '<span class="qualifier">' + esc(q) + '</span>'; }).join('') +
      '</span></div>';
  }
  /* Always persisted, even where the finding is code-neutral — otherwise an
     uncoded entity loses its genotype permanently (Pathway §7.3 item 7). */
  if (state.captured.genotype_annotation) h += orow('Genotype', state.captured.genotype_annotation);
  if (r.routing && r.routing.note) h += orow('Group routing', r.routing.note);
  h += labResultsBlock();
  h += outActions();
  return h + '</div>';
}
/* Ruling 6, 4 Sep 2026: whatever path the clerk took, the answer names the
   code's aliases. The abstractor is matching what a report actually says
   against what REDCap calls it, and the alias file already holds both. Alias
   plus every `also_known_as` on it, de-duplicated, in file order. */
function aliasesFor(code) {
  var seen = {}, out = [];
  arr(state.aliases).forEach(function (a) {
    if (arr(a.maps_to_morphology_codes).indexOf(String(code)) === -1) return;
    [a.alias].concat(arr(a.also_known_as)).forEach(function (t) {
      if (t && !seen[t.toLowerCase()]) { seen[t.toLowerCase()] = true; out.push(t); }
    });
  });
  return out;
}
function renderAliases(code) {
  var list = aliasesFor(code);
  if (!list.length) {
    return '<div class="orow"><b>Also called</b><span>No alias recorded for this code.</span></div>';
  }
  return '<div class="orow"><b>Also called</b><span class="aliases">' +
    list.map(function (t) { return '<span class="qualifier">' + esc(t) + '</span>'; }).join('') +
    '</span></div>';
}

/* Ruling 11: a stain the clerk marked not done or not readable is named on the
   answer. The case still resolves to the nearest code the evidence supports —
   it is not a dead end — but the reader can see what was missing. */
function renderUnread() {
  var out = Object.keys(state.markers).filter(function (m) {
    return state.markers[m] === MARKER_UNREAD;
  });
  if (!out.length) return '';
  return '<div class="orow"><b>Not read</b><span>' + esc(out.join(' · ')) + '</span></div>';
}

/* `emphasise` runs the value through rich() so an authored **bold** lands on
   the word that carries the warning; `mod` names an optional .orow--<mod>
   variant, which degrades to the plain row if the stylesheet has none. */
function orow(label, value, emphasise, mod) {
  return '<div class="orow' + (mod ? ' orow--' + esc(mod) : '') + '"><b>' + esc(label) +
    '</b><span>' + (emphasise ? rich(value) : esc(value)) + '</span></div>';
}
/* Per MISSING TEST, not per case. */
function renderWorkup() {
  if (!state.workup.length) return 'Complete — no outstanding tests.';
  return '<span class="workup">' + state.workup.map(function (w, i) {
    return '<span class="workup__row"><span class="workup__test">' + esc(w.test) + '</span>' +
      '<select data-act="workup" data-i="' + i + '" aria-label="Workup status for ' + esc(w.test) + '">' +
      WORKUP_STATES.map(function (s) {
        return '<option value="' + esc(s) + '"' + (w.status === s ? ' selected' : '') + '>' + esc(s) + '</option>';
      }).join('') + '</select></span>';
  }).join('') + '</span>';
}
/* DOES THIS TERMINAL CARRY A CODE? Asked of the RESOLVED OUTCOME, never of a
   flag on the branch. `state.result.code` is set in exactly one place —
   finish(), from the branch's own morphology_code, and only after entryFor()
   has proved the code is real. The other three terminal builders never set it:
   refer() builds {referral, group, codeHint}, exclude() builds {excluded,
   reason}, excludeBehaviour() builds {behaviourExcluded, icdoCode} — and
   icdoCode is deliberately a DIFFERENT key, because the code a benign tumour
   sits at is not a code this group emitted.

   So `code` is the one value that distinguishes the terminals that emitted a
   morphology code from the terminals that emitted none, and it is the same
   value the headline renders and the same value an override would replace.
   Adding a fourth no-code terminal kind in a later group needs nothing here:
   if it does not run through finish(), it carries no code, and it is covered.

   Do NOT reintroduce a test on `referral`/`excluded`/`behaviourExcluded`. That
   is a list somebody has to remember to extend, and the first kind left off it
   gets the affordance back. */
function resultCarriesCode(r) {
  return !!(r && r.code);
}

/* Override sits VISIBLY beside the primary action, never hidden — but ONLY on a
   terminal that actually emitted a code. On a terminal that emitted none it was
   worse than useless: the handler validates the typed code with entryFor(),
   which accepts only codes from THIS group, so the single thing the button
   could do on a cross-group referral ("Emitting a code from this group would
   put the case in the wrong ICCC-3 group") was force the case into this group —
   the exact error the terminal exists to prevent. Observed in a browser on the
   Group XI referral out of hn_ihc_checklist and on the 9490/0 ganglioneuroma
   behaviour_exclusion, 18 Sep 2026. */
function outActions() {
  var acts = '<button class="btn" data-act="restart">Start new case</button>';
  if (resultCarriesCode(state.result)) {
    acts += '<button class="btn btn--ghost" data-act="override">Override this code</button>';
  }
  return '<div class="out__actions">' + acts + '</div>';
}

/* ============================================================================
   Interaction — one delegated listener, actions declared in the markup
   ========================================================================= */
function handleOption(act, el) {
  /* A group's file is loading (a referral hop, a tree entered): the screen on
     show is the one being left, and a second tap on it would act on a case
     already on its way elsewhere. */
  if (state.stage === 'boot' && !state.error) return;
  var n = node(), before = snapshot(), i = +el.getAttribute('data-i');
  /* Anything but Home itself dismisses the "leave this case?" question. */
  if (act !== 'home') state.confirmExit = false;
  switch (act) {
    case 'home':
      if (!state.trail.length && !state.result) return reset();
      state.confirmExit = true;
      /* The safe answer takes the keyboard focus, and Escape gives it. */
      state.focusNext = '[data-act="home-no"]';
      return;
    case 'home-yes': return reset();
    case 'home-no': state.focusNext = '#appbar-home'; return;
    /* The text in a filter box. Held on the draft so a re-render of this
       screen keeps it; the rows are hidden by applyFilter() as it is typed. */
    case 'filter':
      state.draft['f:' + el.getAttribute('data-key')] = el.value;
      return;
    /* A step back through the trail can return to the landing screen from an
       express-lane case, and the snapshot it restores carries that case's
       search term and group. The guided route starts without them, or its
       site step would become the express lane's. */
    case 'guided':
      state.searchTerm = null; state.group = null; state.candidates = [];
      state.stage = 'archetype'; break;
    case 'query': state.query = el.value; break;
    case 'alias': {
      var hit = searchAlias(state.query)[i];
      pushTrail('Search', hit.alias, before);
      state.searchTerm = hit.alias;
      state.candidates = hit.groups.slice();
      state.group = null;
      /* The express lane bypasses the clinical scaffold and enters at the
         evidence gate — but a multi-tree group still needs its tree picked.
         A term the index files under more than one group is never settled by
         the index's order: the lowest-numbered group is not evidence, and its
         tree may capture a site the case does not have. The primary site
         settles it instead (afterSearchSite), and the clerk is not asked for
         a group (registrar, 4 October 2026). */
      if (hit.groups.length > 1) { state.stage = 'site'; return; }
      /* A term filed under ONE group is still asked its site when that
         group's data reads the site: a tree routed from the topography, or a
         rule keyed on it. Entered without one, every such rule fails open —
         a renal rhabdoid tumour searched by a Group IX-only spelling coded in
         Group IX because the kidney referral could never match (registrar,
         4 October 2026). afterSearchSite() then keeps the group only if the
         site carries it, and stops for the registrar if it does not. */
      var only = hit.groups[0];
      if (!groupMeta(only).built) { state.group = only; return afterGroup(); }
      return loadGroupData(only).then(function () {
        if (groupReadsSite(only)) { state.stage = 'site'; return; }
        state.group = only;
        return afterGroup();
      });
    }
    case 'archetype': {
      var a = state.router.archetypes[i];
      state.archetype = a;
      pushTrail('Presentation', a.label, before);
      return afterArchetype();
    }
    case 'site': {
      var row = systemRows()[i];
      state.organSystem = row;
      state.captured.organ_system = row.organ;
      pushTrail('Organ system', systemLabel(row), before);
      return afterSystem();
    }
    case 'site_region': {
      var reg = regionOptions(state.organSystem)[i];
      state.captured.topography = reg.topography;
      pushTrail('Topography', reg.topography + ' — ' + reg.label, before);
      return afterSite();
    }
    case 'discriminator': {
      var d = discriminator(), o = d.options[i];
      var val = typeof o === 'string' ? o : o.value;
      state.captured[d.variable] = val;
      pushTrail(d.variable.replace(/_/g, ' '), String(val).replace(/_/g, ' '), before);
      if (d.ask_before_site) return afterDiscriminator();
      narrowByDiscriminator();
      return afterSite();
    }
    case 'group': {
      state.group = arr(state.candidates)[i];
      var gmeta = (state.router.groups || {})[String(state.group)] || {};
      pushTrail('Group', gmeta.name || ('Group ' + state.group), before);
      return afterGroup();
    }
    case 'handoff': {
      var sel = ((state.router.groups || {})[String(state.group)] || {}).tree_selection;
      var ho = sel.options[i];
      state.captured[sel.variable] = ho.value;
      pushTrail('Tree', ho.label, before);
      return enterGroup(state.group, ho.tree_id, ho.entry_node);
    }
    case 'opt': {
      var o2 = arr(n.options)[i];
      return advance(o2, n.step_label || 'Answer', optionLabel(o2), before);
    }
    /* A list whose options carry recognition aids is answered in two taps: the
       first selects (bold, aid shown), Confirm advances. */
    case 'optsel': state.draft.sel = i; return;
    case 'optconfirm': {
      var o3 = arr(n.options)[state.draft.sel];
      if (!o3) return;
      return advance(o3, n.step_label || 'Answer', optionLabel(o3), before);
    }
    /* One box on a tick list. It changes the draft and nothing else. */
    case 'tick': {
      var tk = tickList(n), mine = ticksNow(tk).slice(), id = el.getAttribute('data-id'), at = mine.indexOf(id);
      if (el.checked && at === -1) mine.push(id);
      else if (!el.checked && at !== -1) mine.splice(at, 1);
      state.draft.ticks = mine;
      return;
    }
    case 'tick-continue': return tickContinue(n, before);
    /* The laboratory screen. A typed number or a unit changes the draft only;
       ticking "Not in the file" clears the number. */
    case 'labval': case 'labunit': case 'lababsent': {
      var lab = arr(n.labs)[i], dd = labDraft();
      if (!lab) return;
      var row = dd[lab.id] = Object.assign({}, dd[lab.id] || {});
      delete row.error;
      if (act === 'labval') { row.value = el.value; row.absent = false; }
      else if (act === 'labunit') row.unit = el.value;
      else { row.absent = !!el.checked; if (el.checked) row.value = ''; }
      state.draft.labs = dd;
      return;
    }
    case 'labs-continue': return labsContinue(n, before);
    case 'tickopt': {
      var pick2 = tickOffered(n, arr(state.captured[tickList(n).variable]))[i];
      if (!pick2) return;
      return advance(pick2.o, n.step_label || 'Answer', optionLabel(pick2.o), before);
    }
    /* A referral to a built group continues into that group's tree. */
    case 'hop': return hopToGroup(before);
    case 'direct': return advance(n, n.step_label || 'Answer', n.accept_label || n.question, before);
    /* One declared result state, captured as a first-class answer (§3.4). It
       does NOT advance: the node still resolves through its own options or its
       own rules, and the state is simply one more fact those rules can read.
       No trail entry either — like a marker chip, it is part of composing this
       node's answer, and the trail records the answer. The engine attaches no
       meaning to any state; keeping `not_assessable` off the `negative` branch
       is the JSON's job, and the validator's. */
    case 'state': {
      var blocks = stateBlocks(n), sb = blocks[+(el.getAttribute('data-b') || 0)];
      if (!sb) return;
      var st = arr(sb.states)[i];
      if (st === undefined) return;
      state.captured[sb.variable] = st;
      return;
    }
    case 'behaviour': {
      var br = state.pending, leaf = behaviourLeaves(br)[i];
      if (!leaf) return;
      /* `unresolved` records that the fact was not established — not a value
         the criterion never offered. */
      state.captured[br.variable] = leaf.key === 'unresolved' ? null : leaf.leaf.when;
      /* RATIFIED, 2026-09-04: recorded on EVERY leaf, not only `unresolved`. A
         case coded today on a criterion that can still change in six months
         needs the review just as much as an unanswered one; hiding the row on
         the resolved leaves would be the quieter and the wronger choice. */
      if (br.deferrable && br.follow_up_review) state.captured.follow_up_review = br.follow_up_review;
      return advance(leaf.leaf, words(br.variable), leaf.label, before);
    }
    /* One answer to the grade criterion. The criterion's own variable is
       captured as an ordinary fact so a later rule can read it, and the grade
       itself is held on the case until the output block. */
    case 'grade': {
      var pg = state.pendingGrade, gl = gradeLeaves(pg.rule)[i], grr = pg.rule;
      if (!gl) return;
      /* `unresolved` records that the fact was NOT established. It is not a
         value the criterion ever offered, so it is captured as null. */
      state.captured[grr.variable] = gl.unresolved ? null
        : (gl.leaf.when !== undefined ? gl.leaf.when : gl.key);
      state.grade = {
        criterion: grr.criterion,
        /* UNRESOLVED NEVER INVENTS A GRADE — not even one authored on it. A
           grade that cannot be established is omitted, which is exactly what
           an untested criterion requires; printing one would be the tool
           stating a finding nobody made. */
        grade: (gl.unresolved || gl.leaf.grade === undefined || gl.leaf.grade === '')
          ? null : gl.leaf.grade,
        grade_system: gl.unresolved ? null : (gl.leaf.grade_system || null),
        reason: gl.leaf.reason || null,
        defer_to: gl.leaf.defer_to || null,
        unresolved: !!gl.unresolved
      };
      /* A leaf that names its own destination is an ordinary branch and takes
         over; one that names none hands the parked branch back its own. */
      var named = gl.leaf.morphology_code || gl.leaf.next_node ||
        gl.leaf.refer_group || gl.leaf.non_reportable;
      return advance(named ? gl.leaf : withoutGradeResolution(pg.target),
        String(grr.variable).replace(/_/g, ' '), gl.label, before);
    }
    /* One answer to one marker in the flow chart. Like a marker chip it
       CAPTURES and re-renders without advancing: the node still resolves
       through its own rules. `clear` unanswers, which is how the clerk goes
       back one question without rewinding the whole node. */
    case 'markerset': {
      var mk = el.getAttribute('data-m'), mv = el.getAttribute('data-v');
      if (mv === 'clear') delete state.markers[mk]; else state.markers[mk] = mv;
      return;
    }
    case 'marker': {
      var m = el.getAttribute('data-m'), cur = state.markers[m];
      var next = MARKER_CYCLE[(MARKER_CYCLE.indexOf(cur) + 1) % MARKER_CYCLE.length];
      if (next === undefined) delete state.markers[m]; else state.markers[m] = next;
      return;
    }
    case 'draft': {
      var k = el.getAttribute('data-k');
      state.draft[k] = el.type === 'checkbox' ? el.checked : el.value;
      return;
    }
    case 'feature': state.draft['f' + i] = el.checked; return;
    case 'diversion': state.draft['d' + i] = el.checked; return;
    case 'biochem': state.draft['b' + i] = el.checked; return;
    case 'workup': state.workup[i].status = el.value; return;
    case 'resolve': return resolveNode(n, before);
    case 'escape-nos': {
      var f = n.nos_fallback;
      return advance({ morphology_code: f.code, discordant: true, upgrade_path: f.reason },
        n.step_label || 'Answer', 'Uncertain subtype — ' + f.name, before);
    }
    case 'escape-excluded':
      pushTrail(n ? (n.step_label || 'Answer') : 'Case', 'Malignancy excluded', before);
      return exclude('The abstractor recorded that this case is not a reportable malignancy.');
    case 'override': {
      /* THE SAME GATE, INDEPENDENTLY OF WHAT RENDERED. outActions() no longer
         offers this button on a code-less terminal, but the handler must refuse
         the action on its own: a delegated listener acts on whatever markup
         carries data-act, so a renderer regression, a stale panel or a hand-
         dispatched action must not be able to turn a referral or a behaviour
         exclusion into a code from this group. Refused BEFORE the prompt, so
         the clerk is never asked for a code that would be discarded. */
      if (!resultCarriesCode(state.result)) {
        state.error = 'This terminal emits no morphology code, so there is no code to ' +
          'override. Overriding here would emit a code from this group — which is the ' +
          'one thing this terminal exists to prevent.';
        return;
      }
      var code = window.prompt('Enter the morphology code you judge correct:');
      if (!code) return;
      var reason = window.prompt('Reason for the override (recorded as a quality signal):') || 'No reason given';
      if (!entryFor(code)) { state.error = 'Override code not in this group: ' + code; return; }
      pushTrail('Override', code + ' — ' + reason, before);
      return finish({ morphology_code: code, upgrade_path: 'Abstractor override: ' + reason }, 'Abstractor override');
    }
    case 'rewind': {
      var j = i;
      while (j > 0 && state.trail[j].automatic) j--;
      var ticked = state.trail[j].ticks, typedLabs = state.trail[j].labDraft;
      restore(state.trail[j].before, j);
      if (ticked) state.draft.ticks = ticked.slice();
      if (typedLabs) state.draft.labs = JSON.parse(JSON.stringify(typedLabs));
      return;
    }
    case 'restart': return reset();
    case 'retry': state.error = null; return boot();
    default: throw new Error('Unknown action: ' + act);
  }
}

/* Node types that take a scalar reading capture it BEFORE any node-level rule
   runs, so a rule naming the node's own variable sees this case's value. Node-
   TYPE knowledge, which the engine is allowed to hold; group knowledge, which
   it is not, stays in the JSON. */
function captureLive(n) {
  if (n.node_type !== 'numeric_gate') return;
  var undoc = state.draft.not_documented === true;
  state.captured[n.variable] =
    (undoc || state.draft.value === '' || state.draft.value === undefined) ? null : Number(state.draft.value);
}

/* §3.5. Crossing the line does not flip a behaviour, it moves the case to a
   DIFFERENT CODE, so each side names its own (code, behaviour) pair and its
   own clerk-facing reason. `operator`/`threshold` describe the OUTSIDE
   condition; `also_outside_when` is a second, independent way out, so a match
   there settles the case even when the reading is missing.

   Returns null when neither test can be decided. Reading an undocumented value
   as "inside" would hand back the narrower entity's code on no evidence at
   all, which is the one failure this tool must never produce — the caller
   sends that case to the node's fallback instead.

   ⚠ RATIFIED, 2026-09-04. This is not an oversight waiting to be tidied into a
   default. Do not "improve" it by treating a missing reading as inside, as
   outside, or as any fixed side: an undecidable boundary is a case the file
   cannot answer, and it must arrive at the clerk saying so. */
function boundary(n) {
  var b = n.entity_boundary, have = state.captured[b.variable];
  var over = numCompare(have, b.operator || '>', b.threshold);
  var also = !!(b.also_outside_when && whenOk(b.also_outside_when));
  if (over === null && !also) return null;
  var out = also || over === true;
  return {
    target: {
      morphology_code: out ? b.outside_code : b.inside_code,
      behavior_code: out ? b.outside_behavior_code : b.inside_behavior_code,
      reason: out ? b.reason_outside : b.reason_inside
    },
    /* `over === null` is exactly "the reading could not be read", so it also
       covers a blank and a non-numeric entry without a second test for each. */
    value: (over === null ? 'reading not documented' : have + tokenLabel(UNIT_LABELS, n.unit)) +
      ' → ' + (out ? 'outside' : 'inside') + ' the entity boundary'
  };
}

function resolveNode(n, before) {
  captureLive(n);
  /* A node-level boundary is the node's resolution: it runs before the node
     type's own branch selection, and routes through advance() like anything
     else so captures, provisionals and terminals are handled once. */
  if (n.entity_boundary) {
    var eb = boundary(n);
    if (!eb) {
      return advance(fallbackTarget(n), n.step_label || 'Boundary',
        String(n.entity_boundary.variable).replace(/_/g, ' ') + ' not documented — boundary undecidable', before);
    }
    return advance(eb.target, n.step_label || 'Boundary', eb.value, before);
  }
  switch (n.node_type) {
    case 'ihc_checklist': {
      var rule = matchRules(n.resolution_logic);
      var summary = Object.keys(state.markers).map(function (m) {
        var v = state.markers[m];
        return m + (v === 'neg' ? '−' : v === 'pos' ? '+' : ' ' + v);
      }).join(', ') || 'no markers recorded';
      if (!rule) return advance(fallbackTarget(n), n.step_label || 'Markers', summary + ' — no rule matched', before);
      return advance(rule, n.step_label || 'Markers', summary, before);
    }
    case 'numeric_gate': {
      var v = state.captured[n.variable];   /* captured by captureLive() above */
      /* Override is checked BEFORE the bands — a declared override outranks
         the threshold (Pathway §7.2). */
      var ov = arr(n.override_when).filter(function (o) {
        return String(state.captured[o.captured_variable]) === String(o.equals);
      })[0];
      var band = ov || arr(n.bands).filter(function (b) { return inBand(b.range, v); })[0];
      if (!band) return advance(fallbackTarget(n), n.step_label || 'Value', 'Not resolvable', before);
      if (band.band_variable) state.captured[band.band_variable] = band.range;
      if (n.band_variable) state.captured[n.band_variable] = band.range;
      if (band.classification_system) state.captured.classification_system_applied = band.classification_system;
      /* The unit travels with the value AND with the threshold it was read
         against, so the trail can never be read back against the wrong
         denominator. A band with no unit keeps the node's own, unchanged. */
      var bu = bandUnitText(band);
      return advance(band, n.step_label || 'Value',
        (v === null ? 'not documented' : v + (bu ? ' ' + bu : tokenLabel(UNIT_LABELS, n.unit))) +
        ' → ' + band.range + (bu ? ' ' + bu : ''), before);
    }
    case 'cytogenetics_dropdown': {
      var o = arr(n.options)[+state.draft.option];
      if (!o) return;
      if (o.classification_system) state.captured.classification_system_applied = o.classification_system;
      return advance(o, n.step_label || 'Genetics', o.label || o.finding, before);
    }
    case 'molecular_freetext': {
      var t = (state.draft.text || '').trim();
      if (t) state.captured.genotype_annotation = t;
      var rule2 = matchRules(n.resolution_logic);
      return advance(rule2 || fallbackTarget(n), n.step_label || 'Molecular', t || 'not recorded', before);
    }
    case 'imaging_pathway': {
      /* ANY DIVERSION FEATURE TICKED FORCES THE TISSUE BRANCH, whatever the
         imaging constellation says — so it is tested BEFORE the constellation
         and there is no path on which a complete constellation outranks it.
         An imaging-only endpoint is the weakest evidence this tool will emit;
         a feature that says "this does not behave like the thing you are
         about to code" has to be able to stop it. */
      var diverted = arr(n.diversion_criteria).filter(function (_, i) { return !!state.draft['d' + i]; });
      if (diverted.length) {
        return advance(fallbackTarget(n), n.step_label || 'Imaging',
          'Tissue required — ' + diverted.map(function (d) { return d.feature; }).join('; '), before);
      }
      var okF = arr(n.imaging_features).every(function (_, i) { return state.draft['f' + i]; });
      var okB = arr(n.biochemical_questions).every(function (q, i) {
        return String(q.required_answer) === 'yes' ? !!state.draft['b' + i] : !state.draft['b' + i];
      });
      if (okF && okB) return advance(n, n.step_label || 'Imaging', 'Constellation confirmed', before);
      return advance(fallbackTarget(n), n.step_label || 'Imaging', 'Constellation incomplete', before);
    }
    default: throw new Error('Node type does not resolve on Continue: ' + n.node_type);
  }
}
/* nos_fallback is non-null for refining nodes and null for entry/gate/
   terminal-NOS nodes — a node-TYPE rule, not a step-number rule
   (DT master §3D). A refining node with no fallback is a data defect. */
function fallbackTarget(n) {
  if (n.insufficient_next_node) return { next_node: n.insufficient_next_node };
  if (n.nos_fallback) {
    /* A behaviour-overloaded fallback has to name which half it means, or
       entryFor() takes whichever entry happens to be written first. */
    return { morphology_code: n.nos_fallback.code, behavior_code: n.nos_fallback.behavior_code,
      upgrade_path: n.nos_fallback.reason };
  }
  throw new Error('Node has no fallback and did not resolve: ' + n.node_id);
}

/* ---------------------------------------------------------------------------
   Moment 1 narrowing (Architecture §6, router._comment)

   Three facts narrow the family, in the order the clerk can answer them:
   the presentation gives an advisory list, the tissue origin drops what it
   excludes, and the topography intersects what is left. Only what survives all
   three is offered, and if one group survives the tool enters it without
   asking. None of this is clinical judgement held in the engine — every fact
   comes from presentation_router.json and topography_codes.json.

   Before 4 Sep 2026 none of it ran. `afterDiscriminator` read the archetype's
   advisory list and went straight to "Which family does this case belong to?",
   which is the question the tool exists to answer.
   ------------------------------------------------------------------------ */
function startCandidates() {
  var cg = state.archetype && state.archetype.candidate_groups;
  state.candidates = arr(cg).slice();
}
/* A discriminator declares, per answer, which groups that answer rules out. */
function narrowByDiscriminator() {
  var d = discriminator();
  if (!d || !d.narrows) return;
  var rule = d.narrows[String(state.captured[d.variable])];
  if (!rule) return;
  var drop = arr(rule.drop);
  var keep = state.candidates.filter(function (g) { return drop.indexOf(g) === -1; });
  if (keep.length) state.candidates = keep;
}
/* The topography carries its own candidate list. Intersect; and if the
   intersection is empty, take the site's list rather than none — an empty
   candidate set is a dead end, and the site is the more specific fact. */
function narrowBySite() {
  var t = (state.topography.topography_lookup || {})[state.captured.topography];
  var site = t && t.candidate_groups;
  if (!site || !Array.isArray(site)) return;
  var keep = state.candidates.filter(function (g) { return site.indexOf(g) !== -1; });
  state.candidates = keep.length ? keep : site.slice();
}

function afterArchetype() {
  startCandidates();
  /* Origin before organ system: the answer decides which systems are worth
     listing first, and asking it after the site would be asking a question the
     site has already answered. */
  var d = discriminator();
  if (d && d.ask_before_site && state.captured[d.variable] === undefined) {
    state.stage = 'discriminator'; return;
  }
  return afterDiscriminator();
}
function afterDiscriminator() {
  narrowByDiscriminator();
  state.stage = 'site';
}
function afterSystem() {
  var codes = arr(state.organSystem && state.organSystem.codes);
  if (codes.length > 1) { state.stage = 'site_region'; return; }
  state.captured.topography = codes[0];
  return afterSite();
}
function afterSite() {
  if (state.searchTerm) return afterSearchSite();
  narrowBySite();
  var d = discriminator();
  if (d && !d.ask_before_site && state.captured[d.variable] === undefined) {
    state.stage = 'discriminator'; return;
  }
  var cands = arr(state.candidates);
  if (cands.length === 1) { state.group = cands[0]; return afterGroup(); }
  if (!cands.length) { state.error = 'No candidate group survives this presentation, origin and site.'; return; }
  state.stage = 'group';
}
/* Does this group's data read the recorded topography? True when the router
   routes its trees from the topography, or when any `when` in its trees names
   `topography`. Structural only: it reads the shape of the JSON, never a code,
   a site or a group number. Needs the group's file loaded. */
function groupReadsSite(g) {
  if (groupMeta(g).tree_routing) return true;
  var found = false;
  (function walk(o) {
    if (found || !o || typeof o !== 'object') return;
    if (Array.isArray(o)) { o.forEach(walk); return; }
    if (o.when && typeof o.when === 'object' && o.when.topography !== undefined) { found = true; return; }
    Object.keys(o).forEach(function (k) { walk(o[k]); });
  })(trees());
  return found;
}

/* The express lane's site step. The groups the search term is filed under
   are intersected with the groups the topography carries, and only one
   survivor enters a tree — routed, not asked, and recorded in the trail so the
   clerk can see which group the case went to and step back to change the
   site. Registrar, 4 October 2026: no survivor (the term and the site point
   to different groups) and several survivors (the site does not separate
   them) both stop the case for referral; neither asks the clerk for a group.

   Stricter than narrowBySite on purpose. That one takes the site's list when
   the intersection is empty, which here would enter a group whose tree does
   not hold the searched term. The term's groups are re-read from the index
   rather than from `candidates`, so a step back through the trail and a new
   site start from the full list. */
function afterSearchSite() {
  var t = (state.topography.topography_lookup || {})[state.captured.topography];
  var site = t && t.candidate_groups;
  var term = arr((state.aliasIndex || {})[state.searchTerm]);
  state.candidates = Array.isArray(site)
    ? term.filter(function (g) { return site.indexOf(g) !== -1; })
    : term.slice();
  /* `group` is cleared because a step back to a Tree entry restores the group
     the case was routed to, and a stop must not name it. */
  if (state.candidates.length !== 1) { state.group = null; state.stage = 'search_unresolved'; return; }
  var before = snapshot();
  state.group = state.candidates[0];
  pushTrail('Group', groupMeta(state.group).name || ('Group ' + state.group), before, true);
  return afterGroup();
}
/* A group whose trees are keyed to a fact the router has ALREADY captured
   does not ask the clerk to pick one. Asking would be redundant, and worse
   than redundant: it invites an answer that contradicts the topography
   already recorded on the case, and then two fields disagree with nothing to
   say which is right.

   The mapping from topography to tree is clinical content and lives in the
   router; this only matches it, through the same ordered-rules matcher the
   subgroup split and the dual-group rules use. `default` is REQUIRED, because
   a topography no rule names would otherwise route nowhere at all — so a
   missing one is refused by name rather than discovered by a clerk. */
function routedTree(meta) {
  var tr = meta.tree_routing;
  if (!tr.default) {
    throw new Error('tree_routing for group ' + state.group + ' declares no default tree. ' +
      'A topography the rules do not name would route nowhere.');
  }
  var topo = state.captured[tr.variable || 'topography'];
  var hit = firstTopographyMatch(tr.rules, topo) || tr.default;
  if (!hit.tree_id) {
    throw new Error('tree_routing for group ' + state.group + ' resolved a rule with no tree_id' +
      ' (topography ' + (topo || 'not captured') + ')');
  }
  return hit;
}
function afterGroup() {
  var meta = (state.router.groups || {})[String(state.group)] || {};
  if (!meta.built) { state.stage = 'handoff'; return; }
  /* Routed, not asked — and RECORDED, as an ordinary trail entry that is
     clickable like every other one. An automatic route is precisely where a
     wrong topography would otherwise mis-route a case in silence, so the
     clerk has to be able to see which tree the case went down and go back and
     change it. */
  if (meta.tree_routing) {
    var before = snapshot();
    var hit = routedTree(meta);
    pushTrail('Tree', hit.label || String(hit.tree_id).replace(/_/g, ' '), before, true);
    return enterGroup(state.group, hit.tree_id, hit.entry_node);
  }
  if (meta.tree_selection) { state.stage = 'handoff'; return; }
  var only = arr(meta.trees)[0];
  if (!only) { state.error = 'Group has no tree declared in the router.'; return; }
  return enterGroup(state.group, only.tree_id, only.entry_node);
}
function enterGroup(group, treeId, entryNode) {
  state.group = group;
  state.stage = 'boot';
  return loadGroupData(group).then(function () {
    var tree = trees().filter(function (t) { return !treeId || t.tree_id === treeId; })[0];
    if (!tree) throw new Error('Tree not in group file: ' + treeId);
    state.treeId = tree.tree_id;
    state.nodeId = entryNode || tree.entry_node;
    if (!findNode(state.nodeId)) throw new Error('Entry node not in file: ' + state.nodeId);
    state.trailAtGroupEntry = state.hopFrom !== null ? state.hopFrom : state.trail.length;
    state.hopFrom = null;
    state.stage = 'node';
  });
}

function reset() {
  state.stage = 'landing'; state.archetype = null; state.group = null;
  state.organSystem = null; state.candidates = []; state.searchTerm = null;
  state.treeId = null; state.nodeId = null; state.captured = {}; state.markers = {};
  state.draft = {}; state.pending = null; state.firedAlert = null;
  state.pendingGrade = null; state.grade = null; state.entity = null; state.basisCodes = [];
  state.trail = []; state.trailAtGroupEntry = 0; state.workup = []; state.result = null;
  state.error = null; state.query = ''; state.confirmExit = false; state.hopFrom = null; state.labs = [];
  state.focusNext = null;
}

/* ============================================================================
   Boot
   ========================================================================= */
/* Two flags, deliberately orthogonal. ?mode= is driven by AVAILABLE WIDTH;
   ?host= by WHO IS READING. They must not be merged: a wide REDCap panel
   wants the rail AND the pick box; a standalone window dragged narrow wants
   the transcript WITHOUT REDCap instructions (engine.md §4). */
function readFlags() {
  var p = new URLSearchParams(window.location.search);
  var mode = p.get('mode');
  state.shell = (mode === 'rail' || mode === 'transcript') ? mode : 'auto';
  state.host = p.get('host') === 'redcap' ? 'redcap' : null;
}

/* Every interaction funnels through here so that exactly ONE render happens
   per action, and it happens AFTER any async transition has settled. An
   earlier version rendered synchronously as well as in the promise, which
   raced: the synchronous render could land last and paint a stale panel. */
function guard(fn) {
  return function () {
    var r;
    try { r = fn.apply(null, arguments); }
    catch (err) { return fail(err); }
    if (r && typeof r.then === 'function') return r.then(render, fail);
    render();
  };
}
function fail(err) {
  state.error = err && err.message ? err.message : String(err);
  render();
}

function boot() {
  state.stage = 'boot';
  render();
  return loadRouter().then(function () {
    state.stage = 'landing';
    render();
  }).catch(function () {
    fail(new Error('Could not load the shared router data. The tool requires network access — check the connection and retry.'));
  });
}

document.addEventListener('DOMContentLoaded', function () {
  readFlags();
  var slot = document.querySelector('.app');
  var run = guard(function (act, el) { return handleOption(act, el); });
  slot.addEventListener('click', function (ev) {
    var el = ev.target.closest('[data-act]');
    if (!el || el.tagName === 'INPUT' || el.tagName === 'SELECT' || el.tagName === 'TEXTAREA') return;
    ev.preventDefault();
    run(el.getAttribute('data-act'), el);
  });
  /* A box the clerk types into — the search box, a number, free text — is
     read on every keystroke and never re-renders the screen. Its 'change'
     fires when focus leaves it, which happens on the mousedown of whatever
     the clerk clicks next; a re-render there replaced that button before the
     mouseup, the browser fired no click, and the first tap on a search result
     or on Continue under a typed answer was lost. Checkboxes and selects keep
     'change': it fires on their own click, and the screen changes with them. */
  function typedInto(el) {
    return el.tagName === 'TEXTAREA' || (el.tagName === 'INPUT' && !/^(checkbox|radio)$/.test(el.type));
  }
  slot.addEventListener('change', function (ev) {
    var el = ev.target.closest('[data-act]');
    if (!el || typedInto(el)) return;
    run(el.getAttribute('data-act'), el);
  });
  slot.addEventListener('input', function (ev) {
    var el = ev.target.closest('[data-act]');
    if (!el || !typedInto(el)) return;
    try { handleOption(el.getAttribute('data-act'), el); } catch (err) { return fail(err); }
    if (el.getAttribute('data-act') === 'query') {
      byId('slot').querySelector('.results').innerHTML = renderSearchResults();
    }
    if (el.getAttribute('data-act') === 'filter') applyFilter(el);
    if (el.getAttribute('data-act') === 'labval') {
      var absentBox = el.closest('.labrow').querySelector('[data-act="lababsent"]');
      if (absentBox && el.value.trim() !== '') absentBox.checked = false;
    }
  });
  /* Escape answers the "Leave this case?" bar with Keep Working. */
  slot.addEventListener('keydown', function (ev) {
    if (ev.key !== 'Escape' || !state.confirmExit) return;
    ev.preventDefault();
    run('home-no', ev.target);
  });
  /* Enter in a filter box takes the first row still showing, so the list can be
     answered without leaving the keyboard. */
  slot.addEventListener('keydown', function (ev) {
    var el = ev.target;
    if (ev.key !== 'Enter' || !el || el.getAttribute('data-act') !== 'filter') return;
    ev.preventDefault();
    /* An empty box has nothing to take: the first option would answer the
       question for a clerk who had only pressed Enter. */
    if (!el.value.trim()) return;
    var box = el.closest('.optbox'), row = null;
    /* A selected row stays on screen whatever was typed; it is not a match. */
    if (box) Array.prototype.some.call(box.querySelectorAll('[data-find]:not([hidden])'), function (r) {
      if (!findMatch(r.getAttribute('data-find'), el.value)) return false;
      row = r; return true;
    });
    var ctl = row && (row.tagName === 'BUTTON' ? row : row.querySelector('input'));
    if (ctl) ctl.click();
  });
  boot();
});
