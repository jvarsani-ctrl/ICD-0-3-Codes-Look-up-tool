# Group 7 — open questions for the registrar

**2 October 2026**, from the Group VII build on branch `claude/group-7-tumor-pathway-a88513`.
Each item says what the tool does today, so nothing here blocks the build, and what decision is
needed. Items 1–8 and 18–21 are coding decisions; 9–13 are REDCap and shared-layer items; 14–17 are
documents and scope. Items 18–21 were added after the independent review of 3 October 2026.

Full reasoning for every item is in `docs/group_07_build_contract.md`; the section is named against
each.

---

## Coding decisions

### 1. The baseline document for Group VII

**Today:** the tree is built on the International Pediatric Liver Tumors Consensus Classification —
López-Terrada D, et al. *Modern Pathology* 2014;27(3):472–491, and its update, López-Terrada D,
Stahlschmidt J, Pérez-Atayde AR. *Virchows Archiv* 2025;486(1):23–47 (Table 1, p. 24).
**Why:** the assigned baseline, Nagtegaal ID, et al. *Histopathology* 2020;76(2):182–188, never
mentions hepatoblastoma and prints no codes. Pfister 2022 states the WHO paediatric volume's
hepatoblastoma taxonomy is based on the consensus classification.
**Decide:** confirm López-Terrada 2025 as the Group VII baseline, or name another. (Contract §0.4.)

### 2. `8975/1` calcifying nested stromal-epithelial tumour

**Today:** a behaviour exclusion. The tool names `8975/1`, emits no Group VII code, and flags the case
for the registrar.
**Why:** ICD-O-3.2 has the code at behaviour 1 only; ICCC-3 Group VII admits behaviour 3. Most
children have a benign course; some relapse or metastasise (López-Terrada 2025, p. 43).
**Decide:** is this tumour registered, and if so on what code and in which group? REDCap pick 2 is
left in place until you rule. (Contract §3.1.)

### 3. Hepatocellular neoplasm NOS (HCN-NOS) has no ICD-O-3.2 code

**Today:** `8000/3` Neoplasm, malignant, at the liver (VIIc), with both candidates named and an
upgrade line saying the ruling is outstanding.
**Why:** a provisional consensus category between hepatoblastoma and hepatocellular carcinoma; these
children are treated as high-risk hepatoblastoma (López-Terrada 2025, pp. 29–31). The two candidates
sit in different ICCC subgroups.
**Decide:** `8970/3` Hepatoblastoma, NOS (VIIa1) or `8170/3` Hepatocellular carcinoma, NOS (VIIb).
The diagnostic pathway suggested `8970`. (Contract §3.3.)

### 4. Coding without tissue

**Today:** hepatoblastoma on imaging plus raised alpha-fetoprotein, child 6 months to under 3 years,
is `8970/3` at **basis 2**. An older child with a liver mass and no tissue is `8000/3`.
**Decide (a):** Visser rule 1 takes the highest basis used. Should the hepatoblastoma route record
basis **4** (tumour marker) because alpha-fetoprotein is part of the constellation? Visser Table 3
lists hepatoblastoma at basis 2, and basis 2 is the lower claim, so the tool uses it.
**Decide (b):** Visser Table 4 allows `8170/3` hepatocellular carcinoma at basis 4 on
alpha-fetoprotein with clinical investigation. Should the tool offer that route for an adolescent with
chronic liver disease (for example chronic hepatitis B), a liver mass and a raised alpha-fetoprotein?
In Uganda this presentation is plausible. Not built, because the Diagnostic Pathway reserves the
imaging route for hepatoblastoma. (Contract §0.6.)
**Decide (c):** Visser Table 3 also lists cholangiocarcinoma, `8160/3`, at basis 2 at C22.1, C24.0 and
C24.9. The tool records a likely cholangiocarcinoma without tissue as `8000/3`, the same as (b). Should
either route be built? The `hp_imaging_insufficient` reason now tells the clerk that both tables allow
these codes and that the ruling is outstanding. *(Added 3 October 2026, from checking Table 3 against
the rendered page.)*

### 5. The youngest age for the imaging route

**Today:** an infant younger than **6 months** is sent to tissue.
**Why:** Ferraro 2019 (PDF p. 7) finds alpha-fetoprotein reference intervals vary widely at least up
to 6 months. The Diagnostic Pathway wrote 4 months.
**Decide:** 6 months or 4. (Contract §4.2.)

### 6. Biliary mucinous cystic carcinoma: `8161/3` or `8470/3`

**Today:** the tree follows the report's words — "bile duct / biliary cystadenocarcinoma" to `8161/3`,
"mucinous cystic neoplasm with an associated invasive carcinoma" to `8470/3`. Both are ICD-O-3.2
terms on their codes.
**Decide:** whether the registry codes this tumour to one code whatever the wording. (Contract §3.5.)

### 7. A referral note that states a malignant liver tumour

**Today:** `8000/3` at **basis 1**, VIIc, with histology and IHC outstanding. Visser rule 5 allows it
when cancer is at least likely.
**Why this needs a look:** Group VI's referral node emits no code at all on a note alone. Group VII
records the malignancy at the weakest basis instead of dropping it, because a note alone cannot carry a
specific code but can carry `8000/3`.
**Decide:** keep basis 1 `8000/3`, or follow Group VI and emit nothing until imaging is in the file.

### 8. Benign and in situ liver lesions

**Today:** hepatocellular adenoma (`8170/0`), bile duct adenoma (`8160/0`) and high-grade biliary
intraepithelial neoplasia (`8148/2`) are behaviour exclusions; haemangioma, mesenchymal hamartoma,
focal nodular hyperplasia, other benign lesions and dysplastic nodules, which the consensus lists as
premalignant (López-Terrada 2025, Table 1, p. 24), are "not a reportable malignancy".
**Decide:** confirm that the registry does not register benign or in situ liver lesions. This also
decides whether the twenty in situ and metastatic REDCap picks are retired (item 9).

---

## REDCap and shared-layer items

### 9. REDCap repairs — `docs/group_07_layer1_repair.md`

9 relabels, 27 retires, 8 appends (picks 113–120: `8171`–`8175`, `8023`, `8054`, `8504/3`), pick 2 held for
item 2. `vii_morph` stores a pick number, so new options go at the end only. **Pick 113, fibrolamellar
carcinoma `8171/3`, matters most:** until it exists a fibrolamellar carcinoma can only be entered as
`8170`. Nothing has been applied.

### 10. Router rule `8158,8290` defaults to Group XI

**Today:** unchanged. **Why it is wrong:** ICCC-2017 places `8158` at the liver in VIIb (row 70) and
`8290` at the kidney in VIb (row 62), but the rule sends both to Group XI everywhere except C75.1. A
C22 branch would also catch `8290`, which is not a VIIb code, so the fix is to split the rule — a
Group III-owned rule this build did not touch. Only the output block's "Group routing" row reads these
rules today.

### 11. Two engine limitations met on this build

- **An alias that exists in two groups enters the first group** (`app.js`, express lane,
  `hit.groups[0]`). A liver rhabdoid tumour searched as "Rhabdoid tumor, NOS" entered the Group VI renal
  tree. Group VII's own aliases are now liver-specific, so none of them is shared, but Groups VIII and IX
  will meet this with Ewing sarcoma and rhabdoid tumour. A fix would ask which group, as the site
  picker already does.
- **`redcap_value` holds the ICD-O code**, by project convention, while `vii_morph` (like `iii_morph`,
  `iv_morph`, `viii_morph`) stores a pick number. The REDCap-framed output's "REDCap value" row
  therefore shows `8171`, not a pick number. The headline option string is what the clerk matches, so
  nothing mis-codes, but the row is misleading for those four groups.

### 12. `alias_index.json` is over its size guideline

31,675 bytes against Architecture §4C's ~30 KB. A WARN. Groups VIII and IX will add more.

### 13. An engine change made on this branch

`app.js`'s behaviour-exclusion panel read "Benign" for every exclusion. It now names the ICD-O
behaviour digit: benign, uncertain whether benign or malignant, in situ. It changes what Groups V and VI
display for `9514/1`, `8959/1` and `8960/1`, which were wrongly headed "Benign". **Confirm** the change is wanted
across groups.

---

## Documents and scope

### 14. The Diagnostic Pathway and the Alias Build Instructions are out of date

Both predate the rulings of 4 September and the ICD-O-3.2 table on disk. The build contract §5 lists
nine errors, among them "fibrolamellar carcinoma has no code of its own" (`8171/3` exists) and "`8170`
is Group XI off the liver" (ICCC-2017 places it in VIIb at any site). Neither vault document was
edited by this build. **Decide:** revise them to v2, or leave them with the contract as the record.

### 15. Hepatoblastoma subtype and PRETEXT are not captured

The pathway proposed capturing hepatoblastoma subtype, PRETEXT stage and specimen timing as
annotations. The tool codes them all `8970/3` and records nothing further, because no code depends on
them and ruling 9 keeps clinical detail out. **Decide:** whether the registry wants any of them
recorded.

### 16. Hepatocellular carcinoma subtypes without their own code

Macrotrabecular massive, steatohepatitic and other WHO 2019 subtypes are coded `8170/3` under
"subtype not listed". Only the five ICD-O-3.2 subtype codes `8171`–`8175` are offered. The WHO
digestive volume's liver chapter would confirm this (`docs/sources-requested.md` item 12).

### 17. Extrahepatic bile duct sites

`8160`–`8162` and `8170`–`8180` are Group VII at any site, but C23.9 and C24.x have no row in
`topography_codes.json`, so the router cannot reach Group VII from a gallbladder or extrahepatic bile
duct primary. Extremely rare in children. **Decide:** whether to add those topography rows.

---

## Added after the independent review, 3 October 2026

### 18. A malignant rhabdoid tumour that keeps INI1

**Today:** a report that **diagnoses** malignant rhabdoid tumour is coded `8963/3` on that diagnosis,
with IHC shown as outstanding if it is not recorded. A tumour whose report **describes rhabdoid cells**
without that diagnosis goes to the INI1 step: lost → `8963/3`; retained → `8000/3`, pending.
**Why:** Vokuhl 2016 (p. 927, case 17) reports a malignant rhabdoid tumour with typical morphology and
INI1 retained; López-Terrada 2014 (p. 479) keeps rhabdoid tumour a histomorphological diagnosis; the
consensus lists an INI1-positive malignant rhabdoid tumour (López-Terrada 2025, Table 1, p. 24).
**Decide:** confirm coding a report-diagnosed rhabdoid tumour on the diagnosis alone, and how to code
rhabdoid cells with INI1 retained.

### 19. Basis of diagnosis for the fibrolamellar molecular findings

**Today:** a `DNAJB1::PRKACA` fusion is basis 8; PRKAR1A loss is basis 7.
**Why:** Visser rule 10 gives basis 8 only to an abnormality specific to the cancer. The fusion is specific
among primary liver tumours (Graham 2015, p. 822), but López-Terrada 2025 (p. 29) notes it also occurs in
oncocytic pancreatic and biliary neoplasms. PRKAR1A loss is read by immunohistochemistry and is the
Carney-complex lesion.
**Decide:** keep 8 for the fusion, or drop it to 7; confirm 7 for PRKAR1A.

### 20. The consensus table and its text disagree on small cell undifferentiated hepatoblastoma

López-Terrada 2025, Table 1 (p. 24), still lists "Small cell undifferentiated, (INI1)+/−" under
hepatoblastoma, while its text (p. 25) and Vokuhl 2016 reclassify the INI1-lost tumours as malignant
rhabdoid tumours. **The tool follows the text.** Confirm.

### 21. REDCap pick 89

The first draft of the repair package relabelled pick 89 ("Intracystic carcinoma, NOS", an `8504/2` term)
to the `8504/3` term. That would have changed every stored record on that pick from in situ to invasive.
The package now retires pick 89 and appends the `/3` term as pick 120. Nothing was applied either way.
