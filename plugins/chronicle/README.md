# Chronicle Skills

[Agent Skills](https://agentskills.io/specification) for chronicling daily activity — sessions and emails — into structured, scannable, git-synced artifacts.

## Skills

| Skill | Description |
|-------|-------------|
| [chronicle-session](skills/chronicle-session/SKILL.md) | Log the current Claude Code session as a concise diagram-rich `.txt` under `~/Daily/<date>/` and sync to **your** private `Daily` git repo |
| [chronicle-daily](skills/chronicle-daily/SKILL.md) | Roll up a day's session `.txt` files into one Excalidraw canvas at 22:00 and mark the day closed |
| [chronicle-email](skills/chronicle-email/SKILL.md) | Index emails from MS365 Outlook into organized monthly markdown files with daily sections and reimbursement tracking |

## Quick start in a new workspace

The session+daily skills need a per-user `Daily` git repo. **You provide it**; setup is one command.

### 🆕 If this is your first time using chronicle on this machine

1. Create a private git repo on your forge of choice (GitHub, GitLab, Gitea, etc). Name it whatever — `Daily` is the convention. Don't push anything yet.

   ```bash
   gh repo create <you>/Daily --private
   ```

2. From the workspace root where you want the symlink:

   ```bash
   Tools/plugins/chronicle/bin/setup.sh git@github.com:<you>/Daily.git
   ```

   Or for a local-only setup with no remote:

   ```bash
   Tools/plugins/chronicle/bin/setup.sh init
   ```

3. Test it:

   ```bash
   echo "🧪 test" | Tools/plugins/chronicle/skills/chronicle-session/bin/write-session.sh smoke-test
   ```

That's it. The setup script:

- 📂 Creates or clones `$HOME/Daily/`
- 🔗 Symlinks `<workspace>/Daily → $HOME/Daily`
- 🚫 Adds `Daily` to the workspace `.gitignore` (the symlink is per-user, not workspace content)
- ⏰ Installs the 22:00 launchd / cron rollup job (`dev.$USER.chronicle-daily`)

### 🤖 If Claude is doing this for you

Tell Claude: *"set up chronicle in this workspace, my Daily repo is `git@github.com:<me>/Daily.git`"*. Claude will run `bin/setup.sh` with that argument. If you don't have a remote yet, say *"set up with init"* for local-only.

The skill scripts give a friendly error pointing to `setup.sh` if you ever try to log a session before bootstrapping.

## Daily repo layout

```
$HOME/Daily/
└── YYYY-MM-DD/
    ├── YYMMDD-HHMM-<slug>.txt    one per session, written when it ends
    ├── canvas-YYMMDD.excalidraw  rollup, built once at ~22:00
    └── .closed                    sentinel: day is finalized
```

- **One `.txt` per session.** Each section is an ASCII diagram (folder tree, pipeline, decision table, takeaway box) — see `chronicle-session/SKILL.md`.
- **One canvas per day.** Built by the 22:00 rollup. After `.closed` exists, new sessions automatically route to tomorrow's folder.
- **Multi-device sync** via git: every session pull-rebases before writing and pushes after committing.

## Sync workflow

```
🧑 "/chronicle-session"
        ▼
🤖 chronicle-session  ─ pull --rebase --autostash
                       ─ write YYMMDD-HHMM-<slug>.txt
                       ─ commit · push (retry once on rejection)
        ▼
📂 ~/Daily/<date>/  ←── multi-device git sync
        ▼
⏰ 22:00 launchd
        ▼
🤖 chronicle-daily/rollup.sh  ─ txt-to-canvas.py (rebuild)
                              ─ touch .closed
                              ─ commit · push
        ▼
🖼️ canvas-YYMMDD.excalidraw  +  🔒 .closed
```

## Prerequisites

| Skill | Needs |
|---|---|
| chronicle-session / chronicle-daily | git, bash, [diagram-ascii-canvas](../diagram-skill/skills/diagram-ascii-canvas/) (for the rollup), a private `Daily` git repo |
| chronicle-email | MS365 MCP integration · Outlook account |

## License

MIT
