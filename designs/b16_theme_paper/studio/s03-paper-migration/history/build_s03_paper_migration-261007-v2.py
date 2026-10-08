"""b16 s03 · paper migration: s03-paper-migration.excalidraw, how the old paper folders and the old paper
workbench move to the new ladder (Block · Job · Task) and the shared frame (JL 261007: "a new s03 about how to
do the immigration from the old paper folder and workbench to the new one").

Read from disk every build: the Project paper Boards (examples-*/*/paper*/Paper-*), counted only and named
Board 1..N (no Board, Section or venue name is drawn); the old workbench's Spaces and Views from
workbench-paper/ref/workbench-table.md; the old page's size and the new tab's size. Typed here, as the
proposal: where each old part goes, the phases, the checks and the open points (red). Drawn with b04's studio
helpers (as s21 is) through b03's canvas.write, so a person's marks survive a rebuild.

    python build_s03_paper_migration.py [out.excalidraw]
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLOCK = HERE.parents[1]
sys.path.insert(0, str(BLOCK.parent / "b04_skill_folder" / "studio" / "_build"))
from sketch import (GRAY, RED, SKILLS, SPACE, TK, arrow, close_frame, concern, legend, mono,  # noqa: E402
                    open_frame, questions_frame, save, sticky, text)

SERVER = TK / "servers" / "workbench-paper"
TABLE = SKILLS / "2_theme" / "paper" / "workbench-paper" / "ref" / "workbench-table.md"


# ── facts, read from disk ──────────────────────────────────────────────────────────────────────
def boards():
    """The Project paper Boards, one dict each, counts only (no names leave this function)."""
    out = []
    for b in sorted(SPACE.glob("examples-*/*/paper*/Paper-*")):
        if not b.is_dir() or {"_old", "_legacy", "_archive"} & set(b.parts):
            continue
        group = lambda pat: [g for g in b.glob(pat) if g.is_dir()]
        pages = lambda gs: sum(1 for g in gs for p in g.iterdir() if p.is_dir())
        md = [p for p in b.rglob("*.md") if not {"_archive", "delivery", "results"} & set(p.relative_to(b).parts)]
        links = sum(1 for p in md if re.search(r"\]\(\.\./(?:\.\./)*(?:A1-Story|B[abc]-)", p.read_text(errors="ignore")))
        receipts = sum(1 for p in b.rglob("runtime.yaml") if re.search(r"A1-Story/|B[abc]-", p.read_text(errors="ignore")))
        out.append({
            "kind": ("before the layout" if (b / "0-sections").is_dir() else
                     "with Sections" if group("Ba-*") else "Story only" if (b / "A1-Story").is_dir() else "empty"),
            "home": b.parent.name + "/",
            "stories": len([p for p in (b / "A1-Story").iterdir() if p.is_dir()]) if (b / "A1-Story").is_dir() else 0,
            "main": pages(group("Ba-*")), "appendix": pages(group("Bb-*")), "round": pages(group("Bc-*")),
            "desks": len(group("Ba-*")),
            "frozen": sum(1 for d in b.rglob("*") if d.is_dir() and d.name in ("sent", "released")),
            "delivery": (b / "delivery").is_dir(), "build_toml": (b / "delivery" / "paper-build.toml").is_file(),
            "venue": (b / "_venue").is_dir(), "code": len([p for p in b.glob("*.py")]),
            "links": links, "receipts": receipts, **git_state(b),
            "heads": len(re.findall(r"(?m)^### [^\n]* · ", (b / "board.md").read_text(errors="ignore").split("## Pages", 1)[-1].split("\n## ", 1)[0])) if (b / "board.md").is_file() else 0,
            "toml_paths": len(re.findall(r'(?m)^(?:order|main|appendix|rounds?)\s*=\s*"\.\./', (b / "delivery" / "paper-build.toml").read_text(errors="ignore"))) if (b / "delivery" / "paper-build.toml").is_file() else 0,
            "link_files": sum(1 for p in md if re.search(r"\]\(\.\./(?:\.\./)*(?:A1-Story|B[abc]-)", p.read_text(errors="ignore"))),
            "generated": sum(1 for f in (b / "delivery").rglob("*") if f.is_file()) if (b / "delivery").is_dir() else 0,
            "result_dirs": sum(1 for d in b.rglob("results") if d.is_dir())})
    return out


def git_state(b):
    """Whether the Board is its own git repository, and how many paths are uncommitted there (counts only)."""
    import subprocess
    run = lambda *a: subprocess.run(["git", "-C", str(b), *a], capture_output=True, text=True)
    top = run("rev-parse", "--show-toplevel").stdout.strip()
    own = bool(top) and Path(top).resolve() == b.resolve()
    dirty = len([l for l in run("status", "--porcelain", "--", ".").stdout.splitlines() if l.strip()]) if top else 0
    return {"repo": "own" if own else "SPACE" if top else "none", "dirty": dirty}


def old_views():
    """The old workbench's (Space, View) pairs, in table order."""
    seen = []
    for line in TABLE.read_text(encoding="utf-8").splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) >= 3 and c[0] == "board" and (c[1], c[2]) not in seen:
            seen.append((c[1], c[2]))
    return seen


lines_of = lambda p: len(p.read_text(encoding="utf-8").splitlines()) if p.is_file() else 0

# ── the proposal, typed ────────────────────────────────────────────────────────────────────────
FOLDERS = [("Paper-<Name>/board.md", "Paper-<Name>/board.md", "the face; its ## Pages headings rewritten"),
           ("A1-Story/Story00-<direction>/", "j00_story/Story00-<direction>/", "? stem kept: runs and receipts cite it"),
           ("A1-Story/Story<L>-<desk>-<idea>/", "j00_story/Story<L>-<desk>-<idea>/", "? one Story Page per idea"),
           ("Ba-<desk>-Main/S-<desk>-Main-…/", "j01_v1_<desk>/S-<desk>-Main-…/", "? Section stems unchanged"),
           ("Bb-<desk>-Appendix/S-…-Appendix-…/", "j01_v1_<desk>/S-<desk>-Appendix-…/", "group read from the stem"),
           ("Bc-<desk>-Round/RD<NN>/", "j01_v1_<desk>/RD<NN>/", "? past rounds stay with the send"),
           ("delivery/ (generated)", "j01_v1_<desk>/delivery/", "? rebuilt there by assemble, not copied"),
           ("delivery/…/sent/ · released/", "j01_v1_<desk>/delivery/…/sent/", "frozen records: git mv, unchanged"),
           ("_venue/", "venues/<venue>/", "call.md · kit/"),
           ("the Story's related-papers table", "related/related.md", "? copied once; the Story then links it"),
           ("studio/ · reports/", "studio/ · reports/", "unchanged, Board level"),
           ("<code>.py at the Board root", "a work Task (work/ or tasks/)", "? a paper computes no facts: flag only")]
NEW_HOME = {"Guide": "Guide tab (four Views, Block · Job · Task sections; s31)",
            "Ideation": "Block › Audience Report › Ideation",
            "Story": "Block › Audience Report › Spine · Design · Narrative · High-level logic + Low-level work; Idea Studio; Description › Related",
            "Sections": "Job tab, live today (each B<x>- group a Job); Work Details · Audience Report › Draft-Main (s12)",
            "Delivery": "Job › Delivery; Board › Delivery from below (Q02)"}
READERS = [("board.md ## Pages headings (### A1 · A1-Story): the folder", "! rewritten to j00_story · j01_v1_<desk>"),
           ("page_file(): <folder>/<stem>/<stem>.md", "survives: stems kept, one level under a Job"),
           ("Page kind by stem: Story00 · Story[A-Z] · S- · RD", "survives: stems kept"),
           ("the desk read from the Ba-<desk>-Main name", "survives in j01_v1_<desk>; or the face's venue:"),
           ("paper-build.toml paths: the Story Page, Main, Appendix", "! edited by the move; delivery/ then rebuilt"),
           ("frame.level_of() + paper level_patterns (Job ^B[a-z]-, Task ^S-)", "live today: groups are Jobs, S- Sections are Tasks"),
           ("guide.yaml folders: (A1-Story/…, B[ab]-*)", "! add j00_story/ · jNN_*/ patterns beside them")]
PHASES = [("0 · settle", "j00_story · rounds as Comments · delivery in the Job · Job types", "you", "a yes per point"),
          ("1 · readers", "partly done 261007: the frame reads today's layout at every level; skills, guide.yaml, assemble next", "agent", "tests on two demo Boards"),
          ("2 · script", "migrate_paper.py --dry-run: every git mv, ## Pages heading, toml and link edit", "agent", "a printed plan"),
          ("3 · one Board", "a Story-only Board, then one with Sections", "you check", "it opens, builds, links resolve"),
          ("4 · the rest", "one at a time, when no session works in it", "agent + you", "same checks"),
          ("5 · retire", "the old page link, paper.py's own page, old docs", "agent", "nothing reads the old layout")]
OPEN = ["? A1-Story/ → j00_story/: renames folders in real Projects",
        "? Past rounds stay with their send (RD<NN> in j01_v1_<desk>); only future sends become new Jobs",
        "? Delivery in the version Job; the Board shows it from below (Q02)",
        "? The Board from before the layout: archive as it is, not migrate",
        "? Root code in a Board: move to a work Task by hand, or leave and flag",
        "? Old Run receipts keep old paths: a moves map the tools read, or leave as history"]


# ── 0 · why migrate, now that the frame reads today's layout ───────────────────────────────────────
WHY = [("the workbench", "works on today's folders at every level (261007): Board, each B<x>- group a Job, each S- a Task", "done"),
       ("the ladder's names", "j00_story/ · jNN_v<N>_<desk>/ say what each folder is; A1-/Ba- only say an order", "idea"),
       ("one version = one send", "! today Ba-, Bb- and Bc- are three Jobs; the ladder makes them one version (JL)", "open"),
       ("homes for new parts", "venues/<venue>/ · related/related.md · reports/ · Related Questions: Board-level", "idea"),
       ("retire the old page", "paper.py's own page and its 14 docs that teach the old layout", "idea")]

# ── 5 · readers × layouts: which tool reads which layout, and the change each needs ────────────────
MATRIX = [("paper.collect() · page_file()", "board.md ## Pages headings", "✓", "✓ after the heading rewrite", "rewrite 1 file per Board"),
          ("paper_theme.py (Block tab)", "collect()", "✓", "✓", "none"),
          ("frame level_patterns (Job · Task)", "folder names", "✓ B<x>- is a Job", "! ✓ jNN_ is a Job; Bb-/Bc- merge into it", "none; ? one Job per send (JL)"),
          ("Page workbench links (/_board/draft)", "board.md, at request time", "✓", "✓", "none: links are built, never stored"),
          ("excalidraw-section (paper map)", "board.md ## Pages", "✓", "✓ after the heading rewrite", "none; redraw the map"),
          ("haipipe-paper-assemble (build)", "paper-build.toml [pages]", "✓", "✗ until edited", "3 paths per Board, then rebuild delivery/"),
          ("guide.yaml folders:", "glob patterns", "✓", "✗", "add the new patterns beside the old"),
          ("paper skills' docs (14 files)", "the layout, as taught", "✓", "✗", "! one contract: paper-structure.md first"),
          ("../ links inside Page .md", "relative paths", "✓", "✗", "the script rewrites them"),
          ("Run receipts (runtime.yaml)", "absolute in the Board", "history", "stale", "? a moves map, never edited")]

# ── 6 · the script, step by step ────────────────────────────────────────────────────────────────────
SCRIPT = [("1 · preflight", "the Board's repo is clean (no uncommitted path); no session works in it; the readers pass"),
          ("2 · plan (--dry-run)", "prints every git mv, the ## Pages heading diff, the toml path diff, each ../ link edit"),
          ("", "file:line, and the receipts it leaves as history; writes nothing"),
          ("3 · apply", "git mv per folder (history kept); the edits; one commit in the Board's own repo"),
          ("4 · moves map", "<board>/.paper-moves.yaml: old → new, with the date; tools resolve old receipt paths by it"),
          ("5 · verify", "every Page opens at its level on the frame (200); assemble --dry-run finds every fragment;"),
          ("", "0 broken links; the Board's own tests"),
          ("6 · roll back", "reverse every git mv from the moves map, or revert the one commit")]


def frame_why(x0, y0):
    fr = open_frame("0 · why migrate, now that the frame reads both")
    text(x0, y0, "0 · why migrate, now that the workbench already works", 28)
    y = y0 + 60
    for head, body, kind in WHY:
        sticky(x0, y, 1100, f"{head}: {body}", kind)
        y += 90
    close_frame(fr)
    return y


def frame_ready(x0, y0, bs):
    fr = open_frame("1b · each Board: its repo, its state, its phase")
    W = (9, 7, 13, 26, 24)
    cell = lambda vals: "".join(f"{str(v):<{w}}" for v, w in zip(vals, W))
    rows = [cell(["Board", "repo", "uncommitted", "phase", "first step"])]
    for i, b in enumerate(bs, 1):
        phase = ("archive" if b["kind"] == "before the layout" else
                 "3 · one Board" if b["kind"] == "Story only" and not b["dirty"] else
                 "4 · the rest" if b["dirty"] == 0 else "after its owner commits")
        step = ("leave as is" if phase == "archive" else "A1-Story → j00_story" if b["kind"] == "Story only"
                else "the full move")
        rows.append(("!" if b["dirty"] else "") + cell([f"Board {i}", b["repo"], b["dirty"] or "0", phase, step]))
    _, bottom = mono(x0, y0, rows, "each Board: its own repo or the SPACE's, uncommitted paths, the phase it fits", size=15)
    close_frame(fr)
    return bottom


def frame_matrix(x0, y0):
    fr = open_frame("5 · readers × layouts")
    W = (38, 28, 18, 42, 40)
    cell = lambda vals: "".join(f"{str(v):<{w}}" for v, w in zip(vals, W))
    rows = [cell(["reader", "reads", "today's layout", "the ladder's layout", "the change it needs"])]
    rows += [("!" if "!" in new or "?" in change or "✗" in new else "") + cell([r, how, old, new.lstrip("! "), change.lstrip("! ")])
             for r, how, old, new, change in MATRIX]
    _, bottom = mono(x0, y0, rows, "5 · readers × layouts: every tool that finds a paper's folders", size=15)
    close_frame(fr)
    return bottom


def frame_script(x0, y0):
    fr = open_frame("6 · migrate_paper.py, step by step")
    rows = [f"{a:<22}{b}" for a, b in SCRIPT]
    _, bottom = mono(x0, y0, rows, "6 · the script: one Board per run; nothing moves without its plan", size=16)
    close_frame(fr)
    return bottom


def frame_example(x0, y0, bs):
    """One Board worked through, counts only: the one with Sections, an Appendix and a Round."""
    pick = max(((i, b) for i, b in enumerate(bs, 1) if b["kind"] == "with Sections"),
               key=lambda ib: (ib[1]["round"], ib[1]["main"] + ib[1]["appendix"]), default=None)
    fr = open_frame("7 · one Board worked through")
    if not pick:
        text(x0, y0, "7 · no Board with Sections yet", 24)
        close_frame(fr)
        return y0 + 40
    i, b = pick
    before = [f"Paper-<Name>/            (Board {i})",
              f"├── board.md              {b['heads']} group headings under ## Pages",
              f"├── A1-Story/             {b['stories']} Story Pages",
              f"├── Ba-<desk>-Main/       {b['main']} Sections",
              f"├── Bb-<desk>-Appendix/   {b['appendix']} Sections",
              f"├── Bc-<desk>-Round/      {b['round']} Round(s), {b['frozen']} frozen build folder(s)",
              f"└── delivery/             {b['generated']} files, generated (paper-build.toml: {b['toml_paths']} paths)"]
    after = [f"Paper-<Name>/",
             f"├── board.md              the same {b['heads']} headings, rewritten",
             f"├── j00_story/            {b['stories']} Story Pages, stems unchanged",
             f"└── j01_v1_<desk>/        one send",
             f"    ├── S-<desk>-Main-…    {b['main']} + {b['appendix']} Sections, stems unchanged",
             f"    ├── RD<NN>-…/          {b['round']} Round(s), frozen builds moved as records",
             f"    └── delivery/          rebuilt by assemble ({b['toml_paths']} toml paths edited)"]
    r1, b1 = mono(x0, y0, before, f"7 · Board {i} today (counts only)", size=16)
    r2, b2 = mono(r1 + 220, y0, after, f"Board {i} after the move", size=16)
    arrow(r1 + 20, y0 + 120, r1 + 200, y0 + 120, "migrate_paper.py")
    edits = [f"{b['heads']} headings rewritten in board.md",
             f"{b['toml_paths']} paths edited in delivery/paper-build.toml, then delivery/ rebuilt ({b['generated']} files)",
             f"{b['links']} ../ links in {b['link_files']} Page files rewritten by the script",
             f"{b['receipts']} Run receipts name old folders: left as history, read through the moves map",
             f"{b['result_dirs']} results/ folders: generated, never edited; stale paths until their Runs rerun",
             f"its repo: {b['repo']} · {b['dirty']} uncommitted paths: its owner commits first"
             + ("" if not b["dirty"] else " ?")]
    r3, b3 = mono(x0, max(b1, b2) + 40, edits, "what the script edits, and what it leaves", size=16)
    close_frame(fr)
    return b3


# ── the drawing ────────────────────────────────────────────────────────────────────────────────
def draw():
    bs = boards()
    text(0, -170, "b16 s03 · moving the old paper folders and workbench to the new ladder", 44)
    legend(1700, -170)
    text(0, -105, f"Read from disk: {len(bs)} Project paper Boards (counted, never named), the old workbench's Views, "
                  "the old page and the new tab. Where each part goes, the phases and the checks are the proposal; "
                  "red = open.", 20, GRAY)

    # 1 · what exists
    fr = open_frame("1 · what there is to move")
    W = (9, 9, 19, 8, 6, 6, 6, 8, 6, 13, 8, 9, 9, 9)    # one width per column, head and rows alike
    cell = lambda vals: "".join(f"{str(v):<{w}}" for v, w in zip(vals, W))
    rows = [cell(["Board", "home", "kind", "Stories", "Main", "Appx", "Round", "frozen", "desk", "delivery",
                  "_venue", "root .py", "../links", "receipts"])]
    for i, b in enumerate(bs, 1):
        flag = "!" if b["kind"] == "before the layout" or b["code"] or b["links"] else ""
        rows.append(flag + cell([f"Board {i}", b["home"], b["kind"], b["stories"], b["main"], b["appendix"], b["round"],
                                 b["frozen"], b["desks"], ("yes · toml" if b["build_toml"] else "yes") if b["delivery"] else "—",
                                 "yes" if b["venue"] else "—", b["code"] or "—", b["links"] or "—", b["receipts"] or "—"]))
    r1, b1 = mono(0, 0, rows, "the Project paper Boards today (counts only)", size=15)
    kinds = {k: sum(1 for b in bs if b["kind"] == k) for k in ("with Sections", "Story only", "before the layout")}
    y = b1 + 40
    sticky(0, y, 560, f"{kinds['with Sections']} Boards hold Sections, each one desk:\none venue, one send so far →"
                      " one version Job", "idea")
    sticky(600, y, 520, f"{kinds['Story only']} are Story-only: only A1-Story\nmoves, to j00_story/", "idea")
    sticky(1160, y, 560, f"{kinds['before the layout']} predates the layout (0-sections/,\nI-Ideation): archive, "
                         "don't migrate ?", "open")
    close_frame(fr)
    frame_why(r1 + 1300, -40)
    yb = frame_ready(0, y + 220, bs)

    # 2 · the folder map
    y0 = yb + 300
    fr = open_frame("2 · the folder map")
    left = [f"{a}" for a, _, _ in FOLDERS]
    right = [("!" if "?" in note else "") + f"{b:<38}{note.lstrip('? ')}" for _, b, note in FOLDERS]
    r2, b2 = mono(0, y0, left, "old: Paper-<Name>/ today", size=16)
    r3, b3 = mono(r2 + 220, y0, right, "new: the ladder (s01) · Job = one send (s12)", size=16)
    for k in range(len(FOLDERS)):
        arrow(r2 + 20, y0 + 36 + 14 + 16 * 1.3 * k + 10, r2 + 200, y0 + 36 + 14 + 16 * 1.3 * k + 10)
    cy = max(b2, b3) + 40
    for c in ["Names inside Pages stay: Section ids (S-<desk>-Main-…) and the Story's compile order do not change, "
              "so a move edits folders, paper-build.toml and ../ links only.",
              "Generated files are never moved by hand: delivery/ is rebuilt in the Job by haipipe-paper-assemble; "
              "frozen sent/ builds move as records, unchanged.",
              "Paths inside generated results/ and manifests go stale until their Run reruns; they are never "
              "hand-edited, and old receipts are read through a moves map."]:
        text(0, cy, c, 18, GRAY)
        cy += 34
    close_frame(fr)

    # 3 · the workbench map
    y0 = cy + 300
    fr = open_frame("3 · the workbench map")
    views, spaces = old_views(), []
    for sp, _ in views:
        if sp not in spaces:
            spaces.append(sp)
    left = [f"{sp:<10}{' · '.join(v for s, v in views if s == sp)}" for sp in spaces]
    right = [f"{sp:<10}→ {NEW_HOME.get(sp, '? not placed')}" for sp in spaces]
    r4, b4 = mono(0, y0, left, "old page: /_board/paper-board, four Spaces + Guide (from its Workbench Table)", size=15)
    r5, b5 = mono(r4 + 120, y0, right, "new: the shared frame, Block · Job · Task tabs", size=15)
    old_n, new_n = lines_of(SERVER / "paper.py"), lines_of(SERVER / "paper_theme.py")
    r6, b6 = mono(0, max(b4, b5) + 60, [f"{'paper.py':<18}{old_n:>6} lines  the old page: its readers + its own drawing",
                                         f"{'paper_theme.py':<18}{new_n:>6} lines  the new tab: reuses paper.py's readers, "
                                         "Block tab only today"],
                  "the code", size=15)
    r7, b7 = mono(r6 + 80, max(b4, b5) + 60, [("!" if t.startswith("!") or w.startswith("!") else "") +
                                               f"{t:<62}{w.lstrip('! ')}" for t, w in READERS],
                  "the old readers' layout assumptions, and the change each needs", size=15)
    cy = max(b6, b7) + 40
    sticky(0, cy, 640, "Keep the readers, retire the page: collect(),\nsection_rows() … stay (paper_theme.py uses them);"
                       "\nrender_* and _PAGE go once nothing links them.", "idea")
    sticky(680, cy, 600, "Both pages side by side until you're happy\n(carry over what exists): the band keeps\n"
                         "'the old page ↗' until phase 5.", "idea")
    cy += 180
    close_frame(fr)

    # 4 · the phases
    y0 = cy + 300
    fr = open_frame("4 · the phases")
    rows = [("!" if who == "you" else "") + f"{ph:<14}{what:<84}{who:<13}{check}" for ph, what, who, check in PHASES]
    _, b8 = mono(0, y0, rows, "phase · what moves · who · the check that ends it", size=16)
    cy = b8 + 40
    for c in ["? Live sessions edit these Boards: migrate a Board only when no session works in it.",
              "? Pages link ../Ba-…: the script rewrites them, or lists them for a person (column ../links above).",
              "? Old Run receipts record old paths (column receipts): history, read through a moves map.",
              "? A Board with its own git repo and uncommitted work: commit or stash there first, by its owner."]:
        cy = concern(0, cy, c) + 8
    close_frame(fr)

    y5 = frame_matrix(0, cy + 260)
    y6 = frame_script(0, y5 + 260)
    y7 = frame_example(0, y6 + 260, bs)
    cy = y7

    questions_frame(0, cy + 200, [
        ("(proposed) Q04 · How do the old paper folders and\nworkbench move to the new ladder?",
         [("readers first, then one Board at a\ntime with a dry-run script", "idea"),
          ("your call: j00_story · rounds as\nComments · delivery in the Job", "open")] +
         [(o, "red") for o in OPEN[3:5]])], width=640)


if __name__ == "__main__":
    draw()
    save(Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s03-paper-migration.excalidraw",
         "build_s03_paper_migration.py")
