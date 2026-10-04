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

---

## B. Routing and reach

### B1. A central nervous system germ cell tumour can reach Group X only through the search box (D18)

Every central nervous system topography lists only Group III, so the front door never offers
Group X there. Group III refers to Group X in nine places, and a referral ends the case. Group
III also has four defects, left untouched because Group III must stay byte-identical to `main`:

1. A biopsy-proven germinoma with normal markers has no route to Group X from `g3_midline`.
2. `pf_imaging_no_tissue` option 0 can never fire (`docs/TODO.md` §10).
3. `g3_supratentorial` has no germ cell route, though germinomas arise in the basal ganglia and
   third ventricle.
4. The search box is the only way into `g10_cns`.

**Options:** (a) add Group 10 to the candidate groups of the midline central nervous system codes
(C75.1–C75.3, C71.5, C72.x) — this adds a choice to every Group III case at those sites; (b) let a
referral to a built group offer "continue in that group", carrying the topography — an `app.js`
change for every group; (c) keep search as the route, and add germ cell routes to Group III's
trees on a Group III branch.

### B2. Front-door candidate groups outside the central nervous system (D19)

**Built:** Group 10 added to C38.1, C38.3 and C48.0; C62.0, C62.1 and C76.3 added to the lookup,
C76.3 with candidate groups 9 and 10. Two questions: does the registry record a sacrococcygeal
tumour at C76.3 *Pelvis, NOS* (the pathway's choice; no Layer 1 file records the ICD-O-3 index
entry)? And should C76.3 also offer Group IV — which needs a Group IV tree to declare C76.3?

### B3. The subgroup line when no topography was captured (D20)

A case entered from the search box has no topography; the output shows the entry's default
subgroup, which is the gonadal one (Xc) for the 18 codes shared across sites. REDCap computes
`x_subgroup` itself from `x_morph` and `topo_code`.

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

### C3. A correction for `docs/group_baseline_documents.md`

It says "kidney" appears zero times in Pfister 2022's full text. The PDF on disk
(`Group 4 Papers/331.pdf`) has four hits, including a Kidney section in Table 3 (p. 342). The
conclusion about Group VI may still stand; the count does not.

---

## D. REDCap — listed, not acted on (standing rule 16)

`docs/group_10_layer1_repair.md` classifies every `x_morph` option. The three that matter most:
`9064` is offered as "Intratubular malignant germ cells", the in situ term, for the number whose
`/3` is *Germinoma*; `9100` reads "Hydatidiform mole, NOS", the benign term, for the number that
carries choriocarcinoma; `9086` reads "Label not found". `9102` is not offered at all. The
REDCap-side list is `docs/TODO.md` §27.
