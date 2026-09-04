---
name: note
description: "The single human-facing vault intake command. Use /note for anything the user wants saved to Obsidian: quick notes, todos, meetings, emails, decisions, people updates, project/matter updates, timelines, and raw pasted material. Routes one input into the readable three-ledger system: daily chronology (通鉴体), people notes (纪传体), and project/matter notes (纪事本末), with optional event artifacts and raw archives. Prefer this over lower-level Obsidian/chronicle skills unless the user explicitly asks for a tool-specific operation. Trigger: /note, note, note this, add to notes, remember this, log this, capture this, intake this."
argument-hint: "[free-form content to capture and route]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: 1.2.0
  last_updated: 2026-07-08
created: 2026-06-27T23:52
updated: 2026-07-08T00:00
---

Skill: note (single vault intake router)

# Purpose

The user dumps content into chat. This skill captures it without friction and
routes it to the right home, then hands control back for the user to review.
The user is the reviewer — never assume the generated note is final.

This is the default and preferred entry point for writing into Obsidian. The
user should not need to remember a menu of specialized note skills. Lower-level
Chronicle/Obsidian skills are implementation details unless the user asks for
a specific tool operation such as querying Bases, formatting markdown, or
recording audio.

The vault is maintained as three cross-checking ledgers:
- Chronological / 通鉴体: today's diary note records when the thing happened.
- Biographical / 纪传体: people notes record the human-centered history.
- Project-centered / 纪事本末: project/matter notes record how one matter
  develops from beginning to end.

One user input should therefore create one canonical intake and write pointers
to every ledger that applies. Do not duplicate long content across all three;
write a short index line in the diary, append or create concise context in the
person note when people are involved, and put the matter narrative/details in
the project note when there is a bounded project or issue.

Each ledger may also carry its own timeline view:
- Daily timeline: one-day chronological sequence.
- Person timeline: the user's history with a person over months/years.
- Project timeline: the internal history of one project/matter from start to
  finish.
Timeline views are summaries and navigation aids, not the only source of truth.

# Readability-first rule

Everything generated for the vault must be easy for the user to scan later.
Machine-queryable metadata is secondary to human readability.

- Prefer short sections with obvious headings over dense paragraphs.
- Put the action or decision first; context comes after.
- Keep diary lines, timeline items, and task text short enough to understand at
  a glance.
- Avoid stuffing long tag chains, bracket metadata, or repeated links into the
  visible text. Use only the tags/links that materially help retrieval.
- If a note needs structured fields, put them in frontmatter or a compact
  "Details" section, not inside every sentence.
- Generated notes should look useful in plain Markdown, even without plugins.

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
  `- **HH:MM** — <one-sentence gist>. → [[<person note if any>]] · [[<project/matter note>]] #<type> #<topic>`
- Always end the line with inline tags so entries are filterable, e.g.
  `#meeting`, `#person`, `#session`, `#idea`, `#vault-maintenance`, plus a
  topic tag when useful.
- Also MERGE those tags into the note's frontmatter `tags:` list (dedup), so
  the day is discoverable both inline and via properties.
- Keep the line brief. The diary is a time-ordered index, not the content.
- Preserve readability: one diary line should usually fit on one screen line
  in Obsidian. If it needs explanation, put the explanation in the project or
  event artifact and link to it.

## Step 2 — 📎 Raw materials → _WorkSpace (IF ANY)
If the input contains raw/verbatim material worth preserving unedited
(pasted email threads, meeting transcripts, long quotes, logs, audio refs):
- Write it VERBATIM to a raw archive file, frontmatter `type: *-raw`.
- Destination by kind:
  - Email/meeting transcript → `1-EVENT-SPACE/Emails/` or `1-EVENT-SPACE/Meeting/`
  - Generic dump / attachment-like text → `_WorkSpace/AssetStore/` (or a
    topic subfolder)
  - Binary attachments the user pasted go to `_WorkSpace/AssetStore/_Inbox/`
    automatically via Obsidian; reference them, don't recreate them.
- Name: `<YYYY-MM-DD>-<slug>-RAW.md`.
- If there is no raw material, SKIP this step (most quick notes skip it).

## Step 3 — 🧑 Person note (纪传体 / WHEN PEOPLE APPLY)
If the input involves a specific person, pick or create that person's note in
`1-PEOPLE-SPACE/`. This is the "who is involved?" home. If the note already
exists, append a dated `## YYYY-MM-DD` or `### YYYY-MM-DD HH:MM` entry instead
of creating a duplicate.

Only people belong to 纪传体. Projects, papers, theories, emails, and meetings
should not be treated as 纪传体, though they may be linked from a person's
timeline.

## Step 4 — 🗂️ Project/matter note (纪事本末 / project ledger)
Pick or create the project/matter note for the main ongoing thing. This is the
"what matter is unfolding?" home. A project/matter can be a formal project,
paper, proposal, meeting thread, email thread, decision, incident, milestone,
or research/work issue that may develop over time.

| Content is about…              | Destination SPACE              | Tag                 |
|--------------------------------|--------------------------------|---------------------|
| Research IT / infra / access   | `1-RESEARCHIT-SPACE/`         | `#researchit`       |
| A project                      | `A-PROJECT-SPACE/`            | `#project`          |
| A paper                        | `B-PAPER-SPACE/`             | `#paper`            |
| Literature / reading notes     | `C-LITERATURE-SPACE/`        | `#literature`       |
| Theory / idea / thinking       | `C-THEORY-SPACE/`           | `#idea`             |
| Language learning              | `C-LANGUAGE-SPACE/`         | `#language`         |
| Work / CC / setup session      | `1-RESEARCHIT-SPACE/` (flag)  | `#session`          |
| Unclear                        | Ask the user, OR diary-only   | `#inbox`            |

The Tag in this row is the canonical tag for that matter type — use it on the
diary line AND in the filed note's frontmatter, so the diary timeline and each
SPACE stay in sync. If a person note is updated, also use `#person` there. Add
a topic tag (e.g. `#cgm`, `#gordon`) when useful.

- Project/matter note frontmatter: `type`, `created`, `updated`, `tags`, plus
  type-specific fields (e.g. project status, owner, related people, deadline).
- Use a clear `# Title`, an Overview/summary, and section scaffolding.
- Keep it concise; placeholders (`_To be filled in._`) are fine — the user
  will review and expand.
- If routing is ambiguous, make your best guess, file it, and FLAG the guess
  in the review summary so the user can move it.

## Step 5 — 🧾 Event artifact (WHEN APPLICABLE)
Create or update a concrete event artifact if the input is about an episode:
meeting, email thread, call, decision, milestone, deadline, incident, travel,
or transaction.

Event destinations:
- Meeting / seminar / call → `1-EVENT-SPACE/Meeting/`
- Email thread → `1-EVENT-SPACE/Emails/`
- Other event-like matter → `1-EVENT-SPACE/`

Event artifact responsibilities:
- State what happened, when, who/what was involved, decisions, open loops, and
  next actions.
- Link to the project/matter note, people notes, diary date, and raw archive if
  any.
- If an existing event artifact clearly matches, append a dated update instead of
  creating a duplicate.
- Maintain a `## Timeline` section when the event has more than one dated
  step, or when the new entry is likely to be followed up. Each timeline item
  should be one concise dated point with links back to project/person notes and
  raw material where relevant. If the event is part of a broader project, also
  mirror the timeline point into the project/matter note's `## Timeline`.
- If there is no coherent event, skip this step and say "event artifact: skipped"
  in the review summary.

## Step 6 — 🕰️ Timeline views (optional but preferred)
After diary + person + project/event routing, update timeline views where they
add real retrieval value.

Timeline destinations:
- Daily note: `## Timeline` for that day's sequence, especially if there are
  multiple substantial entries.
- Person note: `## Timeline` for interactions with that person over time.
- Project/matter note: `## Timeline` for milestones and major decisions from
  beginning to end.
- Event artifact: `## Timeline` only when that specific event itself has
  multiple dated steps.

Timeline format:
- Use ordinary Markdown bullets by default for portability:
  `- YYYY-MM-DD HH:MM — <short event>. → [[linked note]]`
- If the vault has the Timelines plugin available and the note already uses
  `timeline-labeled`, preserve that style and append compatible entries.
- Keep timeline items short. Link to the project note, person note, diary date,
  or raw archive for details instead of duplicating content.
- Do not create a timeline section for a one-off note unless it is likely to
  become a recurring thread.

## Step 7 — ✅ Tasks and daily todos (readability-first)
Tasks should be written for fast human review first, plugin queries second.
Prefer a small visible Today list over a large undifferentiated task dump.

Daily note task sections:
- `## Today` — 3-7 concrete tasks the user may actually do today.
- `## Waiting` — blocked/waiting-for tasks.
- `## Captured` — raw inbox tasks that still need routing.

Task style:
- Use one short action per checkbox:
  `- [ ] <verb + object> 📅 YYYY-MM-DD #task #topic`
- Start with an action verb: `Email`, `Draft`, `Review`, `Schedule`, `Submit`,
  `Ask`, `Fix`, `Read`, `Decide`.
- Link once at the end if useful: `→ [[Project or person]]`.
- Avoid vague nouns as tasks. Do not write `proposal`; write
  `Draft proposal timeline section`.
- Avoid over-tagging. Use `#task` plus at most 1-2 useful topic/status tags.
- If a task belongs to a project/matter, the project/matter note is the source
  of truth; Daily may duplicate only today's execution copy or show it via a
  query/dashboard.

Task blocks:
- A todo may be a block, not just a one-line checkbox. The checkbox is the
  visible handle; indented child bullets hold details.
- Use task blocks when the action needs context, criteria, notes, or links.
- Keep the first line short and actionable so Daily stays scannable.
- Put detailed context under the task, indented beneath it.
- Use a block id when the task should be referenced from Daily, a person note,
  or another project note: `^task-YYYYMMDD-short-slug`.
- The project/matter note should hold the full task block. Daily may include
  either a short duplicate execution line or a block reference/link back to the
  project task.

Readable task block example:
```md
- [ ] Draft proposal timeline section 📅 2026-07-09 #task #proposal → [[Proposal Defense]] ^task-20260709-proposal-timeline
  - Why: Need a clear sequence from data access to validation to submission.
  - Done when: one-page timeline draft is ready for Gordon review.
  - Related: [[Gordon Gao]], [[Insulin CDS Validation]]
  - Notes:
    - Keep the timeline readable; do not turn it into a database dump.
```

Daily projection of that task:
```md
## Today
- [ ] Draft proposal timeline section → [[Proposal Defense#^task-20260709-proposal-timeline]]
```

Readable daily example:
```md
## Today
- [ ] Email Gordon about proposal timeline 📅 2026-07-08 #task #proposal → [[Gordon Gao]]
- [ ] Draft Obsidian intake task rules 📅 2026-07-08 #task #obsidian → [[Obsidian note intake system]]

## Waiting
- [ ] Waiting for Azure approval ⏳ 2026-07-10 #task #waiting → [[JHU Research IT]]

## Captured
- [ ] Turn timeline plugin idea into project note #task #inbox
```

## Step 8 — 🔗 Cross-link the ledgers and raw artifact
Wire them together so navigation works:
- Diary line → links to person note(s) if any and the project/matter note.
- Person note → links back to the diary date and project/matter note.
- Project/matter note → links to the diary date, people notes, event artifacts,
  and raw archive if any.
- Event artifact → links to the project/matter note, people notes, diary date,
  and raw archive if any.
- Raw archive → links to the project/matter or event artifact that curates it.
This is the "one intake, three ledgers, raw source optional" pattern.

## Step 9 — ✅ Review handoff
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
  `#gordon`, `#haipipe` — name the person/project/topic so timelines emerge.
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
  PEOPLE-SPACE + diary line; create an event artifact only if there was a
  meeting or bounded interaction worth tracking.
- "intake this email thread <paste>" → RAW archive in
  `1-EVENT-SPACE/Emails/` + event artifact + relevant project/person note
  updates + diary line.
- "log this idea about HTE personalization ceilings" → theory note in
  C-THEORY-SPACE as a project/matter-style note + diary line; event artifact
  skipped unless tied to a meeting, decision, or milestone.
