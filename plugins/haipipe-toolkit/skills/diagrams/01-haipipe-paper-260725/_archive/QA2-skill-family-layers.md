# Layers of the paper skill family
state: ✅ SETTLED
owner: JL
method: keep the existing spine, then give each layer one responsibility and one direction

## Question
How should the `paper/` skill family divide entry, lifecycle, workers, delivery, venue knowledge, and design work?

The current numbered tree is already close to the desired architecture, but several skills still carry routing, craft, rendering, history, and state at the same time. The useful change is a tighter ownership map, not a wholesale directory migration.

## Boundary
- ✅ Covered here
  The responsibility of each top-level paper skill-family layer.
- ↪ Covered elsewhere
  The contents of one callable skill folder are `QA3`; Display utilities need their own skill-set ruling after this ownership map is stable.

## Diagram
```
   one request, one direction, no second orchestrator

   user intent
       │
       ▼
   haipipe-paper/            thin front door: resolve the paper, open the Board,
       │                     route the intent. It decides WHICH, never HOW.
       ▼
   0-enter/                  which paper, which round
       │
       ▼
   1-lifecycle/              pick ONE S page, load ONE stage contract
       │
       ▼
   2-phase/                  DRAFT → PROBE → REVISE → CHECK
       │                     a bounded worker, returning to the SAME page
       ▼
   3-deliver/ → 4-respond/ → 5-present/
       build · audit · ship    rebuttal          slides · posters

   consulted, never in the chain of command:
     venue/     knowledge packs, read lazily. NEVER lifecycle verbs.
     diagram/   design Boards.               NEVER runtime contracts.
```

## Content
### Proposed family map
```
haipipe-paper/   thin front door: resolve paper, open Board, route intent
0-enter/         create or enter a paper and manage dated rounds
1-lifecycle/     stage contracts and the Board-aware stage runner
2-phase/         internal DRAFT, PROBE, REVISE, and CHECK workers
3-deliver/       build, render, audit, compile, export, and ship
4-respond/       rebuttal and revision response
5-present/       slides and posters derived from the accepted paper
venue/           lazily consulted knowledge packs, never lifecycle verbs
diagram/         design Boards, never runtime contracts
```

### Direction of control
The front door selects context.
The stage runner works one S page and dispatches a bounded worker.
Workers return results to the same page.
Delivery adapters materialize accepted Content into target formats.

## Items to Finish
- [x] 🗂 Keep the numbered family spine
      The existing top-level organization remains useful and avoids a migration with no user benefit.
- [ ] ✂️ Make the front door thin
      Move stage craft, comment detail, evidence detail, and output-specific rules to their actual owners.
- [ ] 🎨 Rule the Display split
      `QD1` now carries the proposed split among Paper meaning, reusable Display rendering, consumer adapters, and low-level utilities.
- [ ] 🧪 Trace one request through the layers
      A fresh session should move from Board to stage runner to worker to the same page without another orchestrator.

## Where we are
The target ownership map is clear and preserves the existing top-level tree.
The current skills still duplicate several responsibilities and have not been compacted.

## Files
- `haipipe-paper/SKILL.md`
  The front door that should become compact.
- `1-lifecycle/haipipe-paper-stage/`
  The page-first runner and stage contracts.
- `2-phase/`
  The internal worker family.
- `3-deliver/`
  The output and shipping family.

## Law
The numbered family spine stays. Each layer owns one responsibility and control flows one way: front door selects context, the stage runner works one S page, a bounded worker returns to that same page, delivery adapters materialize accepted Content.

`venue/` is knowledge consulted lazily and never carries a lifecycle verb. `diagram/` holds design Boards and never a runtime contract. Neither is in the chain of command.
