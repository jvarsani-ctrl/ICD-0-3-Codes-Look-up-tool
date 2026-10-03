# Group 7 build contract — Hepatic Tumours

**Branch:** `claude/group-7-tumor-pathway-a88513`, cut from `main` at `cff8149`. Worktree
`.claude/worktrees/group-7-tumor-pathway-a88513`. `main` is untouched until the registrar merges.

**Written 2 October 2026, before any JSON was authored.** Every fact in §0 was verified the same day
against `ICCC-2017.sqlite`, `icdo32.sqlite`, the REDCap option file and the papers held in
`Group 7 Papers/`. An implementing agent reads this file, authors its task, and flags anything here
that turns out to be wrong. It does not re-derive a fact this file states.

Groups VIII and IX are being built at the same time by two other sessions. §7.1 records which shared
router rules each session owns.

> **Standing rule, inherited.** Advisory tools must never overstate evidence. Every defect that
> reached the browser in Groups III to VI made a case look better evidenced than it was. This group
> has two new instances: a small cell undifferentiated "hepatoblastoma" coded 8970 before anyone has
> looked at INI1 (§4.3), and a neonatal alpha-fetoprotein read as raised against an adult reference
> (§4.2).

---

## 0. Pre-context — everything an implementing agent needs

### 0.1 What this group is

ICCC-3 Group VII, **Hepatic tumours**. Five subgroups:

| Subgroup | Name | What lands here |
|---|---|---|
| **VIIa1** | Hepatoblastoma | `8970/3`, the dominant entity. `8975` is named by the range but has no behaviour-3 term (§0.3) |
| **VIIa2** | Rhabdoid hepatic tumour | `8963/3`, liver only |
| **VIIa3** | Embryonal sarcoma of liver | `8991/3`, liver only |
| **VIIb** | Hepatic carcinomas | `8160`–`8162` and `8170`–`8180` at any site, and the 8010–8573 carcinoma block at the liver only |
| **VIIc** | Unspecified malignant hepatic tumours | `8000/3`–`8005/3`, liver only |

Clinically the group is lopsided. Hepatoblastoma is the most common primary hepatic malignancy under
five; hepatocellular carcinoma is second at about 20% of paediatric hepatic malignancies; embryonal
sarcoma is 9–15%; malignant rhabdoid tumour is about 5% of primary liver malignancy in infants
(López-Terrada D, Stahlschmidt J, Pérez-Atayde AR. *Update on pediatric primary liver tumors.*
Virchows Archiv 2025;486(1):23–47, pp. 24, 27, 35, 36).

### 0.2 ★ The ICCC-3 definition, read off `ICCC-2017.sqlite`

`code_ranges` for `main_group = 'VII'`, verbatim:

| Subgroup | Source row | Morphology range | Topography | Behaviour |
|---|---|---|---|---|
| VIIa1 | 67 | `8970,8975` | `000-809` (any site) | **3** |
| VIIa2 | 68 | `8963` | `220,221` (**C22.0, C22.1 only**) | **3** |
| VIIa3 | 69 | `8991` | `220,221` (**C22.0, C22.1 only**) | **3** |
| VIIb | 70 | `8010-8041,8050-8075,8082,8120-8122,8140,8141,8143,8148,8155,8158,8190-8201,8202,8210,8211,8230,8231,8240,8241,8244-8246,8260-8264,8310,8320,8323,8401,8430,8440,8470,8480-8490,8503,8504,8510,8550,8560-8562,8570-8573,9013` | `220,221` | **3** |
| VIIb | 71 | `8160-8162,8170-8180` | `000-809` (any site) | **3** |
| VIIc | 72 | `8000-8005` | `220,221` | **3** |

Five consequences:

1. **Group VII declares behaviour 3 and nothing else.** Every benign, borderline, in-situ and
   metastatic reading in the REDCap list is outside the group by the recode's own definition. This
   is the mechanism that kept `9510/0` out of Group V and `8959/0` out of Group VI.
2. **`8963` and `8991` are liver-only.** `8963` elsewhere is VIa2 (C64.9) or IXd3; `8991` elsewhere
   is **IXa** (row 91, sites `000-218,239-809`). Both are dual-group codes and both need a router
   branch for C22 (§7).
3. **`8160`–`8162` and `8170`–`8180` are any-site.** A hepatocellular carcinoma or a
   cholangiocarcinoma is VIIb wherever it is recorded. No Group XI range carries `8170` at all. The
   router's `dual_group_rules["8170"]` default of Group XI has no basis in ICCC-2017 (§7.1).
4. **`8970` is any-site.** Hepatoblastoma keeps VIIa1 wherever it is recorded.
5. **No ICCC range carries `8576` Hepatoid adenocarcinoma in Group VII** (the VIIb carcinoma block
   stops at 8573). A hepatoid carcinoma is not a Group VII code.

### 0.3 ★ The code inventory — 92 usable codes, generated, not transcribed

```
python3 build/generate_group_inventory.py --group VII \
  --iccc "<vault>/ICCC-2017.sqlite" --icdo "<vault>/ICD coding/ICD-O-3.2/icdo32.sqlite"
```

> ICCC range entries 149 · distinct codes 149 · absent from ICD-O-3.2 at behaviour 3: 57 · usable 92

The 92 break down as **6** VIIc (8000–8005), **83** VIIb, **1** VIIa1 (8970), **1** VIIa2 (8963),
**1** VIIa3 (8991). "Absent" means absent at behaviour 3, not absent from ICD-O-3.2. Six of the 57
are REDCap options (§2A).

**The paediatric core is these codes.** Everything else in VIIb is an adult-type carcinoma reachable
by direct code entry, or by the "other carcinoma" node (§4), with no branch of its own:

| Code | ICD-O-3.2 preferred term at /3 | Subgroup | Reached by |
|---|---|---|---|
| `8970/3` | Hepatoblastoma, NOS | VIIa1 | imaging plus alpha-fetoprotein; histology; INI1 retained |
| `8963/3` | Rhabdoid tumor, NOS | VIIa2 | SMARCB1 or SMARCA4 loss |
| `8991/3` | Embryonal sarcoma | VIIa3 | histology alone |
| `8170/3` | Hepatocellular carcinoma, NOS | VIIb | histology |
| `8171/3` | Hepatocellular carcinoma, fibrolamellar | VIIb | histology ± molecular |
| `8172/3`–`8175/3` | scirrhous, spindle cell, clear cell, pleomorphic | VIIb | histology |
| `8180/3` | Combined hepatocellular carcinoma and cholangiocarcinoma | VIIb | histology |
| `8160/3`, `8162/3`, `8161/3`, `8470/3` | cholangiocarcinoma family | VIIb | histology |
| `8010/3`, `8020/3`, `8140/3`, `8240/3`, `8246/3`, `8023/3` | carcinoma fallbacks and the named paediatric "other" carcinomas | VIIb | histology |
| `8000/3`–`8005/3` | unspecified | VIIc | fallback |

### 0.4 ★★ The baseline document is insufficient, and the spine comes from the consensus classification

`docs/group_baseline_documents.md` assigns **Nagtegaal ID, et al.** *The 2019 WHO classification of
tumours of the digestive system.* Histopathology 2020;76(2):182–188 (PMC7003895), and flags it
provisional. **Retrieved and searched in full on 2 October 2026.** "Hepatoblastoma" appears zero
times. It prints no ICD-O code. Its liver content is four facts:

- several rarer hepatocellular carcinoma subtypes are now defined by morphomolecular features, with
  fibrolamellar carcinoma and its `DNAJB1::PRKACA` translocation the prime example;
- intrahepatic cholangiocarcinoma has a large duct and a small duct subtype;
- the definition of combined hepatocellular-cholangiocarcinoma is clearer, and cholangiolocellular
  carcinoma is now a subtype of small duct intrahepatic cholangiocarcinoma;
- "carcinoma in situ" is not recommended in the pancreatobiliary tree.

It is adequate for the adult VIIb carcinomas and silent on VIIa. **It cannot carry this group.**

**Pfister SM, et al.** *Cancer Discovery* 2022;12(2):331–355 (PMC9401511), the summary of the WHO
paediatric volume, was retrieved and searched the same day. It gives hepatoblastoma one paragraph
and states that the paediatric volume's taxonomy *"is based on the International Pediatric Tumor
Consensus Classification"* (its reference 93, López-Terrada 2014). Its Table 3, the solid-tumour
classification, is published as an image and is not machine-readable.

So the spine is the **International Pediatric Liver Tumors Consensus Classification**, held on disk
in two forms:

- **López-Terrada D, Alaggio R, de Dávila MT, et al.** *Towards an international pediatric liver tumor
  consensus classification.* Modern Pathology 2014;27(3):472–491 — the original;
- **López-Terrada D, Stahlschmidt J, Pérez-Atayde AR.** Virchows Archiv 2025;486(1):23–47 — Table 1,
  p. 24, reproduces the classification and states it *"has been incorporated in the recent WHO
  classification"*. This is the **latest document**, and under ruling 7 it governs where the two
  disagree.

Neither prints an ICD-O code. Codes come from `icdo32.sqlite` term by term (§2, §3). This finding
goes to the registrar (§11.1); the build proceeds on it.

**No registry-implications paper exists.** The MeSH sweep is recorded in
`Group 7 Papers/Group 7 — Registry-Implications MeSH Search Results.md`: 24 records, no candidate.

### 0.5 The entity list the tree is built against — López-Terrada 2025, Table 1, p. 24

Malignant hepatocellular: hepatoblastoma, epithelial variants (pure fetal with low mitotic activity;
fetal, mitotically active; embryonal; small cell undifferentiated, INI1+/−; pleomorphic; epithelial
mixed; cholangioblastic; macrotrabecular pattern); hepatocellular carcinoma; fibrolamellar
hepatocellular carcinoma; **hepatocellular malignant neoplasm, NOS**. Biliary: cholangiocarcinoma.
Mixed: combined hepatocellular cholangiocarcinoma. Mixed epithelial/mesenchymal or uncertain origin:
hepatoblastoma, mixed (epithelial and mesenchymal; teratoid); **malignant rhabdoid tumour, INI1−
and INI1+**; nested epithelial–stromal tumour. Malignant mesenchymal: embryonal sarcoma,
rhabdomyosarcoma, epithelioid hemangioendothelioma, angiosarcoma, synovial sarcoma, other (including
desmoplastic small round cell tumour, PNET, NUT carcinoma). Benign: hepatocellular adenoma, focal
nodular hyperplasia, macroregenerative nodules, bile duct adenoma, infantile and cavernous hemangioma,
mesenchymal hamartoma. Premalignant: dysplastic nodules, low and high grade. Metastatic: solid tumours,
leukaemias (AML M7). *(Corrected 3 October 2026 against the rendered table: the first draft listed
dysplastic nodules as benign.)*

### 0.6 ★★ Visser Tables 3 and 4 — what may be registered without tissue

Visser O, et al. *Frontiers in Oncology* 2023;13:1250549, transcribed in
`docs/references/visser-2023-key-points.md`:

| Table | Entity | Basis | Topography | Morphology |
|---|---|---|---|---|
| 3, pp. 04–05 | Hepatoblastoma | **2** | C22 | `8970/3` |
| 3, pp. 04–05 | Hepatocellular carcinoma | **2** | C22.0 | `8170/3` |
| 3, pp. 04–05 | Cholangiocarcinoma | **2** | C22.1, C24.0, C24.9 | `8160/3` |
| 4, p. 06 | Hepatocellular carcinoma, on alpha-fetoprotein | **4** | — | `8170/3` |

Three consequences:

1. **The imaging route is legitimate for `8970/3` at basis 2.** The Design Specification §3.6 adds
   the constellation: large hepatic mass, child under 3, raised alpha-fetoprotein.
2. **No specific Group VII code is emitted at basis 1.** A referral note that states a malignant liver
   tumour is likely records `8000/3` at basis 1, which Visser rule 5 allows; it never records `8970` or any
   other specific code. *(Amended during the build: the first draft said no terminal emits basis 1, which
   would drop a likely cancer from the registry on a note alone. Registrar item 7 in
   `docs/group_07_open_questions.md`.)*
3. **Everything else without pathology is `8000/3`** (rule 5), which at C22 is subgroup VIIc.

**Treating without tissue and registering without tissue are different decisions.** The consensus
says *"A diagnostic tumor biopsy should be mandatory for all patients regardless of their age and
serum alpha-feto protein level"* (López-Terrada 2014, p. 484), and Ng K, Mogul DB. *Pediatric liver
tumors.* Clinics in Liver Disease 2018;22(4):753–772, PDF p. 7, recommends biopsy for all patients
and advises against fine-needle aspiration. Neither forbids registering a case that was never
biopsied; Visser Table 3 governs that. The imaging node's hint says both.

*Superseded 3 October 2026 — the registrar ruled "go with Visser" (open question 4); both routes are
built at `hp_imaging_insufficient`, and the hepatoblastoma imaging route gains a seventh diversion for a
record that names hepatocellular carcinoma or cholangiocarcinoma. The paragraph below is the original
reasoning.*

**Not built: an HCC no-tissue route, or a cholangiocarcinoma one.** Visser licenses `8170/3` at basis 2
or 4 and `8160/3` at C22.1 at basis 2 without pathology. *(The cholangiocarcinoma row was added on
3 October 2026, when the table was checked against the rendered page; the first transcription
omitted it.)*
The Diagnostic Pathway reserves imaging sufficiency for hepatoblastoma. In an older child three
entities present as a liver mass with a raised alpha-fetoprotein: hepatoblastoma, hepatocellular
neoplasm NOS, which López-Terrada 2025 (pp. 29–30) describes in older children with very high
alpha-fetoprotein, and hepatocellular carcinoma, typical in about 80% (Ferraro, Table 4, p. 10).
Separating them is the histological classification the consensus asks for, and an imaging report
does not make it. An older child with a liver mass and no tissue is `8000/3`. Registrar item §11.4.

### 0.7 Engine facts that shape every node

**(a) `when` is string equality on a captured variable.** No operators.

**(b) `resolution_logic[]` is flat and first-match-wins**, and conditioned rules precede
unconditioned ones.

**(c) A `negative` marker requirement is satisfied by a marker that is off, never recorded, or
unreadable** (`app.js` `markerOff()`, line 1220: *"the three are the same evidence"*). So "INI1 not
lost" cannot be written as `negative: ["SMARCB1 (INI1) loss"]` — that rule fires on an untested
tumour and codes it hepatoblastoma, which is exactly the error Vokuhl 2016 documents. Retention is
its own positive marker, worded as Group III's `st_embryonal_family` words it: *"SMARCB1 (INI1)
performed and RETAINED with a valid internal control"*.

**(d) `imaging_pathway` requires every `imaging_features` box ticked**, every
`biochemical_questions[]` entry to match its `required_answer`, and **any one** diversion criterion
forces `insufficient_next_node`. `options[]` is never rendered on this node type.

**(e) `refer_group` must name a different group, carry no `morphology_code`, and put its
clerk-facing text in `reason`.** `coding_note` and `topography_routing_note` are never rendered.

**(f) `clinical_alert` is `null` everywhere** (ruling 9; `check_no_clinical_alerts()`). Warnings go
to `docs/clinical-warnings.md`.

### 0.8 Schema

`morphology_entries[]` field order is `build/build_database.py` `MORPHOLOGY_FIELDS`. Never null:
`morphology_code`, `morphology_name`, `behavior_code`. `confidence_ceiling` is not written (ruling of
16 September 2026). `diagnostic_tests_required` closed vocabulary: `Referral only`, `Histology`,
`Imaging`, `IHC`, `Flow cytometry`, `Cytogenetics/FISH`, `Molecular/PCR`, `ISH`. Flow cytometry is
irrelevant to this group.

`behaviour_exclusion` shape, as Groups IV and VI write it:

```json
{"icdo_code": "8975", "icdo_behaviour": "1", "icdo_term": "Calcifying nested stromal-epithelial tumor",
 "group_declares": "3", "reason": "<clerk-facing>", "registrar_decision_required": true}
```

Basis of diagnosis is the ENCR vocabulary; `ihc_counts_as: 7`, `methylation_counts_as: 8`.

---

## 1. The inventory is generated, never transcribed

`morphology_entries[]` comes from `build/generate_group07_entries.py`, which calls
`build/generate_group_inventory.py`'s `build_inventory()` for Group VII and applies an annotation
layer keyed by code. It never destroys a tree already on disk (the Group 6 generator's rule). Paths
come from `ICCC_DB` / `ICDO_DB` when set, so it runs from a worktree.

---

## 2. ★ Layer 1 conflict — REDCap and ICD-O-3.2 disagree in 42 places

Six options the group cannot emit (§2A), seven codes REDCap lacks (§2B), ten codes whose behaviour-3 string drifts (§2C) and nineteen option strings at a behaviour the group does not declare (§2D). The heading said 36 in the first draft; the sections sum to 42.

`ICD coding/RedCap Options/Group 7- Hepatic Tumors.md` offers 112 option strings on 91 codes against
the inventory's 92 codes. It gates the exact-string check, not the build. The REDCap-facing repair
package is `docs/group_07_layer1_repair.md`.

### 2A. Six codes the tool cannot emit at behaviour 3

| Code | REDCap label | ICD-O-3.2 |
|---|---|---|
| `8975` | Calcifying nested epithelial stromal tumor | **`8975/1` only**, "Calcifying nested stromal-epithelial tumor" — the word order differs too |
| `8148` | Glandular intraepithelial neoplasia, high grade | `8148/0` and `8148/2` only; "Biliary intraepithelial neoplasia, high grade" is a related term at `/2` |
| `8202` | Microcystic adenoma | `8202/0` only |
| `8264` | Papillomatosis, glandular | `8264/0` only, **[obs]**, as is "Biliary papillomatosis" |
| `8561` | Adenolymphoma | `8561/0` only |
| `9013` | Adenofibroma, NOS | `9013/0` only |

### 2B. Seven codes the inventory carries that REDCap does not offer

`8023/3` NUT-associated carcinoma, `8054/3` Warty carcinoma, and **`8171/3`–`8175/3`**, the five
ICD-O-3.2 hepatocellular carcinoma subtypes. Built under rulings 1–3 with `awaiting_layer1`, and
appended to `docs/codes-awaiting-redcap.md`. **`8171/3` is the one that matters**: the Diagnostic
Pathway's §4D and §8.3 say fibrolamellar carcinoma "has no distinct code in this code set". It does.
ICD-O-3.2 carries it and ICCC range 71 admits it.

### 2C. Ten codes whose behaviour-3 REDCap string drifts from ICD-O-3.2

| Code | REDCap string | ICD-O-3.2 at `/3` |
|---|---|---|
| `8970` | Hepatoblastoma | Hepatoblastoma, **NOS** (no term "Hepatoblastoma" at any level) |
| `8963` | Malignant rhabdoid tumor | synonym; preferred is Rhabdoid tumor, NOS |
| `8162` | Klatskin tumor | synonym carrying **[obs]**; preferred is Perihilar cholangiocarcinoma |
| `8170` | Hepatocellular carcinoma, NOS *(plus a transcription note pasted into the label)* | Hepatocellular carcinoma, NOS |
| `8158` | Endocrine tumor, functioning, NOS | a Related term under `8158/3` carrying **[obs]**; the preferred term is ACTH-producing tumor. ICD-O-3.2 has no `8158/1` row (corrected 2 October 2026; the first draft of this row said `8158/1`) |
| `8155` | Vipoma, malignant | no match at any level; ICD-O-3.2 has "Vipoma" |
| `8122` | Transitional cell carcinoma, spindle cell | synonym; preferred is Urothelial carcinoma, sarcomatoid |
| `8240` | Carcinoid tumor, NOS · Carcinoid tumor of uncertain malignant potential | synonym · no match; preferred is Neuroendocrine tumor, NOS |
| `8482` | Mucinous adenocarcinoma, endocervical type | synonym carrying **[obs]**; preferred is Mucinous carcinoma, gastric type |
| `8504` | Noninfiltrating intracystic carcinoma · Intracystic carcinoma, NOS | both are `8504/2` synonyms; `/3` is Encapsulated papillary carcinoma with invasion |

### 2D. Nineteen option strings sit at a behaviour the group does not declare

In situ (`/2`): 8010, 8050 (no match at any behaviour), 8052, 8070, 8120, 8140, 8201, 8210, 8230
(**[obs]**), 8261, 8263, 8470, 8503. Metastatic (`/6`): 8000, 8070, 8140, 8480 ("Pseudomyxoma
peritonei"), 8490. Uncertain primary (`/9`): 8000. Each shares its four digits with a valid `/3`
option, so a clerk can pick the right number with the wrong label. The repair package lists them.

### 2E. Extend the round-trip check, and step the exact-string check aside

As Groups III, IV and VI did: `check_icdo32_round_trip()` admits GROUP7, and
`check_redcap_exact_names()` steps aside for it. `morphology_name` is the ICD-O-3.2 preferred term at
behaviour 3. The REDCap strings move to the alias file, where every alias must resolve and none is
emitted as a name.

---

## 3. The code decisions this group forces

### 3.1 `8975` calcifying nested stromal-epithelial tumour is outside the group

ICD-O-3.2 has it at `/1` only. ICCC range 67 names the code at behaviour 3, where nothing exists.
López-Terrada 2025, p. 43, calls it *"a rare, low-grade hepatic neoplasm of uncertain lineage"*;
most patients have a benign course, some relapse or metastasise. The tree emits a
`behaviour_exclusion` on `8975/1` with `registrar_decision_required: true`. It does not recode to
`/3`. Registrar item §11.2.

*Ruled 3 October 2026 (open question 2).* The tumour is registered in Group VII. The histology step
offers it twice: with no statement of malignancy → `8975/1`; reported as malignant or with metastases →
`8975/3`, by the ICD-O matrix rule, which permits changing the behaviour digit to what the pathologist
reports. ICCC-2017 row 67 places `8975/3` in VIIa1. Both are entries outside the generated inventory,
anchored on Layer 1 by `check_group7_cnset()` (rule 10); the round-trip check admits `8975/3` through
`ICDO32_MATRIX_RULE`, which fails if icdo32.sqlite stops printing the term at `8975/1`.

### 3.2 `8171/3` fibrolamellar carcinoma is built, and is reached by morphology

Fibrolamellar carcinoma codes `8171/3`, never `8170/3`, on a report that diagnoses it. The molecular
node records the basis and catches the one case that moves off the code:

- `DNAJB1::PRKACA` fusion, or a PRKACA rearrangement by FISH, detected → `8171/3`, basis 8. Graham RP,
  et al. Modern Pathology 2015;28(6):822–829, p. 822: the fusion was found in all fibrolamellar
  carcinomas and in no other tumour type tested, and PRKACA FISH was negative in all six scirrhous
  hepatocellular carcinomas, the closest mimic.
- PRKAR1A loss, fusion absent → `8171/3`, basis **7** (revised from 8 after review: the loss is read by
  immunohistochemistry and is not specific to fibrolamellar carcinoma). Graham RP, et al. Hepatology 2018;68(4):1441–1447,
  PDF p. 2: Carney-complex fibrolamellar carcinomas carry PRKAR1A inactivation instead of the fusion.
- not tested → `8171/3`, basis 7. CK7 and CD68 positivity is the routine diagnosis (Lin CC, Yang HM.
  Archives of Pathology & Laboratory Medicine 2018;142(9):1141–1145, p. 1143).
- tested, neither found, and the report revises the diagnosis to hepatocellular carcinoma with
  fibrolamellar-like features → `8170/3`, basis 7. López-Terrada 2025, p. 29: fibrolamellar mimics
  with BAP1 inactivation lack the fusion.

`8171/3`–`8175/3` carry `awaiting_layer1`.

### 3.3 Hepatocellular neoplasm NOS has no ICD-O-3.2 code

López-Terrada 2025, pp. 29–31: a provisional consensus category for tumours with features between
hepatoblastoma and hepatocellular carcinoma, universally nuclear β-catenin positive, treated as
high-risk hepatoblastoma in the Paediatric Hepatic International Tumour Trial and not as
hepatocellular carcinoma. `icdo32.sqlite` has no term for it. A web search on 2 October 2026 found
no authoritative ICD-O assignment.

The two candidates are `8970/3` (VIIa1) and `8170/3` (VIIb), and the choice changes the ICCC
subgroup. **The tool does not choose.** It emits `8000/3`, VIIc at C22, with a `reason` naming both
candidates, the same shape as Group VI's unresolved SMARCB1 fork. Registrar item §11.3.


*Ruled 3 October 2026 (open question 3): `8970/3` Hepatoblastoma, NOS*, following López-Terrada 2025,
p. 30 — the PHITT trial treats these patients as high-risk hepatoblastoma, not as hepatocellular
carcinoma. The histology option emits `8970/3` at basis 7 with no `satisfies_tests` (8970 requires
Histology only). The aliases "Hepatocellular neoplasm NOS", "HCN-NOS" and, added the same day,
"Hepatocellular malignant neoplasm NOS" map to no code, so they are never listed under "Also called" on
an ordinary hepatoblastoma output; each search enters the tree, where the option records `8970/3`.

### 3.4 `8963` and `8991` need the liver confirmed

Both are C22-only in this group. `hp_document_inventory` captures `primary_site: "C22"` on every
option, and every rule or option that emits `8963` or `8991` carries a `when` on `primary_site` or
sits downstream of that capture. `check_group7_c22_only_codes` enforces it.

### 3.5 `8161/3` and `8470/3` both carry the biliary mucinous cystic carcinoma

ICD-O-3.2 carries "Bile duct cystadenocarcinoma" at `8161/3` and "Mucinous cystic neoplasm with an
associated invasive carcinoma" as a synonym at `8470/3`. Salles-Silva E, et al. Seminars in
Ultrasound, CT and MRI 2025;46(2):161–176, p. 165, records that the fifth edition renamed biliary
cystadenocarcinoma to mucinous cystic neoplasm. The tree follows the report's wording: the old term
to `8161/3`, the WHO 2019 term to `8470/3`. Registrar item §11.6.

### 3.6 `8162/3` Perihilar cholangiocarcinoma — REDCap's label is obsolete

The REDCap option reads "Klatskin tumor", which ICD-O-3.2 marks **[obs]**. The tool names the code
by its preferred term. Perihilar tumours sit at C24.0 more often than C22.1, and `8162` is any-site
in ICCC, so the code stays VIIb either way.

### 3.7 Metastases are not Group VII cases

López-Terrada 2025 Table 1 lists metastatic solid tumours and leukaemias (AML M7) among liver
masses. A deposit from a known primary is referred to that primary's group; an unknown primary goes
to Group XII, the Group III `pf_secondary_deposit` precedent.

---

## 4. Tree architecture

One tree, `g7_hepatic`, entry node `hp_document_inventory`. Node-id prefix `hp_`.

```
hp_document_inventory   (document_inventory)        captures primary_site C22 on every option
  ├── referral / clinical note only ................ hp_clinical_alias
  ├── imaging (± alpha-fetoprotein), no tissue ...... hp_imaging_pathway
  ├── histology report ............................. hp_histology
  ├── cytology only ................................ hp_cytology
  └── specimen inadequate .......................... hp_imaging_pathway

hp_clinical_alias        (clinical_alias)           never emits a code (basis 2 only)
hp_imaging_pathway       (imaging_pathway)          8970/3 at basis 2, or insufficient
hp_imaging_insufficient  (morphology_only)          8000/3 basis 2 · non-reportable · tissue now in file
hp_cytology              (morphology_only)          8970/3 or 8170/3 at basis 5 · 8000/3
hp_histology             (histology_subclassification)  the entity split
  ├── hepatoblastoma, no small cell undifferentiated predominance ..... 8970/3
  ├── small cell undifferentiated / blastemal predominance .............. hp_ini1
  ├── report diagnoses malignant rhabdoid tumour ......................... 8963/3
  ├── rhabdoid cells described, no rhabdoid tumour diagnosis ............. hp_ini1
  ├── hepatocellular carcinoma ..................................... hp_hcc_subtype
  ├── hepatocellular neoplasm NOS / features between HB and HCC ...... 8000/3, registrar
  ├── combined hepatocellular-cholangiocarcinoma ..................... 8180/3
  ├── cholangiocarcinoma or another biliary carcinoma ............... hp_biliary
  ├── undifferentiated embryonal sarcoma ............................ 8991/3
  ├── calcifying nested stromal-epithelial tumour ................... behaviour_exclusion 8975/1
  ├── other sarcoma ................................................. refer Group IX
  ├── germ cell tumour .............................................. refer Group X
  ├── lymphoma / leukaemia ........................................... refer Group II / I
  ├── metastasis .................................................... hp_secondary_deposit
  ├── other carcinoma ............................................... hp_other_carcinoma
  ├── benign lesion on a Group VII stem ............................. behaviour_exclusion
  ├── benign lesion, no Group VII stem .............................. non-reportable
  └── malignant, type not determined ................................ 8000/3
hp_ini1                  (ihc_checklist)            SMARCB1 / SMARCA4 loss → 8963 · small cell + retained → 8970 · rhabdoid cells + retained → 8000
hp_hcc_subtype           (histology_subclassification)  8170, 8172–8175; fibrolamellar → hp_flc_molecular
hp_flc_molecular         (cytogenetics_dropdown)    8171 (basis 8 or 7) · 8170 on revision
hp_biliary               (histology_subclassification)  8160, 8162, 8161, 8470
hp_other_carcinoma       (morphology_only)          8010, 8020, 8140, 8240, 8246, 8023
hp_secondary_deposit     (site_resolution)          refer to the primary's group
```

No `numeric_gate`: no code in this group forks on age once tissue exists. Age enters only the
imaging route, as diversion criteria.

### 4.1 Evidence does not monotonically refine the code

As in Group VI: a hepatoblastoma coded on imaging stays `8970/3` when histology arrives. Epithelial
subtype refines risk, not the code (López-Terrada 2025, pp. 24–25). **Unlike Group VI, the imaging
`8970` terminal does show histology as outstanding work**: the consensus asks for a biopsy in every
patient (López-Terrada 2014, p. 484), so suppressing the row would show the case as better worked up
than it is. *(The first draft of this paragraph said the opposite; the build chose the safer reading.)*
Use `satisfies_tests` deliberately.

The citation "Ferraro 2019" refers to *Clinical Chemistry and Laboratory Medicine* 2019;57(6):783–797;
the copy held is the 2018 ahead-of-print PDF, and its PDF page numbers are the ones cited.

### 4.2 The imaging route

`imaging_sufficient: true` on `8970/3` only. The constellation:

- **imaging feature:** a solid hepatic mass on ultrasound, CT or MRI, arising in the liver;
- **biochemical question:** serum alpha-fetoprotein reported raised above the laboratory's
  age-specific reference range — `required_answer: "yes"`.

**Diversion criteria — any one forces tissue:**

1. **Child is 3 years or older.** The Design Specification §3.6 window. Hepatoblastoma is generally
   diagnosed under 3 (López-Terrada 2025, p. 24); hepatocellular carcinoma, hepatocellular neoplasm
   NOS and embryonal sarcoma take over in older children.
2. **Infant younger than 6 months.** Ferraro S, et al. Clinical Chemistry and Laboratory Medicine
   2019;57(6):783–797, p. 7: the variability of reference intervals *"is striking for early age
   partitions at least up to 6 months of age"*, and abstract, p. 1: robust intervals cannot be defined
   in the first months of life. A "raised" value cannot be read reliably. The Diagnostic Pathway
   says 4 months; the paper supports 6. Registrar item §11.5 — *ruled 6 months, 3 October 2026.*
3. **Predominantly cystic or multicystic mass.** Mesenchymal hamartoma and undifferentiated embryonal
   sarcoma both present as solid-cystic masses (López-Terrada 2025, pp. 35, 39), and alpha-fetoprotein
   can be moderately raised in mesenchymal hamartoma (p. 39).
4. **The radiologist favours a vascular lesion, such as haemangioma.** Haemangioma is the most common
   vascular liver tumour of childhood (López-Terrada 2025, p. 33), and 14% carry a raised
   alpha-fetoprotein (Ferraro, Table 4, p. 10).
5. **Background chronic liver disease** — cirrhosis, biliary atresia, tyrosinaemia, progressive
   familial intrahepatic cholestasis, chronic hepatitis B. These are the conditions of paediatric
   hepatocellular carcinoma (López-Terrada 2025, Table 2, p. 29).
6. **A mass elsewhere is also described**, so the liver lesions may be metastases. Alpha-fetoprotein
   is raised in over 90% of yolk sac tumours (Ferraro, Table 4, p. 10).

A low alpha-fetoprotein never codes and never excludes: the biochemical box stays unticked, the case
falls to `hp_imaging_insufficient`, and the warning that 10% of hepatoblastomas present below
100 μg/L (Ferraro, p. 10) goes to `docs/clinical-warnings.md`.

`basis_of_diagnosis: 2` — Visser Table 3's row. Whether the alpha-fetoprotein raises it to 4 under
rule 1 is registrar item §11.4. Basis 2 is the lower claim.

### 4.3 ★ The INI1 fork — the group's signature

Vokuhl C, et al. *Small cell undifferentiated (SCUD) hepatoblastomas: all malignant rhabdoid
tumors?* Genes, Chromosomes & Cancer 2016;55(12):925–931, p. 925: of 23 tumours first diagnosed as
small cell undifferentiated hepatoblastoma or malignant rhabdoid tumour, all but one had lost INI1;
*"SCUD hepatoblastoma is not a hepatoblastoma but represents a malignant rhabdoid tumor of the
liver."* López-Terrada 2025, p. 25: the small cell undifferentiated pattern *"is not associated with
adverse prognosis as long as the cells retain INI1 expression"*, and p. 26: INI1 is intact in minor
small cell areas of an otherwise typical hepatoblastoma. P. 37: *"About 5% of MRTs have preserved
SMARCB1 but lack SMARCA4 expression."*

`hp_ini1` markers and rules, first match wins:

```
1. when {primary_site: [C22]}  positive [SMARCB1 (INI1) loss …]
                               negative [SMARCB1 (INI1) … RETAINED …]  → 8963/3, basis 7
2. when {primary_site: [C22]}  positive [SMARCA4 (BRG1) loss …]
                               negative [SMARCA4 (BRG1) … RETAINED …]  → 8963/3, basis 7
   INI1 retained AND SMARCA4 retained (workup complete):
3. small_cell_undifferentiated                                        → 8970/3
4. hepatoblastoma_with_rhabdoid_cells                                 → 8970/3
5. rhabdoid_cells (report names no type)                              → 8000/3, satisfies IHC
   INI1 retained, SMARCA4 not recorded (outstanding_tests [IHC], upgrade names SMARCA4):
6. small_cell_undifferentiated                                        → 8970/3
7. hepatoblastoma_with_rhabdoid_cells                                 → 8970/3
8. rhabdoid_cells                                                     → 8000/3
nos_fallback                                                           → 8000/3

*Revised after the independent review of 3 October 2026.* The first version had one option carrying
both "small cell undifferentiated" and "malignant rhabdoid tumour" into this step and an unconditioned
rule 3, so an INI1-retained malignant rhabdoid tumour — Vokuhl 2016, p. 927, case 17 — was coded
`8970` with "Workup: complete". A report that **diagnoses** malignant rhabdoid tumour is now coded
`8963/3` at the histology step, because rhabdoid tumour is still a histomorphological diagnosis
(López-Terrada 2014, p. 479).
```

**A small cell undifferentiated or rhabdoid tumour never reaches `8970` without a recorded INI1
result.** INI1 not done falls to `8000/3` (ruling 11: the nearest code that does not overstate).

*Two amendments from driving the step in the browser.* Rule 1 names the RETAINED marker as negative,
so once retention is recorded the flow does not ask for an INI1 loss that would contradict it; SMARCA4
is still asked. And `8000/3` requires Histology **and** IHC, so the INI1-not-done terminal shows IHC as
outstanding instead of "Workup: complete".

*Rebuilt on the registrar's ruling, 3 October 2026 (open question 18).* The first build coded rhabdoid
cells with INI1 retained as `8000/3` on one case: Vokuhl 2016, p. 927, case 17, which kept both INI1
and SMARCA4. The registrar asked for more evidence, since one case should not outweigh the typical
pattern. The current definition of a primary rhabdoid tumour of the liver "requires testing for loss
of SMARCB1 expression" (Trobaugh-Lotrario AD, et al. *Cancers* 2023;15(2):467, Discussion); a liver
tumour with rhabdoid or small cell features that keeps INI1 "should then be evaluated for BRG1
protein" (Fazlollahi L, et al. *Cancers* 2019;11(12):1992, §4.1.1); and of 20 tumours with features
suggesting rhabdoid tumour, the 7 that kept INI1 carried no INI1 mutation (Wu X, et al. *Pathology*
2008;40(7):664–670, p. 664). So:

- the histology step splits rhabdoid cells by what the report calls the tumour: hepatoblastoma with
  rhabdoid cells, or rhabdoid cells with no type named. The plain hepatoblastoma option now excludes
  any rhabdoid cells, so every tumour with rhabdoid cells passes through INI1;
- INI1 and SMARCA4 both retained: not a malignant rhabdoid tumour; the code follows the report;
- INI1 retained, SMARCA4 not recorded: the same code, with IHC outstanding. A code's required-test
  list is fixed per code, so this needed one group-agnostic engine field, `outstanding_tests[]`, the
  reverse of `satisfies_tests[]`, approved by the registrar the same day. `check_outstanding_tests()`
  validates it and rule 4(g) requires it on every such rule. Hepatoblastoma subtype is code-neutral

Pure fetal, crowded fetal, embryonal, pleomorphic, cholangioblastic, macrotrabecular, mixed
epithelial-mesenchymal and teratoid are all `8970/3` (López-Terrada 2025, pp. 24–25). The histology
option names them so the clerk can match the report; none forks.

### 4.5 Combined hepatocellular-cholangiocarcinoma is histology-defined

Brunt E, et al. Hepatology 2018;68(1):113–126, manuscript p. 2: *"diagnosis is based on routine
histopathology with hematoxylin and eosin (H&E); immunostains are supportive, but not essential"*;
collision tumours are excluded (p. 4). `8180/3` is a histology option, not an IHC rule.

### 4.6 Undifferentiated embryonal sarcoma needs no marker panel

López-Terrada 2025, p. 36: *"No helpful immunohistochemical markers exist for this tumor. The
diagnosis is based on the characteristic histopathology alone."* The 19q13 rearrangement settles
non-classical cases. This closes the Diagnostic Pathway's gap §8.1. `8991/3` is a histology option.

### 4.7 Hepatobiliary rhabdomyosarcoma is Group IX

López-Terrada 2025, p. 38: embryonal rhabdomyosarcoma of the biliary tree is *"the most common
malignant cause of obstructive jaundice in childhood"*, median age 3. It codes `8910/3` and its ICCC
group is IX. The histology node refers it, with angiosarcoma, epithelioid haemangioendothelioma,
synovial sarcoma, desmoplastic small round cell tumour and Kaposi sarcoma.

---

## 5. What the Diagnostic Pathway document gets wrong

The pathway is v1 of 9 June 2026. It predates the registrar's rulings of 4 September and the
ICD-O-3.2 table on disk.

1. **§4D, §7.5, §8.3 — "fibrolamellar has no distinct code".** `8171/3` exists and is in range (§3.2).
2. **§1, §4F, §7.6 — `8975` in a malignant subgroup at `/1`.** Group VII declares `/3` only. CNSET is
   a behaviour exclusion (§3.1).
3. **§4A, §4C and §5 — `clinical_alert` strings.** Ruling 9 removed warnings from the tool. They go
   to `docs/clinical-warnings.md`.
4. **§7.3 — "8963 has no hepatic destination in the master table".** True of the master file and of
   the router: the router has no C22 branch for `8963` (§7).
5. **§2D — fibrolamellar "CK7+, CD68+, HepPar-1+ triad" as code-defining IHC.** It is a diagnostic
   aid and changes no code; the molecular node handles the one revision that does.
6. **§8.1 — "no UESL IHC panel".** None exists, by the latest document (§4.6). Not a gap.
7. **§3 — "8963 at VIIa2 via the SCUD fork" without SMARCA4.** López-Terrada 2025 adds the SMARCA4
   route (§4.3).
8. **§2B — AFP "age < 4 months non-excludable".** Ferraro supports 6 months (§4.2).
9. **The alias instructions (14 May 2026) say `8170` is Group XI off the liver.** ICCC range 71 says
   VIIb at any site (§0.2).

---

## 6. The alias layer

`data/aliases/aliases_group_07.json`. The vocabulary a clerk meets:

- hepatoblastoma in every form: *hepatoblastoma*, *HB*, *HBL*, *embryonal hepatoma*, *pure fetal
  hepatoblastoma*, *crowded fetal*, *embryonal hepatoblastoma*, *mixed epithelial and mesenchymal
  hepatoblastoma*, *teratoid hepatoblastoma*, *cholangioblastic*, *macrotrabecular* → `8970`;
- *small cell undifferentiated hepatoblastoma*, *SCUD* → the INI1 fork, never straight to `8970`;
- *malignant rhabdoid tumour of the liver*, *MRT*, and the INI1 vocabulary (*INI1*, *SMARCB1*,
  *BAF47*, *SNF5*, *SMARCA4*, *BRG1*) → `8963`;
- *undifferentiated embryonal sarcoma*, *UESL*, *UES* → `8991`;
- *hepatocellular carcinoma*, *HCC*, *hepatoma* → `8170`; *fibrolamellar*, *FLC*, *FL-HCC* → `8171`;
- *hepatocellular neoplasm NOS*, *HCN-NOS*, *hepatocellular malignant neoplasm NOS* → `8000`, with
  the registrar note;
- *combined hepatocellular-cholangiocarcinoma*, *cHCC-CCA*, *hepatocholangiocarcinoma* → `8180`;
- *cholangiocarcinoma*, *intrahepatic cholangiocarcinoma*, *Klatskin tumour*, *perihilar
  cholangiocarcinoma*, *biliary cystadenocarcinoma*, *mucinous cystic neoplasm with invasive
  carcinoma*;
- *calcifying nested stromal-epithelial tumour*, *CNSET*, *nested epithelial stromal tumour*,
  *ossifying stromal-epithelial tumour* → `8975` behaviour exclusion, never a `/3` code;
- *liver cancer*, *liver tumour*, *hepatic malignancy* → `8000`.

REDCap's drifted strings (§2C) are aliases. Clerk-facing alias text is in `reason` / `hint`.

**Three constraints found driving the search, recorded so the next group does not relearn them.**
(1) The express-lane index reads the `alias` field only, never `also_known_as`, so every abbreviation a
clerk types — SCUD, UESL, CNSET, HCN-NOS, HCC, FLC, cHCC-CCA, Klatskin — is an alias of its own.
(2) An alias that exists in another group's file enters that group's tree if its number is lower,
because the engine takes `hit.groups[0]`; Group VII's primary aliases are therefore liver-specific
("Malignant rhabdoid tumour of the liver"), with the generic strings in `also_known_as`. (3) An alias
that maps to a code is listed under "Also called" on every output of that code, so the small cell
undifferentiated and hepatocellular neoplasm NOS aliases map to no code.

---

## 7. Shared-layer changes this build requires

### 7.1 `data/shared/presentation_router.json` — and who owns what

Agreed with the Group IX session on 2 October 2026 by cross-session message; the Group VIII session
was told the same day.

| Edit | Owner |
|---|---|
| `groups["7"]`: `built: true`, tree, `handoff` | Group 7 |
| `dual_group_rules["8963"]`: add C22.0/C22.1 → group 7 VIIa2, after the CNS and C64.9 branches | Group 7 |
| `dual_group_rules["8991"]`: new — C22.0/C22.1 → group 7 VIIa3, default group 9 IXa | Group 7 |
| `dual_group_rules["8000-8005"]`: add C22.0/C22.1 → group 7 VIIc, after the C64.9 branch | Group 7 (Group VIII may add C40/C41 → VIIIe to the same array; disjoint) |
| `dual_group_rules["8170"]`: default group 11 → group 7 VIIb | Group 7 |

### 7.2 `data/shared/topography_codes.json`

`C22.0` and `C22.1` already carry `candidate_groups: [7]`. No change. C23.9 and C24.x have no rows;
an extrahepatic cholangiocarcinoma is VIIb by ICCC but the router cannot reach Group VII from those
sites. Recorded in §11.7, not fixed here — it is a Group XI-adjacent edit outside this build.

### 7.3 Documents

1. `docs/group_07_layer1_repair.md` — the REDCap repair package for §2.
2. `docs/codes-awaiting-redcap.md` — append a Group 7 section for 8023, 8054, 8171–8175.
3. `docs/clinical-warnings.md` — a Group VII section in the established format.
4. `docs/group_baseline_documents.md` — record the §0.4 finding against row VII.
5. `docs/group_07_open_questions.md` — every item in §11, for the registrar's review.
6. `docs/group_07_build_report.md` — written last.

---

## 8. Validation rules this group adds

Each with a negative control, and, where the check reads free text, a positive probe on the most
plausible correct branch (Group 6 contract §8.1).

| # | Check | Catches |
|---|---|---|
| 1 | `check_group7_code_set` | an entry or terminal whose `(code, behaviour)` is not in the 92-code generated inventory — the fabricated-code guard |
| 2 | `check_group7_absent_codes` | any §2A code (8975, 8148, 8202, 8264, 8561, 9013) as a `morphology_code` or `nos_fallback` code |
| 3 | `check_group7_behaviour_declaration` | a `behaviour_exclusion` whose `group_declares` is not `"3"`, or whose code/behaviour pair is not real in `icdo32.sqlite` |
| 4 | `check_group7_ini1_fork` | a terminal emitting `8963` without a SMARCB1 or SMARCA4 loss marker; a rule emitting `8970` on SMARCB1 loss; a small cell undifferentiated or rhabdoid histology option that emits `8970` instead of routing to the INI1 node; **(e)** an alias on `8970` that names a small cell undifferentiated or rhabdoid tumour (added after the browser drive); **(f)** any route into the INI1 step that does not describe a small cell undifferentiated pattern but can reach the `8970` rule (added after review). Exemption **(a')**: an option whose label says the report diagnoses a malignant rhabdoid tumour may emit `8963` without a loss marker |
| 5 | `check_group7_c22_only_codes` | an `8963` or `8991` terminal reachable without `primary_site` C22 captured |
| 6 | `check_group7_no_tissue_codes` | a no-tissue or imaging terminal emitting anything but `8970/3` at basis 2 or `8000/3`; any basis 1 |
| 7 | `check_group7_imaging_constellation` | the imaging node without an alpha-fetoprotein question requiring "yes", or without the age diversions |
| 8 | `check_group7_fibrolamellar` | a fusion or PRKAR1A-positive branch emitting anything but `8171`; a fibrolamellar histology option emitting `8170` directly; **(d)** any branch of the fibrolamellar molecular step other than a revised diagnosis emitting anything but `8171` (added after the first negative-control pass) |
| 9 | `check_group7_router_c22` | the router failing to reach group 7 for 8963, 8991 and 8000–8005 at C22.0/C22.1, or 8170 at any site, keyed off `ICCC-2017.sqlite` |

Plus the round-trip extension (§2E) and `BEHAVIOUR_DECLARED_BY_GROUP[GROUP7] = {"3"}`.

Regression: Groups 1–6 byte-identical to `main`.

---

## 9. Proof before this group is called done

1. `python3 build/build_database.py` → **0 FAIL**, engine gate included.
2. `python3 build/induce_flow.py` → every rule has a witness.
3. Negative controls on all nine checks, recorded in `docs/validator_negative_controls.md`.
4. **Drive the changed branches in the browser**: the imaging route with a diversion, the INI1 fork
   both ways and untested, fibrolamellar with each molecular answer, hepatocellular neoplasm NOS, a
   Group IX referral, and the express lane.
5. Groups 1–6 byte-identical to `main`.

---

## 10. Tasks

| # | Task | Output | Status, 3 October 2026 |
|---|---|---|---|
| T1 | Generator and entries | `build/generate_group07_entries.py`, `group_07_dt.json` entries | done |
| T2 | Tree | `decision_trees[0]` in `group_07_dt.json`; `induce_flow.py` | done — 12 nodes |
| T3 | Aliases | `data/aliases/aliases_group_07.json` | done — 58 entries |
| T4 | Router | §7.1 | done |
| T5 | Validator | §8 checks in `build/build_database.py` | done — rules 1–9 |
| T6 | Documents | §7.3 items 1–5 | done |
| T7 | Verify | §9, negative controls | done — `build/negative_controls_group07.py`, 34 controls |
| T8 | Report | `docs/group_07_build_report.md` | done |

Build all parts, then verify once (standing rule 12).

---

## 11. What needs the registrar

**`docs/group_07_open_questions.md` is the current list** — seventeen items, including the eight below
and nine found during the build. The list here is the one written before any JSON.

1. **The baseline document.** Nagtegaal 2019 does not cover hepatoblastoma. The build uses the
   International Consensus Classification as written in López-Terrada 2014 and 2025 (§0.4). Confirm,
   or name another baseline.
2. **`8975/1` calcifying nested stromal-epithelial tumour.** Outside Group VII by ICD-O-3.2
   behaviour. Register it, and if so where?
3. **Hepatocellular neoplasm NOS.** No ICD-O-3.2 code. `8970/3` or `8170/3`? The tool emits `8000/3`
   until ruled (§3.3).
4. **No-tissue coding.** (a) Does alpha-fetoprotein raise the hepatoblastoma imaging basis from 2 to
   4 under Visser rule 1? (b) Should an older child with chronic liver disease, a liver mass and a
   raised alpha-fetoprotein be coded `8170/3` at basis 4 under Visser Table 4, rather than `8000/3`?
   (c) Visser Table 3 also allows cholangiocarcinoma, `8160/3`, at basis 2 at C22.1: build that route,
   or keep `8000/3`?
5. **Infant threshold for the imaging route**: 6 months (Ferraro) or 4 months (the pathway).
6. **`8161/3` versus `8470/3`** for biliary mucinous cystic carcinoma (§3.5).
7. **Extrahepatic biliary sites.** `8160`–`8162` are VIIb at any site, but C23.9 and C24.x have no
   topography row, so the router cannot reach Group VII from them.
8. **REDCap repairs** — §2 and `docs/group_07_layer1_repair.md`, including adding `8171`–`8175`.
