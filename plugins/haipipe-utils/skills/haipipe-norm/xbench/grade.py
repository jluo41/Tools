"""
Grade one noun against its frozen corpus, cell by cell.

TWO WEIGHTINGS, BOTH, ALWAYS
================================================================================
    row     every logged event counts once. Common inputs dominate -- which is
            what a patient actually does. THE DEPLOYMENT QUESTION.
    dedup   every distinct input string counts once. The long tail dominates.
            THE VOCABULARY QUESTION.

They are not two views of one number; they disagree, and on describe-food they
disagree in OPPOSITE DIRECTIONS on two cells of the same run. Quoting one
without saying which is how a resolver looks better than it is. So grade() has
no switch: it always returns both.

They need two DIFFERENT SAMPLES. Deduplicating a row-weighted sample after the
fact leaves the common inputs in and reproduces the row-weighted number.
"""
import argparse
import json
import subprocess
from pathlib import Path

import pandas as pd

from . import score as _score


def _git_head(root) -> str:
    r = subprocess.run(["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
                       capture_output=True, text=True)
    return r.stdout.strip() or "unknown"


def grade(spec, gold: pd.DataFrame, out_dir, tag: str = "current",
          n: int = 600, full: bool = False, root=None, verbose: bool = True) -> dict:
    """Frozen corpus -> runs/bench_<tag>.json. Returns the same dict."""
    spec.check()
    out_dir = Path(out_dir); (out_dir / "runs").mkdir(parents=True, exist_ok=True)
    root = Path(root or Path(__file__).resolve().parents[5])

    test = gold[(gold.split == "test") & (gold.label.isin(spec.gradeable))]
    cells = sorted(test.groupby(["shape", "label"]).size().items(), key=lambda kv: -kv[1])

    if verbose:
        print(f"{spec.noun} benchmark '{tag}'  ·  {len(cells)} cells  ·  "
              f"{'ALL test rows' if full else str(n) + ' rows/cell/weighting'}")
        print("=" * 116)
        print(f"{'':<22} {'':<15} {'------ row-weighted ------':^34} {'-------- deduped --------':^34}")
        print(f"{'shape':<22} {'label':<15} {'n':>5} {'cov':>7} {'circ':>5} {'MAE':>6} {'r':>7}  "
              f"{'n':>5} {'cov':>7} {'circ':>5} {'MAE':>6} {'r':>7}")
        print("-" * 116)

    results = {}
    for (shape, label), n_total in cells:
        cell = test[(test["shape"] == shape) & (test["label"] == label)]
        uniq = cell.drop_duplicates(spec.text_col)
        row_s = cell if full or len(cell) <= n else cell.sample(n, random_state=0)
        ded_s = uniq if full or len(uniq) <= n else uniq.sample(n, random_state=0)

        # ONE normalize call for both samples. Every member caches per input, so
        # the overlap between the two samples costs nothing -- and over HTTP a
        # duplicate is a byte on the wire and a row in the reply.
        both = pd.concat([row_s.assign(_w="row"), ded_s.assign(_w="dedup")],
                         ignore_index=True)
        both = both.rename(columns={c: f"true_{c}" for c in spec.label_cols})
        got = spec.normalize(both)

        per = {}
        for w in ("row", "dedup"):
            sub = got[got._w == w]
            m = _score.basics(sub, spec)
            # The headline is scored on the NON-CIRCULAR rows only. Rows whose
            # confidence says the bank handed back the label are kept, counted
            # and scored, but under their own key -- never folded into the
            # number a reader will quote.
            circ = sub[spec.conf_col].isin(spec.circular_conf) if spec.circular_conf \
                else pd.Series(False, index=sub.index)
            m["circular_n"] = int(circ.sum())
            m.update(spec.metric(sub[~circ], label) or {})
            if circ.any():
                m["circular"] = spec.metric(sub[circ], label) or {}
            per[w] = m
        results[f"{shape}|{label}"] = {
            "n_in_test": int(n_total), "n_unique_in_test": int(len(uniq)), **per}

        if verbose:
            def f(v, s):
                return format(v, s) if v is not None else "-"
            rm, dm = per["row"], per["dedup"]
            print(f"{shape:<22} {label:<15} "
                  f"{rm['n']:>5} {rm['coverage']*100:>6.1f}% {rm['circular_n']:>5} "
                  f"{f(rm.get('mae'),'.1f'):>6} {f(rm.get('r'),'.3f'):>7}  "
                  f"{dm['n']:>5} {dm['coverage']*100:>6.1f}% {dm['circular_n']:>5} "
                  f"{f(dm.get('mae'),'.1f'):>6} {f(dm.get('r'),'.3f'):>7}")

    payload = {"noun": spec.noun, "tag": tag, "git_head": _git_head(root),
               "n_per_cell": None if full else n, "cells": results}
    path = out_dir / "runs" / f"bench_{tag}.json"
    path.write_text(json.dumps(payload, indent=2))
    if verbose:
        print(f"\nwrote {path}")
    return payload


def cli(spec, corpus_dir, out_dir, root=None):
    """The 6 lines of argparse every noun's run.py would otherwise repeat."""
    ap = argparse.ArgumentParser(description=f"grade describe-{spec.noun}")
    ap.add_argument("--n", type=int, default=600)
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--tag", default="current")
    ap.add_argument("--freeze", action="store_true", help="rebuild the corpus first")
    a = ap.parse_args()

    from .freeze import freeze
    corpus_dir = Path(corpus_dir)
    gold_path = corpus_dir / "gold_index.parquet"
    if a.freeze or not gold_path.exists():
        source_store = Path(root or Path.cwd()) / "_WorkSpace/1-SourceStore"
        freeze(spec, source_store, corpus_dir)
    gold = pd.read_parquet(gold_path)
    return grade(spec, gold, out_dir, tag=a.tag, n=a.n, full=a.full, root=root)
