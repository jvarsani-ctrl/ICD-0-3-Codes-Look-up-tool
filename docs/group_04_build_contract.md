# Group 4 build contract — Neuroblastoma and Other Peripheral Nervous Cell Tumours

**2026-09-16.** The single spec every Group 4 build task works from. It exists for the same reason
the Group 3 contract did: four trees, a shared-layer change, a router change and an alias file are
authored in parallel and must agree on the schema before any of them is written.

**Authority, in order:**

1. `ICD coding/ICD-O-3.2/icdo32.sqlite` (IARC FINAL workbook, 9 Oct 2020) and
   `ICCC-2017.sqlite` — Layer 1. Code identity, term strings, behaviour, subgroup, topography.
2. `ICD Look Up tool/Group 4 — Neuroblastoma Diagnostic Pathway.md` — the clinical source of
   truth, **with the corrections in §0 below applied.**
3. `ICD Look Up tool/Decision tree JSON Build — Master Instruction File.md` — the base schema.
4. `ICD Look Up tool/memory/*.md` — locked decisions. `registrar-rulings.md` binds.
5. `ICD-Lookup/docs/group_03_build_contract.md` — the method. Group 4 follows it.
6. This file — where 1–5 need reconciling for Group 4, the reconciliation is written here.

---

## 0. What the pathway document gets wrong, and why it cannot be followed unamended

The pathway was written 2026-05-26 and last revised 2026-06-02 — **before Groups 2 and 3 were
built.** Six of its statements are now false. Each was checked against the two databases on
2026-09-16.

### 0.1 The eight "schema challenges" are four solved problems and four non-problems

The pathway's closing section lists eight structural issues, four of them marked schema-breaking
or needing a new node type. **All four were solved by the Group 3 build. Do not re-solve them,
do not propose new node types, and do not amend the engine for any of them.**

| Pathway challenge | Status on 2026-09-16 |
|---|---|
| #1 IHC confirms type, not code | **Solved.** `histology_subclassification` is in `NODE_TYPES` (`build/build_database.py` line 48) and in `app.js` line 27. Group 3 authors 22 of them. |
| #2 `imaging_pathway` needs a biochemical component | **Solved.** `biochemical_questions[]` is live on `imaging_pathway` (`app.js` line 1010, validator line 4812). Group 3's `pf_imaging_no_tissue` uses it for AFP and β-hCG. |
| #3 No histology sub-classification node type | **Solved.** Same as #1. |
| #4 PCC/PGL codes are site-resolved | **Solved.** `site_resolution` is in `NODE_TYPES` and in `app.js`. Group 3 authors 7 of them. |
| #5 Flat NOS fallback | Correct, and unchanged. |
| #6 Cross-group routing for 9503 | **Wrong in its conclusion.** See §2.4. |
| #7 Germline genetics ≠ somatic cytogenetics | Correct. Resolution: `molecular_freetext`, and the result does not change the code. No new node type. |
| #8 SDHB IHC is a screening trigger | Correct, but `clinical_alert` is **banned** — registrar ruling 9. See §4.1. |

**The closed node-type vocabulary is unchanged by this group.** Group 4 adds no node type. Like
Groups 1, 2 and 3 before it, anything it needs that does not exist is a *field*, and §3 says there
is only one.

### 0.2 8683 Gangliocytic paraganglioma is not a usable Group IV code

ICD-O-3.2 carries `8683` **only at behaviour /0** — `Gangliocytic paraganglioma`, code reference
`(C17.0)`, duodenum. ICCC-3 declares behaviour **`3` and nothing else** for every Group IV range.
There is no `8683/3`, so there is no Group IV entry for it. It drops out exactly as the sixteen
absent codes dropped out of Group 3.

**The WHO classification agrees, independently.** Mete O, et al. *Overview of the 2022 WHO
Classification of Paragangliomas and Pheochromocytomas.* Endocrine Pathology 2022;33(1):90–114,
PMID 35285002, abstract: *"in the 2022 WHO classification, ... the lesion known as gangliocytic
paraganglioma has been renamed composite gangliocytoma/neuroma and neuroendocrine tumor
(CoGNET)."* WHO 2022 does not retain gangliocytic paraganglioma as a paraganglioma at all — it
walks the entity out of the family. So both legs of the two-source test say the same thing: the
behaviour is wrong in ICD-O-3.2 for this group, and no current WHO paraganglioma entity lives on
the stem. **`8683` is removed on the full test, not the weak one.**

It appears in `RedCap Options/Group 4- ….md` and in the pathway's Tree B coding table. Both are
wrong. **8683 appears nowhere in `group_04_dt.json`, in no alias target, and in no example.**
It is an alias *input* only, resolving to a terminal that says why it cannot be coded here: the
entity is now CoGNET, and the registrar assigns its code.

> Only the abstract of Mete 2022 was retrievable — no PMCID, not open access. The quotation above
> is from the abstract and carries no page number. Whether WHO 2022 states an ICD-O code for
> CoGNET is **unknown** and needs the full text.

### 0.3 The ICD-O-3.2 preferred terms are not the REDCap option strings

Four divergences, all verified:

| Code | ICD-O-3.2 preferred term (authoritative) | REDCap option string (alias input only) |
|---|---|---|
| `8690/3` | `Middle ear paraganglioma` | `Glomus jugulare tumor, NOS` — ICD-O-3.2 carries this as a **Synonym** |
| `8692/3` | `Carotid body paraganglioma` | `Carotid body tumor` — ICD-O-3.2 carries this as a **Synonym** |
| `9490/3` | `Ganglioneuroblastoma` | lists `Ganglioneuroma` as a separate option — that is `9490/0`, see §2.1 |
| `9502/3` | `Teratoid medulloepithelioma, NOS` | `Teratoid medulloepithelioma` — no `, NOS` |

### 0.4 `Paraganglioma, benign` and `Pheochromocytoma, malignant` do not exist

ICD-O-3.2 carries `8680` and `8700` **at /3 only**. The REDCap option file's benign and malignant
variants are ICD-O-3.1 legacy strings. The pathway's note on this is correct in substance; the
consequence it does not draw is that the *names* change too — `Paraganglioma, NOS` and
`Pheochromocytoma, NOS` are the only terms the tool may emit on those stems.

### 0.5 9520, 9521 and 9523 are separate codes, not synonyms of 9522

The pathway calls them "older synonyms". ICD-O-3.2 prints each as its **own Preferred term on its
own stem**, none marked `[obs]`:

| Code | Preferred term | Synonym ICD-O-3.2 also carries |
|---|---|---|
| `9520/3` | `Olfactory neurogenic tumor` | — |
| `9521/3` | `Olfactory neurocytoma` | `Esthesioneurocytoma` |
| `9522/3` | `Olfactory neuroblastoma` `(C30.0)` | `Esthesioneuroblastoma` `(C30.0)` |
| `9523/3` | `Olfactory neuroepithelioma` | `Esthesioneuroepithelioma` |

Whether a current WHO entity lives on 9520, 9521 and 9523 is **decision D3 in §6**. The test is
the Group 3 test, not "the pathway called it a synonym".

### 0.6 Group IV's topography is every site, and 9490 / 9500 include the CNS

ICCC-3 gives `C00.0–C80.9` to every Group IV range except `9501`–`9504`. That means
`9500/3` at `C71.x` — which ICD-O-3.2 calls `Central neuroblastoma` and `CNS neuroblastoma`, both
Synonyms on `9500/3` — is **ICCC-3 Group IVa, not Group III**. Group III does not claim 9500 or
9490. There is no conflict to resolve; there is a routing note to write, because it reads wrong.

---

## 1. The inventory is generated, never transcribed

`build/generate_group04_inventory.py` joins `ICCC-2017.sqlite` to `icdo32.sqlite` and emits every
`(code, behaviour)` Group IV can carry. Run it; build `morphology_entries[]` from its output.

Verified output, 2026-09-16:

| | |
|---|---|
| ICCC-3 code-range entries | 19 |
| Distinct codes | 19 |
| Absent from ICD-O-3.2 **at a declared behaviour** | **1** — `8683` (exists at /0 only; §0.2) |
| Usable codes | **18** |
| `(code, behaviour)` records | **18** — no code appears twice |
| **`morphology_entries[]` target** | **18** |
| Behaviour declaration | `3` — exactly one, across every Group IV range |

The full table, with subgroup and topography scope:

| Code | Beh | Subgroup | ICD-O-3.2 preferred term | ICCC-3 topography scope |
|---|---|---|---|---|
| 8680 | 3 | IVb | Paraganglioma, NOS | C00.0–C80.9 |
| 8681 | 3 | IVb | Sympathetic paraganglioma | C00.0–C80.9 |
| 8682 | 3 | IVb | Parasympathetic paraganglioma | C00.0–C80.9 |
| 8690 | 3 | IVb | Middle ear paraganglioma | C00.0–C80.9 |
| 8691 | 3 | IVb | Aortic body tumor | C00.0–C80.9 |
| 8692 | 3 | IVb | Carotid body paraganglioma | C00.0–C80.9 |
| 8693 | 3 | IVb | Extra-adrenal paraganglioma, NOS | C00.0–C80.9 |
| 8700 | 3 | IVb | Pheochromocytoma, NOS | C00.0–C80.9 |
| 9490 | 3 | IVa | Ganglioneuroblastoma | C00.0–C80.9 |
| 9500 | 3 | IVa | Neuroblastoma, NOS | C00.0–C80.9 |
| 9501 | 3 | IVb | Medulloepithelioma, NOS | C00.0–C69.9, C73.9–C76.8, C80.9 |
| 9502 | 3 | IVb | Teratoid medulloepithelioma, NOS | C00.0–C69.9, C73.9–C76.8, C80.9 |
| 9503 | 3 | IVb | Neuroepithelioma, NOS | C00.0–C69.9, C73.9–C76.8, C80.9 |
| 9504 | 3 | IVb | Spongioneuroblastoma | C00.0–C69.9, C73.9–C76.8, C80.9 |
| 9520 | 3 | IVb | Olfactory neurogenic tumor | C00.0–C80.9 |
| 9521 | 3 | IVb | Olfactory neurocytoma | C00.0–C80.9 |
| 9522 | 3 | IVb | Olfactory neuroblastoma | C00.0–C80.9 |
| 9523 | 3 | IVb | Olfactory neuroepithelioma | C00.0–C80.9 |

**Note the asymmetry.** ICCC-3 admits `9501`–`9504` in Group IV only *outside* C70–C72, and gives
them to Group III (`IIIc3`, behaviour `0-1,3`) inside it. Everything else in Group IV is admitted
at every site, including the CNS.

### 1.1 Layer 1 for this group is ICD-O-3.2, not the REDCap option file

The same rule Group 3 adopted (contract §1.1a, §5.2), for the same reason and with the same
consequences. `icdo32.sqlite` is authoritative for code identity, term strings and behaviour;
`ICCC-2017.sqlite` for subgroup, topography constraint and behaviour range.

- Every `(morphology_code, morphology_name, behavior_code)` triple the engine can emit must exist
  **verbatim** in `icdo32.sqlite`. The four divergences of §0.3 resolve in ICD-O-3.2's favour.
- The REDCap option strings become **alias inputs**, checked the other way: every alias resolves
  to a valid triple, and **no alias may be emitted**.
- Groups 1 and 2 keep their current `check_redcap_exact_names` behaviour. This must not regress
  them.

### 1.2 No behaviour-overloaded codes

Group IV declares behaviour `3` only, so there is exactly one entry per code and
`check_duplicate_code_behavior_pairs` has nothing to catch. Four codes carry a /0 term in
ICD-O-3.2 that Group IV does not admit — `9490/0 Ganglioneuroma`, `9501/0 Medulloepithelioma,
benign`, `9502/0 Teratoid medulloepithelioma, benign`, and `8683/0` (§0.2). **None is authored.**
The Group 3 precedent governs: `8000/6` and `8000/9` were left unauthored because a case carrying
them leaves the group silently. See §2.1 for what the tree says instead.

---

## 2. The five code decisions this group forces

### 2.1 `9490/0 Ganglioneuroma` — out of group, and the tree must say so

A ganglioneuroma is the fully matured, benign end of the neuroblastic spectrum. ICD-O-3.2 codes it
`9490/0`. ICCC-3 Group IV admits behaviour `3` only, so **a ganglioneuroma is not a registrable
Group IV cancer.** It shares its four-digit stem with ganglioneuroblastoma, which is the trap: a
tree that resolves "Schwannian stroma-dominant, fully mature" to `9490` without carrying the
behaviour emits `9490/3 Ganglioneuroblastoma` for a benign tumour.

**Required:** the `histology_subclassification` node that separates the INPC categories carries a
distinct option for *ganglioneuroma, maturing or mature* whose destination is a terminal that
emits **no Group IV code**, states that the lesion is benign and falls outside the group's
behaviour declaration, and refers the decision to the registrar. `Ganglioneuroma` is an alias
input resolving to that terminal. This is decision **D1** in §6.

### 2.2 `8683` — §0.2. Not built.

### 2.3 `9504 Spongioneuroblastoma` — built, unreachable

ICD-O-3.2 prints `Spongioneuroblastoma` on `9504/3` **without** `[obs]`, so the Group 3 test
(*a code leaves the decision tree only when no current WHO entity lives on its stem*) does not
remove it on the `[obs]` ground. But no current WHO entity lives on it either: the term is a 1948
artefact with no modern diagnostic criteria.

**Required, following the Group 3 precedent for its thirteen `obsolete_term` entries:** `9504/3`
is authored in `morphology_entries[]`, flagged, and **reachable from no tree**. It exists so that
an alias on the string can explain itself, and so a historical record carrying the code resolves.
This is decision **D2** in §6.

### 2.4 `9503 Neuroepithelioma, NOS` — and where "peripheral PNET" actually goes

**The pathway and the alias instructions both send "peripheral PNET" to 9503. ICD-O-3.2 sends it
to 9364.** Verified 2026-09-16:

```
9364/3  Preferred  Ewing sarcoma
9364/3  Synonym    Peripheral neuroectodermal tumor
9364/3  Synonym    PPNET
9364/3  Related    Peripheral primitive neuroectodermal tumor
9364/3  Related    Neuroectodermal tumor, NOS
9365/3  Preferred  Askin tumor
9503/3  Preferred  Neuroepithelioma, NOS          <- and nothing else
9260/0  Preferred  Aneurysmal bone cyst           <- 9260/3 Ewing sarcoma no longer exists
```

So ICD-O-3.2 has already made the call the pathway describes as pending: **peripheral PNET,
pPNET and peripheral neuroectodermal tumour are Ewing sarcoma, `9364/3`** — Group VIII at bone,
Group IX at soft tissue. `9503/3 Neuroepithelioma, NOS` keeps its own stem and carries no synonym.

Consequences:
- Alias-instruction entries **30, 31 and 33** (`Peripheral primitive neuroectodermal tumor`,
  `pPNET`, `Peripheral PNET` → `9503`) are **wrong** and must map to `9364` with a cross-group
  referral, not to `9503`.
- Entry 29 (`Neuroepithelioma` → `9503`) stands.
- `9503/3` stays in Group IV at peripheral sites, with a `topography_routing_note` that says what
  ICD-O-3.2 did, not what the 2026-06 pathway guessed.
- **Out of scope and flagged, not fixed here:** `presentation_router.json`'s `9260` dual-group rule
  still routes a code that ICD-O-3.2 no longer carries at /3. That is a Group VIII/IX defect.
  Record it in `docs/TODO.md`; do not touch it in this build.

This is decision **D4** in §6.

### 2.5 The router's `9501-9504` rule is stale and currently misroutes CNS cases

`presentation_router.json → dual_group_rules → "9501-9504"` matches only `C70.9`, `C71.9` and
`C72.9`, and carries its own note: *"Extend both files together when Group III is authored."*
**Group III was authored on 2026-09-16.** As it stands, a medulloepithelioma at `C71.6` falls
through the rule and routes to Group IV, which is wrong — ICCC-3 gives `9501`–`9504` to Group III
across the whole of `C70.0–C72.9`.

**Required:** extend the rule's `topography_in` to every code in `C70.0–C72.9` that
`topography_codes.json` enumerates (all 21 are already present), and delete the obsolete scope
note. No ruling needed — this is the fix the note itself asked for.

---

## 3. The one new field: `behaviour_exclusion`

Group 1 added six fields, Group 2 five, Group 3 seven. **Group 4 adds one**, and it is forced by
§2.1: the schema has no way to say *"this histological entity exists, has an ICD-O code, and that
code's behaviour falls outside the group's declaration, so no Group IV code may be emitted."*

Without it the only options are to emit `9490/3` for a benign tumour, or to route the option to a
`refer_group` terminal — but there is no group to refer to, because ICCC-3 does not register
benign neurogenic tumours anywhere.

On a branch or a terminal:

```json
"behaviour_exclusion": {
  "icdo_code": "9490",
  "icdo_behaviour": "0",
  "icdo_term": "Ganglioneuroma",
  "group_declares": "3",
  "reason": "A fully matured ganglioneuroma is benign. ICD-O-3.2 codes it 9490/0. ICCC-3 Group IV admits behaviour 3 only, so it is not a registrable cancer in this group and no Group IV code is emitted for it.",
  "registrar_decision_required": true
}
```

Rules:
- All six keys required. `icdo_code`, `icdo_behaviour` and `icdo_term` must round-trip against
  `icdo32.sqlite` — the term must be the **Preferred** term at that `(code, behaviour)`.
- `icdo_behaviour` must **not** be in the group's declaration. A `behaviour_exclusion` naming an
  admitted behaviour is a build error — it would hide a code that should have been emitted.
- A branch carrying `behaviour_exclusion` emits **no** `morphology_code`. Carrying both is a
  build error.
- `reason` is **clerk-facing** and is rendered. It is not a `coding_note`.

**Group 4 only.** The engine supports it; no other group is obliged to adopt it. Groups 5–12 will
meet the same problem (Group 6's benign renal tumours, Group 9's benign soft-tissue tumours) and
may adopt it then, on their own evidence.

---

## 4. Rules inherited unchanged from Groups 1–3

### 4.1 No clinical alerts. `clinical_alert` is `null` everywhere.

Registrar ruling 9 of 4 Sep 2026. `check_no_clinical_alerts` FAILs the build on any text. This
group generates a lot of pressure to break it — hypertensive crisis in an untreated
pheochromocytoma, the 80% germline fraction in paediatric PCC/PGL, SDHB loss implying family
screening. **All of it goes to `docs/clinical-warnings.md` under a Group IV heading**, in the
format the existing entries use, with the exact place it came from.

Where an alert carries information the clerk **must act on to code correctly**, that information
goes in `question`, `hint`, or the branch's own `label` or `reason` — never in `coding_note`,
which is author-facing and is not displayed.

### 4.2 `basis_of_diagnosis` — and the two Visser rows this group owns

ENCR, per `docs/references/visser-2023-key-points.md`. Valid set `{0,1,2,4,5,7,8,9}`; codes 3 and
6 do not exist; 0 and 9 override; computed as the highest of 1–8. Declared on the tree object:
`"ihc_counts_as": 7`, `"methylation_counts_as": 8`.

**Visser Table 4 (p. 06) names two Group IV entities directly.** These are the only two specific
morphology codes this group may assign with no pathology at all:

| Entity | Marker | Morphology | Basis |
|---|---|---|---|
| Neuroblastoma | homovanillic acid, vanillylmandelic acid | `9500/3` | **4** |
| Phaeochromocytoma | catecholamines, chromogranin A | `8700/3` | **4** |

Three consequences the build must honour:

1. **The imaging-sufficient neuroblastoma terminal emits basis 4, not 2.** The pathway's Stage-2C
   constellation is a Table 4 row, not a Table 3 row.
2. **Rule 6, p. 05 — basis 4 never stands alone.** The marker must accompany a clinical diagnosis
   or a clinical investigation showing cancer. So the `imaging_pathway` node requires *both* the
   imaging constellation *and* the biochemistry; neither alone resolves. This is what
   `biochemical_questions[]` is for.
3. **Rule 5, p. 03 — everything else without pathology is `8000/3`.** No olfactory neuroblastoma,
   no paraganglioma, no ganglioneuroblastoma may be coded to its specific code on imaging alone.
   And `8000` at a Group IV topography is **not a Group IV code** — it routes to Group XII under
   the existing `8000-8005` dual-group rule. Those branches are `refer_group: 12` terminals, and
   the reason must say why plainly.

> ⚠️ **Divergence to record, not to act on.** Visser's own table puts phaeochromocytoma in
> *Group XI*. ICCC-2017 puts `8700` in **IVb**. ICCC-2017 is Layer 1 and governs. Note it in the
> build report; do not change the routing.

### 4.3 `check_satisfies_tests`, `check_refer_terminals`, `check_flow_charts`

All three already run and all three bite. In particular:
- `satisfies_tests` values come from the closed vocabulary and must appear in the terminal code's
  own `diagnostic_tests_required`. It suppresses an outstanding-workup row, so it is the one field
  that can make a case look better evidenced than it is.
- Clerk-facing text on a `refer_group` terminal goes in `reason`, never `coding_note`.
- Every `ihc_checklist` carries a `branch_sequence` induced by `build/induce_flow.py`, and every
  rule needs a witness. Rerun `induce_flow.py` after editing any `resolution_logic`.

### 4.4 `nos_fallback` by node type

Non-null for `ihc_checklist`, `cytogenetics_dropdown`, `molecular_freetext`, `numeric_gate`.
**Null** for `document_inventory`, `clinical_alias`, `morphology_only`, `imaging_pathway`,
`histology_subclassification`, `site_resolution`.

The group's NOS chains are flat, as the pathway correctly says: `9500` for the neuroblastic tree,
`8680` for the paraganglionic trees, `9522` for the sinonasal tree. All three exist in
`morphology_entries[]`, so `check_fallback_chains` is satisfied trivially. **No code falls back to
a code on its own stem** — the Group 3 `8000/0 → 8000/1` self-reference failure cannot recur here
because there are no behaviour-overloaded codes.

### 4.5 No `resource_level_gate` unless a site profile justifies it

Group 3's corrected rule (contract §2(2)): **unavailability follows from a declared site profile,
never from the required level.** With no site profile the honest output is *not established*, not
*unavailable*. The flag `upgrade_line_says_unavailable` is banned and the build FAILs on it.

Group 4's temptation is `¹⁸F-FDOPA` and `⁶⁸Ga-DOTATATE` PET, which most laboratories cannot run.
That is not a reason to gate: it is a reason for the node to ask which functional imaging was
actually done, and to carry the answer. The tool is global, not built around one kind of
laboratory.

---

## 5. Tree architecture — four trees, keyed by site

`metadata.decision_trees` lists all four. Each begins at its own `document_inventory`. Node IDs
are tree-prefixed and globally unique across the file.

Site is the key, for the same reason compartment was the key in Group 3: **the router has already
captured it at Stage 1, so the tree is chosen without asking the clerk anything extra.** The three
tumour families of Group 4 are biologically distinct and separate cleanly on topography, with one
real overlap — the adrenal gland, where neuroblastoma and pheochromocytoma both live — which is
resolved inside `g4_sympathoadrenal` by age and catecholamine profile, not by a site question.

| `tree_id` | Prefix | Topography it owns | Codes it can emit | Dominant differential |
|---|---|---|---|---|
| `g4_sympathoadrenal` | `sa_` | C74.0, C74.1, C74.9, C47.x, C48.0, C48.2, C48.8, C38.1–C38.3 | 9500, 9490, 8700, 8681, 8693, 8680 | Neuroblastoma · ganglioneuroblastoma · ganglioneuroma · pheochromocytoma · extra-adrenal sympathetic paraganglioma |
| `g4_head_neck_paraganglia` | `hn_` | C75.4, C75.5, C30.1, C10.x, C32.x, C77.0 | 8692, 8690, 8691, 8682, 8693, 8680 | Carotid body · jugulotympanic · vagal · laryngeal paraganglioma |
| `g4_sinonasal` | `sn_` | C30.0, C31.x, C11.x | 9522, and 9520/9521/9523 subject to **D3** | Olfactory neuroblastoma · sinonasal small round cell differential |
| `g4_other_peripheral` | `op_` | everything else Group IV can carry, including C80.9 | 9501, 9502, 9503, 9504, 8680, 9500 | Medulloepithelioma · neuroepithelioma at peripheral sites; the unestablished-site terminus |

**The map must be total and disjoint over every topography Group IV can carry, and that is a
validation rule.** Group IV's scope is `C00.0–C80.9` for fourteen of its eighteen codes, so
`g4_other_peripheral` is the catch-all — the analogue of `g3_unspecified` — and it is reachable
from every tree as the terminal for an inadequate specimen or an unestablished site. The sweep
must confirm every enumerated topography resolves to exactly one tree, and that no code is
emittable from a tree whose topography scope excludes it (`9501`–`9504` must be unreachable from
any node whose captured topography is in `C70.0–C72.9` — those belong to Group III).

### 5.1 The adrenal overlap is the group's one hard differential

`g4_sympathoadrenal` must separate neuroblastoma from pheochromocytoma at the same organ. The
separators, in the order the file will state them:

- **Age.** Neuroblastoma: 90% under 5. Paediatric pheochromocytoma: rare under 10.
- **Catecholamine profile.** Neuroblastoma: urinary VMA and HVA (Visser Table 4). Pheochromocytoma:
  plasma free metanephrines or 24-hour urinary fractionated metanephrines.
- **IHC.** Both are PHOX2B+, synaptophysin+, chromogranin+. **PHOX2B does not separate them.**
  What separates them is `GATA3` (pheochromocytoma/paraganglioma positive), the zellballen
  architecture with S100/SOX10-positive sustentacular cells, and the neuroblastic Schwannian
  stroma assessment.
- **Cytokeratin is negative in both** and separates neither. It separates both from a
  well-differentiated neuroendocrine tumour.

A branch that claims PHOX2B distinguishes neuroblastoma from pheochromocytoma is a build error
and must be caught by review, not by the validator — the validator cannot know.

---

## 6. The registrar's rulings, 16 September 2026

All six were put to the registrar with their evidence on 16 September 2026 and all six are ruled.
**They bind. A build task that finds one of them inconvenient escalates; it does not reinterpret.**

### D1 — A ganglioneuroma gets no Group IV code. `behaviour_exclusion` is ratified.

The new field of §3 is approved and built. The branch that resolves *Schwannian stroma-dominant,
maturing or mature* emits **no** `morphology_code`; it states that the lesion is benign, sits at
`9490/0 Ganglioneuroma` in ICD-O-3.2, and falls outside ICCC-3 Group IV's `3`-only behaviour
declaration. Precedent: `8000/6` and `8000/9` were left unauthored in Group 3 for the same reason.
Groups 6 and 9 will meet the same problem; they may adopt the field on their own evidence.

### D2 — `9504 Spongioneuroblastoma` is built, flagged, and reachable from no tree.

Not `[obs]` in ICD-O-3.2, so the Group 3 test does not remove it; but no current WHO entity lives
on the stem, so no branch may reach it. Precedent: Group 3's thirteen `obsolete_term` entries.

### D3 — All four olfactory codes are built. Only `9522` is resolvable.

`9520`, `9521` and `9523` are live Preferred terms in ICD-O-3.2 with no `[obs]`, so the Group 3
test retains them. The literature does not settle whether a current WHO entity lives on any of
them — Veyrat 2020 and Pfister 2022 are both silent (§10). So:

- A tree may **resolve to `9522` only.**
- `9520`, `9521` and `9523` are reachable **solely** when the pathology report uses that exact
  string, through a `clinical_alias` branch, at `confidence_ceiling: "low"`, carrying a
  `coding_note` that records that no current WHO entity has been confirmed on the stem.
- Settling it properly needs WHO *Head and Neck Tumours*, 5th edition, which this registry does
  not hold. Recorded in §10.1.

### D4 — "pPNET" and its synonyms alias to `9364`, with a cross-group referral.

**Verified from the source workbooks on 16 September 2026, at the registrar's instruction**, not
from the SQLite conversion, and checked across both the 2019 draft and the 9 October 2020 final so
that a conversion artefact or a draft-stage edit could be excluded. Both agree:

```
9260/0  Preferred  Aneurysmal bone cyst      <- 9260/3 Ewing sarcoma does not exist in ICD-O-3.2
9364/3  Preferred  Ewing sarcoma
9364/3  Synonym    Ewing tumor                   (final only; absent from the 2019 draft)
9364/3  Synonym    Peripheral neuroectodermal tumor
9364/3  Synonym    PPNET
9364/3  Related    Peripheral primitive neuroectodermal tumor
9364/3  Related    Neuroectodermal tumor, NOS
9365/3  Preferred  Askin tumor
9473/3  Synonym    Primitive neuroectodermal tumor, NOS   <- the CNS one, Group III
9473/3  Synonym    PNET, NOS
9473/3  Related    Central primitive neuroectodermal tumor   (C71._)
9473/3  Related    Supratentorial PNET                       (C71._)
9503/3  Preferred  Neuroepithelioma, NOS     <- its only term, in both versions. No PNET synonym.
```

So: `Peripheral primitive neuroectodermal tumor`, `Peripheral neuroectodermal tumor` and `PPNET`
alias to **`9364`** and **refer out** — Group VIII at bone, Group IX at soft tissue. This
**overrides alias-instruction entries 30, 31 and 33.** `Neuroepithelioma` alone (entry 29) stays
on `9503`.

Note the third row of that table: `PNET, NOS` and `Primitive neuroectodermal tumor, NOS` without
"peripheral" are **`9473/3`, Group III**, not `9364` and not `9503`. An alias on the unqualified
string must not be authored in Group IV.

### D5 — `morphology_name` is keyed to ICD-O-3.2, not to the REDCap option file.

§1.1 stands as written. Every emittable `(morphology_code, morphology_name, behavior_code)` triple
must exist verbatim in `icdo32.sqlite`; the four divergences of §0.3 resolve in ICD-O-3.2's
favour; the REDCap strings become alias inputs. Groups 1 and 2 keep their current
`check_redcap_exact_names` behaviour unchanged. This supersedes `Cancer Registry/CLAUDE.md` §5 for
Group 4, exactly as it was superseded for Group 3, under the latest-document-wins rule.

### D6 — "Peripheral neuroepithelioma" goes to `9503`, and the branch asks what the IHC shows.

The verification for D4 turned up a question that had been folded into it. **The exact phrase
"peripheral neuroepithelioma" appears nowhere in ICD-O-3.2** — not as a term, a synonym, a
see-also, an inclusion or an exclusion. Layer 1 is silent on it. `9503/3 Neuroepithelioma, NOS` is
its only plausible home, and nothing in Layer 1 says so.

Ruled: **alias to `9503`, and route to a branch that asks one question of the file rather than
guessing from a word.**

```
CD99 positive, with PHOX2B negative and synaptophysin negative?
  yes -> Ewing-family tumour. refer_group 8 (bone) or 9 (soft tissue), code 9364.
  no, or not done -> 9503/3 Neuroepithelioma, NOS, confidence_ceiling "low",
                     with an outstanding-workup row naming CD99, PHOX2B and synaptophysin.
```

This decides on evidence the file already holds instead of on the wording of a report, and it is
the branch that keeps the pathway document's stated failure mode from happening. `reason` is
clerk-facing; the ICD-O-3.2 reasoning goes in `coding_note`.

---

## 7. Shared-layer changes this build requires

### 7.1 `topography_codes.json` is missing every site this group needs

It enumerates 68 codes. **None of the following is present, and Group 4 cannot be routed without
them:**

| Code | Label | Why Group 4 needs it |
|---|---|---|
| `C30.0` | Nasal cavity | ICD-O-3.2 prints `(C30.0)` against `9522/3` itself. Without it the sinonasal tree has no topography. |
| `C30.1` | Middle ear | `8690 Middle ear paraganglioma` — the code's own name. |
| `C31.0`–`C31.9` | Paranasal sinuses | Kadish B and C olfactory neuroblastoma. |
| `C75.4` | Carotid body | `8692 Carotid body paraganglioma`. |
| `C75.5` | Aortic body and other paraganglia | `8691 Aortic body tumor`, `8693`. |
| `C38.1`–`C38.3` | Mediastinum | Posterior mediastinal neuroblastoma — a common presentation. |
| `C11.0`–`C11.9` | Nasopharynx | Sinonasal differential. |

Each needs `code`, `label`, `redcap_code`, `coarse_organ`, `candidate_groups`, matching the
existing 68. `redcap_code` must be taken from `ICD coding/RedCap Options/Topography Redcap.md` —
**never invented.** Where that file has no entry, say so and stop; do not guess.

`coarse_organ_crosswalk` needs the matching organ rows. `adrenal_paraspinal` (C74) already exists
with `candidate_groups: [4]`.

### 7.2 `presentation_router.json`

- `groups["4"]` — `built: true`, four trees, entry nodes, `handoff`, `tree_selection`.
- `dual_group_rules["9501-9504"]` — extend as §2.5.
- `archetypes` — `solid_mass` and `organ_functional_sign` already list group 4 as a candidate.
  The sinonasal presentation (unilateral nasal obstruction, epistaxis, anosmia) fits
  `organ_functional_sign`; confirm it routes there rather than adding an archetype.

---

## 8. Validation rules this group adds

Each gets a **negative control**: break the data deliberately, confirm the check FAILs, restore,
confirm it passes. Record them in `docs/validator_negative_controls.md` in the existing format.

1. **`behaviour_exclusion` shape** — all six keys; `icdo_code`/`icdo_behaviour`/`icdo_term`
   round-trip to the **Preferred** term in `icdo32.sqlite`; `icdo_behaviour` is **not** in the
   group's declaration; no `morphology_code` on the same branch; `reason` non-empty.
2. **Behaviour declaration.** Every Group IV `morphology_entries[]` object carries
   `behavior_code: "3"`. Any other value is a build error.
3. **`8683` appears nowhere** — not as a `morphology_code`, not as an alias target, not in an
   example. Alias *input* is permitted.
4. **`9504` is unreachable** — no `next_node`, `resolution_logic` result, branch or terminal
   anywhere in `group_04_dt.json` emits `9504`.
5. **Topography map total and disjoint** over every topography Group IV can carry (§5), and
   `9501`–`9504` unreachable from any node whose captured topography is in `C70.0–C72.9`.
6. **Visser Table 4 gate.** A terminal with `no_tissue: true` may emit a specific morphology code
   **only** if that code is `9500/3` or `8700/3` and it carries `basis_of_diagnosis: 4` and a
   non-empty `biochemical_questions[]` on the reaching `imaging_pathway`. Every other `no_tissue`
   terminal emits `refer_group: 12` (`8000/3`). Basis 4 never stands alone.
7. **ICD-O-3.2 round-trip** (§1.1) — every emittable
   `(morphology_code, morphology_name, behavior_code)` triple exists verbatim in `icdo32.sqlite`.
   Groups 1 and 2 keep their current behaviour.
8. **`9364` is not a Group IV code.** The pPNET aliases (D4) resolve through a cross-group
   referral; `9364` must not appear in `morphology_entries[]`.
9. **Negative controls** for all of the above.

---

## 9. Build order

Parts are built **in full** before anything is validated. Validating between trees on Group 1
produced 132, then 88, then 4 failures that were all "a later tree does not exist yet" and cleared
on their own.

1. `build/generate_group04_inventory.py` — and the `topography_codes.json` extension (§7.1).
2. This contract — done.
3. `morphology_entries[]` — all 18, one pass.
4. Engine + validator support for `behaviour_exclusion`, and the nine checks of §8.
5. The four trees.
6. Router registration (§7.2).
7. `aliases_group_04.json` — with D4 applied.
8. Docs — clinical warnings, negative controls, build report, `TODO.md` entry for the `9260`
   router defect.
9. **Then verify once:** `induce_flow.py` → `build_database.py` → negative controls → drive the
   tool in a browser.

**A green build is not a working tool.** Group 2 passed 74 checks, 10 of 10 data-level traversals
and 102 engine assertions while 15 of its 61 nodes did not render at all. Every automated layer
tested the data or the renderer in isolation; the fault was in the seam between them. Step 9's
browser pass is not optional.

---

## 10. The baseline document, and what this group is built on

**Group IV's assigned baseline is Pfister SM, et al. *A Summary of the Inaugural WHO Classification
of Pediatric Tumors: Transitioning from the Optical into the Molecular Era.* Cancer Discovery
2022;12(2):331–355. PMID 34921008 · PMC9401511.** It was retrieved in full on 16 September 2026
and is held at `Group 4 Papers/Pfister-2022-who-pediatric-tumors-summary.md`.

**It does not serve as a baseline, and the build does not pretend otherwise.** Read, it is a
chapter-by-chapter tour of the WHO Paediatric Tumours volume rather than the pathology text. Its
whole treatment of peripheral neuroblastic tumours is one paragraph noting that neuroblastoma is
the most common solid tumour in children, deferring the classification and molecular detail to a
**Supplementary Table S3 that could not be retrieved**. Ganglioneuroblastoma and ganglioneuroma
are never named. Paraganglioma and pheochromocytoma are never mentioned. *Medulloepithelioma*
never appears, and *neuroepithelial* appears only in CNS contexts. **No ICD-O code is stated
anywhere in the paper.**

That is the finding the registrar's ruling of 16 September 2026 anticipated: *"This group has
scanty research. There are no definitive papers that set baseline. Let's go with what we have."*
The build proceeds on that ruling, and this section is what "what we have" actually amounts to,
stated plainly so no reader mistakes it for more.

| Family | Evidence held | Strength |
|---|---|---|
| Neuroblastic (9490, 9500) | Shimada 1999 · Peuchmaur 2003 · Okamatsu 2009 · Ambros 2005 · Ma 2021 · Verly 2017 · Monclair 2009 · Ambros 2009 · Nakagawara 2018 — all on disk | **Strong, and stronger than the nominal baseline.** The INPC (Shimada, Peuchmaur) and the INRG (Monclair, Ambros) are international consensus documents covering exactly what a coder needs: the four INPC categories, the Schwannian-stroma criterion that separates 9490 from 9500, the age-linked favourable/unfavourable assignment, and the staging system. This family is better evidenced than Group III's was. |
| Paraganglionic (8680–8700) | Manethova 2023 · Maignan 2017 · Bausch 2017 · Testa 2013 · Di Stasio 2022 on disk. **Mete 2022 retrieved 16 Sep 2026 — abstract only.** | **Medium.** The IHC panel is well sourced and Mete's abstract corroborates it (INSM1, synaptophysin, chromogranins; GATA3, tyrosine hydroxylase, dopamine β-hydroxylase, phenylethanolamine *N*-methyltransferase; SOX10/S100 sustentacular; keratins negative). Two things the abstract settles: **CoGNET** (§0.2), and that pheochromocytoma is *"used specifically for intra-adrenal paragangliomas"*. One thing it unsettles: it attributes the abolition of the benign/malignant split to **the 4th edition**, not the 5th. The full entity list is not confirmed from source. |
| Olfactory (9520–9523) | Manethova 2023 for the negative PHOX2B finding. **Veyrat 2020 retrieved 16 Sep 2026 — abstract only.** | **Weak.** Veyrat confirms that Kadish (clinical-radiological) and Hyams (histological) are the two systems and that Kadish C–D and Hyams III–IV mark poor prognosis, but **reproduces neither set of criteria** and is silent on 9520, 9521 and 9523. It is also a chapter in the Karger monograph series *Advances in Oto-Rhino-Laryngology* vol. 84, pp. 154–167 — not the standalone journal review the pathway's reference list implies. The Hyams and Kadish tables in the pathway document are from recall and are **not** source-verified. Decision **D3** is therefore unresolved by literature and is settled on the ICD-O-3.2 test alone. |
| Medulloepithelioma / neuroepithelioma at peripheral sites (9501–9504) | Shuangshoti 1986 — one case report | **Very weak, and honestly so.** Pfister 2022 does not discuss peripheral medulloepithelioma or neuroepithelioma at all. No pathway is built. §2.3, §2.4. |

### 10.1 What is still missing, recorded rather than glossed

1. **Pfister 2022 Supplementary Table S3** — the only place the baseline states its neuroblastic
   entity list. Not retrievable through the full-text tool.
2. **Mete 2022 full text** — needed for the WHO 2022 paraganglioma entity list, for any ICD-O code
   WHO states for CoGNET, and for what the paper says about neuroblastic tumours (its abstract
   claims it summarises them).
3. **Veyrat 2020 full text** — the actual Kadish A–D and Hyams I–IV criteria. Until it is held, the
   sinonasal tree must not present grading criteria as sourced.
4. **WHO Head and Neck Tumours, 5th edition** — the only document that can settle **D3**.
5. **The exact WHO edition that abolished the paraganglioma benign/malignant split.** Mete's
   abstract says the 4th. Immaterial to the coding (ICD-O-3.2 carries /3 only either way), but the
   build report must not assert 2022 when the source says 2017.

Items 2 and 3 are behind paywalls with no PMCID. They need an institutional route, not another
PubMed attempt.

### 10.2 The rule this section exists to enforce

Where the evidence is weak the tool says **less**, not the same amount with less warrant. A
`confidence_ceiling` of `low`, an outstanding-workup row and a `provisional_pending` are all
cheaper than a coded diagnosis the file does not support. The sinonasal and peripheral-medullo­
epithelioma branches are where this group will be tempted to overstate, and they are the branches
review must look at first.

---

*Written 16 September 2026, following `docs/group_03_build_contract.md` and the method recorded in
`docs/group_baseline_documents.md`.*
