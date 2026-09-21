---
name: subjective-label-workflow
description: >-
  Defines the subjective-label Workflow as Run Specs, their dependencies,
  gates, routes, entry conditions and completion rule. P0-P5 and G0-G6 remain
  compatibility capability/gate labels on domain records; they are not
  independent lifecycle units or owners. The graph connects the Building and
  Scanning Run Specs across the immutable Label Handoff. Use when resolving
  the next eligible Run Spec, a held route, or /subjective-label-workflow.
metadata:
  version: "0.12.0"
  last_updated: "2026-09-20"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /subjective-label-workflow · the Labeling Run graph

Load `subjective-label` first. **A Workflow is a list of Runs.** Its definition
is the list of planned Run Specs plus their dependency/Route graph and
completion rule; execution is the native Run Instances and their receipts.
This document defines the Labeling graph over the operation types in
`../../ref/ref-run.md`. The Run Type/owner contract defines each operation's
bounded target, action, acceptance, and canonical Result. The Building and
Scanning doors define semantic authority and forbidden acts.

The serialized `phase: P0` ... `P5` field is retained for compatibility and
readable capability grouping. It may appear in Tickets, status, and views, but
it does not own work, authorize an operation, establish a frontier, or create a
separate lifecycle entity. Likewise G0-G6 are stable labels for predicates and
human authorization evidence attached to the relevant Run or job control;
they are not Runs by themselves. Do not create a Run just for a gate, route,
episode, item, model call, or display row.

## Run Spec list and graph

Each operation name below is a Run Type used by one or more stable Run Specs.
The Workflow Definition supplies each Spec's bounded target, actor, action,
inputs/dependencies, entry and exit gates, allowed routes, cardinality and
durable Result. See `haipipe-workflow`'s Run Spec contract. The P0-P5 column is
only the legacy capability tag to preserve on existing records and projections;
the rows and their Routes are the Workflow.

| Capability tag (compatibility only) | Episode / target scope | Run Specs (`run_type`) and dependency order | Planned cardinality |
|---|---|---|---:|
| P0 · Contract | one imported corpus and target job | `corpus-contract`; independently commissioned `discovery-search`, `guideline-seed`, `test-reserve`, and `embedding-build` Specs when needed | 1 + D + G + T + E |
| P1 · Round | one released Card per round | `round-prepare` → optional `weak-prelabel` Runs → `human-calibration` → `guideline-learn` → `round-measure` → `round-close`; `round-close` Routes to another `round-prepare`, `handoff-freeze`, or `HOLD` | 5N + sum(W_r) |
| P2 · Freeze | one stopped Building lineage | `handoff-freeze`; on accepted Result, Route to `test-gold-lock` | 1 |
| P3 · Test | one frozen executor registry and sealed test | `test-gold-lock` → `executor-predict` per candidate/baseline → `executor-score` per closed prediction → `executor-select` | 2K + 2 |
| P4 · Scan | one immutable production manifest and its shards | `scan-preflight` → `scan-shard` per shard → `risk-route` → `human-review` → `reconcile` | S + 4 |
| P5 · Audit | one frozen audit design and candidate corpus | `audit-sample` → `audit-human-gold` → `audit-analyze` → `dstar-materialize` when pass or bounded limitation is accepted | 4 |

`D` is commissioned discovery queries; `G`, `T`, and `E` are the commissioned
counts for optional policy-candidate, reservation-frame, and embedding Runs
(usually 0 or 1 each); `N` is the number of calibration rounds; `W_r` is weak
executors per round; `K` is
qualification candidates including the baseline; `S` is production shards.
The expected happy-path total is `D + G + T + E + sum(W_r) + 5N + 2K + S +
12`. This is planned cardinality, not an inventory. Count actual work only
from allocated Tickets with runtime receipts; retries under unchanged inputs
are attempts on the same Run.

Operation targets and minimum Results are defined in `../../ref/ref-run.md`.
The Definition must use the host Run Spec contract for actor/action, gates,
Routes, dependencies, and terminal rules. A symbolic repeat such as one
`scan-shard` per frozen shard means a Run Instance for each commissioned
target; it does not make a folder or round an extra Run.

## Gates and ownership

G0-G6 remain recognizable gate labels, but each evaluation belongs to the Run
whose exit or entry condition it checks, or to an explicitly identified job
control. The Run receipt records Run-owned gate evidence and its Route. A
control-only update to job authority is a resource control; do not fabricate a
Run identity for it. A Workflow Runtime may index these records as an aggregate
view, but does not replace the Run receipts or become a child Run.

| Gate label | Owning work / evidence | Route enabled by the predicate |
|---|---|---|
| G0 | job `resource_controls` entry referencing the completed `corpus-contract` Result plus the identified human's meaning-confirmation receipt bound to the five contract authority files | `round-prepare` may be commissioned; optional `embedding-build` remains separately commissioned |
| G1 | `round-close` Result: Keeper checks pass and checkpoint is closed | another `round-prepare`, `handoff-freeze`, or `HOLD`, as recorded on the closing Run |
| G2 | final qualifying `round-close` Result, configured stability/coverage/risk checks, and human STOP evidence | allocate `handoff-freeze` |
| G3 | `handoff-freeze` Result binds the exact G*/D_cal* checksums and human FREEZE signature | `test-gold-lock` may begin under the frozen registry |
| G4 | `executor-select` Result applies the preregistered rule to closed predictions and scorecards | `scan-preflight` for a qualified or explicitly human-only route; otherwise `HOLD` or a semantic reopen |
| G5 | `reconcile` Result proves one terminal disposition per in-scope id and a reconciled risk queue | `audit-sample` may begin under the frozen audit design |
| G6 | `audit-analyze` Result and required human limitation acceptance; `dstar-materialize` validates the accepted route | `dstar-materialize` may promote the audited candidate, or the Run's explicit repair/rescan/semantic Route applies |

For G0, the five contract authority paths are `config.yaml`,
`corpus/manifest.json`, `test/sealed/status.json`, `register.md`, and
`policy/versions/G_00/manifest.yaml`. A complete, integrity-valid
`corpus-contract` Result with valid human authority but no meaning receipt is
**G0 pending**: the identified human confirmation is owed, and this pending
predicate is not itself a `HOLD`. The engine's `authority_hold(config)` sets
HOLD for simulation/proxy authority, imported source labels without a locally
appointed human, a missing human id, or an authority mode other than
`single_human_semantic_authority` with `creates_human_gold: true`. Missing or
invalid P0 files and checksum failures require repair before continuing.

The `confirm` API checks that the caller-supplied id matches the configured
semantic authority only when all five P0 files and their bound inputs pass
integrity checks and `authority_hold(config)` is false. The CLI and local
Board record explicit caller attestation but do not authenticate caller
identity. Before confirmation, an absent meaning receipt/G0 receipt is expected
and status asks for explicit meaning attestation; it is not HOLD. If semantic
confirmation exists but the G0 receipt is missing, invalid, or no longer binds
the current files, status reports an integrity defect and does not enable
`round-prepare`. A repeat confirmation can write a missing G0 receipt. A prior
bound receipt can be upgraded only when its existing G0 receipt still verifies;
the old receipt is archived by checksum before replacement. Corrupt or
unverified receipts are never overwritten. G0 evidence belongs to the
transition into `round-prepare`;
represent the control in the Workflow Runtime's `resource_controls` with a
reference to the completed Run Result. The current engine serializes the human
attestation and G0 receipt in `config.yaml` and `gates/g0/receipt.json`; that
storage mapping does not create a gate Run or change the closed
`corpus-contract` Result. The independent `embedding-build` Spec may be
commissioned after the P0 files pass integrity and the job is not on HOLD; it
does not depend on G0. G0 plus a separately released Card is required before
commissioning `round-prepare`.

These labels do not transfer authority. The identified human remains the
semantic authority; the named Keeper, Custodian, evaluator, or auditor writes
only the artifacts assigned by the owner contract. Bare approval, signature,
or click events are evidence inside that bounded work, not independently
closable Runs.

## Handoff and Routes

The Result of `handoff-freeze` is the immutable Label Handoff. Scanning Runs
bind its exact checksum in their Tickets and never follow `policy/current`.
Read `../../ref/ref-label-handoff.md` for its fields. A later semantic change
must preserve the closed Results, record an invalidation control/receipt, and
Route to a new Building lineage; it must not rewrite downstream history.

The routes are owned by their source Run Specs and recorded with the source
Run's terminal Result/receipt. Their compatibility capability tags do not
decide them:

```text
round-close       → round-prepare | handoff-freeze | HOLD
handoff-freeze    → test-gold-lock | HOLD
executor-select   → scan-preflight | HOLD | NEW_RUN (semantic defect)
reconcile         → audit-sample | NEW_VERSION (changed production contract)
audit-analyze     → dstar-materialize | audit-sample (repair) |
                    scan-preflight (rescan) | round-prepare (semantic reopen) | HOLD
```

Every reopen preserves the superseded Results and names affected Runs and
claims. A material target, frozen input, policy, route, threshold, scope, or
design change receives the new Run/Version authorized by the owner profile.

## Select and return

Resolve the Workflow Definition and inspect native Run Tickets, Results, and
runtime receipts. Select one eligible Run Spec from its declared dependencies
and the latest source Run Route. Stop at a named human entry/exit gate, an
invalidated handoff, missing owner/worker, or explicit `HOLD`; do not infer
progress from a highest P-number, view, or artifact timestamp. Allocate only
after that Spec's commission and frozen inputs exist.

Return the active Run address or `none`, its Run Spec, terminal/held outcome,
bound handoff checksum or its absence, the first unmet gate predicate and its
evidence owner, eligible next Run Spec, actual allocated Run count, and the
optional planned count with its assumptions. P0-P5 may be included as
compatibility display tags, clearly labeled as projections.
