"""Placeholder worker: Display C, the placebo check, drawn for Tools' Paper-Example.

Reads only the value Run its ticket names, j02_evidence_value/t01_values-sample/runs/r01_read_values/result/values.yaml,
never a path under work/: the policy-year estimate by id (RQ1-t01-002 main.b, RQ1-t01-003 main.ci_lo, RQ1-t01-004
main.ci_hi). Writes into RESULT_DIR (set by the Run's ticket) assets/figure.png, float.tex, method.md and
values_used.csv. The placebo-year estimates are fixed placeholders, not fitted, and not values; no number here is real.
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
B, LO, HI = "RQ1-t01-002", "RQ1-t01-003", "RQ1-t01-004"   # the policy-year estimate and its 95% interval
IDS = [B, LO, HI]
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
<The data source>, years <YYYY to YYYY>: the value Run j02.t01.r01, its result/values.yaml (placeholder).

## Sample
- <who is in it>, as in Display A

## Method
The main model refitted with <the policy> moved to each earlier year, where it did not happen; each estimate with its
95% interval. The placebo estimates are placeholders.

## Made by
- `{value_run}/result/values.yaml` (the policy-year estimate: {b}, {lo}, {hi}), the value Run this
  display reads (pinned in its run.yaml `reads:`)
- `j01_evidence_display/t03_display-c-placebo-check/scripts/draw_placebo_check.py`

## Numbers
The policy-year estimate is read by id from values.yaml above (result/values_used.csv lists the ids); the placebo
estimates are fixed placeholders.
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
    rows = PLACEBO + [("<policy year>", *(float(by_id[i]["value"]) for i in (B, LO, HI)))]
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
    (res / "method.md").write_text(METHOD.format(value_run=VALUE_RUN, b=B, lo=LO, hi=HI), encoding="utf-8")
    write_used(res, by_id)


if __name__ == "__main__":
    main()
