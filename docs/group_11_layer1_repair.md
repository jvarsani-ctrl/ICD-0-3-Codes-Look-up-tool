# Group 11 — Layer 1 Repair Package (REDCap `xi_morph`)

**Written 8 October 2026 with the Group 11 build.** Input for the REDCap Registry repository,
which owns every change to the registry's dictionary (routing table in `../../CLAUDE.md`).
Nothing here edits REDCap. Live REDCap is production and is written only on the registrar's
approval of a specific change.

**The lookup tool does not act on this list.** Standing rule 16 (registrar, 4 October 2026): the
tool does not connect to REDCap, and no check, flag or fix in it tests what REDCap holds. The
clerk reads the answer and picks the option by hand. This package exists so the REDCap side can
repair the dropdown; the tool needs none of it.

**Source.** `ICD coding/RedCap Options/Group 11- Other Malignant Epithelial Neoplasms And Malignant
Melanomas.md`: 503 option lines in six lists (XIa, XIb, XIc, XId, XIe, and one consolidated list for
XIf1 to XIf11), **282 distinct numbers**. Two numbers carry a second label in the XIf list (§9.2).
`ICD coding/RedCap Options/Group 11 - Unique codes.md` and `xi_morph` in
`REDCap Registry/snapshots/2026-10-01/data_dictionary.csv` are identical: 282 choices, one per number,
with the same labels character for character. The tables below classify those 282 labels against
`icdo32.sqlite` (IARC final table, 9 October 2020) and `ICCC-2017.sqlite`, and read what the tool does
from the 230 entries of `data/database/group_11_dt.json` and the evidence files in
`docs/group_11_evidence/`. The tables are a script's output, not a transcription. Every ICD-O-3.2 term in
them is read from `icdo32.sqlite`.

**Method.** Seven scripts in the session scratchpad
(`/private/tmp/claude-501/-Users-jay-Ai-Environment-Cancer-Registry-ICD-Look-Up-tool-ICD-Lookup/747dd8f2-ef3f-4f1c-b29b-4c7843301e8b/scratchpad/`):
`g11_layer1_sources.py` reads and compares the option file, the unique-codes file and the snapshot;
`g11_layer1_classify.py` classifies each option; `g11_layer1_tables.py` prints the tables;
`g11_layer1_vs_currency.py` compares the classes with the code currency check; `g11_layer1_calc.py`
reads the `xi_subgroup` formula (§10); `g11_layer1_assemble.py` writes this file from
`g11_layer1_template.md` and the printed tables; `g11_layer1_verify.py` checks every relabel and append
string against the current behaviour-3 terms in `icdo32.sqlite`. All read the databases and the vault
read-only.

**The tool column is the specification, not a walk of the built trees.** When this was written,
`group_11_dt.json` held its 230 entries and no tree. "Option: thyroid" means the evidence part names
the code as a screen option (contract D1). A part name is its evidence file: `thyroid` is
`XIb_thyroid.json`, `endocrine/unspecified` is `XIf10_parathyroid_other_unspecified.json`, `urinary` is
`XIf8_urinary_male_genital.json`, `NUT` is `NUT_carcinoma.json`, and the others follow the same
pattern; contract §4.1 maps each part to its trees. "Picker" means the code reaches the clerk only
through a tree's picker, which lists every current behaviour-3 code that ICCC-2017 places in Group XI
at the tree's sites (contract D2). "Off every screen" is contract D3. Check the column against the
built trees before applying a row.

**What a change costs.** In the snapshot the choice code of every `xi_morph` option is the
four-digit number itself, so the dropdown holds one row per number. Relabelling a row changes no
stored value. `xi_subgroup` and `xi_extended` compute from the number and `topo_code` (§10). A row
carries no behaviour digit, so its label should name the number's behaviour-3 term, which is what the
lookup tool shows.

| Class | Options | What |
|---|---|---|
| A | 157 | the ICD-O-3.2 Preferred term at behaviour 3, which is current — correct as a label. 11 of them sit on numbers ICCC-2017 places in another group (class H) |
| B | 31 | a behaviour-3 term that is not the Preferred term — relabel. 25 are current terms (B1); 6 are terms ICD-O-3.2 marks `[obs]` on a number whose Preferred term is current (B2) |
| C | 22 | drift: not an ICD-O-3.2 term at that number. 14 carry "malignant" where the behaviour-3 Preferred term has none (C1); 6 differ in punctuation or a qualifier (C2); 2 are ICD-O-3.2 terms of another number, `8441/3` (C3) |
| ★ D | 7 | a benign, borderline or in situ term on a number the tool emits at behaviour 3 |
| E | 50 | ICD-O-3.2 prints no behaviour-3 term on the number. The tool shows 25 as exclusions under that term (E1), 1 under another term on the number (E2), and does not show 24 (E3) |
| ★ O | 15 | obsolete. 13 numbers whose every behaviour-3 term is `[obs]` (O1): ten of the eleven in contract §0.2 and the three pituitary numbers. 2 numbers whose Preferred behaviour-3 term is the `[obs]` label, beside a current synonym or related term (O2) |
| F | 0 | no "Label not found" row. The option file drops `8085`, `8086` and `8157` with a note instead (§7.3) |
| ★ G | 12 missing | codes the tool emits that no option names |
| ★ H | 16, inside A to O | numbers ICCC-2017 places in another group at every site: 10 in VIIb, 6 in IIIe1 |

A to O add up to the 282 options; class A is listed in §14 so the count can be audited. The five
that most misstate the evidence are §1: `8130`, `8504`, `8335` with `8339`, `8023` and `8770`.

---

## 1. ★ The five that most misstate the evidence

### 1.1 `8130` — a label with no current malignant term, on the number of the commonest paediatric bladder lesions

| | |
|---|---|
| Option string | `Papillary transitional cell carcinoma` (the XIb, XIc and XIf lists) |
| ICD-O-3.2 | `8130/3` Preferred *Papillary urothelial carcinoma* `[obs]`; Synonym *Papillary transitional cell carcinoma* `[obs]`, the option string. Every behaviour-3 term on the number is `[obs]`. Current on the number: `8130/1` Preferred *Papillary urothelial neoplasm of low malignant potential*; `8130/2` Preferred *Papillary urothelial carcinoma, non-invasive*. `8120/3` Preferred *Transitional cell carcinoma, NOS*, Synonym *Urothelial carcinoma, NOS* |
| What the tool does | `8130/3` is an entry and is off every screen (contract D3; registrar's ruling on Group 10 review A11, 8 October 2026). The urinary part shows `8130/1` and `8130/2` as exclusions and records an invasive papillary urothelial carcinoma as `8120/3` Transitional cell carcinoma, NOS: the WHO 2022 table prints `8130` only at behaviours 1 and 2 (Netto 2022, Part B, PDF p. 7) |
| Risk | Liu 2025 names papillary urothelial neoplasm of low malignant potential among the two commonest bladder neoplasms in children, and states that most urothelial bladder tumours in children are that neoplasm or low-grade carcinoma, often confined to the mucosa (Liu 2025, PDF p. 8). Both sit on this number below behaviour 3. A clerk who matches the label registers either lesion as a Group XI cancer, on a number with no current malignant term |
| REDCap should | retire the row in place: `[RETIRED] 8130 - Papillary transitional cell carcinoma`. An invasive tumour is recorded on `8120` |

### 1.2 `8504` — the in situ term for the number whose behaviour-3 term is invasive

| | |
|---|---|
| Option string | `Intracystic carcinoma, NOS` (the XIc and XIf lists) |
| ICD-O-3.2 | `8504/2` Preferred *Encapsulated papillary carcinoma*; *Intracystic carcinoma, NOS* is a Synonym at `8504/2`. `8504/3` Preferred ***Encapsulated papillary carcinoma with invasion***; Synonyms *Encysted papillary carcinoma with invasion*, *Intracystic papillary carcinoma with invasion*. `8504/0` Preferred *Intracystic papillary adenoma*. ICD-O-3.2 moved *Intracystic carcinoma, NOS* from behaviour 3 to 2 (IARC, *3.1 to 3.2 — Terms that are changing behaviour*, p. 5) |
| What the tool does | `8504/3` is a picker entry; the breast part shows `8504/2` as an exclusion |
| Risk | The label names an in situ lesion. A clerk with a non-invasive encapsulated papillary carcinoma finds a Group XI row that matches the report and registers a lesion outside the registry's scope; a clerk with an invasive tumour records it under a label that says in situ |
| REDCap should offer | `8504 - Encapsulated papillary carcinoma with invasion` |

### 1.3 `8335` and `8339` — a correct label beside a missing code

| | |
|---|---|
| Option string | `Follicular carcinoma, minimally invasive` (the XIb list). It is the `8335/3` Preferred term: class A |
| ICD-O-3.2 | `8335/1` Preferred *Follicular tumor of uncertain malignant potential*; Synonym *Follicular carcinoma, encapsulated, NOS*. `8335/3` Preferred *Follicular carcinoma, minimally invasive*. `8339/3` Preferred ***Follicular carcinoma, encapsulated, angioinvasive***, a new code in ICD-O-3.2 (IARC, *New codes and their terms*, p. 1). IARC's *Terms that are changing behaviour* (p. 5) moves the ICD-O-3.1 term "Follicular carcinoma, encapsulated" from `8335/3` to `8335/1` |
| ICCC-2017 | `8335` is in range 121, XIb, at every site. No range holds `8339`; standing rule 3 places it in XIb, the group that offers it (contract D11) |
| What the tool does | The thyroid part asks the invasion (`th_ftc_invasion` in `XIb_thyroid.json`): capsular invasion only records `8335/3`; invasion of a blood vessel in an encapsulated tumour records `8339/3`; widely invasive, or invasive to an extent not described, records `8330/3` *Follicular carcinoma, NOS*; an encapsulated tumour with questionable invasion, or with no invasion described, is the `8335/1` exclusion |
| Risk | The dropdown has no `8339`. A clerk with an angioinvasive encapsulated follicular carcinoma finds no row; the nearest, `8335`, records a minimally invasive tumour. A report that says only "encapsulated follicular carcinoma" carries ICD-O-3.2's behaviour-1 synonym on the same number, and the row cannot show the behaviour |
| REDCap should | keep `8335` as it stands and append `8339 - Follicular carcinoma, encapsulated, angioinvasive` |

### 1.4 `8023` — NUT carcinoma has no row

| | |
|---|---|
| Option string | none |
| ICD-O-3.2 | `8023/3` Preferred ***Nuclear protein in testis (NUT)-associated carcinoma***; Synonyms *NUT carcinoma*, *NUT midline carcinoma*. A new code in ICD-O-3.2 (IARC, *New codes and their terms*, p. 1) |
| ICCC-2017 | in 8010–8041 of ranges 120 (XIb), 122 (XIc) and 124 (XIe), and in 8010–8077 of ranges 125 to 136 (XIf1 to XIf11) |
| What the tool does | `8023/3` is an option in the NUT, nasopharynx, head and neck, lung and thymus parts (contract D12) and a picker entry elsewhere |
| Risk | A carcinoma the sources report in children and adolescents (Lemelle 2022, PDF p. 6, a thoracic NUT carcinoma in a 13-year-old; Luo 2025, PDF p. 2, first considered an aggressive thymic carcinoma of children and adolescents) has nothing to select. The nearest rows are `8010` Carcinoma, NOS and `8070` Squamous cell carcinoma, NOS; either loses the entity |
| REDCap should | append `8023 - Nuclear protein in testis (NUT)-associated carcinoma`. `x_morph`, `vi_morph` and `vii_morph` owe the same append (`docs/TODO.md` §7) |

### 1.5 `8770` — the benign Spitz naevus term for the number that carries Spitz melanoma

| | |
|---|---|
| Option string | `Epithelioid and spindle cell nevus` (the XId list) |
| ICD-O-3.2 | `8770/0` Preferred *Epithelioid and spindle cell nevus*, the option string; Synonyms *Spitz nevus, NOS*, *Juvenile melanoma*, *Juvenile nevus*. `8770/3` Preferred ***Malignant Spitz tumor***; Synonyms *Spitz melanoma*, *Spitzoid melanoma*; Related *Mixed epithelioid and spindle cell melanoma* |
| What the tool does | `8770/3` is an option on the melanoma tree; `8770/0` is an exclusion there. The build contract's proof drives "Spitz melanoma → `8770/3` XId" (contract §9 item 6) |
| Risk | Sargen 2026 names Spitz melanoma among the melanoma subtypes that occur in children (PDF p. 1), and Ferrari 2021 calls spitzoid melanoma the most common histotype before age 10 (PDF p. 2). A Spitz melanoma is entered under a label naming the benign naevus, and a clerk with a Spitz naevus finds a Group XI row that matches the report. The subgroup formula names no subgroup for `8770` (§10) |
| REDCap should offer | `8770 - Malignant Spitz tumor` |

---

## 2. ★ Class H — 16 rows on numbers ICCC-2017 places in another group

ICCC-2017 range 57 places `8160`–`8162` and `8170`–`8180` in VIIb, hepatic carcinomas, at every site
(000–809). Range 37 places `8270`–`8281` and `8300` in IIIe1, pituitary adenomas and carcinomas, at every
site and at behaviours 0, 1 and 3. No Group XI range holds any of these numbers, and `group_11_dt.json`
has no entry on them. The digestive part refers a cholangiocarcinoma, and the endocrine/unspecified part a
hepatocellular carcinoma, to Group 7; the endocrine/unspecified and nasopharynx parts refer a pituitary
carcinoma to Group 3. `xi_morph` shows only when `[diag_main] = '11'`, so a record on one of these
rows files a Group VII or Group III tumour in Group XI.

| Number | Option string | Class | ICCC-2017 | The tool |
|---|---|---|---|---|
| `8160` | Cholangiocarcinoma | A | VIIb | no Group 11 entry; referred to Group 7 by the digestive part |
| `8161` | Bile duct cystadenocarcinoma | A | VIIb | no Group 11 entry |
| `8162` | Klatskin tumor | B2 | VIIb | no Group 11 entry; referred to Group 7 by the digestive part |
| `8170` | Hepatocellular carcinoma, NOS | A | VIIb | no Group 11 entry; referred to Group 7 by the endocrine/unspecified part |
| `8171` | Hepatocellular carcinoma, fibrolamellar | A | VIIb | no Group 11 entry |
| `8172` | Hepatocellular carcinoma, scirrhous | A | VIIb | no Group 11 entry |
| `8173` | Hepatocellular carcinoma, spindle cell variant | A | VIIb | no Group 11 entry |
| `8174` | Hepatocellular carcinoma, clear cell type | A | VIIb | no Group 11 entry |
| `8175` | Hepatocellular carcinoma, pleomorphic type | A | VIIb | no Group 11 entry |
| `8180` | Combined hepatocellular carcinoma and cholangiocarcinoma | A | VIIb | no Group 11 entry |
| `8270` | Chromophobe carcinoma | A | IIIe1 | no Group 11 entry |
| `8271` | Prolactinoma | E | IIIe1 | no Group 11 entry |
| `8272` | Pituitary carcinoma, NOS | A | IIIe1 | no Group 11 entry; referred to Group 3 by the endocrine/unspecified part; Group 3 by the nasopharynx part |
| `8280` | Acidophil carcinoma | O1 | IIIe1 | no Group 11 entry |
| `8281` | Mixed acidophil-basophil carcinoma | O1 | IIIe1 | no Group 11 entry |
| `8300` | Basophil carcinoma | O1 | IIIe1 | no Group 11 entry |

The owning dropdowns in the snapshot: `iii_morph` carries all six pituitary numbers. `vii_morph` carries
`8160`, `8161`, `8162`, `8170` and `8180` and lacks `8171`–`8175`, which the Group VII package appends
(`docs/TODO.md` §7, Group VII row). Until those appends land, `xi_morph` is the only dropdown that names
`8171` *Hepatocellular carcinoma, fibrolamellar*.

`8271` *Prolactinoma* is an ICD-O-3.2 Synonym of `8271/0` *Lactotroph adenoma*. Range 37 admits
behaviour 0, so a prolactinoma is a Group III registration, not a lesion outside the registry's scope.

**Repair.** Retire each row in place once the owning dropdown carries the number: now for the six
pituitary numbers and for `8160`, `8161`, `8162`, `8170` and `8180`; after the Group VII appends for
`8171`–`8175`. Count records first (§11).

---

## 3. ★ Class D — a below-behaviour-3 label on a number the tool emits at behaviour 3

Seven options. The label is an ICD-O-3.2 term at behaviour 0, 1 or 2; for `8983` it differs from the
`8983/0` Preferred term only in ", NOS", which the Group 10 package treated the same way for `8213`. The
tool emits the number at behaviour 3 under the term in the fourth column. §1.2 and §1.5 cover `8504` and
`8770`.

| Number | Option string | The string is | The tool emits at /3 | Also shown by the tool | Relabel to |
|---|---|---|---|---|---|
| `8504` | Intracystic carcinoma, NOS | `8504/2 Synonym` | *Encapsulated papillary carcinoma with invasion* (picker) | /2 exclusion (breast) | `8504 - Encapsulated papillary carcinoma with invasion` |
| `8507` | Intraductal micropapillary carcinoma | `8507/2 Preferred` | *Invasive micropapillary carcinoma of breast* (picker) | — | `8507 - Invasive micropapillary carcinoma of breast` |
| `8728` | Meningeal melanocytoma | `8728/1 Preferred` | *Meningeal melanomatosis* (option: melanoma) | /0 exclusion (melanoma); /1 exclusion (melanoma) | `8728 - Meningeal melanomatosis` |
| `8770` | Epithelioid and spindle cell nevus | `8770/0 Preferred` | *Malignant Spitz tumor* (option: melanoma) | /0 exclusion (melanoma) | `8770 - Malignant Spitz tumor` |
| `8100` | Trichoepithelioma | `8100/0 Preferred` | *Trichoblastic carcinoma* (picker) | /0 exclusion (skin) | `8100 - Trichoblastic carcinoma` |
| `8406` | Papillary syringadenoma | `8406/0 Synonym` | *Syringocystadenocarcinoma papilliferum* (picker) | /0 exclusion (salivary, skin) | `8406 - Syringocystadenocarcinoma papilliferum` |
| `8983` | Adenomyoepithelioma | `8983/0 Preferred` (the string differs from it only in ", NOS") | *Adenomyoepithelioma with carcinoma* (picker) | /0 exclusion (breast) | `8983 - Adenomyoepithelioma with carcinoma` |

`8728` is the other paediatric option in the class: the melanoma part offers meningeal melanomatosis
(`8728/3`, C70.9) as an option and shows meningeal melanocytoma (`8728/1`), the option string, as an
exclusion.

---

## 4. ★ Class O — obsolete

### 4.1 O1 (13) — every behaviour-3 term on the number is `[obs]`

Ten are among the eleven contract §0.2 names (`8124`, `8130`, `8141`, `8245`, `8251`, `8350`, `8440`,
`8450`, `8508`, `8512`). The eleventh, `8042` *Oat cell carcinoma*, is not in `xi_morph`. The other
three are the pituitary numbers `8280`, `8281` and `8300`, which are class H as well.

| Number | Option string | The string is | Preferred terms below /3 on the number | ICCC-2017 Group XI | The tool | Shown as exclusion |
|---|---|---|---|---|---|---|
| `8130` | Papillary transitional cell carcinoma | `8130/3 Synonym [obs]` | /1 *Papillary urothelial neoplasm of low malignant potential*; /2 *Papillary urothelial carcinoma, non-invasive* | XIb, XIc, XIf1–XIf11 | entry, off every screen (D3) | /1 exclusion (urinary); /2 exclusion (urinary) |
| `8141` | Scirrhous adenocarcinoma | `8141/3 Preferred [obs]` | — | XIb, XIc, XIf1–XIf11 | entry, off every screen (D3) | — |
| `8245` | Adenocarcinoid tumor | `8245/3 Preferred [obs]` | /1 *Tubular carcinoid* | XIb, XIc, XIf1–XIf11 | entry, off every screen (D3) | — |
| `8440` | Cystadenocarcinoma, NOS | `8440/3 Preferred [obs]` | /0 *Cystadenoma, NOS* | XIb, XIc, XIf1–XIf11 | entry, off every screen (D3) | /0 exclusion (urinary) |
| `8350` | Nonencapsulated sclerosing carcinoma | `8350/3 Preferred [obs]` | — | XIb | entry, off every screen (D3) | — |
| `8508` | Cystic hypersecretory carcinoma | `8508/3 Preferred [obs]` | — | XIc, XIf1–XIf11 | entry, off every screen (D3) | — |
| `8512` | Medullary carcinoma with lymphoid stroma | `8512/3 Preferred [obs]` | — | XIc, XIf1–XIf11 | entry, off every screen (D3) | — |
| `8124` | Cloacogenic carcinoma | `8124/3 Preferred [obs]` | — | XIf1–XIf11 | entry, off every screen (D3) | — |
| `8251` | Alveolar adenocarcinoma | `8251/3 Preferred [obs]` | /0 *Alveolar adenoma* | XIf1–XIf11 | entry, off every screen (D3) | /0 exclusion (lung) |
| `8280` | Acidophil carcinoma | `8280/3 Preferred [obs]` | /0 *Acidophil adenoma* `[obs]` | IIIe1 | no Group 11 entry | — |
| `8281` | Mixed acidophil-basophil carcinoma | `8281/3 Preferred [obs]` | /0 *Mixed acidophil-basophil adenoma* `[obs]` | IIIe1 | no Group 11 entry | — |
| `8300` | Basophil carcinoma | `8300/3 Preferred [obs]` | /0 *Basophil adenoma* `[obs]` | IIIe1 | no Group 11 entry | — |
| `8450` | Papillary cystadenocarcinoma, NOS | `8450/3 Preferred [obs]` | /0 *Papillary cystadenoma, NOS* | XIf1–XIf11 | entry, off every screen (D3) | — |

The tool keeps the ten Group XI numbers as entries, off every screen (contract D3; registrar's ruling
on Group 10 review A11, 8 October 2026), and has no entry on the three pituitary numbers. A report that
names one reaches the nearest current code. Where the WHO source names the current entity on the stem,
the tree offers that entity's code (contract D3): goblet cell adenocarcinoma records
`8243/3` *Goblet cell carcinoid*, not `8245/3`; the diffuse sclerosing subtype of papillary thyroid carcinoma records `8260/3`
*Papillary adenocarcinoma, NOS*, not `8350/3`; an invasive papillary urothelial carcinoma records `8120/3`
(§1.1).

**Repair, for the registrar.** Retire each row in place, `[RETIRED] NNNN - <label>`, after the count in
§11. No current malignant term lives on any of these numbers, so no new case belongs on one.

### 4.2 O2 (2) — the label is an `[obs]` Preferred term beside a current term

| Number | Option string | The string is | Current /3 terms on the number | ICCC-2017 Group XI | The tool |
|---|---|---|---|---|---|
| `8551` | Acinar cell cystadenocarcinoma | `8551/3 Preferred [obs]` | Related *Acinar adenocarcinoma of lung* | XIc, XIf1–XIf11 | entry, off every screen while D3 holds |
| `8780` | Blue nevus, malignant | `8780/3 Preferred [obs]` | Synonym *Melanoma arising in blue nevus* | XId | entry, off every screen while D3 holds |

Contract D3 holds both codes off every screen and puts them to the registrar. Before that decision the
lung, nasopharynx, breast and endocrine/unspecified parts proposed `8551/3` as a picker entry, most of them
labelled with the current related term, and the melanoma part proposed `8780/3` as an option under the
current synonym. If the registrar keeps a code, relabel the row to that current term:
`8551 - Acinar adenocarcinoma of lung`, `8780 - Melanoma arising in blue nevus`. If not, retire it in
place.

---

## 5. Class B and C — relabel

### 5.1 B1 (25) — a current behaviour-3 term that is not the Preferred term

| Number | Option string | The string is | The tool | Relabel to |
|---|---|---|---|---|
| `8033` | Sarcomatoid carcinoma | `8033/3 Synonym` | picker | `8033 - Pseudosarcomatous carcinoma` |
| `8122` | Transitional cell carcinoma, spindle cell | `8122/3 Synonym` | picker | `8122 - Urothelial carcinoma, sarcomatoid` |
| `8589` | Carcinoma showing thymus-like element | `8589/3 Synonym` | picker | `8589 - Intrathyroid thymic carcinoma` |
| `8330` | Follicular adenocarcinoma, NOS | `8330/3 Synonym` | option: thyroid | `8330 - Follicular carcinoma, NOS` |
| `8337` | Insular carcinoma | `8337/3 Synonym` | option: thyroid | `8337 - Poorly differentiated thyroid carcinoma` |
| `8342` | Papillary carcinoma, oxyphilic cell | `8342/3 Synonym` | option: thyroid | `8342 - Papillary carcinoma, oncocytic variant` |
| `8345` | Medullary carcinoma with amyloid stroma | `8345/3 Related` | option: thyroid | `8345 - Medullary thyroid carcinoma` |
| `8743` | Superficial spreading melanoma | `8743/3 Related` | option: melanoma | `8743 - Low cumulative sun damage melanoma` |
| `8744` | Acral lentiginous melanoma, malignant | `8744/3 Synonym` | picker | `8744 - Acral melanoma` |
| `8761` | Malignant melanoma in giant pigmented nevus | `8761/3 Synonym` | option: melanoma | `8761 - Malignant melanoma arising in giant congenital nevus` |
| `8091` | Multifocal superficial basal cell carcinoma | `8091/3 Synonym` | picker | `8091 - Superficial basal cell carcinoma` |
| `8110` | Pilomatrix carcinoma | `8110/3 Synonym` | picker | `8110 - Pilomatrical carcinoma` |
| `8240` | Carcinoid tumor, NOS | `8240/3 Synonym` | option: digestive, endocrine/unspecified, lung, thymus, urinary | `8240 - Neuroendocrine tumor, NOS` |
| `8390` | Skin appendage carcinoma | `8390/3 Synonym` | picker | `8390 - Adnexal adenocarcinoma, NOS` |
| `8402` | Nodular hidradenoma, malignant | `8402/3 Synonym` | picker | `8402 - Hidradenocarcinoma` |
| `8407` | Sclerosing sweat duct carcinoma | `8407/3 Synonym` | picker | `8407 - Microcystic adnexal carcinoma` |
| `8408` | Eccrine papillary adenocarcinoma | `8408/3 Synonym` | picker | `8408 - Digital papillary adenocarcinoma` |
| `8409` | Eccrine poroma, malignant | `8409/3 Synonym` | picker | `8409 - Porocarcinoma, NOS` |
| `8410` | Sebaceous adenocarcinoma | `8410/3 Synonym` | picker | `8410 - Sebaceous carcinoma` |
| `8131` | Transitional cell carcinoma, micropapillary | `8131/3 Synonym` | picker | `8131 - Urothelial carcinoma, micropapillary` |
| `8154` | Mixed pancreatic endocrine and exocrine tumor, malignant | `8154/3 Related` | picker | `8154 - Mixed neuroendocrine non-neuroendocrine neoplasm (MiNEN)` |
| `8249` | Atypical carcinoid tumor | `8249/3 Synonym` | option: digestive, lung | `8249 - Neuroendocrine tumor, grade 2` |
| `8441` | Serous cystadenocarcinoma, NOS | `8441/3 Synonym` | picker | `8441 - Serous carcinoma, NOS` |
| `8452` | Solid pseudopapillary carcinoma | `8452/3 Related` | option: digestive | `8452 - Solid pseudopapillary neoplasm of pancreas` |
| `8941` | Carcinoma in pleomorphic adenoma | `8941/3 Synonym` | option: eye | `8941 - Carcinoma ex pleomorphic adenoma` |

### 5.2 B2 (6) — a behaviour-3 term ICD-O-3.2 marks `[obs]`, on a number whose Preferred term is current

| Number | Option string | The string is | The tool | Relabel to |
|---|---|---|---|---|
| `8158` | Endocrine tumor, functioning, NOS | `8158/3 Related [obs]` | option: digestive, lung, thymus | `8158 - ACTH-producing tumor` |
| `8162` | Klatskin tumor | `8162/3 Synonym [obs]` | no Group 11 entry | `8162 - Perihilar cholangiocarcinoma` |
| `8250` | Bronchiolo-alveolar adenocarcinoma, NOS | `8250/3 Synonym [obs]` | picker | `8250 - Lepidic adenocarcinoma` |
| `8253` | Bronchiolo-alveolar carcinoma, mucinous | `8253/3 Synonym [obs]` | picker | `8253 - Adenocarcinoma of lung, mucinous` |
| `8254` | Bronchiolo-alveolar carcinoma, mixed mucinous and non-mucinous | `8254/3 Synonym [obs]` | picker | `8254 - Adenocarcinoma of lung, mixed mucinous and non-mucinous` |
| `8482` | Mucinous adenocarcinoma, endocervical type | `8482/3 Synonym [obs]` | picker | `8482 - Mucinous carcinoma, gastric type` |

`8162` is class H as well (§2). `vii_morph` already carries it, so the row is retired, not relabelled.

### 5.3 C (22) — no ICD-O-3.2 term at that number

| Sub | Number | Option string | ICD-O-3.2 Preferred terms on this number | The tool | Relabel to |
|---|---|---|---|---|---|
| C1 | `8745` | Desmoplastic melanoma, malignant | /3 *Desmoplastic melanoma, NOS* | picker | `8745 - Desmoplastic melanoma, NOS` |
| C1 | `8150` | Pancreatic endocrine tumor, malignant | /0 *Pancreatic neuroendocrine microadenoma*; /3 *Pancreatic neuroendocrine tumor, nonfunctioning* | option: digestive | `8150 - Pancreatic neuroendocrine tumor, nonfunctioning` |
| C1 | `8151` | Insulinoma, malignant | /3 *Insulinoma, NOS* | option: digestive | `8151 - Insulinoma, NOS` |
| C1 | `8152` | Glucagonoma, malignant | /3 *Glucagonoma* | option: digestive | `8152 - Glucagonoma` |
| C1 | `8153` | Gastrinoma, malignant | /3 *Gastrinoma* | option: digestive | `8153 - Gastrinoma` |
| C1 | `8155` | Vipoma, malignant | /3 *Vipoma* | option: digestive | `8155 - Vipoma` |
| C1 | `8156` | Somatostatinoma, malignant | /3 *Somatostatinoma* | option: digestive | `8156 - Somatostatinoma` |
| C1 | `8242` | Enterochromaffin-like cell tumor, malignant | /3 *Enterochromaffin-like cell tumor* | picker | `8242 - Enterochromaffin-like cell tumor` |
| C1 | `8580` | Thymoma, malignant, NOS | /0 *Microscopic thymoma*; /1 *Micronodular thymoma with lymphoid stroma*; /3 *Thymoma, NOS* | option: thymus | `8580 - Thymoma, NOS` |
| C1 | `8581` | Thymoma, type A, malignant | /3 *Thymoma, type A* | option: thymus | `8581 - Thymoma, type A` |
| C1 | `8582` | Thymoma, type AB, malignant | /3 *Thymoma, type AB* | option: thymus | `8582 - Thymoma, type AB` |
| C1 | `8583` | Thymoma, type B1, malignant | /3 *Thymoma, type B1* | option: thymus | `8583 - Thymoma, type B1` |
| C1 | `8584` | Thymoma, type B2, malignant | /3 *Thymoma, type B2* | option: thymus | `8584 - Thymoma, type B2` |
| C1 | `8585` | Thymoma, type B3, malignant | /3 *Thymoma, type B3* | option: thymus | `8585 - Thymoma, type B3` |
| C2 | `8343` | Papillary carcinoma, encapsulated | /3 *Papillary carcinoma, encapsulated, of thyroid* | option: thyroid | `8343 - Papillary carcinoma, encapsulated, of thyroid` |
| C2 | `8502` | Secretory carcinoma of breast | /3 *Secretory carcinoma* | option: breast, eye, salivary, thyroid | `8502 - Secretory carcinoma` |
| C2 | `8525` | Polymorphous low grade adenocarcinoma | /3 *Polymorphous adenocarcinoma* | option: salivary | `8525 - Polymorphous adenocarcinoma` |
| C2 | `8163` | Pancreatobiliary-type carcinoma | /0 *Pancreatobiliary neoplasm, non-invasive*; /2 *Papillary neoplasm, pancreatobiliary type, with high grade intraepithelial neoplasia*; /3 *Pancreatobiliary type carcinoma* | picker | `8163 - Pancreatobiliary type carcinoma` |
| C2 | `8384` | Adenocarcinoma, endocervical type | /3 *Adenocarcinoma, endocervical type, NOS* | picker | `8384 - Adenocarcinoma, endocervical type, NOS` |
| C2 | `8453` | Intraductal papillary-mucinous carcinoma, invasive | /0 *Intraductal papillary mucinous adenoma*; /2 *Intraductal papillary mucinous neoplasm with high grade dysplasia*; /3 *Intraductal papillary mucinous neoplasm with an associated invasive carcinoma* | picker | `8453 - Intraductal papillary mucinous neoplasm with an associated invasive carcinoma` |
| C3 | `8460` | Papillary serous cystadenocarcinoma | /2 *Serous borderline tumor, micropapillary variant*; /3 *Low grade serous carcinoma* | picker | `8460 - Low grade serous carcinoma` |
| C3 | `8461` | Serous surface papillary carcinoma | /0 *Serous surface papilloma*; /3 *High grade serous carcinoma* | picker | `8461 - High grade serous carcinoma` |

**C1 (14).** Each label carries "malignant", and the behaviour-3 Preferred term on the number does not.
Thirteen sit on numbers ICD-O-3.2 moved to behaviour 3 (IARC, *Terms that are changing behaviour*, pp.
1–4): `8150`, `8152`, `8153`, `8155`, `8156`, `8242` and `8580`–`8585` from behaviour 1, `8151` from
behaviour 0. On those numbers the qualifier no longer separates one behaviour from another. `8745` names
*Desmoplastic melanoma, NOS* with "malignant" in place of ", NOS". The relabels are wording; no code
changes.

**C2 (6).** `8163` and `8453` differ from an ICD-O-3.2 behaviour-3 term only by a hyphen (the `8163/3`
Preferred term; the `8453/3` Related term *Intraductal papillary mucinous carcinoma, invasive*). `8384`
lacks ", NOS". `8343` lacks ", of thyroid". `8502` adds "of breast" to *Secretory carcinoma*, the term the
tool also emits at the salivary gland, the eye and the thyroid. `8525` keeps "low grade", which the
ICD-O-3.2 Preferred term *Polymorphous adenocarcinoma* does not carry.

**C3 (2).** `Papillary serous cystadenocarcinoma` and `Serous surface papillary carcinoma` are both
ICD-O-3.2 Synonyms of `8441/3` *Serous carcinoma, NOS*. The rows on `8460` and `8461` therefore name a
different code's term. A clerk who matches either label to a report records `8460` *Low grade serous
carcinoma* or `8461` *High grade serous carcinoma* for a tumour ICD-O-3.2 codes `8441/3`.

---

## 6. Class E (50) — ICD-O-3.2 prints no behaviour-3 term on the number

ICCC-3 Group XI declares behaviour 3 for every range, and ICD-O-3.2 has no behaviour-3 term on these
numbers, so none of them can be a Group XI cancer. `8271` is the exception in kind: it is a Group III
registration (§2).

| Sub | Number | Option string | ICD-O-3.2 | Where the tool shows the number | ICCC-2017 |
|---|---|---|---|---|---|
| E1 | `8371` | Adrenal cortical adenoma, compact cell | `8371/0 Preferred` | /0 exclusion (adrenal) | XIa |
| E1 | `8372` | Adrenal cortical adenoma, pigmented | `8372/0 Preferred` | /0 exclusion (adrenal) | XIa |
| E1 | `8373` | Adrenal cortical adenoma, clear cell | `8373/0 Preferred` | /0 exclusion (adrenal) | XIa |
| E1 | `8374` | Adrenal cortical adenoma, glomerulosa cell | `8374/0 Preferred` | /0 exclusion (adrenal) | XIa |
| E1 | `8375` | Adrenal cortical adenoma, mixed cell | `8375/0 Preferred` | /0 exclusion (adrenal) | XIa |
| E1 | `8053` | Squamous cell papilloma, inverted | `8053/0 Preferred` | /0 exclusion (lung) | XIb, XIc, XIe, XIf1–XIf11 |
| E1 | `8060` | Squamous papillomatosis | `8060/0 Preferred` | /0 exclusion (digestive, head and neck) | XIb, XIc, XIe, XIf1–XIf11 |
| E1 | `8324` | Lipoadenoma | `8324/0 Preferred` | /0 exclusion (endocrine/unspecified) | XIb, XIf1–XIf11 |
| E1 | `8561` | Adenolymphoma | `8561/0 Preferred` | /0 exclusion (salivary) | XIb, XIc, XIf1–XIf11 |
| E1 | `8336` | Hyalinizing trabecular adenoma | `8336/1 Synonym` | /1 exclusion (thyroid) | XIb |
| E1 | `8505` | Intraductal papillomatosis, NOS | `8505/0 Preferred` | /0 exclusion (breast) | XIc, XIf1–XIf11 |
| E1 | `8506` | Adenoma of nipple | `8506/0 Preferred` | /0 exclusion (breast) | XIc, XIf1–XIf11 |
| E1 | `8726` | Magnocellular nevus | `8726/0 Preferred` | /0 exclusion (melanoma) | XId |
| E1 | `8727` | Dysplastic nevus | `8727/0 Preferred` | /0 exclusion (melanoma) | XId |
| E1 | `8081` | Bowen disease | `8081/2 Preferred` | /2 exclusion (skin) | XIe, XIf1–XIf11 |
| E1 | `8103` | Pilar tumor | `8103/0 Preferred` | /0 exclusion (skin); /1 exclusion (skin) | XIe |
| E1 | `8077` | Squamous intraepithelial neoplasia, high grade | `8077/2 Preferred` | /0 exclusion (digestive, eye, female genital, head and neck, lung); /2 exclusion (digestive, eye, female genital, head and neck, lung, nasopharynx, skin, urinary) | XIf1–XIf11 |
| E1 | `8080` | Queyrat erythroplasia | `8080/2 Preferred` | /2 exclusion (skin) | XIf1–XIf11 |
| E1 | `8148` | Glandular intraepithelial neoplasia, high grade | `8148/2 Preferred` | /0 exclusion (digestive); /2 exclusion (digestive, female genital, urinary) | XIf1–XIf11 |
| E1 | `8149` | Canalicular adenoma | `8149/0 Preferred` | /0 exclusion (salivary) | XIf1–XIf11 |
| E1 | `8204` | Lactating adenoma | `8204/0 Preferred` | /0 exclusion (breast) | XIf1–XIf11 |
| E1 | `8321` | Chief cell adenoma | `8321/0 Preferred` | /0 exclusion (endocrine/unspecified) | XIf1–XIf11 |
| E1 | `9010` | Fibroadenoma, NOS | `9010/0 Preferred` | /0 exclusion (breast, thymus) | XIf1–XIf11 |
| E1 | `9016` | Giant fibroadenoma | `9016/0 Preferred` | /0 exclusion (breast) | XIf1–XIf11 |
| E1 | `9030` | Juvenile fibroadenoma | `9030/0 Preferred` | /0 exclusion (breast) | XIf1–XIf11 |
| E2 | `8040` | Tumorlet, NOS | `8040/1 Preferred` | /0 exclusion (lung) | XIb, XIc, XIe, XIf1–XIf11 |
| E3 | `8334` | Macrofollicular adenoma | `8334/0 Preferred` | — | XIb |
| E3 | `8725` | Neuronevus | `8725/0 Preferred` | — | XId |
| E3 | `8750` | Intradermal nevus | `8750/0 Synonym` | — | XId |
| E3 | `8760` | Compound nevus | `8760/0 Preferred` | — | XId |
| E3 | `8790` | Cellular blue nevus | `8790/0 Preferred` | — | XId |
| E3 | `8096` | Intraepidermal epithelioma of Jadassohn | `8096/0 Preferred` | — | XIe |
| E3 | `8101` | Trichofolliculoma | `8101/0 Preferred` | — | XIe |
| E3 | `8391` | Follicular fibroma | `8391/0 Preferred` | — | XIe |
| E3 | `8392` | Syringofibroadenoma | `8392/0 Preferred` | — | XIe |
| E3 | `8404` | Hidrocystoma | `8404/0 Preferred` | — | XIe |
| E3 | `8405` | Papillary hidradenoma | `8405/0 Preferred` | — | XIe, XIf1–XIf11 |
| E3 | `8146` | Monomorphic adenoma | `8146/0 Preferred` | — | XIf1–XIf11 |
| E3 | `8191` | Embryonal adenoma | `8191/0 Preferred` | — | XIf1–XIf11 |
| E3 | `8202` | Microcystic adenoma | `8202/0 Preferred` | — | XIf1–XIf11 |
| E3 | `8212` | Flat adenoma | `8212/0 Preferred` | — | XIf1–XIf11 |
| E3 | `8248` | Apudoma | `8248/1 Preferred [obs]` | — | XIf1–XIf11 |
| E3 | `8264` | Papillomatosis, glandular | `8264/0 Preferred [obs]` | — | XIf1–XIf11 |
| E3 | `8271` | Prolactinoma | `8271/0 Synonym` | — | IIIe1 |
| E3 | `8360` | Multiple endocrine adenomas | `8360/1 Preferred [obs]` | — | XIf1–XIf11 |
| E3 | `8442` | Serous cystadenoma, borderline malignancy | `8442/1 Synonym` | — | XIf1–XIf11 |
| E3 | `8454` | Cystic tumor of atrio-ventricular node | `8454/0 Preferred` | — | XIf1–XIf11 |
| E3 | `9011` | Intracanalicular fibroadenoma | `9011/0 Preferred` | — | XIf1–XIf11 |
| E3 | `9012` | Pericanalicular fibroadenoma | `9012/0 Preferred` | — | XIf1–XIf11 |
| E3 | `9013` | Adenofibroma, NOS | `9013/0 Preferred` | — | XIf1–XIf11 |

E1 means the tool shows the option's own (code, behaviour) as an exclusion; E2 means it shows another
behaviour on the number (`8040/0` *Tumorlet, benign* in the lung part, where the option string is
`8040/1`); E3 means no part shows the number. Three option strings are `[obs]` in ICD-O-3.2 (`8248`,
`8264`, `8360`), and `8336` *Hyalinizing trabecular adenoma* is now the `8336/1` Synonym of *Hyalinizing
trabecular tumor*. Whether the dropdown keeps these 50 rows is the registrar's question that Group IX
(registrar questions G1) and Group X (§5 of its package) raised; the currency check (§5) puts it beside
Group II's mastocytoma question.

---

## 7. ★ Class G — 12 codes the tool emits that no option names

### 7.1 The twelve

The data carries no flag for them (standing rule 16, 4 October 2026): this table and `docs/TODO.md` §7
are the record. Append them at the end of the list.

| Code | ICD-O-3.2 Preferred term | ICCC-2017 Group XI | Entry's default subgroup | Reached from | Append |
|---|---|---|---|---|---|
| `8023/3` | Nuclear protein in testis (NUT)-associated carcinoma | XIb, XIc, XIe, XIf1–XIf11 | `XIf10` | option: NUT, head and neck, lung, nasopharynx, thymus | `8023 - Nuclear protein in testis (NUT)-associated carcinoma` |
| `8043/3` | Small cell carcinoma, fusiform cell | XIf1–XIf11 | `XIf10` | picker | `8043 - Small cell carcinoma, fusiform cell` |
| `8044/3` | Small cell carcinoma, intermediate cell | XIf1–XIf11 | `XIf10` | option: head and neck, lung | `8044 - Small cell carcinoma, intermediate cell` |
| `8045/3` | Combined small cell carcinoma | XIf1–XIf11 | `XIf10` | picker | `8045 - Combined small cell carcinoma` |
| `8046/3` | Non-small cell carcinoma | XIf1–XIf11 | `XIf10` | option: lung | `8046 - Non-small cell carcinoma` |
| `8054/3` | Warty carcinoma | XIb, XIc, XIe, XIf1–XIf11 | `XIf10` | option: female genital, urinary | `8054 - Warty carcinoma` |
| `8085/3` | Squamous cell carcinoma, HPV positive | XIf1–XIf11 | `XIf10` | option: female genital, nasopharynx, urinary | `8085 - Squamous cell carcinoma, HPV positive` |
| `8086/3` | Squamous cell carcinoma, HPV negative | XIf1–XIf11 | `XIf10` | option: female genital, nasopharynx, urinary | `8086 - Squamous cell carcinoma, HPV negative` |
| `8256/3` | Minimally invasive adenocarcinoma, non-mucinous | XIf1–XIf11 | `XIf10` | picker | `8256 - Minimally invasive adenocarcinoma, non-mucinous` |
| `8257/3` | Minimally invasive adenocarcinoma, mucinous | XIf1–XIf11 | `XIf10` | picker | `8257 - Minimally invasive adenocarcinoma, mucinous` |
| `8339/3` | Follicular carcinoma, encapsulated, angioinvasive | none (standing rule 3: XIb) | `XIb` | option: thyroid | `8339 - Follicular carcinoma, encapsulated, angioinvasive` |
| `8509/3` | Solid papillary carcinoma with invasion | XIc, XIf1–XIf11 | `XIf10` | picker | `8509 - Solid papillary carcinoma with invasion` |

Eight are new in ICD-O-3.2 (IARC, *New codes and their terms*, pp. 1–2): `8023`, `8054`, `8085`, `8086`,
`8256`, `8257`, `8339`, `8509`. Four predate ICD-O-3.2 and sit in the gap the option list leaves between
`8041` and `8050`: `8043`, `8044`, `8045`, `8046`.

Three subgroup facts the dropdown's subgroup formula has to follow (the entry's `iccc3_subgroup_by_topography`
already does):

- `8085` and `8086` are in ranges 125 to 136 only. Range 122 (XIc) lists `8082` and `8083` from that
  stretch, not `8085` or `8086`, so at the nasopharynx ICCC-2017 gives no Group XI subgroup and the entry
  shows its default, XIf10 (contract D11).
- `8509` is in range 122 (XIc) and ranges 125 to 136. Range 124 (XIe) does not hold it, and no Group XI
  range covers it at the skin, where ICD-O-3.2 prints its Related term *Endocrine mucin-producing sweat
  gland carcinoma*; there the entry shows XIf10.
- `8054` lies in 8050–8075 of ranges 120, 122 and 124, so at C51.9 vulva and C60.9 penis it is XIe, not
  XIf10.

### 7.2 Two new codes Group XI does not owe

| Code | ICD-O-3.2 Preferred term | ICCC-2017 | What the tool does | Owed by |
|---|---|---|---|---|
| `8474/3` | Seromucinous carcinoma | range 114, Xd, at every site | no Group 11 entry; the endocrine/unspecified part refers it to Group 10 | `x_morph` (`docs/group_10_layer1_repair.md` §6) |
| `8273/3` | Pituitary blastoma | range 37, IIIe1, at every site | no Group 11 entry; the endocrine/unspecified part refers it to Group 3 | `iii_morph` pick 109, which the snapshot labels `8273 - Oncocytoma, NOS`; the Group 3 package already relabels it to `8273 - Pituitary blastoma` |

### 7.3 The three codes the option file drops

The option file's XIf paragraph (line 325) excludes `8085`, `8086` and `8157` because their labels were
"not found in Cancer Morphology.pdf". `8085` and `8086` are in §7.1. ICD-O-3.2 holds no `8157`, although
ICCC-2017's XIf ranges (8120–8158; 8120–8157 in range 134) still span the number; nothing is owed for it.

---

## 8. Topography — two sites the dropdown lacks

`ICD coding/RedCap Options/Topography Redcap.md` and `topo_code` in the 1 October 2026 snapshot (327
choices) offer 440 to 443 and 445 to 449, and 480, 482 and 488. Two Group XI sites have no choice:

| Code | Site | Group XI range | Append |
|---|---|---|---|
| C44.4 | skin of scalp and neck | range 124 (XIe, 440–449); range 123 (XId, every site) | `444, Skin of scalp and neck` |
| C48.1 | specified parts of peritoneum | range 134 (XIf10, 480–488) | `481, Specified parts of peritoneum` |

A basal cell carcinoma or a melanoma of the scalp or neck, and a carcinoma of a specified part of the
peritoneum, cannot be recorded at its own site. The lookup's
`topography_codes.json` does not carry either code, because the REDCap list has none (contract §3.1). `444`
is already owed for Group IX (`docs/TODO.md` §7; Group 9 registrar questions H2).

---

## 9. Layer 1 Markdown repairs

These are vault files. Repair them in the vault, not from this repository.

### 9.1 `ICD coding/ICCC 2017 Cancer Classification.md` — four malformed Group XI rows

A replacement of "809" by "C80.9" has run through the code column. The build reads that column
(`parse_classification`, `parse_classification_subgroups` in `build/build_database.py`), skips each
malformed token, and so loses `8090`–`8098` from XIe and `8098` from XIf1, XIf2 and XIf11. `8090`–`8097`
appear in no other Group XI row, so the build warns that they are out of range (contract §8, a T1
finding), although `ICCC-2017.sqlite` range 124 places them in XIe.

Line 180, the code cell of `XIe Skin carcinomas`:

```
8010-8041,8050-8075,8078,8081,8082,C80.90-C80.98,8100-8110,8140,8143,8147,8190,8200,8211,8240,8246,8247,8260,8263,8310,8320,8323,8390-8420,8430,8480,8540,8542,8560,8570-8573
```

`C80.90-C80.98` should read `8090-8098` (range 124). The same row's site cell reads
`C44.0-C44.9,519,609,632`; range 124 gives `440-449,519,609,632`, which is C44.0–C44.9, C51.9, C60.9 and
C63.2, so the cell should read `C44.0-C44.9,C51.9,C60.9,C63.2`.

Lines 182, 183 and 193, the code cells of `XIf1 Carcinomas of salivary glands`, `XIf2 Carcinomas of colon
and rectum` and `XIf11 Carcinomas of unspecified site`, each begin:

```
8010-8077,8080-8086,C80.98,8120-8158,8163,8190-8265,...
```

`C80.98` should read `8098` (ranges 125, 126 and 136), as it does on the XIf3 to XIf10 rows.

Line 18, `Ie Unspecified and other specified leukemias`, carries the same fault outside Group XI:
`9805-9C80.9` should read `9805-9809` (range 11). The build's note already names it. It is listed here so
one pass repairs all five lines.

### 9.2 The option file — two labels the dropdown does not carry

The consolidated XIf list prints `8010, 8010 - Epithelial Tumor, NOS` (line 342) and
`8011, 8011 - Epithelioma` (line 343). The XIb, XIc and XIe lists, the unique-codes file and the
snapshot carry `Carcinoma, NOS` and `Epithelioma, malignant`, both class A. `Epithelial Tumor, NOS` is not an
ICD-O-3.2 term (`8010/0` is *Epithelial tumor, benign*; `8010/3` has the Synonym *Epithelial tumor,
malignant*), and `Epithelioma` differs from the `8011/3` Synonym *Epithelioma, NOS* only in ", NOS".
Correct the two lines to the dropdown's labels so the option file matches the live list.

---

## 10. The subgroup formula — a pointer for the REDCap Registry repository

`xi_subgroup` in the 1 October 2026 snapshot is an `@CALCTEXT` that names XIa to XIe from `xi_morph`
and `topo_code`; `xi_extended` computes the extended subtype. Read by `g11_layer1_calc.py`, ignoring
topography, the XIa to XIe clauses of `xi_subgroup` do not name these current behaviour-3 codes that
ICCC-2017 places in the subgroup:

| Subgroup | Not named |
|---|---|
| XIb | `8023`, `8054`, `8131` *Urothelial carcinoma, micropapillary*; and `8339` (standing rule 3) |
| XIc | `8023`, `8054`, `8131`, `8290` *Oxyphilic adenocarcinoma*, `8310` *Clear cell adenocarcinoma, NOS*, `8320` *Granular cell carcinoma*, `8323` *Mixed cell adenocarcinoma*, `8514` *Duct carcinoma, desmoplastic type* |
| XId | `8770` *Malignant Spitz tumor* |
| XIe | `8023`, `8054`, `8100` *Trichoblastic carcinoma*, `8102` *Trichilemmocarcinoma* |

Each code appended in §7 needs both formulas to name it. `xi_extended` was not parsed here. The
formulas belong to the REDCap Registry repository, which audits them; the lookup tool tests none of this
(standing rule 16).

---

## 11. Pre-flight, and the repair proposed

**Before anything changes**, export `record_id`, `xi_morph`, `topo_code` and `xi_subgroup` read-only, with
the registrar's approval, and count records on: the 13 class O1 numbers and the two class O2 numbers,
`8551` and `8780` (§4); the seven
class D numbers (§3); `8460` and `8461` (§5.3); `8335`, where an angioinvasive tumour belongs on `8339`
(§1.3); the 16 class H numbers (§2); and the 50 class E numbers (§6). A record on `8130` is an invasive
papillary urothelial carcinoma, a non-invasive one or a low-malignant-potential neoplasm, and the
dictionary cannot say which; read the report. The registry began operating in 2025. Count first: the repair
is cheapest before records accumulate on a wrong label.

The three safe operations are unchanged (`docs/TODO.md` §7): relabel in place, retire in place (prefix
`[RETIRED]`), append at the end.

1. Retire `8130`; relabel `8504` and `8770`; append `8339` and `8023` (§1).
2. Append the other ten codes in §7.1.
3. Relabel the other class D rows (§3).
4. Retire the class H rows once the owning dropdown carries each number (§2).
5. Retire the other class O1 rows; decide `8551` and `8780` with the registrar (§4).
6. Relabel the class B and C rows (§5).
7. Append `topo_code` 444 and 481 (§8).
8. Decide, with the registrar, the 50 class E rows (§6).
9. Repair the two Layer 1 Markdown files in the vault (§9).

---

## 12. What the lookup tool already does

- Names every code by ICD-O-3.2's Preferred term at its behaviour, never by the REDCap label (contract
  §2 item 2).
- Carries no REDCap field (contract §2 item 7; standing rule 16). The drifted labels and the twelve codes
  with no option are recorded here and in `docs/TODO.md` §7 only. Nothing in the tool tests REDCap.
- Keeps every code whose behaviour-3 terms are all `[obs]` off every screen (contract D3). Its referral
  branches send a hepatocellular carcinoma, a cholangiocarcinoma and a pituitary carcinoma to Groups VII and
  III (§2).

---

## 13. Where this package differs from the code currency check

`ICD Look Up tool/Group 11 — ICD-O-3.2 Code Currency Check 2026-10-08.md` §§2, 4, 5 and 6 are carried
above, each recomputed from the databases. The code sets agree: its 13 (§2) are class O1, its 62 (§4) are
classes B, C, D and O2, and its 50 (§5) are class E. The differences:

1. **§6 lists `8474/3` under XIf10.** ICCC-2017 range 114 places `8474` in Xd at every site, and no Group
   XI range holds it. The Group 11 data has no entry on it and refers it to Group 10. `x_morph` owes it
   (§7.2); `xi_morph` does not.
2. **§6 omits four codes.** `8043`, `8044`, `8045` and `8046` are current at behaviour 3, ICCC-2017 places
   them in XIf1 to XIf11, and `xi_morph` lacks them. They predate ICD-O-3.2, so a list of new codes does not
   catch them. `xi_morph` lacks twelve codes the tool emits, not nine.
3. **§6 subgroups.** It places `8085` and `8086` in XIc; ICCC-2017 places them in XIf1 to XIf11 only. It
   places `8509` in XIf6 and XIe; ICCC-2017 places it in XIc and XIf1 to XIf11, not XIe. It places `8054` in
   XIf7 and XIf10 for the cervix, vulva and penis; ICCC-2017 also places it in XIb, XIc and XIe, and at C51.9
   and C60.9 the subgroup is XIe (§7.1).
4. **§4, `8551` and `8780`.** It names *Acinar adenocarcinoma of lung* and *Melanoma arising in blue nevus*
   as the Preferred terms at behaviour 3. In `icdo32.sqlite` the Preferred terms are the REDCap labels
   themselves, *Acinar cell cystadenocarcinoma* and *Blue nevus, malignant*, both `[obs]`; the terms it
   names are a Related term and a Synonym (class O2, §4.2).
5. **§4, `8460` and `8461`.** It calls both labels "term not in ICD-O-3.2". Both are ICD-O-3.2 Synonyms of
   `8441/3` *Serous carcinoma, NOS* (class C3, §5.3).
6. **§4, `8983`.** It calls `Adenomyoepithelioma` "term not in ICD-O-3.2". The string differs from the
   `8983/0` Preferred term *Adenomyoepithelioma, NOS* only in ", NOS", so it reads as the benign tumour
   (class D, §3).
7. **§4, `8163` and `8453`.** It calls both "term not in ICD-O-3.2". Each differs from an ICD-O-3.2
   behaviour-3 term only by a hyphen (class C2).
8. **§4, `8507`.** It calls the label a synonym listed at behaviour 2. It is the `8507/2` Preferred term.
9. **§2, `8130`.** It names *Urothelial carcinoma, NOS* as the current `8120/3` term. That is a Synonym; the
   Preferred term is *Transitional cell carcinoma, NOS*.
10. **§2, `8280`, `8281` and `8300`.** It says the pituitary site C75.1 routes them to Group III. ICCC-2017
    range 37 places them in IIIe1 at every site. With `8160`–`8180` (range 57, VIIb, every site) they are 16
    `xi_morph` rows on numbers ICCC-2017 places in another group, which the check does not list (§2). §6
assigns `8273` *Pituitary blastoma* to Group III "by site"; range 37 holds it at every site too.
11. **§3, `8335`.** It says "REDCap offers 8335". REDCap's label is *Follicular carcinoma, minimally
    invasive*, the current `8335/3` Preferred term, so the row is correct; the defect is the missing `8339`
    (§1.3).
12. **§5, `8271`.** It lists *Prolactinoma* among options with no malignant form. ICCC-2017 range 37 admits
    behaviour 0 in IIIe1, so `8271/0` is a Group III registration (§2).

---

## 14. Class A (157) — correct as labels

The label is the ICD-O-3.2 Preferred term at behaviour 3, which is current. Eleven sit on numbers
ICCC-2017 places in another group (§2).

| Number | Option string | The tool |
|---|---|---|
| `8370` | Adrenal cortical carcinoma | option: adrenal |
| `8010` | Carcinoma, NOS | option: adrenal, breast, digestive, endocrine/unspecified, eye, female genital, head and neck, lung, nasopharynx, salivary, skin, thymus, thyroid, urinary |
| `8011` | Epithelioma, malignant | picker |
| `8012` | Large cell carcinoma, NOS | option: lung |
| `8013` | Large cell neuroendocrine carcinoma | option: lung |
| `8014` | Large cell carcinoma with rhabdoid phenotype | picker |
| `8015` | Glassy cell carcinoma | picker |
| `8020` | Carcinoma, undifferentiated, NOS | option: head and neck, nasopharynx |
| `8021` | Carcinoma, anaplastic, NOS | option: breast |
| `8022` | Pleomorphic carcinoma | picker |
| `8030` | Giant cell and spindle cell carcinoma | picker |
| `8031` | Giant cell carcinoma | picker |
| `8032` | Spindle cell carcinoma, NOS | picker |
| `8034` | Polygonal cell carcinoma | picker |
| `8035` | Carcinoma with osteoclast-like giant cells | picker |
| `8041` | Small cell carcinoma, NOS | option: lung |
| `8050` | Papillary carcinoma, NOS | picker |
| `8051` | Verrucous carcinoma, NOS | option: female genital, head and neck, urinary |
| `8052` | Papillary squamous cell carcinoma | option: female genital, head and neck, urinary |
| `8070` | Squamous cell carcinoma, NOS | option: eye, female genital, head and neck, lung, nasopharynx, skin, urinary |
| `8071` | Squamous cell carcinoma, keratinizing, NOS | option: female genital, head and neck, nasopharynx, skin |
| `8072` | Squamous cell carcinoma, large cell, nonkeratinizing, NOS | option: female genital, head and neck, nasopharynx |
| `8073` | Squamous cell carcinoma, small cell, nonkeratinizing | picker |
| `8074` | Squamous cell carcinoma, spindle cell | option: head and neck, urinary |
| `8075` | Squamous cell carcinoma, adenoid | option: head and neck |
| `8082` | Lymphoepithelial carcinoma | option: head and neck, urinary |
| `8120` | Transitional cell carcinoma, NOS | option: urinary |
| `8121` | Schneiderian carcinoma | picker |
| `8140` | Adenocarcinoma, NOS | option: digestive, endocrine/unspecified, eye, female genital, head and neck, lung, salivary, thymus, urinary |
| `8190` | Trabecular adenocarcinoma | picker |
| `8200` | Adenoid cystic carcinoma | option: eye, salivary |
| `8201` | Cribriform carcinoma, NOS | option: thyroid |
| `8211` | Tubular adenocarcinoma | option: digestive |
| `8230` | Solid carcinoma, NOS | picker |
| `8231` | Carcinoma simplex | picker |
| `8244` | Mixed adenoneuroendocrine carcinoma | picker |
| `8246` | Neuroendocrine carcinoma, NOS | option: digestive, head and neck, nasopharynx |
| `8260` | Papillary adenocarcinoma, NOS | option: thyroid |
| `8261` | Adenocarcinoma in villous adenoma | picker |
| `8262` | Villous adenocarcinoma | picker |
| `8263` | Adenocarcinoma in tubulovillous adenoma | picker |
| `8290` | Oxyphilic adenocarcinoma | option: thyroid |
| `8310` | Clear cell adenocarcinoma, NOS | option: female genital |
| `8320` | Granular cell carcinoma | picker |
| `8323` | Mixed cell adenocarcinoma | picker |
| `8333` | Fetal adenocarcinoma | picker |
| `8430` | Mucoepidermoid carcinoma | option: eye, head and neck, lung, nasopharynx, salivary |
| `8480` | Mucinous adenocarcinoma | option: digestive |
| `8481` | Mucin-producing adenocarcinoma | picker |
| `8510` | Medullary carcinoma, NOS | option: breast |
| `8560` | Adenosquamous carcinoma | option: head and neck |
| `8562` | Epithelial-myoepithelial carcinoma | option: eye |
| `8570` | Adenocarcinoma with squamous metaplasia | picker |
| `8571` | Adenocarcinoma with cartilaginous and osseous metaplasia | picker |
| `8572` | Adenocarcinoma with spindle cell metaplasia | picker |
| `8573` | Adenocarcinoma with apocrine metaplasia | picker |
| `8331` | Follicular adenocarcinoma, well differentiated | picker |
| `8332` | Follicular adenocarcinoma, trabecular | picker |
| `8335` | Follicular carcinoma, minimally invasive | option: thyroid |
| `8340` | Papillary carcinoma, follicular variant | option: thyroid |
| `8341` | Papillary microcarcinoma | option: thyroid |
| `8344` | Papillary carcinoma, columnar cell | option: thyroid |
| `8346` | Mixed medullary-follicular carcinoma | picker |
| `8347` | Mixed medullary-papillary carcinoma | picker |
| `8588` | Spindle epithelial tumor with thymus-like element | option: thyroid |
| `8083` | Basaloid squamous cell carcinoma | option: female genital, head and neck, nasopharynx, urinary |
| `8500` | Infiltrating duct carcinoma, NOS | option: breast, eye, salivary |
| `8501` | Comedocarcinoma, NOS | picker |
| `8503` | Intraductal papillary adenocarcinoma with invasion | picker |
| `8513` | Atypical medullary carcinoma | picker |
| `8514` | Duct carcinoma, desmoplastic type | picker |
| `8520` | Lobular carcinoma, NOS | option: breast |
| `8521` | Infiltrating ductular carcinoma | picker |
| `8522` | Infiltrating duct and lobular carcinoma | picker |
| `8523` | Infiltrating duct mixed with other types of carcinoma | picker |
| `8524` | Infiltrating lobular mixed with other types of carcinoma | picker |
| `8530` | Inflammatory carcinoma | option: breast |
| `8540` | Paget disease, mammary | picker |
| `8541` | Paget disease and infiltrating duct carcinoma of breast | picker |
| `8542` | Paget disease, extramammary | picker |
| `8543` | Paget disease and intraductal carcinoma of breast | picker |
| `8550` | Acinar cell carcinoma | option: digestive, eye, head and neck, nasopharynx, salivary |
| `8574` | Adenocarcinoma with neuroendocrine differentiation | picker |
| `8575` | Metaplastic carcinoma, NOS | picker |
| `8576` | Hepatoid adenocarcinoma | picker |
| `8720` | Malignant melanoma, NOS | option: female genital, head and neck, lung, melanoma, nasopharynx |
| `8721` | Nodular melanoma | picker |
| `8722` | Balloon cell melanoma | picker |
| `8723` | Malignant melanoma, regressing | picker |
| `8730` | Amelanotic melanoma | picker |
| `8740` | Malignant melanoma in junctional nevus | picker |
| `8741` | Malignant melanoma in precancerous melanosis | picker |
| `8742` | Lentigo maligna melanoma | picker |
| `8746` | Mucosal lentiginous melanoma | picker |
| `8771` | Epithelioid cell melanoma | picker |
| `8772` | Spindle cell melanoma, NOS | picker |
| `8773` | Spindle cell melanoma, type A | picker |
| `8774` | Spindle cell melanoma, type B | picker |
| `8078` | Squamous cell carcinoma with horn formation | picker |
| `8090` | Basal cell carcinoma, NOS | option: skin |
| `8092` | Infiltrating basal cell carcinoma, NOS | picker |
| `8093` | Basal cell carcinoma, fibroepithelial | picker |
| `8094` | Basosquamous carcinoma | picker |
| `8095` | Metatypical carcinoma | picker |
| `8097` | Basal cell carcinoma, nodular | picker |
| `8098` | Adenoid basal carcinoma | picker |
| `8102` | Trichilemmocarcinoma | picker |
| `8143` | Superficial spreading adenocarcinoma | picker |
| `8147` | Basal cell adenocarcinoma | picker |
| `8247` | Merkel cell carcinoma | option: skin |
| `8400` | Sweat gland adenocarcinoma | picker |
| `8401` | Apocrine adenocarcinoma | picker |
| `8403` | Malignant eccrine spiradenoma | picker |
| `8413` | Eccrine adenocarcinoma | picker |
| `8420` | Ceruminous adenocarcinoma | picker |
| `8076` | Squamous cell carcinoma, microinvasive | option: female genital |
| `8084` | Squamous cell carcinoma, clear cell type | option: urinary |
| `8123` | Basaloid carcinoma | picker |
| `8142` | Linitis plastica | picker |
| `8144` | Adenocarcinoma, intestinal type | option: thymus |
| `8145` | Carcinoma, diffuse type | picker |
| `8160` | Cholangiocarcinoma | no Group 11 entry (ICCC-2017 VIIb; §2) |
| `8161` | Bile duct cystadenocarcinoma | no Group 11 entry (ICCC-2017 VIIb; §2) |
| `8170` | Hepatocellular carcinoma, NOS | no Group 11 entry (ICCC-2017 VIIb; §2) |
| `8171` | Hepatocellular carcinoma, fibrolamellar | no Group 11 entry (ICCC-2017 VIIb; §2) |
| `8172` | Hepatocellular carcinoma, scirrhous | no Group 11 entry (ICCC-2017 VIIb; §2) |
| `8173` | Hepatocellular carcinoma, spindle cell variant | no Group 11 entry (ICCC-2017 VIIb; §2) |
| `8174` | Hepatocellular carcinoma, clear cell type | no Group 11 entry (ICCC-2017 VIIb; §2) |
| `8175` | Hepatocellular carcinoma, pleomorphic type | no Group 11 entry (ICCC-2017 VIIb; §2) |
| `8180` | Combined hepatocellular carcinoma and cholangiocarcinoma | no Group 11 entry (ICCC-2017 VIIb; §2) |
| `8210` | Adenocarcinoma in adenomatous polyp | picker |
| `8213` | Serrated adenocarcinoma | picker |
| `8214` | Parietal cell carcinoma | picker |
| `8215` | Adenocarcinoma of anal glands | picker |
| `8220` | Adenocarcinoma in adenomatous polyposis coli | option: digestive |
| `8221` | Adenocarcinoma in multiple adenomatous polyps | picker |
| `8241` | Enterochromaffin cell carcinoid | option: digestive, endocrine/unspecified, lung |
| `8243` | Goblet cell carcinoid | picker |
| `8252` | Bronchiolo-alveolar carcinoma, non-mucinous | picker |
| `8255` | Adenocarcinoma with mixed subtypes | picker |
| `8265` | Micropapillary carcinoma, NOS | picker |
| `8270` | Chromophobe carcinoma | no Group 11 entry (ICCC-2017 IIIe1; §2) |
| `8272` | Pituitary carcinoma, NOS | no Group 11 entry (ICCC-2017 IIIe1; §2) |
| `8314` | Lipid-rich carcinoma | picker |
| `8315` | Glycogen-rich carcinoma | picker |
| `8322` | Water-clear cell adenocarcinoma | picker |
| `8380` | Endometrioid adenocarcinoma, NOS | picker |
| `8381` | Endometrioid adenofibroma, malignant | picker |
| `8382` | Endometrioid adenocarcinoma, secretory variant | picker |
| `8383` | Endometrioid adenocarcinoma, ciliated cell variant | picker |
| `8470` | Mucinous cystadenocarcinoma, NOS | picker |
| `8490` | Signet ring cell carcinoma | option: digestive |
| `8552` | Mixed acinar-ductal carcinoma | picker |
| `8586` | Thymic carcinoma, NOS | picker |
| `9000` | Brenner tumor, malignant | picker |
| `9014` | Serous adenocarcinofibroma | picker |
| `9020` | Phyllodes tumor, malignant | option: breast |
