#!/usr/bin/env python3
"""open_writing_lab.py · the paper writing lab: VS Code windows whose terminals open the Section sessions.

`/hai-paper lab` runs this. Contract: ../ref/writing-lab.md.

    python open_writing_lab.py <paper-root>                 plan only
    python open_writing_lab.py <paper-root> --apply         write the workspace files and open them
        [--prefix <Short>]      session names <Short>-<unit>; default board.md `session-prefix:`
        [--per-window 4]        terminals per VS Code window (default 4)
        [--appendix]            add the Appendix unit (default: the Main Sections only); --no-appendix drops it
        [--sizes 5 2]           units per window, in order (default: an even split by --per-window)
        [--no-board]            leave out the Board session (default: it opens first, in Lab-A)
        [--pages <id> ...]      only these units
        [--terminal vscode]     vscode (default): VS Code windows whose own terminals open the sessions
                                (needs the Paper Writing Lab extension, ../vscode-lab, installed once);
                                tmux: tmux sessions shown in Terminal windows
        [--no-open]             write the files, open nothing
        [--version <job>]       the writing Job; default the newest
        [--no-codex]            skip the Codex side (default: a Codex thread per unit that has none)
        [--close | --restart]   close or reload the paper's open lab windows (extension 0.3+)
        [--refresh]             reopen each page fresh in VS Code's browser, sessions untouched (extension 0.6+)

A unit is what one Section session owns (create_section_sessions.py builds the units). The Main Sections are
split as evenly as possible over ceil(n / per-window) windows. By default each window is a VS Code
window (a `.code-workspace` whose `haipipeLab.terminals` the Paper Writing Lab extension, ../vscode-lab, opens as
VS Code terminals in a grid); --terminal tmux makes it a tmux session shown in Terminal instead.
--appendix and --sizes are kept in the lab folder's layout.json on --apply, so the next lab opens the same way.
Files go under ~/.config/haipipe/labs/<paper>/. Each pane runs lab_launch.py: it resumes the unit's `session:` when its transcript exists, else starts a new
session with that id and the unit's read-only first turn. A unit with no `session:`, or one naming another
unit's session, gets a new id written into its page header on --apply.

The Board session is the session in charge of the whole paper (JL 261114: "the session for the whole block"):
it plans, routes rulings to the Sections, builds and checks the paper. board.md names it in `board-session:`;
the lab opens it first, beside the Board's own page, and resumes it under whatever name it has. A Board with no
`board-session:` gets a new session, named <Short>-Board, recorded on --apply. It has no Codex twin here.
"""
import argparse
import json
import math
import os
import shutil
import subprocess
import time
import sys
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import create_section_sessions as css  # noqa: E402

def fresh_env() -> dict:
    """This process's environment without the calling session's own variables (every CLAUDE* and CODEX_COMPANION*).
    A VS Code window opened by `code --new-window` gives its terminals the caller's environment, so a `claude` started
    there read CLAUDE_CODE_CHILD_SESSION and ran as a child with transcript saving off, holding the parent's messaging
    socket too (JL 261116: "I have this issue")."""
    keep = {"CLAUDE_BIN", "CLAUDE_CONFIG_DIR"}                       # where claude is and its home, the person's own
    return {k: v for k, v in os.environ.items() if k in keep or not k.startswith(("CLAUDE", "CODEX_COMPANION"))}


LABS = Path(os.environ.get("HAIPIPE_LABS_DIR", Path.home() / ".config" / "haipipe" / "labs"))


def transcript(sid):
    home = Path(os.environ.get("CLAUDE_CONFIG_DIR", Path.home() / ".claude"))
    return next(iter((home / "projects").glob(f"*/{sid}.jsonl")), None) if sid else None


def plan_units(paper, prefix, appendix, pages):
    """[(unit, name, sid, state)]: state is resume, start (id kept, no transcript yet) or new (id to write)."""
    units = css.build_units(css.section_pages(paper), "one")
    if not appendix:
        units = [u for u in units if u["key"] != "Appendix"]
    if pages:
        units = [u for u in units if u["key"] in pages or any(p in pages for p, _ in u["pages"])]
    out = []
    for u in units:
        name = f"{prefix}-{u['key']}"
        sid = css.unit_header(u, "session")
        title = css.claude_title(sid) if sid else None
        if sid and title is not None and title not in ("", name):
            sid, state = "", "new"            # a predecessor's or another unit's session
        elif sid and title is not None:
            state = "resume"
        elif sid:
            state = "start"                   # an id on the page whose transcript never existed or is gone
        else:
            state = "new"
        out.append((u, name, sid or str(uuid.uuid4()), state))
    return out


BOARD = "Board"


def board_unit(paper, prefix):
    """The Board session as a lab unit: (unit, name, sid, state). Any saved name is kept (it is the person's)."""
    md = paper / "board.md"
    sid = css.header_value(md, "board-session")
    state = ("resume" if transcript(sid) else "start") if sid else "new"
    return ({"key": BOARD, "pages": [(BOARD, md)]}, f"{prefix}-{BOARD}", sid or str(uuid.uuid4()), state)


def board_prompt(root, paper, version):
    rel = lambda p: p.relative_to(root).as_posix()
    return f"""You are the Board session of the paper {paper.name}: the session in charge of the whole paper.
Board: {rel(paper / 'board.md')}. Writing Job: {rel(version)}.
Each Section has its own session (`session:` in its page header); they write their Section. You plan the paper,
route rulings to the Sections, build the paper (delivery/build.py), run paper_check.py and keep the checklist.
Use /hai-paper. Work in place, never a worktree. Do not edit a Section's Draft while its session works on it.
This first turn is read only: read board.md and the writing Job face, then say in three lines where the paper stands.
"""


def windows(items, per):
    """Split evenly: 8 by 4 is 4+4, 6 by 4 is 3+3, 9 by 4 is 3+3+3."""
    n = max(1, math.ceil(len(items) / per))
    size, extra = divmod(len(items), n)
    out, i = [], 0
    for w in range(n):
        k = size + (1 if w < extra else 0)
        out.append(items[i:i + k])
        i += k
    return out


LAYOUT = "layout.json"


def by_sizes(items, sizes):
    """The windows the person asked for: --sizes 5 2 puts the first five units in Lab-A, the next two in Lab-B."""
    out, i = [], 0
    for k in sizes:
        out.append(items[i:i + k])
        i += k
    return out


def saved_layout(out_dir):
    """What the last --apply kept for this paper: {"appendix": bool, "sizes": [..]}; {} when none or unreadable."""
    try:
        return json.loads((out_dir / LAYOUT).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def board_origin(root):
    """The workbench origin readers use: `.server_config/settings.env` PUBLIC_URL or DOMAIN (a JJLUO_ prefix
    stripped), else None. Never localhost (AGENTS.md, Board serving)."""
    env = root / ".server_config" / "settings.env"
    keys = {}
    if env.is_file():
        for line in env.read_text(encoding="utf-8").splitlines():
            k, _, v = line.partition("=")
            keys[k.strip().removeprefix("JJLUO_")] = v.strip().strip("'\"")
    origin = keys.get("PUBLIC_URL") or keys.get("DOMAIN")
    if origin and "://" not in origin:
        origin = f"http://{origin}" + (f":{keys['PORT']}" if keys.get("PORT") else "")
    return origin.rstrip("/") if origin else None


def page_url(root, unit):
    """The unit's first page in the workbench (its draft view), or None without a configured origin."""
    origin = board_origin(root)
    if not origin:
        return None
    rel = unit["pages"][0][1].parent.relative_to(root).as_posix()
    return f"{origin}/_board/workbench?path={rel}&layout=focus"


def workspace(root, version, group, prompts):
    """One VS Code window: the writing Job and the repository as folders, and `haipipeLab.terminals`, which the
    Paper Writing Lab extension (../vscode-lab) opens as each unit's draft page above (its `url`) and its session
    terminal in the panel below."""
    launcher = HERE / "lab_launch.py"
    claude = shutil.which("claude") or "claude"
    terms = [{"name": u["key"], "url": page_url(root, u), "cwd": str(root),
              "command": f"CLAUDE_BIN='{claude}' python3 '{launcher}' {sid} {name} '{prompts / (u['key'] + '.txt')}'"}
             for u, name, sid, _ in group]
    return {
        "folders": [{"name": version.name, "path": str(version)}, {"name": root.name, "path": str(root)}],
        "settings": {"haipipeLab.terminals": terms},
    }


def signal_windows(out_dir, action):
    """Write `haipipeLab.window` {action, at} into each lab workspace; the extension (0.3+) in an open window
    closes or reloads it on that change. A window that is not open is untouched (its file opens normally later:
    the action is read only on a change)."""
    import datetime
    files = sorted(out_dir.glob("*.code-workspace"))
    if not files:
        sys.exit(f"{out_dir}: no lab workspaces; run --apply first")
    at = datetime.datetime.now().isoformat(timespec="seconds")
    for f in files:
        d = json.loads(f.read_text(encoding="utf-8"))
        d.setdefault("settings", {})["haipipeLab.window"] = {"action": action, "at": at}
        f.write_text(json.dumps(d, indent=2) + "\n", encoding="utf-8")
        print(f"{action}: {f.name}")


def codex_side(paper, prefix, units, missing):
    """The Codex side of each unit: create_section_sessions.py --providers codex makes a Codex thread (shown in
    the Codex app, named <Short>-<unit>-Codex), runs the same read-only first turn, writes `codex-session:` and
    pairs it with the unit's Claude session. Units that already name a Codex thread are skipped."""
    pages = [p for u, _, _, _ in units if u["key"] in missing for p, _ in u["pages"]]
    env = {k: v for k, v in os.environ.items() if not k.startswith("CODEX_COMPANION")}
    print(f"codex: creating {len(missing)} Codex Section sessions (first turns take a few minutes)")
    subprocess.run([sys.executable, str(HERE / "create_section_sessions.py"), str(paper), "--prefix", prefix,
                    "--providers", "codex", "--pages", *pages, "--apply"], env=env, check=False)


def extension_installed():
    r = subprocess.run(["code", "--list-extensions"], capture_output=True, text=True)
    return "haipipe.paper-lab" in r.stdout


def tmux_lab(root, group, prompts, session, out_dir, show):
    """One tmux session per window, one pane per unit, tiled, each pane titled with its unit."""
    launcher = HERE / "lab_launch.py"
    claude = shutil.which("claude") or "claude"
    if subprocess.run(["tmux", "has-session", "-t", session], capture_output=True).returncode != 0:
        for i, (u, name, sid, _) in enumerate(group):
            cmd = ["python3", str(launcher), sid, name, str(prompts / f"{u['key']}.txt")]
            if i == 0:
                subprocess.run(["tmux", "new-session", "-d", "-s", session, "-x", "240", "-y", "64",
                                "-c", str(root), "-e", f"CLAUDE_BIN={claude}", *cmd], env=fresh_env(), check=True)
            else:
                subprocess.run(["tmux", "split-window", "-t", session, "-c", str(root),
                                "-e", f"CLAUDE_BIN={claude}", *cmd], check=True)
                subprocess.run(["tmux", "select-layout", "-t", session, "tiled"], check=True)
            subprocess.run(["tmux", "select-pane", "-t", f"{session}.{i}", "-T", u["key"]], check=True)
        for opt in (["pane-border-status", "top"], ["pane-border-format", " #{pane_title} "], ["mouse", "on"],
                    ["remain-on-exit", "on"]):
            subprocess.run(["tmux", "set-option", "-t", session, *opt], check=True)
        print(f"started tmux session {session}")
    else:
        print(f"tmux session {session} already runs; showing it")
    cmd_file = out_dir / f"{session}.command"
    cmd_file.write_text(f"#!/bin/zsh\nexec tmux attach -t {session}\n", encoding="utf-8")
    cmd_file.chmod(0o755)
    if show:
        subprocess.run(["open", "-a", "Terminal", str(cmd_file)], check=False)
        print(f"opened {session} in Terminal")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paper", help="the paper root (the folder holding board.md)")
    ap.add_argument("--prefix")
    ap.add_argument("--per-window", type=int, default=4)
    ap.add_argument("--appendix", action=argparse.BooleanOptionalAction, default=None, help="add the Appendix unit")
    ap.add_argument("--sizes", type=int, nargs="+", help="units per window, in order, e.g. 5 2")
    ap.add_argument("--no-board", action="store_true", help="leave out the Board session")
    ap.add_argument("--pages", nargs="*", default=None)
    ap.add_argument("--apply", action="store_true", help="write the files and open them (default: plan only)")
    ap.add_argument("--terminal", choices=["vscode", "tmux"], default="vscode")
    ap.add_argument("--no-open", action="store_true")
    ap.add_argument("--no-codex", action="store_true",
                    help="skip the Codex side (default: create a Codex thread for each unit without `codex-session:`)")
    ap.add_argument("--close", action="store_true", help="close the paper's open lab windows (sessions keep their transcripts)")
    ap.add_argument("--restart", action="store_true", help="reload the paper's open lab windows in place")
    ap.add_argument("--refresh", action="store_true", help="reopen each page fresh, sessions untouched (extension 0.6+)")
    ap.add_argument("--version")
    a = ap.parse_args()
    css.VERSION = a.version

    paper = Path(a.paper).resolve()
    if not (paper / "board.md").is_file():
        sys.exit(f"{paper}: no board.md; pass the paper root")
    root = css.repo_root(paper)
    if a.close or a.restart or a.refresh:
        signal_windows(LABS / paper.name, "close" if a.close else "restart" if a.restart else "refresh")
        return
    recorded = css.board_prefix(paper)
    if a.prefix and recorded and a.prefix != recorded:
        sys.exit(f"the writing Job (or board.md) records session-prefix: {recorded}; use it, or edit that line first")
    prefix = a.prefix or recorded
    if not prefix:
        sys.exit("pass --prefix <Short>: two or three words naming this paper, unused by other papers")
    story, order = css.compile_order(paper)
    version = css.current_version(paper)
    if not story or not version:
        sys.exit("no writing Job with a `haipipe:compile-order` block: settle the Section structure first")

    out_dir = LABS / paper.name
    kept = saved_layout(out_dir)
    appendix = kept.get("appendix", False) if a.appendix is None else a.appendix
    units = plan_units(paper, prefix, appendix, a.pages)
    if not units:
        sys.exit("no Section units found")
    lab = ([] if a.no_board or a.pages else [board_unit(paper, prefix)]) + units
    sizes = a.sizes or ([] if a.pages or a.no_board else kept.get("sizes") or [])
    if a.sizes and (sum(sizes) != len(lab) or min(sizes) < 1):
        sys.exit(f"--sizes {' '.join(map(str, sizes))} must add up to the {len(lab)} units of this lab")
    groups = by_sizes(lab, sizes) if sizes and sum(sizes) == len(lab) else windows(lab, a.per_window)
    letters = "ABCDEFGHIJ"
    for w, g in enumerate(groups):
        print(f"{prefix}-Lab-{letters[w]}")
        for u, name, sid, state in g:
            print(f"  {u['key']:<40} {state:<7} {sid}  {name}")
    if not a.apply:
        print("plan only; --apply writes the workspaces and opens them")
        return

    if not recorded:
        css.record_prefix(paper, prefix)
    prompts = out_dir / "prompts"
    prompts.mkdir(parents=True, exist_ok=True)
    if not a.pages and not a.no_board:
        (out_dir / LAYOUT).write_text(json.dumps({"appendix": appendix, "sizes": [len(g) for g in groups] if sizes else []})
                                      + "\n", encoding="utf-8")
    for old in out_dir.glob("*.code-workspace"):
        old.unlink()   # only the current layout stays
    files = []
    for w, g in enumerate(groups):
        for u, name, sid, state in g:
            if u["key"] == BOARD:
                if state == "new":
                    css.write_header(u["pages"][0][1], "board-session", sid)
                (prompts / f"{BOARD}.txt").write_text(board_prompt(root, paper, version), encoding="utf-8")
                continue
            if state == "new":
                for _, md in u["pages"]:
                    css.write_header(md, "session", sid)
            (prompts / f"{u['key']}.txt").write_text(css.first_prompt(root, paper, u, story), encoding="utf-8")
        session = f"{prefix}-Lab-{letters[w]}"
        if a.terminal == "tmux":
            tmux_lab(root, g, prompts, session, out_dir, show=not a.no_open)
            continue
        f = out_dir / f"{session}.code-workspace"
        f.write_text(json.dumps(workspace(root, version, g, prompts), indent=2) + "\n", encoding="utf-8")
        files.append(f)
        print(f"wrote {f}")
    missing = [] if a.no_codex else [u["key"] for u, _, _, _ in units if not css.unit_header(u, "codex-session")]
    if a.no_open or a.terminal == "tmux":
        if missing:
            codex_side(paper, prefix, units, missing)
        return
    if not extension_installed():
        vsix = HERE.parent / "vscode-lab" / "build_vsix.sh"
        print("The Paper Writing Lab extension is not installed, so the windows open without their terminals."
              f" Install it once: bash '{vsix}' && code --install-extension '{vsix.parent / 'paper-lab.vsix'}'")
    for f in files:
        subprocess.run(["code", "--new-window", str(f)], env=fresh_env(), check=False)
        print(f"opened {f.name}")
        time.sleep(3)   # two quick `code --new-window` calls can drop one window (JL 261114: Lab-A never opened)
    if missing:   # after the windows, so they are not kept waiting for the Codex first turns
        codex_side(paper, prefix, units, missing)

if __name__ == "__main__":
    main()
