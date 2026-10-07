# The ICD-O sixth digit: how registries hold grade (first-pass research)

Desk research of 7 October 2026 for TODO section 32. It asks what the main registry standards require for grade and
differentiation, how they hold it, and what that means for a hospital-based registry. Nothing here is built.

**How to read the evidence.** "Read" means I opened the document and the quoted passage is in it. "Reported" means a web
search summary said it and I did not open the source. Reported claims are marked and are not relied on.

## Finding 1: the sixth digit is not how United States registries hold grade today

The WHO manual in this vault defines grade as the sixth digit of the morphology code (ICD-O-3 first revision, Rule G,
p. 15; section 4.3.4 with Tables 21 and 22, pp. 21-22). Two United States standards followed that model and then left it.

- **SEER, cases diagnosed 2014 to 2017 (read).** "Code the grade shown below (6th digit) for specific histologic terms
  that imply a grade", with the examples "Retinoblastoma, differentiated (9511/31)" and "Retinoblastoma, undifferentiated
  (9512/34)" ([SEER Grade Coding Instructions 2014-2017](https://seer.cancer.gov/tools/grade)).
- **NAACCR, cases diagnosed 2018 and later (read).** The grade became three separate data items: Grade Clinical, Grade
  Pathological and Grade Post Therapy, each with a code set per schema. The manual says they replace "all previous grade
  related data items, including NAACCR Data Item Grade [440] and Collaborative Stage Site-Specific Factors (SSF's)
  (2004-2017)" ([NAACCR Grade Manual v3.3](https://www.naaccr.org/wp-content/uploads/2025/12/Version-3.3.Grade-Manual.pdf)).
  Item 440 was the single grade or differentiation item that preceded them; a search summary describes the change as
  replacing the ICD-O-3 sixth-digit approach (reported, not opened).
- **Commission on Cancer, 2018 (reported).** A search summary of the STORE 2018 manual says the three NAACCR grade items are
  required data items for cancer programs diagnosed from 1 January 2018. I did not open the manual.

So a United States hospital registry records grade in its own item, beside a four-digit histology code, not inside the
morphology string.

## Finding 2: Europe lists grade in its minimum dataset without prescribing a digit

The European Network of Cancer Registries standard dataset (March 2023, Table 1, p. 3) lists "Grade (differentiation grade,
WHO grade, Gleason grade group)" as "According to the latest version of ICD-O and/or WHO". It also lists "Immunophenotype
(T-cell, B-cell, NK-cell)" for lymphoid haematological malignancies. A footnote accepts equivalent systems such as ICD-11
extension codes, and the dataset says registries may collect additional items
([ENCR standard dataset](https://www.encr.eu/sites/default/files/Recommendations/ENCR-Recommendation-standard-dataset_Mar2023.pdf), read).

## Finding 3: retinoblastoma has its own grade table, and it matches our wording

NAACCR schema 00680, Retinoblastoma, Grade 21 (Grade Manual v3.3, pp. 176 to 178, read):

| Code | Meaning |
|---|---|
| 1 | G1: tumour with areas of retinoma (retinocytoma) (fleurettes or neuronal differentiation) |
| 2 | G2: tumour with many rosettes (Flexner-Wintersteiner or Homer Wright) |
| 3 | G3: tumour with occasional rosettes |
| 4 | G4: tumour with poorly differentiated cells without rosettes and/or with extensive areas (more than half of tumour) of anaplasia |
| A to D | generic: well, moderately, poorly differentiated; undifferentiated, anaplastic |
| 9 | grade cannot be assessed (GX) or unknown |

- The rules: "Assign the highest grade from the primary tumor"; "If there are multiple tumors with different grades abstracted
  as one primary, code the highest grade"; "Codes 1-4 take priority over A-D". This is the registrar's decision of 7 October
  2026 (the higher grade governs) written as a registry rule.
- The wording is the College of American Pathologists text, with a proportion ("more than half") only on G4's anaplasia.
  The Pathology Outlines version in your screenshot adds proportions to G1, G2 and G3 that NAACCR does not carry.
- The table has no place for a Mendoza anaplasia grade (mild, moderate, severe). That supports keeping moderate
  anaplasia out of the code where a grade is stated.
- Growth pattern is not part of the grade. Under a separate grade item, a diffuse retinoblastoma (`9513`) with G3 is
  `9513` plus Grade 3, with no conflict. That is my reading: the manual does not mention diffuse. The conflict between
  `9513` and `9512` exists only because the tool records one four-digit code and no grade.

## Finding 4: which of our groups carry a grade a clerk can read

Schemas in the NAACCR Grade Manual v3.3 (read for the first two rows only; the others exist but I did not read their tables):

| Tool group | NAACCR grade schema |
|---|---|
| I Leukaemias, II Lymphomas | None. "No grade fields ... since grade is no longer applicable" (Grade 88, code 8, not applicable). ENCR asks for immunophenotype instead. |
| V Retinoblastoma | Grade 21, read (above). |
| III Central nervous system | Brain and CNS Other, Grade 24.1 (2018 to 2022) and 24.2 (2023 on) |
| IV Neuroblastoma | No neuroblastoma schema found. Adrenal Gland has Grade 26. |
| VI Renal | Kidney-Parenchyma, Grade 18 |
| VII Hepatic | Liver, Grade 02 |
| VIII Bone | Bone, Grade 08 |
| IX Soft tissue | Soft Tissue, Grades 09 and 10; Orbital Sarcoma, Grade 09 |
| X Germ cell | Testis, Grade 98; Ovary, Grade 15 |

The manual states the purpose: "Grade and cell type are important prognostic indicators for many cancers. For some sites,
grade is required to assign the post neoadjuvant clinical stage group."

## Finding 5: grade that is already in the entity's name

The ICD-O-3 term and the digit are two entries that must agree. SEER 2014 to 2017 paired `9511` differentiated with
digit 1 and `9512` undifferentiated with digit 4. The WHO manual gives the same `9511/31` example. NAACCR 2018 and later
keeps the two apart: a four-digit histology and a separate grade code from the schema's own list.

## Finding 6: completeness and use, where the evidence is thin

- **Read:** a population-based registry in Iran (Sima Cancer, 2016 to 2018) reported grade in all 12,000 breast pathology
  reports reviewed ([PMC11469693](https://pmc.ncbi.nlm.nih.gov/articles/PMC11469693)). It is a breast study and says nothing
  about children or about a hospital registry.
- **Reported, not opened:** a search summary of an Australian study of vulval cancer says hospital registries recorded grade
  and treatment where population registries did not. A search summary also gave completeness figures for colorectal and
  brain tumours; I could not tie them to a source and leave them out.
- **Not found:** any paediatric registry study of grade completeness, and any registry statement that grade changed an
  analysis or a treatment audit for a childhood tumour. The childhood sources found concern staging (the Toronto
  Guidelines), not grade.

## What this means for the tool

The research changes the question in TODO section 32. It is not only "should the tool carry the sixth digit?". There are
two models, and the evidence favours the second for a hospital registry:

1. **A sixth digit appended to the morphology code.** This is the WHO manual's model and SEER's up to 2017. The code
   would be `9511/31`. REDCap holds four-digit morphology options and has no grade field in the 1 October 2026 snapshot
   (found by the audit), so a six-digit string needs a dictionary change in `REDCap Registry/`.
2. **A separate grade item with a code set per tumour.** This is NAACCR's model since 2018 and the shape of ENCR's table.
   For retinoblastoma the codes are 1 to 4, A to D and 9. It resolves the diffuse-versus-grade conflict, handles the
   highest-grade rule in one place, and leaves the four-digit code alone. It would be a new row in the output block,
   which the registrar's 6 October 2026 ruling fixed at five rows.

Open questions for the registrar:

- Which model, and for which groups first (retinoblastoma has a complete table; Groups I and II have none).
- Whether grade is Clinical or Pathological or both (NAACCR separates them; a retinoblastoma enucleation is a pathological
  specimen after treatment decisions are made).
- Whether the registry wants the immunophenotype for lymphoid cases (ENCR lists it; NAACCR dropped grade for these).
- Which wording of G1 to G3 the registry reads: the College of American Pathologists and NAACCR text, or the Pathology
  Outlines text with proportions.

## Sources

- NAACCR Grade Manual, version 3.3: <https://www.naaccr.org/wp-content/uploads/2025/12/Version-3.3.Grade-Manual.pdf>
- SEER Grade Coding Instructions 2014-2017: <https://seer.cancer.gov/tools/grade>
- ENCR Recommendation, standard dataset, March 2023: <https://www.encr.eu/sites/default/files/Recommendations/ENCR-Recommendation-standard-dataset_Mar2023.pdf>
- Examining the completeness of breast cancer pathology reports in Iran's population-based cancer registration system: <https://pmc.ncbi.nlm.nih.gov/articles/PMC11469693>
- WHO ICD-O-3 first revision (the vault's extract): Rule G, section 4.3.4, Tables 21 and 22.
- College of American Pathologists Retinoblastoma Protocol v4.0.0.0 (2017), p. 4.
- Mendoza PR, et al. Histopathologic grading of anaplasia in retinoblastoma. American Journal of Ophthalmology
  2015;159(4):764-776.
