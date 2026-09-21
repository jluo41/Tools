# Idea × Venue Fit

Venue fit is an evidence-bound comparison between one Idea Card and one or
more plausible publication targets. It is not a prestige score, an acceptance
prediction, or permission for the machine to choose a journal.

## Two-pass protocol

Every admitted Idea Card receives a broad screen. Deep fit is reserved for
candidates that remain live after novelty and feasibility pressure-testing.

```text
all admitted ideas
  └─ broad screen: field · audience · contribution · method/evidence shape ·
                   article type · obvious desk mismatch
       ├─ off-fit / eliminated → retain the screen and reason
       └─ live candidate → deep fit against current venue contract(s)
                              └─ machine recommendation → human target decision
```

The broad screen may identify a journal family or named candidate from
verified scope material. It does not need a full Venue Page for every weak
idea. Deep fit normally compares a small defensible set and requires a current
versioned `haipipe-paper-venue` contract for every named finalist. When useful,
label candidates `ambitious`, `realistic`, `fallback`, or `reroute`; these are
portfolio roles, not rankings or acceptance probabilities.

## Authority

Use the Venue Page authority vocabulary without modification:

- `DESK RULE`: current official target material, with source and access date;
- `PACK OBSERVATION`: measured exemplar pattern, explicitly nonbinding;
- `PACK PRESCRIPTION`: playbook or external skill guidance without enough
  direct observations;
- `LOCAL DECISION`: this project's interpretation or target choice; and
- `UNKNOWN`: a visible gap with a refresh route; and
- `OWN ESTIMATE`: a local estimate with its basis and uncertainty, explicitly
  not a desk rule. Use only when the candidate assessment needs an estimate
  that is neither established by official material nor a pack observation.

`OWN ESTIMATE` is a Venue authority value and must be preserved unchanged in
Fit. Do not translate it to `LOCAL DECISION`: the former estimates an uncertain
fact, while the latter records a project's chosen interpretation or target.

Journal skill packs, remembered policies, static rankings, and search snippets
may suggest candidates. They are never `DESK RULE`. Volatile claims such as
scope, article types, limits, fees, timelines, data/code rules, and submission
requirements must resolve through current official-source Discovery Results or
a current Venue Page contract backed by those Results. Do not invent or infer
acceptance odds from journal reputation.

## Required shape

One fit card belongs to one Idea Card:

Each immutable assessor snapshot uses this shape with its own non-null
`assessment_binding`. The current Fit Card is a projection: copy that binding
only when one assessment supports the projection; when multiple judgments
contribute, keep the field null, list every raw snapshot and exact-byte hash in
`assessment_receipts`, and point `review_resolution` to the resolution receipt
and hash. Those links preserve reviewer identity, rubric version and frozen
inputs without implying a single reviewer authored the combined result.

```yaml
version: 2
kind: idea-venue-fit
id: i01-venue-fit
idea_card: ../i01_idea.yaml
assessment_binding: null  # one raw assessment's binding; null when several are projected
assessment_receipts:
  - assessment_id: "e01"
    receipt: "workflow/venue-fit/i01_<timestamp>.yaml"
    sha256: "sha256:<exact receipt bytes>"
review_resolution: null  # {receipt, sha256} for multiple judgments; null for one
broad_screen:
  status: complete | pending
  field: "..."
  target_audience: "..."
  contribution_type: "conceptual | empirical | methodological | resource | review | other"
  method_shape: "..."
  evidence_shape: "..."
  likely_article_type: "..."
  submission_goal: "..."
  candidate_families: ["..."]
  excluded_families:
    - family: "..."
      reason: "..."
      evidence: [ext01]
candidates:
  - id: v01
    target: "Journal name"
    category: "article type or submission category"
    portfolio_role: ambitious | realistic | fallback | reroute
    profile: broad-screen | deep-fit
    venue_contract:
      status: not-required | missing | current | partial | stale | legacy-unclassified
      source_id: null
      path: null
      version: null
      refreshed_at: null
    dimensions:
      scope_audience:
        status: strong | conditional | weak | off-fit | unknown
        reason: "..."
        authority: DESK RULE | PACK OBSERVATION | PACK PRESCRIPTION | LOCAL DECISION | UNKNOWN
        evidence: [ven01]
      contribution_significance:
        status: strong | conditional | weak | off-fit | unknown
        reason: "..."
        authority: "..."
        evidence: [ext01, ven01]
      novelty_delta:
        status: "..."
        reason: "..."
        authority: "..."
        evidence: [ext01]
      method_and_design:
        status: "..."
        reason: "..."
        authority: "..."
        evidence: [int01, ven01]
      evidence_floor:
        status: "..."
        reason: "..."
        authority: "..."
        evidence: [int01, ven01]
      article_type:
        status: "..."
        reason: "..."
        authority: "..."
        evidence: [ven01]
      generality_and_impact:
        status: "..."
        reason: "..."
        authority: "..."
        evidence: [int01, ext01, ven01]
      compliance_and_openness:
        status: "..."
        reason: "..."
        authority: "..."
        evidence: [ven01]
    nature_overlay:
      status: not-requested | complete | hold
      receipt: null
      verdict: null
    overall: strong | conditional | weak | off-fit | unknown
    desk_risks: ["..."]
    missing_evidence: ["..."]
recommendation:
  target: "Journal name or unresolved"
  category: "article type"
  overall: strong | conditional | weak | off-fit | unknown
  reason: "bounded synthesis, not an acceptance prediction"
  alternatives: [v02, v03]
human_target:
  status: open | selected | deferred | rejected
  selection_receipt: null  # immutable I3 snapshot after an answer
  contract_version: ""
  target: ""
  category: ""
  venue_contract: ""
  by: ""
  at: ""
  accepted_conditions: []
updated_at: "2026-09-07T13:00:00-04:00"
```

For `profile: broad-screen`, `venue_contract.status: not-required` and null
contract fields are valid; its dimensions may cite verified scope evidence
directly. Promoting that candidate to `deep-fit` changes the status to
`missing` until a contract passes the currentness test. Null fields are never
silently treated as current.

The listed dimensions are the default comparison surface. Add a
discipline-specific dimension only when it changes the decision; do not create
a numeric composite score that hides an off-fit or unknown requirement. Apply
these anchors to each dimension and cite the evidence that meets the anchor:

- `strong`: current evidence directly supports the stated fit; no material
  unresolved caveat remains.
- `conditional`: the fit is supported if one or more named, verifiable
  conditions are satisfied; state each condition and its owner.
- `weak`: evidence shows a material mismatch, but a plausible, specific
  repair exists and has not yet been demonstrated. Name the repair and what
  evidence would show that it worked.
- `off-fit`: cited binding evidence establishes an incompatibility that cannot
  be repaired within the declared project constraints. Name the constraint
  and why each plausible repair is unavailable.
- `unknown`: evidence is missing, inaccessible, or materially conflicting, so
  the dimension cannot yet be assessed. Name the missing input or resolver.

Derive the overall summary without averaging: `off-fit` if a decision-critical
dimension has a proven, unrepairable incompatibility; otherwise `unknown` if a
decision-critical dimension is unknown; otherwise `weak` if any such dimension
is weak; otherwise `conditional` if any such dimension is conditional;
otherwise `strong`. A human may still choose to defer, repair, or reroute an
off-fit candidate; the summary does not authorize selection or rejection.
`unknown` stays open and routes to Discovery or Venue refresh. A non-decisive
dimension may be excluded from the overall rule only when the reason and
project constraint are recorded on the card.

`nature_overlay` is populated only when a Nature-family target is actually
under consideration. Its receipt comes from `haipipe-nature-paper-review` and
evaluates editorial shape; binding target/category rules still resolve through
the candidate's current Venue contract. A generic Nature-brand intuition is
not a completed overlay.

## Currentness and legacy migration

A contract is `current` only when the Venue Page exposes the machine-readable
contract block required by `haipipe-paper-venue`, its state is `current`, its
target/category match this candidate, its named official-source Results
resolve, and no blocking unknown invalidates the fit dimension being used.
`partial`, `stale`, `superseded`, or absent blocks cannot close deep fit.

A legacy QB page, archived desk note, project README, folder name, or prior
Narrative is a lead until migrated. Retype inherited prose statement by
statement under the Venue authority vocabulary, retain the original locator,
and mint a checked contract block; never infer currentness from a file's
existence, modification time, or prior use. A visibly `PARTIAL` page can seed
the broad screen and refresh request but not a target-selection gate.

## Selection and change control

human_target is a read-only projection of one per-card I3 decision, using the
exact mapping in [receipts.md](receipts.md#immutable-history-and-projections).
Its by/at, intended target/category, contract version and accepted_conditions
come from that receipt. Recommendation fields remain machine advice. A mismatch
is a handoff HOLD; never repair it by independently changing the human target.

A selected Idea may leave Ideation only when its broad screen and deep fit are
complete, every candidate marked `profile: deep-fit` has a current Venue
contract, and a person has
selected one intended target/category or explicitly deferred the entire Idea.
Deferral does not authorize Paper handoff. The target can change later, but
only through a new human receipt and a refreshed Story/Venue binding; never
silently rewrite the historical fit card.
