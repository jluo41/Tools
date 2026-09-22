# Design Run Profile · v0.4.0

## Allowed Run Types

| Run Type | Operation | Actor mode | Target |
|---|---|---|---|
| `Design.commission` | `commission` | human | one Design Item's exact config version |
| `Design.generate` | `generate` (config mode compose, revise, brainstorm, theory-driven, or challenge) | agent | the released item |
| `Design.verify` | `verify` | agent | named immutable generation Result(s) |

The Workflow is a list of Runs. Actual current Design Runs per Item are
`C Commission + N Generate + J Verify`. Count allocated records with receipts,
including held, failed, blocked and superseded Runs. C=1 only when no hold
preceded release; an Item permits at most one release.
Do not count Workflow, Space, Steps, calls, drafts, renders, Results,
projections, or retry attempts.

## Identity

```text
<Design Folder>/runs/rdNN_commission_<slug>.yaml
<Design Folder>/runs/rdNN_generate_<slug>.yaml
<Design Folder>/runs/rdNN_verify_<slug>.yaml

<Design Folder>/results/<same-stem>/
```

The slug is the item id: `rd01_commission_item01`, `rd02_generate_item01`.
`rdNN` counts across the whole Design Folder, so ITEM02's first Run may be
`rd05`. `haipipe.design-ticket/v2` and its paired v2 Result/receipt are the
only accepted Design schemas. Run record and Result stem are one Run identity.

## Run record fields

There are two shapes: the Commission decision run record, written by the
Design workbench for a person, and worker run records (Generate, Verify), read by
`haipipe-design-unit`. They are not interchangeable: `check_unit.py` rejects a
worker run record written in the decision shape ("unexpected worker").

Commission decision run record, as `design_actions` writes it:

```yaml
schema: haipipe.design-ticket/v2
run: rd01_commission_item01          # equals the file stem
run_type: Design.commission
operation: commission                # matches the stem
item: ITEM01
target: <the item's title>
actor: {mode: human, owner: <the named person>}
action: release or hold the frozen commission
inputs: [{path, sha256}, …]          # Commission: its config + the item's evidence (role, path, sha256)
entry_gate: <condition>
exit_gate: {mode: human, assertion: <close rule>}
routes: {release: generate, hold: HOLD}
result: results/rd01_commission_item01/
receipt: results/rd01_commission_item01/runtime.yaml
```

`check_unit.py --folder` checks a decision run for pairing only: `schema`, `run`
equal to the stem, `operation` matching the stem, a `runtime.yaml` with the
same `run` and a known status, and, once complete, a `decision.yaml` with
`run`, `decision`, and `actor`, plus `finished_at` on the receipt.

Worker run record (Generate, Verify): these are the fields `check_unit.py`
requires; the full contract is `haipipe-design-unit/references/unit-contract.md`.

```yaml
schema: haipipe.design-ticket/v2
run: rd02_generate_item01            # equals the file stem
operation: generate                  # generate | verify; matches the stem
worker: haipipe-design-unit          # exactly this
actor: designer-context-01           # a plain string naming the worker context
item: ITEM01                         # the workbench groups by it; the checker ignores it
target: <the item's title>
config: {path: scripts/config/rd02_generate_item01.yaml, sha256: <hash>}
approval:
  actor: <the person who released>
  record: {path: results/rd01_commission_item01/decision.yaml, sha256: <hash>}
inputs: [{role, path, sha256, run_id?}, …]   # evidence | handoff | inspiration | reference | avoid | base | feedback
targets: []                          # verify: the exact Generate result.yaml refs
```

The config it pins needs `goal` (the goal sentence), `kind`, `mode`, `basis`,
the five `design_intent` fields, `review_mode` (`self` for generate,
`independent` for verify), a positive `max_iterations`, `unit`
(`shape`, `count`), and a nonempty `criteria` list with unique ids. A revise
needs `base` and `feedback` inputs; `evidence-informed` needs an `evidence` or
`handoff` input; an independent reviewer's `actor` must differ from every
producer.

## Commission decision Run

The human actor decides `release` or `hold` for one Design Item's exact config
fingerprint. The Result is `decision.yaml` with run, item, decision, actor,
exact words, target, input hashes, and timestamp. `release` routes to
Generate; `hold` routes to HOLD, and the person may release later with a new
Commission Run. Preserve the completed hold decision; a second release is refused.
The decision itself is independently closable, so this is a Run. Each
comment/click leading to it is a Step, not another Run.

## Generate Run

Modes include `compose`, `brainstorm`, `theory-driven`, `challenge`, and
`revise`; revise pins the base draft and the feedback file
(`outline/feedback/<run>.md`); a challenge item's revise stays in challenge
mode. The worker is `haipipe-design-unit` through the existing designer
dispatcher.

The run record pins a derived copy of the released Commission's config (only
`review_mode` and the permitted operation `mode` may differ; see Unit contract), the
Commission's `decision.yaml` as approval, and the evidence files the
Commission pinned. The Result folder contains `result.yaml`, `checks.yaml`,
`content/`, optional `render/` with a hash-bound `render_manifest` reference in
`result.yaml`, and caller-owned `runtime.yaml`. Completion requires the records
check to pass; a draft that fails it is recorded `failed` with route
`generate`, and the person queues a revise with feedback.

## Verify Run

The run record pins exact generation Results/hashes, the released config's
criteria, and an independent reviewer context. The Result contains complete
coverage and a pass/fail/unresolved verdict. Pass routes to the read-only
Delivery projection; fail routes to a revise Generate. An unresolved judgment
with complete per-check reasons is a completed Result, recorded
`status: complete`, `terminal_outcome: unresolved`, and
`route: resolve-unresolved`. It is not ready for Delivery, and the same target
and criteria must not be reviewed again unchanged. The person routes each gap:
missing evidence to its named evidence owner, unclear or conflicting criteria
to the Commission owner for a clarified successor item, or inspection limits
to the owner who can supply the needed render/context. Preserve the unresolved
Result as history. A malformed/missing judgment or execution failure is not a
completed unresolved assessment; it is `failed`/`blocked`, and a justified
retry can use the appropriate recovery route. Verification never edits the
candidate.

## Delivery projection

Delivery is not another decision Run. It is a read-only projection of the
exact Generate Result and Verify receipt whose latest independent verdict is
`pass`. The projection exposes the design text, source Result, verification
Run, and hashes so the next team can consume the candidate directly. No
person-specific status is recorded or displayed.

Pictures are read from the candidate's Result-local render manifest, without
worker writes to Delivery. Existing Delivery manifests are legacy display input.

## Runtime receipt

A worker run's receipt, as the workbench queues it and `complete_run` closes it:

```yaml
run: rd02_generate_item01
family: design
operation: generate
item: ITEM01
target: <the item's title>
status: complete                     # planned | running | complete | failed | blocked | superseded
ticket: runs/rd02_generate_item01.yaml
result: results/rd02_generate_item01/
ticket_sha256: <hash of the run record>
inputs:
  - {path: scripts/config/rd02_generate_item01.yaml, sha256: <hash>}
  - {path: results/rd01_commission_item01/decision.yaml, sha256: <hash>}
  - {role: handoff, path: <insight page>, sha256: <hash>}
worker: {kind: skill, name: haipipe-design-unit, actor: designer-context-01}
queued_at: <RFC3339 timestamp>
started_at: <RFC3339 timestamp>
finished_at: <RFC3339 timestamp>
route: verify                        # resolve-unresolved after a complete unresolved Verify
terminal_outcome: pass               # pass | fail | unresolved
failure: null                        # failed, blocked, superseded: the reason
```

A decision run's receipt carries the same run, family, status, and input
fields plus `run_type`, `actor: {mode: human, owner}`, `action`,
`entry_gate`, and `exit_gate`. Actor/context provenance must be honest. The
worker may write only its paired Result, excluding runtime; the caller owns
runtime and human authority. A worker's named hold diagnostic is not a human
Commission HOLD decision. The presenter distinguishes `commission held` from
`blocked`, showing the blocked Run, failure and the caller responsible for repair.

## Reopen and retry

A draft changes only through a new Generate Run (a revise with base and
feedback); preserve the old Result and decision. A queued run whose pinned
file changed is replaced, never re-pinned in place: "Queue again with today's
insight files" marks it `superseded`, with the changed files as its
`failure` reason, and queues a fresh run that pins today's bytes. A worker
that dies without a Result is put back to `planned` under the same identity,
with the lost worker named on the receipt.

## Audit

```bash
python3 <haipipe-design-unit>/scripts/check_unit.py --folder <Design Folder>
```

An open run must match its pins exactly; a closed run (complete, failed,
blocked) reads inputs outside the Design Folder (Insight pages) as history;
a superseded run needs a reason and no result. Also verify that every Design
Run resolves to one Workflow Run Spec, legal Gate/Route outcomes, paired v2
Result, and runtime receipt; Run Space rows must show the same ids.

## Clean break

Historical `rdNN_adopt_*` decisions remain readable for pairing/audit only,
under their original ids and marked as legacy. Current writers create only
Commission, Generate and Verify; no new Adopt or Delivery Run is allocated.

Reject v1 Ticket/Result schemas, `rNN_design_*`, D0-D5/GD0-GD6,
`design/DU*/`, PageX, and previous phase-shaped Design folders. Stop at the
first decisive unsupported marker. There is no read, compatibility, or
migration route.
