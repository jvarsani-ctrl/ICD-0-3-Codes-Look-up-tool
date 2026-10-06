# Evidence gates as document checklists: the mapping, for the registrar

**Written 6 October 2026** by the "ICD Overall fixes" session. Spec: `docs/superpowers/specs/2026-10-06-ux-overall-fixes-design.md` §4 and §7.
Machine-readable mapping: `docs/evidence_documents/group_NN.json`. Applied by `build/apply_evidence_documents.py`.

## How to read this

The clerk ticks which of seven documents are in the file. Each existing option keeps its label, captures and route; here it gets a rule. A **tier** option is offered when the rule fits the ticked set. A **special situation** option is always listed under the boxes. The tool never overstates its evidence (standing rule 8): an IHC Report or Gene reports for cancer never raises a tier on its own, and a tier that asserts a smear or tissue report requires the Cytology or Histology Report box itself.

What each document was taken to mean:

| Document | Taken to mean |
|---|---|
| Referral Letter/Clinical Note | referral letter, clinic letter or clinical note |
| Imaging Report | X-ray, ultrasound, CT, MRI, PET, B-scan, skeletal survey |
| Lab Report | blood, serum, urine or CSF results that are neither tissue nor smear: tumour markers, hormone assays, blood count, serum tryptase, **flow cytometry** |
| Cytology | smear or fluid morphology: fine-needle aspirate, effusion or CSF cytology, **blood film, bone marrow aspirate smear**, squash or touch preparation, aqueous-humour or liquid-biopsy cytology |
| Histology Report | pathology report on tissue: biopsy, resection, **trephine biopsy**, cell block, curettage, enucleation |
| IHC Report | immunohistochemistry panel, including in-situ hybridisation read as a stain (for example EBER) |
| Gene reports for cancer | karyotype, FISH, RT-PCR, sequencing or NGS, MLPA, methylation profiling, clonality testing |

The three haematology readings in bold (flow cytometry as Lab Report, blood film and marrow aspirate as Cytology, trephine as Histology Report) are the registrar's to confirm.

## Added on 6 October, after review

Two Group I gates, `ac_document_inventory` and `ml_document_inventory`, word a tier "flow cytometry and/or IHC". The first
mapping let only a Lab Report satisfy it, so a trephine with an IHC Report and no Lab Report fell to the tier that says "no
IHC". A tier's rule has one `any_of`, which cannot say morphology AND (Lab Report OR IHC Report), so each such tier now has a
copy placed after it: same label, route and captures, rule "needs IHC Report, none of Lab Report", with Flow cytometry removed
from the tests it credits (an IHC report is not flow cytometry). The tier "morphology only" now also excludes IHC Report. The
acute gate has three copies and the mature gate two; they are listed under `extra_options` in `docs/evidence_documents/group_01.json`.

## Group 1

### `ac_document_inventory` (tree `tree_acute_leukemia`)

*Question:* What reports are in this patient's file?
*(question rewritten; it said: What reports are in this patient's file?)*

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | Referral / clinical note only — no marrow report | tier | none of Cytology, Histology Report | Lowest tier. Fits any set with no smear and no tissue report, so a lone Lab, IHC or Gene report, imaging, or nothing ticked all land here and are understated rather than overstated. | high |
| 1 | Marrow aspirate / blood film morphology only (no flow cytometry, no IHC) | tier | at least one of Cytology, Histology Report; none of Lab Report | Marrow aspirate or blood film morphology is Cytology; a Histology Report (trephine) is also accepted as morphology because the ladder has no tissue tier. Excludes Lab to honour 'no flow cytometry'. IHC and Gene reports are tolerated so that immunocytochemistry (IHC beside Cytology) and a Gene report without a flow rung stay at this tier. | medium |
| 2 | Morphology + flow cytometry and/or IHC | tier | needs Lab Report; at least one of Cytology, Histology Report; none of Gene reports for cancer | Morphology (Cytology or Histology) plus flow cytometry, mapped to the Lab Report. Excludes Gene reports so a file with genetics fits options 3 and 4 instead. One any_of cannot also express 'IHC beside Histology', so an IHC Report without a Lab Report does not lift the tier. | medium |
| 3 | Morphology + flow/IHC + cytogenetics / FISH | tier | needs Lab Report and Gene reports for cancer; at least one of Cytology, Histology Report | Every rung named: morphology (Cytology or Histology), flow (Lab Report), cytogenetics/FISH (Gene report). A set with genetics but no Lab Report falls to option 1. | medium |
| 4 | Morphology + flow/IHC + cytogenetics + molecular / PCR / NGS | tier | needs Lab Report and Gene reports for cancer; at least one of Cytology, Histology Report | Same sets as option 3: cytogenetics and molecular testing are both Gene reports and no document id separates them, so the clerk is asked which describes the file. | medium |
| 5 | Trisomy 21 (Down syndrome) confirmed or suspected — neonatal or infant blasts | context | special situation (always offered) | A special population (trisomy 21, neonatal or infant blasts); does not follow from which documents exist. | high |
| 6 | Extramedullary mass with a myeloid phenotype (myeloid sarcoma / chloroma) | context | special situation (always offered) | A dominant finding (extramedullary myeloid mass) that redirects to the sarcoma-site node; not a statement about which documents exist. | medium |
| 7 | Malignancy excluded on review — reactive, non-neoplastic or the diagnosis was revised | context | special situation (always offered) | Malignancy excluded on review; always available. | high |

*For the registrar:*

- option 2: Flow cytometry is mapped to the Lab Report, which also holds blood counts, and the node after options 2 to 4 does not ask for the flow result (ac_prior_therapy_gate asks about prior therapy), so is it acceptable that any Lab Report ticked beside a smear or tissue report places the file at 'Morphology + flow cytometry and/or IHC'?
- option 1: The label names only marrow aspirate and blood film (mapped to Cytology), so is it acceptable that a Histology Report on its own (a trephine, or an extramedullary biopsy that is not marrow at all) also fits option 1?
- option 2: An IHC Report beside Cytology or Histology with no Lab Report stays at option 1, which says 'no IHC', although option 2 says 'and/or IHC'; is this understatement acceptable, in particular for a trephine with IHC and no flow report?
- option 3: A file with morphology and a Gene report but no Lab Report falls to option 1 because the flow/IHC rung is missing; is it right to understate it this way?
- option 4: Options 3 and 4 differ only by cytogenetics/FISH versus molecular testing, which are both Gene reports, so they fit the same sets and the clerk is asked which applies; is that acceptable?
- option 0: DATA GAP: the gate has no tier for a flow cytometry (Lab Report) or IHC report with no smear or tissue report, which falls to option 0 although option 0 says 'no marrow report'; should the gate gain an option such as 'flow cytometry or IHC report only, no morphology report'?
- option 6: Is the myeloid sarcoma option correctly a context option (a finding that redirects), given that its captures imply a histology and IHC report in the file?
- option 1: Options 1 to 4 here, and the matching options in the other three gates, record 'Histology' in evidence_tests for what the mapping reads as a Cytology file (aspirate or film); should the captured evidence_tests value be reviewed to follow the ticked documents?
- option 1: Is a marrow aspirate or blood film report correctly the Cytology document (including cytochemistry such as MPO and Sudan black), and a trephine biopsy correctly the Histology Report, with either one accepted as the morphology rung of the acute-leukaemia ladder?
- option 1: DATA GAP: a trephine-only file (Histology Report without Cytology) has no truthful option because every morphology option names the aspirate or blood film and the referral option says no marrow report, so it is held at the aspirate/blood-film tier; should the gate gain an option for a marrow trephine report only?
- option 0: DATA GAP: a Lab Report alone (flow cytometry on blood with no marrow or film report) fits only the referral-only option; should the gate gain an option for a flow cytometry report with no marrow morphology?
- option 2: Does a ticked Lab Report stand for flow cytometry here, so that any Lab Report beside a marrow or blood-film report, even a blood count alone, lifts the file to the flow tier and removes it from the morphology-only tier?
- option 2: The tick rules cannot express (Cytology or Histology) AND (Lab Report or IHC), so IHC beside morphology without a Lab Report is held at the morphology-only tier, whose label says no IHC; is that understatement acceptable, or should the flow/IHC rung be reached by IHC instead?
- option 3: Morphology plus Gene reports without a Lab Report (no flow cytometry) is held at the morphology-only tier because the ladder needs the flow/IHC rung; is that understatement acceptable?
- option 3: Should the cytogenetics/FISH option and the molecular/PCR/NGS option both be offered whenever Gene reports is ticked, with the clerk choosing, since one document cannot say which tests were done?
- option 6: Is the extramedullary myeloid-sarcoma option correctly a context option, given its captures record Histology and IHC and so it could be read as a tissue tier?

### `ml_document_inventory` (tree `tree_mature_lymphoid`)

*Question:* What reports are in this patient's file?
*(question rewritten; it said: What reports are in this patient's file?)*

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | Referral / clinical note only — no blood film, no marrow, no flow report | tier | none of Cytology, Histology Report | Lowest tier. A lone Lab Report is allowed here (otherwise it would dead-end), so 'no flow report' is not enforced. | high |
| 1 | Blood film and/or marrow morphology only (no flow cytometry, no IHC) | tier | at least one of Cytology, Histology Report; none of Lab Report | Blood film (Cytology) and/or marrow morphology (Cytology or Histology Report; the next node names the trephine). Excludes Lab to honour 'no flow cytometry'. IHC and Gene reports are tolerated and stay at this tier. | medium |
| 2 | Morphology + flow cytometry and/or IHC | tier | needs Lab Report; at least one of Cytology, Histology Report; none of Gene reports for cancer | Morphology plus flow cytometry (Lab Report). Excludes Gene reports so genetics lifts to option 3. An IHC Report without a Lab Report does not lift the tier. | medium |
| 3 | Morphology + flow / IHC + cytogenetics / FISH / molecular / PCR | tier | needs Lab Report and Gene reports for cancer; at least one of Cytology, Histology Report | Morphology, flow (Lab Report) and a Gene report (cytogenetics, FISH, molecular and PCR are all Gene reports). Genetics without a Lab Report falls to option 1. | medium |
| 4 | The marrow shows 20% or more blasts — an acute leukaemia, not a mature lymphoid neoplasm | context | special situation (always offered) | A dominant finding (20% or more blasts) that redirects to the acute leukaemia gate; not a statement about which documents exist. | medium |
| 5 | Malignancy excluded on review — reactive lymphocytosis, viral, or the diagnosis was revised | context | special situation (always offered) | Malignancy excluded on review; always available. | high |

*For the registrar:*

- option 2: Flow cytometry is mapped to the Lab Report, which also holds blood counts, and the node after options 2 and 3 (ml_compartment_gate) asks where the disease is, not what the flow showed, so is it acceptable that any Lab Report ticked beside a smear or tissue report places the file at 'Morphology + flow cytometry and/or IHC'?
- option 1: Blood film is mapped to Cytology and marrow morphology to Cytology or Histology Report (the next node names the trephine), so is it right that a Histology Report on its own fits option 1?
- option 2: A trephine with IHC but no Lab Report (the usual hairy cell leukaemia picture with a dry tap) stays at option 1, which says 'no IHC', although option 2 says 'and/or IHC'; is this understatement acceptable?
- option 3: A file with morphology and a Gene report but no Lab Report falls to option 1 because the flow rung is missing; is it right to understate it this way?
- option 0: DATA GAP: the gate has no tier for a peripheral-blood flow report (Lab Report) with no blood film or marrow report, which falls to option 0 although option 0 says 'no flow report'; should the gate gain an option such as 'flow cytometry report only, no morphology report'?
- option 4: Is the 20% or more blasts option correctly a context option (a finding that redirects to the acute leukaemia gate), given that it presumes a marrow report is in the file?
- option 0: DATA GAP: the referral-only option says no flow report, yet a Lab Report alone (flow cytometry with no film or marrow report) must fit it to avoid a dead end; should the gate gain an option for a flow cytometry report with no blood film or marrow morphology?
- option 1: Is a blood film or marrow aspirate report correctly the Cytology document and a trephine the Histology Report, with either one accepted as the morphology rung, since the destination question names the film, aspirate and trephine?
- option 2: Does a ticked Lab Report stand for flow cytometry here, so that any Lab Report beside blood-film or marrow morphology, even a blood count alone, lifts the file to the flow tier?
- option 2: The tick rules cannot express (Cytology or Histology) AND (Lab Report or IHC), so a trephine with IHC but no Lab Report is held at the morphology-only tier, whose label says no IHC; is that understatement acceptable?
- option 3: Morphology plus Gene reports without a Lab Report (no flow cytometry) is held at the morphology-only tier because the ladder needs the flow/IHC rung; is that understatement acceptable?
- option 4: Is the 20% or more blasts option correctly a context option, given it presupposes a marrow morphology report but redirects to the acute-leukaemia gate whatever else is ticked?

### `mpn_document_inventory` (tree `tree_chronic_myeloid_mpn`)

*Question:* What reports are in this patient's file?
*(question rewritten; it said: What reports are in this patient's file?)*

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | Referral / clinical note only — no blood film or marrow report | tier | none of Cytology, Histology Report | Lowest tier. Fits any set with no smear and no tissue report, including a lone Gene report (understated). | high |
| 1 | Blood film and/or marrow morphology only (no cytogenetics, no molecular) | tier | at least one of Cytology, Histology Report; none of Gene reports for cancer | Blood film or marrow morphology (Cytology or Histology Report). Excludes Gene reports to honour 'no cytogenetics, no molecular'. Lab and IHC Reports have no rung in this ladder and are tolerated. | high |
| 2 | Morphology + cytogenetics / FISH | tier | needs Gene reports for cancer; at least one of Cytology, Histology Report | Morphology plus a Gene report (cytogenetics or FISH). A Gene report cannot be told apart from molecular testing, so this fits the same sets as option 3. | medium |
| 3 | Morphology + cytogenetics / FISH + molecular / PCR / NGS | tier | needs Gene reports for cancer; at least one of Cytology, Histology Report | Same sets as option 2: cytogenetics and molecular testing are both Gene reports, so the clerk is asked which describes the file. | medium |
| 4 | Hypereosinophilia is the dominant finding, whatever else is in the file | context | special situation (always offered) | A dominant finding (hypereosinophilia) that redirects to the eosinophilia gate; the label itself says it holds whatever else is in the file. | high |
| 5 | Monocytosis-predominant picture — persistent monocytosis with or without splenomegaly | context | special situation (always offered) | A dominant finding (monocytosis) that redirects to the monocyte-count gate; not a statement about which documents exist. | high |
| 6 | Malignancy excluded on review — reactive, non-neoplastic or the diagnosis was revised | context | special situation (always offered) | Malignancy excluded on review; always available. | high |

*For the registrar:*

- option 1: Blood film is mapped to Cytology and marrow morphology to Cytology or Histology Report (the next node names only the blood film and marrow aspirate), so is it right that a trephine alone fits option 1?
- option 1: This ladder has no flow or IHC rung, so a Lab Report (blood count) or an IHC Report (reticulin, CD61) leaves the tier unchanged; is that the intended reading?
- option 3: Options 2 and 3 differ only by cytogenetics/FISH versus molecular testing, which are both Gene reports, so they fit the same sets and the clerk is asked which applies; is that acceptable?
- option 0: DATA GAP: the gate has no tier for a BCR::ABL1 or JAK2 Gene report on blood with no blood film or marrow report, which falls to option 0 although the report is real evidence; should the gate gain an option such as 'cytogenetic or molecular report only, no morphology report'?
- option 1: Is a blood film or marrow aspirate report correctly the Cytology document and a trephine the Histology Report, with either one accepted as marrow morphology, although the destination question names only the blood film and marrow aspirate?
- option 1: Is it right that the MPN ladder ignores Lab Report (blood count) and IHC entirely, so neither changes the tier?
- option 2: Should the cytogenetics/FISH option and the molecular/PCR/NGS option both be offered whenever Gene reports is ticked, with the clerk choosing, since one document cannot say which tests were done?

### `mds_document_inventory` (tree `tree_mds_jmml`)

*Question:* What reports are in this patient's file?
*(question rewritten; it said: What reports are in this patient's file?)*

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | Referral / clinical note only — no marrow report | tier | none of Cytology, Histology Report | Fallback for any set with no smear and no tissue report. A lone IHC, Gene, Lab or imaging report falls here and is understated, which is the safe direction. | high |
| 1 | Blood film / marrow aspirate morphology only (no trephine, no IHC, no cytogenetics) | tier | at least one of Cytology, Histology Report | Catches every set with a smear or trephine report that does not reach the rungs of options 2 to 4, including immunocytochemistry (Cytology plus IHC Report with no Histology Report), a trephine without IHC, and genetics without the full ladder. Excluding IHC or genetics would dead-end those sets, and the tick rules cannot express 'not all of the three'. Complete files also fit this option, so the clerk is asked between this option and the higher rung that fits. | medium |
| 2 | Marrow aspirate + trephine biopsy with IHC (CD61 / CD41 performed) | tier | needs Cytology and Histology Report and IHC Report; none of Gene reports for cancer | The label names the aspirate, the trephine and the IHC, so all three documents are required (standing rule 8, rule c). Cytology plus IHC Report with no Histology Report is immunocytochemistry and must not reach a tissue tier (rule d), so Proposer B's any_of lift is rejected. Genetics is excluded so files with a Gene report fit options 3 and 4 instead. | medium |
| 3 | Marrow + trephine/IHC + cytogenetics / FISH | tier | needs Cytology and Histology Report and IHC Report and Gene reports for cancer | Every rung the label names is required: aspirate, trephine, IHC and a Gene report. Genetics without the trephine and IHC rungs falls to option 1, which understates. Same fit set as option 4 because one Gene report cannot say which tests were done. | medium |
| 4 | Marrow + trephine/IHC + cytogenetics + molecular / PCR / NGS | tier | needs Cytology and Histology Report and IHC Report and Gene reports for cancer | Sibling of option 3 with an identical fit set; the clerk is asked which describes the file. | medium |
| 5 | Monocytosis-predominant picture — persistent monocytosis with or without splenomegaly (JMML / CMML suspicion) | context | special situation (always offered) | A dominant finding that redirects to the monocyte-count gate; independent of which documents exist. | high |
| 6 | Hypereosinophilia is the dominant finding, not monocytosis or dysplasia | context | special situation (always offered) | A dominant finding that redirects to the MDS/MPN overlap confirmation; independent of which documents exist. | high |
| 7 | Malignancy excluded on review — reactive, non-neoplastic or the diagnosis was revised | context | special situation (always offered) | Malignancy excluded on review; always available. | high |

*For the registrar:*

- option 1: Option 1 carries no excludes, because 'no trephine, no IHC, no cytogenetics' would leave an aspirate with IHC (immunocytochemistry) or an aspirate with a trephine and no IHC with no tier, so a file with aspirate, trephine and IHC fits options 1 and 2 (and 1, 3 and 4 with a Gene report) and the clerk is asked; is that acceptable?
- option 2: Option 2 requires Cytology, Histology Report and IHC Report because the label names the aspirate, the trephine and the IHC, so a trephine with IHC but no aspirate or film report falls to option 1; is this understatement acceptable?
- option 2: The label asserts CD61 / CD41 was performed, but the IHC Report document does not distinguish markers, so is it acceptable that any IHC Report beside the aspirate and trephine places the file at option 2?
- option 1: An IHC Report beside Cytology with no Histology Report (immunocytochemistry) stays at option 1, which says 'no IHC'; is that the intended reading?
- option 1: DATA GAP: the gate has no tier for an aspirate with a trephine report but no IHC, or for a trephine alone, so both fall to option 1 although option 1 says 'no trephine'; should the gate gain an option such as 'aspirate and trephine biopsy, IHC not performed'?
- option 4: Options 3 and 4 differ only by cytogenetics/FISH versus molecular testing, which are both Gene reports, so they fit the same sets and the clerk is asked which applies; is that acceptable?
- option 1: DATA GAP: a trephine without IHC (Histology Report alone, or beside a Cytology report) has no truthful option, because the aspirate-only option says no trephine and the next tier says IHC was performed; it is held at the aspirate tier, which understates; should the gate gain an option for aspirate with trephine and no IHC?
- option 2: Cytology plus IHC with no Histology Report fits the aspirate-plus-trephine tier, which lifts immunocytochemistry to a tissue tier; should it instead stay at the aspirate tier, accepting that a trephine without IHC then has no tier and needs the data-gap option above?
- option 2: A Histology Report plus IHC with no Cytology report fits the aspirate-plus-trephine tier although no aspirate is ticked; is that acceptable?
- option 1: Are the iron stain and cytochemistry on the aspirate correctly part of the Cytology document, and CD61/CD41 stains correctly the IHC Report?
- option 3: Morphology plus Gene reports without IHC is held at the aspirate tier because the ladder needs the trephine/IHC rung; is that understatement acceptable?
- option 3: Should the cytogenetics/FISH option and the molecular/PCR/NGS option both be offered whenever Gene reports is ticked, with the clerk choosing, since one document cannot say which tests were done?
- option 5: Are the monocytosis-predominant and hypereosinophilia options correctly context options that redirect whatever documents are ticked?
- option 1: DATA GAP: the gate has no tier for an aspirate with a trephine report but no IHC, for a trephine alone, or for an aspirate with IHC but no trephine, so all fall to the aspirate-only option although its label says no trephine and no IHC; should the gate gain an option such as 'aspirate and trephine biopsy, IHC not performed'?
- option 1: Because the tick rules cannot say 'not all of aspirate, trephine and IHC', a complete aspirate, trephine and IHC file also fits the aspirate-only option and the clerk is asked between the two; is that acceptable?
- option 1: Is a blood film or marrow aspirate report (including iron stain and cytochemistry) correctly the Cytology document, and is a trephine biopsy alone accepted as morphology at this tier?
- option 2: Option 2 requires Cytology, Histology Report and IHC Report, so a trephine with IHC but no aspirate or film report (for example a dry tap) falls to the aspirate-only tier; is this understatement acceptable?
- option 2: The label asserts CD61 / CD41 staining, but the IHC Report document does not distinguish markers; is it acceptable that any IHC Report beside the aspirate and trephine places the file at option 2?
- option 2: Cytology plus IHC Report with no Histology Report is treated as immunocytochemistry and stays at the aspirate-only tier, not the trephine-with-IHC tier; is that the intended reading?
- option 3: Aspirate, trephine and a Gene report with no IHC Report fall to the aspirate-only tier because the IHC rung is missing; is this understatement acceptable?
- option 0: A lone IHC Report, Gene report or Lab Report with no smear or tissue report falls to the referral-only option, which says no marrow report; is that understatement acceptable?

## Group 2

### `g2_document_inventory` (tree `g2_lymphoid_main`)

*Question:* What specimen and what reports are in this patient's file, and what was the outcome of any aspirate?
*(question rewritten; it said: What specimen and what reports are in this patient's file, and what was the outcome of any aspirate?)*

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | Referral or clinical note only — no cytology and no histology report | tier | none of Cytology, Histology Report | Lowest tier: fits every file with neither a Cytology nor a Histology Report, so imaging, lab, IHC or gene reports on their own fall here and understate. | high |
| 1 | FNA smear only — ADEQUATE, and the cytology reports a neoplastic / malignant / lymphomatous population (no cell block, no flow, no IHC) | tier | needs Cytology; none of Histology Report, Lab Report | Smear-only tier: needs the Cytology document, no tissue or cell block (Histology) and no flow (Lab Report); IHC beside Cytology is immunocytochemistry and stays at this tier. | medium |
| 2 | FNA smear only — ADEQUATE, and the cytology reports granulomas, necrosis, reactive change or another benign picture | tier | needs Cytology; none of Histology Report, Lab Report | Sibling of option 1 that differs only by the cytological reading (benign picture), which no document expresses, so it fits the same sets. | medium |
| 3 | FNA smear only — INADEQUATE / non-diagnostic ("too few cells for cytology") | context | special situation (always offered) | Inadequate aspirate is an outcome state of the specimen, not a document set. | high |
| 4 | FNA smear only — technically UNINTERPRETABLE (air-dried, obscured by blood, stain failure); no opinion could be given on the cells present | context | special situation (always offered) | Technically uninterpretable aspirate is an outcome state of the specimen, not a document set. | high |
| 5 | FNA + cell block, or core needle biopsy, or excisional / incisional biopsy — H&E only, no IHC and no flow | tier | needs Histology Report; none of IHC Report, Lab Report | Tissue or cell-block report with no IHC and no flow: requires Histology and excludes IHC and Lab Report; genetics alone does not lift it. | high |
| 6 | Tissue (cell block / core / excisional) WITH immunohistochemistry and/or flow cytometry | tier | needs Histology Report; at least one of IHC Report, Lab Report; none of Gene reports for cancer | Tissue with IHC and/or flow: requires Histology plus an IHC Report or a Lab Report read as flow; excludes genetics so option 8 holds the higher rung. | medium |
| 7 | Effusion, CSF, marrow aspirate or node aspirate WITH flow cytometry — no tissue block | tier | needs Cytology and Lab Report; none of Histology Report | Fluid or aspirate cytology with flow cytometry and no tissue block: requires Cytology and a Lab Report read as flow, and excludes Histology. | medium |
| 8 | Tissue with IHC/flow PLUS cytogenetics / FISH, or plus molecular / NGS | tier | needs Histology Report and Gene reports for cancer; at least one of IHC Report, Lab Report | Cumulative rung: tissue, IHC and/or flow, and a gene report; histology plus genetics without IHC or flow falls to option 5. | medium |
| 9 | Malignancy excluded on review — reactive, infective or non-neoplastic; or the diagnosis was revised | context | special situation (always offered) | Malignancy excluded on review is a conclusion that does not follow from which documents exist. | high |

*For the registrar:*

- option 1: DATA GAP: No option describes a smear, fluid or aspirate cytology report read with immunocytochemistry (Cytology and IHC Report ticked, no Histology Report), so that file fits options 1 and 2 although their labels say 'no IHC'; should the gate gain an option for cytology with immunocytochemistry?
- option 0: Does a file with only a Lab Report holding flow cytometry (no Cytology Report) falling to option 0 understate acceptably, given that option 7 requires the Cytology Report for its smear or aspirate specimen?
- option 7: Do you confirm that a Lab Report ticked beside Cytology stands for flow cytometry in option 7 (and that options 1 and 2 exclude the Lab Report to honour 'no flow'), although the Lab Report also covers blood counts and tumour markers?
- option 7: Do you confirm that effusion, cerebrospinal-fluid, marrow aspirate and node aspirate preparations (and a blood film) map to the Cytology document?
- option 6: Do you confirm that flow cytometry maps to the Lab Report, so that Histology plus a Lab Report fits option 6 (and option 5 excludes the Lab Report to honour 'no flow'), and that a bone marrow trephine biopsy maps to the Histology Report?
- option 2: Is option 2 (adequate smear whose cytology reads benign) correctly a tier sibling of option 1 rather than a context option, given that the two differ only by the cytological reading?
- option 8: Is it acceptable that a Histology Report with a gene report but without IHC or flow falls to option 5 (H&E only), because option 8 is a cumulative ladder that requires tissue, IHC and/or flow, and a gene report?
- option 7: Is the Lab Report an acceptable stand-in for flow cytometry on an aspirate or effusion, given that it also covers unrelated blood tests such as a blood count?
- option 6: Is the Lab Report an acceptable stand-in for flow cytometry beside a tissue report (options 6 and 8), so that a Histology Report plus a Lab Report with no IHC fits the IHC-and/or-flow option and not the H&E-only option?
- option 7: Should a flow cytometry report with no Cytology Report ticked fall to the referral-only option, given that a marrow aspirate smear, blood film, effusion or cerebrospinal-fluid cytology is the Cytology document?
- option 5: Is a Histology Report with a Gene report but no IHC and no flow cytometry correctly held at the H&E-only option, which understates the file?
- option 8: Should the option stay tissue-only, so that a marrow aspirate or effusion with flow cytometry plus cytogenetics falls to the flow-only option without its genetics credited?
- option 1: DATA GAP: the gate has no option for a smear with immunocytochemistry (Cytology plus IHC, no cell block, no flow), so that set fits the smear options although their label says no IHC; should an option for FNA smear with immunocytochemistry be added?
- option 2: DATA GAP: the gate has no option for a smear with a gene report (FISH or molecular on an aspirate, no flow, no cell block), so that set fits the smear options although their label says FNA smear only; should an option for smear with genetics be added?
- option 1: Are the adequate-and-neoplastic and adequate-and-benign smear options correctly kinds of tier rather than context, given that this makes the clerk choose between them on every cytology-only file?
- option 0: Is it acceptable that a file holding only imaging, a Lab Report, an IHC Report or a Gene report fits the referral-only option, whose label says no cytology and no histology report?
- option 3: Should the inadequate and the technically uninterpretable smear outcomes (options 3 and 4) stay available as context options even when no Cytology Report is ticked?

### `g2cut_document_inventory` (tree `g2_cutaneous`)

*Question:* What is in this patient's file for the skin lesion?
*(question rewritten; it said: What is in this patient's file for the skin lesion?)*

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | Referral, clinic or dermatology letter only — no skin biopsy in the file | tier | none of Histology Report | Letter-only tier: fits every file with no Histology Report (skin biopsy), so cytology, IHC, lab or gene reports alone fall here and understate. | high |
| 1 | Skin biopsy with H&E only — no immunohistochemistry | tier | needs Histology Report; none of IHC Report | Skin biopsy with H&E only: requires Histology and excludes IHC; genetics or lab without IHC falls here because the higher rungs need IHC. | high |
| 2 | Skin biopsy with immunohistochemistry (with or without EBER in-situ hybridisation) | tier | needs Histology Report and IHC Report; none of Gene reports for cancer, Lab Report | Skin biopsy with IHC: requires Histology and IHC and excludes genetics and Lab Report so option 3 holds the higher rung. | high |
| 3 | Skin biopsy with immunohistochemistry, plus TCR clonality, FISH, or blood flow cytometry | tier | needs Histology Report and IHC Report; at least one of Gene reports for cancer, Lab Report | Cumulative rung: biopsy, IHC and TCR clonality or FISH (genetics) or blood flow cytometry (Lab Report read as flow). | medium |
| 4 | The skin lesion is one site of an established systemic or nodal lymphoma, or nodal / visceral disease dominates the picture | context | special situation (always offered) | Established systemic or nodal lymphoma is a dominant finding that redirects to the main tree. | high |
| 5 | The infiltrate is B-lineage — CD20, CD79a or PAX5 positive and CD3 negative | context | special situation (always offered) | B-lineage infiltrate is a finding that redirects to the mature B-cell tree, not a document set. | medium |
| 6 | The infiltrate is Langerhans cell or histiocytic — CD1a, CD207 / langerin, S100, CD68 or CD163 positive | context | special situation (always offered) | Langerhans or histiocytic infiltrate is a finding that redirects to the histiocytic tree, not a document set. | medium |
| 7 | The infiltrate is mast cell — tryptase or CD117 positive, or the report says urticaria pigmentosa or mastocytoma | context | special situation (always offered) | Mast cell infiltrate is a finding that redirects to the mast cell tree, not a document set. | medium |
| 8 | The file establishes a non-neoplastic skin condition — infection, drug reaction, pseudolymphoma or another mimic | context | special situation (always offered) | Established non-neoplastic mimic is a conclusion, not a document set. | high |
| 9 | Malignancy excluded on review — the diagnosis was revised and no lymphoid neoplasm is present | context | special situation (always offered) | Malignancy excluded on review is a conclusion, not a document set. | high |

*For the registrar:*

- option 0: DATA GAP: The cutaneous gate has no cytology tier, so a skin smear or aspirate with no biopsy falls to option 0 ('letter only, no skin biopsy'); should the gate gain an option for cytology only?
- option 3: Do you confirm that option 3 reads a Lab Report as blood flow cytometry and a gene report as TCR clonality or FISH, requires IHC beside the biopsy (so biopsy plus genetics or lab without IHC falls to option 1), and that option 2 excludes genetics and the Lab Report to stay below it?
- option 5: Is option 5 (B-lineage infiltrate on CD20, CD79a, PAX5 and CD3) correctly a context redirect to the mature B-cell tree rather than an evidence tier that needs Histology and IHC ticked?
- option 6: Is option 6 (Langerhans or histiocytic infiltrate on CD1a, langerin, S100, CD68, CD163) correctly a context redirect to the histiocytic tree rather than an evidence tier that needs Histology and IHC ticked?
- option 7: Is option 7 (mast cell infiltrate on tryptase or CD117) correctly a context redirect to the mast cell tree rather than an evidence tier that needs Histology and IHC ticked?
- option 0: DATA GAP: the gate has no cytology option, so a file with only a smear or aspirate of the skin lesion falls to the referral-letter-only option, whose label says no skin biopsy; should an option for cytology of the skin lesion without a biopsy be added?
- option 3: Is the Lab Report an acceptable stand-in for blood flow cytometry, given that it also covers unrelated blood tests, so that biopsy plus IHC plus any Lab Report fits the top rung?
- option 3: Are T-cell receptor clonality and FISH correctly counted as the Gene reports document for this rung?
- option 1: Is a skin biopsy with a Gene report or Lab Report but no IHC correctly held at the H&E-only option, which understates the file?
- option 4: Is the systemic or nodal lymphoma option correctly a context option available whatever is ticked?
- option 5: Is the B-lineage option correctly a context option, given that its label is an IHC finding and could be read as a tier asserting an IHC Report?
- option 6: Is the Langerhans or histiocytic option correctly a context option, given that its label is an IHC finding and could be read as a tier asserting an IHC Report?
- option 7: Is the mast cell option correctly a context option, given that its label is an IHC finding and could be read as a tier asserting an IHC Report?
- option 8: Is the non-neoplastic cutaneous mimic option correctly a context option, given that the file establishing it implies a histology report?

### `g2hist_document_inventory` (tree `g2_histiocytic`)

*Question:* What is in this patient's file for the histiocytic or dendritic lesion?
*(question rewritten; it said: What is in this patient's file for the histiocytic or dendritic lesion?)*

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | Referral or clinic letter only — it names a histiocytosis, but there is no biopsy report in the file | tier | none of Histology Report | Letter-only tier: fits every file with no Histology Report, so imaging, cytology, IHC or gene reports alone fall here and understate. | high |
| 1 | Biopsy report with H&E morphology only — no IHC performed, or none reported | tier | needs Histology Report; none of IHC Report | Biopsy with H&E only: requires Histology and excludes IHC; histology plus genetics without IHC falls here because the higher rungs need IHC. | high |
| 2 | Biopsy report with immunohistochemistry | tier | needs Histology Report and IHC Report; none of Gene reports for cancer | Biopsy with IHC: requires Histology and IHC and excludes genetics so option 3 holds the higher rung. | high |
| 3 | Biopsy + IHC + molecular (BRAF, ALK rearrangement, clonality or NGS) | tier | needs Histology Report and IHC Report and Gene reports for cancer | Cumulative rung: biopsy, IHC and a molecular gene report (BRAF, ALK, clonality, NGS) all required. | high |
| 4 | Spindled or epithelioid tumour in a node, tonsil, spleen, liver or abdomen — reported as "sarcoma" or "undifferentiated tumour", with the routine lymphoma panel non-contributory | context | special situation (always offered) | Sarcoma-like or undifferentiated tumour with a non-contributory panel is a finding in the report, not a document set; as context it stays selectable whatever is ticked. | medium |
| 5 | The file establishes a named non-neoplastic or uncoded histiocytic condition — Rosai-Dorfman disease, juvenile xanthogranuloma, HLH, indeterminate dendritic cell tumour or ALK-positive histiocytosis | context | special situation (always offered) | Named non-neoplastic or uncoded histiocytic condition is a conclusion, not a document set. | high |
| 6 | On review this is a lymphoma, not a histiocytic or dendritic neoplasm | context | special situation (always offered) | Lymphoma on review is a dominant finding that redirects to the lymphoid lineage node. | high |
| 7 | Malignancy excluded on review — the lesion is reactive or infective and no neoplasm is asserted | context | special situation (always offered) | Malignancy excluded on review is a conclusion, not a document set. | high |

*For the registrar:*

- option 0: DATA GAP: The histiocytic gate has no cytology tier, so a marrow aspirate smear (for example showing haemophagocytosis) or other cytology with no biopsy falls to option 0 ('letter only, no biopsy report'); should the gate gain an option for cytology only?
- option 3: Do you confirm that option 3 requires Histology, IHC and a gene report together, so a biopsy with a gene report but no IHC (for example BRAF by sequencing) falls to option 1 (H&E only), and that option 2 excludes genetics to stay below it?
- option 4: Is option 4 (spindled or epithelioid tumour reported as sarcoma or undifferentiated tumour, with a non-contributory lymphoma panel) correctly a context option, given that it describes a report finding rather than which documents exist and that context keeps it selectable whatever is ticked?
- option 0: DATA GAP: the gate has no cytology option, so a file with only a smear or aspirate (for example a marrow aspirate) falls to the referral-letter-only option, whose label says no biopsy report; should an option for cytology without a biopsy be added?
- option 1: Is a biopsy with a Gene report but no IHC correctly held at the H&E-only option, which understates the file?
- option 3: Are BRAF, ALK rearrangement, clonality and next-generation sequencing correctly counted as the Gene reports document, and is it right that a Lab Report adds nothing at this gate?
- option 4: Is the spindled or epithelioid tumour option correctly a context option, given that it describes a morphology and panel finding that implies a histology report and IHC?
- option 5: Is the named uncoded entity option correctly a context option, given that the file establishing it implies a histology report?
- option 6: Is the on-review-lymphoma option correctly a context option available whatever is ticked?

### `g2mast_document_inventory` (tree `g2_mastcell`)

*Question:* What reports are in this patient's file?
*(question rewritten; it said: What reports are in this patient's file?)*

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | Referral or clinical note only — no pathology report in the file | tier | none of Histology Report, Cytology | Lowest tier. Fits every set with neither a Histology Report nor a Cytology document, so lab, imaging, IHC or gene reports on their own fall here and understate. | medium |
| 1 | Morphology only — skin biopsy, marrow biopsy and/or a blood or marrow smear, with no IHC, no serum tryptase and no KIT result | tier | at least one of Histology Report, Cytology; none of IHC Report | Morphology (biopsy or smear) with no IHC Report. A lab or gene report beside morphology without IHC falls here and understates. | medium |
| 2 | Morphology + IHC (tryptase, CD117, and/or CD25 / CD30 / CD2) | tier | needs IHC Report; at least one of Histology Report, Cytology; none of Lab Report | Judged: option 3 is a cumulative rung above this one, so the two must not fit the same set; a clerk should not be asked to choose between a tier and the tier that strictly contains it. Excluding the Lab Report makes option 3 exclusive. Sets with a gene report but no Lab Report stay here, which understates the KIT result. | medium |
| 3 | Morphology + IHC + basal serum tryptase and/or KIT molecular result | tier | needs IHC Report and Lab Report; at least one of Histology Report, Cytology | Judged: the rung needs morphology, IHC and a tryptase or KIT result. The schema allows one any_of group, which is spent on morphology, so the Lab Report (basal serum tryptase) is required and the gene report (KIT) cannot be an alternative. A KIT-only file falls to option 2, which understates and is the safe direction. Proposer A's alternative (require Histology, any_of lab or genetics) overlaps option 2 on every qualifying set and forces a question on each. A gene report alone never raises a tier; IHC and Lab Report ticked without morphology cannot reach this rung because morphology is required. | medium |
| 4 | Reviewed — this is not a mast cell neoplasm, or the diagnosis was revised | context | special situation (always offered) | Review outcome leading to a non-reportable exit; does not follow from which documents exist. | high |

*For the registrar:*

- option 1: Do you confirm that 'morphology' here means a Histology Report (skin or marrow biopsy) or a Cytology report (blood or marrow smear), so either one satisfies options 1, 2 and 3 and option 0 excludes both?
- option 1: DATA GAP: No option describes morphology plus a serum tryptase and/or KIT result without IHC (the cheapest route the hint names), so that file falls to option 1 although its label says 'no serum tryptase and no KIT result'; should the gate gain an option for morphology plus serum tryptase or KIT without IHC?
- option 2: Is it acceptable that an IHC Report beside a smear with no Histology Report fits option 2 'Morphology + IHC' (immunocytochemistry), since the gate merges smear and biopsy into one morphology rung and has no separate cytology tier to hold it?
- option 3: Do you confirm that a Lab Report stands for basal serum tryptase and a gene report for the KIT result in option 3, that option 3 needs the Histology Report (so smear plus IHC plus lab falls to option 2), and that Histology plus IHC plus lab or genetics fits both options 2 and 3 so the clerk is asked?
- option 1: Are skin biopsy and marrow biopsy correctly the Histology Report document and a blood or marrow smear differential correctly the Cytology document, so that either one satisfies the morphology tier?
- option 1: DATA GAP: the gate has no option for morphology plus serum tryptase or a KIT result without IHC, which its own hint calls a route to a definitive code, so that set falls to the morphology-only option whose label says no tryptase and no KIT result; should an option for morphology with serum tryptase and/or KIT but no IHC be added?
- option 2: Should IHC beside a smear with no Histology Report stay at the morphology-plus-IHC option because this gate counts a smear as morphology, or should the option require the Histology Report?
- option 3: Is the Lab Report an acceptable stand-in for basal serum tryptase, given that it also covers unrelated blood tests?
- option 3: Should a KIT molecular result alone (Gene report, no Lab Report) lift a file to the top rung, given that the label reads tryptase and/or KIT and the mapping currently credits only the Lab Report?
- option 0: Is it acceptable that a file holding only a Lab Report (serum tryptase), an IHC Report or a Gene report fits the referral-only option, whose label says no pathology report?
- option 3: Do you confirm that the Lab Report stands for basal serum tryptase in option 3, although it also covers blood counts and other results, and that the next question asks for the specific result?
- option 3: Is it acceptable that a KIT molecular result without a serum tryptase result (Gene report ticked, no Lab Report) falls to option 2 and is not credited at option 3, although the label reads 'tryptase and/or KIT'?
- option 1: Do you confirm that 'morphology' here means a Histology Report (skin or marrow biopsy, trephine) or a Cytology document (blood film or marrow aspirate smear), so that either satisfies options 1, 2 and 3?

## Group 3

### `pf_document_inventory` (tree `g3_posterior_fossa`)

*Question:* Posterior fossa mass (cerebellum C71.6 or brain stem C71.7). What is actually in this patient's file, and was the specimen adequate for diagnosis?
*Hint rewritten:* Posterior fossa resection is often the only tissue that will ever exist, so record adequacy honestly: an uninterpretable specimen is not a negative one, and it must not be coded as though a diagnosis was reached.

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | Referral letter or clinical note only — no imaging report and no pathology report | tier | none of Imaging Report, Cytology, Histology Report | Lowest tier: fits when no imaging, cytology or histology document is ticked, so a lone Lab, IHC or Gene report falls here and understates. | high |
| 1 | Imaging report only (MRI / CT) — no tissue and no cytology | tier | needs Imaging Report; none of Cytology, Histology Report | Imaging report with no cytology or tissue; Lab is not excluded because the next node asks for the marker results. | high |
| 2 | Intraoperative frozen section or squash cytology only — no definitive histology report has followed | tier | needs Cytology; none of Histology Report | Intraoperative frozen section or squash without a definitive report is the Cytology document; IHC beside it stays at this tier. | medium |
| 3 | Definitive histology report — H&E, reticulin, PAS or Alcian blue only; no immunohistochemistry | tier | needs Histology Report; none of IHC Report | Tissue report with no IHC ticked; a Gene report without IHC also lands here, which understates. | high |
| 4 | Histology WITH basic diagnostic immunohistochemistry — GFAP, synaptophysin, EMA, S100, Ki-67, SMARCB1 (INI1) | tier | needs Histology Report and IHC Report; none of Gene reports for cancer | Histology plus IHC with no Gene report; sibling of option 5, since the Histology and IHC documents cannot tell the basic panel from the surrogate panel. | high |
| 5 | Histology WITH surrogate molecular immunohistochemistry — H3 K27me3, H3 K27M, EZHIP, LEF1, β-catenin, GAB1, YAP1, LIN28A, BRG1/SMARCA4 | tier | needs Histology Report and IHC Report; none of Gene reports for cancer | Histology plus IHC with no Gene report; sibling of option 4 and fits the same sets, so the clerk is asked which panel was run. | high |
| 6 | Histology and IHC PLUS molecular testing — FISH, RT-PCR, Sanger or NGS sequencing, or DNA methylation profiling | tier | needs Histology Report and IHC Report and Gene reports for cancer | Cumulative ladder: the label names histology, IHC and molecular testing, so all three documents are required. | medium |
| 7 | A specimen was taken but the report says it is inadequate, non-diagnostic, or crush artefact only | context | special situation (always offered) | Inadequate or non-diagnostic specimen is a statement about the specimen, not about which documents exist. | high |
| 8 | The specimen could not be interpreted at all — stain failure, no residual lesional tissue on the levels cut | context | special situation (always offered) | Uninterpretable specimen (stain failure, no residual lesional tissue) is a statement about the specimen. | high |
| 9 | The posterior fossa is not established as the site — the lesion crosses compartments, or the site is not stated | context | special situation (always offered) | Site not established is a situation that no document id expresses. | high |
| 10 | Reviewed and NOT a neoplasm — cerebellar abscess, tuberculoma, demyelination or another non-neoplastic mass | context | special situation (always offered) | Non-neoplastic lesion reviewed and excluded is a situation that no document id expresses. | high |

*For the registrar:*

- option 2: DATA GAP: the posterior fossa gate offers only an intraoperative frozen-section or squash cytology tier, so a Cytology-only file of cerebrospinal-fluid or aspirate cytology is described as intraoperative; should an option for cerebrospinal-fluid or aspirate cytology without tissue be added?
- option 3: A file that holds a Histology Report and a Gene report but no IHC Report falls to the H&E-only option, which understates; is that the intended direction?
- option 6: Gene reports for cancer may be germline or on blood; should a Gene report ticked beside Histology and IHC always count as tissue molecular testing for the molecular option?
- option 4: Options 4 and 5 differ only by the immunohistochemistry panel, so every Histology plus IHC file asks the clerk to choose between them; is that acceptable?
- option 2: Does the Cytology tick correctly stand for an intraoperative frozen section or squash, given that a cerebrospinal-fluid or fine-needle cytology report would also take this option?
- option 3: Options 3 to 6 record the specimen as adequate and no document can show adequacy, so is it acceptable that a ticked Histology Report takes an adequate option unless the clerk chooses the inadequate or uninterpretable line?
- option 4: Is it right that the basic and surrogate-molecular immunohistochemistry options fit the same ticked sets, so the clerk is asked which panel the file holds?
- option 6: Should a file with a Histology Report and a Gene report but no IHC Report fall to the H&E-only option (understating), because the molecular option names immunohistochemistry as a rung?
- option 0: Is it acceptable that a lone Laboratory Report, which may hold an alpha-fetoprotein or human chorionic gonadotropin result, falls to the referral-only option and so skips the marker questions that the imaging branch asks?

### `st_document_inventory` (tree `g3_supratentorial`)

*Question:* What is in this patient's file for this supratentorial lesion, and was the specimen adequate for diagnosis?
*Hint rewritten:* A crush-artefact or non-diagnostic biopsy is INADEQUATE — it is not a negative biopsy, and it must not be recorded as one. An intraoperative frozen section or squash is never the coded diagnosis on its own.

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | Referral letter or clinical note only — no pathology report and no imaging report in the file | tier | none of Imaging Report, Cytology, Histology Report | Lowest tier: no imaging, cytology or histology ticked; IHC, Gene or Lab reports alone fall here and understate. | high |
| 1 | Imaging report only — no tissue has been taken, or none will be | tier | needs Imaging Report; none of Cytology, Histology Report | Imaging report with no cytology or tissue ticked. | high |
| 2 | Intraoperative frozen section or squash cytology only — no definitive paraffin histology report | tier | needs Cytology; none of Histology Report | Frozen section or squash with no definitive paraffin report is the Cytology document; IHC beside it stays at this tier. | medium |
| 3 | Definitive histology report (H&E) — no immunohistochemistry | tier | needs Histology Report; none of IHC Report | Definitive histology with no IHC ticked; a Gene report without IHC lands here and understates. | high |
| 4 | Histology with basic diagnostic immunohistochemistry (GFAP, synaptophysin, EMA, Olig2, S100, Ki-67, INI1) | tier | needs Histology Report and IHC Report; none of Gene reports for cancer | Histology plus IHC and no Gene report; sibling of option 5, whose panel difference no document id expresses. | high |
| 5 | Histology with surrogate molecular immunohistochemistry as well (IDH1 R132H, ATRX, p53, H3 K27M, H3 G34R/V, BRAF VE1, L1CAM, p65/RelA, LIN28A, CD34) | tier | needs Histology Report and IHC Report; none of Gene reports for cancer | Histology plus IHC and no Gene report; sibling of option 4 and fits the same sets. | high |
| 6 | Histology plus a molecular result — FISH, RT-PCR, Sanger sequencing or MLPA | tier | needs Histology Report and IHC Report and Gene reports for cancer | Molecular rung: requires Histology, IHC and Gene reports because the captures record all three; sibling of option 7. | medium |
| 7 | Histology plus DNA methylation profiling or NGS | tier | needs Histology Report and IHC Report and Gene reports for cancer | Molecular rung for methylation or next-generation sequencing; fits the same sets as option 6 because a Gene report does not state its assay. | medium |
| 8 | The pathology report is in the file but hedges throughout ('suggestive of', 'cannot exclude') and never states whether the specimen was adequate | context | special situation (always offered) | A hedged report that never states adequacy is a statement about the report, not about which documents exist. | medium |
| 9 | The specimen was INADEQUATE — non-diagnostic, crush artefact, necrosis only, or too little tissue | context | special situation (always offered) | Inadequate specimen is a statement about the specimen. | high |
| 10 | The supratentorial site recorded at Stage 1 is not established, or the lesion is not in fact supratentorial | context | special situation (always offered) | Site not established, or not supratentorial, is a situation that no document id expresses. | high |
| 11 | An extracranial primary tumour is documented and this brain lesion is a metastasis from it | context | special situation (always offered) | Metastasis from an extracranial primary redirects to another group and is not a document tier. | high |

*For the registrar:*

- option 2: DATA GAP: the supratentorial gate has no tier for cerebrospinal-fluid or aspirate cytology, so a Cytology-only file is described as an intraoperative frozen section or squash; should an option for cytology without tissue be added?
- option 3: A Histology Report plus a Gene report without an IHC Report fits only the H&E-only option; should that understatement stand?
- option 6: Options 6 and 7 name only histology plus a molecular result, but their captures record IHC, so I required an IHC Report as well; should a file with Histology and Gene reports but no IHC be called H&E only?
- option 7: Options 6 and 7 differ only by assay type, which the Gene reports document cannot express, so every Histology, IHC and Gene file asks the clerk to choose; is that acceptable?
- option 8: Is the hedged report that never states adequacy correctly a context option, given it implies a Histology Report is in the file?
- option 1: Does an Imaging Report with no cytology or histology adequately describe "no tissue has been taken, or none will be", given that a planned biopsy cannot be shown by ticks?
- option 2: Does the Cytology tick correctly stand for an intraoperative frozen section or squash, noting that this option's captures record the evidence as Histology while the document definitions place it under Cytology?
- option 3: Options 3 to 7 record the specimen as adequate and no document can show adequacy, so is it acceptable that a ticked Histology Report takes an adequate option unless the clerk chooses the inadequate or hedged-report line?
- option 4: Is it right that the basic and surrogate-molecular immunohistochemistry options fit the same ticked sets, so the clerk is asked which panel the file holds?
- option 6: The label says "Histology plus a molecular result" but its captures also record IHC, so should the molecular options require the IHC Report, letting a Histology Report with a Gene report but no IHC Report fall to the H&E-only option (understating)?
- option 7: Is it right that the FISH/RT-PCR/Sanger/MLPA option and the methylation/next-generation-sequencing option fit the same ticked sets, so the clerk is asked which molecular test the file holds?
- option 8: Is the hedged-report option correctly a context line, given that it presumes a pathology report yet can be chosen with no Histology Report ticked?

### `md_document_inventory` (tree `g3_midline`)

*Question:* Sellar, suprasellar, pineal, optic pathway or cranial nerve lesion. What is in this patient's file?
*(question rewritten; it said: Sellar, suprasellar, pineal, optic pathway or cranial nerve lesion. What is in this patient's file?)*
*Hint rewritten:* Answer the specimen-adequacy selector too. The commonest failure in CNS pathology is not a missing test but an uninterpretable specimen, and a crush-artefact biopsy is not a negative biopsy. 'Not assessable' means the report does not say - it is not the same answer as 'inadequate' and it does not route the same way.

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | Referral or clinic letter only - it names a diagnosis, but there is no biopsy or imaging report in the file | tier | none of Imaging Report, Cytology, Histology Report | Lowest tier: no imaging, cytology or histology ticked; Lab, IHC or Gene reports alone fall here and understate. | high |
| 1 | Imaging only - MRI or CT report, no tissue | tier | needs Imaging Report; none of Lab Report, Cytology, Histology Report | Imaging with no hormone or marker result and no tissue; excluding Lab keeps it distinct from option 2. | medium |
| 2 | Hormone assays and imaging - a functioning pituitary tumour that has not been operated on | tier | needs Imaging Report and Lab Report; none of Cytology, Histology Report | Imaging plus a Lab Report read as the hormone assay; the pituitary wording cannot be expressed by the seven documents. | medium |
| 3 | Frozen section or squash cytology only - no definitive paraffin histology | tier | needs Cytology; none of Histology Report | Frozen section or squash without a definitive paraffin report is the Cytology document; IHC beside it stays at this tier. | medium |
| 4 | Histology report with H&E morphology only - no immunohistochemistry | tier | needs Histology Report; none of IHC Report | Histology with no IHC ticked; a Gene report without IHC lands here and understates. | high |
| 5 | Histology report with immunohistochemistry | tier | needs Histology Report and IHC Report; none of Gene reports for cancer | Histology with IHC and no Gene report. | high |
| 6 | Histology, immunohistochemistry and molecular or DNA methylation profiling | tier | needs Histology Report and IHC Report and Gene reports for cancer | Cumulative ladder: histology, IHC and molecular or methylation profiling all named, so all three are required. | medium |
| 7 | A specimen was taken but the report states it is inadequate, non-diagnostic or uninterpretable | context | special situation (always offered) | Inadequate, non-diagnostic or uninterpretable specimen is a statement about the specimen. | high |
| 8 | The report does not say whether the specimen was adequate - continue on what it does contain | context | special situation (always offered) | Report silent on adequacy is a statement about the report; it records no evidence tier. | medium |
| 9 | The compartment is not established - the file does not say whether the lesion is sellar, suprasellar, pineal or optic pathway | context | special situation (always offered) | Compartment not established is a situation that no document id expresses. | high |
| 10 | The file establishes a non-neoplastic lesion - Rathke cleft cyst, arachnoid cyst, hypophysitis, sellar tuberculoma, pineal cyst or an abscess | context | special situation (always offered) | Non-neoplastic lesion is a situation that no document id expresses. | high |

*For the registrar:*

- option 1: Does excluding the Lab Report from 'Imaging only' suit the registrar, given a ticked Lab Report could be an unrelated blood count rather than a hormone or marker assay?
- option 2: Is a ticked Lab Report acceptable as the hormone assay for 'Hormone assays and imaging', given a pineal file with an alpha-fetoprotein or human chorionic gonadotropin Lab Report would also be offered the pituitary wording?
- option 3: DATA GAP: the midline gate has only an intraoperative frozen-section or squash tier, so cerebrospinal-fluid cytology for a suspected germ cell tumour is described as intraoperative; should a cerebrospinal-fluid cytology option be added?
- option 4: A Histology Report plus a Gene report without an IHC Report falls to the H&E-only option; should that understatement stand?
- option 8: Is 'the report does not say whether the specimen was adequate' correctly a context option, given choosing it records no evidence tier?
- option 1: Is it right that the imaging-only option excludes a ticked Lab Report, so that imaging with any laboratory report goes to the hormone-assay option without a question?
- option 2: Does a ticked Lab Report correctly stand for the hormone assays in "hormone assays and imaging", given that the same tick may be an alpha-fetoprotein or human chorionic gonadotropin result and the label also asserts a functioning pituitary tumour that has not been operated on?
- option 3: Does the Cytology tick correctly stand for an intraoperative frozen section or squash, given that a cerebrospinal-fluid or fine-needle cytology report would also take this option?
- option 6: Should a file with a Histology Report and a Gene report but no IHC Report fall to the H&E-only option (understating), because the molecular option names immunohistochemistry as a rung?
- option 0: DATA GAP: Should the gate gain an option for a tumour-marker or hormone result in the file with no imaging report and no tissue, because a lone Lab Report now falls to the referral-only option, which routes to the referral wording and skips the germ cell marker question that every other option reaches?
- option 8: Is the "report does not say whether the specimen was adequate" option correctly a context line, given that it carries no evidence of its own and routes like the histology tiers?

### `sp_document_inventory` (tree `g3_spinal`)

*Question:* Spinal cord or cauda equina tumour. What reports are in this patient's file, and was the specimen adequate for diagnosis?
*Hint rewritten:* Intraspinal biopsy carries real morbidity, so an inadequate or absent specimen is common here and it changes the code. Inadequate is not a negative result, and an uninterpretable section is not an inadequate one — pick the line that says what actually happened. A tumour that turns out to arise from a nerve root, a vertebra or a paraspinal mass is not a Group III primary; there is a line for that too.

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | Referral letter or clinical note only — no imaging report, no cytology and no histology | tier | none of Imaging Report, Cytology, Histology Report | Lowest tier: no imaging, cytology or histology ticked; Lab, IHC or Gene reports alone fall here and understate. | high |
| 1 | MRI report only — no tissue was taken, and none is planned or available | tier | needs Imaging Report; none of Cytology, Histology Report | Imaging report with no tissue; the Imaging document also covers CT, which the label does not name. | medium |
| 2 | Intraoperative frozen section or squash cytology only — with or without a definitive paraffin report to follow | tier | needs Cytology; none of Histology Report | Frozen section or squash is the Cytology document; with a Histology Report ticked the file is higher. | medium |
| 3 | Definitive histology report — ADEQUATE specimen, H&E only, no immunohistochemistry available | tier | needs Histology Report; none of IHC Report | Definitive histology with no IHC ticked; a Gene report without IHC lands here and understates. | high |
| 4 | Definitive histology report — ADEQUATE specimen, with immunohistochemistry (GFAP, EMA, Olig2, S100, synaptophysin and similar) | tier | needs Histology Report and IHC Report | Histology with IHC and no Gene report. Registrar-session adjustment: Gene reports are no longer excluded, so a file with Histology, IHC and a Gene report is asked between this tier and the next. The next tier's label also claims "on fresh tissue", which a Gene report tick cannot establish, and the clerk may decline that claim. | high |
| 5 | Definitive histology report — ADEQUATE specimen, with immunohistochemistry AND FISH, RT-PCR or sequencing on fresh tissue | tier | needs Histology Report and IHC Report and Gene reports for cancer | Cumulative ladder: IHC and FISH, RT-PCR or sequencing both named, so Histology, IHC and Gene reports are all required. | medium |
| 6 | Biopsy taken but INADEQUATE — too little tissue, crush artefact, or the report says non-diagnostic | context | special situation (always offered) | Inadequate biopsy is a statement about the specimen. | high |
| 7 | Biopsy taken but NOT ASSESSABLE — the section or the stains could not be read at all (processing failure, tissue exhausted, block lost) | context | special situation (always offered) | Not-assessable section (processing failure, block lost) is a statement about the specimen. | high |
| 8 | The lesion is a deposit, a metastasis, a nerve sheath tumour, or a paraspinal or vertebral mass invading the canal | context | special situation (always offered) | Deposit, metastasis, nerve sheath or paraspinal mass redirects to another tree. | high |
| 9 | It cannot be established from the file that this is a spinal cord or cauda equina primary | context | special situation (always offered) | Spinal primary not established is a situation that no document id expresses. | high |

*For the registrar:*

- option 1: The label says 'MRI report only' but the Imaging Report document also covers CT and ultrasound; should a CT-only spinal file fit this option?
- option 2: The label allows a definitive paraffin report to follow, but I excluded a ticked Histology Report so that file fits the histology tiers; is that correct?
- option 2: DATA GAP: the spinal gate has only an intraoperative frozen-section or squash tier, so cerebrospinal-fluid or aspirate cytology is described as intraoperative; should an option for cytology without tissue be added?
- option 3: A Histology Report plus a Gene report without an IHC Report fits only the H&E-only option; should that understatement stand?
- option 5: The label requires FISH, RT-PCR or sequencing on fresh tissue, which no document id expresses and a Gene report on blood would also satisfy; is ticking the Gene report beside Histology and IHC enough?
- option 1: Does the Imaging Report tick adequately describe "MRI report only, no tissue taken, none planned or available", given that a CT or ultrasound report would also fit and a planned biopsy cannot be shown by ticks?
- option 2: The label reads "with or without a definitive paraffin report to follow": is it right that a ticked Histology Report moves the file to the histology tiers, so this option fits only Cytology without Histology Report?
- option 3: Options 3 to 5 record the specimen as adequate and no document can show adequacy, so is it acceptable that a ticked Histology Report takes an adequate option unless the clerk chooses the inadequate or not-assessable line?
- option 5: Should a file with a Histology Report and a Gene report but no IHC Report fall to the H&E-only option (understating), and is a gene report beside the histology enough to stand for FISH, RT-PCR or sequencing "on fresh tissue"?

### `mn_document_inventory` (tree `g3_meninges`)

*Question:* A meningeal lesion (C70.0 cerebral meninges, C70.1 spinal meninges, C70.9 meninges NOS). What is actually in this patient's file, and was the specimen adequate for diagnosis?
*Hint rewritten:* An inadequate or unreadable specimen is not a negative one and never closes to a code here - it leaves this tree. Benign behaviour does NOT leave the registry: this registry registers non-malignant CNS tumours, and six of the twelve meningioma codes are /0 only.

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | Referral letter or clinical note only - no pathology report and no imaging report in the file | tier | none of Imaging Report, Cytology, Histology Report | Lowest tier: no imaging, cytology or histology ticked; Lab, IHC or Gene reports alone fall here and understate. | high |
| 1 | Imaging report only - no tissue, no cytology | tier | needs Imaging Report; none of Cytology, Histology Report | Imaging with no tissue and no cytology. | high |
| 2 | Intraoperative frozen section or squash cytology only - no definitive paraffin-section report yet | tier | needs Cytology; none of Histology Report | Frozen section or squash without a definitive paraffin report is the Cytology document; IHC beside it stays at this tier. | medium |
| 3 | Tissue with a definitive H&E report - no immunohistochemistry (RL I) | tier | needs Histology Report; none of IHC Report | Tissue with H&E and no IHC ticked; a Gene report without IHC lands here and understates. | high |
| 4 | Tissue with H&E and immunohistochemistry (EMA, SSTR2A, STAT6, SOX10, SMARCE1, BAP1 and the like) - RL II-III | tier | needs Histology Report and IHC Report; none of Gene reports for cancer | Tissue with H&E and IHC and no Gene report. | high |
| 5 | Tissue with H&E, immunohistochemistry AND a molecular, copy-number or methylation result (FISH, MLPA, CMA, WES, methylation array) - RL IV-V | tier | needs Histology Report and IHC Report and Gene reports for cancer | Cumulative ladder: H&E, IHC and a molecular, copy-number or methylation result are all named, so all three are required. | medium |
| 6 | Specimen INADEQUATE / non-diagnostic - too little tissue, crush artefact, no lesional tissue identified | context | special situation (always offered) | Inadequate specimen is a statement about the specimen. | high |
| 7 | Specimen technically UNINTERPRETABLE - processing or stain failure, no opinion could be given on the cells present | context | special situation (always offered) | Technically uninterpretable specimen is a statement about the specimen. | high |
| 8 | The meningeal origin of the lesion is not established - it is not clear from the file whether the mass is dural, leptomeningeal or intraparenchymal | context | special situation (always offered) | Meningeal origin not established is a situation that no document id expresses. | high |
| 9 | The lesion proved NOT to be a neoplasm - tuberculoma, abscess, meningitis, inflammatory pseudotumour or demyelination | context | special situation (always offered) | Proven non-neoplastic lesion leaves the registry and is not a document tier. | high |

*For the registrar:*

- option 2: DATA GAP: the meninges gate has only an intraoperative frozen-section or squash tier, so cerebrospinal-fluid or aspirate cytology is described as intraoperative; should an option for cytology without tissue be added?
- option 3: A Histology Report plus a Gene report without an IHC Report fits only the H&E-only option; should that understatement stand?
- option 5: Gene reports may be germline, as in SMARCE1-related disease, so should a Gene report ticked beside Histology and IHC count as tissue copy-number or methylation testing?
- option 2: Does the Cytology tick correctly stand for an intraoperative frozen section or squash, given that a cerebrospinal-fluid or fine-needle cytology report would also take this option?
- option 3: Options 3 to 5 record the specimen as adequate and no document can show adequacy, so is it acceptable that a ticked Histology Report takes an adequate option unless the clerk chooses the inadequate or uninterpretable line?
- option 5: Should a file with a Histology Report and a Gene report but no IHC Report fall to the H&E-only option (understating), because the molecular option names immunohistochemistry as a rung?

### `un_document_inventory` (tree `g3_unspecified`)

*Question:* What is in this patient's file, and how far did the diagnosis actually get?
*(question rewritten; it said: What is in this patient's file, and how far did the diagnosis actually get?)*
*Hint rewritten:* Every case in this subgroup records five facts: (a) was surgery performed, (b) was tissue sent to pathology, (c) was immunohistochemistry requested, (d) was the result unavailable or never requested, and (e) the ENCR basis of diagnosis. The description of the file that applies sets them. A tumour that was never diagnosed is still a tumour with recoverable facts on it - record what the file has, not "unknown".

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | Death certificate only - the certificate names a brain or spinal tumour and there is no other document in the file | context | special situation (always offered) | A death certificate is not one of the seven documents; the clerk must be able to choose it whatever is ticked. | medium |
| 1 | Referral or clinical note only - no imaging report, no operation, no pathology | tier | none of Imaging Report, Cytology, Histology Report | Lowest tier: fits whenever no imaging, cytology or histology report is ticked, so nothing ticked and a lone Lab, IHC or Gene report land here (understates, the safe direction). 'No operation' cannot be shown by documents. | high |
| 2 | Imaging only - CT, MRI or ultrasound describes a mass and reads it as a tumour; no operation and no tissue | tier | needs Imaging Report; none of Cytology, Histology Report | Imaging Report with no cytology or histology. Lab is deliberately not excluded: the label does not say 'no marker result', and the Lab Report document is general (it may be an unrelated blood count), so hiding this option when Lab is ticked would force an imaging-only file into the marker/equivocal route. It fits the same sets as option 3 and the clerk is asked which describes the file. | medium |
| 3 | Imaging is in the file but it is equivocal, reads the lesion as something other than a tumour, or serum/CSF tumour markers were measured | tier | needs Imaging Report; none of Cytology, Histology Report | Imaging Report with no cytology or histology. The marker clause is one of three alternatives (equivocal imaging, a non-tumour reading, markers measured), so no Lab Report is required; a ticked Lab Report is read as the possible marker result and the next node asks which it is. | medium |
| 4 | An operation was performed and nothing reached the laboratory - a shunt, a decompression, a debulking recorded only in the operative note, or a biopsy that was abandoned | context | special situation (always offered) | An operation with no specimen is an event, not a document; the operative note has no id of its own, so the clerk must be able to choose it whatever is ticked. | medium |
| 5 | Tissue was taken and only an intraoperative preparation was reported - frozen section or squash/smear cytology; no paraffin report ever followed | tier | needs Cytology; none of Histology Report | A frozen section or squash/smear with no paraffin report is the Cytology document; IHC or Gene reports beside it stay at this tier (immunocytochemistry, not tissue); a Histology Report sends the file to option 7. | medium |
| 6 | Tissue was taken and a pathology report exists, but the specimen did not yield a diagnosis - too little tissue, no lesional tissue, or a section that could not be read | context | special situation (always offered) | A report exists but the specimen did not yield a diagnosis; adequacy is a statement about the specimen, not a document. | high |
| 7 | Tissue was taken, the section was adequate, and the report describes a neoplasm but names no entity | tier | needs Histology Report | The only histology tier in this gate, so it fits every set that ticks Histology Report, with or without IHC or Gene reports; the next node asks about IHC. Adequacy cannot be shown by documents, so a clerk with an inadequate specimen must choose option 6. | medium |
| 8 | Tissue was taken and reported somewhere, but the report itself is not in the file | context | special situation (always offered) | The report is missing from the file; the absence of a document cannot be ticked. | high |
| 9 | The lesion is documented as non-neoplastic - abscess, tuberculoma, granuloma, parasitic cyst, demyelination, infarct | context | special situation (always offered) | A non-neoplastic lesion is documented; a finding that redirects to another node, not a document tier. | high |
| 10 | A tumour is documented outside the nervous system and this lesion is a deposit from it | context | special situation (always offered) | A deposit from a tumour elsewhere redirects to another node; a dominant finding, not a document tier. | high |
| 11 | The site of the lesion has never been established - the file does not say where in the nervous system it is, or whether it is in the nervous system at all | context | special situation (always offered) | The site is not established; this does not follow from which documents exist. | high |

*For the registrar:*

- option 0: Should death certificate only be a context option, since a death certificate is not one of the seven documents?
- option 1: The label says 'no operation', which no document id expresses, so an operative note is read as the clinical note; is that acceptable?
- option 3: Is option 3 correctly a tier fitting every imaging-only file beside option 2, given it joins an equivocal imaging read with a tumour-marker result?
- option 3: A ticked Lab Report is read as the serum or cerebrospinal-fluid tumour marker result for option 3 and removes option 2; is that acceptable, given the Lab Report may be a blood count?
- option 4: Is 'an operation was performed and nothing reached the laboratory' correctly a context option, given the operative note has no document id and the option's captures record Imaging?
- option 5: DATA GAP: the unspecified gate has only an intraoperative frozen-section or squash tier, so cerebrospinal-fluid or aspirate cytology is described as intraoperative; should an option for cytology without tissue be added?
- option 7: Option 7 asserts an adequate section and a neoplasm with no entity named, which no document id expresses, so any Histology Report reaches it unless a context option is chosen; is that acceptable?
- option 0: Is it acceptable that a file with nothing ticked, which includes a death-certificate-only file, takes the "referral or clinical note only" option unless the clerk chooses the death-certificate line?
- option 1: Can the "no operation" wording of the referral-only option be left unchecked, given that an operative note is a clinical note and cannot be told apart by ticks?
- option 2: Is it right that the imaging-only option and the equivocal-imaging-or-marker option fit the same ticked sets, so every file with imaging and no tissue asks the clerk which describes it?
- option 3: Does a ticked Lab Report correctly stand for "serum or cerebrospinal-fluid tumour markers were measured", given that the option needs no Lab Report to fit and the next question asks for the specific result?
- option 4: Is the "operation performed and nothing reached the laboratory" option correctly a context line rather than a tier, given that an operation is not a document and an operative note would be ticked as a referral or clinical note?
- option 5: Does the Cytology tick correctly stand for a frozen section or squash/smear, given that a cerebrospinal-fluid or fine-needle cytology report would also take this option?
- option 7: Is it right that the only histology tier fits every set that ticks a Histology Report, including sets with IHC or gene reports, leaving the immunohistochemistry question to the next node?
- option 8: Is the "report is not in the file" option correctly a context line, given that the absence of a document cannot be ticked?
- option 1: DATA GAP: Should the gate gain an option for a serum or cerebrospinal-fluid tumour-marker result with no imaging report, because a lone Lab Report now falls to the referral-only option and never reaches the marker question that the imaging-incomplete node asks?
- option 2: Options 2 and 3 fit the same ticked sets (imaging with no cytology or histology, with or without a Lab Report), so every such file asks the clerk which describes it; is that acceptable, given that excluding Lab Report from option 2 would force an imaging-only file with an unrelated blood count into the marker route?
- option 3: Option 3 asserts that serum or cerebrospinal-fluid tumour markers were measured as one of three alternatives; is it acceptable that it fits without a Lab Report ticked, and that a ticked Lab Report is only read as the possible marker result (the Lab Report document is general and the next node asks for the specific result)?
- option 0: Should death certificate only be a context option, given that a death certificate is not one of the seven documents and a file with nothing ticked otherwise takes the referral-only option?
- option 1: DATA GAP: a lone Lab Report (possibly a serum or cerebrospinal-fluid tumour marker) with no imaging report falls to the referral-only option and never reaches the marker question that option 3 leads to; should the gate gain an option for a tumour-marker result with no imaging report?
- option 5: DATA GAP: a Cytology-only file of cerebrospinal-fluid or fine-needle aspirate cytology is described by an option that asserts an intraoperative frozen section or squash; should the gate gain a cytology-without-tissue option? Its captures also record the evidence as Histology while the document definitions place a frozen section or squash under Cytology.
- option 8: Is 'the report is not in the file' correctly a context option, given that the absence of a document cannot be ticked?

## Group 4

### `sa_document_inventory` (tree `g4_sympathoadrenal`)

*Question:* Sympathoadrenal-region mass — adrenal gland (C74.0, C74.1, C74.9), peripheral nerve or autonomic nervous system (C47.0–C47.9), retroperitoneum (C48.0, C48.2, C48.8), or mediastinum (C38.1–C38.3). What is actually in this patient's file, and was the specimen adequate for diagnosis?
*Hint rewritten:* This compartment holds two biologically distinct tumour families — the neuroblastic spectrum (neuroblastoma, ganglioneuroblastoma, ganglioneuroma) and the paraganglioma/pheochromocytoma family — plus, at the adrenal gland specifically, an epithelial differential (adrenocortical carcinoma). Record adequacy honestly: an uninterpretable specimen is not a negative one.

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | Referral letter or clinical note only — no imaging report, no laboratory result and no pathology report | tier | none of Cytology, Histology Report | Lowest tier. Excludes only the two pathology documents, so every set without cytology or histology fits it, including imaging-only and lab-only files and sets holding IHC or genetics alone, which understates. It cannot exclude imaging and lab because the gate has no imaging-only or lab-only option (DATA GAP). A file with imaging and lab ticked fits this option and option 1, and the clerk is asked. | medium |
| 1 | Imaging report (CT/MRI) with a biochemical or catecholamine work-up documented — no tissue and no cytology | tier | needs Imaging Report and Lab Report; none of Cytology, Histology Report | The label asserts imaging plus a documented biochemical work-up with no tissue and no cytology. Requires both documents; the Lab Report stands for the catecholamine or biochemical work-up (assumption e, flagged). Excludes cytology and histology per the label. | medium |
| 2 | Fine-needle aspiration or core-needle cytology only — no excisional or incisional biopsy report is in the file | tier | needs Cytology; none of Histology Report | Cytology with no histology report. IHC or genetics ticked beside cytology stays at this tier (immunocytochemistry, rule d). Imaging and lab do not change it. The label calls core-needle sampling cytology, which the seven-document definitions class as histology (flagged). | medium |
| 3 | Definitive histology report — no immunohistochemistry performed or reported | tier | needs Histology Report; none of IHC Report | Histology with no IHC reported, per the label. Genetics ticked beside histology without IHC falls here, because option 5 needs the IHC rung below it (rule c, flagged). | high |
| 4 | Definitive histology WITH immunohistochemistry — any of PHOX2B, synaptophysin, chromogranin A, GATA3 or cytokeratin reported | tier | needs Histology Report and IHC Report; none of Gene reports for cancer | Histology read with IHC and no molecular result. Excludes genetics so a file with all three fits option 5 only; both options route to the same IHC checklist. | high |
| 5 | Histology and immunohistochemistry PLUS cytogenetic or molecular testing — MYCN FISH, ALK testing, germline susceptibility gene testing, or another molecular result | tier | needs Histology Report and IHC Report and Gene reports for cancer | Cumulative ladder: the label names histology, IHC and cytogenetic or molecular testing, so all three are required. Histology plus genetics without IHC falls to option 3. | high |
| 6 | A specimen was taken but the report says it is inadequate, non-diagnostic, or crush artefact only | context | special situation (always offered) | Inadequate, non-diagnostic or crush-artefact specimen: a situation, not a document set. | high |
| 7 | Reviewed and NOT a neoplasm — adrenal haemorrhage, extramedullary haematopoiesis, or another non-neoplastic mass at this site | context | special situation (always offered) | Non-neoplastic lesion reviewed and excluded: a situation. Routes to a non-reportable exit. | high |

*For the registrar:*

- option 1: Option 1 asserts a biochemical or catecholamine work-up; does a ticked Lab Report adequately stand for the urinary homovanillic acid and vanillylmandelic acid, plasma or urinary metanephrine or chromogranin A result, given that the next question (which work-up the file describes) asks for the specific result?
- option 0: DATA GAP: this gate has no option for an imaging report without a biochemical work-up, or for a laboratory result without imaging, so those files fit only the referral-only option and the case is understated; should the gate gain 'Imaging report only, no biochemical work-up and no tissue'?
- option 0: A file with imaging and a Lab Report ticked fits both option 0 and option 1 because option 0 cannot exclude imaging or lab without stranding the imaging-only and lab-only files, so the clerk is asked between them; is that acceptable until the missing imaging-only option exists?
- option 2: Option 2 calls core-needle sampling cytology, but a core-needle biopsy is a tissue section and a clerk would tick Histology Report for it, which fits options 3 to 5; should core-needle be moved out of this label?
- option 3: Histology plus genetics with no IHC falls to option 3 (histology, no IHC) and cytology plus genetics falls to option 2, because option 5 needs histology and IHC and genetics together; is it right that the molecular result is dropped in those files?
- option 5: Option 5 counts germline susceptibility gene testing as molecular testing, so a Gene reports for cancer tick on a germline test lifts a histology-with-IHC file to the complete tier; is that intended?
- option 6: Is the inadequate, non-diagnostic or crush-artefact specimen (option 6) correctly a context option that stays available whatever is ticked?
- option 0: DATA GAP: no option describes an Imaging Report with no laboratory result and no tissue, or a lone Lab Report. Both land on option 0, whose label says no imaging report and no laboratory result, which understates; should the gate gain an option 'Imaging report only, no biochemical result, no tissue' routing to the same place as 'No biochemical marker was sent'?
- option 1: Is the general Lab Report document acceptable as the biochemical or catecholamine work-up that option 1 asserts, given that the next question (which work-up the file describes) asks for the specific result?
- option 0: Option 0 cannot exclude imaging and laboratory together, so a file with both an Imaging Report and a Lab Report fits options 0 and 1 and the clerk is asked; is that extra question acceptable, or would you rather option 0 excluded imaging and accept that an imaging-only file is then sent to option 1, whose label claims a work-up?
- option 2: This option groups core-needle sampling with fine-needle cytology, but a core-needle biopsy report is tissue; should a core-needle report be ticked as Histology Report (tissue tiers) or as Cytology?
- option 5: A gene report ticked beside a Histology Report but with no IHC Report falls to the histology-only option because the top rung names immunohistochemistry as well; is that understatement acceptable?

### `hn_document_inventory` (tree `g4_head_neck_paraganglia`)

*Question:* A head and neck paraganglioma is suspected (carotid body C75.4; aortic body and other paraganglia C75.5, which covers vagal, laryngeal and other extra-adrenal head and neck sites; middle ear C30.1). What is actually in this patient's file, and was the specimen adequate for diagnosis?
*Hint rewritten:* This tree has no imaging-sufficient route and no clinical-only route: Group IV has no Visser Table 3 entries at all, so a terminal without a tissue diagnosis never emits 8692/8690/8691/8693/8682/8680 — it refers to Group XII instead. An inadequate or unassessable specimen is treated the same way.

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | Referral letter or clinical note only — no pathology report and no imaging report in the file | tier | none of Imaging Report, Histology Report | Lowest tier. Excludes imaging (option 1 takes imaging files) and histology (option 2). Cytology-only and cytology-with-nothing-else files fall here because the gate has no cytology option (DATA GAP); a lone Lab Report, IHC or genetics also falls here, which understates. | medium |
| 1 | Imaging report only — no tissue, no cytology | tier | needs Imaging Report; none of Histology Report | Imaging report with no tissue report. Cytology is not excluded because a file with imaging and cytology would otherwise fit no tier; the label's 'no cytology' wording cannot be honoured (DATA GAP). The gate has no lab wording, so a Lab Report does not change the tier. | medium |
| 2 | Tissue with a definitive pathology report — with or without immunohistochemistry, with or without constitutional genetic testing | tier | needs Histology Report | Tissue report. IHC and genetics refine it only beside histology and the label allows either or neither, so neither is required or excluded. Cytology alone never fits here. | high |
| 3 | Specimen INADEQUATE or non-diagnostic — insufficient tissue, crush artefact, no lesional tissue identified | context | special situation (always offered) | Inadequate or non-diagnostic specimen: a situation, not a document set. | high |
| 4 | Specimen technically UNINTERPRETABLE — processing or stain failure, no opinion could be given on the cells present | context | special situation (always offered) | Technically uninterpretable specimen: a situation, not a document set. | high |

*For the registrar:*

- option 0: DATA GAP: the gate has no cytology option, so a cytology-only file falls to the referral-only option, whose label says no pathology report; should the gate gain 'Cytology only, no tissue'?
- option 1: DATA GAP: a file with imaging and cytology and no tissue fits the imaging-only option although its label says no cytology; should the missing cytology option be added so that wording holds?
- option 1: The gate has no laboratory wording, so a Lab Report ticked beside imaging leaves the tier at imaging only and a lone Lab Report falls to the referral-only option; is that correct for a paraganglioma work-up, where a metanephrine result is common?
- option 2: Option 2 allows constitutional genetic testing but needs only a Histology Report, so a gene report refines nothing here; confirm the label should not require any gene report.
- option 0: DATA GAP: the gate has no cytology tier, so a cytology-only file fits option 0 ('no pathology report'), and imaging plus cytology fits option 1 ('no cytology'); should the gate gain an option 'Cytology only, no tissue' routing to Group XII?
- option 2: An IHC Report or gene report ticked without the Histology Report sends the case to Group XII through option 0 and never reaches the paraganglioma panel; is that acceptable, given the clerk can tick the Histology Report to recover?

### `sn_document_inventory` (tree `g4_sinonasal`)

*Question:* A sinonasal or nasopharyngeal mass (C30.0 nasal cavity; C31.0-C31.9 paranasal sinuses; C11.0-C11.9 nasopharynx). What is actually in this patient's file, and was the specimen adequate for diagnosis?
*Hint rewritten:* This tree has no imaging-sufficient route and no clinical-only route: Group IV has no Visser Table 3 entries at all, so a terminal without a tissue diagnosis never emits 9522/9520/9521/9523 — it refers to Group XII instead. An inadequate or unassessable specimen is treated the same way.

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | Referral letter or clinical note only — no pathology report and no imaging report in the file | tier | none of Imaging Report, Histology Report | Lowest tier. Excludes imaging (option 1 takes imaging files) and histology (option 2). Cytology-only and cytology-with-nothing-else files fall here because the gate has no cytology option (DATA GAP); a lone Lab Report, IHC or genetics also falls here, which understates. | medium |
| 1 | Imaging report only — no tissue, no cytology | tier | needs Imaging Report; none of Histology Report | Imaging report with no tissue report. Cytology is not excluded because a file with imaging and cytology would otherwise fit no tier; the label's 'no cytology' wording cannot be honoured (DATA GAP). The gate has no lab wording, so a Lab Report does not change the tier. | medium |
| 2 | Tissue with a pathology report — with or without immunohistochemistry | tier | needs Histology Report | Tissue report. IHC and genetics refine it only beside histology and the label allows either or neither, so neither is required or excluded. Cytology alone never fits here. | high |
| 3 | Specimen INADEQUATE or non-diagnostic — insufficient tissue, crush artefact, no lesional tissue identified | context | special situation (always offered) | Inadequate or non-diagnostic specimen: a situation, not a document set. | high |
| 4 | Specimen technically UNINTERPRETABLE — processing or stain failure, no opinion could be given on the cells present | context | special situation (always offered) | Technically uninterpretable specimen: a situation, not a document set. | high |

*For the registrar:*

- option 0: DATA GAP: the gate has no cytology option, so a cytology-only file falls to the referral-only option, whose label says no pathology report; should the gate gain 'Cytology only, no tissue'?
- option 1: DATA GAP: a file with imaging and cytology and no tissue fits the imaging-only option although its label says no cytology; should the missing cytology option be added so that wording holds?
- option 2: Option 2 says tissue with a pathology report, with or without IHC, and needs only a Histology Report; confirm a cell block, which the document definitions class as histology, may satisfy it.
- option 0: DATA GAP: the gate has no cytology tier, so a cytology-only file fits option 0 ('no pathology report'), and imaging plus cytology fits option 1 ('no cytology'); should the gate gain an option 'Cytology only, no tissue' routing to Group XII?
- option 2: An IHC Report or gene report ticked without the Histology Report sends the case to Group XII through option 0 and never reaches the report-wording question; is that acceptable, given the clerk can tick the Histology Report to recover?

### `op_document_inventory` (tree `g4_other_peripheral`)

*Question:* What does the pathology file establish about this tumour, and where is it - record the topography first.
*Hint rewritten:* Record the topography exactly as documented before answering anything else. This tree covers every Group IV site this registry does not have a dedicated tree for, including a primary that was never established (C80.9). If the topography is a meningeal, brain, spinal cord or other central-nervous-system site (C70.0-C72.9), stop here and choose the first of the special situations listed under the boxes, because four of this group's codes belong to ICCC-3 Group III at that topography, whatever the pathology report says.

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | The topography recorded for this tumour is a meningeal, brain, spinal cord or other central-nervous-system site coded C70.0 through C72.9 | context | special situation (always offered) | A topography situation that redirects to the Group III tree, whatever documents exist. | high |
| 1 | No operation, biopsy or cytology preparation was ever performed - the tumour is known only from imaging, a clinical impression, or a referral note | tier | none of Histology Report | No tissue. Excludes histology only, so sets with no pathology, imaging, referral, lab, or IHC or genetics alone all fit. Cytology is not excluded because a cytology-only file would otherwise fit no tier, although the label says no cytology preparation was performed (DATA GAP). | medium |
| 2 | Tissue was obtained and examined, but the specimen was inadequate, non-diagnostic, or could not be assessed | context | special situation (always offered) | Inadequate, non-diagnostic or unassessable specimen: a situation, not a document set. | high |
| 3 | Tissue was examined and reported somewhere, but the report itself is not in this file | context | special situation (always offered) | The report is missing: a situation, not a document set. | high |
| 4 | The pathology report identifies Medulloepithelioma or Teratoid medulloepithelioma at this site | tier | needs Histology Report | The pathology report names the entity. Fits every set with a Histology Report; options 4 to 7 differ only by what the report states, which no document id expresses, so the clerk is asked among them. | medium |
| 5 | The pathology report uses the word "neuroepithelioma" in any form - "Neuroepithelioma, NOS", "peripheral neuroepithelioma", "peripheral PNET", "PPNET", or "peripheral (primitive) neuroectodermal tumour" | tier | needs Histology Report | Same fit as option 4: differs only by the wording the report uses. | medium |
| 6 | The pathology report confirms a paraganglioma-family tumour (paraganglioma, sympathetic paraganglioma, parasympathetic paraganglioma, or extra-adrenal paraganglioma), but the primary site is not one this registry's dedicated paraganglioma trees cover, or the primary site could not be established | tier | needs Histology Report | Same fit as option 4: differs only by the entity and site the report establishes. IHC is not required because the label does not name it. | medium |
| 7 | Tissue was examined and is adequate, and the report describes a neuroblastic, neuroendocrine or small round cell neoplasm, but none of the entities above is named | tier | needs Histology Report | Same fit as option 4: adequate tissue whose report names none of the entities above. | medium |

*For the registrar:*

- option 1: DATA GAP: the label says no biopsy or cytology preparation was performed, but the gate has no cytology option, so a cytology-only file fits this option and routes to Group XII; should the gate gain 'Cytology only, no tissue'?
- option 4: Options 4 to 7 describe what the pathology report states and not which documents exist, so each is mapped as a tier option needing a Histology Report and the clerk is asked among them; is it acceptable that they are tier rather than context options?
- option 6: Option 6 confirms a paraganglioma-family tumour by the pathology report alone, without requiring IHC; confirm a Histology Report is enough.
- option 0: Is it right that the central-nervous-system topography option is a context option available whatever is ticked?
- option 3: Option 3 (report examined elsewhere but not in the file) is a context option whose capture records Imaging as evidence; should it be a context option, and should the capture change?
- option 1: Is option 1 a tier (no Histology Report ticked) or a context option, given that its label asserts no operation, biopsy or cytology was ever performed, which an unticked box cannot establish and the 'report missing' option covers?
- option 1: DATA GAP: no option describes a cytology-only file; it fits option 1, whose label says no cytology preparation was performed, and routes to Group XII; should the gate gain an option 'Cytology only, no tissue'?
- option 6: Is option 6 (paraganglioma-family report, site not covered or not established) a tier requiring the Histology Report, or a context option because its second half states the site is not established?
- option 4: Are options 4 to 7, which state what the pathology report names, tier siblings that all require the Histology Report (so the clerk is asked among them after ticking it), or context options always choosable?

## Group 5

### `rb_document_inventory` (tree `g5_retinoblastoma`)

*Question:* A child with a suspected retinal tumour (retinoblastoma). What is actually in this patient's file?
*Hint rewritten:* Biopsy of an eye that still contains the tumour is avoided, because incisional or needle biopsy risks seeding the tumour outside the eye. A pathology report therefore exists only once the eye itself has been removed as treatment. B-scan ultrasound and orbital magnetic resonance imaging are not available everywhere, so the next step records which imaging was actually performed.

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | Referral letter or clinical note only — no ophthalmic examination or imaging report, no cytology, no pathology report in the file | tier | none of Imaging Report, Cytology, Histology Report | Lowest tier. Fits every set with no Imaging Report, Cytology or Histology Report, so a lone Lab Report, IHC Report or Gene report, or nothing ticked, lands here. Mirrors the label's three 'no' clauses. | high |
| 1 | Ophthalmic examination under anaesthesia, B-scan ultrasound, and/or orbital magnetic resonance imaging report — the eye is intact, no cytology, no pathology report | tier | needs Imaging Report; none of Cytology, Histology Report | Imaging Report ticked with no cytology and no pathology report, as the label states. Lab, IHC and genetics ticked beside imaging do not change the tier. 'Eye is intact' follows from the absence of a Histology Report. | high |
| 2 | Cytology report, or an aqueous-humour or plasma liquid biopsy report — no enucleation or exenteration specimen in the file | tier | needs Cytology; none of Histology Report | Requires the Cytology document itself (aqueous-humour or liquid-biopsy cytology is in its definition). IHC beside Cytology stays here as immunocytochemistry. Excludes Histology Report because the label says no enucleation or exenteration specimen is in the file; a set with Histology falls to the tissue tier. | medium |
| 3 | Enucleation or exenteration specimen with a pathology report | tier | needs Histology Report | The label asserts a pathology report on a tissue specimen, so it requires the Histology Report document. Histology outranks Cytology and Imaging. IHC or genetics alone never reach this tier. | high |
| 4 | A specimen (cytology, or enucleation/exenteration) was obtained but is reported INADEQUATE, non-diagnostic, or technically UNINTERPRETABLE | context | special situation (always offered) | States a quality finding (inadequate, non-diagnostic or uninterpretable specimen) that no document id can express. Always available, carries no tick rules. | high |

*For the registrar:*

- option 1: Option 1 names an ophthalmic examination under anaesthesia, which a clerk may tick as Referral Letter/Clinical Note rather than Imaging Report; such a file falls to option 0, which says no ophthalmic examination is in the file, so does the registrar accept that understatement or want the examination-under-anaesthesia note counted as Imaging Report?
- option 2: Option 2 includes a plasma liquid biopsy report, but a cell-free DNA gene report ticked as Gene reports for cancer never raises a tier, so it falls to imaging or referral; should the clerk be told to tick plasma and aqueous-humour liquid-biopsy reports as Cytology, or is the understatement acceptable?
- option 3: Option 3 asserts an enucleation or exenteration specimen but fits any Histology Report, including a biopsy of an extraocular or metastatic site; is that acceptable given that biopsy of an intact eye is avoided and the Histology Report is read as the enucleation report?
- option 2: Does the registrar accept that Cytology plus IHC Report with no Histology Report stays at option 2 as immunocytochemistry, since this gate says nothing about a cell block?
- A germline RB1 gene report or any other Gene report in this file never changes the tier because no option of this gate asks about genetics; is that the intended behaviour?
- option 4: Option 4 is treated as context and is available whatever is ticked, including when neither Cytology nor Histology Report is ticked; is that acceptable for an inadequate-specimen finding?
- option 0: A file holding only a Lab Report, IHC Report or Gene reports (for example a germline RB1 result) fits the referral-only tier, whose label says 'only'; is that understatement acceptable?
- option 1: Option 1 names an examination under anaesthesia, which is usually recorded in a clinical note and not in an Imaging Report; the mapping requires the Imaging Report, so a file with an examination note but no imaging report falls to the referral tier, and is that acceptable?
- option 2: A plasma liquid-biopsy report is often a cell-free DNA assay; should the clerk tick it as Cytology (as the document definition lists liquid-biopsy cytology) or as Gene reports, given that the mapping requires the Cytology document and a Gene report alone falls to a lower tier?
- option 3: Option 3 asserts an enucleation or exenteration specimen but the Histology Report document also covers other tissue (for example a bone marrow trephine or an orbital biopsy); is it safe to treat any Histology Report in a retinoblastoma file as the enucleation or exenteration report?
- option 4: Option 4 is treated as a context option because specimen adequacy cannot be read from the documents; do you agree, noting that a clerk with a Cytology or Histology Report ticked must still choose it deliberately?

## Group 6

### `rn_document_inventory` (tree `g6_renal`)

*Question:* A child with a suspected renal (kidney) tumour. What is actually in this patient's file?
*Hint rewritten:* Under SIOP protocols, up-front chemotherapy without a prior biopsy is standard for a typical Wilms tumour presentation, so a histology report often does not exist yet at the point of coding — that is expected, not a gap to chase.

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | Referral letter or clinical note only — no imaging report, no cytology, no histology report in the file | tier | none of Imaging Report, Cytology, Histology Report | Lowest tier. Fits every set with no Imaging Report, Cytology or Histology Report, so a lone Lab Report, IHC Report or Gene report, or nothing ticked, lands here. | high |
| 1 | Ultrasound, CT, or MRI report — no tissue (cytology or histology) in the file | tier | needs Imaging Report; none of Cytology, Histology Report | Imaging Report ticked and no tissue of either kind, matching the label's 'no tissue (cytology or histology)'. Lab, IHC and genetics beside imaging do not change the tier. | high |
| 2 | Histology report from a nephrectomy, core biopsy, or intraoperative specimen | tier | needs Histology Report | Tissue section report, so it requires the Histology Report document. It outranks Cytology and Imaging, so a set holding Histology plus anything else routes here. IHC or genetics alone never reach this tier. | high |
| 3 | Fine-needle aspiration or other cytology report only — no histology report in the file | tier | needs Cytology; none of Histology Report | Requires the Cytology document and excludes Histology Report, as the label says 'no histology report in the file'. IHC beside Cytology without Histology stays here as immunocytochemistry. | high |
| 4 | A specimen (cytology, or biopsy/nephrectomy) was obtained but is reported INADEQUATE, non-diagnostic, or technically UNINTERPRETABLE | context | special situation (always offered) | States a quality finding (inadequate, non-diagnostic or uninterpretable specimen) that no document id can express. Always available, carries no tick rules. | high |

*For the registrar:*

- option 2: Option 2 lists an intraoperative specimen as histology, but an intraoperative frozen section or squash with no definitive report is Cytology under the document list and would fall to option 3; does the registrar accept that, with only a definitive frozen-section report counting as Histology Report?
- option 3: Option 3 treats fine-needle aspiration and any other smear or fluid morphology as Cytology and keeps IHC beside it at the cytology tier; is that the registrar's reading, given that the gate does not mention a cell block?
- option 4: Option 4 is treated as context and is available whatever is ticked, including when neither Cytology nor Histology Report is ticked; is that acceptable for an inadequate-specimen finding?
- option 0: A file holding only a Lab Report, IHC Report or Gene reports fits the referral-only tier, whose label says 'only'; is that understatement acceptable?
- option 2: Option 2 includes an intraoperative specimen; the mapping treats a definitive frozen-section report as Histology Report while a frozen section or squash with no definitive report is ticked as Cytology and so falls to the cytology tier, and is that the intended reading?
- option 3: Option 3 says 'cytology report only', but the mapping also fits a file with an imaging report beside the cytology (no other option can hold that file); is it right to read 'only' as meaning no histology report?
- option 4: Option 4 is treated as a context option because specimen adequacy cannot be read from the documents; do you agree, noting that a clerk with a Cytology or Histology Report ticked must still choose it deliberately?

## Group 7

### `hp_document_inventory` (tree `g7_hepatic`)

*Question:* A child with a liver (hepatic) mass. What is actually in this patient's file?
*Hint rewritten:* When the file holds both a biopsy taken before chemotherapy and a resection taken after it, code from the biopsy: after chemotherapy about 20% of hepatoblastomas show areas that mimic hepatocellular carcinoma (López-Terrada 2025, p. 27).

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | Referral letter or clinical note only — no imaging report, no cytology, no histology report in the file | tier | none of Imaging Report, Cytology, Histology Report | Lowest tier. It fits any set with no Imaging Report, Cytology or Histology Report, so nothing ticked, a referral alone, and a lone Lab Report, IHC Report or Gene report all land here. Lab, IHC and genetics are deliberately not excluded: they cannot raise a tier without the document they are read against, and excluding them would dead-end those sets. | high |
| 1 | Ultrasound, CT or MRI report, with or without a serum alpha-fetoprotein result — no tissue (cytology or histology) in the file | tier | needs Imaging Report; none of Cytology, Histology Report | Requires the Imaging Report and excludes the two tissue documents to honour 'no tissue'. The label says 'with or without' serum alpha-fetoprotein, so Lab Report is optional and is not required; the next node (hp_imaging_pathway) asks for the actual marker result. IHC or genetics ticked beside imaging without a tissue document stay at this tier, which understates. | high |
| 2 | Histology report from a needle or wedge biopsy, a resection, a transplant hepatectomy or an autopsy | tier | needs Histology Report | Fits every set that holds the Histology Report, whatever else is ticked, so it is the highest tier and the only fit for those sets. IHC and genetics refine the histology tier only beside the Histology Report, and need no separate option here. | high |
| 3 | Fine-needle aspiration or other cytology report only — no histology report in the file | tier | needs Cytology; none of Histology Report | Requires the Cytology document itself and excludes Histology Report to honour 'no histology report'. Imaging may also be ticked, because cytology outranks imaging in the old ladder. IHC beside cytology stays here (immunocytochemistry), as does genetics. | high |
| 4 | A specimen was taken but is reported inadequate, non-diagnostic or uninterpretable | context | special situation (always offered) | An inadequate, non-diagnostic or uninterpretable specimen is a situation that does not follow from which documents exist, so it is a context option with no tick rules. The clerk can choose it with any ticked set. | high |

*For the registrar:*

- option 0: A file with only a Lab Report (for example a serum alpha-fetoprotein), an IHC Report or a Gene report and no imaging or tissue falls to the referral-or-note tier, which understates but is not literally 'a referral only'; is that acceptable, or does the gate need an option for a laboratory result alone?
- option 1: The imaging tier fits whether or not a Lab Report is ticked because the label says 'with or without a serum alpha-fetoprotein result'; confirm that the alpha-fetoprotein result is to be asked only at the next node (hp_imaging_pathway) and never inferred from the Lab Report tick.
- option 2: The histology label includes a transplant hepatectomy and an autopsy; should an autopsy histology report count as the Histology Report document, and should a cell block from a fine-needle aspirate route to this tier rather than the cytology tier?
- option 3: IHC ticked beside a Cytology document with no Histology Report stays at the cytology tier as immunocytochemistry; is that the intended reading for a liver aspirate that carries a marker panel?
- option 1: Option 1 fits imaging whether or not a Lab Report is ticked, because the label says 'with or without' alpha-fetoprotein and the imaging pathway asks for the specific result next; do you accept that a ticked Lab Report never changes the tier here?
- option 0: A file holding only a Lab Report (for example a serum alpha-fetoprotein result with no imaging report), only an IHC Report or only a Gene report falls to the referral-only tier, which understates it; do you accept that, given the referral wording node already lets the clerk record reported imaging or alpha-fetoprotein?
- option 2: Does an autopsy report, a transplant hepatectomy report and a needle or wedge biopsy report all count as the Histology Report document, so that option 2 fits any of them?
- option 3: Option 3 is worded 'cytology only' but fits a file that also holds an imaging report, since cytology outranks imaging and the 'only' refers to tissue; is that the intended reading?
- option 4: A clerk who ticks the Histology Report or Cytology document for a specimen the report calls inadequate would fit the histology or cytology tier unless the clerk also chooses option 4, so the tick rules alone cannot catch an inadequate specimen; is it acceptable that this depends on the clerk choosing the context option?
- Gate 7 has no immunohistochemistry or genetics tier, so IHC beside the Histology Report stays at the histology tier and IHC beside Cytology stays at the cytology tier; do you accept that no tier here expresses immunohistochemistry or genetic evidence?

## Group 8

### `bn_document_inventory` (tree `g8_bone`)

*Question:* A suspected malignant bone tumour. What is actually in this patient's file?
*Hint rewritten:* A radiology report counts as imaging. A pathology report on a biopsy, curettage or resection counts as histology.

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | Referral letter or clinical note only — no imaging report, no cytology, no histology report in the file | tier | none of Imaging Report, Cytology, Histology Report | Lowest tier. It fits any set with no Imaging Report, Cytology or Histology Report, including nothing ticked and a lone Lab Report, IHC Report or Gene report. Lab, IHC and genetics are not excluded, so those sets do not dead-end and the tier understates rather than overstates. | high |
| 1 | X-ray, CT or MRI report — no tissue (cytology or histology) in the file | tier | needs Imaging Report; none of Cytology, Histology Report | Requires the Imaging Report and excludes Cytology and Histology Report to honour 'no tissue'. Lab, IHC and genetics ticked beside imaging without a tissue document stay at this tier, which understates. The gate has no laboratory tier, so Lab Report does not change the fit. | high |
| 2 | Histology report from a biopsy, curettage or resection | tier | needs Histology Report | Fits every set that holds the Histology Report. It is the highest tier and the only fit for those sets. IHC and genetics refine it only beside the Histology Report and need no separate option. | high |
| 3 | Fine-needle aspiration or other cytology report only — no histology report | tier | needs Cytology; none of Histology Report | Requires the Cytology document itself and excludes Histology Report to honour 'no histology report'. Imaging may also be ticked. IHC beside cytology is immunocytochemistry and stays at this tier; genetics beside cytology likewise. | high |
| 4 | A specimen was taken but the report calls it inadequate, non-diagnostic or uninterpretable | context | special situation (always offered) | An inadequate, non-diagnostic or uninterpretable specimen does not follow from which documents exist. It is a context option with no tick rules. | high |
| 5 | The tumour arises in soft tissue, not bone — the mass is outside the bone and the cortex is intact | context | special situation (always offered) | The site is not established as bone and the option redirects to Group IX. That is a situation, not a document combination, so it is a context option with no tick rules and the clerk can always choose it. | medium |

*For the registrar:*

- option 0: A file with only a Lab Report, an IHC Report or a Gene report and no imaging or tissue falls to the referral-or-note tier, which understates; is that acceptable, or does the bone gate need an option for those files?
- option 1: The imaging label names X-ray, CT or MRI, but the Imaging Report document also covers ultrasound, PET and skeletal survey; should an ultrasound, PET or skeletal-survey report in a bone-tumour file count at the imaging tier, as the hint's 'a radiology report counts as imaging' implies?
- option 5: The soft-tissue-not-bone option states an imaging finding (mass outside the bone, cortex intact) yet carries no Imaging Report tick rule because it is a context option that redirects to Group IX; confirm it stays context rather than a tier.
- option 0: A file holding only a Lab Report, only an IHC Report or only a Gene report falls to the referral-only tier, which understates it; do you accept that for bone tumours?
- option 1: Option 1 counts a radiology report of any kind (X-ray, CT, MRI, and by the document definition also PET or skeletal survey) as the Imaging Report; is that acceptable although the label names only X-ray, CT or MRI?
- option 2: Does a curettage pathology report count as the Histology Report document alongside biopsy and resection reports, so that option 2 fits it?
- option 3: Option 3 is worded 'cytology only' but fits a file that also holds an imaging report, since cytology outranks imaging and the 'only' refers to tissue; is that the intended reading?
- option 4: A clerk who ticks the Histology Report or Cytology document for a specimen the report calls inadequate would fit the histology or cytology tier unless the clerk also chooses option 4, so the tick rules alone cannot catch an inadequate specimen; is it acceptable that this depends on the clerk choosing the context option?
- option 5: Is the soft-tissue origin option rightly a context option, available whatever is ticked, since the origin finding redirects to Group IX and does not follow from which documents exist?
- Gate 8 has no immunohistochemistry or genetics tier, so IHC beside the Histology Report stays at the histology tier and IHC beside Cytology stays at the cytology tier; do you accept that no tier here expresses immunohistochemistry or genetic evidence?

## Group 9

### `st_document_inventory` (tree `g9_soft_tissue`)

*Question:* A child or adolescent with a suspected soft tissue sarcoma. What is actually in this patient's file?
*Hint rewritten:* A histology report is the usual basis for a soft tissue sarcoma code. Without one, only a few codes can be registered at all.

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | Referral letter or clinical note only — no imaging report, no cytology, no histology report in the file | tier | none of Imaging Report, Cytology, Histology Report | Lowest tier. The label excludes imaging, cytology and histology. A lone Lab Report, IHC Report or Gene report names none of those, so such sets fall here, which understates the file and is the safe direction. Together with options 1 to 3 every one of the 128 sets fits exactly one tier. | high |
| 1 | Ultrasound, CT or MRI report — no cytology or histology in the file | tier | needs Imaging Report; none of Cytology, Histology Report | Needs the Imaging Report document and excludes the two higher tiers named in the label. Lab, IHC and genetics ticks beside imaging do not change the tier because the label asserts none of them. | high |
| 2 | Fine-needle aspiration or other cytology report only — no histology report | tier | needs Cytology; none of Histology Report | Requires the Cytology document itself. IHC beside Cytology with no Histology Report stays here as immunocytochemistry, because the option wording names no cell block or tissue. Imaging may also be ticked, since the label says cytology only against histology, not against imaging; the higher evidence wins. | high |
| 3 | Histology report from a biopsy or a resection | tier | needs Histology Report | Highest tier. Requires the Histology Report document, with no other restriction; the destination question (st_report_contents) asks what else the pathology file holds, so IHC and genetics ticks refine it there. | high |
| 4 | A specimen was taken but the report calls it inadequate, non-diagnostic or uninterpretable | context | special situation (always offered) | States the quality of a specimen, which no document id can express. It captures evidence_tests [] and basis_evidence_tier inadequate_specimen, and routes to st_imaging_report, which has its own 'No imaging report in the file' branch. Always available. | high |

*For the registrar:*

- option 1: The label names only ultrasound, CT or MRI, but the Imaging Report document also covers X-ray, PET and skeletal survey; should a plain X-ray or PET report count as this tier, as the mapping assumes?
- option 0: A file holding only a Lab Report, IHC Report or Gene report (no imaging, cytology or histology) falls to the referral-only tier because those documents cannot lift a tier on their own; is that the right way to record such a file?
- option 2: When the clerk ticks Cytology and IHC together with no Histology Report, the mapping keeps the cytology tier (immunocytochemistry) even though the next question (st_cytology) offers cell-block stain wording; is that correct, or should a cell block be a separate document?
- option 4: Is the inadequate, non-diagnostic or uninterpretable specimen option correctly a context option that is always available, given that it routes to the imaging-conclusion question and captures no evidence test?
- option 3: The Histology Report document includes a cell block, but this tree's cytology node (st_cytology) treats cell-block stains as cytology evidence at basis 5, so a clerk who ticks Histology Report for a cell block alone would reach the histology tier at basis 7; should the Histology Report tick be restricted to tissue sections for this group?
- option 0: Should a file with nothing ticked, or holding only a lab report, IHC report or gene report with no imaging, cytology or histology, fall to the referral-only tier, which understates the file but never claims a document that was not ticked?
- option 1: The Imaging Report document also covers X-ray, PET and skeletal survey, while the label names ultrasound, CT or MRI; is it acceptable that any imaging report raises the imaging tier, given that the next question asks for the radiologist's conclusion?
- option 2: The cytology label says 'cytology report only', but an Imaging Report ticked beside cytology still fits this tier; is the cytology tier the correct highest tier when imaging is also in the file, given that a non-diagnostic cytology result drops to the imaging conclusion?
- option 4: Is 'a specimen was taken but the report calls it inadequate, non-diagnostic or uninterpretable' correctly a context option that the clerk can always select, even when no histology or cytology document is ticked?

### `sk_document_inventory` (tree `g9_skin`)

*Question:* A child or adolescent with a skin lesion suspected to be a soft tissue sarcoma, most often Kaposi sarcoma. What is actually in this patient's file?
*Hint rewritten:* A histology report is the usual basis for a soft tissue sarcoma code. Without one, only a few codes can be registered at all.

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | Referral letter or clinical note only — no imaging report, no cytology, no histology report in the file | tier | none of Imaging Report, Cytology, Histology Report | Lowest tier. The label excludes imaging, cytology and histology. A lone Lab Report, IHC Report or Gene report names none of those, so such sets fall here, which understates the file and is the safe direction. Together with options 1 to 3 every one of the 128 sets fits exactly one tier. | high |
| 1 | Ultrasound, CT or MRI report — no cytology or histology in the file | tier | needs Imaging Report; none of Cytology, Histology Report | Needs the Imaging Report document and excludes the two higher tiers named in the label. Lab, IHC and genetics ticks beside imaging do not change the tier because the label asserts none of them. | high |
| 2 | Fine-needle aspiration or other cytology report only — no histology report | tier | needs Cytology; none of Histology Report | Requires the Cytology document itself. IHC beside Cytology with no Histology Report stays here as immunocytochemistry, because the option wording names no cell block or tissue. Imaging may also be ticked, since the label says cytology only against histology, not against imaging; the higher evidence wins. | high |
| 3 | Histology report from a biopsy or a resection | tier | needs Histology Report | Highest tier. Requires the Histology Report document, with no other restriction; the destination question (st_report_contents) asks what else the pathology file holds, so IHC and genetics ticks refine it there. | high |
| 4 | A specimen was taken but the report calls it inadequate, non-diagnostic or uninterpretable | context | special situation (always offered) | States the quality of a specimen, which no document id can express. It captures evidence_tests [] and basis_evidence_tier inadequate_specimen, and routes to st_imaging_report, which has its own 'No imaging report in the file' branch. Always available. | high |

*For the registrar:*

- option 1: The skin gate's imaging option routes to the soft-tissue tree's st_imaging_report and the label names only ultrasound, CT or MRI; should an X-ray or PET report count as this tier here too?
- option 0: A skin file holding only a Lab Report, IHC Report or Gene report falls to the referral-only tier and then to sk_clinical_alias, where Kaposi sarcoma can be registered from a clinical note alone; is that acceptable for a file with a gene report or IHC but no tissue document?
- option 2: For the skin gate, Cytology plus IHC with no Histology Report stays at the cytology tier; is that correct for a suspected Kaposi sarcoma, where an LANA-1 (HHV-8) stain on a smear is possible?
- option 4: Is the inadequate-specimen option correctly a context option in the skin gate, given that it routes to st_imaging_report in the soft-tissue tree rather than to a skin node?
- option 0: Once any imaging, cytology or histology report is ticked, the skin tree can no longer reach the clinical-note Kaposi sarcoma branch (basis 1) in sk_clinical_alias, because a clerk could previously pick the referral tier deliberately; is it correct that a skin file with an imaging report is coded from the imaging conclusion rather than from Kaposi sarcoma recognised on examination?
- option 3: The same cell-block question applies to the skin tree, which routes histology to st_report_contents: should a cell block ticked as Histology Report reach the tissue tier here?
- option 1: The skin gate routes its imaging, cytology, histology and inadequate-specimen options to the soft tissue nodes (st_imaging_report, st_cytology, st_report_contents); is that sharing intended for skin lesions?

## Group 10

**Changed 6 October 2026 (registrar's ruling: the laboratory screen follows the checklist, and only when Lab Report is
ticked).** Each Group X gate now has eight options. Options 0, 4 and 6 are copies of the referral, cytology and histology
tiers that add Lab Report to the rule and route through a laboratory screen to the tier's own destination; options 1, 5 and
7 are those tiers with Lab Report excluded. Option 2 (imaging and a marker result) keeps its rule and routes through its
laboratory screen; option 3 (imaging only) is unchanged. Labels and captures are the tiers' own, so with Lab Report unticked
every route is the one in the tables below. The tables keep the five tiers as they were derived; the indices in
`docs/evidence_documents/group_10.json` are the eight options.

### `cn_document_inventory` (tree `g10_cns`)

*Question:* What is in the file for this tumour?
*Hint rewritten:* A radiology report counts as imaging. A pathology report on a biopsy or resection counts as histology. A biopsy or cytology report that calls the specimen inadequate or non-diagnostic counts as no tissue: pick from the other tiers.

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | A referral letter or clinical note only — no imaging report, no marker result, no tissue | tier | none of Imaging Report, Cytology, Histology Report | Lowest tier: fits when no imaging, cytology or histology document is ticked, so it catches nothing ticked, a lone Lab Report, and IHC or Gene reports without the document they are read against (all understate, the safe direction). | high |
| 1 | An imaging report and a serum or cerebrospinal fluid alpha-fetoprotein or human chorionic gonadotropin result — no tissue | tier | needs Imaging Report and Lab Report; none of Cytology, Histology Report | Needs the Imaging Report and the Lab Report (assumed to hold the alpha-fetoprotein or human chorionic gonadotropin result); the label's 'no tissue' excludes Cytology and Histology Report. The next node asks for the specific marker result. | medium |
| 2 | An imaging report only — no marker result, no tissue | tier | needs Imaging Report; none of Lab Report, Cytology, Histology Report | Imaging Report alone, honouring 'no marker result, no tissue' by excluding Lab Report, Cytology and Histology Report; sibling to option 1, so imaging with a Lab Report fits only option 1. | high |
| 3 | Cytology only — cerebrospinal fluid, effusion or fine-needle aspirate; no tissue | tier | needs Cytology; none of Histology Report | Needs the Cytology document itself (cerebrospinal-fluid cytology, effusion, aspirate); Histology Report excluded because the label says no tissue. IHC or genetics beside Cytology stays here (immunocytochemistry, no cell block named); imaging or lab beside Cytology also lands here. | high |
| 4 | A histology report — biopsy or resection | tier | needs Histology Report | Histology Report ticked; the top tier regardless of other documents, with IHC and genetics refining it only beside the report. | high |

*For the registrar:*

- option 1: Option 1 fits any file that ticks the Imaging Report and the general Lab Report, so is it acceptable that a Lab Report holding only a blood count, with no alpha-fetoprotein or human chorionic gonadotropin result, still offers the marker route (the next node asks for the specific result)?
- option 0: DATA GAP: a file holding a serum or cerebrospinal fluid marker result with no imaging report and no tissue fits only option 0, whose label says 'no marker result', so should the gate gain an option such as 'A serum or cerebrospinal fluid marker result only, no imaging report, no tissue'?
- option 0: Is it acceptable that IHC or Gene reports ticked without a Cytology or Histology Report (for example a germline or liquid-biopsy gene report) fall to option 0, and that a set with both Cytology and Histology Report ticked ignores the cytology?
- option 3: Is it acceptable that imaging and marker results ticked beside a Cytology document fit only the cytology option (which excludes only Histology Report), so that the marker route of option 1 is never offered when cytology is present, and that IHC beside Cytology stays at the cytology tier as immunocytochemistry?
- The old hint said an inadequate or non-diagnostic biopsy or cytology report counts as no tissue and the gate has no context option for it, so is it acceptable that the clerk is told to leave such a report unticked rather than the engine detecting it?
- option 1: Does the registrar accept that ticking the general Lab Report document is taken to mean the serum or cerebrospinal fluid alpha-fetoprotein or human chorionic gonadotropin result named in the label, given that the next question (cn_markers) asks for the specific result?
- option 0: A file with only a Lab Report, IHC Report or Gene reports ticked falls to the referral-or-clinical-note tier although the label says no marker result; does the registrar accept this understatement rather than a separate tier?
- option 3: A file with Cytology plus an Imaging Report or Lab Report but no Histology Report fits the cytology tier despite the word only in the label, and IHC ticked beside Cytology stays at the cytology tier as immunocytochemistry; does the registrar accept both?
- The gate has no context option for a biopsy or cytology report that calls the specimen inadequate or non-diagnostic; the hint tells the clerk to leave such a report unticked, so the file drops to a lower tier. Does the registrar want that handled by the hint alone?

### `ov_document_inventory` (tree `g10_ovary`)

*Question:* What is in the file for this tumour?
*Hint rewritten:* A radiology report counts as imaging. A pathology report on a biopsy or resection counts as histology. A biopsy or cytology report that calls the specimen inadequate or non-diagnostic counts as no tissue: pick from the other tiers.

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | A referral letter or clinical note only — no imaging report, no marker result, no tissue | tier | none of Imaging Report, Cytology, Histology Report | Lowest tier: fits when no imaging, cytology or histology document is ticked, so it catches nothing ticked, a lone Lab Report, and IHC or Gene reports without the document they are read against (all understate, the safe direction). | high |
| 1 | An imaging report and a serum or cerebrospinal fluid alpha-fetoprotein or human chorionic gonadotropin result — no tissue | tier | needs Imaging Report and Lab Report; none of Cytology, Histology Report | Needs the Imaging Report and the Lab Report (assumed to hold the alpha-fetoprotein or human chorionic gonadotropin result); the label's 'no tissue' excludes Cytology and Histology Report. The next node asks for the specific marker result. | medium |
| 2 | An imaging report only — no marker result, no tissue | tier | needs Imaging Report; none of Lab Report, Cytology, Histology Report | Imaging Report alone, honouring 'no marker result, no tissue' by excluding Lab Report, Cytology and Histology Report; sibling to option 1, so imaging with a Lab Report fits only option 1. | high |
| 3 | Cytology only — cerebrospinal fluid, effusion or fine-needle aspirate; no tissue | tier | needs Cytology; none of Histology Report | Needs the Cytology document itself (effusion, aspirate, fluid cytology); Histology Report excluded because the label says no tissue. IHC or genetics beside Cytology stays here (immunocytochemistry, no cell block named); imaging or lab beside Cytology also lands here. | high |
| 4 | A histology report — biopsy or resection | tier | needs Histology Report | Histology Report ticked; the top tier regardless of other documents, with IHC and genetics refining it only beside the report. | high |

*For the registrar:*

- option 1: Option 1 fits any file that ticks the Imaging Report and the general Lab Report, so is it acceptable that a Lab Report holding only a blood count, with no alpha-fetoprotein or human chorionic gonadotropin result, still offers the marker route (the next node asks for the specific result)?
- option 0: DATA GAP: a file holding a serum or cerebrospinal fluid marker result with no imaging report and no tissue fits only option 0, whose label says 'no marker result', so should the gate gain an option such as 'A serum or cerebrospinal fluid marker result only, no imaging report, no tissue'?
- option 0: Is it acceptable that IHC or Gene reports ticked without a Cytology or Histology Report (for example a germline or liquid-biopsy gene report) fall to option 0, and that a set with both Cytology and Histology Report ticked ignores the cytology?
- option 3: Is it acceptable that imaging and marker results ticked beside a Cytology document fit only the cytology option (which excludes only Histology Report), so that the marker route of option 1 is never offered when cytology is present, and that IHC beside Cytology stays at the cytology tier as immunocytochemistry?
- The old hint said an inadequate or non-diagnostic biopsy or cytology report counts as no tissue and the gate has no context option for it, so is it acceptable that the clerk is told to leave such a report unticked rather than the engine detecting it?
- option 1: Does the registrar accept that ticking the general Lab Report document is taken to mean the serum or cerebrospinal fluid alpha-fetoprotein or human chorionic gonadotropin result named in the label, given that the next question (ov_markers) asks for the specific result?
- option 0: A file with only a Lab Report, IHC Report or Gene reports ticked falls to the referral-or-clinical-note tier although the label says no marker result; does the registrar accept this understatement rather than a separate tier?
- option 3: A file with Cytology plus an Imaging Report or Lab Report but no Histology Report fits the cytology tier despite the word only in the label, and IHC ticked beside Cytology stays at the cytology tier as immunocytochemistry; does the registrar accept both?
- The gate has no context option for a biopsy or cytology report that calls the specimen inadequate or non-diagnostic; the hint tells the clerk to leave such a report unticked, so the file drops to a lower tier. Does the registrar want that handled by the hint alone?

### `ts_document_inventory` (tree `g10_testis`)

*Question:* What is in the file for this tumour?
*Hint rewritten:* A radiology report counts as imaging. A pathology report on a biopsy or resection counts as histology. A biopsy or cytology report that calls the specimen inadequate or non-diagnostic counts as no tissue: pick from the other tiers.

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | A referral letter or clinical note only — no imaging report, no marker result, no tissue | tier | none of Imaging Report, Cytology, Histology Report | Lowest tier: fits when no imaging, cytology or histology document is ticked, so it catches nothing ticked, a lone Lab Report, and IHC or Gene reports without the document they are read against (all understate, the safe direction). | high |
| 1 | An imaging report and a serum or cerebrospinal fluid alpha-fetoprotein or human chorionic gonadotropin result — no tissue | tier | needs Imaging Report and Lab Report; none of Cytology, Histology Report | Needs the Imaging Report and the Lab Report (assumed to hold the alpha-fetoprotein or human chorionic gonadotropin result); the label's 'no tissue' excludes Cytology and Histology Report. The next node asks for the specific marker result. | medium |
| 2 | An imaging report only — no marker result, no tissue | tier | needs Imaging Report; none of Lab Report, Cytology, Histology Report | Imaging Report alone, honouring 'no marker result, no tissue' by excluding Lab Report, Cytology and Histology Report; sibling to option 1, so imaging with a Lab Report fits only option 1. | high |
| 3 | Cytology only — cerebrospinal fluid, effusion or fine-needle aspirate; no tissue | tier | needs Cytology; none of Histology Report | Needs the Cytology document itself (effusion, aspirate, fluid cytology); Histology Report excluded because the label says no tissue. IHC or genetics beside Cytology stays here (immunocytochemistry, no cell block named); imaging or lab beside Cytology also lands here. | high |
| 4 | A histology report — biopsy or resection | tier | needs Histology Report | Histology Report ticked; the top tier regardless of other documents, with IHC and genetics refining it only beside the report. | high |

*For the registrar:*

- option 1: Option 1 fits any file that ticks the Imaging Report and the general Lab Report, so is it acceptable that a Lab Report holding only a blood count, with no alpha-fetoprotein or human chorionic gonadotropin result, still offers the marker route (the next node asks for the specific result)?
- option 0: DATA GAP: a file holding a serum or cerebrospinal fluid marker result with no imaging report and no tissue fits only option 0, whose label says 'no marker result', so should the gate gain an option such as 'A serum or cerebrospinal fluid marker result only, no imaging report, no tissue'?
- option 0: Is it acceptable that IHC or Gene reports ticked without a Cytology or Histology Report (for example a germline or liquid-biopsy gene report) fall to option 0, and that a set with both Cytology and Histology Report ticked ignores the cytology?
- option 3: Is it acceptable that imaging and marker results ticked beside a Cytology document fit only the cytology option (which excludes only Histology Report), so that the marker route of option 1 is never offered when cytology is present, and that IHC beside Cytology stays at the cytology tier as immunocytochemistry?
- The old hint said an inadequate or non-diagnostic biopsy or cytology report counts as no tissue and the gate has no context option for it, so is it acceptable that the clerk is told to leave such a report unticked rather than the engine detecting it?
- option 1: Does the registrar accept that ticking the general Lab Report document is taken to mean the serum or cerebrospinal fluid alpha-fetoprotein or human chorionic gonadotropin result named in the label, given that the next question (ts_markers) asks for the specific result?
- option 0: A file with only a Lab Report, IHC Report or Gene reports ticked falls to the referral-or-clinical-note tier although the label says no marker result; does the registrar accept this understatement rather than a separate tier?
- option 3: A file with Cytology plus an Imaging Report or Lab Report but no Histology Report fits the cytology tier despite the word only in the label, and IHC ticked beside Cytology stays at the cytology tier as immunocytochemistry; does the registrar accept both?
- The gate has no context option for a biopsy or cytology report that calls the specimen inadequate or non-diagnostic; the hint tells the clerk to leave such a report unticked, so the file drops to a lower tier. Does the registrar want that handled by the hint alone?

### `eg_document_inventory` (tree `g10_extragonadal`)

*Question:* What is in the file for this tumour?
*Hint rewritten:* A radiology report counts as imaging. A pathology report on a biopsy or resection counts as histology. A biopsy or cytology report that calls the specimen inadequate or non-diagnostic counts as no tissue: pick from the other tiers.

| # | Option | Kind | Rule | Why | Confidence |
|---|---|---|---|---|---|
| 0 | A referral letter or clinical note only — no imaging report, no marker result, no tissue | tier | none of Imaging Report, Cytology, Histology Report | Lowest tier: fits when no imaging, cytology or histology document is ticked, so it catches nothing ticked, a lone Lab Report, and IHC or Gene reports without the document they are read against (all understate, the safe direction). | high |
| 1 | An imaging report and a serum or cerebrospinal fluid alpha-fetoprotein or human chorionic gonadotropin result — no tissue | tier | needs Imaging Report and Lab Report; none of Cytology, Histology Report | Needs the Imaging Report and the Lab Report (assumed to hold the alpha-fetoprotein or human chorionic gonadotropin result); the label's 'no tissue' excludes Cytology and Histology Report. The next node asks for the specific marker result. | medium |
| 2 | An imaging report only — no marker result, no tissue | tier | needs Imaging Report; none of Lab Report, Cytology, Histology Report | Imaging Report alone, honouring 'no marker result, no tissue' by excluding Lab Report, Cytology and Histology Report; sibling to option 1, so imaging with a Lab Report fits only option 1. | high |
| 3 | Cytology only — cerebrospinal fluid, effusion or fine-needle aspirate; no tissue | tier | needs Cytology; none of Histology Report | Needs the Cytology document itself (cerebrospinal-fluid cytology, effusion, aspirate); Histology Report excluded because the label says no tissue. IHC or genetics beside Cytology stays here (immunocytochemistry, no cell block named); imaging or lab beside Cytology also lands here. | high |
| 4 | A histology report — biopsy or resection | tier | needs Histology Report | Histology Report ticked; the top tier regardless of other documents, with IHC and genetics refining it only beside the report. | high |

*For the registrar:*

- option 1: Option 1 fits any file that ticks the Imaging Report and the general Lab Report, so is it acceptable that a Lab Report holding only a blood count, with no alpha-fetoprotein or human chorionic gonadotropin result, still offers the marker route (the next node asks for the specific result)?
- option 0: DATA GAP: a file holding a serum or cerebrospinal fluid marker result with no imaging report and no tissue fits only option 0, whose label says 'no marker result', so should the gate gain an option such as 'A serum or cerebrospinal fluid marker result only, no imaging report, no tissue'?
- option 0: Is it acceptable that IHC or Gene reports ticked without a Cytology or Histology Report (for example a germline or liquid-biopsy gene report) fall to option 0, and that a set with both Cytology and Histology Report ticked ignores the cytology?
- option 3: Is it acceptable that imaging and marker results ticked beside a Cytology document fit only the cytology option (which excludes only Histology Report), so that the marker route of option 1 is never offered when cytology is present, and that IHC beside Cytology stays at the cytology tier as immunocytochemistry?
- The old hint said an inadequate or non-diagnostic biopsy or cytology report counts as no tissue and the gate has no context option for it, so is it acceptable that the clerk is told to leave such a report unticked rather than the engine detecting it?
- option 1: Does the registrar accept that ticking the general Lab Report document is taken to mean the serum or cerebrospinal fluid alpha-fetoprotein or human chorionic gonadotropin result named in the label, given that the next question (eg_markers) asks for the specific result?
- option 0: A file with only a Lab Report, IHC Report or Gene reports ticked falls to the referral-or-clinical-note tier although the label says no marker result; does the registrar accept this understatement rather than a separate tier?
- option 3: A file with Cytology plus an Imaging Report or Lab Report but no Histology Report fits the cytology tier despite the word only in the label, and IHC ticked beside Cytology stays at the cytology tier as immunocytochemistry; does the registrar accept both?
- The gate has no context option for a biopsy or cytology report that calls the specimen inadequate or non-diagnostic; the hint tells the clerk to leave such a report unticked, so the file drops to a lower tier. Does the registrar want that handled by the hint alone?

## Questions for the registrar

### Data gaps: a gate has no option that describes a file the checklist can now express

- Group 1 `ac_document_inventory`: DATA GAP: the gate has no tier for a flow cytometry (Lab Report) or IHC report with no smear or tissue report, which falls to option 0 although option 0 says 'no marrow report'; should the gate gain an option such as 'flow cytometry or IHC report only, no morphology report'?
- Group 1 `ml_document_inventory`: DATA GAP: the gate has no tier for a peripheral-blood flow report (Lab Report) with no blood film or marrow report, which falls to option 0 although option 0 says 'no flow report'; should the gate gain an option such as 'flow cytometry report only, no morphology report'?
- Group 1 `mpn_document_inventory`: DATA GAP: the gate has no tier for a BCR::ABL1 or JAK2 Gene report on blood with no blood film or marrow report, which falls to option 0 although the report is real evidence; should the gate gain an option such as 'cytogenetic or molecular report only, no morphology report'?
- Group 1 `mds_document_inventory`: DATA GAP: the gate has no tier for an aspirate with a trephine report but no IHC, or for a trephine alone, so both fall to option 1 although option 1 says 'no trephine'; should the gate gain an option such as 'aspirate and trephine biopsy, IHC not performed'?
- Group 1 `ac_document_inventory`: DATA GAP: a trephine-only file (Histology Report without Cytology) has no truthful option because every morphology option names the aspirate or blood film and the referral option says no marrow report, so it is held at the aspirate/blood-film tier; should the gate gain an option for a marrow trephine report only?
- Group 1 `ac_document_inventory`: DATA GAP: a Lab Report alone (flow cytometry on blood with no marrow or film report) fits only the referral-only option; should the gate gain an option for a flow cytometry report with no marrow morphology?
- Group 1 `ml_document_inventory`: DATA GAP: the referral-only option says no flow report, yet a Lab Report alone (flow cytometry with no film or marrow report) must fit it to avoid a dead end; should the gate gain an option for a flow cytometry report with no blood film or marrow morphology?
- Group 1 `mds_document_inventory`: DATA GAP: a trephine without IHC (Histology Report alone, or beside a Cytology report) has no truthful option, because the aspirate-only option says no trephine and the next tier says IHC was performed; it is held at the aspirate tier, which understates; should the gate gain an option for aspirate with trephine and no IHC?
- Group 2 `g2_document_inventory`: DATA GAP: No option describes a smear, fluid or aspirate cytology report read with immunocytochemistry (Cytology and IHC Report ticked, no Histology Report), so that file fits options 1 and 2 although their labels say 'no IHC'; should the gate gain an option for cytology with immunocytochemistry?
- Group 2 `g2cut_document_inventory`: DATA GAP: The cutaneous gate has no cytology tier, so a skin smear or aspirate with no biopsy falls to option 0 ('letter only, no skin biopsy'); should the gate gain an option for cytology only?
- Group 2 `g2hist_document_inventory`: DATA GAP: The histiocytic gate has no cytology tier, so a marrow aspirate smear (for example showing haemophagocytosis) or other cytology with no biopsy falls to option 0 ('letter only, no biopsy report'); should the gate gain an option for cytology only?
- Group 2 `g2mast_document_inventory`: DATA GAP: No option describes morphology plus a serum tryptase and/or KIT result without IHC (the cheapest route the hint names), so that file falls to option 1 although its label says 'no serum tryptase and no KIT result'; should the gate gain an option for morphology plus serum tryptase or KIT without IHC?
- Group 2 `g2_document_inventory`: DATA GAP: the gate has no option for a smear with immunocytochemistry (Cytology plus IHC, no cell block, no flow), so that set fits the smear options although their label says no IHC; should an option for FNA smear with immunocytochemistry be added?
- Group 2 `g2_document_inventory`: DATA GAP: the gate has no option for a smear with a gene report (FISH or molecular on an aspirate, no flow, no cell block), so that set fits the smear options although their label says FNA smear only; should an option for smear with genetics be added?
- Group 2 `g2cut_document_inventory`: DATA GAP: the gate has no cytology option, so a file with only a smear or aspirate of the skin lesion falls to the referral-letter-only option, whose label says no skin biopsy; should an option for cytology of the skin lesion without a biopsy be added?
- Group 2 `g2hist_document_inventory`: DATA GAP: the gate has no cytology option, so a file with only a smear or aspirate (for example a marrow aspirate) falls to the referral-letter-only option, whose label says no biopsy report; should an option for cytology without a biopsy be added?
- Group 2 `g2mast_document_inventory`: DATA GAP: the gate has no option for morphology plus serum tryptase or a KIT result without IHC, which its own hint calls a route to a definitive code, so that set falls to the morphology-only option whose label says no tryptase and no KIT result; should an option for morphology with serum tryptase and/or KIT but no IHC be added?
- Group 3 `pf_document_inventory`: DATA GAP: the posterior fossa gate offers only an intraoperative frozen-section or squash cytology tier, so a Cytology-only file of cerebrospinal-fluid or aspirate cytology is described as intraoperative; should an option for cerebrospinal-fluid or aspirate cytology without tissue be added?
- Group 3 `st_document_inventory`: DATA GAP: the supratentorial gate has no tier for cerebrospinal-fluid or aspirate cytology, so a Cytology-only file is described as an intraoperative frozen section or squash; should an option for cytology without tissue be added?
- Group 3 `md_document_inventory`: DATA GAP: the midline gate has only an intraoperative frozen-section or squash tier, so cerebrospinal-fluid cytology for a suspected germ cell tumour is described as intraoperative; should a cerebrospinal-fluid cytology option be added?
- Group 3 `sp_document_inventory`: DATA GAP: the spinal gate has only an intraoperative frozen-section or squash tier, so cerebrospinal-fluid or aspirate cytology is described as intraoperative; should an option for cytology without tissue be added?
- Group 3 `mn_document_inventory`: DATA GAP: the meninges gate has only an intraoperative frozen-section or squash tier, so cerebrospinal-fluid or aspirate cytology is described as intraoperative; should an option for cytology without tissue be added?
- Group 3 `un_document_inventory`: DATA GAP: the unspecified gate has only an intraoperative frozen-section or squash tier, so cerebrospinal-fluid or aspirate cytology is described as intraoperative; should an option for cytology without tissue be added?
- Group 3 `md_document_inventory`: DATA GAP: Should the gate gain an option for a tumour-marker or hormone result in the file with no imaging report and no tissue, because a lone Lab Report now falls to the referral-only option, which routes to the referral wording and skips the germ cell marker question that every other option reaches?
- Group 3 `un_document_inventory`: DATA GAP: Should the gate gain an option for a serum or cerebrospinal-fluid tumour-marker result with no imaging report, because a lone Lab Report now falls to the referral-only option and never reaches the marker question that the imaging-incomplete node asks?
- Group 3 `un_document_inventory`: DATA GAP: a lone Lab Report (possibly a serum or cerebrospinal-fluid tumour marker) with no imaging report falls to the referral-only option and never reaches the marker question that option 3 leads to; should the gate gain an option for a tumour-marker result with no imaging report?
- Group 3 `un_document_inventory`: DATA GAP: a Cytology-only file of cerebrospinal-fluid or fine-needle aspirate cytology is described by an option that asserts an intraoperative frozen section or squash; should the gate gain a cytology-without-tissue option? Its captures also record the evidence as Histology while the document definitions place a frozen section or squash under Cytology.
- Group 4 `sa_document_inventory`: DATA GAP: this gate has no option for an imaging report without a biochemical work-up, or for a laboratory result without imaging, so those files fit only the referral-only option and the case is understated; should the gate gain 'Imaging report only, no biochemical work-up and no tissue'?
- Group 4 `hn_document_inventory`: DATA GAP: the gate has no cytology option, so a cytology-only file falls to the referral-only option, whose label says no pathology report; should the gate gain 'Cytology only, no tissue'?
- Group 4 `hn_document_inventory`: DATA GAP: a file with imaging and cytology and no tissue fits the imaging-only option although its label says no cytology; should the missing cytology option be added so that wording holds?
- Group 4 `sn_document_inventory`: DATA GAP: the gate has no cytology option, so a cytology-only file falls to the referral-only option, whose label says no pathology report; should the gate gain 'Cytology only, no tissue'?
- Group 4 `sn_document_inventory`: DATA GAP: a file with imaging and cytology and no tissue fits the imaging-only option although its label says no cytology; should the missing cytology option be added so that wording holds?
- Group 4 `op_document_inventory`: DATA GAP: the label says no biopsy or cytology preparation was performed, but the gate has no cytology option, so a cytology-only file fits this option and routes to Group XII; should the gate gain 'Cytology only, no tissue'?
- Group 4 `sa_document_inventory`: DATA GAP: no option describes an Imaging Report with no laboratory result and no tissue, or a lone Lab Report. Both land on option 0, whose label says no imaging report and no laboratory result, which understates; should the gate gain an option 'Imaging report only, no biochemical result, no tissue' routing to the same place as 'No biochemical marker was sent'?
- Group 4 `hn_document_inventory`: DATA GAP: the gate has no cytology tier, so a cytology-only file fits option 0 ('no pathology report'), and imaging plus cytology fits option 1 ('no cytology'); should the gate gain an option 'Cytology only, no tissue' routing to Group XII?
- Group 4 `sn_document_inventory`: DATA GAP: the gate has no cytology tier, so a cytology-only file fits option 0 ('no pathology report'), and imaging plus cytology fits option 1 ('no cytology'); should the gate gain an option 'Cytology only, no tissue' routing to Group XII?
- Group 4 `op_document_inventory`: DATA GAP: no option describes a cytology-only file; it fits option 1, whose label says no cytology preparation was performed, and routes to Group XII; should the gate gain an option 'Cytology only, no tissue'?
- Group 10 `cn_document_inventory`: DATA GAP: a file holding a serum or cerebrospinal fluid marker result with no imaging report and no tissue fits only option 0, whose label says 'no marker result', so should the gate gain an option such as 'A serum or cerebrospinal fluid marker result only, no imaging report, no tissue'?
- Group 10 `ov_document_inventory`: DATA GAP: a file holding a serum or cerebrospinal fluid marker result with no imaging report and no tissue fits only option 0, whose label says 'no marker result', so should the gate gain an option such as 'A serum or cerebrospinal fluid marker result only, no imaging report, no tissue'?
- Group 10 `ts_document_inventory`: DATA GAP: a file holding a serum or cerebrospinal fluid marker result with no imaging report and no tissue fits only option 0, whose label says 'no marker result', so should the gate gain an option such as 'A serum or cerebrospinal fluid marker result only, no imaging report, no tissue'?
- Group 10 `eg_document_inventory`: DATA GAP: a file holding a serum or cerebrospinal fluid marker result with no imaging report and no tissue fits only option 0, whose label says 'no marker result', so should the gate gain an option such as 'A serum or cerebrospinal fluid marker result only, no imaging report, no tissue'?

### Judgement calls

There are 265 judgement calls, written under each gate above as "For the registrar". The three that recur everywhere are the haematology readings named at the top of this document and the general reading of Lab Report (it covers tumour markers, flow cytometry and serum tryptase alike, and the next screen on the path asks which).

## Ticked sets the clinical reviewer marked doubtful or wrong

Every set not listed here was judged to take the tier a registrar would pick. These are the exceptions, with the reviewer's reason.

| Group | Gate | Ticked set | Verdict | Reviewer's note |
|---|---|---|---|---|
| 1 | `ac_document_inventory` | {cytology, lab} | doubtful | Tier [2] claims flow cytometry and/or IHC, but nothing ticks IHC and 'lab' also covers blood count, tryptase etc. A blood-count-only lab report is lifted to a flow/IHC tier. The same tick alone ({lab}) is treated as no flow, so lab is read two ways. |
| 1 | `ac_document_inventory` | {histology} | doubtful | Tier [1] names 'marrow aspirate / blood film' (the cytology specimens) for a tissue-section report such as a trephine. It is the lowest morphology tier and understates, but it names a specimen type not ticked and the gate has no trephine/histology wording. |
| 1 | `ac_document_inventory` | {histology, ihc} | doubtful | IHC is ticked but [1] says 'no IHC' and the result is dropped. Tier [2] (morphology + flow and/or IHC) fits and does not overstate; the engine apparently needs lab to reach it. |
| 1 | `ac_document_inventory` | {histology, genetics} | doubtful | Genetics result dropped; [1] captures karyotype 'not done' although a gene report is ticked. [3] would claim flow/IHC that is not ticked, so [1] is the only non-overstating choice, but the genetic result is lost. |
| 1 | `ac_document_inventory` | {histology, ihc, genetics} | doubtful | Drops both IHC and genetics and states 'no IHC'. Tier [3] (morphology + flow/IHC + cytogenetics/FISH) fits the ticks, since 'flow/IHC' is satisfied by IHC, yet the engine offers only the lowest morphology tier. Largest avoidable understatement in this gate. |
| 1 | `ac_document_inventory` | {imaging, histology} | doubtful | Same as {histology}: imaging is correctly ignored, but [1] names aspirate/blood film for a histology tick. |
| 1 | `ac_document_inventory` | {genetics} | doubtful | A karyotype, FISH or fusion result is often diagnostic by itself in leukaemia, yet it falls to 'Referral only', with karyotype captured as 'not done'. No tier fits without claiming morphology, but the registrar would want the result kept. |
| 1 | `ac_document_inventory` | {cytology, ihc} | doubtful | IHC is ticked but [1] says 'no IHC' and drops it. Tier [2] (morphology + flow and/or IHC) fits exactly and does not overstate. |
| 1 | `ac_document_inventory` | {referral, imaging, lab, cytology, histology, ihc, genetics} | doubtful | Both offered tiers [3] and [4] claim cytogenetics/FISH, but 'genetics' also covers RT-PCR, sequencing, MLPA and methylation. A file whose gene report is molecular only has no accurate tier here. Otherwise the full set is correctly offered the top two tiers. |
| 1 | `ml_document_inventory` | {imaging, lab} | doubtful | Tier [0] says 'no flow report', but 'lab' includes flow cytometry. Flow is the key test for mature lymphoid disease, so the label can deny a ticked result. No flow-only tier exists, so this is understatement, not overstatement. |
| 1 | `ml_document_inventory` | {lab} | doubtful | As {imaging, lab}: [0] denies a flow report that the lab tick may hold, and lab is read as flow when cytology is added ({cytology, lab} gives [2]). |
| 1 | `ml_document_inventory` | {cytology, lab} | doubtful | Tier [2] claims flow cytometry and/or IHC on the strength of 'lab' alone; a blood-count-only lab report is lifted to a flow/IHC tier. Nothing ticks IHC. |
| 1 | `ml_document_inventory` | {histology, ihc} | doubtful | IHC is ticked but [1] says 'no IHC' and drops it. Tier [2] fits and does not overstate. |
| 1 | `ml_document_inventory` | {histology, genetics} | doubtful | Genetics result dropped and captured as 'not done'. Tier [3] would claim flow/IHC that is not ticked, so [1] is the only non-overstating choice, but the genetic result is lost. |
| 1 | `ml_document_inventory` | {histology, ihc, genetics} | doubtful | Drops IHC and genetics and states 'no IHC'. Tier [3] (morphology + flow/IHC + cytogenetics/FISH/molecular/PCR) fits the ticks (IHC satisfies 'flow/IHC') but is not offered. |
| 1 | `ml_document_inventory` | {genetics} | doubtful | A clonality, fusion or karyotype result falls to 'Referral only' with karyotype 'not done'. No tier fits without claiming morphology, but the registrar would want the result kept. |
| 1 | `ml_document_inventory` | {cytology, ihc} | doubtful | IHC is ticked but [1] says 'no IHC' and drops it. Tier [2] (morphology + flow and/or IHC) fits. |
| 1 | `mpn_document_inventory` | {histology, genetics} | doubtful | Both offered tiers claim cytogenetics/FISH, but 'genetics' also covers RT-PCR and sequencing (BCR::ABL1, JAK2). A molecular-only report is forced to claim cytogenetics, and the lower tier [1] is not offered. Fine for a karyotype or FISH file. |
| 1 | `mpn_document_inventory` | {histology, ihc, genetics} | doubtful | Same as {histology, genetics}: every offered tier claims cytogenetics/FISH and no molecular-only tier exists. |
| 1 | `mpn_document_inventory` | {genetics} | doubtful | A BCR::ABL1 RT-PCR, karyotype or FISH result alone is often diagnostic in this tree, yet it falls to 'Referral only' with karyotype 'not done' and BCR-ABL1 'not tested'. No tier fits without claiming morphology, but the registrar would want the result kept. |
| 1 | `mpn_document_inventory` | {referral, imaging, lab, cytology, histology, ihc, genetics} | doubtful | Both offered tiers [2] and [3] claim cytogenetics/FISH, so a molecular-only gene report has no accurate tier. Otherwise the correct top two tiers are offered. |
| 1 | `mds_document_inventory` | {histology} | doubtful | A trephine report is ticked but [1] says 'no trephine' and names aspirate/blood film. [2] would claim aspirate plus CD61/CD41 IHC, so [1] is the nearest non-overstating tier, but its label contradicts the tick. |
| 1 | `mds_document_inventory` | {histology, ihc} | doubtful | [1] denies trephine and IHC, both ticked, and drops them. [2] is the right family but claims an aspirate and specific CD61/CD41 stains that are not ticked. |
| 1 | `mds_document_inventory` | {histology, genetics} | doubtful | [1] denies trephine and cytogenetics, both ticked, and captures karyotype 'not done'. The genetic result is dropped; [3] would claim IHC that is not ticked. |
| 1 | `mds_document_inventory` | {histology, ihc, genetics} | doubtful | [1] flatly contradicts the ticks (no trephine, no IHC, no cytogenetics) and drops all three. Tier [3] 'Marrow + trephine/IHC + cytogenetics/FISH' fits and is not offered. Worst avoidable understatement in this gate. |
| 1 | `mds_document_inventory` | {imaging, histology} | doubtful | Same as {histology}: [1] denies the trephine that the histology tick covers. |
| 1 | `mds_document_inventory` | {genetics} | doubtful | A karyotype or fusion result alone falls to 'Referral only' with karyotype 'not done'. No tier fits without claiming marrow, but the registrar would want the result kept. |
| 1 | `mds_document_inventory` | {cytology, ihc} | doubtful | IHC is ticked but [1] says 'no IHC' and drops it. No better non-overstating tier exists because [2] needs a trephine, so this is an unavoidable understatement with a false label. |
| 1 | `mds_document_inventory` | {lab, histology, ihc} | doubtful | Same as {histology, ihc}: [1] denies the ticked trephine and IHC. |
| 2 | `g2_document_inventory` | {cytology, lab} | doubtful | Option 7 asserts flow cytometry. Lab also covers blood count and tumour markers, so the tick does not establish flow. The tick set also loses the adequate-neoplastic and adequate-benign options (1 and 2), so a benign smear skips the not-lymphoma gate. |
| 2 | `g2_document_inventory` | {histology, genetics} | doubtful | Understates in the safe direction: option 5 reads 'H&E only' and drops the genetics result. Option 8 would claim IHC/flow that was not ticked, so no better option exists. A registrar would still want the genetics kept. |
| 2 | `g2_document_inventory` | {cytology, ihc} | doubtful | Options 1 and 2 state 'no cell block, no flow, no IHC' (option 1) although IHC was ticked. The label denies a ticked result and the IHC is dropped. The safe direction, but a false negative. |
| 2 | `g2cut_document_inventory` | {histology, genetics} | doubtful | Option 1 reads 'H&E only' and drops the genetics (TCR clonality or FISH), which in this branch is a tier criterion. Option 3 needs IHC, so no better option exists. A registrar would want the genetics kept. |
| 2 | `g2cut_document_inventory` | {lab, histology, ihc} | doubtful | The only tier offered is option 3 (clonality, FISH or blood flow, workup 'complete', capturing Molecular/PCR). Genetics was not ticked, and a lab tick may be a blood count only. The plain-IHC tier (option 2) is not offered, so a file with a biopsy, IHC and a blood count is forced up a tier. This is the closest row to wrong. |
| 2 | `g2hist_document_inventory` | {histology, genetics} | doubtful | Option 1 reads 'H&E only', and the genetics is dropped (BRAF, ALK or clonality is a defining result for histiocytic neoplasms). Option 3 needs IHC, so no better option exists. |
| 2 | `g2mast_document_inventory` | {cytology, lab} | doubtful | Option 1 states 'no serum tryptase' although lab was ticked, and lab explicitly includes serum tryptase. The tier denies the ticked result and drops what the hint calls the cheap route to a definitive code. The only tier that names tryptase (option 3) also claims IHC, so no better option exists. |
| 2 | `g2mast_document_inventory` | {histology, genetics} | doubtful | Option 1 states 'no KIT result' and captures kit_d816v 'not_done', but a genetics report was ticked and KIT sequencing or PCR falls under genetics. The tier denies a probable KIT result. Option 3 needs IHC, so no better option exists. |
| 2 | `g2mast_document_inventory` | {histology, ihc, genetics} | doubtful | Option 2 drops the genetics, and captures kit_d816v 'not_done'. Option 3 ('IHC plus tryptase and/or KIT molecular result') fits this file exactly but is reachable only through lab, not genetics. In the other three gates genetics lifts to the top tier. |
| 2 | `g2mast_document_inventory` | {lab, histology, ihc} | doubtful | Option 3 names serum tryptase and/or KIT, with workup 'complete'. Lab is the only tick and may be a blood count rather than tryptase. Arguable: the lab definition lists serum tryptase, so the lift is probably intended. |
| 3 | `pf_document_inventory` | {histology, genetics} | doubtful | Falls to H&E-only and drops the molecular result; [6] needs IHC, so no option keeps histology plus molecular without IHC. Safe direction but loses the highest-value result. |
| 3 | `pf_document_inventory` | {ihc} | doubtful | IHC report ticked but the floor option says 'no pathology report' and the IHC result is dropped. Safe direction; likely a missed histology tick. |
| 3 | `pf_document_inventory` | {genetics} | doubtful | A molecular report is the only diagnostic document yet the offer is 'referral only'; result dropped, no better option. |
| 3 | `pf_document_inventory` | {cytology, ihc} | doubtful | IHC dropped and the label says 'only'; understates in the safe direction but loses the IHC result. |
| 3 | `st_document_inventory` | {histology, genetics} | doubtful | Falls to H&E-only and drops the molecular result; [6] and [7] lie behind an IHC tick. |
| 3 | `st_document_inventory` | {ihc} | doubtful | IHC report ticked but the floor option says 'no pathology report' and the IHC result is dropped. Safe direction. |
| 3 | `st_document_inventory` | {genetics} | doubtful | A molecular report is the only diagnostic document yet the offer is 'referral only'; result dropped, no better option. |
| 3 | `st_document_inventory` | {cytology, ihc} | doubtful | IHC dropped and the label says 'only'; safe direction but loses the IHC result. |
| 3 | `md_document_inventory` | {imaging, lab} | doubtful | Only [2] is offered; its label says hormone assays and a functioning pituitary tumour, narrower than the lab document (could be AFP/hCG or a blood count). [1] is not offered, so a germ-cell file is forced onto a pituitary wording. Captures ('Tumour markers') are right. |
| 3 | `md_document_inventory` | {lab} | doubtful | Lab dropped to the referral floor although this gate treats assays and markers as evidence; the label also assumes a referral naming a diagnosis. |
| 3 | `md_document_inventory` | {histology, genetics} | doubtful | Falls to H&E-only and drops the molecular result; [6] requires IHC. |
| 3 | `md_document_inventory` | {ihc} | doubtful | IHC report ticked but the floor option says no biopsy report and the IHC result is dropped. Safe direction. |
| 3 | `md_document_inventory` | {genetics} | doubtful | Molecular report is the only diagnostic document yet the offer is 'referral only'; result dropped, no better option. |
| 3 | `md_document_inventory` | {cytology, ihc} | doubtful | IHC dropped and the label says 'only'; safe direction but loses the IHC result. |
| 3 | `sp_document_inventory` | {imaging} | doubtful | Label says 'MRI report only'; the imaging document also covers CT, X-ray, ultrasound and PET, so a non-MRI file is described as MRI (overstates modality). Other gates say 'Imaging report' or 'MRI or CT'. |
| 3 | `sp_document_inventory` | {imaging, lab} | doubtful | Same 'MRI report only' modality claim as {imaging}; lab dropped (no lab tier in this gate). |
| 3 | `sp_document_inventory` | {histology, genetics} | doubtful | Falls to H&E-only ('no immunohistochemistry available') and drops the molecular result; [5] requires IHC. |
| 3 | `sp_document_inventory` | {histology, ihc, genetics} | wrong | Only [5] is offered and it claims FISH, RT-PCR or sequencing 'on fresh tissue' (and sets resource level IV). A genetics tick says nothing about fresh tissue; FISH on paraffin sections is common. It also omits methylation, MLPA, karyotype and clonality. [4] is not offered as a fallback. |
| 3 | `sp_document_inventory` | {ihc} | doubtful | IHC report ticked but the offer is 'referral only' and the IHC result is dropped. Safe direction. |
| 3 | `sp_document_inventory` | {genetics} | doubtful | Molecular report is the only diagnostic document yet the offer is 'referral only'; result dropped, no better option. |
| 3 | `sp_document_inventory` | {cytology, ihc} | doubtful | IHC dropped and the label says 'only'; safe direction but loses the IHC result. |
| 3 | `sp_document_inventory` | {referral, imaging, lab, cytology, histology, ihc, genetics} | wrong | Only [5] is offered; same 'on fresh tissue' specimen claim and resource level IV as {histology, ihc, genetics}. |
| 3 | `mn_document_inventory` | {histology, genetics} | doubtful | Falls to H&E-only and drops the molecular, copy-number or methylation result; [5] requires IHC. |
| 3 | `mn_document_inventory` | {ihc} | doubtful | IHC report ticked but the floor option says 'no pathology report' and the IHC result is dropped. Safe direction. |
| 3 | `mn_document_inventory` | {genetics} | doubtful | Molecular report is the only diagnostic document yet the offer is 'referral only'; result dropped, no better option. |
| 3 | `mn_document_inventory` | {cytology, ihc} | doubtful | IHC dropped and the label says 'only'; safe direction but loses the IHC result. |
| 3 | `un_document_inventory` | {lab} | doubtful | Lab dropped to the referral floor; [3] (markers measured) is worded as imaging plus markers, so a markers-only file has no route and the tumour-marker fact is lost. |
| 3 | `un_document_inventory` | {ihc} | doubtful | Floor option says no pathology and its captures set IHC requested 'n' / 'not_indicated' while an IHC report is ticked; the result is dropped. Safe direction but contradicts the tick. |
| 3 | `un_document_inventory` | {genetics} | doubtful | Molecular report is the only diagnostic document yet the offer is 'referral only'; result dropped, no better option. |
| 3 | `un_document_inventory` | {cytology, ihc} | doubtful | [5] captures IHC requested 'n' while an IHC report is ticked; IHC dropped. Safe direction but contradicts the tick. |
| 4 | `sa_document_inventory` | {imaging} | doubtful | Offers [0], whose text says there is no imaging report, though one is ticked. This gate has no imaging-only tier (hn and sn do). [1] needs a biochemical work-up that was not ticked, so [0] is the safe understatement, but the imaging result is dropped. |
| 4 | `sa_document_inventory` | {lab} | doubtful | [0] says there is no laboratory result, and the ticked lab result (possibly catecholamines) is dropped. [1] needs imaging that was not ticked, so [0] is the safe direction, but the only evidence in the file is lost. |
| 4 | `sa_document_inventory` | {histology, genetics} | doubtful | [3] drops the genetics result, which is MYCN or ALK testing and tier-defining in this gate. [5] needs immunohistochemistry that was not ticked, so offering it would overstate. The gate has no histology-plus-genetics tier. |
| 4 | `sa_document_inventory` | {ihc} | doubtful | IHC without histology is an inconsistent tick set, because IHC implies tissue. [0] says there is no pathology report and drops the IHC result. [4] and [5] would claim histology that was not ticked, so [0] is the safe direction. |
| 4 | `sa_document_inventory` | {genetics} | doubtful | The sole result, which may be MYCN or ALK, is dropped into the referral-only tier. [4] and [5] would claim histology and IHC that were not ticked, so [0] is the safe direction. |
| 4 | `sa_document_inventory` | {cytology, ihc} | doubtful | [2] is safe, since [4] would claim histology. It drops the IHC result, which ranks above cytology. This is immunocytochemistry or an inconsistent tick set. |
| 4 | `hn_document_inventory` | {cytology} | doubtful | Cytology lands on referral-only, and the tree has no cytology tier. [1] says 'no cytology', so it would be false, and [2] would claim tissue. [0] is the safe direction, but a possible diagnostic basis is dropped. The reason text on [3] and [4] speaks of basis 5, 7 or 8 diagnoses. |
| 4 | `hn_document_inventory` | {cytology, lab} | doubtful | Same as cytology alone: [0] drops the cytology result, and there is no cytology tier. |
| 4 | `hn_document_inventory` | {imaging, cytology} | doubtful | [1] reads 'no tissue, no cytology', which contradicts the ticked cytology. This is a safe understatement with no better option, but the label denies a ticked document. |
| 4 | `hn_document_inventory` | {ihc} | doubtful | IHC without histology is an inconsistent tick set, because IHC implies tissue. [0] says there is no pathology report and drops the IHC result. [2] would claim a tissue report that was not ticked, so [0] is the safe direction. |
| 4 | `hn_document_inventory` | {cytology, ihc} | doubtful | [0] drops both the cytology and the IHC result, and its text denies a pathology report. [2] would overstate with tissue that was not ticked. Immunocytochemistry or an inconsistent tick set. |
| 4 | `sn_document_inventory` | {cytology} | doubtful | Cytology lands on referral-only, and the tree has no cytology tier. [1] says 'no cytology', so it would be false, and [2] would claim tissue. [0] is the safe direction, but a possible diagnostic basis is dropped. |
| 4 | `sn_document_inventory` | {cytology, lab} | doubtful | Same as cytology alone: [0] drops the cytology result, and there is no cytology tier. |
| 4 | `sn_document_inventory` | {imaging, cytology} | doubtful | [1] reads 'no tissue, no cytology', which contradicts the ticked cytology. This is a safe understatement with no better option, but the label denies a ticked document. |
| 4 | `sn_document_inventory` | {ihc} | doubtful | IHC without histology is an inconsistent tick set, because IHC implies tissue. [0] says there is no pathology report and drops the IHC result. [2] would claim a tissue report that was not ticked, so [0] is the safe direction. |
| 4 | `sn_document_inventory` | {cytology, ihc} | doubtful | [0] drops both the cytology and the IHC result, and its text denies a pathology report. [2] would overstate with tissue that was not ticked. |
| 4 | `op_document_inventory` | {cytology} | doubtful | [1] says no biopsy or cytology preparation was ever performed, which is false when cytology is ticked. Its own reason text treats cytology as a basis that avoids the 8000/3 route. No option describes a cytology-only file, and [4] to [7] claim a pathology report or tissue. The offer is a safe understatement, but it is the weakest row in this gate. |
| 4 | `op_document_inventory` | {cytology, lab} | doubtful | Same as cytology alone: [1] denies a cytology preparation that was ticked, and the cytology result is dropped. |
| 4 | `op_document_inventory` | {imaging, cytology} | doubtful | [1] says no cytology preparation was ever performed, which contradicts the ticked cytology. See cytology alone. |
| 4 | `op_document_inventory` | {ihc} | doubtful | IHC implies a specimen was processed, yet [1] says no biopsy or cytology was ever performed. The IHC result is dropped. [4] to [7] would claim a pathology report that was not ticked, so [1] is the safe direction. Probably an inconsistent tick set. |
| 4 | `op_document_inventory` | {genetics} | doubtful | Tumour genetics needs a specimen, so [1] ('never performed') is probably false, and the result is dropped. It would be fine if the test was germline on blood. Safe direction, ambiguous. |
| 4 | `op_document_inventory` | {cytology, ihc} | doubtful | [1] denies a cytology preparation that was ticked and drops the IHC result. [4] to [7] would claim a pathology report or tissue that was not ticked. |
| 5 | `rb_document_inventory` | (nothing ticked) | doubtful | Tier 0 says 'Referral letter or clinical note only' and sends the clerk to rb_clinical_alias, which in this group can emit 9510 with basis 1 on referral wording alone. An empty tick set therefore claims a referral the clerk did not tick and invites a code from it. It is the floor tier and the weakest claim available, but the gate has no 'nothing in the file' option. |
| 5 | `rb_document_inventory` | ihc | doubtful | An IHC report is a tissue result, yet tier 0 says 'no pathology report' and discards it. This group declares ihc_counts_as 7, so the tool's own basis rule would treat IHC as histology-grade evidence. The understatement is safe and no tier fits without overstating (histology or enucleation were not ticked), but the only substantive document in the file is lost. |
| 5 | `rb_document_inventory` | genetics | doubtful | The only substantive document is dropped and the file is described as referral only. Tier 2 explicitly includes an aqueous-humour or plasma liquid biopsy, and a cell-free DNA report is a genetics report, so a clerk with that report has no tick that reaches tier 2. A germline RB1 report would correctly stay at referral. Safe direction, but arguable. |
| 6 | `rn_document_inventory` | (nothing ticked) | doubtful | Tier 0 claims a referral letter or clinical note the clerk did not tick. It is the floor and the next node (rn_clinical_alias) never emits a code, so the harm is small, but the gate has no 'nothing in the file' option. |
| 6 | `rn_document_inventory` | ihc | doubtful | An IHC report is a tissue result, but tier 0 says 'no histology report' and discards it. IHC is decisive in renal tumours (INI1 loss for rhabdoid tumour, 8963; 8964, 8319). No tier fits without overstating, so the understatement is safe, but the file's only substantive document is lost. |
| 6 | `rn_document_inventory` | genetics | doubtful | The only substantive document is dropped and the file is described as referral only. Safe direction, and no tier fits without tissue, but a registrar may want the molecular result recorded (entry 8311 lists cytogenetic and molecular tests as required). |
| 7 | `hp_document_inventory` | {lab} | doubtful | Safe understatement: offering [1] would claim imaging that was not ticked. But in this group the lab report is the alpha-fetoprotein result, a basis-of-diagnosis input (Visser basis 2/4, registrar item 11.4a). Tier [0] records 'Referral only' and drops it. It can re-enter only through hp_clinical_alias, as what a note reports. |
| 7 | `hp_document_inventory` | {ihc} | doubtful | Safe understatement, but an IHC report implies tissue was examined, yet the offered tier says no histology and records 'Referral only'. The result is dropped and no downstream node of the referral route reads it. Offering [2] would claim a histology report that was not ticked, so [0] is the only safe option. |
| 7 | `hp_document_inventory` | {genetics} | doubtful | Same as IHC alone. A genetic test needs a specimen; the tier drops the result and nothing in the referral route reads it. Safe direction. |
| 7 | `hp_document_inventory` | {cytology, ihc} | doubtful | Tier cytology claims nothing unticked, but the IHC is dropped. hp_cytology has no IHC question and says a smear carries no INI1 result. IHC on cytology usually means a cell block, which counts as histology. The clerk should be prompted to tick histology instead. Safe direction. |
| 8 | `bn_document_inventory` | {ihc} | doubtful | Safe understatement, but in this group IHC and EWSR1 results drive the code (bn_round_cell_ihc). An IHC report implies tissue. The tier says no histology and records 'Referral only', and bn_clinical_alias caps the case at 8000/3. Offering [2] would claim an unticked histology report, so [0] is the only safe option. |
| 8 | `bn_document_inventory` | {genetics} | doubtful | Same as IHC alone. A genetic result such as EWSR1 rearrangement is dropped, and the referral route never reads it. Safe direction. |
| 8 | `bn_document_inventory` | {cytology, ihc} | doubtful | Tier cytology claims nothing unticked, but the IHC is dropped. bn_cytology has no IHC question and codes only 8001/3. IHC on cytology usually means a cell block, which counts as histology, so the clerk should be prompted to tick histology. Safe direction. |
| 9 | `st_document_inventory` | {nothing ticked} | doubtful | Floor tier reads 'Referral letter or clinical note only', so it names a referral the clerk did not tick. No lower option exists and nothing is overstated beyond that, so arguable rather than wrong. |
| 9 | `st_document_inventory` | {lab} | doubtful | Falls to the referral-only floor, which names a referral that was not ticked. The dropped lab result is not tier-bearing for sarcoma, so the doubt is the unticked referral claim only. |
| 9 | `st_document_inventory` | {ihc} | doubtful | IHC without a histology report is odd (IHC is read on tissue), and it falls to the referral-only floor, dropping the IHC result and naming an unticked referral. No better option exists. |
| 9 | `st_document_inventory` | {genetics} | doubtful | A fusion or other genetic result can be diagnostic in sarcoma, and it is dropped to the referral-only floor, which also names an unticked referral. The gate has no genetics-only tier. |
| 9 | `st_document_inventory` | {cytology, ihc} | doubtful | Cytology tier is right, but the IHC result is dropped and the cytology node asks only for the cytology conclusion. A registrar may want IHC on cytological material kept. |
| 9 | `sk_document_inventory` | {nothing ticked} | doubtful | Floor tier reads 'Referral letter or clinical note only', so it names a referral the clerk did not tick. No lower option exists and nothing is overstated beyond that, so arguable rather than wrong. |
| 9 | `sk_document_inventory` | {lab} | doubtful | Falls to the referral-only floor, which names a referral that was not ticked. The dropped lab result is not tier-bearing, so the doubt is the unticked referral claim only. |
| 9 | `sk_document_inventory` | {ihc} | doubtful | IHC without a histology report is odd (IHC is read on tissue), and it falls to the referral-only floor, dropping the IHC result and naming an unticked referral. No better option exists. |
| 9 | `sk_document_inventory` | {genetics} | doubtful | A genetic result can be diagnostic in sarcoma, and it is dropped to the referral-only floor, which also names an unticked referral. The gate has no genetics-only tier. |
| 9 | `sk_document_inventory` | {cytology, ihc} | doubtful | Cytology tier is right, but the IHC result is dropped and the cytology node asks only for the cytology conclusion. A registrar may want IHC on cytological material kept. |
| 10 | `cn_document_inventory` | {imaging, lab} | doubtful | Option claims an AFP or hCG result, but 'lab' also covers blood count, hormone assay or LDH, and the engine offers no fall-back to the imaging-only option. The downstream 'Neither marker is raised' answer only partly recovers this. |
| 10 | `cn_document_inventory` | {lab} | doubtful | Drops the lab result. The label says 'no marker result', which is false if the lab is AFP or hCG. The tree has a markers tier that needs imaging, so the gate has no better option, but the label contradicts the tick. |
| 10 | `cn_document_inventory` | {ihc} | doubtful | Drops an IHC result the tree can use (the IHC checklist is reachable only from histology). The label asserts 'no tissue', yet an IHC report implies tissue. Understates safely, but a result the registrar may want kept is lost. |
| 10 | `cn_document_inventory` | {cytology, ihc} | doubtful | Drops IHC, which sits at or above cytology in the tier order (IHC implies a cell block or tissue). The label asserts 'no tissue', and the cytology branch cannot use IHC. |
| 10 | `ov_document_inventory` | {imaging, lab} | doubtful | Option claims an AFP or hCG result, but 'lab' also covers blood count, hormone assay or LDH, and the engine offers no fall-back to the imaging-only option. The downstream 'Neither marker is raised' answer only partly recovers this. |
| 10 | `ov_document_inventory` | {lab} | doubtful | Drops the lab result. The label says 'no marker result', which is false if the lab is AFP or hCG. The tree has a markers tier that needs imaging, so the gate has no better option, but the label contradicts the tick. |
| 10 | `ov_document_inventory` | {ihc} | doubtful | Drops an IHC result the tree can use (the IHC checklist is reachable only from histology). The label asserts 'no tissue', yet an IHC report implies tissue. Understates safely, but a result the registrar may want kept is lost. |
| 10 | `ov_document_inventory` | {cytology, ihc} | doubtful | Drops IHC, which sits at or above cytology in the tier order (IHC implies a cell block or tissue). The label asserts 'no tissue', and the cytology branch cannot use IHC. |
| 10 | `ts_document_inventory` | {imaging, lab} | doubtful | Option claims an AFP or hCG result, but 'lab' also covers blood count, hormone assay or LDH, and the engine offers no fall-back to the imaging-only option. The downstream 'Neither marker is raised' answer only partly recovers this. |
| 10 | `ts_document_inventory` | {lab} | doubtful | Drops the lab result. The label says 'no marker result', which is false if the lab is AFP or hCG. The tree has a markers tier that needs imaging, so the gate has no better option, but the label contradicts the tick. |
| 10 | `ts_document_inventory` | {ihc} | doubtful | Drops an IHC result the tree can use (the IHC checklist is reachable only from histology). The label asserts 'no tissue', yet an IHC report implies tissue. Understates safely, but a result the registrar may want kept is lost. |
| 10 | `ts_document_inventory` | {cytology, ihc} | doubtful | Drops IHC, which sits at or above cytology in the tier order (IHC implies a cell block or tissue). The label asserts 'no tissue', and the cytology branch cannot use IHC. |
| 10 | `eg_document_inventory` | {imaging, lab} | doubtful | Option claims an AFP or hCG result, but 'lab' also covers blood count, hormone assay or LDH, and the engine offers no fall-back to the imaging-only option. The downstream 'Neither marker is raised' answer only partly recovers this. |
| 10 | `eg_document_inventory` | {lab} | doubtful | Drops the lab result. The label says 'no marker result', which is false if the lab is AFP or hCG. The tree has a markers tier that needs imaging, so the gate has no better option, but the label contradicts the tick. |
| 10 | `eg_document_inventory` | {ihc} | doubtful | Drops an IHC result the tree can use (the IHC checklist is reachable only from histology). The label asserts 'no tissue', yet an IHC report implies tissue. Understates safely, but a result the registrar may want kept is lost. |
| 10 | `eg_document_inventory` | {cytology, ihc} | doubtful | Drops IHC, which sits at or above cytology in the tier order (IHC implies a cell block or tissue). The label asserts 'no tissue', and the cytology branch cannot use IHC. |
