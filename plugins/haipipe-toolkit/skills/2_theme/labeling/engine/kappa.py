"""Generic agreement metrics for the subjective-label engine (canonical; S0).

Metric family is chosen by `labels.type` (categorical | ordinal) — the engine is
NOT frozen to tri-polar Cohen's κ. Ported from the per-task `compute_kappa.py`
(B01–B03) and generalized.

  categorical : Cohen κ (2 raters) / Fleiss κ (>2) · accuracy · per-label P/R/F1 · confusion
  ordinal     : quadratic weighted κ (primary) · Spearman ρ · MAE · + categorical set
  inter-annot : Krippendorff α (nominal for categorical, interval for ordinal)

Usage:
    python engine/kappa.py --project-dir <task> --version v04                 # reads config labels
    python engine/kappa.py --project-dir <task> --version v04 --labels HIGH,LOW,NONE --type categorical
    python engine/kappa.py --selftest                                         # metric sanity checks

Reads:  <project>/eval/anchor_set.jsonl (gold) + eval/per_version/<version>_<engine>_results.jsonl
Writes: <project>/eval/trajectory.jsonl (one row per version, natural version order)

Failed predictions (PARSE_ERROR, ERROR, UNRESOLVED, null, missing, off-set) are never
silently dropped: every `kappa_*` / `acc_*` over scored items carries `n_scored_*` and
`n_failed_*`, and `kappa_all_*` / `acc_all_*` score every gold item with a failure as
its own category that never matches gold.
"""

import argparse
import json
import re
from collections import Counter
from pathlib import Path

import numpy as np

FAILED = "__FAILED__"      # stand-in category for a failed prediction in *_all metrics
UNRESOLVED = "UNRESOLVED"  # majority with no valid vote; a disposition, never NONE


def version_key(version):
    """Natural sort key: v2 < v9 < v10 (not the string order v10 < v2)."""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", str(version))]


# ── config ──────────────────────────────────────────────────────────────────

def _read_config(project_dir: Path) -> dict:
    import yaml  # noqa: PLC0415
    p = project_dir / "config.yaml"
    return (yaml.safe_load(p.read_text(encoding="utf-8")) or {}) if p.exists() else {}


# ── metrics ───────────────────────────────────────────────────────────────--

def cohen_kappa(a, b, labels):
    pairs = [(x, y) for x, y in zip(a, b) if x in labels and y in labels]
    n = len(pairs)
    if not n:
        return None
    po = sum(1 for x, y in pairs if x == y) / n
    ca, cb = Counter(x for x, _ in pairs), Counter(y for _, y in pairs)
    pe = sum((ca[l] / n) * (cb[l] / n) for l in labels)
    return round((po - pe) / (1 - pe), 4) if abs(1 - pe) > 1e-12 else (1.0 if po == 1 else 0.0)


def weighted_kappa(a, b, labels):
    """Quadratic weighted κ; `labels` is the ORDERED value list."""
    idx = {l: i for i, l in enumerate(labels)}
    pairs = [(idx[x], idx[y]) for x, y in zip(a, b) if x in idx and y in idx]
    n = len(pairs)
    k = len(labels)
    if not n or k < 2:
        return None
    O = np.zeros((k, k))
    for x, y in pairs:
        O[x, y] += 1
    ra = O.sum(axis=1)
    rb = O.sum(axis=0)
    E = np.outer(ra, rb) / n
    W = np.array([[((i - j) / (k - 1)) ** 2 for j in range(k)] for i in range(k)])
    denom = (W * E).sum()
    return round(1 - (W * O).sum() / denom, 4) if denom > 1e-12 else (1.0 if (W * O).sum() == 0 else 0.0)


def _avg_ranks(vals):
    order = np.argsort(vals, kind="mergesort")
    ranks = np.empty(len(vals), float)
    i = 0
    while i < len(vals):
        j = i
        while j + 1 < len(vals) and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2.0 + 1
        i = j + 1
    return ranks


def spearman(a, b, labels):
    idx = {l: i for i, l in enumerate(labels)}
    xs = np.array([idx[x] for x, y in zip(a, b) if x in idx and y in idx], float)
    ys = np.array([idx[y] for x, y in zip(a, b) if x in idx and y in idx], float)
    if len(xs) < 2:
        return None
    rx, ry = _avg_ranks(xs), _avg_ranks(ys)
    if rx.std() < 1e-12 or ry.std() < 1e-12:
        return None
    return round(float(np.corrcoef(rx, ry)[0, 1]), 4)


def mae(a, b, labels):
    idx = {l: i for i, l in enumerate(labels)}
    d = [abs(idx[x] - idx[y]) for x, y in zip(a, b) if x in idx and y in idx]
    return round(sum(d) / len(d), 4) if d else None


def per_label_prf(pred, gold, labels):
    stats = {}
    for l in labels:
        tp = sum(1 for i in gold if gold[i] == l and pred.get(i) == l)
        fp = sum(1 for i in gold if pred.get(i) == l and gold[i] != l)
        fn = sum(1 for i in gold if gold[i] == l and pred.get(i) != l)
        prec = tp / (tp + fp) if (tp + fp) else None
        rec = tp / (tp + fn) if (tp + fn) else None
        if tp == 0:
            f1 = 0.0 if (fp + fn) else None   # predicted or gold, never hit → 0.0
        else:
            f1 = 2 * prec * rec / (prec + rec)
        stats[l] = {"n_gold": sum(1 for i in gold if gold[i] == l),
                    "precision": round(prec, 3) if prec is not None else None,
                    "recall": round(rec, 3) if rec is not None else None,
                    "f1": round(f1, 3) if f1 is not None else None}
    return stats


def _weighted_kappa_all(a, b, labels):
    """Quadratic weighted κ where FAILED is an extra category at maximal distance (1.0)
    from every label; equals weighted_kappa when nothing failed."""
    k = len(labels)
    idx = {l: i for i, l in enumerate(labels)}
    idx[FAILED] = k
    pairs = [(idx[x], idx[y]) for x, y in zip(a, b) if x in idx and y in idx]
    n = len(pairs)
    if not n or k < 2:
        return None
    O = np.zeros((k + 1, k + 1))
    for x, y in pairs:
        O[x, y] += 1
    E = np.outer(O.sum(axis=1), O.sum(axis=0)) / n
    W = np.ones((k + 1, k + 1))
    W[:k, :k] = [[((i - j) / (k - 1)) ** 2 for j in range(k)] for i in range(k)]
    W[k, k] = 0.0
    denom = (W * E).sum()
    return round(1 - (W * O).sum() / denom, 4) if denom > 1e-12 else (1.0 if (W * O).sum() == 0 else 0.0)


def score_vs_gold(pred, gold, labels, ltype="categorical"):
    """pred/gold: {item: label}. Returns metrics over scored items (pred in labels) with
    n_scored/n_failed, plus kappa_all/acc_all over every gold item (failure = wrong)."""
    ids = [i for i in gold if gold[i] in labels]
    scored = [i for i in ids if pred.get(i) in labels]
    pl, gl = [pred[i] for i in scored], [gold[i] for i in scored]
    pa = [pred.get(i) if pred.get(i) in labels else FAILED for i in ids]
    ga = [gold[i] for i in ids]
    out = {"n_scored": len(scored), "n_failed": len(ids) - len(scored)}
    if ltype == "ordinal":
        out["kappa"] = weighted_kappa(pl, gl, labels)
        out["kappa_all"] = _weighted_kappa_all(pa, ga, labels)
    else:
        out["kappa"] = cohen_kappa(pl, gl, labels)
        out["kappa_all"] = cohen_kappa(pa, ga, list(labels) + [FAILED])
    out["acc"] = round(sum(x == y for x, y in zip(pl, gl)) / len(pl), 3) if pl else None
    out["acc_all"] = round(sum(x == y for x, y in zip(pa, ga)) / len(ids), 3) if ids else None
    if ltype == "ordinal":
        out["spearman"] = spearman(pl, gl, labels)
        out["mae"] = mae(pl, gl, labels)
    return out


def fleiss_kappa(rows, labels):
    """rows: list of per-item label lists (≥2 raters each). Categorical."""
    k = len(labels); idx = {l: i for i, l in enumerate(labels)}
    M = []
    for r in rows:
        counts = [0] * k
        for v in r:
            if v in idx:
                counts[idx[v]] += 1
        if sum(counts) >= 2:
            M.append(counts)
    if not M:
        return None
    M = np.array(M, float)
    n = M.sum(axis=1)
    P = ((M ** 2).sum(axis=1) - n) / (n * (n - 1))
    Pbar = P.mean()
    p = M.sum(axis=0) / M.sum()
    Pe = (p ** 2).sum()
    return round((Pbar - Pe) / (1 - Pe), 4) if abs(1 - Pe) > 1e-12 else (1.0 if Pbar == 1 else 0.0)


def krippendorff_alpha(units, labels, level="nominal"):
    """units: list of per-item label lists (missing allowed). level: nominal|interval."""
    idx = {l: i for i, l in enumerate(labels)}
    units = [[idx[v] for v in u if v in idx] for u in units]
    units = [u for u in units if len(u) >= 2]
    if not units:
        return None

    def dist(i, j):
        return 0.0 if i == j else (1.0 if level == "nominal" else float((i - j) ** 2))

    Do_num = Do_den = 0.0
    all_vals = []
    for u in units:
        m = len(u)
        for a in range(m):
            for b in range(m):
                if a != b:
                    Do_num += dist(u[a], u[b]) / (m - 1)
        Do_den += m
        all_vals.extend(u)
    Do = Do_num / Do_den if Do_den else 0.0
    N = len(all_vals)
    De_num = sum(dist(all_vals[a], all_vals[b]) for a in range(N) for b in range(N) if a != b)
    De = De_num / (N * (N - 1)) if N > 1 else 0.0
    return round(1 - Do / De, 4) if De > 1e-12 else (1.0 if Do == 0 else 0.0)


# ── driver ────────────────────────────────────────────────────────────────--

def load_preds(pv_dir, version, engine):
    p = pv_dir / f"{version}_{engine}_results.jsonl"
    if not p.exists():
        return None
    rows = [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
    return {r["anchor_idx"]: r["pred"] for r in rows}


def majority(dicts, labels, none_value, tie_break):
    out, idxs = {}, set()
    for d in dicts:
        if d:
            idxs |= set(d)
    for i in sorted(idxs):
        votes = [d[i] for d in dicts if d and d.get(i) in labels]
        if not votes:
            out[i] = UNRESOLVED   # no valid label from any engine: never NONE
            continue
        top = Counter(votes).most_common()
        best = top[0][0]
        if len(top) > 1 and top[0][1] == top[1][1]:  # tie
            if tie_break == "none_loses" and none_value:
                nn = [l for l, _ in top if l != none_value]
                best = nn[0] if nn else none_value
            else:
                best = top[0][0]
        out[i] = best
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-dir", type=Path)
    ap.add_argument("--version", default="v01")
    ap.add_argument("--labels", default=None)
    ap.add_argument("--type", default=None, choices=["categorical", "ordinal"])
    ap.add_argument("--engines", default="claude_sdk,codex")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("cmd", nargs="?", help="'selftest' (or use --selftest)")
    args = ap.parse_args()

    if args.selftest or args.cmd == "selftest":
        return _selftest()

    if args.project_dir is None:
        ap.error("--project-dir is required (or run: kappa.py selftest)")
    pd = args.project_dir.resolve()
    cfg = _read_config(pd)
    lc = cfg.get("labels") or {}
    labels = ([x.strip() for x in args.labels.split(",")] if args.labels else [str(x) for x in lc.get("values", [])])
    if not labels:
        raise SystemExit("no labels: add labels.values to config or pass --labels")
    ltype = args.type or lc.get("type", "categorical")
    none_value = lc.get("none_value")
    if none_value is None and "NONE" in labels:
        none_value = "NONE"
    tie_break = lc.get("tie_break") or ("none_loses" if none_value else "first")
    engines = [e.strip() for e in args.engines.split(",") if e.strip()]

    anchor = [json.loads(l) for l in (pd / "eval" / "anchor_set.jsonl").read_text().splitlines() if l.strip()]
    gold = {r["anchor_idx"]: (r.get("gold") or "").upper() for r in anchor if r.get("gold")}
    gold = {i: g for i, g in gold.items() if g in [l.upper() for l in labels]}
    # normalize gold case to label casing
    up2lab = {l.upper(): l for l in labels}
    gold = {i: up2lab[g] for i, g in gold.items()}
    idxs = sorted({r["anchor_idx"] for r in anchor})

    pv = pd / "eval" / "per_version"
    preds = {e: load_preds(pv, args.version, e) for e in engines}
    preds = {e: d for e, d in preds.items() if d}

    def primary(a, b):
        return weighted_kappa(a, b, labels) if ltype == "ordinal" else cohen_kappa(a, b, labels)

    report = {"version": args.version, "type": ltype, "labels": labels,
              "n_anchor": len(idxs), "n_gold": len(gold)}

    # panel-internal (reliability) over the first two engines
    if len(preds) >= 2:
        e1, e2 = engines[0], engines[1]
        la = [preds[e1].get(i) for i in idxs]; lb = [preds[e2].get(i) for i in idxs]
        report["panel_kappa"] = primary(la, lb)
        report[f"panel_kappa_{e1}_vs_{e2}"] = report["panel_kappa"]
        report["panel_n_scored"] = sum(1 for x, y in zip(la, lb) if x in labels and y in labels)
        report["panel_n_failed"] = len(idxs) - report["panel_n_scored"]

    for e in preds:
        report[f"dist_{e}"] = dict(Counter(preds[e][i] for i in idxs if preds[e].get(i)))

    if gold:
        maj = majority(list(preds.values()), labels, none_value, tie_break)
        named = list(preds.items()) + [("majority", maj)]
        for name, d in named:
            s = score_vs_gold(d, gold, labels, ltype)
            for key in ("kappa", "acc", "n_scored", "n_failed", "kappa_all", "acc_all"):
                report[f"{key}_{name}_vs_gold"] = s[key]
            if ltype == "ordinal":
                report[f"spearman_{name}_vs_gold"] = s["spearman"]
                report[f"mae_{name}_vs_gold"] = s["mae"]
        # class metrics exclude UNRESOLVED / failed majority rows; counts reported beside
        maj_gold = {i: g for i, g in gold.items() if maj.get(i) in labels}
        report["per_label_majority"] = per_label_prf({i: maj[i] for i in maj_gold}, maj_gold, labels)
        report["per_label_majority_n_scored"] = len(maj_gold)
        report["per_label_majority_n_failed"] = len(gold) - len(maj_gold)
        report["n_unresolved_majority"] = sum(1 for v in maj.values() if v == UNRESOLVED)
        report["dist_gold"] = dict(Counter(gold.values()))
        # clarity (R3): executor-independence = strong vs weak model on the SAME guideline,
        # both vs gold. Smaller gap = guideline leans less on the strong model's priors (junjie P01).
        lab_cfg = cfg.get("labeler") or {}
        strong = lab_cfg.get("strong_engine") or ("codex" if "codex" in preds else None)
        weak = lab_cfg.get("weak_engine") or ("claude_sdk" if "claude_sdk" in preds else None)
        if strong and weak and strong != weak and strong in preds and weak in preds:
            ks = report.get(f"kappa_{strong}_vs_gold")
            kw = report.get(f"kappa_{weak}_vs_gold")
            if ks is not None and kw is not None:
                report["executor_independence"] = {
                    "strong": strong, "weak": weak,
                    "kappa_strong_vs_gold": ks, "kappa_weak_vs_gold": kw,
                    "gap": round(ks - kw, 4),
                    "ratio": round(kw / ks, 4) if ks else None,
                }
        # inter-annotator ceiling if the anchor carries ≥2 human columns
        acols = [r for r in anchor if isinstance(r.get("gold_annotators"), list)]
        if acols:
            units = [r["gold_annotators"] for r in acols]
            report["human_ceiling_krippendorff"] = krippendorff_alpha(
                units, labels, "interval" if ltype == "ordinal" else "nominal")
    else:
        report["note"] = "gold not filled — only reliability (panel) available"

    print(json.dumps(report, indent=2, ensure_ascii=False))

    traj = pd / "eval" / "trajectory.jsonl"
    rows = [json.loads(l) for l in traj.read_text().splitlines() if l.strip()] if traj.exists() else []
    rows = [r for r in rows if r.get("version") != args.version] + [report]
    rows.sort(key=lambda r: version_key(r["version"]))
    traj.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    print(f"\n→ trajectory updated: {traj}")


def _selftest():
    L = ["NONE", "LOW", "HIGH"]
    # perfect agreement
    a = ["HIGH", "LOW", "NONE", "HIGH"]
    assert cohen_kappa(a, a, L) == 1.0
    assert weighted_kappa(a, a, L) == 1.0
    assert krippendorff_alpha([["HIGH", "HIGH"], ["LOW", "LOW"]], L) == 1.0
    assert mae(a, a, L) == 0.0
    # off-by-one hurts weighted less than off-by-two
    b1 = ["LOW", "LOW", "NONE", "HIGH"]   # one adjacent error
    b2 = ["NONE", "LOW", "NONE", "HIGH"]  # one 2-step error
    assert weighted_kappa(a, b2, L) < weighted_kappa(a, b1, L)
    # ordinal weighted ≠ nominal cohen in general
    assert weighted_kappa(a, b1, L) != cohen_kappa(a, b1, L)
    # failures are counted, never silently dropped; no valid vote is UNRESOLVED
    s = score_vs_gold({1: "HIGH", 2: "PARSE_ERROR"}, {1: "HIGH", 2: "LOW"}, L)
    assert (s["n_scored"], s["n_failed"], s["acc"], s["acc_all"]) == (1, 1, 1.0, 0.5), s
    assert majority([{1: "ERROR"}], L, "NONE", "none_loses")[1] == UNRESOLVED
    assert sorted(["v10", "v2", "v9"], key=version_key) == ["v2", "v9", "v10"]
    print("selftest OK: cohen, weighted κ (ordinal penalty), krippendorff, mae, failures counted")


if __name__ == "__main__":
    main()
