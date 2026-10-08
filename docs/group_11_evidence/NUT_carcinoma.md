# Group 11 evidence — NUT carcinoma (8023/3), every site

Part `NUT_carcinoma`. Evidence only: this file writes no tool JSON. The machine-readable copy is
`NUT_carcinoma.json` beside it; every quote in it was checked against its PDF page of the text file.
Page numbers below are PDF pages. For the rules file, PDF page 1 is printed page 14.

## 1 Sources

| File | Citation | WHO volume |
|---|---|---|
| `NUT-carcinoma-any-site__Luo-2025.txt` | Luo J, Bishop JA, DuBois SG, Hanna GJ, Sholl LM, Stelow EB, Thompson LDR, Shapiro GI, French CA. Hiding in plain sight: NUT carcinoma is an unrecognized subtype of squamous cell carcinoma of the lungs and head and neck. *Nat Rev Clin Oncol* 2025;22:292–306. doi:10.1038/s41571-025-00986-3 | Cites WHO Thoracic Tumours, 5th ed., 2021, pp. 364–367 (Luo 2025, PDF p. 12); Head and Neck Tumours Part A, 5th ed., 2024, pp. 65–67 (PDF p. 12); Paediatric Tumours, 5th ed., 2022, pp. 908–909 (PDF p. 13) |
| `NUT-carcinoma-paediatric__Lemelle-2022.txt` | Lemelle L, Moya-Plana A, Dumont B, Fresneau B, Laprie A, Claude L, et al. NUT carcinoma in children, adolescents and young adults. *Bull Cancer* 2022;109:491–504. doi:10.1016/j.bulcan.2022.01.015 | Cites the 2015 WHO classification of lung tumours (Travis 2015, reference 39) for the rename. The text-file header says "Eur J Cancer 2022" and "cites WHO 5th ed."; both are wrong (section 10) |
| `ALL-paediatric-occurrence__Pfister-2022.txt` | Pfister SM, Reyes-Mugica M, Chan JKC, et al. A Summary of the Inaugural WHO Classification of Pediatric Tumors. *Cancer Discov* 2022;12(2):331–355 | WHO Paediatric Tumours, 5th ed., 2022 |
| `RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt` | WHO. International Classification of Diseases for Oncology, 3rd ed., 1st revision, section 4, printed pp. 14–28 | Coding manual |

The latest WHO volume for each site is current: Thoracic 2021, Head and Neck 2024, Paediatric 2022.
None of the three chapters is in the files; Luo cites each.

## 2 Entities

ICD-O-3.2 holds 8023/3 with the Preferred term *Nuclear protein in testis (NUT)-associated carcinoma*
and the synonyms *NUT carcinoma* and *NUT midline carcinoma*. It holds no other behaviour for 8023.
The WHO defines the entity as a poorly differentiated carcinoma with a NUTM1 rearrangement
(Luo 2025, PDF p. 2).

| Entity | Code | ICD-O-3.2 term (level) | Sites | Paediatric | Decision | Page |
|---|---|---|---|---|---|---|
| NUT carcinoma, thorax | 8023/3 | NUT carcinoma (Synonym) | Lung C34 (XIf4), thymus C37.9 (XIf5), mediastinum C38.1–C38.3 and overlap C39.8 (XIf10) | occurs | option | Lemelle 2022, PDF p. 6 (13-year-old boy); Luo 2025, PDF p. 12 (11-year-old girl, reference 34); Luo 2025, PDF p. 2 |
| NUT carcinoma, head and neck | 8023/3 | NUT carcinoma (Synonym) | Nasal cavity C30.0, paranasal sinuses C31, larynx and other mucosal sites (XIf10); nasopharynx C11 (XIc) | occurs | option | Pfister 2022, PDF p. 14 (Table 3); Lemelle 2022, PDF p. 6 |
| NUT carcinoma, salivary gland and thyroid | 8023/3 | NUT carcinoma (Synonym) | C07.9–C08.9 (XIf1); C73.9 (XIb) | not reported | picker | Luo 2025, PDF p. 5 |
| NUT carcinoma, skin | 8023/3 | NUT carcinoma (Synonym) | C44, C51.9, C60.9, C63.2 (XIe) | not reported | picker | Luo 2025, PDF p. 12 |
| NUT carcinoma, other specified and unknown sites | 8023/3 | NUT carcinoma (Synonym) | Pancreas C25, central nervous system C70–C72 (XIf10); bladder C67 (XIf8); unknown primary C80.9 (XIf11) | rare | option on the general tree | Lemelle 2022, PDF p. 4; Luo 2025, PDF p. 13 (2-year-old, newborn) |
| NUT carcinoma, colorectum, appendix, breast, cervix, eye | 8023/3 | NUT carcinoma (Synonym) | XIf2, XIf3, XIf6, XIf7, XIf9 | not reported | picker | Luo 2025, PDF p. 5 |
| NUT carcinoma, kidney | 8023/3 | NUT carcinoma (Synonym) | C64.9 (VIb) | occurs | refer to Group VI | Lemelle 2022, PDF p. 4; Luo 2025, PDF p. 12 |
| NUT carcinoma, liver | 8023/3 | NUT carcinoma (Synonym) | C22.0–C22.1 (VIIb) | rare | refer to Group VII | Luo 2025, PDF p. 13 |
| NUT carcinoma, ovary and testis | 8023/3 | NUT carcinoma (Synonym) | C56.9, C62 (Xd) | not reported | refer to Group X | ICCC-2017 only |
| NUT carcinoma, bone, soft tissue, peripheral nerve, adrenal | 8023/3 | NUT carcinoma (Synonym) | C40–C41, C49, C47, C74: no ICCC-2017 range | rare | registrar | Lemelle 2022, PDF p. 4 (iliac bone); Lemelle 2022, PDF p. 8 (Table I, Chau: bone or soft tissue 6%) |
| NUTM1-rearranged sarcoma | 8805/3 (verification only) | Undifferentiated sarcoma (Preferred) | Bone (VIIIe); other sites (IXe) | not reported | refer to Group VIII or IX | Luo 2025, PDF pp. 2, 5 |
| NUTM1-rearranged leukaemia | 9811/3 (verification only) | B lymphoblastic leukemia/lymphoma, NOS (Preferred) | C42.1 (Ia1) | not reported | refer to Group I | Luo 2025, PDF pp. 5, 13 |
| NUTM1-rearranged porocarcinoma | 8409/3 | Porocarcinoma, NOS (Preferred) | Skin (XIe) | not reported | back to the skin screen | Luo 2025, PDF p. 5 |
| Poroma with YAP1::NUTM1 fusion | 8409/0 | Poroma, NOS (Preferred) | Skin | not reported | exclusion, on the skin screen | Luo 2025, PDF p. 12 (reference 22) |

Paediatric occurrence. The tumour occurs at any age; onset in infancy is exceptional (Lemelle 2022,
PDF p. 3). The registry series give a median age of 23.6 years (Lemelle 2022, PDF p. 3; Luo 2025,
PDF p. 6, range 1–82 years) and 18.1 years in the French series (Lemelle 2022, PDF p. 3). The Bauer
series held 63 patients including 25 children, with thorax 56% and head and neck 21% (Lemelle 2022,
PDF p. 9, Table I). The lung and mediastinum or the head and neck hold the primary in 70% of cases
(Lemelle 2022, PDF p. 4), and the paranasal sinuses are the commonest head and neck site
(Lemelle 2022, PDF p. 6). The WHO Paediatric Tumours volume lists NUT carcinoma among the malignant
head and neck tumours and not in its thoracic chapter (Pfister 2022, PDF p. 14; Luo 2025, PDF p. 12).

No benign, borderline or in situ NUT entity is reported in people (Luo 2025, PDF p. 3, Table 1), so
this part has no exclusion of its own.

## 3 The pathway

The part is one cross-site path of four screens. Each calling tree supplies the site; the NUT path
never sets one.

**Entry option (`nut_site_option`).** Each calling tree adds one option to its own histology screen,
"What does the histology report call the tumour?":

- *NUT carcinoma (also written NUT midline carcinoma, BRD4::NUTM1 carcinoma or carcinoma with t(15;19)
  translocation), or a carcinoma reported with a NUT immunostain or a NUTM1 gene result* → goes to
  `nut_result`. Recognition aid: "Reports describe a poorly differentiated or undifferentiated
  carcinoma, sometimes with abrupt keratinization, and nuclear staining for NUT." Sources: the WHO
  definition (Luo 2025, PDF p. 2); the old name carcinoma with t(15;19) translocation (Luo 2025,
  PDF p. 2); poorly differentiated histology (Lemelle 2022, PDF p. 6); squamous differentiation in a
  third of cases (Luo 2025, PDF p. 3); microgranular nuclear staining (Lemelle 2022, PDF p. 7).

The option sits on the histology screen of the lung, thymus, nasopharynx and general carcinoma trees.
On the thyroid, salivary gland and colorectum trees 8023/3 sits in the long-tail picker; choosing it
also goes to `nut_result`, so the deposit, referral and basis screens still apply.

**`nut_result` — "What does the file report for this tumour?"** Hint: "Choose the first answer that
matches the file. Keratin, p63, p40 and CD99 stains do not decide NUT carcinoma; a NUT immunostain or
a NUTM1 gene test does." (p63 nonspecific: Lemelle 2022, PDF p. 7; CD99 misleads toward Ewing sarcoma:
Lemelle 2022, PDF p. 7; keratins in 85%: Luo 2025, PDF p. 6.)

| Option | Outcome | Page |
|---|---|---|
| The sample is a deposit in a lymph node, bone, liver or another organ, and the file names a different site where the tumour began | refer, recapture site | Luo 2025, PDF p. 8; Lemelle 2022, PDF p. 6; rules, PDF p. 7 (Table 19) |
| A sarcoma with a NUTM1 rearrangement, in a bone | refer to Group VIII | Luo 2025, PDF pp. 2, 5 |
| A sarcoma with a NUTM1 rearrangement, at any other site | refer to Group IX | Luo 2025, PDF p. 5 |
| A leukaemia with a NUTM1 rearrangement | refer to Group I | Luo 2025, PDF pp. 5, 13 |
| A skin poroma or porocarcinoma with a YAP1::NUTM1 fusion | back to the skin histology screen | Luo 2025, PDF pp. 5, 12 |
| The diagnosis names NUT carcinoma or NUT midline carcinoma | go to `nut_basis` | Luo 2025, PDF p. 2 |
| The diagnosis names another carcinoma, and the file reports a NUT immunostain or NUTM1 gene test | go to `nut_ihc` | Luo 2025, PDF p. 7 |

Each referral reason names why: "A NUTM1-rearranged sarcoma is not NUT carcinoma. It is coded with
the malignant bone tumours (Group VIII)."

**`nut_basis` — "Does the file hold a positive NUTM1 gene result?"** Hint names how the result is
written: a NUTM1 (NUT) rearrangement, a translocation t(15;19), or a BRD4::NUTM1, BRD3::NUTM1 or
NSD3::NUTM1 fusion, by FISH, RT-PCR or sequencing (Luo 2025, PDF p. 2; Lemelle 2022, PDF p. 6).

| Option | Records | Basis |
|---|---|---|
| Yes: a NUTM1 rearrangement or fusion is reported | 8023/3 | 8 |
| No: the diagnosis rests on the histology report, with or without a NUT immunostain | 8023/3 | 7 |

Both reasons read: "Recorded as Nuclear protein in testis (NUT)-associated carcinoma (8023/3). Squamous
features named in the same report do not change the code."

**`nut_ihc` — "Which NUT results does the file report?"** Hint: "Choose the first answer that matches.
A NUT immunostain counts only when the report states nuclear staining in more than half (over 50%) of
the tumour cells." Options and rules are in section 4.

## 4 Immunohistochemistry rules

The panel is `nut_ihc`, reached only from a report that names a carcinoma. Order matters: the first
rule that fires wins.

| Order | Positive | Records | Basis | Page |
|---|---|---|---|---|
| 1 | NUTM1 rearrangement or fusion (FISH, RT-PCR or sequencing) | 8023/3 | 8 | Luo 2025, PDF p. 2; Lemelle 2022, PDF pp. 6–7 |
| 2 | NUT immunostain, nuclear staining in more than 50% of tumour cells | 8023/3 | 7 | Luo 2025, PDF p. 7; Lemelle 2022, PDF pp. 6–7 |
| Fallback | Neither: stain negative or in 50% or fewer, no NUTM1 rearrangement | no NUT code; back to the site's histology screen | — | Luo 2025, PDF p. 7 |

Luo states that diffuse nuclear NUT staining in more than 50% of nuclei is 100% specific in a tumour
with carcinoma histology (Luo 2025, PDF p. 7). Lemelle gives the stain a sensitivity of 87% and a
specificity of 100% (Lemelle 2022, PDF p. 6) and calls the molecular test definitive (Lemelle 2022,
PDF p. 2). The BRD3 or BRD4 to NUT translocation is specific for NUT carcinoma, but other tumours carry
NUT gene fusions (Lemelle 2022, PDF p. 7): sarcomas with CIC, BCORL1, MXD1, MXD4 or MGA, porocarcinomas
with YAP1 and leukaemias (Luo 2025, PDF p. 5, Table 2). That is why the rules apply only to a
carcinoma and why `nut_result` sends the other NUTM1 tumours away before the panel.

Markers that do not decide: keratins (85%), CK5, p63 and p40 (Luo 2025, PDF p. 6); p63 is
nonspecific in this setting (Lemelle 2022, PDF p. 7); TTF1, desmin, myogenin and lymphoid markers are
generally negative (Lemelle 2022, PDF p. 6); CD99 suggests Ewing sarcoma falsely (Lemelle 2022,
PDF p. 7).

The engine's checklist needs a fallback code. This panel's honest fallback is the report's own term,
on the calling tree's histology screen. If the engine requires a fixed code, 8010/3 *Carcinoma, NOS*
is the nearest code that covers every carcinoma reaching the panel.

## 5 Registration without tissue

| Evidence on file | Records | Basis | Page |
|---|---|---|---|
| A referral or clinical note only | 8000/3 Neoplasm, malignant | 1 | Lemelle 2022, PDF p. 2 |
| An imaging report only, with or without a blood test result | 8000/3 Neoplasm, malignant | 2 | Lemelle 2022, PDF p. 5; Luo 2025, PDF p. 8 |
| A cytology report that names NUT carcinoma (for example a lymph-node fine-needle aspirate) | 8023/3 | 5 | Lemelle 2022, PDF pp. 5, 8 |

Imaging cannot recognise NUT carcinoma: its features are non-specific (Lemelle 2022, PDF p. 5) and
it looks like squamous carcinoma of the lung or head and neck (Luo 2025, PDF p. 8). No tumour marker
or hormone appears in Visser Table 4 or in either source for this tumour, so basis 4 never records
8023/3. Cytology is a recognised specimen: lymph nodes are sampled by cyto-aspiration (Lemelle 2022,
PDF p. 5) and Bishop's series studied 26 cytology specimens (Lemelle 2022, PDF p. 8, Table I).

## 6 Laboratory tests

Neither source gives a serum, plasma or urine test a diagnostic role in NUT carcinoma. The part
needs no laboratory screen.

## 7 Rules A to K

| Rule | Applies | How it reaches the clerk |
|---|---|---|
| A | yes | On the calling tree's site screen. A neck mass is usually a cervical lymph-node deposit of a sinonasal primary (Lemelle 2022, PDF p. 6); the deposit option on `nut_result` sends it to its primary site (rules, PDF p. 1) |
| B | no | No prefix site occurs; paranasal sinus is an ICD-O site (C31) |
| C | yes | Hint on the lung and thymus trees' site screens: a tumour involving the lung and mediastinum with no stated origin records C39.8 (rules, PDF p. 5, Table 17; Lemelle 2022, PDF p. 7, "mediastinopulmonary") |
| D | no | No lymphoma is recorded here |
| E | yes | Reason on the leukaemia referral; Group I records C42.1 (rules, PDF p. 2) |
| F | yes | Every code option records /3; each reason names 8023/3. ICD-O-3.2 holds 8023 at /3 only, and no human precursor lesion is reported (Luo 2025, PDF p. 3) |
| G | no | No grade screen: the entity is poorly differentiated by definition (Luo 2025, PDF p. 2); the sixth digit is not built |
| H | yes | ICD-O-3.2 prints no site beside 8023, and "midline" names no site: two thirds of tumours are lateral (Lemelle 2022, PDF p. 4; rules, PDF pp. 10–11). The option label lists NUT midline carcinoma as a name only; the calling tree sets the site |
| J | no | No compound word roots (rules, PDF p. 3) |
| K | yes | Reason on every 8023/3 option: squamous features in the same report do not change the code. The entity is a carcinoma with squamous or poorly differentiated features (Luo 2025, PDF pp. 5–6), so 8023/3 includes every term. Strict numeric Rule K (rules, PDF p. 3) would choose 8070/3 to 8072/3; registrar question 1 |

There is no Rule I.

## 8 Code currency

- **8023/3.** New in ICD-O-3.2 and absent from the REDCap Group 11 option list (Code Currency Check
  2026-10-08, section 6). No term is [obs]. Build one entry with the subgroup computed from the site.
  Put it on the REDCap-side list in `docs/TODO.md` section 7 and the Group 11 Layer 1 repair package.
  The currency check names XIc, XIf4, XIf5 and XIe. ICCC-2017's 8010–8041 ranges place 8023/3 at every
  Group XI carcinoma site — XIb, XIc, XIe and XIf1 to XIf11 — and in VIb, VIIb and Xd. The check's
  subgroup column needs that correction; the nasal cavity and paranasal sinuses, the commonest head
  and neck site, are XIf10.
- **8409/3.** ICD-O-3.2 Preferred term *Porocarcinoma, NOS*; REDCap's string is "Eccrine poroma,
  malignant", an ICD-O-3.2 synonym. The skin part owns the code; note the string on the REDCap-side list.
- **8000/3** *Neoplasm, malignant*, **8805/3** *Undifferentiated sarcoma* and **9811/3** *B
  lymphoblastic leukemia/lymphoma, NOS*: no finding. 8805 and 9811 verify referral groups only.

## 9 Conflicts with other groups

| Group | Codes | Sites | Issue |
|---|---|---|---|
| VI | 8023 | C64.9 | ICCC-2017 places 8023/3 at the kidney in VIb, and both sources report kidney primaries (Lemelle 2022, PDF p. 4; Luo 2025, PDF p. 12). The Group VI renal tree must offer 8023/3 |
| VII | 8023 | C22.0, C22.1 | VIIb. Luo cites a 2-year-old with a pancreatic or hepatic primary (Luo 2025, PDF p. 13). The liver is a common deposit site (Luo 2025, PDF p. 8), so a liver sample is a primary only when the file says so |
| X | 8023 | C56.9, C62, C34, C38.1–C38.3 | Xd at the gonads. A pulmonary NUT carcinoma can show a germ cell phenotype (Luo 2025, PDF p. 12, reference 17), so a thoracic tumour with germ cell markers and a NUTM1 result belongs here |
| VIII | 8023, 9364, 8805 | C40–C41 | NUT carcinoma is misdiagnosed as Ewing sarcoma (Luo 2025, PDF p. 3; Lemelle 2022, PDF p. 7); the corrected later report is coded (Lemelle 2022, PDF p. 8). NUTM1-rearranged sarcoma of bone goes to Group VIII. 8023/3 at bone has no ICCC range |
| IX | 9364, 8805 | C49, C70–C72, colon | NUTM1-rearranged sarcomas arise in soft tissue, the central nervous system and the colon (Luo 2025, PDF p. 5) |
| I | 9811 | C42.1 | NUT carcinoma can present like leukaemia (Luo 2025, PDF p. 3); NUTM1 fuses in B-cell precursor leukaemia (Luo 2025, PDF p. 13) |
| III | 8023 | C70–C72 | Lemelle reports central nervous system primaries (Lemelle 2022, PDF p. 4). ICCC-2017 places 8023/3 there in XIf10, so a Group III tree refers a NUT carcinoma to Group XI |

Within Group XI, the boundaries are nasopharyngeal-type undifferentiated carcinoma and salivary gland
carcinoma (Lemelle 2022, PDF p. 7), thymic carcinoma (Luo 2025, PDF p. 2) and squamous cell carcinoma
(Rule K). An untested NUT carcinoma is coded as the report names it; the tool raises no prompt to test.

Alias layer. A bare alias "NUTM1" or "NUTM1-rearranged" must open `nut_result`, not code 8023/3,
because sarcomas, porocarcinomas and leukaemias carry NUTM1 fusions (Luo 2025, PDF p. 5). The
entity-specific aliases are NUT carcinoma, NUT midline carcinoma, carcinoma with t(15;19)
translocation, BRD4::NUTM1, BRD3::NUTM1 and NSD3::NUTM1. Check `alias_index.json` for any Group I or
Group IX alias on these strings: a shared alias enters the lowest-numbered group.

## 10 Data gaps

1. **The WHO chapters' own criteria.** Thoracic (2021) pp. 364–367, Head and Neck Part A (2024)
   pp. 65–67, Paediatric (2022) pp. 908–909. The 50% threshold rests on Luo's figure legend (Luo 2025,
   PDF p. 7). Neither file names the C52B clone or a "speckled" pattern; Lemelle calls it
   microgranular (Lemelle 2022, PDF p. 7). Candidate: Haack H et al., *Am J Surg Pathol*
   2009;33:984–991 (Luo reference 26), and the WHO chapters.
2. **Site distribution for ages 0 to 18.** The series mix children and adults. Candidate: Bauer DE et
   al., *Clin Cancer Res* 2012 (25 children; Luo reference 40); Chau NG et al., *JNCI Cancer Spectr*
   2020;4:pkz094.
3. **Ages in the thyroid and salivary gland reports.** Candidate: Barletta JA et al., *Am J Surg
   Pathol* 2022;46:1706–1715; Agaimy A et al., *Am J Surg Pathol* 2018;42:877–884.
4. **Lemelle header.** The text file names *Eur J Cancer*; the PDF is *Bull Cancer* 2022;109:491–504.
   The paper cites the 2015 WHO lung classification, not a 5th edition volume.
5. **ICCC subgroup at bone, soft tissue, peripheral nerve, adrenal and lymph node.** ICCC-2017 has no
   range for 8023 there; registrar question 3.

### Registrar questions

1. A diagnosis naming NUT carcinoma and squamous cell carcinoma together: 8023/3, or the numerically
   higher 8070/3 to 8072/3 under Rule K? This evidence recommends 8023/3.
2. A report naming only a poorly differentiated carcinoma with nuclear NUT staining in more than 50%
   of tumour cells: may the tool record 8023/3 at basis 7, including when a NUTM1 FISH test is
   negative? Luo gives the stain 100% specificity; Lemelle calls the molecular test definitive; Luo
   cites a false-negative FISH case (Luo 2025, PDF p. 14, reference 144).
3. NUT carcinoma primary in bone, soft tissue, peripheral nerve or adrenal: which subgroup does the
   tool output, given no ICCC-2017 range?
4. Is the WHO Paediatric head and neck listing enough to make 8023/3 an option on the nasopharynx and
   salivary gland trees, or only where a child case is reported (lung, mediastinum, nasal cavity and
   sinuses)?
5. Cytology naming NUT carcinoma with a NUT immunostain on the cell block: basis 5 or 7?
6. A NUTM1 break-apart FISH result that names no partner, in a carcinoma: basis 8?
