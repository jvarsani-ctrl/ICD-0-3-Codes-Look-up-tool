# Group XI cross-group map, part A: referrals, router, topography and ICCC placement

**Written 8 October 2026, before any Group 11 JSON exists.** Branch `claude/group-11-carcinomas`,
identical to `main` at `7025128`. Companion data: `cross_group_A.json` in this folder.

**Sources read.** The repository (`app.js`, `data/database/group_01…10_dt.json`,
`data/shared/presentation_router.json`, `data/shared/topography_codes.json`,
`build/build_database.py`, `docs/group_10_*`, `docs/group_11_build_contract.md`);
`ICCC-2017.sqlite` (tables `groups`, `code_ranges`, `topography_segments`, `morphology_codes`);
`icdo32.sqlite` (table `icd_o_3_2_morphology`); the Group XI inventory `g11_inventory.json`
(229 usable codes). No paper was read and nothing was fetched.

**Method.** Every placement below was computed, not transcribed. A script joins each ICCC-2017
range's expanded codes (`morphology_codes`) to its topography segments and tests every
(code, topography) pair, behaviour 3, for all 229 usable Group XI codes plus `8339`, across the
330 ICD-O-3 topography codes. No (code, topography) pair falls in two subgroups. The topography
universe is the ICD-O-3 topography list written into the script. The Layer 1 file
`RedCap Options/Topography Redcap.md` was outside this part's reading list and was not read.
Labels and REDCap codes for the missing sites therefore still have to be read from it.

---

## Findings in brief

1. **Seventeen branches refer to Group 11** (Groups II ×2, III ×3, IV ×3, VII ×1, VIII ×1,
   IX ×1, X ×6). Seven carry `recapture_site` and land wherever the recorded primary routes.
   Ten keep the case's topography and land in the tree that Group XI routes that site to.
2. **The recaptured primary cannot be recorded at most Group XI sites.** The site screen offers
   only `coarse_organ_crosswalk` rows (`app.js:653-711`). **155 Group XI topography codes have no lookup entry
   and no crosswalk row**, among them every salivary gland, colon, rectum, anus, appendix, breast,
   oral cavity, pharynx, oesophagus, stomach, pancreas, gallbladder and larynx code. Every deposit referral (Groups III, VII, VIII and X) dead-ends there today.
3. **Group XI places none of its carcinoma codes at bone (C40-C41), marrow (C42), peripheral
   nerve and soft tissue (C47, C49), lymph nodes (C77) or the adrenal gland (C74, except
   8370-8375 and 8158 at C74.0).** These pairs are unclassified in ICCC-2017. Two referrals keep
   such a site: Group IX `st_not_sarcoma` (soft tissue) and Group X `eg_other` (bone, marrow,
   soft tissue, adrenal). Both need the primary asked.
4. **ICCC-2017 gives Group XI-range codes to another group at only four places:** the liver
   (VIIb, 73 codes), the kidney (VIb, 74), the ovary and testis (Xd, 93 and 86) and the
   pituitary (IIIe1, 8158 and 8290). No Group XI-range code is Group I, II, IV, V, VIII, IX or XII
   at any site.
5. **Three referral reasons overstate.** "Carcinomas of other organs and melanomas are ICCC-3
   Group XI" (Group VII `hp_secondary_deposit`; Group X `ov_deposit`, `ts_deposit`,
   `eg_deposit`) and "A carcinoma or melanoma outside the gonads belongs to ICCC-3 Group XI"
   (`eg_other`) are false for a renal carcinoma (VIb), a cholangiocarcinoma (VIIb at any site) and
   a carcinoma at the liver. Group III's `mn_lesion_triage` sends meningeal melanocytoma, which
   is `8728/1` and has no ICCC group, to Group XI as if it were XId.
6. **Router rules `8158` and `8290` default to Group 11 and miss ICCC branches.** At C56.9 8158
   is Xd, at C56.9 and C62.x 8290 is Xd, and at C64.9 8290 is VIb. Group X and Group VI already
   carry those entries. The rules feed only the output's "Group routing" note (`app.js:2285`,
   `2639`), so no case enters the wrong group, but the note can name Group 11 wrongly.
7. **Only two presentations list Group 11** ("Incidental imaging finding", "Not sure"). A
   melanoma of the skin cannot reach Group XI from "Cutaneous / mucosal lesion", and a thyroid
   nodule cannot reach it from "Mass / swelling". Adding 11 to "Organ-functional sign" would hide
   Group IX at the bladder, cervix, vagina and uterus (`narrowBySite`, `app.js:3205-3212`).

---

## 1. Referrals into Group XI

### 1.1 How a referral hop runs (`app.js`)

| Step | Code | What it does |
|---|---|---|
| Branch fires | `advance()` → `refer(target)`, `app.js:2157`, `2369-2380` | Builds `{referral, group: refer_group, codeHint: refer_code, note: reason, recaptureSite: recapture_site === true}`. No code is emitted. |
| Referral screen | `app.js:2520-2530` | Shows "Code here: None", "Code there" from `refer_code`, "Why" from `reason`, and the topography unless the site is to be recaptured. |
| Hop allowed? | `canHop`, `app.js:2315-2321` | The target must be `built`. A target with `tree_routing` also needs a captured topography, unless the referral recaptures it. |
| Carry-over | `caseFacts`, `app.js:2302-2314` | Keeps only `topography`, `organ_system`, `tumour_origin`, the discriminator variables and the tick-vocabulary variables. Every other capture is dropped. |
| Hop, site kept | `hopToGroup`, `app.js:2328-2349` | Fixes the group (`state.group = target; state.candidates = [target]`, `app.js:2345`) and calls `afterGroup()`. The site's `candidate_groups` are not consulted again. |
| Hop, site recaptured | `app.js:2337`, `2344`, `2350-2358` | Deletes the topography and organ system, clears the presentation, sets `recordGroup`, and asks the site from every crosswalk row. `siteRecordOnly = !groupReadsSite(11)`, which is false once Group 11 has `tree_routing`, so the "The file does not state the site" escape is not offered: the clerk picks C80.9 for an unknown primary. |
| Tree chosen | `afterGroup`, `app.js:3376-3392`; `routedTree`, `3362-3374` | Group 11 is routed by the first `tree_routing` rule whose `topography_in` holds the site, else the default. The default is required. |

**What Group 11 must provide for every referral to land:**

- `groups["11"].built: true`, with `tree_routing` naming every lookup code (section 2.4). Without
  `tree_routing` a 15-tree group would fall to `tree_selection`, a question the topography
  already answers.
- An entry `document_inventory` per routed tree (`build_database.py` `check_presentation_router`,
  ~12150-12205).
- A melanoma branch at the first histology question of **every** tree, jumping by cross-tree
  `next_node` to a melanoma histology node that is not the melanoma tree's own
  `document_inventory`. `app.js` replaces a captured `evidence_tests` list at each
  `document_inventory` (Group 10 report §7 item 1).
- In the tree for sites with no Group XI carcinoma subgroup (rule R8 below), a carcinoma branch
  that refers by site: C22 → Group VII, C64.9 → Group VI, C56.9 and C62.x → Group X. At
  C40-C42, C47, C49 and C77 it asks for the primary.
- The lookup and crosswalk additions of section 3, without which no recaptured primary reaches
  most Group XI trees.

### 1.2 The seventeen branches

`R` = `recapture_site: true`. "Kept" = the case keeps the topography of the referring tree.

| # | Branch (`file:line`; node line) | Tree / node (type) | Option or rule | Site on hop | Lands in (approach 3) | Subgroup |
|---|---|---|---|---|---|---|
| 1 | `group_02_dt.json:10888` (node 10796) | `g2_histiocytic` / `g2hist_minimum_panel` (ihc_checklist) | positive melanocytic markers (HMB-45 / Melan-A / SOX10) | kept; any site (Group II is `occurs_at_any_site`, router 357). Absent after "site not stated" in the typed lane, so no hop button | the tree the site routes to; `g11_melanoma` at C40-C42, C47, C49, C77; elsewhere a cross-tree jump to melanoma | XId |
| 2 | `group_02_dt.json:11288` (node 11221) | `g2_histiocytic` / `g2hist_mhn_algorithm` (ihc_checklist) | same | same | same | XId |
| 3 | `group_03_dt.json:4173` (node 4103) | `g3_posterior_fossa` / `pf_secondary_deposit` (site_resolution) | site "Carcinoma or melanoma" | **R** | by the recorded primary | any |
| 4 | `group_03_dt.json:24027` (node 23991) | `g3_meninges` / `mn_lesion_triage` (histology_subclassification) | "Melanin-pigmented or melanocytic proliferation; HMB-45, Melan-A or SOX10 positive" | kept: C70.0, C70.1, C70.9 (router 511-518) | `g11_other_specified` (C70 is XIf10), jumping to melanoma | XId for 8720/3, 8728/3; **none** for 8728/1, 8728/0 |
| 5 | `group_03_dt.json:29390` (node 29294) | `g3_unspecified` / `un_metastatic_deposit` (site_resolution) | "Thyroid, nasopharynx, skin melanoma or another carcinoma"; captures `metastatic_deposit` (dropped on hop) | **R** | by the recorded primary | any |
| 6 | `group_04_dt.json:1116` (node 1066) | `g4_sympathoadrenal` / `sa_ihc_checklist` (ihc_checklist) | when topography C74.0, C74.1, C74.9; Cytokeratin +, GATA3 −; **`refer_code: "8370"`** | kept: C74.x | `g11_adrenal` | XIa (8370 at any site, range 119) |
| 7 | `group_04_dt.json:1626` (node 1542) | `g4_head_neck_paraganglia` / `hn_ihc_checklist` (ihc_checklist) | `keratin_status` positive | kept: C75.4, C75.5, C30.1 (router 591-598) | `g11_other_specified` | XIf10 |
| 8 | `group_04_dt.json:2193` (node 2112) | `g4_sinonasal` / `sn_ihc_checklist` (ihc_checklist) | `pankeratin_status` positive | kept: C30.0, C31.x, C11.x (router 601-618) | `g11_other_specified` at C30/C31; `g11_nasopharynx` at C11 | XIf10; XIc |
| 9 | `group_07_dt.json:3831` (node 3736) | `g7_hepatic` / `hp_secondary_deposit` (site_resolution) | "A carcinoma or melanoma of another organ, other than the ovary or testis" | **R** | by the recorded primary; C64.9 → R8 tree → Group VI | any |
| 10 | `group_08_dt.json:2860` (node 2812) | `g8_bone` / `bn_metastasis` (morphology_only) | "Carcinoma or melanoma (for example nasopharyngeal carcinoma)" | **R** | by the recorded primary | any (XIc for the example) |
| 11 | `group_09_dt.json:5125` (node 5062) | `g9_soft_tissue` / `st_not_sarcoma` (histology_subclassification) | "Melanoma or carcinoma"; captures `not_sarcoma_diagnosis` (dropped on hop) | kept: every non-C44 Group IX site (C47, C48, C49, C11, C24, C30, C31, C51-C55, C57.8, C61.9, C63, C67, C68.8, C69.6, C69.8, C76.3, C77) | the tree the site routes to; `g11_melanoma` at C47, C49, C77 | XId; a carcinoma at C47, C49 or C77 has **none** |
| 12 | `group_10_dt.json:11156` (node 11099) | `g10_ovary` / `ov_other` (morphology_only) | "A melanoma" | kept: C56.9 | `g11_melanoma` | XId |
| 13 | `group_10_dt.json:11222` (node 11168) | `g10_ovary` / `ov_deposit` (morphology_only) | "A carcinoma or melanoma of another organ" | **R** | by the recorded primary | any |
| 14 | `group_10_dt.json:13897` (node 13840) | `g10_testis` / `ts_other` (morphology_only) | "A melanoma" | kept: C62.0, C62.1, C62.9 | `g11_melanoma` | XId |
| 15 | `group_10_dt.json:13963` (node 13909) | `g10_testis` / `ts_deposit` (morphology_only) | "A carcinoma or melanoma of another organ" | **R** | by the recorded primary | any |
| 16 | `group_10_dt.json:16490` (node 16370) | `g10_extragonadal` / `eg_other` (morphology_only) | "Another carcinoma, or a melanoma" | kept: one of the 139 codes of the rule at router 824-967 | the tree that site routes to (every Group XI tree except salivary, colorectal and breast, whose sites Group X does not route) | by site; none for a carcinoma at C40-C42, C47, C49, C74.1, C74.9; VIIb at C22; VIb at C64.9 |
| 17 | `group_10_dt.json:16556` (node 16502) | `g10_extragonadal` / `eg_deposit` (morphology_only) | "A carcinoma or melanoma of another organ" | **R** | by the recorded primary | any |

Only branch 6 carries `refer_code`. No branch names a Group XI subgroup.

### 1.3 Defects in the referring branches

| Branch | Defect | Consequence |
|---|---|---|
| 9, 13, 15, 17 | Reason "Carcinomas of other organs and melanomas are ICCC-3 Group XI." | False for a renal carcinoma (VIb), a cholangiocarcinoma or hepatocellular carcinoma at any site (VIIb, range 57) and a gonadal carcinoma (Xd). The hop still lands, because Group XI's R8 tree refers those on, but the text overstates (standing rule 8). |
| 16 | Reason "A carcinoma or melanoma outside the gonads belongs to ICCC-3 Group XI." | False at C22 and C64.9, both routed to `g10_extragonadal`. |
| 4 | Reason names meningeal melanocytoma among the cases ICCC "files … in XId". | XId (range 123) is behaviour 3. `8728/1` meningeal melanocytoma and `8728/0` meningeal melanocytosis have no ICCC group, and no Group III range holds 8728. Group XI needs behaviour exclusions for both. |
| 11 | "Melanoma or carcinoma" keeps the soft-tissue site. | A melanoma is XId there. A carcinoma at C47, C49 or C77 has no ICCC subgroup and needs its primary. Either Group IX splits the option (carcinoma with `recapture_site`) or Group XI's R8 tree refers a carcinoma to Group 11 with `recapture_site`. A self-referral is untested in the engine. |
| 5, 11 | `captures` (`metastatic_deposit`, `not_sarcoma_diagnosis`) | Dropped by `caseFacts()`. Group XI must ask again. |
| 13 | Sibling option "The primary is not known and has not been found" → Group 12. | A carcinoma of unknown primary is XIf11 at C80.9, and a melanoma is XId. Sending every unknown primary to Group XII misfiles carcinoma and melanoma. |
| 1, 2 | Typed-lane case with "The file does not state the site". | `canHop()` is false for a routed target with no topography, so the referral screen shows no hop button. That is correct behaviour, not a defect, but it is the one path where a Group XI referral cannot continue. |

---

## 2. The router (`data/shared/presentation_router.json`)

### 2.1 Everything that names Group 11 today

| Place | Lines | Content | Effect |
|---|---|---|---|
| `groups["11"]` | 983-988 | `built: false, trees: [], handoff: null` | `afterGroup()` shows the "not yet available" handoff (`app.js:792-806`); `canHop()` is false, so all 17 referrals stop at the referral screen. |
| `archetypes` | 116, 139 | 11 is listed only by `incidental_imaging_finding` and `unsure` | Not listed by `solid_mass` (31-40), `lymphadenopathy` (55-59), `organ_functional_sign` (75-80), `cutaneous_mucosal_lesion` (93-96) or `blood_marrow` (12-14). |
| `site_to_group` | 262-265 | `"C75.1": [3, 11]` | Validated as numbers 1-12 only. `app.js` never reads `site_to_group`. `C44` (277-280) is `[9, 2]`, `C69` (266-269) `[5, 9]`, `C74` (249-251) `[4]`, `C77` (270-273) `[2, 9]`. |
| `dual_group_rules["8158"]` | 1269-1307 | C75.1 → III IIIe1; C22 → VII VIIb; default group 11 | See 2.2. |
| `dual_group_rules["8290"]` | 1308-1332 | C75.1 → III IIIe1; default group 11 | See 2.2. |
| `dual_group_rules["8170"]` | 1508-1534 | default VII VIIb | 8160-8162 and 8170-8180 are VIIb at any site (range 57). No Group XI part. |
| `dual_group_rules["8000-8005"]` | 1535-1653 | branches III, VI, VIII, VII, X; default XII | 8000-8005 is in no Group XI range. Group XI emits none of them. |

No dual-group rule exists for carcinoma NOS, 8240, the melanoma codes or any other Group XI code.

### 2.2 Gaps in rules 8158 and 8290

`resolveGroup()` (`app.js:290-310`) feeds only the output's "Group routing" note
(`app.js:2285`, `2639`). It never decides which group a case enters. A wrong default is a wrong
note, not a wrong code.

| Code | ICCC-2017 placement (all 330 sites) | Rule today | Missing |
|---|---|---|---|
| `8158` ACTH-producing tumor | XIa C74.0 (range 118); XIb C73.9 (120); IIIe1 C75.1 (36); VIIb C22 (56); **Xd C56.9 (115)**; XIf1-XIf11 by site (125-133, 135, 136); **none** at C11, C40-C42, C44, C47, C49, C62, C64.9, C70-C72, C74.1, C74.9, C77 | C75.1, C22 branches; default 11 | a C56.9 → group 10 Xd branch (`group_10_dt.json` carries `8158/3` Xd at C56.9) |
| `8290` Oxyphilic adenocarcinoma | XIb C73.9; XIc C11; IIIe1 C75.1; **Xd C56.9, C62.x (113)**; **VIb C64.9 (50)**; XIf by site; **none** at C22, C40-C42, C44, C47, C49, C70-C72, C74, C77 | C75.1 branch; default 11 | C56.9 and C62.0-C62.9 → group 10 Xd; C64.9 → group 6 VIb (`group_06_dt.json` carries `8290/3` VIb at C64.9) |

At the "none" sites the default of 11 has no ICCC basis either. The Group VII build split 8158
from 8290 on 4 October 2026 for the same class of fault (router 1300).

### 2.3 What Group 10 added, and the lessons for Group 11

| Group 10 rule | Lines | What it does |
|---|---|---|
| `occurs_at_routed_sites: true` | 751 | The typed lane keeps a term filed under Group X alone at a site one of its own rules names, even when that site's `candidate_groups` omits 10, provided an entry of the term lists the site in `primary_sites` (`occursAtRoutedSite`, `app.js:3284-3299`). The default does not count. `build_database.py` ~12096-12106 requires `built` and a `tree_routing` rule list. |
| `tree_routing` | 770-976 | Four rules (rules 773-969): the 24 Xa codes → `g10_cns`; C56.9 → `g10_ovary`; C62.0, C62.1, C62.9 → `g10_testis`; 139 Xb codes → `g10_extragonadal`. Every lookup code that lists 10 is named by a rule. |
| `default` | 970-975 | `g10_extragonadal`. Required by `routedTree()`; reached only by a hop from an unnamed site. |
| `handoff` | 977-981 | `g10_extragonadal`. Validated by `check_presentation_router()`; `app.js` does not read it. |
| `dual_group_rules["8000-8005"]` C56.9/C62 branch | 1632-1646 | Xe at the gonads. |
| Build check `check_group10_subgroups_and_routing` | `build_database.py:10625` | Recomputes rules and per-entry subgroups from ICCC ranges 94-117 against the lookup on every build. A missing or extra rule code fails by name. |
| Registrar review B2 | `docs/group_10_registrar_review.md:194-226`, `547-552` | The front door stays as it is: listing Group X at the kidney, liver, bone and soft tissue would add a family question to the commonest childhood masses. The typed lane and the referral hop reach Group X instead. |
| F-H-12 | router 83; `docs/group_10_registrar_review.md:553-559` | Adding a group to "Organ-functional sign" removes the choice at sites where that group is the only overlap, because `narrowBySite()` takes the intersection and falls back to the site list only when the intersection is empty. |

### 2.4 What `groups["11"]` must contain

```json
"11": {
  "name": "Other Malignant Epithelial Neoplasms and Malignant Melanomas",
  "built": true,
  "occurs_at_routed_sites": true,
  "trees": [ fifteen {tree_id, entry_node} pairs, one per tree below ],
  "tree_routing": {
    "variable": "topography",
    "rules": [ R1 … R15, below ],
    "default": { "tree_id": "g11_other_specified", "entry_node": "<its document_inventory>",
                 "reason": "Every lookup code is named by a rule; app.js routedTree() requires a default." }
  },
  "handoff": { "group": 11, "tree_id": "g11_other_specified", "entry_node": "<its document_inventory>" }
}
```

Tree identifiers are proposals. The rule sets are computed from ICCC ranges 118-136 and cover
all 330 ICD-O-3 codes and all 175 lookup codes, each exactly once:

| Rule | Tree | ICCC basis | Lookup codes today | Codes after section 3 additions |
|---|---|---|---|---|
| R1 | `g11_adrenal` | XIa (range 118 C74.0; range 119 any site) | C74.0, C74.1, C74.9 | 3 |
| R2 | `g11_thyroid` | XIb (range 120, 739) | C73.9 | 1 |
| R3 | `g11_nasopharynx` | XIc (range 122, 110-119) | C11.0-C11.3, C11.8, C11.9 | 6 |
| R4 | `g11_salivary` | XIf1 (range 125, 079-089) | none | 5: C07.9, C08.0, C08.1, C08.8, C08.9 |
| R5 | `g11_lung` | XIf4 (range 128) | C34.0-C34.3, C34.8, C34.9 | 6 |
| R6 | `g11_thymus` | XIf5 (range 129) | C37.9 | 1 |
| R7 | `g11_colorectal` | XIf2 (range 126) + XIf3 (range 127, C18.1) | none | 16: C18.0-C18.9, C19.9, C20.9, C21.0-C21.2, C21.8 |
| R8 | `g11_melanoma` | no Group XI carcinoma subgroup: XId, 8370 (XIa) and the XIb any-site codes only | 51: C22.0-C22.1, C40.x, C41.x, C42.0-C42.4, C47.x, C49.x, C56.9, C62.0, C62.1, C62.9, C64.9, C77.x | 51 |
| R9 | `g11_skin` | XIe (range 124: 440-449, 519, 609, 632) | C44.0-C44.3, C44.5-C44.9, C51.9, C63.2 | 13 (+C44.4, C60.9) |
| R10 | `g11_breast` | XIf6 (range 130) | none | 9: C50.0-C50.6, C50.8, C50.9 |
| R11 | `g11_cervix` | XIf7 (range 131) | C53.0, C53.1, C53.8, C53.9 | 4 |
| R12 | `g11_bladder` | XIf8 (range 132) | C67.0-C67.9 | 10 |
| R13 | `g11_eye` | XIf9 (range 133) | C69.0-C69.6, C69.8, C69.9 | 9 |
| R14 | `g11_other_specified` | XIf10 (range 134) | 64 (C24.0, C24.8, C24.9, C30.x, C31.x, C38.1-C38.3, C48.0, C48.2, C48.8, C51.0-C51.8, C52.9, C54.x, C55.9, C57.8, C58.9, C61.9, C63.0, C63.1, C63.7-C63.9, C68.8, C70-C72 (21), C75.1-C75.5) | 187 |
| R15 | `g11_unspecified` | XIf11 (range 136: 760-768, 809) | C76.0-C76.5, C76.7, C76.8, C80.9 | 9 |

Constraints the build already enforces or the contract adopts:

- Each rule's `entry_node` is a `document_inventory` (or a `lab_results` node whose `next_node` is
  one) in `group_11_dt.json`, and its `tree_id` is declared there (`check_presentation_router`,
  `build_database.py` ~12150-12205).
- `occurs_at_routed_sites` needs `built` and a rule list (`build_database.py` ~12096-12106).
  Since R1-R15 name every lookup code, it reduces to the entries' `primary_sites`. Melanoma
  entries must therefore list `C00.0-C80.9`, and each carcinoma entry exactly its Group XI sites
  (`sitesCover` reads the first two codes of each string, `app.js:3266-3276`).
- `occurs_at_any_site` stays absent. It would admit every Group XI-only term at every site,
  including a carcinoma term at the liver.
- One rule per tree is the contract's convention (§0.4). `app.js` `routedTree()` accepts several
  rules naming one tree, and no check in `build_database.py` forbids it.
- A Group 10 RULE 4 analogue recomputes R1-R15 and every entry's
  `iccc3_subgroup_by_topography` from ICCC ranges 118-136 on each build.
- 8158 and 8290 have their own XIf10 range (135), which excludes C70-C72 and C75.1 and includes
  C51.9, C60.9 and C63.2. Their subgroup rules differ from the shared list's.

### 2.5 Presentations: what adding 11 does

`narrowBySite()` (`app.js:3205-3212`) intersects the presentation's list with the site's list
and falls back to the site's list only when the intersection is empty.

| Presentation | Today | Adding 11 |
|---|---|---|
| `solid_mass` (31-40) | Thyroid C73.9 `[2, 10, 11]` → `[2, 10]`; Group XI unreachable | Adds Group XI to the family question wherever the site lists 11. |
| `cutaneous_mucosal_lesion` (93-96) | Skin C44 `[9, 2, 11]` → `[9, 2]`; melanoma of the skin unreachable | Adds Group XI at skin and mucosa. |
| `lymphadenopathy` (55-59) | Nasopharynx C11 `[4, 9, 11]` → `[9]`, or `[2, 9]` when the compartment answer keeps Group II (`keep_on_site`, router 182-193): a nasopharyngeal carcinoma presenting with neck nodes is never offered Group XI | C11 → `[9, 11]` (plus 2 when kept); C73.9 → `[2, 11]`; C77 unchanged. |
| `organ_functional_sign` (75-80) | Bladder C67 `[9, 11]` → empty → fallback `[9, 11]` | **Removes Group IX** at C67, C24, C51-C55, C57.8, C61.9 and C11, because the intersection becomes `[11]` (the F-H-12 effect). Not recommended. |

---

## 3. Topography (`data/shared/topography_codes.json`)

### 3.1 Every Group XI ICCC topography against the lookup

XIa range 119, XIb range 121 and XId (range 123) are any-site ranges (`000-809`), so every lookup
code carries a Group XI code for melanoma, 8370-8375 and the XIb any-site codes. The table covers
the site-specific ranges.

| Subgroup (range) | ICCC topography | ICD-O-3 codes | In lookup, lists 11 | In lookup, no 11 | Not in lookup |
|---|---|---|---|---|---|
| XIa (118) | 740 | 1 | 0 | C74.0 `[4]` | 0 |
| XIb (120) | 739 | 1 | C73.9 | 0 | 0 |
| XIc (122) | 110-119 | 6 | C11.0-C11.9 (6) | 0 | 0 |
| XIe (124) | 440-449, 519, 609, 632 | 13 | 10 (C44.0-C44.3, C44.5-C44.9, C51.9) | C63.2 `[9, 10]` | C44.4, C60.9 |
| XIf1 (125) | 079-089 | 5 | 0 | 0 | 5 |
| XIf2 (126) | 180, 182-189, 199, 209, 210-218 | 15 | 0 | 0 | 15 |
| XIf3 (127) | 181 | 1 | 0 | 0 | C18.1 |
| XIf4 (128) | 340-349 | 6 | 6 | 0 | 0 |
| XIf5 (129) | 379 | 1 | C37.9 | 0 | 0 |
| XIf6 (130) | 500-509 | 9 | 0 | 0 | 9 |
| XIf7 (131) | 530-539 | 4 | 4 | 0 | 0 |
| XIf8 (132) | 670-679 | 10 | 10 | 0 | 0 |
| XIf9 (133) | 690-699 | 9 | 0 | 9 (C69.x `[5]`; C69.4 `[5, 4]`; C69.6, C69.8 `[5, 9]`) | 0 |
| XIf10 (134) | 000-069, 090-109, 129-179, 239-339, 380-399, 480-488, 510-518, 529, 540-559, 570-608, 619, 630-631, 637-639, 659-669, 680-689, 700-729, 750-759 | 187 | 19 | 45 | 123 |
| XIf10 (135, 8158 and 8290) | as 134 but 510-529, 570-619, 630-639, 750, 752-759 | 168 | 19 | 25 | 124 |
| XIf11 (136) | 760-768, 809 | 9 | 0 | C76.3 `[9, 10]`; eight codes carry `"route_by_morphology"` | 0 |

`"route_by_morphology"` (C76.0-C76.2, C76.4, C76.5, C76.7, C76.8, C80.9; lines 1645-1677) is a
string. `narrowBySite()` leaves the candidates unfiltered (`app.js:3208`) and `afterSearchSite()`
keeps every group of the term (`app.js:3313-3315`), so XIf11 needs no change there.

### 3.2 Codes missing from the lookup: 155

None of these has a lookup entry or a crosswalk row, so no path can record them.

| Family | Codes | n |
|---|---|---|
| Skin (XIe) | C44.4; C60.9 | 2 |
| Salivary glands (XIf1) | C07.9; C08.0, C08.1, C08.8, C08.9 | 5 |
| Colon, rectum, anus, appendix (XIf2, XIf3) | C18.0-C18.9; C19.9; C20.9; C21.0, C21.1, C21.2, C21.8 | 16 |
| Breast (XIf6) | C50.0-C50.6, C50.8, C50.9 | 9 |
| Lip, oral cavity, pharynx (XIf10) | C00.0-C00.6, C00.8, C00.9; C01.9; C02.0-C02.4, C02.8, C02.9; C03.0, C03.1, C03.9; C04.0, C04.1, C04.8, C04.9; C05.0-C05.2, C05.8, C05.9; C06.0-C06.2, C06.8, C06.9; C09.0, C09.1, C09.8, C09.9; C10.0-C10.4, C10.8, C10.9; C12.9; C13.0-C13.2, C13.8, C13.9; C14.0, C14.2, C14.8 | 54 |
| Digestive organs (XIf10) | C15.0-C15.5, C15.8, C15.9; C16.0-C16.6, C16.8, C16.9; C17.0-C17.3, C17.8, C17.9; C23.9; C24.1; C25.0-C25.4, C25.7-C25.9; C26.0, C26.8, C26.9 | 36 |
| Larynx, trachea, heart, pleura, thorax (XIf10) | C32.0-C32.3, C32.8, C32.9; C33.9; C38.0, C38.4, C38.8; C39.0, C39.8, C39.9 | 13 |
| Peritoneum (XIf10) | C48.1 | 1 |
| Female genital (XIf10) | C57.0-C57.4, C57.7, C57.9 | 7 |
| Male genital (XIf10) | C60.0, C60.1, C60.2, C60.8 | 4 |
| Urinary tract (XIf10) | C65.9; C66.9; C68.0, C68.1, C68.9 | 5 |
| Other endocrine (XIf10) | C75.0, C75.8, C75.9 | 3 |

Labels and REDCap codes come from Layer 1 `RedCap Options/Topography Redcap.md`.
`renderSite()` lists crosswalk rows only (`app.js:653-711`), so each family also needs a
`coarse_organ_crosswalk` row. Today every lookup code sits in a row and every row code is in
the lookup.

### 3.3 Lookup codes in a Group XI site range that do not list 11: 57 (plus 8 string-valued)

| Codes | `candidate_groups` today | Lines | Note |
|---|---|---|---|
| C74.0 | `[4]` | 1393 | XIa. Adding 11 brings a Group IV / Group XI question to every adrenal mass (B2 trade-off). The Group IV referral (branch 6) reaches Group XI without it. |
| C63.2 | `[9, 10]` | 1304 | XIe. |
| C69.0-C69.6, C69.8, C69.9 | `[5]`, `[5, 4]`, `[5, 9]` | 2383-2451, 1636 | XIf9 and uveal or conjunctival melanoma. **Today a uveal melanoma at C69.3 enters Group V alone.** |
| C30.0, C30.1, C31.0-C31.3, C31.8, C31.9 | `[4, 9]` | 2240-2318 | XIf10. Group IV branches 7 and 8 refer here. |
| C38.1, C38.2, C38.3 | `[2, 4, 10]`, `[2, 4]`, `[2, 4, 10]` | 2329-2352 | XIf10. |
| C48.0, C48.2, C48.8 | `[2, 4, 9, 10]`, `[2, 4, 9]`, `[2, 4, 9]` | 1833-1868 | XIf10. |
| C58.9 | `[10]` | 1272 | XIf10. |
| C63.0, C63.1, C63.7, C63.8, C63.9 | `[9, 10]` | 1282-1337 | XIf10. |
| C70.0-C72.9 (21) | `[3, 10]` | 1474-2156 | XIf10. A carcinoma here is a deposit in nearly every case (contract §0.1 point 4). Group III refers deposits and melanocytic tumours. Leaving 11 off avoids a third family choice at every brain site. |
| C75.2, C75.3 | `[3, 10]` | 1685, 1695 | XIf10; Group III and X midline. |
| C75.4, C75.5 | `[4]` | 2364, 2373 | XIf10; Group IV branch 7 refers here. |
| C76.3 | `[9, 10]` | 1526 | XIf11; a list, so 11 must be added for XIf11 at the pelvis. |

The 19 codes that already list 11 are C24.0, C24.8, C24.9, C51.0-C51.2, C51.8, C52.9, C54.0-C54.3,
C54.8, C54.9, C55.9, C57.8, C61.9, C68.8 and C75.1 (XIf10), plus the 38 XIb, XIc, XIe, XIf4,
XIf5, XIf7 and XIf8 codes counted in 3.1.

### 3.4 Group 10's Stage 1 additions

Added 7 October 2026 (audit of Group X, F-A-05) so that `9080/1` immature teratoma of the lung,
thymus and thyroid is recordable. Group 11 was listed in advance.

| Addition | Crosswalk row | Lookup | `candidate_groups` |
|---|---|---|---|
| Lung C34.0-C34.3, C34.8, C34.9 | `lung`, line 441 | 525-595 | `[2, 10, 11]` |
| Thymus C37.9 | `thymus`, line 460 | 597 | `[2, 10, 11]` |
| Thyroid C73.9 | `thyroid`, line 474 | 1381 | `[2, 10, 11]` |

Group 10 also added C62.0, C62.1 and C76.3, put 10 on C38.1, C38.3 and C48.0, and on 6 October
added the uterus and placenta (`docs/group_10_build_contract.md:225-235`,
`docs/group_10_registrar_review.md:196-200`).

### 3.5 Other topography defects seen

- C44.4 *Skin of scalp and neck* is absent. Groups IX and X therefore route nine skin codes, not
  ten (router 726-734, 872-880).
- C71.0 carries `redcap_code: null` (line 2156).

---

## 4. ICCC cross-group placement

### 4(a) Group XI-range codes that ICCC places in another group, by site

Only five non-Group XI ranges share any code with a Group XI range: 36 (IIIe1, 751), 50 (VIb,
649), 56 (VIIb, 220-221), 113 (Xd, 569 and 620-629) and 115 (Xd, 569). Counts are of the 230
usable codes.

| Site | Other group | Group XI codes placed there | Codes with no group at the site | Also at the site | Group 11 action |
|---|---|---|---|---|---|
| Liver C22.0, C22.1 | VII, VIIb (range 56) | 73: 8010-8015, 8020-8023, 8030-8035, 8041, 8050-8052, 8054, 8070-8075, 8082, 8120-8122, 8140-8141, 8143, 8155, 8158, 8190, 8200-8201, 8210-8211, 8230-8231, 8240-8241, 8244-8246, 8260-8263, 8310, 8320, 8323, 8401, 8430, 8440, 8470, 8480-8482, 8490, 8503-8504, 8510, 8550, 8560, 8562, 8570-8573 | 121 (among them 8290, 8130-8131, 8150-8154, 8247, 8452, 8580-8586, 9020) | 8000-8005 VIIc; 8160-8162 and 8170-8180 VIIb at any site | refer a carcinoma to Group VII; melanoma stays XId |
| Kidney C64.9 | VI, VIb (range 50) | 74: as the liver list, with 8130-8131, 8221 and 8290 and without 8158, 8470, 8503 | 120 (8158 among them) | 8000-8005 VIc; 8311, 8312, 8316-8319 VIb at any site | refer a carcinoma to Group VI |
| Ovary C56.9 | X, Xd (ranges 113, 115) | 93 (8044, 8123, 8153, 8158, 8213, 8221, 8243, 8290, 8380-8384, 8410, 8441, 8450, 8452, 8460-8461, 8576, 9000, 9014 among them) | 101 | 8000-8005 Xe; 8313, 8474, 9015 Xd and 8590-8671 Xe at any site | refer a carcinoma to Group X; melanoma, 8370 and the XIb codes stay Group XI |
| Testis C62.0, C62.1, C62.9 | X, Xd (range 113) | 86 (as the ovary without 8158, 8243, 8410, 8452, 8460-8461, 8576) | 108 | 8000-8005 Xe | refer a carcinoma to Group X |
| Pituitary C75.1 | III, IIIe1 (range 36) | 2: 8158, 8290 | 20 (the 19 skin-only codes and 8339) | 8270-8300 IIIe1 at any site (8272/3 pituitary carcinoma) | refer 8158 and 8290 at C75.1 to Group III; every other shared-list code is XIf10 here |
| Every other site, including C70-C72, C40-C41, C42, C47, C49 and C77 | none | 0 | see section 5 | — | no Group XI-range code is Group I, II, IV, V, VIII, IX or XII anywhere |

### 4(b) Entities other groups own that the clerk meets at Group XI sites

Group of each code from `ICCC-2017.sqlite`. Groups I-X are built; Group XII is not, so a referral
to XII shows the referral screen with no hop.

| Entity | ICD-O-3.2 | ICCC-2017 | Met at | Group 11 tree must |
|---|---|---|---|---|
| Phaeochromocytoma; paraganglioma | 8700/3; 8680-8693/3 | IVb, any site (range 44) | C74.x; C75.4-C75.5; C67; C30.1 | refer to IV (state the marker basis so the adrenal tree and `sa_ihc_checklist` do not send a case back and forth) |
| Neuroblastoma; ganglioneuroblastoma | 9500/3; 9490/3 | IVa, any site (43) | C74.x; C38.2-C38.3; C48.0 | refer to IV |
| Olfactory neuroblastoma, neuroepithelioma | 9522/3; 9523/3 | IVb (44) | C30.0; C31.x; C11 | refer to IV |
| Medulloepithelioma of the ciliary body | 9501-9504/3 | IVb outside C70-C72 and C77 (45); IIIc3 in the CNS | C69.4 | refer to IV |
| Retinoblastoma | 9510-9514/3 | V (46) | C69.2 | refer to V |
| Pancreatoblastoma | 8971/3 | XIIa2 (138) | C25 | refer to XII |
| Pleuropulmonary blastoma; pulmonary blastoma | 8973/3; 8972/3 | XIIa3 (139) | C34; C38.4 | refer to XII |
| Mesothelioma | 9050-9053/3 | XIIa5 (141) | C38.4; C48.1-C48.2 | refer to XII |
| Gastrointestinal stromal tumour | 8936/3 | XIIa1 (137) | C16-C18, C20 | refer to XII |
| Malignant mixed tumour; myoepithelial carcinoma; carcinosarcoma | 8940/3; 8982/3; 8980-8981/3 | XIIa4 (140) | C07-C08; C44; C50; C54 | refer to XII. Carcinoma ex pleomorphic adenoma `8941/3` and adenomyoepithelioma with carcinoma `8983/3` stay Group XI. Sialoblastoma is `8974/1` only (behaviour exclusion) |
| Endometrial stromal sarcoma; adenosarcoma; Müllerian and mesodermal mixed tumour | 8930-8935/3; 8950-8951/3 | XIIa4 (140) | C53; C54-C55; C52.9 | refer to XII |
| Mesonephroma, malignant | 9110/3 | XIIa6 (142) | C53; C52.9 | refer to XII |
| Germ cell tumours | 9060-9105/3 | Xb extragonadal; Xa C70-C72, C75.1-C75.3; Xc C56.9, C62; none at C77 | C37.9; C38.1-C38.3; C73.9; C52.9; C11 | refer to X |
| Lymphomas | 9590-9729/3 | Group II at these sites (9591 is Ia4 only at C42.0, C42.1, C42.3, C42.4) | C11; C37.9; C38.1; C07-C08; C73.9; C18.0 (Burkitt 9687, IIc); C69 adnexa | refer to II |
| Rhabdomyosarcoma | 8900-8920/3 | IXa (72) | C67; C61.9; C52.9; C53; C69.6; C11; C30-C31 | refer to IX |
| Other sarcomas | 9364/3; 8890/3; 9120/3; 8806/3; 8825/3; 8800-8805/3 | IXd2 (VIIIc2 in bone); IXd6; IXd8; IXd11; IXb1; IXe (VIIIe in bone) | every site | refer to IX |
| Kaposi sarcoma; dermatofibrosarcoma protuberans | 9140/3; 8832-8833/3 | IXc; IXd5 | C44 | refer to IX |
| Cutaneous lymphomas; Langerhans cell histiocytosis | 9700/3, 9709/3, 9718/3; 9751/3 | IIb3; IId | C44 | refer to II |
| Myeloid sarcoma | 9930/3 | Ib always (router 1654-1666) | C44; C69 | refer to I |
| Wilms tumour; rhabdoid tumour; clear cell sarcoma of kidney | 8960/3; 8963/3; 8964-8967/3 | VIa1; VIa2 at C64.9 (VIIa2 at C22, IXd3 elsewhere, none in the CNS and C77); VIa3 | C64.9 | refer to VI |
| Hepatocellular carcinoma; cholangiocarcinoma | 8170-8180/3; 8160-8162/3 | VIIb at any site (57) | C23.9; C24.x; C25; C16 | refer to VII; a Group XI biliary option must exclude 8160-8162 |
| Renal cell carcinoma | 8311, 8312, 8316-8319/3 | VIb at any site (51) | any | refer to VI |
| Sex cord-stromal tumours; seromucinous carcinoma; adenocarcinofibromas | 8590-8671/3; 8474/3; 8313/3, 9015/3 | Xe; Xd at any site (114, 116) | C54; C48; C57 | refer to X (`eg_other`, `group_10_dt.json:16370`, emits them at any site) |
| Pituitary carcinoma; pituitary blastoma | 8272/3, 8273/3 | IIIe1 at any site (37) | C75.1 | refer to III |
| Choroid plexus carcinoma | 9390/3 | IIIa2 (25) | C71.5 | refer to III |
| Craniopharyngioma | 9350-9352/1 | IIIe2 (38, behaviour 0-1,3) | C75.1-C75.2 | refer to III |
| Meningeal melanocytoma; melanocytosis | 8728/1; 8728/0 | none (XId is behaviour 3; no Group III range holds 8728) | C70.x | behaviour exclusions; registrar question |
| Malignant glomus tumour; glomangiosarcoma; malignant PEComa | 8711/3; 8710/3; 8714/3 | IXd11 at any site (92) | C44; C16; C54 | refer to IX. Contract §0.2 files 8710-8714 under Group IV; ICCC-2017 places them in IXd11 |
| Malignant struma ovarii; thyroid-type carcinoma in struma ovarii | 9090/3; 8330-8350/3 | 9090/3 Xc2 (107) at C56.9 and C62; 8330-8350 XIb at any site (121) | C56.9 | Group X codes 9090/3; a follicular or papillary carcinoma named in struma is XIb by ICCC (registrar question) |

All the epithelial and melanocytic `/3` codes in 8010-8799 that no Group XI range holds belong to
other groups at **every** site: VIIb 8160-8162, 8170-8175, 8180; IIIe1 8270, 8272, 8273, 8280,
8281, 8300; VIb 8311, 8312, 8316-8319; Xd 8313, 8474; Xe 8600, 8620, 8630, 8631, 8634, 8640,
8650, 8670; IVb 8680-8682, 8690-8693, 8700; IXd11 8710, 8711, 8714. `8339` alone is in no range.

---

## 5. Sites where a carcinoma enters no Group XI subgroup

### 5.1 The site-specific Group XI topographies

- **XIe** (range 124): `440-449, 519, 609, 632`: skin C44.0-C44.9, vulva NOS C51.9, penis NOS
  C60.9, scrotum C63.2. Specific vulvar and penile subsites (C51.0-C51.8, C60.0-C60.8) are XIf10.
- **XIf10** (range 134) includes `700-729` (brain, spinal cord, meninges) and `750-759` (the
  other endocrine glands, the pituitary among them). It excludes the adrenal `740-749`, the
  thyroid `739`, the nasopharynx `110-119`, skin `440-449`, the liver `220-221`, the kidney
  `649` and the gonads `569`, `620-629`.
- **XIf10 for 8158 and 8290** (range 135) excludes `700-729` and `751` and adds `519`, `609`,
  `632` (`510-529`, `570-619`, `630-639`).
- **XIf11** (range 136): `760-768, 809`, C76.0-C76.8 and C80.9.

### 5.2 Where a carcinoma has no Group XI subgroup

"No group" means `ICCC-2017.sqlite` holds no range for the pair, so the recode leaves it
unclassified.

| Sites | Carcinoma codes with no group | Malignant neoplasm NOS (8000-8005) | What ICCC does with a carcinoma | Group 11 action |
|---|---|---|---|---|
| Bone C40.0-C41.9 (13) | 194 of 230 | VIIIe (71) | unclassified | ask the primary; melanoma XId, 8370 XIa and the XIb any-site codes remain |
| Marrow, blood, spleen C42.0-C42.4 (5) | 194 | XIIb (143) | unclassified | ask the primary |
| Peripheral nerves C47 and soft tissue C49 (18) | 194 | XIIb | unclassified | ask the primary (Group IX branch 11 arrives here) |
| Lymph nodes C77.0-C77.9 (8) | 194 | XIIb | unclassified | ask the primary; unknown primary is C80.9, XIf11 |
| Adrenal C74.0, C74.1, C74.9 | 193 at C74.0; 194 at C74.1, C74.9 | XIIb | XIf10 excludes 740-749; only 8370-8375 (any site) and 8158 at C74.0 are XIa | adrenal tree emits 8370/3 at all three codes, 8158/3 only at C74.0 |
| Liver C22.0, C22.1 | 121 | VIIc | 73 codes VIIb | refer to VII |
| Kidney C64.9 | 120 | VIc | 74 codes VIb | refer to VI |
| Ovary C56.9; testis C62.x | 101; 108 | Xe | 93 and 86 codes Xd | refer to X |
| Thyroid C73.9 | 128 | XIIb | only the 81 codes of the XIb lists | thyroid tree offers XIb codes only |
| Nasopharynx C11 | 103 | XIIb | only the 91 codes of the XIc list (8240-8243 and 8150-8158 are not in it) | nasopharynx tree offers XIc codes only |
| Skin C44 | 119 | XIIb | only the 75 codes of the XIe list; 8158 and 8290 have no group at C44 | skin tree offers XIe codes only |
| CNS C70-C72; pituitary C75.1 | 22 (19 skin-only codes, 8339, 8158, 8290); 20 | IIIf | shared list is XIf10 | ask the primary: a carcinoma here is a deposit in nearly every case |
| Every non-XIe site (317) | 20 | by site | the 19 skin-only codes (8078, 8090-8095, 8097, 8100, 8102, 8110, 8390, 8400, 8403, 8407-8409, 8413, 8420) are XIe at the 13 XIe sites and unclassified elsewhere: a basal cell carcinoma at C51.0 has no group, at C51.9 it is XIe. 8339 is in no range anywhere | offer these only in the skin tree; 8339 follows standing rule 3 (XIb) |

---

## 6. Questions for the registrar

1. Meningeal melanocytoma `8728/1` and meningeal melanocytosis `8728/0` have no ICCC group.
   Behaviour exclusions in the melanoma tree, or registered as non-malignant intracranial
   tumours?
2. A follicular or papillary thyroid carcinoma arising in struma ovarii: `9090/3` Struma ovarii,
   malignant (Xc2, as Group X codes it), or the thyroid code at C56.9 (XIb by ICCC range 121)?
3. A carcinoma recorded at bone, marrow, soft tissue, lymph node or adrenal NOS has no ICCC
   group. Must the tool always ask the primary and record C80.9 when it is unknown (XIf11)?
4. Where is a nodal melanoma with no known primary recorded: at the node (C77.x, XId), or at
   C80.9?
5. Olfactory carcinoma and IDH2-mutant sinonasal carcinoma, named by the Group IV sinonasal
   referral, have no ICD-O-3.2 term. Which code do they take?
6. Group X `ov_deposit` sends "The primary is not known" to Group XII. Should a carcinoma or
   melanoma of unknown primary go to Group XI (XIf11 or XId at C80.9) instead?
7. Front door: list 11 at C74.0 and C74.9, C69.x, the XIf10 head-and-neck, thoracic, abdominal
   and genital sites, and on the "Mass / swelling", "Cutaneous / mucosal lesion" and
   "Lymphadenopathy" presentations? Leave the CNS sites and "Organ-functional sign" unchanged?
8. Should the referral reasons that overstate (section 1.3) be corrected in Groups VII, X and III
   in this branch, or handed to their own sessions?

## 7. Data gaps

- Labels and REDCap codes for the 155 missing topography codes need Layer 1
  `RedCap Options/Topography Redcap.md`, which this part did not read.
- The topography universe was built from the ICD-O-3 topography list in the analysis script. A
  check against the Layer 1 topography file confirms the 330 codes.
- The engine has never run a referral from a group to itself with `recapture_site`. If Group XI's
  R8 tree uses one, a browser walk has to prove it first.
