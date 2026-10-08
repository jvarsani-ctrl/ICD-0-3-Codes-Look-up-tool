# Group 11, registrar review A1 (a) and (b): the WHO ICD-O-3 coding Rules A to K applied

Written 8 October 2026. The registrar ruled that A1 (a) and (b) are decided by the WHO ICD-O-3 coding Rules A to K (there is no Rule I). This file applies the rules to the twelve instances in `docs/group_11_registrar_review.md` (A1, lines 67 to 114), one wording at a time, and states the code the rules give, what the build holds now, and the change the build must make. Instance (c) is not covered here.

Sources used. The coding manual extract `Group 11 Papers/text/RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt` (ICD-O-3.1, section 4, printed pp. 14 to 28), read through the snippet tool, with Tables 21 and 23 read from PDF pages 9 and 10 of `WHO ICD Manual_Extracted.pdf`. The term list `ICD coding/ICD-O-3.2/icdo32.sqlite` (IARC final workbook of 9 October 2020). `ICCC-2017.sqlite`, through the build's own `iccc_status` and `iccc_subgroups` functions in `build/group11_common.py`. The evidence rows in `docs/group_11_evidence/*.json` and the built file `data/database/group_11_dt.json` and the tree modules, as data on what is built. No other paper was opened and nothing was fetched.

Quotation. The task asked for a verbatim quotation per rule. Only one quotation is given in this file, because the response rules for this session limit quoted source text to one short passage. Every other rule is paraphrased and located by printed page and section number, so each can be checked against the manual in a few seconds.

---

## The coding principle the manual sets

The manual says that coding is based on what the pathologist states ("Coding is based on what the pathologist states", printed p. 21, section 4.3.3). ICD-O is a coded nomenclature of topography and morphology terms, not a classification of tumours by entity (p. 21). The coder therefore takes the term the report uses, looks it up in the numeric list or alphabetic index, and records the code printed for that term. A term printed in ICD-O-3.2 as Preferred, Synonym or Related carries the code of the line it sits under; the level does not change the code.

When the exact term is not printed, the manual gives three moves and no others. Rule J (pp. 16 and 24, section 4.3.7): reorder the word roots of a compound term and look again. Rule K (pp. 16 and 24, section 4.3.8): when no single code names every diagnostic term, and one tumour carries two modifying terms with different codes, take the numerically higher code, because the higher is usually the more specific. Rule F (pp. 15 and 20, section 4.3.3): give the term the behaviour digit the pathologist states, even when the term is not printed with it. Rule G (pp. 15 and 21 to 22, section 4.3.4, Table 21 on p. 22) puts a grade or differentiation word in the sixth digit and leaves the four-digit code alone, except where the word is an integral part of a printed term. Rule H (pp. 15 and 23, section 4.3.5, Table 23) uses the topography printed beside a term only when the report states no site, and disregards it when the tumour is known to arise elsewhere; the manual's own example is infiltrating duct carcinoma, which prints the breast and is recorded at the pancreas when the report says pancreas. Section 4.2.2 (p. 16) treats a site noun and its adjective as the same site ("glioma of pons" and "pontine glioma").

The manual names no tumour-classification table as the authority for a carcinoma code. In printed pp. 14 to 28 the WHO classification is mentioned as the source of preferred terms for haematological malignancies only (section 3.13.1, p. 14) and as a grading scale for central nervous system tumours (section 4.6, p. 27). Neither concerns these instances. A WHO tumour volume or an ICCR table that prints a different code for a tumour therefore does not override a term that ICD-O-3.2 prints and the report uses. The WHO table decides only where it supplies the term the report uses and ICD-O-3.2 has no line for it.

Limits of the rules. The manual gives no instruction for a term that no permutation reaches. In that case the build's NOS fallback applies (Decision Tree master section 3D, a node-type rule of the tool, not a manual rule), and the table says so each time. The manual is the ICD-O-3.1 edition; the term list is the ICD-O-3.2 workbook. The tool emits a four-digit code and a behaviour digit and no sixth digit (`docs/TODO.md` section 32, open for the registrar), so Rule G changes no code the tool records.

### Which rules apply

| Rule | Printed pages | Applies to these instances? |
|---|---|---|
| A (ill-defined sites), B (prefixes), C (overlapping sites) | 14, 17 | No. Every report names a precise organ. |
| D (lymphoma topography), E (leukaemia topography) | 15, 19 | No. Every instance is a carcinoma or melanoma. One lookalike term, 9702/3 Lymphoepithelioid lymphoma, is not the report's term for a lymphoepithelioma. |
| F (behaviour digit) | 15, 20 | Only (a6): a report that calls an adenomyoepithelioma malignant. |
| G (grade, differentiation) | 15, 21 to 22 | (a1), (a2), (a4), (a5): grade words in the wording. |
| H (site-associated terms) | 15, 23 | Wherever ICD-O-3.2 prints a topography beside the term. |
| J (word order) | 16, 24 | Wherever the exact term is not printed. |
| K (two modifying terms) | 16, 24 | Only where no single printed code names every term. |

How to read the tables. The lookup column gives ICD-O-3.2 level, code with behaviour, term, and any topography printed beside it. "ICCC-2017" states the subgroup at the site; every code below stays in Group XI at the sites named, so none refers to another group. "Built now" is read from `group_11_dt.json` and the tree module, not from the review's table.

---

## (a1) Nasopharynx (Q17), sites C11.0 to C11.9

ICD-O-3.2 rows for the family: 8082/3 Preferred "Lymphoepithelial carcinoma"; 8082/3 Synonym "Lymphoepithelioma"; 8082/3 Synonym "Lymphoepithelioma-like carcinoma"; 8082/3 Related "Schmincke tumor" with (C11._); 8072/3 Preferred "Squamous cell carcinoma, large cell, nonkeratinizing, NOS" with Synonym "Squamous cell carcinoma, nonkeratinizing, NOS"; 8020/3 Preferred "Carcinoma, undifferentiated, NOS" with Related "Anaplastic undifferentiated carcinoma". No ICD-O-3.2 term contains the word nasopharyngeal (count 0). ICCC-2017 holds 8082/3, 8072/3, 8020/3 and 8070/3 in XIc at C11.0 to C11.9.

| Wording | ICD-O-3.2 lookup | Rules applied | Code the rules give | Built now | Change needed |
|---|---|---|---|---|---|
| Lymphoepithelial carcinoma | Printed: 8082/3 Preferred, Lymphoepithelial carcinoma | Lookup principle (p. 21): the term is printed. Rule H (p. 23): no topography printed; site stated. | 8082/3 Lymphoepithelial carcinoma. ICCC-2017: XIc. | The type screen's older-name option records 8072/3; 8082/3 is reachable only in the picker. | Yes. 8072/3 to 8082/3 (C1). |
| Lymphoepithelioma | Printed: 8082/3 Synonym | Lookup principle (p. 21). | 8082/3 Lymphoepithelial carcinoma. XIc. | Older-name option, 8072/3. | Yes (C1). |
| Lymphoepithelioma-like carcinoma | Printed: 8082/3 Synonym | Lookup principle (p. 21). | 8082/3 Lymphoepithelial carcinoma. XIc. | Picker search term, 8082/3. The older-name option does not name it. | Name it in the C1 option. |
| Schmincke tumour | Printed: 8082/3 Related, "Schmincke tumor", (C11._) | Lookup principle (p. 21). Rule H (p. 23): the printed C11 is the nasopharynx and agrees with the stated site. | 8082/3 Lymphoepithelial carcinoma. XIc. | Older-name option, 8072/3. | Yes (C1). |
| Undifferentiated carcinoma of nasopharyngeal type | Not printed. Nearest printed term: 8020/3 Preferred "Carcinoma, undifferentiated, NOS". No reordering of undifferentiated, carcinoma, nasopharyngeal and type gives a printed term. | Rule J (p. 24): no permutation. Section 4.2.2 (p. 16): "nasopharyngeal" names the site, which the record carries as C11. Rule G (p. 22): undifferentiated is a grade word and is integral to the printed term 8020/3. | 8020/3 Carcinoma, undifferentiated, NOS. XIc. | Older-name option, 8072/3. | Yes. 8072/3 to 8020/3 (C2). See open point 4. |
| Non-keratinizing carcinoma, undifferentiated subtype (also written non-keratinising squamous cell carcinoma, undifferentiated subtype) | With "squamous cell": printed, 8072/3 Synonym "Squamous cell carcinoma, nonkeratinizing, NOS". Without it: not printed; only 8072/3 and 8073/3 (small cell) carry "nonkeratinizing". The word "undifferentiated" belongs to 8020/3. | Rule K (p. 24): no single printed code names both terms, so the higher code is taken: 8072 is higher than 8020. Rule G (p. 22): "undifferentiated" is also a grade (4) and adds nothing to the four-digit code. | 8072/3 Squamous cell carcinoma, large cell, nonkeratinizing, NOS. XIc. | 8072/3 on the first np_npc_type option, whose label names the differentiated or undifferentiated subtype. | None. |
| Non-keratinising carcinoma with lymphoepithelial features, where the diagnosis line says the tumour is lymphoepithelial | Two printed terms: 8072/3 (nonkeratinizing) and 8082/3 (lymphoepithelial). | Rule K (p. 24): no single code names both, so the higher, 8082. The manual's example is one neoplasm with elements of both cell types. | 8082/3 Lymphoepithelial carcinoma. XIc. Depends on reading "features" as a modifier; see open point 6. | Older-name option, 8072/3. | Hint sentence only (C3). |

---

## (a2) Salivary gland (Q45), sites C07.9 and C08.0 to C08.9

ICCC-2017: 8290/3, 8020/3 and 8140/3 are all XIf1 at these sites.

| Wording | ICD-O-3.2 lookup | Rules applied | Code the rules give | Built now | Change needed |
|---|---|---|---|---|---|
| Oncocytic carcinoma | Printed: 8290/3 Synonym "Oncocytic carcinoma" under Preferred "Oxyphilic adenocarcinoma"; also Synonym "Oncocytic adenocarcinoma". | Lookup principle (p. 21). Rule H (p. 23): no topography is printed on these terms (the Hurthle terms of 8290/3 print C73.9 but are not the report's term). | 8290/3 Oxyphilic adenocarcinoma. XIf1. The WHO salivary volume's place for the entity (salivary carcinoma NOS and emerging entities, 8140/3 Adenocarcinoma, NOS) is not a rule of the manual. | sg_picker holds 8290/3 Oxyphilic adenocarcinoma with the search term "Oncocytic carcinoma". | None. |
| Poorly differentiated carcinoma | Printed: 8020/3 Related "Carcinoma, poorly differentiated, NOS" under Preferred "Carcinoma, undifferentiated, NOS". | Lookup principle (p. 21). Rule G (p. 22, Table 21): poorly differentiated is grade 3 and, with the term printed, is part of the listed name; a sixth digit of 3 would be added where the tool recorded one, and the four-digit code is the printed one. | 8020/3 Carcinoma, undifferentiated, NOS. XIf1. | sg_picker holds 8020/3 with the search term "Carcinoma, poorly differentiated, NOS". | None. |

---

## (a3) Salivary gland (Q44), mucinous adenocarcinoma with a signet ring subtype

ICD-O-3.2 rows: 8480/3 Preferred "Mucinous adenocarcinoma" with Synonym "Mucinous carcinoma"; 8490/3 Preferred "Signet ring cell carcinoma" with Synonyms "Signet ring cell adenocarcinoma" and "Mucinous carcinoma, signet ring cell type". ICCC-2017: 8480/3 and 8490/3 are XIf1 at C07.9 and C08.0 to C08.9.

| Wording | ICD-O-3.2 lookup | Rules applied | Code the rules give | Built now | Change needed |
|---|---|---|---|---|---|
| Mucinous carcinoma, signet ring cell type | Printed: 8490/3 Synonym. | Lookup principle (p. 21). | 8490/3 Signet ring cell carcinoma. XIf1. | sg_picker holds 8490/3 with this term as a search term. | None. |
| Mucinous adenocarcinoma, signet ring subtype | Not letter for letter. It differs from the printed synonym by "adenocarcinoma" for "carcinoma" and "subtype" for "type"; ICD-O-3.2 prints carcinoma and adenocarcinoma as the same line at both 8480/3 and 8490/3, so the printed synonym is the report's term. | Lookup principle (p. 21). If a coder declines that match, Rule K (p. 24): mucinous and signet ring are two modifying terms; the one printed code 8490/3 names both, and in any case the higher of 8480 and 8490 is 8490. Both routes agree. | 8490/3 Signet ring cell carcinoma. XIf1. | sg_picker offers both 8480/3 Mucinous adenocarcinoma and 8490/3 Signet ring cell carcinoma; no node states which a combined wording takes. The review's "built 8480/3" describes the WHO-table draft, not the picker. | Hint sentence (C6). |
| Signet ring cell adenocarcinoma | Printed: 8490/3 Synonym. | Lookup principle (p. 21). | 8490/3. XIf1. | Picker search term. | None. |
| Mucinous adenocarcinoma, no subtype named | Printed: 8480/3 Preferred. | Lookup principle (p. 21). | 8480/3 Mucinous adenocarcinoma. XIf1. | Picker. | None. |

---

## (a4) Thymus (Q68), sites C37.9 (ICCC XIf5) and mediastinum C38.x (XIf10)

ICD-O-3.2 rows: 8576/3 Preferred "Hepatoid adenocarcinoma" with Synonym "Hepatoid carcinoma"; 8410/3 Preferred "Sebaceous carcinoma" and Synonym "Sebaceous adenocarcinoma", each with (C44._); 8586/3 Preferred "Thymic carcinoma, NOS" with (C37.9); 8012/3 Preferred "Large cell carcinoma, NOS"; 8014/3 Preferred "Large cell carcinoma with rhabdoid phenotype"; 8963/3 Preferred "Rhabdoid tumor, NOS" (a rhabdoid tumour, which ICCC-2017 places in Group IX at C37.9, so it is not a carcinoma code); no printed term "rhabdoid carcinoma"; no morphology term for a Castleman disease-like reaction. ICCC-2017: 8576/3, 8410/3, 8586/3, 8012/3 and 8014/3 are XIf5 at C37.9 and XIf10 at C38.x.

| Wording | ICD-O-3.2 lookup | Rules applied | Code the rules give | Built now | Change needed |
|---|---|---|---|---|---|
| Hepatoid carcinoma (or hepatoid adenocarcinoma) of the thymus | Printed: 8576/3 Synonym (Preferred for adenocarcinoma). No topography printed. | Lookup principle (p. 21). Rule H (p. 23): site stated as thymus. | 8576/3 Hepatoid adenocarcinoma. XIf5. | ty_thymic records 8586/3 Thymic carcinoma, NOS for all four wordings in one option, marked as awaiting the registrar. | Yes. 8586/3 to 8576/3 (C4a). |
| Sebaceous carcinoma of the thymus | Printed: 8410/3 Preferred, (C44._). | Lookup principle (p. 21). Rule H (pp. 15, 23): the printed skin topography is disregarded because the tumour is known to arise in the thymus; the morphology code is kept, as in the manual's infiltrating duct carcinoma of the pancreas. | 8410/3 Sebaceous carcinoma at C37.9. XIf5. | As above, 8586/3. | Yes. 8586/3 to 8410/3 (C4b). |
| Rhabdoid carcinoma of the thymus | Not printed. Reordering gives "carcinoma, rhabdoid", also not printed. 8014/3 names a large cell carcinoma; 8963/3 names a rhabdoid tumour, not a carcinoma. | Rule J (p. 24): no permutation. Rule K (p. 24): not met, because carcinoma is the head noun and rhabdoid is the only modifier. Section 4.2.2 (p. 16): "of the thymus" names the site. | The rules reach no printed term. The NOS fallback gives 8586/3 Thymic carcinoma, NOS, the printed term for a carcinoma of the thymus (same code as the WHO footnote). XIf5. See open point 3. | 8586/3. | Code unchanged; new reason (C4c). |
| Undifferentiated large cell carcinoma of the thymus, with a Castleman disease-like reaction | Printed: 8012/3 Preferred "Large cell carcinoma, NOS". "Undifferentiated" is printed with a type only as 8020/3 "Carcinoma, undifferentiated, NOS". The Castleman disease-like reaction has no morphology term. | Rule G (pp. 15, 22): undifferentiated is a grade word (grade 4, Table 21); the manual's own example codes "anaplastic squamous cell carcinoma" as 8070/3 with grade 4, so the type keeps its code. Rule K (p. 24) is not used, because a grade word has a sixth-digit code of its own. Rule H: no topography printed. | 8012/3 Large cell carcinoma, NOS, with grade 4 not recorded by the tool. XIf5. See open point 2. | 8586/3. | Yes. 8586/3 to 8012/3 (C4d). |
| Thymic carcinoma, hepatoid type (or hepatoid thymic carcinoma) | Printed: 8586/3 "Thymic carcinoma, NOS" and 8576/3 "Hepatoid carcinoma". | Section 4.2.2 (p. 16): "thymic" names the site, so the wording is the same tumour as hepatoid carcinoma of the thymus. Rule K (p. 24) does not move the code to 8586/3: its stated reason is that the higher code is usually the more specific, and 8586/3 is the NOS term. | 8576/3 Hepatoid adenocarcinoma. XIf5. Literal Rule K reading would give 8586/3; see open point 1. | 8586/3. | Yes (C4a, C5). |
| Thymic carcinoma, sebaceous type | Printed: 8586/3 and 8410/3 (C44._). | As above, plus Rule H (p. 23). | 8410/3 Sebaceous carcinoma. XIf5. | 8586/3. | Yes (C4b, C5). |
| Thymic carcinoma, rhabdoid type | Printed: 8586/3 only. | As for rhabdoid carcinoma above. | 8586/3 Thymic carcinoma, NOS. XIf5. | 8586/3. | New reason only (C4c). |
| Thymic carcinoma, undifferentiated large cell type | Printed: 8586/3 and 8012/3. | Rule G (p. 22) and section 4.2.2 (p. 16), as above. | 8012/3 Large cell carcinoma, NOS. XIf5. | 8586/3. | Yes (C4d, C5). |

The picker already holds 8576/3, 8410/3, 8012/3, 8014/3 and 8586/3 with their ICD-O-3.2 search terms, so a clerk who types the name reaches each today; the fault is the combined screen option, which records 8586/3 for all.

---

## (a5) Thymus (Q70), "neuroendocrine tumour, grade 3", sites C37.9 and C38.x

ICD-O-3.2 rows: 8249/3 Preferred "Neuroendocrine tumor, grade 2" with Related "Neuroendocrine tumor, grade 3", Related "Neuroendocrine carcinoma, moderately differentiated" and Synonym "Atypical carcinoid tumor"; 8013/3 Preferred "Large cell neuroendocrine carcinoma"; 8240/3 Preferred "Neuroendocrine tumor, NOS" with Related "Neuroendocrine tumor, grade 1". ICCC-2017: 8249/3 and 8013/3 are XIf5 at C37.9 and XIf10 at C38.x.

| Wording | ICD-O-3.2 lookup | Rules applied | Code the rules give | Built now | Change needed |
|---|---|---|---|---|---|
| Neuroendocrine tumour, grade 3 | Printed: 8249/3 Related, exact. | Lookup principle (p. 21). Rule G (p. 22): the grade is part of the printed name, so the four-digit code is the printed one. The WHO thoracic criteria that would reclassify a tumour with carcinoid morphology and high proliferation as 8013/3 are the pathologist's diagnosis to make, not the coder's. | 8249/3 Neuroendocrine tumor, grade 2. XIf5. | ty_picker holds 8249/3 with the search term "Neuroendocrine tumor, grade 3". The result prints the Preferred term, "grade 2". | Code none. Reason sentence (C12). |
| Grade 3 neuroendocrine tumour; NET grade 3 | Same words reordered. The abbreviation NET G3 is not a printed term. | Rule J (p. 24) for the reordering; the abbreviation is read as the spelled-out term. | 8249/3. XIf5. | Picker finds the spelled-out form. | None. |
| Neuroendocrine tumour, grade 2 to 3 | Two grades. | Rule G (pp. 15, 21): two grades take the higher, grade 3. | 8249/3. XIf5. | Hint sentence on ty_picker. | None. |
| Atypical carcinoid | Printed: 8249/3 Synonym. | Lookup principle (p. 21). | 8249/3. XIf5. | Picker search term. | None. |
| Large cell neuroendocrine carcinoma (including a report that says a NET G3 is reclassified by the pathologist as this) | Printed: 8013/3 Preferred. | Lookup principle (p. 21): the diagnosis the pathologist states. | 8013/3 Large cell neuroendocrine carcinoma. XIf5. | Picker. | None. |

---

## (a6) Breast (Q81), sites C50.0 to C50.9 (ICCC XIf6)

ICD-O-3.2 rows: 8983/3 Preferred "Adenomyoepithelioma with carcinoma" with Synonym "Malignant adenomyoepithelioma" (C50._); 8983/0 Preferred "Adenomyoepithelioma, NOS" and Related "Adenomyoepithelioma, benign" (C50._); 8562/3 Preferred "Epithelial-myoepithelial carcinoma". ICCC-2017: 8983/3 and 8562/3 are XIf6 at C50.x.

| Wording | ICD-O-3.2 lookup | Rules applied | Code the rules give | Built now | Change needed |
|---|---|---|---|---|---|
| Malignant adenomyoepithelioma | Printed: 8983/3 Synonym, (C50._). | Lookup principle (p. 21). Rule H (p. 23): the printed breast agrees with the stated site. | 8983/3 Adenomyoepithelioma with carcinoma. XIf6. The ICCR table's 8562/3 is not a rule of the manual. | br_picker holds 8983/3 with the search term "Malignant adenomyoepithelioma". | None. |
| Adenomyoepithelioma with carcinoma | Printed: 8983/3 Preferred. | Lookup principle (p. 21). | 8983/3. XIf6. | Picker. | None. |
| Adenomyoepithelioma, which the report calls malignant | The term is printed at /0; the pathologist states a different behaviour. | Rule F (p. 15): code the behaviour the pathologist states. The printed synonym 8983/3 agrees. | 8983/3. XIf6. | Picker. | None. |
| Adenomyoepithelioma with no word of malignancy | Printed: 8983/0. | Rule F (p. 15). | 8983/0 Adenomyoepithelioma, NOS: not registered (Group XI declares /3). | The not-malignant screen's exclusion. | None. |
| Epithelial-myoepithelial carcinoma | Printed: 8562/3 Preferred. | Lookup principle (p. 21). | 8562/3 Epithelial-myoepithelial carcinoma. XIf6. | br_picker. | None. |

---

## (a7) Parathyroid (Q114), site C75.0 (ICCC XIf10)

ICD-O-3.2 rows: 8322/3 Preferred "Water-clear cell adenocarcinoma" and Synonym "Water-clear cell carcinoma", each (C75.0); 8290/3 Synonym "Oncocytic carcinoma"; 8140/3 Related "Parathyroid carcinoma", (C75.0). ICCC-2017: 8322/3, 8290/3 and 8140/3 are XIf10 at C75.0.

| Wording | ICD-O-3.2 lookup | Rules applied | Code the rules give | Built now | Change needed |
|---|---|---|---|---|---|
| Water-clear cell parathyroid carcinoma | Printed: 8322/3, (C75.0). | Lookup principle (p. 21). Rule H (p. 23): the printed C75.0 agrees with the stated site. Rule K (p. 24) gives the same answer if the wording is read as two terms (8322 is higher than 8140). | 8322/3 Water-clear cell adenocarcinoma. XIf10. | en_picker holds 8322/3; the en_histology hint sends this wording to it. | None. |
| Oncocytic parathyroid carcinoma | Printed: 8290/3 Synonym "Oncocytic carcinoma"; "parathyroid carcinoma" is the printed 8140/3. | Lookup principle (p. 21), with "parathyroid" read as the site (p. 16). Rule K (p. 24): 8290 is higher than 8140; same code. | 8290/3 Oxyphilic adenocarcinoma. XIf10. | en_picker holds 8290/3. | None. |
| Parathyroid carcinoma | Printed: 8140/3 Related, (C75.0). | Lookup principle (p. 21). Rule H (p. 23). | 8140/3 Adenocarcinoma, NOS. XIf10. Equal to the ICCR table's code. | en_histology option, 8140/3. | None. |

---

## (a8) Urinary tract (Q95), "mixed adenocarcinoma"

Sites C65.9, C66.9 and C68.x are XIf10; C67.x is XIf8. ICD-O-3.2 rows near the wording: 8323/3 Preferred "Mixed cell adenocarcinoma"; 8255/3 Preferred "Adenocarcinoma with mixed subtypes" with Synonym "Adenocarcinoma combined with other types of carcinoma"; 8560/3 Synonyms "Mixed adenocarcinoma and squamous cell carcinoma" and "Mixed adenocarcinoma and epidermoid carcinoma" (a mixture of two cancers, not this term); 8140/3 Preferred "Adenocarcinoma, NOS". ICCC-2017: 8323/3, 8255/3 and 8140/3 are Group XI at these sites.

| Wording | ICD-O-3.2 lookup | Rules applied | Code the rules give | Built now | Change needed |
|---|---|---|---|---|---|
| Mixed adenocarcinoma | Not printed. The nearest printed terms each add a word: "Mixed cell adenocarcinoma" adds "cell"; "Adenocarcinoma with mixed subtypes" adds "with" and "subtypes". | Rule J (p. 24) reorders word roots only, so "adenocarcinoma, mixed" is the one permutation and it is not printed; neither neighbour is reached. Rule K (p. 24) is not met: "mixed" is a modifier with no code of its own. | The rules reach no printed term. The NOS fallback gives 8140/3 Adenocarcinoma, NOS, the head noun, which is also the ICCR corrigendum's code. The Netto 2022 table's 8323/3 is not a rule of the manual. See open point 5. | gu_histology option "Adenocarcinoma with no type named, mixed adenocarcinoma, ..." records 8140/3. gu_picker holds 8323/3. | Code none. Wording only (C8). |
| Mixed cell adenocarcinoma | Printed: 8323/3 Preferred. | Lookup principle (p. 21). | 8323/3 Mixed cell adenocarcinoma. XIf8 or XIf10 by site. | gu_picker. | None. |
| Adenocarcinoma with mixed subtypes | Printed: 8255/3 Preferred. | Lookup principle (p. 21). | 8255/3 Adenocarcinoma with mixed subtypes. | gu_picker. | None. |

The review's "ICD-O-3.2 wins" branch names 8323/3 for the term "mixed adenocarcinoma". ICD-O-3.2 does not print that term, so that branch cannot apply to this wording.

---

## (a9) Uterine corpus (Q86), gastric-type mucinous carcinoma, sites C54.0 to C54.9 and C55.9 (ICCC XIf10)

ICD-O-3.2 rows: 8482/3 Preferred "Mucinous carcinoma, gastric type", (C53._), with Synonym "Mucinous adenocarcinoma, endocervical type" marked obsolete; 8144/3 Preferred "Adenocarcinoma, intestinal type", (C16._), with Synonyms "Carcinoma, intestinal type", (C16._), "Adenocarcinoma, enteric" and "Mucinous carcinoma, intestinal type" (the last two print no topography). ICCC-2017: 8482/3, 8144/3 and 8140/3 are XIf10 at C54.x and C55.9.

| Wording | ICD-O-3.2 lookup | Rules applied | Code the rules give | Built now | Change needed |
|---|---|---|---|---|---|
| Mucinous carcinoma, gastric type; gastric-type mucinous carcinoma | Printed: 8482/3 Preferred, (C53._). The second form is the same words reordered (Rule J). | Lookup principle (p. 21). Rule H (pp. 15, 23): the printed C53 is the cervix; the report names the corpus, so the cervical code is ignored and the corpus is recorded, with 8482/3 kept. | 8482/3 Mucinous carcinoma, gastric type, at C54.x. XIf10. | fg_picker holds both 8482/3 and 8144/3; no node states which the corpus takes. The review's "built 8144/3" is the ICCR-table draft. | Hint sentence (C7). |
| Mucinous carcinoma, gastric (gastrointestinal)-type (the ICCR endometrial table's wording) | "Gastric type" is printed at 8482/3. "Gastrointestinal" is not printed; "intestinal type" is printed at 8144/3. | The pathologist's own term, "gastric type", is printed (p. 21). If "gastrointestinal" is read as a second modifier, Rule K (p. 24) takes the higher of 8482 and 8144, which is 8482. Both routes agree. | 8482/3. XIf10. | As above. | Hint sentence (C7). |
| Mucinous carcinoma, intestinal type; adenocarcinoma, intestinal type | Printed: 8144/3 Preferred, (C16._); the Synonym "Mucinous carcinoma, intestinal type" prints no topography. | Lookup principle (p. 21). Rule H (p. 23): the printed stomach code is disregarded at the corpus. | 8144/3 Adenocarcinoma, intestinal type. XIf10. | fg_picker. | None. |

---

## (a10) Skin (Q32), pseudovascular squamous cell carcinoma, sites C44.0 to C44.9 (ICCC XIe)

ICD-O-3.2 rows: 8074/3 Preferred "Squamous cell carcinoma, spindle cell" with Related "Pseudovascular squamous cell carcinoma"; 8075/3 Preferred "Squamous cell carcinoma, adenoid" with Synonyms "Squamous cell carcinoma, acantholytic" and "Squamous cell carcinoma, pseudoglandular". ICCC-2017: 8074/3 and 8075/3 are XIe at C44.x.

| Wording | ICD-O-3.2 lookup | Rules applied | Code the rules give | Built now | Change needed |
|---|---|---|---|---|---|
| Pseudovascular squamous cell carcinoma | Printed: 8074/3 Related, exact. No topography printed. | Lookup principle (p. 21). The WHO volume's statement that it is not a subtype, and not a term for acantholytic carcinoma, is not a rule of the manual; 8075/3 is a different printed line that this report does not use. | 8074/3 Squamous cell carcinoma, spindle cell. XIe. | sk_picker holds 8074/3 with "Pseudovascular squamous cell carcinoma" as a search term (skin.py, departure 9: the picker follows ICD-O-3.2). The review's "held; no option or alias names it" is out of date for the picker; no alias holds it. | None to the code. Correct the review's built column. |
| Acantholytic squamous cell carcinoma | Printed: 8075/3 Synonym. | Lookup principle (p. 21). | 8075/3 Squamous cell carcinoma, adenoid. XIe. | sk_picker. | None. |

---

## (b1) Melanoma (Q20), spitzoid melanoma, sites C44.0 to C44.9 (ICCC XId)

ICD-O-3.2 rows: 8770/3 Preferred "Malignant Spitz tumor" with Synonyms "Spitz melanoma" and "Spitzoid melanoma", each (C44._); 8743/3 Preferred "Low cumulative sun damage melanoma" (C44._); 8761/3 Preferred "Malignant melanoma arising in giant congenital nevus" (C44._); 8720/3 Preferred "Malignant melanoma, NOS". ICCC-2017: all four are XId at C44.x and at C69.x.

| Wording | ICD-O-3.2 lookup | Rules applied | Code the rules give | Built now | Change needed |
|---|---|---|---|---|---|
| Spitzoid melanoma (as the diagnosis) | Printed: 8770/3 Synonym, (C44._). | Lookup principle (p. 21). Rule H (p. 23): the printed skin agrees. The view in Sargen 2026 that "spitzoid" is a description is not a rule of the manual and does not remove a printed synonym. | 8770/3 Malignant Spitz tumor. XId. | me_skin_histology option "Spitz melanoma, malignant Spitz tumour or spitzoid melanoma", 8770/3. | None to the code. |
| Spitz melanoma; malignant Spitz tumour | Printed: 8770/3 Synonym; Preferred. | Lookup principle (p. 21). | 8770/3. XId. | Same option. | None. |
| Melanoma, with "spitzoid features" only in the microscopic description and a diagnosis line of malignant melanoma | The diagnosis the pathologist states is "Melanoma, NOS", printed at 8720/3. | Lookup principle (p. 21): the code follows what the pathologist states as the diagnosis. | 8720/3 Malignant melanoma, NOS. XId. | The same Spitz option does not say to read the diagnosis line. | Hint sentence (C11). |
| Spitzoid melanoma that the report also calls low cumulative sun damage melanoma, or arising in a congenital naevus | Two printed types: 8770/3, 8743/3 or 8761/3. | Rule K (p. 24): no single code names both, so the higher code: 8770 is higher than 8761 and 8743. | 8770/3 Malignant Spitz tumor. XId. | me_skin_histology hint already states the Rule K order for two melanoma types. | None. |

---

## (b2) Eye (Q25), uveal melanoma of mixed epithelioid and spindle cell type, sites C69.0 to C69.9 (ICCC XId)

ICD-O-3.2 rows: 8770/3 Related "Mixed epithelioid and spindle cell melanoma" (no topography printed) under Preferred "Malignant Spitz tumor" (C44._); 8771/3 Preferred "Epithelioid cell melanoma"; 8772/3 Preferred "Spindle cell melanoma, NOS"; 8773/3 Preferred "Spindle cell melanoma, type A", (C69._); 8774/3 Preferred "Spindle cell melanoma, type B", (C69._); none is marked obsolete. ICCC-2017: 8770/3, 8771/3, 8772/3, 8773/3 and 8774/3 are XId at C69.0 to C69.9 and at C44.x.

| Wording | ICD-O-3.2 lookup | Rules applied | Code the rules give | Built now | Change needed |
|---|---|---|---|---|---|
| Uveal melanoma, mixed epithelioid and spindle cell type | Printed: 8770/3 Related "Mixed epithelioid and spindle cell melanoma". The report adds "type" and "uveal"; the first is the same term, the second is the site. | Lookup principle (p. 21). Rule H (pp. 15, 23): the code's Preferred term prints skin, the report states the eye, so the skin topography is disregarded and the eye code is used. Rule K (p. 24) is not reached, because one printed code names both cell types; had the term not been printed, Rule K would have taken 8772/3 Spindle cell melanoma, NOS over 8771/3 Epithelioid cell melanoma. | 8770/3 Malignant Spitz tumor, at the eye site. XId. | me_picker 8770/3 with search term "Mixed epithelioid and spindle cell melanoma"; me_eye hint states the code. The result prints only "Malignant Spitz tumor". | None to the code. Reason sentence (C9). |
| Epithelioid cell melanoma; spindle cell melanoma | Printed: 8771/3; 8772/3. | Lookup principle (p. 21). | 8771/3; 8772/3. XId. | me_picker. | None. |
| Spindle cell melanoma, type A (or type B) | Printed: 8773/3, (C69._); 8774/3, (C69._). | Lookup principle (p. 21). Rule H (p. 23): the printed C69 is the usual site and gives way to a site the report states; it does not remove the morphology term from any site. | 8773/3 Spindle cell melanoma, type A. XId. | me_picker holds 8773/3 and 8774/3. | None to the code. |

Does 8773/3 stay in the eye picker? Yes. It is a printed, current term with the eye printed beside it, and ICCC-2017 holds it in XId at every eye site. Nothing in the rules removes it. The shared picker also offers it at skin sites; the hint sentence that spindle cell type A and type B are terms for the eye should say a skin report that literally says type A takes the term too (C10).

---

## Points the rules leave open

1. Thymus, "thymic carcinoma, <type>" (a4). Section 4.2.2 reads "thymic" as the site, and Rule K prefers the more specific of two terms, so the rules give 8576/3 or 8410/3. A literal reading that treats "Thymic carcinoma, NOS" as a coded term and applies Rule K gives 8586/3 for the wordings with a type, because 8586 is higher than 8576 and 8410. The registrar can rule which reading the build follows; this file builds the first.
2. Thymus, "undifferentiated large cell carcinoma" (a4). Rule G treats undifferentiated as a grade and gives 8012/3 Large cell carcinoma, NOS. Treating it as a modifying term and applying Rule K would give 8020/3 Carcinoma, undifferentiated, NOS, the higher code. The manual's own "anaplastic squamous cell carcinoma" example supports Rule G.
3. Thymus, rhabdoid carcinoma (a4). The rules reach no printed term; 8586/3 Thymic carcinoma, NOS is the fallback of the tool, not a manual rule. If a report calls the tumour a large cell carcinoma with a rhabdoid phenotype, the printed term is 8014/3 Large cell carcinoma with rhabdoid phenotype.
4. Nasopharynx, undifferentiated carcinoma of nasopharyngeal type (a1). The rules give 8020/3. Whether the WHO equates the older name with non-keratinising carcinoma (8072/3) rests on the WHO 5th edition chapter text, which the XIc evidence file records as not held (data gap 1 in `XIc_nasopharynx.md`). No rule of the manual makes that equation. This is the one item in this file that needs evidence the files do not contain.
5. Urinary tract, mixed adenocarcinoma (a8). The rules give the NOS fallback, 8140/3. If the registrar holds that "mixed adenocarcinoma" is a short form of "mixed cell adenocarcinoma", the code is 8323/3; if of "adenocarcinoma with mixed subtypes", 8255/3. The rules do not choose between them.
6. Nasopharynx, "with lymphoepithelial features" (a1). Rule K gives 8082/3 only if the diagnosis line states the tumour is lymphoepithelial. A report that says non-keratinising squamous cell carcinoma and mentions lymphoepithelial features only in the description takes 8072/3.
7. Sixth digit (Rule G). The tool emits no sixth digit (`docs/TODO.md` section 32). If the registrar rules that it should, the grade words in (a1), (a2) and (a4) would add a digit; none changes the four-digit code.

---

## Changes the build must make

### Code changes (the code the rules give differs from the code built)

| No. | Tree module | Node | Option label (new) | Old code to new code | Reason sentence the clerk should see | Rule named |
|---|---|---|---|---|---|---|
| C1 | `build/group11_organs/nasopharynx.py` | `np_npc_type` | Replace the option "An older name: lymphoepithelioma, lymphoepithelial carcinoma, Schmincke tumour, or undifferentiated carcinoma of nasopharyngeal type" with "Lymphoepithelioma, lymphoepithelial carcinoma, lymphoepithelioma-like carcinoma or Schmincke tumour" | 8072/3 Squamous cell carcinoma, large cell, nonkeratinizing, NOS to 8082/3 Lymphoepithelial carcinoma | Recorded as Lymphoepithelial carcinoma (8082/3). ICD-O-3.2 lists Lymphoepithelioma, Lymphoepithelioma-like carcinoma and Schmincke tumor as terms of this code, and the code follows the term the report uses. A report that says non-keratinising squamous cell carcinoma is coded 8072/3 on the first option. | Lookup principle (p. 21); Rule H (p. 23) for Schmincke tumor and the nasopharynx |
| C2 | `build/group11_organs/nasopharynx.py` | `np_npc_type` | New option: "Undifferentiated carcinoma of nasopharyngeal type" | 8072/3 to 8020/3 Carcinoma, undifferentiated, NOS | Recorded as Carcinoma, undifferentiated, NOS (8020/3). ICD-O-3.2 has no term for undifferentiated carcinoma of nasopharyngeal type, and no reordering of its words reaches another code. A report that says non-keratinising squamous cell carcinoma, undifferentiated subtype, is coded 8072/3 on the first option. Hold until open point 4 is settled. | Rule J (p. 24); Rule G (p. 22); section 4.2.2 (p. 16) |
| C4a | `build/group11_organs/thymus.py` | `ty_thymic` | Split the option "Hepatoid, rhabdoid or sebaceous carcinoma of the thymus, or undifferentiated large cell carcinoma with a Castleman disease-like reaction"; first new option: "Hepatoid carcinoma or hepatoid adenocarcinoma of the thymus" | 8586/3 Thymic carcinoma, NOS to 8576/3 Hepatoid adenocarcinoma | Recorded as Hepatoid adenocarcinoma (8576/3). ICD-O-3.2 lists Hepatoid carcinoma as a term of this code, and the code follows the term the report uses. | Lookup principle (p. 21) |
| C4b | `build/group11_organs/thymus.py` | `ty_thymic` | "Sebaceous carcinoma of the thymus" | 8586/3 to 8410/3 Sebaceous carcinoma | Recorded as Sebaceous carcinoma (8410/3). ICD-O-3.2 prints the skin beside this term; the report places the tumour in the thymus, so the skin is disregarded. | Rule H (pp. 15, 23) |
| C4c | `build/group11_organs/thymus.py` | `ty_thymic` | "Rhabdoid carcinoma of the thymus" | 8586/3 Thymic carcinoma, NOS, unchanged | Recorded as Thymic carcinoma, NOS (8586/3). ICD-O-3.2 has no term for rhabdoid carcinoma, and reordering its words reaches no listed term. A report that calls the tumour a large cell carcinoma with a rhabdoid phenotype is found in the picker as 8014/3. | Rule J (p. 24) |
| C4d | `build/group11_organs/thymus.py` | `ty_thymic` | "Undifferentiated large cell carcinoma of the thymus, including one with a Castleman disease-like reaction" | 8586/3 to 8012/3 Large cell carcinoma, NOS | Recorded as Large cell carcinoma, NOS (8012/3). Undifferentiated is a grade, and a grade does not change the code. The Castleman disease-like reaction has no ICD-O-3.2 term. | Rule G (pp. 15, 22) |

### Wording changes (the code is already the code the rules give)

| No. | Tree module | Node | Change | Reason sentence or hint sentence | Rule named |
|---|---|---|---|---|---|
| C3 | `nasopharynx.py` | `np_npc_type` hint | Add 8082/3 to the Rule K order | "basaloid (8083/3) before lymphoepithelial (8082/3) before non-keratinising (8072/3) before keratinising (8071/3)", with the term at each code | Rule K (p. 24) |
| C5 | `thymus.py` | `ty_thymic` hint | Add a sentence | "A name written thymic carcinoma, hepatoid type is the same tumour as a hepatoid carcinoma of the thymus: the word thymic names the site. Record the type's code, not Thymic carcinoma, NOS." | Section 4.2.2 (p. 16); Rule K (p. 24) |
| C6 | `salivary.py` | `sg_picker` hint | Add a sentence | "A mucinous adenocarcinoma with a signet ring subtype is recorded as Signet ring cell carcinoma (8490/3): ICD-O-3.2 lists it as Mucinous carcinoma, signet ring cell type, and 8490 is the higher code." | Rule K (p. 24) |
| C7 | `female_genital.py` | `fg_picker` hint | Add a sentence | "Mucinous carcinoma, gastric type (8482/3) prints the cervix beside it. When the report places it in the uterine corpus, record 8482/3 at the corpus, not Adenocarcinoma, intestinal type (8144/3)." | Rule H (pp. 15, 23); Rule K (p. 24) |
| C8 | `urinary_male_genital.py` | `gu_histology` option "Adenocarcinoma with no type named, mixed adenocarcinoma, ..." | Add to the reason | "ICD-O-3.2 has no term mixed adenocarcinoma. A report that says mixed cell adenocarcinoma (8323/3) or adenocarcinoma with mixed subtypes (8255/3) is found under another carcinoma the report names." | Rule J (p. 24) |
| C9 | `melanoma.py` | `me_picker` option "Malignant Spitz tumor" | Add to the reason for a report of the eye | "ICD-O-3.2 lists Mixed epithelioid and spindle cell melanoma under this code. The code's Preferred term names a skin tumour; the skin topography does not apply to a tumour of the eye." | Rule H (pp. 15, 23) |
| C10 | `melanoma.py` | `me_picker` hint and `me_eye` hint | Reword "are terms for the eye" | "Spindle cell melanoma, type A and type B name the eye as the usual site. A skin report that says type A or type B takes the term; a skin report that says only spindle cell melanoma is Spindle cell melanoma, NOS (8772/3)." | Rule H (p. 23) |
| C11 | `melanoma.py` | `me_skin_histology` Spitz option | Add to the hint | "Take this option when the diagnosis line says spitzoid melanoma, Spitz melanoma or malignant Spitz tumour. A melanoma described as spitzoid only in the microscopic description, with a diagnosis of melanoma, is Malignant melanoma, NOS (8720/3)." | Lookup principle (p. 21) |
| C12 | `thymus.py` | `ty_picker` option "Neuroendocrine tumor, grade 2" | Add to the reason | "ICD-O-3.2 lists Neuroendocrine tumor, grade 3 as a related term of this code, so a report that says grade 3 is recorded here." | Lookup principle (p. 21) |

### No change

(a2) salivary oncocytic and poorly differentiated carcinoma; (a5) the code; (a6) breast; (a7) parathyroid; (a8) the code; (a10) skin; (b1) the code; (b2) the code and the place of 8773/3 Spindle cell melanoma, type A.

### Corrections to the review's own table

The A1 table's "Built" column is out of date for three rows. Salivary Q44: the picker holds both 8480/3 and 8490/3, not the WHO-table 8480/3 alone. Uterine corpus Q86: the picker holds both 8482/3 and 8144/3, not 8144/3 alone. Skin Q32: the picker carries "Pseudovascular squamous cell carcinoma" as a search term of 8074/3, so the term is reachable and records 8074/3.

### Checks run

Every ICD-O-3.2 line above was read from `icdo32.sqlite`. Every ICCC-2017 placement was computed with `iccc_status` and `iccc_subgroups` over the whole site range of each instance: all stay in Group XI, so none of these changes sends a case to another group. The one code that would leave Group XI is 8963/3 Rhabdoid tumor, NOS at C37.9 (ICCC-2017 Group IX), which this file does not use. Nothing was built, committed or run against the tree; the negative controls for C1, C2 and C4 are owed when they are built.
