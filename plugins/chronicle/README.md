# Chronicle Skills

[Agent Skills](https://agentskills.io/specification) for chronicling and indexing emails from MS365 Outlook. Provides Claude with the ability to automatically organize emails into structured monthly markdown indexes with reimbursement tracking.

## Skills

| Skill | Description |
|-------|-------------|
| [chronicle-email](skills/chronicle-email/SKILL.md) | Index emails from MS365 Outlook into organized monthly markdown files with daily sections and reimbursement tracking |

## Installation

### Claude Code (via marketplace)

```
/plugin marketplace add chronicle-skills
/plugin install chronicle@chronicle-skills
```

### Claude Code (manual)

Copy the `skills/` directory and `.claude-plugin/` to your project's `.claude/` folder, or to `~/.claude/` for global access.

## Prerequisites

- **MS365 MCP Server**: Requires MS365 MCP integration for Outlook access
- **Email Account**: Configured access to junjieluo.jhu@outlook.com
- **Folder Structure**: Emails organized in `jluo41-{YEAR}/{YEAR}_{MONTH}` format

## Usage

```
/chronicle-email 2026-01
```

Or simply:
```
Chronicle emails for January 2026
```

Claude will:
1. Connect to MS365 Outlook
2. Retrieve all emails from the specified month
3. Organize them into daily sections
4. Identify and mark reimbursement-related emails
5. Generate a structured markdown index at `3-Chronile/Emails/MonthIndex/`

## Output Format

Each monthly index includes:
- **Total email count** and coverage period
- **Pre-month section** for older threads
- **Daily sections** organized by date
- **Reimbursement markers** (**[$]**) for expense-related emails
- **Expense summary** table at the end

Example: `3-Chronile/Emails/MonthIndex/2026-01-index.md`

## License

MIT
