"""b16 s04 · the Story into topics and Questions: s04-story-to-topics.excalidraw (Q04, JL 261007).

A paper Board takes b03's shape: its thinking is studio topics (studio/sNN-<topic>/), its answers are
Questions (board.md ## Questions, grouped by topic, each with reports/qNN_<topic>/), and a version tells the
story in its own order (its face's Narrative). The Story and Ideation Pages stop being Pages: each part goes
where it is used. The Story and Ideation skills stay, called as run types from those views.

Frames, top to bottom: 1 · where each part of a Story goes; 2 · the Board after; 3 · the readers that change;
open. A plain prototype: lines-only boxes, placeholders, no names; red = open. Drawn with b04's studio
helpers through b03's canvas.write, so a person's marks survive a rebuild.

    python build_s04_story_to_topics.py [out.excalidraw]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1].parent / "b04_skill_folder" / "studio" / "_build"))
from sketch import GRAY, INK, MONO, RED, SANS, arrow, base, close_frame, open_frame, save, text  # noqa: E402

LINE = 26
STORY = ["Story<L>-<desk>-<idea>.md",          # a Story Page today, division by division
         "§1 Identity",
         "§2 Pitch",
         "§3 Research Questions  (RQ1 … RQn)",
         "§4 Stakes",
         "§5 Evidence Basis and Boundaries",
         "§6 Discovery Roadmap",
         "§7 Task Roadmap",
         "§8 Section Narrative + compile order",
         "Related papers table"]
IDEATION = ["Story00-<direction>.md", "Direction", "Ideas (ranked)", "the admitted idea", "Eliminated ideas"]
# (the parts, where they go, on screen)
HOMES = [("Story00 · all of it", "studio/s01-ideation/  (face: decided · open · feeds)",
          "Idea Studio · and Audience Report › Ideation"),
         ("§1 · §2 · §4", "studio/sNN-story-<telling>/  its face", "Description › Scope · Audience Report › Narrative"),
         ("the Story's drawings", "studio/sNN-story-<telling>/  its drawings", "Idea Studio"),
         ("§3 · one RQ each", "board.md ## Questions (group: <topic>) + reports/qNN_<question>/",
          "Audience Report › High-level logic + Low-level work"),
         ("§5 · §6 · §7", "each report's Work: its evidence, its discovery and Task work",
          "the Question's Work column"),
         ("§8 + compile order", "jNN_v<MMDD>_<desk>/jNN_….md  ## Narrative", "the version's Draft-Main · the build"),
         ("Related papers", "related/related.md (or the topic's face)", "Description › Related")]
AFTER = [("Paper-<Name>/", "Block: the paper"),
         ("├── board.md", "## Questions: Q01 … each with group: <topic>"),
         ("├── studio/", "Idea Studio: think, argue, try"),
         ("│   ├── s01-ideation/", "the ideas: s01-ideation.md · drawings"),
         ("│   ├── s02-story-<telling A>/", "a telling: identity · pitch · stakes · drawings"),
         ("│   └── s03-story-<telling B>/ …", "an earlier telling, ended"),
         ("├── reports/", "Audience Report: answer, show the evidence"),
         ("│   ├── q01_<question>/", "q01_<question>.md: Answer · Evidence · Limits · Next"),
         ("│   └── q02_<question>/ …", ""),
         ("├── jNN_v<MMDD>_<desk>/", "a version: one send"),
         ("│   ├── jNN_v<MMDD>_<desk>.md", "face: tells · ## Narrative · compile order · ## Questions"),
         ("│   ├── studio/ · reports/ · runs/", "its own topics, Questions, Runs"),
         ("│   ├── t0N_<title>/ · t2N_<title>/", "Sections (Tasks)"),
         ("│   ├── t31_cover-letter/ · t32_response/", "Letters (Tasks)"),
         ("│   └── delivery/", "the paper built"),
         ("└── runs/", "the Board's Runs")]
READERS = [("Audience Report › Ideation", "Story00 Page", "studio/s01-ideation/ face"),
           ("Audience Report › Narrative", "the Story's §1 · §2 · §4 · §8", "the telling's face · the version's Narrative"),
           ("High-level logic + Low-level work", "the Story's §3 · §5–§7", "board.md ## Questions + reports/qNN_"),
           ("Description › Related", "the Story's related-papers table", "related/related.md"),
           ("version › Draft-Main rows", "the Story's §8 rows", "the version face's ## Narrative"),
           ("the build's compile order", "[pages] order = the Story Page", "[pages] order = the version face"),
           ("haipipe-paper-story · -ideation", "write a Story / Ideation Page", "called from Idea Studio and Audience "
                                                                          "Report: write a topic, register a Question")]
OPEN = ["? A Board with Stories still reads: both shapes until every paper Board has moved",
        "? An earlier telling's questions (one sent and judged): their own group, answered from that send",
        "? Review comments: their points become Questions in a reviewer group, answered by the next version",
        "? §8 per version: each version's face keeps its own Narrative and order, or the newest only"]


def box(x, y, title, lines, w=None, mono=True):
    """A lines-only box with a title above it; a line starting "?" draws red. Returns (right, bottom)."""
    w = w or max(len(l) for l in lines) * 15 * 0.6 + 40
    text(x, y, title, 18, GRAY)
    top = y + 32
    base("rectangle", x, top, w, 20 + len(lines) * LINE, INK, sw=1, rough=0)
    for i, l in enumerate(lines):
        text(x + 18, top + 12 + i * LINE, l, 15, RED if l.lstrip().startswith("?") else INK, MONO if mono else SANS)
    return x + w, top + 20 + len(lines) * LINE


def rows(x, y, heads, data, widths):
    """A lines-only table: a header line, then one line per row. Returns the bottom."""
    for h, c in zip(heads, [0] + list(_cum(widths))[:-1]):
        text(x + c, y, h, 16, GRAY)
    base("rectangle", x, y + 30, sum(widths), 1, GRAY, sw=1, rough=0)
    for i, r in enumerate(data):
        for cell, c in zip(r, [0] + list(_cum(widths))[:-1]):
            text(x + c, y + 44 + i * 34, cell, 15, RED if cell.startswith("?") else INK)
    return y + 44 + len(data) * 34


def _cum(ws):
    s = 0
    for w in ws:
        s += w
        yield s


def frame_homes(y0):
    fr = open_frame("1 · where each part of a Story goes")
    text(0, y0, "1 · where each part of a Story goes", 30)
    text(0, y0 + 44, "The Story stops being a Page: its thinking becomes studio topics, its questions become the Board's "
                     "Questions, and each version tells it in its own order.", 18, GRAY)
    r1, b1 = box(0, y0 + 100, "a Story Page today", STORY)
    box(0, b1 + 40, "an Ideation Page today", IDEATION)
    x = r1 + 220
    rows(x, y0 + 132, ("the part", "goes to", "shows in"), HOMES, (300, 720, 560))
    arrow(r1 + 30, y0 + 240, x - 30, y0 + 240)
    return close_frame(fr)


def frame_after(y0):
    fr = open_frame("2 · the Board after")
    text(0, y0, "2 · the Board after", 30)
    text(0, y0 + 44, "b03's shape at every level: a face with its Questions, studio/ topics, reports/ answers, runs/.",
         18, GRAY)
    lw = max(len(l) for l, _ in AFTER) * 15 * 0.6 + 40
    base("rectangle", 0, y0 + 100, lw + 620, 24 + len(AFTER) * LINE, INK, sw=1, rough=0)
    for i, (line, why) in enumerate(AFTER):
        text(18, y0 + 112 + i * LINE, line, 15, INK, MONO)
        text(lw + 20, y0 + 112 + i * LINE, why, 15, GRAY)
    return close_frame(fr)


def frame_readers(y0):
    fr = open_frame("3 · the readers that change")
    text(0, y0, "3 · the readers that change", 30)
    text(0, y0 + 44, "Each reads the new home first and the Story Page until every Board has moved.", 18, GRAY)
    rows(0, y0 + 110, ("view or tool", "reads today", "reads after"), READERS, (420, 520, 760))
    return close_frame(fr)


def frame_open(y0):
    fr = open_frame("open")
    text(0, y0, "open", 30, RED)
    for i, o in enumerate(OPEN):
        text(0, y0 + 56 + i * 32, o, 18, RED)
    return close_frame(fr)


def main():
    text(0, -110, "b16 s04 · the Story into studio topics and Questions (Q04)", 40)
    text(0, -52, "A plain prototype: placeholders only. Red = open.", 18, GRAY)
    y = frame_homes(60) + 220
    y = frame_after(y) + 220
    y = frame_readers(y) + 220
    frame_open(y)
    save(Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s04-story-to-topics.excalidraw",
         "build_s04_story_to_topics.py")


if __name__ == "__main__":
    main()
