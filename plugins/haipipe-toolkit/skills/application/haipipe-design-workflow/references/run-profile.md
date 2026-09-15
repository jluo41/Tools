# Design Run Profile · v0.4.0

## Allowed Run Types

| Run Type | Operation | Actor mode | Target |
|---|---|---|---|
| `Design.commission` | `commission` | human | one exact Commission/config version |
| `Design.generate` | `generate` or `revise` | agent | one released unit/set/sequence |
| `Design.verify` | `verify` | agent | named immutable generation Result(s) |
| `Design.adopt` | `adopt` | human | exact verified candidate hashes |

Expected actual Design Runs are `1 + N_generate + J_verify + 1`. Count only
allocated Tickets with runtime receipts. Do not count Workflow, Workspace,
Steps, calls, drafts, renders, Results, projections, or retry attempts.

## Identity

```text
<DS>/runs/rdNN_commission_<slug>.yaml
<DS>/runs/rdNN_generate_<slug>.yaml
<DS>/runs/rdNN_verify_<slug>.yaml
<DS>/runs/rdNN_adopt_<slug>.yaml

<DS>/results/<same-stem>/
```

`haipipe.design-ticket/v2` and its paired v2 Result/receipt are the only
accepted Design schemas. Ticket and Result stem are one Run identity.

## Common required fields

```yaml
schema: haipipe.design-ticket/v2
run: rdNN_<operation>_<slug>
run_type: Design.<operation>
operation: commission | generate | verify | adopt
target: <bounded target>
actor: {mode: human | agent, owner: <literal owner>}
action: <decision or execution action>
inputs: [<immutable path/hash entries>]
entry_gate: <open or testable condition>
exit_gate: {mode: human | automatic | agent | hybrid, assertion: <close rule>}
routes: {<outcome>: <next Run Spec | CLOSE | HOLD>}
result: results/<same-stem>/
receipt: results/<same-stem>/runtime.yaml
```

Inputs may be empty only for a new Commission whose exact target/config is
fully inside the Ticket. Exit Gate, route outcomes, and receipt are required.

## Commission decision Run

The human actor decides `release` or `hold` for one exact Commission/config
fingerprint. The Result is `decision.yaml` with actor, exact words, decision,
target, input hashes, and timestamp. `release` routes to Generate; `hold`
routes to HOLD. The decision itself is independently closable, so this is a
Run. Each comment/click leading to it is a Step, not another Run.

## Generate Run

Modes include `compose`, `brainstorm`, `theory-driven`, `challenge`, and
`revise`; revise pins frozen base + feedback. The worker is
`haipipe-design-unit` through the existing designer dispatcher.

The Ticket pins config, Commission decision receipt, exact file references and
hashes, defaults, and one `design_intent` bet. The Result folder contains
`result.yaml`, `checks.yaml`, operation payload, and caller-owned
`runtime.yaml`. Completion requires integrity and substantive self-checks.

## Verify Run

The Ticket pins exact generation Results/hashes, criteria, and an independent
reviewer context. The Result contains complete coverage and a pass/fail/
unresolved verdict. Pass and fail can be honest terminal judgments; unresolved
is a HOLD. Verification never edits the candidate.

## Adopt decision Run

The Ticket pins exact candidate hashes, verification Results, preview manifest,
and handoff versions. The named human records `adopt`, `decline`, `revise`, or
`hold` in `decision.yaml`. Adopt/decline route to CLOSE, revise to a new
Generate Run, hold to HOLD. The exact adoption receipt is reused by the Design
Page owner gate; Page CHECK verifies and never duplicates the decision.

## Runtime receipt

```yaml
run: rd03_generate_sms
run_type: Design.generate
operation: generate
target: One SMS
actor: {mode: agent, owner: designer-context-01}
action: generate
status: complete
ticket: runs/rd03_generate_sms.yaml
result: results/rd03_generate_sms/
inputs:
  - {path: scripts/config/rd03_generate_sms.yaml, sha256: <hash>}
  - {path: results/rd01_commission_sms/decision.yaml, sha256: <hash>}
entry_gate: {status: passed, assertion: Commission released}
exit_gate: {status: passed, assertion: integrity and self-check pass}
route: verify
terminal_outcome: pass
worker: {kind: skill, name: haipipe-design-unit, actor: designer-context-01}
started_at: <RFC3339 timestamp>
finished_at: <RFC3339 timestamp>
failure: null
supersedes: null
```

Actor/context provenance must be honest. The worker may write only its paired
Result; the caller owns runtime and human authority.

## Reopen and retry

A changed target, config, source, criteria, candidate content, decision set, or
post-closure feedback creates a new Run and may name `supersedes`. Preserve the
old Result and decision. An unchanged failed attempt may append an attempt
trail under the same identity.

## Audit

```bash
python3 <haipipe-design-unit>/scripts/check_unit.py --folder <DS>
```

Also verify that every Design Run resolves to one Workflow Run Spec, legal
Gate/Route outcomes, paired v2 Result, and runtime receipt; Runtime Workspace
cards must preserve the same ids.

## Clean break

Reject v1 Ticket/Result schemas, `rNN_design_*`, D0-D5/GD0-GD6,
`design/DU*/`, PageX, and previous phase-shaped Design folders. Stop at the
first decisive unsupported marker. There is no read, compatibility, or
migration route.
