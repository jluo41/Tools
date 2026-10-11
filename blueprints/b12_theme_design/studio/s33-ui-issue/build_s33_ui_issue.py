"""b12 s33 · UI issues: s33-ui-issue.excalidraw, the design workbench's open problems as one review found them
(JL 261008: "review the Design workbench as it is now and list every problem").

One source, issues.yaml beside this file: each problem (rank · owner · where · what is wrong · what it should be ·
evidence) and the list of what works well. The drawing reads left to right:

    title frame        what was reviewed, how, the counts per owner, the change notes
    one frame per owner, worst first:  Block tab (s11) · Job tab (s12) · Task tab (s13) · shared frame (b03)
    works well         what to keep

Each problem is a box: its rank and where, what is wrong (red: open), what it should be, its evidence. A fix
closes a problem: mark it fixed in issues.yaml (`fixed: <YYMMDD>`) and rebuild; it then shows a green note.

    python build_s33_ui_issue.py
    python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py \
        s33-ui-issue.excalidraw s33-ui-issue.png 1

Marks a person draws on the canvas are kept on rebuild (canvas.write).
"""
from __future__ import annotations

import random
import sys
import textwrap
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))
import canvas  # noqa: E402

INK, RED, GREEN = canvas.INK, canvas.RED, canvas.GREEN
SANS, MONO = 2, 3
OUT = HERE / "s33-ui-issue.excalidraw"
DATA = yaml.safe_load((HERE / "issues.yaml").read_text(encoding="utf-8"))

random.seed(33)
els: list = []
FRAME = [None]

OWNERS = [("s11", "Block tab · s11 design Block"), ("s12", "Job tab · s12 design Job"),
          ("s13", "Task tab · s13 design Task"), ("b03", "Shared frame · b03 workbench")]
COL_W, BOX_W, GAP = 980, 900, 40


def base(kind, x, y, w, h, stroke=INK, sw=1, dashed=False):
    e = {"id": f"v{len(els)}", "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
         "strokeColor": stroke, "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": sw,
         "strokeStyle": "dashed" if dashed else "solid", "roughness": 1, "opacity": 100, "groupIds": [],
         "frameId": FRAME[0], "roundness": None, "seed": random.randint(1, 2**31 - 1), "version": 1,
         "versionNonce": random.randint(1, 2**31 - 1), "isDeleted": False, "boundElements": [], "updated": 1,
         "link": None, "locked": False}
    els.append(e)
    return e


def text(x, y, s, size=16, color=INK, font=SANS, max_w=None):
    lines = s.split("\n")
    w = max(len(l) for l in lines) * size * (0.62 if font == MONO else 0.5)
    e = base("text", x, y, min(w, max_w) if max_w else w,
             len(lines) * size * 1.25, color)
    e.update(text=s, originalText=s, fontSize=size, fontFamily=font, textAlign="left", verticalAlign="top",
             containerId=None, autoResize=True, lineHeight=1.25, roughness=0)
    return e


def wrap(s, width):
    return "\n".join(textwrap.wrap(str(s), width)) or "—"


def open_frame(name):
    FRAME[0] = None
    fr = base("frame", 0, 0, 10, 10)
    fr["name"] = name
    FRAME[0] = fr["id"]
    return fr


def close_frame(fr, pad=60):
    xs, ys = [], []
    for e in els:
        if e.get("frameId") == fr["id"]:
            xs += [e["x"], e["x"] + e["width"]]
            ys += [e["y"], e["y"] + e["height"]]
    fr.update(x=min(xs) - pad, y=min(ys) - pad, width=max(xs) - min(xs) + 2 * pad, height=max(ys) - min(ys) + 2 * pad)
    FRAME[0] = None


def issue_box(x, y, it):
    """One problem: rank · where, what is wrong (red, open), what it should be, evidence; returns its bottom."""
    fixed = it.get("fixed")
    head = wrap(f'#{it["rank"]}  {it["where"]}', 90)
    wrong = wrap(it["wrong"], 110)
    should = wrap("→ " + it["should"], 110)
    ev = wrap("evidence: " + it["evidence"], 105)
    cy = y + 16
    parts = []
    for s, size, color, font in ((head, 18, INK, SANS), (wrong, 16, GREEN if fixed else RED, SANS),
                                 (should, 16, INK, SANS), (ev, 13, INK, MONO)):
        parts.append((cy, s, size, color, font))
        cy += len(s.split("\n")) * size * 1.25 + 8
    if fixed:
        parts.append((cy, f"✎ {fixed} fixed", 15, GREEN, SANS))
        cy += 15 * 1.25 + 8
    h = cy - y + 8
    base("rectangle", x, y, BOX_W, h, INK, 1, dashed=bool(fixed))
    for py, s, size, color, font in parts:
        text(x + 18, py, s, size, color, font, max_w=BOX_W - 36)
    return y + h


issues = sorted(DATA["issues"], key=lambda i: i["rank"])

# ── title frame ──────────────────────────────────────────────────────────────────────────────
fr = open_frame("s33 · UI issues")
text(0, 0, "s33 · Design workbench: UI issues", 36)
text(0, 56, wrap(DATA["reviewed"], 120), 16)
y = 56 + len(wrap(DATA["reviewed"], 120).split("\n")) * 20 + 20
counts = "   ".join(f'{label.split(" · ")[0]}: {sum(i["owner"] == key for i in issues)}' for key, label in OWNERS)
text(0, y, f"{len(issues)} problems, ranked worst first   ·   {counts}", 18)
text(0, y + 34, "red = open problem · black = what it should be · green = fixed (dashed box)", 14)
notes = DATA.get("changes", [])
for k, n in enumerate(notes):
    text(0, y + 70 + k * 22, f"✎ {n}", 15, GREEN)
close_frame(fr)
title_bottom = fr["y"] + fr["height"]

# ── one frame per owner, side by side ────────────────────────────────────────────────────────
x0, top = 0, title_bottom + 140
for key, label in OWNERS:
    mine = [i for i in issues if i["owner"] == key]
    fr = open_frame(label)
    text(x0, top, f"{label}   ({len(mine)})", 24)
    y = top + 50
    for it in mine:
        y = issue_box(x0, y, it) + GAP
    if not mine:
        text(x0, y, "none found", 16)
    close_frame(fr)
    x0 += COL_W + 120

# ── works well ───────────────────────────────────────────────────────────────────────────────
fr = open_frame("works well · keep")
text(x0, top, "Works well · keep", 24)
y = top + 50
for k, w in enumerate(DATA.get("works_well", []), 1):
    s = wrap(f"{k}. {w}", 70)
    text(x0, y, s, 16, max_w=BOX_W)
    y += len(s.split("\n")) * 20 + 14
close_frame(fr)

canvas.write(OUT, els, "build_s33_ui_issue.py")
print(f"wrote {OUT.name}: {len(issues)} problems, {len(DATA.get('works_well', []))} keep")
