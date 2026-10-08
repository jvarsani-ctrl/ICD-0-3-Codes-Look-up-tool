# Group 11 evidence — XIf4 lung carcinoma, plus trachea-free pleura and other thoracic sites (XIf10)

Part `XIf4_lung_pleura`. Sites: lung and bronchus C34.0 to C34.9 (ICCC-3 XIf4); heart and pericardium C38.0, pleura C38.4, overlapping lesion C38.8, and C39.0, C39.8, C39.9 (ICCC-3 XIf10). The trachea (C33.9) and the mediastinum and thymus (C37.9, C38.1 to C38.3) belong to other parts. Built 8 October 2026 from the first six files below, read through the snippet tool only, with table cells read from the PDF page images. The same day two paediatric papers from PubMed Central, Ozkan 2024 and Chen 2026, were added, read through the snippet tool only (section 11).

**Headline.** The six WHO and ICCR files report no lung carcinoma in a child; the two paediatric papers do. Ozkan 2024 reports bronchial carcinoid as the commonest primary lung malignancy of children and mucoepidermoid carcinoma as the next, and lists adenocarcinoma, squamous cell carcinoma, small cell carcinoma and large cell carcinoma among them; Chen 2026 reports mucoepidermoid carcinoma and carcinoid tumour in its series of 36 children and names large cell neuroendocrine carcinoma. Under the registrar's ruling of 8 October 2026 these seven are now options on the lung histology screen, ahead of NUT carcinoma, and the other WHO lung carcinomas stay picker entries. Pleuropulmonary blastoma, the commonest primary lung tumour in Chen 2026's series, is still referred to Group XII, and a paraganglioma of the lung is referred to Group IV. The pleura has no carcinoma entity in Sauter 2022, the ICCR mesothelioma dataset or the two paediatric papers; its screen offers carcinoma, not otherwise specified, the general picker and the deposit routes, and refers mesothelioma to Group XII.

## 1. Sources

| File | Citation | WHO volume |
|---|---|---|
| `XIf4-lung__Nicholson-2022.txt` | Nicholson AG, Tsao MS, Beasley MB, et al. The 2021 WHO Classification of Lung Tumors: Impact of Advances Since 2015. J Thorac Oncol 2022;17(3):362-387. | WHO Classification of Tumours, Thoracic Tumours, 5th edition, 2021 |
| `XIf4-lung__ICCR-Lung-4th.txt` | International Collaboration on Cancer Reporting. Lung Cancer Histopathology Reporting Guide, 4th edition, version 4.0, April 2023. | WHO Classification of Tumours, Thoracic Tumours, 5th edition, 2021 |
| `XIf10-pleura__Sauter-2022.txt` | Sauter JL, Dacic S, Galateau-Salle F, et al. The 2021 WHO Classification of Tumors of the Pleura: Advances Since the 2015 Classification. J Thorac Oncol 2022;17(5):608-622. | WHO Classification of Tumours, Thoracic Tumours, 5th edition, 2021 |
| `XIf10-pleura__ICCR-Mesothelioma-3rd.txt` | International Collaboration on Cancer Reporting. Mesothelioma in the Pleura, Pericardium and Peritoneum Histopathology Reporting Guide, 3rd edition, version 3.1, September 2022. | WHO Classification of Tumours, Thoracic Tumours, 5th edition, 2021 |
| `ALL-paediatric-occurrence__Pfister-2022.txt` | Pfister SM, Reyes-Mugica M, Chan JKC, et al. A Summary of the Inaugural WHO Classification of Pediatric Tumors: Transitioning from the Optical into the Molecular Era. Cancer Discov 2022;12(2):331-355. | WHO Classification of Tumours, Paediatric Tumours, 5th edition, 2022 |
| `RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt` | World Health Organization. International Classification of Diseases for Oncology, 3rd edition, 1st revision (ICD-O-3.1), section 4, Coding guidelines, printed pp. 14-28. | Not a tumour classification: the ICD-O coding manual |
| `XIf4-lung-paediatric__Ozkan-2024.txt` | Ozkan M, et al. Pulmonary tumors in childhood. Turk Gogus Kalp Damar Cerrahisi Derg 2024. doi:10.5606/tgkdc.dergisi.2024.25863. PMC10995685. | not a WHO summary; paediatric evidence |
| `XIf4-lung-paediatric__Chen-2026.txt` | Chen Y, et al. Clinical and pathological analysis of pediatric patients with primary pulmonary tumors at a single center. Biomed Rep 2026. doi:10.3892/br.2026.2166. PMC13320230. | not a WHO summary; paediatric evidence |

Short names used below: Nicholson 2022 = `XIf4-lung__Nicholson-2022.txt`; ICCR Lung 2023 = `XIf4-lung__ICCR-Lung-4th.txt`; Sauter 2022 = `XIf10-pleura__Sauter-2022.txt`; ICCR Mesothelioma 2022 = `XIf10-pleura__ICCR-Mesothelioma-3rd.txt`; Pfister 2022 = `ALL-paediatric-occurrence__Pfister-2022.txt`; ICD-O-3 manual = `RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt`; Ozkan 2024 = `XIf4-lung-paediatric__Ozkan-2024.txt`; Chen 2026 = `XIf4-lung-paediatric__Chen-2026.txt`. The ICD-O-3 manual extract's PDF page 1 is printed page 14.

Topography names come from the vault list `Topography/C30-C39 RESPIRATORY SYSTEM AND INTRATHORACIC ORGANS.md`. Every code was checked in `icdo32.sqlite` and its ICCC-2017 group in `ICCC-2017.sqlite`.

## 2. Entities

Decision counts: exclusion 30, not_built 1, option 11, picker 26, refer 20, registrar 6.

| Entity (WHO term) | Code | ICD-O-3.2 term matched (level) | ICD-O-3.2 preferred term | Paediatric | Decision | Pages |
|---|---|---|---|---|---|---|
| NUT carcinoma | 8023/3 | NUT carcinoma (Synonym) | Nuclear protein in testis (NUT)-associated carcinoma | occurs | option | Pfister 2022, PDF p. 14; Nicholson 2022, PDF p. 3; Nicholson 2022, PDF p. 15 |
| Carcinoma, not otherwise specified | 8010/3 | Carcinoma, NOS (Preferred) | Carcinoma, NOS | not_reported | option | ICD-O-3 manual, PDF p. 6 (printed p. 19) |
| Melanoma (tumour of ectopic tissue in the lung) | 8720/3 | Melanoma, NOS (Synonym) | Malignant melanoma, NOS | not_reported | option | Nicholson 2022, PDF p. 3 |
| Typical carcinoid/neuroendocrine tumour, grade 1; carcinoid tumour, NOS/neuroendocrine tumour, NOS | 8240/3 | Typical carcinoid (Synonym) | Neuroendocrine tumor, NOS | common | option | Nicholson 2022, PDF p. 3; ICCR Lung 2023, PDF p. 11; Nicholson 2022, PDF p. 12; Pfister 2022, PDF p. 14; Ozkan 2024, PMC section 2; Chen 2026, PMC section 10 |
| Atypical carcinoid/neuroendocrine tumour, grade 2 | 8249/3 | Atypical carcinoid tumor (Synonym) | Neuroendocrine tumor, grade 2 | occurs | option | Nicholson 2022, PDF p. 3; ICCR Lung 2023, PDF p. 11; Nicholson 2022, PDF p. 12; Ozkan 2024, PMC section 2 |
| Mucoepidermoid carcinoma | 8430/3 | Mucoepidermoid carcinoma (Preferred) | Mucoepidermoid carcinoma | common | option | Nicholson 2022, PDF p. 3; ICCR Lung 2023, PDF p. 11; Pfister 2022, PDF p. 14; Ozkan 2024, PMC section 2; Chen 2026, PMC section 10; Chen 2026, PMC section 9 |
| Adenoid cystic carcinoma | 8200/3 | Adenoid cystic carcinoma (Preferred) | Adenoid cystic carcinoma | not_reported | picker | Nicholson 2022, PDF p. 3 |
| Epithelial-myoepithelial carcinoma | 8562/3 | Epithelial-myoepithelial carcinoma (Preferred) | Epithelial-myoepithelial carcinoma | not_reported | picker | Nicholson 2022, PDF p. 3 |
| Hyalinizing clear cell carcinoma | 8310/3 | Clear cell carcinoma, NOS (Synonym) | Clear cell adenocarcinoma, NOS | not_reported | picker | Nicholson 2022, PDF p. 3, table image; Nicholson 2022, PDF p. 18 |
| Small cell carcinoma | 8041/3 | Small cell carcinoma, NOS (Preferred) | Small cell carcinoma, NOS | occurs | option | Nicholson 2022, PDF p. 3; Ozkan 2024, PMC section 2; Chen 2026, PMC section 2 |
| Combined small cell carcinoma | 8045/3 | Combined small cell carcinoma (Preferred) | Combined small cell carcinoma | not_reported | picker | Nicholson 2022, PDF p. 3; Nicholson 2022, PDF p. 12 |
| Large cell neuroendocrine carcinoma; combined large cell neuroendocrine carcinoma | 8013/3 | Large cell neuroendocrine carcinoma (Preferred) | Large cell neuroendocrine carcinoma | occurs | option | Nicholson 2022, PDF p. 3; Nicholson 2022, PDF p. 13; Chen 2026, PMC section 2 |
| Minimally invasive adenocarcinoma, nonmucinous | 8256/3 | Minimally invasive adenocarcinoma, non-mucinous (Preferred) | Minimally invasive adenocarcinoma, non-mucinous | not_reported | picker | Nicholson 2022, PDF p. 2; ICCR Lung 2023, PDF p. 10; Nicholson 2022, PDF p. 5 |
| Minimally invasive adenocarcinoma, mucinous | 8257/3 | Minimally invasive adenocarcinoma, mucinous (Preferred) | Minimally invasive adenocarcinoma, mucinous | not_reported | picker | Nicholson 2022, PDF p. 2; ICCR Lung 2023, PDF p. 10 |
| Lepidic adenocarcinoma | 8250/3 | Lepidic adenocarcinoma (Preferred) | Lepidic adenocarcinoma | not_reported | picker | Nicholson 2022, PDF p. 2 |
| Acinar adenocarcinoma | 8551/3 | Acinar adenocarcinoma of lung (Related) | Acinar cell cystadenocarcinoma | not_reported | picker | Nicholson 2022, PDF p. 2 |
| Papillary adenocarcinoma | 8260/3 | Papillary adenocarcinoma, NOS (Preferred) | Papillary adenocarcinoma, NOS | not_reported | picker | Nicholson 2022, PDF p. 2 |
| Micropapillary adenocarcinoma | 8265/3 | Micropapillary adenocarcinoma (Related) | Micropapillary carcinoma, NOS | not_reported | picker | Nicholson 2022, PDF p. 2 |
| Solid adenocarcinoma | 8230/3 | Solid adenocarcinoma, NOS (Synonym) | Solid carcinoma, NOS | not_reported | picker | Nicholson 2022, PDF p. 2; Nicholson 2022, PDF p. 8 |
| Invasive mucinous adenocarcinoma | 8253/3 | Adenocarcinoma of lung, mucinous (Preferred) | Adenocarcinoma of lung, mucinous | not_reported | picker | Nicholson 2022, PDF p. 2; Nicholson 2022, PDF p. 9 |
| Mixed invasive mucinous and nonmucinous adenocarcinoma | 8254/3 | Adenocarcinoma of lung, mixed mucinous and non-mucinous (Preferred) | Adenocarcinoma of lung, mixed mucinous and non-mucinous | not_reported | picker | Nicholson 2022, PDF p. 2 |
| Colloid adenocarcinoma | 8480/3 | Colloid adenocarcinoma (Synonym) | Mucinous adenocarcinoma | not_reported | picker | Nicholson 2022, PDF p. 2 |
| Fetal adenocarcinoma | 8333/3 | Fetal adenocarcinoma (Preferred) | Fetal adenocarcinoma | not_reported | picker | Nicholson 2022, PDF p. 2; Nicholson 2022, PDF p. 10 |
| Adenocarcinoma, enteric type | 8144/3 | Adenocarcinoma, enteric (Synonym) | Adenocarcinoma, intestinal type | not_reported | picker | Nicholson 2022, PDF p. 2; Nicholson 2022, PDF p. 10 |
| Adenocarcinoma, NOS | 8140/3 | Adenocarcinoma, NOS (Preferred) | Adenocarcinoma, NOS | occurs | option | Nicholson 2022, PDF p. 2; Ozkan 2024, PMC section 2 |
| Squamous cell carcinoma, NOS | 8070/3 | Squamous cell carcinoma, NOS (Preferred) | Squamous cell carcinoma, NOS | occurs | option | Nicholson 2022, PDF p. 2; Ozkan 2024, PMC section 2 |
| Squamous cell carcinoma, keratinizing | 8071/3 | Squamous cell carcinoma, keratinizing, NOS (Preferred) | Squamous cell carcinoma, keratinizing, NOS | not_reported | picker | Nicholson 2022, PDF p. 2 |
| Squamous cell carcinoma, nonkeratinizing | 8072/3 | Squamous cell carcinoma, nonkeratinizing, NOS (Synonym) | Squamous cell carcinoma, large cell, nonkeratinizing, NOS | not_reported | picker | Nicholson 2022, PDF p. 2 |
| Basaloid squamous cell carcinoma | 8083/3 | Basaloid squamous cell carcinoma (Preferred) | Basaloid squamous cell carcinoma | not_reported | picker | Nicholson 2022, PDF p. 2 |
| Lymphoepithelial carcinoma | 8082/3 | Lymphoepithelial carcinoma (Preferred) | Lymphoepithelial carcinoma | not_reported | picker | Nicholson 2022, PDF p. 2; Nicholson 2022, PDF p. 14 |
| Large cell carcinoma | 8012/3 | Large cell carcinoma, NOS (Preferred) | Large cell carcinoma, NOS | occurs | option | Nicholson 2022, PDF p. 2; Nicholson 2022, PDF p. 5; Ozkan 2024, PMC section 2 |
| Adenosquamous carcinoma | 8560/3 | Adenosquamous carcinoma (Preferred) | Adenosquamous carcinoma | not_reported | picker | Nicholson 2022, PDF p. 2; ICD-O-3 manual, PDF p. 11 (printed p. 24) |
| Pleomorphic carcinoma | 8022/3 | Pleomorphic carcinoma (Preferred) | Pleomorphic carcinoma | not_reported | picker | Nicholson 2022, PDF p. 3 |
| Giant cell carcinoma | 8031/3 | Giant cell carcinoma (Preferred) | Giant cell carcinoma | not_reported | picker | Nicholson 2022, PDF p. 3 |
| Spindle cell carcinoma | 8032/3 | Spindle cell carcinoma, NOS (Preferred) | Spindle cell carcinoma, NOS | not_reported | picker | Nicholson 2022, PDF p. 3 |
| Sarcomatoid carcinomas (group heading) | 8033/3 | Sarcomatoid carcinoma (Synonym) | Pseudosarcomatous carcinoma | not_reported | picker | Nicholson 2022, PDF p. 2 |
| Nonsmall cell carcinoma, NOS (small biopsy and cytology term) | 8046/3 | Non-small cell carcinoma (Preferred) | Non-small cell carcinoma | not_reported | picker | Nicholson 2022, PDF p. 6, table image; Nicholson 2022, PDF p. 5 |
| Thoracic SMARCA4-deficient undifferentiated tumour | 8044/3 | none (none) | Small cell carcinoma, intermediate cell | not_reported | registrar | Nicholson 2022, PDF p. 3, table image; Nicholson 2022, PDF p. 3; Nicholson 2022, PDF p. 17; Sauter 2022, PDF p. 9 |
| Bronchioloalveolar carcinoma, non-mucinous (term retired by the WHO) | 8252/3 | Bronchiolo-alveolar carcinoma, non-mucinous (Preferred) | Bronchiolo-alveolar carcinoma, non-mucinous | not_reported | registrar | Nicholson 2022, PDF p. 9 |
| Alveolar adenocarcinoma (no WHO 2021 entity) | 8251/3 | Alveolar adenocarcinoma (Preferred) | Alveolar adenocarcinoma | occurs | not_built | Nicholson 2022, PDF p. 2; Chen 2026, PMC section 2 |
| Fetal lung interstitial tumour | none | none (none) | none | occurs | registrar | Pfister 2022, PDF p. 14 |
| Diffuse lymphangiomatosis | 9170/3 | none (none) | Lymphangiosarcoma | not_reported | registrar | Nicholson 2022, PDF p. 3, table image |
| Lymphangioleiomyomatosis | 9174/3 | none (none) | none | not_reported | registrar | Nicholson 2022, PDF p. 3, table image; Nicholson 2022, PDF p. 3 |
| Pleuropulmonary blastoma | 8973/3 | Pleuropulmonary blastoma (Preferred) | Pleuropulmonary blastoma | common | refer to Group 12 | Pfister 2022, PDF p. 14; Nicholson 2022, PDF p. 3; Chen 2026, PMC section 9; Ozkan 2024, PMC section 2 |
| Pulmonary blastoma | 8972/3 | Pulmonary blastoma (Preferred) | Pulmonary blastoma | occurs | refer to Group 12 | Nicholson 2022, PDF p. 3; ICCR Lung 2023, PDF p. 10; Chen 2026, PMC section 11; Chen 2026, PMC section 9; Ozkan 2024, PMC section 2 |
| Carcinosarcoma | 8980/3 | Carcinosarcoma, NOS (Preferred) | Carcinosarcoma, NOS | not_reported | refer to Group 12 | Nicholson 2022, PDF p. 3 |
| Myoepithelial carcinoma | 8982/3 | Myoepithelial carcinoma (Preferred) | Myoepithelial carcinoma | not_reported | refer to Group 12 | Nicholson 2022, PDF p. 3; ICCR Lung 2023, PDF p. 11 |
| MALT lymphoma | 9699/3 | Extranodal marginal zone lymphoma of mucosa-associated lymphoid tissue (Related) | Marginal zone B-cell lymphoma, NOS | not_reported | refer to Group 2 | Nicholson 2022, PDF p. 3 |
| Diffuse large B-cell lymphoma, NOS | 9680/3 | Diffuse large B-cell lymphoma, NOS (Preferred) | Diffuse large B-cell lymphoma, NOS | not_reported | refer to Group 2 | Nicholson 2022, PDF p. 3 |
| Langerhans cell histiocytosis | 9751/1 | Langerhans cell histiocytosis, NOS (Preferred) | Langerhans cell histiocytosis, NOS | occurs | refer to Group 2 | Nicholson 2022, PDF p. 3; Chen 2026, PMC section 11; Chen 2026, PMC section 9 |
| Erdheim-Chester disease | 9749/3 | Erdheim-Chester disease (Preferred) | Erdheim-Chester disease | not_reported | refer to Group 2 | Nicholson 2022, PDF p. 3 |
| Intimal sarcoma | 9137/3 | Intimal sarcoma (Preferred) | Intimal sarcoma | not_reported | refer to Group 9 | Nicholson 2022, PDF p. 3 |
| Pulmonary myxoid sarcoma with EWSR1-CREB1 fusion | 8842/3 | Pulmonary myxoid sarcoma with EWSR1-CREB1 translocation (Related) | Ossifying fibromyxoid tumor, malignant | not_reported | refer to Group 9 | Nicholson 2022, PDF p. 3 |
| PEComa, malignant | 8714/3 | PEComa, malignant (Synonym) | Perivascular epithelioid tumor, malignant | not_reported | refer to Group 9 | Nicholson 2022, PDF p. 3 |
| Primary pulmonary paraganglioma | 8693/3 | Extra-adrenal paraganglioma, NOS (Preferred) | Extra-adrenal paraganglioma, NOS | occurs | refer to Group 4 | Ozkan 2024, PMC section 2 |
| Hodgkin lymphoma | 9650/3 | Hodgkin lymphoma, NOS (Preferred) | Hodgkin lymphoma, NOS | occurs | refer to Group 2 | Chen 2026, PMC section 9; Chen 2026, PMC section 11 |
| Rhabdomyosarcoma | 8900/3 | Rhabdomyosarcoma, NOS (Preferred) | Rhabdomyosarcoma, NOS | occurs | refer to Group 9 | Chen 2026, PMC section 2 |
| Ewing sarcoma | 9364/3 | Ewing sarcoma (Preferred) | Ewing sarcoma | occurs | refer to Group 9 | Chen 2026, PMC section 9 |
| Alveolar soft part sarcoma | 9581/3 | Alveolar soft part sarcoma (Preferred) | Alveolar soft part sarcoma | occurs | refer to Group 9 | Chen 2026, PMC section 9; Chen 2026, PMC section 11 |
| Congenital peribronchial myofibroblastic tumour | 8827/1 | Congenital peribronchial myofibroblastic tumor (Synonym) | Myofibroblastic tumor, peribronchial | occurs | exclusion | Pfister 2022, PDF p. 14; Nicholson 2022, PDF p. 3 |
| Inflammatory myofibroblastic tumour | 8825/1 | Inflammatory myofibroblastic tumor (Synonym) | Myofibroblastic tumor, NOS | common | exclusion | Pfister 2022, PDF p. 6; Ozkan 2024, PMC section 2; Chen 2026, PMC section 2 |
| Adenocarcinoma in situ, nonmucinous | 8250/2 | Adenocarcinoma in situ of lung, non-mucinous (Preferred) | Adenocarcinoma in situ of lung, non-mucinous | not_reported | exclusion | Nicholson 2022, PDF p. 2; ICCR Lung 2023, PDF p. 10 |
| Adenocarcinoma in situ, mucinous | 8253/2 | Adenocarcinoma in situ of lung, mucinous (Preferred) | Adenocarcinoma in situ of lung, mucinous | not_reported | exclusion | Nicholson 2022, PDF p. 2 |
| Atypical adenomatous hyperplasia | 8250/0 | Atypical adenomatous hyperplasia (Preferred) | Atypical adenomatous hyperplasia | not_reported | exclusion | Nicholson 2022, PDF p. 2 |
| Squamous cell carcinoma in situ | 8070/2 | Squamous cell carcinoma in situ, NOS (Preferred) | Squamous cell carcinoma in situ, NOS | not_reported | exclusion | Nicholson 2022, PDF p. 2; ICCR Lung 2023, PDF p. 10 |
| Mild squamous dysplasia | 8077/0 | none (none) | Squamous intraepithelial neoplasia, low grade | not_reported | exclusion | Nicholson 2022, PDF p. 2 |
| Moderate or severe squamous dysplasia | 8077/2 | Squamous dysplasia, high grade (Synonym) | Squamous intraepithelial neoplasia, high grade | not_reported | exclusion | Nicholson 2022, PDF p. 2 |
| Squamous cell papilloma, NOS | 8052/0 | Squamous cell papilloma, NOS (Preferred) | Squamous cell papilloma, NOS | not_reported | exclusion | Nicholson 2022, PDF p. 2 |
| Squamous cell papilloma, inverted | 8053/0 | Squamous cell papilloma, inverted (Preferred) | Squamous cell papilloma, inverted | not_reported | exclusion | Nicholson 2022, PDF p. 2 |
| Glandular papilloma; papillary adenoma | 8260/0 | Glandular papilloma (Related) | Papillary adenoma, NOS | not_reported | exclusion | Nicholson 2022, PDF p. 2 |
| Mixed squamous cell and glandular papilloma | 8560/0 | Mixed squamous cell and glandular papilloma (Preferred) | Mixed squamous cell and glandular papilloma | not_reported | exclusion | Nicholson 2022, PDF p. 2 |
| Sclerosing pneumocytoma | 8832/0 | Sclerosing pneumocytoma (Related) | Dermatofibroma, NOS | occurs | exclusion | Nicholson 2022, PDF p. 2; Chen 2026, PMC section 9; Chen 2026, PMC section 11 |
| Alveolar adenoma | 8251/0 | Alveolar adenoma (Preferred) | Alveolar adenoma | not_reported | exclusion | Nicholson 2022, PDF p. 2 |
| Bronchiolar adenoma/ciliated muconodular papillary tumour | 8140/0 | none (none) | Adenoma, NOS | not_reported | exclusion | Nicholson 2022, PDF p. 2, table image; Nicholson 2022, PDF p. 15 |
| Mucinous cystadenoma | 8470/0 | Mucinous cystadenoma, NOS (Preferred) | Mucinous cystadenoma, NOS | not_reported | exclusion | Nicholson 2022, PDF p. 2 |
| Mucous gland adenoma | 8480/0 | Mucous gland adenoma (Related) | Mucinous adenoma | not_reported | exclusion | Nicholson 2022, PDF p. 2 |
| Pleomorphic adenoma | 8940/0 | Pleomorphic adenoma (Preferred) | Pleomorphic adenoma | not_reported | exclusion | Nicholson 2022, PDF p. 3 |
| Myoepithelioma | 8982/0 | Myoepithelioma, NOS (Preferred) | Myoepithelioma, NOS | not_reported | exclusion | Nicholson 2022, PDF p. 3 |
| Diffuse idiopathic neuroendocrine cell hyperplasia | 8040/0 | Diffuse idiopathic neuroendocrine cell hyperplasia (Related) | Tumorlet, benign | not_reported | exclusion | Nicholson 2022, PDF p. 3 |
| Pulmonary hamartoma | 8992/0 | Pulmonary hamartoma (Preferred) | Pulmonary hamartoma | occurs | exclusion | Nicholson 2022, PDF p. 3; Ozkan 2024, PMC section 2; Chen 2026, PMC section 11 |
| Chondroma | 9220/0 | Chondroma, NOS (Preferred) | Chondroma, NOS | not_reported | exclusion | Nicholson 2022, PDF p. 3 |
| PEComa, benign | 8714/0 | PEComa, benign (Synonym) | Perivascular epithelioid tumor, benign | not_reported | exclusion | Nicholson 2022, PDF p. 3 |
| Meningioma (tumour of ectopic tissue) | 9530/0 | Meningioma, NOS (Preferred) | Meningioma, NOS | not_reported | exclusion | Nicholson 2022, PDF p. 3 |
| Bronchial adenoma, NOS (older report term) | 8140/1 | Bronchial adenoma, NOS (Synonym) | Atypical adenoma | not_reported | exclusion | ICD-O-3 manual, PDF p. 7 (printed p. 20) |
| Mature teratoma | 9080/0 | Mature teratoma, NOS (Synonym) | Teratoma, benign | occurs | exclusion | Chen 2026, PMC section 11 |
| Localized mesothelioma; diffuse mesothelioma, NOS | 9050/3 | Mesothelioma, NOS (Synonym) | Mesothelioma, malignant | not_reported | refer to Group 12 | Sauter 2022, PDF p. 2; ICCR Mesothelioma 2022, PDF p. 9; Pfister 2022, PDF p. 13 |
| Sarcomatoid mesothelioma | 9051/3 | Sarcomatoid mesothelioma (Synonym) | Fibrous mesothelioma, malignant | not_reported | refer to Group 12 | Sauter 2022, PDF p. 2 |
| Epithelioid mesothelioma | 9052/3 | Epithelioid mesothelioma, NOS (Synonym) | Epithelioid mesothelioma, malignant | not_reported | refer to Group 12 | Sauter 2022, PDF p. 2 |
| Mesothelioma, biphasic | 9053/3 | Mesothelioma, biphasic, NOS (Synonym) | Mesothelioma, biphasic, malignant | not_reported | refer to Group 12 | Sauter 2022, PDF p. 2 |
| Well-differentiated papillary mesothelial tumour (pleura) | 9052/1 | Well differentiated papillary mesothelioma of pleura (Preferred) | Well differentiated papillary mesothelioma of pleura | not_reported | exclusion | Sauter 2022, PDF p. 2 |
| Well-differentiated papillary mesothelial tumour (pericardium) | 9052/0 | Well differentiated papillary mesothelioma (Related) | Epithelioid mesothelioma, benign | not_reported | exclusion | Sauter 2022, PDF p. 2; ICCR Mesothelioma 2022, PDF p. 5 |
| Adenomatoid tumour | 9054/0 | Adenomatoid tumor, NOS (Preferred) | Adenomatoid tumor, NOS | not_reported | exclusion | Sauter 2022, PDF p. 2; ICCR Mesothelioma 2022, PDF p. 9 |
| Mesothelioma in situ | 9050/2 | none (none) | none | not_reported | registrar | Sauter 2022, PDF p. 2; ICCR Mesothelioma 2022, PDF p. 13 |
| Cardiac rhabdomyoma | 8900/0 | Rhabdomyoma, NOS (Preferred) | Rhabdomyoma, NOS | occurs | exclusion | Pfister 2022, PDF p. 14 |

Why, for the entities whose decision is not self-evident:

- **NUT carcinoma** (8023/3, option). Pfister 2022 lists NUT carcinoma among the malignant tumours of children (head and neck section). Nicholson 2022 lists it among lung tumours, says it may be primary to the lung, and names young age as a reason to test for it. The NUT carcinoma part owns its full evidence; the lung histology screen offers it.
- **Carcinoma, not otherwise specified** (8010/3, option). The fallback code for a report that names a carcinoma without a type. The ICD-O-3 manual also gives 8010/3 at C80.9 for a carcinoma that has spread to the lung from an unknown site of origin.
- **Melanoma (tumour of ectopic tissue in the lung)** (8720/3, option). The WHO lists melanoma among lung tumours of ectopic tissue. The one melanoma tree that any site reaches records it (approach 3); the lung and pleural screens route there rather than code it.
- **Typical carcinoid/neuroendocrine tumour, grade 1; carcinoid tumour, NOS/neuroendocrine tumour, NOS** (8240/3, option). A WHO 2021 lung entity and the commonest primary lung carcinoma of children. Ozkan 2024 reports bronchial carcinoids as 42-63% of primary lung malignancies in the pediatric population and carcinoid tumour as the most common histology in a series of 301 children; Chen 2026 names carcinoid tumours, with pleuropulmonary blastoma, as the most prevalent primary malignant lung tumours of children and reports one case. An option: the lu_histology carcinoid entry leads to lu_carcinoid for the type. The WHO uses carcinoid tumour, NOS for small biopsy and cytology samples.
- **Atypical carcinoid/neuroendocrine tumour, grade 2** (8249/3, option). A WHO 2021 lung entity separated from typical carcinoid by mitotic count and necrosis. Ozkan 2024 reports typical and atypical bronchial carcinoids in children and says atypical bronchial carcinoids occur more frequently in children. An option, reached through the lu_histology carcinoid entry and lu_carcinoid.
- **Mucoepidermoid carcinoma** (8430/3, option). A WHO 2021 salivary gland-type lung tumour. Ozkan 2024 cites it as the second most common primary malignant lung tumour of children; Chen 2026 reports four cases in 36 children, the commonest carcinoma of that series. An option on lu_histology.
- **Small cell carcinoma** (8041/3, option). A WHO 2021 lung entity. Ozkan 2024 lists small cell carcinoma among the primary epithelial lung malignancies of children and calls it exceedingly rare in them; Chen 2026 names it among the neuroendocrine lung tumours of children. An option on lu_histology.
- **Large cell neuroendocrine carcinoma; combined large cell neuroendocrine carcinoma** (8013/3, option). A WHO 2021 lung entity. Chen 2026 names large cell neuroendocrine carcinoma among the neuroendocrine lung tumours of children; its series has no case. An option on lu_histology.
- **Adenocarcinoma, NOS** (8140/3, option). A WHO 2021 lung entity. Ozkan 2024 lists adenocarcinoma among the primary epithelial lung malignancies of children, says it is more common than squamous cell carcinoma in them, and cites series in which it is 8% and 10.3% of children's primary lung malignancies. An option on lu_histology for an adenocarcinoma with no subtype named; the WHO subtypes stay picker entries.
- **Squamous cell carcinoma, NOS** (8070/3, option). A WHO 2021 lung entity. Ozkan 2024 lists squamous cell carcinoma among the primary epithelial lung malignancies of children, less common than adenocarcinoma. An option on lu_histology for a squamous cell carcinoma with no subtype named; the keratinizing, non-keratinizing and basaloid subtypes stay picker entries.
- **Large cell carcinoma** (8012/3, option). A WHO 2021 lung entity. Ozkan 2024 lists large cell carcinoma among the primary epithelial lung malignancies of children, with the lowest incidence. An option on lu_histology.
- **Thoracic SMARCA4-deficient undifferentiated tumour** (8044/3, registrar). The WHO prints 8044/3 with a dagger (change in terminology of a previous code); the ICD-O-3.2 term at 8044/3 is Small cell carcinoma, intermediate cell. Nicholson 2022 describes adult smokers. Not built until the registrar rules (registrar question 3).
- **Bronchioloalveolar carcinoma, non-mucinous (term retired by the WHO)** (8252/3, registrar). ICD-O-3.2 keeps this preferred term current, but the WHO 2021 lung classification prints no entity at 8252. Nicholson 2022 says bronchioloalveolar carcinoma was defined as a noninvasive tumour, so an older report using the term may describe an adenocarcinoma in situ (/2). Registrar question 4.
- **Alveolar adenocarcinoma (no WHO 2021 entity)** (8251/3, not_built). Every /3 term at 8251 is [obs] in ICD-O-3.2. The WHO 2021 lung classification keeps only alveolar adenoma at 8251/0. Lung adenocarcinomas now sit at 8250/3 Lepidic adenocarcinoma, 8253/3 and 8254/3 by subtype; neither ICD-O-3.2 nor the WHO source names a successor for 8251/3. Chen 2026 names alveolar carcinoma, an [obs] ICD-O-3.2 synonym at this code, as an epithelial lung tumour of children. The code stays off every screen (data gap 7).
- **Fetal lung interstitial tumour** (no code, registrar). A paediatric lung tumour new in the WHO paediatric classification. Neither the files nor ICD-O-3.2 give it a code. The tree treats it as not registrable until the registrar rules (registrar question 5).
- **Diffuse lymphangiomatosis** (9170/3, registrar). The WHO prints 9170/3 with a dagger for diffuse lymphangiomatosis; the ICD-O-3.2 preferred term at 9170/3 is Lymphangiosarcoma, an ICCC Group IX code. Group IX decides; listed here because the clerk meets it in a lung report.
- **Lymphangioleiomyomatosis** (9174/3, registrar). The WHO prints 9174/3, a code the IARC/WHO committee approved in October 2020; ICD-O-3.2 holds only 9174/1 Lymphangioleiomyomatosis. A code the WHO prints and ICD-O-3.2 lacks goes to the registrar. It is not epithelial.
- **Pleuropulmonary blastoma** (8973/3, refer). Pfister 2022 lists it as a paediatric lung tumour. ICCC-2017 places 8973 in XIIa3 at every site, so it is referred to Group XII. Chen 2026 reports it as the most prevalent primary lung tumour in 36 children (16 cases), and Ozkan 2024 calls it a childhood tumour.
- **Pulmonary blastoma** (8972/3, refer). A WHO sarcomatoid carcinoma of the lung, but ICCC-2017 places 8972 in XIIa3 at every site. Chen 2026 reports two cases in children, and Ozkan 2024 cites a series of 301 children in which pulmonary blastoma was 22.3% of primary lung malignancies.
- **Langerhans cell histiocytosis** (9751/1, refer). A histiocytic tumour; the Group II screens decide its behaviour and whether it registers. Chen 2026 reports two cases of Langerhans cell histiocytosis of the lung in children, counted there among the benign tumours.
- **Primary pulmonary paraganglioma** (8693/3, refer). Ozkan 2024 reports a functioning primary pulmonary paraganglioma in a child and lists paraganglioma among children's benign lung tumours. ICD-O-3.2 codes every paraganglioma /3 (8680/3 Paraganglioma, NOS; 8693/3 Extra-adrenal paraganglioma, NOS), and ICCC-2017 places both in IVb at every site, so it is referred to Group IV, whose screens choose the code. Ozkan 2024 says it can mimic a carcinoid tumour.
- **Hodgkin lymphoma** (9650/3, refer). Chen 2026 reports a Hodgkin lymphoma of the lung in a child. ICCC-2017 places 9650 in IIa at every site; the lu_histology lymphoma option refers it to Group II.
- **Rhabdomyosarcoma** (8900/3, refer). Chen 2026 names rhabdomyosarcoma among the mesenchymal primary lung tumours of children; its series has no case. ICCC-2017 places 8900 in IXa at every site; the lu_histology sarcoma option refers it to Group IX.
- **Ewing sarcoma** (9364/3, refer). Chen 2026 reports an Ewing sarcoma of the lung with an EWSR1-FLI1 fusion in a child. ICCC-2017 places 9364 in IXd2 away from bone (VIIIc2 only at C40-C41); the lu_histology sarcoma option refers it to Group IX.
- **Alveolar soft part sarcoma** (9581/3, refer). Chen 2026 reports an alveolar soft part sarcoma of the lung in a child. ICCC-2017 places 9581 in IXd10 at every site; the lu_histology sarcoma option refers it to Group IX.
- **Inflammatory myofibroblastic tumour** (8825/1, exclusion). Pfister 2022 lists it among children's myofibroblastic tumours without naming a site. ICD-O-3.2 gives it /1; the malignant 8825/3 is Myofibroblastic sarcoma, a Group IX code. Ozkan 2024 reports it as more than half of children's benign lung tumours; Chen 2026 names it among the mesenchymal lung tumours of children.
- **Sclerosing pneumocytoma** (8832/0, exclusion). Benign (/0); ICD-O-3.2 lists it as a Related term under Dermatofibroma, NOS. Chen 2026 reports four cases in 36 children.
- **Pulmonary hamartoma** (8992/0, exclusion). Benign (/0). Ozkan 2024 lists it among children's benign lung tumours and says it is much rarer in children than in adults; Chen 2026 reports three cases in children.
- **Mature teratoma** (9080/0, exclusion). Chen 2026 reports a mature teratoma of the lung in a child, counted there among the benign tumours. Benign (/0); ICCC-2017 holds 9080 at the lung only at behaviour /3 (Xb2). No lung screen offers it (data gap 8).
- **Mesothelioma in situ** (9050/2, registrar). The WHO prints 9050/2, a code the IARC/WHO committee approved in October 2020; ICD-O-3.2 holds no 9050/2. It is not a malignant (/3) tumour. The tree shows it as not registrable until the registrar rules (question 5).

## 3. The pathway

Lung cases enter at `lu_site`; pleural, cardiac and other thoracic cases at `pl_site`. Nodes named `site_capture`, `mel_site`, `gc_picker` and `thymus_tree` belong to other parts: the shared site capture, the melanoma tree (`mel_site` in the XId evidence), the general carcinoma tree's long-tail list (`sk_carcinoma_other` in the XIe evidence), and the thymus and mediastinum tree. The controller wires them.

### `lu_site` (site_resolution)

**Question:** Which part of the lung or bronchus does the report name as the site of the tumour?

**Hint:** Choose a lobe only when the report places the tumour in it. When one tumour spans two or more lobes and the report does not say where it began, choose the overlapping lesion of the lung.

| Option | Outcome | Records | Reason shown | Recognition aid | Pages |
|---|---|---|---|---|---|
| Main bronchus, carina or hilum of the lung | go | site C34.0; go to `lu_evidence` | Site recorded as Main bronchus (C34.0). |  |  |
| Upper lobe or lingula | go | site C34.1; go to `lu_evidence` | Site recorded as Upper lobe, lung (C34.1). |  | ICD-O-3 manual, PDF p. 7 (printed p. 20) |
| Middle lobe | go | site C34.2; go to `lu_evidence` | Site recorded as Middle lobe, lung (C34.2). |  |  |
| Lower lobe | go | site C34.3; go to `lu_evidence` | Site recorded as Lower lobe, lung (C34.3). |  |  |
| More than one lobe, and the report does not say where the tumour began | go | site C34.8; go to `lu_evidence` | Site recorded as Overlapping lesion of lung (C34.8). |  | ICD-O-3 manual, PDF p. 5 (printed p. 18) |
| Lung or bronchus, with no lobe named | go | site C34.9; go to `lu_evidence` | Site recorded as Lung, NOS (C34.9). |  |  |
| The lung together with the pleura, chest wall or mediastinum, and the report does not say where the tumour began | go | site C39.8; go to `pl_evidence` | Site recorded as Overlapping lesion of respiratory system and intrathoracic organs (C39.8). |  | ICD-O-3 manual, PDF p. 5 (printed p. 18) |
| The pleura only, with no tumour inside the lung | go | go to `pl_site` | A tumour of the pleura is recorded through the pleural screens. |  |  |
| Beside the lung or a bronchus (for example paratracheal or peribronchial), with no organ named as the site | go | go to `site_capture`, site recaptured | Rule B: a site with a prefix such as para- or peri- that ICD-O does not list is coded to an ill-defined site (C76) unless the tumour type shows the tissue it arose in. The next screen records the site. |  | ICD-O-3 manual, PDF p. 1 (printed p. 14) |

### `lu_evidence` (document_inventory)

**Question:** What is in the file for this lung tumour?

**Hint:** Choose the strongest report in the file. A radiology report counts as imaging. Cytology of sputum, a bronchial washing or brushing, or a needle aspirate counts as cytology. A biopsy or resection report counts as histology. A report that calls the tumour possible, probable or suspected cancer does not register it.

| Option | Outcome | Records | Reason shown | Recognition aid | Pages |
|---|---|---|---|---|---|
| A referral letter or clinical note only, stating a malignant lung tumour | code | 8000/3, basis 1 | Recorded as Neoplasm, malignant (8000/3), basis of diagnosis clinical. |  |  |
| An imaging report only, such as a chest X-ray, computed tomography or magnetic resonance imaging | code | 8000/3, basis 2 | Recorded as Neoplasm, malignant (8000/3), basis of diagnosis imaging. |  |  |
| Imaging that shows a lung tumour, with a chromogranin A, serotonin or adrenocorticotropic hormone (ACTH) result | go | go to `lu_lab` | The laboratory result decides whether the case can be recorded without tissue. |  |  |
| A note or report that calls the tumour possible, probable or suspected cancer only | not_registrable | nothing registered | A possible or suspected cancer is not registered. |  |  |
| A cytology report (sputum, bronchial washing or brushing, or a needle aspirate) | go | go to `lu_cytology` (basis 5) |  |  |  |
| A histology report on a biopsy or resection, with or without immunohistochemistry or gene reports | go | go to `lu_histology` (basis 7) |  |  |  |

### `lu_lab` (lab_results)

**Question:** Which result does the file give with the imaging that shows the lung tumour?

**Hint:** A raised result counts only when imaging shows a tumour. A raised marker with no tumour on imaging is not registrable.

| Option | Outcome | Records | Reason shown | Recognition aid | Pages |
|---|---|---|---|---|---|
| Raised chromogranin A | code | 8240/3, basis 4 | Recorded as Neuroendocrine tumor, NOS (8240/3), basis of diagnosis tumour marker. |  |  |
| Raised serotonin | code | 8241/3, basis 4 | Recorded as Enterochromaffin cell carcinoid (8241/3), basis of diagnosis tumour marker. |  |  |
| Raised adrenocorticotropic hormone (ACTH) | code | 8158/3, basis 4 | Recorded as ACTH-producing tumor (8158/3), basis of diagnosis tumour marker. |  |  |
| None of these is raised, or the result is not given | code | 8000/3, basis 2 | Recorded as Neoplasm, malignant (8000/3), basis of diagnosis imaging. |  |  |

### `lu_cytology` (morphology_only)

**Question:** What does the cytology report call the tumour?

**Hint:** Code a carcinoma only when the report states one. Suspicious or atypical cells are not a diagnosis of cancer. Cytology does not use the terms adenocarcinoma in situ or minimally invasive adenocarcinoma.

| Option | Outcome | Records | Reason shown | Recognition aid | Pages |
|---|---|---|---|---|---|
| A named carcinoma or neuroendocrine tumour type, such as carcinoid tumour, small cell carcinoma or non-small cell carcinoma | go | go to `lu_histology` (basis 5) |  |  | Nicholson 2022, PDF p. 5 |
| Carcinoma, with no type named | code | 8010/3, basis 5 | Recorded as Carcinoma, NOS (8010/3) on cytology. |  |  |
| Malignant cells, with no tumour type named | code | 8000/3, basis 5 | Recorded as Neoplasm, malignant (8000/3) on cytology. |  |  |
| Lymphoma | refer | Group 2 | Lymphoma is coded in Group II, lymphomas and reticuloendothelial neoplasms. |  |  |
| Suspicious for malignancy, atypical, benign, or non-diagnostic | not_registrable | nothing registered | The cytology report does not state a malignant tumour, so nothing is registered. |  |  |

### `lu_histology` (histology_subclassification)

**Question:** What does the histology report call the tumour?

**Hint:** Choose the name in the report's diagnosis line. A tumour that the report says has spread to the lung from another organ is coded at the organ where it began.

NOS fallback: 8010/3.

| Option | Outcome | Records | Reason shown | Recognition aid | Pages |
|---|---|---|---|---|---|
| Carcinoid tumour, typical or atypical carcinoid, or neuroendocrine tumour | go | go to `lu_carcinoid` |  |  | Nicholson 2022, PDF p. 3; Ozkan 2024, PMC section 2; Chen 2026, PMC section 10 |
| Mucoepidermoid carcinoma | code | 8430/3, basis 7 | Recorded as Mucoepidermoid carcinoma (8430/3). | Reports describe a mix of mucus-secreting, squamous and intermediate cells. | Nicholson 2022, PDF p. 3; Ozkan 2024, PMC section 2; Chen 2026, PMC section 10 |
| Adenocarcinoma, with no subtype named | code | 8140/3, basis 7 | Recorded as Adenocarcinoma, NOS (8140/3). |  | Nicholson 2022, PDF p. 2; Ozkan 2024, PMC section 2 |
| Squamous cell carcinoma, with no subtype named | code | 8070/3, basis 7 | Recorded as Squamous cell carcinoma, NOS (8070/3). |  | Nicholson 2022, PDF p. 2; Ozkan 2024, PMC section 2 |
| Small cell carcinoma | code | 8041/3, basis 7 | Recorded as Small cell carcinoma, NOS (8041/3). |  | Nicholson 2022, PDF p. 3; Ozkan 2024, PMC section 2; Chen 2026, PMC section 2 |
| Large cell carcinoma | code | 8012/3, basis 7 | Recorded as Large cell carcinoma, NOS (8012/3). |  | Nicholson 2022, PDF p. 2; Ozkan 2024, PMC section 2 |
| Large cell neuroendocrine carcinoma, including combined large cell neuroendocrine carcinoma | code | 8013/3, basis 7 | Recorded as Large cell neuroendocrine carcinoma (8013/3). | A tumour that looks like a carcinoid but has a mitotic count above the atypical carcinoid range is called large cell neuroendocrine carcinoma. | Nicholson 2022, PDF p. 3; Nicholson 2022, PDF p. 13; Chen 2026, PMC section 2 |
| NUT carcinoma (NUT midline carcinoma) | code | 8023/3, basis 7 | Recorded as Nuclear protein in testis (NUT)-associated carcinoma (8023/3). | Reports describe sheets of poorly differentiated cells with small squamous nests, and nuclear NUT staining or a NUTM1 rearrangement. | Nicholson 2022, PDF p. 3; Nicholson 2022, PDF p. 15; Pfister 2022, PDF p. 14 |
| Pleuropulmonary blastoma | refer | Group 12 | Pleuropulmonary blastoma (8973/3) is coded in Group XII, other and unspecified malignant tumours. |  | Pfister 2022, PDF p. 14; Nicholson 2022, PDF p. 3 |
| Pulmonary blastoma | refer | Group 12 | Pulmonary blastoma (8972/3) is coded in Group XII, other and unspecified malignant tumours. | Pulmonary blastoma and pleuropulmonary blastoma are different tumours; choose the one the report names. | Nicholson 2022, PDF p. 3 |
| Paraganglioma | refer | Group 4 | Paraganglioma, NOS (8680/3) and Extra-adrenal paraganglioma, NOS (8693/3) are coded in Group IV, neuroblastoma and other peripheral nervous cell tumours. | Paraganglioma and carcinoid tumour can look alike; choose the one the report names. | Ozkan 2024, PMC section 2 |
| Carcinosarcoma | refer | Group 12 | Carcinosarcoma, NOS (8980/3) is coded in Group XII, other and unspecified malignant tumours. |  | Nicholson 2022, PDF p. 3 |
| Myoepithelial carcinoma | refer | Group 12 | Myoepithelial carcinoma (8982/3) is coded in Group XII, other and unspecified malignant tumours. |  | Nicholson 2022, PDF p. 3 |
| Melanoma | go | go to `mel_site` | Melanoma is recorded through the melanoma screens, which ask where it began. |  | Nicholson 2022, PDF p. 3 |
| Lymphoma, Langerhans cell histiocytosis or Erdheim-Chester disease | refer | Group 2 | Lymphomas and histiocytic tumours are coded in Group II, lymphomas and reticuloendothelial neoplasms. |  | Nicholson 2022, PDF p. 3 |
| A sarcoma, such as intimal sarcoma, pulmonary myxoid sarcoma or malignant perivascular epithelioid tumour (PEComa) | refer | Group 9 | Soft-tissue sarcomas are coded in Group IX, soft-tissue and other extraosseous sarcomas. |  | Nicholson 2022, PDF p. 3; ICCR Lung 2023, PDF p. 6 |
| Congenital peribronchial myofibroblastic tumour | exclude | 8827/1 | Not registered: Myofibroblastic tumor, peribronchial (8827/1) is not a malignant tumour. |  | Nicholson 2022, PDF p. 3 |
| Inflammatory myofibroblastic tumour | exclude | 8825/1 | Not registered: Myofibroblastic tumor, NOS (8825/1) is not a malignant tumour. |  | Pfister 2022, PDF p. 6 |
| Fetal lung interstitial tumour | not_registrable | nothing registered | Fetal lung interstitial tumour has no malignant code in ICD-O-3.2, so it is not registered. |  | Pfister 2022, PDF p. 14 |
| A deposit (metastasis) of a tumour that began in another organ | go | go to `site_capture`, site recaptured | A deposit is coded at the site where the tumour began. The next screen asks for that site. |  | Nicholson 2022, PDF p. 6; ICCR Lung 2023, PDF p. 16 |
| A carcinoma that the report says has spread to the lung, and the organ where it began is not known | code | 8010/3, basis 7, site C80.9 | Recorded as Carcinoma, NOS (8010/3) at unknown primary site (C80.9). |  | ICD-O-3 manual, PDF p. 6 (printed p. 19) |
| Carcinoma, with no type named | code | 8010/3, basis 7 | Recorded as Carcinoma, NOS (8010/3). |  |  |
| Another carcinoma or neuroendocrine tumour the report names | go | go to `lu_picker` |  |  |  |
| A benign tumour, a precursor lesion or an in situ carcinoma, such as adenocarcinoma in situ, a papilloma, a hamartoma or sclerosing pneumocytoma | go | go to `lu_not_malignant` |  |  |  |
| A malignant tumour, with no type named | code | 8000/3, basis 7 | Recorded as Neoplasm, malignant (8000/3). |  |  |

### `lu_picker` (morphology_only)

**Question:** Which carcinoma or neuroendocrine tumour does the report name?

**Hint:** Type part of the report's term to filter the list. When one tumour shows two types and no entry names both, choose the one with the higher code number. If a compound name is not found, search for its parts in the other order.

NOS fallback: 8010/3.

| Option | Outcome | Records | Reason shown | Recognition aid | Pages |
|---|---|---|---|---|---|
| Adenoid cystic carcinoma | code | 8200/3, basis 7 | Recorded as Adenoid cystic carcinoma (8200/3). |  | Nicholson 2022, PDF p. 3 |
| Epithelial-myoepithelial carcinoma | code | 8562/3, basis 7 | Recorded as Epithelial-myoepithelial carcinoma (8562/3). |  | Nicholson 2022, PDF p. 3 |
| Hyalinizing clear cell carcinoma | code | 8310/3, basis 7 | Recorded as Clear cell adenocarcinoma, NOS (8310/3). |  | Nicholson 2022, PDF p. 3, table image |
| Combined small cell carcinoma (small cell carcinoma with adenocarcinoma, squamous cell carcinoma or large cell carcinoma) | code | 8045/3, basis 7 | Recorded as Combined small cell carcinoma (8045/3). |  | Nicholson 2022, PDF p. 3; Nicholson 2022, PDF p. 12 |
| Minimally invasive adenocarcinoma, non-mucinous | code | 8256/3, basis 7 | Recorded as Minimally invasive adenocarcinoma, non-mucinous (8256/3). | Reports use this term on a resection, for a small lepidic tumour with an invasive focus under 5 mm. | Nicholson 2022, PDF p. 2; Nicholson 2022, PDF p. 9 |
| Minimally invasive adenocarcinoma, mucinous | code | 8257/3, basis 7 | Recorded as Minimally invasive adenocarcinoma, mucinous (8257/3). |  | Nicholson 2022, PDF p. 2 |
| Lepidic adenocarcinoma | code | 8250/3, basis 7 | Recorded as Lepidic adenocarcinoma (8250/3). |  | Nicholson 2022, PDF p. 2 |
| Acinar adenocarcinoma | code | 8551/3, basis 7 | Recorded as Acinar adenocarcinoma of lung (8551/3). |  | Nicholson 2022, PDF p. 2 |
| Papillary adenocarcinoma | code | 8260/3, basis 7 | Recorded as Papillary adenocarcinoma, NOS (8260/3). |  | Nicholson 2022, PDF p. 2 |
| Micropapillary adenocarcinoma | code | 8265/3, basis 7 | Recorded as Micropapillary carcinoma, NOS (8265/3). |  | Nicholson 2022, PDF p. 2 |
| Solid adenocarcinoma | code | 8230/3, basis 7 | Recorded as Solid carcinoma, NOS (8230/3). |  | Nicholson 2022, PDF p. 2 |
| Invasive mucinous adenocarcinoma | code | 8253/3, basis 7 | Recorded as Adenocarcinoma of lung, mucinous (8253/3). |  | Nicholson 2022, PDF p. 2 |
| Mixed invasive mucinous and non-mucinous adenocarcinoma | code | 8254/3, basis 7 | Recorded as Adenocarcinoma of lung, mixed mucinous and non-mucinous (8254/3). |  | Nicholson 2022, PDF p. 2 |
| Colloid adenocarcinoma | code | 8480/3, basis 7 | Recorded as Mucinous adenocarcinoma (8480/3). |  | Nicholson 2022, PDF p. 2 |
| Fetal adenocarcinoma, low grade or high grade | code | 8333/3, basis 7 | Recorded as Fetal adenocarcinoma (8333/3). | Reports of the low-grade form describe morules and nuclear beta-catenin staining. | Nicholson 2022, PDF p. 2; Nicholson 2022, PDF p. 10 |
| Enteric-type adenocarcinoma | code | 8144/3, basis 7 | Recorded as Adenocarcinoma, intestinal type (8144/3). | Reports use this name only after a bowel primary has been ruled out clinically. | Nicholson 2022, PDF p. 2; Nicholson 2022, PDF p. 10 |
| Keratinizing squamous cell carcinoma | code | 8071/3, basis 7 | Recorded as Squamous cell carcinoma, keratinizing, NOS (8071/3). |  | Nicholson 2022, PDF p. 2 |
| Non-keratinizing squamous cell carcinoma | code | 8072/3, basis 7 | Recorded as Squamous cell carcinoma, large cell, nonkeratinizing, NOS (8072/3). |  | Nicholson 2022, PDF p. 2 |
| Basaloid squamous cell carcinoma | code | 8083/3, basis 7 | Recorded as Basaloid squamous cell carcinoma (8083/3). |  | Nicholson 2022, PDF p. 2 |
| Lymphoepithelial carcinoma (formerly lymphoepithelial-like carcinoma) | code | 8082/3, basis 7 | Recorded as Lymphoepithelial carcinoma (8082/3). |  | Nicholson 2022, PDF p. 2; Nicholson 2022, PDF p. 14 |
| Adenosquamous carcinoma (mixed adenocarcinoma and squamous cell carcinoma) | code | 8560/3, basis 7 | Recorded as Adenosquamous carcinoma (8560/3). |  | Nicholson 2022, PDF p. 2; ICD-O-3 manual, PDF p. 11 (printed p. 24) |
| Pleomorphic carcinoma | code | 8022/3, basis 7 | Recorded as Pleomorphic carcinoma (8022/3). |  | Nicholson 2022, PDF p. 3 |
| Giant cell carcinoma | code | 8031/3, basis 7 | Recorded as Giant cell carcinoma (8031/3). |  | Nicholson 2022, PDF p. 3 |
| Spindle cell carcinoma | code | 8032/3, basis 7 | Recorded as Spindle cell carcinoma, NOS (8032/3). |  | Nicholson 2022, PDF p. 3 |
| Sarcomatoid carcinoma, with no subtype named | code | 8033/3, basis 7 | Recorded as Pseudosarcomatous carcinoma (8033/3). |  | Nicholson 2022, PDF p. 2 |
| Non-small cell carcinoma, with no type named, including one the report says favours a type | code | 8046/3, basis 7 | Recorded as Non-small cell carcinoma (8046/3). A report that says the carcinoma favours a type has not stated that type as the diagnosis. |  | Nicholson 2022, PDF p. 6, table image; Nicholson 2022, PDF p. 5 |

### `lu_carcinoid` (histology_subclassification)

**Question:** Which neuroendocrine tumour does the report name?

**Hint:** When the report gives both typical and atypical carcinoid features, choose atypical carcinoid: the higher grade is recorded. A small biopsy or cytology report may call the tumour carcinoid tumour, not otherwise specified.

| Option | Outcome | Records | Reason shown | Recognition aid | Pages |
|---|---|---|---|---|---|
| Typical carcinoid, or neuroendocrine tumour grade 1 | code | 8240/3, basis 7 | Recorded as Neuroendocrine tumor, NOS (8240/3). ICD-O-3.2 gives Typical carcinoid as a synonym of this code. |  | Nicholson 2022, PDF p. 3; ICCR Lung 2023, PDF p. 11; Ozkan 2024, PMC section 2 |
| Atypical carcinoid, or neuroendocrine tumour grade 2 | code | 8249/3, basis 7 | Recorded as Neuroendocrine tumor, grade 2 (8249/3). ICD-O-3.2 gives Atypical carcinoid tumor as a synonym of this code. | Reports separate atypical from typical carcinoid by a higher mitotic count or by necrosis. | Nicholson 2022, PDF p. 3; Nicholson 2022, PDF p. 12; Ozkan 2024, PMC section 2 |
| Carcinoid tumour or neuroendocrine tumour, with no type or grade stated, or bronchial adenoma of carcinoid type | code | 8240/3, basis 7 | Recorded as Neuroendocrine tumor, NOS (8240/3). |  | Nicholson 2022, PDF p. 3; Nicholson 2022, PDF p. 12; Chen 2026, PMC section 11 |
| A tumour with carcinoid appearance that the report calls large cell neuroendocrine carcinoma | code | 8013/3, basis 7 | Recorded as Large cell neuroendocrine carcinoma (8013/3). |  | Nicholson 2022, PDF p. 13 |

### `lu_not_malignant` (histology_subclassification)

**Question:** Which non-malignant tumour or lesion does the report name?

**Hint:** These are benign, uncertain or in situ tumours, and Group XI registers malignant tumours only. If the report also names an invasive carcinoma, go back and choose that. If the pathologist states that one of these tumours is malignant, the stated behaviour is recorded: go back and choose the malignant tumour the report names.

| Option | Outcome | Records | Reason shown | Recognition aid | Pages |
|---|---|---|---|---|---|
| Adenocarcinoma in situ, non-mucinous | exclude | 8250/2 | Not registered: Adenocarcinoma in situ of lung, non-mucinous (8250/2) is not a malignant tumour. |  | Nicholson 2022, PDF p. 2 |
| Adenocarcinoma in situ, mucinous | exclude | 8253/2 | Not registered: Adenocarcinoma in situ of lung, mucinous (8253/2) is not a malignant tumour. |  | Nicholson 2022, PDF p. 2 |
| Atypical adenomatous hyperplasia | exclude | 8250/0 | Not registered: Atypical adenomatous hyperplasia (8250/0) is not a malignant tumour. |  | Nicholson 2022, PDF p. 2 |
| Squamous cell carcinoma in situ | exclude | 8070/2 | Not registered: Squamous cell carcinoma in situ, NOS (8070/2) is not a malignant tumour. |  | Nicholson 2022, PDF p. 2 |
| Mild squamous dysplasia | exclude | 8077/0 | Not registered: Squamous intraepithelial neoplasia, low grade (8077/0) is not a malignant tumour. |  | Nicholson 2022, PDF p. 2 |
| Moderate or severe squamous dysplasia | exclude | 8077/2 | Not registered: Squamous intraepithelial neoplasia, high grade (8077/2) is not a malignant tumour. |  | Nicholson 2022, PDF p. 2 |
| Squamous cell papilloma | exclude | 8052/0 | Not registered: Squamous cell papilloma, NOS (8052/0) is not a malignant tumour. |  | Nicholson 2022, PDF p. 2 |
| Inverted squamous cell papilloma | exclude | 8053/0 | Not registered: Squamous cell papilloma, inverted (8053/0) is not a malignant tumour. |  | Nicholson 2022, PDF p. 2 |
| Glandular papilloma or papillary adenoma | exclude | 8260/0 | Not registered: Papillary adenoma, NOS (8260/0) is not a malignant tumour. |  | Nicholson 2022, PDF p. 2 |
| Mixed squamous cell and glandular papilloma | exclude | 8560/0 | Not registered: Mixed squamous cell and glandular papilloma (8560/0) is not a malignant tumour. |  | Nicholson 2022, PDF p. 2 |
| Sclerosing pneumocytoma | exclude | 8832/0 | Not registered: ICD-O-3.2 lists Sclerosing pneumocytoma under Dermatofibroma, NOS (8832/0), a benign tumour. |  | Nicholson 2022, PDF p. 2 |
| Alveolar adenoma | exclude | 8251/0 | Not registered: Alveolar adenoma (8251/0) is not a malignant tumour. |  | Nicholson 2022, PDF p. 2 |
| Bronchiolar adenoma or ciliated muconodular papillary tumour | exclude | 8140/0 | Not registered: Adenoma, NOS (8140/0) is not a malignant tumour. |  | Nicholson 2022, PDF p. 2, table image |
| Mucinous cystadenoma | exclude | 8470/0 | Not registered: Mucinous cystadenoma, NOS (8470/0) is not a malignant tumour. |  | Nicholson 2022, PDF p. 2 |
| Mucous gland adenoma | exclude | 8480/0 | Not registered: Mucinous adenoma (8480/0) is not a malignant tumour. |  | Nicholson 2022, PDF p. 2 |
| Pleomorphic adenoma | exclude | 8940/0 | Not registered: Pleomorphic adenoma (8940/0) is not a malignant tumour. |  | Nicholson 2022, PDF p. 3 |
| Myoepithelioma | exclude | 8982/0 | Not registered: Myoepithelioma, NOS (8982/0) is not a malignant tumour. |  | Nicholson 2022, PDF p. 3 |
| Diffuse idiopathic neuroendocrine cell hyperplasia, or a tumourlet | exclude | 8040/0 | Not registered: Tumorlet, benign (8040/0) is not a malignant tumour. |  | Nicholson 2022, PDF p. 3 |
| Pulmonary hamartoma | exclude | 8992/0 | Not registered: Pulmonary hamartoma (8992/0) is not a malignant tumour. |  | Nicholson 2022, PDF p. 3 |
| Chondroma | exclude | 9220/0 | Not registered: Chondroma, NOS (9220/0) is not a malignant tumour. |  | Nicholson 2022, PDF p. 3 |
| Benign perivascular epithelioid tumour (PEComa) | exclude | 8714/0 | Not registered: Perivascular epithelioid tumor, benign (8714/0) is not a malignant tumour. |  | Nicholson 2022, PDF p. 3 |
| Meningioma | exclude | 9530/0 | Not registered: Meningioma, NOS (9530/0) is not a malignant tumour. |  | Nicholson 2022, PDF p. 3 |
| Bronchial adenoma, with no type named | exclude | 8140/1 | Not registered: ICD-O-3.2 codes Bronchial adenoma, NOS to Atypical adenoma (8140/1), uncertain behaviour. |  | ICD-O-3 manual, PDF p. 7 (printed p. 20) |

### `pl_site` (site_resolution)

**Question:** Which site in the chest does the report name for the tumour?

**Hint:** Choose the overlapping lesion only when the tumour spans the named sites and the report does not say where it began.

| Option | Outcome | Records | Reason shown | Recognition aid | Pages |
|---|---|---|---|---|---|
| Pleura (parietal or visceral) | go | site C38.4; go to `pl_evidence` | Site recorded as Pleura, NOS (C38.4). |  |  |
| Heart or pericardium | go | site C38.0; go to `pl_evidence` | Site recorded as Heart (C38.0). |  |  |
| More than one of the heart, mediastinum and pleura, and the report does not say where the tumour began | go | site C38.8; go to `pl_evidence` | Site recorded as Overlapping lesion of heart, mediastinum and pleura (C38.8). |  | ICD-O-3 manual, PDF p. 5 (printed p. 18) |
| The lung together with the pleura, chest wall or mediastinum, and the report does not say where the tumour began | go | site C39.8; go to `pl_evidence` | Site recorded as Overlapping lesion of respiratory system and intrathoracic organs (C39.8). |  | ICD-O-3 manual, PDF p. 5 (printed p. 18) |
| Upper respiratory tract, with no part named | go | site C39.0; go to `pl_evidence` | Site recorded as Upper respiratory tract, NOS (C39.0). |  |  |
| Respiratory tract, with no part named | go | site C39.9; go to `pl_evidence` | Site recorded as Ill-defined sites within respiratory system (C39.9). |  |  |
| The lung or a bronchus | go | go to `lu_site` | A lung tumour is recorded through the lung screens. |  |  |
| The mediastinum or thymus | go | go to `thymus_tree` | Mediastinal and thymic tumours are recorded through the thymus and mediastinum screens. |  |  |
| The chest or chest wall, with no organ or tissue named | go | go to `site_capture`, site recaptured | Rule A: when the report names a region and no tissue, the site follows the tissue the tumour type implies. The next screen records the site. |  | ICD-O-3 manual, PDF p. 1 (printed p. 14) |

### `pl_evidence` (document_inventory)

**Question:** What is in the file for this tumour?

**Hint:** Choose the strongest report in the file. Cytology of pleural or pericardial fluid, or of a needle aspirate, counts as cytology. A report that calls the tumour possible, probable or suspected cancer does not register it.

| Option | Outcome | Records | Reason shown | Recognition aid | Pages |
|---|---|---|---|---|---|
| A referral letter or clinical note only, stating a malignant tumour | code | 8000/3, basis 1 | Recorded as Neoplasm, malignant (8000/3), basis of diagnosis clinical. |  |  |
| An imaging report only | code | 8000/3, basis 2 | Recorded as Neoplasm, malignant (8000/3), basis of diagnosis imaging. |  |  |
| A note or report that calls the tumour possible, probable or suspected cancer only | not_registrable | nothing registered | A possible or suspected cancer is not registered. |  |  |
| A cytology report, including pleural or pericardial fluid | go | go to `pl_cytology` (basis 5) |  |  |  |
| A histology report on a biopsy or resection, with or without immunohistochemistry or gene reports | go | go to `pl_histology` (basis 7) |  |  |  |

### `pl_cytology` (morphology_only)

**Question:** What does the cytology report on the fluid or aspirate call the tumour?

**Hint:** A carcinoma found in pleural or pericardial fluid is coded at the organ where it began when the file names that organ. Reactive or atypical mesothelial cells are not a diagnosis of cancer.

| Option | Outcome | Records | Reason shown | Recognition aid | Pages |
|---|---|---|---|---|---|
| Carcinoma, and the file names the organ where the tumour began | go | go to `site_capture`, site recaptured | A deposit is coded at the site where the tumour began. The next screen asks for that site. |  | ICCR Mesothelioma 2022, PDF p. 6; Sauter 2022, PDF p. 2 |
| Carcinoma, and the organ where it began is not known | code | 8010/3, basis 5, site C80.9 | Recorded as Carcinoma, NOS (8010/3) at unknown primary site (C80.9), on cytology. |  | ICD-O-3 manual, PDF p. 6 (printed p. 19) |
| Mesothelioma | refer | Group 12 | Mesothelioma (9050/3 to 9053/3) is coded in Group XII, other and unspecified malignant tumours. |  | Sauter 2022, PDF p. 2 |
| Malignant cells, with no tumour type named | code | 8000/3, basis 5 | Recorded as Neoplasm, malignant (8000/3) on cytology. |  |  |
| Lymphoma | refer | Group 2 | Lymphoma is coded in Group II, lymphomas and reticuloendothelial neoplasms. |  |  |
| Suspicious for malignancy, atypical or reactive mesothelial cells, benign, or non-diagnostic | not_registrable | nothing registered | The cytology report does not state a malignant tumour, so nothing is registered. |  |  |

### `pl_histology` (histology_subclassification)

**Question:** What does the histology report call the tumour?

**Hint:** Mesothelioma is coded in Group XII. A carcinoma in the pleura, pericardium or heart that began in another organ is coded at that organ.

NOS fallback: 8010/3.

| Option | Outcome | Records | Reason shown | Recognition aid | Pages |
|---|---|---|---|---|---|
| Mesothelioma of any type: diffuse or localized, epithelioid, sarcomatoid, desmoplastic or biphasic | refer | Group 12 | Mesothelioma (9050/3 to 9053/3) is coded in Group XII, other and unspecified malignant tumours. |  | Sauter 2022, PDF p. 2 |
| Well-differentiated papillary mesothelial tumour (well-differentiated papillary mesothelioma) of the pleura | exclude | 9052/1 | Not registered: Well differentiated papillary mesothelioma of pleura (9052/1) is not a malignant tumour. |  | Sauter 2022, PDF p. 2 |
| Well-differentiated papillary mesothelial tumour of the pericardium | exclude | 9052/0 | Not registered: away from the pleura ICD-O-3.2 codes this tumour 9052/0, Epithelioid mesothelioma, benign. |  |  |
| Adenomatoid tumour | exclude | 9054/0 | Not registered: Adenomatoid tumor, NOS (9054/0) is not a malignant tumour. |  | Sauter 2022, PDF p. 2 |
| Mesothelioma in situ | not_registrable | nothing registered | Mesothelioma in situ is not a malignant tumour and ICD-O-3.2 gives it no code, so it is not registered. |  | Sauter 2022, PDF p. 2 |
| Cardiac rhabdomyoma | exclude | 8900/0 | Not registered: Rhabdomyoma, NOS (8900/0) is not a malignant tumour. |  | Pfister 2022, PDF p. 14 |
| A carcinoma that began in another organ and has spread to the pleura, pericardium or heart | go | go to `site_capture`, site recaptured | A deposit is coded at the site where the tumour began. The next screen asks for that site. |  | Sauter 2022, PDF p. 7 |
| A carcinoma that has spread here, and the organ where it began is not known | code | 8010/3, basis 7, site C80.9 | Recorded as Carcinoma, NOS (8010/3) at unknown primary site (C80.9). |  | ICD-O-3 manual, PDF p. 6 (printed p. 19) |
| A malignant tumour the report does not type, with immunohistochemistry that compares mesothelioma and carcinoma | go | go to `pl_ihc` |  |  |  |
| Pleuropulmonary blastoma | refer | Group 12 | Pleuropulmonary blastoma (8973/3) is coded in Group XII, other and unspecified malignant tumours. |  | Nicholson 2022, PDF p. 3 |
| A sarcoma | refer | Group 9 | Soft-tissue sarcomas are coded in Group IX, soft-tissue and other extraosseous sarcomas. |  | Sauter 2022, PDF p. 2 |
| Lymphoma | refer | Group 2 | Lymphoma is coded in Group II, lymphomas and reticuloendothelial neoplasms. |  |  |
| Melanoma | go | go to `mel_site` | Melanoma is recorded through the melanoma screens, which ask where it began. |  |  |
| Carcinoma, with no type named | code | 8010/3, basis 7 | Recorded as Carcinoma, NOS (8010/3). |  |  |
| Another carcinoma the report names | go | go to `gc_picker` |  |  |  |
| A malignant tumour, with no type named | code | 8000/3, basis 7 | Recorded as Neoplasm, malignant (8000/3). |  |  |

### `pl_ihc` (ihc_checklist)

**Question:** Which markers does the immunohistochemistry report call positive?

**Hint:** Tick each marker the report calls positive. Mesothelial markers are calretinin, WT1, cytokeratin 5/6 and D2-40 (podoplanin). Carcinoma markers are claudin 4, MOC31, BG8 and BerEP4.

Checklist fallback: 8000/3. Recorded as Neoplasm, malignant (8000/3): the markers do not settle the tumour type.

The checklist has no answer buttons; the rules in section 4 decide.

## 4. Immunohistochemistry rules

`pl_ihc` is built: a malignant pleural tumour the report does not type, with a panel comparing mesothelioma and carcinoma. The ICCR mesothelioma dataset asks for at least two mesothelial and two carcinoma markers. The `lu_nscc_favour` rules are recorded for registrar question 2 and are not built: the WHO maps a TTF-1 or p40 result to a 'favour' term on small biopsies, and the tree codes a 'favour' report to 8046/3 until the registrar rules.

| Panel | Positive | Negative | Code | Outcome | Pages |
|---|---|---|---|---|---|
| `pl_ihc` | two or more of calretinin, WT1, cytokeratin 5/6, D2-40 | claudin 4, MOC31, BG8, BerEP4 | 9050/3 | refer to Group XII (mesothelioma) | ICCR Mesothelioma 2022, PDF p. 12 |
| `pl_ihc` | claudin 4, or two or more of MOC31, BG8, BerEP4 | calretinin, WT1, cytokeratin 5/6, D2-40 | 8010/3 | carcinoma: the next question asks whether the report names the organ where it began | Sauter 2022, PDF p. 7; ICCR Mesothelioma 2022, PDF p. 12 |
| `pl_ihc` | CD34, SOX2, SALL4 | cytokeratin (negative or only focal), BRG1 (SMARCA4) expression lost | 8044/3 | thoracic SMARCA4-deficient undifferentiated tumour; not built until registrar question 3 is answered | Sauter 2022, PDF p. 10 |
| `lu_nscc_favour (proposed; only if registrar question 2 rules that favour terms take the type's code)` | TTF-1 | p40 | 8140/3 | adenocarcinoma (WHO small-biopsy term: non-small cell carcinoma, favour adenocarcinoma) | Nicholson 2022, PDF p. 5; ICCR Lung 2023, PDF p. 16 |
| `lu_nscc_favour (proposed)` | mucin stain | TTF-1, p40 | 8140/3 | adenocarcinoma | Nicholson 2022, PDF p. 5 |
| `lu_nscc_favour (proposed)` | p40 | TTF-1 | 8070/3 | squamous cell carcinoma (WHO small-biopsy term: non-small cell carcinoma, favour squamous cell carcinoma) | Nicholson 2022, PDF p. 6, table image; ICCR Lung 2023, PDF p. 16 |
| `lu_nscc_favour (proposed)` | none | TTF-1, p40, mucin stain | 8046/3 | fallback: non-small cell carcinoma, NOS | Nicholson 2022, PDF p. 6, table image; Nicholson 2022, PDF p. 5 |

## 5. Registration without tissue

The registrar's ruling on Visser 2023 governs; none of the six files covers registration without tissue. Every row below is that ruling applied to these sites.

| Evidence on file | Code | Basis |
|---|---|---|
| Lung or thoracic site: a referral letter or clinical note only (registrar's ruling on Visser 2023) | 8000/3 | 1 |
| Lung or thoracic site: an imaging report only (registrar's ruling on Visser 2023) | 8000/3 | 2 |
| Lung: imaging that shows the tumour with raised chromogranin A (Visser 2023 Table 4; the lung papers name no serum test) | 8240/3 | 4 |
| Lung: imaging that shows the tumour with raised serotonin (Visser 2023 Table 4; the lung papers name no serum test) | 8241/3 | 4 |
| Lung: imaging that shows the tumour with raised adrenocorticotropic hormone (Visser 2023 Table 4; the lung papers name no serum test) | 8158/3 | 4 |

A note that calls the tumour possible or suspected cancer is not registrable (`lu_evidence`, `pl_evidence`). A raised marker with no tumour on imaging is not registrable (`lu_lab` hint). At the lung, pleura and heart, ICCC-2017 places 8000/3 in XIIb (section 9).

## 6. Laboratory tests

The six files give no serum or urine test a diagnostic role at these sites. `lab_tests` is empty. The `lu_lab` screen (chromogranin A, serotonin, adrenocorticotropic hormone) rests on the Visser 2023 Table 4 ruling alone (data gap 3, registrar question 7). Pleural fluid is read as cytology, not as a laboratory test.

## 7. Rules A to K

| Rule | Applies | Where it reaches the clerk |
|---|---|---|
| A | yes | pl_site option 'The chest or chest wall, with no organ or tissue named' sends the case to site capture; its reason states that the site follows the tissue the tumour type implies (ICD-O-3 manual, PDF p. 1, printed p. 14). |
| B | yes | lu_site option 'Beside the lung or a bronchus (for example paratracheal or peribronchial)' sends the case to site capture; its reason states the C76 rule and its exception (ICD-O-3 manual, PDF p. 1, printed p. 14). |
| C | yes | lu_site option for C34.8, and pl_site options for C38.8 and C39.8, each worded 'and the report does not say where the tumour began'; the lu_site hint names the overlapping lesion (ICD-O-3 manual, PDF p. 5, printed p. 18). |
| D | yes | Referral only: lymphoma options on lu_cytology, lu_histology, pl_cytology and pl_histology refer to Group II, whose screens apply Rule D. |
| E | no | No leukaemia is coded at these sites. Any leukaemia report is referred to Group I before it reaches this tree. |
| F | yes | lu_not_malignant hint: if the pathologist states one of these tumours is malignant, the stated behaviour is recorded. Exclusion reasons name the ICD-O-3.2 behaviour; 'Bronchial adenoma, with no type named' is 8140/1 while 'bronchial adenoma of carcinoid type' on lu_carcinoid is 8240/3 (ICD-O-3 manual, PDF pp. 2 and 7, printed pp. 15 and 20). |
| G | yes | lu_carcinoid hint: when the report gives both typical and atypical carcinoid features, choose atypical carcinoid, the higher grade. The sixth-digit grade itself is not built (registrar, 7 October 2026). |
| H | yes | pl_histology offers the well-differentiated papillary mesothelial tumour twice: 9052/1 at the pleura, 9052/0 at the pericardium, as ICD-O-3.2 prints. The deposit options on lu_histology, pl_cytology and pl_histology, and the enteric-type adenocarcinoma recognition aid, carry the manual's check that the stated site is not a metastasis (ICD-O-3 manual, PDF p. 10, printed p. 23). The lung-specific terms (lepidic, mucinous and minimally invasive adenocarcinoma, pulmonary blastoma) carry C34 in ICD-O-3.2 and are offered only at the lung. |
| J | yes | lu_picker hint: if a compound name is not found, search for its parts in the other order (ICD-O-3 manual, PDF p. 3, printed p. 16). |
| K | yes | lu_picker hint: when one tumour shows two types and no entry names both, choose the higher code number. Adenosquamous carcinoma (8560/3), combined small cell carcinoma (8045/3) and combined large cell neuroendocrine carcinoma (8013/3) are single codes that name both components, so the rule is not needed for them (ICD-O-3 manual, PDF pp. 3 and 11, printed pp. 16 and 24). |

There is no Rule I. Rules D and E are met by referral only.

## 8. Code currency

Findings from `Group 11 — ICD-O-3.2 Code Currency Check 2026-10-08.md`, the REDCap Group 11 XIf list and the sources. REDCap strings are recorded for the REDCap-side list only (standing rule 16).

| Code | Finding | What the tree does |
|---|---|---|
| 8240/3 | Currency check section 4: the REDCap label Carcinoid tumor, NOS is a synonym; the ICD-O-3.2 preferred term is Neuroendocrine tumor, NOS. Typical carcinoid is a synonym at this code. | Reason names Neuroendocrine tumor, NOS (8240/3) and states the synonym. REDCap-side list: relabel. |
| 8249/3 | Currency check section 4: REDCap label Atypical carcinoid tumor is a synonym; preferred term is Neuroendocrine tumor, grade 2. | Reason names Neuroendocrine tumor, grade 2 (8249/3). REDCap-side list: relabel. |
| 8250/3 | Currency check section 4: the REDCap label Bronchiolo-alveolar adenocarcinoma, NOS is an [obs] term; the preferred term is Lepidic adenocarcinoma. | Picker entry labelled Lepidic adenocarcinoma. No obsolete term is shown. REDCap-side list: relabel. |
| 8251/3 | Currency check section 2: every /3 term is [obs]. The WHO 2021 lung classification keeps only 8251/0 Alveolar adenoma. | Not built. No successor is printed by ICD-O-3.2 or the WHO source. |
| 8252/3 | Not in the currency check. ICD-O-3.2 keeps the preferred term Bronchiolo-alveolar carcinoma, non-mucinous current; its two synonyms are [obs]. The WHO 2021 lung table prints no entity at 8252. | Registrar question 4. Not on any screen until ruled. |
| 8253/3 | Currency check section 4: REDCap label Bronchiolo-alveolar carcinoma, mucinous is [obs]; preferred term is Adenocarcinoma of lung, mucinous. | Picker entry labelled Invasive mucinous adenocarcinoma; reason names Adenocarcinoma of lung, mucinous. REDCap-side list: relabel. |
| 8254/3 | Currency check section 4: REDCap label is an [obs] term; preferred term is Adenocarcinoma of lung, mixed mucinous and non-mucinous. | Reason names the preferred term. REDCap-side list: relabel. |
| 8551/3 | Currency check section 4: the preferred term Acinar cell cystadenocarcinoma (also the REDCap label) is [obs]; the current Related term is Acinar adenocarcinoma of lung. | Picker entry labelled Acinar adenocarcinoma; reason names Acinar adenocarcinoma of lung (8551/3). REDCap-side list: relabel. |
| 8256/3 | Currency check section 6: new in ICD-O-3.2; REDCap does not offer it. | Built as a picker entry. REDCap-side list: add. |
| 8257/3 | Currency check section 6: new in ICD-O-3.2; REDCap does not offer it. | Built as a picker entry. REDCap-side list: add. |
| 8023/3 | Currency check section 6: REDCap does not offer NUT carcinoma; it is built in four Group XI sites, the lung among them. | Option on lu_histology. REDCap-side list: add. |
| 8045/3 | The REDCap XIf option list does not offer Combined small cell carcinoma. | Built as a picker entry. REDCap-side list: add. |
| 8046/3 | The REDCap XIf option list does not offer Non-small cell carcinoma. | Built as a picker entry. REDCap-side list: add. |
| 8044/3 | The WHO prints 8044/3 for thoracic SMARCA4-deficient undifferentiated tumour; the ICD-O-3.2 term at 8044/3 is Small cell carcinoma, intermediate cell. REDCap does not offer 8044. | Registrar question 3. Not built until ruled. |
| 8310/3 | The WHO term Hyalinizing clear cell carcinoma has no ICD-O-3.2 term; the code's preferred term is Clear cell adenocarcinoma, NOS. | Picker label uses the WHO term; reason names Clear cell adenocarcinoma, NOS (8310/3). |
| 8033/3 | Currency check section 4: REDCap label Sarcomatoid carcinoma is a synonym; preferred term is Pseudosarcomatous carcinoma. | Reason names Pseudosarcomatous carcinoma (8033/3). REDCap-side list: relabel. |
| 8010/3 | The REDCap XIf label is Epithelial Tumor, NOS (a synonym); preferred term is Carcinoma, NOS. | Reason names Carcinoma, NOS (8010/3). REDCap-side list: relabel. |
| 8158/3 | The REDCap XIf label Endocrine tumor, functioning, NOS is an [obs] Related term; the preferred term is ACTH-producing tumor. | lu_lab reason names ACTH-producing tumor (8158/3). REDCap-side list: relabel. |
| 8042/3 | Currency check section 2 note: Oat cell carcinoma is [obs] and sits in the ICCC Group XI ranges; the WHO 2021 lung entity is Small cell carcinoma (8041/3). | Not built. The lung histology screen offers Small cell carcinoma (8041/3) only. |
| 9050/2 | The WHO prints 9050/2 Mesothelioma in situ, approved by the IARC/WHO committee in October 2020; ICD-O-3.2 holds no 9050/2. | Registrar question 5. pl_histology shows it as not registrable, with no code. |
| 9174/3 | The WHO prints 9174/3 Lymphangioleiomyomatosis (approved October 2020); ICD-O-3.2 holds 9174/1 only. | Not in Group XI. Listed for the registrar; no screen in this part. |
| 9052/1 | The WHO renamed the tumour Well-differentiated papillary mesothelial tumour; ICD-O-3.2 keeps Well differentiated papillary mesothelioma of pleura. | Label carries both names; reason names the ICD-O-3.2 term. |

## 9. Conflicts with other groups

| Group | Codes | Sites | Issue |
|---|---|---|---|
| 12 | 8973, 8972, 8980, 8982 | C34.0, C34.1, C34.2, C34.3, C34.8, C34.9, C38.4 | Pleuropulmonary blastoma, pulmonary blastoma, carcinosarcoma and myoepithelial carcinoma are WHO lung tumours, three of them in the WHO carcinoma chapters, but ICCC-2017 places them in XIIa3 and XIIa4 at every site. The lung screen refers them to Group XII. |
| 12 | 9050, 9051, 9052, 9053 | C38.4, C38.0, C38.8 | Mesothelioma is ICCC XIIa5 at every site. The pleural screens refer it to Group XII; the benign and uncertain mesothelial tumours (9052/1, 9052/0, 9054/0) are exclusions here. |
| 12 | 8000 | C34.0, C34.1, C34.2, C34.3, C34.8, C34.9, C38.0, C38.4, C38.8, C39.0, C39.8, C39.9 | The tissue-free code 8000/3 (basis 1 or 2) and a histology report of a malignant tumour with no type fall in ICCC XIIb at the lung, pleura, heart and C39, not in Group XI. The subgroup computed at output will be XIIb (registrar question 6). |
| 2 | 9699, 9680, 9751, 9749 | C34.0, C34.1, C34.2, C34.3, C34.8, C34.9 | Lymphomas and histiocytic tumours of the lung refer to Group II. ICCC-2017 holds no range for 9749 Erdheim-Chester disease; the Group II tree carries it. |
| 9 | 9137, 8842, 8714, 9170, 8825 | C34.0, C34.1, C34.2, C34.3, C34.8, C34.9, C38.4 | Lung and pleural sarcomas refer to Group IX. Diffuse lymphangiomatosis carries 9170/3 in the WHO table but ICD-O-3.2's term there is Lymphangiosarcoma; Group IX decides. Inflammatory myofibroblastic tumour is 8825/1 (exclusion here); 8825/3 Myofibroblastic sarcoma is Group IX. |
| 10 | 9080 | C34.0, C34.1, C34.2, C34.3, C34.8, C34.9 | ICD-O-3.2 lists Immature teratoma of lung as a Related term at 9080/1 (C34._). Germ cell tumours of the lung or mediastinum belong to the Group X tree; this part offers no germ cell option and the clerk reaches Group X through the router. |
| 11 | 8720 | C34.0, C34.1, C34.2, C34.3, C34.8, C34.9, C38.4 | The melanoma tree (XId evidence, node mel_site) has no route for melanoma arising in an internal organ such as the lung. The lung and pleural screens send melanoma to mel_site; that node needs an 'another organ' option recording 8720/3 at the stated site. |
| 11 | 8023, 8580, 8044 | C34.0, C34.9, C37.9, C38.1, C38.3 | Thymus and mediastinum part (XIf5) and NUT part: Nicholson 2022 places NUT carcinoma of the thorax under thymic tumours; ICD-O-3.2 lists Intrapulmonary thymoma at 8580/3 with topography C34._; thoracic SMARCA4-deficient undifferentiated tumour presents in the mediastinum, lung or pleura. The lung tree codes NUT carcinoma at the lung site; the mediastinum is routed to the thymus tree (next 'thymus_tree'). |
| 11 | 8010 | C80.9 | The deposit options that record 8010/3 at C80.9 change the topography away from the tree's site. ICCC places 8010/3 at C80.9 in XIf11. The node option carries topography_override C80.9; the engine needs to honour it. |

## 10. Data gaps

1. **Paediatric occurrence of the lung carcinomas that remain picker entries: mucinous adenocarcinoma arising in a congenital pulmonary airway malformation, fetal adenocarcinoma, adenoid cystic carcinoma and the other WHO subtypes.** Ozkan 2024 and Chen 2026, added 8 October 2026, report carcinoid tumour, mucoepidermoid carcinoma, adenocarcinoma, squamous cell carcinoma, small cell carcinoma, large cell carcinoma and large cell neuroendocrine carcinoma in children; those are now options on lu_histology. Ozkan 2024 names a congenital pulmonary airway malformation only as a preexisting disease, not the carcinoma that arises in it. Neither paper reports a named adenocarcinoma or squamous cell carcinoma subtype, fetal adenocarcinoma, a salivary gland-type carcinoma other than mucoepidermoid carcinoma, or a sarcomatoid carcinoma in a child, so those stay picker entries. Candidate source: WHO Classification of Tumours, Paediatric Tumours, 5th ed., thoracic chapter; Dishop MK, Kuruvilla S. Primary and metastatic lung tumors in the pediatric population. Arch Pathol Lab Med 2008;132:1079-1103; Rojas Y, et al. Primary malignant pulmonary tumors in children: a review of the National Cancer Data Base. J Pediatr Surg 2015;50:1004-1008.
2. **The mitotic and necrosis thresholds that separate typical carcinoid, atypical carcinoid and large cell neuroendocrine carcinoma.** Nicholson 2022 says mitoses per 2 mm2 and necrosis decide, but does not print the cut-offs. The tree relies on the report naming the type; a numeric gate cannot be built without them. Candidate source: WHO Classification of Tumours, Thoracic Tumours, 5th ed., 2021, lung neuroendocrine neoplasms chapter.
3. **Serum or urine tests with a diagnostic role for lung neuroendocrine tumours.** The lu_lab screen rests on the registrar's Visser 2023 Table 4 ruling (chromogranin A 8240/3, serotonin 8241/3, ACTH 8158/3). The lung papers name no serum or urine test, so no page supports the screen for the lung. Candidate source: Caplin ME, et al. Pulmonary neuroendocrine (carcinoid) tumors: European Neuroendocrine Tumor Society expert consensus. Ann Oncol 2015;26:1604-1620.
4. **An ICD-O code for fetal lung interstitial tumour.** Pfister 2022 lists it as a new paediatric lung entity; ICD-O-3.2 and the six files give no code. The tree shows it as not registrable. Candidate source: WHO Classification of Tumours, Paediatric Tumours, 5th ed., fetal lung interstitial tumour entry.
5. **A primary carcinoma entity of the pleura, pericardium or heart.** Sauter 2022 and the ICCR mesothelioma dataset name none; the pleural screen offers carcinoma, NOS, the general picker and the deposit routes only.
6. **A paediatric source for the two lung options that rest on none: Carcinoma, NOS (8010/3) and melanoma (8720/3).** Neither Ozkan 2024 nor Chen 2026 reports a carcinoma, NOS or a melanoma of the lung in a child. Carcinoma, NOS is the fallback code for a report that names no type; melanoma is a route to the melanoma tree. Both stay options as built; the controller decides.
7. **The code for a child's report of bronchoalveolar carcinoma or alveolar carcinoma.** Ozkan 2024 cites a series of 211 children in which bronchoalveolar carcinoma was 2% of primary lung malignancies, and Chen 2026 names alveolar carcinoma as an epithelial lung tumour of children. Both are retired terms: ICD-O-3.2 holds Bronchiolo-alveolar carcinoma, NOS as an [obs] synonym at 8250/3 Lepidic adenocarcinoma, keeps 8252/3 Bronchiolo-alveolar carcinoma, non-mucinous current, and marks Alveolar carcinoma [obs] at 8251/3. Nicholson 2022 records that bronchioloalveolar carcinoma was defined as a noninvasive tumour, so neither paper reports lepidic adenocarcinoma itself in a child. Lepidic adenocarcinoma (8250/3) stays a picker entry, 8252/3 stays with registrar question 4, and 8251/3 stays off every screen. Candidate source: Rojas Y, et al. Primary malignant pulmonary tumors in children: a review of the National Cancer Data Base. J Pediatr Surg 2015;50:1004-1008.
8. **A screen entry for a mature teratoma of the lung.** Chen 2026 reports a mature teratoma of the lung in a child. ICD-O-3.2 codes Mature teratoma, NOS to 9080/0 (Teratoma, benign), and ICCC-2017 holds 9080 at the lung only at behaviour /3 (Xb2), so it is added as an exclusion. Neither lu_histology nor lu_not_malignant offers it, and section 9 of the evidence records that germ cell tumours of the lung reach the Group X tree through the router. The controller decides between an exclusion option on lu_not_malignant and a referral option to Group X.
9. **Whether the lu_histology hint states the two-types rule (Rule K).** Seven carcinoma and neuroendocrine entries moved from lu_picker to lu_histology on 8 October 2026. Rule K (when one tumour shows two types and no entry names both, choose the higher code) is stated in the lu_picker hint only. The controller decides whether the lu_histology hint states it too.
10. **Paediatric examples in the lymphoma and sarcoma referral labels on lu_histology.** Chen 2026 reports Hodgkin lymphoma, Ewing sarcoma and alveolar soft part sarcoma of the lung in children and names rhabdomyosarcoma. The lu_histology sarcoma label names adult examples (intimal sarcoma, pulmonary myxoid sarcoma, malignant PEComa). The referral groups are right for all four. The controller decides whether the labels name the paediatric tumours.

### Questions for the registrar

- 1. Answered by the paediatric evidence of 8 October 2026 (section 11). Ozkan 2024 and Chen 2026 report typical and atypical carcinoid (8240/3, 8249/3) and mucoepidermoid carcinoma (8430/3) in children, so under the registrar's ruling of 8 October 2026 they are options on the lung histology screen, no longer picker entries.
- 2. A lung biopsy report of non-small cell carcinoma, favour adenocarcinoma (or favour squamous cell carcinoma): record 8046/3 Non-small cell carcinoma, as built, or the favoured type's code (8140/3 or 8070/3)?
- 3. Thoracic SMARCA4-deficient undifferentiated tumour: the WHO prints 8044/3, where the ICD-O-3.2 term is Small cell carcinoma, intermediate cell. Build it on 8044/3, or leave it unbuilt?
- 4. Bronchioloalveolar carcinoma in an older report: 8252/3 Bronchiolo-alveolar carcinoma, non-mucinous is a current ICD-O-3.2 preferred term with no WHO 2021 entity, and the term was defined as noninvasive. Code such a report to 8252/3, to the current adenocarcinoma code, or treat it as adenocarcinoma in situ (not registrable)?
- 5. Mesothelioma in situ (WHO 9050/2, not in ICD-O-3.2) and fetal lung interstitial tumour (no ICD-O-3.2 code) are shown as not registrable. Confirm.
- 6. The tissue-free code 8000/3 at the lung, pleura and heart falls in ICCC XIIb. Confirm the tool records it at the stated site and lets the computed subgroup be XIIb.
- 7. The lung laboratory screen (chromogranin A 8240/3, serotonin 8241/3, ACTH 8158/3, basis 4) rests on the Visser Table 4 ruling alone; the lung papers name no test. Keep the screen for the lung?

## 11. Paediatric evidence added 8 October 2026

The controller fetched two open-access paediatric papers from PubMed Central for this part: Ozkan 2024 (`XIf4-lung-paediatric__Ozkan-2024.txt`, a review of lung tumours in childhood with the authors' own cases) and Chen 2026 (`XIf4-lung-paediatric__Chen-2026.txt`, 36 children with primary lung tumours at one centre, aged 2.0 to 9.8 years). Both were read through the snippet tool only. A PubMed Central text has sections, not pages, so each cite gives the section number in the `pdf_page` field. Under the registrar's ruling of 8 October 2026 an entity a source reports at ages 0 to 18 is an option on the histology screen, and a valid current /3 code with no paediatric report stays a picker entry.

### Entities

| Entity | Code | Before (paediatric, decision) | After (paediatric, decision) | Cite |
|---|---|---|---|---|
| Typical carcinoid/neuroendocrine tumour, grade 1; carcinoid tumour, NOS/neuroendocrine tumour, NOS | 8240/3 | not_reported, picker | common, option | Ozkan 2024, PMC section 2: "Bronchial carcinoids account for 42-63% of all primary lung malignancies in the pediatric population"; Ozkan 2024, PMC section 2: "carcinoid tumor was the most common histology (29.6%)"; Ozkan 2024, PMC section 2: "diagnosed between a mean age of 11.6 and 13.8 years"; Chen 2026, PMC section 10: "the most prevalent primary malignant pulmonary tumors in children are carcinoid tumors and PPB" |
| Atypical carcinoid/neuroendocrine tumour, grade 2 | 8249/3 | not_reported, picker | occurs, option | Ozkan 2024, PMC section 2: "Bronchial carcinoids are classified as typical low-grade carcinoids and atypical intermediate-grade carcinoids"; Ozkan 2024, PMC section 2: "Atypical bronchial carcinoids occur more frequently in children." |
| Mucoepidermoid carcinoma | 8430/3 | not_reported, picker | common, option | Ozkan 2024, PMC section 2: "It was reported as the second most common primary malignant pulmonary tumor in children"; Chen 2026, PMC section 10: "followed by mucoepidermoid carcinoma, which constitutes 11.11%"; Chen 2026, PMC section 9: "Pulmonary mucoepidermoid carcinoma and pulmonary sclerosing pneumocytoma each accounted for 11.11%" |
| Small cell carcinoma | 8041/3 | not_reported, picker | occurs, option | Ozkan 2024, PMC section 2: "Small cell lung carcinoma is exceedingly rare in pediatric patients."; Ozkan 2024, PMC section 2: "adenocarcinoma, squamous cell carcinoma, small cell carcinoma, and large cell carcinoma"; Chen 2026, PMC section 2: "neuroendocrine tumors (small cell carcinoma and large cell neuroendocrine carcinoma)" |
| Large cell neuroendocrine carcinoma; combined large cell neuroendocrine carcinoma | 8013/3 | not_reported, picker | occurs, option | Chen 2026, PMC section 2: "neuroendocrine tumors (small cell carcinoma and large cell neuroendocrine carcinoma)" |
| Adenocarcinoma, NOS | 8140/3 | not_reported, picker | occurs, option | Ozkan 2024, PMC section 2: "epithelial origin in pediatric patients are carcinoid tumors, mucoepidermoid carcinoma, adenocarcinoma, squamous cell carcinoma"; Ozkan 2024, PMC section 2: "Adenocarcinoma was more common than squamous cell carcinoma."; Ozkan 2024, PMC section 2: "followed by pulmonary blastoma (22.3%), mucoepidermoid carcinoma (12.3%), adenocarcinoma (10.3%)" |
| Squamous cell carcinoma, NOS | 8070/3 | not_reported, picker | occurs, option | Ozkan 2024, PMC section 2: "epithelial origin in pediatric patients are carcinoid tumors, mucoepidermoid carcinoma, adenocarcinoma, squamous cell carcinoma"; Ozkan 2024, PMC section 2: "Adenocarcinoma was more common than squamous cell carcinoma." |
| Large cell carcinoma | 8012/3 | not_reported, picker | occurs, option | Ozkan 2024, PMC section 2: "adenocarcinoma, squamous cell carcinoma, small cell carcinoma, and large cell carcinoma"; Ozkan 2024, PMC section 2: "squamous cell, large cell, and small cell lung carcinomas have the lowest incidence rate" |
| Alveolar adenocarcinoma (no WHO 2021 entity) | 8251/3 | not_reported, not_built | occurs, not_built | Chen 2026, PMC section 2: "epithelial tumors (alveolar carcinoma)" |
| Pleuropulmonary blastoma | 8973/3 | occurs, refer to Group 12 | common, refer to Group 12 | Chen 2026, PMC section 9: "Pleuropulmonary blastoma (PPB) was the most prevalent tumor type, comprising 44.44%"; Ozkan 2024, PMC section 2: "Pleuropulmonary blastoma is a rare and aggressive childhood tumor of mesenchymal origin" |
| Pulmonary blastoma | 8972/3 | not_reported, refer to Group 12 | occurs, refer to Group 12 | Chen 2026, PMC section 11: "mucoepidermoid carcinoma 4 Pulmonary blastoma 2 Hodgkin's lymphoma 1 Carcinoid tumor 1"; Chen 2026, PMC section 9: "The third patient was diagnosed with pulmonary blastoma"; Ozkan 2024, PMC section 2: "followed by pulmonary blastoma (22.3%), mucoepidermoid carcinoma (12.3%), adenocarcinoma (10.3%)" |
| Langerhans cell histiocytosis | 9751/1 | not_reported, refer to Group 2 | occurs, refer to Group 2 | Chen 2026, PMC section 11: "Pulmonary sclerosing pneumocytoma 4 Hamartoma 3 Langerhans cell histiocytosis 2 Mature teratoma 1"; Chen 2026, PMC section 9: "pulmonary hamartoma, Langerhans cell histiocytosis, pulmonary blastoma, mature teratoma, Hodgkin's lymphoma, carcinoid" |
| Primary pulmonary paraganglioma | 8693/3 | not listed | occurs, refer to Group 4 | Ozkan 2024, PMC section 2: "the second pediatric functioning PPP in the literature"; Ozkan 2024, PMC section 2: "Benign pulmonary tumors in childhood include inflammatory myofibroblastic tumors, hamartoma, and primary pulmonary paraganglioma"; Ozkan 2024, PMC section 2: "They can mimic carcinoid tumors or primary lung cancer" |
| Hodgkin lymphoma | 9650/3 | not listed | occurs, refer to Group 2 | Chen 2026, PMC section 9: "A patient with Hodgkin's lymphoma was confirmed by ultrasound-guided biopsy"; Chen 2026, PMC section 11: "mucoepidermoid carcinoma 4 Pulmonary blastoma 2 Hodgkin's lymphoma 1 Carcinoid tumor 1" |
| Rhabdomyosarcoma | 8900/3 | not listed | occurs, refer to Group 9 | Chen 2026, PMC section 2: "Mesenchymal tumors (rhabdomyosarcoma and inflammatory myofibroblastic tumor)" |
| Ewing sarcoma | 9364/3 | not listed | occurs, refer to Group 9 | Chen 2026, PMC section 9: "The second pediatric patient with Ewing sarcoma with EWSR1-FLI1 gene fusion"; Chen 2026, PMC section 9: "carcinoid, pulmonary alveolar soft tissue sarcoma and Ewing's sarcoma" |
| Alveolar soft part sarcoma | 9581/3 | not listed | occurs, refer to Group 9 | Chen 2026, PMC section 9: "carcinoid, pulmonary alveolar soft tissue sarcoma and Ewing's sarcoma"; Chen 2026, PMC section 11: "Alveolar soft part sarcoma 1 Ewing's sarcoma 1" |
| Inflammatory myofibroblastic tumour | 8825/1 | occurs, exclusion | common, exclusion | Ozkan 2024, PMC section 2: "Inflammatory myofibroblastic tumors account for more than 50% of benign pulmonary tumors in childhood"; Chen 2026, PMC section 2: "Mesenchymal tumors (rhabdomyosarcoma and inflammatory myofibroblastic tumor)" |
| Sclerosing pneumocytoma | 8832/0 | not_reported, exclusion | occurs, exclusion | Chen 2026, PMC section 9: "Pulmonary mucoepidermoid carcinoma and pulmonary sclerosing pneumocytoma each accounted for 11.11%"; Chen 2026, PMC section 11: "Pulmonary sclerosing pneumocytoma 4 Hamartoma 3 Langerhans cell histiocytosis 2 Mature teratoma 1" |
| Pulmonary hamartoma | 8992/0 | not_reported, exclusion | occurs, exclusion | Ozkan 2024, PMC section 2: "Benign pulmonary tumors in childhood include inflammatory myofibroblastic tumors, hamartoma, and primary pulmonary paraganglioma"; Chen 2026, PMC section 11: "Pulmonary sclerosing pneumocytoma 4 Hamartoma 3 Langerhans cell histiocytosis 2 Mature teratoma 1" |
| Mature teratoma | 9080/0 | not listed | occurs, exclusion | Chen 2026, PMC section 11: "Pulmonary sclerosing pneumocytoma 4 Hamartoma 3 Langerhans cell histiocytosis 2 Mature teratoma 1"; Chen 2026, PMC section 11: "Mature teratoma. (D) Tissue components, including skin and its appendages" |

### Screens

- `lu_histology`: seven entries moved here from `lu_picker` and now head the screen, commonest in children first: the carcinoid entry (which still leads to `lu_carcinoid` for typical, atypical or unstated type), mucoepidermoid carcinoma (8430/3), adenocarcinoma with no subtype named (8140/3), squamous cell carcinoma with no subtype named (8070/3), small cell carcinoma (8041/3), large cell carcinoma (8012/3) and large cell neuroendocrine carcinoma (8013/3). NUT carcinoma (8023/3) follows them. Each moved entry keeps its label, code, basis 7, reason and search terms and gains the paediatric cites. Mucoepidermoid carcinoma gains the recognition aid 'Reports describe a mix of mucus-secreting, squamous and intermediate cells.' (Ozkan 2024, PMC section 2).
- `lu_histology`: a new referral option, Paraganglioma, after Pulmonary blastoma. It refers to Group IV (ICCC-2017 IVb holds 8680 and 8693 at every site) and carries the recognition aid 'Paraganglioma and carcinoid tumour can look alike; choose the one the report names.' (Ozkan 2024, PMC section 2: "They can mimic carcinoid tumors or primary lung cancer").
- `lu_picker`: the same seven entries removed. It keeps the 26 WHO lung carcinomas no paediatric source reports, from adenoid cystic carcinoma to non-small cell carcinoma.
- `lu_carcinoid`: no option changed; the typical, atypical and unstated-type options gain the Ozkan 2024 and Chen 2026 cites.
- No pleural screen changed: neither paper reports a tumour of the pleura, pericardium or heart.

### Other changes

- Section 1: the two papers added to the sources.
- Headline rewritten for the paediatric evidence.
- Section 8: the 8042/3 row now says the lung histology screen, not the picker, offers Small cell carcinoma (8041/3).
- Section 10: data gap 1 narrowed to the carcinomas that stay picker entries; data gaps 6 to 10 added (the two options with no paediatric source, bronchoalveolar and alveolar carcinoma in a child's report, a screen entry for mature teratoma, Rule K on `lu_histology`, and paediatric examples in the referral labels). Registrar question 1 is answered by this evidence.
- Not changed: carcinoma, NOS (8010/3) and melanoma (8720/3) stay options with no paediatric source (data gap 6); NUT carcinoma keeps its Pfister 2022 evidence, and neither new paper reports it.
