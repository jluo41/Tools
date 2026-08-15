#!/usr/bin/env python3
"""Render this deck from the value record it declares a need on.

WHAT A DECK ADDS OVER A FIGURE. `for-value`'s rule is that every number shown
names a value binding or a producing run, and a deck is the surface where that
rule is hardest to hold: numbers get typed into slide markup by hand at 2am and
never traced again. Here they cannot be. The template carries NO DIGITS. Every
one of `<!--ROWS-->`, `<!--TOTAL-->` and `<!--ZERO-->` is filled from the record's
own CSV, so a corrected measurement changes the slide on the next build and a
hand-edited slide is overwritten rather than preserved.

The atom is `QA-probe/QBt5-for-value/1-artifact-paths`, and its numbers are
MEASURED: `.data/source/measure.py` counts artifact-path mentions across the ten
page-type contracts, the record types them once, and `.data/source/build.py`
parses them into the CSV this file reads. Three files, one number.

    python3 build.py [stage-dir]   ->  <paper-root>/slides/QBt9-for-slide/deck.html
"""
import csv
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
UNIT = HERE.parent
STAGE = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else UNIT.parent.parent
ATOM = STAGE / "QA-probe/QBt5-for-value/1-artifact-paths.data/counts.csv"
ROOT = STAGE / "_fixture" if (STAGE / "_fixture").is_dir() else STAGE.parents[1]
OUT = ROOT / "slides" / UNIT.name / "deck.html"

if not ATOM.is_file():
    sys.exit(f"the value record this deck needs has not been built: {ATOM}\n"
             "run QA-probe/QBt5-for-value/1-artifact-paths.data/source/build.py")

rows = list(csv.DictReader(ATOM.open(encoding="utf-8")))
if not rows:
    sys.exit(f"{ATOM} is empty; refusing to render a deck with no numbers")

body = "\n".join(
    '    <tr class="{}"><td>{}</td><td class="n">{}</td><td class="n">{}</td></tr>'
    .format("zero" if r["paths"] == "0" else "", r["contract"], r["paths"], r["lines"])
    for r in rows)

html = (HERE / "deck.template.html").read_text(encoding="utf-8")
html = (html.replace("<!--ROWS-->", "\n" + body + "\n  ")
            .replace("<!--TOTAL-->", str(sum(int(r["paths"]) for r in rows)))
            .replace("<!--ZERO-->", str(sum(1 for r in rows if r["paths"] == "0"))))

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(html, encoding="utf-8")
print(f"{len(rows)} rows from {ATOM.name} -> {OUT.relative_to(STAGE)}")
