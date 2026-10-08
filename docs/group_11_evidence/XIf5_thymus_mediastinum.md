# Group 11 evidence — XIf5 thymus, plus mediastinum (XIf10)

Part `XIf5_thymus_mediastinum`. Sites: C37.9 thymus (XIf5); C38.1 anterior mediastinum, C38.2 posterior mediastinum, C38.3 mediastinum NOS and C38.8 overlapping lesion of heart, mediastinum and pleura (XIf10). Evidence only: this file writes no tool JSON. The machine-readable twin is `XIf5_thymus_mediastinum.json`; every quote in it was checked against its PDF page by `check_g11_evidence.py` (180 quotes found on the cited page).

## 1 Sources

| File | Citation | WHO volume |
|---|---|---|
| `XIf5-thymus-and-mediastinum__Marx-2022.txt` | Marx A, Chan JKC, Chalabreysse L, Dacic S, Detterbeck F, French CA, Hornick JL, Inagaki H, Jain D, et al. The 2021 WHO Classification of Tumors of the Thymus and Mediastinum: What Is New in Thymic Epithelial, Germ Cell, and Mesenchymal Tumors? J Thorac Oncol 2022;17(2):200-213 | WHO Classification of Tumours, Thoracic Tumours, 5th edition, volume 5, 2021 |
| `XIf5-thymus__ICCR-Thymic-Epithelial-3rd.txt` | International Collaboration on Cancer Reporting. Thymic Epithelial Tumours Histopathology Reporting Guide, 3rd edition, version 3.0. Sydney: ICCR; May 2022. ISBN 978-1-922324-32-0 | WHO Classification of Thoracic Tumours, 5th edition, 2021 |
| `ALL-paediatric-occurrence__Pfister-2022.txt` | Pfister SM, Reyes-Mugica M, Chan JKC, et al. A Summary of the Inaugural WHO Classification of Pediatric Tumors: Transitioning from the Optical into the Molecular Era. Cancer Discov 2022;12(2):331-355 | WHO Classification of Paediatric Tumours, 5th edition, 2022 |
| `RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt` | World Health Organization. International Classification of Diseases for Oncology, 3rd edition, 1st revision (ICD-O-3.1), section 4, Coding guidelines, printed pp. 14-28 | not a tumour classification; the ICD-O coding manual |
| `XIf5-thymus-paediatric__Rossi-2022.txt` | Rossi C, et al. Pediatric Thymoma: A Review and Update of the Literature. Diagnostics (Basel) 2022;12(9):2205. doi:10.3390/diagnostics12092205 | not a WHO summary; paediatric evidence |

Tables were read from the PDF page images: ICCR Thymic 2022 Table 1 (PDF pp. 9-10) and Table 2 (PDF p. 11); Marx 2022 Table 1 (PDF p. 4), Table 2 (PDF p. 9) and Table 3 (PDF p. 11); Pfister 2022 Table 3 (PDF p. 14). Each table's text layer matched the image, so the quotes cite the text layer.

Rossi 2022 is a PubMed Central text (PMC9497562, added 8 October 2026). It has sections, not pages: its cites give the PMC section number in the `pdf_page` field, and this file writes "PMC section N". The review covers 82 thymomas in 32 articles from 1985 to 2020, in patients under the age of eighteen (aged 0.9 to 17 years). It excluded thymic carcinoma, thymic neuroendocrine tumours and combined thymic carcinomas (PMC section 3).

## 2 Entities

Paediatric evidence decides option or picker (ruling 1). Pfister 2022 Table 3 lists no thymic tumour among the thoracic tumours of children (PDF p. 14), and neither Marx 2022 nor the ICCR guide gives an age. NUT carcinoma has a paediatric report (Pfister 2022, head and neck section). Rossi 2022 reports thymoma types A, AB, B1, B2 and B3 and thymoma with no WHO type in patients aged 0.9 to 17 years, and names type B1 the most frequent (PMC section 4); these six are options. Rossi 2022 excluded thymic carcinoma and thymic neuroendocrine tumours, so every thymic carcinoma, thymic neuroendocrine entity and metaplastic thymoma stays a picker entry (data gap 1).

| Entity (WHO) | Code | ICD-O-3.2 term matched (level) | ICD-O-3.2 preferred term | Paediatric | Decision | Pages |
|---|---|---|---|---|---|---|
| NUT carcinoma | 8023/3 | NUT carcinoma (Synonym) | Nuclear protein in testis (NUT)-associated carcinoma | occurs | option | Pfister 2022, PDF p. 14; Marx 2022, PDF p. 4; ICCR Thymic 2022, PDF p. 10; ICCR Thymic 2022, PDF p. 15 |
| Carcinoma, with no type named | 8010/3 | Carcinoma, NOS (Preferred) | Carcinoma, NOS | not_reported | option | ICD-O-3.1 manual, PDF p. 8 (printed p. 21) |
| Thymoma, type A, including atypical variant | 8581/3 | Thymoma, type A (Preferred) | Thymoma, type A | occurs | option | ICCR Thymic 2022, PDF p. 9; Marx 2022, PDF p. 4; Pfister 2022, PDF p. 14; Rossi 2022, PMC section 4 |
| Thymoma, type AB | 8582/3 | Thymoma, type AB (Preferred) | Thymoma, type AB | occurs | option | ICCR Thymic 2022, PDF p. 9; Pfister 2022, PDF p. 14; Rossi 2022, PMC section 4 |
| Thymoma, type B1 | 8583/3 | Thymoma, type B1 (Preferred) | Thymoma, type B1 | common | option | ICCR Thymic 2022, PDF p. 9; Pfister 2022, PDF p. 14; Rossi 2022, PMC section 4 |
| Thymoma, type B2 | 8584/3 | Thymoma, type B2 (Preferred) | Thymoma, type B2 | occurs | option | ICCR Thymic 2022, PDF p. 9; Pfister 2022, PDF p. 14; Rossi 2022, PMC section 4 |
| Thymoma, type B3 | 8585/3 | Thymoma, type B3 (Preferred) | Thymoma, type B3 | occurs | option | ICCR Thymic 2022, PDF p. 9; Pfister 2022, PDF p. 14; Rossi 2022, PMC section 4 |
| Metaplastic thymoma | 8580/3 | Metaplastic thymoma (Related) | Thymoma, NOS | not_reported | picker | ICCR Thymic 2022, PDF p. 9; Marx 2022, PDF p. 3; Pfister 2022, PDF p. 14 |
| Thymoma, NOS (including a report that still says sclerosing thymoma) | 8580/3 | Thymoma, NOS (Preferred) | Thymoma, NOS | occurs | option | ICCR Thymic 2022, PDF p. 9; Marx 2022, PDF p. 3; Pfister 2022, PDF p. 14; Rossi 2022, PMC sections 1, 3 and 4 |
| Squamous cell carcinoma, including subtype micronodular carcinoma with lymphoid hyperplasia | 8070/3 | Squamous cell carcinoma, NOS (Preferred) | Squamous cell carcinoma, NOS | not_reported | picker | ICCR Thymic 2022, PDF p. 10; Marx 2022, PDF p. 6; Marx 2022, PDF p. 7 |
| Basaloid carcinoma | 8123/3 | Basaloid carcinoma (Preferred) | Basaloid carcinoma | not_reported | picker | ICCR Thymic 2022, PDF p. 10 |
| Lymphoepithelial carcinoma (previously lymphoepithelioma-like carcinoma) | 8082/3 | Lymphoepithelial carcinoma (Preferred) | Lymphoepithelial carcinoma | not_reported | picker | Marx 2022, PDF p. 4; Marx 2022, PDF p. 6 |
| Adenocarcinoma, NOS | 8140/3 | Adenocarcinoma, NOS (Preferred) | Adenocarcinoma, NOS | not_reported | picker | ICCR Thymic 2022, PDF p. 10; Marx 2022, PDF p. 6 |
| Low-grade papillary adenocarcinoma (previously papillary adenocarcinoma) | 8260/3 | Papillary adenocarcinoma, NOS (Preferred) | Papillary adenocarcinoma, NOS | not_reported | picker | Marx 2022, PDF p. 4; Marx 2022, PDF p. 6 |
| Thymic carcinoma with adenoid cystic carcinoma-like features | 8200/3 | Thymic carcinoma with adenoid cystic carcinoma-like features (Related) | Adenoid cystic carcinoma | not_reported | picker | ICCR Thymic 2022, PDF p. 10 |
| Adenocarcinoma, enteric type | 8144/3 | Adenocarcinoma, enteric (Synonym) | Adenocarcinoma, intestinal type | not_reported | picker | ICCR Thymic 2022, PDF p. 10; Marx 2022, PDF p. 4; Marx 2022, PDF p. 7 |
| Adenosquamous carcinoma | 8560/3 | Adenosquamous carcinoma (Preferred) | Adenosquamous carcinoma | not_reported | picker | Marx 2022, PDF p. 4 |
| Mucoepidermoid carcinoma | 8430/3 | Mucoepidermoid carcinoma (Preferred) | Mucoepidermoid carcinoma | not_reported | picker | ICCR Thymic 2022, PDF p. 10; ICCR Thymic 2022, PDF p. 16 |
| Clear cell carcinoma, including subtype hyalinizing clear cell carcinoma | 8310/3 | Clear cell carcinoma, NOS (Synonym) | Clear cell adenocarcinoma, NOS | not_reported | picker | ICCR Thymic 2022, PDF p. 10; Marx 2022, PDF p. 6 |
| Sarcomatoid carcinoma | 8033/3 | Sarcomatoid carcinoma (Synonym) | Pseudosarcomatous carcinoma | not_reported | picker | Marx 2022, PDF p. 4 |
| Carcinoma, undifferentiated, NOS | 8020/3 | Carcinoma, undifferentiated, NOS (Preferred) | Carcinoma, undifferentiated, NOS | not_reported | picker | ICCR Thymic 2022, PDF p. 10 |
| Thymic carcinoma, NOS | 8586/3 | Thymic carcinoma, NOS (Preferred) | Thymic carcinoma, NOS | not_reported | picker | Marx 2022, PDF p. 4; ICCR Thymic 2022, PDF p. 10 |
| Hepatoid carcinoma, rhabdoid carcinoma, sebaceous carcinoma and undifferentiated large cell carcinoma associated with Castleman disease-like reaction, of the thymus | 8586/3 | Thymic carcinoma, NOS (Preferred) | Thymic carcinoma, NOS | not_reported | picker | Marx 2022, PDF p. 4; Marx 2022, PDF p. 6 |
| Typical carcinoid / neuroendocrine tumour, grade 1 (and carcinoid tumour, NOS) | 8240/3 | Typical carcinoid (Synonym) | Neuroendocrine tumor, NOS | not_reported | picker | ICCR Thymic 2022, PDF p. 10; Marx 2022, PDF p. 8 |
| Atypical carcinoid / neuroendocrine tumour, grade 2 | 8249/3 | Atypical carcinoid tumor (Synonym) | Neuroendocrine tumor, grade 2 | not_reported | picker | ICCR Thymic 2022, PDF p. 10 |
| Neuroendocrine tumour with carcinoid morphology and elevated mitotic count or Ki-67 index ('NET G3') | 8249/3 | Neuroendocrine tumor, grade 3 (Related) | Neuroendocrine tumor, grade 2 | not_reported | picker | Marx 2022, PDF p. 8; Marx 2022, PDF p. 9; ICD-O-3.1 manual, PDF p. 8 (printed p. 21) |
| Small cell carcinoma | 8041/3 | Small cell carcinoma, NOS (Preferred) | Small cell carcinoma, NOS | not_reported | picker | ICCR Thymic 2022, PDF p. 10; Marx 2022, PDF p. 6 |
| Combined small cell carcinoma | 8045/3 | Combined small cell carcinoma (Preferred) | Combined small cell carcinoma | not_reported | picker | ICCR Thymic 2022, PDF p. 10; ICCR Thymic 2022, PDF p. 9 |
| Large cell neuroendocrine carcinoma (including combined large cell neuroendocrine carcinoma) | 8013/3 | Large cell neuroendocrine carcinoma (Preferred) | Large cell neuroendocrine carcinoma | not_reported | picker | ICCR Thymic 2022, PDF p. 10; ICCR Thymic 2022, PDF p. 9 |
| Micronodular thymoma with lymphoid stroma | 8580/1 | Micronodular thymoma with lymphoid stroma (Preferred) | Micronodular thymoma with lymphoid stroma | not_reported | exclusion | ICCR Thymic 2022, PDF p. 9; Marx 2022, PDF p. 3 |
| Microscopic thymoma (now nodular epithelial hyperplasia); thymoma the report calls benign | 8580/0 | Microscopic thymoma (Preferred) | Microscopic thymoma | not_reported | exclusion | Marx 2022, PDF p. 3; ICCR Thymic 2022, PDF p. 14; ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |
| Lipofibroadenoma | 9010/0 | Lipofibroadenoma (Related) | Fibroadenoma, NOS | not_reported | exclusion | ICCR Thymic 2022, PDF p. 9; Marx 2022, PDF p. 4 |
| Thymolipoma | 8850/0 | Thymolipoma (Related) | Lipoma, NOS | not_reported | exclusion | Marx 2022, PDF p. 10; Marx 2022, PDF p. 11 |
| Thoracic SMARCA4-deficient undifferentiated tumour | none | none | none | not_reported | registrar | Marx 2022, PDF p. 10 |
| Seminoma | 9061/3 | Seminoma, NOS (Preferred) | Seminoma, NOS | occurs | refer to Group 10 | Marx 2022, PDF p. 9 |
| Yolk sac tumour | 9071/3 | Yolk sac tumor, NOS (Preferred) | Yolk sac tumor, NOS | occurs | refer to Group 10 | Marx 2022, PDF p. 9 |
| Immature teratoma | 9080/1 | Immature teratoma of thymus (Related) | Teratoma, NOS | occurs | refer to Group 10 | Marx 2022, PDF p. 9 |
| Teratoma with somatic-type malignancies | 9084/3 | Teratoma with somatic type malignancies (Synonym) | Teratoma with malignant transformation | not_reported | refer to Group 10 | Marx 2022, PDF p. 9 |
| Mixed germ cell tumour | 9085/3 | Mixed germ cell tumor (Preferred) | Mixed germ cell tumor | not_reported | refer to Group 10 | Marx 2022, PDF p. 9 |
| Primary mediastinal (thymic) large B-cell lymphoma | 9679/3 | Thymic large B-cell lymphoma (Synonym) | Mediastinal large B-cell lymphoma | occurs | refer to Group 2 | Pfister 2022, PDF p. 4 |
| T-lymphoblastic leukaemia/lymphoma | 9837/3 | T lymphoblastic leukemia/lymphoma (Related) | Precursor T-cell lymphoblastic leukemia | not_reported | refer to Group 2 | ICCR Thymic 2022, PDF p. 15; ICD-O-3.1 manual, PDF p. 6 (printed p. 19) |
| Neuroblastoma | 9500/3 | Neuroblastoma, NOS (Preferred) | Neuroblastoma, NOS | not_reported | refer to Group 4 | Marx 2022, PDF p. 10; Marx 2022, PDF p. 11 |
| Extra-adrenal paraganglioma | 8693/3 | Extra-adrenal paraganglioma, NOS (Preferred) | Extra-adrenal paraganglioma, NOS | not_reported | refer to Group 4 | Marx 2022, PDF p. 11 |
| Synovial sarcoma | 9040/3 | Synovial sarcoma, NOS (Preferred) | Synovial sarcoma, NOS | not_reported | refer to Group 9 | Marx 2022, PDF p. 10; Marx 2022, PDF p. 11 |
| Rhabdomyosarcoma, NOS | 8900/3 | Rhabdomyosarcoma, NOS (Preferred) | Rhabdomyosarcoma, NOS | not_reported | refer to Group 9 | Marx 2022, PDF p. 11 |
| Carcinosarcoma | 8980/3 | Carcinosarcoma, NOS (Preferred) | Carcinosarcoma, NOS | not_reported | refer to Group 12 | ICCR Thymic 2022, PDF p. 10; Marx 2022, PDF p. 4 |

The WHO gives thymic squamous cell carcinoma 8070/3, Squamous cell carcinoma, NOS (ICCR Thymic 2022, PDF p. 10; Marx 2022, PDF p. 4). A report that says "thymic carcinoma, squamous type" takes 8070/3 as well: the WHO table assigns one code to the entity, so Rule K does not apply.

## 3 The pathway

Eight screens, prefixed `tm_` (the thyroid part already uses `th_`). Order: site, evidence gate, then laboratory, cytology or histology; histology leads to the NUT carcinoma screen, the picker and the adenocarcinoma marker checklist. The basis of diagnosis carried from the evidence gate (5 for cytology, 7 for histology) stands unless a screen sets another (8 for a NUTM1 gene test).

### `tm_site` (site_resolution)

**Question:** Where does the report place the tumour?

**Hint:** A thymoma, a thymic carcinoma and a thymic carcinoid arise in the thymus, which lies in the anterior (prevascular) mediastinum. Pick another site for one of these only when the report says it arose in thymic tissue outside the thymus. A tumour that has spread to the pleura or pericardium keeps the site where it began.

| Option | Outcome | Records | Reason or recognition aid | Pages |
|---|---|---|---|---|
| The thymus | go | go to `tm_evidence` | Site recorded as Thymus (C37.9). | ICCR Thymic 2022, PDF p. 8 |
| The anterior mediastinum, the mediastinum with no part named, or the chest, and the report calls the tumour a thymoma, a thymic carcinoma or a thymic carcinoid | go | go to `tm_evidence` | Site recorded as Thymus (C37.9). These tumours arise in the thymus. | ICCR Thymic 2022, PDF p. 8; ICD-O-3.1 manual, PDF p. 3 (printed p. 16); ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |
| The anterior (prevascular) mediastinum, for any other tumour | go | go to `tm_evidence` | Site recorded as Anterior mediastinum (C38.1). |  |
| The posterior (paravertebral) mediastinum, including a thymic tumour the report places there | go | go to `tm_evidence` | Site recorded as Posterior mediastinum (C38.2). | ICCR Thymic 2022, PDF p. 8; ICD-O-3.1 manual, PDF p. 10 (printed p. 23) |
| The mediastinum with no part named, for any other tumour | go | go to `tm_evidence` | Site recorded as Mediastinum, NOS (C38.3). |  |
| More than one part of the mediastinum, and the report does not say where the tumour began | go | go to `tm_evidence` | Site recorded as Overlapping lesion of heart, mediastinum and pleura (C38.8). | ICD-O-3.1 manual, PDF p. 5 (printed p. 18) |
| Beside the thymus or the mediastinum (for example perithymic), and the report does not call the tumour a thymic tumour type | go | go to `tm_evidence` | Site recorded as Thorax, NOS (C76.1). | ICD-O-3.1 manual, PDF p. 4 (printed p. 17) |
| Outside the mediastinum, such as inside the lung or in the neck (a thymic tumour in thymic tissue there) | refer | re-site (next screen asks the site) | A thymic tumour outside the mediastinum is coded to the place where it arose, and one inside the lung is coded as a lung tumour. The next screen asks for that site. | ICCR Thymic 2022, PDF p. 8 |

### `tm_evidence` (document_inventory)

**Question:** What is in the file for this tumour?

**Hint:** A radiology report counts as imaging. A fine needle aspiration report counts as cytology. A pathology report on a biopsy or a resection counts as histology. A report that calls the specimen inadequate or non-diagnostic counts as no tissue.

| Option | Outcome | Records | Reason or recognition aid | Pages |
|---|---|---|---|---|
| A referral letter or clinical note that states a malignant tumour of the thymus or mediastinum, with no imaging report and no tissue | code | 8000/3, basis 1 | Recorded as Neoplasm, malignant (8000/3) on clinical evidence. |  |
| An imaging report that states a malignant tumour, with no tissue | code | 8000/3, basis 2 | Recorded as Neoplasm, malignant (8000/3) on imaging evidence. |  |
| Imaging that shows the tumour, with a raised tumour-marker or hormone result, and no tissue | go | go to `tm_lab` |  |  |
| A note or report that calls the tumour possible, probable or suspected cancer only | not_registrable | not registrable | A possible or suspected cancer is not registered. |  |
| A cytology report (fine needle aspiration or fluid) | go | go to `tm_cytology` (basis 5) |  |  |
| A histology report on a biopsy or resection, with or without immunohistochemistry or gene reports | go | go to `tm_histology` (basis 7) |  | ICCR Thymic 2022, PDF p. 15 |

### `tm_lab` (lab_results)

**Question:** What does the marker or hormone result show, beside imaging that shows the tumour?

**Hint:** Pick a result only when the imaging report shows a tumour. A raised result with imaging that shows no tumour is not registered.

| Option | Outcome | Records | Reason or recognition aid | Pages |
|---|---|---|---|---|
| Raised chromogranin A in the blood | code | 8240/3, basis 4 | Recorded as Neuroendocrine tumor, NOS (8240/3) on tumour-marker evidence. | Marx 2022, PDF p. 8 |
| Raised adrenocorticotropic hormone (ACTH) with Cushing syndrome | code | 8158/3, basis 4 | Recorded as ACTH-producing tumor (8158/3) on hormone evidence. |  |
| Raised alpha-fetoprotein or human chorionic gonadotropin in the blood | refer | Group 10 | Germ cell tumours of the mediastinum are coded in ICCC-3 Group X, germ cell, trophoblastic and gonadal tumours. | ICCR Thymic 2022, PDF p. 15 |
| Another marker, or a raised result with imaging that shows no tumour | not_registrable | not registrable | This result is not enough to register a cancer. |  |

### `tm_cytology` (morphology_only)

**Question:** What does the cytology report call the tumour?

**Hint:** Code a cancer only when the report states one. Suspicious or atypical is not a diagnosis of cancer.

| Option | Outcome | Records | Reason or recognition aid | Pages |
|---|---|---|---|---|
| A named tumour type, such as thymoma, thymic carcinoma or NUT carcinoma | go | go to `tm_histology` (basis 5) |  |  |
| Carcinoma, with no type named | code | 8010/3, basis 5 | Recorded as Carcinoma, NOS (8010/3) on cytology. |  |
| Malignant, with no tumour type named | code | 8000/3, basis 5 | Recorded as Neoplasm, malignant (8000/3) on cytology. |  |
| Lymphoma | refer | Group 2 | Lymphomas are coded in ICCC-3 Group II, lymphomas and reticuloendothelial neoplasms. |  |
| Germ cell tumour | refer | Group 10 | Germ cell tumours of the mediastinum are coded in ICCC-3 Group X, germ cell, trophoblastic and gonadal tumours. |  |
| Suspicious for malignancy, atypical, benign or non-diagnostic | not_registrable | not registrable | The cytology report does not state a malignant tumour, so nothing is registered. |  |

### `tm_histology` (morphology_only)

**Question:** What does the histology report call the tumour?

**Hint:** Use the report's final diagnosis. Record the behaviour the pathologist states: a tumour the report calls benign is not recorded, and one it calls malignant is recorded as malignant. When the report lists more than one thymoma type in one tumour, pick the type with the higher code number; type AB is a single type.

| Option | Outcome | Records | Reason or recognition aid | Pages |
|---|---|---|---|---|
| Thymoma, type B1 | code | 8583/3, basis 7 | Recorded as Thymoma, type B1 (8583/3). | ICCR Thymic 2022, PDF p. 9; Rossi 2022, PMC section 4 |
| Thymoma, type B2 | code | 8584/3, basis 7 | Recorded as Thymoma, type B2 (8584/3). | ICCR Thymic 2022, PDF p. 9; Rossi 2022, PMC section 4 |
| Thymoma, type AB | code | 8582/3, basis 7 | Recorded as Thymoma, type AB (8582/3). Aid: The report records type AB as one type at 100 percent, not as a mixture of type A and type B. | ICCR Thymic 2022, PDF p. 9; Rossi 2022, PMC section 4 |
| Thymoma, type A, including atypical type A thymoma | code | 8581/3, basis 7 | Recorded as Thymoma, type A (8581/3). | ICCR Thymic 2022, PDF p. 9; Rossi 2022, PMC section 4 |
| Thymoma, type B3 | code | 8585/3, basis 7 | Recorded as Thymoma, type B3 (8585/3). | ICCR Thymic 2022, PDF p. 9; Rossi 2022, PMC section 4 |
| Thymoma with no type named, or sclerosing thymoma | code | 8580/3, basis 7 | Recorded as Thymoma, NOS (8580/3). | ICCR Thymic 2022, PDF p. 9; Marx 2022, PDF p. 3; Rossi 2022, PMC sections 1, 3 and 4 |
| NUT carcinoma | go | go to `tm_nut` | Aid: The report confirms NUT carcinoma with nuclear NUT staining on immunohistochemistry or a NUTM1 gene fusion. | Pfister 2022, PDF p. 14; ICCR Thymic 2022, PDF p. 15; Marx 2022, PDF p. 7 |
| A thymic carcinoma, a thymic carcinoid, a neuroendocrine carcinoma, metaplastic thymoma, or another carcinoma the report names | go | go to `tm_picker` |  |  |
| Carcinoma, with no type named | code | 8010/3, basis 7 | Recorded as Carcinoma, NOS (8010/3). | ICD-O-3.1 manual, PDF p. 8 (printed p. 21) |
| Micronodular thymoma with lymphoid stroma | exclude | 8580/1 | Not recorded. Micronodular thymoma with lymphoid stroma is 8580/1 in ICD-O-3.2, a tumour of uncertain behaviour. Aid: The report describes epithelial nodules in a lymphoid stroma that holds TdT-positive immature T cells. | ICCR Thymic 2022, PDF p. 9; Marx 2022, PDF p. 3; Marx 2022, PDF p. 7 |
| Microscopic thymoma, or a thymoma the report calls benign | exclude | 8580/0 | Not recorded. Microscopic thymoma is 8580/0 in ICD-O-3.2, a benign tumour, and a thymoma the report calls benign takes the same code. Aid: The current name for microscopic thymoma is nodular epithelial hyperplasia. | Marx 2022, PDF p. 3; ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |
| Nodular epithelial hyperplasia, thymic hyperplasia or a thymic cyst | not_registrable | not registrable | Not registrable. These are not tumours. | ICCR Thymic 2022, PDF p. 14 |
| Lipofibroadenoma | exclude | 9010/0 | Not recorded. Lipofibroadenoma is 9010/0 in ICD-O-3.2 (Fibroadenoma, NOS), a benign tumour. | ICCR Thymic 2022, PDF p. 9 |
| Thymolipoma | exclude | 8850/0 | Not recorded. Thymolipoma is 8850/0 in ICD-O-3.2 (Lipoma, NOS), a benign tumour. | Marx 2022, PDF p. 11 |
| A germ cell tumour: seminoma, embryonal carcinoma, yolk sac tumour, choriocarcinoma, teratoma or a mixed germ cell tumour | refer | Group 10 | Germ cell tumours of the mediastinum are coded in ICCC-3 Group X, germ cell, trophoblastic and gonadal tumours. | Marx 2022, PDF p. 9 |
| A carcinoma or another cancer that arose in a teratoma (teratoma with somatic-type malignancy) | refer | Group 10 | A teratoma with somatic-type malignancy is coded in ICCC-3 Group X as Teratoma with malignant transformation (9084/3), not as a carcinoma. | Marx 2022, PDF p. 9 |
| Lymphoma, including mediastinal large B-cell lymphoma, Hodgkin lymphoma and T-lymphoblastic lymphoma | refer | Group 2 | Lymphomas are coded in ICCC-3 Group II, lymphomas and reticuloendothelial neoplasms. | Pfister 2022, PDF p. 4; ICCR Thymic 2022, PDF p. 15 |
| T-lymphoblastic leukaemia | refer | Group 1 | Leukaemias are coded in ICCC-3 Group I and recorded at the bone marrow (C42.1). | ICD-O-3.1 manual, PDF p. 6 (printed p. 19) |
| Neuroblastoma, ganglioneuroblastoma or paraganglioma | refer | Group 4 | These tumours are coded in ICCC-3 Group IV, neuroblastoma and other peripheral nervous cell tumours. | Marx 2022, PDF p. 10; Marx 2022, PDF p. 11 |
| A sarcoma, such as synovial sarcoma, rhabdomyosarcoma, Ewing sarcoma, liposarcoma or malignant peripheral nerve sheath tumour | refer | Group 9 | Soft-tissue sarcomas are coded in ICCC-3 Group IX, soft-tissue and other extraosseous sarcomas. | Marx 2022, PDF p. 10; Marx 2022, PDF p. 11 |
| Carcinosarcoma | refer | Group 12 | Carcinosarcoma, NOS (8980/3) is coded in ICCC-3 Group XII, other and unspecified malignant tumours. | ICCR Thymic 2022, PDF p. 10 |
| A deposit (metastasis) of a tumour that began outside the thymus and mediastinum | refer | re-site (next screen asks the site) | A deposit is coded at the site where the tumour began. The next screen asks for that site. | ICCR Thymic 2022, PDF p. 15; Marx 2022, PDF p. 9; ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |

### `tm_nut` (histology_subclassification)

**Question:** How does the report confirm the NUT carcinoma?

| Option | Outcome | Records | Reason or recognition aid | Pages |
|---|---|---|---|---|
| Nuclear NUT staining on immunohistochemistry | code | 8023/3, basis 7 | Recorded as Nuclear protein in testis (NUT)-associated carcinoma (8023/3). | ICCR Thymic 2022, PDF p. 15 |
| A gene test that shows a NUTM1 gene fusion | code | 8023/3, basis 8 | Recorded as Nuclear protein in testis (NUT)-associated carcinoma (8023/3). | Marx 2022, PDF p. 7 |
| The report names NUT carcinoma and gives no NUT stain or gene result | code | 8023/3, basis 7 | Recorded as Nuclear protein in testis (NUT)-associated carcinoma (8023/3). | ICD-O-3.1 manual, PDF p. 8 (printed p. 21) |
| The report calls NUT carcinoma possible or suspected only | go | go to `tm_picker` | A possible NUT carcinoma is not recorded as NUT carcinoma. Pick the carcinoma the report names. |  |

### `tm_picker` (morphology_only)

**Question:** Which tumour does the histology report name?

**Hint:** Type part of the name to filter the list. When the report names two tumour types in one tumour and no entry covers both, pick the one with the higher code number. When the report gives two grades of carcinoid or neuroendocrine tumour, pick the higher grade.

| Option | Outcome | Records | Reason or recognition aid | Pages |
|---|---|---|---|---|
| Metaplastic thymoma | code | 8580/3, basis 7 | Recorded as Thymoma, NOS (8580/3), the code the World Health Organization gives metaplastic thymoma. Aid: The report may name a YAP1-MAML2 gene fusion. | ICCR Thymic 2022, PDF p. 9; ICCR Thymic 2022, PDF p. 16 |
| Squamous cell carcinoma of the thymus, including micronodular thymic carcinoma with lymphoid hyperplasia | code | 8070/3, basis 7 | Recorded as Squamous cell carcinoma, NOS (8070/3). Aid: The micronodular subtype shows nodules of atypical epithelial cells in a lymphoid stroma with no TdT-positive immature T cells. | ICCR Thymic 2022, PDF p. 10; Marx 2022, PDF p. 7 |
| Basaloid carcinoma | code | 8123/3, basis 7 | Recorded as Basaloid carcinoma (8123/3). | ICCR Thymic 2022, PDF p. 10 |
| Lymphoepithelial carcinoma, or lymphoepithelioma-like carcinoma | code | 8082/3, basis 7 | Recorded as Lymphoepithelial carcinoma (8082/3). | Marx 2022, PDF p. 6 |
| Adenocarcinoma with no type named, including a high-grade adenocarcinoma with papillary features | code | 8140/3, basis 7 | Recorded as Adenocarcinoma, NOS (8140/3). | Marx 2022, PDF p. 6 |
| Low-grade papillary adenocarcinoma, or papillary adenocarcinoma | code | 8260/3, basis 7 | Recorded as Papillary adenocarcinoma, NOS (8260/3). Aid: The report describes bland papillary features; the former name was papillary adenocarcinoma. | Marx 2022, PDF p. 4; Marx 2022, PDF p. 6 |
| Thymic carcinoma with adenoid cystic carcinoma-like features | code | 8200/3, basis 7 | Recorded as Adenoid cystic carcinoma (8200/3), the code the World Health Organization gives this carcinoma. | ICCR Thymic 2022, PDF p. 10 |
| Adenocarcinoma, enteric type | code | 8144/3, basis 7 | Recorded as Adenocarcinoma, intestinal type (8144/3). Aid: The report shows at least one intestinal marker, CK20, CDX2 or MUC2, and the tumour may be mucinous or non-mucinous. | Marx 2022, PDF p. 4 |
| Adenocarcinoma with CK20, CDX2 or MUC2 results, and no type named | go | go to `tm_adeno_ihc` |  | Marx 2022, PDF p. 7 |
| Adenosquamous carcinoma | code | 8560/3, basis 7 | Recorded as Adenosquamous carcinoma (8560/3). | Marx 2022, PDF p. 4 |
| Mucoepidermoid carcinoma | code | 8430/3, basis 7 | Recorded as Mucoepidermoid carcinoma (8430/3). Aid: The report may name a MAML2 rearrangement. | ICCR Thymic 2022, PDF p. 16 |
| Clear cell carcinoma, including hyalinizing clear cell carcinoma | code | 8310/3, basis 7 | Recorded as Clear cell adenocarcinoma, NOS (8310/3). Aid: The hyalinizing subtype resembles its salivary gland counterpart and may carry an EWSR1 rearrangement. | ICCR Thymic 2022, PDF p. 10; Marx 2022, PDF p. 6 |
| Sarcomatoid carcinoma | code | 8033/3, basis 7 | Recorded as Pseudosarcomatous carcinoma (8033/3), the ICD-O-3.2 preferred term for sarcomatoid carcinoma. | Marx 2022, PDF p. 4 |
| Undifferentiated carcinoma | code | 8020/3, basis 7 | Recorded as Carcinoma, undifferentiated, NOS (8020/3). | ICCR Thymic 2022, PDF p. 10 |
| Thymic carcinoma, with no type named | code | 8586/3, basis 7 | Recorded as Thymic carcinoma, NOS (8586/3). | Marx 2022, PDF p. 4 |
| Hepatoid, rhabdoid or sebaceous carcinoma of the thymus, or undifferentiated large cell carcinoma with a Castleman disease-like reaction | code | 8586/3, basis 7 | Recorded as Thymic carcinoma, NOS (8586/3), the code the World Health Organization gives these thymic carcinomas. | Marx 2022, PDF p. 4 |
| Typical carcinoid, neuroendocrine tumour grade 1, or carcinoid with no type named | code | 8240/3, basis 7 | Recorded as Neuroendocrine tumor, NOS (8240/3). | ICCR Thymic 2022, PDF p. 10 |
| Atypical carcinoid, or neuroendocrine tumour grade 2 | code | 8249/3, basis 7 | Recorded as Neuroendocrine tumor, grade 2 (8249/3). | ICCR Thymic 2022, PDF p. 10 |
| Neuroendocrine tumour, grade 3 | code | 8249/3, basis 7 | Recorded as Neuroendocrine tumor, grade 2 (8249/3), the code ICD-O-3.2 gives neuroendocrine tumour, grade 3. Aid: The report describes carcinoid morphology with a raised mitotic count or Ki-67 index and does not call the tumour large cell neuroendocrine carcinoma. | Marx 2022, PDF p. 8; ICD-O-3.1 manual, PDF p. 8 (printed p. 21) |
| Small cell carcinoma | code | 8041/3, basis 7 | Recorded as Small cell carcinoma, NOS (8041/3). Aid: A small cell carcinoma with less than 10 percent large cell neuroendocrine carcinoma keeps this name. | ICCR Thymic 2022, PDF p. 10; Marx 2022, PDF p. 6 |
| Combined small cell carcinoma, including small cell carcinoma with 10 percent or more large cell neuroendocrine carcinoma | code | 8045/3, basis 7 | Recorded as Combined small cell carcinoma (8045/3). | ICCR Thymic 2022, PDF p. 10; Marx 2022, PDF p. 6 |
| Large cell neuroendocrine carcinoma, including combined large cell neuroendocrine carcinoma | code | 8013/3, basis 7 | Recorded as Large cell neuroendocrine carcinoma (8013/3). | ICCR Thymic 2022, PDF p. 10; ICCR Thymic 2022, PDF p. 9 |

### `tm_adeno_ihc` (ihc_checklist)

**Question:** Answer each stain as the report states it.

**Hint:** Answer CK20, CDX2 and MUC2 as positive, negative or not done. One positive intestinal marker records Adenocarcinoma, intestinal type (8144/3). With none positive, the tumour is recorded as Adenocarcinoma, NOS (8140/3).

No answer buttons: the clerk answers each stain; the rules are in section 4.

**Paediatric evidence, 8 October 2026.** Rossi 2022 reports the thymoma types A, AB, B1, B2 and B3 and thymoma with no WHO type in patients aged 0.9 to 17 years (PMC section 4), so those six picker entries moved onto `tm_histology` as options, with the same codes, reasons and recognition aids, ordered by Rossi's counts: B1 (20 of 44 typed thymomas), B2 (12), AB (6), A (3), B3 (3), then thymoma with no type named. The sentence of the picker hint on more than one thymoma type moved with them to the `tm_histology` hint. Rossi 2022 excluded thymic carcinoma and thymic neuroendocrine tumours, so thymic squamous cell carcinoma, thymic carcinoma with no type named and the carcinoids stay in the picker until a paediatric source reports them (data gap 1).

**Combined and heterogeneous tumours.** ICCR Thymic 2022 (PDF p. 9) and Marx 2022 (PDF p. 6) set how pathologists name them: thymomas of more than one type list every type from the predominant one in 10 percent steps; a thymic carcinoma with any thymoma is "combined thymic carcinoma and thymoma"; a tumour with any small cell or large cell neuroendocrine carcinoma component is "combined small cell carcinoma" or "combined large cell neuroendocrine carcinoma"; the more aggressive component is named first. ICD-O-3.2 holds single codes for two of these (8045/3 Combined small cell carcinoma; Combined large cell neuroendocrine carcinoma, a related term at 8013/3). Every other combination falls to Rule K: more than one thymoma type through the `tm_histology` hint, and two tumour types with no entry covering both through the `tm_picker` hint (data gap 8).

## 4 Immunohistochemistry rules

| Panel | Positive | Negative | Records | Pages |
|---|---|---|---|---|
| `tm_adeno_ihc` | CK20 | — | 8144/3 | Marx 2022, PDF p. 7; Marx 2022, PDF p. 4 |
| `tm_adeno_ihc` | CDX2 | — | 8144/3 | Marx 2022, PDF p. 7; Marx 2022, PDF p. 4 |
| `tm_adeno_ihc` | MUC2 | — | 8144/3 | Marx 2022, PDF p. 7; Marx 2022, PDF p. 4 |
| `tm_adeno_ihc` | — | CK20, CDX2, MUC2 | 8140/3 | Marx 2022, PDF p. 7 |

One positive intestinal marker (CK20, CDX2 or MUC2) makes a thymic adenocarcinoma enteric type, 8144/3 (Marx 2022, PDF pp. 4 and 7). The fallback, with none positive, is Adenocarcinoma, NOS 8140/3. No other marker panel in these sources decides between codes: no immunohistochemical marker reliably separates type B3 thymoma from thymic carcinoma (ICCR Thymic 2022, PDF p. 15); CD5 with CD117 only supports a thymic origin over a lung squamous cell carcinoma, a site question rather than a code; Ki-67 helps separate carcinoid from small cell carcinoma in biopsies but has no cut-off in these sources and does not separate typical from atypical carcinoid (Marx 2022, PDF p. 8); chromogranin A, EZH2, TP53, RB and SSTR2A separate NET G3 from large cell neuroendocrine carcinoma (Marx 2022, PDF p. 9) without a stated rule. TdT-positive immature T cells mark micronodular thymoma with lymphoid stroma and are absent from micronodular thymic carcinoma (Marx 2022, PDF p. 7); this reaches the clerk as a recognition aid on both entries, not as a checklist, because the report names one or the other.

## 5 Registration without tissue

| Evidence on file | Records | Basis | Pages |
|---|---|---|---|
| A referral letter or clinical note that states a malignant tumour of the thymus or mediastinum, no imaging, no tissue | 8000/3 | 1 | registrar's rule |
| An imaging report that states a malignant tumour of the thymus or mediastinum, no tissue | 8000/3 | 2 | registrar's rule |
| Imaging that shows a thymic or mediastinal tumour, with a raised chromogranin A in the blood (Visser 2023 Table 4, as the registrar gave it) | 8240/3 | 4 | Marx 2022, PDF p. 8 |
| Imaging that shows a thymic or mediastinal tumour, with raised adrenocorticotropic hormone and Cushing syndrome (Visser 2023 Table 4, as the registrar gave it) | 8158/3 | 4 | registrar's rule |

Clinical or imaging evidence records 8000/3 (basis 1 or 2). ICCC-2017 places 8000/3 at C37.9 and C38 in XIIb, so these cases count in Group XII (section 9). The two basis 4 answers apply the registrar's Visser 2023 Table 4 rule as the controller gave it; no source in this part discusses a serum or plasma marker (data gap 3). Marx 2022 (PDF p. 8) supports only that neuroendocrine tumours arise in the thymus. A marker with imaging that shows no tumour, and a possible or suspected cancer, are not registrable.

## 6 Laboratory tests

| Test | Specimen | Role | Pages |
|---|---|---|---|
| Chromogranin A | plasma | With imaging that shows the tumour, a raised result records Neuroendocrine tumor, NOS (8240/3) at basis 4 under the registrar's Visser 2023 Table 4 rule. The sources in this part give chromogranin A a role only as an immunohistochemical marker, separating NET G3 from large cell neuroendocrine carcinoma. | Marx 2022, PDF p. 9 |
| Adrenocorticotropic hormone (ACTH) | plasma | With imaging that shows the tumour and Cushing syndrome, a raised result records ACTH-producing tumor (8158/3) at basis 4 under the registrar's Visser 2023 Table 4 rule. No source in this part mentions it. | registrar's rule |
| Alpha-fetoprotein and human chorionic gonadotropin | serum | A raised result sends the case to Group X. The sources in this part name both only as immunohistochemical stains for germ cell tumours, and warn that NUT carcinomas can express alpha-fetoprotein. | ICCR Thymic 2022, PDF p. 15; Marx 2022, PDF p. 10 |

Neither Marx 2022 nor the ICCR guide gives a serum, plasma or urine test a diagnostic role for a thymic or mediastinal tumour. `tm_lab` carries the registrar's rule for chromogranin A and adrenocorticotropic hormone, and a referral to Group X for alpha-fetoprotein or human chorionic gonadotropin.

## 7 Rules A to K

| Rule | Applies | Where it reaches the clerk |
|---|---|---|
| A | yes | tm_site option 'The anterior mediastinum, the mediastinum with no part named, or the chest, and the report calls the tumour a thymoma, a thymic carcinoma or a thymic carcinoid' records Thymus (C37.9): the chest (C76.1) is an ill-defined region and the tumour type names the tissue. Its reason states the site. |
| B | yes | tm_site option 'Beside the thymus or the mediastinum (for example perithymic), and the report does not call the tumour a thymic tumour type' records Thorax, NOS (C76.1). A thymic tumour type beside the thymus takes the thymus through the option above it, because the tumour type shows the tissue. |
| C | yes | tm_site option 'More than one part of the mediastinum, and the report does not say where the tumour began' records Overlapping lesion of heart, mediastinum and pleura (C38.8), named in its reason. |
| D | yes | Referral only: the lymphoma options on tm_histology and tm_cytology send the case to Group II, whose questions set the lymphoma's site. |
| E | yes | tm_histology option 'T-lymphoblastic leukaemia' refers to Group I; its reason states that leukaemias are recorded at the bone marrow (C42.1). |
| F | yes | tm_histology hint ('Record the behaviour the pathologist states') and the exclusion options: micronodular thymoma with lymphoid stroma (8580/1), and 'Microscopic thymoma, or a thymoma the report calls benign' (8580/0), whose reason says a thymoma called benign takes the benign code. |
| G | yes | tm_picker hint ('When the report gives two grades of carcinoid or neuroendocrine tumour, pick the higher grade'): typical and atypical carcinoid in one tumour records 8249/3. The sixth digit is not built (registrar, 7 October 2026). |
| H | yes | ICD-O-3.2 prints (C37.9) beside 8580-8586. tm_site hint and its second option record the thymus for a thymic tumour type when the report places it in the anterior mediastinum or mediastinum with no part named; the posterior mediastinum option and the 'Outside the mediastinum' option keep the site the report gives for an ectopic thymic tumour, including Intrapulmonary thymoma, which ICD-O-3.2 prints with (C34._). The deposit option on tm_histology covers the check that the stated site is not a metastasis. |
| J | no | Every WHO thymus and mediastinum name maps to an ICD-O-3.2 term or to a code the WHO table prints; no name needs its word roots reordered. |
| K | yes | tm_histology hint: more than one thymoma type in one tumour takes the higher code (A 8581 < AB 8582 < B1 8583 < B2 8584 < B3 8585). tm_picker hint: two tumour types with no entry covering both take the higher code. Combined small cell carcinoma (8045/3) and combined large cell neuroendocrine carcinoma (8013/3) have single codes and their own entries. Combined thymic carcinoma and thymoma is registrar question 4. |

Rule sources: ICD-O-3.1 manual, PDF p. 2 (printed p. 15) for the summaries of Rules C to H; PDF p. 3 (printed p. 16) for Rule A; PDF p. 4 (printed p. 17) for Rule B; PDF p. 5 (printed p. 18) for Rule C; PDF p. 6 (printed p. 19) for Rule E; PDF p. 8 (printed p. 21) for Rule G and "Coding is based on what the pathologist states"; PDF p. 10 (printed p. 23) for Rule H; PDF p. 11 (printed p. 24) for Rules J and K. There is no Rule I.

## 8 Code currency

| Code | Behaviour | Finding | What the tree does |
|---|---|---|---|
| 8580-8585 | 3 | Currency check section 3: thymoma types A to B3 changed behaviour /1 to /3 in ICD-O-3.2. Section 4: REDCap labels read 'Thymoma, malignant, NOS', 'Thymoma, type A, malignant' and so on; the ICD-O-3.2 preferred terms are 'Thymoma, NOS', 'Thymoma, type A', 'Thymoma, type AB', 'Thymoma, type B1', 'Thymoma, type B2', 'Thymoma, type B3'. | Every thymoma entry records /3, and each reason names the ICD-O-3.2 preferred term. The six relabels go on the REDCap-side list. |
| 8580 | 1 | Micronodular thymoma with lymphoid stroma is 8580/1 in ICD-O-3.2 and in the WHO table. | Exclusion on tm_histology. |
| 8580 | 0 | ICD-O-3.2 keeps Microscopic thymoma (preferred) and Thymoma, benign (related) at 8580/0; the WHO 5th edition calls the lesion nodular epithelial hyperplasia. | Exclusion on tm_histology, with a recognition aid that names nodular epithelial hyperplasia. |
| 8580 | 3 | ICD-O-3.2 lists Sclerosing thymoma as a related term at 8580/3; the WHO 5th edition no longer counts it as a type. | The tm_histology option 'Thymoma with no type named, or sclerosing thymoma' records 8580/3. |
| 8581, 8583, 8584, 8585 | 3 | ICD-O-3.2 marks the old synonyms [obs]: Thymoma, medullary and Thymoma, spindle cell (8581); lymphocyte-rich, lymphocytic, organoid and predominantly cortical (8583); cortical (8584); atypical, epithelial and Well differentiated thymic carcinoma (8585). The preferred terms are current. | Labels carry the WHO 5th edition names only; no obsolete synonym appears on a screen. |
| 8023 | 3 | Currency check section 6: NUT carcinoma is current in ICD-O-3.2 (synonym of Nuclear protein in testis (NUT)-associated carcinoma) and REDCap does not offer it. | Built on tm_nut; reason names the preferred term. Goes on the REDCap-side list. |
| 8045 | 3 | Combined small cell carcinoma is current in ICD-O-3.2 and in the WHO thymus table, and the REDCap Group 11 list does not offer it. The currency check does not list it. | Picker entry. Goes on the REDCap-side list. |
| 8033 | 3 | Currency check section 4: REDCap label 'Sarcomatoid carcinoma'; ICD-O-3.2 preferred term 'Pseudosarcomatous carcinoma'. | Reason names Pseudosarcomatous carcinoma; relabel on the REDCap-side list. |
| 8240 | 3 | Currency check section 4: REDCap label 'Carcinoid tumor, NOS'; ICD-O-3.2 preferred term 'Neuroendocrine tumor, NOS'. | Reason names Neuroendocrine tumor, NOS; relabel on the REDCap-side list. |
| 8249 | 3 | Currency check section 4: REDCap label 'Atypical carcinoid tumor'; ICD-O-3.2 preferred term 'Neuroendocrine tumor, grade 2'. ICD-O-3.2 also lists Neuroendocrine tumor, grade 3 as a related term here, while Marx 2022 reports that current WHO thoracic criteria designate such thymic tumours large cell neuroendocrine carcinoma (8013/3). | Reasons name Neuroendocrine tumor, grade 2; a report that says neuroendocrine tumour, grade 3 records 8249/3 (registrar question 7). |
| 8158 | 3 | Currency check section 4: REDCap label 'Endocrine tumor, functioning, NOS' is an [obs] term; the ICD-O-3.2 preferred term is 'ACTH-producing tumor'. Section 3: 8158 changed behaviour /1 to /3. | tm_lab reason names ACTH-producing tumor (8158/3); relabel on the REDCap-side list. |
| 8010 | 3 | The REDCap Group 11 XIf list labels 8010 'Epithelial Tumor, NOS'; ICD-O-3.2 has no such term at /3 (preferred Carcinoma, NOS; synonym Epithelial tumor, malignant; 8010/0 is Epithelial tumor, benign). The currency check section 4 does not list it. | Reason names Carcinoma, NOS. Relabel on the REDCap-side list. |
| 8260 | 3 | The WHO name Low-grade papillary adenocarcinoma is not an ICD-O-3.2 term; the code's preferred term is Papillary adenocarcinoma, NOS. REDCap's label matches the preferred term. | Label carries both names; reason names Papillary adenocarcinoma, NOS. |
| 8586 | 3 | The WHO places hepatoid, rhabdoid and sebaceous carcinoma of the thymus and undifferentiated large cell carcinoma with Castleman disease-like reaction under Thymic carcinoma, NOS 8586/3. ICD-O-3.2 also holds 8410/3 Sebaceous carcinoma (REDCap label 'Sebaceous adenocarcinoma', currency check section 4) and 8576/3 Hepatoid adenocarcinoma. | Draft records 8586/3 per the WHO table (registrar question 5). |
| 8980 | 3 | The WHO lists carcinosarcoma as a subtype of thymic sarcomatoid carcinoma; ICCC-2017 places 8980 in XIIa4 at every site. | Referral to Group XII, not a Group XI option. |
| 8000 | 3 | ICCC-2017 places 8000/3 at C37.9 and C38 in XIIb (other unspecified malignant tumours). | Tissue-free and cytology 'malignant, no type' answers record 8000/3; the case falls in Group XII by ICCC (conflicts). |
| 9080 | 1 | ICD-O-3.2 prints Immature teratoma of thymus at 9080/1; ICCC-2017 Xb2 takes 9080 at C37.9 only at /3. | Referral to Group X, which decides. |

REDCap-side list (standing rule 16; the tool does not test REDCap): relabel 8580-8585 to their ICD-O-3.2 preferred terms; relabel 8033, 8240, 8249, 8158 and 8010; add 8023/3 and 8045/3, which the Group 11 option list lacks.

## 9 Conflicts with other groups

| Other group | Codes | Sites | Issue |
|---|---|---|---|
| 12 | 8980 | C37.9, C38.1, C38.2, C38.3, C38.8 | The WHO thymus table lists carcinosarcoma 8980/3 as a subtype of sarcomatoid carcinoma, but ICCC-2017 places 8980 in XIIa4 at every site. The thymus tree refers it to Group XII. |
| 12 | 8000 | C37.9, C38.1, C38.2, C38.3, C38.8 | Registration without tissue (basis 1 or 2) and cytology that names no type record 8000/3, which ICCC-2017 places in XIIb at C37.9 and C38. These cases count in Group XII, not Group XI. |
| 10 | 9084, 9061, 9071, 9085, 9086 | C37.9, C38.1, C38.2, C38.3, C38.8 | A carcinoma arising in a mediastinal teratoma is Teratoma with somatic-type malignancies 9084/3, Group X (Xb2), not a Group XI carcinoma. Every mediastinal germ cell tumour refers to Group X. |
| 10 | 9080 | C37.9 | ICD-O-3.2 codes immature teratoma of thymus 9080/1, and the WHO mediastinal table agrees; ICCC-2017 Xb2 at C37.9 takes /3 only. Group X decides whether it is registered. |
| 10 | 8023, 9071 | C37.9, C38.1, C38.2, C38.3, C38.8 | NUT carcinomas can express SALL4 and alpha-fetoprotein and be mistaken for germ cell tumours, and germ cell tumours can express wild-type NUT protein and be mistaken for NUT carcinoma (Marx 2022, PDF p. 10). The tool records the final diagnosis the report states. |
| 2 | 9679, 9837, 9727 | C37.9, C38.1, C38.2, C38.3, C38.8 | Mediastinal large B-cell lymphoma and T-lymphoblastic lymphoma present as thymic or mediastinal masses, and the lymphoid component of type B thymoma can raise the suspicion of T-lymphoblastic lymphoma. ICCC-2017 places 9679/3 in IIb2 and 9837/3 in IIb1 at these sites. |
| 1 | 9837 | C42.1 | T-lymphoblastic leukaemia is coded to the bone marrow (Rule E) and ICCC-2017 places 9837/3 there in Ia1; the same code at C37.9 or C38 is IIb1. The histology screen offers the leukaemia and the lymphoma as separate referrals. |
| 4 | 9500, 9490, 8693 | C38.2, C38.3 | Neuroblastoma, ganglioneuroblastoma and extra-adrenal paraganglioma occur in the posterior mediastinum. ICCC-2017 places 9500 and 9490 in IVa and 8693/3 in IVb. |
| 9 | 9040, 8900, 9364, 8850, 9540 | C37.9, C38.1, C38.2, C38.3, C38.8 | Mediastinal sarcomas refer to Group IX. Thymolipoma 8850/0 shares its code number with liposarcoma 8850/3: the thymus tree excludes the first and refers the second. |
| 11 | 8580, 8581, 8582, 8583, 8584, 8585, 8586 | C34.0, C34.1, C34.2, C34.3, C34.8, C34.9 | Within Group XI: an ectopic thymoma in the lung is dealt with as a primary pulmonary tumour (ICCR, PDF p. 8), and ICD-O-3.2 prints Intrapulmonary thymoma (C34._). The thymus tree re-sites it, so the lung part (XIf4) must offer thymoma codes or a route back to this tree's thymoma options. |
| 11 | — | C38.1, C38.3 | Within Group XI: thoracic SMARCA4-deficient undifferentiated tumour belongs to the lung chapter of the WHO thoracic volume and most often invades the mediastinum. This part's sources print no code and ICD-O-3.2 holds no term; the lung part (XIf4) and the registrar decide. |
| 11 | 8588, 8589, 8580, 8586 | C73.9 | Within Group XI: thymic-type tumours of the thyroid (spindle epithelial tumour with thymus-like elements 8588/3, intrathyroid thymic carcinoma 8589/3, thymoma within the thyroid) belong to the thyroid tree. The thymus tree's 'Outside the mediastinum' option re-sites them. |
| 11 | 8023 | C37.9, C38.1, C38.2, C38.3 | Within Group XI: NUT carcinoma 8023/3 is shared with the nasopharynx, lung and NUT carcinoma parts. Whether a mediastinal NUT carcinoma records C37.9 (XIf5) or C38 (XIf10) is open (registrar question 3). The draft records the site the report gives. |

Each referral was checked in ICCC-2017 for the code at C37.9 and C38: 9061, 9071, 9085, 9084 in Xb; 9679 in IIb2; 9837 in IIb1 (Ia1 at C42.1); 9500 and 9490 in IVa; 8693 in IVb; 9040 in IXd7; 8900 in IXa; 9364 in IXd2; 9540 in IXb2; 8850/3 in IXd4; 8980 in XIIa4; 8000 in XIIb. Group 11 rows mark boundaries with other Group 11 parts.

## 10 Data gaps

1. **Paediatric occurrence (ages 0 to 18) of thymic carcinoma by type, thymic carcinoid and neuroendocrine carcinoma, and metaplastic thymoma.** Rossi 2022 settles the thymoma types A to B3 and thymoma with no type named in patients aged 0.9 to 17 years; they are now options on tm_histology. Its review excluded thymic carcinoma, thymic neuroendocrine tumours and combined thymic carcinomas (PMC section 3) and reports no metaplastic thymoma. Neither Marx 2022 nor the ICCR guide gives ages, and Pfister 2022 Table 3 lists no thymic tumour among the thoracic tumours of children, so every other thymic entity stays in tm_picker. A paediatric report would move thymic squamous cell carcinoma and the carcinoids onto tm_histology as options. Candidate source: Stachowicz-Stencel T, Orbach D, Brecht I, et al. Thymoma and thymic carcinoma in children and adolescents: a report from the European Cooperative Study Group for Pediatric Rare Tumors (EXPeRT). Eur J Cancer 2015;51(16):2444-2452.
2. **Where a mediastinal NUT carcinoma is recorded: thymus (C37.9) or mediastinum (C38.1 to C38.3).** Marx 2022 lists NUT carcinoma in the WHO table of thymic epithelial tumours (PDF p. 4) and says nothing about its site. The choice moves the case between XIf5 and XIf10. Candidate source: The NUT carcinoma part's sources (Lemelle 2022, Luo 2025), or the NUT carcinoma chapter of WHO Classification of Tumours, Thoracic Tumours, 5th edition (2021).
3. **Confirmation that Visser 2023 Table 4 (chromogranin A; adrenocorticotropic hormone) applies at the thymus and mediastinum.** No source in this part gives any serum or plasma test a diagnostic role. tm_lab applies the registrar's Visser rule as the controller stated it. Candidate source: Visser 2023, Front Oncol 13:1250549, Table 4.
4. **The ICD-O code the WHO gives thoracic SMARCA4-deficient undifferentiated tumour.** Marx 2022 names the tumour only as a mimic that invades the mediastinum; ICD-O-3.2 holds no term for it. It cannot be built or excluded. Candidate source: XIf4-lung__Nicholson-2022.txt (the lung part's WHO thoracic summary), Table 1.
5. **A registry coding rule for a thymic epithelial tumour reported as an anterior mediastinal or mediastinal mass.** Rule H keeps the stated site when it differs from the printed site, while ICCR states these tumours arise in the thymus in the anterior mediastinum. The draft records C37.9 (registrar question 2). Candidate source: SEER Program Coding and Staging Manual, primary site instructions for thymus and mediastinum.
6. **A paediatric source for the option 'Carcinoma, with no type named' (8010/3).** The option rests on the coding rule that the clerk codes what the pathologist states, not on a paediatric report, and Rossi 2022 reviews thymomas only. It stays an option; the controller decides whether a fallback option needs a paediatric report. Candidate source: A paediatric thymic carcinoma series, such as Stachowicz-Stencel T, et al. Eur J Cancer 2015;51(16):2444-2452 (EXPeRT).
7. **The order of NUT carcinoma against the thymoma options on tm_histology.** Rossi 2022 gives paediatric counts for the thymoma types only. No source in this part counts thymic or mediastinal NUT carcinoma in children; its paediatric report (Pfister 2022) is in the head and neck section. The draft lists type B1 (the commonest), then types B2, AB, A and B3 by Rossi's counts, then thymoma with no type named, then NUT carcinoma. Candidate source: The NUT carcinoma part's paediatric sources (Lemelle 2022).
8. **Where the clerk records a combined thymic carcinoma and thymoma now that the two components sit on different screens.** The thymoma types are options on tm_histology and the thymic carcinomas and carcinoids are tm_picker entries. The thymoma-type sentence of the Rule K hint moved to tm_histology; the two-tumour-types sentence stays on tm_picker. Rossi 2022 found no thymoma of mixed types in its paediatric cases (PMC section 5) and excluded combined thymic carcinomas (PMC section 3). Registrar question 4 decides which component is recorded, and with it which screen carries the rule. Candidate source: Registrar question 4.

### Questions for the registrar

1. Paediatric occurrence of thymic tumours. Rossi 2022 (PMC section 4) now reports the thymoma types and thymoma with no type named in patients aged 0.9 to 17 years, and they are options on the histology screen. No source in this part reports thymic carcinoma or a thymic neuroendocrine tumour in patients aged 0 to 18: Rossi 2022 excluded them, and Pfister 2022 Table 3 lists no thymic tumour among the thoracic tumours of children (PDF p. 14). Under ruling 1 they sit in the picker. Should the controller fetch a paediatric series (for example the EXPeRT report, Stachowicz-Stencel 2015) so that the commonest thymic carcinomas and carcinoids become options on the histology screen?
2. Site of a thymic tumour reported in the mediastinum. A thymoma, thymic carcinoma or thymic carcinoid that the report places in the anterior mediastinum, the mediastinum with no part named, or the chest: record Thymus (C37.9), because these tumours arise in the thymus (ICCR Thymic 2022, PDF p. 8) and ICD-O-3.2 prints C37.9 beside 8580-8586, or the stated mediastinal site (C38.1 or C38.3), as Rule H's wording on a stated site allows? The draft records C37.9. Only the subgroup changes (XIf5 against XIf10).
3. Site of a mediastinal NUT carcinoma. Marx 2022 places NUT carcinoma in the WHO table of thymic epithelial tumours (PDF p. 4) and says nothing about its site. The draft records the site the report gives: Thymus (C37.9) only when the report names the thymus, otherwise C38.1, C38.2 or C38.3. Confirm, or rule that an anterior mediastinal NUT carcinoma records C37.9.
4. Combined thymic carcinoma and thymoma under Rule K. The higher code wins, and every thymoma code (8581-8585) is higher than every thymic carcinoma code except 8586/3 Thymic carcinoma, NOS. A combined squamous cell carcinoma and type B3 thymoma would record 8585/3, although the WHO and ICCR name the carcinoma first as the more aggressive component (Marx 2022, PDF p. 6; ICCR Thymic 2022, PDF p. 9). The same holds for combined carcinoid and thymoma. Keep Rule K, or record the carcinoma (or carcinoid) component?
5. Rare thymic carcinomas. The WHO places hepatoid, rhabdoid and sebaceous carcinoma of the thymus and undifferentiated large cell carcinoma with a Castleman disease-like reaction under Thymic carcinoma, NOS 8586/3 (Marx 2022, PDF p. 4, footnote g). ICD-O-3.2 also holds 8410/3 Sebaceous carcinoma and 8576/3 Hepatoid adenocarcinoma. The draft follows the WHO table. Confirm 8586/3.
6. A thymoma the report calls benign. The WHO treats every thymoma except micronodular thymoma with lymphoid stroma as malignant (Marx 2022, PDF p. 3), but ICD-O-3.2 keeps Thymoma, benign at 8580/0 and Rule F codes the behaviour the pathologist states. The draft excludes it as 8580/0. Confirm.
7. Neuroendocrine tumour, grade 3 of the thymus. ICD-O-3.2 lists Neuroendocrine tumor, grade 3 at 8249/3, while current WHO thoracic criteria designate these tumours large cell neuroendocrine carcinoma, 8013/3 (Marx 2022, PDF pp. 8-9). The draft records what the report states: 8249/3 for neuroendocrine tumour, grade 3 and 8013/3 for large cell neuroendocrine carcinoma. Confirm.
8. Thoracic SMARCA4-deficient undifferentiated tumour. It most often invades the mediastinum (Marx 2022, PDF p. 10); this part's sources print no code for it and ICD-O-3.2 holds no term. It is not built until you rule, after the lung part reports the code the WHO gives it.

## 11. Paediatric evidence added 8 October 2026

New source: Rossi 2022 (`XIf5-thymus-paediatric__Rossi-2022.txt`, PMC9497562), a review of 82 thymomas in patients under the age of eighteen. It was read through the snippet tool only. Every quote below was checked against its PMC section, ignoring case and whitespace. All six codes were checked in ICD-O-3.2: each has a current preferred term at /3 (8580/3 Thymoma, NOS; 8581/3 Thymoma, type A; 8582/3 Thymoma, type AB; 8583/3 Thymoma, type B1; 8584/3 Thymoma, type B2; 8585/3 Thymoma, type B3), and ICCC-2017 places each at C37.9 in XIf5.

| Entity | Before | After | Cite |
|---|---|---|---|
| Thymoma, type B1 (8583/3) | not_reported; picker | common; option 1 on `tm_histology` | Rossi 2022, PMC section 4: "20 (45%) type B1"; "Type B1 thymoma was the most frequent"; "Patients ranged in age from 0.9 to 17 years" |
| Thymoma, type B2 (8584/3) | not_reported; picker | occurs; option 2 on `tm_histology` | Rossi 2022, PMC section 4: "12 (27%) type B2"; "Patients ranged in age from 0.9 to 17 years" |
| Thymoma, type AB (8582/3) | not_reported; picker | occurs; option 3 on `tm_histology` | Rossi 2022, PMC section 4: "6 (14%) type AB"; "Patients ranged in age from 0.9 to 17 years" |
| Thymoma, type A, including atypical variant (8581/3) | not_reported; picker | occurs; option 4 on `tm_histology` | Rossi 2022, PMC section 4: "3 (7%) were WHO type A thymomas"; "Patients ranged in age from 0.9 to 17 years" |
| Thymoma, type B3 (8585/3) | not_reported; picker | occurs; option 5 on `tm_histology` | Rossi 2022, PMC section 4: "and 3 (7%) type B3"; "Patients ranged in age from 0.9 to 17 years" |
| Thymoma, NOS, including sclerosing thymoma (8580/3) | not_reported; picker | occurs; option 6 on `tm_histology` | Rossi 2022, PMC section 1: "Thirty-two articles involving 82 pediatric thymomas were included"; PMC section 4: "Of the 44 cases with WHO histopathological classification"; PMC section 3: "retained the original description of the thymoma type when a WHO histotype was not assigned" |

Consequential changes, each made because the six entries moved:

- `tm_histology`: the six thymoma options sit first, ordered by Rossi's counts (B1 20, B2 12, AB 6, A 3, B3 3 of 44 typed thymomas; A before B3 by code), then thymoma with no type named, then NUT carcinoma. The option that leads to the picker drops "a thymoma" and names metaplastic thymoma, which stays in the picker. The hint gains the picker's sentence on more than one thymoma type in one tumour.
- `tm_picker`: the six thymoma entries are removed, and its hint loses the sentence that moved. Metaplastic thymoma (8580/3) stays a picker entry: Rossi 2022 does not report it.
- Rule K (section 7), the 8580/3 code-currency row (section 8) and the lung conflict row (section 9) now name `tm_histology` for the thymoma entries.
- Data gap 1 now covers thymic carcinoma, thymic neuroendocrine tumours and metaplastic thymoma only; Rossi 2022 excluded the first two (PMC section 3). Registrar question 1 is narrowed to match.
- Data gaps 6, 7 and 8 are new: the Carcinoma, NOS option (8010/3) rests on no paediatric source and Rossi 2022 does not report it, so it stays as it is for the controller to decide; the place of NUT carcinoma among the thymoma options has no paediatric count behind it; and a combined thymic carcinoma and thymoma now spans two screens (registrar question 4).

Unchanged, because Rossi 2022 does not report them in children: NUT carcinoma (still "occurs" from Pfister 2022), every thymic carcinoma and thymic neuroendocrine entity, metaplastic thymoma, the four exclusions (micronodular thymoma with lymphoid stroma, microscopic thymoma, lipofibroadenoma, thymolipoma), and every referral. Rossi 2022 names no paediatric entity this part does not already list, so no entity was added.
