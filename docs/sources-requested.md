# Sources requested from the registrar

**16 September 2026, from the Group IV build.** What the registry does not hold, what each would
settle, and what it costs to go without. Ordered by what it changes, not by how hard it is to get.

**Nothing here blocks the Group IV build.** Every item below is either a corroborating second
source or a question the build has already answered conservatively. The cost of going without is
that the tool says less, or that a note reads "not established" where it could read a fact.

---

> ## ✅ Update, 18 September 2026 — the registrar supplied most of this
>
> **Closed:** the **IARC ICD-O-3.2 change documents** (item 1, the highest-value item and
> cross-cutting for all twelve groups) are now at `ICD coding/ICD-O-3.2/` — *Deleted codes and
> their terms*, *New codes and their terms*, *Terms that are changing behaviour*, *Summary of main
> changes*, plus the ICD-O-3.2 multiple-primaries workbook. **Pfister Supplementary Table S3**
> (item 2) is at `Group 4 Papers/6549397/cd-21-1094_supp3.xlsx`, with the full paper at `331.pdf`.
> **Agarwal 2023** (item 4) and **Di Stasio 2022** (item 6) are both held.
>
> **Substituted:** WHO Blue Book volume 10 (item 3) is not freely available. The registrar supplied
> **Juhlin CC.** *The road ahead: a brief guide to navigating the 2022 WHO classification of
> endocrine and neuroendocrine tumours.* Journal of Clinical Pathology 2025;78:1–10.
> [10.1136/jcp-2023-209060](https://doi.org/10.1136/jcp-2023-209060) — `1.full.pdf` — in its place.
>
> **Ruled out by the registrar, do not pursue:** the **Hyams AFIP fascicle** (item 5) and
> **Bradová 2026** (item 7). **Veyrat 2020** (item 8) was already demoted.
>
> **What the new documents settled immediately**, before any of the papers were read:
>
> - IARC's *Summary of main changes*: *"In the 3-digit group 868–870 the only remaining
>   non-malignant term is under 8683/0."* `8683/0` is IARC's **deliberate** single survivor of that
>   block — third confirmation for build contract §0.2.
> - IARC's *Summary of main changes*: *"Ewing sarcoma (9260/3) has moved to, and is now the
>   preferred term for, 9364/3 (peripheral neuroectodermal tumour)."* Ruling **D4** in IARC's own
>   words.
> - IARC's *Deleted codes and their terms* carries the whole paraganglioma block —
>   `8680/0 Paraganglioma, benign  Deleted`, `8680/1 … Moved to /3`, and the same for `8681`,
>   `8682`, `8690`, `8691`, `8692`, `8693`, `8700`. The REDCap repair package now cites deletions
>   rather than inferring from absent strings.
> - **Supplementary Table S3** gives the WHO entity list for both halves of Group IV, reproducing
>   the International Neuroblastoma Pathology Committee's four categories unaltered. Extracted at
>   `Group 4 Papers/Pfister-2022-supplementary-table-S3-key-points.md`.
>
> **What is still open:** CoGNET's ICD-O code and the fate of the number `8683` — pending the
> Juhlin 2025 read.

---

## Tier 1 — would change the build

### 1. The IARC ICD-O-3.2 change documents · **no DOI — IARC/IACR website** · ★ highest value

Five documents, published alongside the ICD-O-3.2 morphology table by the International Agency for
Research on Cancer:

- *Deleted codes and their terms*
- *New codes and their terms*
- *Terms that are changing behaviour*
- *A summary of the main changes*
- the full ICD-O-3.1 → ICD-O-3.2 change listing

**Why this is first.** `docs/group_baseline_documents.md` §2 names these as steps **2 and 3** of the
two-source code-verification chain that every group build is required to follow, and calls them
*"the primary registry-facing artefacts"*. **They are not on disk.** `ICD coding/ICD-O-3.2/` holds
the 2019 draft workbook, the 9 October 2020 final workbook, and the SQLite conversion — nothing
else. Verified 16 September 2026.

So every code-currency finding in Groups 1 through 4 rests on steps 1, 4 and 5 of a five-step
chain. In practice that has been enough, because the `obs` column and the WHO volumes agreed. It
will not always be.

**This is cross-cutting — it affects all twelve groups, not Group IV.** It is the single most
valuable thing on this list.

**What it would settle for Group IV specifically:** whether IARC ever formally retired the number
`8683`, and whether `9520`, `9521` and `9523` were touched between ICD-O-3.1 and 3.2. Both are
currently inferred from the absence of an `[obs]` marker, which is weaker evidence than a change
listing.

### 2. WHO Classification of Paediatric Tumours, 1st edition — IARC Blue Book, volume 7

Or, failing the volume, **Supplementary Table S3** of its summary paper:

> Pfister SM, et al. *A Summary of the Inaugural WHO Classification of Pediatric Tumors:
> Transitioning from the Optical into the Molecular Era.* Cancer Discovery 2022;12(2):331–355.
> PMID 34921008 · PMC9401511 · [DOI](https://doi.org/10.1158/2159-8290.CD-21-1094)

**The paper is held and has been read.** Its entire treatment of peripheral neuroblastic tumours is
one paragraph, which defers the classification and molecular detail to Supplementary Table S3 —
and that table could not be retrieved. Ganglioneuroblastoma and ganglioneuroma are never named;
paraganglioma and pheochromocytoma are never mentioned; no ICD-O code appears anywhere.

**What it would settle:** the WHO entity list for the neuroblastic tumours, which is Group IVa's
whole content. Mitigated for now — Mete 2022 Table 1 (p. 108) reproduces the International
Neuroblastoma Pathology Committee classification in full, which is what the Tree A node actually
needs. So this is corroboration, not a blocker.

### 3. WHO Classification of Endocrine and Neuroendocrine Tumours, 5th edition — IARC Blue Book, volume 10

**What it would settle:** the ICD-O code for **CoGNET** (composite gangliocytoma/neuroma and
neuroendocrine tumour), and what becomes of the number **8683**.

Mete 2022's full text is held and read. It states the rename — *"the lesion known as gangliocytic
paraganglioma has been renamed composite gangliocytoma/neuroma and neuroendocrine tumor
(CoGNET)"* — but gives **no ICD-O code for any entity in 25 pages**, and never mentions `8683`.
Only the Blue Book itself carries the codes.

**Why it matters practically:** `Group 4 — Layer 1 Repair Package (REDCap iv_morph).md` retires
`iv_morph` pick 9 and tells whoever applies it that a record sitting there has *"no automatic
destination"*. That is honest and unhelpful. This volume would give it one.

---

## Tier 2 — would strengthen a branch, or close a documented gap

### 4. Agarwal A, et al. *Update from the 5th Edition of the WHO Classification of Nasal, Paranasal, and Skull Base Tumors.* AJNR 2023;44(10):1116–1125
PMID 37591773 · PMC10549938 · [DOI](https://doi.org/10.3174/ajnr.A7960)

Imaging overview with histopathologic and genetic correlation. Partly superseded — see *Already
closed* below — but it is the other WHO-5th-edition sinonasal review and would corroborate.

### 5. Hyams VJ. "Olfactory neuroblastoma", in *Tumors of the Upper Respiratory Tract and Ear*, Atlas of Tumor Pathology, 2nd series, Fascicle 25. Armed Forces Institute of Pathology, 1988, pp. 240–248
**No DOI. No PMID. Not indexed by PubMed.** A book fascicle.

The primary source for Hyams grading. Every paper that says "Hyams grade" cites this book.
**Largely mitigated** — Gargano 2025 reproduces the original criteria table and it is now
transcribed (see *Already closed*). Worth having only if the registry ever wants to grade rather
than record a grade, which on current evidence it should not.

### 6. Di Stasio GD, et al. *Tailored Molecular Imaging of Pheochromocytoma and Paraganglioma.* Neuroendocrinology 2022;112(10):927–945
[DOI](https://doi.org/10.1159/000522089)

Cited nine times in the Group IV pathway document as the source for the whole functional-imaging
section of Tree B — MIBG, FDOPA, DOTATATE sensitivities, and the biochemical-phenotype-to-genetic-
cluster mapping. **Only a `.md` note is on disk, not the paper.** Tree B's imaging node will be
built from that note unless the paper arrives.

### 7. Bradová M, Laco J, Skálová A. *News in the 5th edition of the WHO Classification of Tumours of the Head and Neck: Tumours of the Sinonasal Tract and Skull Base Tumors.* Československá patologie 2026;62(2):87–95
PMID 42472341 · **PubMed returns no DOI** (`pii 144083`)

Covers all 24 sinonasal entities. Lower priority now that Rooper 2023 is held.

### 8. Veyrat M, et al. *Olfactory Neuroblastoma.* Advances in Oto-Rhino-Laryngology 2020;84:154–167
PMID 32731231 · [DOI](https://doi.org/10.1159/000457935)

**Demoted — do not spend effort on this.** Its abstract is now held and shows it to be a clinical
management review: it names Kadish and Hyams as *"two complementary classifications"* but the
grading and staging criteria themselves came from elsewhere, and Gargano 2025 has them. It was
originally requested because the pathway document cited it; that citation was aspirational.

---

## Already closed — do not chase these

| Question | Settled by | How |
|---|---|---|
| Does WHO recognise olfactory neurocytoma (`9521`), olfactory neurogenic tumour (`9520`) or olfactory neuroepithelioma (`9523`) as entities? | **Rooper LM.** Head and Neck Pathology 2023;17(2):299–312. PMC10293143 · [DOI](https://doi.org/10.1007/s12105-023-01548-8) | Read in full from PubMed Central. In 57,027 characters about WHO-5th-edition sinonasal neuroectodermal tumours: `neurocytoma` **0** occurrences, `neurogenic` **0**, `neuroepithelioma` only in reference titles. WHO recognises one entity, olfactory neuroblastoma. Corroborates ruling D3 on evidence. |
| The original Hyams grading criteria, grades I–IV | **Gargano SM, et al.** Head and Neck Pathology 2025;19(1):92. PMC12307849 · [DOI](https://doi.org/10.1007/s12105-025-01804-z) | Table 1 read with its HTML column structure intact. Transcribed in `Group 4 Papers/Gargano-2025-hyams-grading-TABLE-key-points.md`. |
| Kadish staging | **Kadish S, Goodman M, Wang CC.** Cancer 1976;37(3):1571–6. PMID 1260676 · [DOI](https://doi.org/10.1002/1097-0142\(197603\)37:3%3C1571::aid-cncr2820370347%3E3.0.co;2-l) | Criteria are in the abstract. **Three stages, A–C.** Stage D is **Morita A, et al.** Neurosurgery 1993;32(5):706–14, PMID 8492845 · [DOI](https://doi.org/10.1227/00006123-199305000-00002). |
| Which WHO edition abolished the paraganglioma benign/malignant split | **Mete O, et al.** Endocrine Pathology 2022;33(1):90–114 · [DOI](https://doi.org/10.1007/s12022-022-09704-6) | Full text supplied by the registrar. The **4th edition, 2017**, p. 100. |
| Is "peripheral PNET" code `9503` or `9364`? | ICD-O-3.2 itself | Verified in both the 2019 draft and the 2020 final workbook. `9364/3`. Ruling D4. |

---

## Group 6 — Renal Tumours, requested 22 September 2026

Two designated imaging papers, named in the Group 6 build contract §4.2 and the papers index as
the sources for this group's imaging content, and **neither is on disk**.

### 9. Chung EM, Graeber AR, Conran RM. *Renal Tumors of Childhood: Radiologic-Pathologic Correlation Part 1. The 1st Decade.* RadioGraphics 2016;36(2):499–522
[DOI](https://doi.org/10.1148/rg.2016150230)

### 10. Chung EM, Lattin GE Jr, Fagen KE, et al. *Renal Tumors of Childhood: Radiologic-Pathologic Correlation Part 2. The 2nd Decade.* RadioGraphics 2017;37(5):1538–1558
[DOI](https://doi.org/10.1148/rg.2017160189)

**What they would settle.** These two papers are the designated sources for two separate parts of
the Group VI build: the imaging-sufficient branch on `8960/3` Nephroblastoma, NOS — the claw sign
separating an intrarenal Wilms tumour from an extrarenal, vessel-encasing neuroblastoma, and the
large, well-demarcated, displacing mass pattern in a child under five — and the imaging
discriminators used to divert a case off the imaging route toward tissue, including the renal cell
carcinoma pattern that becomes more likely from the second decade on.

**What it costs to go without them.** `imaging_sufficient` is built on `8960/3` regardless, because
Visser 2023 Table 3 (build contract §0.11) already establishes that nephroblastoma is registrable
at basis 2, imaging, and that finding does not depend on either Chung paper. But the specific
imaging features written into `imaging_features` rest on Spreafico F, et al. *Wilms tumour.* Nature
Reviews Disease Primers 2021;7:75 and the papers index, rather than on a dedicated
radiology–pathology correlation source. Spreafico is a clinical review with a paragraph on imaging,
not an imaging paper; a dedicated source would let those features be cited with the same precision
the rest of the imaging-pathway node has, and would corroborate — or correct — the diversion
criteria in build contract §4.2 rather than leaving them resting on a single non-imaging review.

---

## One paper already on disk that nobody listed

**Mudassar M, et al.** *Sub-categorization of Pediatric Small Round Blue Cell Tumors using
Immunohistochemistry.* Journal of Rawalpindi Medical College 2022;26(3):480–486. Held at
`Group 4 Papers/1921-Article+Text-7209-1-10-20221013.pdf`, seven pages, full text.

It appears in neither `Cancer IV Neuroblastoma sources.md` nor the pathway document's reference
list. Found by extracting the title page of every PDF in the folder rather than trusting filenames.
Directly relevant to Tree A step 4, the small round blue cell tumour differential, which is
currently sourced to Bashyal 2011 alone — a five-page paper in the *Journal of Pathology of Nepal*.
A second independent immunohistochemistry series on the same differential, and more recent.

**Also a citation error to correct:** `Cancer IV Neuroblastoma sources.md` and the pathway
document's reference 4 both attribute the European Journal of Cancer 2005 International
Neuroblastoma Pathology Classification paper to "Ambros et al." The first author is **Sano H**;
Ambros is further down the list.

---

*Citations resolved against PubMed, 16 September 2026.*
