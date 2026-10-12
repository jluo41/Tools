"""s04 · Paper Related: venues and related papers: s04-paper-related.excalidraw, drawn by this builder (haipipe-studio).

One frame: where this view sits in a paper Board, what b10 already decided for every Block, and what paper
still has to settle (red). Made in the b16 reorganization (261011, JL: "you just propose it").

    python build_s04_paper_related.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str((HERE / "../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts").resolve()))
import canvas  # noqa: E402  (haipipe-studio's merge-safe writer)

INK, RED = canvas.INK, canvas.RED
TITLE = 's04 · Paper Related: venues and related papers'
TOPIC = "what a paper Board sits beside. The Board keeps the related work and stays venue-free (s01-D01, D02); each version Job is attached to one venue (s01-D03). The Block's `related/` shelf (b10 s01-D34) holds one table, `related/related.md` (kind · date · item · link · feeds · group), and its subfolders meetings/ · papers/ · files/ · emails/, each kept as it came (/haipipe-related). A row's groups on the Studio's bar are its subfolder first, then its `group` cell, comma-separated, a paper's research questions among them (b10 s04-D07, D08, D09). This topic settles where venues and related papers go on that shelf, and who writes them. Its decisions start at s04-D06: s04-D01..D05 are the retired Story decisions, kept by their old ids in s01's notes."
DISK = ['<paper Board>/related/', '├── related.md            one row per item: paper, dataset, code, venue?', '└── meetings/ · papers/ · files/ · emails/   as they came, each a group', '<paper Board>/venues/<venue>/   ? today, written by haipipe-paper-venue']
B10 = ["Related folds inside the Studio, under its topic cards (b10 s04-D05, 261011);",
       "the top row stays Guide · Studio | Block · Job · Task | Delivery",
       "b10 s01-D34: related/ keeps its name, one table",
       "paper: Description is now Scope · Venue · Resources (paper_theme)"]
OPEN = ['Venues: rows of kind venue in related/related.md, or their own venues/ folder?', 'Related papers by research question (s01-D05, today in Block › Report): keep there, or move to Related?', "Who writes related/: haipipe-discovery's Runs, haipipe-paper-venue, or a person by hand?", "An email that carries comments: related/emails/, cited by the comments batch, or the batch's feedback/ as today?"]
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
    els.append(canvas.change_note(1284, 720, "Related now folds inside the Studio (b10 s04-D05)", "261011", f))
    text(60, 870, "OPEN", 24, f, RED)
    text(60, 912, "\n".join("? " + wrap(o, 150) for o in OPEN), 21, f, RED)
    canvas.write(HERE / 's04-paper-related.excalidraw', els, 'build_s04_paper_related.py')


if __name__ == "__main__":
    main()
