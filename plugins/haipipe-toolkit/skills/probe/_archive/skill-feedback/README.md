# haipipe-probe — Feedback Inbox (orchestrator fallback)

Capture complaints, confusions, and wishes about the probe SKILL (its output is
hard to read, a lifecycle step is clunky, a verb is missing) while using it, then
fix them later in a skill-revision pass. This is feedback about the TOOL, not a
probe verdict.

Feedback is ROUTED at capture time to the unit it concerns. Probe is the FLAT
case: there are only two units. Feedback about agent BEHAVIOR (orchestrator /
creator / reviewer dispatch, monolithic collapse, nested-agent hangs, the
creator/reviewer loop skipped, a reviewer's verdict enum, broken independence)
goes to `../../agents/feedback/`. THIS folder is the **fallback**: it holds the
lifecycle procedures (Plan/Gather/Read/Judge/Deposit, owned by `../fn/*.md`), the
console/dashboard, and every cross-cutting concern no single step owns (the stage
strip, the return/status tail, probe id/naming/granularity, the venue
editor-chair test, compile-tex, the one-probe-many-discoveries fan-out, the
Read/Judge/Deposit boundary as a concept) plus anything the router could not
classify. The procedure a non-agent item concerns stays in its filename slug; the
folder a file lives in IS the record of which unit it concerns; there is no
cross-skill shared feedback.

## How

```
capture   /haipipe-probe feedback "<what bugged you>"
          -> infers the target unit (agents vs orchestrator) from the text
             (+ active context), then MERGES into a same-topic file or CREATES a
             new one in THAT unit's feedback/ (here, if not agent behavior).
             confirms merged-vs-new.
digest    /haipipe-probe digest ["<session-name|id>"] [--dry-run]
          -> digests a session (CURRENT, or a named/id'd PAST session run from a
             fresh context): scans the transcript for feedback, distills items,
             dedups (merge-or-create), and (after a confirm gate) routes each
             through capture. The bulk harvester. See ../fn/digest.md.
deposit   /haipipe-probe deposit
          -> settles a judged verdict; the deposit pass may also surface
             session feedback for routing through capture. See ../fn/deposit.md.
list      /haipipe-probe feedback list [unit]
          -> aggregates open items across BOTH feedback/ inboxes (newest first,
             grouped by unit); [unit] (agents|orchestrator) restricts to one.
move      /haipipe-probe feedback move <file> <unit>
          -> re-route a mis-filed item (unit = agents | orchestrator).
resolve   during a revision: set status: fixed + fixed_in + a one-line Fix note
          (keep the file as history; do not delete)
```

The 2-way routing map, inbox paths, merge-or-create, and the file schema live in
`../fn/feedback.md`. Inboxes are SELF-LIMITING: a same-topic complaint updates the
existing file (appends a dated recurrence, preserves prior wording verbatim,
reopens it if it had been fixed) instead of spawning a duplicate.

Capture-only by design: filing a complaint never tries to fix it on the spot.
Fixing is a separate, deliberate pass over the open items.
