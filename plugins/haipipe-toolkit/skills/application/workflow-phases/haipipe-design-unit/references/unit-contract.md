# Design unit Ticket and Result contract · v1

Owner: `haipipe-design-unit` for worker inputs and outputs; the caller's
Run Profile owns allocation, release, lifecycle, and promotion.

## Declarative Ticket dialect

A native Design Run is `<owner>/runs/<rNN_design_generate|verify_slug>.yaml`
paired with `<owner>/results/<same-stem>/`. The workflow reads the YAML Ticket
and dispatches the skill; do not `bash` a YAML file or fabricate a shell runner.
Its runtime is `results/<stem>/runtime.yaml`, owned by the caller.
The read-only checker requires Python 3 and PyYAML; missing dependencies are
a reported environment hold, never permission to skip verification.
Full external identity is the stable owner address plus this exact Run stem;
do not invent a b/j/t address for a DS Folder.

All Ticket references resolve from the owner directory (Ticket parent parent).
Result-local artifact/check paths resolve from the Result directory. Every
reference names a regular file and its lowercase SHA-256, not a whole Board
or directory. Result-local paths cannot escape their output directory.

```yaml
schema: haipipe.design-ticket/v1
run: r01_design_generate_sms
operation: generate
worker: haipipe-design-unit
actor: designer-context-01
target: One supportive prescription-confirmation SMS
config: {path: scripts/config/r01_design_generate_sms.yaml, sha256: <hash>}
approval:
  actor: <person>
  record: {path: outline/decisions/release-01.yaml, sha256: <hash>}
inputs: []  # each: role + path + sha256; optional real upstream run_id
targets: [] # verify only: exact DU result.yaml refs; no raw legacy directories
```

Allowed input roles: `evidence | inspiration | reference | avoid | base |
feedback | handoff`. A source's role does not promote its authority.
`run_id` is only supplied for a real Supporting Run, never for a static Brief
or historical W page. For an Application, the caller validates signed/contextual
W applicability, register settlement, and grant ⊆ Board reads before release.
A legacy signed handoff may be a frozen `handoff` input, explicitly without a
Run id; it is not advertised as an Insight Supporting Run.

The approval record is a real person's decision about the already-written
commission/config; the worker cannot author it. The hash checker verifies
integrity, not who made the human decision. The caller verifies its scope.
Pin an immutable individual receipt, not the growing decision-log index.
No release is inferred from an instruction to propose a design.

## Frozen config

```yaml
goal: Help the recipient find the next confirmation step
kind: sms
mode: compose
basis: brief-only
unit: {shape: single, count: 1}
max_iterations: 2
review_mode: self
criteria:
  - {id: length, kind: max_chars, value: 160}
  - {id: link, kind: contains, value: "{confirmation_link}"}
  - {id: tone, kind: semantic, description: Respectful and non-coercive wording}
```

This length is an example, not a universal SMS cap. The caller compiles its
actual venue/Brief/user requirements into the config and pins those sources
as inputs when used. Explicit changes cannot silently waive authority or
safety requirements; report conflicts.

`unit.shape` is single, sequence, or set; `count` is the commissioned number
of content artifacts. One artifact represents one member, so count and member
selection are independently checkable. A sequence/set is one DU only when
jointly commissioned. Each artifact has a stable Result-local path; choosing
a subset later references those paths and hashes, not a second DU id.

Modes: compose, revise, brainstorm, theory-driven, challenge.
Basis: brief-only or evidence-informed. Review mode: self or independent
(independent is used by verify). A revise config requires base and feedback
inputs. Evidence-informed requires evidence/handoff inputs. Conditional mode
requirements are in modes.md and must become explicit criteria before release.
Every criterion has a unique id. Built-ins operate on each UTF-8 text artifact:
max_chars (Unicode code points), contains, excludes. Semantic/visual criteria
need a described method and recorded observations; do not label them automatic.

## Result envelope

```yaml
schema: haipipe.design-result/v1
run: r01_design_generate_sms
operation: generate
target: One supportive prescription-confirmation SMS
producer: designer-context-01
ticket_sha256: <hash-of-ticket>
config_sha256: <same-hash-as-ticket-config>
verdict: pass
artifacts:
  - {path: content/sms.txt, sha256: <hash>}
checks: {path: checks.yaml, sha256: <hash>}
targets: []
```

For verify: operation is verify; producer is the reviewer; artifacts is empty;
targets exactly reproduces the Ticket target refs. Optional commentary can
live in `review.md`, but checks.yaml is the structured evaluation output.
Verification never writes checks into the DU it evaluates.

Checks file:

```yaml
checks:
  - target: content/sms.txt
    criterion: length
    status: pass
    evidence: "87 Unicode code points, within the configured 160 limit"
```

For generate, target is an artifact path. For verify it is
`<Ticket target path>::<artifact path>` (one unambiguous string).
Cover every artifact × criterion exactly once; duplicate, extra, and missing
pairs are invalid. A semantic/visual row records observed evidence, not
private reasoning. `unresolved` includes the missing observation or dependency.

Verdict is derived: unresolved if any check is unresolved; else fail if any
failed; else pass. The checker recomputes built-ins from actual bytes and
rejects dishonest check rows. It validates hashes and coverage but cannot
prove the correctness of a subjective judgment or a human authorization.

## Lifecycle and completion

The caller creates runtime.yaml when allocating the Ticket: run, family:
design, operation, target, status: planned, ticket, result, inputs, worker.
Also record ticket_sha256. inputs covers config, release record, all declared
inputs and target manifests by path/hash; worker records kind, name and actor.
Before dispatch it records status: running and started_at; terminal records
include finished_at and failure (if any). Only the caller writes this file.
A failed/blocked attempt retains its Ticket, partial artifacts, and receipt.

Generate completes only when structural checks and all commissioned criteria
pass. A verification Run completes with pass or fail when all checks were
performed; unresolved checks are blocked/incomplete. Human adoption is a
separate version-bound record and is never a field written into the DU.

Validate with `python3 scripts/check_unit.py --ticket <ticket> [--result
<result.yaml>]`. Exit 0 means that command's stated gate passed, not human
adoption. This read-only checker never writes outputs or advances state.
