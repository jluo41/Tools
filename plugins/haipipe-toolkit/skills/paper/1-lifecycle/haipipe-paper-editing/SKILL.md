---
name: haipipe-paper-editing
description: "Per-section editing scaffolds under 0-lifecycle/5-editing/. Each section gets a folder with an outline-narrative .md (paragraph headlines + previews + narrative sentences) and a _LOG changelog. Replaces minimap as the final lifecycle stage before prose writing. Monitors user inline comments (> JL: ...), addresses them in outline + tex, and logs changes with conversation context. Trigger: editing, section scaffold, outline narrative, edit section, 5-editing, /haipipe-paper-editing."
argument-hint: "[section-name-or-number] [paper-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Agent
metadata:
  version: "1.1.0"
  last_updated: "2026-06-26"
  summary: "Per-section editing scaffolds (outline-narrative + changelog) under 0-lifecycle/5-editing/. Subagent verbs: lesson, digest, feedback."
  changelog:
    - "1.1.0 (2026-06-26): added lesson/digest/feedback subagent verbs; these dispatch to background Agent, never run inline."
    - "1.0.0 (2026-06-26): created from live MISQ literature editing session."
---

Skill: haipipe-paper-editing
=============================

Per-section editing scaffolds that bridge lifecycle planning and prose
writing. Each section the user wants to work on gets a folder under
`0-lifecycle/5-editing/` with two files: an outline-narrative and a
changelog. This replaces minimap as the final lifecycle stage.

```
/haipipe-paper-editing                          -> dashboard (list sections, show status)
/haipipe-paper-editing <section>                -> open or create scaffold for that section
/haipipe-paper-editing log <section>            -> show recent changelog entries
/haipipe-paper-editing lesson [section]         -> SUBAGENT: harvest what we learned (venue norms, structural decisions, exemplar patterns)
/haipipe-paper-editing digest [section]         -> SUBAGENT: summarize session changes into the _LOG
/haipipe-paper-editing feedback [section]       -> SUBAGENT: capture corrections and preferences as memory files
```

## Folder structure

```
0-lifecycle/5-editing/
  1-introduction/
    1-introduction.md              outline-narrative
    _LOG_1-introduction.md         changelog
  2-literature/
    2-literature.md                outline-narrative
    _LOG_2-literature.md           changelog
  3-theory/
    3-theory.md                    outline-narrative
    _LOG_3-theory.md               changelog
  ...
```

Each folder is one section that the user wants to treat as a unit.
The numbering and naming are flexible per the user's choice.

## Outline-narrative file

The outline-narrative is the working document for one section, at the **paragraph level**. Each paragraph is a unit with its own job.

The file starts with a **structure overview** block at the top, showing all subsections and paragraphs with sentence counts at a glance. This is the first thing you see when opening the file.

```markdown
# Section N: Title — Structure

\```
§N.1 Subsection Title (K ¶)
  P1. Short paragraph job description                        N sentences
  P2. Short paragraph job description                        N sentences

§N.2 Subsection Title (K ¶)
  P3. Short paragraph job description                        N sentences
  ...
\```

---

## §N.1 Subsection Title

### P1. What this paragraph does (one-line job description)

(Semicolon-separated preview of key points in this paragraph.)

Narrative sentence one.

Narrative sentence two.

### P2. What the next paragraph does

(Preview.)

Narrative sentence one.

...
```

Rules:
- **Structure overview at top**: `# Section N: Title — Structure` followed by a code block listing all subsections and paragraphs with sentence counts. Update this block whenever the structure changes.
- `##` for subsections within the section.
- `###` for each paragraph within a subsection.
- Each paragraph gets: headline (its job), parenthetical preview, narrative sentences.
- One narrative sentence per line (these become the paragraph sentences in tex, marked with `Pn.Sn`).
- Target 5-6 sentences per paragraph (MISQ/ISR norm from exemplar analysis).
- User adds inline comments as `> JL: comment text`.
- Agent addresses comments, then removes the `> JL:` line once resolved.

## _LOG changelog

Simple changelog, newest entry at top. Each entry:

```markdown
## YYYY-MM-DD #N ~HH:MM

JL (source): "user's comment verbatim"
- Change one.
- Change two.
```

Rules:
- Newest at top.
- Number entries sequentially within a date (#1, #2, ...).
- Add timestamp (~HH:MM) when available.
- Log JL's comments that triggered changes. Source = where the comment came from: `(outline L1)`, `(tex P3.S2)`, `(chat)`. Quote the comment.
- Bullet points for changes, as short as possible.
- No commentary, summaries, or "Context:" labels.

## Workflow

1. **Create scaffold**: when the user wants to edit a section, create the folder + two files. Populate the outline-narrative from the existing tex if one exists.
2. **Monitor comments**: read the outline-narrative for `> JL:` lines. These are the user's inline feedback.
3. **Address comments**: update the outline-narrative (and tex if syncing), then log the change with conversation context.
4. **Sync to tex**: when the user confirms, update the corresponding `0-sections/*.tex` to match the outline. The tex uses `Pn.Sn` markers per the manuscript convention.
5. **Compile**: run `./1-compile.sh` after tex changes.

## Subagent verbs: lesson, digest, feedback

These three verbs MUST dispatch to a background subagent via the Agent tool. They never run inline in the main session. The main thread stays focused on prose; the subagent reads files, harvests context, and writes outputs independently.

### lesson

Harvest what was learned during this editing session. The subagent reads:
- The outline-narrative and _LOG for the target section
- The venue pack (`_venue/playbook-*/`) if consulted
- Exemplar papers if referenced
- The conversation context (via the prompt)

It produces project-type memories about structural decisions, venue norms, or exemplar patterns that will be useful in future sessions. Example outputs: "MISQ papers don't use standalone Research Gap subsections (from exemplar analysis)" or "L2 should cover communication styles broadly, not just agreeableness definition."

Dispatch pattern:
```
Agent({
  description: "editing lesson harvest",
  prompt: "Read [section scaffold path] and [_LOG path]. Harvest structural decisions, venue norms, and exemplar patterns learned during this editing session. Save each as a project-type memory file under the memory directory. Do NOT save ephemeral task details or things derivable from the code.",
  run_in_background: true
})
```

### digest

Summarize the session's changes into the _LOG changelog. The subagent reads:
- The outline-narrative (current state)
- The corresponding tex file (current state)
- The _LOG (to avoid duplicating existing entries)
- The git diff for the section files

It appends a new _LOG entry with: what changed, what JL comments were addressed, what decisions were made, and what's next. Uses the _LOG format (date, numbered entry, bullet changes).

Dispatch pattern:
```
Agent({
  description: "editing digest to LOG",
  prompt: "Read [outline], [tex], [_LOG], and run git diff on both. Write a new _LOG entry summarizing changes since the last entry. Follow the _LOG format exactly. Do not duplicate existing entries.",
  run_in_background: true
})
```

### feedback

Capture corrections and preferences from this session as memory files. The subagent reads:
- The conversation context (via the prompt, which should include key corrections)
- Existing memory files (to avoid duplicates)

It produces feedback-type memories about how to approach future editing work. Example: "L2 should open with communication styles broadly, not jump straight to agreeableness definition" or "No standalone Research Gap subsection in MISQ; fold gap into last literature stream."

Dispatch pattern:
```
Agent({
  description: "editing feedback capture",
  prompt: "From this editing session, capture the following corrections/preferences as feedback-type memory files: [list the key corrections from the conversation]. Check existing memories first to avoid duplicates. Each memory gets its own file with frontmatter.",
  run_in_background: true
})
```

### Prompt construction for subagents

The caller (main session) MUST include concrete context in the Agent prompt because the subagent has no access to the conversation history. Include:
- File paths to read
- Key decisions or corrections made (summarized from conversation)
- The memory directory path (`/Users/jluo41/.claude/projects/.../memory/`)
- What NOT to save (ephemeral details, things already in the code)

## Relation to other skills

```
haipipe-paper-lifecycle (orchestrator)
  ├─► seed → pitch → claims → narrative → display
  └─► editing (this skill, replaces minimap as stage 5)
        └─► hands off to 3-write-edit/ skills for prose polishing
```

The lifecycle orchestrator routes `editing` to this skill.
The edit skills (haipipe-paper-edit-content, -weaving, -write, etc.)
handle prose-level work AFTER the section scaffold is settled.
