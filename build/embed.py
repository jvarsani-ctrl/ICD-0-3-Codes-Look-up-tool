#!/usr/bin/env python3
"""
embed.py
Reads all data JSON files and produces a single self-contained docs/index.html.
Run AFTER build_database.py.

Usage: python3 build/embed.py
"""

import json, os, re
from pathlib import Path

ROOT     = Path(__file__).parent.parent
DATA_DB  = ROOT / "data" / "database"
DATA_AL  = ROOT / "data" / "aliases"
DATA_TOPO = ROOT / "data" / "topography_codes.json"
DATA_IHC  = ROOT / "data" / "ihc_decision_trees.json"
OUT_HTML  = ROOT / "docs" / "index.html"

def load_all_groups():
    db = []
    for fname in sorted(DATA_DB.glob("group_*.json")):
        db += json.loads(fname.read_text(encoding='utf-8'))
    return db

def load_all_aliases():
    aliases = []
    for fname in sorted(DATA_AL.glob("aliases_group_*.json")):
        data = json.loads(fname.read_text(encoding='utf-8'))
        aliases += data
    return aliases

def main():
    print("Embedding data into docs/index.html...")

    db      = load_all_groups()
    aliases = load_all_aliases()
    topo    = json.loads(DATA_TOPO.read_text(encoding='utf-8'))
    ihc     = json.loads(DATA_IHC.read_text(encoding='utf-8'))

    # Serialize data for embedding
    db_js      = json.dumps(db,      ensure_ascii=False, separators=(',',':'))
    aliases_js = json.dumps(aliases, ensure_ascii=False, separators=(',',':'))
    topo_js    = json.dumps(topo,    ensure_ascii=False, separators=(',',':'))
    ihc_js     = json.dumps(ihc,     ensure_ascii=False, separators=(',',':'))

    html = HTML_TEMPLATE.replace('__DB_DATA__',      db_js)
    html = html.replace('__ALIASES_DATA__',  aliases_js)
    html = html.replace('__TOPO_DATA__',     topo_js)
    html = html.replace('__IHC_DATA__',      ihc_js)

    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(html, encoding='utf-8')
    size_kb = OUT_HTML.stat().st_size // 1024
    print(f"  → docs/index.html  ({size_kb} KB)  {len(db)} entries + {len(aliases)} aliases")
    print("✅ Done")


# ── HTML Template ──────────────────────────────────────────────────────────────
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ICCC-3 Lookup Tool — UCI Cancer Registry</title>
<style>
  /* ── Reset & Base ── */
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 14px;
    background: #f0f4f8;
    color: #1a202c;
    min-height: 100vh;
  }

  /* ── Header ── */
  .header {
    background: linear-gradient(135deg, #1a365d 0%, #2c5282 100%);
    color: white;
    padding: 14px 18px;
    display: flex;
    align-items: center;
    gap: 10px;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
  }
  .header-icon { font-size: 22px; }
  .header-title { font-size: 16px; font-weight: 700; letter-spacing: 0.3px; }
  .header-sub { font-size: 11px; opacity: 0.8; margin-top: 1px; }

  /* ── Search bar ── */
  .search-wrap {
    padding: 14px 16px 8px;
    background: white;
    border-bottom: 1px solid #e2e8f0;
    position: sticky;
    top: 58px;
    z-index: 90;
  }
  .search-row {
    display: flex;
    gap: 8px;
    align-items: center;
  }
  #searchInput {
    flex: 1;
    padding: 10px 14px;
    border: 2px solid #3182ce;
    border-radius: 8px;
    font-size: 15px;
    outline: none;
    background: #fff;
    transition: border-color 0.2s;
  }
  #searchInput:focus { border-color: #2b6cb0; box-shadow: 0 0 0 3px rgba(49,130,206,0.2); }
  .btn-clear {
    background: #e2e8f0;
    border: none;
    border-radius: 6px;
    padding: 8px 12px;
    cursor: pointer;
    font-size: 13px;
    color: #4a5568;
    transition: background 0.15s;
  }
  .btn-clear:hover { background: #cbd5e0; }
  .hint {
    font-size: 11px;
    color: #718096;
    margin-top: 6px;
    padding-left: 2px;
  }

  /* ── Group filter tabs ── */
  .group-tabs {
    display: flex;
    gap: 4px;
    flex-wrap: wrap;
    padding: 8px 16px 10px;
    background: white;
    border-bottom: 1px solid #e2e8f0;
    position: sticky;
    top: 126px;
    z-index: 89;
  }
  .tab {
    padding: 4px 10px;
    border-radius: 20px;
    border: 1.5px solid #cbd5e0;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    background: white;
    color: #4a5568;
    transition: all 0.15s;
    white-space: nowrap;
  }
  .tab:hover { background: #ebf8ff; border-color: #3182ce; color: #2b6cb0; }
  .tab.active { background: #3182ce; border-color: #3182ce; color: white; }

  /* ── Results container ── */
  .results-wrap {
    padding: 12px 16px 20px;
    max-width: 900px;
    margin: 0 auto;
  }
  .results-count {
    font-size: 12px;
    color: #718096;
    margin-bottom: 10px;
    padding-left: 2px;
  }

  /* ── Result card ── */
  .card {
    background: white;
    border-radius: 10px;
    border: 1px solid #e2e8f0;
    margin-bottom: 10px;
    overflow: hidden;
    transition: box-shadow 0.15s, border-color 0.15s;
  }
  .card:hover { box-shadow: 0 4px 14px rgba(0,0,0,0.1); border-color: #bee3f8; }

  .card-header {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 14px 8px;
  }
  .code-badge {
    background: #ebf8ff;
    color: #2b6cb0;
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 13px;
    font-weight: 700;
    font-family: "Courier New", monospace;
    white-space: nowrap;
    border: 1px solid #bee3f8;
    min-width: 52px;
    text-align: center;
    flex-shrink: 0;
  }
  .card-main { flex: 1; min-width: 0; }
  .morph-name {
    font-size: 14px;
    font-weight: 600;
    color: #1a202c;
    line-height: 1.4;
    margin-bottom: 4px;
  }
  .iccc-line {
    font-size: 12px;
    color: #4a5568;
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    align-items: center;
  }
  .group-pill {
    background: #f7fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 1px 7px;
    font-size: 11px;
    font-weight: 600;
    color: #2d3748;
  }
  .subgroup-text { color: #718096; font-size: 11px; }

  /* Tags row */
  .card-tags {
    padding: 0 14px 10px;
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
  }
  .tag {
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 20px;
    font-weight: 600;
  }
  .tag-topo { background: #fffbeb; color: #92400e; border: 1px solid #fde68a; }
  .tag-ihc  { background: #fff5f5; color: #c53030; border: 1px solid #fed7d7; }
  .tag-alias { background: #f0fff4; color: #276749; border: 1px solid #c6f6d5; }
  .tag-note { background: #faf5ff; color: #553c9a; border: 1px solid #e9d8fd; }

  /* Alias card variant */
  .card.alias-card { border-left: 3px solid #38a169; }
  .alias-banner {
    background: #f0fff4;
    padding: 6px 14px;
    font-size: 11px;
    color: #276749;
    font-weight: 600;
    border-bottom: 1px solid #c6f6d5;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .alias-full-form { font-size: 13px; font-weight: 700; color: #1a202c; }

  /* IHC tree panel */
  .ihc-btn {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #fff5f5;
    color: #c53030;
    border: 1.5px solid #fc8181;
    border-radius: 6px;
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    margin: 0 14px 10px;
    transition: all 0.15s;
  }
  .ihc-btn:hover { background: #fed7d7; border-color: #e53e3e; }

  .ihc-panel {
    background: #fffbeb;
    border-top: 1px solid #fde68a;
    padding: 14px;
  }
  .ihc-title {
    font-size: 13px;
    font-weight: 700;
    color: #744210;
    margin-bottom: 10px;
  }
  .ihc-question {
    background: white;
    border: 1px solid #fde68a;
    border-radius: 8px;
    padding: 12px 14px;
    margin-bottom: 10px;
  }
  .ihc-q-text {
    font-size: 13px;
    font-weight: 600;
    color: #1a202c;
    margin-bottom: 10px;
    line-height: 1.4;
  }
  .ihc-btns { display: flex; gap: 8px; }
  .btn-yes, .btn-no {
    padding: 7px 20px;
    border-radius: 6px;
    border: none;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s;
  }
  .btn-yes { background: #48bb78; color: white; }
  .btn-yes:hover { background: #38a169; }
  .btn-no  { background: #e2e8f0; color: #4a5568; }
  .btn-no:hover  { background: #cbd5e0; }

  .ihc-breadcrumb {
    font-size: 11px;
    color: #718096;
    margin-bottom: 8px;
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    align-items: center;
  }
  .bc-step {
    background: #e2e8f0;
    border-radius: 4px;
    padding: 1px 7px;
    font-size: 11px;
  }
  .bc-arrow { color: #a0aec0; }

  .ihc-result {
    background: white;
    border: 2px solid #38a169;
    border-radius: 8px;
    padding: 12px 14px;
  }
  .ihc-result-label {
    font-size: 14px;
    font-weight: 700;
    color: #276749;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .ihc-result-code {
    font-family: "Courier New", monospace;
    background: #ebf8ff;
    color: #2b6cb0;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 13px;
    font-weight: 700;
  }
  .ihc-result-subgroup { font-size: 12px; color: #4a5568; margin-bottom: 6px; }
  .ihc-result-notes { font-size: 12px; color: #718096; line-height: 1.5; }
  .ihc-result-markers {
    background: #f0fff4;
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 11px;
    font-weight: 600;
    color: #276749;
    display: inline-block;
    margin-bottom: 6px;
    border: 1px solid #c6f6d5;
  }
  .btn-restart {
    margin-top: 8px;
    background: #e2e8f0;
    border: none;
    border-radius: 6px;
    padding: 6px 14px;
    font-size: 12px;
    cursor: pointer;
    color: #4a5568;
  }
  .btn-restart:hover { background: #cbd5e0; }

  /* Empty state */
  .empty-state {
    text-align: center;
    padding: 40px 20px;
    color: #718096;
  }
  .empty-icon { font-size: 40px; margin-bottom: 12px; }
  .empty-title { font-size: 16px; font-weight: 600; margin-bottom: 6px; }
  .empty-sub { font-size: 13px; }

  /* Welcome state */
  .welcome {
    text-align: center;
    padding: 30px 20px;
  }
  .welcome-title { font-size: 18px; font-weight: 700; color: #2d3748; margin-bottom: 8px; }
  .welcome-sub { font-size: 13px; color: #718096; max-width: 400px; margin: 0 auto 20px; line-height: 1.6; }
  .tips {
    text-align: left;
    background: white;
    border-radius: 10px;
    padding: 14px 16px;
    border: 1px solid #e2e8f0;
    max-width: 420px;
    margin: 0 auto;
  }
  .tips-title { font-size: 12px; font-weight: 700; color: #4a5568; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }
  .tip { font-size: 13px; color: #4a5568; margin-bottom: 6px; display: flex; gap: 8px; }
  .tip-icon { flex-shrink: 0; }

  /* Highlight match */
  mark { background: #fefcbf; color: #1a202c; border-radius: 2px; padding: 0 1px; }

  /* Topography info */
  .topo-wrap { padding: 0 14px 10px; }
  .topo-label { font-size: 11px; font-weight: 600; color: #718096; text-transform: uppercase; letter-spacing: 0.4px; margin-bottom: 4px; }
  .topo-codes { display: flex; flex-wrap: wrap; gap: 4px; }
  .topo-code {
    background: #f7fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 2px 7px;
    font-size: 11px;
    font-family: "Courier New", monospace;
    color: #4a5568;
  }

  /* REDCap value section */
  .redcap-row {
    background: #f7fafc;
    border-top: 1px solid #e2e8f0;
    padding: 6px 14px;
    font-size: 11px;
    color: #718096;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .redcap-label { font-weight: 600; color: #4a5568; }

  @media (max-width: 480px) {
    .header-title { font-size: 14px; }
    .card-header { gap: 8px; }
    .code-badge { min-width: 46px; font-size: 12px; }
    .morph-name { font-size: 13px; }
  }
</style>
</head>
<body>

<!-- Header -->
<div class="header">
  <div class="header-icon">🔬</div>
  <div>
    <div class="header-title">ICCC-3 Lookup Tool</div>
    <div class="header-sub">UCI Cancer Registry — ICD-O-3 to ICCC-3 Classification</div>
  </div>
</div>

<!-- Search bar -->
<div class="search-wrap">
  <div class="search-row">
    <input type="search"
           id="searchInput"
           placeholder="Search by diagnosis name, code, or abbreviation (e.g. AML, 9470, Wilms)…"
           autocomplete="off"
           autocorrect="off"
           spellcheck="false">
    <button class="btn-clear" id="clearBtn">Clear</button>
  </div>
  <div class="hint">Type at least 2 characters to search. Results include ICD-O-3 names and clinical aliases.</div>
</div>

<!-- Group tabs -->
<div class="group-tabs" id="groupTabs">
  <button class="tab active" data-group="all">All</button>
  <button class="tab" data-group="I">I&nbsp;Leukemias</button>
  <button class="tab" data-group="II">II&nbsp;Lymphomas</button>
  <button class="tab" data-group="III">III&nbsp;CNS</button>
  <button class="tab" data-group="IV">IV&nbsp;Neuroblastoma</button>
  <button class="tab" data-group="V">V&nbsp;Retinoblastoma</button>
  <button class="tab" data-group="VI">VI&nbsp;Renal</button>
  <button class="tab" data-group="VII">VII&nbsp;Hepatic</button>
  <button class="tab" data-group="VIII">VIII&nbsp;Bone</button>
  <button class="tab" data-group="IX">IX&nbsp;Soft Tissue</button>
  <button class="tab" data-group="X">X&nbsp;Germ Cell</button>
  <button class="tab" data-group="XI">XI&nbsp;Epithelial</button>
  <button class="tab" data-group="XII">XII&nbsp;Other</button>
</div>

<!-- Results area -->
<div class="results-wrap" id="resultsWrap">
  <div class="welcome" id="welcomeScreen">
    <div class="welcome-title">ICD-O-3 / ICCC-3 Lookup</div>
    <div class="welcome-sub">Search for a cancer diagnosis to find the ICCC-3 group, subgroup, and morphology code for REDCap data entry.</div>
    <div class="tips">
      <div class="tips-title">Search tips</div>
      <div class="tip"><span class="tip-icon">💊</span><span>Clinical name: <strong>AML</strong>, <strong>ALL</strong>, <strong>Wilms tumour</strong></span></div>
      <div class="tip"><span class="tip-icon">🔢</span><span>Morphology code: <strong>9470</strong>, <strong>9861</strong></span></div>
      <div class="tip"><span class="tip-icon">🔬</span><span>Histology name: <strong>Medulloblastoma</strong>, <strong>Burkitt</strong></span></div>
      <div class="tip"><span class="tip-icon">📁</span><span>Browse by group using the tabs above</span></div>
    </div>
  </div>
</div>

<script>
// ── Embedded data ──────────────────────────────────────────────────────────────
const DB      = __DB_DATA__;
const ALIASES = __ALIASES_DATA__;
const TOPO    = __TOPO_DATA__;
const IHC     = __IHC_DATA__;

// ── Build indices ──────────────────────────────────────────────────────────────
// Topography lookup: code → name
const topoMap = {};
TOPO.forEach(t => { topoMap[t.code] = t.name; });

// Group label map
const GROUP_NAMES = {
  'I':   'Leukemias, Myeloproliferative And Myelodysplastic Diseases',
  'II':  'Lymphomas And Reticuloendothelial Neoplasms',
  'III': 'CNS And Miscellaneous Intracranial And Intraspinal Neoplasms',
  'IV':  'Neuroblastoma And Other Peripheral Nervous Cell Tumors',
  'V':   'Retinoblastoma',
  'VI':  'Renal Tumors',
  'VII': 'Hepatic Tumors',
  'VIII':'Malignant Bone Tumors',
  'IX':  'Soft Tissue And Other Extraosseous Sarcomas',
  'X':   'Germ Cell Tumors, Trophoblastic Tumors And Neoplasms Of Gonads',
  'XI':  'Other Malignant Epithelial Neoplasms And Malignant Melanomas',
  'XII': 'Other And Unspecified Malignant Neoplasms',
};

// ── State ──────────────────────────────────────────────────────────────────────
let currentGroup  = 'all';
let currentQuery  = '';
let ihcStates     = {};  // cardId → {tree, node, breadcrumb}

// ── Search function ────────────────────────────────────────────────────────────
function normalise(s) {
  return String(s).toLowerCase().replace(/[^a-z0-9]/g, ' ').replace(/\s+/g,' ').trim();
}

function search(query, group) {
  const q = normalise(query);
  if (q.length < 2 && group === 'all') return [];

  const words = q.split(' ').filter(Boolean);
  if (!words.length) return [];

  const dbResults = [];
  const seen = new Set();

  // Search DB
  DB.forEach(entry => {
    if (group !== 'all' && entry.iccc3_group !== group) return;

    const haystack = normalise(entry.morphology_code + ' ' + entry.morphology_name);
    const score = scoreMatch(words, haystack, entry.morphology_code);
    if (score > 0) {
      const key = entry.morphology_code + '|' + entry.iccc3_subgroup_id;
      if (!seen.has(key)) {
        seen.add(key);
        dbResults.push({ type: 'db', score, entry, query });
      }
    }
  });

  // Search aliases
  const aliasResults = [];
  ALIASES.forEach(alias => {
    if (!alias.maps_to_morphology_codes || !alias.maps_to_morphology_codes.length) return;

    const haystack = normalise(alias.alias + ' ' + (alias.full_form || '') + ' ' + (alias.notes || ''));
    const score = scoreMatch(words, haystack, alias.alias);
    if (score > 0) {
      // Find matching DB entries for this alias
      alias.maps_to_morphology_codes.forEach(code => {
        const matching = DB.filter(e => e.morphology_code === code && (group === 'all' || e.iccc3_group === group));
        if (matching.length > 0) {
          const key = 'alias|' + alias.alias + '|' + code;
          if (!seen.has(key)) {
            seen.add(key);
            aliasResults.push({ type: 'alias', score, alias, entry: matching[0], query });
          }
        }
      });
    }
  });

  // If query is a pure group filter (no text), show all entries for that group
  if (q.length < 2 && group !== 'all') {
    const groupEntries = [];
    const groupSeen = new Set();
    DB.forEach(entry => {
      if (entry.iccc3_group !== group) return;
      const key = entry.morphology_code + '|' + entry.iccc3_subgroup_id;
      if (!groupSeen.has(key)) {
        groupSeen.add(key);
        groupEntries.push({ type: 'db', score: 1, entry, query: '' });
      }
    });
    return groupEntries.slice(0, 200);
  }

  // Combine: aliases first (more likely what clerk searched), then DB hits
  const combined = [...aliasResults, ...dbResults];
  combined.sort((a,b) => b.score - a.score);

  // Deduplicate final list by morphology_code+subgroup_id (showing alias version if available)
  const finalSeen = new Set();
  return combined.filter(r => {
    const key = (r.alias ? 'alias_' : '') + r.entry.morphology_code + '|' + r.entry.iccc3_subgroup_id;
    if (finalSeen.has(key)) return false;
    finalSeen.add(key);
    return true;
  }).slice(0, 80);
}

function scoreMatch(words, haystack, exactField) {
  const norm = normalise(exactField || '');
  let score = 0;
  // Exact match on code or alias = highest score
  if (words.length === 1 && norm === words[0]) score += 100;
  // Starts with
  if (norm.startsWith(words[0])) score += 50;
  // All words present
  const allPresent = words.every(w => haystack.includes(w));
  if (allPresent) score += 30;
  else {
    const matchCount = words.filter(w => haystack.includes(w)).length;
    score += matchCount * 5;
  }
  return score;
}

// ── Render ─────────────────────────────────────────────────────────────────────
function highlight(text, query) {
  if (!query || query.length < 2) return escHtml(text);
  const words = normalise(query).split(' ').filter(w => w.length >= 2);
  let result = escHtml(text);
  words.forEach(w => {
    const re = new RegExp('(' + escRe(w) + ')', 'gi');
    result = result.replace(re, '<mark>$1</mark>');
  });
  return result;
}

function escHtml(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
function escRe(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
}

function renderResults(results, query, group) {
  const wrap = document.getElementById('resultsWrap');
  const welcome = document.getElementById('welcomeScreen');

  if (query.length < 2 && group === 'all') {
    wrap.innerHTML = '';
    wrap.appendChild(welcome);
    return;
  }

  if (!results.length) {
    wrap.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">🔍</div>
        <div class="empty-title">No results found</div>
        <div class="empty-sub">Try a different spelling, abbreviation, or morphology code.<br>For clinical names like "AML", make sure Groups I–III are selected.</div>
      </div>`;
    return;
  }

  wrap.innerHTML = `<div class="results-count">${results.length} result${results.length!==1?'s':''} ${group!=='all'?'in Group '+group:''}</div>`;

  results.forEach((r, idx) => {
    const cardId = 'card_' + idx;
    const card = document.createElement('div');
    card.className = 'card' + (r.type === 'alias' ? ' alias-card' : '');
    card.id = cardId;

    const e = r.entry;
    const q = r.query || query;

    // Alias banner
    if (r.type === 'alias') {
      const a = r.alias;
      card.innerHTML += `
        <div class="alias-banner">
          🏷️ CLINICAL NAME / ALIAS &rarr; <span class="alias-full-form">${highlight(a.alias,q)}</span>
          ${a.full_form && a.full_form !== a.alias ? '&nbsp;&mdash;&nbsp;' + escHtml(a.full_form) : ''}
          &nbsp;(${escHtml(a.origin_system||'')})
        </div>`;
      if (a.notes) {
        card.innerHTML += `<div class="card-tags"><span class="tag tag-note">ℹ️ ${escHtml(a.notes)}</span></div>`;
      }
      if (a.needs_ihc_tree && a.ihc_tree_id && IHC[a.ihc_tree_id]) {
        card.innerHTML += `<button class="ihc-btn" onclick="startIhcTree('${cardId}','${a.ihc_tree_id}')">
          🧬 IHC Decision Tree Needed — Click to classify
        </button>`;
        card.innerHTML += `<div class="ihc-panel" id="ihc_${cardId}" style="display:none"></div>`;
      }
    }

    // Main card body
    card.innerHTML += `
      <div class="card-header">
        <div class="code-badge">${highlight(e.morphology_code, q)}</div>
        <div class="card-main">
          <div class="morph-name">${highlight(e.morphology_name, q)}</div>
          <div class="iccc-line">
            <span class="group-pill">Group ${escHtml(e.iccc3_group)}</span>
            <span class="subgroup-text">${escHtml(e.iccc3_subgroup_id)} — ${highlight(e.iccc3_subgroup_name, q)}</span>
          </div>
        </div>
      </div>`;

    // Tags
    let tags = '';
    if (e.topography_dependent) {
      tags += `<span class="tag tag-topo">⚠️ Topography-dependent classification</span>`;
    }
    if (tags) {
      card.innerHTML += `<div class="card-tags">${tags}</div>`;
    }

    // Primary sites
    if (e.primary_sites && e.primary_sites.length > 0 && !(e.primary_sites.length === 1 && e.primary_sites[0] === 'C00.0-C80.9')) {
      const codes = e.primary_sites.map(s => {
        // Try to look up individual codes
        const name = topoMap[s] ? ` (${escHtml(topoMap[s])})` : '';
        return `<span class="topo-code">${escHtml(s)}${name}</span>`;
      }).join('');
      card.innerHTML += `
        <div class="topo-wrap">
          <div class="topo-label">Primary site required</div>
          <div class="topo-codes">${codes}</div>
        </div>`;
    }

    // REDCap value
    card.innerHTML += `
      <div class="redcap-row">
        <span class="redcap-label">REDCap value:</span>
        <span>${escHtml(e.redcap_value)}</span>
        &nbsp;|&nbsp;
        <span class="redcap-label">Group name:</span>
        <span>${escHtml(e.iccc3_group_name)}</span>
      </div>`;

    // IHC tree button for DB results (if alias has ihc flag)
    if (r.type === 'db') {
      // Check if any alias for this entry requests an IHC tree
      const matchAlias = ALIASES.find(a => a.maps_to_morphology_codes && a.maps_to_morphology_codes.includes(e.morphology_code) && a.needs_ihc_tree && a.ihc_tree_id);
      if (matchAlias && IHC[matchAlias.ihc_tree_id]) {
        card.innerHTML += `<button class="ihc-btn" onclick="startIhcTree('${cardId}','${matchAlias.ihc_tree_id}')">
          🧬 IHC Decision Tree Available — Click to verify lineage
        </button>`;
        card.innerHTML += `<div class="ihc-panel" id="ihc_${cardId}" style="display:none"></div>`;
      }
    }

    wrap.appendChild(card);
  });
}

// ── IHC Decision Tree ──────────────────────────────────────────────────────────
function startIhcTree(cardId, treeId) {
  ihcStates[cardId] = { treeId, nodeId: 'root', breadcrumb: [] };
  renderIhcNode(cardId);
  const panel = document.getElementById('ihc_' + cardId);
  if (panel) {
    panel.style.display = 'block';
    panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}

function renderIhcNode(cardId) {
  const state = ihcStates[cardId];
  const tree  = IHC[state.treeId];
  const panel = document.getElementById('ihc_' + cardId);
  if (!panel || !tree) return;

  panel.innerHTML = `<div class="ihc-title">🧬 ${escHtml(tree.title)}</div>`;

  // Breadcrumb
  if (state.breadcrumb.length > 0) {
    let bc = '<div class="ihc-breadcrumb">';
    state.breadcrumb.forEach((step, i) => {
      bc += `<span class="bc-step">${escHtml(step.answer)}</span>`;
      if (i < state.breadcrumb.length - 1) bc += '<span class="bc-arrow">→</span>';
    });
    bc += '</div>';
    panel.innerHTML += bc;
  }

  const node = tree.nodes[state.nodeId];

  if (!node) {
    // Try result
    const result = tree.results[state.nodeId];
    if (result) {
      renderIhcResult(panel, result, cardId);
      return;
    }
    panel.innerHTML += '<p style="color:#e53e3e">Error: node not found</p>';
    return;
  }

  // Question node
  panel.innerHTML += `
    <div class="ihc-question">
      <div class="ihc-q-text">${escHtml(node.question)}</div>
      <div class="ihc-btns">
        <button class="btn-yes" onclick="answerIhc('${cardId}','yes')">✅ Yes</button>
        <button class="btn-no"  onclick="answerIhc('${cardId}','no')">❌ No</button>
      </div>
    </div>`;
}

function answerIhc(cardId, answer) {
  const state = ihcStates[cardId];
  const tree  = IHC[state.treeId];
  const node  = tree.nodes[state.nodeId];
  if (!node) return;

  const shortQ = node.question.replace(/\?.*/, '?').substring(0, 50) + (node.question.length > 50 ? '…' : '');
  state.breadcrumb.push({ q: shortQ, answer: answer === 'yes' ? 'YES' : 'NO' });
  state.nodeId = answer === 'yes' ? node.yes : node.no;
  renderIhcNode(cardId);
}

function renderIhcResult(panel, result, cardId) {
  panel.innerHTML += `
    <div class="ihc-result">
      <div class="ihc-result-label">
        ✅ ${escHtml(result.label)}
        <span class="ihc-result-code">${escHtml(result.morphology_code)}</span>
      </div>
      <div class="ihc-result-subgroup">Group ${escHtml(result.iccc3_group)} &bull; ${escHtml(result.iccc3_subgroup_id)} — ${escHtml(result.iccc3_subgroup_name)}</div>
      ${result.marker_summary ? `<div class="ihc-result-markers">IHC: ${escHtml(result.marker_summary)}</div>` : ''}
      ${result.notes ? `<div class="ihc-result-notes">ℹ️ ${escHtml(result.notes)}</div>` : ''}
      <button class="btn-restart" onclick="startIhcTree('${cardId}','${ihcStates[cardId].treeId}')">↺ Restart tree</button>
    </div>`;
}

// ── Event handlers ─────────────────────────────────────────────────────────────
let searchTimer;

document.getElementById('searchInput').addEventListener('input', function() {
  clearTimeout(searchTimer);
  const q = this.value.trim();
  currentQuery = q;
  searchTimer = setTimeout(() => {
    const results = search(q, currentGroup);
    renderResults(results, q, currentGroup);
  }, 120);
});

document.getElementById('clearBtn').addEventListener('click', function() {
  const input = document.getElementById('searchInput');
  input.value = '';
  currentQuery = '';
  currentGroup = 'all';
  document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.group === 'all'));
  renderResults([], '', 'all');
  input.focus();
});

document.getElementById('groupTabs').addEventListener('click', function(e) {
  const btn = e.target.closest('.tab');
  if (!btn) return;
  currentGroup = btn.dataset.group;
  document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t === btn));
  const results = search(currentQuery, currentGroup);
  renderResults(results, currentQuery, currentGroup);
});

// Auto-focus search on load
window.addEventListener('load', () => {
  document.getElementById('searchInput').focus();
});
</script>
</body>
</html>"""

if __name__ == '__main__':
    main()
