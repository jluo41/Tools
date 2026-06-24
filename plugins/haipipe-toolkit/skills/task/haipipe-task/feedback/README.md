# haipipe-task — Feedback Inbox (orchestrator fallback)

Capture complaints, confusions, and wishes about the task SKILL (its output is
hard to read, a step is clunky, a verb is missing) while using it, then fix them
later in a skill-revision pass. This is feedback about the TOOL, not the work it
produces.

Feedback is ROUTED at capture time to the specific domain folder it concerns.
Each domain folder (`1_data` … `9_agent`, plus `agents/`) keeps its OWN
`feedback/` folder so the report sits next to the code that needs fixing. THIS
folder is the **fallback**: it holds cross-cutting discipline that no single
domain owns (the 4-stage lifecycle Plan/Build/Execute/Report, the IPO contract,
the task-folder scaffold, run conventions, the creator-reviewer loop, stage
file-ownership) plus anything the router could not classify. The folder a file
lives in IS the record of which unit it concerns; there is no cross-unit shared
feedback.

## How

```
capture   /haipipe-task feedback "<what bugged you>"
          -> infers the target domain folder from the text (+ active task-type),
             then MERGES into a same-topic file or CREATES a new one in THAT
             unit's feedback/ (or here, if cross-cutting). confirms merged-vs-new.
digest    /haipipe-task digest ["<session-name|id>"] [--dry-run]
          -> harvests a session (the CURRENT one, or a PAST session named/id'd
             as an argument, run from a fresh session): scans the transcript for
             feedback, distills items, dedups (merge-or-create), and (after a
             MANDATORY confirm gate) routes each through capture. The bulk
             harvester; never auto-files. See ../fn/digest.md.
list      /haipipe-task feedback list [unit]
          -> aggregates open items across ALL feedback/ inboxes (newest first,
             grouped by unit); [unit] restricts to one inbox.
move      /haipipe-task feedback move <file> <unit>
          -> re-route a mis-filed item to the right unit's inbox.
resolve   during a revision: set status: fixed + fixed_in + a one-line Fix note
          (keep the file as history; do not delete)
```

Routing map, inbox paths, merge-or-create, and the file schema live in
`../fn/feedback.md`. Inboxes are SELF-LIMITING: a same-topic complaint updates
the existing file (appends a dated recurrence, preserves prior wording verbatim,
reopens it if it had been fixed) instead of spawning a duplicate.

## One file per item

```
---
status: open | fixed
created: YYYY-MM-DD
updated: YYYY-MM-DD        # = created until the first merge
occurrences: 1            # bumped on each same-topic merge
context: <what you were doing, or general>
fixed_in: ""
regressed: ""             # set to a date if a fixed item resurfaces
---
<the feedback, in the reporter's words>

## Recurrences            # added on the FIRST merge; one dated line per re-surfacing
- YYYY-MM-DD: <the new phrasing, verbatim from the reporter>

Fix: <added when resolved>
```

Capture-only by design: filing a complaint never tries to fix it on the spot.
Fixing is a separate, deliberate pass over the open items.
