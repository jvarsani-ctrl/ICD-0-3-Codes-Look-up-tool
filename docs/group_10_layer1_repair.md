# Group 10 — Layer 1 Repair Package (REDCap `x_morph`)

**Written 4 October 2026 with the Group 10 build.** Input for the REDCap Registry repository,
which owns every change to the registry's dictionary (routing table in `../../CLAUDE.md`).
Nothing here edits REDCap. Live REDCap is production and is written only on the registrar's
approval of a specific change.

**The lookup tool does not act on this list.** Standing rule 16 (registrar, 4 October 2026): the
tool does not connect to REDCap, and no check, flag or fix in it tests what REDCap holds. The
clerk reads the answer and picks the option by hand. This package exists so the REDCap side can
repair the dropdown; the tool needs none of it.

**Source.** `ICD coding/RedCap Options/Group 10- Germ Cell Tumors, Trophoblastic Tumors And
Neoplasms Of Gonads.md`: 195 option lines, **158 distinct options** (an option repeats under each
subgroup that offers it; no number carries two labels). 157 of the 158 are character-identical to
`x_morph` in `REDCap Registry/snapshots/2026-10-01/data_dictionary.csv`, which has 157 choices.
The one difference is `9086`: the option file lists it and that snapshot's `x_morph` has no
`9086` choice (§1.3). Every option string was compared with `icdo32.sqlite` and with
`data/database/group_10_dt.json` by script (`136` entries, `131` of them at behaviour 3); the tables
below are that script's output, not a transcription.

**What a change costs.** In the snapshot the choice code of every `x_morph` option is the
four-digit number itself, so the dropdown holds one row per number. Relabelling a row changes no
stored value, and `x_extended` and `x_subgroup` compute from the number and `topo_code`. The option
file prints no behaviour digit, and the diagnosis form in that snapshot has no field labelled for
behaviour (Diagnostic Pathway §8 item 9). A row's label should therefore name the number's
behaviour-3 term, which is what the lookup tool shows.

| Class | Options | What |
|---|---|---|
| A | 58 | the ICD-O-3.2 preferred term at behaviour 3 — correct as it stands |
| B | 4 | a real behaviour-3 term, not the preferred one — usable, relabel when convenient |
| C | 12 | drift: no exact ICD-O-3.2 term. 7 sit on a number the tool emits at behaviour 3 (C1); 5 sit on a number ICD-O-3.2 deleted (C2) |
| ★ D | 54 | a benign, borderline or in situ term on a number the tool emits at behaviour 3 |
| E | 28 | a term that exists only below behaviour 3, on a number with no behaviour-3 term for the tool to emit. 13 are behaviour exclusions the tool shows (E1); 15 it does not show (E2) |
| ★ F | 2 | "Label not found" in place of a term: `8474` and `9086` |
| ★ G | 6 missing | codes the tool emits that no option names |

A to F add up to the 158 distinct options; class A is listed in §11 so the count can be audited. The
three that most misstate the evidence are §1: `9064`, `9100` and `9086`.

---

## 1. ★ The three that most misstate the evidence

### 1.1 `9064` — the in situ term for the number whose behaviour-3 term is Germinoma

| | |
|---|---|
| Option string | `Intratubular malignant germ cells` (subgroups Xa1, Xb1, Xc1) |
| ICD-O-3.2 | `9064/2` Preferred, *Intratubular malignant germ cells*; *Germ cell neoplasia in situ* is a Synonym. `9064/3` Preferred, ***Germinoma***; *Germ cell tumor, NOS* is a Synonym |
| What the tool emits | `9064/3` Germinoma from 27 branches in 4 trees (`g10_cns`, `g10_extragonadal`, `g10_ovary`, `g10_testis`). `9064/2` appears once, as a behaviour exclusion in `ts_histology` (germ cell neoplasia in situ with no invasive tumour; design D9) |
| Risk | The commonest germ cell code the tool emits sits behind a label that names the in situ lesion, which is not registered. A clerk who matches the label records germ cell neoplasia in situ for a germinoma, or for a germ cell tumour of unnamed type (design D2) |
| REDCap should offer | `9064 - Germinoma` |

`9064/2` is not lost by the relabel. ICCC-2017 Group X counts behaviour 3 outside the central
nervous system, so the in situ lesion is not a Group X registration at any site.

### 1.2 `9100` — the benign term for the number that carries choriocarcinoma

| | |
|---|---|
| Option string | `Hydatidiform mole, NOS` (subgroups Xa5, Xb5, Xc5) |
| ICD-O-3.2 | `9100/0` Preferred, *Hydatidiform mole, NOS*. `9100/1` Preferred, *Invasive hydatidiform mole*. `9100/3` Preferred, ***Choriocarcinoma, NOS*** |
| What the tool emits | `9100/3` Choriocarcinoma, NOS from 5 branches in 4 trees (`g10_cns`, `g10_extragonadal`, `g10_ovary`, `g10_testis`). Outside the central nervous system the complete mole (`9100/0`) and the invasive mole (`9100/1`) are behaviour exclusions in `eg_histology`. Inside it they are in the inventory and off the tree (design D8) |
| Risk | A choriocarcinoma, which the Diagnostic Pathway (§4D) calls the paediatric-relevant reading of this number, is entered under a row labelled with a benign mole |
| REDCap should offer | `9100 - Choriocarcinoma, NOS` |

`9101 - Choriocarcinoma combined with other germ cell elements` is a separate, correct row.

### 1.3 `9086` — "Label not found"

| | |
|---|---|
| Option string | `Label not found in the provided "Cancer Morphology.pdf" source.` in the option file (subgroup Xb6). The 1 October 2026 snapshot's `x_morph` has **no `9086` choice** |
| ICD-O-3.2 | `9086/3` Preferred, ***Germ cell tumor with associated hematological malignancy***, a new code in ICD-O-3.2 (IARC, *3.1 to 3.2 — New codes and their terms*, p. 2) |
| ICCC-2017 | range 105, subgroup Xb6, extragonadal sites only |
| What the tool emits | `9086/3` from `eg_mixed` (the extragonadal tree), when the report lists an associated haematological malignancy |
| Risk | The option file carries a placeholder from the source-extraction step in place of a term; the dropdown, if it carries the row, shows the clerk a message about a PDF. The snapshot suggests it does not carry the row, so a `9086` case has nothing to select |
| REDCap should offer | `9086 - Germ cell tumor with associated hematological malignancy` |

**One thing not to do.** Diagnostic Pathway §8 item 7 warns against labelling `9086` *Mixed
embryonal carcinoma and teratoma*. That is a Synonym of `9081/3`, and the label would collide
with `9081`. `9086` is a different number with a different entity.

---

## 2. Class D — a below-behaviour-3 label on a number the tool emits at behaviour 3

54 options. The label is an ICD-O-3.2 term at behaviour 0, 1 or 2; for `8213` it differs from that
term only in ", NOS". The tool emits the number at behaviour 3 under the term in the fourth column.
§2.1 lists the rows whose behaviour-3 code the trees emit, the same hazard as §1.1 and §1.2; §2.2 lists
those the tool reaches by search only.

`9080`, `9084` and `9100` need one decision from the REDCap side. The central nervous system tree
registers `9080` at behaviours 0, 1 and 3 and `9084` at 0 and 3, and a dropdown row cannot carry
a behaviour. Name the behaviour-3 term, as proposed here, or a behaviour-neutral term; either
is better than the benign term the rows carry now.

In the "Also shown" column, *code* means a tree registers the number at that behaviour (the central
nervous system tree does for `9080/0`, `9080/1`, `9084/0`), *exclusion* means a tree shows it as not
registered, and *search* means only the inventory holds it.

### 2.1 The tree emits the behaviour-3 code (21 options)

| Number | Option string | The string is | The tool emits at /3 | Also shown by the tool | Relabel to |
|---|---|---|---|---|---|
| `9064` | Intratubular malignant germ cells | `9064/2` Preferred | *Germinoma* | /2 exclusion | `9064 - Germinoma` |
| `9080` | Teratoma, benign | `9080/0` Preferred | *Teratoma, malignant, NOS* | /0 code and exclusion, /1 code and exclusion | `9080 - Teratoma, malignant, NOS` |
| `9084` | Dermoid cyst, NOS | `9084/0` Preferred | *Teratoma with malignant transformation* | /0 code and exclusion | `9084 - Teratoma with malignant transformation` |
| `9100` | Hydatidiform mole, NOS | `9100/0` Preferred | *Choriocarcinoma, NOS* | /0 exclusion, /1 exclusion | `9100 - Choriocarcinoma, NOS` |
| `9090` | Struma ovarii, NOS | `9090/0` Preferred | *Struma ovarii, malignant* | /0 exclusion | `9090 - Struma ovarii, malignant` |
| `8010` | Epithelial tumor, benign | `8010/0` Preferred | *Carcinoma, NOS* | — | `8010 - Carcinoma, NOS` |
| `8140` | Adenoma, NOS | `8140/0` Preferred | *Adenocarcinoma, NOS* | — | `8140 - Adenocarcinoma, NOS` |
| `8310` | Clear cell adenoma | `8310/0` Preferred | *Clear cell adenocarcinoma, NOS* | — | `8310 - Clear cell adenocarcinoma, NOS` |
| `8380` | Endometrioid adenoma, NOS | `8380/0` Preferred | *Endometrioid adenocarcinoma, NOS* | /1 exclusion | `8380 - Endometrioid adenocarcinoma, NOS` |
| `8441` | Serous cystadenoma, NOS | `8441/0` Preferred | *Serous carcinoma, NOS* | /0 exclusion | `8441 - Serous carcinoma, NOS` |
| `8461` | Serous surface papilloma | `8461/0` Preferred | *High grade serous carcinoma* | — | `8461 - High grade serous carcinoma` |
| `8470` | Mucinous cystadenoma, NOS | `8470/0` Preferred | *Mucinous cystadenocarcinoma, NOS* | /0 exclusion | `8470 - Mucinous cystadenocarcinoma, NOS` |
| `8480` | Mucinous adenoma | `8480/0` Preferred | *Mucinous adenocarcinoma* | — | `8480 - Mucinous adenocarcinoma` |
| `8600` | Thecoma, NOS | `8600/0` Preferred | *Thecoma, malignant* | /0 exclusion | `8600 - Thecoma, malignant` |
| `8631` | Sertoli-Leydig cell tumor, well differentiated | `8631/0` Preferred | *Sertoli-Leydig cell tumor, poorly differentiated* | /0 exclusion, /1 exclusion | `8631 - Sertoli-Leydig cell tumor, poorly differentiated` |
| `8634` | Sertoli-Leydig cell tumor, intermediate differentiation, with heterologous elements | `8634/1` Preferred | *Sertoli-Leydig cell tumor, poorly differentiated, with heterologous elements* | /1 exclusion | `8634 - Sertoli-Leydig cell tumor, poorly differentiated, with heterologous elements` |
| `8640` | Sertoli cell tumor, NOS | `8640/1` Preferred | *Sertoli cell carcinoma* | /1 exclusion | `8640 - Sertoli cell carcinoma` |
| `8670` | Lipid cell tumor of ovary | `8670/0` Preferred | *Steroid cell tumor, malignant* | /0 exclusion | `8670 - Steroid cell tumor, malignant` |
| `8000` | Neoplasm, benign | `8000/0` Preferred | *Neoplasm, malignant* | — | `8000 - Neoplasm, malignant` |
| `8001` | Tumor cells, benign | `8001/0` Preferred | *Tumor cells, malignant* | — | `8001 - Tumor cells, malignant` |
| `8005` | Clear cell tumor, NOS | `8005/0` Preferred | *Malignant tumor, clear cell type* | — | `8005 - Malignant tumor, clear cell type` |

### 2.2 The behaviour-3 code is reached by search only (33 options)

| Number | Option string | The string is | The tool emits at /3 | Also shown by the tool | Relabel to |
|---|---|---|---|---|---|
| `8011` | Epithelioma, benign | `8011/0` Preferred | *Epithelioma, malignant* | — | `8011 - Epithelioma, malignant` |
| `8050` | Papilloma, NOS | `8050/0` Preferred | *Papillary carcinoma, NOS* | — | `8050 - Papillary carcinoma, NOS` |
| `8051` | Verrucous papilloma | `8051/0` Preferred | *Verrucous carcinoma, NOS* | — | `8051 - Verrucous carcinoma, NOS` |
| `8052` | Squamous cell papilloma, NOS | `8052/0` Preferred | *Papillary squamous cell carcinoma* | — | `8052 - Papillary squamous cell carcinoma` |
| `8070` | Squamous cell carcinoma in situ, NOS | `8070/2` Preferred | *Squamous cell carcinoma, NOS* | — | `8070 - Squamous cell carcinoma, NOS` |
| `8120` | Transitional cell papilloma, benign | `8120/0` Synonym [obs] | *Transitional cell carcinoma, NOS* | — | `8120 - Transitional cell carcinoma, NOS` |
| `8121` | Schneiderian papilloma, NOS | `8121/0` Synonym | *Schneiderian carcinoma* | — | `8121 - Schneiderian carcinoma` |
| `8130` | Papillary transitional cell neoplasm of low malignant potential | `8130/1` Synonym | *Papillary urothelial carcinoma* | — | `8130 - Papillary urothelial carcinoma` |
| `8190` | Trabecular adenoma | `8190/0` Preferred | *Trabecular adenocarcinoma* | — | `8190 - Trabecular adenocarcinoma` |
| `8200` | Eccrine dermal cylindroma | `8200/0` Preferred | *Adenoid cystic carcinoma* | — | `8200 - Adenoid cystic carcinoma` |
| `8201` | Cribriform carcinoma in situ | `8201/2` Preferred | *Cribriform carcinoma, NOS* | — | `8201 - Cribriform carcinoma, NOS` |
| `8210` | Adenomatous polyp, NOS | `8210/0` Preferred | *Adenocarcinoma in adenomatous polyp* | — | `8210 - Adenocarcinoma in adenomatous polyp` |
| `8211` | Tubular adenoma, NOS | `8211/0` Preferred | *Tubular adenocarcinoma* | — | `8211 - Tubular adenocarcinoma` |
| `8213` | Serrated adenoma | `8213/0` Preferred (the string differs from the term only in ", NOS") | *Serrated adenocarcinoma* | — | `8213 - Serrated adenocarcinoma` |
| `8221` | Multiple adenomatous polyps | `8221/0` Preferred | *Adenocarcinoma in multiple adenomatous polyps* | — | `8221 - Adenocarcinoma in multiple adenomatous polyps` |
| `8245` | Tubular carcinoid | `8245/1` Preferred | *Adenocarcinoid tumor* | — | `8245 - Adenocarcinoid tumor` |
| `8260` | Papillary adenoma, NOS | `8260/0` Preferred | *Papillary adenocarcinoma, NOS* | — | `8260 - Papillary adenocarcinoma, NOS` |
| `8261` | Villous adenoma, NOS | `8261/0` Preferred | *Adenocarcinoma in villous adenoma* | — | `8261 - Adenocarcinoma in villous adenoma` |
| `8263` | Tubulovillous adenoma, NOS | `8263/0` Preferred | *Adenocarcinoma in tubulovillous adenoma* | — | `8263 - Adenocarcinoma in tubulovillous adenoma` |
| `8290` | Oxyphilic adenoma | `8290/0` Preferred | *Oxyphilic adenocarcinoma* | — | `8290 - Oxyphilic adenocarcinoma` |
| `8313` | Clear cell adenofibroma | `8313/0` Preferred | *Clear cell adenocarcinofibroma* | — | `8313 - Clear cell adenocarcinofibroma` |
| `8323` | Mixed cell adenoma | `8323/0` Preferred | *Mixed cell adenocarcinoma* | — | `8323 - Mixed cell adenocarcinoma` |
| `8381` | Endometrioid adenofibroma, NOS | `8381/0` Preferred | *Endometrioid adenofibroma, malignant* | — | `8381 - Endometrioid adenofibroma, malignant` |
| `8410` | Sebaceous adenoma | `8410/0` Related | *Sebaceous carcinoma* | — | `8410 - Sebaceous carcinoma` |
| `8440` | Cystadenoma, NOS | `8440/0` Preferred | *Cystadenocarcinoma, NOS* | — | `8440 - Cystadenocarcinoma, NOS` |
| `8450` | Papillary cystadenoma, NOS | `8450/0` Preferred | *Papillary cystadenocarcinoma, NOS* | — | `8450 - Papillary cystadenocarcinoma, NOS` |
| `8504` | Intracystic papillary adenoma | `8504/0` Preferred | *Encapsulated papillary carcinoma with invasion* | — | `8504 - Encapsulated papillary carcinoma with invasion` |
| `8550` | Acinar cell adenoma | `8550/0` Preferred | *Acinar cell carcinoma* | — | `8550 - Acinar cell carcinoma` |
| `8560` | Mixed squamous cell and glandular papilloma | `8560/0` Preferred | *Adenosquamous carcinoma* | — | `8560 - Adenosquamous carcinoma` |
| `9000` | Brenner tumor, NOS | `9000/0` Preferred | *Brenner tumor, malignant* | — | `9000 - Brenner tumor, malignant` |
| `9014` | Serous adenofibroma, NOS | `9014/0` Preferred | *Serous adenocarcinofibroma* | — | `9014 - Serous adenocarcinofibroma` |
| `9015` | Mucinous adenofibroma, NOS | `9015/0` Preferred | *Mucinous adenocarcinofibroma* | — | `9015 - Mucinous adenocarcinofibroma` |
| `8630` | Androblastoma, benign | `8630/0` Preferred [obs] | *Androblastoma, malignant* | — | `8630 - Androblastoma, malignant` |

`8000`, `8001` and `8005` are the gonadal not-otherwise-specified fallback (§2.1). ICCC-2017 range 117
places `8000`–`8005` at the ovary and testis in Xe, and the tool emits `8000/3` for a malignant
tumour of type not stated (design D13). A clerk who matches `8000` finds *Neoplasm, benign*.

---

## 3. Class B and C1 — relabel

### 3.1 Class B (4) — a behaviour-3 term that is not the preferred one

| Number | Option string | ICD-O-3.2 | Relabel to |
|---|---|---|---|
| `8122` | Transitional cell carcinoma, spindle cell | `8122/3` Synonym | `8122 - Urothelial carcinoma, sarcomatoid` |
| `8131` | Transitional cell carcinoma, micropapillary | `8131/3` Synonym | `8131 - Urothelial carcinoma, micropapillary` |
| `8158` | Endocrine tumor, functioning, NOS | `8158/3` Related [obs] | `8158 - ACTH-producing tumor` |
| `8620` | Granulosa cell tumor, adult type | `8620/3` Related | `8620 - Adult granulosa cell tumor of ovary` |

### 3.2 Class C1 (7) — no exact ICD-O-3.2 term, on a number the tool emits at behaviour 3

| Number | Option string | ICD-O-3.2 preferred terms on this number | The tool emits at /3 | Relabel to |
|---|---|---|---|---|
| `9071` | Yolk sac tumor | /3 *Yolk sac tumor, NOS* | *Yolk sac tumor, NOS* (tree) (the string differs from the /3 term only in ", NOS") | `9071 - Yolk sac tumor, NOS` |
| `8153` | Gastrinoma, NOS | /3 *Gastrinoma* | *Gastrinoma* (search) (the string differs from the /3 term only in ", NOS") | `8153 - Gastrinoma` |
| `8240` | Carcinoid tumor of uncertain malignant potential | /3 *Neuroendocrine tumor, NOS* | *Neuroendocrine tumor, NOS* (search) | `8240 - Neuroendocrine tumor, NOS` |
| `8384` | Adenocarcinoma, endocervical type | /3 *Adenocarcinoma, endocervical type, NOS* | *Adenocarcinoma, endocervical type, NOS* (search) (the string differs from the /3 term only in ", NOS") | `8384 - Adenocarcinoma, endocervical type, NOS` |
| `8452` | Solid pseudopapillary tumor | /1 *Solid pseudopapillary tumor of ovary*; /3 *Solid pseudopapillary neoplasm of pancreas* | *Solid pseudopapillary neoplasm of pancreas* (search) | `8452 - Solid pseudopapillary neoplasm of pancreas` |
| `8460` | Papillary serous cystadenoma, NOS | /2 *Serous borderline tumor, micropapillary variant*; /3 *Low grade serous carcinoma* | *Low grade serous carcinoma* (tree) | `8460 - Low grade serous carcinoma` |
| `8650` | Leydig cell tumor, benign | /0 *Leydig cell tumor of ovary, NOS*; /1 *Leydig cell tumor of testis, NOS*; /3 *Leydig cell tumor, malignant* | *Leydig cell tumor, malignant* (tree) | `8650 - Leydig cell tumor, malignant` |

`8460`, `8650` and `8240` read as benign or borderline tumours, and the tool emits `8460/3` and
`8650/3` from its trees (low grade serous carcinoma of the ovary; malignant Leydig cell tumour).
Those two rows are as sharp as the class D rows in §2.1.

---

## 4. Class C2 (5) — the number is deleted from ICD-O-3.2

ICD-O-3.2 deleted these four-digit codes and all their extensions (IARC, *3.1 to 3.2 — Deleted codes
and their terms*, 9 October 2020, p. 1). The tool has no entry on any of them. A record on one of
these numbers needs re-coding from the report to the code its terms moved to.

| Number | Option string | ICD-O-3.2 | Terms moved to |
|---|---|---|---|
| `8444` | Clear cell cystic tumor of borderline malignancy | deleted | `8313/1` |
| `8462` | Serous papillary cystic tumor of borderline malignancy | deleted | `8442/1` |
| `8463` | Serous surface papillary tumor of borderline malignancy | deleted | `8442/1` |
| `8471` | Papillary mucinous cystadenoma, NOS | deleted | `8470/0`, `8470/3` |
| `8473` | Papillary mucinous cystadenoma, borderline malignancy | deleted | `8472/1` |

Every destination is below behaviour 3 except `8470/3`, which takes *Papillary mucinous
cystadenocarcinoma* from `8471`. The tool emits `8470/3` Mucinous cystadenocarcinoma. Whether the
dropdown keeps the five rows is the registrar's decision (§8 step 6).

---

## 5. Class E (28) — a term that exists only below behaviour 3

ICCC-3 Group X declares behaviour 3 outside the central nervous system, and ICD-O-3.2 has no
behaviour-3 term on these numbers, so none of them can be a Group X cancer.

### 5.1 E1 (13) — the tool shows the term as a behaviour exclusion

| Number | Option string | ICD-O-3.2 | Where the tool shows it |
|---|---|---|---|
| `9103` | Partial hydatidiform mole | `9103/0` Preferred | exclusion in `g10_extragonadal` |
| `9104` | Placental site trophoblastic tumor | `9104/1` Preferred | exclusion in `g10_extragonadal`, `g10_testis` |
| `9091` | Strumal carcinoid | `9091/1` Preferred | exclusion in `g10_ovary` |
| `9073` | Gonadoblastoma | `9073/1` Preferred | exclusion in `g10_ovary`, `g10_testis` |
| `8442` | Serous cystadenoma, borderline malignancy | `8442/1` Synonym | exclusion in `g10_ovary` |
| `8472` | Mucinous cystic tumor of borderline malignancy | `8472/1` Preferred | exclusion in `g10_ovary` |
| `8590` | Sex cord-gonadal stromal tumor, NOS | `8590/1` Preferred | exclusion in `g10_ovary`, `g10_testis` |
| `8592` | Sex cord-gonadal stromal tumor, mixed forms | `8592/1` Preferred | exclusion in `g10_testis` |
| `8622` | Granulosa cell tumor, juvenile | `8622/1` Preferred | exclusion in `g10_ovary` |
| `8623` | Sex cord tumor with annular tubules | `8623/1` Preferred | exclusion in `g10_ovary` |
| `8632` | Gynandroblastoma | `8632/1` Preferred | exclusion in `g10_ovary` |
| `8633` | Sertoli-Leydig cell tumor, retiform | `8633/1` Preferred | exclusion in `g10_ovary` |
| `8642` | Large cell calcifying Sertoli cell tumor | `8642/1` Preferred | exclusion in `g10_testis` |

### 5.2 E2 (15) — the tool does not show it

| Number | Option string | ICD-O-3.2 |
|---|---|---|
| `8040` | Tumorlet, benign | `8040/0` Preferred |
| `8053` | Squamous cell papilloma, inverted | `8053/0` Preferred |
| `8191` | Embryonal adenoma | `8191/0` Preferred |
| `8443` | Clear cell cystadenoma | `8443/0` Preferred |
| `8451` | Papillary cystadenoma, borderline malignancy | `8451/1` Preferred [obs] |
| `8561` | Adenolymphoma | `8561/0` Preferred |
| `8591` | Sex cord-gonadal stromal tumor, incompletely differentiated | `8591/1` Preferred |
| `8593` | Stromal tumor with minor sex cord elements | `8593/1` Preferred |
| `8601` | Thecoma, luteinized | `8601/0` Preferred |
| `8602` | Sclerosing stromal tumor | `8602/0` Preferred |
| `8610` | Luteoma, NOS | `8610/0` Preferred |
| `8621` | Granulosa cell-theca cell tumor | `8621/1` Preferred |
| `8641` | Sertoli cell tumor with lipid storage | `8641/0` Preferred |
| `8660` | Hilus cell tumor | `8660/0` Preferred |
| `8671` | Adrenal rest tumor | `8671/0` Preferred |

The lookup tool records the commonest below-behaviour-3 tumours as exclusions with a registrar flag
(`docs/group_10_registrar_review.md` A1, A4, A6). Whether the registry keeps the rest in the
dropdown is the question Groups IV to VIII raised.

---

## 6. Class F — `8474`, the second "Label not found"

| | |
|---|---|
| Option string | `Label not found in the provided "Cancer Morphology.pdf" source.` (the Xd list) |
| ICD-O-3.2 | `8474/3` Preferred, ***Seromucinous carcinoma***. `8474/0` *Seromucinous cystadenoma* and `8474/1` *Seromucinous borderline tumor* are new in ICD-O-3.2 (IARC, *New codes and their terms*, p. 1) |
| What the tool emits | `8474/3` from `ov_epithelial`; `8474/1` as a behaviour exclusion (seromucinous borderline tumour; design D14) |
| REDCap should offer | `8474 - Seromucinous carcinoma` |

---

## 7. Class G — 6 codes the tool emits that no option names

The data carries no flag for them (standing rule 16, 4 October 2026): this table and
`docs/TODO.md` §7 are the record. Append them at the end of the list.

| Code | ICD-O-3.2 preferred term | ICCC-2017 | Reached from | Append |
|---|---|---|---|---|
| `8023/3` | Nuclear protein in testis (NUT)-associated carcinoma | Xd | search only | `8023 - Nuclear protein in testis (NUT)-associated carcinoma` |
| `8054/3` | Warty carcinoma | Xd | search only | `8054 - Warty carcinoma` |
| `8230/3` | Solid carcinoma, NOS | Xd | search only | `8230 - Solid carcinoma, NOS` |
| `8231/3` | Carcinoma simplex | Xd | search only | `8231 - Carcinoma simplex` |
| `8482/3` | Mucinous carcinoma, gastric type | Xd | search only | `8482 - Mucinous carcinoma, gastric type` |
| `9102/3` | Malignant teratoma, trophoblastic | Xc5 | `g10_ovary`, `g10_testis` | `9102 - Malignant teratoma, trophoblastic` |

`8594/1` *Mixed germ cell-sex cord-stromal tumor, NOS* is new in ICD-O-3.2 and appears on a
behaviour exclusion in `ov_gonadoblastoma` and `ts_gonadoblastoma`. It is not in the option file.
It is below behaviour 3 and needs no option unless the registrar keeps below-behaviour-3 rows.

---

## 8. Pre-flight, and the repair proposed

**Before anything changes**, export `record_id`, `x_morph`, `topo_code` and `x_subgroup`, and count
records on the numbers whose label names a different tumour from the one the tool emits: `9064`,
`9100`, `9080`, `9084`, `9090`, `8000`, `8001`, `8005`, `8460`, `8650`, and the five deleted numbers
in §4. A record on `9064` is a germinoma, a germ cell tumour of unnamed type or a true germ cell
neoplasia in situ, and the dictionary cannot say which; read the report. The registry began
operating in 2025. Count first:
the repair is cheapest before records accumulate on a wrong label.

The three safe operations are unchanged (`docs/TODO.md` §7): relabel in place, retire in place
(prefix `[RETIRED]`), append at the end.

1. Relabel `9064` and `9100` (§1.1, §1.2).
2. Replace the `9086` and `8474` labels (§1.3, §6); add `9086` to the dictionary if the snapshot is
   right and the option file is stale.
3. Append the six codes in §7.
4. Relabel the class D rows in §2.1, then §2.2, to the behaviour-3 terms shown.
5. Relabel the class B and C1 rows in §3.
6. Decide, with the registrar, the five deleted numbers (§4) and the 28 class E rows (§5).

---

## 9. What the lookup tool already does

- Names every code by ICD-O-3.2's preferred term at its behaviour, never by the REDCap label.
- Carries no REDCap field. Until 4 October 2026 the entries generator wrote `redcap_option_verified`
  and `awaiting_layer1` from the option file; standing rule 16 removed both, so the drifted labels
  and the six codes with no option are recorded here and in `docs/TODO.md` §7 only. Nothing in the
  tool tests REDCap.

---

## 10. Two Layer 1 observations

1. **The 1 October 2026 snapshot has no `9086` choice**, although the option file lists one (§1.3).
   If the snapshot is the live dictionary, a Group X case on `9086` cannot be recorded today.
2. **The placeholder string** *Label not found in the provided "Cancer Morphology.pdf" source.* stands in
   for a term in two rows: `8474` in the snapshot and the option file, `9086` in the option file only.
   Both numbers are new codes in ICD-O-3.2 (IARC, *New codes and their terms*, pp. 1–2).

---

## 11. Class A (58) — correct as they stand

The label is the ICD-O-3.2 preferred term at behaviour 3, and the tool emits that behaviour.

| Number | Option string | Tool emits `/3` from |
|---|---|---|
| `9060` | Dysgerminoma | `g10_ovary`, `g10_testis` |
| `9061` | Seminoma, NOS | `g10_extragonadal`, `g10_ovary`, `g10_testis` |
| `9062` | Seminoma, anaplastic | `g10_testis` |
| `9063` | Spermatocytic seminoma | `g10_testis` |
| `9065` | Germ cell tumor, nonseminomatous | `g10_cns`, `g10_extragonadal`, `g10_ovary`, `g10_testis` |
| `9081` | Teratocarcinoma | `g10_cns`, `g10_extragonadal`, `g10_ovary`, `g10_testis` |
| `9082` | Malignant teratoma, undifferentiated | `g10_cns`, `g10_extragonadal`, `g10_ovary`, `g10_testis` |
| `9083` | Malignant teratoma, intermediate | `g10_cns`, `g10_extragonadal`, `g10_ovary`, `g10_testis` |
| `9070` | Embryonal carcinoma, NOS | `g10_cns`, `g10_extragonadal`, `g10_ovary`, `g10_testis` |
| `9072` | Polyembryoma | `g10_cns`, `g10_extragonadal`, `g10_ovary`, `g10_testis` |
| `9101` | Choriocarcinoma combined with other germ cell elements | `g10_cns`, `g10_extragonadal`, `g10_ovary`, `g10_testis` |
| `9085` | Mixed germ cell tumor | `g10_cns`, `g10_extragonadal`, `g10_ovary`, `g10_testis` |
| `9105` | Trophoblastic tumor, epithelioid | `g10_extragonadal`, `g10_testis` |
| `8012` | Large cell carcinoma, NOS | search only |
| `8013` | Large cell neuroendocrine carcinoma | search only |
| `8014` | Large cell carcinoma with rhabdoid phenotype | search only |
| `8015` | Glassy cell carcinoma | search only |
| `8020` | Carcinoma, undifferentiated, NOS | `g10_ovary` |
| `8021` | Carcinoma, anaplastic, NOS | search only |
| `8022` | Pleomorphic carcinoma | search only |
| `8030` | Giant cell and spindle cell carcinoma | search only |
| `8031` | Giant cell carcinoma | search only |
| `8032` | Spindle cell carcinoma, NOS | search only |
| `8033` | Pseudosarcomatous carcinoma | search only |
| `8034` | Polygonal cell carcinoma | search only |
| `8035` | Carcinoma with osteoclast-like giant cells | search only |
| `8041` | Small cell carcinoma, NOS | search only |
| `8044` | Small cell carcinoma, intermediate cell | `g10_ovary` |
| `8071` | Squamous cell carcinoma, keratinizing, NOS | search only |
| `8072` | Squamous cell carcinoma, large cell, nonkeratinizing, NOS | search only |
| `8073` | Squamous cell carcinoma, small cell, nonkeratinizing | search only |
| `8074` | Squamous cell carcinoma, spindle cell | search only |
| `8075` | Squamous cell carcinoma, adenoid | search only |
| `8082` | Lymphoepithelial carcinoma | search only |
| `8123` | Basaloid carcinoma | search only |
| `8141` | Scirrhous adenocarcinoma | search only |
| `8143` | Superficial spreading adenocarcinoma | search only |
| `8241` | Enterochromaffin cell carcinoid | search only |
| `8243` | Goblet cell carcinoid | search only |
| `8244` | Mixed adenoneuroendocrine carcinoma | search only |
| `8246` | Neuroendocrine carcinoma, NOS | search only |
| `8262` | Villous adenocarcinoma | search only |
| `8320` | Granular cell carcinoma | search only |
| `8382` | Endometrioid adenocarcinoma, secretory variant | search only |
| `8383` | Endometrioid adenocarcinoma, ciliated cell variant | search only |
| `8430` | Mucoepidermoid carcinoma | search only |
| `8481` | Mucin-producing adenocarcinoma | search only |
| `8490` | Signet ring cell carcinoma | search only |
| `8510` | Medullary carcinoma, NOS | search only |
| `8562` | Epithelial-myoepithelial carcinoma | search only |
| `8570` | Adenocarcinoma with squamous metaplasia | search only |
| `8571` | Adenocarcinoma with cartilaginous and osseous metaplasia | search only |
| `8572` | Adenocarcinoma with spindle cell metaplasia | search only |
| `8573` | Adenocarcinoma with apocrine metaplasia | search only |
| `8576` | Hepatoid adenocarcinoma | search only |
| `8002` | Malignant tumor, small cell type | `g10_ovary`, `g10_testis` |
| `8003` | Malignant tumor, giant cell type | `g10_ovary`, `g10_testis` |
| `8004` | Malignant tumor, spindle cell type | `g10_ovary`, `g10_testis` |

`8141` *Scirrhous adenocarcinoma* matches the preferred term, and ICD-O-3.2 marks every term on `8141/3` obsolete (`[obs]`)
including the preferred one. The tool reaches it by search only. `[obs]` marks a term string, not a
retired code (`docs/group_baseline_documents.md` §2); whether the code is current is a question for
ICD-O-3.2 and the group's WHO paper.
