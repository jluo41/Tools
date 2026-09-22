# Page Workflow Runtime contract

This file specifies the automated Page controller. Its durable object is one
Workflow Runtime/pass, not an `rp-*` Page Run. The low-level controller keeps
`run`, `cycle`, and `next_cycle` fields as serialized dispatch coordinates (receipts before 2026-09-22 say `phase`);
they are not Run authority, Run Specs, or Run identities.

Interactive writing uses `interactive-writing-run.md`. Its fixed-scope RP Run
owns Version/Step history. A controller HOLD ends one pass, not the persistent
writing goal. Controller CLOSE means whole-Page closure, not acceptance of one
Writing Version.

The executable controller is
`../../../../board/haipipe-board/ref/page-lifecycle.workflow.js`; the auditor is
`../../haipipe-page/src/page_lifecycle.py`. This contract preserves
their current serialization so the workflow still runs.

## Runtime and Run boundary

```text
Page Workflow Definition  graph compiled from Run Spec-owned Routes
Page Workflow Runtime     one controller execution + frontier + receipts
RP / RE / RD Runs          independently closable Page Run Instances
controller dispatch       internal orchestration record; not another L4 Run
```

Gate and Route belong to the owning Run Spec/Instance. The Workflow Runtime
records the actual evaluation and chosen cross-Run route. A controller label
becomes a separate Run only when it has its own stable id, Ticket, bounded
target, Result, receipt, and independent close.

## Raw-material packet

The current executable adapter requires this shape:

```yaml
run_id: 260804-2130-QB5        # Workflow Runtime/pass id; not an rp-* id
board: /absolute/path/to/board-folder
page: group/QB5-page-loop.md   # board-relative
start_phase: CHECK             # serialized dispatch label
intent: audit and improve the automatic Page loop
mode: copilot                  # copilot | auto
sources: []
related_context:
  command: pagecontext.py <page> --run check
  traversal: one-hop
  packet: "# Related Board Pages ..."
constraints: []
page_ruling: none              # none | domain-gate | local
human_gate:
  required: false
  rule: all Aims met or explicitly held
limits:
  max_steps: 12
  max_rounds: 3
```

Required fields are `run_id`, `board`, `page`, `start_phase`, and `intent`.
Semantically, `run_id` is the current `workflow_runtime_id`; it must never use
or consume an RP/RE/RD/Task Run identity.

For a new Page, CREATE scaffolds/registers the persistent Page and this Runtime
begins with CONTEXT. For an existing Page with unknown next work, begin with
CHECK so a fresh judge routes without editing.

## Human control

The set of person-reserved acts is the same in both modes:

```text
copilot  unanswered selected human Gate produces HOLD
auto     declared review ticks may defer; branching choices never auto-resolve
```

`Decide` is a branching Gate, not a review tick. Auto must HOLD when no durable
owner decision/default supplies it. No machine writes a person's approval,
verification, acceptance, release, or adoption.

`human_gate` in a controller receipt is a pointer to durable evidence, never
the tick itself. Its `required` value must match the packet on every dispatch.

## Controller receipt

Each dispatch appends one ordered receipt:

```json
{
  "step": 4,
  "round": 1,
  "phase": "CHECK",
  "cycle": "CHECK",
  "actor": "haipipe-page-check-agent",
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
  "route": "CONTENT",
  "next_cycle": "WRITE",
  "requested_route": "CONTENT",
  "reopens_promise": false,
  "reason": "A3.1 lacks visible evidence",
  "artifacts": [],
  "evidence": ["QB5-page-loop.md#A3"],
  "findings": ["A3.1 is asserted but not demonstrated"],
  "human_gate": {"required": false, "status": "not-required", "evidence": []}
}
```

Interpretation:

- `run` selects the worker/dispatch group only;
- `cycle` records the internal controller action;
- `route` records the actual next dispatch or terminal outcome;
- `reason`, evidence, findings, and Gate pointer explain the decision;
- version hashes make the built Page identity auditable;
- this receipt does not mint a Page Run.

## Required receipt invariants

| Field | Rule |
|---|---|
| `step` | exact 1-based receipt position |
| `round` | positive and within packet limits |
| `run` | current Run key; equals prior nonterminal route |
| `cycle` / `next_cycle` | valid action labels for current/next dispatch |
| `route` | legal destination; terminal receipt is CLOSE or HOLD |
| `actor` | non-empty and role-correct |
| `builder_actor` | non-empty and separate where required |
| `role` | producer except CHECK judge |
| `status` | blocked/failed must HOLD |
| version fields | lowercase SHA-256 source/render pair with continuity |
| CHECK identity | before, after, and checked version identical |
| verdict | pass may CLOSE/HOLD; revise routes to an owning worker |
| reason | non-empty authority/route explanation |
| artifacts/evidence/findings | JSON lists |
| human Gate | shape matches packet; required CLOSE needs durable evidence |

Only the exact source/render identity observed by a fresh CHECK may CLOSE.
Any content edit creates a new version and invalidates that CHECK.

## Dispatch routes

These labels are the current adapter grammar:

```text
CONTEXT  → CONTEXT | OUTLINE | HOLD
OUTLINE  → CONTEXT | OUTLINE | EVIDENCE | CONTENT | HOLD
EVIDENCE → CONTEXT | OUTLINE | EVIDENCE | CONTENT | HOLD
CONTENT  → CONTEXT | OUTLINE | EVIDENCE | CONTENT | CHECK | HOLD
CHECK    → CLOSE | CONTEXT | OUTLINE | EVIDENCE | CONTENT | HOLD
```

The owning Run's semantic Route must point to a Run Spec admitted by the
Workflow graph. The adapter maps that selection to these labels. `SHAPE`, `SURVEY`,
`LAND`, `EMBED`, and `WRITE` are internal action/cycle labels and never Run
Specs merely because they appear in `next_cycle`.

HOLD is terminal for one controller pass and preserves the exact unresolved
Gate/input/failure. Continuation creates/resumes the appropriate Workflow
Runtime and owner-native Run according to the current graph.

## Role separation

```text
controller  records legal route/frontier; edits no Page prose
producer    performs one bounded dispatch action
builder     builds/checks/hashes; no semantic acceptance
judge       fresh CHECK over immutable source/render identity
human       supplies person-reserved Gates or bounded decision Runs
```

Producer, builder, and judge must be distinct for one version. A human
decision is a separate Run only when independently commissioned and closable;
otherwise it remains a Gate/Step in the owning Run.

## Page Run families

`../../haipipe-page/ref/page-run-families.md` owns:

- RP: fixed-scope human-feedback Structure/Section/paragraph Runs;
- RE: item-scoped VALUE/CITE/DISPLAY evidence Runs;
- RD: target-scoped delivery Runs.

The Workflow Runtime may coordinate them but never renames, duplicates, or
recounts them. A Task/Discovery Supporting Run keeps its native identity.

## Durable audit bundle

The controller writes:

```text
<board>/_runs/page/<page-id>/<run-id>.json
```

Audit it with:

```bash
python3 <toolkit>/skills/board/haipipe-board/cli/pageflow.py audit <receipt.json>
```

The auditor recomputes source/render hashes. Store `page` board-relative; an
absolute/stale path is a defect even if a unique filename fallback permits
inspection. Mechanical error counts are Page-scoped, not Board-scoped.

Do not append CHECK output to the just-checked Page or Folder log: that would
change the closed version. Terminal evidence stays in the audit bundle or the
declared review surface.

## Historical adapter receipts

The executable auditor can still inspect stored DRAFT/REVISE/COMPILE/PROBE
receipts. That is audit-only behavior for the Page controller and grants no
current dispatch, write, Run identity, or Workflow authority. Current packets
use the routes above.

## Required fault tests

Exercise:

- straight CLOSE and evidence-loop paths;
- every legal backward route;
- producer/self-judge and judge/builder violations;
- changed source/render after CHECK;
- illegal route and nonterminal trace;
- required human Gate absent and explicit HOLD;
- packet/runtime mismatch and version discontinuity;
- max-step/max-round bounds;
- historical adapter receipt audit without current dispatch authority.

Passing only the common route is not evidence that the controller works.
