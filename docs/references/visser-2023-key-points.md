# Visser 2023 — the ENCR basis of diagnosis, and what it settles for this tool

> **Visser O, Kościańska B, Caetano dos Santos FL, Cuccaro F, Forjaz G, Michalek IM, Mousavi M,
> Sulkowska U, Martos C, Giusti F.** *2022 revised European recommendations for the coding of the
> basis of diagnosis of cancer cases in population-based cancer registries.*
> Frontiers in Oncology 2023;13:1250549. [10.3389/fonc.2023.1250549](https://doi.org/10.3389/fonc.2023.1250549)
> · PDF held at [`Visser-2023-ENCR-basis-of-diagnosis.pdf`](Visser-2023-ENCR-basis-of-diagnosis.pdf) · CC BY.

**A cross-cutting source. It applies to all twelve groups, not to Group 3.** It is the authority
for the `basis_of_diagnosis` value every terminal emits, and its Tables 3 and 4 are the authority
for which specific morphology code a registry may assign **when no pathology exists** — the
question the tool's imaging and resource-level branches exist to answer.

Page references are to the printed page numbers in the PDF (01–07).

---

## 1. The scale, and why 3 and 6 are absent

Table 1, p. 03. The valid set is **`{0, 1, 2, 4, 5, 7, 8, 9}`**.

| Code | Means | Note |
|---|---|---|
| 0 | Death certificate only | trace-back not possible |
| 1 | Clinical | diagnosed before death with none of 2–8 — **physical examination only** |
| 2 | Clinical investigation | imaging, endoscopy, ultrasound, exploratory surgery, autopsy — **without a tissue diagnosis** |
| 4 | Specific tumour markers | biochemical or immunologic, specific to a site |
| 5 | Cytology | cells from primary or secondary site; peripheral blood and bone marrow **aspirates**; **immunophenotyping by flow cytometry**; **liquid biopsy** |
| 7 | Histology | tissue from primary or metastasis, however obtained, **including bone marrow biopsies** and autopsy specimens |
| 8 | Cytogenetic and/or molecular testing | karyotyping, fluorescent in situ hybridization, polymerase chain reaction, DNA sequencing |
| 9 | Unknown | |

**Code 6 was abolished by this revision** (p. 02). The old code 6, histology of a metastasis, was
merged into code 7, which now covers histology of the primary tumour, of a metastasis, and at
autopsy. **Code 3 has never existed** in the ENCR scale.

**Code 8 is new in this revision** (p. 02). It did not exist in the 1999 recommendations.

Codes **7.1** histology of the primary, **7.2** histology of a metastasis, **7.3** histology at
autopsy are **optional** sub-codes (Table 2, p. 03; rule 9, p. 06). They carry equal diagnostic
certainty and exist for staging and cross-checks — 7.2 implies metastatic disease. Not required
for international comparison. **The tool emits none of them.**

**In force for incident cases from 1 January 2023.** This registry began operating in 2025, so the
2022 revision governs every case it holds. There is no transitional period to model.

## 2. The rules that bind the tool

**Rule 1, p. 03 — take the highest code in 1–8.** The order 1→8 is increasing reliability.
`0` and `9` override the range. This is exactly what the contract computes.

**Rule 4, p. 03 — "possible" is not registrable.** Codes 1 and 2 may be used when cancer is *at
least likely* ("probably cancer"). If clinical investigation makes cancer only *possible*, or if a
non-malignant disorder could equally explain the findings, **the case is not registered at all**
in the absence of pathology. The paper's own example is a cerebellar lesion whose differential
includes an arterial malformation.

**Rule 5, p. 03 — basis 1 or 2 means morphology `8000/3`,** with a CNS exception: **`8000/0` and
`8000/1` are also allowed for benign and borderline central nervous system tumours.** Table 3 lists
the exceptions where a specific code may be used instead, and only when that specific diagnosis is
at least likely. Worked examples, p. 03: *"lesion in the frontal lobe, typical for glioblastoma"*
→ `9440/3` with basis 2; *"low-grade lesion in the temporal lobe; differential diagnosis
dysembryoplastic neuroepithelial tumour, ganglioglioma, low-grade astrocytoma"* → `8000/1`.

**Rule 6, p. 05 — code 4 never stands alone.** Tumour markers rise without cancer, so basis 4 must
always accompany a clinical diagnosis or a clinical investigation showing cancer.

**Rule 7, p. 06 — flow cytometry is 5, not 7.** It uses a cell suspension, so it codes as cytology,
even though it is an immunophenotyping method. This is the one that will bite Groups I and II.

**Rule 8, p. 06 — a liquid biopsy is 5, not 8,** even when it finds a cancer-specific genetic
abnormality, as long as no pathology is available. Molecular method, cytology code.

**Rule 10, p. 06 — basis 8 only when the abnormality is specific to that cancer.** Most tumours
carry genetic abnormalities; few are diagnostic. Basis 8 covers **both** an abnormality being
present and an entity defined by its absence. The paper expects 8 to be a temporary device: it
exists "until specific morphology codes are available for cancer entities defined by genetic
abnormalities", and **basis 7 is correct where molecular testing was simply not performed.**

## 3. What it confirms about the build, and what it does not

**Confirmed, against `docs/group_03_build_contract.md` §2(5):**

- The valid set `{0, 1, 2, 4, 5, 7, 8, 9}`, and that 3 and 6 are not values in it — rule 10 in
  `build/build_database.py` and negative controls 52 and 53.
- Highest of 1–8, with 0 and 9 overriding — rule 1.
- Flow cytometry and liquid biopsy at **5**, not 8 — rules 7 and 8. The contract already says this.
- **No Group III terminal may emit basis 1.** Verified directly against Table 3: every one of the
  forty-three central nervous system rows is basis **2**. The only rows carrying basis 1 are
  melanoma of the skin, melanoma of the eye, retinoblastoma, angiosarcoma of the irradiated breast
  and Kaposi sarcoma of the skin — none of them Group III. Group 3 currently emits
  `{0: 4, 2: 68, 4: 2, 5: 29, 7: 352, 8: 54, 9: 11}`; no 1, no 3, no 6.

**Declared by us, not stated by the paper — two gaps:**

- **`ihc_counts_as: 7`** is sound. Immunohistochemistry is performed on tissue sections, and
  Table 1 puts tissue at 7. The boundary is rule 7: immunophenotyping **by flow cytometry** is 5.
  The distinction is the specimen, not the antibody.
- **`methylation_counts_as: 8` is an extension by analogy, and should stay declared.** Code 8's
  named techniques are karyotyping, fluorescent in situ hybridization, polymerase chain reaction
  and DNA sequencing. **DNA methylation profiling is not among them**, and methylation is
  epigenetic rather than a genetic abnormality. Rule 10's own test — is the finding specific to
  that cancer? — supports 8 for a defining methylation class, and nothing else in the scale fits.
  But the paper does not say it, so the contract is right to declare it rather than cite it.

## 4. One error in the paper — do not inherit it

Rule 10, p. 06, gives *"glioblastoma IDH wild type is 9445/3"*. **ICD-O-3.2 says otherwise.**
Queried against `ICD coding/ICD-O-3.2/icdo32.sqlite`:

| Code | ICD-O-3.2 |
|---|---|
| `9440/3` | Glioblastoma, NOS — *Glioblastoma, IDH-wildtype* is a **related term under this code** |
| `9445/3` | **Glioblastoma, IDH-mutant** (preferred term) |

The paper has the two reversed. The example is incidental to its argument — it is illustrating
that basis 8 applies to an entity defined by the *absence* of an abnormality — and the argument
stands. The code does not.

**This is the trap the project already knows.** Visser 2023 is authority for the basis-of-diagnosis
vocabulary. It is **not** a morphology source, and a registry recommendation paper does not
override ICD-O-3.2 on a code. See `memory/cbtrus-groupings-not-a-code-currency-source.md`.

Second reading trap, Table 3: codes written `9380/39`, `9380/32`, `9400/32`, `9401/33`, `9450/39`,
`9451/33` are **behaviour digit plus ICD-O grade digit**, not five-digit ICD-O-4 codes. `9400/32`
is `9400/3` at grade 2, low-grade astrocytoma. Nothing here is ICD-O-4
(`memory/tool-codes-icdo32-not-icdo4.md`).

## 5. Why this matters to groups 4–12 — Tables 3 and 4

These two tables are the reason this paper belongs to the whole tool. They answer, per entity,
*may a registry assign this specific morphology code with no pathology at all?*

**Table 3, pp. 04–05 — specific morphology on clinical information (basis 1) or clinical
investigation (basis 2).** Paediatric rows outside Group 3:

| Entity | Basis | Topography | Morphology | Group |
|---|---|---|---|---|
| Retinoblastoma | 1 or 2 | C69.2 | `9510/3` | **V** |
| Nephroblastoma | 2 | C64 | `8960/3` | **VI** |
| Hepatoblastoma | 2 | C22 | `8970/3` | **VII** |
| Hepatocellular carcinoma | 2 | C22.0 | `8170/3` | **VII** |
| Cholangiocarcinoma | 2 | C22.1, C24.0, C24.9 | `8160/3` | **VII** |
| Osteosarcoma · chondrosarcoma | 2 | C40, C41 | `9180/3` · `9220/3` | **VIII** |
| Sarcoma NOS · liposarcoma · leiomyosarcoma · angiosarcoma | 2 | any site | `8800/3` · `8850/3` · `8890/3` · `9120/3` | **IX** |
| Kaposi sarcoma of the skin | 1 | C44 | `9140/3` | **IX** |
| Melanoma of the skin | 1 | C44 | `8720/3` | **XI** |
| Langerhans cell histiocytosis | 2 | C34, C41, C71 and others | `9751/3` | **II** |
| Primary lymphoma of the central nervous system | 2 | C71 | `9590/3` | **II / III** |

The paper explicitly heads three of these *"Solid childhood cancers (age <15 years)"* —
nephroblastoma, hepatoblastoma, retinoblastoma. That is our population.

**Table 4, p. 06 — specific morphology on an elevated tumour marker plus clinical investigation
(basis 4).** Paediatric rows:

| Entity | Marker | Morphology | Group |
|---|---|---|---|
| Neuroblastoma | homovanillic acid, vanillylmandelic acid | `9500/3` | **IV** |
| Germ cell tumour | human chorionic gonadotropin | `9064/3` | **X** |
| Germ cell tumour | alpha-fetoprotein ± human chorionic gonadotropin | `9065/3` | **X** |
| Choriocarcinoma of the placenta | human chorionic gonadotropin | `9100/3` | **X** |
| Hepatocellular carcinoma | alpha-fetoprotein | `8170/3` | **VII** |
| Medullary thyroid carcinoma | calcitonin | `8345/3` | **XI** |
| Phaeochromocytoma | catecholamines, chromogranin A | `8700/3` | **XI** |
| Prolactinoma | prolactin | `8271/0` | **III** |
| Other functioning pituitary tumours | growth hormone, follicle-stimulating hormone, luteinising hormone, adrenocorticotropic hormone, thyroid-stimulating hormone | `8272/0` | **III** |
| Neuroendocrine tumour | chromogranin A | `8240/3` | **XI** |
| Functioning neuroendocrine tumours | insulin · glucagon · gastrin · vasoactive intestinal peptide · somatostatin · serotonin · adrenocorticotropic hormone | `8151/3` · `8152/3` · `8153/3` · `8155/3` · `8156/3` · `8241/3` · `8158/3` | **XI** |

Anything **not** in Table 3 or Table 4, diagnosed without pathology, is `8000/3` under rule 5 —
unless a coding expert at the registry rules otherwise, which the paper permits and which is the
registrar's call, not the tool's.

`8271/0` prolactinoma corroborates the Group 3 pituitary branch, which already emits it from
`md_pituitary_ihc`.

## 6. Open items this raises

1. **Groups 1 and 2 emit no `basis_of_diagnosis` at all.** Only `group_03_dt.json` carries the
   field. For haematolymphoid groups rule 7 is load-bearing — flow-cytometry immunophenotyping is
   **5**, a bone marrow **aspirate** is 5 while a bone marrow **biopsy** is 7 — and neither group
   records it. A gap, not a defect: the groups were built before the field existed.
2. **Table 3 coverage of Group 3 is not yet audited.** Its forty-three central nervous system rows
   are the ENCR-sanctioned imaging-only diagnoses. Whether every one is reachable in
   `group_03_dt.json`, and whether any imaging terminal emits a specific code **absent** from
   Table 3, is a check that does not exist. Worth one validator rule.
3. Whether the registry adopts the optional **7.1 / 7.2 / 7.3** sub-codes is a registrar decision.
   Recommendation: no. They are optional, not needed for comparability, and REDCap has no field.

---

*Extracted 16 September 2026 from the full text. Cross-checked against
`docs/group_03_build_contract.md` §2(5), `build/build_database.py` rule 10, and
`ICD coding/ICD-O-3.2/icdo32.sqlite`.*
