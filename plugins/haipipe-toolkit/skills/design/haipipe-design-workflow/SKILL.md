---
name: haipipe-design-workflow
description: >-
  Native Design Workflow inside one stable Design Folder: a list of Commission,
  Generate and Verify Runs, with routes to the next Run or ready Delivery.
  Binds it across the Goal/Design/Insight/Run/Delivery Spaces, and
  coordinates with but never impersonates the Page workflow.
metadata:
  version: "0.4.0"
  last_updated: "2026-09-20"
---

# /haipipe-design-workflow · a list of Design Runs

## Version governance

Only explicit user approval may authorize `1.0.0`.

This Design skill remains exactly `v0.4.0`. Do not change the version or create
a `v1.x` release without explicit user permission.

## Run list and Routes

A Workflow is a list of Runs. Each allocated Run has a stable identity,
bounded target, actor, gate and Result or receipt. The three current Run Types
are Commission, Generate and Verify. Routes describe dependencies and the next
permitted Run; the graph below is a view of those relationships.

```text
Design.commission (C decisions; at most one release per Design Item)
  release ──────────────────────────▶ Design.generate (N)
  hold ─────────────────────────────▶ HOLD (a person may release it later)

Design.generate
  passes the records check ─────────▶ Design.verify (J)
  fails the records check ──────────▶ Design.generate (the person queues a revise, with feedback)

Design.verify
  pass ─────────────────────────────▶ Delivery (ready)
  fail ─────────────────────────────▶ Design.generate (revise)
  unresolved with complete reasons ──▶ Resolve the named evidence/criterion gap
  malformed records / execution fails ▶ Design.verify only after repair

```

Actual current Runs per Design Item: `C Commission + N Generate + J Verify`.
Count all allocated records, including held, failed, blocked and superseded Runs;
an attempt inside one Run adds no identity. C=1 when exactly one Commission record exists.
`rdNN` numbers count across the whole Design Folder.

There is no HOLD route from the agent side. HOLD is a person's decision at
Commission. A passed independent review is ready for Delivery; the agent-side
"Queue revise" exists for a failed draft or a failed review.

Every row in Run Specs is an independently closable Run
Spec. Gate and Route belong to that Run. A Workflow execution materializes
Run Instances and records the selected routes.

## Run Specs

| Spec | Type | Actor | Target | Action | Exit Gate | Result/receipt |
|---|---|---|---|---|---|---|
| `commission` | `Design.commission` | named human | one Design Item's exact config version | release/hold decision | decision names exact fingerprint | `decision.yaml` + `runtime.yaml` |
| `generate` | `Design.generate` | designer agent | the released item | generate/revise | the records check passes (integrity + self-check) | draft Result + checks + runtime |
| `verify` | `Design.verify` | fresh independent agent | named generation Results | verify | the records check passes (complete independent coverage) | verdict Result + checks + runtime |

Commission is the only human decision Run. It has one Ticket, Result, close
rule, and receipt. Individual comments/clicks are Steps or Gate events inside
that Run and never receive new Run ids. Delivery is a read-only projection,
not a Run.

## Space bindings

The Design Workbench presents the graph through five Spaces (`Space` is the only
reader-facing word, JL 260916): Goal (the Brief line and the Insight board),
Design (the items), Insight (what supports each item), Run, Delivery. Every
Run names the Design Item it serves with `item: ITEM<NN>`, and the Spaces
group by that id:

| Run or projection | Design Space | Insight Space | Run Space | Delivery Space |
|---|---|---|---|---|
| Commission | the item's goal and acceptance rules it pins; a warning when the register changed after release | the insights the Commission run record pins by hash | release/hold row: person, time, words, route | — |
| Generate | the latest draft that passed the records check, and its self-check marks | — | row: agent, time, verdict n/m, folded checks and draft text; `Generate · revise of rdNN` with its feedback | listed only after Verify passes |
| Verify | the rule marks of the draft it reviewed | — | row: independent reviewer, time, verdict n/m, folded checks; red when it fails | — |
| Delivery | ready state and exact Verify-passed candidate | — | the Verify row remains the authority | the ready draft's text is listed for handoff |

Run Space presents the same Run ids, Results, Gates, Routes, and receipts the
Folder holds. It cannot mint, rename, copy, or recount.

## Commission Run

The Design Item register lives under `outline/` (`outline/<stem>-design-items.md`); the Commission freezes one of its blocks.

The caller authors `rdNN_commission_<slug>.yaml` for the Design Item it serves
(`item: ITEM<NN>`). It pins its config (the goal sentence, stance, basis, mode,
expected, falsified, the compiled criteria, the raw rule text, unit, and
`max_iterations`) and the item's evidence files, each with sha256; it does not
pin the Brief version or venue packs. The named person records `release` or
`hold` in the paired decision Result. Only `release` routes to Generate. One
release per item: a second Release is refused. A held Commission is complete;
releasing later creates a new Commission Run and preserves the held decision.

Do not create an unsigned Commission and later back-fill the bet after seeing
candidate output. Generate and Verify inherit the released design fields and evidence
list; only `review_mode` and the permitted operation `mode` are derived as
specified in the Unit contract. An edit to the register after release reaches only a new Commission,
which means a new Design Item.

## Generate Runs

For every released independently closable target, allocate one
`rdNN_generate_<slug>.yaml`. Load `haipipe-design-unit`; generate only what the
Ticket permits. The worker writes the paired immutable Result and its checks;
the caller writes the runtime receipt (`design_actions.name_worker` before
dispatch, `design_actions.complete_run` after). Internal ideation,
renderer/model calls, revisions under the same frozen target, and self-checks
are Steps of this Run.

A draft changes only through a new Generate Run: a revise pins the base draft
and a feedback file (`outline/feedback/<run>.md`). A queued run whose pinned
file changed is never re-pinned in place: "Queue again with today's insight
files" marks it `superseded`, with the changed files as its reason, and
queues a fresh run; a revise keeps its base and feedback. A worker that dies
without a Result is put back in the queue under the same Run, with the lost
worker named on the receipt.

## Verify Runs

Allocate `rdNN_verify_<slug>.yaml` over exact generation Result hashes and
criteria. Use a genuinely fresh reviewer context. A verification Run returns a
complete pass/fail/unresolved judgment and never edits the candidate. A
generation self-check is not independent verification. A draft that already
has a completed, valid independent review is not reviewed again.

`pass` routes directly to Delivery as a ready candidate. A fail verdict routes
to a new revise Generate Run. An unresolved check with its required reason,
`next_owner`, and `needed` field is a completed judgment routed to
`resolve-unresolved`; it is never ready for Delivery. The person sends missing
evidence to its named owner, asks the Commission owner for a clarified
successor item when a criterion is ambiguous or conflicting, or supplies the
render/context required by an inspection. Preserve the unresolved Result and
do not queue the same review against unchanged pins. A malformed record or
review execution failure is recorded failed/blocked and may be retried only
after the defect is repaired. A reviewer that is not independent writes no
Result, and the run goes back to the queue.

## Delivery projection

Delivery is not a decision Run. When the latest independent Verify is complete
with verdict `pass`, the exact generation candidate it targeted becomes
`ready`. The presenter exposes its text, hash, generating Run, and verifying
Run as a read-only handoff. The presenter reads the candidate's Result-local
`render/manifest.json` and hash-bound picture. Existing `delivery/render/`
manifests remain legacy display sources. Neither replaces the Verify Result,
adds an approval step, or authorizes a worker to write outside its Result.

## Page interlock

Page Runs cannot satisfy Commission release, and Design Runs cannot approve a Page: a change to candidate content or behavior is a Design Run, a change to Page structure or explanatory prose is a Page Run.

Page and Design Workflows share the Folder, not a controller:

```text
Page RP/RE/RD/check Runs      explain, support, deliver, and verify the Page
Design Runs                  commission, generate, and verify candidates
Verify-passed candidate      one exact cross-workflow authority pointer
```

Page work never mints or renumbers Design Runs. Design work never writes Page
prose, Page approvals, or Page CHECK. A candidate change is a new Design
Generate Run; an explanatory wording-only change is a Page Writing Step.

## Status and stop rules

Only Commission → Generate → Verify is routable. The page shows only
the button an item's state allows and refuses any other action, naming the
state and who is waited on; the writer refuses a second open run for one item
and a second review of a draft with an already completed, valid independent review.
Stop Design work once the exact Verify-passed version is ready for Delivery;
implementation, distribution, and measurement belong to other families.
The presenter rechecks the Generate and independent Verify Results before
handoff. A changed artifact or broken pin displays `records invalid`, with
the repair owner and diagnostic, and is excluded from Delivery and ready totals.

Report each actual Run with type, target, actor, status, Result, Gate outcome,
Route taken, and receipt. Planned cardinality is not actual inventory.

HOLD is a person's decision at Commission and displays as `commission held`.
A `blocked` receipt displays as `blocked`, names the affected Run and repair
owner, and offers no Commission release action. A caller that cannot run a queued record (missing authority,
invalid run record, a pinned file changed since queueing, a reviewer that is
not independent) leaves it queued or replaces it, and says why; it never
re-pins in place. Preserve failed and superseded Results.

## Clean break

Unsupported Design bytes are not readable history. Historical `rdNN_adopt_*`
records from the retired flow may be read only as legacy Delivery evidence;
new writers must not create them.

Current grammar is v2 Ticket/Result plus
`rdNN_commission|generate|verify_*`. Reject v1, `rNN_design_*`,
D0-D5/GD0-GD6, `design/DU*/`, PageX, and phase-shaped Design folders. Do not
read them as compatibility history and do not offer migration.

The detailed Run contract is
[`references/run-profile.md`](references/run-profile.md).
