# Baseline WHO documents, and the verification pathway for every group

**Registrar's ruling, 16 September 2026.** The way Group 3 was built is the standard for every
remaining group. Each one gets a baseline WHO classification document, the same two-source code
verification, and the same proof before it is called done.

Built: **1, 2, 3**, then **4** and **5** on their own branches, and **6** in progress on
`group-06-renal`. Remaining: **7, 8, 9, 10, 11, 12**.

---

## 1. The baseline document

Every group needs one current WHO classification summary paper, doing for that group what
**Louis DN, et al. *The 2021 WHO Classification of Tumors of the Central Nervous System: a
summary.* Neuro-Oncology 2021;23(8):1231–1251** does for Group 3: it is the authority on which
entities exist, which were retired, and which share an ICD-O code.

**If the document is absent or insufficient — load the PubMed connector, find it, and tell Jay
before building.** A pathway is not designed on secondary sources or on recall.

| ICCC-3 group | WHO 5th-edition volume | Baseline summary paper | PubMed |
|---|---|---|---|
| **I** — Leukaemias, myeloproliferative and myelodysplastic diseases | Vol. 11, Haematolymphoid Tumours | **Khoury JD, et al.** *The 5th edition of the WHO Classification of Haematolymphoid Tumours: Myeloid and Histiocytic/Dendritic Neoplasms.* Leukemia 2022;36(7):1703–1719. [10.1038/s41375-022-01613-1](https://doi.org/10.1038/s41375-022-01613-1) | PMID 35732831 · PMC9252913 |
| **II** — Lymphomas and reticuloendothelial neoplasms | Vol. 11, Haematolymphoid Tumours | **Alaggio R, et al.** *The 5th edition of the WHO Classification of Haematolymphoid Tumours: Lymphoid Neoplasms.* Leukemia 2022;36(7):1720–1748. [10.1038/s41375-022-01620-2](https://doi.org/10.1038/s41375-022-01620-2) | PMID 35732829 · PMC9214472 |
| **III** — CNS and miscellaneous intracranial and intraspinal | Vol. 6, CNS Tumours | **Louis DN, et al.** *The 2021 WHO Classification of Tumors of the Central Nervous System: a summary.* Neuro-Oncology 2021;23(8):1231–1251. [10.1093/neuonc/noab106](https://doi.org/10.1093/neuonc/noab106) | **held on disk** — `Group 3 Papers/Exported Items/PDF/13300/` |
| **IV** — Neuroblastoma and other peripheral nervous cell tumours | Vol. 7, Paediatric Tumours | **Pfister SM, et al.** *A Summary of the Inaugural WHO Classification of Pediatric Tumors: Transitioning from the Optical into the Molecular Era.* Cancer Discovery 2022;12(2):331–355. [10.1158/2159-8290.CD-21-1094](https://doi.org/10.1158/2159-8290.CD-21-1094) | PMID 34921008 · PMC9401511 |
| **V** — Retinoblastoma | Vol. 13, Eye and Orbit Tumours | **Milman T, Grossniklaus HE, et al.** *The 5th Edition of the World Health Organization Classification of Tumours of the Eye and Orbit.* Ocular Oncology and Pathology 2023;9(3–4):71–95. [10.1159/000530730](https://doi.org/10.1159/000530730) | PMID 37900189 · PMC10601864 |
| **VI** — Renal tumours ✅ | Vol. 8, Urinary and Male Genital Tumours (Part A) | **Moch H, et al.** *The 2022 WHO Classification of Tumours of the Urinary System and Male Genital Organs — Part A: Renal, Penile, and Testicular Tumours.* European Urology 2022;82(5):458–468. [10.1016/j.eururo.2022.06.016](https://doi.org/10.1016/j.eururo.2022.06.016) | PMID 35853783 · **held on disk** — `Group 6 Papers/Moch-2022-WHO-urinary-male-genital-PartA.pdf` |
| **VII** — Hepatic tumours | Vol. 1, Digestive System Tumours | **Nagtegaal ID, et al.** *The 2019 WHO classification of tumours of the digestive system.* Histopathology 2020;76(2):182–188. [10.1111/his.13975](https://doi.org/10.1111/his.13975) | PMID 31433515 · PMC7003895 |
| **VIII** — Malignant bone tumours | Vol. 3, Soft Tissue and Bone Tumours | **Sbaraglia M, Bellan E, Dei Tos AP.** *The 2020 WHO Classification of Soft Tissue Tumours: news and perspectives.* Pathologica 2020;113(2):70–84. [10.32074/1591-951X-213](https://doi.org/10.32074/1591-951X-213) | PMID 33179614 · PMC8167394 |
| **IX** — Soft-tissue and other extraosseous sarcomas | Vol. 3, Soft Tissue and Bone Tumours | same as VIII | PMID 33179614 · PMC8167394 |
| **X** — Germ cell, trophoblastic and gonadal neoplasms | Vol. 8, Urinary and Male Genital (Part A, testis) **+** Vol. 4, Female Genital | **Moch H, et al.** European Urology 2022;82(5):458–468. [10.1016/j.eururo.2022.06.016](https://doi.org/10.1016/j.eururo.2022.06.016) · **Höhn AK, et al.** *2020 WHO Classification of Female Genital Tumors.* Geburtshilfe und Frauenheilkunde 2021;81(10):1145–1153. [10.1055/a-1545-4279](https://doi.org/10.1055/a-1545-4279) | PMID 35853783 · PMID 34629493 / PMC8494521 |
| **XI** — Other malignant epithelial neoplasms and malignant melanomas | Vol. 10, Endocrine and Neuroendocrine Tumours (**thyroid only**) | **Juhlin CC, Mete O, Baloch ZW.** *The 2022 WHO classification of thyroid tumors: novel concepts in nomenclature and grading.* Endocrine-Related Cancer 2022;30(2):e220293. [10.1530/ERC-22-0293](https://doi.org/10.1530/ERC-22-0293) | PMID 36445235 |
| **XII** — Other and unspecified malignant neoplasms | none | **Residual bucket by design** — no single volume. Verify each code against whichever volume owns the entity. | — |

Baseline list supplied by the registrar, 16 September 2026, and **every entry verified against
PubMed** the same day: each DOI was resolved to its PubMed record and the citation checked against
the returned metadata. Only Group III's paper is held on disk. **Four entries are provisional — see below.**

### ⚠️ Four entries are provisional and await the registrar's verification

Flagged 16 September 2026. **No 6th-edition volume exists for any of these** — a PubMed sweep for
sixth editions returned nothing, so the 5th-edition volumes are current. The problem is **fit, not
edition**: three of these papers do not actually cover the group they are assigned to.

| Group | Concern |
|---|---|
| **VIII** — bone | Sbaraglia is titled *"The 2020 WHO Classification of **Soft Tissue** Tumours"*. It does not cover the bone chapter. A search for a dedicated bone-chapter summary returns only head-and-neck jawbone tumours (Vered & Wright, Head Neck Pathol 2022;16(1):63–75) and further soft-tissue summaries (Choi & Ro, Adv Anat Pathol 2021;28(1):44–58). **Group VIII currently has no baseline that covers it.** |
| **V** — retinoblastoma | ~~Milman 2023 is indexed by PubMed as an **Editorial** with no abstract. It announces the Eye and Orbit volume rather than summarising its entities the way Louis 2021 does for CNS. Usable as a pointer; thin as an authority.~~ **RESOLVED 22 Sep 2026 — Milman 2023 stands.** The Editorial tag is real and is not a measure of standing: 25 pages against Louis 2021's 21, organised by chapter with "ICD-O coding" subsections throughout, and written by the Eye and Orbit volume's **own editorial board** — the same model as Louis 2021, which is the CNS volume's own board. No better candidate exists. Two real weaknesses replace the one withdrawn: it summarises a **beta version ahead of print** (April 2023) while the bound volume printed **23 January 2026**, thirty-three months later with no published comparison; and its Table 9 names only *Retinocytoma* and *Retinoblastoma* under the neurosensory retina, leaving the status of `9511/3`, `9512/3` and `9513/3` unsettled behind a paywall. Full working: `docs/group_05_build_contract.md` §10. |
| **VII** — hepatic | Nagtegaal 2019 is a seven-page overview of the **whole** digestive system, also with no abstract in PubMed. Paediatric liver tumours — hepatoblastoma above all — will be thinly covered. |
| **XI** — other epithelial and melanoma | Vol. 10 is **thyroid only**. The group also takes skin melanoma, adrenocortical carcinoma and carcinomas of other sites, each in a different volume. At least two further baselines are needed. |

**A structural question for groups IV–VII and X.** These are paediatric-site groups, and
**Pfister SM, et al. (Cancer Discovery 2022;12(2):331–355)** summarises the inaugural *WHO
Classification of Paediatric Tumours* — the volume written for exactly these tumours. It may be the
better spine for several of them, with the organ volume as the second source rather than the first.
That is the registrar's call and is not assumed here.

> **Closed for Group V, 22 September 2026 — and the way it closed is a warning for the rest.**
> Pfister 2022's complete full text was retrieved and searched: *eye*, *ocular* and *retina* appear
> nowhere in it, and *retinoblastoma* appears exactly once, inside a list of cancer predisposition
> syndromes. The paediatric volume reportedly has an *Eye tumours* chapter; its summary paper does
> not engage it. **Pfister's coverage is chapter-by-chapter and uneven**, and it is the group's
> baseline only where it actually discusses the group. Search the full text before assuming it for
> VI, VII or X — the volume name matching the group name proved nothing here.

> **Closed for Group VI the same day, the same way, and more starkly.** The same full text
> (PMC9401511) was searched for the renal vocabulary: **"kidney" appears zero times.** "Renal"
> appears 16 times, none of them opening a renal section; "Wilms" appears 6 times, all in passing —
> as the worked example of a blastoma, in the anaplasia criterion, and in the
> cancer-predisposition-syndrome groupings. There is no renal tumour section. **Pfister 2022 is not
> the spine for Group VI either**, and the structural question above can be treated as answered for
> two of the five paediatric-site groups: search the text, do not assume the volume.

### Two things to carry into the builds

**Group XI is only half covered.** Vol. 10 is thyroid. The group also takes skin melanomas,
carcinomas of other sites and adrenocortical carcinoma, which live in other volumes. Expect to add
a second and third baseline as that build reaches them.

**Group XII has no baseline and cannot have one.** It is the residual bucket, so verification there
runs code by code against whichever volume owns the entity, not against a single document.

---

## 1b. The second document: registry implications

A classification summary says which entities exist. It does **not** say what the classification
does to a registry — which distinct entities were forced to share one ICD-O code, which codes
became unusable, what a coder should do about it. For Group 3 that second document is:

> **Hoogendijk R, van der Lugt J, Hoving E, Kremer L, Visser O, Wesseling P, van Vuurden D,
> Karim-Kos H.** *The fifth edition of the WHO Classification of Tumors of the Central Nervous
> System: Implications for cancer registries.* Neuro-Oncology 2022;24(11):1811–1814.
> [10.1093/neuonc/noac176](https://doi.org/10.1093/neuonc/noac176) · PMID 35877072 · PMC9629428

Its Table 1 gave us the **thirteen ICD-O codes that carry more than one WHO CNS5 entity** — the
check that proved our `entity_annotation` layer covers all of them. A classification summary would
never have surfaced that.

### This genre is thin, and mostly does not exist per group

A PubMed sweep on 16 September 2026 found **no equivalent paper for any other volume**. Searches on
*"implications for cancer registries"*, *cancer registration* + WHO classification, and the articles
PubMed computes as similar to Hoogendijk returned classification reviews, radiology reviews and
registry-comparison studies — nothing that does for another volume what Hoogendijk does for CNS.

**Do not fabricate an equivalent.** When a group has none, say so and fall back on the layers below.

### What fills the role instead

**Cross-cutting — applies to all twelve groups, and is already in use:**

| Source | What it gives |
|---|---|
| IARC/IACR ICD-O-3.2 change documents — *Deleted codes and their terms*, *New codes and their terms*, *Terms that are changing behaviour*, *A summary of the main changes*, and the full 3.1→3.2 change listing | which numbers were retired, which terms moved, which behaviours changed. The primary registry-facing artefacts. |
| **Visser O, et al.** *2022 revised European recommendations for the coding of the basis of diagnosis of cancer cases in population-based cancer registries.* Front Oncol 2023;13:1250549. [10.3389/fonc.2023.1250549](https://doi.org/10.3389/fonc.2023.1250549) — **in this repo**, `docs/references/Visser-2023-ENCR-basis-of-diagnosis.pdf`, key points extracted in [`docs/references/visser-2023-key-points.md`](references/visser-2023-key-points.md) | the ENCR basis-of-diagnosis vocabulary every terminal emits, and — Tables 3 and 4 — **which specific morphology code a registry may assign when no pathology exists**. Applies to every group, not just Group 3. Moved out of `Group 3 Papers/` on 16 Sep 2026 for that reason. |
| A national registry coding table keyed to the classification **and** to ICD-O-3.2 — e.g. the Belgian Cancer Registry's CNS5 table | per-entity code assignments, and the footnotes that reveal terminology-versus-number changes. Corroboration only. |

**Per group, where something exists:**

| Group | Registry-implications source |
|---|---|
| **III** — CNS | Hoogendijk 2022, above ✅ |
| **VI** — renal | **None exists and none is needed** ✅ — the classification summary and the registry-implications document are the same paper. **Moch 2022's Table 1, *"ICD-O coding of tumours of the kidney"*, prints the ICD-O-3.2 code against every WHO 2022 renal entity**, which is precisely what Hoogendijk's Table 1 does for CNS. It is what established that `8311/3` carries seven entities, `8510/3` four, `8316/3` two, and that `8959/3` carries none at all. A PubMed MeSH sweep for a Hoogendijk equivalent (recorded in `Group 6 Papers/Group 6 — Registry-Implications MeSH Search Results.md`) returned nine records and no candidate, and that is the correct result rather than a gap. |
| **I, II** — haematolymphoid | No registry paper. The equivalent problem is **two competing classifications published in 2022**: WHO-HAEM5 and the **International Consensus Classification**. Compared in **Falini B & Martelli MP.** *Comparison of the International Consensus and 5th WHO edition classifications of adult myelodysplastic syndromes and acute myeloid leukemia.* Am J Hematol 2023;98(3):481–492. [10.1002/ajh.26812](https://doi.org/10.1002/ajh.26812) · PMID 36606297 — and for myelodysplastic syndromes specifically **Hasserjian RP, et al.** Virchows Arch 2023;482(1):39–51. [10.1007/s00428-022-03417-1](https://doi.org/10.1007/s00428-022-03417-1) · PMID 36287260 |
| **IV–XII** | **None found.** Use the cross-cutting layer. |

> ⚠️ **A question this raises about work already done.** Groups 1 and 2 are built. They were built
> against WHO-HAEM5. The International Consensus Classification is a *second* 2022 classification
> of the same diseases, and the two disagree on entity definitions — which classification the
> registry codes to is a registrar's decision that does not appear to have been recorded. Worth
> checking before Group 4 starts.

---

## 2. Code verification — two sources, in this order

Currency is settled from **ICD-O-3.2 itself** and **the WHO classification the entity belongs to**.
A registry grouping table corroborates; it never decides.

1. **`icdo32.sqlite`, the `obs` column.** It marks a **term string**, never a retired code. 40
   code/behaviour pairs carry `[obs]` and non-`[obs]` terms at the same time.
2. **IARC's *Deleted codes and their terms*** (IACR, 9 October 2020) — where a retired **number**
   is actually recorded, and where `[obs]` can be seen sitting on synonyms under live codes.
3. **The 3.1 → 3.2 change listing** — shows whether ICD-O-3.2 touched the code at all. It has no
   status meaning "made obsolete"; that marker is inherited.
4. **The group's WHO baseline document** — does a current entity live on this stem?
5. **A national registry coding table keyed to ICD-O-3.2** — corroboration only. Its inclusions may
   be legacy: a registry keeps codes alive because it already holds cases on them, and this
   registry began operating in 2025.

### The test

> **A code leaves the decision tree only when no current WHO entity lives on its stem** — not
> merely because ICD-O-3.2 prints no usable term.

Applying the weaker test wrongly removed `9430/3` Astroblastoma and `9480/3` from Group 3. Both
carry current WHO CNS5 entities and both were restored. See `docs/group_03_obsolete_terms.md`.

---

## 3. Which skill to load, and when

| Situation | Skill |
|---|---|
| First command of a new group pathway build | `superpowers:subagent-driven-development` |
| Morphology codes conflict, or a code's destination is undetermined | `superpowers:brainstorming` — **immediately**, before proposing a fix |
| A bug, a failing check, unexpected behaviour | `superpowers:systematic-debugging` |

Brainstorming is loaded *before* a fix is proposed, not after one fails. The `9535/0` and
DICER1-sarcoma decisions both changed materially once the question was opened properly.

---

## 4. Proof before a group is called done

Green build is necessary and not sufficient.

1. `python3 build/build_database.py` → **0 FAIL**.
2. `python3 build/induce_flow.py` → every rule in every checklist has a witness.
3. **Negative controls** on every new check — break the data deliberately and confirm the check
   catches it. A check nobody has broken is not known to work.
4. **Drive the changed branches in the browser.** The two Group 3 defects that mattered most were
   invisible to the build: a `confidence_ceiling` flooring a molecularly confirmed case at low, and
   a resource-level gate telling the clerk a test was unavailable when they had just recorded its
   result.
5. Confirm previously built groups are **byte-identical to `main`**.

---

*Written 16 September 2026, from the Group 3 build. Baseline documents for groups 1, 2, 8 and 9
retrieved via PubMed; groups 4, 5, 6, 7, 10, 11 and 12 were outstanding and flagged to the
registrar.*

*Updated 22 September 2026 on the Group VI branch. Moch 2022 is now held on disk and is confirmed
as both the classification summary and the registry-implications document for Group VI — the only
group so far where one paper does both jobs. Pfister 2022 is ruled out as the spine for Group VI as
it was for Group V, on the same evidence: its full text does not discuss the organ.*
