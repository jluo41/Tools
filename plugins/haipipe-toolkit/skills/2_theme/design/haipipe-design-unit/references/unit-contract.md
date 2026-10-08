# Design unit contract

Owner: `haipipe-design-unit` for what the worker reads and writes. The caller (`haipipe-design-workflow`, with
`haipipe-design`'s scaffold) owns allocation, the Run card, the Job's fence, Task opening, projection, release and
closure. Two contracts live here: the ladder's (every new design Run), then the older boards' v2 Ticket.

## Ladder

### The Ticket

A ladder Run has no separate Ticket file. It is the Run folder the caller made and froze before dispatch:

```text
<Task>/runs/run-<type>-<target>/run.yaml    run · kind · type · scope · target · skill · agent · signs · status ·
                                            by · started_at · finished_at · usage
<Job>/<Job>.md                              front matter: goal · method (MNN m<k>) · method-sha · inputs (i<N>) · n
<Job>/inputs/                               goal.md · method.md · links into ../inputs/i<N>/ · manifest.yaml
```

`type` is one of `reason` (t00), `generate`, `verify` (a design Task), `rank` (t99), all `kind: hard`, and `revise`
(a design Task, `kind: soft`, one pass per draft). The target is the Task's: `t00`, `d<NN>`, `d<NN>-v<k>` (a verify
names the draft it reads), `t99`. Older names `rNN_<type>_<target>/` stay readable.

The worker reads `inputs/method.md` (front matter `method · version · steps` with the pinned version's choice at
each of ① – ⑤) for its step, and only the fence's files. `manifest.yaml` lists every fence file:

```yaml
inputs: i2
frozen: '<YYMMDD>'
method: method.md
parts:                       # step ①'s parts: which file serves which
- {part: Goal · how much is set, choice: <what>, file: goal.md}
files:
- {path: goal.md, source: written, sha256: <sha>}
- {path: method.md, source: <registry version, e.g. haipipe-design-method M04 m2>, sha256: <sha>}
- {path: rules.md, source: ../../inputs/i2/rules.md, sha256: <sha>}
```

`sha256` holds the first 12 hex of the file's sha256.

A fence file whose content no longer matches its `sha256`, a link that does not resolve, or a step `method.md` does
not define is a hold: the worker writes no Result and names the problem.

### The fence rule

Every `from` (a topic or a step in `chains.yaml`, an element in `elements.yaml`) is either exactly `own knowledge`
or names a fence file: its path or name or stem (`rules.md`, `rules`), its stem word followed by an id with a digit
(`rule r2.1`), or an id with a digit inside its name (`W-03 row 2` for `handoff-W-03.md`), with an optional locator
after it. Nothing else is a source: prose that only shares a word with a file name does not pass. A step's own
`from` overrides its topic's.

### Results by type

```text
reason    result/chains.yaml   topics[id, title, from, steps[says, so, from?], ideas]
          result/ideas.yaml    ideas[id, idea, topic, design, name]
          result/topics.md     the readable report
generate  result/design.md     the design, word for word (a UI: result/content/screen.html + render/)
          result/elements.yaml [element, words, from, because, step: ③, changed]; project_draft.py draft carries
                               it into the Task's elements.yaml
revise    passes/pNN-<MMDD>/design.md · elements.yaml · feedback.md (the pass is draft k = 1 + its number)
verify    result/review.md     each test, its verdict, its evidence, what to change; run.yaml carries
                               status: passed | failed, tests: {T0, T1[, T2]} and by
rank      result/ranking.csv   rank,design,predicted,why,kept (kept yes | no, exactly N yes)
          result/coverage.md   the kept N against the goal
```

A hard Run writes nothing outside its `result/` (and its own card). Faces, `elements.yaml`, `prediction.yaml` and
`state:` are `haipipe-design-workflow`'s projections (`project_draft.py`, `project_predictions.py`). A verify's or rank's `by` is never the actor of the generate or revise it reads.

### Checks

`python3 scripts/check_unit.py --ladder-result <run folder>` checks the Run's name and kind, its Result's shape for
its type (every idea has a `name`), the fence rule for every `from`, a verify's independence (its `by` set and
different from the generator's), and that a ranking keeps the face's N. It is read-only and structural.

## Older boards · Ticket and Result contract v2

An older Design Folder board keeps this contract; the ladder never writes it.

Owner: `haipipe-design-unit` for worker inputs/outputs; the caller's Run Profile
owns allocation, release, runtime, lifecycle, and promotion. v2 is the only
accepted Ticket/Result schema; v1 is rejected.

### Ticket

A Run is `<owner>/runs/run-design-<generate|verify>-<MMDD>-<slug>.yaml` (older
`rdNN_*` names are retired), paired with
`<owner>/results/<same-stem>/`. Resolve Ticket references from the owner and
Result-local references from the Result directory. Every reference names one
regular file by path; no content hash (JL 260928). Never dispatch YAML through bash.

```yaml
schema: haipipe.design-ticket/v2
run: run-design-generate-0918-design-1
operation: generate
item: ITEM01            # the Design Item this Run serves (register id)
worker: haipipe-design-unit
actor: designer-context-01
target: Send the salience wording unchanged
config: {path: scripts/config/run-design-generate-0918-design-1.yaml}
approval:
  actor: <person>
  record: {path: results/run-design-commission-0918-design-1/decision.yaml}
inputs: []  # role + path; optional real upstream run_id
targets: [] # verify only: exact generation result.yaml refs
```

The slug is the design as the screen says it (`ITEM01` -> `design-1`); a second run of
the same step, day and design gets `-2`, `-3`. Order is the ticket's `sequence:`, counted
across the whole Design Folder, so ITEM02's first Run may be sequence 5. The
approval record is the released Commission's `decision.yaml` under
`results/`.

`item` names the Design Item register row (`draft/<stem>-design-items.md`)
this Run serves. The checker does not interpret it; the Design workbench groups
Runs by it. Commission Tickets carry it too. Historical Adopt Tickets may be
read for audit only; they are never new worker inputs or current workflow gates.

Roles: `evidence | inspiration | reference | avoid | base | feedback | handoff`.
Role never promotes authority. `run_id` normally names a real Supporting/native
Run. An `rpNN` Page Run may enter only as frozen `feedback` to a revise Run; it
cannot become evidence, handoff authority, or the producer of a Generate
Result. A revise Generate's `feedback` input is `draft/feedback/<run>.md`,
written when the revise is queued. Static
Briefs and signed W handoffs omit Run ids.
Design callers validate W signing/applicability, Board reads, and allowed input
scope. The approval receipt is a person's release of an already-written
commission/config. The worker cannot create or infer it.

### Frozen v2 config

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

The Design workbench writes this config when a person releases the Commission,
and each downstream Run inherits its design fields. Only `review_mode` and the
operation's permitted `mode` are derived: Generate uses `self`, Verify uses
`independent`; a revise uses `revise` unless the frozen stance is `challenge`,
which stays in `challenge` mode. The caller names the derived config file.
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
distinguishing/failure condition. See `legacy/modes.md`.

`unit.shape` is single, sequence, or set; positive `count` is the number of
content artifacts. Each member has a stable Result-local path. Choosing a
subset later references those exact files. Modes are compose, revise,
brainstorm, theory-driven, challenge. Basis is brief-only or evidence-informed.
A revise Ticket requires base + feedback; evidence-informed requires evidence
or handoff. Generate uses self review; verify uses independent review.

Criteria have unique ids. The kinds are `max_chars`, `contains`, `excludes`,
`starts_with`, `ends_with`, `semantic`, and `visual`. The first five are
built-ins the checker recomputes per UTF-8 artifact; `ends_with` compares the
draft with trailing whitespace stripped, `starts_with` with leading
whitespace stripped. `max_chars` does not count the `{LINK}` slot, which the
sending platform fills with the real link later (JL 261001). `semantic` and `visual` name an observation method; they
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
viewport, and scale. A config the Design workbench compiles names rule N `rNN`,
plus `rNNb`, `rNNc` for a rule quoting several phrases. Mode-specific
rationale/forecast/member provenance must be explicit commissioned
deliverables and criteria before release.

### Result

```yaml
schema: haipipe.design-result/v2
run: run-design-generate-0918-design-1
operation: generate
target: Send the salience wording unchanged
producer: designer-context-01
verdict: pass
artifacts:
  - {path: content/sms.txt}
checks: {path: checks.yaml}
targets: []
# Optional visual evidence, separate from the commissioned content count:
# render_manifest: {path: render/manifest.json}
```

Ticket and Result schema versions must match. Verify has no replacement
artifacts and reproduces target paths exactly. Every file the Result names
(content, checks, render) must not be newer than `result.yaml`; a later edit
reads as stale by file time. Optional review prose may live in
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
name `render_manifest` in `result.yaml`. The manifest is a nonempty JSON list;
each row has `item`, `candidate` (the source Generate Run), positive `version`,
`source` (relative to the manifest), and `render` (picture relative to the
manifest), plus the renderer's measurements.
The source must be a commissioned content artifact of this Generate or a named
target artifact of this Verify. Pictures and manifest stay inside this Result's
`render/`; they are checked by path and file time without adding to `unit.count`
or the artifact × criterion grid. Write these files before completing the Result.
The presenter reads Generate render evidence directly; Delivery lists it only
after independent Verify passes. A Verify may render into its own Result but
never add a picture to a completed Generate Result.

### Optional element record

A design is made of elements: for a message, its sender, its greeting, the news,
the ask, the reason, the link and the opt-out. When a criterion commissions it
(a semantic rule that observes `elements.yaml`), a Generate writes one entry per
element of the design, in reading order, and names the file in `result.yaml` as
`elements: {path: elements.yaml}`:

```yaml
- element: sender                  # the part's role in the design
  words: "<greeting>, it's {SENDER}."
  from: requirements               # requirements | internal | external | intuition
  source: "Design Goal: personalization"   # the rule, insight row or theory; none for intuition
  thinking: reasoned               # reasoned (System 2) | intuitive (System 1)
  because: the goal requires the sender placeholder, and a known sender reads as safe
  alternatives: ["<another sender line>"]   # options weighed, when there were any
```

Element names: when the board's Design Goal names its elements (`Elements:` under
Resources), the workbench gives every new Design Item a rule that commissions this
record and lists those names; an entry for one of them keeps its name (`sender`, not
`from`), and any other element is named for its role. The Design Space's element matrix
reads the record by these names.

`from` says which input the element rests on; `thinking` says how it was chosen.
A reasoned element writes its `because`. An intuitive element is a labeled hunch:
it records the hunch and names no source, and it never becomes warrant; its
`because` may stay empty. Record the observable choice, not private
chain-of-thought. Write the file before `result.yaml`; like content, it must
not be newer. The Verify checks it against the commissioned criterion, and the
workbench's Design elements fold shows it beside the text.

### Lifecycle

Allocation creates caller-owned `runtime.yaml` with run/family/operation/target,
planned status, Ticket/Result addresses, complete input manifest (paths), and
worker actor. Running adds start time. Terminal adds finish time and a reason
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
is stale when one of its `inputs` or `targets` is newer than the Ticket. A
closed run (complete, failed, blocked) reads its inputs as history, so their
later edits do not void it; a closed Verify is still stale when a target
Result is newer than its own `result.yaml`, and every Result's files are held
to that Result's `result.yaml`. The config and approval record are frozen
copies written with the Ticket and are checked for existence only, so a fresh
checkout (which writes `scripts/` after `runs/` and `results/`) never reads as
stale. A `superseded` run (a queued run
replaced after a named file changed) needs a reason in `failure` and no
result. Any hash field left in an older record is ignored. Commission decisions, and explicitly supported historical
`run-design-adopt-*` decisions, are checked for pairing and a recorded decision.
Historical Adopt records retain their real ids; no current writer creates them.
Messages use folder-relative paths and plain words
("a Generate Result requires content artifacts").

Exit 0 proves only the stated structural/check gate, not semantic quality,
independence, release validity or Page closure.

There is no adapter path. v1, `rNN_design_*`, D0–D5/GD0–GD6,
`design/DU*/`, and PageX are invalid inputs rather than readable history.
