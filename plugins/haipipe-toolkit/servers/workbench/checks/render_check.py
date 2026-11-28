"""Render every real file of each kind a Block holds through the page code that reads it (hai-ui A09; JL 261126:
"do we have the code to preview the folder and file content, to make sure the generated files and folder can be
rendered to the html").

    PYTHONPATH=plugins/haipipe-toolkit/servers/_host <host venv python> \\
        plugins/haipipe-toolkit/servers/workbench/checks/render_check.py [examples/<Project>/...] [--kind "Task face"]

The kinds are the rows of the format table, `examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec/
file-formats.md`; this script names the same kinds (a test keeps the two lists equal). For each file of a kind it
renders the page that shows it, in this process, and reports a page that raises, comes back empty, or does not show
the file's name or its goal. One line per problem with ❗, a count per kind, exit 1 on any problem.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
import time
from pathlib import Path

SPACE = next(p for p in Path(__file__).resolve().parents if (p / "plugins" / "haipipe-toolkit").is_dir())
TABLE = SPACE / "examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec/file-formats.md"
BLOCK = "*/*/b[0-9]*_*"                                   # <Project>/<theme folder>/bNN_<block>, under examples/


def table_kinds(path: Path = TABLE) -> list[str]:
    """The kinds the format table names, in its order (the first cell of each body row)."""
    rows = re.findall(r"(?m)^\| ([^|`]+?) \| `", path.read_text(encoding="utf-8"))
    return [r.strip() for r in rows if r.strip() != "Kind"]


def _live():
    sys.path.insert(0, str(SPACE / "plugins/haipipe-toolkit/servers/_host"))
    from host_paths import bootstrap
    bootstrap()
    import live  # noqa: F401  (grafts every server folder onto live)


def page(folder: Path, **kw) -> str:
    from live import focus_page, frame
    theme = frame.themes().get(frame.theme_of(folder, SPACE), frame.VANILLA)
    return focus_page.render(theme, SPACE, folder, **kw)


def goal(face: Path) -> str:
    m = re.search(r"(?m)^goal:\s*(.+)$", face.read_text(encoding="utf-8", errors="ignore"))
    return m[1].strip() if m and not m[1].strip().startswith("<") else ""


def shows(out: str, words: str) -> bool:
    """The words are on the page, as text (escaped or not), ignoring how lines wrap."""
    flat = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", out)).split())
    return " ".join(words.split())[:40] in flat


def face_page(face: Path, need_goal: bool) -> str:
    """'' when the page of this face renders and shows its folder's name (and its goal), else the problem."""
    folder = face.parent
    out = page(folder)
    if len(out) < 500:
        return "renders empty"
    if folder.name not in out:
        return "does not show its folder's name"
    g = goal(face) if need_goal else ""
    if g and not shows(out, g):
        return f"does not show its goal ({g[:40]}…)"
    return ""


def run_card(card: Path) -> str:
    from live.focus_runs import run_rows
    task = card.parent.parent.parent
    if not any(r == card.parent for r, _, _ in run_rows(task)):
        return "its Task's Run rows leave it out"
    return ""


def run_pass(pass_md: Path) -> str:
    from live.focus_plan_results import round_rows
    run, task = pass_md.parent.parent.parent, pass_md.parent.parent.parent.parent.parent
    rows = [r for r in round_rows(task) if r[4] == "round" and r[5] == pass_md.parent]
    if not rows:
        return "its Task's rounds leave it out"
    if not rows[0][1].strip():
        return "its round has no title"
    return ""


def trace(face: Path) -> str:
    from live import trace_view
    meta = trace_view.read(face)
    if not meta:
        return "front matter does not read"
    missing = [k for k in ("title", "date", "aim", "plan") if not meta.get(k)]
    return f"front matter lacks {', '.join(missing)}" if missing else ""


def topic(face: Path) -> str:
    holder = face.parent.parent
    out = page(holder, section="studio")
    num = face.parent.name.split("-", 1)[0]
    return "" if re.search(rf">\s*{re.escape(num)}\b", out) else f"the Studio of {holder.name} does not list it"


def page_spec(views: Path) -> str:
    block = views.parent.parent.parent
    level = views.name.split("-", 1)[0]
    out = page(block, section="report", group=f"ui-{level}")
    return "" if len(out) > 500 else "its view renders empty"


# kind: (glob under examples/, check)
KINDS = {
    "Block face": (f"{BLOCK}/board.md", lambda f: face_page(f, False)),
    "Job face": (f"{BLOCK}/j[0-9]*_*/j[0-9]*_*.md", lambda f: face_page(f, True) if f.stem == f.parent.name else ""),
    "Task face": (f"{BLOCK}/j[0-9]*_*/t[0-9]*_*/t[0-9]*_*.md", lambda f: face_page(f, True) if f.stem == f.parent.name else ""),
    "Run card": (f"{BLOCK}/j[0-9]*_*/t[0-9]*_*/runs/*/run.yaml", run_card),
    "Run round (pass)": (f"{BLOCK}/j[0-9]*_*/t[0-9]*_*/runs/*/passes/p[0-9]*-*/pass.md", run_pass),
    "Trace": (f"{BLOCK}/trace/[0-9]*/[0-9]*_*.md", trace),
    "Studio topic face": (f"{BLOCK}/s[0-9]*-*/s[0-9]*-*.md", lambda f: topic(f) if f.stem == f.parent.name else ""),
    "Page spec views table": (f"{BLOCK}/delivery/page-spec/*-views.md", page_spec),
}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("under", nargs="?", default="examples")
    ap.add_argument("--kind", action="append")
    a = ap.parse_args(argv)
    _live()
    base = (SPACE / a.under).resolve()
    bad, t0 = 0, time.perf_counter()
    for kind, (pattern, check) in KINDS.items():
        if a.kind and kind not in a.kind:
            continue
        files = [f for f in sorted((SPACE / "examples").glob(pattern)) if f == base or base in f.parents]
        problems = []
        for f in files:
            try:
                why = check(f)
            except Exception as e:                       # noqa: BLE001  a page that raises is the finding
                why = f"raises {type(e).__name__}: {str(e)[:80]}"
            if why:
                problems.append(f"❗ {kind}: {f.relative_to(SPACE)}: {why}")
        print("\n".join(problems)) if problems else None
        print(f"{'❗' if problems else '✅'} {kind}: {len(files)} files, {len(problems)} problems")
        bad += len(problems)
    print(f"{'❗' if bad else '✅'} render check: {bad} problems in {time.perf_counter() - t0:.0f} s")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
