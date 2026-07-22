"""Base-rate probe + enriched sampling (S5, deterministic core).

Generalizes junjie's `probe_base_rate.py` + `sample_candidates.py` from a
hardcoded openness lexicon to a **construct-driven** one: the probe/confound
regexes are INPUTS (a lexicon produced by an LLM from `construct.definition` +
`discriminant_from` — the judgment layer, orchestrated in the skill). THIS file
only applies them: estimate prevalence, and draw an enriched sample with a random
NONE quota so a rare construct still yields HIGH/LOW candidates AND its
false-positive rate on the silent majority stays measurable.

Why enriched-with-none-quota (not pure random): a construct firing on ~5% of the
corpus gives a random anchor ~95% NONE — too few positives to estimate per-label
quality. Enrich to see positives; keep a random NONE quota so over-firing on the
95% is still measured. ALWAYS report base rate alongside any κ.

Usage:
    python lib/sample.py probe  --corpus c.jsonl --lexicon lex.json
    python lib/sample.py sample --corpus c.jsonl --lexicon lex.json --confounds conf.json \
                                --per-stratum 8 --none-quota 0.33 --out batch.jsonl [--exclude ids.txt] [--seed 42]
    python lib/sample.py selftest

Inputs: lexicon.json = {stratum: regex, ...}   confounds.json = {sibling: regex, ...}
        (both LLM-generated per construct; nothing hardcoded here)
"""

import argparse
import json
import random
import re
from collections import Counter
from pathlib import Path


def _corpus(path, text_field="text"):
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]


def base_rate(rows, lexicon, text_field="text"):
    comp = {k: re.compile(v, re.I) for k, v in lexicon.items()}
    hits = Counter(); any_hit = 0; examples = {k: [] for k in lexicon}
    for r in rows:
        t = r.get(text_field, "")
        fired = [k for k, rx in comp.items() if rx.search(t)]
        for k in fired:
            hits[k] += 1
            if len(examples[k]) < 3:
                examples[k].append({"id": r.get("id"), "text": t[:200]})
        if fired:
            any_hit += 1
    n = len(rows)
    return {"n": n, "any_hit": any_hit, "any_hit_rate": round(any_hit / n, 4) if n else 0.0,
            "no_hit_rate": round((n - any_hit) / n, 4) if n else 0.0,
            "per_stratum": {k: {"n": hits[k], "pct": round(100 * hits[k] / n, 2) if n else 0.0}
                            for k in lexicon},
            "examples": examples}


def sample(rows, lexicon, confounds, per_stratum=8, none_quota=0.33,
           text_field="text", max_len=900, exclude=None, seed=42):
    """Enriched: per probe stratum + per confound stratum + a random NONE quota.
    Probe strata take precedence over confound strata (an item that fires a probe
    is a probe candidate, not a confound). Returns items tagged with `stratum`."""
    rng = random.Random(seed)
    exclude = set(exclude or [])
    probe = {k: re.compile(v, re.I) for k, v in lexicon.items()}
    conf = {k: re.compile(v, re.I) for k, v in (confounds or {}).items()}
    strata = {k: [] for k in list(lexicon) + [f"confound:{c}" for c in (confounds or {})] + ["none_quota"]}

    for r in rows:
        if r.get("id") in exclude:
            continue
        t = r.get(text_field, "")
        if len(t) > max_len:
            continue
        probe_hit = [k for k, rx in probe.items() if rx.search(t)]
        if probe_hit:
            for k in probe_hit:
                strata[k].append(r)
            continue                       # probe precedence
        conf_hit = next((c for c, rx in conf.items() if rx.search(t)), None)
        if conf_hit:
            strata[f"confound:{conf_hit}"].append(r)
        else:
            strata["none_quota"].append(r)

    picked, seen = [], set()
    # probe + confound strata: per_stratum each
    for name in [k for k in strata if name_is_signal(k)]:
        pool = strata[name]; rng.shuffle(pool)
        for r in pool[:per_stratum]:
            if r.get("id") not in seen:
                seen.add(r.get("id")); picked.append({**r, "stratum": name})
    # random NONE quota
    n_none = max(1, round(none_quota * len(picked) / (1 - none_quota))) if none_quota < 1 else 0
    npool = strata["none_quota"]; rng.shuffle(npool)
    for r in npool[:n_none]:
        if r.get("id") not in seen:
            seen.add(r.get("id")); picked.append({**r, "stratum": "none_quota"})
    return picked


def name_is_signal(name):
    return name != "none_quota"


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for c in ("probe", "sample"):
        p = sub.add_parser(c)
        p.add_argument("--corpus", required=True)
        p.add_argument("--lexicon", required=True)
        p.add_argument("--text-field", default="text")
        if c == "sample":
            p.add_argument("--confounds", default=None)
            p.add_argument("--per-stratum", type=int, default=8)
            p.add_argument("--none-quota", type=float, default=0.33)
            p.add_argument("--exclude", default=None)
            p.add_argument("--seed", type=int, default=42)
            p.add_argument("--out", default=None)
    sub.add_parser("selftest")
    args = ap.parse_args()

    if args.cmd == "selftest":
        return _selftest()

    rows = _corpus(args.corpus, args.text_field)
    lexicon = json.loads(Path(args.lexicon).read_text())
    if args.cmd == "probe":
        print(json.dumps(base_rate(rows, lexicon, args.text_field), indent=2, ensure_ascii=False))
    else:
        confounds = json.loads(Path(args.confounds).read_text()) if args.confounds else {}
        exclude = Path(args.exclude).read_text().split() if args.exclude else None
        picked = sample(rows, lexicon, confounds, args.per_stratum, args.none_quota,
                        args.text_field, exclude=exclude, seed=args.seed)
        by = Counter(p["stratum"] for p in picked)
        print(f"sampled {len(picked)} — by stratum: {dict(by)}")
        if args.out:
            Path(args.out).write_text("".join(json.dumps(p, ensure_ascii=False) + "\n" for p in picked))
            print(f"wrote {args.out}")


def _selftest():
    # synthetic corpus: 100 items; 10 fire "curiosity", 8 fire "warmth"(confound), rest silent
    rows = []
    for i in range(100):
        if i < 10:
            t = "the doctor was open to new ideas and curious"
        elif i < 18:
            t = "the doctor listened and was warm"
        else:
            t = "long wait at the front desk billing"
        rows.append({"id": f"i{i}", "text": t})
    lex = {"curiosity": r"curious|open to new"}
    conf = {"agreeableness": r"warm|listened"}
    br = base_rate(rows, lex)
    assert br["per_stratum"]["curiosity"]["n"] == 10, br
    assert br["any_hit_rate"] == 0.1, br
    s = sample(rows, lex, conf, per_stratum=5, none_quota=0.5, seed=1)
    by = Counter(p["stratum"] for p in s)
    assert by["curiosity"] == 5, by                 # per_stratum honored
    assert by["confound:agreeableness"] == 5, by    # confound stratum present
    assert by["none_quota"] >= 1, by                # NONE quota injected
    assert len({p["id"] for p in s}) == len(s), "deduped"
    print(f"selftest OK: base_rate curiosity=10% · enriched strata {dict(by)}")


if __name__ == "__main__":
    main()
