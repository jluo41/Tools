"""Placeholder worker: Display D, the subgroup estimate beside the whole sample, drawn for Tools' Paper-Example.

Reads two returned estimates from the work Runs the paper names:
  the whole sample   main.b, main.ci_lo, main.ci_hi   work/b90_example_paper_results/j02_example_estimates/t01_example_main/runs/r01_example_main/result/values.csv
  <the subgroup>     sub.b, sub.ci_lo, sub.ci_hi      work/b90_example_paper_results/j02_example_estimates/t02_example_subgroup/runs/r01_example_subgroup/result/values.csv
and writes into RESULT_DIR (set by the Run's ticket) assets/figure.png, float.tex and method.md. Both work Runs return
placeholder values; no number here is real.
"""
from __future__ import annotations

import csv
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

LADDER = Path(__file__).resolve().parents[5]            # blueprints/Project-Ladder
JOB = "work/b90_example_paper_results/j02_example_estimates"
MAIN_RUN = f"{JOB}/t01_example_main/runs/r01_example_main"
SUB_RUN = f"{JOB}/t02_example_subgroup/runs/r01_example_subgroup"

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
<The data source>, years <YYYY to YYYY>: the work Runs b90.j02.t01.r01 and b90.j02.t02.r01, each its
result/values.csv (placeholder).

## Sample
- the whole sample, {n_all} units, as in Display A
- <the subgroup>, {n_sub} units

## Method
The main model, fitted once in everyone and once in <the subgroup>; each estimate with its 95% interval.

## Made by
- `r01_example_main/result/values.csv` (main.b, main.ci_lo, main.ci_hi, sample.n_units), the Run of `{main_task}/`
- `r01_example_subgroup/result/values.csv` (sub.b, sub.ci_lo, sub.ci_hi, sub.n_units), the Run of `{sub_task}/`
- `scripts/draw_subgroup_estimate.py`, the worker of `t51_display-d-subgroup-estimate/`

## Numbers
Every point and interval is read from the two values.csv files above; nothing is typed in.
"""


def read(run: str) -> dict:
    with (LADDER / run / "result" / "values.csv").open(encoding="utf-8") as f:
        return {r["key"]: float(r["value"]) for r in csv.DictReader(f) if r["value"]}


def main() -> None:
    res = Path(os.environ["RESULT_DIR"])
    m, s = read(MAIN_RUN), read(SUB_RUN)
    rows = [("whole sample", m["main.b"], m["main.ci_lo"], m["main.ci_hi"]),
            ("<the subgroup>", s["sub.b"], s["sub.ci_lo"], s["sub.ci_hi"])]
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
    (res / "method.md").write_text(METHOD.format(n_all=int(m["sample.n_units"]), n_sub=int(s["sub.n_units"]),
                                                 main_task=MAIN_RUN.rsplit("/runs/", 1)[0],
                                                 sub_task=SUB_RUN.rsplit("/runs/", 1)[0]), encoding="utf-8")


if __name__ == "__main__":
    main()
