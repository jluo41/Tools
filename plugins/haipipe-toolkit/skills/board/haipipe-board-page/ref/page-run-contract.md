# Page RUN contract

`RUN` is the bounded router for one persistent Page. It does not mean
`ADVANCE`: Page work is non-linear, so the next authority may repeat, branch,
return to DRAFT in a new round, close, or hold.

The executable controller lives in
`../../haipipe-board/ref/page-lifecycle.workflow.js`. The deterministic auditor
lives in `../../haipipe-board/src/page_lifecycle.py`. This file owns the packet
and receipt they share.

## Raw-material packet

The caller supplies facts and authority, not a proposed paragraph formula.

```yaml
run_id: 260804-2130-QB9
board: /absolute/path/to/board-folder
page: /absolute/path/to/QB9-page-loop.md
start_phase: CHECK              # DRAFT | PROBE | REVISE | CHECK
intent: audit and improve the automatic Page loop
sources:                       # exact files the run may rely on
  - /absolute/path/to/source.md
related_context:               # derived from this Page's Files for start_phase
  command: pagecontext.py <page> --phase CHECK
  traversal: one-hop
  packet: "# Related Board Pages ..."  # exact bounded Markdown handed to the phase
constraints:                   # settled rulings that no phase may reopen silently
  - Page is not a configuration
human_gate:
  required: false
  rule: all Aims met or explicitly held
limits:
  max_steps: 12
  max_rounds: 3
```

Required fields are `run_id`, `board`, `page`, `start_phase`, and `intent`.
The caller resolves the stable Page Type before dispatch. A missing source,
unknown gate, or ambiguous authority is a named HOLD, never a guessed input.

Before every phase dispatch, the controller resolves `### 🔗 Related Board
Pages` with `../../haipipe-board/cli/pagecontext.py`. Only rows matching that
phase or `ALL` enter the packet. A `§n` scope brings the target Page identity,
Opening, requested Content division, and matching Aims/States group; `page`
brings the whole target. Traversal stops after that one hop even when the target
declares more related Pages. A malformed row, dead target, Page-id mismatch, or
missing scope is a named HOLD. If CHECK routes to a different authority, the
controller rematerializes context for the new phase rather than reusing CHECK's
packet.

For a new Page, CREATE scaffolds and registers the persistent Page first; RUN
then begins at DRAFT. For an existing Page whose next need is unknown, RUN
begins at CHECK so a fresh judge routes the visible version.

## Phase receipt

Every attempted phase returns one receipt. The controller normalizes it to this
shape and preserves all receipts in order:

```json
{
  "step": 4,
  "round": 1,
  "phase": "CHECK",
  "actor": "haipipe-board-reviewer-agent",
  "role": "judge",
  "builder_actor": "fresh-page-builder",
  "status": "ok",
  "version_before": "source-sha256:render-sha256",
  "version_after": "source-sha256:render-sha256",
  "checked_version": "source-sha256:render-sha256",
  "source_sha256": "64-lowercase-hex-characters",
  "render_sha256": "64-lowercase-hex-characters",
  "mechanical_errors": 0,
  "mechanical_warnings": 0,
  "verdict": "revise",
  "route": "REVISE",
  "requested_route": "REVISE",
  "reopens_promise": false,
  "reason": "A3.1 lacks visible evidence",
  "artifacts": [],
  "evidence": ["QB9-page-loop.md#A3"],
  "findings": ["A3.1 is asserted but not demonstrated"],
  "human_gate": {"required": false, "status": "not-required", "evidence": []}
}
```

The minimum auditable identity is the SHA-256 of the Markdown source joined to
the SHA-256 of its rendered HTML. The auditor requires lowercase 64-character
hex digests and verifies that `version_after` is exactly
`source_sha256:render_sha256`. `builder_actor` identifies who produced that
snapshot. Every receipt's `version_before` must equal the preceding receipt's
`version_after`. CHECK is valid only when `version_before`, `version_after`, and
`checked_version` are identical. Any content edit creates a new version that
must be checked again.

`reason` names the authority exercised, not merely the file operation. A route
to DRAFT from PROBE, REVISE, or CHECK sets `reopens_promise: true` and increments
the round. Repeated DRAFT within the same unsettled promise does not.

## Legal routes

```text
from DRAFT    → DRAFT | PROBE | REVISE | CHECK | HOLD
from PROBE    → PROBE | REVISE | DRAFT | CHECK | HOLD
from REVISE   → REVISE | PROBE | DRAFT | CHECK | HOLD
from CHECK    → CLOSE | REVISE | PROBE | DRAFT | HOLD
```

Only CHECK may CLOSE. CLOSE is a route, not a fifth Page Phase. HOLD is also a
terminal route: it preserves a named unresolved gate, missing input, tool
failure, concurrency mismatch, or exhausted limit without pretending quality
was achieved.

## Role separation

```text
controller   chooses and records the next legal route; edits no Page prose
producer     performs DRAFT, PROBE, or REVISE; may not approve its own version
builder      rebuilds, runs mechanical checks, and identifies the version
judge        performs CHECK read-only against that exact version
human        supplies any ruling required by the Page Type or local contract
```

The producer, builder, and judge for one version must have distinct actor
identities. The builder may report deterministic defects but does not make
semantic claims. The controller may stop a run for safety, but cannot turn that
stop into CLOSE.

## Durable audit bundle

The Workflow result is written to:

```text
<board>/_runs/page/<page-id>/<run-id>.json
```

`_runs/` is outside Page discovery and never renders as a Board Page. The
bundle contains the original packet, ordered receipts, final version, terminal
route, and limit values. It is checked with:

```bash
python3 <toolkit>/skills/board/haipipe-board/cli/pageflow.py audit <receipt.json>
```

The CLI resolves `board` and `page` from the receipt, locates the rendered Page
under `<board>/board/`, and independently recomputes both SHA-256 digests. A
well-formed receipt still fails if the files currently on disk do not equal its
`final_version`. Thus version evidence is not accepted merely because an agent
wrote the same claimed hash into several fields.

Do not append a CHECK result to the Page's own Log after approval: that would
change the just-checked version. DRAFT, PROBE, and REVISE may update the Page
Log as part of the version they produce; terminal CHECK evidence stays in the
audit bundle or the Page Type's declared review surface.

## What the audit can prove

The audit can prove that the declared process was followed: the preserved
packet matches the run, routes and version handoffs were legal, rounds changed
for the right reason, producer/builder/judge stayed separate, CHECK observed an
immutable version, human gates were not fabricated, and bounded loops stopped
honestly.

It cannot prove that an arbitrary claim is true merely because the process
passed. High confidence comes from combining three kinds of evidence:

1. deterministic mechanics from `check.py` and the lifecycle auditor;
2. fresh-context semantic judgment against the Page's declared requirements;
3. direct evidence or an explicit human gate for claims a machine cannot settle.

The final record therefore says what passed, what evidence was inspected, and
what residual risk remains. It never says “quality guaranteed” without naming
the gate and its evidence.

## Required fault tests

The shipped harness must exercise at least these cases:

```text
happy paths     DRAFT→CHECK→CLOSE; DRAFT→PROBE→REVISE→CHECK→CLOSE
legal loops     CHECK→REVISE→CHECK; CHECK→PROBE; CHECK→DRAFT(new round)
faults          producer=self-judge; version changed after CHECK; illegal route
gates           required human approval absent; explicit HOLD
bounds          max steps reached; non-terminal trace; failed or blocked worker
integrity       packet/run mismatch; broken version continuity; symbolic hashes
```

Passing only the common route is not evidence that the router works. Branch and
fault coverage are part of the Page lifecycle contract.
