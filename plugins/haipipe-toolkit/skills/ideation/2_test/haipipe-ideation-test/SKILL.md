---
name: haipipe-ideation-test
description: >-
  Stage 2 router for HAI Ideation. Reconcile claim-level novelty, scientific
  pressure testing, feasibility, journal fit, and optional Nature-family
  editorial review into one evidence-bound test matrix. Use to test, vet,
  red-team, or compare admitted research ideas before human selection.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.1.0"
  last_updated: "2026-09-08"
  capability_family: "2_test"
---

# /haipipe-ideation-test · reconcile the evidence against each Idea

Load `haipipe-ideation` and the admitted Idea Cards first. This skill owns the
Stage 2 routing and test matrix; the specialists own their respective craft:

```text
haipipe-novelty-check          prior-work overlap and remaining delta
haipipe-idea-pressure-test     falsifiability, identification, feasibility
haipipe-journal-fit            broad screen and current-contract deep fit
haipipe-nature-paper-review    optional Nature-family editorial overlay
```

Load the first three for a complete test. Load the Nature specialist only when
the user asks for it or a named Nature-family target remains live. A
single-axis request loads only that specialist and updates the corresponding
matrix row; it does not imply the other axes passed.

## Per-Idea test matrix

Maintain `cards/test-matrix.yaml` as a projection over canonical cards and
receipts:

```yaml
kind: ideation-test-matrix
bundle: ../bundle/evidence-bundle.yaml
ideas:
  - idea_id: i01
    novelty: ready | partial | preempted | hold
    identification: strong | conditional | weak | unknown
    feasibility: positive | negative | waived | pending | hold
    journal_fit: strong | conditional | weak | off-fit | unknown | hold
    nature_shape: plausible | upgrade-required | specialist-reroute | not-nature-shaped | not-requested | hold
    fatal_blockers: []
    repairable_gaps: []
    receipts:
      novelty: workflow/novelty/i01_<timestamp>.yaml
      pressure: workflow/pressure/i01_<timestamp>.yaml
      journal_fit: cards/venue-fit/i01_venue-fit.yaml
      nature: null
    next_route: novelty | pressure | task | discovery | venue | select | defer | abandon
updated_at: "ISO-8601"
```

The matrix is a readable index, not a second authority. Every cell links back
to the Idea Card, owner Result, Venue Fit Card, or specialist receipt that
supports it.

## Test protocol

1. Inventory admitted cards and check that each passed the Generate exit gate.
2. Run novelty claim by claim. Do not test a title-shaped blob.
3. Run the pressure test independently. A novel idea may have weak
   identification; a feasible idea may be preempted.
4. Broad-screen every admitted card for publication families. Deep-fit only
   live finalists against current Venue contracts.
5. Apply the Nature overlay only after a concrete Nature-family target and
   generic fit card exist.
6. Reconcile results without averaging. A fatal blocker remains visible even
   when other axes are strong. Use no composite prestige or novelty score.
7. Route every gap to its actual owner and stop at any required human or
   execution gate. Resume the affected axis when new evidence lands.
8. Refresh `projection/paper-ideation-sync.yaml` and route it to the same
   evergreen Paper P0 Page whenever an Idea, evidence reading, comparison
   order, elimination, or next route changes.

Independent Idea checks may run in parallel. Writes remain one canonical card
and receipt per Idea; the router reconciles the matrix only after checking the
returned paths and statuses.

## State readings

- `ready` means the specialist's own evidence gate passed, not that the Idea
  is selected.
- `partial` or `conditional` can proceed only with named residual risk.
- `hold` means missing, stale, inaccessible, or contradictory evidence blocks
  an honest judgment.
- `preempted`, `negative`, `off-fit`, or `not-nature-shaped` are legitimate
  findings, not execution failures.
- A machine recommendation never changes an Idea to `selected` or
  `eliminated`; those states belong to `3_select` and a human receipt.

Project Core Claims into the matrix by contribution role:

```text
any central claim preempted                 → preempted
else any central claim inconclusive/unverified → hold
else any central claim partial              → partial
else all central claims novel               → ready
```

Each Core Claim declares `contribution_role: central | supporting`. A
supporting-claim gap remains visible in `repairable_gaps` but does not
mechanically preempt the Idea. If no role is declared, treat the claim as
central. Do not use count, majority vote, or an average to override this
precedence.

## Exit gate

An Idea is eligible for Select only when all Core Claims have bounded novelty
readings, novelty and identification are separate, feasibility has a Task
receipt or reasoned waiver, its broad venue screen is complete, and every
named deep-fit finalist has a current Venue contract. Nature review is
required only when a Nature-family target is under consideration.

Run the shared checker with `--gate test` before presenting a durable test as
complete. Mechanical success does not replace scientific judgment.
