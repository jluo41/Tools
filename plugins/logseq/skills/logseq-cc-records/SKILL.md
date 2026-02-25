---
name: logseq-cc-records
description: Log the current Claude Code conversation to today's LogSeq journal with a time-stamped summary. Use when the user wants to record, log, or save the current session to LogSeq, or when they say /logseq-cc-records.
---

# LogSeq CC Records

Log the current Claude Code / OpenClaw work session to today's LogSeq journal with a time-stamped, concise summary.

**Method**: Direct markdown file editing (more reliable than MCP for nested structure)

**Location (configurable)**
- Set `LOGSEQ_GRAPH_DIR` to your LogSeq graph folder (the one that contains `journals/`, `pages/`, `logseq/`).
- Journals path: `$LOGSEQ_GRAPH_DIR/journals/`

**Example (OpenClaw + jluo41-repo default)**
- `LOGSEQ_GRAPH_DIR=/home/jluo41/.openclaw/workspace/jluo41-repo/3-Chronile/LogSeq-Me`

## Entry Format

All entries are written under the `[[CC-Veritable-Records]]` section with **time prefix, topic as main bullet, description as child block**:

```markdown
- [[CC-Veritable-Records]]
	- 14:30 LogSeq Skills Plugin Creation #ClaudeCode #LogSeq
		- Built 4-skill plugin: markdown, queries, templates, whiteboards.
```

**Note**: Entries use plain bullets (no DONE/TODO) to avoid strikethrough in LogSeq.

## Example Output

**First entry of the day** (creates section):
```markdown
- [[CC-Veritable-Records]]
	- 09:15 Paper Analysis - PNAS Submission #Research #Paper
		- Reviewed methodology section, updated figures, fixed citations.
```

**Subsequent entries** (appends under existing section):
```markdown
	- 14:30 LogSeq Skills Plugin Creation #ClaudeCode #LogSeq
		- Built 4-skill plugin: markdown, queries, templates, whiteboards.
	- 16:45 DIKW Agent Routing Fix #Code #DIKW-Agent
		- Fixed routing logic for oneway mode, updated test prompts.
```

## Writing Style Guidelines

**Keep descriptions simple and scannable:**
- Max 10-15 words
- Use active verbs (built, tested, fixed, added, updated)
- Drop unnecessary words (articles, conjunctions when possible)
- Use abbreviations naturally (MCP, auth, config)
- Focus on outcome, not process
- Avoid: "Successfully configured...", "In order to..."
- Avoid: Long compound sentences with multiple clauses

## Implementation Steps

1. Get today's date in YYYY_MM_DD format (LogSeq uses underscores in filenames)
2. Get current time in HH:MM format (24-hour)
3. Resolve journal path: `$LOGSEQ_GRAPH_DIR/journals/{date}.md`
   - If `LOGSEQ_GRAPH_DIR` is not set, fall back to `~/Desktop/LogSeq-Me` (legacy default).
4. **Check if `[[CC-Veritable-Records]]` section exists** in the file
5. Analyze the conversation context to identify:
   - Main topic/project
   - Key activities or outcomes
   - Relevant tags based on topics discussed
6. Generate the summary entry with time, topic, and one-sentence description (max 10-15 words)
7. **Edit the markdown file directly** using proper LogSeq format:

   **If section EXISTS** - Find the section and append entry with TAB indentation:
   ```markdown
   	- HH:MM [Topic] #tags
   		- [Short description]
   ```

   **If section DOES NOT exist** - Add new section at end of file:
   ```markdown
   - [[CC-Veritable-Records]]
   	- HH:MM [Topic] #tags
   		- [Short description]
   ```

   **CRITICAL**: Use TABS (not spaces) for indentation in LogSeq markdown files

8. LogSeq will auto-sync the file changes
9. Confirm to user that entry was logged successfully

## Error Handling

- If today's journal file doesn't exist yet, create it with the entry
- If no clear topic emerges, ask user for clarification before logging

## Tags Strategy

Automatically add relevant tags based on conversation content:
- Projects: #DrFirst, #MedStar, #DIKW-Agent, #PD2D
- Tools: #ClaudeCode, #LogSeq, #Python, #LaTeX
- Activities: #Research, #Code, #Paper, #Meeting
- General: #TODO, #Done, #InProgress
