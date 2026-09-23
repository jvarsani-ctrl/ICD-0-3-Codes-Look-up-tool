# Papers for the registrar to review

**16 September 2026, Group IV build.** Not a fetch list — everything here is **on disk now**.
These are the papers where your reading changes a decision, ordered by what it changes.

---

## The finding that shapes this list

**Of the eighteen PDFs in `Group 4 Papers/`, exactly one has been read in this build** — Mete 2022,
the full text you supplied. The other seventeen have not been opened by anyone during the Group IV
work. Everything the build currently believes about them comes from
`ICD Look Up tool/Group 4 — Neuroblastoma Diagnostic Pathway.md`, which summarises them.

**That document has six documented false statements** (build contract §0): its eight "schema
challenges" are four problems Group 3 already solved and four non-problems; it lists `8683` as a
codeable Group IV entity when ICD-O-3.2 carries it at `/0` only; it prints four ICD-O-3.2 preferred
terms that do not exist; it calls `9520`, `9521` and `9523` "older synonyms" of `9522` when each is
its own stem; and it prints a four-stage Kadish table when Kadish defines three.

None of those six is a *clinical* error — they are coding and schema errors. But a document with six
known faults is not a safe proxy for nine papers nobody has opened.

---

## Tier 1 — read these; they decide a code

### 1. Shimada H, et al. *Terminology and Morphologic Criteria of Neuroblastic Tumors.* Cancer 1999;86(2):349–63 · **15 pages, on disk**
`Cancer - 2000 - Shimada - Terminology and morphologic criteria of neuroblastic tumors.pdf`

### 2. Peuchmaur M, et al. *Revision of the International Neuroblastoma Pathology Classification.* Cancer 2003;98(10):2274–81 · **8 pages, on disk**
`Cancer - 2003 - Peuchmaur - Revision of the International Neuroblastoma Pathology Classification.pdf`

**What they decide: the single most load-bearing clinical distinction in Group IV — `9490`
Ganglioneuroblastoma versus `9500` Neuroblastoma, NOS.** These two codes are IVa, they are the
group's commonest diagnoses, and nothing separates them but the International Neuroblastoma
Pathology Committee's assessment of Schwannian stromal content on the H&E. Tree A's
`histology_subclassification` node is built directly on that assessment.

**What to check specifically:**
- The four INPC categories and their exact names — neuroblastoma (Schwannian stroma-poor),
  ganglioneuroblastoma intermixed (stroma-rich), ganglioneuroma (stroma-dominant),
  ganglioneuroblastoma nodular (composite).
- **The stroma-dominant category is where ruling D1 bites.** Ganglioneuroma, maturing and mature,
  is `9490/0` — benign, outside ICCC-3 Group IV's `3`-only behaviour declaration, and the branch
  that reaches it emits **no code** via the new `behaviour_exclusion` field. Confirm that reading
  against Shimada's own definition before the tree is written.
- Whether "ganglioneuroblastoma, nodular" being a **composite** tumour changes what a registry
  should code when both components are present.
- Peuchmaur's favourable and unfavourable subsets of nodular ganglioneuroblastoma.

**Corroboration already held:** Mete 2022 Table 1, p. 108, reproduces the INPC classification in
full and attributes it to Shimada 1999. Two witnesses agreeing is why this is Tier 1 and not
blocking — but the tool will code cases on this, and you are the registrar.

### 3. Mete O, et al. *Overview of the 2022 WHO Classification of Paragangliomas and Pheochromocytomas.* Endocrine Pathology 2022;33(1):90–114 · **25 pages, on disk — you supplied it**
`s12022-022-09704-6.pdf` · [DOI](https://doi.org/10.1007/s12022-022-09704-6)

Read in full. Three passages worth your own eye:

- **p. 94 — the CoGNET rename.** *"The entity previously known as gangliocytic para-ganglioma has
  been renamed composite gangliocytoma/neuroma and neuroendocrine tumor (CoGNET)."* This is one of
  the two legs removing `8683` from the group and retiring `iv_morph` pick 9. The paper gives
  CoGNET **no ICD-O code** and never mentions `8683`, which is why a record on pick 9 currently has
  no automatic destination.
- **p. 100 — the edition.** *"Prior to the 2017 WHO classification (also known the 4th edition),
  PPGLs… were accompanied by the adjectives 'benign' or 'malignant'."* The **4th** edition, not the
  5th. Worth confirming, because the repair package now states it without hedging.
- **p. 108 — Table 1, the INPC table.** The corroboration for items 1 and 2 above.

**And one absence worth your judgement.** PHOX2B appears twice in 25 pages, both under the
*neuroblastoma* differential. **WHO's recommended paraganglioma panel does not include it** — it is
INSM1, synaptophysin and chromogranin, keratins negative, then GATA3, tyrosine hydroxylase,
dopamine β-hydroxylase and choline acetyltransferase. Our pathway document builds Tree B's
differential on PHOX2B being positive in 97.2% of paragangliomas, sourced to Manethova 2023 alone.
The two are not in conflict — a marker can be sensitive without being recommended — but the tree
should not imply WHO endorses it, and **GATA3, not PHOX2B, is what separates paraganglioma from
neuroblastoma at the adrenal.**

---

## Tier 2 — read if you want the tree to say more than it currently will

### 4. Ma Y, et al. *PHOX2B as a Reliable Marker for Neuroblastoma in Tissue and Cytology Specimens.* Journal of Neuropathology and Experimental Neurology 2021;80(12):1108–16 · **9 pages, on disk**
`nlab112.pdf`

The source for the 100% sensitivity / 97.6% specificity figures the pathway document quotes for
PHOX2B in neuroblastoma. **Directly in tension with item 3's absence.** If PHOX2B is that good for
neuroblastoma but absent from WHO's paraganglioma panel, the two tumours are separated by GATA3 and
the sustentacular pattern, not by PHOX2B — which is what the build contract §5.1 already says, and
what Tree A's IHC node will be written on.

### 5. Manethova M, et al. *Phox2B is a sensitive and reliable marker of paraganglioma.* Virchows Archiv 2023;482(4):679–86 · **8 pages, on disk**
`s00428-023-03490-0.pdf`

The **sole** source for two claims the tool would otherwise make: PHOX2B positive in 97.2% of
paragangliomas, and PHOX2B positive in only 1 of 6 olfactory neuroblastomas. The second is why the
sinonasal tree must not use PHOX2B to rule anything out. A single paper carrying two load-bearing
claims is worth one read.

### 6. Bashyal R, et al. *Role of immunohistochemistry in the diagnosis of malignant small round cell tumors.* Journal of Pathology of Nepal 2011;1:87–91 · **5 pages, on disk**
`admin,+5398-18934-1-CE.pdf`

### 7. Mudassar M, et al. *Sub-categorization of Pediatric Small Round Blue Cell Tumors using Immunohistochemistry.* Journal of Rawalpindi Medical College 2022;26(3):480–486 · **7 pages, on disk**
`1921-Article+Text-7209-1-10-20221013.pdf`

**Read these two together.** Item 6 is currently the *sole* source for Tree A step 4 — the small
round blue cell tumour differential separating neuroblastoma from Ewing sarcoma, rhabdomyosarcoma,
lymphoma, Wilms tumour and desmoplastic small round cell tumour. It is five pages in a national
journal.

**Item 7 was found sitting in the folder, listed nowhere** — not in `Cancer IV Neuroblastoma
sources.md`, not in the pathway document's references. It is a second, independent, more recent
immunohistochemistry series on the same differential. **Your decision: adopt it as a Tree A source
or not.** If yes it should be added to the sources file with the rest.

### 8. Visser O, et al. *2022 revised European recommendations for the coding of the basis of diagnosis.* Frontiers in Oncology 2023;13:1250549 · **on disk, key points extracted**
`ICD-Lookup/docs/references/Visser-2023-ENCR-basis-of-diagnosis.pdf`

**Table 4, p. 06** names two Group IV entities directly and they are the only two codes this group
may assign with no pathology at all:

| Entity | Marker | Morphology | Basis |
|---|---|---|---|
| Neuroblastoma | homovanillic acid, vanillylmandelic acid | `9500/3` | **4** |
| Phaeochromocytoma | catecholamines, chromogranin A | `8700/3` | **4** |

Two things for you. **Rule 6, p. 05 — basis 4 never stands alone**, so the imaging node must require
both the marker and the imaging. And **Visser's own table puts phaeochromocytoma in Group XI**;
ICCC-2017 puts `8700` in IVb. ICCC-2017 is Layer 1 and governs, so the build ignores Visser's
grouping — but you should know the two disagree.

---

## Tier 3 — read only if a specific branch looks wrong later

On disk, unread, each the sole source for one section of the pathway document: **Okamatsu 2009**
(`nihms123021.pdf`, ganglioneuroma and ganglioneuroblastoma clinicopathology) · **Sano H, et al.
2005** (`j.ejca.2005.11.031.pdf`, INPC prognostic value) · **Verly 2017**
(`j.ejca.2016.12.002.pdf`, the catecholamine panel sensitivities) · **Monclair 2009**
(`JCO.2008.16.6876.pdf`, INRG staging and image-defined risk factors) · **Ambros PF 2009**
(`sj.bjc.6605014.pdf`, MYCN and molecular consensus) · **Nakagawara 2018** (`jjco%2Fhyx176.pdf`,
28-page neuroblastoma review) · **Bausch 2017** (`jamaoncol.2017.0223.pdf`, SDHx genetics) ·
**Testa 2013** · **Maignan 2017** (SDHB immunohistochemistry) · **Shuangshoti 1986**
(`bjo.70.7.543.pdf`, the single peripheral medulloepithelioma case report) · **Stathopoulos 2020**
(`s12886-020-01512-y.pdf`, ciliary body medulloepithelioma — Group V, not IV).

None of these decides a code. They set what a node may *ask*, not what it may emit.

---

## Two citation errors to rule on

1. **`Cancer IV Neuroblastoma sources.md` and the pathway document's reference 4** both attribute
   the European Journal of Cancer 2005 INPC paper to *"Ambros et al."* **The first author is
   Sano H.** Ambros is further down the list. The PDF on disk confirms it.
2. **The pathway document's Kadish table has four stages under Kadish's name.** Kadish S, Goodman M,
   Wang CC, Cancer 1976;37(3):1571–6 defines **three**, A to C, in its own abstract. Stage D is
   Morita A, et al., Neurosurgery 1993;32(5):706–14. The four-stage system is **Kadish-Morita**.

---

*Everything above is on disk. The separate list of what the registry does not hold is
`docs/sources-requested.md`.*
