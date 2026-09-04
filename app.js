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
   `numeric_gate` is the ratified continuous-threshold type. */
var NODE_TYPES = [
  'clinical_presentation', 'site_capture', 'document_inventory', 'clinical_alias',
  'morphology_only', 'imaging_pathway', 'ihc_checklist', 'cytogenetics_dropdown',
  'molecular_freetext', 'histology_subclassification', 'site_resolution', 'numeric_gate'
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

/* Cleared per case. No localStorage — the iframe reloads between patients
   (Architecture §4D, §7). */
var state = {
  stage: 'boot',
  shell: 'auto', host: null,
  router: null, topography: null, aliasIndex: null,
  archetype: null, group: null, treeId: null, nodeId: null,
  organSystem: null,     /* the crosswalk row picked at Stage 1, before the region */
  candidates: [],        /* groups still possible — narrowed, never asked for blind */
  dt: null, aliases: null,
  captured: {},          /* every resolution_logic[].when variable reads here */
  markers: {},
  draft: {},             /* in-progress input for the live node only */
  pending: null,         /* a branch parked mid-flight waiting on one answer */
  firedAlert: null,      /* alert of the branch that routed here, one hop only */
  trail: [], trailAtGroupEntry: 0, workup: [], result: null, error: null, query: ''
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
function byId(id) { return document.getElementById(id); }
function arr(v) { return Array.isArray(v) ? v : []; }

function snapshot() {
  return JSON.stringify({
    stage: state.stage, archetype: state.archetype, group: state.group,
    organSystem: state.organSystem, candidates: state.candidates,
    treeId: state.treeId, nodeId: state.nodeId, captured: state.captured,
    markers: state.markers, workup: state.workup, result: state.result,
    pending: state.pending || null, firedAlert: state.firedAlert || null,
    trailAtGroupEntry: state.trailAtGroupEntry
  });
}
function restore(snap, upto) {
  var s = JSON.parse(snap);
  Object.keys(s).forEach(function (k) { state[k] = s[k]; });
  state.trail = state.trail.slice(0, upto);
  state.draft = {};
}
/* `before` is the snapshot taken BEFORE the answer was applied, so clicking a
   trail entry rewinds to the moment that question was asked. Trail entries are
   clickable in BOTH shells — a wrong answer is one tap from correction
   (engine.md §3). */
function pushTrail(label, value, before) {
  state.trail.push({ label: label, value: value, before: before });
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
function render() {
  var app = byId('app');
  app.setAttribute('data-shell', state.shell);
  byId('appbar-context').textContent = contextLabel();
  byId('rail').innerHTML = renderRail();
  byId('trail-rows').innerHTML = renderTrailRows();
  byId('slot').innerHTML = renderStage();
}

function contextLabel() {
  if (state.error) return 'Error';
  if (state.dt && state.dt.metadata) {
    return esc(state.dt.metadata.group_name) + (state.result ? ' · case complete' : '');
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
       '</b><span>… in progress</span></div>';
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
  if (state.pending) return 'Behaviour';
  var n = node();
  if (n) return n.step_label || n.node_type.replace(/_/g, ' ');
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
    case 'handoff':   return renderHandoff();
    case 'node':      return renderLiveNode();
    case 'behaviour': return renderBehaviour();
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
  }));
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
    '<p class="node__q">' + esc(question) + '</p>' +
    (hint ? '<p class="node__hint">' + esc(hint) + '</p>' : '') + body + '</div>';
}
function pick(act, items) {
  return '<div class="opts">' + items.map(function (it, i) {
    return '<button class="opt" data-act="' + esc(act) + '" data-i="' + i + '">' +
      '<span class="opt__label">' + esc(it.label) +
      (it.meta ? '<span class="opt__meta">' + rich(it.meta) + '</span>' : '') +
      /* A CLINICAL ALERT AUTHORED ON A BRANCH IS CLERK-FACING (DT master §3E)
         — the counterpart of coding_note, which is author-facing and stays
         unrendered. On an option it must be visible BEFORE the option is
         taken: "a normal karyotype does not exclude this code" is worthless
         once the clerk has already picked "karyotype normal". Compact, not a
         banner each — several can be on screen at once. */
      (it.alert ? '<span class="opt__alert"><b>Clinical alert</b> ' + rich(it.alert) + '</span>' : '') +
      '</span></button>';
  }).join('') + '</div>';
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
  if (a.auto_topography) {
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
    state.archetype.site_capture === false
      ? 'Site is fixed for this presentation — one tap confirms which system to record.'
      : (origin
          ? 'Systems matching the origin you recorded are listed first. The others are still here — an abdominal mass is soft tissue and may still be renal or hepatic.'
          : 'The organ of origin, not the region of the swelling. Code the primary, not the biopsy site.'),
    pick('site', systemRows().map(function (c) {
      return { label: systemLabel(c), meta: c.topography_range + ' · ' + arr(c.codes).length + ' codes' };
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
        'The presentation, origin and site place this case in Group ' + state.group +
        (meta.name ? ', ' + meta.name : '') + '. No decision tree for that group is in this ' +
        'build yet, so the tool cannot reach a morphology code. Record the topography (' +
        esc(state.captured.topography || 'not captured') + ') and refer the morphology to the registrar.') +
      '<div class="actions"><button class="btn btn--ghost" data-act="restart">Start again</button></div>';
  }
  var sel = meta.tree_selection;
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
  return panel(n.step_label || ('Step ' + (n.step_number === undefined ? '' : n.step_number)),
    n.question || '', n.hint,
    priorNote(n.prior_probability) + dispatchNode(n) + renderEscapes(n));
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
  return pick('opt', opts.map(function (o) {
    return { label: optionLabel(o), meta: priorText(o.prior_probability) || null,
             alert: o.clinical_alert || null };
  }));
}

function cytogeneticsSelect(n) {
  var opts = arr(n.options);
  var h = '<label class="field"><span class="field__label">Reported finding</span><select data-act="draft" data-k="option"><option value="">—</option>';
  opts.forEach(function (o, i) {
    var sel = String(state.draft.option) === String(i) ? ' selected' : '';
    h += '<option value="' + i + '"' + sel + '>' + esc(o.label || o.finding) + '</option>';
  });
  h += '</select></label>';
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
     rule left, or every remaining rule emitting the same outcome. */
  if (live.length <= 1 || outcomeCount(live) <= 1) return null;

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
    h += '<p class="node__hint">' + (outcomeCount(live) <= 1
      ? 'One outcome remains. Continue to record it.'
      : 'No remaining marker separates what is left — continue, and the first rule the '
        + 'answers satisfy decides it.') + '</p>';
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
function numericGate(n) {
  var undoc = state.draft.not_documented === true;
  return '<label class="field"><span class="field__label">' + esc(n.variable_label || n.variable) +
    (n.unit ? ' (' + esc(n.unit) + ')' : '') + '</span>' +
    '<input type="number" step="any" data-act="draft" data-k="value" value="' +
    esc(state.draft.value === undefined ? '' : state.draft.value) + '"' + (undoc ? ' disabled' : '') + '></label>' +
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
  h += '<div class="actions"><button class="btn" data-act="resolve">Continue</button></div>';
  return h;
}

/* Two escapes on EVERY node, visually and semantically distinct. They must
   never be collapsed into one control: forcing an NOS *malignant* code on the
   second would record a cancer that does not exist (nodes.md §4). */
function renderEscapes(n) {
  var nos = n.nos_fallback;
  return '<div class="escapes">' +
    (nos ? '<button class="escape escape--nos" data-act="escape-nos">Uncertain subtype — still a malignancy' +
      '<small>Falls back to ' + esc(nos.name) + ', flagged as discordant, confidence low.</small></button>' : '') +
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
  return panel('Behaviour', br.criterion,
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

/* Every branch ends here: another node, or a terminal. Captures are applied
   HERE rather than at each call site, so a `captures` block works identically
   on an option, an ihc_checklist rule, a numeric_gate band, an override, or a
   molecular rule. They were previously applied only for options and the
   cytogenetics dropdown, so a capture declared on a marker rule was silently
   dropped — the JSON looked right and the variable never arrived, which is
   the worst shape a bug can take here. Applied before finish() so the output
   block sees them. */
function advance(target, label, value, before) {
  pushTrail(label, value, before);
  capture(target.captures);
  state.draft = {};
  state.pending = null;
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
  if (target.non_reportable) return exclude(target.reason || 'Not a reportable malignancy', target.clinical_alert);
  if (target.next_node) {
    if (!findNode(target.next_node)) throw new Error('Unresolved next_node: ' + target.next_node);
    state.firedAlert = target.clinical_alert || null;
    state.nodeId = target.next_node;
    state.stage = 'node';
    return;
  }
  throw new Error('Branch resolves to neither a code nor a next_node');
}

/* confidence_ceiling is the MAXIMUM achievable with all required tests
   present (Design Spec §6) — not the answer. The reported confidence is the
   lowest of the ceiling, whatever the reaching branch declared, and `low`
   whenever the code was reached by a fallback or an escape hatch rather than
   by a rule that actually matched. Reporting the ceiling on a fallback route
   would overstate every incomplete case in the registry. */
var CONFIDENCE_ORDER = ['low', 'medium', 'high'];
function lowestConfidence(list) {
  var best = 'high';
  list.forEach(function (c) {
    if (!c) return;
    if (CONFIDENCE_ORDER.indexOf(c) < CONFIDENCE_ORDER.indexOf(best)) best = c;
  });
  return best;
}
/* "Based on" is the evidence chain since the case entered the group — the
   clerk has to be able to justify the code at the output block. */
function basisFromTrail() {
  return state.trail.slice(state.trailAtGroupEntry || 0).map(function (t) { return t.value; }).join(' · ');
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
     test from "done" to "outstanding" — it can never raise a confidence. */
  var evidence = arr(state.captured.evidence_tests).concat(
    arr(target.satisfies_tests).filter(function (t) {
      return !pending || String(t) !== String(pending.resolving_test);
    }));
  var missing = arr(entry.diagnostic_tests_required).filter(function (t) { return evidence.indexOf(t) === -1; });
  /* A NAMED PROVISIONAL IS A DECLARATION THAT A SPECIFIC TEST IS OUTSTANDING,
     whether or not the entry's required-test list happens to name it. Without
     this, a code whose required tests are all present renders "Workup:
     complete — no outstanding tests" and a HIGH badge directly above a
     Provisional row saying the resolving test has not been done and two other
     entities are not excluded. That is the one thing an advisory tool must
     never do, and it is worse here than an ordinary missing test because the
     panel positively asserts completeness.

     This is NOT the provisional being collapsed into a confidence level — the
     named row stays exactly as authored, alongside. The test simply joins the
     workup list under its own name, with its own status dropdown, and
     confidence falls to `medium` through the SAME rule that already governs
     every outstanding test. Nothing here is silent: the clerk sees the test,
     the reason and the alternatives. */
  if (pending && pending.resolving_test && missing.indexOf(pending.resolving_test) === -1) {
    missing = missing.concat([pending.resolving_test]);
  }
  state.workup = missing.map(function (t) {
    var prior = state.workup.filter(function (w) { return w.test === t; })[0];
    return { test: t, status: prior ? prior.status : WORKUP_STATES[0] };
  });
  var discordant = !!target.discordant;
  /* The ceiling is what is achievable WITH ALL REQUIRED TESTS PRESENT (Design
     Spec §6). While one is still outstanding the case cannot claim it — a
     morphology-only result reporting "high" next to an outstanding flow
     cytometry row tells the clerk the answer is firmer than the evidence
     supports, which is the one thing an advisory tool must never do. */
  state.result = {
    code: code, entry: entry, basis: basisFromTrail() || basis,
    confidence: lowestConfidence([entry.confidence_ceiling, target.confidence,
      missing.length ? 'medium' : null, discordant ? 'low' : null]),
    discordant: discordant,
    upgrade: target.upgrade_path || entry.upgrade_path ||
      (missing.length ? missing.join(', ') + ' would yield a more specific code.' : ''),
    classification_system: target.classification_system || state.captured.classification_system_applied || null,
    /* A NAMED, REVERSIBLE provisional — deliberately NOT a confidence level,
       and deliberately absent from lowestConfidence() above (§3.2). Collapsing
       "this specific test is outstanding, these specific entities are not
       excluded" into the word "low" throws away everything actionable about
       it. It renders on complete cases too; it is never suppressed. */
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
function exclude(reason, alert) {
  state.workup = []; state.pending = null;
  state.result = { excluded: true, reason: reason, alert: alert || null };
  state.stage = 'output';
}

/* ============================================================================
   Output block — rows in REDCap field order so the clerk reads down both
   panels in lockstep (redcap.md §2).
   ========================================================================= */
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
      orow('Topography', state.captured.topography || '—') +
      orow('Based on', basisFromTrail() || '—') +
      outActions() + '</div>';
  }
  if (r.excluded) {
    return '<div class="node--live">' +
      banner('info', 'Not a reportable malignancy', r.reason) +
      '<div class="orow orow--excluded"><b>Morphology</b><span>No code emitted. This case leaves the malignant registry.</span></div>' +
      '<div class="orow"><b>Topography</b><span>' + esc(state.captured.topography || '—') + '</span></div>' +
      outActions() + '</div>';
  }
  var e = r.entry, redcap = state.host === 'redcap';
  var h = '<div class="node--live">';

  /* Rows run in REDCap FIELD ORDER — morphology → subgroup → confidence →
     workup — so the clerk reads down this panel and down the REDCap form in
     lockstep (redcap.md §2). Everything advisory follows underneath. */
  if (redcap) {
    /* The headline is the FULL option string, verbatim — not the bare code.
       Matching a whole string is self-checking; matching four digits is not,
       and it fails loudly when the tool and the options file drift apart. */
    h += '<div class="pickbox"><div class="pickbox__head">Select this option in REDCap</div>' +
      '<div class="pickbox__value">' + esc(e.redcap_value) + '&nbsp;&nbsp;' + esc(e.morphology_name) + '</div></div>';
  } else {
    h += '<div class="headline"><div class="headline__code">' + esc(r.code) + '</div>' +
      '<div class="headline__name">' + esc(e.morphology_name) + '</div></div>';
  }
  /* Ruling 3: the tree is allowed to run ahead of the REDCap option list, but
     never silently. A clerk who cannot find the row has to be told why before
     they go looking, and in BOTH views — the code is just as unselectable
     outside the REDCap host as inside it. */
  if (e.redcap_option_verified === false) {
    var aw = e.awaiting_layer1;
    h += banner('warn', 'Not yet a REDCap option',
      'This code has no option in the registry dropdown, so it cannot be selected yet.' +
      (aw && arr(aw.needs).length ? ' Outstanding: ' + arr(aw.needs).join(' · ') + '.' : '') +
      ' Record the case against the nearest available option and flag it for re-coding.');
  }
  /* Behaviour is shown only where it is not the reportable /3 default: a case
     whose code carries the other behaviour reads as an ordinary malignancy
     otherwise, and under ?host=redcap the option string names the /3 disease. */
  if (e.behavior_code && String(e.behavior_code) !== '3') {
    h += orow('Behaviour', r.code + '/' + e.behavior_code);
  }

  h += '<div class="out__head out__head--' + esc(r.confidence) + '">' +
    '<span class="out__subgroup">' + esc(e.iccc3_subgroup_name) + ' — ICCC-3 <b>' + esc(e.iccc3_subgroup_id) + '</b></span>' +
    '<span class="badge badge--' + esc(r.confidence) + '">Confidence ' + esc(r.confidence) + '</span></div>';

  /* Not a confidence level — a specific claim with a specific resolving test
     (§3.2). Rendered whether or not the case is otherwise complete. */
  if (r.provisional) {
    var pv = r.provisional, alts = arr(pv.alternative_entities), altc = arr(pv.alternative_codes);
    h += orow('Provisional', String(pv.reason || '') +
      (pv.resolving_test ? ' **Resolved by:** ' + pv.resolving_test + '.' : '') +
      (alts.length ? ' **Not excluded:** ' + alts.join('; ') + '.' : '') +
      (altc.length ? ' **Alternative codes:** ' + altc.join(', ') + '.' : ''), true, 'provisional');
  }

  h += '<div class="orow"><b>Workup</b><span>' + renderWorkup() + '</span></div>';
  /* A deferrable behaviour criterion is answered months later. The case has to
     be re-opened, and a flag nobody can see will not make that happen — so it
     is an explicit row, next to the outstanding tests it behaves like. */
  if (r.followUp) h += orow('Follow-up', r.followUp, true, 'followup');
  /* Renders even when empty. If it vanishes on complete cases the clerk stops
     trusting it as a checklist (Design Spec §5, redcap.md §4). */
  h += '<div class="orow orow--upgrade"><b>Upgrade</b><span>' +
    esc(r.upgrade || 'None — fully subtyped at this evidence tier.') + '</span></div>';
  h += renderAliases(r.code);
  h += renderUnread();
  h += orow('Topography', state.captured.topography || '—');
  if (redcap) h += orow('REDCap value', e.redcap_value);
  h += orow('Based on', r.basis || '—');
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
/* Override sits VISIBLY beside the primary action, never hidden. */
function outActions() {
  return '<div class="out__actions"><button class="btn" data-act="restart">Start new case</button>' +
    '<button class="btn btn--ghost" data-act="override">Override this code</button></div>';
}

/* ============================================================================
   Interaction — one delegated listener, actions declared in the markup
   ========================================================================= */
function handleOption(act, el) {
  var n = node(), before = snapshot(), i = +el.getAttribute('data-i');
  switch (act) {
    case 'guided': state.stage = 'archetype'; break;
    case 'query': state.query = el.value; break;
    case 'alias': {
      var hit = searchAlias(state.query)[i];
      pushTrail('Search', hit.alias, before);
      state.group = hit.groups[0];
      /* The express lane bypasses the clinical scaffold and enters at the
         evidence gate — but a multi-tree group still needs its tree picked. */
      return afterGroup();
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
      return advance(leaf.leaf, String(br.variable).replace(/_/g, ' '), leaf.label, before);
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
      var code = window.prompt('Enter the morphology code you judge correct:');
      if (!code) return;
      var reason = window.prompt('Reason for the override (recorded as a quality signal):') || 'No reason given';
      if (!entryFor(code)) { state.error = 'Override code not in this group: ' + code; return; }
      pushTrail('Override', code + ' — ' + reason, before);
      return finish({ morphology_code: code, confidence: 'low', upgrade_path: 'Abstractor override: ' + reason }, 'Abstractor override');
    }
    case 'rewind': return restore(state.trail[i].before, i);
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
    value: (over === null ? 'reading not documented' : have + (n.unit || '')) +
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
      return advance(band, n.step_label || 'Value', (v === null ? 'not documented' : v + (n.unit || '')) + ' → ' + band.range, before);
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
      upgrade_path: n.nos_fallback.reason, confidence: 'low' };
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
function afterGroup() {
  var meta = (state.router.groups || {})[String(state.group)] || {};
  if (!meta.built) { state.stage = 'handoff'; return; }
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
    state.trailAtGroupEntry = state.trail.length;
    state.stage = 'node';
  });
}

function reset() {
  state.stage = 'landing'; state.archetype = null; state.group = null;
  state.organSystem = null; state.candidates = [];
  state.treeId = null; state.nodeId = null; state.captured = {}; state.markers = {};
  state.draft = {}; state.pending = null; state.firedAlert = null;
  state.trail = []; state.trailAtGroupEntry = 0; state.workup = []; state.result = null;
  state.error = null; state.query = '';
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
  slot.addEventListener('change', function (ev) {
    var el = ev.target.closest('[data-act]');
    if (!el) return;
    run(el.getAttribute('data-act'), el);
  });
  slot.addEventListener('input', function (ev) {
    var el = ev.target.closest('[data-act]');
    if (!el || el.getAttribute('data-act') !== 'query') return;
    state.query = el.value;
    byId('slot').querySelector('.results').innerHTML = renderSearchResults();
  });
  boot();
});
