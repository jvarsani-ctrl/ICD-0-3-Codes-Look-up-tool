# Group 11 evidence — XId malignant melanoma, any site

Part `XId_melanoma`. Evidence for the one melanoma tree that every Group 11 site reaches (approach 3, registrar, 8 October 2026). ICCC-2017 places 8720-8780 and 8790 at behaviour 3 in XId at every topography (000-809), so every code this tree records is subgroup XId whatever the site. This file carries the same content as `XId_melanoma.json`; the JSON is the build input.

## 1 Sources

| File | Citation | WHO volume |
|---|---|---|
| `XId-melanoma__ICCR-Invasive-Melanoma-3rd.txt` | International Collaboration on Cancer Reporting (ICCR). Invasive Melanoma Histopathology Reporting Guide, 3rd edition, version 3.0. Sydney: ICCR; January 2026. ISBN 978-1-922324-77-1. | WHO Classification of Skin Tumours, 5th edition, 2025 (Table 1 reproduced with permission) |
| `XId-XIe-skin-melanoma-and-skin-carcinoma__Goldman-Levy-2025.txt` | Goldman-Levy G, Barnhill R, Bastian BC, et al. WHO classification of skin tumours: key updates in the fifth edition. Histopathology 2026;88:555-568. doi:10.1111/his.15562 | WHO Skin Tumours, 5th edition (Skin5) |
| `XId-melanoma-paediatric__Sargen-2026.txt` | Sargen MR. What Is Pediatric Melanoma? Clinical and Genomic Features and the Role of Next-Generation Sequencing in Tumor Classification. Int J Dermatol 2026;65(Suppl 1):S67-S74. doi:10.1111/ijd.70616 | cites WHO Skin Tumours, 5th edition (2025) |
| `XId-melanoma-paediatric__Ferrari-2021.txt` | Ferrari A, et al. Cutaneous melanoma in children and adolescents: The EXPeRT/PARTNER diagnostic and therapeutic recommendations. Pediatr Blood Cancer 2021;68(Suppl 4):e28992. doi:10.1002/pbc.28992 | not a WHO summary |
| `XIf9-eye-XId-ocular-melanoma__Milman-2023.txt` | Milman T, Grossniklaus HE, Goldman-Levy G, et al. The 5th Edition of the WHO Classification of Tumours of the Eye and Orbit. Ocul Oncol Pathol 2023;9(3-4):71-95. doi:10.1159/000530730 | WHO Eye and Orbit Tumours, 5th edition, 2023 |
| `XIf10-nasal-cavity__Thompson-2022.txt` | Thompson LDR, Bishop JA. Update from the 5th Edition of the WHO Classification of Head and Neck Tumors: Nasal Cavity, Paranasal Sinuses and Skull Base. Head Neck Pathol 2022;16(1):1-18. doi:10.1007/s12105-021-01406-5 | WHO Head and Neck Tumours, 5th edition |
| `ALL-paediatric-occurrence__Pfister-2022.txt` | Pfister SM, Reyes-Mugica M, Chan JKC, et al. A Summary of the Inaugural WHO Classification of Pediatric Tumors: Transitioning from the Optical into the Molecular Era. Cancer Discov 2022;12(2):331-355 | WHO Paediatric Tumours, 5th edition, 2022 |
| `RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt` | WHO. International Classification of Diseases for Oncology, 3rd edition, 1st revision (ICD-O-3.1), section 4 Coding guidelines, printed pp. 14-28 | not a tumour classification; the coding manual |

ICCR Invasive Melanoma Table 1 (PDF p. 8) is the only code table in this file set; it reproduces the WHO skin 5th edition (2025) classification. Milman 2023 prints ICD-11 codes, not ICD-O (Milman 2023, PDF p. 4), so eye codes come from `icdo32.sqlite` alone. Thompson 2022 holds no melanoma text: it states that melanocytic tumours have their own chapter in the WHO head and neck 5th edition (Thompson 2022, PDF p. 2). The ICCR dataset covers primary cutaneous melanoma and sends head and neck mucosal melanoma to a separate ICCR dataset (ICCR Invasive Melanoma 2026, PDF pp. 2 and 5).

## 2 Entities

Paediatric column: `common`, `occurs`, `rare` or `not_reported` in the kept sources. Decisions follow the registrar's rulings: paediatric entities are options, other valid /3 codes go in the picker, /0, /1 and /2 entities are exclusions, codes ICD-O-3.2 lacks go to the registrar.

| Entity (WHO or source term) | Code | ICD-O-3.2 term matched (level) | Preferred term at that code | Paediatric | Decision | Pages |
|---|---|---|---|---|---|---|
| Melanoma, not otherwise specified (NOS) | 8720/3 | Malignant melanoma, NOS (Preferred) | Malignant melanoma, NOS | occurs | option | ICCR Invasive Melanoma 2026, PDF p. 8; Pfister 2022, PDF p. 14 |
| Spitz melanoma | 8770/3 | Spitz melanoma (Synonym) | Malignant Spitz tumor | common | option | ICCR Invasive Melanoma 2026, PDF p. 8; Sargen 2026, PDF p. 1; Ferrari 2021, PDF p. 2; Sargen 2026, PDF p. 3 |
| Low-cumulative sun damaged melanoma (including superficial spreading melanoma) | 8743/3 | Low cumulative sun damage melanoma (Preferred) | Low cumulative sun damage melanoma | occurs | option | ICCR Invasive Melanoma 2026, PDF p. 8; Sargen 2026, PDF p. 1; Ferrari 2021, PDF p. 2 |
| Melanoma arising in giant congenital naevus | 8761/3 | Malignant melanoma arising in giant congenital nevus (Preferred) | Malignant melanoma arising in giant congenital nevus | common | option | ICCR Invasive Melanoma 2026, PDF p. 8; Sargen 2026, PDF p. 4; Ferrari 2021, PDF p. 2; Pfister 2022, PDF p. 11 |
| Melanoma arising in blue naevus | 8780/3 | Melanoma arising in blue nevus (Synonym) | Blue nevus, malignant | rare | option | ICCR Invasive Melanoma 2026, PDF p. 8; Sargen 2026, PDF p. 4 |
| Meningeal melanomatosis | 8728/3 | Meningeal melanomatosis (Preferred) | Meningeal melanomatosis | occurs | option | Pfister 2022, PDF p. 18; Goldman-Levy 2025, PDF p. 5 |
| Meningeal melanoma (primary central nervous system melanoma) | 8720/3 | Melanoma, meningeal (Related) | Malignant melanoma, NOS | occurs | option | Pfister 2022, PDF p. 16; Sargen 2026, PDF p. 4; Goldman-Levy 2025, PDF p. 5 |
| Conjunctival melanoma | 8720/3 | Malignant melanoma, NOS (Preferred) | Malignant melanoma, NOS | rare | option | Milman 2023, PDF p. 3; Milman 2023, PDF p. 22; Milman 2023, PDF p. 4 |
| Melanoma, primary site not found (deposit only) | 8720/3 | Malignant melanoma, NOS (Preferred) | Malignant melanoma, NOS | occurs | option | Goldman-Levy 2025, PDF p. 10; ICD-O-3.1 manual, PDF p. 14 |
| Nodular melanoma | 8721/3 | Nodular melanoma (Preferred) | Nodular melanoma | not_reported | picker | ICCR Invasive Melanoma 2026, PDF p. 8 |
| High-cumulative sun damaged melanoma (lentigo maligna melanoma) | 8742/3 | Lentigo maligna melanoma (Preferred) | Lentigo maligna melanoma | not_reported | picker | ICCR Invasive Melanoma 2026, PDF p. 8 |
| Desmoplastic melanoma | 8745/3 | Desmoplastic melanoma, NOS (Preferred) | Desmoplastic melanoma, NOS | not_reported | picker | ICCR Invasive Melanoma 2026, PDF p. 8 |
| Acral melanoma | 8744/3 | Acral melanoma (Preferred) | Acral melanoma | not_reported | picker | ICCR Invasive Melanoma 2026, PDF p. 8; Goldman-Levy 2025, PDF p. 9 |
| Mucosal melanoma | 8720/3 | Malignant melanoma, NOS (Preferred) | Malignant melanoma, NOS | not_reported | picker | ICCR Invasive Melanoma 2026, PDF p. 8; Thompson 2022, PDF p. 2; ICCR Invasive Melanoma 2026, PDF p. 2 |
| Mucosal lentiginous melanoma | 8746/3 | Mucosal lentiginous melanoma (Preferred) | Mucosal lentiginous melanoma | not_reported | picker | ICCR Invasive Melanoma 2026, PDF p. 8 |
| Naevoid melanoma | 8720/3 | Nevoid melanoma (Related) | Malignant melanoma, NOS | not_reported | picker | ICCR Invasive Melanoma 2026, PDF p. 8 |
| Amelanotic melanoma | 8730/3 | Amelanotic melanoma (Preferred) | Amelanotic melanoma | occurs | picker | Ferrari 2021, PDF p. 2 |
| Balloon cell melanoma | 8722/3 | Balloon cell melanoma (Preferred) | Balloon cell melanoma | not_reported | picker | icdo32.sqlite only |
| Malignant melanoma, regressing | 8723/3 | Malignant melanoma, regressing (Preferred) | Malignant melanoma, regressing | not_reported | picker | icdo32.sqlite only |
| Malignant melanoma in junctional naevus | 8740/3 | Malignant melanoma in junctional nevus (Preferred) | Malignant melanoma in junctional nevus | not_reported | picker | icdo32.sqlite only |
| Malignant melanoma in precancerous melanosis | 8741/3 | Malignant melanoma in precancerous melanosis (Preferred) | Malignant melanoma in precancerous melanosis | not_reported | picker | icdo32.sqlite only |
| Choroidal, ciliary body and iris melanoma (uveal melanoma) | 8720/3 | Malignant melanoma, NOS (Preferred) | Malignant melanoma, NOS | not_reported | picker | Milman 2023, PDF p. 10; Milman 2023, PDF p. 9; Milman 2023, PDF p. 4 |
| Epithelioid cell melanoma | 8771/3 | Epithelioid cell melanoma (Preferred) | Epithelioid cell melanoma | not_reported | picker | Milman 2023, PDF p. 10 |
| Spindle cell melanoma, NOS | 8772/3 | Spindle cell melanoma, NOS (Preferred) | Spindle cell melanoma, NOS | not_reported | picker | Milman 2023, PDF p. 10 |
| Spindle cell melanoma, type A | 8773/3 | Spindle cell melanoma, type A (Preferred) | Spindle cell melanoma, type A | not_reported | picker | Milman 2023, PDF p. 10 |
| Spindle cell melanoma, type B | 8774/3 | Spindle cell melanoma, type B (Preferred) | Spindle cell melanoma, type B | not_reported | picker | Milman 2023, PDF p. 10 |
| Mixed epithelioid and spindle cell melanoma | 8770/3 | Mixed epithelioid and spindle cell melanoma (Related) | Malignant Spitz tumor | not_reported | picker | Milman 2023, PDF p. 10 |
| Primary orbital melanoma | 8720/3 | Malignant melanoma, NOS (Preferred) | Malignant melanoma, NOS | not_reported | picker | Milman 2023, PDF p. 15 |
| Melanoma involving the lacrimal drainage system | 8720/3 | Malignant melanoma, NOS (Preferred) | Malignant melanoma, NOS | not_reported | picker | Milman 2023, PDF p. 12 |
| Melanoma in situ | 8720/2 | Melanoma in situ (Preferred) | Melanoma in situ | occurs | exclusion | Ferrari 2021, PDF p. 2; ICCR Invasive Melanoma 2026, PDF p. 9; Milman 2023, PDF p. 5 |
| Spitz naevus | 8770/0 | Spitz nevus, NOS (Synonym) | Epithelioid and spindle cell nevus | common | exclusion | Pfister 2022, PDF p. 14; Goldman-Levy 2025, PDF p. 4 |
| Pigmented spindle cell naevus (Reed naevus) | 8770/0 | Pigmented spindle cell nevus of Reed (Related) | Epithelioid and spindle cell nevus | common | exclusion | Pfister 2022, PDF p. 14 |
| Congenital melanocytic naevus | 8761/0 | Congenital melanocytic nevus, NOS (Preferred) | Congenital melanocytic nevus, NOS | common | exclusion | Pfister 2022, PDF p. 11 |
| Giant congenital melanocytic naevus | 8761/1 | Giant pigmented nevus, NOS (Preferred) | Giant pigmented nevus, NOS | common | exclusion | Pfister 2022, PDF p. 11 |
| Proliferative nodule in congenital naevus (melanocytoma) | 8762/1 | Proliferative nodule in congenital melanocytic nevus (Synonym) | Proliferative dermal lesion in congenital nevus | occurs | exclusion | Goldman-Levy 2025, PDF p. 4; Sargen 2026, PDF p. 4; Sargen 2026, PDF p. 5 |
| Blue naevus and cellular blue naevus | 8780/0 | Blue nevus, NOS (Preferred) | Blue nevus, NOS | occurs | exclusion | Pfister 2022, PDF p. 14 |
| Pigmented epithelioid melanocytoma | 8780/1 | Pigmented epithelioid melanocytoma (Preferred) | Pigmented epithelioid melanocytoma | occurs | exclusion | Goldman-Levy 2025, PDF p. 4; Sargen 2026, PDF p. 5 |
| Melanocytic tumour of uncertain malignant potential (MELTUMP); BAP1-inactivated melanocytoma; atypical cellular blue naevus (cellular blue melanocytoma) | none | none | none | occurs | exclusion | Ferrari 2021, PDF p. 2; Goldman-Levy 2025, PDF p. 5; Goldman-Levy 2025, PDF p. 3 |
| WNT-activated deep penetrating/plexiform melanocytoma (naevus) | 8720/0 | Deep penetrating nevus (Related) | Pigmented nevus, NOS | not_reported | exclusion | Sargen 2026, PDF p. 4 |
| Dysplastic naevus | 8727/0 | Dysplastic nevus (Preferred) | Dysplastic nevus | occurs | exclusion | Sargen 2026, PDF p. 5 |
| Acral naevus | 8744/0 | Acral nevus (Preferred) | Acral nevus | not_reported | exclusion | ICCR Invasive Melanoma 2026, PDF p. 8 |
| Mucosal and genital naevi | 8720/0 | Pigmented nevus, NOS (Preferred) | Pigmented nevus, NOS | not_reported | exclusion | ICCR Invasive Melanoma 2026, PDF p. 8 |
| Conjunctival naevi (junctional, compound, subepithelial, inflamed juvenile, blue) | 8720/0 | Conjunctival nevus (Related) | Pigmented nevus, NOS | common | exclusion | Pfister 2022, PDF p. 12; Milman 2023, PDF p. 3 |
| Conjunctival melanocytic intraepithelial lesion (low or high grade) | none | none | none | not_reported | exclusion | Milman 2023, PDF p. 3; Milman 2023, PDF p. 5 |
| Uveal melanocytoma; melanocytoma of the optic disc | 8726/0 | Melanocytoma, eyeball (Synonym) | Magnocellular nevus | not_reported | exclusion | Milman 2023, PDF p. 10; Milman 2023, PDF p. 12 |
| Meningeal melanocytoma | 8728/1 | Meningeal melanocytoma (Preferred) | Meningeal melanocytoma | occurs | exclusion | Pfister 2022, PDF p. 16 |
| Meningeal melanocytosis | 8728/0 | Meningeal melanocytosis (Preferred) | Meningeal melanocytosis | occurs | exclusion | Pfister 2022, PDF p. 18 |
| Spitz melanocytoma (Atypical Spitz tumour) | 8770/1 | none | none | common | registrar | ICCR Invasive Melanoma 2026, PDF p. 8; Sargen 2026, PDF p. 3; Goldman-Levy 2025, PDF p. 4; Ferrari 2021, PDF p. 2; Ferrari 2021, PDF p. 3 |
| Low-cumulative sun damaged melanoma in situ | 8743/2 | none | none | occurs | registrar | ICCR Invasive Melanoma 2026, PDF p. 8 |
| Dermal melanoma | 8750/3 | none | none | not_reported | registrar | ICCR Invasive Melanoma 2026, PDF p. 8 |
| BAP1-inactivated melanoma; WNT-activated deep penetrating melanoma; melanoma arising in pigmented epithelioid melanocytoma | none | none | none | occurs | registrar | Sargen 2026, PDF p. 4 |
| CRTC1::TRIM11 cutaneous tumour; MED15::ATF1-rearranged tumour | none | none | none | occurs | registrar | Goldman-Levy 2025, PDF p. 11; Sargen 2026, PDF p. 3 |
| Dermal clear cell tumour with melanocytic differentiation (ACTIN::MITF or MITF::CREM) | none | none | none | not_reported | registrar | Goldman-Levy 2025, PDF p. 4 |
| Cellular blue naevus (8790 at behaviour 3) | 8790/3 | none | none | not_reported | not_built | ICCR Invasive Melanoma 2026, PDF p. 8 |
| Clear cell sarcoma (malignant melanoma of soft parts) | 9044/3 | Malignant melanoma of soft parts (Related) | Clear cell sarcoma, NOS | not_reported | refer to Group 9 | Goldman-Levy 2025, PDF p. 4; Goldman-Levy 2025, PDF p. 11 |
| Metastatic melanoma (deposit of a melanoma that began elsewhere) | none | none | none | occurs | refer to Group 11 | Goldman-Levy 2025, PDF p. 10; ICD-O-3.1 manual, PDF p. 2 |

Why each decision was taken, in the order of the table:

- **Melanoma, not otherwise specified (NOS)** (8720/3). The inaugural WHO paediatric classification lists melanoma among paediatric skin tumours. It is the fallback option on every melanoma screen.
- **Spitz melanoma** (8770/3). Spitz melanoma is one of the four WHO melanoma subtypes that occur in children and the commonest histotype before age 10. ICD-O-3.2 also lists Spitzoid melanoma as a synonym at 8770/3; Sargen 2026 calls spitzoid a descriptive term (registrar question).
- **Low-cumulative sun damaged melanoma (including superficial spreading melanoma)** (8743/3). Low cumulative sun damage (superficial spreading) melanoma is a WHO paediatric subtype and the commonest conventional melanoma in adolescents.
- **Melanoma arising in giant congenital naevus** (8761/3). Melanoma arising in a congenital melanocytic naevus develops in large and giant naevi, often in the first decade. ICD-O-3.2 also lists Malignant melanoma in congenital melanocytic nevus as a synonym, so naevus size does not change the code.
- **Melanoma arising in blue naevus** (8780/3). Sargen 2026 reports paediatric cases, most within giant congenital blue naevi. The Preferred term at 8780/3 is [obs] and the synonym is current, so the code is built under the synonym.
- **Meningeal melanomatosis** (8728/3). The paediatric classification lists meningeal melanocytosis and melanomatosis among central nervous system tumour types that mainly occur in children. ICD-O-3.2 prints C70.9 beside the term.
- **Meningeal melanoma (primary central nervous system melanoma)** (8720/3). Meningeal melanoma is a molecular group of paediatric central nervous system tumours, and leptomeningeal melanocytes in a large congenital naevus can transform into primary central nervous system melanoma. ICD-O-3.2 records it at 8720/3 (Related term, C70._).
- **Conjunctival melanoma** (8720/3). WHO Eye and Orbit 5th edition lists conjunctival melanoma; Milman 2023 cites a report of childhood conjunctival melanoma. Milman prints ICD-11 codes, not ICD-O, so the code comes from ICD-O-3.2 alone.
- **Melanoma, primary site not found (deposit only)** (8720/3). A melanoma known only from a deposit is recorded at C80.9. ICCC-2017 XId covers topography 000-809, so it stays in Group XI rather than Group XII. Basis 6 is histology of a metastasis.
- **Nodular melanoma** (8721/3). WHO skin 5th edition prints it (twice, under two families: a printed duplication). No kept source reports it as a paediatric subtype.
- **High-cumulative sun damaged melanoma (lentigo maligna melanoma)** (8742/3). ICD-O-3.2 holds no term for high cumulative sun damage; the WHO entity takes the Lentigo maligna melanoma code. No paediatric report.
- **Desmoplastic melanoma** (8745/3). No paediatric report in the kept sources.
- **Acral melanoma** (8744/3). WHO skin 5th edition holds acral melanoma in its own chapter, and no kept source gives its criteria or a paediatric report.
- **Mucosal melanoma** (8720/3). WHO skin 5th edition codes mucosal melanoma 8720/3. No kept source gives criteria or a paediatric report; head and neck mucosal melanoma sits in a chapter the kept head and neck summary does not cover.
- **Mucosal lentiginous melanoma** (8746/3). No paediatric report in the kept sources.
- **Naevoid melanoma** (8720/3). WHO skin 5th edition codes naevoid melanoma 8720/3. No paediatric report.
- **Amelanotic melanoma** (8730/3). Ferrari 2021 says paediatric melanoma may be amelanotic, which describes its clinical colour. WHO skin 5th edition lists no amelanotic subtype, so the ICD-O-3.2 term goes in the picker and Rule K sends a combined term to the higher code.
- **Balloon cell melanoma** (8722/3). Current ICD-O-3.2 term, not a WHO 5th edition subtype, no paediatric report. Source: icdo32.sqlite only.
- **Malignant melanoma, regressing** (8723/3). Current ICD-O-3.2 term, no paediatric report. Source: icdo32.sqlite only.
- **Malignant melanoma in junctional naevus** (8740/3). Current ICD-O-3.2 term, no paediatric report. Source: icdo32.sqlite only.
- **Malignant melanoma in precancerous melanosis** (8741/3). Current ICD-O-3.2 term, no paediatric report. Source: icdo32.sqlite only.
- **Choroidal, ciliary body and iris melanoma (uveal melanoma)** (8720/3). WHO Eye and Orbit 5th edition lists these melanomas. The paediatric classification's eye list holds no uveal melanoma, and Milman prints no ICD-O code.
- **Epithelioid cell melanoma** (8771/3). Cell-type term used for uveal melanoma. No paediatric report.
- **Spindle cell melanoma, NOS** (8772/3). Cell-type term. No paediatric report.
- **Spindle cell melanoma, type A** (8773/3). ICD-O-3.2 prints C69._ beside it (Rule H). Whether WHO Eye and Orbit 5th edition still uses the spindle A category is not in the kept sources.
- **Spindle cell melanoma, type B** (8774/3). ICD-O-3.2 prints C69._ beside it (Rule H). No paediatric report.
- **Mixed epithelioid and spindle cell melanoma** (8770/3). ICD-O-3.2 files this cell-type term under 8770/3, whose Preferred term is Malignant Spitz tumor (C44._). A uveal melanoma of mixed cell type therefore records 8770/3 (registrar question).
- **Primary orbital melanoma** (8720/3). WHO Eye and Orbit 5th edition lists it. No paediatric report.
- **Melanoma involving the lacrimal drainage system** (8720/3). WHO Eye and Orbit 5th edition lists it. No paediatric report.
- **Melanoma in situ** (8720/2). In situ melanoma occurs in children; behaviour /2 is outside Group XI.
- **Spitz naevus** (8770/0). Benign; the paediatric classification lists it.
- **Pigmented spindle cell naevus (Reed naevus)** (8770/0). Benign; the paediatric classification lists it.
- **Congenital melanocytic naevus** (8761/0). Benign.
- **Giant congenital melanocytic naevus** (8761/1). Behaviour /1 in ICD-O-3.2; outside Group XI.
- **Proliferative nodule in congenital naevus (melanocytoma)** (8762/1). An intermediate nodule within a congenital naevus that often raises concern for melanoma; behaviour /1.
- **Blue naevus and cellular blue naevus** (8780/0). Benign (cellular blue naevus is 8790/0, Cellular blue nevus).
- **Pigmented epithelioid melanocytoma** (8780/1). A melanocytoma, behaviour /1, and a precursor of low cumulative sun damage melanoma in children.
- **Melanocytic tumour of uncertain malignant potential (MELTUMP); BAP1-inactivated melanocytoma; atypical cellular blue naevus (cellular blue melanocytoma)** (none). Intermediate tumours falling short of melanoma. ICD-O-3.2 prints no single code for them; Rule F gives behaviour /1 when the pathologist states uncertain behaviour. Outside Group XI either way.
- **WNT-activated deep penetrating/plexiform melanocytoma (naevus)** (8720/0). Benign or intermediate; outside Group XI.
- **Dysplastic naevus** (8727/0). Benign; a precursor of low cumulative sun damage melanoma. 8727 has no /3 term.
- **Acral naevus** (8744/0). Benign.
- **Mucosal and genital naevi** (8720/0). Benign (ICD-O-3.2 Related term Genital nevus).
- **Conjunctival naevi (junctional, compound, subepithelial, inflamed juvenile, blue)** (8720/0). Benign; the paediatric classification lists conjunctival naevi among paediatric eye tumours.
- **Conjunctival melanocytic intraepithelial lesion (low or high grade)** (none). Not invasive melanoma. Milman prints no ICD-O code; ICD-O-3.2 holds 8741/2 Precancerous melanosis, NOS, and no kept source maps the lesion to it (registrar question).
- **Uveal melanocytoma; melanocytoma of the optic disc** (8726/0). Benign; 8726 has no /3 term.
- **Meningeal melanocytoma** (8728/1). A paediatric central nervous system molecular group, behaviour /1. No ICCC-2017 range takes 8728 at /0 or /1 (registrar question).
- **Meningeal melanocytosis** (8728/0). Behaviour /0; no ICCC-2017 range takes it.
- **Spitz melanocytoma (Atypical Spitz tumour)** (8770/1). ICCR prints 8770/1; ICD-O-3.2 holds no 8770/1. Rule F allows a stated /1 behaviour on an unlisted term. The screen excludes it as non-malignant, naming no ICD-O-3.2 term.
- **Low-cumulative sun damaged melanoma in situ** (8743/2). ICCR prints 8743/2; ICD-O-3.2 holds 8743/3 only. In situ, so the screen excludes it under Melanoma in situ (8720/2).
- **Dermal melanoma** (8750/3). ICCR prints 8750/3; ICD-O-3.2 holds 8750/0 (Dermal nevus) only. A malignant code the tool cannot verify; not offered until the registrar rules.
- **BAP1-inactivated melanoma; WNT-activated deep penetrating melanoma; melanoma arising in pigmented epithelioid melanocytoma** (none). Sargen 2026 places all three among low cumulative sun damage melanomas according to WHO. No kept source prints their code; 8743/3 is the candidate. The picker offers no entry until the registrar rules.
- **CRTC1::TRIM11 cutaneous tumour; MED15::ATF1-rearranged tumour** (none). Tumours with partial melanocytic differentiation that mimic Spitz tumours; WHO skin 5th edition files the CRTC1::TRIM11 tumour among soft tissue tumours. No kept source prints a code.
- **Dermal clear cell tumour with melanocytic differentiation (ACTIN::MITF or MITF::CREM)** (none). New WHO skin 5th edition tumours with no code in the kept sources.
- **Cellular blue naevus (8790 at behaviour 3)** (8790/3). ICCC-2017 XId includes 8790, and ICD-O-3.2 prints only 8790/0 Cellular blue nevus. WHO skin 5th edition names the malignant entity Melanoma arising in blue naevus, current code 8780/3.
- **Clear cell sarcoma (malignant melanoma of soft parts)** (9044/3). A soft tissue sarcoma: ICCC-2017 places 9044 in IXd7 at every site. WHO skin 5th edition separates it from melanoma.
- **Metastatic melanoma (deposit of a melanoma that began elsewhere)** (none). A deposit is coded at its primary: the next screen asks the primary site and the code stays a melanoma code.

## 3 The pathway

The tree opens on the evidence gate, settles where the melanoma arose, and then asks the site's histology question. Every code answer names the ICD-O-3.2 Preferred term in its reason. When the calling tree has already captured a site, the build may enter `mel_site` with that site preselected; the site screen still matters, because the WHO melanoma subtypes are tied to their sites (skin, conjunctiva, uvea, mucosa, meninges). No option on the evidence gate offers a tumour-marker route: Visser 2023 Table 4 lists no melanoma marker.

### `mel_evidence` (document_inventory)

**Question:** What is in the file about this melanoma?

**Hint:** Choose the strongest evidence in the file. An immunohistochemistry or gene report is read with the histology report it belongs to.

| Option | Outcome | Records | Basis | Reason | Recognition aid | Pages |
|---|---|---|---|---|---|---|
| A referral letter or clinical note only | go to `mel_clinical` |  |  |  |  | Ferrari 2021, PDF p. 3 |
| An imaging report only (ultrasound, CT or MRI scan) | code | 8000/3 | 2 | Recorded as Neoplasm, malignant (8000/3). Imaging alone does not show that the tumour is a melanoma. |  |  |
| A cytology report (fine needle aspiration) | go to `mel_cytology` |  |  |  |  | Milman 2023, PDF p. 8; Ferrari 2021, PDF p. 3 |
| A histology report from a biopsy or excision, with or without immunohistochemistry or gene reports | go to `mel_site` |  |  |  |  | Ferrari 2021, PDF p. 3; ICCR Invasive Melanoma 2026, PDF p. 16 |
| An immunohistochemistry or gene report only, with no histology report | not_registrable |  |  | A stain or gene result does not stand in for the histology report. Find the histology report the tests were done on. |  | Sargen 2026, PDF p. 5 |

### `mel_clinical` (clinical_alias)

**Question:** What does the clinical note say?

**Hint:** Possible, suspected or query melanoma is not registrable.

| Option | Outcome | Records | Basis | Reason | Recognition aid | Pages |
|---|---|---|---|---|---|---|
| Melanoma of the skin, stated as the diagnosis | code | 8720/3 | 1 | Recorded as Malignant melanoma, NOS (8720/3) on clinical evidence. Melanoma of the skin may be registered from a clinical diagnosis. |  |  |
| Melanoma at a site other than the skin (eye, mucosa, meninges), stated as the diagnosis | code | 8000/3 | 1 | Recorded as Neoplasm, malignant (8000/3). Only melanoma of the skin is registered as a melanoma from clinical evidence. |  |  |
| Possible, suspected or query melanoma | not_registrable |  |  | A possible or suspected diagnosis is not registrable. Record the case when the diagnosis is stated. |  | Ferrari 2021, PDF p. 2 |

### `mel_cytology` (morphology_only)

**Question:** What does the cytology report call the tumour?

| Option | Outcome | Records | Basis | Reason | Recognition aid | Pages |
|---|---|---|---|---|---|---|
| Melanoma, stated as the diagnosis, in a sample from the primary tumour | code | 8720/3 | 5 | Recorded as Malignant melanoma, NOS (8720/3). A cytology sample does not show the melanoma subtype. |  | Milman 2023, PDF p. 10; Milman 2023, PDF p. 8 |
| Melanoma in a lymph node or another deposit, and the primary melanoma is known | refer to Group 11, asks the primary site |  |  | A deposit is coded at its primary. The next screen asks where the primary melanoma arose. |  | Ferrari 2021, PDF p. 3; ICD-O-3.1 manual, PDF p. 2 |
| Melanoma in a deposit, and the report states no primary melanoma was found | code | 8720/3 | 5 | Recorded as Malignant melanoma, NOS (8720/3). The site is recorded as unknown primary site (C80.9). |  | Goldman-Levy 2025, PDF p. 10 |
| Suspicious for melanoma, or melanoma not excluded | not_registrable |  |  | A suspected diagnosis is not registrable. Record the case when a report states melanoma. |  |  |

### `mel_site` (site_resolution)

**Question:** Where did the melanoma arise?

**Hint:** A melanoma of the arm, leg, trunk, chin or forehead with no tissue named is a melanoma of the skin of that region. A site named with a prefix such as peri- or para- takes the tissue the report names. A melanoma that spans two skin regions with no stated point of origin takes the overlapping-lesion code (.8). ICD-O prints skin (C44) beside many melanoma names: when the report names another site, record that site once the report shows the tumour there is not a deposit.

| Option | Outcome | Records | Basis | Reason | Recognition aid | Pages |
|---|---|---|---|---|---|---|
| Skin, including the eyelid, the skin of the lip, the scalp, the palm, the sole and the nail unit | go to `mel_skin_histology` |  |  |  |  | ICD-O-3.1 manual, PDF p. 4; Milman 2023, PDF p. 9; Goldman-Levy 2025, PDF p. 9 |
| Conjunctiva | go to `mel_conjunctiva` |  |  |  |  | Milman 2023, PDF p. 3 |
| Inside the eye (choroid, ciliary body or iris), the orbit or the lacrimal drainage system | go to `mel_eye` |  |  |  |  | Milman 2023, PDF p. 10; Milman 2023, PDF p. 15; Milman 2023, PDF p. 12 |
| A mucosa: mouth, nasal cavity or sinuses, nasopharynx, anal canal or rectum, vulva, vagina or another mucosa | go to `mel_mucosa` |  |  |  |  | ICCR Invasive Melanoma 2026, PDF p. 8; Thompson 2022, PDF p. 2 |
| The meninges, brain or spinal cord, as the primary site | go to `mel_cns` |  |  |  |  | Goldman-Levy 2025, PDF p. 5; Sargen 2026, PDF p. 4 |
| Deep soft tissue, tendon or aponeurosis, and the report calls the tumour clear cell sarcoma or melanoma of soft parts | refer to Group 9 |  |  | Clear cell sarcoma, NOS (9044/3) is a soft tissue sarcoma, ICCC-3 subgroup IXd. Code it from the Group IX tree. |  | Goldman-Levy 2025, PDF p. 4 |
| A lymph node or another organ holding a deposit of a melanoma that began elsewhere, and the primary melanoma is known | refer to Group 11, asks the primary site |  |  | A deposit is coded at its primary. The next screen asks where the primary melanoma arose. |  | Goldman-Levy 2025, PDF p. 10; ICD-O-3.1 manual, PDF p. 2 |
| A deposit of melanoma, and the report states no primary melanoma was found | code | 8720/3 | 6 | Recorded as Malignant melanoma, NOS (8720/3). The site is recorded as unknown primary site (C80.9). |  | Goldman-Levy 2025, PDF p. 10; ICD-O-3.1 manual, PDF p. 14 |

### `mel_skin_histology` (morphology_only)

**Question:** What does the histology report call the tumour?

**Hint:** If the report names two melanoma types for one tumour, record the type with the higher code number: an amelanotic Spitz melanoma is recorded as Malignant Spitz tumor (8770/3). Record the behaviour the pathologist states.

| Option | Outcome | Records | Basis | Reason | Recognition aid | Pages |
|---|---|---|---|---|---|---|
| Spitz melanoma, malignant Spitz tumour or spitzoid melanoma | code | 8770/3 | 7 | Recorded as Malignant Spitz tumor (8770/3). | The report describes spitzoid cells with an HRAS variant or a kinase fusion such as ALK, ROS1, NTRK1, NTRK3, MET, RET, BRAF or MAP3K8. | ICCR Invasive Melanoma 2026, PDF p. 8; Sargen 2026, PDF p. 3 |
| Melanoma arising in a congenital melanocytic naevus, including a large or giant congenital naevus | code | 8761/3 | 7 | Recorded as Malignant melanoma arising in giant congenital nevus (8761/3). | The report places the melanoma within a large or giant congenital naevus, often in a child under ten. | ICCR Invasive Melanoma 2026, PDF p. 8; Sargen 2026, PDF p. 4 |
| Superficial spreading melanoma, or low cumulative sun damage melanoma | code | 8743/3 | 7 | Recorded as Low cumulative sun damage melanoma (8743/3). | The report names superficial spreading melanoma, the commonest conventional melanoma in adolescents. | ICCR Invasive Melanoma 2026, PDF p. 8; Ferrari 2021, PDF p. 2 |
| Melanoma arising in a blue naevus | code | 8780/3 | 7 | Recorded as Melanoma arising in blue nevus (8780/3). | The report places the melanoma within a blue naevus, in a child most often a giant congenital blue naevus. | ICCR Invasive Melanoma 2026, PDF p. 8; Sargen 2026, PDF p. 4 |
| Melanoma or malignant melanoma, with no type stated | code | 8720/3 | 7 | Recorded as Malignant melanoma, NOS (8720/3). |  | ICCR Invasive Melanoma 2026, PDF p. 8; ICCR Invasive Melanoma 2026, PDF p. 7 |
| Another melanoma type the report names (for example nodular, acral, desmoplastic or lentigo maligna melanoma) | go to `mel_picker` |  |  |  |  | ICCR Invasive Melanoma 2026, PDF p. 8 |
| Melanoma in situ, with no invasion | exclude | 8720/2 |  | Melanoma in situ (8720/2) has behaviour /2. The registry records malignant tumours, behaviour /3, only. | The report confines the melanoma to the epidermis or the adnexal epithelium. | ICCR Invasive Melanoma 2026, PDF p. 9; Ferrari 2021, PDF p. 2 |
| Spitz melanocytoma (atypical Spitz tumour) | exclude |  |  | Not registrable. A Spitz melanocytoma is an intermediate tumour between a Spitz naevus and Spitz melanoma, not a malignant one. The registry records behaviour /3 only. | The report calls the Spitz tumour intermediate, or of uncertain malignancy. | Goldman-Levy 2025, PDF p. 4; Sargen 2026, PDF p. 3; Ferrari 2021, PDF p. 3 |
| Melanocytic tumour of uncertain malignant potential (MELTUMP), a melanocytoma, or an atypical cellular blue naevus | exclude |  |  | Not registrable. These tumours fall short of melanoma, and the registry records behaviour /3 only. | The report lists features suggestive of malignancy but calls them too few to diagnose melanoma. | Ferrari 2021, PDF p. 2; Goldman-Levy 2025, PDF p. 5 |
| Pigmented epithelioid melanocytoma | exclude | 8780/1 |  | Pigmented epithelioid melanocytoma (8780/1) has behaviour /1. The registry records behaviour /3 only. |  | Goldman-Levy 2025, PDF p. 4 |
| Proliferative nodule in a congenital naevus | exclude | 8762/1 |  | Proliferative dermal lesion in congenital nevus (8762/1) has behaviour /1. The registry records behaviour /3 only. | The report describes a nodule within a congenital naevus and states it falls short of melanoma. | Goldman-Levy 2025, PDF p. 4; Sargen 2026, PDF p. 4 |
| A naevus: Spitz, Reed, congenital, blue, cellular blue, dysplastic or acral naevus | exclude |  |  | Not registrable. A naevus is benign, behaviour /0, for example Epithelioid and spindle cell nevus (8770/0). |  | Pfister 2022, PDF p. 14; ICCR Invasive Melanoma 2026, PDF p. 8 |
| Clear cell sarcoma, or malignant melanoma of soft parts | refer to Group 9 |  |  | Clear cell sarcoma, NOS (9044/3) is a soft tissue sarcoma, ICCC-3 subgroup IXd. Code it from the Group IX tree. |  | Goldman-Levy 2025, PDF p. 4 |
| CRTC1::TRIM11 cutaneous tumour, MED15::ATF1-rearranged tumour, or dermal clear cell tumour with melanocytic differentiation | not_registrable |  |  | ICD-O-3.2 holds no code for these tumours. They are listed for the registrar, and the case is not recorded until the registrar rules. |  | Goldman-Levy 2025, PDF p. 11; Sargen 2026, PDF p. 3; Goldman-Levy 2025, PDF p. 4 |

### `mel_conjunctiva` (morphology_only)

**Question:** What does the histology report call the conjunctival tumour?

| Option | Outcome | Records | Basis | Reason | Recognition aid | Pages |
|---|---|---|---|---|---|---|
| Conjunctival melanoma, or melanoma with no type stated | code | 8720/3 | 7 | Recorded as Malignant melanoma, NOS (8720/3). |  | Milman 2023, PDF p. 3; Milman 2023, PDF p. 22 |
| Melanoma in situ of the conjunctiva | exclude | 8720/2 |  | Melanoma in situ (8720/2) has behaviour /2. The registry records malignant tumours, behaviour /3, only. | The report finds melanoma without subepithelial invasion. | Milman 2023, PDF p. 5 |
| Conjunctival melanocytic intraepithelial lesion, low or high grade (primary acquired melanosis) | exclude |  |  | Not registrable. The lesion is intraepithelial, not invasive melanoma, and the registry records behaviour /3 only. |  | Milman 2023, PDF p. 3; Milman 2023, PDF p. 5 |
| Conjunctival naevus: junctional, compound, subepithelial, inflamed juvenile, blue or deep penetrating naevus | exclude | 8720/0 |  | Not registrable. A conjunctival naevus is benign: Pigmented nevus, NOS (8720/0). |  | Pfister 2022, PDF p. 12; Milman 2023, PDF p. 3 |
| Another melanoma type the report names | go to `mel_picker` |  |  |  |  |  |

### `mel_eye` (morphology_only)

**Question:** What does the report call the tumour inside the eye, in the orbit or in the lacrimal drainage system?

| Option | Outcome | Records | Basis | Reason | Recognition aid | Pages |
|---|---|---|---|---|---|---|
| A melanoma: choroidal, ciliary body or iris melanoma, orbital melanoma, or melanoma of the lacrimal drainage system | go to `mel_picker` |  |  |  |  | Milman 2023, PDF p. 10; Milman 2023, PDF p. 9; Milman 2023, PDF p. 15; Milman 2023, PDF p. 12 |
| Uveal naevus, uveal melanocytoma, or melanocytoma of the optic disc | exclude | 8726/0 |  | Not registrable. A melanocytoma of the eye is benign: Magnocellular nevus (8726/0). |  | Milman 2023, PDF p. 10; Milman 2023, PDF p. 12 |

### `mel_mucosa` (morphology_only)

**Question:** What does the histology report call the mucosal tumour?

| Option | Outcome | Records | Basis | Reason | Recognition aid | Pages |
|---|---|---|---|---|---|---|
| Melanoma or malignant melanoma, with no type stated | code | 8720/3 | 7 | Recorded as Malignant melanoma, NOS (8720/3). |  | ICCR Invasive Melanoma 2026, PDF p. 8 |
| Another melanoma type the report names (for example mucosal melanoma or mucosal lentiginous melanoma) | go to `mel_picker` |  |  |  |  | ICCR Invasive Melanoma 2026, PDF p. 8 |
| Melanoma in situ of the mucosa | exclude | 8720/2 |  | Melanoma in situ (8720/2) has behaviour /2. The registry records malignant tumours, behaviour /3, only. |  |  |
| A mucosal or genital naevus | exclude | 8720/0 |  | Not registrable. A naevus is benign: Pigmented nevus, NOS (8720/0). |  | ICCR Invasive Melanoma 2026, PDF p. 8 |

### `mel_cns` (morphology_only)

**Question:** What does the histology report call the melanocytic tumour of the meninges, brain or spinal cord?

| Option | Outcome | Records | Basis | Reason | Recognition aid | Pages |
|---|---|---|---|---|---|---|
| Meningeal melanomatosis | code | 8728/3 | 7 | Recorded as Meningeal melanomatosis (8728/3). |  | Pfister 2022, PDF p. 18 |
| Meningeal melanoma, or primary melanoma of the central nervous system | code | 8720/3 | 7 | Recorded as Malignant melanoma, NOS (8720/3), the code ICD-O-3.2 gives Melanoma, meningeal. | The report may describe the melanoma in a child with a large congenital naevus. | Pfister 2022, PDF p. 16; Sargen 2026, PDF p. 4 |
| Meningeal melanocytoma | exclude | 8728/1 |  | Meningeal melanocytoma (8728/1) has behaviour /1. The registry records behaviour /3 only. |  | Pfister 2022, PDF p. 16 |
| Meningeal melanocytosis | exclude | 8728/0 |  | Meningeal melanocytosis (8728/0) is benign. The registry records behaviour /3 only. |  | Pfister 2022, PDF p. 18 |
| Melanoma that spread to the brain or meninges from a primary elsewhere | refer to Group 11, asks the primary site |  |  | A deposit is coded at its primary. The next screen asks where the primary melanoma arose. |  | ICD-O-3.1 manual, PDF p. 2 |

### `mel_picker` (morphology_only)

**Question:** Which melanoma does the report name?

**Hint:** Type a word from the report into the search box; the search matches the words in any order. Spindle cell melanoma type A and type B are terms for the eye: a spindle cell melanoma of the skin is Spindle cell melanoma, NOS (8772/3).

| Option | Outcome | Records | Basis | Reason | Recognition aid | Pages |
|---|---|---|---|---|---|---|
| Nodular melanoma | code | 8721/3 | 7 | Recorded as Nodular melanoma (8721/3). |  | ICCR Invasive Melanoma 2026, PDF p. 8 |
| Lentigo maligna melanoma (high cumulative sun damage melanoma) | code | 8742/3 | 7 | Recorded as Lentigo maligna melanoma (8742/3). |  | ICCR Invasive Melanoma 2026, PDF p. 8 |
| Desmoplastic melanoma, including desmoplastic neurotropic melanoma | code | 8745/3 | 7 | Recorded as Desmoplastic melanoma, NOS (8745/3). |  | ICCR Invasive Melanoma 2026, PDF p. 8 |
| Acral melanoma, or acral lentiginous melanoma | code | 8744/3 | 7 | Recorded as Acral melanoma (8744/3). |  | ICCR Invasive Melanoma 2026, PDF p. 8 |
| Mucosal melanoma | code | 8720/3 | 7 | Recorded as Malignant melanoma, NOS (8720/3). |  | ICCR Invasive Melanoma 2026, PDF p. 8 |
| Mucosal lentiginous melanoma | code | 8746/3 | 7 | Recorded as Mucosal lentiginous melanoma (8746/3). |  | ICCR Invasive Melanoma 2026, PDF p. 8 |
| Naevoid melanoma | code | 8720/3 | 7 | Recorded as Malignant melanoma, NOS (8720/3). |  | ICCR Invasive Melanoma 2026, PDF p. 8 |
| Amelanotic melanoma | code | 8730/3 | 7 | Recorded as Amelanotic melanoma (8730/3). |  | Ferrari 2021, PDF p. 2 |
| Balloon cell melanoma | code | 8722/3 | 7 | Recorded as Balloon cell melanoma (8722/3). |  |  |
| Regressing melanoma | code | 8723/3 | 7 | Recorded as Malignant melanoma, regressing (8723/3). |  |  |
| Melanoma in a junctional naevus | code | 8740/3 | 7 | Recorded as Malignant melanoma in junctional nevus (8740/3). |  |  |
| Melanoma in precancerous melanosis | code | 8741/3 | 7 | Recorded as Malignant melanoma in precancerous melanosis (8741/3). |  |  |
| Choroidal, ciliary body or iris melanoma (uveal melanoma), cell type not stated | code | 8720/3 | 7 | Recorded as Malignant melanoma, NOS (8720/3). |  | Milman 2023, PDF p. 10; Milman 2023, PDF p. 9 |
| Epithelioid cell melanoma | code | 8771/3 | 7 | Recorded as Epithelioid cell melanoma (8771/3). |  | Milman 2023, PDF p. 10 |
| Spindle cell melanoma, type not stated | code | 8772/3 | 7 | Recorded as Spindle cell melanoma, NOS (8772/3). |  | Milman 2023, PDF p. 10 |
| Spindle cell melanoma, type A (eye) | code | 8773/3 | 7 | Recorded as Spindle cell melanoma, type A (8773/3). |  | Milman 2023, PDF p. 10 |
| Spindle cell melanoma, type B (eye) | code | 8774/3 | 7 | Recorded as Spindle cell melanoma, type B (8774/3). |  | Milman 2023, PDF p. 10 |
| Mixed epithelioid and spindle cell melanoma | code | 8770/3 | 7 | Recorded as Malignant Spitz tumor (8770/3). |  | Milman 2023, PDF p. 10 |
| Primary orbital melanoma | code | 8720/3 | 7 | Recorded as Malignant melanoma, NOS (8720/3). |  | Milman 2023, PDF p. 15 |
| Melanoma of the lacrimal drainage system | code | 8720/3 | 7 | Recorded as Malignant melanoma, NOS (8720/3). |  | Milman 2023, PDF p. 12 |

## 4 Immunohistochemistry rules

None. No kept source gives a marker panel that decides between melanoma codes, and the tree builds no immunohistochemistry checklist. The WHO skin 5th edition sorts melanomas into nine progression pathways (Goldman-Levy 2025, PDF p. 3; ICCR Invasive Melanoma 2026, PDF p. 7), and the subtype is decided by morphology and molecular findings that the pathologist integrates into the named diagnosis. Melanocytic markers do not separate melanoma from its mimics: the CRTC1::TRIM11 cutaneous tumour shows SOX10, S100 protein, melan-A and HMB45 (Goldman-Levy 2025, PDF p. 11), and RNA sequencing is needed to separate CRTC1::TRIM11 and MED15::ATF1 tumours from Spitz tumours (Sargen 2026, PDF p. 3). Sargen 2026 Table 1 (PDF p. 3) lists diffuse PRAME nuclear staining, loss of p16 and a Ki-67 index of 20% or more as reasons to consider sequencing, not as diagnostic rules. A diagnosis of melanoma does not rest on the genetic profile alone (Sargen 2026, PDF p. 5), so a stain or gene report without its histology report is not registrable on the evidence gate.

Group III already routes a meningeal tumour that is melanin-pigmented or positive for HMB-45, Melan-A or SOX10 to Group XI (`group_03_dt.json`, meningeal lesion triage). That referral stays in Group III; `mel_cns` receives it.

## 5 Registration without tissue

| Evidence on file | Records | Basis | Source |
|---|---|---|---|
| A clinical note states melanoma of the skin (C44) as the diagnosis (Visser 2023, Table 3; not in this part's files) | 8720/3 | 1 | Visser 2023 (controller's file; no verbatim cite in this part) |
| A clinical note or an imaging report names melanoma at a site other than the skin (Visser 2023: basis 1 or 2 records 8000/3) | 8000/3 | 2 | Visser 2023 (controller's file; no verbatim cite in this part) |

A clinical note that states melanoma of the skin records Malignant melanoma, NOS (8720/3), basis 1 (Visser 2023 Table 3). Melanoma named only clinically at any other site, or seen only on imaging, records Neoplasm, malignant (8000/3), basis 1 or 2. ICCC-2017 places 8000/3 in XIIb at the skin, eye and unknown primary sites and in IIIf at C70-C72, so these cases leave Group XI (section 9). Possible, suspected or query melanoma is not registrable. Visser 2023 Table 4 lists no marker for melanoma, so no tumour-marker route exists in this tree.

The paediatric sources bear on Table 3. Benign pigmented lesions in children can show alarming, melanoma-like features and the adult ABCDE rule can mislead (Ferrari 2021, PDF p. 2), and an excisional biopsy is required when melanoma is suspected (Ferrari 2021, PDF p. 3). The tree applies Table 3 as ruled and lists the point for the registrar.

Cytology records 8720/3, basis 5: WHO Eye and Orbit 5th edition adds diagnostic cytology for uveal melanocytic tumours (Milman 2023, PDF pp. 8 and 10), and fine needle aspiration samples suspected nodes (Ferrari 2021, PDF p. 3). Cytology does not show the subtype, so it records Malignant melanoma, NOS. A deposit with no primary found records 8720/3 at C80.9; on histology its basis is 6, histology of a metastasis (ICD-O-3.1 manual, PDF p. 14, Table 26).

## 6 Laboratory tests

None. No kept source gives a serum or urine test a diagnostic role in melanoma, and the tree has no laboratory screen.

## 7 Rules A to K

| Rule | Applies | How it reaches the clerk |
|---|---|---|
| A | yes | Hint on mel_site: a melanoma of the arm, leg, trunk, chin or forehead with no tissue named is a melanoma of the skin of that region (ICD-O-3.1 manual, printed p. 17). |
| B | yes | Hint on mel_site: a site named with a prefix such as peri- or para- takes the tissue the report names; melanoma indicates its tissue, so C76 is not used for a melanoma of a named region. |
| C | yes | Hint on mel_site: a melanoma spanning two skin regions with no stated point of origin takes the overlapping-lesion code (.8). |
| D | no | No lymphoma is reached from this tree. |
| E | no | No leukaemia is reached from this tree. |
| F | yes | Exclusion options and their reasons state the behaviour (/0, /1, /2) and that the registry records /3 only; the mel_skin_histology hint tells the clerk to record the behaviour the pathologist states. Spitz melanocytoma takes a stated /1 although ICD-O-3.2 prints no 8770/1. |
| G | no | Melanomas carry no ICD-O grade, and the sixth digit is not built (registrar, 7 October 2026). |
| H | yes | Question and hint on mel_site: ICD-O-3.2 prints C44._ beside 8720 (Nevoid melanoma), 8721-8723, 8730, 8740-8745, 8761, 8770 and 8780, C69._ beside 8773 and 8774, C70._ beside Melanoma, meningeal and C70.9 beside 8728. With no site stated the printed site is used; a named site wins once the report shows the tumour is not a deposit. The mel_picker hint applies it to spindle cell melanoma type A and B. |
| J | yes | mel_picker hint and search: the search matches word roots in any order (melanoma, naevoid and naevoid melanoma find the same entry). |
| K | yes | Hint on mel_skin_histology: two melanoma types named for one tumour record the higher code number (amelanotic Spitz melanoma is 8770/3; acral nodular melanoma is 8744/3). |

Sources: Rule A, ICD-O-3.1 manual PDF pp. 1 and 4 (melanoma and naevus of the arm are skin of arm, C44.6; chin and forehead are skin); Rule B, PDF p. 1; Rule C, PDF p. 2; Rule F, PDF p. 2; Rule H, PDF pp. 2 and 10; Rules J and K, PDF p. 3. Table 23 (PDF p. 10) prints no melanoma row; the site-associated codes Rule H uses for melanoma are the ones `icdo32.sqlite` prints beside each term.

## 8 Code currency

| Code | Finding | What the tree does |
|---|---|---|
| 8720/3 | Current. WHO skin 5th edition codes melanoma NOS, mucosal melanoma and naevoid melanoma to 8720/3. REDCap Malignant melanoma, NOS matches. | One entry; option on every screen and picker entries for mucosal, naevoid, uveal, orbital and lacrimal melanoma. |
| 8721/3 | Current. ICCR Invasive Melanoma Table 1 (PDF p. 8) prints Nodular melanoma 8721/3 twice, under two families: a printed duplication. | One picker entry. |
| 8728/3 | Currency check: REDCap label Meningeal melanocytoma is the /1 term; the /3 Preferred term is Meningeal melanomatosis. | Records Meningeal melanomatosis (8728/3); excludes 8728/1 and 8728/0. REDCap relabel goes on the REDCap-side list in docs/TODO.md. |
| 8742/3 | Current. WHO prints High-cumulative sun damaged melanoma (lentigo maligna melanoma); ICD-O-3.2 holds no high cumulative sun damage term. | Picker entry under Lentigo maligna melanoma. |
| 8743/3 | Currency check: REDCap label Superficial spreading melanoma is a Related term; Preferred is Low cumulative sun damage melanoma. | Records the Preferred term; REDCap-side list. |
| 8743/2 | ICCR Table 1 prints Low-cumulative sun damaged melanoma in situ 8743/2; ICD-O-3.2 holds no 8743/2. | Not built; the in situ exclusion uses 8720/2 Melanoma in situ. Registrar item. |
| 8744/3 | Currency check: REDCap label Acral lentiginous melanoma, malignant is a Synonym; Preferred is Acral melanoma. | Picker entry under the Preferred term; REDCap-side list. |
| 8745/3 | Currency check: REDCap label Desmoplastic melanoma, malignant is not an ICD-O-3.2 term; Preferred is Desmoplastic melanoma, NOS. | Picker entry under the Preferred term; REDCap relabel. |
| 8750/3 | ICCR Table 1 prints Dermal melanoma 8750/3; ICD-O-3.2 holds 8750/0 Dermal nevus only. Currency check section 5: REDCap 8750 Intradermal nevus has no malignant form. | Not built; registrar item. |
| 8761/3 | Currency check: REDCap label Malignant melanoma in giant pigmented nevus is a Synonym; Preferred is Malignant melanoma arising in giant congenital nevus. | Records the Preferred term; REDCap-side list. |
| 8770/3 | Currency check: REDCap label Epithelioid and spindle cell nevus is the /0 Preferred term; the /3 Preferred term is Malignant Spitz tumor. A clerk sees a naevus name on the option a Spitz melanoma records. | Records Malignant Spitz tumor (8770/3); REDCap relabel, first on the REDCap-side list. |
| 8770/1 | ICCR Table 1 prints Spitz melanocytoma (Atypical Spitz tumour) 8770/1; ICD-O-3.2 holds 8770/0 and 8770/3 only. | Exclusion with no ICD-O-3.2 term named; registrar item. |
| 8780/3 | Currency check: Preferred term Blue nevus, malignant is [obs]; the Synonym Melanoma arising in blue nevus is current and is the WHO 5th edition name. REDCap label is the [obs] term. | Built under the current synonym; REDCap relabel. |
| 8790/3 | ICCC-2017 XId includes 8790; ICD-O-3.2 prints only 8790/0 Cellular blue nevus (currency check section 5). | Not built; 8790/0 appears inside the naevus exclusion. |
| 8725/0 | Currency check section 5: 8725 Neuronevus, 8726 Magnocellular nevus, 8727 Dysplastic nevus, 8750 Intradermal nevus, 8760 Compound nevus and 8790 Cellular blue nevus have no /3 term. | Not built as codes; 8726/0 and 8727/0 appear as exclusions. Registrar rules whether REDCap keeps them. |
| 8773/3 | Current; ICD-O-3.2 prints C69._ beside 8773 and 8774. | Eye picker entries only; the picker hint routes a skin spindle cell melanoma to 8772/3. |
| 9044/3 | ICD-O-3.2 Related term Malignant melanoma of soft parts (C49._) sits under Clear cell sarcoma, NOS; ICCC-2017 places 9044 in IXd7 at every site. | Referral to Group IX. |

REDCap labels that differ from the ICD-O-3.2 Preferred term (8728, 8743, 8744, 8745, 8761, 8770, 8780) go on the REDCap-side list in `docs/TODO.md`. The tool does not test REDCap (standing rule 16).

## 9 Conflicts with other groups

| Group | Codes | Sites | Issue |
|---|---|---|---|
| 3 | 8720, 8728 | C70.0, C70.1, C70.9, C71.0-C72.9 | The clerk meets primary meningeal melanocytic tumours in the central nervous system. Group III (meningeal lesion triage, group_03_dt.json) already refers every melanin-pigmented or melanocytic meningeal proliferation to Group XI, including meningeal melanocytoma and melanocytosis. XId takes 8720/3 and 8728/3; no ICCC-2017 range takes 8728/0 or 8728/1, so mel_cns excludes them. Group III must keep the referral and add no 8720 or 8728 code. |
| 3 | 8000 | C70.0-C72.9 | A tissue-free melanoma at a central nervous system site records 8000/3, which ICCC-2017 places in IIIf, not Group XI. |
| 12 | 8000 | C44.0-C44.9, C69.0-C69.9, C80.9 | A melanoma recorded from imaging, or from a clinical note at a non-skin site, records 8000/3, which ICCC-2017 places in XIIb at these sites. The case leaves Group XI. |
| 3 | 8720 | C80.9 | Group III's secondary-deposit screen sends a deposit whose primary is not known to Group XII. A melanoma deposit with no primary found records 8720/3 at C80.9, which ICCC-2017 places in XId (topography 000-809). The other groups' deposit screens (III, VII, VIII, IX) need a melanoma exception: melanoma of unknown primary stays in Group XI. |
| 9 | 9044 | C49.0-C49.9, C44.0-C44.9 | Clear cell sarcoma carries the ICD-O-3.2 term Malignant melanoma of soft parts and is IXd7. The melanoma tree refers it to Group IX; Group IX's not-a-sarcoma screen already sends melanoma to Group XI. |
| 9 | none | C44.0-C44.9 | WHO skin 5th edition files the CRTC1::TRIM11 cutaneous tumour among soft tissue tumours of the skin, and Sargen 2026 leaves open whether CRTC1::TRIM11 and MED15::ATF1 tumours are melanoma or clear cell sarcoma variants. No code is printed: registrar. |
| 9 | 9540 | C47.0-C47.9 | Malignant melanotic nerve sheath tumour (ICD-O-3.2 Related term Melanotic MPNST, 9540/3) is IXb2 and is coded from the Group IX tree; it is not a melanoma code. |
| 3 | 9470 | C71.6 | Melanotic medulloblastoma is an ICD-O-3.2 Related term of 9470/3 (IIIc1); melanin in an embryonal tumour does not make it a melanoma. |
| 12 | 9363 | C41.0, C41.1 | Melanotic neuroectodermal tumour of infancy is listed in the paediatric classification (Pfister 2022, PDF p. 14). ICD-O-3.2 holds 9363/0 only, and ICCC-2017 XIIa6 lists 9363 at /3. It is not a melanoma and is not coded from this tree. |

## 10 Data gaps

- **Diagnostic criteria and paediatric occurrence for head and neck mucosal melanoma (nasal cavity, sinuses, nasopharynx, mouth).** Thompson 2022 says only that melanocytic tumours have their own chapter in the WHO head and neck 5th edition (PDF p. 2); it holds no melanoma text. The mucosa screen offers 8720/3 and the picker only. Candidate source: Hernandez-Prera 2022 (the screening's XId head and neck mucosa source), or the ICCR Mucosal Melanomas of the Head and Neck dataset that ICCR Invasive Melanoma cites (PDF p. 2).
- **Criteria and paediatric occurrence for acral melanoma and for non-head-and-neck mucosal melanoma.** Codes come from ICCR Table 1 alone; Goldman-Levy 2025 points to a dedicated acral chapter (PDF p. 9). Both stay picker entries. Candidate source: A summary of the WHO skin 5th edition (2025) acral and mucosal melanocytic chapters.
- **Evidence on uveal melanoma in children, and the WHO Eye and Orbit 5th edition ICD-O codes for uveal melanoma and its cell types.** Milman 2023 prints ICD-11 codes, not ICD-O (PDF p. 4), and the paediatric eye list (Pfister 2022 PDF p. 12) holds no uveal melanoma. Whether spindle cell type A (8773/3) is still melanoma, and whether mixed cell type takes 8770/3, is not settled. Candidate source: WHO Eye and Orbit Tumours 5th edition (2023), uveal melanoma chapter; a paediatric uveal melanoma case series.
- **WHO criteria separating meningeal melanomatosis, meningeal melanoma, melanocytoma and melanocytosis.** The kept sources list the entities (Pfister 2022 PDF pp. 16 and 18) with no criteria, so mel_cns options carry no recognition aid. Candidate source: The WHO central nervous system 5th edition summary already used for Group III (Louis 2021).
- **ICD-O codes for WHO skin 5th edition entities: BAP1-inactivated melanoma, WNT-activated deep penetrating melanoma, melanoma arising in pigmented epithelioid melanocytoma, CRTC1::TRIM11 cutaneous tumour, MED15::ATF1-rearranged tumour, dermal clear cell tumours with melanocytic differentiation, Spitz melanocytoma (8770/1 printed), dermal melanoma (8750/3 printed), conjunctival melanocytic intraepithelial lesion.** These entities have no verifiable ICD-O-3.2 code, so each is a registrar item and none is offered. Candidate source: WHO Classification of Tumours online, Skin Tumours 5th edition (2025) and Eye and Orbit 5th edition entity pages, which print the ICD-O code per entity.
- **The Visser 2023 Table 3 text (melanoma of the skin registered on clinical information, basis 1, C44: 8720/3).** The tissue-free entries and mel_clinical carry no verbatim cite because Visser 2023 is not in this part's files. Candidate source: Visser 2023, Front Oncol 13:1250549, Table 3.
- **An immunohistochemistry panel that decides between melanoma codes.** No kept source gives one. Melanocytic markers do not separate melanoma from its mimics: the CRTC1::TRIM11 tumour stains for SOX10, S100, melan-A and HMB45 (Goldman-Levy 2025 PDF p. 11), and RNA sequencing separates CRTC1::TRIM11 and MED15::ATF1 tumours from Spitz tumours (Sargen 2026 PDF p. 3). The tree builds no immunohistochemistry checklist; the subtype is the one the histology report names.

## Questions for the registrar

1. Spitzoid melanoma. ICD-O-3.2 lists Spitzoid melanoma as a synonym of 8770/3, while Sargen 2026 (PDF p. 1) calls spitzoid a descriptive term that also fits low cumulative sun damage melanoma and melanoma in a congenital naevus. Does a report of spitzoid melanoma record 8770/3, as the Spitz option now does?
2. Clinical-only melanoma of the skin in children. Visser 2023 Table 3 allows 8720/3 on clinical evidence (basis 1); Ferrari 2021 (PDF pp. 2-3) says benign pigmented lesions in children can look like melanoma and requires an excisional biopsy. Does Table 3 apply to ages 0 to 18?
3. Codes ICCR prints and ICD-O-3.2 lacks: 8770/1 Spitz melanocytoma, 8743/2 low cumulative sun damage melanoma in situ, 8750/3 dermal melanoma. 8750/3 is malignant and would be XId. Build it, record dermal melanoma as 8720/3, or hold it?
4. BAP1-inactivated melanoma, WNT-activated deep penetrating melanoma and melanoma arising in a pigmented epithelioid melanocytoma: Sargen 2026 (PDF p. 4) places them among low cumulative sun damage melanomas. Record 8743/3 or 8720/3?
5. Basis of diagnosis 6 (histology of a metastasis, ICD-O-3.1 Table 26) for a melanoma known only from a deposit. The basis list in the build brief has no 6. Use 6?
6. Uveal melanoma of mixed cell type: ICD-O-3.2 files Mixed epithelioid and spindle cell melanoma under 8770/3, whose Preferred term is Malignant Spitz tumor. Confirm 8770/3, and confirm Spindle cell melanoma, type A (8773/3) stays in the picker.
7. Meningeal melanocytoma (8728/1) and meningeal melanocytosis (8728/0) have no ICCC-3 group, and Group III refers them to Group XI. Exclude them as not registrable, as the tree now does?
8. A melanoma recorded from imaging, or clinically at a non-skin site, records 8000/3 and leaves Group XI for XIIb (IIIf in the central nervous system). Accept?
9. CRTC1::TRIM11 cutaneous tumour, MED15::ATF1-rearranged tumour and dermal clear cell tumours with melanocytic differentiation have no code in the kept sources. How are they recorded?
10. Conjunctival melanocytic intraepithelial lesion: is ICD-O-3.2 8741/2 Precancerous melanosis, NOS its code? It is excluded either way.
