# haipipe-insight — Feedback Inbox (orchestrator fallback)

Capture complaints, confusions, and wishes about the insight SKILL (its output is
hard to read, a verb is clunky, routing is wrong, a card-review gate misfires)
while using it, then fix them later in a skill-revision pass. This is feedback
about the TOOL, not the D/I/K/W cards it produces.

Feedback is ROUTED at capture time to the specific sub-skill it concerns. Each
sub-skill keeps its OWN `feedback/` folder so the report sits next to the code
that needs fixing. THIS folder is the **fallback**: it holds cross-cutting DIKW
concerns that no single layer owns (the in-sample vs generalization boundary, the
insight-md card schema, INDEX.md, the id<->layer graph, sources<->ref_by symmetry,
the review/apply funnel, card granularity / lifecycle / change-log policy) plus
anything the router could not classify. The folder a file lives in IS the record
of which skill it concerns; there is no cross-skill shared feedback.

## How

```
capture   /haipipe-insight feedback "<what bugged you>"
          -> infers the target skill from the text (+ active layer), then
             MERGES into a same-topic file or CREATES a new one in THAT skill's
             feedback/ (or here, if cross-cutting). confirms merged-vs-new.
digest    /haipipe-insight digest ["<session-name|id>"] [--dry-run]
          -> digests a session (CURRENT with no arg, or a PAST one by name/id
             from a fresh session): scans the transcript for feedback, distills
             items, dedups, and (after a confirm gate) routes each through
             capture. The bulk harvester; self-limiting via merge-or-create.
             See ../fn/digest.md (session resolution + harvest).
list      /haipipe-insight feedback list [skill]
          -> aggregates open items across ALL feedback/ inboxes (newest first,
             grouped by skill); [skill] restricts to one inbox.
move      /haipipe-insight feedback move <file> <skill>
          -> re-route a mis-filed item to the right skill's inbox.
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

## Recurrences            # added on the first merge; one dated line per re-surfacing
- YYYY-MM-DD: <the new phrasing, verbatim from the reporter>

Fix: <added when resolved>
```

Capture-only by design: filing a complaint never tries to fix it on the spot.
Fixing is a separate, deliberate pass over the open items.
