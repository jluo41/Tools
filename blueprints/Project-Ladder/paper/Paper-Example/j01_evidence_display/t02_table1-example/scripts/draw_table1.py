"""Placeholder worker: Display B, Table 1, drawn for Tools' Paper-Example.

Reads only the value Run its ticket names, j02_evidence_value/t01_values-sample/runs/r01_read_values/result/values.yaml,
never a path under work/. Every number the table prints is a value id read by id (the before and after means,
RQ1-t01-007 and RQ1-t01-008), printed as the value Run shows it. Writes into RESULT_DIR (set by the Run's ticket)
table-body.tex, float.tex, method.md and values_used.csv. No number here is real.
"""
from __future__ import annotations

import csv
import os
from pathlib import Path

import yaml

BOARD = Path(__file__).resolve().parents[3]              # paper/Paper-Example
VALUE_TASK = "t01_values-sample"
VALUE_RUN = f"j02_evidence_value/{VALUE_TASK}/runs/r01_read_values"
BEFORE, AFTER = "RQ1-t01-007", "RQ1-t01-008"             # mean <outcome> before and after <the policy>
IDS = [BEFORE, AFTER]

FLOAT = r"""\begin{table}
  \centering
  \caption{\textbf{Mean <outcome> before and after <the policy>.} Placeholder table of Tools' Paper-Example; no real data.}
  \label{tab:example}
  \input{table-body.tex}
\end{table}
"""

BODY = r"""% Display B (placeholder): the before and after means, ids {before} and {after} of the value Run {value_run}
\begin{{tabular}}{{lrr}}
\toprule
 & Before & After \\
\midrule
Mean <outcome> & {b} & {a} \\
\bottomrule
\end{{tabular}}
"""

METHOD = """# Method · Table 1

## Data
<The data source>, years <YYYY to YYYY>: the value Run j02.t01.r01, its result/values.yaml (placeholder).

## Method
The mean <outcome> per <unit> before and after <the policy>, as the value Run gives them.

## Made by
- `{value_run}/result/values.yaml`, the value Run this display reads (pinned in its run.yaml `reads:`)
- `j01_evidence_display/t02_table1-example/scripts/draw_table1.py`

## Numbers
Each cell is a value id read by id ({before}, {after}); result/values_used.csv lists them with their values.
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
    res.mkdir(parents=True, exist_ok=True)
    (res / "table-body.tex").write_text(BODY.format(before=BEFORE, after=AFTER, value_run=VALUE_RUN,
                                                    b=by_id[BEFORE]["shown"], a=by_id[AFTER]["shown"]), encoding="utf-8")
    (res / "float.tex").write_text(FLOAT, encoding="utf-8")
    (res / "method.md").write_text(METHOD.format(value_run=VALUE_RUN, before=BEFORE, after=AFTER), encoding="utf-8")
    write_used(res, by_id)


if __name__ == "__main__":
    main()
