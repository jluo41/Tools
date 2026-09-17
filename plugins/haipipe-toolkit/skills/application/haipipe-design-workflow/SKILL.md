---
name: haipipe-design-workflow
description: >-
  Native Design Workflow inside one stable Design Folder. Defines the directed
  Run Spec graph Design.commission → Design.generate → Design.verify →
  Design.adopt, binds it across the Goal/Design/Insight/Run/Delivery Spaces, and
  coordinates with but never impersonates the Page workflow.
metadata:
  version: "0.4.0"
  last_updated: "2026-09-15"
---

# /haipipe-design-workflow · a directed graph of Design Runs

## Version governance

Only explicit user approval may authorize `1.0.0`.

This Design skill remains exactly `v0.4.0`. Do not change the version or create
a `v1.x` release without explicit user permission.

## Run Spec graph

```text
Design.commission (1)
  release ──▶ Design.generate (N)
  hold ─────▶ HOLD

Design.generate
  pass ─────▶ Design.verify (J)
  fail ─────▶ HOLD

Design.verify
  pass ─────▶ Design.adopt (1)
  revise ───▶ Design.generate
  blocked ──▶ HOLD

Design.adopt
  adopt/decline ──▶ CLOSE
  revise ─────────▶ Design.generate
  hold ───────────▶ HOLD
```

Expected actual Runs: `1 + N_generate + J_verify + 1`.

There is no Design Phase layer. Every row is an independently closable Run
Spec. Gate and Route belong to that Run. A Workflow execution materializes
Run Instances and records the selected routes.

## Run Specs

| Spec | Type | Actor | Target | Action | Exit Gate | Result/receipt |
|---|---|---|---|---|---|---|
| `commission` | `Design.commission` | named human | exact Commission/config version | release/hold decision | decision names exact fingerprint | `decision.yaml` + `runtime.yaml` |
| `generate` | `Design.generate` | designer agent | released unit/set/sequence | generate/revise | integrity + self-check pass | candidate Result + checks + runtime |
| `verify` | `Design.verify` | fresh independent agent | named generation Results | verify | complete independent coverage settles | verdict Result + checks + runtime |
| `adopt` | `Design.adopt` | named human | exact verified candidate hashes | adopt/decline/revise | exact decision + preview/handoff fingerprints | `decision.yaml` + `runtime.yaml` |

Commission and Adopt are decision Runs. The bounded decision itself has one
Ticket, Result, close rule, and receipt. Individual comments/clicks are Steps or
Gate events inside that Run and never receive new Run ids.

## Space bindings

The Design Plugin presents the graph through five Spaces (`Space` is the only
reader-facing word, JL 260916): Goal (the Brief line and the Insight board),
Design (the items), Insight (what supports each item), Run, Delivery. Every
Run names the Design Item it serves with `item: ITEM<NN>`, and the Spaces
group by that id:

| Run Spec | Design Space | Insight Space | Run Space | Delivery Space |
|---|---|---|---|---|
| Commission | the item's goal and acceptance rules it freezes | the insights the config pins by hash | release/hold row: person, time, words, route | — |
| Generate | — | — | row: agent, time, verdict n/m, folded checks and draft text | — |
| Verify | — | — | row: independent reviewer, time, verdict n/m, folded checks | — |
| Adopt | derived item state and waiting-on | — | adopt/decline/revise/hold row: person, time, words | the adopted card: text, draft hash, verifier, words |

Run Space presents the same Run ids, Results, Gates, Routes, and receipts the
Folder holds. It cannot mint, rename, copy, or recount.

## Commission Run

The Design Item register lives under `outline/` (`outline/<stem>-design-items.md`); the Commission freezes one of its blocks.

The caller authors `rdNN_commission_<slug>.yaml` and freezes the Design Item
it serves (`item: ITEM<NN>`), the exact Brief, config, target, criteria, allowed
sources, iteration budget, and `design_intent`. The named person records `release` or `hold` in the paired
decision Result. Only `release` routes to Generate.

Do not create an unsigned Commission and later back-fill the bet after seeing
candidate output. A changed Commission target/fingerprint requires a new
Commission Run and new downstream generation Runs.

## Generate Runs

For every released independently closable target, allocate one
`rdNN_generate_<slug>.yaml`. Load `haipipe-design-unit`; generate only what the
Ticket permits; write the paired immutable Result, checks, and caller-owned
runtime receipt. Internal ideation, renderer/model calls, revisions under the
same frozen target, and self-checks are Steps of this Run.

Changed target, config, source, criteria, candidate base, or feedback after
closure creates a new Generate Run with `supersedes`. An unchanged failed
attempt may append a retry trail under the same Run.

## Verify Runs

Allocate `rdNN_verify_<slug>.yaml` over exact generation Result hashes and
criteria. Use a genuinely fresh reviewer context. A verification Run returns a
complete pass/fail/unresolved judgment and never edits the candidate. A
generation self-check is not independent verification.

`pass` may route to Adopt. Review pass cannot adopt by itself: only the named person's adopt decision does. A candidate defect routes to a new Generate Run.
Missing coverage or contaminated reviewer context routes to HOLD.

## Adopt Run

The preview the person judges is rendered under `delivery/render/` and pinned by hash in the adopt decision together with the render manifest/version, so Verify and Adopt stay bound to one exact rendered version.

The caller creates `rdNN_adopt_<slug>.yaml` over exact verified candidates and
a rendered preview manifest. The named person records `adopt`, `decline`,
`revise`, or `hold`, including exact words and candidate/result fingerprints.

`adopt` and `decline` are truthful terminal outcomes. `revise` routes back to a
new Generate Run without rewriting any prior Result. The adoption receipt is the immutable adoption receipt of the item and
also the Design Folder's domain ruling consumed by Page CHECK.

## Page interlock

Page Runs cannot satisfy Commission release, and Design Runs cannot approve a Page: a change to candidate content or behavior is a Design Run, a change to Page structure or explanatory prose is a Page Run.

Page and Design Workflows share the Folder, not a controller:

```text
Page RP/RE/RD/check Runs      explain, support, deliver, and verify the Page
Design Runs                  commission, generate, verify, and decide candidates
adoption decision receipt    one exact cross-workflow authority pointer
```

Page work never mints or renumbers Design Runs. Design work never writes Page
prose, Page approvals, or Page CHECK. A candidate change is a new Design
Generate Run; an explanatory wording-only change is a Page Writing Step.

## Status and stop rules

Only Commission → Generate → Verify → Adopt is routable; every other route is HOLD.
Stop Design work once the exact adopted version is recorded in the adopt decision; implementation, distribution, and measurement belong to other families.

Report each actual Run with type, target, actor, status, Result, Gate outcome,
Route taken, and receipt. Planned cardinality is not actual inventory.

Stop at `HOLD` for missing authority, unresolved target, invalid Ticket,
unfrozen input, contaminated independent review, missing receipt, illegal
route, or changed candidate after decision. Preserve failed and superseded
Results.

## Clean break

Unsupported Design bytes are not readable history.

Current grammar is v2 Ticket/Result plus
`rdNN_commission|generate|verify|adopt_*`. Reject v1, `rNN_design_*`,
D0-D5/GD0-GD6, `design/DU*/`, PageX, and phase-shaped Design folders. Do not
read them as compatibility history and do not offer migration.

The detailed Run contract is
[`references/run-profile.md`](references/run-profile.md).
