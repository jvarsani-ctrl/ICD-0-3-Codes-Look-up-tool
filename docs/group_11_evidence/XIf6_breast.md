# Group 11 evidence — XIf6 breast carcinoma

Part `XIf6_breast`, sites C50.0 to C50.9 (ICCC-3 subgroup XIf6). Evidence for the breast branch of the general carcinoma tree (approach 3, registrar, 8 October 2026). Written 8 October 2026. The machine-readable copy is `XIf6_breast.json` in this folder; this file carries the same content.

## 1. Sources

| File | Citation | WHO volume |
|---|---|---|
| `XIf6-breast__Tan-2020.txt` | Tan PH, Ellis I, Allison K, et al. The 2019 World Health Organization classification of tumours of the breast. Histopathology 2020;77(2):181-185. doi:10.1111/his.14091 | WHO Classification of Tumours, Breast Tumours, 5th edition, 2019 |
| `XIf6-breast__ICCR-Invasive-Breast-2nd.txt` | International Collaboration on Cancer Reporting. Invasive Carcinoma of the Breast Histopathology Reporting Guide, 2nd edition, version 2.1, June 2022. ISBN 978-1-922324-35-1. | WHO Classification of Breast Tumours, 5th edition, 2019, with the Corrigenda of September 2020 |
| `ALL-paediatric-occurrence__Pfister-2022.txt` | Pfister SM, Reyes-Mugica M, Chan JKC, et al. A Summary of the Inaugural WHO Classification of Pediatric Tumors: Transitioning from the Optical into the Molecular Era. Cancer Discov 2022;12(2):331-355. | WHO Classification of Paediatric Tumours, 5th edition, 2022 |
| `RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt` | World Health Organization. International Classification of Diseases for Oncology, 3rd edition, 1st revision (ICD-O-3.1), section 4, Coding guidelines, printed pp. 14-28. | not a tumour classification; the ICD-O coding manual |
| `XIf6-breast-paediatric__Sosnowska-Sienkiewicz-2024.txt` | Sosnowska-Sienkiewicz P, et al. Benign and malignant breast lesions in children and adolescents - diagnostic and therapeutic approach. Front Pediatr 2024;12:1417050. doi:10.3389/fped.2024.1417050 | not a WHO summary; paediatric evidence |

Tables were read from the PDF page images: ICCR Invasive Breast Table 1 (PDF pp. 13–14), Pfister 2022 Table 3 (PDF p. 13) and ICD-O-3.1 manual Table 23 (PDF p. 10). Sosnowska-Sienkiewicz 2024 is a PubMed Central text with sections and no pages; it is cited by PMC section number. Codes were checked against `icdo32.sqlite` (ICD-O-3.2, IARC final, 9 October 2020) and `ICCC-2017.sqlite`; the topography subsites against `ICD coding/RedCap Options/Topography Redcap.md`, which also states that C50 excludes the skin of the breast (C44.5).

Pfister 2022 Table 3 lists two breast tumours of children, juvenile fibroadenoma and juvenile papillomatosis, both non-malignant (Pfister 2022, PDF p. 13). Neither Tan 2020 nor the ICCR guide gives ages. Sosnowska-Sienkiewicz 2024, a review of breast lesions in children and adolescents added on 8 October 2026, names invasive secretory carcinoma the commonest invasive breast cancer in children and lists invasive ductal, invasive lobular, medullary, inflammatory and anaplastic carcinomas as less common subtypes (PMC section 72); it also lists malignant phyllodes tumour among the malignant breast lesions of children and adolescents (PMC section 2). Under the registrar's ruling of 8 October 2026 those six carcinomas are answers on the histology screen, and every other breast carcinoma goes in the picker. The histology screen also carries the fallback Carcinoma, NOS, the fibroepithelial screen, the exclusions and the referrals. Section 11 lists the changes.

## 2. Entities

### 2.1 Entities the sources name, and the exclusions and referrals

| Entity | Code | ICD-O-3.2 term (level) | Paediatric | Decision | Page |
|---|---|---|---|---|---|
| Carcinoma with no type named (ICD-O-3.2 term; the fallback for a report that names no type) | 8010/3 | Carcinoma, NOS (Preferred) | not_reported | option | Pfister 2022, PDF p. 13 |
| Invasive breast carcinoma of no special type | 8500/3 | Invasive breast carcinoma of no special type (Synonym) | occurs | option | ICCR Invasive Breast 2022, PDF p. 13 (table); Tan 2020, PDF p. 1; ICD-O-3.1 manual, PDF p. 10 (table); Pfister 2022, PDF p. 13; Sosnowska-Sienkiewicz 2024, PMC section 72; Sosnowska-Sienkiewicz 2024, PMC section 76 |
| Invasive lobular carcinoma | 8520/3 | Infiltrating lobular carcinoma, NOS (Synonym) | occurs | option | ICCR Invasive Breast 2022, PDF p. 13 (table); Pfister 2022, PDF p. 13; Sosnowska-Sienkiewicz 2024, PMC section 72 |
| Tubular carcinoma | 8211/3 | Tubular carcinoma (Synonym) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 13 (table); Pfister 2022, PDF p. 13 |
| Invasive cribriform carcinoma | 8201/3 | Cribriform carcinoma, NOS (Preferred) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 13 (table); Pfister 2022, PDF p. 13 |
| Mucinous carcinoma | 8480/3 | Mucinous carcinoma (Synonym) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 13 (table); Pfister 2022, PDF p. 13 |
| Invasive micropapillary carcinoma | 8507/3 | Invasive micropapillary carcinoma of breast (Preferred) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 13 (table); Pfister 2022, PDF p. 13 |
| Carcinoma with apocrine differentiation | 8401/3 | Apocrine carcinoma (Synonym) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 13 (table); Pfister 2022, PDF p. 13 |
| Metaplastic carcinoma | 8575/3 | Metaplastic carcinoma, NOS (Preferred) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 13 (table); Pfister 2022, PDF p. 13 |
| Invasive breast carcinoma of no special type, oncocytic pattern | 8290/3 | Oncocytic carcinoma (Synonym) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 13 (table); Pfister 2022, PDF p. 13 |
| Invasive breast carcinoma of no special type, lipid-rich pattern | 8314/3 | Lipid-rich carcinoma (Preferred) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 13 (table); Pfister 2022, PDF p. 13 |
| Invasive breast carcinoma of no special type, glycogen-rich pattern | 8315/3 | Glycogen-rich clear cell carcinoma (Synonym) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 13 (table); Pfister 2022, PDF p. 13 |
| Invasive breast carcinoma of no special type, sebaceous pattern | 8410/3 | Sebaceous carcinoma (Preferred) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 13 (table); Pfister 2022, PDF p. 13 |
| Mucinous cystadenocarcinoma | 8470/3 | Mucinous cystadenocarcinoma, NOS (Preferred) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 14 (table); Tan 2020, PDF p. 4; Tan 2020, PDF p. 2; Pfister 2022, PDF p. 13 |
| Acinic cell carcinoma | 8550/3 | Acinic cell adenocarcinoma (Synonym) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 14 (table); Pfister 2022, PDF p. 13 |
| Adenoid cystic carcinoma | 8200/3 | Adenoid cystic carcinoma (Preferred) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 14 (table); Pfister 2022, PDF p. 13 |
| Secretory carcinoma | 8502/3 | Secretory carcinoma (Preferred) | common | option | ICCR Invasive Breast 2022, PDF p. 14 (table); Pfister 2022, PDF p. 13; Sosnowska-Sienkiewicz 2024, PMC section 72 |
| Mucoepidermoid carcinoma | 8430/3 | Mucoepidermoid carcinoma (Preferred) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 14 (table); Pfister 2022, PDF p. 13 |
| Polymorphous adenocarcinoma | 8525/3 | Polymorphous adenocarcinoma (Preferred) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 14 (table); Pfister 2022, PDF p. 13 |
| Solid papillary carcinoma, invasive | 8509/3 | Solid papillary carcinoma with invasion (Preferred) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 14 (table); Pfister 2022, PDF p. 13 |
| Invasive papillary carcinoma | 8503/3 | Papillary carcinoma of breast (Related) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 14 (table); Pfister 2022, PDF p. 13 |
| Neuroendocrine tumour | 8240/3 | Neuroendocrine tumor, NOS (Preferred) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 14 (table); Tan 2020, PDF p. 3; Pfister 2022, PDF p. 13 |
| Neuroendocrine carcinoma | 8246/3 | Neuroendocrine carcinoma, NOS (Preferred) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 14 (table); Pfister 2022, PDF p. 13 |
| Tall cell carcinoma with reversed polarity | 8509/3 | none (none) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 14 (table); Tan 2020, PDF p. 2; Tan 2020, PDF p. 4; Pfister 2022, PDF p. 13 |
| Malignant adenomyoepithelioma | 8983/3 | Malignant adenomyoepithelioma (Synonym) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 14 (table); Pfister 2022, PDF p. 13 |
| Epithelial-myoepithelial carcinoma (ICD-O-3.2 term; the ICCR table prints its code beside malignant adenomyoepithelioma) | 8562/3 | Epithelial-myoepithelial carcinoma (Preferred) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 14 (table); Pfister 2022, PDF p. 13 |
| Small cell neuroendocrine carcinoma | 8041/3 | Small cell neuroendocrine carcinoma (Related) | not_reported | picker | Tan 2020, PDF p. 3; Pfister 2022, PDF p. 13 |
| Large cell neuroendocrine carcinoma | 8013/3 | Large cell neuroendocrine carcinoma (Preferred) | not_reported | picker | Tan 2020, PDF p. 3; Pfister 2022, PDF p. 13 |
| Mixed carcinoma of no special type and invasive lobular carcinoma | 8522/3 | Infiltrating duct and lobular carcinoma (Preferred) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 12; Pfister 2022, PDF p. 13 |
| Mixed carcinoma of no special type and another special type | 8523/3 | Infiltrating duct mixed with other types of carcinoma (Preferred) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 2; Pfister 2022, PDF p. 13 |
| Mixed lobular carcinoma and another special type (ICD-O-3.2 term; the ICCR reports mixed types) | 8524/3 | Infiltrating lobular mixed with other types of carcinoma (Preferred) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 2; Pfister 2022, PDF p. 13 |
| Medullary carcinoma (WHO 2019: invasive breast carcinoma of no special type with medullary pattern) | 8510/3 | Medullary carcinoma, NOS (Preferred) | occurs | option | Tan 2020, PDF p. 2; ICCR Invasive Breast 2022, PDF p. 12; Pfister 2022, PDF p. 13; Sosnowska-Sienkiewicz 2024, PMC section 72 |
| Invasive carcinoma of no special type with neuroendocrine differentiation | 8574/3 | Carcinoma with neuroendocrine differentiation (Synonym) | not_reported | picker | Tan 2020, PDF p. 3; Pfister 2022, PDF p. 13 |
| Inflammatory carcinoma (WHO 2019: a clinical presentation, not a subtype) | 8530/3 | Inflammatory carcinoma (Preferred) | occurs | option | Tan 2020, PDF p. 2; Pfister 2022, PDF p. 13; Sosnowska-Sienkiewicz 2024, PMC section 72 |
| Paget disease of the nipple | 8540/3 | Paget disease of nipple (Synonym) | not_reported | picker | ICD-O-3.1 manual, PDF p. 8; ICCR Invasive Breast 2022, PDF p. 2; Pfister 2022, PDF p. 13 |
| Fibromatosis-like metaplastic carcinoma | 8572/3 | Fibromatosis-like metaplastic carcinoma (Related) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 13 (table); Pfister 2022, PDF p. 13 |
| Metaplastic carcinoma with mesenchymal differentiation (chondroid, osseous) | 8571/3 | Adenocarcinoma with chondroid differentiation (Synonym) | not_reported | picker | ICCR Invasive Breast 2022, PDF p. 14 (table); Pfister 2022, PDF p. 13 |
| Encapsulated papillary carcinoma with invasion | 8504/3 | Encapsulated papillary carcinoma with invasion (Preferred) | not_reported | picker | Pfister 2022, PDF p. 13 |
| Phyllodes tumour, malignant (including periductal stromal tumour, now a phyllodes variant) | 9020/3 | Phyllodes tumor, malignant (Preferred) | occurs | option | Tan 2020, PDF p. 4; ICCR Invasive Breast 2022, PDF p. 8; Pfister 2022, PDF p. 13; Sosnowska-Sienkiewicz 2024, PMC section 2; Sosnowska-Sienkiewicz 2024, PMC section 76 |
| Juvenile fibroadenoma | 9030/0 | Juvenile fibroadenoma (Preferred) | occurs | exclusion | Pfister 2022, PDF p. 13 |
| Juvenile papillomatosis | — | none (none) | occurs | exclusion | Pfister 2022, PDF p. 13; Sosnowska-Sienkiewicz 2024, PMC section 33 |
| Fibroadenoma | 9010/0 | Fibroadenoma, NOS (Preferred) | common | exclusion | Pfister 2022, PDF p. 13; Sosnowska-Sienkiewicz 2024, PMC section 12 |
| Giant fibroadenoma | 9016/0 | Giant fibroadenoma (Preferred) | not_reported | exclusion | Pfister 2022, PDF p. 13 |
| Phyllodes tumour, benign | 9020/0 | Phyllodes tumor, benign (Preferred) | common | exclusion | Tan 2020, PDF p. 4; Sosnowska-Sienkiewicz 2024, PMC section 77 |
| Phyllodes tumour, borderline, or with no grade stated | 9020/1 | Phyllodes tumor, NOS (Synonym) | not_reported | exclusion | Tan 2020, PDF p. 3 |
| Ductal carcinoma in situ | 8500/2 | Ductal carcinoma in situ, NOS (Related) | not_reported | exclusion | ICCR Invasive Breast 2022, PDF p. 7 |
| Lobular carcinoma in situ, classic or florid | 8520/2 | Lobular carcinoma in situ, NOS (Preferred) | not_reported | exclusion | Tan 2020, PDF p. 2 |
| Lobular carcinoma in situ, pleomorphic | 8519/2 | Lobular carcinoma in situ, pleomorphic (Preferred) | not_reported | exclusion | Tan 2020, PDF p. 2 |
| Encapsulated papillary carcinoma, without invasion | 8504/2 | Encapsulated papillary carcinoma (Preferred) | not_reported | exclusion | — |
| Solid papillary carcinoma in situ | 8509/2 | Solid papillary carcinoma in situ (Preferred) | not_reported | exclusion | Tan 2020, PDF p. 3 |
| Paget disease of the nipple, called in situ by the pathologist | 8540/2 | none (none) | not_reported | exclusion | ICD-O-3.1 manual, PDF p. 8; ICD-O-3.1 manual, PDF p. 2 |
| Intraductal papilloma (ICD-O-3.2 term; a benign breast tumour the clerk may meet) | 8503/0 | Intraductal papilloma (Preferred) | occurs | exclusion | Sosnowska-Sienkiewicz 2024, PMC section 25 |
| Intraductal papillomatosis (ICD-O-3.2 term; a benign breast tumour the clerk may meet) | 8505/0 | Intraductal papillomatosis, NOS (Preferred) | not_reported | exclusion | — |
| Adenoma of the nipple (ICD-O-3.2 term; a benign breast tumour the clerk may meet) | 8506/0 | Adenoma of nipple (Preferred) | not_reported | exclusion | — |
| Lactating adenoma (ICD-O-3.2 term; a benign breast tumour the clerk may meet) | 8204/0 | Lactating adenoma (Preferred) | not_reported | exclusion | — |
| Adenomyoepithelioma, benign (ICD-O-3.2 term; a benign breast tumour the clerk may meet) | 8983/0 | Adenomyoepithelioma, benign (Related) | not_reported | exclusion | — |
| Tubular adenoma of the breast | 8211/0 | Tubular adenoma, NOS (Preferred) | occurs | exclusion | Sosnowska-Sienkiewicz 2024, PMC section 2 |
| Malignant tumour on clinical information or imaging only | 8000/3 | Neoplasm, malignant (Preferred) | not_reported | refer → Group 12 | — |
| Malignant cells on cytology, no tumour type named | 8001/3 | Tumor cells, malignant (Preferred) | not_reported | refer → Group 12 | — |
| Myoepithelial carcinoma, named on its own | 8982/3 | Myoepithelial carcinoma (Preferred) | not_reported | refer → Group 12 | ICCR Invasive Breast 2022, PDF p. 13 (table) |
| Malignant mixed tumour | 8940/3 | Mixed tumor, malignant, NOS (Preferred) | not_reported | refer → Group 12 | — |
| Sarcoma of the breast | 8800/3 | Sarcoma, NOS (Preferred) | not_reported | refer → Group 9 | — |
| Breast implant-associated anaplastic large cell lymphoma, and other lymphomas of the breast | 9715/3 | Breast implant-associated anaplastic large cell lymphoma (Related) | not_reported | refer → Group 2 | ICD-O-3.1 manual, PDF p. 2 |
| Myeloid sarcoma in the breast | 9930/3 | Myeloid sarcoma (Preferred) | not_reported | refer → Group 1 | ICD-O-3.1 manual, PDF p. 2 |
| Melanoma at the breast or the skin of the breast | 8720/3 | Malignant melanoma, NOS (Preferred) | not_reported | refer | — |
| Cystic hypersecretory carcinoma | 8508/3 | Cystic hypersecretory carcinoma (Preferred) | not_reported | not_built | — |
| Medullary carcinoma with lymphoid stroma | 8512/3 | Medullary carcinoma with lymphoid stroma (Preferred) | not_reported | not_built | Tan 2020, PDF p. 2 |

Notes on the decisions:

- **Carcinoma with no type named (ICD-O-3.2 term; the fallback for a report that names no type)** (8010/3): The fallback code on the histology screen for a carcinoma whose report names no type. No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13).
- **Invasive breast carcinoma of no special type** (8500/3): The commonest breast carcinoma overall (Tan 2020, PDF p. 1). ICD-O prints the breast beside Infiltrating duct carcinoma, NOS (Rule H, Table 23). A review of breast lesions in children and adolescents lists invasive ductal carcinoma among the less common subtypes of breast cancer in children, and its summary table of breast lesions in the paediatric population lists invasive ductal carcinoma among the malignant lesions (Sosnowska-Sienkiewicz 2024, PMC sections 72 and 76). It is an answer on the breast histology screen; its picker entry stays, because the microinvasion answer on br_not_malignant leads to the picker.
- **Invasive lobular carcinoma** (8520/3): ICD-O-3.2 lists Tubulolobular carcinoma and Lobular carcinoma, pleomorphic under this code; the ICCR lists classical, pleomorphic, solid, alveolar, tubulolobular and mixed subtypes under 8520/3. A review of breast lesions in children and adolescents lists invasive lobular carcinoma among the less common subtypes of breast cancer in children (Sosnowska-Sienkiewicz 2024, PMC section 72). It is an answer on the breast histology screen; its picker entry stays.
- **Tubular carcinoma** (8211/3): No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13). It goes in the breast carcinoma picker.
- **Invasive cribriform carcinoma** (8201/3): No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13). It goes in the breast carcinoma picker.
- **Mucinous carcinoma** (8480/3): No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13). It goes in the breast carcinoma picker.
- **Invasive micropapillary carcinoma** (8507/3): No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13). It goes in the breast carcinoma picker.
- **Carcinoma with apocrine differentiation** (8401/3): ICD-O-3.2 prints no term with the WHO wording; the WHO table gives 8401/3, whose ICD-O-3.2 synonym is Apocrine carcinoma. No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13). It goes in the breast carcinoma picker.
- **Metaplastic carcinoma** (8575/3): The WHO table gives 8575/3 to every metaplastic subtype: low grade adenosquamous, fibromatosis-like, squamous cell, spindle cell or myoepithelial, with mesenchymal differentiation, and mixed. No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13). It goes in the breast carcinoma picker.
- **Invasive breast carcinoma of no special type, oncocytic pattern** (8290/3): The WHO 2019 classification treats oncocytic carcinoma as a pattern of no special type and still prints 8290/3 beside it (ICCR Table 1). No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13). It goes in the breast carcinoma picker.
- **Invasive breast carcinoma of no special type, lipid-rich pattern** (8314/3): A special pattern of no special type with its own printed code. No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13). It goes in the breast carcinoma picker.
- **Invasive breast carcinoma of no special type, glycogen-rich pattern** (8315/3): A special pattern of no special type with its own printed code. No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13). It goes in the breast carcinoma picker.
- **Invasive breast carcinoma of no special type, sebaceous pattern** (8410/3): A special pattern of no special type with its own printed code. No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13). It goes in the breast carcinoma picker.
- **Mucinous cystadenocarcinoma** (8470/3): New in the WHO 2019 breast volume. ICD-O prints the ovary beside this term (Rule H, Table 23); at the breast the breast entity is meant, so the ICD-O site is disregarded. No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13). It goes in the breast carcinoma picker.
- **Acinic cell carcinoma** (8550/3): No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13). It goes in the breast carcinoma picker.
- **Adenoid cystic carcinoma** (8200/3): No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13). It goes in the breast carcinoma picker.
- **Secretory carcinoma** (8502/3): ICD-O-3.2 lists Juvenile carcinoma of breast as a related term under this code. A review of breast lesions in children and adolescents names invasive secretory carcinoma the commonest subtype of invasive breast cancer in children (Sosnowska-Sienkiewicz 2024, PMC section 72). It is an answer on the breast histology screen, first among the carcinomas; its picker entry stays.
- **Mucoepidermoid carcinoma** (8430/3): No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13). It goes in the breast carcinoma picker.
- **Polymorphous adenocarcinoma** (8525/3): No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13). It goes in the breast carcinoma picker.
- **Solid papillary carcinoma, invasive** (8509/3): 8509 is new in ICD-O-3.2 (currency check section 6). No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13). It goes in the breast carcinoma picker.
- **Invasive papillary carcinoma** (8503/3): No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13). It goes in the breast carcinoma picker.
- **Neuroendocrine tumour** (8240/3): For a well-differentiated neuroendocrine tumour, the WHO advises excluding a deposit from another site first (Tan 2020, PDF p. 3). No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13). It goes in the breast carcinoma picker.
- **Neuroendocrine carcinoma** (8246/3): No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13). It goes in the breast carcinoma picker.
- **Tall cell carcinoma with reversed polarity** (8509/3): The WHO 2019 breast table gives this entity 8509/3, the code it shares with invasive solid papillary carcinoma (ICCR Table 1, PDF p. 14). ICD-O-3.2 prints no term for it; its Preferred term at 8509/3 is Solid papillary carcinoma with invasion. No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13). It goes in the picker as its own entry, with the shared code stated in the reason (registrar question 3).
- **Malignant adenomyoepithelioma** (8983/3): ICD-O-3.2 lists Malignant adenomyoepithelioma as a synonym of Adenomyoepithelioma with carcinoma (8983/3), but the ICCR table prints 8562/3 (Epithelial-myoepithelial carcinoma) beside it. The picker follows ICD-O-3.2, the coding authority, and the registrar rules on the discrepancy (registrar question 4). No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13).
- **Epithelial-myoepithelial carcinoma (ICD-O-3.2 term; the ICCR table prints its code beside malignant adenomyoepithelioma)** (8562/3): A current ICD-O-3.2 code that ICCC-2017 places in XIf6 at the breast. No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13).
- **Small cell neuroendocrine carcinoma** (8041/3): The WHO 2019 volume states that small cell neuroendocrine carcinoma arises in the breast (Tan 2020, PDF p. 3). No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13).
- **Large cell neuroendocrine carcinoma** (8013/3): Added as a breast entity in the WHO 2019 volume (Tan 2020, PDF p. 3). No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13).
- **Mixed carcinoma of no special type and invasive lobular carcinoma** (8522/3): The ICCR reports a mixed carcinoma when a special type forms 10 to 90 per cent of the tumour; ICD-O-3.2 has one code that names both parts, so Rule K does not apply. No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13).
- **Mixed carcinoma of no special type and another special type** (8523/3): ICD-O-3.2 lists Infiltrating duct and mucinous, tubular, cribriform and colloid carcinoma as related terms under this code. No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13).
- **Mixed lobular carcinoma and another special type (ICD-O-3.2 term; the ICCR reports mixed types)** (8524/3): No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13).
- **Medullary carcinoma (WHO 2019: invasive breast carcinoma of no special type with medullary pattern)** (8510/3): The WHO 2019 volume no longer treats medullary carcinoma as a separate entity but as a pattern of no special type (Tan 2020, PDF p. 2; ICCR, PDF p. 12). ICD-O-3.2 keeps 8510/3 current. A report that still says medullary carcinoma records 8510/3; whether a report of no special type with medullary pattern records 8500/3 or 8510/3 waits on the registrar (registrar question 2). A review of breast lesions in children and adolescents lists medullary carcinoma among the less common subtypes of breast cancer in children (Sosnowska-Sienkiewicz 2024, PMC section 72). It is an answer on the breast histology screen for a report that names medullary carcinoma; its picker entry stays.
- **Invasive carcinoma of no special type with neuroendocrine differentiation** (8574/3): The WHO 2019 volume classifies most breast cancers with neuroendocrine expression as invasive carcinoma of no special type with neuroendocrine differentiation (Tan 2020, PDF p. 3). ICD-O-3.2 lists Carcinoma with neuroendocrine differentiation at 8574/3. Whether that report records 8500/3 or 8574/3 waits on the registrar (registrar question 2). No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13).
- **Inflammatory carcinoma (WHO 2019: a clinical presentation, not a subtype)** (8530/3): The WHO 2019 volume treats inflammatory breast carcinoma as a clinical presentation rather than a special subtype (Tan 2020, PDF p. 2). ICD-O-3.2 keeps 8530/3 current; registrar question 2 covers which code a report of a named type with inflammatory presentation records. A review of breast lesions in children and adolescents lists inflammatory carcinoma among the less common subtypes of breast cancer in children (Sosnowska-Sienkiewicz 2024, PMC section 72). It is an answer on the breast histology screen for a report that names inflammatory carcinoma; its picker entry stays.
- **Paget disease of the nipple** (8540/3): ICD-O treats Paget disease of the nipple as malignant; a pathologist who calls it in situ is followed (Rule F; ICD-O-3.1 manual, PDF p. 8). The nipple is C50.0. ICCC-2017 places 8540/3 at C44 in XIe, so Paget disease of the skin of the breast belongs to the skin part. No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13).
- **Fibromatosis-like metaplastic carcinoma** (8572/3): ICD-O-3.2 lists this exact term under 8572/3, while the WHO table places it under metaplastic carcinoma, 8575/3. Both codes are XIf6 at the breast; which one the report records waits on the registrar (registrar question 5). No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13).
- **Metaplastic carcinoma with mesenchymal differentiation (chondroid, osseous)** (8571/3): ICD-O-3.2 has Adenocarcinoma with cartilaginous and osseous metaplasia at 8571/3; the WHO table places this subtype under metaplastic carcinoma, 8575/3 (registrar question 5). It is a carcinoma, not a bone or soft-tissue sarcoma. No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13).
- **Encapsulated papillary carcinoma with invasion** (8504/3): ICD-O-3.2 moved Intracystic carcinoma, NOS from /3 to /2; 8504/3 is now Encapsulated papillary carcinoma with invasion (currency check section 3). The ICCR invasive table does not list it. No source held for this part reports it in children: the paediatric breast chapter lists only juvenile fibroadenoma and juvenile papillomatosis (Pfister 2022 Table 3, PDF p. 13).
- **Phyllodes tumour, malignant (including periductal stromal tumour, now a phyllodes variant)** (9020/3): ICCC-2017 places 9020/3 in XIf6 at the breast, so it stays in Group XI. It is offered on the fibroepithelial screen because that screen must separate the malignant grade from the benign and borderline grades and from juvenile fibroadenoma, which the WHO paediatric volume lists (Pfister 2022 Table 3, PDF p. 13). A review of breast lesions in children and adolescents lists malignant phyllodes tumour among the primary malignant breast lesions of children and adolescents (Sosnowska-Sienkiewicz 2024, PMC sections 2 and 76), which answers registrar question 6. ICD-O-3.2 lists Periductal stromal tumor, low grade, under this code.
- **Juvenile fibroadenoma** (9030/0): The WHO paediatric volume lists juvenile fibroadenoma among breast tumours of children (Pfister 2022 Table 3, PDF p. 13). ICD-O-3.2 gives it 9030/0 only. Group XI declares behaviour /3 only; the tree records the exclusion and registers nothing from this report.
- **Juvenile papillomatosis** (no code): The WHO paediatric volume lists juvenile papillomatosis among breast tumours of children (Pfister 2022 Table 3, PDF p. 13). ICD-O-3.2 prints no term for it and gives it no malignant code. Intraductal papillomatosis, NOS (8505/0) is a different entity and is not used for it. Group XI declares behaviour /3 only; the tree records the exclusion and registers nothing from this report. A review of breast lesions in children and adolescents calls juvenile papillomatosis benign and associates it with carcinoma in up to 15 per cent of cases (Sosnowska-Sienkiewicz 2024, PMC section 33).
- **Fibroadenoma** (9010/0): Benign fibroepithelial tumour. Group XI declares behaviour /3 only; the tree records the exclusion and registers nothing from this report. Fibroadenoma is the commonest breast tumour of adolescents, 95 per cent of breast lesions (Sosnowska-Sienkiewicz 2024, PMC section 12).
- **Giant fibroadenoma** (9016/0): Benign fibroepithelial tumour. Group XI declares behaviour /3 only; the tree records the exclusion and registers nothing from this report.
- **Phyllodes tumour, benign** (9020/0): Benign grade. Group XI declares behaviour /3 only; the tree records the exclusion and registers nothing from this report. In children and adolescents the commonest histological diagnoses are fibroadenoma and benign phyllodes tumour (Sosnowska-Sienkiewicz 2024, PMC section 77).
- **Phyllodes tumour, borderline, or with no grade stated** (9020/1): ICD-O-3.2 lists Phyllodes tumor, NOS as a synonym under 9020/1 (Preferred: Phyllodes tumor, borderline), so a phyllodes tumour reported with no grade is not malignant. Group XI declares behaviour /3 only; the tree records the exclusion and registers nothing from this report.
- **Ductal carcinoma in situ** (8500/2): The ICCR invasive dataset covers invasive carcinoma with or without ductal carcinoma in situ and leaves ductal carcinoma in situ alone to a separate dataset. Its patterns carry their own /2 codes (cribriform 8201/2, papillary 8503/2, micropapillary 8507/2). Group XI declares behaviour /3 only; the tree records the exclusion and registers nothing from this report.
- **Lobular carcinoma in situ, classic or florid** (8520/2): The WHO 2019 volume recognises classic, pleomorphic and florid lobular carcinoma in situ (Tan 2020, PDF p. 2). Group XI declares behaviour /3 only; the tree records the exclusion and registers nothing from this report.
- **Lobular carcinoma in situ, pleomorphic** (8519/2): Group XI declares behaviour /3 only; the tree records the exclusion and registers nothing from this report.
- **Encapsulated papillary carcinoma, without invasion** (8504/2): ICD-O-3.2 moved 8504 Intracystic carcinoma, NOS from /3 to /2 (currency check section 3); Intracystic papillary carcinoma is a /2 synonym. Group XI declares behaviour /3 only; the tree records the exclusion and registers nothing from this report.
- **Solid papillary carcinoma in situ** (8509/2): The WHO 2019 volume describes solid papillary carcinoma of both in situ and invasive types (Tan 2020, PDF p. 3). Group XI declares behaviour /3 only; the tree records the exclusion and registers nothing from this report.
- **Paget disease of the nipple, called in situ by the pathologist** (8540/2): ICD-O-3.2 prints no /2 term at 8540. Rule F codes the behaviour the pathologist states, and the ICD-O manual uses this tumour as its example (ICD-O-3.1 manual, PDF p. 8). Group XI declares behaviour /3 only; the tree records the exclusion and registers nothing from this report.
- **Intraductal papilloma (ICD-O-3.2 term; a benign breast tumour the clerk may meet)** (8503/0): Benign. Group XI declares behaviour /3 only; the tree records the exclusion and registers nothing from this report. Intraductal papilloma occurs in children, very rarely (Sosnowska-Sienkiewicz 2024, PMC section 25).
- **Intraductal papillomatosis (ICD-O-3.2 term; a benign breast tumour the clerk may meet)** (8505/0): Benign. REDCap offers 8204, 8505 and 8506 under XIf although they have no malignant form (currency check section 5). Group XI declares behaviour /3 only; the tree records the exclusion and registers nothing from this report.
- **Adenoma of the nipple (ICD-O-3.2 term; a benign breast tumour the clerk may meet)** (8506/0): Benign. REDCap offers 8204, 8505 and 8506 under XIf although they have no malignant form (currency check section 5). Group XI declares behaviour /3 only; the tree records the exclusion and registers nothing from this report.
- **Lactating adenoma (ICD-O-3.2 term; a benign breast tumour the clerk may meet)** (8204/0): Benign. REDCap offers 8204, 8505 and 8506 under XIf although they have no malignant form (currency check section 5). Group XI declares behaviour /3 only; the tree records the exclusion and registers nothing from this report.
- **Adenomyoepithelioma, benign (ICD-O-3.2 term; a benign breast tumour the clerk may meet)** (8983/0): Benign. Group XI declares behaviour /3 only; the tree records the exclusion and registers nothing from this report.
- **Tubular adenoma of the breast** (8211/0): A review of breast lesions in children and adolescents lists tubular adenoma among the benign breast lesions of children and adolescents (Sosnowska-Sienkiewicz 2024, PMC section 2). ICD-O-3.2 gives Tubular adenoma, NOS 8211/0; its malignant code 8211/3 is Tubular adenocarcinoma, a different tumour. Group XI declares behaviour /3 only; the tree records the exclusion and registers nothing from this report. br_not_malignant has no answer of its own for it; its catch-all answer covers it (data gap 8).
- **Malignant tumour on clinical information or imaging only** (8000/3): A case with no tissue records 8000/3 (Visser 2023, from the controller's brief). ICCC-2017 places 8000/3 at C50 in XIIb, so the case is coded from the Group XII tree.
- **Malignant cells on cytology, no tumour type named** (8001/3): ICCC-2017 places 8001/3 at C50 in XIIb; the case is coded from the Group XII tree.
- **Myoepithelial carcinoma, named on its own** (8982/3): ICCC-2017 places 8982/3 in XIIa4 at every site. The WHO breast table lists spindle cell carcinoma or myoepithelial carcinoma as a subtype of metaplastic carcinoma (8575/3, XIf6), so the same tumour can land in Group XI or Group XII depending on the report's words (registrar question 5).
- **Malignant mixed tumour** (8940/3): ICCC-2017 places 8940/3 in XIIa4 at every site; coded from the Group XII tree.
- **Sarcoma of the breast** (8800/3): ICCC-2017 places Sarcoma, NOS (8800/3) at C50 in IXe and Hemangiosarcoma (9120/3) in IXd8; soft-tissue sarcomas of the breast are coded from the Group IX tree. The WHO 2019 volume moved mesenchymal tumours to a dedicated chapter (Tan 2020, PDF p. 4).
- **Breast implant-associated anaplastic large cell lymphoma, and other lymphomas of the breast** (9715/3): ICD-O-3.2 lists this as a related term of Anaplastic large cell lymphoma, ALK negative (9715/3). ICCC-2017 holds no 9715; the Group II tree carries it. A lymphoma that begins in the breast is recorded at the breast (Rule D).
- **Myeloid sarcoma in the breast** (9930/3): ICCC-2017 places 9930/3 in Ib at every site. Rule E keeps the breast site for a myeloid sarcoma; every other leukaemia is recorded at C42.1.
- **Melanoma at the breast or the skin of the breast** (8720/3): ICCC-2017 places 8720/3 in XId at every site. Melanoma is coded from the Group XI melanoma tree, not this part.
- **Cystic hypersecretory carcinoma** (8508/3): Every ICD-O-3.2 /3 term at 8508 is [obs] (currency check section 2). Neither source for this part names an invasive cystic hypersecretory carcinoma; ICD-O-3.2 lists Cystic hypersecretory carcinoma, intraductal at 8500/2. No successor is proposed (data gap 3).
- **Medullary carcinoma with lymphoid stroma** (8512/3): Every ICD-O-3.2 /3 term at 8512 is [obs] (currency check section 2). The WHO 2019 volume now calls carcinomas with medullary features invasive breast carcinoma of no special type with medullary pattern; ICD-O-3.2 gives that entity 8500/3 and keeps Medullary carcinoma, NOS at 8510/3 (registrar question 2).

### 2.2 Other current codes ICCC-2017 places in XIf6 at the breast

Each is a picker entry or, where every /3 term is [obs], not built. None is named by a source for this part at the breast. Pfister 2022 reports none of them in children (PDF p. 13). The source added 8 October 2026 reports one: Sosnowska-Sienkiewicz 2024 lists anaplastic carcinoma among the less common subtypes of breast cancer in children (PMC section 72), so Carcinoma, anaplastic, NOS (8021/3) is an option on br_histology and keeps its picker entry.

| Code | ICD-O-3.2 term | Decision |
|---|---|---|
| 8011/3 | Epithelioma, malignant | picker |
| 8012/3 | Large cell carcinoma, NOS | picker |
| 8014/3 | Large cell carcinoma with rhabdoid phenotype | picker |
| 8015/3 | Glassy cell carcinoma | picker |
| 8020/3 | Carcinoma, undifferentiated, NOS | picker |
| 8021/3 | Carcinoma, anaplastic, NOS | option |
| 8022/3 | Pleomorphic carcinoma | picker |
| 8023/3 | Nuclear protein in testis (NUT)-associated carcinoma | picker |
| 8030/3 | Giant cell and spindle cell carcinoma | picker |
| 8031/3 | Giant cell carcinoma | picker |
| 8032/3 | Spindle cell carcinoma, NOS | picker |
| 8033/3 | Pseudosarcomatous carcinoma | picker |
| 8034/3 | Polygonal cell carcinoma | picker |
| 8035/3 | Carcinoma with osteoclast-like giant cells | picker |
| 8042/3 | Oat cell carcinoma | not_built |
| 8043/3 | Small cell carcinoma, fusiform cell | picker |
| 8044/3 | Small cell carcinoma, intermediate cell | picker |
| 8045/3 | Combined small cell carcinoma | picker |
| 8046/3 | Non-small cell carcinoma | picker |
| 8050/3 | Papillary carcinoma, NOS | picker |
| 8051/3 | Verrucous carcinoma, NOS | picker |
| 8052/3 | Papillary squamous cell carcinoma | picker |
| 8054/3 | Warty carcinoma | picker |
| 8070/3 | Squamous cell carcinoma, NOS | picker |
| 8071/3 | Squamous cell carcinoma, keratinizing, NOS | picker |
| 8072/3 | Squamous cell carcinoma, large cell, nonkeratinizing, NOS | picker |
| 8073/3 | Squamous cell carcinoma, small cell, nonkeratinizing | picker |
| 8074/3 | Squamous cell carcinoma, spindle cell | picker |
| 8075/3 | Squamous cell carcinoma, adenoid | picker |
| 8076/3 | Squamous cell carcinoma, microinvasive | picker |
| 8082/3 | Lymphoepithelial carcinoma | picker |
| 8083/3 | Basaloid squamous cell carcinoma | picker |
| 8084/3 | Squamous cell carcinoma, clear cell type | picker |
| 8085/3 | Squamous cell carcinoma, HPV positive | picker |
| 8086/3 | Squamous cell carcinoma, HPV negative | picker |
| 8098/3 | Adenoid basal carcinoma | picker |
| 8120/3 | Transitional cell carcinoma, NOS | picker |
| 8121/3 | Schneiderian carcinoma | picker |
| 8122/3 | Urothelial carcinoma, sarcomatoid | picker |
| 8123/3 | Basaloid carcinoma | picker |
| 8124/3 | Cloacogenic carcinoma | not_built |
| 8130/3 | Papillary urothelial carcinoma | not_built |
| 8131/3 | Urothelial carcinoma, micropapillary | picker |
| 8140/3 | Adenocarcinoma, NOS | picker |
| 8141/3 | Scirrhous adenocarcinoma | not_built |
| 8142/3 | Linitis plastica | picker |
| 8143/3 | Superficial spreading adenocarcinoma | picker |
| 8144/3 | Adenocarcinoma, intestinal type | picker |
| 8145/3 | Carcinoma, diffuse type | picker |
| 8147/3 | Basal cell adenocarcinoma | picker |
| 8150/3 | Pancreatic neuroendocrine tumor, nonfunctioning | picker |
| 8151/3 | Insulinoma, NOS | picker |
| 8152/3 | Glucagonoma | picker |
| 8153/3 | Gastrinoma | picker |
| 8154/3 | Mixed neuroendocrine non-neuroendocrine neoplasm (MiNEN) | picker |
| 8155/3 | Vipoma | picker |
| 8156/3 | Somatostatinoma | picker |
| 8158/3 | ACTH-producing tumor | picker |
| 8163/3 | Pancreatobiliary type carcinoma | picker |
| 8190/3 | Trabecular adenocarcinoma | picker |
| 8210/3 | Adenocarcinoma in adenomatous polyp | picker |
| 8213/3 | Serrated adenocarcinoma | picker |
| 8214/3 | Parietal cell carcinoma | picker |
| 8215/3 | Adenocarcinoma of anal glands | picker |
| 8220/3 | Adenocarcinoma in adenomatous polyposis coli | picker |
| 8221/3 | Adenocarcinoma in multiple adenomatous polyps | picker |
| 8230/3 | Solid carcinoma, NOS | picker |
| 8231/3 | Carcinoma simplex | picker |
| 8241/3 | Enterochromaffin cell carcinoid | picker |
| 8242/3 | Enterochromaffin-like cell tumor | picker |
| 8243/3 | Goblet cell carcinoid | picker |
| 8244/3 | Mixed adenoneuroendocrine carcinoma | picker |
| 8245/3 | Adenocarcinoid tumor | not_built |
| 8247/3 | Merkel cell carcinoma | picker |
| 8249/3 | Neuroendocrine tumor, grade 2 | picker |
| 8250/3 | Lepidic adenocarcinoma | picker |
| 8251/3 | Alveolar adenocarcinoma | not_built |
| 8252/3 | Bronchiolo-alveolar carcinoma, non-mucinous | picker |
| 8253/3 | Adenocarcinoma of lung, mucinous | picker |
| 8254/3 | Adenocarcinoma of lung, mixed mucinous and non-mucinous | picker |
| 8255/3 | Adenocarcinoma with mixed subtypes | picker |
| 8256/3 | Minimally invasive adenocarcinoma, non-mucinous | picker |
| 8257/3 | Minimally invasive adenocarcinoma, mucinous | picker |
| 8260/3 | Papillary adenocarcinoma, NOS | picker |
| 8261/3 | Adenocarcinoma in villous adenoma | picker |
| 8262/3 | Villous adenocarcinoma | picker |
| 8263/3 | Adenocarcinoma in tubulovillous adenoma | picker |
| 8265/3 | Micropapillary carcinoma, NOS | picker |
| 8310/3 | Clear cell adenocarcinoma, NOS | picker |
| 8320/3 | Granular cell carcinoma | picker |
| 8322/3 | Water-clear cell adenocarcinoma | picker |
| 8323/3 | Mixed cell adenocarcinoma | picker |
| 8333/3 | Fetal adenocarcinoma | picker |
| 8380/3 | Endometrioid adenocarcinoma, NOS | picker |
| 8381/3 | Endometrioid adenofibroma, malignant | picker |
| 8382/3 | Endometrioid adenocarcinoma, secretory variant | picker |
| 8383/3 | Endometrioid adenocarcinoma, ciliated cell variant | picker |
| 8384/3 | Adenocarcinoma, endocervical type, NOS | picker |
| 8402/3 | Hidradenocarcinoma | picker |
| 8406/3 | Syringocystadenocarcinoma papilliferum | picker |
| 8440/3 | Cystadenocarcinoma, NOS | not_built |
| 8441/3 | Serous carcinoma, NOS | picker |
| 8450/3 | Papillary cystadenocarcinoma, NOS | not_built |
| 8452/3 | Solid pseudopapillary neoplasm of pancreas | picker |
| 8453/3 | Intraductal papillary mucinous neoplasm with an associated invasive carcinoma | picker |
| 8460/3 | Low grade serous carcinoma | picker |
| 8461/3 | High grade serous carcinoma | picker |
| 8481/3 | Mucin-producing adenocarcinoma | picker |
| 8482/3 | Mucinous carcinoma, gastric type | picker |
| 8490/3 | Signet ring cell carcinoma | picker |
| 8501/3 | Comedocarcinoma, NOS | picker |
| 8513/3 | Atypical medullary carcinoma | picker |
| 8514/3 | Duct carcinoma, desmoplastic type | picker |
| 8521/3 | Infiltrating ductular carcinoma | picker |
| 8541/3 | Paget disease and infiltrating duct carcinoma of breast | picker |
| 8542/3 | Paget disease, extramammary | picker |
| 8543/3 | Paget disease and intraductal carcinoma of breast | picker |
| 8551/3 | Acinar adenocarcinoma of lung | picker |
| 8552/3 | Mixed acinar-ductal carcinoma | picker |
| 8560/3 | Adenosquamous carcinoma | picker |
| 8570/3 | Adenocarcinoma with squamous metaplasia | picker |
| 8573/3 | Adenocarcinoma with apocrine metaplasia | picker |
| 8576/3 | Hepatoid adenocarcinoma | picker |
| 8580/3 | Thymoma, NOS | picker |
| 8581/3 | Thymoma, type A | picker |
| 8582/3 | Thymoma, type AB | picker |
| 8583/3 | Thymoma, type B1 | picker |
| 8584/3 | Thymoma, type B2 | picker |
| 8585/3 | Thymoma, type B3 | picker |
| 8586/3 | Thymic carcinoma, NOS | picker |
| 8589/3 | Intrathyroid thymic carcinoma | picker |
| 8941/3 | Carcinoma ex pleomorphic adenoma | picker |
| 9000/3 | Brenner tumor, malignant | picker |
| 9014/3 | Serous adenocarcinofibroma | picker |

## 3. The pathway

Nine screens. `melanoma_tree` and `sk_site` are entry nodes of the melanoma part (XId) and the skin part (XIe). Basis of diagnosis: clinical 1, imaging 2, cytology 5, histology 7.

### `br_document_inventory` — document_inventory

**Question:** What is in the file for this breast tumour?

**Hint:** A core needle biopsy, excision or mastectomy report counts as histology. An immunohistochemistry or gene report on its own does not stand in for a histology report.

| Option | Outcome | Records | Reason | Recognition aid | Page |
|---|---|---|---|---|---|
| A referral letter or clinical note only — no imaging report, no tissue | go → `br_clinical` | basis 1 | — | — | — |
| An imaging report only — mammogram, ultrasound or magnetic resonance imaging; no tissue | go → `br_imaging` | basis 2 | — | — | ICCR Invasive Breast 2022, PDF p. 9 |
| Cytology only — a fine-needle aspirate or a smear; no tissue | go → `br_cytology` | basis 5 | — | — | Tan 2020, PDF p. 1 |
| A histology report — core needle biopsy, excision or mastectomy, with or without immunohistochemistry or gene reports | go → `br_site` | basis 7 | — | — | Tan 2020, PDF p. 1; ICCR Invasive Breast 2022, PDF p. 8 |

### `br_clinical` — clinical_alias

**Question:** What does the referral letter or clinical note say?

| Option | Outcome | Records | Reason | Recognition aid | Page |
|---|---|---|---|---|---|
| The note states a malignant breast tumour as the diagnosis, or as probable | refer → Group 12 | 8000/3, basis 1 | A diagnosis resting on clinical information alone is registered as Neoplasm, malignant (8000/3). ICCC-3 places 8000/3 at the breast in Group XII, so the case is coded from the Group XII tree. | — | — |
| The note names melanoma of the skin of the breast | go → `melanoma_tree` | basis 1 | Melanoma of the skin is coded from the melanoma tree, which registers it on clinical information (8720/3, basis 1). | — | — |
| The note says only possible or suspected | not_registrable | — | Cancer is only possible on this evidence. A case that is only possibly cancer is not registered without pathology. | — | — |
| An imaging report is in the file after all | go → `br_imaging` | — | — | — | — |

### `br_imaging` — morphology_only

**Question:** No tissue is in the file. What does the imaging report conclude?

| Option | Outcome | Records | Reason | Recognition aid | Page |
|---|---|---|---|---|---|
| Imaging shows a malignant breast tumour, at least probable | refer → Group 12 | 8000/3, basis 2 | A diagnosis resting on imaging alone is registered as Neoplasm, malignant (8000/3). ICCC-3 places 8000/3 at the breast in Group XII, so the case is coded from the Group XII tree. | — | — |
| Imaging calls it possible only, or describes a benign lesion such as a fibroadenoma | not_registrable | — | Cancer is only possible on this evidence. A case that is only possibly cancer is not registered without pathology. | — | — |
| A histology report is in the file after all | go → `br_site` | — | — | — | — |

### `br_cytology` — morphology_only

**Question:** What does the cytology report conclude?

**Hint:** Cytology does not give a histological type. A histology report, when one arrives, confirms the type.

| Option | Outcome | Records | Reason | Recognition aid | Page |
|---|---|---|---|---|---|
| Cytology names a carcinoma, with or without a type | code | 8010/3, basis 5 | Recorded as Carcinoma, NOS (8010/3) at basis of diagnosis 5. | — | ICCR Invasive Breast 2022, PDF p. 12 |
| Cytology names melanoma | go → `melanoma_tree` | — | Melanoma is coded from the melanoma tree. | — | — |
| Cytology names a lymphoma | refer → Group 2 | — | A lymphoma in the breast is coded from the Group II (lymphomas) tree, at the breast (C50). | — | — |
| Cytology names a sarcoma | refer → Group 9 | — | Soft-tissue sarcomas are coded from the Group IX (soft-tissue sarcomas) tree. | — | — |
| Cytology names a fibroadenoma, a phyllodes tumour or another fibroepithelial lesion | not_registrable | — | Whether a phyllodes tumour is malignant is decided on histology. The case is not registered from this report. | — | Tan 2020, PDF p. 3 |
| Malignant cells are present, with no tumour type named | refer → Group 12 | 8001/3, basis 5 | Cytology establishes malignant cells but no tumour type. ICCC-3 places Tumor cells, malignant (8001/3) at the breast in Group XII, so the case is coded from the Group XII tree. | — | — |
| No malignant cells, scant material, or a non-diagnostic report — and an imaging report is in the file | go → `br_imaging` | — | — | — | — |
| No malignant cells, scant material, or a non-diagnostic report — and no imaging report is in the file | go → `br_clinical` | — | — | — | — |

### `br_site` — site_resolution

**Question:** Which part of the breast does the report name?

**Hint:** Choose the quadrant or part the report names. If the report gives only a clock-face position, choose breast, part not stated. A carcinoma described with a prefix such as periareolar or retroareolar is still a breast tumour: choose the part the report names, or breast, part not stated. Choose overlapping only for a single tumour that crosses two or more parts when the report does not say where it began. A tumour of the skin of the breast is a skin tumour.

| Option | Outcome | Records | Reason | Recognition aid | Page |
|---|---|---|---|---|---|
| Nipple or areola | go → `br_histology` | C50.0 | — | — | ICCR Invasive Breast 2022, PDF p. 2 |
| Central portion of the breast | go → `br_histology` | C50.1 | — | — | ICCR Invasive Breast 2022, PDF p. 2 |
| Upper inner quadrant | go → `br_histology` | C50.2 | — | — | ICCR Invasive Breast 2022, PDF p. 2 |
| Lower inner quadrant | go → `br_histology` | C50.3 | — | — | ICCR Invasive Breast 2022, PDF p. 2 |
| Upper outer quadrant | go → `br_histology` | C50.4 | — | — | ICCR Invasive Breast 2022, PDF p. 2 |
| Lower outer quadrant | go → `br_histology` | C50.5 | — | — | ICCR Invasive Breast 2022, PDF p. 2 |
| Axillary tail of the breast | go → `br_histology` | C50.6 | — | — | — |
| One tumour crossing more than one part, and the report does not say where it began | go → `br_histology` | C50.8 | — | — | ICD-O-3.1 manual, PDF p. 5 |
| Breast, part not stated — or a clock-face position only | go → `br_histology` | C50.9 | — | — | ICCR Invasive Breast 2022, PDF p. 8 |
| Skin of the breast | go → `sk_site` | C44.5 | A tumour of the skin of the breast is coded from the skin tree, at skin of trunk (C44.5); the breast (C50) does not include its skin. | — | — |

### `br_histology` — histology_subclassification

**Question:** What does the histology report call the tumour?

**Hint:** Use the report's own term. When a core needle biopsy and a later excision both name a type, use the excision report. If the report states that the tumour is benign, in situ or of uncertain malignant potential, choose that answer, even for a tumour type that is usually malignant.

| Option | Outcome | Records | Reason | Recognition aid | Page |
|---|---|---|---|---|---|
| Secretory carcinoma (also called juvenile carcinoma) | code | 8502/3, basis 7 | Recorded as Secretory carcinoma (8502/3), the ICD-O-3.2 Preferred term; ICD-O-3.2 lists Juvenile carcinoma of breast under the same code. | The report may call it invasive secretory carcinoma (ISC). | Sosnowska-Sienkiewicz 2024, PMC section 72 |
| Invasive ductal carcinoma, or invasive carcinoma of no special type | code | 8500/3, basis 7 | Recorded as Infiltrating duct carcinoma, NOS (8500/3), the ICD-O-3.2 Preferred term for invasive breast carcinoma of no special type. | — | Sosnowska-Sienkiewicz 2024, PMC section 72; Sosnowska-Sienkiewicz 2024, PMC section 76 |
| Invasive lobular carcinoma | code | 8520/3, basis 7 | Recorded as Lobular carcinoma, NOS (8520/3), the ICD-O-3.2 Preferred term; Infiltrating lobular carcinoma, NOS is its synonym. | — | Sosnowska-Sienkiewicz 2024, PMC section 72 |
| Medullary carcinoma | code | 8510/3, basis 7 | Recorded as Medullary carcinoma, NOS (8510/3), the ICD-O-3.2 Preferred term. | — | Sosnowska-Sienkiewicz 2024, PMC section 72 |
| Inflammatory carcinoma | code | 8530/3, basis 7 | Recorded as Inflammatory carcinoma (8530/3), the ICD-O-3.2 Preferred term. | — | Sosnowska-Sienkiewicz 2024, PMC section 72 |
| Anaplastic carcinoma | code | 8021/3, basis 7 | Recorded as Carcinoma, anaplastic, NOS (8021/3), the ICD-O-3.2 Preferred term. | — | Sosnowska-Sienkiewicz 2024, PMC section 72 |
| An invasive carcinoma of a named type — for example no special type (ductal), lobular, secretory, mucinous, papillary, metaplastic or neuroendocrine | go → `br_carcinoma_picker` | — | — | — | ICCR Invasive Breast 2022, PDF p. 13 (table); ICCR Invasive Breast 2022, PDF p. 12 |
| Carcinoma, with no type named | code | 8010/3, basis 7 | Recorded as Carcinoma, NOS (8010/3). | — | — |
| Fibroadenoma or phyllodes tumour | go → `br_fibroepithelial` | — | — | — | Pfister 2022, PDF p. 13 |
| Benign, in situ, or of uncertain malignant potential — the report says so, for example ductal carcinoma in situ | go → `br_not_malignant` | — | — | — | ICD-O-3.1 manual, PDF p. 2 |
| Melanoma | go → `melanoma_tree` | — | Melanoma is coded from the melanoma tree. | — | — |
| Lymphoma, including breast implant-associated anaplastic large cell lymphoma | refer → Group 2 | — | Lymphomas are coded from the Group II (lymphomas) tree. A lymphoma that begins in the breast is recorded at the breast (C50). | — | ICD-O-3.1 manual, PDF p. 2 |
| Leukaemia in the breast, or myeloid sarcoma | refer → Group 1 | — | Leukaemias are coded from the Group I tree. A leukaemia is recorded at bone marrow (C42.1); a myeloid sarcoma keeps its breast site. | — | ICD-O-3.1 manual, PDF p. 2 |
| Sarcoma or another malignant soft-tissue tumour | refer → Group 9 | — | Soft-tissue sarcomas of the breast are coded from the Group IX (soft-tissue sarcomas) tree. | A report that calls the tumour metaplastic carcinoma, even with chondroid or osseous differentiation, names a carcinoma, and a phyllodes tumour is answered under fibroadenoma or phyllodes tumour. | ICCR Invasive Breast 2022, PDF p. 14 (table) |
| Myoepithelial carcinoma or malignant mixed tumour, named on its own | refer → Group 12 | — | ICCC-3 places Myoepithelial carcinoma (8982/3) and Mixed tumor, malignant, NOS (8940/3) in Group XII at every site, so the case is coded from the Group XII tree. | A report that names metaplastic carcinoma with a spindle cell or myoepithelial pattern names a carcinoma: choose the named carcinoma answer. | ICCR Invasive Breast 2022, PDF p. 13 (table) |
| A deposit (metastasis) of a tumour that began elsewhere | refer → primary site (recapture site) | — | A deposit in the breast is coded at the tumour's primary site. The next screen asks where the tumour began. | The report calls the tumour metastatic, or names a tumour of another organ, such as a neuroendocrine tumour shown to come from elsewhere. | Tan 2020, PDF p. 3; ICD-O-3.1 manual, PDF p. 10 |

### `br_fibroepithelial` — histology_subclassification

**Question:** Which fibroadenoma or phyllodes tumour does the report name?

**Hint:** Choose the grade the report states: benign, borderline or malignant. A phyllodes tumour reported with no grade is answered as borderline.

| Option | Outcome | Records | Reason | Recognition aid | Page |
|---|---|---|---|---|---|
| Juvenile fibroadenoma | exclude | 9030/0 | Juvenile fibroadenoma (9030/0) is benign. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | — | Pfister 2022, PDF p. 13 |
| Giant fibroadenoma | exclude | 9016/0 | Giant fibroadenoma (9016/0) is benign. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | — | — |
| Fibroadenoma of any other kind | exclude | 9010/0 | Fibroadenoma, NOS (9010/0) is benign. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | — | — |
| Phyllodes tumour, benign | exclude | 9020/0 | Phyllodes tumor, benign (9020/0) is benign. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | — | — |
| Phyllodes tumour, borderline — or with no grade stated | exclude | 9020/1 | Phyllodes tumor, borderline (9020/1) is of uncertain behaviour; ICD-O-3.2 lists Phyllodes tumor, NOS under the same code. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | — | — |
| Phyllodes tumour, malignant — or periductal stromal tumour | code | 9020/3, basis 7 | Recorded as Phyllodes tumor, malignant (9020/3). ICD-O-3.2 lists Periductal stromal tumor, low grade, under this code. | The report itself calls the phyllodes tumour malignant; a well-differentiated liposarcoma-like component on its own does not make it malignant. | Tan 2020, PDF p. 4 |

### `br_not_malignant` — histology_subclassification

**Question:** Which benign, in situ or uncertain tumour does the report name?

**Hint:** These tumours are benign, in situ or of uncertain behaviour, and the registry records malignant tumours (behaviour /3) only. An in situ carcinoma with microinvasion (invasion of 1 mm or less) is an invasive carcinoma.

| Option | Outcome | Records | Reason | Recognition aid | Page |
|---|---|---|---|---|---|
| In situ carcinoma with microinvasion — invasion of 1 mm or less | go → `br_carcinoma_picker` | — | Microinvasion is invasion: the tumour is coded as an invasive carcinoma of the type the report names. | — | ICCR Invasive Breast 2022, PDF p. 7 |
| Ductal carcinoma in situ, of any pattern or grade | exclude | 8500/2 | Ductal carcinoma in situ is in situ (behaviour /2): Intraductal carcinoma, noninfiltrating, NOS (8500/2); its patterns carry their own /2 codes. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | — | ICCR Invasive Breast 2022, PDF p. 7 |
| Lobular carcinoma in situ, classic or florid | exclude | 8520/2 | Lobular carcinoma in situ, NOS (8520/2) is in situ. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | — | Tan 2020, PDF p. 2 |
| Lobular carcinoma in situ, pleomorphic | exclude | 8519/2 | Lobular carcinoma in situ, pleomorphic (8519/2) is in situ. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | — | Tan 2020, PDF p. 2 |
| Encapsulated papillary carcinoma or intracystic papillary carcinoma, with no invasion | exclude | 8504/2 | Encapsulated papillary carcinoma (8504/2) is in situ. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | — | — |
| Solid papillary carcinoma in situ | exclude | 8509/2 | Solid papillary carcinoma in situ (8509/2) is in situ. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | — | Tan 2020, PDF p. 3 |
| Paget disease of the nipple, which the report calls in situ | exclude | 8540/2 | The pathologist states an in situ behaviour, so it is recorded as in situ (/2), as the ICD-O rules direct. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | — | ICD-O-3.1 manual, PDF p. 8; ICD-O-3.1 manual, PDF p. 2 |
| Juvenile papillomatosis | exclude | — | Juvenile papillomatosis has no malignant code in ICD-O-3.2. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | — | Pfister 2022, PDF p. 13 |
| Intraductal papilloma | exclude | 8503/0 | Intraductal papilloma (8503/0) is benign. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | — | — |
| Intraductal papillomatosis | exclude | 8505/0 | Intraductal papillomatosis, NOS (8505/0) is benign. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | — | — |
| Adenoma of the nipple | exclude | 8506/0 | Adenoma of nipple (8506/0) is benign. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | — | — |
| Lactating adenoma | exclude | 8204/0 | Lactating adenoma (8204/0) is benign. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | — | — |
| Adenomyoepithelioma, not called malignant | exclude | 8983/0 | Adenomyoepithelioma, NOS (8983/0) is benign. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | — | — |
| Another tumour the report calls benign, in situ or of uncertain malignant potential | exclude | — | A behaviour the pathologist states is recorded as stated. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | — | ICD-O-3.1 manual, PDF p. 2 |

### `br_carcinoma_picker` — histology_subclassification

**Question:** Which carcinoma does the report name?

**Hint:** Type part of the name in the box and the matching options appear. The other names ICD-O-3.2 gives a tumour find it too. If a compound name is not found, search for its parts in the other order. A carcinoma of no special type mixed with lobular carcinoma is Infiltrating duct and lobular carcinoma (8522/3); mixed with another special type it is Infiltrating duct mixed with other types of carcinoma (8523/3). When one tumour carries two type names and no single option names both, choose the higher code number: a metaplastic squamous cell carcinoma is recorded as Metaplastic carcinoma, NOS (8575/3). A name that places the tumour in another organ, such as the lung, pancreas, thymus or ovary, means a deposit unless the report says the tumour began in the breast: go back and choose the deposit answer.

163 entries, searchable by every current ICD-O-3.2 synonym and related term and by the WHO wording. The entries the ICCR table names come first, in table order; the rest follow by code. Each records its code at basis 7 with the reason "Recorded as <ICD-O-3.2 Preferred term> (<code>/3)."

| Label | Records | Extra search terms | Page |
|---|---|---|---|
| Infiltrating duct carcinoma, NOS | 8500/3 | Invasive breast carcinoma of no special type; Duct adenocarcinoma, NOS; Duct carcinoma, NOS; Ductal carcinoma, NOS; Duct cell carcinoma; Infiltrating duct adenocarcinoma; Basal-like carcinoma of breast; Adenocarcinoma of mammary gland type; Adenocarcinoma of anogenital mammary-like glands; Carcinoma of male breast; Invasive ductal carcinoma; No special type; IBC-NST | ICCR Invasive Breast 2022, PDF p. 13 (table) |
| Lobular carcinoma, NOS | 8520/3 | Infiltrating lobular carcinoma, NOS; Lobular adenocarcinoma; Tubulolobular carcinoma; Lobular carcinoma, pleomorphic; Invasive lobular carcinoma | — |
| Tubular adenocarcinoma | 8211/3 | Tubular carcinoma | — |
| Cribriform carcinoma, NOS | 8201/3 | Ductal carcinoma, cribriform type; Cribriform comedo type carcinoma; Adenocarcinoma, cribriform comedo type; Invasive cribriform carcinoma | — |
| Mucinous adenocarcinoma | 8480/3 | Acinar adenocarcinoma, mucinous variant; Colloid adenocarcinoma; Colloid carcinoma; Mucinous carcinoma; Mucoid adenocarcinoma; Mucoid carcinoma; Pseudomyxoma peritonei with unknown primary site; Mucinous tubular and spindle cell carcinoma | — |
| Invasive micropapillary carcinoma of breast | 8507/3 | Micropapillary carcinoma of breast | — |
| Apocrine adenocarcinoma | 8401/3 | Apocrine carcinoma; Carcinoma with apocrine differentiation | — |
| Metaplastic carcinoma, NOS | 8575/3 | Metaplastic carcinoma, squamous cell type; Metaplastic carcinoma, spindle cell type; Mixed metaplastic carcinoma | ICCR Invasive Breast 2022, PDF p. 13 (table) |
| Oxyphilic adenocarcinoma | 8290/3 | Oncocytic adenocarcinoma; Oncocytic carcinoma; Hurthle cell carcinoma; Hurthle cell adenocarcinoma; Follicular carcinoma, oxyphilic cell; Oncocytic pattern | — |
| Lipid-rich carcinoma | 8314/3 | — | — |
| Glycogen-rich carcinoma | 8315/3 | Glycogen-rich clear cell carcinoma | — |
| Sebaceous carcinoma | 8410/3 | Sebaceous adenocarcinoma | — |
| Mucinous cystadenocarcinoma, NOS | 8470/3 | Pseudomucinous cystadenocarcinoma, NOS; Pseudomucinous adenocarcinoma; Mucinous cystic tumor with an associated invasive carcinoma; Mucinous cystic neoplasm with an associated invasive carcinoma; Papillary mucinous cystadenocarcinoma; Papillary pseudomucinous cystadenocarcinoma | — |
| Acinar cell carcinoma | 8550/3 | Acinar adenocarcinoma, NOS; Acinar carcinoma; Acinic cell adenocarcinoma; Acinic cell carcinoma | — |
| Adenoid cystic carcinoma | 8200/3 | Adenocystic carcinoma; Thymic carcinoma with adenoid cystic carcinoma-like features | — |
| Secretory carcinoma | 8502/3 | Juvenile carcinoma of breast | ICCR Invasive Breast 2022, PDF p. 14 (table) |
| Mucoepidermoid carcinoma | 8430/3 | — | — |
| Polymorphous adenocarcinoma | 8525/3 | Polymorphous carcinoma; Terminal duct adenocarcinoma | — |
| Tall cell carcinoma with reversed polarity | 8509/3 | Breast tumour resembling the tall cell variant of papillary thyroid carcinoma; Solid papillary carcinoma with reverse polarity | ICCR Invasive Breast 2022, PDF p. 14 (table); Tan 2020, PDF p. 2 |
| Solid papillary carcinoma with invasion | 8509/3 | Endocrine mucin-producing sweat gland carcinoma; Solid papillary carcinoma, invasive | — |
| Intraductal papillary adenocarcinoma with invasion | 8503/3 | Infiltrating papillary adenocarcinoma; Infiltrating and papillary adenocarcinoma; Papillary carcinoma of breast; Intraductal papillary neoplasm with associated invasive carcinoma; Intracystic papillary neoplasm with associated invasive carcinoma; Invasive papillary carcinoma | — |
| Neuroendocrine tumor, NOS | 8240/3 | Carcinoid tumor, NOS; Carcinoid, NOS; Bronchial adenoma, carcinoid; Neuroendocrine carcinoma, low grade; Neuroendocrine carcinoma, well differentiated; Neuroendocrine tumor, grade 1; Typical carcinoid; Neuroendocrine tumour | — |
| Neuroendocrine carcinoma, NOS | 8246/3 | Poorly differentiated neuroendocrine neoplasm; Neuroendocrine carcinoma | — |
| Adenomyoepithelioma with carcinoma | 8983/3 | Malignant adenomyoepithelioma | ICCR Invasive Breast 2022, PDF p. 14 (table) |
| Epithelial-myoepithelial carcinoma | 8562/3 | — | — |
| Infiltrating duct and lobular carcinoma | 8522/3 | Lobular and ductal carcinoma; Intraductal and lobular carcinoma; Infiltrating duct and lobular carcinoma in situ; Infiltrating lobular carcinoma and ductal carcinoma in situ | — |
| Infiltrating duct mixed with other types of carcinoma | 8523/3 | Infiltrating duct and colloid carcinoma; Infiltrating duct and cribriform carcinoma; Infiltrating duct and mucinous carcinoma; Infiltrating duct and tubular carcinoma | — |
| Infiltrating lobular mixed with other types of carcinoma | 8524/3 | — | — |
| Epithelioma, malignant | 8011/3 | Epithelioma, NOS | — |
| Large cell carcinoma, NOS | 8012/3 | — | — |
| Large cell neuroendocrine carcinoma | 8013/3 | Combined large cell neuroendocrine carcinoma | — |
| Large cell carcinoma with rhabdoid phenotype | 8014/3 | — | — |
| Glassy cell carcinoma | 8015/3 | — | — |
| Carcinoma, undifferentiated, NOS | 8020/3 | Carcinoma, poorly differentiated, NOS; Anaplastic undifferentiated carcinoma; Dedifferentiated carcinoma | — |
| Carcinoma, anaplastic, NOS | 8021/3 | — | — |
| Pleomorphic carcinoma | 8022/3 | — | — |
| Nuclear protein in testis (NUT)-associated carcinoma | 8023/3 | NUT carcinoma; NUT midline carcinoma | — |
| Giant cell and spindle cell carcinoma | 8030/3 | — | — |
| Giant cell carcinoma | 8031/3 | — | — |
| Spindle cell carcinoma, NOS | 8032/3 | — | — |
| Pseudosarcomatous carcinoma | 8033/3 | Sarcomatoid carcinoma | — |
| Polygonal cell carcinoma | 8034/3 | — | — |
| Carcinoma with osteoclast-like giant cells | 8035/3 | Squamous carcinoma with osteoclast-like giant cells; Undifferentiated carcinoma with osteoclast-like giant cells | — |
| Small cell carcinoma, NOS | 8041/3 | Reserve cell carcinoma; Round cell carcinoma; Small cell neuroendocrine carcinoma; Small cell carcinoma, pulmonary type | — |
| Small cell carcinoma, fusiform cell | 8043/3 | — | — |
| Small cell carcinoma, intermediate cell | 8044/3 | Small cell carcinoma, hypercalcemic type | — |
| Combined small cell carcinoma | 8045/3 | Mixed small cell carcinoma; Combined small cell-adenocarcinoma; Combined small cell-large cell carcinoma; Combined small cell-squamous cell carcinoma | — |
| Non-small cell carcinoma | 8046/3 | — | — |
| Papillary carcinoma, NOS | 8050/3 | — | — |
| Verrucous carcinoma, NOS | 8051/3 | Verrucous epidermoid carcinoma; Verrucous squamous cell carcinoma | — |
| Papillary squamous cell carcinoma | 8052/3 | Papillary epidermoid carcinoma | — |
| Warty carcinoma | 8054/3 | Condylomatous carcinoma; Warty-basaloid carcinoma | — |
| Squamous cell carcinoma, NOS | 8070/3 | Squamous cell carcinoma, usual type; Epidermoid carcinoma, NOS; Squamous carcinoma; Squamous cell epithelioma | — |
| Squamous cell carcinoma, keratinizing, NOS | 8071/3 | Epidermoid carcinoma, keratinizing; Squamous cell carcinoma, large cell, keratinizing; Keratoacanthoma | — |
| Squamous cell carcinoma, large cell, nonkeratinizing, NOS | 8072/3 | Epidermoid carcinoma, large cell, nonkeratinizing; Squamous cell carcinoma, nonkeratinizing, NOS | — |
| Squamous cell carcinoma, small cell, nonkeratinizing | 8073/3 | Epidermoid carcinoma, small cell, nonkeratinizing | — |
| Squamous cell carcinoma, spindle cell | 8074/3 | Epidermoid carcinoma, spindle cell; Squamous cell carcinoma, sarcomatoid; Pseudovascular squamous cell carcinoma | — |
| Squamous cell carcinoma, adenoid | 8075/3 | Squamous cell carcinoma, acantholytic; Squamous cell carcinoma, pseudoglandular | — |
| Squamous cell carcinoma, microinvasive | 8076/3 | — | — |
| Lymphoepithelial carcinoma | 8082/3 | Lymphoepithelioma; Lymphoepithelioma-like carcinoma; Schmincke tumor | — |
| Basaloid squamous cell carcinoma | 8083/3 | Papillary-basaloid carcinoma | — |
| Squamous cell carcinoma, clear cell type | 8084/3 | — | — |
| Squamous cell carcinoma, HPV positive | 8085/3 | — | — |
| Squamous cell carcinoma, HPV negative | 8086/3 | — | — |
| Adenoid basal carcinoma | 8098/3 | — | — |
| Transitional cell carcinoma, NOS | 8120/3 | Urothelial carcinoma, NOS; Transitional carcinoma; Squamotransitional carcinoma | — |
| Schneiderian carcinoma | 8121/3 | Cylindrical cell carcinoma | — |
| Urothelial carcinoma, sarcomatoid | 8122/3 | Urothelial carcinoma, spindle cell; Transitional cell carcinoma, spindle cell; Transitional cell carcinoma, sarcomatoid | — |
| Basaloid carcinoma | 8123/3 | — | — |
| Urothelial carcinoma, micropapillary | 8131/3 | Transitional cell carcinoma, micropapillary | — |
| Adenocarcinoma, NOS | 8140/3 | Adenocarcinoma, usual type; Carcinoma of Skene, Cowper and Littre glands; Endolymphatic sac tumor; Parathyroid carcinoma; Acinar adenocarcinoma of prostate | — |
| Linitis plastica | 8142/3 | — | — |
| Superficial spreading adenocarcinoma | 8143/3 | — | — |
| Adenocarcinoma, intestinal type | 8144/3 | Adenocarcinoma, enteric; Carcinoma, intestinal type; Mucinous carcinoma, intestinal type | — |
| Carcinoma, diffuse type | 8145/3 | Adenocarcinoma, diffuse type | — |
| Basal cell adenocarcinoma | 8147/3 | Basal cell carcinoma of prostate | — |
| Pancreatic neuroendocrine tumor, nonfunctioning | 8150/3 | Pancreatic endocrine tumor, nonfunctioning; Pancreatic endocrine tumor, NOS | — |
| Insulinoma, NOS | 8151/3 | Beta cell adenoma; Beta cell tumor | — |
| Glucagonoma | 8152/3 | Alpha cell tumor; Glucagon-like peptide-producing tumor; L-cell tumor; Pancreatic peptide and pancreatic peptide-like peptide within terminal tyrosine amide producing tumor; PP/PYY producing tumor | — |
| Gastrinoma | 8153/3 | G cell tumor; Gastrin cell tumor | — |
| Mixed neuroendocrine non-neuroendocrine neoplasm (MiNEN) | 8154/3 | Mixed pancreatic endocrine and exocrine tumor, malignant; Mixed islet cell and exocrine adenocarcinoma; Mixed acinar-endocrine carcinoma; Mixed acinar-neuroendocrine carcinoma; Mixed acinar-endocrine-ductal carcinoma; Mixed ductal-endocrine carcinoma; Mixed ductal-neuroendocrine carcinoma; Mixed endocrine and exocrine adenocarcinoma | — |
| Vipoma | 8155/3 | — | — |
| Somatostatinoma | 8156/3 | Somatostatin cell tumor | — |
| ACTH-producing tumor | 8158/3 | — | — |
| Pancreatobiliary type carcinoma | 8163/3 | Adenocarcinoma, pancreatobiliary type | — |
| Trabecular adenocarcinoma | 8190/3 | Trabecular carcinoma | — |
| Adenocarcinoma in adenomatous polyp | 8210/3 | Adenocarcinoma in polyp, NOS; Carcinoma in polyp, NOS; Adenocarcinoma in polypoid adenoma; Adenocarcinoma in tubular adenoma; Carcinoma in adenomatous polyp | — |
| Serrated adenocarcinoma | 8213/3 | — | — |
| Parietal cell carcinoma | 8214/3 | Parietal cell adenocarcinoma | — |
| Adenocarcinoma of anal glands | 8215/3 | Adenocarcinoma of anal ducts | — |
| Adenocarcinoma in adenomatous polyposis coli | 8220/3 | — | — |
| Adenocarcinoma in multiple adenomatous polyps | 8221/3 | — | — |
| Solid carcinoma, NOS | 8230/3 | Solid adenocarcinoma, NOS; Solid carcinoma with mucin formation; Solid adenocarcinoma with mucin formation | — |
| Carcinoma simplex | 8231/3 | — | — |
| Enterochromaffin cell carcinoid | 8241/3 | Carcinoid tumor, argentaffin; EC cell carcinoid; Serotonin producing carcinoid; Serotonin producing tumor | — |
| Enterochromaffin-like cell tumor | 8242/3 | ECL cell carcinoid | — |
| Goblet cell carcinoid | 8243/3 | Mucinous carcinoid; Mucocarcinoid tumor | — |
| Mixed adenoneuroendocrine carcinoma | 8244/3 | Combined carcinoid and adenocarcinoma; Mixed carcinoid and adenocarcinoma; Composite carcinoid; MANEC; Mixed carcinoid-adenocarcinoma | — |
| Merkel cell carcinoma | 8247/3 | Merkel cell tumor; Primary cutaneous neuroendocrine carcinoma | — |
| Neuroendocrine tumor, grade 2 | 8249/3 | Atypical carcinoid tumor; Neuroendocrine carcinoma, moderately differentiated; Neuroendocrine tumor, grade 3 | — |
| Lepidic adenocarcinoma | 8250/3 | — | — |
| Bronchiolo-alveolar carcinoma, non-mucinous | 8252/3 | — | — |
| Adenocarcinoma of lung, mucinous | 8253/3 | — | — |
| Adenocarcinoma of lung, mixed mucinous and non-mucinous | 8254/3 | — | — |
| Adenocarcinoma with mixed subtypes | 8255/3 | Adenocarcinoma combined with other types of carcinoma | — |
| Minimally invasive adenocarcinoma, non-mucinous | 8256/3 | — | — |
| Minimally invasive adenocarcinoma, mucinous | 8257/3 | — | — |
| Papillary adenocarcinoma, NOS | 8260/3 | Papillary carcinoma of thyroid; Papillary renal cell carcinoma | — |
| Adenocarcinoma in villous adenoma | 8261/3 | — | — |
| Villous adenocarcinoma | 8262/3 | — | — |
| Adenocarcinoma in tubulovillous adenoma | 8263/3 | Villoglandular carcinoma; Villoglandular variant of endometrioid adenocarcinoma; Papillotubular adenocarcinoma; Tubulopapillary adenocarcinoma | — |
| Micropapillary carcinoma, NOS | 8265/3 | Micropapillary adenocarcinoma | — |
| Clear cell adenocarcinoma, NOS | 8310/3 | Clear cell carcinoma, NOS; Clear cell adenocarcinoma, mesonephroid; Clear cell renal cell carcinoma, NOS | — |
| Granular cell carcinoma | 8320/3 | Granular cell adenocarcinoma | — |
| Water-clear cell adenocarcinoma | 8322/3 | Water-clear cell carcinoma | — |
| Mixed cell adenocarcinoma | 8323/3 | — | — |
| Fetal adenocarcinoma | 8333/3 | — | — |
| Endometrioid adenocarcinoma, NOS | 8380/3 | Endometrioid carcinoma, NOS; Endometrioid cystadenocarcinoma | — |
| Endometrioid adenofibroma, malignant | 8381/3 | Endometrioid cystadenofibroma, malignant | — |
| Endometrioid adenocarcinoma, secretory variant | 8382/3 | — | — |
| Endometrioid adenocarcinoma, ciliated cell variant | 8383/3 | — | — |
| Adenocarcinoma, endocervical type, NOS | 8384/3 | — | — |
| Hidradenocarcinoma | 8402/3 | Nodular hidradenoma, malignant | — |
| Syringocystadenocarcinoma papilliferum | 8406/3 | — | — |
| Serous carcinoma, NOS | 8441/3 | Serous cystadenocarcinoma, NOS; Serous adenocarcinoma, NOS; Serous papillary adenocarcinoma, NOS; Papillary serous cystadenocarcinoma; Papillary serous adenocarcinoma; Serous surface papillary carcinoma | — |
| Solid pseudopapillary neoplasm of pancreas | 8452/3 | Solid pseudopapillary carcinoma | — |
| Intraductal papillary mucinous neoplasm with an associated invasive carcinoma | 8453/3 | Intraductal papillary mucinous carcinoma, invasive | — |
| Low grade serous carcinoma | 8460/3 | Micropapillary serous carcinoma | — |
| High grade serous carcinoma | 8461/3 | — | — |
| Mucin-producing adenocarcinoma | 8481/3 | Mucin-producing carcinoma; Mucin-secreting adenocarcinoma; Mucin-secreting carcinoma | — |
| Mucinous carcinoma, gastric type | 8482/3 | — | — |
| Signet ring cell carcinoma | 8490/3 | Signet ring cell adenocarcinoma; Acinar adenocarcinoma, signet ring-like variant; Mucinous carcinoma, signet ring cell type; Poorly cohesive carcinoma; Signet ring cell/histiocytoid carcinoma | — |
| Comedocarcinoma, NOS | 8501/3 | — | — |
| Encapsulated papillary carcinoma with invasion | 8504/3 | Encysted papillary carcinoma with invasion; Intracystic papillary carcinoma with invasion | — |
| Medullary carcinoma, NOS | 8510/3 | Medullary adenocarcinoma; Medullary-like carcinoma | — |
| Atypical medullary carcinoma | 8513/3 | — | — |
| Duct carcinoma, desmoplastic type | 8514/3 | — | — |
| Infiltrating ductular carcinoma | 8521/3 | — | — |
| Inflammatory carcinoma | 8530/3 | Inflammatory adenocarcinoma | — |
| Paget disease, mammary | 8540/3 | Paget disease of breast; Paget disease of nipple | — |
| Paget disease and infiltrating duct carcinoma of breast | 8541/3 | — | — |
| Paget disease, extramammary | 8542/3 | — | — |
| Paget disease and intraductal carcinoma of breast | 8543/3 | — | — |
| Acinar adenocarcinoma of lung | 8551/3 | — | — |
| Mixed acinar-ductal carcinoma | 8552/3 | — | — |
| Adenosquamous carcinoma | 8560/3 | Mixed adenocarcinoma and epidermoid carcinoma; Mixed adenocarcinoma and squamous cell carcinoma; Squamoid eccrine ductal carcinoma | — |
| Adenocarcinoma with squamous metaplasia | 8570/3 | Adenoacanthoma; Endometrioid carcinoma with squamous differentiation | — |
| Adenocarcinoma with cartilaginous and osseous metaplasia | 8571/3 | Adenocarcinoma with cartilaginous metaplasia; Adenocarcinoma with chondroid differentiation; Adenocarcinoma with osseous metaplasia | — |
| Adenocarcinoma with spindle cell metaplasia | 8572/3 | Acinar adenocarcinoma, sarcomatoid variant; Fibromatosis-like metaplastic carcinoma | — |
| Adenocarcinoma with apocrine metaplasia | 8573/3 | Carcinoma with apocrine metaplasia | — |
| Adenocarcinoma with neuroendocrine differentiation | 8574/3 | Carcinoma with neuroendocrine differentiation; Adenocarcinoma admixed with neuroendocrine carcinoma | — |
| Hepatoid adenocarcinoma | 8576/3 | Hepatoid carcinoma | — |
| Thymoma, NOS | 8580/3 | Intrapulmonary thymoma; Sclerosing thymoma; Metaplastic thymoma | — |
| Thymoma, type A | 8581/3 | — | — |
| Thymoma, type AB | 8582/3 | Thymoma, mixed type | — |
| Thymoma, type B1 | 8583/3 | — | — |
| Thymoma, type B2 | 8584/3 | — | — |
| Thymoma, type B3 | 8585/3 | — | — |
| Thymic carcinoma, NOS | 8586/3 | Thymoma, type C | — |
| Intrathyroid thymic carcinoma | 8589/3 | Carcinoma showing thymus-like element; Carcinoma showing thymus-like differentiation; CASTLE | — |
| Carcinoma ex pleomorphic adenoma | 8941/3 | Carcinoma in pleomorphic adenoma | — |
| Brenner tumor, malignant | 9000/3 | — | — |
| Serous adenocarcinofibroma | 9014/3 | Malignant serous adenofibroma; Serous cystadenocarcinofibroma; Malignant serous cystadenofibroma | — |

## 4. Immunohistochemistry rules

None. The ICCR guide states that the histological type of a breast carcinoma rests on routine histology and that special stains such as E-cadherin are not needed to decide it (ICCR Invasive Breast 2022, PDF p. 12). The WHO 2019 classification types a carcinoma with neuroendocrine expression by its morphology and does not advise routine neuroendocrine markers (Tan 2020, PDF p. 3). Oestrogen receptor and HER2 status define treatment-relevant subtypes (Tan 2020, PDF p. 1) and do not change the morphology code. No breast screen carries an immunohistochemistry checklist.

## 5. Registration without tissue

| Evidence | Code | Basis | Offered | Note | Page |
|---|---|---|---|---|---|
| Referral letter or clinical note stating a malignant breast tumour, at least probable | 8000/3 | 1 | yes | Visser 2023, from the controller's brief (not one of this part's files). ICCC-2017 places 8000/3 at C50 in XIIb: referred to Group XII. | — |
| Imaging report (mammogram, ultrasound, magnetic resonance imaging) showing a malignant breast tumour, at least probable | 8000/3 | 2 | yes | As above: XIIb, referred to Group XII. | ICCR Invasive Breast 2022, PDF p. 9 |
| Clinical information naming melanoma of the skin of the breast | 8720/3 | 1 | yes | Visser 2023 Table 3, from the controller's brief; coded in the melanoma tree at C44.5, not here. | — |
| Cytology naming a carcinoma | 8010/3 | 5 | yes | Family-level code only: the type of a breast carcinoma is not settled on a limited sample. | ICCR Invasive Breast 2022, PDF p. 12 |
| Imaging with a raised chromogranin A, for a breast mass | 8240/3 | 4 | no | Not offered at the breast. Visser 2023 Table 4 allows 8240/3 for a neuroendocrine tumour shown on imaging with chromogranin A, but no source for this part ties a serum marker to a breast tumour, and the WHO advises excluding a deposit from another site for a well-differentiated breast neuroendocrine tumour. The evidence gate carries no marker answer. | Tan 2020, PDF p. 3 |

"Possible" or "suspected" is not registrable (br_clinical, br_imaging). The evidence gate carries no tumour-marker answer for the breast.

## 6. Laboratory tests

None. Neither breast source gives a serum or urine test a diagnostic role. The breast has no laboratory screen.

## 7. Rules A to K

| Rule | Applies | How it reaches the clerk | Page |
|---|---|---|---|
| A | yes | br_site hint and last option: the breast (C50) excludes its skin, so a tumour of the skin of the breast goes to the skin tree at C44.5. The breast is a named organ, not an ill-defined region, so Rule A does not otherwise change a breast code. | ICD-O-3.1 manual, PDF p. 1 |
| B | yes | br_site hint: a carcinoma described as periareolar or retroareolar is a breast tumour, because the tumour type shows breast tissue; the clerk chooses the part named or breast, part not stated. | ICD-O-3.1 manual, PDF p. 1 |
| C | yes | br_site option 'One tumour crossing more than one part, and the report does not say where it began' records C50.8; the hint limits it to a single tumour. | ICD-O-3.1 manual, PDF p. 5; ICCR Invasive Breast 2022, PDF p. 9 |
| D | yes | Referral only: the lymphoma option's reason says a lymphoma that begins in the breast is recorded at the breast in the Group II tree. | ICD-O-3.1 manual, PDF p. 2 |
| E | yes | Referral only: the leukaemia option's reason says a leukaemia is recorded at C42.1 and a myeloid sarcoma keeps its breast site. | ICD-O-3.1 manual, PDF p. 2 |
| F | yes | br_histology hint and the 'Benign, in situ, or of uncertain malignant potential' option; br_not_malignant offers Paget disease of the nipple called in situ (the ICD-O manual's own example) and a catch-all for any stated non-malignant behaviour; br_fibroepithelial asks for the phyllodes grade the report states. | ICD-O-3.1 manual, PDF p. 2; ICD-O-3.1 manual, PDF p. 8 |
| G | no | No breast screen offers two grades, and the sixth digit is not built. The Nottingham grade the report gives does not change the morphology code. The phyllodes benign, borderline and malignant answers are behaviours (Rule F), not grades. | ICD-O-3.1 manual, PDF p. 2; ICCR Invasive Breast 2022, PDF p. 14 |
| H | yes | br_histology deposit option, its reason and recognition aid, and the picker hint: a name that places the tumour in another organ means a deposit unless the report says it began in the breast. Mucinous cystadenocarcinoma keeps the breast although ICD-O prints the ovary beside it. For the unspecified-site part: ICD-O prints the breast beside Infiltrating duct carcinoma, NOS (Table 23), so a report naming it with no site is C50.9. | ICD-O-3.1 manual, PDF p. 10; ICD-O-3.1 manual, PDF p. 10 (table) |
| J | yes | br_carcinoma_picker hint: if a compound name is not found, search for its parts in the other order. | ICD-O-3.1 manual, PDF p. 3 |
| K | yes | br_carcinoma_picker hint: mixed no special type and lobular has its own code (8522/3), as does no special type mixed with another special type (8523/3); otherwise, when no option names both terms, the higher code number, with the example metaplastic squamous cell carcinoma, 8575/3. How Rule K meets the WHO 2019 special patterns of no special type waits on the registrar (registrar question 2). | ICD-O-3.1 manual, PDF p. 3; ICCR Invasive Breast 2022, PDF p. 12 |

There is no Rule I.

## 8. Code currency

| Code | Finding | What the tree does |
|---|---|---|
| 8504/3 | ICD-O-3.2 moved Intracystic carcinoma, NOS from 8504/3 to 8504/2; 8504/3 is now Encapsulated papillary carcinoma with invasion and 8504/2 Encapsulated papillary carcinoma (currency check section 3). REDCap labels 8504 Intracystic carcinoma, NOS, which now names an in situ term (section 4). | Picker label Encapsulated papillary carcinoma with invasion (8504/3); exclusion option for 8504/2 on br_not_malignant. The /2 synonyms are not picker search terms. REDCap relabel on the REDCap-side list. |
| 8508/3 | Every /3 term is [obs] (currency check section 2). ICD-O-3.2 lists Cystic hypersecretory carcinoma, intraductal at 8500/2. Neither source for this part names the entity. | Not built; never on a screen. Data gap 3. |
| 8512/3 | Every /3 term is [obs] (currency check section 2). The WHO 2019 volume calls carcinomas with medullary features invasive breast carcinoma of no special type with medullary pattern (Tan 2020, PDF p. 2); ICD-O-3.2 gives that 8500/3 and keeps Medullary carcinoma, NOS at 8510/3. | Not built. Registrar question 2 decides 8500/3 or 8510/3 for a medullary pattern. |
| 8509/3 | New in ICD-O-3.2; REDCap does not offer it (currency check section 6). The ICCR table prints 8509/3 for both tall cell carcinoma with reversed polarity and invasive solid papillary carcinoma; ICD-O-3.2 prints only Solid papillary carcinoma with invasion (Preferred) and Endocrine mucin-producing sweat gland carcinoma (Related) at 8509/3. | Two picker entries on the one code, each reason naming the Preferred term. REDCap-side list: add 8509. Registrar question 3. |
| 8502/3 | REDCap labels 8502 Secretory carcinoma of breast, a string ICD-O-3.2 does not print; the Preferred term is Secretory carcinoma, with Juvenile carcinoma of breast as a related term (currency check section 4). | Picker label Secretory carcinoma; Juvenile carcinoma of breast is a search term. REDCap relabel on the REDCap-side list. |
| 8507/3 | REDCap labels 8507 Intraductal micropapillary carcinoma, the /2 Preferred term; the /3 Preferred term is Invasive micropapillary carcinoma of breast (currency check section 4). | Picker label Invasive micropapillary carcinoma of breast. REDCap relabel on the REDCap-side list. |
| 8525/3 | REDCap labels 8525 Polymorphous low grade adenocarcinoma, a string ICD-O-3.2 does not print; Preferred is Polymorphous adenocarcinoma (currency check section 4). | Picker label Polymorphous adenocarcinoma. REDCap relabel. |
| 8983/3 | REDCap labels 8983 Adenomyoepithelioma, the /0 term; the /3 Preferred term is Adenomyoepithelioma with carcinoma, with Malignant adenomyoepithelioma as a synonym (currency check section 4). The ICCR table prints 8562/3 beside Malignant adenomyoepithelioma. | Picker label Adenomyoepithelioma with carcinoma (8983/3), following ICD-O-3.2. REDCap relabel. Registrar question 4 on the ICCR code. |
| 8941/3 | REDCap labels 8941 Carcinoma in pleomorphic adenoma, a synonym; Preferred is Carcinoma ex pleomorphic adenoma (currency check section 4). | Picker label Carcinoma ex pleomorphic adenoma. REDCap relabel. |
| 8410/3 | REDCap labels 8410 Sebaceous adenocarcinoma, a synonym; Preferred is Sebaceous carcinoma (currency check section 4). | Picker label Sebaceous carcinoma. REDCap relabel. |
| 8240/3 | REDCap labels 8240 Carcinoid tumor, NOS, a synonym; Preferred is Neuroendocrine tumor, NOS (currency check section 4). | Picker label Neuroendocrine tumor, NOS. REDCap relabel. |
| 8010/3 | New finding, not in the currency check: the REDCap XIf list labels 8010 Epithelial Tumor, NOS. ICD-O-3.2 gives 8010/3 the Preferred term Carcinoma, NOS; Epithelial tumor, malignant is a synonym and Epithelial tumor, benign is 8010/0. | The tree records Carcinoma, NOS (8010/3). REDCap relabel of the XIf option goes on the REDCap-side list. |
| 8551/3 | The Preferred term Acinar cell cystadenocarcinoma is [obs]; the only current /3 term is Acinar adenocarcinoma of lung (currency check section 4). | Picker label Acinar adenocarcinoma of lung; at the breast the picker hint sends an organ-named tumour to the deposit answer. |
| 8042 8124 8130 8141 8245 8251 8440 8450/3 | Every /3 term is [obs] (currency check section 2; 8042 in its note). These numbers sit in the XIf6 range at the breast; no source for this part names a breast entity on them. | Not built; never on a screen. |
| 9020/3 | Phyllodes tumor, malignant is current; Cystosarcoma phyllodes, malignant is [obs]. ICCC-2017 places 9020/3 at C50 in XIf6. | Coded on br_fibroepithelial. The [obs] synonym is not a search term. |
| 8480/3 | Gelatinous adenocarcinoma, Gelatinous carcinoma, Mucous adenocarcinoma and Mucous carcinoma are [obs] synonyms of Mucinous adenocarcinoma. | Not used as search terms. |
| 9010 9016 9030 8505 8506 8204/0 | REDCap offers these under XIf, but ICD-O-3.2 gives them no malignant form (currency check section 5). | Exclusion options on br_fibroepithelial and br_not_malignant. REDCap retire items for the registrar (section 5). |

The REDCap strings above are recorded for the REDCap-side list in `docs/TODO.md` only; the tool does not test REDCap (standing rule 16).

## 9. Conflicts with other groups

| Other group | Codes | Sites | Issue |
|---|---|---|---|
| 12 | 8000, 8001 | C50.0-C50.9 | A breast case with no tissue (8000/3) or with cytology showing malignant cells of no type (8001/3) falls in XIIb by ICCC-2017. The tree refers it to Group XII. |
| 12 | 8982, 8940, 8575 | C50.0-C50.9 | ICCC-2017 places Myoepithelial carcinoma (8982/3) and Mixed tumor, malignant, NOS (8940/3) in XIIa4 at every site, but the WHO breast table lists spindle cell or myoepithelial carcinoma as a subtype of metaplastic carcinoma, 8575/3, in XIf6. The report's words decide the group; registrar question 5. |
| 9 | 8800, 9120, 9020, 8571 | C50.0-C50.9 | Sarcomas of the breast go to Group IX. Malignant phyllodes tumour (9020/3), including periductal stromal tumour, stays in XIf6 by ICCC-2017, and a metaplastic carcinoma with chondroid or osseous differentiation (8575/3 or 8571/3) is a carcinoma, not a sarcoma. The sarcoma option carries a recognition aid against both misroutes. |
| 2 | 9715 | C50.0-C50.9 | Breast implant-associated anaplastic large cell lymphoma is a related term of 9715/3, which ICCC-2017 does not hold; the Group II tree carries 9715. Every breast lymphoma is referred to Group II and recorded at the breast. |
| 1 | 9930 | C50.0-C50.9 | Myeloid sarcoma in the breast is Ib; referred to Group I, keeping the breast site. |
| 10 | 9100 | C50.0-C50.9 | The WHO 2019 volume treats a choriocarcinomatous pattern as a pattern of invasive breast carcinoma of no special type. Applying Rule K to 'no special type with choriocarcinomatous pattern' would give Choriocarcinoma, NOS (9100/3), which ICCC-2017 places in Xb5 at the breast. Registrar question 2. |
| 11 | 8720, 8540 | C44.5 | Within Group XI: a melanocytic pattern of no special type must not be coded to melanoma by Rule K (registrar question 2); melanoma goes to the melanoma tree (XId); Paget disease (8540/3) at the skin of the breast, C44.5, is XIe by ICCC-2017, while at the nipple, C50.0, it is XIf6. |

## 10. Data gaps

1. **A source reporting breast carcinoma in patients aged 0 to 18, naming its types (secretory carcinoma above all).** Pfister 2022 Table 3 (PDF p. 13) lists only juvenile fibroadenoma and juvenile papillomatosis at the breast, and neither breast source gives ages. Without a paediatric report every breast carcinoma, secretory carcinoma included, stays in the picker. With one, secretory carcinoma (8502/3) moves to br_histology as 'Secretory carcinoma (also called juvenile carcinoma)', reason 'Recorded as Secretory carcinoma (8502/3).' Settled 8 October 2026: Sosnowska-Sienkiewicz 2024 (PMC section 72) names secretory carcinoma the commonest invasive breast cancer in children and lists invasive ductal, invasive lobular, medullary, inflammatory and anaplastic carcinomas as less common; the six are now answers on br_histology, and registrar question 1 is answered by the 8 October ruling. The review gives no ages or case counts by type, so a population series remains wanted for frequency. Candidate source: WHO Classification of Tumours, Breast Tumours, 5th edition (2019), secretory carcinoma chapter (age and ETV6::NTRK3); or WHO Classification of Paediatric Tumours, 5th edition (2022), breast chapter; or a population-based series of breast carcinoma under 20 years.
2. **Whether malignant phyllodes tumour occurs in adolescents, and how often.** It decides whether 9020/3 stays as an answer on br_fibroepithelial (now offered so the screen can separate the grades) or only in the picker. Settled 8 October 2026 for occurrence: Sosnowska-Sienkiewicz 2024 lists malignant phyllodes tumour among the primary malignant breast lesions of children and adolescents (PMC sections 2 and 76), so 9020/3 stays on br_fibroepithelial and registrar question 6 is answered by the 8 October ruling. How often it occurs under 19 is still unstated: the review gives the under-20 share of all phyllodes tumours only (PMC section 20). Candidate source: WHO Classification of Paediatric Tumours, 5th edition (2022), breast chapter; or a paediatric phyllodes tumour series.
3. **What the WHO 2019 breast volume calls cystic hypersecretory carcinoma with invasion, and its code.** Every 8508/3 term is [obs] and neither source names the entity, so a report using the term has no entry. Candidate source: WHO Classification of Tumours, Breast Tumours, 5th edition (2019), entity list with ICD-O codes.
4. **The behaviour the WHO paediatric volume gives juvenile papillomatosis.** ICD-O-3.2 prints no term for it; the tree excludes it as having no malignant code, and a WHO statement would confirm the exclusion. Sosnowska-Sienkiewicz 2024 calls it benign and associates it with carcinoma in up to 15 per cent of cases (PMC section 33); the WHO statement is still not held. Candidate source: WHO Classification of Paediatric Tumours, 5th edition (2022), breast chapter.
5. **Whether the WHO 2019 breast volume codes malignant adenomyoepithelioma 8983/3 or 8562/3.** ICD-O-3.2 lists it at 8983/3; the ICCR table prints 8562/3. It decides registrar question 4. Candidate source: WHO Classification of Tumours, Breast Tumours, 5th edition (2019), epithelial-myoepithelial tumours entity list.
6. **Whether the six carcinomas now on br_histology also stay in br_carcinoma_picker.** Secretory 8502/3, Infiltrating duct 8500/3, Lobular 8520/3, Medullary 8510/3, Inflammatory 8530/3 and Carcinoma, anaplastic 8021/3 are now answers on br_histology and remain picker entries. The picker copy keeps the microinvasion answer on br_not_malignant working, since it leads to the picker. The br_histology gateway label still names no special type, lobular and secretory as examples of a picker carcinoma. The controller decides whether to remove the picker copies, re-point the microinvasion answer and relabel the gateway. Candidate source: Controller decision; no paper needed.
7. **A paediatric report for the options that rest on no paediatric source: Carcinoma, NOS (8010/3) on br_histology.** Sosnowska-Sienkiewicz 2024 reports breast cancer in children by named subtype and never as carcinoma with no type named. 8010/3 is left as it is, an option as the fallback for a report that names no type, for the controller to decide. Candidate source: A paediatric breast carcinoma series that reports untyped cases.
8. **An answer for tubular adenoma on br_not_malignant.** Sosnowska-Sienkiewicz 2024 lists tubular adenoma among benign breast lesions of children and adolescents (PMC section 2). It is added as an exclusion entity (8211/0) but has no answer of its own on br_not_malignant; the catch-all answer covers it. A clerk who searches the picker for 'tubular' finds Tubular adenocarcinoma (8211/3), the malignant code on the same number, which would register a benign tumour. An exclusion answer 'Tubular adenoma' on br_not_malignant would close that route. Rule 3 of the brief adds an option only for a /3 code, so the controller decides. Candidate source: Controller decision; no paper needed.
9. **Whether the breast tree should state that a breast deposit is commoner than a primary breast tumour in children.** Sosnowska-Sienkiewicz 2024 states that metastatic disease in the breast is commoner than a primary breast neoplasm in children, naming renal cell carcinoma, rhabdomyosarcoma, neuroblastoma, Burkitt lymphoma, leukaemia, Ewing sarcoma and melanoma (PMC section 67), and lists infiltration by leukaemia or lymphoma (PMC section 2). The deposit, lymphoma and leukaemia answers on br_histology already route these; their position and the refer entities' paediatric fields are unchanged. The controller decides whether the deposit answer moves up or carries this cite. Candidate source: Controller decision; Sosnowska-Sienkiewicz 2024, PMC sections 2 and 67.
10. **Paediatric breast lesions the review names that have no ICD-O-3.2 breast code, and grades it does not report in children.** Sosnowska-Sienkiewicz 2024 names gynaecomastia, fibrous nodule, hamartoma, cyst, fibrocystic change and abscess in children (PMC sections 2 and 6 to 63). ICD-O-3.2 prints no breast term for any of them (its only hamartoma terms are Pulmonary hamartoma 8992/0 and Ectopic hamartomatous thymoma 8587/0), so none is added as an entity; the catch-all answer on br_not_malignant covers a report of one. The review mentions juvenile giant fibroadenoma only as a mimic of hamartoma (PMC section 45) and borderline phyllodes tumour only in the WHO grading (PMC section 22), so Giant fibroadenoma (9016/0) and Phyllodes tumor, borderline (9020/1) keep paediatric not_reported. The fibroepithelial screen's order is unchanged, because its residual answer 'Fibroadenoma of any other kind' must follow the named variants. Candidate source: WHO Classification of Paediatric Tumours, 5th edition (2022), breast chapter.

### Questions for the registrar

1. Secretory carcinoma. Pfister 2022 Table 3 (PDF p. 13) lists no breast carcinoma in children, and neither breast source gives ages, so every breast carcinoma, secretory carcinoma (8502/3) included, sits in the picker. ICD-O-3.2 lists Juvenile carcinoma of breast as a related term of 8502/3. Should secretory carcinoma wait in the picker until the controller fetches a paediatric source (data gap 1), or go on the breast histology screen now?

2. Special patterns of no special type. The WHO 2019 classification treats medullary, neuroendocrine-differentiated, pleomorphic, choriocarcinomatous, melanocytic, clear cell, oncocytic, lipid-rich, glycogen-rich and sebaceous carcinomas as patterns of invasive breast carcinoma of no special type (ICCR Invasive Breast 2022, PDF p. 12), and treats inflammatory carcinoma as a clinical presentation (Tan 2020, PDF p. 2). The ICCR table prints codes only beside oncocytic (8290/3), lipid-rich (8314/3), glycogen-rich (8315/3) and sebaceous (8410/3). Rule K would take the higher code for the others: Medullary carcinoma, NOS 8510/3, Carcinoma with neuroendocrine differentiation 8574/3, Inflammatory carcinoma 8530/3, Choriocarcinoma, NOS 9100/3 (Group X at the breast) and Malignant melanoma, NOS 8720/3 (XId). Proposed: a pattern with a printed code records that code; every other pattern records Infiltrating duct carcinoma, NOS (8500/3); a report that names medullary carcinoma or inflammatory carcinoma as the diagnosis records 8510/3 or 8530/3. Which does the registrar rule?

3. Tall cell carcinoma with reversed polarity. The WHO 2019 breast table (ICCR Invasive Breast 2022, PDF p. 14) gives it 8509/3, the code of invasive solid papillary carcinoma. ICD-O-3.2 prints no term for it at 8509/3. Confirm 8509/3, with the reason naming Solid papillary carcinoma with invasion.

4. Malignant adenomyoepithelioma. ICD-O-3.2 lists it as a synonym of Adenomyoepithelioma with carcinoma (8983/3); the ICCR table prints 8562/3 (Epithelial-myoepithelial carcinoma). The picker follows ICD-O-3.2. Confirm 8983/3.

5. Metaplastic carcinoma subtypes. The WHO table gives 8575/3 to every subtype. ICD-O-3.2 holds exact terms elsewhere: Fibromatosis-like metaplastic carcinoma 8572/3, Adenocarcinoma with chondroid differentiation 8571/3, Squamous cell carcinoma, NOS 8070/3, Spindle cell carcinoma, NOS 8032/3, Adenosquamous carcinoma 8560/3, and Myoepithelial carcinoma 8982/3, which ICCC-2017 places in Group XII. Proposed: a report that names metaplastic carcinoma with a subtype records 8575/3 (this also follows Rule K, as 8575 is the higher code); a report that names only the subtype records the ICD-O-3.2 term, and myoepithelial carcinoma named alone goes to Group XII. Which does the registrar rule?

6. Malignant phyllodes tumour. ICCC-2017 places 9020/3 at the breast in XIf6. It is offered on the fibroepithelial screen beside the benign and borderline grades and juvenile fibroadenoma, although no source here reports a malignant phyllodes tumour in a child (data gap 2). Keep it there, or move it to the picker?

## 11. Paediatric evidence added 8 October 2026

Source added: Sosnowska-Sienkiewicz 2024 (`XIf6-breast-paediatric__Sosnowska-Sienkiewicz-2024.txt`), a review of benign and malignant breast lesions in children and adolescents, read by PMC section. Applied under the registrar's ruling of 8 October 2026: an entity a source reports at ages 0 to 18 is an option on the histology screen; a current /3 code with no paediatric report is a picker entry.

| Entity | Before | After | Cite |
|---|---|---|---|
| Secretory carcinoma (8502/3) | paediatric not_reported; picker | paediatric common; option, first answer on `br_histology`: 'Secretory carcinoma (also called juvenile carcinoma)', recognition aid 'The report may call it invasive secretory carcinoma (ISC).' Picker entry kept | Sosnowska-Sienkiewicz 2024, PMC section 72 |
| Invasive breast carcinoma of no special type (8500/3) | paediatric not_reported; picker | paediatric occurs; option on `br_histology`: 'Invasive ductal carcinoma, or invasive carcinoma of no special type'. Picker entry kept | Sosnowska-Sienkiewicz 2024, PMC sections 72 and 76 (table) |
| Invasive lobular carcinoma (8520/3) | paediatric not_reported; picker | paediatric occurs; option on `br_histology`: 'Invasive lobular carcinoma'. Picker entry kept | Sosnowska-Sienkiewicz 2024, PMC section 72 |
| Medullary carcinoma (8510/3) | paediatric not_reported; picker | paediatric occurs; option on `br_histology`: 'Medullary carcinoma'. Picker entry kept; registrar question 2 still governs a report of no special type with a medullary pattern | Sosnowska-Sienkiewicz 2024, PMC section 72 |
| Inflammatory carcinoma (8530/3) | paediatric not_reported; picker | paediatric occurs; option on `br_histology`: 'Inflammatory carcinoma'. Picker entry kept | Sosnowska-Sienkiewicz 2024, PMC section 72 |
| Carcinoma, anaplastic, NOS (8021/3) | paediatric not_reported; picker | paediatric occurs; option on `br_histology`: 'Anaplastic carcinoma'. Picker entry kept | Sosnowska-Sienkiewicz 2024, PMC section 72 |
| Phyllodes tumour, malignant (9020/3) | paediatric not_reported; option on `br_fibroepithelial` | paediatric occurs; option unchanged. Answers data gap 2 for occurrence and registrar question 6 | Sosnowska-Sienkiewicz 2024, PMC sections 2 and 76 (table) |
| Fibroadenoma (9010/0) | paediatric not_reported; exclusion | paediatric common; exclusion | Sosnowska-Sienkiewicz 2024, PMC section 12 |
| Phyllodes tumour, benign (9020/0) | paediatric not_reported; exclusion | paediatric common; exclusion | Sosnowska-Sienkiewicz 2024, PMC section 77 |
| Intraductal papilloma (8503/0) | paediatric not_reported; exclusion; no cite | paediatric occurs; exclusion | Sosnowska-Sienkiewicz 2024, PMC section 25 |
| Juvenile papillomatosis (no code) | paediatric occurs; exclusion | paediatric occurs; exclusion; cite added: benign, with carcinoma in up to 15 per cent of cases | Sosnowska-Sienkiewicz 2024, PMC section 33 |
| Tubular adenoma of the breast (8211/0) | not listed | new entity: paediatric occurs; exclusion. ICD-O-3.2 Tubular adenoma, NOS (Preferred) verified; no /3 form of this tumour, so no option (data gap 8) | Sosnowska-Sienkiewicz 2024, PMC section 2 |

Screen changed: `br_histology` gains six answers at the top, in this order: secretory carcinoma (common in children), then invasive ductal or no special type, invasive lobular, medullary, inflammatory and anaplastic carcinoma (reported in children, in the review's own order). Each records its code at basis 7 with a reason naming the ICD-O-3.2 Preferred term. The answers that were already there keep their order. ICCC-2017 places all six codes in XIf6 at C50.0 to C50.9; none has an [obs] /3 Preferred term.

Data gaps: 1 and 2 are marked settled for occurrence, 4 records what the review says of juvenile papillomatosis, and 6 to 10 are new. Registrar questions 1 and 6 are answered by the 8 October ruling and the new source; their text is left in place for the controller to remove.

Not changed, for the controller (data gaps 6 to 10): the six carcinomas' picker entries and the picker gateway's label; Carcinoma, NOS (8010/3), an option with no paediatric report; an exclusion answer for tubular adenoma, whose malignant code 8211/3 is a picker entry; the deposit answer, which the review supports for children; and the lesions with no ICD-O-3.2 breast code. Giant fibroadenoma (9016/0) and Phyllodes tumor, borderline (9020/1) keep paediatric not_reported: the review does not report either in children.
