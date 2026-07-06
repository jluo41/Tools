# Delivery Need (application side)

How an intervention (message / checklist / dashboard / report) records a gap as a need and routes it to the right evidence worker, then backfills when the verdict/artifact returns. Application-owned; the paper skill keeps its own copy (`../../paper/wiki/11-delivery-need.md`). There is no cross-skill shared file.

## How the application talks to probe

No message bus, no shared contract file. Two channels carry it, and the agent (this session) is the medium:

```
1. Command   a stage hits an evidence gap -> the stage's PROBE phase buffers a
             _PROBE/PPNN card; `/haipipe-application probe run` hands the buffer
             to haipipe-application-probe (the PROBE phase worker), which
             dispatches Agent(haipipe-probe-orchestrator-agent). Stages never
             call /haipipe-probe or the discovery/task agents directly.
2. Disk      the need lives in the stage's _PROBE/PPNN_*.md card (+ index row in
   (async)   1-probe-plans/README.md); the returned takeaways and (full-mode)
             verdict land IN that card at TRANSLATE; the application reads the
             card to backfill. No handshake, just read/write the same card in turn.
```

Who owns which format: the application owns the NEED (the card's Need/Why/Route, loose; probe only reads the gap). Probe owns the VERDICT (strict; the PPNN card's `## Verdict` anatomy in `probe/haipipe-probe/SKILL.md`, enum `supported | refuted | inconclusive`). That is why no shared interface file is needed: each artifact's shape belongs to the skill that produces it.

## When to record a need

Only when the deliverable requires EVIDENCE the project does not yet have. A framing/format/tone problem stays inside the application lifecycle. A need leaves the application for an evidence worker.

```
stage gap -> _PROBE/PPNN card -> probe worker -> gateway -> verdict/artifact -> card -> backfill
```

## Routes (v5 verbs)

```
claim needs a verdict / robustness            -> /haipipe-application probe "<need>"   (buffer; run dispatches)
outside context / benchmark (non-claim)       -> /haipipe-application discover "<question>"
run / data artifact / display materialization -> /haipipe-application task "<contract>"  (or /haipipe-task-for-display)
finished evidence needs reusable K/W meaning  -> /haipipe-insight <artifact>
```

The retired verb `/haipipe-probe plan from-need` no longer exists (folderless probe, 2026-07-05): needs are cards, and the PROBE phase worker is the single dispatch point.

## Need record

Each open need is one `_PROBE/PPNN_<slug>.md` card (anatomy + statuses: `haipipe-application/fn/probe-plans.md`), indexed in `1-probe-plans/README.md`:

```
id           PPNN (numbering authority = the index)
stage        which lifecycle stage owns the card
claim/gap    which claim / element / section has the gap
kind         verdict | context | artifact | meaning
mode         light | full
status       planned | dispatched | read | verdicted
backfill     the ledger row / section / round slot to update on return
```

## Backfill (the return direction)

When the gateway returns, TRANSLATE lands everything in the card; backfill flows FROM the card:

```
- update the claim / element / section with the verdict or takeaway, citing the card + its refs
- verdict enum: supported -> claim supported; refuted -> drop or reword (never ship a
  refuted claim); inconclusive -> stays weak/GAP with the caveat recorded
- if support is partial, state the supported scope and the caveat
- the probe side NEVER edits application files; it returns, the worker lands, the
  application decides how to phrase it for its audience
```

The same landed evidence can serve both a paper and an application; each frames it for its own audience.
