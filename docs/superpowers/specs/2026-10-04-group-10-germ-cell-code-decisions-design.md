# Group 10 — germ cell, trophoblastic and gonadal tumours: code decisions

**Written 4 October 2026, before any JSON was authored, while the registrar was away.** The
registrar asked for the build to continue and for every undecided point to be written down for
review. Each decision below states the evidence, the default the build carries, and its status.
The registrar's questions are collected in `docs/group_10_registrar_review.md`. The build plan is
`docs/group_10_build_contract.md`.

Status words: **settled** means ICD-O-3.2 or ICCC-2017 decides it and the build follows; 
**provisional** means a default was chosen between defensible readings and the registrar
confirms it; **deviation** means the build departs from the Group 10 Diagnostic Pathway
(14 July 2026) under a registrar ruling.

## Sources

| Need | Source | Held |
|---|---|---|
| Codes and behaviours | `icdo32.sqlite`, IARC ICD-O-3.2 final, 9 October 2020 | Layer 1 |
| What ICD-O-3.2 changed | IARC *New codes and their terms*; *Terms that are changing behaviour*, 9 October 2020 | Layer 1, `ICD-O-3.2/` |
| Group membership and behaviour per site | `ICCC-2017.sqlite`, ranges 94–117 | vault root |
| Testis entities with ICD-O codes | Moch H, et al. European Urology 2022;82(5):458–468, Table 3, pp. 464–465 | `Group 6 Papers/` |
| Central nervous system germ cell entities | Louis DN, et al. Neuro-Oncology 2021;23(8):1231–1251, Table 1, p. 1235 | `Group 3 Papers/`; `data/shared/who_cns5_table1.json` |
| Paediatric entities at every site | Pfister SM, et al. Cancer Discovery 2022;12(2):331–355, Table 3, p. 342; text pp. 340–343 | `Group 4 Papers/331.pdf` |
| Registration without tissue | Visser O, et al. Frontiers in Oncology 2023;13:1250549, rules 4–6 (pp. 03, 05), Table 4 (p. 06) | `docs/references/` |
| Ovary | Höhn AK, et al. Geburtshilfe und Frauenheilkunde 2021;81(10):1145–1153 | **does not cover the ovary** — see D22 |

---

## D1. Germinoma is `9064/3` — settled

ICD-O-3.2 prints *Germinoma* as the preferred term of `9064/3`, and *Dysgerminoma* as the
preferred term of `9060/3`. The Diagnostic Pathway (§1, §8 item 11) and the Alias Build
Instructions (lines 23, 117, 231, 369) map central nervous system germinoma to `9060`. ICD-O-3.2
decides currency (ruling 5), and the latest document wins (ruling 7). A tumour reported as
germinoma, at any site, is `9064/3`.

## D2. "Germ cell tumour, not otherwise specified" is `9064/3` — provisional

ICD-O-3.2 lists *Germ cell tumor, NOS* as a synonym of `9064/3`. Visser 2023 Table 4 (p. 06)
codes a germ cell tumour diagnosed on human chorionic gonadotropin to `9064/3`. The pathway's
fallback, `9065/3`, is *Germ cell tumor, nonseminomatous*: it asserts a non-seminomatous
tumour and contradicts a germinoma.

**Built:** a germ cell tumour whose type the report does not name is `9064/3`, and every
germ cell `ihc_checklist` falls back to `9064/3`. The output names the code by its preferred
term, *Germinoma*. The branch `reason` states that ICD-O-3.2 files *Germ cell tumor, NOS* under
the same number, so the screen does not claim a germinoma was diagnosed.

## D3. The germinoma family is coded by the term the report uses — provisional

Moch 2022 (p. 464) treats dysgerminoma, seminoma and germinoma as one tumour. ICD-O-3.2 keeps
three numbers. **Built:** dysgerminoma `9060/3`, seminoma `9061/3`, anaplastic seminoma
`9062/3`, spermatocytic tumour `9063/3`, germinoma `9064/3`, coded as the report writes them.
Each site tree offers the terms that site's reports use (ovary: dysgerminoma and germinoma;
testis: the three seminoma terms; central nervous system: germinoma; other sites: germinoma and
seminoma), and search reaches the rest. Where
an immunohistochemistry panel identifies the family without a name, the tree uses the name the
site customarily carries: ovary `9060/3`, testis `9061/3`, central nervous system and other
sites `9064/3`.

## D4. Registration without tissue follows Visser 2023 Table 4 — provisional

Visser 2023 Table 4 (p. 06): germ cell tumour with human chorionic gonadotropin → `9064/3`;
germ cell tumour with alpha-fetoprotein, with or without human chorionic gonadotropin →
`9065/3`; choriocarcinoma of the placenta with human chorionic gonadotropin → `9100/3`. Basis
of diagnosis 4. Rule 6 (p. 05): basis 4 never stands alone — a clinical investigation must show
the tumour. Rule 5 (p. 03): no germ cell row exists in Table 3, so imaging alone is `8000/3`.
Rule 4 (p. 03): "possible" is not registrable.

**Built, in every site tree:** imaging that shows a tumour **and** a marker the report calls
raised → `9065/3` (alpha-fetoprotein raised) or `9064/3` (human chorionic gonadotropin raised,
alpha-fetoprotein not raised), basis 4. The extragonadal tree adds `9100/3` at basis 4 for a
uterine or placental tumour with raised human chorionic gonadotropin after a pregnancy. A marker
with no imaging is not registrable. Imaging alone is `8000/3` at basis 2: in the gonadal trees
this is Group X (D13); in the central nervous system tree ICCC-2017 places it in Group III
(IIIf), so the branch refers to Group III; in the extragonadal tree it refers to Group XII.

**Deviation from the pathway (§2C, §6).** The pathway coded a marker-defined tumour by its
dominant marker: alpha-fetoprotein → yolk sac tumour `9071/3`, very high human chorionic
gonadotropin → choriocarcinoma `9100/3`, both → mixed `9085/3`. Visser Table 4 gives the
registry standard, and it does not name a histotype from a marker. Building the pathway's
mapping would record a histology no one saw.

**What "raised" means.** The tree reads the report's own statement against the laboratory's
reference range for the patient's age. It does not re-gate numerically. Group III's
`md_gct_*` numeric gates (Takami 2022 cut-offs) stay in Group III and are not copied. A newborn's
alpha-fetoprotein is physiologically high; the hint says the report must call it raised for the
patient's age.

## D5. Teratoma — settled except where marked

| Report says | Code | Source |
|---|---|---|
| Immature teratoma | `9080/3` | ICD-O-3.2 synonym *Immature teratoma, NOS* |
| Immature teratoma of the lung, thymus or thyroid | `9080/1` | *Terms that are changing behaviour*, p. 6 — provisional for the thymus, see below |
| Mature teratoma | `9080/0` | ICD-O-3.2 synonym *Mature teratoma, NOS* |
| Teratoma, type not stated | `9080/1` | ICD-O-3.2 preferred *Teratoma, NOS* |
| Dermoid cyst | `9084/0` | ICD-O-3.2 preferred |
| Teratoma, prepubertal type (testis); dermoid or epidermoid cyst of the testis | `9084/0` | ICD-O-3.2 related term; Moch 2022 Table 3, p. 465 |
| Teratoma, postpubertal type | `9080/3` | Moch 2022 Table 3, p. 464 |
| Teratoma with somatic-type malignancy | `9084/3` | ICD-O-3.2 synonym; Louis 2021 Table 1 |
| Struma ovarii, benign | `9090/0` | ICD-O-3.2 |
| Struma ovarii, malignant | `9090/3` | ICD-O-3.2; ICCC-2017 range 107 (Xc2, ovary and testis). Struma ovarii is ovarian, so only the ovary tree offers it |
| Strumal carcinoid | `9091/1` | ICD-O-3.2 has no `9091/3` |

**Where the behaviour digit is reportable.** ICCC-2017 ranges 94–99 (Xa, central nervous
system) declare behaviours `0-1,3`; ranges 100–117 declare `3`. So `9080/0`, `9080/1` and
`9084/0` are Group X codes in the central nervous system tree and behaviour exclusions in every
other tree. `9090/0` and `9091/1` are exclusions.

**Deviation from the pathway (§1, §4C).** The pathway codes immature teratoma `9083`. ICD-O-3.2
gives `9083/3` the British term *Malignant teratoma, intermediate*. Immature teratoma is `9080/3`.

**The thymus.** ICD-O-3.2 makes immature teratoma of the thymus (C37.9) `9080/1`. A mediastinal
immature teratoma recorded at C38.1 is `9080/3` by the same rule. The extragonadal tree asks the
site as the report writes it. Registrar to confirm.

## D6. Mixed tumours and the British terms are coded by ICD-O-3.2 term — provisional

| Report says | Code |
|---|---|
| Mixed germ cell tumour, components listed or not | `9085/3` |
| Choriocarcinoma is one of the components | `9101/3` *Choriocarcinoma combined with other germ cell elements* |
| Embryonal carcinoma and teratoma, and nothing else | `9081/3` (synonym *Mixed embryonal carcinoma and teratoma*) |
| Teratocarcinoma | `9081/3` |
| Malignant teratoma, undifferentiated (anaplastic) | `9082/3` |
| Malignant teratoma, intermediate | `9083/3` |
| Malignant teratoma, trophoblastic | `9102/3` — ovary and testis only (ICCC-2017 range 110) |
| Teratoma and seminoma | `9085/3` (related term *Mixed teratoma and seminoma*) |
| Mixed teratoma and yolk sac tumour, prepubertal type | `9085/3` (Moch 2022 Table 3) |
| Germ cell tumour with an associated haematological malignancy | `9086/3`, extragonadal tree only (ICCC-2017 range 105) |

WHO 2022 (Moch Table 3) codes every mixture `9085/3`. ICD-O-3.2 keeps the specific terms, and
the Group 8 build codes a subtype term as written to ICD-O-3.2's specific code (Group 8 D8).

## D7. Polyembryoma is `9072/3` — provisional

Moch 2022 Table 3 prints polyembryoma at `9085/3`. ICD-O-3.2 prints `9072/3`. ICD-O-3.2 governs.

## D8. Trophoblastic tumours — settled except `9104`

Choriocarcinoma `9100/3`; epithelioid trophoblastic tumour `9105/3`. Complete hydatidiform mole
`9100/0`, partial mole `9103/0` and invasive mole `9100/1` are behaviour exclusions outside the
central nervous system. **Placental site trophoblastic tumour** is `9104/1` in ICD-O-3.2; Moch
2022 Table 3 prints `9104/3` with the footnote "approved by the IARC/WHO Committee for ICD-O at
its meeting in February 2022", after ICD-O-3.2. **Built:** behaviour exclusion `9104/1`,
registrar decision required — the Group 8 `9222` pattern.

`9100/0` and `9100/1` are inside ICCC-2017 range 98 (Xa5, behaviours `0-1,3`). No central
nervous system entity lives at either behaviour: Louis 2021 Table 1 lists choriocarcinoma and
no mole. Both entries stay in the inventory and off the tree.

The pathway's p57 and genotyping algorithm (§4D) separates complete mole, partial mole and
non-molar pregnancy. Every outcome is a behaviour exclusion, so the algorithm changes no
registered code. It is not built.

## D9. Germ cell neoplasia in situ is a behaviour exclusion — settled

`9064/2`. Xa declares `0-1,3` and Xc declares `3`. Moch 2022 Table 3 prints intratubular forms
at `9061/2`, `9070/2`, `9071/2` and `9080/2`; ICD-O-3.2 has none of the four, so they are not
built and a report of any of them is the `9064/2` exclusion.

## D10. Gonadoblastoma is a behaviour exclusion — provisional

ICD-O-3.2 has `9073/1` only, so ICCC-2017 subgroup Xc7 (declared `/3`) holds no usable code.
New in ICD-O-3.2, `8594/1` *Mixed germ cell-sex cord-stromal tumor, NOS* is also `/1`.

**Built:** gonadoblastoma alone → exclusion `9073/1`; gonadoblastoma with an invasive germ cell
tumour → the invasive tumour's own question, coded by the term the report uses. Moch 2022
(p. 464) lists gonadoblastoma among the non-invasive lesions.

**Deviation from the pathway (§3 Xc7, §4F, §7.6).** The disorder-of-sex-development entry, the
karyotype variables and the "upgrade edge" are not built. The tool codes the tumour present in
the file; who should be screened is a clinical question (ruling 9).

## D11. Sex cord–stromal tumours — settled by ICD-O-3.2, one registrar question

| Report says | Code |
|---|---|
| Adult granulosa cell tumour of the ovary | `8620/3` (changed from `/1`: *Terms that are changing behaviour*, p. 4) |
| Adult granulosa cell tumour of the testis | exclusion `8620/1` |
| Juvenile granulosa cell tumour, ovary | exclusion `8622/1` |
| Juvenile granulosa cell tumour, testis | exclusion `8622/0` |
| Sertoli-Leydig cell tumour, poorly differentiated | `8631/3` |
| — poorly differentiated, with heterologous elements | `8634/3` |
| — intermediate differentiation, with or without heterologous elements; retiform; not otherwise specified | exclusions `8631/1`, `8634/1`, `8633/1`, `8631/1` |
| — well differentiated | exclusion `8631/0` |
| Sertoli cell carcinoma or malignant Sertoli cell tumour | `8640/3` |
| Malignant Leydig cell tumour | `8650/3` |
| Malignant steroid cell tumour | `8670/3` |
| Malignant thecoma | `8600/3` |
| Malignant androblastoma | `8630/3` |
| Sex cord-stromal tumour, type not stated | exclusion `8590/1` |
| Any other benign or borderline sex cord–stromal tumour | its own exclusion |

**The registrar question.** Juvenile granulosa cell tumour is the commonest sex cord–stromal
tumour of childhood (Pathway §3 Xe; Pfister 2022 p. 343), and ICCC-2017 does not register it. A
wrong answer here removes the group's commonest gonadal stromal tumour from the registry.

**Deviation from the pathway (§4E, §5).** FOXL2 and DICER1 do not change any code here. They are
not built as variables.

## D12. A borderline tumour called malignant is not given a `/3` that ICD-O-3.2 does not print — provisional

The ICD-O matrix principle lets a coder raise the behaviour digit when a pathologist calls a
`/1` tumour malignant. ICD-O-3.2 prints neither `8590/3` nor `8622/3`, and standing rule 1
forbids fabricating a code. **Built:** the term as ICD-O-3.2 prints it.
This is the same question as Group 8 registrar item A1, and is put to the registrar once for
both groups.

## D13. Gonadal `8000–8005` is Group X — settled

ICCC-2017 range 117 places `8000–8005` at C56.9 and C62 in Xe. The pathway (§4H, §8 item 8)
reports a conflict with Master §6, which sends it to Group XII. ICCC-2017 is the grouping
convention (ruling 3) and settles it. **Built:** the gonadal trees emit `8000/3`–`8005/3`, and
the router's `8000-8005` rule gains a C56.9, C62.0, C62.1, C62.9 branch to group 10, Xe.

## D14. Gonadal carcinomas: the paediatric subset is on the tree — provisional

Xd holds 96 usable records. The ovary tree offers:

| Report says | Code |
|---|---|
| Small cell carcinoma, hypercalcaemic type | `8044/3` (ICD-O-3.2 related term) |
| Serous carcinoma, low grade / high grade / not stated | `8460/3` / `8461/3` / `8441/3` |
| Mucinous carcinoma | `8480/3` (ICD-O-3.2 synonym *Mucinous carcinoma*) |
| Mucinous cystadenocarcinoma | `8470/3` |
| Endometrioid carcinoma | `8380/3` |
| Clear cell carcinoma | `8310/3` |
| Seromucinous carcinoma | `8474/3` |
| Carcinoma, type not stated / undifferentiated / adenocarcinoma, type not stated | `8010/3` / `8020/3` / `8140/3` |
| Serous, mucinous, seromucinous or endometrioid borderline tumour | exclusions `8442/1`, `8472/1`, `8474/1`, `8380/1` |
| Cystadenoma | exclusion at the cystadenoma's own code |

The testis tree offers *Carcinoma* → `8010/3` only. Every other Xd code is in the inventory and
reachable by search. Small cell carcinoma of the ovary, hypercalcaemic type is coded from the
report's diagnosis; the BRG1 and SMARCA4 discussion (Pathway §4G) goes to
`docs/clinical-warnings.md`.

## D15. Variables the pathway proposes and the build does not — deviation

`pubertal_status`, `dsd_status`, `karyotype_y_material`, `teratoma_maturity`, `p57_status`,
`genotype_result`, `smarca4_brg1_status`, `serum_calcium`, `foxl2_status`, `dicer1_status` and
`i12p_status` (Pathway §5). Each is either code-neutral or decides between outcomes that are
all excluded. The Group 8 build made the same call on decalcification (Group 8 D15). The
prepubertal and postpubertal types enter only where they change the code: as the report's term
for a testicular teratoma (D5). Serum and cerebrospinal fluid markers enter through the
evidence route (D4), not as captured variables.

## D16. The site resolver is the router plus one small tree — design

The same code sits in Xa, Xb and Xc by site (Pathway §0.1, §7.1). The schema allows one entry
per (code, behaviour), so each shared entry carries `iccc3_subgroup_by_topography`, which
`app.js` resolves at output (`subgroupFor`), as Group 3's `9380` does.

Trees, routed by the router's `tree_routing` on the Stage 1 topography:

| Tree | Prefix | Topography |
|---|---|---|
| `g10_cns` | `cn_` | C70.0–C72.9, C75.1–C75.3 |
| `g10_ovary` | `ov_` | C56.9 |
| `g10_testis` | `ts_` | C62.0, C62.1, C62.9 |
| `g10_extragonadal` | `eg_` | every other code in `topography_codes.json` that ICCC-2017 places in Xb |
| `g10_site_unstated` | `su_` | the default: no topography captured, or one no rule names |

The search box enters a group with no topography, so it reaches `g10_site_unstated`. That tree
asks the evidence, then the site, and hands on by cross-tree `next_node` into the site trees, as
Groups 1–3 already do. No node type is added. The pathway's `site_resolution` node is used as
the closed vocabulary already defines it.

## D17. `9086/3` is a real code — settled

The REDCap option reads "Label not found". ICD-O-3.2 adds `9086/3` *Germ cell tumor with
associated hematological malignancy* (*New codes and their terms*, p. 2). ICCC-2017 range 105
places it in Xb6 only. Built in the extragonadal tree.

## D18. Group III is not changed — design, with open defects

Twelve branches in Groups III, VII and VIII refer to Group X; nine are Group III's. An
`app.js` referral is a terminal screen: the clerk starts a new case. Group III's own defects,
found on 4 October 2026 and left for the registrar because Group III must stay byte-identical
to `main`:

1. A biopsy-proven germinoma with normal markers has no route to Group X from `g3_midline`.
2. `pf_imaging_no_tissue` option 0 can never fire (`docs/TODO.md` §10).
3. `g3_supratentorial` has no germ cell route, though germinomas arise in the basal ganglia and
   third ventricle.
4. Every central nervous system topography lists only Group III in `topography_codes.json`, so
   the front door never offers Group X there. The search box is the only way into `g10_cns`.

## D19. Front-door reach outside the central nervous system — provisional

Add `C62.0` (620), `C62.1` (621) and `C76.3` (763, which the ICD-O-3 topography index uses for
the sacrococcygeal region) to `topography_codes.json`. Add Group 10 to the candidate groups of
`C38.1`, `C38.3`, `C48.0` and the new `C76.3`, the extragonadal sites the pathway names (§2A).
This adds one choice at those sites and changes no other group's tree.

## D20. A case with no topography shows the entry's default subgroup — design

An entry's own `iccc3_subgroup_id` is what the output shows when no topography was captured.
Each shared entry defaults to its gonadal subgroup (Xc) where one exists, else its extragonadal
subgroup (Xb), else Xa. REDCap computes `x_subgroup` itself from `x_morph` and `topo_code`, so the
tool's subgroup line is advisory.

## D21. An alias maps to a code only if it is true of every behaviour the group emits — design

`app.js` lists aliases under "Also called" by four-digit code (`aliasesFor`), not by behaviour.
Group X emits `9080` at `/0`, `/1` and `/3` and `9084` at `/0` and `/3` from the central nervous
system tree. An alias *Mature teratoma* on `9080` would appear on every immature teratoma output.
**Built:** an ICD-O-3.2 term becomes an alias of its code only when the group emits that code
at that term's behaviour and at no other. `9080` and `9084` carry the behaviour-neutral alias
*Teratoma* only. Terms of excluded behaviours (germ cell neoplasia in situ, gonadoblastoma,
juvenile granulosa cell tumour) are not aliased, as in Group 8.

## D22. The ovary has no baseline paper on disk — open

`docs/group_baseline_documents.md` assigns Group X two baselines. Moch 2022 covers the testis
and prints ICD-O codes. Höhn 2021 covers the vulva, vagina and cervix only: its full text
(PMC8494521, retrieved 4 October 2026) has no ovary or placenta section and prints no ICD-O
code. The natural replacement is McCluggage WG, Singh N, Gilks CB. *Key changes to the World
Health Organization (WHO) classification of female genital tumours introduced in the 5th
edition (2020).* Histopathology 2022;80(5):762–778. doi:10.1111/his.14609, PMID 34996131. It is
not in PubMed Central. **Built on:** ICD-O-3.2 for every ovarian code, and Pfister 2022 Table 3
(p. 342) and pp. 340–343 for which paediatric ovarian entities are current.
