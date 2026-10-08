# Group 11 evidence — XIf1 salivary gland carcinoma

Part `XIf1_salivary`. Sites C07.9 parotid gland and C08.0–C08.9 other major salivary glands, ICCC-2017 subgroup XIf1. Written 8 October 2026 from the four text files assigned to this part and the page images of their tables; paediatric evidence from a fifth file, Perez-de-Oliveira 2025, was added the same day (section 11). The JSON twin is `XIf1_salivary.json` in this folder; every quote in it was checked against its PDF page of the text file.

## 1 Sources

| File | Citation | WHO volume |
|---|---|---|
| `XIf1-salivary-gland__Skalova-2022.txt` | Skalova A, Hyrcza MD, Leivo I. Update from the 5th Edition of the World Health Organization Classification of Head and Neck Tumors: Salivary Glands. Head Neck Pathol 2022;16(1):40-53. doi:10.1007/s12105-022-01420-1 | WHO Classification of Head and Neck Tumours, 5th edition |
| `XIf1-salivary-gland__ICCR-Major-Salivary-Glands-2nd.txt` | International Collaboration on Cancer Reporting. Carcinomas of the Major Salivary Glands Histopathology Reporting Guide, 2nd edition, version 2.0. Sydney: ICCR; July 2024. ISBN 978-1-922324-51-1 | WHO Classification of Head and Neck Tumours, 5th edition, 2024 |
| `ALL-paediatric-occurrence__Pfister-2022.txt` | Pfister SM, Reyes-Mugica M, Chan JKC, et al. A Summary of the Inaugural WHO Classification of Pediatric Tumors: Transitioning from the Optical into the Molecular Era. Cancer Discov 2022;12(2):331-355 | WHO Classification of Paediatric Tumours, 5th edition, 2022 |
| `RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt` | World Health Organization. International Classification of Diseases for Oncology, 3rd edition, 1st revision (ICD-O-3.1), section 4, Coding guidelines, printed pp. 14-28 | not a tumour classification; the coding manual |
| `XIf1-salivary-gland-paediatric__Perez-de-Oliveira-2025.txt` | Perez-de-Oliveira ME, et al. Epithelial salivary gland neoplasms in pediatric patients: A comprehensive review. Med Oral Patol Oral Cir Bucal 2025. doi:10.4317/medoral.26983. PMC12019652 | not a WHO summary; paediatric evidence |

The ICCR guide's Table 1 (PDF p. 8) is the World Health Organization 5th-edition entity list with ICD-O codes, reproduced with permission; it is the code source for every salivary entity below. Skalova 2022 Table 1 (PDF pp. 3–4) lists genetic alterations, not codes; it supplies the recognition aids. Pfister 2022 Table 3 (PDF p. 14, printed p. 344) and Perez-de-Oliveira 2025 are the paediatric-occurrence evidence. Perez-de-Oliveira 2025 is a PubMed Central text with sections, not pages: its cites give the PMC section number in the `pdf_page` field, and the tables here write "PMC section N". It reviews patients aged 0 to 19 years (PMC section 3). Rules file pages are cited as PDF pages; the printed page is PDF page plus 13.

## 2 Entities

Paediatric evidence comes from two files. Pfister 2022 Table 3 lists three malignant salivary entities in children (mucoepidermoid carcinoma, acinic cell carcinoma, sialoblastoma) and one benign one (pleomorphic adenoma). Perez-de-Oliveira 2025 ranks the malignant ones in children and adolescents: mucoepidermoid carcinoma first, acinic cell carcinoma second, secretory carcinoma third; it reports adenoid cystic carcinoma and polymorphous adenocarcinoma less often than in adults, and states that carcinoma ex pleomorphic adenoma has not been reported in children. Neither Skalova 2022 nor the ICCR guide gives ages. Every other current salivary carcinoma is a picker entry (data gap 1).

| Entity (WHO term) | Code | ICD-O-3.2 term matched (level) | ICD-O-3.2 preferred term | Paediatric | Decision | Page |
|---|---|---|---|---|---|---|
| Mucoepidermoid carcinoma | 8430/3 | Mucoepidermoid carcinoma (Preferred) | Mucoepidermoid carcinoma | common | option | Perez-de-Oliveira 2025, PMC section 5; Perez-de-Oliveira 2025, PMC section 1; Pfister 2022, PDF p. 14; ICCR Salivary 2024, PDF p. 8, table image |
| Acinic cell carcinoma | 8550/3 | Acinic cell adenocarcinoma (Synonym) | Acinar cell carcinoma | common | option | Perez-de-Oliveira 2025, PMC section 5; Pfister 2022, PDF p. 14; ICCR Salivary 2024, PDF p. 8, table image; ICCR Salivary 2024, PDF p. 18 |
| Salivary gland carcinoma NOS and emerging entities | 8140/3 | Adenocarcinoma, NOS (Preferred) | Adenocarcinoma, NOS | not_reported | option | ICCR Salivary 2024, PDF p. 8, table image; Skalova 2022, PDF p. 1 |
| Carcinoma, no type named | 8010/3 | Carcinoma, NOS (Preferred) | Carcinoma, NOS | not_reported | option | — |
| Adenoid cystic carcinoma | 8200/3 | Adenoid cystic carcinoma (Preferred) | Adenoid cystic carcinoma | occurs | option | Perez-de-Oliveira 2025, PMC section 5; ICCR Salivary 2024, PDF p. 8, table image |
| Secretory carcinoma | 8502/3 | Secretory carcinoma (Preferred) | Secretory carcinoma | common | option | Perez-de-Oliveira 2025, PMC section 5; ICCR Salivary 2024, PDF p. 8, table image; Skalova 2022, PDF p. 3 |
| Microsecretory adenocarcinoma | 8502/3 | not printed (none) | Secretory carcinoma | not_reported | picker | ICCR Salivary 2024, PDF p. 8, table image; ICCR Salivary 2024, PDF p. 2; Skalova 2022, PDF p. 5 |
| Polymorphous adenocarcinoma (classic and cribriform subtypes) | 8525/3 | Polymorphous adenocarcinoma (Preferred) | Polymorphous adenocarcinoma | occurs | option | Perez-de-Oliveira 2025, PMC section 5; ICCR Salivary 2024, PDF p. 8, table image; Skalova 2022, PDF p. 7; Skalova 2022, PDF p. 1 |
| Hyalinizing clear cell carcinoma | 8310/3 | not printed (none) | Clear cell adenocarcinoma, NOS | not_reported | picker | ICCR Salivary 2024, PDF p. 8, table image; Skalova 2022, PDF p. 3 |
| Basal cell adenocarcinoma | 8147/3 | Basal cell adenocarcinoma (Preferred) | Basal cell adenocarcinoma | not_reported | picker | ICCR Salivary 2024, PDF p. 8, table image |
| Salivary duct carcinoma | 8500/3 | not printed (none) | Infiltrating duct carcinoma, NOS | not_reported | picker | ICCR Salivary 2024, PDF p. 8, table image; ICD-O-3.1 manual, PDF p. 10 (printed p. 23) |
| Epithelial-myoepithelial carcinoma | 8562/3 | Epithelial-myoepithelial carcinoma (Preferred) | Epithelial-myoepithelial carcinoma | not_reported | picker | ICCR Salivary 2024, PDF p. 8, table image |
| Mucinous adenocarcinoma | 8480/3 | Mucinous adenocarcinoma (Preferred) | Mucinous adenocarcinoma | not_reported | picker | ICCR Salivary 2024, PDF p. 8, table image; Skalova 2022, PDF p. 7 |
| Sclerosing microcystic adenocarcinoma | 8407/3 | not printed (none) | Microcystic adnexal carcinoma | not_reported | picker | ICCR Salivary 2024, PDF p. 8, table image; Skalova 2022, PDF p. 5 |
| Carcinoma ex pleomorphic adenoma | 8941/3 | Carcinoma ex pleomorphic adenoma (Preferred) | Carcinoma ex pleomorphic adenoma | not_reported | picker | Perez-de-Oliveira 2025, PMC section 5; ICCR Salivary 2024, PDF p. 8, table image; ICCR Salivary 2024, PDF p. 7 |
| Sebaceous adenocarcinoma | 8410/3 | Sebaceous adenocarcinoma (Synonym) | Sebaceous carcinoma | not_reported | picker | ICCR Salivary 2024, PDF p. 8, table image |
| Lymphoepithelial carcinoma | 8082/3 | Lymphoepithelial carcinoma (Preferred) | Lymphoepithelial carcinoma | not_reported | picker | ICCR Salivary 2024, PDF p. 8, table image |
| Squamous cell carcinoma (primary in the salivary gland) | 8070/3 | Squamous cell carcinoma, NOS (Preferred) | Squamous cell carcinoma, NOS | not_reported | picker | ICCR Salivary 2024, PDF p. 8, table image; ICCR Salivary 2024, PDF p. 7 |
| Oncocytic carcinoma | 8290/3 | Oncocytic carcinoma (Synonym) | Oxyphilic adenocarcinoma | not_reported | picker | Skalova 2022, PDF p. 2 |
| Poorly differentiated carcinoma | 8020/3 | Carcinoma, poorly differentiated, NOS (Related) | Carcinoma, undifferentiated, NOS | not_reported | picker | Skalova 2022, PDF p. 1 |
| Small cell neuroendocrine carcinoma | 8041/3 | Small cell neuroendocrine carcinoma (Related) | Small cell carcinoma, NOS | not_reported | picker | ICCR Salivary 2024, PDF p. 7 |
| Large cell neuroendocrine carcinoma | 8013/3 | Large cell neuroendocrine carcinoma (Preferred) | Large cell neuroendocrine carcinoma | not_reported | picker | ICCR Salivary 2024, PDF p. 7 |
| NUT carcinoma | 8023/3 | NUT carcinoma (Synonym) | Nuclear protein in testis (NUT)-associated carcinoma | occurs | picker | Pfister 2022, PDF p. 14 |
| Myoepithelial carcinoma | 8982/3 | Myoepithelial carcinoma (Preferred) | Myoepithelial carcinoma | not_reported | refer → Group 12 | ICCR Salivary 2024, PDF p. 8, table image |
| Carcinosarcoma of the salivary glands | 8980/3 | Carcinosarcoma, NOS (Preferred) | Carcinosarcoma, NOS | not_reported | refer → Group 12 | ICCR Salivary 2024, PDF p. 8, table image; Skalova 2022, PDF p. 2 |
| Malignant mixed tumour (term not used by the World Health Organization 5th edition) | 8940/3 | Mixed tumor, salivary gland type, malignant (Synonym) | Mixed tumor, malignant, NOS | not_reported | refer → Group 12 | ICD-O-3.1 manual, PDF p. 11 (printed p. 24) |
| Intraductal carcinoma | 8500/2 | Intraductal carcinoma, NOS (Synonym) | Intraductal carcinoma, noninfiltrating, NOS | not_reported | exclusion | ICCR Salivary 2024, PDF p. 8, table image; Skalova 2022, PDF p. 7 |
| Intraductal carcinoma with invasion stated in the report | 8500/3 | Infiltrating duct carcinoma, NOS (Preferred) | Infiltrating duct carcinoma, NOS | not_reported | registrar | Skalova 2022, PDF p. 2; ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |
| Sialoblastoma | 8974/1 | Sialoblastoma (Preferred) | Sialoblastoma | occurs | exclusion | Perez-de-Oliveira 2025, PMC section 5; Pfister 2022, PDF p. 14; ICCR Salivary 2024, PDF p. 8, table image |
| Sialoblastoma that the report calls malignant | 8974/3 | not printed (none) | — | occurs | registrar → Group 12 | ICD-O-3.1 manual, PDF p. 2 (printed p. 15); Perez-de-Oliveira 2025, PMC section 5 |
| Pleomorphic adenoma (including metastasizing pleomorphic adenoma) | 8940/0 | Pleomorphic adenoma (Preferred) | Pleomorphic adenoma | common | exclusion | Perez-de-Oliveira 2025, PMC section 5; Perez-de-Oliveira 2025, PMC section 1; Pfister 2022, PDF p. 14; ICCR Salivary 2024, PDF p. 7 |
| Warthin tumour | 8561/0 | Warthin tumor (Synonym) | Adenolymphoma | not_reported | exclusion | Skalova 2022, PDF p. 4 |
| Basal cell adenoma | 8147/0 | Basal cell adenoma (Preferred) | Basal cell adenoma | not_reported | exclusion | Skalova 2022, PDF p. 4 |
| Canalicular adenoma | 8149/0 | Canalicular adenoma (Preferred) | Canalicular adenoma | not_reported | exclusion | Skalova 2022, PDF p. 4 |
| Myoepithelioma | 8982/0 | Myoepithelioma, NOS (Preferred) | Myoepithelioma, NOS | common | exclusion | Perez-de-Oliveira 2025, PMC section 5; Skalova 2022, PDF p. 2 |
| Oncocytoma | 8290/0 | Oncocytoma (Synonym) | Oxyphilic adenoma | not_reported | exclusion | ICCR Salivary 2024, PDF p. 10 |
| Sialadenoma papilliferum | 8406/0 | Sialadenoma papilliferum (Related) | Syringocystadenoma papilliferum | not_reported | exclusion | Skalova 2022, PDF p. 3 |
| Cystadenocarcinoma | 8440/3 | Cystadenocarcinoma, NOS (Preferred) | Cystadenocarcinoma, NOS | not_reported | not_built | Skalova 2022, PDF p. 7 |
| Papillary cystadenocarcinoma | 8450/3 | Papillary cystadenocarcinoma, NOS (Preferred) | Papillary cystadenocarcinoma, NOS | not_reported | not_built | — |

Notes on the table:

- **Mucoepidermoid carcinoma (8430/3).** Perez-de-Oliveira 2025 calls mucoepidermoid carcinoma the most common malignant salivary gland tumour in children and adolescents, and Pfister 2022 lists it among the malignant head and neck tumours of children. The World Health Organization codes it 8430/3.
- **Acinic cell carcinoma (8550/3).** Perez-de-Oliveira 2025 names acinic cell carcinoma the second most frequent malignant salivary gland tumour in children and adolescents, Pfister 2022 lists it among the malignant head and neck tumours of children, and the ICCR guide cites a paediatric survival series. ICD-O-3.2 prints the World Health Organization name only as the synonym Acinic cell adenocarcinoma; the preferred term at 8550/3 is Acinar cell carcinoma.
- **Salivary gland carcinoma NOS and emerging entities (8140/3).** The not-otherwise-specified fallback of the histology screen. The World Health Organization codes salivary gland carcinoma NOS and its emerging entities 8140/3; Skalova 2022 places poorly differentiated and oncocytic carcinomas in this category.
- **Carcinoma, no type named (8010/3).** The not-otherwise-specified fallback for a report that names a carcinoma and no type. It is the ICD-O-3.2 code for the term; no World Health Organization source is needed.
- **Adenoid cystic carcinoma (8200/3).** Perez-de-Oliveira 2025 states that adenoid cystic carcinoma is observed less frequently in paediatric patients than in adults; it gives no paediatric case count (data gap 2). A current World Health Organization salivary carcinoma.
- **Secretory carcinoma (8502/3).** Perez-de-Oliveira 2025 names secretory carcinoma the third most frequent malignant salivary gland tumour in children and adolescents, after mucoepidermoid and acinic cell carcinoma. It resembles acinic cell carcinoma and carries an ETV6 translocation. A current World Health Organization salivary carcinoma.
- **Microsecretory adenocarcinoma (8502/3).** A new World Health Organization 5th-edition entity. ICD-O-3.2 prints no term for it; the ICCR Table 1 gives it 8502/3, a code ICD-O-3.2 holds. The ICCR table prints it as Microsecretory carcinoma; the ICCR value list and Skalova 2022 call it microsecretory adenocarcinoma.
- **Polymorphous adenocarcinoma (classic and cribriform subtypes) (8525/3).** Perez-de-Oliveira 2025 states that polymorphous adenocarcinoma is observed less frequently in paediatric patients than in adults; it gives no paediatric case count (data gap 2). Predominantly a minor salivary gland tumour. Cribriform adenocarcinoma of salivary gland origin is now its cribriform subtype and takes the same code. The ICCR table prints Polymorphous carcinoma, an ICD-O-3.2 synonym.
- **Hyalinizing clear cell carcinoma (8310/3).** ICD-O-3.2 prints no term for hyalinizing clear cell carcinoma; the ICCR Table 1 gives it 8310/3, whose preferred term is Clear cell adenocarcinoma, NOS.
- **Basal cell adenocarcinoma (8147/3).** A current World Health Organization salivary carcinoma with no paediatric report in this part's sources.
- **Salivary duct carcinoma (8500/3).** ICD-O-3.2 prints no salivary duct carcinoma term; the ICCR Table 1 gives it 8500/3. ICD-O-3.1 Table 23 attaches 8500/3 to breast but lists the parotid and salivary glands as other primary sites, so the salivary site stands (Rule H).
- **Epithelial-myoepithelial carcinoma (8562/3).** A current World Health Organization salivary carcinoma with no paediatric report in this part's sources.
- **Mucinous adenocarcinoma (8480/3).** Occurs typically in oral minor salivary glands; no paediatric report in this part's sources. Its signet ring subtype raises a Rule K question (registrar question 6).
- **Sclerosing microcystic adenocarcinoma (8407/3).** Described so far in minor salivary glands only. ICD-O-3.2 prints no term for it; the ICCR Table 1 gives it 8407/3. ICCC-2017 places 8407 only in XIe (skin, C44): at C07-C08 it lies outside every range, so under the registrar's ruling of 1 October 2026 it belongs to Group XI and takes XIf1 by site.
- **Carcinoma ex pleomorphic adenoma (8941/3).** Perez-de-Oliveira 2025 states that malignant transformation of pleomorphic adenoma has not been reported in paediatric patients, so it stays a picker entry. The ICCR guide asks the pathologist to report the type of the carcinoma inside the pleomorphic adenoma and its extent of invasion; the World Health Organization codes the whole tumour 8941/3 (registrar questions 4 and 5).
- **Sebaceous adenocarcinoma (8410/3).** A current World Health Organization salivary carcinoma with no paediatric report in this part's sources.
- **Lymphoepithelial carcinoma (8082/3).** A current World Health Organization salivary carcinoma with no paediatric report in this part's sources. At C07-C08 ICCC-2017 places 8082 in XIf1; at the nasopharynx it is XIc.
- **Squamous cell carcinoma (primary in the salivary gland) (8070/3).** The ICCR guide states that squamous cell carcinoma in a salivary gland is typically a metastasis; the picker entry is for a report that states a salivary primary, and the deposit option covers the rest.
- **Oncocytic carcinoma (8290/3).** The World Health Organization 5th edition moves oncocytic carcinoma into the emerging entities. ICD-O-3.2 prints the term itself at 8290/3, so the term's own code is used (registrar question 7).
- **Poorly differentiated carcinoma (8020/3).** Skalova 2022 places poorly differentiated carcinomas in the not-otherwise-specified category; ICD-O-3.2 prints the term at 8020/3 (registrar question 7).
- **Small cell neuroendocrine carcinoma (8041/3).** The ICCR guide records primary salivary neuroendocrine carcinomas under other types; ICCC-2017 places 8041 in XIf1 at C07-C08.
- **Large cell neuroendocrine carcinoma (8013/3).** As for small cell neuroendocrine carcinoma.
- **NUT carcinoma (8023/3).** Pfister 2022 lists NUT carcinoma among malignant head and neck tumours of children without naming a salivary site, and neither salivary source lists it, so it is a picker entry here. ICCC-2017 places 8023 in XIf1 at C07-C08.
- **Myoepithelial carcinoma (8982/3).** A World Health Organization salivary carcinoma that ICCC-2017 places in XIIa4 (other complex mixed and stromal neoplasms, every site), not in Group XI (registrar question 2).
- **Carcinosarcoma of the salivary glands (8980/3).** ICCC-2017 places 8980 in XIIa4 at every site (registrar question 2).
- **Malignant mixed tumour (term not used by the World Health Organization 5th edition) (8940/3).** Not a World Health Organization 5th-edition entity, but ICD-O-3.2 keeps the term current at 8940/3 and ICCC-2017 places 8940 in XIIa4.
- **Intraductal carcinoma (8500/2).** The World Health Organization codes it 8500/2, in situ, outside Group XI. Its intact myoepithelial layer shows its in situ nature.
- **Intraductal carcinoma with invasion stated in the report (8500/3).** Skalova 2022 reports frank invasive growth in some intraductal carcinomas. Rule F codes the behaviour the pathologist states, which gives 8500/3; the registrar confirms (registrar question 3).
- **Sialoblastoma (8974/1).** Perez-de-Oliveira 2025 calls sialoblastoma a rare malignant neoplasm diagnosed mainly in the neonatal period or early childhood, most often in the parotid gland, and Pfister 2022 lists it among malignant head and neck tumours of children. Neither gives a code or behaviour; ICD-O-3.2 and the ICCR Table 1 print it at /1, outside Group XI and outside every ICCC-2017 range (registrar question 1).
- **Sialoblastoma that the report calls malignant (8974/3).** Rule F codes a behaviour the pathologist states. ICD-O-3.2 prints no 8974/3; ICCC-2017 places 8974 at /3 in XIIa4, so the proposed outcome is a Group 12 referral (registrar question 1). Perez-de-Oliveira 2025 calls sialoblastoma a malignant neoplasm without giving a behaviour code.
- **Pleomorphic adenoma (including metastasizing pleomorphic adenoma) (8940/0).** Benign. Perez-de-Oliveira 2025 calls pleomorphic adenoma the most prevalent salivary gland tumour in children and adolescents, and Pfister 2022 lists it among benign head and neck tumours of children; the ICCR guide states that metastasizing pleomorphic adenoma is benign under the World Health Organization classification.
- **Warthin tumour (8561/0).** Benign.
- **Basal cell adenoma (8147/0).** Benign; the benign counterpart of basal cell adenocarcinoma.
- **Canalicular adenoma (8149/0).** Benign.
- **Myoepithelioma (8982/0).** Benign. Perez-de-Oliveira 2025 Table 1 names pleomorphic adenoma and myoepithelioma as the main benign salivary gland tumours of children and adolescents. Skalova 2022 notes that a core biopsy may not separate it from myoepithelial carcinoma, so a report must state carcinoma before a carcinoma is coded.
- **Oncocytoma (8290/0).** Benign.
- **Sialadenoma papilliferum (8406/0).** Benign.
- **Cystadenocarcinoma (8440/3).** Every ICD-O-3.2 term at 8440/3 is [obs]. The World Health Organization 5th-edition salivary table in the ICCR guide lists no cystadenocarcinoma, and neither source names its successor (data gap 3). Skalova 2022 records that an earlier 'low-grade cribriform cystadenocarcinoma' was renamed intraductal carcinoma, which is 8500/2.
- **Papillary cystadenocarcinoma (8450/3).** Every ICD-O-3.2 term at 8450/3 is [obs]; neither source lists the entity or names a successor.

The picker also carries every other current behaviour-3 code ICCC-2017 places in XIf1 (164 of the 174 XIf1 codes in `g11_inventory.json` have a current /3 term), each under its ICD-O-3.2 preferred term, plus 8407/3, which lies outside every ICCC range at this site. The ten XIf1 codes whose every /3 term is [obs] are not built: 8042, 8124, 8130, 8141, 8245, 8251, 8440, 8450, 8508, 8512.

## 3 The pathway

Order: `sg_site` (may merge into the router's site capture) → `sg_document_inventory` → `sg_cytology` or `sg_histology` → `sg_carcinoma_picker`, `sg_sialoblastoma` or `sg_not_malignant`. When `sg_histology` or `sg_carcinoma_picker` is reached through `sg_cytology`, every code answer records basis 5, not 7. There is no tumour-marker tier: Visser 2023 Table 4 names no salivary marker.

### `sg_site` (site_resolution)

**Question:** Which salivary gland does the report name as the site of the tumour?

**Hint:** Pick a gland only when the report places the tumour in it. When the tumour spreads across more than one major salivary gland and the report does not say where it began, pick the overlapping lesion. A tumour of a minor salivary gland is coded to the place where that gland lies, such as the hard palate.

| Option | Outcome | Records | Reason | Recognition aid | Page |
|---|---|---|---|---|---|
| Parotid gland | go | → `sg_document_inventory` | Site recorded as Parotid gland (C07.9). | — | ICCR Salivary 2024, PDF p. 4 |
| Submandibular gland | go | → `sg_document_inventory` | Site recorded as Submandibular gland (C08.0). | — | ICCR Salivary 2024, PDF p. 4 |
| Sublingual gland | go | → `sg_document_inventory` | Site recorded as Sublingual gland (C08.1). | — | ICCR Salivary 2024, PDF p. 4 |
| More than one major salivary gland, and the report does not say where the tumour began | go | → `sg_document_inventory` | Site recorded as Overlapping lesion of major salivary glands (C08.8). | — | ICD-O-3.1 manual, PDF p. 5 (printed p. 18) |
| A major salivary gland, with no gland named | go | → `sg_document_inventory` | Site recorded as Major salivary gland, not otherwise specified (C08.9). | — | — |
| The region of a salivary gland, or beside it (for example periparotid), with no gland named as the site | refer | Group 11, site recaptured | A tumour placed beside or in the region of a gland is coded to head, face and neck, not otherwise specified (C76.0), unless the tumour type shows that it arose in the gland. | — | ICD-O-3.1 manual, PDF p. 1 (printed p. 14) |
| A minor salivary gland, for example of the palate, lip, cheek or tongue | refer | Group 11, site recaptured | A minor salivary gland tumour is coded to the place where the gland lies, such as the hard palate (C05.0). When the report names no place, the site is mouth, not otherwise specified (C06.9). | — | ICD-O-3.1 manual, PDF p. 11 (printed p. 24); ICCR Salivary 2024, PDF p. 4 |

### `sg_document_inventory` (document_inventory)

**Question:** What is in the file for this tumour?

**Hint:** A radiology report counts as imaging. A fine needle aspiration report counts as cytology. A pathology report on a biopsy or resection counts as histology. A cytology or biopsy report that calls the specimen inadequate or non-diagnostic counts as no tissue.

| Option | Outcome | Records | Reason | Recognition aid | Page |
|---|---|---|---|---|---|
| A referral letter or clinical note that states a malignant salivary gland tumour, with no imaging report and no tissue | code | 8000/3, basis 1 | Recorded as Neoplasm, malignant (8000/3) on clinical evidence. | — | — |
| An imaging report that states a malignant salivary gland tumour, with no tissue | code | 8000/3, basis 2 | Recorded as Neoplasm, malignant (8000/3) on imaging evidence. | — | — |
| A note or report that calls the tumour possible, probable or suspected cancer only | not_registrable | not registrable | A possible or suspected cancer is not registered. | — | — |
| A cytology report (fine needle aspiration) | go | → `sg_cytology` (basis 5) | — | — | Skalova 2022, PDF p. 2; ICCR Salivary 2024, PDF p. 5 |
| A histology report on a biopsy or resection, with or without immunohistochemistry or gene reports | go | → `sg_histology` (basis 7) | — | — | — |

### `sg_cytology` (morphology_only)

**Question:** What does the cytology report call the tumour?

**Hint:** Code a carcinoma only when the report states one. Suspicious or atypical is not a diagnosis of cancer.

| Option | Outcome | Records | Reason | Recognition aid | Page |
|---|---|---|---|---|---|
| A named carcinoma type, such as mucoepidermoid carcinoma or acinic cell carcinoma | go | → `sg_histology` (basis 5) | — | — | Skalova 2022, PDF p. 2 |
| Carcinoma, with no type named | code | 8010/3, basis 5 | Recorded as Carcinoma, NOS (8010/3) on cytology. | — | — |
| Malignant, with no tumour type named | code | 8000/3, basis 5 | Recorded as Neoplasm, malignant (8000/3) on cytology. | — | — |
| Lymphoma | refer | Group 2 | Lymphoma is coded in Group II, lymphomas and reticuloendothelial neoplasms. | — | ICCR Salivary 2024, PDF p. 4 |
| Suspicious for malignancy, atypical, benign, or non-diagnostic | not_registrable | not registrable | The cytology report does not state a malignant tumour, so nothing is registered. | — | — |

### `sg_histology` (morphology_only)

**Question:** What does the histology report call the tumour?

**Hint:** The grade the report gives, and high grade transformation, do not change the code: pick the carcinoma type the report names.

| Option | Outcome | Records | Reason | Recognition aid | Page |
|---|---|---|---|---|---|
| Mucoepidermoid carcinoma | code | 8430/3, basis 7 | Recorded as Mucoepidermoid carcinoma (8430/3). | The report may give a low, intermediate or high grade, or name a CRTC1::MAML2 or CRTC3::MAML2 fusion. | Perez-de-Oliveira 2025, PMC section 5; Perez-de-Oliveira 2025, PMC section 1; Pfister 2022, PDF p. 14; ICCR Salivary 2024, PDF p. 8, table image; Skalova 2022, PDF p. 2; Skalova 2022, PDF p. 3 |
| Acinic cell carcinoma | code | 8550/3, basis 7 | Recorded as Acinar cell carcinoma (8550/3). | The report may name an NR4A3 rearrangement, or high grade transformation. | Perez-de-Oliveira 2025, PMC section 5; Pfister 2022, PDF p. 14; ICCR Salivary 2024, PDF p. 8, table image; Skalova 2022, PDF p. 3; ICCR Salivary 2024, PDF p. 9 |
| Secretory carcinoma | code | 8502/3, basis 7 | Recorded as Secretory carcinoma (8502/3). | Secretory carcinoma resembles acinic cell carcinoma. The report may name an ETV6 translocation, an ETV6::NTRK3 fusion or strong mammaglobin staining. | Perez-de-Oliveira 2025, PMC section 5; ICCR Salivary 2024, PDF p. 8, table image; Skalova 2022, PDF p. 3; Skalova 2022, PDF p. 5 |
| Adenoid cystic carcinoma | code | 8200/3, basis 7 | Recorded as Adenoid cystic carcinoma (8200/3). | The report may describe a tubular, cribriform or solid pattern, or name a MYB::NFIB fusion or another MYB or MYBL1 rearrangement. | Perez-de-Oliveira 2025, PMC section 5; ICCR Salivary 2024, PDF p. 8, table image; ICCR Salivary 2024, PDF p. 2; Skalova 2022, PDF p. 3 |
| Polymorphous adenocarcinoma, classic or cribriform subtype | code | 8525/3, basis 7 | Recorded as Polymorphous adenocarcinoma (8525/3). | Cribriform adenocarcinoma of salivary gland origin is the cribriform subtype of polymorphous adenocarcinoma. | Perez-de-Oliveira 2025, PMC section 5; ICCR Salivary 2024, PDF p. 8, table image; Skalova 2022, PDF p. 1; Skalova 2022, PDF p. 7 |
| Another carcinoma the report names, such as salivary duct carcinoma, epithelial-myoepithelial carcinoma or carcinoma ex pleomorphic adenoma | go | → `sg_carcinoma_picker` | — | — | — |
| Salivary gland carcinoma, not otherwise specified, or adenocarcinoma, not otherwise specified | code | 8140/3, basis 7 | Recorded as Adenocarcinoma, NOS (8140/3). | — | ICCR Salivary 2024, PDF p. 8, table image |
| Carcinoma, with no type named | code | 8010/3, basis 7 | Recorded as Carcinoma, NOS (8010/3). | — | — |
| Sialoblastoma | go | → `sg_sialoblastoma` | — | — | Perez-de-Oliveira 2025, PMC section 5; Pfister 2022, PDF p. 14; ICCR Salivary 2024, PDF p. 8, table image |
| A benign tumour or a non-invasive carcinoma, such as pleomorphic adenoma, Warthin tumour, another adenoma, myoepithelioma, oncocytoma or intraductal carcinoma | go | → `sg_not_malignant` | — | — | Pfister 2022, PDF p. 14 |
| Lymphoma | refer | Group 2 | Lymphoma is coded in Group II, lymphomas and reticuloendothelial neoplasms. A lymphoma in a lymph node within or beside the parotid takes a lymph node site; a lymphoma of the gland itself takes the gland's site. | — | ICCR Salivary 2024, PDF p. 4; ICD-O-3.1 manual, PDF p. 2 (printed p. 15); ICCR Salivary 2024, PDF p. 9 |
| Rhabdomyosarcoma or another sarcoma | refer | Group 9 | A sarcoma of the salivary gland is coded in Group IX, soft-tissue and other extraosseous sarcomas. | — | ICCR Salivary 2024, PDF p. 4 |
| Melanoma | go | → `melanoma tree entry (controller binds the node id)` | Melanoma is coded through the melanoma questions. | — | ICCR Salivary 2024, PDF p. 4 |
| A deposit (metastasis) of a tumour that began elsewhere, such as squamous cell carcinoma or melanoma in a lymph node of the parotid | refer | primary site, site recaptured | A deposit is coded at the site where the tumour began. The next question asks for that site. | — | ICCR Salivary 2024, PDF p. 7; ICCR Salivary 2024, PDF p. 9 |

### `sg_carcinoma_picker` (morphology_only)

**Question:** Which carcinoma does the histology report name?

**Hint:** Type part of the name to filter the list. When the report names two carcinoma types for one tumour and no entry covers both, pick the one with the higher code number.

| Option | Outcome | Records | Reason | Recognition aid | Page |
|---|---|---|---|---|---|
| Microsecretory adenocarcinoma | code | 8502/3, basis 7 | Recorded as Secretory carcinoma (8502/3), the code the World Health Organization gives microsecretory adenocarcinoma. | The report may name an MEF2C::SS18 fusion. | ICCR Salivary 2024, PDF p. 8, table image; Skalova 2022, PDF p. 3 |
| Hyalinizing clear cell carcinoma | code | 8310/3, basis 7 | Recorded as Clear cell adenocarcinoma, NOS (8310/3). | The report may name an EWSR1::ATF1 fusion. | ICCR Salivary 2024, PDF p. 8, table image; Skalova 2022, PDF p. 3 |
| Basal cell adenocarcinoma | code | 8147/3, basis 7 | Recorded as Basal cell adenocarcinoma (8147/3). | — | ICCR Salivary 2024, PDF p. 8, table image |
| Salivary duct carcinoma | code | 8500/3, basis 7 | Recorded as Infiltrating duct carcinoma, NOS (8500/3), the code the World Health Organization gives salivary duct carcinoma, at the salivary gland site. | — | ICCR Salivary 2024, PDF p. 8, table image; ICD-O-3.1 manual, PDF p. 10 (printed p. 23) |
| Epithelial-myoepithelial carcinoma | code | 8562/3, basis 7 | Recorded as Epithelial-myoepithelial carcinoma (8562/3). | — | ICCR Salivary 2024, PDF p. 8, table image |
| Mucinous adenocarcinoma | code | 8480/3, basis 7 | Recorded as Mucinous adenocarcinoma (8480/3). | The report may describe a papillary, colloid, signet ring or mixed pattern, or an AKT1 E17K mutation. | ICCR Salivary 2024, PDF p. 8, table image; Skalova 2022, PDF p. 7; Skalova 2022, PDF p. 3 |
| Sclerosing microcystic adenocarcinoma | code | 8407/3, basis 7 | Recorded as Microcystic adnexal carcinoma (8407/3), the code the World Health Organization gives sclerosing microcystic adenocarcinoma. | — | ICCR Salivary 2024, PDF p. 8, table image |
| Carcinoma ex pleomorphic adenoma | code | 8941/3, basis 7 | Recorded as Carcinoma ex pleomorphic adenoma (8941/3). | The report names the carcinoma inside the pleomorphic adenoma, most often salivary duct carcinoma, myoepithelial carcinoma or epithelial-myoepithelial carcinoma. | ICCR Salivary 2024, PDF p. 8, table image; ICCR Salivary 2024, PDF p. 7 |
| Sebaceous adenocarcinoma | code | 8410/3, basis 7 | Recorded as Sebaceous carcinoma (8410/3). | — | ICCR Salivary 2024, PDF p. 8, table image |
| Lymphoepithelial carcinoma | code | 8082/3, basis 7 | Recorded as Lymphoepithelial carcinoma (8082/3). | — | ICCR Salivary 2024, PDF p. 8, table image |
| Squamous cell carcinoma, which the report states began in the salivary gland | code | 8070/3, basis 7 | Recorded as Squamous cell carcinoma, NOS (8070/3). | The report may name sialodochodysplasia, or state that a skin or mucosal primary has been excluded. | ICCR Salivary 2024, PDF p. 8, table image; ICCR Salivary 2024, PDF p. 7 |
| Oncocytic carcinoma | code | 8290/3, basis 7 | Recorded as Oxyphilic adenocarcinoma (8290/3). | — | Skalova 2022, PDF p. 2 |
| Poorly differentiated carcinoma or undifferentiated carcinoma | code | 8020/3, basis 7 | Recorded as Carcinoma, undifferentiated, NOS (8020/3). | — | Skalova 2022, PDF p. 1 |
| Small cell neuroendocrine carcinoma | code | 8041/3, basis 7 | Recorded as Small cell carcinoma, NOS (8041/3). | — | ICCR Salivary 2024, PDF p. 7 |
| Large cell neuroendocrine carcinoma | code | 8013/3, basis 7 | Recorded as Large cell neuroendocrine carcinoma (8013/3). | — | ICCR Salivary 2024, PDF p. 7 |
| NUT carcinoma | code | 8023/3, basis 7 | Recorded as Nuclear protein in testis (NUT)-associated carcinoma (8023/3). | — | Pfister 2022, PDF p. 14 |
| Myoepithelial carcinoma | refer | Group 12 (8982/3) | Myoepithelial carcinoma (8982/3) is coded in Group XII, other and unspecified malignant neoplasms. | — | ICCR Salivary 2024, PDF p. 8, table image |
| Carcinosarcoma | refer | Group 12 (8980/3) | Carcinosarcoma, NOS (8980/3) is coded in Group XII, other and unspecified malignant neoplasms. | — | ICCR Salivary 2024, PDF p. 8, table image |
| Malignant mixed tumour | refer | Group 12 (8940/3) | Mixed tumor, malignant, NOS (8940/3) is coded in Group XII, other and unspecified malignant neoplasms. | — | ICD-O-3.1 manual, PDF p. 11 (printed p. 24) |

### `sg_sialoblastoma` (histology_subclassification)

**Question:** Does the report call the sialoblastoma malignant?

| Option | Outcome | Records | Reason | Recognition aid | Page |
|---|---|---|---|---|---|
| No, or the report gives no behaviour | exclude | excluded, 8974/1 | Sialoblastoma (8974/1) is of uncertain behaviour and is not registered as a malignant tumour. | — | ICCR Salivary 2024, PDF p. 8, table image |
| Yes, the report calls it malignant | refer | Group 12 (8974/3) | A sialoblastoma the pathologist calls malignant takes behaviour 3 (8974/3) and is coded in Group XII, other and unspecified malignant neoplasms. | — | ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |

### `sg_not_malignant` (morphology_only)

**Question:** Which tumour does the report name?

| Option | Outcome | Records | Reason | Recognition aid | Page |
|---|---|---|---|---|---|
| Pleomorphic adenoma, including metastasizing pleomorphic adenoma | exclude | excluded, 8940/0 | Pleomorphic adenoma (8940/0) is benign and is not registered in this group. | — | Perez-de-Oliveira 2025, PMC section 5; Perez-de-Oliveira 2025, PMC section 1; Pfister 2022, PDF p. 14; ICCR Salivary 2024, PDF p. 7 |
| Myoepithelioma | exclude | excluded, 8982/0 | Myoepithelioma, NOS (8982/0) is benign and is not registered in this group. | — | Perez-de-Oliveira 2025, PMC section 5; Skalova 2022, PDF p. 2 |
| Warthin tumour | exclude | excluded, 8561/0 | Adenolymphoma (8561/0) is benign and is not registered in this group. | — | Skalova 2022, PDF p. 4 |
| Basal cell adenoma | exclude | excluded, 8147/0 | Basal cell adenoma (8147/0) is benign and is not registered in this group. | — | Skalova 2022, PDF p. 3 |
| Canalicular adenoma | exclude | excluded, 8149/0 | Canalicular adenoma (8149/0) is benign and is not registered in this group. | — | Skalova 2022, PDF p. 4 |
| Oncocytoma | exclude | excluded, 8290/0 | Oxyphilic adenoma (8290/0) is benign and is not registered in this group. | — | ICCR Salivary 2024, PDF p. 10 |
| Sialadenoma papilliferum | exclude | excluded, 8406/0 | Syringocystadenoma papilliferum (8406/0) is benign and is not registered in this group. | — | Skalova 2022, PDF p. 3 |
| Intraductal carcinoma, with no invasion stated | exclude | excluded, 8500/2 | Intraductal carcinoma, noninfiltrating, NOS (8500/2) is in situ and is not registered in this group. | — | ICCR Salivary 2024, PDF p. 8, table image; Skalova 2022, PDF p. 7 |
| Intraductal carcinoma, and the report states invasion or invasive growth | code | 8500/3, basis 7 | Recorded as Infiltrating duct carcinoma, NOS (8500/3), because the report states invasion. | — | Skalova 2022, PDF p. 2; ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |
| Another benign tumour, such as sclerosing polycystic adenoma, keratocystoma, intercalated duct adenoma or striated duct adenoma | not_registrable | not registrable | A benign salivary gland tumour is not registered as a cancer. | — | Skalova 2022, PDF p. 1 |

## 4 Immunohistochemistry rules

None built. In these sources the histology report names the salivary entity; marker profiles appear only as the pathologist's differential diagnosis, and no panel separates two codes the clerk could otherwise not tell apart. The one marker contrast that crosses a group boundary is microsecretory adenocarcinoma (S100, SOX10 and p63 positive; p40, calponin, smooth muscle actin and mammaglobin negative) against myoepithelial carcinoma (calponin, smooth muscle actin and p40 positive) (Skalova 2022, PDF p. 5): 8502/3 in XIf1 against 8982/3 in Group XII. An immunohistochemistry report on its own does not stand in for the histology report's diagnosis, so the tree does not build this as a checklist. Microsecretory adenocarcinoma and secretory carcinoma (strong mammaglobin, Skalova 2022, PDF p. 5) share 8502/3, so no panel is needed between them.

## 5 Registration without tissue

| Evidence | Code | Basis |
|---|---|---|
| A referral letter or clinical note that states a malignant salivary gland tumour, no imaging, no tissue | 8000/3 | 1 |
| An imaging report that states a malignant salivary gland tumour, no tissue | 8000/3 | 2 |

Source: the registrar's rule from Visser 2023 as relayed by the controller; this part holds no copy, so these rows carry no page (data gap 6). No Visser Table 3 or Table 4 exception applies at a salivary site. 'Possible' or 'suspected' is not registrable. ICCC-2017 places 8000/3 at C07–C08 in XIIb, so these registrations compute to Group XII (conflicts, registrar question 8).

## 6 Laboratory tests

None. Neither salivary source gives a serum or urine test a diagnostic role. The tree has no laboratory screen.

## 7 Rules A to K

| Rule | Applies | Where it reaches the clerk |
|---|---|---|
| A | no | The salivary glands are named organs, not ill-defined regions. A face or neck tumour reaches this tree only after the router's site capture names a salivary gland. |
| B | yes | sg_site hint ('Pick a gland only when the report places the tumour in it') and the option 'The region of a salivary gland, or beside it', whose reason gives C76.0 unless the tumour type shows origin in the gland (registrar question 9). |
| C | yes | sg_site option 'More than one major salivary gland, and the report does not say where the tumour began' records C08.8, and the hint names the overlapping lesion. |
| D | yes | sg_histology Lymphoma option reason: a lymphoma in an intraparotid lymph node takes a lymph node site, a lymphoma of the gland takes the gland's site; Group II codes it. |
| E | no | No leukaemia option at this site. A leukaemic deposit leaves through the deposit option. |
| F | yes | sg_sialoblastoma (the report calls it malignant: 8974/3, Group XII); sg_not_malignant (intraductal carcinoma with invasion stated: 8500/3); every exclusion reason names the code with its non-malignant behaviour. Codes whose WHO term ICD-O-3.2 does not print (acinic cell carcinoma, salivary duct carcinoma, hyalinizing clear cell carcinoma, microsecretory and sclerosing microcystic adenocarcinoma) take the code with behaviour 3, and the reason names the preferred term. |
| G | no | No screen offers two grades: grade does not change any code here and the sixth digit is not built. The sg_histology hint says the grade does not change the code. |
| H | yes | Salivary duct carcinoma picker reason: 8500/3 is recorded at the salivary site although ICD-O ties the term to breast. sg_site minor salivary gland option reason: a minor salivary gland tumour takes the site where the gland lies, or C06.9 when none is named. |
| J | no | Every term on these screens reaches its code through ICD-O-3.2 or the WHO table without reordering word roots. |
| K | yes | sg_carcinoma_picker hint: two carcinoma types for one tumour with no entry covering both take the higher code number. sg_histology hint: high grade transformation keeps the carcinoma type's code (8550 is higher than 8020 Dedifferentiated carcinoma). Carcinoma ex pleomorphic adenoma with a myoepithelial component and mucinous adenocarcinoma with a signet ring pattern wait on the registrar (questions 5 and 6). |

Sources: Rule A, ICD-O-3.1 manual PDF p. 1 (printed p. 14); Rule B, PDF p. 1 and p. 4; Rule C and Table 17 (C08.8), PDF p. 5 (printed p. 18); Rule D, PDF p. 2; Rule F, PDF p. 2; Rule G, PDF p. 2; Rule H, PDF p. 2, Table 23 PDF p. 10 (printed p. 23) and the minor salivary gland paragraph PDF p. 11 (printed p. 24); Rules J and K, PDF p. 3 (printed p. 16). Grading: ICCR Salivary 2024 PDF pp. 8–9 and Skalova 2022 PDF p. 2.

## 8 Code currency

| Code | Finding | What the tree does |
|---|---|---|
| 8502/3 | Currency check section 4: the REDCap label is 'Secretory carcinoma of breast'; the ICD-O-3.2 preferred term is Secretory carcinoma. The ICCR Table 1 also gives microsecretory adenocarcinoma 8502/3. | Both options record 8502/3 with the reason naming Secretory carcinoma; the relabel goes on the REDCap-side list. |
| 8525/3 | Currency check section 4: the REDCap label is 'Polymorphous low grade adenocarcinoma'; the preferred term is Polymorphous adenocarcinoma. The ICCR Table 1 prints 'Polymorphous carcinoma', an ICD-O-3.2 synonym. | Reason names Polymorphous adenocarcinoma; relabel goes on the REDCap-side list. |
| 8941/3 | Currency check section 4: the REDCap label is 'Carcinoma in pleomorphic adenoma' (a synonym); the preferred term is Carcinoma ex pleomorphic adenoma. | Reason names Carcinoma ex pleomorphic adenoma; relabel goes on the REDCap-side list. |
| 8410/3 | Currency check section 4: the REDCap label is 'Sebaceous adenocarcinoma' (a synonym); the preferred term is Sebaceous carcinoma. | Reason names Sebaceous carcinoma; relabel goes on the REDCap-side list. |
| 8407/3 | Currency check section 4: REDCap offers 8407 only under XIe, labelled 'Sclerosing sweat duct carcinoma'; the preferred term is Microcystic adnexal carcinoma. The REDCap XIf list has no 8407. ICCC-2017 places 8407 only in XIe (C44); at C07-C08 it lies in no range. | Picker entry records 8407/3; the subgroup is XIf1 by site under the 1 October 2026 ruling. The missing XIf option goes on the REDCap-side list. |
| 8550/3 | ICD-O-3.2 does not print 'Acinic cell carcinoma'; the nearest term is the synonym Acinic cell adenocarcinoma, and the preferred term is Acinar cell carcinoma. 8550/1 Acinar cell tumor and its synonym Acinic cell tumor are [obs]. | Option label keeps the report term; reason names Acinar cell carcinoma (8550/3). No /1 option is built. |
| 8430/1 | 8430/1 Mucoepidermoid tumor is [obs] in ICD-O-3.2. | Not built; every mucoepidermoid carcinoma records 8430/3. |
| 8500/3 | ICD-O-3.2 prints no 'Salivary duct carcinoma'; the WHO code is 8500/3 Infiltrating duct carcinoma, NOS, site-associated with breast in ICD-O-3.1 Table 23, which lists parotid and salivary gland as other primary sites. | Reason states the salivary site is kept (Rule H). |
| 8310/3 | ICD-O-3.2 prints no 'Hyalinizing clear cell carcinoma'; the WHO code is 8310/3 Clear cell adenocarcinoma, NOS. | Reason names Clear cell adenocarcinoma, NOS. |
| 8440/3 | Currency check section 2: every /3 term is [obs]; no successor printed. The ICCR salivary Table 1 lists no cystadenocarcinoma. | not_built; data gap 3. |
| 8450/3 | Currency check section 2: every /3 term is [obs]; no successor printed. | not_built. |
| 8023/3 | Currency check section 6: new in ICD-O-3.2 and not offered by REDCap. | Picker entry; the missing REDCap option goes on the REDCap-side list. |
| 8974/1 | ICD-O-3.2 holds sialoblastoma at /1 only; ICCC-2017 holds 8974 at /3 only, in XIIa4. REDCap Group 11 does not offer 8974. | Exclusion at /1; Rule F referral to Group XII at /3 waits on the registrar. |
| 8982/3 | Current (Myoepithelial carcinoma). Not in any ICCC-2017 Group XI range and not in the REDCap Group 11 list; ICCC places it in XIIa4. | Referral to Group XII. |
| 8980/3 | Current (Carcinosarcoma, NOS). ICCC-2017 XIIa4; not in the REDCap Group 11 list. | Referral to Group XII. |
| 8940/3 | Current (Mixed tumor, malignant, NOS; synonym Mixed tumor, salivary gland type, malignant). ICCC-2017 XIIa4. The WHO 5th-edition salivary table does not list it. | Picker referral to Group XII. |

REDCap-side list (standing rule 16; the tool does not test REDCap): relabel 8502, 8525, 8941 and 8410 in the XIf list to the ICD-O-3.2 preferred term; add 8407 and 8023 to the XIf list. 8982, 8980, 8940 and 8974 belong to Group XII's list, not Group 11's.

## 9 Conflicts with other groups

| Other group | Codes | Sites | Issue |
|---|---|---|---|
| 12 | 8982, 8980, 8940 | C07.9, C08.0, C08.1, C08.8, C08.9 | The WHO lists myoepithelial carcinoma and carcinosarcoma as salivary carcinomas, but ICCC-2017 places 8982, 8980 and 8940 in XIIa4 at every site, so the tree refers them to Group XII. |
| 12 | 8974 | C07.9, C08.0, C08.1, C08.8, C08.9 | Sialoblastoma is /1 in ICD-O-3.2 and in the WHO table, outside every ICCC group; ICCC-2017 holds 8974/3 in XIIa4. A sialoblastoma the report calls malignant goes to Group XII. |
| 12 | 8000 | C07.9, C08.0, C08.1, C08.8, C08.9 | ICCC-2017 places 8000/3 at C07-C08 in XIIb, so a registration without tissue (basis 1 or 2) or a cytology report that says only 'malignant' is computed to Group XII, not XIf1. |
| 11 | 8407 | C07.9, C08.0, C08.1, C08.8, C08.9 | ICCC-2017 holds 8407 only in XIe (C44). At C07-C08 it lies in no range, so the subgroup computation from site must place it in XIf1 under the 1 October 2026 ruling, or it returns no subgroup. |
| 2 | 9699, 9680, 9650 | C07.9, C08.0, C08.1, C08.8, C08.9 | Lymphoma of the salivary gland is Group II (IIb2 for 9699 and 9680, IIa for 9650 at C07-C08). A lymphoma in an intraparotid lymph node takes a lymph node site under Rule D. |
| 9 | 8900, 8910, 8920, 9364 | C07.9, C08.0, C08.1, C08.8, C08.9 | Rhabdomyosarcoma at C07-C08 is IXa; an extraosseous Ewing sarcoma (9364) there is IXd2, Group IX not Group VIII. |
| 11 | 8720 | C07.9, C08.0, C08.1, C08.8, C08.9 | Melanoma at C07-C08 is XId and goes to the melanoma tree; a melanoma deposit in a parotid lymph node goes to the deposit option. |
| 11 | 8082, 8200, 8430, 8525, 8480 | C00.0-C06.9, C09.0-C10.9, C11.0-C11.9, C12.9-C14.8, C30.0-C32.9 | A minor salivary gland carcinoma is coded at the site of the gland: XIf10 for the mouth and other head and neck mucosa, XIc for the nasopharynx. The sg_site option re-sites it. |

Every referral was checked in `ICCC-2017.sqlite` for the code at C07–C08 (topography 079–089).

## 10 Data gaps

1. **Paediatric occurrence of the salivary carcinomas still in the picker: microsecretory adenocarcinoma, hyalinizing clear cell carcinoma, basal cell adenocarcinoma, salivary duct carcinoma, epithelial-myoepithelial carcinoma, mucinous adenocarcinoma, sclerosing microcystic adenocarcinoma, sebaceous adenocarcinoma, lymphoepithelial carcinoma, primary squamous cell carcinoma, oncocytic carcinoma, poorly differentiated carcinoma, small cell and large cell neuroendocrine carcinoma, and NUT carcinoma at a salivary site.** Perez-de-Oliveira 2025 names only mucoepidermoid, acinic cell, secretory and adenoid cystic carcinoma, polymorphous adenocarcinoma and sialoblastoma among the malignant salivary gland tumours of children, and states that carcinoma ex pleomorphic adenoma has not been reported in them. Pfister 2022 names NUT carcinoma in children without a salivary site and none of the other entities listed here, so each stays in the picker. Candidate source: A paediatric series of salivary gland carcinoma that reports every histological type, such as the 203-case series of Quixabeira et al. that Perez-de-Oliveira 2025 cites; or WHO Classification of Paediatric Tumours, 5th edition (2022), salivary gland chapter.
2. **A paediatric case count for adenoid cystic carcinoma and polymorphous adenocarcinoma, and their order on the histology screen.** Perez-de-Oliveira 2025 says only that both are observed less frequently in paediatric patients than in adults, and its children's column in Table 1 lists mucoepidermoid, acinic cell and secretory carcinoma alone. The tree makes both options on that sentence and places adenoid cystic carcinoma before polymorphous adenocarcinoma without a paediatric source for the order. The controller decides whether one comparative sentence is enough for an option. Candidate source: The series of Quixabeira et al. or the earlier systematic review of 2,937 paediatric cases, both cited by Perez-de-Oliveira 2025.
3. **What the WHO 5th edition salivary chapter calls cystadenocarcinoma (8440/3) and papillary cystadenocarcinoma (8450/3) now.** Every ICD-O-3.2 /3 term on both codes is [obs]; the ICCR Table 1 omits them and names no successor, so a report using either term has no current entry. Candidate source: WHO Classification of Head and Neck Tumours, 5th edition, salivary gland chapter (entity list with ICD-O codes).
4. **The Milan System for Reporting Salivary Gland Cytopathology categories.** Both sources recommend the Milan system but print none of its categories, so the cytology screen's wording for suspicious, atypical and uncertain-malignant-potential results is not sourced. Candidate source: Faquin WC, Rossi ED, editors. The Milan System for Reporting Salivary Gland Cytopathology, 2nd edition (2023).
5. **Which gene results the WHO counts as entity-defining for basis of diagnosis 8.** Skalova 2022 Table 1 gives the prevalence of each alteration, not whether it is diagnostic, so the tree cannot say when a gene report raises the basis from 7 to 8. Candidate source: WHO Classification of Head and Neck Tumours, 5th edition, essential and desirable diagnostic criteria per salivary entity.
6. **Visser 2023 pages for registration without tissue.** The tissue-free entries follow the registrar's rule relayed by the controller; this part holds no copy of Visser 2023, so those entries carry no page cite. Candidate source: Visser O, et al. Front Oncol 2023;13:1250549 (held by the controller).
7. **A paediatric report of salivary gland carcinoma, not otherwise specified (8140/3) and carcinoma with no type named (8010/3).** Both are options on the histology screen as not-otherwise-specified fallbacks, and neither rests on a paediatric source. Perez-de-Oliveira 2025 does not report either in children. The controller decides whether a fallback needs one. Candidate source: None needed if the controller keeps fallbacks without paediatric evidence.
8. **Paediatric figures limited to ages 0 to 18.** Perez-de-Oliveira 2025 reviews patients aged 0 to 19 years, one year beyond the registrar's 0 to 18, and notes that some studies set the upper limit at 14. Its ranking of mucoepidermoid, acinic cell and secretory carcinoma pools those age limits. Candidate source: A paediatric salivary series that reports age in single years or with an upper limit of 18.

## Registrar questions

1. Sialoblastoma: Pfister 2022 (PDF p. 14) lists it as a malignant paediatric head and neck tumour, and Perez-de-Oliveira 2025 (PMC section 5) calls it a rare malignant neoplasm of the neonatal period and early childhood, but ICD-O-3.2 and the ICCR Table 1 print 8974/1, and ICCC-2017 holds 8974 only at /3 in XIIa4. The tree excludes 8974/1 and refers a sialoblastoma the report calls malignant to Group XII as 8974/3, a code ICD-O-3.2 does not print (Rule F). Is that right, or is every sialoblastoma registered at /3?

2. Myoepithelial carcinoma (8982/3) and carcinosarcoma (8980/3) are WHO salivary carcinomas that ICCC-2017 places in XIIa4. The tree refers them to Group XII. Confirm.

3. Intraductal carcinoma is 8500/2 in the WHO table. When the report states invasion, Rule F gives 8500/3 Infiltrating duct carcinoma, NOS, the same code as salivary duct carcinoma. Confirm.

4. The ICCR guide (PDF p. 7) calls intracapsular carcinoma ex pleomorphic adenoma 'in situ'. The tree records 8941/3 for every extent, as the WHO table does. Should an intracapsular carcinoma ex pleomorphic adenoma instead be treated as in situ and excluded?

5. Rule K and carcinoma ex pleomorphic adenoma: when the named malignant component is myoepithelial carcinoma, 8982 is higher than 8941 and would move the case to Group XII. The tree records 8941/3, treating the carcinoma ex pleomorphic adenoma code as covering the component. Confirm.

6. Mucinous adenocarcinoma, signet ring subtype: the WHO codes the entity 8480/3, but ICD-O-3.2 lists 'Mucinous carcinoma, signet ring cell type' under 8490/3 and Rule K favours 8490. Which code?

7. Oncocytic carcinoma and poorly differentiated carcinoma: the WHO places both in 'salivary carcinoma NOS and emerging entities' (8140/3), while ICD-O-3.2 prints the terms themselves at 8290/3 and 8020/3. The tree uses the ICD-O-3.2 term's code. Confirm.

8. A registration without tissue at C07-C08 records 8000/3, which ICCC-2017 places in XIIb, Group XII. Confirm the salivary tree records it and the output shows Group XII.

9. Rule B: should a tumour the report places 'around' or 'in the region of' the parotid be coded to the parotid when its type is a salivary gland carcinoma, or to head, face or neck (C76.0)?

## 11. Paediatric evidence added 8 October 2026

Source added: `XIf1-salivary-gland-paediatric__Perez-de-Oliveira-2025.txt` (Perez-de-Oliveira ME, et al. Med Oral Patol Oral Cir Bucal 2025; PMC12019652), read through the snippet tool only. It reviews epithelial salivary gland tumours in patients aged 0 to 19 years (PMC section 3). The quotes below are the cites in the JSON; each was checked against its PMC section.

| Entity | Before | After | Cite |
|---|---|---|---|
| Mucoepidermoid carcinoma 8430/3 | paediatric occurs; option | paediatric common; option, first on `sg_histology` (unchanged place) | PMC section 5: "Regarding histological subtypes, MEC is the most common malignant SGT."; PMC section 1: "Pleomorphic adenoma and mucoepidermoid carcinoma are the most frequently observed entities." |
| Acinic cell carcinoma 8550/3 | paediatric occurs; option | paediatric common; option, second on `sg_histology` (unchanged place) | PMC section 5: "Notably, AciCC and secretory carcinoma is the second and third most frequent malignant SGT" |
| Secretory carcinoma 8502/3 | paediatric not_reported; picker | paediatric common; option, third on `sg_histology`, removed from `sg_carcinoma_picker`. Recognition aid now adds that it resembles acinic cell carcinoma and that the report may name an ETV6 translocation | PMC section 5: the ranking quote above; "Secretory carcinoma was first described in 2010, mimicking AciCC."; "presence of ETV6 translocation and if positive, reclassified as secretory carcinoma" |
| Adenoid cystic carcinoma 8200/3 | paediatric not_reported; picker | paediatric occurs; option, fourth on `sg_histology`, removed from `sg_carcinoma_picker`. Recognition aid now names a MYB::NFIB fusion | PMC section 5: "polymorphous adenocarcinoma and ACC are less frequently observed in pediatric patients"; "CRTC1-MAML2 and MYB-NFIB fusion genes found in MEC and ACC, respectively" |
| Polymorphous adenocarcinoma 8525/3 | paediatric not_reported; picker | paediatric occurs; option, fifth on `sg_histology`, removed from `sg_carcinoma_picker` | PMC section 5: "polymorphous adenocarcinoma and ACC are less frequently observed in pediatric patients" |
| Carcinoma ex pleomorphic adenoma 8941/3 | paediatric not_reported; picker | unchanged; cite added that it is not reported in children | PMC section 5: "malignant transformation of pleomorphic adenoma (PA) has not been reported in pediatric patients" |
| Sialoblastoma 8974/1 | paediatric occurs; exclusion | unchanged; cite added on the entity and on the `sg_histology` Sialoblastoma option | PMC section 5: "rare malignant neoplasm primarily diagnosed in the neonatal period or early childhood" |
| Sialoblastoma that the report calls malignant 8974/3 | registrar | unchanged; cite added, and registrar question 1 records that this paper calls sialoblastoma malignant | PMC section 5: as above |
| Pleomorphic adenoma 8940/0 | paediatric occurs; exclusion | paediatric common; exclusion | PMC section 5: "Regarding histopathological diagnoses, PA is the most prevalent neoplasm." |
| Myoepithelioma 8982/0 | paediatric not_reported; exclusion | paediatric common; exclusion, moved to second on `sg_not_malignant` after pleomorphic adenoma | PMC section 5: "PA and MEC are the most prevalent. Benign: PA and myoepithelioma." (the children's column of Table 1) |
| `sg_histology` option "Another carcinoma the report names" | examples: adenoid cystic carcinoma, secretory carcinoma, salivary duct carcinoma | examples: salivary duct carcinoma, epithelial-myoepithelial carcinoma, carcinoma ex pleomorphic adenoma, because the first two are now on the screen | — |
| Data gaps | gap 1 listed every carcinoma but three; gap 2 asked which carcinoma is commonest in children | gap 1 lists the carcinomas still unreported in children; gap 2 is settled and replaced by the weak evidence for adenoid cystic carcinoma and polymorphous adenocarcinoma; gaps 7 (the not-otherwise-specified options) and 8 (the 0 to 19 age range) added | — |

Codes checked in ICD-O-3.2 on 8 October 2026: 8502/3 Secretory carcinoma, 8200/3 Adenoid cystic carcinoma and 8525/3 Polymorphous adenocarcinoma are current preferred terms. ICCC-2017 places all three in XIf1 at C07.9–C08.9. No code was added or changed.

Not changed, and why:

- Microsecretory adenocarcinoma, hyalinizing clear cell carcinoma, basal cell adenocarcinoma, salivary duct carcinoma, epithelial-myoepithelial carcinoma, mucinous, sclerosing microcystic and sebaceous adenocarcinoma, lymphoepithelial carcinoma, primary squamous cell carcinoma, oncocytic carcinoma, poorly differentiated carcinoma, the two neuroendocrine carcinomas and NUT carcinoma: the paper does not name them. They stay in the picker (data gap 1).
- Salivary gland carcinoma, not otherwise specified (8140/3) and carcinoma with no type named (8010/3): options without a paediatric source, and the paper does not report them. Left as they are for the controller (data gap 7).
- Warthin tumour 8561/0: the paper says it is not usually diagnosed in children and adolescents; it stays an exclusion with paediatric not_reported.
- The paper names no paediatric salivary entity that this part does not already list.
