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
run: rd02_generate_item01
operation: generate
item: ITEM01            # the Design Item this Run serves (register id)
worker: haipipe-design-unit
actor: designer-context-01
target: Send the salience wording unchanged
config: {path: scripts/config/rd02_generate_item01.yaml, sha256: <hash>}
approval:
  actor: <person>
  record: {path: results/rd01_commission_item01/decision.yaml, sha256: <hash>}
inputs: []  # role + path + sha256; optional real upstream run_id
targets: [] # verify only: exact generation result.yaml refs
```

Run slugs follow the item id (`rd02_generate_item01`), and `rdNN` counts
across the whole Design Folder, so ITEM02's first Run may be `rd05`. The
approval record is the released Commission's `decision.yaml` under
`results/`.

`item` names the Design Item register row (`outline/<stem>-design-items.md`)
this Run serves. The checker does not interpret it; the Design plugin groups
Runs by it. Commission and Adopt Tickets carry it too.

Roles: `evidence | inspiration | reference | avoid | base | feedback | handoff`.
Role never promotes authority. `run_id` normally names a real Supporting/native
Run. An `rpNN` Page Run may enter only as frozen `feedback` to a revise Run; it
cannot become evidence, handoff authority, or the producer of a Generate
Result. A revise Generate's `feedback` input is `outline/feedback/<run>.md`,
written when the revise is queued. Static
Briefs and signed W handoffs omit Run ids.
Application callers validate W signing/applicability, Board reads, and grant
scope. The approval receipt is a person's release of an already-written
commission/config. The worker cannot create or infer it.

## Frozen v2 config

```yaml
goal: Make the required next action immediately legible   # the item's goal sentence
kind: sms
mode: compose
basis: brief-only
item: ITEM01
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
  - {id: r01, kind: max_chars, value: 160}
  - {id: r02, kind: ends_with, value: "Reply STOP to opt-out"}
  - {id: r03, kind: semantic, description: Respectful, non-coercive wording}
acceptance:             # the rule text as released, for the card
  - ≤ 160 characters including the opt-out suffix
  - ends with 'Reply STOP to opt-out' verbatim
  - Respectful, non-coercive wording
```

The Design plugin writes this config when a person releases the Commission,
and Generate and Verify copy it unchanged, so a later register edit never
reaches this item's drafts. `goal` is the item's goal sentence (the same text
as `design_intent.move`), not its title. `max_iterations` is the budget inside
one Generate run; nothing counts revise runs across an item.

`design_intent` freezes the bet before output exists. `move` says what the
design tries; `basis` must equal config basis; `stance` is `follow | challenge |
explore | generate`; expected effect/failure are typed forecasts of design
quality, not measured evidence. Compose/revise may leave them null.
Brainstorm must leave both null and takes stance `explore` or `generate`.
Theory-driven requires both. Challenge mode requires stance `challenge` (and
stance `challenge` requires challenge mode), an alternative effect, and a
distinguishing/failure condition. See `modes.md`.

`unit.shape` is single, sequence, or set; positive `count` is the number of
content artifacts. Each member has a stable Result-local path/hash. Choosing a
subset later references those exact bytes. Modes are compose, revise,
brainstorm, theory-driven, challenge. Basis is brief-only or evidence-informed.
A revise Ticket requires base + feedback; evidence-informed requires evidence
or handoff. Generate uses self review; verify uses independent review.

Criteria have unique ids. The kinds are `max_chars`, `contains`, `excludes`,
`starts_with`, `ends_with`, `semantic`, and `visual`. The first five are
built-ins the checker recomputes per UTF-8 artifact; `ends_with` compares the
draft with trailing whitespace stripped, `starts_with` with leading
whitespace stripped. `semantic` and `visual` name an observation method; they
are not automatic. A config the Design plugin compiles names rule N `rNN`,
plus `rNNb`, `rNNc` for a rule quoting several phrases. Mode-specific
rationale/forecast/member provenance must be explicit commissioned
deliverables and criteria before release.

## Result

```yaml
schema: haipipe.design-result/v2
run: rd02_generate_item01
operation: generate
target: Send the salience wording unchanged
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
    criterion: r01
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

Generate completes only when every required check passes; a draft that fails
the records check is recorded `failed` and routed back to Generate. Verify
completes with pass or fail only when coverage is complete; a review with any
unresolved check fails the records check, is recorded `failed`, and is routed
back to Verify. The caller closes a run with `design_actions.complete_run`.
Human adoption is a separate version-bound receipt and never a Result field.

Validate read-only with:

```bash
python3 scripts/check_unit.py --ticket <ticket> [--result <result.yaml>]
python3 scripts/check_unit.py --folder <Design Folder>
```

`--folder` audits every run in the folder. An open run (planned, running)
must match its pins exactly. A closed run (complete, failed, blocked) reads
inputs that live outside the Design Folder, such as Insight pages, as
history, so their later edits do not void it; inputs inside the folder
(config, approval, targets, artifacts) stay exact. A `superseded` run (a
queued run replaced after a pinned file changed) needs a reason in `failure`
and no result. Commission and Adopt runs are checked for pairing and a
recorded decision. Messages use folder-relative paths and plain words
("a Generate Result requires content artifacts").

Exit 0 proves only the stated structural/check gate, not semantic quality,
independence, release validity, Page closure, or adoption.

There is no adapter path. v1, `rNN_design_*`, D0–D5/GD0–GD6,
`design/DU*/`, and PageX are invalid inputs rather than readable history.
