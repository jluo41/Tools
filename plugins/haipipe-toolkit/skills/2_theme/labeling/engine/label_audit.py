#!/usr/bin/env python3
"""Audit an existing labeled corpus from its raters' votes (use case 2: "Recover a standard from existing labels,
then apply it to new items"; deck v12 slide 3). Pure functions plus a small CLI; no model calls.

Existing labels are evidence of prior decisions, not a reference set: this module reads only per-rater answers, and
a flag is a reason to ask, never a finding that a label is wrong ("A flag does not establish an error").

    legacy_votes(rows, ...)        per item: the raters' answer counts, overall and per group level (the fence)
    legacy_row(item_id, votes)     one item's existing label: majority, unsafe share, Unsure share, group shares
    signals(row, ...)              the flags of one item: split, tie, Unsure, a group gap (|z|)
    draw(signal_rows, train, ...)  three disjoint samples of Train items, each with its inclusion probability
    evidence_row(item, row, ...)   one decision-report evidence row, the item's exact excerpt (meaning_contracts)
    apply_answers(...)             the reviewed labels a person's answers make (l01 from l00)

The fence: an expert key (a label the dataset's experts gave once per item) must never reach the audit. A field
named to legacy_votes that is the same for every rater of every item is an item property, not a rater's answer,
and raises FenceError; any field not named is never read.

CLI (the Project's Runs call it):
    label_audit.py legacy --raters items.raters.jsonl --answer Q_overall --groups a,b --out legacy_labels.jsonl
    label_audit.py draw --legacy legacy_labels.jsonl --split split.json --seed 261101 --out-dir result/
"""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

POSITIVE, NEGATIVE, UNSURE = "Yes", "No", "Unsure"      # DICES Q_overall: Yes = the reply is unsafe
LABEL = {POSITIVE: "unsafe", NEGATIVE: "safe"}            # the audit's binary label
FLAG_ORDER = ("tie", "split", "gap", "unsure")            # a flagged item's stratum: its first flag in this order
DEFAULTS = {"split": (0.4, 0.6), "unsure_min": 0.15, "z_min": 3.0, "min_level": 20}

# The option ids each card kind uses; apply_answers reads them (the effects stay human words in the report).
CHAT_OPTIONS = ("keep", "flip", "change_rule")            # question_type reference_label: one flagged item
TIE_OPTIONS = ("set_unsafe", "set_safe", "change_rule")    # the same, for an item whose raters have no majority
BLIND_OPTIONS = ("blind_unsafe", "blind_safe", "blind_cant_tell")  # question_type diagnostic: label hidden
RULE_OPTIONS = ("rule_holds", "rule_change", "rule_drop")  # question_type define_rule: a candidate rule


class FenceError(ValueError):
    """An item-level field (an expert key, or any per-item property) was named as a rater's answer or group."""


# ── the raters' votes, behind the fence ────────────────────────────────────────────────────────────────────


def legacy_votes(rows, *, item="item_id", answer="Q_overall", values=(POSITIVE, NEGATIVE, UNSURE), groups=(),
                 rater="rater_id") -> dict:
    """Count each item's answers, overall and per level of each group field, reading only the named fields.

    Returns {item_id: {"n": int, "counts": {value: int}, "groups": {field: {level: {value: int, "n": int}}}}}.
    Raises FenceError when a named field (the answer or a group) is constant across the raters of every item that
    has two or more raters: such a field is an item property, such as an expert's label, not a rater's answer.
    """
    rows = list(rows)
    named = [answer, *groups]
    seen: dict[str, dict[str, set]] = {field: defaultdict(set) for field in named}
    raters: Counter = Counter()
    out: dict[str, dict] = {}
    for row in rows:
        item_id = str(row[item])
        raters[item_id] += 1
        for field in named:
            seen[field][item_id].add(row.get(field))
        value = row.get(answer)
        rec = out.setdefault(item_id, {"n": 0, "counts": {v: 0 for v in values},
                                       "groups": {g: {} for g in groups}})
        if value not in values:
            continue
        rec["n"] += 1
        rec["counts"][value] += 1
        for field in groups:
            level = str(row.get(field))
            cell = rec["groups"][field].setdefault(level, {**{v: 0 for v in values}, "n": 0})
            cell[value] += 1
            cell["n"] += 1
    multi = [item_id for item_id, k in raters.items() if k >= 2]
    for field in named:
        if multi and all(len(seen[field][item_id]) == 1 for item_id in multi):
            raise FenceError(f"{field!r} is the same for every rater of every item: an item property (an expert "
                             "key?), not a rater's answer; the audit never reads it")
    return out


def majority(counts: dict) -> str:
    """The most common answer; "Tie" when two answers share the top count (t02's rule, Unsure included)."""
    top = Counter({k: v for k, v in counts.items()}).most_common()
    if not top or top[0][1] == 0:
        return "Tie"
    if len(top) > 1 and top[0][1] == top[1][1]:
        return "Tie"
    return top[0][0]


def legacy_row(item_id: str, votes: dict) -> dict:
    """One item's existing label (l00) from its votes: the majority, its binary label, the unsafe and Unsure shares
    over all raters (t02's definitions), and each group level's unsafe share."""
    n = votes["n"]
    counts = votes["counts"]
    major = majority(counts)
    groups = {field: {level: {"n": cell["n"], "unsafe": cell.get(POSITIVE, 0)}
                      for level, cell in sorted(levels.items())}
              for field, levels in votes["groups"].items()}
    return {"item_id": item_id, "n": n, "counts": counts, "majority": major, "label": LABEL.get(major),
            "unsafe_share": round(counts.get(POSITIVE, 0) / n, 4) if n else None,
            "unsure_share": round(counts.get(UNSURE, 0) / n, 4) if n else None, "groups": groups}


# ── the flags ───────────────────────────────────────────────────────────────────────────────────────────────


def _gap(row: dict, min_level: int) -> dict | None:
    """The largest two-proportion |z| between one group level and the rest of that item's raters, counting only
    levels and rests of at least min_level raters (small groups make a maximum over many levels mostly noise)."""
    best = None
    for field, levels in row["groups"].items():
        n_all = sum(cell["n"] for cell in levels.values())
        y_all = sum(cell["unsafe"] for cell in levels.values())
        for level, cell in levels.items():
            n_rest, y_rest = n_all - cell["n"], y_all - cell["unsafe"]
            if cell["n"] < min_level or n_rest < min_level:
                continue
            p = y_all / n_all
            se = math.sqrt(p * (1 - p) * (1 / cell["n"] + 1 / n_rest))
            if se == 0:
                continue
            z = (cell["unsafe"] / cell["n"] - y_rest / n_rest) / se
            if best is None or abs(z) > abs(best["z"]):
                best = {"field": field, "level": level, "z": round(z, 2), "share": round(cell["unsafe"] / cell["n"], 3),
                        "rest": round(y_rest / n_rest, 3), "n": cell["n"]}
    return best


def signals(row: dict, *, split=DEFAULTS["split"], unsure_min=DEFAULTS["unsure_min"], z_min=DEFAULTS["z_min"],
            min_level=DEFAULTS["min_level"]) -> dict:
    """The flags of one item, from its legacy row only. The cutoffs are fixed before any item is read and never
    tuned after scoring (the Run's config records them)."""
    share, unsure = row["unsafe_share"], row["unsure_share"]
    gap = _gap(row, min_level)
    flags = {
        "tie": row["majority"] == "Tie",
        "split": share is not None and split[0] <= share <= split[1],
        "gap": gap is not None and abs(gap["z"]) >= z_min,
        "unsure": unsure is not None and unsure >= unsure_min,
    }
    on = [name for name in FLAG_ORDER if flags[name]]
    return {"item_id": row["item_id"], "label": row["label"], "majority": row["majority"], "unsafe_share": share,
            "unsure_share": unsure, "gap": gap, "flags": on, "flagged": bool(on),
            "stratum": on[0] if on else "unflagged"}


# ── the draw ────────────────────────────────────────────────────────────────────────────────────────────────


def _allocate(n: int, sizes: dict[str, int], minimum: int = 0) -> dict[str, int]:
    """Share n among strata in proportion to their sizes (largest remainder), never more than a stratum holds; with a
    minimum, every non-empty stratum first gets that many when n allows (so no kind of flag goes unasked)."""
    total = sum(sizes.values())
    if total == 0 or n <= 0:
        return {key: 0 for key in sizes}
    n = min(n, total)
    base = {key: min(minimum, size) for key, size in sizes.items()}
    if minimum and sum(base.values()) <= n:
        rest = _allocate(n - sum(base.values()), {key: sizes[key] - base[key] for key in sizes})
        return {key: base[key] + rest[key] for key in sizes}
    raw = {key: n * size / total for key, size in sizes.items()}
    take = {key: min(int(value), sizes[key]) for key, value in raw.items()}
    order = sorted(sizes, key=lambda key: (-(raw[key] - int(raw[key])), key))
    while sum(take.values()) < n:
        for key in order:
            if sum(take.values()) < n and take[key] < sizes[key]:
                take[key] += 1
    return take


def draw(signal_rows, train_ids, *, n_hard=12, n_blind=4, n_typical=40, seed=261101) -> dict:
    """Three disjoint samples of Train items: hard (flagged, stratified by first flag, at least one per kind), blind (unflagged, shown
    without their label) and typical (unflagged, for reading the rules the raters followed). Test items are never
    drawn. Each sample carries its inclusion probability: pi = drawn / eligible, per stratum for hard."""
    train = {str(i) for i in train_ids}
    rows = sorted((r for r in signal_rows if r["item_id"] in train), key=lambda r: r["item_id"])
    rng = random.Random(seed)
    flagged: dict[str, list[str]] = defaultdict(list)
    unflagged: list[str] = []
    for r in rows:
        (flagged[r["stratum"]] if r["flagged"] else unflagged).append(r["item_id"])
    sizes = {key: len(ids) for key, ids in sorted(flagged.items())}
    take = _allocate(n_hard, sizes, minimum=1)
    hard, pi_hard = [], {}
    for key in sorted(take):
        chosen = rng.sample(flagged[key], take[key])
        hard += sorted(chosen)
        pi_hard[key] = round(take[key] / sizes[key], 4) if sizes[key] else 0.0
    n_blind = min(n_blind, len(unflagged))
    blind = sorted(rng.sample(unflagged, n_blind))
    rest = [i for i in unflagged if i not in set(blind)]
    n_typical = min(n_typical, len(rest))
    typical = sorted(rng.sample(rest, n_typical))
    return {
        "seed": seed, "train": len(rows), "flagged": sum(sizes.values()), "unflagged": len(unflagged),
        "strata": sizes, "sets": {"hard": hard, "blind": blind, "typical": typical},
        "pi": {"hard": pi_hard, "blind": round(n_blind / len(unflagged), 4) if unflagged else 0.0,
               "typical": round(n_typical / len(rest), 4) if rest else 0.0},
    }


def stratified_split(legacy_rows, *, n_test=50, seed=261101, bins=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0)) -> dict:
    """One seeded Train/Test split whose Test mirrors the raters' vote spread: items binned by unsafe share, the
    n_test drawn in proportion to each bin's size (largest remainder). fence_source.draw_sealed gives every stratum
    the same share, which leaves a small bin short; nothing here is hashed."""
    rows = sorted(legacy_rows, key=lambda r: r["item_id"])
    strata: dict[str, list[str]] = defaultdict(list)
    for r in rows:
        share = r["unsafe_share"] or 0.0
        k = next((i for i in range(len(bins) - 1) if share <= bins[i + 1]), len(bins) - 2)
        strata[f"{bins[k]:.1f}-{bins[k + 1]:.1f}"].append(r["item_id"])
    sizes = {key: len(ids) for key, ids in sorted(strata.items())}
    take = _allocate(n_test, sizes)
    rng = random.Random(seed)
    test = sorted(i for key in sorted(take) for i in rng.sample(strata[key], take[key]))
    held = set(test)
    return {"version": "v01", "seed": seed, "n_test": len(test), "n_train": len(rows) - len(test),
            "strata": {key: {"items": sizes[key], "test": take[key],
                             "inclusion_probability": round(take[key] / sizes[key], 4)} for key in sizes},
            "test": test, "train": [r["item_id"] for r in rows if r["item_id"] not in held]}


# ── the report's evidence, and the answers back ────────────────────────────────────────────────────────────


def votes_line(row: dict) -> str:
    """The raters' votes in one line: 'safe (majority) · 54 unsafe · 61 safe · 8 unsure'."""
    c = row["counts"]
    head = f"{row['label']} (majority)" if row["label"] else "no majority"
    return f"{head} · {c.get(POSITIVE, 0)} unsafe · {c.get(NEGATIVE, 0)} safe · {c.get(UNSURE, 0)} unsure"


def gap_line(sig: dict) -> str:
    """The largest group gap in one line: 'rater_gender Woman 58% unsafe · the rest 30% (z 3.1)'."""
    g = sig.get("gap")
    if not g:
        return ""
    return f"{g['field']} {g['level']} {g['share']:.0%} unsafe · the rest {g['rest']:.0%} (z {g['z']})"


def evidence_row(item: dict, row: dict, *, role="case_a", show_label=True, sig: dict | None = None,
                 split="train") -> dict:
    """One evidence row of a decision report: the item's exact excerpt (its earlier turns as context, the judged
    reply as text), and its raters' signal unless the card is blind. A Test item is cited by reference only."""
    if split == "test":
        return {"item_ref": str(item["item_id"]), "split": "test", "role": role, "context": "", "text": "",
                "signal": ""}
    signal = ""
    if show_label:
        signal = votes_line(row) + (f" · {gap_line(sig)}" if sig and sig.get("gap") else "")
    return {"item_ref": str(item["item_id"]), "split": "train", "role": role,
            "context": item.get("context_before") or "", "text": item.get("main") or "", "signal": signal}


def apply_answers(legacy_rows, report: dict, answers: dict, *, version="l01", run="r04") -> dict:
    """The reviewed labels a person's answers make, from the existing labels (l00).

    Chat cards (reference_label) act on their case_a item: keep → reviewed; flip → the other label, citing the card;
    change_rule → kept, pending the rule; defer → deferred; custom → kept, the person's own words attached.
    Blind cards (diagnostic) only fill the item's blind judgment. Rule cards (define_rule) change no label; their
    answers are returned under "rules" for Update to write into the guideline. An unanswered card changes nothing.
    """
    labels = {r["item_id"]: {"item_id": r["item_id"], "label": r["label"], "from": r["label"],
                             "status": "unreviewed", "cites": None, "note": "", "blind": None}
              for r in legacy_rows}
    rules, changes = {}, []
    for index, card in enumerate(report["cards"], 1):
        answer = answers.get(card["decision_id"]) or {"kind": "unanswered"}
        kind, option = answer.get("kind"), answer.get("option_id")
        cite = f"{run} Q{index}"
        case = next((row["item_ref"] for row in card["evidence"] if row["role"] == "case_a"), None)
        if card["question_type"] == "define_rule":
            rules[card["decision_id"]] = {"answer": kind, "option": option, "text": answer.get("text"),
                                          "comment": answer.get("comment", ""), "cites": cite}
            continue
        if case is None or case not in labels or kind == "unanswered":
            continue
        rec = labels[case]
        if card["question_type"] == "diagnostic":
            if kind == "chosen":
                rec["blind"] = {"blind_unsafe": "unsafe", "blind_safe": "safe"}.get(option, "cant_tell")
            continue
        rec["cites"], rec["note"] = cite, answer.get("comment", "") or answer.get("text") or ""
        if kind == "chosen" and option == "keep":
            rec["status"] = "reviewed"
        elif kind == "chosen" and option == "flip":
            if rec["label"] is None:                   # no majority to flip: the card should offer set_unsafe/set_safe
                raise ValueError(f"{card['decision_id']}: 'flip' on {case}, whose raters have no majority; "
                                 "offer set_unsafe and set_safe on a tie")
            rec["label"] = {"unsafe": "safe", "safe": "unsafe"}[rec["label"]]
            rec["status"] = "corrected"
            changes.append({"item_id": case, "from": rec["from"], "to": rec["label"], "cites": cite})
        elif kind == "chosen" and option in ("set_unsafe", "set_safe"):
            rec["label"] = option.split("_", 1)[1]
            rec["status"] = "reviewed" if rec["label"] == rec["from"] else "corrected"
            if rec["status"] == "corrected":
                changes.append({"item_id": case, "from": rec["from"], "to": rec["label"], "cites": cite})
        elif kind == "chosen" and option == "change_rule":
            rec["status"] = "pending_rule"
        elif kind == "defer":
            rec["status"] = "deferred"
        elif kind == "custom":
            rec["status"] = "custom"
        else:
            rec["status"] = kind
    return {"version": version, "labels": [labels[k] for k in sorted(labels)], "changes": changes, "rules": rules}


# ── the score, against a hidden expert key (the score Task only; the meaning Task never calls this) ──────────


def _binom_cdf(k: int, n: int, p: float) -> float:
    return sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k + 1))


def clopper_pearson(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    """The exact two-sided confidence interval of a binomial proportion k/n, by bisection (no scipy)."""
    if n == 0:
        return (0.0, 1.0)

    def solve(f, lo=0.0, hi=1.0):
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if f(mid) else (lo, mid)
        return (lo + hi) / 2

    low = 0.0 if k == 0 else solve(lambda p: 1 - _binom_cdf(k - 1, n, p) < alpha / 2)
    high = 1.0 if k == n else solve(lambda p: _binom_cdf(k, n, p) > alpha / 2)
    return (round(low, 4), round(high, 4))


def _kappa(a: list, b: list) -> float | None:
    n = len(a)
    if n == 0:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(v) / n) * (b.count(v) / n) for v in set(a) | set(b))
    return round((po - pe) / (1 - pe), 3) if pe < 1 else None


CHANGED = ("corrected", "pending_rule", "custom")           # the person changed a label or a rule
ANSWERED = ("reviewed", *CHANGED)


def score(legacy_rows, train_ids, signal_rows, draws: dict, labels, expert: dict) -> dict:
    """The audit against an independent expert key: the raters' baseline, the flags' precision and recall, the
    person's corrections, the missed-issue estimate from the blind cards. Agreeing with the experts means agreeing with
    an independent standard; it never proves a rater was wrong.

    expert: {item_id: "unsafe" | "safe"}; labels: apply_answers' rows (l01); draws: draw()'s output."""
    c = {r["item_id"]: r["label"] for r in legacy_rows}
    have = sorted(i for i in c if c[i] is not None and i in expert)
    sig = {s["item_id"]: s for s in signal_rows}
    T = [i for i in sorted(set(map(str, train_ids))) if c.get(i) is not None and i in expert]
    d = {i: c[i] != expert[i] for i in T}
    F = [i for i in T if sig[i]["flagged"]]
    U = [i for i in T if not sig[i]["flagged"]]
    strata = defaultdict(list)
    for i in F:
        strata[sig[i]["stratum"]].append(i)
    lab = {r["item_id"]: r for r in labels}
    hard = [i for i in draws["sets"]["hard"] if i in lab]
    answered = [i for i in hard if lab[i]["status"] in ANSWERED and i in expert]
    toward = sum(1 for i in answered if lab[i]["label"] != c[i] and lab[i]["label"] == expert[i])
    away = sum(1 for i in answered if lab[i]["label"] != c[i] and c[i] == expert[i])
    person_precision = 0.0
    for key, ids in strata.items():
        drawn = [i for i in answered if sig[i]["stratum"] == key]
        if drawn:
            person_precision += len(ids) / len(F) * sum(lab[i]["status"] in CHANGED for i in drawn) / len(drawn)
    blind = [i for i in draws["sets"]["blind"] if i in lab and lab[i]["blind"] in ("unsafe", "safe")]
    k = sum(1 for i in blind if lab[i]["blind"] != c[i])
    low, high = clopper_pearson(k, len(blind))
    missed = sum(d[i] for i in U)
    return {
        "raters_baseline": {"items": len(have), "agreement": round(sum(c[i] == expert[i] for i in have) / len(have), 3)
                            if have else None, "kappa": _kappa([c[i] for i in have], [expert[i] for i in have])},
        "train": {"items": len(T), "disagree_with_experts": sum(d.values()),
                  "base_rate": round(sum(d.values()) / len(T), 3) if T else None},
        "flags": {"flagged": len(F),
                  "precision": round(sum(d[i] for i in F) / len(F), 3) if F else None,
                  "lift": round((sum(d[i] for i in F) / len(F)) / (sum(d.values()) / len(T)), 2)
                  if F and T and sum(d.values()) else None,
                  "recall": round(sum(d[i] for i in F) / sum(d.values()), 3) if sum(d.values()) else None,
                  "by_stratum": {key: {"flagged": len(ids), "disagree": sum(d[i] for i in ids)}
                                 for key, ids in sorted(strata.items())}},
        "person": {"hard_cards": len(hard), "answered": len(answered),
                   "statuses": dict(Counter(lab[i]["status"] for i in hard)),
                   "toward_experts": toward, "away_from_experts": away,
                   "paired_agreement": {"raters": round(sum(c[i] == expert[i] for i in answered) / len(answered), 3)
                                        if answered else None,
                                        "reviewed": round(sum(lab[i]["label"] == expert[i] for i in answered)
                                                          / len(answered), 3) if answered else None},
                   "flag_precision_person": round(person_precision, 3) if answered else None},
        "missed": {"unflagged": len(U), "blind_judged": len(blind), "blind_differs": k,
                   "estimate": round(len(U) * k / len(blind), 1) if blind else None,
                   "estimate_ci95": [round(len(U) * low, 1), round(len(U) * high, 1)] if blind else None,
                   "vs_experts": missed},
    }


def score_markdown(result: dict, *, title: str = "Label quality") -> str:
    """The label-quality report: totals only (per-item rows stay in the store until the last loop)."""
    b, tr, f, p, m = (result[k] for k in ("raters_baseline", "train", "flags", "person", "missed"))
    lines = [f"# {title}", "",
             f"- Raters' majority vs the experts: {b['agreement']} agreement over {b['items']} chats (kappa {b['kappa']}).",
             f"- Train: {tr['items']} chats; the raters and the experts differ on {tr['disagree_with_experts']} "
             f"({tr['base_rate']}).",
             f"- Flags: {f['flagged']} flagged; precision {f['precision']} (lift {f['lift']}), recall {f['recall']}.",
             f"- Your answers: {p['answered']} of {p['hard_cards']} hard cards answered; {p['toward_experts']} labels "
             f"moved toward the experts, {p['away_from_experts']} away.",
             f"- Missed issues: {m['blind_differs']} of {m['blind_judged']} blind cards differ from the raters; "
             f"about {m['estimate']} of {m['unflagged']} unflagged chats (95% CI {m['estimate_ci95']}); "
             f"the experts differ on {m['vs_experts']} of them.", "",
             "Agreeing with the experts means agreeing with an independent standard; it does not prove a rater was "
             "wrong.", ""]
    return "\n".join(lines)


# ── a quick profile, to check a run against t02's numbers ──────────────────────────────────────────────────


def profile(legacy_rows) -> dict:
    """Majority counts, mean Unsure share and the 40-60% split count, as t02's profile reports them."""
    rows = list(legacy_rows)
    major = Counter(r["majority"] for r in rows)
    shares = [r["unsure_share"] for r in rows if r["unsure_share"] is not None]
    split = sum(1 for r in rows if r["unsafe_share"] is not None and 0.4 <= r["unsafe_share"] <= 0.6)
    return {"items": len(rows), "majority": dict(sorted(major.items())),
            "unsure_share_mean": round(sum(shares) / len(shares), 3) if shares else None, "split_40_60": split}


# ── CLI ─────────────────────────────────────────────────────────────────────────────────────────────────────


def _read_jsonl(path: Path):
    with Path(path).open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def _write_jsonl(path: Path, rows) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            n += 1
    return n


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("legacy", help="per-item existing labels (l00) from the raters' file only")
    a.add_argument("--raters", type=Path, required=True)
    a.add_argument("--answer", default="Q_overall")
    a.add_argument("--groups", default="")
    a.add_argument("--out", type=Path, required=True)
    a.add_argument("--check", action="store_true", help="print the profile only; write nothing")
    b = sub.add_parser("draw", help="signals for every item, then the three Train samples")
    b.add_argument("--legacy", type=Path, required=True)
    b.add_argument("--split", type=Path, required=True, help="split.json with 'train' and 'test' id lists")
    b.add_argument("--seed", type=int, default=261101)
    b.add_argument("--n-hard", type=int, default=12)
    b.add_argument("--n-blind", type=int, default=4)
    b.add_argument("--n-typical", type=int, default=40)
    b.add_argument("--out-dir", type=Path, required=True)
    b.add_argument("--check", action="store_true", help="print the counts only; write nothing")
    args = ap.parse_args(argv)
    if args.cmd == "legacy":
        groups = [g for g in args.groups.split(",") if g]
        votes = legacy_votes(_read_jsonl(args.raters), answer=args.answer, groups=groups)
        rows = [legacy_row(item_id, votes[item_id]) for item_id in sorted(votes)]
        print(json.dumps(profile(rows)))
        if not args.check:
            print(_write_jsonl(args.out, rows), "rows ->", args.out)
        return
    legacy = list(_read_jsonl(args.legacy))
    split = json.loads(args.split.read_text(encoding="utf-8"))
    sigs = [signals(r) for r in legacy]
    drawn = draw(sigs, split["train"], n_hard=args.n_hard, n_blind=args.n_blind, n_typical=args.n_typical,
                 seed=args.seed)
    drawn["cutoffs"] = {**DEFAULTS, "split": list(DEFAULTS["split"])}
    print(json.dumps({k: drawn[k] for k in ("train", "flagged", "unflagged", "strata")}))
    if not args.check:
        _write_jsonl(args.out_dir / "signals.jsonl", sigs)
        (args.out_dir / "draws.json").write_text(json.dumps(drawn, indent=1) + "\n", encoding="utf-8")
        print("signals.jsonl, draws.json ->", args.out_dir)


if __name__ == "__main__":
    main()
