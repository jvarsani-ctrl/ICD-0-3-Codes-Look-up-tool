# Group 11 evidence — XIf8 bladder, plus renal pelvis, ureter, urethra, prostate, penis, other male genital (XIf10)

Part `XIf8_urinary_male_genital`. Evidence agent output, 8 October 2026. The data is in `XIf8_urinary_male_genital.json` beside this file; this page carries the same content for a reader. Every code was checked in `icdo32.sqlite` and, at its site, in `ICCC-2017.sqlite`. Every quote was checked against its page of the text file by `check_g11_evidence.py` (242 quotes found on the cited page or PMC section, 4 read from table images, after the 8 October 2026 update).

**The finding that shapes this part:** no file in this part reports a carcinoma of the bladder, renal pelvis, ureter, urethra, prostate or penis in a patient aged 0 to 18. Pfister 2022 Table 3 (PDF pp. 12-13) lists only kidney and testis tumours under renal and male genital tumours. By ruling 1, every carcinoma here is a picker entry, and the histology screens offer carcinoma, NOS, the picker, the non-invasive exclusions and the referrals. Data gap 1 names the sources that would change this.

**Updated 8 October 2026:** Liu 2025, a paediatric bladder series, reports urothelial papilloma, PUNLMP and low-grade non-invasive urothelial carcinoma of the bladder in children, and rare infiltration beyond the mucosa. Invasive urothelial carcinoma (8120/3) is now an option on `gu_urinary_histology`; every other carcinoma in this part stays a picker entry. Section 11 lists each change.

## 1 Sources

| File | Citation | WHO volume |
|---|---|---|
| `XIf8-bladder-XIf10-prostate-urinary-tract__Netto-2022.txt` | Netto GJ, Amin MB, Berney DM, et al. The 2022 World Health Organization Classification of Tumors of the Urinary System and Male Genital Organs - Part B: Prostate and Urinary Tract Tumors. Eur Urol 2022;82(5):469-482 | WHO Classification of Tumours, Urinary and Male Genital Tumours, 5th ed., 2022 |
| `XIf8-bladder__ICCR-Urinary-Bladder-2nd.txt` | International Collaboration on Cancer Reporting. Carcinoma of the Bladder - Cystectomy, Cystoprostatectomy and Diverticulectomy Specimen. Histopathology Reporting Guide, 2nd ed., v2.0, December 2025 | WHO Urinary and Male Genital Tumours, 5th ed., 2022, with the Corrigenda of July 2024 |
| `XIf10-renal-pelvis-ureter__ICCR-Renal-Pelvis-Ureter-2nd.txt` | International Collaboration on Cancer Reporting. Carcinoma of the Renal Pelvis and Ureter. Histopathology Reporting Guide, 2nd ed., v2.0, December 2025 | WHO Urinary and Male Genital Tumours, 5th ed., 2022, with the Corrigenda of July 2024 |
| `XIf10-prostate__ICCR-Prostate-3rd.txt` | International Collaboration on Cancer Reporting. Prostate Cancer (radical prostatectomy). Histopathology Reporting Guide, 3rd ed., v3.0, November 2024 | WHO Urinary and Male Genital Tumours, 5th ed., 2022, with the Corrigenda of July 2024 |
| `XIf10-penis__ICCR-Penis-Distal-Urethra-2nd.txt` | International Collaboration on Cancer Reporting. Carcinoma of the Penis and Distal Urethra. Histopathology Reporting Guide, 2nd ed., v2.0, November 2024 | WHO Urinary and Male Genital Tumours, 5th ed., 2022, with the Corrigenda of July 2024 |
| `ALL-paediatric-occurrence__Pfister-2022.txt` | Pfister SM, Reyes-Mugica M, Chan JKC, et al. A Summary of the Inaugural WHO Classification of Pediatric Tumors: Transitioning from the Optical into the Molecular Era. Cancer Discov 2022;12(2):331-355 | WHO Paediatric Tumours, 5th ed., 2022 |
| `RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt` | World Health Organization. International Classification of Diseases for Oncology, 3rd ed., 1st revision (ICD-O-3.1), coding rules A to K, printed pp. 14-26 | ICD-O-3.1, 2013 |
| `XIf8-bladder-urothelial-paediatric__Liu-2025.txt` | Liu P, et al. Pediatric papillary urothelial neoplasm: 18-year single-center experience in diagnosis and treatment. BMC Urol 2025. doi:10.1186/s12894-025-01831-6 | not a WHO summary; paediatric evidence |

Tables read from the PDF page image: Netto 2022 Table 1 (PDF p. 2) and Table 3 (PDF p. 7); ICCR Bladder Table 1 (PDF pp. 10-11); ICCR Renal Pelvis Table 1 (PDF p. 9); ICCR Prostate Table 1 (PDF p. 7); ICCR Penis Table 1 (PDF pp. 10-11); Pfister 2022 Table 3 (PDF pp. 12-13). The ICCR guides carry the WHO 5th edition Corrigenda of July 2024; Netto 2022 predates them. Where they differ, the ICCR (the later document) is followed and the difference is listed in section 8.

Liu 2025 is a PubMed Central text (PMC12254994, fetched 8 October 2026). It has sections, not pages; its citations give the PMC section number in place of a PDF page.

Sites in this part:

| Topography | ICCC-3 subgroup |
|---|---|
| C67.0 | XIf8 |
| C67.1 | XIf8 |
| C67.2 | XIf8 |
| C67.3 | XIf8 |
| C67.4 | XIf8 |
| C67.5 | XIf8 |
| C67.6 | XIf8 |
| C67.7 | XIf8 |
| C67.8 | XIf8 |
| C67.9 | XIf8 |
| C65.9 | XIf10 |
| C66.9 | XIf10 |
| C68.0 | XIf10 |
| C68.1 | XIf10 |
| C68.8 | XIf10 |
| C68.9 | XIf10 |
| C61.9 | XIf10 |
| C60.0 | XIf10 |
| C60.1 | XIf10 |
| C60.2 | XIf10 |
| C60.8 | XIf10 |
| C63.0 | XIf10 |
| C63.1 | XIf10 |
| C63.7 | XIf10 |
| C63.8 | XIf10 |
| C63.9 | XIf10 |

C60.9 penis, NOS and C63.2 scrotum belong to XIe (skin carcinomas) and are routed to the skin carcinoma tree. C64.9 kidney is Group 6; C62 testis is Group 10.

## 2 Entities

| Entity (WHO term) | Code | ICD-O-3.2 term matched (level) | ICD-O-3.2 preferred term | Paediatric | Decision | Source |
|---|---|---|---|---|---|---|
| Urothelial papilloma | 8120/0 | Urothelial papilloma, NOS (Preferred) | Urothelial papilloma, NOS | common | exclusion | Netto 2022, PDF p. 7 ("8120/0 Urothelial papilloma"); Liu 2025, PMC section 8 ("the two most common types of bladder neoplasms in children, UP and PUNLMP"); Liu 2025, PMC section 7 ("comprised 17 patients, including 11 children diagnosed with UP"); Liu 2025, PMC section 7 ("The average age of onset was 10.5 years (range: 3–18 years)") |
| Urothelial papilloma, inverted | 8121/0 | Urothelial papilloma, inverted (Related) | Sinonasal papilloma, exophytic | not_reported | exclusion | Netto 2022, PDF p. 7 ("8121/0 Urothelial papilloma, inverted") |
| Papillary urothelial neoplasm of low malignant potential (including the inverted form) | 8130/1 | Papillary urothelial neoplasm of low malignant potential (Preferred) | Papillary urothelial neoplasm of low malignant potential | common | exclusion | Netto 2022, PDF p. 7 ("8130/1 Papillary urothelial neoplasm of low malignant potential"); ICCR Bladder 2025, PDF p. 12 ("which will not invade or metastasise"); Liu 2025, PMC section 8 ("the two most common types of bladder neoplasms in children, UP and PUNLMP"); Liu 2025, PMC section 8 ("The majority of urothelial bladder tumors in children are papillary urothelial neoplasm"); Liu 2025, PMC section 7 ("The study focused on six male children with PUNLMP") |
| Non-invasive papillary urothelial carcinoma, low grade and high grade (including inverted growth) | 8130/2 | Papillary urothelial carcinoma, non-invasive (Preferred) | Papillary urothelial carcinoma, non-invasive | common | exclusion | Netto 2022, PDF p. 7 ("8130/2 Noninvasive papillary urothelial carcinoma, low grade"); Netto 2022, PDF p. 7 ("8130/2 Noninvasive papillary urothelial carcinoma, high grade"); ICCR Bladder 2025, PDF p. 4 ("Non-invasive papillary carcinoma"); Liu 2025, PMC section 8 ("The majority of urothelial bladder tumors in children are papillary urothelial neoplasm"); Liu 2025, PMC section 8 ("(PUNLMP) and low-grade urothelial carcinomas, often confined to the mucosal layer (Ta)") |
| Urothelial carcinoma in situ | 8120/2 | Urothelial carcinoma in situ (Preferred) | Urothelial carcinoma in situ | not_reported | exclusion | Netto 2022, PDF p. 7 ("8120/2 Urothelial carcinoma in situ") |
| Invasive urothelial carcinoma (conventional, nested, large nested, tubular and microcystic subtypes) | 8120/3 | Urothelial carcinoma, NOS (Synonym) | Transitional cell carcinoma, NOS | occurs | option | Netto 2022, PDF p. 7 ("8120/3 Invasive urothelial carcinoma"); Netto 2022, PDF p. 7 ("8120/3 Nested urothelial carcinoma"); ICCR Bladder 2025, PDF p. 8 ("a tumour is classified as a urothelial carcinoma if there is any identifiable urothelial component"); Pfister 2022, PDF p. 12 ("Renal and male genital tumors Kidney Nephroblastic and related tumors"); Liu 2025, PMC section 8 ("often confined to the mucosal layer (Ta) with rare infiltration into deeper layers"); Liu 2025, PMC section 8 ("childhood bladder urothelial carcinoma is typically low-grade") |
| Papillary urothelial carcinoma, invasive | 8130/3 | Papillary urothelial carcinoma (Preferred) | Papillary urothelial carcinoma | not_reported | not_built | Netto 2022, PDF p. 7 ("8130/2 Noninvasive papillary urothelial carcinoma, high grade"); Netto 2022, PDF p. 7 ("8120/3 Invasive urothelial carcinoma") |
| Urothelial carcinoma with squamous, glandular or trophoblastic differentiation | 8120/3 | Urothelial carcinoma, NOS (Synonym) | Transitional cell carcinoma, NOS | not_reported | picker | Netto 2022, PDF p. 7 ("8120/3 Urothelial carcinoma with squamous differentiation"); Netto 2022, PDF p. 7 ("8120/3 Urothelial carcinoma with trophoblastic differentiation"); ICD-O-3.1 rules, PDF p. 11 ("coders should use the numerically higher code number, 8120/3 in this example") |
| Plasmacytoid urothelial carcinoma | 8120/3 | Urothelial carcinoma, NOS (Synonym) | Transitional cell carcinoma, NOS | not_reported | picker | Netto 2022, PDF p. 7 ("8122/3 Plasmacytoid urothelial"); ICCR Bladder 2025, PDF p. 10 (table image: "Plasmacytoid (no code printed)") |
| Lipid-rich urothelial carcinoma | 8120/3 | Urothelial carcinoma, NOS (Synonym) | Transitional cell carcinoma, NOS | not_reported | picker | Netto 2022, PDF p. 7 ("8120/3 Lipid-rich urothelial carcinoma") |
| Clear cell (glycogen-rich) urothelial carcinoma | 8120/3 | Urothelial carcinoma, NOS (Synonym) | Transitional cell carcinoma, NOS | not_reported | picker | Netto 2022, PDF p. 7 ("8120/3 Clear cell (glycogen-rich) urothelial carcinoma"); Netto 2022, PDF p. 8 ("is added to clear cell urothelial carcinoma subtype") |
| Micropapillary urothelial carcinoma | 8131/3 | Urothelial carcinoma, micropapillary (Preferred) | Urothelial carcinoma, micropapillary | not_reported | picker | Netto 2022, PDF p. 7 ("8131/3 Micropapillary urothelial carcinoma"); ICCR Bladder 2025, PDF p. 10 ("Micropapillary 8131/3") |
| Sarcomatoid urothelial carcinoma | 8122/3 | Urothelial carcinoma, sarcomatoid (Preferred) | Urothelial carcinoma, sarcomatoid | not_reported | picker | ICCR Bladder 2025, PDF p. 10 ("Sarcomatoid 8122/3"); ICCR Renal Pelvis 2025, PDF p. 9 ("Sarcomatoid 8122/3"); Netto 2022, PDF p. 7 ("8120/3 Sarcomatoid urothelial carcinoma") |
| Lymphoepithelioma-like urothelial carcinoma | 8082/3 | Lymphoepithelioma-like carcinoma (Synonym) | Lymphoepithelial carcinoma | not_reported | picker | Netto 2022, PDF p. 7 ("8082/3 Lymphoepithelioma-like urothelial carcinoma"); ICCR Bladder 2025, PDF p. 10 ("Lymphoepithelioma-like 8082/3") |
| Giant cell urothelial carcinoma | 8031/3 | Giant cell carcinoma (Preferred) | Giant cell carcinoma | not_reported | picker | Netto 2022, PDF p. 7 ("8031/3 Giant cell urothelial carcinoma") |
| Poorly differentiated urothelial carcinoma | 8020/3 | Carcinoma, poorly differentiated, NOS (Related) | Carcinoma, undifferentiated, NOS | not_reported | picker | Netto 2022, PDF p. 7 ("8020/3 Poorly differentiated urothelial carcinoma") |
| Squamous papilloma | 8052/0 | Squamous papilloma (Synonym) | Squamous cell papilloma, NOS | not_reported | exclusion | Netto 2022, PDF p. 7 ("8052/0 Squamous papilloma") |
| Verrucous carcinoma (urinary tract) | 8051/3 | Verrucous carcinoma, NOS (Preferred) | Verrucous carcinoma, NOS | not_reported | picker | Netto 2022, PDF p. 7 ("8051/3 Verrucous carcinoma"); ICCR Bladder 2025, PDF p. 11 ("Verrucous carcinoma 8051/3") |
| Pure squamous cell carcinoma of the urothelial tract | 8070/3 | Squamous cell carcinoma, NOS (Preferred) | Squamous cell carcinoma, NOS | not_reported | picker | Netto 2022, PDF p. 7 ("Pure squamous carcinoma of the urothelial"); ICCR Bladder 2025, PDF p. 11 ("Pure squamous cell carcinoma 8070/3") |
| Villous adenoma | 8261/0 | Villous adenoma, NOS (Preferred) | Villous adenoma, NOS | not_reported | exclusion | Netto 2022, PDF p. 7 ("8261/0 Villous adenoma") |
| Tubular adenoma | 8211/0 | Tubular adenoma, NOS (Preferred) | Tubular adenoma, NOS | not_reported | exclusion | Netto 2022, PDF p. 7 ("8211/0 Tubular adenoma") |
| Tubulovillous adenoma | 8263/0 | Tubulovillous adenoma, NOS (Preferred) | Tubulovillous adenoma, NOS | not_reported | exclusion | Netto 2022, PDF p. 7 ("8263/0 Tubulovillous adenoma") |
| Adenocarcinoma in situ | 8140/2 | Adenocarcinoma in situ, NOS (Preferred) | Adenocarcinoma in situ, NOS | not_reported | exclusion | Netto 2022, PDF p. 7 ("8140/2 Adenocarcinoma in situ") |
| Adenocarcinoma, NOS (urinary tract) | 8140/3 | Adenocarcinoma, NOS (Preferred) | Adenocarcinoma, NOS | not_reported | picker | Netto 2022, PDF p. 7 ("8140/3 Adenocarcinoma, NOS"); ICCR Bladder 2025, PDF p. 9 ("the diagnosis of primary origin requires clinical correlation to exclude the possibility of origin") |
| Enteric adenocarcinoma | 8144/3 | Adenocarcinoma, enteric (Synonym) | Adenocarcinoma, intestinal type | not_reported | picker | Netto 2022, PDF p. 7 ("8144/3 Enteric adenocarcinoma"); ICCR Bladder 2025, PDF p. 11 ("Enteric 8144/3") |
| Mucinous adenocarcinoma (urinary tract) | 8480/3 | Mucinous adenocarcinoma (Preferred) | Mucinous adenocarcinoma | not_reported | picker | Netto 2022, PDF p. 7 ("8480/3 Mucinous adenocarcinoma"); ICCR Bladder 2025, PDF p. 11 ("Mucinous 8480/3") |
| Mixed adenocarcinoma | 8140/3 | Adenocarcinoma, NOS (Preferred) | Adenocarcinoma, NOS | not_reported | picker | Netto 2022, PDF p. 7 ("8323/3 Mixed adenocarcinoma"); ICCR Bladder 2025, PDF p. 11 ("Mixed 8140/3") |
| Signet ring cell adenocarcinoma | 8490/3 | Signet ring cell adenocarcinoma (Synonym) | Signet ring cell carcinoma | not_reported | picker | Netto 2022, PDF p. 7 ("8490/3 Signet ring cell adenocarcinoma") |
| Urachal carcinoma (subtype not named) | 8010/3 | Carcinoma, NOS (Preferred) | Carcinoma, NOS | not_reported | picker | Netto 2022, PDF p. 7 ("8010/3 Urachal carcinoma"); ICCR Bladder 2025, PDF p. 9 ("If a diagnosis of urachal carcinoma is rendered the subtype must be specified."); ICCR Bladder 2025, PDF p. 9 ("diagnosis of urachal carcinoma include location in the bladder dome or anterior wall") |
| Mucinous cystic tumour of low malignant potential (urachus) | 8472/1 | Mucinous tumor, NOS, of low malignant potential (Synonym) | Mucinous cystic tumor of borderline malignancy | not_reported | exclusion | ICCR Bladder 2025, PDF p. 9 ("mucinous cystic tumour of low malignant potential") |
| Carcinoma of Littre, Skene or Cowper glands (urethral accessory gland carcinoma) | 8140/3 | Carcinoma of Skene, Cowper and Littre glands (Related) | Adenocarcinoma, NOS | not_reported | picker | Netto 2022, PDF p. 7 ("8140/3 Carcinoma of Littré glands"); Netto 2022, PDF p. 7 ("8140/3 Carcinoma of Skene glands"); Netto 2022, PDF p. 7 ("8140/3 Carcinoma of Cowper glands") |
| Clear cell adenocarcinoma (Mullerian type) | 8310/3 | Clear cell adenocarcinoma, NOS (Preferred) | Clear cell adenocarcinoma, NOS | not_reported | picker | Netto 2022, PDF p. 7 ("8310/3 Clear cell carcinoma"); ICCR Bladder 2025, PDF p. 11 ("Clear cell adenocarcinoma 8310/3"); ICCR Bladder 2025, PDF p. 9 ("it represents secondary involvement most often originating in an urethral diverticulum") |
| Endometrioid carcinoma (Mullerian type) | 8380/3 | Endometrioid carcinoma, NOS (Synonym) | Endometrioid adenocarcinoma, NOS | not_reported | picker | Netto 2022, PDF p. 7 ("8380/3 Endometrioid carcinoma"); ICCR Bladder 2025, PDF p. 11 ("Endometrioid carcinoma 8380/3") |
| Small cell neuroendocrine carcinoma | 8041/3 | Small cell neuroendocrine carcinoma (Related) | Small cell carcinoma, NOS | not_reported | picker | ICCR Bladder 2025, PDF p. 11 ("Small cell neuroendocrine carcinoma 8041/3"); ICCR Bladder 2025, PDF p. 8 ("An exception to this rule is for neuroendocrine carcinomas"); ICCR Bladder 2025, PDF p. 9 ("In cases with pure small cell morphology the possibility of direct spread from") |
| Mixed neuroendocrine neoplasm (small cell neuroendocrine carcinoma with urothelial or another carcinoma) | 8045/3 | Mixed small cell carcinoma (Synonym) | Combined small cell carcinoma | not_reported | picker | ICCR Bladder 2025, PDF p. 11 (table image: "Mixed neuroendocrine neoplasms (no code printed)"); ICCR Bladder 2025, PDF p. 8 ("cases with a small cell neuroendocrine carcinoma component irrespective of the amount are managed") |
| Large cell neuroendocrine carcinoma | 8013/3 | Large cell neuroendocrine carcinoma (Preferred) | Large cell neuroendocrine carcinoma | not_reported | picker | ICCR Bladder 2025, PDF p. 11 ("Large cell neuroendocrine carcinoma 8013/3") |
| Well differentiated neuroendocrine tumour | 8240/3 | Neuroendocrine tumor, NOS (Preferred) | Neuroendocrine tumor, NOS | not_reported | picker | ICCR Bladder 2025, PDF p. 11 ("Well differentiated neuroendocrine tumour 8240/3") |
| Paraganglioma | 8693/3 | Extra-adrenal paraganglioma, NOS (Preferred) | Extra-adrenal paraganglioma, NOS | not_reported | refer to Group 4 | ICCR Bladder 2025, PDF p. 11 ("Paraganglioma is not an epithelial derived tumour.") |
| Rhabdomyosarcoma (embryonal including botryoid, alveolar, NOS) | 8910/3 | Embryonal rhabdomyosarcoma, NOS (Preferred) | Embryonal rhabdomyosarcoma, NOS | occurs | refer to Group 9 | Pfister 2022, PDF p. 6 ("with rhabdomyosarcomas (RMS) being the most common"); Liu 2025, PMC section 8 ("other pediatric malignancies, including Wilms tumor and bladder rhabdomyosarcoma") |
| Inflammatory myofibroblastic tumour | 8825/1 | Inflammatory myofibroblastic tumor (Synonym) | Myofibroblastic tumor, NOS | occurs | exclusion | Pfister 2022, PDF p. 6 ("Infantile fibrosarcoma and inflammatory myofibroblastic tumor are both tyrosine kinase") |
| Nephroblastoma at the renal pelvis or ureter | 8960/3 | Wilms tumor (Synonym) | Nephroblastoma, NOS | common | refer to Group 6 | Pfister 2022, PDF p. 12 ("Nephroblastic and related tumors Pediatric cystic nephroma Nephroblastoma") |
| Renal cell carcinoma with MiT translocation | 8311/3 | MiT family translocation carcinoma (Related) | Hereditary leiomyomatosis and renal cell carcinoma (HLRCC) syndrome-associated renal cell carcinoma | occurs | refer to Group 6 | Pfister 2022, PDF p. 12 ("Renal cell carcinoma with MIT translocations") |
| Yolk sac tumour and other extragonadal germ cell tumours | 9071/3 | Yolk sac tumor, NOS (Preferred) | Yolk sac tumor, NOS | occurs | refer to Group 10 | Pfister 2022, PDF p. 12 ("Embryonal carcinoma Yolk sac tumor"); Netto 2022, PDF p. 7 ("8120/3 Urothelial carcinoma with trophoblastic differentiation") |
| Acinar adenocarcinoma (including pleomorphic giant cell and prostatic intraepithelial neoplasia-like subtypes) | 8140/3 | Acinar adenocarcinoma of prostate (Related) | Adenocarcinoma, NOS | not_reported | picker | Netto 2022, PDF p. 2 ("8140/3 Acinar adenocarcinoma"); ICCR Prostate 2024, PDF p. 7 ("The vast majority (>95%) of prostate cancers are acinar adenocarcinomas."); Pfister 2022, PDF p. 12 ("Renal and male genital tumors Kidney Nephroblastic and related tumors") |
| Signet ring cell-like acinar adenocarcinoma | 8490/3 | Acinar adenocarcinoma, signet ring-like variant (Synonym) | Signet ring cell carcinoma | not_reported | picker | Netto 2022, PDF p. 2 ("8490/3 Signet ring cell-like acinar adenocarcinoma") |
| Sarcomatoid acinar adenocarcinoma | 8572/3 | Acinar adenocarcinoma, sarcomatoid variant (Synonym) | Adenocarcinoma with spindle cell metaplasia | not_reported | picker | Netto 2022, PDF p. 2 ("8572/3 Sarcomatoid acinar adenocarcinoma"); ICCR Prostate 2024, PDF p. 7 ("Sarcomatoid acinar adenocarcinoma 8572/3") |
| Ductal adenocarcinoma (prostate) | 8500/3 | Duct adenocarcinoma, NOS (Synonym) | Infiltrating duct carcinoma, NOS | not_reported | picker | Netto 2022, PDF p. 2 ("8500/3 Ductal adenocarcinoma"); ICCR Prostate 2024, PDF p. 7 ("Ductal adenocarcinoma 8500/3"); ICD-O-3.1 rules, PDF p. 10 ("Infiltrating duct carcinoma, NOS C50._ Breast C07.9 Parotid gland") |
| Treatment-related neuroendocrine prostatic carcinoma (adenocarcinoma with neuroendocrine differentiation) | 8574/3 | Adenocarcinoma with neuroendocrine differentiation (Preferred) | Adenocarcinoma with neuroendocrine differentiation | not_reported | picker | Netto 2022, PDF p. 2 ("8574/3 Treatment-related neuroendocrine prostatic carcinomas"); ICCR Prostate 2024, PDF p. 7 ("Adenocarcinoma with neuroendocrine differentiation 8574/3") |
| Adenosquamous carcinoma (prostate) | 8560/3 | Adenosquamous carcinoma (Preferred) | Adenosquamous carcinoma | not_reported | picker | Netto 2022, PDF p. 2 ("8560/3 Adenosquamous carcinoma") |
| Squamous cell carcinoma (prostate) | 8070/3 | Squamous cell carcinoma, NOS (Preferred) | Squamous cell carcinoma, NOS | not_reported | picker | Netto 2022, PDF p. 2 ("8070/3 Squamous cell carcinoma") |
| Adenoid cystic (basal cell) carcinoma of the prostate | 8147/3 | Basal cell carcinoma of prostate (Related) | Basal cell adenocarcinoma | not_reported | picker | Netto 2022, PDF p. 2 ("8147/3 Adenoid cystic (basal cell)"); ICD-O-3.1 rules, PDF p. 10 ("C60._ Penis C63.2 Scrotum C61.9 Prostate") |
| Urothelial carcinoma arising in the prostate | 8120/3 | Urothelial carcinoma, NOS (Synonym) | Transitional cell carcinoma, NOS | not_reported | picker | ICCR Prostate 2024, PDF p. 4 ("urothelial carcinomas arising within the prostate are included in a separate ICCR dataset") |
| Cystadenoma (prostate) | 8440/0 | Cystadenoma, NOS (Preferred) | Cystadenoma, NOS | not_reported | exclusion | Netto 2022, PDF p. 2 ("8440/0 Cystadenoma") |
| Prostatic intraepithelial neoplasia, high grade | 8148/2 | Prostatic intraepithelial neoplasia, high grade (Synonym) | Glandular intraepithelial neoplasia, high grade | not_reported | exclusion | Netto 2022, PDF p. 2 ("8148/2 Prostatic intraepithelial neoplasia, high grade") |
| Intraductal carcinoma of the prostate (with no invasive carcinoma) | 8500/2 | Intraductal carcinoma, NOS (Synonym) | Intraductal carcinoma, noninfiltrating, NOS | not_reported | exclusion | Netto 2022, PDF p. 2 ("8500/2 Intraductal carcinoma"); Netto 2022, PDF p. 3 ("is an exceedingly rare finding in biopsies and prostatectomies") |
| Stromal tumour of uncertain malignant potential | 8935/1 | Stromal tumor of uncertain malignant potential (Related) | Stromal tumor, NOS | not_reported | exclusion | Netto 2022, PDF p. 2 ("8935/1 Stromal tumor of uncertain malignant potential") |
| Stromal sarcoma (prostate) | 8935/3 | Stromal sarcoma, NOS (Preferred) | Stromal sarcoma, NOS | not_reported | refer to Group 12 | Netto 2022, PDF p. 2 ("8935/3 Stromal sarcoma"); ICCR Prostate 2024, PDF p. 7 ("Stromal sarcoma 8935/3") |
| Squamous cell carcinoma, HPV-associated | 8085/3 | Squamous cell carcinoma, HPV positive (Preferred) | Squamous cell carcinoma, HPV positive | not_reported | picker | ICCR Penis 2024, PDF p. 10 ("Squamous cell carcinoma, HPV-associated 8085/3"); ICCR Penis 2024, PDF p. 16 ("the p16 protein is upregulated and can be detected in high risk HPV related malignancies"); Pfister 2022, PDF p. 12 ("Renal and male genital tumors Kidney Nephroblastic and related tumors") |
| Basaloid squamous cell carcinoma | 8083/3 | Basaloid squamous cell carcinoma (Preferred) | Basaloid squamous cell carcinoma | not_reported | picker | ICCR Penis 2024, PDF p. 10 ("Basaloid squamous cell carcinoma 8083/3") |
| Warty carcinoma | 8054/3 | Warty carcinoma (Preferred) | Warty carcinoma | not_reported | picker | ICCR Penis 2024, PDF p. 10 ("Warty carcinoma 8054/3") |
| Clear cell squamous cell carcinoma | 8084/3 | Squamous cell carcinoma, clear cell type (Preferred) | Squamous cell carcinoma, clear cell type | not_reported | picker | ICCR Penis 2024, PDF p. 10 ("Clear cell squamous cell carcinoma 8084/3") |
| Lymphoepithelial carcinoma (penis) | 8082/3 | Lymphoepithelial carcinoma (Preferred) | Lymphoepithelial carcinoma | not_reported | picker | ICCR Penis 2024, PDF p. 10 ("Lymphoepithelial carcinoma 8082/3") |
| Squamous cell carcinoma, HPV-independent | 8086/3 | Squamous cell carcinoma, HPV negative (Preferred) | Squamous cell carcinoma, HPV negative | not_reported | picker | ICCR Penis 2024, PDF p. 10 ("Squamous cell carcinoma, HPV-independent") |
| Squamous cell carcinoma, usual type | 8070/3 | Squamous cell carcinoma, usual type (Synonym) | Squamous cell carcinoma, NOS | not_reported | picker | ICCR Penis 2024, PDF p. 10 ("Squamous cell carcinoma, usual type 8086/3") |
| Verrucous carcinoma, including carcinoma cuniculatum (penis) | 8051/3 | Verrucous carcinoma, NOS (Preferred) | Verrucous carcinoma, NOS | not_reported | picker | ICCR Penis 2024, PDF p. 10 ("Verrucous carcinoma (including carcinoma cuniculatum) 8051/3") |
| Papillary squamous cell carcinoma | 8052/3 | Papillary squamous cell carcinoma (Preferred) | Papillary squamous cell carcinoma | not_reported | picker | ICCR Penis 2024, PDF p. 10 ("Papillary squamous cell carcinoma 8052/3") |
| Sarcomatoid squamous cell carcinoma | 8074/3 | Squamous cell carcinoma, sarcomatoid (Synonym) | Squamous cell carcinoma, spindle cell | not_reported | picker | ICCR Penis 2024, PDF p. 10 ("Sarcomatoid squamous cell carcinoma 8074/3") |
| Squamous cell carcinoma, NOS (p16 not available) | 8070/3 | Squamous cell carcinoma, NOS (Preferred) | Squamous cell carcinoma, NOS | not_reported | picker | ICCR Penis 2024, PDF p. 11 ("p16 is not available or is not performed the tumour should be designated as SCC-NOS") |
| Adenosquamous carcinoma (penis) | 8560/3 | Adenosquamous carcinoma (Preferred) | Adenosquamous carcinoma | not_reported | picker | ICCR Penis 2024, PDF p. 11 ("Adenosquamous carcinoma 8560/3") |
| Mucoepidermoid carcinoma (penis) | 8430/3 | Mucoepidermoid carcinoma (Preferred) | Mucoepidermoid carcinoma | not_reported | picker | ICCR Penis 2024, PDF p. 11 ("Mucoepidermoid carcinoma 8430/3") |
| Paget disease, extramammary (penis) | 8542/3 | Paget disease, extramammary (Preferred) | Paget disease, extramammary | not_reported | picker | ICCR Penis 2024, PDF p. 11 ("Paget disease, extramammary 8542/3") |
| Medullary carcinoma (emerging entity, penis) | 8510/3 | Medullary carcinoma, NOS (Preferred) | Medullary carcinoma, NOS | not_reported | picker | ICCR Penis 2024, PDF p. 11 ("Medullary carcinoma is a poorly differentiated carcinoma that grows in solid sheets") |
| High grade squamous intraepithelial lesion (penile intraepithelial neoplasia, HPV-associated) | 8077/2 | High grade squamous intraepithelial lesion (Synonym) | Squamous intraepithelial neoplasia, high grade | not_reported | exclusion | ICCR Penis 2024, PDF p. 11 ("High grade squamous intraepithelial lesion 8077/2") |
| Differentiated penile intraepithelial neoplasia | 8071/2 | Differentiated penile intraepithelial neoplasia (PeIN) (Related) | Differentiated intraepithelial neoplasia | not_reported | exclusion | ICCR Penis 2024, PDF p. 11 ("Differentiated penile intraepithelial neoplasia 8071/2") |
| Carcinoma, no type named | 8010/3 | Carcinoma, NOS (Preferred) | Carcinoma, NOS | not_reported | option | ICD-O-3.1 rules, PDF p. 2 ("the appropriate 5th digit behavior code even if the exact term is not listed") |

Why each decision was taken:

- **Urothelial papilloma, 8120/0.** Benign urothelial papillary lesion; behaviour /0 is outside Group XI. Liu 2025 names urothelial papilloma and PUNLMP the two commonest bladder neoplasms in children; 11 of its 17 children, aged 3 to 18, had urothelial papilloma.
- **Urothelial papilloma, inverted, 8121/0.** Benign. ICD-O-3.2 lists the urothelial term as a related term under 8121/0, whose preferred term is a sinonasal papilloma.
- **Papillary urothelial neoplasm of low malignant potential (including the inverted form), 8130/1.** Behaviour /1. The ICCR states it does not invade or metastasise. Liu 2025 names PUNLMP and urothelial papilloma the two commonest bladder neoplasms in children, and states that most urothelial bladder tumours in children are PUNLMP or low-grade urothelial carcinoma; 6 of its 17 children had PUNLMP.
- **Non-invasive papillary urothelial carcinoma, low grade and high grade (including inverted growth), 8130/2.** Both grades code 8130/2 (pTa). Behaviour /2 is outside Group XI. Liu 2025 states that most urothelial bladder tumours in children are PUNLMP or low-grade urothelial carcinoma confined to the mucosa (pTa); its own 17 children had none.
- **Urothelial carcinoma in situ, 8120/2.** Flat carcinoma in situ (pTis); behaviour /2 is outside Group XI.
- **Invasive urothelial carcinoma (conventional, nested, large nested, tubular and microcystic subtypes), 8120/3.** The WHO code for invasive urothelial carcinoma and most of its subtypes. A tumour with any urothelial component, including urothelial carcinoma in situ, is a urothelial carcinoma unless it is a neuroendocrine carcinoma. Pfister 2022 Table 3 does not list it. Liu 2025 states that urothelial carcinoma of the bladder in children is typically low grade and confined to the mucosa (pTa), with rare infiltration into deeper layers; its own 17 children had urothelial papilloma or PUNLMP only. An option on `gu_urinary_histology`. At the prostate it stays a picker entry (urothelial carcinoma arising in the prostate).
- **Papillary urothelial carcinoma, invasive, 8130/3.** Every /3 term at 8130 is [obs] in ICD-O-3.2. The WHO 2022 table prints 8130 only at /1 and /2; an invasive papillary urothelial carcinoma is an invasive urothelial carcinoma, 8120/3.
- **Urothelial carcinoma with squamous, glandular or trophoblastic differentiation, 8120/3.** The WHO codes divergent differentiation 8120/3. Rule K agrees for squamous differentiation (8120 is higher than 8070); for glandular differentiation Rule K would give 8140 (registrar question). No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Plasmacytoid urothelial carcinoma, 8120/3.** Netto 2022 Table 3 prints 8122/3 beside plasmacytoid; ICD-O-3.2 8122/3 is sarcomatoid urothelial carcinoma, and the ICCR tables (with the July 2024 corrigenda) print no code for plasmacytoid. Recorded at the head code 8120/3. No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Lipid-rich urothelial carcinoma, 8120/3.** The WHO prints 8120/3. ICD-O-3.2 holds 8314/3 Lipid-rich carcinoma, which Rule K would prefer (registrar question). No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Clear cell (glycogen-rich) urothelial carcinoma, 8120/3.** The WHO prints 8120/3 and adds glycogen-rich to separate it from Mullerian clear cell adenocarcinoma. ICD-O-3.2 holds 8315/3 Glycogen-rich carcinoma, which Rule K would prefer (registrar question). No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Micropapillary urothelial carcinoma, 8131/3.** No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Sarcomatoid urothelial carcinoma, 8122/3.** ICCR Bladder and ICCR Renal Pelvis (with the July 2024 corrigenda) print 8122/3; Netto 2022 Table 3 prints 8120/3. ICD-O-3.2 names sarcomatoid urothelial carcinoma at 8122/3. No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Lymphoepithelioma-like urothelial carcinoma, 8082/3.** WHO subtype code. Rule K would give 8120/3 (registrar question). No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Giant cell urothelial carcinoma, 8031/3.** WHO subtype code. Rule K would give 8120/3 (registrar question). No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Poorly differentiated urothelial carcinoma, 8020/3.** WHO subtype code. Rule K would give 8120/3 (registrar question). No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Squamous papilloma, 8052/0.** Benign; behaviour /0.
- **Verrucous carcinoma (urinary tract), 8051/3.** No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Pure squamous cell carcinoma of the urothelial tract, 8070/3.** Pure squamous carcinoma with no urothelial component. Keratinising squamous metaplasia supports a primary squamous cell carcinoma. No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Villous adenoma, 8261/0.** Benign; behaviour /0.
- **Tubular adenoma, 8211/0.** Benign; behaviour /0.
- **Tubulovillous adenoma, 8263/0.** Benign; behaviour /0.
- **Adenocarcinoma in situ, 8140/2.** Behaviour /2 is outside Group XI.
- **Adenocarcinoma, NOS (urinary tract), 8140/3.** Primary origin needs clinical correlation to exclude spread from another site. No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Enteric adenocarcinoma, 8144/3.** No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Mucinous adenocarcinoma (urinary tract), 8480/3.** No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Mixed adenocarcinoma, 8140/3.** Netto 2022 Table 3 prints 8323/3; ICCR Bladder and ICCR Renal Pelvis, which carry the July 2024 corrigenda, print 8140/3. The later document is followed (registrar question). No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Signet ring cell adenocarcinoma, 8490/3.** No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Urachal carcinoma (subtype not named), 8010/3.** The WHO prints 8010/3. The ICCR requires the subtype to be named; a named subtype (most often mucinous adenocarcinoma) takes its own code. Criteria: bladder dome or anterior wall, epicentre in the bladder wall or perivesical tissue. No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Mucinous cystic tumour of low malignant potential (urachus), 8472/1.** The ICCR names the entity without a code; the nearest ICD-O-3.2 term is at 8472/1. Behaviour /1 is outside Group XI whichever /1 code the WHO assigns.
- **Carcinoma of Littre, Skene or Cowper glands (urethral accessory gland carcinoma), 8140/3.** ICD-O-3.2 prints the term under 8140/3, matching the WHO code. No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Clear cell adenocarcinoma (Mullerian type), 8310/3.** In the bladder it most often represents secondary involvement from a urethral diverticulum. No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Endometrioid carcinoma (Mullerian type), 8380/3.** No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Small cell neuroendocrine carcinoma, 8041/3.** Exception to the urothelial rule. Pure small cell morphology requires clinical exclusion of spread from another organ. No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Mixed neuroendocrine neoplasm (small cell neuroendocrine carcinoma with urothelial or another carcinoma), 8045/3.** The ICCR prints no code for mixed neuroendocrine neoplasms. ICD-O-3.2 names mixed small cell carcinoma at 8045/3; proposed pending the registrar. No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Large cell neuroendocrine carcinoma, 8013/3.** No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Well differentiated neuroendocrine tumour, 8240/3.** No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Paraganglioma, 8693/3.** ICCC-2017 places 8693/3 at the bladder in IVb. The ICCR notes it is not an epithelial tumour.
- **Rhabdomyosarcoma (embryonal including botryoid, alveolar, NOS), 8910/3.** ICCC-2017 places 8900-8920 at every site in IXa. Pfister 2022 names rhabdomyosarcoma the commonest soft-tissue sarcoma of childhood but does not name the urinary or genital sites. Liu 2025 names bladder rhabdomyosarcoma among the paediatric malignancies that present with haematuria.
- **Inflammatory myofibroblastic tumour, 8825/1.** Behaviour /1 in ICD-O-3.2, so not registrable in any group. A report that calls the tumour malignant codes 8825/3 Myofibroblastic sarcoma, ICCC-2017 IXb1 (Rule F).
- **Nephroblastoma at the renal pelvis or ureter, 8960/3.** ICCC-2017 places 8960/3 at every site in VIa1.
- **Renal cell carcinoma with MiT translocation, 8311/3.** ICCC-2017 places 8311/3 at every site in VIb, so a renal pelvis tumour of this type is Group 6.
- **Yolk sac tumour and other extragonadal germ cell tumours, 9071/3.** ICCC-2017 places 9071/3 at these sites in Xb4. A urothelial carcinoma with trophoblastic differentiation stays 8120/3.
- **Acinar adenocarcinoma (including pleomorphic giant cell and prostatic intraepithelial neoplasia-like subtypes), 8140/3.** More than 95% of prostate cancers. No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Signet ring cell-like acinar adenocarcinoma, 8490/3.** No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Sarcomatoid acinar adenocarcinoma, 8572/3.** No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Ductal adenocarcinoma (prostate), 8500/3.** Rule H: ICD-O attaches breast to infiltrating duct carcinoma but lists prostate among its other sites, so the site stays C61.9. No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Treatment-related neuroendocrine prostatic carcinoma (adenocarcinoma with neuroendocrine differentiation), 8574/3.** Netto 2022 and ICCR Prostate (with the July 2024 corrigenda) label 8574/3 differently. No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Adenosquamous carcinoma (prostate), 8560/3.** No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Squamous cell carcinoma (prostate), 8070/3.** No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Adenoid cystic (basal cell) carcinoma of the prostate, 8147/3.** Rule H: ICD-O attaches skin to basal cell carcinoma but lists prostate among its other sites; ICD-O-3.2 prints basal cell carcinoma of prostate at 8147/3, not 8090/3. No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Urothelial carcinoma arising in the prostate, 8120/3.** Rare; reported with the urothelial dataset. A bladder carcinoma that spreads into the prostate is recorded at the bladder. No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Cystadenoma (prostate), 8440/0.** Benign. Every /3 term at 8440 is [obs].
- **Prostatic intraepithelial neoplasia, high grade, 8148/2.** Behaviour /2; 8148 has no /3 term.
- **Intraductal carcinoma of the prostate (with no invasive carcinoma), 8500/2.** Behaviour /2. Isolated intraductal carcinoma without invasive cancer is rare; with invasive carcinoma the invasive code applies.
- **Stromal tumour of uncertain malignant potential, 8935/1.** Behaviour /1.
- **Stromal sarcoma (prostate), 8935/3.** ICCC-2017 places 8935/3 in XIIa4.
- **Squamous cell carcinoma, HPV-associated, 8085/3.** p16 immunohistochemistry is the surrogate for high-risk HPV. No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Basaloid squamous cell carcinoma, 8083/3.** HPV-associated subtype with its own WHO code, numerically lower than 8085 (registrar question on Rule K). No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Warty carcinoma, 8054/3.** HPV-associated subtype. Not offered by REDCap (currency check section 6). No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Clear cell squamous cell carcinoma, 8084/3.** No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Lymphoepithelial carcinoma (penis), 8082/3.** No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Squamous cell carcinoma, HPV-independent, 8086/3.** Includes pseudohyperplastic and pseudoglandular patterns. Not offered by REDCap (currency check section 6). No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Squamous cell carcinoma, usual type, 8070/3.** ICCR prints the usual type under HPV-independent at 8086/3; ICD-O-3.2 prints the term as a synonym at 8070/3. The tree asks HPV or p16 status: HPV-independent or p16 negative records 8086/3; no result records 8070/3 (registrar question). No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Verrucous carcinoma, including carcinoma cuniculatum (penis), 8051/3.** No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Papillary squamous cell carcinoma, 8052/3.** No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Sarcomatoid squamous cell carcinoma, 8074/3.** No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Squamous cell carcinoma, NOS (p16 not available), 8070/3.** The ICCR designates SCC-NOS when morphology does not settle a subtype and p16 is not available or not performed. No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Adenosquamous carcinoma (penis), 8560/3.** No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Mucoepidermoid carcinoma (penis), 8430/3.** No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Paget disease, extramammary (penis), 8542/3.** No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **Medullary carcinoma (emerging entity, penis), 8510/3.** The ICCR lists it as an emerging entity outside the WHO table. No source in this part reports it in a patient aged 0 to 18; Pfister 2022 Table 3 lists only kidney and testis tumours under renal and male genital tumours.
- **High grade squamous intraepithelial lesion (penile intraepithelial neoplasia, HPV-associated), 8077/2.** Behaviour /2; 8077 has no /3 term.
- **Differentiated penile intraepithelial neoplasia, 8071/2.** Behaviour /2.
- **Carcinoma, no type named, 8010/3.** The short tree's fallback on every histology screen: a report that states carcinoma with no type. Rule F gives the malignant behaviour.

Node answers with no entity row are generic ICD-O-3.2 entries that no file in this part names at these sites: 8246/3 Neuroendocrine carcinoma, NOS (urinary picker); 8041/3 at the prostate; 8070/2 Squamous cell carcinoma in situ, NOS (penis exclusion); 9050/3 Mesothelioma, malignant (tunica vaginalis referral, ICCC-2017 XIIa5); and the generic answers on gu_male_genital_histology. The ICCC-2017 XIf8 range holds 164 codes with a current /3 term; the pickers here list only the entities the WHO urinary, prostate and penile tables print, plus these generic entries.

## 3 The pathway

Node prefix `gu_`. The site screen opens the part; the evidence gate follows; `gu_histology_by_site` is the engine's site-keyed dispatch (bladder, urachus, renal pelvis, ureter, urethra and urinary NOS to `gu_urinary_histology`; prostate to `gu_prostate_histology`; penis C60.0 to C60.8 to `gu_penis_histology`; epididymis, spermatic cord and other male genital organs to `gu_male_genital_histology`). Targets written "controller binds the node id" belong to other parts' trees.

A deposit answer is `refer` with `refer_group` null and `recapture_site` true, as the task specifies. The checker reports these four answers as `bad_refer` because it expects a group number; the encoding matches the other parts.

### `gu_site` (site_resolution)

**Question:** Which organ does the report name as the site of the tumour?

**Hint:** Choose the organ where the tumour began. If one tumour spans two parts of the bladder, two urinary organs or two male genital organs, and the report does not say where it began, choose the answer for two parts or two organs. A report that names only the tissue around an organ, such as perivesical, periprostatic or periurethral tissue, does not name that organ.

| Answer | Outcome | Records | Basis | Reason | Recognition aid | Source |
|---|---|---|---|---|---|---|
| Bladder: trigone, dome, lateral wall, anterior wall, posterior wall, bladder neck or ureteric orifice | go | next: `gu_document_inventory` |  | Site recorded as the part of the bladder the report names (C67.0 to C67.6). |  |  |
| Urachus, or a urachal remnant at the bladder dome | go | next: `gu_document_inventory` |  | Site recorded as urachus (C67.7). |  | ICCR Bladder 2025, PDF p. 9 ("diagnosis of urachal carcinoma include location in the bladder dome or anterior wall") |
| Bladder, with no part named, or a tumour spanning two parts of the bladder | go | next: `gu_document_inventory` |  | Site recorded as bladder, NOS (C67.9), or overlapping lesion of bladder (C67.8). |  | ICD-O-3.1 rules, PDF p. 5 ("tumor overlaps the boundaries of two or more categories or subcategories") |
| Renal pelvis or renal calyx, including a renal pelvis tumour that invades the kidney | go | next: `gu_document_inventory` |  | Site recorded as renal pelvis (C65.9). |  | ICCR Renal Pelvis 2025, PDF p. 11 ("Invasion of the renal parenchyma is included in the definition of pT3 disease.") |
| Ureter | go | next: `gu_document_inventory` |  | Site recorded as ureter (C66.9). |  |  |
| Urethra | go | next: `gu_document_inventory` |  | Site recorded as urethra (C68.0). |  |  |
| Paraurethral gland | go | next: `gu_document_inventory` |  | Site recorded as paraurethral gland (C68.1). |  |  |
| Two or more urinary organs with no organ of origin stated, or urinary system with no organ named | go | next: `gu_document_inventory` |  | Site recorded as overlapping lesion of urinary organs (C68.8), or urinary system, NOS (C68.9). |  | ICD-O-3.1 rules, PDF p. 5 ("C68.8 Overlapping lesion of urinary organs") |
| Kidney (renal parenchyma) | refer | Group 6 |  | A carcinoma, nephroblastoma or renal cell carcinoma of the kidney is recorded in Group 6, renal tumours. |  |  |
| Prostate | go | next: `gu_document_inventory` |  | Site recorded as prostate (C61.9). |  |  |
| Penis: foreskin (prepuce), glans or body (shaft), or a tumour spanning two of these | go | next: `gu_document_inventory` |  | Site recorded as prepuce (C60.0), glans penis (C60.1), body of penis (C60.2), or overlapping lesion of penis (C60.8). |  | ICCR Penis 2024, PDF p. 1 ("Glans penis Coronal sulcus Foreskin") |
| Penis, with no part named | go | next: `skin carcinoma tree entry, XIe (controller binds the node id)` |  | Site recorded as penis, NOS (C60.9). The skin carcinoma questions follow. |  |  |
| Scrotum | go | next: `skin carcinoma tree entry, XIe (controller binds the node id)` |  | Site recorded as scrotum (C63.2). The skin carcinoma questions follow. |  |  |
| Testis | refer | Group 10 |  | A tumour of the testis is recorded in Group 10, germ cell, trophoblastic and gonadal tumours. |  |  |
| Epididymis, spermatic cord, seminal vesicle, tunica vaginalis or another named male genital organ | go | next: `gu_document_inventory` |  | Site recorded as epididymis (C63.0), spermatic cord (C63.1) or other specified male genital organ (C63.7). |  |  |
| Two or more male genital organs with no organ of origin stated, or male genital organ with no organ named | go | next: `gu_document_inventory` |  | Site recorded as overlapping lesion of male genital organs (C63.8), or male genital organ, NOS (C63.9). |  | ICD-O-3.1 rules, PDF p. 5 ("C63.8 Overlapping lesion of male genital organs") |
| A region such as the pelvis or groin, with no organ named | go | next: `general carcinoma tree site screen (controller binds the node id)` |  | A region names no organ. The site follows the tissue the tumour type implies, or an ill-defined site. |  | ICD-O-3.1 rules, PDF p. 3 ("If the diagnosis does not specify the tissue of origin") |

### `gu_document_inventory` (document_inventory)

**Question:** What is in the file for this tumour?

**Hint:** Choose the strongest evidence the file holds. A report that calls the tumour possible, probable or suspected does not register it. A raised prostate-specific antigen does not register a tumour.

| Answer | Outcome | Records | Basis | Reason | Recognition aid | Source |
|---|---|---|---|---|---|---|
| A referral letter or clinical note that states a malignant tumour, with no imaging report and no tissue report | code | 8000/3 | 1 | Recorded as Neoplasm, malignant (8000/3). Basis of diagnosis: clinical. |  |  |
| An imaging report that states a malignant tumour, with no tissue report | code | 8000/3 | 2 | Recorded as Neoplasm, malignant (8000/3). Basis of diagnosis: imaging. |  |  |
| An imaging report that shows the tumour, a raised chromogranin A result, and a clinical note that names a neuroendocrine tumour, with no tissue report | code | 8240/3 | 4 | Recorded as Neuroendocrine tumor, NOS (8240/3). Basis of diagnosis: tumour marker. |  | ICCR Bladder 2025, PDF p. 11 ("Well differentiated neuroendocrine tumour 8240/3") |
| A raised prostate-specific antigen (PSA) result with no imaging that shows a tumour and no tissue report | not_registrable | not registered |  | A tumour marker with no imaging that shows the tumour does not register a tumour. |  | ICCR Prostate 2024, PDF p. 5 ("Pre-biopsy serum PSA is a key parameter in some nomograms") |
| A note or report that calls the tumour possible, probable or suspected | not_registrable | not registered |  | A possible, probable or suspected tumour is not registered until a report states it. |  |  |
| A cytology report (urine, bladder washing, brushing or fine needle aspiration) | go | next: `gu_cytology` | 5 |  |  |  |
| A histology report on a biopsy, transurethral resection or resection, with or without immunohistochemistry or gene reports | go | next: `gu_histology_by_site` | 7 |  |  |  |

### `gu_cytology` (morphology_only)

**Question:** What does the cytology report call the tumour?

**Hint:** Urine cytology cannot tell an invasive urothelial carcinoma from urothelial carcinoma in situ, and cannot separate the low-grade papillary lesions from each other. A later histology report replaces this answer.

| Answer | Outcome | Records | Basis | Reason | Recognition aid | Source |
|---|---|---|---|---|---|---|
| Positive for high-grade urothelial carcinoma (urine or bladder washing) | code | 8120/3 | 5 | Recorded as Transitional cell carcinoma, NOS (8120/3). Basis of diagnosis: cytology. |  | Netto 2022, PDF p. 9 ("Positive for high-grade urothelial Ca (HGUC)"); Netto 2022, PDF p. 9 ("staging cannot be achieved on cytology") |
| Another named tumour type, such as squamous cell carcinoma, adenocarcinoma or small cell carcinoma | go | next: `gu_histology_by_site` | 5 | The next screen records the named type. Basis of diagnosis: cytology. |  |  |
| Carcinoma, with no type named | code | 8010/3 | 5 | Recorded as Carcinoma, NOS (8010/3). Basis of diagnosis: cytology. |  |  |
| Malignant, with no tumour type named | code | 8000/3 | 5 | Recorded as Neoplasm, malignant (8000/3). Basis of diagnosis: cytology. |  |  |
| Lymphoma | refer | Group 2 |  | Lymphoma is recorded in Group 2, lymphomas and reticuloendothelial neoplasms. |  |  |
| Suspicious for high-grade urothelial carcinoma, atypical urothelial cells, low-grade urothelial neoplasm, negative, or non-diagnostic | not_registrable | not registered |  | A cytology report that does not state malignancy does not register the tumour. |  | Netto 2022, PDF p. 9 ("Suspicious for high-grade urothelial Ca (SHGUC)"); Netto 2022, PDF p. 9 ("Atypical urothelial cells (AUC)"); Netto 2022, PDF p. 9 ("Low-grade urothelial neoplasm (LGUN)") |

### `gu_urinary_histology` (morphology_only)

**Question:** What does the histology report call the tumour?

**Hint:** When the report gives two tumour types for one tumour and no answer covers both, choose the answer with the higher code. A tumour with any urothelial component, including urothelial carcinoma in situ, is a urothelial carcinoma, except a neuroendocrine carcinoma.

| Answer | Outcome | Records | Basis | Reason | Recognition aid | Source |
|---|---|---|---|---|---|---|
| Urothelial (transitional cell) carcinoma with invasion, including conventional, nested, large nested, tubular and microcystic urothelial carcinoma, and papillary urothelial carcinoma with invasion | code | 8120/3 | 7 | Recorded as Transitional cell carcinoma, NOS (8120/3). | The report states invasion of the lamina propria (subepithelial connective tissue) or deeper, pT1 or higher. | Netto 2022, PDF p. 7 ("8120/3 Invasive urothelial carcinoma"); ICCR Bladder 2025, PDF p. 4 ("Tumour invades subepithelial connective tissue"); Liu 2025, PMC section 8 ("often confined to the mucosal layer (Ta) with rare infiltration into deeper layers"); Liu 2025, PMC section 8 ("childhood bladder urothelial carcinoma is typically low-grade") |
| Another carcinoma the report names, such as micropapillary, plasmacytoid or sarcomatoid urothelial carcinoma, squamous cell carcinoma, adenocarcinoma, urachal carcinoma or small cell neuroendocrine carcinoma | go | next: `gu_urinary_picker` |  |  |  | ICCR Bladder 2025, PDF p. 8 ("a tumour is classified as a urothelial carcinoma if there is any identifiable urothelial component") |
| A papilloma, papillary urothelial neoplasm of low malignant potential, non-invasive papillary urothelial carcinoma, urothelial carcinoma in situ, an adenoma, dysplasia or another non-invasive lesion | go | next: `gu_not_malignant_urinary` |  |  |  |  |
| Carcinoma, with no type named | code | 8010/3 | 7 | Recorded as Carcinoma, NOS (8010/3). |  |  |
| Rhabdomyosarcoma (embryonal, botryoid or alveolar), malignant rhabdoid tumour, or another sarcoma | refer | Group 9 |  | A sarcoma is recorded in Group 9, soft-tissue and other extraosseous sarcomas. |  | Pfister 2022, PDF p. 6 ("with rhabdomyosarcomas (RMS) being the most common"); Liu 2025, PMC section 8 ("other pediatric malignancies, including Wilms tumor and bladder rhabdomyosarcoma") |
| Inflammatory myofibroblastic tumour | exclude | 8825/1 |  | Not registered: Myofibroblastic tumor, NOS (8825/1) is of uncertain behaviour. A report that calls the tumour malignant, or names myofibroblastic sarcoma, is a sarcoma: choose the sarcoma answer. |  | ICD-O-3.1 rules, PDF p. 2 ("If the pathologist states that the behavior differs from the usual behavior") |
| Paraganglioma | refer | Group 4 |  | Extra-adrenal paraganglioma, NOS (8693/3) is recorded in Group 4, neuroblastoma and other peripheral nervous cell tumours. |  | ICCR Bladder 2025, PDF p. 11 ("Paraganglioma is not an epithelial derived tumour.") |
| Nephroblastoma (Wilms tumour), or renal cell carcinoma such as translocation renal cell carcinoma | refer | Group 6 |  | Nephroblastoma and these renal cell carcinomas are recorded in Group 6, renal tumours, wherever they arise. |  | Pfister 2022, PDF p. 12 ("Renal cell carcinoma with MIT translocations") |
| Yolk sac tumour, teratoma, choriocarcinoma or another germ cell tumour | refer | Group 10 |  | A germ cell tumour is recorded in Group 10, germ cell, trophoblastic and gonadal tumours. A urothelial carcinoma with trophoblastic differentiation is a carcinoma: choose the carcinoma answer. |  | Netto 2022, PDF p. 7 ("8120/3 Urothelial carcinoma with trophoblastic differentiation") |
| Lymphoma | refer | Group 2 |  | Lymphoma is recorded in Group 2, lymphomas and reticuloendothelial neoplasms. |  |  |
| Melanoma | go | next: `melanoma tree entry (controller binds the node id)` |  | Melanoma at any site is recorded through the melanoma questions. |  |  |
| A deposit (metastasis) or direct spread of a tumour that began elsewhere, such as a carcinoma of the prostate, cervix or colon | refer | re-asks the primary site |  | A deposit or direct spread is recorded at the site where the tumour began. The next screen asks that site. |  | ICCR Bladder 2025, PDF p. 6 ("Most cases of secondary involvement of the urinary bladder represent direct extension") |

### `gu_not_malignant_urinary` (morphology_only)

**Question:** Which lesion does the report name?

**Hint:** A non-invasive papillary carcinoma is pTa and carcinoma in situ is pTis. If the report states invasion of the lamina propria (subepithelial connective tissue) or deeper, pT1 or higher, go back and choose the carcinoma answer.

| Answer | Outcome | Records | Basis | Reason | Recognition aid | Source |
|---|---|---|---|---|---|---|
| Urothelial papilloma | exclude | 8120/0 |  | Not registered: Urothelial papilloma, NOS (8120/0) is benign. |  | Netto 2022, PDF p. 7 ("8120/0 Urothelial papilloma"); Liu 2025, PMC section 8 ("the two most common types of bladder neoplasms in children, UP and PUNLMP"); Liu 2025, PMC section 7 ("comprised 17 patients, including 11 children diagnosed with UP") |
| Papillary urothelial neoplasm of low malignant potential (PUNLMP), including the inverted form | exclude | 8130/1 |  | Not registered: Papillary urothelial neoplasm of low malignant potential (8130/1) is of uncertain behaviour. | The report places the papillary tumour below low-grade carcinoma; it does not invade or metastasise. | ICCR Bladder 2025, PDF p. 12 ("which will not invade or metastasise"); Liu 2025, PMC section 8 ("the two most common types of bladder neoplasms in children, UP and PUNLMP"); Liu 2025, PMC section 7 ("The study focused on six male children with PUNLMP") |
| Non-invasive papillary urothelial carcinoma, low grade or high grade (pTa), including an inverted growth pattern | exclude | 8130/2 |  | Not registered: Papillary urothelial carcinoma, non-invasive (8130/2) is in situ. |  | Netto 2022, PDF p. 7 ("8130/2 Noninvasive papillary urothelial carcinoma, low grade"); ICCR Bladder 2025, PDF p. 4 ("Non-invasive papillary carcinoma"); Liu 2025, PMC section 8 ("The majority of urothelial bladder tumors in children are papillary urothelial neoplasm"); Liu 2025, PMC section 8 ("(PUNLMP) and low-grade urothelial carcinomas, often confined to the mucosal layer (Ta)") |
| Inverted urothelial papilloma | exclude | 8121/0 |  | Not registered: Urothelial papilloma, inverted (8121/0; ICD-O-3.2 preferred term Sinonasal papilloma, exophytic) is benign. |  | Netto 2022, PDF p. 7 ("8121/0 Urothelial papilloma, inverted") |
| Urothelial carcinoma in situ (flat, pTis) | exclude | 8120/2 |  | Not registered: Urothelial carcinoma in situ (8120/2) is in situ. |  | Netto 2022, PDF p. 7 ("8120/2 Urothelial carcinoma in situ") |
| Urothelial dysplasia, with no carcinoma | not_registrable | not registered |  | Dysplasia with no carcinoma is not registered. |  | ICCR Bladder 2025, PDF p. 10 (table image: "Dysplasia (no code printed)") |
| Squamous papilloma | exclude | 8052/0 |  | Not registered: Squamous cell papilloma, NOS (8052/0) is benign. |  | Netto 2022, PDF p. 7 ("8052/0 Squamous papilloma") |
| Villous adenoma | exclude | 8261/0 |  | Not registered: Villous adenoma, NOS (8261/0) is benign. |  | Netto 2022, PDF p. 7 ("8261/0 Villous adenoma") |
| Tubular adenoma | exclude | 8211/0 |  | Not registered: Tubular adenoma, NOS (8211/0) is benign. |  | Netto 2022, PDF p. 7 ("8211/0 Tubular adenoma") |
| Tubulovillous adenoma | exclude | 8263/0 |  | Not registered: Tubulovillous adenoma, NOS (8263/0) is benign. |  | Netto 2022, PDF p. 7 ("8263/0 Tubulovillous adenoma") |
| Adenocarcinoma in situ | exclude | 8140/2 |  | Not registered: Adenocarcinoma in situ, NOS (8140/2) is in situ. |  | Netto 2022, PDF p. 7 ("8140/2 Adenocarcinoma in situ") |
| Mucinous cystic tumour of low malignant potential (urachus) | exclude | 8472/1 |  | Not registered: Mucinous cystic tumor of borderline malignancy (8472/1) is of uncertain behaviour. |  | ICCR Bladder 2025, PDF p. 9 ("mucinous cystic tumour of low malignant potential") |

### `gu_urinary_picker` (morphology_only)

**Question:** Which carcinoma does the histology report name?

**Hint:** Type part of the report's term to filter the list. If the term is not found, search its words in a different order. When the report gives two tumour types for one tumour and no answer covers both, choose the answer with the higher code. Transitional cell epidermoid carcinoma is urothelial carcinoma (8120/3).

| Answer | Outcome | Records | Basis | Reason | Recognition aid | Source |
|---|---|---|---|---|---|---|
| Plasmacytoid urothelial carcinoma | code | 8120/3 | 7 | Recorded as Transitional cell carcinoma, NOS (8120/3). |  | Netto 2022, PDF p. 7 ("8122/3 Plasmacytoid urothelial"); ICCR Bladder 2025, PDF p. 10 (table image: "Plasmacytoid (no code printed)") |
| Urothelial carcinoma with squamous, glandular or trophoblastic differentiation | code | 8120/3 | 7 | Recorded as Transitional cell carcinoma, NOS (8120/3). |  | Netto 2022, PDF p. 7 ("8120/3 Urothelial carcinoma with glandular differentiation") |
| Lipid-rich urothelial carcinoma, or clear cell (glycogen-rich) urothelial carcinoma | code | 8120/3 | 7 | Recorded as Transitional cell carcinoma, NOS (8120/3). |  | Netto 2022, PDF p. 7 ("8120/3 Lipid-rich urothelial carcinoma") |
| Micropapillary urothelial carcinoma | code | 8131/3 | 7 | Recorded as Urothelial carcinoma, micropapillary (8131/3). |  | ICCR Bladder 2025, PDF p. 10 ("Micropapillary 8131/3") |
| Sarcomatoid (spindle cell) urothelial carcinoma | code | 8122/3 | 7 | Recorded as Urothelial carcinoma, sarcomatoid (8122/3). |  | ICCR Bladder 2025, PDF p. 10 ("Sarcomatoid 8122/3") |
| Lymphoepithelioma-like urothelial carcinoma | code | 8082/3 | 7 | Recorded as Lymphoepithelial carcinoma (8082/3). |  | ICCR Bladder 2025, PDF p. 10 ("Lymphoepithelioma-like 8082/3") |
| Giant cell urothelial carcinoma | code | 8031/3 | 7 | Recorded as Giant cell carcinoma (8031/3). |  | Netto 2022, PDF p. 7 ("8031/3 Giant cell urothelial carcinoma") |
| Poorly differentiated urothelial carcinoma | code | 8020/3 | 7 | Recorded as Carcinoma, undifferentiated, NOS (8020/3). |  | Netto 2022, PDF p. 7 ("8020/3 Poorly differentiated urothelial carcinoma") |
| Squamous cell carcinoma, pure | code | 8070/3 | 7 | Recorded as Squamous cell carcinoma, NOS (8070/3). | The tumour is entirely squamous, with no urothelial component and no urothelial carcinoma in situ. | ICCR Bladder 2025, PDF p. 11 ("Pure squamous cell carcinoma 8070/3") |
| Verrucous carcinoma | code | 8051/3 | 7 | Recorded as Verrucous carcinoma, NOS (8051/3). |  | ICCR Bladder 2025, PDF p. 11 ("Verrucous carcinoma 8051/3") |
| Adenocarcinoma, with no type named | code | 8140/3 | 7 | Recorded as Adenocarcinoma, NOS (8140/3). |  | Netto 2022, PDF p. 7 ("8140/3 Adenocarcinoma, NOS") |
| Enteric (intestinal-type) adenocarcinoma | code | 8144/3 | 7 | Recorded as Adenocarcinoma, intestinal type (8144/3). |  | ICCR Bladder 2025, PDF p. 11 ("Enteric 8144/3") |
| Mucinous (colloid) adenocarcinoma | code | 8480/3 | 7 | Recorded as Mucinous adenocarcinoma (8480/3). |  | ICCR Bladder 2025, PDF p. 11 ("Mucinous 8480/3") |
| Mixed adenocarcinoma | code | 8140/3 | 7 | Recorded as Adenocarcinoma, NOS (8140/3). |  | ICCR Bladder 2025, PDF p. 11 ("Mixed 8140/3") |
| Signet ring cell adenocarcinoma | code | 8490/3 | 7 | Recorded as Signet ring cell carcinoma (8490/3). |  | Netto 2022, PDF p. 7 ("8490/3 Signet ring cell adenocarcinoma") |
| Urachal carcinoma, with no subtype named | code | 8010/3 | 7 | Recorded as Carcinoma, NOS (8010/3). A named subtype, such as mucinous adenocarcinoma, is chosen instead. | The report places the tumour at the bladder dome or anterior wall, centred in the bladder wall or perivesical tissue. | Netto 2022, PDF p. 7 ("8010/3 Urachal carcinoma"); ICCR Bladder 2025, PDF p. 9 ("If a diagnosis of urachal carcinoma is rendered the subtype must be specified.") |
| Carcinoma of Littre, Skene or Cowper glands (urethral accessory gland carcinoma) | code | 8140/3 | 7 | Recorded as Adenocarcinoma, NOS (8140/3). |  | Netto 2022, PDF p. 7 ("8140/3 Carcinoma of Skene glands") |
| Clear cell adenocarcinoma (Mullerian type) | code | 8310/3 | 7 | Recorded as Clear cell adenocarcinoma, NOS (8310/3). |  | ICCR Bladder 2025, PDF p. 11 ("Clear cell adenocarcinoma 8310/3") |
| Endometrioid carcinoma | code | 8380/3 | 7 | Recorded as Endometrioid adenocarcinoma, NOS (8380/3). |  | ICCR Bladder 2025, PDF p. 11 ("Endometrioid carcinoma 8380/3") |
| Small cell neuroendocrine carcinoma | code | 8041/3 | 7 | Recorded as Small cell carcinoma, NOS (8041/3). |  | ICCR Bladder 2025, PDF p. 11 ("Small cell neuroendocrine carcinoma 8041/3") |
| Small cell neuroendocrine carcinoma mixed with urothelial carcinoma or another carcinoma | code | 8045/3 | 7 | Recorded as Combined small cell carcinoma (8045/3). |  | ICCR Bladder 2025, PDF p. 8 ("cases with a small cell neuroendocrine carcinoma component irrespective of the amount are managed") |
| Large cell neuroendocrine carcinoma | code | 8013/3 | 7 | Recorded as Large cell neuroendocrine carcinoma (8013/3). |  | ICCR Bladder 2025, PDF p. 11 ("Large cell neuroendocrine carcinoma 8013/3") |
| Neuroendocrine carcinoma, with no type named | code | 8246/3 | 7 | Recorded as Neuroendocrine carcinoma, NOS (8246/3). |  |  |
| Well differentiated neuroendocrine tumour, or carcinoid | code | 8240/3 | 7 | Recorded as Neuroendocrine tumor, NOS (8240/3). |  | ICCR Bladder 2025, PDF p. 11 ("Well differentiated neuroendocrine tumour 8240/3") |

### `gu_prostate_histology` (morphology_only)

**Question:** What does the histology report call the tumour?

**Hint:** When the report gives two tumour types for one tumour and no answer covers both, choose the answer with the higher code.

| Answer | Outcome | Records | Basis | Reason | Recognition aid | Source |
|---|---|---|---|---|---|---|
| Adenocarcinoma of the prostate or another carcinoma the report names, such as acinar adenocarcinoma, ductal adenocarcinoma, squamous cell carcinoma, basal cell carcinoma or urothelial carcinoma | go | next: `gu_prostate_picker` |  |  |  |  |
| High-grade prostatic intraepithelial neoplasia, intraductal carcinoma with no invasive carcinoma, cystadenoma, or a stromal tumour of uncertain malignant potential | go | next: `gu_not_malignant_prostate` |  |  |  |  |
| Carcinoma, with no type named | code | 8010/3 | 7 | Recorded as Carcinoma, NOS (8010/3). |  |  |
| Stromal sarcoma of the prostate | refer | Group 12 |  | Stromal sarcoma, NOS (8935/3) is recorded in Group 12, other and unspecified malignant tumours. |  | ICCR Prostate 2024, PDF p. 7 ("Stromal sarcoma 8935/3") |
| Rhabdomyosarcoma (embryonal, botryoid or alveolar), malignant rhabdoid tumour, or another sarcoma | refer | Group 9 |  | A sarcoma is recorded in Group 9, soft-tissue and other extraosseous sarcomas. |  | Pfister 2022, PDF p. 6 ("with rhabdomyosarcomas (RMS) being the most common") |
| Yolk sac tumour, teratoma, choriocarcinoma or another germ cell tumour | refer | Group 10 |  | A germ cell tumour is recorded in Group 10, germ cell, trophoblastic and gonadal tumours. A urothelial carcinoma with trophoblastic differentiation is a carcinoma: choose the carcinoma answer. |  | Netto 2022, PDF p. 7 ("8120/3 Urothelial carcinoma with trophoblastic differentiation") |
| Lymphoma | refer | Group 2 |  | Lymphoma is recorded in Group 2, lymphomas and reticuloendothelial neoplasms. |  |  |
| A deposit (metastasis) or direct spread of a tumour that began elsewhere, such as a urothelial carcinoma of the bladder that extends into the prostate | refer | re-asks the primary site |  | A deposit or direct spread is recorded at the site where the tumour began. The next screen asks that site. |  | ICCR Bladder 2025, PDF p. 6 ("Most cases of secondary involvement of the urinary bladder represent direct extension") |

### `gu_prostate_picker` (morphology_only)

**Question:** Which carcinoma does the histology report name?

**Hint:** Type part of the report's term to filter the list. If the term is not found, search its words in a different order. When the report gives two tumour types for one tumour and no answer covers both, choose the answer with the higher code. Ductal adenocarcinoma and basal cell carcinoma of the prostate keep the prostate as the site.

| Answer | Outcome | Records | Basis | Reason | Recognition aid | Source |
|---|---|---|---|---|---|---|
| Acinar adenocarcinoma, including pleomorphic giant cell and prostatic intraepithelial neoplasia-like carcinoma, or adenocarcinoma of the prostate with no type named | code | 8140/3 | 7 | Recorded as Adenocarcinoma, NOS (8140/3). |  | ICCR Prostate 2024, PDF p. 7 ("The vast majority (>95%) of prostate cancers are acinar adenocarcinomas.") |
| Signet ring cell-like acinar adenocarcinoma | code | 8490/3 | 7 | Recorded as Signet ring cell carcinoma (8490/3). |  | Netto 2022, PDF p. 2 ("8490/3 Signet ring cell-like acinar adenocarcinoma") |
| Sarcomatoid acinar adenocarcinoma, or sarcomatoid carcinoma of the prostate | code | 8572/3 | 7 | Recorded as Adenocarcinoma with spindle cell metaplasia (8572/3). |  | ICCR Prostate 2024, PDF p. 7 ("Sarcomatoid acinar adenocarcinoma 8572/3") |
| Ductal adenocarcinoma | code | 8500/3 | 7 | Recorded as Infiltrating duct carcinoma, NOS (8500/3). The site stays prostate (C61.9). |  | ICCR Prostate 2024, PDF p. 7 ("Ductal adenocarcinoma 8500/3"); ICD-O-3.1 rules, PDF p. 10 ("should be disregarded if the tumor is known to arise at another site") |
| Adenocarcinoma with neuroendocrine differentiation, or treatment-related neuroendocrine prostatic carcinoma | code | 8574/3 | 7 | Recorded as Adenocarcinoma with neuroendocrine differentiation (8574/3). |  | ICCR Prostate 2024, PDF p. 7 ("Adenocarcinoma with neuroendocrine differentiation 8574/3") |
| Small cell neuroendocrine carcinoma | code | 8041/3 | 7 | Recorded as Small cell carcinoma, NOS (8041/3). |  |  |
| Adenosquamous carcinoma | code | 8560/3 | 7 | Recorded as Adenosquamous carcinoma (8560/3). |  | Netto 2022, PDF p. 2 ("8560/3 Adenosquamous carcinoma") |
| Squamous cell carcinoma | code | 8070/3 | 7 | Recorded as Squamous cell carcinoma, NOS (8070/3). |  | Netto 2022, PDF p. 2 ("8070/3 Squamous cell carcinoma") |
| Adenoid cystic (basal cell) carcinoma, or basal cell carcinoma of the prostate | code | 8147/3 | 7 | Recorded as Basal cell adenocarcinoma (8147/3), under which ICD-O-3.2 lists basal cell carcinoma of prostate. |  | Netto 2022, PDF p. 2 ("8147/3 Adenoid cystic (basal cell)"); ICD-O-3.1 rules, PDF p. 10 ("C60._ Penis C63.2 Scrotum C61.9 Prostate") |
| Urothelial carcinoma arising in the prostate (prostatic urethra or prostatic ducts) | code | 8120/3 | 7 | Recorded as Transitional cell carcinoma, NOS (8120/3). |  | ICCR Prostate 2024, PDF p. 4 ("urothelial carcinomas arising within the prostate are included in a separate ICCR dataset") |

### `gu_not_malignant_prostate` (morphology_only)

**Question:** Which lesion does the report name?

**Hint:** If the report also names an invasive carcinoma, go back and choose the carcinoma.

| Answer | Outcome | Records | Basis | Reason | Recognition aid | Source |
|---|---|---|---|---|---|---|
| High-grade prostatic intraepithelial neoplasia | exclude | 8148/2 |  | Not registered: Glandular intraepithelial neoplasia, high grade (8148/2) is in situ. |  | Netto 2022, PDF p. 2 ("8148/2 Prostatic intraepithelial neoplasia, high grade") |
| Intraductal carcinoma of the prostate, with no invasive carcinoma | exclude | 8500/2 |  | Not registered: Intraductal carcinoma, noninfiltrating, NOS (8500/2) is in situ. |  | Netto 2022, PDF p. 2 ("8500/2 Intraductal carcinoma"); Netto 2022, PDF p. 3 ("is an exceedingly rare finding in biopsies and prostatectomies") |
| Cystadenoma | exclude | 8440/0 |  | Not registered: Cystadenoma, NOS (8440/0) is benign. |  | Netto 2022, PDF p. 2 ("8440/0 Cystadenoma") |
| Stromal tumour of uncertain malignant potential | exclude | 8935/1 |  | Not registered: Stromal tumor, NOS (8935/1) is of uncertain behaviour. |  | Netto 2022, PDF p. 2 ("8935/1 Stromal tumor of uncertain malignant potential") |

### `gu_penis_histology` (morphology_only)

**Question:** What does the histology report call the tumour?

**Hint:** When the report gives two tumour types for one tumour and no answer covers both, choose the answer with the higher code.

| Answer | Outcome | Records | Basis | Reason | Recognition aid | Source |
|---|---|---|---|---|---|---|
| Squamous cell carcinoma of any type, including basaloid, warty, verrucous, papillary or sarcomatoid squamous cell carcinoma | go | next: `gu_penis_scc_subtype` |  |  |  |  |
| Another carcinoma the report names, such as adenosquamous carcinoma, mucoepidermoid carcinoma, extramammary Paget disease or medullary carcinoma | go | next: `gu_penis_picker` |  |  |  |  |
| Carcinoma, with no type named | code | 8010/3 | 7 | Recorded as Carcinoma, NOS (8010/3). |  |  |
| Penile intraepithelial neoplasia, high-grade squamous intraepithelial lesion, differentiated penile intraepithelial neoplasia, or squamous cell carcinoma in situ | go | next: `gu_not_malignant_penis` |  |  |  |  |
| Melanoma | go | next: `melanoma tree entry (controller binds the node id)` |  | Melanoma at any site is recorded through the melanoma questions. |  |  |
| Kaposi sarcoma, rhabdomyosarcoma or another sarcoma | refer | Group 9 |  | A sarcoma is recorded in Group 9, soft-tissue and other extraosseous sarcomas. |  |  |
| Lymphoma | refer | Group 2 |  | Lymphoma is recorded in Group 2, lymphomas and reticuloendothelial neoplasms. |  |  |
| A deposit (metastasis) or direct spread of a tumour that began elsewhere, such as a carcinoma of the bladder or prostate | refer | re-asks the primary site |  | A deposit or direct spread is recorded at the site where the tumour began. The next screen asks that site. |  | ICCR Bladder 2025, PDF p. 6 ("Most cases of secondary involvement of the urinary bladder represent direct extension") |

### `gu_penis_scc_subtype` (histology_subclassification)

**Question:** Which squamous cell carcinoma does the report name?

**Hint:** Choose the subtype the report names. A report that names squamous cell carcinoma with no subtype, or the usual type, goes to the next screen, which asks the human papillomavirus (HPV) status. When the report gives two tumour types for one tumour and no answer covers both, choose the answer with the higher code.

| Answer | Outcome | Records | Basis | Reason | Recognition aid | Source |
|---|---|---|---|---|---|---|
| Basaloid squamous cell carcinoma | code | 8083/3 | 7 | Recorded as Basaloid squamous cell carcinoma (8083/3). |  | ICCR Penis 2024, PDF p. 10 ("Basaloid squamous cell carcinoma 8083/3") |
| Warty (condylomatous) carcinoma | code | 8054/3 | 7 | Recorded as Warty carcinoma (8054/3). |  | ICCR Penis 2024, PDF p. 10 ("Warty carcinoma 8054/3") |
| Clear cell squamous cell carcinoma | code | 8084/3 | 7 | Recorded as Squamous cell carcinoma, clear cell type (8084/3). |  | ICCR Penis 2024, PDF p. 10 ("Clear cell squamous cell carcinoma 8084/3") |
| Lymphoepithelial carcinoma | code | 8082/3 | 7 | Recorded as Lymphoepithelial carcinoma (8082/3). |  | ICCR Penis 2024, PDF p. 10 ("Lymphoepithelial carcinoma 8082/3") |
| Verrucous carcinoma, including carcinoma cuniculatum | code | 8051/3 | 7 | Recorded as Verrucous carcinoma, NOS (8051/3). |  | ICCR Penis 2024, PDF p. 10 ("Verrucous carcinoma (including carcinoma cuniculatum) 8051/3") |
| Papillary squamous cell carcinoma | code | 8052/3 | 7 | Recorded as Papillary squamous cell carcinoma (8052/3). |  | ICCR Penis 2024, PDF p. 10 ("Papillary squamous cell carcinoma 8052/3") |
| Sarcomatoid squamous cell carcinoma | code | 8074/3 | 7 | Recorded as Squamous cell carcinoma, spindle cell (8074/3). |  | ICCR Penis 2024, PDF p. 10 ("Sarcomatoid squamous cell carcinoma 8074/3") |
| Squamous cell carcinoma with no subtype named, usual type, or HPV-associated or HPV-independent squamous cell carcinoma with no subtype named | go | next: `gu_penis_hpv` |  |  |  |  |

### `gu_penis_hpv` (ihc_checklist)

**Question:** What does the report say about human papillomavirus (HPV) or p16?

**Hint:** p16 immunohistochemistry stands in for an HPV test. A report with no HPV status and no p16 result records squamous cell carcinoma, NOS.

| Answer | Outcome | Records | Basis | Reason | Recognition aid | Source |
|---|---|---|---|---|---|---|
| HPV-associated, a positive high-risk HPV test, or p16 positive | code | 8085/3 | 7 | Recorded as Squamous cell carcinoma, HPV positive (8085/3). |  | ICCR Penis 2024, PDF p. 16 ("the p16 protein is upregulated and can be detected in high risk HPV related malignancies") |
| HPV-independent, a negative high-risk HPV test, or p16 negative | code | 8086/3 | 7 | Recorded as Squamous cell carcinoma, HPV negative (8086/3). |  | ICCR Penis 2024, PDF p. 10 ("Squamous cell carcinoma, usual type 8086/3") |
| No HPV status and no p16 result, or p16 not done | code | 8070/3 | 7 | Recorded as Squamous cell carcinoma, NOS (8070/3). |  | ICCR Penis 2024, PDF p. 11 ("p16 is not available or is not performed the tumour should be designated as SCC-NOS") |

### `gu_penis_picker` (morphology_only)

**Question:** Which carcinoma does the histology report name?

**Hint:** Type part of the report's term to filter the list. If the term is not found, search its words in a different order. When the report gives two tumour types for one tumour and no answer covers both, choose the answer with the higher code.

| Answer | Outcome | Records | Basis | Reason | Recognition aid | Source |
|---|---|---|---|---|---|---|
| Adenosquamous carcinoma | code | 8560/3 | 7 | Recorded as Adenosquamous carcinoma (8560/3). |  | ICCR Penis 2024, PDF p. 11 ("Adenosquamous carcinoma 8560/3") |
| Mucoepidermoid carcinoma | code | 8430/3 | 7 | Recorded as Mucoepidermoid carcinoma (8430/3). |  | ICCR Penis 2024, PDF p. 11 ("Mucoepidermoid carcinoma 8430/3") |
| Extramammary Paget disease | code | 8542/3 | 7 | Recorded as Paget disease, extramammary (8542/3). |  | ICCR Penis 2024, PDF p. 11 ("Paget disease, extramammary 8542/3") |
| Medullary carcinoma | code | 8510/3 | 7 | Recorded as Medullary carcinoma, NOS (8510/3). | A poorly differentiated carcinoma in solid sheets of large anaplastic cells, rich in inflammatory cells. | ICCR Penis 2024, PDF p. 11 ("Medullary carcinoma is a poorly differentiated carcinoma that grows in solid sheets") |

### `gu_not_malignant_penis` (morphology_only)

**Question:** Which lesion does the report name?

**Hint:** If the report states invasion, go back and choose the carcinoma.

| Answer | Outcome | Records | Basis | Reason | Recognition aid | Source |
|---|---|---|---|---|---|---|
| High-grade squamous intraepithelial lesion, or HPV-associated penile intraepithelial neoplasia | exclude | 8077/2 |  | Not registered: Squamous intraepithelial neoplasia, high grade (8077/2) is in situ. |  | ICCR Penis 2024, PDF p. 11 ("High grade squamous intraepithelial lesion 8077/2") |
| Differentiated penile intraepithelial neoplasia | exclude | 8071/2 |  | Not registered: Differentiated intraepithelial neoplasia (8071/2) is in situ. |  | ICCR Penis 2024, PDF p. 11 ("Differentiated penile intraepithelial neoplasia 8071/2") |
| Squamous cell carcinoma in situ | exclude | 8070/2 |  | Not registered: Squamous cell carcinoma in situ, NOS (8070/2) is in situ. |  |  |

### `gu_male_genital_histology` (morphology_only)

**Question:** What does the histology report call the tumour?

**Hint:** When the report gives two tumour types for one tumour and no answer covers both, choose the answer with the higher code.

| Answer | Outcome | Records | Basis | Reason | Recognition aid | Source |
|---|---|---|---|---|---|---|
| Adenocarcinoma, with no type named | code | 8140/3 | 7 | Recorded as Adenocarcinoma, NOS (8140/3). |  |  |
| Squamous cell carcinoma | code | 8070/3 | 7 | Recorded as Squamous cell carcinoma, NOS (8070/3). |  |  |
| Carcinoma, with no type named | code | 8010/3 | 7 | Recorded as Carcinoma, NOS (8010/3). |  |  |
| Another carcinoma the report names | go | next: `general carcinoma picker (controller binds the node id)` |  |  |  |  |
| Mesothelioma of the tunica vaginalis | refer | Group 12 |  | Mesothelioma, malignant (9050/3) is recorded in Group 12, other and unspecified malignant tumours. |  |  |
| Rhabdomyosarcoma (embryonal, botryoid or alveolar), malignant rhabdoid tumour, or another sarcoma | refer | Group 9 |  | A sarcoma is recorded in Group 9, soft-tissue and other extraosseous sarcomas. |  | Pfister 2022, PDF p. 6 ("with rhabdomyosarcomas (RMS) being the most common") |
| Yolk sac tumour, teratoma, choriocarcinoma or another germ cell tumour | refer | Group 10 |  | A germ cell tumour is recorded in Group 10, germ cell, trophoblastic and gonadal tumours. A urothelial carcinoma with trophoblastic differentiation is a carcinoma: choose the carcinoma answer. |  | Netto 2022, PDF p. 7 ("8120/3 Urothelial carcinoma with trophoblastic differentiation") |
| Lymphoma | refer | Group 2 |  | Lymphoma is recorded in Group 2, lymphomas and reticuloendothelial neoplasms. |  |  |
| A deposit (metastasis) or direct spread of a tumour that began elsewhere, such as a carcinoma of the prostate or bladder | refer | re-asks the primary site |  | A deposit or direct spread is recorded at the site where the tumour began. The next screen asks that site. |  | ICCR Bladder 2025, PDF p. 6 ("Most cases of secondary involvement of the urinary bladder represent direct extension") |

## 4 Immunohistochemistry rules

One checklist, `gu_penis_hpv`. ICCR Penis 2024 (PDF p. 16) states that p16 is upregulated after high-risk HPV infection and stands in for HPV; Table 1 (PDF p. 10) splits squamous cell carcinoma into HPV-associated 8085/3 and HPV-independent 8086/3; the note on PDF p. 11 designates SCC-NOS when p16 is not available.

| Panel | Positive | Negative | Code | Source |
|---|---|---|---|---|
| `gu_penis_hpv` | p16 (or a positive high-risk HPV test) | — | 8085/3 | ICCR Penis 2024, PDF p. 16 ("the p16 protein is upregulated and can be detected in high risk HPV related malignancies"); ICCR Penis 2024, PDF p. 10 ("Squamous cell carcinoma, HPV-associated 8085/3") |
| `gu_penis_hpv` | — | p16 (or a negative high-risk HPV test) | 8086/3 | ICCR Penis 2024, PDF p. 16 ("The p16 protein is not only a surrogate for HPV expression"); ICCR Penis 2024, PDF p. 10 ("Squamous cell carcinoma, usual type 8086/3") |
| `gu_penis_hpv` | — | — | 8070/3 (fallback) | ICCR Penis 2024, PDF p. 11 ("p16 is not available or is not performed the tumour should be designated as SCC-NOS") |

No checklist is built for the urinary tract. ICCR Bladder 2025 (PDF p. 17) recommends no ancillary study for routine use in urothelial carcinoma, and states (PDF p. 9) that no reliable marker separates pure squamous cell carcinoma or adenocarcinoma from urothelial carcinoma with divergent differentiation, or a urachal adenocarcinoma from a secondary gastrointestinal one. Small cell neuroendocrine carcinoma is defined by morphology; chromogranin A and synaptophysin are its most specific markers (PDF p. 9), so the picker answer names the morphology.

## 5 Registration without tissue

| Evidence on file | Code | Basis | Source |
|---|---|---|---|
| A referral letter or clinical note that states a malignant tumour, no imaging, no tissue | 8000/3 | 1 | Visser 2023 (controller ruling) |
| An imaging report that states a malignant tumour, no tissue | 8000/3 | 2 | Visser 2023 (controller ruling) |
| Imaging that shows the tumour, a raised chromogranin A, and a note naming a neuroendocrine tumour (Visser 2023 Table 4) | 8240/3 | 4 | ICCR Bladder 2025, PDF p. 11 ("Well differentiated neuroendocrine tumour 8240/3") |

ICCC-2017 places 8000/3 at every site in this part in XIIb, so a clinical or imaging registration records a Group 12 case (section 9). A raised prostate-specific antigen with no imaging that shows a tumour is not registrable; with imaging that shows a tumour it records 8000/3 basis 2 like any imaging registration. Urine cytology positive for high-grade urothelial carcinoma records 8120/3 basis 5 (proposed; registrar question 7): Netto 2022 (PDF p. 9) states cytology cannot separate carcinoma in situ from invasive carcinoma.

## 6 Laboratory tests

| Test | Specimen | Role | Source |
|---|---|---|---|
| Serum prostate-specific antigen (PSA) | serum | Clinical information for risk nomograms after radical prostatectomy. It does not register a tumour and does not decide a code; Visser 2023 Table 4 gives it no basis-4 code. | ICCR Prostate 2024, PDF p. 5 ("Pre-biopsy serum PSA is a key parameter in some nomograms") |

No file in this part gives a serum or urine test a diagnostic role at these sites. Chromogranin A appears in ICCR Bladder only as an immunohistochemical marker; the basis-4 answer for a neuroendocrine tumour rests on Visser 2023 Table 4 (data gap 6).

## 7 Rules A to K

| Rule | Applies | How it reaches the clerk |
|---|---|---|
| A | yes | Option on gu_site: 'A region such as the pelvis or groin, with no organ named' sends the clerk to the general carcinoma site screen, because a region names no organ; its reason states that the site follows the tissue the tumour type implies. |
| B | yes | Hint on gu_site: a report naming only perivesical, periprostatic or periurethral tissue does not name that organ. The paraurethral gland, which ICD-O lists, is its own answer (C68.1). |
| C | yes | Options on gu_site: two parts of the bladder take C67.8; two urinary organs C68.8; two male genital organs C63.8; two parts of the penis C60.8. Each reason names the code. |
| D | yes | Referral only: every lymphoma answer refers to Group 2, which applies Rule D. |
| E | no | No leukaemia reaches these screens; lymphoma and leukaemia go to Groups 2 and 1. |
| F | yes | Hints on gu_not_malignant_urinary, gu_not_malignant_prostate and gu_not_malignant_penis: a stated invasion (pT1 or higher) sends the clerk back to the carcinoma answer. The inflammatory myofibroblastic tumour option's reason: a report calling it malignant is a sarcoma (8825/3, Group 9). The urothelial picker hint: a papillary urothelial carcinoma is chosen there only when the report states invasion. |
| G | no | No screen offers a grade: low-grade and high-grade non-invasive papillary carcinoma share 8130/2, invasive urothelial grades share 8120/3, and Gleason grade and penile grade do not change the code. The sixth digit is not built. |
| H | yes | Picker labels and reasons on gu_prostate_picker: ductal adenocarcinoma (8500/3, breast attached in ICD-O) and basal cell carcinoma (8147/3 basal cell carcinoma of prostate, not 8090/3 skin) keep C61.9; the picker hint says so. The deposit option on every histology screen sends a tumour that began elsewhere to its primary site. |
| J | yes | Hint on gu_urinary_picker, gu_prostate_picker and gu_penis_picker: if the term is not found, search its words in a different order. |
| K | yes | Hint on every histology screen and picker: when two terms describe one tumour and no answer covers both, choose the higher code. gu_urinary_picker's hint gives the manual's own example, transitional cell epidermoid carcinoma 8120/3. Registrar questions 2 and 3 ask whether WHO subtype codes lower than 8120 or 8085 stand against Rule K. |

Rule sources: Rule A, ICD-O-3.1 rules PDF p. 3; Rule C, PDF p. 5 (C63.8, C68.8 listed); Rule F, PDF p. 2; Rule H and Table 23 (basal cell carcinoma: C44 with C60, C63.2, C61.9; infiltrating duct carcinoma: C50 with C61.9), PDF p. 10; Rules J and K with the transitional cell epidermoid carcinoma example, PDF p. 11.

## 8 Code currency

| Code | Finding | What the tree does |
|---|---|---|
| 8130/3 | Every /3 term [obs] in ICD-O-3.2 (currency check section 2). The WHO 2022 table (Netto 2022 Table 3; ICCR Bladder Table 1) prints 8130 only at /1 and /2 and codes invasive urothelial carcinoma 8120/3. | not_built. Papillary urothelial carcinoma with invasion records 8120/3; non-invasive records the 8130/2 exclusion. |
| 8122/3 | Netto 2022 Table 3 prints 8122/3 beside plasmacytoid and 8120/3 beside sarcomatoid. ICCR Bladder and ICCR Renal Pelvis, which carry the July 2024 corrigenda, print sarcomatoid 8122/3 and no code for plasmacytoid. ICD-O-3.2 8122/3 is Urothelial carcinoma, sarcomatoid. REDCap labels 8122 Transitional cell carcinoma, spindle cell (a synonym). | Sarcomatoid records 8122/3; plasmacytoid records 8120/3. REDCap relabel to the preferred term goes on the REDCap-side list. |
| 8323/3 | Netto 2022 Table 3 codes mixed adenocarcinoma 8323/3; ICCR Bladder and Renal Pelvis (corrigenda July 2024) code it 8140/3. | Records 8140/3 (latest document); registrar question 4. |
| 8314/3 | ICD-O-3.2 holds Lipid-rich carcinoma at 8314/3 and Glycogen-rich carcinoma at 8315/3; the WHO codes lipid-rich and clear cell (glycogen-rich) urothelial carcinoma 8120/3. | Records 8120/3 per the WHO; registrar question 3 asks whether Rule K's higher code applies. |
| 8086/3 | ICCR Penis prints Squamous cell carcinoma, usual type at 8086/3; ICD-O-3.2 prints that term as a synonym at 8070/3. 8054/3, 8085/3 and 8086/3 are new in ICD-O-3.2 and REDCap does not offer them (currency check section 6). | Usual type goes to the HPV/p16 screen: HPV-independent or p16 negative 8086/3, no result 8070/3 (registrar question 6). 8054, 8085, 8086 go on the REDCap-side list. |
| 8574/3 | Netto 2022 labels 8574/3 Treatment-related neuroendocrine prostatic carcinoma; ICCR Prostate (corrigenda) labels it Adenocarcinoma with neuroendocrine differentiation, the ICD-O-3.2 preferred term. | Reason carries the ICD-O-3.2 preferred term; the option label names both. |
| 8147/3 | WHO label Adenoid cystic (basal cell) carcinoma changed terminology; ICD-O-3.2 preferred term Basal cell adenocarcinoma, with Basal cell carcinoma of prostate as a related term. | Records 8147/3 at the prostate (Rule H). |
| 8121/0 | WHO term Urothelial papilloma, inverted is a related term at 8121/0, whose preferred term is Sinonasal papilloma, exophytic. | Exclusion reason names both terms. |
| 8440/3 | Every /3 term [obs] (currency check section 2). At the prostate the WHO lists only Cystadenoma 8440/0. | not_built; cystadenoma is an exclusion. |
| 8045/3 | ICCR prints no code for mixed neuroendocrine neoplasms. ICD-O-3.2 8045/3 Combined small cell carcinoma has the synonym Mixed small cell carcinoma. | Proposed 8045/3 in gu_urinary_picker; registrar question 5. |
| 8472/1 | The urachal mucinous cystic tumour of low malignant potential is named by the ICCR without a code; ICD-O-3.2 holds Mucinous tumor, NOS, of low malignant potential at 8472/1. | Exclusion at /1; the WHO code is a data gap. |
| 8077/2 | REDCap offers 8077, which has no /3 term (currency check section 5); 8148 likewise. | Both are exclusions (8077/2 penis, 8148/2 prostate). |
| 8131/3 | REDCap label Transitional cell carcinoma, micropapillary; ICD-O-3.2 preferred Urothelial carcinoma, micropapillary. | Reason carries the preferred term; REDCap-side list. |
| 8240/3 | REDCap label Carcinoid tumor, NOS; ICD-O-3.2 preferred Neuroendocrine tumor, NOS (currency check section 4). | Reason carries the preferred term; REDCap-side list. |
| 8010/3 | The REDCap XIf list labels 8010 Epithelial Tumor, NOS; ICD-O-3.2 preferred Carcinoma, NOS (Epithelial tumor, malignant is a synonym). | Reason carries the preferred term; REDCap-side list. |
| 8154/3 | REDCap label Mixed pancreatic endocrine and exocrine tumor, malignant; ICD-O-3.2 preferred Mixed neuroendocrine non-neuroendocrine neoplasm (MiNEN) (currency check section 4). | Not offered at these sites; REDCap-side list only. |

REDCap-side list (standing rule 16; the tool does not test REDCap): REDCap lacks 8054/3, 8085/3 and 8086/3; its labels for 8010, 8122, 8131, 8154 and 8240 are not the ICD-O-3.2 preferred terms; it offers 8130/3, whose every /3 term is obsolete, and 8077 and 8148, which have no /3 term.

## 9 Conflicts with other groups

Each was checked in `ICCC-2017.sqlite` for the code at the site.

| Other group | Codes | Sites | Issue |
|---|---|---|---|
| 6 | 8960, 8311, 8312, 8316, 8317, 8318, 8319, 8361 | C65.9, C66.9 | ICCC-2017 places nephroblastoma (VIa1) and these renal cell carcinomas (VIb) in Group 6 at every site, so at the renal pelvis they refer to Group 6. Every carcinoma of the kidney (C64.9) is VIb. A urothelial carcinoma of the renal pelvis that invades the kidney stays C65.9 (pT3). |
| 6 | 8310 | C64.9, C65.9 | 8310/3 is Clear cell renal cell carcinoma at the kidney (VIb) and Mullerian clear cell adenocarcinoma at the renal pelvis (XIf10); the site answer decides. |
| 9 | 8900, 8910, 8920, 8963, 8825 | C67.0 to C63.9 (22 sites) | Rhabdomyosarcoma (IXa) and malignant rhabdoid tumour (IXd3 at these sites) refer to Group 9. Inflammatory myofibroblastic tumour is 8825/1 in ICD-O-3.2 and is not registrable; only a report calling it malignant (8825/3 Myofibroblastic sarcoma, IXb1) refers to Group 9. |
| 10 | 9071, 9100, 9080 | C67.0 to C63.9 (22 sites) | Extragonadal germ cell tumours at these sites are Xb. A urothelial carcinoma with trophoblastic differentiation is 8120/3 (Netto 2022 Table 3), not choriocarcinoma 9100/3. Testis (C62) is Group 10. |
| 4 | 8693 | C67.0 to C61.9 (17 sites) | Paraganglioma of the bladder, which the WHO urothelial table lists, is ICCC-2017 IVb. |
| 12 | 8935, 9050, 9051, 9052, 9053, 9055, 8000 | C61.9 to C68.9 (22 sites) | Prostatic stromal sarcoma 8935/3 is XIIa4; mesothelioma of the tunica vaginalis is XIIa5. The tissue-free answer 8000/3 falls in XIIb at every site in this part, so a clinical or imaging registration records a Group 12 case. |
| 11 | 8083, 8084, 8085, 8086, 8120, 8090 | C60.9, C60.0, C60.1, C60.2, C60.8 | ICCC-2017 puts carcinomas of penis, NOS (C60.9) and scrotum (C63.2) in XIe. At C60.9, 8083, 8084, 8085, 8086 and 8120 fall in no ICCC range; at C60.0 to C60.8, basal cell carcinoma 8090/3 falls in no range. Ruling 3 keeps them in Group XI; the subgroup is computed from the site (registrar question 8). |

The controller expected inflammatory myofibroblastic tumour to refer to Group 9. ICD-O-3.2 codes it 8825/1, and every ICCC-2017 range is behaviour 3, so it is an exclusion; only a report that calls it malignant (8825/3 Myofibroblastic sarcoma, IXb1) refers.

## 10 Data gaps

1. **A source reporting urothelial neoplasms of the bladder, renal pelvis, ureter or urethra in patients aged 0 to 18.** Liu 2025 (added 8 October 2026) reports urothelial papilloma, PUNLMP and low-grade non-invasive urothelial carcinoma of the bladder in children, and rare infiltration beyond the mucosa, so invasive urothelial carcinoma (8120/3) is now an option. It covers the bladder only and excluded children with upper urinary tract tumours, and it names no urothelial carcinoma subtype and no squamous, glandular, urachal or neuroendocrine carcinoma in a child. Those stay picker entries until a source reports them at ages 0 to 18. Candidate: Paner GP et al. Urothelial neoplasms of the urinary bladder occurring in young adult and pediatric patients: a comprehensive review. Adv Anat Pathol 2011;18(1):79-89; Alanee S, Shukla AR. Bladder malignancies in children aged <18 years: results from the SEER database. BJU Int 2010;106:557-560.
2. **A source reporting prostate or penile carcinoma in patients aged 0 to 18.** Without it every prostate and penile carcinoma stays in the picker. Candidate: A SEER or population-registry series of prostate and penile carcinoma under age 20.
3. **The WHO 5th edition classification of paratesticular and penile tumours (epididymis, spermatic cord, seminal vesicle, tunica vaginalis).** No file in this part covers C63.0, C63.1 or C63.7 to C63.9, so gu_male_genital_histology carries only generic answers and referrals, with no cited entity. Candidate: Moch H, Amin MB, Berney DM, et al. The 2022 WHO Classification of Tumours of the Urinary System and Male Genital Organs - Part A: Renal, Penile, and Testicular Tumours. Eur Urol 2022;82(5):458-468.
4. **The WHO ICD-O code for urachal mucinous cystic tumour of low malignant potential, and for mixed neuroendocrine neoplasms of the urinary tract.** ICCR Bladder names both without a code; the exclusion uses 8472/1 and the picker proposes 8045/3 from ICD-O-3.2 terms. Candidate: WHO Classification of Tumours, Urinary and Male Genital Tumours, 5th ed., 2022 (urachal and neuroendocrine chapters).
5. **ICD-O-3.2 topography placement of urethral glands (Littre, Cowper, Skene) and of seminal vesicle and tunica vaginalis.** The site screen assigns urethra C68.0, paraurethral gland C68.1 and other specified male genital organ C63.7 from the ICD-O topography list, which no file in this part prints. Candidate: ICD-O-3.2 topography list (Layer 1).
6. **Evidence that serum chromogranin A is used to diagnose neuroendocrine tumours of the urinary tract.** The basis-4 answer on gu_document_inventory rests on Visser 2023 Table 4 alone; ICCR Bladder names chromogranin A only as an immunohistochemical marker. Candidate: Visser 2023, Front Oncol 13:1250549 (held by the controller).
7. **A primary paediatric series that reports invasive urothelial carcinoma (pT1 or higher) in patients aged 0 to 18.** The 8120/3 option rests on Liu 2025's discussion, which reports rare infiltration into deeper layers from the literature it cites; Liu's own 17 children had urothelial papilloma or PUNLMP only. Candidate: Alanee S, Shukla AR. Bladder malignancies in children aged <18 years: results from the SEER database. BJU Int 2010;106:557-560 (cited by Liu 2025); Paner GP et al. Adv Anat Pathol 2011;18(1):79-89.
8. **Paediatric evidence for urothelial carcinoma of the renal pelvis, ureter and urethra.** `gu_urinary_histology` serves the bladder, renal pelvis, ureter and urethra, so the 8120/3 option shows at all of them. Liu 2025 reports bladder tumours only and excluded children with upper urinary tract tumours. The controller decides whether the option is limited to the bladder. Candidate: a paediatric series of upper urinary tract urothelial neoplasms.
9. **A paediatric source for Carcinoma, NOS (8010/3) at these sites.** The 8010/3 answer is an option on every histology screen in this part and rests on no paediatric source. Liu 2025 does not report it. The controller decides. Candidate: none identified.
10. **Whether the urinary picker keeps the 8120/3 subtypes now that the tree offers 8120/3 as an option.** Build contract D2 excludes from the picker the codes the tree already offers as options. Urothelial carcinoma with squamous, glandular or trophoblastic differentiation, plasmacytoid, lipid-rich and clear cell (glycogen-rich) urothelial carcinoma all code 8120/3 and remain picker rows here. The controller decides. Candidate: build contract D2 (registrar).

### Questions for the registrar

1. No source in this part reports a bladder, urinary tract, prostate or penile carcinoma in a patient aged 0 to 18. Should invasive urothelial carcinoma (8120/3) and the non-invasive urothelial lesions stay as they are (picker and exclusion screen), or become options on the bladder histology screen until a paediatric source is fetched? (8 October 2026: Liu 2025 reports both in children; invasive urothelial carcinoma is now an option and the non-invasive lesions stay on the exclusion screen. See section 11.)
2. Urothelial carcinoma subtypes whose WHO code is lower than 8120 (lymphoepithelioma-like 8082/3, giant cell 8031/3, poorly differentiated 8020/3) and penile HPV-associated subtypes lower than 8085 (basaloid 8083/3, warty 8054/3, clear cell 8084/3, lymphoepithelial 8082/3): record the WHO subtype code (proposed) or Rule K's higher code?
3. Lipid-rich (ICD-O-3.2 8314/3) and clear cell glycogen-rich (8315/3) urothelial carcinoma, and urothelial carcinoma with glandular differentiation (8140 is higher than 8120): the WHO prints 8120/3 for all three. Record 8120/3 (proposed) or Rule K's higher code?
4. Mixed adenocarcinoma of the urinary tract: Netto 2022 prints 8323/3, ICCR with the July 2024 corrigenda prints 8140/3. Confirm 8140/3.
5. Small cell neuroendocrine carcinoma mixed with urothelial carcinoma: record 8045/3 Combined small cell carcinoma (proposed; ICD-O-3.2 synonym Mixed small cell carcinoma), 8041/3, or 8154/3?
6. Penile squamous cell carcinoma, usual type, with no HPV status or p16 result: 8070/3 (proposed; ICD-O-3.2 prints usual type as a synonym there) or 8086/3 (ICCR places usual type under HPV-independent)?
7. Urine cytology positive for high-grade urothelial carcinoma with no histology: record 8120/3 basis 5 (proposed), or 8010/3, given that cytology cannot tell carcinoma in situ from invasive carcinoma?
8. Carcinomas at penis, NOS (C60.9) and scrotum (C63.2) belong to XIe; 8083, 8084, 8085, 8086 and 8120 at C60.9, and 8090 at C60.0 to C60.8, fall in no ICCC range. Confirm ruling 3 keeps them in Group XI with the subgroup computed from the site.
9. Inflammatory myofibroblastic tumour is 8825/1 in ICD-O-3.2: confirm it is an exclusion, with only a report calling it malignant (8825/3) referring to Group 9.

## 11. Paediatric evidence added 8 October 2026

Source added: Liu 2025 (`XIf8-bladder-urothelial-paediatric__Liu-2025.txt`), a single-centre series of 17 children (ages 3 to 18) with bladder urothelial neoplasms treated from 2006 to 2024: 11 urothelial papillomas and 6 PUNLMPs. Its discussion reviews the paediatric literature. It reports no tumour of the renal pelvis, ureter, urethra, prostate or penis.

| Entity | Before | After | Cite |
|---|---|---|---|
| Urothelial papilloma, 8120/0 | paediatric not_reported; exclusion | paediatric common; exclusion; first on `gu_not_malignant_urinary` | Liu 2025, PMC section 8 ("the two most common types of bladder neoplasms in children, UP and PUNLMP"); Liu 2025, PMC section 7 ("comprised 17 patients, including 11 children diagnosed with UP"); Liu 2025, PMC section 7 ("The average age of onset was 10.5 years (range: 3–18 years)") |
| Papillary urothelial neoplasm of low malignant potential, 8130/1 | paediatric not_reported; exclusion | paediatric common; exclusion; second on `gu_not_malignant_urinary` | Liu 2025, PMC section 8 ("the two most common types of bladder neoplasms in children, UP and PUNLMP"); Liu 2025, PMC section 8 ("The majority of urothelial bladder tumors in children are papillary urothelial neoplasm"); Liu 2025, PMC section 7 ("The study focused on six male children with PUNLMP") |
| Non-invasive papillary urothelial carcinoma, low grade and high grade, 8130/2 | paediatric not_reported; exclusion | paediatric common; exclusion; third on `gu_not_malignant_urinary` (inverted urothelial papilloma moves below it) | Liu 2025, PMC section 8 ("The majority of urothelial bladder tumors in children are papillary urothelial neoplasm"); Liu 2025, PMC section 8 ("(PUNLMP) and low-grade urothelial carcinomas, often confined to the mucosal layer (Ta)") |
| Invasive urothelial carcinoma (conventional, nested, large nested, tubular and microcystic), 8120/3 | paediatric not_reported; picker; first row of `gu_urinary_picker` | paediatric occurs; option; first answer on `gu_urinary_histology`, basis 7, reason "Recorded as Transitional cell carcinoma, NOS (8120/3).", recognition aid on pT1 or higher kept | Liu 2025, PMC section 8 ("often confined to the mucosal layer (Ta) with rare infiltration into deeper layers"); Liu 2025, PMC section 8 ("childhood bladder urothelial carcinoma is typically low-grade") |
| Plasmacytoid urothelial carcinoma, 8120/3 | named inside the first row of `gu_urinary_picker` | own row on `gu_urinary_picker` (still a picker entry); the picker hint drops the sentence on papillary carcinoma with invasion, which now sits on `gu_urinary_histology` | Netto 2022, PDF p. 7 ("8122/3 Plasmacytoid urothelial") |
| Picker answer on `gu_urinary_histology` | "A carcinoma of any type the report names, such as urothelial (transitional cell) carcinoma with invasion, …" | "Another carcinoma the report names, such as micropapillary, plasmacytoid or sarcomatoid urothelial carcinoma, …" | none (label only) |
| Rhabdomyosarcoma, 8910/3 | paediatric occurs; refer to Group 9; Pfister 2022 only | unchanged decision; Liu 2025 cite added to the entity and to the sarcoma answer on `gu_urinary_histology` | Liu 2025, PMC section 8 ("other pediatric malignancies, including Wilms tumor and bladder rhabdomyosarcoma") |

Not changed: every other picker entity in this part. Liu 2025 reports no urothelial carcinoma subtype, and no squamous, glandular, urachal, neuroendocrine, prostatic or penile carcinoma, in a child. Carcinoma, no type named (8010/3) stays an option with no paediatric source (data gap 9). Liu 2025 names Wilms tumour as a cause of haematuria in children but not at the renal pelvis or ureter, so the nephroblastoma referral keeps its Pfister 2022 cite. No new entity was added. Data gaps 1 and 7 to 10 record what stays open.
