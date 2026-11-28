"""run-score-e<NN>: score every arm's design of one Exp against the prediction frozen at its release.

    python score_exp.py <block> e01

Reads the Block's observed/e01_<exp>/arms.csv (arm · job · design · n · observed; per-arm totals only) and, for each
arm that names a Job and a design, that design Task's prediction.yaml (predicted · against · frozen). Writes
runs/run-score-e01/scores.csv (job · design · predicted · observed · direction · in_range · error) beside the Run's
run.yaml, and prints the scorecard: per method version, how many designs were scored, how many had the right
direction, how many fell in the predicted range. A value it cannot read as a number scores "?". Never overwrites:
scoring again is a new pass, after the old scores.csv is moved into the Run's passes/.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

NUM = r"[-+]?\d+(?:\.\d+)?"
COLS = ("job", "design", "predicted", "observed", "direction", "in_range", "error")


def front(md: Path) -> dict:
    if not md.is_file():
        return {}
    m = re.match(r"(?s)^---\n(.*?)\n---\n", md.read_text(encoding="utf-8"))
    return (yaml.safe_load(m.group(1)) or {}) if m else {}


def parse(value: str) -> dict:
    """'+0.8 [0.2; 1.4]' → {sign: '+', point: 0.8, lo: 0.2, hi: 1.4}; a placeholder keeps only what it shows."""
    s = str(value or "").strip()
    out = {"sign": "-" if s.startswith("-") else "+" if s.startswith("+") else "", "point": None, "lo": None, "hi": None}
    if not out["sign"] and "%" in s.split("[")[0]:
        return out                                     # a bare rate (12%) is a level, not an effect: unscored
    m = re.match(rf"^({NUM})", s)
    if m:
        out["point"] = float(m.group(1))
        out["sign"] = out["sign"] or ("-" if out["point"] < 0 else "+")
    r = re.search(rf"\[\s*({NUM})\s*[;,]\s*({NUM})\s*\]", s)
    if r:
        out["lo"], out["hi"] = float(r.group(1)), float(r.group(2))
    return out


def score(predicted: str, observed: str) -> tuple:
    p, o = parse(predicted), parse(observed)
    direction = "?" if not (p["sign"] and o["sign"]) else "✓" if p["sign"] == o["sign"] else "✗"
    in_range = "?" if None in (p["lo"], p["hi"], o["point"]) else "✓" if p["lo"] <= o["point"] <= p["hi"] else "✗"
    error = "?" if None in (p["point"], o["point"]) else f"{o['point'] - p['point']:+.2f}"
    return direction, in_range, error


def _job(block: Path, jid: str) -> Path | None:
    return next((p for p in sorted(block.glob(f"{jid}_*")) if p.is_dir() and (p / f"{p.name}.md").is_file()), None)


def run(block: Path, exp: str, made: list) -> list:
    if not re.match(r"^e\d+$", exp):
        sys.exit(f"an Exp id is e<NN>: {exp!r}")
    obs = next(iter(sorted((block / "observed").glob(f"{exp}_*"))), None) if (block / "observed").is_dir() else None
    if obs is None or not (obs / "arms.csv").is_file():
        sys.exit(f"no observed/{exp}_<exp>/arms.csv in {block.name} (run-add-observed-{exp} first)")
    rundir = block / "runs" / f"run-score-{exp}"
    out = rundir / "scores.csv"
    if out.exists():
        sys.exit(f"{out.relative_to(block)} is there already: move it into passes/ to score again")
    with (obs / "arms.csv").open(encoding="utf-8") as f:
        arms = list(csv.DictReader(f))
    rows = []
    for a in arms:
        jid, did = (a.get("job") or "").strip(), (a.get("design") or "").strip()
        if not re.match(r"^j\d+$", jid) or not re.match(r"^d\d+$", did):
            continue                                     # the control arm, or an arm with no design of ours
        job = _job(block, jid)
        task = next(iter(sorted(job.glob(f"t*_{did}_*"))), None) if job else None
        pred = (yaml.safe_load((task / "prediction.yaml").read_text(encoding="utf-8")) or {}) \
            if task and (task / "prediction.yaml").is_file() else {}
        predicted = str(pred.get("predicted", ""))
        if str(pred.get("frozen", "draft")).strip() in ("", "draft"):
            predicted = ""                               # a draft prediction was never released, so never scored
        direction, in_range, error = score(predicted, a.get("observed", "")) if predicted else ("?", "?", "?")
        rows.append({"job": jid, "design": did, "predicted": predicted or "?", "observed": a.get("observed", ""),
                     "direction": direction, "in_range": in_range, "error": error,
                     "_method": str(front(job / f"{job.name}.md").get("method", "?")) if job else "?"})
    rundir.mkdir(parents=True, exist_ok=True)
    card = rundir / "run.yaml"
    if not card.exists():
        card.write_text(f"run: run-score-{exp}\nkind: soft\ntype: score\ntarget: {exp}\nstatus: open\nby: ''\n"
                        "started_at: ''\nfinished_at: ''\nusage: {}\n", encoding="utf-8")
        made.append(card)
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    made.append(out)
    return rows


def scorecard(rows: list) -> list:
    """Per method version: [(method, scored, direction ✓, in range ✓)]."""
    by = defaultdict(list)
    for r in rows:
        by[r["_method"]].append(r)
    out = []
    for m, rs in sorted(by.items()):
        scored = [r for r in rs if r["direction"] != "?"]         # a draft or unreadable prediction scores "?"
        out.append((m, len(scored), sum(r["direction"] == "✓" for r in scored),
                    sum(r["in_range"] == "✓" for r in scored)))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("block", type=Path)
    ap.add_argument("exp")
    a = ap.parse_args(argv)
    made = []
    rows = run(a.block, a.exp, made)
    for p in made:
        print("made", p)
    print("method version   scored   direction ✓   in range ✓")
    for m, n, d, r in scorecard(rows):
        print(f"{m:<16} {n:>6}   {d:>11}   {r:>10}")
    return rows


if __name__ == "__main__":
    main()
