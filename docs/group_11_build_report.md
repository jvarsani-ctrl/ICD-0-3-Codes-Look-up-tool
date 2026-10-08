# Group XI — build report, 2026-10-08

**Branch:** `claude/group-11-carcinomas`, a worktree at `.claude/worktrees/group-11-carcinomas`, cut from
`main` at `7025128` (Groups I–X merged, the Group X audit fixes of pull request #14, the registrar's
obsolete-code ruling of 8 October 2026). Built on 8 October 2026; not committed or merged at the time of
writing.
Plan: `docs/group_11_build_contract.md` (decisions D1–D16). Evidence, one JSON and one Markdown file per
part: `docs/group_11_evidence/`. Questions for the registrar: `docs/group_11_registrar_review.md`.
REDCap-side list: `docs/group_11_layer1_repair.md` and `docs/TODO.md` §7 and §35.

| | |
|---|---|
| Entries | 230 (code, behaviour) pairs, all behaviour 3: 229 from the 2,183 ICCC-2017 records of ranges 118–136, and `8339/3` *Follicular carcinoma, encapsulated, angioinvasive*, a code ICD-O-3.2 added and no ICCC-2017 range holds (standing rule 3, D11) |
| Trees | 19 trees, 292 nodes: the eight organ trees (adrenal 15, thyroid 19, nasopharynx 16, salivary 15, colorectal 16, appendix 16, lung 19, thymus 23), the melanoma tree (15) and ten family trees (skin 14, breast 12, female genital 12, urinary and male genital 17, eye 11, head and neck 19, digestive 16, thoracic 11, endocrine 10, unspecified 16) |
| Node types | `histology_subclassification` 104 · `morphology_only` 85 · `clinical_alias` 38 · `lab_results` 32 · `document_inventory` 19 · `site_resolution` 8 · `ihc_checklist` 6 |
| Emitted | 217 (code, behaviour) pairs on code branches, all behaviour 3. The 13 pairs never emitted are the eleven whose every malignant ICD-O-3.2 term is `[obs]` (`8042`, `8124`, `8130`, `8141`, `8245`, `8251`, `8350`, `8440`, `8450`, `8508`, `8512`) and `8551/3`, `8780/3` (D3). 124 distinct pairs on exclusion screens, in 204 exclusion blocks |
| Pickers | 19, one per tree, 2,699 entries in all (D2) |
| Immunohistochemistry panels | 6 (`th_ihc`, `np_ihc`, `ty_ihc`, `hn_ihc`, `hn_sn_ihc`, `dg_ihc`), 15 rules, every rule with a witness |
| Aliases | 354 in `data/aliases/aliases_group_11.json` |
| Validator | four of the eight Group XI rules of contract §5 (rules 1, 2, 3 and 5) plus the registration changes in `build/build_database.py`; 20 negative controls and 10 probes in `build/negative_controls_group11.py`, all caught for the expected reason. Rules 4, 6, 7 and 8 are deferred (`docs/TODO.md` §35) |

---

## 1. What this group is, and the facts that reshaped it

ICCC-3 Group XI: adrenocortical carcinomas (XIa), thyroid carcinomas (XIb), nasopharyngeal carcinomas
(XIc), malignant melanomas (XId), skin carcinomas (XIe) and other carcinomas by site (XIf1 to XIf11:
salivary gland, colon and rectum, appendix, lung, thymus, breast, cervix, bladder, eye, other specified
sites, unspecified site). Ranges 118–136 of `ICCC-2017.sqlite`, all behaviour 3.

The registrar ruled on 8 October 2026 that the pathway is built directly into the tool, with no Diagnostic
Pathway document in the vault first, under six rules: every paper converted to text and marked for its
cancer; agents read snippets only; each agent reads only the files its part needs; only the controlling
session fetches more; WHO ICD-O-3 coding Rules A to K govern; conflicts with other groups are handled as
Group X handled them. The contract records the rules (contract header).

### ★ XIf1 to XIf11 differ only by site

Ranges 125–134 and 136 share one list of 174 codes and differ in topography alone (range 135 holds `8158` and `8290` only). One (code, behaviour) pair sits
in up to eleven subgroups, so every shared-list entry carries `iccc3_subgroup_by_topography` and is one
entry. The subgroup is computed from the recorded site at output (contract §0.1, §2).

### ★ Eleven codes have no current malignant term, and REDCap labels them as malignant

For `8042`, `8124`, `8130`, `8141`, `8245`, `8251`, `8350`, `8440`, `8450`, `8508` and `8512` every
`/3` term in ICD-O-3.2 is `[obs]`. `8130/3` *Papillary urothelial carcinoma* `[obs]` is the one that misstates the
evidence most: its current terms are `8130/1` *Papillary urothelial neoplasm of low malignant potential*
and `8130/2` *Papillary urothelial carcinoma, non-invasive*. Liu 2025 names the first among the two commonest
bladder neoplasms in children, so a clerk who matches the REDCap label registers a low-risk lesion as a Group XI
cancer. The eleven are entries and are never on a screen (D3, the registrar's Group X ruling of
8 October 2026). Where the WHO source names the current entity on the stem, the tree offers that entity's code:
`8243/3` *Goblet cell carcinoid* in place of `8245/3`, and `8260/3` *Papillary adenocarcinoma, NOS* for the diffuse
sclerosing subtype of papillary thyroid carcinoma.

### ★ ICD-O-3.2 changed three codes that a clerk will meet

- `8335/3` *Follicular carcinoma, minimally invasive* stays `/3`; the encapsulated tumour with no invasion
  is `8335/1` *Follicular tumor of uncertain malignant potential*, an exclusion; `8339/3` is the angioinvasive
  tumour. The thyroid tree asks the invasion (`th_ftc_invasion`).
- `8504/3` is now *Encapsulated papillary carcinoma with invasion*; the term REDCap labels `8504`,
  *Intracystic carcinoma, NOS*, moved to `8504/2`. The breast tree shows `8504/2` as an exclusion.
- `8023/3` *Nuclear protein in testis (NUT)-associated carcinoma* is new. It is an option on every tree whose
  site a source reports it at (D12) and a picker entry elsewhere.

### ★ No Group XI range covers seven families of site

The liver (C22, Group VII), kidney (C64, Group VI), ovary and testis (C56, C62, Group X), bone (C40–C41),
marrow (C42), soft tissue (C47, C49) and lymph nodes (C77) hold no Group XI code. A carcinoma recorded there is a
deposit in nearly every case and is coded at its primary (D10): each tree's deposit node refers to Group XI itself
with `recapture_site: true`, so the case re-enters at the primary's site. The contract (§0.1 item 3) also lists
the pituitary (C75.1) among these. That is wrong for the shared carcinoma list: range 134 of `ICCC-2017.sqlite`
ends `750-759`, which takes C75.1, and only range 135 (`8158`, `8290`) leaves it out. §7 item 4 follows from this.

---

## 2. The baseline

Group XI has no single WHO volume. Volume 10 covers the thyroid only (`docs/group_baseline_documents.md` §1),
and the registrar ruled on 8 October 2026 that the current WHO volume for each part is up to date whatever
its year: the breast (2019), digestive system (2019) and female genital (2020) volumes have no later edition.
Each part rests on its own volume, its International Collaboration on Cancer Reporting (ICCR) dataset and the
paediatric papers. The 48 PDFs were converted to page-marked text, tagged by cancer, in the vault at
`Group 11 Papers/text/` (`INDEX.md` lists them).

| Part | WHO volume, 5th edition | Summary paper | ICCR dataset |
|---|---|---|---|
| XIa adrenal cortex | Endocrine and Neuroendocrine Tumours, 2022 | Mete O, et al. Endocr Pathol 2022;33(1):155–196 | Adrenal Cortex, 2nd |
| XIb thyroid | Endocrine and Neuroendocrine Tumours, 2022 | Juhlin CC, Mete O, Baloch ZW. Endocr Relat Cancer 2023;30(2):e220293 | Thyroid, 3rd |
| XIc nasopharynx, oropharynx | Head and Neck Tumours, 2022 and 2024 | Badoual C. Head Neck Pathol 2022;16(1):19–30 | Oropharynx and Nasopharynx, 2nd |
| XId melanoma | Skin Tumours, 2025; Eye and Orbit Tumours, 2023 | Goldman-Lévy G, et al. Histopathology 2025; Milman T, et al. Ocul Oncol Pathol 2023;9(3–4):71–95 | Invasive Melanoma, 3rd |
| XIe skin carcinoma | Skin Tumours, 2025 | Goldman-Lévy 2025 | Merkel Cell Carcinoma, 2nd |
| XIf1 salivary gland | Head and Neck Tumours | Skálová A, et al. Head Neck Pathol 2022;16(1):40–53 | Major Salivary Glands, 2nd |
| XIf2 colon and rectum, XIf3 appendix, other digestive sites | Digestive System Tumours, 2019 | Nagtegaal ID, et al. Histopathology 2020;76(2):182–188 | Oesophagus, 3rd; Stomach, 3rd |
| XIf4 lung, pleura | Thoracic Tumours, 2021 | Nicholson AG, et al. J Thorac Oncol 2022;17(3):362–387; Sauter JL, et al. 2022;17(5):608–622 | Lung, 4th; Mesothelioma, 3rd (negative evidence: mesothelioma is XIIa5) |
| XIf5 thymus | Thoracic Tumours, 2021 | Marx A, et al. J Thorac Oncol 2022;17(2):200–213 | Thymic Epithelial Tumours, 3rd |
| XIf6 breast | Breast Tumours, 2019 | Tan PH, et al. Histopathology 2020;77(2):181–185 | Invasive Breast, 2nd |
| XIf7 cervix; vulva, vagina, uterus | Female Genital Tumours, 2020 | Höhn AK, et al. Geburtshilfe Frauenheilkd 2021;81(10):1145–1153 | Cervix; Vulva, 2nd; Vagina, 1st; Endometrial, 5th |
| XIf8 bladder; prostate, urinary tract, penis | Urinary and Male Genital Tumours, 2022 | Netto GJ, et al. Eur Urol 2022;82(5):469–482 (Part B) | Urinary Bladder, 2nd; Renal Pelvis and Ureter, 2nd; Prostate, 3rd; Penis and Distal Urethra, 2nd |
| XIf9 eye | Eye and Orbit Tumours, 2023 | Milman 2023 | none |
| XIf10 oral cavity, larynx, nasal cavity, neck | Head and Neck Tumours | Muller S, Tilakaratne WM. 2022;16(1):54–62; Zidar N, Gale N. 2022;16(1):31–39; Thompson LDR, Bishop JA. 2022;16(1):1–18; Hernandez-Prera JC. 2022;16(1):110–122 (all Head Neck Pathol) | Oral Cavity, 2nd; Hypopharynx, Larynx and Trachea, 2nd; Nasal Cavity, 2nd |
| XIf10 parathyroid | Endocrine and Neuroendocrine Tumours, 2022 | Erickson LA, et al. Endocr Pathol 2022;33(1):64–89 | Parathyroid, 2nd |
| NUT carcinoma, any site | cites Thoracic and Head and Neck | Luo J, Bishop JA, et al. Nat Rev Clin Oncol 2025;22:292–306; Lemelle L, et al. Eur J Cancer 2022 | none |
| Paediatric occurrence, every part | Paediatric Tumours, 2022 | Pfister SM, et al. Cancer Discov 2022;12(2):331–355, Table 3 | none |

Every part also rests on the WHO ICD-O-3.1 manual extract for Rules A to K, Visser 2023 Tables 3 and 4 for
registration without tissue, the IARC ICD-O-3.2 change documents, and
`Group 11 — ICD-O-3.2 Code Currency Check 2026-10-08.md` (the registrar ruled it carried into the pathway).
Every code was settled against `icdo32.sqlite`.

**Paediatric papers fetched from PubMed Central on 8 October 2026** (the registrar: "Fetch now, then build").
`INDEX.md` lists 14 files: Perez-de-Oliveira 2025 (salivary gland), Polat 2021 and Mahajan 2022 (colorectal),
Ozkan 2024 and Chen 2026 (lung), Rossi 2022 (thymus), Sosnowska-Sienkiewicz 2024 (breast), Huang 2019 and
Kaloga 2016 (skin), Wohlmuth 2021 (female genital tract), Ebrahim 2025 and Karges 2025 (pancreas),
Roganovic 2026 (appendix) and Liu 2025 (bladder). The registrar review counts 13. They have sections, not pages;
citations name the section. Four more papers are in PubMed Central but the publisher blocks the full text:
Ozolek 2021 (PMC8010056), Cortes-Santiago 2021 (PMC8010005), Cole 2023 (PMC10063734) and Sthapit 2025
(PMC12143885). They are requested in `docs/sources-requested.md`.

**Evidence process.** Fifteen evidence agents and eight addendum agents each read only their own text files,
through a 30-line snippet tool. A checker script verified every quotation on its cited page. An audit of the
agents' transcripts found no breach of the registrar's rules. Agents interrupted by a usage limit were re-run on
Sonnet 5.5.

---

## 3. Where the sources disagree

The evidence agents raised 140 questions and the paediatric addendum 47 more items. The build applies one
default per class, as Group X applied D1–D22. Part A of `docs/group_11_registrar_review.md` lists every instance;
the classes are:

| Point | The sources | Built, and why |
|---|---|---|
| ICD-O-3.2 and the WHO table code one term differently (A1), 15 instances | e.g. lymphoepithelial carcinoma `8082/3` against `8072/3` *Squamous cell carcinoma, large cell, nonkeratinizing, NOS*; thymic hepatoid or sebaceous carcinoma `8576/3`, `8410/3` against `8586/3` *Thymic carcinoma, NOS*; malignant adenomyoepithelioma `8983/3` against `8562/3` *Epithelial-myoepithelial carcinoma* | Mixed: ICD-O-3.2 in 5 instances, the WHO table in 4, both reachable in 2, held in 4. No D-number decides the class |
| A result elsewhere in the report decides what the diagnosis line leaves open (A2) | adrenal cortex, others | Yes in 3 places, no in 1 |
| No type or no human papillomavirus status named (A3) | | `8010/3` *Carcinoma, NOS*; `8070/3` *Squamous cell carcinoma, NOS*; `8120/3` *Transitional cell carcinoma, NOS* |
| Rule K against the WHO entity's single code (A4) | | The WHO entity's code where it has one (D5); Rule K where no single code covers |
| Obsolete terms and their successors (A5, A17) | `8260/3` *Papillary adenocarcinoma, NOS*; `8243/3` *Goblet cell carcinoid*; `8512/3`; `8551/3` and `8780/3` have a live term beside an `[obs]` Preferred term | Off every screen (D3) |
| Stated behaviour against printed behaviour (A6, A10, A11) | solid pseudopapillary neoplasm called benign; sialoblastoma called malignant | ICD-O-3.2's printed behaviour (D6): `8452/3` *Solid pseudopapillary neoplasm of pancreas*; exclusion `8974/1` *Sialoblastoma* |
| Codes the WHO or ICCR prints that ICD-O-3.2 lacks (A12, A13, A15, A16, A18) | `8976` gastroblastoma, `8483` and `8484` HPV-associated and HPV-independent adenocarcinoma, `9113` mesonephric-like adenocarcinoma, `8750/3` dermal melanoma | Not built (D4); a report that names one reaches the nearest generic option |
| Melanoma of the skin on clinical evidence in a child (A8) | Visser 2023 Table 3 | `8720/3` *Malignant melanoma, NOS* at basis 1 (D7) |
| Marker without tissue (A14) | Visser 2023 Table 4 | Offered at the lung, digestive tract and unknown primary (D7) |
| Adrenal cortical neoplasm of uncertain malignant potential (A7); `8158/3` *ACTH-producing tumor* at the adrenal cortex (A20) | Visser Table 4 has no adrenal cortical row | Excluded, no code named; `8158/3` off the adrenal screens (D16) |
| Thyroid-type carcinoma in struma ovarii (A19) | | `9090/3` *Struma ovarii, malignant*, Group X |
| Group X's ovary picker records `8452/3` (A21) | | Handed to the Group X session |
| Basis of diagnosis in three situations (A22) | | 7, 5 and 8 (D8, D15) |

Not built from the evidence: the codes the WHO or the ICCR prints that ICD-O-3.2 lacks (D4, the table above) and
every `clinical_alert` string (`docs/clinical-warnings.md`, Group XI). Each module's docstring in `build/group11_families/` and
`build/group11_organs/` lists its nodes and the changes made to the evidence's proposals; this report holds no
separate list of dropped nodes.

---

## 4. The trees

Approach 3 (registrar, 8 October 2026): organ trees where the WHO classification is organ-specific, one
melanoma tree that every site reaches, and general carcinoma trees written once and instantiated per site
family. The ten family trees are one module each in `build/group11_families/`; the eight organ trees and the melanoma
tree are in `build/group11_organs/`; `build/group11_tree.py` assembles them in contract §4.1 order, and
`build/group11_common.py` holds the shared builders. `python3 build/group11_tree.py --report` prints each tree's
node count and picker contents.

| Tree | Prefix | Routed topography | Nodes | Picker entries |
|---|---|---|---|---|
| `g11_adrenal` | `ad_` | C74.0, C74.1, C74.9 | 15 | 14 |
| `g11_thyroid` | `th_` | C73.9 | 19 | 73 |
| `g11_nasopharynx` | `np_` | C11.0–C11.9 | 16 | 95 |
| `g11_salivary` | `sg_` | C07.9, C08.0–C08.9 | 15 | 171 |
| `g11_colorectal` | `cr_` | C18.0, C18.2–C18.9, C19.9, C20.9, C21.0–C21.8 | 16 | 170 |
| `g11_appendix` | `ap_` | C18.1 | 16 | 173 |
| `g11_lung` | `lu_` | C34.0–C34.9 | 19 | 166 |
| `g11_thymus` | `ty_` | C37.9, C38.1–C38.3 | 23 | 171 |
| `g11_melanoma` | `me_` | none: every tree enters it by a cross-tree `next_node` (D13) | 15 | 19 |
| `g11_skin` | `sk_` | C44.0–C44.9, C51.9, C60.9, C63.2 | 14 | 91 |
| `g11_breast` | `br_` | C50.0–C50.9 | 12 | 167 |
| `g11_female_genital` | `fg_` | C51.0–C51.8, C52.9, C53.x, C54.x, C55.9, C57.x, C58.9 | 12 | 171 |
| `g11_urinary_male_genital` | `gu_` | C60.0–C60.8, C61.9, C63.0, C63.1, C63.7–C63.9, C65.9, C66.9, C67.x, C68.x | 17 | 175 |
| `g11_eye` | `ey_` | C69.0–C69.9 | 11 | 177 |
| `g11_head_neck` | `hn_` | C00–C06, C09–C10, C12–C14, C30–C33 | 19 | 161 |
| `g11_digestive` | `dg_` | C15, C16, C17, C23–C26 | 16 | 176 |
| `g11_thoracic` | `tx_` | C38.0, C38.4, C38.8, C39.x | 11 | 176 |
| `g11_endocrine` | `en_` | C75.0, C75.2, C75.4, C75.5, C75.8, C75.9 | 10 | 178 |
| `g11_unspecified` | `un_` | C76.x, C80.9, C70–C72, C48.x; the router default | 16 | 175 |

Every tree opens on a `document_inventory` evidence gate, and each evidence context has its own node, because
`app.js` replaces a captured `evidence_tests` list rather than merging it (Group X report §7 item 1). A tissue-free
or type-free route refers to Group XII with the `8000` family code. The exceptions are melanoma of the skin at
basis 1 (`8720/3`) and the Visser Table 4 marker codes at basis 4 (`8345/3`, `8240/3`, `8151/3`–`8156/3`,
`8241/3`, `8158/3`), recorded only on the trees whose sites the marker concerns (D7). Cytology that names an entity records it at basis 5;
suspicious cytology is not registrable (D8).

Each histology screen lists the paediatric entities first (D1: an entity a source reports at ages 0–18),
then the generic options, then melanoma, NUT carcinoma, "another carcinoma the report names" (the picker),
"a tumour the report calls benign, borderline or in situ" (the exclusion screen), a deposit and "not a
carcinoma". An entity whose code depends on a further answer (invasion, subtype, grade, human papillomavirus
status, behaviour) is an option wherever it occurs, because the picker cannot ask.

**The picker** (D2) is Group X's gonadal carcinoma picker applied per tree: one `histology_subclassification` node
with `prefill_filter_from_search`, listing every code ICCC-2017 places in Group XI at the tree's routed sites plus
the codes standing rule 3 places there, each under its ICD-O-3.2 Preferred term, with ICD-O-3.2 synonyms and
related terms in `search_terms`. It leaves out the all-`[obs]` codes and the codes the tree already offers as
options. The clerk types the tumour's name into the list's own filter box.

**Rule H site corrections.** Eight `site_resolution` nodes capture a corrected `topography` (D9): an adrenal
cortical carcinoma recorded at C74.9 becomes C74.0; a thymic epithelial tumour reported in the anterior
mediastinum becomes C37.9; carcinoma of the skin of the arm becomes C44.6.

**The six immunohistochemistry panels** resolve the entities a source gives a rule for, each rule citing its
page: the thyroid (`th_ihc`), nasopharynx (`np_ihc`), thymus (`ty_ihc`), head and neck (`hn_ihc` and the sinonasal
panel `hn_sn_ihc`) and digestive tract (`dg_ihc`). `python3 build/induce_flow.py` gives each a `branch_sequence`
and fails if a rule has no witness.

---

## 5. Shared-layer changes

| File | Change |
|---|---|
| `presentation_router.json` | `groups["11"]` built: `occurs_at_routed_sites: true`, the 19 trees, 18 `tree_routing` rules (each rule's `topography_in` computed from ICCC-2017 against the lookup, never typed) and default `g11_unspecified`; `dual_group_rules` for `8158` and `8290` gained a Group XI branch per subgroup, written by `build/apply_group11_shared_layer.py`; the other branches of both rules are left to their owners |
| `topography_codes.json` | 153 lookup codes added (salivary glands C07–C08, colon and rectum C18–C21, breast C50, lip and oral cavity C00–C06 and the rest), each from `Topography Redcap.md`, with `candidate_groups: [11]`; 11 added to 57 existing codes. `C44.4` and `C48.1` are not added: the REDCap topography list has neither (REDCap-side list, `docs/TODO.md` §7) |
| `group_10_dt.json` | Group X's extragonadal routing and its 18 topography-dependent entries regenerated to name the new sites. Group X rule 4 requires each routing list to equal ICCC-2017's site family exactly, so that check fails without it |
| `negative_controls_group10.py` | control R4-E's expected reason updated to the regenerated routing list (one line) |
| `build_database.py` | `GROUP11 = 11`; `BEHAVIOUR_DECLARED_BY_GROUP[GROUP11] = {"3"}`; `GROUP11` in `ROUND_TRIP_GROUPS`; four rules (§6); `check_refer_terminals` admits `refer_group` equal to the file's own group only on a branch with `recapture_site: true`; `parse_classification_subgroups` reads two-digit subgroups (`XIf10`, `XIf11`) and a Group XII heading with no colon. Group X helpers parameterised by group, not copied |
| `alias_index.json` | regenerated by the build and committed (standing rule 15) |
| `docs/validator_negative_controls.md` | the Group XI section |

New files: `build/generate_group11_entries.py`, `build/group11_common.py`, `build/group11_families/`,
`build/group11_organs/`, `build/group11_tree.py`, `build/apply_group11_shared_layer.py`,
`build/generate_group11_aliases.py`, `build/negative_controls_group11.py`, `data/database/group_11_dt.json`,
`data/aliases/aliases_group_11.json`, `docs/evidence_documents/group_11.json`, the contract, this report, the
registrar review, the Layer 1 repair package and `docs/group_11_evidence/`.

`app.js`, `index.html`, `uccf-tool.css` and every Group I–IX data and alias file are byte-identical to `main`.

---

## 6. Rules this group adds

| Rule | Asserts | Source |
|---|---|---|
| `check_group11_codes_fit_site` (1) | every emitted (code, behaviour) lies in a Group XI range covering every routed site of every tree that reaches the node, or no range of any group holds it there (D11); no exclusion lies in such a range; the melanoma tree's emissions lie in an XId range | `ICCC-2017.sqlite`, router |
| `check_group11_no_pathology_codes` (2) | on a path with neither Histology nor Cytology, basis 1 emits only `8720/3` and only in `g11_skin`; basis 4 emits only a Visser Table 4 pair with Imaging and Tumour markers on the path; nothing reaches basis 2, 5, 7 or 8 | the walked path (`_group8_terminals_by_evidence`); Visser 2023 |
| `check_group11_obs_never_emitted` (3) | none of the eleven all-`[obs]` pairs, nor any pair whose ICD-O-3.2 Preferred term is `[obs]` (`8551/3`, `8780/3`), is emitted | `icdo32.sqlite` |
| `check_group11_subgroups_and_routing` (5) | the subgroup `app.js` shows equals ICCC-2017's at every lookup code; each routing list equals exactly the sites contract §4.1 assigns; the default is `g11_unspecified`; a lookup code that lists 11 and no rule routes is a NOTE (C75.1) | `ICCC-2017.sqlite`, router, lookup |

Twenty controls, recorded in `docs/validator_negative_controls.md`: R1-A to R1-D, R2-A to R2-D, R3-A and R3-B,
R5-A to R5-F, and REG-A to REG-D for the registration changes. R1-A (a hepatic code `8170/3` in the lung tree) and
R2-B (the histology tier captures only Imaging; the path, not the flag, decides) are the two the contract names.

**Deferred by the registrar's trim, 8 October 2026** (`docs/TODO.md` §35): contract §5 rule 4 (every code has a
route), rule 6 (alias terms match ICD-O-3.2, site form), rule 7 (picker aliases stay unshared) and rule 8
(deposits recapture), and the generalisation of the engine-gate picker sweep to every `prefill_filter_from_search`
node.

---

## 7. What the walks and the browser found

**The walk.** A script in the session scratchpad (`walk_g11.py`) walked every terminal of the 18 routed trees:
57,000 to 127,000 (ticked set, path) terminals per tree, 0 failures. It checks that the evidence captured on
every path equals the reports the clerk ticked, the check that found Group X's erased evidence (Group X report §7
item 1).

**The browser.** One case driven end to end: "Medullary thyroid carcinoma" by search, organ system Thyroid gland,
the Group XI thyroid tree, Histology Report, Medullary thyroid carcinoma, giving `8345/3` *Medullary thyroid
carcinoma*, topography 739, subgroup XIb, basis 7, "Also called" C cell carcinoma and Medullary carcinoma with
amyloid stroma. The remaining browser cases of contract §9 item 6 were not driven in this build.

**Found by the controlling session, and not seen by the build or the walk:**

1. **The front door omits Group XI.** The guided route narrows a presentation's group list by the site's
   list, and the presentations do not name Group XI. Details in §8 item 1 and `docs/TODO.md` §35.2.
2. **Group X's gonadal carcinoma picker holds 224 generic carcinoma strings** ("Carcinoma, NOS",
   "Adenocarcinoma, NOS", "Squamous cell carcinoma, NOS", "Papillary carcinoma of thyroid", "NUT carcinoma",
   "Mucoepidermoid carcinoma" and others). Group X rule 8 forbids sharing a string, so Group XI does not alias
   them, and a typed carcinoma term at a Group XI site enters Group X or stops. Details in §8 item 2 and `docs/TODO.md` §35.3.
3. **The search box does not reach 53 sites** a Group XI case otherwise reaches only by referral: bone, liver,
   soft tissue, lymph node, gonad, kidney, C71.0 and C75.3. The engine's `occursAtRoutedSites()` ignores the
   router default (`docs/TODO.md` §35.4).
4. **C75.1 lists Group 11 and no rule routes it.** It reaches the default tree; the build prints a NOTE
   (`docs/TODO.md` §35.5).
5. **The Layer 1 Markdown rows for XIe, XIf1, XIf2 and XIf11 are malformed**: the tokens `C80.90-C80.98` and
   `C80.98` stand for `8090-8098` and `8098`, and the table omits `8090`–`8095`, `8097` and `8339`. The build
   prints 12 warnings for it. The ligature "ft" is printed "!" in `Topography Redcap.md` for the REDCap codes 058,
   113, 186 and 696. Both are repairs in the vault (`docs/group_11_layer1_repair.md` §9; `docs/TODO.md` §1.3 and §35.6).
6. **A tissue-free referral to Group IV** (neuroblastoma with raised catecholamines) **or Group X** (raised
   alpha-fetoprotein or human chorionic gonadotropin) **is a hint, not an option**, because a tissue-free path
   may refer only to Group XII (D7; `docs/TODO.md` §35.7).
7. **Myeloid sarcoma is not offered as a site-keeping Group I referral** in the Group XI trees
   (`check_leukaemia_referrals_record_marrow` lists the nodes; `docs/TODO.md` §35.8).

---

## 8. What needs you

`docs/group_11_registrar_review.md`, ordered by cost. Part E (your decisions) is empty. The first three:

1. **The front door.** Group XI is not offered under "Mass / swelling" (98 routed sites: thyroid, lung, thymus,
   nasopharynx, skin, cervix, brain and others), "Cutaneous / mucosal lesion" (87 sites; at the skin the list
   narrows to Groups IX and II), "Lymphadenopathy" (76) or "Organ-functional sign" (38). Adding 11 to those
   presentations as data would remove other groups at some sites. The fix is an `app.js` feature, a
   presentation-level list of groups added back only where the site lists them (as `keep_on_site` does for a
   discriminator), and it belongs to the "ICD Overall fixes" session. Until then Group XI is reachable through the
   search box, "Incidental imaging finding", "Not sure" and referrals from other groups. Review B5
   asks for your rulings on it: whether 11 belongs on the site lists, and whether the three presentations gain it.
2. **The search-term collision.** Typed at a site that lists Groups 10 and 11, a generic carcinoma string enters
   Group X's extragonadal tree, which refers the carcinoma on to Group XI; typed at a Group XI-only site it
   stops. The guided route codes these carcinomas correctly. The fix needs two things: you relax Group X rule 8
   so both groups may file the strings, and an `app.js` tie-break by the entries' `primary_sites` (the "ICD
   Overall fixes" session). Review B6 items 1 to 6 hold the other alias questions, including Group VI's nine
   strings and the lay organ terms.
3. **Part A of the review, 22 items that change which code a case gets.** The defaults built:
   - **A1.** ICD-O-3.2 or the WHO table when they code one term differently. Mixed today; one principle would replace the mixture.
   - **A2, A3.** A stain or gene result printed elsewhere in the report may decide what the diagnosis line leaves open (yes in 3 places, no in 1). A carcinoma that names no type records `8010/3`, `8070/3` or `8120/3`.
   - **A4.** Rule K against a WHO entity's single code: the WHO entity's code (D5).
   - **A5, A17.** Obsolete terms stay off every screen, including `8551/3` *Acinar cell cystadenocarcinoma* and `8780/3` *Blue nevus, malignant*, whose Preferred term is `[obs]` beside a live term.
   - **A6, A10, A11.** Stated behaviour against printed behaviour follows ICD-O-3.2 (D6): a solid pseudopapillary neoplasm called benign records `8452/3`, and a sialoblastoma called malignant is the exclusion `8974/1`.
   - **A7.** An adrenal cortical neoplasm of uncertain malignant potential is excluded with no code named.
   - **A8.** Melanoma of the skin of a child on clinical evidence records `8720/3` at basis 1.
   - **A9.** Keratoacanthoma records `8071/3` *Squamous cell carcinoma, keratinizing, NOS*, flagged as held.
   - **A12, A13, A15, A16, A18.** Entities the WHO prints and ICD-O-3.2 lacks are not built (D4).
   - **A14.** A marker without tissue is offered at the lung, digestive tract and unknown primary.
   - **A19 to A22.** Struma ovarii carcinoma stays in Group X; `8158/3` stays off the adrenal screens; Group X's ovary picker records `8452/3` and is handed to that session; basis 7, 5 and 8.

Also open, in `docs/TODO.md` §35 with what closes each: the search box's 53 unreached sites (§35.4), C75.1
(§35.5), the Layer 1 table rows (§35.6), the tissue-free hint to Groups IV and X (§35.7) and the myeloid sarcoma
option (§35.8). The
four restricted PubMed Central papers and the WHO volumes the data gaps name are in `docs/sources-requested.md`.
The REDCap side, with its relabels, retirements, 12 appended codes and two topography codes, is in
`docs/group_11_layer1_repair.md`; the tool does not act on it (standing rule 16).

---

## 9. Proof

| Gate | Result |
|---|---|
| `python3 build/build_database.py` | BUILD PASSED — 1,321 checks: 577 OK, 90 NOTE, 104 WARN, 0 FAIL (8 October 2026). Group XI adds 12 warnings from the malformed Layer 1 rows and 13 from the pairs whose ICD-O-3.2 Preferred term is `[obs]`; Group X's report gave 79 on 6 October 2026, and 79 plus 25 is 104 |
| Engine gate (`node build/check_engine_flow.mjs`, run inside the build) | passes |
| `python3 build/induce_flow.py --check` | every immunohistochemistry checklist rule has a witness |
| `python3 build/negative_controls_group11.py` | 20 of 20 caught for the expected reason, 10 of 10 probes pass |
| `python3 build/negative_controls_group10.py` | 41 of 41 caught, 8 of 8 probes pass |
| Groups III, VII, VIII, IX and UX controls | each behaves |
| Walk of every terminal of the 18 routed trees | 0 failures; 57,000 to 127,000 terminals per tree |
| Browser | one case, §7 |
| `app.js`, `index.html`, `uccf-tool.css`, Groups I–IX | byte-identical to `main` |

Not run for this report: the build, the controls and the browser were run by the controlling session on
8 October 2026 and recorded here as it reported them. The remaining browser cases in contract §9 item 6 and the
`generate_group11_entries.py --check` and `apply_evidence_documents.py --check` runs are not in the record.
