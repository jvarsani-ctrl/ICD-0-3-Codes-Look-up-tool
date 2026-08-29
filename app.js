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

var MARKER_CYCLE = [undefined, 'pos', 'strong', 'weak', 'neg'];
/* Screen-reader wording for each marker state. The visible chip shows a short
   token; a marker read aloud needs the whole word. */
var MARKER_LABELS = { pos: 'positive', strong: 'strongly positive', weak: 'weakly positive', neg: 'negative' };

/* Cleared per case. No localStorage — the iframe reloads between patients
   (Architecture §4D, §7). */
var state = {
  stage: 'boot',
  shell: 'auto', host: null,
  router: null, topography: null, aliasIndex: null,
  archetype: null, group: null, treeId: null, nodeId: null,
  dt: null, aliases: null,
  captured: {},          /* every resolution_logic[].when variable reads here */
  markers: {},
  draft: {},             /* in-progress input for the live node only */
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
    treeId: state.treeId, nodeId: state.nodeId, captured: state.captured,
    markers: state.markers, workup: state.workup, result: state.result,
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
  if (when.value !== undefined && when.operator) {
    var a = Number(have), b = Number(when.value);
    if (isNaN(a)) return false;
    switch (when.operator) {
      case '>=': return a >= b;  case '>': return a > b;
      case '<=': return a <= b;  case '<': return a < b;
      case '==': return a === b;
    }
  }
  return false;
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
    case 'discriminator': return renderDiscriminator();
    case 'group':     return renderGroupSelect();
    case 'handoff':   return renderHandoff();
    case 'node':      return renderLiveNode();
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
      (it.meta ? '<span class="opt__meta">' + esc(it.meta) + '</span>' : '') +
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

/* Site options come from the shared topography crosswalk, so site is expressed
   in ONE vocabulary that site_capture, site_to_group and the output block all
   consult (Architecture §4C). For an auto-topography archetype this is a
   one-tap confirmation across that organ's codes — a dual-group rule can turn
   on exactly which sub-code was picked, so they are never lumped together. */
function siteOptions() {
  var a = state.archetype, cross = arr(state.topography.coarse_organ_crosswalk);
  var look = state.topography.topography_lookup || {}, codes = [];
  if (a.auto_topography) {
    var stem = String(a.auto_topography).replace(/x$/, '');
    cross.forEach(function (c) {
      arr(c.codes).forEach(function (code) { if (code.indexOf(stem) === 0) codes.push(code); });
    });
  }
  if (codes.length) {
    return codes.map(function (code) {
      return { topography: code, label: (look[code] || {}).label || code };
    });
  }
  return cross.map(function (c) {
    var code = arr(c.codes)[0], t = look[code] || {};
    return {
      topography: code, meta: c.topography_range,
      label: String(c.organ).replace(/_/g, ' ') + (t.label ? ' — ' + t.label : '')
    };
  });
}
function renderSite() {
  return panel('Stage 1 · site', 'Which topography does this case record?',
    state.archetype.site_capture === false
      ? 'Site is fixed for this presentation — one tap confirms which code to record.'
      : 'Capture the organ of origin, not the region. Code the primary, not the biopsy site.',
    pick('site', siteOptions().map(function (o) {
      return { label: o.label, meta: o.topography + (o.meta ? ' · ' + o.meta : '') };
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
  return panel('Stage 1 · disambiguation', d.question, d.settles,
    pick('discriminator', arr(d.options).map(function (o) {
      return { label: String(typeof o === 'string' ? o : o.label).replace(/_/g, ' ') };
    })));
}

/* One question when site leaves more than one candidate group. */
function renderGroupSelect() {
  return panel('Stage 1 · group', 'Which family does this case belong to?', null,
    pick('group', arr(state.archetype.candidate_groups).map(function (g) {
      var m = (state.router.groups || {})[String(g)] || {};
      return { label: m.name || ('Group ' + g), meta: m.built ? 'Available' : 'Not yet available in this build' };
    })));
}

/* The handoff into a group tree. For a multi-tree group the router carries a
   one-tap data-level selector; each option names tree_id + that tree's
   document_inventory entry node (DT master §3B). */
function renderHandoff() {
  var meta = (state.router.groups || {})[String(state.group)] || {};
  if (!meta.built) {
    return banner('info', 'Not yet available', 'This group has no decision tree in this build yet.') +
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
  return panel(n.step_label || ('Step ' + (n.step_number === undefined ? '' : n.step_number)),
    n.question || '', n.hint,
    (n.clinical_alert ? banner('alert', 'Clinical alert', n.clinical_alert) : '') +
    dispatchNode(n) + renderEscapes(n));
}

function dispatchNode(n) {
  switch (n.node_type) {
    case 'clinical_presentation':
    case 'site_capture':
    case 'document_inventory':
    case 'morphology_only':
    case 'histology_subclassification':
    case 'site_resolution':
      return optionList(n);
    case 'cytogenetics_dropdown':  return cytogeneticsSelect(n);
    case 'ihc_checklist':          return markerGrid(n);
    case 'numeric_gate':           return numericGate(n);
    case 'molecular_freetext':     return freeText(n);
    case 'imaging_pathway':        return imagingPathway(n);
    case 'clinical_alias':         return optionList(n);
    default: throw new Error('No renderer for node_type: ' + n.node_type);
  }
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
    return { label: optionLabel(o) };
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
  /* detection_method is why a normal result cannot silently close a branch. */
  if (chosen && chosen.detection_method) {
    h += banner('info', 'Detection method', String(chosen.detection_method).replace(/_/g, ' '));
  }
  h += '<div class="actions"><button class="btn" data-act="resolve"' + (chosen ? '' : ' disabled') + '>Continue</button></div>';
  return h;
}

/* Tap cycles a marker: off → positive → strong → weak → negative. The
   intensity tokens ("MARKER:strong") are backward-compatible with plain
   marker names — a rule that names no intensity matches any positive state. */
function markerGrid(n) {
  var h = arr(n.marker_groups).map(function (g) {
    return '<div class="tag">' + esc(g.group_label) + '</div><div class="markers">' +
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

function banner(kind, label, text) {
  return '<div class="banner banner--' + esc(kind) + '"><span class="banner__label">' +
    esc(label) + '</span>' + rich(text) + '</div>';
}

/* ============================================================================
   Resolution — first matching rule wins. resolution_logic is FLAT: nested
   conditional logic inside a rule is not allowed, because flatness is what
   keeps it validatable and testable (DT master §3C).
   ========================================================================= */
function markerOk(token) {
  var bits = String(token).split(':'), name = bits[0], want = bits[1];
  var have = state.markers[name];
  if (!have || have === 'neg') return false;
  if (want) return have === want;
  return true;
}
function whenOk(when) {
  if (!when) return true;
  return Object.keys(when).every(function (k) {
    return String(state.captured[k]) === String(when[k]);
  });
}
function matchRules(rules) {
  for (var i = 0; i < arr(rules).length; i++) {
    var r = rules[i];
    if (!whenOk(r.when)) continue;
    if (arr(r.positive).length && !arr(r.positive).every(markerOk)) continue;
    if (arr(r.negative).length && !arr(r.negative).every(function (m) {
      var v = state.markers[m]; return !v || v === 'neg';
    })) continue;
    return r;
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
  if (target.morphology_code) return finish(target, label);
  if (target.refer_group) return refer(target);
  if (target.non_reportable) return exclude(target.reason || 'Not a reportable malignancy');
  if (target.next_node) {
    if (!findNode(target.next_node)) throw new Error('Unresolved next_node: ' + target.next_node);
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
  var entry = entryFor(code, target.behavior_code);
  if (!entry) throw new Error('Terminal code not in morphology_entries: ' + code);
  /* `diagnostic_tests_required` has no OR semantics — an entry that names both
     "Cytogenetics/FISH" and "Molecular/PCR" means "either will do", but the
     list cannot say so. A branch therefore declares `satisfies_tests[]`: the
     requirements the finding it just captured actually discharges. Without
     this the tool reports an outstanding test on a fully-subtyped case, which
     both invents an upgrade path and feeds a false pending-worklist entry.
     The engine holds no opinion on which test substitutes for which — that
     judgement stays in the JSON. */
  var evidence = arr(state.captured.evidence_tests).concat(arr(target.satisfies_tests));
  var missing = arr(entry.diagnostic_tests_required).filter(function (t) { return evidence.indexOf(t) === -1; });
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
  state.workup = [];
  state.result = {
    referral: true,
    group: target.refer_group,
    codeHint: target.refer_code || null,
    note: target.reason || null
  };
  state.stage = 'output';
}

/* A clean terminal that emits NO malignant code. Marked "not a reportable
   malignancy" and removed from the malignant registry (nodes.md §4). */
function exclude(reason) {
  state.workup = [];
  state.result = { excluded: true, reason: reason };
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
  if (e.clinical_alert) h += banner('alert', 'Clinical alert', e.clinical_alert);

  /* Rows run in REDCap FIELD ORDER — morphology → subgroup → confidence →
     workup — so the clerk reads down this panel and down the REDCap form in
     lockstep (redcap.md §2). Everything advisory follows underneath. */
  if (redcap) {
    /* The headline is the FULL option string, verbatim — not the bare code.
       Matching a whole string is self-checking; matching four digits is not,
       and it fails loudly when the tool and the options file drift apart. */
    h += '<div class="pickbox"><div class="pickbox__head">Select this option in REDCap</div>' +
      '<div class="pickbox__value">' + esc(e.redcap_value) + '&nbsp;&nbsp;' + esc(e.morphology_name) + '</div></div>';
    if (e.redcap_option_verified === false) {
      h += banner('warn', 'No REDCap option', 'This code has no dropdown option in the registry yet — it cannot be selected until one is added.');
    }
  } else {
    h += '<div class="headline"><div class="headline__code">' + esc(r.code) + '</div>' +
      '<div class="headline__name">' + esc(e.morphology_name) + '</div></div>';
  }

  h += '<div class="out__head out__head--' + esc(r.confidence) + '">' +
    '<span class="out__subgroup">' + esc(e.iccc3_subgroup_name) + ' — ICCC-3 <b>' + esc(e.iccc3_subgroup_id) + '</b></span>' +
    '<span class="badge badge--' + esc(r.confidence) + '">Confidence ' + esc(r.confidence) + '</span></div>';

  h += '<div class="orow"><b>Workup</b><span>' + renderWorkup() + '</span></div>';
  /* Renders even when empty. If it vanishes on complete cases the clerk stops
     trusting it as a checklist (Design Spec §5, redcap.md §4). */
  h += '<div class="orow orow--upgrade"><b>Upgrade</b><span>' +
    esc(r.upgrade || 'None — fully subtyped at this evidence tier.') + '</span></div>';
  h += orow('Topography', state.captured.topography || '—');
  if (redcap) h += orow('REDCap value', e.redcap_value);
  h += orow('Based on', r.basis || '—');
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
function orow(label, value) {
  return '<div class="orow"><b>' + esc(label) + '</b><span>' + esc(value) + '</span></div>';
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
      state.stage = 'site'; break;
    }
    case 'site': {
      var s = siteOptions()[i];
      state.captured.topography = s.topography;
      pushTrail('Topography', s.topography + ' — ' + s.label, before);
      return afterSite();
    }
    case 'discriminator': {
      var d = discriminator(), o = d.options[i];
      var val = typeof o === 'string' ? o : o.value;
      state.captured[d.variable] = val;
      pushTrail(d.variable.replace(/_/g, ' '), String(val).replace(/_/g, ' '), before);
      return afterDiscriminator();
    }
    case 'group': {
      state.group = arr(state.archetype.candidate_groups)[i];
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

function resolveNode(n, before) {
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
      var undoc = state.draft.not_documented === true;
      var v = undoc || state.draft.value === '' || state.draft.value === undefined ? null : Number(state.draft.value);
      state.captured[n.variable] = v;
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
    return { morphology_code: n.nos_fallback.code, upgrade_path: n.nos_fallback.reason, confidence: 'low' };
  }
  throw new Error('Node has no fallback and did not resolve: ' + n.node_id);
}

function afterSite() {
  var d = discriminator();
  if (d && state.captured[d.variable] === undefined) { state.stage = 'discriminator'; return; }
  return afterDiscriminator();
}
function afterDiscriminator() {
  var cands = arr(state.archetype.candidate_groups);
  if (cands.length === 1) { state.group = cands[0]; return afterGroup(); }
  if (!cands.length) { state.error = 'No candidate group for this presentation.'; return; }
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
  state.treeId = null; state.nodeId = null; state.captured = {}; state.markers = {};
  state.draft = {}; state.trail = []; state.trailAtGroupEntry = 0; state.workup = []; state.result = null;
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
