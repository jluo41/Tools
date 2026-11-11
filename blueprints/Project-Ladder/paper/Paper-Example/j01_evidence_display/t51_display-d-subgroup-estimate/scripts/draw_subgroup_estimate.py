"""Placeholder worker: Display D, the subgroup estimate beside the whole sample, drawn for Tools' Paper-Example.

Reads only the value Run its ticket names, j02_evidence_value/t01_values-sample/runs/r01_read_values/result/values.yaml,
never a path under work/; every number it draws or prints is a value id, read by id:
  the whole sample   RQ1-t01-002 main.b, RQ1-t01-003 main.ci_lo, RQ1-t01-004 main.ci_hi, RQ1-t01-001 sample.n_units
  <the subgroup>     RQ1-t01-006 sub.b, RQ1-t01-011 sub.ci_lo, RQ1-t01-012 sub.ci_hi, RQ1-t01-010 sub.n_units
and writes into RESULT_DIR (set by the Run's ticket) assets/figure.png, float.tex, method.md and values_used.csv. The
values are placeholders; no number here is real.
"""
from __future__ import annotations

import csv
import os
from pathlib import Path

import matplotlib
import yaml

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

BOARD = Path(__file__).resolve().parents[3]              # paper/Paper-Example
VALUE_TASK = "t01_values-sample"
VALUE_RUN = f"j02_evidence_value/{VALUE_TASK}/runs/r01_read_values"
MAIN = ("RQ1-t01-002", "RQ1-t01-003", "RQ1-t01-004")      # the whole sample: estimate, 95% CI low, high
SUB = ("RQ1-t01-006", "RQ1-t01-011", "RQ1-t01-012")       # <the subgroup>: estimate, 95% CI low, high
N_ALL, N_SUB = "RQ1-t01-001", "RQ1-t01-010"               # units in each, printed in the method
IDS = [*MAIN, *SUB, N_ALL, N_SUB]

FLOAT = r"""\begin{figure}
  \centering
  \includegraphics[width=\linewidth]{assets/figure.png}
  \caption{\textbf{<Subgroup> estimate beside the whole sample.} Each point is the same model's estimate with its 95\%% interval, in everyone and in <the subgroup>; the dashed line marks zero. Placeholder figure of Tools' Paper-Example; no real data.}
  \label{fig:subgroup}
\end{figure}
"""

METHOD = """# Method · eFigure 2

## Message
In <the subgroup> the association with <the policy> is larger than in the whole sample, and its interval is wider,
so the paper's answer to RQ2, for whom it changes, rests on fewer units.

## Data
<The data source>, years <YYYY to YYYY>: the value Run j02.t01.r01, its result/values.yaml, which reads the work
Runs b90.j02.t01.r01 and b90.j02.t02.r01 (placeholder).

## Sample
- the whole sample, {n_all} units, as in Display A
- <the subgroup>, {n_sub} units

## Method
The main model, fitted once in everyone and once in <the subgroup>; each estimate with its 95% interval.

## Made by
- `{value_run}/result/values.yaml`, the value Run this display reads (pinned in its run.yaml `reads:`)
- `scripts/draw_subgroup_estimate.py`, the worker of `t51_display-d-subgroup-estimate/`

## Numbers
Every point, interval and count is a value id read by id from values.yaml above; result/values_used.csv lists
them. Nothing is typed in.
"""


def values_by_id() -> dict:
    """The value Run's values, by id; a missing id stops the Run (rule 2: id before ink)."""
    doc = yaml.safe_load((BOARD / VALUE_RUN / "result" / "values.yaml").read_text(encoding="utf-8")) or {}
    by_id = {v["id"]: dict(v, key=k) for k, v in (doc.get("values") or {}).items() if isinstance(v, dict) and v.get("id")}
    missing = [i for i in IDS if i not in by_id]
    if missing:
        raise SystemExit(f"stop: {', '.join(missing)} not in {VALUE_RUN}/result/values.yaml")
    return by_id


def write_used(res: Path, by_id: dict) -> None:
    with (res / "values_used.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "key", "value", "shown", "value_task", "value_run"])
        for i in IDS:
            v = by_id[i]
            w.writerow([i, v["key"], v["value"], v.get("shown", ""), VALUE_TASK, VALUE_RUN.rsplit("/", 1)[1]])


def main() -> None:
    res = Path(os.environ["RESULT_DIR"])
    by_id = values_by_id()
    val = lambda i: float(by_id[i]["value"])               # noqa: E731
    rows = [("whole sample", *map(val, MAIN)), ("<the subgroup>", *map(val, SUB))]
    (res / "assets").mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 2.8), dpi=300)   # the venue: 7 in at 300 dpi
    for y, (name, b, lo, hi) in zip(range(len(rows))[::-1], rows):
        ax.errorbar([b], [y], xerr=[[b - lo], [hi - b]], fmt="o", color="#1e1e1e", capsize=4, markersize=6)
    ax.axvline(0, color="#1e1e1e", linestyle="--", linewidth=0.8)
    ax.set_yticks(list(range(len(rows))[::-1]), [r[0] for r in rows])
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.set_xlabel("<estimate>, points (95% interval)")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    fig.savefig(res / "assets" / "figure.png")
    plt.close(fig)
    (res / "float.tex").write_text(FLOAT.replace("%%", "%"), encoding="utf-8")
    (res / "method.md").write_text(METHOD.format(n_all=by_id[N_ALL]["shown"], n_sub=by_id[N_SUB]["shown"],
                                                 value_run=VALUE_RUN), encoding="utf-8")
    write_used(res, by_id)


if __name__ == "__main__":
    main()
