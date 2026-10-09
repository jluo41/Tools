"""s13 · The case builder: the Case view on each of the three (synthetic) data types, and how a case is meant to be
built: a TriggerFn picks the moments, a Key names each case, CaseFns give it its facets (diagram/07-case-builder.txt).
Since 261009 the view reads the cooked case set when one is mounted, and otherwise a record row that holds prose.
Redraw after `_build/shoot_console.py`; a person's marks are kept.

    python build_s13_case_builder.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_build"))
from console_draw import DISK, GREEN, Sheet, header, save  # noqa: E402

CHANGES = [("261009", "fixed: cases come from the case set (3-CaseStore), one per trigger moment, with facets"),
           ("261009", "no case set: a row is a case only if it holds prose (5+ words); a timeline has none")]
DATASETS = [("SynthCGM_v0", "a glucose timeline with a case set mounted: one case per meal, with its two facets"),
            ("SynthDialogue_v0", "a doctor–patient visit, no case set: the rows that hold prose are cases"),
            ("SynthReview_v0", "a physician's reviews, no case set: one review, one case")]
DESIGN = [("TriggerFn", "WHICH moments become cases, and each one's ObsDT", "fn_case/fn_trigger"),
          ("Key", "how a case is identified (case_id_cols, e.g. PID · EncounterID · ObsDT)", "inside the TriggerFn"),
          ("CaseFn × N", "WHAT facets each case carries (dialogue, note, context …)", "fn_case/case_casefn")]


def main():
    s = Sheet()
    f = s.frame("1 · The case builder", 0, 0, 3 * 620 + 60, 100)
    y = header(s, f, "s13 · The case builder: one human's record, cut into cases",
               "A case is the unit a score or a label attaches to. The Case view, on each synthetic data type:", CHANGES)
    x, w = 40, 560
    tallest = 0
    for i, (ds, what) in enumerate(DATASETS):
        cx = x + i * (w + 60)
        s.text(cx, y, f"📌 Case · {ds}", 20, f)
        s.text(cx, y + 28, what, 14, f)
        h = s.image(HERE / "shots" / f"case_{ds}.png", cx, y + 56, w, f)
        tallest = max(tallest, h)
    y += 56 + tallest + 30
    s.text(40, y, "on disk", 14, f)
    for line in DISK["case"]:
        y += 20
        s.text(52, y, line, 14, f)
    y += 50
    s.text(40, y, "How a case is meant to be built (diagram/07-case-builder.txt)", 22, f)
    y = s.table(40, y + 40, [("function", 200, 20), ("decides", 620, 64), ("lives in", 300, 30)],
                [list(r) for r in DESIGN], f)
    y += 30
    s.text(40, y, "✎ 261009 the view reads the cooked CaseSet when one is mounted ($INLAB_CASE_STORE: df_case + one "
                  "parquet per CaseFn, row for row); no table, column or CaseFn is named in the code", 16, f, GREEN)
    s.text(40, y + 28, "✎ 261009 without one, a row is a case only if it holds prose; a glucose timeline shows "
                       "'no case set mounted' and no cases, never a reading per case", 16, f, GREEN)
    save(s, f, y + 60, HERE / "s13-case-builder.excalidraw", "build_s13_case_builder.py")


if __name__ == "__main__":
    main()
