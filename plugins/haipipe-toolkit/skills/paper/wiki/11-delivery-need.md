# Delivery Need (paper side)

How the paper records a gap as a need, routes it to the right evidence worker, and
backfills when the answer returns. Paper-owned; the application skill keeps its own
copy. There is no cross-skill shared file.

## How paper talks to probe

No message bus, no shared contract file. Two channels carry it, and the agent
(this session) is the medium:

```
1. Command   paper hits a claim gap -> the agent runs
             /haipipe-paper probe "<question>" (opens a SECTION in the topic's probe
             file). The PROBE worker MATCHes it against the bank's QA corpus first, and
             dispatches the `commission:` block only if MATCH cannot close it.
2. Disk      paper writes the need (in 0-lifecycle/1-claims / STATUS); the executor
   (async)   writes the answer as <task-folder>/QA/<n>-<slug>.md; the section's `target:`
             points at that FILE and its `reading:` interprets it. No handshake —
             binding is by PATH, and the file on disk IS the state.
```

Who owns which format: the paper owns the NEED (loose) and the `reading:` (its own
vocabulary). The EXECUTOR owns the ANSWER (the QA file: `# Q` / `## Answer` /
`## Caveats` / `## Not-done`, general language, anatomy in
`probe/haipipe-probe/SKILL.md`). A CLAIM's status is the paper's alone, and lives in
`0-lifecycle/1-claims/1-claims.md`. That is why no shared interface file is needed:
each artifact's shape belongs to the layer that produces it.

## When to record a need

Only when the problem is EVIDENCE, not wording. A wording/structure problem loops
back inside the paper lifecycle (1-claims / 2-pitch / 3-narrative / 4-display
/ 5-section-edit). A need leaves the paper for an evidence worker.

```
paper GAP -> a question SECTION in 1-probes/ -> the PROBE phase MATCHes it ->
DISPATCH only what MATCH cannot close -> the answering QA file -> the section's
`reading:` -> the paper backfills (the claim's status flips in 1-claims.md)
```

Do NOT route through a project-level narrative layer (there isn't one).

## Routes (v4 verbs)

```
claim needs its status settled                -> /haipipe-paper probe "<need>"  (a question SECTION)
claim needs outside literature / context      -> /haipipe-discovery <question>
claim or display needs a run / data artifact  -> /haipipe-task <contract>
settled claim status (supported|refuted|      -> 0-lifecycle/1-claims/1-claims.md (the ONLY home of a
  inconclusive + confidence + claim_type)         claim's status; the probe section carries only its
                                                  `reading:`. `## Verdict`/`verdicted` are DELETED)
```

The entry is `/haipipe-paper probe "<need>"`: it opens a question SECTION in the
right topic's probe file. The PROBE phase then runs the five-step loop — ORGANIZE →
MATCH (reuse an existing QA file if one answers it) → DISPATCH (the `commission:`
block, verbatim, to the task/discovery orchestrator) → POINT → INTERPRET.

Two entry rules (who the delivery calls):

- a CLAIM need (a claim's status is at stake) -> raise a question SECTION and let the PROBE phase route it. The paper never calls a raw compute agent for a claim-bearing need, and never executes bank work inline (LAW 1).
- a pure ARTIFACT / render need (no claim at stake, e.g. re-render a figure) -> call `/haipipe-task-for-display` directly; the display references the rendered asset.

## Need record

Each open need is one row in `0-lifecycle/1-claims/` (the claim ledger) or the
paper STATUS dashboard:

```
need_id      stable handle (e.g. N1, tied to a claim slot C2 or a display)
gap          which claim slot / display / section has the gap
kind         evidence | context | artifact | meaning
route        the command above
state        open | commissioned | returned      (mirrors the probe section's derived state)
backfill     the slot/display to update when the worker returns
```

## Backfill (the return direction)

The answer is a FILE: the executor's `<task-folder>/QA/<n>-<slug>.md`. The probe
section's `target:` points at it, and its `reading:` says what it MEANS for
this paper. On backfill:

```
- write the claim's status in 0-lifecycle/1-claims/1-claims.md — supported |
  refuted | inconclusive, + confidence + claim_type + G1/G2/G3. THAT ledger is
  the only home of a claim's status.
- if the evidence narrows the claim, narrow the claim wording in 1-claims
- the executor NEVER edits paper prose: it returns a FACT, and the paper decides
  what the fact means and how to phrase it
```

Multiple papers can cite the SAME QA file in discoveries/ + tasks/, each through
its own section and its own `reading:` — the FACT is shared, the JUDGMENT is not.

## Autonomous drain (the "keep going" loop)

The console is a derive-from-disk, resumable loop body. To drive a delivery to done:

```
LOOP until (no open needs) OR (gate hit) OR (only server-blocked left):
  1. enter    derive frontier + open needs from disk (the queue)
  2. pick     the next actionable need (skip server-blocked)
  3. route    claim -> a question SECTION (the PROBE phase dispatches it) ;
              artifact -> task-for-display ; prose -> edit
  4. execute  write the artifact locally, or wait for the dispatched QA file
  5. backfill update the slot/display/section; mark the need returned
  6. -> 1
```

State lives on disk (the need ledger + STATUS), so a fresh session re-enters and continues.

### Server vs local

A local need (render, parse, draft, backfill) drains immediately. A need that requires a NEW server run (Stata on PHI depositing to `Report-From-CMS-Server`) is server-blocked: schedule a poll and resume when results land. A figure renders locally; it blocks only if its underlying regression is not back yet.

### Autonomy policy

```
AUTO (no asking):  local render/parse, backfill claims/displays, draft a stage tex,
                   compile previews, parse logs, status/ledger updates
PAUSE + surface:   trigger a server/PHI run; declare a final yes/no answer;
                   settle a claim's status in 1-claims.md; compile-to-submit;
                   destructive round / git ops
```

The loop runs AUTO unattended and stops at the first PAUSE gate, reporting what it hit.
