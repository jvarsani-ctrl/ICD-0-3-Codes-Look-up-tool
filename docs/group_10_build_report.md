# Group X — build report, 2026-10-04

**Branch:** `claude/group-10-tumor-pathway-3a99f7`, cut from `main` at `dbe5fd4` and brought up to
`main` at `334c586` (Group IX merged, the registrar's 4 October rulings). Not pushed, not merged.
Plan: `docs/group_10_build_contract.md`. Code decisions: `docs/superpowers/specs/2026-10-04-group-10-germ-cell-code-decisions-design.md`
(D1–D22). Questions for the registrar: `docs/group_10_registrar_review.md`. REDCap-side list:
`docs/group_10_layer1_repair.md` and `docs/TODO.md` §7 and §27.

| | |
|---|---|
| Entries | 136 (code, behaviour) pairs from 131 ICD-O-3.2 codes; 171 ICCC records |
| Trees | `g10_cns` 11 nodes · `g10_ovary` 18 · `g10_testis` 17 · `g10_extragonadal` 14 — 60 nodes (a deposit node per gonadal and extragonadal tree added 6 October 2026) |
| Emitted | 49 (code, behaviour) pairs on code branches; 36 behaviour exclusions |
| Immunohistochemistry panels | 4, one per tree, 8 rules each, every rule with a witness |
| Aliases | 123: each code emitted by at least one tree a search can reach, less five generic terms Group III holds (128 before they were left out, 46 under the earlier filter, which required every reachable tree to emit it; all 6 October 2026) |
| Validator | four Group X rules; 24 negative controls, all caught |

---

## 1. What this group is, and the facts that reshaped it

ICCC-3 Group X: germ cell tumours (central nervous system Xa, extragonadal Xb, gonadal Xc),
gonadal carcinomas (Xd) and other gonadal tumours (Xe). The same four-digit code sits in Xa, Xb or
Xc by site, so 18 entries carry `iccc3_subgroup_by_topography` and the router's `tree_routing`
picks the tree from the recorded topography.

### ★ The Diagnostic Pathway coded germinoma to the wrong number

ICD-O-3.2 prints *Germinoma* as the preferred term of `9064/3`, with *Germ cell tumor, NOS* as its
synonym; `9060/3` is *Dysgerminoma*. The pathway (§1, §8 item 11) and the Alias Build Instructions
(lines 23, 117, 231, 369) map central nervous system germinoma to `9060`. Built: `9064/3` (D1).

### ★ The behaviour digit decides, and ICCC-2017 declares it per site

ICCC-2017 ranges 94–99 (Xa) declare behaviours `0-1,3`; every other range declares `3`. A mature
teratoma is a Group X code in the brain and a behaviour exclusion in the ovary. Three entities the
pathway builds as Group X codes exist in ICD-O-3.2 only below behaviour 3 and leave the group:
gonadoblastoma `9073/1` (so Xc7 is empty), juvenile granulosa cell tumour `8622/1` and `8622/0`,
and germ cell neoplasia in situ `9064/2`.

### ★ REDCap offers the in situ term on the germinoma number

`x_morph` labels `9064` "Intratubular malignant germ cells", the `/2` term, and `9100` "Hydatidiform
mole, NOS", the benign term, for the number that carries choriocarcinoma. `9086` reads "Label not
found". Listed in `docs/group_10_layer1_repair.md`; the tool does not act on it (standing rule 16).

---

## 2. The baseline

| Need | Source | Held |
|---|---|---|
| Testis entities with ICD-O codes | Moch H, et al. European Urology 2022;82(5):458–468, Table 3, pp. 464–465 | `Group 6 Papers/` |
| Central nervous system germ cell entities | Louis DN, et al. Neuro-Oncology 2021;23(8):1231–1251, Table 1, p. 1235 | `Group 3 Papers/` |
| Paediatric entities at every site | Pfister SM, et al. Cancer Discovery 2022;12(2):331–355, Table 3, pp. 342–343 | `Group 4 Papers/331.pdf` |
| Registration without tissue | Visser O, et al. Frontiers in Oncology 2023;13:1250549, Table 4, p. 06 | `docs/references/` |
| Immunohistochemistry | Siegmund 2023 (Human Pathology 133); Wu 2020; Rougemont 2018 | `Group 10 Papers/` |
| Ovary | **none on disk.** Höhn 2021, the assigned baseline, covers the vulva, vagina and cervix only (PMC8494521, read 4 October 2026). Candidate: McCluggage WG, Singh N, Gilks CB. Histopathology 2022;80(5):762–778, not in PubMed Central | requested (D22) |

Every code was settled against `icdo32.sqlite`; the WHO documents decided which entities are
current. The one paper fetched was Höhn 2021, through PubMed.

---

## 3. Where the sources disagree

| Point | Pathway or secondary source | Built, and why |
|---|---|---|
| Germinoma | `9060` | `9064/3` — ICD-O-3.2 (D1) |
| Germ cell tumour, type not named | `9065/3` | `9064/3` — ICD-O-3.2 synonym; Visser Table 4 (D2) |
| No-tissue diagnosis | coded by dominant marker: `9071/3`, `9100/3`, `9085/3` | Visser Table 4: `9065/3` or `9064/3` at basis 4 (D4) |
| Immature teratoma | `9083` | `9080/3`; `9083/3` is *Malignant teratoma, intermediate* (D5) |
| Gonadal `8000–8005` | conflict with Master §6 (Group XII) | Xe — ICCC-2017 range 117 (D13) |
| `9086` | "label not found"; Alias Build Instructions: obsolete | `9086/3` *Germ cell tumor with associated hematological malignancy*, new in ICD-O-3.2 (D17) |
| Partial mole | Alias Build Instructions: `/1` | `9103/0`, excluded (D8) |
| Polyembryoma | Moch Table 3: `9085/3` | `9072/3` — ICD-O-3.2 (D7) |
| Placental site trophoblastic tumour | Moch Table 3: `9104/3` (February 2022) | exclusion `9104/1` — ICD-O-3.2; registrar (D8) |
| Adult granulosa cell tumour of ovary | pathway: `/1` | `8620/3` — *Terms that are changing behaviour*, p. 4 (D11) |
| Malignant androblastoma | pathway: Xe code | off the tree; every `8630` term is `[obs]` (D11) |

Not built from the pathway, each for a stated reason (D10, D15): the disorder-of-sex-development
entry and karyotype variables; pubertal status, p57, genotype, FOXL2, DICER1, SMARCA4, i12p and
serum calcium as captured variables; the `clinical_alert` strings, which are in
`docs/clinical-warnings.md` under Group X (ruling 9).

---

## 4. The trees

Four trees, one per site family, written once in `build/group10_tree.py` as functions
parameterised by site. Each opens on a `document_inventory` evidence gate. Each evidence context
has its own node — referral, referral after cytology, imaging, imaging after markers, imaging after
cytology — because `app.js` replaces a captured `evidence_tests` list rather than merging it; a
walk of every terminal (1,620 on the final trees) finds the evidence on every path equal to the
reports the clerk said are on file. The no-tissue routes emit only `8000/3` (basis 1 or 2) or the Visser Table 4 codes (basis 4).

Histology nodes offer each site's own terms (the ovary: dysgerminoma, struma ovarii, the
sex cord–stromal and epithelial lists; the testis: the seminoma terms, prepubertal and
postpubertal teratoma, germ cell neoplasia in situ; other sites: the trophoblastic tumours and
`9086/3`), then a shared germ cell core in one order. The immunohistochemistry panel resolves a
germ cell tumour whose type the report does not name: embryonal carcinoma on OCT3/4 with CD30 or
SOX2; the germinoma family on OCT3/4 with CD117, SOX17 or D2-40; yolk sac tumour only on two
markers (glypican-3 with tissue alpha-fetoprotein, or with nuclear HNF1-beta), because glypican-3
also stains choriocarcinoma and teratoma (Siegmund 2023 Table 1, p. 34; p. 38). Fallback
`9064/3` *Germ cell tumor, NOS*. Every rule cites its page.

---

## 5. Shared-layer changes

| File | Change |
|---|---|
| `presentation_router.json` | `groups["10"]` built, four trees, `tree_routing` (Xa 24 codes → `g10_cns`; C56.9 → `g10_ovary`; C62.0, C62.1, C62.9 → `g10_testis`; Xb 122 codes → `g10_extragonadal`; default `g10_extragonadal`); one `8000-8005` branch, C56.9 and C62 → group 10, Xe; Group 3 added to the "Mass / swelling (solid tumour)" presentation (registrar review B1, 6 October 2026) |
| `topography_codes.json` | `C62.0`, `C62.1`, `C76.3` added; Group 10 added to `C38.1`, `C38.3`, `C48.0`; `C76.3` lists groups 9 and 10; Group 10 added to the 24 Xa codes C70.0–C72.9 and C75.1–C75.3 (registrar review B1, 6 October 2026) |
| `build_database.py` | `GROUP10`; behaviour row `{"3"}`; `ROUND_TRIP_GROUPS`; four rules |
| `alias_index.json` | regenerated |

`app.js`, `index.html`, `uccf-tool.css` and every Group I–IX data and alias file are
byte-identical to `main`.

---

## 6. Rules this group adds

| Rule | Asserts | Source |
|---|---|---|
| `check_group10_codes_fit_site` | every emitted (code, behaviour) lies in a Group X range covering the tree's routed sites and declaring that behaviour; no exclusion does | `ICCC-2017.sqlite` |
| `check_group10_no_pathology_codes` | tissue-free paths emit only `8000/3` at basis 1–2, or `9064/3`, `9065/3` (and `9100/3` extragonadal) at basis 4 with imaging and markers on the path | the walked path; Visser rules 4–6, Table 4 |
| `check_group10_alias_terms_match_icdo32` | an alias equal to an ICD-O-3.2 term maps to its code and is true of every behaviour the group emits for it (D21); no germinoma alias on `9060` | `icdo32.sqlite` |
| `check_group10_subgroups_and_routing` | the subgroup shown equals ICCC-2017's at every lookup code; each routing list equals exactly ICCC's site family | `ICCC-2017.sqlite`, router, lookup |

24 controls in `build/negative_controls_group10.py`, recorded in
`docs/validator_negative_controls.md`; R2-B ("the path, not the flag") is the one that matters
most. Five controls were added after review because the rules they test were missed by the
earlier versions: three in rule 3 and two in rule 4, whose first version checked destinations only.

---

## 7. What the browser and the walks found that the build did not

1. **Captured evidence was erased on three paths** (cytology then referral; markers then
   histology; cytology then imaging). The data gate and the engine gate passed throughout; a walk
   that compared each terminal's evidence with what the clerk had said was on file found it. Fixed
   by one node per evidence context. Group VIII's cytology path has the same shape (`docs/TODO.md` §29).
2. **The stop screen misstates the fact at a central nervous system site.** Searching "Germinoma"
   at C71.0 stops with "C71.0 … is not a site that group codes this term at". ICCC-2017 range 94
   places germinoma at C71.0 in Xa1. The message reads `candidate_groups`, which list Group III
   alone. Registrar review B1. Closed 6 October 2026 by the B1 decision: "Germinoma" at the
   pineal enters `g10_cns` and records `9064/3` Xa1.
3. **D21 costs three searches.** "Mature teratoma", "Immature teratoma" and "Dermoid" find nothing,
   because an alias on `9080` or `9084` would show on every behaviour's output ("Also called" is
   keyed by code, `docs/TODO.md` §30). "Teratoma" finds them.
4. **Five generic search terms stop at the central nervous system sites** (found 6 October 2026,
   after the B1 decision). "Neoplasm, malignant" and the four `8001`–`8004` terms are Group X
   aliases because the ovary and testis trees emit them, and Group III holds the same strings.
   At a site that now lists Groups 3 and 10, the search stops with "The site does not decide the
   group", which is untrue for Group X: ICCC-2017 range 42 places `8000` there in IIIf and
   `g10_cns` emits none of the five. **Closed 6 October 2026** (registrar): the five are left out
   of Group X's aliases (`EXCLUDED_TERMS` in `build/generate_group10_aliases.py`), so at the brain
   sites they enter Group III again. At the ovary and testis these searches now stop, and the
   guided route still codes them. Registrar review B1.

Seven cases driven on 4 October 2026, all as specified: ovarian dysgerminoma by search → `9060/3`
Xc1; germinoma at C71.0 → stop for referral; front door, mass, C76.3, Group X → immature teratoma
`9080/3` Xb2; testicular mixed tumour with choriocarcinoma → `9101/3` Xc5; ovary, imaging with raised
alpha-fetoprotein → `9065/3` basis 4; ovarian mature cystic teratoma → exclusion `9080/0`; adult
granulosa cell tumour of the ovary → `8620/3` Xe. No console errors.

Seven walks on 6 October 2026, after the B1 decision: mass at the pineal → Group III or Group X
offered → Group X → germinoma `9064/3` Xa1; "Germinoma" searched at the pineal → `g10_cns` →
`9064/3` Xa1; mass at the cerebellum → Group III chosen → Group III's posterior fossa tree;
organ-functional sign at the pineal → Group III's midline tree, no group screen; "Dysgerminoma"
searched at the ovary → `9060/3` Xc1; organ-functional sign at C55.9 → Groups IX, X and XI, as
before; "Neoplasm, malignant" searched at C71.6 → the stop in item 4. No console errors.

---

## 8. The merge of `main`

`main` moved during the build: Group IX merged, and the registrar ruled on 4 October that the data
carries no REDCap fields and that the search box asks the site of any group whose data reads it.
The branch took `main` (`e2963fd`) and adapted: the entries dropped `redcap_option_verified`,
`awaiting_layer1` and the drift sentences; `g10_site_unstated`, built for a search with no
topography, became unreachable and was removed; the extragonadal routing list grew from 75 to 114
codes to take Group IX's lookup additions.

---

## 9. What needs you

`docs/group_10_registrar_review.md`, ordered by cost. The first three:

- **B1. Decided 6 October 2026, option (a).** Group 10 is listed at the 24 Xa sites and Group 3 on
  "Mass / swelling", so `g10_cns` is reached from every presentation except "Organ-functional
  sign" and from the search box. Open under B1: Group III's three gaps. The five generic search
  terms in §7 item 4 are closed. The germ cell referrals Groups VII, VIII and IX make from the liver,
  bone and soft tissue still lead nowhere (B2).
- **A1. Juvenile granulosa cell tumour is not registered** — the commonest paediatric sex
  cord–stromal tumour, excluded by ICD-O-3.2's behaviour.
- **A2–A3. Germ cell tumour of unnamed type and the marker route code to `9064/3`, which prints as
  "Germinoma".**

---

## 10. Proof

| Gate | Result |
|---|---|
| `python3 build/build_database.py` | BUILD PASSED — 1082 checks, 0 FAIL, 94 WARN |
| `python3 build/induce_flow.py --check` | every rule has a witness |
| `python3 build/generate_group10_entries.py --check` | up to date |
| `python3 build/negative_controls_group10.py` | 24 of 24 caught, 5 of 5 probes pass |
| `python3 build/group09_negative_controls.py <repo>`, `negative_controls_group08.py` | unchanged |
| `node build/check_engine_flow.mjs` | OK |
| Browser | seven cases on 4 October 2026 and seven walks on 6 October 2026, §7 |
| Groups I–IX, `app.js`, `index.html`, `uccf-tool.css` | byte-identical to `main` |

The seven Group X warnings: six search-only entries whose ICD-O-3.2 preferred term is marked
`[obs]` (8130/3, 8141/3, 8245/3, 8440/3, 8450/3, 8630/3 — the same class Groups III, VI and VII
carry), and one listing the six codes `x_morph` does not offer.
