# Ideation receipts

These small records make the handoffs testable without turning Ideation into a
third evidence bank. They are written under the ideation unit’s `workflow/`
and `handoff/` lanes; source owners retain their own Runs and Results.

Stage-specialist receipts live under `workflow/generate/`,
`workflow/novelty/`, `workflow/pressure/`, and `workflow/nature/`. Their
canonical fields are defined by the numbered Ideation specialists. The Idea
Card and Venue Fit Card retain the current conclusion plus receipt path; they
do not duplicate the specialist's search coverage, adversarial comparison, or
pressure table.

## Paper P0 working-state sync

`projection/paper-ideation-sync.yaml` is the I1/I2 adapter defined in
`manifest-and-sync.md`. It carries the evolving Discovery Landscape,
Opportunity Map, candidate portfolio, Test Matrix projection, and open gaps to
the same evergreen Paper P0 Page. It contains no human selection fields and
does not authorize a Story. Material Generate/Test changes increment its
revision and make the Paper projection stale until
`haipipe-paper-ideation` records the same revision.

## Discovery search request/return

```yaml
version: 1
kind: discovery-search-request
id: sr01
question: "the exact external question"
discovery_type: source-map | source-reading
channels:
  required: [preprint, journal-index]
  optional: [semantic-scholar, openalex, gemini-search]
acceptance: "identity, relevance, reading depth, and Bib requirements"
status: requested | returned | blocked
requested_at: "2026-09-07T12:00:00-04:00"
discovery_task_path: "../../discoveries/bNN_.../jNN_.../tNN_..."
returned_results:
  - address: bNN.jNN.tNN.rNN
    result_path: "../../discoveries/.../results/rNN_.../rNN_....md"
    bib_path: "../../discoveries/.../results/rNN_.../rNN_....bib"
    runtime_path: "../../discoveries/.../results/rNN_.../runtime.yaml"
    cite: "@CanonicalKey"
    status: complete | blocked | unresolved
unresolved_gap: ""
returned_at: "2026-09-07T12:30:00-04:00"
```

The request is a consumer-side receipt. Do not put `consumer`, `parent`, or
ideation paths into `discovery.yaml`; Discovery remains consumer
unaware. A returned result is usable only after the bundle’s direct Result,
Bib, Card, runtime path, and `bib.verification` checks pass.

If the request reuses a Discovery Task, record its path and exact reused Result
addresses. If the question or acceptance contract changes materially, open a
new Discovery Run under the owner’s supersession rule rather than editing the
old receipt.

## Human selection receipt

```yaml
version: 2
kind: ideation-selection
ideation_task: bNN.jNN.tNN
direction_card: cards/direction.yaml
decision: select | defer | abandon
selection_posture: proceed | proceed-with-caution | not-applicable
selected_cards: [cards/i01_idea.yaml]
story_routes:
  - card: cards/i01_idea.yaml
    story_role: Story-A
    story_path: "Paper-.../A1-Story/Story-A/Story-A.md"
target_routes:
  - card: cards/i01_idea.yaml
    venue_fit_card: cards/venue-fit/i01_venue-fit.yaml
    target: "Journal name"
    category: "article type"
    venue_contract: "shared venue bank/.../QBvN-....md#versioned-contract"
by: "person:<identifier>"
at: "2026-09-07T13:00:00-04:00"
accepted_risks:
  - "risk accepted for the selected card"
assertions:
  evidence_complete: true | false
  novelty_reviewed: true | false
  feasibility_receipt_or_waiver: true | false
  venue_fit_reviewed: true | false
  target_selected: true | false
reason: "bounded decision rationale"
```

`PROCEED` maps to `decision: select` plus `selection_posture: proceed`.
`PROCEED WITH CAUTION` maps to `decision: select` plus
`selection_posture: proceed-with-caution` and requires at least one named
`accepted_risks` entry. `ABANDON` maps to `decision: abandon`; an open or
deferred verdict maps to `decision: defer` until a person changes it.

Only `decision: select` with all five assertions true can produce a Paper
handoff. Every selected card has exactly one distinct `story_routes` entry,
one matching `target_routes` entry, and resolved Core-Claim
`novelty_check.status` values (`novel` or `partial`; never `unverified`,
`inconclusive`, or `preempted`). Its Venue Fit Card must have a complete broad
screen, complete deep fit, and a human-selected target/category backed by the
named current Venue contract. Selection may name several cards, but it does
not declare one global winner; each selected card becomes one Story with its
own intended target.
`defer` and `abandon` remain durable history and do not authorize Paper work.
The machine may prepare this record, but a person owns `by`, `at`, `decision`,
`selection_posture`, every `target_routes` value, and accepted risks.

## Paper P0 handoff

```yaml
version: 2
kind: paper-ideation-handoff
source:
  ideation_task: bNN.jNN.tNN
  direction_card: cards/direction.yaml
  evidence_bundle: bundle/evidence-bundle.yaml
  paper_ideation_sync: projection/paper-ideation-sync.yaml
  selection_receipt: workflow/selection.yaml
selected_ideas:
  - card: cards/i01_idea.yaml
    story_role: Story-A
    story_path: "Paper-.../A1-Story/Story-A/Story-A.md"
    claim_ids: [c01, c02]
    evidence_ids: [int01, ext01]
    feasibility_receipt_or_waiver: "tasks/.../results/.../runtime.yaml or cards/i01_idea.yaml#feasibility.waiver"
    venue_fit_card: cards/venue-fit/i01_venue-fit.yaml
    intended_target: "Journal name"
    intended_category: "article type"
    venue_contract: "shared venue bank/.../QBvN-....md#versioned-contract"
    hard_limits: ["what Paper must not claim"]
paper_route: haipipe-paper-ideation
status: ready
created_at: "2026-09-07T13:05:00-04:00"
```

The handoff contains IDs, owner paths, statuses, interpretations, novelty
readings, feasibility receipt/waiver, Venue Fit/contract paths, human-selected
target/category, latest Paper sync revision, and hard limits. It contains no
copied Result Card, venue rule, facts, or BibTeX. Paper P0 maps it to Direction, Ideas, Core
Claims, Pilot result, Journal / Venue Fit, Recommendation, Eliminated Ideas,
and the human target plus `went to` decision, then binds its Paper origin back
to this packet.

`workflow/selection.yaml` is the sole human decision authority. Paper P0
projects its verdict, target, and `went to` values from the final handoff; Page
approval and Page CHECK cannot create a second decision or override the
receipt.

For an inherited Story such as `Story01-seed`, keep that path and record its
canonical role in `story_role`. G0 requires reciprocal origin links, not a
filesystem rename. Historical `pagex/` links are navigation/evidence only and
cannot stand in for this selection receipt.

## Receipt checks

- every referenced path exists and resolves to the stated owner;
- every source address is full BJTR and every Discovery Result/Bib/runtime trio
  is same-stem with one matching Bib key and a verified `bib.verification`
  receipt;
- every Core Claim has a `novelty_check` containing a search question, closest
  work or explicit none, steelmanned rejection and defense, four-part delta
  tuple, evidence depth, remaining delta, limitation, specialist receipt, and
  a resolved status for a selected card;
- novelty and identification credibility are reported as separate axes, with
  the pressure receipt linked from the Idea Card;
- feasibility has the required receipt or reasoned waiver;
- every admitted Idea has a broad Venue screen; each selected card has complete
  deep fit, a current Venue contract, and a human-selected target/category;
- selection and handoff contain a person/date; each selected card has one
  distinct Story route and one matching target route; the handoff is emitted
  only for selected cards whose idea and target gates both pass.
- the latest Paper P0 sync packet resolves, its revision is not stale, and it
  contains no independent selection fields.
