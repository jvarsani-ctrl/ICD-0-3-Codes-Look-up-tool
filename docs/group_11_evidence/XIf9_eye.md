# Group 11 evidence — XIf9 carcinoma of the eye and adnexa

Part `XIf9_eye`. Sites C69.0 conjunctiva, C69.1 cornea, C69.2 retina, C69.3 choroid, C69.4 ciliary body, C69.5 lacrimal gland and duct, C69.6 orbit, C69.8 overlapping lesion, C69.9 eye, part not stated. ICCC-2017 places every Group XI carcinoma code at these sites in XIf9. The eyelid (C44.1) belongs to XIe and melanoma at every eye site to XId; this part hands both to their own trees. Built 8 October 2026 from the three files below, read only through the snippet tool, with the codes queried in `icdo32.sqlite` and `ICCC-2017.sqlite`. The checker found all 203 quotations on their cited pages.

## 1. Sources

| File | Citation | WHO volume |
|---|---|---|
| `XIf9-eye-XId-ocular-melanoma__Milman-2023.txt` | Milman T, Grossniklaus HE, Goldman-Levy G, et al. The 5th Edition of the World Health Organization Classification of Tumours of the Eye and Orbit. Ocul Oncol Pathol 2023;9(3-4):71-95. doi:10.1159/000530730 | WHO Classification of Tumours, Eye and Orbit Tumours, 5th edition, 2023 (volume 13) |
| `ALL-paediatric-occurrence__Pfister-2022.txt` | Pfister SM, Reyes-Mugica M, Chan JKC, et al. A Summary of the Inaugural WHO Classification of Pediatric Tumors: Transitioning from the Optical into the Molecular Era. Cancer Discov 2022;12(2):331-355 | WHO Classification of Tumours, Paediatric Tumours, 5th edition, 2022 |
| `RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt` | World Health Organization. International Classification of Diseases for Oncology, 3rd edition, 1st revision (ICD-O-3.1), section 4, Coding guidelines, printed pp. 14-28 | ICD-O-3.1 coding manual (not a tumour classification) |

Milman 2023 summarises the fifth-edition WHO eye volume. Its tables list entity names only; it prints no ICD-O code. Every code below is matched by term in ICD-O-3.2 (`icdo32.sqlite`). Pfister 2022 Table 3 (PDF p. 12, read from the page image) is the paediatric list: its eye section names retinocytoma, retinoblastoma, medulloepithelioma and optic nerve gliomas, and no carcinoma.

## 2. Entities

| Entity (WHO term) | Code | ICD-O-3.2 term matched (level) | Preferred term | Sites | Paediatric | Decision | Page |
|---|---|---|---|---|---|---|---|
| Conjunctival squamous cell carcinoma; squamous cell carcinoma of the lacrimal drainage system | 8070/3 | Squamous cell carcinoma, NOS (Preferred) | Squamous cell carcinoma, NOS | C69.0, C69.1, C69.5 | not_reported | picker | Milman 2023, PDF p. 3; Milman 2023, PDF p. 12; Pfister 2022, PDF p. 12 |
| Squamous cell carcinoma with mucinous differentiation (conjunctiva) | 8070/3 | Squamous cell carcinoma, NOS (Preferred) | Squamous cell carcinoma, NOS | C69.0 | not_reported | registrar | Milman 2023, PDF p. 7; Milman 2023, PDF p. 6 |
| Adenosquamous carcinoma (conjunctiva) | 8560/3 | Adenosquamous carcinoma (Preferred) | Adenosquamous carcinoma | C69.0, C69.1 | not_reported | picker | Milman 2023, PDF p. 3; Milman 2023, PDF p. 7; Milman 2023, PDF p. 5 |
| Mucoepidermoid carcinoma (lacrimal gland, lacrimal drainage system; the Eye4 term for some conjunctival carcinomas) | 8430/3 | Mucoepidermoid carcinoma (Preferred) | Mucoepidermoid carcinoma | C69.0, C69.5 | not_reported | picker | Milman 2023, PDF p. 12; Milman 2023, PDF p. 14; Milman 2023, PDF p. 7 |
| Conjunctival squamous intraepithelial neoplasia, high grade | 8077/2 | Squamous intraepithelial neoplasia, high grade (Preferred) | Squamous intraepithelial neoplasia, high grade | C69.0, C69.1 | not_reported | exclusion | Milman 2023, PDF p. 3; Milman 2023, PDF p. 7 |
| Conjunctival squamous intraepithelial neoplasia, low grade | 8077/0 | Squamous intraepithelial neoplasia, low grade (Preferred) | Squamous intraepithelial neoplasia, low grade | C69.0, C69.1 | not_reported | exclusion | Milman 2023, PDF p. 3 |
| Squamous cell carcinoma in situ of the conjunctiva or cornea | 8070/2 | Squamous cell carcinoma in situ, NOS (Preferred) | Squamous cell carcinoma in situ, NOS | C69.0, C69.1 | not_reported | exclusion | Milman 2023, PDF p. 3; ICD-O-3.1 manual, PDF p. 6 |
| Conjunctival squamous papilloma; squamous papilloma of the lacrimal drainage system | 8052/0 | Squamous papilloma (Synonym) | Squamous cell papilloma, NOS | C69.0, C69.5 | not_reported | exclusion | Milman 2023, PDF p. 3; Milman 2023, PDF p. 12 |
| Inverted papilloma of the lacrimal drainage system | 8121/1 | Schneiderian papilloma, inverted (Related) | Sinonasal papilloma, inverted | C69.5 | not_reported | exclusion | Milman 2023, PDF p. 12 |
| Conjunctival oncocytoma; lacrimal gland oncocytoma | 8290/0 | Oncocytoma (Synonym) | Oxyphilic adenoma | C69.0, C69.5 | not_reported | exclusion | Milman 2023, PDF p. 3; Milman 2023, PDF p. 12 |
| Sebaceous carcinoma reported at the conjunctiva or caruncle | 8410/3 | Sebaceous carcinoma (Preferred) | Sebaceous carcinoma | C69.0 | not_reported | refer | Milman 2023, PDF p. 7; Milman 2023, PDF p. 9 |
| Pleomorphic adenoma of the lacrimal gland | 8940/0 | Pleomorphic adenoma (Preferred) | Pleomorphic adenoma | C69.5 | not_reported | exclusion | Milman 2023, PDF p. 12; Milman 2023, PDF p. 13 |
| Myoepithelioma of the lacrimal gland | 8982/0 | Myoepithelioma, NOS (Preferred) | Myoepithelioma, NOS | C69.5 | not_reported | exclusion | Milman 2023, PDF p. 12 |
| Intraductal carcinoma of the lacrimal gland | 8500/2 | Intraductal carcinoma, NOS (Synonym) | Intraductal carcinoma, noninfiltrating, NOS | C69.5 | not_reported | exclusion | Milman 2023, PDF p. 12 |
| Carcinoma ex pleomorphic adenoma (lacrimal gland) | 8941/3 | Carcinoma ex pleomorphic adenoma (Preferred) | Carcinoma ex pleomorphic adenoma | C69.5 | not_reported | picker | Milman 2023, PDF p. 12; Milman 2023, PDF p. 13 |
| Adenoid cystic carcinoma (lacrimal gland) | 8200/3 | Adenoid cystic carcinoma (Preferred) | Adenoid cystic carcinoma | C69.5 | not_reported | picker | Milman 2023, PDF p. 13 |
| Primary ductal adenocarcinoma of the lacrimal gland | 8500/3 | Duct adenocarcinoma, NOS (Synonym) | Infiltrating duct carcinoma, NOS | C69.5 | not_reported | picker | Milman 2023, PDF p. 12; Milman 2023, PDF p. 14 |
| Secretory carcinoma (lacrimal gland) | 8502/3 | Secretory carcinoma (Preferred) | Secretory carcinoma | C69.5 | not_reported | picker | Milman 2023, PDF p. 14 |
| Epithelial-myoepithelial carcinoma (lacrimal gland) | 8562/3 | Epithelial-myoepithelial carcinoma (Preferred) | Epithelial-myoepithelial carcinoma | C69.5 | not_reported | picker | Milman 2023, PDF p. 12; Milman 2023, PDF p. 14 |
| Acinic cell carcinoma (lacrimal gland) | 8550/3 | Acinic cell adenocarcinoma (Synonym) | Acinar cell carcinoma | C69.5 | not_reported | picker | Milman 2023, PDF p. 15 |
| Adenocarcinoma, NOS (lacrimal gland; lacrimal drainage system) | 8140/3 | Adenocarcinoma, NOS (Preferred) | Adenocarcinoma, NOS | C69.5 | not_reported | picker | Milman 2023, PDF p. 12 |
| Lymphoepithelial carcinoma (lacrimal drainage system) | 8082/3 | Lymphoepithelial carcinoma (Preferred) | Lymphoepithelial carcinoma | C69.5 | not_reported | picker | Milman 2023, PDF p. 12 |
| Adenocarcinoma of the ciliary body epithelium | 8140/3 | Adenocarcinoma, NOS (Preferred) | Adenocarcinoma, NOS | C69.4 | not_reported | picker | Milman 2023, PDF p. 10; Milman 2023, PDF p. 11 |
| Adenocarcinoma of the retinal pigment epithelium | 8140/3 | Adenocarcinoma, NOS (Preferred) | Adenocarcinoma, NOS | C69.2 | not_reported | picker | Milman 2023, PDF p. 10; Milman 2023, PDF p. 11 |
| Adenoma of the ciliary body epithelium; adenoma of the retinal pigment epithelium | 8140/0 | Adenoma, NOS (Preferred) | Adenoma, NOS | C69.2, C69.4 | not_reported | exclusion | Milman 2023, PDF p. 10 |
| Oncocytic carcinoma of the lacrimal gland (removed from WHO Eye5 as obsolete) | 8290/3 | Oncocytic carcinoma (Synonym) | Oxyphilic adenocarcinoma | C69.5 | not_reported | registrar | Milman 2023, PDF p. 15 |
| Medulloepithelioma of the ciliary body (including teratoid medulloepithelioma) | 9501/3 | Medulloepithelioma, NOS (Preferred) | Medulloepithelioma, NOS | C69.4 | occurs | refer → Group 4 | Pfister 2022, PDF p. 12; Milman 2023, PDF p. 10; Milman 2023, PDF p. 11 |
| Medulloepithelioma of the optic disc and optic nerve | 9501/3 | Medulloepithelioma, NOS (Preferred) | Medulloepithelioma, NOS | C72.3 | occurs | refer → Group 3 | Milman 2023, PDF p. 12; Pfister 2022, PDF p. 12 |
| Retinoblastoma | 9510/3 | Retinoblastoma, NOS (Preferred) | Retinoblastoma, NOS | C69.0, C69.1, C69.2, C69.3, C69.4, C69.5, C69.6, C69.8, C69.9 | occurs | refer → Group 5 | Pfister 2022, PDF p. 12; Milman 2023, PDF p. 11; ICD-O-3.1 manual, PDF p. 2 |
| Retinocytoma (retinoma) | 9510/0 | Retinocytoma (Preferred) | Retinocytoma | C69.2 | occurs | refer → Group 5 | Milman 2023, PDF p. 8; Pfister 2022, PDF p. 12 |
| Ocular adnexal lymphomas; intraocular lymphomas (primary vitreoretinal and choroidal) | 9590/3 | Malignant lymphoma, NOS (Preferred) | Malignant lymphoma, NOS | C69.0, C69.1, C69.2, C69.3, C69.4, C69.5, C69.6, C69.8, C69.9 | not_reported | refer → Group 2 | Milman 2023, PDF p. 16; ICD-O-3.1 manual, PDF p. 2 |
| Langerhans cell histiocytosis of the orbit | 9751/1 | Langerhans cell histiocytosis, NOS (Preferred) | Langerhans cell histiocytosis, NOS | C69.6 | not_reported | refer → Group 2 | Milman 2023, PDF p. 16 |
| Extramedullary myeloid sarcoma of the orbit | 9930/3 | Myeloid sarcoma (Preferred) | Myeloid sarcoma | C69.6 | not_reported | refer → Group 1 | Milman 2023, PDF p. 16; ICD-O-3.1 manual, PDF p. 2 |
| Rhabdomyosarcoma of the orbit | 8900/3 | Rhabdomyosarcoma, NOS (Preferred) | Rhabdomyosarcoma, NOS | C69.6 | not_reported | refer → Group 9 | Milman 2023, PDF p. 20 |
| Teratoma of the orbit | 9080/1 | Teratoma, NOS (Preferred) | Teratoma, NOS | C69.6 | not_reported | refer → Group 10 | Milman 2023, PDF p. 15 |
| Yolk sac tumour of the orbit | 9071/3 | Yolk sac tumor, NOS (Preferred) | Yolk sac tumor, NOS | C69.6 | not_reported | refer → Group 10 | Milman 2023, PDF p. 15 |
| Conjunctival melanoma; choroidal, ciliary body and iris melanoma; primary orbital melanoma; melanoma involving the lacrimal drainage system | 8720/3 | Malignant melanoma, NOS (Preferred) | Malignant melanoma, NOS | C69.0, C69.1, C69.2, C69.3, C69.4, C69.5, C69.6, C69.8, C69.9 | not_reported | refer | Milman 2023, PDF p. 3; Milman 2023, PDF p. 10; Milman 2023, PDF p. 15; Milman 2023, PDF p. 12 |
| Pilocytic astrocytoma and other gliomas of the optic nerve | 9421/1 | Pilocytic astrocytoma (Preferred) | Pilocytic astrocytoma | C72.3 | occurs | refer → Group 3 | Pfister 2022, PDF p. 12; Milman 2023, PDF p. 12 |
| Ewing sarcoma of the orbital bone | 9364/3 | Ewing sarcoma (Preferred) | Ewing sarcoma | C41.0 | not_reported | refer → Group 8 | Milman 2023, PDF p. 21 |
| Carcinoma, type not stated (NOS fallback) | 8010/3 | Carcinoma, NOS (Preferred) | Carcinoma, NOS | C69.0, C69.1, C69.2, C69.3, C69.4, C69.5, C69.6, C69.8, C69.9 | not_reported | option | ICD-O-3.1 manual, PDF p. 6 |
| Malignant tumour, type not stated (tissue-free registration and non-typed malignant cytology) | 8000/3 | Neoplasm, malignant (Preferred) | Neoplasm, malignant | C69.0, C69.1, C69.2, C69.3, C69.4, C69.5, C69.6, C69.8, C69.9 | not_reported | refer → Group 12 | ICD-O-3.1 manual, PDF p. 6 |

**Why every carcinoma is a picker entry.** Ruling 1 makes an entity an option only when a source reports it in children. Neither source does for any eye carcinoma: Pfister 2022 Table 3 lists no carcinoma among the paediatric eye tumours (PDF p. 12), and Milman 2023 mentions children only for retinoblastoma (PDF p. 8). So conjunctival squamous cell carcinoma, the lacrimal gland carcinomas and the intraocular adenocarcinomas sit in the eye picker. The registrar may promote them if the controller fetches a paediatric source (section 10).

Notes on the decisions:

- **Conjunctival squamous cell carcinoma; squamous cell carcinoma of the lacrimal drainage system** (8070/3): Neither Milman 2023 nor Pfister 2022 reports this carcinoma in children; Pfister 2022 Table 3 lists no carcinoma among the paediatric eye tumours. It is a picker entry (ruling 1). Milman lists it at the conjunctiva (Table 3) and the lacrimal drainage system (Table 12).
- **Squamous cell carcinoma with mucinous differentiation (conjunctiva)** (8070/3): WHO Eye5 names a squamous cell carcinoma with scattered mucin-containing cells, and no true glands, a squamous cell carcinoma with mucinous differentiation rather than an adenosquamous carcinoma. ICD-O-3.2 prints no term for it. 8070/3 follows the WHO name; Rule K would give the higher code 8480/3 Mucinous adenocarcinoma. The registrar decides.
- **Adenosquamous carcinoma (conjunctiva)** (8560/3): Neither Milman 2023 nor Pfister 2022 reports this carcinoma in children; Pfister 2022 Table 3 lists no carcinoma among the paediatric eye tumours. It is a picker entry (ruling 1). WHO Eye5 keeps the term for tumours with both squamous cell carcinoma and true mucin-forming adenocarcinoma.
- **Mucoepidermoid carcinoma (lacrimal gland, lacrimal drainage system; the Eye4 term for some conjunctival carcinomas)** (8430/3): Neither Milman 2023 nor Pfister 2022 reports this carcinoma in children; Pfister 2022 Table 3 lists no carcinoma among the paediatric eye tumours. It is a picker entry (ruling 1). WHO Eye5 lists it in the lacrimal gland and drainage system. At the conjunctiva, Eye4 used adenosquamous carcinoma as the preferred term; a conjunctival report that still says mucoepidermoid carcinoma is coded as written, 8430/3.
- **Conjunctival squamous intraepithelial neoplasia, high grade** (8077/2): WHO Eye5 lists it among the premalignant conjunctival tumours. Behaviour /2 is outside Group XI.
- **Conjunctival squamous intraepithelial neoplasia, low grade** (8077/0): Low-grade intraepithelial neoplasia is not malignant. Milman names the entity without its grades; ICD-O-3.2 codes the low grade /0.
- **Squamous cell carcinoma in situ of the conjunctiva or cornea** (8070/2): An in situ carcinoma has not invaded; behaviour /2 is outside Group XI.
- **Conjunctival squamous papilloma; squamous papilloma of the lacrimal drainage system** (8052/0): Benign epithelial tumour (WHO Eye5 Tables 3 and 12).
- **Inverted papilloma of the lacrimal drainage system** (8121/1): Listed with the benign and premalignant drainage-system tumours; ICD-O-3.2 codes it /1.
- **Conjunctival oncocytoma; lacrimal gland oncocytoma** (8290/0): Benign epithelial tumour.
- **Sebaceous carcinoma reported at the conjunctiva or caruncle** (8410/3): WHO Eye5 removed sebaceous carcinoma from the conjunctiva and caruncle chapter and covers it with the eyelid tumours. The eye tree sends it to the skin carcinoma tree at the eyelid (C44.1, XIe), inside Group XI. ICD-O-3.2 prints the skin site (C44._) beside the term. A report that places the tumour in the conjunctiva itself is a registrar question.
- **Pleomorphic adenoma of the lacrimal gland** (8940/0): Benign lacrimal gland neoplasm.
- **Myoepithelioma of the lacrimal gland** (8982/0): Listed with the benign and premalignant lacrimal gland tumours.
- **Intraductal carcinoma of the lacrimal gland** (8500/2): WHO Eye5 lists intraductal carcinoma with the benign and premalignant lacrimal gland tumours; ICD-O-3.2 codes it /2.
- **Carcinoma ex pleomorphic adenoma (lacrimal gland)** (8941/3): Neither Milman 2023 nor Pfister 2022 reports this carcinoma in children; Pfister 2022 Table 3 lists no carcinoma among the paediatric eye tumours. It is a picker entry (ruling 1). ICD-O-3.2 prints the salivary gland sites (C07._, C08._) beside the term; the stated lacrimal gland site wins (Rule H).
- **Adenoid cystic carcinoma (lacrimal gland)** (8200/3): Neither Milman 2023 nor Pfister 2022 reports this carcinoma in children; Pfister 2022 Table 3 lists no carcinoma among the paediatric eye tumours. It is a picker entry (ruling 1).
- **Primary ductal adenocarcinoma of the lacrimal gland** (8500/3): Neither Milman 2023 nor Pfister 2022 reports this carcinoma in children; Pfister 2022 Table 3 lists no carcinoma among the paediatric eye tumours. It is a picker entry (ruling 1). Milman prints no code. ICD-O-3.2 lists Duct adenocarcinoma, NOS at 8500/3; the breast site (C50._) printed beside the preferred term does not apply at the lacrimal gland (Rule H).
- **Secretory carcinoma (lacrimal gland)** (8502/3): Neither Milman 2023 nor Pfister 2022 reports this carcinoma in children; Pfister 2022 Table 3 lists no carcinoma among the paediatric eye tumours. It is a picker entry (ruling 1).
- **Epithelial-myoepithelial carcinoma (lacrimal gland)** (8562/3): Neither Milman 2023 nor Pfister 2022 reports this carcinoma in children; Pfister 2022 Table 3 lists no carcinoma among the paediatric eye tumours. It is a picker entry (ruling 1).
- **Acinic cell carcinoma (lacrimal gland)** (8550/3): Neither Milman 2023 nor Pfister 2022 reports this carcinoma in children; Pfister 2022 Table 3 lists no carcinoma among the paediatric eye tumours. It is a picker entry (ruling 1). ICD-O-3.2 prints Acinar cell carcinoma as the preferred term; Acinic cell adenocarcinoma is its synonym.
- **Adenocarcinoma, NOS (lacrimal gland; lacrimal drainage system)** (8140/3): Neither Milman 2023 nor Pfister 2022 reports this carcinoma in children; Pfister 2022 Table 3 lists no carcinoma among the paediatric eye tumours. It is a picker entry (ruling 1).
- **Lymphoepithelial carcinoma (lacrimal drainage system)** (8082/3): Neither Milman 2023 nor Pfister 2022 reports this carcinoma in children; Pfister 2022 Table 3 lists no carcinoma among the paediatric eye tumours. It is a picker entry (ruling 1).
- **Adenocarcinoma of the ciliary body epithelium** (8140/3): Neither Milman 2023 nor Pfister 2022 reports this carcinoma in children; Pfister 2022 Table 3 lists no carcinoma among the paediatric eye tumours. It is a picker entry (ruling 1). Milman prints no code; Adenocarcinoma, NOS is the ICD-O-3.2 term the WHO name reduces to.
- **Adenocarcinoma of the retinal pigment epithelium** (8140/3): Neither Milman 2023 nor Pfister 2022 reports this carcinoma in children; Pfister 2022 Table 3 lists no carcinoma among the paediatric eye tumours. It is a picker entry (ruling 1). The topography of the retinal pigment epithelium is taken as retina (C69.2); see data gaps.
- **Adenoma of the ciliary body epithelium; adenoma of the retinal pigment epithelium** (8140/0): Benign epithelial tumour.
- **Oncocytic carcinoma of the lacrimal gland (removed from WHO Eye5 as obsolete)** (8290/3): WHO Eye5 removed oncocytic carcinoma of the lacrimal gland as an obsolete entity. ICD-O-3.2 keeps 8290/3 current, and the code is in the XIf9 inventory, so the picker would offer it. The registrar decides whether the eye picker holds it.
- **Medulloepithelioma of the ciliary body (including teratoid medulloepithelioma)** (9501/3): Pfister 2022 lists medulloepithelioma among the paediatric retinal and neuroepithelial tumours. ICCC-2017 places 9501-9504 at C00-C69 in IVb, so it refers to Group IV, whose tree holds the ciliary body site.
- **Medulloepithelioma of the optic disc and optic nerve** (9501/3): The optic nerve is C72.3; ICCC-2017 places 9501-9504 at C70-C72 in IIIc3, so it refers to Group III.
- **Retinoblastoma** (9510/3): Pfister 2022 lists it as a paediatric eye tumour; ICCC-2017 places 9510-9514 in Group V at every site. Biopsy is usually avoided, so Group V registers it on eye examination and imaging; the eye carcinoma tree refers it before any 8000/3 answer.
- **Retinocytoma (retinoma)** (9510/0): WHO Eye5 classes it as premalignant; Group V's tree decides how a report that uses the word is recorded.
- **Ocular adnexal lymphomas; intraocular lymphomas (primary vitreoretinal and choroidal)** (9590/3): Lymphoma is Group II (ICCC-2017 II at every site). Rule D records an extranodal lymphoma at its site of origin; Group II's tree assigns the code.
- **Langerhans cell histiocytosis of the orbit** (9751/1): ICCC-2017 places 9751 in IId (behaviour /3). Group II's tree decides the behaviour and whether it registers.
- **Extramedullary myeloid sarcoma of the orbit** (9930/3): ICCC-2017 places 9930 in Ib. Rule E keeps the site of a myeloid sarcoma (the orbit) rather than bone marrow.
- **Rhabdomyosarcoma of the orbit** (8900/3): ICCC-2017 places 8900-8920 in IXa at every site.
- **Teratoma of the orbit** (9080/1): Germ cell tumour of the orbit (WHO Eye5 Table 14); Group X's tree decides mature, immature and malignant teratoma.
- **Yolk sac tumour of the orbit** (9071/3): ICCC-2017 places 9071 at C69 in Xb4.
- **Conjunctival melanoma; choroidal, ciliary body and iris melanoma; primary orbital melanoma; melanoma involving the lacrimal drainage system** (8720/3): Melanoma is XId at every site and is owned by the melanoma part; the eye tree hands it to the melanoma tree inside Group XI.
- **Pilocytic astrocytoma and other gliomas of the optic nerve** (9421/1): Pfister 2022 lists optic nerve gliomas as paediatric eye tumours. The optic nerve is C72.3 and ICCC-2017 places 9421 in IIIb.
- **Ewing sarcoma of the orbital bone** (9364/3): A tumour of the orbital bone is recorded at the bone; ICCC-2017 places 9364 at C40-C41 in VIIIc2 (at the orbit soft tissue, C69.6, it is IXd2).
- **Carcinoma, type not stated (NOS fallback)** (8010/3): The NOS fallback of every eye histology screen and of the picker (node-type rule, not a paediatric claim).
- **Malignant tumour, type not stated (tissue-free registration and non-typed malignant cytology)** (8000/3): The eye tree records 8000/3 on a clinical note or imaging (registrar's tissue-free rule) and on cytology that names no tumour type. ICCC-2017 places 8000/3 at C69 in XIIb, so these cases leave Group XI when the subgroup is computed.

## 3. The pathway

The eye is one site family of the general carcinoma tree (approach 3). Nine screens: the evidence gate, a cytology screen, the site screen, four site histology screens, the carcinoma picker and a deposit screen. Node ids are suggestions; `mel_site`, `mel_conjunctiva`, `mel_eye` (melanoma part), `sk_histology` (skin part), `site_capture` and `site_capture_unknown_primary` (shared) are nodes of other parts that the controller binds.

The basis of diagnosis on a code answer is 7 when the case came through the histology route and 5 when it came through the cytology route; the picker is shared by both, so the engine takes the basis from the gate answer.

### `ey_evidence` (document_inventory)

**Question:** What does the file hold about this tumour of the eye, the lacrimal gland or the orbit?

**Hint:** Choose the strongest evidence in the file. An immunohistochemistry or gene report on its own does not stand in for a histology report. A tumour the file calls possible or suspected is not registrable.

| Option | Outcome | Records | Reason | Recognition aid | Source |
|---|---|---|---|---|---|
| The file names retinoblastoma or retinocytoma (retinoma), from an eye examination, imaging or a pathology report | refer | Group 5 | Retinoblastoma is recorded in Group V, which registers it on an eye examination or imaging, because a biopsy of the eye is usually avoided. |  | Milman 2023, PDF p. 11; Pfister 2022, PDF p. 12 |
| A referral letter or clinical note only | code | 8000/3, basis 1 | Recorded as Neoplasm, malignant (8000/3). A clinical note does not show the tumour type. |  |  |
| An imaging report only (ultrasound, computed tomography or magnetic resonance imaging) | code | 8000/3, basis 2 | Recorded as Neoplasm, malignant (8000/3). An imaging report does not show the tumour type. |  |  |
| A cytology report (a fine-needle aspirate or another cytology sample) | go | → `ey_cytology` | The next screen asks what the cytology report calls the tumour. |  |  |
| A histology report (biopsy or excision), with or without immunohistochemistry or gene reports | go | → `ey_site` | The next screen asks where the tumour arose. |  |  |
| The file calls the tumour possible or suspected, with no diagnosis made | not_registrable | not registrable | A possible or suspected tumour is not registrable. |  |  |

### `ey_cytology` (histology_subclassification)

**Question:** What does the cytology report call the tumour?

**Hint:** Use the report's own words.

| Option | Outcome | Records | Reason | Recognition aid | Source |
|---|---|---|---|---|---|
| Carcinoma, type not stated | code | 8010/3, basis 5 | Recorded as Carcinoma, NOS (8010/3). |  | ICD-O-3.1 manual, PDF p. 6 |
| Squamous cell carcinoma | code | 8070/3, basis 5 | Recorded as Squamous cell carcinoma, NOS (8070/3). |  | Milman 2023, PDF p. 3 |
| Adenocarcinoma | code | 8140/3, basis 5 | Recorded as Adenocarcinoma, NOS (8140/3). |  | Milman 2023, PDF p. 12; Milman 2023, PDF p. 11 |
| Another carcinoma the report names | go | → `ey_carcinoma_other` | The next screen lists the carcinomas; cytology is the basis of diagnosis (5). |  |  |
| Melanoma | go | → `mel_site` | Melanoma is recorded with the melanomas; the next screen asks about it. |  | Milman 2023, PDF p. 3 |
| Retinoblastoma | refer | Group 5 | Retinoblastoma is recorded in Group V, which registers it on an eye examination or imaging, because a biopsy of the eye is usually avoided. |  | Milman 2023, PDF p. 11 |
| Medulloepithelioma | refer | Group 4 | Medulloepithelioma of the eye is recorded in Group IV. |  | Milman 2023, PDF p. 11 |
| Lymphoma | refer | Group 2 | Lymphoma is recorded in Group II, at the part of the eye or orbit where it arose. |  | Milman 2023, PDF p. 16 |
| Malignant cells, tumour type not stated | code | 8000/3, basis 5 | Recorded as Neoplasm, malignant (8000/3). |  |  |
| No malignant cells, or the sample is not diagnostic | not_registrable | not registrable | A cytology report without malignant cells does not register a tumour. |  |  |

### `ey_site` (site_resolution)

**Question:** Where did the tumour arise?

**Hint:** Use the site the histology report or the operation note names. A tumour the report places at the limbus, where the cornea meets the conjunctiva, is recorded at the cornea (C69.1).

| Option | Outcome | Records | Reason | Recognition aid | Source |
|---|---|---|---|---|---|
| Conjunctiva | go | → `ey_surface_histology` | Site recorded as Conjunctiva (C69.0). |  | Milman 2023, PDF p. 3 |
| Cornea, or the limbus | go | → `ey_surface_histology` | Site recorded as Cornea (C69.1). |  |  |
| Lacrimal gland | go | → `ey_lacrimal_histology` | Site recorded as Lacrimal gland (C69.5). |  | Milman 2023, PDF p. 12 |
| Lacrimal sac or nasolacrimal duct (the tear drainage passages) | go | → `ey_lacrimal_histology` | Site recorded as Lacrimal gland and duct (C69.5), which holds the lacrimal sac and the nasolacrimal duct. |  | Milman 2023, PDF p. 12 |
| Retina, including the retinal pigment epithelium | go | → `ey_intraocular_histology` | Site recorded as Retina (C69.2). |  | Milman 2023, PDF p. 10 |
| Choroid | go | → `ey_intraocular_histology` | Site recorded as Choroid (C69.3). |  |  |
| Ciliary body or iris | go | → `ey_intraocular_histology` | Site recorded as Ciliary body (C69.4). |  | Milman 2023, PDF p. 10 |
| Orbit (the tissue around the eyeball, including the muscles that move the eye) | go | → `ey_orbit_histology` | Site recorded as Orbit (C69.6). |  |  |
| More than one of these parts, and the report cannot say where the tumour began | go | → `ey_orbit_histology` | Recorded at Overlapping lesion of eye and adnexa (C69.8), because the point of origin cannot be determined. |  | ICD-O-3.1 manual, PDF p. 2 |
| Eye, part not stated | go | → `ey_orbit_histology` | Site recorded as Eye, NOS (C69.9). |  |  |
| Eyelid, including the eyelid margin | go | → `sk_histology` | A tumour of the eyelid is recorded at the skin of the eyelid (C44.1), with the skin carcinomas. |  | Milman 2023, PDF p. 9 |
| Optic nerve | refer | Group 3 | A tumour of the optic nerve is recorded at the optic nerve (C72.3) with the central nervous system tumours. |  | Milman 2023, PDF p. 12; Pfister 2022, PDF p. 12 |
| Only a region around the eye (periorbital or periocular), with no part of the eye or eyelid named | go | → `site_capture` (recapture site) | A site named only by a prefix such as peri- is not an ICD-O site. The next screen asks which tissue the report names; with none, the site is head, face or neck (C76.0). |  | ICD-O-3.1 manual, PDF p. 1 |
| A deposit (metastasis) of a tumour that began elsewhere, or a tumour that grew into the eye or orbit from a neighbouring part | go | → `ey_deposit` (recapture site) | A tumour that began elsewhere is recorded at the site where it began. |  | Milman 2023, PDF p. 17; ICD-O-3.1 manual, PDF p. 2 |

### `ey_surface_histology` (histology_subclassification)

**Question:** What does the histology report call the tumour of the conjunctiva or cornea?

**Hint:** Use the report's own term. Squamous intraepithelial neoplasia, dysplasia and carcinoma in situ have not invaded and are not registrable.

| Option | Outcome | Records | Reason | Recognition aid | Source |
|---|---|---|---|---|---|
| A carcinoma the report names, such as squamous cell carcinoma, adenosquamous carcinoma or mucoepidermoid carcinoma | go | → `ey_carcinoma_other` | The next screen lists the carcinomas. |  | Milman 2023, PDF p. 3; Milman 2023, PDF p. 7 |
| Carcinoma, type not stated | code | 8010/3, basis 7 | Recorded as Carcinoma, NOS (8010/3). |  | ICD-O-3.1 manual, PDF p. 6 |
| Sebaceous carcinoma | go | → `sk_histology` | Recorded at the skin of the eyelid (C44.1) with the skin carcinomas: the WHO classification of eye tumours places sebaceous carcinoma with the eyelid tumours. |  | Milman 2023, PDF p. 7; Milman 2023, PDF p. 9 |
| Melanoma | go | → `mel_conjunctiva` | Melanoma is recorded with the melanomas; the next screen asks about it. |  | Milman 2023, PDF p. 3 |
| Lymphoma | refer | Group 2 | Lymphoma is recorded in Group II, at the part of the eye or orbit where it arose. |  | Milman 2023, PDF p. 16 |
| Squamous intraepithelial neoplasia, high grade, or moderate or severe dysplasia | exclude | 8077/2 | Squamous intraepithelial neoplasia, high grade (8077/2) has not invaded and is not registrable as a malignant tumour. |  | Milman 2023, PDF p. 3 |
| Squamous intraepithelial neoplasia, low grade, or mild dysplasia | exclude | 8077/0 | Squamous intraepithelial neoplasia, low grade (8077/0) is not malignant. |  | Milman 2023, PDF p. 3 |
| Squamous cell carcinoma in situ, with no invasion | exclude | 8070/2 | Squamous cell carcinoma in situ, NOS (8070/2) has not invaded and is not registrable as a malignant tumour. |  | ICD-O-3.1 manual, PDF p. 6 |
| Squamous papilloma | exclude | 8052/0 | Squamous cell papilloma, NOS (8052/0) is benign. |  | Milman 2023, PDF p. 3 |
| Oncocytoma | exclude | 8290/0 | Oxyphilic adenoma (8290/0) is benign; ICD-O-3.2 gives Oncocytoma as its synonym. |  | Milman 2023, PDF p. 3 |
| A deposit of a tumour that began elsewhere | go | → `ey_deposit` (recapture site) | A tumour that began elsewhere is recorded at the site where it began. |  | Milman 2023, PDF p. 17 |

### `ey_lacrimal_histology` (histology_subclassification)

**Question:** What does the histology report call the tumour of the lacrimal gland or the tear drainage passages?

**Hint:** Use the report's own term. Pleomorphic adenoma, oncocytoma, myoepithelioma, papillomas and intraductal carcinoma are not registrable.

| Option | Outcome | Records | Reason | Recognition aid | Source |
|---|---|---|---|---|---|
| A carcinoma the report names, such as adenoid cystic carcinoma, carcinoma ex pleomorphic adenoma or mucoepidermoid carcinoma | go | → `ey_carcinoma_other` | The next screen lists the carcinomas. |  | Milman 2023, PDF p. 12 |
| Carcinoma, type not stated | code | 8010/3, basis 7 | Recorded as Carcinoma, NOS (8010/3). |  | ICD-O-3.1 manual, PDF p. 6 |
| Malignant mixed tumour, or malignant pleomorphic adenoma, and no carcinoma is named | refer | Group 12 | A malignant mixed tumour (8940/3) is recorded with the other specified malignant tumours (Group XII). A carcinoma ex pleomorphic adenoma is a carcinoma: choose it from the carcinoma list instead. |  | ICD-O-3.1 manual, PDF p. 2 |
| Melanoma of the lacrimal sac or duct | go | → `mel_eye` | Melanoma is recorded with the melanomas; the next screen asks about it. |  | Milman 2023, PDF p. 12 |
| Lymphoma | refer | Group 2 | Lymphoma is recorded in Group II, at the part of the eye or orbit where it arose. |  | Milman 2023, PDF p. 16 |
| Pleomorphic adenoma | exclude | 8940/0 | Pleomorphic adenoma (8940/0) is benign. |  | Milman 2023, PDF p. 12; Milman 2023, PDF p. 13 |
| Oncocytoma | exclude | 8290/0 | Oxyphilic adenoma (8290/0) is benign; ICD-O-3.2 gives Oncocytoma as its synonym. |  | Milman 2023, PDF p. 12 |
| Myoepithelioma | exclude | 8982/0 | Myoepithelioma, NOS (8982/0) is benign. |  | Milman 2023, PDF p. 12 |
| Intraductal carcinoma, with no invasion | exclude | 8500/2 | Intraductal carcinoma, noninfiltrating, NOS (8500/2) has not invaded and is not registrable as a malignant tumour. |  | Milman 2023, PDF p. 12 |
| Squamous papilloma | exclude | 8052/0 | Squamous cell papilloma, NOS (8052/0) is benign. |  | Milman 2023, PDF p. 12 |
| Inverted papilloma | exclude | 8121/1 | Sinonasal papilloma, inverted (8121/1) is not malignant. |  | Milman 2023, PDF p. 12 |
| A deposit of a tumour that began elsewhere | go | → `ey_deposit` (recapture site) | A tumour that began elsewhere is recorded at the site where it began. |  | Milman 2023, PDF p. 17 |

### `ey_intraocular_histology` (histology_subclassification)

**Question:** What does the histology report call the tumour inside the eye?

**Hint:** Use the report's own term. An adenoma of the ciliary body or of the retinal pigment epithelium is not malignant.

| Option | Outcome | Records | Reason | Recognition aid | Source |
|---|---|---|---|---|---|
| Retinoblastoma, or retinocytoma (retinoma) | refer | Group 5 | Retinoblastoma is recorded in Group V, which registers it on an eye examination or imaging, because a biopsy of the eye is usually avoided. |  | Pfister 2022, PDF p. 12; Milman 2023, PDF p. 8 |
| Medulloepithelioma (diktyoma), including teratoid medulloepithelioma | refer | Group 4 | Medulloepithelioma of the eye is recorded in Group IV. |  | Milman 2023, PDF p. 10; Milman 2023, PDF p. 11; Pfister 2022, PDF p. 12 |
| Melanoma of the choroid, ciliary body or iris | go | → `mel_eye` | Melanoma is recorded with the melanomas; the next screen asks about it. |  | Milman 2023, PDF p. 10 |
| Lymphoma, including vitreoretinal or choroidal lymphoma | refer | Group 2 | Lymphoma is recorded in Group II, at the part of the eye or orbit where it arose. |  | Milman 2023, PDF p. 16 |
| Adenocarcinoma of the ciliary body epithelium or of the retinal pigment epithelium, or another carcinoma the report names | go | → `ey_carcinoma_other` | The next screen lists the carcinomas. | Reports describe cuboidal to epithelioid epithelial cells with basement membrane material that stains with periodic acid-Schiff, and PAX8 staining. | Milman 2023, PDF p. 10; Milman 2023, PDF p. 11 |
| Carcinoma, type not stated | code | 8010/3, basis 7 | Recorded as Carcinoma, NOS (8010/3). |  | ICD-O-3.1 manual, PDF p. 6 |
| Adenoma of the ciliary body epithelium or of the retinal pigment epithelium | exclude | 8140/0 | Adenoma, NOS (8140/0) is benign. |  | Milman 2023, PDF p. 10 |
| A deposit of a tumour that began elsewhere | go | → `ey_deposit` (recapture site) | A tumour that began elsewhere is recorded at the site where it began. |  | Milman 2023, PDF p. 17 |

### `ey_orbit_histology` (histology_subclassification)

**Question:** What does the histology report call the tumour?

**Hint:** Use the report's own term.

| Option | Outcome | Records | Reason | Recognition aid | Source |
|---|---|---|---|---|---|
| A carcinoma the report names | go | → `ey_carcinoma_other` | The next screen lists the carcinomas. |  |  |
| Carcinoma, type not stated | code | 8010/3, basis 7 | Recorded as Carcinoma, NOS (8010/3). |  | ICD-O-3.1 manual, PDF p. 6 |
| Rhabdomyosarcoma, or another soft-tissue sarcoma | refer | Group 9 | Soft-tissue sarcomas are recorded in Group IX. |  | Milman 2023, PDF p. 20 |
| Myeloid sarcoma (granulocytic sarcoma, chloroma) | refer | Group 1 | Myeloid sarcoma is recorded with the leukaemias in Group I, at the orbit where it arose. |  | Milman 2023, PDF p. 16; ICD-O-3.1 manual, PDF p. 2 |
| Lymphoma | refer | Group 2 | Lymphoma is recorded in Group II, at the part of the eye or orbit where it arose. |  | Milman 2023, PDF p. 16 |
| Langerhans cell histiocytosis | refer | Group 2 | Langerhans cell histiocytosis is recorded in Group II. |  | Milman 2023, PDF p. 16 |
| Teratoma or yolk sac tumour | refer | Group 10 | Germ cell tumours are recorded in Group X. |  | Milman 2023, PDF p. 15 |
| Melanoma | go | → `mel_eye` | Melanoma is recorded with the melanomas; the next screen asks about it. |  | Milman 2023, PDF p. 15 |
| Retinoblastoma, including retinoblastoma that has spread into the orbit | refer | Group 5 | Retinoblastoma is recorded in Group V, which registers it on an eye examination or imaging, because a biopsy of the eye is usually avoided. |  | Pfister 2022, PDF p. 12 |
| A tumour of the bone of the orbital wall, such as Ewing sarcoma | refer | Group 8 (recapture site) | A bone tumour is recorded at the bone where it arose, in Group VIII. |  | Milman 2023, PDF p. 21 |
| A deposit (metastasis) of a tumour that began elsewhere, or a tumour that grew in from a neighbouring part | go | → `ey_deposit` (recapture site) | A tumour that began elsewhere is recorded at the site where it began. |  | Milman 2023, PDF p. 17 |

### `ey_carcinoma_other` (histology_subclassification)

**Question:** Which carcinoma does the report name?

**Hint:** Type part of the report's term to filter the list. If the report names two carcinoma types for one tumour and no single term covers both, choose the one with the higher code number.

| Option | Outcome | Records | Reason | Recognition aid | Source |
|---|---|---|---|---|---|
| Squamous cell carcinoma | code | 8070/3, basis 7 | Recorded as Squamous cell carcinoma, NOS (8070/3). | Reports describe irregular islands and bands of invasive squamous cells. | Milman 2023, PDF p. 3; Milman 2023, PDF p. 5 |
| Adenosquamous carcinoma | code | 8560/3, basis 7 | Recorded as Adenosquamous carcinoma (8560/3). | Reports describe squamous cell carcinoma together with true glands of adenocarcinoma whose cells hold mucin. | Milman 2023, PDF p. 7; Milman 2023, PDF p. 5; ICD-O-3.1 manual, PDF p. 11 |
| Mucoepidermoid carcinoma | code | 8430/3, basis 7 | Recorded as Mucoepidermoid carcinoma (8430/3). | Reports describe squamous (epidermoid) cells, intermediate cells and mucous cells in varying proportions. | Milman 2023, PDF p. 14 |
| Carcinoma ex pleomorphic adenoma | code | 8941/3, basis 7 | Recorded as Carcinoma ex pleomorphic adenoma (8941/3), at the site the report names. The salivary gland site ICD-O-3.2 prints beside this term applies only when a report names no site. | Reports describe a carcinoma beside areas of pleomorphic adenoma, or at the site of an earlier pleomorphic adenoma. | Milman 2023, PDF p. 13; ICD-O-3.1 manual, PDF p. 2 |
| Adenoid cystic carcinoma | code | 8200/3, basis 7 | Recorded as Adenoid cystic carcinoma (8200/3). | Reports describe ductal and myoepithelial cells in tubular, cribriform and solid patterns, often with perineural invasion. | Milman 2023, PDF p. 13 |
| Ductal adenocarcinoma of the lacrimal gland (salivary duct-type carcinoma) | code | 8500/3, basis 7 | Recorded as Infiltrating duct carcinoma, NOS (8500/3); ICD-O-3.2 lists Duct adenocarcinoma, NOS under this code. The breast site printed beside the preferred term does not apply when the report names the lacrimal gland. | Reports describe a high-grade adenocarcinoma resembling salivary duct carcinoma or ductal carcinoma of the breast, often with comedonecrosis. | Milman 2023, PDF p. 12; Milman 2023, PDF p. 14; ICD-O-3.1 manual, PDF p. 2 |
| Secretory carcinoma | code | 8502/3, basis 7 | Recorded as Secretory carcinoma (8502/3). | Reports describe a tumour with vacuolated secretory material that stains for S100 protein and mammaglobin, often with an ETV6 gene rearrangement. | Milman 2023, PDF p. 14 |
| Epithelial-myoepithelial carcinoma | code | 8562/3, basis 7 | Recorded as Epithelial-myoepithelial carcinoma (8562/3). | Reports describe inner ductal cells surrounded by outer, usually clear, myoepithelial cells. | Milman 2023, PDF p. 14 |
| Acinic cell carcinoma | code | 8550/3, basis 7 | Recorded as Acinar cell carcinoma (8550/3); ICD-O-3.2 gives Acinic cell adenocarcinoma as its synonym. | Reports describe tumour cells with serous acinar differentiation and zymogen granules. | Milman 2023, PDF p. 15 |
| Lymphoepithelial carcinoma | code | 8082/3, basis 7 | Recorded as Lymphoepithelial carcinoma (8082/3). |  | Milman 2023, PDF p. 12 |
| Adenocarcinoma, including adenocarcinoma of the ciliary body epithelium or of the retinal pigment epithelium | code | 8140/3, basis 7 | Recorded as Adenocarcinoma, NOS (8140/3). |  | Milman 2023, PDF p. 12; Milman 2023, PDF p. 10 |
| Carcinoma, type not stated | code | 8010/3, basis 7 | Recorded as Carcinoma, NOS (8010/3). |  | ICD-O-3.1 manual, PDF p. 6 |

### `ey_deposit` (site_resolution)

**Question:** Which tumour does the report say has spread to the eye or orbit?

**Hint:** A deposit is recorded at the site where the tumour began. The next screens ask about that tumour.

| Option | Outcome | Records | Reason | Recognition aid | Source |
|---|---|---|---|---|---|
| Neuroblastoma | refer | Group 4 (recapture site) | Neuroblastoma is recorded in Group IV, at the site where it began. |  |  |
| A carcinoma or melanoma of another organ, or of the eyelid, sinuses or nasal cavity | go | → `site_capture` (recapture site) | The next screen asks where the carcinoma or melanoma began. |  | Milman 2023, PDF p. 17 |
| A soft-tissue sarcoma, including rhabdomyosarcoma | refer | Group 9 (recapture site) | Soft-tissue sarcomas are recorded in Group IX, at the site where they began. |  |  |
| A bone sarcoma, such as Ewing sarcoma | refer | Group 8 (recapture site) | Bone sarcomas are recorded in Group VIII, at the bone where they began. |  | Milman 2023, PDF p. 21 |
| Leukaemia | refer | Group 1 (recapture site) | Leukaemia is recorded in Group I. |  |  |
| Lymphoma | refer | Group 2 (recapture site) | Lymphoma is recorded in Group II. |  |  |
| A tumour of the brain or its coverings | refer | Group 3 (recapture site) | Tumours of the brain and its coverings are recorded in Group III. |  |  |
| Nephroblastoma (Wilms tumour), or another kidney tumour | refer | Group 6 (recapture site) | Kidney tumours are recorded in Group VI. |  |  |
| A germ cell tumour | refer | Group 10 (recapture site) | Germ cell tumours are recorded in Group X. |  |  |
| The primary is not known and has not been found | go | → `site_capture_unknown_primary` (recapture site) | The next screen records an unknown primary site. |  |  |

**The picker’s long tail.** `ey_carcinoma_other` lists the Milman entities first. Below them the controller appends every other current XIf9 code from the Group XI inventory: 164 of its 174 XIf9 records, leaving out the ten whose every /3 term is [obs] (8042, 8124, 8130, 8141, 8245, 8251, 8440, 8450, 8508, 8512). Two Milman names have no option of their own: "squamous cell carcinoma with mucinous differentiation" waits on the registrar (section 8), and "other salivary gland-type carcinomas of the lacrimal drainage system" (Milman 2023, PDF p. 12) is a heading the long tail covers.

**Not on any screen.** Oncocytic carcinoma of the lacrimal gland (8290/3) waits on the registrar: WHO Eye5 removed it as obsolete (Milman 2023, PDF p. 15), while ICD-O-3.2 keeps 8290/3 current and the XIf9 inventory would put it in the picker.

## 4. Immunohistochemistry rules

Held back: no checklist node is proposed. Every lacrimal and intraocular carcinoma is a picker entry, the pathologist names the type in the report, and the type does not need a marker panel to reach its code. The rules below are the evidence should the registrar promote the lacrimal carcinomas to options; the checklist fallback would then be Carcinoma, NOS (8010/3). Markers come from Milman 2023 Table 13 (PDF pp. 13–15) and Table 10 (PDF p. 11). Milman gives most of them as supportive, not essential: only secretory carcinoma has an immunohistochemistry result among its essential criteria (PDF p. 14).

| Panel | Positive | Negative | Code | Source |
|---|---|---|---|---|
| `ey_lacrimal_ihc` | MYB, KIT |  | 8200/3 | Milman 2023, PDF p. 13 |
| `ey_lacrimal_ihc` | S100 protein, SOX10, mammaglobin, NTRK (pan-TRK) | CK5, p63, p40, androgen receptor | 8502/3 | Milman 2023, PDF p. 14 |
| `ey_lacrimal_ihc` | p63, p40 | S100 protein, SOX10 | 8430/3 | Milman 2023, PDF p. 14 |
| `ey_lacrimal_ihc` | pancytokeratin and CK7 (inner cells), p63, SMA, calponin and S100 protein (outer myoepithelial cells) |  | 8562/3 | Milman 2023, PDF p. 14 |
| `ey_lacrimal_ihc` | NR4A3 or NR4A2, DOG1, SOX10 | p63, S100 protein, mammaglobin, pan-TRK | 8550/3 | Milman 2023, PDF p. 15 |
| `ey_lacrimal_ihc` | CK7, androgen receptor, GCDFP-15, HER2 | SMA, p63, calponin, ER, PR, PSA | 8500/3 | Milman 2023, PDF p. 14 |
| `ey_lacrimal_ihc` | PLAG1 and HMGA2 in the pleomorphic adenoma component, p53 and c-MYC in the carcinoma |  | 8941/3 | Milman 2023, PDF p. 13 |
| `ey_intraocular_ihc` | PAX8 | melanocytic markers | 8140/3 | Milman 2023, PDF p. 11 |
| `ey_intraocular_ihc` | LIN28A, PAX8 |  | 9501/3 | Milman 2023, PDF p. 11 |

The intraocular rule for 9501 is a referral to Group IV, not a Group XI code: medulloepithelioma expresses LIN28A and PAX8, which separates it from retinoblastoma (Milman 2023, PDF p. 11). PAX8 and a basement membrane that stains with periodic acid-Schiff separate an adenocarcinoma of the ciliary body epithelium from melanoma (Milman 2023, PDF p. 11).

## 5. Registration without tissue

| Evidence on file | Code | Basis |
|---|---|---|
| A referral letter or clinical note that names a malignant tumour of the eye, lacrimal gland or orbit | 8000/3 | 1 |
| An imaging report (ultrasound, computed tomography or magnetic resonance imaging) that shows the tumour | 8000/3 | 2 |

These rows follow the registrar’s brief (Visser 2023, Front Oncol 13:1250549). Visser is not among this part’s files, so the rows carry no quotation. Visser Table 4 names no eye entity, so the gate has no tumour-marker answer. ICCC-2017 places 8000/3 at C69 in XIIb: a tissue-free eye case leaves Group XI.

Retinoblastoma is the exception the gate must catch first. Biopsy is usually avoided (Milman 2023, PDF p. 11), and Group V registers retinoblastoma on eye examination and imaging. The gate’s first option refers any file that names retinoblastoma or retinocytoma to Group V before the 8000/3 answers.

## 6. Laboratory tests

None. Milman 2023 gives no serum or urine test a diagnostic role for any eye carcinoma. The only fluid test it names is the liquid biopsy of cell-free DNA from aqueous humour or plasma, for retinoblastoma (PDF p. 8), which belongs to Group V. No laboratory screen is proposed for this part.

## 7. Rules A to K

Source: ICD-O-3.1 manual, section 4 (PDF p. 1 = printed p. 14).

| Rule | Applies | Where it reaches the clerk |
|---|---|---|
| A | yes | ey_site options: 'Eyelid, including the eyelid margin' carries the reason that an eyelid tumour is recorded at the skin of the eyelid (C44.1) and hands the case to the skin tree; 'Eye, part not stated' records C69.9. |
| B | yes | ey_site option 'Only a region around the eye (periorbital or periocular)': its reason states that a prefix site is not an ICD-O site and the next screen asks the tissue, falling back to C76.0. |
| C | yes | ey_site option 'More than one of these parts, and the report cannot say where the tumour began' records C69.8; the reason states the point of origin cannot be determined. |
| D | yes | Referral reasons for lymphoma (ey_surface, ey_lacrimal, ey_intraocular, ey_orbit) state that Group II records the lymphoma at the part of the eye or orbit where it arose. |
| E | yes | ey_orbit_histology option 'Myeloid sarcoma': the reason states it is recorded in Group I at the orbit, not at bone marrow. |
| F | yes | Exclusion option labels and reasons on the surface and lacrimal screens name the in situ, low-grade and benign behaviours (8077/2, 8077/0, 8070/2, 8500/2, 8940/0). The lacrimal option 'Malignant mixed tumour, or malignant pleomorphic adenoma' codes the stated malignant behaviour (8940/3) and refers it to Group XII. |
| G | no | No eye code depends on grade and no screen in this part offers two grades. Mucoepidermoid carcinoma is graded in the report, but every grade records 8430/3. |
| H | yes | Reasons on the picker options for carcinoma ex pleomorphic adenoma (8941/3, printed site C07/C08) and ductal adenocarcinoma (8500/3, printed site C50) state that the stated lacrimal site wins. The sebaceous carcinoma option (printed site C44) sends the case to the eyelid. Retinoblastoma (printed site C69.2) refers to Group V. The deposit option on every screen applies the clause that the site is used only after a metastasis is ruled out. |
| J | no | Every Milman eye term matches an ICD-O-3.2 term or synonym directly (checked in icdo32.sqlite); no word roots need reordering. ICD-O lists the combination 'mixed adenocarcinoma and squamous cell carcinoma' at 8560/3 itself. |
| K | yes | Hint on ey_carcinoma_other, the screen that offers both codes: 'If the report names two carcinoma types for one tumour and no single term covers both, choose the one with the higher code number.' Adenosquamous carcinoma needs no Rule K because 8560/3 covers both components. Squamous cell carcinoma with mucinous differentiation is a registrar question (8070/3 by the WHO name, 8480/3 by Rule K). |

Pages: Rule A, PDF p. 1; Rule B, PDF p. 1; Rule C, PDF pp. 1–2; Rules D to H, PDF p. 2, with Rule H’s site-associated table on PDF p. 10 (8500/3 lists C50 with other primary sites; 9510/3 lists C69.2) and the pseudo-topographic terms on PDF p. 11; Rules J and K, PDF p. 3 and PDF p. 11. ICD-O-3.2 prints the site beside 8410/3 Sebaceous carcinoma (C44._), 8941/3 Carcinoma ex pleomorphic adenoma (C07._, C08._), 8500/3 Infiltrating duct carcinoma, NOS (C50._) and 9510/3 Retinoblastoma, NOS (C69.2); its synonym Duct adenocarcinoma, NOS carries no site. There is no Rule I.

## 8. Code currency

| Code | Finding | What the tree does |
|---|---|---|
| 8410/3 | Currency check section 4: REDCap label 'Sebaceous adenocarcinoma' is a synonym; ICD-O-3.2 preferred term is Sebaceous carcinoma. | Not output by the eye tree (sent to the eyelid skin tree); the skin tree carries the preferred term. REDCap-side list. |
| 8941/3 | Currency check section 4: REDCap label 'Carcinoma in pleomorphic adenoma' is a synonym; ICD-O-3.2 preferred term is Carcinoma ex pleomorphic adenoma. | The picker option names Carcinoma ex pleomorphic adenoma (8941/3). REDCap-side list. |
| 8502/3 | Currency check section 4: REDCap label 'Secretory carcinoma of breast' is not an ICD-O-3.2 term; the preferred term is Secretory carcinoma. | The picker option names Secretory carcinoma (8502/3). REDCap-side list: at the lacrimal gland the REDCap label names the wrong organ. |
| 8077/2 | Currency check section 5: REDCap offers 8077 'Squamous intraepithelial neoplasia, high grade' in XIf; ICD-O-3.2 holds 8077 at /0 and /2 only. | Exclusion on ey_surface_histology (8077/2 and 8077/0). Not built as a code answer. |
| 8010/3 | Not in the currency check: the REDCap XIf consolidated list labels 8010 'Epithelial Tumor, NOS'. ICD-O-3.2 prints Carcinoma, NOS as the preferred term at 8010/3; 'Epithelial tumor, benign' is 8010/0 and 'Epithelial tumor, malignant' is the /3 synonym. | Every 8010/3 answer names Carcinoma, NOS. Add the XIf label to the REDCap-side list. |
| 8290/3 | ICD-O-3.2 keeps 8290/3 current (preferred term Oxyphilic adenocarcinoma; Oncocytic carcinoma a synonym). WHO Eye5 removed oncocytic carcinoma of the lacrimal gland as obsolete (Milman 2023, PDF p. 15). | Registrar question: whether the eye picker holds 8290/3. |
| 8430/1 | ICD-O-3.2 marks Mucoepidermoid tumor (8430/1) [obs]; only 8430/3 Mucoepidermoid carcinoma is current. | No /1 option. A report that says mucoepidermoid tumour is coded from the pathologist's stated behaviour (Rule F). |
| 8200/3 | ICD-O-3.2 marks Cylindroma, NOS and Adenocarcinoma, cylindroid [obs] at 8200/3; Adenoid cystic carcinoma is the current preferred term. | The picker option names Adenoid cystic carcinoma only. |
| 8550/1 | ICD-O-3.2 marks Acinar cell tumor and Acinic cell tumor (8550/1) [obs]. | No /1 option; the picker offers 8550/3 under the preferred term Acinar cell carcinoma. |
| 8500/3 | Milman prints no code for primary ductal adenocarcinoma of the lacrimal gland. ICD-O-3.2 holds no 'salivary duct carcinoma' term; Duct adenocarcinoma, NOS is a synonym at 8500/3, whose preferred term carries the breast site (C50._). | Picker option records 8500/3 with the Rule H reason. Confirm against the WHO Eye5 volume (data gap). |
| XIf9 inventory/3 | 164 of the 174 XIf9 inventory records are current. Ten are wholly [obs] at /3: 8042, 8124, 8130, 8141, 8245, 8251, 8440, 8450, 8508, 8512. | The eye picker's long tail is the 164 current XIf9 codes; the ten [obs] codes never appear (registrar, 8 October 2026). |

The currency check (8 October 2026) names no eye-specific finding beyond 8410, 8941, 8502 and 8077. Each REDCap difference above goes on the REDCap-side list in `docs/TODO.md`; the tool does not test REDCap (standing rule 16).

## 9. Conflicts with other groups

| Other group | Codes | Sites | Issue |
|---|---|---|---|
| 5 | 9510 | C69.0, C69.1, C69.2, C69.3, C69.4, C69.5, C69.6, C69.8, C69.9 | Retinoblastoma is Group V at every eye site and is registered there without tissue, because biopsy is avoided. The eye tree refers it on the evidence gate before the 8000/3 answers; without that option, an imaging-only retinoblastoma would record 8000/3 (XIIb). The router's C69 candidate groups (topography_codes.json) do not yet list Group 11; its note says to add it when Group 11 is built. |
| 4 | 9501, 9502, 9503, 9504 | C69.0-C69.9 | ICCC-2017 places medulloepithelioma at C00-C69 in IVb (behaviour /3 only). Group IV's tree already holds the ciliary body site (op_medulloepithelioma). |
| 3 | 9501, 9502, 9380, 9421 | C72.3 | The optic nerve is C72.3, a central nervous system site: medulloepithelioma there is IIIc3 and optic nerve glioma is IIIb. The eye site screen refers optic nerve tumours to Group III. |
| 12 | 8000 | C69.0, C69.1, C69.2, C69.3, C69.4, C69.5, C69.6, C69.8, C69.9 | Tissue-free registration records 8000/3, and non-typed malignant cytology records 8000/3; ICCC-2017 places 8000/3 at C69 in XIIb, so these cases leave Group XI when the subgroup is computed. |
| 12 | 8940, 8982 | C69.5 | Malignant mixed tumour (8940/3) and myoepithelial carcinoma (8982/3) of the lacrimal gland are XIIa4 at every site, while carcinoma ex pleomorphic adenoma (8941/3) is XIf9. The lacrimal screen refers the malignant mixed tumour wording to Group XII. Myoepithelial carcinoma is not in the Milman list and has no option; a report naming it needs the Group XII tree. |
| 1 | 9930 | C69.6 | Myeloid sarcoma of the orbit is Ib; Group I's tree already holds the orbit (C69.6). Rule E keeps the orbit as its site. |
| 2 | 9590-9699, 9751 | C69.0, C69.1, C69.2, C69.3, C69.4, C69.5, C69.6, C69.8, C69.9 | Ocular adnexal and intraocular lymphomas are Group II; Langerhans cell histiocytosis (9751) is IId. |
| 9 | 8900-8920, 9364 | C69.6 | Orbital rhabdomyosarcoma is IXa. Ewing sarcoma of the orbital soft tissue (C69.6) is IXd2, while Ewing sarcoma of the orbital bone (C41.0) is VIIIc2 (Group 8). |
| 10 | 9071, 9080 | C69.6 | Orbital teratoma and yolk sac tumour are Xb at C69; Group X's tree holds the C69 sites. |
| 8 | 9364 | C41.0 | A tumour of the bone of the orbital wall is recorded at the bone (C41.0), not at the orbit (C69.6). |
| 11 | 8410, 8090, 8247, 8509, 8200 | C44.1, C69.0 | Inside Group XI: eyelid tumours (sebaceous carcinoma, basal cell carcinoma, Merkel cell carcinoma, endocrine mucin-producing sweat gland carcinoma, adenoid cystic carcinoma of the eyelid) are XIe at C44.1. WHO Eye5 removed sebaceous carcinoma from the conjunctiva chapter. Melanoma (8720-8790) at every eye site is XId and goes to the melanoma tree. |

Every referral group was checked in ICCC-2017 for its code at the eye site: 9510 V; 9501–9504 IVb at C00–C69 and IIIc3 at C70–C72; 9421 IIIb; 9930 Ib; 9590 IIe, 9699 IIb2, 9751 IId; 8900 IXa; 9364 IXd2 at C69.6 and VIIIc2 at C40–C41; 9071 and 9080 Xb at C69; 8940 and 8982 XIIa4; 8000 XIIb at C69. The built Group I, IV, V, IX and X trees already hold C69 sites.

## 10. Data gaps

- **A paediatric source for eye carcinomas: conjunctival squamous cell carcinoma (ocular surface squamous neoplasia) in children and adolescents, and lacrimal gland carcinoma (chiefly adenoid cystic carcinoma) in childhood.** Neither Milman 2023 nor Pfister 2022 reports any eye carcinoma in a child, so ruling 1 makes every eye carcinoma a picker entry. With a paediatric report, conjunctival squamous cell carcinoma and lacrimal adenoid cystic carcinoma would become options on their site screens. Candidate: PubMed: 'ocular surface squamous neoplasia children' and 'lacrimal gland adenoid cystic carcinoma childhood adolescence' (for example Tellado MV et al., Ophthalmology 1997, on lacrimal adenoid cystic carcinoma in childhood and adolescence; citation to be verified).
- **The ICD-O codes the WHO Eye5 volume prints for its entities, especially squamous cell carcinoma with mucinous differentiation, primary ductal adenocarcinoma of the lacrimal gland and adenocarcinoma of the ciliary body and retinal pigment epithelium.** Milman 2023 prints no codes; every code here is matched by term in icdo32.sqlite alone (screening file, gap 4). The mucinous-differentiation code is a registrar question until the WHO volume is read. Candidate: WHO Classification of Tumours Editorial Board. Eye and orbit tumours, 5th ed., vol. 13 (IARC 2023), or its online edition.
- **The grades WHO Eye5 uses for conjunctival squamous intraepithelial neoplasia.** Milman names the entity without grades; the exclusion options split it into low grade (8077/0) and high grade (8077/2) from ICD-O-3.2 alone. Candidate: WHO Eye5 chapter on conjunctival squamous intraepithelial neoplasia.
- **ICD-O-3 topography index entries for the caruncle, the retinal pigment epithelium and the optic disc.** Milman groups the caruncle with the conjunctiva and treats optic disc tumours with the optic nerve; no topography index is in this part's files. The site screen assumes conjunctiva (C69.0), retina (C69.2) and optic nerve (C72.3). Candidate: ICD-O-3.2 topography alphabetic index.
- **Visser 2023 (Front Oncol 13:1250549) in this part's files.** The tissue-free rows follow the registrar's brief; they carry no quotation because Visser is not among this part's sources. Table 4 names no eye entity. Candidate: Visser 2023, Tables 2 to 4 (already held by the controller).

### Questions for the registrar

1. A sebaceous carcinoma the report places in the conjunctiva or caruncle itself: record it at the eyelid (C44.1, XIe), where WHO Eye5 now classifies it (Milman 2023, PDF p. 7), or at the stated site, conjunctiva (C69.0, XIf9), as Rule H directs?
2. Squamous cell carcinoma with mucinous differentiation of the conjunctiva: 8070/3, following the WHO name (Milman 2023, PDF p. 7), or 8480/3 Mucinous adenocarcinoma, the higher code Rule K gives?
3. Oncocytic carcinoma of the lacrimal gland: WHO Eye5 removed it as obsolete (Milman 2023, PDF p. 15) and ICD-O-3.2 keeps 8290/3 current. Does the eye picker offer 8290/3?
4. If the controller finds a paediatric source for conjunctival squamous cell carcinoma or lacrimal gland adenoid cystic carcinoma, are they promoted from the picker to options on their site screens?
