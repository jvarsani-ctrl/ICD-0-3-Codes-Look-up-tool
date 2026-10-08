# Group 11 evidence — XIa adrenocortical carcinoma

Part `XIa_adrenal_cortex`. Sites: C74.0 cortex of adrenal gland and C74.9 adrenal gland, NOS.
ICCC-2017 places 8370–8375 in XIa at every site and 8158 in XIa at C74.0 only. The machine copy
of this file is `XIa_adrenal_cortex.json`. All 167 quotes in it were checked against the text
file page they cite. A negative control confirmed the checker: one changed quote and one wrong
page were both reported missing.

## 1 Sources

| File | Citation | WHO volume |
|---|---|---|
| `XIa-adrenal-cortex__Mete-2022.txt` | Mete O, Erickson LA, Juhlin CC, de Krijger RR, Sasano H, Volante M, Papotti MG. Overview of the 2022 WHO Classification of Adrenal Cortical Tumors. Endocr Pathol 2022;33(1):155–196. doi:10.1007/s12022-022-09710-8 | WHO Classification of Endocrine and Neuroendocrine Tumours, 5th edition, 2022 |
| `XIa-adrenal-cortex__ICCR-Adrenal-Cortex-2nd.txt` | International Collaboration on Cancer Reporting. Carcinoma of the Adrenal Cortex Histopathology Reporting Guide, 2nd edition, version 2.0, November 2025. ISBN 978-1-922324-68-9 | WHO Classification of Endocrine and Neuroendocrine Tumours, 5th edition, 2025 (ICCR 2025, PDF p. 5). This is the latest volume, so it is current |
| `ALL-paediatric-occurrence__Pfister-2022.txt` | Pfister SM, Reyes-Múgica M, Chan JKC, et al. A Summary of the Inaugural WHO Classification of Pediatric Tumors. Cancer Discov 2022;12(2):331–355 | WHO Classification of Paediatric Tumours, 5th edition, 2022 |
| `RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt` | WHO. International Classification of Diseases for Oncology, 3rd edition, 1st revision, section 4, printed pp. 14–28 | The coding manual, not a classification |

The ICCR guide reproduces the WHO 2025 table of adrenal cortical carcinomas. It holds one row:
adrenal cortical carcinoma, 8370/3 (ICCR 2025, PDF p. 7, read from the page image). Mete 2022
holds no ICD-O code table.

## 2 Entities

| Entity (WHO wording) | Code | ICD-O-3.2 term matched (level) | Paediatric | Decision | Page |
|---|---|---|---|---|---|
| Adrenal cortical carcinoma, conventional | 8370/3 | Adrenal cortical carcinoma (Preferred) | occurs | option | ICCR 2025, PDF p. 7; Pfister 2022, PDF p. 14; Mete 2022, PDF p. 20 |
| Adrenal cortical carcinoma, oncocytic type | 8370/3 | Adrenal cortical carcinoma (Preferred) | occurs | option (same entry) | ICCR 2025, PDF p. 2; Mete 2022, PDF pp. 17, 21 |
| Adrenal cortical carcinoma, myxoid type | 8370/3 | Adrenal cortical carcinoma (Preferred) | not reported | option (same entry) | ICCR 2025, PDF p. 2; Mete 2022, PDF p. 17 |
| Adrenal cortical carcinoma, sarcomatoid type | 8370/3 | Adrenal cortical carcinoma (Preferred) | not reported | option (same entry) | ICCR 2025, PDF p. 2; Mete 2022, PDF pp. 17–18 |
| Adrenocortical tumour called malignant, or a Wieneke score of 4 or more | 8370/3 | Adrenal cortical tumor, malignant (Synonym) | occurs | option | Mete 2022, PDF pp. 1, 21 |
| Adrenal cortical adenoma | 8370/0 | Adrenal cortical adenoma, NOS (Preferred) | occurs | exclusion | Mete 2022, PDF p. 21 |
| Adrenocortical tumour with no behaviour stated | 8370/0 | Adrenal cortical tumor, NOS (Synonym of Adrenal cortical adenoma, NOS) | occurs | exclusion | Pfister 2022, PDF p. 14 |
| Oncocytic adrenal cortical adenoma | 8370/0 | Adrenal cortical adenoma, NOS (Preferred) | not reported | exclusion | Mete 2022, PDF pp. 14, 19 |
| Adrenal cortical adenoma, compact cell | 8371/0 | same (Preferred) | not reported | exclusion | ICD-O-3.2 |
| Adrenal cortical adenoma, pigmented | 8372/0 | same (Preferred) | not reported | exclusion | Mete 2022, PDF p. 15 |
| Adrenal cortical adenoma, clear cell | 8373/0 | same (Preferred) | not reported | exclusion | ICD-O-3.2 |
| Adrenal cortical adenoma, glomerulosa cell | 8374/0 | same (Preferred) | not reported | exclusion | ICD-O-3.2 |
| Adrenal cortical adenoma, mixed cell | 8375/0 | same (Preferred) | not reported | exclusion | ICD-O-3.2 |
| Adrenal cortical neoplasm of uncertain malignant potential | 8370/1 (Rule F) | none: ICD-O-3.2 prints no 8370/1 | occurs | exclusion (registrar: show the code or not) | ICCR 2025, PDF pp. 2, 7; Mete 2022, PDF pp. 19, 21 |
| Adrenal myelolipoma | 8870/0 | Myelolipoma (Preferred) | not reported | exclusion | Mete 2022, PDF p. 2 |
| Adrenal cyst, pseudocyst, hyperplasia, nodular disease | none | not neoplasms | not reported | not registrable | Mete 2022, PDF pp. 2, 6 |
| Functioning adrenal cortical tumour (REDCap: Endocrine tumor, functioning, NOS) | 8158/3 | Endocrine tumor, functioning, NOS (Related, [obs]); Preferred ACTH-producing tumor | not reported | registrar | Mete 2022, PDF p. 2; ICCR 2025, PDF p. 1 |
| Carcinoma of the adrenal gland, origin not shown | 8010/3 | Carcinoma, NOS (Preferred) | not reported | option (immunohistochemistry fallback) | Mete 2022, PDF p. 23 |
| Malignant tumour, type not stated; registration without tissue | 8000/3 | Neoplasm, malignant (Preferred) | — | refer to Group XII | ICCC-2017 XIIb |
| Malignant cells on cytology | 8001/3 | Tumor cells, malignant (Preferred) | — | refer to Group XII | ICCC-2017 XIIb |
| Phaeochromocytoma | 8700/3 | Pheochromocytoma, NOS (Preferred) | occurs | refer to Group IV | Pfister 2022, PDF p. 14; ICCR 2025, PDF p. 4 |
| Paraganglioma | 8680/3 | Paraganglioma, NOS (Preferred) | occurs | refer to Group IV | Pfister 2022, PDF p. 14 |
| Neuroblastoma | 9500/3 | Neuroblastoma, NOS (Preferred) | common | refer to Group IV | Pfister 2022, PDF p. 10; ICCR 2025, PDF p. 4 |
| Ganglioneuroblastoma | 9490/3 | Ganglioneuroblastoma (Preferred) | occurs | refer to Group IV | ICCR 2025, PDF p. 4 |
| Sarcoma | 8800/3 | Sarcoma, NOS (Preferred) | not reported | refer to Group IX | ICCR 2025, PDF p. 4 |
| Lymphoma | 9590/3 | Malignant lymphoma, NOS (Preferred) | not reported | refer to Group II | ICCR 2025, PDF p. 4 |
| Teratoma or another germ cell tumour | 9080/3 | Teratoma, malignant, NOS (Preferred) | not reported | refer to Group X | Mete 2022, PDF p. 6 |
| Deposit (metastasis) or direct spread | — | — | occurs | refer, recapture_site | ICCR 2025, PDF pp. 4–5 |

The WHO 2025 table gives one code for adrenal cortical carcinoma. The conventional, oncocytic,
myxoid and sarcomatoid types (Mete 2022, PDF p. 1) are therefore one entry and one option.
Paediatric occurrence comes from three places. The WHO paediatric classification lists
adrenocortical tumours (Pfister 2022, PDF p. 14). Mete 2022 describes paediatric adrenal
cortical carcinoma as uncommon, with one age peak before 5 years and one in adolescence
(Mete 2022, PDF p. 20). Paediatric tumours sometimes show oncocytic differentiation
(Mete 2022, PDF p. 21).

**Paediatric criteria.** WHO 2022 assesses paediatric adrenal cortical neoplasms with the
Wieneke system (Mete 2022, PDF p. 1). The Weiss criteria used in adults over-diagnose carcinoma
in children (Mete 2022, PDF p. 21). The Wieneke system has nine parameters, each worth one
point: weight over 400 g, size over 10.5 cm, extension into periadrenal soft tissue or adjacent
organs, invasion into the vena cava, vascular invasion, capsular invasion, necrosis, more than 15
mitoses per 20 high-power fields, and atypical mitosis. A score of 4 or more is
malignant/poor outcome, a score of 3 is uncertain malignant potential, and a score of 2 or less
is benign behaviour (Mete 2022, PDF p. 21, Table 6; ICCR 2025, PDF p. 16).

## 3 The pathway

Every 8370/3 reason reads: "Recorded as Adrenal cortical carcinoma (8370/3) at the adrenal
cortex (C74.0)."

**`ac_evidence`** (document_inventory), "What is in the file for this adrenal tumour?"
Hint: hormone results do not change the code.
- Referral letter or clinical note only → `ac_clinical`.
- Imaging report only → `ac_imaging`.
- Cytology only (fine-needle aspirate) → `ac_cytology`.
- Histology report from a biopsy or resection → `ac_histology`.

No marker option. Visser Table 4 gives no hormone code for an adrenal cortical tumour (section 5).

**`ac_clinical`** (clinical_alias)
- The note states a malignant adrenal tumour, at least probable → refer to Group XII, 8000/3, basis 1.
- Possible or suspected only → not registrable.
- An imaging report is on file after all → `ac_imaging`.

**`ac_imaging`** (morphology_only)
- Imaging shows a malignant tumour, at least probable → refer to Group XII, 8000/3, basis 2.
- Possible only, benign, or a cyst → not registrable.
- A histology report is on file → `ac_histology`.

**`ac_cytology`** (morphology_only)
- Names adrenal cortical carcinoma → 8370/3, basis 5. Data gap 2 applies.
- Names neuroblastoma, phaeochromocytoma or another medulla tumour → refer to Group IV
  (Pfister 2022, PDF p. 14).
- Malignant cells, type not named → refer to Group XII, 8001/3, basis 5.
- No malignant cells, an adrenal cortical neoplasm not called malignant, or not diagnostic →
  `ac_imaging_cytology`. This node holds the imaging options, as Group 10 gave each evidence
  context its own node.

**`ac_histology`** (morphology_only), "What does the histology report call the tumour?"
Hint: the oncocytic, myxoid and sarcomatoid types take the conventional type's code, and low or
high grade does not change it.

| Option | Records | Recognition aid | Page |
|---|---|---|---|
| Adrenal cortical carcinoma (adrenocortical carcinoma, carcinoma of the adrenal cortex), of any type | 8370/3, basis 7; the reason adds that a periadrenal or suprarenal placement records the same | A report on a child often gives a Wieneke score out of 9; a score of 4 or more is the malignant category | ICCR 2025, PDF p. 7; Mete 2022, PDF pp. 1, 21 |
| Adrenocortical tumour or adrenal cortical neoplasm, without the word carcinoma or adenoma | → `ac_behaviour` | Paediatric reports often use adrenocortical tumour for both benign and malignant tumours and state the behaviour separately | Pfister 2022, PDF p. 14 |
| Adrenal cortical adenoma, of any type | exclusion, Adrenal cortical adenoma, NOS (8370/0) | A report on a child may give this as a Wieneke score of 2 or less | Mete 2022, PDF pp. 15, 21 |
| Adrenal cortical neoplasm of uncertain malignant potential | exclusion (8370/1 by Rule F) | A report on a child may give this as a Wieneke score of 3 | ICCR 2025, PDF pp. 2, 7; Mete 2022, PDF p. 21 |
| Myelolipoma | exclusion, Myelolipoma (8870/0) | — | Mete 2022, PDF p. 2 |
| Cyst or pseudocyst, haemorrhage, hyperplasia or nodular disease, with no tumour | not registrable | — | Mete 2022, PDF p. 6 |
| Carcinoma of the adrenal gland; the report does not say it began in the cortex | → `ac_ihc_carcinoma` | — | Mete 2022, PDF p. 23 |
| Malignant tumour or neoplasm of the adrenal gland, type not stated | → `ac_ihc_malignant` | — | Mete 2022, PDF p. 23 |
| Phaeochromocytoma, paraganglioma, neuroblastoma, ganglioneuroblastoma, or another medulla tumour | refer to Group IV | Phaeochromocytoma is also reported as pheochromocytoma or adrenal paraganglioma | Pfister 2022, PDF p. 14; Mete 2022, PDF p. 14 |
| Sarcoma of the adrenal gland | refer to Group IX; the reason says a sarcomatoid adrenal cortical carcinoma is the first option | — | ICCR 2025, PDF p. 4; Mete 2022, PDF p. 18 |
| Lymphoma of the adrenal gland | refer to Group II | — | ICCR 2025, PDF p. 4 |
| Teratoma or another germ cell tumour | refer to Group X | — | Mete 2022, PDF p. 6 |
| Deposit (metastasis) of a tumour that began elsewhere, or a kidney or liver tumour growing into the adrenal | refer, recapture_site true | The report may name the primary tumour, for example a melanoma, a lung carcinoma, or a kidney tumour | ICCR 2025, PDF pp. 4–5; Mete 2022, PDF p. 5 |

There is no long-tail picker. XIa holds one malignant code, 8370/3, and that code already has an
option. The only other XIa code is 8158/3, which waits on the registrar (section 8).

**`ac_behaviour`** (histology_subclassification), "The report calls the tumour an adrenocortical
tumour or adrenal cortical neoplasm. What does it say about its behaviour?" Hint: use the
diagnosis line, a comment or an addendum. With no behaviour stated, ICD-O-3.2 codes an adrenal
cortical tumour as benign.
- Malignant, or a Wieneke score of 4 or more out of 9 → 8370/3, basis 7. The reason notes that
  ICD-O-3.2 lists *Adrenal cortical tumor, malignant* under 8370/3.
- Uncertain malignant potential, or a Wieneke score of 3 → exclusion.
- Benign, or a Wieneke score of 2 or less → exclusion, 8370/0.
- No behaviour and no score → exclusion, 8370/0. ICD-O-3.2 files *Adrenal cortical tumor, NOS*
  under Adrenal cortical adenoma, NOS.

Source: Mete 2022, PDF p. 21, Table 6; ICCR 2025, PDF p. 16.

## 4 Immunohistochemistry rules

SF1 is the most reliable and specific marker of adrenal cortical origin (Mete 2022, PDF pp. 1,
23). Synaptophysin and alpha-inhibin do not separate a cortical tumour from a phaeochromocytoma.
An oncocytic adrenal cortical adenoma was once mislabelled as a phaeochromocytoma because of
synaptophysin staining, and SF1 positivity settled it (Mete 2022, PDF pp. 14, 23). Melan-A and
calretinin are non-specific (Mete 2022, PDF p. 23; ICCR 2025, PDF p. 17). Both checklists carry
the same hint, naming SF1 as the deciding marker.

| Panel | Positive | Records | Fallback | Page |
|---|---|---|---|---|
| `ac_ihc_carcinoma` (histology says carcinoma) | SF1 | 8370/3, basis 7 | 8010/3 Carcinoma, NOS | Mete 2022, PDF pp. 1, 14, 23 |
| `ac_ihc_malignant` (histology says malignant tumour) | SF1 | 8370/3, basis 7 | refer to Group XII, 8000/3 | Mete 2022, PDF pp. 1, 14, 23 |

SF1 alone does not prove malignancy, because adenomas also express it. Each rule therefore fires
only after the histology report has called the tumour malignant. The immunohistochemistry adds
the lineage and never stands in for the histology report. No rule refers to Group IV on
chromogranin A. The sources say that a chromogranin A-negative, SF1-positive tumour is cortical
(Mete 2022, PDF p. 14), but they do not state the converse.

## 5 Registration without tissue

| Evidence on file | Code | Basis | Route |
|---|---|---|---|
| Referral or clinical note stating a malignant adrenal tumour, at least probable | 8000/3 | 1 | refer to Group XII (ICCC XIIb at C74) |
| Imaging report showing a malignant adrenal tumour, at least probable | 8000/3 | 2 | refer to Group XII |
| Imaging with a raised cortisol, androgen or aldosterone result | 8000/3 | 2 | the imaging route; the hormone adds no code |

These rows rest on the registrar's Visser 2023 ruling as the controller gave it. Visser is not in
this part's file list (data gap 1). Visser Table 4 lists adrenocorticotropic hormone, 8158/3,
among the functioning tumours. At the adrenal cortex that route does not fit. An
ACTH-producing neoplasm drives adrenal cortical hyperplasia from outside the gland (Mete 2022,
PDF p. 2). Adrenal cortical carcinoma presents with ACTH-independent hypercortisolism
(ICCR 2025, PDF p. 1). The evidence gate therefore offers no marker option.

## 6 Laboratory tests

The sources name four hormone tests. None has a coding role, so the tree needs no laboratory
screen.

| Test | Role in the sources | Coding role | Page |
|---|---|---|---|
| Androgens | Androgen excess is the most frequent paediatric presentation, in up to 80%, with virilisation | none | Mete 2022, PDF pp. 16, 20 |
| Cortisol | ACTH-independent hypercortisolism, Cushing syndrome | none | ICCR 2025, PDF p. 1; Mete 2022, PDF p. 21 |
| Adrenocorticotropic hormone | A raised value points to a pituitary or ectopic source and adrenal hyperplasia | none at the adrenal cortex | Mete 2022, PDF p. 2 |
| Aldosterone-to-renin ratio | Diagnoses primary aldosteronism | none | Mete 2022, PDF p. 10 |

The sources do not state the specimen (serum, plasma or urine) for any of these tests.

## 7 Rules A to K

WHO ICD-O-3.1 manual pages are printed pages, with the PDF page in brackets.

- **A** (printed p. 14 [PDF p. 1]). Applies. Adrenal cortical carcinoma names its own tissue, so
  an abdominal, flank or retroperitoneal placement still records C74.0. This reaches the clerk
  through the reason on every 8370/3 option, which names C74.0.
- **B** (printed p. 14 [PDF p. 1]; printed p. 17 [PDF p. 4]). Applies. ICD-O lists *periadrenal
  tissue* as C48.0 retroperitoneum, but the tumour type indicates the adrenal cortex. This
  reaches the clerk through the reason on the `ac_histology` carcinoma option.
- **C** (printed p. 15 [PDF p. 2]). Not applied. No source describes a tumour overlapping cortex
  and medulla whose origin cannot be determined. The histology screen separates cortex from
  medulla by tumour type.
- **D** (printed p. 15 [PDF p. 2]). Referral only. The lymphoma reason says lymphomas are coded
  at the site where they began.
- **E**. Not applied: the tree has no leukaemia option.
- **F** (printed p. 15 [PDF p. 2]). Applies. `ac_behaviour` codes the behaviour the report
  states. This reaches the clerk through the question, the option labels and the hint. Uncertain
  malignant potential gives 8370/1 by Rule F, which ICD-O-3.2 does not print.
- **G** (printed p. 15 [PDF p. 2]). Not built (registrar, 7 October 2026). The WHO grade (low
  grade is 20 or fewer mitoses per 10 mm², Mete 2022, PDF p. 1) does not change the code, and the
  `ac_histology` hint says so.
- **H** (printed pp. 15, 23 [PDF pp. 2, 10]). Applies. ICD-O-3.2 prints (C74.0) beside every
  8370 term, and the reason names C74.0. The rule is set aside for a tumour that arises in
  ectopic adrenal tissue elsewhere (Mete 2022, PDF p. 5), once the metastasis option has been
  passed. Table 23 does not list 8370.
- **J** (printed p. 24 [PDF p. 11]). Applies. *Adrenocortical carcinoma*, *carcinoma of the
  adrenal cortex* and *adrenal cortical carcinoma* are listed together in the option label.
- **K** (printed p. 24 [PDF p. 11]). Applies. The oncocytic (8290), sarcomatoid (8033) and
  functioning (8158) forms take the numerically higher code, 8370/3, which agrees with the WHO
  2025 table. This reaches the clerk through the `ac_histology` hint.

## 8 Code currency

| Code | Finding | Action |
|---|---|---|
| 8370/3 | Current. ICD-O-3.2 Preferred term: Adrenal cortical carcinoma (C74.0). The REDCap label is identical. ICCC places it in XIa at every site | option |
| 8370/0 | Adrenal cortical adenoma, NOS. Synonyms: Adrenal cortical tumor, NOS; Adrenal cortical tumor, benign | exclusion |
| 8370/1 | Not in ICD-O-3.2. Rule F gives it | exclusion; registrar question 2 |
| 8371–8375 | Currency check section 5: /0 only. REDCap offers all five in XIa | exclusion under the adenoma option; REDCap-side list |
| 8158/3 | Currency check section 4: REDCap's label *Endocrine tumor, functioning, NOS* is the [obs] Related term, and the Preferred term is *ACTH-producing tumor*. Section 3: moved /1 → /3. ICCC places it in XIa at C74.0 only | registrar question 1; REDCap-side relabel |
| 8290/3, 8033/3 | Not used at the adrenal cortex: Rule K and the WHO table give 8370/3 | not offered |
| 8010/3 | Current. ICCC-2017 has no range for it at C74 | immunohistochemistry fallback; registrar question 5 |
| 8000/3, 8001/3 | ICCC XIIb at C74 | refer to Group XII |

## 9 Conflicts with other groups

- **Group IV.** The medulla tumours are Group IV at every site: neuroblastoma 9500/3 and
  ganglioneuroblastoma 9490/3 (IVa), and phaeochromocytoma 8700/3 and paraganglioma 8680–8693
  (IVb). A medulla tumour reported only as "adrenal gland" (C74.9) reaches this tree and refers
  out. Synaptophysin and alpha-inhibin stain both cortical and medullary tumours, so SF1 decides.
  An adrenal mass on imaging alone in a young child is more often neuroblastoma (data gap 5).
- **Group XII.** ICCC places 8000–8005 at C74 in XIIb. Every tissue-free route, malignant cells
  on cytology, and the malignant-tumour fallback therefore refer to Group XII, as Group 10 did at
  the central nervous system.
- **Group IX.** A sarcoma at C74 is IXe. A sarcomatoid adrenal cortical carcinoma is 8370/3 and
  must not go to Group IX (Mete 2022, PDF p. 18).
- **Group II.** An adrenal lymphoma is IIe.
- **Group X.** Teratoma at C74 is Xb2. Adrenal rests must be told apart from Leydig cell and other
  steroid cell gonadal tumours, which are Xe at every site (Mete 2022, PDF p. 5).
- **Groups VI and VII.** Ectopic adrenal tissue must be told apart from renal cell carcinoma and
  hepatocellular carcinoma (Mete 2022, PDF p. 5). An adrenal cortical carcinoma that invades the
  kidney, liver or pancreas stays at C74.0, because extent of invasion is a staging item
  (ICCR 2025, PDF p. 8). A kidney or liver tumour that grows into the adrenal goes through the
  deposit option.
- **Group XI, other trees.** 8370/3 is XIa at every site. The general carcinoma tree must offer
  adrenal cortical carcinoma arising in ectopic adrenal tissue (Mete 2022, PDF p. 5), or such a
  case would be recorded under XIf. At other sites, 8158/3 belongs to the XIb and XIf trees.

## 10 Data gaps

1. **Visser 2023 Table 4 at the adrenal.** Does any hormone or marker with imaging give an
   adrenal cortical code, and does the adrenocorticotropic hormone route apply to an adrenal
   mass? Visser is not in this part's file list. Candidate source: Visser O, et al. Front Oncol
   2023;13:1250549.
2. **Cytology of adrenal cortical carcinoma.** Neither source discusses it. Both the Wieneke and
   Weiss systems need a resection. Candidate source: WHO Endocrine and Neuroendocrine Tumours, 5th
   edition, 2025, adrenal cortical carcinoma chapter.
3. **The age range of the Wieneke criteria.** Both sources say "paediatric" without an age bound,
   and the registry covers ages 0 to 18. Candidate sources: Wieneke JA, et al. Am J Surg Pathol
   2003;27:867–881; Picard C, et al. Mod Pathol 2019;32:546–559.
4. **The WHO 2025 adrenal cortex chapter itself.** It would show whether a paediatric-specific
   term or code exists. Candidate source: WHO Classification of Tumours Editorial Board,
   Endocrine and Neuroendocrine Tumours, 5th edition, IARC 2025.
5. **A Group IV tissue-free route.** Does the built Group IV tree offer a tissue-free neuroblastoma
   route at the adrenal? This is a controller check of `group_04_dt.json`, not a paper.

### Questions only the registrar can answer

1. 8158/3 at C74.0: should it be kept off the adrenal cortex screens and the marker route?
2. Uncertain malignant potential: should the exclusion name 8370/1 by Rule F, or no code?
3. May the clerk record 8370/3 from a printed Wieneke score of 4 or more when the diagnosis line
   says only "adrenocortical tumour"? May an adolescent's Weiss score be used the same way?
4. "Adrenocortical tumour" with no behaviour and no score: is it an exclusion as 8370/0?
5. 8010/3 at C74.0 or C74.9 has no ICCC subgroup. Which Group XI subgroup does it take?
6. An adrenal cortical carcinoma whose site screen recorded C74.9: should it record C74.0, as the
   term and Rule H indicate?
