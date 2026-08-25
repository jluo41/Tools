# Paper: Cross-event normalization for CGM prediction

state: 🟡 INTAKE · P0 Ideation is drafted · open: novelty receipts, decisive pilot, Seed
owner: research team
target: ICLR, provisional until a Narrative binds a Venue Page

## Purpose

This paper project develops the proposed ICLR study from the Claude Code
sessions that built the four event normalizers and their benchmark materials.
The candidate paper asks whether heterogeneous diabetes self-care events can be
made useful to CGM prediction by separating event identity from event quantity
and carrying the quantity basis, source, and confidence with the normalized
event.

The current project is intentionally at P0 Ideation.
The ICLR target is recorded as a requested direction, not as a completed venue
decision.
No Seed, Roadmap, Collection, Narrative, manuscript section, or submission
claim has been minted yet.

## Candidate paper story

The source sessions converge on one research direction:

1. Food, exercise, medication, and insulin logs arrive in incompatible forms.
2. Their existing normalizers independently expose the same five slots:
   `WHAT`, `HOW MUCH`, `BASIS`, `SOURCE`, and `CONF`.
3. A benchmark should evaluate `IDENTITY` and `QUANTITY` separately instead of
   collapsing them into one score.
4. The decisive downstream test is whether a basis-aware, confidence-aware
   event representation helps a CGM model use events that it currently ignores.

This is a working hypothesis.
The numerical results mentioned in the source sessions are recorded as
session-reported probes until the corresponding local task and QA receipts
exist.

## Source intake

- `Raw-FoodForm`, session `beae21bc-6d8b-4b68-a516-34d761f44573`, remote
  path `/home/jluo41/.claude/projects/-home-jluo41-WellDoc-SPACE/beae21bc-6d8b-4b68-a516-34d761f44573.jsonl`.
  This is the direct paper-story discussion, including the ICLR question,
  identity/quantity split, five-slot contract, and downstream CGM pilot.
- `CGM-Raw-Page-Workflow`, session `19088662-a806-4498-971f-9b5b9d15ab7e`,
  remote path `/home/jluo41/.claude/projects/-home-jluo41-WellDoc-SPACE/19088662-a806-4498-971f-9b5b9d15ab7e.jsonl`.
  This is the upstream normalization, benchmark, DataBoard, and outline work.
- Local synced event-normalization artifacts:
  `_WorkSpace/0-RawDataStore/0-EventNorm/`.
- Local synced DataBoard and source analysis:
  `examples/ProjA-CGM-Raw2AIData/diagram/01-DataBoard-260818/`.

## Next gate

Before creating `SD01-seed`, the project needs a claim-level novelty pass and
the smallest decisive pilot:

- expose `MatchedID` and `MatchedName` from the food normalizer;
- split every ruler into `IDENTITY` and `QUANTITY` metrics;
- rerun the XL-meal CGM experiment with quantity, basis, confidence, and
  coverage as explicit event inputs;
- record the result in a task-owned QA receipt.

The paper board and current ideation page are in
`0-paperboard/`.
