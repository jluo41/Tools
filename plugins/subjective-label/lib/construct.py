"""Construct auto-selection engine (S2, deterministic core).

The MECHANICS of "pick the best operational construct against an objective":
given several candidate labelings of a shared sample (produced by multi-LLM
proposals executed via lib/label.py) + sibling-construct labelings, score each
candidate and select the winner. Also emits a DIVERGENCE report (items where the
candidates most disagree = the ambiguous region a guideline must pin down).

Judgment (proposing the candidate definitions) is LLM orchestration and lives in
the skill/agent layer; THIS file is pure computation so it is testable.

Objective kinds (config `objective.kind`):
  discriminance  : maximize distinctness from sibling constructs × informativeness
                   (works now, no external data)
  downstream     : maximize predictive validity for a target (PHI-gated; stub)
  dataset_match  : maximize agreement with a public labeled set (stub)

Degenerate guard: a labeling that is nearly constant (e.g. all-NONE) is trivially
"discriminant" but useless → score is multiplied by informativeness (normalized
label entropy), which is ~0 for a constant labeling.

Usage:
    python lib/construct.py score --candidates cand.jsonl --siblings sib.jsonl [--objective discriminance]
    python lib/construct.py selftest

Input files (jsonl, one object per line):
    candidates: {"candidate": "<id>", "labels": {"<item_id>": "<label>", ...}}
    siblings:   {"sibling":   "<id>", "labels": {"<item_id>": "<label>", ...}}
"""

import argparse
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np


def cramers_v(x, y):
    """Association between two aligned categorical sequences, in [0, 1]."""
    xs = [(a, b) for a, b in zip(x, y) if a is not None and b is not None]
    if len(xs) < 2:
        return None
    xa = sorted({a for a, _ in xs}); ya = sorted({b for _, b in xs})
    if len(xa) < 2 or len(ya) < 2:
        return 0.0  # one variable constant → no association
    xi = {v: i for i, v in enumerate(xa)}; yi = {v: i for i, v in enumerate(ya)}
    T = np.zeros((len(xa), len(ya)))
    for a, b in xs:
        T[xi[a], yi[b]] += 1
    n = T.sum()
    row = T.sum(1, keepdims=True); col = T.sum(0, keepdims=True)
    E = row @ col / n
    chi2 = float(((T - E) ** 2 / np.where(E == 0, 1, E)).sum())
    v = math.sqrt(chi2 / (n * (min(len(xa), len(ya)) - 1)))
    return round(min(v, 1.0), 4)


def informativeness(labels):
    """Normalized label entropy in [0, 1]; ~0 for a near-constant labeling."""
    vals = [v for v in labels if v is not None]
    if len(vals) < 2:
        return 0.0
    c = Counter(vals); n = len(vals); k = len(c)
    if k < 2:
        return 0.0
    H = -sum((cnt / n) * math.log(cnt / n) for cnt in c.values())
    return round(H / math.log(k), 4)  # divide by log(#distinct) → 1.0 if uniform over used labels


def score_candidates(candidates, siblings, objective="discriminance"):
    """candidates/siblings: {id: {item_id: label}}. Returns ranked list + divergence."""
    items = sorted({it for d in candidates.values() for it in d})
    rows = []
    for cid, clab in candidates.items():
        cseq = [clab.get(it) for it in items]
        info = informativeness(cseq)
        if objective == "discriminance":
            assoc = {sid: cramers_v(cseq, [slab.get(it) for it in items])
                     for sid, slab in siblings.items()}
            assoc = {s: v for s, v in assoc.items() if v is not None}
            max_assoc = max(assoc.values()) if assoc else 0.0
            discriminance = round(1 - max_assoc, 4)
            score = round(discriminance * info, 4)
            rows.append({"candidate": cid, "objective": "discriminance",
                         "discriminance": discriminance, "informativeness": info,
                         "nearest_sibling": (max(assoc, key=assoc.get) if assoc else None),
                         "sibling_assoc": assoc, "score": score,
                         "n_labeled": sum(v is not None for v in cseq)})
        else:
            rows.append({"candidate": cid, "objective": objective, "informativeness": info,
                         "score": None, "note": f"{objective} not implemented (S6/PHI)"})
    rows.sort(key=lambda r: (r["score"] is not None, r["score"] or -1), reverse=True)

    # divergence: per-item disagreement across candidates (distinct-label count)
    div = []
    for it in items:
        labs = [d.get(it) for d in candidates.values() if d.get(it) is not None]
        if labs:
            div.append({"item_id": it, "n_distinct": len(set(labs)),
                        "labels": dict(Counter(labs))})
    div.sort(key=lambda d: d["n_distinct"], reverse=True)
    return {"objective": objective, "ranked": rows,
            "selected": rows[0]["candidate"] if rows and rows[0].get("score") is not None else None,
            "divergence_top": div[:15]}


def _load(path):
    out = {}
    key = None
    for line in Path(path).read_text().splitlines():
        if not line.strip():
            continue
        o = json.loads(line)
        key = "candidate" if "candidate" in o else "sibling"
        out[o[key]] = {str(k): v for k, v in o["labels"].items()}
    return out


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    ps = sub.add_parser("score")
    ps.add_argument("--candidates", required=True)
    ps.add_argument("--siblings", default=None)
    ps.add_argument("--objective", default="discriminance")
    sub.add_parser("selftest")
    args = ap.parse_args()

    if args.cmd == "selftest":
        return _selftest()

    candidates = _load(args.candidates)
    siblings = _load(args.siblings) if args.siblings else {}
    print(json.dumps(score_candidates(candidates, siblings, args.objective), indent=2, ensure_ascii=False))


def _selftest():
    items = [f"i{n}" for n in range(30)]
    import random
    rng = random.Random(0)
    sib = {it: rng.choice(["A", "B", "C"]) for it in items}
    # REDUNDANT: copies sibling → high assoc → low discriminance
    redundant = {it: sib[it] for it in items}
    # DEGENERATE: near-constant → high discriminance but ~0 informativeness
    degenerate = {it: "X" for it in items}
    # GOOD: informative AND independent of sibling
    good = {it: rng.choice(["P", "Q", "R"]) for it in items}
    cands = {"redundant": redundant, "degenerate": degenerate, "good": good}
    res = score_candidates(cands, {"agreeableness": sib}, "discriminance")
    winner = res["selected"]
    sc = {r["candidate"]: r["score"] for r in res["ranked"]}
    assert winner == "good", f"expected 'good' to win, got {winner} ({sc})"
    assert sc["degenerate"] < sc["good"], "degenerate must be penalized by informativeness"
    assert sc["redundant"] < sc["good"], "redundant (high sibling assoc) must lose"
    assert res["divergence_top"], "divergence report present"
    print(f"selftest OK: selected='{winner}'  scores={sc}")


if __name__ == "__main__":
    main()
