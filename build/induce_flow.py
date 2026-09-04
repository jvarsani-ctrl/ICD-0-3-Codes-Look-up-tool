#!/usr/bin/env python3
"""Turn every marker checklist into a flow chart.

Registrar ruling 13 (4 Sep 2026): the coding logic is a flow chart. One option
leads to the next, and only the codes reachable through the branch taken are
loaded. A rule that can never fire is then structurally impossible instead of
a defect to hunt.

A node of type `ihc_checklist` used to show every marker it knows about at
once and evaluate an ordered rule list against whatever was ticked. Two things
follow from that shape and neither is visible on screen:

  * A rule whose conditions are a subset of an earlier rule's can never fire.
    It sits in the file looking like coding logic and is unreachable.
  * The clerk sees fifty-two markers and every code the node can reach, with
    nothing saying which are still in play.

This script induces, per node, the ORDER in which its markers should be asked,
and writes it into the node as `branch_sequence`. At runtime the engine asks
one marker at a time in that order, skipping any marker that no longer
separates the rules still alive, and stops when one rule stands.

The order is clinical content, so it is computed here and stored in the JSON;
the engine only walks it. Ordering key, in priority order:

  1. how many OUTCOMES the question removes on average — a question that cannot
     change the code is not worth asking;
  2. how many RULES it removes, which breaks the tie where several rules emit
     the same code;
  3. the marker group the marker was authored under — lineage groups are
     authored before entity groups;
  4. the order the author wrote the markers in.

The script also proves every rule is reachable by constructing a witness: an
answer vector under which that rule, and no earlier one, matches. A rule with
no witness is a build failure.

Idempotent: rerunning replaces `branch_sequence` and changes nothing else.
"""

import json
import os
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, 'data', 'database')

INTENSITIES = ('strong', 'weak')


# ---------------------------------------------------------------------------
# Rule semantics — these mirror app.js markerOk()/matchRules() exactly. If the
# two ever disagree the flow chart is a lie, so the validator re-runs the same
# simulation over the shipped JSON.
# ---------------------------------------------------------------------------

def split_token(token):
    """`CD30` -> ('CD30', None). `PAX5:weak` -> ('PAX5', 'weak').

    Split on the LAST colon and only when the tail is an intensity word, so a
    marker whose own name contains a colon — `NPM1::ALK` — survives intact.
    """
    s = str(token)
    for w in INTENSITIES:
        suffix = ':' + w
        if s.endswith(suffix) and len(s) > len(suffix):
            return s[:-len(suffix)], w
    return s, None


def marker_ok(token, answers):
    name, want = split_token(token)
    have = answers.get(name)
    if not have or have == 'neg':
        return False
    return have == want if want else True


def negative_ok(name, answers):
    v = answers.get(name)
    return (not v) or v == 'neg'


def when_value_ok(have, want):
    """A `when` value may be one state or a list of states that behave alike.

    The list form exists for ruling 11: a test that could not be interpreted
    is handled exactly like one that was never done, so both states point at
    the same branch instead of one of them falling through to a definite call
    the evidence does not support.
    """
    if isinstance(want, (list, tuple)):
        return any(str(have) == str(w) for w in want)
    return str(have) == str(want)


def when_ok(when, captured):
    if not when:
        return True
    return all(when_value_ok(captured.get(k), v) for k, v in when.items())


def rule_matches(rule, answers, captured):
    if not when_ok(rule.get('when'), captured):
        return False
    if not all(marker_ok(p, answers) for p in rule.get('positive') or []):
        return False
    if not all(negative_ok(m, answers) for m in rule.get('negative') or []):
        return False
    return True


def first_match(rules, answers, captured):
    for i, r in enumerate(rules):
        if rule_matches(r, answers, captured):
            return i
    return None


# ---------------------------------------------------------------------------
# Liveness during a partial walk
# ---------------------------------------------------------------------------

def still_live(rule, answers, captured):
    """True while no answer given so far rules this rule out."""
    for k, v in (rule.get('when') or {}).items():
        if k in captured and not when_value_ok(captured[k], v):
            return False
    for p in rule.get('positive') or []:
        name, want = split_token(p)
        have = answers.get(name)
        if have is None:
            continue
        if have == 'neg':
            return False
        if want and have != want:
            return False
    for m in rule.get('negative') or []:
        have = answers.get(m)
        if have is not None and have != 'neg':
            return False
    return True


def requirement(rule, marker):
    """What this rule needs of `marker`: 'pos', an intensity, 'neg', or None."""
    for p in rule.get('positive') or []:
        name, want = split_token(p)
        if name == marker:
            return want or 'pos'
    for m in rule.get('negative') or []:
        if m == marker:
            return 'neg'
    return None


def answer_options(marker, live):
    """The answers worth offering for `marker` given the rules still alive.

    Intensity buttons appear only where some live rule actually turns on
    intensity — a clerk should not be asked to grade a marker no rule grades.
    """
    reqs = {requirement(r, marker) for r in live}
    opts = ['pos']
    for w in INTENSITIES:
        if w in reqs:
            opts.append(w)
    opts.append('neg')
    return opts


def outcome_key(rule):
    """Where a rule lands. Several rules often land in the same place, and it is the
    number of PLACES still reachable that the clerk is watching shrink — so that, not the
    number of rules, is what a question should be scored on."""
    if rule.get('morphology_code'):
        return ('code', rule['morphology_code'], str(rule.get('behaviour_code')
                                                     or rule.get('behavior_code') or ''))
    if rule.get('next_node'):
        return ('node', rule['next_node'])
    if rule.get('refer_group'):
        return ('group', rule['refer_group'])
    if rule.get('exclude'):
        return ('exclude',)
    return ('continue',)


def outcomes(rules):
    return {outcome_key(r) for r in rules}


def power(marker, live):
    """What asking about `marker` is worth: (outcomes removed, rules removed).

    Both averaged across the answers rather than taken at the worst of them. Worst-case
    scoring sounds stricter and is useless here: near the top of a node almost every rule
    is still alive, so for every marker there is some answer that eliminates nothing,
    every marker scores zero, and the ranking collapses to the order the file happens to
    be written in.

    Outcomes lead because the clerk is coding, and a question that cannot change the code
    is not worth asking. Rules break the tie: a node where five rules emit one code and a
    sixth falls through never reduces its outcome count, and scoring on outcomes alone
    would ask nothing there at all — which is how an Erdheim-Chester case reached the
    fall-through after a single question.
    """
    here_o, here_r = len(outcomes(live)), len(live)
    opts = answer_options(marker, live)
    if not opts:
        return (0.0, 0.0)
    tot_o = tot_r = 0
    for opt in opts:
        survivors = [r for r in live if still_live(r, {marker: opt}, {})]
        tot_o += len(outcomes(survivors))
        tot_r += len(survivors)
    n = float(len(opts))
    return (here_o - tot_o / n, here_r - tot_r / n)


# ---------------------------------------------------------------------------
# Induction
# ---------------------------------------------------------------------------

def marker_universe(node):
    """Every marker the node offers, with the group index it was authored under."""
    order = OrderedDict()
    for gi, g in enumerate(node.get('marker_groups') or []):
        for mi, m in enumerate(g.get('markers') or []):
            if m not in order:
                order[m] = (gi, mi)
    return order


def induce(node):
    """The static question order for one node, plus the intensity markers."""
    rules = node.get('resolution_logic') or []
    universe = marker_universe(node)
    used = set()
    for r in rules:
        for p in r.get('positive') or []:
            used.add(split_token(p)[0])
        for m in r.get('negative') or []:
            used.add(m)

    # A marker no rule mentions can never change the answer. It stays in
    # marker_groups (the clerk may still want to record it) but it is not a
    # step in the flow chart.
    candidates = [m for m in universe if m in used]

    order = []
    live = list(rules)
    answers = {}
    while candidates:
        scored = []
        for m in candidates:
            po, pr = power(m, live)
            if po <= 1e-9 and pr <= 1e-9:
                continue
            gi, mi = universe[m]
            # Discriminating power leads. The authored group order is the tiebreak, not
            # the primary key: sorting by group first made a mature-T case answer eight
            # lineage markers that removed one candidate between them before reaching the
            # two that decided it. Lineage still tends to come first, because at a lineage
            # node the lineage markers ARE the ones that split the rules.
            scored.append((-po, -pr, gi, mi, m))
        if not scored:
            break
        scored.sort()
        chosen = scored[0][-1]
        order.append(chosen)
        candidates.remove(chosen)
        # Walk the branch that keeps the most rules alive, so the order stays
        # useful for the deepest path rather than for one lucky answer.
        best, best_n = None, -1
        for opt in answer_options(chosen, live):
            probe = dict(answers)
            probe[chosen] = opt
            n = sum(1 for r in live if still_live(r, probe, {}))
            if n > best_n:
                best, best_n = opt, n
        answers[chosen] = best
        live = [r for r in live if still_live(r, answers, {})]
        if len(live) <= 1:
            # Keep going: other branches of the chart still need their markers.
            live = list(rules)
            answers = {}

    # Anything mentioned by a rule but never selected above still has to be
    # askable, or the rule that needs it can never be reached.
    for m in candidates:
        order.append(m)

    intensity = sorted({
        split_token(p)[0]
        for r in rules for p in r.get('positive') or []
        if split_token(p)[1]
    })
    return order, intensity


# ---------------------------------------------------------------------------
# Proof: every rule must have a witness
# ---------------------------------------------------------------------------

def subsumes(a, b):
    """Rule `a` fires whenever rule `b` would — so `b` after `a` is dead."""
    def pos(r):
        return {split_token(p) for p in r.get('positive') or []}
    ap, bp = pos(a), pos(b)
    # a bare requirement is satisfied by any intensity, so it subsumes the graded one
    for name, want in ap:
        if want is None:
            if not any(n == name for n, _ in bp):
                return False
        elif (name, want) not in bp:
            return False
    if not set(a.get('negative') or []) <= set(b.get('negative') or []):
        return False
    aw, bw = a.get('when') or {}, b.get('when') or {}
    for k, v in aw.items():
        if not when_value_ok(bw.get(k), v):
            return False
    return True


def witness(rules, idx):
    """An answer vector under which rules[idx] matches and nothing earlier does.

    Breaking one earlier rule can make another one match — turning a marker on
    to violate rule 5's `negative` may be exactly what rule 2's `positive`
    was waiting for. So this repairs to a fixpoint rather than making one pass,
    and when it has a choice of marker it picks the one fewest earlier rules
    depend on. Only when no repair is available is the rule genuinely dead.
    """
    rule = rules[idx]
    fixed = {}
    # A list-valued `when` accepts any of its states; the witness picks one.
    captured = {k: (v[0] if isinstance(v, (list, tuple)) and v else v)
                for k, v in (rule.get('when') or {}).items()}
    for p in rule.get('positive') or []:
        name, want = split_token(p)
        fixed[name] = want or 'pos'
    for m in rule.get('negative') or []:
        fixed.setdefault(m, 'neg')
    answers = dict(fixed)

    # How many earlier rules would be helped by turning each marker on.
    demand = {}
    for j in range(idx):
        for p in rules[j].get('positive') or []:
            name, _ = split_token(p)
            demand[name] = demand.get(name, 0) + 1

    seen = set()
    blocker = [None]

    def search(ans, cap, depth):
        key = (tuple(sorted(ans.items())),
               tuple(sorted((k, repr(v)) for k, v in cap.items())))
        if key in seen or depth > len(rules) + 4:
            return None
        seen.add(key)
        j = first_match(rules, ans, cap)
        if j == idx:
            return ans, cap
        if j is None or j > idx:
            return None
        blocker[0] = j
        earlier = rules[j]
        # Every way of breaking this rule, cheapest first. Greedily taking one
        # can dead-end where another succeeds, so try them all.
        options = [m for m in (earlier.get('negative') or [])
                   if m not in fixed and ans.get(m) != 'pos']
        options.sort(key=lambda m: (demand.get(m, 0), m))
        for m in options:
            nxt = dict(ans)
            nxt[m] = 'pos'
            got = search(nxt, cap, depth + 1)
            if got:
                return got
        for k in (earlier.get('when') or {}):
            if k not in cap:
                ncap = dict(cap)
                ncap[k] = '__unmatched__'
                got = search(ans, ncap, depth + 1)
                if got:
                    return got
        return None

    found = search(answers, captured, 0)
    if found:
        return found, None
    return None, blocker[0]


def check_node(node):
    """Returns a list of failure strings."""
    fails = []
    rules = node.get('resolution_logic') or []
    for i in range(len(rules)):
        w, blocker = witness(rules, i)
        if w is None:
            if blocker is None:
                fails.append(
                    '%s rule[%d] can never fire — its own conditions cannot all be met'
                    % (node['node_id'], i))
            else:
                fails.append(
                    '%s rule[%d] can never fire — rule[%d] fires whenever it would'
                    % (node['node_id'], i, blocker))
            continue
        answers, captured = w
        got = first_match(rules, answers, captured)
        if got != i:
            fails.append(
                '%s rule[%d] is unreachable — its own witness matches rule[%s]'
                % (node['node_id'], i, got))
    return fails


def check_order_covers(node, order):
    """Every marker any rule turns on must be askable in the flow chart."""
    need = set()
    for r in node.get('resolution_logic') or []:
        for p in r.get('positive') or []:
            need.add(split_token(p)[0])
        for m in r.get('negative') or []:
            need.add(m)
    missing = sorted(need - set(order))
    return ['%s flow chart never asks: %s' % (node['node_id'], ', '.join(missing))] if missing else []


# ---------------------------------------------------------------------------

def process(path, write=True):
    with open(path) as fh:
        data = json.load(fh)
    fails, touched = [], 0
    for tree in data.get('decision_trees') or []:
        for node in tree.get('nodes') or []:
            if node.get('node_type') != 'ihc_checklist':
                node.pop('branch_sequence', None)
                continue
            order, intensity = induce(node)
            fails += check_node(node)
            fails += check_order_covers(node, order)
            node['branch_sequence'] = {
                'order': order,
                'intensity_markers': intensity,
                'rule_count': len(node.get('resolution_logic') or []),
            }
            touched += 1
    if write and not fails:
        with open(path, 'w') as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
            fh.write('\n')
    return touched, fails


def main():
    write = '--check' not in sys.argv
    total_fail = []
    for name in sorted(os.listdir(DB)):
        if not name.endswith('_dt.json'):
            continue
        path = os.path.join(DB, name)
        touched, fails = process(path, write=write)
        print('%-22s %2d checklist nodes  %s'
              % (name, touched, 'OK' if not fails else '%d FAIL' % len(fails)))
        total_fail += fails
    if total_fail:
        print('\n%d unreachable rules:' % len(total_fail))
        for f in total_fail:
            print('  FAIL  ' + f)
        return 1
    print('\nEvery rule in every checklist has a witness. Flow charts written.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
