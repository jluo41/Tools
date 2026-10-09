"""s03 · paper migration, the Task part: what a Section folder keeps, gains and regenerates on the move,
and where its old screen goes (owned by the -task session; build_s03_paper_migration.py draws it).

A Section (S-<desk>-<Group>-<N>-<Title>/) moves whole into its version Job and takes the version's Task name,
t0N_<title>/ (t2N_ an appendix; the version's rename, s12); inside it nothing is moved by hand. It gains studio/ and reports/ as every Task (b16 s13, JL 261007), its
requirement record is written by its Context Run where missing, and its generated files are rebuilt.
Counts are read from disk on every build, counts only: no Board, Section or venue name leaves this file.

Exports LEVEL, OLD (the old tree), NEW [(tree line, what happens, why)], SCREEN [(old view, new place)],
COUNTS [(what, count)] and OPEN ["? …"]. What happens is one word: kept · new · regenerated · rebuilt · open.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2].parent / "b01_haipipe-toolkit" / "j04_skill_folder" / "studio" / "_build"))
from sketch import SPACE  # noqa: E402  (the SPACE root, as the s03 builder finds it)

LEVEL = "Task"

OLD = ["S-<desk>-Main-<N>-<Title>/",
       "├── S-<…>.md                      the face",
       "├── draft/                        the plan · records/",
       "├── results/run-<type>-<…>/       local Results",
       "├── runs/run-<type>-<…>.md        soft Runs",
       "└── delivery/latex/               <page>.tex · draft-bibliography/"]

NEW = [("j0N_v<MMDD>_<venue>/t0N_<title>/", "new", "the version's Task name; Runs and the Story cite the new stem"),
       ("├── t0N_<title>.md", "kept", "the face, renamed with its folder; + ## Questions, empty until the first question"),
       ("├── draft/", "kept", "the plan and its versions"),
       ("│   └── records/<stem>-requirement.md", "regenerated", "written by the Context Run where missing"),
       ("├── results/ · runs/", "kept", "a Run is one file + its Result; renamed run-<kind>-<slug> by page.py run-names"),
       ("├── studio/sNN-<topic>/", "new", "empty until Draw the logic"),
       ("├── reports/qNN_<topic>/", "new", "empty until Ask a question"),
       ("└── delivery/latex/", "rebuilt", "by Build, never copied"),
       ("    draft-bibliography/<page>.bib", "open", "stays until its home is decided")]

SCREEN = [("Page workbench › Draft › Table · Reading", "Task tab › Audience Report › Table · Reading"),
          ("Page workbench › Draft › Scratch · Revise", "Task tab › Work Details › Draft-Scratch · Draft-Revise"),
          ("Page workbench › Evidence › Citations · Displays · Values", "Task tab › Work Details › Evidence-…"),
          ("Page workbench › Delivery › LaTeX · Word", "Task tab › Delivery › LaTeX · Word"),
          ("Outline's Requirement lens", "Task tab › Description › Requirement"),
          ("(none)", "Task tab › Audience Report › Questions · Comments · Idea Studio")]


def _sections():
    found = [s for pattern in ("B[a-z]-*/S-*", "j[0-9][0-9]_*/S-*", "j[0-9][0-9]_*/t[0-2][0-9]_*")   # old groups,
             for s in SPACE.glob(f"examples-*/*/paper*/Paper-*/{pattern}")]                    # then a version Job
    return [s for s in found if s.is_dir() and not {"_old", "_legacy", "_archive"} & set(s.parts)]


def counts():
    """[(what, count)]: what the move finds in today's Section folders, counts only."""
    secs = _sections()
    units = [u for s in secs for u in s.glob("results/run-display-*/payload/Display*") if u.is_dir()]
    req = sum(any(s.glob("draft/records/*-requirement.md")) for s in secs)
    moved = sum(s.parent.name[:1] == "j" and s.parent.name[1:3].isdigit() for s in secs)
    return [("Sections", len(secs)),
            ("moved into a version Job", moved),
            ("still in an old B<x>- group", len(secs) - moved),
            ("renamed t0N_<title>", sum(s.name[:1] == "t" for s in secs)),
            ("with a requirement record", req),
            ("without one: their Context Run writes it", len(secs) - req),
            ("display units", len(units)),
            ("display units without preview.pdf", sum(not (u / "preview.pdf").is_file() for u in units)),
            ("with studio/ or reports/ today", sum((s / "studio").is_dir() or (s / "reports").is_dir() for s in secs)),
            ("with a Bib under delivery/latex/draft-bibliography/", sum(any(s.glob("delivery/latex/draft-bibliography/*.bib")) for s in secs))]


COUNTS = counts()

OPEN = ["? The citation file's home: <stem>.bib, selected-bibliography/, or delivery/latex/draft-bibliography/ (today)"]

CHANGES = ["a Section takes the version's Task name t0N_<title>/ (t2N_ appendix) (was: keeps S-<desk>-<Group>-<N>-<Title>/)",
           "new Runs carry no date: run-<type>-<slug>, its passes inside (was run-<type>-<MMDD>-<slug>)",
           "the counts also read j0N_*/t0N_* folders: 'renamed t0N_<title>'",
           "a comments batch is a report of type comments: <version>/reports/qNN_<kind>-<MMDD>/, never a Task",
           "dated Runs renamed by page.py run-names: 9 Sections now, 7 with their delivery rebuild"]
