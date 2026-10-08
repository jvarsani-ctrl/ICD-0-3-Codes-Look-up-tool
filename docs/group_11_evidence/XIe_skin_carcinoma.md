# Group 11 evidence — XIe skin carcinoma

Part `XIe_skin_carcinoma`, 8 October 2026. Sites: skin C44.0–C44.9, vulva NOS C51.9, penis NOS C60.9 and scrotum C63.2 (ICCC-2017 XIe topography 440–449, 519, 609, 632). Every ICD-O-3.2 term below was read from `icdo32.sqlite`; every subgroup from `ICCC-2017.sqlite`. The JSON twin is `XIe_skin_carcinoma.json`.

**Headline.** Two paediatric papers added on 8 October 2026 report basal cell carcinoma and squamous cell carcinoma in children (Huang 2019, a multicentre series of 124 patients under 20 years; Kaloga 2016, three children aged 7 and 8 years with xeroderma pigmentosum). Under the registrar's ruling of 8 October 2026 both are now options on the histology screen, basal cell carcinoma first. The WHO paediatric classification's skin chapter lists only benign epithelial tumours (angiokeratoma, epidermal naevi, pilomatricoma) and melanocytic tumours (Pfister 2022, PDF p. 14, table), and no held source reports Merkel cell carcinoma, an adnexal carcinoma or a named basal cell or squamous cell subtype in a child, so every other XIe carcinoma code stays in the skin carcinoma picker. Section 11 lists the changes; section 10 asks for the evidence still missing.

## 1 Sources

| File | Citation | WHO volume |
|---|---|---|
| `XId-XIe-skin-melanoma-and-skin-carcinoma__Goldman-Levy-2025.txt` | Goldman-Lévy G, Barnhill R, Bastian BC, et al. WHO classification of skin tumours: key updates in the fifth edition. Histopathology 2025;88(3):555-568. | WHO Classification of Tumours, Skin Tumours, 5th edition (Skin5), 2025 |
| `XIe-skin-carcinoma-Merkel__ICCR-Merkel-Cell-2nd.txt` | International Collaboration on Cancer Reporting. Merkel Cell Carcinoma Histopathology Reporting Guide, 2nd edition, version 2.0, January 2026. ISBN 978-1-922324-78-8. | WHO Classification of Skin Tumours, 5th edition, 2025 |
| `ALL-paediatric-occurrence__Pfister-2022.txt` | Pfister SM, Reyes-Múgica M, Chan JKC, et al. A Summary of the Inaugural WHO Classification of Pediatric Tumors: Transitioning from the Optical into the Molecular Era. Cancer Discov 2022;12(2):331-355. | WHO Classification of Paediatric Tumours, 5th edition, 2022 |
| `RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt` | World Health Organization. International Classification of Diseases for Oncology, 3rd edition, 1st revision (ICD-O-3.1), section 4, Coding guidelines, printed pp. 14-28. | not a tumour classification; the ICD-O coding manual |
| `XIe-skin-carcinoma-paediatric__Huang-2019.txt` | Huang JT, et al. Risk Factors and Outcomes of Nonmelanoma Skin Cancer in Children and Young Adults. J Pediatr 2019;211:152-158. doi:10.1016/j.jpeds.2019.04.017. PMC7916541. | not a WHO summary; paediatric evidence |
| `XIe-skin-carcinoma-paediatric__Kaloga-2016.txt` | Kaloga M, et al. Squamous Cell Carcinoma in African Children with Xeroderma Pigmentosum: Three Case Reports. Case Rep Dermatol 2016;8(3):311-318. doi:10.1159/000452438. PMC5126593. | not a WHO summary; paediatric evidence |

Goldman-Lévy 2025 covers keratinocytic and adnexal tumours and primary cutaneous NUT carcinoma; it prints no ICD-O codes and does not discuss basal cell carcinoma. ICCR Merkel 2026 prints the one WHO code it covers, 8247/3 (Table 1, PDF p. 7). The skin codes otherwise come from ICD-O-3.2 alone (Paper Screening 2026-10-08 §5 item 4).

The two paediatric papers are PubMed Central texts with sections, not pages; their cites give the PMC section number. Huang 2019 is a multicentre case-control study of patients under 20 years with basal cell or squamous cell carcinoma diagnosed 1995 to 2015; Table I's age bands show patients aged 0 to 5 years with each carcinoma, so the series covers ages 0 to 18. It counts in situ carcinoma and keratoacanthoma as squamous cell carcinoma (PMC section 4) and names no histological subtype. Kaloga 2016 reports three children with xeroderma pigmentosum and histologically confirmed squamous cell carcinoma. Neither paper prints ICD-O codes.

## 2 Entities

| Entity | Code | ICD-O-3.2 term (level) | Preferred term at this code | Paediatric | Decision | Source |
|---|---|---|---|---|---|---|
| Basal cell carcinoma | 8090/3 | Basal cell carcinoma, NOS (Preferred) | Basal cell carcinoma, NOS | occurs | option | ICD-O-3.1 manual, PDF p. 10 (printed p. 23), table; ICD-O-3.1 manual, PDF p. 10 (printed p. 23); Pfister 2022, PDF p. 14, table; Huang 2019, PMC section 6; Huang 2019, PMC section 7; Huang 2019, PMC section 12 (Table I) |
| Cutaneous squamous cell carcinoma (cSCC) | 8070/3 | Squamous cell carcinoma, NOS (Preferred) | Squamous cell carcinoma, NOS | occurs | option | Goldman-Lévy 2025, PDF p. 2; Pfister 2022, PDF p. 14, table; Kaloga 2016, PMC section 1; Kaloga 2016, PMC section 4; Huang 2019, PMC section 7; Huang 2019, PMC section 10; Huang 2019, PMC section 12 (Table I) |
| Carcinoma, type not named | 8010/3 | Carcinoma, NOS (Preferred) | Carcinoma, NOS | not_reported | option | Pfister 2022, PDF p. 14, table |
| Epithelioma, malignant (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8011/3 | Epithelioma, malignant (Preferred) | Epithelioma, malignant | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Large cell carcinoma, NOS (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8012/3 | Large cell carcinoma, NOS (Preferred) | Large cell carcinoma, NOS | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Large cell neuroendocrine carcinoma (ICD-O-3.2 term) | 8013/3 | Large cell neuroendocrine carcinoma (Preferred) | Large cell neuroendocrine carcinoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Large cell carcinoma with rhabdoid phenotype (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8014/3 | Large cell carcinoma with rhabdoid phenotype (Preferred) | Large cell carcinoma with rhabdoid phenotype | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Glassy cell carcinoma (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8015/3 | Glassy cell carcinoma (Preferred) | Glassy cell carcinoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Carcinoma, undifferentiated, NOS (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8020/3 | Carcinoma, undifferentiated, NOS (Preferred) | Carcinoma, undifferentiated, NOS | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Carcinoma, anaplastic, NOS (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8021/3 | Carcinoma, anaplastic, NOS (Preferred) | Carcinoma, anaplastic, NOS | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Pleomorphic carcinoma (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8022/3 | Pleomorphic carcinoma (Preferred) | Pleomorphic carcinoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| NUT (adnexal) carcinoma; primary cutaneous NUT carcinoma | 8023/3 | NUT carcinoma (Synonym) | Nuclear protein in testis (NUT)-associated carcinoma | not_reported | picker | Goldman-Lévy 2025, PDF p. 6, table; Goldman-Lévy 2025, PDF p. 5; Goldman-Lévy 2025, PDF p. 7; Pfister 2022, PDF p. 14, table |
| Giant cell and spindle cell carcinoma (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8030/3 | Giant cell and spindle cell carcinoma (Preferred) | Giant cell and spindle cell carcinoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Giant cell carcinoma (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8031/3 | Giant cell carcinoma (Preferred) | Giant cell carcinoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Spindle cell carcinoma, NOS (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8032/3 | Spindle cell carcinoma, NOS (Preferred) | Spindle cell carcinoma, NOS | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Pseudosarcomatous carcinoma (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8033/3 | Pseudosarcomatous carcinoma (Preferred) | Pseudosarcomatous carcinoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Polygonal cell carcinoma (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8034/3 | Polygonal cell carcinoma (Preferred) | Polygonal cell carcinoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Carcinoma with osteoclast-like giant cells (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8035/3 | Carcinoma with osteoclast-like giant cells (Preferred) | Carcinoma with osteoclast-like giant cells | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Small cell carcinoma, NOS (ICD-O-3.2 term) | 8041/3 | Small cell carcinoma, NOS (Preferred) | Small cell carcinoma, NOS | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Papillary carcinoma, NOS (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8050/3 | Papillary carcinoma, NOS (Preferred) | Papillary carcinoma, NOS | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Verrucous carcinoma, NOS (ICD-O-3.2 term; this part's sources do not describe it at skin) | 8051/3 | Verrucous carcinoma, NOS (Preferred) | Verrucous carcinoma, NOS | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Papillary squamous cell carcinoma (ICD-O-3.2 term; this part's sources do not describe it at skin) | 8052/3 | Papillary squamous cell carcinoma (Preferred) | Papillary squamous cell carcinoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Warty carcinoma (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8054/3 | Warty carcinoma (Preferred) | Warty carcinoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Squamous cell carcinoma, keratinizing (ICD-O-3.2 term) | 8071/3 | Squamous cell carcinoma, keratinizing, NOS (Preferred) | Squamous cell carcinoma, keratinizing, NOS | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Squamous cell carcinoma, large cell, nonkeratinizing, NOS (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8072/3 | Squamous cell carcinoma, large cell, nonkeratinizing, NOS (Preferred) | Squamous cell carcinoma, large cell, nonkeratinizing, NOS | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Squamous cell carcinoma, small cell, nonkeratinizing (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8073/3 | Squamous cell carcinoma, small cell, nonkeratinizing (Preferred) | Squamous cell carcinoma, small cell, nonkeratinizing | not_reported | picker | Pfister 2022, PDF p. 14, table |
| SCC with sarcomatoid differentiation | 8074/3 | Squamous cell carcinoma, sarcomatoid (Synonym) | Squamous cell carcinoma, spindle cell | not_reported | picker | Goldman-Lévy 2025, PDF p. 3 |
| Acantholytic SCC | 8075/3 | Squamous cell carcinoma, acantholytic (Synonym) | Squamous cell carcinoma, adenoid | not_reported | picker | Goldman-Lévy 2025, PDF p. 3 |
| Squamous cell carcinoma with horn formation (ICD-O-3.2 term; this part's sources do not describe it at skin) | 8078/3 | Squamous cell carcinoma with horn formation (Preferred) | Squamous cell carcinoma with horn formation | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Lymphoepithelial carcinoma | 8082/3 | Lymphoepithelial carcinoma (Preferred) | Lymphoepithelial carcinoma | not_reported | picker | Goldman-Lévy 2025, PDF p. 3 |
| Superficial basal cell carcinoma (ICD-O-3.2 term; this part's sources do not describe it) | 8091/3 | Superficial basal cell carcinoma (Preferred) | Superficial basal cell carcinoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Infiltrating basal cell carcinoma, NOS (ICD-O-3.2 term; this part's sources do not describe it) | 8092/3 | Infiltrating basal cell carcinoma, NOS (Preferred) | Infiltrating basal cell carcinoma, NOS | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Basal cell carcinoma, fibroepithelial (ICD-O-3.2 term; this part's sources do not describe it) | 8093/3 | Basal cell carcinoma, fibroepithelial (Preferred) | Basal cell carcinoma, fibroepithelial | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Mixed basal-squamous cell carcinoma | 8094/3 | Mixed basal-squamous cell carcinoma (Synonym) | Basosquamous carcinoma | not_reported | picker | ICD-O-3.1 manual, PDF p. 11 (printed p. 24); Pfister 2022, PDF p. 14, table |
| Metatypical carcinoma (ICD-O-3.2 term; this part's sources do not describe it) | 8095/3 | Metatypical carcinoma (Preferred) | Metatypical carcinoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Basal cell carcinoma, nodular (ICD-O-3.2 term; this part's sources do not describe it) | 8097/3 | Basal cell carcinoma, nodular (Preferred) | Basal cell carcinoma, nodular | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Adenoid basal carcinoma (ICD-O-3.2 term; this part's sources do not describe it) | 8098/3 | Adenoid basal carcinoma (Preferred) | Adenoid basal carcinoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Trichoblastic carcinoma/carcinosarcoma | 8100/3 | Trichoblastic carcinoma (Preferred) | Trichoblastic carcinoma | not_reported | picker | Goldman-Lévy 2025, PDF p. 6, table |
| Trichilemmocarcinoma (ICD-O-3.2 term; this part's sources do not describe it) | 8102/3 | Trichilemmocarcinoma (Preferred) | Trichilemmocarcinoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Pilomatrical carcinoma | 8110/3 | Pilomatrical carcinoma (Preferred) | Pilomatrical carcinoma | not_reported | picker | Goldman-Lévy 2025, PDF p. 6, table |
| Adenocarcinoma, NOS (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8140/3 | Adenocarcinoma, NOS (Preferred) | Adenocarcinoma, NOS | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Superficial spreading adenocarcinoma (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8143/3 | Superficial spreading adenocarcinoma (Preferred) | Superficial spreading adenocarcinoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Basal cell adenocarcinoma (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8147/3 | Basal cell adenocarcinoma (Preferred) | Basal cell adenocarcinoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Trabecular adenocarcinoma (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8190/3 | Trabecular adenocarcinoma (Preferred) | Trabecular adenocarcinoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Adenoid cystic carcinoma | 8200/3 | Adenoid cystic carcinoma (Preferred) | Adenoid cystic carcinoma | not_reported | picker | Goldman-Lévy 2025, PDF p. 6, table |
| Tubular adenocarcinoma (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8211/3 | Tubular adenocarcinoma (Preferred) | Tubular adenocarcinoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Neuroendocrine tumor, NOS (ICD-O-3.2 term) | 8240/3 | Neuroendocrine tumor, NOS (Preferred) | Neuroendocrine tumor, NOS | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Neuroendocrine carcinoma, NOS (ICD-O-3.2 term) | 8246/3 | Neuroendocrine carcinoma, NOS (Preferred) | Neuroendocrine carcinoma, NOS | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Merkel cell carcinoma | 8247/3 | Merkel cell carcinoma (Preferred) | Merkel cell carcinoma | not_reported | picker | ICCR Merkel 2026, PDF p. 7, table; ICCR Merkel 2026, PDF p. 7 |
| Papillary adenocarcinoma, NOS (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8260/3 | Papillary adenocarcinoma, NOS (Preferred) | Papillary adenocarcinoma, NOS | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Adenocarcinoma in tubulovillous adenoma (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8263/3 | Adenocarcinoma in tubulovillous adenoma (Preferred) | Adenocarcinoma in tubulovillous adenoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Clear cell adenocarcinoma, NOS (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8310/3 | Clear cell adenocarcinoma, NOS (Preferred) | Clear cell adenocarcinoma, NOS | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Granular cell carcinoma (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8320/3 | Granular cell carcinoma (Preferred) | Granular cell carcinoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Mixed cell adenocarcinoma (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8323/3 | Mixed cell adenocarcinoma (Preferred) | Mixed cell adenocarcinoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Adnexal carcinoma (ICD-O-3.2 term; this part's sources do not describe it) | 8390/3 | Adnexal carcinoma (Synonym) | Adnexal adenocarcinoma, NOS | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Sweat gland adenocarcinoma (ICD-O-3.2 term; this part's sources do not describe it) | 8400/3 | Sweat gland adenocarcinoma (Preferred) | Sweat gland adenocarcinoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Apocrine adenocarcinoma (ICD-O-3.2 term; this part's sources do not describe it) | 8401/3 | Apocrine adenocarcinoma (Preferred) | Apocrine adenocarcinoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Hidradenocarcinoma | 8402/3 | Hidradenocarcinoma (Preferred) | Hidradenocarcinoma | not_reported | picker | Goldman-Lévy 2025, PDF p. 6, table |
| Malignant tumours evolving in cylindroma and spiradenoma | 8403/3 | Malignant neoplasm arising from pre-existing spiradenoma (Related) | Malignant eccrine spiradenoma | not_reported | picker | Goldman-Lévy 2025, PDF p. 6, table |
| Syringocystadenocarcinoma papilliferum (ICD-O-3.2 term; this part's sources do not describe it) | 8406/3 | Syringocystadenocarcinoma papilliferum (Preferred) | Syringocystadenocarcinoma papilliferum | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Microcystic adnexal carcinoma | 8407/3 | Microcystic adnexal carcinoma (Preferred) | Microcystic adnexal carcinoma | not_reported | picker | Goldman-Lévy 2025, PDF p. 6, table |
| Digital papillary adenocarcinoma | 8408/3 | Digital papillary adenocarcinoma (Preferred) | Digital papillary adenocarcinoma | not_reported | picker | Goldman-Lévy 2025, PDF p. 6, table |
| Porocarcinoma | 8409/3 | Porocarcinoma, NOS (Preferred) | Porocarcinoma, NOS | not_reported | picker | Goldman-Lévy 2025, PDF p. 6, table; Goldman-Lévy 2025, PDF p. 5 |
| Sebaceous carcinoma | 8410/3 | Sebaceous carcinoma (Preferred) | Sebaceous carcinoma | not_reported | picker | Goldman-Lévy 2025, PDF p. 6, table |
| Eccrine adenocarcinoma (ICD-O-3.2 term; this part's sources do not describe it) | 8413/3 | Eccrine adenocarcinoma (Preferred) | Eccrine adenocarcinoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Ceruminous adenocarcinoma (ICD-O-3.2 term; this part's sources do not describe it) | 8420/3 | Ceruminous adenocarcinoma (Preferred) | Ceruminous adenocarcinoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Mucoepidermoid carcinoma (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8430/3 | Mucoepidermoid carcinoma (Preferred) | Mucoepidermoid carcinoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Mucinous carcinoma (ICD-O-3.2 term; this part's sources do not describe it) | 8480/3 | Mucinous carcinoma (Synonym) | Mucinous adenocarcinoma | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Signet-ring cell/histiocytoid carcinoma | 8490/3 | Signet ring cell/histiocytoid carcinoma (Related) | Signet ring cell carcinoma | not_reported | picker | Goldman-Lévy 2025, PDF p. 6, table |
| Secretory carcinoma | 8502/3 | Secretory carcinoma (Preferred) | Secretory carcinoma | not_reported | picker | Goldman-Lévy 2025, PDF p. 6, table |
| Endocrine mucin-producing sweat gland carcinoma (ICD-O-3.2 term; this part's sources do not describe it) | 8509/3 | Endocrine mucin-producing sweat gland carcinoma (Related) | Solid papillary carcinoma with invasion | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Paget disease, extramammary (ICD-O-3.2 term; this part's sources do not describe it) | 8542/3 | Paget disease, extramammary (Preferred) | Paget disease, extramammary | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Squamoid eccrine ductal carcinoma (formerly cutaneous adenosquamous carcinoma) | 8560/3 | Squamoid eccrine ductal carcinoma (Related) | Adenosquamous carcinoma | not_reported | picker | Goldman-Lévy 2025, PDF p. 3 |
| Adenocarcinoma with squamous metaplasia (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8570/3 | Adenocarcinoma with squamous metaplasia (Preferred) | Adenocarcinoma with squamous metaplasia | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Adenocarcinoma with cartilaginous and osseous metaplasia (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8571/3 | Adenocarcinoma with cartilaginous and osseous metaplasia (Preferred) | Adenocarcinoma with cartilaginous and osseous metaplasia | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Adenocarcinoma with spindle cell metaplasia (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8572/3 | Adenocarcinoma with spindle cell metaplasia (Preferred) | Adenocarcinoma with spindle cell metaplasia | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Adenocarcinoma with apocrine metaplasia (ICD-O-3.2 term; generic carcinoma in the ICCC-2017 XIe range) | 8573/3 | Adenocarcinoma with apocrine metaplasia (Preferred) | Adenocarcinoma with apocrine metaplasia | not_reported | picker | Pfister 2022, PDF p. 14, table |
| Keratoacanthoma | 8071/3 | Keratoacanthoma (Related) | Squamous cell carcinoma, keratinizing, NOS | occurs | registrar | Goldman-Lévy 2025, PDF p. 2; Goldman-Lévy 2025, PDF p. 3; Huang 2019, PMC section 6; Huang 2019, PMC section 4 |
| Pseudovascular SCC | 8074/3 | Pseudovascular squamous cell carcinoma (Related) | Squamous cell carcinoma, spindle cell | not_reported | registrar | Goldman-Lévy 2025, PDF p. 3 |
| Cribriform carcinoma (of skin, the term the WHO 5th edition retires) | 8201/3 | Cribriform carcinoma, NOS (Preferred) | Cribriform carcinoma, NOS | not_reported | registrar | Goldman-Lévy 2025, PDF p. 5 |
| Actinic keratosis | 8070/0 | Actinic keratosis (Preferred) | Actinic keratosis | occurs | exclusion | Huang 2019, PMC section 8 |
| Squamous cell carcinoma in situ | 8070/2 | Squamous cell carcinoma in situ, NOS (Preferred) | Squamous cell carcinoma in situ, NOS | occurs | exclusion | Huang 2019, PMC section 6 |
| Differentiated vulvar or penile intraepithelial neoplasia | 8071/2 | Differentiated intraepithelial neoplasia (Preferred) | Differentiated intraepithelial neoplasia | not_reported | exclusion | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Vulvar intraepithelial neoplasia, high grade (VIN III) | 8077/2 | VIN III (Synonym) | Squamous intraepithelial neoplasia, high grade | not_reported | exclusion | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Queyrat erythroplasia | 8080/2 | Queyrat erythroplasia (Preferred) | Queyrat erythroplasia | not_reported | exclusion | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Bowen disease | 8081/2 | Bowen disease (Preferred) | Bowen disease | not_reported | exclusion | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Trichoblastoma (including trichoepithelioma) | 8100/0 | Trichoblastoma (Related) | Trichoepithelioma | not_reported | exclusion | Goldman-Lévy 2025, PDF p. 6, table |
| Trichilemmoma | 8102/0 | Trichilemmoma (Preferred) | Trichilemmoma | not_reported | exclusion | Goldman-Lévy 2025, PDF p. 6, table |
| Proliferating trichilemmal tumour | 8103/1 | Proliferating trichilemmal tumor (Synonym) | Proliferating trichilemmal cyst | not_reported | exclusion | Goldman-Lévy 2025, PDF p. 6, table |
| Pilar tumour | 8103/0 | Pilar tumor (Preferred) | Pilar tumor | not_reported | exclusion | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Pilomatricoma | 8110/0 | Pilomatricoma, NOS (Preferred) | Pilomatricoma, NOS | occurs | exclusion | Pfister 2022, PDF p. 14, table; Goldman-Lévy 2025, PDF p. 6, table |
| Cylindroma | 8200/0 | Cylindroma of skin (Related) | Eccrine dermal cylindroma | not_reported | exclusion | Goldman-Lévy 2025, PDF p. 6, table |
| Hidradenoma | 8402/0 | Hidradenoma, NOS (Preferred) | Hidradenoma, NOS | not_reported | exclusion | Goldman-Lévy 2025, PDF p. 6, table |
| Spiradenoma | 8403/0 | Spiradenoma, NOS (Preferred) | Spiradenoma, NOS | not_reported | exclusion | Goldman-Lévy 2025, PDF p. 6, table |
| Syringocystadenoma papilliferum | 8406/0 | Syringocystadenoma papilliferum (Preferred) | Syringocystadenoma papilliferum | not_reported | exclusion | Goldman-Lévy 2025, PDF p. 6, table |
| Poroma | 8409/0 | Poroma, NOS (Preferred) | Poroma, NOS | not_reported | exclusion | Goldman-Lévy 2025, PDF p. 6, table |
| Porocarcinoma in situ | 8409/2 | Porocarcinoma in situ (Preferred) | Porocarcinoma in situ | not_reported | exclusion | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Sebaceous adenoma and sebaceoma | 8410/0 | Sebaceoma (Preferred) | Sebaceoma | not_reported | exclusion | Goldman-Lévy 2025, PDF p. 6, table |
| Cutaneous mixed tumour | 8940/0 | Chondroid syringoma, NOS (Related) | Pleomorphic adenoma | not_reported | exclusion | Goldman-Lévy 2025, PDF p. 6, table |
| Myoepithelioma | 8982/0 | Myoepithelioma, NOS (Preferred) | Myoepithelioma, NOS | not_reported | exclusion | Goldman-Lévy 2025, PDF p. 6, table |
| Angiokeratoma | 9141/0 | Angiokeratoma (Preferred) | Angiokeratoma | occurs | exclusion | Pfister 2022, PDF p. 14, table |
| Squamoproliferative tumour of uncertain malignant potential | no code (/1) | — (none) | — | not_reported | exclusion | Goldman-Lévy 2025, PDF p. 3; ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |
| Merkel cell carcinoma in situ | no code (/2) | — (none) | — | not_reported | exclusion | ICCR Merkel 2026, PDF p. 10; ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |
| Nevus sebaceus (epidermal naevus) | no code (/0) | — (none) | — | occurs | exclusion | Pfister 2022, PDF p. 14, table; Pfister 2022, PDF p. 11; Goldman-Lévy 2025, PDF p. 6, table; Huang 2019, PMC section 12 (Table I) |
| Cutaneous cribriform tumour | no code (/0) | — (none) | — | not_reported | exclusion | Goldman-Lévy 2025, PDF p. 5 |
| Neoplasm, malignant, on clinical or imaging evidence only | 8000/3 | Neoplasm, malignant (Preferred) | Neoplasm, malignant | not_reported | refer → Group 12 | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Paget disease, mammary | 8540/3 | Paget disease, mammary (Preferred) | Paget disease, mammary | not_reported | refer | ICD-O-3.1 manual, PDF p. 10 (printed p. 23) |
| Melanoma | 8720/3 | Malignant melanoma, NOS (Preferred) | Malignant melanoma, NOS | occurs | refer | Goldman-Lévy 2025, PDF p. 3; Pfister 2022, PDF p. 14, table |
| Malignant mixed tumour of skin (malignant chondroid syringoma) | 8940/3 | Malignant chondroid syringoma (Related) | Mixed tumor, malignant, NOS | not_reported | refer → Group 12 | Goldman-Lévy 2025, PDF p. 6, table |
| Myoepithelial carcinoma of skin | 8982/3 | Myoepithelial carcinoma (Preferred) | Myoepithelial carcinoma | not_reported | refer → Group 12 | Goldman-Lévy 2025, PDF p. 6, table |
| Kaposi sarcoma and other soft-tissue tumours of skin | 9140/3 | Kaposi sarcoma (Preferred) | Kaposi sarcoma | not_reported | refer → Group 9 | Goldman-Lévy 2025, PDF p. 9 |
| Primary cutaneous lymphoma (for example mycosis fungoides) | 9700/3 | Mycosis fungoides (Preferred) | Mycosis fungoides | not_reported | refer → Group 2 | Goldman-Lévy 2025, PDF p. 7; ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |
| Langerhans cell histiocytosis in skin | 9751/3 | Langerhans cell histiocytosis, disseminated (Preferred) | Langerhans cell histiocytosis, disseminated | not_reported | refer → Group 2 | Goldman-Lévy 2025, PDF p. 7 |
| Leukaemia in skin or myeloid sarcoma | 9930/3 | Myeloid sarcoma (Preferred) | Myeloid sarcoma | not_reported | refer → Group 1 | ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |
| Metastasis to skin (deposit of a tumour that began elsewhere) | no code (/6) | — (none) | — | not_reported | refer | Goldman-Lévy 2025, PDF p. 10; ICCR Merkel 2026, PDF p. 8 |

Notes on the decisions:

- **Pseudovascular SCC** (8074/3): ICD-O-3.2 files Pseudovascular squamous cell carcinoma as a related term of 8074/3 (spindle cell). The WHO 5th edition says it is no longer a subtype and is not a recommended term for acantholytic squamous cell carcinoma (8075/3). The registrar rules which code a report using this term records; until then it is not a search term.
- **Keratoacanthoma** (8071/3): ICD-O-3.2 files Keratoacanthoma as a related term of 8071/3, a malignant code, and prints no 8071/1. The WHO 5th edition considers keratoacanthoma likely a separate entity from squamous cell carcinoma, and the two cannot always be told apart. The registrar rules whether a report of keratoacanthoma is registered as 8071/3.
- **Squamoproliferative tumour of uncertain malignant potential** (no code (/1)): The WHO 5th edition uses this term when keratoacanthoma and squamous cell carcinoma cannot be told apart. ICD-O-3.2 prints no term for it; a stated uncertain behaviour is /1 (Rule F), which Group XI does not declare. No code is recorded.
- **Merkel cell carcinoma in situ** (no code (/2)): ICCR describes Merkel cell carcinoma confined to the epidermis or adnexal epithelium. In situ is behaviour /2 (Rule F), which Group XI does not declare; ICD-O-3.2 prints no 8247/2 term, so the screen names no code.
- **Basal cell carcinoma** (8090/3) and **Cutaneous squamous cell carcinoma** (8070/3): options on `sk_histology` since 8 October 2026, on the paediatric reports of Huang 2019 and Kaloga 2016 (section 11). Basal cell carcinoma comes first because Huang 2019 counts 95 patients with it against 40 with squamous cell carcinoma. Both labels say "with no subtype named", so a named subtype (nodular, superficial, keratinizing) still reaches its own code through the picker. Both codes stay in the picker as well; section 10 asks the controller whether they should.
- **Carcinoma, type not named** (8010/3): The NOS fallback of the histology screen (Decision Tree master §3D), not a paediatric entity. It is offered as an answer so a report naming no type is coded, and it is left out of the picker.
- **Nevus sebaceus (epidermal naevus)** (no code (/0)): Listed in the WHO paediatric skin chapter as a hamartoma-type epidermal naevus. ICD-O-3.2 prints no term for it; it is not a registrable neoplasm.
- **Cutaneous cribriform tumour** (no code (/0)): The WHO 5th edition downgrades cribriform carcinoma of skin to an indolent cribriform tumour. ICD-O-3.2 prints no term for the tumour; it is not registered.
- **Cribriform carcinoma (of skin, the term the WHO 5th edition retires)** (8201/3): ICD-O-3.2 codes Cribriform carcinoma, NOS 8201/3, and no ICCC-2017 range holds 8201 at skin. The WHO 5th edition says the skin tumour has no reported recurrence or metastasis and renames it cribriform tumour. The registrar rules whether an older skin report of cribriform carcinoma records 8201/3 or is excluded.
- **Melanoma** (8720/3): Melanoma at any site is coded from the Group XI melanoma tree (XId at every site); the skin histology screen hands over to it.
- **Primary cutaneous lymphoma (for example mycosis fungoides)** (9700/3): ICCC-2017 places 9700 in IIb3 at every site. Rule D codes an extranodal lymphoma to its site of origin, here the skin.
- **Langerhans cell histiocytosis in skin** (9751/3): ICCC-2017 places 9751 in IId at every site; the Group II tree decides its behaviour (9751/1 or 9751/3).
- **Leukaemia in skin or myeloid sarcoma** (9930/3): ICCC-2017 places 9930 in Ib at every site. Rule E records every leukaemia at C42.1 except myeloid sarcoma, which keeps the skin site.
- **Kaposi sarcoma and other soft-tissue tumours of skin** (9140/3): ICCC-2017 places 9140 in IXc and dermatofibrosarcoma 8832/3 in IXd5 at every site. The WHO skin volume carries a soft tissue chapter; the Group IX tree codes these tumours and their behaviour.
- **Malignant mixed tumour of skin (malignant chondroid syringoma)** (8940/3): ICD-O-3.2 prints C44 beside Malignant chondroid syringoma, but ICCC-2017 places 8940/3 in XIIa4 at every site, a different group: a conflict under standing rule 3. It is referred to Group XII.
- **Myoepithelial carcinoma of skin** (8982/3): ICCC-2017 places 8982/3 in XIIa4 at every site, a different group. It is referred to Group XII.
- **Neoplasm, malignant, on clinical or imaging evidence only** (8000/3): ICCC-2017 places 8000/3 and 8001/3 at C44, C51.9, C60.9 and C63.2 in XIIb, not Group XI. A skin case registered without tissue or type is referred to Group XII, as Group X referred 8000/3 in the brain to Group III.
- **Paget disease, mammary** (8540/3): ICCC-2017's XIe range holds 8540 at skin, but ICD-O-3.2 prints C50 beside it (Rule H): the nipple is breast. It is not offered at skin; a skin Paget disease is extramammary, 8542/3.
- **Metastasis to skin (deposit of a tumour that began elsewhere)** (no code (/6)): The WHO 5th edition adds a chapter on metastases to skin. A deposit is coded at its primary: the referral asks the primary's site (recapture_site).

## 3 The pathway

The skin instance of the general carcinoma tree. `melanoma_tree` stands for the entry node of the Group XI melanoma tree, which the controller substitutes.

### `sk_document_inventory` (document_inventory)

**Question:** What is in the file for this skin tumour?

**Hint:** A pathology report on a curettage, shave, punch or excision biopsy counts as histology. An immunohistochemistry or gene report on its own does not stand in for a histology report.

| Answer | Outcome | Records | Reason shown | Source |
|---|---|---|---|---|
| A referral letter or clinical note only — no imaging report, no tissue | go → `sk_clinical` | basis 1 |  | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| An imaging report only — no tissue | go → `sk_imaging` | basis 2 |  | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Cytology only — a scraping or fine-needle aspirate; no tissue | go → `sk_cytology` | basis 5 |  | ICCR Merkel 2026, PDF p. 4 |
| A histology report — biopsy or excision, with or without immunohistochemistry or gene reports | go → `sk_site` | basis 7 |  | ICCR Merkel 2026, PDF p. 1 |

### `sk_clinical` (clinical_alias)

**Question:** What does the referral letter or clinical note say?

| Answer | Outcome | Records | Reason shown | Source |
|---|---|---|---|---|
| The note names melanoma of the skin | go → `melanoma_tree` | basis 1 | Melanoma of the skin is coded from the melanoma tree, which registers it on clinical information (8720/3, basis 1). | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| The note states another malignant skin tumour as the diagnosis, or as probable | refer → Group 12 | 8000/3, basis 1 | A diagnosis resting on clinical information alone is registered with the unspecified code. ICCC-3 places Neoplasm, malignant (8000/3) at a skin site in Group XII, other and unspecified malignant tumours, not in Group XI. Code the case from the Group XII tree. | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| The note says only possible or suspected | not_registrable |  | Cancer is only possible on this evidence. A case that is only possibly cancer is not registered without pathology. | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| An imaging report is in the file after all | go → `sk_imaging` |  |  | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |

### `sk_imaging` (morphology_only)

**Question:** No tissue is in the file. What does the imaging report conclude?

| Answer | Outcome | Records | Reason shown | Source |
|---|---|---|---|---|
| Imaging shows a malignant tumour, at least probable | refer → Group 12 | 8000/3, basis 2 | A diagnosis resting on imaging alone is registered with the unspecified code. ICCC-3 places Neoplasm, malignant (8000/3) at a skin site in Group XII, other and unspecified malignant tumours, not in Group XI. Code the case from the Group XII tree. | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Imaging calls it possible only, or describes a benign lesion | not_registrable |  | Cancer is only possible on this evidence. A case that is only possibly cancer is not registered without pathology. | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| A histology report is in the file after all | go → `sk_site` |  |  | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |

### `sk_cytology` (morphology_only)

**Question:** What does the cytology report conclude?

**Hint:** Cytology does not give a histological subtype. A histology report, when one arrives, confirms the type.

| Answer | Outcome | Records | Reason shown | Source |
|---|---|---|---|---|
| Cytology names squamous cell carcinoma | code | 8070/3, basis 5 | Recorded as Squamous cell carcinoma, NOS (8070/3) at basis of diagnosis 5. | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Cytology names basal cell carcinoma | code | 8090/3, basis 5 | Recorded as Basal cell carcinoma, NOS (8090/3) at basis of diagnosis 5. | ICD-O-3.1 manual, PDF p. 10 (printed p. 23), table |
| Cytology names Merkel cell carcinoma | code | 8247/3, basis 5 | Recorded as Merkel cell carcinoma (8247/3) at basis of diagnosis 5. | ICCR Merkel 2026, PDF p. 4; ICCR Merkel 2026, PDF p. 7, table |
| Cytology names a carcinoma without naming its type | code | 8010/3, basis 5 | Recorded as Carcinoma, NOS (8010/3) at basis of diagnosis 5. | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Cytology names melanoma | go → `melanoma_tree` |  | Melanoma is coded from the melanoma tree. | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Cytology names a lymphoma | refer → Group 2 |  | A lymphoma in the skin is coded from the Group II (lymphomas) tree at its skin site. | ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |
| Malignant cells are present, with no tumour type named | refer → Group 12 | 8001/3, basis 5 | Cytology establishes malignant cells but no tumour type. ICCC-3 places Tumor cells, malignant (8001/3) at a skin site in Group XII, not in Group XI. Code the case from the Group XII tree. | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| No malignant cells, scant material, or a non-diagnostic report — and an imaging report is in the file | go → `sk_imaging` |  |  | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| No malignant cells, scant material, or a non-diagnostic report — and no imaging report is in the file | go → `sk_clinical` |  |  | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |

### `sk_site` (site_resolution)

**Question:** Which skin site does the report name?

**Hint:** A carcinoma reported at a body region with no tissue named (arm, leg, back, chin, forehead) is skin of that region. A site written with peri- or para- is skin of that region when the tumour arises in skin. When the report names no site, a basal cell carcinoma, Merkel cell carcinoma or adnexal carcinoma is skin, site not stated. If the tumour covers two skin regions and the report does not say where it began, choose overlapping.

| Answer | Outcome | Records | Reason shown | Source |
|---|---|---|---|---|
| Skin of lip | go → `sk_histology` | C44.0 |  | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Eyelid | go → `sk_histology` | C44.1 |  | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| External ear | go → `sk_histology` | C44.2 |  | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Skin of the face — chin, forehead, nose, cheek, temple or face not further stated | go → `sk_histology` | C44.3 |  | ICD-O-3.1 manual, PDF p. 1 (printed p. 14); ICD-O-3.1 manual, PDF p. 4 (printed p. 17) |
| Skin of the scalp or neck | go → `sk_histology` | C44.4 |  | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Skin of the trunk — back, chest, abdomen, buttock, groin or perianal skin | go → `sk_histology` | C44.5 |  | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Skin of the arm, hand or shoulder | go → `sk_histology` | C44.6 |  | ICD-O-3.1 manual, PDF p. 1 (printed p. 14); ICD-O-3.1 manual, PDF p. 4 (printed p. 17) |
| Skin of the leg, foot or hip | go → `sk_histology` | C44.7 |  | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| More than one skin region, and the report does not say where it began | go → `sk_histology` | C44.8 |  | ICD-O-3.1 manual, PDF p. 5 (printed p. 18) |
| Skin, site not stated | go → `sk_histology` | C44.9 |  | ICD-O-3.1 manual, PDF p. 10 (printed p. 23) |
| Vulva, part not stated | go → `sk_histology` | C51.9 |  | ICD-O-3.1 manual, PDF p. 10 (printed p. 23), table |
| Penis, part not stated | go → `sk_histology` | C60.9 |  | ICD-O-3.1 manual, PDF p. 10 (printed p. 23), table |
| Scrotum | go → `sk_histology` | C63.2 |  | ICD-O-3.1 manual, PDF p. 10 (printed p. 23), table |

### `sk_histology` (histology_subclassification)

**Question:** What does the histology report call the tumour?

**Hint:** Use the report's own term. If the report states that the tumour is benign, in situ or of uncertain malignant potential, choose that answer, even for a tumour type that is usually malignant.

**NOS fallback:** 8010/3 Carcinoma, NOS.

| Answer | Outcome | Records | Reason shown | Source |
|---|---|---|---|---|
| Basal cell carcinoma, with no subtype named | code | 8090/3, basis 7 | Recorded as Basal cell carcinoma, NOS (8090/3). | Huang 2019, PMC section 6; Huang 2019, PMC section 7; Huang 2019, PMC section 12 (Table I) |
| Squamous cell carcinoma, with no subtype named — well, moderately or poorly differentiated, or no grade stated | code | 8070/3, basis 7 | Recorded as Squamous cell carcinoma, NOS (8070/3). | Kaloga 2016, PMC section 1; Kaloga 2016, PMC section 4; Huang 2019, PMC section 7; Huang 2019, PMC section 10; Kaloga 2016, PMC section 9 |
| Melanoma | go → `melanoma_tree` |  | Melanoma is coded from the melanoma tree. | Goldman-Lévy 2025, PDF p. 3 |
| Keratoacanthoma | code (held for the registrar) | 8071/3, basis 7 | Recorded as Squamous cell carcinoma, keratinizing, NOS (8071/3). ICD-O-3.2 gives Keratoacanthoma as a related term of this code. | Goldman-Lévy 2025, PDF p. 3; Huang 2019, PMC section 6; Huang 2019, PMC section 4 |
| A named subtype of basal cell or squamous cell carcinoma (nodular, superficial, keratinizing and others), or another named carcinoma — Merkel cell, adnexal (sweat gland, hair follicle or sebaceous) or another | go → `sk_carcinoma_other` |  |  | Goldman-Lévy 2025, PDF p. 6, table; ICCR Merkel 2026, PDF p. 7, table |
| Carcinoma, with no type named | code | 8010/3, basis 7 | Recorded as Carcinoma, NOS (8010/3). | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Benign, in situ, or of uncertain malignant potential — the report says so | go → `sk_not_malignant` |  |  | ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |
| Lymphoma or histiocytosis in the skin — for example mycosis fungoides or Langerhans cell histiocytosis | refer → Group 2 |  | Lymphomas and histiocytoses are coded from the Group II tree. A lymphoma that begins in the skin is recorded at its skin site. | Goldman-Lévy 2025, PDF p. 7; ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |
| Leukaemia in the skin, or myeloid sarcoma | refer → Group 1 |  | Leukaemias are coded from the Group I tree. A leukaemia is recorded at bone marrow (C42.1); a myeloid sarcoma keeps its skin site. | ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |
| Sarcoma or another soft-tissue tumour — for example Kaposi sarcoma or dermatofibrosarcoma protuberans | refer → Group 9 |  | Soft-tissue tumours of the skin are coded from the Group IX (soft-tissue sarcomas) tree. | Goldman-Lévy 2025, PDF p. 9 |
| Malignant mixed tumour (malignant chondroid syringoma) or myoepithelial carcinoma | refer → Group 12 |  | ICCC-3 places Mixed tumor, malignant, NOS (8940/3) and Myoepithelial carcinoma (8982/3) in Group XII at every site. Code the case from the Group XII tree. | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| A deposit (metastasis) of a tumour that began elsewhere | refer, recapture site |  | A deposit in the skin is coded at the tumour's primary site. The next screen asks where the tumour began. | Goldman-Lévy 2025, PDF p. 10 |

Option order: the entities reported in children come first, commonest first (basal cell carcinoma, squamous cell carcinoma, melanoma, keratoacanthoma), then the picker and the NOS answer, then the exclusion and referral answers. The squamous cell carcinoma option carries a recognition aid: "Reports describe atypical squamous cells with hyperkeratosis, and tumour cells infiltrating the dermis." (Kaloga 2016, PMC section 9, figure legend.)

### `sk_not_malignant` (histology_subclassification)

**Question:** Which benign, in situ or uncertain tumour does the report name?

**Hint:** These tumours are benign, in situ or of uncertain behaviour. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report.

| Answer | Outcome | Records | Reason shown | Source |
|---|---|---|---|---|
| Squamoproliferative tumour of uncertain malignant potential | exclude |  | The report states an uncertain behaviour (/1). The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | Goldman-Lévy 2025, PDF p. 3; ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |
| Merkel cell carcinoma in situ | exclude |  | This tumour is in situ, not invasive (behaviour /2). The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | ICCR Merkel 2026, PDF p. 10; ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |
| Pilomatricoma | exclude | 8110/0 | Pilomatricoma, NOS (8110/0) is benign. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | Pfister 2022, PDF p. 14, table; Goldman-Lévy 2025, PDF p. 6, table |
| Angiokeratoma | exclude | 9141/0 | Angiokeratoma (9141/0) is benign. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | Pfister 2022, PDF p. 14, table |
| Actinic keratosis | exclude | 8070/0 | Actinic keratosis (8070/0) is benign. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | Huang 2019, PMC section 8 |
| Proliferating trichilemmal tumour | exclude | 8103/1 | Proliferating trichilemmal cyst (8103/1) is of uncertain behaviour. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | Goldman-Lévy 2025, PDF p. 6, table |
| Pilar tumour | exclude | 8103/0 | Pilar tumor (8103/0) is benign. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Trichoblastoma (including trichoepithelioma) | exclude | 8100/0 | Trichoepithelioma (8100/0) is benign. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | Goldman-Lévy 2025, PDF p. 6, table |
| Trichilemmoma | exclude | 8102/0 | Trichilemmoma (8102/0) is benign. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | Goldman-Lévy 2025, PDF p. 6, table |
| Poroma | exclude | 8409/0 | Poroma, NOS (8409/0) is benign. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | Goldman-Lévy 2025, PDF p. 6, table |
| Hidradenoma | exclude | 8402/0 | Hidradenoma, NOS (8402/0) is benign. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | Goldman-Lévy 2025, PDF p. 6, table |
| Spiradenoma | exclude | 8403/0 | Spiradenoma, NOS (8403/0) is benign. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | Goldman-Lévy 2025, PDF p. 6, table |
| Cylindroma | exclude | 8200/0 | Eccrine dermal cylindroma (8200/0) is benign. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | Goldman-Lévy 2025, PDF p. 6, table |
| Sebaceous adenoma and sebaceoma | exclude | 8410/0 | Sebaceoma (8410/0) is benign. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | Goldman-Lévy 2025, PDF p. 6, table |
| Syringocystadenoma papilliferum | exclude | 8406/0 | Syringocystadenoma papilliferum (8406/0) is benign. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | Goldman-Lévy 2025, PDF p. 6, table |
| Cutaneous mixed tumour | exclude | 8940/0 | Pleomorphic adenoma (8940/0) is benign. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | Goldman-Lévy 2025, PDF p. 6, table |
| Myoepithelioma | exclude | 8982/0 | Myoepithelioma, NOS (8982/0) is benign. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | Goldman-Lévy 2025, PDF p. 6, table |
| Bowen disease | exclude | 8081/2 | Bowen disease (8081/2) is in situ, not invasive. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Squamous cell carcinoma in situ | exclude | 8070/2 | Squamous cell carcinoma in situ, NOS (8070/2) is in situ, not invasive. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | Huang 2019, PMC section 6 |
| Porocarcinoma in situ | exclude | 8409/2 | Porocarcinoma in situ (8409/2) is in situ, not invasive. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Vulvar intraepithelial neoplasia, high grade (VIN III) | exclude | 8077/2 | Squamous intraepithelial neoplasia, high grade (8077/2) is in situ, not invasive. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Differentiated vulvar or penile intraepithelial neoplasia | exclude | 8071/2 | Differentiated intraepithelial neoplasia (8071/2) is in situ, not invasive. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Queyrat erythroplasia | exclude | 8080/2 | Queyrat erythroplasia (8080/2) is in situ, not invasive. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Nevus sebaceus (epidermal naevus) | exclude |  | This lesion is benign, and ICD-O-3.2 prints no malignant code for it. The case is not registered from this report. | Pfister 2022, PDF p. 14, table; Pfister 2022, PDF p. 11; Goldman-Lévy 2025, PDF p. 6, table; Huang 2019, PMC section 12 (Table I) |
| Cutaneous cribriform tumour | exclude |  | This lesion is benign, and ICD-O-3.2 prints no malignant code for it. The case is not registered from this report. | Goldman-Lévy 2025, PDF p. 5 |
| Another tumour the report calls benign, in situ or of uncertain malignant potential | exclude |  | A behaviour the pathologist states is recorded as stated. The registry records malignant tumours (behaviour /3) only, so the case is not registered from this report. | ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |

### `sk_carcinoma_other` (histology_subclassification)

**Question:** Which carcinoma does the report name?

**Hint:** Type part of the name in the box and the matching options appear. The other names ICD-O-3.2 gives a tumour find it too. If a compound name is not found, search for its parts in the other order. When one tumour shows two types and no single option names both, choose the higher code number: a Merkel cell carcinoma combined with squamous cell carcinoma is recorded as Merkel cell carcinoma (8247/3).

**NOS fallback:** 8010/3 Carcinoma, NOS.

The skin carcinoma picker: 76 options, every ICCC-2017 XIe code that ICD-O-3.2 prints at /3, in code order, less 8010 (offered on `sk_histology`) and 8540 (Paget disease, mammary, a breast code by Rule H), plus 8490, 8502 and 8509, which no ICCC range holds at skin (standing rule 3). Each option records its code at basis 7; its search terms are the ICD-O-3.2 synonyms and related terms that are not `[obs]` and not tied to another organ. Keratoacanthoma (8071) and Pseudovascular squamous cell carcinoma (8074) are left out of the search terms until the registrar rules. Reached from cytology, the picker must record basis 5; the cytology screen therefore offers its own family codes instead. Since 8 October 2026, 8090/3 and 8070/3 are also options on `sk_histology` (paediatric reports, section 11); they stay in this list so that their ICD-O-3.2 synonyms stay searchable, and section 10 asks the controller whether they should.

| Code | Label | Search terms | Recognition aid |
|---|---|---|---|
| 8011/3 | Epithelioma, malignant | Epithelioma, NOS |  |
| 8012/3 | Large cell carcinoma, NOS |  |  |
| 8013/3 | Large cell neuroendocrine carcinoma | Combined large cell neuroendocrine carcinoma |  |
| 8014/3 | Large cell carcinoma with rhabdoid phenotype |  |  |
| 8015/3 | Glassy cell carcinoma |  |  |
| 8020/3 | Carcinoma, undifferentiated, NOS | Carcinoma, poorly differentiated, NOS; Anaplastic undifferentiated carcinoma; Dedifferentiated carcinoma |  |
| 8021/3 | Carcinoma, anaplastic, NOS |  |  |
| 8022/3 | Pleomorphic carcinoma |  |  |
| 8023/3 | Nuclear protein in testis (NUT)-associated carcinoma | NUT carcinoma; NUT midline carcinoma | Reports describe a primitive epithelial tumour of uniform cells with one prominent nucleolus, often with small ducts and abrupt keratinisation, and a NUT gene fusion. (Goldman-Lévy 2025, PDF p. 5; Goldman-Lévy 2025, PDF p. 7) |
| 8030/3 | Giant cell and spindle cell carcinoma |  |  |
| 8031/3 | Giant cell carcinoma |  |  |
| 8032/3 | Spindle cell carcinoma, NOS |  |  |
| 8033/3 | Pseudosarcomatous carcinoma | Sarcomatoid carcinoma |  |
| 8034/3 | Polygonal cell carcinoma |  |  |
| 8035/3 | Carcinoma with osteoclast-like giant cells | Squamous carcinoma with osteoclast-like giant cells; Undifferentiated carcinoma with osteoclast-like giant cells |  |
| 8041/3 | Small cell carcinoma, NOS | Small cell neuroendocrine carcinoma; Reserve cell carcinoma; Round cell carcinoma |  |
| 8050/3 | Papillary carcinoma, NOS |  |  |
| 8051/3 | Verrucous carcinoma, NOS | Verrucous epidermoid carcinoma; Verrucous squamous cell carcinoma |  |
| 8052/3 | Papillary squamous cell carcinoma | Papillary epidermoid carcinoma |  |
| 8054/3 | Warty carcinoma | Warty-basaloid carcinoma; Condylomatous carcinoma |  |
| 8070/3 | Squamous cell carcinoma, NOS | Squamous cell carcinoma, usual type; Epidermoid carcinoma, NOS; Squamous carcinoma; Squamous cell epithelioma |  |
| 8071/3 | Squamous cell carcinoma, keratinizing, NOS | Epidermoid carcinoma, keratinizing; Squamous cell carcinoma, large cell, keratinizing |  |
| 8072/3 | Squamous cell carcinoma, large cell, nonkeratinizing, NOS | Epidermoid carcinoma, large cell, nonkeratinizing; Squamous cell carcinoma, nonkeratinizing, NOS |  |
| 8073/3 | Squamous cell carcinoma, small cell, nonkeratinizing | Epidermoid carcinoma, small cell, nonkeratinizing |  |
| 8074/3 | Squamous cell carcinoma, spindle cell | Epidermoid carcinoma, spindle cell; Squamous cell carcinoma, sarcomatoid |  |
| 8075/3 | Squamous cell carcinoma, adenoid | Squamous cell carcinoma, acantholytic; Squamous cell carcinoma, pseudoglandular |  |
| 8078/3 | Squamous cell carcinoma with horn formation |  |  |
| 8082/3 | Lymphoepithelial carcinoma | Lymphoepithelioma; Lymphoepithelioma-like carcinoma |  |
| 8090/3 | Basal cell carcinoma, NOS | Pigmented basal cell carcinoma; Basal cell carcinoma with adnexal differentiation; Basal cell epithelioma; Rodent ulcer |  |
| 8091/3 | Superficial basal cell carcinoma | Multifocal superficial basal cell carcinoma; Multicentric basal cell carcinoma |  |
| 8092/3 | Infiltrating basal cell carcinoma, NOS | Infiltrating basal cell carcinoma, non-sclerosing; Infiltrating basal cell carcinoma, sclerosing; Basal cell carcinoma, sarcomatoid; Basal cell carcinoma, desmoplastic type; Basal cell carcinoma, morpheic |  |
| 8093/3 | Basal cell carcinoma, fibroepithelial | Fibroepithelioma, NOS; Fibroepithelioma of Pinkus type; Fibroepithelial basal cell carcinoma, Pinkus type; Pinkus tumor |  |
| 8094/3 | Basosquamous carcinoma | Mixed basal-squamous cell carcinoma |  |
| 8095/3 | Metatypical carcinoma |  |  |
| 8097/3 | Basal cell carcinoma, nodular | Basal cell carcinoma, micronodular |  |
| 8098/3 | Adenoid basal carcinoma |  |  |
| 8100/3 | Trichoblastic carcinoma | Trichoblastic carcinosarcoma |  |
| 8102/3 | Trichilemmocarcinoma | Trichilemmal carcinoma |  |
| 8110/3 | Pilomatrical carcinoma | Pilomatrix carcinoma; Matrical carcinoma; Pilomatricoma, malignant; Pilomatrixoma, malignant |  |
| 8140/3 | Adenocarcinoma, NOS | Adenocarcinoma, usual type |  |
| 8143/3 | Superficial spreading adenocarcinoma |  |  |
| 8147/3 | Basal cell adenocarcinoma |  |  |
| 8190/3 | Trabecular adenocarcinoma | Trabecular carcinoma |  |
| 8200/3 | Adenoid cystic carcinoma | Adenocystic carcinoma |  |
| 8211/3 | Tubular adenocarcinoma | Tubular carcinoma |  |
| 8240/3 | Neuroendocrine tumor, NOS | Neuroendocrine tumor, grade 1; Carcinoid tumor, NOS; Carcinoid, NOS; Neuroendocrine carcinoma, low grade; Neuroendocrine carcinoma, well differentiated; Typical carcinoid |  |
| 8246/3 | Neuroendocrine carcinoma, NOS | Poorly differentiated neuroendocrine neoplasm |  |
| 8247/3 | Merkel cell carcinoma | Merkel cell tumor; Primary cutaneous neuroendocrine carcinoma | Reports describe a tumour with a neuroendocrine appearance; one that also shows squamous cell carcinoma or another line of differentiation is called combined Merkel cell carcinoma. (ICCR Merkel 2026, PDF p. 7) |
| 8260/3 | Papillary adenocarcinoma, NOS |  |  |
| 8263/3 | Adenocarcinoma in tubulovillous adenoma | Villoglandular carcinoma; Papillotubular adenocarcinoma; Tubulopapillary adenocarcinoma |  |
| 8310/3 | Clear cell adenocarcinoma, NOS | Clear cell adenocarcinoma, mesonephroid; Clear cell carcinoma, NOS |  |
| 8320/3 | Granular cell carcinoma | Granular cell adenocarcinoma |  |
| 8323/3 | Mixed cell adenocarcinoma |  |  |
| 8390/3 | Adnexal adenocarcinoma, NOS | Skin appendage carcinoma; Adnexal carcinoma |  |
| 8400/3 | Sweat gland adenocarcinoma | Sweat gland carcinoma; Sweat gland tumor, malignant |  |
| 8401/3 | Apocrine adenocarcinoma | Apocrine carcinoma |  |
| 8402/3 | Hidradenocarcinoma | Nodular hidradenoma, malignant |  |
| 8403/3 | Malignant eccrine spiradenoma | Malignant neoplasm arising from pre-existing spiradenoma; Malignant neoplasm arising from pre-existing cylindroma; Malignant neoplasm arising from pre-existing spiradenocylindroma |  |
| 8406/3 | Syringocystadenocarcinoma papilliferum |  |  |
| 8407/3 | Microcystic adnexal carcinoma | Sclerosing sweat duct carcinoma; Syringomatous carcinoma |  |
| 8408/3 | Digital papillary adenocarcinoma | Eccrine papillary adenocarcinoma |  |
| 8409/3 | Porocarcinoma, NOS | Eccrine poroma, malignant |  |
| 8410/3 | Sebaceous carcinoma | Sebaceous adenocarcinoma |  |
| 8413/3 | Eccrine adenocarcinoma |  |  |
| 8420/3 | Ceruminous adenocarcinoma | Ceruminous carcinoma |  |
| 8430/3 | Mucoepidermoid carcinoma |  |  |
| 8480/3 | Mucinous adenocarcinoma | Colloid adenocarcinoma; Colloid carcinoma; Mucinous carcinoma; Mucoid adenocarcinoma; Mucoid carcinoma |  |
| 8490/3 | Signet ring cell/histiocytoid carcinoma | Signet ring cell carcinoma; Signet ring cell adenocarcinoma; Mucinous carcinoma, signet ring cell type |  |
| 8502/3 | Secretory carcinoma |  |  |
| 8509/3 | Endocrine mucin-producing sweat gland carcinoma |  |  |
| 8542/3 | Paget disease, extramammary |  |  |
| 8560/3 | Squamoid eccrine ductal carcinoma (adenosquamous carcinoma of skin) | Squamoid eccrine ductal carcinoma; Mixed adenocarcinoma and epidermoid carcinoma; Mixed adenocarcinoma and squamous cell carcinoma; Adenosquamous carcinoma | Older reports may call this tumour adenosquamous carcinoma of skin; the WHO skin classification now names it squamoid eccrine ductal carcinoma. (Goldman-Lévy 2025, PDF p. 3) |
| 8570/3 | Adenocarcinoma with squamous metaplasia | Adenoacanthoma |  |
| 8571/3 | Adenocarcinoma with cartilaginous and osseous metaplasia | Adenocarcinoma with cartilaginous metaplasia; Adenocarcinoma with chondroid differentiation; Adenocarcinoma with osseous metaplasia |  |
| 8572/3 | Adenocarcinoma with spindle cell metaplasia | Fibromatosis-like metaplastic carcinoma |  |
| 8573/3 | Adenocarcinoma with apocrine metaplasia | Carcinoma with apocrine metaplasia |  |

## 4 Immunohistochemistry rules

None. No held source gives a marker set that decides between two skin codes:

- Merkel cell carcinoma: ICCR says no single immunohistochemical reagent recognises every case, and the panel depends on the differential; CK20 is used because most tumours express it (ICCR Merkel 2026, PDF p. 9). Merkel cell polyomavirus immunohistochemistry is recommended for prognosis (PDF p. 6), not for the code.
- Keratoacanthoma against squamous cell carcinoma: p53, Ki67 and p16 may permit the distinction, but reliable distinction is not always possible (Goldman-Lévy 2025, PDF p. 3). ICD-O-3.2 files keratoacanthoma under 8071/3, the keratinizing squamous cell carcinoma code, so the markers would not change the code in any case. A checklist that costs the clerk attention without changing the emitted code has no benefit (standing rule 16).
- Primary cutaneous NUT carcinoma is defined by a BRD3 or NSD3 fusion with a NUT-family partner (Goldman-Lévy 2025, PDF p. 7). That is a gene report, which on its own does not stand in for a histology report.

## 5 Registration without tissue

| Evidence on file | Code | Basis | Note | Source |
|---|---|---|---|---|
| Referral letter or clinical note stating a malignant skin tumour other than melanoma | 8000/3 | 1 | Visser 2023 rule 5, from the controller's brief (not one of this part's files). ICCC-2017 places 8000/3 at C44, C51.9, C60.9 and C63.2 in XIIb: referred to Group XII. | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Imaging report showing a malignant skin tumour, at least probable | 8000/3 | 2 | As above: XIIb, referred to Group XII. | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Clinical information naming melanoma of the skin | 8720/3 | 1 | Visser 2023 Table 3, from the controller's brief; coded in the melanoma tree, not here. | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |
| Cytology naming Merkel cell carcinoma | 8247/3 | 5 | ICCR reports the tumour diagnosis on cytology specimens. | ICCR Merkel 2026, PDF p. 4 |
| Cytology naming squamous cell carcinoma, basal cell carcinoma, or carcinoma with no type | 8070 / 8090 / 8010/3 | 5 | Family-level codes only; cytology gives no subtype. | no paper: icdo32.sqlite, ICCC-2017.sqlite or the controller brief |

No Visser 2023 Table 4 marker applies to a skin carcinoma, so the evidence gate carries no imaging-with-marker tier for skin.

## 6 Laboratory tests

None. No held source gives a serum or urine test a diagnostic role for a skin carcinoma. The skin tree needs no laboratory screen.

## 7 Rules A to K

| Rule | Applies | How it reaches the clerk | Source |
|---|---|---|---|
| A | yes | sk_site hint and option labels: a carcinoma at a body region with no tissue named is skin of that region (arm C44.6); chin and forehead are skin of face, C44.3. | ICD-O-3.1 manual, PDF p. 1 (printed p. 14); ICD-O-3.1 manual, PDF p. 4 (printed p. 17) |
| B | yes | sk_site hint: a site written with peri- or para- is skin of that region when the tumour type arises in skin. | ICD-O-3.1 manual, PDF p. 1 (printed p. 14) |
| C | yes | sk_site option 'More than one skin region, and the report does not say where it began' records C44.8. | ICD-O-3.1 manual, PDF p. 5 (printed p. 18) |
| D | yes | Referral only: the lymphoma option's reason says a lymphoma that begins in the skin is recorded at its skin site in the Group II tree. | ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |
| E | yes | Referral only: the leukaemia option's reason says a leukaemia is recorded at C42.1 and a myeloid sarcoma keeps its skin site. | ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |
| F | yes | sk_histology hint and the option 'Benign, in situ, or of uncertain malignant potential', leading to sk_not_malignant; its last option covers any stated non-malignant behaviour. | ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |
| G | no | No skin screen offers two grades, and the sixth digit is not built. A squamous cell carcinoma's stated differentiation does not change the code. | ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |
| H | yes | sk_site hint and the 'Skin, site not stated' option: with no site named, basal cell carcinoma, Merkel cell carcinoma and the adnexal carcinomas are skin (ICD-O-3.2 prints C44 beside them). Table 23 names vulva, penis, scrotum and prostate as other primary sites of basal cell carcinoma, which the site options for C51.9, C60.9 and C63.2 carry. 8540/3 Paget disease, mammary is not offered at skin because its printed site is C50. | ICD-O-3.1 manual, PDF p. 10 (printed p. 23); ICD-O-3.1 manual, PDF p. 10 (printed p. 23), table |
| J | yes | sk_carcinoma_other hint: search the parts of a compound name in the other order. ICD-O-3.2 synonyms such as Mixed basal-squamous cell carcinoma are search terms on 8094/3. | ICD-O-3.1 manual, PDF p. 11 (printed p. 24) |
| K | yes | sk_carcinoma_other hint: when no single option names both types, choose the higher code; combined Merkel cell carcinoma with squamous cell carcinoma is 8247/3. | ICD-O-3.1 manual, PDF p. 11 (printed p. 24); ICCR Merkel 2026, PDF p. 7 |

There is no Rule I.

## 8 Code currency

| Code | Behaviour | Finding | What the tree does |
|---|---|---|---|
| 8408 | 3 | ICD-O-3.2 moved Aggressive digital papillary adenoma from 8408/1 to 8408/3 Digital papillary adenocarcinoma and marks the old term [obs] (currency check §3). REDCap labels 8408 Eccrine papillary adenocarcinoma, a synonym (§4). | Picker label Digital papillary adenocarcinoma; the [obs] term is not a search term. REDCap relabel goes on the REDCap-side list. |
| 8103 | 1 | ICD-O-3.2 moved 8103 from /0 to /1 (Proliferating trichilemmal cyst; synonym Proliferating trichilemmal tumor); 8103/0 is Pilar tumor; no /3 term (currency check §3, §5). REDCap offers 8103 Pilar tumor under XIe. | Exclusion on sk_not_malignant. REDCap retire item for the REDCap-side list. |
| 8071 | 3 | ICD-O-3.2 lists Keratoacanthoma as a related term of 8071/3 and prints no 8071/1. The WHO 5th edition treats keratoacanthoma as likely distinct from squamous cell carcinoma. | Held for the registrar. Keratoacanthoma is not a search term on 8071/3 until the ruling, so the 'Also called' row does not show it. |
| 8074 | 3 | ICD-O-3.2 lists Pseudovascular squamous cell carcinoma as a related term of 8074/3; the WHO 5th edition says it is not a subtype and not a term for acantholytic squamous cell carcinoma (8075/3). | Held for the registrar; not a search term. |
| 8560 | 3 | ICD-O-3.2 lists Squamoid eccrine ductal carcinoma (C44) as a related term of 8560/3 Adenosquamous carcinoma; the WHO 5th edition moves cutaneous adenosquamous carcinoma into squamoid eccrine ductal carcinoma. | Same code; picker label names both. |
| 8200 | 3 | ICD-O-3.2 marks Cylindroma, NOS [obs] as a synonym of 8200/3 Adenoid cystic carcinoma; Cylindroma of skin is 8200/0. | The [obs] synonym is not a search term; cylindroma is an exclusion at 8200/0. |
| 8023 | 3 | New in ICD-O-3.2; REDCap's XIe list does not offer it (currency check §6). | Picker entry; REDCap-side list. |
| 8509 | 3 | ICD-O-3.2 gives Endocrine mucin-producing sweat gland carcinoma (C44) as a related term of 8509/3, whose preferred term is Solid papillary carcinoma with invasion (C50); REDCap does not offer it (currency check §6). No ICCC-2017 range holds 8509 at skin. | Picker entry labelled with the skin term; the reason names the preferred term. REDCap-side list. |
| 8490 | 3 | No ICCC-2017 range holds 8490 at C44; REDCap's XIe list does not offer it. ICD-O-3.2 prints the WHO name Signet ring cell/histiocytoid carcinoma as a related term. | Picker entry (standing rule 3). REDCap-side list. |
| 8502 | 3 | No ICCC-2017 range holds 8502 at C44; REDCap's XIe list does not offer it. | Picker entry (standing rule 3). REDCap-side list. |
| 8091 8100 8110 8240 8390 8402 8406 8407 8409 8410 8033 | 3 | REDCap's XIe labels are not the ICD-O-3.2 preferred terms: 8091 Multifocal superficial basal cell carcinoma (preferred Superficial basal cell carcinoma); 8100 Trichoepithelioma, the /0 term (preferred Trichoblastic carcinoma); 8110 Pilomatrix carcinoma (Pilomatrical carcinoma); 8240 Carcinoid tumor, NOS (Neuroendocrine tumor, NOS); 8390 Skin appendage carcinoma (Adnexal adenocarcinoma, NOS); 8402 Nodular hidradenoma, malignant (Hidradenocarcinoma); 8406 Papillary syringadenoma, the /0 synonym (Syringocystadenocarcinoma papilliferum); 8407 Sclerosing sweat duct carcinoma (Microcystic adnexal carcinoma); 8409 Eccrine poroma, malignant (Porocarcinoma, NOS); 8410 Sebaceous adenocarcinoma (Sebaceous carcinoma); 8033 Sarcomatoid carcinoma (Pseudosarcomatous carcinoma) (currency check §4). | Every picker option carries the ICD-O-3.2 preferred term. The 8100 and 8406 labels name a benign tumour on a malignant code and lead the REDCap-side list. |
| 8081 8096 8101 8391 8392 8404 8405 8040 8053 8060 | 0/1/2 | REDCap's XIe list offers codes that ICD-O-3.2 prints at /0, /1 or /2 only (currency check §5). | Not built. Bowen disease 8081/2 is an exclusion on sk_not_malignant. |
| 8540 | 3 | REDCap's XIe list and the ICCC-2017 XIe range hold Paget disease, mammary; ICD-O-3.2 prints C50 beside it. | Not offered at skin (Rule H); extramammary Paget disease 8542/3 is the skin code. |
| 8090 | 1 | 8090/1 Basal cell tumor is [obs], the only /1 term. | Not built; no screen names it. |

## 9 Conflicts with other groups

| Group | Codes | Sites | Issue |
|---|---|---|---|
| 12 | 8940, 8982 | C44.0-C44.9 | ICD-O-3.2 prints C44 beside Malignant chondroid syringoma (8940/3), yet ICCC-2017 places 8940/3 and Myoepithelial carcinoma 8982/3 in XIIa4 at every site. Both are referred to Group XII. |
| 12 | 8000, 8001 | C44.0-C44.9, C51.9, C60.9, C63.2 | A skin case with no tissue, or cytology with malignant cells and no type, records 8000/3 or 8001/3, which ICCC-2017 places in XIIb at these sites. The tree refers it to Group XII. |
| 9 | 9140, 8832 | C44.0-C44.9 | Kaposi sarcoma (IXc) and dermatofibrosarcoma (IXd5) arise in skin; the Group IX tree codes them and decides the behaviour of 8832 (8832/1 is Dermatofibrosarcoma protuberans, NOS; 8832/3 is the fibrosarcomatous form). |
| 2 | 9700, 9709, 9751 | C44.0-C44.9 | Cutaneous lymphomas (IIb3) and Langerhans cell histiocytosis (IId) are coded from the Group II tree at the skin site (Rule D). |
| 1 | 9930 | C44.0-C44.9 | Leukaemia in the skin records C42.1 (Rule E); myeloid sarcoma (Ib) keeps the skin site. |
| 11 | 8720 | C44.0-C44.9 | Melanoma is XId at every site; the skin histology screen and the clinical and cytology screens hand over to the melanoma tree. |
| 11 | 8070, 8071, 8051, 8085, 8086, 8077, 8090, 8542 | C51.9, C60.9, C63.2 | ICCC-2017 makes C51.9 vulva NOS, C60.9 penis NOS and C63.2 scrotum XIe, while C51.0-C51.8 and C60.0-C60.8 are XIf10. If the vulva and penis carcinoma part serves these sites, the subgroup computed from the site gives XIe at C51.9, C60.9 and C63.2 whichever tree is used; the skin tree offers the three sites only so a case is never stranded. 8085 and 8086 (HPV positive and negative squamous cell carcinoma) sit in no ICCC range at these sites and come from that part's sources, not this one. |
| 11 | 8540 | C50.0 | Paget disease, mammary sits in the ICCC XIe range at skin but is a breast code by its printed site; it belongs to the breast tree. |

## 10 Data gaps

1. **Paediatric occurrence (ages 0 to 18) of Merkel cell carcinoma, the adnexal carcinomas (pilomatrical, porocarcinoma, sebaceous, microcystic adnexal, digital papillary) and the named subtypes of basal cell and squamous cell carcinoma.** Huang 2019 and Kaloga 2016 make basal cell carcinoma (8090/3) and squamous cell carcinoma (8070/3) options. Neither names Merkel cell carcinoma, an adnexal carcinoma or a basal cell or squamous cell subtype, so those codes stay in the picker. Pfister 2022 lists Gorlin syndrome and xeroderma pigmentosum as paediatric predisposition syndromes (PDF p. 19). Candidate source: WHO Classification of Paediatric Tumours, 5th edition, skin chapter; a population study of skin carcinoma under 20 years (for example SEER) that reports histological type; case series of pilomatrical carcinoma, sebaceous carcinoma, porocarcinoma and Merkel cell carcinoma in children.
2. **The WHO 5th-edition skin entity list with its ICD-O codes: basal cell carcinoma subtypes, cutaneous squamous cell carcinoma subtypes, the adnexal carcinomas, cutaneous cribriform tumour and primary cutaneous NUT carcinoma.** Goldman-Lévy prints no codes and does not discuss basal cell carcinoma at all; the skin codes come from icdo32.sqlite alone (Paper Screening §5 item 4). The code the WHO gives keratoacanthoma and cribriform tumour would settle two registrar questions. Candidate source: WHO Classification of Tumours: Skin Tumours, 5th edition (IARC), ICD-O coding list; an ICCR invasive non-melanoma skin carcinoma dataset aligned to it, if one exists.
3. **Recognition text for basal cell carcinoma in report vocabulary.** Squamous cell carcinoma now carries a recognition aid from Kaloga 2016 (PMC section 9, figure legend). Basal cell carcinoma, the commoner carcinoma in Huang 2019, carries none: neither new paper describes its histology. Candidate source: WHO Skin Tumours 5th edition chapter text for basal cell carcinoma.
4. **A paediatric frequency ranking of skin carcinomas.** Neither new paper calls basal cell or squamous cell carcinoma the common type in children. Huang 2019 selected patients with these two carcinomas only, and Kaloga 2016 reports three children with xeroderma pigmentosum. Both entities are therefore occurs, not common; the option order (basal cell before squamous cell) follows Huang's counts of 95 and 40 patients. Candidate source: a population-based registry study of skin carcinoma under 20 years.
5. **Whether the skin carcinoma picker keeps 8090/3 and 8070/3 now that both are options on `sk_histology`.** Both stay in `sk_carcinoma_other`, so their ICD-O-3.2 synonyms (Rodent ulcer, Basal cell epithelioma, Epidermoid carcinoma, NOS, Squamous carcinoma) stay searchable. Carcinoma, NOS (8010/3) is the precedent for an option left out of the picker. The controller decides; no source is needed.
6. **Paediatric evidence for Carcinoma, NOS (8010/3), which stays an option on `sk_histology`.** It is an option as the screen's NOS fallback, not because a source reports it in children, and neither new paper reports it. It is left as it is; the controller decides. No source is needed if the controller keeps the NOS fallback as an option on every histology screen.

### Questions only the registrar can answer

1. Keratoacanthoma: ICD-O-3.2 files Keratoacanthoma as a related term of 8071/3 (Squamous cell carcinoma, keratinizing, NOS), a malignant code, and prints no 8071/1. The WHO 5th-edition skin volume treats keratoacanthoma as likely a separate entity from squamous cell carcinoma, and says the two cannot always be told apart (Goldman-Lévy 2025, PDF p. 3). Is a report of keratoacanthoma registered as 8071/3, or excluded unless the pathologist calls it malignant? The draft holds the option on sk_histology and keeps the term out of the 8071 search terms until you rule.
2. Paediatric occurrence: answered by the registrar's ruling of 8 October 2026. Basal cell carcinoma and cutaneous squamous cell carcinoma, reported in children by Huang 2019 and Kaloga 2016, are now options on `sk_histology` (section 11). No held source reports Merkel cell carcinoma or pilomatrical carcinoma in a child, so both stay in the picker until one does (section 10, gap 1).
3. Pseudovascular squamous cell carcinoma: ICD-O-3.2 files it under 8074/3 (spindle cell); the WHO 5th edition says it is not a subtype and not a term for acantholytic squamous cell carcinoma (8075/3). Which code does a report using the term record?
4. Cribriform carcinoma of skin: ICD-O-3.2 codes Cribriform carcinoma, NOS 8201/3 (no ICCC range holds 8201 at skin); the WHO 5th edition downgrades the skin tumour to cutaneous cribriform tumour, which ICD-O-3.2 does not name. Is an older skin report of cribriform carcinoma recorded as 8201/3 or excluded?
5. Squamoproliferative tumour of uncertain malignant potential: ICD-O-3.2 prints no term; Rule F makes the stated behaviour /1. Confirm it is excluded with no code.
6. Merkel cell carcinoma found only in a lymph node with no skin primary (ICCR T0, 'No evidence of primary tumour'): is the site skin, site not stated (C44.9) by Rule H, or unknown primary (C80.9)?
7. A skin case on clinical or imaging evidence only records 8000/3, and cytology with malignant cells and no type records 8001/3; ICCC-2017 places both in XIIb at skin. Confirm the referral to Group XII, as Group X referred 8000/3 in the brain to Group III.
8. Malignant chondroid syringoma (8940/3, which ICD-O-3.2 site-associates with skin) and myoepithelial carcinoma of skin (8982/3) are ICCC XIIa4 at every site. Confirm the referral to Group XII.
9. C51.9 vulva NOS, C60.9 penis NOS and C63.2 scrotum are XIe by ICCC-2017. Which tree serves them: the skin tree (which offers them in this draft), the vulva and penis carcinoma tree, or both, with the subgroup computed from the site?

## 11. Paediatric evidence added 8 October 2026

The controller fetched two open-access paediatric papers from PubMed Central: Huang 2019 (`XIe-skin-carcinoma-paediatric__Huang-2019.txt`) and Kaloga 2016 (`XIe-skin-carcinoma-paediatric__Kaloga-2016.txt`). Each cite below gives the PMC section number; the JSON carries it in `pdf_page`. Every code was read again from `icdo32.sqlite`, and ICCC-2017 places 8070, 8071 and 8090 in XIe at C44, C51.9, C60.9 and C63.2 at behaviour /3.

| Entity | Before | After | Cite |
|---|---|---|---|
| Basal cell carcinoma (8090/3) | paediatric not_reported; decision picker | paediatric occurs; decision option, first on `sk_histology` as "Basal cell carcinoma, with no subtype named", basis 7, reason "Recorded as Basal cell carcinoma, NOS (8090/3)." | Huang 2019, PMC section 6: "Forty cases had at least 1 SCC, 95 patients had at least 1 BCC"; PMC section 6: "There were a total of 856 skin cancers, including 716 BCC"; PMC section 7: "12.2 years (range 0.9–19.8) in patients with BCC"; PMC section 12 (Table I): "Age at diagnosis 0–5 y 6 (15) 12 (13)" |
| Cutaneous squamous cell carcinoma (8070/3) | paediatric not_reported; decision picker | paediatric occurs; decision option, second on `sk_histology` as "Squamous cell carcinoma, with no subtype named — well, moderately or poorly differentiated, or no grade stated", basis 7, reason "Recorded as Squamous cell carcinoma, NOS (8070/3).", with a recognition aid | Kaloga 2016, PMC section 1: "Histology confirmed squamous cell carcinoma in all 3 cases"; PMC section 1: "the average age was 7.6 years"; PMC section 4: "A 7-year-old phototype VI boy"; PMC section 4: "A pathological examination of a fragment of the tumor confirmed squamous cell carcinoma"; Huang 2019, PMC section 7: "14.1 years (range 2.2–19.8) in patients with SCC"; PMC section 10: "Of those with invasive SCC (n = 29)"; PMC section 12 (Table I): "Age at diagnosis 0–5 y 6 (15) 12 (13)" |
| Squamous cell carcinoma, recognition aid on the `sk_histology` option | none | "Reports describe atypical squamous cells with hyperkeratosis, and tumour cells infiltrating the dermis." | Kaloga 2016, PMC section 9 (figure legend): "Hyperplasia of the squamous epithelium formed from atypical cells with hyperkeratosis" |
| Keratoacanthoma (8071/3) | paediatric not_reported; decision registrar | paediatric occurs; decision registrar, unchanged. Huang counts keratoacanthoma as squamous cell carcinoma; that grouping is the paper's, not a coding ruling. The option stays fourth on `sk_histology` and gains the two cites | Huang 2019, PMC section 6: "131 SCC (36 in situ, 87 invasive lesions, and 8 keratoacanthomas)"; PMC section 4: "the term SCC includes SCC in situ, SCC invasive, and keratoacanthomas" |
| Squamous cell carcinoma in situ (8070/2) | paediatric not_reported; exclusion; no paper cited | paediatric occurs; exclusion, unchanged; the `sk_not_malignant` option gains the cite | Huang 2019, PMC section 6: "131 SCC (36 in situ, 87 invasive lesions, and 8 keratoacanthomas)" |
| Nevus sebaceus (epidermal naevus), no code (/0) | paediatric occurs; exclusion | unchanged values; why and the `sk_not_malignant` option gain the Huang cite: nevus sebaceus was the predisposing lesion in 9 of 95 patients with basal cell carcinoma | Huang 2019, PMC section 12 (Table I): "Nevus sebaceus 0 (0) 9 (9) 9 (7)" |
| Actinic keratosis (8070/0), new entity | not listed | paediatric occurs; exclusion; new `sk_not_malignant` option after Angiokeratoma, reason "Actinic keratosis (8070/0) is benign." ICD-O-3.2 prints Actinic keratosis as the preferred term at 8070/0; the ICCC-2017 XIe range holds 8070 at skin at /3 only | Huang 2019, PMC section 8: "including 21 with actinic keratoses" |
| `sk_histology` picker answer | "A carcinoma of a named type — basal cell, squamous cell, Merkel cell, adnexal (sweat gland, hair follicle or sebaceous) or another", first | "A named subtype of basal cell or squamous cell carcinoma (nodular, superficial, keratinizing and others), or another named carcinoma — Merkel cell, adnexal (sweat gland, hair follicle or sebaceous) or another", fifth. Relabelled so a plain basal cell or squamous cell carcinoma takes its own option and a named subtype (8091, 8092, 8097, 8071 and the rest) still reaches its code | no new cite; follows from the two new options |
| `sk_histology` option order | picker, Carcinoma with no type named, Melanoma, Keratoacanthoma, then the rest | Basal cell carcinoma, Squamous cell carcinoma, Melanoma, Keratoacanthoma, picker, Carcinoma with no type named, then the rest unchanged | registrar's rule of 8 October 2026: entities reported in children first, commonest first |
| Sources | four | six: Huang 2019 and Kaloga 2016 added, who_volume "not a WHO summary; paediatric evidence" | file headers |
| Data gaps | three | six: gap 1 narrowed to Merkel cell carcinoma, the adnexal carcinomas and the basal cell and squamous cell subtypes; gap 3 narrowed to basal cell carcinoma; gaps 4 (paediatric frequency ranking), 5 (whether the picker keeps 8090/3 and 8070/3) and 6 (Carcinoma, NOS, an option with no paediatric source) added | — |
| Registrar question 2 | asked whether basal cell, squamous cell, Merkel cell and pilomatrical carcinoma become options | answered by the 8 October 2026 ruling: basal cell and squamous cell carcinoma are options; Merkel cell and pilomatrical carcinoma stay in the picker | — |

Searched for and not found in either paper: Merkel cell carcinoma, sebaceous carcinoma, pilomatrical carcinoma, porocarcinoma and every other adnexal carcinoma, and every named basal cell or squamous cell subtype (nodular, superficial, infiltrating, keratinizing). Those entries keep paediatric not_reported and stay in the picker. Carcinoma, NOS (8010/3) stays an option with no paediatric source (section 10, gap 6).

Named by Huang 2019 and not added: atypical naevi and lentigines, which are melanocytic and belong to the melanoma part; porokeratosis and warts, for which ICD-O-3.2 prints no term; and nine melanomas in patients with non-melanoma skin cancer, which the melanoma entity (a referral to the melanoma tree) already covers. Kaloga 2016 quotes regional skin cancer frequencies (squamous cell carcinoma 3%, basal cell carcinoma 2%) without ages, so they are not used. Huang's abstract gives 40 basal cell and 90 squamous cell carcinomas; its Results and Table I give 95 and 40, and this file follows Table I.
