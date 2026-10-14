# Question-flow changes, Group 5 (Retinoblastoma)

Branch `flow-g05`, made on 14 October 2026 from `main` at `f19df62e21b589c08263d2a622cac976aba83bd1`. Never pushed. The reachability review of the same group (`reach-g05`) starts from this branch and reads this file first.

Data file `data/database/group_05_dt.json`: SHA-256 `3ea75a5f7daa9116bc5da62f3a93013d381534bf16ee825046aa6c6b427d5599` before, `cb55b169ae4771e3a5f5c3f855635f38906a40e4a812d0dc6196e79641835689` after. `app.js` is unchanged (`d293eda3641e12d05fea2966e1f53e929c12855a1f4c9419f73125bf6f3fee37`).

## 1. What changed

**No screen, answer, tick box or captured variable was merged, split, renamed, reordered or removed.** All seven screens keep their node ids, node types, answer counts and answer order, and every answer keeps the destination, code, behaviour, referral, outstanding tests, basis of diagnosis and captures it had. A click list written by answer position, by tick id or by feature and diversion position is still valid.

What changed is wording only: 4 questions, 6 hints, 19 labels (17 answers and rows, 1 feature, 1 diversion). Eighteen of the 19 labels went from 94–317 characters to 90 or fewer. The nineteenth, the first screen's inadequate-specimen row, went from 138 to 125 characters and cannot go lower, see section 4.

- Each label now states one fact. Detail that made a label long (the alternative wordings of one finding, the definitions of grade G1 to G4, what leukocoria is) moved into the screen's hint, which the clerk reads above the answers.
- Restatements of what the first screen already established were removed: the third screen no longer says "No tissue exists", and the fourth screen's answers no longer say "no tissue is in the file" or "no tissue yet obtained". (The inadequate-specimen row reaches the third screen with a specimen in the file, so the old sentence was also untrue on that route.)
- The diffuse-pattern box on the third screen no longer adds "or a child aged five years or older". The age is asked once, as the unticked box "Child under five years of age", and an unticked box and the old age clause lead to the same screen. Build contract section 4.1 lists the age clause inside the diffuse criterion; the clause is carried by the box, and no route changed.
- Wording the lint found was removed from the screens edited: "actually", capitals for emphasis (INADEQUATE, UNINTERPRETABLE), the double hyphen, "Feature 2" (a number the clerk cannot see), "not available everywhere" on the third screen, and two meta sentences that spoke to the author ("this option exists only because the report may already be in the file", "the only clinical-alias node in the tool").

## 2. Mapping: old answer and wording to new

Identity on every click: an old answer at position *i* is the new answer at position *i*. Only the text differs.

| Screen | Field | Old | New |
|---|---|---|---|
| `rb_document_inventory` | answer 4 | A specimen (cytology, or enucleation/exenteration) was obtained but is reported INADEQUATE, non-diagnostic, or technically UNINTERPRETABLE | A specimen (cytology, or enucleation/exenteration) was obtained but is reported inadequate, non-diagnostic or uninterpretable |
| `rb_clinical_alias` | answer 0 | Note states retinoblastoma, or describes leukocoria (white pupillary reflex, or 'cat's-eye reflex') or strabismus with a suspected intraocular tumour of the retina | Note names retinoblastoma, or describes leukocoria or strabismus with a suspected tumour |
| `rb_clinical_alias` | answer 1 | Note describes a mass, a red-reflex abnormality, or 'for eye examination' with no diagnosis asserted — or the differential named includes a non-malignant cause (for example Coats disease or persistent hyperplastic primary vitreous) that could equally explain the findings | Note states no diagnosis, or names a non-malignant cause that could equally explain it |
| `rb_imaging_pathway` | feature 1 | Calcification within the mass — on ultrasound, high-reflectivity foci casting acoustic shadows | Calcification within the mass (high-reflectivity foci casting acoustic shadows) |
| `rb_imaging_pathway` | diversion 1 feature | A flat, diffusely infiltrating intraocular process with no discrete mass, or a child aged five years or older | A flat, diffusely infiltrating intraocular process with no discrete mass |
| `rb_imaging_insufficient` | answer 0 | Findings match a non-malignant mimic — retinal detachment or exudate with no calcified mass (Coats disease / persistent hyperplastic primary vitreous pattern), or an anterior-segment/inflammatory picture (pseudohypopyon) — and no tissue is in the file | Mimic pattern: retinal detachment or exudate with no calcified mass, or pseudohypopyon |
| `rb_imaging_insufficient` | answer 1 | Findings match the diffuse variant (a flat, diffusely infiltrating process with no discrete mass, or a child aged five or older), or show extraocular or orbital extension — no tissue yet obtained | Needs tissue: diffuse pattern, age five or older, or extraocular or orbital extension |
| `rb_imaging_insufficient` | answer 3 | Tissue has since been obtained — an enucleation or exenteration specimen with a pathology report is now in the file | Tissue has since been obtained — an enucleation or exenteration report is now in the file |
| `rb_cytology` | answer 0 | Cytology or liquid biopsy shows malignant cells consistent with retinoblastoma, with necrosis, mitoses and/or nuclear atypia present | Malignant cells consistent with retinoblastoma, with necrosis, mitoses or nuclear atypia |
| `rb_cytology` | answer 1 | Cytology or liquid biopsy is non-diagnostic, shows scant material or sampled retinal neurons only, or the diagnostic features of malignancy (necrosis, mitoses, nuclear atypia) are not present | Non-diagnostic: scant material, retinal neurons only, or no features of malignancy |
| `rb_enucleation_report` | answer 0 | Diffuse infiltrating growth — the tumour spreads laterally within the retina with no discrete mass | Diffuse infiltrating growth, spreading within the retina with no discrete mass |
| `rb_enucleation_report` | answer 1 | Fleurette formation or neuronal differentiation (grade G1); numerous Flexner-Wintersteiner rosettes, moderately differentiated (grade G2); or, on the Mendoza anaplasia scale, a retinocytoma-grade area or mild anaplasia recorded within an otherwise viable retinoblastoma; and no poorer grade or severe anaplasia stated | Differentiated: grade G1 or G2, mild anaplasia, or a retinocytoma-grade area; none poorer |
| `rb_enucleation_report` | answer 2 | Occasional rosettes, poorly differentiated (grade G3); no rosettes present, anaplasia, poorly differentiated (grade G4); or, on the Mendoza anaplasia scale, severe anaplasia (also where a G1 or G2 grade is stated beside it) | Poorly differentiated or undifferentiated: grade G3 or G4, or severe anaplasia |
| `rb_enucleation_report` | answer 3 | Enucleation performed; the report states no differentiation grade and no growth pattern (grade GX) — or states only moderate anaplasia on the Mendoza scale with no differentiation grade given | No grade and no growth pattern stated (grade GX), or moderate anaplasia only |
| `rb_enucleation_report` | answer 5 | The report describes a shrunken, calcified, non-functional globe (phthisis bulbi) with no viable tumour — consistent with spontaneous regression | Phthisis bulbi: a shrunken, calcified, non-functional globe with no viable tumour |
| `rb_retinocytoma_word` | answer 0 | The entire specimen is retinocytoma/retinoma — no viable (malignant) retinoblastoma component is described anywhere in the specimen | The whole specimen is retinocytoma or retinoma; no viable retinoblastoma anywhere |
| `rb_retinocytoma_word` | answer 1 | The word describes an area of differentiation within an otherwise viable, active retinoblastoma — a 'retinocytomatous area', or retinocytoma-grade on the Mendoza anaplasia scale — and the report states no poorer grade and no severe anaplasia for the rest of the tumour | Area in a viable tumour; no poorer grade and no severe anaplasia stated |
| `rb_retinocytoma_word` | answer 2 | The word describes an area of differentiation within an otherwise viable, active retinoblastoma, and the report states a poorly differentiated grade (G3 or G4) or severe anaplasia for the rest of the tumour | Area in a viable tumour; report states a poorly differentiated grade or severe anaplasia |
| `rb_retinocytoma_word` | answer 3 | The word describes an area of differentiation within an otherwise viable, active retinoblastoma, and the report also states a diffuse infiltrating growth pattern | Area in a viable tumour; report also states a diffuse infiltrating growth pattern |

Questions and hints edited (full text in the diff of `data/database/group_05_dt.json`): S1 question; S2 hint; S3 hint; S3 question; S4 hint; S4 question; S5 hint; S6 hint; S7 hint; S7 question.

## 3. Click lists that are now stale

None by position. A click list or real-page replay that finds an answer by its visible label is stale for the 19 labels above and for the questions of screens 1, 3, 4 and 7. `build/flow_golden_g05.json` holds the 41 routes recorded before the edit, by position, and still passes.

The engine gate holds one assertion that finds three answers of `rb_retinocytoma_word` by the text they contain (`states a poorly differentiated grade`, `also states a diffuse infiltrating growth pattern`, `no poorer grade and no severe anaplasia`). The new labels of that screen keep those three phrases.

## 4. What the edit could not do, and why

- **First screen, `rb_document_inventory`.** `docs/evidence_documents/group_05.json` pins its hint, its five labels' first 70 characters and its option count, and the data gate fails on any difference. The hint therefore keeps "not available everywhere" and "actually", and the inadequate-specimen row (125 characters) stays over 90, as do the three tier labels the clerk never sees (122 to 163 characters). Needs the registrar to release one string in that file.
- **Retinocytoma screen, `rb_retinocytoma_word`.** The engine-gate assertion above fixes its node id, its four answers and three phrases. Merging it into `rb_enucleation_report` as one tick list was built and replayed in a scratch copy and passes every route (Registrar Queue, RQ2) but cannot be applied while that assertion stands.
- **Repeats the engine cannot skip.** See Control Requests CR1 to CR3 in the workbook.

## 5. Pathway findings for the reachability review

Each was replayed through the engine on this branch. None changes a code in this review.

1. **PF1. Histology listed as outstanding after a histology report is reported.** Imaging only, then "Tissue has since been obtained — an enucleation or exenteration report is now in the file", then any subtype answer ends on 9511, 9512 or 9513 with Histology outstanding and basis of diagnosis 7. The same codes reached by ticking the Histology report on the first screen list no outstanding test. The fourth screen's third answer captures no evidence test.
2. **PF2. No answer for an incomplete imaging constellation with no tissue-needing feature.** Mass and calcification ticked, age not stated, no diversion box ticked: the fourth screen opens and offers a mimic, a tissue-needed pattern or tissue obtained. None says "a required feature is missing", although the question names that case. A clerk can take the mimic answer, which ends the case as not reportable.
3. **PF3. The inadequate-specimen row discards ticked tissue reports.** Cytology and Histology report ticked, plus the inadequate-specimen row: the case goes to the imaging screen. The same ticks without the row go to the enucleation screen. A chosen row routes at once and reads no ticks.
4. **PF4. Known open.** An empty tick set lands on the referral tier, and an IHC or genetic report alone is dropped (`docs/evidence_document_mapping.md`, Group 5 rows).

## 6. Gate additions (additive)

`build/flow_golden_g05.json` and a section in `build/check_engine_flow.mjs` (`ONLY=g05` runs it alone). It replays the 41 recorded routes and asserts the same code, behaviour, referral group, outstanding tests, basis of diagnosis and evidence credited; asserts that every label the page draws is 90 characters or fewer except the pinned row; and asserts that no question, hint, answer, feature or diversion carries the wording removed here. Controls: swapping two destinations, dropping a credited test, and restoring the pre-edit wording each fail the section for the right reason.

## 7. Checks

`python3 build/build_database.py`: 1334 checks, 0 failures, the same counts as `main`. The engine gate passes. Every one of the 558 answers the clerk can give on the seven screens leads to the same next screen or terminal in the old and the new data. The real page returned the same code, behaviour, basis of diagnosis, referral group and outstanding tests as the engine for all 41 routes, twice.

## 8. The registrar's rulings of 14 October 2026 (branch `reach-g05`, uncommitted)

The registrar answered the Registrar Queue of both workbooks the same day. Sections 1 to 7 describe the wording-only edit; this section describes what the rulings changed on top of it. The old statement that no screen, answer or route moved holds for sections 1 to 7 only.

| Item | Ruling | What changed |
|---|---|---|
| RQ1 | Remove both | `rb_imaging_insufficient` loses the two "Tissue has since been obtained" answers. A clerk with a new report goes back to the first screen. The defect behind them (PF1, Histology listed as outstanding) goes with them. |
| RQ2, RQ6 | Merge; a retinocytoma-grade area is read as an area | `rb_enucleation_report` is one tick screen, read in file order: diffuse growth 9513, poorly differentiated or undifferentiated 9512, differentiated or a retinocytoma-grade area 9511, whole-specimen retinocytoma 9510/0, phthisis bulbi 9514/1, nothing 9510/3. `rb_retinocytoma_word` is removed (seven nodes become six). The engine-gate assertion that named it now drives the merged screen. |
| RQ3 | Coats disease to be excluded (it may not be reported in the file) | `rb_clinical_alias` is a tick list. A named non-malignant cause is read first and makes the case not reportable; leaving it unticked is the usual case. Read as option B of the queue item. |
| RQ4 | Asked whether any paper supports MRI plus clinical suspicion; then chose A, tissue needed | No paper does (Visser 2023 rule 4, p. 03; Foerl 2008; Nelson 2025; recorded in the node's author note). `rb_imaging_insufficient` is now a first-match tick list, tissue first, then mimic, then the referral note, then nothing, so tissue wins in the data when both patterns are ticked. |
| RQ5 | Option A | First screen's hint replaced with the registrar's text, the inadequate-specimen row shortened to "A specimen was taken but reported inadequate or non-diagnostic". `docs/evidence_documents/group_05.json` carries the new wording. |
| RQ7 | Option B | The first screen offers Imaging report, Cytology report, Liquid biopsy report and Histology report. The node carries its own list (`tick_list.items`); the shared list of seven is unchanged, so no other group's first screen moves. A file with none of the four ticked is the referral tier. |
| RP1 | Option A | The fall-through takes the rungs in order, cytology, imaging, referral wording. A required imaging feature that is not stated and a referral note in the file read the note (`rb_clinical_alias`). A mimic pattern and a pattern that needs tissue do not fall through: the imaging itself says what the findings are, and the note's own rule (Visser 2023 rule 4, p. 03) would be overruled by a wording the imaging contradicts. |
| RP2 | Pseudohypopyon is diffuse retinoblastoma too | Pseudohypopyon is its own diversion box (it was bundled with an anterior-segment mass) and the fourth screen's needs-tissue answer names it. An anterior-segment mass stays with the mimics. Build contract §4.1 and §2.5 are amended. |
| RP3 | Without imaging it is a suspected neoplasm | The fourth screen gains "A required feature is not stated, and no referral letter or clinical note is in the file", which refers Group XII provisional (8000/3). |
| RP4 | Option A | A liquid biopsy report is a box on the first screen and fits the cytology tier. `rb_cytology` gains the answer "Liquid biopsy reports a tumour-specific genetic change" (9510/3, basis of diagnosis 5). Placed on this node's own list, not the shared one (RQ7 removed boxes that change no route, and the box would change none in the other groups). |
| RP5 | Not connected to Group III; a metastatic scenario. 698 proposed and checked, then "go with eye": the eye stays the topography and the mass goes in the registry's site-of-metastasis field, which has its own topography code | `docs/clinical-warnings.md` and the build contract are corrected. The alias entry *Trilateral retinoblastoma* loses `refer_group: 3`, `refer_code` and `reason` (`data/aliases/aliases_group_05.json`); the engine never rendered them. No screen carries the instruction, and the engine gate asserts that no Group 5 alias refers to another group. 698 exists, but ICD-O-3 Rule C limits `.8` to adjacent, contiguous sites. |
| RP6 | Specimen inadequate means no histological diagnosis; warn on a discrepancy | The inadequate-specimen row beats a ticked histology report. A warning banner shows under the checklist while both are chosen, and the case drops the histology tick, so the result never lists that report as its evidence. New row field `tick_conflict` (engine, data gate, one gate section). |

New engine surface, group-agnostic: `tick_conflict` on a special-situation row (`app.js` `tickConflictNotice()` and `tickContinue()`), its validation in `build/build_database.py`, and node-level `items` in the evidence-mapping applier (`build/apply_evidence_documents.py`). `data/shared/presentation_router.json` is unchanged.

Tables rewritten: `build/flow_golden_g05.json` now holds 59 routes and `build/pathway_cases_g05.json` 51 cases, with every expectation typed from the ruling or the Pathway, not copied from a run. Controls are in `docs/engine_flow_negative_controls.md`. The routes the first version stood for (41, recorded on `main`) are no longer the table: 22 started from the two removed answers, and the rest were rewritten for the new first screen and the tick screens.

Result: `python3 build/build_database.py` 1334 checks, 0 failures, 105 warnings (one more than before, the merged node's author note naming 9514, which the build's own message calls expected). The real page was driven through six awkward scenarios and agreed with the engine; the first run found that the result listed a discarded histology report as its evidence, which is fixed and has its own assertion.

