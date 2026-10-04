# Group 9 checks — negative controls

Evidence that the ten Group 9 rules in `build/build_database.py` catch what they claim to, and
stay silent on correct data. Method per `memory/data.md` §5A and Group 6 contract §8.1: break the
data and watch the rule FAIL for the right reason, then write a plausible correct variant and
watch it stay quiet.

**Pinned:** the data under test is `data/database/group_09_dt.json` as committed at `a46d52c`,
before any fix arising from these controls. Each control mutates an in-memory copy and calls the
rule function directly; nothing on disk changes. The harness is `build/group09_negative_controls.py`:

```
python3 build/group09_negative_controls.py .
```

## Results, 2 October 2026

```
Group 9 negative controls against data/database/group_09_dt.json (HEAD a46d52c)

ok   baseline, unmodified                                                   check_group9_code_set                  expect OK  
        RULE 1 — all 82 entries and 98 tree emission(s) are in the generated 82-code Group IX inventory
ok   baseline, unmodified                                                   check_group9_absent_codes              expect OK  
        RULE 2 — none of 9260, 9150, 9366, 9367, 9368, 8859 is emitted, referred to or used as a fallback
ok   baseline, unmodified                                                   check_group9_ewing_code                expect OK  
        RULE 3 — 4 code-emitting branch(es) naming Ewing sarcoma or a Ewing-like family carry the right code
ok   baseline, unmodified                                                   check_group9_basis_rows                expect OK  
        RULE 4 — 5 basis-1/basis-2 branch(es), each a Visser Table 3 row
ok   baseline, unmodified                                                   check_group9_kaposi_hhv8               expect OK  
        RULE 5 — 5 branch(es) emit 9140; none records HHV-8 negative on the same branch, and every marker rule requires HHV-8 LANA-1 positive
ok   baseline, unmodified                                                   check_group9_8963_site                 expect OK  
        RULE 6 — 1 8963 emission(s), each a SMARCB1-loss rule after the CNS, kidney and liver referrals
ok   baseline, unmodified                                                   check_group9_no_imaging_sufficient     expect OK  
        RULE 7 — no imaging_sufficient entry and no imaging_pathway node
ok   baseline, unmodified                                                   check_group9_no_flow_cytometry         expect OK  
        RULE 8 — no Flow cytometry in any Group IX test list
ok   baseline, unmodified                                                   check_group9_obs_unreachable           expect OK  
        RULE 9 — neither 9560 nor 8853 is emitted by the tree
ok   baseline, unmodified                                                   check_group9_leaf_claims               expect OK  
        RULE 10 — 60 leaf claims and 22 direct-entry claims all match the tree
ok   1a fabricated code 8919 emitted                                        check_group9_code_set                  expect FAIL
        RULE 1 — node st_rms (options[0]) emits 8919, which is not a Group IX code (contract §0.3)
ok   1b entry deleted                                                       check_group9_code_set                  expect FAIL
        RULE 1 — 1 generated Group IX code(s) have no morphology_entries[] object: 8710
ok   1c entry behaviour changed to /1                                       check_group9_code_set                  expect FAIL
        RULE 1 — morphology_entries[3] carries 8800/1, which is not one of the 82 (code, behaviour) records build/generate_group_inventory.py --group IX generates (contract §0.3)
ok   2a Ewing option emits retired 9260                                     check_group9_absent_codes              expect FAIL
        RULE 2 — decision_trees[0].nodes[9].options[0].morphology_code is 9260, a number this group must never emit (contract §0.5, §0.6)
ok   2b refer_code 9150                                                     check_group9_absent_codes              expect FAIL
        RULE 2 — decision_trees[0].nodes[3].options[4].refer_code is 9150, a number this group must never emit (contract §0.5, §0.6)
ok   2c nos_fallback 9367                                                   check_group9_absent_codes              expect FAIL
        RULE 2 — decision_trees[0].nodes[10].nos_fallback.code is 9367, a number this group must never emit (contract §0.5, §0.6)
ok   2p PROBE: 9260 named in a reason (prose) is not a FAIL                 check_group9_absent_codes              expect OK  
        RULE 2 — none of 9260, 9150, 9366, 9367, 9368, 8859 is emitted, referred to or used as a fallback
ok   3a Ewing option emits 8803                                             check_group9_ewing_code                expect FAIL
        RULE 3 — st_round_cell (options[0]) names Ewing sarcoma and emits 8803. Ewing sarcoma is 9364/3 in ICD-O-3.2 (contract §0.5)
ok   3b CIC option emits 9364                                               check_group9_ewing_code                expect FAIL
        RULE 3 — st_round_cell (options[3]) names a Ewing-like sarcoma and emits 9364. WHO 2020 Table XII separates it from Ewing sarcoma; it codes 8803/3 (contract §3.2)
ok   3c BCOR option emits 9364                                              check_group9_ewing_code                expect FAIL
        RULE 3 — st_round_cell (options[4]) names a Ewing-like sarcoma and emits 9364. WHO 2020 Table XII separates it from Ewing sarcoma; it codes 8803/3 (contract §3.2)
ok   3p PROBE: 'Ewing-like' label emitting 8803 is not a FAIL               check_group9_ewing_code                expect OK  
        RULE 3 — 4 code-emitting branch(es) naming Ewing sarcoma or a Ewing-like family carry the right code
ok   4a cutaneous KS basis 1 without skin capture                           check_group9_basis_rows                expect FAIL
        RULE 4 — decision_trees[0].nodes[1].options[0] emits 9140 at basis 1 without capturing lesion_site 'skin'. Visser Table 3 gives basis 1 only to Kaposi sarcoma of the skin, C44 (contract §0.7)
ok   4b basis 1 on 8800                                                     check_group9_basis_rows                expect FAIL
        RULE 4 — decision_trees[0].nodes[2].options[0] emits 8800 at basis 1. Visser Table 3 gives basis 1 only to Kaposi sarcoma of the skin, C44 (contract §0.7)
ok   4c basis 2 on 8910 (no Visser row)                                     check_group9_basis_rows                expect FAIL
        RULE 4 — decision_trees[0].nodes[6].options[0] emits 8910 at basis 2. Visser Table 3's soft tissue rows at basis 2 are 8800, 8850, 8890 and 9120 only (contract §0.7)
ok   4d basis 2 on a next_node branch                                       check_group9_basis_rows                expect FAIL
        RULE 4 — decision_trees[0].nodes[4].options[0] asserts basis 2 but emits no code
ok   4p PROBE: basis 2 on 9120 (a Visser row) is not a FAIL                 check_group9_basis_rows                expect OK  
        RULE 4 — 6 basis-1/basis-2 branch(es), each a Visser Table 3 row
ok   5a KS option records HHV-8 negative                                    check_group9_kaposi_hhv8               expect FAIL
        RULE 5 — st_vascular (options[1]) records HHV-8 negative and emits 9140
ok   5b KS marker rule keyed on the wrong marker                            check_group9_kaposi_hhv8               expect FAIL
        RULE 5 — st_spindle_ihc (resolution_logic[1]) is a marker rule emitting 9140 without HHV-8 LANA-1 positive
ok   5c KS marker rule with HHV-8 required negative                         check_group9_kaposi_hhv8               expect FAIL
        RULE 5 — st_spindle_ihc (resolution_logic[1]) emits 9140 with HHV-8 LANA-1 required negative
ok   5p PROBE: KS 'as stated' after a negative stain (captured upstream) is not a FAIL check_group9_kaposi_hhv8               expect OK  
        RULE 5 — 5 branch(es) emit 9140; none records HHV-8 negative on the same branch, and every marker rule requires HHV-8 LANA-1 positive
ok   6a CNS referral rule removed                                           check_group9_8963_site                 expect FAIL
        RULE 6 — st_epithelioid_ihc: the 8963 rule is not preceded by a SMARCB1-loss rule referring the CNS to Group 3 (missing C70.0, C70.1, C70.9, C71.0, C71.1)
ok   6b CNS referral at NOS level only                                      check_group9_8963_site                 expect FAIL
        RULE 6 — st_epithelioid_ihc: the 8963 rule is not preceded by a SMARCB1-loss rule referring the CNS to Group 3 (missing C70.0, C70.1, C71.0, C71.1, C71.2)
ok   6c kidney referral after the 8963 rule                                 check_group9_8963_site                 expect FAIL
        RULE 6 — st_epithelioid_ihc: the 8963 rule is not preceded by a SMARCB1-loss rule referring C64.9 to Group 6 (missing C64.9)
ok   6d named rhabdoid option emits 8963 directly                           check_group9_8963_site                 expect FAIL
        RULE 6 — st_uncertain (options[3]) emits 8963 outside an ihc_checklist rule; a rhabdoid tumour must pass the SMARCB1 (INI1) site fork (contract §3.6)
ok   6e 8963 rule without SMARCB1 loss                                      check_group9_8963_site                 expect FAIL
        RULE 6 — st_epithelioid_ihc (resolution_logic[3]) emits 8963 without SMARCB1 (INI1) loss
ok   7a 8800 imaging_sufficient                                             check_group9_no_imaging_sufficient     expect FAIL
        RULE 7 — 8800 is imaging_sufficient
ok   7b imaging_pathway node                                                check_group9_no_imaging_sufficient     expect FAIL
        RULE 7 — st_imaging_report is an imaging_pathway node
ok   8a Flow cytometry in an entry                                          check_group9_no_flow_cytometry         expect FAIL
        RULE 8 — morphology_entries[0].diagnostic_tests_required names Flow cytometry
ok   8b Flow cytometry in satisfies_tests                                   check_group9_no_flow_cytometry         expect FAIL
        RULE 8 — decision_trees[0].nodes[13].options[0].satisfies_tests names Flow cytometry
ok   9a tree emits 9560                                                     check_group9_obs_unreachable           expect FAIL
        RULE 9 — st_nerve_sheath (options[4]) emits 9560, whose every behaviour-3 term is [obs]
ok   9b tree emits 8853                                                     check_group9_obs_unreachable           expect FAIL
        RULE 9 — st_adipocytic (options[0]) emits 8853, whose every behaviour-3 term is [obs]
ok   10a leaf claimed, never emitted (9042 option recoded)                  check_group9_leaf_claims               expect FAIL
        RULE 10 — 9042 claims a tree leaf, but no branch or fallback emits it
ok   10b direct-only code emitted (8991)                                    check_group9_leaf_claims               expect FAIL
        RULE 10 — 8902 claims a tree leaf, but no branch or fallback emits it
        RULE 10 — 8991 claims direct code entry only, but the tree emits it
ok   10c coding_note claims both                                            check_group9_leaf_claims               expect FAIL
        RULE 10 — 8710's coding_note states neither or both of 'Reached by the g9_soft_tissue tree' and 'direct code entry only'

44 control(s), 0 not behaving as expected
```

Every baseline reports OK against real content, not an empty NOTE: rule 6 sees its `8963`
emission, rule 10 sees 60 leaf claims and 22 direct-entry claims.

## The probes that matter most

- **2p** — `9260` named in a `reason` is not a FAIL. Rule 2 bans the number as an emitted,
  referred or fallback code; prose saying "not 9260" is how a reason explains the change.
- **3p** — a label reading "Ewing-like" that emits `8803` is not a FAIL. The Ewing pattern
  excludes "Ewing-like"; without that exclusion the correct coding of every Ewing-like family fails.
- **5p** — the unmodified tree passes rule 5 although `st_kaposi_hhv8_negative` emits `9140` after
  a negative stain. That is the one deliberate route, where the pathologist still concludes Kaposi
  sarcoma, and it is why the rule is branch-local (contract §3.5).

One message was corrected after the first run: control 4b (basis 1 on `8800`) reported a missing
skin capture, when the defect is the code. The rule now names the code alone in that case.

## Three controls on the changes to generic checks

Same day, same method.

| Control | Result |
|---|---|
| Round trip, baseline | OK — 169/169 (code, name, behaviour) triples exist verbatim in `icdo32.sqlite` |
| Round trip, `8825/3` renamed to REDCap's label *Myofibroblastoma* | FAIL — the triple `(8825, 'Myofibroblastoma', 3)` does not exist in ICD-O-3.2 |
| Exact-string check on Group 9 | NOTE — steps aside for `check_icdo32_round_trip()`, as for Groups 3, 4 and 6 |
| CNS completeness, baseline | OK — 3 of 3 NOS-level CNS branches name all 21 codes |
| CNS completeness, the old `9473` rule restored in a scratch copy | **FAIL** — names 3 of 21 CNS codes and falls to Group 9 |

The last row is why the exemption had to go with the rule. With `9473` still named, restoring the
defective rule would have been downgraded to a WARN and the build would have passed.

## Added 4 October 2026 — RULE 3 reads marker rules

`check_group9_ewing_code` read only branch labels, so the `st_round_cell_ihc` rule that emits
`9364` was never checked (code review, 4 October 2026). It now holds a marker rule emitting `9364`
to NKX2.2 positive with no CIC, BCOR or non-ETS marker, the partner Group 8 rule 3 requires for
bone. Two controls were added to `build/group09_negative_controls.py`, run against the working
tree on the merged branch (`96beb55` plus the uncommitted review fixes; neither touches the
`9364` rule):

```
ok   3d 9364 marker rule on a CIC-rearranged profile (WT1, ETV4)            check_group9_ewing_code                expect FAIL
        RULE 3 — st_round_cell_ihc (resolution_logic[6]) emits 9364 on ['WT1', 'ETV4']; a marker rule for Ewing sarcoma requires NKX2.2 positive and no CIC, BCOR or non-ETS marker (contract §0.5, §3.2)
ok   3e 9364 marker rule on CD99 alone                                      check_group9_ewing_code                expect FAIL
        RULE 3 — st_round_cell_ihc (resolution_logic[6]) emits 9364 on ['CD99']; a marker rule for Ewing sarcoma requires NKX2.2 positive and no CIC, BCOR or non-ETS marker (contract §0.5, §3.2)

46 control(s), 0 not behaving as expected
```

On the unmodified data RULE 3 now counts five branches, the four labelled options and the marker
rule, and reports OK.

## Added 4 October 2026 — RULE 6 reads a scalar topography

`check_group9_8963_site` built its covered-site set with `set(when.topography)`, which turns a
string such as `"C64.9"` into a set of characters. The engine accepts a scalar `when` value
(`whenValueOk`), so a kidney referral written that way worked in the tool and failed the check.
The check now treats a scalar as a one-item list, and finds the 8963 rule's position by identity
instead of `list.index()`, which returned the first equal rule. Probe `6p` writes the kidney
referral as a string:

```
before the fix:  FAIL  RULE 6 — st_epithelioid_ihc: the 8963 rule is not preceded by a SMARCB1-loss rule referring C64.9 to Group 6
after the fix:   ok   6p PROBE: kidney referral with a scalar topography (engine form) is not a FAIL
                         RULE 6 — 1 8963 emission(s), each a SMARCB1-loss rule after the CNS, kidney and liver referrals

47 control(s), 0 not behaving as expected
```

Controls `6a`–`6e` still fail for the reasons recorded above.
