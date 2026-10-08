# Group 11 evidence — XIf2 colorectum and anus, XIf3 appendix, XIf10 other digestive organs (oesophagus, stomach, small intestine, extrahepatic bile ducts, gallbladder, pancreas)

Part `XIf2_XIf3_digestive`, 8 October 2026. Evidence for the digestive screens of the Group 11 tree: what the clerk is asked, which ICD-O-3.2 code each answer records, and the page behind each answer. The JSON beside this file holds the same content for the build. Every code below was checked in `icdo32.sqlite`, and every option code was checked against ICCC-2017 at its sites.

**What the sources establish.** Five digestive entities have a paediatric report in this part's files: appendiceal neuroendocrine tumours, solid pseudopapillary neoplasm and acinar cell carcinoma of the pancreas (Group 11 options), pancreatoblastoma (Group 12) and gastroblastoma (no ICD-O-3.2 code). Pfister 2022 also lists paediatric gastrointestinal stromal tumour (Group 12). No file reports colorectal, gastric, oesophageal, small-bowel or biliary carcinoma in patients aged 0 to 18. Under ruling 1 those carcinomas sit in the long-tail picker, not on the histology screens, until the controller fetches a paediatric source (data gap 1). This differs from the controller's starting brief, which put colorectal adenocarcinoma, mucinous, signet ring cell and medullary carcinoma on the colorectal screen.

**Update, 8 October 2026.** Five paediatric papers from PubMed Central (section 1) report colorectal carcinoma, appendiceal neuroendocrine tumours, solid pseudopapillary neoplasm and pancreatic neuroendocrine tumours in patients aged 0 to 18. Under the registrar's ruling of that date, an entity a source reports at ages 0 to 18 is an option on its site's histology screen. The colorectal screen now offers mucinous adenocarcinoma, signet ring cell carcinoma, adenocarcinoma NOS, adenocarcinoma in familial adenomatous polyposis and tubular adenocarcinoma; the pancreas screen offers the pancreatic neuroendocrine tumours and neuroendocrine carcinoma. Section 11 lists each change. Carcinomas of the oesophagus, stomach, small intestine, anus and biliary tract still have no paediatric report and stay in the picker.

## 1 Sources

| Cited as | File | Citation | WHO volume |
|---|---|---|---|
| Nagtegaal 2020 | `XIf2-colorectum-XIf3-appendix-XIf10-digestive__Nagtegaal-2019.txt` | Nagtegaal ID, Odze RD, Klimstra D, Paradis V, Rugge M, Schirmacher P, Washington KM, Carneiro F, Cree IA; WHO Classification of Tumours Editorial Board. The 2019 WHO classification of tumours of the digestive system. Histopathology 2020;76(2):182-188. doi:10.1111/his.13975 | WHO Classification of Tumours, Digestive System Tumours, 5th edition, 2019 |
| ICCR Oesophagus 2025 | `XIf10-oesophagus__ICCR-Oesophagus-3rd.txt` | International Collaboration on Cancer Reporting. Carcinoma of the Oesophagus Histopathology Reporting Guide, 3rd edition, version 3.0, December 2025. ISBN 978-1-922324-66-5 | WHO Classification of Tumours of the Digestive System, 5th edition, 2019, with Corrigenda July 2024 |
| ICCR Stomach 2025 | `XIf10-stomach__ICCR-Stomach-3rd.txt` | International Collaboration on Cancer Reporting. Carcinoma of the Stomach Histopathology Reporting Guide, 3rd edition, version 3.0, December 2025. ISBN 978-1-922324-64-1 | WHO Classification of Tumours of the Digestive System, 5th edition, 2019, with Corrigenda July 2024 |
| Stanley 2015 | `XIf10-pancreas-solid-pseudopapillary__Stanley-2015.txt` | Stanley P, Stanley C, Ciambotti J, LeGallo R, Altes T. Solid pseudopapillary neoplasm of the pancreas in a pediatric patient. J Diagn Med Sonogr 2015;31(5):308-312. doi:10.1177/8756479315597708 | None: a case report |
| Pfister 2022 | `ALL-paediatric-occurrence__Pfister-2022.txt` | Pfister SM, Reyes-Múgica M, Chan JKC, et al. A summary of the inaugural WHO classification of pediatric tumors: transitioning from the optical into the molecular era. Cancer Discov 2022;12(2):331-355 | WHO Classification of Tumours, Paediatric Tumours, 5th edition, 2022 |
| ICD-O-3.1 manual | `RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt` | World Health Organization. International Classification of Diseases for Oncology, 3rd edition, 1st revision (ICD-O-3.1), section 4, Coding guidelines, printed pp. 14-28 | None: the coding manual |
| Polat 2021 | `XIf2-colorectum-paediatric__Polat-2021.txt` | Polat E, et al. Colorectal Carcinoma in Childhood. JPGN Rep 2021;2(1):e039. doi:10.1097/PG9.0000000000000039 | not a WHO summary; paediatric evidence |
| Mahajan 2022 | `XIf2-colorectum-paediatric__Mahajan-2022.txt` | Mahajan N, et al. Pediatric Colorectal Carcinoma: A Series of Seven Cases. J Indian Assoc Pediatr Surg 2022. doi:10.4103/jiaps.JIAPS_33_21 | not a WHO summary; paediatric evidence |
| Roganovic 2026 | `XIf3-appendix-neuroendocrine-paediatric__Roganovic-2026.txt` | Roganovic J. Appendiceal Neuroendocrine Tumors in Children and Adolescents. Acta Med Acad 2026. doi:10.5644/ama2006-124.496 | not a WHO summary; paediatric evidence |
| Ebrahim 2025 | `XIf10-pancreas-solid-pseudopapillary-paediatric__Ebrahim-2025.txt` | Ebrahim NAA, et al. Diagnostic insights into solid pseudopapillary neoplasms of the pancreas: a decade of experience with pediatric representation. Diagn Pathol 2025. doi:10.1186/s13000-025-01648-9 | not a WHO summary; paediatric evidence |
| Karges 2025 | `XIf10-pancreas-neuroendocrine-paediatric__Karges-2025.txt` | Karges K, et al. Pancreatic neuroendocrine tumors in children and adolescents - Data from the German MET studies (1997-2023). J Neuroendocrinol 2025. doi:10.1111/jne.70039 | not a WHO summary; paediatric evidence |

Nagtegaal 2020 is the WHO editorial board's commentary on the 5th-edition digestive volume. It prints a table of changes and the neuroendocrine grading table, but no entity list with codes. The ICCR Oesophagus and Stomach guides print the WHO 5th-edition entity tables with ICD-O-3.2 codes (Oesophagus Table 1, PDF pp. 12-13; Stomach Table 3, PDF pp. 14-15); these were read from the page images. Stanley 2015 is a single case report and the only diagnostic text for solid pseudopapillary neoplasm. PDF page numbers are the page index of each PDF; for the ICD-O-3.1 manual extract the printed page is given too.

The five paediatric papers were added on 8 October 2026. Each is a PubMed Central text with sections, not pages, so its citations give the PMC section number in place of a PDF page. Polat 2021 and Mahajan 2022 are colorectal carcinoma case series in patients aged 12 to 16 and 8.6 to 11.8; Roganovic 2026 is a review of paediatric appendiceal neuroendocrine tumours; Ebrahim 2025 is a 60-case series of solid pseudopapillary neoplasm with four patients aged 8 to 14; Karges 2025 reports 28 pancreatic neuroendocrine tumours in patients under 18 from the German Malignant Endocrine Tumour Registry.

## 2 Entities

Decision: `option` appears on a histology screen; `picker` is in the searchable long-tail list `dg_carcinoma_picker`; `exclusion` is benign, borderline or in situ and not registered; `not_built` has no current ICD-O-3.2 term at /3; `refer` goes to another group; `registrar` waits for Jay's ruling because ICD-O-3.2 has no code for it.

| Entity (WHO term) | Code | ICD-O-3.2 term matched (level) | ICD-O-3.2 preferred term | Paediatric | Decision | Source |
|---|---|---|---|---|---|---|
| Neuroendocrine tumour, grade 1 (appendix) | 8240/3 | Neuroendocrine tumor, grade 1 (Related) | Neuroendocrine tumor, NOS | common | option | Pfister 2022, PDF p. 13; Nagtegaal 2020, PDF p. 4; Roganovic 2026, PMC section 1; Roganovic 2026, PMC section 4 |
| Neuroendocrine tumour, grade 2 (appendix) | 8249/3 | Neuroendocrine tumor, grade 2 (Preferred) | Neuroendocrine tumor, grade 2 | occurs | option | Pfister 2022, PDF p. 13; Nagtegaal 2020, PDF p. 4; Roganovic 2026, PMC section 4 |
| Neuroendocrine tumour, grade 3 (appendix) | 8249/3 | Neuroendocrine tumor, grade 3 (Related) | Neuroendocrine tumor, grade 2 | occurs | option | Pfister 2022, PDF p. 13; Nagtegaal 2020, PDF p. 4; Nagtegaal 2020, PDF p. 5 |
| Neuroendocrine tumour, grade not stated (appendix); carcinoid | 8240/3 | Neuroendocrine tumor, NOS (Preferred) | Neuroendocrine tumor, NOS | common | option | Pfister 2022, PDF p. 13; Nagtegaal 2020, PDF p. 4; Roganovic 2026, PMC section 1 |
| Neuroendocrine tumour, grade 1 or grade not stated (sites other than the appendix and pancreas) | 8240/3 | Neuroendocrine tumor, NOS (Preferred) | Neuroendocrine tumor, NOS | not_reported | picker | Nagtegaal 2020, PDF p. 4; ICCR Stomach 2025, PDF p. 15 (table image) |
| Neuroendocrine tumour, grade 1 or grade not stated (pancreas) | 8240/3 | Neuroendocrine tumor, NOS (Preferred) | Neuroendocrine tumor, NOS | occurs | option | Karges 2025, PMC section 1; Karges 2025, PMC section 8; Karges 2025, PMC section 9 |
| Neuroendocrine tumour, grade 2 or grade 3 (sites other than the appendix and pancreas) | 8249/3 | Neuroendocrine tumor, grade 2 (Preferred) | Neuroendocrine tumor, grade 2 | not_reported | picker | ICCR Stomach 2025, PDF p. 15 (table image) |
| Neuroendocrine tumour, grade 2 or grade 3 (pancreas) | 8249/3 | Neuroendocrine tumor, grade 2 (Preferred) | Neuroendocrine tumor, grade 2 | occurs | option | Karges 2025, PMC section 9; Karges 2025, PMC section 8 |
| Enterochromaffin-cell carcinoid (serotonin-producing neuroendocrine tumour) | 8241/3 | Enterochromaffin cell carcinoid (Preferred) | Enterochromaffin cell carcinoid | not_reported | picker | ICCR Stomach 2025, PDF p. 15 (table image) |
| ECL-cell carcinoid, malignant | 8242/3 | ECL cell carcinoid (Synonym) | Enterochromaffin-like cell tumor | not_reported | picker | ICCR Stomach 2025, PDF p. 15 (table image) |
| Gastrinoma NOS | 8153/3 | Gastrinoma (Preferred) | Gastrinoma | not_reported | picker | ICCR Stomach 2025, PDF p. 15 (table image) |
| Gastrinoma (pancreas) | 8153/3 | Gastrinoma (Preferred) | Gastrinoma | occurs | option | Karges 2025, PMC section 7; Karges 2025, PMC section 2 |
| Somatostatinoma NOS | 8156/3 | Somatostatinoma (Preferred) | Somatostatinoma | not_reported | picker | ICCR Stomach 2025, PDF p. 15 (table image) |
| Somatostatinoma (pancreas) | 8156/3 | Somatostatinoma (Preferred) | Somatostatinoma | occurs | option | Karges 2025, PMC section 2 |
| Non-functioning pancreatic neuroendocrine tumour | 8150/3 | Pancreatic neuroendocrine tumor, nonfunctioning (Preferred) | Pancreatic neuroendocrine tumor, nonfunctioning | common | option | Nagtegaal 2020, PDF p. 6; Nagtegaal 2020, PDF p. 4; Karges 2025, PMC section 1; Karges 2025, PMC section 11 |
| Insulinoma | 8151/3 | Insulinoma, NOS (Preferred) | Insulinoma, NOS | common | option | Nagtegaal 2020, PDF p. 4; Karges 2025, PMC section 2; Karges 2025, PMC section 11; Karges 2025, PMC section 7 |
| Glucagonoma | 8152/3 | Glucagonoma (Preferred) | Glucagonoma | occurs | option | Nagtegaal 2020, PDF p. 4; Karges 2025, PMC section 2 |
| VIPoma | 8155/3 | Vipoma (Preferred) | Vipoma | occurs | option | Nagtegaal 2020, PDF p. 4; Karges 2025, PMC section 2 |
| ACTH-producing neuroendocrine tumour | 8158/3 | ACTH-producing tumor (Preferred) | ACTH-producing tumor | not_reported | picker | Nagtegaal 2020, PDF p. 4 |
| Neuroendocrine carcinoma NOS | 8246/3 | Neuroendocrine carcinoma, NOS (Preferred) | Neuroendocrine carcinoma, NOS | not_reported | picker | Nagtegaal 2020, PDF p. 4; Nagtegaal 2020, PDF p. 5; ICCR Stomach 2025, PDF p. 15 (table image) |
| Neuroendocrine carcinoma NOS (pancreas) | 8246/3 | Neuroendocrine carcinoma, NOS (Preferred) | Neuroendocrine carcinoma, NOS | occurs | option | Karges 2025, PMC section 9 |
| Large cell neuroendocrine carcinoma | 8013/3 | Large cell neuroendocrine carcinoma (Preferred) | Large cell neuroendocrine carcinoma | not_reported | picker | ICCR Stomach 2025, PDF p. 15 (table image); ICCR Oesophagus 2025, PDF p. 12 (table image) |
| Small cell neuroendocrine carcinoma | 8041/3 | Small cell neuroendocrine carcinoma (Related) | Small cell carcinoma, NOS | not_reported | picker | ICCR Stomach 2025, PDF p. 15 (table image); ICCR Oesophagus 2025, PDF p. 13 (table image) |
| Mixed neuroendocrine–non-neuroendocrine neoplasm (MiNEN) | 8154/3 | Mixed neuroendocrine non-neuroendocrine neoplasm (MiNEN) (Preferred) | Mixed neuroendocrine non-neuroendocrine neoplasm (MiNEN) | not_reported | picker | Nagtegaal 2020, PDF p. 4; ICCR Stomach 2025, PDF p. 14; ICCR Stomach 2025, PDF p. 15 (table image) |
| Mixed neuroendocrine carcinoma; mixed adenoneuroendocrine carcinoma (MANEC) | 8244/3 | Mixed adenoneuroendocrine carcinoma (Preferred) | Mixed adenoneuroendocrine carcinoma | not_reported | picker | ICCR Oesophagus 2025, PDF p. 13 (table image); Nagtegaal 2020, PDF p. 4 |
| Combined small cell carcinoma (with adenocarcinoma or squamous cell carcinoma) | 8045/3 | Combined small cell carcinoma (Preferred) | Combined small cell carcinoma | not_reported | picker | ICCR Oesophagus 2025, PDF p. 13 (table image) |
| Goblet cell adenocarcinoma | 8243/3 | Goblet cell carcinoid (Preferred) | Goblet cell carcinoid | not_reported | picker | Nagtegaal 2020, PDF p. 4; Nagtegaal 2020, PDF p. 2 |
| Adenocarcinoid tumour | 8245/3 | Adenocarcinoid tumor (Preferred) | Adenocarcinoid tumor | not_reported | not_built | Nagtegaal 2020, PDF p. 4 |
| Low-grade appendiceal mucinous neoplasm | 8480/1 | Low grade appendiceal mucinous neoplasm (Preferred) | Low grade appendiceal mucinous neoplasm | not_reported | exclusion | Nagtegaal 2020, PDF p. 4 |
| Adenocarcinoma NOS | 8140/3 | Adenocarcinoma, NOS (Preferred) | Adenocarcinoma, NOS | not_reported | picker | Nagtegaal 2020, PDF p. 3; ICCR Stomach 2025, PDF p. 14 (table image); Pfister 2022, PDF p. 18 |
| Adenocarcinoma NOS (colon, rectosigmoid junction and rectum) | 8140/3 | Adenocarcinoma, NOS (Preferred) | Adenocarcinoma, NOS | occurs | option | Polat 2021, PMC section 2; Mahajan 2022, PMC section 4 |
| Mucinous adenocarcinoma | 8480/3 | Mucinous adenocarcinoma (Preferred) | Mucinous adenocarcinoma | not_reported | picker | ICCR Stomach 2025, PDF p. 15 (table image); ICCR Stomach 2025, PDF p. 13 |
| Mucinous adenocarcinoma (colon, rectosigmoid junction and rectum) | 8480/3 | Mucinous adenocarcinoma (Preferred) | Mucinous adenocarcinoma | common | option | Polat 2021, PMC section 2; Mahajan 2022, PMC section 1; Mahajan 2022, PMC section 5; Mahajan 2022, PMC section 4 |
| Signet-ring cell carcinoma; poorly cohesive carcinoma | 8490/3 | Signet ring cell carcinoma (Preferred) | Signet ring cell carcinoma | not_reported | picker | ICCR Stomach 2025, PDF p. 15 (table image); Nagtegaal 2020, PDF p. 1; ICCR Stomach 2025, PDF p. 21 |
| Signet ring cell carcinoma (colon, rectosigmoid junction and rectum) | 8490/3 | Signet ring cell carcinoma (Preferred) | Signet ring cell carcinoma | common | option | Mahajan 2022, PMC section 1; Mahajan 2022, PMC section 5 |
| Serrated adenocarcinoma | 8213/3 | Serrated adenocarcinoma (Preferred) | Serrated adenocarcinoma | not_reported | picker | Nagtegaal 2020, PDF p. 2 |
| Adenocarcinoma in adenomatous polyposis coli | 8220/3 | Adenocarcinoma in adenomatous polyposis coli (Preferred) | Adenocarcinoma in adenomatous polyposis coli | not_reported | picker | Nagtegaal 2020, PDF p. 6; Pfister 2022, PDF p. 19 |
| Adenocarcinoma in familial adenomatous polyposis (colon, rectosigmoid junction and rectum) | 8220/3 | Adenocarcinoma in adenomatous polyposis coli (Preferred) | Adenocarcinoma in adenomatous polyposis coli | occurs | option | Mahajan 2022, PMC section 5; Polat 2021, PMC section 3 |
| Tubular adenocarcinoma | 8211/3 | Tubular adenocarcinoma (Preferred) | Tubular adenocarcinoma | not_reported | picker | ICCR Stomach 2025, PDF p. 14 (table image) |
| Tubular adenocarcinoma (colon, rectosigmoid junction and rectum) | 8211/3 | Tubular adenocarcinoma (Preferred) | Tubular adenocarcinoma | occurs | option | Polat 2021, PMC section 2 |
| Papillary adenocarcinoma NOS | 8260/3 | Papillary adenocarcinoma, NOS (Preferred) | Papillary adenocarcinoma, NOS | not_reported | picker | ICCR Stomach 2025, PDF p. 15 (table image) |
| Adenocarcinoma with mixed subtypes (mixed adenocarcinoma) | 8255/3 | Adenocarcinoma with mixed subtypes (Preferred) | Adenocarcinoma with mixed subtypes | not_reported | picker | ICCR Stomach 2025, PDF p. 15 (table image) |
| Micropapillary carcinoma NOS | 8265/3 | Micropapillary carcinoma, NOS (Preferred) | Micropapillary carcinoma, NOS | not_reported | picker | ICCR Stomach 2025, PDF p. 15 (table image) |
| Hepatoid adenocarcinoma | 8576/3 | Hepatoid adenocarcinoma (Preferred) | Hepatoid adenocarcinoma | not_reported | picker | ICCR Stomach 2025, PDF p. 15 (table image); ICCR Stomach 2025, PDF p. 13 |
| Parietal cell carcinoma | 8214/3 | Parietal cell carcinoma (Preferred) | Parietal cell carcinoma | not_reported | picker | ICCR Stomach 2025, PDF p. 14 (table image) |
| Mucoepidermoid carcinoma | 8430/3 | Mucoepidermoid carcinoma (Preferred) | Mucoepidermoid carcinoma | not_reported | picker | ICCR Stomach 2025, PDF p. 15 (table image); ICCR Oesophagus 2025, PDF p. 12 (table image) |
| Paneth cell carcinoma | none | none | none | not_reported | registrar | ICCR Stomach 2025, PDF p. 13; ICCR Stomach 2025, PDF p. 15 (table image) |
| Medullary carcinoma with lymphoid stroma (gastric carcinoma with lymphoid stroma) | 8512/3 | Medullary carcinoma with lymphoid stroma (Preferred) | Medullary carcinoma with lymphoid stroma | not_reported | not_built | ICCR Stomach 2025, PDF p. 15 (table image); ICCR Stomach 2025, PDF p. 13 |
| Squamous cell carcinoma NOS | 8070/3 | Squamous cell carcinoma, NOS (Preferred) | Squamous cell carcinoma, NOS | not_reported | picker | ICCR Oesophagus 2025, PDF p. 12 (table image); Nagtegaal 2020, PDF p. 4 |
| Verrucous squamous cell carcinoma | 8051/3 | Verrucous squamous cell carcinoma (Synonym) | Verrucous carcinoma, NOS | not_reported | picker | ICCR Oesophagus 2025, PDF p. 12 (table image) |
| Squamous cell carcinoma, spindle cell | 8074/3 | Squamous cell carcinoma, spindle cell (Preferred) | Squamous cell carcinoma, spindle cell | not_reported | picker | ICCR Oesophagus 2025, PDF p. 12 (table image) |
| Basaloid squamous cell carcinoma | 8083/3 | Basaloid squamous cell carcinoma (Preferred) | Basaloid squamous cell carcinoma | not_reported | picker | ICCR Oesophagus 2025, PDF p. 12 (table image) |
| Lymphoepithelioma-like carcinoma | 8082/3 | Lymphoepithelioma-like carcinoma (Synonym) | Lymphoepithelial carcinoma | not_reported | picker | ICCR Oesophagus 2025, PDF p. 12 (table image) |
| Adenoid cystic carcinoma | 8200/3 | Adenoid cystic carcinoma (Preferred) | Adenoid cystic carcinoma | not_reported | picker | ICCR Oesophagus 2025, PDF p. 12 (table image) |
| Adenosquamous carcinoma | 8560/3 | Adenosquamous carcinoma (Preferred) | Adenosquamous carcinoma | not_reported | picker | ICCR Stomach 2025, PDF p. 15 (table image); ICCR Stomach 2025, PDF p. 13 |
| Carcinoma, undifferentiated, NOS | 8020/3 | Carcinoma, undifferentiated, NOS (Preferred) | Carcinoma, undifferentiated, NOS | not_reported | picker | ICCR Stomach 2025, PDF p. 15 (table image); ICCR Oesophagus 2025, PDF p. 12 (table image) |
| Large cell carcinoma with rhabdoid phenotype | 8014/3 | Large cell carcinoma with rhabdoid phenotype (Preferred) | Large cell carcinoma with rhabdoid phenotype | not_reported | picker | ICCR Stomach 2025, PDF p. 15 (table image) |
| Pleomorphic carcinoma | 8022/3 | Pleomorphic carcinoma (Preferred) | Pleomorphic carcinoma | not_reported | picker | ICCR Stomach 2025, PDF p. 15 (table image) |
| Sarcomatoid carcinoma | 8033/3 | Sarcomatoid carcinoma (Synonym) | Pseudosarcomatous carcinoma | not_reported | picker | ICCR Stomach 2025, PDF p. 15 (table image) |
| Carcinoma with osteoclast-like giant cells | 8035/3 | Carcinoma with osteoclast-like giant cells (Preferred) | Carcinoma with osteoclast-like giant cells | not_reported | picker | ICCR Stomach 2025, PDF p. 15 (table image) |
| Solid pseudopapillary neoplasm | 8452/3 | Solid pseudopapillary neoplasm of pancreas (Preferred) | Solid pseudopapillary neoplasm of pancreas | occurs | option | Pfister 2022, PDF p. 13; Stanley 2015, PDF p. 1; Ebrahim 2025, PMC section 13 |
| Pancreatic acinar cell carcinoma | 8550/3 | Acinar cell carcinoma (Preferred) | Acinar cell carcinoma | occurs | option | Pfister 2022, PDF p. 13 |
| Pancreatoblastoma | 8971/3 | Pancreatoblastoma (Preferred) | Pancreatoblastoma | rare | refer 12 | Pfister 2022, PDF p. 11; Pfister 2022, PDF p. 13 |
| Pancreatic ductal adenocarcinoma (infiltrating duct carcinoma) | 8500/3 | Infiltrating duct carcinoma, NOS (Preferred) | Infiltrating duct carcinoma, NOS | not_reported | picker | ICD-O-3.1 manual, PDF p. 10 (printed p. 23) |
| Mucinous cystic neoplasm with an associated invasive carcinoma (mucinous cystadenocarcinoma) | 8470/3 | Mucinous cystadenocarcinoma, NOS (Preferred) | Mucinous cystadenocarcinoma, NOS | not_reported | picker | ICD-O-3.1 manual, PDF p. 10 (printed p. 23); Nagtegaal 2020, PDF p. 5 |
| Intraductal papillary mucinous neoplasm with an associated invasive carcinoma | 8453/3 | Intraductal papillary mucinous neoplasm with an associated invasive carcinoma (Preferred) | Intraductal papillary mucinous neoplasm with an associated invasive carcinoma | not_reported | picker | Nagtegaal 2020, PDF p. 5 |
| Gastroblastoma | 8976/3 | none | none | rare | registrar | Pfister 2022, PDF p. 11; ICCR Stomach 2025, PDF p. 14; ICCR Stomach 2025, PDF p. 15 (table image) |
| Serrated dysplasia, high grade (stomach) | 8213/2 | none | none | not_reported | registrar | ICCR Stomach 2025, PDF p. 14 (table image) |
| Intestinal-type adenoma, high grade (stomach) | 8144/2 | none | none | not_reported | registrar | ICCR Stomach 2025, PDF p. 14 (table image) |
| Cholangiocarcinoma (bile duct carcinoma), extrahepatic bile ducts and gallbladder | 8160/3 | Cholangiocarcinoma (Preferred) | Cholangiocarcinoma | not_reported | refer 7 | ICD-O-3.1 manual, PDF p. 11 (printed p. 24); Nagtegaal 2020, PDF p. 2 |
| Perihilar cholangiocarcinoma (Klatskin tumour) | 8162/3 | Perihilar cholangiocarcinoma (Preferred) | Perihilar cholangiocarcinoma | not_reported | refer 7 | ICD-O-3.1 manual, PDF p. 11 (printed p. 24) |
| Cloacogenic carcinoma | 8124/3 | Cloacogenic carcinoma (Preferred) | Cloacogenic carcinoma | not_reported | not_built | Nagtegaal 2020, PDF p. 4 |
| Gastrointestinal stromal tumour | 8936/3 | Gastrointestinal stromal tumor (Preferred) | Gastrointestinal stromal tumor | occurs | refer 12 | Pfister 2022, PDF p. 9 |
| Burkitt lymphoma and other lymphomas of the digestive tract | 9687/3 | Burkitt lymphoma, NOS (Preferred) | Burkitt lymphoma, NOS | occurs | refer 2 | Pfister 2022, PDF p. 6 |
| EBV-positive inflammatory follicular dendritic cell sarcoma of the digestive tract | 9758/3 | Follicular dendritic cell sarcoma (Preferred) | Follicular dendritic cell sarcoma | not_reported | refer 2 | Nagtegaal 2020, PDF p. 2 |
| Gastrointestinal clear cell sarcoma | 9044/3 | Clear cell sarcoma, NOS (Preferred) | Clear cell sarcoma, NOS | not_reported | refer 9 | Nagtegaal 2020, PDF p. 3 |
| Adenomatous polyp, low-grade dysplasia | 8210/0 | Adenomatous polyp, NOS (Preferred) | Adenomatous polyp, NOS | not_reported | exclusion | ICCR Stomach 2025, PDF p. 14 (table image) |
| Adenomatous polyp, high-grade dysplasia | 8210/2 | Adenocarcinoma in situ in adenomatous polyp (Preferred) | Adenocarcinoma in situ in adenomatous polyp | occurs | exclusion | ICCR Stomach 2025, PDF p. 14 (table image); Nagtegaal 2020, PDF p. 2; Polat 2021, PMC section 2 |
| Conventional adenoma (tubular adenoma) | 8211/0 | Tubular adenoma, NOS (Preferred) | Tubular adenoma, NOS | not_reported | exclusion | Nagtegaal 2020, PDF p. 3 |
| Sessile serrated lesion; serrated dysplasia, low grade | 8213/0 | Sessile serrated polyp (Related) | Serrated adenoma, NOS | not_reported | exclusion | Nagtegaal 2020, PDF p. 3; ICCR Stomach 2025, PDF p. 14 (table image) |
| Intestinal-type adenoma, low grade | 8144/0 | Adenoma, intestinal type (Preferred) | Adenoma, intestinal type | not_reported | exclusion | ICCR Stomach 2025, PDF p. 14 (table image) |
| Familial adenomatous polyposis with no carcinoma | 8220/0 | Adenomatous polyposis coli (Preferred) | Adenomatous polyposis coli | occurs | exclusion | Pfister 2022, PDF p. 19; Nagtegaal 2020, PDF p. 6; Polat 2021, PMC section 3 |
| Glandular dysplasia (intraepithelial neoplasia), low grade | 8148/0 | Glandular intraepithelial neoplasia, low grade (Preferred) | Glandular intraepithelial neoplasia, low grade | not_reported | exclusion | ICCR Oesophagus 2025, PDF p. 12; ICCR Stomach 2025, PDF p. 14 (table image) |
| Glandular dysplasia (intraepithelial neoplasia), high grade; biliary or pancreatic intraepithelial neoplasia, high grade | 8148/2 | Glandular intraepithelial neoplasia, high grade (Preferred) | Glandular intraepithelial neoplasia, high grade | not_reported | exclusion | ICCR Oesophagus 2025, PDF p. 12; ICCR Stomach 2025, PDF p. 14 (table image); Nagtegaal 2020, PDF p. 2 |
| Squamous dysplasia (intraepithelial neoplasia), low grade (oesophagus, anus) | 8077/0 | Squamous intraepithelial neoplasia, low grade (Preferred) | Squamous intraepithelial neoplasia, low grade | not_reported | exclusion | ICCR Oesophagus 2025, PDF p. 12; Nagtegaal 2020, PDF p. 2 |
| Squamous dysplasia (intraepithelial neoplasia), high grade (oesophagus, anus) | 8077/2 | Squamous intraepithelial neoplasia, high grade (Preferred) | Squamous intraepithelial neoplasia, high grade | not_reported | exclusion | ICCR Oesophagus 2025, PDF p. 12; Nagtegaal 2020, PDF p. 2 |
| Squamous cell papilloma (oesophagus) | 8052/0 | Squamous cell papilloma, NOS (Preferred) | Squamous cell papilloma, NOS | not_reported | exclusion | ICCR Oesophagus 2025, PDF p. 12 |
| Squamous papillomatosis (oesophagus) | 8060/0 | Squamous papillomatosis (Preferred) | Squamous papillomatosis | not_reported | exclusion | ICCR Oesophagus 2025, PDF p. 12 |
| Intraductal papillary mucinous neoplasm with low-grade dysplasia | 8453/0 | Intraductal papillary mucinous neoplasm with low grade dysplasia (Synonym) | Intraductal papillary mucinous adenoma | not_reported | exclusion | Nagtegaal 2020, PDF p. 5; Nagtegaal 2020, PDF p. 6 |
| Intraductal papillary mucinous neoplasm with high-grade dysplasia | 8453/2 | Intraductal papillary mucinous neoplasm with high grade dysplasia (Preferred) | Intraductal papillary mucinous neoplasm with high grade dysplasia | not_reported | exclusion | Nagtegaal 2020, PDF p. 5; Nagtegaal 2020, PDF p. 6 |
| Mucinous cystic neoplasm with low-grade dysplasia | 8470/0 | Mucinous cystic neoplasm with low grade dysplasia (Related) | Mucinous cystadenoma, NOS | not_reported | exclusion | Nagtegaal 2020, PDF p. 5; Nagtegaal 2020, PDF p. 6 |
| Mucinous cystic neoplasm with high-grade dysplasia | 8470/2 | Mucinous cystic neoplasm with high grade dysplasia (Preferred) | Mucinous cystic neoplasm with high grade dysplasia | not_reported | exclusion | Nagtegaal 2020, PDF p. 5; Nagtegaal 2020, PDF p. 6 |

Why each decision was taken:

- **Neuroendocrine tumour, grade 1 (appendix)** (8240/3): The WHO paediatric volume lists appendiceal neuroendocrine tumours among the digestive tumours of children. Grade 1 is a Ki-67 index below 3% and fewer than 2 mitoses per 2 mm². Paediatric papers added 8 October 2026: Roganovic 2026 calls appendiceal neuroendocrine tumours the most frequent gastrointestinal epithelial tumours of children and adolescents, with a Ki-67 index usually below 3%, consistent with grade 1.
- **Neuroendocrine tumour, grade 2 (appendix)** (8249/3): Appendiceal neuroendocrine tumours occur in children. Grade 2 is a Ki-67 index of 3% to 20% or 2 to 20 mitoses per 2 mm². Paediatric papers added 8 October 2026: Roganovic 2026 states that grade 2 appendiceal neuroendocrine tumours are rare in children.
- **Neuroendocrine tumour, grade 3 (appendix)** (8249/3): Appendiceal neuroendocrine tumours occur in children. A grade 3 neuroendocrine tumour stays well differentiated and is distinct from neuroendocrine carcinoma; ICD-O-3.2 lists it under 8249/3.
- **Neuroendocrine tumour, grade not stated (appendix); carcinoid** (8240/3): Appendiceal neuroendocrine tumours occur in children. A report that gives no grade, or says carcinoid, records the NOS code; Carcinoid tumor, NOS is an ICD-O-3.2 synonym at 8240/3. Paediatric papers added 8 October 2026: Roganovic 2026 calls appendiceal neuroendocrine tumours, historically called carcinoids, the most frequent gastrointestinal epithelial tumours of children and adolescents.
- **Neuroendocrine tumour, grade 1 or grade not stated (sites other than the appendix and pancreas)** (8240/3): The WHO digestive volume grades neuroendocrine tumours at every digestive site. No file in this part reports them in children outside the appendix. On 8 October 2026 the pancreas (C25.0 to C25.9) moved to its own entity, an option, because Karges 2025 reports this tumour in the pancreas of patients under 18; no paper added that day reports it at the other sites in a child.
- **Neuroendocrine tumour, grade 1 or grade not stated (pancreas)** (8240/3): Karges 2025 reports 28 pancreatic neuroendocrine tumours in patients under 18 years from the German Malignant Endocrine Tumour Registry, including grade 1 tumours. A report that gives no grade records the NOS code; ICD-O-3.2 lists neuroendocrine tumour, grade 1 under 8240/3.
- **Neuroendocrine tumour, grade 2 or grade 3 (sites other than the appendix and pancreas)** (8249/3): ICCR Stomach Table 3 codes grade 2 and grade 3 neuroendocrine tumours 8249/3. No file in this part reports them in children outside the appendix. On 8 October 2026 the pancreas (C25.0 to C25.9) moved to its own entity, an option, because Karges 2025 reports this tumour in the pancreas of patients under 18; no paper added that day reports it at the other sites in a child.
- **Neuroendocrine tumour, grade 2 or grade 3 (pancreas)** (8249/3): Karges 2025 reports well-differentiated grade 1 to 3 pancreatic neuroendocrine tumours in 18 of 25 patients under 18 years; of 14 graded tumours with distant metastases, six were grade 2 and eight grade 3. ICD-O-3.2 lists neuroendocrine tumour, grade 3 under 8249/3.
- **Enterochromaffin-cell carcinoid (serotonin-producing neuroendocrine tumour)** (8241/3): A WHO 5th-edition gastric neuroendocrine tumour subtype; Serotonin producing tumor is an ICD-O-3.2 synonym at 8241/3. No paediatric report in this part.
- **ECL-cell carcinoid, malignant** (8242/3): A WHO 5th-edition gastric neuroendocrine tumour subtype. ICD-O-3.2 moved 8242 from /1 to /3. No paediatric report in this part.
- **Gastrinoma NOS** (8153/3): A WHO 5th-edition functioning neuroendocrine tumour. No paediatric report in this part. On 8 October 2026 the pancreas (C25.0 to C25.9) moved to its own entity, an option, because Karges 2025 reports this tumour in the pancreas of patients under 18; no paper added that day reports it at the other sites in a child.
- **Gastrinoma (pancreas)** (8153/3): Karges 2025 diagnosed one gastrinoma among 28 pancreatic neuroendocrine tumours in patients under 18 years, and states that gastrinomas follow insulinomas among the functioning pancreatic neuroendocrine tumours of children.
- **Somatostatinoma NOS** (8156/3): A WHO 5th-edition functioning neuroendocrine tumour. No paediatric report in this part. On 8 October 2026 the pancreas (C25.0 to C25.9) moved to its own entity, an option, because Karges 2025 reports this tumour in the pancreas of patients under 18; no paper added that day reports it at the other sites in a child.
- **Somatostatinoma (pancreas)** (8156/3): Karges 2025 names somatostatinoma among the rarer functioning pancreatic neuroendocrine tumours of children, each under 10% of functioning tumours.
- **Non-functioning pancreatic neuroendocrine tumour** (8150/3): The WHO digestive volume covers the whole spectrum of pancreatic neuroendocrine neoplasms, functioning and non-functioning. No file in this part reports them in children. Paediatric papers added 8 October 2026: Karges 2025 reports non-functioning tumours as 75% of 28 pancreatic neuroendocrine tumours in patients under 18 years; the paper notes that other paediatric series are dominated by insulinoma.
- **Insulinoma** (8151/3): A functioning pancreatic neuroendocrine tumour of the WHO digestive volume. ICD-O-3.2 moved 8151 from /0 to /3. No paediatric report in this part. Paediatric papers added 8 October 2026: Karges 2025 states that insulinomas predominate among the functioning pancreatic neuroendocrine tumours of children and dominate paediatric series in the literature; its registry holds four insulinomas in 28 patients under 18 years.
- **Glucagonoma** (8152/3): A functioning pancreatic neuroendocrine tumour of the WHO digestive volume. No paediatric report in this part. Paediatric papers added 8 October 2026: Karges 2025 names glucagonoma among the rarer functioning pancreatic neuroendocrine tumours of children, each under 10% of functioning tumours.
- **VIPoma** (8155/3): A functioning pancreatic neuroendocrine tumour of the WHO digestive volume. No paediatric report in this part. Paediatric papers added 8 October 2026: Karges 2025 names VIPoma among the rarer functioning pancreatic neuroendocrine tumours of children, each under 10% of functioning tumours.
- **ACTH-producing neuroendocrine tumour** (8158/3): A functioning pancreatic neuroendocrine tumour of the WHO digestive volume. No paediatric report in this part.
- **Neuroendocrine carcinoma NOS** (8246/3): Neuroendocrine carcinomas are poorly differentiated, high grade by definition and not graded. No paediatric report in this part. On 8 October 2026 the pancreas (C25.0 to C25.9) moved to its own entity, an option, because Karges 2025 reports this tumour in the pancreas of patients under 18; no paper added that day reports it at the other sites in a child.
- **Neuroendocrine carcinoma NOS (pancreas)** (8246/3): Karges 2025 identified poorly differentiated neuroendocrine carcinoma in 7 of 25 patients under 18 years with a pancreatic neuroendocrine neoplasm. The paper names no small cell or large cell type, so the NOS code applies.
- **Large cell neuroendocrine carcinoma** (8013/3): The large-cell type of digestive neuroendocrine carcinoma. No paediatric report in this part.
- **Small cell neuroendocrine carcinoma** (8041/3): The small-cell type of digestive neuroendocrine carcinoma. No paediatric report in this part.
- **Mixed neuroendocrine–non-neuroendocrine neoplasm (MiNEN)** (8154/3): The WHO 5th edition groups mixed neoplasms under MiNEN; each component is at least 30% of the tumour. No paediatric report in this part.
- **Mixed neuroendocrine carcinoma; mixed adenoneuroendocrine carcinoma (MANEC)** (8244/3): ICCR Oesophagus Table 1 lists mixed neuroendocrine carcinoma 8244/3 as a MiNEN subtype; ICD-O-3.2 keeps MANEC as a current synonym at 8244/3. No paediatric report in this part.
- **Combined small cell carcinoma (with adenocarcinoma or squamous cell carcinoma)** (8045/3): ICCR Oesophagus Table 1 lists combined small cell–adenocarcinoma and combined small cell–squamous cell carcinoma, both 8045/3, as MiNEN subtypes. No paediatric report in this part.
- **Goblet cell adenocarcinoma** (8243/3): The WHO 5th edition renamed goblet cell carcinoid/carcinoma of the appendix goblet cell adenocarcinoma; ICD-O-3.2 holds the entity at 8243/3 under its former name. Pfister 2022 names only appendiceal neuroendocrine tumours among appendiceal tumours of children.
- **Adenocarcinoid tumour** (8245/3): Every ICD-O-3.2 term at 8245/3 is [obs]. The WHO digestive volume names goblet cell adenocarcinoma, formerly goblet cell carcinoid/carcinoma, and ICD-O-3.2 gives that entity 8243/3. Neither source names adenocarcinoid, so no successor is assigned here.
- **Low-grade appendiceal mucinous neoplasm** (8480/1): ICD-O-3.2 codes the low-grade appendiceal mucinous neoplasm /1, outside the registry's malignant scope. The WHO digestive volume describes appendiceal precursor lesions.
- **Adenocarcinoma NOS** (8140/3): Adenocarcinoma of the small and large bowel, appendix, stomach and other digestive organs. No file in this part reports digestive adenocarcinoma in patients aged 0 to 18; the WHO paediatric volume lists predisposition to gastrointestinal tumours among childhood cancer predisposition syndromes, which is not a report of carcinoma in children. On 8 October 2026 the colon, rectosigmoid junction and rectum (C18.0, C18.2 to C18.9, C19.9, C20.9) moved to their own entity, an option, because Polat 2021 and Mahajan 2022 report this type in colorectal carcinoma of patients aged 8 to 16; no paper added that day reports it at the other sites in a child.
- **Adenocarcinoma NOS (colon, rectosigmoid junction and rectum)** (8140/3): Polat 2021 reports a poorly differentiated rectal adenocarcinoma in a 12-year-old, and Mahajan 2022 records one of seven colorectal carcinomas in children as NOS. The grade is not part of the code.
- **Mucinous adenocarcinoma** (8480/3): A WHO 5th-edition digestive adenocarcinoma subtype with mucin pools over 50% of the tumour area. No paediatric report in this part. On 8 October 2026 the colon, rectosigmoid junction and rectum (C18.0, C18.2 to C18.9, C19.9, C20.9) moved to their own entity, an option, because Polat 2021 and Mahajan 2022 report this type in colorectal carcinoma of patients aged 8 to 16; no paper added that day reports it at the other sites in a child.
- **Mucinous adenocarcinoma (colon, rectosigmoid junction and rectum)** (8480/3): The commonest type in both paediatric series: four of five colorectal carcinomas in patients aged 12 to 16 (Polat 2021) and four of seven in children aged 8.6 to 11.8 (Mahajan 2022). Mahajan 2022 states that more than half of paediatric patients have a mucinous or signet ring cell type.
- **Signet-ring cell carcinoma; poorly cohesive carcinoma** (8490/3): The WHO 5th edition groups signet-ring cell carcinoma under poorly cohesive carcinoma; ICD-O-3.2 lists Poorly cohesive carcinoma as a related term at 8490/3. Hereditary diffuse gastric cancer arises with CDH1 or CTNNA1 mutations. No paediatric report in this part. On 8 October 2026 the colon, rectosigmoid junction and rectum (C18.0, C18.2 to C18.9, C19.9, C20.9) moved to their own entity, an option, because Mahajan 2022 reports this type in colorectal carcinoma of children aged 8.6 to 11.8; no paper added that day reports it at the other sites in a child.
- **Signet ring cell carcinoma (colon, rectosigmoid junction and rectum)** (8490/3): Mahajan 2022 reports the signet ring cell type in two of seven colorectal carcinomas in children aged 8.6 to 11.8, and names mucinous and signet ring cell types as the types of more than half of paediatric patients. The diagnosis needs signet ring cells in more than 50% of the tumour.
- **Serrated adenocarcinoma** (8213/3): The WHO digestive volume separates the serrated neoplastic pathway of the colon, rectum and appendix. No file in this part names serrated adenocarcinoma or reports it in children.
- **Adenocarcinoma in adenomatous polyposis coli** (8220/3): Familial adenomatous polyposis is a WHO digestive tumour syndrome and an APC-associated polyposis syndrome of children. No file in this part reports carcinoma in it before age 19. On 8 October 2026 the colon, rectosigmoid junction and rectum (C18.0, C18.2 to C18.9, C19.9, C20.9) moved to their own entity, an option, because Polat 2021 and Mahajan 2022 report colorectal carcinoma arising in familial adenomatous polyposis in children; no paper added that day reports it at the other sites in a child.
- **Adenocarcinoma in familial adenomatous polyposis (colon, rectosigmoid junction and rectum)** (8220/3): Mahajan 2022 states that 10% to 30% of reported childhood colorectal carcinomas arise in hereditary cancer syndromes, most often familial adenomatous polyposis and Lynch syndrome. Polat 2021 names familial adenomatous polyposis as the commonest predisposing factor of colorectal carcinoma in children.
- **Tubular adenocarcinoma** (8211/3): The commonest gastric adenocarcinoma subtype in the WHO 5th edition. No paediatric report in this part. On 8 October 2026 the colon, rectosigmoid junction and rectum (C18.0, C18.2 to C18.9, C19.9, C20.9) moved to their own entity, an option, because Polat 2021 reports a tubular adenocarcinoma component in the colorectal carcinoma of a 16-year-old; no paper added that day reports it at the other sites in a child.
- **Tubular adenocarcinoma (colon, rectosigmoid junction and rectum)** (8211/3): Polat 2021 reports a colorectal carcinoma with mucinous and tubular adenocarcinoma components in a 16-year-old (Table 1, MA + TA). That tumour records 8480/3 under the higher-code rule; no paediatric report gives tubular adenocarcinoma as the only type (data gap 8).
- **Papillary adenocarcinoma NOS** (8260/3): A WHO 5th-edition gastric adenocarcinoma subtype. No paediatric report in this part.
- **Adenocarcinoma with mixed subtypes (mixed adenocarcinoma)** (8255/3): A WHO 5th-edition gastric adenocarcinoma subtype: a poorly cohesive component with another distinct component. No paediatric report in this part.
- **Micropapillary carcinoma NOS** (8265/3): A WHO 5th-edition gastric adenocarcinoma subtype. No paediatric report in this part.
- **Hepatoid adenocarcinoma** (8576/3): A WHO 5th-edition gastric adenocarcinoma subtype of hepatocyte-like cells expressing alpha fetoprotein. No paediatric report in this part.
- **Parietal cell carcinoma** (8214/3): A rare WHO 5th-edition gastric adenocarcinoma subtype. No paediatric report in this part.
- **Mucoepidermoid carcinoma** (8430/3): A rare WHO 5th-edition oesophageal and gastric carcinoma. No paediatric report in this part.
- **Paneth cell carcinoma** (no code): ICCR Stomach Table 3 lists Paneth cell carcinoma as a WHO 5th-edition gastric subtype with no ICD-O code.
- **Medullary carcinoma with lymphoid stroma (gastric carcinoma with lymphoid stroma)** (8512/3): ICCR Stomach Table 3 prints 8512/3, but its only ICD-O-3.2 term is [obs]. ICD-O-3.2 holds 8510/3 Medullary carcinoma, NOS and 8082/3 Lymphoepithelial carcinoma; neither source names a successor, so the registrar rules.
- **Squamous cell carcinoma NOS** (8070/3): The main oesophageal carcinoma and the main anal carcinoma, where HPV infection drives it. No paediatric report in this part.
- **Verrucous squamous cell carcinoma** (8051/3): A WHO 5th-edition oesophageal squamous subtype. No paediatric report in this part.
- **Squamous cell carcinoma, spindle cell** (8074/3): A WHO 5th-edition oesophageal squamous subtype. No paediatric report in this part.
- **Basaloid squamous cell carcinoma** (8083/3): A WHO 5th-edition oesophageal squamous subtype. No paediatric report in this part.
- **Lymphoepithelioma-like carcinoma** (8082/3): A WHO 5th-edition oesophageal subtype of undifferentiated carcinoma. No paediatric report in this part.
- **Adenoid cystic carcinoma** (8200/3): A WHO 5th-edition oesophageal carcinoma. No paediatric report in this part.
- **Adenosquamous carcinoma** (8560/3): A WHO 5th-edition oesophageal and gastric carcinoma; in the stomach the squamous component is at least 25%. No paediatric report in this part.
- **Carcinoma, undifferentiated, NOS** (8020/3): A WHO 5th-edition oesophageal and gastric carcinoma. No paediatric report in this part.
- **Large cell carcinoma with rhabdoid phenotype** (8014/3): A WHO 5th-edition gastric undifferentiated carcinoma subtype. No paediatric report in this part.
- **Pleomorphic carcinoma** (8022/3): A WHO 5th-edition gastric undifferentiated carcinoma subtype. No paediatric report in this part.
- **Sarcomatoid carcinoma** (8033/3): A WHO 5th-edition gastric undifferentiated carcinoma subtype. No paediatric report in this part.
- **Carcinoma with osteoclast-like giant cells** (8035/3): A WHO 5th-edition gastric undifferentiated carcinoma subtype. No paediatric report in this part.
- **Solid pseudopapillary neoplasm** (8452/3): The WHO paediatric volume lists solid pseudopapillary neoplasm among pancreatic tumours of children; Stanley 2015 reports it in a 14-year-old girl. ICD-O-3.2 codes it /3 at the pancreas and /1 at the ovary. Paediatric papers added 8 October 2026: Ebrahim 2025 reports four paediatric cases, aged 8 to 14, among 60 solid pseudopapillary neoplasms; the tumour of the one boy lacked nuclear beta-catenin (data gap 9).
- **Pancreatic acinar cell carcinoma** (8550/3): The WHO paediatric volume lists pancreatic acinar cell carcinoma among pancreatic tumours of children.
- **Pancreatoblastoma** (8971/3): Pancreatoblastoma is a paediatric tumour of the first decade. ICCC-2017 places 8971 in XIIa2 at every site, so it is recorded in Group 12.
- **Pancreatic ductal adenocarcinoma (infiltrating duct carcinoma)** (8500/3): ICD-O attaches breast topography to infiltrating duct carcinoma; a primary in the pancreas is coded C25 (Rule H). No paediatric report in this part.
- **Mucinous cystic neoplasm with an associated invasive carcinoma (mucinous cystadenocarcinoma)** (8470/3): ICD-O Table 23 lists the pancreas as another primary site of mucinous cystadenocarcinoma. No paediatric report in this part.
- **Intraductal papillary mucinous neoplasm with an associated invasive carcinoma** (8453/3): The invasive form of a WHO pancreatic precursor lesion. No paediatric report in this part.
- **Gastroblastoma** (8976/3): Gastroblastoma arises in the stomach of children and young adults and carries a MALAT1::GLI1 fusion. ICCR Stomach prints 8976/3 with an asterisk (approved by IARC in April 2019); ICD-O-3.2 and ICCC-2017 hold no 8976, so it is not built until the registrar rules.
- **Serrated dysplasia, high grade (stomach)** (8213/2): ICCR Stomach Table 3 prints 8213/2 with an asterisk; ICD-O-3.2 holds 8213 at /0 and /3 only. It is in situ and outside the malignant scope either way.
- **Intestinal-type adenoma, high grade (stomach)** (8144/2): ICCR Stomach Table 3 prints 8144/2 with an asterisk; ICD-O-3.2 holds 8144 at /0 and /3 only. It is in situ and outside the malignant scope either way.
- **Cholangiocarcinoma (bile duct carcinoma), extrahepatic bile ducts and gallbladder** (8160/3): Bile duct carcinoma is a histological type, not a site (Rule H). ICCC-2017 places 8160 to 8162 in VIIb, hepatic carcinomas, at every site, so a cholangiocarcinoma of the extrahepatic bile ducts or gallbladder is recorded in Group 7.
- **Perihilar cholangiocarcinoma (Klatskin tumour)** (8162/3): ICCC-2017 places 8162 in VIIb at every site. Klatskin tumor is an [obs] synonym in ICD-O-3.2.
- **Cloacogenic carcinoma** (8124/3): Every ICD-O-3.2 term at 8124/3 is [obs]. The WHO digestive volume describes HPV-driven anal squamous lesions and names no cloacogenic entity; ICD-O-3.2 prints no successor, so none is assigned.
- **Gastrointestinal stromal tumour** (8936/3): The WHO paediatric volume lists paediatric gastrointestinal stromal tumour. ICCC-2017 places 8936 in XIIa1, so it is recorded in Group 12.
- **Burkitt lymphoma and other lymphomas of the digestive tract** (9687/3): Burkitt lymphoma is a high-grade lymphoma of children. ICCC-2017 places 9687 in IIc at every digestive site.
- **EBV-positive inflammatory follicular dendritic cell sarcoma of the digestive tract** (9758/3): A WHO 5th-edition digestive entity. ICCC-2017 places 9758 in IId, so it is recorded in Group 2.
- **Gastrointestinal clear cell sarcoma** (9044/3): Its EWSR1 fusion must be shown for the diagnosis. ICCC-2017 places 9044 in IXd7, so it is recorded in Group 9.
- **Adenomatous polyp, low-grade dysplasia** (8210/0): Benign. Outside the malignant scope.
- **Adenomatous polyp, high-grade dysplasia** (8210/2): In situ. The WHO digestive volume does not recommend the term carcinoma in situ in the tubal gut; the lesion is reported as high-grade dysplasia. Paediatric papers added 8 October 2026: Polat 2021 found adenomatous polyps with high-grade dysplasia in the colon of a 16-year-old after resection of a colorectal carcinoma.
- **Conventional adenoma (tubular adenoma)** (8211/0): Benign precursor lesion of the large and small bowel. Outside the malignant scope.
- **Sessile serrated lesion; serrated dysplasia, low grade** (8213/0): Benign serrated precursor lesion; the WHO 5th edition renamed sessile serrated polyp/adenoma sessile serrated lesion.
- **Intestinal-type adenoma, low grade** (8144/0): Benign gastric precursor lesion. Outside the malignant scope.
- **Familial adenomatous polyposis with no carcinoma** (8220/0): APC-associated polyposis is a cancer predisposition syndrome of children. The polyps are benign; only a carcinoma arising in them is registered (8220/3, in the picker). Paediatric papers added 8 October 2026: Polat 2021 names familial adenomatous polyposis as the commonest predisposing factor of colorectal carcinoma in children.
- **Glandular dysplasia (intraepithelial neoplasia), low grade** (8148/0): Benign precursor lesion. Outside the malignant scope.
- **Glandular dysplasia (intraepithelial neoplasia), high grade; biliary or pancreatic intraepithelial neoplasia, high grade** (8148/2): In situ. Dysplasia is the WHO term in the tubal gut; intra-epithelial neoplasia in the pancreas, gallbladder and biliary tree.
- **Squamous dysplasia (intraepithelial neoplasia), low grade (oesophagus, anus)** (8077/0): Benign precursor lesion. Outside the malignant scope.
- **Squamous dysplasia (intraepithelial neoplasia), high grade (oesophagus, anus)** (8077/2): In situ. ICCR Oesophagus Table 1 prints this row as 'low grade' 8077/2, a printing error: 8077/2 is high grade.
- **Squamous cell papilloma (oesophagus)** (8052/0): Benign. Outside the malignant scope.
- **Squamous papillomatosis (oesophagus)** (8060/0): Benign. Outside the malignant scope.
- **Intraductal papillary mucinous neoplasm with low-grade dysplasia** (8453/0): The WHO 5th edition grades pancreatic precursor lesions in two tiers. Low grade is benign.
- **Intraductal papillary mucinous neoplasm with high-grade dysplasia** (8453/2): In situ. Outside the malignant scope.
- **Mucinous cystic neoplasm with low-grade dysplasia** (8470/0): Benign. Outside the malignant scope.
- **Mucinous cystic neoplasm with high-grade dysplasia** (8470/2): In situ. Outside the malignant scope.

## 3 The pathway

Node prefix `dg_`. Order: site, then evidence gate, then the histology screen for that site.

```
dg_site → dg_document_inventory → clinical / imaging: 8000/3 (basis 1 or 2)
                                 → dg_marker (basis 4)
                                 → dg_cytology (basis 5) → named type → dg_histology_by_site
                                 → dg_histology_by_site (basis 7)
dg_histology_by_site: appendix → dg_appendix_histology → dg_net_grade
                      colon, rectosigmoid, rectum, anus → dg_colorectal_histology
                      oesophagus → dg_oesophagus_histology
                      stomach → dg_stomach_histology
                      small intestine → dg_small_intestine_histology
                      gallbladder, extrahepatic bile duct, ampulla → dg_biliary_histology
                      pancreas → dg_pancreas_histology → dg_pancreas_ihc
                      overlapping digestive (C26.8) → dg_carcinoma_picker
every histology screen → dg_carcinoma_picker, dg_not_malignant_gut or dg_not_malignant_pancreatobiliary, and referrals
```

`dg_histology_by_site` is not a screen. It is the site-keyed jump the controller binds from the answer given at `dg_site`; the clerk sees no second site question. In approach 3 the appendix and colorectal screens belong to the colorectum-with-appendix organ tree; the oesophagus, stomach, small intestine, biliary and pancreas screens are site-specific short screens inside the general carcinoma tree. The melanoma answer jumps to the melanoma tree, whose node id the controller binds. The metastasis answer refers with `recapture_site: true` and no group, as the brief specifies; the checker reports these eight answers as `bad_refer` because it expects a group number.

### `dg_site` (site_resolution)

**Question:** Which part of the digestive tract does the report name as the site of the tumour?

**Hint:** Choose the part where the tumour began. If one tumour spans two parts of an organ and the report does not say where it began, choose that organ with no part named; a carcinoma of the stomach and small intestine is an overlapping lesion of the digestive system. A report that names only the tissue around an organ, such as peripancreatic tissue, does not name that organ.

| Answer | Records | Basis | Reason shown | Recognition aid | Source |
|---|---|---|---|---|---|
| Appendix | go to `dg_document_inventory` |  | Site recorded as appendix (C18.1). |  |  |
| Colon: caecum, ascending, hepatic flexure, transverse, splenic flexure, descending or sigmoid colon | go to `dg_document_inventory` |  | Site recorded as the part of the colon the report names (C18.0, C18.2 to C18.7). |  |  |
| Colon, with no part named, or a tumour spanning two parts of the colon | go to `dg_document_inventory` |  | Site recorded as colon, NOS (C18.9), or overlapping lesion of colon (C18.8). |  | ICD-O-3.1 manual, PDF p. 5 (printed p. 18) |
| Rectosigmoid junction | go to `dg_document_inventory` |  | Site recorded as rectosigmoid junction (C19.9). |  |  |
| Rectum | go to `dg_document_inventory` |  | Site recorded as rectum (C20.9). |  |  |
| Anus or anal canal, or a tumour spanning rectum, anus and anal canal | go to `dg_document_inventory` |  | Site recorded as anus or anal canal (C21.0 to C21.2), or overlapping lesion of rectum, anus and anal canal (C21.8). |  | ICD-O-3.1 manual, PDF p. 5 (printed p. 18) |
| Oesophagus | go to `dg_document_inventory` |  | Site recorded as the part of the oesophagus the report names (C15.0 to C15.9). |  |  |
| Stomach, including a tumour of the oesophagus and stomach together | go to `dg_document_inventory` |  | Site recorded as the part of the stomach the report names (C16.0 to C16.9); a carcinoma of oesophagus and stomach is indexed to cardia (C16.0). |  | ICD-O-3.1 manual, PDF p. 5 (printed p. 18) |
| Small intestine: duodenum, jejunum or ileum | go to `dg_document_inventory` |  | Site recorded as the part of the small intestine the report names (C17.0 to C17.9). |  |  |
| Gallbladder | go to `dg_document_inventory` |  | Site recorded as gallbladder (C23.9). |  |  |
| Extrahepatic bile duct or ampulla of Vater | go to `dg_document_inventory` |  | Site recorded as extrahepatic bile duct (C24.0), ampulla of Vater (C24.1), or biliary tract (C24.8, C24.9). |  | ICD-O-3.1 manual, PDF p. 5 (printed p. 18) |
| Pancreas | go to `dg_document_inventory` |  | Site recorded as the part of the pancreas the report names (C25.0 to C25.9). |  |  |
| Two digestive organs, and the report does not say where the tumour began | go to `dg_document_inventory` |  | Site recorded as overlapping lesion of digestive system (C26.8). |  | ICD-O-3.1 manual, PDF p. 5 (printed p. 18) |
| Liver, or bile ducts inside the liver | refer to Group 7 |  | A carcinoma of the liver is recorded in Group 7, hepatic tumours. |  |  |
| Tissue beside an organ, such as peripancreatic or retrocaecal tissue, or a region such as the abdomen | refer, site asked again |  | Tissue beside an organ is not that organ. ICD-O lists peripancreatic and retrocaecal tissue under retroperitoneum (C48.0). The next screen asks the site again. |  | ICD-O-3.1 manual, PDF p. 4 (printed p. 17); ICD-O-3.1 manual, PDF p. 1 (printed p. 14) |

### `dg_document_inventory` (document_inventory)

**Question:** What is in the file for this tumour?

**Hint:** Choose the strongest evidence the file holds. A report that calls the tumour possible, probable or suspected does not register it.

| Answer | Records | Basis | Reason shown | Recognition aid | Source |
|---|---|---|---|---|---|
| A referral letter or clinical note that states a malignant tumour, with no imaging report and no tissue report | 8000/3 | 1 | Recorded as Neoplasm, malignant (8000/3). Basis of diagnosis: clinical. |  |  |
| An imaging report that states a malignant tumour, with no tissue report | 8000/3 | 2 | Recorded as Neoplasm, malignant (8000/3). Basis of diagnosis: imaging. |  | Stanley 2015, PDF p. 4 |
| An imaging report that shows the tumour, and a raised chromogranin A or hormone result | go to `dg_marker` | 4 |  |  |  |
| A note or report that calls the tumour possible, probable or suspected | not registrable |  | A possible, probable or suspected tumour is not registered until a report states it. |  | Stanley 2015, PDF p. 1 |
| A cytology report (fine needle aspiration or brushings) | go to `dg_cytology` | 5 |  |  |  |
| A histology report on a biopsy or resection, with or without immunohistochemistry or gene reports | go to `dg_histology_by_site` | 7 |  |  |  |

### `dg_marker` (lab_results)

**Question:** Which raised result does the file give, together with imaging that shows the tumour?

**Hint:** A raised result counts only when an imaging report shows the tumour. A raised result with no imaging that shows a tumour does not register it.

| Answer | Records | Basis | Reason shown | Recognition aid | Source |
|---|---|---|---|---|---|
| Chromogranin A | 8240/3 | 4 | Recorded as Neuroendocrine tumor, NOS (8240/3). Basis of diagnosis: tumour marker. |  |  |
| Insulin | 8151/3 | 4 | Recorded as Insulinoma, NOS (8151/3). Basis of diagnosis: tumour marker. |  |  |
| Glucagon | 8152/3 | 4 | Recorded as Glucagonoma (8152/3). Basis of diagnosis: tumour marker. |  |  |
| Gastrin | 8153/3 | 4 | Recorded as Gastrinoma (8153/3). Basis of diagnosis: tumour marker. |  |  |
| Vasoactive intestinal peptide | 8155/3 | 4 | Recorded as Vipoma (8155/3). Basis of diagnosis: tumour marker. |  |  |
| Somatostatin | 8156/3 | 4 | Recorded as Somatostatinoma (8156/3). Basis of diagnosis: tumour marker. |  |  |
| Serotonin | 8241/3 | 4 | Recorded as Enterochromaffin cell carcinoid (8241/3). Basis of diagnosis: tumour marker. |  |  |
| Adrenocorticotropic hormone | 8158/3 | 4 | Recorded as ACTH-producing tumor (8158/3). Basis of diagnosis: tumour marker. |  |  |
| Another raised result, and the imaging report states a malignant tumour | 8000/3 | 2 | Recorded as Neoplasm, malignant (8000/3). Basis of diagnosis: imaging. |  |  |
| A raised result, and no imaging report shows a tumour | not registrable |  | A raised result with no imaging that shows a tumour does not register it. |  |  |

### `dg_cytology` (morphology_only)

**Question:** What does the cytology report call the tumour?

| Answer | Records | Basis | Reason shown | Recognition aid | Source |
|---|---|---|---|---|---|
| A named tumour type, such as solid pseudopapillary neoplasm, neuroendocrine tumour or adenocarcinoma | go to `dg_histology_by_site` | 5 | The next screen records the named type. Basis of diagnosis: cytology. |  |  |
| Carcinoma, with no type named | 8010/3 | 5 | Recorded as Carcinoma, NOS (8010/3). Basis of diagnosis: cytology. |  |  |
| Malignant, with no tumour type named | 8000/3 | 5 | Recorded as Neoplasm, malignant (8000/3). Basis of diagnosis: cytology. |  |  |
| Lymphoma | refer to Group 2 |  | Lymphoma is recorded in Group 2, lymphomas and reticuloendothelial neoplasms. |  |  |
| Suspicious for malignancy, atypical, benign or non-diagnostic | not registrable |  | A cytology report that does not state malignancy does not register the tumour. |  |  |

### `dg_appendix_histology` (morphology_only)

**Question:** What does the histology report call the tumour?

**Hint:** When the report gives two tumour types for one tumour and no answer covers both, choose the answer with the higher code.

| Answer | Records | Basis | Reason shown | Recognition aid | Source |
|---|---|---|---|---|---|
| Neuroendocrine tumour, or carcinoid | go to `dg_net_grade` |  |  | The report calls the tumour well differentiated and may give a grade (G1, G2 or G3), a Ki-67 index or a mitotic count. | Pfister 2022, PDF p. 13; Nagtegaal 2020, PDF p. 4; Roganovic 2026, PMC section 1; Roganovic 2026, PMC section 4 |
| Low-grade appendiceal mucinous neoplasm, with no invasion stated | exclusion 8480/1 |  | Not registered: Low grade appendiceal mucinous neoplasm (8480/1) is not malignant. If the report states invasion or calls the tumour malignant, choose the carcinoma answer. |  | Nagtegaal 2020, PDF p. 4; ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |
| Another carcinoma the report names, such as goblet cell adenocarcinoma, mucinous adenocarcinoma, adenocarcinoma or neuroendocrine carcinoma | go to `dg_carcinoma_picker` |  |  |  |  |
| An adenoma, a serrated lesion, dysplasia or another non-invasive lesion | go to `dg_not_malignant_gut` |  |  |  |  |
| Lymphoma, such as Burkitt lymphoma | refer to Group 2 |  | Lymphoma is recorded in Group 2, lymphomas and reticuloendothelial neoplasms. |  | Pfister 2022, PDF p. 6 |
| Sarcoma, such as rhabdomyosarcoma or clear cell sarcoma | refer to Group 9 |  | A sarcoma is recorded in Group 9, soft-tissue and other extraosseous sarcomas. |  | Nagtegaal 2020, PDF p. 3 |
| Melanoma | go to `melanoma tree entry (controller binds the node id)` |  | Melanoma at any site is recorded through the melanoma questions. |  |  |
| A deposit (metastasis) of a tumour that began elsewhere | refer, site asked again |  | A deposit is recorded at the site where the tumour began. The next screen asks that site. |  | ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |

### `dg_net_grade` (histology_subclassification)

**Question:** Which grade does the report give the neuroendocrine tumour?

**Hint:** If the report gives two grades, or the Ki-67 index and the mitotic count point to different grades, choose the higher grade. A neuroendocrine carcinoma (poorly differentiated, small cell or large cell) is the last answer.

| Answer | Records | Basis | Reason shown | Recognition aid | Source |
|---|---|---|---|---|---|
| Grade 1 (G1) | 8240/3 | 7 | Recorded as Neuroendocrine tumor, NOS (8240/3); ICD-O-3.2 lists neuroendocrine tumour, grade 1 under this code. | Ki-67 index below 3% and fewer than 2 mitoses per 2 mm². | Nagtegaal 2020, PDF p. 4; Roganovic 2026, PMC section 4 |
| Grade 2 (G2), or atypical carcinoid | 8249/3 | 7 | Recorded as Neuroendocrine tumor, grade 2 (8249/3). | Ki-67 index from 3% to 20%, or 2 to 20 mitoses per 2 mm². | Nagtegaal 2020, PDF p. 4; Roganovic 2026, PMC section 4 |
| Grade 3 (G3), and the report still calls the tumour well differentiated | 8249/3 | 7 | Recorded as Neuroendocrine tumor, grade 2 (8249/3); ICD-O-3.2 lists neuroendocrine tumour, grade 3 under this code. | Ki-67 index above 20%, or more than 20 mitoses per 2 mm², in a tumour the report calls well differentiated. | Nagtegaal 2020, PDF p. 4; Nagtegaal 2020, PDF p. 5 |
| No grade stated, or carcinoid with no grade | 8240/3 | 7 | Recorded as Neuroendocrine tumor, NOS (8240/3). |  | Nagtegaal 2020, PDF p. 4; Roganovic 2026, PMC section 1 |
| Neuroendocrine carcinoma (poorly differentiated, small cell or large cell), or a mixed tumour with a neuroendocrine component | go to `dg_carcinoma_picker` |  |  |  | Nagtegaal 2020, PDF p. 4; Nagtegaal 2020, PDF p. 5 |

### `dg_colorectal_histology` (morphology_only)

**Question:** What does the histology report call the tumour?

**Hint:** When the report gives two tumour types for one tumour and no answer covers both, choose the answer with the higher code.

| Answer | Records | Basis | Reason shown | Recognition aid | Source |
|---|---|---|---|---|---|
| Mucinous adenocarcinoma, or colloid carcinoma | 8480/3 | 7 | Recorded as Mucinous adenocarcinoma (8480/3). | Tumour cells floating in pools of extracellular mucin. | Mahajan 2022, PMC section 1; Polat 2021, PMC section 2; Mahajan 2022, PMC section 5; Mahajan 2022, PMC section 4 |
| Signet ring cell carcinoma, or signet ring cell variant of adenocarcinoma | 8490/3 | 7 | Recorded as Signet ring cell carcinoma (8490/3). | Tumour cells holding mucin inside the cell; signet ring cells make up more than half of the tumour. | Mahajan 2022, PMC section 1; Mahajan 2022, PMC section 5; Mahajan 2022, PMC section 4 |
| Adenocarcinoma with no subtype named, including poorly differentiated adenocarcinoma | 8140/3 | 7 | Recorded as Adenocarcinoma, NOS (8140/3). |  | Polat 2021, PMC section 2; Mahajan 2022, PMC section 4 |
| Adenocarcinoma arising in familial adenomatous polyposis | 8220/3 | 7 | Recorded as Adenocarcinoma in adenomatous polyposis coli (8220/3). |  | Mahajan 2022, PMC section 5; Polat 2021, PMC section 3 |
| Tubular adenocarcinoma | 8211/3 | 7 | Recorded as Tubular adenocarcinoma (8211/3). |  | Polat 2021, PMC section 2 |
| Another carcinoma or neuroendocrine tumour the report names, such as serrated adenocarcinoma, squamous cell carcinoma or carcinoid | go to `dg_carcinoma_picker` |  |  |  |  |
| An adenoma, a polyp, a serrated lesion, polyposis, dysplasia or another non-invasive lesion | go to `dg_not_malignant_gut` |  |  |  |  |
| Lymphoma, such as Burkitt lymphoma | refer to Group 2 |  | Lymphoma is recorded in Group 2, lymphomas and reticuloendothelial neoplasms. |  | Pfister 2022, PDF p. 6 |
| Gastrointestinal stromal tumour (GIST) | refer to Group 12 (8936/3) |  | Gastrointestinal stromal tumor (8936/3) is recorded in Group 12, other and unspecified malignant tumours. |  | Pfister 2022, PDF p. 9 |
| Sarcoma, such as rhabdomyosarcoma or clear cell sarcoma | refer to Group 9 |  | A sarcoma is recorded in Group 9, soft-tissue and other extraosseous sarcomas. |  | Nagtegaal 2020, PDF p. 3 |
| Melanoma | go to `melanoma tree entry (controller binds the node id)` |  | Melanoma at any site is recorded through the melanoma questions. |  |  |
| A deposit (metastasis) of a tumour that began elsewhere | refer, site asked again |  | A deposit is recorded at the site where the tumour began. The next screen asks that site. |  | ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |

### `dg_pancreas_histology` (morphology_only)

**Question:** What does the histology report call the tumour?

**Hint:** When the report gives two terms for one tumour and no single answer covers both, choose the answer with the higher code; this includes a hormone type, or non-functioning, given together with a grade, such as insulinoma, grade 2.

| Answer | Records | Basis | Reason shown | Recognition aid | Source |
|---|---|---|---|---|---|
| Non-functioning pancreatic neuroendocrine tumour | 8150/3 | 7 | Recorded as Pancreatic neuroendocrine tumor, nonfunctioning (8150/3). |  | Karges 2025, PMC section 1; Karges 2025, PMC section 11 |
| Insulinoma | 8151/3 | 7 | Recorded as Insulinoma, NOS (8151/3). |  | Karges 2025, PMC section 2; Karges 2025, PMC section 11; Karges 2025, PMC section 7 |
| Solid pseudopapillary neoplasm, or solid pseudopapillary tumour | 8452/3 | 7 | Recorded as Solid pseudopapillary neoplasm of pancreas (8452/3). | Uniform epithelioid cells around a delicate fibrovascular network, with nuclear beta-catenin staining. | Pfister 2022, PDF p. 13; Stanley 2015, PDF p. 2; Stanley 2015, PDF p. 3; Ebrahim 2025, PMC section 13 |
| Acinar cell carcinoma | 8550/3 | 7 | Recorded as Acinar cell carcinoma (8550/3). |  | Pfister 2022, PDF p. 13 |
| Neuroendocrine tumour, grade 1, or with no grade stated | 8240/3 | 7 | Recorded as Neuroendocrine tumor, NOS (8240/3); ICD-O-3.2 lists neuroendocrine tumour, grade 1 under this code. |  | Karges 2025, PMC section 8; Karges 2025, PMC section 9 |
| Neuroendocrine tumour, grade 2 or grade 3 (well differentiated) | 8249/3 | 7 | Recorded as Neuroendocrine tumor, grade 2 (8249/3); ICD-O-3.2 lists neuroendocrine tumour, grade 3 under this code. |  | Karges 2025, PMC section 9; Karges 2025, PMC section 8 |
| Neuroendocrine carcinoma (poorly differentiated), with no small cell or large cell type named | 8246/3 | 7 | Recorded as Neuroendocrine carcinoma, NOS (8246/3). |  | Karges 2025, PMC section 9 |
| Gastrinoma | 8153/3 | 7 | Recorded as Gastrinoma (8153/3). |  | Karges 2025, PMC section 7; Karges 2025, PMC section 2 |
| Glucagonoma | 8152/3 | 7 | Recorded as Glucagonoma (8152/3). |  | Karges 2025, PMC section 2 |
| VIPoma | 8155/3 | 7 | Recorded as Vipoma (8155/3). |  | Karges 2025, PMC section 2 |
| Somatostatinoma | 8156/3 | 7 | Recorded as Somatostatinoma (8156/3). |  | Karges 2025, PMC section 2 |
| Pancreatoblastoma | refer to Group 12 (8971/3) |  | Pancreatoblastoma (8971/3) is recorded in Group 12, other and unspecified malignant tumours. |  | Pfister 2022, PDF p. 11 |
| The report describes the tumour and its immunohistochemistry but names no tumour type | go to `dg_pancreas_ihc` |  |  |  |  |
| Another carcinoma or neuroendocrine tumour the report names, such as ductal adenocarcinoma, small cell carcinoma or ACTH-producing tumour | go to `dg_carcinoma_picker` |  |  |  |  |
| An intraductal papillary mucinous neoplasm, a mucinous cystic neoplasm, intraepithelial neoplasia or another non-invasive lesion | go to `dg_not_malignant_pancreatobiliary` |  |  |  |  |
| Lymphoma, such as Burkitt lymphoma | refer to Group 2 |  | Lymphoma is recorded in Group 2, lymphomas and reticuloendothelial neoplasms. |  | Pfister 2022, PDF p. 6 |
| Sarcoma, such as rhabdomyosarcoma or clear cell sarcoma | refer to Group 9 |  | A sarcoma is recorded in Group 9, soft-tissue and other extraosseous sarcomas. |  | Nagtegaal 2020, PDF p. 3 |
| A deposit (metastasis) of a tumour that began elsewhere | refer, site asked again |  | A deposit is recorded at the site where the tumour began. The next screen asks that site. |  | ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |

### `dg_pancreas_ihc` (ihc_checklist)

**Question:** Which immunohistochemistry results does the report give?

**Hint:** Mark each marker the report gives as positive or negative. Immunohistochemistry is read with the histology report; it does not replace it.

| Answer | Records | Basis | Reason shown | Recognition aid | Source |
|---|---|---|---|---|---|
| Nuclear beta-catenin positive, chromogranin negative and trypsin negative | 8452/3 | 7 | Recorded as Solid pseudopapillary neoplasm of pancreas (8452/3). |  | Stanley 2015, PDF p. 2; Stanley 2015, PDF p. 3 |
| The results match no answer above, and the report states the tumour is malignant | 8000/3 | 7 | Recorded as Neoplasm, malignant (8000/3). |  |  |
| The results match no answer above, and the report does not state the tumour is malignant | not registrable |  | A tumour the report does not call malignant or name is not registered. |  |  |

### `dg_stomach_histology` (morphology_only)

**Question:** What does the histology report call the tumour?

**Hint:** When the report gives two tumour types for one tumour and no answer covers both, choose the answer with the higher code.

| Answer | Records | Basis | Reason shown | Recognition aid | Source |
|---|---|---|---|---|---|
| Adenocarcinoma, poorly cohesive carcinoma, signet ring cell carcinoma, neuroendocrine tumour or another carcinoma the report names | go to `dg_carcinoma_picker` |  |  |  |  |
| An adenoma, a polyp, dysplasia or intraepithelial neoplasia, or another non-invasive lesion | go to `dg_not_malignant_gut` |  |  |  |  |
| Lymphoma, such as Burkitt lymphoma | refer to Group 2 |  | Lymphoma is recorded in Group 2, lymphomas and reticuloendothelial neoplasms. |  | Pfister 2022, PDF p. 6 |
| Gastrointestinal stromal tumour (GIST) | refer to Group 12 (8936/3) |  | Gastrointestinal stromal tumor (8936/3) is recorded in Group 12, other and unspecified malignant tumours. |  | Pfister 2022, PDF p. 9 |
| Sarcoma, such as rhabdomyosarcoma or clear cell sarcoma | refer to Group 9 |  | A sarcoma is recorded in Group 9, soft-tissue and other extraosseous sarcomas. |  | Nagtegaal 2020, PDF p. 3 |
| Melanoma | go to `melanoma tree entry (controller binds the node id)` |  | Melanoma at any site is recorded through the melanoma questions. |  |  |
| A deposit (metastasis) of a tumour that began elsewhere | refer, site asked again |  | A deposit is recorded at the site where the tumour began. The next screen asks that site. |  | ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |

### `dg_oesophagus_histology` (morphology_only)

**Question:** What does the histology report call the tumour?

**Hint:** When the report gives two tumour types for one tumour and no answer covers both, choose the answer with the higher code.

| Answer | Records | Basis | Reason shown | Recognition aid | Source |
|---|---|---|---|---|---|
| Squamous cell carcinoma, adenocarcinoma, neuroendocrine tumour or another carcinoma the report names | go to `dg_carcinoma_picker` |  |  |  |  |
| A papilloma, dysplasia or intraepithelial neoplasia, or another non-invasive lesion | go to `dg_not_malignant_gut` |  |  |  |  |
| Lymphoma, such as Burkitt lymphoma | refer to Group 2 |  | Lymphoma is recorded in Group 2, lymphomas and reticuloendothelial neoplasms. |  | Pfister 2022, PDF p. 6 |
| Gastrointestinal stromal tumour (GIST) | refer to Group 12 (8936/3) |  | Gastrointestinal stromal tumor (8936/3) is recorded in Group 12, other and unspecified malignant tumours. |  | Pfister 2022, PDF p. 9 |
| Sarcoma, such as rhabdomyosarcoma or clear cell sarcoma | refer to Group 9 |  | A sarcoma is recorded in Group 9, soft-tissue and other extraosseous sarcomas. |  | Nagtegaal 2020, PDF p. 3 |
| Melanoma | go to `melanoma tree entry (controller binds the node id)` |  | Melanoma at any site is recorded through the melanoma questions. |  |  |
| A deposit (metastasis) of a tumour that began elsewhere | refer, site asked again |  | A deposit is recorded at the site where the tumour began. The next screen asks that site. |  | ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |

### `dg_small_intestine_histology` (morphology_only)

**Question:** What does the histology report call the tumour?

**Hint:** When the report gives two tumour types for one tumour and no answer covers both, choose the answer with the higher code.

| Answer | Records | Basis | Reason shown | Recognition aid | Source |
|---|---|---|---|---|---|
| Adenocarcinoma, neuroendocrine tumour or another carcinoma the report names | go to `dg_carcinoma_picker` |  |  |  | Nagtegaal 2020, PDF p. 2 |
| An adenoma, a polyp, dysplasia or another non-invasive lesion | go to `dg_not_malignant_gut` |  |  |  |  |
| Lymphoma, such as Burkitt lymphoma | refer to Group 2 |  | Lymphoma is recorded in Group 2, lymphomas and reticuloendothelial neoplasms. |  | Pfister 2022, PDF p. 6 |
| Gastrointestinal stromal tumour (GIST) | refer to Group 12 (8936/3) |  | Gastrointestinal stromal tumor (8936/3) is recorded in Group 12, other and unspecified malignant tumours. |  | Pfister 2022, PDF p. 9 |
| Sarcoma, such as rhabdomyosarcoma or clear cell sarcoma | refer to Group 9 |  | A sarcoma is recorded in Group 9, soft-tissue and other extraosseous sarcomas. |  | Nagtegaal 2020, PDF p. 3 |
| Melanoma | go to `melanoma tree entry (controller binds the node id)` |  | Melanoma at any site is recorded through the melanoma questions. |  |  |
| A deposit (metastasis) of a tumour that began elsewhere | refer, site asked again |  | A deposit is recorded at the site where the tumour began. The next screen asks that site. |  | ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |

### `dg_biliary_histology` (morphology_only)

**Question:** What does the histology report call the tumour?

**Hint:** Bile duct carcinoma names a tumour type, not a site: keep the site the report states.

| Answer | Records | Basis | Reason shown | Recognition aid | Source |
|---|---|---|---|---|---|
| Cholangiocarcinoma, bile duct carcinoma or bile duct adenocarcinoma | refer to Group 7 (8160/3) |  | Cholangiocarcinoma (8160/3) is recorded in Group 7, hepatic tumours, at every site. |  | ICD-O-3.1 manual, PDF p. 11 (printed p. 24) |
| Perihilar cholangiocarcinoma, or Klatskin tumour | refer to Group 7 (8162/3) |  | Perihilar cholangiocarcinoma (8162/3) is recorded in Group 7, hepatic tumours, at every site. |  |  |
| Adenocarcinoma of the gallbladder or ampulla, neuroendocrine tumour, or another carcinoma the report names | go to `dg_carcinoma_picker` |  |  |  |  |
| Biliary intraepithelial neoplasia, an adenoma or another non-invasive lesion | go to `dg_not_malignant_pancreatobiliary` |  |  |  | Nagtegaal 2020, PDF p. 2 |
| Lymphoma, such as Burkitt lymphoma | refer to Group 2 |  | Lymphoma is recorded in Group 2, lymphomas and reticuloendothelial neoplasms. |  | Pfister 2022, PDF p. 6 |
| Sarcoma, such as rhabdomyosarcoma or clear cell sarcoma | refer to Group 9 |  | A sarcoma is recorded in Group 9, soft-tissue and other extraosseous sarcomas. |  | Nagtegaal 2020, PDF p. 3 |
| A deposit (metastasis) of a tumour that began elsewhere | refer, site asked again |  | A deposit is recorded at the site where the tumour began. The next screen asks that site. |  | ICD-O-3.1 manual, PDF p. 2 (printed p. 15) |

### `dg_not_malignant_gut` (morphology_only)

**Question:** Which lesion does the report name?

**Hint:** If the report states invasion, or calls the lesion malignant, go back and choose the invasive tumour.

| Answer | Records | Basis | Reason shown | Recognition aid | Source |
|---|---|---|---|---|---|
| Adenomatous polyp, or adenoma with low-grade dysplasia | exclusion 8210/0 |  | Not registered: Adenomatous polyp, NOS (8210/0) is benign. |  | ICCR Stomach 2025, PDF p. 14 (table image) |
| Tubular adenoma | exclusion 8211/0 |  | Not registered: Tubular adenoma, NOS (8211/0) is benign. |  | Nagtegaal 2020, PDF p. 3 |
| Sessile serrated lesion, serrated adenoma or serrated polyp | exclusion 8213/0 |  | Not registered: Serrated adenoma, NOS (8213/0) is benign. |  | Nagtegaal 2020, PDF p. 3 |
| Intestinal-type adenoma (stomach or small intestine) | exclusion 8144/0 |  | Not registered: Adenoma, intestinal type (8144/0) is benign. |  | ICCR Stomach 2025, PDF p. 14 (table image) |
| Familial adenomatous polyposis, or multiple adenomatous polyps, with no carcinoma | exclusion 8220/0 |  | Not registered: Adenomatous polyposis coli (8220/0) is benign. A carcinoma arising in it is chosen from the carcinoma list. |  | Nagtegaal 2020, PDF p. 6; Pfister 2022, PDF p. 19; Polat 2021, PMC section 3 |
| High-grade dysplasia, or carcinoma in situ, in a polyp | exclusion 8210/2 |  | Not registered: Adenocarcinoma in situ in adenomatous polyp (8210/2) is not invasive. |  | Nagtegaal 2020, PDF p. 2; Polat 2021, PMC section 2 |
| Glandular dysplasia or intraepithelial neoplasia, low grade | exclusion 8148/0 |  | Not registered: Glandular intraepithelial neoplasia, low grade (8148/0) is benign. |  | ICCR Oesophagus 2025, PDF p. 12 |
| Glandular dysplasia or intraepithelial neoplasia, high grade | exclusion 8148/2 |  | Not registered: Glandular intraepithelial neoplasia, high grade (8148/2) is not invasive. |  | ICCR Oesophagus 2025, PDF p. 12 |
| Squamous dysplasia or squamous intraepithelial neoplasia, low grade (oesophagus or anus) | exclusion 8077/0 |  | Not registered: Squamous intraepithelial neoplasia, low grade (8077/0) is benign. |  | ICCR Oesophagus 2025, PDF p. 12 |
| Squamous dysplasia or squamous intraepithelial neoplasia, high grade (oesophagus or anus) | exclusion 8077/2 |  | Not registered: Squamous intraepithelial neoplasia, high grade (8077/2) is not invasive. |  | Nagtegaal 2020, PDF p. 2 |
| Squamous cell papilloma | exclusion 8052/0 |  | Not registered: Squamous cell papilloma, NOS (8052/0) is benign. |  | ICCR Oesophagus 2025, PDF p. 12 |
| Squamous papillomatosis | exclusion 8060/0 |  | Not registered: Squamous papillomatosis (8060/0) is benign. |  | ICCR Oesophagus 2025, PDF p. 12 |
| Low-grade appendiceal mucinous neoplasm | exclusion 8480/1 |  | Not registered: Low grade appendiceal mucinous neoplasm (8480/1) is not malignant. |  |  |
| Another benign lesion | not registrable |  | A benign lesion is not registered. |  |  |

### `dg_not_malignant_pancreatobiliary` (morphology_only)

**Question:** Which lesion does the report name?

**Hint:** If the report states an associated invasive carcinoma, go back and choose the carcinoma answer.

| Answer | Records | Basis | Reason shown | Recognition aid | Source |
|---|---|---|---|---|---|
| Intraductal papillary mucinous neoplasm with low-grade dysplasia | exclusion 8453/0 |  | Not registered: Intraductal papillary mucinous adenoma (8453/0) is benign. |  | Nagtegaal 2020, PDF p. 6 |
| Intraductal papillary mucinous neoplasm with high-grade dysplasia | exclusion 8453/2 |  | Not registered: Intraductal papillary mucinous neoplasm with high grade dysplasia (8453/2) is not invasive. |  | Nagtegaal 2020, PDF p. 6 |
| Mucinous cystic neoplasm with low-grade dysplasia | exclusion 8470/0 |  | Not registered: Mucinous cystadenoma, NOS (8470/0) is benign. |  | Nagtegaal 2020, PDF p. 6 |
| Mucinous cystic neoplasm with high-grade dysplasia | exclusion 8470/2 |  | Not registered: Mucinous cystic neoplasm with high grade dysplasia (8470/2) is not invasive. |  | Nagtegaal 2020, PDF p. 6 |
| Pancreatic or biliary intraepithelial neoplasia, low grade | exclusion 8148/0 |  | Not registered: Glandular intraepithelial neoplasia, low grade (8148/0) is benign. |  | Nagtegaal 2020, PDF p. 2 |
| Pancreatic or biliary intraepithelial neoplasia, high grade | exclusion 8148/2 |  | Not registered: Glandular intraepithelial neoplasia, high grade (8148/2) is not invasive. |  | Nagtegaal 2020, PDF p. 2 |
| Another benign lesion | not registrable |  | A benign lesion is not registered. |  |  |

### `dg_carcinoma_picker` (morphology_only)

**Question:** Which tumour does the histology report name?

**Hint:** Type part of the report's term to filter the list. If the term is not found, search its words in a different order. When the report gives two terms for one tumour and no single answer covers both, choose the answer with the higher code; this includes a hormone type and a grade given together, such as gastrinoma, grade 2.

| Answer | Records | Basis | Reason shown | Recognition aid | Source |
|---|---|---|---|---|---|
| Adenocarcinoma, not otherwise specified | 8140/3 | 7 | Recorded as Adenocarcinoma, NOS (8140/3). |  |  |
| Mucinous adenocarcinoma, or colloid carcinoma | 8480/3 | 7 | Recorded as Mucinous adenocarcinoma (8480/3). | Extracellular mucin pools make up more than half of the tumour. | ICCR Stomach 2025, PDF p. 13 |
| Signet ring cell carcinoma, or poorly cohesive carcinoma | 8490/3 | 7 | Recorded as Signet ring cell carcinoma (8490/3). | Single cells or small clusters with no well-formed glands, with or without signet ring cells. | ICCR Stomach 2025, PDF p. 13 |
| Serrated adenocarcinoma | 8213/3 | 7 | Recorded as Serrated adenocarcinoma (8213/3). |  |  |
| Adenocarcinoma arising in familial adenomatous polyposis | 8220/3 | 7 | Recorded as Adenocarcinoma in adenomatous polyposis coli (8220/3). |  |  |
| Tubular adenocarcinoma | 8211/3 | 7 | Recorded as Tubular adenocarcinoma (8211/3). |  |  |
| Papillary adenocarcinoma | 8260/3 | 7 | Recorded as Papillary adenocarcinoma, NOS (8260/3). |  |  |
| Mixed adenocarcinoma, or adenocarcinoma with mixed subtypes | 8255/3 | 7 | Recorded as Adenocarcinoma with mixed subtypes (8255/3). |  |  |
| Micropapillary carcinoma | 8265/3 | 7 | Recorded as Micropapillary carcinoma, NOS (8265/3). |  |  |
| Hepatoid adenocarcinoma | 8576/3 | 7 | Recorded as Hepatoid adenocarcinoma (8576/3). | Large polygonal hepatocyte-like cells that express alpha fetoprotein. | ICCR Stomach 2025, PDF p. 13 |
| Parietal cell carcinoma | 8214/3 | 7 | Recorded as Parietal cell carcinoma (8214/3). |  |  |
| Mucoepidermoid carcinoma | 8430/3 | 7 | Recorded as Mucoepidermoid carcinoma (8430/3). |  |  |
| Goblet cell adenocarcinoma, or goblet cell carcinoid (appendix) | 8243/3 | 7 | Recorded as Goblet cell carcinoid (8243/3). | Formerly called goblet cell carcinoid or goblet cell carcinoma; it has a minor neuroendocrine component. | Nagtegaal 2020, PDF p. 4; Nagtegaal 2020, PDF p. 2 |
| Ductal adenocarcinoma, or infiltrating duct carcinoma, of the pancreas | 8500/3 | 7 | Recorded as Infiltrating duct carcinoma, NOS (8500/3). |  | ICD-O-3.1 manual, PDF p. 10 (printed p. 23) |
| Mucinous cystadenocarcinoma, or mucinous cystic neoplasm with an associated invasive carcinoma | 8470/3 | 7 | Recorded as Mucinous cystadenocarcinoma, NOS (8470/3). |  |  |
| Intraductal papillary mucinous neoplasm with an associated invasive carcinoma | 8453/3 | 7 | Recorded as Intraductal papillary mucinous neoplasm with an associated invasive carcinoma (8453/3). |  |  |
| Squamous cell carcinoma | 8070/3 | 7 | Recorded as Squamous cell carcinoma, NOS (8070/3). |  |  |
| Verrucous squamous cell carcinoma | 8051/3 | 7 | Recorded as Verrucous carcinoma, NOS (8051/3). |  |  |
| Spindle cell squamous cell carcinoma | 8074/3 | 7 | Recorded as Squamous cell carcinoma, spindle cell (8074/3). |  |  |
| Basaloid squamous cell carcinoma | 8083/3 | 7 | Recorded as Basaloid squamous cell carcinoma (8083/3). |  |  |
| Lymphoepithelioma-like carcinoma | 8082/3 | 7 | Recorded as Lymphoepithelial carcinoma (8082/3). |  |  |
| Adenoid cystic carcinoma | 8200/3 | 7 | Recorded as Adenoid cystic carcinoma (8200/3). |  |  |
| Adenosquamous carcinoma | 8560/3 | 7 | Recorded as Adenosquamous carcinoma (8560/3). | Adenocarcinoma mixed with squamous cell carcinoma; in the stomach the squamous part is at least 25%. | ICCR Stomach 2025, PDF p. 13 |
| Undifferentiated carcinoma, or anaplastic carcinoma | 8020/3 | 7 | Recorded as Carcinoma, undifferentiated, NOS (8020/3). |  |  |
| Large cell carcinoma with rhabdoid phenotype | 8014/3 | 7 | Recorded as Large cell carcinoma with rhabdoid phenotype (8014/3). |  |  |
| Pleomorphic carcinoma | 8022/3 | 7 | Recorded as Pleomorphic carcinoma (8022/3). |  |  |
| Sarcomatoid carcinoma | 8033/3 | 7 | Recorded as Pseudosarcomatous carcinoma (8033/3). |  |  |
| Carcinoma with osteoclast-like giant cells | 8035/3 | 7 | Recorded as Carcinoma with osteoclast-like giant cells (8035/3). |  |  |
| Neuroendocrine tumour, grade 1 | 8240/3 | 7 | Recorded as Neuroendocrine tumor, NOS (8240/3). | Ki-67 index below 3% and fewer than 2 mitoses per 2 mm². |  |
| Neuroendocrine tumour or carcinoid, grade not stated | 8240/3 | 7 | Recorded as Neuroendocrine tumor, NOS (8240/3). |  |  |
| Neuroendocrine tumour, grade 2, or atypical carcinoid | 8249/3 | 7 | Recorded as Neuroendocrine tumor, grade 2 (8249/3). | Ki-67 index from 3% to 20%, or 2 to 20 mitoses per 2 mm². |  |
| Neuroendocrine tumour, grade 3 (well differentiated) | 8249/3 | 7 | Recorded as Neuroendocrine tumor, grade 2 (8249/3). | Ki-67 index above 20%, or more than 20 mitoses per 2 mm², in a well-differentiated tumour. |  |
| Enterochromaffin cell (serotonin-producing) neuroendocrine tumour | 8241/3 | 7 | Recorded as Enterochromaffin cell carcinoid (8241/3). |  |  |
| Enterochromaffin-like (ECL) cell neuroendocrine tumour | 8242/3 | 7 | Recorded as Enterochromaffin-like cell tumor (8242/3). |  |  |
| Gastrinoma | 8153/3 | 7 | Recorded as Gastrinoma (8153/3). |  |  |
| Somatostatinoma | 8156/3 | 7 | Recorded as Somatostatinoma (8156/3). |  |  |
| Non-functioning pancreatic neuroendocrine tumour, or islet cell tumour | 8150/3 | 7 | Recorded as Pancreatic neuroendocrine tumor, nonfunctioning (8150/3). |  |  |
| Insulinoma | 8151/3 | 7 | Recorded as Insulinoma, NOS (8151/3). |  |  |
| Glucagonoma | 8152/3 | 7 | Recorded as Glucagonoma (8152/3). |  |  |
| VIPoma | 8155/3 | 7 | Recorded as Vipoma (8155/3). |  |  |
| ACTH-producing neuroendocrine tumour | 8158/3 | 7 | Recorded as ACTH-producing tumor (8158/3). |  |  |
| Neuroendocrine carcinoma, not otherwise specified | 8246/3 | 7 | Recorded as Neuroendocrine carcinoma, NOS (8246/3). | A poorly differentiated, high-grade carcinoma that stains for synaptophysin and chromogranin A; the report gives it no grade. | Nagtegaal 2020, PDF p. 5; ICCR Stomach 2025, PDF p. 21; ICCR Oesophagus 2025, PDF p. 19 |
| Large cell neuroendocrine carcinoma | 8013/3 | 7 | Recorded as Large cell neuroendocrine carcinoma (8013/3). |  |  |
| Small cell neuroendocrine carcinoma, or small cell carcinoma | 8041/3 | 7 | Recorded as Small cell carcinoma, NOS (8041/3). |  |  |
| Mixed neuroendocrine–non-neuroendocrine neoplasm (MiNEN), including mixed acinar–neuroendocrine carcinoma | 8154/3 | 7 | Recorded as Mixed neuroendocrine non-neuroendocrine neoplasm (MiNEN) (8154/3). | A neuroendocrine and a non-neuroendocrine component, each at least 30% of the tumour. | ICCR Stomach 2025, PDF p. 14 |
| Mixed adenoneuroendocrine carcinoma (MANEC), or mixed neuroendocrine carcinoma | 8244/3 | 7 | Recorded as Mixed adenoneuroendocrine carcinoma (8244/3). |  |  |
| Combined small cell carcinoma, with adenocarcinoma or squamous cell carcinoma | 8045/3 | 7 | Recorded as Combined small cell carcinoma (8045/3). |  |  |

The picker lists the codes this part's files name. The other valid /3 codes that ICCC-2017 places in XIf2, XIf3 and XIf10 (`g11_inventory.json`, 174 codes each) can be added to it from the inventory; none of them has a paediatric report in this part.

## 4 Immunohistochemistry rules

| Panel | Positive | Negative | Records | Source |
|---|---|---|---|---|
| `dg_pancreas_ihc` | beta-catenin (nuclear) | chromogranin, trypsin | 8452/3 | Stanley 2015, PDF p. 2; Stanley 2015, PDF p. 3 |

The pancreas checklist has one rule. Stanley 2015 reports nuclear beta-catenin staining with chromogranin and trypsin negative, "thus confirming a solid pseudopapillary tumor" (PDF p. 2), and lists vimentin, CD56 and CD10 as positive (PDF p. 3). The same page reads "anti-trypsin" positive; that is a different antigen from the trypsin the tumour lacks, so it is not used as a marker. Its fallback answers record 8000/3 when the report states malignancy, and nothing otherwise. No file in this part gives markers that separate acinar cell carcinoma, pancreatoblastoma or a pancreatic neuroendocrine tumour (data gap 3).

Neuroendocrine differentiation: both ICCR guides require synaptophysin and chromogranin A as a minimum to confirm a neuroendocrine carcinoma or the neuroendocrine part of a MiNEN (ICCR Stomach 2025, PDF p. 21; ICCR Oesophagus 2025, PDF p. 19). The markers confirm differentiation; the grade and the differentiation come from the histology report. This is carried as the recognition aid on the neuroendocrine carcinoma picker answer, not as a checklist rule, because the markers do not separate a neuroendocrine tumour from a neuroendocrine carcinoma. A MiNEN needs each component to be at least 30% of the tumour (ICCR Stomach 2025, PDF p. 14).

## 5 Registration without tissue

| Evidence on file | Records | Basis |
|---|---|---|
| A referral letter or clinical note that states a malignant digestive tumour, no imaging, no tissue | 8000/3 | 1 |
| An imaging report that states a malignant digestive tumour, no tissue | 8000/3 | 2 |
| Imaging that shows the tumour, with a raised chromogranin A | 8240/3 | 4 |
| Imaging that shows the tumour, with a raised insulin | 8151/3 | 4 |
| Imaging that shows the tumour, with a raised glucagon | 8152/3 | 4 |
| Imaging that shows the tumour, with a raised gastrin | 8153/3 | 4 |
| Imaging that shows the tumour, with a raised vasoactive intestinal peptide | 8155/3 | 4 |
| Imaging that shows the tumour, with a raised somatostatin | 8156/3 | 4 |
| Imaging that shows the tumour, with a raised serotonin | 8241/3 | 4 |
| Imaging that shows the tumour, with a raised adrenocorticotropic hormone | 8158/3 | 4 |

The basis-4 answers come from the registrar's rule on Visser 2023 Table 4, which is outside this part's files. Stanley 2015 supports the imaging answer only as far as stating that sonography alone cannot give a definitive diagnosis of a pancreatic neoplasm (PDF p. 4) and that its case was suspected on imaging and confirmed by pathology (PDF p. 1). A suspected tumour is not registrable. No file in this part reports a functioning digestive neuroendocrine tumour in a child (registrar question 7).

## 6 Laboratory tests

| Test | Specimen | Role | Source |
|---|---|---|---|
| Chromogranin A | serum | With imaging that shows the tumour, records Neuroendocrine tumor, NOS (8240/3), basis 4. Source: the registrar's rule from Visser 2023 Table 4; no file in this part names a serum test. | registrar rule (Visser 2023 Table 4) |
| Insulin, glucagon, gastrin, vasoactive intestinal peptide, somatostatin, serotonin, adrenocorticotropic hormone | serum | With imaging that shows the tumour, records the matching functioning tumour (8151/3, 8152/3, 8153/3, 8155/3, 8156/3, 8241/3, 8158/3), basis 4. Source: the registrar's rule from Visser 2023 Table 4. | registrar rule (Visser 2023 Table 4) |
| Pancreatic laboratory values | serum | No diagnostic role: they are typically normal in solid pseudopapillary neoplasm, so a normal result does not exclude it and is not offered. | Stanley 2015, PDF p. 3 |

No file in this part gives a serum or urine test a diagnostic role. Stanley 2015 states that pancreatic laboratory values are typically normal in solid pseudopapillary neoplasm (PDF p. 3). ICCR Stomach 2025 describes alpha fetoprotein expression in hepatoid adenocarcinoma as a tissue finding (PDF p. 13), not a serum test.

## 7 Rules A to K

| Rule | Applies | How it reaches the clerk |
|---|---|---|
| A | yes | Option on dg_site: 'Tissue beside an organ ... or a region such as the abdomen' sends the clerk back to the site screen, because a region names no digestive tissue. No digestive tumour type implies a tissue the way squamous cell carcinoma implies skin. |
| B | yes | Hint and option on dg_site: tissue beside an organ, such as peripancreatic tissue, does not name the organ; the option's reason states that ICD-O lists peripancreatic and retrocaecal tissue under retroperitoneum (C48.0). |
| C | yes | Hint and options on dg_site: overlapping lesions take .8 (colon C18.8; rectum, anus and anal canal C21.8; biliary tract C24.8; digestive system C26.8); a carcinoma of oesophagus and stomach is indexed to cardia C16.0. Each reason names the code. |
| D | yes | Referral only: the lymphoma options refer to Group 2, which applies Rule D to the topography. |
| E | no | No leukaemia reaches these screens; the cytology and histology lymphoma options refer to Group 2. |
| F | yes | Hints on dg_not_malignant_gut and dg_not_malignant_pancreatobiliary, and the reason on the low-grade appendiceal mucinous neoplasm option: if the report states invasion or calls the lesion malignant, the clerk goes back to the invasive answer. Registrar question 6 asks whether a report calling a pancreatic solid pseudopapillary neoplasm benign changes its behaviour. |
| G | yes | Hint on dg_net_grade: if the report gives two grades, or the Ki-67 index and mitotic count point to different grades, choose the higher (Nagtegaal 2020 Table 2 footnote states the same rule). The sixth digit is not built. |
| H | yes | Hint on dg_biliary_histology: bile duct carcinoma names a type, not a site. Picker label for infiltrating duct carcinoma names the pancreas, so the clerk keeps C25 rather than the breast topography ICD-O attaches. Solid pseudopapillary neoplasm records 8452/3 only at the pancreas; the metastasis option on every histology screen sends a deposit to its primary site. |
| J | yes | Hint on dg_carcinoma_picker: if the term is not found, search its words in a different order. |
| K | yes | Hint on every histology screen and on dg_carcinoma_picker: when two terms describe one tumour and no answer covers both, choose the higher code. The picker hint names the hormone-plus-grade case (gastrinoma, grade 2), which registrar question 8 asks Jay to confirm. |

Sources for the rules: Rule A, ICD-O-3.1 manual PDF p. 1 (printed p. 14); Rules B and C with Table 17's overlapping digestive codes, PDF pp. 4-5 (printed pp. 17-18), including "carcinoma of the stomach and small intestine" to C26.8 and "carcinoma of esophagus and stomach" to C16.0; Rules F and G, PDF p. 2 (printed p. 15); Rule H and Table 23, PDF pp. 10-11 (printed pp. 23-24), including infiltrating duct carcinoma of the pancreas coded C25.9 and "bile duct carcinoma" (8160/3) not coded automatically to C24.0; Rules J and K, PDF p. 3 (printed p. 16). Nagtegaal 2020 Table 2 (PDF p. 4) states the same higher-grade rule as Rule G for neuroendocrine tumours.

## 8 Code currency

Findings from `Group 11 — ICD-O-3.2 Code Currency Check 2026-10-08.md` and from this part's sources. REDCap strings are noted only where they differ from the ICD-O-3.2 preferred term, for the REDCap-side list in `docs/TODO.md`; the tool does not test REDCap (standing rule 16).

| Code | Finding | What the tree does |
|---|---|---|
| 8245/3 | Every ICD-O-3.2 term at 8245/3 (Adenocarcinoid tumor) is [obs]. Currency check §2: 8243/3 Goblet cell carcinoid is current; the WHO source decides. | Not built. Nagtegaal 2020 names goblet cell adenocarcinoma, formerly goblet cell carcinoid/carcinoma, and does not name adenocarcinoid; no successor is assigned. Registrar question 4. REDCap offers 8245 under XIf: REDCap-side list. |
| 8124/3 | Every ICD-O-3.2 term at 8124/3 (Cloacogenic carcinoma, C21.2) is [obs]. Currency check §2: 8083/3 and 8070/3 exist with no cross-reference. | Not built. The WHO source in this part names no cloacogenic entity. REDCap offers 8124: REDCap-side list. |
| 8512/3 | ICCR Stomach Table 3 (PDF p. 15) prints 8512/3 Medullary carcinoma with lymphoid stroma; its only ICD-O-3.2 term is [obs]. Currency check §2: 8510/3 Medullary carcinoma, NOS is current; the WHO source decides. | Not built. The WHO table keeps the [obs] code, so it does not settle the successor. Registrar question 3. REDCap offers 8512: REDCap-side list. |
| 8976/3 | ICCR Stomach Table 3 prints Gastroblastoma 8976/3* (approved by IARC in April 2019). ICD-O-3.2 and ICCC-2017 hold no 8976. Currency check §7 covers the asterisk. | Registrar decides; not on any screen until then. Registrar question 2. |
| 8213/2 | ICCR Stomach prints Serrated dysplasia, high grade 8213/2*; ICD-O-3.2 holds 8213 at /0 and /3 only. | Not built. High-grade dysplasia in the stomach is excluded under 8148/2 Glandular intraepithelial neoplasia, high grade. Registrar question 9. |
| 8144/2 | ICCR Stomach prints Intestinal-type adenoma, high grade 8144/2*; ICD-O-3.2 holds 8144 at /0 and /3 only. | Not built; excluded as in situ. Registrar question 9. |
| 8077/2 | ICCR Oesophagus Table 1 (PDF p. 12) labels 8077/2 'Oesophageal squamous intraepithelial neoplasia (dysplasia), low grade', a printing error; ICD-O-3.2 8077/2 is Squamous intraepithelial neoplasia, high grade. | The exclusion option says high grade and records 8077/2. |
| 8243/3 | ICD-O-3.2 holds no term 'Goblet cell adenocarcinoma'; its Preferred term at 8243/3 is Goblet cell carcinoid, the name the WHO 5th edition retired. | Picker label names both; the reason records Goblet cell carcinoid (8243/3). REDCap label matches the ICD-O-3.2 Preferred term. |
| 8240/3 | REDCap label 'Carcinoid tumor, NOS' is a synonym; Preferred is Neuroendocrine tumor, NOS. Neuroendocrine tumor, grade 1 is a Related term here. ICD-O-3.2 moved 8240/1 Carcinoid tumor, argentaffin to 8241/3. | Reasons carry Neuroendocrine tumor, NOS. REDCap relabel: REDCap-side list. |
| 8249/3 | REDCap label 'Atypical carcinoid tumor' is a synonym; Preferred is Neuroendocrine tumor, grade 2. Neuroendocrine tumor, grade 3 is a Related term at 8249/3. | Grade 2 and grade 3 both record 8249/3. REDCap relabel: REDCap-side list. |
| 8150/3 | Behaviour /1 to /3 in ICD-O-3.2. REDCap label 'Pancreatic endocrine tumor, malignant' is not an ICD-O-3.2 term; Preferred is Pancreatic neuroendocrine tumor, nonfunctioning. Islet cell tumor, NOS and Islet cell carcinoma are [obs] related terms at 8150/3. | Picker label offers 'islet cell tumour' so an older report finds the current code. REDCap relabel: REDCap-side list. |
| 8151/3 | Insulinoma moved /0 to /3. REDCap label 'Insulinoma, malignant' is not an ICD-O-3.2 term; Preferred is Insulinoma, NOS. | Built as picker and as a basis-4 marker answer. REDCap relabel: REDCap-side list. |
| 8152/3 | Behaviour /1 to /3. REDCap label 'Glucagonoma, malignant'; Preferred is Glucagonoma. | REDCap relabel: REDCap-side list. |
| 8153/3 | Behaviour /1 to /3. REDCap label 'Gastrinoma, malignant'; Preferred is Gastrinoma. | REDCap relabel: REDCap-side list. |
| 8155/3 | Behaviour /1 to /3. REDCap label 'Vipoma, malignant'; Preferred is Vipoma. | REDCap relabel: REDCap-side list. |
| 8156/3 | Behaviour /1 to /3. REDCap label 'Somatostatinoma, malignant'; Preferred is Somatostatinoma. | REDCap relabel: REDCap-side list. |
| 8158/3 | REDCap label 'Endocrine tumor, functioning, NOS' is an [obs] related term; Preferred is ACTH-producing tumor. | Reason carries ACTH-producing tumor. REDCap relabel: REDCap-side list. |
| 8154/3 | REDCap label 'Mixed pancreatic endocrine and exocrine tumor, malignant' is a related term; Preferred is Mixed neuroendocrine non-neuroendocrine neoplasm (MiNEN). | REDCap relabel: REDCap-side list. |
| 8242/3 | Behaviour /1 to /3. REDCap label 'Enterochromaffin-like cell tumor, malignant'; Preferred is Enterochromaffin-like cell tumor. | REDCap relabel: REDCap-side list. |
| 8452/3 | Site-specific in ICD-O-3.2: 8452/3 Solid pseudopapillary neoplasm of pancreas; 8452/1 Solid pseudopapillary tumor of ovary. REDCap label 'Solid pseudopapillary carcinoma' is a related term. | Pancreas screen records 8452/3. REDCap relabel: REDCap-side list. |
| 8453/3 | REDCap label 'Intraductal papillary-mucinous carcinoma, invasive' is not an ICD-O-3.2 term; Preferred is Intraductal papillary mucinous neoplasm with an associated invasive carcinoma. | REDCap relabel: REDCap-side list. |
| 8033/3 | REDCap label 'Sarcomatoid carcinoma' is a synonym; Preferred is Pseudosarcomatous carcinoma. | REDCap relabel: REDCap-side list. |
| 8162/3 | REDCap XIf offers 8162 'Klatskin tumor', an [obs] synonym; Preferred is Perihilar cholangiocarcinoma. ICCC-2017 places 8160 to 8162 in VIIb at every site. | Refers to Group 7. REDCap-side list: 8160, 8161 and 8162 sit in the Group 11 option list though ICCC groups them in VII. |
| 8045/3 | Combined small cell carcinoma is current in ICD-O-3.2 and in the ICCC Group XI range; REDCap Group 11 does not offer 8045. | Built in the picker. REDCap-side list: add 8045. |
| 8010/3 | REDCap XIf label 'Epithelial Tumor, NOS' differs from the Preferred term Carcinoma, NOS. | Cytology answer records Carcinoma, NOS (8010/3). REDCap relabel: REDCap-side list. |
| 8480/1 | Low grade appendiceal mucinous neoplasm is /1 in ICD-O-3.2. | Exclusion. |

## 9 Conflicts with other groups

| Group | Codes | Sites | Issue |
|---|---|---|---|
| 7 | 8160, 8161, 8162 | C23.9, C24.0, C24.1, C24.8, C24.9 | ICCC-2017 places cholangiocarcinoma, bile duct cystadenocarcinoma and perihilar cholangiocarcinoma in VIIb at every site, so a bile duct carcinoma of the gallbladder or extrahepatic bile ducts goes to Group 7, though those sites are XIf10 for other carcinomas and REDCap lists the codes in Group 11. |
| 7 | 8010-8041, 8140, 8240, 8480-8490, 8550 | C22.0, C22.1 | Liver is a Group 7 site: ICCC-2017 places these carcinoma codes in VIIb at C22.0 and C22.1. The site screen refers liver tumours to Group 7. |
| 12 | 8971 | C25.0 to C25.9 (8 sites) | Pancreatoblastoma is ICCC XIIa2 at every site; the pancreas screen refers it to Group 12. |
| 12 | 8936 | C16.0 to C15.9 (38 sites) | Gastrointestinal stromal tumour is ICCC XIIa1; the stomach, small intestine, oesophagus and colorectal screens refer it to Group 12. |
| 12 | 8000 | C18.0 to C26.9 (55 sites) | Tissue-free registration (basis 1 or 2) records 8000/3, which ICCC-2017 places in XIIb at every digestive site. The ICCC subgroup computed at output is XIIb, not XI. |
| 12 | 8976 | C16.0 to C16.9 (9 sites) | Gastroblastoma is a biphasic epithelial and spindle-cell tumour with no code in ICD-O-3.2 or ICCC-2017; whether it belongs in Group 11 or Group 12 is the registrar's ruling. |
| 10 | 8452 | C56.9 to C25.9 (9 sites) | 8452 is /3 at the pancreas (Group 11) and /1 at the ovary (out of scope, a Group 10 site). The behaviour follows the site. |
| 10 | 8576, 9071 | C16.0 to C16.9 (9 sites) | Hepatoid adenocarcinoma and yolk sac tumour-like carcinoma of the stomach express alpha fetoprotein; a hepatoid yolk sac tumour (9071/3) is ICCC Xb4. The histology report's tumour name decides. |
| 2 | 9590-9989, 9758 | C18.0 to C26.9 (55 sites) | Lymphomas (Burkitt lymphoma 9687/3 is ICCC IIc) and EBV-positive inflammatory follicular dendritic cell sarcoma (9758/3, ICCC IId) of the digestive tract refer to Group 2. |
| 9 | 9044, 8900-8920 | C18.0 to C26.9 (55 sites) | Gastrointestinal clear cell sarcoma (9044/3, ICCC IXd7) and rhabdomyosarcoma (8900 to 8920, ICCC IXa), including that of the biliary tree, refer to Group 9. |

Each referral was verified in ICCC-2017 for the code at the site: 8971/3 XIIa2, 8936/3 XIIa1, 8160/3 and 8162/3 VIIb, 9687/3 IIc, 9758/3 IId, 9044/3 IXd7, 8900/3 and 8910/3 IXa, each at C15.9, C16.9, C17.0, C18.0, C18.1, C21.1, C23.9, C24.0 and C25.0. The Group 10 lessons applied here: a code is resolved by its site (8452/3 pancreas against 8452/1 ovary; the ICCC subgroup computed at output); a referral is tested against ICCC-2017 at the site, not assumed from the tumour's name (cholangiocarcinoma of the gallbladder is VIIb, not XIf10); and an AFP-expressing gastric carcinoma is kept apart from a yolk sac tumour by the report's tumour name.

## 10 Data gaps

1. **A source reporting small-bowel, gastric, oesophageal, anal and biliary carcinoma in patients aged 0 to 18, and medullary carcinoma of the colon in a child.** Polat 2021 and Mahajan 2022 report colorectal carcinoma in patients aged 8 to 16 (mucinous, signet ring cell, adenocarcinoma NOS, one tubular component), and those types are now colorectal options. No paper in this part reports carcinoma of the other digestive sites in a child, so those stay in the picker. Mahajan 2022 describes a medullary growth pattern in Lynch syndrome tumours without reporting one in a child, so medullary carcinoma (8510/3 Medullary carcinoma, NOS) is not added. Constitutional mismatch repair deficiency is not named in the new papers. Candidate: The EXPeRT/PARTNER diagnostic and therapeutic recommendations for colorectal carcinoma in children and adolescents (Pediatric Blood & Cancer 2021, supplement; controller to verify the citation).
2. **The WHO 5th-edition entity list, with ICD-O codes, for the colon and rectum, the appendix, the anal canal, the small intestine and ampulla, the gallbladder and extrahepatic bile ducts, and the exocrine pancreas.** Nagtegaal 2020 is a commentary and prints no entity table. Without it the picker cannot name medullary carcinoma (8510/3 Medullary carcinoma, NOS), adenoma-like adenocarcinoma, high-grade appendiceal mucinous neoplasm, ampullary intestinal and pancreatobiliary types (8144/3, 8163/3), or the pancreatic carcinoma subtypes, and the colorectal exclusion screen cannot be checked against WHO terms. Candidate: The ICCR histopathology reporting guides for colorectal cancer, carcinoma of the exocrine pancreas, ampulla of Vater, gallbladder and bile ducts (each prints the WHO 5th-edition table with ICD-O codes).
3. **Diagnostic criteria and immunohistochemistry for pancreatic acinar cell carcinoma and pancreatoblastoma in children, and for paediatric pancreatic neuroendocrine tumours.** Pfister 2022 names acinar cell carcinoma and pancreatoblastoma but gives no criteria, and no paper added on 8 October 2026 reports acinar cell carcinoma in a child. Karges 2025 reports the occurrence, grade and function of paediatric pancreatic neuroendocrine tumours but gives no immunohistochemistry criteria. The pancreas checklist keeps one rule (solid pseudopapillary neoplasm) and no recognition aid for acinar cell carcinoma. Candidate: The EXPeRT/PARTNER recommendations for pancreatic tumours in children and adolescents (Pediatric Blood & Cancer 2021, supplement; controller to verify).
4. **Whether goblet cell adenocarcinoma, appendiceal mucinous neoplasms and grade 3 appendiceal neuroendocrine tumours occur before age 19.** Roganovic 2026 settles the frequency and grading of paediatric appendiceal neuroendocrine tumours: the most frequent gastrointestinal epithelial tumour of children, mostly grade 1, grade 2 rare. It reports no grade 3 tumour in a child; the grade 3 option rests on Pfister 2022's listing of appendiceal neuroendocrine tumours, and the controller decides whether it stays. Goblet cell adenocarcinoma, low-grade appendiceal mucinous neoplasm and mucinous adenocarcinoma of the appendix have no paediatric report. Candidate: A paediatric appendiceal neuroendocrine tumour series or the EXPeRT/PARTNER neuroendocrine neoplasm recommendations (controller to verify).
5. **A serum or urine test that the digestive sources give a diagnostic role.** No file in this part names one. The marker screen rests only on the registrar's Visser 2023 Table 4 rule. The papers added on 8 October 2026 give no marker a diagnostic role: Roganovic 2026 states that raised urinary 5-HIAA, chromogranin A or neuron-specific enolase has not been described in children with appendiceal neuroendocrine tumours, Mahajan 2022 that the role of carcinoembryonic antigen in paediatric colorectal carcinoma is not established, and Karges 2025 defines a functioning tumour by a clinical syndrome with hormone abnormalities, not by immunohistochemistry alone.
6. **The ICD-O code of malignant gastrointestinal neuroectodermal tumour.** Nagtegaal 2020 names it with gastrointestinal clear cell sarcoma; ICD-O-3.2 has no term for it, so its referral group is unverified. The sarcoma option covers it until the registrar rules. Candidate: WHO Digestive System Tumours, 5th ed., 2019, mesenchymal tumours chapter.
7. **A ruling on whether the colorectal options apply at the anus and anal canal (C21.0 to C21.8).** dg_colorectal_histology serves the colon, rectosigmoid junction, rectum and anus. The five new colorectal options rest on colon, rectosigmoid and rectal carcinomas in children (Polat 2021, Mahajan 2022); no paper reports anal carcinoma in a child. Their entities list C18.0, C18.2 to C18.9, C19.9 and C20.9, while the screen still shows them for an anal tumour; the anal sites stay on the picker entities.
8. **A paediatric report of colorectal tubular adenocarcinoma as the only histological type.** The tubular adenocarcinoma option rests on one tumour with mucinous and tubular adenocarcinoma components in a 16-year-old (Polat 2021 Table 1, PMC section 2), which records 8480/3 under the higher-code rule. The controller decides whether the option stays on the colorectal screen or returns to the picker.
9. **An immunohistochemistry rule for a solid pseudopapillary neoplasm without nuclear beta-catenin.** Ebrahim 2025 reports a boy whose solid pseudopapillary neoplasm lacked nuclear beta-catenin, and higher CD99 and LEF1 expression in the four paediatric cases (PMC section 13). The single dg_pancreas_ihc rule requires nuclear beta-catenin, so such a tumour reaches 8000/3 when the report names no type, and the recognition aid on the solid pseudopapillary neoplasm option names nuclear beta-catenin. The controller decides whether to add a CD99 and LEF1 rule.

### Questions for the registrar

1. Colorectal carcinoma: no file in this part reports colorectal, gastric, small-bowel, oesophageal or biliary carcinoma in patients aged 0 to 18. Under ruling 1 they stay in the picker and the colorectal screen has no carcinoma answer of its own. Keep that until the controller's paediatric source arrives, or build adenocarcinoma, mucinous, signet ring cell and medullary carcinoma as colorectal options now? *Overtaken 8 October 2026:* the registrar's ruling and Polat 2021 and Mahajan 2022 put mucinous adenocarcinoma, signet ring cell carcinoma, adenocarcinoma NOS, adenocarcinoma in familial adenomatous polyposis and tubular adenocarcinoma on the colorectal screen; medullary carcinoma has no paediatric report and is not added (section 11).
2. Gastroblastoma: ICCR Stomach 2025 prints 8976/3* (PDF p. 15); ICD-O-3.2 and ICCC-2017 hold no 8976. Pfister 2022 lists it as a paediatric tumour (PDF pp. 11, 13). How is it recorded, and in Group 11 or Group 12? No screen offers it until the ruling.
3. Gastric carcinoma with lymphoid stroma: ICCR Stomach 2025 prints 8512/3 Medullary carcinoma with lymphoid stroma (PDF p. 15); every ICD-O-3.2 term at 8512/3 is [obs]. 8510/3 Medullary carcinoma, NOS and 8082/3 Lymphoepithelial carcinoma are both current. Which does the clerk record, or is it left unbuilt?
4. Adenocarcinoid tumour 8245/3 is [obs]. Nagtegaal 2020 names goblet cell adenocarcinoma, formerly goblet cell carcinoid/carcinoma (PDF p. 4), and does not name adenocarcinoid. May a report of appendiceal adenocarcinoid be recorded as 8243/3 Goblet cell carcinoid?
5. Cholangiocarcinoma of the gallbladder and extrahepatic bile ducts: ICCC-2017 places 8160 to 8162 in VIIb at every site, so the tree refers them to Group 7, while REDCap offers 8160, 8161 and 8162 in Group 11. Confirm the referral.
6. Solid pseudopapillary neoplasm: Stanley 2015 says most are benign (PDF p. 3). ICD-O-3.2 codes the pancreatic tumour 8452/3 and holds no 8452/0. When a report calls it benign or of low malignant potential, is it still 8452/3, or does Rule F record a stated behaviour?
7. Tissue-free hormone and chromogranin A answers: no file in this part reports a functioning digestive neuroendocrine tumour in a child. Offer all eight Visser Table 4 answers on the digestive marker screen? *Note, 8 October 2026:* Karges 2025 now reports insulinoma and gastrinoma in children and defines a functioning tumour by a clinical syndrome with hormone abnormalities (PMC sections 3 and 7).
8. Rule K with a functioning neuroendocrine tumour and a grade (for example gastrinoma, grade 2: 8153 against 8249): does the clerk record the numerically higher code 8249/3, as the picker hint now says, or the hormone code? *Note, 8 October 2026:* the pancreas screen now offers hormone types, non-functioning tumour and grades side by side, and its hint gives the same higher-code instruction, so this ruling now governs that screen too.
9. Gastric high-grade dysplasia: ICCR Stomach 2025 prints 8213/2* and 8144/2* (PDF p. 14), which ICD-O-3.2 lacks. Confirm the exclusion screen records 8148/2 Glandular intraepithelial neoplasia, high grade.

## 11. Paediatric evidence added 8 October 2026

The registrar ruled on 8 October 2026 that an entity a source reports at ages 0 to 18 is an option on its site's histology screen, and a valid current /3 code at the site with no paediatric report is a picker entry. The five papers in section 1 were read through the snippet tool only. Every option code below was rechecked in `icdo32.sqlite` (each has a current /3 preferred term) and in ICCC-2017 (XIf2 at the colorectal sites, XIf3 at the appendix, XIf10 at the pancreas). Where a picker entity covered several digestive sites, only the sites a paper reports moved to a new option entity; the parent keeps the other sites as a picker entry, so the shared picker still serves the stomach, small intestine, oesophagus, biliary tract and anus.

### Entities

| Entity | Before | After | Cite |
|---|---|---|---|
| Neuroendocrine tumour, grade 1 (appendix) (8240/3) | option, paediatric occurs | option, paediatric common | Roganovic 2026, PMC section 1; Roganovic 2026, PMC section 4 |
| Neuroendocrine tumour, grade 2 (appendix) (8249/3) | option, paediatric occurs | option, paediatric occurs | Roganovic 2026, PMC section 4 |
| Neuroendocrine tumour, grade not stated (appendix); carcinoid (8240/3) | option, paediatric occurs | option, paediatric common | Roganovic 2026, PMC section 1 |
| Neuroendocrine tumour, grade 1 or grade not stated (pancreas) (8240/3) | inside 'Neuroendocrine tumour, grade 1 or grade not stated (sites other than the appendix)': picker, paediatric not_reported | own entity at C25.0 to C25.9: option, paediatric occurs; parent keeps the other sites as picker | Karges 2025, PMC section 1; Karges 2025, PMC section 8; Karges 2025, PMC section 9 |
| Neuroendocrine tumour, grade 2 or grade 3 (pancreas) (8249/3) | inside 'Neuroendocrine tumour, grade 2 or grade 3 (sites other than the appendix)': picker, paediatric not_reported | own entity at C25.0 to C25.9: option, paediatric occurs; parent keeps the other sites as picker | Karges 2025, PMC section 9; Karges 2025, PMC section 8 |
| Gastrinoma (pancreas) (8153/3) | inside 'Gastrinoma NOS': picker, paediatric not_reported | own entity at C25.0 to C25.9: option, paediatric occurs; parent keeps the other sites as picker | Karges 2025, PMC section 7; Karges 2025, PMC section 2 |
| Somatostatinoma (pancreas) (8156/3) | inside 'Somatostatinoma NOS': picker, paediatric not_reported | own entity at C25.0 to C25.9: option, paediatric occurs; parent keeps the other sites as picker | Karges 2025, PMC section 2 |
| Non-functioning pancreatic neuroendocrine tumour (8150/3) | picker, paediatric not_reported | option, paediatric common | Karges 2025, PMC section 1; Karges 2025, PMC section 11 |
| Insulinoma (8151/3) | picker, paediatric not_reported | option, paediatric common | Karges 2025, PMC section 2; Karges 2025, PMC section 11; Karges 2025, PMC section 7 |
| Glucagonoma (8152/3) | picker, paediatric not_reported | option, paediatric occurs | Karges 2025, PMC section 2 |
| VIPoma (8155/3) | picker, paediatric not_reported | option, paediatric occurs | Karges 2025, PMC section 2 |
| Neuroendocrine carcinoma NOS (pancreas) (8246/3) | inside 'Neuroendocrine carcinoma NOS': picker, paediatric not_reported | own entity at C25.0 to C25.9: option, paediatric occurs; parent keeps the other sites as picker | Karges 2025, PMC section 9 |
| Neuroendocrine tumour, grade 1 or grade not stated (sites other than the appendix and pancreas) (8240/3) | named 'Neuroendocrine tumour, grade 1 or grade not stated (sites other than the appendix)' | renamed to exclude the pancreas, which is now its own entity; still picker, paediatric not_reported |  |
| Neuroendocrine tumour, grade 2 or grade 3 (sites other than the appendix and pancreas) (8249/3) | named 'Neuroendocrine tumour, grade 2 or grade 3 (sites other than the appendix)' | renamed to exclude the pancreas, which is now its own entity; still picker, paediatric not_reported |  |
| Mucinous adenocarcinoma (colon, rectosigmoid junction and rectum) (8480/3) | inside 'Mucinous adenocarcinoma': picker, paediatric not_reported | own entity at C18.0, C18.2 to C18.9, C19.9 and C20.9: option, paediatric common; parent keeps the other sites as picker | Polat 2021, PMC section 2; Mahajan 2022, PMC section 1; Mahajan 2022, PMC section 5; Mahajan 2022, PMC section 4 |
| Signet ring cell carcinoma (colon, rectosigmoid junction and rectum) (8490/3) | inside 'Signet-ring cell carcinoma; poorly cohesive carcinoma': picker, paediatric not_reported | own entity at C18.0, C18.2 to C18.9, C19.9 and C20.9: option, paediatric common; parent keeps the other sites as picker | Mahajan 2022, PMC section 1; Mahajan 2022, PMC section 5 |
| Adenocarcinoma NOS (colon, rectosigmoid junction and rectum) (8140/3) | inside 'Adenocarcinoma NOS': picker, paediatric not_reported | own entity at C18.0, C18.2 to C18.9, C19.9 and C20.9: option, paediatric occurs; parent keeps the other sites as picker | Polat 2021, PMC section 2; Mahajan 2022, PMC section 4 |
| Adenocarcinoma in familial adenomatous polyposis (colon, rectosigmoid junction and rectum) (8220/3) | inside 'Adenocarcinoma in adenomatous polyposis coli': picker, paediatric not_reported | own entity at C18.0, C18.2 to C18.9, C19.9 and C20.9: option, paediatric occurs; parent keeps the other sites as picker | Mahajan 2022, PMC section 5; Polat 2021, PMC section 3 |
| Tubular adenocarcinoma (colon, rectosigmoid junction and rectum) (8211/3) | inside 'Tubular adenocarcinoma': picker, paediatric not_reported | own entity at C18.0, C18.2 to C18.9, C19.9 and C20.9: option, paediatric occurs; parent keeps the other sites as picker | Polat 2021, PMC section 2 |
| Adenomatous polyp, high-grade dysplasia (8210/2) | exclusion, paediatric not_reported | exclusion, paediatric occurs | Polat 2021, PMC section 2 |
| Familial adenomatous polyposis with no carcinoma (8220/0) | exclusion, paediatric occurs | exclusion, paediatric occurs | Polat 2021, PMC section 3 |
| Solid pseudopapillary neoplasm (8452/3) | option, paediatric occurs | option, paediatric occurs | Ebrahim 2025, PMC section 13 |

### Screens

- dg_appendix_histology and dg_net_grade: Roganovic 2026 cites added to the neuroendocrine tumour, grade 1, grade 2 and no-grade answers; option order unchanged.
- dg_colorectal_histology: five options added at the top (8480/3, 8490/3, 8140/3, 8220/3, 8211/3, commonest first); the carcinoma answer that goes to the picker was relabelled from 'A carcinoma, adenocarcinoma or neuroendocrine tumour of any type the report names, such as mucinous adenocarcinoma, signet ring cell carcinoma, squamous cell carcinoma or carcinoid' to 'Another carcinoma or neuroendocrine tumour the report names, such as serrated adenocarcinoma, squamous cell carcinoma or carcinoid'.
- dg_pancreas_histology: nine options added (8150/3, 8151/3, 8240/3, 8249/3, 8246/3, 8153/3, 8152/3, 8155/3, 8156/3); order is the two the papers call common, then solid pseudopapillary neoplasm and acinar cell carcinoma as before, then the other reported types in Karges 2025's order; hint added for a hormone type or non-functioning given with a grade; the picker answer relabelled from 'Another carcinoma or neuroendocrine tumour the report names, such as ductal adenocarcinoma or pancreatic neuroendocrine tumour' to 'Another carcinoma or neuroendocrine tumour the report names, such as ductal adenocarcinoma, small cell carcinoma or ACTH-producing tumour'.
- dg_not_malignant_gut: Polat 2021 cites added to the high-grade dysplasia in a polyp (8210/2) and familial adenomatous polyposis (8220/0) answers.

### Left as they were

- Neuroendocrine tumour, grade 3 (appendix), 8249/3: still an option on Pfister 2022's listing of appendiceal neuroendocrine tumours. Roganovic 2026 reports grades 1 and 2 in children and names grade 3 only in the WHO grading table and among follow-up risk features (data gap 4).
- Pancreatic acinar cell carcinoma, 8550/3: still an option on Pfister 2022 alone; no new paper reports it in a child (data gap 3).
- Goblet cell adenocarcinoma 8243/3, low-grade appendiceal mucinous neoplasm 8480/1, ACTH-producing tumour 8158/3, large cell and small cell neuroendocrine carcinoma 8013/3 and 8041/3, and every oesophageal, gastric, small-bowel, anal and biliary carcinoma: no new paper reports them in a child, so they stay in the picker or the exclusions.
- `dg_net_grade` keeps its grade order (grade 1, grade 2, grade 3, no grade, neuroendocrine carcinoma); its hint names the neuroendocrine carcinoma answer as the last answer.
- `dg_pancreas_ihc` keeps its single beta-catenin rule; Ebrahim 2025's beta-catenin-negative paediatric case is data gap 9.
- No new paper names a paediatric digestive entity this part did not already list, so no entity was added outside the site splits above, and no referral changed.
