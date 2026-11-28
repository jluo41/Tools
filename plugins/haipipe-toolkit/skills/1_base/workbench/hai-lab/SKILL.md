---
name: hai-lab
description: "Opens a theme Block (paper, insight, design, labeling) as a lab: VS Code windows whose terminals run that Block's sessions, its page above each one. Use to start working on a Block; a path or plain words find it. Trigger: lab, open the lab, start the lab, open sessions for this block, /hai-lab."
metadata:
  version: "0.1.0"
  last_updated: "2026-11-15"
---

# /hai-lab · one Block, its sessions side by side

> Scripts here need Python 3.10+: where a command says `python3`, run it as `uv run --no-project --python 3.13 --with pyyaml --with markdown python ...` (or a SPACE `.venv/bin/python`); see `plugins/haipipe-toolkit/skills/README.md` § Running a skill's scripts.

`/wb <Block>` opens a Block's page. `/hai-lab <Block>` opens the Block to work on: one or more VS Code windows, each
showing up to four pages on top and, in the terminal panel below, the Claude session that owns each page.

## 🚪 Run it

```text
/hai-lab <Block path | words>          open the lab                 cli/lab.py <Block>
/hai-lab <Block> plan                  show windows and sessions    cli/lab.py <Block> --plan
/hai-lab <Block> close | restart       close or reload its windows  cli/lab.py <Block> --close | --restart
/hai-lab <Block> refresh               reopen the pages only        cli/lab.py <Block> --refresh
```

Run from the SPACE root (the folder with `env.sh`): `uv run --no-project --python 3.13 --with pyyaml --with markdown
python Tools/plugins/haipipe-toolkit/skills/1_base/workbench/hai-lab/cli/lab.py <Block>` (from Tools-SPACE, drop
`Tools/`). Options: `--jobs j01 j03` (only these Jobs), `--max 8` (sessions per lab, Board included; past it the
newest Jobs), `--per-window 4`, `--no-board`, `--prefix <Short>`, `--terminal tmux`, `--no-open`.

1. **Find the Block.** A path, or words found the /wb way (`cli/wb.py`); a Job or Task path opens its Block's lab.
   A work, cowork or discovery Block is refused with its /wb link.
2. **Pick the lab by theme.**

| Theme | Lab | Sessions |
|---|---|---|
| paper, with a writing Job | the paper writing lab (`hai-paper` `ref/writing-lab.md`) | Board + one per Section; extra arguments pass through |
| paper without one yet, insight (a Question Book too), design, labeling | the Block lab (this skill) | Board + one per Job |

3. **Say what opens.** `--plan` prints each window and each session's state: `resume` (its transcript exists),
   `start` (an id is kept, no transcript yet) or `new`. Without `--plan` the lab is written and opened.
4. **Report** the windows opened, one line each, and which sessions were new.

## What a Block lab writes

All of it under `~/.config/haipipe/labs/<Project>--<Block>/`, never in the Block:

1. `sessions.json`: each unit's session id and name, so the next `/hai-lab` resumes the same sessions. A board.md
   `board-session:` line wins for the Board session. Names are `<prefix>-Board` and `<prefix>-jNN`; the prefix is
   board.md `session-prefix:`, else the Block folder's name.
2. `prompts/<unit>.txt`: the first turn, read only: the Board session reads board.md, a Job session reads its Job
   face, and each says in three lines where it stands. Each is told its scope: a Job session stays in its Job; the
   Board session plans the Block and never edits a Job's files while that Job's session works.
3. `<prefix>-Lab-<A|B|…>.code-workspace`: the Block and the SPACE as folders and `haipipeLab.terminals`, one
   `{name, url, cwd, command}` per unit; `url` is the unit's focus page at the SPACE's configured origin
   (`.server_config/settings.env`), and `command` runs the paper lab's `scripts/lab_launch.py`, which resumes or
   starts the session and never opens one twice.

## Shared with the paper writing lab

The windows, the tmux form, `--close`/`--restart`/`--refresh` and the VS Code extension are the paper lab's
(`hai-paper` `scripts/open_writing_lab.py`, `vscode-lab/`). The extension is installed once by the person:
`bash <hai-paper>/vscode-lab/build_vsix.sh && code --install-extension <hai-paper>/vscode-lab/paper-lab.vsix`.
Without it the windows open with no terminals, and `/hai-lab` says so. An agent never installs it.

Every open session spends usage while it works; close a terminal to stop its session.
