# Group 6 build contract — Renal Tumours

**Branch:** `group-06-renal`, cut from `group-05-retinoblastoma` (which is itself unmerged).
`main` is untouched until the registrar merges.

**Written 22 September 2026, before any JSON was authored.** Everything in §0 was verified against
the two databases, the four IARC change documents and the baseline paper on the same day. An
implementing agent should not need to re-derive any of it, and should not re-read the source
documents to confirm a fact this section states — it should read this file, author its task, and
flag anything here that turns out to be wrong.

> **Standing rule, inherited.** Advisory tools must never overstate evidence. Every defect that
> reached the browser in Groups 3, 4 and 5 made a case look better evidenced than it was. That is
> the class of fault to test first, and this group has a new instance of it: see §0.5.

---

## 0. Pre-context — everything an implementing agent needs

### 0.1 What this group is

ICCC-3 Group VI, **Renal tumours**. Three subgroup families:

| Subgroup | Name | What actually lands here |
|---|---|---|
| **VIa1** | Nephroblastoma | `8959/3`, `8960/3` — Wilms tumour, the dominant entity |
| **VIa2** | Rhabdoid renal tumour | `8963/3` — kidney only |
| **VIa3** | Kidney sarcomas | `8964/3` — clear cell sarcoma of kidney |
| **VIb** | Renal carcinomas | the 8010–8573 carcinoma block at C64.9, plus `8311/3`, `8312/3`, `8316/3`–`8319/3` at any site |
| **VIc** | Unspecified malignant renal tumours | `8000/3`–`8005/3` at C64.9 |

Clinically the group is **small and lopsided**: Wilms tumour is roughly 90% of paediatric renal
cancer, clear cell sarcoma of the kidney about 5%, and everything else is rare. That lopsidedness
is why the research literature for the group is thin — not because the group is badly studied, but
because the system is small. The build reflects it: one dominant imaging-first route and a set of
narrow confirmatory routes.

### 0.2 ★ The ICCC-3 definition, read off `ICCC-2017.sqlite` — this decides most open questions

`code_ranges` for `main_group = 'VI'`, verbatim:

| Subgroup | Morphology range | Topography | Behaviour |
|---|---|---|---|
| VIa1 | `8959,8960` | `000-809` (any site) | **3** |
| VIa2 | `8963` | `649` (**C64.9 only**) | **3** |
| VIa3 | `8964-8967` | `000-809` (any site) | **3** |
| VIb | `8010-8041,8050-8075,8082,8120-8122,8130-8141,8143,8155,8190-8201,8210,8211,8221-8231,8240,8241,8244-8246,8260-8263,8290,8310,8320,8323,8325,8401,8430,8440,8480-8490,8504,8510,8550,8560-8562,8570-8573,9013` | `649` (**C64.9 only**) | **3** |
| VIb | `8311,8312,8316-8319,8361` | `000-809` (any site) | **3** |
| VIc | `8000-8005` | `649` (**C64.9 only**) | **3** |

Four consequences, each of which settles something the diagnostic pathway document leaves open or
gets wrong:

1. **Group VI declares behaviour 3 and nothing else.** Every benign and borderline renal entity is
   therefore outside the group *by the recode's own definition*, not by a scope decision anyone
   made. This is the same mechanism that kept `9510/0` out of Group V and `8683/0` out of Group IV.
2. **`8963` is C64.9-only.** The dual-group routing for rhabdoid tumour is not an annotation this
   build has to invent — it is in the recode. `8963` at a CNS site is Group III (via `9508`), at
   soft tissue Group IX (`IXd3`, whose declared topography `000-218,239-639,659-699,739-768,809`
   explicitly excludes `649`).
3. **There is no `C65.9` anywhere in Group VI.** Renal pelvis is `XIf10`, not Group VI. A urothelial
   carcinoma of the renal pelvis is **not a Group VI case**, and the diagnostic pathway document's
   §1 claim that "transitional/urothelial [sits] at C65.9" inside this group is wrong (§5.4).
4. **`8964` is any-site.** Clear cell sarcoma *of kidney* keeps subgroup VIa3 wherever it is
   recorded. Do not gate it on topography.

### 0.3 ★ The code inventory — 90 usable codes, generated, not transcribed

```
python3 build/generate_group_inventory.py --group VI --out /tmp/g6_inventory.json
```

> ICCC range entries 160 · distinct codes 160 · absent at the declared behaviour 70 · usable 90

**Do not transcribe the option file.** `morphology_entries[]` is generated from
`ICCC-2017.sqlite` joined to `icdo32.sqlite`, exactly as Groups 3, 4 and 5 were. The generator's
`codes_absent_from_icdo32` list means *absent at behaviour 3*, not absent from ICD-O-3.2 — the
same wording trap recorded in Group 5's metadata.

The 90 break down as: **6** VIc (8000–8005), **81** VIb, **2** VIa1 (8959, 8960), **1** VIa2
(8963), **1** VIa3 (8964).

**The paediatric core is five codes.** Everything else in VIb is an adult-type carcinoma that is
reachable by direct code entry and gets no decision-tree leaf:

| Code | ICD-O-3.2 preferred term | Subgroup |
|---|---|---|
| `8959/3` | Malignant cystic nephroma | VIa1 |
| `8960/3` | Nephroblastoma, NOS | VIa1 |
| `8963/3` | **Rhabdoid tumor, NOS** | VIa2 |
| `8964/3` | Clear cell sarcoma of kidney | VIa3 |
| `8510/3` | Medullary carcinoma, NOS | VIb |

plus the renal-carcinoma leaves `8312/3` (RCC NOS), `8311/3`, `8310/3`, `8317/3`, `8319/3`,
`8260/3`, `8316/3`, `8480/3`, and the VIc fallbacks `8000/3`–`8005/3`.

### 0.4 ★★ The baseline paper's Table 1 is this group's Hoogendijk — read it before authoring

**Moch H, Amin MB, Berney DM, et al. *The 2022 World Health Organization Classification of Tumours
of the Urinary System and Male Genital Organs — Part A: Renal, Penile, and Testicular Tumours.*
European Urology 2022;82(5):458–468.** DOI [10.1016/j.eururo.2022.06.016](https://doi.org/10.1016/j.eururo.2022.06.016) · PMID 35853783.

**Held on disk from 22 September 2026:** `Group 6 Papers/Moch-2022-WHO-urinary-male-genital-PartA.pdf`
— the CC BY 4.0 version of record, 14 pp., retrieved with the registrar's permission from the
Francis Crick Institute's figshare deposit after the Zurich and Bern repository copies proved to
sit behind bot checks. Downloaded, extracted and read in full; §10 records what it settles.

Its **Table 1, "ICD-O coding of tumours of the kidney"**, prints the ICD-O-3.2 code against every
WHO 2022 renal entity. That is precisely the artefact Hoogendijk 2022 Table 1 is for Group III, and
it is the reason this group does **not** need a separate registry-implications paper. A PubMed MeSH
sweep for one (recorded in `Group 6 Papers/Group 6 — Registry-Implications MeSH Search Results.md`)
found nothing, and nothing is needed.

**The codes that carry more than one WHO 2022 entity — the `entity_annotation` problem for this group:**

| ICD-O-3.2 | WHO 2022 entities sharing it |
|---|---|
| **`8311/3`** | Eosinophilic solid and cystic RCC · TFE3-rearranged RCC · TFEB-altered RCC · ELOC (formerly TCEB1)-mutated RCC · Fumarate hydratase–deficient RCC · Hereditary leiomyomatosis and RCC syndrome–associated RCC · Succinate dehydrogenase–deficient RCC — **seven** |
| **`8510/3`** | Medullary carcinoma NOS · SMARCB1-deficient medullary-like RCC · SMARCB1-deficient undifferentiated RCC NOS · SMARCB1-deficient dedifferentiated RCC of other specific subtypes — **four** |
| **`8316/3`** | Tubulocystic RCC · Acquired cystic disease–associated RCC — **two** |
| **`8960/1`** | Mesoblastic nephroma · classic CMN · cellular CMN · mixed CMN — four, all at behaviour 1, **all outside the group** |
| **`8959/0`** | Mixed epithelial and stromal tumour · adult cystic nephroma · paediatric cystic nephroma — three, all at behaviour 0, **all outside the group** |

### 0.5 ⚠️ The single most load-bearing correction in this build: `8311/3` is not what the option file says

The diagnostic pathway document's §4F and §7.6 state that the molecularly defined renal carcinomas
— TFE3-rearranged, TFEB-altered, ELOC-mutated, FH-deficient, SDH-deficient, ALK-rearranged —
"**all collapse to 8312 (RCC NOS)**" because "the registry code set has no distinct codes" for them,
and instruct the build to capture them as annotation only.

**That is wrong, and building on it would understate the registry's own code set.** ICD-O-3.2
created `8311/3` for exactly these tumours, and WHO 2022 Table 1 assigns five of the seven
molecularly defined carcinomas to it:

```
icdo32.sqlite, code4 = 8311
  8311/1  Preferred  Hypernephroid tumor                                          [obs]
  8311/3  Preferred  Hereditary leiomyomatosis and renal cell carcinoma (HLRCC)
                     syndrome-associated renal cell carcinoma
  8311/3  Related    MiT family translocation carcinoma
  8311/3  Related    Succinate dehydrogenase deficient renal cell carcinoma
```

`3.1 to 3.2 — New codes and their terms`, p. 5, lists `8311/3` among the new codes, with the
HLRCC preferred term and the SDH-deficient related term both new in 3.2.

So the correct handling is: **TFE3-rearranged, TFEB-altered, ELOC-mutated, FH-deficient,
HLRCC-associated and SDH-deficient RCC code `8311/3`, not `8312/3`.** ALK-rearranged RCC is the one
of the seven that WHO Table 1 also puts on `8311/3`. `8312/3` is for renal cell carcinoma that is
genuinely unclassified after workup, and the tool must not route a molecularly *defined* tumour to
the NOS code. Doing so would be the exact failure mode this project names: making a case look
**less** evidenced than it is, which is the mirror of overstating and is equally a defect, because
the registry then cannot count the entity it actually holds.

**Both directions are banned.** Do not emit `8311/3` on a molecular suspicion that the file does not
state; do not emit `8312/3` for a tumour the file names as one of the six.

**How much of the group this decides.** Cajaiba MM, et al. *Cancer* 2018;124(16):3381–3389, DOI
[10.1002/cncr.31578](https://doi.org/10.1002/cncr.31578) — on disk — classified 212 renal cell
carcinomas in children and young adults enrolled prospectively on Children's Oncology Group
protocol AREN03B2. Mapped onto ICD-O-3.2 by WHO 2022 Table 1:

| Subtype | Frequency | ICD-O-3.2 |
|---|---|---|
| MiT-family translocation renal cell carcinoma (TFE3 93.2%, TFEB 6.8%) | **41.5%** | `8311/3` |
| Papillary renal cell carcinoma | 16.5% | `8260/3` |
| Renal medullary carcinoma | 12.3% | `8510/3` |
| Chromophobe renal cell carcinoma | 6.6% | `8317/3` |
| ALK-rearranged renal cell carcinoma | 3.8% | `8311/3` |
| Clear cell renal cell carcinoma | 3.3% | `8310/3` |
| Fumarate hydratase-deficient renal cell carcinoma | 1.4% | `8311/3` |
| Succinate dehydrogenase-deficient renal cell carcinoma | 0.5% | `8311/3` |
| Unclassified | 7.5% | `8312/3` |

**`8311/3` carries 47.2% of paediatric renal cell carcinoma, and MiT-family translocation carcinoma
alone is the commonest subtype in this age group.** Routing them to `8312/3` as the diagnostic
pathway document instructs would record nearly half of this group's carcinomas as unclassified when
the file names the entity. That is not a technicality; it is the difference between a registry that
can count its translocation carcinomas and one that cannot.

### 0.6 ICD-O-3.2 changed this group materially — checked, not assumed

All four IARC 3.1→3.2 change documents were text-extracted and searched on 22 September 2026 for
every code in the Group VI ranges. Findings:

| Document | Group VI hits |
|---|---|
| *Deleted codes and their terms* (9 Oct 2020) | **`8965/0 Nephrogenic adenofibroma (C64.9) — Moved to 9013/0`**. The only deleted Group VI number. |
| *New codes and their terms* | `8023/3` NUT carcinoma · `8054/3` warty carcinoma · `8311/3` HLRCC-associated RCC (+ SDH-deficient RCC) · `8316/1` multilocular cystic renal neoplasm of low malignant potential · `8323/1` clear cell papillary RCC |
| *Terms that are changing behaviour* | `8504/3 → /2` (Intracystic carcinoma NOS) · `8155/1 → /3` (Vipoma NOS) · `8120/1 → /0` (Urothelial papilloma NOS) · `8240/1` deleted |
| *Summary of main changes* | `8323/1` clear cell papillary RCC is a new term |

**`8965` is the only genuinely retired number in the group.** The other ten codes the REDCap option
file offers but the inventory does not (§2) exist in ICD-O-3.2 at behaviour 0 or 1 and are out of
the group by behaviour, not by deletion. Applying the weaker test — "ICD-O-3.2 prints no usable
term, therefore remove" — is what wrongly removed `9430/3` and `9480/3` from Group III. The test is:
**a code leaves the decision tree only when no current WHO entity lives on its stem.**

### 0.7 ⚠️ `8959/3` has no WHO 2022 entity, and that is a registrar question, not a deletion

Moch 2022 Table 1 lists `8959` **twice, both below behaviour 3**:

```
Mixed epithelial and stromal renal tumours
  8959/0  Mixed epithelial and stromal tumour
  8959/0  Adult cystic nephroma
  8959/0  Paediatric cystic nephroma
...
Embryonal neoplasms of the kidney / Nephroblastic tumours
  8959/1  Cystic partially differentiated nephroblastoma
```

There is **no `8959/3` entity in WHO 2022**. ICD-O-3.2 still carries `8959/3 Malignant cystic
nephroma`, and ICCC-3 VIa1 still admits `8959` at behaviour 3, so the code is live in both of the
tool's own sources and must stay in the inventory. But the tool must not pretend a current WHO
entity stands behind it. See §3.2 for how the tree handles this and §11 for the registrar item.

**Corollary the pathway document gets wrong (§5.2):** it calls `8959` "the DICER1-associated cystic
variant" and says to code `8959` for it. WHO 2022 puts **paediatric cystic nephroma — the
DICER1 tumour — at `8959/0`, benign**. A DICER1 cystic nephroma is not a Group VI registration.

### 0.8 The two engine facts that shape every node in this group

**(a) `when` is string equality on a captured variable. There are no operators.**

```js
function whenValueOk(have, want) {
  if (Array.isArray(want)) return want.some(w => String(have) === String(w));
  return String(have) === String(want);
}
```

So the age-dependent fork (§4.3) **cannot** be written as `age >= 10`. Age must be captured as a
`numeric_gate`, whose `band_variable` stores the band's literal `range` string
(`app.js:2240–2241`), and downstream rules match that string:
`"when": {"age_band": [">=10"]}`.

**(b) `resolution_logic[]` is flat and first-match-wins, and the validator enforces that rules
carrying a `when` precede unconditioned ones.** A rule whose conditions are a subset of an earlier
rule's can never fire. The `8963` / `8510` fork is therefore written as *two conditioned rules
above one unconditioned rule*, not as a nested branch.

### 0.9 Schema, in one place

`morphology_entries[]` — every field present, `null` where it does not apply
(`build/build_database.py:100–120`):

```
morphology_code · morphology_name · iccc3_subgroup_id · iccc3_subgroup_name · who_version
behavior_code · diagnostic_tests_required · ihc_markers_required · ihc_markers_exclude
imaging_sufficient · imaging_features · nos_fallback_code · nos_fallback_name
clinical_alert · coding_note · code_neutral_molecular · redcap_value · primary_sites
topography_dependent · topography_routing_note
```

Never null: `morphology_code`, `morphology_name`, `behavior_code`.
`confidence_ceiling` is **removed from the engine** (registrar ruling, 16 Sep 2026) and is not
written by any group from Group 4 on. Do not author it.

`diagnostic_tests_required` closed vocabulary: `Referral only`, `Histology`, `Imaging`, `IHC`,
`Flow cytometry`, `Cytogenetics/FISH`, `Molecular/PCR`, `ISH`.
**Flow cytometry is irrelevant to this group. Do not use it.**

`node_type` closed vocabulary (`build/build_database.py:48–62`) — this group uses a subset and
invents nothing:

```
document_inventory · clinical_alias · morphology_only · imaging_pathway · ihc_checklist
cytogenetics_dropdown · molecular_freetext · histology_subclassification · site_resolution
numeric_gate
```

`clinical_presentation` and `site_capture` are **router-tier** and may never appear in a
`group_XX_dt.json`.

**NOS-fallback rule is by node type, not by step number.** Required on `ihc_checklist`,
`cytogenetics_dropdown`, `molecular_freetext`, `numeric_gate`. **Forbidden** on
`document_inventory`, `clinical_alias`, `morphology_only`, `imaging_pathway`,
`histology_subclassification`, `site_resolution`.

`behaviour_exclusion` (Group 4 extension) — the shape for a code the group cannot emit:

```json
{"icdo_code": "8959", "icdo_behaviour": "0", "icdo_term": "Benign cystic nephroma",
 "group_declares": "3", "reason": "<clerk-facing>", "registrar_decision_required": true}
```

`refer_group` — must name a different ICCC-3 group, carry **no** morphology code, and put its
clerk-facing text in `reason`. `coding_note` is **not rendered** and is author-facing only; the
same is true of `topography_routing_note`. Clerk-facing text goes in `reason`, `hint` or
`clinical_alert`.

### 0.10 Rules inherited unchanged, which this build does not reopen

- Basis of diagnosis is the ENCR vocabulary of Visser O, et al. *Frontiers in Oncology*
  2023;13:1250549 (in repo: `docs/references/Visser-2023-ENCR-basis-of-diagnosis.pdf`, key points
  in `docs/references/visser-2023-key-points.md`). Every terminal emits one.
- `ihc_counts_as: 7`, `methylation_counts_as: 8`.
- Rule 4, p. 03: *possible is not registrable*. A case where a non-malignant disorder could equally
  explain the findings is **not registered**, which is `non_reportable`, not `refer_group`.
- The tool codes to **ICD-O-3.2**, not ICD-O-4. No five-digit codes, no migration TODOs.
- CBTRUS groupings are not a code-currency source.
- No raw hex outside the `:root` token block.
- Cite the paper and the page, and write full forms — *clear cell sarcoma of the kidney*, not CCSK,
  in clerk-facing text.

### 0.11 ★★ Visser Table 3 — settled, and it licenses the imaging route at basis 2 only

The load-bearing claim of this entire group is that a renal mass may be **registered** without
tissue. That claim must rest on the European Network of Cancer Registries rules, not on the SIOP
protocol's willingness to *treat* without biopsy — treating without tissue and registering without
tissue are different decisions, and the diagnostic pathway document conflates them.

**It rests on Visser, and the row is already extracted in this repo.** Visser O, et al. *Frontiers
in Oncology* 2023;13:1250549, Table 3, pp. 04–05, transcribed in
`docs/references/visser-2023-key-points.md`:

| Entity | Basis | Topography | Morphology | Group |
|---|---|---|---|---|
| **Nephroblastoma** | **2** | **C64** | **`8960/3`** | **VI** |

The paper heads this row, with hepatoblastoma and retinoblastoma, *"Solid childhood cancers (age
<15 years)"*.

**Three things follow, and they are not negotiable:**

1. **The imaging-sufficient route is legitimate, and it is `8960/3` at C64 and nothing else.** No
   other Group VI code appears in Table 3 or Table 4.
2. **Basis 2, never basis 1.** Unlike retinoblastoma — which Table 3 gives as "1 or 2" and which is
   why Group V has a clinical-alias node that emits a code on wording alone — nephroblastoma is
   basis **2**: clinical investigation, which includes imaging. **No Group VI terminal may emit
   basis 1.** A referral letter saying "Wilms tumour", with no imaging in the file, does not
   register `8960/3`.
3. **Everything else without pathology is `8000/3`.** Visser rule 5: anything not in Table 3 or
   Table 4, diagnosed without pathology, is `8000/3` — unless a coding expert at the registry rules
   otherwise, which is the registrar's call and not the tool's. So a renal mass that fails the
   nephroblastoma imaging constellation, and has no tissue, is `8000/3` at C64.9, subgroup VIc. That
   is what VIc is for, and it is why §3.4's router fix matters: without it that case reaches
   Group XII instead.

---

## 1. The inventory is generated, never transcribed

`morphology_entries[]` comes from `build/generate_group_inventory.py --group VI`. The entry author's
work is the **annotation** — `coding_note`, `clinical_alert`, `diagnostic_tests_required`,
`imaging_sufficient`, `imaging_features`, `nos_fallback_*`, `topography_*` — not the code list.

Every `coding_note` states its provenance and its source with page or table. The house citation form
is full: *"Moch H, et al. European Urology 2022;82(5):458–468, Table 1"*, never *"Moch 2022"* alone
and never a bare number for a code.

---

## 2. ★ Layer 1 conflict — the REDCap option file and ICD-O-3.2 disagree in nineteen places

This is the largest Layer 1 divergence of any group built so far. It does **not** gate the build:
the tool generates from the databases and does not read the option file for its inventory. It gates
the **exact-string check**, which is keyed off Layer 1, and it produces
`docs/group_06_layer1_repair.md`.

`ICD coding/RedCap Options/Group 6 - Renal Tumors.md` offers 98 options against the inventory's 90.

### 2A. Eleven options the tool cannot emit

| Option | REDCap label | Why it cannot be emitted |
|---|---|---|
| `8965` | Nephrogenic adenofibroma | **Deleted in ICD-O-3.2** — moved to `9013/0`. Zero rows in `icdo32.sqlite`. |
| `8966` | Renomedullary interstitial cell tumor | `/0` only. WHO 2022 Table 1: `8966/0`. |
| `8967` | Ossifying renal tumor | `/0` only. WHO 2022 Table 1: `8967/0`, ossifying renal tumour of infancy. |
| `8325` | Metanephric adenoma | `/0` only. WHO 2022 Table 1: `8325/0`. |
| `8361` | Juxtaglomerular tumor | `/0` only. WHO 2022 Table 1: `8361/0`. |
| `9013` | Adenofibroma, NOS | `/0` only. WHO 2022 Table 1: `9013/0` metanephric adenofibroma. |
| `8040` | Small cell carcinoma, NOS | **Mislabelled and out of behaviour.** `8040` is *Tumorlet* at `/0` and `/1`. "Small cell carcinoma, NOS" is `8041/3`, which the file already offers separately. |
| `8053` | Squamous cell papilloma, inverted | `/0` only. |
| `8060` | Squamous papillomatosis | `/0` only. |
| `8191` | Embryonal adenoma | `/0` only. |
| `8561` | Adenolymphoma | `/0` only. |

Ten of the eleven are **behaviour exclusions**, the `9514` pattern from Group V. One (`8965`) is a
**retired number**, the first the project has met in a live option list.

### 2B. Three codes the inventory carries that REDCap does not offer

`8023/3` NUT-associated carcinoma · `8054/3` warty carcinoma · `8482/3` mucinous carcinoma, gastric
type. All three are ICD-O-3.2 additions. They go on `docs/codes-awaiting-redcap.md`.

### 2C. Eight string drifts — the exact-string check will fail on these

| Code | REDCap option string | ICD-O-3.2 preferred term | Where the REDCap string sits |
|---|---|---|---|
| `8963` | Malignant rhabdoid tumor | **Rhabdoid tumor, NOS** | a synonym under `8963/3` |
| `8122` | Transitional cell carcinoma, spindle cell | **Urothelial carcinoma, sarcomatoid** | a synonym under `8122/3` |
| `8130` | Papillary transitional cell carcinoma | **Papillary urothelial carcinoma** | a synonym, and **both carry `[obs]`** |
| `8131` | Transitional cell carcinoma, micropapillary | **Urothelial carcinoma, micropapillary** | a synonym under `8131/3` |
| `8240` | Carcinoid tumor, NOS | **Neuroendocrine tumor, NOS** | a synonym under `8240/3` |
| `8155` | Vipoma, malignant | **Vipoma** | **no match at any level** |
| `8311` | Hypernephroid tumor `[obs]` | **Hereditary leiomyomatosis and renal cell carcinoma (HLRCC) syndrome-associated renal cell carcinoma** | the `[obs]` `8311/1` term — see §0.5 |
| `8504` | Intracystic carcinoma, NOS | **Encapsulated papillary carcinoma with invasion** | the `8504/**2**` synonym — a behaviour drift |

`8311` and `8504` are the two that matter clinically: each REDCap label names a **different lesion**
from the one the code now carries.

### 2D. One code has no current term at behaviour 3 at all

`8130` is not in any of the three classes above. Queried against `icdo32.sqlite` on 22 September
2026: it carries six terms across three behaviours, and **both of the two at behaviour 3 carry
`[obs]`** — *Papillary urothelial carcinoma* (Preferred) and *Papillary transitional cell carcinoma*
(Synonym). The `/1` and `/2` terms are clean and current. None of the four IARC 3.1→3.2 change
documents mentions `8130`, so the marker is inherited from ICD-O-3.1.

The reason is visible in the behaviour split: an invasive papillary urothelial carcinoma is now
coded `8120/3 Transitional cell carcinoma, NOS`, and the "papillary" qualifier was dropped at
behaviour 3. WHO 2022 Table 1 does not list `8130` under the kidney at all.

**The code stays in the inventory.** ICD-O-3.2 carries `8130/3` and ICCC-3 VIb admits it, so the
generator returns it and the tool holds it. It has no decision-tree branch — it is an adult
urothelial code — and its `coding_note` must record that every term on it at behaviour 3 is
obsolete. Do not apply the weaker test and remove it; that is what wrongly removed `9430/3` and
`9480/3` from Group III (§0.6).

---

**The exact-string check is keyed off Layer 1, never off `redcap_option_verified`.** A flag authored
to mean "not yet checked" was once read as "exempt", and six drifted names passed a green build.
`morphology_name` is the ICD-O-3.2 preferred term; where Layer 1 disagrees, the repair package
records it and the check is expected to report the drift.

---

## 3. The code decisions this group forces

### 3.1 `8963` — the group's only dual-group code, and the routing already exists

`data/shared/presentation_router.json` → `dual_group_rules["8963"]` already routes
`C70.9/C71.9/C72.9` → Group 3 (via `9508`), `C64.9` → Group 6 `VIa2`, default → Group 9 `IXd3`.
**No router change is needed for `8963`.** The morphology entry carries
`topography_dependent: true` and a `topography_routing_note`; the tree's rhabdoid terminal is
reachable only with `C64.9` confirmed.

### 3.2 `8959/3` — emitted, but never on a benign or borderline description

`8959` is one four-digit code over three diseases: `/0` benign cystic nephroma (including the
DICER1 paediatric cystic nephroma), `/1` cystic partially differentiated nephroblastoma, `/3`
malignant cystic nephroma. Only `/3` is in Group VI, and WHO 2022 places no entity there (§0.7).

The tree must therefore ask which of the three the report describes, and:

- **malignant cystic nephroma stated** → `8959/3`, with a `coding_note` recording that ICD-O-3.2
  carries the code and WHO 2022 Table 1 does not list an entity on it;
- **benign cystic nephroma / mixed epithelial and stromal tumour / paediatric (DICER1) cystic
  nephroma** → `behaviour_exclusion` on `8959/0`, `registrar_decision_required: true`;
- **cystic partially differentiated nephroblastoma** → `behaviour_exclusion` on `8959/1`. Note this
  one carefully: SIOP treats CPDN as *low-risk nephroblastoma* and it is a real paediatric
  diagnosis, so the exclusion text must say the case is outside the group's behaviour declaration,
  **not** that it is not a tumour.
- **cystic Wilms tumour** (a Wilms with cystic change, not a cystic nephroma) → `8960/3`.

### 3.3 `8960/1` mesoblastic nephroma is out of the group — and the pathway document's recode is wrong

The diagnostic pathway document §4D asserts that "this registry maps congenital mesoblastic
nephroma to 8960 by ICD-O-3 recode convention" and instructs the build to document the convention
in the `8960` `coding_note`.

**Do not implement that.** WHO 2022 Table 1 puts mesoblastic nephroma, and its classic, cellular
and mixed subtypes, at `8960/**1**`. ICD-O-3.2 agrees: `8960/1 Preferred Mesoblastic nephroma`.
ICCC-3 Group VI admits behaviour 3. Coding a congenital mesoblastic nephroma as `8960/3` records a
**malignant Wilms tumour for an infant who has a borderline fibroblastic tumour** — the precise
class of defect this project exists to prevent, and a far worse error than leaving the case for the
registrar. Congenital mesoblastic nephroma gets a `behaviour_exclusion` on `8960/1`, not a recode.

If the registrar *wants* the recode, that is a ruling to make explicitly, with its consequences on
the record. It is not a convention to inherit silently from a document that cites no source for it.

### 3.4 `8000`–`8005` at a renal site currently reach Group XII, not Group VI

`dual_group_rules["8000-8005"]` sends everything that is not a CNS site to Group 12. ICCC-3 VIc is
`8000-8005` **at C64.9**. A malignant renal neoplasm NOS therefore cannot reach Group VI at all.
This is the same class of defect as *"a neuroblastoma at C48.2 could never reach Group 4"*
(commit `10ca4fa`). Add a `C64.9 → {group: 6, subgroup: "VIc"}` branch **above** the default.

### 3.5 Nephrogenic rests and nephroblastomatosis have no ICD-O code at all

WHO 2022 Table 1 lists *Nephrogenic rests*, *Perilobar nephrogenic rests*, *Intralobar nephrogenic
rests* and *Nephroblastomatosis* under "Nephroblastic tumours" **with no ICD-O code printed against
any of them**. Fialkowski et al. *Pediatric Blood & Cancer* 2022;69(12):e30162, DOI
[10.1002/pbc.30162](https://doi.org/10.1002/pbc.30162) — on disk — establishes that there is no
gold-standard test separating them from Wilms tumour on imaging or on pathology.

This is the justification for **not** auto-coding a diffuse or multifocal renal process to `8960/3`
without histology, and for the imaging route's diversion criteria. A terminal for this pattern emits
no code and says why.

---

## 4. Tree architecture

One tree, `g6_renal`, entry node `rn_document_inventory`. Node-id prefix `rn_`.

```
rn_document_inventory  (document_inventory, step 1)
  ├── referral / clinical note only ............ rn_clinical_alias
  ├── imaging only, no tissue ................. rn_age_gate  →  rn_imaging_pathway
  ├── histology report present ................ rn_age_gate  →  rn_histology
  ├── cytology only ........................... rn_cytology
  └── specimen inadequate / uninterpretable ... rn_age_gate  →  rn_imaging_pathway

rn_age_gate            (numeric_gate, step 2)   variable patient_age_years, band_variable age_band
                                                bands: <2 · 2-4 · 5-9 · >=10 · not_documented

rn_imaging_pathway     (imaging_pathway, step 3)
rn_imaging_insufficient(morphology_only, step 4)

rn_histology           (histology_subclassification, step 3)  Wilms vs non-Wilms
  ├── triphasic nephroblastoma ................ 8960/3
  ├── cystic mass ............................. rn_cystic          (3.2)
  ├── rhabdoid morphology ..................... rn_ihc_checklist
  ├── clear-cell-sarcoma morphology ........... rn_ihc_checklist
  ├── carcinomatous architecture .............. rn_carcinoma
  └── benign / borderline entity named ........ behaviour_exclusion terminals

rn_ihc_checklist       (ihc_checklist, step 4)   the SMARCB1/INI1 fork  (4.3)
rn_carcinoma           (histology_subclassification, step 4)  the VIb leaves
rn_molecular           (molecular_freetext, step 5)  code-neutral for 8960; code-defining for 8311
```

Exact node inventory, labels and options are Task 2's to author against this shape. A deviation is
allowed if it is recorded with its reason in the build report.

### 4.1 Evidence does not monotonically refine the code — and the output must say so

This is the group's structural peculiarity and the pathway document's §0 is right about it. For
Wilms tumour, histology arrives **after** the nephrectomy that treats the child, and when it
arrives it refines the **SIOP risk group**, not the ICD-O code. `8960/3` is the code at every stage.

So the `8960` terminal must **not** present missing histology as an outstanding-workup row the clerk
should close. Nothing is outstanding: under SIOP the tissue does not exist yet, and under COG a
biopsy would upstage the tumour to local stage III. Spreafico F, et al. *Wilms tumour.* Nature
Reviews Disease Primers 2021;7:75, DOI [10.1038/s41572-021-00308-8](https://doi.org/10.1038/s41572-021-00308-8) — on disk — is the source for both facts.

**`satisfies_tests` is the field that suppresses an outstanding-workup row, and it is the one field
that can make a case look better worked up than it is.** A typo never matches and the suppression
quietly does nothing; a value the code does not require is an inert no-op that still reads as a live
claim. The validator checks it. Use it deliberately here and nowhere casually.

### 4.2 The imaging route

`imaging_sufficient: true` on `8960/3` **only** (§0.11). The confirmed-constellation terminal emits
`8960/3` at `basis_of_diagnosis: 2`. No Group VI terminal emits basis 1. A file with a referral
letter and nothing else reaches `rn_clinical_alias`, which emits **no code** — it records the
wording and sends the case on for imaging, because Table 3 gives nephroblastoma basis 2 and not
basis 1. That is the one structural difference between this group's alias node and Group V's, and
it is deliberate.

Note the engine constraint recorded in `docs/TODO.md` §10 and Group 5 contract §0.6:
`imagingPathway()` renders only `imaging_features`, `biochemical_questions` and
`diversion_criteria` — `options[]` is **never** rendered on an `imaging_pathway` node. So
`rn_imaging_pathway` declares `insufficient_next_node`, does not declare `options[]`, and carries
its own `morphology_code` / `behavior_code` / `basis_of_diagnosis` for the confirmed outcome.

Imaging features to encode, and their standing:

- intrarenal origin — the **claw sign** — separating Wilms tumour from neuroblastoma, which is
  extrarenal and **encases** vessels where Wilms **displaces** them;
- a large, well-demarcated mass that pushes rather than invades, in a child under five.

**The dedicated imaging source is still missing.** Chung EM, et al. *Renal Tumors of Childhood:
Radiologic-Pathologic Correlation* Part 1, RadioGraphics 2016;36(2):499–522, DOI
[10.1148/rg.2016150230](https://doi.org/10.1148/rg.2016150230), and Part 2, RadioGraphics
2017;37(5):1538–1558, DOI [10.1148/rg.2017160189](https://doi.org/10.1148/rg.2017160189), are named
in the papers index as the designated sources and **neither is on disk**. Author the imaging
features from what is on disk, mark them in `imaging_features` as resting on Spreafico 2021 and the
papers index rather than on a dedicated imaging source, and put both Chung papers on
`docs/sources-requested.md`.

**Diversion criteria — any one forces the tissue branch:**

1. diffuse or multifocal renal involvement, or nephrogenic rests / nephroblastomatosis described
   (§3.5) — imaging cannot separate these from Wilms tumour;
2. extrarenal origin, or vessel encasement rather than displacement — the neuroblastoma pattern,
   which is Group IV, not Group VI;
3. an infiltrative medullary mass in an adolescent, with or without sickle-cell trait — the renal
   medullary carcinoma pattern (§4.3);
4. age ten or over — renal cell carcinoma overtakes Wilms tumour in the second decade
   (Cajaiba MM, et al. *Cancer* 2018;124(16):3381–3389, DOI
   [10.1002/cncr.31578](https://doi.org/10.1002/cncr.31578), on disk), and imaging alone cannot
   carry a carcinoma diagnosis.

### 4.3 ★ The SMARCB1/INI1 fork — one marker, two codes, decided by age and sickle-cell status

Loss of nuclear SMARCB1 (INI1) is the defining finding for **both** `8963/3` rhabdoid tumour of the
kidney and `8510/3` renal medullary carcinoma. **The tool must not auto-resolve INI1 loss to
`8963`.** Written as three rules in `rn_ihc_checklist.resolution_logic`, conditioned rules first:

```
1. when {age_band: [">=10"]}, sickle_cell_status in {trait, disease}, SMARCB1 lost   → 8510/3
2. when {age_band: ["<2", "2-4"]},                                  SMARCB1 lost     → 8963/3
3.                                                                  SMARCB1 lost     → no code; registrar
```

Sources, all on disk: Sredni ST & Tomita T. *Rhabdoid Tumor Predisposition Syndrome.* Pediatric and
Developmental Pathology 2015;18(1):49–58, DOI [10.2350/14-07-1531-MISC.1](https://doi.org/10.2350/14-07-1531-MISC.1)
for the rhabdoid side; Trpkov K, et al. *New developments in existing WHO entities and evolving
molecular concepts: the Genitourinary Pathology Society (GUPS) update on renal neoplasia.* Modern
Pathology 2021;34(7):1392–1424, DOI [10.1038/s41379-021-00779-w](https://doi.org/10.1038/s41379-021-00779-w),
and Kanakaraj J, Chang J, Hampton LJ, Smith SC. *The new WHO category of "molecularly defined renal
carcinomas": clinical and diagnostic features and management implications.* Urologic Oncology
2024;42(7):211–219, DOI [10.1016/j.urolonc.2024.02.003](https://doi.org/10.1016/j.urolonc.2024.02.003),
for the medullary side.

**★ A genuine two-source conflict on haemoglobinopathy, and the later document wins.**

The diagnostic pathway document's §2E says haemoglobinopathy is an "**essential** diagnostic
criterion" for renal medullary carcinoma. It is not making that up — it is quoting Trpkov 2021
correctly:

> **Trpkov 2021, p. 1407:** *"The presence of a hemoglobinopathy is now considered an essential
> diagnostic criterion."* GUPS separated the SMARCB1-lost tumour **without** a haemoglobinopathy as
> a distinct lesion, *"unclassified renal cell carcinoma with medullary phenotype"* (RCCU-MP),
> *"essentially indistinguishable from renal medullary carcinoma, by histology and
> immunohistochemistry, except for the lack of hemoglobinopathy in the affected patients, and often
> older age at presentation."*

> **Moch 2022 §2.4, one year later and the group's baseline:** *"Some unclassified RCC cases with
> medullary phenotype can show complete loss of SMARCB1, but no association with
> haemoglobinopathies, suggesting that sickle cell is not a prerequisite for this genetic lesion.
> These tumours can be regarded as subtypes of SMARCB1-deficient medullary RCC."*

WHO 2022 Table 1 acts on that: *SMARCB1-deficient undifferentiated renal cell carcinoma, NOS* sits
on **`8510/3`**, alongside medullary carcinoma. **Latest document wins, and it is also the group's
baseline**, so the tool follows Moch.

Two consequences for the fork:

1. Rule 3 must not read "no sickle-cell trait, therefore not `8510`". Under WHO 2022 the tumour
   Trpkov called RCCU-MP is a subtype of the same code. The honest terminal names the finding, emits
   no code on its own authority, and refers to the registrar — and its `reason` says *why* it is
   uncertain, which is that two current sources disagree and the case is an adolescent with a
   SMARCB1-deficient medullary tumour and no documented haemoglobinopathy.
2. **Collecting duct carcinoma retains SMARCB1.** Both sources agree, and it is what separates
   `8319/3` from `8510/3`. Trpkov 2021 adds that collecting duct carcinoma *"should only be
   diagnosed when other considerations, particularly fumarate hydratase-deficient renal cell
   carcinoma, medullary carcinoma, and metastases from other primaries are excluded"* — a diagnosis
   of exclusion, which belongs in the node's `hint`.

**And the third tumour the sickle-cell association points at.** Argani P. *Translocation carcinomas
of the kidney.* Genes, Chromosomes and Cancer 2021;60(3):219–227, DOI
[10.1002/gcc.23007](https://doi.org/10.1002/gcc.23007) — on disk — records that ALK-rearranged renal
cell carcinoma also has a predilection for children with sickle-cell trait. So "sickle trait plus a
renal carcinoma" is not pathognomonic for renal medullary carcinoma, and the node must prompt for
ALK as well as SMARCB1. ALK-rearranged RCC codes `8311/3` (§0.5).

`sickle_cell_status` is a captured variable with values `trait` · `disease` · `negative` ·
`unknown`. In a registry where sickle-cell trait is common, `unknown` will be the modal answer and
must not be silently read as `negative`.

### 4.4 Anaplasia is a prognostic modifier, never a code — and "nuclear unrest" is not anaplasia

Hill DA, et al. *Clinical and biologic significance of nuclear unrest in Wilms tumor.* Cancer
2003;97(9):2318–2326, DOI [10.1002/cncr.11325](https://doi.org/10.1002/cncr.11325) — on disk —
defines **nuclear unrest** as nuclear enlargement resembling anaplasia **with no abnormal multipolar
mitotic figures**, and shows it behaves as favourable histology.

Pfister SM, et al. *Cancer Discovery* 2022;12(2):331–355, DOI
[10.1158/2159-8290.CD-21-1094](https://doi.org/10.1158/2159-8290.CD-21-1094) gives the WHO
three-part criterion for true anaplasia: *"nucleomegaly (at least three times the size of
nonanaplastic nuclei), nuclear hyperchromatism, and abnormal/atypical mitoses."*

Both stay `8960/3`. The tool records anaplasia status as a code-neutral annotation and **must not
let the words "atypia" or "nuclear enlargement" alone set a high-risk flag**. The SIOP risk subtypes
— completely necrotic, blastemal, regressive, epithelial, stromal, mixed, focal or diffuse
anaplasia (Vujanić GM, et al. *Medical and Pediatric Oncology* 2002;38(2):79–82, DOI
[10.1002/mpo.1276](https://doi.org/10.1002/mpo.1276), on disk) — are likewise code-neutral.

### 4.5 The molecular layer splits by entity

- **Wilms tumour (`8960/3`):** WT1, CTNNB1, WTX, 1q gain, 11p15 loss of heterozygosity are
  prognostic and change no code. `code_neutral_molecular: true`.
- **Clear cell sarcoma of the kidney (`8964/3`):** BCOR internal tandem duplication and
  YWHAE::NUTM2B confirm a code morphology and immunohistochemistry already set. Code-neutral.
  Aldera AP & Pillay K. *Clear cell sarcoma of the kidney.* Archives of Pathology & Laboratory
  Medicine 2020;144(1):119–123, DOI [10.5858/arpa.2018-0353-RS](https://doi.org/10.5858/arpa.2018-0353-RS),
  on disk, for the BCOR / cyclin D1 / NGFR panel.
- **Renal carcinoma:** molecular findings are **code-defining** and land on `8311/3` (§0.5), not on
  `8312/3`. The prioritised workup Cajaiba 2018 gives is TFE3 immunohistochemistry → TFE3/TFEB
  break-apart FISH → fusion FISH → next-generation sequencing.

### 4.6 The clinical detail the tree needs, extracted so nobody re-reads the PDFs

Everything below was read out of the papers held in `Group 6 Papers/` on 22 September 2026. An
implementing agent should author from this section, not from the PDFs.

**Clear cell sarcoma of the kidney — the marker panel.** Aldera AP & Pillay K. *Archives of
Pathology & Laboratory Medicine* 2020;144(1):119–123, pp. 121–122:

- **BCOR** (BCL-6 coreceptor), diffuse strong **nuclear** staining — *"highly sensitive and specific
  for the diagnosis of [clear cell sarcoma of the kidney] in the context of pediatric renal
  neoplasia."* This is the confirmatory marker.
- **Cyclin D1** and **nerve growth factor receptor (NGFR)** — *"sensitive but not entirely
  specific."* Supporting, not confirmatory.
- **Consistently negative** for cytokeratins, epithelial membrane antigen, synaptophysin, S100,
  CD34, desmin, membranous CD99, **and WT1**.
- Molecular: **BCOR internal tandem duplication**; **t(10;17) YWHAE::NUTM2B/E**.

> **The WT1-negative result is the discriminator that matters.** Blastemal Wilms tumour is WT1
> positive and clear cell sarcoma of the kidney is WT1 negative, and the two are the pair the
> morphology node cannot separate. Put WT1 in the panel.

**The anaplasia criterion — all three features, or it is not anaplasia.** Vujanić GM, et al.
*Medical and Pediatric Oncology* 2002;38(2):79–82, p. 81, requires *"the presence of all three
criteria"*:

1. atypical tri- or multipolar mitotic figures;
2. marked nuclear enlargement, with diameters **at least three times** those of adjacent cells;
3. hyperchromatic tumour cell nuclei.

Pfister SM, et al. *Cancer Discovery* 2022;12(2):331–355 states the same three for WHO. Hill DA,
et al. *Cancer* 2003;97(9):2318–2326 shows that nuclear enlargement **without** the abnormal
multipolar mitoses — *nuclear unrest* — behaves as favourable histology. So a report saying "atypia"
or "nuclear enlargement" and nothing about mitotic figures does **not** support an anaplastic
classification, and the tool must not let it set one.

*Focal* anaplasia (Vujanić p. 81) is *"a clearly defined focus within a primary intrarenal tumour,
without evidence of anaplasia or prominent nuclear atypia in extrarenal tumour sites."* *Diffuse*
anaplasia is everything else. Both stay `8960/3`.

**The SIOP risk groups, verbatim from Vujanić Table I — and note there are two lists, not one.**

*A. For pretreated cases (after preoperative chemotherapy):*

| Risk | Entities |
|---|---|
| Low | Mesoblastic nephroma · cystic partially differentiated nephroblastoma · completely necrotic nephroblastoma |
| Intermediate | Nephroblastoma — epithelial type · stromal type · mixed type · regressive type · focal anaplasia |
| High | Nephroblastoma — blastemal type · diffuse anaplasia · clear cell sarcoma of the kidney · rhabdoid tumour of the kidney |

*B. For primary nephrectomy cases (no preoperative chemotherapy):*

| Risk | Entities |
|---|---|
| Low | Mesoblastic nephroma · cystic partially differentiated nephroblastoma |
| Intermediate | Non-anaplastic nephroblastoma and its variants · focal anaplasia |
| High | Nephroblastoma — diffuse anaplasia · clear cell sarcoma of the kidney · rhabdoid tumour of the kidney |

**Blastemal type is high risk only after preoperative chemotherapy.** Vujanić p. 80: *"In cases
diagnosed after primary nephrectomy, blastemal nephroblastoma remains in the intermediate risk
tumors."* Its criteria: only the **viable** part is assessed and must comprise **more than one
third** of the tumour mass; **at least two thirds** of that viable tumour must be blastema.

So the tool cannot record a SIOP risk subtype without knowing whether the specimen is
pre-treatment or post-chemotherapy. If the tree captures risk at all, it captures that first. All
of it is code-neutral — every row above that is a nephroblastoma stays `8960/3`.

> Note what the SIOP low-risk row contains: **mesoblastic nephroma** and **cystic partially
> differentiated nephroblastoma**, both of which this group cannot code (§3.2, §3.3). They are real
> paediatric diagnoses that a SIOP-following unit will send to this registry. The behaviour-exclusion
> text for them must say the case is outside the group's behaviour declaration and belongs with the
> registrar — never that it is not a tumour.

**Renal cell carcinoma workup order.** Cajaiba 2018, p. 3387: characteristic morphology plus
under-expression of epithelial markers plus diffuse strong nuclear **TFE3** immunohistochemistry
*"reliably detected RCC with TFE3 rearrangements in our series without the need for molecular
studies"* — but FISH break-apart probes give **false negatives** on NONO::TFE3 and RBM10::TFE3
because the rearrangements are inversions and the split signals do not separate. So a negative
break-apart FISH does not overturn a positive TFE3 immunohistochemistry with matching morphology.
Order: TFE3 immunohistochemistry → TFE3/TFEB break-apart FISH → fusion-specific FISH →
next-generation sequencing.

---

## 5. What the diagnostic pathway document gets wrong

`../Group 6 — Renal Tumors Diagnostic Pathway.md` (v1.1, 5 June 2026). Most of it is sound and its
§0 diagnosis of the group's structure is the best thing written about this build. Six errors:

| # | The document says | The sources say |
|---|---|---|
| **5.1** | Benign and borderline entities "are intentionally present in the RedCap list and are therefore in-scope" (§4H scope note, §7.11, §8 item 7) | ICCC-3 Group VI declares behaviour **3**. They are out of the group by the recode's definition. Presence in an option file is not scope (§0.2). |
| **5.2** | `8959` is "the DICER1-associated cystic variant"; code `8959` for it (§4C) | WHO 2022 Table 1 puts paediatric (DICER1) cystic nephroma at `8959/**0**`, benign (§0.7). |
| **5.3** | CMN is recoded to `8960` "per registry convention" (§4D, §7.10) | `8960/1` in both ICD-O-3.2 and WHO 2022 Table 1. The recode would register a benign-behaviour tumour as malignant (§3.3). |
| **5.4** | Urothelial carcinoma of the renal pelvis is Group VI at C65.9 (§1) | C65.9 is `XIf10`. Group VI has no C65.9 anywhere (§0.2). |
| **5.5** | The molecular RCCs "all collapse to 8312" with no dedicated code (§4F, §7.6) | `8311/3` exists and WHO 2022 Table 1 assigns them to it (§0.5). |
| **5.6** | Haemoglobinopathy is an "essential diagnostic criterion" for `8510` (§2E) | Correct as of Trpkov 2021, superseded by Moch 2022 §2.4: sickle cell is **not a prerequisite**, and WHO 2022 Table 1 puts the SMARCB1-deficient tumour without haemoglobinopathy on the same code. Latest document wins (§4.3). |

Its §7.13 proposal to author separate `morphology_entries` per behaviour for `8959` and `8960` is
**half right**: the behaviours below 3 are not entries in this file at all, they are
`behaviour_exclusion` blocks. `morphology_entries[]` is generated and carries only behaviour 3.

Everything else in §7 — 7.1 through 7.5, 7.7, 7.8, 7.9, 7.12 — is correct and is implemented.

---

## 6. The alias layer

`data/aliases/aliases_group_06.json`, cross-resolving against `group_06_dt.json`, regenerated into
`alias_index.json` by `build/build_database.py`.

The vocabulary this group must catch, beyond the preferred terms:

- **Wilms tumour** in every spelling a clerk will write — *Wilms*, *Wilms'*, *Wilm's tumour*,
  *nephroblastoma* — all to `8960`.
- **Historical names**: *bone-metastasizing renal tumour of childhood* → `8964` clear cell sarcoma
  of the kidney; *Grawitz tumor* and *hypernephroma*, both `[obs]` synonyms of `8312/3`;
  *hypernephroid tumor*, the `[obs]` `8311/1` term, which must **not** reach `8311/3` (§0.5).
- **Molecular shorthand** a report will carry: *TFE3-rearranged*, *MiT family translocation
  carcinoma*, *TFEB-altered*, *FH-deficient*, *HLRCC*, *SDH-deficient*, *ELOC-mutated*,
  *ALK-rearranged* — all to `8311`.
- **The INI1 vocabulary**: *INI1*, *SMARCB1*, *BAF47*, *SNF5* are the same protein under four names
  and a report may use any of them.
- **Renal medullary carcinoma**, *RMC*, and its distinction from **collecting duct carcinoma** /
  *Bellini duct carcinoma* (`8319`), which is a different entity (§4.3).
- Terms that must resolve to a **non-Group-VI** destination: *congenital mesoblastic nephroma*,
  *cystic nephroma*, *metanephric adenoma*, *nephrogenic rest*, *nephroblastomatosis*,
  *angiomyolipoma*, *oncocytoma*.

Clerk-facing alias text goes in `reason` / `hint`. `coding_note` is not rendered.

---

## 7. Shared-layer changes this build requires

1. **`data/shared/presentation_router.json`** — `groups["6"]`: set `built: true`, declare the tree
   and the `handoff`, mirroring `groups["5"]`.
2. **`data/shared/presentation_router.json`** — `dual_group_rules["8000-8005"]`: add a
   `C64.9 → {group: 6, subgroup: "VIc"}` branch **above** the Group XII default (§3.4).

2b. **★ `data/shared/presentation_router.json` — close `docs/TODO.md` §12 for the two rules this
   group owns.** TODO §12 records three router rules still carrying a `cns_topography_scope_note`
   that reads *"topography_codes.json does not yet enumerate finer CNS subsites … Extend both files
   together when Group III is authored."* **Group III was authored on 16 September 2026 and
   `topography_codes.json` now enumerates all 21 codes in `C70.0`–`C72.9`.** The note's premise is
   false on its face. Two of the three rules are Group VI codes and this build owns them:

   | Rule | Defect | Fix |
   |---|---|---|
   | `8963` | Matches only `C70.9`/`C71.9`/`C72.9`. A rhabdoid tumour at a **specific** CNS subsite — `C71.6` cerebellum, say — misses the branch and falls to the default, **Group IX `IXd3`**, whose ICCC-2017 site list (`000-218,239-639,659-699,739-768,809`) **excludes `700-729` entirely**. So the default names a group ICCC-2017 does not admit there at all, and the case never reaches `9508/3` atypical teratoid/rhabdoid tumour. | Extend `topography_in` to all 21 codes `C70.0`–`C72.9`. Delete the scope note. |
   | `8000-8005` | Same shape. `8000/3` at a specific CNS subsite falls to **Group XII**, whose `XIIb` site list excludes `700-729` and `751-753`. | Extend `topography_in` to all 21 codes `C70.0`–`C72.9`, **keeping `C75.1`, `C75.2` and `C75.3`**, which match ICCC-2017 range 42's `700-729,751-753`. Delete the scope note. Then add the C64.9 branch from item 2. |

   Do this in the same edit as item 2, because it is the same rule object and leaving half of it
   stale while touching the other half is how a note outlives its reason.

   **The third rule, `9473`, is not this build's to fix.** TODO §12 shows it is wrong more broadly
   than the stale note accounts for — ICCC-2017 range 29 is the only range carrying `9473` at all,
   takes sites `000-809`, and resolves to `IIIc2`, so the rule's Group IX default has no basis at
   any topography. That is a Group III/IX decision. Leave it and say in the build report that it was
   left.
3. **`data/shared/topography_codes.json`** — `C64.9` already exists with `candidate_groups: [6]`.
   Confirm no change is needed. **Do not add `C65.9` to Group VI** (§0.2).
4. **`docs/group_06_layer1_repair.md`** — the REDCap-project repair package for §2. A REDCap
   document; nothing in the lookup tool depends on it, and nothing is applied to the live form.
5. **`docs/codes-awaiting-redcap.md`** — append `8023`, `8054`, `8482` (§2B).
6. **`docs/sources-requested.md`** — append both Chung RadioGraphics papers (§4.2).

---

## 8. Validation rules this group adds

Each is written **with a negative control**: break the data deliberately, watch the check fail,
restore. A check nobody has broken is not known to work.

| # | Check | What it would catch |
|---|---|---|
| 1 | `check_group6_code_set` | An entry whose `(code, behaviour)` is not in the generated inventory — the fabricated-code guard. |
| 2 | `check_group6_absent_codes` | Any of the eleven §2A codes appearing as a `morphology_code` anywhere in `group_06_dt.json`. |
| 3 | `check_group6_behaviour_declaration` | A `behaviour_exclusion` block whose `group_declares` is not `"3"`, or whose `icdo_code`/`icdo_behaviour` pair is not real in `icdo32.sqlite`. |
| 4 | `check_group6_ini1_fork` | An INI1-loss rule that resolves to `8963` or `8510` without a `when` on `age_band` **and**, for `8510`, without `sickle_cell_status` — the §4.3 guard. This is the group's signature check. |
| 5 | `check_group6_molecular_rcc_code` | A terminal that emits `8312/3` while the branch names a molecularly defined entity, or emits `8311/3` with no molecular finding recorded — the §0.5 guard, both directions. |
| 6 | `check_group6_8963_topography` | An `8963` terminal reachable without `C64.9` confirmed. |
| 7 | `check_group6_anaplasia_code_neutral` | An anaplasia or SIOP-risk option that carries a `morphology_code` other than `8960` — the §4.4 guard. |
| 8 | `check_group6_imaging_sufficient` | `imaging_sufficient: true` on any entry other than `8960`. |
| 9 | `check_group6_no_flow_cytometry` | `Flow cytometry` appearing in any Group VI `diagnostic_tests_required`. |

**Plus one extension to an existing check, which is not optional.**

`check_redcap_exact_names()` requires `morphology_name` to be character-identical to the REDCap
option string. Group VI has **eight** drifts (§2C), so under that check the build cannot pass with
correct data. Groups 3 and 4 already step aside from it in favour of `check_icdo32_round_trip()`,
which asks the stronger question — *is this a real ICD-O-3.2 term for this code at this behaviour?*
— and therefore rejects the `(code, term)` pairs the option list carries that ICD-O-3.2 does not,
where the REDCap check would inherit them.

**Extend `check_icdo32_round_trip()` to Group VI, and make `check_redcap_exact_names()` step aside
for it**, exactly as Group 4's contract §1.1a did. The scoping is a single equality on the group
number, which `check_top_level_keys()` cross-checks against `metadata.group_id`, so it is not a flag
in the file exempting itself. The drifted option strings do not disappear: they move to the alias
file, where they are checked the other way round — every alias must resolve to a valid triple, and
no alias is ever emitted as a name.

**Group 5 is left alone.** Its four names are character-identical to both sources, so it passes
either check and there is no defect to fix. Whether it should also move to the round-trip is a
question for the Group 5 branch, not this one. Record it; do not change it here.

Regression: Groups 1–5 must stay **byte-identical to their state on `group-05-retinoblastoma`**.

---

## 9. Proof before this group is called done

Green build is necessary and not sufficient.

1. `python3 build/build_database.py` → **0 FAIL**.
2. `python3 build/induce_flow.py` → every rule in every checklist has a witness.
3. Negative controls on all nine new checks.
4. **Drive the changed branches in the browser.** The two Group III defects that mattered most were
   invisible to the build, and Group V's two browser-only defects were a contraindicated procedure
   being requested and twenty-eight alias chips compressed to eighteen pixels. Check the SMARCB1
   fork, the imaging route and the `8959` cystic node by hand.
5. Confirm Groups 1–5 byte-identical.

---

## 10. The baseline document

**Moch 2022 is the right baseline and it is unusually good for this purpose.** It is a
peer-reviewed Review in *European Urology*, written by the volume's own editorial board with IARC's
Ian Cree among the authors, and — unlike Louis 2021 for CNS or Milman 2023 for eye — **it prints
the ICD-O-3.2 code against every entity in a single table**. For this group the classification
summary and the registry-implications document are the same paper.

**What it settles**

- The seven molecularly defined renal carcinomas, and that six of them share `8311/3` (§0.5).
- The four entities on `8510/3`, and that sickle-cell trait is not a prerequisite (§4.3).
- That `8959/3` carries no WHO 2022 entity (§0.7).
- That mesoblastic nephroma is `8960/1` (§3.3).
- That nephrogenic rests and nephroblastomatosis have no ICD-O code (§3.5).
- That collecting duct carcinoma retains SMARCB1 while medullary carcinoma loses it.

**What it does not settle**

- It is an adult-weighted paper. Wilms tumour gets one line in Table 1 and no discussion; the
  paediatric detail comes from Spreafico 2021, Vujanić 2002, Fialkowski 2022 and Treece 2020.
- Table 1's footnote marks codes "approved by the IARC/WHO Committee for ICD-O at its meeting in
  February 2022" with an asterisk. **The asterisks did not survive the PDF text extraction**, so
  which specific codes carry that mark is not readable from the extracted text and has not been
  established. Any claim resting on it must be checked against the PDF itself.
- No sixth edition of the urinary volume exists; a PubMed sweep found none.

**The paediatric volume is not the spine for this group — checked, not assumed.**
Pfister SM, et al. *Cancer Discovery* 2022;12(2):331–355 was retrieved in full from PubMed Central
(PMC9401511) and searched on 22 September 2026: **"kidney" appears zero times**; "renal" appears
16 times, none of them introducing a renal chapter; "Wilms" appears 6 times, all in passing — as
the worked example of a blastoma, in the anaplasia criterion quoted at §4.4, and in the
cancer-predisposition-syndrome groupings. There is no renal tumour section. This is the same
finding as for Group V, and it confirms the standing warning in
`docs/group_baseline_documents.md`: Pfister's coverage is chapter-by-chapter and uneven, and the
volume's name matching the group's name proves nothing.

**No registry-implications paper exists, and none is needed.** The PubMed MeSH sweep is recorded in
`Group 6 Papers/Group 6 — Registry-Implications MeSH Search Results.md`; its nine hits contain no
candidate. Moch Table 1 does the job.

---

## 11. What needs the registrar

Left for Jay, not resolved in this build.

1. **★ `8959/3` carries no WHO 2022 entity** (§0.7). ICD-O-3.2 has the code, ICCC-3 admits it at
   behaviour 3, WHO 2022 places nothing on it. Does the tool keep emitting it, or does malignant
   cystic nephroma become a registrar referral?
2. **★ The congenital mesoblastic nephroma recode** (§3.3). The pathway document asserts a registry
   convention mapping CMN to `8960` with no source. This build refuses it and emits a behaviour
   exclusion instead. If the convention is real, it needs a ruling and a record.
3. **`8311` is mislabelled in REDCap as a `[obs]` term for a different lesion** (§0.5, §2C). This is
   the most consequential single option-file defect the project has found: a clerk picking `8311`
   today reads "Hypernephroid tumor [obs]" and has no way to know the code now means HLRCC-associated
   and other molecularly defined renal cell carcinoma.
4. **`8965` is a retired number still offered in REDCap** (§2A). First retired number met in a live
   option list. It needs the `[RETIRED]` treatment the Group V package defines for `9514`.
5. ~~**Does Visser Table 3 admit a renal tumour at basis 1 or 2?**~~ **Closed 22 September 2026.**
   Table 3 gives nephroblastoma basis **2**, C64, `8960/3`, Group VI. The imaging route is
   legitimate at basis 2; no Group VI terminal emits basis 1 (§0.11).
6. **Whether benign renal entities should be registered at all.** Ten REDCap options are behaviour 0
   or 1 (§2A). Group VI cannot hold them. If the registry wants them, they need a home outside
   Group VI, not a behaviour override inside it.
7. **Both Chung RadioGraphics papers are missing** (§4.2), so the imaging-feature lists rest on
   Spreafico 2021 and the papers index rather than on a dedicated imaging source.
