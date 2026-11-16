#!/usr/bin/env python3
"""/lab <Block>: open a theme Block (paper, insight, design, labeling) as a lab, VS Code windows whose terminals
run that Block's Claude sessions, the way /wb opens its page.

    lab.py <Block path | words>              open the lab (writes the lab files, opens VS Code)
    lab.py <Block> --plan                    print the windows and sessions, open nothing
        [--jobs j01 j03 ...]                 only these Jobs (default: every Job, newest last; at most --max)
        [--max 8]                            sessions per lab, the Board session included
        [--per-window 4]                     terminals per VS Code window
        [--no-board]                         leave out the Board session
        [--prefix <Short>]                   session names <Short>-<unit>; default board.md `session-prefix:`,
                                             else the Block folder's name
        [--terminal vscode|tmux]             vscode (default) or tmux shown in Terminal
        [--no-open]                          write the files, open nothing
    lab.py <Block> --close | --restart | --refresh    close, reload or refresh its open lab windows

A paper Block with a writing Job goes to the paper writing lab (haipipe-paper scripts/open_writing_lab.py: one
session per Section); any other paper argument after the Block is passed on to it. An insight, design or labeling
Block (or a paper Block with no writing Job yet) gets one session for the whole Block (the Board session) and one
per Job. Session ids live outside the Block, in ~/.config/haipipe/labs/<Project>--<Block>/sessions.json, so the Block's
files are never written; a board.md `board-session:` line is honoured when present. Each terminal runs the paper
lab's lab_launch.py: it resumes a session whose transcript exists, else starts it with a read-only first turn.
Contract: ../SKILL.md.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path

SKILLS = next(p for p in Path(__file__).resolve().parents if p.name == "skills")
sys.path.insert(0, str(SKILLS / "1_base" / "workbench" / "workbench" / "cli"))
PAPER = SKILLS / "2_theme" / "paper" / "haipipe-paper" / "scripts"
sys.path.insert(0, str(PAPER))
import wb  # noqa: E402  (the /wb finder: SPACE root, words to a place, frame helpers)
import open_writing_lab as owl  # noqa: E402  (windows, workspace signals, tmux, extension check)

LAB_THEMES = {"paper": "haipipe-paper", "insight": "haipipe-insight", "design": "haipipe-design",
              "labeling": "haipipe-labeling"}
BOARD = "Board"
LETTERS = "ABCDEFGHIJ"


def lab_theme(block: Path, root: Path) -> str:
    """The theme a Block's lab runs under: its page theme, except a Question Book (`board-kind: prototype`), which is
    an insight Block (insight/InsightQuestionBook-<Topic>/, the questions of the Board beside it) although its page
    opens on the work page."""
    theme = wb.frame.theme_of(block, root)
    face = block / "board.md"
    if theme == "work" and face.is_file() and re.search(r"(?m)^board-kind:\s*prototype\s*$",
                                                        face.read_text(encoding="utf-8", errors="ignore")[:2000]):
        return "insight"
    return theme


def labs_dir() -> Path:
    return Path(os.environ.get("HAIPIPE_LABS_DIR", Path.home() / ".config" / "haipipe" / "labs"))


def find_block(query: str, root: Path) -> Path:
    """A Block from a path or plain words, the /wb way; a Job or Task path opens its Block's lab."""
    folder = wb.resolve_path(query, root)
    if folder is None:
        found = wb.places(root)
        named = wb.by_name(query, found) if " " not in query else []
        if len(named) == 1:
            folder = root / named[0].path
        else:
            ranked, words = wb.rank(found, query)
            if not ranked or not wb.clear_winner(ranked, words):
                tops = "\n".join(f"  {p.level:<6} {p.path}" for p in ranked[:5])
                sys.exit(f"lab: no single Block matches {query!r}; pass its path" + (f":\n{tops}" if tops else ""))
            folder = root / ranked[0].path
    if folder.is_file():
        folder = folder.parent
    for p in (folder, *folder.parents):
        if p == root or root not in p.parents:
            break
        if wb.frame.level_of(p) == "Block":
            return p
    sys.exit(f"lab: {folder} is not inside a Block; /lab opens a Block (pass a Block, Job or Task path)")


def header(md: Path, key: str) -> str:
    """A `key: value` line in the file's first 40 lines (front matter or header block), or ""."""
    if not md.is_file():
        return ""
    for line in md.read_text(encoding="utf-8", errors="replace").splitlines()[:40]:
        m = re.match(rf"{re.escape(key)}:\s*(.*)$", line)
        if m:
            return m.group(1).strip().strip("'\"")
    return ""


def transcript(sid: str) -> bool:
    home = Path(os.environ.get("CLAUDE_CONFIG_DIR", Path.home() / ".claude"))
    return bool(sid) and any((home / "projects").glob(f"*/{sid}.jsonl"))


def paper_lab_ready(block: Path) -> bool:
    """A paper Block the writing lab can open: a writing Job with its compile order."""
    try:
        story, _ = owl.css.compile_order(block)
        return bool(story and owl.css.current_version(block))
    except SystemExit:
        return False


def load_sessions(out_dir: Path) -> dict:
    f = out_dir / "sessions.json"
    try:
        return json.loads(f.read_text(encoding="utf-8")) if f.is_file() else {}
    except ValueError:
        return {}


def plan(block: Path, prefix: str, jobs: list[str] | None, limit: int, no_board: bool, saved: dict) -> list[dict]:
    """[{key, folder, name, sid, state}]: the Board session first, then one per Job. state: resume (transcript
    exists), start (an id kept, no transcript yet) or new."""
    units = []
    if not no_board:
        units.append({"key": BOARD, "folder": block})
    children = list(wb.frame.children(block, "Block"))
    if jobs:
        children = [j for j in children if any(j.name == k or j.name.startswith(k + "_") for k in jobs)]
    room = max(0, limit - len(units))
    if len(children) > room:
        children = children[-room:] if room else []      # the newest Jobs, in order
    units += [{"key": j.name.split("_", 1)[0], "folder": j} for j in children]
    for u in units:
        sid = (header(block / "board.md", "board-session") if u["key"] == BOARD else "") or saved.get(u["key"], {}).get("sid", "")
        u["name"] = saved.get(u["key"], {}).get("name") or f"{prefix}-{u['key']}"
        u["state"] = ("resume" if transcript(sid) else "start") if sid else "new"
        u["sid"] = sid or str(uuid.uuid4())
    return units


def first_turn(u: dict, block: Path, root: Path, theme: str) -> str:
    rel = lambda p: p.relative_to(root).as_posix()
    skill = LAB_THEMES[theme]
    if u["key"] == BOARD:
        return f"""You are the Board session of the {theme} Block {block.name}: the session in charge of the whole Block.
Block face: {rel(block / 'board.md')}. Each Job has its own session in this lab; you plan the Block, route rulings
to the Jobs, and keep the Block face, its Questions and its delivery. Use /{skill}. Work in place, never a worktree.
Do not edit a Job's files while its session works on it.
This first turn is read only: read board.md, then say in three lines where the Block stands and what comes next.
"""
    face = wb.frame.face(u["folder"]) or u["folder"]
    return f"""You are the session of Job {u['folder'].name} in the {theme} Block {block.name}.
Job: {rel(u['folder'])} (face: {rel(face)}). Use /{skill}. Work in place, never a worktree. Stay inside this Job:
another Job's work belongs to its own session, and the whole Block belongs to the Board session.
This first turn is read only: read the Job face, then say in three lines where the Job stands and what comes next.
"""


def page_url(root: Path, folder: Path) -> str | None:
    origin = owl.board_origin(root)
    return origin + wb.focus_url(folder, root) if origin else None


def workspace(root: Path, block: Path, group: list[dict], prompts: Path) -> dict:
    """One VS Code window in the paper lab's format: the Block and the SPACE as folders, and haipipeLab.terminals,
    which the Lab extension (haipipe-paper vscode-lab/) opens as each unit's page above and its terminal below."""
    launcher = PAPER / "lab_launch.py"
    claude = shutil.which("claude") or "claude"
    terms = [{"name": u["key"], "url": page_url(root, u["folder"]), "cwd": str(root),
              "command": f"CLAUDE_BIN='{claude}' python3 '{launcher}' {u['sid']} {u['name']} '{prompts / (u['key'] + '.txt')}'"}
             for u in group]
    return {"folders": [{"name": block.name, "path": str(block)}, {"name": root.name, "path": str(root)}],
            "settings": {"haipipeLab.terminals": terms}}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="lab.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("words", nargs="+", help="a Block path, or words that find it")
    ap.add_argument("--root")
    ap.add_argument("--plan", action="store_true", help="print the windows and sessions, open nothing")
    ap.add_argument("--jobs", nargs="*")
    ap.add_argument("--max", type=int, default=8)
    ap.add_argument("--per-window", type=int, default=4)
    ap.add_argument("--no-board", action="store_true")
    ap.add_argument("--prefix")
    ap.add_argument("--terminal", choices=["vscode", "tmux"], default="vscode")
    ap.add_argument("--no-open", action="store_true")
    ap.add_argument("--close", action="store_true")
    ap.add_argument("--restart", action="store_true")
    ap.add_argument("--refresh", action="store_true")
    a, rest = ap.parse_known_args(argv)

    root = Path(a.root).resolve() if a.root else wb.space_root(Path.cwd().resolve())
    if root is None:
        sys.exit("lab: no SPACE root above this folder (no env.sh or .server_config); pass --root")
    block = find_block(" ".join(a.words).strip(), root)
    theme = lab_theme(block, root)
    if theme not in LAB_THEMES:
        sys.exit(f"lab: {block.name} is a {theme or 'plain'} Block; /lab opens paper, insight, design and labeling "
                 f"Blocks. Use /wb {block.relative_to(root)} for its page.")
    # a paper lab keeps the writing lab's folder name; any other Block is keyed by its Project too, since
    # Block names (b01_...) repeat across Projects
    out_dir = labs_dir() / (block.name if theme == "paper" else f"{block.parent.parent.name}--{block.name}")
    if a.close or a.restart or a.refresh:
        owl.signal_windows(out_dir, "close" if a.close else "restart" if a.restart else "refresh")
        return 0

    if theme == "paper" and paper_lab_ready(block):
        args = [sys.executable, str(PAPER / "open_writing_lab.py"), str(block), "--per-window", str(a.per_window),
                "--terminal", a.terminal, *rest]
        args += [] if a.plan else ["--apply"]
        args += ["--prefix", a.prefix] if a.prefix else []
        args += ["--no-board"] if a.no_board else []
        args += ["--no-open"] if a.no_open else []
        print(f"{block.name}: paper writing lab (one session per Section)", flush=True)
        return subprocess.run(args).returncode
    if rest:
        sys.exit(f"lab: unknown arguments {' '.join(rest)}")

    prefix = a.prefix or header(block / "board.md", "session-prefix") or block.name
    saved = load_sessions(out_dir)
    units = plan(block, prefix, a.jobs, a.max, a.no_board, saved)
    if not units:
        sys.exit(f"lab: {block.name} has no Jobs to open")
    groups = owl.windows(units, a.per_window)
    print(f"{block.name}: {theme} lab")
    for w, g in enumerate(groups):
        print(f"{prefix}-Lab-{LETTERS[w]}")
        for u in g:
            print(f"  {u['key']:<8} {u['state']:<7} {u['sid']}  {u['name']}  {u['folder'].relative_to(root)}")
    if a.plan:
        print("plan only; drop --plan to write the lab and open it")
        return 0

    prompts = out_dir / "prompts"
    prompts.mkdir(parents=True, exist_ok=True)
    saved.update({u["key"]: {"sid": u["sid"], "name": u["name"]} for u in units})
    (out_dir / "sessions.json").write_text(json.dumps(saved, indent=2) + "\n", encoding="utf-8")
    for u in units:
        (prompts / f"{u['key']}.txt").write_text(first_turn(u, block, root, theme), encoding="utf-8")
    for old in out_dir.glob("*.code-workspace"):
        old.unlink()                                         # only the current layout stays
    files = []
    for w, g in enumerate(groups):
        session = f"{prefix}-Lab-{LETTERS[w]}"
        if a.terminal == "tmux":
            tg = [({"key": u["key"]}, u["name"], u["sid"], u["state"]) for u in g]
            owl.tmux_lab(root, tg, prompts, session, out_dir, show=not a.no_open)
            continue
        f = out_dir / f"{session}.code-workspace"
        f.write_text(json.dumps(workspace(root, block, g, prompts), indent=2) + "\n", encoding="utf-8")
        files.append(f)
        print(f"wrote {f}")
    if a.no_open or a.terminal == "tmux":
        return 0
    if not owl.extension_installed():
        vsix = PAPER.parent / "vscode-lab" / "build_vsix.sh"
        print("The Lab extension is not installed, so the windows open without their terminals. Install it once:"
              f" bash '{vsix}' && code --install-extension '{vsix.parent / 'paper-lab.vsix'}'")
    for f in files:
        subprocess.run(["code", "--new-window", str(f)], check=False)
        print(f"opened {f.name}")
        time.sleep(3)                                        # two quick --new-window calls can drop a window
    return 0


if __name__ == "__main__":
    sys.exit(main())
