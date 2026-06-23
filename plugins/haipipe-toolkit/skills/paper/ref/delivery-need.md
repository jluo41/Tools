# Delivery Need (paper side)

How the paper records a gap as a need and routes it to the right evidence worker,
then backfills when the verdict/artifact returns. Paper-owned; the application
skill keeps its own copy. There is no cross-skill shared file.

## How paper talks to probe

No message bus, no shared contract file. Two channels carry it, and the agent
(this session) is the medium:

```
1. Command   paper hits a claim gap -> the agent runs
             /haipipe-probe plan from-need <need>. paper does not call probe
             directly; the agent reads this instruction, invokes probe, brings
             the result back.
2. Disk      paper writes the need (in 0-lifecycle/2-claims / STATUS); probe
   (async)   writes its verdict to probes/<id>/probe.yaml; paper reads that
             verdict to backfill. No handshake, just read/write the same files
             in turn.
```

Who owns which format: paper owns the NEED (loose; probe only reads the gap, no
strict schema). probe owns the VERDICT (strict, single source of truth in
`probe/.../ref/probe-yaml-schema.md`). That is why no shared interface file is
needed: each artifact's shape belongs to the skill that produces it.

## When to record a need

Only when the problem is EVIDENCE, not wording. A wording/structure problem loops
back inside the paper lifecycle (1-pitch / 2-claims / 3-narrative / 4-display
/ 5-minimap). A need leaves the paper for an evidence worker.

```
paper GAP -> delivery need -> evidence worker -> verdict/artifact -> paper backfill
```

Do NOT route through a project-level narrative layer (there isn't one).

## Routes (v4 verbs)

```
claim needs a verdict or robustness check     -> /haipipe-probe plan from-need <need>
claim needs outside literature / context      -> /haipipe-discovery <question>
claim or display needs a run / data artifact  -> /haipipe-task <contract>
finished evidence needs reusable K/W meaning  -> /haipipe-insight <artifact>
```

The probe entry is `plan from-need`: Plan intakes the paper claim gap, then
decides attach-to-existing-probe / new-probe / standalone and runs the
Plan -> Gather -> Read -> Judge -> Return lifecycle.

Two entry rules (who the delivery calls):

- a CLAIM need (needs a judged verdict) -> call PROBE; the probe owns the task call (its Gather step), so the claim is always judged before it lands. The delivery never calls a raw compute task for a claim-bearing need.
- a pure ARTIFACT / render need (no new claim, e.g. re-render a figure) -> call `/haipipe-task-for-display` directly; the display references the rendered asset.

## Need record

Each open need is one row in `0-lifecycle/2-claims/` (the claim ledger) or the
paper STATUS dashboard:

```
need_id      stable handle (e.g. N1, tied to a claim slot C2 or a display)
gap          which claim slot / display / section has the gap
kind         verdict | context | artifact | meaning
route        the command above
status       open | dispatched | returned
backfill     the slot/display to update when the worker returns
```

## Backfill (the return direction)

When a probe finishes, its Return step (`probe/.../fn/return.md`) sends the
verdict back here. On backfill:

```
- update the 2-claims slot status: have | weak | GAP, citing the probe verdict
- if the verdict narrows the claim, narrow the claim wording in 2-claims
- a probe NEVER edits paper prose without asking; it returns a verdict, the
  paper decides how to phrase it
```

One claim slot can be backed by one probe; multiple papers can cite the SAME
probe (evidence is shared, framing is not).

## Autonomous drain (the "keep going" loop)

The console is a derive-from-disk, resumable loop body. To drive a delivery to done:

```
LOOP until (no open needs) OR (gate hit) OR (only server-blocked left):
  1. enter    derive frontier + open needs from disk (the queue)
  2. pick     the next actionable need (skip server-blocked)
  3. route    claim -> probe (probe calls task) ; artifact -> task-for-display ; prose -> edit
  4. execute  write the artifact / verdict (local)
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
PAUSE + surface:   trigger a server/PHI run; declare a final yes/no verdict;
                   file insight as accepted knowledge; compile-to-submit;
                   destructive round / git ops
```

The loop runs AUTO unattended and stops at the first PAUSE gate, reporting what it hit.
