---
name: obsidian-note
description: "Vault intake router — add free-form chat content to the right note. Triage it through a 3-step pipeline: (1) quick-capture a timestamped line to today's daily note (0-DIARY-SPACE/YYYY-MM/YYYY-MM-DD.md), (2) archive any raw materials (pasted emails, long dumps, transcripts) to _WorkSpace, (3) write a clean structured note into the correct SPACE (people, meeting, project, paper, etc.). Generates everything, then presents a summary for the user to actively review. Use when the user says /obsidian-note, 'note this', 'add this to my notes', 'log and file this', 'intake this', or dumps content they want captured and routed. Trigger: obsidian-note, note this, add to notes, intake, log and file, capture this, route this note."
argument-hint: "[free-form content to capture and route]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: 1.1.0
  last_updated: 2026-07-01
  summary: Chat-in → today's daily note (quick captures) + raw archive + filed note across vault's SPACE folders, then user reviews. Simplified workflow (single daily note, no separate scratchpad).
created: 2026-06-27T23:52
updated: 2026-07-01T10:20
---

Skill: obsidian-note (vault intake router)

# Purpose

The user dumps content into chat. This skill captures it without friction and
routes it to the right home, then hands control back for the user to review.
The user is the reviewer — never assume the generated note is final.

# Operating mode: GENERATE → then REVIEW

Run the full pipeline in one pass, then show a compact summary of everything
created and invite edits. Do NOT stop mid-pipeline to ask routing questions
unless the destination is genuinely ambiguous (see Step 3).

# Pipeline (every invocation)

## Step 0 — Resolve dates
```bash
date +%Y-%m-%d   # today, e.g. 2026-06-27  → used in filenames & log lines
date +%Y-%m      # month folder, e.g. 2026-06
date +%H:%M      # timestamp for the diary line
```

## Step 1 — 📔 Brief diary log (ALWAYS) — TIME-ORDERED + TAGGED
Append ONE short timestamped line to today's diary note, kept in chronological
order under a single `## Log (chronological)` section.
- Path: `0-DIARY-SPACE/<YYYY-MM>/<YYYY-MM-DD>.md`
- If the file/folder doesn't exist, create it with frontmatter
  (`created`, `updated`, `tags`) and an `# Outline (<date>)` header,
  matching existing diary notes.
- Ensure a `## Log (chronological)` section exists; if not, add it.
- INSERT the new line in time order (by `HH:MM`), not blindly at the end —
  earliest at top, latest at bottom. Bold the time so the timeline scans fast:
  `- **HH:MM** — <one-sentence gist>. → [[<filed note name>]] #<type> #<topic>`
- Always end the line with inline tags so entries are filterable, e.g.
  `#meeting`, `#person`, `#session`, `#idea`, `#vault-maintenance`, plus a
  topic tag when useful.
- Also MERGE those tags into the note's frontmatter `tags:` list (dedup), so
  the day is discoverable both inline and via properties.
- Keep the line brief. The diary is a time-ordered index, not the content.

## Step 2 — 📎 Raw materials → _WorkSpace (IF ANY)
If the input contains raw/verbatim material worth preserving unedited
(pasted email threads, meeting transcripts, long quotes, logs, audio refs):
- Write it VERBATIM to a raw archive file, frontmatter `type: *-raw`.
- Destination by kind:
  - Email/meeting transcript → `1-MEETING-SPACE/Emails/` or `1-MEETING-SPACE/`
  - Generic dump / attachment-like text → `_WorkSpace/AssetStore/` (or a
    topic subfolder)
  - Binary attachments the user pasted go to `_WorkSpace/AssetStore/_Inbox/`
    automatically via Obsidian; reference them, don't recreate them.
- Name: `<YYYY-MM-DD>-<slug>-RAW.md`.
- If there is no raw material, SKIP this step (most quick notes skip it).

## Step 3 — 🗂️ Clean note → correct SPACE
Write a clean, structured note into the matching SPACE. Routing map:

| Content is about…              | Destination SPACE              | Tag                 |
|--------------------------------|--------------------------------|---------------------|
| A person                       | `1-PEOPLE-SPACE/`              | `#person`           |
| A meeting / seminar            | `1-MEETING-SPACE/`            | `#meeting`          |
| An email thread                | `1-MEETING-SPACE/Emails/`     | `#email`            |
| Research IT / infra / access   | `1-RESEARCHIT-SPACE/`         | `#researchit`       |
| A project                      | `A-PROJECT-SPACE/`            | `#project`          |
| A paper                        | `B-PAPER-SPACE/`             | `#paper`            |
| Literature / reading notes     | `C-LITERATURE-SPACE/`        | `#literature`       |
| Theory / idea / thinking       | `C-THEORY-SPACE/`           | `#idea`             |
| Language learning              | `B-LANGUAGE-SPACE/`         | `#language`         |
| Work / CC / setup session      | `1-RESEARCHIT-SPACE/` (flag)  | `#session`          |
| Unclear                        | Ask the user, OR diary-only   | `#inbox`            |

The Tag in this row is the canonical tag for that content type — use it on
the diary line AND in the filed note's frontmatter, so the diary timeline and
each SPACE stay in sync. Add a topic tag (e.g. `#cgm`, `#gordon`) when useful.

- Note frontmatter: `type`, `created`, `updated`, `tags`, plus type-specific
  fields (e.g. people: `name`, `title`, `introduced-by`).
- Use a clear `# Title`, an Overview/summary, and section scaffolding.
- Keep it concise; placeholders (`_To be filled in._`) are fine — the user
  will review and expand.
- If routing is ambiguous, make your best guess, file it, and FLAG the guess
  in the review summary so the user can move it.

## Step 4 — 🔗 Cross-link the three artifacts
Wire them together so navigation works:
- Diary line → links to the filed note.
- Filed note → links to the raw archive (if any) and back to the diary date.
- Raw archive → links to the filed note (its curated view).
This is the proven "summary + raw + pointer" pattern.

## Step 5 — ✅ Review handoff
Present a compact summary table of what was created/updated:
`| artifact | path | action |`
Then explicitly invite the user to review, edit, re-route, or discard.
End your turn — do not auto-finalize.

# Tag vocabulary (canonical — keep tags consistent)
Use exactly these type tags so diary filters and SPACE queries stay reliable.
Always apply ONE type tag; add topic tags freely.

- Type tags (one per entry): `#person` · `#meeting` · `#email` · `#researchit`
  · `#project` · `#paper` · `#literature` · `#idea` · `#language`
  · `#session` · `#inbox` (unrouted)
- Cross-cutting tags (optional, stack as needed): `#vault-maintenance`
  (setup/reorg), `#todo` (has open action items), `#followup`.
- Topic tags (free-form, lowercase, hyphenated): e.g. `#cgm`, `#dikw`,
  `#gordon`, `#haipipe` — name the subject so a topic timeline emerges.
- Do NOT invent new TYPE tags; if none fit, use `#inbox` and flag for review.

# Conventions
- Vault paths are RELATIVE from vault root; never use absolute paths or a
  leading slash.
- Reference notes in chat as clickable `[[wikilinks]]`.
- Match the date/frontmatter style of existing notes in the target SPACE.
- Wikilinks resolve by filename — keep note names unique.
- Never overwrite an existing note; if a same-named note exists, append or
  ask.

# Examples of intent
- "note: met Julia Wolfson, PhD MPP, intro'd by Dr Park" → person note in
  PEOPLE-SPACE + diary line.
- "intake this email thread <paste>" → RAW archive in Emails/ + curated
  summary + pointer + diary line.
- "log this idea about HTE personalization ceilings" → theory note in
  C-THEORY-SPACE + diary line (no raw step).
