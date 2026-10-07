# Group V — build report, 2026-09-22

**Branch:** `group-05-retinoblastoma`, cut from `group-04-neuroblastoma`.
**Build:** `python3 build/build_database.py` — **347 checks, 0 FAIL, BUILD PASSED**.
**Contract:** `docs/group_05_build_contract.md`. **Layer 1 repair:** `docs/group_05_layer1_repair.md`.

---

## 1. What this group is, and why it is the smallest and the least standard

One subgroup. One tumour. **Four codes.** Group V is the smallest group in ICCC-3 and the only one
so far whose modal case is diagnosed with **no tissue at all**.

| ICD-O-3.2 | Term | Built |
|---|---|---|
| `9510/3` | Retinoblastoma, NOS | ✅ the dominant output |
| `9511/3` | Retinoblastoma, differentiated | ✅ report-wording only |
| `9512/3` | Retinoblastoma, undifferentiated | ✅ report-wording only |
| `9513/3` | Retinoblastoma, diffuse | ✅ report-wording only |
| `9510/0` | Retinocytoma | ❌ `behaviour_exclusion` |
| `9514/1` | Retinoblastoma, spontaneously regressed | ❌ `behaviour_exclusion` |

The inventory was **generated**, not transcribed: `build/generate_group_inventory.py --group V`
returns `usable 4`, and names `9514` as absent — absent *at a declared behaviour*, because ICD-O-3.2
carries it only at `/1` and ICCC-3 Group V declares `3`.

**Three facts drove every design decision** (contract §0.5): biopsy of an intact globe is an
absolute contraindication, so there is no histology-first route; diagnosis is clinical plus
imaging, so the imaging route is the spine and not an exception; and no molecular finding changes
the code, so `code_neutral_molecular` is `true` on all four entries.

---

## 2. The cross-cutting source did more work here than in any group so far

Group V has **no registry-implications paper** — confirmed twice (contract §10.6). What replaced it
was one row of **Visser O, et al. Frontiers in Oncology 2023;13:1250549, Table 3, pp. 04–05**:

> Retinoblastoma · basis **1 or 2** · **C69.2** · `9510/3`

Retinoblastoma is one of only **five** entities in the entire European Network of Cancer Registries
scheme registrable at **basis 1 — clinical examination alone**. No other group gets an entity, a
topography, a code and a basis handed to it in one line.

It also bounded the group: Table 3 licenses `9510/3` **and nothing else** without pathology, which
is validator rule 3b, and its **rule 4, p. 03** — *"possible" is not registrable* — is the citation
behind the leukocoria-mimic terminal.

---

## 3. What the baseline paper settled, and what it could not

The registrar supplied **Milman T, et al. *The 5th Edition of the World Health Organization
Classification of Tumours of the Eye and Orbit.* Ocular Oncology and Pathology 2023;9(3–4):71–95**
mid-build. It was read in full. Full working in contract §10.

**The provisional flag comes off.** The "Editorial" tag is real and is not a measure of standing:
25 pages, organised by chapter with *ICD-O coding* subsections, written by the volume's **own
editorial board** — the same model as Louis 2021 for the central nervous system. No better
candidate exists.

**Two real weaknesses replace the withdrawn one.** It summarises a **beta version ahead of print**
(April 2023) while the bound volume printed **23 January 2026** — thirty-three months, no published
comparison. And **it states no ICD-O code anywhere**: "ICD-O" occurs once in twenty-five pages, as a
subsection heading in Table 1, never with a number. Same standing as Group 4's baseline: it
corroborates which entities exist; `icdo32.sqlite` states the numbers.

**★ The finding that shaped the tree.** Table 9 lists, under premalignant and malignant retinal
tumours, exactly two entities: **Retinocytoma** and **Retinoblastoma**. Differentiated,
undifferentiated and diffuse appear nowhere as subtype names.

**But Table 9 lists tumour *types*.** The paper's own **Table 2** defines *type*, *subtype* and
*pattern* as three different things, and Table 1 shows *Subtypes* is a subsection **inside** an
entity's own section. **A subtype would not appear in Table 9 at all.** So Table 9's silence proves
the three are not separate *types* and says nothing about whether they are *subtypes* carrying
codes — the question the governing test actually asks, and the entity page is paywalled.

So `9511`, `9512` and `9513` are **built and reachable only from the pathology report's own stated
grade or growth pattern**. The tool records; it does not grade. Removing them on this evidence
would repeat the error that wrongly deleted `9430/3` and `9480/3` from Group 3.

**The paediatric volume is not this group's spine, and that question is now closed.** Pfister 2022's
complete full text contains *eye*, *ocular* and *retina* **zero** times, and *retinoblastoma* once,
in a list of predisposition syndromes. Its coverage is chapter-by-chapter and uneven — check the
full text before assuming it for Groups VI, VII or X.

---

## 4. Shared-layer changes

### 4.1 `topography_codes.json` — the eye had one code and needed nine

`C69` held **`C69.9` alone**. `C69.2` (retina) — the topography Visser Table 3 names for
retinoblastoma — **did not exist in the file**. A retinoblastoma at the retina could not reach
Group V at all. All nine REDCap C69 codes were added with REDCap's own labels.

`C69.6`'s REDCap label reads `So! tissue of orbit` — ligature damage, the same defect class as
`docs/TODO.md` §1.3, which now records this second instance. Written correctly in the JSON; the
REDCap source was not edited.

### 4.2 `C69.4` — a Group 4 tumour that could reach no group at all

C69.4 (ciliary body) carries `candidate_groups: [5, 4]`: ICCC-3 gives `9501`–`9504` to **Group IVb**
everywhere outside C70.0–C72.9, so an intraocular medulloepithelioma is a Group IV tumour and a
genuine leukocoria mimic. Milman 2023 Table 10 gives the discriminator — medulloepithelioma
expresses **LIN28A and PAX8**.

That change made `check_group4_topography_map` (rule 5) FAIL correctly: no Group 4 tree declared
C69.4. Fixed by declaring it on `g4_other_peripheral`, whose `op_medulloepithelioma` node was
already the right destination. **This closed a pre-existing gap, not just one I opened** — before
the C69 expansion, no ciliary body case could reach any group.

> The diagnostic pathway document says medulloepithelioma "routes Group III/IV/V by site". It never
> routes to Group V (contract §5.3). Three other pathway statements are wrong and are corrected in
> contract §5 — most consequentially that `9514` is `/3`, which it is not.

### 4.3 `presentation_router.json`

`groups["5"]` built, one tree, one handoff. No `tree_routing`, no `tree_selection`, no new
`dual_group_rules` entry — Group V's codes route nowhere else. `site_to_group["C69"]` and the
`organ_functional_sign` archetype were already correct and were left alone.

---

## 5. The seven validation rules, and what each would have caught

Rule 2 is a generalisation, not a new check. **All thirteen negative controls caught; zero false
FAILs** — `docs/validator_negative_controls.md`.

| | Rule | What it binds |
|---|---|---|
| 1 | `imaging_pathway` shape | must declare `insufficient_next_node`, must not declare `options[]` |
| 2 | `behaviour_exclusion` **generalised** | was hard-guarded to Group 4; now reads `BEHAVIOUR_DECLARED_BY_GROUP` |
| 3 | Visser Table 3 | every emitted code in `{9510,9511,9512,9513}`; **basis 1 or 2 emits `9510` only** |
| 4 | `9514` banned | as `morphology_code`, `nos_fallback_code` or alias target — never in prose |
| 5 | `imaging_sufficient` | true on `9510` only |
| 6 | no immunohistochemistry | zero `ihc_checklist` nodes; `ihc_markers_*` null |
| 7 | `code_neutral_molecular` | true on every entry |

**Rule 1 is an engine fact and sweeps every group** — FAIL for Group 5, WARN elsewhere. Run against
the repository it independently rediscovered the three Group 3 nodes that **throw at runtime**
(`pf_imaging_no_tissue`, `st_imaging_pathway`, `sp_imaging_no_tissue`) with exactly the dead-option
counts `docs/TODO.md` §10 recorded — 6, 4 and 4. A positive control nobody had to construct. They
are on `main`, outside this branch, so they are reported and not fixed.

**Rule 3b is the one that matters most.** A subtype emitted at basis 2 is a syntactically perfect
record saying a diffuse retinoblastoma was established by imaging — when diffuse retinoblastoma is
the one variant with *no* calcified mass. Downstream it reads as a graded, enucleation-confirmed
tumour for a child whose eye was never removed.

**Rule 2 mattered more than it looks.** Before this branch, `check_behaviour_exclusion` began
`if ctx.group != GROUP4: return []`. Group 5's two blocks would have been authored and **never
validated at all**.

### 5.1 Two validator gaps found by the first correct tree

`ctx.transitions()` yielded `next_node` edges only. `insufficient_next_node` is equally an edge —
`fallbackTarget()` returns `{next_node: ...}` — so:

- `check_next_node_resolution` **never validated those targets**. A typo would throw at runtime and
  pass the build, the same class of crash TODO §10 records.
- `check_orphan_nodes` could not see the edge and reported `rb_imaging_insufficient` as an orphan —
  a **false FAIL on correct data**, which is the more corrosive failure.

Both closed by yielding the edge from `transitions()`.

---

## 6. Regression evidence for Groups 1–4

The validator at `HEAD` and the new one were run over identical data from the repository root.

| | checks | OK | WARN | FAIL |
|---|---|---|---|---|
| Validator at HEAD | 255 | 188 | 53 | 0 |
| With Group 5 rules | 279 | 189 | 59 | 0 |

**Diffed line by line, no finding changed for any group.** Every difference is one of the new
checks. Groups 1, 2 and 3's `dt.json` and alias files are byte-identical to HEAD; `group_04_dt.json`
differs by 3 lines (§4.2).

---

## 7. What a green build missed — the browser pass

Two defects passed 347 checks and were obvious in ten minutes of driving the tool.

### 7.1 `9510` required `Histology`, so the tool asked for a contraindicated procedure

`9510` was authored with `diagnostic_tests_required: ["Histology"]` and no `upgrade_path`. `9510`
is the **imaging-sufficient** code, reached with no tissue on the modal path, so the engine computed
Histology as **outstanding** and wrote its own sentence:

> *"Histology would yield a more specific code."*

— onto a case with an intact globe, where the only histology available is **removing the eye**. It
also listed Histology as an outstanding workup row, recording a correctly-coded case as
incompletely worked up. Contract §5.5 bans that framing outright; §5.4 maps examination under
anaesthesia, ultrasound and magnetic resonance imaging all onto `"Imaging"`.

Fixed: `9510` requires `["Imaging"]`; an `upgrade_path` is authored on the entry, which suppresses
the engine's automatic sentence on **every** 9510 terminal; and `satisfies_tests: ["Imaging"]` sits
on the cytology and enucleation-GX branches, because imaging is not outstanding on a case that
already has cells or a removed eye.

Now renders: **Workup — Complete, no outstanding tests. Basis 2 — clinical investigation without
tissue.** Upgrade: *"Enucleation is a TREATMENT decision, not an outstanding investigation… do not
request tissue on account of this code."*

### 7.2 Twenty-eight alias chips compressed to 18 pixels each

The *"Also called"* row rendered as `Re Rd RB Rd Ey Ey Ey Int Int Le Wh Wh Wh…`. `.aliases` is a
flex row and `.orow span { flex: 1 }` matched every chip: `white-space: nowrap` stopped the text
reflowing inside a box that was **collapsing anyway**, so names were clipped rather than wrapped.
The existing comment records the earlier half-fix.

It never showed on Groups I–IV because no code there carries enough aliases to overflow one row —
**the defect scaled with the alias count rather than existing from the start.** Fixed with
`flex: 0 0 auto`. All 28 now wrap legibly.

### 7.3 What the browser confirmed correct

| Path | Result |
|---|---|
| Guided entry → eye → **C69.2 Retina** → Group 5 | routes correctly; all nine C69 codes render, ligature fixed |
| Search `white pupil` / `squint` / `cat` / `bulging` | all resolve to Group 5 after the alias promotion; 28 chips, 0 duplicates |
| Imaging constellation confirmed | `9510` · basis 2 · workup complete · correct upgrade text |
| Enucleation G1 / diffuse / GX | `9511` / `9513` / `9510`, all basis 7, all workup complete |
| Retinocytoma, whole specimen | **"No code emitted here"**, `9510/0` shown as ICD-O only, registrar decision flagged, **no override button** |
| Mimic — detachment, no calcified mass | **"No code emitted. This case leaves the malignant registry."** Visser rule 4 cited |

The Group 4 override defect — *"Override this code"* offered on terminals that emit none — **does
not reproduce**. The fix made there is group-agnostic and holds.

---

## 8. What needs you

### ★ 1. `9514` is a selectable REDCap option the tool cannot emit

`v_morph` offers `9514 - Retinoblastoma, spontaneously regressed`. ICD-O-3.2 carries `9514` only at
`/1`; ICCC-3 Group V declares `3`. Withdraw the option, or rule that the registry registers a
regressed retinoblastoma and say on what code. **`v_morph` is the simplest block in the form** — it
stores the real code as the option value and has no `_code`/`_extended`/`_subgroup` companion, so
the repair is a label change with no formula or renumbering risk.
Full package: `docs/group_05_layer1_repair.md`.

### 2. Is a regressed retinoblastoma an incident case? Is a retinocytoma registrable at all?

A registration-rules question, not a morphology one. Retinocytoma is the parallel of Group 4's
ganglioneuroma (ruling D1). Note the divergence: **the World Health Organization calls retinocytoma
premalignant; ICD-O-3.2 codes it `9510/0`, benign.** The behaviour digit is IARC's and the tool
codes to ICD-O-3.2 — nobody should "fix" it — but the registry is being asked to hold a lesion the
two sources disagree about.

### 3. Do `9511`, `9512` and `9513` still carry a World Health Organization entity?

§3 above. **This is the ruling that most changes what the tree contains.** Needs the paywalled
entity page, or the International Collaboration on Cancer Reporting's *Ocular retinoblastoma*
dataset — in development in synchrony with the volume, consultation late 2026, publication first
half of 2027.

### 4. Did the retina chapter change between the 2023 beta and the January 2026 print?

Thirty-three months apart, no published comparison. Only IARC or the book can say.

### 5. Which intraocular classification does the pathway document mean by "Murphree 2005"?

The International **Intraocular** Retinoblastoma Classification (Murphree AL, *Ophthalmology Clinics
of North America* 2005;18(1):41–53, viii) or the International Classification of Retinoblastoma
(Shields, 2006)? They have different group E criteria. Changes no code; the pathway document needs
the correction.

### 6. Two cross-group alias defects, both outside this branch

- **`docs/TODO.md` §17** — every alias field except `alias` and `also_known_as` is unread by the
  engine, and **24 alias strings already resolve to two groups**, every one a dual-group term
  (`CLL`, `ATLL`, the B-lymphoblastic family, `medulloepithelioma`). `state.group = hit.groups[0]`
  takes the lower number without asking the discriminator.
- **`docs/TODO.md` §18** — `build_database.py` indexes the `alias` field alone, so
  `also_known_as` strings cannot be searched at all. **Fixed for Group 5, still open for I–IV
  (375 strings).** On the registrar's question — *why not just add them in `alias`?* — that is
  what the master instruction file Sec. 2 already prescribes for a **local term**, so 20 Group 5
  strings were promoted to primary entries (19 entries → 39): `white pupil`, `white eye`,
  `cat's-eye reflex`, `squint`, `crossed eye`, `protruding eye`, `bulging eye`, `eye tumor`,
  `intraocular mass` and eleven clinical variants. Zero new collisions; the *"Also called"* list
  is unchanged because `aliasesFor()` dedupes. **The other 375 are machine-harvested NCI Thesaurus
  synonyms, not curated local terms** — promoting those would duplicate every field 375 times, so
  the one-loop index fix remains the right answer there, after §17.

---

## 9. Divergences recorded, not acted on

- **`who_version` on `9511`/`9512`/`9513` reads `"ICD-O-3.2"`, not a WHO edition.** Deliberate and
  honest: no WHO edition confirms a separate entity on those stems (§3). `9510` reads `"WHO 2023"`.
- **A cytology is ENCR basis 5 and the closed `diagnostic_tests_required` vocabulary has no member
  for it.** The branch captures `"Cytology"` as a free-form evidence tag; the entries stay inside
  the closed list. A schema gap, not a Group 5 gap.
- **`"Moderate" anaplasia alone**, with no differentiation grade, is not covered by the contract's
  Mendoza bridge. Folded into the GX/`9510` default as the least-specific answer rather than
  guessed toward `9511` or `9512`; recorded in the node's `coding_note`.
- **Where a report states more than one grade, the higher governs** (registrar, 7 October 2026;
  contract §2.4). The first build coded from the differentiation grade and set anaplasia aside, so a
  G2 report with severe anaplasia recorded `9511`. Severe anaplasia now outranks G1 and G2 on
  `rb_enucleation_report`, and `rb_retinocytoma_word` has a `9512` option for a retinocytomatous area
  inside a tumour whose remainder is G3, G4 or severely anaplastic, and a second one for a stated diffuse
  growth pattern (`9513`). Moderate anaplasia stays as above. That it changes no code where a differentiation
  grade is stated rests on the 7 October decision alone, with no source: open for the registrar (TODO §30).
- **The alias express lane now records the site** (registrar, 7 October 2026). A typed Group V term
  used to complete a case with no topography (`TOPOGRAPHY —`), because the lane bypassed site capture
  for a group that reads no site. It now asks the organ system and region and only records the answer:
  "Retinoblastoma" at the retina records `C69.2`, and the group never changes. A file that does not
  state the site takes "The file does not state the site" and keeps the dash.
- **Two claims in an early draft of contract §9 were wrong and were corrected against the
  primaries**: chromosome 6p gain does **not** significantly correlate with extraocular spread
  (P = 0.07, a trend — *the paper's own title and conclusion overstate its results*), and
  aqueous-humour cell-free DNA is **not** confined to prognostication. The second correction is why
  this group has a cytology route at all.

---

*Group V — Retinoblastoma. Built 22 September 2026 following the Group 3 method
(`docs/group_baseline_documents.md`). Four codes, one tree, seven nodes, thirty-nine aliases,
seven validation rules, thirteen negative controls, 347 checks, 0 FAIL.*
