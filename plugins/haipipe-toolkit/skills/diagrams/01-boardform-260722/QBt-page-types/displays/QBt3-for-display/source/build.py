#!/usr/bin/env python3
"""Render this display unit from the QA atom it declares a need on.

🚫 FABRICATED input. See `QA-probe/QBt5-for-value/1-drift-counts.md`.

The one thing to notice: this script never writes the QA's path. It asks the
resolver for `QA-probe/QBt5-for-value/1-drift-counts`, which is the id declared in the
`needs:` line of `QBt3-for-display.md`. Move that QA anywhere in the group and
this file does not change.

That is the whole proposal. A real display page carries six hand-written paths in
its provenance chain; this one carries none.
"""
import csv
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
UNIT = HERE.parent                       # displays/QBt3-for-display/
GROUP = UNIT.parents[1]                  # the QBt group folder
sys.path.insert(0, str(GROUP))

from unit import resolve                                    # noqa: E402

NEED = "QA-probe/QBt5-for-value/1-drift-counts"
OUT = UNIT / "out" / "assets" / "figure.txt"
BAR = 30


def rate(row):
    return 100.0 * int(row["drift_events"]) / int(row["pages"])


def render(rows):
    worst = max(rate(r) for r in rows)
    out = [
        "  📉 Contract drift by type-key tenure          🚫 FABRICATED",
        "  " + "─" * 60,
        f"  {'BAND':<26}{'PAGES':>6}{'DRIFT':>7}   RATE",
        "  " + "─" * 60,
    ]
    for r in rows:
        pct = rate(r)
        out.append(
            f"  {r['band']:<26}{r['pages']:>6}{r['drift_events']:>7}   "
            f"{'█' * round(BAR * pct / worst)} {pct:.1f}%"
        )
    out += [
        "  " + "─" * 60,
        f"  source: {NEED} · 95% CI in that atom's counts.csv",
        "  label: ASSOCIATION. Tenure is not assigned and page size is not",
        "  controlled, so this figure may not say 'reduces'.",
        "  🚫 every number above is invented; cite nothing here",
    ]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    with resolve(NEED).open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(rows))
    print(f"{len(rows)} rows from {NEED} -> {OUT.relative_to(GROUP)}")
