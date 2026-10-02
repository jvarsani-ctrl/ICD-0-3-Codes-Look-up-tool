# Group VII — build report, 2026-10-03

**Branch:** `claude/group-7-tumor-pathway-a88513`, cut from `main` at `cff8149`. `main` untouched;
nothing pushed. **Contract:** `docs/group_07_build_contract.md`. **Questions for you:**
`docs/group_07_open_questions.md`.

Read §1 and §7 if you read nothing else.

---

## 1. What this group is, and the three facts that shaped it

Ninety-two codes. **The paediatric disease sits on a handful**: `8970/3` hepatoblastoma, `8963/3`
malignant rhabdoid tumour of the liver, `8991/3` undifferentiated embryonal sarcoma, `8170/3`
hepatocellular carcinoma with its subtypes `8171`–`8175`, `8180/3` combined
hepatocellular-cholangiocarcinoma and the cholangiocarcinomas. The other carcinoma codes are the ICCC-3
carcinoma block placed at the liver, reachable by direct code entry.

**Fibrolamellar carcinoma has its own code, `8171/3`.** The Diagnostic Pathway (§4D, §8.3) says it has
none and collapses to `8170`. ICD-O-3.2 carries `8171/3`, and ICCC-2017 range 71 (`8170-8180`, any site)
admits it. It is 15–25% of paediatric hepatocellular carcinoma over five years (López-Terrada 2025,
p. 29). The tree codes it `8171`; REDCap has no option for it yet.

**A small cell undifferentiated hepatoblastoma is usually not a hepatoblastoma.** In Vokuhl 2016 (p. 925)
22 of 23 tumours first diagnosed as small cell undifferentiated hepatoblastoma or malignant rhabdoid
tumour had lost INI1, and the authors class them all as malignant rhabdoid tumours of the liver. The
tree never codes a small cell undifferentiated tumour as hepatoblastoma without an INI1 result: lost →
`8963/3`, retained → `8970/3`, not done → `8000/3`. About 5% of rhabdoid tumours keep INI1 and lose
SMARCA4 (López-Terrada 2025, p. 37), which is a second route to `8963`. A report that diagnoses
malignant rhabdoid tumour is coded `8963/3` on that diagnosis whatever INI1 shows, because an
INI1-retained rhabdoid tumour exists (Vokuhl 2016, p. 927).

**The assigned baseline does not cover the group.** Nagtegaal 2019 never mentions hepatoblastoma. The
build uses the International Pediatric Liver Tumors Consensus Classification, which Pfister 2022 names
as the basis of the WHO paediatric volume's hepatoblastoma taxonomy (§2).

---

## 2. The baseline

Nagtegaal 2019 (PMC7003895) and Pfister 2022 (PMC9401511) were retrieved from PubMed Central and searched
in full. Nagtegaal covers the adult carcinomas and fibrolamellar carcinoma's `DNAJB1::PRKACA`
translocation, and nothing on hepatoblastoma, rhabdoid tumour or embryonal sarcoma. Pfister defers to the
consensus classification. Both consensus papers are on disk: López-Terrada 2014 (*Modern Pathology*) and
López-Terrada 2025 (*Virchows Archiv*), whose Table 1 (p. 24) gives the entity list the tree is built on.
Neither prints ICD-O codes, so every code was settled term by term against `icdo32.sqlite`.

No registry-implications paper exists; the MeSH sweep in `Group 7 Papers/` found none.

The PubMed connector was pending in this session; the two papers were fetched from NCBI's public
E-utilities into the session's scratch directory, not into the vault. Papers on disk were read with
macOS PDFKit, because neither poppler nor a Python PDF library is installed.

---

## 3. The tree

`g7_hepatic`, twelve nodes, entry `hp_document_inventory`:

| Node | Type | Does |
|---|---|---|
| `hp_document_inventory` | document_inventory | five evidence routes; captures `primary_site` C22 on each |
| `hp_clinical_alias` | clinical_alias | a note stating malignancy → `8000/3` at basis 1; otherwise not registered |
| `hp_imaging_pathway` | imaging_pathway | solid liver mass + alpha-fetoprotein raised for age → `8970/3` at basis 2; six diversions |
| `hp_imaging_insufficient` | morphology_only | `8000/3` at basis 2, not registrable, or tissue now in file |
| `hp_cytology` | morphology_only | `8970` / `8170` at basis 5, `8000`, or back to imaging |
| `hp_histology` | histology_subclassification | twenty-one diagnoses — codes, onward steps, four behaviour exclusions, referrals to Groups I, II, IX, X |
| `hp_ini1` | ihc_checklist | the INI1 fork: SMARCB1 or SMARCA4 loss → `8963`; small cell undifferentiated with INI1 retained → `8970`; rhabdoid cells with INI1 retained → `8000` |
| `hp_hcc_subtype` | histology_subclassification | `8170`, `8172`–`8175`, or fibrolamellar → molecular step |
| `hp_flc_molecular` | cytogenetics_dropdown | `8171` at basis 8 or 7; `8170` only when the report revises the diagnosis |
| `hp_biliary` | histology_subclassification | `8160`, `8162`, `8470`, `8161` by the report's wording |
| `hp_other_carcinoma` | morphology_only | `8140`, `8240`, `8246`, `8023`, `8020`, `8010` |
| `hp_secondary_deposit` | site_resolution | a metastasis is referred to its primary's group (I–VI, VIII–XI); unknown primary → XII |

No new node type and no new field; Group VII uses existing constructs only.

---

## 4. Shared-layer changes

**Router.** `groups["7"]` built. `dual_group_rules["8963"]` gains a C22 → VIIa2 branch (before it, a
hepatic rhabdoid tumour fell to IXd3, which ICCC-2017 does not admit at C22). `dual_group_rules["8991"]`
is new: C22 → VIIa3, otherwise IXa. `dual_group_rules["8000-8005"]` gains a C22 → VIIc branch.
`dual_group_rules["8170"]`'s default moves from group 11 to group 7, because ICCC-2017 range 71 is
any-site and no Group XI range carries `8170`. Ownership of `8963` and `8991` was agreed with the
Group IX session by cross-session message; the Group VIII session was told about the shared `8000-8005`
rule.

**`app.js`, one group-agnostic change.** The behaviour-exclusion panel was headed "Benign" for every
exclusion. It now names the ICD-O behaviour digit. This also corrects Groups V and VI, whose `/1`
exclusions read "Benign" (§7 item 13).

**`build/build_database.py`.** Nine Group 7 rules (§6). Group 7 joins `check_icdo32_round_trip()` in
place of `check_redcap_exact_names()`, as Groups III, IV and VI did, and `BEHAVIOUR_DECLARED_BY_GROUP`
gains GROUP7.

**New files.** `build/generate_group07_entries.py` regenerates the entries from the two databases and
derives `redcap_option_verified` and `awaiting_layer1` from Layer 1 instead of writing them by hand.
`build/negative_controls_group07.py` reruns every control.

**Documents.** `docs/codes-awaiting-redcap.md` (Group 7 section, seven codes),
`docs/clinical-warnings.md` (Group VII section, twelve rows), `docs/group_07_layer1_repair.md`,
`docs/group_baseline_documents.md` (row VII closed), `docs/sources-requested.md` (items 11, 12),
`docs/TODO.md` §7 (Group VII row), `docs/validator_negative_controls.md` (Group VII section).

**Not edited:** the Diagnostic Pathway and Alias Build Instructions in the vault (§7 item 14), and
`topography_codes.json`.

---

## 5. Layer 1 — forty-two findings

`vii_morph` stores a pick number, 1–112, translated by `vii_code`; new options can only be appended.
`docs/group_07_layer1_repair.md` lists every pick: **9 relabel, 27 retire, 8 append (picks 113–120),
1 held for your ruling (`8975`)**. The ten relabels include `8970` "Hepatoblastoma", which is not an
ICD-O-3.2 term, and two obsolete synonyms used as labels (`8162` "Klatskin tumor", `8482`). Seven labels
carry pasted transcription notes. Nothing has been applied.

---

## 6. What the build passed and the browser found

The build reported 0 FAIL before the browser drive. Driving the tool found six defects, every one of
them the kind the standing rules warn about: the case looked better evidenced, or better resolved, than
it was.

1. **"SCUD hepatoblastoma" listed under "Also called" on every `8970` output**, including a case coded
   on imaging alone. The alias mapped to both `8970` and `8963`. It now maps to no code; rule 4(e) and
   control 4F guard it.
2. **"Workup: complete — no outstanding tests" above an upgrade line saying INI1 was not done.** `8000`
   required histology only. It now requires histology and IHC.
3. **Hepatocellular neoplasm NOS showed "Upgrade: none — fully subtyped"** on a case awaiting your
   ruling. It now says the ruling is outstanding.
4. **The calcifying nested stromal-epithelial tumour, `8975/1`, was headed "Benign".** Engine fix, §4.
5. **The flow asked for INI1 loss after INI1 had been recorded as retained.** The loss rule now names
   retention as negative.
6. **The express lane found nothing for SCUD, UESL, CNSET, HCN-NOS, HCC, FLC, cHCC-CCA, Klatskin, NUT
   carcinoma or liver cancer**, because the index reads the `alias` field only. Each is now its own
   alias. Six aliases shared with Groups III and VI sent a liver rhabdoid tumour into the renal tree;
   Group VII's primary aliases are now liver-specific.

The negative-control pass found two defects in the new checks themselves: a false FAIL on correct data
in rule 8, and rule 9 comparing an integer with a string so that a wrong subgroup could never fail. Both
fixed (`docs/validator_negative_controls.md`).

## 6b. What the independent review found

One reviewer subagent read the branch against the contract, the databases and the papers on
3 October 2026. Every finding was checked against its source before it was fixed.

- **Critical, fixed.** An INI1-retained malignant rhabdoid tumour was coded `8970` hepatoblastoma with
  "Workup: complete": one histology option carried both the small cell undifferentiated pattern and a
  rhabdoid diagnosis into the INI1 step. Vokuhl 2016 (p. 927, case 17) reports exactly that tumour. The
  option is now three (§1), and rule 4 gains clause (f), which fails any route that can reach `8970`
  without describing a small cell undifferentiated pattern.
- **Fixed.** PRKAR1A loss was recorded at basis 8; it is read by immunohistochemistry and is not specific
  to fibrolamellar carcinoma, so it is now basis 7. The INI1 hint misdescribed the Vokuhl cohort. Three
  histology-proven fallback and exclusion terminals carried no basis of diagnosis. The REDCap package
  relabelled pick 89 from an in situ term to an invasive one, which would have changed stored records.
- **Fixed, minor.** A citation for embryonal sarcoma's cyst-like imaging pointed to the wrong paper; the
  metastasis step lacked retinoblastoma and CNS and sent gonadal carcinoma to Group XI; four generic
  aliases would capture other groups' searches; several wording points.
- **The fix exposed a defect in the check itself.** The shared negation matcher also reads 90 characters
  after a term, so "pattern predominates, with no rhabdoid cells" read as not asserting the small cell
  pattern. Rule 4 now uses a before-only matcher. The correct-data run caught it.

Three statements in the first draft of the contract were wrong and are corrected in place: `8158`'s
REDCap label is an obsolete `8158/3` term, not an `8158/1` term; the Layer 1 count is 42, not 36; and one
sentence attributed to López-Terrada 2025 a conclusion the paper does not state.

---

## 7. What needs you

Twenty-one items, in `docs/group_07_open_questions.md`. The five that change codes:

1. **Hepatocellular neoplasm NOS** — `8970/3` or `8170/3`? The tool records `8000/3` until you rule.
2. **`8975/1` calcifying nested stromal-epithelial tumour** — registered or not, and where.
3. **Coding without tissue** — basis 2 or 4 for the hepatoblastoma imaging route; and whether to build
   Visser Table 4's `8170/3` route for adolescents with chronic hepatitis B, a liver mass and a raised
   alpha-fetoprotein.
4. **A referral note stating a malignant liver tumour** records `8000/3` at basis 1. Group VI emits
   nothing in the same case.
5. **The baseline** — confirm López-Terrada 2025.

And one REDCap change that matters more than the rest: **append `8171` fibrolamellar carcinoma as
pick 113.**

**One deliberate departure from Group VI, recorded here as its coding note promised:** the imaging
`8970` terminal shows histology as outstanding work, where Group VI's `8960` imaging terminal
suppresses it. The paediatric liver consensus asks for a biopsy in every patient (López-Terrada 2014,
p. 484), so suppressing the row would show the case as better worked up than it is.

---

## 8. Proof

| Step | Result |
|---|---|
| `python3 build/build_database.py` | **614 checks, 0 FAIL**, engine gate included (`main`: 479) |
| `python3 build/induce_flow.py` | every rule in every checklist has a witness |
| `build/negative_controls_group07.py` | **37 of 37 caught**; all eleven checks OK on correct data |
| Groups 1–6 | `dt.json`, alias files, `topography_codes.json`, `index.html`, `uccf-tool.css` byte-identical to `main` |
| Browser, `http://localhost:8817` | driven through the UI and confirmed: hepatoblastoma imaging route; a diversion (age ≥ 3) to `8000/3`; INI1 lost → `8963`, small cell undifferentiated retained → `8970`, rhabdoid cells retained → `8000`, not done → `8000`; report-diagnosed malignant rhabdoid tumour → `8963`; fibrolamellar with fusion → `8171`, revised → `8170`; hepatocellular neoplasm NOS → `8000`; sarcoma → Group IX; calcifying nested stromal-epithelial tumour → behaviour exclusion; referral note → `8000` basis 1; cytology → `8970` basis 5; C22.1 cholangiocarcinoma → `8160`; unknown-primary metastasis → Group XII; other carcinoma → `8010` with search upgrade; the express lane; the REDCap-framed output. No console errors |

---

## 9. Merge notes — Groups VIII and IX are being built at the same time

These shared files will conflict at merge. Each conflict resolves by keeping both sides.

| File | Group VII touches | Expected overlap |
|---|---|---|
| `build/build_database.py` | `GROUP7` beside `GROUP6`; one `BEHAVIOUR_DECLARED_BY_GROUP` row; the round-trip and exact-name guard tuples; a constants block and a function block after Group 6's; dispatch lines after Group 6's | Groups VIII and IX add the same kinds of lines in the same places |
| `data/shared/presentation_router.json` | `groups["7"]`; `8963`, `8991`, `8000-8005`, `8170` rules | Group VIII may add a C40/C41 branch to `8000-8005`; disjoint |
| `data/aliases/alias_index.json` | regenerated | regenerate after merging the alias files; never hand-merge |
| `docs/*` shared files | appended sections | appended at the ends of the same files |
| `app.js` | `BEHAVIOUR_LABELS` beside `BASIS_LABELS`; one heading line | none expected |

**Reported by the Group IX session, 3 October 2026** (branch `claude/group-9-tumor-pathway-911c69`, 0 FAIL):
it removed `dual_group_rules["9473"]` from the router and the `"9473"` exemption from
`check_router_cns_topography_completeness()`, on the grounds that ICCC-2017 places `9473` in IIIc2 at
every site and ICD-O-3.2 codes peripheral PNET at `9364/3`. No Group VII rule or check reads `9473`, so
the two branches do not interact there. It expects text conflicts with this branch in
`build/build_database.py`, the end of `docs/clinical-warnings.md`, `docs/codes-awaiting-redcap.md` and
`alias_index.json`; keep both sides and regenerate the index.
