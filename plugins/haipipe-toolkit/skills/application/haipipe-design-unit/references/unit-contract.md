# Design unit Ticket and Result contract · v2

Owner: `haipipe-design-unit` for worker inputs/outputs; the caller's Run Profile
owns allocation, release, runtime, lifecycle, and promotion. v2 is the only
accepted Ticket/Result schema; v1 is rejected.

## Ticket

A Run is `<owner>/runs/<rdNN_generate|verify_slug>.yaml`, paired with
`<owner>/results/<same-stem>/`. Resolve Ticket references from the owner and
Result-local references from the Result directory. Every reference names one
regular file plus lowercase SHA-256. Never dispatch YAML through bash.

```yaml
schema: haipipe.design-ticket/v2
run: rd01_generate_sms
operation: generate
worker: haipipe-design-unit
actor: designer-context-01
target: One supportive prescription-confirmation SMS
config: {path: scripts/config/rd01_generate_sms.yaml, sha256: <hash>}
approval:
  actor: <person>
  record: {path: outline/decisions/release-01.yaml, sha256: <hash>}
inputs: []  # role + path + sha256; optional real upstream run_id
targets: [] # verify only: exact generation result.yaml refs
```

Roles: `evidence | inspiration | reference | avoid | base | feedback | handoff`.
Role never promotes authority. `run_id` normally names a real Supporting/native
Run. An `rpNN` Page Run may enter only as frozen `feedback` to a revise Run; it
cannot become evidence, handoff authority, or the producer of a DU. Static
Briefs and signed W handoffs omit Run ids.
Application callers validate W signing/applicability, Board reads, and grant
scope. The approval receipt is a person's release of an already-written
commission/config. The worker cannot create or infer it.

## Frozen v2 config

```yaml
goal: Help the recipient find the next confirmation step
kind: sms
mode: compose
basis: brief-only
design_intent:
  move: Make the required next action immediately legible
  basis: brief-only
  stance: generate
  expected_effect: null
  failure_condition: null
unit: {shape: single, count: 1}
max_iterations: 2
review_mode: self
criteria:
  - {id: length, kind: max_chars, value: 160}
  - {id: link, kind: contains, value: "{confirmation_link}"}
  - {id: tone, kind: semantic, description: Respectful, non-coercive wording}
```

`design_intent` freezes the bet before output exists. `move` says what the
design tries; `basis` must equal config basis; `stance` is `follow | challenge |
explore | generate`; expected effect/failure are typed forecasts, not measured
evidence. Compose/revise may leave them null. Brainstorm must leave both null.
Theory-driven requires both. Challenge requires stance `challenge`, an
alternative effect, and a distinguishing/failure condition. See `modes.md`.

`unit.shape` is single, sequence, or set; positive `count` is the number of
content artifacts. Each member has a stable Result-local path/hash. Choosing a
subset later references those exact bytes. Modes are compose, revise,
brainstorm, theory-driven, challenge. Basis is brief-only or evidence-informed.
A revise Ticket requires base + feedback; evidence-informed requires evidence
or handoff. Generate uses self review; verify uses independent review.

Criteria have unique ids. Built-ins run per UTF-8 artifact: `max_chars`,
`contains`, `excludes`. `semantic` and `visual` name an observation method;
they are not automatic. Mode-specific rationale/forecast/member provenance
must be explicit commissioned deliverables and criteria before release.

## Result

```yaml
schema: haipipe.design-result/v2
run: rd01_generate_sms
operation: generate
target: One supportive prescription-confirmation SMS
producer: designer-context-01
ticket_sha256: <ticket-hash>
config_sha256: <same-config-hash-as-ticket>
verdict: pass
artifacts:
  - {path: content/sms.txt, sha256: <hash>}
checks: {path: checks.yaml, sha256: <hash>}
targets: []
```

Ticket and Result schema versions must match. Verify has no replacement
artifacts and reproduces target refs exactly. Optional review prose may live in
`review.md`; structured coverage remains in `checks.yaml`:

```yaml
checks:
  - target: content/sms.txt
    criterion: length
    status: pass
    evidence: "87 Unicode code points; configured maximum is 160"
```

For verify, target is `<target-result-ref>::<artifact-path>`. Cover every
artifact × criterion exactly once. Verdict derives as unresolved if any row is
unresolved, else fail if any failed, else pass. The checker recomputes built-ins
from actual bytes. It cannot prove subjective judgment or human authorization.

## Lifecycle

Allocation creates caller-owned `runtime.yaml` with run/family/operation/target,
planned status, Ticket/Result addresses, complete input manifest, worker actor,
and Ticket hash. Running adds start time. Terminal adds finish time and a reason
for failed/blocked work. The worker never writes runtime.

Generate completes only when every required check passes. Verify completes
with pass or fail only when coverage is complete; unresolved remains blocked.
Human adoption is a separate version-bound receipt and never a Result field.

Validate read-only with:

```bash
python3 scripts/check_unit.py --ticket <ticket> [--result <result.yaml>]
```

Exit 0 proves only the stated structural/check gate, not semantic quality,
independence, release validity, Page closure, or adoption.

There is no adapter path. v1, `rNN_design_*`, D0–D5/GD0–GD6,
`design/DU*/`, and PageX are invalid inputs rather than readable history.
