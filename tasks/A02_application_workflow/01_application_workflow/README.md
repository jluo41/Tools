# Application Workflow

Status: planned  
Scope: define the two Application workflow blocks and the fix plan.

## Problem

Paper already has a phase-owned workflow (`P0 Ideation` through `P6 Round`).
Application currently has a top-level lifecycle, but the two meaningful parts—
Insight and Design—are not yet expressed as two explicit, independently
readable workflow blocks.

This task is about the Application layer only. It does not change the Paper
workflow, the Task lifecycle, or the `code/haipipe` runtime pipeline.

## Canonical target

Application should be organized as:

```text
Application Workflow
├── Application Insight Workflow
│   ├── I0 Meta       — establish scope, data, grain, freshness, and limits
│   ├── I1 Chain      — climb registered D → I → K questions
│   └── I2 Wisdom     — contextualize K and issue a signed Design Handoff
└── Application Design Workflow
    ├── D0 Brief       — frame the design problem from the handoff
    └── D1 Design      — compose, render, judge, and reach human acceptance
```

The existing cross-phase gates remain gates, not extra phases:

```text
G0 Meta → Chain
G1 Chain → Wisdom
G2 Wisdom handoff signed
G3 question register settled
G4 Brief → Design
G5 Design → ACCEPTED
```

`Application Design` keeps its internal loop:

```text
direction proposed → human release → arm-agent realization
→ judge → render → human accept
```

The shared Page workflow remains underneath the blocks where a Page is used:
`OUTLINE → PROBE → EVIDENCE → DRAFT → REVISE/COMPILE → CHECK`.

## Fix plan

1. Make `haipipe-application-workflow` the top-level authority for the two
   blocks, their inputs/outputs, and gates G0–G5.
2. Add an explicit Application Insight workflow contract for I0–I2. It should
   own question-register settlement, D/I/K progression, receipts, and the
   signed Design Handoff.
3. Add an explicit Application Design workflow contract for D0–D1. It should
   own the Brief, direction/unit realization, design judgment, render, and
   human acceptance. `haipipe-design` remains the design-artifact contract;
   the new workflow contract owns sequencing and gates.
4. Update the Application README, router/index references, diagrams, and
   fixtures so that “Insight” and “Design” resolve to the same phase names and
   artifacts everywhere.
5. Preserve the shared Page workflow as a nested, non-linear workflow rather
   than introducing a second competing Page state machine.
6. Verify the change with fresh-context routing checks and known-broken cases:
   unresolved question register, missing Wisdom handoff, missing Brief, and
   unaccepted Design must each stop at the correct gate.

## Acceptance criteria

- A reader can identify the two Application blocks without inferring them from
  prose.
- Every phase has a named owner, input, output/receipt, and human gate where
  applicable.
- Insight ends at a signed Design Handoff; Design ends at `ACCEPTED`.
- The Paper workflow remains unchanged and is still the authority for Paper.
- No Application phase is silently delegated to the Task lifecycle.

## Source references

- `Tools/plugins/haipipe-toolkit/skills/application/haipipe-application-workflow/SKILL.md`
- `Tools/plugins/haipipe-toolkit/skills/application/haipipe-application/SKILL.md`
- `Tools/plugins/haipipe-toolkit/skills/application/haipipe-design/SKILL.md`
- `Tools/plugins/haipipe-toolkit/skills/paper/haipipe-paper-workflow/SKILL.md`
- `Tools/plugins/haipipe-toolkit/skills/board/page-workflows/haipipe-page-workflow/SKILL.md`
