# Codex Suggestions — Board-first HAI Paper Stage

Status: historical consolidation of the 2026-07-25 discussion. Active decisions and finish lines now live in QC3 and QG, QH, and QI on this Board; this file is not a runtime contract.

## Direction already established

- The Board is the remote interaction and control plane. The user should see the lifecycle, queues, comments, gates, progress, and handoffs on the Board rather than in a CLI or a long-lived coding session.
- A Claude Code, Codex, or sub-agent session is an ephemeral worker. It may disappear after one queue item because the durable context and state live on the wire page.
- One lifecycle stage or independently gated unit has one canonical S wire page. The page contains its substance, open work, comments, current state, and completed handoffs.
- An existing Display request goes directly into that Display's `S-Display-N` page. A new unallocated Display first enters the Display stage page and moves into its new `S-Display-N` page when the unit is created.
- Do not create `_DISPLAY_REQUEST.md`, a request file per change, or a separate Handoff sidecar.
- A Section refers to a stable `display_id`. It does not copy a table, pin itself to a candidate filename, or edit the Display unit directly.

## Proposed architecture

```text
┌──────────────────────────────── BOARD ────────────────────────────────┐
│ lifecycle bar · S wire pages · Content · Items to Finish · comments │
│ state · gate · preview · Work this item / Work this queue            │
└──────────────────────────────┬────────────────────────────────────────┘
                               │ page path + optional item id
                               ▼
┌────────────────────── haipipe-paper-stage ────────────────────────────┐
│ resolve stage · read one contract · read the page · claim an item    │
│ read requires/style-from · choose a worker · enforce gate/boundary   │
└──────────────────────────────┬────────────────────────────────────────┘
                               │ narrow task packet
                               ▼
┌──────────────────────── EPHEMERAL WORKER ─────────────────────────────┐
│ draft/revise · probe · display renderer · task agent · checker       │
│ Claude Code / Codex / fresh sub-agent                                │
└──────────────────────────────┬────────────────────────────────────────┘
                               │ result + artifacts + verification
                               ▼
┌──────────────────────── SAME WIRE PAGE ───────────────────────────────┐
│ update Content · check To Do · write handoff · update state · log    │
└───────────────────────────────────────────────────────────────────────┘
```

The Board is not merely a renderer that is synchronized after CLI work. It is where work starts, where the human steers it, and where the result returns. The stage skill is the engine behind the Board.

## One-page wire contract

Keep the Board's existing visible order. Do not add a new file or require a new top-level Handoff section.

```text
Opening
Stage Contract
Content
Items to Finish
Where we are
Files
Discussion / Comments / Log
```

- `Content` contains only the current stage or unit substance.
- `Items to Finish` is the page's executable To Do queue.
- `Where we are` summarizes the actual state instead of duplicating every item.
- `Comments` anchors human discussion to the exact Content or queue item.
- `Log` keeps only concise completed history when history is useful.
- Each completed queue item carries its own `handoff:` field. A separate Handoff file would split the state again.

## Queue item contract

Use a local item id because the owning page already provides global context.

```markdown
- [ ] I4 · Rebuild the primary regression columns
  - phase: revise
  - kind: display-render
  - from: S-Main-7 · P2.S3
  - request: Use the binary exposure as the primary specification and retain the continuous score as robustness.
  - acceptance: The prose, caption, table columns, estimand, and statistical label agree.
  - status: ready
  - owner: --
  - blocked-by: --
  - handoff: --
```

The minimal item states are `ready`, `claimed`, `blocked`, and `done`.

When a worker claims an item, it writes `status: claimed` and `owner:` before doing work. When it finishes, it checks the item, writes `status: done`, and fills `handoff:` with the live artifact, preview, verification, and downstream consumer. An unverified result stays unchecked.

## Existing Display revision

```text
Section sentence or comment
        │
        │ identifies stable display04
        ▼
S-Display-4 · Items to Finish
        │
        │ I4 records from/request/acceptance
        ▼
Display worker updates the same display04 unit
        │
        ├─ updates Content and live preview
        ├─ fills I4 handoff
        └─ leaves Section's display_id unchanged
```

Section-edit may allocate work to a Display page, but it does not perform that Display work. Display owns the visual argument, caption, row or panel selection, venue formatting, and live asset.

If the request requires new numbers or a new data artifact, the Display worker routes the evidence-side work through the task/probe lifecycle. The paper-side To Do remains on `S-Display-N`; the bank's QA/task artifact is evidence, not a second paper queue.

## New Display

If no Display page exists, write one item on the Display stage page:

```markdown
- [ ] I7 · Create a cohort inclusion funnel
  - phase: draft
  - kind: display-new
  - from: S-Main-6 · P3.S2
  - request: Show per-step inclusion and exclusion counts ending at each analytic cohort.
  - acceptance: The unit has a stable display id, source binding, preview, caption job, and manuscript placement.
  - status: ready
  - owner: --
  - handoff: --
```

After the Display stage accepts it, create the real `S-Display-N` page and unit, move the item verbatim into that page, and remove it from the unallocated queue. The new S page is the Display itself, not a request sidecar.

## What `haipipe-paper-stage` should become

The current skill is stage-first and phase-first: the user supplies a stage and often a phase through a CLI-shaped invocation. The proposed skill is page-first and queue-first.

Its main internal entry should be equivalent to:

```text
work --page <S-face-path> [--item <local-id>]
```

The Board supplies this invocation. A direct CLI form may remain as a debugging or recovery path, but it is not the primary user interaction.

The stage runner should perform one small deterministic loop:

1. Resolve the S page and read its explicit `stage:` key.
2. Read `stages/index.yml`, then load only that stage's `stage.md`.
3. Read the wire page completely, including `requires`, `style-from`, Content, queue, comments, and state.
4. Pick the requested item or the first ready item allowed by the current phase and dependencies.
5. Claim it on the wire page before dispatch.
6. Route it to the worker declared by the stage contract.
7. Verify the returned result in proportion to risk.
8. Update Content, the item handoff, Where we are, state, and the Board in the same turn.
9. Continue with another ready item only when the user asked to work the queue.
10. Stop at a human decision, spend authorization, unresolved dependency, or CHECK gate.

## DPRC remains, but the user should not operate it manually

DRAFT, PROBE, REVISE, and CHECK still protect important boundaries. In particular, evidence must continue to enter through PROBE. The change is that phases become queue semantics rather than the main remote-control interface.

```text
Board: Work this queue
          │
          ▼
Stage runner reads current phase and item tags
          │
          ├─ draft items  → draft worker
          ├─ probe items  → probe worker
          ├─ revise items → revise worker
          └─ check items  → checker, then visible human gate on Board
```

The user should not need to remember a command such as `display revise`. The page knows its phase, and each queue item states the phase in which it may run.

## Worker routing belongs in each stage contract

The root `haipipe-paper-stage` skill should know the queue loop, not every discipline. Each `stage.md` should declare the routes it permits.

```text
kind: content-draft       → haipipe-paper-draft
kind: evidence            → haipipe-paper-probe
kind: content-revise      → haipipe-paper-revise
kind: display-render      → the renderer selected by Display
kind: data-artifact       → haipipe task lifecycle agent
kind: check               → haipipe-paper-check
kind: human-decision      → stop and surface on the Board
```

Display may commission renderers. Section-edit may allocate a request to an existing Display page. Neither may bypass the evidence boundary or write into the other's owned Content.

## Fresh sessions are a feature

A new remote session should need only:

```text
paper root
S page path
queue item id, or "work this queue"
```

It should not need the transcript of the previous CLI session. It reconstructs context from the page, its managed Stage Contract, its upstream `requires`, and its `style-from` source.

One worker owns one wire page at a time. Different pages may run in parallel. Data or artifact work uses the task lifecycle agents; a generic sub-agent is appropriate for bounded paper reasoning, page editing, or review that does not create a data artifact.

## Contracts and state to rationalize

- Make the S page's `requires:` authoritative for dependencies. Remove or reduce stale hand-maintained `inputs:` lists after the reading order has a clear home.
- Make each page's `state:` authoritative. Derive the lifecycle frontier from the Board pipeline and page states; do not maintain a second current-stage pointer that can disagree.
- Give each S page an explicit `stage:` key so the stage runner never infers execution logic from a filename, Pages position, or Board family.
- Make Display and Section per-unit because their units gate independently. Keep Seed, Resource, Claims, Venue, Pitch, and Narrative single-page unless their units gain independent gates.
- Use one page creator. The stage runner should call the Board scaffolder for the shell and managed Stage Contract, then compose Content from the selected stage template, venue template, and accepted upstream contracts.
- Remove migration status, retired paths, and known-history narration from the live stage skill. Current operational rules belong in `SKILL.md`; history belongs outside the execution context.

## Board interaction

The Board should eventually expose two actions on each S page:

- `Work this item` starts a fresh worker with the page path and item id.
- `Work this queue` lets the stage runner drain ready items until it reaches a gate, human decision, spend boundary, or blocker.

The worker may run through a CLI process internally, but the user should not have to monitor or resume that CLI. The Board shows `claimed`, owner, progress, blocker, result, and handoff, then refreshes the page.

## Sentence and Display resolution

A Section refers to a stable semantic id:

```text
[Display:display04]
```

The Board resolves it to the Display page and hover preview. The paper renderer resolves the same id to LaTeX/PDF or Word. Changing the winning candidate or regenerating the table does not change the Section reference.

The same pattern can later serve citations and values:

```text
sentence anchor → semantic id → Board preview/provenance → output-specific rendering
```

This later rendering work should not be mixed into the first queue refactor.

## Recommended implementation sequence

### Step 1 — settle the contract in this board

- Decide that Board is the control plane and sessions are workers.
- Decide that `Items to Finish` is the queue and `handoff:` lives inside each item.
- Decide the page-first `work` loop and one-writer-per-page rule.
- Decide that no `_DISPLAY_REQUEST.md` or Handoff sidecar is created.

### Step 2 — documentation-only cut

- Simplify `haipipe-paper-stage/SKILL.md` around the page-first queue loop.
- Add the queue item contract to the Board/paper stage contract.
- Update Display and Section contracts so they allocate work directly to owning S pages.
- Stop future generation of `_DISPLAY_REQUEST.md`.
- Do not change renderers or migrate every existing paper in this step.

### Step 3 — minimum working execution

- Add or adapt a stage-runner entry that accepts an S page path and optional item id.
- Implement claim, worker dispatch, result integration, and Board rebuild.
- Keep direct CLI invocation only as an internal fallback.

### Step 4 — Board controls

- Connect `Work this item` and `Work this queue` to fresh sessions.
- Display owner, status, blocker, and handoff on the page.
- Keep the page readable and fully informative without JavaScript.

### Step 5 — independent validation

- Give a fresh agent only a paper root and an S page path.
- Ask it to work one existing Display revision item.
- Inspect whether it reads the Board first, claims the item, selects the correct skill, respects the evidence boundary, updates the same page, and stops at the gate.
- Repeat with a new Display item and a Section prose item.

## Acceptance scenarios

- A fresh session can open `S-Display-4`, work its next ready item, and finish without reading an old transcript.
- A Section can allocate a revision to `S-Display-4` without creating a request file or editing the table.
- A new Display can begin on the Display stage page and become one canonical `S-Display-N` page.
- Two agents can work different Display pages concurrently without editing the same wire page.
- A data-bearing request routes through the task/probe boundary rather than a generic worker inventing or recomputing values.
- A human sees every decision, blocker, comment, live preview, and completed handoff on the Board.
- CHECK cannot become ✅ through an unattended worker.

## Recommendation

Keep `haipipe-paper-stage`, but redefine it narrowly as the Board-aware queue runner for one S page. Do not make it another broad paper orchestrator. `haipipe-paper` chooses the paper and lifecycle context, `haipipe-board` owns the durable interaction surface, `haipipe-paper-stage` executes the selected page, and specialized skills do the bounded work.
