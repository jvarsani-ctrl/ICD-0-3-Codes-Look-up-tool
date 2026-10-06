# Group X — for the registrar

**Written 4 October 2026, while the Group X build ran without you.** Every item here was built on
a stated default so the work could continue. None is hidden in the JSON: each default is one
branch, one alias or one router line, and the file named in each item says where. Argument for
each code decision: `docs/superpowers/specs/2026-10-04-group-10-germ-cell-code-decisions-design.md`
(D1–D22). Build plan: `docs/group_10_build_contract.md`.

Items are ordered by how much a wrong answer costs the registry.

---

## A. Decisions that change which code a case gets

### A1. Juvenile granulosa cell tumour is not registered (D11)

ICD-O-3.2 codes juvenile granulosa cell tumour `8622/1` at the ovary and `8622/0` at the testis.
ICCC-2017 Group X counts behaviour 3 only outside the central nervous system, so the commonest
sex cord–stromal tumour of childhood leaves the registry. The pathway (§3 Xe) and Pfister 2022
(p. 343) both name it as the paediatric entity.

**Built:** behaviour exclusion `8622/1` (ovary) and `8622/0` (testis), registrar decision
required. **If you rule otherwise:** there is no `8622/3` in ICD-O-3.2; registering it means a
registry-local rule, which item A10 covers.

**Also open: an ovarian granulosa cell tumour whose report does not state the type** (added
6 October 2026). ICD-O-3.2 prints no term for it; the adult type is `8620/3` (registered) and
the juvenile type `8622/1` (excluded). **Built:** the exclusion `8622/1`, registrar decision
required, so the tool does not register a cancer the report does not establish. **Question:**
keep that default, or register it as `8620/3`?

### A2. A germ cell tumour of unnamed type is `9064/3`, which prints as "Germinoma" (D2)

ICD-O-3.2 files *Germ cell tumor, NOS* under `9064/3`, whose preferred term is *Germinoma*.
Visser 2023 Table 4 (p. 06) uses `9064/3` for a germ cell tumour diagnosed on human chorionic
gonadotropin. The pathway proposed `9065/3`, *Germ cell tumor, nonseminomatous*, which asserts
the opposite of a germinoma.

**Built:** `9064/3`, with a reason on screen saying ICD-O-3.2 files *Germ cell tumor, NOS* under
that number. The output's name line still reads *Germinoma*.

### A3. Registration on tumour markers without tissue (D4)

**Built, following Visser 2023 Table 4:** imaging shows a tumour and alpha-fetoprotein is raised →
`9065/3`; human chorionic gonadotropin raised, alpha-fetoprotein not → `9064/3`; a uterine or
placental tumour after a pregnancy with human chorionic gonadotropin raised → `9100/3`. Basis 4.
A marker with no imaging is not registrable (rule 6); imaging alone is `8000/3`.

The pathway coded by dominant marker instead: alpha-fetoprotein → yolk sac tumour `9071/3`, very
high human chorionic gonadotropin → choriocarcinoma `9100/3`. That records a histology no one saw.
The tool reads the report's word "raised"; it does not apply Group III's numeric cut-offs.

### A4. Gonadoblastoma is not registered (D10)

ICD-O-3.2 has `9073/1` only, so ICCC-2017 subgroup Xc7 holds no usable code. **Built:**
gonadoblastoma alone → exclusion `9073/1`; with an invasive germ cell tumour → the invasive
tumour's code. The disorder-of-sex-development entry and karyotype questions are not built.

### A5. Testicular teratoma whose type the report does not state (D5)

WHO 2022 (Moch Table 3, pp. 464–465) splits testicular teratoma into prepubertal type `9084/0`
and postpubertal type `9080/3`. A report that says only "mature teratoma" or "teratoma" is coded
as written: `9080/0` or `9080/1`, both outside Group X. In an adolescent, a postpubertal-type
teratoma reported without its type leaves the registry. **Question:** keep coding as written, or
code a testicular teratoma of unstated type `9080/3` after puberty?

### A6. Placental site trophoblastic tumour — `9104/1` or `9104/3`? (D8)

ICD-O-3.2 prints `9104/1`. Moch 2022 Table 3 prints `9104/3`, "approved by the IARC/WHO Committee
for ICD-O at its meeting in February 2022". **Built:** exclusion `9104/1`, the same pattern as
Group VIII's chondrosarcoma grade 1 (Group VIII review A1).

### A7. Immature teratoma of the thymus (D5)

ICD-O-3.2 makes immature teratoma of the lung, thymus and thyroid `9080/1`. **Built:** the
extragonadal tree asks; the thymus answer is an exclusion, any other mediastinal site `9080/3`.

### A8. Mixed tumours are coded to ICD-O-3.2's specific term (D6, D7)

WHO 2022 codes every mixed germ cell tumour `9085/3` and polyembryoma `9085/3`. **Built:**
choriocarcinoma among the components → `9101/3`; embryonal carcinoma with teratoma only →
`9081/3`; the British terms to `9081`, `9082`, `9083` and `9102`; polyembryoma `9072/3`; anything
else `9085/3`.

### A9. The germinoma family by site (D1, D3)

Germinoma is `9064/3` (the pathway and the Alias Build Instructions said `9060`, which is
dysgerminoma). Each term is coded as written. Where only immunohistochemistry identifies the
family, the tree uses the site's term: ovary `9060/3`, testis `9061/3`, central nervous system and
other sites `9064/3`.

### A10. A `/1` tumour the pathologist calls malignant (D12)

The ICD-O matrix principle would allow a `/3` that ICD-O-3.2 does not print, for example
`8590/3`. Standing rule 1 forbids building an unprinted code. **Built:** the term as ICD-O-3.2
prints it. This is the same question as Group VIII review A1; one answer serves both groups.

### A11. Gonadal carcinomas on the tree (D14)

The ovary tree offers twelve carcinoma terms, including small cell carcinoma of the ovary,
hypercalcaemic type (`8044/3`), and excludes the borderline tumours and cystadenomas. The other
84 Xd codes are in the inventory and reachable by search only.

### A12. Three teratoma searches find nothing (D21)

"Also called" lists aliases by four-digit code, so an alias true of one behaviour shows on every
behaviour's output. Group X emits `9080` at `/0`, `/1` and `/3` and `9084` at `/0` and `/3`, so
neither carries an ICD-O-3.2 term as an alias, only the neutral "Teratoma". Searching "Mature
teratoma", "Immature teratoma" or "Dermoid" finds nothing; "Teratoma" finds them. An engine change
keying aliases by behaviour (`docs/TODO.md` §30) would lift this.

---

## B. Routing and reach

### B1. The central nervous system tree (D18) — decided 6 October 2026: option (a)

**Decided, 6 October 2026: option (a).** `topography_codes.json` lists Group 10 at the 24 lookup
codes ICCC-2017 places in Xa (C70.0–C72.9 and C75.1–C75.3; ranges 94–99, subgroups Xa1–Xa6), the
same 24 codes `groups["10"].tree_routing` sends to `g10_cns`. C75.1 lists Groups 3, 10 and 11; the
other 23 list Groups 3 and 10. The "Mass / swelling (solid tumour)" presentation lists Group 3.

What the front door does now. `app.js` narrows the presentation's list by the site's list, and
takes the site's list when the two share no group. Run over every presentation, every answer to
its origin or compartment question and every lookup code, the candidate list changes at these 25
codes and at no other:

- At the 24 sites, every presentation except "Organ-functional sign" offers Group III and Group X,
  and the clerk chooses by the pathology report. "Organ-functional sign" lists Group 3 and not
  Group 10, so it still goes to Group III alone.
- At C75.1 *Pituitary gland*, "Mass / swelling" offered Groups III and XI and now offers Groups III
  and X: Group XI, which is not built, leaves that one picker. "Incidental imaging finding", "Not
  sure / mixed presentation", "Lymphadenopathy" and "Cutaneous / mucosal lesion" offer Groups III,
  X and XI.
- At C80.9 *Unknown primary site* (`route_by_morphology`), "Mass / swelling" lists Group 3 with the
  others. No organ-system row offers C80.9, so the guided front door does not record it.

Driven on 6 October 2026: Mass / swelling, soft tissue, Pineal gland offers Group III and Group X,
and Group X's histology answer "Germinoma" records `9064/3` Xa1. "Germinoma" searched at the
pineal enters `g10_cns` and records the same code; before the decision it stopped with "The term
and the site point to different groups". At the cerebellum, Group III's posterior fossa tree
starts as before. Organ-functional sign at the pineal enters Group III's midline tree directly.

**Decided 6 October 2026: five generic search terms are left out of Group X.** Before the decision: Group X's
aliases include "Neoplasm, malignant", "Tumor cells, malignant" and "Malignant tumor, small cell
type", "giant cell type" and "spindle cell type" (`8000`–`8004`), because the ovary and testis
trees emit them (Xe, ICCC-2017 range 117, sites 569 and 620–629). Group III holds the same five
strings. Searched at any of the 24 sites, each used to enter Group III. Each now stops with "The
site does not decide the group", and the screen says Group III and Group X both occur at the site.
That is untrue for Group X: ICCC-2017 range 42 places `8000` at those sites in IIIf, and `g10_cns`
emits none of the five. Driven on 6 October 2026: "Neoplasm, malignant" at C71.6. The registrar
chose to leave the five strings out of Group X's aliases. At the brain sites they enter Group III
again. At the ovary and testis these searches stop for referral, and the guided route still codes
them. Group X keeps 123 aliases. Keying generic aliases to a site would need an alias field the
engine reads; it was not chosen.

**Still open: Group III's own gaps.** Group III stays byte-identical to `main` on this branch, so
these three are unchanged:

1. A biopsy-proven germinoma with normal markers has no route to Group X from `g3_midline`.
2. `pf_imaging_no_tissue` option 0 can never fire (`docs/TODO.md` §10).
3. `g3_supratentorial` has no germ cell route, though germinomas arise in the basal ganglia and
   third ventricle.

Group III refers to Group X in nine places, and a referral still ends the case: the clerk starts
a new case, and at a central nervous system site the front door now offers Group X.

**Before the decision.** Every central nervous system topography listed only Group III (and
Group XI at C75.1), so no clerk could reach `g10_cns`. Driven on 4 October 2026: "Germinoma"
searched at C71.0 stopped with "C71.0 … is not a site that group codes this term at", which was
untrue, since ICCC-2017 range 94 places germinoma at C71.0 in Xa1. The options put to you were:

- **(a)** — chosen. List Group 10 on the central nervous system topographies, and add Group 3 to
  "Mass / swelling", which listed 10 and not 3 and would otherwise have sent those sites straight
  to Group X.
- **(b)** Let a referral to a built group offer "continue in that group", carrying the topography —
  an `app.js` change that serves every group's referrals.
- **(c)** Add germ cell routes to Group III's trees, on a Group III branch, that end in a referral.

### B2. Front-door candidate groups outside the central nervous system (D19)

**Built:** Group 10 added to C38.1, C38.3 and C48.0; C62.0, C62.1 and C76.3 added to the lookup,
C76.3 with candidate groups 9 and 10. Added 6 October 2026: the uterus (C54.0–C54.9, C55.9;
candidate groups 9, 10 and 11) and the placenta (C58.9; Group 10), so a gestational
trophoblastic tumour is recorded at its own site (ICCC-2017 range 104, Xb5, sites 540–559 and
589). Groups IX and XI are listed there as at the cervix; neither group's tree was changed. Two questions: does the registry record a sacrococcygeal
tumour at C76.3 *Pelvis, NOS* (the pathway's choice; no Layer 1 file records the ICD-O-3 index
entry)? And should C76.3 also offer Group IV — which needs a Group IV tree to declare C76.3?

**Referrals from other sites also lead nowhere.** Groups VII, VIII and IX refer germ cell tumours
to Group X: Group VII "at any site including the liver", Group VIII from a bone deposit, Group IX
from soft tissue. The liver (C22.0, C22.1), bone (C40–C41) and soft tissue (C49.x) do not list
Group 10, so the front door never offers Group X there, and the search box stops with the same
untrue message that C71.0 gave before the B1 decision. Group VII's own alias "Yolk sac tumour of the liver" leads straight
into it. The same three options as B1 apply; option (a) here means listing Group 10 at the sites
where extragonadal germ cell tumours arise — the build added only C38.1, C38.3, C48.0 and C76.3.

### B3. The subgroup line (D20)

Each code shared across sites carries its gonadal subgroup (Xc) as its own and rules for the
central nervous system (Xa) and extragonadal (Xb) sites. Group X is always entered with a recorded
topography, so the line follows the site. REDCap computes `x_subgroup` itself from `x_morph` and
`topo_code`. Nothing to decide unless you want the tool to show no subgroup at all.

---

## C. Sources

### C1. The ovary has no baseline paper on disk (D22)

Höhn 2021, the assigned baseline, covers the vulva, vagina and cervix only (full text, PMC8494521,
read 4 October 2026). **Requested:** McCluggage WG, Singh N, Gilks CB. Histopathology
2022;80(5):762–778, doi:10.1111/his.14609 — not in PubMed Central. The ovary was built on
ICD-O-3.2 and Pfister 2022 Table 3.

### C2. Group 10 Papers

The literature file's references 3, 8, 16 and 19 (Al-Obaidy 2021, Wong 2023, Ronnett 2018, Jin
2024) are not on disk; no code decision depended on them. `Journal of Microscopy - 2024 -
Kallogjerovic …pdf` in `Group 10 Papers/` is unrelated to Group X (Pathway §8 item 6).

### C3. A correction made in `docs/group_baseline_documents.md`

It said "kidney" appears zero times in Pfister 2022's full text. The PDF on disk
(`Group 4 Papers/331.pdf`) has four hits, all in Table 3 (pp. 342–343); the zero came from the
PubMed Central text, where Table 3 is an image. The correction is applied on this branch, and the
Group VI conclusion stands. Nothing to decide.

---

## D. REDCap — listed, not acted on (standing rule 16)

`docs/group_10_layer1_repair.md` classifies every `x_morph` option. The three that matter most:
`9064` is offered as "Intratubular malignant germ cells", the in situ term, for the number whose
`/3` is *Germinoma*; `9100` reads "Hydatidiform mole, NOS", the benign term, for the number that
carries choriocarcinoma; `9086` reads "Label not found". `9102` is not offered at all. The
REDCap-side list is `docs/TODO.md` §27.

---

## E. Decided by the registrar, 6 October 2026 (hand review of fifteen cases)

The cases are in `docs/group_10_scenarios.md`.

### E1. "Choriocarcinoma" keeps one label on two screens

"Choriocarcinoma" appears in two places:
- on "What does the histology report call the tumour?", meaning a pure choriocarcinoma, `9100/3`;
- on "Which components does the report list?", meaning one component of a mixed tumour, `9101/3`.

**Decided:** keep both labels as they are. A clerk reaches the second screen only after saying
the tumour is mixed, and that screen's question says so.

Since 6 October 2026 the second "Choriocarcinoma" is a box on the component checklist and the label
of the option the checklist resolves to (E4). Both keep the one word.

### E2. Laboratory results are recorded as numbers on one screen

**Decided:**
- One "Laboratory results" screen with a row per test: the value as the report gives it, its unit,
  and "not in the file".
- The values appear on the result. The tool sets no cut-offs and does not interpret the values. No
  value chooses a code; the no-tissue routes keep coding on the report's own word "raised".
- Changed for the brain the same day (E6): from 24 months the brain marker route reads the numbers
  against the SIOP cut-offs, and its laboratory screen is kept for younger patients.
- The screen is a new question type in the engine. It was handed to the "ICD Overall fixes"
  session on 6 October 2026.
- Once the engine supports it, this branch places the screen at the start of each Group X tree,
  before "What is in the file for this tumour?".

**Group X's list:**

| Test | Points to | Source |
|---|---|---|
| Alpha-fetoprotein | Yolk sac tumour, immature teratoma, embryonal carcinoma | van Heerden 2019, Table 4, p. 107; Rajpert-De Meyts 2015, p. 177 |
| Beta human chorionic gonadotropin | Choriocarcinoma, embryonal carcinoma, some dysgerminomas | van Heerden 2019, Table 4, p. 107; Rajpert-De Meyts 2015, p. 177 |
| Lactate dehydrogenase | Dysgerminoma; tumour bulk | van Heerden 2019, Table 4, p. 107; Rajpert-De Meyts 2015, p. 177 |
| CA-125 | Epithelial tumours | van Heerden 2019, Table 4, p. 107 |
| Human epididymis protein 4 | Malignant and borderline epithelial tumours | van Heerden 2019, Table 4, p. 107 |
| Carcinoembryonic antigen | Epithelial tumours | van Heerden 2019, p. 108 |
| Inhibin A | Granulosa cell tumour | van Heerden 2019, Table 4, p. 107 |
| Calcium | Sex cord–stromal tumours; small cell carcinoma of the ovary, hypercalcaemic type | van Heerden 2019, Table 4, p. 107 |

**Built, 6 October 2026, to the registrar's ruling of the same day:** the "Laboratory results"
screen (node type `lab_results`) follows the evidence checklist, and only when Lab Report is ticked.
The engine routes the screen by its own next step, so the gate carries it in its data. Each tier a Lab
Report can join has a copy, listed just before it, that requires Lab Report and goes to a laboratory
screen; the screen then goes on to the tier's own next question, and the tier itself now excludes Lab
Report. The marker tier always has Lab Report ticked, so it goes through the screen directly. The
imaging-only tier excludes Lab Report and has no screen. That is four screens per tree, one per
destination (`<tree>_labs_referral`, `_labs_markers`, `_labs_cytology`, `_labs_histology`), each with
the tree's own tests. With Lab Report unticked the routes are the ones the gate had before. The trees
and the router open on the evidence checklist, as before. No value chooses a code, and the values
print on the result. The rules are in `docs/evidence_documents/group_10.json`.

| Tree | Tests, in screen order | Units the clerk chooses from |
|---|---|---|
| Ovary | Alpha-fetoprotein (AFP) · Beta human chorionic gonadotropin (β-hCG) · Lactate dehydrogenase (LDH) · Cancer antigen 125 (CA-125) · Human epididymis protein 4 (HE4) · Carcinoembryonic antigen (CEA) · Inhibin A · Calcium | AFP ng/mL, µg/L, IU/mL, kU/L · β-hCG IU/L, mIU/mL · LDH U/L, IU/L · CA-125 U/mL, kU/L · HE4 pmol/L · CEA ng/mL, µg/L · Inhibin A pg/mL, ng/L · Calcium mmol/L, mg/dL |
| Testis | AFP · β-hCG · LDH | as for the ovary |
| Other sites, the uterus and placenta among them | AFP · β-hCG · LDH | as for the ovary |
| Brain and spinal cord | Serum alpha-fetoprotein (AFP) · Serum beta human chorionic gonadotropin (β-hCG) · Cerebrospinal fluid alpha-fetoprotein (AFP) · Cerebrospinal fluid beta human chorionic gonadotropin (β-hCG) | AFP and β-hCG as above |

Sources for the tests: van Heerden 2019, Table 4, p. 107, and p. 108 for carcinoembryonic antigen;
Rajpert-De Meyts 2015, p. 177; for the brain, the Group 10 Diagnostic Pathway §2C (Takami 2022).
Neither paper prints a unit. The unit lists are the registrar's closed lists. Tourne 2019 reports
human chorionic gonadotropin in IU/L (pp. 331, 335) and alpha-fetoprotein in ng/mL (p. 335), Buza 2022
beta human chorionic gonadotropin in mIU/mL (p. 206), and Coşkun 2023 CA-125 in U/mL and calcium in
mg/dL (pp. 112–113). The labels spell out cerebrospinal fluid and cancer antigen 125, as the tree's
other text does (standing rule 14).

### E3. Pineal germinoma belongs to Group X

ICCC-3 places germ cell codes 9060–9065, 9070–9072, 9080–9085, 9100 and 9101 at sites C70–C72
and C75.1–C75.3 in X(a) (SEER ICCC-3 recode table). The local ICCC-2017 table agrees: range 94,
Xa1. The route is open since 6 October 2026 (item B1): every presentation except "Organ-functional
sign" offers Group X at those sites, and a Group X term searched there enters the central
nervous system tree.

### E4. The components of a mixed tumour are ticked, not chosen

The mixed germ cell tumour step is two screens since 6 October 2026:

1. "Does the report call the tumour by one of these names?" Teratocarcinoma `9081/3`; malignant
   teratoma, undifferentiated or anaplastic `9082/3`; malignant teratoma, intermediate `9083/3`;
   malignant teratoma, trophoblastic `9102/3` (ovary and testis); germ cell tumour with a
   haematological malignancy `9086/3` (other sites); or "None of these: the report lists the
   components". A term the report uses wins, so it is asked first. The checklist cannot hold these
   as plain choices: on a first-match checklist every option carries a rule and only the boxes are
   drawn.
2. "Which components does the report list?" A box each for choriocarcinoma, embryonal carcinoma,
   yolk sac tumour (endodermal sinus tumour), teratoma (mature or immature), seminoma, germinoma or
   dysgerminoma, and another germ cell component such as polyembryoma. The first rule that fits, top
   down, is the code:

| Option | Rule | Code |
|---|---|---|
| Choriocarcinoma | choriocarcinoma ticked | `9101/3` |
| Embryonal carcinoma and teratoma only | both ticked, nothing else | `9081/3` |
| Teratoma and seminoma, germinoma or dysgerminoma | both ticked, no choriocarcinoma, not exactly embryonal carcinoma and teratoma | `9085/3` |
| Other combination, or none listed | any other set, an empty one included | `9085/3` |

Every code, label and destination is the one the single-choice list had. The data gate enumerates all
64 ticked sets: none is stranded, and each option is the first fit for at least one. "Another germ cell
component" exists so that embryonal carcinoma, teratoma and a third component of any kind, polyembryoma
among them, is not coded `9081/3`.

### E5. Recognition aids on the tumour-type lists

The histology, teratoma, sex cord–stromal and epithelial screens carry a one-sentence aid under the
option the clerk selects, then Confirm (70 aids across the four trees). Each aid is drawn from the
Pathway's §1 and §6 anchors or a Group 10 paper, and its source and page are in the comment beside it
in `build/group10_tree.py`. An aid helps a clerk recognise a report; the code stays the report's own
term.

Left without an aid:
- **No source on disk describes them:** Sertoli cell tumour and malignant Sertoli cell tumour; Leydig
  cell tumour and malignant Leydig cell tumour; steroid cell tumour and its malignant form; thecoma
  and malignant thecoma; sex cord tumour with annular tubules; microcystic or signet-ring stromal
  tumour; malignant struma ovarii; invasive mole; high-grade serous, endometrioid, clear cell,
  seromucinous and undifferentiated carcinoma; mucinous carcinoma; the four borderline tumours and
  the two cystadenomas.
- **The sources describe the tumour at another site:** every option on the testis's sex cord–stromal
  screen and the extragonadal "Another tumour type" screen (Lim and Oliva 2018 describe the ovary),
  and the epithelioid and placental site trophoblastic tumours of the testis (Buza 2022 describes the
  uterine tumours; the extragonadal tree carries both aids).
- **The aid would decide an open question:** teratoma of prepubertal or of postpubertal type, and the
  testicular teratoma whose type is not stated (A5). A description of the two types would invite the
  clerk to choose a type the report does not state.
- **The option names no tumour:** every "type not named", "type not stated", "not determined",
  "Another tumour type" and "Not a germ cell tumour" option, the sex cord–stromal and epithelial
  category options on the ovary's histology screen, and the teratoma-with-another-component routes.
- **Not in this change:** the gonadoblastoma screen, the cytology screen and the mixed tumour's
  named-term screen.

### E6. Brain tumour markers: the SIOP cut-offs decide "raised" (rulings of 6 October 2026)

Evidence: `docs/group_10_lab_marker_evidence.md` §1, §4 and §5. Each number below carries the source
that file gives for it.

**Ruling 1 — the brain reads the SIOP cut-offs in Group III and in Group X.** Alpha-fetoprotein
above 25 ng/mL and beta human chorionic gonadotropin (β-hCG) above 50 IU/L, in serum or in
cerebrospinal fluid, count as raised.
- SIOP CNS GCT 96 diagnosed a malignant non-germinomatous germ cell tumour without biopsy on
  alpha-fetoprotein > 25 ng/mL or β-hCG > 50 IU/L in serum or cerebrospinal fluid (Calaminus 2017,
  Methods and Results). SIOP CNS GCT II required alpha-fetoprotein < 25 ng/mL and β-hCG < 50 IU/L
  in serum and cerebrospinal fluid for germinoma (Calaminus 2026, Table 2 and Results).
- SIOP applies the serum cut-off to either compartment (Takami 2023, Results; Calaminus 2026,
  Results).
- The boundary is strict, as SIOP CNS GCT 96 prints it: a value equal to the cut-off is not raised.

**Ruling 2 — ovary.** Alpha-fetoprotein above 1,000 ng/mL with teratoma histology does not change the
code: the histology decides, and the value is only recorded on the laboratory screen. Paediatric
practice reads such a value as a yolk sac component (Pashankar 2022, p. 68, citing Mann 2008), and
adult guidance sets no threshold. No data change.

**Ruling 3 — the Diagnostic Pathway's §2C "raised AFP → yolk sac tumour (9071)" is not supported.**
Every immature teratoma in Takami 2023 raised alpha-fetoprotein (Results); a yolk sac component was
found in 19 of 37 alpha-fetoprotein-raised patients in SIOP CNS GCT 96 (Calaminus 2017, Results);
alpha-fetoprotein ≥ 10 ng/mL had a positive predictive value of 57.7% for any malignant
non-germinomatous component (Takami 2022, Table 2, p. 5). The tree keeps 9065/3, Germ cell tumor,
nonseminomatous, on the no-tissue route. The pathway file lives outside this repository and is not
edited here.

**Built in Group X (`build/group10_tree.py`, `brain_marker_nodes()`).** The brain tree's marker
tier (Imaging and Lab Report ticked, no tissue) now opens on an age question and up to six marker
screens, each a `numeric_gate`, instead of the laboratory screen:

| Age at diagnosis | What decides |
|---|---|
| 24 completed months or more | The numbers. Any value above its cut-off, in either compartment, is raised. Alpha-fetoprotein raised leads to 9065/3. β-hCG raised, with alpha-fetoprotein at or below 25 ng/mL in both compartments, leads to 9064/3. All four values at or below the cut-offs leads to the imaging question, as "Neither marker is raised" did. Each coded option still needs imaging that shows the tumour and a file that calls it a germ cell tumour (Visser 2023, Table 4) |
| Under 24 months, or not in the file | The laboratory screen records the values, then the report's own reading decides, as before this ruling |

- **Each number is typed once.** From 24 months the gates replace the laboratory screen; under 24
  months the gates are never asked. A gate asks only what can still change the code, as Group III's
  `md_gct_*` gates do, so a value after the deciding one is not asked. The trail records each typed
  value with the band it fell in. The laboratory block on the result is empty on the gate route.
- **A value not entered never counts as normal.** "Not raised" needs both compartments entered and
  at or below the cut-off. A value left empty, for any reason, sends the case to the report question.
- **The age boundary is 24 months.** It is the first age at which every published upper reference
  limit of serum alpha-fetoprotein in term infants is at or below 25 ng/mL: 12 and 15 ng/mL at
  2 years (La'ulu 2011). Before it the limits run above 25: 27 ng/mL after 8 months (Lahdenne 1991),
  41 and 38 ng/mL for girls at 1 year (La'ulu 2011), up to 87 ng/mL from day 180 to day 720 (Blohm
  1998). All from Ferraro 2019, Table 3, aop pp. 8–9. A β-hCG number does not decide under 24
  months either: the split between 9065/3 and 9064/3 needs the alpha-fetoprotein reading.
- **Units.** The screens ask ng/mL for alpha-fetoprotein and IU/L for β-hCG, SIOP's units. The hint
  says that µg/L is the same number as ng/mL and mIU/mL the same as IU/L (the evidence file's Units
  paragraph). No conversion is built: a value in kU/L or IU/mL is left empty and goes to the report
  question.
- **The escape "Uncertain subtype — still a malignancy"** on each gate falls back to 9064/3 (Germ
  cell tumor, NOS), the one Visser Table 4 code that names no type, as on the stain panel.
- **Proof:** `check_brain_marker_cutoffs` walks 324 combinations of age and the four values through
  the gates with the engine's own band rule. Ten negative controls in
  `build/negative_controls_group10.py` (R5-A to R5-J) move each cut-off, flip the boundary, read a
  missing value as normal, and run the tree at commit `689d610`, before the gates.

**Changed in Group III (`data/database/group_03_dt.json`).** The four `md_gct_*` gates read the SIOP
cut-offs; they read Hu 2016's, which separate any intracranial germ cell tumour from a non-germ-cell
lesion rather than germinoma from a non-germinomatous tumour (evidence file §1):

| Gate | Was | Now |
|---|---|---|
| `md_gct_afp_serum` | ≥ 25 ng/mL | > 25 ng/mL |
| `md_gct_afp_csf` | ≥ 3.8 ng/mL | > 25 ng/mL |
| `md_gct_hcg_csf` | ≥ 8.2 IU/L | > 50 IU/L |
| `md_gct_hcg_serum` | ≥ 2.5 IU/L | > 50 IU/L |

The four gates' hints and referral reasons, and the clerk-facing cut-offs on `pf_imaging_no_tissue`,
`pf_family_triage`, `un_imaging_only` and `un_imaging_incomplete`, now state the same numbers. No
routing changed. Seven negative controls in `build/negative_controls_group03.py`.

**Traced: a pineal mass, imaging only, β-hCG 20 IU/L.** Before the ruling the gate referred it to
Group X. Now it continues to the compartment question, the pineal route and the imaging-only node
`md_pineal_imaging_only`. That node asks whether alpha-fetoprotein and β-hCG "have been measured and
are not elevated" and diverts to tissue when either "is elevated, or was never measured"; it states
no number. With alpha-fetoprotein measured and not elevated, and no other diversion, the case codes
8000/1 (Neoplasm, uncertain whether benign or malignant) at basis 2. With alpha-fetoprotein never
measured, it goes to "tissue required" and, with no tissue, the same 8000/1 at basis 2.

**For the registrar:**
1. **β-hCG above 50 IU/L with alpha-fetoprotein not raised.** SIOP CNS GCT 96 reads it as a
   secreting, malignant non-germinomatous tumour (Calaminus 2017, Methods), which ICD-O-3.2 holds as
   9065/3. The tree keeps Visser 2023 Table 4's 9064/3. Not chosen; your decision.
2. **A raised value by the laboratory's range that is not raised by SIOP's** (β-hCG 5 to 50 IU/L,
   alpha-fetoprotein 10 to 25 ng/mL) in a complete set of four values now reaches the imaging
   question and, for a malignant tumour on imaging, Group III's 8000/3. Before the ruling the
   report's word "raised" led to 9064/3 or 9065/3. This follows ruling 1; COG would read
   alpha-fetoprotein above 10 ng/mL as raised (Goldman 2015; Fangusaro 2019).
3. **A value equal to the cut-off** (25 ng/mL, 50 IU/L) is not raised under SIOP CNS GCT 96, and
   SIOP CNS GCT II's "< 25" does not admit it to germinoma either.
4. **Age limit of the SIOP cut-offs.** Ferraro 2019 states they were reported for patients older
   than 4 years (aop p. 9); the evidence file did not confirm this against the trial text (§6 item
   10). The tool applies them from 24 months, the reference-table age.
5. **Cerebrospinal fluid alpha-fetoprotein in infants.** Coakley 2005 (abstract only) gives a 95th
   centile of 12.5 kIU/L, about 15 ng/mL at 25 ng/mL = 20.8 kU/L (Calaminus 2026), from a corrected
   age of 32 days, and all values under 3 kIU/L after 2 months. The tool asks chronological age
   and no prematurity, so no earlier boundary for cerebrospinal fluid is built.
6. **Preterm infants** run higher and fall more slowly (Lahdenne 1991, 1 year: 5–33 ng/mL); Table 3
   has no preterm values at 2 years.
7. **Group III has no age question.** An infant whose physiological serum alpha-fetoprotein exceeds
   25 ng/mL is referred to Group X, where the age question sends the case to the report question.
8. **`md_pineal_imaging_only` says "elevated" without a number**, in its question and in its
   diversion. A clerk may read β-hCG 20 IU/L as elevated against the laboratory's range there.
9. **The non-diagnostic cytology route into the marker question** still reads the report: its values
   are typed on the cytology laboratory screen, which no gate can read.

**For the engine session (not done here; `app.js` is unchanged):**
- A gate that reads a `lab_results` value, or a laboratory screen that stores into the case
  variables, would let the cytology route and the under-24-month route use the numbers without a
  second entry.
- A referral from Group III does not carry the typed marker values (`caseFacts()` keeps the case
  facts only), so a Group III marker case enters its values again in Group X.
- `numeric_gate` has no "given in another unit" answer: a value left empty for its unit shows as
  "not documented" in the trail.
- The "Uncertain subtype" escape asserts no basis of diagnosis; its result carries no basis row. The
  gates' fallback names basis 4 for the validator's rule 2 only.
