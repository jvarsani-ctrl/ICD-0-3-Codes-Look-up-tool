# Group 11 cross-group map, part B: the alias layer, the validator, and the Group 10 lessons

**Written 8 October 2026** on branch `claude/group-11-carcinomas` (worktree identical to `main` at
`7025128`). Read: the repository, `ICCC-2017.sqlite`, `icdo32.sqlite`, the Group XI inventory
(`g11_inventory.json`, 229 usable codes plus `8339/3`), and
`ICD Look Up tool/Group 11 — Alias Build Instructions.md` (14 May 2026). Nothing was fetched and nothing
outside this file and `cross_group_B.json` was edited. A full build of a scratch copy of the tree passed
(1162 checks, 0 FAIL, 79 WARN), so every line number below is from code that runs green today.

Machine-readable form: `cross_group_B.json` (same sections).

---

## 0. One correction to the brief

The vault router says an alias shared by two groups enters the lowest-numbered one because `app.js`
takes `hit.groups[0]`. **That stopped being true on 4 October 2026.** `handleOption('alias')`
(`app.js` L2768–2810) sends a term filed under more than one group to the site question, and
`afterSearchSite()` (L3309–3330) intersects the term's groups with the site's `candidate_groups`:

- one survivor enters that group;
- several survivors stop the case ("The site does not decide the group", `renderSearchUnresolved`);
- no survivor stops it ("…is not a site that group codes this term at"), unless exactly the right
  group is `occurs_at_any_site` (Group II) or passes `occursAtRoutedSite()` (Group X, L3284–3294).

`occursAtRoutedSite()` applies only to a term filed under **one** group, only at a site one of the
group's own `tree_routing` rules names (the default does not count), and only when an entry for one of
the alias's `maps_to_morphology_codes` lists the site in `primary_sites`. A code-less alias can never
use it. `hit.groups[0]` survives only for a single-group term (L2791).

So the cost of a shared alias is a **stop at every site that lists both groups**, and the cost of an
unshared alias is a **stop at every site that lists neither**. "Also called" is unaffected across
groups: `aliasesFor()` (L2648) reads `state.aliases`, the current group's own file only.

---

## 1. Alias collisions

### 1.1 The numbers

- 536 live (not `[obs]`) ICD-O-3.2 Preferred, Synonym and Related terms sit at `/3` on the 230 Group XI
  codes. 238 of them are already alias strings in another group's file: **227 in Group 10, 9 in
  Group 6, 4 in Group 3** (some in two).
- `alias_index.json` holds 1,699 keys, 51 filed under more than one group.
- Lookup sites that list Groups 10 and 11 together (where a shared Group 10/11 term ties): **27** —
  C34.0–C34.3, C34.8, C34.9, C37.9, C51.0–C51.2, C51.8, C51.9, C52.9, C53.0, C53.1, C53.8, C53.9,
  C57.8, C54.0–C54.3, C54.8, C54.9, C55.9, C73.9, C75.1.
- Lookup sites that list 11 without 10: 30 (C11.x, C24.x, C44.x, C61.9, C67.x, C68.8).

### 1.2 Group 10 — the gonadal carcinoma picker's 183 aliases (rule 8 applies)

Group 10 files 232 aliases on Group XI codes, all `maps_to_iccc3_subgroup_id` Xd, all entering
`g10_extragonadal` by the router. 183 of them map to the **75 codes only the two picker nodes emit**
(`ov_carcinoma_other`, `ts_carcinoma_other`; computed with `_group10_emissions` and
`prefill_filter_from_search`). Among them are the strings Group 11 needs most:

| String(s) | Code | Group 11 home |
|---|---|---|
| Papillary carcinoma of thyroid | 8260 | thyroid (also "Papillary renal cell carcinoma", a kidney term) |
| Hurthle cell carcinoma, Hurthle cell adenocarcinoma, Follicular carcinoma, oxyphilic cell, Oncocytic adenocarcinoma | 8290 | thyroid |
| Lymphoepithelial carcinoma, Lymphoepithelioma, Lymphoepithelioma-like carcinoma, Schmincke tumor | 8082 | nasopharynx |
| Mucoepidermoid carcinoma | 8430 | salivary gland |
| Adenoid cystic carcinoma, Adenocystic carcinoma, Thymic carcinoma with adenoid cystic carcinoma-like features | 8200 | salivary gland, thymus |
| Acinar cell carcinoma, Acinar carcinoma, Acinic cell adenocarcinoma, Acinar adenocarcinoma, NOS | 8550 | salivary gland |
| NUT carcinoma, NUT midline carcinoma, Nuclear protein in testis (NUT)-associated carcinoma | 8023 | any carcinoma site |
| Sebaceous carcinoma, Sebaceous adenocarcinoma | 8410 | skin |
| Squamous cell carcinoma, NOS and its 20 variants | 8070–8075 | skin, nasopharynx, cervix, every site |
| Small cell carcinoma, NOS; Small cell neuroendocrine carcinoma; Small cell carcinoma, pulmonary type | 8041 | lung, every site |
| Large cell neuroendocrine carcinoma | 8013 | lung |
| Goblet cell carcinoid, Mucinous carcinoid, Mucocarcinoid tumor | 8243 | appendix |
| MANEC, Mixed adenoneuroendocrine carcinoma | 8244 | colorectum |
| Solid pseudopapillary neoplasm of pancreas, Solid pseudopapillary carcinoma | 8452 | pancreas |
| Transitional cell carcinoma, NOS; Urothelial carcinoma, NOS | 8120 | bladder |
| Signet ring cell carcinoma, Hepatoid carcinoma, Gastrinoma, Enterochromaffin cell carcinoid … | 8490, 8576, 8153, 8241 | various |

Group 10 rule 8 (`check_group10_picker_aliases_stay_unshared`, `build_database.py` L10085) **fails the
build** while any of these strings is held by another group. `generate_group10_aliases.py` gives a
picker-only string to the group that already holds it (`other_groups_aliases`, L275; the hand-over at L351–352). So these cannot be
shared: either Group 10 keeps them or Group 11 takes them.

**What Group 11 does:** files each one that is an ICD-O-3.2 term true at every site Group 11 emits the
code (see §1.6 for the site test), then reruns `build/generate_group10_aliases.py`, which drops them from
Group 10. Two consequences need the registrar:

1. Typed at the ovary or testis, these strings then stop (Group 11's entries do not list C56.9 or
   C62.x; Group 10 is no longer filed). The picker still finds them through its own filter box once the
   clerk is in Group X. This is the trade rule 8 already accepted for six Group VI and three Group III
   strings (TODO §34, third review finding 1).
2. The engine gate's picker sweep asserts `pairs > 100` (`check_engine_flow.mjs` L1063–1077, reading
   `aliases_group_10.json`). After the transfer the sweep finds **45** pairs (computed against today's
   data) and fails. The check must be re-keyed before the transfer lands (§3).

Today, the effect of these strings sitting in Group 10 is visible: "thyroid" typed in the search box
matches one alias, "Papillary carcinoma of thyroid" [10]; at C73.9 it enters Group 10's extragonadal
germ cell tree.

### 1.3 Group 10 — 49 strings on 13 codes Group 10 also emits on named options

`8010` (ov_epithelial, ts_histology), `8020`, `8044`, `8140`, `8310`, `8380`, `8441`, `8460`, `8461`,
`8470`, `8480` (ov_epithelial), `8240`, `8246` (ov_other, ts_other). Strings: "Carcinoma, NOS",
"Carcinoma, undifferentiated, NOS", "Anaplastic undifferentiated carcinoma", "Carcinoma, poorly
differentiated, NOS", "Dedifferentiated carcinoma", "Adenocarcinoma, NOS", "Adenocarcinoma, usual
type", "Neuroendocrine tumor, NOS", "Carcinoid tumor, NOS", "Carcinoid, NOS", "Typical carcinoid",
"Neuroendocrine tumor, grade 1", "Neuroendocrine carcinoma, low grade", "Neuroendocrine carcinoma,
well differentiated", "Bronchial adenoma, carcinoid", "Neuroendocrine carcinoma, NOS", "Poorly
differentiated neuroendocrine neoplasm", "Clear cell carcinoma, NOS", "Clear cell adenocarcinoma, NOS",
"Clear cell adenocarcinoma, mesonephroid", "Mucinous adenocarcinoma", "Mucinous carcinoma", "Colloid
carcinoma", "Colloid adenocarcinoma", "Mucoid carcinoma", "Mucoid adenocarcinoma", "Mucinous
cystadenocarcinoma, NOS" and its four relatives, "Endometrioid carcinoma, NOS" and two relatives,
"Serous carcinoma, NOS" and six relatives, the low- and high-grade serous strings, and the three
`8044` small cell, hypercalcaemic type strings.

Rule 8 does not apply. If Group 11 files the same string the index lists it under `[10, 11]`
(`[6, 10, 11]` for the two `8240` strings) and the case **stops at all 27 shared sites**, which include
the thyroid, lung and thymus organ trees. If Group 11 does not file it, the term enters
`g10_extragonadal` at those sites (its `tree_routing` names C34.x, C37.9, C73.9, C53.x, C54.x) and
reaches Group 11 only through `eg_other` → "Another carcinoma, or a melanoma", after a germ cell
evidence gate and histology screen.

**What Group 11 does:** leaves the ovary-named and serous/endometrioid strings with Group 10 outright
("Small cell carcinoma of the ovary, hypercalcaemic type", the serous family). For the generic
carcinoma and neuroendocrine strings neither default is acceptable. The fix is one group-agnostic engine
change, handed to the "ICD Overall fixes" session: **when several groups survive the site, keep only the
groups whose own entries for the alias's codes list the site in `primary_sites`** — the evidence test
`occursAtRoutedSite()` already applies to single-group terms. Every other group's entry for a shared
code is site-bound (Group 10: C56.9, C62.0–C62.9; Group 6: C64.9; Group 3: C75.1; Group 7: C22.0,
C22.1), so the tie-break settles every collision in this section, §1.4 and §1.5. Until the registrar
approves it, the 49 strings stay with Group 10 and Group 11 does not file them.

### 1.4 Group 6 — nine strings

"Medullary carcinoma, NOS" (8510), "Neuroendocrine tumor, NOS" and "Carcinoid tumor, NOS" (8240, already
`[6, 10]`), "Vipoma" (8155), "Encapsulated papillary carcinoma with invasion" (8504), "Urothelial
carcinoma, sarcomatoid" and "Transitional cell carcinoma, spindle cell" (8122), "Urothelial carcinoma,
micropapillary" and "Transitional cell carcinoma, micropapillary" (8131). Also held, not to be copied:
"Papillary urothelial carcinoma" and "Papillary transitional cell carcinoma" (8130, every `/3` term
`[obs]`), "Vipoma, malignant" (not an ICD-O-3.2 term), "Intracystic carcinoma, NOS" (code-less; 8504/2).

Group 6 reads no site (no `tree_routing`, no `when.topography`), so each of these is entered in
Group 6 at every site today, the site only recorded. Filed under Group 11 too, it becomes a multi-group
term: Group 6 at C64.9, Group 11 at its own sites, and a stop everywhere else, including the eight
`route_by_morphology` codes (C76.x, C80.9), where both survive. Rule 8's review called the same shift a
defect for Group 10 (174 sites). For Group 11 it puts thyroid medullary carcinoma, pancreatic vipoma and
bladder urothelial variants in the right group. **Registrar decides**; the tie-break of §1.3 does not
change it (it acts only where several groups survive).

### 1.5 Group 3 — four strings, plus two code-less thyroid strings

"ACTH-producing tumor" (8158), "Oncocytic carcinoma" and "Oxyphilic adenocarcinoma" (8290), and
"Papillary carcinoma, follicular variant" (code-less in Group 3; the ICD-O-3.2 Preferred term of
8340/3). Group 3 also files "Papillary carcinoma, encapsulated" and "Papillary carcinoma, columnar cell
type" code-less; their notes say the strings belong to Group XI. The ICD-O-3.2 forms are "Papillary
carcinoma, encapsulated, of thyroid" (8343/3) and "Papillary carcinoma, columnar cell" (8344/3).

Group 3 reads the site and has no `occurs_*` flag, so these stop today wherever the site omits 3 —
the thyroid among them. Shared with Group 11 they enter Group 11 at C73.9 (and C74.0 once it lists
11) and **tie at C75.1** (candidate groups 3, 10, 11), where Group 3 enters today. ICCC-2017 range 135
places 8158 and 8290 in XIf10 at `750, 752-759` and not at 751, so the primary-sites tie-break settles
C75.1 for Group III. `dual_group_rules` already carry `8158` and `8290` with C75.1 → Group 3 and
default Group 11 (and 8158 at C22 → Group 7).

**What Group 11 does:** files the four, and asks the Group 3 session to delete Group 3's three
code-less thyroid strings once Group 11 holds the thyroid terms.

### 1.6 The site version of design D21

D21 (Group 10 spec) forbids an alias true of one behaviour on a code emitted at several, because "Also
called" is keyed by four-digit code. Group 11 emits every code at `/3`, so the behaviour test is
trivially met. Its own form of the fault is **site**: one code sits in up to eleven subgroups, and an
alias naming one organ prints under "Also called" on that code's output at every site. ICD-O-3.2
carries such terms on shared codes, for example "Papillary carcinoma of thyroid" and "Papillary renal
cell carcinoma" (8260), "Parathyroid carcinoma", "Acinar adenocarcinoma of prostate", "Endolymphatic
sac tumor" and "Carcinoma of Skene, Cowper and Littre glands" (8140), "Clear cell renal cell carcinoma,
NOS" (8310), "Acinar adenocarcinoma of lung" (8551), "Juvenile carcinoma of breast" (8502), "Papillary
carcinoma of breast" (8503), "Intrapulmonary thymoma" (8580), "Intrathyroid thymic carcinoma" (8589),
"Small cell carcinoma, pulmonary type" (8041), "Pseudomyxoma peritonei with unknown primary site"
(8480), "Bronchial adenoma, carcinoid" (8240).

**Rule for the Group 11 generator:** an organ-naming term becomes an alias of its code only when every
Group 11 tree that emits the code is that organ's tree; otherwise it is a code-less alias (searchable,
never on "Also called") or left out. Kidney terms ("Papillary renal cell carcinoma", "Clear cell renal
cell carcinoma, NOS", "Mucinous tubular and spindle cell carcinoma") name a Group VI tumour and are left
out. The organ lay terms ("Thyroid cancer", "Skin cancer", "Lung cancer", "Nasopharyngeal carcinoma",
"Salivary gland carcinoma") are code-less for the same reason. A code-less alias cannot use
`occurs_at_routed_sites` (§0), so it reaches Group 11 only where the site lists 11.

### 1.7 Other groups, abbreviations and terms not to copy

| String | Held by | Action |
|---|---|---|
| "Adrenal tumour" (9500, 8700), "Adrenal medullary paraganglioma", "Extra-adrenal paraganglioma" | 4 | Typing "adrenal" lists these first. C74.0 lists Group 4 only, so a Group 11 adrenal cortical term stops at C74.0 until 11 is listed there or Group 11 is `occurs_at_routed_sites`. Do not alias "Adrenal cancer". |
| "Eye cancer" (9510) | 5 | Do not copy. C69.0–C69.9 list Group 5 (and 4, 9), not 11, though XIf9 and the melanoma ranges cover the eye. |
| "Malignant melanoma of soft parts" (9044, clear cell sarcoma) | 9 | A Group IX tumour; Group 11 neither aliases it nor treats it as melanoma. |
| "Myoepithelial carcinoma" (code-less; 8982/3 is ICCC XIIa4) | 9 | The salivary tree refers myoepithelial carcinoma to Group XII; no Group 11 alias. |
| "EMC" (extraskeletal myxoid chondrosarcoma) | 9 | Do not use "EMC" for epithelial-myoepithelial carcinoma. |
| "MANEC" | 10, picker-only | Transfers with §1.2. |
| "HCC", "cHCC-CCA" | 7 | Not Group 11. ICCC-2017 range 57 places 8170 in VIIb at sites 000-809. |
| "… of the liver" strings (NUT carcinoma, neuroendocrine tumour, ACTH-producing tumour, vipoma, hepatic carcinoma) | 7 | No collision; Group VII's site-qualified naming is the pattern that avoids ties. |
| "ACC" | none | Three Group XI entities (adrenal cortical carcinoma, adenoid cystic carcinoma, acinar cell carcinoma). Not aliased, as Group 10 did not alias "GCT". |
| "NET", "NEC" | none | Family names; typing "NET" also lists DNET, PNET, PitNET. Code-less, or the NOS code only. |
| "PTC", "MEC", "IDC", "ALM" | none | Exact keys free; substring search also lists PTCL [2], MECOM-rearranged AML [1], 29 "…oid carcinoma" strings, 19 "…alm…" strings. The exact alias sorts first (shortest), so no tie. |
| "Epithelial tumor, malignant", "Heterotopia-associated carcinoma" | none (Group 10 `EXCLUDED_TERMS`) | Group 11's own `8010` terms; free to file. |

Search shows the eight shortest matching keys (`searchAlias`, L507). Several hundred Group 11 aliases
change what "carcinoma", "adenocarcinoma" and "melanoma" show; the index is already 53,657 bytes against
the 30 KB guideline (build WARN, TODO §24).

---

## 2. What the Group 11 Alias Build Instructions get wrong

The file predates the rulings of 4 September to 8 October 2026. Each item names the entry.

**Collisions and routing**
1. Entry 2 "ACC": three Group XI entities share it (§1.7).
2. Entry 3 "Adrenal cancer" → 8370: in a child the commonest adrenal malignancy is neuroblastoma
   (Group IV); the alias overstates (standing rule 8). C74.0 lists Group 4 only, and typing "adrenal"
   lists Group 4's "Adrenal tumour" first.
3. Entries 7–8, 16, 23–30, 56–60, 64, 67–68, 79–80 name strings Group 10 holds (§1.2, §1.3); entry 16's
   also_known_as "Oncocytic carcinoma" and "Oxyphilic adenocarcinoma" are Group 3's (§1.5); entry 11
   maps to 8510, Group 6's "Medullary carcinoma, NOS".
4. Entry 80 "Carcinoma NOS" (no comma) is not the ICD-O-3.2 string; it creates a second index key beside
   Group 10's "Carcinoma, NOS" and both appear for "carcinoma nos".
5. Challenge 1–2 and §0 items 2–3: "site-specific aliases ('colon adenocarcinoma')" mapped to a shared
   code print under "Also called" at every site (§1.6). "Anchored to its most clinically expected site"
   and `maps_to_iccc3_subgroup_id` do nothing: the field is dead (TODO §17), the express lane asks the
   site, and the subgroup is computed at output.
6. §4 "ihc_tree_id null": Groups 9 and 10 set `ihc_tree_id` and `tree_entry_node` to the router's
   handoff tree for a group with `tree_routing`; `check_alias_cross_references` resolves both.
7. Entries 62–63 and 73–74: C18–C21 and C50 are not in `topography_codes.json`, so the express lane
   cannot record a colorectal or breast site at all (§4).

**Multi-code aliases**
8. Entries 5–6 (12 codes), 7–8 (7), 9–10 (4), 23–24 and 27 (7), 47–48 (8), 49–50 (7), 54 (3), 57 (6),
   62–63 (8), 64 (4), 65–66 (6–7), 70 (6), 72 (7), 73–74 (4), 77 (6), 78 (3), 79 (4): each puts its
   string under "Also called" on every output of every listed code at every site. A replica of Group 10
   rule 3 fails entry 70: "Thymoma" equals "Thymoma, NOS" (8580/3) and ICD-O-3.2 does not file it under
   8581–8585. Entry 47–48 maps "Basal cell carcinoma" to 8094 *Basosquamous carcinoma* and 8095
   *Metatypical carcinoma*, other entities.

**Codes ICD-O-3.2 changed or marks `[obs]`**
9. Entry 4 "Adrenal cortical tumor" → 8158, 8370–8375: 8371–8375 exist only at `/0` (adenomas);
   "Adrenal cortical tumor" is an ICD-O-3.2 synonym of 8370/0, benign — a behaviour exclusion, not an
   alias.
10. Entries 9–10 FTC → 8335: "Follicular carcinoma, encapsulated" is now 8335/1; 8335/3 is "Follicular
    carcinoma, minimally invasive"; 8339/3 "Follicular carcinoma, encapsulated, angioinvasive" is new
    and missing.
11. Entry 11 also_known_as "Parafollicular Cell Carcinoma": `[obs]` synonym of 8345/3.
12. Entry 45 "Malignant blue nevus" → 8780: the Preferred term "Blue nevus, malignant" is `[obs]`; the live
    synonym is "Melanoma arising in blue nevus".
13. Entry 53 "Bowen disease" → 8081: ICD-O-3.2 has 8081/2 only; the note "included in ICCC-3 as /3 at
    certain sites" is false (the inventory lists 8081 among codes absent at `/3`).
14. Entry 58 also_known_as "Mucoepidermoid Tumor": 8430/1, `[obs]`.
15. Entry 59 also_known_as "Cylindroma": `[obs]` synonym of 8200/3, and 8200/0 is "Eccrine dermal
    cylindroma", benign.
16. Entries 65, 69 "Bronchioloalveolar carcinoma", "BAC": the ICD-O-3.2 synonyms ("Bronchiolo-alveolar
    carcinoma, NOS") are `[obs]`; the Preferred term is "Lepidic adenocarcinoma" (8250/3).
17. Entry 67 also_known_as "Oat cell carcinoma": 8042/3, whose every `/3` term is `[obs]`.
18. Entry 78 maps 8482, whose synonym "Mucinous adenocarcinoma, endocervical type" is `[obs]`.
19. Entry 79 maps 8130, whose every `/3` term is `[obs]` (design D11 keeps it off every screen).
20. §5 "8170 … XIf10 for non-hepatic sites": ICCC-2017 range 57 places 8170 in VIIb at sites 000-809.
21. Entry 1 also_known_as: ICD-O-3.2 also files "Endocrine tumor, functioning, NOS" under 8158/3 as
    `[obs]` — not to be used for the 8158 entry.

**Strings that are not ICD-O-3.2 terms** (keep as curated aliases only where §1.6 allows; give the
ICD-O-3.2 term as well): "Adrenocortical carcinoma" (ICD-O-3.2: "Adrenal cortical carcinoma"),
"Papillary thyroid carcinoma", "Follicular thyroid carcinoma", "Anaplastic thyroid carcinoma",
"Undifferentiated thyroid carcinoma", "Nasopharyngeal carcinoma", "Undifferentiated nasopharyngeal
carcinoma", "Non-keratinizing / Keratinizing nasopharyngeal carcinoma", "Acral lentiginous melanoma"
(ICD-O-3.2: "Acral melanoma", synonym "Acral lentiginous melanoma, malignant"), "Mucosal melanoma"
(8746 is *mucosal lentiginous* melanoma; a mucosal melanoma not so called is 8720/3 — the alias
overstates), "Epithelioid melanoma" ("Epithelioid cell melanoma"), "Melanoma in giant congenital nevus"
("Malignant melanoma arising in giant congenital nevus"), "Squamous cell carcinoma of skin", "Acinic cell
carcinoma" ("Acinar cell carcinoma"), "Polymorphous low grade adenocarcinoma" / "PLGA" ("Polymorphous
adenocarcinoma"), "Goblet cell adenocarcinoma" (not offered by the file but the WHO name), "Invasive
ductal carcinoma" (ICD-O-3.2 synonym "Invasive breast carcinoma of no special type"), "Malignant
Thymoma", "Type C Thymoma" ("Thymoma, type C"). Entry 34 "Superficial spreading melanoma" is now a
Related term; the Preferred term is "Low cumulative sun damage melanoma".

**Standing rule 9 (the tool is global)**
22. §0 item 7 (line 32), item 8 (line 34) and the entry notes at lines 341, 343, 345, 347, 349 and 353
    frame the tool regionally: "critical in high-EBV-prevalence regions", "dominant form in those
    settings", "disproportionately important in East Africa", "widely used in East African clinical
    practice", "the standard classification in this region". None goes into an alias note.

**Omissions**
23. No alias for 8023 NUT carcinoma, 8452/3 solid pseudopapillary neoplasm (pancreas only; ICD-O-3.2
    codes the ovarian tumour 8452/1), 8249 *Neuroendocrine tumor, grade 2* (TODO §33: no group offers
    it), 8339/3, 8770/3 "Malignant Spitz tumor" / "Spitz melanoma". The note on entries 73–76 calls
    8502 "Secretory carcinoma" too rare to alias; it is the breast carcinoma of children and also the
    salivary entity, and ICD-O-3.2 files "Juvenile carcinoma of breast" under it.
24. The `confidence` column is not in the alias schema Groups 8 to 10 write. NCIt Title Case in
    also_known_as prints verbatim under "Also called" and is never searched (only `alias` is indexed).

---

## 3. The validator

### 3.1 Checks that apply to Group 11 with no change

All run per file in `run_build()` (L12722–12850) or cross-layer (L12852–12868):

| Check | Line | Note for Group 11 |
|---|---|---|
| `check_node_types` | 2035 | closed vocabulary |
| `check_nos_fallback_by_node_type` | 2054 | required on `ihc_checklist`, `numeric_gate`; explicit null elsewhere |
| `check_orphan_nodes` | 2193 | cross-tree `next_node` counts, so the melanoma tree may be reached only from site trees |
| `check_node_ids_unique_and_prefixed` | 2155 | prefix from each tree's entry node; two trees may not share one. Each instance of the general carcinoma tree needs its own prefix |
| `check_fallback_chains`, `check_next_node_resolution`, `check_terminal_codes_exist`, `check_duplicate_code_behavior_pairs`, `check_metadata_counts` | 1948–2118 | |
| `check_refer_terminals` | 2320 | includes the `recapture_site` shape (L2403–2412) |
| `check_deposit_referrals` | 9791 | keyed off node ids containing deposit/metast and `DEPOSIT_TRIPWIRE` words |
| `check_leukaemia_referrals_record_marrow` | 9844 | any referral into Group I |
| `check_tick_lists` | 11495 | every tree's entry evidence gate must carry a `tick_list` |
| `check_lab_results` | 11376 | a laboratory screen never chooses a code |
| `check_recognition_aids` | 11698 | aids only on select-then-confirm lists without a tick list |
| `check_evidence_mapping` | 11724 | **silent OK when `docs/evidence_documents/group_11.json` is absent** — write the mapping, or the gates are never compared |
| `check_satisfies_tests`, `check_basis_of_diagnosis`, `check_imaging_pathway_shape` | 2771, 5229, 7039 | |
| `check_no_clinical_alerts` | 11014 | ruling 9 |
| `check_flow_charts` | 11029 | `induce_flow.py` witnesses; rerun after any `resolution_logic` edit |
| `check_ihc_checklist_renders_a_control`, `check_marker_names_verbatim`, `check_declared_states_consumed`, `check_no_internal_identifier_leaks` | 11114, 11208, 11233, 567 | |
| `check_codes_against_source_of_truth` | 10851 | 8339/3 passes as a NOTE (in ICD-O-3.2, outside every ICCC range) |
| `check_iccc_subgroup_ranges` | 10965 | **blind for Group 11**, see below |
| `check_override_affordance` | 11768 | |
| `check_presentation_router`, `check_routing_narrows` (incl. `occurs_at_routed_sites` shape, L12092–12106), `check_router_branch_when_vocabulary`, `check_alias_cross_references`, `regenerate_alias_index` | 12118, 11956, 12246, 12464, 1588 | |
| engine gate `run_engine_gate` → `check_engine_flow.mjs` | 12610 | the express-lane sweep computes every (term, site) outcome from the index and the topography file |

Two generic checks run only for registered groups: `check_behaviour_exclusion` (L6433, reads
`BEHAVIOUR_DECLARED_BY_GROUP`) and `check_icdo32_round_trip` (L6041, reads `ROUND_TRIP_GROUPS`). The
round trip only WARNs when `morphology_name` is an `[obs]` term: Group 11 will carry 13 such WARNs (the
eleven obs-only codes, and 8551, 8780 if they take their Preferred term).

`check_iccc_subgroup_ranges` reads the Layer 1 markdown through `parse_classification_subgroups`
(L10926–10927). Its `sub_re` (`[IVX]+[a-z]\d?\b`) does not match "XIf10" or "XIf11", so those rows are
filed under XIf9; and the Layer 1 heading "## XII Other And Unspecified …" has no colon, so `head_re`
files every Group XII row under group 11 (the flat parser at L1541 does the same). An entry declaring
XIf10 or XIf11 is never checked, and an XIf9 entry holding an XIf10-only code passes. Four tokens
(`C80.90-C80.98`, `C80.98`) also WARN as malformed. Group 11 must verify subgroups from
`ICCC-2017.sqlite` (§3.2 rule 4) and the parser fix is a one-character change; the heading is a Layer 1
repair.

### 3.2 Checks Group 10 added for itself that Group 11 must replicate

Each is guarded `if ctx.group != GROUP10: return []` and keyed to Group 10 names. The helpers hard-code
the group: `_group10_iccc_ranges` (L9588, `main_group = 'X'`), `_group10_tree_routing` (L9683,
`groups["10"]`). Parameterise them by group rather than copy them.

| # | Group 10 function (line) | Group 11 rule |
|---|---|---|
| 1 | `check_group10_codes_fit_site` (9695) | every emission lies in a Group XI range covering the tree's sites. **Difference:** the melanoma tree has no routing rule, so a node's sites must be the union of the routed sites of every tree that can reach it by `next_node`; Group 10's per-tree lookup would give the melanoma tree no sites and FAIL |
| 2 | `check_group10_no_pathology_codes` (10147), walk `_group8_terminals_by_evidence` (9010, group-agnostic, passes `lab_results`) | tissue-free paths: basis 1 only `8720/3` at C44 (Visser Table 3); basis 4 only the Visser Table 4 pairs (8345/3, 8240/3, 8151/3, 8152/3, 8153/3, 8155/3, 8156/3, 8241/3, 8158/3) with Imaging and the marker evidence on the path; every other no-tissue case refers to Group XII (`8000/3` is not a Group XI code) |
| 3 | `check_group10_alias_terms_match_icdo32` (10520), `_group10_term_key` (10512) | every ICD-O-3.2-term alias maps to the code ICD-O-3.2 files it under; plus the site test of §1.6 |
| 4 | `check_group10_subgroups_and_routing` (10625) | `iccc3_subgroup_by_topography` gives ICCC-2017's subgroup at every lookup topography; each organ tree's rule names exactly ICCC's sites; every lookup code from which Group 11 can be entered is named by a rule. The generic `check_iccc3_subgroup_by_topography` (6277) is guarded to Group 3 (L6293) and will not do it |
| 5 | `check_group10_referrals_carry_the_right_site` (9878) | node ids hard-coded; Group 11 writes its own for deposit and tissue-site referrals (a carcinoma or melanoma deposit in brain, bone, liver, lymph node) |
| 6 | `check_group10_terms_offered_where_allowed` (9935) | node plan hard-coded; Group 11's version asserts the WHO Rule H terms each organ tree must offer |
| 7 | `check_group10_every_gonadal_carcinoma_has_a_route` (9979), `_icdo_preferred_obsolete` (10078) | every Group XI code ICD-O-3.2 prints live at `/3` has an option at each site ICCC places it; no option records an obsolete pair; `search_terms` are live Synonym/Related terms |
| 8 | `check_group10_picker_aliases_stay_unshared` (10085) | Group 11's picker-only aliases are held by no other group |
| — | `check_group9_obs_unreachable` (9486), `GROUP9_OBS_ONLY` (9164) | `GROUP11_OBS_ONLY` = 8042, 8124, 8130, 8141, 8245, 8251, 8350, 8440, 8450, 8508, 8512 never emitted |
| — | `check_group9_code_set` (9176), `GROUP9_CODES` (9146) | a `GROUP11_CODES` anchor typed from the inventory, never read back from the file |
| — | `check_group9_leaf_claims` (9497) | each entry's coding_note claim about reachability derived from the tree |
| — | `check_group7_router_c22` (8788) | the `dual_group_rules` for 8158 and 8290 resolve to the ICCC subgroup (XIa at C74.0, XIb at C73.9, XIf10 elsewhere, Group III at C75.1) |

`check_brain_marker_cutoffs` (10372, Groups III and X) and `check_visser_table4_gate` (7315, Group IV)
apply only if Group 11 reads numbers; a `numeric_gate` for calcitonin or chromogranin A needs its own
walk check and an `other_unit` band.

### 3.3 Registration

- `GROUP11 = 11` after `GROUP10` (L776), above `BEHAVIOUR_DECLARED_BY_GROUP` (module load order).
- `BEHAVIOUR_DECLARED_BY_GROUP[GROUP11] = {"3"}` (L794): ICCC-2017 ranges 118–136 declare behaviour 3 on
  every row (verified 8 October 2026). Without it every Group 11 `behaviour_exclusion` (8335/1, 8504/2,
  8336/1, 8103/1, 8370/0, 8371–8375/0 …) goes unchecked.
- `ROUND_TRIP_GROUPS` (L823) gains `GROUP11`.
- The new rules registered after the Group 10 block in `run_build()` (after L12825).
- Generators: `build/generate_group11_entries.py` (Group 10's pattern: reads `ICCC_DB`/`ICDO_DB`,
  `carry_branch_sequences`, applies `docs/evidence_documents/group_11.json`, `--check`, converts the
  inventory's en dashes in `primary_sites` to hyphens), `build/group11_tree.py`,
  `build/generate_group11_aliases.py`, `build/negative_controls_group11.py`; a Group 11 section in
  `docs/validator_negative_controls.md`.
- Router `groups["11"]`: `built`, `trees`, `tree_routing` with a rule naming every lookup code Group 11
  can be entered from and a default, `handoff`, and the `occurs_at_routed_sites` decision.
- `topography_codes.json`: 57 lookup codes where a Group XI site range applies omit 11 (C74.0; C69.0–C69.9;
  C70.0–C72.9; C75.2–C75.5; C30.0–C31.9; C38.1–C38.3; C48.0–C48.8; C58.9; C63.0–C63.9; C76.3); 31
  ICD-O-3 topography headings holding a Group XI site range have no lookup code (C00–C10, C12–C17,
  C18–C21, C23, C25, C26, C32, C33, C39, C50, C60, C65, C66), so the salivary and colorectal organ trees
  and every breast case have no site to be entered at.
- `check_engine_flow.mjs`: the picker sweep (L1020–1090) names Group 10's nodes and asserts
  `pairs > 100` from `aliases_group_10.json`; generalise it to every `prefill_filter_from_search` node.
- Regenerate `aliases_group_10.json` after writing `aliases_group_11.json` (rule 8), then the build,
  then commit `alias_index.json` (standing rule 15).

---

## 4. The Group 10 lessons, applied from the start

| # | Lesson | Group 11 from the start |
|---|---|---|
| 1 | **Evidence erased between nodes.** `capture()` replaces `evidence_tests`; three paths lost a report (report §7 item 1; TODO §29). | One node per evidence context in every tree (referral, referral after cytology, imaging, imaging after markers, imaging after cytology), and a terminal walk comparing each terminal's evidence with what the clerk ticked. |
| 2 | **The stop screen at routed sites** said a site was not one the group codes the term at, though ICCC placed it there (report §7 item 2; B1). | List 11 at the 57 lookup codes of §3.3, or mark Group 11 `occurs_at_routed_sites` with rules naming them; add the 31 missing headings. |
| 3 | **"Also called" keyed by four-digit code** (D21; TODO §30). | The site form of D21 (§1.6) in the generator and in rule 3. |
| 4 | **Generic search terms stopping at shared sites** (report §7 item 4; `EXCLUDED_TERMS`). | §1.3–§1.5; request the primary-sites tie-break; keep a Group 11 `EXCLUDED_TERMS` with a reason per string. |
| 5 | **Laboratory screens** (E2): a tier a Lab Report can join gets a copy requiring Lab Report, through a `lab_results` screen, to the tier's destination; values never choose a code. | Per-tree test lists with a source and page each (thyroid: calcitonin, carcinoembryonic antigen, thyroglobulin; adrenal cortex: cortisol, dehydroepiandrosterone sulfate, testosterone, 17-hydroxyprogesterone; neuroendocrine: chromogranin A, urinary 5-hydroxyindoleacetic acid, the hormones of Visser Table 4); the rules in `docs/evidence_documents/group_11.json`. |
| 6 | **The picker** (A11): every code a tree does not otherwise offer, under its Preferred term, `search_terms` the live Synonym and Related terms, `prefill_filter_from_search`. | The natural form for the shared XIf list. Rules 7 and 8 replicated; the engine gate's picker sweep generalised before Group 11's picker exists. |
| 7 | **Obsolete codes on screen** (design D11; registrar 8 October 2026). | The eleven obs-only codes are entries, never options. 8551 and 8780 have an `[obs]` Preferred term and a live synonym: registrar question. |
| 8 | **`recapture_site`** for deposits; leukaemia referrals record C42.1; an unknown primary records C80.9 and goes to Group XII. | Every deposit option in Group 11 (XIf10 includes the brain) carries it; `check_deposit_referrals` finds deposit nodes by id and words, so name deposit nodes `*_deposit`. |
| 9 | **`occurs_at_routed_sites`** reads the alias's codes and the entries' `primary_sites`, single-group terms only. | `primary_sites` one range per list item, ASCII hyphen (the engine gate's `covers()` splits on "-"; an en dash makes "C11.0–C11.9" cover C11.0 only while `app.js` covers all six). Code-less aliases rely on `candidate_groups`. |
| 10 | **Brain marker gates**: SIOP cut-offs, a test with no result read as not raised, an `other_unit` band, a walk check. | Group 11 codes on the report's word "raised" (Visser Table 4) unless the registrar rules cut-offs; any `numeric_gate` gets the `other_unit` band and a walk check. |
| 11 | **A referral to a built group continues there with the case's site** (6 October 2026). | 17 inbound branches (Groups II, III, IV, VII, VIII, IX, X) land in Group 11 once it is built, some at sites no Group XI carcinoma range covers (Group IX soft tissue, Group X ovary and testis without recapture). Group 11's router must route every such topography and its trees must refer a carcinoma there onward. |
| 12 | **The subgroup line at a site outside every range** (F-A-04). | Choose the entry default deliberately (XIf11 at C76.x/C80.9 is ICCC's own); compute `topography_in` from ICCC ranges against the lookup, never typed. |
| 13 | **Checks that tested destinations, not conditions**; five controls added after review; controls pinned to a pre-fix commit. | Write the negative controls with the rules; one per rule face. |
| 14 | **Three independent reviews found defects after a green build**; the third swept 297,325 (term, site) cells against `main`. | Run the same diff sweep before and after adding `aliases_group_11.json`, and drive the browser. |
| 15 | **Regeneration order.** Entries generator (applies the evidence mapping) → `induce_flow.py` → aliases generator → `generate_group10_aliases.py` → `build_database.py` (rewrites `alias_index.json`) → commit the index. Group VIII must not be regenerated from `group08_tree.py`. | Same order; never hand-edit generated JSON. |
| 16 | **Stale `app.js` in the preview browser.** `index.html` L55 loads `app.js` by a plain script tag; only the JSON is fetched `no-cache` (`app.js` L177–186). | Force-reload and confirm a new function exists before judging a walk. |
| 17 | **Worktree builds need `ICD_LAYER1`, `ICCC_DB`, `ICDO_DB`**; `generate_group06_entries.py` reads module defaults only. | Export the three; every Group 11 generator reads the environment first. |
| 18 | **Build every tree, then verify once** (standing rule 12). | Same. |
| 19 | **Recognition aids**: one sentence, source and page in a comment, shown under the selected option only. | Same, with the options left without an aid listed for the registrar. |
| 20 | **Mixed tumours**: a named term first, then a `first_match` component checklist with a witness per option. | Mixed medullary–follicular (8346), medullary–papillary (8347), mixed neuroendocrine–non-neuroendocrine (8244, 8154). |
| 21 | **A Group 10 defect found here.** The ovary picker offers 8452/3 "Solid pseudopapillary neoplasm of pancreas"; ICD-O-3.2 codes the ovarian tumour 8452/1. | Hand to the Group 10 session and the registrar; Group 11 offers 8452/3 at the pancreas only. |
