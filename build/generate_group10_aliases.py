#!/usr/bin/env python3
"""Generate data/aliases/aliases_group_10.json for ICCC-3 Group X, germ cell, trophoblastic
and gonadal tumours.

Group 10 build contract §6. Three sources, merged by alias string (first source wins):

  1. ICD-O-3.2 terms (Preferred, Synonym, Related; never [obs]) of every (code, behaviour)
     the trees emit. The emitted set is read from the trees, the same way validator rule 3
     reads it (build_database._group10_emissions: code branches, immunohistochemistry rule
     results, imaging_pathway nodes, nos_fallback), never from a hand list.
  2. REDCap x_morph option strings that differ from the preferred term and are ICD-O-3.2
     terms at an emitted pair. This helps a clerk who types the REDCap wording. It does not
     test REDCap (standing rule 16).
  3. Curated names, CURATED below: the British spellings and WHO names the trees use.

Design D21 governs all three. app.js aliasesFor() lists an alias under "Also called" on every
output of a four-digit code, whatever the behaviour. So an alias is attached to a code only
when it is true of every behaviour the group emits for that code. A term is used only if the
group emits its code at the term's behaviour and at no other. Group X emits 9080 at /0, /1 and
/3 and 9084 at /0 and /3, so neither code carries an ICD-O-3.2 term; both carry the neutral
alias "Teratoma" (bd.GROUP10_D21_NEUTRAL_ALIASES). A term of a behaviour the group does not emit (germ cell
neoplasia in situ 9064/2, gonadoblastoma 9073/1, juvenile granulosa cell tumour 8622/1, struma
ovarii 9090/0, hydatidiform moles 9100/0 and 9100/1, placental site trophoblastic tumour
9104/1, borderline and benign tumours) is never aliased: the express lane is for codes the
tree emits.

The generator and validator rule 3 (check_group10_alias_terms_match_icdo32) share two
functions: build_database._group10_term_key(), which decides what "equal to an ICD-O-3.2 term"
means, and build_database._group10_emissions(), which reads the emitted set from the trees. A
fault in either is therefore invisible to the rule: on those two functions the rule is not
independent of the generator. It is independent on everything else (the ICD-O-3.2 terms read
from icdo32.sqlite, the D21 test itself, the neutral-alias exemption and the germinoma check),
and negative_controls_group10.py proves it catches a wrong alias for the right reason.

Not aliased: "GCT" (germ cell tumour or granulosa cell tumour; the Alias Build Instructions'
own collision), and "Teratoma, postpubertal type" and "Immature teratoma" (each true of 9080/3
only; D21).

Each alias carries the router's hand-off tree and entry node, as Group 9's aliases do for a
group with tree_routing: the express lane asks the site, and the router's tree_routing picks
the site tree. needs_ihc_tree is True where an ihc_checklist node can emit the alias's code.

Run after build/generate_group10_entries.py:

    python3 build/generate_group10_aliases.py

In a git worktree set ICD_LAYER1, ICCC_DB and ICDO_DB first (docs/group_10_build_contract.md,
section 1).
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_database as bd  # noqa: E402
import generate_group_inventory as gi  # noqa: E402

GROUP = bd.GROUP10
DT = REPO / "data" / "database" / "group_10_dt.json"
ROUTER = REPO / "data" / "shared" / "presentation_router.json"
OUT = REPO / "data" / "aliases" / "aliases_group_10.json"
LAYER1 = Path(os.environ.get("ICD_LAYER1", str(gi.DEFAULT_LAYER1)))

LEVELS = ("Preferred", "Synonym", "Related")
_LEVEL_RANK = {name: i for i, name in enumerate(LEVELS)}

# ICD-O-3.2 terms on an emitted pair that would mislead a gonadal or germ cell search.
EXCLUDED_TERMS = {
    "Cancer": "generic; matches every group",
    "Malignancy": "generic; matches every group",
    "Tumor, malignant, NOS": "generic; matches every group",
    "Unclassified tumor, malignant": "generic; matches every group",
    "Blastoma, NOS": "generic; a blastoma in a child is rarely a gonadal tumour",
    "Malignant tumor, fusiform cell type": "generic descriptor",
    "Epithelial tumor, malignant": "generic; matches every carcinoma",
    "Heterotopia-associated carcinoma": "generic descriptor with no gonadal meaning",
    "Carcinoma of Skene, Cowper and Littre glands": "a urethral gland tumour, not a gonadal one",
    "Endolymphatic sac tumor": "an ear tumour; the code is the adenocarcinoma stem",
    "Parathyroid carcinoma": "a parathyroid tumour; the code is the adenocarcinoma stem",
    "Acinar adenocarcinoma of prostate": "a prostate tumour; the code is the adenocarcinoma stem",
    "Clear cell renal cell carcinoma, NOS": "a kidney tumour, Group VI",
    "Acinar adenocarcinoma, mucinous variant": "a prostate variant; the code is the mucinous "
                                               "adenocarcinoma stem",
    "Mucinous tubular and spindle cell carcinoma": "a kidney tumour, Group VI",
    "Mucinous cystic neoplasm with an associated invasive carcinoma": "digestive-system "
        "(pancreatic or hepatobiliary) mucinous cystic neoplasm wording; the code is the "
        "ovarian mucinous cystadenocarcinoma stem",
    "Mucinous cystic tumor with an associated invasive carcinoma": "as above",
    "Pseudomyxoma peritonei with unknown primary site": "names a peritoneal or appendiceal "
        "primary; Pseudomyxoma peritonei is 8480/6",
}

# Appended to the notes of every ICD-O-3.2-term alias on the code.
NOTE_SUFFIX = {
    "9060": " Germinoma, at any site, is 9064/3, not 9060 (design D1).",
    "9064": " Not 9060: ICD-O-3.2 files Germinoma under 9064/3 and Dysgerminoma under 9060/3 "
            "(design D1). Germ cell tumor, NOS is a synonym of 9064/3 (design D2).",
    "8620": " Adult type of the ovary. Of the testis it is 8620/1, and the juvenile type is "
            "8622/1 or 8622/0; neither is a Group X code (design D11).",
    "8631": " Poorly differentiated only. Well, intermediate and retiform forms and Sertoli-Leydig "
            "cell tumor, NOS are behaviour exclusions (design D11).",
    "8640": " The malignant tumour. Sertoli cell tumor, NOS is 8640/1, a behaviour exclusion "
            "(design D11).",
    "8650": " The malignant tumour. Leydig cell tumor of testis, NOS is 8650/1 and Leydig cell "
            "tumor of ovary, NOS is 8650/0, behaviour exclusions (design D11).",
    "9100": " Choriocarcinoma only. Hydatidiform moles are 9100/0 and 9100/1, behaviour "
            "exclusions (design D8).",
}

# D21's behaviour-neutral aliases: exact alias text (lower case) -> the codes it maps to.
# This is the exemption rule 3 reads, imported so the two cannot drift.
D21_NEUTRAL = bd.GROUP10_D21_NEUTRAL_ALIASES

SOURCE_1 = "ICD-O-3.2 term"
SOURCE_2 = "REDCap option string"
SOURCE_3 = "curated"

# alias, codes, alias_type, origin_system, nci_concept_id, notes
# NCIt concept IDs come from the confirmed table in 'Group 10 — Alias Build Instructions.md'
# (14 May 2026), section 1, and only where the table's entity is the alias's entity.
CURATED = [
    ("Yolk sac tumour", ["9071"], "descriptive", "ICD-O-3.2 (British spelling)", "NCIT:C3011",
     "British spelling of Yolk sac tumor, NOS (9071/3)."),
    ("Endodermal sinus tumour", ["9071"], "descriptive", "ICD-O-3.2 (British spelling)",
     "NCIT:C3011",
     "British spelling of the ICD-O-3.2 synonym Endodermal sinus tumor, 9071/3."),
    ("Yolk sac tumour, prepubertal type", ["9071"], "descriptive",
     "ICD-O-3.2 (British spelling)", "NCIT:C3011",
     "British spelling of the ICD-O-3.2 synonym Yolk sac tumor, pre-pubertal type, 9071/3. "
     "The prepubertal and postpubertal types are 9071/3 (contract §4.4)."),
    ("Yolk sac tumour, postpubertal type", ["9071"], "descriptive",
     "ICD-O-3.2 (British spelling)", "NCIT:C3011",
     "British spelling of the ICD-O-3.2 related term Yolk sac tumor, post-pubertal type, "
     "9071/3."),
    ("Germ cell tumour, NOS", ["9064"], "descriptive", "ICD-O-3.2 (British spelling)", None,
     "British spelling of the ICD-O-3.2 synonym Germ cell tumor, NOS, 9064/3 (design D2). "
     "The output names the code by its preferred term, Germinoma; a report that says only "
     "germ cell tumour has not diagnosed a germinoma."),
    ("Non-germinomatous germ cell tumour", ["9065"], "descriptive",
     "Clinical descriptive term", "NCIT:C121619",
     "Clinical wording for Germ cell tumor, nonseminomatous (9065/3). NCIt names the concept "
     "Nongerminomatous Germ Cell Tumor."),
    ("Mixed germ cell tumour", ["9085"], "descriptive", "ICD-O-3.2 (British spelling)",
     "NCIT:C4290", "British spelling of Mixed germ cell tumor (9085/3)."),
    ("Teratoma", ["9080", "9084"], "descriptive", "Clinical descriptive term", "NCIT:C3403",
     "The behaviour-neutral alias (design D21). Group X emits 9080 at /0, /1 and /3 and 9084 "
     "at /0 and /3 (the central nervous system tree emits /0 and /1; every tree emits /3), "
     "and 'Also called' lists an alias on every output of its code, so only this text, true "
     "of every behaviour, is attached to these codes. The tree takes the behaviour from the "
     "report."),
    ("Embryonal carcinoma", ["9070"], "descriptive", "ICD-O-3.2 (wording variant)",
     "NCIT:C3752",
     "Embryonal carcinoma, NOS (9070/3) without the NOS. Embryonal carcinoma, infantile is "
     "an ICD-O-3.2 synonym of Yolk sac tumor, 9071/3."),
    ("Spermatocytic tumour", ["9063"], "descriptive", "ICD-O-3.2 (British spelling)",
     "NCIT:C39921",
     "British spelling of the ICD-O-3.2 synonym Spermatocytic tumor, 9063/3. Coded as the "
     "report writes it (design D3)."),
    ("Small cell carcinoma of the ovary, hypercalcaemic type", ["8044"], "descriptive",
     "Clinical descriptive term", None,
     "The ovarian tumour that ICD-O-3.2 lists as Small cell carcinoma, hypercalcemic type, a "
     "related term of 8044/3 (design D14; contract §4.4)."),
    ("Low-grade serous carcinoma", ["8460"], "descriptive", "ICD-O-3.2 (wording variant)", None,
     "Hyphenated form of Low grade serous carcinoma (8460/3) (design D14)."),
    ("High-grade serous carcinoma", ["8461"], "descriptive", "ICD-O-3.2 (wording variant)",
     None, "Hyphenated form of High grade serous carcinoma (8461/3) (design D14)."),
    ("Adult granulosa cell tumour", ["8620"], "descriptive", "ICD-O-3.2 (British spelling)",
     None,
     "British spelling of Adult granulosa cell tumor of ovary (8620/3). Of the testis the "
     "tumour is 8620/1, which Group X does not register (design D11)."),
    ("Sertoli-Leydig cell tumour, poorly differentiated", ["8631"], "descriptive",
     "ICD-O-3.2 (British spelling)", None,
     "British spelling of Sertoli-Leydig cell tumor, poorly differentiated (8631/3)."),
    ("Germ cell tumour with associated haematological malignancy", ["9086"], "descriptive",
     "ICD-O-3.2 (British spelling)", None,
     "British spelling of Germ cell tumor with associated hematological malignancy (9086/3)."),
    ("Epithelioid trophoblastic tumour", ["9105"], "descriptive",
     "ICD-O-3.2 (British spelling)", "NCIT:C6900",
     "British spelling of Trophoblastic tumor, epithelioid (9105/3)."),
]


# --------------------------------------------------------------------------------------
# What the group emits and what ICD-O-3.2 says
# --------------------------------------------------------------------------------------

def key(text: str) -> str:
    """The comparison form validator rule 3 uses."""
    return bd._group10_term_key(text)


def load():
    dt = json.loads(DT.read_text(encoding="utf-8"))
    ctx = bd.DTContext(DT, dt, GROUP)
    emitted: dict[str, set[str]] = {}
    ihc: set[str] = set()
    for node_id, _where, code, beh in bd._group10_emissions(ctx):
        emitted.setdefault(code, set()).add(beh)
        if ctx.nodes[node_id].get("node_type") == "ihc_checklist":
            ihc.add(code)
    index, err = bd.load_icdo32(LAYER1)
    if err:
        raise SystemExit("ERROR: %s" % err)
    pairs: dict[str, dict[tuple[str, str], str]] = {}
    for (code, beh), bucket in index.items():
        for term in bucket:
            pairs.setdefault(key(term), {})[(code, beh)] = term
    options, found = bd.parse_redcap_options(LAYER1)
    opts = options.get(GROUP)
    if not opts:
        raise SystemExit("ERROR: no REDCap options parsed for Group %d (%s)"
                         % (GROUP, "; ".join(m for _s, m in found)))
    router = json.loads(ROUTER.read_text(encoding="utf-8"))
    handoff = router["groups"][str(GROUP)]["handoff"]
    entries = {(e["morphology_code"], e["behavior_code"]): e for e in dt["morphology_entries"]}
    return emitted, ihc, index, pairs, opts, handoff, entries


def d21_codes(pairs, emitted, text):
    """The codes ICD-O-3.2 files `text` under that the group emits at the term's behaviour
    and at no other (design D21), sorted."""
    hits = pairs.get(key(text), {})
    ok = []
    for code in sorted({c for c, _b in hits}):
        term_behs = {b for c, b in hits if c == code}
        em = emitted.get(code)
        if em and em <= term_behs:
            ok.append(code)
    return ok


def report_shared(out: list[dict]) -> None:
    """Print every alias string another group's file also holds, with that group's codes."""
    other: dict[str, list[tuple[int, list]]] = {}
    for path in sorted((REPO / "data" / "aliases").glob("aliases_group_*.json")):
        group = int(path.stem.rsplit("_", 1)[1])
        if group == GROUP:
            continue
        for a in json.loads(path.read_text(encoding="utf-8")):
            other.setdefault(a["alias"].strip().lower(), []).append(
                (group, a.get("maps_to_morphology_codes") or []))
    shared = [(a, other[a["alias"].strip().lower()]) for a in out
              if a["alias"].strip().lower() in other]
    print("%d alias string(s) shared with other groups (the site settles a shared term):"
          % len(shared), file=sys.stderr)
    for a, holders in shared:
        print("  %r -> %s; also %s" % (
            a["alias"], "/".join(a["maps_to_morphology_codes"]) or "no code",
            ", ".join("Group %d -> %s" % (g, "/".join(c) or "no code") for g, c in holders)),
            file=sys.stderr)


def main() -> int:
    emitted, ihc, index, pairs, opts, handoff, entries = load()
    redcap_names = {key(n) for rec in opts.values() for n in rec["names"]}

    def entry_at(code: str, beh: str) -> dict:
        try:
            return entries[(code, beh)]
        except KeyError:
            raise SystemExit("ERROR: the trees emit %s/%s but group_10_dt.json has no "
                             "morphology entry for that pair; run "
                             "build/generate_group10_entries.py" % (code, beh)) from None

    def entry_for(code: str) -> dict:
        return entry_at(code, max(emitted[code]))

    def name_for(code: str) -> str:
        if len(emitted[code]) == 1:
            return "%s (%s)" % (entry_for(code)["morphology_name"], code)
        return "%s at /%s, by the behaviour the report states" % (
            code, ", /".join(sorted(emitted[code])))

    out: list[dict] = []
    seen: set[str] = set()
    by_source: dict[str, int] = {SOURCE_1: 0, SOURCE_2: 0, SOURCE_3: 0}

    def add(source, alias, codes, alias_type, origin, nci, notes, coding_note):
        if alias.lower() in seen:
            return
        for c in codes:
            if c not in emitted:
                raise SystemExit("ERROR: alias %r maps to %s, which no tree emits" % (alias, c))
        seen.add(alias.lower())
        by_source[source] += 1
        out.append({
            "alias": alias,
            "full_form": "%s -> %s" % (alias, " / ".join(name_for(c) for c in codes)),
            "also_known_as": [],
            "alias_type": alias_type,
            "origin_system": origin,
            "nci_concept_id": nci,
            "who_version_current": "ICD-O-3.2",
            "maps_to_morphology_codes": codes,
            "maps_to_iccc3_subgroup_id": entry_for(codes[0])["iccc3_subgroup_id"],
            "needs_ihc_tree": any(c in ihc for c in codes),
            "ihc_tree_id": handoff["tree_id"],
            "tree_entry_node": handoff["entry_node"],
            "clinical_alert": None,
            "notes": notes,
            "coding_note": coding_note,
        })

    # 1. ICD-O-3.2 terms on the emitted pairs, subject to D21.
    for code in sorted(emitted):
        for beh in sorted(emitted[code]):
            bucket = index.get((code, beh), {})
            for term, (level, obs) in sorted(
                    bucket.items(), key=lambda kv: (_LEVEL_RANK.get(kv[1][0], 9), kv[0])):
                if obs or level not in LEVELS or term in EXCLUDED_TERMS:
                    continue
                if code not in d21_codes(pairs, emitted, term):
                    continue
                preferred = level == "Preferred"
                name = entry_at(code, beh)["morphology_name"]
                add(SOURCE_1, term, [code],
                    "who_preferred" if preferred else "descriptive",
                    "ICD-O-3.2" if preferred else "ICD-O-3.2 %s" % (
                        "synonym" if level == "Synonym" else "related term"),
                    None,
                    (("%s, %s/%s." % (name, code, beh)) if preferred else
                     ("An ICD-O-3.2 %s term for %s (%s/%s)." % (level.lower(), name, code, beh)))
                    + NOTE_SUFFIX.get(code, ""),
                    "ICD-O-3.2 %s term on %s/%s, read from icdo32.sqlite; D21 holds: Group X "
                    "emits %s at /%s only.%s"
                    % (level, code, beh, code, "/".join(sorted(emitted[code])),
                       " Also the REDCap option wording." if key(term) in redcap_names else ""))

    # 2. REDCap option strings that differ from the preferred term and are ICD-O-3.2 terms at
    #    an emitted pair. A string that names a benign, borderline or in situ term, or no
    #    ICD-O-3.2 term at that code, is not aliased.
    for code in sorted(opts):
        if code not in emitted:
            continue
        for name in opts[code]["names"]:
            if code not in d21_codes(pairs, emitted, name):
                continue
            hits = [(c, b) for (c, b) in pairs[key(name)] if c == code]
            matched = [index[(c, b)].get(name) for c, b in hits]
            if any(m and m[0] == "Preferred" for m in matched):
                continue
            if any(m and m[1] for m in matched):
                continue
            add(SOURCE_2, name, [code], "descriptive", "REDCap option label", None,
                "The REDCap option wording for %s. It equals an ICD-O-3.2 term of %s/%s apart "
                "from a trailing NOS." % (code, code, "/".join(sorted(emitted[code]))),
                "x_morph option string for %s that differs from the ICD-O-3.2 preferred term. "
                "Offered so a clerk who types the dropdown wording finds the code; it is not a "
                "test of REDCap (standing rule 16)." % code)

    # 3. Curated names. A curated alias that is an ICD-O-3.2 term must satisfy D21 or be the
    #    neutral alias; a violation is a build error here, before rule 3 would catch it.
    for alias, codes, alias_type, origin, nci, notes in CURATED:
        neutral = D21_NEUTRAL.get(" ".join(alias.lower().split()))
        if neutral is not None:
            if set(codes) != set(neutral) or len(codes) != len(neutral):
                raise SystemExit("ERROR: %r must map to %s (D21)" % (alias, sorted(neutral)))
        elif key(alias) in pairs:
            bad = [c for c in codes if c not in d21_codes(pairs, emitted, alias)]
            if bad:
                raise SystemExit("ERROR: curated alias %r maps to %s, which fails D21 or is "
                                 "not a code ICD-O-3.2 files it under" % (alias, bad))
        add(SOURCE_3, alias, codes, alias_type, origin, nci, notes,
            "Curated: %s%s. Corrected to ICD-O-3.2 by the Group 10 build (design D1-D21)."
            % ("Group 10 build contract §6", ", NCIt " + nci +
               " from 'Group 10 — Alias Build Instructions.md' (14 May 2026)" if nci else ""))

    # Every 'X, NOS' stays even where a bare 'X' exists for the same code: app.js
    # searchAlias() matches key.indexOf(needle), so a clerk who types the exact ICD-O-3.2 or
    # REDCap string must find an alias that holds it. The bare 'X' does not contain ', NOS'.
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote %s (%d aliases: %s)"
          % (OUT, len(out), ", ".join("%d %s" % (n, s) for s, n in by_source.items())),
          file=sys.stderr)
    report_shared(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
