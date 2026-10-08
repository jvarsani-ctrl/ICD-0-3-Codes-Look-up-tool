# Group 11 evidence — XIc nasopharyngeal carcinoma, plus oropharynx (XIf10)

Part `XIc_nasopharynx`. Evidence for the Group 11 build, 8 October 2026. The JSON beside this file holds the same content with every quotation; each quotation was checked against its page by `check_g11_evidence.py` (279 of 279 found). This file writes no tool JSON.

Sites: nasopharynx C11.0, C11.1, C11.2, C11.3, C11.8, C11.9 (ICCC-2017 XIc); tonsil C09.0, C09.1, C09.8, C09.9 and oropharynx C10.0 to C10.4, C10.8, C10.9 (XIf10). The ICCR dataset also counts the base of tongue (C01.9, lingual tonsil C02.4), soft palate (C05.1) and uvula (C05.2) as oropharynx; ICCC-2017 places those sites in XIf10 too, so the subgroup does not change if the router sends them here.

## 1. Sources

| File | Citation | WHO volume |
|---|---|---|
| `XIc-nasopharynx__Badoual-2022.txt` | Badoual C. Update from the 5th Edition of the World Health Organization Classification of Head and Neck Tumors: Oropharynx and Nasopharynx. Head Neck Pathol 2022;16(1):19-30. doi:10.1007/s12105-022-01449-2 | WHO Classification of Head and Neck Tumours, 5th edition, 2022 (beta), published 2024 |
| `XIc-nasopharynx__ICCR-Oropharynx-Nasopharynx-2nd.txt` | International Collaboration on Cancer Reporting. Carcinomas of the Oropharynx and Nasopharynx Histopathology Reporting Guide, 2nd edition, version 2.0, July 2024. ISBN 978-1-922324-47-4 | WHO Classification of Head and Neck Tumours, 5th edition, 2024 |
| `ALL-paediatric-occurrence__Pfister-2022.txt` | Pfister SM, Reyes-Mugica M, Chan JKC, et al. A Summary of the Inaugural WHO Classification of Pediatric Tumors: Transitioning from the Optical into the Molecular Era. Cancer Discov 2022;12(2):331-355 | WHO Classification of Paediatric Tumours, 5th edition, 2022 |
| `RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt` | World Health Organization. International Classification of Diseases for Oncology, 3rd edition, 1st revision (ICD-O-3.1), section 4, Coding guidelines, printed pp. 14-28 | Coding manual, not a tumour classification |

Tables were read from the PDF page images and match the text: ICCR Table 1 (oropharynx, PDF p. 10), ICCR Table 2 (nasopharynx, PDF p. 11), the ICCR histological tumour type data item (PDF p. 2) and Pfister Table 3 (PDF p. 14).

The WHO nasopharynx table (ICCR Table 2, PDF p. 11) lists four carcinomas: non-keratinising squamous cell carcinoma 8072/3, keratinising squamous cell carcinoma 8071/3, basaloid squamous cell carcinoma 8083/3 and low grade nasopharyngeal papillary adenocarcinoma 8260/3. It prints no separate code for the undifferentiated subtype of non-keratinising carcinoma, and neither file prints that subtype's name for the nasopharynx (section 10). The WHO oropharynx table (ICCR Table 1, PDF p. 10) lists squamous cell carcinoma, HPV-associated 8085/3 and HPV-independent 8086/3, and drops further histologic typing (ICCR PDF p. 10). Pfister Table 3 lists nasopharyngeal carcinoma, NUT carcinoma, mucoepidermoid carcinoma, acinic cell carcinoma and sialoblastoma among paediatric malignant head and neck tumours (PDF p. 14); no source reports oropharyngeal squamous cell carcinoma in children.

## 2. Entities

Named entities (options, referrals, exclusions, oropharynx entries, not built):

| Entity | Code | ICD-O-3.2 term matched (level) | Paediatric | Decision | Pages |
|---|---|---|---|---|---|
| Non-keratinising squamous cell carcinoma (nasopharyngeal carcinoma) | 8072/3 | Squamous cell carcinoma, nonkeratinizing, NOS (Synonym) | occurs | option | ICCR Oropharynx and Nasopharynx 2024, PDF p. 11; Badoual 2022, PDF p. 8; Pfister 2022, PDF p. 14 |
| Keratinising squamous cell carcinoma (nasopharyngeal carcinoma) | 8071/3 | Squamous cell carcinoma, keratinizing, NOS (Preferred) | occurs | option | ICCR Oropharynx and Nasopharynx 2024, PDF p. 11; Badoual 2022, PDF p. 8; Pfister 2022, PDF p. 14 |
| Basaloid squamous cell carcinoma (nasopharyngeal carcinoma) | 8083/3 | Basaloid squamous cell carcinoma (Preferred) | occurs | option | ICCR Oropharynx and Nasopharynx 2024, PDF p. 11; Badoual 2022, PDF p. 8; Pfister 2022, PDF p. 14 |
| Nasopharyngeal carcinoma reported as squamous cell carcinoma with no subtype | 8070/3 | Squamous cell carcinoma, NOS (Preferred) | occurs | option | Badoual 2022, PDF p. 6; Badoual 2022, PDF p. 8; Pfister 2022, PDF p. 14 |
| Nasopharyngeal carcinoma with no type stated | 8010/3 | Carcinoma, NOS (Preferred) | occurs | option | Badoual 2022, PDF p. 6; Badoual 2022, PDF p. 8; Pfister 2022, PDF p. 14 |
| Poorly differentiated or undifferentiated carcinoma, type not named | 8020/3 | Carcinoma, poorly differentiated, NOS (Related) | occurs | option | ICCR Oropharynx and Nasopharynx 2024, PDF p. 11; Badoual 2022, PDF p. 8 |
| NUT carcinoma | 8023/3 | NUT carcinoma (Synonym) | occurs | option | Pfister 2022, PDF p. 14 |
| Mucoepidermoid carcinoma (salivary gland-type, minor salivary gland) | 8430/3 | Mucoepidermoid carcinoma (Preferred) | occurs | option | Pfister 2022, PDF p. 14; ICCR Oropharynx and Nasopharynx 2024, PDF p. 10 |
| Acinic cell carcinoma (salivary gland-type, minor salivary gland) | 8550/3 | Acinic cell adenocarcinoma (Synonym) | occurs | option | Pfister 2022, PDF p. 14; ICCR Oropharynx and Nasopharynx 2024, PDF p. 10 |
| Mucosal melanoma | 8720/3 | Melanoma, NOS (Synonym) | not_reported | option | ICCR Oropharynx and Nasopharynx 2024, PDF p. 4; Badoual 2022, PDF p. 5; Pfister 2022, PDF p. 14 |
| Diffuse large B-cell lymphoma | 9680/3 | Diffuse large B-cell lymphoma, NOS (Preferred) | occurs | refer to Group 2 | Badoual 2022, PDF p. 5 |
| NK/T-cell lymphoma | 9719/3 | Extranodal NK/T-cell lymphoma, nasal type (Synonym) | not_reported | refer to Group 2 | Badoual 2022, PDF p. 5 |
| Rhabdomyosarcoma | 8900/3 | Rhabdomyosarcoma, NOS (Preferred) | occurs | refer to Group 9 | ICCR Oropharynx and Nasopharynx 2024, PDF p. 4; Pfister 2022, PDF p. 8 |
| Chordoma | 9370/3 | Chordoma, NOS (Preferred) | not_reported | refer to Group 8 | Badoual 2022, PDF p. 5 |
| Craniopharyngioma (adamantinomatous craniopharyngioma) | 9350/1 | Craniopharyngioma, NOS (Preferred) | not_reported | refer to Group 3 | Badoual 2022, PDF p. 5 |
| Ectopic or invasive pituitary neuroendocrine tumour (pituitary adenoma) | 8272/0 | Pituitary adenoma, ectopic (Related) | not_reported | refer to Group 3 | Badoual 2022, PDF p. 5 |
| Carcinoma in situ | 8070/2 | Squamous cell carcinoma in situ, NOS (Preferred) | not_reported | exclusion | ICCR Oropharynx and Nasopharynx 2024, PDF p. 2; Badoual 2022, PDF p. 9 |
| High grade dysplasia (moderate or severe dysplasia) | 8077/2 | Squamous dysplasia, high grade (Synonym) | not_reported | exclusion | ICCR Oropharynx and Nasopharynx 2024, PDF p. 2; Badoual 2022, PDF p. 9 |
| Angiofibroma of the sinonasal tract (nasopharyngeal angiofibroma) | 9160/0 | Juvenile angiofibroma (Synonym) | not_reported | exclusion | Badoual 2022, PDF p. 5 |
| Nasopharyngeal dermoid | 9084/0 | Dermoid, NOS (Synonym) | occurs | exclusion | Pfister 2022, PDF p. 14 |
| Pleomorphic adenoma | 8940/0 | Pleomorphic adenoma (Preferred) | occurs | exclusion | Pfister 2022, PDF p. 14 |
| Squamous cell carcinoma, HPV-associated (oropharynx) | 8085/3 | Squamous cell carcinoma, HPV positive (Preferred) | not_reported | picker | ICCR Oropharynx and Nasopharynx 2024, PDF p. 10; Badoual 2022, PDF p. 2; Pfister 2022, PDF p. 14 |
| Squamous cell carcinoma, HPV-independent (oropharynx) | 8086/3 | Squamous cell carcinoma, HPV negative (Preferred) | not_reported | picker | ICCR Oropharynx and Nasopharynx 2024, PDF p. 10; Badoual 2022, PDF p. 5; Pfister 2022, PDF p. 14 |
| Squamous cell carcinoma with no HPV or p16 result (oropharynx) | 8070/3 | Squamous cell carcinoma, NOS (Preferred) | not_reported | picker | ICCR Oropharynx and Nasopharynx 2024, PDF p. 10; Pfister 2022, PDF p. 14 |
| Papillary urothelial carcinoma | 8130/3 | Papillary urothelial carcinoma (Preferred) | not_reported | not_built | ICCR Oropharynx and Nasopharynx 2024, PDF p. 11 |
| Scirrhous adenocarcinoma | 8141/3 | Scirrhous adenocarcinoma (Preferred) | not_reported | not_built | ICCR Oropharynx and Nasopharynx 2024, PDF p. 11 |
| Adenocarcinoid tumor | 8245/3 | Adenocarcinoid tumor (Preferred) | not_reported | not_built | ICCR Oropharynx and Nasopharynx 2024, PDF p. 11 |
| Cystadenocarcinoma, NOS | 8440/3 | Cystadenocarcinoma, NOS (Preferred) | not_reported | not_built | ICCR Oropharynx and Nasopharynx 2024, PDF p. 11 |
| Cystic hypersecretory carcinoma | 8508/3 | Cystic hypersecretory carcinoma (Preferred) | not_reported | not_built | ICCR Oropharynx and Nasopharynx 2024, PDF p. 11 |
| Medullary carcinoma with lymphoid stroma | 8512/3 | Medullary carcinoma with lymphoid stroma (Preferred) | not_reported | not_built | ICCR Oropharynx and Nasopharynx 2024, PDF p. 11 |
| Large cell neuroendocrine carcinoma | 8013/3 | Large cell neuroendocrine carcinoma (Preferred) | not_reported | picker | ICCR Oropharynx and Nasopharynx 2024, PDF p. 11; Pfister 2022, PDF p. 14 |
| Small cell neuroendocrine carcinoma | 8041/3 | Small cell carcinoma, NOS (Preferred) | not_reported | picker | ICCR Oropharynx and Nasopharynx 2024, PDF p. 11; Pfister 2022, PDF p. 14 |
| Lymphoepithelial carcinoma | 8082/3 | Lymphoepithelial carcinoma (Preferred) | not_reported | picker | Badoual 2022, PDF p. 8; Pfister 2022, PDF p. 14 |
| Adenoid cystic carcinoma | 8200/3 | Adenoid cystic carcinoma (Preferred) | not_reported | picker | ICCR Oropharynx and Nasopharynx 2024, PDF p. 10; Pfister 2022, PDF p. 14 |
| Neuroendocrine carcinoma | 8246/3 | Neuroendocrine carcinoma, NOS (Preferred) | not_reported | picker | ICCR Oropharynx and Nasopharynx 2024, PDF p. 4; Badoual 2022, PDF p. 3; ICCR Oropharynx and Nasopharynx 2024, PDF p. 15; Pfister 2022, PDF p. 14 |
| Low-grade nasopharyngeal papillary adenocarcinoma | 8260/3 | Papillary adenocarcinoma, NOS (Preferred) | not_reported | picker | ICCR Oropharynx and Nasopharynx 2024, PDF p. 11; Badoual 2022, PDF p. 6; Pfister 2022, PDF p. 14 |
| Neuroendocrine tumour, grade 1 or no grade | 8240/3 | Neuroendocrine tumor, NOS (Preferred) | not_reported | picker | ICCR Oropharynx and Nasopharynx 2024, PDF p. 4; ICCR Oropharynx and Nasopharynx 2024, PDF p. 11; Pfister 2022, PDF p. 14 |
| Neuroendocrine tumour, grade 2 or grade 3 | 8249/3 | Neuroendocrine tumor, grade 2 (Preferred) | not_reported | picker | ICCR Oropharynx and Nasopharynx 2024, PDF p. 4; ICCR Oropharynx and Nasopharynx 2024, PDF p. 11; Pfister 2022, PDF p. 14 |

Why, per entity:

- **8072/3 Non-keratinising squamous cell carcinoma (nasopharyngeal carcinoma).** The WHO nasopharynx table codes non-keratinising nasopharyngeal carcinoma 8072/3. It is the commonest subtype; the sources report nasopharyngeal carcinoma in children without naming the subtype.
- **8071/3 Keratinising squamous cell carcinoma (nasopharyngeal carcinoma).** A WHO subtype of nasopharyngeal carcinoma, an entity the sources report in children. Offered on the subtype screen.
- **8083/3 Basaloid squamous cell carcinoma (nasopharyngeal carcinoma).** A WHO subtype of nasopharyngeal carcinoma. Offered on the subtype screen.
- **8070/3 Nasopharyngeal carcinoma reported as squamous cell carcinoma with no subtype.** Nasopharyngeal carcinoma usually shows squamous differentiation; a report that names squamous cell carcinoma and no subtype records the squamous NOS code.
- **8010/3 Nasopharyngeal carcinoma with no type stated.** The WHO definition says the carcinoma is usually, not always, squamous, so a report that names no type records Carcinoma, NOS. The registrar rules whether 8010/3 or 8070/3 is the default.
- **8020/3 Poorly differentiated or undifferentiated carcinoma, type not named.** Fallback of the stain panel when no rule fires. Epstein-Barr virus-positive nasopharyngeal carcinoma looks poorly differentiated, so this wording reaches the panel first.
- **8023/3 NUT carcinoma.** The paediatric WHO summary lists NUT carcinoma among malignant head and neck tumours of children. At C11 ICCC-2017 places 8023/3 in XIc. The NUT carcinoma part decides its recognition text and confirming tests; this part only offers it on the nasopharynx histology screen.
- **8430/3 Mucoepidermoid carcinoma (salivary gland-type, minor salivary gland).** The paediatric WHO summary lists mucoepidermoid carcinoma among malignant head and neck tumours of children, without naming a site. The ICCR dataset covers minor salivary carcinomas of the nasopharynx and oropharynx. ICCC-2017 places 8430/3 in XIc at C11 and XIf10 at C09-C10.
- **8550/3 Acinic cell carcinoma (salivary gland-type, minor salivary gland).** The paediatric WHO summary lists acinic cell carcinoma among malignant head and neck tumours of children, without naming a site. ICD-O-3.2 prints Acinar cell carcinoma as the preferred term.
- **8720/3 Mucosal melanoma.** Melanoma is offered on the histology screen only as a route to the Group XI melanoma tree, which any site reaches and which decides the code. No source reports mucosal melanoma of the pharynx in children; Pfister lists melanoma among paediatric skin tumours.
- **9680/3 Diffuse large B-cell lymphoma.** Lymphoma of the nasopharynx, adenoid or tonsil is Group II (ICCC-2017 IIb2 at every site).
- **9719/3 NK/T-cell lymphoma.** Group II (ICCC-2017 IIb3 at every site).
- **8900/3 Rhabdomyosarcoma.** Sarcomas fall outside the ICCR carcinoma dataset; ICCC-2017 places rhabdomyosarcoma (8900-8920) in IXa at every site.
- **9370/3 Chordoma.** Chordoma arises in the clivus and reaches the nasopharynx from the skull base. ICCC-2017 places 9370/3 in VIIId2 at every site; the case is coded at its bone site.
- **9350/1 Craniopharyngioma (adamantinomatous craniopharyngioma).** The WHO head and neck volume treats it with the skull base. ICCC-2017 places 9350-9352 in IIIe2 at every site, behaviours 0, 1 and 3.
- **8272/0 Ectopic or invasive pituitary neuroendocrine tumour (pituitary adenoma).** ICCC-2017 places 8270-8281 in IIIe1 at every site, behaviours 0, 1 and 3, so an ectopic pituitary adenoma of the nasopharynx is Group III.
- **8070/2 Carcinoma in situ.** In situ carcinoma is behaviour 2; Group XI registers behaviour 3. The ICCR applies the in situ category only to HPV-independent oropharyngeal and EBV-independent nasopharyngeal tumours.
- **8077/2 High grade dysplasia (moderate or severe dysplasia).** Behaviour 2; not registrable in Group XI.
- **9160/0 Angiofibroma of the sinonasal tract (nasopharyngeal angiofibroma).** Benign. ICCC-2017 holds no range for 9160 at behaviour 0.
- **9084/0 Nasopharyngeal dermoid.** Benign; the paediatric WHO summary lists it among benign head and neck tumours.
- **8940/0 Pleomorphic adenoma.** Benign; the paediatric WHO summary lists it among benign head and neck tumours.
- **8085/3 Squamous cell carcinoma, HPV-associated (oropharynx).** The WHO oropharynx table codes it 8085/3; p16 positivity is an accepted surrogate. No source of this part reports oropharyngeal squamous cell carcinoma in children, so it is a long-tail entry until the registrar rules otherwise. New in ICD-O-3.2; REDCap does not offer it.
- **8086/3 Squamous cell carcinoma, HPV-independent (oropharynx).** The WHO oropharynx table codes it 8086/3; p16 negativity is an accepted surrogate. No paediatric report in this part's sources. New in ICD-O-3.2; REDCap does not offer it.
- **8070/3 Squamous cell carcinoma with no HPV or p16 result (oropharynx).** A report that gives no HPV or p16 result records the squamous NOS code. No paediatric report in this part's sources.
- **8130/3 Papillary urothelial carcinoma.** ICD-O-3.2 marks both /3 terms [obs]. 8130/2 Papillary urothelial carcinoma, non-invasive and 8120/3 Urothelial carcinoma, NOS are current. The WHO nasopharynx table names no entity on 8130.
- **8141/3 Scirrhous adenocarcinoma.** Every /3 term [obs]; ICD-O-3.2 prints no cross-reference. The WHO nasopharynx table names no entity on 8141.
- **8245/3 Adenocarcinoid tumor.** Every /3 term [obs]. 8243/3 Goblet cell carcinoid is current but is an appendiceal entity. The WHO nasopharynx table names no entity on 8245.
- **8440/3 Cystadenocarcinoma, NOS.** Every /3 term [obs]; no cross-reference. The WHO nasopharynx table names no entity on 8440.
- **8508/3 Cystic hypersecretory carcinoma.** Every /3 term [obs]. 8500/2 Cystic hypersecretory carcinoma, intraductal is current (breast). The WHO nasopharynx table names no entity on 8508.
- **8512/3 Medullary carcinoma with lymphoid stroma.** Every /3 term [obs]. 8510/3 Medullary carcinoma, NOS is current. The WHO nasopharynx table names no entity on 8512.
- **8013/3 Large cell neuroendocrine carcinoma.** Large cell is one of the two neuroendocrine carcinoma categories. No source reports it in children.
- **8041/3 Small cell neuroendocrine carcinoma.** Small cell is one of the two neuroendocrine carcinoma categories. No source reports it in children.
- **8082/3 Lymphoepithelial carcinoma.** ICD-O-3.2 files Lymphoepithelioma and Schmincke tumor here. The WHO nasopharynx table prints no 8082/3 entity: lymphoepithelial features are a variation of non-keratinising carcinoma. Kept in the long tail; the registrar rules which code a nasopharyngeal report of lymphoepithelioma takes.
- **8200/3 Adenoid cystic carcinoma.** A salivary gland-type carcinoma; the ICCR dataset covers minor salivary carcinomas here. No paediatric report in this part's sources.
- **8246/3 Neuroendocrine carcinoma.** The ICCR dataset covers neuroendocrine carcinoma of the nasopharynx. No source reports it in children.
- **8260/3 Low-grade nasopharyngeal papillary adenocarcinoma.** The WHO nasopharynx table codes it 8260/3. No source reports it in children.
- **8240/3 Neuroendocrine tumour, grade 1 or no grade.** The ICCR dataset covers neuroendocrine tumours of the nasopharynx. No source reports them in children. ICCC-2017 holds no range for this code at C11 (XIc stops at 8244-8246; XIf10 excludes C11); by the 1 October 2026 ruling a valid code outside every range belongs to the group it is offered in, so the subgroup is XIc.
- **8249/3 Neuroendocrine tumour, grade 2 or grade 3.** The ICCR dataset covers neuroendocrine tumours of the nasopharynx. No source reports them in children. ICCC-2017 holds no range for this code at C11 (XIc stops at 8244-8246; XIf10 excludes C11); by the 1 October 2026 ruling a valid code outside every range belongs to the group it is offered in, so the subgroup is XIc.

Long-tail picker at C11, generated (no source of this part names these or reports them in children; ICCC-2017 places each in XIc at C11; paediatric evidence checked against Pfister Table 3, PDF p. 14): 70 codes.

8011/3 Epithelioma, malignant, 8012/3 Large cell carcinoma, NOS, 8014/3 Large cell carcinoma with rhabdoid phenotype, 8015/3 Glassy cell carcinoma, 8021/3 Carcinoma, anaplastic, NOS, 8022/3 Pleomorphic carcinoma, 8030/3 Giant cell and spindle cell carcinoma, 8031/3 Giant cell carcinoma, 8032/3 Spindle cell carcinoma, NOS, 8033/3 Pseudosarcomatous carcinoma, 8034/3 Polygonal cell carcinoma, 8035/3 Carcinoma with osteoclast-like giant cells, 8050/3 Papillary carcinoma, NOS, 8051/3 Verrucous carcinoma, NOS, 8052/3 Papillary squamous cell carcinoma, 8054/3 Warty carcinoma, 8073/3 Squamous cell carcinoma, small cell, nonkeratinizing, 8074/3 Squamous cell carcinoma, spindle cell, 8075/3 Squamous cell carcinoma, adenoid, 8120/3 Transitional cell carcinoma, NOS, 8121/3 Schneiderian carcinoma, 8122/3 Urothelial carcinoma, sarcomatoid, 8131/3 Urothelial carcinoma, micropapillary, 8140/3 Adenocarcinoma, NOS, 8190/3 Trabecular adenocarcinoma, 8201/3 Cribriform carcinoma, NOS, 8211/3 Tubular adenocarcinoma, 8230/3 Solid carcinoma, NOS, 8231/3 Carcinoma simplex, 8244/3 Mixed adenoneuroendocrine carcinoma, 8261/3 Adenocarcinoma in villous adenoma, 8262/3 Villous adenocarcinoma, 8263/3 Adenocarcinoma in tubulovillous adenoma, 8290/3 Oxyphilic adenocarcinoma, 8310/3 Clear cell adenocarcinoma, NOS, 8320/3 Granular cell carcinoma, 8323/3 Mixed cell adenocarcinoma, 8480/3 Mucinous adenocarcinoma, 8481/3 Mucin-producing adenocarcinoma, 8500/3 Infiltrating duct carcinoma, NOS, 8501/3 Comedocarcinoma, NOS, 8502/3 Secretory carcinoma, 8503/3 Intraductal papillary adenocarcinoma with invasion, 8504/3 Encapsulated papillary carcinoma with invasion, 8507/3 Invasive micropapillary carcinoma of breast, 8509/3 Solid papillary carcinoma with invasion, 8510/3 Medullary carcinoma, NOS, 8513/3 Atypical medullary carcinoma, 8514/3 Duct carcinoma, desmoplastic type, 8520/3 Lobular carcinoma, NOS, 8521/3 Infiltrating ductular carcinoma, 8522/3 Infiltrating duct and lobular carcinoma, 8523/3 Infiltrating duct mixed with other types of carcinoma, 8524/3 Infiltrating lobular mixed with other types of carcinoma, 8525/3 Polymorphous adenocarcinoma, 8530/3 Inflammatory carcinoma, 8540/3 Paget disease, mammary, 8541/3 Paget disease and infiltrating duct carcinoma of breast, 8542/3 Paget disease, extramammary, 8543/3 Paget disease and intraductal carcinoma of breast, 8551/3 Acinar adenocarcinoma of lung, 8560/3 Adenosquamous carcinoma, 8562/3 Epithelial-myoepithelial carcinoma, 8570/3 Adenocarcinoma with squamous metaplasia, 8571/3 Adenocarcinoma with cartilaginous and osseous metaplasia, 8572/3 Adenocarcinoma with spindle cell metaplasia, 8573/3 Adenocarcinoma with apocrine metaplasia, 8574/3 Adenocarcinoma with neuroendocrine differentiation, 8575/3 Metaplastic carcinoma, NOS, 8576/3 Hepatoid adenocarcinoma.

## 3. The pathway

The nasopharynx tree (node prefix `np_`). Oropharynx entries (prefix `op_`) follow. Basis of diagnosis: clinical 1, imaging 2, cytology 5, histology 7.

### `np_document_inventory` — document_inventory

**What is in the file for this tumour?**

Hint: A radiology report counts as imaging. A pathology report on a biopsy or resection counts as histology. An Epstein-Barr virus blood test does not establish the tumour: a file with imaging and an Epstein-Barr virus blood test belongs with imaging.

| Option | Outcome | Records | Page |
|---|---|---|---|
| A referral letter or clinical note only, with no imaging report and no tissue | go | next: `np_clinical` |  |
| An imaging report, with or without an Epstein-Barr virus blood test, and no tissue | go | next: `np_imaging` | ICCR Oropharynx and Nasopharynx 2024, PDF p. 15 |
| A cytology report, such as a fine-needle aspirate, and no histology report | go | next: `np_cytology` |  |
| A histology report, with or without stains or Epstein-Barr virus encoded RNA (EBER) in situ hybridisation | go | next: `np_histology` | ICCR Oropharynx and Nasopharynx 2024, PDF p. 10 |

### `np_clinical` — clinical_alias

**What does the referral letter or clinical note say?**

| Option | Outcome | Records | Page |
|---|---|---|---|
| The note states nasopharyngeal cancer as the diagnosis. *Reason:* Recorded as Neoplasm, malignant (8000/3) at basis of diagnosis 1. A diagnosis on clinical information alone takes the unspecified code; a histology report gives the specific code. | code | 8000/3, basis 1 |  |
| The note says possible or suspected cancer only. *Reason:* A possible or suspected cancer is not registrable on this evidence. | not_registrable | not registrable |  |
| An imaging report is in the file after all | go | next: `np_imaging` |  |

### `np_imaging` — morphology_only

**No tissue is in the file. What does the imaging report conclude?**

| Option | Outcome | Records | Page |
|---|---|---|---|
| Imaging shows a malignant tumour of the nasopharynx. *Reason:* Recorded as Neoplasm, malignant (8000/3) at basis of diagnosis 2. Imaging and an Epstein-Barr virus blood test give no tumour type; a histology report gives the specific code. | code | 8000/3, basis 2 | ICCR Oropharynx and Nasopharynx 2024, PDF p. 15 |
| Imaging calls it possible only, or describes a benign lesion. *Reason:* A possible cancer is not registrable on this evidence. | not_registrable | not registrable |  |
| A histology report is in the file | go | next: `np_histology` |  |

### `np_cytology` — morphology_only

**What does the cytology report conclude?**

| Option | Outcome | Records | Page |
|---|---|---|---|
| Cytology names squamous cell carcinoma. *Reason:* Recorded as Squamous cell carcinoma, NOS (8070/3) at basis of diagnosis 5. Cytology does not give the nasopharyngeal carcinoma subtype; a histology report confirms it. | code | 8070/3, basis 5 |  |
| Cytology names a poorly differentiated or undifferentiated carcinoma. *Reason:* Recorded as Carcinoma, undifferentiated, NOS (8020/3) at basis of diagnosis 5. | code | 8020/3, basis 5 |  |
| Cytology names a carcinoma with no type. *Reason:* Recorded as Carcinoma, NOS (8010/3) at basis of diagnosis 5. | code | 8010/3, basis 5 |  |
| Malignant cells are present, with no tumour type named. *Reason:* Recorded as Tumor cells, malignant (8001/3) at basis of diagnosis 5. Cytology establishes malignant cells but no tumour type. | code | 8001/3, basis 5 |  |
| Cytology names a lymphoma. *Reason:* Lymphoma is coded in Group II, Lymphomas and reticuloendothelial neoplasms. | refer | Group 2 | Badoual 2022, PDF p. 5 |
| No malignant cells, scant material, or a non-diagnostic report, and an imaging report is in the file | go | next: `np_imaging` |  |
| No malignant cells, scant material, or a non-diagnostic report, and no imaging report is in the file | go | next: `np_clinical` |  |

### `np_histology` — histology_subclassification

**What does the histology report call the tumour?**

Hint: Use the report's own term. At the nasopharynx the code follows the histologic type: an Epstein-Barr virus (EBER) or p16 result does not change it. (ICCR Oropharynx and Nasopharynx 2024, PDF p. 10; ICCR Oropharynx and Nasopharynx 2024, PDF p. 15)

| Option | Outcome | Records | Page |
|---|---|---|---|
| Nasopharyngeal carcinoma, or squamous cell carcinoma of the nasopharynx *Recognition aid:* Reports describe a carcinoma of the nasopharyngeal lining, usually with squamous features, often in sheets among many lymphocytes and plasma cells. | go | next: `np_npc_type` | Badoual 2022, PDF p. 6; Badoual 2022, PDF p. 8; Pfister 2022, PDF p. 14 |
| Carcinoma, poorly differentiated or undifferentiated, and the report names no type *Recognition aid:* Epstein-Barr virus-positive nasopharyngeal carcinoma often reads as poorly differentiated because of its non-keratinising, lymphoepithelial look. | go | next: `np_ihc` | ICCR Oropharynx and Nasopharynx 2024, PDF p. 11 |
| NUT carcinoma. *Reason:* Recorded as Nuclear protein in testis (NUT)-associated carcinoma (8023/3). | code | 8023/3, basis 7 | Pfister 2022, PDF p. 14 |
| A salivary gland-type carcinoma, such as mucoepidermoid carcinoma or acinic cell carcinoma | go | next: `np_salivary` | ICCR Oropharynx and Nasopharynx 2024, PDF p. 10 |
| Melanoma. *Reason:* Melanoma at any site is coded on the melanoma screens of Group XI. | go | next: `melanoma_tree_entry` | ICCR Oropharynx and Nasopharynx 2024, PDF p. 4; Badoual 2022, PDF p. 5 |
| Lymphoma, of any type. *Reason:* Lymphoma is coded in Group II, Lymphomas and reticuloendothelial neoplasms. | refer | Group 2 | Badoual 2022, PDF p. 5 |
| Rhabdomyosarcoma, or another soft-tissue sarcoma. *Reason:* A sarcoma of the nasopharynx is coded in Group IX, Soft-tissue and other extraosseous sarcomas. | refer | Group 9 | ICCR Oropharynx and Nasopharynx 2024, PDF p. 4 |
| Chordoma. *Reason:* Chordoma begins in the bone of the skull base. It is coded in Group VIII, Malignant bone tumours, at its bone site. | refer | Group 8 (site recaptured) | Badoual 2022, PDF p. 5 |
| Craniopharyngioma, or a pituitary neuroendocrine tumour or pituitary adenoma. *Reason:* Coded in Group III, Central nervous system and miscellaneous intracranial and intraspinal neoplasms. | refer | Group 3 | Badoual 2022, PDF p. 5 |
| A tumour that began at another site and spread to the nasopharynx | go | next: `np_deposit` | ICCR Oropharynx and Nasopharynx 2024, PDF p. 15; ICD-O-3.1 manual, PDF p. 2 |
| A benign lesion, carcinoma in situ or dysplasia, with no invasive tumour | go | next: `np_not_malignant` | Badoual 2022, PDF p. 6 |
| Another carcinoma the report names | go | next: `np_carcinoma_other` |  |

### `np_npc_type` — histology_subclassification

**Which type of nasopharyngeal carcinoma does the report name?**

Hint: When the report names two of these types, pick the higher code: basaloid (8083/3) before non-keratinising (8072/3) before keratinising (8071/3). (ICD-O-3.1 manual, PDF p. 3)

| Option | Outcome | Records | Page |
|---|---|---|---|
| Non-keratinising squamous cell carcinoma (non-keratinising nasopharyngeal carcinoma), differentiated or undifferentiated subtype. *Reason:* Recorded as Squamous cell carcinoma, large cell, nonkeratinizing, NOS (8072/3). The WHO classification codes non-keratinising nasopharyngeal carcinoma to this number. *Recognition aid:* Reports often call it poorly differentiated or undifferentiated and describe sheets of tumour cells among many lymphocytes and plasma cells; Epstein-Barr virus (EBER) is usually positive. | code | 8072/3, basis 7 | ICCR Oropharynx and Nasopharynx 2024, PDF p. 11; Badoual 2022, PDF p. 8 |
| Keratinising squamous cell carcinoma (keratinising nasopharyngeal carcinoma). *Reason:* Recorded as Squamous cell carcinoma, keratinizing, NOS (8071/3). *Recognition aid:* Reports describe a keratinising squamous cell carcinoma like those elsewhere in the head and neck. | code | 8071/3, basis 7 | ICCR Oropharynx and Nasopharynx 2024, PDF p. 11; Badoual 2022, PDF p. 8 |
| Basaloid squamous cell carcinoma. *Reason:* Recorded as Basaloid squamous cell carcinoma (8083/3). | code | 8083/3, basis 7 | ICCR Oropharynx and Nasopharynx 2024, PDF p. 11; Badoual 2022, PDF p. 8 |
| Squamous cell carcinoma, and the report names no type. *Reason:* Recorded as Squamous cell carcinoma, NOS (8070/3). | code | 8070/3, basis 7 | Badoual 2022, PDF p. 6 |
| Nasopharyngeal carcinoma, and the report names no type and does not call it squamous. *Reason:* Recorded as Carcinoma, NOS (8010/3). The report does not state the squamous type. | code | 8010/3, basis 7 | Badoual 2022, PDF p. 6 |

### `np_ihc` — ihc_checklist

**Answer each stain as the report states it.**

Hint: Answer the Epstein-Barr virus question from Epstein-Barr virus encoded RNA (EBER) in situ hybridisation. A latent membrane protein 1 (LMP1) stain misses about half of these tumours. Answer 'Not done or not readable' for a stain the report does not mention. (Badoual 2022, PDF p. 8)

Markers: pan-cytokeratin; p40 or p63; Epstein-Barr virus encoded RNA (EBER) in situ hybridisation; chromogranin, synaptophysin or insulinoma-associated protein 1 (INSM1). Fallback: 8020/3.

| Option | Outcome | Records | Page |
|---|---|---|---|
| Rule 1: pan-cytokeratin positive, p40 or p63 positive, EBER positive. *Reason:* Recorded as Squamous cell carcinoma, large cell, nonkeratinizing, NOS (8072/3). | code | 8072/3, basis 7 | Badoual 2022, PDF p. 8; ICCR Oropharynx and Nasopharynx 2024, PDF p. 15; ICCR Oropharynx and Nasopharynx 2024, PDF p. 11 |
| Rule 2: pan-cytokeratin positive, p40 or p63 positive, EBER negative. *Reason:* Recorded as Squamous cell carcinoma, NOS (8070/3). The stains show squamous carcinoma but not its type. | code | 8070/3, basis 7 | Badoual 2022, PDF p. 8; ICCR Oropharynx and Nasopharynx 2024, PDF p. 15 |
| Rule 3: chromogranin, synaptophysin or INSM1 positive, pan-cytokeratin positive, p40 negative. *Reason:* Recorded as Neuroendocrine carcinoma, NOS (8246/3). | code | 8246/3, basis 7 | Badoual 2022, PDF p. 3; ICCR Oropharynx and Nasopharynx 2024, PDF p. 15 |
| No rule fires. *Reason:* Recorded as Carcinoma, undifferentiated, NOS (8020/3). The stains do not decide the type. | code | 8020/3, basis 7 |  |

### `np_salivary` — histology_subclassification

**Which salivary gland-type carcinoma does the report name?**

Hint: These carcinomas arise in the minor salivary glands of the nasopharynx and carry the same names as in the major salivary glands. (ICCR Oropharynx and Nasopharynx 2024, PDF p. 10)

| Option | Outcome | Records | Page |
|---|---|---|---|
| Mucoepidermoid carcinoma. *Reason:* Recorded as Mucoepidermoid carcinoma (8430/3). | code | 8430/3, basis 7 | Pfister 2022, PDF p. 14 |
| Acinic cell carcinoma. *Reason:* Recorded as Acinar cell carcinoma (8550/3). ICD-O-3.2 gives Acinic cell adenocarcinoma as a synonym. | code | 8550/3, basis 7 | Pfister 2022, PDF p. 14 |
| Another salivary gland-type carcinoma | go | next: `np_carcinoma_other` |  |

### `np_not_malignant` — histology_subclassification

**Which lesion does the report describe?**

| Option | Outcome | Records | Page |
|---|---|---|---|
| Carcinoma in situ, with no invasive carcinoma. *Reason:* Squamous cell carcinoma in situ, NOS (8070/2) is not malignant in the registry's sense. Group XI registers invasive tumours only. | exclude | 8070/2 | ICCR Oropharynx and Nasopharynx 2024, PDF p. 2; ICD-O-3.1 manual, PDF p. 2 |
| High grade, moderate or severe dysplasia, with no invasive carcinoma. *Reason:* Squamous intraepithelial neoplasia, high grade (8077/2) is not registrable in Group XI. | exclude | 8077/2 | ICCR Oropharynx and Nasopharynx 2024, PDF p. 2; Badoual 2022, PDF p. 9 |
| Angiofibroma (juvenile or nasopharyngeal angiofibroma). *Reason:* Angiofibroma, NOS (9160/0) is benign and not registrable. | exclude | 9160/0 | Badoual 2022, PDF p. 5 |
| Dermoid (nasopharyngeal dermoid). *Reason:* Dermoid cyst, NOS (9084/0) is benign and not registrable. | exclude | 9084/0 | Pfister 2022, PDF p. 14 |
| Pleomorphic adenoma. *Reason:* Pleomorphic adenoma (8940/0) is benign and not registrable. | exclude | 8940/0 | Pfister 2022, PDF p. 14 |
| Hairy polyp, or salivary gland anlage tumour. *Reason:* The report describes a benign lesion. ICD-O-3.2 gives it no code, and it is not registrable. *Recognition aid:* A hairy polyp is a benign polyp of the lateral nasopharyngeal wall; a salivary gland anlage tumour is a hamartoma of infancy. | not_registrable | not registrable | Badoual 2022, PDF p. 6 |

### `np_deposit` — morphology_only

**Where does the report say the primary tumour is?**

Hint: The tumour in the nasopharynx is a deposit, not a separate registration: the case is coded at its primary site. An oropharyngeal carcinoma can extend into the nasopharynx. (ICCR Oropharynx and Nasopharynx 2024, PDF p. 15; ICD-O-3.1 manual, PDF p. 2)

| Option | Outcome | Records | Page |
|---|---|---|---|
| A carcinoma or melanoma of another organ, such as the oropharynx or the thyroid. *Reason:* Carcinomas and melanomas of other organs are coded at their primary site. Record the primary's site and code again. | go | next: `site_capture` (site recaptured) | ICCR Oropharynx and Nasopharynx 2024, PDF p. 15 |
| A soft-tissue sarcoma, including rhabdomyosarcoma. *Reason:* Soft-tissue sarcomas are ICCC-3 Group IX. Code the case at its primary. | refer | Group 9 (site recaptured) |  |
| A bone sarcoma. *Reason:* Malignant bone tumours are ICCC-3 Group VIII. Code the case at its primary. | refer | Group 8 (site recaptured) |  |
| A tumour of the brain or spinal cord. *Reason:* Central nervous system tumours are ICCC-3 Group III. Code the case at its primary. | refer | Group 3 (site recaptured) |  |
| Neuroblastoma. *Reason:* Neuroblastoma is ICCC-3 Group IV. Code the case at its primary. | refer | Group 4 (site recaptured) |  |
| Nephroblastoma (Wilms tumour), or another kidney tumour. *Reason:* Renal tumours are ICCC-3 Group VI. Code the case at its primary. | refer | Group 6 (site recaptured) |  |
| A germ cell tumour. *Reason:* Germ cell tumours are ICCC-3 Group X. Code the case at its primary. | refer | Group 10 (site recaptured) |  |
| The primary is not known and has not been found. *Reason:* A carcinoma deposit with no identified primary is coded at unknown primary site (C80.9). | go | next: `site_capture_unknown_primary` (site recaptured) |  |

### `np_carcinoma_other` — histology_subclassification

**Which carcinoma does the report name?**

Hint: Type part of the name in the box and the matching options appear. Use the report's own term. A term that names another organ, such as breast, lung or thyroid, describes a deposit: go back and pick the deposit option. When the report gives two grades of a neuroendocrine tumour, pick the higher. (ICD-O-3.1 manual, PDF p. 2; ICCR Oropharynx and Nasopharynx 2024, PDF p. 11)

Author note: Long-tail picker: every XIc code ICD-O-3.2 prints at /3 that the other nasopharynx nodes do not offer, less the six all-[obs] codes, plus 8240/3 and 8249/3, which ICCC-2017 leaves without a range at C11. Search terms are the other current /3 terms at each code, less those that name another organ (Rule H: such a term at the nasopharynx implies a deposit). Several ICCC XIc codes carry organ-named preferred terms (8507, 8540-8543 breast; 8551 lung); they stay, under the hint.

78 entries, each recorded as its ICD-O-3.2 term at basis 7 and searchable by the code's other current terms. Entries with their own evidence:

- Large cell neuroendocrine carcinoma — 8013/3. Recorded as Large cell neuroendocrine carcinoma (8013/3). (ICCR Oropharynx and Nasopharynx 2024, PDF p. 11)
- Small cell neuroendocrine carcinoma — 8041/3. Recorded as Small cell carcinoma, NOS (8041/3). (ICCR Oropharynx and Nasopharynx 2024, PDF p. 11)
- Lymphoepithelial carcinoma — 8082/3. Recorded as Lymphoepithelial carcinoma (8082/3). (Badoual 2022, PDF p. 8)
- Adenoid cystic carcinoma — 8200/3. Recorded as Adenoid cystic carcinoma (8200/3). (ICCR Oropharynx and Nasopharynx 2024, PDF p. 10)
- Neuroendocrine carcinoma — 8246/3. Recorded as Neuroendocrine carcinoma, NOS (8246/3). (ICCR Oropharynx and Nasopharynx 2024, PDF p. 4; Badoual 2022, PDF p. 3; ICCR Oropharynx and Nasopharynx 2024, PDF p. 15)
- Low-grade nasopharyngeal papillary adenocarcinoma — 8260/3. Recorded as Papillary adenocarcinoma, NOS (8260/3). Recognition aid: Reports describe a papillary tumour of bland glandular cells, positive for thyroid transcription factor 1 (TTF1) and negative for thyroglobulin and PAX8. (ICCR Oropharynx and Nasopharynx 2024, PDF p. 11; Badoual 2022, PDF p. 6)
- Neuroendocrine tumor, NOS — 8240/3. Recorded as Neuroendocrine tumor, NOS (8240/3). (ICCR Oropharynx and Nasopharynx 2024, PDF p. 4; ICCR Oropharynx and Nasopharynx 2024, PDF p. 11)
- Neuroendocrine tumor, grade 2 — 8249/3. Recorded as Neuroendocrine tumor, grade 2 (8249/3). (ICCR Oropharynx and Nasopharynx 2024, PDF p. 4; ICCR Oropharynx and Nasopharynx 2024, PDF p. 11)

### `op_carcinoma_other` — histology_subclassification

**Which carcinoma does the report name?**

Hint: Type part of the name in the box. A squamous cell carcinoma with a human papillomavirus (HPV) or p16 result takes the HPV entry: p16 positive counts as HPV-associated, p16 negative as HPV-independent. A squamous subtype named with an HPV status also takes the HPV entry, the higher code. (ICCR Oropharynx and Nasopharynx 2024, PDF p. 10; ICD-O-3.1 manual, PDF p. 3)

Author note: Oropharynx (C09-C10) long tail. These three entries head the XIf10 picker the general carcinoma tree builds for other specified sites; the rest of that list is every XIf10 code ICD-O-3.2 prints at /3.

| Option | Outcome | Records | Page |
|---|---|---|---|
| Squamous cell carcinoma, HPV-associated, or p16 positive. *Reason:* Recorded as Squamous cell carcinoma, HPV positive (8085/3). *Recognition aid:* Reports count a tumour as HPV-associated when p16 stains at least 70% of tumour cells, nuclear and cytoplasmic. | code | 8085/3, basis 7 | ICCR Oropharynx and Nasopharynx 2024, PDF p. 10; Badoual 2022, PDF p. 4 |
| Squamous cell carcinoma, HPV-independent, or p16 negative. *Reason:* Recorded as Squamous cell carcinoma, HPV negative (8086/3). | code | 8086/3, basis 7 | ICCR Oropharynx and Nasopharynx 2024, PDF p. 10; Badoual 2022, PDF p. 5 |
| Squamous cell carcinoma, with no HPV or p16 result in the report. *Reason:* Recorded as Squamous cell carcinoma, NOS (8070/3). | code | 8070/3, basis 7 | ICCR Oropharynx and Nasopharynx 2024, PDF p. 10 |

### `op_squamous_hpv` — histology_subclassification

*Status: proposed: built only if the registrar rules oropharyngeal squamous cell carcinoma a paediatric option; until then the three codes sit in op_carcinoma_other.*

**What does the report say about human papillomavirus (HPV) in the squamous cell carcinoma?**

Hint: A p16 result alone counts: p16 positive is HPV-associated, p16 negative is HPV-independent. A squamous subtype named with an HPV status takes the HPV code, the higher code. (ICCR Oropharynx and Nasopharynx 2024, PDF p. 10; ICD-O-3.1 manual, PDF p. 3)

| Option | Outcome | Records | Page |
|---|---|---|---|
| Squamous cell carcinoma, HPV-associated, or p16 positive. *Reason:* Recorded as Squamous cell carcinoma, HPV positive (8085/3). *Recognition aid:* Reports count a tumour as HPV-associated when p16 stains at least 70% of tumour cells, nuclear and cytoplasmic. | code | 8085/3, basis 7 | ICCR Oropharynx and Nasopharynx 2024, PDF p. 10; Badoual 2022, PDF p. 4 |
| Squamous cell carcinoma, HPV-independent, or p16 negative. *Reason:* Recorded as Squamous cell carcinoma, HPV negative (8086/3). | code | 8086/3, basis 7 | ICCR Oropharynx and Nasopharynx 2024, PDF p. 10; Badoual 2022, PDF p. 5 |
| Squamous cell carcinoma, with no HPV or p16 result in the report. *Reason:* Recorded as Squamous cell carcinoma, NOS (8070/3). | code | 8070/3, basis 7 | ICCR Oropharynx and Nasopharynx 2024, PDF p. 10 |

## 4. Immunohistochemistry rules

The `np_ihc` panel is reached when the histology report calls the tumour a poorly differentiated or undifferentiated carcinoma and names no type. An immunohistochemistry result does not stand in for a histology report: the panel only types a carcinoma the histology report has already diagnosed.

| Panel | Positive | Negative | Code | Page |
|---|---|---|---|---|
| `np_ihc` | pan-cytokeratin; p40 or p63; Epstein-Barr virus encoded RNA (EBER) in situ hybridisation | — | 8072/3 | Badoual 2022, PDF p. 8; ICCR Oropharynx and Nasopharynx 2024, PDF p. 15; ICCR Oropharynx and Nasopharynx 2024, PDF p. 11 |
| `np_ihc` | pan-cytokeratin; p40 or p63 | Epstein-Barr virus encoded RNA (EBER) in situ hybridisation | 8070/3 | Badoual 2022, PDF p. 8; ICCR Oropharynx and Nasopharynx 2024, PDF p. 15 |
| `np_ihc` | chromogranin, synaptophysin or insulinoma-associated protein 1 (INSM1); pan-cytokeratin | p40 | 8246/3 | Badoual 2022, PDF p. 3; ICCR Oropharynx and Nasopharynx 2024, PDF p. 15 |
| `np_ihc` | — | — | 8020/3 (fallback) | ICCR Oropharynx and Nasopharynx 2024, PDF p. 11 |
| `op_squamous_hpv` | p16 (at least 70% of tumour cells, nuclear and cytoplasmic) | — | 8085/3 | ICCR Oropharynx and Nasopharynx 2024, PDF p. 10; Badoual 2022, PDF p. 4 |
| `op_squamous_hpv` | — | p16 | 8086/3 | ICCR Oropharynx and Nasopharynx 2024, PDF p. 10 |

Rule 1 rests on three statements: pan-cytokeratin shows epithelial origin and p40 or p63 squamous differentiation (Badoual 2022, PDF p. 8); EBER in situ hybridisation is positive in most non-keratinising carcinomas and variable in keratinising and basaloid carcinoma (Badoual 2022, PDF p. 8; ICCR, PDF p. 15); and Epstein-Barr virus-positive nasopharyngeal carcinoma reads as poorly differentiated because of its non-keratinising morphology (ICCR, PDF p. 11). Rule 2 does not type an EBER-negative squamous carcinoma, because HPV-related nasopharyngeal carcinomas are EBER-negative yet non-keratinising (ICCR, PDF p. 15). Latent membrane protein 1 staining is not an Epstein-Barr virus answer: it misses half the tumours (Badoual 2022, PDF p. 8).

Low-grade nasopharyngeal papillary adenocarcinoma is positive for thyroid transcription factor 1 and negative for thyroglobulin and PAX8 (Badoual 2022, PDF p. 6). This is carried as the recognition aid on its picker entry, not as a panel: the entity has no paediatric report.

The panel cannot exclude NUT carcinoma or lymphoma; this part's sources give no NUT or CD45 rule (section 10).

## 5. Registration without tissue

- Referral letter or clinical note stating nasopharyngeal cancer, no imaging and no tissue: 8000/3, basis 1.
- Imaging report showing a malignant nasopharyngeal tumour, with or without an Epstein-Barr virus serology or plasma Epstein-Barr virus DNA result: 8000/3, basis 2. (ICCR Oropharynx and Nasopharynx 2024, PDF p. 15)

No basis 4 code. Per the controller's summary, Visser 2023 Table 4 holds no nasopharyngeal carcinoma entry, and this part's sources give Epstein-Barr virus serology only a post-treatment surveillance role (ICCR, PDF p. 15). A file with imaging and an Epstein-Barr virus blood test therefore registers 8000/3 at basis 2. Possible or suspected cancer is not registrable.

## 6. Laboratory tests

| Test | Specimen | Role | Page |
|---|---|---|---|
| Epstein-Barr virus serology | serum | Post-treatment surveillance in Epstein-Barr virus-positive tumours. It does not establish the tumour and does not change the code. | ICCR Oropharynx and Nasopharynx 2024, PDF p. 15 |
| Plasma Epstein-Barr virus DNA | plasma | Named only in a cited study on pretreatment staging. No diagnostic or coding role in this part's sources. | ICCR Oropharynx and Nasopharynx 2024, PDF p. 17 |
| Epstein-Barr virus encoded RNA (EBER) in situ hybridisation | other | Tissue test. Positive in most non-keratinising nasopharyngeal carcinomas, variable in keratinising and basaloid; decides rule 1 against rule 2 of the np_ihc panel. | Badoual 2022, PDF p. 8; ICCR Oropharynx and Nasopharynx 2024, PDF p. 10 |
| p16 immunohistochemistry | other | Tissue test. At the oropharynx it decides HPV-associated (8085/3) against HPV-independent (8086/3); at the nasopharynx it does not change the code. | ICCR Oropharynx and Nasopharynx 2024, PDF p. 10; Badoual 2022, PDF p. 4 |
| High-risk HPV-specific testing (polymerase chain reaction for HPV DNA, reverse transcription polymerase chain reaction for E6/E7 mRNA, DNA or RNA in situ hybridisation) | other | Tissue test. Confirms HPV when p16 is equivocal or disagrees with the morphology. No separate code. | ICCR Oropharynx and Nasopharynx 2024, PDF p. 15 |

No serum or urine test has a diagnostic role in this part's sources, so the nasopharynx tree needs no laboratory screen.

## 7. Rules A to K

| Rule | Applies | How it reaches the clerk | Page |
|---|---|---|---|
| A | no | The nasopharynx and oropharynx are specific sites, so no screen in this part applies Rule A. A report that names only the neck is settled at the router's site capture; a neck deposit goes through np_deposit. | ICD-O-3.1 manual, PDF p. 1 |
| B | no | No screen here. A site written as para-, peri- or retropharyngeal is settled at the router's site capture. | ICD-O-3.1 manual, PDF p. 1 |
| C | yes | At the router's site capture for this part, as a hint: a tumour over two or more nasopharyngeal walls with no stated origin is C11.8; one over the nasopharynx and the oropharynx with no stated origin is C14.8, which ICCC-2017 places in XIf10, not XIc. Multifocal nasopharyngeal tumour is one primary. | ICD-O-3.1 manual, PDF p. 5; ICCR Oropharynx and Nasopharynx 2024, PDF p. 5 |
| D | yes | Only through referral: the lymphoma options on np_histology and np_cytology refer to Group II, which codes lymphoma of the tonsil, adenoid or Waldeyer ring as nodal. | ICD-O-3.1 manual, PDF p. 5; Badoual 2022, PDF p. 5 |
| E | no | No leukaemia presents at this site in this part's sources. | ICD-O-3.1 manual, PDF p. 2 |
| F | yes | Option labels and reasons on np_not_malignant: carcinoma in situ (8070/2) and high grade dysplasia (8077/2) are excluded as behaviour 2. Low-grade nasopharyngeal papillary adenocarcinoma is a malignant glandular neoplasm and takes /3 despite 'low-grade' (reason on its picker entry). | ICD-O-3.1 manual, PDF p. 2; Badoual 2022, PDF p. 6; ICCR Oropharynx and Nasopharynx 2024, PDF p. 2 |
| G | yes | Hint on np_carcinoma_other, the only screen that offers two grades of one tumour (neuroendocrine tumour 8240/3 grade 1 and 8249/3 grade 2 or 3): pick the higher. The sixth digit is not built. 'Poorly differentiated' or 'undifferentiated' in a nasopharyngeal carcinoma report describes the non-keratinising look, shown as a recognition aid on 8072/3, not as a grade. | ICD-O-3.1 manual, PDF p. 2; ICD-O-3.1 manual, PDF p. 9; ICCR Oropharynx and Nasopharynx 2024, PDF p. 11 |
| H | yes | Option 'A tumour that began at another site and spread to the nasopharynx' on np_histology leads to np_deposit, whose hint and reasons code the case at its primary and recapture the site. The recognition aid on 8260/3 (TTF1 positive, thyroglobulin and PAX8 negative) marks a nasopharyngeal primary rather than a thyroid deposit. | ICD-O-3.1 manual, PDF p. 2; ICCR Oropharynx and Nasopharynx 2024, PDF p. 15; Badoual 2022, PDF p. 6 |
| J | no | No compound term in this part needs its word roots reordered. | ICD-O-3.1 manual, PDF p. 3 |
| K | yes | Hint on np_npc_type: two types named, pick the higher code (8083 before 8072 before 8071). Hint on op_carcinoma_other and op_squamous_hpv: a squamous subtype named with an HPV status takes 8085/3 or 8086/3, higher than every squamous subtype code 8051-8084. Adenosquamous carcinoma (8560/3) with an HPV status is a registrar question. | ICD-O-3.1 manual, PDF p. 3; Badoual 2022, PDF p. 3 |

There is no Rule I.

## 8. Code currency

| Code | Finding | Action |
|---|---|---|
| 8072/3 | Current. ICD-O-3.2 preferred term Squamous cell carcinoma, large cell, nonkeratinizing, NOS; the WHO 5th edition term is Non-keratinising squamous cell carcinoma (ICCR Table 2, PDF p. 11). REDCap's XIc label equals the preferred term. | Option on np_npc_type; label in report vocabulary, reason names the preferred term. |
| 8071/3 | Current; REDCap label equals the preferred term. | Option on np_npc_type. |
| 8083/3 | Current; REDCap label equals the preferred term. | Option on np_npc_type. |
| 8260/3 | Current. The WHO 5th edition renamed nasopharyngeal papillary adenocarcinoma 'low-grade nasopharyngeal papillary adenocarcinoma' (Badoual 2022, PDF p. 6); ICD-O-3.2 has no site-specific term, preferred Papillary adenocarcinoma, NOS. | Picker entry labelled with the WHO name and searchable by the ICD-O-3.2 term. |
| 8082/3 | Current. ICD-O-3.2 files Lymphoepithelioma, Lymphoepithelioma-like carcinoma and Schmincke tumor here; the WHO nasopharynx table names no 8082/3 entity. | Picker entry; registrar question on which code a nasopharyngeal report of lymphoepithelioma takes. |
| 8085/3 | New in ICD-O-3.2 (Code Currency Check section 6); REDCap does not offer it. ICD-O-3.2 term Squamous cell carcinoma, HPV positive; WHO term Squamous cell carcinoma, HPV-associated. ICCC-2017 places it in XIf10 at C09-C10 and in no range at C11. | Oropharynx only. Goes on the REDCap-side list in docs/TODO.md section 7. Not offered at C11: the WHO codes nasopharyngeal carcinoma by histologic type. |
| 8086/3 | New in ICD-O-3.2; REDCap does not offer it. ICD-O-3.2 term Squamous cell carcinoma, HPV negative; WHO term HPV-independent. No ICCC range at C11. | As 8085/3. |
| 8023/3 | New in ICD-O-3.2; REDCap's XIc list does not offer it. | Offered on np_histology; REDCap-side list. The NUT carcinoma part owns its detail. |
| 8130/3 | Every /3 term [obs]. | not_built; listed in the build report. |
| 8141/3 | Every /3 term [obs]. | not_built. |
| 8245/3 | Every /3 term [obs]. | not_built. |
| 8440/3 | Every /3 term [obs]. | not_built. |
| 8508/3 | Every /3 term [obs]. | not_built. |
| 8512/3 | Every /3 term [obs]. | not_built. |
| 8551/3 | The preferred term Acinar cell cystadenocarcinoma is [obs]; the related term Acinar adenocarcinoma of lung is current. REDCap's label is the [obs] term. | Picker entry labelled Acinar adenocarcinoma of lung; REDCap relabel goes on the REDCap-side list. |
| 8033/3 | REDCap label Sarcomatoid carcinoma is a synonym; preferred Pseudosarcomatous carcinoma. | Picker entry under the preferred term, searchable by the synonym; REDCap-side list. |
| 8122/3 | REDCap label Transitional cell carcinoma, spindle cell; preferred Urothelial carcinoma, sarcomatoid. | Picker entry; REDCap-side list. |
| 8502/3 | REDCap label Secretory carcinoma of breast is not an ICD-O-3.2 term; preferred Secretory carcinoma. | Picker entry; REDCap-side list. |
| 8504/3 | REDCap label Intracystic carcinoma, NOS now names an in situ term (8504/2); 8504/3 is Encapsulated papillary carcinoma with invasion. | Picker entry under the /3 term; REDCap-side list. |
| 8507/3 | REDCap label Intraductal micropapillary carcinoma is listed at /2; 8507/3 is Invasive micropapillary carcinoma of breast. | Picker entry; REDCap-side list. |
| 8525/3 | REDCap label Polymorphous low grade adenocarcinoma is not an ICD-O-3.2 term; preferred Polymorphous adenocarcinoma. | Picker entry; REDCap-side list. |
| 8240/3 | Current, but ICCC-2017 holds no range for it at C11. | Picker entry; the subgroup computation needs XIc for it at C11 under the 1 October 2026 ruling. |
| 8249/3 | Current, but ICCC-2017 holds no range for it at C11. | As 8240/3. |

## 9. Conflicts with other groups

| Group | Codes | Sites | Issue |
|---|---|---|---|
| 2 | 9680, 9719, 9687, 9650 | C11.1, C11.9, C09.9, C14.2 | Lymphoma of the nasopharynx, adenoid, tonsil or Waldeyer ring is Group II (ICCC-2017 IIa, IIb2, IIb3, IIc at every site). Nasopharyngeal lymphomas are 15% of head and neck lymphomas; diffuse large B-cell and NK/T-cell lymphoma are named. |
| 9 | 8900, 8910, 8920, 9364 | C11.0, C11.1, C11.2, C11.3, C11.8, C11.9 and others | Rhabdomyosarcoma (IXa) and extraosseous Ewing sarcoma (IXd2) of the pharynx are Group IX at every site. The ICCR carcinoma dataset excludes sarcomas. |
| 8 | 9370 | C41.0, C11.9 | Chordoma of the clivus reaches the nasopharynx; ICCC-2017 places 9370/3 in VIIId2 at every site. Referred with the site recaptured. |
| 3 | 9350, 9351, 8272 | C11.9 | Craniopharyngioma (IIIe2) and ectopic pituitary adenoma or pituitary neuroendocrine tumour (IIIe1) are Group III at every site, behaviours 0, 1 and 3, so a benign ectopic pituitary adenoma of the nasopharynx is registrable in Group III. |
| 12 | 8982, 8940, 8974 | C11.0, C11.1, C11.2, C11.3, C11.8, C11.9 and others | Myoepithelial carcinoma (8982/3), malignant mixed tumour (8940/3) and sialoblastoma (8974) are XIIa4 at every site. A salivary gland-type myoepithelial carcinoma of the nasopharynx or oropharynx is Group XII by ICCC-2017; the salivary part decides how the salivary screens route it. |
| 10 | 9084 | C11.9 | Nasopharyngeal dermoid (9084/0) is benign and not registrable; a teratoma with malignant transformation (9084/3) at C11 is Xb2. Hairy polyp, which Badoual calls a form of teratoma, is benign and has no ICD-O-3.2 term. |
| 11 | 8085, 8086, 8240, 8249, 8941, 8147 | C11.0, C11.1, C11.2, C11.3, C11.8, C11.9 | Within Group XI: these valid /3 codes have no ICCC-2017 range at C11 (XIc's ranges stop short of them; XIf10 excludes C11). 8085/8086 are not offered at C11; 8240/8249 are picker entries; 8941 and 8147 are salivary types the salivary part names. The subgroup computation must return XIc for them at C11. |
| 11 | 8070, 8072, 8020 | C14.8, C80.9 | Within Group XI: a tumour over the nasopharynx and oropharynx with no stated origin is C14.8 (XIf10), and a neck deposit with no primary is C80.9 (XIf11). The nasopharyngeal codes then fall in XIf10 or XIf11, not XIc. |

Each referral was verified in ICCC-2017 for the code at C11 and C09-C10: 9680/3 IIb2, 9719/3 IIb3, 9687/3 IIc, 9650/3 IIa, 8900-8920/3 IXa, 9364/3 IXd2, 9370/3 VIIId2, 9350/1 IIIe2, 8272/0 IIIe1, 8982/3 XIIa4, 8720/3 XId.

## 10. Data gaps

- **The WHO 5th edition nasopharyngeal carcinoma chapter's own text on the differentiated and undifferentiated subtypes of non-keratinising carcinoma, and its mapping of the older terms (WHO types 1 to 3, lymphoepithelioma, Schmincke tumour, undifferentiated carcinoma of nasopharyngeal type).** Neither file prints 'undifferentiated subtype' for the nasopharynx; ICCR names only the differentiated subtype (PDF p. 15). The 8072/3 option label and the 8072/3-or-8082/3 registrar question rest on it. Candidate source: WHO Classification of Head and Neck Tumours, 5th ed. (2024), Chapter 4, Nasopharyngeal carcinoma; or Stelow EB, Wenig BM, Head Neck Pathol 2017;11:16-22 (4th edition nasopharynx update) as corroboration.
- **Paediatric occurrence of the nasopharyngeal carcinoma subtypes and of Epstein-Barr virus status in patients aged 0-18.** Both sources report nasopharyngeal carcinoma in children without naming the subtype, so keratinising and basaloid carcinoma are options only as subdivisions of a paediatric entity. Candidate source: WHO Classification of Paediatric Tumours, 5th ed., nasopharyngeal carcinoma chapter; Children's Oncology Group ARAR0331 report (Rodriguez-Galindo C, et al. J Clin Oncol 2019).
- **Paediatric occurrence of oropharyngeal squamous cell carcinoma, HPV-associated or HPV-independent, aged 0-18.** No source of this part reports it in children, so 8085/3, 8086/3 and 8070/3 at C09-C10 are picker entries and op_squamous_hpv is only proposed. Candidate source: A population-based series of head and neck carcinoma in patients aged 0-19 (for example a Surveillance, Epidemiology, and End Results analysis).
- **Paediatric occurrence of low-grade nasopharyngeal papillary adenocarcinoma.** It is a WHO nasopharynx entity; without a paediatric report it is a picker entry. Candidate source: Lai Y, et al. Cancer Manag Res 2021;13:1271-8 and Pineda-Daboin K, et al. Ann Diagn Pathol 2006;10:215-21 (Badoual references 69 and 70).
- **Immunohistochemistry that separates NUT carcinoma and lymphoma from nasopharyngeal carcinoma in a poorly differentiated tumour (NUT, CD45).** The np_ihc panel cannot exclude NUT carcinoma or lymphoma from this part's sources; a NUT-positive or CD45-positive tumour must not fall to 8020/3. Candidate source: The NUT carcinoma part's files (Luo 2025, Lemelle 2022) for NUT; a Group II source for CD45.
- **How cytology reports of nasopharyngeal carcinoma (fine-needle aspirate of a neck node) are worded.** np_cytology rests on ICD-O-3.2 terms only; no source of this part describes cytology.
- **Visser 2023 Table 4 entry, if any, for nasopharyngeal carcinoma with plasma Epstein-Barr virus DNA.** This part records no basis 4 code on the controller's statement that Visser lists no nasopharyngeal entry; Visser is not among this part's files. Candidate source: Visser O, et al. Front Oncol 2023;13:1250549, Table 4.
- **The registry rule for a neck lymph node deposit that is EBER-positive or p16-positive with no primary found.** ICCR staging treats a p16-positive node with no primary as oropharyngeal (pT0, PDF p. 3), but the registry site (C10.9, C11.9 or C80.9) is not settled by this part's sources. Candidate source: XIf11 part file Hernandez-Prera 2022 (unknown primary, head and neck).

## Registrar questions

- Oropharyngeal squamous cell carcinoma (8085/3 HPV-associated, 8086/3 HPV-independent, 8070/3 no HPV result) has no paediatric report in this part's sources. Does it stay in the oropharynx picker, or become an option with the HPV status screen `op_squamous_hpv`?
- A nasopharyngeal report that says lymphoepithelial carcinoma, lymphoepithelioma, Schmincke tumour or undifferentiated carcinoma of nasopharyngeal type: 8072/3, as the WHO 5th edition codes non-keratinising nasopharyngeal carcinoma (ICCR Table 2), or 8082/3, where ICD-O-3.2 files Lymphoepithelioma and Schmincke tumor? Rule K, applied to 'non-keratinising carcinoma with lymphoepithelial features', would also give 8082/3.
- A report that says only 'nasopharyngeal carcinoma': 8010/3 Carcinoma, NOS (built here, because the WHO definition says 'usually' squamous) or 8070/3 Squamous cell carcinoma, NOS?
- An oropharyngeal adenosquamous carcinoma that is HPV-associated: 8560/3 by Rule K (the higher code) or 8085/3 by the WHO, which removes histologic typing from HPV-associated squamous cell carcinoma?
