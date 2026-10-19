"""s03 · Delivery: its workbench and its skill: s03-delivery-workbench-skill.excalidraw (haipipe-studio).

One dense frame (JL 261010: one idea, one frame): Jobs and Tasks make outputs, the Block keeps them in its
one delivery/, and each subfolder leads back to its Job or Task folder; storage named by source today
(b10 s02-D14), kept on 261011 with one table of sends, delivery.md (s03-D05; the dNN cards were dropped); the table, the Delivery screen at the right end of
the top row, and the skill that owns the rule, /haipipe-delivery. Moved here from s09's frame 2 on 261010
(JL: "have a s03 delivery-workbench-skill").

A rebuild keeps whatever a person drew on the canvas (canvas.write, a seed snapshot beside the drawing).

    python build_s03_delivery_workbench_skill.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "s01-overall-tree-structure"))
sys.path.insert(0, str(HERE.parent / "_build"))
import build_ladder_v4 as L  # noqa: E402  (the shared drawing helpers)
sys.path.insert(0, str((HERE / "../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts").resolve()))
import canvas  # noqa: E402  (haipipe-studio's merge-safe writer)

INK, RED, SANS, MONO = L.INK, L.RED, L.SANS, L.MONO
text, path, base = L.text, L.path, L.base


def card(x, y, w, h, title, body, size=24, body_size=21, body_color=INK):
    base("rectangle", x, y, w, h, INK, 1.5)
    text(x + 22, y + 16, title, size)
    if body:
        text(x + 22, y + 16 + size * 1.25 + 14, body, body_size, body_color)


def note(x, y, what, date="261010"):
    e = canvas.change_note(x, y, what, date, L.FRAME[0], 17)
    e["id"] = f"e{len(L.els)}"
    L.els.append(e)


DELIVERY_TREES = [  # (title, lines): Paper-ScalingGlucose-NatSeries2026/delivery/, read off the disk 261010
    ("named by its source (s02-D14, kept by s03-D05)", [
        ("delivery/", ""),
        ("├── delivery.md", "one row per send: date · for · from · status"),
        ("└── j01_v1009_nmi/", "links to the Job folder j01_v1009_nmi/"),
        ("    ├── latex/  word/", "the whole paper"),
        ("    ├── t00_abstract/ … t21_extended-data/", "each links to its Task folder"),
        ("    └── build.py  paper-build.toml", "how it is built"),
    ]),
]
DELIVERY_OPEN = [
    "? a send that pulls from several Blocks: its own Block, as a paper Board already is",
    "? a Report's own build (delivery/reports/qNN_<topic>/): a row in delivery.md too",
    "? Delivery rows take the Studio's groups (Current and tags)",
]


def delivery_design(x0):
    """The one frame: Jobs and Tasks make outputs, the Block keeps them, one row per send."""
    text(x0, 0, "Delivery: Jobs and Tasks make outputs, the Block keeps them, one row per send", 34)
    text(x0, 52, "The Studio's rule: one per Block, opened from every level. "
                 "Example: Proj11-CGM-FM papers/Paper-ScalingGlucose-NatSeries2026.", 21)
    makers = [("TASK  t01_introduction", "its section, built to latex/"),
              ("TASK  t02_results", "its section, built to latex/"),
              ("JOB  j01_v1009_nmi", "the whole paper: latex/ word/ pdf")]
    for i, (title, body) in enumerate(makers):
        y = 160 + i * 150
        card(x0, y, 560, 110, title, body, 23, 20)
        path([(x0 + 568, y + 55), (x0 + 702, 455)])
    text(x0 + 600, 140, "make", 20)
    card(x0 + 710, 380, 540, 150, "BLOCK  delivery/j01_v1009_nmi/", "kept once, at the Block\nJobs and Tasks keep no delivery/", 23, 20)
    note(x0 + 1270, 444, "named by its source; a send is a row", "261011")      # beside the card it describes
    path([(x0 + 980, 538), (x0 + 980, 642)])
    text(x0 + 1000, 572, "a person sends it", 20)
    card(x0 + 710, 650, 540, 130, "SENT  to NMI", "a row in delivery.md: draft → sent\nset by a person, never by a build", 23, 20)
    card(x0, 1080, 1250, 140, "SKILL  /haipipe-delivery  (skills/1_base/project)",
         "owns: the Block's delivery/, its paths, the Delivery view, sent by a person\n"
         "builds by: haipipe-draft-delivery · haipipe-paper-assemble · haipipe-design-delivery · haipipe-cowork", 23, 20)
    note(x0, 1232, "the skill haipipe-delivery is made: one owner for the Block-only rule (JL)")
    text(x0, 840, "Rules", 25)
    text(x0, 884, "Jobs and Tasks make deliveries but keep no delivery/; they keep their own Report (s09-D02)\n"
                  "every writer goes through one helper, haipipe-draft/src/common.py (s02-D14)\n"
                  "Runs and Results stay with their source; only built files land in delivery/\n"
                  "opened from Job j01, Delivery is the Block's, with j01 picked in its source row (s03-D06)\n"
                  "Delivery sits at the right end of the top row: Studio | Block · Job · Task | Delivery", 20)
    xr = x0 + 1360
    text(xr, 140, "Storage", 25)
    y = 190
    for title, lines in DELIVERY_TREES:
        text(xr, y, title, 22)
        for i, (line, meaning) in enumerate(lines):
            text(xr, y + 40 + i * 30, line, 20, INK, MONO)
            if meaning:
                text(xr + 560, y + 41 + i * 30, meaning, 20)
        y += 40 + len(lines) * 30 + 40
    card(xr, 560, 540, 230, "delivery.md  · one row per send",
         "date     for          from        status\n261009   NMI          j01_v1009   sent\n"
         "261012   co-authors   j01_v1009   draft\na resend is a row, not a copy", 22, 20)
    note(xr, 800, "dNN dropped: the path stays the link, and dNN is a design in b12", "261011")
    card(xr + 580, 560, 560, 230, "Delivery · opened from Job j01",
         "the Block's Delivery, not j01's own\n[ Paper Board ] [ j01 · v1009 nmi ] [ j01 › t00 ]\n"
         "its part: delivery/j01_v1009_nmi/ · from j01\nthe Block's own view ends with By source", 22, 20)
    note(xr + 580, 800, "from a Job or Task: the Block's Delivery, its source picked", "261011")
    for i, q in enumerate(DELIVERY_OPEN):
        text(xr, 860 + i * 36, q, 21, RED)


def main():
    out = HERE / "s03-delivery-workbench-skill.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    fr = L.open_frame("Delivery: one per Block, one row per send")
    delivery_design(0)
    L.close_frame(fr)
    tools = L.tools_frame(                                # the skill's folder and its code (JL 261011)
        "In Tools: haipipe-delivery", ["1_base/project/haipipe-delivery"],
        [("servers/workbench/frame.py", ["delivery_parts", "_delivery_row", "delivery_by_source"]),
         ("skills/1_base/draft/haipipe-draft/src/common.py",
          ["delivery_owner", "delivery_dir", "delivery_source", "delivery_relative"])],
        around=["haipipe-draft-delivery builds a Page's lanes", "haipipe-paper-assemble builds the paper",
                "haipipe-design-delivery releases a design Job", "haipipe-cowork keeps a drafted email or reply",
                "haipipe-related keeps what came in, the twin"],
        note="its skill's folder and code, read from disk (JL)")
    canvas.grid(L.els, [[fr["id"], tools["id"]]])
    for e in canvas.off_palette(L.els):                  # the look: black, red, green only
        print("off the studio palette:", e["type"], e.get("text", "")[:40])
    canvas.write(out, list(L.els), "build_s03_delivery_workbench_skill.py")


if __name__ == "__main__":
    main()
