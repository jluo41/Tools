---
name: haipipe-design-workflow
description: >-
  Run-backed Design Folder workflow: plan/release, generate, independently
  verify, and adopt/render. Owns the Phase × Run map, dispatch, recovery and
  person gates. Reads legacy D0-D5 records without creating new DU Folders.
metadata:
  version: "2.0.0"
  last_updated: "2026-09-07"
---

# /haipipe-design-workflow · commission units, preserve results

Load `haipipe-design`, `haipipe-folder`, and `haipipe-run`.
The stable Design Folder owns both faces throughout; these phases do not
create Card/Unit/Verdict Folder identities. Read
[run-profile.md](references/run-profile.md) before commissioning a Run.

## Phase × Run map

| Phase | Folder / episode | Purpose | Allowed operations | Cardinality | Gate | Close |
|---|---|---|---|---:|---|---|
| Plan | stable DS Folder | write bounded commissions, config, grants, criteria | none | 0 | person releases named written commissions | frozen inputs |
| Generate | same Folder, released set | produce candidate DUs | Design.generate | N | unit Result integrity + self-check | N generation Results or truthful non-success |
| Verify | same Folder, review set | independently assess selected candidates | Design.verify | J | coverage, source integrity, actual independent context | J review Results, including rejecting verdicts |
| Adopt | same Folder | present, record selection, update readable projections | none by default | 0 | person accepts exact current versions | Page and receipt current; stop |

Expected total is N + J. Both are commissioned cardinalities, not the number
of messages, files, API calls, internal drafts, or phase invocations.
Do not allocate an umbrella Run as well as its independently closable children.
A separately commissioned display may use its own existing Display Run
profile; never count its rendering again as a Design Run.

## Plan and release

Resolve the Brief/roster, stable audience × job × venue, and native Folder
owner. If a legacy phase.yaml still
controls the Folder, follow the Design migration reference and hold new writes
until its explicit owner-metadata migration is authorized. Keep historical DUs.
Write commissions under outline/, reusable defaults and frozen per-Run configs under
scripts/config/. Compile exact input roles, required outputs, criteria, mode,
and budget. Present the written set to the person. A release covers only that
named, existing set; changed terms require a new release.

After release allocate the next monotonic Run stem, its YAML Ticket and planned
runtime receipt. Do not change a released config in place. Future proposals
remain plans, not allocated Runs.

## Dispatch

1. Read the Ticket, pinned files, release scope, and current dependencies.
   Run the unit checker's Ticket gate. Missing inputs hold only dependent work.
2. The caller records running/start time, then dispatches
   `haipipe-design-unit generate|verify <ticket>`. For independent verify
   use a fresh reviewer context, never the producer's context.
3. The worker returns a Result in the preallocated directory. Validate it with
   the unit checker, inspect the substantive checks, then record the truthful
   runtime terminal state and receipt. Exit-code success alone is insufficient.
4. Generate completes only with passing required checks. Verify may complete
   with pass or fail when the review is fully performed; unresolved checks
   remain blocked. Completion is not adoption.
5. Present current previews, verification findings, and unresolved issues.
   Record the person's exact selection or decline. A selection may name a
   subset of a DU's members, pinned by path/hash. Review pass cannot adopt.
6. Update the Page through its own workflow and record a round receipt under
   workflow/. Stop when the requested round closes or a named gate blocks.

## Recovery and boundaries

Internal generation/check/revision cycles stay inside the released budget.
Once a Result is complete, changed content, config, input, target or criteria
requires a new Run; pin the base and feedback. An unchanged failed attempt can
resume under the same identity with an append-only attempt trail. Never
overwrite a successful Result while retrying or verifying.

Stale upstream inputs invalidate dependent current bindings, not unrelated
units or historical records. Missing evidence returns a named gap to the
Design owner; do not launch Insight/Task work or invent a signed handoff.
A brief-only proposal may proceed within its commissioned non-empirical scope.

Release, independent verification, and person adoption preserve their distinct
authority. Keep existing Page controls without duplicating those decisions.
Never ship, measure, or keep iterating after budget exhaustion.

Release and adoption are the two cross-phase authority gates; nested Page-Face
controls remain in the Page workflow and never substitute for either decision.
Record release/adoption in immutable `outline/decisions/<decision-id>.yaml`
receipts naming the person's words and exact commission/Result versions.
The DS Folder's `outline/<DS-stem>-log.md` is the dated index of those receipts;
the Page projects them instead of becoming a second acceptance ledger. Pin the
individual release receipt in a Ticket, never the growing log file: appending
a later adoption must not invalidate an earlier Run's input hashes.

## Status and compatibility

Report each commissioned target, Run, runtime state, verification verdict,
adoption binding, freshness and next action. Do not compress every target into
one phase scalar or count plan rows as Runs.

Legacy D0–D5/GD0–GD6 describe old artifacts only:
[legacy-workflow.md](references/legacy-workflow.md). Read their receipts for
status; new work always uses the native map above. Historical DU content may
be a pinned base, never a fabricated historical Run.
