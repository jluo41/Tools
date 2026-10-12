"""s04 · Related: its workbench and its skill: s04-related-workbench-skill.excalidraw (haipipe-studio).

One dense frame, the same shape as s03 (Delivery): what comes in (a meeting, a paper, a file we were
sent, a repo), the Block keeps it once in its related/, one row each in related.md, and the studio
topics and reports it feeds read it from there. The Delivery's twin on the other side: related/ is what
came in, delivery/ what went out (b10 s01-D34, s03-D05). New on 261011 (JL: "s02 studio, s03 delivery,
and s04 related, and s05 report, and s06 run").

A rebuild keeps whatever a person drew on the canvas (canvas.write, a seed snapshot beside the drawing).

    python build_s04_related_workbench_skill.py
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


def note(x, y, what, date="261011"):
    e = canvas.change_note(x, y, what, date, L.FRAME[0], 17)
    e["id"] = f"e{len(L.els)}"
    L.els.append(e)


SOURCES = [  # (title, body): what comes in, and where it lands
    ("MEETING  2026-10-10 18:00", "notes or a transcript → meetings/"),
    ("PAPER  <author><year>", "open PDF → papers/; else a row, its DOI"),
    ("FILE  sent to us", "a draft, a form, slides → files/"),
    ("EMAIL  as it came", "saved from the mail app, .eml → emails/"),
    ("REPO · DATASET · TOOL", "only a row with its link"),
]
STORAGE = [  # (line, meaning): b10's own related/, read off the disk 261011
    ("related/", ""),
    ("├── related.md", "one row per item: kind · date · item · link · feeds · group"),
    ("├── _groups.txt", "the group buttons, in order (s04-D07)"),
    ("├── meetings/", "2026-10-10-1800 <title>.md, as it came"),
    ("├── papers/", "<author><year>.pdf, open-licensed only"),
    ("├── files/", "what we were sent, as it came"),
    ("├── emails/", "<date> <subject>.eml, as it came"),
    ("└── <other>/", "any subfolder: a group of its files"),
]
RELATED_OPEN = [
    "? a Job's own inputs (a site visit's notes): its Job folder, or here with feeds jNN",
    "? the Project's external/ (pinned code and data): rows here that point to it",
]


def related_design(x0):
    """The one frame: what comes in, the Block keeps it once, one row per item, read by studio and reports."""
    text(x0, 0, "Related: what came in, kept once at the Block, one row per item", 34)
    text(x0, 52, "The Studio's rule: one per Block, opened from every level, read only. "
                 "Example: b10's own related/.", 21)
    for i, (title, body) in enumerate(SOURCES):
        y = 160 + i * 128
        card(x0, y, 560, 100, title, body, 23, 20)
        path([(x0 + 568, y + 50), (x0 + 702, 455)])
    note(x0 + 300, 160 + 3 * 128 + 20, "added (JL)")                 # inside the EMAIL card
    text(x0 + 600, 140, "comes in", 20)
    card(x0 + 710, 380, 540, 150, "BLOCK  related/", "kept once, at the Block\nJobs and Tasks keep no related/", 23, 20)
    note(x0 + 732, 500, "holds meetings · papers · files · emails (JL)")       # inside the card it describes
    path([(x0 + 980, 538), (x0 + 980, 642)])
    text(x0 + 1000, 572, "a row's feeds names them", 20)
    card(x0 + 710, 650, 540, 150, "READ BY  studio sNN · reports qNN",
         "a report cites the row, as it cites a Run\na meeting's question becomes a qNN", 23, 20)
    text(x0, 840, "Rules", 25)
    text(x0, 884, "what lands here is not edited again; notes about it go to a studio topic or a report (s01-D34)\n"
                  "only open-licensed PDFs are kept; every other item links out (s01-D21, D27)\n"
                  "a deep read of a paper is a discovery Task's Run, linked from its row\n"
                  "a paper Board builds reference.bib from its paper rows at Delivery\n"
                  "flow: related (in) → studio (think) → Jobs and Tasks (work) → reports (answer) → delivery (out)", 20)
    card(x0, 1080, 1250, 140, "SKILL  /haipipe-related  (skills/1_base/project)",
         "owns: the Block's related/, related.md, its groups, the Related view\n"
         "beside haipipe-studio · haipipe-delivery · haipipe-report · haipipe-run (the In Tools frame)", 23, 20)
    note(x0, 1232, "the skill haipipe-related is made, on its own (JL)")
    xr = x0 + 1360
    text(xr, 140, "Storage", 25)
    text(xr, 190, "one shelf, one table (s01-D34)", 22)
    for i, (line, meaning) in enumerate(STORAGE):
        text(xr, 230 + i * 30, line, 20, INK, MONO)
        if meaning:
            text(xr + 300, 231 + i * 30, meaning, 20)
    card(xr, 500, 560, 230, "related.md  · one row per item",
         "kind      date      item               group\nmeeting   261010    Studio · Report …  meetings\n"
         "email     261009    IRB question       emails, IRB\nrepo      —         <name> ↗          (Untagged)", 22, 20)
    card(xr + 600, 500, 560, 230, "Studio · its second part, Related",
         "▸ s01 … s51   the topic cards\n▾ Related   Current · meetings 1 · + Group\n"
         "   ▸ 261010 研究项目…   [meetings]\n   drag a row onto a group; a row opens its file", 22, 20)
    note(xr, 740, "the Block's in-door, as delivery/ is its out-door")
    note(xr + 600, 740, "folds inside the Studio, under the topics (JL)")
    note(xr + 600, 770, "a row opens the file, Word too (JL)")
    note(xr, 770, "a group column, as the Studio's tags (JL)")      # beside the table it changed
    note(xr + 600, 800, "the Studio's group bar, not the subfolders (JL)")
    note(xr + 600, 830, "a subfolder is a group: meetings/ → meetings (JL)")
    for i, q in enumerate(RELATED_OPEN):
        text(xr, 880 + i * 36, q, 21, RED)


def main():
    out = HERE / "s04-related-workbench-skill.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    fr = L.open_frame("Related: one per Block, one row per item")
    related_design(0)
    L.close_frame(fr)
    tools = L.tools_frame(                                # the skill's folder and its code (JL 261011)
        "In Tools: haipipe-related", ["1_base/project/haipipe-related"],
        [("servers/workbench/frame.py", ["related_items", "_related_folder", "related_view", "studio_related",
                                         "_related_preview", "docx_preview", "eml_preview", "_related_set_groups"]),
         ("servers/workbench/page_reader.py", ["markdown_document"])],
        around=["haipipe-studio: Related folds inside its view", "haipipe-paper builds reference.bib from paper rows",
                "haipipe-discovery: a paper's deep read is a Task's Run", "table-papers: a workbench's papers, not this",
                "haipipe-delivery keeps what went out, the twin"],
        note="its skill's folder and code, read from disk (JL)")
    canvas.grid(L.els, [[fr["id"], tools["id"]]])
    for e in canvas.off_palette(L.els):                  # the look: black, red, green only
        print("off the studio palette:", e["type"], e.get("text", "")[:40])
    canvas.write(out, list(L.els), "build_s04_related_workbench_skill.py")


if __name__ == "__main__":
    main()
