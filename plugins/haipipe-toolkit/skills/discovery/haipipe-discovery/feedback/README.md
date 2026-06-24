# haipipe-discovery - Feedback Inbox (orchestrator fallback)

Capture complaints, confusions, and wishes about the discovery SKILL (its output
is hard to read, a step is clunky, a verb is missing) while using it, then fix
them later in a skill-revision pass. This is feedback about the TOOL, not the
discovery findings it produces (sources / verdict / landscape / ideas).

Feedback is ROUTED at capture time to the specific bucket unit it concerns. Each
unit (1_search, 2_read, 3_review, 4_idea, agents) keeps its OWN `feedback/`
folder so the report sits next to the code that needs fixing. THIS folder is the
**fallback**: it holds cross-cutting discipline that no single bucket owns (the
Plan/Build/Execute/Report lifecycle, the Search/Review/Idea (搜/析/创) type field,
the discovery.yaml schema, status.yaml, the report block, the stage strip, the
dashboard, the group-letter hints) plus anything the router could not classify.
The folder a file lives in IS the record of which unit it concerns; there is no
cross-skill shared feedback.

## How

```
capture   /haipipe-discovery feedback "<what bugged you>"
          -> infers the target unit from the text (+ active type/stage), then
             MERGES into a same-topic file or CREATES a new one in THAT unit's
             feedback/ (or here, if cross-cutting). confirms merged-vs-new.
digest    /haipipe-discovery digest
          -> digests THIS session: scans the transcript for feedback, distills
             items, dedups, and (after a confirm gate) routes each through
             capture. The bulk harvester. See ../fn/digest.md.
list      /haipipe-discovery feedback list [unit]
          -> aggregates open items across ALL feedback/ inboxes (newest first,
             grouped by unit); [unit] restricts to one inbox.
move      /haipipe-discovery feedback move <file> <unit>
          -> re-route a mis-filed item to the right unit's inbox.
resolve   during a revision: set status: fixed + fixed_in + a one-line Fix note
          (keep the file as history; do not delete)
```

Routing map, inbox paths, merge-or-create, and the file schema live in
`../fn/feedback.md`. Inboxes are SELF-LIMITING: a same-topic complaint updates
the existing file (appends a dated recurrence, preserves prior wording verbatim,
reopens it if it had been fixed) instead of spawning a duplicate.

Capture-only by design: filing a complaint never tries to fix it on the spot.
Fixing is a separate, deliberate pass over the open items.
