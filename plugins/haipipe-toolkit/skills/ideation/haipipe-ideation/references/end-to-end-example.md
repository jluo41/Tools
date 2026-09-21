# End-to-end Ideation specimen

This synthetic specimen shows how the numbered capability families join. It
demonstrates artifact relationships; its sources and findings are placeholders,
not scientific claims.

## Starting direction

```text
Question       Can communication signals improve understanding of variation in
               a clinical decision after established patient/context factors?
Boundary       One defined clinician population, one decision outcome, one
               historical interval; no causal claim without an identification design.
Decision rule  Keep an Idea only if it has a material claim delta, an executable
               minimum experiment, and a plausible publication audience.
```

The bundle points to two completed Task Results (`int01`, `int02`) and three
verified Discovery Results (`ext01`–`ext03`). Their content remains with the
owners.

## 1 Generate

The signal map exposes a measurement opening, a contradiction across prior
studies, and an identification limitation. Generation deliberately uses
different lenses:

| Card | Lens | Falsifiable proposition | Minimum experiment | Initial states |
|---|---|---|---|---|
| `i01` | mechanism | communication signal M moderates the relation between context X and decision Y | add prespecified interaction M×X and compare held-out calibration | novelty unverified; pilot pending; venue pending |
| `i02` | measurement | representation R predicts Y beyond structured covariates | nested held-out model comparison | novelty unverified; pilot pending; venue pending |
| `i03` | boundary | the association between M and Y changes across setting Z | prespecified stratified estimate with interaction test | novelty unverified; pilot pending; venue pending |

`i02` and an alternative title are merged because their research question,
mechanism, setting, and outcome tuple are identical. The generation receipt
preserves that deduplication; it does not award a novelty score.

Generate also writes Paper sync revision 1. The evergreen P0 cockpit projects
the Direction, accepted Discovery synthesis pointers, current landscape,
Opportunity Map, and all three unverified Ideas before any Idea is selected.

## 2 Test

### Novelty

For `i01`, the search specialist freezes two Core Claims and routes the query
ladder through Discovery. The closest-work comparison is explicit:

| Delta component | Closest verified work | `i01` | Reading |
|---|---|---|---|
| research question | predicts decision Y from communication | asks whether M changes the X→Y relation | different |
| mechanism | representation as predictor | moderation mechanism | different |
| identification/setting | cross-sectional setting A | held-out setting B; still associational | partly different |
| outcome | decision Y | same Y | shared |

The receipt steelmans rejection (same outcome and communication family) and
defense (different mechanism and test). The Core Claim is `partial`, not
automatically `novel`. Identification remains a separate pressure-test axis.

`i02` is `preempted` after full-text review shows the same question, method,
setting, and outcome. `i03` remains `inconclusive` because the closest paper
could be verified only at abstract depth.

### Pressure test

| Card | Identification | Pilot | Fatal/repairable reading |
|---|---|---|---|
| `i01` | conditional | positive Task-owned receipt | causal language is fatal unless a design is added; associational framing is repairable |
| `i02` | strong | positive | scientifically executable but novelty is preempted |
| `i03` | unknown | pending | setting linkage and subgroup power remain open |

This is why novelty and feasibility are not collapsed into one score.

### Journal fit

All three cards retain a broad screen. Only `i01` receives deep fit because it
remains live:

| Target role | Target/category | Fit | Decisive condition |
|---|---|---|---|
| ambitious | multidisciplinary clinical journal / original research | conditional | broader validation and stronger identification |
| realistic | specialist digital-health journal / original research | strong | claim remains associational and validation is external |
| fallback | methods/application journal / research article | conditional | foreground measurement contribution |

Each named finalist resolves to a current Venue contract. The recommendation
does not select a target.

### Nature overlay

Because a Nature-family target is explicitly under consideration, the Nature
specialist reviews `i01`:

```text
broad significance       conditional
conceptual advance       conditional
evidence decisiveness    upgrade-required
generality               upgrade-required
figure-led claim shape   plausible
specialist reroute       likely
verdict                  specialist-reroute
```

The overlay recommends a specialist Nature-family route only if broader
validation lands. Current category and submission requirements still come
from the target's Venue contract, not from the overlay.

### Reconciled matrix

```yaml
kind: ideation-test-matrix
ideas:
  - idea_id: i01
    novelty: partial
    identification: conditional
    feasibility: positive
    journal_fit: strong
    nature_shape: specialist-reroute
    fatal_blockers: []
    repairable_gaps: [broader validation, causal-language boundary]
    next_route: select
  - idea_id: i02
    novelty: preempted
    identification: strong
    feasibility: positive
    journal_fit: weak
    nature_shape: not-requested
    fatal_blockers: [material claim already established]
    repairable_gaps: []
    next_route: abandon
  - idea_id: i03
    novelty: hold
    identification: unknown
    feasibility: pending
    journal_fit: unknown
    nature_shape: not-requested
    fatal_blockers: []
    repairable_gaps: [full-text closest-work review, linkage feasibility]
    next_route: defer
```

Test writes Paper sync revision 2 with this matrix and the machine-only
portfolio recommendation. The same P0 Page now shows why `i02` is headed
toward abandonment and why the machine recommends deferring `i03`; it creates neither a second
portfolio nor an independent human verdict.

## 3 Select

The machine recommends `i01` with caution, abandoning `i02`, and deferring
`i03`. A person then chooses the realistic specialist target for `i01`, names
the article category, accepts the associational-claim boundary, and records
the date and identity. The person also explicitly abandons i02 and defers i03;
these dispositions are not inferred from their absence from selected_cards.

```yaml
version: 3
kind: ideation-selection
ideation_task: b01.j01.t01
direction_card: cards/direction.yaml
decision: select
selected_cards:
- cards/i01_moderation.yaml
story_routes:
- card: cards/i01_moderation.yaml
  story_role: Story-A
  story_path: Paper-Example/A1-Story/StoryA-specialist-moderation/StoryA-specialist-moderation.md
target_routes:
- card: cards/i01_moderation.yaml
  venue_fit_card: cards/venue-fit/i01_venue-fit.yaml
  target: Specialist journal
  category: Original research
  venue_contract: shared-venue-bank/QBvN-specialist.md#versioned-contract
  contract_version: 2026-09-08.1
by: person:example
at: 2026-09-08 12:00:00-04:00
reason: Best balance of material delta, executable pilot, and current desk fit.
id: s01
snapshot: workflow/selections/s01.yaml
source:
  sync_revision: 2
  source_hash: sha256:<reviewed semantic source>
reviewed_cards:
- cards/i01_moderation.yaml
- cards/i02_prediction.yaml
- cards/i03_linkage.yaml
candidates:
- card: cards/i01_moderation.yaml
  disposition: select
  reason: Best balance of material delta, executable pilot, and current desk fit.
  posture: proceed-with-caution
  accepted_risks:
  - Do not make a causal claim without a new design
  assertions:
    evidence_complete: true
    novelty_reviewed: true
    feasibility_receipt_or_waiver: true
    venue_fit_reviewed: true
    target_selected: true
  target_route:
    venue_fit_card: cards/venue-fit/i01_venue-fit.yaml
    target: Specialist journal
    category: Original research
    venue_contract: shared-venue-bank/QBvN-specialist.md#versioned-contract
    contract_version: 2026-09-08.1
  story_route:
    story_role: Story-A
    story_path: Paper-Example/A1-Story/StoryA-specialist-moderation/StoryA-specialist-moderation.md
- card: cards/i02_prediction.yaml
  disposition: abandon
  reason: The person accepts the preemption evidence
- card: cards/i03_linkage.yaml
  disposition: defer
  reason: The person waits for full-text and linkage work
```

Save identical copies at workflow/selection.yaml and workflow/selections/s01.yaml.
Project each answered card and Venue Fit human_target using receipts.md; keep
machine recommendations separate. The handoff uses version 3, id s01 and
snapshot handoff/history/s01.yaml. It points to Paper sync revision 2 and its
source hash, this immutable human receipt, the Idea
Card, claim ids, owner Results, pilot receipt, Venue Fit Card, current Venue
contract, hard claim limits, and the planned Story route. Paper P0 projects
the receipt's verdict, target, and `went to` fields; it does not decide again.
The handoff copies none of those source artifacts.

## Run ownership for this example

The durable commission uses the portfolio Run Spec in workflow-runs.md, with
a Task-owned Execution Ticket/Result/runtime for this direction and snapshot.
The I1/I2/I3 sections above are its internal Steps. Existing source and pilot
Results are dependencies; only missing independently closable source/pilot
questions allocate their owner-native Runs. P0 projection and each specialist
lens do not create extra Runs. If i03 remains HOLD, the whole Test gate is not
complete, but selected-subset gates may still authorize i01.
