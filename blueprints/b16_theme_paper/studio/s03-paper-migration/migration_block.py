"""s03 · paper migration, the Block part: what the paper Board's folder keeps, gains and moves, and where its old
screen goes (owned by the -job session; build_s03_paper_migration.py draws it).

Counts are read from disk on every build, counts only: no Board, Section or venue name leaves this file.
Exports LEVEL, OLD (the old tree), NEW [(tree line, what happens, why)], SCREEN [(old view, new place)],
COUNTS [(what, count)] and OPEN ["? …"]; what happens is one word: kept · new · moved · rebuilt · open. CHANGES ["…"] says, in green,
what changed since the last build.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1].parent / "b04_skill_folder" / "studio" / "_build"))
from sketch import SPACE  # noqa: E402

LEVEL = "Block"

OLD = ["Paper-<Name>/",
       "├── board.md                  the face; ## Pages names each group",
       "├── A1-Story/                 Ideation + Story Pages",
       "│   ├── Story00-<direction>/",
       "│   └── Story<L>-<desk>-<idea>/",
       "├── _venue/                   (some Boards)",
       "├── <code>.py                 (some Boards, at the root)",
       "├── studio/ · reports/",
       "└── Ba- · Bb- · Bc-<desk>-…/   → the Job part"]

NEW = [("Paper-<Name>/", "kept", "the Board is the paper"),
       ("├── board.md", "kept", "its ## Pages headings point to the new folders"),
       ("├── studio/s01-ideation/", "moved", "✎ the Ideation Page becomes a studio topic (Q04)"),
       ("├── studio/sNN-story-<telling>/", "moved", "✎ each Story Page: §1 · §2 · §4 in the face, drawings beside"),
       ("├── board.md ## Questions", "new", "✎ each research question, grouped by topic"),
       ("├── reports/qNN_<question>/", "new", "✎ its report; the Story's §5-§7 go into its Work"),
       ("├── venues/<venue>/", "moved", "from _venue/: call.md · kit/"),
       ("├── related/related.md", "new", "the Story's related table, copied once"),
       ("├── reports/", "kept", "Board level, as before"),
       ("├── <code>.py", "open", "a paper computes no facts: it belongs in a work Task"),
       ("└── j01_v<MMDD>_<desk>/", "new", "✎ → the Job part, dated by its send (was j01_v1_)")]

SCREEN = [("old page › Ideation", "Block tab › Audience Report › Ideation (questions)"),
          ("old page › Story › Spine · RoadMap Draw", "Block tab › Audience Report › Narrative"),
          ("old page › Story › High-level logic + Low-level work", "Block tab › Audience Report › High-level logic …"),
          ("old page › Story › Related Papers", "Block tab › Description › Related (cards)"),
          ("(none)", "Block tab › Description › Venue · Resources"),
          ("old page › Sections · Delivery", "the Job tab (the Job part)")]


def _boards():
    return [b for b in SPACE.glob("examples-*/*/paper*/Paper-*")
            if b.is_dir() and not {"_old", "_legacy", "_archive"} & set(b.parts)]


def counts():
    bs = _boards()
    linked = 0
    for b in bs:
        for p in b.rglob("*.md"):
            if {"_archive", "delivery", "results"} & set(p.relative_to(b).parts):
                continue
            if re.search(r"\]\(\.\./(?:\.\./)*(?:A1-Story|B[abc]-)", p.read_text(errors="ignore")):
                linked += 1
                break
    return [("paper Boards", len(bs)),
            ("with Sections", sum(any(b.glob("Ba-*")) or any(b.glob("j[0-9][0-9]_v*")) for b in bs)),
            ("Story only", sum((b / "A1-Story").is_dir() and not any(b.glob("Ba-*")) for b in bs)),
            ("moved to the ladder (j0N_v…)", sum(any(b.glob("j[0-9][0-9]_v*")) for b in bs)),
            ("from before the layout", sum((b / "0-sections").is_dir() for b in bs)),
            ("with a _venue/", sum((b / "_venue").is_dir() for b in bs)),
            ("with code at the root", sum(any(b.glob("*.py")) for b in bs)),
            ("with Pages linking ../ old folders", linked)]


COUNTS = counts()

CHANGES = ["the Story is not a Job: no j00_story/; the Pages keep their names",
           "the Story and Ideation stop being Pages: studio topics, Board Questions and reports; §8 goes to the version face (Q04)"]

OPEN = [        "? the Board from before the layout: archive it as it is",
        "? code at a Board's root: moved to a work Task by hand"]
