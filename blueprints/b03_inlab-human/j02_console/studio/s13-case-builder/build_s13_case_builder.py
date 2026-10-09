"""s13 · The case builder: the Case view on each of the three (synthetic) data types, and how a case is meant to be
built: a TriggerFn picks the moments, a Key names each case, CaseFns give it its facets (diagram/07-case-builder.txt).
Today the view cuts a case from any record row that carries text; that gap is drawn in red.
Redraw after `_build/shoot_console.py`; a person's marks are kept.

    python build_s13_case_builder.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_build"))
from console_draw import DISK, RED, Sheet, header, save  # noqa: E402

CHANGES = []                                          # (YYMMDD, what changed): a green note each
DATASETS = [("SynthCGM_v0", "a 5-minute glucose timeline: every row with a text cell becomes a case"),
            ("SynthDialogue_v0", "a doctor–patient visit: the dialogue and the note are cases"),
            ("SynthReview_v0", "a physician's reviews: one review, one case")]
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
    s.text(40, y, "? today the view reads record rows as a stand-in (any row with a text cell is a case); the target reads "
                  "the cooked CaseSet (3-CaseStore: df_case + one parquet per CaseFn)", 16, f, RED)
    s.text(40, y + 28, "? on a glucose timeline that makes every event row a 'case': is a case a 5-minute window "
                       "(CGM5MinEntry) there, not a row?", 16, f, RED)
    save(s, f, y + 60, HERE / "s13-case-builder.excalidraw", "build_s13_case_builder.py")


if __name__ == "__main__":
    main()
