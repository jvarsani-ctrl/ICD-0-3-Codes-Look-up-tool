# Group X — laboratory marker evidence, 2026-10-06

**Purpose.** The Group X "Laboratory results" screen records the value of each test as the report
gives it. The registrar asked what each marker predicts, on published evidence, and chose published
cut-offs over the lab report's own reference range. This file is the evidence for that ruling. It
does not design the feature.

**Method.** Snippets of the Group X and Group III Diagnostic Pathways, the PDFs in
`Group 10 Papers/` and `Group 7 Papers/` (Ferraro), then PubMed. Full text was read where PubMed
Central holds it; otherwise the abstract only, and the reference list says which. Every number below
carries its source.

**Abbreviations.** AFP, alpha-fetoprotein. β-hCG, beta human chorionic gonadotropin (papers write
HCG, hCG or bHCG). LDH, lactate dehydrogenase. CA-125, cancer antigen 125. HE4, human epididymis
protein 4. CEA, carcinoembryonic antigen. CSF, cerebrospinal fluid. NGGCT, non-germinomatous germ
cell tumour. SIOP, International Society of Paediatric Oncology. COG, Children's Oncology Group.
MAKEI, the German cooperative protocols for non-testicular germ cell tumours. IGCCCG, International
Germ Cell Cancer Collaborative Group. ULN, upper limit of normal. PPV and NPV, positive and negative
predictive value.

**Units.** ng/mL equals µg/L. IU/L equals mIU/mL. AFP reported in kU/L converts at 25 ng/mL =
20.8 kU/L (Calaminus 2026, Methods, "Diagnostic and Staging Procedures").

**Codes.** Named by ICD-O-3.2 (`icdo32.sqlite`): germinoma 9064/3 (synonym "Germ cell tumor, NOS");
dysgerminoma 9060/3; germ cell tumour, nonseminomatous 9065/3; embryonal carcinoma 9070/3; yolk sac
tumour 9071/3; teratoma 9080; mixed germ cell tumour 9085/3; choriocarcinoma 9100/3; juvenile
granulosa cell tumour 8622/1; small cell carcinoma, hypercalcaemic type 8044/3 (a Related term under
8044/3). The brief's "germinoma or dysgerminoma (9060)" is ICD-O-3.2's dysgerminoma only; the build
report already records this.

**Read every performance figure for what it measures.** The ovarian figures measure prediction of
*any malignancy*, not of one code. The brain figures measure prediction of a *malignant
non-germinomatous component*, not of one histotype.

---

## 1. Brain: pineal, suprasellar and other intracranial sites

| Marker | Compartment | Raised value predicts | Normal value argues against | Published cut-off (units) | Population | Performance | Source with page |
|---|---|---|---|---|---|---|---|
| AFP | Serum | A malignant NGGCT with a yolk sac component. Also immature teratoma: every immature teratoma in the Mayo Clinic and Japanese cohort had raised AFP, range 12.4–224,865 ng/mL, median 97 | A yolk sac component: every case with histology-proven yolk sac tumour had AFP > 10 ng/mL. It does not exclude an NGGCT: one marker-negative resected tumour held embryonal carcinoma. AFP is rare in pure germinoma: one of the resected germinomas had serum AFP 85 ng/mL; 2 of 166 localised germinomas had serum AFP 10–25 ng/mL | **SIOP CNS GCT 96: > 25 ng/mL** in serum or CSF diagnoses malignant NGGCT without biopsy. **SIOP CNS GCT II: germinoma requires < 25 ng/mL** in serum and CSF. **COG ACNS0122: > 10** (printed "IU/L") or above the institutional normal. **COG ACNS1123: > 10 ng/mL** or above the institutional normal. **Hu: serum ≥ 25 ng/mL** (empirical) | SIOP 96: 149 patients with NGGCT, Europe, age groups < 10, 10–16 and > 16 years. COG: North American trial cohorts (age range not extracted). Takami: 162 histology-proven cases, Mayo Clinic 1988–2017 and the Japanese intracranial germ cell tumour consortium. Hu: 58 intracranial germ cell tumours and 17 controls aged 9–57, one Chinese centre | AFP ≥ 10 ng/mL (higher of serum and CSF) for a malignant non-germinomatous component in resected cases: sensitivity 83.3% (15/18), specificity 78.0% (39/50), PPV 57.7% (15/26), NPV 92.9% (39/42). In SIOP 96, a yolk sac component was found in 19 of 37 AFP-raised patients with full histology; five biopsies showing pure teratoma had AFP 115–430 ng/mL | Calaminus 2017, Methods and Results; Calaminus 2026, Table 2 and Results; Goldman 2015, Patients and Methods; Fangusaro 2019, Patients and Methods; Takami 2022, p. 3, p. 4 and Table 2 (p. 5); Takami 2023, Results; Hu 2016, Abstract |
| AFP | CSF | As serum. Serum is the more sensitive compartment for AFP: of 49 paired cases, 7 had AFP raised in serum only and 1 in CSF only | As serum. In SIOP CNS GCT II no localised germinoma (0 of 166) had CSF AFP above 10 ng/mL | **SIOP and COG apply the serum threshold to either compartment** (> 25 and > 10 ng/mL). **Hu: CSF ≥ 3.8 ng/mL** (empirical adjustment, no sensitivity reported). Infant CSF reference values in §4 | As above. Infant CSF values: 128 infants aged 1–110 days without malignancy | Hu's CSF and serum criteria together raised sensitivity for any intracranial germ cell tumour from 34.6% to 65.4% | Takami 2023, Results; Calaminus 2026, Results; Hu 2016, Abstract; Coakley 2005, Abstract |
| β-hCG | Serum | Choriocarcinoma or a choriocarcinoma component at high values. Germinoma also secretes β-hCG: pure germinomas reached 3,267.5 IU/L (CSF). Above 3,300–6,300 IU/L a choriocarcinoma component was present in every case of one series | A choriocarcinoma component: every case with one showed marked elevation. A raised value does not argue against germinoma | **SIOP CNS GCT 96: > 50 IU/L** in serum or CSF diagnoses malignant NGGCT without biopsy. **SIOP CNS GCT II: germinoma requires < 50 IU/L.** **COG ACNS0122: > 50 IU/L**; a germinoma above 50 IU/L was treated as high risk. **COG ACNS1123: > 100 IU/L** for NGGCT; germinoma 5–≤ 50 IU/L, or ≤ 100 IU/L for "bifocal, pineal lesion + diabetes insipidus or histologically confirmed germinoma". **Hu: serum ≥ 2.5 IU/L.** **Takami 2023: 3,300–6,300 IU/L** for a choriocarcinoma component. Normal β-hCG < 5 IU/L (Fangusaro) | As above. Takami 2023: 161 histology-proven cases from the same two cohorts | β-hCG ≥ 100 IU/L (higher of serum and CSF) for a malignant non-germinomatous component in resected cases: sensitivity 61.5% (8/13), specificity 82.1% (32/39), PPV 53.3% (8/15), NPV 86.5% (32/37). In SIOP 96, of 21 patients with β-hCG raised alone and full histology, choriocarcinoma was found in 4 and yolk sac tumour in 1. Hu serum ≥ 2.5 IU/L: sensitivity 34%, specificity 100% for any intracranial germ cell tumour against 17 controls | Calaminus 2017, Methods and Results; Calaminus 2026, Table 2; Goldman 2015, Patients and Methods; Fangusaro 2019, Patients and Methods and Results; Takami 2022, Table 2 (p. 5); Takami 2023, Results and Discussion; Hu 2016, Abstract and Results |
| β-hCG | CSF | As serum. CSF is the more sensitive compartment for β-hCG: of 52 paired cases, 3 had β-hCG raised in CSF only, all with a germinoma component | As serum | **SIOP and COG apply the serum threshold to either compartment.** **Hu: CSF ≥ 8.2 IU/L.** A control craniopharyngioma reached CSF β-hCG 8 IU/L | As above | Hu CSF ≥ 8.2 IU/L: sensitivity 47%, specificity 100% for any intracranial germ cell tumour against non-germ-cell controls | Takami 2023, Results; Hu 2016, Abstract and Discussion |
| AFP or β-hCG, either raised | Serum or CSF | A malignant non-germinomatous component in half of cases: of 35 marker-positive resections, 18 (51%) held one and 17 (49%) were germinoma, teratoma or both | 19 of 20 marker-negative resections held no malignant non-germinomatous component | AFP ≥ 10 ng/mL or β-hCG ≥ 100 IU/L (COG thresholds) | Takami 2022 resection cohort, n = 77 | Sensitivity 94.7% (18/19), specificity 52.8% (19/36), PPV 51.4% (18/35), NPV 95.0% (19/20) | Takami 2022, pp. 3–4 and Table 2 (p. 5) |

**The SIOP and COG cut-offs differ, and each comes from its own population.** SIOP sets AFP at
25 ng/mL and β-hCG at 50 IU/L (European trials). COG sets AFP at 10 ng/mL and β-hCG at 50 IU/L in
ACNS0122 and 100 IU/L in ACNS1123 (North American trials). Hu 2016 lists three criteria in use since
the 1990s: β-hCG ≥ 50 IU/L or AFP ≥ 10 ng/mL; β-hCG ≥ 100 IU/L or AFP ≥ 50 ng/mL; β-hCG > 50 IU/L
or AFP > 25 ng/mL, and states that none rests on pathology (Hu 2016, Abstract and Background).
Takami 2022 records cases of over- and under-diagnosis under both the COG and the SIOP thresholds
(p. 7). Ferraro states that the SIOP cut-offs were reported for patients older than 4 years (aop
p. 9); the retrieved Calaminus 2017 methods text states no age limit.

**Hu's low cut-offs answer a different question.** They separate an intracranial germ cell tumour of
any type, germinoma included, from non-germ-cell lesions (Langerhans cell histiocytosis and other
tumours). They do not separate germinoma from NGGCT. The Group III pathway uses them for routing to
Group X (Group III pathway, §3.2).

**The ACNS1123 wording.** Fangusaro 2019 prints the NGGCT entry criterion as "β-hCG level greater
than 100 IU/L and serum and/or CSF α-fetoprotein (AFP) level greater than 10 ng/mL". The conjunction
is "and" as printed.

---

## 2. Ovary

| Marker | Compartment | Raised value predicts | Normal value argues against | Published cut-off (units) | Population | Performance (any malignancy unless stated) | Source with page |
|---|---|---|---|---|---|---|---|
| AFP | Serum | Yolk sac tumour (9071) or a yolk sac component of a mixed germ cell tumour (9085). Also immature teratoma, embryonal carcinoma and, rarely, Sertoli-Leydig cell tumour | Yolk sac tumour: more than 90% of yolk sac tumours have raised AFP. In 78 children aged 0–10 with ovarian yolk sac tumour, AFP was < 200 µg/L in 5.1%, 200–1,000 in 6.4%, 1,000–10,000 in 35.9% and > 10,000 in 48.7% | **> 10 ng/mL** (lab threshold, Midwest consortium). **20 µg/L**, the threshold most authors use (Ferraro). **> 1,000 ng/mL: paediatric convention for a yolk sac component within a teratoma, in use for over 25 years**; the European Society for Medical Oncology guideline sets no such threshold. The Malignant Germ Cell International Consortium classed a mixed germ cell tumour with AFP > 1,000 ng/mL as "putative yolk sac tumour" | Lawrence: girls 2–21 years, 10 United States children's hospitals, 2010–2016, 401 patients. Bayramoglu: 1,128 females under 30, one centre, 2003–2024. Faure Conter: 251 patients, median 13 years | Lawrence: sensitivity 42%, specificity 98%, PPV 86%, NPV 88%. Bayramoglu: sensitivity 92%, specificity 88%, PPV 86%, NPV 93% (cut-off not stated). Yolk sac tumour > 90% positive; immature and mature teratoma < 20%; dysgerminoma, embryonal carcinoma and choriocarcinoma 0% | Lawrence 2020, Tables 2 and 5; Bayramoglu 2025, Table 4; Ferraro aop p. 10 and Table 4 (p. 10); Pashankar 2022, p. 68; Faure Conter 2018, Abstract; van Heerden 2019, Table 4 (p. 107) |
| β-hCG | Serum | Choriocarcinoma (9100/3) or a choriocarcinoma component. Also embryonal carcinoma, and rarely dysgerminoma. Pregnancy must be excluded in adolescents | A choriocarcinoma component | **> 2.3 mIU/mL** (lab threshold, Midwest consortium). No ovary-specific cut-off for choriocarcinoma found | As above | Lawrence: sensitivity 44%, specificity 76%, PPV 32%, NPV 85%. Bayramoglu: sensitivity 85%, specificity 90%, PPV 83%, NPV 89% | Lawrence 2020, Tables 2 and 5; Bayramoglu 2025, Table 4; van Heerden 2019, Table 4 (p. 107); Schneider 2001, Abstract |
| LDH | Serum | Malignancy, non-specifically. Dysgerminoma is the germ cell tumour listed against LDH; haemolysis, haematological malignancy and tissue necrosis also raise it | Weakly against malignancy (NPV 92%) | **> 170 U/L** (lab threshold, Midwest consortium). No diagnostic cut-off published | As above | Lawrence: sensitivity 95%, specificity 13%, PPV 32%, NPV 92%. Bayramoglu: sensitivity 78%, specificity 82%, PPV 76%, NPV 83% | Lawrence 2020, Tables 2 and 5; Bayramoglu 2025, Table 4; van Heerden 2019, Table 4 (p. 107) |
| CA-125 | Serum | Epithelial tumours. Also raised in juvenile granulosa cell tumour (48%) and in endometriosis and liver disease | Weakly against malignancy (NPV 87%) | **> 35 U/mL** (lab threshold, Midwest consortium; an adult-derived limit). Paediatric reference intervals exist (CALIPER); the values were not accessed | As above. Harris: 70 ovarian juvenile granulosa cell tumours, median age 10 | Lawrence: sensitivity 59%, specificity 81%, PPV 49%, NPV 87%. Bayramoglu: sensitivity 60%, specificity 75%, PPV 58%, NPV 77%. Raised in 20 of 42 juvenile granulosa cell tumours | Lawrence 2020, Tables 2 and 5; Bayramoglu 2025, Table 4; Harris 2025, Table 1; van Heerden 2019, Table 4 (p. 107); Bevilacqua 2014, Abstract |
| HE4 | Serum | Malignant and borderline epithelial tumours | No source found | **No paediatric cut-off found.** Paediatric reference intervals exist (CALIPER); the values were not accessed | — | No paediatric performance study found | van Heerden 2019, Table 4 (p. 107); Bevilacqua 2014, Abstract |
| CEA | Serum | Mucinous tumours; the Midwest cohort records one malignant case | Nothing: sensitivity 5% | **> 3 ng/mL** (lab threshold, Midwest consortium) | Lawrence cohort | Sensitivity 5%, specificity 100%, PPV 100% (one patient), NPV 78% | Lawrence 2020, Tables 2 and 5 and Discussion |
| Inhibin A | Serum | Granulosa cell tumour, including juvenile granulosa cell tumour (8622/1). Inhibin B is the more sensitive marker of the two | Weakly: inhibin A was normal in 35% of juvenile granulosa cell tumours | **> 80 pg/mL** (lab threshold, Midwest consortium). Inhibin B thresholds were age-banded, 27 to 136 pg/mL | Lawrence and Harris cohorts | Lawrence: sensitivity 32%, specificity 97%, PPV 82%, NPV 80% for any malignancy. Harris: inhibin A raised in 22 of 34 (65%) and inhibin B in 38 of 42 (90%) juvenile granulosa cell tumours. Lin: the best-performing combinations all held β-hCG; β-hCG with inhibin A and LDH had accuracy 0.951 | Lawrence 2020, Tables 2 and 5; Harris 2025, Table 1; Lin 2025, Abstract; van Heerden 2019, Table 4 (p. 107) |
| Calcium | Serum | Small cell carcinoma of the ovary, hypercalcaemic type (8044/3). Also listed for sex cord-stromal tumours, bone tumours, parathyroid disease and rhabdoid tumours; dysgerminoma raises calcium through calcitriol in reported cases | Weakly: calcium was normal in 38% of measured hypercalcaemic-type small cell carcinomas | **No tumour-specific cut-off found.** The papers define hypercalcaemia by the laboratory range | Young: 150 cases aged 9–43 (mean 23.9). Tischkowitz: fewer than 500 reported cases | Calcium raised in 49 of 79 measured (62%); about 60% in the later review | Young 1994, Abstract; Tischkowitz 2020, Abstract; van Heerden 2019, Table 4 (p. 107); Hara 2022, title (case report and review) |

**The sources disagree on embryonal carcinoma.** van Heerden lists embryonal carcinoma against AFP
(Table 4, p. 107); Ferraro gives 0% AFP-positive for embryonal carcinoma, from series that tie AFP to
yolk sac elements (Table 4, p. 10, citing Talerman 1980 among others).

**The two paediatric cohorts disagree.** Lawrence 2020 and Bayramoglu 2025 report different
performance for the same markers. Lawrence states its thresholds and the testing rate (AFP in 94%,
LDH in 39%, inhibin A in 25%; Table 4) and warns that markers were drawn more often when malignancy
was suspected (Discussion). Bayramoglu does not state its thresholds.

---

## 3. Testis, and sites outside the gonads (mediastinum, sacrococcygeal, retroperitoneum and others)

| Marker | Compartment | Raised value predicts | Normal value argues against | Published cut-off (units) | Population | Performance | Source with page |
|---|---|---|---|---|---|---|---|
| AFP | Serum | Yolk sac tumour (9071) or a yolk sac component (9085). Outside the liver, after liver disease, pregnancy and hereditary causes are excluded, AFP above the age-related range establishes a malignant germ cell tumour with a substantial yolk sac or choriocarcinoma component (MAKEI). AFP rules against pure seminoma: IGCCCG classes seminoma as "normal AFP" | Yolk sac tumour beyond infancy. In infants under 6 months AFP overlaps between benign and malignant testis tumours, and in fetuses and neonates AFP alone does not identify a sacrococcygeal yolk sac focus even against the age-related range. Congenital teratomas carried AFP 15,900–170,000 µg/L | **"Clearly increased for patient age"** (Prepubertal Testis Tumor Registry), read against §4. **20 µg/L** outside infancy (Ferraro). Prognostic only: **IGCCCG < 1,000 / 1,000–10,000 / > 10,000 ng/mL** (adult); **≥ 10,000 µg/L** at baseline in patients over 1 year (Ferraro aop p. 9, citing the Pediatric Oncology Group 9049 / Children's Cancer Group 8882 trial) | Ross: 395 prepubertal testis tumours. Schneider: MAKEI experience. Dieckmann: 422 adult testicular germ cell tumours (18 aged ≤ 20). IGCCCG: adults | Yolk sac tumour > 90% AFP-positive; teratoma < 20%; seminoma, dysgerminoma, embryonal carcinoma and choriocarcinoma 0% (threshold 20 µg/L). Adult nonseminoma 60.1%, seminoma 2.8% (the seminoma elevations unrelated to the tumour) | Schneider 2001, Abstract; Ross 2002, Abstract; Ferraro aop pp. 9–10 and Table 4; Calaminus 2016, p. 122 (IGCCCG table); Dieckmann 2019, Table 2; Phi 2021, p. 409 |
| β-hCG | Serum | Choriocarcinoma (9100/3) or a choriocarcinoma component. Seminoma and germinoma secrete small amounts | A choriocarcinoma component. A raised value does not argue against seminoma: 28.0% of adult seminomas had raised β-hCG, most below 10 × ULN | **No diagnostic cut-off found for extracranial sites.** Prognostic only: **IGCCCG < 5,000 / 5,000–50,000 / > 50,000 IU/L** (adult). Normal < 5 IU/L (COG ACNS1123 report) | Dieckmann adult cohort; IGCCCG adults | Adult nonseminoma 53.0%, seminoma 28.0% | Ferraro aop p. 9; Dieckmann 2019, Table 2 and Results; Calaminus 2016, p. 122; Fangusaro 2019, Results |
| LDH | Serum | Tumour burden in any germ cell tumour; prognostic in advanced disease | Nothing | **No diagnostic cut-off.** Prognostic only: **IGCCCG < 1.5 × ULN / 1.5–10 × ULN / > 10 × ULN** (adult) | Dieckmann adult cohort; IGCCCG adults | Adult seminoma 29.1%, nonseminoma 38.7%. LDH stayed raised at the end of treatment in 30.5% of patients with metastases | Calaminus 2016, p. 118 and p. 122; Dieckmann 2019, Tables 2 and 8 |

**Paediatric testis data are thin.** Ross 2002 is an abstract-level source for the infant overlap.
The age-specific AFP reference values in §4 carry the "raised for age" judgement for the testis and
for sacrococcygeal tumours, which present in the first months of life (Phi 2021, p. 409).

---

## 4. Age-specific AFP reference values

**No pooled upper limit exists.** Ferraro's review rejected most studies on method (Table 2) and
concluded that the spread of reference intervals prevents a pooled upper limit by age; term infants
need more than 8 months, and preterm infants possibly more than 1 year, to reach adult values (aop
p. 7). Blohm 1998 found that children had not reached adult serum AFP (0–6 ng/mL) by age 2 years
(Abstract). Wu 1981 found infant AFP approached adult values at 8 months, with half-lives of 5.5 days
(birth to 2 weeks), 11 days (2 weeks to 2 months) and 33 days (2 to 4 months) (Abstract).

### 4A. Serum AFP, term infants (µg/L, equal to ng/mL)

From Ferraro 2019, Table 3 ("Reference intervals for preterm and term infants in the selected
studies", aop pp. 8–9). The statistic differs by study; each row names it.

| Age | Interval (µg/L) | Statistic | n | Assay | Original study |
|---|---|---|---|---|---|
| Birth | 9,000–191,000 | 95.5% central range | 13 | Enzyme immunoassay, Abbott | Blohm 1998 |
| Birth | 15,000–147,000 | 95% central range | 184 | DELFIA | Bader 2004 |
| Birth | 30,875–44,350 | 10th–90th percentile | 8 | In-house radioimmunoassay | Lahdenne 1991 |
| 1 day | 7,900–166,000 | 95.5% central range | 13 | Abbott | Blohm 1998 |
| 2 days | 7,000–144,500 | 95.5% central range | 13 | Abbott | Blohm 1998 |
| 3 days | 6,000–126,000 | 95.5% central range | 13 | Abbott | Blohm 1998 |
| 3 days | 9.7–111,900 | 95% central range | 241 | DELFIA | Bader 2004 |
| 7 days | 3,500–73,600 | 95.5% central range | 13 | Abbott | Blohm 1998 |
| 7–14 days | 1,500–59,000 | 95.5% central range | 13 | Abbott | Blohm 1998 |
| 15–21 days | 575–22,900 | 95.5% central range | 13 | Abbott | Blohm 1998 |
| 22–28 days | 316–6,300 | 95.5% central range | 13 | Abbott | Blohm 1998 |
| 1 month–6 weeks | 30–5,800 | 95.5% central range | 10 | Abbott | Blohm 1998 |
| 6 weeks–2 months | 16–2,000 | 95.5% central range | 10 | Abbott | Blohm 1998 |
| 2 months | 88–412 | 10th–90th percentile | 12 | In-house radioimmunoassay | Lahdenne 1991 |
| 4 months | 16–127 | 10th–90th percentile | 11 | In-house radioimmunoassay | Lahdenne 1991 |
| 6 months | 11–67 | 10th–90th percentile | 10 | In-house radioimmunoassay | Lahdenne 1991 |
| > 8 months | 5–27 | 10th–90th percentile | 11 | In-house radioimmunoassay | Lahdenne 1991 |
| 1 year | 4–17 | 10th–90th percentile | 10 | In-house radioimmunoassay | Lahdenne 1991 |
| 1 year, girls | 0.2–41 (Beckman Access); 1.8–38 (Roche E170) | 95% central range | 72; 67 | Two immunoassays | La'ulu 2011 |
| 1 year, boys | 1–17 (Beckman Access); 1.4–21 (Roche E170) | 95% central range | 65; 64 | Two immunoassays | La'ulu 2011 |
| 2 years | 0.6–12 (Beckman Access); 1.2–15 (Roche E170) | 95% central range | 134; 131 | Two immunoassays | La'ulu 2011 |
| Day 180 to day 720 | Up to 87; mean 8 | 95.5% interval | — | — | Blohm 1998, Abstract |

**Preterm infants run higher and fall more slowly** (same table). Examples: birth 31,300–799,800
(Blohm, 95.5% central range, n = 4); 4 months 75–621, 6 months 22–170, 1 year 5–33 (Lahdenne,
10th–90th percentile).

**The intervals disagree by up to an order of magnitude at the same age** (compare the two
statistics at 1 year). Ferraro calls the variability striking up to 6 months of age (aop p. 7). No
validated threshold exists for infants under 4 months (Group VII pathway, §8 item 7, from Ferraro).

### 4B. CSF AFP, infants (Coakley 2005, Abstract)

| Corrected age | Median | 5th–95th centile |
|---|---|---|
| −69 to 31 days | 61 kIU/L | 2–889 kIU/L |
| 32 to 110 days | 1.2 kIU/L | 0.1–12.5 kIU/L |
| Over 2 months | — | all < 3 kIU/L |

Plasma AFP runs about 20 times CSF AFP in newborns sampled within 24 hours of birth (Ferraro aop
p. 10, citing Coakley 2005). No CSF reference values for older children and no CSF β-hCG reference
values were found.

---

## 5. Verdict per marker

### Brain

- **Serum AFP: can decide a code without tissue — the category "malignant NGGCT", not a
  histotype.** SIOP (> 25 ng/mL) and COG (> 10 ng/mL) diagnose malignant NGGCT on markers without
  biopsy (Calaminus 2017; Goldman 2015; Fangusaro 2019). SIOP 96 accepted that AFP-secreting teratomas
  entered this category (Calaminus 2017, Methods). A raised AFP does not name yolk sac tumour: a yolk
  sac component was found in 19 of 37 AFP-raised patients (Calaminus 2017), every immature teratoma
  raised AFP (Takami 2023), and the PPV of AFP ≥ 10 ng/mL for any malignant non-germinomatous
  component was 57.7% (Takami 2022, Table 2).
- **CSF AFP: can decide a code without tissue — the same category, on the same thresholds.** Serum
  detects AFP more often than CSF (Takami 2023). In infants, CSF AFP is physiologically high until a
  corrected age of about 2 months (Coakley 2005).
- **Serum β-hCG: supports a histology report only, below about 3,300 IU/L; can decide a code without
  tissue above about 6,300 IU/L (choriocarcinoma component).** SIOP and COG treat > 50 or > 100 IU/L
  as malignant NGGCT, but pure germinomas reach 3,267.5 IU/L (Takami 2023), the PPV of ≥ 100 IU/L for
  a malignant non-germinomatous component was 53.3% (Takami 2022), and of 21 patients with β-hCG
  raised alone only 4 had choriocarcinoma on histology (Calaminus 2017). The upper threshold rests on
  one series with few choriocarcinomas (Takami 2023). The registrar decides between the protocol
  convention and the histology series.
- **CSF β-hCG: as serum β-hCG.** CSF detects β-hCG more often than serum (Takami 2023).
- **Normal markers decide nothing.** One marker-negative resected tumour held embryonal carcinoma
  (Takami 2022, p. 4); at least 3.4% of marker-negative bifocal tumours are NGGCT (Takami 2022,
  p. 2). SIOP CNS GCT II diagnosed germinoma on biopsy with markers below its thresholds (Calaminus
  2026, Methods). The COG ACNS1123 entry in Calaminus 2026 Table 2 admits "bifocal, pineal lesion +
  diabetes insipidus" germinoma at β-hCG ≤ 100 IU/L and does not state that histology was required
  for that group.

**On the Diagnostic Pathway's §2C rule "↑AFP → yolk sac (9071)".** The evidence above does not
support it: AFP rises in immature teratoma, and a marker-defined case is a non-germinomatous
category. ICD-O-3.2 holds the category as 9065/3, *Germ cell tumor, nonseminomatous*, and the Group X
data already carry 9065. This is an observation for the ruling, not a design.

### Ovary

- **AFP: supports a histology report only.** Specificity 98% and PPV 86% for any malignancy, but
  sensitivity 42% (Lawrence 2020). The ovarian tumour is resected, so tissue exists. One convention
  bears on the code: paediatric practice reads AFP > 1,000 ng/mL with teratoma histology as a yolk sac
  component (Pashankar 2022, p. 68, citing Mann 2008); adult guidance sets no threshold.
- **β-hCG: supports a histology report only.** PPV 32% for any malignancy (Lawrence 2020); pregnancy
  must be excluded (Schneider 2001).
- **LDH: no diagnostic value for coding.** Specificity 13% (Lawrence 2020).
- **CA-125: no diagnostic value for coding.** PPV 49% for any malignancy (Lawrence 2020); raised in
  juvenile granulosa cell tumour as well as epithelial tumours (Harris 2025).
- **HE4: no diagnostic value for coding.** No paediatric study found.
- **CEA: no diagnostic value for coding.** Sensitivity 5% (Lawrence 2020).
- **Inhibin A: supports a histology report only.** Specificity 97% for any malignancy (Lawrence
  2020); raised in 65% of juvenile granulosa cell tumours (Harris 2025). It does not separate juvenile
  from adult granulosa cell tumour.
- **Calcium: supports a histology report only.** Raised in 62% of hypercalcaemic-type small cell
  carcinomas (Young 1994), and raised by other tumours (van Heerden 2019; Hara 2022).

### Testis and sites outside the gonads

- **AFP: supports a histology report only.** MAKEI accepts a clinical diagnosis of a malignant germ
  cell tumour with a yolk sac or choriocarcinoma component on AFP above the age-related range
  (Schneider 2001), which is a category, not a histotype. In infants under 6 months and in neonates
  the values overlap with benign tumours (Ross 2002; Ferraro aop p. 9). The Prepubertal Testis Tumor
  Registry recommends excisional biopsy for every amenable tumour except one with AFP clearly
  increased for age; the abstract does not state the alternative (Ross 2002).
- **β-hCG: supports a histology report only.** Raised in 28% of adult seminomas (Dieckmann 2019).
- **LDH: no diagnostic value for coding.** Every published threshold is prognostic (Calaminus 2016,
  p. 122).

---

## 6. Gaps: no usable published cut-off

1. **HE4, ovary:** no paediatric cut-off or diagnostic study found.
2. **CEA, ovary:** only one cohort's laboratory threshold (3 ng/mL), with sensitivity 5%.
3. **Calcium, ovary:** no tumour-specific threshold; hypercalcaemia is defined by the laboratory
   range.
4. **Inhibin A, ovary:** only one cohort's laboratory threshold (80 pg/mL); no age-specific paediatric
   source extracted.
5. **CA-125, ovary:** only the adult-derived 35 U/mL; paediatric intervals exist in CALIPER
   (Bevilacqua 2014) but the table sits behind a paywall and was not read.
6. **LDH, every site:** no diagnostic cut-off; no age-specific paediatric reference values extracted.
7. **β-hCG, testis and sites outside the gonads:** no diagnostic cut-off for a choriocarcinoma
   component; only adult prognostic bands.
8. **AFP in infants under 4 months:** no validated threshold; published intervals vary by an order of
   magnitude.
9. **CSF β-hCG reference values in children:** no source found. CSF AFP reference values exist only
   for infants.
10. **The SIOP and COG CNS thresholds:** no published age limit confirmed; Ferraro's "older than
    4 years" is unverified against the trial text.
11. **Sources read at abstract level only:** Murray 2015 consensus (not used for any number), Renaud
    2019 (American Pediatric Surgical Association review), Schneider 2001, Blohm 1998, Wu 1981, Ross
    2002, Young 1994, Coakley 2005, Faure Conter 2018, Lin 2025, Bevilacqua 2014.

---

## 7. References

1. Bader D, Riskin A, Vafsi O, et al. Alpha-fetoprotein in the early neonatal period — a large study and review of the literature. *Clin Chim Acta.* 2004;349:15–23. Cited through Ferraro 2019, Table 3; not read.
2. Bayramoglu Z, et al. Pediatric and young adult ovarian masses: clinical approach, diagnostic evaluation, and management. *Front Pediatr.* 2025;13:1639582. DOI:10.3389/fped.2025.1639582. PMID 41000187. Full text (PMC12459912).
3. Bevilacqua V, et al. Pediatric population reference value distributions for cancer biomarkers and covariate-stratified reference intervals in the CALIPER cohort. *Clin Chem.* 2014;60:1532–42. DOI:10.1373/clinchem.2014.229799. PMID 25261558. Abstract only.
4. Blohm ME, Vesterling-Hörner D, Calaminus G, Göbel U. Alpha 1-fetoprotein (AFP) reference values in infants up to 2 years of age. *Pediatr Hematol Oncol.* 1998;15:135–42. DOI:10.3109/08880019809167228. PMID 9592840. Abstract; values also through Ferraro 2019, Table 3.
5. Calaminus G, Joffe J. Germ cell tumors in adolescents and young adults. *Prog Tumor Res.* 2016;43:115–127. DOI:10.1159/000447081. PMID 27595361. PDF on disk.
6. Calaminus G, Frappaz D, Kortmann RD, et al. Outcome of patients with intracranial non-germinomatous germ cell tumors — lessons from the SIOP-CNS-GCT-96 trial. *Neuro Oncol.* 2017;19:1661–1672. DOI:10.1093/neuonc/nox122. PMID 29048505. Full text (PMC5716085).
7. Calaminus G, et al. Final report of the SIOP-CNS-GCT II protocol for germinoma. *Neuro Oncol.* 2026;28:2234–2247. DOI:10.1093/neuonc/noag127. PMID 42234858. Full text (PMC13550669).
8. Coakley J, Kellie SJ, Nath C, Munas A, Cooke-Yarborough C. Interpretation of alpha-fetoprotein concentrations in cerebrospinal fluid of infants. *Ann Clin Biochem.* 2005;42:24–9. DOI:10.1258/0004563053026763. PMID 15802029. Abstract only.
9. Dieckmann KP, et al. Serum tumour markers in testicular germ cell tumours: frequencies of elevated levels and extents of marker elevation are significantly associated with clinical parameters and with response to treatment. *Biomed Res Int.* 2019;2019:5030349. DOI:10.1155/2019/5030349. PMID 31275973. Full text (PMC6558624).
10. Fangusaro J, Wu S, MacDonald S, et al. Phase II trial of response-based radiation therapy for patients with localized CNS nongerminomatous germ cell tumors: a Children's Oncology Group study. *J Clin Oncol.* 2019;37:3283–3290. DOI:10.1200/JCO.19.00701. PMID 31545689. Full text (PMC6900864).
11. Faure Conter C, Xia C, Gershenson D, et al. Ovarian yolk sac tumors; does age matter? *Int J Gynecol Cancer.* 2018;28:77–84. DOI:10.1097/IGC.0000000000001149. PMID 29194189. Abstract; age-band data through Ferraro 2019, aop p. 10.
12. Ferraro S, Panzeri A, Braga F, Panteghini M. Serum α-fetoprotein in pediatric oncology: not a children's tale. *Clin Chem Lab Med.* 2019;57(6):783–797. DOI:10.1515/cclm-2018-0803. PMID 30367785. PDF on disk (`Group 7 Papers/cclm-2018-0803.pdf`, ahead-of-print pagination 1–15; pages above are that PDF's).
13. Goldman S, et al. Phase II trial assessing the ability of neoadjuvant chemotherapy with or without second-look surgery to eliminate measurable disease for nongerminomatous germ cell tumors: a Children's Oncology Group study. *J Clin Oncol.* 2015;33:2464–71. DOI:10.1200/JCO.2014.59.5132. PMID 26101244. Full text (PMC4507465).
14. Hara N, et al. Hypercalcemia associated with dysgerminoma and elevation of calcitriol: a case report and review of the literature. *SAGE Open Med Case Rep.* 2022;10:2050313X211068562. DOI:10.1177/2050313X211068562. PMID 35070316. Title only.
15. Harris AK, et al. Ovarian juvenile granulosa cell tumor: a report from the International Ovarian and Testicular Stromal Tumor and International Pleuropulmonary Blastoma/DICER1 registries. *Cancer.* 2025;131:e35862. DOI:10.1002/cncr.35862. PMID 40267023. Full text (PMC12305807).
16. Hu M, et al. An update on the clinical diagnostic value of β-hCG and αFP for intracranial germ cell tumors. *Eur J Med Res.* 2016;21:10. DOI:10.1186/s40001-016-0204-2. PMID 26968839. Full text (PMC4788851).
17. Lahdenne P, Kuusela P, Siimes MA, et al. Biphasic reduction and concanavalin A binding properties of serum alpha-fetoprotein in preterm and term infants. *J Pediatr.* 1991;118:272–6. Cited through Ferraro 2019, Table 3; not read.
18. La'ulu SL, Rasmussen KJ, Roberts WL. Pediatric reference intervals for serum alpha-fetoprotein. *Clin Chim Acta.* 2011;412:1695–6. Cited through Ferraro 2019, Table 3; not read.
19. Lawrence AE, et al. Understanding the value of tumor markers in pediatric ovarian neoplasms. *J Pediatr Surg.* 2020;55:122–125. DOI:10.1016/j.jpedsurg.2019.09.062. PMID 31677824. Full text (PMC7181461).
20. Lin AM, et al. Use of ovarian tumor markers in prediction of malignancy risk in pediatric and adolescent patients. *J Surg Res.* 2025;315:839–846. DOI:10.1016/j.jss.2025.09.084. PMID 41187700. Abstract only.
21. Mann JR, Gray ES, Thornton C, et al. Mature and immature extracranial teratomas in children: the UK Children's Cancer Study Group experience. *J Clin Oncol.* 2008;26:3590–7. DOI:10.1200/JCO.2008.16.0622. PMID 18541896. Abstract; the 1,000 ng/mL convention through Pashankar 2022, p. 68.
22. Murray MJ, Bartels U, Nishikawa R, et al. Consensus on the management of intracranial germ-cell tumours. *Lancet Oncol.* 2015;16:e470–e477. DOI:10.1016/S1470-2045(15)00244-2. PMID 26370356. Abstract only; no number taken from it.
23. Pashankar F, Hanley K, Lockley M, et al. Addressing the diagnostic and therapeutic dilemmas of ovarian immature teratoma: report from a clinicopathologic consensus conference. *Eur J Cancer.* 2022;173:59–70. DOI:10.1016/j.ejca.2022.06.006. PMID 35863107. PDF on disk.
24. Phi JH. Sacrococcygeal teratoma: a tumor at the center of embryogenesis. *J Korean Neurosurg Soc.* 2021;64:406–413. DOI:10.3340/jkns.2021.0015. PMID 33906346. PDF on disk.
25. Renaud EJ, Sømme S, Islam S, et al. Ovarian masses in the child and adolescent: an American Pediatric Surgical Association Outcomes and Evidence-Based Practice Committee systematic review. *J Pediatr Surg.* 2019;54:369–377. DOI:10.1016/j.jpedsurg.2018.08.058. PMID 30220452. Abstract only; it states that tumour markers help estimate malignant potential and gives no cut-off in the abstract.
26. Ross JH, et al. Clinical behavior and a contemporary management algorithm for prepubertal testis tumors: a summary of the Prepubertal Testis Tumor Registry. *J Urol.* 2002;168:1675–8. DOI:10.1097/01.ju.0000030749.27823.f5. PMID 12352332. Abstract only.
27. Schneider DT, Calaminus G, Göbel U. Diagnostic value of alpha 1-fetoprotein and beta-human chorionic gonadotropin in infancy and childhood. *Pediatr Hematol Oncol.* 2001;18:11–26. DOI:10.1080/088800101750059828. PMID 11205836. Abstract only.
28. Takami H, et al. Roles of tumor markers in central nervous system germ cell tumors revisited with histopathology-proven cases in a large international cohort. *Cancers (Basel).* 2022;14:979. DOI:10.3390/cancers14040979. PMID 35205726. PDF on disk.
29. Takami H, et al. Impact of tumor markers on diagnosis, treatment and prognosis in CNS germ cell tumors: correlations with clinical practice and histopathology. *Brain Tumor Pathol.* 2023;40:124–132. DOI:10.1007/s10014-023-00460-x. PMID 36995447. Full text (PMC10113344).
30. Talerman A, Haije WG, Baggerman L. Serum alphafetoprotein (AFP) in patients with germ cell tumors of the gonads and extragonadal sites: correlation between endodermal sinus (yolk sac) tumor and raised serum AFP. *Cancer.* 1980. Cited through Ferraro 2019, Table 4; not read.
31. Tischkowitz M, et al. Small-cell carcinoma of the ovary, hypercalcemic type — genetics, new treatment targets, and current management guidelines. *Clin Cancer Res.* 2020;26:3908–3917. DOI:10.1158/1078-0432.CCR-19-3797. PMID 32156746. Full text (PMC7415570).
32. van Heerden J, Tjalma WA. The multidisciplinary approach to ovarian tumours in children and adolescents. *Eur J Obstet Gynecol Reprod Biol.* 2019;243:103–110. DOI:10.1016/j.ejogrb.2019.10.032. PMID 31683108. PDF on disk.
33. Wu JT, Book L, Sudar K. Serum alpha fetoprotein (AFP) levels in normal infants. *Pediatr Res.* 1981;15:50–2. DOI:10.1203/00006450-198101000-00012. PMID 6163129. Abstract only.
34. Young RH, et al. Small cell carcinoma of the ovary, hypercalcemic type: a clinicopathological analysis of 150 cases. *Am J Surg Pathol.* 1994;18:1102–16. DOI:10.1097/00000478-199411000-00004. PMID 7943531. Abstract only.

PubMed records were retrieved through the PubMed connector and NCBI E-utilities on 6 October 2026.
