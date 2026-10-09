"""s02 · The data lineage: the four DATA views are one dataset at four pipeline stages (Raw · Source · Record · Case),
each view to its store (read from web/src/views.ts' LAYER_BLURB) and the route that serves it; and the open fork of
diagram/09-workspace-wiring.txt, drawn in red: copy each human into a json, or read the record store in place.
A rebuild keeps whatever a person drew.

    python build_s02_data_lineage.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_build"))
from console_draw import BLURBS, DISK, RED, VIEWS, Sheet, header, save  # noqa: E402

CHANGES = []                                          # (YYMMDD, what changed): a green note each
FNS = {"raw": "(arrives)", "source": "SourceFn", "record": "HumanFn + RecordFn", "case": "TriggerFn + CaseFn"}
FORK = [
    ["① COPY (today)", "a build step flattens the RecSet into InLabStore/<dataset>/patients/<human>.json",
     "simple, fast reads", "a second copy that can go stale, and one more copy of patient data to secure"],
    ["② ADAPTER", "the console reads 2-RecStore directly and assembles each human's json per request",
     "one source of truth, always fresh, no copy", "a parquet filter per request (cacheable)"],
]


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
    s.text(40, y, "How _WorkSpace reaches the console (diagram/09): the open fork", 22, f, RED)
    y = s.table(40, y + 40, [("way", 180, 18), ("how", 640, 64), ("for", 320, 32), ("against", 640, 64)], FORK, f,
                red=lambda r: True)
    y += 30
    s.text(40, y, "? copy or read in place: JL's question in diagram/09, recorded as j02 Q02, not decided here", 18, f, RED)
    save(s, f, y + 40, HERE / "s02-data-lineage.excalidraw", "build_s02_data_lineage.py")


if __name__ == "__main__":
    main()
