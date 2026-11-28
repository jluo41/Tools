"""s02 · The data lineage: the four DATA views are one dataset at four pipeline stages (Raw · Source · Record · Case),
each view to its store (read from web/src/views.ts' LAYER_BLURB) and the route that serves it; and the fork of
diagram/09-workspace-wiring.txt, decided 261009 (j02 Q02): read the record store in place; the json copy is the fallback.
A rebuild keeps whatever a person drew.

    python build_s02_data_lineage.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_build"))
from console_draw import BLURBS, DISK, GREEN, VIEWS, Sheet, header, save  # noqa: E402

CHANGES = [("261009", "decided: read in place (Q02); record_store.py, checked equal to the json copy")]
FNS = {"raw": "(arrives)", "source": "SourceFn", "record": "HumanFn + RecordFn", "case": "TriggerFn + CaseFn"}
FORK = [
    ["① COPY (the fallback)", "a build step flattens the RecSet into InLabStore/<dataset>/patients/<human>.json",
     "simple, fast reads", "a second copy that can go stale, and one more copy of patient data to secure"],
    ["② READ IN PLACE (chosen)", "$INLAB_RECORD_STORE: the console assembles each human's json per request from "
     "the record set (record_store.py, beside the engine's json reader)",
     "one source of truth, always fresh, no copy", "a parquet filter per request (cached per human); no raw layer"],
]
CHECK = ("on the 5 synthetic glucose humans, every Individual view's API answer from the record store equals the json "
         "copy's (116 equal); the record store also carries the one-row Ptt record, and has no raw layer")


def main():
    s = Sheet()
    f = s.frame("1 · The data lineage", 0, 0, 1900, 100)
    y = header(s, f, "s02 · The data lineage: one dataset, four stages",
               "Put two DATA views side by side (drag a tab) and the transformation between them is visible row for row.",
               CHANGES)
    label = {k: f"{icon} {lab}" for k, icon, lab, _ in VIEWS}
    rows = []
    for key in ("raw", "source", "record", "case"):
        store, what = BLURBS.get(key, ("", ""))
        rows.append([label[key], store, FNS[key], what, DISK[key][-1]])
    y = s.table(40, y, [("view", 150, 14), ("store", 180, 18), ("made by", 220, 22), ("what you see", 760, 76),
                        ("route", 500, 50)], rows, f)
    y += 50
    s.text(40, y, "How _WorkSpace reaches the console (diagram/09)", 22, f)
    y = s.table(40, y + 40, [("way", 220, 22), ("how", 640, 64), ("for", 320, 32), ("against", 600, 60)], FORK, f)
    y += 30
    s.text(40, y, "✎ 261009 decided (j02 Q02): read in place; the copy stays only where no record store is mounted",
           18, f, GREEN)
    s.text(40, y + 30, "✎ 261009 check: " + CHECK, 16, f, GREEN)
    y += 30
    save(s, f, y + 40, HERE / "s02-data-lineage.excalidraw", "build_s02_data_lineage.py")


if __name__ == "__main__":
    main()
