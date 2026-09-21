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
Runs by it. Commission Tickets carry it too. Historical Adopt Tickets may be
read for audit only; they are never new worker inputs or current workflow gates.

Roles: `evidence | inspiration | reference | avoid | base | feedback | handoff`.
Role never promotes authority. `run_id` normally names a real Supporting/native
Run. An `rpNN` Page Run may enter only as frozen `feedback` to a revise Run; it
cannot become evidence, handoff authority, or the producer of a Generate
Result. A revise Generate's `feedback` input is `outline/feedback/<run>.md`,
written when the revise is queued. Static
Briefs and signed W handoffs omit Run ids.
Design callers validate W signing/applicability, Board reads, and allowed input
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
  - id: r03
    kind: semantic
    description: The recipient can decline without pressure or penalty.
    observation: Read the whole message as its recipient, including the stated opt-out.
    pass_when: The refusal path is explicit and no penalty or false urgency is stated.
    fail_when: Refusal is hidden, discouraged by a threat, or made conditional on compliance.
    not_verifiable_when: The message depends on consequences or options not supplied in the pinned inputs.
acceptance:             # the rule text as released, for the card
  - ≤ 160 characters including the opt-out suffix
  - ends with 'Reply STOP to opt-out' verbatim
  - "semantic: The recipient can decline without pressure or penalty. | observe: Read the whole message as its recipient, including the stated opt-out. | pass: The refusal path is explicit and no penalty or false urgency is stated. | fail: Refusal is hidden, discouraged by a threat, or made conditional on compliance. | not-verifiable: The message depends on consequences or options not supplied in the pinned inputs."
```

The Design plugin writes this config when a person releases the Commission,
and each downstream Run inherits its design fields. Only `review_mode` and the
operation's permitted `mode` are derived: Generate uses `self`, Verify uses
`independent`; a revise uses `revise` unless the frozen stance is `challenge`,
which stays in `challenge` mode. The caller pins the derived config's own hash.
Goal, intent, basis, unit, criteria, acceptance and iteration budget stay frozen;
a later register edit never reaches this item's drafts. `goal` is the item's goal sentence (the same text
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
are not automatic. Each such criterion freezes `description`, `observation`,
`pass_when`, `fail_when`, and `not_verifiable_when`; a bare phrase such as
"respectful" is insufficient. The Commission editor accepts one rule per line
in this form:

```text
semantic: <criterion> | observe: <method> | pass: <observable boundary> | fail: <observable boundary> | not-verifiable: <missing/conflicting input boundary>
visual: <criterion> | observe: inspect the pinned render at <viewport/scale> | pass: <observable boundary> | fail: <observable boundary> | not-verifiable: <missing render/input boundary>
```

The `|` separators are reserved; keep them out of criterion values. Every
semantic/visual criterion needs distinct pass, fail, and not-verifiable
examples or boundaries. Visual evidence names the exact rendered target,
viewport, and scale. A config the Design plugin compiles names rule N `rNN`,
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
# Optional visual evidence, separate from the commissioned content count:
# render_manifest: {path: render/manifest.json, sha256: <hash>}
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
  - target: content/sms.txt
    criterion: r03
    status: unresolved
    evidence: "The copy offers STOP but the source does not state whether stopping changes access."
    unresolved_reason: missing_context
    next_owner: commissioning-person
    needed: "State the consequence of opting out in the approved source packet."
```

For verify, target is `<target-result-ref>::<artifact-path>`. Cover every
artifact × criterion exactly once. Verdict derives as unresolved if any row is
unresolved, else fail if any failed, else pass. An unresolved row also requires
`unresolved_reason` (`missing_context`, `criterion_ambiguous`,
`criterion_conflict`, or `inspection_limit`), `next_owner`, and `needed`.
Execution failure is not an unresolved judgment: return no Result and let the
caller record a failed/blocked Run. The checker recomputes built-ins from actual
bytes. It cannot prove subjective judgment or human authorization.

### Optional render evidence

Workers write PNGs and measurements only inside their own Result. When rendering,
pin `render_manifest` in `result.yaml`. The manifest is a nonempty JSON list;
each row has `item`, `candidate` (the source Generate Run), positive `version`,
`source` (relative to the manifest), source `sha256`, `render` (picture relative
to the manifest) and `render_sha256`, plus the renderer's measurements.
The source must be a commissioned content artifact of this Generate or a pinned
target artifact of this Verify. Pictures and manifest stay inside this Result's
`render/`; their hashes are checked without adding to `unit.count` or the
artifact × criterion grid. Pin these files before completing the Result.
The presenter reads Generate render evidence directly; Delivery lists it only
after independent Verify passes. A Verify may render into its own Result but
never add a picture to a completed Generate Result.

## Lifecycle

Allocation creates caller-owned `runtime.yaml` with run/family/operation/target,
planned status, Ticket/Result addresses, complete input manifest, worker actor,
and Ticket hash. Running adds start time. Terminal adds finish time and a reason
for failed/blocked work. The worker never writes runtime.

Generate completes only when every required check passes; a draft that fails
the records check is recorded `failed` and routed back to Generate only when a
new repair is authorized. Verify completes with pass, fail, or unresolved when
coverage and the judgment record are complete. An unresolved Result is a
completed finding, not a failed review: the caller records
`status: complete`, `terminal_outcome: unresolved`, and
`route: resolve-unresolved`. It is never ready for Delivery. The person routes
missing inputs to their owner, unclear/conflicting criteria to the Commission
owner for a clarified successor item, and inspection limits to the owner who
can supply the render or context. Preserve the Result; do not repeat Verify on
the unchanged target and criterion. A worker or tool execution failure that
prevents a trustworthy Result is `failed`/`blocked` and may be retried under
the caller's retry policy. The caller closes a run with
`design_actions.complete_run`.
The caller projects the exact independently verified candidate as ready for
Delivery. Current writes have no separate adoption receipt or decision Run.

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
and no result. Commission decisions, and explicitly supported historical
`rdNN_adopt_*` decisions, are checked for pairing and a recorded decision.
Historical Adopt records retain their real ids; no current writer creates them.
Messages use folder-relative paths and plain words
("a Generate Result requires content artifacts").

Exit 0 proves only the stated structural/check gate, not semantic quality,
independence, release validity or Page closure.

There is no adapter path. v1, `rNN_design_*`, D0–D5/GD0–GD6,
`design/DU*/`, and PageX are invalid inputs rather than readable history.
