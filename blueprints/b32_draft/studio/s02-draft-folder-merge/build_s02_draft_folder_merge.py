"""s02 · One draft folder: page and writing: s02-draft-folder-merge.excalidraw, drawn by this builder.

How it looks and reads: /excalidraw-studio, its principles and scripts/draw.py (frames, a map, the key point,
the density badge, acts). The topic, its face and sessions: /haipipe-studio. A rebuild keeps whatever a person drew
on the canvas (canvas.write, a seed snapshot beside the drawing). Check it: excalidraw-studio's scripts/check.py.

Words come from the face's yaml block; the folder trees and the callers of haipipe-writing are read from disk.

    python build_s02_draft_folder_merge.py
"""
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[3]
BASE = TOOLS / "plugins/haipipe-toolkit/skills/1_base"
sys.path.insert(0, str((HERE / "../../../../plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts").resolve()))
from draw import Drawing, RED, canvas  # noqa: E402  (excalidraw-studio's helpers; canvas.write keeps a person's marks)

# every change to this drawing: (date YYMMDD, what changed). Each gets a green note where it changed (JL 261007)
CHANGES = [("261014", "moved: page/ is draft/, writing/ is draft/writing/; the writing link removed")]
TEXT_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json", ".js", ".html", ".sh", ".txt", ".toml", ".excalidraw"}


def face_words():
    face = (HERE / "s02-draft-folder-merge.md").read_text()
    block = re.search(r"```yaml\n(.*?)```", face, re.S).group(1)
    return yaml.safe_load(block)


def writer_callers():
    """Files outside draft/writing/ that name haipipe-writing, grouped by the skill (or server) they sit in."""
    groups = Counter()
    for root in (TOOLS / "plugins",):
        for p in root.rglob("*"):
            if not p.is_file() or p.suffix not in TEXT_SUFFIXES or "__pycache__" in p.parts or ".pytest_cache" in p.parts:
                continue
            rel = p.relative_to(TOOLS).parts
            if rel[:6] == ("plugins", "haipipe-toolkit", "skills", "1_base", "draft", "writing"):
                continue
            try:
                if "haipipe-writing" not in p.read_text(errors="ignore"):
                    continue
            except OSError:
                continue
            if rel[:5] == ("plugins", "haipipe-toolkit", "skills", "1_base", "draft"):
                groups["inside draft/"] += 1
            elif "servers" in rel:
                groups[f"servers/{rel[rel.index('servers') + 1]}"] += 1
            elif "agents" in rel:
                groups["agents"] += 1
            elif "skills" in rel:
                i = rel.index("skills")
                groups["/".join(rel[i + 2:i + 4]) if rel[i + 1][0].isdigit() else rel[i + 1]] += 1
            else:
                groups[rel[1]] += 1
    return groups


def files_in(folder):
    return sum(1 for q in folder.rglob("*") if q.is_file() and "__pycache__" not in q.parts and ".pytest_cache" not in q.parts)


def main():
    w = face_words()
    callers = writer_callers()
    inside = callers.pop("inside draft/", 0)
    outside = sum(callers.values())
    out = HERE / "s02-draft-folder-merge.excalidraw"
    d = Drawing()

    # ① the main frame: who calls the writer
    f1 = d.frame("① Who calls the writer, and what draft/ now holds")
    d.heading("s02 · One draft folder: page and writing",
              f"{inside + outside} files outside draft/writing/ name haipipe-writing: {inside} elsewhere in draft/, "
              f"{outside} in other skills (counted from disk on this build)")
    d.key(40, 170, 2480, 110)
    d.para(70, 192, w["key"], 2420, 32)

    top = d.flow(w["draft_chain"], 100, 380, 1560, labels=w["chain_labels"], title=34, leaf=28, gap=150)
    runs_x, runs_y, runs_w, runs_h = top[-1]

    row_y = 880
    low = d.flow([w["style"], {**w["writer"], "key": True}, w["evaluate"]], 100, row_y, 1560,
                 labels=["shapes the voice", "is judged by"], title=36, leaf=28, gap=200)
    wx, wy, ww, wh = low[1]
    mid = wx + ww / 2
    d.line([(runs_x + runs_w / 2, runs_y + runs_h + 6), (runs_x + runs_w / 2, (runs_y + runs_h + wy) / 2), (mid, (runs_y + runs_h + wy) / 2), (mid, wy - 6)], sw=3)
    d.text(mid + 20, (runs_y + runs_h + wy) / 2 - 42, w["request_label"], 30)

    bottom = max(y + h for _, y, _, h in low)
    d.box(60, 340, 1640, bottom + 50 - 340, dashed=True, sw=2)
    d.text(80, bottom + 62, "1_base/draft/ since 261014: everything inside this line", 28, code=True)
    d.para(80, bottom + 130, w["clash"], 1600, 30, RED)

    # the other callers, read from disk, on the right
    d.text(1860, 340, f"🔌 {w['outside_label']}", 34)
    yy = 410
    for name, n in callers.most_common(10):
        d.box(1860, yy, 620, 62)
        d.text(1884, yy + 13, f"{name}", 28, code=True)
        d.text(2420, yy + 13, f"{n}", 30)
        d.line([(1860, yy + 31), (1800, yy + 31), (1800, bottom + 26), (mid, bottom + 26), (mid, wy + wh + 6)], sw=1.5,
               arrow=(name == callers.most_common(1)[0][0]))
        yy += 80
    if len(callers) > 10:
        d.text(1860, yy, f"… {len(callers) - 10} more", 28)
    d.badge(f1)

    # ② the folders before and after
    f2 = canvas.explains(d.frame("② The folders: before and now", 2400, 1000))
    d.heading("② page/ + writing/ ─▶ draft/", "before: as on disk on 261014, kept in the face · now: read from disk on this build")
    now = [f"1_base/draft/   {files_in(BASE / 'draft')} files"]
    now += ["  " + (re.sub(r"(haipipe-page/?)\s+\d+ files", r"haipipe-page  ─▶ link to haipipe-draft", s)
                    if (BASE / "draft/haipipe-page").is_symlink() else s)
            for s in Drawing.folder_tree(BASE / "draft", notes={"writing/": "haipipe-writing, 1_style, 2_evaluate"})[1:]]
    now += ["", w["links_now"].rstrip()]
    d.text(40, 190, "before (261014)", 34)
    d.text(40, 250, w["before_tree"].rstrip(), 22, code=True)
    d.line([(1080, 520), (1220, 520)], sw=5)
    d.text(1080, 460, "moved", 30)
    d.text(1260, 190, "✅ now, on disk", 34)
    d.text(1260, 250, "\n".join(now), 22, code=True)

    # ③ the steps and what is open
    f3 = canvas.explains(d.frame("③ Steps and open points", 2400, 640))
    d.heading("③ Where it stands")
    d.flow(w["steps"], 40, 170, 2320, labels=["then", "then", "then"], title=30, leaf=22)
    yy = 440
    for q in w["open"]:
        yy = d.para(40, yy, q, 2320, 26, RED) + 14

    for i, (date, what) in enumerate(CHANGES):
        e = canvas.change_note(1640, 205 + i * 26, what, date, f2["id"], size=22)
        e["id"] = f"c{i}"
        d.els.append(e)
    placed = canvas.stairs(d.els, [f1["id"], f2["id"], f3["id"]])
    d.fid = None                                                  # the act names stand outside the frames
    for f, name in ((placed[0], "Act 1 · who calls the writer"), (placed[1], "Act 2 · the folders, then the steps")):
        d.para(f["x"] - 820, f["y"] + 20, name, 760, 56)
    d.write(out, "build_s02_draft_folder_merge.py")


if __name__ == "__main__":
    main()
