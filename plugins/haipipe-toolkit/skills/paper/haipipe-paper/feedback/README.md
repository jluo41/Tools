# haipipe-paper — Feedback Inbox (orchestrator fallback)

Capture complaints, confusions, and wishes about the paper SKILL (its output is
hard to read, a step is clunky, a verb is missing) while using it, then fix them
later in a skill-revision pass. This is feedback about the TOOL, not the work it
produces.

Feedback is ROUTED at capture time to the specific sub-skill it concerns. Each
sub-skill keeps its OWN `feedback/` folder so the report sits next to the code
that needs fixing. THIS folder is the **fallback**: it holds cross-cutting
discipline that no single stage owns (stage strip, illuminate-every-stage,
compile-pdf-every-stage, the stage gate, the status tail, the diagram-ascii
habit, interrogate-every-unit, probe-routing from the paper, the construction
beat) plus anything the router could not classify. The folder a file lives in IS
the record of which skill it concerns; there is no cross-skill shared feedback.

## How

```
capture   /haipipe-paper feedback "<what bugged you>"
          -> infers the target skill from the text (+ active stage), then
             MERGES into a same-topic file or CREATES a new one in THAT skill's
             feedback/ (or here, if cross-cutting). confirms merged-vs-new.
digest    /haipipe-paper digest
          -> digests THIS session: scans the transcript for feedback, distills
             items, dedups, and (after a confirm gate) routes each through
             capture. The bulk harvester. See ../fn/digest.md.
list      /haipipe-paper feedback list [skill]
          -> aggregates open items across ALL feedback/ inboxes (newest first,
             grouped by skill); [skill] restricts to one inbox.
move      /haipipe-paper feedback move <file> <skill>
          -> re-route a mis-filed item to the right skill's inbox.
resolve   during a revision: set status: fixed + fixed_in + a one-line Fix note
          (keep the file as history; do not delete)
```

Routing map, inbox paths, merge-or-create, and the file schema live in
`../fn/feedback.md`. Inboxes are SELF-LIMITING: a same-topic complaint updates
the existing file (appends a dated recurrence, preserves prior wording verbatim,
reopens it if it had been fixed) instead of spawning a duplicate.

Capture-only by design: filing a complaint never tries to fix it on the spot.
Fixing is a separate, deliberate pass over the open items.
