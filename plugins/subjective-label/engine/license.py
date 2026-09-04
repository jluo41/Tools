"""Autonomy-license assessment (S6, deterministic core).

The engine earns the right to run autonomously on constructs with NO human labels
by first reaching the HUMAN CEILING on a battery of public per-rater datasets
(junjie P02: DICES / POPQuorn / GoEmotions / LeWiDi) on THEIR native constructs.
This is where human ground truth lives — once, externally, amortized (F1/F2/F3).

THIS file is the deterministic scorer: given the engine's predictions on a public
dataset + that dataset's per-rater human labels (projected to the construct's
label set), compute the human ceiling (Krippendorff α among raters) and the
agent-vs-consensus agreement, and issue PASS / BELOW.

Downloading the datasets + running the engine + projecting labels is orchestration
(label-evaluate); it is network/compute-heavy and run when a license is established.

Usage:
    python engine/license.py assess --agent agent.jsonl --raters raters.jsonl \
                                 --labels HIGH,LOW,NONE --type categorical [--eps 0.0]
    python engine/license.py selftest

Inputs (jsonl):
    agent:  {"item_id": "...", "pred": "<label>"}
    raters: {"item_id": "...", "ratings": ["<label>", "<label>", ...]}   # per-rater, projected
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kappa import cohen_kappa, weighted_kappa, krippendorff_alpha  # noqa: E402


def consensus(ratings, labels, none_value=None, tie_break="first"):
    votes = [r for r in ratings if r in labels]
    if not votes:
        return None
    top = Counter(votes).most_common()
    best = top[0][0]
    if len(top) > 1 and top[0][1] == top[1][1] and tie_break == "none_loses" and none_value:
        nn = [l for l, _ in top if l != none_value]
        best = nn[0] if nn else none_value
    return best


def assess(agent, raters, labels, ltype="categorical", eps=0.0):
    """agent: {item_id: pred}. raters: {item_id: [labels]}. Returns verdict dict."""
    items = [i for i in raters if i in agent]
    units = [raters[i] for i in items]
    level = "interval" if ltype == "ordinal" else "nominal"
    ceiling = krippendorff_alpha(units, labels, level)

    cons = {i: consensus(raters[i], labels) for i in items}
    a = [agent[i] for i in items if cons[i] is not None]
    c = [cons[i] for i in items if cons[i] is not None]
    agent_kappa = weighted_kappa(a, c, labels) if ltype == "ordinal" else cohen_kappa(a, c, labels)

    if ceiling is None or agent_kappa is None:
        verdict = "INSUFFICIENT_DATA"
    elif agent_kappa >= ceiling - eps:
        verdict = "PASS"
    else:
        verdict = "BELOW_CEILING"
    return {"n_items": len(items), "type": ltype,
            "human_ceiling_krippendorff": ceiling,
            "agent_vs_consensus_kappa": agent_kappa,
            "gap": (round(agent_kappa - ceiling, 4) if (ceiling is not None and agent_kappa is not None) else None),
            "verdict": verdict,
            "note": "PASS = engine reaches human agreement on this construct → licenses autonomy on adjacent constructs"}


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("assess")
    p.add_argument("--agent", required=True)
    p.add_argument("--raters", required=True)
    p.add_argument("--labels", required=True)
    p.add_argument("--type", default="categorical", choices=["categorical", "ordinal"])
    p.add_argument("--eps", type=float, default=0.0)
    sub.add_parser("selftest")
    args = ap.parse_args()

    if args.cmd == "selftest":
        return _selftest()

    agent = {json.loads(l)["item_id"]: json.loads(l)["pred"]
             for l in Path(args.agent).read_text().splitlines() if l.strip()}
    raters = {json.loads(l)["item_id"]: json.loads(l)["ratings"]
              for l in Path(args.raters).read_text().splitlines() if l.strip()}
    labels = [x.strip() for x in args.labels.split(",")]
    print(json.dumps(assess(agent, raters, labels, args.type, args.eps), indent=2, ensure_ascii=False))


def _selftest():
    import random
    rng = random.Random(0)
    L = ["POS", "NEG", "NEU"]
    raters, agent_good, agent_bad = {}, {}, {}
    for i in range(60):
        true = rng.choice(L)
        # noisy humans: 3 raters, each ~75% on `true` → a realistic sub-perfect ceiling
        raters[f"i{i}"] = [true if rng.random() < .75 else rng.choice(L) for _ in range(3)]
        cons = Counter(raters[f"i{i}"]).most_common(1)[0][0]
        agent_good[f"i{i}"] = cons if rng.random() < .85 else rng.choice(L)   # tracks consensus
        agent_bad[f"i{i}"] = rng.choice(L)                                    # random
    good = assess(agent_good, raters, L)
    bad = assess(agent_bad, raters, L)
    assert good["verdict"] == "PASS", good
    assert bad["verdict"] == "BELOW_CEILING", bad
    assert good["agent_vs_consensus_kappa"] > bad["agent_vs_consensus_kappa"]
    print(f"selftest OK: ceiling={good['human_ceiling_krippendorff']} · "
          f"good agent κ={good['agent_vs_consensus_kappa']} PASS · "
          f"random agent κ={bad['agent_vs_consensus_kappa']} BELOW")


if __name__ == "__main__":
    main()
