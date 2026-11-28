# Meaning and approval contract review

Reviewer: delegated Meaning-contract reviewer. Reviewed 2026-10-27. Scope: the six assembled documents under `/private/tmp/labeling-implementation-plan/`; read-only review, no production implementation or tests. The package was being revised concurrently; findings below use section names as stable references and account for the updated submission replay protocol in CONTRACTS section 13.

## Disposition

Approve the architecture and bounded synthetic M1 direction. Before the R1/T01 interface freeze, resolve findings M1–M3 below. They are contract gaps, not evidence that an implemented service is defective. They do not require stopping planning or changing the selected `J/meaning/` architecture. The later complete Meaning implementation must not be called accepted until their specified negative/recovery tests pass.

The coordinator's choices are sound: keep new reports in `J/meaning/`, preserve legacy item rounds, treat clear explicit submission of an exact visible patch as scoped approval, retain historical prototype exports as `rule_preference_only`, and require confirmation only when custom or qualified text needs operational reinterpretation.

## M1. Confirmed source authority must be derived from a real approval event

Severity: important, resolve before T01 freeze.

Locations: CONTRACTS section 3 `SourceRecord.authority`; section 11 `collect_source`; PLAN section 5 Meaning writes; WORK-PACKAGES T07/T09/T10.

The source schema currently permits `authority: confirmed_decision`, while the collector accepts source text/reference and provenance. The prose correctly prohibits the agent from manufacturing an attestation, but the contract does not explicitly require a valid approval-event reference before a SourceRecord may claim confirmed authority. A source importer or model-generated record could therefore satisfy structural validation while laundering an ordinary chat excerpt into a confirmed decision. The same gap affects sources imported from legacy labels or the form prototype.

Smallest fix: specify that source collection creates only context/proposed-preference records. `confirmed_decision` is a derived projection requiring an existing, authorized, immutable approval event with matching actor, exact decision scope and versions. Add `approval_event_ref` and validate it through the authority store. An imported document or caller-supplied enum cannot create that event. Explicit supplemental chat approvals, if supported later, must pass the same trusted adapter and exact-scope checks; otherwise chat remains evidence to confirm in the form. Apply the same authority check to `approve_reference_items` so a model cannot invoke a function with a fabricated reviewer ID and create gold.

Tests: (1) collect a source whose payload says confirmed_decision without an approval event and reject/downgrade it; (2) reference an approval from another job or another rule and reject it; (3) reference a valid exact patch submission and derive precisely that authority; (4) import prototype preference-only feedback and preserve its narrow scope; (5) import an unambiguous-looking chat statement through a non-authoritative source path and ensure it does not become approved automatically.

## M2. Integration needs its own atomic release protocol

Severity: important, resolve before T01/T02 freeze; acceptance required for T09–T11.

Locations: CONTRACTS sections 1, 8, 13 and 14; WORK-PACKAGES T02 `commit_integration`, T09 and T11.

The submission protocol is strong: immutable bundle plus outbox, atomic rename, receipt replay and rebuildable indexes. Integration then promises a receipt and no duplicate semantic patch, but it updates a wider graph: approved meaning, compatible reference membership/exclusions, dependency invalidations and release/current projections. These outputs occupy different directories. A crash after advancing the meaning pointer but before recording reference invalidation or the integration receipt can expose an incoherent approved pair or reapply the patch on recovery. Atomic submission alone does not address this failure.

Smallest fix: define an immutable integration transaction containing its expected prior release, exact approved decision refs, new semantic release, compatible reference selection/exclusions and invalidation events. Write complete immutable artifacts first, then publish one authoritative release descriptor/commit record binding them atomically under the job lock. Current/view pointers are rebuildable projections of committed release records. A prepared-but-uncommitted transaction cannot become visible as approved. Recovery completes the same integration or leaves the prior committed release active. If no compatible references remain, release meaning with an explicit pending-reference state and block scoring; do not invent approved labels to complete the pair.

Tests: crash before artifact completion, after artifacts but before commit, after commit but before indexing, and after indexing but before acknowledgement. Every reader sees either the prior coherent release or the new coherent release. Retrying the same integration creates neither another semantic version nor duplicate invalidation. An affected reference remains excluded until its explicit review/compatibility decision is recorded.

## M3. Partial submissions require per-decision answer identity and supersession

Severity: important, resolve before T01/T02 freeze.

Locations: CONTRACTS sections 6, 9 and 13; PLAN section 7; WORK-PACKAGES T05/T09/T11.

Request-level replay is correctly scoped to job and actor, and integration retry is keyed by submission. The UI also supports partial submission, later editing and a new draft. It is not yet specified whether a later submission includes all visible answers or only newly answered cards, nor how already integrated answers are recognized across different submission/request IDs. A human can submit card A, return to answer card B, and submit a form that still contains A. An implementation keyed only by the second submission can reapply A, create another version, or mistake it for a preference reversal. The state machine also needs to distinguish a card intentionally revising an approved answer from a previously deferred card being answered for the first time.

Smallest fix: assign each submitted card answer an immutable answer identity/revision bound to report revision and decision ID, plus optional `supersedes_answer_ref`. Define submission as a set of answer events; unchanged previously submitted answers may be included only as references/no-ops. Integration idempotency applies at answer/decision scope as well as submission scope. A changed choice or qualifying comment creates a new event and follows explicit supersession/conflict review; it never overwrites or silently retracts the earlier approval. Selecting defer or leaving unanswered cannot revoke an already applied decision. Keep dependency checks scoped to affected rules so unrelated approved branches can continue.

Tests: (1) submit A, later submit B while A is still visible, and apply A once; (2) resubmit identical A under a fresh request ID and create no second patch; (3) change A after integration and preserve both decisions with explicit supersession handling; (4) add a qualifying comment after integration and create a new pending issue rather than mutating old scope; (5) resolve a formerly deferred B without reopening A; (6) two concurrent submissions for the same card with conflicting answers remain inspectable and do not silently last-write-win.

## M4. Minor version and readiness clarifications

Severity: useful clarification, not a blocker for M1.

Locations: PLAN section 8; CONTRACTS sections 1 and 8; WORK-PACKAGES T10/T14.

The plan names semantic snapshots `mNN` and stores approved releases under `policy/versions/G_NN`. State the exact mapping: one `G_NN` manifest identifies one `meaning_version`, or choose one canonical counter and make the other a presentation label. Also make an approved principle without reviewed examples a valid state. It is approved-but-not-yet-supported for evaluation, not a reason to fabricate example labels. Expression development may begin with the approved rule, but executor qualification requires sufficient compatible approved references and disclosed support. If T14 uses T10's operational reference builder rather than pure contract fixtures, add T10 as a dependency; its current pure-validator preparation can proceed under T01.

## Confirmed strengths and scoped approval

The Meaning architecture correctly treats both rough ideas and legacy labels as entry cases to the same workflow. Human original wording and agent interpretation are separate. Legacy labels are evidence rather than automatic references. Only learning case details develop meaning. Protected adjudication and executor access are separate from development. Existing `definition_discussion` and first-round-only calibration are treated as limited legacy APIs rather than silently broadened services.

Diagnostics correctly distinguish substantive task labels, ambiguity, review effort, uncertainty reasons, model confidence and next actions. Unknown values remain representable. The design does not force H/L/N onto new tasks. Rule approval, directly reviewed references and audit-accepted production labels are distinct. Semantic changes invalidate dependent references, expressions and claims rather than erasing history.

Engineering ownership is workable: A owns Meaning contracts/store/integration; B owns renderer and route; C owns custody/evaluation/executor work; R owns shared integration files and final acceptance. T00–T05 is a useful bounded vertical slice. No additional autonomous runtime agents are required simply to implement the internal helpers. Later model Runs remain separately authorized, and planned scientific benefits are not presented as measured results.

No further architectural blocker found in the reviewed scope. This is plan approval conditional on the above contract clarifications, not production approval or a statement that new code/tests exist.

## Resolution review after coordinator amendments

Reviewed the amended CONTRACTS sections 3, 6, 8, 11 and 13 and WORK-PACKAGES T07/T09/T10/T14 on 2026-10-27. All three required findings are resolved at specification level, and the optional M4 clarification is addressed.

- M1 resolved: confirmed source authority requires committed scoped approval references; collection cannot self-confirm; reference approval explicitly requires committed scoped events and an authorized actor.
- M2 resolved: the integration transaction publishes its complete semantic release through one final commit manifest; compatible references, exclusions, invalidations and outcomes are bound together; recovery and reader visibility are specified and fault-injection acceptance is assigned to T09.
- M3 resolved: answer identity/revision and decision-effect history prevent reapplying an unchanged answer under a new request; edited answers retain supersession/conflict lineage; repeated partial submission tests are explicit.
- M4 resolved: G_NN maps explicitly to mNN; pending or partial references are valid but do not support scored claims; T14 now depends on T10.

Verdict: approve the amended plan within this review's Meaning/approval/asynchrony/reference scope. No outstanding blocker in that scope. Implementation still requires the assigned tests and coordinator review; this verdict is not implementation or production acceptance.

Small implementation note, not a new planning gate: distinguish the exact source payload revision that the person approved from the new derived source revision that records confirmed authority. An approval of source v1 can support a checked v2 authority projection only while v2 explicitly preserves its approved v1 payload/scope lineage. Do not require an impossible prior approval of a revision that integration itself has not created yet, and do not use the projection to approve changed source text.
