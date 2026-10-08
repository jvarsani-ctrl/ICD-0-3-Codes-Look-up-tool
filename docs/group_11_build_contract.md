# Group 11 build contract — Other malignant epithelial neoplasms and malignant melanomas

**Branch:** `claude/group-11-carcinomas`, a worktree at `.claude/worktrees/group-11-carcinomas`,
cut from `main` at `7025128` (Groups 1–10 merged, the Group 10 audit fixes of PR 14, the
registrar's obsolete-code ruling of 8 October 2026).

**Written 8 October 2026, before any JSON was authored.** The registrar ruled the same day that the
Group 11 diagnostic pathway is built directly into the tool, without a Diagnostic Pathway document
in the vault first, under six rules:

1. Every paper is converted to text, one file per paper, marked for its cancer; tables are read
   from the PDF page image.
2. An agent reads a paper only as snippets: a search for the cancer, about 30 lines either side.
3. Each agent uses only the text files its part needs.
4. If the data is insufficient, only the controlling session fetches more.
5. The pathway follows the WHO ICD-O-3 coding Rules A to K.
6. Conflicts with other groups are handled as Group 10 handled them, with Group 10's lessons
   applied from the start.

The evidence behind every screen is in `docs/group_11_evidence/` (one JSON and one Markdown file
per part, every claim with its file, PDF page and a quotation a checker script found on that page).
The text files are in the vault at `Group 11 Papers/text/` (`INDEX.md` lists them). Everything that
needs the registrar goes to `docs/group_11_registrar_review.md`.

> **Standing rule, inherited.** The tool must never overstate its evidence. Group XI has three
> sharp instances. Thirteen REDCap codes carry a malignant label on a number whose every
> malignant ICD-O-3.2 term is `[obs]` (`8130` *Papillary transitional cell carcinoma* among
> them). REDCap labels `8504` *Intracystic carcinoma, NOS*, which ICD-O-3.2 moved to `/2`.
> And `8335` *Follicular carcinoma, encapsulated* is `/1` in ICD-O-3.2: only the minimally
> invasive tumour stays `8335/3`.

---

## 0. Pre-context

### 0.1 ★ The ICCC-3 definition, read off `ICCC-2017.sqlite`

`code_ranges` for `main_group = 'XI'`, ranges 118–136, all behaviour `3`:

| Range | Subgroup | Histology | Topography (REDCap 3-digit) |
|---|---|---|---|
| 118 | XIa adrenocortical carcinomas | `8158` | `740` (C74.0 only) |
| 119 | XIa | `8370-8375` | `000-809` (any site) |
| 120 | XIb thyroid carcinomas | the carcinoma list (8010–8041, 8050–8075, 8082, 8120–8122, 8130–8141, 8158, 8190–8246, …) | `739` |
| 121 | XIb | `8330-8332, 8334-8337, 8340-8347, 8350, 8588` | `000-809` (any site) |
| 122 | XIc nasopharyngeal carcinomas | the carcinoma list with 8083, 8500–8576 | `110-119` |
| 123 | XId malignant melanomas | `8720-8780, 8790` | `000-809` (any site) |
| 124 | XIe skin carcinomas | the skin list (8090–8110 basal cell and adnexal, 8247, 8390–8420 …) | `440-449, 519, 609, 632` |
| 125–133 | XIf1 salivary · XIf2 colon and rectum · XIf3 appendix · XIf4 lung · XIf5 thymus · XIf6 breast · XIf7 cervix · XIf8 bladder · XIf9 eye | **one shared list of 174 codes** | `079-089` · `180, 182-189, 199, 209, 210-218` · `181` · `340-349` · `379` · `500-509` · `530-539` · `670-679` · `690-699` |
| 134 | XIf10 other specified sites | the shared list | `000-069, 090-109, 129-179, 239-339, 380-399, 480-488, 510-518, 529, 540-559, 570-608, 619, 630-631, 637-639, 659-669, 680-689, 700-729, 750-759` |
| 135 | XIf10 | `8158, 8290` only | `000-069, 090-109, 129-179, 239-339, 380-399, 480-488, 510-529, 540-559, 570-619, 630-639, 659-669, 680-689, 750, 752-759` (takes C51.9, C60.9, C63.2; leaves out C70–C72 and C75.1) |
| 136 | XIf11 unspecified site | the shared list | `760-768, 809` |

What follows:

1. **XIf1 to XIf11 differ only by site.** One (code, behaviour) pair sits in up to eleven
   subgroups, so every shared-list entry carries `iccc3_subgroup_by_topography` (Group 10's D16
   and D20 shape) and is one entry.
2. **Melanoma, the adrenocortical carcinoma codes and the thyroid-specific codes are Group XI at
   every site.**
3. **No Group XI carcinoma range covers** the liver (C22, Group VII), the kidney (C64, Group VI),
   the ovary and testis (C56, C62, Group X), bone (C40–C41),
   marrow (C42), soft tissue (C47, C49) or lymph nodes (C77). A carcinoma recorded there is not a
   Group XI code: §3 says where each goes. *(Corrected after the build, 8 October 2026: the first version also listed the pituitary,
   C75.1. Range 134 takes C75.1 (`750-759`); only range 135 leaves it out. C75.1 is not routed by a
   Group XI rule and reaches the default tree, `docs/TODO.md` §35.5.)*
4. **XIf10 (range 134) includes the brain and spinal cord (C70–C72) and the other endocrine glands** (C75.0,
   C75.2–C75.9). Range 135 (`8158`, `8290`) does not take C70–C72; there those two codes show XIf10 only as the D11 default. A carcinoma in the brain is a deposit in nearly every case and is coded at its
   primary.
5. **XIe takes three genital skin sites**: C51.9 vulva NOS, C60.9 penis NOS and C63.2 scrotum.

### 0.2 ★ The inventory — 229 usable codes, 230 entries

`build/generate_group_inventory.py --group XI`, 8 October 2026:

```
ICCC range entries 4358 · distinct codes 483 · absent from ICD-O-3.2 254 · usable 229 · (code,behaviour) records 2183
```

2,183 records collapse to **229 distinct (code, behaviour) pairs**, all `/3`. Add **`8339/3`**
*Follicular carcinoma, encapsulated, angioinvasive* (C73.9), new in ICD-O-3.2 and outside every
ICCC range; standing rule 3 places it in the group that offers it, XIb by site: **230 entries.**
The other 43 ICD-O-3.2 `/3` codes in 8010–8790 that no Group XI range holds belong to Groups III
(8270–8300 pituitary), IV (8680–8714), VI (8311–8319), VII (8160–8180) and X (8474, 8600–8670).

Of the 229, **eleven have no current malignant term** (every `/3` term `[obs]`): 8042, 8124,
8130, 8141, 8245, 8251, 8350, 8440, 8450, 8508, 8512. They are entries and are never on a screen
(D-OBS below).

### 0.3 What ICD-O-3.2 changed in this group

From `ICD Look Up tool/Group 11 — ICD-O-3.2 Code Currency Check 2026-10-08.md`, which the
registrar ruled must be carried into the pathway (8 October 2026):

| Change | Section of the currency check | What the tree does |
|---|---|---|
| No code in the group was deleted | §1 | nothing |
| Thirteen REDCap codes have no current malignant term; 8042/3 too (ICCC only) | §2 | off every screen; the WHO source names the current entity on the stem where one exists (§4 per tree) |
| `8335` encapsulated follicular carcinoma `/3`→`/1`; minimally invasive stays `8335/3`; `8339/3` angioinvasive new | §3 | the thyroid tree asks invasion and separates the three |
| `8504` `/3`→`/2`; `8504/3` is now *Encapsulated papillary carcinoma with invasion* | §3 | breast: the in situ term is an exclusion |
| `8240/1`→`8241/3`; `8242/1`→`/3`; `8150–8158` `/1`→`/3`; `8151` `/0`→`/3` | §3 | neuroendocrine tumours code `/3` |
| `8580–8585` thymoma `/1`→`/3` | §3 | thymoma types are Group XI codes |
| `8408/1`→`8408/3` *Digital papillary adenocarcinoma* | §3 | skin |
| `8452/3` pancreas only; ovary stays `8452/1` | §3 | the pancreas option codes `8452/3`; the ovary is Group X |
| `8336` `/0`→`/1`; `8103` `/0`→`/1` | §3 | exclusions |
| 62 REDCap labels that are not the ICD-O-3.2 preferred term | §4 | the REDCap-side list (`docs/group_11_layer1_repair.md`); the tool shows the ICD-O-3.2 term |
| 50 REDCap options with no malignant form (adenomas 8371–8375 among them) | §5 | exclusions where the clerk meets them; the REDCap-side list |
| New codes REDCap lacks: 8023, 8054, 8085, 8086, 8256, 8257, 8339, 8474, 8509 | §6 | built where a tree offers them; the REDCap-side list (standing rule 16) |
| ICCR prints `8483` and `8484`, which ICD-O-3.2 lacks | §7 | registrar; not built |

### 0.4 Engine facts that shape every node

Unchanged from Group 10 build contract §0.4. In short:
- `when` is string equality.
- `resolution_logic[]` is flat and first-match-wins.
- `clinical_alert` is `null` everywhere (ruling 9).
- A NOS fallback is required on `ihc_checklist` and `numeric_gate`, and forbidden (explicit `null`) on every other type used here.
- `refer_group` carries no code.
- `behaviour_exclusion.icdo_term` is the ICD-O-3.2 **Preferred** term at its (code, behaviour).
- Cross-tree `next_node` is legal.
- Router `tree_routing` entries must be `document_inventory` nodes, one entry node per tree: no group routes two rules into one tree.
- `app.js` *replaces* a captured `evidence_tests` list rather than merging it, so each evidence context needs its own node (Group 10 report §7 item 1).
- A referral that names a deposit asks for the primary's site (`recapture_site`).
- A leukaemia referral records C42.1, and an unknown primary C80.9.
- The search box asks the site of a group with `tree_routing`, and keeps the group only if the site lists it. A group marked `occurs_at_routed_sites` is also kept at any site its own routing names.
- "Also called" lists aliases by four-digit code (Group 10 D21).

### 0.5 Visser 2023 — what may be registered without tissue

Visser O, et al. Front Oncol 2023;13:1250549 (`docs/references/visser-2023-key-points.md` §5):

- **Table 3, p. 04–05:** melanoma of the skin on clinical information, basis 1, C44: `8720/3`.
- **Table 4, p. 06,** basis 4, with a clinical investigation that shows the tumour:
  - medullary thyroid carcinoma with calcitonin: `8345/3`;
  - neuroendocrine tumour with chromogranin A: `8240/3`;
  - functioning tumours: insulin `8151/3`, glucagon `8152/3`, gastrin `8153/3`, vasoactive intestinal peptide `8155/3`, somatostatin `8156/3`, serotonin `8241/3`, adrenocorticotropic hormone `8158/3`.
- **Rule 4 (p. 03):** "possible" is not registrable.
- **Rule 5:** otherwise `8000/3`.
- **Rule 6:** basis 4 never stands alone.

Read from the page image of Table 4 (PDF p. 6) on 8 October 2026. Three rows that
`visser-2023-key-points.md` §5 leaves out bear on Group XI. Colorectal cancer with carcinoembryonic
antigen, pancreatic and gallbladder or bile duct cancer with cancer antigen 19-9, and prostate cancer
with prostate-specific antigen each give **`8000/3`** at basis 4, not a specific code. ICCC-2017
places `8000/3` in XIIb at those sites. So, as Group 10 did with `8000/3`, the tissue-free route there
refers to Group XII. The table has **no adrenal cortical row**. Its adrenocorticotropic hormone line
belongs to "functioning neuroendocrine tumours (excluding pituitary gland tumours)" (`8158/3`), and
the adrenal cortex tree therefore offers no marker route. The chromogranin A row (`8240/3`) names no
site.

### 0.6 The tree structure (registrar, 8 October 2026: approach 3)

- **Organ trees** where the WHO classification is organ-specific: adrenal cortex, thyroid,
  nasopharynx, salivary gland, lung, thymus, colorectum with appendix.
- **One melanoma tree** that every site reaches.
- **One general carcinoma tree** for skin and the short-tree sites. It is written once, as Group 10
  wrote its site trees once (`build/group10_tree.py`, functions parameterised by site), and
  instantiated per site family, because the router gives each tree one entry node.
- **The subgroup is computed from the site at output** (`iccc3_subgroup_by_topography`), so each
  (code, behaviour) is one entry.

### 0.7 Decisions (D-numbers) — defaults the build applies; each open one is in the registrar review

The evidence agents raised 140 questions for the registrar
(`docs/group_11_registrar_review.md`). Most belong to a few classes. The build applies one default per
class, in the way Group 10 applied D1–D22, and lists every instance for the registrar.

| # | Decision | Source |
|---|---|---|
| D1 | **An option is an entity a source reports at ages 0–18** (Pfister 2022 Table 3, the WHO summaries, the paediatric papers fetched on 8 October 2026). **Any other current `/3` code valid at the site is a picker entry.** Exception: an entity whose code depends on a further answer (invasion, subtype, grade, HPV status, behaviour) is an option wherever it occurs, because the picker cannot ask the question. | registrar, 8 October 2026 ("Picker, as in Group 10") |
| D2 | **The picker** is Group 10's gonadal carcinoma picker (`prefill_filter_from_search`, option `search_terms` = live ICD-O-3.2 synonyms and related terms). It is one `histology_subclassification` node per tree. It lists every code ICCC-2017 places in Group XI at the tree's routed sites, plus the codes standing rule 3 places there (§2). It excludes the eleven all-`[obs]` codes and the codes the tree already offers as options. | Group 10 build report §4; registrar review A11 |
| D3 | **All-`[obs]` codes stay off every screen** (8042, 8124, 8130, 8141, 8245, 8251, 8350, 8440, 8450, 8508, 8512). They are entries, never emitted. Where the WHO source names the current entity on the stem, the tree offers that entity's current code. Examples: goblet cell adenocarcinoma `8243/3`, not adenocarcinoid `8245/3`; the diffuse sclerosing subtype of papillary thyroid carcinoma `8260/3`. A code whose Preferred term is `[obs]` but which has a live synonym (`8551`, `8780`) is held off screen too, as Group 10 rule 7 does, and goes to the registrar. | registrar, 8 October 2026 (Group 10 A11); currency check §2 |
| D4 | **A code the WHO or ICCR prints that ICD-O-3.2 lacks is not built.** Examples: 8483, 8484, 9113, 8976, 8750, 8770/1, 8743/2, thyroblastoma, differentiated high-grade thyroid carcinoma with no dominant type, thoracic SMARCA4-deficient undifferentiated tumour on 8044. No screen names the entity. A report that names it reaches the nearest generic option the screen offers (adenocarcinoma, carcinoma, the parent entity). The registrar review lists each one. | standing rule 2; currency check §7 |
| D5 | **Rule K (higher code) applies only when no single code covers every term.** When the report names a WHO entity whose one code covers its features (NUT carcinoma with squamous features `8023/3`; a WHO subtype code), the entity's code is recorded. Where a screen offers two modifiers that no single code covers, the hint states the Rule K choice, as the registrar ruled on 7 October 2026. The instances the agents found (thyroid, salivary, thymus, breast, urinary, oropharynx, functioning neuroendocrine tumour with a grade) are listed for the registrar. | ICD-O-3.1 §4.3.8, p. 24–26; registrar 7 October 2026 |
| D6 | **Rule F stated behaviour is not built where ICD-O-3.2 prints the term only below `/3`.** Examples: a hyalinizing trabecular tumour called malignant; a sialoblastoma called malignant; a solid pseudopapillary neoplasm called benign. The tree records ICD-O-3.2's printed behaviour, and the instance goes to the registrar with Group 10's open items A1, A6 and A10. | registrar's open policy, Group 10 review |
| D7 | **No tissue, or no tumour type:** `8000/3` and `8001/3`–`8005/3` sit in ICCC XIIb at every Group XI site. Each tissue-free or type-free route refers to Group XII with `refer_code`, as Group 10 did. There is one exception. ~~Melanoma of the skin on clinical evidence records `8720/3` at basis 1 (Visser Table 3).~~ Withdrawn 8 October 2026: the registrar ruled for the paediatric source (review A8, E9; Ferrari 2021, PDF p. 3, excisional biopsy required). The Visser Table 4 marker codes (`8345/3`, `8240/3`, `8151–8156/3`, `8241/3`, `8158/3`) record at basis 4, only with imaging that shows the tumour and only in the trees whose sites the marker concerns. | Visser 2023 rules 4–6, Tables 3–4; Group 10 D-tissue-free |
| D8 | **Cytology that names an entity records it at basis 5**; cytology that is suspicious or "favours" an entity is not registrable (Visser rule 4, "possible"). | Visser 2023 rule 4 |
| D9 | **Rule H corrects the site through a `site_resolution` node that captures `topography`,** the Group III pattern (`pf_subsite`, `md_compartment`). Examples: an adrenal cortical carcinoma recorded at C74.9 becomes C74.0; a thymic epithelial tumour reported in the anterior mediastinum becomes C37.9; carcinoma of the "skin of the arm" becomes C44.6. The node appears only where an agent's evidence names a site-associated term. | ICD-O-3.1 §4.3.5, p. 23–24; Rule A p. 16–17 |
| D10 | **A deposit asks where the primary is.** Each tree's `*_deposit` node follows Group 10's `n_deposit`: one option per primary family, `refer_group` with `recapture_site: true`. A carcinoma or melanoma primary refers to Group 11 itself with `recapture_site: true`, so the case re-enters at the primary's site. A leukaemia records C42.1; an unknown primary records C80.9. | Group 10 build report §4; audit 7 October 2026 |
| D11 | **Subgroup where ICCC names none.** A code standing rule 3 keeps in Group XI at a site no XI range covers takes the entry's default subgroup. For a shared-list code that is XIf10: 8010/3 or 8023/3 at the adrenal, bone or soft tissue. ICCC's own range 136 already gives the shared list XIf11 at C76.x and C80.9. A code with one ICCC subgroup keeps that subgroup at every site, because its term implies its site (Rule H): the 19 skin-only codes such as `8090` take XIe, and `8339/3` takes XIb. The registrar review lists them. *(Amended after T1, 8 October 2026: the first version said XIf11 at C76.x and C80.9 for every rule-3 code, which contradicted the one-subgroup instruction in §2.)* | standing rule 3; ICD-O-3.1 Rule H; Group 10 lesson "the subgroup line at a site outside every range" |
| D12 | **NUT carcinoma (`8023/3`)** is an option on every tree whose site a source reports it at (nasal cavity, nasopharynx, salivary gland, lung, thymus and mediastinum, skin). It is a picker entry elsewhere. The tree records the site the report gives (C37.9 only when the report names the thymus). The registrar review holds C37.9 versus C38.x. | NUT evidence; Marx 2022 |
| D13 | **Melanoma** is reached from every tree's histology screen by a cross-tree `next_node` into `g11_melanoma`. The melanoma tree has a `document_inventory` entry node so that the router may list it, and no routing rule names it. | approach 3; `app.js` `findNode` |
| D14 | **Tree families.** The general carcinoma tree is written once (`build/group11_template.py`) and instantiated per site family, because the engine cannot filter options by site inside one tree. Where one family covers several organs, the histology screen groups options by organ, with the organ named in the label. | approach 3; §4.1 |
| D15 | **Basis of diagnosis:** clinical 1, imaging 2, marker 4, cytology 5, histology 7, immunohistochemistry 7, a gene test specific to the entity 8 (`basis_of_diagnosis_declarations` `{"ihc_counts_as": 7, "methylation_counts_as": 8}` as Group 10). | Visser 2023 |
| D16 | **The 8158/3 adrenal question:** `8158/3` (*ACTH-producing tumor*) is off the adrenal cortex screens, because Visser's adrenocorticotropic hormone row concerns functioning neuroendocrine tumours. ICCC range 118 keeps it in the inventory at C74.0. | Visser Table 4; adrenal evidence |

---

## 1. Files this build creates or changes

| File | Kind | Task |
|---|---|---|
| `build/generate_group11_entries.py` | new — entries, metadata, writes the dt.json | T1 |
| `build/group11_common.py` | new — helpers (`code`, `go`, `refer`, `excl`, `nonrep`, `aid`, `node`), the evidence gate, the tissue-free, cytology, deposit and picker node builders | T2a |
| `build/group11_families/*.py` | new — one module per site family (D14) | T2b |
| `build/group11_organs/*.py` | new — one module per organ tree and the melanoma tree | T2c |
| `build/group11_tree.py` | new — `trees()` assembles every module in §4.1 order | T2d |
| `data/database/group_11_dt.json` | generated | T1, T2 |
| `docs/evidence_documents/group_11.json` | new — the evidence-checklist rules per gate (Group 10's format, `build/apply_evidence_documents.py`) | T2 |
| `data/shared/presentation_router.json` | edit — `groups["11"]`; `dual_group_rules` 8158 and 8290 checked | T3 |
| `data/shared/topography_codes.json` | edit — the missing Group XI lookup codes; 11 in `candidate_groups` | T3 |
| `build/build_database.py` | edit — registration and the Group 11 rules (§5) | T4 |
| `build/negative_controls_group11.py` | new | T4 |
| `build/check_engine_flow.mjs` | edit — generalise the picker sweep to every `prefill_filter_from_search` node (cross_group_B) | T4 |
| `build/generate_group11_aliases.py`, `data/aliases/aliases_group_11.json` | new | T5 |
| `data/aliases/alias_index.json` | regenerated by the build, committed (rule 15) | T7 |
| `docs/group_11_registrar_review.md`, `docs/group_11_layer1_repair.md`, `docs/TODO.md`, `docs/clinical-warnings.md`, `docs/group_baseline_documents.md`, `docs/sources-requested.md`, `docs/validator_negative_controls.md` | docs | T6 |
| `docs/group_11_build_report.md` | docs | T8 |

`app.js`, `index.html` and `uccf-tool.css` stay byte-identical to `main`. Another group's data file
changes only where §7 says so.

Environment for every command in the worktree:

```bash
export ICD_LAYER1="/Users/jay/Ai Environment/Cancer Registry/ICD coding"
export ICCC_DB="/Users/jay/Ai Environment/Cancer Registry/ICCC-2017.sqlite"
export ICDO_DB="/Users/jay/Ai Environment/Cancer Registry/ICD coding/ICD-O-3.2/icdo32.sqlite"
```

Run order (cross_group_B; Group 10 traps):
1. `generate_group11_entries.py`
2. `induce_flow.py`
3. `generate_group11_aliases.py`
4. `generate_group10_aliases.py`, because its rule 8 reads the other groups' aliases
5. `build_database.py`, which rewrites `alias_index.json`
6. commit `alias_index.json`

---

## 2. Entries — `build/generate_group11_entries.py` (T1)

Modelled on `build/generate_group10_entries.py`. It reads `ICCC_DB` and `ICDO_DB` from the environment first.

1. `gi.build_inventory(ICCC_PATH, ICDO_PATH, "XI")` gives 2,183 records. Group them by (code,
   behaviour) into 229 entries, and add `8339/3` (standing rule 3, D11). Assert 2,183 records and
   230 entries.
2. `morphology_name` is the ICD-O-3.2 **Preferred** term at the entry's behaviour.
3. **Subgroup.** A pair in one subgroup takes that subgroup, with `topography_dependent: false`.
   A pair in more than one takes `topography_dependent: true`, a `topography_routing_note` and
   `iccc3_subgroup_by_topography`. That field holds one rule per subgroup, listing every code in
   `topography_codes.json` (after T3's additions) that falls in that subgroup's ICCC topography.
   Compute the lists from the ICCC range strings and never type them. The entry's own
   `iccc3_subgroup_id` is the default: XIf10 for the shared list, the only subgroup otherwise,
   XIb for `8339/3` (D11).
4. `primary_sites`: the ICCC topography of each subgroup, one range per item, written with ASCII
   hyphens. The engine gate's `covers()` splits on `-` (cross_group_B, Group 10 lesson).
5. `who_version`: "ICD-O-3.2"; annotations may name the WHO volume a part cites.
6. **Annotations** keyed by `code/behaviour` for every pair a tree emits:
   - `diagnostic_tests_required`;
   - `ihc_markers_required` where an immunohistochemistry rule uses them;
   - a `coding_note` naming the D-number, the evidence file and the node or nodes that emit the pair.

   A pair the tree never emits gets the templated note "In the inventory, not on the tree…". The
   eleven `[obs]` pairs say so (D3).
7. **No REDCap fields** (standing rule 16). What REDCap owes goes to `docs/group_11_layer1_repair.md` and `docs/TODO.md` §7.
8. `metadata`:
   - `group_id` 11, `group_name` "Other Malignant Epithelial Neoplasms and Malignant Melanomas";
   - `iccc3_version`, `icdo_version`, `total_morphology_entries` 230, `total_decision_nodes`;
   - `decision_trees` (the §4.1 order);
   - `basis_of_diagnosis_declarations` (D15).
9. `carry_branch_sequences`, as Group 10, so `induce_flow.py` output survives regeneration. It applies `docs/evidence_documents/group_11.json` as Group 10 does.
10. `--check` writes nothing and exits non-zero if the file would change.

---

## 3. Shared layer — router and topography (T3)

### 3.1 `data/shared/topography_codes.json`

- **C44.4 and C48.1 are not added.** `Topography Redcap.md` has neither C44.4 (skin of scalp and neck) nor C48.1 (specified parts of peritoneum), so the lookup cannot carry a REDCap code for them. They go on the REDCap-side list in `docs/TODO.md` §7 and `docs/group_11_layer1_repair.md` (T1 finding). 153 codes are added.
- **Add every Group XI lookup code that is missing.** Read the REDCap three-digit list in
  `ICD coding/RedCap Options/Topography Redcap.md`, and take each code that falls in a Group XI
  ICCC topography range and that §4.1 routes. That covers the salivary glands C07–C08, colon and
  rectum C18–C21, breast C50, lip and oral cavity C00–C06, and the rest cross_group_A lists (155
  missing codes in all). Labels and REDCap codes come from that file; never type them. Insert each
  beside its numeric neighbours. Each new code takes `candidate_groups: [11]` and a crosswalk row
  matching its organ. Where the crosswalk has no row for the organ, add one with a plain label.
- **Add 11 to `candidate_groups`** of each existing lookup code in a routed Group XI range that
  lacks it (65 codes; cross_group_A). Among them: C74.0, C69.0–C69.9, C30.0–C31.9, C38.1–C38.3,
  C70–C72 and C48.
- Leave every other field unchanged.

### 3.2 `data/shared/presentation_router.json`

`groups["11"]`:
- `built: true`;
- `occurs_at_routed_sites: true` (Group 10's flag; not `occurs_at_any_site`);
- `trees` in §4.1 order;
- `tree_routing`, one rule per routed tree. Each rule's `topography_in` is computed from §4.1 against the lookup after §3.1, never typed. The `entry_node` is the tree's `document_inventory` node;
- `default`: `g11_unspecified`, label "Another or unspecified site", with the reason "every lookup code that lists Group 11 is named by a rule; app.js requires a default";
- `handoff`: `{"group": 11, "tree_id": "g11_unspecified", "entry_node": "un_document_inventory"}`.

`dual_group_rules`: read the `8158` and `8290` rules. Make each resolve to ICCC's subgroup at
C74.0 and C73.9, and leave the kidney branch of `8290` to Group III's owner (cross_group_A). Touch
no other rule.

---

## 4. The trees (T2)

### 4.1 Trees, prefixes, routed sites and their evidence

| Tree | Prefix | Routed topography | Evidence file(s) |
|---|---|---|---|
| `g11_adrenal` | `ad_` | C74.0, C74.1, C74.9 | `XIa_adrenal_cortex` |
| `g11_thyroid` | `th_` | C73.9 | `XIb_thyroid` |
| `g11_nasopharynx` | `np_` | C11.0–C11.9 | `XIc_nasopharynx` (nasopharynx nodes) |
| `g11_salivary` | `sg_` | C07.9, C08.0–C08.9 | `XIf1_salivary` |
| `g11_colorectal` | `cr_` | C18.0, C18.2–C18.9, C19.9, C20.9, C21.0–C21.8 | `XIf2_XIf3_digestive` (colorectal nodes) |
| `g11_appendix` | `ap_` | C18.1 | `XIf2_XIf3_digestive` (appendix nodes) |
| `g11_lung` | `lu_` | C34.0–C34.9 | `XIf4_lung_pleura` (lung nodes) |
| `g11_thymus` | `ty_` | C37.9, C38.1, C38.2, C38.3 | `XIf5_thymus_mediastinum` |
| `g11_melanoma` | `me_` | none (D13) | `XId_melanoma` |
| `g11_skin` | `sk_` | C44.0–C44.9, C51.9, C60.9, C63.2 | `XIe_skin_carcinoma` |
| `g11_breast` | `br_` | C50.0–C50.9 | `XIf6_breast` |
| `g11_female_genital` | `fg_` | C51.0–C51.8, C52.9, C53.x, C54.x, C55.9, C57.x, C58.9 | `XIf7_female_genital` |
| `g11_urinary_male_genital` | `gu_` | C60.0–C60.8, C61.9, C63.0, C63.1, C63.7–C63.9, C65.9, C66.9, C67.x, C68.x | `XIf8_urinary_male_genital` |
| `g11_eye` | `ey_` | C69.0–C69.9 | `XIf9_eye` |
| `g11_head_neck` | `hn_` | C00–C06, C09–C10, C12–C14, C30–C33 | `XIf10_head_neck`; `XIc_nasopharynx` (oropharynx nodes) |
| `g11_digestive` | `dg_` | C15, C16, C17, C23, C24, C25, C26 | `XIf2_XIf3_digestive` (oesophagus, stomach, small intestine, biliary, pancreas nodes) |
| `g11_thoracic` | `tx_` | C38.0, C38.4, C38.8, C39.x | `XIf4_lung_pleura` (pleura nodes) |
| `g11_endocrine` | `en_` | C75.0, C75.2, C75.4, C75.5, C75.8, C75.9 | `XIf10_parathyroid_other_unspecified` (parathyroid and endocrine nodes) |
| `g11_unspecified` | `un_` | C76.x, C80.9, C70–C72, C48.x; the router default | `XIf10_parathyroid_other_unspecified` (unknown primary, central nervous system, peritoneum nodes) |

The NUT carcinoma evidence (`NUT_carcinoma`) supplies the option and the immunohistochemistry
rule that each tree in D12 offers. The cross-group maps (`cross_group_A`, `cross_group_B`)
supply every referral and every lesson in §7.

**The evidence files are the specification of each tree.** Each module reads its part's
`.json` by hand, not at run time. It copies every option's label, outcome, code, behaviour, basis,
reason and recognition aid, and puts the cite in a comment (file, page and quotation, as Group 10's
aids carry theirs). An implementer may change an agent's node only to apply a D-number, to remove
an organ question the router already answers (D14), or to merge duplicate nodes. Each change goes
in the module's docstring. A node the evidence proposes and the build drops goes in the build
report.

### 4.2 Nodes every tree has (built by `group11_common.py`)

Group 10's lesson: one node per evidence context, because `app.js` replaces `evidence_tests` and
does not merge it.

| Node | Type | What it does |
|---|---|---|
| `<p>_document_inventory` | `document_inventory` | What is in the file. Its tiers are referral or clinical note only, imaging only, imaging with a marker result (only where D7 allows a code), cytology, and histology. Each tier captures `evidence_tests`, `workup_status` and `basis_evidence_tier`. The checklist rules live in `docs/evidence_documents/group_11.json`, with laboratory-screen copies where the tree has laboratory tests (Group 10 report §4). |
| `<p>_clinical`, `<p>_clinical_cytology` | `clinical_alias` | A note stating a malignant tumour that is at least probable refers to Group XII with `8000`, melanoma of the skin included (D7, as ruled 8 October 2026). "Possible" is not registrable. |
| `<p>_imaging`, `<p>_imaging_markers`, `<p>_imaging_cytology` | `morphology_only` | The same, from imaging; the marker codes only on `_imaging_markers` (D7). |
| `<p>_cytology` | `morphology_only` | Cytology names an entity: its code at basis 5 (D8). Malignant cells, type not named: refer to Group XII with `8001`. Suspicious: not registrable. |
| `<p>_histology` | `histology_subclassification` | From the evidence file. Options run paediatric entities first (D1), then the generic options (carcinoma, adenocarcinoma, squamous cell carcinoma where the site has them), then melanoma (D13), NUT carcinoma (D12), "another carcinoma the report names" (the picker), "a tumour the report calls benign, borderline or in situ" (the exclusion screen), "a deposit" (D10), and "not a carcinoma" (referrals). |
| `<p>_picker` | `histology_subclassification` | D2. |
| `<p>_not_malignant` | `histology_subclassification` | Exclusions with the ICD-O-3.2 Preferred term at each (code, behaviour); `excl` looks the term up from `icdo32.sqlite` at generation time. |
| `<p>_deposit` | `morphology_only` | D10. |
| `<p>_ihc` | `ihc_checklist` | Only where the evidence gives rules; each rule's page in its `reason` or `coding_note`; NOS fallback required; run `induce_flow.py` and confirm every rule has a witness. |

Laboratory screens (`lab_results`) use only the tests the evidence names with a diagnostic role.
Examples are calcitonin at the thyroid, and chromogranin A and the hormones at the appendix,
digestive, lung and thymus trees. A value never chooses a code (Group 10 lesson). A `numeric_gate`
is built only if the registrar rules cut-offs.

Clerk-facing text uses report vocabulary and full forms. Every `reason` that names a code gives
the ICD-O-3.2 Preferred term and the code, for example "Recorded as Papillary thyroid carcinoma
(8260/3)." No `clinical_alert` carries text (ruling 9). The clinical sentences go to
`docs/clinical-warnings.md`.

---

## 5. Validation rules this group adds (T4)

Registration (cross_group_B):
- `GROUP11 = 11` after `GROUP10`;
- `BEHAVIOUR_DECLARED_BY_GROUP[GROUP11] = {"3"}`;
- `GROUP11` joins `ROUND_TRIP_GROUPS`;
- rules registered after the Group 10 block, each `if ctx.group != GROUP11: return []`;
- Group 10 helpers parameterised by group, not copied, where they are group-neutral;
- `parse_classification_subgroups` accepts two-digit subgroups (`XIf10`, `XIf11`).

| # | Function | Asserts | Keyed off |
|---|---|---|---|
| 1 | `check_group11_codes_fit_site` | Every emitted (code, behaviour) on a code branch, an immunohistochemistry rule or a fallback lies in a Group XI range covering every site of every tree that reaches the node, or is a D11 code. A node's sites are the union of the routed sites of each tree that reaches it; the melanoma tree takes the union of the trees that enter it. No `behaviour_exclusion` lies in such a range | `ICCC-2017.sqlite`, router |
| 2 | `check_group11_no_pathology_codes` | On paths whose `evidence_tests` hold neither Histology nor Cytology: basis 1 emits only `8720/3`, and only on a skin tree; basis 4 emits only the Visser Table 4 codes, with Imaging and a marker on the path; no such path reaches basis 5, 7 or 8 | the walked path (`_group8_terminals_by_evidence`) |
| 3 | `check_group11_obs_never_emitted` | None of the eleven all-`[obs]` pairs (and `8551`, `8780` while D3 holds) is emitted, offered by a picker, or aliased | `icdo32.sqlite` |
| 4 | `check_group11_every_code_has_a_route` | Every live `/3` code ICCC places in Group XI at a tree's routed sites is an option or a picker entry in that tree; picker `search_terms` are live ICD-O-3.2 synonyms and related terms | inventory, `icdo32.sqlite` |
| 5 | `check_group11_subgroups_and_routing` | The subgroup `app.js` shows equals ICCC-2017's at every lookup code where ICCC places the pair in Group XI. Each routing list equals exactly the sites §4.1 assigns, computed from ICCC. Every lookup code listing 11 is named by a rule. The default is `g11_unspecified` | ICCC, router, lookup |
| 6 | `check_group11_alias_terms_match_icdo32` | Group 10 rule 3 in its site form (cross_group_B): an alias equal to an ICD-O-3.2 term maps to that term's code; an organ-naming term is not an alias of a code another tree emits at another organ | `icdo32.sqlite` |
| 7 | `check_group11_picker_aliases_stay_unshared` | Group 10 rule 8: a picker-only alias is held by no other group | alias files |
| 8 | `check_group11_deposits_recapture` | Every option labelled as a deposit, or whose reason says "primary", carries `recapture_site: true`; a leukaemia referral records C42.1 | the tree |

`build/negative_controls_group11.py`, modelled on `negative_controls_group10.py`, runs a probe of
the correct data for each rule, then at least two mutations per rule, each expected CAUGHT. Two
are named here:
- **R2-B, "the path, not the flag":** the histology tier of one gate captures `["Imaging"]`.
- **R1-A:** the lung picker gains `8170/3`.

Record the run in `docs/validator_negative_controls.md` under `# Group 11 (8 October 2026)`.

---

## 6. The alias layer (T5)

`build/generate_group11_aliases.py`, modelled on `generate_group10_aliases.py`. Sources, with the
first source winning on the same string:
1. ICD-O-3.2 terms (Preferred, Synonym, Related; not `[obs]`) of every pair a tree emits, subject
   to Group 10's D21 in its site form;
2. curated British spellings and the WHO names the trees use.

Not aliased: "ACC", "NET", "NEC", "GCT"; any excluded-behaviour term; any string another group
holds (cross_group_B C1–C15).
- Where Group 10's picker already aliases a carcinoma string, Group 11 does not duplicate it:
  rule 8 forbids sharing.
- Where both groups need the term, `occurs_at_routed_sites` and the term's `primary_sites` let
  the site decide.
- A term that still ties goes to the "ICD Overall fixes" engine request (cross_group_B,
  registration list), not into `app.js`.

`ihc_tree_id` and `tree_entry_node` follow Group 10's convention.

---

## 7. Other groups' files and the 17 referrals

The 17 `refer_group: 11` branches (cross_group_A, `referrals_in`) land through the router. With
`groups["11"]` built, each continues in Group 11 with the case's topography, or asks the primary's
site where it carries `recapture_site`. Change another group's file only where a branch would land
at a site Group 11 does not route, or where its reason names a code Group 11 no longer emits.
List each change in the build report. Hand engine changes to the "ICD Overall fixes" session (memory
rule); do not build them here.

---

## 8. Docs (T6)

- **`docs/group_11_registrar_review.md`:** the 140 questions, grouped by D-number class, each with
  the default the build applies and the evidence file and page; the cost-ordered list first, as
  Group 10's.
- **`docs/group_11_layer1_repair.md`:** every REDCap Group 11 option classified against ICD-O-3.2,
  in Group 10's format, carrying the currency check §§2, 4, 5 and 6.
- **The Layer 1 ICCC Markdown table** (`ICD coding/ICCC 2017 Cancer Classification.md`) has malformed
  Group XI rows (`C80.90-C80.98`, `C80.98`) that make the build warn that 8090–8097 are out of range, when
  `ICCC-2017.sqlite` range 124 places them in XIe (T1 finding). List the repair in the Layer 1 repair package.
  Do not edit Layer 1 from this repository.
- **`docs/TODO.md`:** a Group XI section, a §7 index row, and the engine request (cross_group_B).
- **`docs/clinical-warnings.md`:** a `# Group XI` section, for any clinical sentence an evidence
  agent wrote that the tree does not render.
- **`docs/group_baseline_documents.md`:** the Group XI row, the WHO volume and year per part
  (registrar, 8 October 2026), and the paediatric papers.
- **`docs/sources-requested.md`:** the four PMC papers the publisher restricts (Ozolek 2021,
  Cortes-Santiago 2021, Cole 2023, Sthapit 2025), and the WHO volumes the data gaps name.

---

## 9. Proof before this group is called done (T7)

1. `python3 build/build_database.py` → 0 FAIL.
2. `python3 build/induce_flow.py --check` → every rule has a witness.
3. `python3 build/negative_controls_group11.py` → every control CAUGHT, every probe passes; the
   Group 10, Group 9, Group 8, Group 3 and UX suites unchanged.
4. `node build/check_engine_flow.mjs` → pass.
5. A walk of every terminal of every Group 11 tree: the evidence captured equals the reports the
   clerk ticked (Group 10 report §7 item 1).
6. Drive in the browser (`python3 -m http.server 8811`), reading the subgroup line and "Also
   called" on each output:
   - papillary thyroid carcinoma by search at C73.9 → `8260/3` XIb;
   - a thyroid follicular carcinoma, minimally invasive → `8335/3`; encapsulated, no invasion → exclusion `8335/1`;
   - adrenal cortical carcinoma at C74.9 → site corrected to C74.0 → `8370/3` XIa;
   - nasopharyngeal carcinoma, non-keratinising → `8072/3` XIc;
   - mucoepidermoid carcinoma of the parotid → `8430/3` XIf1;
   - appendiceal neuroendocrine tumour, grade 1 → `8240/3` XIf3;
   - melanoma of the skin of the arm, clinical only → `8720/3` basis 1 XId;
   - Spitz melanoma → `8770/3` XId;
   - NUT carcinoma of the lung → `8023/3` XIf4;
   - solid pseudopapillary neoplasm of the pancreas → `8452/3` XIf10;
   - secretory carcinoma of the breast → `8502/3` XIf6;
   - a carcinoma at C80.9 → XIf11;
   - a Group IX referral (`st_not_sarcoma`) arriving at soft tissue → `g11_unspecified`, the deposit question;
   - the picker on the lung tree filtered by a typed term.
7. `app.js`, `index.html` and `uccf-tool.css` byte-identical to `main`.

---

## 10. Tasks

- [x] T1 `build/generate_group11_entries.py` → 230 entries and metadata (stub tree). Build 0 FAIL, `--check` 0
- [x] T2a `build/group11_common.py` and the thyroid exemplar
- [x] T2b the ten family trees, one module each in `build/group11_families/` (a template module could not be written in parallel)
- [x] T2c `build/group11_organs/` (eight organ trees and the melanoma tree)
- [x] T2d integration: 19 trees, 230 entries, every checklist rule witnessed; walk of all 18 routed trees 0 failures; build 0 FAIL (8 October 2026)
- [x] T3 router and topography (§3): 153 codes added, 57 given 11, `groups["11"]` built; Group 10's Xb routing and entries regenerated to name the new sites
- [ ] T4 `build_database.py` registration and §5 rules 1, 2, 3, 5 and the self-referral admission; `negative_controls_group11.py`. Rules 4, 6, 7, 8 and the engine-gate picker sweep deferred to `docs/TODO.md` (registrar near a usage limit, 8 October 2026)
- [ ] T5 `aliases_group_11.json`
- [ ] T6 docs (§8)
- [ ] T7 proof (§9)
- [ ] T8 `docs/group_11_build_report.md`
