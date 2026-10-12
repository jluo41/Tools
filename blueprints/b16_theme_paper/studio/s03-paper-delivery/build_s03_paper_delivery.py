"""s03 · Paper Delivery: the built paper, per version: s03-paper-delivery.excalidraw, drawn by this builder (haipipe-studio).

One frame: where this view sits in a paper Board, what b10 already decided for every Block, and what paper
still has to settle (red). Made in the b16 reorganization (261011, JL: "you just propose it").

    python build_s03_paper_delivery.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str((HERE / "../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts").resolve()))
import canvas  # noqa: E402  (haipipe-studio's merge-safe writer)

INK, RED = canvas.INK, canvas.RED
TITLE = 's03 · Paper Delivery: the built paper, per version'
TOPIC = "the paper Board's one `delivery/` (b10 s09-D05, s01-D32): each version's built paper sits under `delivery/jNN_<version>/` (LaTeX, Word, cover letter), and each Section's own output under `delivery/jNN_<version>/tNN_<section>/`. haipipe-paper-assemble builds the paper from the Sections' outputs; haipipe-delivery owns the folder and the rule that only a person marks a send done. This topic settles what paper adds: the lanes a paper needs, how versions sit side by side, and what a send freezes."
DISK = ['<paper Board>/delivery/', '├── j01_v1009_nmi/latex/   the built paper for one send', '├── j01_v1009_nmi/word/', "├── j01_v1009_nmi/t02_results/latex/   one Section's output", '└── (no Job or Task keeps its own delivery/)']
B10 = ['b10 s03: Delivery is one per Block, like the Studio', 'b10 s02-D18: Delivery sits at the right of the top row']
OPEN = ["The Board's Delivery: each version side by side, or the newest first? (was s33 open 1)", "The cover letter and a rebuttal letter: a Section Task's output, or the version's own?", "A sent version: which files freeze, and where does the send's decision live? (was s33 open 3)", 'The supplement: its own lane, or inside latex/?']
CHANGES = []
els = []


def el(kind, x, y, w, h, **extra):
    e = {"id": f"e{len(els)}", "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
          "strokeColor": INK, "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 1.5,
          "strokeStyle": "solid", "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
          "roundness": None, "seed": 1, "version": 1, "versionNonce": 1, "isDeleted": False,
          "boundElements": [], "updated": 1, "link": None, "locked": False}
    e.update(extra)
    els.append(e)
    return e


def text(x, y, s, size, frame, color=INK, font=6):
    lines = s.split("\n")
    return el("text", x, y, max(len(l) for l in lines) * size * (0.6 if font == 3 else 0.55), len(lines) * size * 1.3,
              text=s, originalText=s, fontSize=size, fontFamily=font, textAlign="left", verticalAlign="top",
              containerId=None, autoResize=True, lineHeight=1.3, frameId=frame, strokeColor=color)


def wrap(s, n=110):
    out, line = [], ""
    for w in s.split():
        if len(line) + len(w) + 1 > n:
            out.append(line); line = w
        else:
            line = (line + " " + w).strip()
    return "\n".join(out + [line])


def main():
    els.clear()
    f = el("frame", 0, 0, 2400, 1300, name="1 · " + TITLE.split(" · ", 1)[1])["id"]
    text(60, 50, TITLE, 36, f)
    for i, (date, what) in enumerate(CHANGES):
        els.append(canvas.change_note(60, 104 + i * 24, what, date, f))
    text(60, 150, wrap(TOPIC), 21, f)
    text(60, 470, "ON DISK", 24, f)
    el("rectangle", 60, 510, 1100, 300, frameId=f)
    text(84, 534, "\n".join(DISK), 20, f, font=3)
    text(1260, 470, "FROM b10 (every Block)", 24, f)
    el("rectangle", 1260, 510, 1080, 300, frameId=f)
    text(1284, 534, "\n".join(B10), 21, f)
    text(60, 870, "OPEN", 24, f, RED)
    text(60, 912, "\n".join("? " + wrap(o, 150) for o in OPEN), 21, f, RED)
    canvas.write(HERE / 's03-paper-delivery.excalidraw', els, 'build_s03_paper_delivery.py')


if __name__ == "__main__":
    main()
