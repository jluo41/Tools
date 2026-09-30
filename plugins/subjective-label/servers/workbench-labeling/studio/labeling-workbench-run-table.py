"""Draw Part 1 of labeling-workbench-design.excalidraw from labeling-workbench-run-table.md.

There is one drawing, labeling-workbench-design.excalidraw. Its Part 1 (every
element whose id starts with `rt-`) is generated from the Markdown table
(AGENTS.md rule 6): edit the .md (a row, a Review tick, a Space question), then
run

    .venv/bin/python Tools/plugins/subjective-label/servers/workbench-labeling/studio/labeling-workbench-run-table.py

The script replaces the `rt-` elements and moves the later parts (the sequence,
the page, the files, the rules) up or down so they start below Part 1; it never
changes their content.

Part 1 has one column per Space, one box per View (its name and View Skill),
and one row per Run Type in table order: green rows are built, gray rows are
not, a dashed row is a gate, the square on the left is JL's Review tick, and
the blue tag on the right is what the S-Label-4 job has on disk.
"""
import json
import random
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "labeling-workbench-run-table.md"
DRAWING = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "labeling-workbench-design.excalidraw"
HEADER = {"l5-title", "l5-subtitle"}
random.seed(260930)
NOW = int(time.time() * 1000)
E = []

BLUE, GREEN, INK, MUTED, RULE = "#1864ab", "#2b8a3e", "#1e1e1e", "#868e96", "#ced4da"
BUILT_BG, TODO_BG, VIEW_BG = "#ebfbee", "#f1f3f5", "#f8f9fa"
SPACES = ["Data", "Labeling", "Quality", "Delivery"]


# ---- read the Markdown source -------------------------------------------------
def section(md: str, title: str) -> str:
    m = re.search(rf"^## {re.escape(title)}\s*$(.*?)(?=^## |\Z)", md, re.M | re.S)
    return m.group(1) if m else ""


def table_rows(block: str) -> list[list[str]]:
    rows = []
    for line in block.splitlines():
        if not line.startswith("|") or re.fullmatch(r"\|[\s|:-]+\|", line.strip()):
            continue
        rows.append([c.strip().replace("`", "") for c in line.strip().strip("|").split("|")])
    return rows[1:]  # drop the header row


md = SOURCE.read_text(encoding="utf-8")
questions = dict(re.findall(r"^- \*\*(\w+)\*\*: (.+)$", section(md, "Spaces"), re.M))
runs = [dict(zip(("step", "where", "run", "does", "skill", "worker", "built", "job", "review"), r))
        for r in table_rows(section(md, "Table"))]
skills = [dict(zip(("name", "version", "role"), r)) for r in table_rows(section(md, "The Skills we have"))]
counts = re.findall(r"^- (.+)$", section(md, "Counts"), re.M)

layout: dict[str, dict[str, list[dict]]] = {s: {} for s in SPACES}
for r in runs:
    space, view = (p.strip() for p in r["where"].split("›"))
    layout[space].setdefault(view, []).append(r)


# ---- Excalidraw elements --------------------------------------------------------
def base(id_, type_, x, y, w, h, stroke=INK, bg="transparent", dashed=False, rounded=True, width=2):
    return {"id": id_, "type": type_, "x": x, "y": y, "width": w, "height": h, "angle": 0,
            "strokeColor": stroke, "backgroundColor": bg, "fillStyle": "solid", "strokeWidth": width,
            "strokeStyle": "dashed" if dashed else "solid", "roughness": 0, "opacity": 100,
            "groupIds": [], "frameId": None, "roundness": {"type": 3} if rounded else None,
            "seed": random.randint(1, 2**31 - 1), "version": 1,
            "versionNonce": random.randint(1, 2**31 - 1), "isDeleted": False,
            "boundElements": [], "updated": NOW, "link": None, "locked": False}


def text(id_, x, y, s, size=16, color=INK, mono=False):
    lines = s.split("\n")
    w = max(len(line) for line in lines) * size * (0.6 if mono else 0.56)
    e = base("rt-" + id_, "text", x, y, w, len(lines) * size * 1.25, stroke=color, rounded=False)
    e.update(text=s, originalText=s, fontSize=size, fontFamily=3 if mono else 8,
             textAlign="left", verticalAlign="top", containerId=None, autoResize=True,
             lineHeight=1.25)
    E.append(e)


def rect(id_, x, y, w, h, stroke=INK, bg="transparent", dashed=False, width=2):
    E.append(base("rt-" + id_, "rectangle", x, y, w, h, stroke, bg, dashed, width=width))


def job_tag(value: str) -> str:
    """'rl08 (blocked)' stays short; 'none' draws nothing."""
    return "" if value in ("", "none") else re.sub(r"[()]", "", value)


drawing = json.loads(DRAWING.read_text(encoding="utf-8"))
kept = [e for e in drawing["elements"] if not e["id"].startswith("rt-") and not e.get("isDeleted")]
header = [e for e in kept if e["id"] in HEADER]
rest = [e for e in kept if e["id"] not in HEADER]

CW, GAP, ROW, VIEW_HEAD = 640, 40, 52, 70
X = [48 + i * (CW + GAP) for i in range(len(SPACES))]
P1 = max(e["y"] + e["height"] for e in header) + 36 if header else 24
TOP = P1 + 96

text("title", 48, P1, "1 · Spaces, Views, Run Types, and their Skills", 28)
text("legend", 48, P1 + 46, "Green row: built (an engine worker exists) · gray row: not built yet · "
     "dashed row: a human gate, not a Run · square: reviewed with JL · blue: what S-Label-4 has", 17, MUTED)


def column_height(views: dict[str, list[dict]]) -> int:
    return 120 + sum(VIEW_HEAD + len(rows) * ROW + 28 for rows in views.values())


BH = max(column_height(layout[s]) for s in SPACES)
for i, space in enumerate(SPACES):
    x0 = X[i]
    rect(f"s{i}-box", x0, TOP, CW, BH)
    text(f"s{i}-title", x0 + 24, TOP + 20, f"{space} Space", 28)
    text(f"s{i}-asks", x0 + 24, TOP + 60, questions.get(space, ""), 17, BLUE)
    y = TOP + 104
    for v, (view, rows) in enumerate(layout[space].items()):
        h = VIEW_HEAD + len(rows) * ROW + 10
        rect(f"s{i}-v{v}-box", x0 + 16, y, CW - 32, h, RULE, VIEW_BG)
        text(f"s{i}-v{v}-name", x0 + 32, y + 10, view, 22)
        text(f"s{i}-v{v}-skill", x0 + 32, y + 40, rows[0]["skill"], 15, GREEN, mono=True)
        ry = y + VIEW_HEAD
        for k, r in enumerate(rows):
            built = r["built"].startswith("✅")
            gate = r["step"].upper().startswith("G")
            rid = f"s{i}-v{v}-r{k}"
            rect(rid + "-row", x0 + 28, ry, CW - 56, ROW - 6, GREEN if built else RULE,
                 BUILT_BG if built else TODO_BG, dashed=gate, width=1)
            reviewed = not r["review"].startswith("⬜")
            rect(rid + "-tick", x0 + 38, ry + 8, 14, 14, GREEN if reviewed else MUTED,
                 GREEN if reviewed else "transparent", width=1)
            text(rid + "-step", x0 + 62, ry + 5, r["step"].ljust(3), 16, INK if built else MUTED, mono=True)
            text(rid + "-run", x0 + 104, ry + 5, r["run"], 16, INK if built else MUTED, mono=True)
            text(rid + "-does", x0 + 104, ry + 26, r["does"], 13, INK if built else MUTED)
            tag = job_tag(r["job"])
            if tag:
                text(rid + "-job", x0 + CW - 44 - len(tag) * 13 * 0.6, ry + 7, tag, 13, BLUE, mono=True)
            ry += ROW
        y += h + 18

# ---- the Skills that are not View Skills, and the counts --------------------------
SY = TOP + BH + 48
shared = [s for s in skills if not s["role"].startswith("View Skill")]
text("shared-title", 48, SY, "The other Skills (each View's own Skill is in its box above)", 26)
rect("shared-box", 48, SY + 46, 2 * CW + GAP, 40 + len(shared) * 30)
for k, s in enumerate(shared):
    text(f"shared-{k}-name", 72, SY + 66 + k * 30, s["name"], 17, GREEN, mono=True)
    text(f"shared-{k}-role", 72 + 330, SY + 66 + k * 30, f'{s["version"]} · {s["role"]}', 16, INK)
text("declared", X[2], SY + 46,
     "Preparation rows (0a to 0e) declare only their View Skill.\n"
     "Building rows (1 to 13) also declare subjective-label-workflow,\n"
     "label-building and label-building-workflow.\n"
     "Scanning rows (14 to 26) also declare subjective-label-workflow,\n"
     "label-scanning and label-scanning-workflow.", 17, INK)
text("counts", X[2], SY + 46 + 150, "\n".join(counts), 17, BLUE)
FOOT = SY + 46 + 40 + len(shared) * 30 + 24
text("footer", 48, FOOT, "Part 1 is generated from studio/labeling-workbench-run-table.md by "
     "labeling-workbench-run-table.py; edit the .md, then run the script.", 16, MUTED)

# ---- move the later parts below Part 1, unchanged ---------------------------------
if rest:
    dy = (FOOT + 90) - min(e["y"] for e in rest)
    for e in rest:
        e["y"] += dy

drawing["elements"] = header + E + rest
DRAWING.write_text(json.dumps(drawing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(runs), "rows,", len(E), "Part 1 elements,", len(rest), "later elements →", DRAWING)
