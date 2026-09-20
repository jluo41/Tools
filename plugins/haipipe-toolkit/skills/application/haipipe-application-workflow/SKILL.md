---
name: haipipe-application-workflow
description: >-
  Crossing orchestrator for an Application's InsightBoard and DesignBoard.
  Preserves the Insight workflow, native Design workflow, and Design Folder's
  Page workflow as separate authorities; validates X0-X3 crossings, creates the
  shared Workflow Runtime view, and delegates one runnable unit. Use for
  whole-Application status or cross-board routing.
metadata:
  version: "3.0.1"
  last_updated: "2026-09-15"
---

# /haipipe-application-workflow · cross without flattening

Load `haipipe-application`, `haipipe-folder`, `haipipe-insight-workflow`, and
`haipipe-design-workflow`. Load `haipipe-page-workflow` only for a Page-facing
action. Sibling workflows retain their own RunTypes, control policies,
owner-native Run identities, and receipts. The Application layer owns the
cross-board Workflow Runtime view; it does not mint a duplicate Gate or Run.
Read `../../task/haipipe-workflow/ref/workflow-runtime.md` when creating or
auditing that cross-board Runtime view.

## Ownership graph

```text
haipipe-insight-workflow    I0–I5 RunTypes · one derived Question Group + one register cell
haipipe-design-workflow     Commission/Generate/Verify/Adopt RunTypes · one design target
haipipe-page-workflow       Page RunTypes · rp-struct-01/rpNN/release/CHECK · one readable Page
haipipe-application-workflow
                            X0–X3 crossing assertions + delegation only
```

There is no Application P0–P4 and no combined Design/Page phase scalar.
The Application Runtime is an aggregate frontier/receipt over these native
workflows; it is not a new Level-4 Run.

## Crossing graph

```text
Design Brief need
        │ X0
        ▼
I1 Question → I2 Data → I3 Information → I4 Knowledge → I5 Wisdom
        │ X1 · settled + signed handoff
        ▼
Commission → Generate → Verify → preview → Adopt
                                      │ same domain ruling
                                      ▼
                 Design Page release → fresh CHECK
                                      │ X2
                                      ▼
                     downstream Task implementation/fielding
                                      │ measured Result · X3
                                      ▼
                            new/reopened I2 Folder
```

X0 and X1 are inside the Application. X2 and X3 are outer boundaries; this
workflow never builds, sends, allocates, executes, or measures.

## X0 · Brief need to Insight question

- BR00 owns one neutral need id and target rung.
- Exactly one Insight register owns the reciprocal QD/QI/QK/QW id.
- The scheduling/status coordinate is derived as
  `QG-<partition>-<target-rung>`; it is never stored as a Folder or authority.
- Neither side contains a preferred answer.
- The need stays open until that register reaches a legal terminal.

## X1 · signed W handoff to Design Commission

- I5 reached Page `CHECK/CLOSE`; the W handoff is contextual, signed by a
  person, and its I1 cell is settled at GI6 under the Insight workflow.
- If W used a Task RF parent, W's Evidence graph pins that exact native
  instance/item/version/Result. The RF itself does not cross directly.
- The DesignBoard `reads:` authorizes the W source.
- The Commission and v2 Ticket pin the exact frozen W handoff
  path/Page-version/content-hash, signature, and GI6 receipt with role
  `handoff`, and name why it applies to this audience/job/venue.
- A static W handoff has no invented Supporting Run id. No D/I/K prose, Page
  `rpNN`, or raw Task output becomes Design authority.

This crossing is Design-domain authority, not a Page Evidence shortcut. Any
factual claim on the Design Page separately uses a typed item under
`outline/evidence/` and the current Page evidence contract.

## X2 · adopted candidate to downstream Task

Native X2 requires all of the following:

- exact generation Result/member hashes;
- complete passing independent verification for the selected members;
- recipient-view render manifest/version;
- signed handoff versions and immutable human adoption receipt;
- released Design Page projection and fresh terminal CHECK bound to the same
  adoption as its `domain-gate`;
- one explicitly named downstream Task Folder, task type, and requested action.

Write a new immutable packet; never overwrite a previous revision:

```yaml
schema: haipipe.application-candidate/v2
packet_id: <Design-NN>-<candidate-slug>-v<N>
packet_version: <N>
state: proposed
source:
  application: <application-root>
  design_board: <board-path>
  folder: <Design-folder-path>
  generation_results: [<result.yaml path@sha256>]
  selected_members: [<artifact path@sha256>]
  verification_results: [<result.yaml path@sha256>]
  handoffs: [<W handoff path@sha256>]
  render: <manifest path@sha256>
  adoption: <decision receipt path@sha256>
  page:
    source: <Design page path@sha256>
    release: <Page release receipt path@sha256>
    check: <terminal CHECK receipt path@sha256>
target:
  folder: <target-task-folder>
  task_type: <target contract key>
  requested_action: <build | field | deploy | measure>
```

The target Task decides how to bind these inputs and allocate its own Runs.
The Design Folder and Page are not fabricated as Supporting Runs. Missing any
required target/source/version/authority row is `X2 HOLD`.

## X3 · measured effect back to Insight

- Resolve the real downstream Task Run/Result/report identity.
- I2 records it as run-bound Data, not as an edited Design claim.
- Reopen only dependent I/K/W and current Design/Page bindings. Preserve the
  old adopted candidate and its historical decision.

## Frontier and dispatch

Report four coordinates:

```text
insight:     <board> · <QG-partition-rung> · <cell> · I0..I5 · gate · next
design:      <board> · <commission/Run/result> · verify/adoption · next
design-page: <rp-struct-01/rpNN/release/CHECK> · projection freshness · next
crossing:    none | X0 | X1 | X2 | X3 · assertion/hold
runtime:     <workflow_runtime_id> · running | held | complete | failed
```

Dispatch:

1. Resolve Application root and exact Boards/Folders.
2. Read all three native frontiers from disk.
3. Validate a pending crossing before delegation.
4. Honor a user-named board/Run/Page interaction exactly.
5. Otherwise finish a ready crossing, then delegate the earliest runnable unit
   without crossing a human gate.
6. Re-read frontiers and write receipts only on owning surfaces.
7. Stop at the first owner gate or named hold.

```text
Insight unit     → /haipipe-insight-workflow
Design unit      → /haipipe-design-workflow
Design Page unit → /haipipe-page-workflow
```

## Receipts and human gates

```text
X0  BR00 log + Question log
X1  W log + consuming Commission/Design decision index
X2  Design adoption/crossing index + downstream workflow inbox packet
X3  Task Result/report + I2 log
```

This crossing layer adds no human gate. It preserves:

```text
Insight  ✋ Page SURVEY Decide for a new Supporting Run · ✋ sign W handoff
Design   ✋ release exact Design Commission · ✋ adopt exact candidate
Page     adoption is reused as domain-gate; CHECK never repeats selection
```

These are cross-RunType authority controls. Shape approval, evidence verification,
and acceptance remain nested Page-Face controls. A Page Run `rpNN` closing is
neither Page `CLOSE` nor a GI/X transition.

## Stop and clean break

Stop at an unresolved assertion, sibling human gate, conflicting owner, or
accepted/current X2 boundary. Never poll or infer consent.

This workflow does not read or adapt PageX, D0–D5/GD0–GD6,
Division/PageDown receipts, or v1 candidate packets. Current crossings use v2;
non-current inputs stop as unsupported.

Return status, the four frontiers, receipts written (or none), and one next
bounded action.
