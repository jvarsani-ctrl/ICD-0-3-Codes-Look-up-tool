# Group 11 evidence — XIf10 parathyroid and other endocrine glands, central nervous system and peritoneum carcinoma sites; XIf11 unspecified site

Part `XIf10_parathyroid_other_unspecified`. Evidence for the general carcinoma tree at the parathyroid gland (C75.0), the other endocrine sites (C75.2, C75.4, C75.5, C75.8, C75.9), the brain, spinal cord and meninges (C70-C72), the retroperitoneum and peritoneum (C48), the ill-defined sites (C76) and unknown primary site (C80.9). The JSON file of the same name holds every cite object. Written 8 October 2026.

## 1 Sources

| File | Citation | WHO volume |
|---|---|---|
| `XIf10-parathyroid__Erickson-2022.txt` | Erickson LA, Mete O, Juhlin CC, Perren A, Gill AJ. Overview of the 2022 WHO Classification of Parathyroid Tumors. Endocr Pathol 2022;33(1):64-89. doi:10.1007/s12022-022-09709-1 | WHO Endocrine and Neuroendocrine Tumours, 5th ed., 2022 |
| `XIf10-parathyroid__ICCR-Parathyroid-2nd.txt` | International Collaboration on Cancer Reporting. Parathyroid Carcinoma and Atypical Parathyroid Neoplasm Histopathology Reporting Guide, 2nd ed., version 2.0, November 2025. ISBN 978-1-922324-69-6 | WHO Classification of Endocrine and Neuroendocrine Tumours, 5th edition, 2025 (as the guide prints it) |
| `XIf11-unknown-primary-head-neck__Hernandez-Prera-2022.txt` | Hernandez-Prera JC. Update from the 5th Edition of the World Health Organization Classification of Head and Neck Tumors: The Neck and Lymph Nodes, Metastasis, and Melanocytic Tumors. Head Neck Pathol 2022;16(1):110-122. doi:10.1007/s12105-022-01433-w | WHO Head and Neck Tumours, 5th ed., 2022 |
| `ALL-paediatric-occurrence__Pfister-2022.txt` | Pfister SM, Reyes-Mugica M, Chan JKC, et al. A Summary of the Inaugural WHO Classification of Pediatric Tumors: Transitioning from the Optical into the Molecular Era. Cancer Discov 2022;12(2):331-355 | WHO Paediatric Tumours, 5th ed., 2022 |
| `RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt` | World Health Organization. International Classification of Diseases for Oncology, 3rd edition, 1st revision (ICD-O-3.1), section 4, Coding guidelines, printed pp. 14-28 (PDF p. 1 = printed p. 14) | Not a tumour classification; the coding manual |

The WHO ICD-O-3.1 manual's PDF p. 1 is printed p. 14. Codes were checked against `icdo32.sqlite` (IARC final, 9 October 2020) and subgroups against `ICCC-2017.sqlite`.

## 2 Entities

Entities with their own decision first; then the long-tail picker and the codes never built. ICD-O-3.2 terms are verbatim.

| Entity | Code | ICD-O-3.2 term (level) | Preferred term | Paediatric | Decision | Page |
|---|---|---|---|---|---|---|
| Parathyroid carcinoma | 8140/3 | Parathyroid carcinoma (Related) | Adenocarcinoma, NOS | rare | option | ICCR Parathyroid 2025, PDF p. 9 (table); ICCR Parathyroid 2025, PDF p. 8; Pfister 2022, PDF p. 14; Pfister 2022, PDF p. 19; ICCR Parathyroid 2025, PDF p. 5 |
| Atypical parathyroid tumour | 8140/1 | Atypical adenoma (Preferred) | Atypical adenoma | not_reported | exclusion | ICCR Parathyroid 2025, PDF p. 9 (table); ICCR Parathyroid 2025, PDF p. 8; Erickson 2022, PDF p. 1; Erickson 2022, PDF p. 12; Erickson 2022, PDF p. 2 |
| Parathyroid adenoma | 8140/0 | Adenoma, NOS (Preferred) | Adenoma, NOS | occurs | exclusion | ICCR Parathyroid 2025, PDF p. 9 (table); Pfister 2022, PDF p. 14; Erickson 2022, PDF p. 1 |
| Chief cell adenoma (ICD-O-3.2 term for chief cell parathyroid adenoma) | 8321/0 | Chief cell adenoma (Preferred) | Chief cell adenoma | not_reported | exclusion |  |
| Parathyroid lipoadenoma | 8324/0 | Lipoadenoma (Preferred) | Lipoadenoma | not_reported | exclusion | ICCR Parathyroid 2025, PDF p. 9 (table) |
| Carcinoma of unknown primary; carcinoma with no type named | 8010/3 | Carcinoma, NOS (Preferred) | Carcinoma, NOS | not_reported | option | WHO ICD-O-3.1 manual, PDF p. 6; Hernandez-Prera 2022, PDF p. 2; Hernandez-Prera 2022, PDF p. 8 |
| Heterotopia-associated carcinoma | 8010/3 | Heterotopia-associated carcinoma (Related) | Carcinoma, NOS | occurs | registrar | Hernandez-Prera 2022, PDF p. 2; Hernandez-Prera 2022, PDF p. 6; Hernandez-Prera 2022, PDF p. 7 |
| Papillary thyroid carcinoma in a neck lymph node, primary not found | 8260/3 | Papillary carcinoma of thyroid (Related) | Papillary adenocarcinoma, NOS | occurs | refer | WHO ICD-O-3.1 manual, PDF p. 10; Hernandez-Prera 2022, PDF p. 6; Pfister 2022, PDF p. 14 |
| Nasopharyngeal carcinoma in a neck lymph node (Schmincke tumour) | 8082/3 | Schmincke tumor (Related) | Lymphoepithelial carcinoma | common | refer | Pfister 2022, PDF p. 14; Hernandez-Prera 2022, PDF p. 8 |
| Pseudomyxoma peritonei | 8480/6 | Pseudomyxoma peritonei (Preferred) | Pseudomyxoma peritonei | not_reported | refer | WHO ICD-O-3.1 manual, PDF p. 6; WHO ICD-O-3.1 manual, PDF p. 7 |
| Mesothelioma (malignant; epithelioid 9052/3, biphasic 9053/3, sarcomatoid 9051/3) | 9050/3 | Mesothelioma, malignant (Preferred) | Mesothelioma, malignant | occurs | refer (Group 12) | Pfister 2022, PDF p. 13 |
| Peritoneal inclusion cyst (multicystic mesothelioma) | 9055/0 | Peritoneal inclusion cysts (Preferred) | Peritoneal inclusion cysts | occurs | exclusion | Pfister 2022, PDF p. 13 |
| Well-differentiated papillary mesothelioma of the peritoneum | 9052/0 | Well differentiated papillary mesothelioma (Related) | Epithelioid mesothelioma, benign | not_reported | exclusion |  |
| Desmoplastic small round cell tumour | 8806/3 | Desmoplastic small round cell tumor (Preferred) | Desmoplastic small round cell tumor | occurs | refer (Group 9) | Pfister 2022, PDF p. 9 |
| Carotid body paraganglioma | 8692/3 | Carotid body paraganglioma (Preferred) | Carotid body paraganglioma | occurs | refer (Group 4) | Pfister 2022, PDF p. 14 |
| Aortic body paraganglioma | 8691/3 | Aortic body paraganglioma (Synonym) | Aortic body tumor | occurs | refer (Group 4) | Pfister 2022, PDF p. 14 |
| Extra-adrenal paraganglioma (sympathetic paraganglioma) | 8693/3 | Extra-adrenal paraganglioma, NOS (Preferred) | Extra-adrenal paraganglioma, NOS | occurs | refer (Group 4) | Pfister 2022, PDF p. 14 |
| Craniopharyngioma | 9350/1 | Craniopharyngioma, NOS (Preferred) | Craniopharyngioma, NOS | common | refer (Group 3) | Pfister 2022, PDF p. 18 |
| Pituitary blastoma | 8273/3 | Pituitary blastoma (Preferred) | Pituitary blastoma | occurs | refer (Group 3) | Pfister 2022, PDF p. 18 |
| Pituitary carcinoma | 8272/3 | Pituitary carcinoma, NOS (Preferred) | Pituitary carcinoma, NOS | not_reported | refer (Group 3) |  |
| Choroid plexus carcinoma | 9390/3 | Choroid plexus carcinoma (Preferred) | Choroid plexus carcinoma | occurs | refer (Group 3) | Pfister 2022, PDF p. 17 |
| Hepatocellular carcinoma presenting with no primary site named | 8170/3 | Hepatocellular carcinoma, NOS (Preferred) | Hepatocellular carcinoma, NOS | occurs | refer (Group 7) | WHO ICD-O-3.1 manual, PDF p. 10; Pfister 2022, PDF p. 13 |
| Seromucinous carcinoma | 8474/3 | Seromucinous carcinoma (Preferred) | Seromucinous carcinoma | not_reported | refer (Group 10) |  |
| Epithelioma, malignant (ICD-O-3.2 term) | 8011/3 | Epithelioma, malignant (Preferred) | Epithelioma, malignant | not_reported | picker |  |
| Large cell carcinoma, NOS (ICD-O-3.2 term) | 8012/3 | Large cell carcinoma, NOS (Preferred) | Large cell carcinoma, NOS | not_reported | picker |  |
| Large cell neuroendocrine carcinoma (ICD-O-3.2 term) | 8013/3 | Large cell neuroendocrine carcinoma (Preferred) | Large cell neuroendocrine carcinoma | not_reported | picker |  |
| Large cell carcinoma with rhabdoid phenotype (ICD-O-3.2 term) | 8014/3 | Large cell carcinoma with rhabdoid phenotype (Preferred) | Large cell carcinoma with rhabdoid phenotype | not_reported | picker |  |
| Glassy cell carcinoma (ICD-O-3.2 term) | 8015/3 | Glassy cell carcinoma (Preferred) | Glassy cell carcinoma | not_reported | picker |  |
| Carcinoma, undifferentiated, NOS (ICD-O-3.2 term) | 8020/3 | Carcinoma, undifferentiated, NOS (Preferred) | Carcinoma, undifferentiated, NOS | not_reported | picker | Hernandez-Prera 2022, PDF p. 8 |
| Carcinoma, anaplastic, NOS (ICD-O-3.2 term) | 8021/3 | Carcinoma, anaplastic, NOS (Preferred) | Carcinoma, anaplastic, NOS | not_reported | picker |  |
| Pleomorphic carcinoma (ICD-O-3.2 term) | 8022/3 | Pleomorphic carcinoma (Preferred) | Pleomorphic carcinoma | not_reported | picker |  |
| Nuclear protein in testis (NUT)-associated carcinoma (ICD-O-3.2 term) | 8023/3 | Nuclear protein in testis (NUT)-associated carcinoma (Preferred) | Nuclear protein in testis (NUT)-associated carcinoma | not_reported | picker |  |
| Giant cell and spindle cell carcinoma (ICD-O-3.2 term) | 8030/3 | Giant cell and spindle cell carcinoma (Preferred) | Giant cell and spindle cell carcinoma | not_reported | picker |  |
| Giant cell carcinoma (ICD-O-3.2 term) | 8031/3 | Giant cell carcinoma (Preferred) | Giant cell carcinoma | not_reported | picker |  |
| Spindle cell carcinoma, NOS (ICD-O-3.2 term) | 8032/3 | Spindle cell carcinoma, NOS (Preferred) | Spindle cell carcinoma, NOS | not_reported | picker |  |
| Pseudosarcomatous carcinoma (ICD-O-3.2 term) | 8033/3 | Pseudosarcomatous carcinoma (Preferred) | Pseudosarcomatous carcinoma | not_reported | picker |  |
| Polygonal cell carcinoma (ICD-O-3.2 term) | 8034/3 | Polygonal cell carcinoma (Preferred) | Polygonal cell carcinoma | not_reported | picker |  |
| Carcinoma with osteoclast-like giant cells (ICD-O-3.2 term) | 8035/3 | Carcinoma with osteoclast-like giant cells (Preferred) | Carcinoma with osteoclast-like giant cells | not_reported | picker |  |
| Small cell carcinoma, NOS (ICD-O-3.2 term) | 8041/3 | Small cell carcinoma, NOS (Preferred) | Small cell carcinoma, NOS | not_reported | picker |  |
| Oat cell carcinoma (ICD-O-3.2 term) | 8042/3 | Oat cell carcinoma (Preferred) | Oat cell carcinoma | not_reported | not_built |  |
| Small cell carcinoma, fusiform cell (ICD-O-3.2 term) | 8043/3 | Small cell carcinoma, fusiform cell (Preferred) | Small cell carcinoma, fusiform cell | not_reported | picker |  |
| Small cell carcinoma, intermediate cell (ICD-O-3.2 term) | 8044/3 | Small cell carcinoma, intermediate cell (Preferred) | Small cell carcinoma, intermediate cell | not_reported | picker |  |
| Combined small cell carcinoma (ICD-O-3.2 term) | 8045/3 | Combined small cell carcinoma (Preferred) | Combined small cell carcinoma | not_reported | picker |  |
| Non-small cell carcinoma (ICD-O-3.2 term) | 8046/3 | Non-small cell carcinoma (Preferred) | Non-small cell carcinoma | not_reported | picker |  |
| Papillary carcinoma, NOS (ICD-O-3.2 term) | 8050/3 | Papillary carcinoma, NOS (Preferred) | Papillary carcinoma, NOS | not_reported | picker |  |
| Verrucous carcinoma, NOS (ICD-O-3.2 term) | 8051/3 | Verrucous carcinoma, NOS (Preferred) | Verrucous carcinoma, NOS | not_reported | picker |  |
| Papillary squamous cell carcinoma (ICD-O-3.2 term) | 8052/3 | Papillary squamous cell carcinoma (Preferred) | Papillary squamous cell carcinoma | not_reported | picker |  |
| Warty carcinoma (ICD-O-3.2 term) | 8054/3 | Warty carcinoma (Preferred) | Warty carcinoma | not_reported | picker |  |
| Squamous cell carcinoma, NOS (ICD-O-3.2 term) | 8070/3 | Squamous cell carcinoma, NOS (Preferred) | Squamous cell carcinoma, NOS | not_reported | picker | Hernandez-Prera 2022, PDF p. 8 |
| Squamous cell carcinoma, keratinizing, NOS (ICD-O-3.2 term) | 8071/3 | Squamous cell carcinoma, keratinizing, NOS (Preferred) | Squamous cell carcinoma, keratinizing, NOS | not_reported | picker |  |
| Squamous cell carcinoma, large cell, nonkeratinizing, NOS (ICD-O-3.2 term) | 8072/3 | Squamous cell carcinoma, large cell, nonkeratinizing, NOS (Preferred) | Squamous cell carcinoma, large cell, nonkeratinizing, NOS | not_reported | picker | Hernandez-Prera 2022, PDF p. 8; Pfister 2022, PDF p. 14 |
| Squamous cell carcinoma, small cell, nonkeratinizing (ICD-O-3.2 term) | 8073/3 | Squamous cell carcinoma, small cell, nonkeratinizing (Preferred) | Squamous cell carcinoma, small cell, nonkeratinizing | not_reported | picker |  |
| Squamous cell carcinoma, spindle cell (ICD-O-3.2 term) | 8074/3 | Squamous cell carcinoma, spindle cell (Preferred) | Squamous cell carcinoma, spindle cell | not_reported | picker |  |
| Squamous cell carcinoma, adenoid (ICD-O-3.2 term) | 8075/3 | Squamous cell carcinoma, adenoid (Preferred) | Squamous cell carcinoma, adenoid | not_reported | picker |  |
| Squamous cell carcinoma, microinvasive (ICD-O-3.2 term) | 8076/3 | Squamous cell carcinoma, microinvasive (Preferred) | Squamous cell carcinoma, microinvasive | not_reported | picker |  |
| Lymphoepithelial carcinoma (ICD-O-3.2 term) | 8082/3 | Lymphoepithelial carcinoma (Preferred) | Lymphoepithelial carcinoma | not_reported | picker | Hernandez-Prera 2022, PDF p. 8; Pfister 2022, PDF p. 14 |
| Basaloid squamous cell carcinoma (ICD-O-3.2 term) | 8083/3 | Basaloid squamous cell carcinoma (Preferred) | Basaloid squamous cell carcinoma | not_reported | picker |  |
| Squamous cell carcinoma, clear cell type (ICD-O-3.2 term) | 8084/3 | Squamous cell carcinoma, clear cell type (Preferred) | Squamous cell carcinoma, clear cell type | not_reported | picker |  |
| Squamous cell carcinoma, HPV positive (ICD-O-3.2 term) | 8085/3 | Squamous cell carcinoma, HPV positive (Preferred) | Squamous cell carcinoma, HPV positive | not_reported | picker | Hernandez-Prera 2022, PDF p. 8 |
| Squamous cell carcinoma, HPV negative (ICD-O-3.2 term) | 8086/3 | Squamous cell carcinoma, HPV negative (Preferred) | Squamous cell carcinoma, HPV negative | not_reported | picker |  |
| Adenoid basal carcinoma (ICD-O-3.2 term) | 8098/3 | Adenoid basal carcinoma (Preferred) | Adenoid basal carcinoma | not_reported | picker |  |
| Transitional cell carcinoma, NOS (ICD-O-3.2 term) | 8120/3 | Transitional cell carcinoma, NOS (Preferred) | Transitional cell carcinoma, NOS | not_reported | picker |  |
| Schneiderian carcinoma (ICD-O-3.2 term) | 8121/3 | Schneiderian carcinoma (Preferred) | Schneiderian carcinoma | not_reported | picker |  |
| Urothelial carcinoma, sarcomatoid (ICD-O-3.2 term) | 8122/3 | Urothelial carcinoma, sarcomatoid (Preferred) | Urothelial carcinoma, sarcomatoid | not_reported | picker |  |
| Basaloid carcinoma (ICD-O-3.2 term) | 8123/3 | Basaloid carcinoma (Preferred) | Basaloid carcinoma | not_reported | picker |  |
| Cloacogenic carcinoma (ICD-O-3.2 term) | 8124/3 | Cloacogenic carcinoma (Preferred) | Cloacogenic carcinoma | not_reported | not_built |  |
| Papillary urothelial carcinoma (ICD-O-3.2 term) | 8130/3 | Papillary urothelial carcinoma (Preferred) | Papillary urothelial carcinoma | not_reported | not_built |  |
| Urothelial carcinoma, micropapillary (ICD-O-3.2 term) | 8131/3 | Urothelial carcinoma, micropapillary (Preferred) | Urothelial carcinoma, micropapillary | not_reported | picker |  |
| Scirrhous adenocarcinoma (ICD-O-3.2 term) | 8141/3 | Scirrhous adenocarcinoma (Preferred) | Scirrhous adenocarcinoma | not_reported | not_built |  |
| Linitis plastica (ICD-O-3.2 term) | 8142/3 | Linitis plastica (Preferred) | Linitis plastica | not_reported | picker |  |
| Superficial spreading adenocarcinoma (ICD-O-3.2 term) | 8143/3 | Superficial spreading adenocarcinoma (Preferred) | Superficial spreading adenocarcinoma | not_reported | picker |  |
| Adenocarcinoma, intestinal type (ICD-O-3.2 term) | 8144/3 | Adenocarcinoma, intestinal type (Preferred) | Adenocarcinoma, intestinal type | not_reported | picker |  |
| Carcinoma, diffuse type (ICD-O-3.2 term) | 8145/3 | Carcinoma, diffuse type (Preferred) | Carcinoma, diffuse type | not_reported | picker |  |
| Basal cell adenocarcinoma (ICD-O-3.2 term) | 8147/3 | Basal cell adenocarcinoma (Preferred) | Basal cell adenocarcinoma | not_reported | picker |  |
| Pancreatic neuroendocrine tumor, nonfunctioning (ICD-O-3.2 term) | 8150/3 | Pancreatic neuroendocrine tumor, nonfunctioning (Preferred) | Pancreatic neuroendocrine tumor, nonfunctioning | not_reported | picker |  |
| Insulinoma, NOS (ICD-O-3.2 term) | 8151/3 | Insulinoma, NOS (Preferred) | Insulinoma, NOS | not_reported | picker |  |
| Glucagonoma (ICD-O-3.2 term) | 8152/3 | Glucagonoma (Preferred) | Glucagonoma | not_reported | picker |  |
| Gastrinoma (ICD-O-3.2 term) | 8153/3 | Gastrinoma (Preferred) | Gastrinoma | not_reported | picker |  |
| Mixed neuroendocrine non-neuroendocrine neoplasm (MiNEN) (ICD-O-3.2 term) | 8154/3 | Mixed neuroendocrine non-neuroendocrine neoplasm (MiNEN) (Preferred) | Mixed neuroendocrine non-neuroendocrine neoplasm (MiNEN) | not_reported | picker |  |
| Vipoma (ICD-O-3.2 term) | 8155/3 | Vipoma (Preferred) | Vipoma | not_reported | picker |  |
| Somatostatinoma (ICD-O-3.2 term) | 8156/3 | Somatostatinoma (Preferred) | Somatostatinoma | not_reported | picker |  |
| ACTH-producing tumor (ICD-O-3.2 term) | 8158/3 | ACTH-producing tumor (Preferred) | ACTH-producing tumor | not_reported | picker |  |
| Pancreatobiliary type carcinoma (ICD-O-3.2 term) | 8163/3 | Pancreatobiliary type carcinoma (Preferred) | Pancreatobiliary type carcinoma | not_reported | picker |  |
| Trabecular adenocarcinoma (ICD-O-3.2 term) | 8190/3 | Trabecular adenocarcinoma (Preferred) | Trabecular adenocarcinoma | not_reported | picker |  |
| Adenoid cystic carcinoma (ICD-O-3.2 term) | 8200/3 | Adenoid cystic carcinoma (Preferred) | Adenoid cystic carcinoma | not_reported | picker |  |
| Cribriform carcinoma, NOS (ICD-O-3.2 term) | 8201/3 | Cribriform carcinoma, NOS (Preferred) | Cribriform carcinoma, NOS | not_reported | picker |  |
| Adenocarcinoma in adenomatous polyp (ICD-O-3.2 term) | 8210/3 | Adenocarcinoma in adenomatous polyp (Preferred) | Adenocarcinoma in adenomatous polyp | not_reported | picker |  |
| Tubular adenocarcinoma (ICD-O-3.2 term) | 8211/3 | Tubular adenocarcinoma (Preferred) | Tubular adenocarcinoma | not_reported | picker |  |
| Serrated adenocarcinoma (ICD-O-3.2 term) | 8213/3 | Serrated adenocarcinoma (Preferred) | Serrated adenocarcinoma | not_reported | picker |  |
| Parietal cell carcinoma (ICD-O-3.2 term) | 8214/3 | Parietal cell carcinoma (Preferred) | Parietal cell carcinoma | not_reported | picker |  |
| Adenocarcinoma of anal glands (ICD-O-3.2 term) | 8215/3 | Adenocarcinoma of anal glands (Preferred) | Adenocarcinoma of anal glands | not_reported | picker |  |
| Adenocarcinoma in adenomatous polyposis coli (ICD-O-3.2 term) | 8220/3 | Adenocarcinoma in adenomatous polyposis coli (Preferred) | Adenocarcinoma in adenomatous polyposis coli | not_reported | picker |  |
| Adenocarcinoma in multiple adenomatous polyps (ICD-O-3.2 term) | 8221/3 | Adenocarcinoma in multiple adenomatous polyps (Preferred) | Adenocarcinoma in multiple adenomatous polyps | not_reported | picker |  |
| Solid carcinoma, NOS (ICD-O-3.2 term) | 8230/3 | Solid carcinoma, NOS (Preferred) | Solid carcinoma, NOS | not_reported | picker |  |
| Carcinoma simplex (ICD-O-3.2 term) | 8231/3 | Carcinoma simplex (Preferred) | Carcinoma simplex | not_reported | picker |  |
| Neuroendocrine tumor, NOS (ICD-O-3.2 term) | 8240/3 | Neuroendocrine tumor, NOS (Preferred) | Neuroendocrine tumor, NOS | not_reported | picker |  |
| Enterochromaffin cell carcinoid (ICD-O-3.2 term) | 8241/3 | Enterochromaffin cell carcinoid (Preferred) | Enterochromaffin cell carcinoid | not_reported | picker |  |
| Enterochromaffin-like cell tumor (ICD-O-3.2 term) | 8242/3 | Enterochromaffin-like cell tumor (Preferred) | Enterochromaffin-like cell tumor | not_reported | picker |  |
| Goblet cell carcinoid (ICD-O-3.2 term) | 8243/3 | Goblet cell carcinoid (Preferred) | Goblet cell carcinoid | not_reported | picker |  |
| Mixed adenoneuroendocrine carcinoma (ICD-O-3.2 term) | 8244/3 | Mixed adenoneuroendocrine carcinoma (Preferred) | Mixed adenoneuroendocrine carcinoma | not_reported | picker |  |
| Adenocarcinoid tumor (ICD-O-3.2 term) | 8245/3 | Adenocarcinoid tumor (Preferred) | Adenocarcinoid tumor | not_reported | not_built |  |
| Neuroendocrine carcinoma, NOS (ICD-O-3.2 term) | 8246/3 | Neuroendocrine carcinoma, NOS (Preferred) | Neuroendocrine carcinoma, NOS | not_reported | picker | Hernandez-Prera 2022, PDF p. 8 |
| Merkel cell carcinoma (ICD-O-3.2 term) | 8247/3 | Merkel cell carcinoma (Preferred) | Merkel cell carcinoma | not_reported | picker | WHO ICD-O-3.1 manual, PDF p. 10 |
| Neuroendocrine tumor, grade 2 (ICD-O-3.2 term) | 8249/3 | Neuroendocrine tumor, grade 2 (Preferred) | Neuroendocrine tumor, grade 2 | not_reported | picker |  |
| Lepidic adenocarcinoma (ICD-O-3.2 term) | 8250/3 | Lepidic adenocarcinoma (Preferred) | Lepidic adenocarcinoma | not_reported | picker |  |
| Alveolar adenocarcinoma (ICD-O-3.2 term) | 8251/3 | Alveolar adenocarcinoma (Preferred) | Alveolar adenocarcinoma | not_reported | not_built |  |
| Bronchiolo-alveolar carcinoma, non-mucinous (ICD-O-3.2 term) | 8252/3 | Bronchiolo-alveolar carcinoma, non-mucinous (Preferred) | Bronchiolo-alveolar carcinoma, non-mucinous | not_reported | picker |  |
| Adenocarcinoma of lung, mucinous (ICD-O-3.2 term) | 8253/3 | Adenocarcinoma of lung, mucinous (Preferred) | Adenocarcinoma of lung, mucinous | not_reported | picker |  |
| Adenocarcinoma of lung, mixed mucinous and non-mucinous (ICD-O-3.2 term) | 8254/3 | Adenocarcinoma of lung, mixed mucinous and non-mucinous (Preferred) | Adenocarcinoma of lung, mixed mucinous and non-mucinous | not_reported | picker |  |
| Adenocarcinoma with mixed subtypes (ICD-O-3.2 term) | 8255/3 | Adenocarcinoma with mixed subtypes (Preferred) | Adenocarcinoma with mixed subtypes | not_reported | picker |  |
| Minimally invasive adenocarcinoma, non-mucinous (ICD-O-3.2 term) | 8256/3 | Minimally invasive adenocarcinoma, non-mucinous (Preferred) | Minimally invasive adenocarcinoma, non-mucinous | not_reported | picker |  |
| Minimally invasive adenocarcinoma, mucinous (ICD-O-3.2 term) | 8257/3 | Minimally invasive adenocarcinoma, mucinous (Preferred) | Minimally invasive adenocarcinoma, mucinous | not_reported | picker |  |
| Papillary adenocarcinoma, NOS (ICD-O-3.2 term) | 8260/3 | Papillary adenocarcinoma, NOS (Preferred) | Papillary adenocarcinoma, NOS | not_reported | picker | Hernandez-Prera 2022, PDF p. 6 |
| Adenocarcinoma in villous adenoma (ICD-O-3.2 term) | 8261/3 | Adenocarcinoma in villous adenoma (Preferred) | Adenocarcinoma in villous adenoma | not_reported | picker |  |
| Villous adenocarcinoma (ICD-O-3.2 term) | 8262/3 | Villous adenocarcinoma (Preferred) | Villous adenocarcinoma | not_reported | picker |  |
| Adenocarcinoma in tubulovillous adenoma (ICD-O-3.2 term) | 8263/3 | Adenocarcinoma in tubulovillous adenoma (Preferred) | Adenocarcinoma in tubulovillous adenoma | not_reported | picker |  |
| Micropapillary carcinoma, NOS (ICD-O-3.2 term) | 8265/3 | Micropapillary carcinoma, NOS (Preferred) | Micropapillary carcinoma, NOS | not_reported | picker |  |
| Oxyphilic adenocarcinoma (ICD-O-3.2 term) | 8290/3 | Oxyphilic adenocarcinoma (Preferred) | Oxyphilic adenocarcinoma | not_reported | picker |  |
| Clear cell adenocarcinoma, NOS (ICD-O-3.2 term) | 8310/3 | Clear cell adenocarcinoma, NOS (Preferred) | Clear cell adenocarcinoma, NOS | not_reported | picker |  |
| Lipid-rich carcinoma (ICD-O-3.2 term) | 8314/3 | Lipid-rich carcinoma (Preferred) | Lipid-rich carcinoma | not_reported | picker |  |
| Glycogen-rich carcinoma (ICD-O-3.2 term) | 8315/3 | Glycogen-rich carcinoma (Preferred) | Glycogen-rich carcinoma | not_reported | picker |  |
| Granular cell carcinoma (ICD-O-3.2 term) | 8320/3 | Granular cell carcinoma (Preferred) | Granular cell carcinoma | not_reported | picker |  |
| Water-clear cell adenocarcinoma (ICD-O-3.2 term) | 8322/3 | Water-clear cell adenocarcinoma (Preferred) | Water-clear cell adenocarcinoma | not_reported | picker | ICCR Parathyroid 2025, PDF p. 9 (table) |
| Mixed cell adenocarcinoma (ICD-O-3.2 term) | 8323/3 | Mixed cell adenocarcinoma (Preferred) | Mixed cell adenocarcinoma | not_reported | picker |  |
| Fetal adenocarcinoma (ICD-O-3.2 term) | 8333/3 | Fetal adenocarcinoma (Preferred) | Fetal adenocarcinoma | not_reported | picker |  |
| Endometrioid adenocarcinoma, NOS (ICD-O-3.2 term) | 8380/3 | Endometrioid adenocarcinoma, NOS (Preferred) | Endometrioid adenocarcinoma, NOS | not_reported | picker |  |
| Endometrioid adenofibroma, malignant (ICD-O-3.2 term) | 8381/3 | Endometrioid adenofibroma, malignant (Preferred) | Endometrioid adenofibroma, malignant | not_reported | picker |  |
| Endometrioid adenocarcinoma, secretory variant (ICD-O-3.2 term) | 8382/3 | Endometrioid adenocarcinoma, secretory variant (Preferred) | Endometrioid adenocarcinoma, secretory variant | not_reported | picker |  |
| Endometrioid adenocarcinoma, ciliated cell variant (ICD-O-3.2 term) | 8383/3 | Endometrioid adenocarcinoma, ciliated cell variant (Preferred) | Endometrioid adenocarcinoma, ciliated cell variant | not_reported | picker |  |
| Adenocarcinoma, endocervical type, NOS (ICD-O-3.2 term) | 8384/3 | Adenocarcinoma, endocervical type, NOS (Preferred) | Adenocarcinoma, endocervical type, NOS | not_reported | picker |  |
| Apocrine adenocarcinoma (ICD-O-3.2 term) | 8401/3 | Apocrine adenocarcinoma (Preferred) | Apocrine adenocarcinoma | not_reported | picker |  |
| Hidradenocarcinoma (ICD-O-3.2 term) | 8402/3 | Hidradenocarcinoma (Preferred) | Hidradenocarcinoma | not_reported | picker |  |
| Syringocystadenocarcinoma papilliferum (ICD-O-3.2 term) | 8406/3 | Syringocystadenocarcinoma papilliferum (Preferred) | Syringocystadenocarcinoma papilliferum | not_reported | picker |  |
| Sebaceous carcinoma (ICD-O-3.2 term) | 8410/3 | Sebaceous carcinoma (Preferred) | Sebaceous carcinoma | not_reported | picker |  |
| Mucoepidermoid carcinoma (ICD-O-3.2 term) | 8430/3 | Mucoepidermoid carcinoma (Preferred) | Mucoepidermoid carcinoma | not_reported | picker | Hernandez-Prera 2022, PDF p. 7; Pfister 2022, PDF p. 14 |
| Cystadenocarcinoma, NOS (ICD-O-3.2 term) | 8440/3 | Cystadenocarcinoma, NOS (Preferred) | Cystadenocarcinoma, NOS | not_reported | not_built |  |
| Serous carcinoma, NOS (ICD-O-3.2 term) | 8441/3 | Serous carcinoma, NOS (Preferred) | Serous carcinoma, NOS | not_reported | picker |  |
| Papillary cystadenocarcinoma, NOS (ICD-O-3.2 term) | 8450/3 | Papillary cystadenocarcinoma, NOS (Preferred) | Papillary cystadenocarcinoma, NOS | not_reported | not_built |  |
| Solid pseudopapillary neoplasm of pancreas (ICD-O-3.2 term) | 8452/3 | Solid pseudopapillary neoplasm of pancreas (Preferred) | Solid pseudopapillary neoplasm of pancreas | not_reported | picker |  |
| Intraductal papillary mucinous neoplasm with an associated invasive carcinoma (ICD-O-3.2 term) | 8453/3 | Intraductal papillary mucinous neoplasm with an associated invasive carcinoma (Preferred) | Intraductal papillary mucinous neoplasm with an associated invasive carcinoma | not_reported | picker |  |
| Low grade serous carcinoma (ICD-O-3.2 term) | 8460/3 | Low grade serous carcinoma (Preferred) | Low grade serous carcinoma | not_reported | picker | WHO ICD-O-3.1 manual, PDF p. 10 |
| High grade serous carcinoma (ICD-O-3.2 term) | 8461/3 | High grade serous carcinoma (Preferred) | High grade serous carcinoma | not_reported | picker | WHO ICD-O-3.1 manual, PDF p. 10 |
| Mucinous cystadenocarcinoma, NOS (ICD-O-3.2 term) | 8470/3 | Mucinous cystadenocarcinoma, NOS (Preferred) | Mucinous cystadenocarcinoma, NOS | not_reported | picker |  |
| Mucinous adenocarcinoma (ICD-O-3.2 term) | 8480/3 | Mucinous adenocarcinoma (Preferred) | Mucinous adenocarcinoma | not_reported | picker | WHO ICD-O-3.1 manual, PDF p. 10 |
| Mucin-producing adenocarcinoma (ICD-O-3.2 term) | 8481/3 | Mucin-producing adenocarcinoma (Preferred) | Mucin-producing adenocarcinoma | not_reported | picker |  |
| Mucinous carcinoma, gastric type (ICD-O-3.2 term) | 8482/3 | Mucinous carcinoma, gastric type (Preferred) | Mucinous carcinoma, gastric type | not_reported | picker |  |
| Signet ring cell carcinoma (ICD-O-3.2 term) | 8490/3 | Signet ring cell carcinoma (Preferred) | Signet ring cell carcinoma | not_reported | picker |  |
| Infiltrating duct carcinoma, NOS (ICD-O-3.2 term) | 8500/3 | Infiltrating duct carcinoma, NOS (Preferred) | Infiltrating duct carcinoma, NOS | not_reported | picker |  |
| Comedocarcinoma, NOS (ICD-O-3.2 term) | 8501/3 | Comedocarcinoma, NOS (Preferred) | Comedocarcinoma, NOS | not_reported | picker |  |
| Secretory carcinoma (ICD-O-3.2 term) | 8502/3 | Secretory carcinoma (Preferred) | Secretory carcinoma | not_reported | picker |  |
| Intraductal papillary adenocarcinoma with invasion (ICD-O-3.2 term) | 8503/3 | Intraductal papillary adenocarcinoma with invasion (Preferred) | Intraductal papillary adenocarcinoma with invasion | not_reported | picker |  |
| Encapsulated papillary carcinoma with invasion (ICD-O-3.2 term) | 8504/3 | Encapsulated papillary carcinoma with invasion (Preferred) | Encapsulated papillary carcinoma with invasion | not_reported | picker |  |
| Invasive micropapillary carcinoma of breast (ICD-O-3.2 term) | 8507/3 | Invasive micropapillary carcinoma of breast (Preferred) | Invasive micropapillary carcinoma of breast | not_reported | picker |  |
| Cystic hypersecretory carcinoma (ICD-O-3.2 term) | 8508/3 | Cystic hypersecretory carcinoma (Preferred) | Cystic hypersecretory carcinoma | not_reported | not_built |  |
| Solid papillary carcinoma with invasion (ICD-O-3.2 term) | 8509/3 | Solid papillary carcinoma with invasion (Preferred) | Solid papillary carcinoma with invasion | not_reported | picker |  |
| Medullary carcinoma, NOS (ICD-O-3.2 term) | 8510/3 | Medullary carcinoma, NOS (Preferred) | Medullary carcinoma, NOS | not_reported | picker |  |
| Medullary carcinoma with lymphoid stroma (ICD-O-3.2 term) | 8512/3 | Medullary carcinoma with lymphoid stroma (Preferred) | Medullary carcinoma with lymphoid stroma | not_reported | not_built |  |
| Atypical medullary carcinoma (ICD-O-3.2 term) | 8513/3 | Atypical medullary carcinoma (Preferred) | Atypical medullary carcinoma | not_reported | picker |  |
| Duct carcinoma, desmoplastic type (ICD-O-3.2 term) | 8514/3 | Duct carcinoma, desmoplastic type (Preferred) | Duct carcinoma, desmoplastic type | not_reported | picker |  |
| Lobular carcinoma, NOS (ICD-O-3.2 term) | 8520/3 | Lobular carcinoma, NOS (Preferred) | Lobular carcinoma, NOS | not_reported | picker |  |
| Infiltrating ductular carcinoma (ICD-O-3.2 term) | 8521/3 | Infiltrating ductular carcinoma (Preferred) | Infiltrating ductular carcinoma | not_reported | picker |  |
| Infiltrating duct and lobular carcinoma (ICD-O-3.2 term) | 8522/3 | Infiltrating duct and lobular carcinoma (Preferred) | Infiltrating duct and lobular carcinoma | not_reported | picker |  |
| Infiltrating duct mixed with other types of carcinoma (ICD-O-3.2 term) | 8523/3 | Infiltrating duct mixed with other types of carcinoma (Preferred) | Infiltrating duct mixed with other types of carcinoma | not_reported | picker |  |
| Infiltrating lobular mixed with other types of carcinoma (ICD-O-3.2 term) | 8524/3 | Infiltrating lobular mixed with other types of carcinoma (Preferred) | Infiltrating lobular mixed with other types of carcinoma | not_reported | picker |  |
| Polymorphous adenocarcinoma (ICD-O-3.2 term) | 8525/3 | Polymorphous adenocarcinoma (Preferred) | Polymorphous adenocarcinoma | not_reported | picker |  |
| Inflammatory carcinoma (ICD-O-3.2 term) | 8530/3 | Inflammatory carcinoma (Preferred) | Inflammatory carcinoma | not_reported | picker |  |
| Paget disease, mammary (ICD-O-3.2 term) | 8540/3 | Paget disease, mammary (Preferred) | Paget disease, mammary | not_reported | picker |  |
| Paget disease and infiltrating duct carcinoma of breast (ICD-O-3.2 term) | 8541/3 | Paget disease and infiltrating duct carcinoma of breast (Preferred) | Paget disease and infiltrating duct carcinoma of breast | not_reported | picker |  |
| Paget disease, extramammary (ICD-O-3.2 term) | 8542/3 | Paget disease, extramammary (Preferred) | Paget disease, extramammary | not_reported | picker |  |
| Paget disease and intraductal carcinoma of breast (ICD-O-3.2 term) | 8543/3 | Paget disease and intraductal carcinoma of breast (Preferred) | Paget disease and intraductal carcinoma of breast | not_reported | picker |  |
| Acinar cell carcinoma (ICD-O-3.2 term) | 8550/3 | Acinar cell carcinoma (Preferred) | Acinar cell carcinoma | not_reported | picker | Hernandez-Prera 2022, PDF p. 7; Pfister 2022, PDF p. 14 |
| Acinar cell cystadenocarcinoma (ICD-O-3.2 term) | 8551/3 | Acinar cell cystadenocarcinoma (Preferred) | Acinar cell cystadenocarcinoma | not_reported | picker |  |
| Mixed acinar-ductal carcinoma (ICD-O-3.2 term) | 8552/3 | Mixed acinar-ductal carcinoma (Preferred) | Mixed acinar-ductal carcinoma | not_reported | picker |  |
| Adenosquamous carcinoma (ICD-O-3.2 term) | 8560/3 | Adenosquamous carcinoma (Preferred) | Adenosquamous carcinoma | not_reported | picker |  |
| Epithelial-myoepithelial carcinoma (ICD-O-3.2 term) | 8562/3 | Epithelial-myoepithelial carcinoma (Preferred) | Epithelial-myoepithelial carcinoma | not_reported | picker |  |
| Adenocarcinoma with squamous metaplasia (ICD-O-3.2 term) | 8570/3 | Adenocarcinoma with squamous metaplasia (Preferred) | Adenocarcinoma with squamous metaplasia | not_reported | picker |  |
| Adenocarcinoma with cartilaginous and osseous metaplasia (ICD-O-3.2 term) | 8571/3 | Adenocarcinoma with cartilaginous and osseous metaplasia (Preferred) | Adenocarcinoma with cartilaginous and osseous metaplasia | not_reported | picker |  |
| Adenocarcinoma with spindle cell metaplasia (ICD-O-3.2 term) | 8572/3 | Adenocarcinoma with spindle cell metaplasia (Preferred) | Adenocarcinoma with spindle cell metaplasia | not_reported | picker |  |
| Adenocarcinoma with apocrine metaplasia (ICD-O-3.2 term) | 8573/3 | Adenocarcinoma with apocrine metaplasia (Preferred) | Adenocarcinoma with apocrine metaplasia | not_reported | picker |  |
| Adenocarcinoma with neuroendocrine differentiation (ICD-O-3.2 term) | 8574/3 | Adenocarcinoma with neuroendocrine differentiation (Preferred) | Adenocarcinoma with neuroendocrine differentiation | not_reported | picker |  |
| Metaplastic carcinoma, NOS (ICD-O-3.2 term) | 8575/3 | Metaplastic carcinoma, NOS (Preferred) | Metaplastic carcinoma, NOS | not_reported | picker |  |
| Hepatoid adenocarcinoma (ICD-O-3.2 term) | 8576/3 | Hepatoid adenocarcinoma (Preferred) | Hepatoid adenocarcinoma | not_reported | picker |  |
| Thymoma, NOS (ICD-O-3.2 term) | 8580/3 | Thymoma, NOS (Preferred) | Thymoma, NOS | not_reported | picker |  |
| Thymoma, type A (ICD-O-3.2 term) | 8581/3 | Thymoma, type A (Preferred) | Thymoma, type A | not_reported | picker |  |
| Thymoma, type AB (ICD-O-3.2 term) | 8582/3 | Thymoma, type AB (Preferred) | Thymoma, type AB | not_reported | picker |  |
| Thymoma, type B1 (ICD-O-3.2 term) | 8583/3 | Thymoma, type B1 (Preferred) | Thymoma, type B1 | not_reported | picker |  |
| Thymoma, type B2 (ICD-O-3.2 term) | 8584/3 | Thymoma, type B2 (Preferred) | Thymoma, type B2 | not_reported | picker |  |
| Thymoma, type B3 (ICD-O-3.2 term) | 8585/3 | Thymoma, type B3 (Preferred) | Thymoma, type B3 | not_reported | picker |  |
| Thymic carcinoma, NOS (ICD-O-3.2 term) | 8586/3 | Thymic carcinoma, NOS (Preferred) | Thymic carcinoma, NOS | not_reported | picker |  |
| Intrathyroid thymic carcinoma (ICD-O-3.2 term) | 8589/3 | Intrathyroid thymic carcinoma (Preferred) | Intrathyroid thymic carcinoma | not_reported | picker |  |
| Carcinoma ex pleomorphic adenoma (ICD-O-3.2 term) | 8941/3 | Carcinoma ex pleomorphic adenoma (Preferred) | Carcinoma ex pleomorphic adenoma | not_reported | picker |  |
| Adenomyoepithelioma with carcinoma (ICD-O-3.2 term) | 8983/3 | Adenomyoepithelioma with carcinoma (Preferred) | Adenomyoepithelioma with carcinoma | not_reported | picker |  |
| Brenner tumor, malignant (ICD-O-3.2 term) | 9000/3 | Brenner tumor, malignant (Preferred) | Brenner tumor, malignant | not_reported | picker |  |
| Serous adenocarcinofibroma (ICD-O-3.2 term) | 9014/3 | Serous adenocarcinofibroma (Preferred) | Serous adenocarcinofibroma | not_reported | picker |  |
| Phyllodes tumor, malignant (ICD-O-3.2 term) | 9020/3 | Phyllodes tumor, malignant (Preferred) | Phyllodes tumor, malignant | not_reported | picker |  |

Why, for the entities with their own decision:

- **Parathyroid carcinoma (8140/3).** The only malignant parathyroid entity in the WHO 5th-edition table (ICCR Parathyroid 2025 Table 1, PDF p. 9). The WHO paediatric volume lists parathyroid endocrine tumours (Pfister 2022 Table 3, PDF p. 14) without naming carcinoma, and lists hyperparathyroidism-jaw tumour syndrome among the paediatric predisposition syndromes (Pfister 2022, PDF p. 19), which carries a lifetime risk of parathyroid carcinoma (ICCR, PDF p. 5). At the other sites of this part 8140/3 Adenocarcinoma, NOS sits in the picker. Registrar question 1.
- **Atypical parathyroid tumour (8140/1).** A neoplasm of uncertain malignant potential with worrying features and no invasion; it replaces atypical parathyroid adenoma (Erickson 2022, PDF pp. 1 and 12). Behaviour /1 is outside Group XI.
- **Parathyroid adenoma (8140/0).** Benign. Listed in the WHO paediatric volume (Pfister 2022 Table 3, PDF p. 14). Multiglandular parathyroid disease is multiple adenomas (Erickson 2022, PDF p. 1). ICD-O-3.2 also holds 8321/0 Chief cell adenoma (C75.0), 8290/0 Oxyphilic adenoma and 8322/0 Water-clear cell adenoma (C75.0) for the adenoma subtypes; all are /0 and excluded the same way.
- **Chief cell adenoma (ICD-O-3.2 term for chief cell parathyroid adenoma) (8321/0).** ICD-O-3.2 ties it to the parathyroid gland (C75.0). REDCap offers 8321 in XIf with no malignant form (currency check section 5). The tree reaches it through the parathyroid adenoma answer.
- **Parathyroid lipoadenoma (8324/0).** Benign (ICCR Parathyroid 2025 Table 1, PDF p. 9). REDCap offers 8324 in XIb and XIf with no malignant form (currency check section 5).
- **Carcinoma of unknown primary; carcinoma with no type named (8010/3).** ICD-O-3 gives C80.9 with 8010/3 for a carcinoma that has spread and whose site of origin is unknown (WHO ICD-O-3.1 manual, PDF p. 6). It is the fallback answer on cu_histology and cu_cytology. True carcinoma of unknown primary is under 3% of the cases first presented as one (Hernandez-Prera 2022, PDF p. 8). No source here gives its frequency in children. In the picker at the other sites.
- **Heterotopia-associated carcinoma (8010/3).** A carcinoma arising in heterotopic thyroid or salivary tissue, after a primary carcinoma at the usual site is excluded (Hernandez-Prera 2022, PDF p. 2). Thyroid-type cases lie in the midline along the thyroglossal duct and are mostly papillary thyroid carcinoma, at ages 9 to 83 (PDF p. 6): they belong to the thyroid tree. Salivary-type cases lie in neck lymph nodes and are subtyped as salivary carcinomas (PDF p. 7). Their topography and code wait on the registrar (registrar question 5).
- **Papillary thyroid carcinoma in a neck lymph node, primary not found (8260/3).** ICD-O-3.2 prints C73.9 beside Papillary carcinoma of thyroid, so Rule H records the thyroid when no primary is named. Follicular cells are not present in the lateral neck (Hernandez-Prera 2022, PDF p. 6). Coded from the thyroid tree (XIb) after the site is recaptured.
- **Nasopharyngeal carcinoma in a neck lymph node (Schmincke tumour) (8082/3).** A report that names nasopharyngeal carcinoma names the primary site; ICD-O-3.2 prints C11 beside Schmincke tumor. EBER in a neck node carcinoma correlates with a nasopharyngeal origin (Hernandez-Prera 2022, PDF p. 8). Nasopharyngeal carcinoma is in the WHO paediatric volume (Pfister 2022 Table 3, PDF p. 14). Coded from the nasopharynx tree (XIc).
- **Pseudomyxoma peritonei (8480/6).** Behaviour /6 (metastatic) is not used by cancer registries (WHO ICD-O-3.1 manual, PDF p. 6): the case is coded at its source organ, or, when no source is found, as 8480/3 Pseudomyxoma peritonei with unknown primary site at C80.9.
- **Mesothelioma (malignant; epithelioid 9052/3, biphasic 9053/3, sarcomatoid 9051/3) (9050/3).** ICCC-2017 places 9050-9055/3 in XIIa5 at every site. The WHO paediatric volume lists mesothelial tumours of the peritoneum (Pfister 2022 Table 3, PDF p. 13).
- **Peritoneal inclusion cyst (multicystic mesothelioma) (9055/0).** Benign; ICD-O-3.2 ties it to the peritoneum (C48._) and lists cystic and multicystic mesothelioma as synonyms. In the WHO paediatric volume (Pfister 2022 Table 3, PDF p. 13).
- **Well-differentiated papillary mesothelioma of the peritoneum (9052/0).** ICD-O-3.2 gives the peritoneal tumour 9052/0 and keeps 9052/1 for the pleura (C38.4). Neither is /3, so it is excluded whichever applies (data gap 3).
- **Desmoplastic small round cell tumour (8806/3).** ICCC-2017 places 8806 in IXd11 at every site. In the WHO paediatric volume (Pfister 2022, PDF p. 9).
- **Carotid body paraganglioma (8692/3).** ICCC-2017 places 8680-8683, 8690-8693 and 8700 in IVb at every site. Head and neck (parasympathetic) paraganglioma is in the WHO paediatric volume (Pfister 2022 Table 3, PDF p. 14).
- **Aortic body paraganglioma (8691/3).** ICCC-2017 IVb at every site. Paragangliomas are in the WHO paediatric volume (Pfister 2022 Table 3, PDF p. 14).
- **Extra-adrenal paraganglioma (sympathetic paraganglioma) (8693/3).** ICCC-2017 IVb at every site. Sympathetic paraganglioma is in the WHO paediatric volume (Pfister 2022 Table 3, PDF p. 14).
- **Craniopharyngioma (9350/1).** ICD-O-3.2 ties it to the craniopharyngeal duct (C75.2). ICCC-2017 places 9350-9352 in IIIe2 at every site with behaviours 0, 1 and 3. Adamantinomatous craniopharyngioma is in the WHO paediatric volume (Pfister 2022 Table 4, PDF p. 18).
- **Pituitary blastoma (8273/3).** New in ICD-O-3.2 (C75.1); ICCC-2017 IIIe1 at every site (currency check section 6). In the WHO paediatric volume (Pfister 2022, PDF p. 18). Listed here because the endocrine site screen meets it.
- **Pituitary carcinoma (8272/3).** ICCC-2017 IIIe1 at every site. The currency check (section 2) names 8272/3 as the current term for the obsolete 8280/3, 8281/3 and 8300/3 at C75.1 and routes C75.1 to Group III.
- **Choroid plexus carcinoma (9390/3).** ICCC-2017 IIIa2 at every site. In the WHO paediatric volume (Pfister 2022 Table 4, PDF p. 17).
- **Hepatocellular carcinoma presenting with no primary site named (8170/3).** ICD-O-3.2 ties it to the liver (C22.0), so Rule H records the liver; ICCC-2017 places 8170-8180 in VIIb at every site. Paediatric hepatocellular carcinoma is in the WHO paediatric volume (Pfister 2022 Table 3, PDF p. 13).
- **Seromucinous carcinoma (8474/3).** ICCC-2017 places 8474 in Xd at every site (000-809), not in XIf10. The currency check (section 6) lists 8474/3 under XIf10; the ICCC-2017 range says Group X (conflict 7).

The picker holds 162 picker entities plus Carcinoma, NOS and Adenocarcinoma, NOS: every current code ICCC-2017 places in XIf10 at these sites and in XIf11 at C76 and C80.9. 10 codes have no current /3 term and are not built. Picker entities with a note:

- **Carcinoma, undifferentiated, NOS (8020/3).** Named with squamous cell and neuroendocrine morphology as a carcinoma of unknown primary type (Hernandez-Prera 2022, PDF p. 8). ICD-O-3.2 lists Carcinoma, poorly differentiated, NOS as a related term of this code.
- **Squamous cell carcinoma, NOS (8070/3).** The WHO head and neck volume names squamous cell, undifferentiated and neuroendocrine morphology as the carcinoma of unknown primary types that need high-risk human papillomavirus testing (Hernandez-Prera 2022, PDF p. 8). No source here reports these in children; the registrar decides whether they become options on cu_histology (registrar question 6).
- **Squamous cell carcinoma, large cell, nonkeratinizing, NOS (8072/3).** A non-keratinizing carcinoma in a neck lymph node that is EBER positive points to the nasopharynx (Hernandez-Prera 2022, PDF p. 8), and nasopharyngeal carcinoma occurs in children (Pfister 2022 Table 3, PDF p. 14). At the nasopharynx it is coded from the nasopharynx tree; at C80.9 it stays here until the registrar rules (registrar question 4).
- **Lymphoepithelial carcinoma (8082/3).** Schmincke tumor, a related term of this code, carries the nasopharynx (C11) and is handled on cu_histology by Rule H. Lymphoepithelial carcinoma in a neck node with no primary named stays at C80.9 until the registrar rules (registrar question 4).
- **Squamous cell carcinoma, HPV positive (8085/3).** New in ICD-O-3.2; REDCap lacks it (currency check section 6). p16 is a sensitive surrogate of high-risk human papillomavirus (Hernandez-Prera 2022, PDF p. 8).
- **Squamous cell carcinoma, HPV negative (8086/3).** New in ICD-O-3.2; REDCap lacks it (currency check section 6).
- **ACTH-producing tumor (8158/3).** ICCC-2017 places 8158 at C75.1 in Group III (IIIe1), and its XIf10 range leaves out C70-C72, where no ICCC-2017 range holds it; the option is not offered at C70-C72. Its REDCap label is the [obs] term Endocrine tumor, functioning, NOS (currency check section 4).
- **Neuroendocrine tumor, NOS (8240/3).** At C80.9 it is also the tissue-free code for deposits on imaging with a raised chromogranin A (cu_lab, Visser 2023 Table 4 as the registrar gave it).
- **Neuroendocrine carcinoma, NOS (8246/3).** Named with squamous cell and undifferentiated morphology as a carcinoma of unknown primary type (Hernandez-Prera 2022, PDF p. 8).
- **Merkel cell carcinoma (8247/3).** ICD-O-3.2 ties Merkel cell carcinoma to the skin (C44). With no primary site found, Rule H records the skin; the cu_histology hint says so.
- **Papillary adenocarcinoma, NOS (8260/3).** Papillary carcinoma of thyroid, a related term, carries C73.9 and is handled on cu_histology by Rule H, so it is left out of this option's search terms. A papillary thyroid carcinoma in the lateral neck is a thyroid deposit, because follicular cells are not present there (Hernandez-Prera 2022, PDF p. 6).
- **Oxyphilic adenocarcinoma (8290/3).** ICCC-2017 places 8290 at C75.1 in Group III (IIIe1), and its XIf10 range leaves out C70-C72, where no ICCC-2017 range holds it; the option is not offered at C70-C72.
- **Water-clear cell adenocarcinoma (8322/3).** ICD-O-3.2 ties Water-clear cell adenocarcinoma to the parathyroid gland (C75.0). The WHO 5th-edition parathyroid table prints only 8140/3 for parathyroid carcinoma (ICCR Parathyroid 2025, PDF p. 9); the WHO overview describes water-clear cells only in adenomas (Erickson 2022, PDF p. 6). Registrar question 2.
- **Mucoepidermoid carcinoma (8430/3).** Heterotopia-associated salivary carcinoma in a neck lymph node is most often mucoepidermoid or acinic cell carcinoma (Hernandez-Prera 2022, PDF p. 7); mucoepidermoid carcinoma occurs in children at the salivary glands (Pfister 2022 Table 3, PDF p. 14). The topography of an intranodal case waits on the registrar (registrar question 5).
- **Serous carcinoma, NOS (8441/3).** Serous carcinoma at the peritoneum belongs here only when the report says it began in the peritoneum; at the ovary it is Group X (ICCC-2017 Xd at C56.9).
- **Low grade serous carcinoma (8460/3).** ICD-O-3.2 ties Low grade serous carcinoma to the ovary (C56.9). At the peritoneum it belongs here only when the report says it began there (Rule H); at the ovary it is Group X.
- **High grade serous carcinoma (8461/3).** ICD-O-3.2 ties High grade serous carcinoma to the ovary (C56.9). At the peritoneum it belongs here only when the report says it began there (Rule H); at the ovary it is Group X.
- **Mucinous adenocarcinoma (8480/3).** ICD-O-3.2 lists Pseudomyxoma peritonei with unknown primary site under this code at C80.9. Its obsolete synonyms (Gelatinous, Mucous) are left out of the search terms.
- **Acinar cell carcinoma (8550/3).** Acinic cell carcinoma is the second common type of heterotopia-associated salivary carcinoma (Hernandez-Prera 2022, PDF p. 7) and occurs in children at the salivary glands (Pfister 2022 Table 3, PDF p. 14). Topography waits on the registrar (registrar question 5).

## 3 The pathway

The search box captures the site first; each site family then opens on its own evidence gate (`pt_` parathyroid, `en_` other endocrine sites, `cn_` central nervous system, `pe_` peritoneum and retroperitoneum, `cu_` ill-defined sites and unknown primary). `ou_cytology` and `ou_picker` are shared. A deposit answer refers with `recapture_site` true and records nothing here.

### `pt_evidence` (document_inventory)

**What is in the file for this parathyroid tumour?**

Hint: A parathyroidectomy or another resection report counts as histology. An immunohistochemistry or gene report on its own does not stand in for a histology report. Serum calcium and parathyroid hormone results do not register a carcinoma.

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| A referral letter or clinical note only, with no imaging report and no tissue | go | go `pt_clinical`, basis 1 |  |  |
| An imaging report, with or without serum calcium and parathyroid hormone results, and no tissue | go | go `pt_imaging`, basis 2 |  | ICCR Parathyroid 2025, PDF p. 5 |
| Cytology only: a fine-needle aspirate and no tissue | go | go `pt_cytology`, basis 5 |  | ICCR Parathyroid 2025, PDF p. 6 |
| A histology report: parathyroidectomy or another resection, with or without immunohistochemistry or gene reports | go | go `pt_histology`, basis 7 |  | ICCR Parathyroid 2025, PDF p. 6 |

### `pt_clinical` (clinical_alias)

**What does the referral letter or clinical note say?**

Hint: High serum calcium and parathyroid hormone raise the question of carcinoma. They do not establish it: the diagnosis is made on the resection specimen.

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| The referral letter or clinical note states parathyroid carcinoma as the diagnosis, for example with deposits in the lungs or bones | refer | Group 12; 8000/3 basis 1 | A diagnosis resting on clinical information alone is registered as Neoplasm, malignant (8000/3). ICCC-3 places 8000/3 at the parathyroid gland in Group XII, so the case is coded from the Group XII tree. | ICCR Parathyroid 2025, PDF p. 6 |
| The referral letter or clinical note says only possible or suspected parathyroid carcinoma, or reports high calcium or parathyroid hormone with no diagnosis | not_registrable | not registrable | Cancer is only possible on this evidence. A case that is only possibly cancer is not registered without pathology. | ICCR Parathyroid 2025, PDF p. 5; ICCR Parathyroid 2025, PDF p. 6 |
| The referral letter or clinical note names a parathyroid adenoma, parathyroid hyperplasia or hyperparathyroidism | not_registrable | not registrable | A parathyroid adenoma, hyperplasia or hyperparathyroidism is not a malignant tumour. Group XI registers malignant tumours only. | ICCR Parathyroid 2025, PDF p. 5 |
| A pathology report is in the file after all | go | go `pt_evidence` |  |  |

### `pt_imaging` (clinical_alias)

**What does the imaging report say?**

Hint: High serum calcium and parathyroid hormone raise the question of carcinoma. They do not establish it: the diagnosis is made on the resection specimen.

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| The imaging report states parathyroid carcinoma as the diagnosis, for example with deposits in the lungs or bones | refer | Group 12; 8000/3 basis 2 | A diagnosis resting on imaging alone is registered as Neoplasm, malignant (8000/3). ICCC-3 places 8000/3 at the parathyroid gland in Group XII, so the case is coded from the Group XII tree. | ICCR Parathyroid 2025, PDF p. 6 |
| The imaging report says only possible or suspected parathyroid carcinoma, or reports high calcium or parathyroid hormone with no diagnosis | not_registrable | not registrable | Cancer is only possible on this evidence. A case that is only possibly cancer is not registered without pathology. | ICCR Parathyroid 2025, PDF p. 5; ICCR Parathyroid 2025, PDF p. 6 |
| The imaging report names a parathyroid adenoma, parathyroid hyperplasia or hyperparathyroidism | not_registrable | not registrable | A parathyroid adenoma, hyperplasia or hyperparathyroidism is not a malignant tumour. Group XI registers malignant tumours only. | ICCR Parathyroid 2025, PDF p. 5 |
| A pathology report is in the file after all | go | go `pt_evidence` |  |  |

### `pt_cytology` (morphology_only)

**What does the cytology report say?**

Hint: A fine-needle aspirate of the parathyroid gland cannot show the invasion that defines carcinoma. Cytology of a deposit away from the gland can show a metastasis, which does.

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| Cytology of a deposit away from the parathyroid gland, which the report calls metastatic parathyroid carcinoma | code | 8140/3, basis 5 | Recorded as Adenocarcinoma, NOS (8140/3) at the parathyroid gland (C75.0). ICD-O-3.2 lists Parathyroid carcinoma under this code. A metastasis documented on cytology is one of the criteria for parathyroid carcinoma. | Erickson 2022, PDF p. 1; ICCR Parathyroid 2025, PDF p. 9 (table) |
| Cytology of the parathyroid gland itself, naming a parathyroid lesion, a parathyroid neoplasm or atypical cells | not_registrable | not registrable | Cytology of the gland cannot show the invasion that defines parathyroid carcinoma, so carcinoma is not established. Register the case when the resection report names carcinoma. | ICCR Parathyroid 2025, PDF p. 6; ICCR Parathyroid 2025, PDF p. 8 |
| Cytology names a carcinoma of another organ, such as the thyroid | refer | recapture site | A deposit is coded at the site where the tumour began. The next screen asks that site. | ICCR Parathyroid 2025, PDF p. 4 |

### `pt_histology` (histology_subclassification)

**What does the histology report call the parathyroid tumour?**

Hint: Use the diagnosis line of the report. Parathyroid carcinoma requires invasion or a metastasis. A tumour with worrying features and no invasion is an atypical parathyroid tumour. A report that adds the words parafibromin-deficient still names one of these diagnoses: choose that diagnosis. When one tumour carries two type names and no single answer names both, choose the higher code number.

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| Parathyroid carcinoma | code | 8140/3, basis 7 | Recorded as Adenocarcinoma, NOS (8140/3). ICD-O-3.2 lists Parathyroid carcinoma as a related term of this code, at the parathyroid gland (C75.0). *Recognition aid:* The report describes invasion of a blood vessel, a lymphatic, a nerve or a neighbouring structure, or a metastasis. | ICCR Parathyroid 2025, PDF p. 9 (table); ICCR Parathyroid 2025, PDF p. 8; Erickson 2022, PDF p. 8 |
| Atypical parathyroid tumour (also written atypical parathyroid neoplasm, or parathyroid tumour of low or uncertain malignant potential; formerly atypical parathyroid adenoma) | exclude | excluded 8140/1 | Atypical parathyroid tumour is recorded by ICD-O-3.2 as Atypical adenoma (8140/1), which is not malignant. Group XI registers malignant tumours only. *Recognition aid:* The report lists worrying features, such as fibrous bands, mitoses or necrosis, and finds no invasion. | ICCR Parathyroid 2025, PDF p. 9 (table); ICCR Parathyroid 2025, PDF p. 8; Erickson 2022, PDF p. 1; Erickson 2022, PDF p. 12 |
| Parathyroid adenoma, in one gland or in several glands (multiglandular parathyroid disease); chief cell, oncocytic or water-clear cell adenoma | exclude | excluded 8140/0 | Parathyroid adenoma is recorded by ICD-O-3.2 as Adenoma, NOS (8140/0), which is not malignant. Group XI registers malignant tumours only. | ICCR Parathyroid 2025, PDF p. 9 (table); Erickson 2022, PDF p. 1; Pfister 2022, PDF p. 14 |
| Parathyroid lipoadenoma | exclude | excluded 8324/0 | Parathyroid lipoadenoma is recorded by ICD-O-3.2 as Lipoadenoma (8324/0), which is not malignant. Group XI registers malignant tumours only. | ICCR Parathyroid 2025, PDF p. 9 (table) |
| Parathyroid hyperplasia, including hyperplasia with kidney failure | not_registrable | not registrable | Parathyroid hyperplasia is not a tumour. It is not registered. | Erickson 2022, PDF p. 1 |
| Lymphoma | refer | Group 2 | Lymphomas are coded in Group II, Lymphomas and reticuloendothelial neoplasms. | ICCR Parathyroid 2025, PDF p. 4 |
| Sarcoma | refer | Group 9 | Sarcomas are coded in Group IX, Soft-tissue and other extraosseous sarcomas. | ICCR Parathyroid 2025, PDF p. 4 |
| A deposit (metastasis) of a tumour that began elsewhere, or a tumour of the thyroid | refer | recapture site | A deposit is coded at the site where the tumour began. The next screen asks that site. | ICCR Parathyroid 2025, PDF p. 4; Erickson 2022, PDF p. 13 |
| Another carcinoma the report names | go | go `ou_picker` |  |  |

### `en_evidence` (document_inventory)

**What is in the file for this tumour of an endocrine site (craniopharyngeal duct, carotid body, aortic body or another endocrine gland)?**

Hint: An immunohistochemistry or gene report on its own does not stand in for a histology report.

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| A referral letter or clinical note only, with no imaging report and no tissue | go | go `en_clinical`, basis 1 |  |  |
| An imaging report only, with no tissue | go | go `en_imaging`, basis 2 |  |  |
| Cytology only: a fine-needle aspirate, a smear or a fluid sample, and no tissue | go | go `ou_cytology`, basis 5 |  |  |
| A histology report: biopsy or resection, with or without immunohistochemistry or gene reports | go | go `en_histology`, basis 7 |  |  |

### `en_clinical` (clinical_alias)

**What does the referral letter or clinical note say?**

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| A paraganglioma, a carotid body tumour or a glomus tumour | refer | Group 4 | Paragangliomas are coded in Group IV, Neuroblastoma and other peripheral nervous cell tumours, at every site. | Pfister 2022, PDF p. 14 |
| A craniopharyngioma, or another tumour at the craniopharyngeal duct | refer | Group 3; 8000/3 basis 1 | A diagnosis resting on clinical information alone is registered as Neoplasm, malignant (8000/3). ICCC-3 places 8000/3 at the craniopharyngeal duct in Group III, so the case is coded from the Group III tree. A craniopharyngioma is also coded in Group III. | Pfister 2022, PDF p. 18 |
| The referral letter or clinical note states a malignant tumour of the carotid body, aortic body or another endocrine gland, type not named | refer | Group 12; 8000/3 basis 1 | A diagnosis resting on clinical information alone is registered as Neoplasm, malignant (8000/3). ICCC-3 places 8000/3 at these endocrine sites in Group XII, so the case is coded from the Group XII tree. |  |
| The referral letter or clinical note says only possible or suspected | not_registrable | not registrable | Cancer is only possible on this evidence. A case that is only possibly cancer is not registered without pathology. |  |
| A deposit (metastasis) of a cancer the file names elsewhere | refer | recapture site | A deposit is coded at the site where the tumour began. The next screen asks that site. | WHO ICD-O-3.1 manual, PDF p. 7 |
| A pathology report is in the file after all | go | go `en_evidence` |  |  |

### `en_imaging` (clinical_alias)

**What does the imaging report say?**

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| A paraganglioma, a carotid body tumour or a glomus tumour | refer | Group 4 | Paragangliomas are coded in Group IV, Neuroblastoma and other peripheral nervous cell tumours, at every site. | Pfister 2022, PDF p. 14 |
| A craniopharyngioma, or another tumour at the craniopharyngeal duct | refer | Group 3; 8000/3 basis 2 | A diagnosis resting on imaging alone is registered as Neoplasm, malignant (8000/3). ICCC-3 places 8000/3 at the craniopharyngeal duct in Group III, so the case is coded from the Group III tree. A craniopharyngioma is also coded in Group III. | Pfister 2022, PDF p. 18 |
| The imaging report states a malignant tumour of the carotid body, aortic body or another endocrine gland, type not named | refer | Group 12; 8000/3 basis 2 | A diagnosis resting on imaging alone is registered as Neoplasm, malignant (8000/3). ICCC-3 places 8000/3 at these endocrine sites in Group XII, so the case is coded from the Group XII tree. |  |
| The imaging report says only possible or suspected | not_registrable | not registrable | Cancer is only possible on this evidence. A case that is only possibly cancer is not registered without pathology. |  |
| A deposit (metastasis) of a cancer the file names elsewhere | refer | recapture site | A deposit is coded at the site where the tumour began. The next screen asks that site. | WHO ICD-O-3.1 manual, PDF p. 7 |
| A pathology report is in the file after all | go | go `en_evidence` |  |  |

### `en_histology` (histology_subclassification)

**What does the histology report call the tumour?**

Hint: The carotid body and the aortic body are paraganglia. A pituitary or pineal tumour belongs to the central nervous system group.

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| Paraganglioma, including carotid body paraganglioma (carotid body tumour) and aortic body paraganglioma | refer | Group 4 | Paragangliomas are coded in Group IV, Neuroblastoma and other peripheral nervous cell tumours, at every site. | Pfister 2022, PDF p. 14 |
| Craniopharyngioma | refer | Group 3 | Craniopharyngioma is coded in Group III, Central nervous system and miscellaneous intracranial and intraspinal neoplasms. | Pfister 2022, PDF p. 18 |
| A pituitary tumour (pituitary neuroendocrine tumour, pituitary blastoma, pituitary carcinoma) or a pineal tumour | refer | Group 3 | Pituitary and pineal tumours are coded in Group III, Central nervous system and miscellaneous intracranial and intraspinal neoplasms. | Pfister 2022, PDF p. 18 |
| A deposit (metastasis) of a tumour that began elsewhere | refer | recapture site | A deposit is coded at the site where the tumour began. The next screen asks that site. | WHO ICD-O-3.1 manual, PDF p. 7 |
| Another carcinoma the report names | go | go `ou_picker` |  |  |

### `cn_evidence` (document_inventory)

**What is in the file for this carcinoma in the brain, spinal cord or meninges?**

Hint: An immunohistochemistry or gene report on its own does not stand in for a histology report.

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| A referral letter or clinical note only, with no imaging report and no tissue | go | go `cn_clinical`, basis 1 |  |  |
| An imaging report only, with no tissue | go | go `cn_imaging`, basis 2 |  |  |
| Cytology only: a fine-needle aspirate, a smear or a fluid sample, and no tissue | go | go `ou_cytology`, basis 5 |  |  |
| A histology report: biopsy or resection, with or without immunohistochemistry or gene reports | go | go `cn_histology`, basis 7 |  |  |

### `cn_clinical` (clinical_alias)

**What does the referral letter or clinical note say?**

Hint: ICD-O records the site where a tumour began.

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| Deposits (metastases) of a cancer the file names elsewhere | refer | recapture site | A deposit is coded at the site where the tumour began. The next screen asks that site. | WHO ICD-O-3.1 manual, PDF p. 7 |
| Deposits of a cancer whose primary site was not found | refer | recapture site | A carcinoma whose primary site was not found is recorded at Primary site not found (C80.9). Choose Primary site not found on the next screen. | WHO ICD-O-3.1 manual, PDF p. 6 |
| A primary tumour of the brain, spinal cord or meninges | refer | Group 3; 8000/3 basis 1 | A diagnosis resting on clinical information alone is registered as Neoplasm, malignant (8000/3). ICCC-3 places 8000/3 at the brain, spinal cord and meninges in Group III, so the case is coded from the Group III tree. |  |
| The referral letter or clinical note says only possible or suspected | not_registrable | not registrable | Cancer is only possible on this evidence. A case that is only possibly cancer is not registered without pathology. |  |
| A pathology report is in the file after all | go | go `cn_evidence` |  |  |

### `cn_imaging` (clinical_alias)

**What does the imaging report say?**

Hint: ICD-O records the site where a tumour began.

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| Deposits (metastases) of a cancer the file names elsewhere | refer | recapture site | A deposit is coded at the site where the tumour began. The next screen asks that site. | WHO ICD-O-3.1 manual, PDF p. 7 |
| Deposits of a cancer whose primary site was not found | refer | recapture site | A carcinoma whose primary site was not found is recorded at Primary site not found (C80.9). Choose Primary site not found on the next screen. | WHO ICD-O-3.1 manual, PDF p. 6 |
| A primary tumour of the brain, spinal cord or meninges | refer | Group 3; 8000/3 basis 2 | A diagnosis resting on imaging alone is registered as Neoplasm, malignant (8000/3). ICCC-3 places 8000/3 at the brain, spinal cord and meninges in Group III, so the case is coded from the Group III tree. |  |
| The imaging report says only possible or suspected | not_registrable | not registrable | Cancer is only possible on this evidence. A case that is only possibly cancer is not registered without pathology. |  |
| A pathology report is in the file after all | go | go `cn_evidence` |  |  |

### `cn_histology` (histology_subclassification)

**What does the report say about the carcinoma in the brain, spinal cord or meninges?**

Hint: ICD-O records the site where a tumour began. A carcinoma found in the brain, spinal cord or meninges is recorded at the organ where it began, unless the report states that it began here.

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| A deposit (metastasis) of a carcinoma that began in an organ the file names | refer | recapture site | A deposit is coded at the site where the tumour began. The next screen asks that site. | WHO ICD-O-3.1 manual, PDF p. 7; WHO ICD-O-3.1 manual, PDF p. 2 |
| A deposit of carcinoma, and no primary site was found | refer | recapture site | A carcinoma whose primary site was not found is recorded at Primary site not found (C80.9). Choose Primary site not found on the next screen. | WHO ICD-O-3.1 manual, PDF p. 6 |
| Choroid plexus carcinoma | refer | Group 3 | Choroid plexus carcinoma is coded in Group III, Central nervous system and miscellaneous intracranial and intraspinal neoplasms. | Pfister 2022, PDF p. 17 |
| Craniopharyngioma, a pituitary tumour, or a papillary tumour of the pineal region | refer | Group 3 | These tumours are coded in Group III, Central nervous system and miscellaneous intracranial and intraspinal neoplasms. | Pfister 2022, PDF p. 18 |
| The report states that the carcinoma began in the brain, spinal cord or meninges | go | go `ou_picker` |  |  |

### `pe_evidence` (document_inventory)

**What is in the file for this tumour of the peritoneum or retroperitoneum?**

Hint: An immunohistochemistry or gene report on its own does not stand in for a histology report.

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| A referral letter or clinical note only, with no imaging report and no tissue | go | go `pe_clinical`, basis 1 |  |  |
| An imaging report only, with no tissue | go | go `pe_imaging`, basis 2 |  |  |
| Cytology only: a fine-needle aspirate, a smear or a fluid sample, and no tissue | go | go `ou_cytology`, basis 5 |  |  |
| A histology report: biopsy or resection, with or without immunohistochemistry or gene reports | go | go `pe_histology`, basis 7 |  |  |

### `pe_clinical` (clinical_alias)

**What does the referral letter or clinical note say?**

Hint: Tissue around the pancreas, the adrenal gland or the caecum is retroperitoneum (C48.0).

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| Deposits spread over the peritoneum from a cancer the file names elsewhere | refer | recapture site | A deposit is coded at the site where the tumour began. The next screen asks that site. | WHO ICD-O-3.1 manual, PDF p. 7 |
| The referral letter or clinical note states a malignant tumour of the peritoneum or retroperitoneum, type not named | refer | Group 12; 8000/3 basis 1 | A diagnosis resting on clinical information alone is registered as Neoplasm, malignant (8000/3). ICCC-3 places 8000/3 at the peritoneum and retroperitoneum in Group XII, so the case is coded from the Group XII tree. |  |
| The referral letter or clinical note says only possible or suspected | not_registrable | not registrable | Cancer is only possible on this evidence. A case that is only possibly cancer is not registered without pathology. |  |
| A pathology report is in the file after all | go | go `pe_evidence` |  |  |

### `pe_imaging` (clinical_alias)

**What does the imaging report say?**

Hint: Tissue around the pancreas, the adrenal gland or the caecum is retroperitoneum (C48.0).

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| Deposits spread over the peritoneum from a cancer the file names elsewhere | refer | recapture site | A deposit is coded at the site where the tumour began. The next screen asks that site. | WHO ICD-O-3.1 manual, PDF p. 7 |
| The imaging report states a malignant tumour of the peritoneum or retroperitoneum, type not named | refer | Group 12; 8000/3 basis 2 | A diagnosis resting on imaging alone is registered as Neoplasm, malignant (8000/3). ICCC-3 places 8000/3 at the peritoneum and retroperitoneum in Group XII, so the case is coded from the Group XII tree. |  |
| The imaging report says only possible or suspected | not_registrable | not registrable | Cancer is only possible on this evidence. A case that is only possibly cancer is not registered without pathology. |  |
| A pathology report is in the file after all | go | go `pe_evidence` |  |  |

### `pe_histology` (histology_subclassification)

**What does the histology report call the tumour of the peritoneum or retroperitoneum?**

Hint: Tissue around the pancreas, the adrenal gland or the caecum is retroperitoneum (C48.0). A sarcoma, neuroblastoma, germ cell tumour or lymphoma of the retroperitoneum is coded in its own group: go back and search its name. ICD-O ties high-grade and low-grade serous carcinoma to the ovary: record the peritoneum only when the report says the tumour began in the peritoneum.

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| Mesothelioma (malignant mesothelioma; epithelioid, biphasic or sarcomatoid mesothelioma) | refer | Group 12 | Mesothelioma is coded in Group XII, Other and unspecified malignant neoplasms, at every site. | Pfister 2022, PDF p. 13 |
| Peritoneal inclusion cyst (also called multicystic or cystic mesothelioma) | exclude | excluded 9055/0 | Peritoneal inclusion cyst is recorded by ICD-O-3.2 as Peritoneal inclusion cysts (9055/0), which is not malignant. Group XI registers malignant tumours only. | Pfister 2022, PDF p. 13 |
| Well-differentiated papillary mesothelioma (well-differentiated papillary mesothelial tumour) of the peritoneum | exclude | excluded 9052/0 | Well-differentiated papillary mesothelioma of the peritoneum is recorded by ICD-O-3.2 as Epithelioid mesothelioma, benign (9052/0), which is not malignant. Group XI registers malignant tumours only. | Pfister 2022, PDF p. 13 |
| Desmoplastic small round cell tumour | refer | Group 9 | Desmoplastic small round cell tumour is coded in Group IX, Soft-tissue and other extraosseous sarcomas, at every site. | Pfister 2022, PDF p. 9 |
| Pseudomyxoma peritonei, or carcinoma spread over the peritoneum from an organ such as the appendix, ovary, stomach or bowel | refer | recapture site | Spread over the peritoneum is coded at the organ where the tumour began. The next screen asks that site. When the report finds no source organ, choose Primary site not found (C80.9): ICD-O-3.2 records Pseudomyxoma peritonei with unknown primary site at C80.9. | WHO ICD-O-3.1 manual, PDF p. 7; WHO ICD-O-3.1 manual, PDF p. 10 |
| Seromucinous carcinoma | refer | Group 10 | ICCC-3 places Seromucinous carcinoma (8474/3) in Group X, Germ cell, trophoblastic and gonadal neoplasms, at every site. |  |
| Another carcinoma the report names, which the report says began in the peritoneum or retroperitoneum | go | go `ou_picker` |  |  |

### `ou_cytology` (morphology_only)

**What does the cytology report say?**

Hint: Cerebrospinal fluid, ascitic fluid and fine-needle aspirates are cytology. Cells that are only atypical or suspicious do not establish cancer.

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| Carcinoma cells from a cancer the file names elsewhere | refer | recapture site | A deposit is coded at the site where the tumour began. The next screen asks that site. | WHO ICD-O-3.1 manual, PDF p. 7 |
| Carcinoma or malignant epithelial cells, and no primary site was found | refer | recapture site | A carcinoma whose primary site was not found is recorded at Primary site not found (C80.9). Choose Primary site not found on the next screen. | WHO ICD-O-3.1 manual, PDF p. 6 |
| Mesothelioma cells in peritoneal fluid | refer | Group 12 | Mesothelioma is coded in Group XII, Other and unspecified malignant neoplasms, at every site. | Pfister 2022, PDF p. 13 |
| A carcinoma the report says began at this site | go | go `ou_picker`, basis 5 |  |  |
| Atypical or suspicious cells only | not_registrable | not registrable | Cells that are only atypical or suspicious do not establish cancer. The case is not registered on this evidence. |  |

### `cu_evidence` (document_inventory)

**What is in the file for this carcinoma at an ill-defined site or with no primary site found?**

Hint: An immunohistochemistry or gene report on its own does not stand in for a histology report.

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| A referral letter or clinical note only, with no imaging report and no tissue | go | go `cu_clinical`, basis 1 |  |  |
| An imaging report only, with no tissue | go | go `cu_imaging`, basis 2 |  |  |
| Imaging that shows tumour deposits, with a raised chromogranin A or serotonin result, and no tissue | go | go `cu_lab`, basis 4 |  |  |
| Cytology only: a fine-needle aspirate, a smear or a fluid sample, and no tissue | go | go `cu_cytology`, basis 5 |  |  |
| A histology report: biopsy or resection of a lymph node, a deposit or a mass, with or without immunohistochemistry or gene reports | go | go `cu_primary`, basis 7 |  |  |

### `cu_clinical` (clinical_alias)

**What does the referral letter or clinical note say?**

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| The referral letter or clinical note names the organ where the cancer began | refer | recapture site | A deposit is coded at the site where the tumour began. The next screen asks that site. | WHO ICD-O-3.1 manual, PDF p. 7 |
| The referral letter or clinical note states a cancer whose primary site was not found | refer | Group 12; 8000/3 basis 1 | A diagnosis resting on clinical information alone is registered as Neoplasm, malignant (8000/3). ICCC-3 places 8000/3 at unknown primary site (C80.9) and at the ill-defined sites (C76) in Group XII, so the case is coded from the Group XII tree. | WHO ICD-O-3.1 manual, PDF p. 6 |
| The referral letter or clinical note says only possible or suspected | not_registrable | not registrable | Cancer is only possible on this evidence. A case that is only possibly cancer is not registered without pathology. |  |
| A pathology report is in the file after all | go | go `cu_evidence` |  |  |

### `cu_imaging` (clinical_alias)

**What does the imaging report say?**

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| The imaging report names the organ where the cancer began | refer | recapture site | A deposit is coded at the site where the tumour began. The next screen asks that site. | WHO ICD-O-3.1 manual, PDF p. 7 |
| The imaging report states a cancer whose primary site was not found | refer | Group 12; 8000/3 basis 2 | A diagnosis resting on imaging alone is registered as Neoplasm, malignant (8000/3). ICCC-3 places 8000/3 at unknown primary site (C80.9) and at the ill-defined sites (C76) in Group XII, so the case is coded from the Group XII tree. | WHO ICD-O-3.1 manual, PDF p. 6 |
| The imaging report says only possible or suspected | not_registrable | not registrable | Cancer is only possible on this evidence. A case that is only possibly cancer is not registered without pathology. |  |
| A pathology report is in the file after all | go | go `cu_evidence` |  |  |

### `cu_lab` (lab_results)

**Which raised result does the file give, with imaging that shows the tumour deposits?**

Hint: A raised marker counts only with imaging that shows the tumour. The primary site was not found.

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| Chromogranin A raised, and the clinician states a neuroendocrine tumour | code | 8240/3, basis 4 | Recorded as Neuroendocrine tumor, NOS (8240/3) at Primary site not found (C80.9). | Visser 2023 Table 4 (not in this file set) |
| Serotonin raised, and the clinician states a neuroendocrine tumour | code | 8241/3, basis 4 | Recorded as Enterochromaffin cell carcinoid (8241/3) at Primary site not found (C80.9). | Visser 2023 Table 4 (not in this file set) |
| A raised marker, and no imaging shows a tumour | not_registrable | not registrable | A tumour marker on its own does not register a tumour. | Visser 2023 Table 4 (not in this file set) |
| Another marker, or the clinician names no tumour type | go | go `cu_imaging`, basis 2 |  |  |

### `cu_cytology` (morphology_only)

**What does the cytology report say?**

Hint: Cells that are only atypical or suspicious do not establish cancer.

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| The cytology report or the clinician names the organ where the carcinoma began | refer | recapture site | A deposit is coded at the site where the tumour began. The next screen asks that site. | WHO ICD-O-3.1 manual, PDF p. 7 |
| Carcinoma or malignant epithelial cells, type not named, and no primary site was found | code | 8010/3, basis 5 | Recorded as Carcinoma, NOS (8010/3) at Primary site not found (C80.9). | WHO ICD-O-3.1 manual, PDF p. 6 |
| A named carcinoma type, such as squamous cell carcinoma or adenocarcinoma, and no primary site was found | go | go `ou_picker`, basis 5 |  |  |
| Malignant cells, not stated to be carcinoma | refer | Group 12; 8000/3 basis 5 | Recorded as Neoplasm, malignant (8000/3). ICCC-3 places 8000/3 at unknown primary site in Group XII, so the case is coded from the Group XII tree. |  |
| Atypical or suspicious cells only | not_registrable | not registrable | Cells that are only atypical or suspicious do not establish cancer. The case is not registered on this evidence. |  |

### `cu_primary` (site_resolution)

**Does the report or the treating clinician name the organ where the carcinoma began?**

Hint: A carcinoma in a lymph node or another organ is recorded at the organ where it began. Some tests point to an organ: Epstein-Barr virus encoded RNA (EBER) to the nasopharynx, p16 or high-risk human papillomavirus to the oropharynx, ultraviolet-signature mutations to the skin. Record that organ only when the report or the treating clinician names it as the primary site.

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| Yes: an organ is named, for example nasopharyngeal carcinoma, or carcinoma of the thyroid | refer | recapture site | A deposit is coded at the site where the tumour began. The next screen asks that site. *Recognition aid:* The report or the clinical note names the primary site, often after a test such as Epstein-Barr virus encoded RNA (EBER) or p16. | WHO ICD-O-3.1 manual, PDF p. 7; Hernandez-Prera 2022, PDF p. 8 (table) |
| The report places the tumour in a region of the body (neck, chest, abdomen, pelvis, arm or leg) and names no organ, tissue or lymph node | go | go `cu_region` |  | WHO ICD-O-3.1 manual, PDF p. 1 |
| No primary site was found: the carcinoma is in a lymph node or another organ as a deposit | go | go `cu_histology` |  *Recognition aid:* The report may say carcinoma of unknown primary, or metastatic carcinoma with the primary not identified after work-up. | WHO ICD-O-3.1 manual, PDF p. 6; Hernandez-Prera 2022, PDF p. 2 |

### `cu_region` (site_resolution)

**The report places the carcinoma in a region of the body. What does it say about the tissue?**

Hint: A region that names no tissue is coded to the tissue the tumour type implies. The chin and the forehead are skin. A site written with a prefix such as peri- or para-, or as the area or region of a site, is an ill-defined site unless the tumour type shows its tissue. One tumour crossing two or more regions, with no known starting point, is recorded at overlapping ill-defined sites (C76.8).

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| A squamous cell carcinoma or basal cell carcinoma of the skin of that region, or of the chin or forehead | refer | recapture site | A carcinoma of a region that names no tissue is coded to the tissue its type implies: a squamous cell carcinoma of the arm is skin of arm (C44.6), not arm (C76.4). The next screen asks the site: choose the skin of that region. | WHO ICD-O-3.1 manual, PDF p. 1; WHO ICD-O-3.1 manual, PDF p. 4 |
| A carcinoma in a lymph node of that region, such as a neck lymph node | refer | recapture site | A carcinoma in a lymph node is a deposit. The next screen asks the site: choose the organ the file names, or Primary site not found (C80.9). | WHO ICD-O-3.1 manual, PDF p. 6; WHO ICD-O-3.1 manual, PDF p. 7 |
| Beside or around an organ, or in the area or region of a site, and the tumour type does not show the tissue | go | go `cu_histology` | A site written with a prefix that ICD-O does not list is coded to the ill-defined site (C76) unless the tumour type shows its tissue. | WHO ICD-O-3.1 manual, PDF p. 1 |
| The region only, with no organ, tissue or lymph node named, for example carcinoma of the abdomen | go | go `cu_histology` |  | WHO ICD-O-3.1 manual, PDF p. 1; WHO ICD-O-3.1 manual, PDF p. 5 |

### `cu_histology` (histology_subclassification)

**What does the report call the carcinoma?**

Hint: When no primary site is found, a tumour name that ICD-O ties to one organ is recorded at that organ: papillary thyroid carcinoma at the thyroid, parathyroid carcinoma at the parathyroid gland, hepatocellular carcinoma at the liver, Merkel cell carcinoma at the skin, infiltrating duct carcinoma at the breast. First check that the report does not place the primary somewhere else.

| Answer | Outcome | Records | Reason | Page |
|---|---|---|---|---|
| Carcinoma with no type named: carcinoma, metastatic carcinoma, or malignant epithelial tumour | code | 8010/3, basis 7 | Recorded as Carcinoma, NOS (8010/3). | WHO ICD-O-3.1 manual, PDF p. 6 |
| Papillary thyroid carcinoma | refer | recapture site | ICD-O-3.2 ties Papillary carcinoma of thyroid to the thyroid gland (C73.9). With no other primary named, record the thyroid: choose Thyroid gland on the next screen. *Recognition aid:* A papillary thyroid carcinoma in a lymph node at the side of the neck is a deposit from the thyroid. | WHO ICD-O-3.1 manual, PDF p. 10; Hernandez-Prera 2022, PDF p. 6; Pfister 2022, PDF p. 14 |
| Nasopharyngeal carcinoma, or Schmincke tumour | refer | recapture site | The name places the primary in the nasopharynx, and ICD-O-3.2 ties Schmincke tumor to the nasopharynx (C11). Choose Nasopharynx on the next screen. | WHO ICD-O-3.1 manual, PDF p. 10; Pfister 2022, PDF p. 14; Hernandez-Prera 2022, PDF p. 8 |
| Parathyroid carcinoma | refer | recapture site | ICD-O-3.2 ties Parathyroid carcinoma to the parathyroid gland (C75.0). Choose Parathyroid gland on the next screen. | WHO ICD-O-3.1 manual, PDF p. 10; ICCR Parathyroid 2025, PDF p. 9 (table) |
| Hepatocellular carcinoma | refer | Group 7 | ICD-O-3.2 ties Hepatocellular carcinoma, NOS to the liver (C22.0). ICCC-3 places hepatocellular carcinoma in Group VII, Hepatic tumours, at every site. | WHO ICD-O-3.1 manual, PDF p. 10; Pfister 2022, PDF p. 13 |
| Melanoma | go | go `melanoma_tree` | Melanoma is coded from the melanoma tree. |  |
| Another carcinoma the report names, for example squamous cell carcinoma, adenocarcinoma, undifferentiated carcinoma or neuroendocrine carcinoma | go | go `ou_picker` |  | Hernandez-Prera 2022, PDF p. 8 |

### `ou_picker` (morphology_only)

**Which carcinoma does the report name?**

Hint: Type part of the name in the box and the matching answers appear; the other names ICD-O-3.2 gives a tumour find it too. If a compound name is not found, search for its parts in the other order. When one tumour carries two type names and no single answer names both, choose the higher code number: a transitional cell epidermoid carcinoma is Transitional cell carcinoma, NOS (8120/3), not Squamous cell carcinoma, NOS (8070/3). Use the behaviour the pathologist states. A name that ICD-O ties to one organ, such as the breast, lung or pancreas, means a deposit unless the report says the tumour began at the site you chose; when no primary site was found, record that organ.

165 answers: one per current code, labelled with the ICD-O-3.2 Preferred term, each recording that code at /3 with its synonyms as search terms, plus Seromucinous carcinoma referred to Group 10. Each reason names the site ICD-O ties to the term when it ties one. 8158 and 8290 carry `not_at` C70-C72. Basis follows the evidence gate: 7 from a histology report, 5 from cytology (ou_cytology and cu_cytology reach this node with basis 5). The full list is in the JSON.

## 4 Immunohistochemistry rules

No immunohistochemistry checklist is built for this part, because no marker panel in these sources decides between codes. The diagnosis of an atypical parathyroid tumour or parathyroid carcinoma is strictly histological (Erickson 2022, PDF p. 12), and no single marker separates carcinoma from atypical tumour or adenoma (ICCR Parathyroid 2025, PDF p. 12). The tests below point to an organ, not to a code; they reach the clerk as hints and recognition aids (`site_pointing_tests` in the JSON).

| Test | Points to | Use in the tree | Page |
|---|---|---|---|
| Epstein-Barr virus encoded RNA (EBER) in situ hybridisation | Nasopharynx (C11) | cu_primary hint and recognition aid only; the organ is recorded when the report or clinician names it | Hernandez-Prera 2022, PDF p. 8 (table) |
| p16 immunohistochemistry or high-risk human papillomavirus testing | Oropharynx: tonsil or base of tongue | cu_primary hint only | Hernandez-Prera 2022, PDF p. 8 (table) |
| Ultraviolet-signature mutations | Skin (C44) | cu_primary hint only | Hernandez-Prera 2022, PDF p. 8 (table) |
| Cytokeratin 20, Merkel cell polyomavirus, ultraviolet-signature mutations | Merkel cell carcinoma, skin (C44) | cu_histology hint (Rule H: Merkel cell carcinoma is tied to C44) | Hernandez-Prera 2022, PDF p. 8 (table) |
| Calcitonin (immunohistochemistry and serum) | Laryngeal neuroendocrine tumour; medullary thyroid carcinoma | lab_tests entry; the organ is recorded when the report names it | Hernandez-Prera 2022, PDF p. 8 (table) |
| Parathyroid hormone, GATA3 and GCM2 positive; TTF1 negative | Parathyroid origin, as against thyroid | Confirms a parathyroid tumour; decides no code. No single marker separates carcinoma from atypical tumour or adenoma, so no immunohistochemistry checklist is built for the parathyroid | ICCR Parathyroid 2025, PDF p. 12; Erickson 2022, PDF p. 13; Erickson 2022, PDF p. 12 |

## 5 Registration without tissue

| Evidence | Records | Basis | Source |
|---|---|---|---|
| Parathyroid: a referral letter or clinical note that states parathyroid carcinoma | 8000/3 | 1 | ICCR Parathyroid 2025, PDF p. 6 Visser 2023 as the registrar gave it. ICCC-2017 places 8000/3 at C75.0 in XIIb, so pt_clinical refers to Group 12. |
| Parathyroid: an imaging report, with or without calcium and parathyroid hormone results, in which the clinician states parathyroid carcinoma | 8000/3 | 2 | ICCR Parathyroid 2025, PDF p. 5 Visser 2023 as the registrar gave it. Visser Table 4 has no entry for parathyroid carcinoma, so calcium and parathyroid hormone never give basis 4. |
| Parathyroid: possible or suspected carcinoma, or high calcium and parathyroid hormone with no diagnosis | not registrable |  | ICCR Parathyroid 2025, PDF p. 5; ICCR Parathyroid 2025, PDF p. 6 Visser 2023 as the registrar gave it. |
| Unknown primary or ill-defined site: a clinical note or imaging report that states a cancer whose primary was not found | 8000/3 | 2 | WHO ICD-O-3.1 manual, PDF p. 6 Visser 2023 as the registrar gave it. Basis 1 for a clinical note. ICCC-2017 places 8000/3 at C76 and C80.9 in XIIb (Group 12). |
| Unknown primary: imaging that shows tumour deposits, with a raised chromogranin A and a stated neuroendocrine tumour | 8240/3 | 4 |  Visser 2023 as the registrar gave it. Registrar question 7. |
| Unknown primary: imaging that shows tumour deposits, with a raised serotonin and a stated neuroendocrine tumour | 8241/3 | 4 |  Visser 2023 as the registrar gave it. Registrar question 7. |
| Any site in this part: a raised marker with no imaging that shows a tumour | not registrable |  |  Visser 2023 as the registrar gave it. Rule 6: basis 4 never stands alone. |
| Brain, spinal cord or meninges, or the craniopharyngeal duct: a clinical note or imaging report that states a primary malignant tumour | 8000/3 | 2 |  Visser 2023 as the registrar gave it. ICCC-2017 places 8000/3 at C70-C72 and C75.1-C75.3 in IIIf, so cn_clinical, cn_imaging, en_clinical and en_imaging refer to Group 3. |
| Peritoneum, retroperitoneum, carotid body, aortic body or another endocrine gland: a clinical note or imaging report that states a malignant tumour, type not named | 8000/3 | 2 |  Visser 2023 as the registrar gave it. ICCC-2017 places 8000/3 at C48 and C75.4-C75.9 in XIIb (Group 12). |

## 6 Laboratory tests

| Test | Specimen | Role | Page |
|---|---|---|---|
| Calcium | serum | The highest level before surgery is recorded. A very high level with a neck mass raises the question of parathyroid carcinoma; it registers no code, because no tissue-free rule covers parathyroid carcinoma and the diagnosis is made on the resection specimen. | ICCR Parathyroid 2025, PDF p. 5; Erickson 2022, PDF p. 5; ICCR Parathyroid 2025, PDF p. 6 |
| Parathyroid hormone | serum | Recorded with calcium. A markedly raised level raises the question of parathyroid carcinoma and registers no code. Parathyroid hormone is also an immunostain that confirms parathyroid origin on tissue. | ICCR Parathyroid 2025, PDF p. 5; Erickson 2022, PDF p. 5; ICCR Parathyroid 2025, PDF p. 12 |
| Calcitonin | serum | In a neck node carcinoma with no primary found, calcitonin (immunostain or serum) points to a neuroendocrine primary such as a laryngeal neuroendocrine tumour; the site is recorded only when the report or clinician names it. With imaging that shows a thyroid tumour, a raised serum calcitonin registers medullary thyroid carcinoma (8345/3, basis 4) in the thyroid tree. | Hernandez-Prera 2022, PDF p. 8 (table) |
| Chromogranin A | plasma | With imaging that shows tumour deposits and no primary found, a raised result records Neuroendocrine tumor, NOS (8240/3) at C80.9, basis 4 (cu_lab). | Visser 2023 Table 4 (not in this file set) |
| Serotonin | other | With imaging that shows tumour deposits and no primary found, a raised result records Enterochromaffin cell carcinoid (8241/3) at C80.9, basis 4 (cu_lab). Specimen as the report gives it. | Visser 2023 Table 4 (not in this file set) |

## 7 Rules A to K

| Rule | Applies | How it reaches the clerk | Page |
|---|---|---|---|
| A | yes | cu_region: the first answer sends a squamous cell or basal cell carcinoma of a region, or of the chin or forehead, to the skin of that region, and its reason gives the arm example (C44.6, not C76.4); the hint says the chin and forehead are skin. cu_primary routes a region-only report to cu_region. | WHO ICD-O-3.1 manual, PDF p. 1; WHO ICD-O-3.1 manual, PDF p. 4 |
| B | yes | cu_region: the answer for a site written with peri-, para-, area of or region of stays at C76 unless the tumour type shows the tissue, and its reason says so. pe_clinical, pe_imaging and pe_histology hints: tissue around the pancreas, the adrenal gland or the caecum is retroperitoneum (C48.0), as ICD-O lists them. | WHO ICD-O-3.1 manual, PDF p. 1; WHO ICD-O-3.1 manual, PDF p. 4 |
| C | yes | cu_region hint: one tumour crossing two or more regions with no known starting point is recorded at C76.8. C48.8 and C75.8 are the overlapping codes for the peritoneum and the endocrine glands and are chosen on the site screen. | WHO ICD-O-3.1 manual, PDF p. 5 |
| D | yes | Referral only: the Lymphoma answer on pt_histology sends the case to Group II, whose tree applies Rule D. | ICCR Parathyroid 2025, PDF p. 4 |
| E | no | No leukaemia is met at these sites; none of this part's screens offers one. |  |
| F | yes | pt_histology separates the pathologist's stated diagnosis by behaviour: parathyroid carcinoma records 8140/3, atypical parathyroid tumour is excluded as 8140/1 and adenoma as 8140/0; each reason names the behaviour. ou_picker hint: use the behaviour the pathologist states. | WHO ICD-O-3.1 manual, PDF p. 2; ICCR Parathyroid 2025, PDF p. 9 (table) |
| G | no | No screen in this part offers two grades of one tumour. The WHO endorses no grading system for parathyroid carcinoma, so the parathyroid screen asks none. | WHO ICD-O-3.1 manual, PDF p. 2; ICCR Parathyroid 2025, PDF p. 8 |
| H | yes | cu_histology hint and answers: with no primary site found, papillary thyroid carcinoma is recaptured to the thyroid (C73.9), nasopharyngeal carcinoma or Schmincke tumour to the nasopharynx (C11), parathyroid carcinoma to C75.0 and hepatocellular carcinoma to the liver (Group VII); each reason names the ICD-O site. ou_picker: every reason names the site ICD-O ties to the term, and the hint sends a site-bound name to its organ unless the report places the tumour at the chosen site. pe_histology hint: serous carcinoma tied to the ovary stays at the peritoneum only when the report says it began there. cn_histology hint: check a carcinoma in the brain is not a deposit. | WHO ICD-O-3.1 manual, PDF p. 10; WHO ICD-O-3.1 manual, PDF p. 2; Hernandez-Prera 2022, PDF p. 6 |
| J | yes | ou_picker hint: if a compound name is not found, search for its parts in the other order. | WHO ICD-O-3.1 manual, PDF p. 3 |
| K | yes | pt_histology and ou_picker hints: when one tumour carries two type names and no single answer names both, choose the higher code number; the picker hint gives the transitional cell epidermoid carcinoma example (8120/3). | WHO ICD-O-3.1 manual, PDF p. 3 |

There is no Rule I.

## 8 Code currency

| Code | Finding | Action |
|---|---|---|
| 8140/3 | Current. Preferred term Adenocarcinoma, NOS; Parathyroid carcinoma is a related term carrying C75.0. The WHO 5th-edition table prints 8140/3 for parathyroid carcinoma (ICCR Parathyroid 2025, PDF p. 9). The REDCap label Adenocarcinoma, NOS matches the Preferred term. | pt_histology answer Parathyroid carcinoma records 8140/3; its reason names Adenocarcinoma, NOS and the related term. |
| 8140/1 | Preferred term Atypical adenoma. The WHO 2022 replaced atypical parathyroid adenoma with atypical parathyroid tumour (Erickson 2022, PDF p. 1) and keeps 8140/1 (ICCR, PDF p. 9). | Exclusion on pt_histology, with the ICD-O-3.2 Preferred term. |
| 8322/3 | Current: Water-clear cell adenocarcinoma (C75.0). Not in the WHO 5th-edition parathyroid table, which prints only 8140/3 for carcinoma. | Picker entry; registrar question 2 decides whether a water-clear cell parathyroid carcinoma records 8322/3 (Rule K) or 8140/3 (WHO table). |
| 8010/3 | Current: Carcinoma, NOS. The REDCap XIf option string is 'Epithelial Tumor, NOS', which ICD-O-3.2 does not print at any behaviour (8010/0 is Epithelial tumor, benign; 8010/3 lists Epithelial tumor, malignant as a synonym). The currency check (section 4) does not list this label; the XIb and XIc lists use Carcinoma, NOS. | The tool shows Carcinoma, NOS. Add the XIf label to the REDCap-side list in docs/TODO.md section 7 (standing rule 16). |
| 8000/3 | Current: Neoplasm, malignant. ICCC-2017 places it in XIIb at C48, C75.0, C75.4-C75.9, C76 and C80.9, and in IIIf at C70-C72 and C75.1-C75.3. | Tissue-free and 'malignant cells, not carcinoma' answers refer to Group 12, or Group 3 at the central nervous system sites and the craniopharyngeal duct. |
| 8480/3 | Current: Mucinous adenocarcinoma, with the related term Pseudomyxoma peritonei with unknown primary site (C80.9); four synonyms are [obs] (Gelatinous adenocarcinoma, Gelatinous carcinoma, Mucous adenocarcinoma, Mucous carcinoma). 8480/6 Pseudomyxoma peritonei is metastatic. | Picker search terms leave out the [obs] synonyms; pe_histology recaptures pseudomyxoma to its source organ or to C80.9. |
| 8474/3 | New in ICD-O-3.2 and absent from REDCap (currency check section 6, which lists it under XIf10). ICCC-2017 places 8474 in Xd at every site (000-809), not in any XIf range. | pe_histology and ou_picker refer it to Group 10. Correct the currency check's XIf10 entry (conflict 7). |
| 8280, 8281, 8300/3 | Every /3 term [obs]; 8272/3 Pituitary carcinoma, NOS is current; C75.1 routes to Group III (currency check section 2). | en_histology refers pituitary and pineal tumours to Group 3; the codes are not built. |
| 9052/0 | ICD-O-3.2 gives Well differentiated papillary mesothelioma as a related term at 9052/0 and keeps 9052/1 for the pleura (C38.4). | Exclusion on pe_histology at 9052/0 (data gap 3). |
| 8321/0 | Chief cell adenoma (C75.0); REDCap offers 8321 in XIf with no malignant form (currency check section 5). | Excluded through the parathyroid adenoma answer; REDCap-side list. |
| 8324/0 | Lipoadenoma; REDCap offers 8324 in XIb and XIf with no malignant form (currency check section 5). | Exclusion on pt_histology; REDCap-side list. |
| 8042/3 | Every /3 term is [obs]. ICD-O-3.2 lists Small cell carcinoma, pulmonary type as a synonym of the current 8041/3 Small cell carcinoma, NOS (currency check section 2). | not_built: never appears on a screen (registrar, 8 October 2026). |
| 8124/3 | Every /3 term is [obs]; ICD-O-3.2 prints no successor (currency check section 2). | not_built: never appears on a screen (registrar, 8 October 2026). |
| 8130/3 | Every /3 term is [obs], including Papillary urothelial carcinoma; 8120/3 Urothelial carcinoma, NOS is current (currency check section 2). | not_built: never appears on a screen (registrar, 8 October 2026). |
| 8141/3 | Every /3 term is [obs]; ICD-O-3.2 prints no successor (currency check section 2). | not_built: never appears on a screen (registrar, 8 October 2026). |
| 8245/3 | Every /3 term is [obs]; 8243/3 Goblet cell carcinoid is current (currency check section 2). | not_built: never appears on a screen (registrar, 8 October 2026). |
| 8251/3 | Every /3 term is [obs]; the lung adenocarcinoma terms sit under 8250/3, 8253/3 and 8254/3 (currency check section 2). | not_built: never appears on a screen (registrar, 8 October 2026). |
| 8440/3 | Every /3 term is [obs]; ICD-O-3.2 prints no successor (currency check section 2). | not_built: never appears on a screen (registrar, 8 October 2026). |
| 8450/3 | Every /3 term is [obs]; ICD-O-3.2 prints no successor (currency check section 2). | not_built: never appears on a screen (registrar, 8 October 2026). |
| 8508/3 | Every /3 term is [obs]; 8500/2 Cystic hypersecretory carcinoma, intraductal is current (currency check section 2). | not_built: never appears on a screen (registrar, 8 October 2026). |
| 8512/3 | Every /3 term is [obs]; 8510/3 Medullary carcinoma, NOS is current (currency check section 2). | not_built: never appears on a screen (registrar, 8 October 2026). |
| 8033/3 | REDCap label 'Sarcomatoid carcinoma' is not the ICD-O-3.2 Preferred term 'Pseudosarcomatous carcinoma' (REDCap label is: synonym or related term; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8122/3 | REDCap label 'Transitional cell carcinoma, spindle cell' is not the ICD-O-3.2 Preferred term 'Urothelial carcinoma, sarcomatoid' (REDCap label is: synonym or related term; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8131/3 | REDCap label 'Transitional cell carcinoma, micropapillary' is not the ICD-O-3.2 Preferred term 'Urothelial carcinoma, micropapillary' (REDCap label is: synonym or related term; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8150/3 | REDCap label 'Pancreatic endocrine tumor, malignant' is not the ICD-O-3.2 Preferred term 'Pancreatic neuroendocrine tumor, nonfunctioning' (REDCap label is: term not in ICD-O-3.2; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8151/3 | REDCap label 'Insulinoma, malignant' is not the ICD-O-3.2 Preferred term 'Insulinoma, NOS' (REDCap label is: term not in ICD-O-3.2; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8152/3 | REDCap label 'Glucagonoma, malignant' is not the ICD-O-3.2 Preferred term 'Glucagonoma' (REDCap label is: term not in ICD-O-3.2; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8153/3 | REDCap label 'Gastrinoma, malignant' is not the ICD-O-3.2 Preferred term 'Gastrinoma' (REDCap label is: term not in ICD-O-3.2; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8154/3 | REDCap label 'Mixed pancreatic endocrine and exocrine tumor, malignant' is not the ICD-O-3.2 Preferred term 'Mixed neuroendocrine non-neuroendocrine neoplasm (MiNEN)' (REDCap label is: synonym or related term; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8155/3 | REDCap label 'Vipoma, malignant' is not the ICD-O-3.2 Preferred term 'Vipoma' (REDCap label is: term not in ICD-O-3.2; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8156/3 | REDCap label 'Somatostatinoma, malignant' is not the ICD-O-3.2 Preferred term 'Somatostatinoma' (REDCap label is: term not in ICD-O-3.2; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8158/3 | REDCap label 'Endocrine tumor, functioning, NOS' is not the ICD-O-3.2 Preferred term 'ACTH-producing tumor' (REDCap label is: [obs] term; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8163/3 | REDCap label 'Pancreatobiliary-type carcinoma' is not the ICD-O-3.2 Preferred term 'Pancreatobiliary type carcinoma' (REDCap label is: term not in ICD-O-3.2; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8240/3 | REDCap label 'Carcinoid tumor, NOS' is not the ICD-O-3.2 Preferred term 'Neuroendocrine tumor, NOS' (REDCap label is: synonym or related term; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8242/3 | REDCap label 'Enterochromaffin-like cell tumor, malignant' is not the ICD-O-3.2 Preferred term 'Enterochromaffin-like cell tumor' (REDCap label is: term not in ICD-O-3.2; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8249/3 | REDCap label 'Atypical carcinoid tumor' is not the ICD-O-3.2 Preferred term 'Neuroendocrine tumor, grade 2' (REDCap label is: synonym or related term; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8250/3 | REDCap label 'Bronchiolo-alveolar adenocarcinoma, NOS' is not the ICD-O-3.2 Preferred term 'Lepidic adenocarcinoma' (REDCap label is: [obs] term; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8253/3 | REDCap label 'Bronchiolo-alveolar carcinoma, mucinous' is not the ICD-O-3.2 Preferred term 'Adenocarcinoma of lung, mucinous' (REDCap label is: [obs] term; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8254/3 | REDCap label 'Bronchiolo-alveolar carcinoma, mixed mucinous and non-mucinous' is not the ICD-O-3.2 Preferred term 'Adenocarcinoma of lung, mixed mucinous and non-mucinous' (REDCap label is: [obs] term; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8384/3 | REDCap label 'Adenocarcinoma, endocervical type' is not the ICD-O-3.2 Preferred term 'Adenocarcinoma, endocervical type, NOS' (REDCap label is: term not in ICD-O-3.2; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8402/3 | REDCap label 'Nodular hidradenoma, malignant' is not the ICD-O-3.2 Preferred term 'Hidradenocarcinoma' (REDCap label is: synonym or related term; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8406/3 | REDCap label 'Papillary syringadenoma' is not the ICD-O-3.2 Preferred term 'Syringocystadenocarcinoma papilliferum' (REDCap label is: synonym or related term (listed at /0); currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8410/3 | REDCap label 'Sebaceous adenocarcinoma' is not the ICD-O-3.2 Preferred term 'Sebaceous carcinoma' (REDCap label is: synonym or related term; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8441/3 | REDCap label 'Serous cystadenocarcinoma, NOS' is not the ICD-O-3.2 Preferred term 'Serous carcinoma, NOS' (REDCap label is: synonym or related term; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8452/3 | REDCap label 'Solid pseudopapillary carcinoma' is not the ICD-O-3.2 Preferred term 'Solid pseudopapillary neoplasm of pancreas' (REDCap label is: synonym or related term; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8453/3 | REDCap label 'Intraductal papillary-mucinous carcinoma, invasive' is not the ICD-O-3.2 Preferred term 'Intraductal papillary mucinous neoplasm with an associated invasive carcinoma' (REDCap label is: term not in ICD-O-3.2; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8460/3 | REDCap label 'Papillary serous cystadenocarcinoma' is not the ICD-O-3.2 Preferred term 'Low grade serous carcinoma' (REDCap label is: term not in ICD-O-3.2; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8461/3 | REDCap label 'Serous surface papillary carcinoma' is not the ICD-O-3.2 Preferred term 'High grade serous carcinoma' (REDCap label is: term not in ICD-O-3.2; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8482/3 | REDCap label 'Mucinous adenocarcinoma, endocervical type' is not the ICD-O-3.2 Preferred term 'Mucinous carcinoma, gastric type' (REDCap label is: [obs] term; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8502/3 | REDCap label 'Secretory carcinoma of breast' is not the ICD-O-3.2 Preferred term 'Secretory carcinoma' (REDCap label is: term not in ICD-O-3.2; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8504/3 | REDCap label 'Intracystic carcinoma, NOS' is not the ICD-O-3.2 Preferred term 'Encapsulated papillary carcinoma with invasion' (REDCap label is: synonym or related term (listed at /2); currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8507/3 | REDCap label 'Intraductal micropapillary carcinoma' is not the ICD-O-3.2 Preferred term 'Invasive micropapillary carcinoma of breast' (REDCap label is: synonym or related term (listed at /2); currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8525/3 | REDCap label 'Polymorphous low grade adenocarcinoma' is not the ICD-O-3.2 Preferred term 'Polymorphous adenocarcinoma' (REDCap label is: term not in ICD-O-3.2; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8551/3 | REDCap label 'Acinar cell cystadenocarcinoma' is not the ICD-O-3.2 Preferred term 'Acinar adenocarcinoma of lung' (REDCap label is: [obs] term; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8580/3 | REDCap label 'Thymoma, malignant, NOS' is not the ICD-O-3.2 Preferred term 'Thymoma, NOS' (REDCap label is: term not in ICD-O-3.2; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8581/3 | REDCap label 'Thymoma, type A, malignant' is not the ICD-O-3.2 Preferred term 'Thymoma, type A' (REDCap label is: term not in ICD-O-3.2; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8582/3 | REDCap label 'Thymoma, type AB, malignant' is not the ICD-O-3.2 Preferred term 'Thymoma, type AB' (REDCap label is: term not in ICD-O-3.2; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8583/3 | REDCap label 'Thymoma, type B1, malignant' is not the ICD-O-3.2 Preferred term 'Thymoma, type B1' (REDCap label is: term not in ICD-O-3.2; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8584/3 | REDCap label 'Thymoma, type B2, malignant' is not the ICD-O-3.2 Preferred term 'Thymoma, type B2' (REDCap label is: term not in ICD-O-3.2; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8585/3 | REDCap label 'Thymoma, type B3, malignant' is not the ICD-O-3.2 Preferred term 'Thymoma, type B3' (REDCap label is: term not in ICD-O-3.2; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8589/3 | REDCap label 'Carcinoma showing thymus-like element' is not the ICD-O-3.2 Preferred term 'Intrathyroid thymic carcinoma' (REDCap label is: synonym or related term; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8941/3 | REDCap label 'Carcinoma in pleomorphic adenoma' is not the ICD-O-3.2 Preferred term 'Carcinoma ex pleomorphic adenoma' (REDCap label is: synonym or related term; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |
| 8983/3 | REDCap label 'Adenomyoepithelioma' is not the ICD-O-3.2 Preferred term 'Adenomyoepithelioma with carcinoma' (REDCap label is: term not in ICD-O-3.2; currency check section 4). | The picker shows the ICD-O-3.2 Preferred term; the label goes on the REDCap-side list. |

## 9 Conflicts with other groups

| Group | Codes | Sites | Issue |
|---|---|---|---|
| 3 | 8010-8265 (XIf10 range), 8272, 8273, 8158, 8290 | C75.1, C75.3 | ICCC-2017 places the carcinoma codes at the pituitary (C75.1) and pineal (C75.3) in XIf10, while pituitary tumours (8270-8281, 8300, and 8158 and 8290 at C75.1) are IIIe1 and the pineal tumours are Group III. This part leaves C75.1 and C75.3 out of its sites and en_histology refers pituitary and pineal tumours to Group 3. |
| 3 | 8000 | C70.0-C72.9, C75.2 | 8000/3 at the brain, spinal cord, meninges and craniopharyngeal duct is IIIf, so a tissue-free case at these sites refers to Group 3, not Group 12. |
| 3 | 9350, 9390, 9395 | C75.2, C70.0-C72.9 | Craniopharyngioma (IIIe2, behaviours 0, 1 and 3), choroid plexus carcinoma (IIIa2) and papillary tumour of the pineal region (IIIe3) are Group III; en_histology and cn_histology refer them. |
| 4 | 8680, 8691, 8692, 8693, 8700 | C75.4, C75.5, C48.0 | Paragangliomas of the carotid body, aortic body and retroperitoneum are IVb at every site; en_histology and en_clinical refer them. |
| 12 | 9050, 9051, 9052, 9053, 8000 | C48.0-C48.8, C75.0, C75.4-C75.9, C76.0-C76.8, C80.9 | Malignant mesothelioma is XIIa5 at every site, and 8000/3 is XIIb at these sites; pe_histology refers mesothelioma and the tissue-free answers refer 8000/3. |
| 9 | 8806 | C48.0-C48.8 | Desmoplastic small round cell tumour is IXd11 at every site; pe_histology refers it. |
| 10 | 8474 | C48.0-C48.8 | Seromucinous carcinoma is Xd at every site in ICCC-2017; the Group 11 currency check (section 6) lists it under XIf10. The tree refers it to Group 10. |
| 10 | 8441, 8460, 8461 | C48.1, C48.2, C56.9 | Serous carcinoma is XIf10 at the peritoneum but Xd at the ovary; ICD-O-3.2 ties low-grade and high-grade serous carcinoma to the ovary (Rule H), so the peritoneum is recorded only when the report says the tumour began there. |
| 7 | 8170 | C80.9 | Hepatocellular carcinoma with no primary named is recorded at the liver by Rule H and is VIIb at every site; cu_histology refers it. |
| 11 | 8260, 8082, 8247, 8500, 8140 | C80.9, C76.0 | Within Group XI, Rule H moves a carcinoma of unknown primary to the thyroid tree (papillary carcinoma of thyroid, XIb), the nasopharynx tree (Schmincke tumor, XIc), the skin tree (Merkel cell carcinoma, XIe), the breast (infiltrating duct carcinoma, XIf6) or the parathyroid gland (XIf10). The thyroid tree must also take thyroglossal duct carcinoma (data gap 5). |
| 11 | 8158, 8290 | C70.0-C72.9 | No ICCC-2017 range holds 8158 or 8290 at C70-C72: their XIf10 range leaves out 700-729 and IIIe1 holds them only at C75.1. The picker does not offer them at C70-C72 (registrar question 10). |
| 2 | 9590-9989 lymphoma codes | C75.0 | A lymphoma of the parathyroid gland is Group II; pt_histology refers it. |

## 10 Data gaps

1. **A source that reports parathyroid carcinoma in patients aged 0 to 18, with its frequency and setting (hyperparathyroidism-jaw tumour syndrome).** Pfister 2022 Table 3 lists parathyroid endocrine tumours and parathyroid adenoma but does not name carcinoma, and neither parathyroid source gives ages. Parathyroid carcinoma is built as an option on that indirect evidence (registrar question 1). Candidate source: WHO Classification of Paediatric Tumours, 5th edition (2022), parathyroid chapter; or a paediatric parathyroid carcinoma series in CDC73-related disease.
2. **The frequency and histological types of carcinoma of unknown primary in patients aged 0 to 18.** No source here reports carcinoma of unknown primary in children. Without it, squamous cell carcinoma, undifferentiated carcinoma, neuroendocrine carcinoma and adenocarcinoma stay in the picker at C80.9 and only Carcinoma, NOS is an option (registrar question 6). Candidate source: A population-based paediatric series of C80.9 cases (for example ACCIS or SEER under 20 years); WHO Paediatric Tumours 5th edition.
3. **The WHO 5th-edition classification of peritoneal tumours, with codes and paediatric occurrence (well-differentiated papillary mesothelial tumour, primary peritoneal serous carcinoma).** Pfister 2022 lists only 'mesothelial tumors' and 'peritoneal inclusion cysts' for the peritoneum. It decides whether the peritoneal well-differentiated papillary tumour is /0 or /1 (both excluded) and whether any peritoneal carcinoma is an option rather than a picker entry. Candidate source: WHO Classification of Tumours, Female Genital Tumours, 5th edition (2020), tumours of the peritoneum chapter, or a review of it.
4. **A source on primary carcinoma of the brain, spinal cord and meninges, and on how often a carcinoma there is a deposit.** No source here addresses it; cn_histology asks the report and sends a stated primary to the picker without evidence of paediatric occurrence. Candidate source: WHO Classification of Tumours of the Central Nervous System, 5th edition (2021), metastatic tumours chapter.
5. **The ICD-O topography for heterotopia-associated carcinoma: thyroglossal duct carcinoma, and salivary carcinoma in a neck lymph node.** The thyroglossal duct carcinoma belongs to the thyroid tree only if ICD-O indexes the thyroglossal duct at C73.9, and no file here holds the topography index. An intranodal salivary carcinoma at C77.0 would fall in no Group XI range (registrar question 5). Candidate source: ICD-O-3.2 topography alphabetic index; SEER or ENCR coding guidance on heterotopic tissue.
6. **Visser 2023 (Front Oncol 13:1250549) Table 4 in this part's file set.** cu_lab and the tissue-free entries rely on the controller's summary of Table 4; no page quote is attached, and whether imaging of deposits alone 'shows the tumour' is not checked (registrar question 7). Candidate source: Visser O, et al. Front Oncol 2023;13:1250549, PDF p. 6.

### Questions for the registrar

1. Parathyroid carcinoma as an option. Pfister 2022 Table 3 (PDF p. 14) lists parathyroid endocrine tumours and parathyroid adenoma in the paediatric classification without naming carcinoma; ICCR Parathyroid 2025 (PDF p. 5) gives hyperparathyroidism-jaw tumour syndrome (CDC73) a lifetime parathyroid carcinoma risk of about 15%, and Pfister (PDF p. 19) lists that syndrome among paediatric predisposition syndromes. Proposed: Parathyroid carcinoma (8140/3) is an answer on pt_histology. Confirm.
2. Water-clear cell or oncocytic parathyroid carcinoma. The WHO 5th-edition table gives only 8140/3 (ICCR, PDF p. 9). ICD-O-3.2 holds 8322/3 Water-clear cell adenocarcinoma (C75.0) and 8290/3 Oxyphilic adenocarcinoma (Oncocytic carcinoma). Rule K takes the higher code. Should a report naming water-clear cell or oncocytic parathyroid carcinoma record 8322/3 or 8290/3 (Rule K), or 8140/3 (the WHO table)?
3. A report that names only 'parafibromin-deficient parathyroid neoplasm' and states no carcinoma, atypical tumour or adenoma. ICD-O-3.2 has no term for it and the diagnosis is strictly histological (Erickson 2022, PDF p. 12). Proposed: not registered until the report states carcinoma. Confirm.
4. A neck lymph node carcinoma that is EBER positive, or p16 or high-risk HPV positive, with no primary named by the report or clinician. The WHO defines true carcinoma of unknown primary as p16 and EBER negative (Hernandez-Prera 2022, PDF p. 2), and EBER correlates with a nasopharyngeal origin (PDF p. 8). ICD-O Rule H applies only to terms that print a site, and Non-keratinizing squamous cell carcinoma (8072/3) prints none. The tree records C80.9 unless the report or clinician names the organ. Should EBER positivity alone record the nasopharynx (C11.9), and p16 or HPV positivity the oropharynx?
5. Heterotopia-associated salivary carcinoma in a neck lymph node (Hernandez-Prera 2022, PDF p. 7). Which topography: lymph node (C77.0, which no ICCC-2017 Group XI range holds), head, face or neck (C76.0), or the salivary gland? Which morphology: the salivary type (for example Mucoepidermoid carcinoma 8430/3) or Carcinoma, NOS (8010/3), under which ICD-O-3.2 lists Heterotopia-associated carcinoma?
6. Carcinoma of unknown primary types. The WHO names squamous cell, undifferentiated and neuroendocrine morphology (Hernandez-Prera 2022, PDF p. 8), but no source reports carcinoma of unknown primary in children. Should Squamous cell carcinoma, NOS (8070/3), Carcinoma, undifferentiated, NOS (8020/3), Neuroendocrine carcinoma, NOS (8246/3) and Adenocarcinoma, NOS (8140/3) be answers on cu_histology, or stay in the picker beside Carcinoma, NOS (8010/3)?
7. Tissue-free registration with no primary found. Does Visser 2023 Table 4 apply when imaging shows only deposits and a raised chromogranin A or serotonin, recording Neuroendocrine tumor, NOS (8240/3) or Enterochromaffin cell carcinoid (8241/3) at C80.9 with basis 4?
8. Seromucinous carcinoma (8474/3). The Group 11 currency check (section 6) lists it under XIf10; ICCC-2017 places 8474 in Xd at every site. Confirm the referral to Group 10 and correct the currency check.
9. Pituitary (C75.1) and pineal (C75.3). ICCC-2017 places carcinoma codes there in XIf10. Confirm that the Group 11 site list leaves both out and refers pituitary and pineal tumours to Group 3.
10. 8158/3 (ACTH-producing tumor) and 8290/3 (Oxyphilic adenocarcinoma) at the brain, spinal cord and meninges fall in no ICCC-2017 range. Proposed: not offered at C70-C72. Confirm.
