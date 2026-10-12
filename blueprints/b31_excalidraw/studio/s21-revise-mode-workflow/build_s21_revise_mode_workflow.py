"""s21 · Revise mode: how a co-author's file becomes a side-by-side drawing (haipipe-studio).

Two frames in one row, both read from the yaml blocks in this topic's face:
  1. the workflow in one picture: the steps in their lanes, the loop back from a person's edits, step 7
     (read_revise.py draw) opened into its parts, seconds per rebuild as bars, and where the effort went;
  2. how b04_prep_ai's s04 got here on 2026-10-11: JL's asks, what changed, the pass, then the open points.
A rebuild keeps whatever a person drew on the canvas (canvas.write, a seed snapshot beside the drawing).

    python build_s21_revise_mode_workflow.py
"""
import re
import subprocess
import sys
import textwrap
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
STUDIO = (HERE / "../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts").resolve()
sys.path.insert(0, str(STUDIO))
import canvas  # noqa: E402  (haipipe-studio's merge-safe writer)

INK, RED, GREEN = canvas.INK, canvas.RED, canvas.GREEN
FACE = HERE / f"{HERE.name}.md"
els = []
FRAME = [None]


def data():
    """Every yaml block of the face, merged: workflow_steps, draw_steps, seconds, effort, rounds, peers, open."""
    out = {}
    for block in re.findall(r"```yaml\n(.*?)\n```", FACE.read_text(encoding="utf-8"), re.S):
        out.update(yaml.safe_load(block))
    return out


def el(kind, x, y, w, h, **extra):
    e = {"id": f"e{len(els)}", "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
         "strokeColor": INK, "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 1,
         "strokeStyle": "solid", "roughness": 0, "opacity": 100, "groupIds": [], "frameId": FRAME[0],
         "roundness": None, "seed": len(els) + 1, "version": 1, "versionNonce": len(els) + 1, "isDeleted": False,
         "boundElements": [], "updated": 1, "link": None, "locked": False}
    e.update(extra)
    els.append(e)
    return e


def text(x, y, s, size=20, color=INK, code=False):
    lines = s.split("\n")
    return el("text", x, y, max(len(l) for l in lines) * size * (0.6 if code else 0.55), len(lines) * size * 1.25,
              text=s, originalText=s, fontSize=size, fontFamily=canvas.CODE_FONT if code else canvas.FONT,
              textAlign="left", verticalAlign="top", containerId=None, autoResize=True, lineHeight=1.25,
              strokeColor=color)


def para(x, y, s, width, size=20, color=INK, code=False):
    """Wrapped text; returns the y below it."""
    s = "\n".join(textwrap.wrap(" ".join(str(s).split()), max(8, int(width / (size * (0.6 if code else 0.55))))))
    return y + text(x, y, s, size, color, code)["height"]


def box(x, y, w, h, color=INK, sw=1):
    return el("rectangle", x, y, w, h, strokeColor=color, strokeWidth=sw, roundness={"type": 3})


def line(points, color=INK, arrow=True, dashed=False):
    x0, y0 = points[0]
    return el("arrow" if arrow else "line", x0, y0, max(1, max(p[0] for p in points) - x0),
              max(1, max(p[1] for p in points) - y0), strokeColor=color,
              strokeStyle="dashed" if dashed else "solid", points=[[x - x0, y - y0] for x, y in points],
              lastCommittedPoint=None, startBinding=None, endBinding=None, startArrowhead=None,
              endArrowhead="arrow" if arrow else None)


def frame(name, w, h):
    FRAME[0] = None
    f = el("frame", 0, 0, w, h, name=name)
    FRAME[0] = f["id"]
    return f


def workflow(d):
    """Frame 1: the workflow in one picture."""
    W = 2560
    f = frame("s21 · Revise mode: the workflow in one picture", W, 1440)
    para(40, 28, "s21 · Revise mode: how a co-author's file becomes a side-by-side drawing", W - 80, 34)
    para(40, 78, "How b04_prep_ai's s04 (Nes Mathioudakis's SHIFT Task 3.1 file) is drawn, step by step, in sentence "
                 "mode: the updated text comes from a haipipe-draft draft and the Word file is built last. The seconds "
                 "are one rebuild on JL's Mac (2026-10-11); red marks what costs most or is still open.", W - 80, 20)

    # ① the 8 steps in 4 lanes, and the loop back from looking to the plan or the script
    steps = d["workflow_steps"]
    gap, top, bh = 34, 200, 380
    bw = (W - 80 - gap * (len(steps) - 1)) // len(steps)
    xs = [40 + i * (bw + gap) for i in range(len(steps))]
    lanes = {}
    for s, x in zip(steps, xs):
        lanes.setdefault(s["lane"], []).append(x)
    names = {"once": "once per file", "plan": "plan · agent", "draft": "draft · haipipe-draft, haipipe-writing",
             "build": "build · script", "look": "look · a person", "last": "last · delivery"}
    for lane, lx in lanes.items():
        text(lx[0], top - 44, names.get(lane, lane), 23)
        line([(lx[0], top - 12), (lx[-1] + bw, top - 12)], arrow=False)
    for s, x in zip(steps, xs):
        color = RED if s.get("costly") else INK
        box(x, top, bw, bh, color, 2 if s.get("costly") else 1)
        y = para(x + 14, top + 12, f"{s['n']} · {s['title']}", bw - 28, 23) + 6
        y = para(x + 14, y, s["script"], bw - 28, 20, code=True) + 6
        para(x + 14, y, s["what"], bw - 28, 20)
        para(x + 14, top + bh - 34, s["cost"], bw - 28, 20, color)
    for a, b in zip(xs, xs[1:]):
        line([(a + bw + 4, top + bh / 2), (b - 4, top + bh / 2)])
    # the loop: a person's edits back into an earlier step
    lo = top + bh + 34
    at = {s["n"]: x for s, x in zip(steps, xs)}
    lp = d.get("loop") or {}
    if lp:
        a, b = at[lp["from"]] + bw / 2, at[lp["to"]] + bw / 2
        line([(a, top + bh + 4), (a, lo), (b, lo), (b, top + bh + 6)])
        text(min(a, b) + 10, lo + 6, lp["text"], 20)

    # ② step 7 opened: read_revise.py draw
    oy = lo + 70
    seven = next(s for s in steps if s["n"] == 7)
    most = max(d["draw_steps"], key=lambda s: float(re.sub(r"[^\d.]", "", s["cost"]) or 0))
    line([(at[7] + bw / 2, top + bh + 4), (at[7] + bw / 2, oy - 6)], dashed=True)
    text(40, oy, f"7 opened · excalidraw-read/ref/read_revise.py draw: {seven['cost']}, of which {most['cost']} "
                 f"{most['title'][0].lower() + most['title'][1:]}", 23)
    dg, dy, dh = 28, oy + 44, 320
    dw = (W - 80 - dg * (len(d["draw_steps"]) - 1)) // len(d["draw_steps"])
    for i, s in enumerate(d["draw_steps"]):
        x = 40 + i * (dw + dg)
        color = RED if s.get("red") else INK
        box(x, dy, dw, dh, color, 2 if s.get("red") else 1)
        y = para(x + 14, dy + 12, f"{s['k']} · {s['title']}", dw - 28, 23) + 6
        y = para(x + 14, y, s["script"], dw - 28, 20, code=True) + 6
        y = para(x + 14, y, s["what"], dw - 28, 20) + 6
        if s.get("red"):
            para(x + 14, y, s["red"], dw - 28, 20, RED)
        para(x + 14, dy + dh - 34, s["cost"], dw - 28, 20, color)
        if i:
            line([(x - dg + 4, dy + dh / 2), (x - 4, dy + dh / 2)])

    # ③ seconds per rebuild, and where the effort went
    cy = dy + dh + 50
    text(40, cy, "Seconds per rebuild, measured", 23)
    most = max(r["s"] for r in d["seconds"])
    y = cy + 44
    for r in d["seconds"]:
        color = RED if r["s"] == most else INK
        text(40, y, r["step"], 20, color)
        w = max(4, 640 * r["s"] / most)
        el("rectangle", 470, y + 2, w, 22, strokeColor=color, strokeWidth=2 if r["s"] == most else 1)
        text(480 + w, y, f"{r['s']:g} s", 20, color)
        y += 34
    text(1320, cy, "Where the effort went: people and agent", 23)
    y = cy + 44
    for r in d["effort"]:
        y = para(1320, y, r["title"], 1200, 22) + 2
        y = para(1340, y, r["what"], 1180, 20) + 14
    f["height"] = max(y, cy + 44 + 34 * len(d["seconds"])) + 40
    return f


def history(d):
    """Frame 2: how s04 got here, one row per ask, then the peers and the open points."""
    W = 2200
    f = frame("s21 · How b04's s04 got here, 2026-10-11", W, 1440)
    para(40, 28, "How b04's s04 got here: one row per ask, 2026-10-11", W - 80, 34)
    cols = [(40, "#", 40), (90, "JL's words", 640), (760, "What changed", 1060), (1850, "pass", 140),
            (2010, "kept", 150)]
    y = 100
    for x, name, _ in cols:
        text(x, y, name, 23)
    y += 40
    line([(40, y), (W - 40, y)], arrow=False)
    for n, r in enumerate(d["rounds"], 1):
        color = INK if r["kept"] else RED
        y0 = y + 10
        bottoms = [para(cols[0][0], y0, str(n), cols[0][2], 20, color),
                   para(cols[1][0], y0, r["ask"], cols[1][2], 20, color),
                   para(cols[2][0], y0, r["did"], cols[2][2], 20, color),
                   para(cols[3][0], y0, r["pass"] or "-", cols[3][2], 20, color),
                   para(cols[4][0], y0, "kept" if r["kept"] else "turned down", cols[4][2], 20, color)]
        y = max(bottoms) + 10
        line([(40, y), (W - 40, y)], arrow=False)
    y += 30
    text(40, y, "From the peer Blocks", 23)
    y += 40
    for p in d["peers"]:
        y = para(60, y, p, W - 120, 20) + 6
    y += 24
    text(40, y, "Open", 23, RED)
    y += 40
    for n, o in enumerate(d["open"], 1):
        y = para(60, y, f"? {n}. {o}", W - 120, 20, RED) + 6
    f["height"] = y + 40
    return f


def main():
    out = HERE / f"{HERE.name}.excalidraw"
    els.clear()
    d = data()
    f1, f2 = workflow(d), history(d)
    FRAME[0] = None
    canvas.grid(els, [[f1["id"], f2["id"]]])
    for e in canvas.off_palette(els):                    # the look: black, red, green only
        print("off the studio palette:", e["type"], e.get("text", "")[:40])
    canvas.write(out, els, "build_s21_revise_mode_workflow.py")
    subprocess.run([sys.executable, str(STUDIO / "render_png.py"), str(out), str(out.with_suffix(".png"))], check=False)
    print("oversized:", canvas.oversized(els), "| small text:", canvas.small_text(els))


if __name__ == "__main__":
    main()
