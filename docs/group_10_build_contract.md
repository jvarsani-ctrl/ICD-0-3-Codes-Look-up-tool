# Group 10 build contract — Germ cell, trophoblastic and gonadal tumours

**Branch:** `claude/group-10-tumor-pathway-3a99f7`, a worktree at
`.claude/worktrees/group-7-tumor-pathway-a88513`, cut from `main` at `dbe5fd4` (Groups 1–8
merged). Group 9 is built on `claude/group-9-tumor-pathway-911c69` and not merged; §7 lists the
lines both branches touch.

**Written 4 October 2026, before any JSON was authored.** Code decisions D1–D22 are argued in
`docs/superpowers/specs/2026-10-04-group-10-germ-cell-code-decisions-design.md` and are not
repeated here. Everything that needs the registrar goes to `docs/group_10_registrar_review.md`.

> **Standing rule, inherited.** The tool must never overstate its evidence. Group X has two sharp
> instances. REDCap's `x_morph` offers `9064` as "Intratubular malignant germ cells", the in situ
> term, for the number ICD-O-3.2 calls *Germinoma*. And `9100` reads "Hydatidiform mole, NOS",
> the benign term, for the number that carries choriocarcinoma.

---

## 0. Pre-context

### 0.1 ★ The ICCC-3 definition, read off `ICCC-2017.sqlite`

`code_ranges` for `main_group = 'X'`, ranges 94–117:

| Ranges | Subgroups | Topography (REDCap 3-digit) | Behaviour |
|---|---|---|---|
| 94–99 | Xa1–Xa6 (germinomas `9060-9065`, teratomas `9080-9084`, embryonal `9070,9072`, yolk sac `9071`, choriocarcinoma `9100,9101`, mixed `9085`) | `700-729,751-753` | **`0-1,3`** |
| 100–105 | Xb1–Xb6 (same sets; Xb5 adds `9103-9105`; Xb6 adds `9086`) | `000-559,570-619,630-699,739-750,754-768,809` | `3` |
| 106–112 | Xc1–Xc7 (same sets; Xc2 adds `9090,9091`; Xc5 is `9100-9105`; Xc7 is `9073`) | `569,620-629` | `3` |
| 113–115 | Xd gonadal carcinomas | 113 `569,620-629`; 114 `000-809`; 115 `569` | `3` |
| 116 | Xe `8590-8671` | `000-809` | `3` |
| 117 | Xe `8000-8005` | `569,620-629` | `3` |

What follows:

1. **Only Xa admits behaviours `0` and `1`.** `9080/0`, `9080/1`, `9084/0`, `9100/0`, `9100/1`
   are Group X codes in the central nervous system and behaviour exclusions everywhere else.
2. **The same (code, behaviour) sits in up to three subgroups by site.** `9071/3` is Xa4, Xb4
   or Xc4. The validator allows one entry per pair, so each such entry carries
   `iccc3_subgroup_by_topography` (D16, D20).
3. **Xc7 is empty.** ICD-O-3.2 has `9073/1` only (D10).
4. **Gonadal `8000–8005` is Xe** (range 117; D13).

### 0.2 ★ The inventory — 131 usable codes, 136 entries

`build/generate_group_inventory.py --group X`, 4 October 2026:

```
ICCC range entries 327 · distinct codes 290 · absent from ICD-O-3.2 159 · usable 131 · (code,behaviour) records 171
```

171 records collapse to **136 distinct (code, behaviour) pairs**: 18 pairs repeat across
subgroups. By subgroup: Xa 22 (incl. five below `/3`), Xb 19, Xc 22, Xd 96, Xe 14 records.

### 0.3 What ICD-O-3.2 changed in this group

| Change | Source |
|---|---|
| `9086/3` *Germ cell tumor with associated hematological malignancy* new | *New codes and their terms*, p. 2 |
| `8594/1` *Mixed germ cell-sex cord-stromal tumor, NOS* new; `8643/1` new | same, p. 2 |
| `8622/0` *Granulosa cell tumor of testis, juvenile* new; `8590/0` new | same, p. 4 |
| `8620/1` → `/3` for *Granulosa cell tumor, adult type (C56.9)* | *Terms that are changing behaviour*, p. 4 |
| `8622/1` kept for the ovary; testis becomes `8622/0` | same, p. 6 |
| `9080/1` for immature teratoma of lung, thymus, thyroid; `9080/3` elsewhere | same, p. 6 |
| `8650` split: ovary `/0`, testis `/1` | same, p. 6 |

### 0.4 Engine facts that shape every node

Unchanged from Group 8 build contract §0.5: `when` is string equality; `resolution_logic[]` is
flat and first-match-wins; `clinical_alert` is `null` everywhere (ruling 9); NOS fallback is
required on `ihc_checklist` and forbidden (explicit `null`) on every other type used here;
`refer_group` carries no code; `behaviour_exclusion.icdo_term` is the ICD-O-3.2 **Preferred**
term at its (code, behaviour). Also:

- Cross-tree `next_node` is legal in the validator (`check_orphan_nodes`) and in `app.js`
  (`findNode` searches every tree). Groups 1–3 use it 95 times.
- `site_resolution` renders as an option list (`app.js` `nodeControl`).
- Router `tree_routing` entries must be `document_inventory` nodes (`build_database.py`
  ~L10168).
- A referral is a terminal screen; nothing carries into the target group (D18).
- The search box enters a group with no topography, so `tree_routing.default` receives it.
- "Also called" lists aliases by four-digit code (D21).

### 0.5 ★ Visser Table 4 — what may be registered without tissue

Visser O, et al. Front Oncol 2023;13:1250549. Table 4 (p. 06): germ cell tumour + human chorionic
gonadotropin → `9064/3`; + alpha-fetoprotein ± human chorionic gonadotropin → `9065/3`;
choriocarcinoma of the placenta + human chorionic gonadotropin → `9100/3`; basis 4. Rule 6
(p. 05): basis 4 needs a clinical investigation showing the tumour. Rule 5 (p. 03): otherwise
`8000/3`. Rule 4 (p. 03): "possible" is not registrable. Summary in
`docs/references/visser-2023-key-points.md` §5.

---

## 1. Files this build creates or changes

| File | Kind | Task |
|---|---|---|
| `build/generate_group10_entries.py` | new — entries, metadata, writes the dt.json | T1 |
| `build/group10_tree.py` | new — the five trees | T2 |
| `data/database/group_10_dt.json` | generated | T1, T2 |
| `data/shared/presentation_router.json` | edit | T3 |
| `data/shared/topography_codes.json` | edit | T3 |
| `build/build_database.py` | edit — registration and four Group 10 rules | T4 |
| `build/negative_controls_group10.py` | new | T4 |
| `docs/validator_negative_controls.md` | append a Group 10 section | T4 |
| `build/generate_group10_aliases.py` | new | T5 |
| `data/aliases/aliases_group_10.json` | generated | T5 |
| `data/aliases/alias_index.json` | regenerated by the build, committed (rule 15) | T7 |
| `docs/clinical-warnings.md`, `docs/group_10_layer1_repair.md`, `docs/codes-awaiting-redcap.md`, `docs/TODO.md`, `docs/group_baseline_documents.md`, `docs/sources-requested.md` | docs | T6 |
| `docs/group_10_build_report.md`, `docs/group_10_registrar_review.md` | docs | T8 |

`app.js`, `index.html`, `uccf-tool.css` and every other group's `group_NN_dt.json` and alias file
stay byte-identical to `main`.

Environment for every command in a worktree:

```bash
export ICD_LAYER1="/Users/jay/Ai Environment/Cancer Registry/ICD coding"
export ICCC_DB="/Users/jay/Ai Environment/Cancer Registry/ICCC-2017.sqlite"
export ICDO_DB="/Users/jay/Ai Environment/Cancer Registry/ICD coding/ICD-O-3.2/icdo32.sqlite"
```

---

## 2. Entries — `build/generate_group10_entries.py` (T1)

Modelled on `build/generate_group08_entries.py`. Reads `ICCC_DB` and `ICDO_DB` from the
environment, falling back to the module defaults.

1. `gi.build_inventory(ICCC_PATH, ICDO_PATH, "X")` gives 171 records. Group them by
   (code, behaviour) into **136 entries**. Assert both counts.
2. `morphology_name` is the ICD-O-3.2 **preferred** term at the entry's behaviour.
3. **Subgroup.** For a pair in one subgroup: that subgroup, `topography_dependent: false`. For a
   pair in more than one: `topography_dependent: true`, a `topography_routing_note`, and
   `iccc3_subgroup_by_topography` — one rule per subgroup, each listing every code in
   `data/shared/topography_codes.json` (after T3's additions: include `C62.0`, `C62.1`, `C76.3`
   in the lists even though T3 adds them to the lookup) that falls in that subgroup's ICCC
   topography ranges. The entry's own `iccc3_subgroup_id` is the default per D20: Xc if the pair
   has an Xc subgroup, else Xb, else Xa. Compute the lists from the ICCC range strings; never
   type them.
4. `primary_sites`: the ICCC topography of each subgroup, in the Group 8 format.
5. `who_version`: "ICD-O-3.2" by default; annotations may set "WHO 2022 (Moch Table 3)" or
   "WHO CNS5 (Louis Table 1)" where the D-numbers cite them.
6. **Annotations** keyed by `code/behaviour` for every pair the tree emits (§4): 
   `diagnostic_tests_required`, `ihc_markers_required` where the IHC rules use them, and a
   `coding_note` naming the D-number and the node(s) that emit it. Pairs the tree never emits get
   the templated note "In the inventory, not on the tree: reachable by search where aliased."
   The five Xa pairs below `/3` that the tree does not emit (`9100/0`, `9100/1`) say why (D8).
7. **REDCap.** Parse the Group 10 option file with `build_database.parse_redcap_options` (or the
   same parsing) — the build reads that markdown, not the REDCap snapshot. For each entry:
   - option present and its label equal to `morphology_name` → `redcap_option_verified: true`;
   - present with a different label → `redcap_option_verified: false`, and `coding_note` gains
     `Layer 1: x_morph offers <code> as "<label>"; ICD-O-3.2's preferred term at /<b> is "<name>".`
     (the Group 8 `REDCAP_DRIFT` pattern, computed, not typed);
   - absent → `redcap_option_verified: false` and `awaiting_layer1:
     {"reason": ..., "needs": ["REDCap Group 10 option list"], "todo": "docs/codes-awaiting-redcap.md"}`.
     `9102` is one; compute the rest. T6 lists every one under `## Group 10 — open`.
8. `metadata`: `group_id` 10, `group_name` "Germ Cell, Trophoblastic Tumors and Neoplasms of
   Gonads", `iccc3_version`, `icdo_version`, `total_morphology_entries` 136,
   `total_decision_nodes`, `decision_trees` (the five tree ids in §4 order),
   `basis_of_diagnosis_declarations` `{"ihc_counts_as": 7, "methylation_counts_as": 8}`.
9. `carry_branch_sequences` as in Group 8, so `induce_flow.py` output survives regeneration.
10. Writes `{metadata, morphology_entries, decision_trees: group10_tree.trees()}`. `--check`
    writes nothing and exits non-zero if the file would change. T1 ships a stub
    `build/group10_tree.py` whose `trees()` returns `[]`; T2 replaces it.

---

## 3. Shared layer — router and topography (T3)

### 3.1 `data/shared/presentation_router.json`

`groups["10"]`:

```json
{
  "name": "Germ Cell, Trophoblastic Tumors and Neoplasms of Gonads",
  "built": true,
  "trees": [
    {"tree_id": "g10_cns", "entry_node": "cn_document_inventory"},
    {"tree_id": "g10_ovary", "entry_node": "ov_document_inventory"},
    {"tree_id": "g10_testis", "entry_node": "ts_document_inventory"},
    {"tree_id": "g10_extragonadal", "entry_node": "eg_document_inventory"},
    {"tree_id": "g10_site_unstated", "entry_node": "su_document_inventory"}
  ],
  "tree_routing": {
    "_comment": "...D16...",
    "variable": "topography",
    "rules": [
      {"topography_in": [every lookup code in ICCC Xa ranges], "tree_id": "g10_cns", "entry_node": "cn_document_inventory", "label": "Brain, spinal cord, pineal and suprasellar region"},
      {"topography_in": ["C56.9"], "tree_id": "g10_ovary", "entry_node": "ov_document_inventory", "label": "Ovary"},
      {"topography_in": ["C62.0", "C62.1", "C62.9"], "tree_id": "g10_testis", "entry_node": "ts_document_inventory", "label": "Testis"},
      {"topography_in": [every lookup code in ICCC Xb ranges], "tree_id": "g10_extragonadal", "entry_node": "eg_document_inventory", "label": "Any other site"}
    ],
    "default": {"tree_id": "g10_site_unstated", "entry_node": "su_document_inventory", "label": "Site not recorded", "reason": "..."}
  },
  "handoff": {"group": 10, "tree_id": "g10_site_unstated", "entry_node": "su_document_inventory"}
}
```

The Xa list must satisfy the router check that a branch naming C70.9, C71.9 or C72.9 lists all
21 central nervous system codes (`build_database.py` ~L10317). Compute both lists from ICCC
ranges against the lookup after §3.2's additions.

`dual_group_rules["8000-8005"]`: append one branch after the C22 branch —
`{"when": {"topography_in": ["C56.9","C62.0","C62.1","C62.9"]}, "then": {"group": 10, "subgroup": "Xe"}}`
in whatever exact shape the existing branches use. Update the rule's authoring note in one
sentence. Touch no other rule.

### 3.2 `data/shared/topography_codes.json`

- Add lookups `C62.0` (REDCap `620`), `C62.1` (`621`) and `C76.3` (`763`), labels and REDCap
  codes read from `ICD coding/RedCap Options/Topography Redcap.md`. Insert them beside their
  neighbours (`C62.9`; the `C76.x` neighbours or end of the C7x block), **not** at the
  `C49.9`→`C74.0` boundary, where the Group 9 branch inserts 448 lines.
- `C62.0`, `C62.1`: `candidate_groups: [10]`, crosswalk row `gonad_sacrococcygeal_midline`.
- `C76.3`: `candidate_groups: [4, 9, 10]`, `candidate_groups_advisory: true`, a note that the
  ICD-O-3 topography index files the sacrococcygeal region under C76.3 *Pelvis, NOS* (verify
  the wording against the Layer 1 topography file; if the file does not say it, write only what it
  says). Crosswalk row: `gonad_sacrococcygeal_midline`, whose label becomes "Ovary, testis and
  sacrococcygeal region".
- Add `10` to `candidate_groups` of `C38.1`, `C38.3` and `C48.0` (D19). Leave every other field.
- Do not edit the C48 crosswalk row (Group 9 edits its tail).

---

## 4. The trees — `build/group10_tree.py` (T2)

Modelled on `build/group08_tree.py`. **The histotype logic is written once** as Python
functions parameterised by site, and instantiated per tree. Helpers:

- `code(label, code, beh, basis, reason, **kw)`; `go(label, next_node, **kw)`;
  `refer(label, group, reason, refer_code=None)`; `nonrep(label, reason)`;
- `excl(label, code, beh, reason)` — **looks up `icdo_term` as the ICD-O-3.2 Preferred term from
  `icdo32.sqlite` at generation time**; `group_declares` is `"3"`; `registrar_decision_required`
  true where the D-number is provisional.
- Every `reason` that names a code uses the ICD-O-3.2 preferred term and the code, e.g.
  "Recorded as Germinoma (9064/3)." Clerk-facing text goes in `question`, `hint`, `label`,
  `reason`; author notes in `coding_note`. No `clinical_alert` text (ruling 9).

Basis of diagnosis on code branches: referral 1, imaging 2, markers 4, cytology 5, histology 7,
immunohistochemistry 7.

### 4.1 Trees

| Tree | Prefix | `topography` | Nodes |
|---|---|---|---|
| `g10_cns` | `cn_` | C70.0–C72.9, C75.1–C75.3 | document_inventory, clinical_alias, markers, imaging, cytology, histology, mixed, ihc |
| `g10_ovary` | `ov_` | C56.9 | the eight above, plus teratoma, gonadoblastoma, sex_cord, epithelial, unspecified, other |
| `g10_testis` | `ts_` | C62.0–C62.9 | the eight, plus teratoma, gonadoblastoma, sex_cord, unspecified, other |
| `g10_extragonadal` | `eg_` | the Xb ranges | the eight, plus teratoma, other |
| `g10_site_unstated` | `su_` | none — default | document_inventory and five `site_resolution` nodes; **no terminals** |

Use whatever `topography` value format the validator accepts for the extragonadal and
site-unstated trees; record the choice in the tree's `coding_note`-equivalent comment.

### 4.2 Nodes common to the four site trees (prefix `p`)

**`p_document_inventory`** (`document_inventory`), "What is in the file for this tumour?"
`captured_variables: ["evidence_tests","workup_status","basis_evidence_tier"]`, Group 8 capture shape:

| Option | → | `evidence_tests` |
|---|---|---|
| A referral letter or clinical note only — no imaging report, no marker result, no tissue | `p_clinical_alias` | `[]` |
| An imaging report **and** a serum or cerebrospinal fluid alpha-fetoprotein or human chorionic gonadotropin result — no tissue | `p_markers` | `["Imaging","Tumour markers"]` |
| An imaging report only — no marker result, no tissue | `p_imaging` | `["Imaging"]` |
| Cytology only — cerebrospinal fluid, effusion or fine-needle aspirate; no tissue | `p_cytology` | `["Cytology"]` |
| A histology report — biopsy or resection | `p_histology` | `["Histology"]` |

If `"Tumour markers"` is not an accepted `evidence_tests` value, report it (NEEDS_CONTEXT):
Group 3 already captures it on `md_gct_*`.

**`p_clinical_alias`** (`clinical_alias`):
- The note states a malignant tumour, at least probable → ovary/testis: `8000/3` basis 1;
  CNS: `refer(3, refer_code "8000")` — ICCC-2017 places `8000/3` at this site in IIIf;
  extragonadal: `refer(12, refer_code "8000")`.
- The note says only possible or suspected → `nonrep` (Visser rule 4).
- An imaging report is on file after all → `p_imaging`.

**`p_markers`** (`morphology_only`) (D4). Hint: "Use the report's own words. The value must be
called raised against the laboratory's range for the patient's age; a newborn's
alpha-fetoprotein is high without a tumour."
- Imaging shows a tumour and alpha-fetoprotein is raised, with or without human chorionic
  gonadotropin → `9065/3` basis 4.
- Imaging shows a tumour and human chorionic gonadotropin is raised; alpha-fetoprotein is
  normal or not measured → `9064/3` basis 4, reason states ICD-O-3.2 files *Germ cell tumor, NOS*
  under 9064/3 (D2).
- **Extragonadal only:** a tumour of the uterus or placenta after a pregnancy, with human
  chorionic gonadotropin raised → `9100/3` basis 4.
- Neither marker is raised → `p_imaging`.
- A marker is raised but no imaging shows a tumour → `nonrep` (Visser rule 6).

**`p_imaging`** (`morphology_only`):
- Imaging shows a malignant tumour, at least probable → ovary/testis `8000/3` basis 2;
  CNS `refer(3, "8000")`; extragonadal `refer(12, "8000")`.
- Imaging calls it possible only, or describes a benign lesion → `nonrep`.
- A histology report is on file → `p_histology`.

**`p_cytology`** (`morphology_only`):
- Cytology names germinoma or the site's term for it → the site family code (D3: CNS `9064`,
  ovary `9060`, testis `9061`, extragonadal `9064`), `/3`, basis 5.
- Cytology names a malignant germ cell tumour without its type → `9064/3` basis 5 (D2).
- Malignant cells, type not named → ovary/testis `8001/3` basis 5; CNS `refer(3, "8001")`;
  extragonadal `refer(12, "8001")`.
- No malignant cells, or not diagnostic → `p_imaging`.

**`p_mixed`** (`histology_subclassification`) (D6), "Which components does the report list?":
choriocarcinoma among them → `9101/3`; embryonal carcinoma and teratoma only → `9081/3`;
teratocarcinoma → `9081/3`; malignant teratoma, undifferentiated → `9082/3`; malignant teratoma,
intermediate → `9083/3`; teratoma and seminoma → `9085/3`; any other combination, or components
not listed → `9085/3`. **Ovary and testis add** malignant teratoma, trophoblastic → `9102/3`.
**Extragonadal adds** germ cell tumour with an associated haematological malignancy → `9086/3`.

**`p_ihc`** (`ihc_checklist`) — for a germ cell tumour whose type the report does not name but
whose immunostains it lists. Marker groups: germ cell lineage (SALL4, OCT3/4); germinoma
(CD117, SOX17, D2-40); embryonal carcinoma (CD30, SOX2); yolk sac tumour (glypican-3,
alpha-fetoprotein in tissue, HNF1-beta). Rules, first match wins, basis 7:

| # | Positive | Negative | Result |
|---|---|---|---|
| 1 | OCT3/4, CD30 | — | `9070/3` |
| 2 | OCT3/4, SOX2 | SOX17 | `9070/3` |
| 3 | OCT3/4, CD117 | — | family code (D3) |
| 4 | OCT3/4, SOX17 | — | family code |
| 5 | OCT3/4, D2-40 | — | family code |
| 6 | glypican-3 | OCT3/4 | `9071/3` |
| 7 | alpha-fetoprotein | OCT3/4 | `9071/3` |
| 8 | HNF1-beta | OCT3/4 | `9071/3` |
| — | fallback | | `9064/3` (D2) |

**Each rule must be verified against the printed page of a source on disk before it is
written**, and the page cited in the rule's `reason` or the node's `coding_note`: Siegmund 2022
(`Group 10 Papers/1-s2.0-S0046817722002040-main.pdf`), Wu 2020 (`s00383-020-04652-w.pdf`),
Rougemont 2018 (`1-s2.0-S0046817718301552-main.pdf`). Drop a rule no source supports and say so
in the report. Do not fetch anything. Choriocarcinoma is not coded from immunohistochemistry:
human chorionic gonadotropin stains syncytiotrophoblastic cells in seminoma too.

### 4.3 Site histology nodes

**`cn_histology`** (`histology_subclassification`), "What does the histology report call the
tumour?": germinoma → `9064/3`; mature teratoma → `9080/0`; immature teratoma → `9080/3`;
teratoma, maturity not stated → `9080/1`; dermoid cyst → `9084/0`; teratoma with somatic-type
malignancy → `9084/3`; embryonal carcinoma → `9070/3`; polyembryoma → `9072/3`; yolk sac tumour →
`9071/3`; choriocarcinoma → `9100/3`; mixed germ cell tumour → `cn_mixed`; germ cell tumour, type
not named, immunostains listed → `cn_ihc`; germ cell tumour, type not named, no immunostains →
`9064/3`; not a germ cell tumour → `refer(3)`. All basis 7.

**`ov_histology`**: dysgerminoma → `9060/3`; germinoma → `9064/3`; yolk sac tumour → `9071/3`;
embryonal carcinoma → `9070/3`; polyembryoma → `9072/3`; non-gestational choriocarcinoma →
`9100/3`; a teratoma, struma ovarii or strumal carcinoid → `ov_teratoma`; mixed germ cell tumour →
`ov_mixed`; gonadoblastoma → `ov_gonadoblastoma`; germ cell tumour, type not named, immunostains
listed → `ov_ihc`; germ cell tumour, type not named → `9064/3`; a sex cord–stromal tumour →
`ov_sex_cord`; an epithelial tumour — carcinoma, borderline tumour or cystadenoma →
`ov_epithelial`; small cell carcinoma, hypercalcaemic type → `8044/3`; malignant tumour, type not
determined → `ov_unspecified`; another tumour type → `ov_other`.

**`ts_histology`**: seminoma → `9061/3`; seminoma, anaplastic or with a high mitotic index →
`9062/3`; spermatocytic tumour → `9063/3`; embryonal carcinoma → `9070/3`; polyembryoma →
`9072/3`; yolk sac tumour, prepubertal or postpubertal type → `9071/3`; choriocarcinoma →
`9100/3`; epithelioid trophoblastic tumour → `9105/3`; placental site trophoblastic tumour →
`excl 9104/1` (D8); a teratoma, dermoid or epidermoid cyst → `ts_teratoma`; mixed germ cell
tumour → `ts_mixed`; germ cell neoplasia in situ only, no invasive tumour → `excl 9064/2` (D9);
gonadoblastoma → `ts_gonadoblastoma`; germ cell tumour, type not named, immunostains listed →
`ts_ihc`; germ cell tumour, type not named → `9064/3`; a sex cord–stromal tumour → `ts_sex_cord`;
carcinoma → `8010/3`; malignant tumour, type not determined → `ts_unspecified`; another tumour
type → `ts_other`.

**`eg_histology`**: germinoma → `9064/3`; seminoma → `9061/3`; a teratoma → `eg_teratoma`; yolk
sac tumour → `9071/3`; embryonal carcinoma → `9070/3`; polyembryoma → `9072/3`; choriocarcinoma,
gestational or not → `9100/3`; epithelioid trophoblastic tumour → `9105/3`; placental site
trophoblastic tumour → `excl 9104/1`; complete hydatidiform mole → `excl 9100/0`; partial
hydatidiform mole → `excl 9103/0`; invasive mole → `excl 9100/1`; mixed germ cell tumour →
`eg_mixed`; germ cell tumour, type not named, immunostains listed → `eg_ihc`; germ cell tumour,
type not named → `9064/3`; not a germ cell or trophoblastic tumour → `eg_other`.

### 4.4 Site-specific nodes

**`ov_teratoma`**: mature cystic teratoma → `excl 9080/0`; dermoid cyst → `excl 9084/0`; immature
teratoma, any grade → `9080/3`; teratoma, maturity not stated → `excl 9080/1`; teratoma or
dermoid cyst with a somatic-type malignancy → `9084/3`; struma ovarii → `excl 9090/0`; malignant
struma ovarii → `9090/3`; strumal carcinoid → `excl 9091/1`; a teratoma with a yolk sac tumour
or another malignant germ cell component → `ov_mixed`.

**`ts_teratoma`**: teratoma, prepubertal type → `excl 9084/0`; dermoid or epidermoid cyst →
`excl 9084/0`; teratoma, postpubertal type → `9080/3`; immature teratoma → `9080/3`; mature
teratoma, type not stated → `excl 9080/0`; teratoma, maturity and type not stated →
`excl 9080/1`; teratoma with a somatic-type malignancy → `9084/3`; with another malignant germ
cell component → `ts_mixed`.

**`eg_teratoma`**: mature teratoma → `excl 9080/0`; immature teratoma of the lung, thymus or
thyroid → `excl 9080/1`; immature teratoma at any other site — sacrococcygeal region,
mediastinum outside the thymus, retroperitoneum → `9080/3`; teratoma, maturity not stated →
`excl 9080/1`; dermoid cyst → `excl 9084/0`; teratoma with a somatic-type malignancy → `9084/3`;
with a yolk sac tumour or another malignant germ cell component → `eg_mixed`.

**`ov_gonadoblastoma`** / **`ts_gonadoblastoma`** (D10): gonadoblastoma alone → `excl 9073/1`;
mixed germ cell–sex cord-stromal tumour → `excl 8594/1`; with an invasive dysgerminoma,
seminoma or germinoma → the site family code; with an invasive yolk sac tumour → `9071/3`;
with an invasive embryonal carcinoma → `9070/3`; with an invasive mixed germ cell tumour →
`p_mixed`.

**`ov_sex_cord`** (D11): adult granulosa cell tumour → `8620/3`; juvenile granulosa cell tumour
→ `excl 8622/1`; Sertoli-Leydig cell tumour, poorly differentiated → `8631/3`; — poorly
differentiated, with heterologous elements → `8634/3`; — intermediate differentiation →
`excl 8631/1`; — intermediate, with heterologous elements → `excl 8634/1`; — well
differentiated → `excl 8631/0`; — retiform → `excl 8633/1`; — differentiation not stated →
`excl 8631/1`; Sertoli cell tumour → `excl 8640/1`; malignant Sertoli cell tumour or Sertoli
cell carcinoma → `8640/3`; Leydig cell tumour → `excl 8650/0`; malignant Leydig cell tumour →
`8650/3`; steroid cell tumour → `excl 8670/0`; malignant steroid cell tumour → `8670/3`;
thecoma → `excl 8600/0`; malignant thecoma → `8600/3`; gynandroblastoma → `excl 8632/1`; sex
cord tumour with annular tubules → `excl 8623/1`; microcystic or signet-ring stromal tumour →
`excl 8590/0`; sex cord-stromal tumour, type not stated → `excl 8590/1`.

**`ts_sex_cord`**: Leydig cell tumour → `excl 8650/1`; malignant Leydig cell tumour → `8650/3`;
Sertoli cell tumour → `excl 8640/1`; malignant Sertoli cell tumour → `8640/3`; large cell
calcifying Sertoli cell tumour → `excl 8642/1`; adult granulosa cell tumour → `excl 8620/1`;
juvenile granulosa cell tumour → `excl 8622/0`; Sertoli-Leydig cell tumour, poorly
differentiated → `8631/3`; mixed or unclassified sex cord-stromal tumour → `excl 8592/1`; sex
cord-stromal tumour, type not stated → `excl 8590/1`.

**`ov_epithelial`** (D14): small cell carcinoma, hypercalcaemic type → `8044/3`; low-grade
serous carcinoma → `8460/3`; high-grade serous carcinoma → `8461/3`; serous carcinoma, grade not
stated → `8441/3`; mucinous carcinoma → `8480/3`; mucinous cystadenocarcinoma → `8470/3`;
endometrioid carcinoma → `8380/3`; clear cell carcinoma → `8310/3`; seromucinous carcinoma →
`8474/3`; undifferentiated carcinoma → `8020/3`; adenocarcinoma, type not stated → `8140/3`;
carcinoma, type not stated → `8010/3`; serous borderline tumour → `excl 8442/1`; mucinous
borderline tumour → `excl 8472/1`; seromucinous borderline tumour → `excl 8474/1`; endometrioid
borderline tumour → `excl 8380/1`; serous cystadenoma → `excl 8441/0`; mucinous cystadenoma →
`excl 8470/0`.

**`ov_unspecified`** / **`ts_unspecified`** (D13): malignant neoplasm, type not determined →
`8000/3`; malignant tumour, small cell type → `8002/3`; giant cell type → `8003/3`; spindle
cell type → `8004/3`; clear cell type → `8005/3`. Basis 7.

**`ov_other`** / **`ts_other`** (`morphology_only`): lymphoma → `refer(2)`; leukaemic
infiltration → `refer(1)`; rhabdomyosarcoma or another sarcoma → `refer(9)`; a deposit of a
tumour that began elsewhere → `nonrep` ("code that tumour at its primary site"); another tumour
type the report names → `refer(12)`.

**`eg_other`** (`morphology_only`): a sarcoma → `refer(9)`; neuroblastoma → `refer(4)`;
lymphoma → `refer(2)`; a deposit of a tumour that began elsewhere → `nonrep`; another tumour
type the report names → `refer(12)`.

### 4.5 `g10_site_unstated`

`su_document_inventory` (`document_inventory`) carries the same five options and captures as
`p_document_inventory`, each going to `su_site_referral`, `su_site_markers`, `su_site_imaging`,
`su_site_cytology` or `su_site_histology`. Each of those is a `site_resolution` node, "Where is
the tumour?", hint "The topography was not recorded at Stage 1. Record it on the case as well.",
with four options capturing `{"gct_site": "cns" | "ovary" | "testis" | "other"}` and going by
cross-tree `next_node` to `cn_`, `ov_`, `ts_` or `eg_` + the same tier node (`clinical_alias`,
`markers`, `imaging`, `cytology`, `histology`). Labels: "Brain or spinal cord, including the
pineal and suprasellar regions"; "Ovary"; "Testis"; "Any other site — sacrococcygeal region,
mediastinum, retroperitoneum or elsewhere". No terminal in this tree.

After the tree is written, run the entries generator, then `python3 build/induce_flow.py`, and
confirm every `ihc_checklist` rule has a witness.

---

## 5. Validation rules this group adds (T4)

Registration in `build/build_database.py`:

- `GROUP10 = 10` after `GROUP8`, with the Group 8 comment style.
- `BEHAVIOUR_DECLARED_BY_GROUP[GROUP10] = {"3"}`, with a comment that ICCC-2017 ranges 94–99
  (Xa) also admit `0` and `1` and that rule 1 below enforces behaviour per site.
- `GROUP10` joins `ROUND_TRIP_GROUPS` (morphology_name is the ICD-O-3.2 preferred term).
- The four rules, each `if ctx.group != GROUP10: return []`, registered after the Group 8 block.

| # | Function | Asserts | Keyed off |
|---|---|---|---|
| 1 | `check_group10_codes_fit_site` | For each site tree, every emitted (code, behaviour) — code branches, IHC rules, `nos_fallback` — lies in a Group X ICCC range whose topography covers the tree's site and whose behaviour declaration includes the behaviour; every `behaviour_exclusion` lies in **no** such range; `g10_site_unstated` emits nothing | `ICCC-2017.sqlite` ranges 94–117 |
| 2 | `check_group10_no_pathology_codes` | On paths whose captured `evidence_tests` hold neither Histology nor Cytology: basis 1 and 2 emit only `8000/3`; basis 4 emits only `9064/3` or `9065/3`, or `9100/3` in `g10_extragonadal`, and only where the path's evidence holds both Imaging and Tumour markers; no such path reaches basis 5, 7 or 8 | the path (Group 8 `_group8_terminals_by_evidence`), Visser Table 4 |
| 3 | `check_group10_alias_terms_match_icdo32` | Every Group 10 alias equal (case-insensitive; tumour/tumor normalised) to an ICD-O-3.2 term maps to that term's code; the group emits that code at that term's behaviour and at no other (D21); no alias containing "germinoma" but not "dysgerminoma" maps to `9060` | `icdo32.sqlite` |
| 4 | `check_group10_subgroups_and_routing` | For every entry and every code in `topography_codes.json`, the subgroup `app.js` would show (`iccc3_subgroup_by_topography`, first match, else the entry's default) equals ICCC-2017's subgroup wherever ICCC places the pair in Group X at that topography; `groups["10"].tree_routing` sends every Xa topography to `g10_cns`, C56.9 to `g10_ovary`, C62.x to `g10_testis`, every Xb topography to `g10_extragonadal`, and defaults to `g10_site_unstated` | `ICCC-2017.sqlite`, router, topography lookup |

`build/negative_controls_group10.py` (modelled on `negative_controls_group08.py`): a
correct-data probe per rule, then at least these mutations, each expected CAUGHT:

| Control | Mutation |
|---|---|
| R1-A | `cn_histology` mature teratoma becomes `excl 9080/0` |
| R1-B | `ov_teratoma` mature cystic teratoma emits code `9080/0` |
| R1-C | `ts_mixed` gains a `9086/3` branch (ICCC-2017 range 105: Xb6 only) |
| R1-D | `eg_mixed` gains a `9102/3` branch |
| R1-E | `su_site_histology` gains a code branch |
| R2-A | `cn_markers` alpha-fetoprotein option emits `9071/3` basis 4 |
| R2-B | **the path, not the flag:** `ov_document_inventory`'s histology option captures `["Imaging"]` |
| R2-C | the markers option of `eg_document_inventory` captures `["Tumour markers"]` only |
| R2-D | `ts_imaging` emits `9061/3` at basis 2 |
| R3-A | an alias "Germinoma" maps to `9060` |
| R3-B | an alias "Mature teratoma" maps to `9080` |
| R3-C | an alias "Germ cell neoplasia in situ" maps to `9064` |
| R4-A | `9071/3` loses its Xa rule |
| R4-B | `C62.0` moves to the ovary routing rule |
| R4-C | `C76.3` is dropped from the extragonadal routing rule |

Record the run in `docs/validator_negative_controls.md` as `# Group 10 — Germ Cell,
Trophoblastic and Gonadal Tumours (4 October 2026)`, Group 8's format.

---

## 6. The alias layer (T5)

`build/generate_group10_aliases.py`, modelled on `generate_group08_aliases.py`; writes
`data/aliases/aliases_group_10.json`, same schema. Sources, first wins on the same string:

1. ICD-O-3.2 terms (preferred, synonym, related; not `[obs]`) of every pair the tree emits,
   **subject to D21**: a term is used only if the group emits its code at the term's behaviour
   and at no other. `9080` and `9084` get no ICD-O term aliases.
2. `x_morph` strings that differ from the preferred term **and** are ICD-O-3.2 terms at an
   emitted pair (e.g. "Yolk sac tumor" → `9071`; "Granulosa cell tumor, adult type" → `8620`).
   A REDCap string naming a benign or in situ term is not aliased.
3. Curated: the British spellings and WHO names the tree uses — "Yolk sac tumour",
   "Endodermal sinus tumour", "Germ cell tumour, NOS" → `9064`, "Non-germinomatous germ cell
   tumour" → `9065`, "Mixed germ cell tumour" → `9085`, "Teratoma" → `9080`, `9084`,
   "Teratoma, postpubertal type" — **not** (it is true of `9080/3` only, D21), "Yolk sac tumour,
   prepubertal type" → `9071`, "Small cell carcinoma of the ovary, hypercalcaemic type" → `8044`,
   "Low-grade serous carcinoma" → `8460`, "High-grade serous carcinoma" → `8461`, "Adult
   granulosa cell tumour" → `8620`, "Sertoli-Leydig cell tumour, poorly differentiated" →
   `8631`, "Epithelioid trophoblastic tumour" → `9105`, "Spermatocytic tumour" → `9063`.

Not aliased: "GCT" (germ cell or granulosa cell — the Alias Build Instructions' own collision),
any excluded-behaviour term (D9, D10, D11). Before writing, check `data/aliases/alias_index.json`
for strings another group holds; an alias shared with a lower-numbered group enters that group.
`tree_entry_node` is `su_document_inventory`, `ihc_tree_id` `g10_site_unstated`.

---

## 7. Shared-layer changes and the Group 9 branch

| File | Group 10 change | Group 9 touches |
|---|---|---|
| `presentation_router.json` | `groups["10"]`; one `8000-8005` branch | `groups["9"]` (three lines above `"10"`), `lymphadenopathy`, `site_to_group` C69/C77, deletes `9473` |
| `topography_codes.json` | C62.0, C62.1, C76.3; candidate groups of C38.1, C38.3, C48.0; gonad row label | inserts at C49.9→C74.0 and after the C48 crosswalk row |
| `build_database.py` | `GROUP10`; behaviour row; `ROUND_TRIP_GROUPS`; four rules after Group 8's | `GROUP9`; the old `(GROUP3, GROUP4, GROUP6)` guards; its checks after Group 6's |
| `docs/clinical-warnings.md`, `docs/codes-awaiting-redcap.md`, `docs/TODO.md`, `docs/group_baseline_documents.md` | append sections | appends at the same anchors |

The doc conflicts are append-only on both sides: keep both on merge. Rebuild
`alias_index.json` after merging either branch.

---

## 8. Docs (T6)

- `docs/clinical-warnings.md`: a `# Group X` section holding the pathway's alert strings (§5,
  §4A–§4G): midline marker alert, neonatal alpha-fetoprotein, mild human chorionic gonadotropin
  in germinoma, gonadoblastoma and Y-chromosome material, germ cell neoplasia in situ, the 9100
  behaviour trap, small cell carcinoma of the ovary hypercalcaemic type with BRG1 retained, DICER1
  and Sertoli-Leydig cell tumour, Klinefelter syndrome and mediastinal germ cell tumour.
- `docs/group_10_layer1_repair.md`: Group 8's format. Every `x_morph` option classified against
  ICD-O-3.2 (exact preferred term at an emitted behaviour; valid term not preferred; drift; a
  benign or borderline term at a number the tool emits at `/3`; "Label not found"; numbers
  absent). The three sharpest first: `9064`, `9100`, `9086`.
- `docs/codes-awaiting-redcap.md`: `## Group 10 — open`, one `### NNNN/B — Name` per
  `awaiting_layer1` entry, matching T1's output exactly.
- `docs/TODO.md`: §27 "Group X codes the REDCap dropdown does not offer correctly", a §7 index
  row, the footer note; and the Group III inbound defects (D18) as an open item.
- `docs/group_baseline_documents.md`: Group X row and a provisional-table row — Höhn 2021 does not
  cover the ovary (D22); Moch 2022 Table 3 is the testis baseline; Pfister 2022 Table 3 and Louis
  2021 Table 1 used for entity currency. Status line: Group 10 built, awaiting merge.
- `docs/sources-requested.md`: McCluggage 2022 (D22).

---

## 9. Proof before this group is called done (T7)

1. `python3 build/build_database.py` → 0 FAIL.
2. `python3 build/induce_flow.py --check` → every rule has a witness.
3. `python3 build/negative_controls_group10.py` → every control CAUGHT, every probe passes.
4. `node build/check_engine_flow.mjs` → pass.
5. Drive in the browser (`python3 -m http.server 8811`): a pineal tumour found by search
   ("germinoma") through `g10_site_unstated` to `9064/3`; an ovarian mature cystic teratoma to its
   behaviour exclusion; a central nervous system mature teratoma to `9080/0`; a sacrococcygeal
   immature teratoma to `9080/3` Xb2; a testicular mixed tumour with choriocarcinoma to `9101/3`;
   the markers route to `9065/3` basis 4; an adult granulosa cell tumour of the ovary to `8620/3`.
   On each output read the subgroup line and the "Also called" row.
6. Groups 1–8 data and alias files, `app.js`, `index.html`, `uccf-tool.css` byte-identical to
   `main`.

---

## 10. Tasks

- [ ] T1 `build/generate_group10_entries.py` → `group_10_dt.json` entries and metadata (stub tree)
- [ ] T2 `build/group10_tree.py`, the five trees; regenerate; `induce_flow.py`
- [ ] T3 router and topography (§3)
- [ ] T4 `build_database.py` registration, the four §5 rules, `negative_controls_group10.py`
- [ ] T5 `aliases_group_10.json`
- [ ] T6 docs (§8)
- [ ] T7 build, negative controls, engine gate, browser drive
- [ ] T8 `docs/group_10_build_report.md`; `docs/group_10_registrar_review.md` complete
