# Tools

Personal [Claude Code](https://claude.ai/code) skill plugins for productivity, academic research, and knowledge management.

## Plugins

| Plugin | Skills | Description |
|--------|--------|-------------|
| **[logseq](plugins/logseq/)** | logseq-markdown, logseq-queries, logseq-templates, logseq-whiteboards, logseq-cc-records | Work with LogSeq graphs |
| **[research](plugins/research/)** | coding-by-logging, evaluation-display-skill, notebook-cell-python, paper-incubator | Academic research workflows |
| **[chronicle](plugins/chronicle/)** | chronicle-email | Index emails from MS365 Outlook |

## Installation

### Quick Setup (marketplace)

```bash
git clone --recursive git@github.com:jluo41/Tools.git
cd Tools
./install.sh
```

Then in Claude Code:
```
/plugin install logseq@jluo41-tools
/plugin install research@jluo41-tools
/plugin install chronicle@jluo41-tools
```

### Global Install (all skills available everywhere)

```bash
./install.sh --global
```

This symlinks all skills to `~/.claude/skills/` so they're available in every Claude Code session.

### Update

```bash
cd Tools
git pull --recurse-submodules
```

## License

MIT
