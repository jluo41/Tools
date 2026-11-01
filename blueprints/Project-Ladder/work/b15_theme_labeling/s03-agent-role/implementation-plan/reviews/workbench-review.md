# Workbench specialist review of assembled implementation plan

Review date: 2026-10-27. Scope: PLAN.md, CONTRACTS.md, WORK-PACKAGES.md, DELEGATION-AND-REVIEW.md, REVIEW.md and the evaluation sections governing UI evidence. Read-only document review against the earlier verified source audit. No production changes, servers, model Runs or new acceptance tests.

## Assessment

The architecture is feasible within the existing Workbench. J/meaning/ isolation, engine-only publication/integration, one browser write door, the new-mode renderer, explicit local attestation and disabled external responses until scoped authorization exists are coherent. The plan correctly permits approval of an exact displayed patch while preserving the prototype's narrower preference-only history.

Resolve the following contract defects before freezing T01/T02. They require small specification changes, not a different architecture.

## F1. Important: idempotency lookup must precede mutable revision checks

Location: CONTRACTS.md section 13, transaction steps 2–3; WORK-PACKAGES.md T02.

The transaction first compares current draft/report revisions and then looks up request_id. A committed submission can lose its response, after which another tab edits the draft or the report becomes superseded. Retrying the original request would now fail its revision check before the server discovers its successful original commit. That contradicts the promised same-request/same-payload receipt behavior.

Smallest fix: after resolving the job and currently authorized actor, look up an actor/job-scoped request ID first. If committed, compare the normalized immutable request envelope and return the original receipt or a request-ID conflict. Only new requests undergo current draft/report/meaning precondition checks. Do not reconstruct a replay comparison from a now-mutated draft. Authorization revocation may still forbid receipt access, but must not erase the committed record.

Acceptance: commit a submit while dropping its response; advance the draft and supersede the report; retry the unchanged original request and receive the same receipt. Changed reuse still returns 409. A different actor cannot retrieve that receipt by guessing its request ID.

## F2. Important: immutable records need an explicit separate lifecycle projection

Location: CONTRACTS.md sections 5–6, 9 and 13; WORK-PACKAGES.md T02/T09/T11.

Published reports and submitted bundles are immutable, but those same record descriptions include advancing status fields such as integrating/applied/failed and report submitted/resolved. Integration receipts and rebuildable indexes are mentioned, yet the authority for these transitions is not specified. Two agents could reasonably implement either in-place status mutation or incompatible separate state stores.

Smallest fix: explicitly define published report status and submission status in their immutable snapshots as the state at publication/receipt. Store later lifecycle transitions in append-only versioned events or immutable integration receipts, including event identity, sequence and parent reference. The UI returns a derived current_status alongside the immutable payload. Name the canonical event/receipt location under J/meaning/ and make the projection rebuildable. Preserve comments, selected patches and submission contents byte-for-byte after commit.

Acceptance: receipt and published-report source remain unchanged through integration, failure and restart; delete derived indexes and reconstruct the same current UI state from authoritative committed records.

## F3. Important: the answer schema omits the required “none” state

Location: CONTRACTS.md section 6 HumanDraft/HumanSubmission; section 5 DecisionCard; WORK-PACKAGES.md T03/T08; DELEGATION-AND-REVIEW.md Agent B prompt.

The UI and report planner require none/custom/defer and explicitly distinguish deferral from rejection. HumanDraft allows selected_option_id | custom | defer | null, and per-card disposition allows chosen | custom_proposal | deferred | unanswered. There is no specified representation for rejecting all offered options without offering a replacement. Implementations could incorrectly conflate this with custom text, deferral or unanswered.

Smallest fix: add a distinct none/reject_options answer kind and disposition, or define a stable explicit none option with equally explicit rejection semantics. Define whether an explanatory comment is required by the card, independently of custom-answer requirements. The integrator keeps the question unresolved and does not infer a new rule.

Acceptance: none without a replacement, custom with text, defer and unanswered survive save/reload/submit as four distinct states; no rejected card applies a semantic patch.

## F4. Important before T04: assign the host boundary if enforcing payload limits there

Location: CONTRACTS.md section 12 response code 413; WORK-PACKAGES.md T04; DELEGATION-AND-REVIEW.md section 2.

The earlier audit verified that the host reads/parses the request body before LabelingMixin.labeling_act dispatch. A form-specific 413 returned only after parsing does not bound the size read into memory. T04 currently assigns labeling.py but does not identify who owns a required pre-parse host guard. This is a limited ownership/integration gap, not a reason to redesign authentication.

Smallest fix: explicitly assign the coordinator the narrow _host/serve.py request-size guard, or state and verify an existing pre-parse bound that applies to this endpoint. B can continue owning action-level validation. Define malformed/negative/non-numeric Content-Length and oversized-body behavior; preserve existing unrelated endpoints and their legitimate limits. Keep shared external responses disabled as already specified.

Acceptance: endpoint-specific oversized requests fail before JSON decoding/body allocation beyond the configured bound; normal legacy labeling and permitted image-note requests remain compatible.

## Minor consistency corrections

- CONTRACTS.md section 12 names decision_reports_view.py; WORK-PACKAGES.md T03 names decision_report_view.py. Choose one before file assignment.
- PLAN.md section 4 says its paths are relative to Tools but lists skills/2_theme/... and servers/... without plugins/haipipe-toolkit/. Its sharing source is _host/live/share.py, not _host/share.py. Use the E/W/H abbreviations or complete verified source-relative paths.
- REVIEW.md section 5 leaves the first deployment's audience open, while PLAN.md section 12 correctly fixes M1 to a trusted local operator. Reword the remaining choice as the deployment after M1.

## Scoped approval after correction

Approve the overall Workbench integration direction and the synthetic M1 work split, contingent on F1–F3 being resolved in the frozen contracts and F4 receiving an explicit owner before T04. No redesign of J/meaning/, the route, the approval model or the two-agent architecture is needed. This review does not approve production identity, external participant access or deployed browser behavior; those remain the plan's explicit implementation gates.

## Resolution verification

Re-read the coordinator's changed sections on 2026-10-27. F1–F4 are resolved at specification level: actor/job-scoped committed replay now precedes mutable version checks; immutable lifecycle events and derived current_status are explicit; rejection has a distinct persisted answer/disposition and no-patch semantics; R owns the host pre-parse guard while B retains action validation. T02/T04 acceptance requirements cover the corresponding failures. The source paths, singular renderer filename and post-M1 deployment wording are corrected.

Scoped approval: the revised Workbench contracts and synthetic M1 assignments are ready for implementation. No remaining blocking finding in the reviewed changes. This is document approval only; persistence, authentication, browser behavior and external-user access still require the planned tests and demonstrations. No production edits or model Runs were performed during re-review.
