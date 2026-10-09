"""s33 · The console UI issues: a review of the In-Lab Console as served on its synthetic fixtures (261009), the way
b01 j11's s33-ui-issue reviews the insight workbench. Every view was opened at both scopes on all three data types
(2 × 3 × 11 = 66 screens), every link and request collected. One lines-only table, worst first (where · what is
wrong · what it should be · evidence · owner), then what works and is kept, then the open points in red.
A rebuild keeps whatever a person drew.

    python build_s33_console_ui_issue.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_build"))
from console_draw import RED, Sheet, header, save  # noqa: E402

CHANGES = []                                          # (YYMMDD, what changed): a green note each

# (where, what is wrong, what it should be, evidence, owner)
ISSUES = [
    ("the image (Dockerfile)", "copies only main.py and console_api.py, but main.py imports four more routers "
     "(haichat, labeling, tasks, message), and personas/ is not copied: the built image cannot start",
     "copy every module and personas/ (or COPY . with the .dockerignore that already exists)",
     "Dockerfile; s51-console-runtime", "j02_console"),
    ("Case view, on a timeline", "every record row with a string becomes a 'case': on a glucose timeline each 5-minute "
     "reading is a case whose text is its timestamp (123 for one human); the banner says 3-CaseStore though the cases "
     "come from the record",
     "read the cooked CaseSet (TriggerFn picks the moments, CaseFns the facets), or name each data type's case stream",
     "s13 shots/case_SynthCGM_v0.png; labeling_api._row_text", "j02_console"),
    ("Health", "reports 'unconfigured' when only INLAB_DATASET_STORE is set: it still requires the single-store "
     "INLAB_PATIENT_STORE, though the dataset picker works from the dataset store",
     "count the dataset store as configured", "console_api.health; fixtures had to set both", "j02_console"),
    ("patient picker", "tags a patient by hard-coded study id prefixes (reach-1 ADHD, reach-2 PD2D, ohio-, CGMacros, "
     "else MIMIC), so a synthetic glucose patient shows MIMIC; study names are written into the plugin",
     "use the store's summary.cohort everywhere; no study names in the code",
     "web/src/types.ts cohortOf; s32 shots/approval_page.png (top bar)", "j02_console"),
    ("Tasks view", "reads examples/Project-*/tasks/<A01_*> (the letter series); projects are now "
     "examples-N-*/Project-*/tasks/bNN_*/jNN_*/tNN_*, so it finds nothing; empty until INLAB_PROJECTS_ROOT is set",
     "read the ladder's Blocks, Jobs and Tasks the way the project skill defines them (Q03)",
     "tasks_api.py; s12 shots/tasks.png", "j02_console · b01 j03"),
    ("Group scope", "seven of eleven views are a placeholder at Group (Raw, Source, Record, Internal, External, Model, "
     "Checklist); Internal and External are placeholders at Individual too",
     "build each, or drop it from the rail at that scope (Q05)", "s11 shots/*.png", "j02_console"),
    ("HaiChat transcript", "the agent called prepare_payload, which the gate's own comment says is deliberately in "
     "neither list; check whether can_use_tool refused it", "refuse a tool in neither list, and show it as refused",
     "s32 shots/approval_page.png; haichat_api ALLOWED_*", "j04_haichat"),
    ("Health view", "shows the absolute host paths of every store; embedded beside a shared thread, that shows the "
     "host's layout", "show the setting's name and whether it resolves, not the path", "s12 shots/health.png (paths masked to <SPACE>/ in the shot)",
     "j05_data_boundary"),
    ("links", "no view links out: the model card, the record and the task names name files and folders that cannot be "
     "opened from the console", "open each in a read-only pop-out, as the toolkit's workbench does",
     "the walk: 0 links in 66 screens", "j02_console"),
    ("docs (fixed by g01)", "the README's API table listed 11 of 26 routes and diagram 04 said four routers (there are "
     "five; message_api was in no diagram)", "generated lists: diagram/10-ui-elements.txt and 11-routes.txt",
     "diagram/build_ui_docs.py", "j02_console"),
    ("small", "no favicon (404 on every load); the front end ships one chunk over 500 kB (plotly)",
     "a favicon; split plotly into its own chunk", "fixtures/.logs/console.log; npm run build", "j02_console"),
]

KEEP = [
    "one engine for the buttons and the agent: the agent's tools dispatch the same ConsoleActions a click does",
    "acts wait for Allow/Deny (the card works: select_model asked first); reads and navigation stay visible, badged 🤖",
    "the score is the endpoint's, verbatim; a forecast is drawn with its context, what was observed, and its MAE",
    "the wall: what was observed never reaches compose or judge",
    "the as-of discipline: rows after the prediction date are flagged in Source, withheld in the chart",
    "each DATA view names its store in a banner; every component explains itself in its opening comment",
    "the walk was clean: no failed request and no browser error across 66 screens (only the favicon)",
]

OPEN = [
    "? copy each human to json, or read the record store in place (j02 Q02)",
    "? one look for the console and the toolkit's workbench (j02 Q04)",
    "? build or drop the Group placeholders (j02 Q05)",
]


def main():
    s = Sheet()
    cols = [("#", 50, 4), ("where", 260, 22), ("what is wrong", 640, 54), ("what it should be", 470, 40),
            ("evidence", 400, 34), ("owner", 200, 16)]
    width = sum(w for _, w, _ in cols)
    f = s.frame("1 · The console UI issues, worst first", 0, 0, width + 80, 100)
    y = header(s, f, "s33 · The console UI issues: a review on the synthetic fixtures, 261009",
               "Every view at both scopes on all three data types (66 screens), every link and request collected; "
               "screenshots in s11 · s12 · s13 · s21 · s32.", CHANGES)
    y = s.table(40, y, cols, [[str(i)] + list(r) for i, r in enumerate(ISSUES, 1)], f)
    f["height"] = y + 40
    f2 = s.frame("2 · What works, kept · open", width + 200, 0, 1100, 100)
    s.text(width + 240, 30, "What works, kept", 30, f2)
    yy = 90
    for k in KEEP:
        s.text(width + 240, yy, "· " + k, 16, f2)
        yy += 30
    yy += 30
    s.text(width + 240, yy, "Open", 30, f2)
    yy += 50
    for o in OPEN:
        s.text(width + 240, yy, o, 16, f2, RED)
        yy += 30
    f2["height"] = yy + 30
    save(s, f, y, HERE / "s33-console-ui-issue.excalidraw", "build_s33_console_ui_issue.py")


if __name__ == "__main__":
    main()
