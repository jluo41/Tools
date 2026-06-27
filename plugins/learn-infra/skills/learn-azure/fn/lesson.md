---
name: learn-azure-lesson
description: "Utility verb. Captures a hard-won lesson about Azure/Databricks — a gotcha, pitfall, workaround, or 'wish I knew this before I started' — into the lesson/ folder as a numbered lesson file. Lessons are things the agent (and team) should be AWARE OF IN ADVANCE before touching Azure infrastructure. Unlike feedback (about the skill/wiki being wrong), a lesson is about the PLATFORM being surprising. `lesson list` shows all lessons; `lesson search <keyword>` finds relevant ones."
argument-hint: "[\"<what-happened-and-what-to-do>\"] | list | search <keyword>"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Lesson (capture hard-won knowledge, consult before acting)

Captures lessons learned the hard way about Azure and Databricks — things that
surprised us, cost us time, or would have saved hours if we'd known upfront.
These are about the PLATFORM being surprising, not about the wiki being wrong
(that's feedback). A lesson is a "don't touch the stove" note for future you.

The key contract: BEFORE executing Azure/Databricks infrastructure work, the
agent MUST scan the lesson/ folder for relevant lessons and flag any that apply.
Lessons are guardrails, not just history.

## Three verbs

### Capture: `/learn-azure lesson "<what-happened>"`

```
1. READ existing lessons in lesson/ to check for duplicates.
2. SAME-TOPIC test: does this lesson cover the same gotcha as an existing one?
   a. SAME TOPIC -> UPDATE the existing file:
      - add a "## Update YYYY-MM-DD" section with the new detail
      - do NOT overwrite prior content
   b. NEW TOPIC -> CREATE lesson/<NN>-YYMMDD-<short-slug>.md
      where NN = max existing number + 1, zero-padded to 2 digits,
      and YYMMDD is today's date (e.g. 260626).
3. WRITE the lesson using the schema below.
4. CONFIRM: show the file path and one-line summary.
```

### List: `/learn-azure lesson list`

```
Print all lessons, one line each:
  <NN> · <YYMMDD> · <title> · <when-to-apply one-liner>
Sorted by number.
```

### Search: `/learn-azure lesson search <keyword>`

```
Grep lesson/*.md for the keyword(s). Print matching lessons with the
relevant excerpt. Use this BEFORE infrastructure work to check for gotchas.
```

## Lesson file schema

```markdown
# Lesson NN: <Short Title>

## The Problem
<What happened — the surprise, the error, the silent failure.>

## The Symptom
<How you noticed — error message, silent data loss, unexpected behavior.>
<Optional — omit if the problem IS the symptom.>

## The Solution
<What to do instead. Code snippets, config, step-by-step.>

## Why It Works (or Why It Fails)
<The underlying reason — so the reader understands, not just follows.>

## When to Apply
<Conditions that trigger this lesson — region, VM type, pipeline stage, etc.>

## Caveats
<Edge cases, cost implications, things this fix doesn't cover.>
<Optional — omit if none.>
```

## The contract: lessons are guardrails

```
BEFORE executing Azure/Databricks work, the agent MUST:
  1. Scan lesson/ for lessons relevant to the planned action.
  2. If any match, FLAG them to the user:
     "⚠️ Lesson 05 applies: dbutils.notebook.run() loses env vars.
      Are you sure you want to use notebook chaining?"
  3. If the user proceeds anyway, note it but do not block.

This is NOT optional. Lessons exist because we burned time on these
exact mistakes. The whole point is to not repeat them.
```

## Distinction from other verbs

```
  lesson   "Azure DC-series is available when standard VMs stock out"
           -> about the PLATFORM being surprising -> lesson/

  feedback "the wiki page on clusters doesn't mention DC-series"
           -> about the WIKI being incomplete -> feedback/

  wiki     the actual concept reference page
           -> the stable knowledge base -> wiki/
```
