---
name: haipipe-ideation-generate
description: >-
  Stage 1 of HAI Ideation: turn a bounded direction and admitted Task/Discovery
  evidence into a diverse, deduplicated set of falsifiable Idea Cards. Use
  when asked to generate research ideas, expand a direction, find promising
  gaps, or build the first candidate portfolio; it does not claim novelty or
  choose a winner.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.1.0"
  last_updated: "2026-09-08"
  capability_family: "1_generate"
---

# /haipipe-ideation-generate · evidence to candidate portfolio

Load `haipipe-ideation` first. Read its `references/evidence-bundle.md` and
`references/idea-card.md`, plus `references/manifest-and-sync.md` for durable
work. Preserve the parent unit's BJTR identity. This skill owns
candidate-generation craft, admission, and the I1 working-state sync packet.
It does not search external sources, run internal analyses, verify novelty,
evaluate a journal's current rules, select an Idea, or write the Paper Page.

## Input contract

Start from four explicit inputs:

```text
direction question    what decision or unexplained phenomenon is in scope
boundary              population, setting, time, evidence and excluded areas
decision rule         what would make a candidate worth testing
evidence population   pointer-based Task and Discovery bundle plus open gaps
```

If the evidence population is missing, draft only provisional candidates and
route the missing source questions to Task or Discovery. Do not turn model
memory, a title hit, or a user hunch into an observed signal.

## Generation protocol

1. **Freeze the direction.** Restate the question, boundary, decision rule,
   and meaningful constraints. Separate user-provided hypotheses from observed
   evidence.
2. **Build the signal map.** Group bundle entries as agreement,
   contradiction, unexplained variation, measurement opening, method opening,
   new setting, negative result, or operational constraint. Retain source IDs.
3. **Generate across lenses.** Use every applicable lens below before
   repeating one:

   | Lens | Candidate move | Guardrail |
   |---|---|---|
   | unresolved contradiction | identify the mechanism or boundary that reconciles opposing Results | both sides must be named |
   | mechanism | explain how or why an observed relation could arise | not a relabeled correlation |
   | measurement/data | make a previously unobservable construct testable | access and validity remain open until tested |
   | identification/design | create a cleaner test of an important claim | novelty and identification stay separate |
   | heterogeneity/boundary | state when, where, or for whom a result changes | subgroup fishing is not a contribution |
   | intervention/decision | change an actionable input and predict an outcome | specify the decision-maker and counterfactual |
   | synthesis/generalization | connect results that have not been jointly explained | a convex combination is not automatically novel |

4. **Write the minimum scientific object.** For every provisional candidate,
   state one falsifiable claim, mechanism, method in 2–4 steps, minimum
   informative experiment, expected signal, failure interpretation, and 1–5
   Core Claims.
5. **Deduplicate semantically.** Compare the tuple `research question ×
   mechanism × identification/setting × outcome`. Merge wording variants;
   preserve genuinely different mechanisms or outcomes even when they share a
   dataset or topic.
6. **Admit deliberately.** Assign the next stable `iNN` only when the minimum
   scientific object is complete and its evidence/inference boundary is
   visible. Rejected pre-admission framings may be logged with a reason but do
   not receive fabricated cards.
7. **Prepare Test.** Set each new Core Claim's novelty status to `unverified`,
   identification to `unknown`, pilot to `pending`, and Venue Fit to pending.
   Generation never pre-passes the next stage.
8. **Sync Paper P0.** Refresh `projection/paper-ideation-sync.yaml` with the
   Direction, Discovery Landscape, Opportunity Map, and every admitted Idea.
   When the Paper P0 Page is in scope, route the packet to
   `haipipe-paper-ideation`; that owner mints or updates the same evergreen
   `Story00-ideation` Page.

Parallel workers may expand independent lenses or candidates, but the parent
desk deduplicates, assigns stable ids, and writes the canonical cards.

## Output contract

Durable output updates only:

```text
bundle/evidence-bundle.yaml     frozen owner pointers
cards/direction.yaml            bounded direction and signal map
cards/iNN_<idea>.yaml           one admitted scientific object per card
workflow/generate/*.yaml        generation receipt and rejected framings
projection/paper-ideation-sync.yaml  I1 reader-facing projection adapter
```

The exact manifest, receipt, filename, and sync schemas are in
`../../haipipe-ideation/references/manifest-and-sync.md`. The receipt records
which lenses were attempted, the provisional-to-canonical dedup map, admitted
ids, rejected framings, unresolved evidence requests, and the exact bundle
version consumed.

## Exit gate

An Idea may enter `2_test` only when it has a stable id, falsifiable claim,
method, hypothesis, minimum experiment, expected outcome, failure
interpretation, Core Claims, and evidence/inference labels. It need not be
novel yet. Claiming or scoring novelty at this stage is a gate failure.

## One-off mode

Return a Direction Card and provisional Idea Cards inline. Label their
novelty, identification, feasibility, and venue states `unverified` or
`unknown`. Write nothing unless the user asks to keep the portfolio.
