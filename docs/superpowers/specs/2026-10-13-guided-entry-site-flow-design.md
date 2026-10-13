# Guided entry: presentation wording, body system → organ, and the marrow question

Date: 13 October 2026. Status: design approved in conversation, awaiting written-spec review.
Branch: `claude/guided-entry-site-flow`, from `origin/main`. Separate from PR #15, because this changes the shared router that all twelve groups use.

## What the registrar asked for

1. The presentation labels name symptoms and findings in plain language. "Cytopenias" is a laboratory finding, not a presentation.
2. After the presentation, ask which **body system** the disease arises in, then which **organ** within it.
3. When the presentation already says blood or marrow, do not ask again. Marrow was established three times in one case: the presentation, the "primary compartment" question, and the organ-system screen, then again as a region.
4. "Primary compartment" is renamed "site of origin".
5. A child with ALL who presents with enlarged lymph nodes is still Group I. Choosing a lymph node must not take Group I away.

## The flow today and the flow after

| Step | Today | After |
|---|---|---|
| 1 | Presentation (7 labels) | Presentation, new wording |
| 2 | "Where is the disease centred?" marrow / nodes / other organ | Body system (15). Skipped when the presentation fixes the system, as blood and marrow does |
| 3 | "Which organ system?" (flat list of 48 crosswalk rows). For blood and marrow it is a one-option confirmation tap | Organ within the system. Skipped when the system has one organ |
| 4 | "Where in …?" (the ICD-O code list) | Unchanged, except its question for blood and marrow is reworded. Skipped when the organ has one code |
| 5 | none | "Is the bone marrow also involved?" Yes / No / Not known yet. Asked only when it can change the group (see below) |

The 48 crosswalk rows stay as they are. They become step 3. The new layer is step 2.

## 1. Presentation labels

Data only, in `data/shared/presentation_router.json` → `archetypes[].label`.

| archetype_id | New label |
|---|---|
| blood_marrow | Pale, bruising or bleeding, repeated infections or bone pain, with an abnormal blood count |
| solid_mass | A lump, mass or swelling |
| lymphadenopathy | Enlarged lymph nodes |
| organ_functional_sign | A symptom from an organ, such as a white pupil, a bulging eye, blood in the urine, jaundice or signs of raised pressure in the head |
| cutaneous_mucosal_lesion | A lesion, sore or growth on the skin or on a mucous surface |
| incidental_imaging_finding | An abnormal mass found by chance on a scan or X-ray |
| unsure | More than one of these, or not sure |

The old labels also appear in `README.md`, `docs/TODO.md`, `docs/validator_negative_controls.md`, `docs/group_10_registrar_review.md`, `docs/group_11_build_report.md` and `docs/group_11_evidence/cross_group_A.md`. The plan updates the ones that describe the live tool and leaves dated build reports alone.

## 2. Body systems

New block `site_systems` in `presentation_router.json`: an ordered list of `{system_id, label, organs: [coarse organ ids]}`. The grouping follows the ICD-O topography site blocks, with two deliberate departures: Lymph nodes is its own system (ICD-O files C77 under other and ill-defined sites), and Reproductive organs merges the female and male genital blocks (the ovary and testis row carries C56, C62 and C76.3 together).

| System | Organs (crosswalk ids) |
|---|---|
| Blood, bone marrow and haematopoietic system | blood_marrow_haematopoietic |
| Lymph nodes | lymph_node |
| Brain and central nervous system | brain_cns |
| Soft tissue and peripheral nerves | soft_tissue_peripheral_nerve, soft_tissue_connective, soft_tissue_retroperitoneum_peritoneum |
| Endocrine glands | adrenal_paraspinal, thyroid, pituitary, midline_cns_extension, head_neck_paraganglia, endocrine_other |
| Eye | eye |
| Head and neck | nasopharynx, nasal_cavity_middle_ear, accessory_sinuses, lip_oral_cavity, salivary_glands, tonsil_oropharynx_hypopharynx |
| Chest and airway | mediastinum, lung, thymus, larynx_trachea, heart_pleura_thorax |
| Digestive system | liver, biliary_extrahepatic, gallbladder, oesophagus, stomach, small_intestine, colon_appendix_rectum_anus, pancreas, digestive_other |
| Urinary system | kidney, urinary_bladder, urinary_tract_other |
| Reproductive organs | prostate, penis, male_genital_paratesticular, gonad_sacrococcygeal_midline, female_genital_lower, female_genital_upper, female_genital_adnexa |
| Bone and joints | bone |
| Skin | skin |
| Breast | breast |
| Ill-defined or unknown site | ill_defined_sites, unknown_primary |

The registrar ruled that the pituitary, craniopharyngeal duct (`midline_cns_extension`, C75.2 and C75.3) and pineal gland sit under Endocrine glands, as ICD-O has them.

Organ labels name what they bundle. "Major salivary glands" becomes "Salivary glands (parotid, submandibular, sublingual)". The plan reviews every bundled label the same way.

**Source limit.** The repository holds no ICD-O topography block headings: the ICD-O-3.2 workbook is morphology only. The system names are therefore authored, from the standard block structure. The build can prove each organ belongs to exactly one system. It cannot prove the names against a source file. If the registrar supplies the ICD-O-3.2 topography chapter, the plan adds that check.

**Build checks (new):**
- every crosswalk organ is in exactly one system;
- every organ id a system names exists;
- no system is empty;
- a system label is non-empty and unique.

## 3. Screens

- **System screen** replaces the first half of `renderSite`. It lists `site_systems`. When a tissue origin was declared, the systems that match it sort first, as the flat list does now. A system answers to the names of the organs and codes inside it, so searching "parotid" finds Head and neck.
- **Organ screen** lists the system's organs. When a system has one organ, the screen is skipped.
- **Region screen** (the code list) is `renderSiteRegion`. When the organ has one code, it is skipped (existing behaviour).
- **Presentation fixes the system.** `blood_marrow` already declares `auto_topography: "C42.x"` and `site_capture: false`. Those fields now skip the system screen as well, which is the existing "one tap confirms" screen removed. Blood and marrow's single organ then skips the organ screen. The region screen is the only site screen the clerk sees, and its crosswalk row carries a new optional `region_question`, "Which of these does the disease arise in?", in place of the repeated "Where in blood, bone marrow and haematopoietic system?".
- The search-led entry paths (`afterSearchSite`, `siteRecordOnly`, `recordGroup`) keep working through the same screens.

`app.js` stays group-agnostic: systems, organs, the skip rules and the question wording all come from the router and crosswalk JSON.

## 4. The marrow question

The routing fact behind it is real. The dual-group rules for 9811–9819, 9823 and 9827 read `primary_compartment`: marrow is Group I, anything else is Group II, and marrow blasts ≥25% override it for 9811–9819. Today the compartment is asked before the site, and its answer shields Group I from the site narrowing. If the site were asked first with no other change, a lymph node would remove Group I, because the lymph node row lists Groups II and IX only.

**Design.**
- The discriminator `primary_compartment` becomes a three-answer question, "Is the bone marrow also involved?", with answers `marrow` (Yes), `not_marrow` (No) and `not_known` (Not known yet). Nodal and extranodal merge. In all three rules above they route identically, because the extranodal answer falls to the same default as nodal. The rules' nodal and extranodal branches become one `not_marrow` branch.
- **Yes** sets `marrow`, drops Group II, and carries `keep_on_site: [1]` so the site cannot remove Group I.
- **No** sets `not_marrow` and drops Group I.
- **Not known yet** sets `not_known`, drops nothing, and carries `keep_on_site: [1]`. Both Groups I and II stay offered, and the "which family?" question decides. It exists because a clerk holding a blood count or a nodal biopsy often has no marrow result yet, and a blood count cannot answer the question: no rule in the router or in any group's data uses one to choose between Groups I and II. The marrow rules read the marrow blast percentage. The one place a count separates the groups is inside a single code (chronic lymphocytic leukaemia against small lymphocytic lymphoma, 9823).
- **What the rules do with `not_known`.** The three dual-group rules fall to Group II when no branch matches, so a case answered "Not known yet" and then filed under Group I could be sent to Group II when its morphology is reached. The plan first reads how `dual_group_rules` are evaluated once the clerk has chosen a group, and then gives each of the three rules an explicit `not_known` branch that keeps the clerk's chosen group. A new build check requires every rule that reads `primary_compartment` to carry a branch for all three answers. If a rule cannot honour the chosen group, the plan stops and returns to the registrar.
- **Auto-answer.** When the chosen code is C42.0, C42.1, C42.3 or C42.4, the compartment is `marrow` and the question is not shown. That list is the one the `9811-9819` rule already carries. A build check requires the discriminator's list to equal it, so there is one truth. The spleen (C42.2) is the only C42 code that is asked.
- **When it is asked.** The discriminator declares an `ask_when` condition in the router: Group I is among the presentation's candidates before the site narrows them, and the chosen site's own candidate list includes Group II. The engine reads the declaration and holds no group numbers. Examples: a kidney tumour never sees it (the kidney lists Group VI only); a lymph node or the thyroid under "enlarged lymph nodes" or "not sure" does.
- The question is asked after the site, so it sits between the region step and the group decision. `ask_before_site` is dropped from this discriminator.

**Build check (new).** No `dual_group_rules` branch may read `nodal` or `extranodal`. This stops a future rule from depending on a distinction the question no longer draws.

## 5. Trail

- The trail shows an answer's label, not its stored value ("Blood and bone marrow", not "marrow"). This is a bug today and applies to every discriminator.
- Trail headings: **Site of origin** for the body-system answer, **Organ** for the organ answer, **Topography** for the code (unchanged), **Bone marrow also involved** for the marrow question. This is my reading of "rename primary compartment to site of origin": the old compartment question no longer exists in its old form, and "site of origin" now names the system and organ it was standing in for. The registrar may correct it on review.

## 6. Verification

- Engine gate (`build/check_engine_flow.mjs`), new cases:
  - Lymph node, "Not known yet": Groups I and II are both offered at the family question, and a Group I choice is not sent to Group II afterwards.
  - ALL with enlarged nodes: pick the lymph node, answer Yes, end in Group I.
  - The same case, answer No: Group II.
  - Lymphoma in a node, with no marrow involvement: Group II.
  - Kidney tumour: the marrow question is never asked.
  - Spleen: asked.
  - Blood and marrow presentation: no system, organ or marrow question shown, and the compartment is `marrow`.
  - A search-led entry still reaches its group.
  - Marrow blasts ≥25% with answer No: the plan first reads when `marrow_blast_percentage` is captured relative to the group decision, then pins the result to today's behaviour. The old nodal answer dropped Group I in the same place, so the test records what happens now and does not promise a change.
- **Routing unchanged.** For every group, the router's group outputs are identical before and after for every case that does not involve the compartment. The plan states the comparison method.
- Negative controls for each new build check, run in memory against the real check: an organ in two systems, an organ in none, an unknown organ id, an empty system, a duplicate label, a discriminator auto-answer list that differs from the 9811-9819 rule, a rule branch reading `nodal`, a rule that reads `primary_compartment` with no `not_known` branch.
- The in-app browser: drive the blood and marrow path and the lymph node path through the real page, and check the trail text.

## Not in this change

- Group-level evidence gates and marker screens (PR #15).
- The C71.0 (cerebrum) gap: the lookup has a row for it but the REDCap list has no code 710. This predates the work and is the registrar's ruling.
- Reordering the presentation list.
- Topography codes, the lookup rows and ICD-O data are unchanged. Only router JSON, the crosswalk's `label` and `region_question` fields, `app.js` and its CSS change.

## Open for review

1. The trail headings in section 5.
2. Whether the plan should add the ICD-O-3.2 topography-chapter check if a source file exists.
