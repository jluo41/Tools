---
name: obsidian-cc-session
description: Write a concise summary of the current Claude Code session to today's Obsidian daily note (~/Documents/Obsidian Vault/0-Diary/YYYY-MM-DD.md) as a timestamped heading + bullet summary + one ASCII diagram. Use when the user says "log this session", "/obsidian-cc-session", or wants to record this conversation in Obsidian.
---

# obsidian-cc-session

Append a concise summary of the current Claude Code session to today's Obsidian daily note. Each entry is one timestamped heading (with a wikilink topic), one aphoristic headline, 2-4 concrete bullets, and one ASCII diagram.

## Where to write

`~/Documents/Obsidian Vault/0-Diary/YYYY-MM-DD.md`

- Create the file if missing.
- Append to the end if it exists.
- **Never edit content already in the file.**

## Scope — what counts as "this session"

Default: the most recent coherent unit of work in the conversation.

User can scope explicitly:
- `/obsidian-cc-session` — default (recent unit of work)
- `/obsidian-cc-session full` — entire session
- `/obsidian-cc-session last 3` — last N exchanges
- `summarize the recent discussion of <topic>` — only threads about that topic, ignore unrelated tangents

When in doubt, prefer narrower scope and ask the user what to include before drafting.

## Entry format

```
## YYYY-MM-DD HH-MM — [[<TopicWikilink>]] <optional 1-3 word descriptor>
> *<one aphoristic headline — punchy, memorable, would survive as a standalone quote>*

- <concrete bullet: name files, paths, decisions, values — not just verbs>
- <key decision with the reason>
- <output or artifact: path, name, count>
- <next step or open question>

​```text
<one ASCII diagram summarizing the session>
​```
```

Heading time format is `YYYY-MM-DD HH-MM` (24h local, hyphen between hour and minute).

**Title wikilink is required** — it's the backlink target. Open `[[<Topic>]]` in Obsidian later and every diary that touched it shows up. Stub pages (link target doesn't exist yet) are fine; the wikilink itself is the index.

**Headline is one sentence, italicized blockquote** (`> *...*`). Aphoristic — should read well in isolation, like a quote on a card. If you can't write one, the session probably isn't worth logging.

## Diagram — pick ONE primitive

Choose whichever fits the session best:

| Primitive | Use for |
|---|---|
| annotated folder tree | what shipped (file/folder changes) |
| pipeline (left→right or top↓) | a flow or step sequence |
| decision table | "we picked X over Y" |
| side-by-side comparison | X vs Y framing |
| single boxed callout | takeaway-only entry |

Rules:
- ≤ 12 lines of diagram.
- Heavy emoji where they help (✅ ⏳ 🔑 ❌).
- One diagram per entry — no bullet-only entries.

## Steps

1. Get today's date + current time (24h local) → format `YYYY-MM-DD HH-MM`. Use `date "+%Y-%m-%d %H-%M"`.
2. Resolve path: `~/Documents/Obsidian Vault/0-Diary/<date>.md`.
3. Draft the entry: heading (with `[[Topic]]` wikilink) + headline blockquote + 2-4 concrete bullets + one fenced diagram block.
4. **Show the draft to the user for ✅ before writing.**
5. On confirm, append `\n\n` + the block to the file (Edit if the file exists, Write if not).
6. Confirm with the file path.

## Style

- English default; quote the user verbatim if they spoke another language.
- Bullets: 1-2 sentences, ≤ 25 words each. **Concrete > abstract** — name files, paths, decisions, values. Drop weak bullets — better 3 strong than 5 vague.
- Wikilinks: title topic is **always** a wikilink (backlink target — stubs OK). Body wikilinks only for notes that exist or topics worth aggregating across diaries.
- Headline: one aphoristic sentence right after the heading. Memorable in isolation. If you can't write one, the session probably isn't worth logging.
- Skip the whole entry if the session was trivial.

## What this skill does NOT do

- ❌ Edit anything already in the daily note
- ❌ Read transcripts (the conversation is in your context already)
- ❌ Sync to git (Obsidian handles sync)
- ❌ Build canvases or roll up sessions
