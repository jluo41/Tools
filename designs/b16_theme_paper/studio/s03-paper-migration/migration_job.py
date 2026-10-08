"""s03 · paper migration, the Job part: how a paper's Ba- / Bb- / Bc-<desk> groups and its root delivery/ become
one version Job, and where their old screens go (owned by the -job session; build_s03_paper_migration.py draws it).

Counts are read from disk on every build, counts only: no Board, Section or venue name leaves this file.
Exports LEVEL, OLD, NEW [(tree line, what happens, why)], SCREEN [(old view, new place)], COUNTS [(what, count)]
and OPEN ["? …"]; what happens is one word: kept · new · moved · rebuilt · open. CHANGES ["…"] says, in green,
what changed since the last build.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1].parent / "b04_skill_folder" / "studio" / "_build"))
from sketch import SPACE  # noqa: E402

LEVEL = "Job"

OLD = ["Paper-<Name>/",
       "├── Ba-<desk>-Main/            Main Sections",
       "├── Bb-<desk>-Appendix/        Appendix Sections",
       "├── Bc-<desk>-Round/RD<NN>/    review rounds",
       "└── delivery/                  paper-build.toml · latex/ · word/",
       "    └── …/sent/ · released/    frozen builds"]

NEW = [("j01_v<MMDD>_<desk>/", "new", "✎ one send to one venue, dated by its send (was j01_v1_)"),
       ("├── j01_v<MMDD>_<desk>.md", "new", "the face: venue · deadline · tells · from · answers"),
       ("├── t0N_<title>/", "moved", "✎ from Ba-, renamed by print order (was S-<desk>-Main-N-…)"),
       ("├── t2N_<title>/", "moved", "✎ from Bb-, A = t21 (was S-<desk>-Appendix-A-…)"),
       ("├── t31_cover-letter/ · t32_response/", "new", "✎ Letters: Page Tasks in the t3N_ band"),
       ("├── reports/qNN_<kind>-<MMDD>/", "moved", "✎ from Bc-…/RD<NN>/: a report of type comments, not a Task"),
       ("├── studio/ · reports/ · runs/", "new", "✎ the version's own Space folders"),
       ("└── delivery/", "", ""),
       ("    ├── paper-build.toml", "moved", "its paths edited to the new folders"),
       ("    ├── latex/ · word/", "rebuilt", "by the build, never copied"),
       ("    └── …/sent/ · released/", "kept", "frozen records, moved unchanged")]

SCREEN = [("old page › Sections › Main · Appendix", "Job tab › Work Details › Main · Appendix"),
          ("old page › Sections › Narrative", "Job tab › Audience Report › Draft-Main"),
          ("old page › Delivery › Rounds", "Job tab › Audience Report › Comments (Review Items)"),
          ("old page › Delivery › LaTeX · Word · Cover letter", "Job tab › Delivery"),
          ("(none)", "Job tab › Audience Report › Questions (one-minute story, why this venue …)")]


def _boards():
    return [b for b in SPACE.glob("examples-*/*/paper*/Paper-*")
            if b.is_dir() and not {"_old", "_legacy", "_archive"} & set(b.parts)]


def counts():
    """Both layouts: old groups (Ba- · Bb- · Bc-<desk>) and new versions (jNN_v<N>_<desk>/), counts only."""
    bs = _boards()
    new = [v for b in bs for v in b.glob("j[0-9][0-9]_v*") if v.is_dir()]
    pages = lambda dirs: sum(1 for g in dirs for p in g.iterdir() if p.is_dir())
    main = [g for b in bs for g in b.glob("Ba-*") if g.is_dir()]
    appx = [g for b in bs for g in b.glob("Bb-*") if g.is_dir()]
    rnd = [g for b in bs for g in b.glob("Bc-*") if g.is_dir()]
    in_new = lambda pat: sum(1 for v in new for p in v.glob(pat) if p.is_dir())
    return [("versions moved (jNN_v…)", len(new)), ("versions still old (Ba- groups)", len(main)),
            ("Main Sections", pages(main) + in_new("S-*-Main-*")),
            ("Appendix Sections", pages(appx) + in_new("S-*-Appendix-*")),
            ("comment batches (RD · CM)", pages(rnd) + in_new("RD[0-9]*") + in_new("CM[0-9]*")),
            ("frozen builds (sent/ · released/)",
             sum(1 for b in bs for d in b.rglob("*") if d.is_dir() and d.name in ("sent", "released"))),
            ("paper-build.toml files", sum(1 for b in bs for _ in b.glob("**/delivery/paper-build.toml")))]


COUNTS = counts()

OPEN = ["? delivery in the version Job; the Board shows it from below (Q02)",
]

CHANGES = ["names: j01_v<MMDD>_<desk>/ · t0N_ Main · t2N_ Appendix · t3N_ Letters; rename_tasks.py, rolled back from .paper-tasks.yaml",
           "comments: a batch is not a Task; the next version answers it (was open, Q03)",
           "comments: a report of type comments in the answering version, reports/qNN_<kind>-<MMDD>/; rename_tasks.py moves RD<NN>-… there",
           "a second version copies the first one's authored files only: faces, drafts, drawings",
           "applied on one Board; the other Boards wait"]
