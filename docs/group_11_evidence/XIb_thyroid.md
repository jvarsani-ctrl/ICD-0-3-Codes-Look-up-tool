# Group 11 evidence — XIb thyroid carcinoma

Part `XIb_thyroid`, site C73.9. Evidence agent output, 8 October 2026. The JSON twin of this file is `XIb_thyroid.json`; every quote in it was checked against its page of the text file (171 cites, 0 failures), and the check was proved by a negative control that moved one cite to the wrong page and altered another.

## 1 Sources

| File | Citation | WHO volume |
|---|---|---|
| `XIb-thyroid__Juhlin-2022.txt` | Juhlin CC, Mete O, Baloch ZW. The 2022 WHO classification of thyroid tumors: novel concepts in nomenclature and grading. Endocrine-Related Cancer 2023;30(2):e220293. doi:10.1530/ERC-22-0293 | WHO Classification of Endocrine and Neuroendocrine Tumours, 5th edition, 2022 |
| `XIb-thyroid__ICCR-Thyroid-3rd.txt` | International Collaboration on Cancer Reporting. Carcinoma of the Thyroid Histopathology Reporting Guide, 3rd edition, version 3.1. Sydney: ICCR; November 2025. ISBN 978-1-922324-71-9 | WHO Classification of Endocrine and Neuroendocrine Tumours, 5th Edition (2025), as the dataset cites it (PDF p. 2, p. 8) |
| `ALL-paediatric-occurrence__Pfister-2022.txt` | Pfister SM, Reyes-Mugica M, Chan JKC, et al. A Summary of the Inaugural WHO Classification of Pediatric Tumors: Transitioning from the Optical into the Molecular Era. Cancer Discovery 2022;12(2):331-355 | WHO Classification of Paediatric Tumours, 5th edition, 2022 |
| `RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt` | World Health Organization. International Classification of Diseases for Oncology, 3rd edition, 1st revision (ICD-O-3.1), section 4 'Coding guidelines for topography and morphology', printed pp. 14-28 | not a tumour classification; the coding manual (PDF page 1 = printed p. 14) |

The ICCR dataset (November 2025) is the later document and cites the WHO 5th edition as published in 2025; Juhlin 2022 reviews the same edition at its 2022 release. Where they differ the ICCR dataset wins (ruling 7). ICCR Table 1 (PDF p. 9) was read from the page image. Facts from `icdo32.sqlite` and `ICCC-2017.sqlite` carry a `verified_by` field in the JSON instead of a page quote. Visser 2023 is not in this part's file set: the registration-without-tissue rows rest on the task brief and `docs/group_11_build_contract.md` §0.5.

ICCC-2017 range 121 places 8330–8332, 8334–8337, 8340–8347, 8350 and 8588 in XIb at every site; range 120 places the general carcinoma list in XIb at C73.9 only.

## 2 Entities

| Entity | Code | ICD-O-3.2 term (level) | Paediatric | Decision | Page |
|---|---|---|---|---|---|
| Papillary thyroid carcinoma, classic (usual, conventional) subtype | 8260/3 | Papillary carcinoma of thyroid (Related) | occurs | option | Pfister 2022, PDF p. 14; ICCR Thyroid 2025, PDF p. 9, table image; ICCR Thyroid 2025, PDF p. 9 |
| Infiltrative follicular variant of papillary thyroid carcinoma | 8340/3 | Papillary carcinoma, follicular variant (Preferred) | not_reported | option | ICCR Thyroid 2025, PDF p. 9, table image; ICCR Thyroid 2025, PDF p. 10 |
| Tall cell subtype of papillary thyroid carcinoma | 8344/3 | Papillary carcinoma, tall cell (Synonym) | not_reported | option | ICCR Thyroid 2025, PDF p. 2; ICCR Thyroid 2025, PDF p. 9 |
| Columnar cell subtype of papillary thyroid carcinoma | 8344/3 | Papillary carcinoma, columnar cell (Preferred) | not_reported | option | ICCR Thyroid 2025, PDF p. 9, table image; ICCR Thyroid 2025, PDF p. 9 |
| Oncocytic subtype of papillary thyroid carcinoma | 8342/3 | Papillary carcinoma, oncocytic variant (Preferred) | not_reported | option | ICCR Thyroid 2025, PDF p. 9, table image; Juhlin 2022, PDF p. 5 |
| Invasive encapsulated follicular variant of papillary thyroid carcinoma | 8343/3 | Papillary carcinoma, encapsulated, of thyroid (Preferred) | not_reported | option | ICCR Thyroid 2025, PDF p. 9, table image; ICCR Thyroid 2025, PDF p. 10 |
| Encapsulated subtype of papillary thyroid carcinoma (including encapsulated non-invasive papillary carcinoma) | 8343/3 | Papillary carcinoma, encapsulated, of thyroid (Preferred) | not_reported | option | ICCR Thyroid 2025, PDF p. 2; ICCR Thyroid 2025, PDF p. 10 |
| Diffuse sclerosing subtype of papillary thyroid carcinoma | 8260/3 | Papillary carcinoma of thyroid (Related) | not_reported | option | ICCR Thyroid 2025, PDF p. 2; ICCR Thyroid 2025, PDF p. 11; ICCR Thyroid 2025, PDF p. 9, table image |
| Solid, hobnail, Warthin-like, spindle cell, clear cell and fibromatosis-like stroma subtypes of papillary thyroid carcinoma | 8260/3 | Papillary carcinoma of thyroid (Related) | not_reported | option | ICCR Thyroid 2025, PDF p. 2; ICCR Thyroid 2025, PDF p. 11 |
| Papillary microcarcinoma (a size term, not a WHO subtype) | 8341/3 | Papillary microcarcinoma (Preferred) | not_reported | option | ICCR Thyroid 2025, PDF p. 10; Juhlin 2022, PDF p. 4 |
| Poorly differentiated thyroid carcinoma (including insular carcinoma and poorly differentiated oncocytic thyroid carcinoma) | 8337/3 | Poorly differentiated thyroid carcinoma (Preferred) | occurs | option | Juhlin 2022, PDF p. 5; ICCR Thyroid 2025, PDF p. 9, table image; ICCR Thyroid 2025, PDF p. 12 |
| Medullary thyroid carcinoma | 8345/3 | Medullary thyroid carcinoma (Preferred) | occurs | option | Pfister 2022, PDF p. 14; ICCR Thyroid 2025, PDF p. 9, table image; ICCR Thyroid 2025, PDF p. 12; Pfister 2022, PDF p. 19 |
| Spindle epithelial tumour with thymus-like elements | 8588/3 | Spindle epithelial tumor with thymus-like element (Preferred) | occurs | option | Pfister 2022, PDF p. 14; Juhlin 2022, PDF p. 7 |
| Follicular thyroid carcinoma, minimally invasive | 8335/3 | Follicular carcinoma, minimally invasive (Preferred) | not_reported | picker | Juhlin 2022, PDF p. 4; ICCR Thyroid 2025, PDF p. 11 |
| Follicular thyroid carcinoma, encapsulated angioinvasive | 8339/3 | Follicular carcinoma, encapsulated, angioinvasive (Preferred) | not_reported | picker | ICCR Thyroid 2025, PDF p. 2; ICCR Thyroid 2025, PDF p. 11 |
| Follicular thyroid carcinoma, widely invasive, or with no invasion extent stated | 8330/3 | Follicular carcinoma, NOS (Preferred) | not_reported | picker | ICCR Thyroid 2025, PDF p. 9, table image; ICCR Thyroid 2025, PDF p. 11 |
| Oncocytic carcinoma of the thyroid (minimally invasive, encapsulated angioinvasive or widely invasive) | 8290/3 | Oncocytic carcinoma (Synonym) | not_reported | picker | ICCR Thyroid 2025, PDF p. 9, table image; ICCR Thyroid 2025, PDF p. 11 |
| Anaplastic thyroid carcinoma | 8020/3 | Anaplastic undifferentiated carcinoma (Related) | not_reported | picker | ICCR Thyroid 2025, PDF p. 9, table image; ICCR Thyroid 2025, PDF p. 12 |
| Mixed medullary-follicular carcinoma | 8346/3 | Mixed medullary-follicular carcinoma (Preferred) | not_reported | picker | ICCR Thyroid 2025, PDF p. 9, table image |
| Mixed medullary-papillary carcinoma | 8347/3 | Mixed medullary-papillary carcinoma (Preferred) | not_reported | picker | ICCR Thyroid 2025, PDF p. 9, table image |
| Cribriform-morular thyroid carcinoma | 8201/3 | Cribriform carcinoma, NOS (Preferred) | not_reported | picker | ICCR Thyroid 2025, PDF p. 9, table image; ICCR Thyroid 2025, PDF p. 10; Juhlin 2022, PDF p. 1 |
| Mucoepidermoid carcinoma of the thyroid | 8430/3 | Mucoepidermoid carcinoma (Preferred) | not_reported | picker | ICCR Thyroid 2025, PDF p. 9, table image; Juhlin 2022, PDF p. 6 |
| Sclerosing mucoepidermoid carcinoma with eosinophilia | 8430/3 | Mucoepidermoid carcinoma (Preferred) | not_reported | picker | ICCR Thyroid 2025, PDF p. 3; Juhlin 2022, PDF p. 7 |
| Secretory carcinoma of the thyroid | 8502/3 | Secretory carcinoma (Preferred) | not_reported | picker | ICCR Thyroid 2025, PDF p. 9, table image; Juhlin 2022, PDF p. 7 |
| Intrathyroid thymic carcinoma (formerly carcinoma showing thymus-like differentiation) | 8589/3 | Intrathyroid thymic carcinoma (Preferred) | not_reported | picker | ICCR Thyroid 2025, PDF p. 3; Juhlin 2022, PDF p. 7 |
| Thymoma within the thyroid (types A, AB, B1, B2, B3) | 8580/3 | Thymoma, NOS (Preferred) | not_reported | picker | ICCR Thyroid 2025, PDF p. 3; Juhlin 2022, PDF p. 7 |
| Thymic carcinoma within the thyroid | 8586/3 | Thymic carcinoma, NOS (Preferred) | not_reported | picker | Juhlin 2022, PDF p. 7 |
| Differentiated high-grade thyroid carcinoma, dominant type not named | none | none | not_reported | registrar | ICCR Thyroid 2025, PDF p. 12; ICCR Thyroid 2025, PDF p. 2 |
| Squamous cell carcinoma of the thyroid (WHO 5th edition: a subtype of anaplastic thyroid carcinoma) | 8070/3 | Squamous cell carcinoma, NOS (Preferred) | not_reported | registrar | Juhlin 2022, PDF p. 6; ICCR Thyroid 2025, PDF p. 12 |
| Mixed medullary and oncocytic carcinoma | none | none | not_reported | registrar | ICCR Thyroid 2025, PDF p. 3 |
| Embryonal thyroid neoplasm (thyroblastoma) | none | none | not_reported | registrar | ICCR Thyroid 2025, PDF p. 3 |
| Papillary carcinoma, diffuse sclerosing (ICD-O-3.2 term on 8350/3) | 8350/3 | Papillary carcinoma, diffuse sclerosing (Related) | not_reported | not_built | ICCR Thyroid 2025, PDF p. 2 |
| Non-invasive follicular thyroid neoplasm with papillary-like nuclear features | 8349/1 | Non-invasive follicular thyroid neoplasm with papillary-like nuclear features (NIFTP) (Preferred) | not_reported | exclusion | Juhlin 2022, PDF p. 3; ICCR Thyroid 2025, PDF p. 10 |
| Follicular tumour of uncertain malignant potential | 8335/1 | Follicular tumor of uncertain malignant potential (Preferred) | not_reported | exclusion | ICCR Thyroid 2025, PDF p. 10; ICCR Thyroid 2025, PDF p. 11 |
| Follicular carcinoma, encapsulated, with no invasion stated | 8335/1 | Follicular carcinoma, encapsulated, NOS (Synonym) | not_reported | exclusion | ICCR Thyroid 2025, PDF p. 11 |
| Well differentiated tumour of uncertain malignant potential | 8348/1 | Well differentiated tumor of uncertain malignant potential (Preferred) | not_reported | exclusion | ICCR Thyroid 2025, PDF p. 11 |
| Hyalinizing trabecular tumour | 8336/1 | Hyalinizing trabecular tumor (Preferred) | not_reported | exclusion | ICCR Thyroid 2025, PDF p. 9, table image; Juhlin 2022, PDF p. 3 |
| Follicular adenoma of the thyroid (including follicular adenoma with papillary architecture) | 8330/0 | Follicular adenoma, NOS (Preferred) | occurs | exclusion | Pfister 2022, PDF p. 13; Juhlin 2022, PDF p. 3 |
| Oncocytic adenoma of the thyroid | 8290/0 | Oncocytic adenoma (Synonym) | not_reported | exclusion | Juhlin 2022, PDF p. 3; ICCR Thyroid 2025, PDF p. 18 |
| Teratoma of the thyroid | 9080/1 | Immature teratoma of thyroid (Related) | not_reported | refer to Group 10 | icdo32.sqlite: 9080/1 Related 'Immature teratoma of thyroid' (C73.9); ICCC-2017: 9080 at 739 -> Xb2 |
| Lymphoma of the thyroid | none | none | not_reported | refer to Group 2 | ICD-O-3.1 coding rules, PDF p. 2 (printed p. 15) |
| Sarcoma of the thyroid | none | none | not_reported | refer to Group 9 | ICCC-2017: 8800 at 739 -> IXe; 9120 at 739 -> IXd8 |

Paediatric evidence: Pfister 2022 Table 3 (printed pp. 343–344, PDF pp. 13–14) lists follicular adenoma, papillary thyroid carcinoma, medullary thyroid carcinoma and the spindle epithelial tumour with thymus-like elements. Juhlin 2022 (PDF p. 5) reports DICER1-associated poorly differentiated thyroid carcinoma in adolescents. ICCR (PDF p. 11) ties the good survival of the diffuse sclerosing subtype to the young age of patients without giving ages. Pfister 2022 (PDF p. 19) lists multiple endocrine neoplasia type 2 among the endocrine predisposition syndromes. No source reports follicular, oncocytic, anaplastic or cribriform-morular carcinoma in children, so those are picker entries (data gap 1, registrar question 1).

## 3 The pathway

### `th_evidence` (document_inventory)

**What is in the file for this thyroid tumour?**

Hint: Choose the strongest report in the file. A thyroid carcinoma reported in a neck lymph node or in the perithyroid tissue is recorded at the thyroid (C73.9). A report that calls the tumour possible or suspected does not register it.

| Option | Outcome | Records | Basis | Reason | Page |
|---|---|---|---|---|---|
| A referral letter or clinical note only | code | 8000/3 | 1 | Recorded as Neoplasm, malignant (8000/3), basis of diagnosis clinical. | Visser 2023 (brief) |
| An imaging report only (ultrasound, CT, MRI or a nuclear medicine scan) | code | 8000/3 | 2 | Recorded as Neoplasm, malignant (8000/3), basis of diagnosis imaging. | Visser 2023 (brief) |
| Imaging that shows a thyroid tumour, with a calcitonin result | go to `th_lab` |  |  | The calcitonin result decides whether the case can be recorded as medullary thyroid carcinoma without tissue. | Visser 2023 (brief) |
| A cytology report (fine-needle aspiration) | go to `th_cytology` |  |  |  |  |
| A histology report, with or without immunohistochemistry or gene reports | go to `th_histology` |  |  |  |  |

### `th_lab` (lab_results)

**What does the serum calcitonin result show?**

Hint: Use the reference range printed on the laboratory report. A raised calcitonin registers a case only when imaging shows the thyroid tumour.

| Option | Outcome | Records | Basis | Reason | Page |
|---|---|---|---|---|---|
| Raised above the laboratory's reference range | code | 8345/3 | 4 | Recorded as Medullary thyroid carcinoma (8345/3), basis of diagnosis tumour marker. | Visser 2023 (brief) |
| Within the reference range | code | 8000/3 | 2 | Recorded as Neoplasm, malignant (8000/3), basis of diagnosis imaging. | Visser 2023 (brief) |

### `th_cytology` (morphology_only)

**What does the cytology report call the tumour?**

Hint: Use the cytology report's own conclusion. Follicular carcinoma is diagnosed by invasion of the capsule or vessels, which only histology shows.

| Option | Outcome | Records | Basis | Reason | Page |
|---|---|---|---|---|---|
| Papillary thyroid carcinoma | code | 8260/3 | 5 | Recorded as Papillary adenocarcinoma, NOS (8260/3). ICD-O-3.2 gives Papillary carcinoma of thyroid as a related term of this code. | ICCR Thyroid 2025, PDF p. 9, table image |
| Medullary thyroid carcinoma | code | 8345/3 | 5 | Recorded as Medullary thyroid carcinoma (8345/3). | ICCR Thyroid 2025, PDF p. 9, table image |
| Malignant, carcinoma of a type the report does not name | code | 8010/3 | 5 | Recorded as Carcinoma, NOS (8010/3). |  |
| Follicular neoplasm, or suspicious for a follicular neoplasm | not_registrable |  |  | Not registrable. Cytology cannot show the capsular or vascular invasion that defines follicular carcinoma; register the case when histology reports it. | ICCR Thyroid 2025, PDF p. 11 |
| Suspicious for malignancy, indeterminate, or benign | not_registrable |  |  | Not registrable. A suspected or benign cytology result does not register a malignant tumour. | Visser 2023 (brief) |

### `th_histology` (histology_subclassification)

**What does the histology report call the tumour?**

Hint: Use the report's final diagnosis. When the report names a well-differentiated carcinoma with a poorly differentiated or anaplastic component, choose the higher-grade tumour (WHO coding Rule G). The benign and uncertain tumours at the end of this list are not recorded as cancers.

| Option | Outcome | Records | Basis | Reason | Page |
|---|---|---|---|---|---|
| Papillary thyroid carcinoma, any subtype, including papillary microcarcinoma and the encapsulated follicular variant | go to `th_ptc_subtype` |  |  |  Recognition aid: Reports describe papillae or follicles lined by cells with the nuclear features of papillary carcinoma. | Pfister 2022, PDF p. 14; Juhlin 2022, PDF p. 5 |
| Poorly differentiated thyroid carcinoma, or insular carcinoma | code | 8337/3 | 7 | Recorded as Poorly differentiated thyroid carcinoma (8337/3). Recognition aid: Reports describe solid, trabecular or insular growth without papillary carcinoma nuclei, with convoluted nuclei, 3 or more mitoses per 2 mm2, or tumour necrosis. | Juhlin 2022, PDF p. 5; ICCR Thyroid 2025, PDF p. 9, table image; ICCR Thyroid 2025, PDF p. 12 |
| Medullary thyroid carcinoma, or C-cell carcinoma | code | 8345/3 | 7 | Recorded as Medullary thyroid carcinoma (8345/3). Recognition aid: Reports describe a tumour of C cells that stains for calcitonin; the report may grade it low or high, which does not change the code. | Pfister 2022, PDF p. 14; ICCR Thyroid 2025, PDF p. 9, table image; Juhlin 2022, PDF p. 7 |
| Spindle epithelial tumour with thymus-like elements | code | 8588/3 | 7 | Recorded as Spindle epithelial tumor with thymus-like element (8588/3). | Pfister 2022, PDF p. 14 |
| A carcinoma whose type the report does not name, with immunohistochemistry results | go to `th_ihc` |  |  |  |  |
| A carcinoma whose type the report does not name, with no immunohistochemistry | code | 8010/3 | 7 | Recorded as Carcinoma, NOS (8010/3). |  |
| Another carcinoma the report names | go to `th_picker` |  |  |  |  |
| Non-invasive follicular thyroid neoplasm with papillary-like nuclear features | exclude | 8349/1 |  | Not recorded. Non-invasive follicular thyroid neoplasm with papillary-like nuclear features (NIFTP) is 8349/1 in ICD-O-3.2, not a malignant tumour. | ICCR Thyroid 2025, PDF p. 10 |
| Follicular tumour of uncertain malignant potential | exclude | 8335/1 |  | Not recorded. Follicular tumor of uncertain malignant potential is 8335/1 in ICD-O-3.2, not a malignant tumour. | ICCR Thyroid 2025, PDF p. 11 |
| Well differentiated tumour of uncertain malignant potential | exclude | 8348/1 |  | Not recorded. Well differentiated tumor of uncertain malignant potential is 8348/1 in ICD-O-3.2, not a malignant tumour. | ICCR Thyroid 2025, PDF p. 11 |
| Hyalinizing trabecular tumour, or hyalinizing trabecular adenoma | exclude | 8336/1 |  | Not recorded. Hyalinizing trabecular tumor is 8336/1 in ICD-O-3.2, not a malignant tumour. | ICCR Thyroid 2025, PDF p. 9, table image |
| Follicular adenoma, including follicular adenoma with papillary architecture | exclude | 8330/0 |  | Not recorded. Follicular adenoma, NOS is 8330/0 in ICD-O-3.2, a benign tumour. | Pfister 2022, PDF p. 13 |
| Oncocytic adenoma, or Hurthle cell adenoma | exclude | 8290/0 |  | Not recorded. Oxyphilic adenoma is 8290/0 in ICD-O-3.2, a benign tumour. | Juhlin 2022, PDF p. 3 |
| Thyroid follicular nodular disease, goitre or an adenomatous nodule | not_registrable |  |  | Not registrable. Follicular nodular disease is not a malignant tumour. | Juhlin 2022, PDF p. 2 |
| Lymphoma | refer to Group 2 |  |  | Lymphomas are ICCC-3 Group II. A lymphoma that arises in the thyroid keeps the thyroid as its site (C73.9). | ICD-O-3.1 coding rules, PDF p. 2 (printed p. 15) |
| Sarcoma, for example angiosarcoma | refer to Group 9 |  |  | Soft-tissue sarcomas are ICCC-3 Group IX. | ICCC-2017: 8800 at 739 -> IXe; 9120 at 739 -> IXd8 |
| Teratoma | refer to Group 10 |  |  | Teratomas are ICCC-3 Group X. | ICCC-2017: 9080 at 739 -> Xb2; icdo32.sqlite 9080/1 Immature teratoma of thyroid |
| A deposit (metastasis) of a tumour that began outside the thyroid | refer, asks the primary's site |  |  | A deposit is coded at the primary site of the tumour. The next screen asks where it began. | ICD-O-3.1 coding rules, PDF p. 2 (printed p. 15) |

### `th_ptc_subtype` (histology_subclassification)

**Which subtype of papillary thyroid carcinoma does the report name?**

Hint: A high-grade papillary carcinoma (tumour necrosis, or 5 or more mitoses per 2 mm2) is coded by its subtype. If the report names more than one subtype, or a subtype with papillary microcarcinoma, choose the one with the higher code (WHO coding Rule K): tall cell and columnar cell 8344, encapsulated 8343, oncocytic 8342, papillary microcarcinoma 8341, infiltrative follicular variant 8340, every other subtype 8260. A report that says papillary and follicular carcinoma is the infiltrative follicular variant (8340).

| Option | Outcome | Records | Basis | Reason | Page |
|---|---|---|---|---|---|
| Classic (usual or conventional) subtype | code | 8260/3 | 7 | Recorded as Papillary adenocarcinoma, NOS (8260/3). ICD-O-3.2 gives Papillary carcinoma of thyroid as a related term of this code. Recognition aid: Reports describe true papillae lined by cells with the nuclear features of papillary carcinoma. | Juhlin 2022, PDF p. 5; ICCR Thyroid 2025, PDF p. 9, table image |
| Infiltrative follicular variant, or follicular variant that is not encapsulated | code | 8340/3 | 7 | Recorded as Papillary carcinoma, follicular variant (8340/3). Recognition aid: Reports describe follicles with papillary carcinoma nuclei growing into the surrounding thyroid. | Juhlin 2022, PDF p. 5; ICCR Thyroid 2025, PDF p. 9, table image |
| Encapsulated follicular variant with capsular or vascular invasion (invasive encapsulated follicular variant) | code | 8343/3 | 7 | Recorded as Papillary carcinoma, encapsulated, of thyroid (8343/3). Recognition aid: Reports describe an encapsulated follicular-patterned tumour with papillary carcinoma nuclei that invades its capsule or vessels. | Juhlin 2022, PDF p. 4; ICCR Thyroid 2025, PDF p. 9, table image |
| Encapsulated subtype, including encapsulated non-invasive papillary carcinoma | code | 8343/3 | 7 | Recorded as Papillary carcinoma, encapsulated, of thyroid (8343/3). Recognition aid: An encapsulated tumour without invasion is called encapsulated non-invasive papillary carcinoma when it has psammoma bodies, true papillae or BRAF p.V600E. | ICCR Thyroid 2025, PDF p. 10 |
| Tall cell subtype | code | 8344/3 | 7 | Recorded as Papillary carcinoma, columnar cell (8344/3). ICD-O-3.2 gives Papillary carcinoma, tall cell as a synonym of this code. Recognition aid: Reports describe pink cells at least three times as tall as they are wide, in a tram-track pattern. | Juhlin 2022, PDF p. 5 |
| Columnar cell subtype | code | 8344/3 | 7 | Recorded as Papillary carcinoma, columnar cell (8344/3). Recognition aid: Reports describe columnar cells with stacked (pseudostratified) nuclei in papillae and gland-like spaces. | Juhlin 2022, PDF p. 5; ICCR Thyroid 2025, PDF p. 9, table image |
| Oncocytic subtype | code | 8342/3 | 7 | Recorded as Papillary carcinoma, oncocytic variant (8342/3). Recognition aid: Reports describe papillary carcinoma in which 75% or more of the cells are oncocytic. | Juhlin 2022, PDF p. 5; ICCR Thyroid 2025, PDF p. 9, table image |
| Diffuse sclerosing subtype | code | 8260/3 (registrar) | 7 | Recorded as Papillary adenocarcinoma, NOS (8260/3). ICD-O-3.2 marks Papillary carcinoma, diffuse sclerosing (8350/3) obsolete. Recognition aid: Reports describe tumour cells in solid nests, sometimes with squamous metaplasia, in dense fibrous tissue with many psammoma bodies and chronic inflammation. | Juhlin 2022, PDF p. 5; ICCR Thyroid 2025, PDF p. 2 |
| Solid, hobnail, Warthin-like, spindle cell or clear cell subtype, or papillary carcinoma with fibromatosis-like stroma | code | 8260/3 | 7 | Recorded as Papillary adenocarcinoma, NOS (8260/3). ICD-O-3.2 holds no separate term for this subtype. | ICCR Thyroid 2025, PDF p. 2 |
| Papillary microcarcinoma, with no subtype named | code | 8341/3 | 7 | Recorded as Papillary microcarcinoma (8341/3). Recognition aid: The report uses papillary microcarcinoma for a papillary carcinoma 10 mm or smaller. | ICCR Thyroid 2025, PDF p. 10 |
| No subtype named | code | 8260/3 | 7 | Recorded as Papillary adenocarcinoma, NOS (8260/3). ICD-O-3.2 gives Papillary carcinoma of thyroid as a related term of this code. | ICCR Thyroid 2025, PDF p. 9, table image |

### `th_ftc_invasion` (histology_subclassification)

**What invasion does the report describe for the follicular carcinoma?**

Hint: Follicular carcinoma is defined by invasion of the capsule or vessels. A tumour with 75% or more oncocytic cells is an oncocytic carcinoma, coded 8290/3 at every invasion extent.

| Option | Outcome | Records | Basis | Reason | Page |
|---|---|---|---|---|---|
| Minimally invasive: capsular invasion only | code | 8335/3 | 7 | Recorded as Follicular carcinoma, minimally invasive (8335/3). | ICCR Thyroid 2025, PDF p. 11 |
| Encapsulated angioinvasive: invasion of a blood vessel | code | 8339/3 (awaiting_layer1) | 7 | Recorded as Follicular carcinoma, encapsulated, angioinvasive (8339/3). | ICCR Thyroid 2025, PDF p. 2 |
| Widely invasive | code | 8330/3 | 7 | Recorded as Follicular carcinoma, NOS (8330/3). Recognition aid: Reports describe extensive invasion of the thyroid or the tissue around it, often with loss of the capsule. | ICCR Thyroid 2025, PDF p. 11; ICCR Thyroid 2025, PDF p. 9, table image |
| Invasive, extent not described | code | 8330/3 | 7 | Recorded as Follicular carcinoma, NOS (8330/3). | ICCR Thyroid 2025, PDF p. 9, table image |
| Encapsulated, with questionable invasion (uncertain malignant potential) | exclude | 8335/1 |  | Not recorded. Follicular tumor of uncertain malignant potential is 8335/1 in ICD-O-3.2, not a malignant tumour. | ICCR Thyroid 2025, PDF p. 10 |
| Encapsulated follicular carcinoma, no invasion described | exclude | 8335/1 (registrar) |  | Not recorded. Follicular tumor of uncertain malignant potential is 8335/1 in ICD-O-3.2, which holds Follicular carcinoma, encapsulated, NOS as a synonym of this code. It is not a malignant tumour. | ICCR Thyroid 2025, PDF p. 11 |

### `th_dhgtc` (histology_subclassification)

**What is the dominant type of the high-grade differentiated thyroid carcinoma?**

Hint: The report names a carcinoma with tumour necrosis or 5 or more mitoses per 2 mm2 that keeps its papillary, follicular or oncocytic pattern. It is coded by that type.

| Option | Outcome | Records | Basis | Reason | Page |
|---|---|---|---|---|---|
| High-grade papillary thyroid carcinoma | go to `th_ptc_subtype` |  |  |  | ICCR Thyroid 2025, PDF p. 2 |
| High-grade follicular thyroid carcinoma | go to `th_ftc_invasion` |  |  |  | ICCR Thyroid 2025, PDF p. 2 |
| High-grade invasive encapsulated follicular variant of papillary thyroid carcinoma | code | 8343/3 | 7 | Recorded as Papillary carcinoma, encapsulated, of thyroid (8343/3). | ICCR Thyroid 2025, PDF p. 2 |
| High-grade oncocytic carcinoma of the thyroid | code | 8290/3 | 7 | Recorded as Oxyphilic adenocarcinoma (8290/3). ICD-O-3.2 gives Oncocytic carcinoma as a synonym of this code. | ICCR Thyroid 2025, PDF p. 2 |
| The report does not name the dominant type | code |  (registrar) | 7 |  | ICCR Thyroid 2025, PDF p. 12 |

### `th_ihc` (ihc_checklist)

**Answer each stain as the report states it.**

Hint: The histology report calls the tumour a carcinoma without naming its type. Answer 'Not done or not readable' for a stain the report does not mention. Thyroglobulin, TTF-1 and PAX8 show that a tumour comes from follicular cells; they do not name its type.

Markers: calcitonin, thyroglobulin, beta-catenin (nuclear), GATA3, mammaglobin, S100 protein, TTF-1. Rules are in section 4. Fallback: 8010/3, Recorded as Carcinoma, NOS (8010/3).

### `th_picker` (morphology_only)

**Which carcinoma does the report name?**

Hint: Type part of the report's term to filter the list. A carcinoma first diagnosed outside the thyroid is coded at its primary site.

| Option | Outcome | Records | Basis | Reason | Page |
|---|---|---|---|---|---|
| Follicular thyroid carcinoma | go to `th_ftc_invasion` |  |  |  Recognition aid: Reports describe a follicular tumour without papillary carcinoma nuclei that invades its capsule or vessels. | ICCR Thyroid 2025, PDF p. 11 |
| Oncocytic carcinoma of the thyroid, or Hurthle cell carcinoma, at any invasion extent | code | 8290/3 | 7 | Recorded as Oxyphilic adenocarcinoma (8290/3). ICD-O-3.2 gives Oncocytic carcinoma as a synonym of this code. Recognition aid: Reports describe an invasive tumour in which 75% or more of the cells are oncocytes, without papillary carcinoma nuclei. | ICCR Thyroid 2025, PDF p. 9, table image; ICCR Thyroid 2025, PDF p. 11 |
| High-grade differentiated thyroid carcinoma | go to `th_dhgtc` |  |  |  | Juhlin 2022, PDF p. 5 |
| Anaplastic (undifferentiated) thyroid carcinoma | code | 8020/3 | 7 | Recorded as Carcinoma, undifferentiated, NOS (8020/3). ICD-O-3.2 gives Anaplastic undifferentiated carcinoma as a related term of this code. Recognition aid: Reports describe a high-grade spindled, pleomorphic or squamoid carcinoma; a papillary or follicular component may be present. | ICCR Thyroid 2025, PDF p. 9, table image; ICCR Thyroid 2025, PDF p. 12 |
| Mixed medullary-follicular carcinoma | code | 8346/3 | 7 | Recorded as Mixed medullary-follicular carcinoma (8346/3). | ICCR Thyroid 2025, PDF p. 9, table image |
| Mixed medullary-papillary carcinoma | code | 8347/3 | 7 | Recorded as Mixed medullary-papillary carcinoma (8347/3). | ICCR Thyroid 2025, PDF p. 9, table image |
| Cribriform-morular thyroid carcinoma, or the cribriform-morular variant of papillary carcinoma | code | 8201/3 | 7 | Recorded as Cribriform carcinoma, NOS (8201/3). Recognition aid: Reports describe cribriform and morular growth with nuclear and cytoplasmic beta-catenin staining. | ICCR Thyroid 2025, PDF p. 9, table image; Juhlin 2022, PDF p. 7 |
| Mucoepidermoid carcinoma, including sclerosing mucoepidermoid carcinoma with eosinophilia | code | 8430/3 | 7 | Recorded as Mucoepidermoid carcinoma (8430/3). Recognition aid: Reports describe mucinous, intermediate and squamous cells in solid and cystic growth. | ICCR Thyroid 2025, PDF p. 9, table image; Juhlin 2022, PDF p. 7 |
| Secretory carcinoma | code | 8502/3 | 7 | Recorded as Secretory carcinoma (8502/3). Recognition aid: Reports describe pink cells with vacuolated cytoplasm that stain for GATA3, mammaglobin and S100 protein, often with an ETV6::NTRK3 fusion. | ICCR Thyroid 2025, PDF p. 9, table image; Juhlin 2022, PDF p. 7 |
| Intrathyroid thymic carcinoma, or carcinoma showing thymus-like differentiation | code | 8589/3 | 7 | Recorded as Intrathyroid thymic carcinoma (8589/3). | ICCR Thyroid 2025, PDF p. 3 |
| Thymoma within the thyroid | code | 8580/3 (registrar) | 7 | Recorded as Thymoma, NOS (8580/3). | ICCR Thyroid 2025, PDF p. 3 |
| Thymic carcinoma within the thyroid | code | 8586/3 (registrar) | 7 | Recorded as Thymic carcinoma, NOS (8586/3). | Juhlin 2022, PDF p. 7 |
| Squamous cell carcinoma of the thyroid | code | 8070/3 (registrar) | 7 | Recorded as Squamous cell carcinoma, NOS (8070/3). | Juhlin 2022, PDF p. 6 |

The picker also lists, one option each under its ICD-O-3.2 preferred term at basis 7, the 58 other current /3 codes ICCC-2017 places in XIb at C73.9, plus thymoma types 8581–8585:

8011 Epithelioma, malignant, 8012 Large cell carcinoma, NOS, 8013 Large cell neuroendocrine carcinoma, 8014 Large cell carcinoma with rhabdoid phenotype, 8015 Glassy cell carcinoma, 8022 Pleomorphic carcinoma, 8023 Nuclear protein in testis (NUT)-associated carcinoma, 8030 Giant cell and spindle cell carcinoma, 8031 Giant cell carcinoma, 8032 Spindle cell carcinoma, NOS, 8033 Pseudosarcomatous carcinoma, 8034 Polygonal cell carcinoma, 8035 Carcinoma with osteoclast-like giant cells, 8041 Small cell carcinoma, NOS, 8051 Verrucous carcinoma, NOS, 8052 Papillary squamous cell carcinoma, 8054 Warty carcinoma, 8071 Squamous cell carcinoma, keratinizing, NOS, 8072 Squamous cell carcinoma, large cell, nonkeratinizing, NOS, 8073 Squamous cell carcinoma, small cell, nonkeratinizing, 8074 Squamous cell carcinoma, spindle cell, 8075 Squamous cell carcinoma, adenoid, 8082 Lymphoepithelial carcinoma, 8120 Transitional cell carcinoma, NOS, 8121 Schneiderian carcinoma, 8122 Urothelial carcinoma, sarcomatoid, 8131 Urothelial carcinoma, micropapillary, 8140 Adenocarcinoma, NOS, 8158 ACTH-producing tumor, 8190 Trabecular adenocarcinoma, 8200 Adenoid cystic carcinoma, 8211 Tubular adenocarcinoma, 8230 Solid carcinoma, NOS, 8231 Carcinoma simplex, 8244 Mixed adenoneuroendocrine carcinoma, 8246 Neuroendocrine carcinoma, NOS, 8261 Adenocarcinoma in villous adenoma, 8262 Villous adenocarcinoma, 8263 Adenocarcinoma in tubulovillous adenoma, 8310 Clear cell adenocarcinoma, NOS, 8320 Granular cell carcinoma, 8323 Mixed cell adenocarcinoma, 8331 Follicular adenocarcinoma, well differentiated, 8332 Follicular adenocarcinoma, trabecular, 8333 Fetal adenocarcinoma, 8480 Mucinous adenocarcinoma, 8481 Mucin-producing adenocarcinoma, 8560 Adenosquamous carcinoma, 8562 Epithelial-myoepithelial carcinoma, 8570 Adenocarcinoma with squamous metaplasia, 8571 Adenocarcinoma with cartilaginous and osseous metaplasia, 8572 Adenocarcinoma with spindle cell metaplasia, 8573 Adenocarcinoma with apocrine metaplasia, 8581 Thymoma, type A, 8582 Thymoma, type AB, 8583 Thymoma, type B1, 8584 Thymoma, type B2, 8585 Thymoma, type B3.

Held back from the thyroid picker, because the thyroid has its own code for the same tumour:

- 8050/3: Papillary carcinoma in the thyroid is 8260/3 (ICD-O-3.2 related term Papillary carcinoma of thyroid, C73.9); 8050/3 in the thyroid picker invites the wrong code.
- 8510/3: Medullary carcinoma in the thyroid is 8345/3 Medullary thyroid carcinoma (C73.9); 8510/3 in the thyroid picker invites the wrong code.
- 8021/3: The WHO source codes anaplastic thyroid carcinoma 8020/3 (ICCR Table 1); 8021/3 in the thyroid picker invites a second code for one entity.

Never on a screen (every /3 term obsolete in ICD-O-3.2): 8130 Papillary urothelial carcinoma, 8141 Scirrhous adenocarcinoma, 8245 Adenocarcinoid tumor, 8350 Nonencapsulated sclerosing carcinoma, 8440 Cystadenocarcinoma, NOS.

The tree opens on `th_evidence`. A histology report leads to `th_histology`, whose options are the four paediatric entities (papillary carcinoma through its subtype screen, poorly differentiated carcinoma, medullary carcinoma, the spindle epithelial tumour with thymus-like elements), two routes for a carcinoma the report does not type, the picker, the exclusions, and the referrals. Follicular carcinoma reaches its invasion screen `th_ftc_invasion` from the picker; the currency check's separation of 8335/3, 8339/3 and 8335/1 holds there. High-grade differentiated carcinoma reaches `th_dhgtc` from the picker and is coded by its dominant type (ICCR Thyroid 2025, PDF p. 12).

## 4 Immunohistochemistry rules

Panel `th_ihc`, first match wins. It is reached only from a histology report that names a carcinoma but not its type.

| Positive | Negative | Records | Page |
|---|---|---|---|
| calcitonin | thyroglobulin | 8345/3 — Recorded as Medullary thyroid carcinoma (8345/3). | ICCR Thyroid 2025, PDF p. 19; Juhlin 2022, PDF p. 7 |
| beta-catenin (nuclear) | thyroglobulin | 8201/3 — Recorded as Cribriform carcinoma, NOS (8201/3). | Juhlin 2022, PDF p. 7 |
| GATA3, mammaglobin, S100 protein | TTF-1, thyroglobulin | 8502/3 — Recorded as Secretory carcinoma (8502/3). | Juhlin 2022, PDF p. 7 |
| (fallback) |  | 8010/3 — Recorded as Carcinoma, NOS (8010/3). Thyroglobulin, TTF-1 and PAX8 show follicular-cell origin without naming the type. | ICCR Thyroid 2025, PDF p. 19 |

Thyroglobulin, TTF-1 and PAX8 show follicular-cell origin and name no type (ICCR Thyroid 2025, PDF p. 19), so a panel that shows only those markers falls to 8010/3. Mucoepidermoid carcinoma has no rule: Juhlin 2022 (PDF p. 7) gives p63 and CK5 as confirming stains but no marker that separates it from other carcinomas with squamous cells, so a rule on them would overstate the evidence.

## 5 Registration without tissue

| Evidence on file | Records | Basis |
|---|---|---|
| A referral letter or clinical note only | 8000/3 | 1 |
| An imaging report only | 8000/3 | 2 |
| Imaging that shows a thyroid tumour with a raised serum calcitonin | 8345/3 | 4 |
| A raised calcitonin with no imaging that shows a tumour | not registrable |  |
| A report that calls a thyroid malignancy possible or suspected | not registrable |  |

Source: Visser 2023, Table 4 and rules 4 to 6, from the task brief and the build contract §0.5. Medullary thyroid carcinoma is the one thyroid entity Table 4 allows at basis 4. At C73.9 ICCC-2017 places 8000/3 in XIIb, so a thyroid case registered on clinical or imaging evidence computes to Group XII (section 9).

## 6 Laboratory tests

- **Calcitonin, serum.** With imaging that shows a thyroid tumour, a raised serum calcitonin registers medullary thyroid carcinoma 8345/3 at basis 4. The thyroid sources name calcitonin and carcinoembryonic antigen only as immunostains on tissue; none gives a serum test a diagnostic role.

No other serum or urine test has a diagnostic role in this part's sources.

## 7 Rules A to K

| Rule | Applies | How it reaches the clerk | Page |
|---|---|---|---|
| A | no | The thyroid is a named organ, not an ill-defined region. A neck mass that histology calls a thyroid carcinoma is placed by Rule H. | ICD-O-3.1 coding rules, PDF p. 1 (printed p. 14) |
| B | yes | Hint on th_evidence: a thyroid carcinoma reported in the perithyroid tissue is recorded at the thyroid, because the tumour type shows its tissue. | ICD-O-3.1 coding rules, PDF p. 1 (printed p. 14) |
| C | no | C73 has one subcategory, C73.9; no .8 overlap code exists for the thyroid. | ICD-O-3.1 coding rules, PDF p. 2 (printed p. 15) |
| D | yes | Reason on the Lymphoma referral on th_histology: a thyroid lymphoma is extranodal and keeps C73.9. | ICD-O-3.1 coding rules, PDF p. 2 (printed p. 15) |
| E | no | No leukaemia is offered at the thyroid. | ICD-O-3.1 coding rules, PDF p. 2 (printed p. 15) |
| F | yes | The exclusion options on th_histology and th_ftc_invasion give the ICD-O-3.2 behaviour in their reason. A report that itself calls one of those tumours malignant is registrar question 9; no screen offers a stated-behaviour code. | ICD-O-3.1 coding rules, PDF p. 2 (printed p. 15) |
| G | yes | Hint on th_histology: a well-differentiated carcinoma with a poorly differentiated or anaplastic component is coded as the higher-grade tumour. Grade words are part of the entity name in poorly differentiated thyroid carcinoma (8337) and Follicular adenocarcinoma, well differentiated (8331); the sixth digit is not built. | ICD-O-3.1 coding rules, PDF p. 2 (printed p. 15); ICD-O-3.1 coding rules, PDF p. 9 (printed p. 22) |
| H | yes | Hint on th_evidence: a lymph node or perithyroid specimen showing a thyroid carcinoma is recorded at C73.9, the site ICD-O-3.2 prints beside 8260/3 Papillary carcinoma of thyroid, 8330, 8335, 8337, 8339, 8340, 8341, 8343, 8345 and 8589. The deposit option on th_histology refers a tumour that began elsewhere. | ICD-O-3.1 coding rules, PDF p. 2 (printed p. 15) |
| J | yes | Hint on th_ptc_subtype: a report that says papillary and follicular carcinoma is the listed combination 8340/3. | ICD-O-3.1 coding rules, PDF p. 3 (printed p. 16); ICD-O-3.1 coding rules, PDF p. 11 (printed p. 24) |
| K | yes | Hint on th_ptc_subtype lists the subtype codes so the clerk records the higher one when the report names two subtypes. Where Rule K and the WHO entity disagree (clear cell, squamous, mixed medullary and oncocytic, anaplastic with a differentiated component) the screens follow the WHO entity pending registrar question 4. | ICD-O-3.1 coding rules, PDF p. 3 (printed p. 16) |

There is no Rule I.

## 8 Code currency

| Code | Finding | What the tree does |
|---|---|---|
| 8335/3 | Currency check section 3: 8335 moved /3 to /1; Follicular carcinoma, minimally invasive stays 8335/3, and Follicular carcinoma, encapsulated, NOS is now a synonym at 8335/1. | th_ftc_invasion codes capsular invasion only 8335/3 and sends questionable or undescribed invasion in an encapsulated tumour to the 8335/1 exclusion. |
| 8339/3 | Currency check sections 3 and 6: new in ICD-O-3.2, outside every ICCC-2017 range, not in REDCap. | Built on th_ftc_invasion with awaiting_layer1; listed in codes-awaiting-redcap.md and on the REDCap-side list. |
| 8336/1 | Currency check section 3: /0 to /1, now Hyalinizing trabecular tumor; section 5: REDCap XIb offers 8336 as Hyalinizing trabecular adenoma, with no malignant form. | Exclusion on th_histology; REDCap-side list. |
| 8350/3 | Currency check section 2: every /3 term [obs], including Papillary carcinoma, diffuse sclerosing. REDCap XIb offers 8350 Nonencapsulated sclerosing carcinoma. | Not built. The diffuse sclerosing subtype option on th_ptc_subtype records 8260/3 (registrar question 3). REDCap-side list: retire 8350. |
| 8330/3 | Currency check section 4: REDCap label Follicular adenocarcinoma, NOS is a synonym; preferred is Follicular carcinoma, NOS. | The tool shows the preferred term; REDCap-side list. |
| 8337/3 | Currency check section 4: REDCap label Insular carcinoma is a synonym; preferred is Poorly differentiated thyroid carcinoma. | The tool shows the preferred term; REDCap-side list. |
| 8342/3 | Currency check section 4: REDCap label Papillary carcinoma, oxyphilic cell is a synonym; preferred is Papillary carcinoma, oncocytic variant. | The tool shows the preferred term; REDCap-side list. |
| 8343/3 | Currency check section 4: REDCap label Papillary carcinoma, encapsulated is not an ICD-O-3.2 term; preferred is Papillary carcinoma, encapsulated, of thyroid. | The tool shows the preferred term; REDCap-side list. |
| 8345/3 | Currency check section 4: REDCap label Medullary carcinoma with amyloid stroma is a related term; preferred is Medullary thyroid carcinoma. The synonym Parafollicular cell carcinoma is [obs]. | The tool shows the preferred term; REDCap-side list. |
| 8589/3 | Currency check section 4: REDCap label Carcinoma showing thymus-like element is a synonym; preferred is Intrathyroid thymic carcinoma. | The tool shows the preferred term; REDCap-side list. |
| 8344/3 | ICD-O-3.2 holds tall cell as a synonym at 8344/3; REDCap offers only the preferred Papillary carcinoma, columnar cell. | Tall cell and columnar cell both record 8344/3 under the preferred term. |
| 8502/3 | REDCap's XIb list does not offer 8502, and its XIc and XIf label Secretory carcinoma of breast is not the ICD-O-3.2 preferred term Secretory carcinoma (currency check section 4). ICCC-2017 places 8502 in no group at C73.9. | Picker entry at C73.9, XIb by standing rule 3; REDCap-side list. |
| 8580/3 | Currency check section 3: thymoma types 8580-8585 moved /1 to /3. ICCC-2017 places 8580-8586 in no group at C73.9; REDCap's XIb list does not offer them. | Picker entries, pending registrar question 7 on topography. |
| 8020/3 | ICCR Table 1 codes anaplastic thyroid carcinoma 8020/3. ICD-O-3.2 also holds 8021/3 Carcinoma, anaplastic, NOS as current. | Anaplastic thyroid carcinoma records 8020/3; 8021/3 is held back from the thyroid picker. |
| 8050/3 | Papillary carcinoma, NOS is 8050/3, but ICD-O-3.2 prints Papillary carcinoma of thyroid (C73.9) as a related term of 8260/3. | Every papillary carcinoma at the thyroid records 8260/3; 8050/3 is held back from the thyroid picker. |
| 8510/3 | Medullary carcinoma, NOS is 8510/3; ICD-O-3.2 prints Medullary thyroid carcinoma (C73.9) at 8345/3. | Every medullary carcinoma at the thyroid records 8345/3; 8510/3 is held back from the thyroid picker. |
| 8330/1 | Atypical follicular adenoma, the only 8330/1 term, is [obs]. | Never on a screen. Not in Group XI scope (behaviour /1). |
| 9080/1 | Currency check section 3: Immature teratoma of thyroid moved /3 to /1; a Group X code at a Group XI site. | The Teratoma option on th_histology refers to Group X, which holds the exclusion. |

## 9 Conflicts with other groups

- **Group 10** (9080; C73.9): Teratoma of the thyroid is Group X: ICCC-2017 puts malignant teratoma 9080 at C73.9 in Xb2, and ICD-O-3.2 codes immature teratoma of thyroid 9080/1. The thyroid tree refers it.
- **Group 10** (9080; C73.9): ICCR lists thyroblastoma as an embryonal thyroid neoplasm, and ICD-O-3.2 gives it no code. A clerk without a code may reach for Teratoma, malignant, NOS 9080/3, which ICCC-2017 places at C73.9 in Group X (Xb2). Registrar question 6.
- **Group 10** (8330, 8335, 8337, 8340, 8341, 8343, 8344, 8260, 9090; C56.9): ICCC-2017 range 121 places 8330-8347 in XIb at every site, so a thyroid-type carcinoma in struma ovarii coded 8330 or 8340 is XIb, while 8260 at the ovary is Xd and 9090/3 Struma ovarii, malignant is Xc2. None of this part's sources covers struma ovarii; the ovary tree must choose one route.
- **Group 12** (8000; C73.9): The evidence gate records 8000/3 on clinical or imaging evidence, and ICCC-2017 places 8000 at C73.9 in XIIb, not XIb. The subgroup computed at output will be XIIb for those cases.
- **Group 2** (no code; C73.9): Thyroid lymphoma refers to Group II and keeps C73.9 (Rule D).
- **Group 9** (8800, 9120; C73.9): Sarcoma of the thyroid refers to Group IX (8800 IXe, 9120 IXd8 at C73.9).
- **Group 11** (8580, 8581, 8582, 8583, 8584, 8585, 8586, 8589; C73.9, C37.9): Thymus tree overlap (XIf): 8589 is XIb at C73.9 but XIf elsewhere; thymoma and thymic carcinoma within the thyroid have no ICCC group at C73.9. Whether an intrathyroid thymoma is recorded at C73.9 or C37.9 is registrar question 7.
- **Group 11** (8430, 8502; C73.9, C07.9, C08.9): Salivary gland tree overlap: mucoepidermoid and secretory carcinoma use the salivary codes; at C73.9 8430 is XIb and 8502 has no ICCC group.

## 10 Data gaps

1. **Paediatric occurrence of follicular thyroid carcinoma, oncocytic carcinoma, the invasive encapsulated follicular variant, anaplastic carcinoma, cribriform-morular carcinoma and the rarer thyroid entities.** Ruling 1 makes an entity a histology-screen option only on a paediatric report. Pfister 2022 Table 3 lists papillary and medullary carcinoma and the spindle epithelial tumour with thymus-like elements; Juhlin reports poorly differentiated carcinoma in adolescents. Follicular carcinoma therefore sits in the picker until a source reports it in children. Candidate source: WHO Classification of Paediatric Tumours, 5th edition, thyroid chapter; Francis GL, et al. Management guidelines for children with thyroid nodules and differentiated thyroid cancer. Thyroid 2015;25:716-759.
2. **The ICD-O codes the WHO 5th edition gives to differentiated high-grade thyroid carcinoma (dominant type not named) and to thyroblastoma.** Neither code is in ICD-O-3.2 or ICCR Table 1; both entities wait on the registrar. Candidate source: Baloch ZW, et al. Overview of the 2022 WHO Classification of Thyroid Neoplasms. Endocrine Pathology 2022;33:27-63, which tabulates ICD-O codes.
3. **A source for serum calcitonin as a registration marker.** The th_lab screen and the basis-4 tissue-free code rest on Visser 2023 Table 4, which is not in this part's file set. Candidate source: Visser O, et al. Front Oncol 2023;13:1250549 (the controller holds docs/references/visser-2023-key-points.md).
4. **Thyroid cytology reporting categories and which of them a registry may record.** th_cytology uses generic labels; none of the sources covers fine-needle aspiration categories. Candidate source: Ali SZ, et al. The 2023 Bethesda System for Reporting Thyroid Cytopathology. Thyroid 2023;33:1039-1044.
5. **Immunohistochemistry that separates intrathyroid thymic carcinoma and the spindle epithelial tumour with thymus-like elements from other thyroid carcinomas.** The th_ihc panel has no rule for either; both fall to the 8010/3 fallback if the report does not name them. Candidate source: WHO Classification of Endocrine and Neuroendocrine Tumours, 5th edition, thyroid chapters.
6. **Coding of thyroid-type carcinoma arising in struma ovarii.** Three routes give three groups (XIb, Xd, Xc2); see conflicts. Candidate source: WHO Classification of Female Genital Tumours, 5th edition, monodermal teratoma chapter.

### Questions only the registrar can answer

1. My sources report papillary and medullary thyroid carcinoma, the spindle epithelial tumour with thymus-like elements, and poorly differentiated carcinoma in adolescents, but not follicular thyroid carcinoma. Should follicular carcinoma (and its invasion screen) be a histology-screen option now, or stay in the picker until a paediatric source is found?
2. A report that says encapsulated follicular carcinoma and describes no capsular or vascular invasion: ICD-O-3.2 codes Follicular carcinoma, encapsulated, NOS 8335/1, outside the malignant scope. Confirm the tree excludes it.
3. The diffuse sclerosing subtype of papillary carcinoma: every 8350/3 term is obsolete and the WHO table gives the subtype no code of its own. Confirm it records 8260/3.
4. Where Rule K and the WHO entity give different codes, which wins? Clear cell papillary carcinoma (Rule K 8310/3, WHO subtype 8260/3); squamous cell carcinoma of the thyroid (term 8070/3, WHO entity anaplastic 8020/3); anaplastic carcinoma with a papillary or follicular component (Rule K 8260/3 or 8330/3, WHO 8020/3); mixed medullary and oncocytic carcinoma (Rule K 8345/3, family code 8346/3). The screens follow the WHO entity until you rule.
5. Papillary microcarcinoma with a named subtype: Rule K keeps 8341/3 over classic 8260/3 and gives 8344/3 for tall cell. Confirm, given that the WHO 5th edition asks pathologists to subtype small tumours and not to use the size term.
6. Thyroblastoma and a high-grade differentiated thyroid carcinoma whose dominant type is not named have no ICD-O-3.2 code in the sources. What should each record?
7. Thymoma or thymic carcinoma found within the thyroid: is the site C73.9 or C37.9? At C73.9 ICCC-2017 gives 8580-8586 no group.
8. Oncocytic carcinoma reported as minimally invasive or encapsulated angioinvasive: confirm it records 8290/3, not 8335/3 or 8339/3 (the invasion words carry no code of their own).
9. Rule F: a report that itself calls a hyalinizing trabecular tumour or another /1 thyroid tumour malignant. Is it recorded (for example 8336/3, which ICCC-2017 range 121 would place in XIb), or excluded?
