# Design Run Profile

ALLOWED: family design; operations generate and verify. Evaluate aliases verify,
compose aliases generate. Revise is generate with a frozen base and feedback.

TARGET: one independently closable unit (single, sequence, or set), or one
independently closable verification over named DUs. Count N generation + J
verification Runs; no umbrella Run and no Run for a signature.

TICKET: caller-authored `<DS>/runs/<rNN_design_operation_slug>.yaml`, conforming
to the unit worker's references/unit-contract.md. This is a declared
Folder-local agent-ticket dialect. Read and dispatch it; do not invoke bash.
A normal renderer/model invocation is an internal worker call, not a Run.

INPUTS: the Ticket pins config and exact file references/hashes. Defaults are
compiled before freeze. Supporting Runs retain their producer's full identity;
do not copy or renumber them. A static Brief, signed legacy W handoff, template,
or old DU input is a versioned input, not an invented Supporting Run. Input
roles never elevate authority. Caller validates release scope and Application
signed-W/grant constraints; worker validates the bounded packet.

WORKER: `haipipe-design-unit`, loaded by path
`../../workflow-phases/haipipe-design-unit/SKILL.md` from this reference's
directory. The existing designer agent is a thin dispatcher into that worker.

RESULT: `<DS>/results/<Ticket-stem>/result.yaml` plus checks.yaml and the
operation's payload. The caller owns runtime.yaml at the same address.
An allocated Ticket immediately owes a planned runtime; failed/blocked work
keeps its truthful partial Result and reason. New Result paths must be empty
apart from the caller's runtime receipt, or an explicitly resumed incomplete
attempt. Never overwrite existing complete results.

ACCEPT: the unit checker's result gate plus substantive verification of the
commissioned criteria. Generate requires pass. Verify requires complete
coverage; pass or fail is an honest finished evaluation, unresolved is not.
Self-check is never independent verification.

PROMOTION: the caller records human adoption of exact DU/member hashes,
independent verification and preview versions. The Page projects that receipt.
Independent review uses a new context, not just a different actor label.
Selection, adoption and ordinary projection updates mint no new Design Run.

REOPEN: materially changed config/source/criteria/content gets a new Run,
with `supersedes` in the runtime when appropriate; the old result remains
immutable. Mark only affected adoption/evidence bindings stale. Failure
retries with unchanged inputs preserve an append-only attempt trail.

## Caller runtime receipt

```yaml
run: r01_design_generate_sms
family: design
operation: generate
target: One SMS
status: complete
ticket: runs/r01_design_generate_sms.yaml
result: results/r01_design_generate_sms/
inputs:
  - {path: scripts/config/r01_design_generate_sms.yaml, sha256: <config-hash>}
  - {path: outline/decisions/release-01.yaml, sha256: <release-hash>}
ticket_sha256: <hash-of-ticket>
worker: {kind: skill, name: haipipe-design-unit, actor: designer-context-01}
started_at: <ISO timestamp>
finished_at: <ISO timestamp>
failure: null
supersedes: null
```

The caller records the Ticket hash and the full input manifest in the runtime
including config, immutable release record, all input files and target manifests
(the brief-only example above has no other inputs). Actor/context provenance
must be honest. A growing decision log is an index, not a hash-pinned input.
The worker cannot use a runtime write to bypass the caller's completion gate.

Audit a native Folder with the worker's
`python3 scripts/check_unit.py --folder <DS>`.
The read-only Runs presenter already recognizes YAML Tickets and runtime.yaml;
it must display Design-local identity without calling it a Paper Run.
