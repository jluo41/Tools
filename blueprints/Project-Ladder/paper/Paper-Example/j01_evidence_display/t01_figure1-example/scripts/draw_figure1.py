"""Placeholder worker: Display A, Figure 1, drawn for Tools' Paper-Example.

Reads only the value Run its ticket names, j02_evidence_value/t01_values-sample/runs/r01_read_values/result/values.yaml,
never a path under work/. Figure 1 prints no number: its four bars are placeholder shapes, not values, so it reads no
id and its result/values_used.csv holds the header only. Writes into RESULT_DIR (set by the Run's ticket)
assets/figure.png, float.tex, method.md and values_used.csv. No number here is real.
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
IDS: list = []                                           # the value ids this display prints: none
BARS = [(300, "#1864ab"), (220, "#1864ab"), (360, "#e8590c"), (180, "#e8590c")]   # placeholder shapes, not values

FLOAT = r"""\begin{figure}
  \centering
  \includegraphics[width=\linewidth]{assets/figure.png}
  \caption{\textbf{<Outcome> by <group>, before and after <the policy>.} Bars show the mean <outcome> per <unit>. Placeholder figure of Tools' Paper-Example; no real data.}
  \label{fig:example}
\end{figure}
"""

METHOD = """# Method · Figure 1

## Data
<The data source>, years <YYYY to YYYY>.

## Sample
- <who is in it>
- <how they were chosen>

## Method
<The comparison or model, and its estimator.>

## Outcomes
1. **<outcome>**: <its definition>

## Made by
- `{value_run}/result/values.yaml`, the value Run this display reads (pinned in its run.yaml `reads:`)
- `j01_evidence_display/t01_figure1-example/scripts/draw_figure1.py`

## Numbers
Figure 1 prints no number; its bars are placeholder shapes. It reads no value id, so result/values_used.csv is empty.
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
    (res / "assets").mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=100)
    xs = [1.19, 2.89, 4.59, 6.30]
    ax.bar(xs, [h for h, _ in BARS], width=1.0, color=[c for _, c in BARS])
    ax.set_xlim(0, 7.8)
    ax.set_ylim(0, 420)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("<group> by <period> (placeholder)", fontsize=7, labelpad=14)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_linewidth(2)
    fig.subplots_adjust(left=0.09, right=0.955, top=0.92, bottom=0.115)
    fig.savefig(res / "assets" / "figure.png")
    plt.close(fig)
    (res / "float.tex").write_text(FLOAT, encoding="utf-8")
    (res / "method.md").write_text(METHOD.format(value_run=VALUE_RUN), encoding="utf-8")
    write_used(res, by_id)


if __name__ == "__main__":
    main()
