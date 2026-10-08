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

Direction `interpretations[].confidence` is the strength of bundle evidence
for that specific cross-source synthesis, not confidence in an observed fact,
novelty, or identification. Use these owner-specific anchors:

| Label | Evidence anchor and example |
|---|---|
| `high` | Multiple independent, directly relevant bundle objects converge on the interpretation; source scope and plausible counter-signals have been checked. Example: separate Results report the same mechanism in the declared setting. Compared with `medium`, no material source or scope caveat remains. |
| `medium` | Direct evidence supports the interpretation, but a named limitation narrows its scope or an alternative explanation remains bounded. Example: one strong Result supports the synthesis while the only second source covers a narrower population. Compared with `high`, a non-decisive limitation remains. |
| `low` | Some relevant evidence suggests the synthesis, but it is indirect, sparse, or qualified by an unresolved but not contradictory limitation. Example: a single secondary analysis suggests a connection that still needs a direct test. Compared with `medium`, the evidentiary basis is weaker and supports only a tentative reading. |

Do not add a `none` label or map another field's confidence into this scale.
If the bundle has no relevant support, evidence is inaccessible, or material
signals conflict so no synthesis is defensible, abstain: omit the interpretation,
retain the observed signals, and record an `open_gaps` question with its owner
route. Do not use `low` to encode no evidence or unresolved contradiction.
These are qualitative anchors, not probabilities or empirically calibrated
inter-rater/outcome scores.

## Idea Card

Every candidate gets its own stable `iNN` card. Keep eliminated cards; their
history prevents rediscovery. The number of cards is dynamic. Optional
`comparison_order` controls display and review order only; it is not a verdict
or an automatic winner.

New ids are zero-padded (`i01`, `i02`, ...). A retrofit does not rename an
existing `i1` file or id merely for formatting: retain it in `legacy_ids`,
record `canonical_id: i01`, and use the mapping in receipts. The alias is an
identity bridge, not a second Idea Card.

A candidate is **admitted** when it receives `iNN`. From that point its card
and Paper division remain durable even after elimination. A loose title,
duplicate wording, or broad framing rejected before admission may be retained
only in the Paper's Eliminated Ideas table with its source and reason; it does
not owe a fabricated card or division.

```yaml
kind: idea-card
id: i01
canonical_id: i01
legacy_ids: []
comparison_order: 1
title: "2–5 word handle derived from the question, for slugs"
question: "the research question this Idea asks · one sentence ending in ? · the Idea's name everywhere"
claim: "one falsifiable research proposition"
method: "2–4 concrete steps"
hypothesis: "one sentence"
minimum_experiment: "smallest informative test"
expected_outcome: "signal and failure interpretation"
failure_interpretation: "what a null, contradictory, or failed minimum experiment means"
novelty_delta: "what the verified closest work does not establish"
core_claims:
  - id: c01
    contribution_role: central | supporting
    claim: "..."
    evidence: [ext01]
    novelty_check:
      search_question: "the exact prior-art question asked"
      closest_work: "ext01 or explicit none found"
      remaining_delta: "what remains different from closest work"
      rejection_case: "strongest evidence-bound case that the claim is already done"
      defense_case: "strongest honest case that a material delta remains"
      delta_tuple:
        research_question: "theirs versus candidate"
        mechanism: "theirs versus candidate"
        identification_or_setting: "theirs versus candidate"
        outcome: "theirs versus candidate"
      evidence_depth: none | metadata | abstract | full-text
      limitation: "what the search did not establish"
      status: novel | partial | preempted | inconclusive | unverified
      receipt: "workflow/novelty/i01_<timestamp>.yaml"  # raw assessment or same-kind resolution receipt; raw reviewer files remain linked there
identification:
  credibility: strong | conditional | weak | unknown
  fatal_assumptions: []
  repair_path: "..."
feasibility:
  evidence: [int01]
  pilot: positive | negative | skipped | waived | pending
  receipt: "tasks/.../results/.../runtime.yaml"
  pressure_receipt: "workflow/pressure/i01_<timestamp>.yaml"  # raw assessment or same-kind resolution receipt
  waiver: ""             # required when pilot: waived
venue_fit:
  card: venue-fit/i01_venue-fit.yaml
  broad_screen: complete | pending
  deep_fit: complete | pending | not-required
  overall: strong | conditional | weak | off-fit | unknown
  recommended_target: "Journal name or unresolved"
  nature_review: "workflow/nature/i01_<timestamp>.yaml or null"
  human_target: open | selected | deferred | rejected
risk: "..."
reviewer_objection: "strongest counterargument"
recommendation: proceed | proceed-with-caution | defer | abandon | unresolved
state: open | deferred | selected | eliminated
decision_ref: null  # immutable selection snapshot for a non-open human state
evidence_bundle: ../bundle/evidence-bundle.yaml
```

Legacy cards with flat `novelty`, `closest_work`, `search_question`,
`remaining_delta`, and `limitation` fields remain readable. Any new or revised
card writes those fields inside `novelty_check` so the claim-level gate is one
visible record rather than five parallel fields.

`question` is the Idea's identity for readers: the Paper Ideation Page heads the
Idea's division with it, its Ideas (ranked) row carries it, and the Paper
Workbench's Idea Card leads with it. It names one object, one relation or
contrast, one outcome, and the boundary it is asked inside, and it stays
informative when the answer is no. `title` is a handle derived from it, never
a substitute; a card with a title and a claim but no question is `unframed`
and the checker reports `unframed-idea` when the question does not end in `?`.

The fields intentionally retain the downstream Paper vocabulary: Method,
Hypothesis, Minimum experiment, Expected outcome, Core Claims, Pilot result,
Journal / Venue Fit, Risk, Reviewer's likely objection, and Recommendation.
The `venue_fit` block is a projection; the named fit card holds the comparison
and evidence detail. A candidate can be semantically strong while still being
`unresolved` if its evidence, feasibility, or venue-fit gate is incomplete.

## Pressure-test rules

- Check Core Claims one at a time, not as one blob.
- Mark every Core Claim `central` when the Idea's contribution depends on it,
  otherwise `supporting`. An omitted role is read as `central` for backward
  compatibility. The Test Matrix uses central-claim precedence rather than a
  count or average.
- For each claim, record a `novelty_check` with the search question, closest
  verified work, steelmanned rejection and defense, four-part delta tuple,
  evidence depth, remaining delta, unresolved limitation, receipt, and status.
  A search result without an admitted Discovery Result remains a lead.
- Novelty and identification credibility are separate axes. A claim may be
  genuinely new while its design is not yet credible; do not lower one axis to
  hide a problem on the other. Novelty confidence is recorded claim by claim in
  the linked novelty receipt and describes support from its stated literature
  boundary; identification credibility is the pressure-test reading of a
  specified design/contrast, with its evidence basis in the linked pressure
  receipt. Apply each owner's anchors in that specialist; neither field maps
  into the other's labels. `unknown`, `inconclusive`, `unverified`, or an
  unresolved reviewer disagreement remains an abstention/HOLD with its route,
  not a low score.
- Feasibility is a Task-owned receipt. A pilot is not a Discovery citation and
  does not become a local ideation Run. `feasibility.receipt` is required only for
  positive or negative pilots; a Task Run receipt counts only when
  it explicitly answers the bounded feasibility/pilot question and gives its
  owner locator. `feasibility.waiver` is required only for a waived pilot and
  must state why no pilot is informative or permitted.
- Existing analyses count as a retrospective pilot only when a Task-owned Run
  receipt answers this card's bounded minimum-experiment question, names the
  exact output and execution provenance, applies an acceptance reading, and
  classifies the result `positive` or `negative`. Folder names, manuscript
  claims, or aggregate outputs by themselves are prior evidence, not a pilot.
  `skipped` records its reason in pressure_receipt (pilot.reason), requires
  no Task result, and maps to pending in the Test Matrix. It does not satisfy
  G0; the card still needs a qualifying pilot or an explicit waiver.
- The selected-card eligibility reading checks every Core Claim separately.
  The matrix novelty column summarizes central contribution only and can be
  ready while a supporting claim still blocks selection. `inconclusive` or
  `unverified` keeps the evidence gate open; it never upgrades to `novel` by intuition. A card with either
  state may be deferred or abandoned, but cannot satisfy the selected Paper
  handoff gate. `partial` is selectable only with the remaining delta and risk
  recorded.
- Every admitted card receives a completed broad venue screen. Deep fit is
  required only for cards still live after novelty/feasibility pressure-testing,
  and it must resolve each named finalist through a current versioned Venue
  contract. An eliminated card may use `deep_fit: not-required`, but its broad
  screen and reason remain durable.
- Venue fit uses `strong | conditional | weak | off-fit | unknown`; it is not a
  numeric prestige score or acceptance prediction. A selected card requires
  `deep_fit: complete` and `human_target: selected`.
- Machine-authored `recommendation` is advice. `comparison_order` is likewise
  only a review aid. `state: deferred`, `state: selected`, or
  `state: eliminated` requires an explicit per-card human decision receipt.
  Store its immutable path in decision_ref; no answer leaves state open.
- New depth values are none/metadata/abstract/full-text. Read legacy
  metadata-only as metadata; none means no source was read and never upgrades
  to metadata. Copy the matching novelty receipt depth without changing it.
- Human target/state fields are projections of the versioned I3 receipt, not
  new write authorities. Follow the exact mapping and history rules in
  [receipts.md](receipts.md#immutable-history-and-projections).

## Selection and Paper adapter

The selection receipt records the person, date, chosen card(s), intended
target/category for each card, accepted risk, and the evidence, feasibility,
and venue-fit assertions that passed. A card cannot enter the handoff only
because it ranks first or because a machine recommended a journal. Zero cards
may be selected; when several are selected, each receives a distinct Paper
Story route and target decision.

The adapter to `haipipe-paper-ideation` is direct:

| Ideation artifact | Paper P0 destination |
|---|---|
| Direction Card | Direction division |
| Idea Card summary | Ideas (ranked) table and one Idea division |
| `core_claims[].novelty_check` + Discovery Result paths | Core Claims / Novelty Check lines |
| Task feasibility receipt or waiver | Pilot result |
| `venue_fit.card` + selected Venue contract | Journal / Venue Fit field and target column |
| `recommendation` | Recommendation field |
| human selection receipt | verdict, target, and `went to` decision |
| eliminated cards | Eliminated Ideas table |

The Paper page binds back to the ideation handoff through its normal origin
and the selected Story's §5 Source Pages row. Historical `pagex/` bindings
remain readable but are not created for new work. The adapter carries IDs,
statuses, interpretations, and paths; it does not copy raw evidence or invent
citations.

For a retrofit, split flat Core Claims into `cNN` rows only where the existing
text actually distinguishes claims. Bind an archived novelty check to a claim
only when its frozen question tests that claim; otherwise keep the claim
`unverified` and route a new Discovery check. Legacy Story ids may remain on
disk when the handoff records both `story_role: Story-A` and the exact
`story_path`; do not manufacture a new Story or a new historical receipt.

The Paper P0 page may retain every candidate in one dynamic comparison set,
but each selected card's `went to` cell names its own Story (`Story-A`,
`Story-B`, ...), and its target cell names the human-selected venue/category.
The comparison order does not have to match Story lettering or target roles.
