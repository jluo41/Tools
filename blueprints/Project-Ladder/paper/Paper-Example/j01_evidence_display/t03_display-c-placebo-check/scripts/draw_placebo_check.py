"""Placeholder worker: Display C, the placebo check, drawn for Tools' Paper-Example.

Reads the policy-year estimate (main.b, main.ci_lo, main.ci_hi) from the work Run the paper names,
work/b90_example_paper_results/j02_example_estimates/t01_example_main/runs/r01_example_main/result/values.csv, and
writes into RESULT_DIR (set by the Run's ticket) assets/figure.png, float.tex and method.md. The placebo-year
estimates are fixed placeholders, not fitted; no number here is real.
"""
from __future__ import annotations

import csv
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

LADDER = Path(__file__).resolve().parents[5]            # blueprints/Project-Ladder
WORK_RUN = "work/b90_example_paper_results/j02_example_estimates/t01_example_main/runs/r01_example_main"
PLACEBO = [("<year −3>", 0.21, -1.12, 1.54),             # (period, estimate, low, high): placeholders, not fitted
           ("<year −2>", -0.34, -1.71, 1.03),
           ("<year −1>", 0.12, -1.25, 1.49)]

FLOAT = r"""\begin{figure}
  \centering
  \includegraphics[width=\linewidth]{assets/figure.png}
  \caption{\textbf{<Placebo check>: the same model in years with no policy.} Points show each estimate with its 95\%% interval; the dashed line marks zero; the last point is the policy year. Placeholder figure of Tools' Paper-Example; no real data.}
  \label{fig:placebo}
\end{figure}
"""

METHOD = """# Method · eFigure 1

## Message
In the years before <the policy> the same model finds no effect, so the effect in the policy year is not a trend
that was already there.

## Data
<The data source>, years <YYYY to YYYY>: the work Run b90.j02.t01.r01, its result/values.csv (placeholder).

## Sample
- <who is in it>, as in Display A

## Method
The main model refitted with <the policy> moved to each earlier year, where it did not happen; each estimate with its
95% interval. The placebo estimates are placeholders.

## Made by
- `r01_example_main/result/values.csv` (the policy-year estimate: main.b, main.ci_lo, main.ci_hi), the Run of
  `{work_task}/`
- `j01_evidence_display/t03_display-c-placebo-check/scripts/draw_placebo_check.py`

## Numbers
The policy-year estimate is read from values.csv above; the placebo estimates are fixed placeholders.
"""


def main() -> None:
    res = Path(os.environ["RESULT_DIR"])
    with (LADDER / WORK_RUN / "result" / "values.csv").open(encoding="utf-8") as f:
        v = {r["key"]: float(r["value"]) for r in csv.DictReader(f) if r["value"]}
    rows = PLACEBO + [("<policy year>", v["main.b"], v["main.ci_lo"], v["main.ci_hi"])]
    (res / "assets").mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=200)
    xs = range(len(rows))
    for x, (name, b, lo, hi) in zip(xs, rows):
        last = x == len(rows) - 1
        ax.errorbar([x], [b], yerr=[[b - lo], [hi - b]], fmt="o", color="#1e1e1e" if last else "#868e96",
                    capsize=4, markersize=6)
    ax.axhline(0, color="#1e1e1e", linestyle="--", linewidth=0.8)
    ax.set_xticks(list(xs), [r[0] for r in rows])
    ax.set_ylabel("<estimate>, points")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    fig.savefig(res / "assets" / "figure.png")
    plt.close(fig)
    (res / "float.tex").write_text(FLOAT.replace("%%", "%"), encoding="utf-8")
    (res / "method.md").write_text(METHOD.format(work_task=WORK_RUN.rsplit('/runs/', 1)[0]), encoding="utf-8")


if __name__ == "__main__":
    main()
