# Group XI — for the registrar

**Written 8 October 2026, while the Group XI build runs.** The evidence agents raised 140 questions
that only you can answer. The paediatric addendum the same day (13 PubMed Central papers, read into
eight parts) left 47 more items for the controlling session, and some of them need you. The build does
not wait for a ruling. Every question has a default: one of the decisions D1 to D16 in
`docs/group_11_build_contract.md` §0.7, or, where no D-number applies, the draft in the part's evidence
file. This file lists each question with its default, the evidence behind it, and what changes if you
rule otherwise.

**How to read the citations.** A part name such as `XIb_thyroid` means
`docs/group_11_evidence/XIb_thyroid.json` and `.md`. The source and its page follow the part name.
"PDF p." is a page of the PDF the text file was made from. "PMC section" is a section of a PubMed
Central text, which has no pages. "ICCR" means the International Collaboration on Cancer Reporting
dataset for the organ named. "ICD-O-3.1" means the WHO coding manual extract, cited by printed page.
Every code is given with its ICD-O-3.2 Preferred term, read from `icdo32.sqlite`.

**Order.** Items are ordered by cost:
- Part A: what changes the code a case gets, or whether the case is registered at all.
- Part B: what is built and how the clerk reaches it.
- Part C: the site, the group and the subgroup.
- Part D: sources you could supply.
- Part E: your decisions.

**Already answered.** Five questions are settled by your earlier rulings, and each is marked
**Settled** where it appears:
- the functioning neuroendocrine tumour with a grade, by "take the higher" (7 October 2026; A4);
- the colorectal, lung and breast carcinomas and malignant phyllodes tumour, by "Picker, as in Group 10"
  and the papers fetched the same day (8 October 2026; B1).

**One question is not among the 140.** `cross_group_A` §6 item 5 asks about olfactory carcinoma and
IDH2-mutant sinonasal carcinoma. It is in A18.

---

## Part A at a glance

| Item | Question | Built until you rule |
|---|---|---|
| A1 ✅ | ICD-O-3.2 and the WHO table code one term differently | (a), (b): **ruled 8 Oct 2026 — Rules A to K decide; applied and verified (E1).** (c): **ruled 8 Oct 2026 (E3):** 8252/3 agreed, built; cribriform carcinoma not added, noted in `docs/TODO.md` §35.9; 8290/3 kept |
| A2 ✅ | A stain, score or gene result decides what the diagnosis line leaves open | **Ruled 8 Oct 2026, built (E5, E6):** NUT carcinoma and female genital tract / oropharynx as built; adrenal asks for the Wieneke score and lists it; lung codes the favoured type when the file confirms it (SEER lung rule H3), with the TTF-1 and p40 stain panel |
| A3 ✅ | The code when the report names no type or no human papillomavirus status | **Agreed 8 Oct 2026 (E7):** 8010/3 Carcinoma, NOS; 8070/3 Squamous cell carcinoma, NOS; 8120/3 Transitional cell carcinoma, NOS |
| A4 ✅ | Rule K against the WHO entity's single code | **Approved 8 Oct 2026 (E7):** the WHO entity's code (D5); Rule K where no single code covers. Three held rows (Q19, Q109, Q102) still wait |
| A5 ✅ | Obsolete terms and their current successors | **Ruled 8 Oct 2026 (E7): Rule K.** Diffuse sclerosing 8260/3; adenocarcinoid 8244/3, built; stomach 8512/3 kept out, `docs/TODO.md` §35.10 |
| A6 ✅ | Stated behaviour against printed behaviour (Rule F) | **Ruled 8 Oct 2026 (E7): Rule F**, built for 8336/3, 8941/2 and 8542/2; behaviour stays tied to the code only where it changes the name; live pilot in `docs/TODO.md` §35.11 |
| A7 ✅ | Adrenal cortical neoplasm of uncertain malignant potential | **Answered 8 Oct 2026 by the score ruling (E8):** excluded, no code named |
| A8 ✅ | Melanoma of the skin registered on clinical evidence in a child | **Ruled 8 Oct 2026 (E9): the paediatric source.** No 8720/3 at basis 1; a note alone refers to Group XII with 8000/3 |
| A9 ✅ | Keratoacanthoma | **Ruled 8 Oct 2026 (E10):** not registered unless the pathologist calls it squamous cell carcinoma |
| A10 | Solid pseudopapillary neoplasm called benign | 8452/3 (D6). Stanley 2015 read in full (E10); ruling open |
| A11 ✅ | Sialoblastoma | **Ruled 8 Oct 2026 (E10): the papers.** Malignant; referred to Group XII as 8974 (XIIa4) |
| A12 ✅ | Gastroblastoma (8976, not in ICD-O-3.2) | **Ruled 9 Oct 2026 (E11): not built**, because ICD-O-3.2 lacks the code |
| A13 ✅ | Adenocarcinoma, HPV-associated and HPV-independent (8483, 8484, not in ICD-O-3.2) | **Ruled 9 Oct 2026 (E11): not built**; no screen names them |
| A14 | Registration on a marker without tissue | Offered at lung, digestive tract and unknown primary (D7) |
| A15 ✅ | Mesonephric-like adenocarcinoma (9113, not in ICD-O-3.2) | **Ruled 9 Oct 2026 (E11): not built** |
| A16 ✅ | Dermal melanoma (8750/3, not in ICD-O-3.2) and two non-malignant ICCR codes | **Ruled 9 Oct 2026 (E11): not built** |
| A17 | 8551/3 Acinar cell cystadenocarcinoma and 8780/3 Blue nevus, malignant: obsolete Preferred term, live other term | Off every screen (D3) |
| A18 | Other entities the WHO names and ICD-O-3.2 does not code | Not built (D4), with two exceptions |
| A19 | Thyroid-type carcinoma in struma ovarii | 9090/3 Struma ovarii, malignant, Group X |
| A20 | 8158/3 ACTH-producing tumor at the adrenal cortex | Off the adrenal screens (D16) |
| A21 | Group X's ovary picker records 8452/3 Solid pseudopapillary neoplasm of pancreas | Handed to the Group 10 session |
| A22 | Basis of diagnosis in three situations | 7, 5 and 8 (D8, D15) |

---

## A. Decisions that change which code a case gets, or whether it is registered

### A1. ICD-O-3.2 and the WHO table code one term differently — ✅ ruled and built: (a), (b) on 8 October 2026; (c) on 8 October 2026

When a term in the report has its own place in ICD-O-3.2 and the WHO table codes that tumour
differently, which code is recorded? The build follows no single rule, so the same kind of report codes
one way at one site and the other way at the next. The fifteen instances fall into three kinds.

**(a) ICD-O-3.2 files the report's term under one code, and the WHO table under another.** ✅ Ruled and built 8 October 2026 (E1).

| Part | The report says | ICD-O-3.2 | WHO or ICCR table | Built | Evidence |
|---|---|---|---|---|---|
| Nasopharynx (Q17) | Lymphoepithelial carcinoma, lymphoepithelioma, Schmincke tumour, undifferentiated carcinoma of nasopharyngeal type | 8082/3 Lymphoepithelial carcinoma (Lymphoepithelioma and Schmincke tumor filed there) | 8072/3 Squamous cell carcinoma, large cell, nonkeratinizing, NOS | Both reachable: the type screen records 8072/3, and 8082/3 is a picker entry whose synonyms lead to it | `XIc_nasopharynx` — ICCR Oropharynx and Nasopharynx, PDF p. 11; Badoual 2022, PDF p. 8 |
| Salivary gland (Q45) | Oncocytic carcinoma; poorly differentiated carcinoma | 8290/3 Oxyphilic adenocarcinoma; 8020/3 Carcinoma, undifferentiated, NOS | 8140/3 Adenocarcinoma, NOS ("salivary carcinoma NOS and emerging entities") | ICD-O-3.2 | `XIf1_salivary` — Skálová 2022, PDF pp. 1–2; ICCR Major Salivary Glands, PDF p. 8 |
| Salivary gland (Q44) | Mucinous adenocarcinoma, signet ring subtype | 8490/3 Signet ring cell carcinoma (synonym "Mucinous carcinoma, signet ring cell type"); Rule K agrees | 8480/3 Mucinous adenocarcinoma | WHO table, 8480/3 | `XIf1_salivary` — ICCR Major Salivary Glands, PDF p. 8; Skálová 2022, PDF p. 7 |
| Thymus (Q68) | Hepatoid, rhabdoid or sebaceous carcinoma; undifferentiated large cell carcinoma with a Castleman disease-like reaction | 8576/3 Hepatoid adenocarcinoma; 8410/3 Sebaceous carcinoma | 8586/3 Thymic carcinoma, NOS | WHO table, 8586/3 | `XIf5_thymus_mediastinum` — Marx 2022, PDF p. 4, footnote g |
| Thymus (Q70) | Neuroendocrine tumour, grade 3 | 8249/3 Neuroendocrine tumor, grade 2 (related term "Neuroendocrine tumor, grade 3") | 8013/3 Large cell neuroendocrine carcinoma, by current thoracic criteria | As the report states | `XIf5_thymus_mediastinum` — Marx 2022, PDF pp. 8–9 |
| Breast (Q81) | Malignant adenomyoepithelioma | 8983/3 Adenomyoepithelioma with carcinoma | 8562/3 Epithelial-myoepithelial carcinoma | ICD-O-3.2 | `XIf6_breast` — ICCR Invasive Breast, PDF p. 14 |
| Parathyroid (Q114) | Water-clear cell or oncocytic parathyroid carcinoma | 8322/3 Water-clear cell adenocarcinoma (C75.0); 8290/3 Oxyphilic adenocarcinoma; Rule K takes the higher | 8140/3 Adenocarcinoma, NOS (related term "Parathyroid carcinoma") | Both reachable: the screen records 8140/3, and 8322/3 and 8290/3 are picker entries | `XIf10_parathyroid_other_unspecified` — ICCR Parathyroid, PDF p. 9 |
| Urinary tract (Q95) | Mixed adenocarcinoma | 8323/3 Mixed cell adenocarcinoma | Netto 2022 prints 8323/3; ICCR, with the July 2024 corrigenda, prints 8140/3 | ICCR, 8140/3 | `XIf8_urinary_male_genital` — Netto 2022, PDF p. 7; ICCR Urinary Bladder, PDF p. 11 |
| Uterine corpus (Q86) | Gastric-type mucinous carcinoma | 8482/3 Mucinous carcinoma, gastric type (C53) | ICCR Endometrial prints 8144/3 Adenocarcinoma, intestinal type; ICCR Cervix and Vagina print 8482/3 | ICCR Endometrial, 8144/3 | `XIf7_female_genital` — ICCR Endometrial, PDF p. 9; ICCR Cervix, PDF p. 19 |
| Skin (Q32) | Pseudovascular squamous cell carcinoma | Related term of 8074/3 Squamous cell carcinoma, spindle cell | Not a subtype, and not a term for acantholytic carcinoma (8075/3 Squamous cell carcinoma, adenoid) | Held; no option or alias names it | `XIe_skin_carcinoma` — Goldman-Lévy 2025, PDF p. 3 |

**(b) ICD-O-3.2 files the term under a code whose Preferred term names another tumour.** ✅ Ruled and built 8 October 2026 (E1).

| Part | The report says | ICD-O-3.2 | The other reading | Built | Evidence |
|---|---|---|---|---|---|
| Melanoma (Q20) | Spitzoid melanoma | Synonym of 8770/3 Malignant Spitz tumor | Sargen 2026 calls "spitzoid" a description that also fits low cumulative sun damage melanoma (8743/3 Low cumulative sun damage melanoma) and melanoma in a congenital naevus (8761/3 Malignant melanoma arising in giant congenital nevus) | ICD-O-3.2, 8770/3 | `XId_melanoma` — Sargen 2026, PDF p. 1; Ferrari 2021, PDF p. 2 |
| Eye (Q25) | Uveal melanoma, mixed epithelioid and spindle cell type | Related term of 8770/3 Malignant Spitz tumor | The result prints a skin tumour's name for an eye tumour; also asked: does 8773/3 Spindle cell melanoma, type A stay in the eye picker? | ICD-O-3.2, 8770/3; 8773/3 in the eye picker | `XId_melanoma` — Milman 2023, PDF p. 10 |

**Rules A to K applied to (a) and (b), 8 October 2026** (`docs/group_11_evidence/registrar_A1ab_rules.md`; the
"Built" column in the tables above describes the evidence drafts before the ruling):

| Instance | What the rules give | Built now |
|---|---|---|
| a1 Nasopharynx | Lymphoepithelioma, lymphoepithelial carcinoma, lymphoepithelioma-like carcinoma, Schmincke tumour: 8082/3 Lymphoepithelial carcinoma (printed terms). Undifferentiated carcinoma of nasopharyngeal type: 8020/3 Carcinoma, undifferentiated, NOS (not printed; Rule J word order). Non-keratinising carcinoma, undifferentiated subtype: 8072/3 Squamous cell carcinoma, large cell, nonkeratinizing, NOS | **Changed:** 8072/3 → 8082/3 for the four older names; new option 8020/3; Rule K order in the hint |
| a2 Salivary | Oncocytic carcinoma 8290/3 Oxyphilic adenocarcinoma; poorly differentiated carcinoma 8020/3 Carcinoma, undifferentiated, NOS | No change (picker) |
| a3 Salivary | Mucinous adenocarcinoma, signet ring subtype: 8490/3 Signet ring cell carcinoma (printed synonym; Rule K agrees) | No code change; picker hint names it |
| a4 Thymus | Hepatoid 8576/3 Hepatoid adenocarcinoma; sebaceous 8410/3 Sebaceous carcinoma (Rule H: the printed skin site does not apply); undifferentiated large cell 8012/3 Large cell carcinoma, NOS (Rule G: "undifferentiated" is a grade); rhabdoid 8586/3 Thymic carcinoma, NOS (no printed term). "Thymic carcinoma, NOS" is a NOS term, so a named type replaces it | **Changed:** one 8586/3 option split into four |
| a5 Thymus | Neuroendocrine tumour, grade 3: 8249/3 (printed related term); large cell neuroendocrine carcinoma: 8013/3 | No code change; reason names the related term |
| a6 Breast | Malignant adenomyoepithelioma: 8983/3 Adenomyoepithelioma with carcinoma (printed synonym) | No change |
| a7 Parathyroid | Water-clear cell 8322/3; oncocytic 8290/3; parathyroid carcinoma 8140/3 Adenocarcinoma, NOS | No change |
| a8 Urinary tract | "Mixed adenocarcinoma" is not printed and Rule J reaches no term: 8140/3 Adenocarcinoma, NOS; "mixed cell adenocarcinoma" 8323/3 | No code change; reason names both printed terms |
| a9 Uterine corpus | Gastric-type mucinous carcinoma: 8482/3 Mucinous carcinoma, gastric type at the corpus (Rule H: the printed C53 does not apply) | No code change; picker hint names it |
| a10 Skin | Pseudovascular squamous cell carcinoma: 8074/3 Squamous cell carcinoma, spindle cell (printed related term) | No change (it was already reachable in the skin picker) |
| b1 Melanoma | Spitzoid melanoma: 8770/3 Malignant Spitz tumor (printed synonym); "spitzoid" used only as a description, with a diagnosis of melanoma: 8720/3 | No code change; hint on the diagnosis line |
| b2 Eye | Mixed epithelioid and spindle cell melanoma: 8770/3 (printed related term; Rule H: the skin site does not apply); 8773/3 Spindle cell melanoma, type A stays in the eye picker | No code change; reason and hint reworded |

**(c) The WHO retired or downgraded the entity, and ICD-O-3.2 keeps a current term.** ✅ Evidence rechecked (E2) and ruled (E3), 8 October 2026.

| Part | The report says | ICD-O-3.2 | WHO | Built | Evidence |
|---|---|---|---|---|---|
| Lung (Q60, addendum gap 7) | Bronchioloalveolar carcinoma; a child's report of "alveolar carcinoma" | 8252/3 Bronchiolo-alveolar carcinoma, non-mucinous (current); every 8251/3 term (Alveolar adenocarcinoma) is obsolete | No entity at 8252; the term was defined as non-invasive. Choices: 8252/3, the current adenocarcinoma code, or adenocarcinoma in situ (not registered) | Held | `XIf4_lung_pleura` — Nicholson 2022, PDF p. 9; Chen 2026, PMC section 2 |
| Skin (Q33) | Cribriform carcinoma (an older skin report) | 8201/3 Cribriform carcinoma, NOS (no ICCC-2017 range holds it at skin) | Downgraded to cutaneous cribriform tumour, which ICD-O-3.2 does not name | Held | `XIe_skin_carcinoma` — Goldman-Lévy 2025, PDF p. 5 |
| Eye (Q103) | Oncocytic carcinoma of the lacrimal gland | 8290/3 Oxyphilic adenocarcinoma (current) | Removed as obsolete | Held; not in the eye picker | `XIf9_eye` — Milman 2023, PDF p. 15 |

**Recheck of (c), 8 October 2026** (`docs/group_11_evidence/registrar_A1c_recheck.md`; the sources read only through
snippets, and the codes read from `icdo32.sqlite`):

| Part | Verdict | What the sources say | What the rules give for a report using the old term |
|---|---|---|---|
| Lung (Q60) | **Partly confirmed** | Nicholson 2022 Table 1 (PDF p. 2) and ICCR Lung Table 1 (PDF pp. 10–11) hold no row at 8252, and ICD-O-3.2 keeps 8252/3 Bronchiolo-alveolar carcinoma, non-mucinous as a current Preferred term. Both 8251/3 terms (Alveolar adenocarcinoma, Alveolar carcinoma) are `[obs]`, and Bronchiolo-alveolar carcinoma, mucinous is an `[obs]` synonym at 8253/3 Adenocarcinoma of lung, mucinous. **Two claims fail:** Nicholson's "noninvasive" sentence (printed p. 370) is about mucinous bronchioloalveolar carcinoma only, and no source in the files says the whole term was retired. Chen 2026 names "alveolar carcinoma" in its introduction only; no child in its 36-child series had one. | "Bronchioloalveolar carcinoma, non-mucinous" finds the current Preferred term, 8252/3. The plain term finds only the `[obs]` synonym at 8250/3 Lepidic adenocarcinoma, and "alveolar carcinoma" finds only `[obs]` terms at 8251/3. |
| Skin (Q33) | **Confirmed, with a qualification** | Goldman-Lévy 2025 (printed p. 559, PDF p. 5): cribriform carcinoma was downgraded to "cutaneous cribriform tumour", an indolent adnexal neoplasm, because no recurrence or metastasis was reported. The paper says "indolent", not "benign", and prints no code or behaviour. ICD-O-3.2 holds 8201/3 Cribriform carcinoma, NOS (not `[obs]`) and names no cribriform tumour. The exclusion line built at behaviour /0 is not sourced. | 8201/3 at C44 (Rule H: the Preferred term prints no site, so the stated site stands). |
| Eye (Q103) | **Confirmed** | Milman 2023 (printed p. 85, PDF p. 15): oncocytic carcinoma was removed as an obsolete entity. It names no successor, and its Table 12 keeps only the benign lacrimal oncocytoma. ICD-O-3.2 keeps 8290/3 Oxyphilic adenocarcinoma, with the synonyms Oncocytic adenocarcinoma and Oncocytic carcinoma, none `[obs]`. | 8290/3 at C69.5 (Rule H: no printed site, so the stated site stands). |

Not settled from the files: the source behind the lung part's 211-child series (Özkan 2024 is outside this
recheck), the WHO lung book's own wording on retiring the term, and the WHO skin volume's code and behaviour for
cutaneous cribriform tumour.

**Built until you rule:** the draft of each part, as the tables show. No D-number decides this class.
Standing rule 2 ("the tool codes to ICD-O-3.2") points to ICD-O-3.2. D5 points to the WHO entity where
the WHO gives the tumour one code.

**If you rule otherwise:** one principle replaces the mixed defaults.
- ICD-O-3.2 wins: 8490/3, 8410/3 or 8576/3, 8323/3 and 8482/3 replace the WHO codes, 8082/3 and 8322/3
  or 8290/3 become the only route, and each held term codes as ICD-O-3.2 prints it.
- The WHO table wins: 8140/3, 8562/3 and 8013/3 replace the ICD-O-3.2 codes, and each held term
  follows the WHO's reading (a non-invasive bronchioloalveolar carcinoma becomes adenocarcinoma in situ
  and is not registered).

The same principle answers A4 for a single term.

### A2. A stain, score or gene result decides what the diagnosis line leaves open — ✅ ruled and built 8 October 2026 (E5, E6)

May a result printed elsewhere in the report decide a code that the diagnosis line does not state?

- ✅ **Adrenal cortex (Q3).** Ruled 8 October 2026 (E6). The line says only "adrenocortical tumour" or "adrenocortical neoplasm", and
  the report gives a Wieneke score. **Built:** a score of 4 or more records 8370/3 Adrenal cortical
  carcinoma, and a score of 2 or less records the exclusion 8370/0 Adrenal cortical adenoma, NOS. A score
  of 3 goes to A7. A Weiss score is not used: in children it over-diagnoses carcinoma. **Also asked:**
  may an adolescent's Weiss score of 3 or more count the same way? **Evidence:** `XIa_adrenal_cortex` —
  Mete 2022, PDF pp. 1 and 21 (Table 6); ICCR Adrenal Cortex, PDF p. 16.
- ✅ **NUT carcinoma (Q73).** Agreed 8 October 2026 (E5). The line names only a poorly differentiated carcinoma. The report states
  nuclear NUT staining in more than 50% of tumour cells, sometimes with a negative NUTM1 fluorescence in
  situ hybridisation result. **Built:** the NUT stain rule records 8023/3 Nuclear protein in testis
  (NUT)-associated carcinoma at basis 7. **Evidence:** `NUT_carcinoma` — Luo 2025, PDF p. 7 (the stain
  is fully specific in a carcinoma; a false-negative fluorescence in situ hybridisation case); Lemelle
  2022, PDF pp. 6–7 (the molecular test is definitive).
- ✅ **Female genital tract (Q89), and the same screen at the oropharynx.** Agreed 8 October 2026 (E5). The line names squamous cell
  carcinoma and no human papillomavirus status. **Built:** a p16 or human papillomavirus result decides
  between 8085/3 Squamous cell carcinoma, HPV positive and 8086/3 Squamous cell carcinoma, HPV negative.
  **Evidence:** `XIf7_female_genital` — ICCR Cervix, PDF p. 19; ICCR Vulva, PDF p. 11; `XIc_nasopharynx`
  — ICCR Oropharynx and Nasopharynx, PDF p. 10.
- ✅ **Lung (Q58).** Ruled 8 October 2026 (E6). A biopsy reads "non-small cell carcinoma, favour adenocarcinoma" or "favour squamous
  cell carcinoma". **Built:** 8046/3 Non-small cell carcinoma. The WHO's TTF-1 and p40 rules are written
  down in the evidence and are not built. **Also asked:** should it record the favoured type, 8140/3
  Adenocarcinoma, NOS or 8070/3 Squamous cell carcinoma, NOS? **Evidence:** `XIf4_lung_pleura` —
  Nicholson 2022, PDF pp. 5–6.

**Built until you rule:** as listed. D8 makes a cytology report that only "favours" an entity
non-registrable. The lung default extends that to a biopsy, but records the non-committal code
instead of excluding the case.

**If you rule otherwise:**
- "The line decides": the adrenal, NUT and p16 routes are removed, and those cases record 8370/0 or go
  to the behaviour question, 8020/3 Carcinoma, undifferentiated, NOS, and 8070/3 Squamous cell
  carcinoma, NOS.
- "The test decides": the lung gains the TTF-1 and p40 rule.

### A3. The code when the report names no type or no human papillomavirus status — ✅ agreed 8 October 2026 (E7)

- **Nasopharynx (Q18).** The report says only "nasopharyngeal carcinoma". **Built:** 8010/3 Carcinoma,
  NOS, because the WHO definition says the tumour is usually, not always, squamous. **Other choice:**
  8070/3 Squamous cell carcinoma, NOS. **Evidence:** `XIc_nasopharynx` — Badoual 2022, PDF p. 6.
- **Penis (Q97).** Squamous cell carcinoma, usual type, with no human papillomavirus or p16 result.
  **Built:** 8070/3 Squamous cell carcinoma, NOS. ICD-O-3.2 prints "Squamous cell carcinoma, usual type"
  as a synonym there. **Other choice:** 8086/3 Squamous cell carcinoma, HPV negative, because ICCR places
  the usual type under HPV-independent. **Evidence:** `XIf8_urinary_male_genital` — ICCR Penis and Distal
  Urethra, PDF pp. 10–11.
- **Urinary tract (Q98).** Urine cytology is positive for high-grade urothelial carcinoma, and there is
  no histology. **Built:** 8120/3 Transitional cell carcinoma, NOS at basis 5. **Other choice:** 8010/3
  Carcinoma, NOS, or no registration, because cytology cannot tell carcinoma in situ (8120/2 Urothelial carcinoma in situ, not
  registered) from invasive carcinoma. **Evidence:** `XIf8_urinary_male_genital` — Netto 2022, PDF p. 9.

**Built until you rule:** as listed. These are the evidence drafts; no D-number applies.

**If you rule otherwise:** the one option or reason at each site changes code. Nasopharyngeal
carcinoma is among the commoner Group XI carcinomas in children, so Q18 decides many cases.

### A4. Rule K against the WHO entity's single code (D5) — ✅ approved 8 October 2026 (E7); three held rows wait

Your ruling of 7 October 2026 says that when no single code covers every term, the clerk takes the
higher code (Rule K, ICD-O-3.1 printed p. 24; `docs/TODO.md` §33). D5 treats a WHO entity's code as
that single code: where the WHO gives the tumour one code, Rule K does not apply. Does the WHO entity's
code count as the single code?

| Part | The report says | Built (D5 unless stated) | Rule K or the other reading | Evidence |
|---|---|---|---|---|
| Thyroid (Q10.1) | Clear cell subtype of papillary carcinoma | 8260/3 Papillary adenocarcinoma, NOS | 8310/3 Clear cell adenocarcinoma, NOS | `XIb_thyroid` — ICCR Thyroid, PDF pp. 2, 9 |
| Thyroid (Q10.2) | Squamous cell carcinoma of the thyroid | 8020/3 Carcinoma, undifferentiated, NOS (the WHO calls it a subtype of anaplastic carcinoma) | 8070/3 Squamous cell carcinoma, NOS | `XIb_thyroid` — ICCR Thyroid, PDF p. 12; Juhlin 2022, PDF p. 6 |
| Thyroid (Q10.3) | Anaplastic carcinoma with a papillary or follicular component | 8020/3 | 8260/3, or 8330/3 Follicular carcinoma, NOS | `XIb_thyroid` — ICCR Thyroid, PDF p. 12 |
| Thyroid (Q10.4) | Mixed medullary and oncocytic carcinoma | 8346/3 Mixed medullary-follicular carcinoma (the family code; the WHO prints none for this entity) | 8345/3 Medullary thyroid carcinoma | `XIb_thyroid` — ICCR Thyroid, PDF p. 3 |
| Thyroid (Q11) | Papillary microcarcinoma with a named subtype | Rule K: 8341/3 Papillary microcarcinoma over classic 8260/3; tall cell 8344/3 Papillary carcinoma, columnar cell | The WHO asks pathologists to subtype small tumours and drop the size term, which gives the subtype's code | `XIb_thyroid` — ICCR Thyroid, PDF p. 10; Juhlin 2022, PDF p. 4 |
| Thyroid (Q14) | Oncocytic carcinoma, minimally invasive or encapsulated angioinvasive | 8290/3 Oxyphilic adenocarcinoma | 8335/3 Follicular carcinoma, minimally invasive, or 8339/3 Follicular carcinoma, encapsulated, angioinvasive | `XIb_thyroid` — ICCR Thyroid, PDF pp. 9, 11 |
| Oropharynx (Q19) | Adenosquamous carcinoma, HPV-associated | Held | 8560/3 Adenosquamous carcinoma (Rule K) against 8085/3 Squamous cell carcinoma, HPV positive (the WHO drops histological typing for HPV-associated squamous cell carcinoma) | `XIc_nasopharynx` — ICCR Oropharynx and Nasopharynx, PDF p. 10 |
| Nasal cavity (Q109) | A squamous subtype and a human papillomavirus status in one line, for example non-keratinising, HPV-associated | Held; at the oropharynx the hint already takes 8085/3 or 8086/3 Squamous cell carcinoma, HPV negative | 8072/3 (WHO subtype) against 8085/3 (Rule K) | `XIf10_head_neck` — ICCR Oral Cavity, PDF p. 8 |
| Salivary gland (Q43) | Carcinoma ex pleomorphic adenoma whose malignant component is myoepithelial carcinoma | 8941/3 Carcinoma ex pleomorphic adenoma | 8982/3 Myoepithelial carcinoma, which ICCC-2017 places in Group XII | `XIf1_salivary` — ICCR Major Salivary Glands, PDF pp. 7–8 |
| NUT carcinoma (Q72) | NUT carcinoma and squamous cell carcinoma in one line | 8023/3 Nuclear protein in testis (NUT)-associated carcinoma; the WHO entity is a squamous or poorly differentiated carcinoma | 8070/3 to 8072/3 | `NUT_carcinoma` — Luo 2025, PDF pp. 5–6; ICD-O-3.1, printed p. 16 |
| Breast (Q79) | A special pattern of invasive carcinoma of no special type | A pattern with a printed code records it (8290/3, 8314/3 Lipid-rich carcinoma, 8315/3 Glycogen-rich carcinoma, 8410/3 Sebaceous carcinoma); every other pattern records 8500/3 Infiltrating duct carcinoma, NOS; medullary or inflammatory carcinoma named as the diagnosis records 8510/3 Medullary carcinoma, NOS or 8530/3 Inflammatory carcinoma | Rule K would give 8510/3, 8574/3 Adenocarcinoma with neuroendocrine differentiation, 8530/3, 9100/3 Choriocarcinoma, NOS (Group X) or 8720/3 Malignant melanoma, NOS | `XIf6_breast` — ICCR Invasive Breast, PDF pp. 12–13; Tan 2020, PDF p. 2 |
| Breast (Q82) | Metaplastic carcinoma and a subtype | 8575/3 Metaplastic carcinoma, NOS. A subtype named alone records its ICD-O-3.2 term (8572/3 Adenocarcinoma with spindle cell metaplasia, 8571/3 Adenocarcinoma with cartilaginous and osseous metaplasia, 8070/3, 8032/3 Spindle cell carcinoma, NOS, 8560/3). Myoepithelial carcinoma (8982/3) named alone goes to Group XII | The subtype's own code in every case | `XIf6_breast` — ICCR Invasive Breast, PDF pp. 13–14 |
| Urinary tract and penis (Q93) | A urothelial subtype whose WHO code is lower than 8120 (8082/3 Lymphoepithelial carcinoma, 8031/3 Giant cell carcinoma, 8020/3); a penile HPV-associated subtype lower than 8085 (8083/3 Basaloid squamous cell carcinoma, 8054/3 Warty carcinoma, 8084/3 Squamous cell carcinoma, clear cell type, 8082/3) | The WHO subtype code | 8120/3 or 8085/3 | `XIf8_urinary_male_genital` — Netto 2022, PDF p. 7; ICCR Penis and Distal Urethra, PDF p. 10 |
| Urinary tract (Q94) | Lipid-rich, clear cell (glycogen-rich), or with glandular differentiation | 8120/3 Transitional cell carcinoma, NOS | 8314/3, 8315/3 or 8140/3 | `XIf8_urinary_male_genital` — Netto 2022, PDF pp. 7–8 |
| Urinary tract (Q96) | Small cell neuroendocrine carcinoma mixed with urothelial carcinoma | 8045/3 Combined small cell carcinoma (synonym Mixed small cell carcinoma) | 8041/3 Small cell carcinoma, NOS, or 8154/3 Mixed neuroendocrine non-neuroendocrine neoplasm (MiNEN) | `XIf8_urinary_male_genital` — ICCR Urinary Bladder, PDF pp. 8, 11 |
| Conjunctiva (Q102) | Squamous cell carcinoma with mucinous differentiation | Held; the evidence proposes 8070/3 | 8480/3 Mucinous adenocarcinoma | `XIf9_eye` — Milman 2023, PDF pp. 6–7 |
| Thymus (Q67; addendum gap 8) | Combined thymic carcinoma and thymoma, or carcinoid and thymoma | Rule K: the thymoma code (8581/3 Thymoma, type A to 8585/3 Thymoma, type B3) is higher than every thymic carcinoma code except 8586/3 Thymic carcinoma, NOS | The carcinoma or carcinoid component, which the WHO and ICCR name first as the more aggressive. Since the addendum, the thymoma types are options on the histology screen and the carcinomas are in the picker, so the two components sit on different screens | `XIf5_thymus_mediastinum` — Marx 2022, PDF p. 6; ICCR Thymic Epithelial, PDF p. 9; Rossi 2022, PMC section 4 |
| Pancreas and digestive tract (Q55) | A functioning neuroendocrine tumour with a grade, for example gastrinoma, grade 2 | **Settled** by your ruling of 7 October 2026: 8249/3 Neuroendocrine tumor, grade 2, the higher code, stated in the hint | — | `XIf2_XIf3_digestive` — Karges 2025, PMC sections 8–9 |

**Built until you rule:** D5, as the table shows. Where no single code covers the terms, Rule K applies
by your ruling of 7 October 2026. The three rows marked held wait for you.

**If you rule otherwise:**
- Rule K wins over the WHO entity: the five thyroid rows take 8310/3, 8070/3, 8260/3 or 8330/3, 8345/3,
  and 8335/3 or 8339/3; the salivary row takes 8982/3 and goes to Group XII; the NUT row takes 8070/3
  to 8072/3; the two urinary rows take 8120/3 or 8085/3, and 8314/3, 8315/3 or 8140/3; the two breast
  rows take the Rule K codes.
- The WHO entity wins even where Rule K applies today: the microcarcinoma row takes the subtype's code.
- The more aggressive component wins: the thymus row takes the carcinoma or carcinoid code.

### A5. Obsolete terms and their current successors (D3) — ✅ ruled 8 October 2026 (E7); stomach in TODO §35.10

D3 keeps every all-obsolete code off the screens. Where the WHO source names the current entity on the
same stem, the tree offers that entity's current code instead. Are these successors right?

- **Thyroid (Q9).** Diffuse sclerosing subtype of papillary carcinoma. Every 8350/3 term is obsolete,
  including "Papillary carcinoma, diffuse sclerosing" (Preferred term Nonencapsulated sclerosing
  carcinoma). The WHO table gives the subtype no code of its own. **Built:** 8260/3 Papillary
  adenocarcinoma, NOS. ICCR notes the subtype in young patients. **Evidence:** `XIb_thyroid` — ICCR
  Thyroid, PDF pp. 2, 9, 11.
- **Appendix (Q51).** A report of adenocarcinoid tumour. 8245/3 Adenocarcinoid tumor is obsolete.
  Nagtegaal 2020 names goblet cell adenocarcinoma, formerly goblet cell carcinoid or carcinoma, and does
  not mention adenocarcinoid. **Built:** the tree offers 8243/3 Goblet cell carcinoid for goblet cell
  adenocarcinoma. The word "adenocarcinoid" has no option or alias of its own. **Asked:** may it record
  8243/3? **Evidence:** `XIf2_XIf3_digestive` — Nagtegaal 2020, PDF p. 4.
- **Stomach (Q50).** Gastric carcinoma with lymphoid stroma. ICCR prints 8512/3, every 8512/3 term is
  obsolete (Medullary carcinoma with lymphoid stroma), and two current codes are candidates: 8510/3
  Medullary carcinoma, NOS and 8082/3 Lymphoepithelial carcinoma. **Built:** not built. **Evidence:**
  `XIf2_XIf3_digestive` — ICCR Stomach, PDF pp. 13, 15.

**If you rule otherwise:** the diffuse sclerosing and goblet cell options change code, an
"adenocarcinoid" alias is added or refused, and gastric carcinoma with lymphoid stroma gains an option
on the code you name.

### A6. Stated behaviour against printed behaviour (Rule F; D6) — ✅ ruled and built 8 October 2026 (E7); pilot in TODO §35.11

Rule F tells the coder to record the behaviour the pathologist states (ICD-O-3.1, printed p. 15). D6
records the behaviour ICD-O-3.2 prints wherever the stated behaviour would need a code ICD-O-3.2 does
not print, because standing rule 1 forbids an unprinted code. This is the policy question left open as
Group X review A1, A6 and A10 and Group VIII review A1. One answer serves every group.

**(a) The report's behaviour differs from what ICD-O-3.2 prints for the term.**
- **Thyroid (Q15).** A hyalinizing trabecular tumour, or another /1 thyroid tumour, that the report calls
  malignant. **Built:** the exclusion 8336/1 Hyalinizing trabecular tumor. 8336/3 is not printed, and
  ICCC-2017 range 121 would place it in XIb. **Evidence:** `XIb_thyroid` — ICCR Thyroid, PDF p. 9;
  Juhlin 2022, PDF p. 3.
- **Thymus (Q69).** A thymoma the report calls benign. **Built:** the exclusion 8580/0 Microscopic
  thymoma, where ICD-O-3.2 prints "Thymoma, benign" as a related term. The WHO treats every thymoma
  except micronodular thymoma with lymphoid stroma as malignant. **Evidence:** `XIf5_thymus_mediastinum`
  — Marx 2022, PDF p. 3.
- **Salivary gland (Q42).** Intracapsular carcinoma ex pleomorphic adenoma, which ICCR calls in situ.
  **Built:** 8941/3 Carcinoma ex pleomorphic adenoma for every extent, as the WHO table does. ICD-O-3.2
  prints no 8941/2. **Evidence:** `XIf1_salivary` — ICCR Major Salivary Glands, PDF pp. 7–8.
- **Vulva (Q90).** Extramammary Paget disease confined to the epithelium. **Built:** registered as
  8542/3 Paget disease, extramammary, the only behaviour ICD-O-3.2 prints. 8542/2 is not printed.
  **Evidence:** `XIf7_female_genital` — ICCR Vulva, PDF p. 11.

**(b) ICD-O-3.2 settles the case directly; confirm.**
- **Adrenal cortex (Q4).** "Adrenocortical tumour" with no behaviour and no score. **Built:** the
  exclusion 8370/0 Adrenal cortical adenoma, NOS, where ICD-O-3.2 files "Adrenal cortical tumor, NOS".
  **Evidence:** `XIa_adrenal_cortex` — Pfister 2022, PDF p. 14.
- **Thyroid (Q8).** Encapsulated follicular carcinoma with no capsular or vascular invasion described.
  **Built:** the exclusion 8335/1 Follicular tumor of uncertain malignant potential, where ICD-O-3.2 files
  "Follicular carcinoma, encapsulated, NOS". **Evidence:** `XIb_thyroid` — ICCR Thyroid, PDF pp. 10–11;
  currency check §3.
- **Skin (Q34).** Squamoproliferative tumour of uncertain malignant potential. **Built:** excluded with
  no code. ICD-O-3.2 prints no term, and Rule F gives /1. **Evidence:** `XIe_skin_carcinoma` —
  Goldman-Lévy 2025, PDF p. 3.
- **Salivary gland (Q41).** Intraductal carcinoma (8500/2 Intraductal carcinoma, noninfiltrating, NOS)
  with invasion stated. **Built:** 8500/3 Infiltrating duct carcinoma, NOS, which is also the code of
  salivary duct carcinoma. **Evidence:** `XIf1_salivary` — Skálová 2022, PDF p. 2.
- **Urinary tract (Q100).** Inflammatory myofibroblastic tumour. **Built:** the exclusion 8825/1
  Myofibroblastic tumor, NOS. A report calling it malignant records 8825/3 Myofibroblastic sarcoma and is
  referred to Group IX. **Evidence:** `XIf8_urinary_male_genital` — Pfister 2022, PDF p. 6.

**Built until you rule:** D6 for (a); ICD-O-3.2 as printed for (b).

**If you rule otherwise:** if the stated behaviour wins, the registry needs codes ICD-O-3.2 does not
print (8336/3; 8941/2 and 8542/2 for exclusions). That is a registry-local rule and lifts standing rule 1
for these cases. A malignant hyalinizing trabecular tumour would then be registered in XIb, and a
"benign" thymoma would still be excluded.

### A7. Adrenal cortical neoplasm of uncertain malignant potential (Q2) — ✅ answered 8 October 2026 (E8)

A tumour reported as of uncertain malignant potential, or with a Wieneke score of 3, is excluded. The
WHO does not treat it as a distinct entity, and ICD-O-3.2 prints no 8370/1. Should the exclusion name
8370/1, built by Rule F, or name no code?

**Built until you rule:** excluded with no code named. The evidence draft named 8370/1. Standing rule 1
and D6 keep an unprinted code off the result.

**Evidence:** `XIa_adrenal_cortex` — ICCR Adrenal Cortex, PDF pp. 2, 7; Mete 2022, PDF p. 21.

**If you rule otherwise:** the result prints 8370/1 as a Rule F code. The same answer then decides
Spitz melanocytoma (A16) and the squamoproliferative tumour (A6). The case stays unregistered either way.

### A8. Melanoma of the skin registered on clinical evidence in a child (Q21) — ✅ ruled and built 8 October 2026 (E9)

Visser 2023 Table 3 registers melanoma of the skin from a clinical note alone: 8720/3 Malignant melanoma,
NOS at basis 1. Ferrari 2021 says that in children, benign pigmented lesions can look like melanoma, and
it requires an excisional biopsy. Should Table 3 apply to ages 0 to 18?

**Built until you rule:** D7, an exception to the Group XII referral: 8720/3 at basis 1, on the skin
tree only.

**Evidence:** `XId_melanoma` — Ferrari 2021, PDF pp. 2–3; contract §0.5 (Visser 2023, Table 3,
pp. 04–05).

**If you rule otherwise:** the skin tree's clinical route refers to Group XII with 8000/3 Neoplasm,
malignant, or the case is not registered until there is tissue.

### A9. Keratoacanthoma (Q30) — ✅ ruled and built 8 October 2026 (E10)

ICD-O-3.2 gives Keratoacanthoma as a related term of 8071/3 Squamous cell carcinoma, keratinizing, NOS,
a malignant code, and prints no 8071/1. The WHO skin volume treats keratoacanthoma as probably a
separate entity, and says the two cannot always be told apart. Huang 2019 counts 8 keratoacanthomas
among 131 squamous cell carcinomas in patients under 20. Is a keratoacanthoma registered as 8071/3, or
excluded unless the pathologist calls it malignant?

**Built until you rule:** an option on the skin histology screen that records 8071/3, flagged as held
for you. The word is not an alias of 8071/3.

**Evidence:** `XIe_skin_carcinoma` — Goldman-Lévy 2025, PDF pp. 2–3; Huang 2019, PMC sections 4 and 6.

**If you rule otherwise:** the option becomes an exclusion. Under Rule F, a report calling the lesion
malignant still records 8071/3.

### A10. Solid pseudopapillary neoplasm called benign (Q53)

ICD-O-3.2 codes the pancreatic tumour 8452/3 Solid pseudopapillary neoplasm of pancreas and prints no
8452/0. Stanley 2015 says most are benign. Is a pancreatic tumour the report calls benign, or of low
malignant potential, still 8452/3?

ICD-O-3.2 also prints three older pancreatic names at 8452/1 Solid pseudopapillary tumor of ovary, each
marked C25: Papillary cystic tumor, Solid and cystic tumor, and Solid and papillary epithelial neoplasm.
An older report that uses one of them would code /1 and be excluded.

**Built until you rule:** D6. Every report that names the tumour records 8452/3, whatever behaviour it
states. The three older names have no option or alias.

**Evidence:** `XIf2_XIf3_digestive` — Stanley 2015, PDF pp. 1, 3; Ebrahim 2025, PMC section 13 (four
patients aged 8 to 14).

**If you rule otherwise:** a stated benign behaviour excludes the case, which needs 8452/0, a code
ICD-O-3.2 does not print (A6). The older names either code 8452/3, as the pancreatic term, or 8452/1, as
ICD-O-3.2 files them.

### A11. Sialoblastoma (Q39) — ✅ ruled and built 8 October 2026 (E10)

Pfister 2022 lists sialoblastoma as a malignant paediatric tumour. Perez-de-Oliveira 2025 calls it a
rare malignant neoplasm of the neonatal period and early childhood. ICD-O-3.2 and ICCR print 8974/1
Sialoblastoma, and ICCC-2017 holds 8974 only at /3, in XIIa4. Is every sialoblastoma registered at /3,
only one the report calls malignant, or none?

**Built until you rule:** D6. Every sialoblastoma records the exclusion 8974/1, whatever the report calls
it. The evidence draft referred one called malignant to Group XII as 8974/3, a code ICD-O-3.2 does not
print.

**Evidence:** `XIf1_salivary` — Pfister 2022, PDF p. 14; Perez-de-Oliveira 2025, PMC section 5; ICCR
Major Salivary Glands, PDF p. 8.

**If you rule otherwise:** the case is referred to Group XII with 8974/3. That needs your policy on an
unprinted /3 code (A6).

### A12. Gastroblastoma (Q49) — ✅ ruled 9 October 2026 (E11): not built

Pfister 2022 lists gastroblastoma among the gastrointestinal tumours of children and young adults
(MALAT1::GLI1 fusion). ICCR Stomach prints 8976/3 with an asterisk. ICD-O-3.2 and ICCC-2017 hold no 8976.
How is it recorded, and in Group XI or Group XII?

**Built until you rule:** D4. Not built: no screen names it, and a report of gastroblastoma meets only the
generic options of the stomach screen.

**Evidence:** `XIf2_XIf3_digestive` — Pfister 2022, PDF pp. 11, 13; ICCR Stomach, PDF pp. 14–15.

**If you rule otherwise:** the stomach screen gains an option with the code you name (Group XI), or a
referral (Group XII).

### A13. Adenocarcinoma, HPV-associated and HPV-independent (8483, 8484; Q84, Q107) — ✅ ruled 9 October 2026 (E11): not built

ICCR Cervix and ICCR Vagina print 8483/3 Adenocarcinoma, HPV-associated and 8484/3 Adenocarcinoma,
HPV-independent, NOS, with their in situ forms 8483/2 and 8484/2. ICCR Nasal Cavity prints 8483/3 for
HPV-related multiphenotypic sinonasal carcinoma. ICD-O-3.2 has neither number. Until IARC publishes them,
what should a report of either record?

**Built until you rule:** D4. Not built.
- At the cervix and vagina, the nearest generic option is 8140/3 Adenocarcinoma, NOS, the interim the
  evidence proposes. **Other choice:** 8384/3 Adenocarcinoma, endocervical type, NOS for the
  HPV-associated type.
- At the nasal cavity, no screen names the sinonasal carcinoma.
- The in situ forms are excluded whatever their code.

The cervical adenocarcinoma Wohlmuth 2021 reports in girls is the clear cell type, which ICCR codes
8310/3 Clear cell adenocarcinoma, NOS. That code is built, so this item touches few children.

**Evidence:** `XIf7_female_genital` — ICCR Cervix, PDF p. 19; ICCR Vagina, PDF p. 8; Wohlmuth 2021, PMC
section 10. `XIf10_head_neck` — ICCR Nasal Cavity, PDF p. 8; Thompson 2022, PDF p. 8.

**If you rule otherwise:** the cervix, vagina and nasal cavity options record the code you name, and the
interim 8140/3 option goes.

### A14. Registration on a marker without tissue (Visser 2023 Table 4; Q54, Q63, Q119)

Visser 2023 Table 4 registers a neuroendocrine tumour at basis 4 from imaging that shows the tumour and
a raised marker. Should the tool offer that route at these three places?
- **Digestive tract and pancreas (Q54).** All eight Table 4 answers:
  - chromogranin A → 8240/3 Neuroendocrine tumor, NOS;
  - insulin → 8151/3 Insulinoma, NOS;
  - glucagon → 8152/3 Glucagonoma;
  - gastrin → 8153/3 Gastrinoma;
  - vasoactive intestinal peptide → 8155/3 Vipoma;
  - somatostatin → 8156/3 Somatostatinoma;
  - serotonin → 8241/3 Enterochromaffin cell carcinoid;
  - adrenocorticotropic hormone → 8158/3 ACTH-producing tumor.

  Karges 2025 now reports insulinoma and gastrinoma in children, and defines a functioning tumour by its
  clinical syndrome. The digestive sources give no serum test a diagnostic role (addendum, digestive
  gap 5).
- **Lung (Q63).** Chromogranin A → 8240/3, serotonin → 8241/3, adrenocorticotropic hormone → 8158/3. The
  lung papers name none of these tests.
- **Unknown primary (Q119).** Imaging shows only deposits, the clinician states a neuroendocrine tumour,
  and chromogranin A or serotonin is raised. The route records 8240/3 or 8241/3 at C80.9.

**Built until you rule:** D7. The marker codes record at basis 4, only with imaging that shows the
tumour, and only in the trees whose sites the marker concerns. The thymus (chromogranin A,
adrenocorticotropic hormone) and the thyroid (calcitonin → 8345/3 Medullary thyroid carcinoma) carry
the same route. A raised marker with no imaging is not registrable (Visser rule 6).

**Evidence:** contract §0.5 (Visser 2023, Table 4, p. 06). `XIf2_XIf3_digestive` — Karges 2025, PMC
sections 3, 7. `XIf4_lung_pleura` — tissue-free routes. `XIf10_parathyroid_other_unspecified` —
tissue-free routes.

**If you rule otherwise:** at each site you remove, the case falls to the 8000/3 Neoplasm, malignant referral to Group XII
(C6).

### A15. Mesonephric-like adenocarcinoma (9113; Q85) — ✅ ruled 9 October 2026 (E11): not built

ICCR Endometrial prints 9113/3 Mesonephric-like adenocarcinoma. ICD-O-3.2 has no 9113, and the currency
check does not list it. Should the case be held, recorded as 8140/3 Adenocarcinoma, NOS, or recorded as
9110/3 Mesonephroma, malignant, which ICCC-2017 places in Group XII?

**Built until you rule:** D4. Held: no screen names it.

**Evidence:** `XIf7_female_genital` — ICCR Endometrial, PDF pp. 9, 23.

**If you rule otherwise:** the uterine screen gains the option you name: 8140/3 in Group XI, or a
referral to Group XII with 9110/3.

### A16. Dermal melanoma (8750/3), and two non-malignant ICCR codes (Q22) — ✅ ruled 9 October 2026 (E11): not built

ICCR Invasive Melanoma prints three codes that ICD-O-3.2 lacks:
- **8750/3 Dermal melanoma.** It is malignant and would fall in XId. ICD-O-3.2 holds 8750/0 Dermal
  nevus only.
- **8770/1 Spitz melanocytoma (atypical Spitz tumour).** It is common in children and is excluded either
  way. ICD-O-3.2 prints "Spitz nevus, atypical" as a related term of 8770/0 Epithelioid and spindle cell
  nevus.
- **8743/2 Low cumulative sun damage melanoma in situ.** It is excluded either way.

Should the tool build 8750/3, record dermal melanoma as 8720/3 Malignant melanoma, NOS, or hold it?

**Built until you rule:** D4.
- Dermal melanoma is not built and reaches 8720/3.
- Spitz melanocytoma is excluded with no code named (A7).
- The in situ melanoma is excluded as 8720/2 Melanoma in situ.

**Evidence:** `XId_melanoma` — ICCR Invasive Melanoma, PDF p. 8; Sargen 2026, PDF p. 3; Goldman-Lévy
2025, PDF p. 4.

**If you rule otherwise:** dermal melanoma records the code you name, and the Spitz melanocytoma
exclusion names 8770/1 or 8770/0.

### A17. 8551 and 8780: an obsolete Preferred term with a live other term (Q137)

Your ruling of 8 October 2026 keeps off every screen the codes whose every term is obsolete. Two Group XI
codes have an obsolete Preferred term but a live other term:
- **8780/3 Blue nevus, malignant.** The live synonym is Melanoma arising in blue nevus, the WHO 5th
  edition name. It is rare in children, most often within a giant congenital blue naevus.
- **8551/3 Acinar cell cystadenocarcinoma.** The live related term is Acinar adenocarcinoma of lung
  (C34), which the WHO lung table prints.

Build them under the live term, or keep them off every screen?

**Built until you rule:** D3. Off every screen, and never aliased.
- A melanoma arising in a blue naevus reaches 8720/3 Malignant melanoma, NOS.
- An acinar adenocarcinoma of the lung reaches 8140/3 Adenocarcinoma, NOS.
- The melanoma and lung evidence drafts had built both codes; D3 overrides them.

**Evidence:** `XId_melanoma` — ICCR Invasive Melanoma, PDF p. 8; Sargen 2026, PDF p. 4.
`XIf4_lung_pleura` — Nicholson 2022, PDF p. 2.

**If you rule otherwise:** each code is offered under its live term. Validation rule 3 then exempts the
two codes.

### A18. Other entities the WHO names and ICD-O-3.2 does not code (D4)

D4 builds no code that ICD-O-3.2 lacks. No screen names the entity, and a report that names it reaches
the nearest generic option. Do you accept that for each entity below, or name a code?

**(a) The WHO places its entity on an ICD-O-3.2 number whose term names another tumour.**
- **Thoracic SMARCA4-deficient undifferentiated tumour (Q59, Q71).** The WHO prints 8044/3. ICD-O-3.2's
  term there is Small cell carcinoma, intermediate cell. **Built:** not built (D4 names it). The tumour
  most often invades the mediastinum. **Evidence:** `XIf4_lung_pleura` — Nicholson 2022, PDF p. 3;
  `XIf5_thymus_mediastinum` — Marx 2022, PDF p. 10.
- **SWI/SNF complex-deficient sinonasal carcinoma (Q106).** Also 8044/3. **Built:** not built. The
  evidence draft had a picker entry on 8044/3. **Evidence:** `XIf10_head_neck` — ICCR Nasal Cavity, PDF
  p. 8; Thompson 2022, PDF p. 5.
- **Carcinoma cuniculatum (Q110).** The WHO prints 8051/3, where ICD-O-3.2's term is Verrucous carcinoma,
  NOS. **Built:** the head and neck draft offers it on 8051/3. **Evidence:** `XIf10_head_neck` — ICCR
  Oral Cavity, PDF p. 8.
- **Tall cell carcinoma with reversed polarity (Q80).** The WHO prints 8509/3, where ICD-O-3.2's term is
  Solid papillary carcinoma with invasion. **Built:** the breast draft puts it in the picker on 8509/3,
  with a reason naming that term. **Evidence:** `XIf6_breast` — ICCR Invasive Breast, PDF p. 14; Tan
  2020, PDF p. 2.

The three defaults in (a) differ. One answer should settle all four rows.

**(b) The WHO names the entity and the sources give no ICD-O-3.2 code.**
- **Thyroid (Q12).** Thyroblastoma, and a high-grade differentiated thyroid carcinoma whose dominant type
  is not named. A clerk with no code may reach for 9080/3 Teratoma, malignant, NOS, which ICCC-2017 places
  in Group X. **Evidence:** `XIb_thyroid` — ICCR Thyroid, PDF pp. 2–3, 12.
- **Melanoma (Q23).** BAP1-inactivated melanoma, WNT-activated deep penetrating melanoma, and melanoma
  arising in a pigmented epithelioid melanocytoma. Sargen places all three among the low cumulative sun
  damage melanomas. **Other choices:** 8743/3 Low cumulative sun damage melanoma, or 8720/3 Malignant melanoma, NOS.
  **Evidence:** `XId_melanoma` — Sargen 2026, PDF p. 4.
- **Melanoma (Q28).** The CRTC1::TRIM11 cutaneous tumour, the MED15::ATF1-rearranged tumour, and the
  dermal clear cell tumours with melanocytic differentiation. The WHO skin volume files the first among
  the soft tissue tumours of the skin, and Sargen leaves open whether they are melanomas or clear cell
  sarcomas, so Group IX is a candidate. **Evidence:** `XId_melanoma` — Goldman-Lévy 2025, PDF pp. 4, 11;
  Sargen 2026, PDF p. 3.
- **Parathyroid (Q115).** A report that names only "parafibromin-deficient parathyroid neoplasm". The
  evidence proposes no registration until a report states carcinoma. **Evidence:**
  `XIf10_parathyroid_other_unspecified` — Erickson 2022, PDF p. 12.
- **Sinonasal tract (`cross_group_A` §6 item 5; not among the 140).** Olfactory carcinoma and IDH2-mutant
  sinonasal carcinoma, which Group IV's sinonasal referral names.

**(c) Excluded whatever the code; only the exclusion's label is in question.**
- **Lung and pleura (Q61).** Mesothelioma in situ (the WHO prints 9050/2) and fetal lung interstitial
  tumour (no code) are not registrable. **Evidence:** `XIf4_lung_pleura` — Sauter 2022, PDF p. 2; Pfister
  2022, PDF p. 14.
- **Stomach (Q56).** ICCR prints 8213/2 for serrated dysplasia, high grade, and 8144/2 for
  intestinal-type adenoma, high grade. The exclusion records 8148/2 Glandular intraepithelial neoplasia,
  high grade. **Evidence:** `XIf2_XIf3_digestive` — ICCR Stomach, PDF p. 14.
- **Conjunctiva (Q29).** A conjunctival melanocytic intraepithelial lesion. Is its exclusion named 8741/2
  Precancerous melanosis, NOS? **Evidence:** `XId_melanoma` — Milman 2023, PDF pp. 3, 5.

**Built until you rule:** D4, apart from the two drafts in (a).

**If you rule otherwise:** each entity you code gains an option or a picker entry, and goes on the
REDCap-side list in `docs/TODO.md` if REDCap lacks the code.

### A19. Thyroid-type carcinoma in struma ovarii (Q124)

A follicular or papillary thyroid carcinoma that arises in struma ovarii. Should it record 9090/3 Struma
ovarii, malignant, which Group X records in Xc2? Or the thyroid code at C56.9: 8330/3 Follicular
carcinoma, NOS and 8340/3 Papillary carcinoma, follicular variant fall in XIb under ICCC-2017 range 121,
while 8260/3 Papillary adenocarcinoma, NOS at the ovary falls in Xd.

**Built until you rule:** Group X's ovary tree records 9090/3. Group XI offers no thyroid code at C56.9.

**Evidence:** `cross_group_A` §4(b); `XIb_thyroid`, conflicts and data gap 6 (WHO Female Genital
Tumours, monodermal teratoma chapter).

**If you rule otherwise:** Group X's ovary tree refers a named thyroid-type carcinoma to Group XI at
C56.9. That is a Group X change, handed to that session.

### A20. 8158/3 at the adrenal cortex (D16; Q1)

ICCC-2017 range 118 places 8158/3 ACTH-producing tumor in XIa at C74.0, under the obsolete term
"Endocrine tumor, functioning, NOS", which REDCap still uses as the label. No source describes an
adrenocorticotropic hormone-producing adrenal cortical tumour. Adrenocorticotropic hormone-producing
tumours drive adrenal hyperplasia from elsewhere, and adrenal cortical carcinoma causes
adrenocorticotropic hormone-independent hypercortisolism. Rule K gives 8370/3 Adrenal cortical carcinoma for a functioning adrenal
cortical carcinoma. Keep 8158/3 off the adrenal cortex screens and off the evidence gate's marker route?

**Built until you rule:** D16. Off the adrenal screens, kept in the inventory.

**Evidence:** `XIa_adrenal_cortex` — Mete 2022, PDF p. 2; ICCR Adrenal Cortex, PDF p. 1; contract §0.5
(Visser Table 4 has no adrenal cortical row).

**If you rule otherwise:** the adrenal histology screen offers 8158/3 for a functioning tumour.

### A21. Group X's ovary picker records 8452/3 (Q139)

Group X's ovary picker offers 8452/3 Solid pseudopapillary neoplasm of pancreas. ICD-O-3.2 codes the
ovarian tumour 8452/1 Solid pseudopapillary tumor of ovary. A /1 tumour of the ovary can therefore be
recorded as malignant. Hand the fix to the Group 10 session?

**Built until you rule:** Group XI offers 8452/3 at the pancreas only. Group X's file is unchanged on
this branch.

**Evidence:** `cross_group_B` §4, row 21; `icdo32.sqlite`.

**If you rule otherwise:** if you approve, Group X's picker drops 8452/3 and its exclusion screen gains
8452/1.

### A22. Basis of diagnosis in three situations (D8, D15; Q24, Q76, Q77)

- **A melanoma known only from a deposit (Q24).** ICD-O-3.1 Table 26 has basis 6, histology of a
  metastasis. D15 lists no 6. **Built:** basis 7. The melanoma draft used 6.
- **A cytology report that names NUT carcinoma, with a NUT stain on the cell block (Q76).** **Built:**
  basis 5 under D8. D15 counts immunohistochemistry as 7, so the cell block stain is the open point.
- **A NUTM1 break-apart fluorescence in situ hybridisation result that names no fusion partner (Q77).**
  **Built:** basis 8. The NUT rule counts a rearrangement shown by in situ hybridisation, reverse
  transcription polymerase chain reaction or sequencing, with or without a named partner.

**Evidence:** `XId_melanoma` — ICD-O-3.1, Table 26, printed p. 27; Goldman-Lévy 2025, PDF p. 10.
`NUT_carcinoma` — Lemelle 2022, PDF pp. 6–7; Luo 2025, PDF pp. 2, 7.

**If you rule otherwise:** D15 gains basis 6 for every deposit route in every Group XI tree, or the NUT
rules change basis.

---

## B. What is built and how the clerk reaches it

### B1. Which entities are options and which wait in the picker (D1)

Your ruling of 8 October 2026 put every code without paediatric evidence in a per-site picker, and the
papers fetched that day moved many entities onto the histology screens. D1 makes an entity an option
when a source reports it at ages 0 to 18. Its exception makes an entity an option wherever it occurs
when its code depends on a further answer (invasion, subtype, grade, human papillomavirus status,
behaviour), because the picker cannot ask that question.

**Settled by the ruling and the papers:**
- **Colorectum (Q48).** Mucinous adenocarcinoma 8480/3, signet ring cell carcinoma 8490/3,
  adenocarcinoma 8140/3, adenocarcinoma in adenomatous polyposis coli 8220/3 and tubular adenocarcinoma
  8211/3 are options (Polat 2021; Mahajan 2022). Medullary carcinoma 8510/3 has no paediatric report and
  stays in the picker.
- **Lung (Q57).** Carcinoid (8240/3 Neuroendocrine tumor, NOS), atypical carcinoid (8249/3 Neuroendocrine tumor, grade 2) and mucoepidermoid carcinoma 8430/3 are
  options, as are adenocarcinoma, squamous cell, small cell, large cell and large cell neuroendocrine
  carcinoma (Ozkan 2024, PMC section 2; Chen 2026, PMC sections 2, 9–10).
- **Breast (Q78; addendum gap 1).** Secretory carcinoma 8502/3 is the commonest invasive breast carcinoma
  in children, and it is an option. So are 8500/3 Infiltrating duct carcinoma, NOS, 8520/3 Lobular carcinoma, NOS, 8510/3 Medullary carcinoma, NOS, 8530/3 Inflammatory carcinoma and
  8021/3 Carcinoma, anaplastic, NOS (Sosnowska-Sienkiewicz 2024, PMC section 72).
- **Breast (Q83; addendum gap 2).** 9020/3 Phyllodes tumor, malignant occurs in adolescents and stays on
  the fibroepithelial screen (Sosnowska-Sienkiewicz 2024, PMC sections 2, 76).
- **In part:**
  - skin: basal cell carcinoma 8090/3 and squamous cell carcinoma 8070/3 are options (Q31; Huang 2019;
    Kaloga 2016);
  - thymus: the thymoma types, 8580/3 Thymoma, NOS to 8585/3 Thymoma, type B3, are options (Q64; Rossi 2022);
  - vulva: squamous cell carcinoma is an option (Q87; Wohlmuth 2021);
  - bladder: invasive urothelial carcinoma 8120/3 is an option (Q92; Liu 2025);
  - salivary gland: secretory carcinoma, adenoid cystic carcinoma 8200/3 and polymorphous adenocarcinoma
    8525/3 are options (Perez-de-Oliveira 2025);
  - pancreas: the neuroendocrine tumours are options (Karges 2025).

**Open (a): the D1 exception makes these options without a paediatric source. Confirm the exception.**
- **Thyroid (Q7).** Follicular carcinoma with its invasion screen: 8330/3 Follicular carcinoma, NOS, 8335/3 Follicular carcinoma,
  minimally invasive, 8339/3 Follicular carcinoma, encapsulated, angioinvasive. The evidence draft put them in the picker.
- **Oropharynx (Q16).** Squamous cell carcinoma with the human papillomavirus screen: 8085/3 Squamous cell carcinoma, HPV positive,
  8086/3 Squamous cell carcinoma, HPV negative, 8070/3 Squamous cell carcinoma, NOS.
- **Cervix and vagina (Q87, remainder).** Squamous cell carcinoma with the human papillomavirus screen.
  The female genital draft kept these in the picker.
- **Head and neck (Q105).** Squamous cell carcinoma and its WHO subtypes stay answers on the screen. The
  only paediatric evidence is indirect: Fanconi anaemia, and laryngeal papillomatosis turning malignant.

**Open (b): no paediatric source yet, so these wait in the picker (D1).**
- **Skin (Q31, remainder).** Merkel cell carcinoma 8247/3, pilomatrical carcinoma 8110/3, the adnexal
  carcinomas, and the named subtypes of basal cell and squamous cell carcinoma.
- **Thymus (Q64, remainder).** Thymic carcinoma 8586/3 and its types, the thymic carcinoids, and
  metaplastic thymoma. Fetch Stachowicz-Stencel 2015 (part D)?
- **Eye (Q104).** Conjunctival squamous cell carcinoma and lacrimal adenoid cystic carcinoma. Sthapit 2025
  would settle the first (D1).
- **Parathyroid (Q113).** Parathyroid carcinoma (8140/3). **Built:** an option, on indirect evidence.
  Pfister lists parathyroid tumours and the hyperparathyroidism-jaw tumour syndrome, and ICCR gives that
  syndrome a lifetime carcinoma risk of about 15%. Ozolek 2021 would settle it (D1). **Evidence:**
  `XIf10_parathyroid_other_unspecified` — Pfister 2022, PDF pp. 14, 19; ICCR Parathyroid, PDF p. 5.
- **Unknown primary (Q118).** 8070/3 Squamous cell carcinoma, NOS, 8020/3 Carcinoma, undifferentiated, NOS,
  8246/3 Neuroendocrine carcinoma, NOS and 8140/3 Adenocarcinoma, NOS are in the
  picker, beside the Carcinoma, NOS option. Contract §4.2 allows the generic adenocarcinoma and squamous
  options "where the site has them".

**Open (c): how thin may the evidence be? The addendum treated each of these as enough for an option.**
- **Salivary gland (addendum gap 2).** Adenoid cystic carcinoma and polymorphous adenocarcinoma rest on
  one comparative sentence with no count, and their order on the screen has no source (Perez-de-Oliveira
  2025, PMC section 5).
- **Salivary gland (addendum gap 8).** That paper pools ages 0 to 19, not 0 to 18.
- **Bladder (addendum gap 7).** Invasive urothelial carcinoma rests on a discussion sentence in Liu 2025
  that reviews other studies; Liu's own 17 children had no carcinoma (PMC sections 7–8). The option also
  shows at the renal pelvis, ureter and urethra, which Liu excluded (gap 8).
- **Skin (addendum gap 4).** Neither paper calls basal cell or squamous cell carcinoma the commoner, so
  both are "occurs" and the order follows Huang's counts.
- **Female genital tract (addendum gap 8).** Wohlmuth 2021's counts are only in Figure 1, an image.
  Clear cell adenocarcinoma at the vagina still rests on the title of Herbst and Scully 1970.
- **Digestive tract (addendum gaps 3, 4, 7, 8).**
  - Neuroendocrine tumour, grade 3 of the appendix (8249/3) rests on Pfister's general listing.
  - Pancreatic acinar cell carcinoma (8550/3) rests on Pfister alone.
  - Tubular adenocarcinoma (8211/3) rests on one mixed mucinous and tubular tumour, which records 8480/3
    by Rule K.
  - The five colorectal options also show at the anus (C21.0 to C21.8), where no paper reports a child.

**Built until you rule:** D1 and its exception, as listed.

**If you rule otherwise:** a stricter test (a paediatric case series that counts the entity) moves the
thin-evidence options back to the picker. A looser one (any WHO paediatric listing) moves the open (b)
entities onto the screens. Neither changes a code: each entity keeps its code and changes only its
place.

### B2. The generic fallback options have no paediatric source (addendum)

Every histology screen offers 8010/3 Carcinoma, NOS for a report that names no type. The salivary
screen also offers 8140/3 Adenocarcinoma, NOS, and the lung screen 8720/3 Malignant melanoma, NOS. No
paediatric paper reports any of them. Nine addendum items from seven parts asked whether a fallback
needs one: skin, salivary gland (8010/3 and 8140/3), lung (8010/3 and 8720/3), thymus, breast, female
genital tract and urinary tract.

**Built until you rule:** contract §4.2 places the generic options on every histology screen, and D13
lets every tree reach the melanoma tree.

**Evidence:** addendum, `still_unreported_options` in each part; for example `XIf4_lung_pleura` data
gap 6.

**If you rule otherwise:** the fallbacks move to the pickers. A report that names no type then has no
route on the screen, and the clerk must search the picker for "Carcinoma, NOS".

### B3. NUT carcinoma as an option on the nasopharynx and salivary gland trees (D12; Q75)

The WHO paediatric volume lists NUT carcinoma among the head and neck tumours. A child case is reported
in the lung, the mediastinum, and the nasal cavity and sinuses. Is the listing enough to make 8023/3 Nuclear protein in testis (NUT)-associated carcinoma an
option on the nasopharynx and salivary gland trees?

**Built until you rule:** D12. 8023/3 is an option on the nasal cavity, nasopharynx, salivary gland,
lung, thymus and mediastinum, and skin trees, and a picker entry elsewhere. The NUT evidence draft had
the salivary gland and skin as picker entries.

**Evidence:** `NUT_carcinoma` — Pfister 2022, PDF p. 14; Luo 2025, PDF pp. 12–13; Lemelle 2022, PDF
p. 8.

**If you rule otherwise:** 8023/3 moves to the picker on the trees you name.

### B4. Meningeal melanocytoma and meningeal melanocytosis (Q26, Q123)

8728/1 Meningeal melanocytoma and 8728/0 Meningeal melanocytosis have no ICCC-2017 group: XId is
behaviour 3, and no Group III range holds 8728. Group III's meningeal lesion triage
(`group_03_dt.json`) refers both to Group XI. Should they be behaviour exclusions in the melanoma tree,
or registered as non-malignant intracranial tumours?

**Built until you rule:** exclusions in the melanoma tree. 8728/3 Meningeal melanomatosis is registered
in XId.

**Evidence:** `XId_melanoma` — Pfister 2022, PDF pp. 16, 18; `cross_group_A` §1.3, branch 4.

**If you rule otherwise:** both are registered. That is a registry policy for non-malignant
intracranial tumours outside ICCC, and it needs a Group III change.

### B5. The front door (Q128, Q135)

On the guided route, `app.js` narrows a presentation's group list by the site's list. Two questions
follow.
- **Sites.** Should 11 be added to the site lists? Contract §3.1 adds 153 lookup codes with candidate
  group 11, and adds 11 to 65 existing codes. Those include C74.0, C69.x, C30–C31, C38.1–C38.3, C48
  and the brain, C70–C72. `cross_group_A` proposed leaving the brain sites unchanged: a carcinoma there
  is nearly always a deposit, and the brain would then offer Groups III, X and XI.
- **Presentations.** Contract §3.2 does not name them. Without 11 on "Mass / swelling", the thyroid's
  list (2, 10, 11) narrows to (2, 10), and Group XI cannot be reached on the guided route. Without 11 on
  "Cutaneous / mucosal lesion", melanoma of the skin cannot be reached. Without 11 on "Lymphadenopathy",
  a nasopharyngeal carcinoma that presents with neck nodes is never offered Group XI. `cross_group_A`
  proposes adding 11 to those three presentations and leaving "Organ-functional sign" alone. Adding 11
  there would remove Group IX at the bladder, biliary tract, female genital sites, prostate and
  nasopharynx (the F-H-12 effect).

**Built until you rule:** contract §3.1 and §3.2. Both mechanisms in Q135 are applied: the site lists,
and `occurs_at_routed_sites` for the search box. The presentations wait for you.

**Evidence:** `cross_group_A` §2.5, §3.3 and §6 item 7. Group X review, part F: under your delegation,
Group X was not added at the kidney, liver, bone and soft tissue, to keep a family question off the
commonest childhood masses.

**If you rule otherwise:** 11 comes off the site lists you name. The search box still enters Group XI
there through `occurs_at_routed_sites`.

### B6. The alias layer (Q131–Q134, Q138, Q140)

The alias map proposes six changes.
1. **Group 10's picker-only carcinoma aliases (Q131).** Group 10 holds 183 of them on 75 codes:
   "Papillary carcinoma of thyroid", "Hurthle cell carcinoma", "Mucoepidermoid carcinoma",
   "Lymphoepithelioma", "NUT carcinoma", and the squamous and small cell families. **Planned:** Group 11
   takes them and Group 10's generator drops them. Typed at the ovary or testis, they then stop; the
   Group X picker still finds them through its own filter box. The engine gate's picker sweep is re-keyed
   first.
2. **49 strings on 13 codes that Group 10 also emits on named options (Q132).** Among them are
   "Carcinoma, NOS", "Adenocarcinoma, NOS" and the neuroendocrine, mucinous and clear cell strings. Filed
   in both groups, they stop the case at 27 shared sites, the thyroid, lung and thymus among them. Left
   with Group 10, they send those sites through the germ cell tree first. **Planned:** they stay with
   Group 10, and an engine tie-break is requested from the "ICD Overall fixes" session: keep only the
   groups whose own entries list the site. **Asked:** approve the request?
3. **Group 6's nine strings (Q133).** "Medullary carcinoma, NOS", "Vipoma", the urothelial variants and
   8504. Group 6 reads no site, so today each enters Group 6 everywhere. Shared, they would enter Group 6
   at the kidney and Group 11 at its own sites, and stop where neither group is listed. **Held:** Group 11
   does not file them until you rule.
4. **Group 3's four strings (Q134).** "ACTH-producing tumor", "Oncocytic carcinoma", "Oxyphilic
   adenocarcinoma" and "Papillary carcinoma, follicular variant". **Planned:** Group 11 files them; they
   tie at C75.1 until the tie-break lands. The Group 3 session is asked to delete its three code-less
   thyroid strings.
5. **Organ lay terms and organ-naming terms on shared codes (Q138).** The lay terms are "Thyroid
   cancer", "Skin cancer", "Lung cancer" and "Nasopharyngeal carcinoma". The shared-code terms include
   "Parathyroid carcinoma" and "Acinar adenocarcinoma of prostate" on 8140/3 Adenocarcinoma, NOS. **Planned:** code-less
   aliases, which are searchable and never shown under "Also called". **Other choices:** leave them out,
   or request an engine change that keys "Also called" by site.
6. **"Adrenal cancer" and "ACC" (Q140).** Neuroblastoma is the commonest adrenal malignancy of
   childhood, and "ACC" names three Group XI entities: adrenal cortical carcinoma, adenoid cystic
   carcinoma and acinic cell carcinoma. **Planned:** neither is an alias.

**Built until you rule:** contract §6 and `cross_group_B` §1.2 to §1.6.

**Evidence:** `cross_group_B` §1.

**If you rule otherwise:** the generator files or drops the strings you name, and the engine request
is withdrawn if you refuse it.

### B7. Other groups' files (Q129, Q130)

- **Referral reasons (Q129).** Five referral reasons in Groups VII and X say that carcinomas of other
  organs are Group XI. That is false for renal carcinoma (VIb), cholangiocarcinoma (VIIb at any site)
  and a carcinoma at the liver. Group III's meningeal triage also calls meningeal melanocytoma XId (B4).
  Correct them on this branch, or hand them to their sessions?
- **Router rules (Q130).** The router rules for 8158 and 8290 default to Group 11 and lack ICCC
  branches: 8158 is Xd at C56.9, and 8290 is Xd at C56.9 and C62.x and VIb at C64.9. The rules feed only
  the output's "Group routing" note, so no case enters the wrong group, but the note can name Group 11
  wrongly.

**Built until you rule:** contract §7 and §3.2.
- The reasons are handed to the Group VII, Group X and Group III sessions.
- The two router rules are resolved at C74.0 and C73.9 only, and every other branch is left to its
  owner.

**Evidence:** `cross_group_A` §1.3 and §2.2.

**If you rule otherwise:** this branch edits the five reasons and adds the ovary, testis and kidney
branches. Each change is listed in the build report.

### B8. Placement questions the build settles without a ruling

These came from the evidence and the addendum. None changes a code. They are listed so you can object.
- **Topography headings (Q136).** The 31 missing headings (oral cavity, salivary glands, stomach,
  colorectum, pancreas, larynx, breast and others) are added as crosswalk rows (contract §3.1).
- **Picker copies (skin gap 5, breast gap 6, urinary gap 10).** D2 removes from each picker the codes the
  tree already offers as options. Their ICD-O-3.2 synonyms stay searchable through the aliases. The
  breast's microinvasion answer, which leads to the picker, keeps 8500/3 Infiltrating duct carcinoma, NOS reachable there.
- **Tubular adenoma of the breast (breast gap 8).** The exclusion screen gains 8211/0 Tubular adenoma,
  NOS. Otherwise a clerk who searches "tubular" finds only 8211/3 Tubular adenocarcinoma and records a
  benign tumour as malignant.
- **Solid pseudopapillary neoplasm without nuclear beta-catenin (digestive gap 9).** Ebrahim 2025 reports
  one paediatric case. The stain rule must not stop a report that names the tumour.
- **Lung (gaps 8, 9, 10).**
  - A screen entry for mature teratoma, 9080/0 Teratoma, benign.
  - The Rule K hint on the histology screen, which D5 and your ruling of 7 October 2026 govern.
  - Paediatric examples in the lymphoma and sarcoma referral labels.
- **Thymus (gap 7).** NUT carcinoma's place among the thymoma options.
- **Breast (gaps 9, 10).**
  - A breast deposit is commoner than a primary in children (Sosnowska-Sienkiewicz 2024, PMC section 67);
    the deposit answer's position follows that.
  - Gynaecomastia, fibrous nodule, hamartoma, cyst, fibrocystic change and abscess have no ICD-O-3.2
    breast code. 9016/0 Giant fibroadenoma and 9020/1 Phyllodes tumor, borderline are not reported in
    children.
- **Female genital tract (gap 9).** Wohlmuth 2021's vulval melanoma in girls is carried to the melanoma
  tree.
- **Skin (gap 3).** No source gives recognition text for basal cell carcinoma, so its option carries no
  aid.

---

## C. Site, group and subgroup

### C1. Rule H and Rule B site corrections (D9; Q6, Q13, Q47, Q65, Q101)

Rule H uses the site ICD-O-3.2 prints beside a term when the report states none, and disregards it when
the tumour is known to arise elsewhere (ICD-O-3.1, printed p. 15). Rule B sends a "peri-" or "region of"
site to C76 unless the tumour type shows its tissue (printed p. 14).

- **Adrenal (Q6).** An adrenal cortical carcinoma recorded at C74.9 Adrenal gland, NOS. **Built:**
  corrected to C74.0 Cortex of adrenal gland; ICD-O-3.2 prints C74.0 beside every 8370 term.
  **Evidence:** `XIa_adrenal_cortex`, Rule H row.
- **Thymus (Q65).** A thymoma, thymic carcinoma or thymic carcinoid that the report places in the
  anterior mediastinum, the mediastinum or the chest. **Built:** C37.9 Thymus. ICD-O-3.2 prints C37.9
  beside 8580 to 8586, and these tumours arise in the thymus. **Other choice:** the stated site, C38.1 or
  C38.3. Only the topography and the subgroup change (XIf5 against XIf10). **Evidence:**
  `XIf5_thymus_mediastinum` — ICCR Thymic Epithelial, PDF p. 8.
- **Thyroid (Q13).** A thymoma or thymic carcinoma found within the thyroid. **Built:** picker entries at
  C73.9, where ICCC-2017 gives 8580 to 8586 no group. **Other choice:** C37.9. **Evidence:** `XIb_thyroid`
  — ICCR Thyroid, PDF p. 3; Juhlin 2022, PDF p. 7.
- **Conjunctiva (Q101).** A sebaceous carcinoma the report places in the conjunctiva or caruncle itself.
  **Built:** sent to the skin tree at the eyelid, C44.1 (XIe), because the WHO eye volume moved sebaceous
  carcinoma to the eyelid chapter. **Other choice:** the stated site, C69.0 Conjunctiva (XIf9), which
  Rule H's second sentence favours. **Evidence:** `XIf9_eye` — Milman 2023, PDF pp. 7, 9.
- **Parotid (Q47).** A salivary gland carcinoma the report places "around" or "in the region of" the
  parotid. **Built:** the "region of a salivary gland" answer records C76.0 Head, face or neck, NOS, and
  its reason adds "unless the tumour type shows origin in the gland". **Asked:** does a salivary gland
  carcinoma's type show that, which would give C07.9 Parotid gland? **Evidence:** `XIf1_salivary`, Rule B
  row.

**Built until you rule:** D9, as listed.

**If you rule otherwise:** the `site_resolution` node of each tree records the site you name.

### C2. A tumour found only in a lymph node, or at a site no Group XI range covers (D10; Q35, Q116, Q117, Q125, Q126, Q127)

ICCC-2017 places no Group XI carcinoma code at bone, marrow, peripheral nerve, soft tissue, lymph nodes or
the adrenal gland NOS (`cross_group_A` §5.2).

- **Any such site (Q125).** Must the tool always ask for the primary, and record C80.9 Unknown primary
  site (XIf11) when it is unknown? **Built:** D10. The deposit question asks for the primary, an unknown
  primary records C80.9, and a carcinoma or melanoma primary re-enters Group XI at its own site.
- **Merkel cell carcinoma in a lymph node with no skin primary (Q35).** ICCR calls this T0. Is the site
  C44.9 Skin, NOS by Rule H, or C80.9? **Built:** D10, C80.9. **Evidence:** `XIe_skin_carcinoma`,
  registrar question 6 (ICCR Merkel Cell staging, T0); ICCR Merkel Cell, PDF p. 7 for the entity.
- **A melanoma in a lymph node with no known primary (Q126).** At the node (C77.x, XId) or C80.9?
  **Built:** C80.9; XId covers every site, so the case stays in Group XI. **Evidence:** `XId_melanoma` —
  Goldman-Lévy 2025, PDF p. 10.
- **A neck node carcinoma, primary unnamed, positive for Epstein-Barr virus RNA or for p16 or high-risk
  human papillomavirus (Q116).** The WHO defines true carcinoma of unknown primary as negative for both,
  and Epstein-Barr virus RNA correlates with a nasopharyngeal origin. **Built:** C80.9 unless the report
  or clinician names the organ. **Other choice:** Epstein-Barr virus RNA alone records C11.9 Nasopharynx,
  NOS, and p16 or human papillomavirus records the oropharynx. **Evidence:**
  `XIf10_parathyroid_other_unspecified` — Hernandez-Prera 2022, PDF pp. 2, 8; `XIc_nasopharynx` — ICCR
  Oropharynx and Nasopharynx, PDF p. 3.
- **Heterotopia-associated salivary carcinoma in a neck node (Q117).** Topography: C77.0 (no Group XI
  range), C76.0, or the salivary gland. Morphology: the salivary type (for example 8430/3
  Mucoepidermoid carcinoma), or 8010/3 Carcinoma, NOS, where ICD-O-3.2 lists "Heterotopia-associated
  carcinoma". **Built:** held. **Evidence:** `XIf10_parathyroid_other_unspecified` — Hernandez-Prera 2022,
  PDF pp. 6–7.
- **Group X's ovary deposit answer "The primary is not known" (Q127).** It goes to Group XII. Should a
  carcinoma or melanoma of unknown primary go to Group XI instead (XIf11 or XId at C80.9)? **Built:** Group
  X unchanged on this branch (contract §7). **Evidence:** `cross_group_A` §1.3, branch 13.

**If you rule otherwise:** the deposit and node answers record the site you name, and Group X's answer
is handed to its session.

### C3. NUT carcinoma in the mediastinum (D12; Q66)

Marx 2022 places NUT carcinoma in the WHO table of thymic epithelial tumours and says nothing about its
site. Record an anterior mediastinal NUT carcinoma at C37.9 Thymus, or at the stated mediastinal site?

**Built until you rule:** D12. The site the report gives: C37.9 only when the report names the thymus,
otherwise C38.1 to C38.3.

**Evidence:** `XIf5_thymus_mediastinum` — Marx 2022, PDF p. 4; `NUT_carcinoma` — Luo 2025, PDF p. 2.

**If you rule otherwise:** the thymus tree's site question records C37.9 for an anterior mediastinal
NUT carcinoma, and the subgroup becomes XIf5 instead of XIf10.

### C4. Which tree serves a site (Q38, Q111, Q112, Q121)

- **C51.9 Vulva, NOS, C60.9 Penis, NOS and C63.2 Scrotum (Q38, and the second half of Q88).** ICCC-2017
  makes all three skin sites (XIe). **Built:** the skin tree (contract §4.1). The female genital and
  male genital trees take C51.0 to C51.8 and C60.0 to C60.8.
- **Middle ear (Q111).** C30.1 has no source in this part. **Built:** the head and neck tree's pharynx and
  larynx screens. **Other choice:** wait for the summary of the WHO ear chapter (part D3).
- **Base of tongue C01.9, lingual tonsil C02.4, soft palate C05.1 and uvula C05.2 (Q112).** The WHO oral
  chapter covers the oral cavity and mobile tongue only. **Built:** the oral cavity screens of the head
  and neck tree. **Other choice:** the oropharynx screens with the human papillomavirus question.
  **Evidence:** `XIf10_head_neck`, conflict 11.
- **Pituitary C75.1 and pineal gland C75.3 (Q121).** ICCC-2017 places carcinoma codes there in XIf10.
  **Built:** the Group XI endocrine tree leaves both out, and pituitary and pineal tumours go to Group III.

**Built until you rule:** contract §4.1.

**If you rule otherwise:** the router's `tree_routing` lists move the sites you name.

### C5. The subgroup where ICCC-2017 names none (D11; Q5, Q74, Q88, Q99, Q122)

Standing rule 3 keeps a valid ICD-O-3.2 code in the group that offers it. D11 gives a code from the
shared carcinoma list its default subgroup, XIf10, at a site no Group XI range covers. A code with a
single ICCC subgroup keeps it at every site.

- **Adrenal (Q5).** 8010/3 Carcinoma, NOS at C74.0 or C74.9, the fallback when steroidogenic factor 1
  (SF1) is negative or not reported. XIa or XIf10? **Built:** XIf10.
- **NUT carcinoma at bone, soft tissue, peripheral nerve or adrenal (Q74).** XIf10, or unclassified?
  **Built:** XIf10.
- **Vulva (Q88).** At C51.9, a skin site, ICCC-2017 holds no range for 8085, 8086, 8482, 8380, 8500,
  8144, 8562, 8441, 8249 or 8045. At C51.0 to C51.8, the XIf10 list holds no range for 8090, 8400, 8409
  or 8413. **Built:** XIf10 for the shared-list codes, XIe for the skin codes.
- **Penis and scrotum (Q99).** 8083, 8084, 8085, 8086 and 8120 at C60.9, and 8090 at C60.0 to C60.8,
  fall in no range. **Built:** as for the vulva.
- **8158/3 ACTH-producing tumor and 8290/3 Oxyphilic adenocarcinoma at the brain and spinal cord, C70 to C72 (Q122).** ICCC range 135 leaves these
  sites out. **Built:** the picker does not offer either code there.

**Evidence:** `XIa_adrenal_cortex` code currency 8010; `NUT_carcinoma` data gap 5; `XIf7_female_genital`;
`XIf8_urinary_male_genital`; `XIf10_parathyroid_other_unspecified`; contract §0.1.

**Built until you rule:** D11.

**If you rule otherwise:** the entry's subgroup rules change. REDCap computes the subgroup from the code
and the site, so only the tool's output line changes.

### C6. No tissue, or no tumour type: 8000/3 and 8001/3 go to Group XII (D7; Q27, Q36, Q46, Q62)

ICCC-2017 places 8000/3 Neoplasm, malignant and 8001/3 Tumor cells, malignant in XIIb at every Group XI
site (IIIf at C70 to C72). The cases are:
- a melanoma recorded from imaging, or from a clinical note at a site other than the skin (Q27);
- a skin case on clinical or imaging evidence, or cytology with malignant cells of no named type (Q36);
- a salivary gland registration without tissue (Q46);
- a registration at the lung, pleura or heart without tissue or type (Q62).

Each is referred to Group XII with the code named, as Group X referred 8000/3 in the brain to Group III.
Confirm?

**Built until you rule:** D7. Group XII is not built, so the referral ends the case with the code shown.

**Evidence:** `XId_melanoma`, `XIe_skin_carcinoma`, `XIf1_salivary`, `XIf4_lung_pleura` — conflicts with
Group XII; contract §0.5.

**If you rule otherwise:** Group XI records 8000/3 itself, while ICCC-2017, and the subgroup REDCap
computes from code and site, still say XIIb.

### C7. Codes ICCC-2017 places in another group (Q37, Q40, Q52, Q91, Q108, Q120)

A code ICCC-2017 places in a different group is a conflict under standing rule 3, and the tree refers
it there. Confirm each referral:
- **Skin (Q37).** Malignant chondroid syringoma, which ICD-O-3.2 files as a related term of 8940/3
  Mixed tumor, malignant, NOS, and 8982/3 Myoepithelial carcinoma. Both go to XIIa4.
- **Salivary gland (Q40).** 8982/3 and 8980/3 Carcinosarcoma, NOS go to XIIa4. The WHO counts both among
  the salivary carcinomas.
- **Female genital tract (Q91).** 8980/3, 8933/3 Adenosarcoma, 8982/3, 8930/3 Endometrial stromal
  sarcoma, NOS and 9110/3 Mesonephroma, malignant go to XIIa4 and XIIa6. The WHO 2020 classifies
  carcinosarcoma and mesonephric adenocarcinoma as carcinomas.
- **Gallbladder and extrahepatic bile ducts (Q52).** 8160/3 Cholangiocarcinoma, 8161/3 Bile duct
  cystadenocarcinoma and 8162/3 Perihilar cholangiocarcinoma are VIIb at every site, so they go to
  Group VII. REDCap offers all three in Group XI.
- **Nose and sinuses (Q108).** Teratocarcinosarcoma, a related term of 9081/3 Teratocarcinoma, is Xb2 in
  Group X, although its germ cell markers are negative and the WHO lists it among the sinonasal
  carcinomas.
- **Peritoneum (Q120).** 8474/3 Seromucinous carcinoma is Xd at every site and goes to Group X. The
  currency check lists it under XIf10; that line in the vault document needs correcting.

**Built until you rule:** each referral as listed, with standing rule 3.

**Evidence:** `XIe_skin_carcinoma` — Goldman-Lévy 2025, PDF p. 6. `XIf1_salivary` — ICCR Major Salivary
Glands, PDF p. 8; Skálová 2022, PDF p. 2. `XIf7_female_genital` — ICCR Cervix, PDF pp. 18–20; ICCR
Endometrial, PDF p. 9. `XIf2_XIf3_digestive` — ICD-O-3.1, printed p. 24. `XIf10_head_neck` — ICCR Nasal
Cavity, PDF p. 8; Thompson 2022, PDF pp. 7–8.

**If you rule otherwise:** a code you keep in Group XI conflicts with ICCC-2017, and needs a
registry-local recode.

---

## D. Sources you could supply

### D1. Four papers whose publisher blocks the PubMed Central text

The controlling session fetched 13 paediatric papers on 8 October 2026. Four came back with "the
publisher does not allow downloading of the full text":

| Paper | PubMed Central | Would settle |
|---|---|---|
| Ozolek JA. Selected topics in the pathology of the thyroid and parathyroid glands in children and adolescents. Head Neck Pathol 2021;15(1):85–106. doi:10.1007/s12105-020-01274-5 | PMC8010056 | Follicular thyroid carcinoma and the rarer thyroid types in children (B1, Q7); parathyroid carcinoma in children (B1, Q113) |
| Cortes-Santiago N, et al. Review of pediatric head and neck neoplasms that raise the possibility of a cancer predisposition syndrome. Head Neck Pathol 2021;15(1):144–158. doi:10.1007/s12105-021-01292-x | PMC8010005 | Head and neck squamous cell carcinoma in children (B1, Q105); skin carcinomas (B1, Q31) |
| Cole GG, et al. Morphologic and ancillary studies of pediatric acinic cell carcinoma: a single institute experience. Head Neck Pathol 2023. doi:10.1007/s12105-022-01492-z | PMC10063734 | Report vocabulary and stains for paediatric acinic cell carcinoma, 8550/3 Acinar cell carcinoma |
| Sthapit PR, et al. Pediatric ocular surface squamous neoplasia in the absence of known risk factors and systemic conditions: a case series. Ocul Oncol Pathol 2025. doi:10.1159/000546002 | PMC12143885 | Conjunctival squamous cell carcinoma in children (B1, Q104) |

The European Cooperative Study Group for Pediatric Rare Tumours (EXPeRT) and PARTNER recommendations of
2021 are not in PubMed Central. They cover colorectal carcinoma, pancreatic tumours and neuroendocrine
neoplasms in children (Pediatric Blood & Cancer 2021, supplement; the citation is unverified), and would
settle digestive data gaps 1, 3 and 4. The same group's thymic tumour report, Stachowicz-Stencel 2015
(Eur J Cancer 2015;51(16):2444–2452), would settle the thymic carcinomas (B1, Q64; thymus data gap 1).

### D2. The WHO volumes the data gaps name

| Volume | Chapter or table | Settles | Data gap |
|---|---|---|---|
| Paediatric Tumours, 5th edition (2022) | Thyroid; nasopharyngeal carcinoma; skin; salivary gland; thoracic (with the fetal lung interstitial tumour entry); breast (with juvenile papillomatosis's behaviour); female genital tract; parathyroid; head and neck; NUT carcinoma (pp. 908–909); carcinoma of unknown primary | B1; A18 (fetal lung interstitial tumour) | thyroid 1; nasopharynx 2; skin 1; salivary 1; lung 1, 4; breast 1, 2, 4, 10; female genital 2; parathyroid 1, 2; head and neck 1; NUT 1 |
| Endocrine and Neuroendocrine Tumours, 5th edition (2025) | Adrenal cortex, including cytology; thyroid chapters | A2 (Q3), A7 | adrenal 2, 4; thyroid 5 |
| Head and Neck Tumours, 5th edition (2024) | Nasopharyngeal carcinoma (chapter 4, mapping of lymphoepithelioma and Schmincke tumour); sinonasal code list (8044, 8051, 8483); salivary entity list (successors of 8440 and 8450; entity-defining genes); NUT carcinoma, Part A, pp. 65–67 | A1 (Q17), A13, A18 | nasopharynx 1; head and neck 2, 3, 6; salivary 3, 5; NUT 1 |
| Skin Tumours, 5th edition (2025) | Entity list with ICD-O codes; acral and mucosal melanoma chapters | A16, A18 (Q23, Q28) | skin 2; melanoma 2, 5 |
| Eye and Orbit Tumours, 5th edition (2023) | Code list; uveal melanoma; grades of conjunctival intraepithelial neoplasia | A1 (Q25), A4 (Q102) | eye 2, 3; melanoma 3 |
| Thoracic Tumours, 5th edition (2021) | NUT carcinoma, pp. 364–367; thresholds between typical carcinoid, atypical carcinoid and large cell neuroendocrine carcinoma | C3; B1 | NUT 1; lung 2; thymus 2 |
| Digestive System Tumours, 5th edition (2019) | Mesenchymal chapter: the code of malignant gastrointestinal neuroectodermal tumour | — | digestive 6 |
| Breast Tumours, 5th edition (2019) | Entity list: cystic hypersecretory carcinoma with invasion; malignant adenomyoepithelioma, 8983 or 8562 | A1 (Q81) | breast 3, 5 |
| Female Genital Tumours, 5th edition (2020) | Monodermal teratoma (struma ovarii); tumours of the peritoneum | A19 | thyroid 6; parathyroid 3 |
| Urinary and Male Genital Tumours, 5th edition (2022) | Urachal and neuroendocrine chapters; paratesticular and penile tumours (Moch 2022, Part A) | A4 (Q96) | urinary 3, 4 |
| Central Nervous System Tumours, 5th edition (2021) | Metastatic tumours; meningeal melanocytic tumours | B4; C2 | parathyroid 4; melanoma 4 |
| IARC/WHO Committee for ICD-O, updates after 2019 | Whether 8483, 8484, 9113, 8976, 8750, 8770/1, 8743/2 and 9050/2 are approved, and what ICCR's asterisk means | A12, A13, A15, A16, A18 | female genital 4; head and neck 3 |

### D3. Other papers and indexes the data gaps name

| Source | Settles | Data gap |
|---|---|---|
| Wieneke JA, et al. Am J Surg Pathol 2003;27:867–881; Picard C, et al. Mod Pathol 2019;32:546–559 | The ages the Wieneke criteria cover (A2, Q3) | adrenal 3 |
| Baloch ZW, et al. Endocr Pathol 2022;33:27–63 (ICD-O codes of the WHO thyroid classification); Francis GL, et al. Thyroid 2015;25:716–759 | A18 (Q12); B1 (Q7) | thyroid 1, 2 |
| Ali SZ, et al. Bethesda System 2023; Faquin WC, Rossi ED, Milan System, 2nd edition (2023) | Which cytology categories a registry may record (D8) | thyroid 4; salivary 4 |
| Rodriguez-Galindo C, et al. J Clin Oncol 2019 (Children's Oncology Group ARAR0331) | Nasopharyngeal carcinoma subtypes in children (A1, A3) | nasopharynx 2 |
| Bauer DE, et al. Clin Cancer Res 2012; Chau NG, et al. JNCI Cancer Spectr 2020; Barletta JA, et al. Am J Surg Pathol 2022; Agaimy A, et al. Am J Surg Pathol 2018; Haack H, et al. Am J Surg Pathol 2009 | NUT carcinoma sites and ages in children (B3, C3) | NUT 1–3 |
| Quixabeira series of 203 paediatric salivary carcinomas (cited by Perez-de-Oliveira 2025) | B1 (c), salivary order | salivary 1, 2, 8 |
| Alanee S, Shukla AR. BJU Int 2010;106:557–560; Paner GP, et al. Adv Anat Pathol 2011;18:79–89 | Invasive urothelial carcinoma in children (B1 (c)) | urinary 1, 7 |
| Rojas Y, et al. J Pediatr Surg 2015;50:1004–1008; Dishop MK, Kuruvilla S. Arch Pathol Lab Med 2008;132:1079–1103; Caplin ME, et al. Ann Oncol 2015;26:1604–1620 | Lung (A1 (c), Q60; A14, Q63) | lung 1, 3, 7 |
| Herbst AL, Scully RE, 1970 (vaginal adenocarcinoma in adolescence), full text | B1 (c), vagina | female genital 1 |
| Tellado MV, et al. Ophthalmology 1997 (lacrimal adenoid cystic carcinoma in childhood) | B1 (b), Q104 | eye 1 |
| Kutler DI, et al. Arch Otolaryngol Head Neck Surg 2003 (Fanconi anaemia); Agaimy A, et al. Am J Surg Pathol 2017 (SMARCB1-deficient sinonasal carcinoma); Thompson LDR, et al. Head Neck Pathol 2022 (ear); Lewis JS Jr. Head Neck Pathol 2022 (oropharynx) | B1 (a), Q105; A18, Q106; C4, Q111 and Q112 | head and neck 1, 2, 4, 5 |
| ICD-O-3.2 topography alphabetic index | Caruncle, retinal pigment epithelium, optic disc; heterotopic tissue; Skene gland; urethral glands | eye 4; parathyroid 5; female genital 6; urinary 5 |

---

## E. Decisions

Each ruling goes here with its date, in the form Group X review part E uses. Each ruling also
records the build change it makes and the check that proves it.

### E1. A1 (a) and (b): Rules A to K decide (8 October 2026)

Jay: "apply rules A-K -> Then based on its ruling, choose the appropriate option." Where ICD-O-3.2 and the
WHO table code a term differently, the twelve instances in A1 (a) and (b) are decided by the WHO ICD-O-3
coding Rules A to K (ICD-O-3.1 section 4, printed pp. 14–28), and the tree records the code the rules give.
The application, instance by instance with the manual's page, is
`docs/group_11_evidence/registrar_A1ab_rules.md`.

✅ **Built 8 October 2026.**
- Nasopharynx `np_npc_type`: the older names record 8082/3, a new option records 8020/3, and the Rule K order is in the hint.
- Thymus `ty_thymic`: split into 8576/3, 8410/3, 8012/3 and 8586/3; the picker keeps those codes.
- Sentences naming the rule were added on the salivary, female genital, urinary, melanoma and thymus screens.

**Proof:**
- `build_database.py`: 1,321 checks, 0 FAIL.
- `negative_controls_group11.py`: 20 of 20 caught.
- Walks of the six changed trees: 0 failures.
- Diff of `group_11_dt.json`: only these options and hints changed.

**Known effect:** the nasopharynx picker no longer lists 8082/3 and 8020/3, because the type screen now offers them.

### E2. A1 (c): recheck the evidence first (8 October 2026)

Jay: "(c) The WHO retired or downgraded the entity, and ICD-O-3.2 keeps a current term. That needs rechecking
and evidence confirmation." The three instances (lung bronchioloalveolar carcinoma, skin cribriform
carcinoma, lacrimal gland oncocytic carcinoma) stay held until the evidence is confirmed. The recheck is
`docs/group_11_evidence/registrar_A1c_recheck.md`.

### E3. A1 (c) ruled (8 October 2026) ✅

Jay, on the rechecked evidence (E2):

- **Lung.** "'Bronchioloalveolar carcinoma, non-mucinous' finds the current Preferred term, 8252/3. I agree."
  ✅ **Built:** the lung tree's hold on 8252/3 is released, so the lung picker (and the chest picker, which shares the
  hold) offers 8252/3 *Bronchiolo-alveolar carcinoma, non-mucinous*. Its label is the ICD-O-3.2 spelling, and ICD-O-3.2
  gives it no other live term to search by.
- **Skin.** "Cribriform carcinoma -> Do not add, note it down somewhere." ✅ **Done:** 8201/3 is not offered at the
  skin, and the ruling is noted in `docs/TODO.md` §35.9. Still open there: the skin exclusion line "Cutaneous
  cribriform tumour" carries behaviour /0, and the source says "indolent", not "benign".
- **Eye.** "Keep 8290/3 Oxyphilic adenocarcinoma, but are you sure its synonym is Oncocytic adenocarcinoma."
  ✅ **Confirmed and kept.** `icdo32.sqlite` and the IARC source workbook (`ICD-O-3.2_final_update09102020.xls`,
  rows 585–587) agree: 8290/3 has the Preferred term *Oxyphilic adenocarcinoma* and two Synonyms, *Oncocytic
  adenocarcinoma* and *Oncocytic carcinoma*, neither `[obs]`. The eye picker already offered 8290/3 with both
  synonyms as search terms; the review's "not in the eye picker" described the evidence draft, not the build.

**Proof:**
- `build_database.py`: 1,321 checks, 0 FAIL.
- `negative_controls_group11.py`: 20 of 20 caught.
- Walks of `g11_lung` and `g11_thoracic`: 0 failures.

### E4. 8290/3: the other names are aliases (8 October 2026) ✅

Jay: "Then add Oxyphilic adenocarcinoma, add other names as aliases. Synonyms are aliases by the way!"

The Group 11 alias generator already writes every live ICD-O-3.2 term of every code the trees offer, including the codes
in the pickers. It skipped 8290/3's six terms because Groups 3 and 10 already held them. A search for any of them therefore
entered Group III or Group X and stopped at the thyroid, the eye and every other Group XI site.

✅ **Built.**
- `build/generate_group11_aliases.py` gains `SHARED_BY_RULING`. Group 11 now holds all six terms although another group
  holds them too.
- *Oxyphilic adenocarcinoma*, *Oncocytic adenocarcinoma* and *Oncocytic carcinoma* map to 8290. They print under "Also
  called" on every 8290/3 output.
- *Hurthle cell carcinoma*, *Hurthle cell adenocarcinoma* and *Follicular carcinoma, oxyphilic cell* are printed with C73.9 in
  ICD-O-3.2, so they are site-associated (Rule H). They are code-less aliases that enter the thyroid tree, as the other
  organ terms do (cross_group_B C15). They do not print under "Also called" at the eye or the salivary gland.
- Group 10's generator yields a picker-only term another group holds (its rule 8), so its file drops its four 8290 terms.
  Group 3 keeps its two. Those two are filed under Groups 3 and 11, and the site settles them.

**Known effect:** at C75.1, both groups are on the site's list, so "Oxyphilic adenocarcinoma" and "Oncocytic carcinoma"
stop for referral there. This is recorded in `docs/TODO.md` §35.5. A Group X ovarian oncocytic adenocarcinoma is still
found by the ovary picker's own filter box.

**Proof:**
- `build_database.py`: 0 FAIL, BUILD PASSED.
- Negative controls: Group 11 20 of 20; Group 10 41 of 41, 8 of 8 probes.
- `alias_index.json`: *Oxyphilic adenocarcinoma* and *Oncocytic carcinoma* → [3, 11]; the other four → [11].
- Browser: "Hurthle cell carcinoma" → site Thyroid gland → Group XI, tree Thyroid carcinomas.

### E5. A2: stain, score and gene results (8 October 2026)

- ✅ **NUT carcinoma (Q73).** Jay: "I agree with NUT carcinoma (Q73)." Built as listed; no change.
- ✅ **Female genital tract and oropharynx (Q89).** Jay: "I agree with Female genital tract (Q89), and the same screen at
  the oropharynx." Built as listed; no change.
- **Adrenal cortex (Q3).** Jay asked what a Wieneke score is. It is the paediatric scoring system of Wieneke, Thompson and
  Heffess (2003), which Mete 2022 calls the currently preferred criteria (PDF p. 21, Table 6). Nine findings score one point
  each: tumour weight over 400 g; size over 10.5 cm; extension into periadrenal soft tissue or adjacent organs; invasion
  into the vena cava; vascular invasion; capsular invasion; tumour necrosis; more than 15 mitoses per 20 high-power fields;
  atypical mitoses. A score of 2 or less means benign behaviour, 3 means uncertain malignant potential, and 4 or more
  means malignant behaviour with a poor outcome. The adult Weiss criteria over-diagnose carcinoma in children (Mete 2022,
  PDF p. 21). **Ruling open.**
- **Lung (Q58).** Jay: "That should be left to the pathologist reporting, and registry rules, A-H, whatever applies, and
  the wording that is superior." The rules, applied:
  - WHO ICD-O-3 Rules A to K say nothing about an uncertain word such as "favour". Rule K covers two definite terms, not a
    favoured one.
  - Visser 2023 rule 4 sets a registry threshold: "possible" does not register a case. Here the carcinoma is certain, and
    only the type is uncertain.
  - The SEER Solid Tumor Rules (lung, rule H3, added 12 October 2018) list "favor" and "favors" as ambiguous terms. They
    code the favoured type only when one of three conditions holds:
    1. a physician confirms that type;
    2. the patient is treated for it;
    3. the case is registered on the ambiguous wording alone, with no other histology in the file.

    Otherwise the code is 8046/3. These are United States rules, read from SEER's inquiry pages, and are not in the Group 11
    sources.
  - Nicholson 2022 (PDF pp. 5–6) makes "non-small cell carcinoma, favour adenocarcinoma" and "favour squamous cell
    carcinoma" the WHO's own small-biopsy terms for a TTF-1 or p40 result. The pathologist's committed diagnosis is
    non-small cell carcinoma, and the favoured type is the stain's suggestion.

  The open choice is between two options:
  - **8046/3 as built.** The definite wording decides.
  - **SEER rule H3.** A new question asks whether a doctor elsewhere in the file states the type, or the patient is treated
    for it. A yes records 8140/3 or 8070/3, and a no records 8046/3.

  **Ruling open.**

### E6. A2: the Wieneke score, the lung stains and the lung confirmation (8 October 2026) ✅

Jay:
- Adrenal: "In the tree, lets ask if Weineke score is mentioned in the file? If it is, then list the score."
- Lung stains: "The TTF-1 and p40 rules are written down and not built" — "Add it".
- Lung confirmation: "'Does a doctor elsewhere in the file state the type, or is the patient treated for it?' A yes records
  8140/3 Adenocarcinoma, NOS or 8070/3 Squamous cell carcinoma, NOS; a no records 8046/3." — "Add this. This is actually
  standard."

✅ **Built.**

**Adrenal (`build/group11_organs/adrenal.py`).**
- "Adrenocortical tumour or adrenal cortical neoplasm" now asks `ad_wieneke`: "Does the file give a Wieneke score?"
- **Yes** leads to `ad_wieneke_score`, which lists every score from 0 to 9:
  - 0 to 2 record the exclusion 8370/0;
  - 3 is not registrable (A7);
  - 4 to 9 record 8370/3 at C74.0.
- **No** leads to the behaviour screen, which no longer mentions the score.
- The hint names the Wieneke score and tells the clerk to answer No for a Weiss score. When a stated behaviour differs from the
  score, the stated behaviour decides (Rule F). Source: Mete 2022, PDF p. 21, Table 6.

**Lung (`build/group11_organs/lung.py`, `nscc_nodes`).**
- "Non-small cell carcinoma, with no type named, including one the report says favours a type" now asks `lu_nscc_confirm`:
  does a doctor elsewhere in the file state the type, or is the patient treated for one?
- **No** records 8046/3.
- **Yes** leads to `lu_nscc_favour`, which asks which type the report favours:
  - adenocarcinoma records 8140/3;
  - squamous cell carcinoma records 8070/3;
  - no type in words, with stains, leads to the `lu_nscc_ihc` stain panel;
  - no favoured type, or a different type from the one stated elsewhere, records 8046/3.
- The stain panel follows Nicholson 2022, PDF p. 5 and PDF p. 6, Table 3:
  - TTF-1 positive and p40 negative records 8140/3;
  - a mucin stain positive and p40 negative records 8140/3;
  - p40 positive with TTF-1 and mucin negative records 8070/3;
  - anything else records 8046/3.
- The cytology route has the same screens at basis 5. Its two stain patterns are options, not a panel: the engine records a
  panel's fallback at the tree's immunohistochemistry basis, 7, and the walk caught that.
- The lung picker leaves 8046 out, because the screens offer it. The 8140/3 and 8070/3 entries now require histology and
  immunohistochemistry, with their markers.

**Proof:**
- `build_database.py`: 1,321 checks, 0 FAIL.
- Negative controls: Group 11 20 of 20.
- Walks of `g11_lung` and `g11_adrenal`: 0 failures. The first lung walk failed the cytology stain panel at basis 7; the
  rebuild fixed it.
- Browser: "Non-small cell carcinoma" → Lung, NOS → histology and immunohistochemistry → the non-small cell carcinoma option →
  Yes → stains → p40 negative, TTF-1 positive. The result is 8140/3 *Adenocarcinoma, NOS*, basis 7, XIf4.

### E7. A3, A4, A5 and A6 (8 October 2026) ✅

**A3 ✅** Jay: "Nasopharynx (Q18). -> I agree, dont use squamous cell unless a histology report mentions it. Penis (Q97). -> I
agree here. Urinary tract (Q98 -> I agree." Built as listed; no change. The nasopharynx records 8010/3 unless the histology
report names squamous cell carcinoma.

**A4 ✅** Jay: "I approve all." D5 stands: where the WHO gives the entity one code, that code is recorded, and Rule K applies
where no single code covers. No change. **Still held:** Q19, oropharynx adenosquamous carcinoma, HPV-associated; Q109, nasal
cavity squamous subtype with HPV status; Q102, conjunctival squamous cell carcinoma with mucinous differentiation. The table
gives these three no built default to approve.

**A5 ✅** Jay: "Use rule K. But Stomach (Q50), keep it out. It needs research."
- **Thyroid, diffuse sclerosing (Q9):** 8260/3, unchanged. The one code that names both terms, 8350/3 *Papillary carcinoma,
  diffuse sclerosing*, is obsolete, so Rule K takes the higher of the usable codes.
- **Appendix, adenocarcinoid (Q51):** ✅ built.
  - 8245/3 *Adenocarcinoid tumor* is obsolete.
  - The term names an adenocarcinoma (8140) and a carcinoid (8240). Rule K (ICD-O-3.1 printed p. 24) takes the single code that
    includes both: 8244/3 *Mixed adenoneuroendocrine carcinoma*, whose ICD-O-3.2 synonyms include *Mixed carcinoid and
    adenocarcinoma* and *Combined carcinoid and adenocarcinoma*.
  - The appendix histology screen offers "Adenocarcinoid tumour", which records 8244/3. Its reason sends a report that names
    goblet cell adenocarcinoma to that option.
- **Stomach (Q50):** kept out, `docs/TODO.md` §35.10.

**A6 ✅** Jay: "I stand with rule F. But the behaviour doesn't need to be hard coded to the morphology code. This needs to be
piloted live. Add this piloting task in todo list, but build it. Only in cases where the behaviour code changes the name of the
cancer, is where its okay to be hard coded."

Built: where the stated behaviour differs from the printed one and the name stays the same, the tree records the stated
behaviour.
- **Thyroid:** "Hyalinizing trabecular tumour that the report calls malignant" records 8336/3 *Hyalinizing trabecular tumor*,
  in XIb (ICCC-2017 range 121). It is a new entry, the 231st.
- **Salivary gland:** "Carcinoma ex pleomorphic adenoma that the report calls in situ, intracapsular and non-invasive, or
  intraductal" is the exclusion 8941/2. A report that does not state in situ keeps 8941/3.
- **Vulva:** "Extramammary Paget disease that the report calls in situ, intraepithelial or confined to the epithelium" is the
  exclusion 8542/2. Invasive disease keeps 8542/3.
- **Kept tied to the code, because the name changes:** 8370/0 against 8370/3, 8825/1 against 8825/3, and 8580/0 *Microscopic
  thymoma* for a thymoma called benign. The (b) items, ICD-O-3.2 as printed, are unchanged.
- **Mechanism:** each pair ICD-O-3.2 does not print is in `build_database.ICDO32_MATRIX_RULE`, anchored on the code's term at
  its printed behaviour. `check_behaviour_exclusion` now reads the same table. `group11_common.term()` and
  `generate_group11_entries.RULE_F_ADDITIONS` use it.
- **Pilot:** `docs/TODO.md` §35.11, which also hands the ruling to the Group X and Group VIII sessions.

**Proof:**
- `build_database.py`: 1,321 checks, 0 FAIL, BUILD PASSED.
- Negative controls: Group 11 20 of 20.
- Walks of `g11_thyroid`, `g11_salivary`, `g11_female_genital`, `g11_appendix`, `g11_lung` and `g11_adrenal`: 0 failures.
- New negative control on the exclusion check:
  - with the 8941/2 anchor misspelt, the check fails: "matrix-rule exclusion anchored on … which icdo32.sqlite no longer
    carries";
  - with the rule removed, it fails: "ICD-O-3.2 carries no term at all for 8941/2";
  - restored, it passes.

### E8. A7: answered by the Wieneke score ruling (8 October 2026) ✅

Jay: "This is answered now, based on my previous score ruling."
- A tumour the report calls of uncertain malignant potential, or with a Wieneke score of 3, is not registered, and no code is
  named.
- The Rule F ruling (E7) leads to the same answer. On 8370 the behaviour changes the name: *Adrenal cortical adenoma, NOS* at
  /0, *Adrenal cortical carcinoma* at /3. So the behaviour stays tied to the code, and ICD-O-3.2 prints no /1 term to name.
- As built, `ad_wieneke_score` score 3 and the behaviour screen's "Uncertain malignant potential" both lead to that line. No
  change.
- The review's note that this answer also decides Spitz melanocytoma (A16) and the squamoproliferative tumour (A6 (b)) is not
  applied. Those items keep their own rulings.

### E9. A8: a child's skin melanoma needs tissue (8 October 2026) ✅

Jay asked: "Is visser table built only for adults?" Visser 2023 Table 3 (printed p. 04) puts an age limit on one block only, "Solid
childhood cancers (age <15 years)". The melanoma rows sit in their own block with no age limit, so they apply to all ages. Ferrari
2021, the paediatric source, says otherwise for children:
- benign pigmented lesions can look like melanoma, and the adult ABCDE rule can mislead (PDF p. 2);
- "When melanoma is suspected, initial excisional biopsy is required" (PDF p. 3).

Jay: "We go with pediatric source."

✅ **Built.**
- `g11_skin` passes `skin_melanoma=False`. The clinical-note screens no longer record 8720/3 at basis 1.
- A note that states a malignant tumour, as the diagnosis or as probable, refers to Group XII with 8000/3 at basis 1, as at every
  other site. "Possible or suspected" is not registrable.
- A melanoma is coded once cytology (basis 5) or histology (the melanoma tree) is in the file.
- The melanoma tree's clinical-note hint no longer sends the clerk to the skin site to register from a note.
- Contract D7 records the withdrawal. Validator rule 2 (`GROUP11_CLINICAL_PAIRS`) now admits no pair at basis 1. Control R2-C puts
  an 8720/3 basis-1 option back on `sk_clinical` and checks that the build fails.

**Proof:**
- `build_database.py`: 1,321 checks, 0 FAIL.
- Negative controls: Group 11 20 of 20. R2-C is caught: "emits 8720/3 at basis 1 … a child's melanoma needs tissue".
- Walks of `g11_skin` and `g11_melanoma`: 0 failures.

### E10. A9 to A12 (8 October 2026)

**A9 ✅ Keratoacanthoma.** Jay: "I agree. excluded unless the pathologist calls it malignant. Only if the pathologist calls it
squamous cell carcinoma."
- The skin histology screen's option reads "Keratoacanthoma, which the report does not call squamous cell carcinoma". It is
  not registered, and its reason sends a report that calls the lesion squamous cell carcinoma to that option.
- No picker searches 8071/3 by "Keratoacanthoma" (`group11_common.SEARCH_TERMS_WITHHELD`).
- "Keratoacanthoma" is a code-less alias into the skin tree. Group 10 gave up its copy (its rule 8), so a search for it no
  longer stops at the skin and does not print under "Also called" on 8071/3.

**A10, solid pseudopapillary neoplasm: Stanley 2015 read in full; ruling open.**

Jay: "Its not benign unless a pathologist says it. Dive deeper into stanley paper and report to me."

What the paper is: Stanley C, et al. J Diagn Med Sonogr 2015;31(5):308–312. It is a case report in a sonography journal, not a
pathology or classification source. One 14-year-old girl had a 14 mm mass in the pancreatic head, found on a routine
sonogram, characterised on magnetic resonance imaging and resected. The pathology showed nuclear beta-catenin positive,
chromogranin and trypsin negative, and no nodal metastasis (PDF p. 2). The paper's own pathologist reports the tumour as "a
solid pseudopapillary tumor", with no behaviour.

What it says about behaviour, all from earlier literature it cites:
- "generally low malignant potential, and an excellent long-term prognosis, despite its aggressive appearance at
  presentation" (PDF p. 1);
- "Most SPNs are benign in nature with malignancy occurring rarely" (PDF p. 3);
- one review found 66 of 452 cases (15%) "demonstrated malignancy with regional metastasis" (PDF pp. 3–4);
- 95% survival after total resection, and 6.2% local recurrence after radical resection (PDF p. 4).

What it does not give: an ICD-O code, a WHO volume, criteria for calling one tumour benign and another malignant, or any
coding guidance.

Against it:
- ICD-O-3.2 prints the pancreatic tumour at /3 only (8452/3 *Solid pseudopapillary neoplasm of pancreas*), from the WHO
  digestive system classification, 5th edition.
- Ebrahim 2025, a pathology series with children, calls these tumours "rare, low-grade malignancies" (PMC section 1).

So Stanley is the weakest source on this question, and it describes the tumour family's behaviour, not a report's wording.

**Proposal, matching your Rule F ruling (E7):**
- Every report of a pancreatic solid pseudopapillary neoplasm records 8452/3, as now.
- Only a report in which the pathologist calls the tumour benign is excluded, as 8452/0 with the same name. That is a
  matrix-rule pair, exactly like 8941/2.
- "Low malignant potential" is not "benign", so it stays 8452/3.

Not built until you confirm.

**A11 ✅ Sialoblastoma.** Jay: "I would go with what papers tell here."
- Pfister 2022, the WHO classification of paediatric tumours, lists sialoblastoma under *Malignant* head and neck tumours (PDF
  p. 13, Table 3). Perez-de-Oliveira 2025 calls it "a rare malignant neoplasm" of the neonatal period and early childhood
  (PMC section 5).
- ICD-O-3.2 and ICCR print 8974/1 only. ICCC-2017 holds 8974 only at /3, in XIIa4.
- Built: on the histology screen and the benign screen, every sialoblastoma now refers to Group XII with `refer_code` 8974,
  as malignant. Group XII owes the 8974/3 pair (`docs/TODO.md` §35.12).

**A12, gastroblastoma: rechecked; ruling open.**
- ICCR Stomach, 3rd edition (December 2025), Table 3, PDF p. 15, read from the page image, prints "Gastroblastoma 8976/3*".
  The asterisk marks a code "approved by the International Agency for Research on Cancer / World Health Organization
  Committee for ICD-O at its meeting in April 2019".
- ICD-O-3.2 (`icdo32.sqlite`, the final workbook of 9 October 2020) has no 8976 and no term "gastroblastoma". ICCC-2017 has no
  8976 either.
- Pfister 2022 lists gastroblastoma among the paediatric digestive epithelial tumours, with the MALAT1::GLI1 fusion (PDF pp.
  11, 13). That list has no benign or malignant heading.
- So the only code is IARC-approved and printed by the newest source, but it is outside ICD-O-3.2 and every ICCC range.

Options:
1. Record 8976/3 *Gastroblastoma* in Group XI on the stomach screen. This needs your ruling to admit a code ICD-O-3.2 lacks,
   since standing rule 1 forbids it, and it goes on the REDCap-side list.
2. Refer it to Group XII.
3. Keep it not built (D4). The clerk then meets only the stomach screen's generic options.

**Online check, 9 October 2026.** Jay asked whether a later update to ICD-O-3.2 added 8976.
- IARC has published no ICD-O-3.2 release that adds it. NAACCR's *Guidelines for 2022 ICD-O-3.2 Histology Code and Behavior
  Update* (1 December 2021) say: "ICD-O-3.2 included changes from all 4th Ed WHO Classification of Tumors books. New editions
  released following the publication of 4th editions are not included in 3.2. A new ICD-O version will be released once all
  5th Ed Blue Books have been published."
- That new version is ICD-O-4, which is out of scope (ruling, 15 September 2026).
- North American registries add 5th-edition codes through yearly NAACCR updates (2021 to 2027). Those are a registry's
  implementation, not IARC's table (ruling, 15 September 2026). Their code tables are separate files, and this check did not
  open them.
- The behaviour digit conflicts. PathologyOutlines (from the WHO digestive system classification, 5th edition) and a 2024
  case review give 8976/1, a tumour of low malignant potential. ICCR prints 8976/3.

**Were these codes in ICD-O-3.0? No (9 October 2026).** Jay suspected that 8976 and the A13 codes were old ICD-O-3.0 codes.
- `icdo32.sqlite` keeps every retired term and marks it `[obs]` (285 rows), so a code from ICD-O-3.0 would still be listed.
  It has no row at all for 8976, 8483, 8484 or 9113.
- ICCC-2017 lists 8483 and 8484 only because its range 8480–8490 spans them, not because the codes existed.
- All four are new codes from 5th-edition WHO volumes published after ICD-O-3.2: 8976 from the digestive system volume (2019),
  and 8483, 8484 and 9113 from the female genital volume (2020).
- The WHO/IARC Committee on ICD-O reviews each new code before the volume is published, which is ICCR's asterisk. IARC has not
  issued a new ICD-O version since ICD-O-3.2.
- NAACCR's yearly updates adopt these WHO codes for North American registries. NAACCR does not create codes.

**Proof (A9, A11):**
- `build_database.py`: 1,321 checks, 0 FAIL.
- Negative controls: Group 11 20 of 20; Group 10 41 of 41.
- Walks of `g11_skin` and `g11_salivary`: 0 failures.
- `alias_index.json`: "Keratoacanthoma" → [11]; no picker carries it on 8071/3.

### E11. A code ICD-O-3.2 does not have is not built (9 October 2026) ✅

Jay: "I see, lets remove such cases where ICD -O- 3.2 does not have the code."

Every code the WHO's 5th-edition volumes added after ICD-O-3.2 stays off every screen, and no option names its entity:
- A12 gastroblastoma (8976);
- A13 adenocarcinoma, HPV-associated and HPV-independent (8483, 8484);
- A15 mesonephric-like adenocarcinoma (9113);
- A16 dermal melanoma (8750/3), Spitz melanocytoma (8770/1) and low cumulative sun damage melanoma in situ (8743/2).

A report naming one reaches the screen's generic option, or the exclusion it already reaches.

✅ **Built:** the cervix and vagina adenocarcinoma option is now "Adenocarcinoma with no type named". Its label, reason and
recognition aid no longer name the HPV-associated and HPV-independent types. The other three items were already unbuilt (D4).

**Not covered, still open: A18 (a).** Carcinoma cuniculatum (8051/3) and tall cell carcinoma with reversed polarity (8509/3)
sit on codes ICD-O-3.2 does have; only the WHO's term is missing. Their options stay as built until you rule on A18.

**Proof:** `build_database.py` 0 FAIL; Group 11 negative controls 20 of 20; walks of `g11_head_neck`, `g11_breast` and
`g11_female_genital` 0 failures (rerun after the revert below).

