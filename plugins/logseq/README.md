# LogSeq Skills

[Agent Skills](https://agentskills.io/specification) for working with [LogSeq](https://logseq.com/) graphs. Provides Claude with comprehensive knowledge of LogSeq's block-based markdown, Datalog query language, template system, and whiteboard format.

## Skills

| Skill | Description |
|-------|-------------|
| [logseq-markdown](skills/logseq-markdown/SKILL.md) | Block-based markdown with properties, wikilinks, block references, embeds, tasks, and namespaces |
| [logseq-queries](skills/logseq-queries/SKILL.md) | Simple queries and advanced Datalog queries for filtering, searching, and aggregating graph data |
| [logseq-templates](skills/logseq-templates/SKILL.md) | Templates with dynamic variables for reusable block structures |
| [logseq-whiteboards](skills/logseq-whiteboards/SKILL.md) | Whiteboard .edn files with shapes, connectors, portals, and embeds on an infinite canvas |
| [logseq-cc-records](skills/logseq-cc-records/SKILL.md) | Log Claude Code conversations to today's LogSeq journal with time-stamped summaries |

## Installation

### Claude Code (via marketplace)

```
/plugin marketplace add logseq-skills
/plugin install logseq@logseq-skills
```

### Claude Code (manual)

Copy the `skills/` directory and `.claude-plugin/` to your project's `.claude/` folder, or to `~/.claude/` for global access.

### OpenClaw (global install, recommended)

OpenClaw loads skills from `~/.openclaw/skills` (managed/global) and `<workspace>/skills` (workspace-specific).

**Symlink install (auto-updates when you `git pull` this repo):**

```bash
mkdir -p ~/.openclaw/skills
ln -s /path/to/logseq-skills/skills/logseq-markdown   ~/.openclaw/skills/logseq-markdown
ln -s /path/to/logseq-skills/skills/logseq-queries    ~/.openclaw/skills/logseq-queries
ln -s /path/to/logseq-skills/skills/logseq-templates  ~/.openclaw/skills/logseq-templates
ln -s /path/to/logseq-skills/skills/logseq-whiteboards ~/.openclaw/skills/logseq-whiteboards
ln -s /path/to/logseq-skills/skills/logseq-cc-records ~/.openclaw/skills/logseq-cc-records

openclaw skills list
openclaw skills check
```

Tip: for `logseq-cc-records`, set `LOGSEQ_GRAPH_DIR` to your graph folder so the logger writes to the right `journals/`.

## License

MIT
