# Tools

Personal [Claude Code](https://claude.ai/code) skill plugins for productivity,
academic research, visual artifacts, and knowledge management.

## Plugins

| Plugin | Description |
|--------|-------------|
| **[chronicle](plugins/chronicle/)** | Session logs, daily rollups, email indexing, and Obsidian/JSON Canvas workflows |
| **[diagram-skill](plugins/diagram-skill/)** | ASCII diagrams, Excalidraw, draw.io, remote diagram sharing, and progress logs |
| **[haipipe](plugins/haipipe-toolkit/)** | HAI-Pipe research toolkit: data, NN, endpoint, task, experiment, insight, paper, and application workflows |
| **[subjective-label](plugins/subjective-label/)** | Multi-agent subjective text annotation with calibration, validation, and scale workflows |

## Installation

### Quick Setup

```bash
git clone git@github.com:jluo41/Tools.git
cd Tools
./install.sh
```

Then in Claude Code:

```text
/plugin install chronicle@jluo41-tools
/plugin install diagram-skill@jluo41-tools
/plugin install haipipe@jluo41-tools
/plugin install subjective-label@jluo41-tools
```

By default, `install.sh` registers this repository as the `jluo41-tools`
marketplace. If the parent workspace has a `.claude/` directory, it symlinks
the skills into that Claude workspace. If the parent workspace has a `.codex/`
directory, it also symlinks the same skills into `.codex/skills/` for Codex.

### Windows

Native symlinks on Windows require Administrator or Developer Mode, so use the
PowerShell installer, which creates directory **junctions** instead (no special
privileges needed):

```powershell
cd Tools
.\install.ps1                          # marketplace + auto-detected project skills
.\install.ps1 -Project C:\path\repo    # link into a specific workspace
.\install.ps1 -Global                  # also link into ~\.claude\skills
.\install.ps1 -Hooks                   # configure sound hooks in settings.json
.\install.ps1 -All                     # marketplace + global + hooks
.\install.ps1 -Symlink                 # use symlinks instead (needs admin / Dev Mode)
.\install.ps1 -NoMarketplace           # skip marketplace registration
```

Agents are single `.md` files, so without `-Symlink` they are copied rather than
linked. The installer records what it wrote in `.jluo41-tools-agents.json` inside
the agents directory, which is how a re-run can refresh its own copies and delete
retired ones while never touching an agent file you wrote yourself.

Junctions use absolute targets, so re-run `install.ps1` if you relocate the
repo. The generated links are OS/machine-specific — gitignore
`<workspace>/.claude/skills/` and `<workspace>/.codex/skills/` and regenerate
per machine rather than committing them (committed symlinks check out as dead
text stubs on Windows).

### Project Install

```bash
./install.sh --project /path/to/workspace
```

This symlinks every discovered skill into `/path/to/workspace/.claude/skills/`
and `/path/to/workspace/.codex/skills/` when those tool directories exist.
Skill discovery is recursive, so deeply nested skills such as
`haipipe-toolkit/skills/F_paper/4-write/paper-write` are included.

### Global Install

```bash
./install.sh --global
```

This symlinks all skills to `~/.claude/skills/` so they are available in every
Claude Code session.

`_archive/` and `_paper-writing-backup/` are excluded, by both installers, so a
retired skill never lands in your skills directory.

Duplicate skill names are resolved deterministically because one skills directory
cannot contain two symlinks with the same basename. No promotion rule is live
today: every skill name is currently unique, so the tie-break is a stable
plugin/path sort and whichever loses is reported on stdout.

### Hooks

```bash
./install.sh --hooks        # macOS / Linux
.\install.ps1 -Hooks        # Windows
```

This configures Claude Code sound hooks in `~/.claude/settings.json`. The per-OS
sound table lives in `install-hooks.json` and is read by both installers, so they
cannot drift; each keeps its own small writer, which is why the PowerShell one
needs no Python. A sound file missing on your machine is reported and its hook
stays silent.

### Update

```bash
cd Tools
git pull
```

## Skill Development Validation

When adding or changing a skill, treat implementation and validation as two
separate steps:

1. Develop or revise the skill.
2. Test the skill by calling a subagent with a fresh context and explicitly
   instructing that subagent to invoke the new or revised skill against a
   realistic task.
3. Confirm that the subagent selected and used the skill as expected, followed
   the skill instructions, and produced the intended result before committing or
   publishing the change.

This fresh-context subagent check is required because it tests the skill from
the point of view of a new agent that has not seen the development discussion.
The standard workflow is: develop the skill, then test the skill.

## License

MIT
