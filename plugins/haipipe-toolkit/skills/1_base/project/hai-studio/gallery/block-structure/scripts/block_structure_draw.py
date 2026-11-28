"""Draw a Block Structure topic's one drawing from its structure.md: the folders as a tree of folder and file
pictures, the Job-Task levels as steps, the Studio bands as a column of topics (b17 s71, Draw: "the folder, the
Job-Task levels and the Studio bands of this Block type, drawn as a pattern ... the same names as Structure").

    <host venv python> block_structure_draw.py <topic> [--check]

Reads `<topic>/structure.md` (the same file the Structure page is built from, so the names cannot differ) and writes
`<topic>/<topic>.excalidraw` and its `.png` preview. A person's marks on the drawing are kept (canvas.write).
`--check` writes nothing and exits 1 when the drawing no longer holds every name of structure.md.
"""
from __future__ import annotations

import json
import os
import random
import re
import subprocess
import sys
from pathlib import Path

SPACE = next(p for p in Path(__file__).resolve().parents if (p / "plugins" / "haipipe-toolkit").is_dir())
STUDIO = Path(__file__).resolve().parents[3] / "scripts"                    # hai-studio/scripts: the shared scripts
sys.path.insert(0, str(STUDIO))
import icons  # noqa: E402
import quick_draw as Q  # noqa: E402

PARTS = ("Folder", "Job-Task", "Studio")
LEVEL = {"Job group": "#7048e8", "Job name": "#1971c2", "Task group": "#2b8a3e", "Task name": "#c2410c"}
LEADS = {"Job group": "sorted into", "Job name": "holds", "Task group": "split into", "Task name": "holds"}
STUDIO_INK, GREY, FOLDER = "#0b7285", "#64748b", ("#996515", "#f8c44f")
ZONES = {"Folder": 40, "Job-Task": 800, "Studio": 1520}
SUBS = {"Folder": "what a Block of this type holds on disk", "Job-Task": "how its Jobs and Tasks are sorted",
        "Studio": "where its topics are kept: one band, one Studio Type"}


def read(path: Path) -> dict[str, list[tuple[int, str, str]]]:
    """{part: [(depth, name, note)]} from one structure.md; the hover after `  | ` is not drawn."""
    out, part = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        head = re.match(r"^##\s+(.+?)\s*$", line)
        if head:
            part = head.group(1)
            out[part] = []
        elif part and re.match(r"^> ?\s*\S", line):
            row = line[1:].removeprefix(" ").rstrip().partition("  | ")[0]
            name, _, note = row.strip().partition("  # ")
            out[part].append(((len(row) - len(row.lstrip(" "))) // 2, name.strip(), note.strip()))
    return out


def words(key, x, y, text, size=24, color=Q.ON, code=False):
    els = Q.text(key, x, y, text, size, color)
    for el in els:
        if not code:
            el["fontFamily"] = 6
        el["width"] = max(len(t) for t in text.splitlines()) * size * 0.62
    return els


def folder(key, x, y, s=1.0):
    """The Files pane's folder: a tab and a body."""
    stroke, fill = FOLDER
    pts = [(x, y + 8 * s), (x, y), (x + 20 * s, y), (x + 26 * s, y + 8 * s), (x + 54 * s, y + 8 * s), (x + 54 * s, y + 42 * s),
           (x, y + 42 * s)]
    return icons.poly(key, pts, stroke, fill, width=2) + icons.line(key + "_l", [(x, y + 15 * s), (x + 54 * s, y + 15 * s)], stroke, 2)


def page(key, x, y, w=40, h=52, color="#64748b"):
    """A file: a sheet with a folded corner and its lines, at any size."""
    c = w * 0.3
    els = icons.poly(key, [(x, y), (x + w - c, y), (x + w, y + c), (x + w, y + h), (x, y + h)], color, "#ffffff", width=2)
    els += icons.poly(key + "_fd", [(x + w - c, y), (x + w - c, y + c), (x + w, y + c)], color, "#e2e8f0", width=2)
    for k in range(3):
        yy = y + h * (0.48 + 0.16 * k)
        els += icons.line(f"{key}_t{k}", [(x + w * 0.2, yy), (x + w * (0.8 - 0.25 * (k == 2)), yy)], color, 2)
    return els


def stack(key, x, y, color):
    """A group: three things of one kind, as three circles."""
    return [dict(e, strokeColor=color, backgroundColor="#ffffff") for i in range(3) for e in Q.dot(f"{key}_{i}", x + 16 + i * 32, y + 30, 14)]


def tint(name: str) -> str:
    """A folder row carries the colour of the zone that explains it."""
    return LEVEL["Job name"] if re.match(r"j(NN|\d\d)", name) else LEVEL["Task name"] if re.match(r"t(NN|\d\d)", name) \
        else STUDIO_INK if re.match(r"s(NN|\d\d)", name) else Q.ON


def draw_folder(rows, x0, y0):
    els, at, step = [], {}, 74
    for i, (depth, name, _) in enumerate(rows):
        x, y = x0 + depth * 58, y0 + i * step
        at[i] = (x, y)
        if name.endswith("/"):
            els += folder(f"f{i}", x, y)
        else:
            els += page(f"f{i}", x + 8, y - 4, 38, 50)
        els += words(f"f{i}_n", x + 70, y + 6, name, 26, tint(name), code=True)
        parent = next((j for j in range(i - 1, -1, -1) if rows[j][0] == depth - 1), None)
        if parent is not None:
            px, py = at[parent]
            els += Q.line(f"f{i}_b", [(px + 27, py + 46), (px + 27, y + 22), (x - 8, y + 22)], "#cbd5e1", 2)
    return els


def draw_levels(rows, x0, y0):
    els, at, step = [], {}, 150
    for i, (depth, name, note) in enumerate(rows):
        x, y, color = x0 + depth * 78, y0 + i * step, LEVEL.get(note, "#176353")
        at[i] = (x, y)
        if note in ("Job group", "Task group"):
            els, gap = els + stack(f"l{i}", x, y + 2, color), 124
        elif note == "Job name" and "people" in name:
            els, gap = els + icons.person(f"l{i}", x + 20, y - 22, "off", s=0.6), 124
        elif note == "Job name":
            els, gap = els + icons.laptop(f"l{i}", x, y - 22, "off"), 214
        elif note == "Task name":
            els, gap = els + page(f"l{i}", x + 14, y - 16, 66, 86, color), 124
        else:
            els, gap = els + folder(f"l{i}", x, y - 8, 1.6), 124
        els += words(f"l{i}_n", x + gap, y, name, 30, color, code=note in ("Job name", "Task name"))
        if note:
            els += words(f"l{i}_r", x + gap, y + 42, note, 21, GREY)
        parent = next((j for j in range(i - 1, -1, -1) if rows[j][0] == depth - 1), None)
        if parent is not None:
            px, py = at[parent]
            els += Q.arrow(f"l{i}_a", [(px + 40, py + 104), (px + 40, y + 30), (x - 8, y + 30)], color)
            first = not any(r[0] == depth for r in rows[parent + 1:i])
            if first:
                els += words(f"l{i}_w", px + 52, py + 110, LEADS.get(note, "holds"), 20, GREY)
    return els


def draw_bands(rows, x0, y0, room):
    bands = [i for i, r in enumerate(rows) if r[0] == 1]
    step = max(118, min(170, room // max(1, len(bands))))
    els = []
    for k, i in enumerate(bands):
        _, name, note = rows[i]
        topics = [r[1] for r in rows[i + 1:] if r[0] == 2][: sum(1 for r in rows[i + 1: (bands[k + 1] if k + 1 < len(bands) else len(rows))])]
        y = y0 + k * step
        els += page(f"s{k}", x0, y, 58, 76, STUDIO_INK)
        els += words(f"s{k}_n", x0 + 84, y - 4, name, 28, STUDIO_INK)
        els += words(f"s{k}_t", x0 + 84, y + 34, note, 20, GREY)
        if topics:
            els += words(f"s{k}_p", x0 + 84, y + 62, " · ".join(topics), 20, Q.ON, code=True)
    return els, len(bands)


def drawing(topic: Path) -> list:
    random.seed(sum(map(ord, topic.name)))
    parts = read(topic / "structure.md")
    kind = parts["Job-Task"][0][1].strip("〈〉")
    els = words("title", 40, 20, f"{kind}: its folders, its Job-Task levels, its Studio bands", 40, Q.TITLE)
    for part, x in ZONES.items():
        els += words(f"z_{part}", x, 112, part, 34, Q.TITLE) + words(f"z_{part}_s", x, 158, SUBS[part], 21, GREY)
    els += draw_folder(parts["Folder"], ZONES["Folder"], 230)
    els += draw_levels(parts["Job-Task"], ZONES["Job-Task"], 240)
    bottom = 230 + max(len(parts["Folder"]) * 74, len(parts["Job-Task"]) * 150)
    bands, n = draw_bands(parts["Studio"], ZONES["Studio"], 230, max(bottom - 230, 700))
    els += bands
    levels = len({r[2] for r in parts["Job-Task"] if r[2]})
    els += icons.big_number("n_levels", ZONES["Job-Task"] + 560, 104, levels, "levels" if levels != 1 else "level", LEVEL["Job name"])
    els += icons.big_number("n_bands", ZONES["Studio"] + 760, 104, n, "bands", STUDIO_INK)
    for i, x in enumerate((ZONES["Job-Task"] - 50, ZONES["Studio"] - 50)):
        els += Q.line(f"rule{i}", [(x, 112), (x, max(bottom, 230 + n * 118))], "#e2e8f0", 2)
    if any(r[2].endswith("group") for r in parts["Job-Task"]):
        els += words("note", 40, max(bottom, 230 + n * 118) + 30, "A group is a named range of numbers on a `bands:` line, never a folder.", 24, GREY)
    return els


def names(topic: Path) -> list[str]:
    return [name for rows in read(topic / "structure.md").values() for _, name, _ in rows]


def main(argv: list[str]) -> int:
    check = "--check" in argv
    topic = (SPACE / next(a for a in argv if not a.startswith("--"))).resolve()
    out = Path(next((a.split("=", 1)[1] for a in argv if a.startswith("--out=")), topic / f"{topic.name}.excalidraw"))
    if check:
        text = " ".join(e.get("text", "") for e in json.loads(out.read_text(encoding="utf-8"))["elements"]) if out.is_file() else ""
        missing = [n for n in names(topic) if n not in text]
        print(f"{'❗' if missing else '✅'} {topic.name}: drawing" + (f" lacks {', '.join(missing[:4])}" if missing else ""))
        return 1 if missing else 0
    els = drawing(topic)
    if "--out=" in " ".join(argv):
        Q.write(out, els)
    else:
        from canvas import write as canvas_write
        canvas_write(out, els, "hai-studio block_structure_draw", palette=False)
    preview = os.environ.get("STUDIO_PREVIEW_PYTHON", "").split() or ["uv", "run", "--quiet", "--python", "3.13", "--with", "pillow", "python"]
    subprocess.run(preview + [str(STUDIO / "render_png.py"), str(out), str(out.with_suffix(".png")), "1"], check=True)
    print(f"Drew {out.name}: {len(els)} shapes.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
