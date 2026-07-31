# Delivery: Opening
state: ✅ RULED
owner: JL
method: bind premise, seed, venue choice, pitch, and narrative into one reader-facing Delivery concern without inferring stage dependencies from Board order

## Question
What belongs together when a reader asks how this paper opens: why it exists, where it goes, what it promises, and what arc it currently follows?

## Boundary
- ✅ Covered here
  Seed, venue, pitch, and narrative as one Opening sequence.
- ↪ Covered by Work
  Growing the discovery and task banks that the opening reveals are needed; accepted answers may reopen the pitch or narrative.
- ↪ Covered by Main
  The manuscript Introduction; Opening is lifecycle control, not §1 prose.

## Diagram
```text
DELIVERY READING GROUP (not an execution graph)
Seed · Venue · Pitch · Narrative
  why    where    promise   arc
          └──────── Opening contract ────────┘
```

## Content
| Field | Contract |
|---|---|
| Lifecycle | Groups `0-seed/` with `2-venue/`; Venue is inside Opening in the Delivery reading order, not a later peer group. |
| Authority | `S-Seed-*` and `S-Venue-*` pages. |
| Projects to | Venue pin, paper promise, narrative arc, and downstream stage requirements. |
| Skills | `haipipe-paper-stage` for seed, venue, pitch, and narrative. |
| Consumes | The paper premise and known project context; no ad-hoc literature or computation. |
| Gate | A human accepts the current why/where/promise/arc snapshot; later Work evidence may reopen the affected pages. |
| Open gaps | Retargeting semantics remain a QA6 decision. |

## Items to Finish
- [x] Put Venue inside Opening.
- [x] Keep Opening distinct from the manuscript Introduction.

## Where we are
JL ruled the sequence on 2026-07-29: Opening includes Venue.

## Files
- `0-lifecycle/0-seed/`
- `0-lifecycle/2-venue/`

## Law
Opening is Seed plus Venue plus Pitch plus Narrative. Venue is not a separate Delivery group. This grouping does not renumber stages or replace their explicit dependency graph.

## Glossary
- **Opening**: the lifecycle contract that decides why, where, and how the paper will argue.

## Log
260729 · JL placed Venue inside Opening.
