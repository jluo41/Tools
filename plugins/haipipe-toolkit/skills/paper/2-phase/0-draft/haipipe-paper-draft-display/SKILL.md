---
name: haipipe-paper-draft-display
description: "DRAFT-phase display auditor (internal). Walks a stage doc or section for claims that need visual support, maps each need to an existing 0-displays/ unit where one fits, and files a DR row in 0-lifecycle/4-display/_DISPLAY_REQUEST.md for each one that does not. Never creates a display, never plots, never links a unit that does not exist yet. Users invoke stage skills (narrative, section-edit...), not this skill directly."
argument-hint: "[stage-or-section] [paper-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "1.0.0"
  last_updated: "2026-07-19"
  summary: "DRAFT-phase display auditor: decide which claims need visual support, map each to an existing unit, and file a DR row in the display stage's inbox for each missing one. The paper layer plans, it does not plot. History: ./CHANGELOG.md."
---

haipipe-paper-draft-display
============================

The display lane of the DRAFT phase.
Called by `haipipe-paper-draft` while it drafts a stage doc or a section.

One job: **no claim that needs a picture leaves DRAFT without a unit or a request.**


The boundary, stated once
--------------------------

**The paper layer plans, it does not plot.**

- NEVER create an ad-hoc plot inline. A figure made in the drafting session has no producing task, no source data, and no way to be regenerated when the numbers change.
- NEVER edit a display's content directly. If it is wrong, the fix is to re-run the task that produced it.
- NEVER fabricate display content.


AUDIT — what needs a display
-----------------------------

Read the stage doc or section outline and ask, per claim:

```
needs a display    a comparison across more than two conditions ·
                   a distribution or a trend the reader must SEE to believe ·
                   a pipeline or architecture the prose keeps re-describing ·
                   a result table the argument returns to more than once
needs nothing      a single number (say it in the sentence) ·
                   a two-way comparison (say it in the sentence) ·
                   something a display would only restate
```

One claim per display. A figure carrying three claims is three figures, and the reader will take none of them.


PLAN — map each need to a unit
-------------------------------

For each need, in order:

```
1. an EXISTING 0-displays/<unit>/ already shows it
     → record the unit path against the need. Do NOT place a \ref yet —
       linking is ⑤ INTERPRET's job, after the unit is confirmed landed.
2. a DR row already requests it
     → reuse that DR id; mark the need 📨 pending.
3. nothing exists
     → file a DR row. This is the ONLY way a display comes into being from here.
```

The DR row, appended to `0-lifecycle/4-display/_DISPLAY_REQUEST.md`:

```markdown
## DR03 -- <short title>                        status: requested
- from: 5-section-edit/4-llmtrait · P4 · 2026-07-10
- claim: <the exact claim the display must support>
- form: figure | table | diagram | illustration   (suggestion; the display stage decides)
- evidence: <source hint: tasks/ path · metrics.json · a landed ### a-executor>
- unit: --                                        (display stage fills: 0-displays/displayNN-slug/)
```

Status flow, and ONLY the display stage advances it:

```
requested → accepted → done (unit: <path>)      or      declined (<reason>)
```

`form:` is a suggestion. The display stage owns the choice of figure vs table vs diagram, because it owns the venue's display budget and the gallery's shape.


The self-reference carve-out
-----------------------------

When the DISPLAY STAGE itself is the caller, working on its own accepted units: commissioning is that stage's own job and no DR row is filed. A stage filing requests into its own inbox is a loop, not a workflow.


Never pre-place a reference
----------------------------

A `\ref{fig:...}` for a display that does not exist yet compiles to `??` and ships that way, because nothing downstream re-checks a reference that was already written. A need whose DR row is still `requested` or `accepted` stays 📨 pending and is flagged for CHECK. Only a `done` row with its unit path filled may be linked, and the linking happens in ⑤ INTERPRET, not here.


Done criteria
--------------

- [ ] Every claim needing visual support maps to a unit path or a DR id
- [ ] Every missing unit has a DR row in the 4-display inbox
- [ ] Every DR row names the exact claim it must support
- [ ] No `\ref` written for a unit that does not exist
- [ ] No plot created, no display content edited


Siblings
---------

```
haipipe-paper-draft            the hub that calls this
haipipe-paper-draft-citation   the same shape for sources  (\cite{TOADD} [Q-<Stage>-<n>])
haipipe-paper-draft-values     the same shape for numbers  ({VAL:?} [Q-<Stage>-<n>])
haipipe-paper-display          owns _DISPLAY_REQUEST.md and advances every DR row
haipipe-paper-probe            ⑤ LINKs a landed unit into the section
haipipe-paper-check-evidence   audits displays pre-submission
```
