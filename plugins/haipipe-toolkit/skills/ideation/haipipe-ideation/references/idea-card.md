# Direction and Idea Cards

Cards are semantic projections over the evidence bundle. They are not
citations, Results, or a replacement for the Paper P0 page.

## Direction Card

One Direction Card describes the bounded area from which candidates are
generated:

```yaml
kind: direction-card
id: direction
title: "..."
question: "..."
why_now: "..."
scope: "..."
observed_signals:
  - statement: "..."
    evidence: [int01, ext01]
interpretations:
  - statement: "..."
    evidence: [int01, ext01]
    confidence: high | medium | low
open_gaps:
  - question: "..."
    route: task | discovery | human
bundle: bundle/evidence-bundle.yaml
```

`observed_signals` must be directly supported. `interpretations` may be
cross-source synthesis, but must name the inputs and confidence. `why_now` is
not a license for an unsupported novelty claim.

## Idea Card

Every candidate gets its own stable `iNN` card. Keep eliminated cards; their
history prevents rediscovery. The number of cards is dynamic. Optional
`comparison_order` controls display and review order only; it is not a verdict
or an automatic winner.

A candidate is **admitted** when it receives `iNN`. From that point its card
and Paper division remain durable even after elimination. A loose title,
duplicate wording, or broad framing rejected before admission may be retained
only in the Paper's Eliminated Ideas table with its source and reason; it does
not owe a fabricated card or division.

```yaml
kind: idea-card
id: i01
comparison_order: 1
title: "..."
claim: "one falsifiable research proposition"
method: "2–4 concrete steps"
hypothesis: "one sentence"
minimum_experiment: "smallest informative test"
expected_outcome: "signal and failure interpretation"
novelty_delta: "what the verified closest work does not establish"
core_claims:
  - id: c01
    claim: "..."
    evidence: [ext01]
    novelty_check:
      search_question: "the exact prior-art question asked"
      closest_work: "ext01 or explicit none found"
      remaining_delta: "what remains different from closest work"
      limitation: "what the search did not establish"
      status: novel | partial | preempted | inconclusive | unverified
feasibility:
  evidence: [int01]
  pilot: positive | negative | skipped | waived | pending
  receipt: "tasks/.../QA/...md"
  waiver: ""             # required when pilot: waived
risk: "..."
reviewer_objection: "strongest counterargument"
recommendation: proceed | proceed-with-caution | abandon | unresolved
state: open | deferred | selected | eliminated
evidence_bundle: ../bundle/evidence-bundle.yaml
```

Legacy cards with flat `novelty`, `closest_work`, `search_question`,
`remaining_delta`, and `limitation` fields remain readable. Any new or revised
card writes those fields inside `novelty_check` so the claim-level gate is one
visible record rather than five parallel fields.

The fields intentionally retain the downstream Paper vocabulary: Method,
Hypothesis, Minimum experiment, Expected outcome, Core Claims, Pilot result,
Risk, Reviewer's likely objection, and Recommendation. A candidate can be
semantically strong while still being `unresolved` if its evidence or
feasibility gate is incomplete.

## Pressure-test rules

- Check Core Claims one at a time, not as one blob.
- For each claim, record a `novelty_check` with the search question, closest
  verified work, remaining delta, unresolved limitation, and status. A search
  result without an admitted Discovery Result remains a lead.
- Feasibility is a Task-owned receipt. A pilot is not a Discovery citation and
  does not become a local ideation Run. `feasibility.receipt` is required for
  positive, negative, or skipped pilots; a `task-qa` receipt counts only when
  it explicitly answers the bounded feasibility/pilot question and gives its
  owner locator. `feasibility.waiver` is required only for a waived pilot and
  must state why no pilot is informative or permitted.
- The card-level novelty reading summarizes the worst
  `core_claims[].novelty_check.status`. `inconclusive` or `unverified` keeps
  the card open; it never upgrades to `novel` by intuition. A card with either
  state may be deferred or abandoned, but cannot satisfy the selected Paper
  handoff gate. `partial` is selectable only with the remaining delta and risk
  recorded.
- Machine-authored `recommendation` is advice. `comparison_order` is likewise
  only a review aid. `state: deferred`, `state: selected`, or
  `state: eliminated` requires a human decision receipt.

## Selection and Paper adapter

The selection receipt records the person, date, chosen card(s), accepted risk,
and the evidence/feasibility assertions that passed. A card cannot enter the
handoff only because it ranks first. Zero cards may be selected; when several
are selected, each receives a distinct Paper Story route.

The adapter to `haipipe-page-ideation` is direct:

| Ideation artifact | Paper P0 destination |
|---|---|
| Direction Card | Direction division |
| Idea Card summary | Ideas (ranked) table and one Idea division |
| `core_claims[].novelty_check` + Discovery Result paths | Core Claims / Novelty Check lines |
| Task feasibility receipt or waiver | Pilot result |
| `recommendation` | Recommendation field |
| human selection receipt | verdict and `went to` decision |
| eliminated cards | Eliminated Ideas table |

The Paper page binds back to the ideation handoff through its normal origin
and the selected Story's §5 Source Pages row. Historical `pagex/` bindings
remain readable but are not created for new work. The adapter carries IDs,
statuses, interpretations, and paths; it does not copy raw evidence or invent
citations.

The Paper P0 page may retain every candidate in one dynamic comparison set,
but each selected card's `went to` cell names its own Story (`Story-A`,
`Story-B`, ...). The comparison order does not have to match Story lettering.
