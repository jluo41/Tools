# Ideation receipts

These small records make the handoffs testable without turning Ideation into a
third evidence bank. They are written under the ideation unit’s `workflow/`
and `handoff/` lanes; source owners retain their own Runs and Results.

Capability-specialist receipts live under `workflow/generate/`,
`workflow/novelty/`, `workflow/pressure/`, and `workflow/nature/`. Their
canonical fields are defined by the numbered Ideation specialists. The Idea
Card and Venue Fit Card retain the current conclusion plus receipt path; they
do not duplicate the specialist's search coverage, adversarial comparison, or
pressure table.

## Assessment identity and review resolution

Every novelty, pressure, or Fit judgment must identify its evaluator, rubric
version, and frozen input snapshot. A specialist receipt uses this binding:

```yaml
assessment_binding:
  mode: owning_run | direct
  assessment_id: "unique id within the owning Result or direct invocation"
  owning_run: "bNN.jNN.tNN/rNN | null"
  # For mode=owning_run, evaluator, criterion and input hashes are inherited
  # from Task Result `assessments[assessment_id]`.
  evaluator: null  # required in direct mode: {actor, model_or_build}
  criterion: null  # required in direct mode: {id, version, owner}
  input: null      # required in direct mode: {subject_hash, manifest_sha256}
```

For a durable assessment, the owning Task Ticket freezes each assessment id,
evaluator identity (including model/build when agent-run), criterion/rubric id
and version, exact subject Card hash, and a hash of the sorted input manifest.
The same-stem Task Result indexes that immutable context and the specialist
receipt path/hash. The specialist receipt records the exact owning Run address
and assessment id; those fields inherit the remaining binding from that Run's
Result. This is a Task-owned evaluation Step, not a new Ideation Run.

For a direct or one-off assessment, set `mode: direct` and `owning_run: null`;
include the evaluator, criterion id/version/owner, exact Idea Card version or
content hash, and `manifest_sha256` over all evidence and contracts consulted.
For inline input, hash the exact received text/attachments and list them in the
manifest. Encode the manifest as a compact UTF-8 JSON array of
`[stable_locator, "sha256:<content hash>"]` pairs, sorted lexicographically by
locator, with no byte-order mark; `manifest_sha256` is SHA-256 of those exact
bytes. Use repo-relative paths for workspace files, canonical URLs plus access
dates for external sources, and `inline:<ordinal>` for inline content. If the
exact inputs cannot be identified, mark the evaluation
provisional/undetermined; do not invent a version. Return these fields inline
even when no durable file is requested. Saving a direct result uses a new
timestamped receipt path; never overwrite a prior assessment.

Each independent judgment is a separate immutable assessment. If more than one
exists, write a resolution receipt of the same specialist kind and canonical
shape, with this additive block:

```yaml
review_resolution:
  status: agreement | resolved | undetermined
  raw_reviews:
    - assessment_id: "..."
      receipt: "immutable reviewer receipt path or null for inline review"
      sha256: "sha256:<exact receipt bytes> or null for inline review"
      raw_judgment: "exact structured result when no receipt file exists"
  resolver: "person:<identifier> | null"
  rationale: "why the reviews agree or how the conflicting evidence was handled"
  outcome: "adjudicated conclusion or HOLD"
  next_route: "named evidence/rubric owner and missing input, or none"
```

Keep every raw review unchanged. `agreement` means the material conclusion is
the same; `resolved` requires a named resolver and evidence-based rationale;
`undetermined` requires a concrete next route and remains HOLD. Never average
reviewer labels or replace an earlier receipt with the resolution. The current
Idea Card/Fit projection points to the resolution receipt when one exists. An
undetermined novelty claim projects to `inconclusive`; unresolved pressure
projects identification to `unknown`; unresolved Fit dimensions and overall
status stay `unknown`, and human target stays `open`. A direct one-off with
multiple reviewers returns the same resolution block inline; it does not mint
a Run. These receipts and resolutions are evidence records, not Runs.

## Paper P0 projection receipts

`projection/paper-ideation-sync.yaml` is the I1/I2 adapter defined in
`manifest-and-sync.md`. It carries the evolving Discovery Landscape,
Opportunity Map, candidate portfolio, Test Matrix projection, and open gaps to
the same evergreen Paper P0 Page. It contains no human selection fields and
does not authorize a Story. Material Generate/Test changes increment its
revision and make the Page working projection stale until
`haipipe-paper-ideation` records the same revision through the Page update
boundary. The working Outline/preview/Bullet Workspace may be refreshed first;
that refresh is not a Page Run and does not publish adopted Content or
delivery.

The Page-owned return uses the normal receipt in the Page's
`workflow/receipts/` lane for each controller dispatch (serialized as `phase`). Ideation adds a
`paper_projection` extension inside that receipt; it does not create a second
Page receipt type or a parallel Page lifecycle:

```yaml
step: 1
round: 1
phase: OUTLINE | CONTENT
status: ok
paper_projection:
  source_packet: projection/paper-ideation-sync.yaml
  source_revision: 4
  source_hash: "sha256:<sync packet hash>"
  page_path: "Paper-.../A1-Story/Story00-ideation/...md"
  surface: working | release | delivery
  output_hash: "sha256:<surface output hash>"
  created_at: "ISO-8601"
```

The adapter is the only writer of the semantic sync packet, including its
nested `paper_page` surface state. The Page/Paper route is the only writer of
the standard dispatch receipt and its `paper_projection` extension. The adapter
reads that receipt on the next sync and records the corresponding state; Page
never edits the semantic packet directly. A `working` extension does not imply
`release` or `delivery`. A release extension must consume the same
revision/source hash as the working surface, and a delivery extension must
identify the released source. Replaying the same source revision and hash is
idempotent and does not allocate an `rpNN` Page Run.

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

## Human selection receipt (version 3)

Write new decisions as version 3. Each candidate has its own disposition;
unanswered candidates remain `open`. Machine recommendations never supply a
human disposition. `reviewed_cards` names exactly the candidate rows in this
review; cards outside that set keep their existing history.

~~~yaml
version: 3
kind: ideation-selection
id: s01
snapshot: workflow/selections/s01.yaml
ideation_task: bNN.jNN.tNN
direction_card: cards/direction.yaml
source:
  sync_revision: 2
  source_hash: "sha256:<reviewed semantic source>"
by: "person:<identifier>"
at: "2026-09-20T12:00:00-04:00"
reason: "The person's bounded portfolio decision"
reviewed_cards: [cards/i01_idea.yaml, cards/i03_idea.yaml]
candidates:
  - card: cards/i01_idea.yaml
    disposition: select
    reason: "Material delta and executable design"
    posture: proceed-with-caution
    accepted_risks: ["Keep the claim associational"]
    assertions:
      evidence_complete: true
      novelty_reviewed: true
      feasibility_receipt_or_waiver: true
      venue_fit_reviewed: true
      target_selected: true
    target_route:
      venue_fit_card: cards/venue-fit/i01_venue-fit.yaml
      target: "Specialist journal"
      category: "Original research"
      venue_contract: "shared-venue-bank/desk.md#versioned-contract"
      contract_version: "2026-09-20.1"
    story_route:
      story_role: Story-A
      story_path: "Paper-Example/A1-Story/StoryA/StoryA.md"
  - card: cards/i03_idea.yaml
    disposition: defer
    reason: "The person deferred pending full-text review"
# Compatibility projections, derived from candidates, never authored separately:
decision: select
selected_cards: [cards/i01_idea.yaml]
story_routes:
  - card: cards/i01_idea.yaml
    story_role: Story-A
    story_path: "Paper-Example/A1-Story/StoryA/StoryA.md"
target_routes:
  - card: cards/i01_idea.yaml
    venue_fit_card: cards/venue-fit/i01_venue-fit.yaml
    target: "Specialist journal"
    category: "Original research"
    venue_contract: "shared-venue-bank/desk.md#versioned-contract"
    contract_version: "2026-09-20.1"
~~~

For each row `disposition` is `select | defer | abandon | open`. Only selected
rows carry posture, risks, assertions, target_route and story_route. Use
`proceed | proceed-with-caution` for posture, with nonempty named risks for
caution. A person owns by/at, answered dispositions, reasons, target/category
and risk acceptance. An all-open draft is not a completed human decision.

The top-level decision is a compatibility summary: select when any row is
selected; otherwise defer when any row is deferred; abandon only when every
row is abandoned; otherwise open. This summary does not resolve open rows.
selected_cards and both route lists contain exactly the select rows; each route
is the corresponding nested route plus card. No global posture or risk list
overrides the per-card values.
When making this receipt current, project ideation.yaml stage to select and
state from its summary: select → selected, defer → deferred, abandon →
abandoned, open → open. The manifest is an index, not a second decision source.

Every selected card requires all Core Claims to be novel/partial, bounded
delta and risks, resolved identification, a positive/negative Task pilot or
reasoned waiver, complete broad/deep fit and its exact current Venue contract.
Machine next_route never substitutes for these eligibility checks. Other
candidates may retain truthful HOLDs; their unresolved tests do not block a
ready selected subset. --gate test still checks completion of the whole Test.

### Immutable history and projections

1. Reserve a new selection id; never reuse an existing id for changed answers.
   Write the immutable full record to workflow/selections/<id>.yaml and make
   workflow/selection.yaml an identical current view. The checker requires
   equality. Keep old snapshots and old handoffs; do not mutate both copies to
   conceal a changed decision.
2. Project each answered row to its Idea Card: select → selected,
   defer → deferred, abandon → eliminated; write decision_ref to that immutable
   selection. Open rows remain open and authorize nothing. Existing decisions
   outside reviewed_cards remain historical until explicitly reviewed again.
3. Project human_target in the Idea Card to selected/deferred/rejected/open.
   In an existing Venue Fit Card write exactly: status, selection_receipt (snapshot),
   target, category, venue_contract, contract_version, by, at,
   accepted_conditions (that row's accepted_risks). Nonselected answered rows
   use empty target/category/contract/version and an empty conditions list.
   An early defer/abandon does not require creating an absent Venue Fit Card;
   selected cards always require their complete fit artifact.
   Machine recommendation/recommended_target stay independent.
4. Refresh only these human projections in the sync/P0 view. They are excluded
   from the semantic source fingerprint; they do not change the evidence
   revision that the person reviewed. Evidence or recommendation changes do
   advance that revision and require a new decision before a new handoff.
5. Any mismatch is HOLD with the stale projection named. Never choose a value
   by file modification time. This describes G0 intended targets; later Story
   target rebinds remain Story-owned and do not rewrite the G0 history.

Legacy version-2 receipts remain readable. A named selected card plus matching
routes records only that selected card's decision. A global defer/abandon or
absence from selected_cards does not invent a per-card decision. Archive the
unchanged original before migration, and carry forward only explicitly
attributable answers. Missing scope or decisions require clarification.
Legacy shape alone cannot authorize a new ready handoff: it must satisfy the
same selected-card/target joins and supply the actual sync revision/hash.

## Paper P0 handoff (version 3)

~~~yaml
version: 3
kind: paper-ideation-handoff
id: s01
snapshot: handoff/history/s01.yaml
source:
  ideation_task: bNN.jNN.tNN
  direction_card: cards/direction.yaml
  evidence_bundle: bundle/evidence-bundle.yaml
  paper_ideation_sync: projection/paper-ideation-sync.yaml
  sync_revision: 2
  source_hash: "sha256:<reviewed semantic source>"
  selection_receipt: workflow/selections/s01.yaml
selected_ideas:
  - card: cards/i01_idea.yaml
    story_role: Story-A
    story_path: "Paper-Example/A1-Story/StoryA/StoryA.md"
    claim_ids: [c01]
    evidence_ids: [ext01]
    feasibility_receipt_or_waiver: "tasks/.../results/.../runtime.yaml"
    venue_fit_card: cards/venue-fit/i01_venue-fit.yaml
    intended_target: "Specialist journal"
    intended_category: "Original research"
    venue_contract: "shared-venue-bank/desk.md#versioned-contract"
    contract_version: "2026-09-20.1"
    selection_posture: proceed-with-caution
    accepted_risks: ["Keep the claim associational"]
    hard_limits: ["No causal claim"]
paper_route: haipipe-paper-ideation
status: ready
created_at: "2026-09-20T12:05:00-04:00"
~~~

The handoff uses the selection id and pins its immutable snapshot plus the
current I2 semantic sync revision/hash. Version-3 selection and handoff require
a version-2 sync with an existing P0 Page and a current working projection
backed by its Page dispatch receipt. A legacy version-1 current flag alone
cannot establish this; Content release and delivery may still be stale.
Store an identical immutable copy in
handoff/history/<id>.yaml; handoff/paper-ideation.yaml is the current view.
Emit it only after --gate select and --gate handoff pass. The selected set,
per-card target/category/contract version, risk posture and distinct physical
Story paths must equal the person's receipt, including when machine advice
suggested a different route.

claim_ids includes every current Core Claim exactly once. evidence_ids resolves
to the bundle and includes the claims' support. The feasibility pointer equals
the card's Task receipt or its #feasibility.waiver anchor. Venue Fit and contract
pointers identify the artifacts actually reviewed. hard_limits is an explicit
list, which may be empty when no additional limits apply. Do not copy source
text, BibTeX or venue rules.

The I3 receipt is the sole human authority; its current view and snapshots are
versions of that authority. Page approval/CHECK does not create another
selection. Preserve inherited Story paths and their canonical roles; do not
rename them to satisfy an example. One selected Idea maps to one distinct
Story, even when two role labels would otherwise name the same physical path.

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
