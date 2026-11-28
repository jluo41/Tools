# Writing lab · terminal windows that open the Section sessions

`/hai-paper lab [paper]` ("start the paper writing lab"), or `/hai-lab <paper>` (the `lab` skill, which also opens insight, design and labeling Blocks), opens the paper's Section sessions side by side:
one window per group of up to four Sections, one pane per Section, each running that Section's own Claude
session. By default a window is a VS Code window: each Section's draft page (its workbench view) side by side on top,
and below them, in the terminal panel, each Section's session, split side by side in the same order; `--terminal tmux` makes it a tmux session `<Short>-Lab-<A|B|…>` shown in a Terminal window instead. It reads the units and `session:` lines that `/hai-paper sessions`
([`section-sessions.md`](section-sessions.md)) keeps, and starts a session itself where a Section has none.

## Run it

From the repository root with the workspace Python:

```text
.venv/bin/python <this skill>/scripts/open_writing_lab.py <paper-root>            plan only
.venv/bin/python <this skill>/scripts/open_writing_lab.py <paper-root> --apply    write and open
    [--prefix <Short>]   session names <Short>-<unit>; default board.md `session-prefix:`, recorded on --apply
    [--per-window 4]     terminals per window
    [--appendix]         add the Appendix unit (default: Main Sections only)
    [--sizes 5 2]        units per window, in order; kept with --appendix in layout.json for the next lab
    [--no-board]         leave out the Board session (default: it opens first)
    [--pages <id> ...]   only these units
    [--terminal vscode]  vscode (default) or tmux
    [--no-open]          write the files, open nothing
    [--version <job>]    the writing Job; default the newest
    [--no-codex]         skip the Codex side
    [--close]            close the paper's open lab windows
    [--restart]          reload them in place
    [--refresh]          reopen each page fresh in VS Code's browser; sessions untouched
```

The plan prints each window and, per unit, what its terminal will do:

```text
resume   the page's `session:` has a transcript: claude --resume <id>
start    the page names an id with no transcript: claude --session-id <id> -n <name> "<first turn>"
new      no `session:` (or one owned by another unit): a new id, written into the page header on --apply
```

## The Board session: the one in charge of the whole paper

JL 261114: "what is the charging session, like the session for the whole block, I think you should add this to the
skill as well". Beside the Section sessions, a paper has one Board session: it plans the paper, routes rulings to
the Sections, builds it (`delivery/build.py`), runs `paper_check.py` and keeps the checklist; it never edits a
Section's Draft while that Section's session works on it. board.md names it in its own header line,
`board-session: <Claude session id>` (the older `session:` line on a Board is a label, not an id).

The lab opens it first, in Lab-A, beside the Board's own page, and resumes it under whatever name the person gave
it. A Board with no `board-session:` gets a new session on `--apply`, named `<Short>-Board`, with a read-only first
turn, and the id is written into board.md. It has no Codex twin, and `--pages` leaves it out. When the Board
session is the one you are typing in, its lab terminal says it is already open and stops.

## What it writes

1. `~/.config/haipipe/labs/<paper>/prompts/<unit>.txt`: the unit's first turn, the same text and scope rules `/hai-paper sessions` uses: a read-only look, then the default review round (paragraph logic, then sentence logic, by fresh reviewers; skipped when the newest Draft was already reviewed at its version; must-check M-D03), and one reply line of its counts;
2. vscode: `~/.config/haipipe/labs/<paper>/<Short>-Lab-<letter>.code-workspace`, two folders (the writing Job, the repository root) and the setting `haipipeLab.terminals`, one `{name, url, cwd, command}` per unit, `url` being the unit's workbench page at the `.server_config/settings.env` origin (never localhost); opened with `code --new-window`. The Paper Writing Lab extension (`vscode-lab/`) reads that list when the window opens, shows each `url` in an editor column and creates the terminals split in the panel, each running `scripts/lab_launch.py <id> <name> <prompt file>` from the repository root, the folder the sessions belong to;
3. tmux: one tmux session per window, tiled panes titled with the unit, and `<Short>-Lab-<letter>.command`, which `open -a Terminal` runs to attach; a running lab is reused, never started twice.

## The Codex side

After the windows open, each unit without `codex-session:` gets a Codex thread through
`create_section_sessions.py --providers codex` ([`section-sessions.md`](section-sessions.md)): named
`<Short>-<unit>-Codex`, shown in the Codex app, given the same first turn and paired with the unit's
Claude session. `--no-codex` skips it.

## The extension, installed once

`vscode-lab/` holds the extension (`package.json`, `extension.js`) and `build_vsix.sh`, which zips it into
`paper-lab.vsix` without npm. The author installs it once:

```text
bash <this skill>/vscode-lab/build_vsix.sh && code --install-extension <this skill>/vscode-lab/paper-lab.vsix
```

An agent builds the `.vsix` but never installs it: an extension that runs commands when a window opens is the
author's decision. A window whose workspace has no `haipipeLab.terminals` is left alone. Running `--apply` again rewrites the list, and an
open window (extension 0.2 or later) reopens whatever page or terminal is missing, so a lab never needs closing to restart.
`--close` and `--restart` write `haipipeLab.window` {action, at} into each workspace; the extension (0.3 or later)
closes an open window on that change, or (0.4 or later) closes the lab's own terminals and opens them again, so each resumes its Section session; it ignores the change when a window opens. A plain window reload is not enough: VS Code restores the old terminals by name, and the lab then starts nothing. The author never has to close
a lab window by hand.

Since 0.5 each page opens in VS Code's integrated browser (`workbench.action.browser.open`: address bar, back,
forward, reload); the iframe webview is used only when that browser is missing. Since 0.6 every open first closes a
column's old tabs, so the page is always fresh, and `--refresh` (or the command "Paper Lab: Refresh pages") reopens
the pages without touching the sessions (JL 261114: "I want the website to be ready and be refreshed"). A newly
installed version runs only in a window opened after the install: `--close`, then `--apply`.

At most eight Main sessions per writing Job (JL 261114): past eight, the last Main Sections share one session
`<first>-to-<last>` (a grant's t00 to t10 gives t00 to t06 plus `t07-to-t10`); the Appendix keeps its own.
The session prefix lives in the writing Job face (`session-prefix:`); board.md's line counts only when the paper
has one writing Job, so a letter and a full proposal in flight never take each other's sessions.

Units split evenly over `ceil(n / per-window)` windows: 8 Sections give 4 + 4, 6 give 3 + 3. Each `--apply` replaces
the paper's lab files; they are generated and live outside the repository.

## Already open

A session already open in another terminal is not opened twice: its terminal says so and stops.

A lab opened from inside a Claude session would hand that session's `CLAUDE_*` markers to every terminal, and
Claude would then save no transcript ("Transcript saving is off"). `lab_launch.py` drops them, keeping only
`CLAUDE_CONFIG_DIR`, so each Section session saves its own transcript.

Eight live sessions spend usage eight times as fast while they work; close a terminal to stop its session.
