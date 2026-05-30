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
marketplace. If the parent workspace has a `.claude/` directory, it also
symlinks the skills into that workspace.

### Project Install

```bash
./install.sh --project /path/to/workspace
```

This symlinks every discovered skill into `/path/to/workspace/.claude/skills/`.
Skill discovery is recursive, so deeply nested skills such as
`haipipe-toolkit/skills/F_paper/4-write/paper-write` are included.

### Global Install

```bash
./install.sh --global
```

This symlinks all skills to `~/.claude/skills/` so they are available in every
Claude Code session.

Duplicate skill names are resolved deterministically because one skills
directory cannot contain two symlinks with the same basename. The installer
prefers standalone diagram skills over haipipe utility mirrors and active paper
skills over `_paper-writing-backup` snapshots.

### Hooks

```bash
./install.sh --hooks
```

This configures Claude Code sound hooks in `~/.claude/settings.json`.

### Update

```bash
cd Tools
git pull
```

## License

MIT
