#!/usr/bin/env python3
"""Render this deck from the QA atom it declares a need on.

🚫 FABRICATED input. See `QA-probe/QBt5-for-value/1-drift-counts.md`.

The one thing to notice is the same thing `displays/QBt3-for-display` shows: this
script never writes the QA record's path. It asks the resolver for the id
declared in the `needs:` line of `QBt9-for-slide.md`, so the record can move
anywhere in the group and this file does not change.

The second thing to notice is what that buys a DECK. A slide keeps `for-value`'s
rule, every number it shows names a value binding or a producing run, and a deck
is the surface where that rule is hardest to hold: numbers get typed into slide
markup by hand at 2am and never traced again. Here they cannot be. The template
carries no digits at all; `<!--ROWS-->` and `<!--N-->` are filled from the atom,
and a changed count in the record changes the slide on the next build.

The denominator is DERIVED, not bound. `QA-probe/QBt5-for-value/2-corpus-size`
holds a corpus count and `QBt5` deliberately leaves it with no consumer, so
binding it here would quietly close another specimen's open row. The N on the
cover is the sum of this atom's own `pages` column instead, and it is labelled as
derived in `QBt9`'s provenance division.

USAGE
    python3 build.py                 (or `python3 unit.py build` for the chain)
"""
import csv
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
UNIT = HERE.parent                       # slides/QBt9-for-slide/
GROUP = UNIT.parents[1]                  # the QBt group folder
sys.path.insert(0, str(GROUP))

from unit import resolve                                      # noqa: E402

NEED = "QA-probe/QBt5-for-value/1-drift-counts"
TEMPLATE = HERE / "deck.template.html"
OUT = UNIT / "out" / "deck.html"


def rate(row):
    return 100.0 * int(row["drift_events"]) / int(row["pages"])


def rows_html(rows):
    """One grid row per band: label, pages, drift, bar, rate.

    The bar is scaled to the WORST band rather than to 100 percent, which is the
    same scaling `QBt3`'s ascii figure uses, so the two renders of this one atom
    cannot disagree about which band looks longest.
    """
    worst = max(rate(r) for r in rows)
    out = []
    for r in rows:
        pct = rate(r)
        out.append(
            f'        <span>{r["band"]}</span>'
            f'<span class="n">{r["pages"]}</span>'
            f'<span class="n">{r["drift_events"]}</span>'
            f'<span class="track"><i style="width:{100.0 * pct / worst:.1f}%"></i></span>'
            f'<span class="pct">{pct:.1f}%</span>'
        )
    return "\n".join(out)


if __name__ == "__main__":
    with resolve(NEED).open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        raise SystemExit(f"{NEED} resolved to an empty table; nothing to render")

    html = TEMPLATE.read_text()
    for token, value in (
        ("<!--ROWS-->", rows_html(rows)),
        ("<!--N-->", str(sum(int(r["pages"]) for r in rows))),
        ("<!--NEED-->", NEED),
    ):
        if token not in html:
            raise SystemExit(f"{TEMPLATE.name} lost its {token} slot")
        html = html.replace(token, value)

    # A deck with a build timestamp in it is a deck whose bytes change on every
    # rebuild, and every slide's acceptance row would fall to ⬜ for no reason a
    # reader could see. The output is a pure function of the template and the
    # atom, so an unchanged input rebuilds to an identical file.
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html)
    print(f"{len(rows)} rows from {NEED} -> {OUT.relative_to(GROUP)}")
