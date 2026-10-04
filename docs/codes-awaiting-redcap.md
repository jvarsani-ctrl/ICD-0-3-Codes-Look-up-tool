# Codes the tree can reach that REDCap cannot record

Registrar ruling 3, 4 Sep 2026: a code missing from the REDCap option list is still built into
the decision tree. It is reported, and it goes on this list. The tree is allowed to run ahead of
the dropdown; this file is what keeps the two reconcilable.

The build reads this file. A code carrying `awaiting_layer1` in `group_NN_dt.json` and **not**
listed here is a build failure, and so is a code listed here that no longer needs to be.

**`awaiting_layer1` is also what the output block reads**, so it has to mean one thing only: Layer 1
carries no option for this code. See *"Two banners, and the flag that separates them"* at the foot of
this file before adding or removing it anywhere.

Every term below is verified against the IARC ICD-O-3.2 morphology table, converted to
`ICD coding/ICD-O-3.2/icdo32.sqlite`. Where a code is also outside the ICCC-2017 ranges, adding
the REDCap option alone is not enough — `iccc_code` will fail to auto-populate and the case
falls out of the group. Both jobs have to be done together.

---

## Group 2 — open

### 9715/3 — Anaplastic large cell lymphoma, ALK negative

| | |
|---|---|
| ICD-O-3.2 | `9715/3` Preferred. `Breast implant-associated anaplastic large cell lymphoma` is a Related term on the same code |
| REDCap | **Absent** from `Group 2- Lymphomas And Reticuloendothelial Neoplasms.md` |
| ICCC-2017 | **Out of range.** IIb3 runs `9700-9702, 9705, 9708, 9709, 9714, 9716-9719, 9724-9726, 9767, 9768`. 9715 falls in the gap between 9714 and 9716 |
| Reached from | `g2_matureT` rule 4 (CD30 strong and homogeneous, ALK negative) and `g2cut_cd30_lpd` rule 4 (ALK negative with extracutaneous involvement) |
| Carried by until now | 9714, whose ICD-O-3.1 name spans both the ALK-positive and ALK-negative diseases |

**Paediatric.** ALCL is 10–30% of childhood non-Hodgkin lymphoma. Over 95% of paediatric cases
are ALK-positive, so this code is uncommon in children — but the cases it names exist, and
without it they are indistinguishable from ALK-positive disease in the registry.

**One thing not to do.** `Changes Made/Aug 2026 Changes to be made.md` proposed relabelling 9714
to "ALK-positive" at the same time. The IARC table does not support that: 9714/3 Preferred is
still `Anaplastic large cell lymphoma, T-cell and Null-cell type`, with `Anaplastic large cell
lymphoma, ALK positive` only a Related term. Add 9715; leave 9714's name alone.

### 9749/3 — Erdheim-Chester disease

| | |
|---|---|
| ICD-O-3.2 | `9749/3` Preferred, single row |
| REDCap | **Absent** |
| ICCC-2017 | **Out of range.** IId runs `9740-9742, 9750, 9751, 9754-9759`. 9749 sits below 9750 |
| Reached from | `g2hist_ecd` rules 1–5 |
| Carried by until now | 9750 Malignant histiocytosis, with a provisional naming Erdheim-Chester |

**Paediatric, but only just.** Mean age at diagnosis is 49.6 years. About twenty paediatric cases
are documented, mean age 9.6 years, the youngest 3.5 years, and there is a published proposal
that some paediatric CNS juvenile xanthogranuloma carrying BRAF V600E is paediatric ECD. Built
under ruling 1 — paediatric occurrence, not frequency, is the test.

### 9819/3 — B lymphoblastic leukemia/lymphoma, BCR-ABL1-like

| | |
|---|---|
| ICD-O-3.2 | `9819/3` Preferred. Note the hyphen form **BCR-ABL1-like**, not `BCR::ABL1-like` |
| REDCap | **Absent from the Group 2 list.** Already present in the Group 1 list |
| ICCC-2017 | **Out of range in both groups.** IIb1 runs `9811-9818, 9837`; Ia1 the same |
| Reached from | `g2_molecular`, on a documented Ph-like signature |
| Carried by until now | 9811 B lymphoblastic leukemia/lymphoma, NOS |

**Paediatric.** About 15% of childhood acute lymphoblastic leukaemia, rising through adolescence.
Ruling 4: one code, two groups. ICCC-2017 already separates 9811–9818 and 9837 by topography —
Group I at `C42.0` blood, `C42.1` marrow, `C42.3` RES; Group II everywhere else — so the
lymphoma presentation belongs here and the genetic layer sits beneath 9811.

---

## Group 1 — open

Group I already carries the seven ICD-O-3.2 additions its own review called for, and the REDCap
Group 1 option list has them. What none of them has is an **ICCC-2017 range**, so each one
classifies to nothing:

| Code | Name | Declared | ICCC-2017 range it needs |
|---|---|---|---|
| `9819/3` | B lymphoblastic leukemia/lymphoma, BCR-ABL1-like | Ia1 | `9811-9818, 9837` |
| `9877/3` | Acute myeloid leukemia with mutated NPM1 | Ib | the Ib list |
| `9878/3` | Acute myeloid leukemia with biallelic mutations of CEBPA | Ib | the Ib list |
| `9879/3` | Acute myeloid leukemia with mutated RUNX1 | Ib | the Ib list |
| `9912/3` | Acute myeloid leukemia with BCR-ABL1 | Ib | the Ib list |
| `9968/3` | Myeloid/lymphoid neoplasm with PCM1-JAK2 | Ie | the Ie list |
| `9993/3` | Myelodysplastic syndrome with ring sideroblasts and multilineage dysplasia | Id | the Id list |

These entries do **not** carry `awaiting_layer1`, because Layer 1's REDCap half already has
them. The gap is the classification table alone.

### A broken row in the ICCC-2017 table

`ICD coding/ICCC 2017 Cancer Classification.md`, the Group I row for subgroup **Ie**:

```
| Ie Unspecified and other specified leukemias | 9800,9801,9805-9C80.9,9860,9965-9967 |
```

`9805-9C80.9` is not a code range. `C80.9` is a topography code and belongs in the next column,
so the range's upper bound has been overwritten during transcription. Until it is repaired,
`9805` Acute biphenotypic leukemia and `9806`–`9809`, the mixed-phenotype acute leukaemia
series, classify to nothing and the build reports them as out-of-range.

**Do not guess the bound.** Repair it against the published ICCC-2017 tables.

---

## Remove from REDCap

### 9754 — retire the option

The Group 2 option list carries:

```
9751, 9751 - Langerhans cell histiocytosis, NOS
9754, 9754 - Langerhans cell histiocytosis, NOS (replaces former 9751/1 through 9754/3 codes)
```

Two faults in one row. 9754's real ICD-O-3 term is **Langerhans' cell histiocytosis,
disseminated**, and the parenthetical it carries is ICD-O-3's change note for **9751** — the code
that absorbed the old 9751/1–9754/3 series. The name and the note both belong to 9751.

ICD-O-3.2 does not list 9754 at all. It gives `9751/1 Langerhans cell histiocytosis, NOS` and
`9751/3 Langerhans cell histiocytosis, disseminated`. SEER records 9754/3 as effective 2001–2009
and reportable 1978–2009, directing 2010-forward cases to 9751/3.

ICCC-2017 still lists 9754 in the IId range because its recode tables carry historic codes so
pre-2010 records still classify. That is not a reason to keep it as a live dropdown option.

**Ruling 8, 4 Sep 2026: take the latest option.** The tool now emits 9751 with the behaviour
split and never 9754. Before removing the REDCap choice, query `i_morph` for existing records
using 9754 — removing a choice orphans any record already on it.

---

## Topography — one option string to repair

`ICD coding/RedCap Options/Topography Redcap.md`, line 185:

```
472, Peripheral nerves and autonomic nervous system of lower limband hip
```

A missing space: **limband**. The `Topography/C47 …md` source file has it right, so the fault
is in the REDCap option list alone. The tool carries the string verbatim in `redcap_label`,
because the clerk has to match what the dropdown actually says, and the clean form in `label`
for display.

---

## Group 3 — open

### 9476/3 — Medulloblastoma, SHH-activated and TP53-mutant

| | |
|---|---|
| ICD-O-3.2 | `9476/3` Preferred, and the code's only term |
| REDCap | **Absent** from `Group 3 - Cns And Miscellaneous Intracranial And Intraspinal Neoplasms.md`. Verified against the live `iii_morph` export of 2026-09-14: of the 87 usable Group III codes this is the **only** one with no option |
| ICCC-2017 | In range. IIIc1 Medulloblastomas, topography `C00.0-C80.9`, behaviour `0-1,3` |
| Reached from | `pf_mb_tp53` option 0 — TP53 **sequencing** performed and a pathogenic or likely pathogenic variant demonstrated |
| Carried by until now | Nothing. The previous pathway revision had the whole medulloblastoma block shifted by one and `9476` was absent from it altogether |

**Why the tree runs ahead of the dropdown here.** `9476/3` is the only route out of a
TP53-mutant SHH medulloblastoma, and it is the one medulloblastoma branch that changes
management: Orr 2020 recommends germline testing and genetic counselling in all SHH
medulloblastoma with large-cell/anaplastic histology or a mutant p53 IHC pattern,
particularly at ages 3–18. Registrar ruling 3 of 4 Sep 2026 allows the tree to carry a code
the option list lacks, provided it is reported here.

**What it must never be.** `9476/3` is reachable **only** from demonstrated TP53 sequencing.
p53 immunohistochemistry cannot establish TP53 status — TP53 has two IHC patterns, diffuse
overexpression and complete absence from null variants, and Ranade 2025 found p53
indeterminate in 11–13% of SHH medulloblastomas with four cases completely negative, which is
the null-variant signature. Every IHC-only route in the tree terminates at `9471/3`
(`Medulloblastoma, SHH activated, NOS`) instead. Adding the REDCap option does not change
that; it only gives the sequenced cases somewhere to go.

**To close it:** append `9476, 9476 - Medulloblastoma, SHH-activated and TP53-mutant` to
`iii_morph`, and add `9476` to the **IIIc1: Medulloblastomas** branch of both the
`iii_extended` and `iii_subgroup` formulas — it is the one code the repair package's F5 notes
neither formula currently handles. Full detail in
`ICD Look Up tool/Group 3 — Layer 1 Repair Package (REDCap iii_morph).md` §F5.

---

## Group 6 — open

Three ICD-O-3.2 additions the inventory carries and `Group 6 - Renal Tumors.md` does not offer.
Unlike the Group 3 entry above, none of these is reached from a decision-tree leaf — the Group 6
build contract §0.3 records that everything in VIb beyond the five-code paediatric core is an
adult-type carcinoma reachable only by direct code entry, with no branch built for it. All three
are appended for completeness, not because a case is expected to need them.

### 8023/3 — Nuclear protein in testis (NUT)-associated carcinoma

| | |
|---|---|
| ICD-O-3.2 | `8023/3` Preferred, an ICD-O-3.2 addition |
| REDCap | **Absent** from `Group 6 - Renal Tumors.md`. The list runs `8022`, `8030`, skipping `8023`–`8029` |
| ICCC-2017 | In range. VIb's carcinoma block runs `8010-8041,...` at `C64.9`, behaviour 3 |
| Reached from | Direct code entry only — no decision-tree leaf |
| Carried by until now | Nothing. `8020` Carcinoma, undifferentiated, NOS is the nearest offered option, but it is a different, less specific diagnosis |

**Paediatric relevance.** NUT carcinoma is an aggressive, molecularly defined carcinoma driven by
`NUTM1` rearrangement, described mainly in the midline thorax and head and neck; a primary renal
presentation is not established in the paediatric literature. Built under ruling 1 — paediatric
occurrence, not frequency, is the test — but occurrence at this site in a child has not been
reported.

### 8054/3 — Warty carcinoma

| | |
|---|---|
| ICD-O-3.2 | `8054/3` Preferred, an ICD-O-3.2 addition |
| REDCap | **Absent**. The list runs `8053`, `8060`, skipping `8054`–`8059` |
| ICCC-2017 | In range. VIb's carcinoma block runs `8050-8075,...` at `C64.9`, behaviour 3 |
| Reached from | Direct code entry only — no decision-tree leaf |
| Carried by until now | Nothing offered nearby names the same entity |

**Paediatric relevance.** Warty carcinoma is a human-papillomavirus-associated squamous carcinoma
pattern, described at genital and upper-aerodigestive sites in adults. It has no established
paediatric renal presentation.

### 8482/3 — Mucinous carcinoma, gastric type

| | |
|---|---|
| ICD-O-3.2 | `8482/3` Preferred, an ICD-O-3.2 addition |
| REDCap | **Absent**. The list runs `8481`, `8490`, skipping `8482`–`8489` |
| ICCC-2017 | In range. VIb's carcinoma block runs `8480-8490,...` at `C64.9`, behaviour 3 |
| Reached from | Direct code entry only — no decision-tree leaf |
| Carried by until now | `8480` Mucinous adenocarcinoma is the nearest offered option, but it is the generic form, not the gastric-type subtype this code names |

**Paediatric relevance.** Gastric-type mucinous carcinoma is described as a rare pattern in adult
renal and Müllerian mucinous neoplasms. No paediatric renal case is established.

**All three are adult-type carcinomas a paediatric renal registry is unlikely to meet.** The append
keeps the inventory-to-REDCap reconciliation complete, per the standing rule at the top of this
file, and is not a signal that any of the three is expected soon.

---

## Group 7 — open

Seven ICD-O-3.2 codes the inventory carries and `Group 7- Hepatic Tumors.md` does not offer
(Group 7 build contract §2B). Five are the ICD-O-3.2 hepatocellular carcinoma subtypes, and the
first of them is the one a paediatric liver registry will meet.

### 8171/3 — Hepatocellular carcinoma, fibrolamellar

| | |
|---|---|
| ICD-O-3.2 | `8171/3` Preferred |
| REDCap | **Absent.** The list carries `8170` and `8180` only from this range |
| ICCC-2017 | In range. VIIb row 71 runs `8160-8162,8170-8180` at any site, behaviour 3 |
| Reached from | `hp_histology` → hepatocellular carcinoma → fibrolamellar carcinoma → the molecular step |
| Carried by until now | `8170` Hepatocellular carcinoma, NOS. The Diagnostic Pathway (§4D, §8.3) states fibrolamellar carcinoma has no code of its own; ICD-O-3.2 gives it one |

**Paediatric relevance.** 15–25% of paediatric hepatocellular carcinoma in children over 5 years,
88% of them after 12 years (López-Terrada D, et al. Virchows Archiv 2025;486(1):23–47, p. 29).
Until REDCap carries the option, a fibrolamellar carcinoma cannot be recorded at its own code.

### 8172/3 — Hepatocellular carcinoma, scirrhous

| | |
|---|---|
| ICD-O-3.2 | `8172/3` Preferred; "Sclerosing hepatic carcinoma" a Synonym |
| REDCap | **Absent** |
| ICCC-2017 | In range, row 71 |
| Reached from | `hp_hcc_subtype` |
| Carried by until now | `8170` |

### 8173/3 — Hepatocellular carcinoma, spindle cell variant

| | |
|---|---|
| ICD-O-3.2 | `8173/3` Preferred; "Hepatocellular carcinoma, sarcomatoid" a Synonym |
| REDCap | **Absent** |
| ICCC-2017 | In range, row 71 |
| Reached from | `hp_hcc_subtype` |
| Carried by until now | `8170` |

### 8174/3 — Hepatocellular carcinoma, clear cell type

| | |
|---|---|
| ICD-O-3.2 | `8174/3` Preferred |
| REDCap | **Absent** |
| ICCC-2017 | In range, row 71 |
| Reached from | `hp_hcc_subtype` |
| Carried by until now | `8170` |

### 8175/3 — Hepatocellular carcinoma, pleomorphic type

| | |
|---|---|
| ICD-O-3.2 | `8175/3` Preferred |
| REDCap | **Absent** |
| ICCC-2017 | In range, row 71 |
| Reached from | `hp_hcc_subtype` |
| Carried by until now | `8170` |

**8172–8175 in children.** No paediatric frequency is given for these four subtypes in the Group 7
papers. They are built under ruling 2 (a code inside an ICCC range is added) and reached only when
a report names them.

### 8023/3 — Nuclear protein in testis (NUT)-associated carcinoma

| | |
|---|---|
| ICD-O-3.2 | `8023/3` Preferred |
| REDCap | **Absent.** The list runs `8022`, `8030` |
| ICCC-2017 | In range. VIIb row 70 runs `8010-8041,...` at C22.0/C22.1 |
| Reached from | `hp_other_carcinoma` |
| Carried by until now | Nothing. `8020` is a different, less specific diagnosis |

**Paediatric relevance.** NUT carcinoma is listed among the rare "other" malignant liver tumours
of childhood in the International Consensus Classification (López-Terrada 2025, Table 1, p. 24).

### 8054/3 — Warty carcinoma

| | |
|---|---|
| ICD-O-3.2 | `8054/3` Preferred |
| REDCap | **Absent.** The list runs `8052`, `8070` |
| ICCC-2017 | In range, row 70 |
| Reached from | Direct code entry only — no decision-tree leaf |
| Carried by until now | Nothing |

**Paediatric relevance.** None established at the liver. Appended so the inventory and the option
list stay reconcilable.

---

## Group 9 — open

Four ICD-O-3.2 codes the generated inventory carries and `Group 9- Soft Tissue And Other
Extraosseous Sarcomas.md` does not offer. All four are inside an ICCC-2017 Group IX range at
behaviour 3, so only the REDCap option is missing. Each has a decision-tree leaf (Group 9 build
contract §0.3, §1). Added 2 October 2026.

### 8714/3 — Perivascular epithelioid tumor, malignant

| | |
|---|---|
| ICD-O-3.2 | `8714/3` Preferred; synonym *PEComa, malignant* |
| REDCap | **Absent**. IXd11 lists `8710`–`8713`, skipping `8714` |
| ICCC-2017 | In range. IXd11 runs `8710-8714` at any site, behaviour 3 |
| Reached from | `st_uncertain`, "Perivascular epithelioid cell tumour (PEComa), malignant" |
| Carried by until now | Nothing |

**Paediatric relevance.** PEComa is in the paediatric soft tissue list of Pfister SM, et al.
*Cancer Discovery* 2022;12(2):331–355, Table 2.

### 9045/3 — Biphenotypic sinonasal sarcoma

| | |
|---|---|
| ICD-O-3.2 | `9045/3` Preferred, site reference C30.0, C31 |
| REDCap | **Absent**. IXd7 runs `9040`–`9044` |
| ICCC-2017 | In range. IXd11 lists `9045` at any site, behaviour 3 |
| Reached from | `st_uncertain`, "Biphenotypic sinonasal sarcoma" |
| Carried by until now | Nothing |

**Paediatric relevance.** An adult sinonasal sarcoma. Built because ICD-O-3.2 and ICCC-2017 both
carry it and the registry's upper age bound is unwritten (registrar questions G2).

### 9137/3 — Intimal sarcoma

| | |
|---|---|
| ICD-O-3.2 | `9137/3` Preferred |
| REDCap | **Absent**. IXd8 runs `9135`, `9136`, `9141`, skipping `9137` |
| ICCC-2017 | In range. IXd8 runs `9135-9138` at any site, behaviour 3 |
| Reached from | `st_uncertain`, "Intimal sarcoma" |
| Carried by until now | Nothing |

**Paediatric relevance.** An adult sarcoma of large vessels (Sbaraglia M, et al. *Pathologica*
2021;113(2):70–84, Table XI). Built for the same reason as `9045`.

### 9542/3 — Malignant peripheral nerve sheath tumor, epithelioid

| | |
|---|---|
| ICD-O-3.2 | `9542/3` Preferred; synonym *Epithelioid MPNST* |
| REDCap | **Absent**. IXb2 lists `9540`, `9541`, `9550`, skipping `9542` |
| ICCC-2017 | In range. IXb2 runs `9540-9571` at any site, behaviour 3 |
| Reached from | `st_nerve_sheath`, "Epithelioid malignant peripheral nerve sheath tumour" |
| Carried by until now | `9540` Malignant peripheral nerve sheath tumor, the less specific code |

**Paediatric relevance.** A subtype of malignant peripheral nerve sheath tumour, which Pfister 2022
names among the non-rhabdomyosarcoma soft tissue sarcomas most frequent in children.

## Also owed to Layer 1, from the same review

These are name faults in the Group 2 option list rather than missing codes, so they do not block
the tool, but they mislead whoever reads the dropdown.

| Code | The list says | ICD-O-3.2 Preferred | Consequence |
|---|---|---|---|
| `9766` | Angiocentric immunoproliferative lesion | `9766/1` Angiocentric immunoproliferative lesion · `9766/3` **Lymphomatoid granulomatosis, grade 3** | The list gives the `/1` term to a `/3` option. Grades 1 and 2 are Related terms on `9766/1` and are no longer malignant, so a 9766 case must now carry a grade |
| `9718` | Primary cutaneous CD30+ T-cell lymphoproliferative disorder | `9718/1` that term (Lymphomatoid papulosis a Synonym) · `9718/3` **Primary cutaneous anaplastic large cell lymphoma** | One option string for two diseases separated only by behaviour, and the distinction is clinical, not histological |
| `9725` | Hydroa vacciniforme-like lymphoma | `9725/1` **Hydroa vacciniforme-like lymphoproliferative disorder** (the list's term is a Synonym) | ICD-O-3.2 has no `9725/3`. The `/1` reassignment takes the case out of Group II unless a local rule says otherwise |
| `9740` | Mastocytoma, NOS | `9740/1` Mastocytoma, NOS · `9740/3` **Mast cell sarcoma** | One option for a harmless skin lump in a small child and for a sarcoma. Every ICCC Group II range is `/3`, so the benign lesion registers as sarcoma |
| `9728`, `9729` | Precursor B-cell / T-cell lymphoblastic lymphoma | **Absent from ICD-O-3.2.** Both are Synonyms on `9811/3` and `9837/3` respectively | Retired. Query `i_morph` before removing the choices |
| `9826` | Burkitt cell leukemia *(Group 1 list)* | **Absent from ICD-O-3.2.** A Synonym on `9687/3` | Retired, and it moves the case from Group I to Group II — a break in any trend series spanning the change |

`9727` needs no action: ICD-O-3.2 Preferred is `Precursor cell lymphoblastic lymphoma, NOS`,
exactly as the list has it. `Blastic plasmacytoid dendritic cell neoplasm` is a Related term on
the same code, which is worth knowing but is not a relabelling.

---

## Two banners, and the flag that separates them

**Found 22 September 2026, on the output block, driving the Group VI carcinoma branch in a browser.**

A clerk who reaches a code the dropdown cannot record has to be told so before they go looking
(ruling 3). The engine did that from `redcap_option_verified: false`, with one message:

> **Not yet a REDCap option** — This code has no option in the registry dropdown, so it cannot be
> selected yet.

**That flag does not carry that claim.** It means the option string was not verified to match. An
option can exist and still fail to match — because its label has drifted from the ICD-O-3.2 term —
and eleven codes across three built groups were in exactly that state, being told a row they can
select is not there:

| Group | Codes | What is actually true |
|---|---|---|
| I | `9898` | The option exists and names the sibling entity on the same four-digit code. |
| II | `9718`, `9725` | Options exist; the strings drifted. |
| VI | `8122`, `8130`, `8131`, `8155`, `8240`, `8311`, `8504`, `8963` | Options exist; eight strings drifted, two of them naming a different lesion. |

`8311` is the sharpest. Its option exists and reads *"Hypernephroid tumor"* — the obsolete `8311/1`
term, for a different lesion from the `8311/3` the tree emits. The clerk needs to be told the label
is wrong, **not** that the row is missing. Sending someone away from a row that is there is the same
class of defect as sending them to one that is not, and this project's rule is that the tool never
states more than the evidence supports — in either direction.

**`awaiting_layer1` is the signal that separates the two cases, and it separates them exactly.**
Checked across all six built groups: every entry flagged `redcap_option_verified: false` either
carries `awaiting_layer1` and has no option in Layer 1, or carries none and has one. Eighteen of
eighteen, no exceptions. So the engine now renders:

| Entry state | Banner |
|---|---|
| `awaiting_layer1` **present** | *Not yet a REDCap option* — the row does not exist; record against the nearest option and flag for re-coding. |
| `awaiting_layer1` **absent** | *The REDCap label for this code is out of date* — the row exists and the case can be entered; match on the four-digit code, not on the words, and flag the option for re-labelling. |

`check_redcap_banner_signal()` keeps the two in step. It keys off the option file itself — Layer 1,
never anything in the file being checked — and fails in **both** directions: `awaiting_layer1` set on
a code Layer 1 does carry, and unset on a code Layer 1 does not. Negative controls were run both
ways, adding the flag to `8311` and removing it from `8023`, with the data restored byte-identically
after each.

**Adding or removing `awaiting_layer1` changes what a clerk is told they can do.** It is not
bookkeeping for this file alone.
