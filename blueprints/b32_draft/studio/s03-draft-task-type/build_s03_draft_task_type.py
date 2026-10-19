"""s03 · A draft is a Task type: s03-draft-task-type.excalidraw, drawn by this builder.

How it looks and reads: /excalidraw-studio, its principles and scripts/draw.py. The topic, its face and sessions:
/haipipe-studio. A rebuild keeps whatever a person drew on the canvas (canvas.write). Check it: excalidraw-studio's
scripts/check.py. Words come from the face's yaml block; the type counts (WellDoc's Task faces) and the servers
tree are read from disk on every build.

    python build_s03_draft_task_type.py
"""
import os
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[3]
SERVERS = TOOLS / "plugins/haipipe-toolkit/servers"
WELLDOC = HERE.parents[4] / "WellDoc-SPACE"
sys.path.insert(0, str((HERE / "../../../../plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts").resolve()))
from draw import Drawing, INK, RED, canvas  # noqa: E402  (excalidraw-studio's helpers; canvas.write keeps a person's marks)

# every change to this drawing: (date YYMMDD, what changed), each a green note where it changed (JL 261007)
CHANGES = [("261015", "185 Section faces say task-type: draft; page is evidence")]
LINE = re.compile(r"(?m)^\**(task-type|page-type)\**:\s*`?([\w-]+)")


def face_words():
    face = (HERE / "s03-draft-task-type.md").read_text()
    return yaml.safe_load(re.search(r"```yaml\n(.*?)```", face, re.S).group(1))


def type_counts():
    """{('task-type'|'page-type', value): faces} over WellDoc's Projects (examples-*): a face is <folder>/<folder>.md,
    outside delivery/ (built copies), read to its first 3000 characters."""
    found = Counter()
    if not WELLDOC.is_dir():
        return found
    for top in sorted(WELLDOC.glob("examples-*")):
        for dp, dns, fns in os.walk(top):
            dns[:] = [d for d in dns if d not in {".git", "node_modules", "__pycache__", "delivery"}]
            for fn in fns:
                if fn.endswith(".md") and fn[:-3] == Path(dp).name:
                    try:
                        head = (Path(dp) / fn).read_text(encoding="utf-8", errors="ignore")[:3000]
                    except OSError:
                        continue
                    for m in LINE.finditer(head):
                        found[(m.group(1), m.group(2))] += 1
    return found


def main():
    w = face_words()
    counts = type_counts()
    out = HERE / "s03-draft-task-type.excalidraw"
    d = Drawing()

    # ① the main frame: how a Task's type picks its layout
    f1 = d.frame("① A Task's type picks its layout")
    d.heading("s03 · A draft is a Task type", "theme ─▶ Task types ─▶ a layout each; the base lays out draft for every theme")
    d.key(40, 170, 2480, 110)
    d.para(70, 192, w["key"], 2420, 32)
    d.flow(w["pick"], 40, 330, 2480, labels=w["pick_labels"], title=34, leaf=30, gap=120)

    d.text(40, 760, "🧭 themes and their Task types today", 36)
    rows = [{"cells": [t["theme"], t["types"], t["layout"]]} for t in w["themes"]]
    d.grid_table(40, 830, ["theme", "Task types", "layout"], rows, [300, 900, 620], size=30, pad=24)

    # the scoreboard: how many WellDoc faces declare each type (read from disk)
    d.text(1960, 760, "📊 WellDoc faces, by line", 36)
    shown = [("task-type", "raw"), ("task-type", "data"), ("task-type", "eval"), ("task-type", "fit"),
             ("task-type", "draft"), ("page-type", "section")]
    for i, (k, v) in enumerate(shown):
        x, y = 1960 + (i % 2) * 290, 830 + (i // 2) * 150
        d.text(x, y, f"{k}: {v}", 28, code=True)
        d.text(x, y + 34, f"{counts.get((k, v), 0):,}", 56,
               RED if (k, v) == ("task-type", "draft") and not counts.get((k, v)) else INK)
    drafts, sections = counts.get(("task-type", "draft"), 0), counts.get(("page-type", "section"), 0)
    d.para(1960, 1290, f"✅ every page-type: section face says task-type: draft" if drafts >= sections else
           f"❓ {sections - drafts} page-type: section faces still lack task-type: draft", 540, 30,
           INK if drafts >= sections else RED)
    d.badge(f1)

    # ② the servers folders, before and now
    f2 = canvas.explains(d.frame("② servers/: before and now", 2400, 1180))
    d.heading("② haipipe-board ✂ · haipipe-page ─▶ workbench-task-draft/reader · task-page ─▶ workbench-task-draft",
              "before: as on disk on 261014, kept in the face · now: read from disk on this build")
    d.text(40, 190, "before (261014)", 34)
    d.text(40, 250, w["servers_before"].rstrip(), 24, code=True)
    d.line([(980, 420), (1140, 420)], sw=5)
    d.text(990, 360, "folded in", 30)
    now = ["servers/workbench/"]
    td = SERVERS / "workbench" / "workbench-task-draft"
    tree = Drawing.folder_tree(td, open_=("reader",), notes={"reader/": "the standalone server, the reader look",
                                                            "exporters/": "md2tex · md2docx · docx2pdf"})
    now += ["└── " + tree[0]] + ["    " + s for s in tree[1:]]
    d.text(1200, 190, "✅ now, on disk", 34)
    d.text(1200, 250, "\n".join(now), 22, code=True)
    gone = [n for n in ("haipipe-board", "haipipe-page") if not (SERVERS / n).exists()]
    d.text(40, 520, "✂ gone from servers/: " + (", ".join(gone) or "none"), 28)

    # ③ steps and open points
    f3 = canvas.explains(d.frame("③ Steps and open points", 2400, 640))
    d.heading("③ Where it stands")
    d.flow(w["steps"], 40, 170, 2320, labels=["then"] * (len(w["steps"]) - 1), title=30, leaf=22)
    yy = 440
    for q in w["open"]:
        yy = d.para(40, yy, q, 2320, 26, RED) + 14

    for i, (date, what) in enumerate(CHANGES):
        e = canvas.change_note(1480, 120 + i * 26, what, date, f1["id"])
        e["id"] = f"c{i}"
        d.els.append(e)
    placed = canvas.stairs(d.els, [f1["id"], f2["id"], f3["id"]])
    d.fid = None
    for f, name in ((placed[0], "Act 1 · a type picks a layout"), (placed[1], "Act 2 · the folders, then the steps")):
        d.para(f["x"] - 820, f["y"] + 20, name, 760, 56)
    d.write(out, "build_s03_draft_task_type.py")


if __name__ == "__main__":
    main()
