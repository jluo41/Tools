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
`projection/paper-ideation-sync.yaml`. If a Paper P0 path is bound, hand the
packet to `haipipe-paper-ideation`, which applies the current `haipipe-page`
update boundary. Updating this packet is the semantic-source step; it does not
by itself publish the P0 Page's adopted Markdown or delivery.

```yaml
version: 2
kind: paper-ideation-sync
source:
  ideation_task: b01.j01.t01
  ideation_manifest: ideation.yaml
  evidence_bundle: bundle/evidence-bundle.yaml
  direction_card: cards/direction.yaml
  test_matrix: cards/test-matrix.yaml | null
stage: I1 | I2
sync_revision: 3
source_hash: "sha256:<hash of this semantic packet>"
projection:
  change_class: state | portfolio | structure
  affected_idea_ids: [i01]
  identity_key: idea_id
paper_page:
  state: missing | bound | blocked
  path: "Paper-.../A1-Story/Story00-ideation/...md or null"
  working:
    state: not-requested | current | stale | blocked
    revision: 2 | null
    source_hash: "sha256:<consumed sync hash>" | null
    receipt: "Paper-.../A1-Story/Story00-ideation/workflow/receipts/p0-working.yaml" | null
  release:
    state: not-requested | current | stale | blocked
    revision: 2 | null
    source_hash: "sha256:<released source hash>" | null
    receipt: "Paper-.../A1-Story/Story00-ideation/workflow/receipts/p0-release.yaml" | null
  delivery:
    state: not-requested | current | stale | blocked
    revision: 2 | null
    source_hash: "sha256:<delivery source hash>" | null
    receipt: "Paper-.../A1-Story/Story00-ideation/workflow/receipts/p0-delivery.yaml" | null
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
    state: open | deferred | selected | eliminated
    decision_ref: null  # immutable I3 receipt required for non-open state
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

`sync_revision` and `source_hash` identify the reviewed semantic source.
Compute the source fingerprint from the semantic packet, excluding source_hash,
updated_at, paper_page projection receipts/surfaces, and human-only ideas[].state
and ideas[].decision_ref projections. Refreshing those human projections does
not advance the evidence revision. Changes to evidence, claims, tests or machine
recommendations do advance it. New I3 selection/handoff pins both values; an old
snapshot remains historical and cannot authorize a new handoff after they change.
The three
`paper_page` surfaces are independent attestations, not three names for one
`current` flag:

- `working` records the latest Page-owned projection refresh. It may be current
  before adopted Content or delivery is current.
- `release` records the Page-level CONTENT/release pass. It is current only
  when it consumed the same semantic revision and source hash as `working`.
- `delivery` records the generated delivery from that released Page source. It
  is current only when `release` is current and its receipt names the matching
  released source.

Every current surface has a real Page-owned dispatch receipt (serialized `phase`) whose
`paper_projection` extension records the consumed `sync_revision`,
`source_hash`, Page path, surface, output hash, and timestamp. A Page update may bring the working
Outline/preview/Bullet Workspace to the new revision while leaving adopted
Content and `delivery/` stale by design. A formal Page-level CONTENT pass is
required before those published surfaces can be called current.

The Page/Paper route writes receipts only. On the next semantic sync, the
Ideation adapter reads those receipts and writes the nested `paper_page` status
back into the sync packet; Page never edits the Ideation-owned semantic packet.

`sync_status` is a compatibility summary of the semantic-to-working route:
`current` means `paper_page.working` is current, `stale` means the packet is
newer than the working projection or the Page is not bound, and `blocked` means
the route cannot currently complete. It never promotes `release` or `delivery`.

Use `paper_page.state: blocked` when the canonical Paper P0 target is known but
the current execution lacks write scope, owner permission, or an available
Paper projection route. Retain the canonical target in `paper_page.path`, keep
each surface at its last honest revision and receipt, set `sync_status:
blocked`, and name the reason in `open_gaps`. Do not mint a run-local surrogate
Page and do not invent a local Ideation Run. The Page-owned dispatch receipt (serialized `phase`) is
the durable success record; the sync packet is the durable blocked-return
record.

### Projection routing

The `projection.change_class` determines the narrowest Page action:

| Change class | Meaning | Page action | Page Run |
|---|---|---|---|
| `state` | evidence/test/status/next-route reading changed | refresh generated working projection | none |
| `portfolio` | Idea added, removed, merged, deferred, or reordered | refresh by stable `idea_id`; inspect shell impact | none unless a human asks for prose feedback |
| `structure` | authored P0 divisions or Page shape must change | route through the Page OUTLINE/SHAPE workflow | only if human review is required |

Ideation never sends `prose` as a sync change class: prose feedback is a
separate Page request and follows the normal Writing Step/Page Run contract.
Portfolio reordering must not silently renumber existing Page-global paragraph
identities. If a portfolio change alters the authored shell, the adapter stops
at the working projection and reports that a Page shape decision is open; it
does not release Content automatically.

## Projection law

- The Discovery Landscape summarizes accepted synthesis Pages and direct
  evidence ids; it does not copy Result Cards, facts, BibTeX, or raw notes.
- The Opportunity Map is Ideation's interpretation of how the landscape opens,
  narrows, contradicts, or exhausts candidate space. Each entry names evidence
  and affected Idea ids.
- Generate or Test may add, revise, merge, reorder, or recommend defer/abandon.
  Only an explicit I3 human receipt changes an admitted Idea to deferred,
  selected or eliminated; projected dispositions retain decision_ref.
  Provisional candidates not yet admitted may still be rejected or deduplicated.
  Every material change increments `sync_revision` and routes the changed
  packet to the same Paper P0 working projection rather than minting another
  portfolio; release of adopted Content remains governed by the Page barrier.
- A working projection is current only when its revision and source hash equal
  the sync packet and its normal Page workflow records a working receipt; this
  does not silently promote adopted Content or delivery to current.
- The sync operation is not a Page Run and does not mint `rpNN`. Do not create
  a local Ideation Run for it. If a human asks for bounded prose feedback on
  the P0 Page, that separate request follows the Page Run/Step contract.
- The sync packet never contains `decision`, `selected_cards`, `target_routes`,
  or `story_routes`. Those fields belong only to the I3 human selection receipt
  and final handoff.
- `portfolio_recommendation` is the canonical pre-decision machine artifact.
  Do not create a parallel `portfolio-recommendation.yaml`; updating the sync
  packet keeps the Paper cockpit and semantic source on the same revision.
- Paper P0 may display verdict, target, and `went to` only by projecting the I3
  receipt received in the final handoff. Page approval or CHECK is not an
  independent selection.
- If a later I2 revision changes an Idea that was already selected, preserve the
  existing I3 receipt and handoff as history. Mark the semantic/P0 projection
  current as applicable, but route the affected selection back through I3 for a
  new human decision; never auto-revoke, replace, or rewrite the old selection.
