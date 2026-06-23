# Delivery Need (application side)

How an application (report / message / ui / answer to a question) records a gap
as a need and routes it to the right evidence worker, then backfills when the
verdict/artifact returns. Application-owned; the paper skill keeps its own copy.
There is no cross-skill shared file.

## How the application talks to probe

No message bus, no shared contract file. Two channels carry it, and the agent
(this session) is the medium:

```
1. Command   application hits a question gap -> the agent runs
             /haipipe-probe plan from-need <need>. application does not call
             probe directly; the agent reads this instruction, invokes probe,
             brings the result back.
2. Disk      application writes the need (in its plan / session state); probe
   (async)   writes its verdict to probes/<id>/probe.yaml; application reads
             that verdict to backfill the answer. No handshake, just read/write
             the same files in turn.
```

Who owns which format: application owns the NEED (loose; probe only reads the
gap, no strict schema). probe owns the VERDICT (strict, single source of truth
in `probe/.../ref/probe-yaml-schema.md`). That is why no shared interface file
is needed: each artifact's shape belongs to the skill that produces it.

## When to record a need

Only when answering the audience question requires EVIDENCE the project does not
yet have. A framing/format problem stays inside the application lifecycle. A need
leaves the application for an evidence worker.

```
question gap -> delivery need -> evidence worker -> verdict/artifact -> answer backfill
```

Do NOT route through a project-level narrative layer (there isn't one).

## Routes (v4 verbs)

```
answer needs a claim verdict / robustness     -> /haipipe-probe plan from-need <need>
answer needs outside context / benchmark      -> /haipipe-discovery <question>
answer needs a run / data artifact / display  -> /haipipe-task <contract>
finished evidence needs reusable K/W meaning  -> /haipipe-insight <artifact>
```

The probe entry is `plan from-need`: Plan intakes the application question gap,
decides attach / new / standalone, and runs Plan -> Gather -> Read -> Judge ->
Return.

## Need record

Each open need is one row in the application plan / session state:

```
need_id      stable handle, tied to the question or a report claim
gap          which question / claim / slide / section has the gap
kind         verdict | context | artifact | meaning
route        the command above
status       open | dispatched | returned
backfill     the answer slot to update when the worker returns
```

## Backfill (the return direction)

When a probe finishes, its Return step sends the verdict back here. On backfill:

```
- update the answer / report claim with the verdict, citing it
- if the verdict is partial, state the supported scope and the caveat
- a probe NEVER edits the application copy without asking; it returns a verdict,
  the application decides how to phrase it for its audience
```

The same probe verdict can serve both a paper and an application; each frames it
for its own audience.
