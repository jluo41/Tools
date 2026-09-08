# Ideation manifest and Paper P0 sync

This reference defines the durable unit manifest, Generate receipt, and the
working-state adapter that keeps one evergreen Paper Ideation Page synchronized
through I1 and I2. None of these records creates a human selection.

## Unit manifest

`ideation.yaml` is the small identity and state index for one direction:

```yaml
version: 1
kind: ideation-unit
address: b01.j01.t01
direction: "short stable direction name"
question: "bounded direction question"
scope: "population, setting, time, and evidence boundary"
decision_rule: "what must be true before an Idea may be selected"
stage: generate | test | select
state: open | held | selected | deferred | abandoned
bundle: bundle/evidence-bundle.yaml
direction_card: cards/direction.yaml
test_matrix: cards/test-matrix.yaml
paper_sync: projection/paper-ideation-sync.yaml
selection_receipt: workflow/selection.yaml
paper_handoff: handoff/paper-ideation.yaml
created_at: "ISO-8601"
updated_at: "ISO-8601"
```

`stage` names the active numbered capability family. It is not a Run state and
does not imply that the current stage passed. `state: selected` requires the
human selection receipt; `held`, `deferred`, and `abandoned` are honest terminal
or waiting readings rather than failures.

## Generate receipt

Write one immutable receipt for each material Generate pass under
`workflow/generate/gNN_<slug>.yaml`:

```yaml
version: 1
kind: ideation-generate
id: g01
direction: cards/direction.yaml
bundle: bundle/evidence-bundle.yaml
bundle_updated_at: "ISO-8601"
lenses_attempted:
  - contradiction
  - mechanism
  - measurement-data
  - identification-design
  - boundary-heterogeneity
  - intervention-decision
  - synthesis-generalization
provisional_candidates:
  - provisional_id: p01
    disposition: admitted | merged | rejected
    canonical_card: cards/i01_<idea>.yaml | null
    reason: "..."
deduplication:
  - candidates: [p01, p04]
    tuple_match: "research question × mechanism × identification/setting × outcome"
    kept: p01
rejected_framings:
  - framing: "..."
    source: "user | model | evidence id"
    reason: "..."
evidence_requests: []
created_at: "ISO-8601"
```

The receipt records how candidates were produced and admitted. It is not a
novelty report, a selection record, or an authority for factual claims.

## Working Paper P0 adapter

After I1 and whenever I2 changes evidence or an Idea, refresh
`projection/paper-ideation-sync.yaml`:

```yaml
version: 1
kind: paper-ideation-sync
source:
  ideation_task: b01.j01.t01
  ideation_manifest: ideation.yaml
  evidence_bundle: bundle/evidence-bundle.yaml
  direction_card: cards/direction.yaml
  test_matrix: cards/test-matrix.yaml | null
stage: I1 | I2
sync_revision: 3
paper_page:
  state: missing | bound | stale | blocked
  path: "Paper-.../A1-Story/Story00-ideation/...md or null"
  last_projected_revision: 2 | null
discovery_landscape:
  accepted_syntheses: ["discoveries/.../<page>.md"]
  direct_result_ids: [ext01, ext02]
  convergent_signals: []
  contradictions: []
  unresolved_territory: []
opportunity_map:
  - id: o01
    opportunity: "evidence-bounded opening"
    evidence: [ext01, int01]
    interpretation: "why the opening may matter"
    idea_ids: [i01, i03]
    status: open | narrowed | exhausted | contradicted
ideas:
  - card: cards/i01_<idea>.yaml
    state: open | deferred | eliminated
    comparison_order: 1
    novelty: unverified | hold | ready | partial | preempted
    identification: unknown | strong | conditional | weak
    feasibility: pending | positive | negative | waived | hold
    journal_fit: pending | strong | conditional | weak | off-fit | unknown | hold
    next_route: generate | novelty | pressure | task | discovery | venue | select | defer | abandon
portfolio_recommendation:
  status: not-reviewed | provisional
  summary: "machine-authored comparison; not a decision"
  ideas:
    - idea_id: i01
      recommendation: proceed | proceed-with-caution | defer | abandon | unresolved
      reason: "..."
selection_authority:
  owner: haipipe-ideation-select
  status: none
  receipt: null
sync_status: current | stale | blocked
open_gaps: []
updated_at: "ISO-8601"
```

At I1, `test_matrix` may be null and test states remain unverified/pending. At
I2, the packet projects the current matrix. `paper_page.state: missing` is a
request for `haipipe-paper-ideation` to mint or bind the one evergreen P0 Page;
it is not permission for Ideation to create Paper files itself.

Use `paper_page.state: blocked` when the canonical Paper P0 target is known but
the current execution lacks write scope, owner permission, or an available
Paper projection route. Retain the canonical target in `paper_page.path`, keep
`last_projected_revision` at the last actually projected revision (or `null`),
set `sync_status: blocked`, and name the reason in `open_gaps`. Do not mint a
run-local surrogate Page and do not invent a separate projection receipt: the
sync packet itself is the durable blocked-return record.

## Projection law

- The Discovery Landscape summarizes accepted synthesis Pages and direct
  evidence ids; it does not copy Result Cards, facts, BibTeX, or raw notes.
- The Opportunity Map is Ideation's interpretation of how the landscape opens,
  narrows, contradicts, or exhausts candidate space. Each entry names evidence
  and affected Idea ids.
- Generate or Test may add, revise, merge, reorder, defer, or eliminate Ideas.
  Every material change increments `sync_revision` and updates the same Paper
  P0 Page rather than minting another portfolio.
- `paper_page.last_projected_revision` lets both sides detect stale rendering.
  A Page is current only when it equals `sync_revision` and its normal Page
  workflow records the projection.
- The sync packet never contains `decision`, `selected_cards`, `target_routes`,
  or `story_routes`. Those fields belong only to the I3 human selection receipt
  and final handoff.
- `portfolio_recommendation` is the canonical pre-decision machine artifact.
  Do not create a parallel `portfolio-recommendation.yaml`; updating the sync
  packet keeps the Paper cockpit and semantic source on the same revision.
- Paper P0 may display verdict, target, and `went to` only by projecting the I3
  receipt received in the final handoff. Page approval or CHECK is not an
  independent selection.
