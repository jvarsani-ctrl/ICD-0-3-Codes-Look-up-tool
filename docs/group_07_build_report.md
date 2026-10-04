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
INI1-retained rhabdoid tumour exists (Vokuhl 2016, p. 927). Rhabdoid cells the report does not call a
malignant rhabdoid tumour go through INI1 and SMARCA4: either lost → `8963/3`; both retained → the
report's own diagnosis (`8970/3` for hepatoblastoma, `8000/3` when no type is named); SMARCA4 not
recorded → the same code with IHC outstanding (registrar ruling, 3 October 2026; §10).

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
macOS PDFKit, because neither poppler nor a Python PDF library was installed during the build.

On 3 October 2026, once PDF libraries were installed, the five table pages the tree depends on were
rendered to images and checked against the printed tables: López-Terrada 2025 Tables 1 and 2
(pp. 24, 29), Visser 2023 Tables 3 and 4 (pp. 04, 06) and Ferraro 2019 Table 4 (p. 10). Every cited
figure matched. Two corrections followed. Visser Table 3 also lists cholangiocarcinoma, `8160/3`, at
basis 2 at C22.1; the contract, the shared transcription `docs/references/visser-2023-key-points.md`
and the `hp_imaging_insufficient` reason now say so, and registrar item 4(c) asks whether to build it.
López-Terrada Table 1 lists dysplastic nodules as premalignant, not benign; the contract and the
benign-lesion option now say so. Neither correction changes a code or a route.

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
| `hp_histology` | histology_subclassification | twenty-two diagnoses — codes, onward steps, four behaviour exclusions, referrals to Groups I, II, IX, X |
| `hp_ini1` | ihc_checklist | the INI1 fork: SMARCB1 or SMARCA4 loss → `8963`; small cell undifferentiated with INI1 retained → `8970`; INI1 retained → SMARCA4 decides: lost → `8963`, retained or not recorded → the report's diagnosis (`8970` or `8000`), with IHC outstanding when SMARCA4 was not recorded |
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
`docs/group_07_layer1_repair.md` lists every pick: **10 relabel, 27 retire, 8 append (picks 113–120)**
— pick 2, `8975`, joined the relabels on the ruling of 3 October 2026 (§11). The relabels include `8970` "Hepatoblastoma", which is not an
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

---

## 10. Registrar ruling on rhabdoid cells with INI1 retained, 3 October 2026

The registrar did not accept coding "rhabdoid cells, INI1 retained" as `8000/3` on one case (Vokuhl
2016, p. 927). The literature search, recorded under open question 18, found that the current
definition requires loss of INI1 or SMARCA4 and that rhabdoid-looking tumours keeping INI1 are mostly
other tumours. Built the same day:

| Change | Where |
|---|---|
| The rhabdoid-cells option splits by what the report calls the tumour; the plain hepatoblastoma option excludes rhabdoid cells | `hp_histology` |
| A SMARCA4-retained marker, and eight rules in place of four | `hp_ini1`; flow chart regenerated by `build/induce_flow.py` |
| `outstanding_tests[]`: a branch names tests its finding leaves owed. Group-agnostic, four lines; the reverse of `satisfies_tests[]`. Registrar's choice over upgrade-line-only and over `8000/3` until SMARCA4 | `app.js`, `finish()` |
| `check_outstanding_tests()`: closed vocabulary, code-emitting branch, never also in `satisfies_tests` | `build/build_database.py`, all groups |
| Rule 4(g): INI1 retained without SMARCA4 retained must owe IHC and name SMARCA4; 4(f) admits an option stating that the report diagnoses hepatoblastoma | `check_group7_ini1_fork()` |
| Controls 4J, 4K, 4L, OT1, OT2; 4E now deletes every `8970` rule | `build/negative_controls_group07.py` |

**A matcher defect found on the way.** `_G7_RETAINED_MARKER_RE` matched "RETAINED" case-insensitively,
so it also matched every loss marker, whose text ends "internal control retained". No earlier clause
needed to tell the two apart. Rule 4(g)'s first correct-data run failed on the INI1-loss rule; both
retained-marker patterns are now anchored on "performed and RETAINED".

**Verification.** 621 checks, 0 FAIL, engine gate included; every rule has a witness; 42 of 42
controls caught and correct data passes. Engine control: the same rule run through `main`'s `app.js`
gives a workup without IHC, and through this branch's gives IHC outstanding. Driven in the browser:
hepatoblastoma with rhabdoid cells, INI1 retained, SMARCA4 not done → `8970/3`, IHC pending, upgrade
naming SMARCA4; both retained → `8970/3`, complete; rhabdoid cells with no type, both retained →
`8000/3`, complete, upgrade asking for the tumour type; SMARCA4 not done → `8000/3`, IHC pending;
SMARCA4 lost → `8963/3`; small cell undifferentiated, SMARCA4 not done → `8970/3`, IHC pending; both
retained → `8970/3`, complete; INI1 lost → `8963/3`.

**Merge note.** `app.js` now also changes `finish()` (the `outstanding_tests` block after the
provisional block). No other group uses the field, so no other group's output changes.

**Vault documents not edited.** The Decision Tree master file's §3F, which documents
`satisfies_tests`, lives in the vault outside this repository; it needs a line for `outstanding_tests`.

---

## 11. Registrar ruling on calcifying nested stromal-epithelial tumour, 3 October 2026

Open question 2. The tumour is registered in Group VII: `8975/1` in the usual case, and `8975/3` under
the ICD-O matrix rule when the report calls it malignant or describes metastases (ICCC-2017 row 67,
VIIa1). It replaces the behaviour exclusion.

| Change | Where |
|---|---|
| Two entries, `8975/1` and `8975/3`, the only ones outside the generated inventory | `build/generate_group07_entries.py` (`build_ruled_8975`); 94 entries |
| The calcifying nested stromal-epithelial tumour option splits by what the report says about malignancy | `hp_histology` |
| `ICDO32_MATRIX_RULE`: a registrar-ruled (group, code, behaviour) passes the round-trip only while icdo32.sqlite prints the same term at the source behaviour | `build/build_database.py`, all groups; one entry |
| `GROUP7_RULED_PAIRS` admitted by rule 1; `8975` removed from the rule 2 absent codes | `build/build_database.py` |
| Rule 10, `check_group7_cnset()`: Layer 1 anchors, both entries emitted, `8975/3` only on an option asserting malignancy or metastases, `8975/1` never on one | `build/build_database.py` |
| The two aliases map to `8975` | `aliases_group_07.json` |
| Controls 10A–C and RT2; 2A, 2B, 3A, 3C retargeted, since the exclusion they broke no longer exists | `build/negative_controls_group07.py` |

**Verification.** 628 checks, 0 FAIL, engine gate included; 46 of 46 controls caught and correct data
passes. Driven in the browser from the express lane ("CNSET"): both options appear; the usual case
records `8975` with the behaviour-1 reason, the malignant case records `8975` with the matrix-rule
reason, both VIIa1, workup complete. Rule 10(a)'s anchors read Layer 1 itself and have no in-memory
control.

**Found while driving it.** The headline shows `8975` for both; nothing but the "Why" row tells the clerk
the behaviour, and REDCap has no field for it. Open question 22.

---

## 12. Registrar ruling on hepatocellular neoplasm NOS, 3 October 2026

Open question 3: `8970/3` Hepatoblastoma, NOS, following López-Terrada 2025, p. 30 (PHITT treats these
children as high-risk hepatoblastoma). The histology option now emits `8970/3`; its `satisfies_tests`
and upgrade line are gone. The generator's `8970` and `8000` notes say so. A new alias, "Hepatocellular
malignant neoplasm NOS" (the consensus name, López-Terrada 2014, p. 481), joins "Hepatocellular neoplasm
NOS" and "HCN-NOS"; all three map to no code, so "Also called" on a hepatoblastoma output does not list
them (the alias layer's third constraint).

Verification: 628 checks, 0 FAIL; controls all caught. Browser: "Hepatocellular malignant neoplasm"
finds Group 7; the option records `8970/3`, workup complete, with the PHITT reason; a plain
hepatoblastoma's "Also called" names none of the three.

---

## 13. Registrar ruling on coding without tissue, 3 October 2026

Open question 4: go with Visser 2023.

| Case, no diagnostic tissue | Recorded | Visser |
|---|---|---|
| Hepatoblastoma constellation (unchanged) | `8970/3`, basis 2 | Table 3; Table 4 has no hepatoblastoma row, so no basis 4 |
| Hepatocellular carcinoma likely, alpha-fetoprotein raised | `8170/3`, basis 4 | Table 4, p. 06 |
| Hepatocellular carcinoma likely, alpha-fetoprotein not raised or not reported | `8170/3`, basis 2 | Table 3, C22.0 |
| Intrahepatic cholangiocarcinoma likely | `8160/3`, basis 2 | Table 3, C22.1 |
| Malignant, no type named or another type | `8000/3`, basis 2 | rule 5 |

The three new options sit at the top of `hp_imaging_insufficient`; its hint and question say when a
specific code is allowed. `hp_imaging_pathway` gains a seventh diversion, so a record naming
hepatocellular carcinoma or cholangiocarcinoma leaves the hepatoblastoma constellation. Rule 6 admits
`8170` at basis 2 and 4 and `8160` at basis 2, and fails basis 4 on an option that does not say
alpha-fetoprotein is raised. Controls 6A retargeted (`8172` at basis 2), 6D and 7E added.

Verification: 628 checks, 0 FAIL; controls all caught. Browser: each new option records its code and
basis (4 — Specific tumour markers; 2 — Clinical investigation without tissue), subgroup VIIb, Histology
outstanding.

---

## 14. Registrar ruling on the youngest age for the imaging route, 3 October 2026

Open question 5: 6 months, as built. No change to the tree or the checks; rule 7 already fails an
imaging node without the under-6-months diversion (control 7C).

---

## 15. Registrar ruling on biliary mucinous cystic carcinoma, 3 October 2026

Open question 6: both codes exist in ICD-O-3.2 at behaviour 3, so both stay — `8161/3` and `8470/3` —
and the report's wording decides, as built. One addition: "Biliary cystadenocarcinoma" was a second name
inside the `8161` alias and so could not be searched; it is now an alias of its own.

---

## 16. Registrar ruling on the referral note, 3 October 2026

Open question 7: go with Visser 2023. Rule 5 was cited for `8000/3` at basis 1, but rule 3 decides
whether basis 1 is available, and it keeps basis 1 for cancers found by physical examination — head and
neck, eye, breast, skin, superficial soft tissue, external genitals, vagina, cervix, anus, rectum,
prostate — not the liver. The earlier route rested on a misreading.

| The note | Now |
|---|---|
| reports the imaging or alpha-fetoprotein the diagnosis rests on | enters `hp_imaging_pathway`; coded as those reports would be — `8970/3`, `8170/3`, `8160/3` or `8000/3` at basis 2 or 4 |
| gives a malignancy as likely, names no method | `8000/3`, basis 9 (rule 1), Histology and IHC outstanding |
| cancer only possible | not registered (rule 4), unchanged |

Rule 6 admits `8000/3` at basis 9 and no longer at basis 1; control 6B now breaks the basis-9 option to
basis 1. The imaging step's question and its `8000/3` option now accept imaging reported in a note.
Verification: 628 checks, 0 FAIL; 49 controls caught. Browser: both note routes give the codes and bases
above.

---

## 17. Benign liver lesions, 3 October 2026

Open question 8, in part. REDCap's Group VII list has no benign liver picks; a non-cancer case is
`dx_cancer` = No plus free text in `dx_exclusion`. The registrar ruled that the benign cases stay in the
tool and the output calls them "Benign neoplasm (benign tumour)".

| Change | Where |
|---|---|
| Behaviour 0 heading reads "Benign neoplasm (benign tumour)" — every group's behaviour-0 exclusion | `app.js`, `BEHAVIOUR_LABELS` |
| `non_reportable_heading`: a non-reportable branch may replace the generic banner. Group-agnostic, text only | `app.js`, `exclude()` |
| `check_non_reportable_heading()`: only on a `non_reportable` branch, non-empty | `build/build_database.py`, all groups |
| The benign/premalignant/non-neoplastic option splits in three, following López-Terrada 2025, Table 1: benign tumours (heading set), dysplastic nodule (premalignant), non-neoplastic lesion | `hp_histology` |
| Controls NH1, NH2 | `build/negative_controls_group07.py` |

Verification: 635 checks, 0 FAIL; all controls caught. Browser, after forcing a fresh `app.js`: the
benign-tumour option and both adenomas read "Benign neoplasm (benign tumour)"; the dysplastic nodule and
the non-neoplastic lesion read "Not a reportable malignancy". Merge note: `app.js` changes in
`exclude()` and `BEHAVIOUR_LABELS`.
