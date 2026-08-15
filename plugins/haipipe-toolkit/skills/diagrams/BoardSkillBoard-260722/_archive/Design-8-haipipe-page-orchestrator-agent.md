# haipipe-page-orchestrator-agent · v0.1.0
state: 🟡 in flux · shipped 0.1.0 260804, exercised once 260805 in emulation, never dispatched
owner: JL
page-type: design
method: unit snapshot in skill/ via skillpage.py plug; every section authored by hand (converted from the mirror kind 260815)

## Opening
`haipipe-page-orchestrator-agent` runs one Page through a bounded DRAFT, PROBE, REVISE, and CHECK loop and preserves its receipt outside the rendered Board.
Reach for it when the Page's next authority should be discovered automatically; use `haipipe-board-reviewer-agent` alone for one read-only CHECK.
Trust the process after `pageflow.py audit` passes, and trust CLOSE only for the exact source and render version named by the reviewer.

**Its narrow scope**: it does not create or register a Page, write Page prose, rebuild by itself, judge a version, or supply a human ruling.
The Workflow dispatches those authorities to the producer, builder, reviewer, and human gate rather than letting the controller absorb them.

**What it leaves visible**: the receipt records every attempted Phase, actor, version, route, finding, evidence item, gate state, and limit stop under `_runs/page/`.
That record is the difference between a resumable process and a hidden agent conversation.

## Writing Style
English only. One sentence per source line. Describe the shipped unit factually and keep generated inventory separate from human health judgment.

## Diagram
**What sits in this page's `skill/` plugin**: the unit's contract surface, written by `skillpage.py plug` and renamed so neither the installer glob nor page discovery can mistake it for the live unit.

```
skill/haipipe-page-orchestrator-agent/
  CHANGELOG.md
  haipipe-page-orchestrator-agent.md
```

**How `haipipe-page-orchestrator-agent` is used**: the controller owns routing and the receipt while four other authorities retain their own boundaries.

```text
WORKFLOW  one packet in, four dispatched authorities, one durable receipt

📦 Page RUN packet
        │
        ▼
🧭 orchestrator
├──▶ ✍️ producer       DRAFT · PROBE · REVISE
├──▶ 🏗 builder        build · check.py · version hash
├──▶ 🧑 reviewer       CHECK · route · no edits
└──▶ 🧾 _runs receipt  pageflow.py audit
        │
        └── CLOSE | HOLD | ↺ next authority
```

## Content
### 1 · What this unit is, in one screen
**Live and snapshot**: the unit ships from its own folder, and this page judges a plugged copy.
```text
  ⚙️ the live unit, ships        📋 skill/haipipe-page-orchestrator-agent/
     from its own folder    ──▶     the snapshot this page's
                            plug    judgments are about
```
`haipipe-page-orchestrator-agent` is the non-interactive RUN target: it drives the bounded Workflow, stores `_runs/page/` receipts, and calls the deterministic auditor without editing page prose.
The live unit is one .md dispatched from `board/agents/`.

### 2 · Selection record · adopted from the specimen
**Where the record lives**: one argument, one home, adopted by reference.
```text
  🅰🅱 the candidates + full record ──▶ Design-3-haipipe-page · Content §2
  📄 this page keeps only what is its own: health · aims · snapshot
```
This page converted to a for-design page under the 260815 ruling that retired the mirror kind.
The candidates and the full record are written once, on the specimen: `Design-3-haipipe-page` Content §2.
This page adopts that selection rather than restating it, because seven copies of one argument would recreate the form-letter failure the ruling killed.
What is page-specific stays here: the Opening, the Aims, the States judgment on the unit's health, and the plugged snapshot above.

## Aims
- [ ] 🧭 The charter is dispatched rather than emulated
      The one live RUN on 260805 could not reach the Workflow tool, so the session played this controller itself, dispatched the producer and the judge as fresh-context `claude -p` subprocesses, and performed the builder role under the identity `orchestrator-mechanical-builder`.
      Nothing has yet run this agent AS an agent, so its procedure, its stop rules and its return contract have been reasoned about rather than exercised.
- [ ] 🧾 The auditor's result reaches the receipt it audits
      Procedure step 4 runs `pageflow.py audit` and the return contract carries an `audit: pass | fail` field, and the one stored receipt has no such field, so whether the auditor ever passed that run is not on the record.
      Re-running the auditor today returns `artifact-version-mismatch`, which is the stop rule working rather than a defect: `QB8e` moved on after CLOSE, so the closed version is no longer the current one.
- [ ] 📐 The deviations the first run invented are ruled or written in
      The receipt names three: the controller appended the preceding CHECK findings to each REVISE dispatch because the shipped workflow prompt omits them, it added a closing-rule interpretation so that CLOSE asserts one exact version rather than every Aim of a decision page, and it minted the `run_id` the packet arrived without.
      Each is a gap the charter does not cover, and none of the three has been folded back into the charter or into `page-lifecycle.workflow.js`.
- [x] 🧾 One run leaves a record a stranger can read
      The 260805 run wrote `_runs/page/QB8e/260805-0216-QB8e.json` carrying five step receipts with their actors, routes and verdicts, the packet it started from, the limits it ran under, and the controller's own deviations.
      It sits outside the rendered board, so a rebuild cannot erase it and no reader stumbles on it by accident.

## States
The first live Page RUN executed this controller logic on 260805 against QB8e: the Workflow tool was unavailable, so the session emulated `page-lifecycle.workflow.js` verbatim, dispatched the producer and judge as fresh-context `claude -p` subprocesses, and played the mechanical builder itself under the actor name `orchestrator-mechanical-builder`.
The run closed in five steps and one round, CHECK to REVISE to CHECK to REVISE to CHECK, on a final reviewer verdict of pass and route CLOSE; the receipt is `_runs/page/QB8e/260805-0216-QB8e.json`.

- 260805 CC · 🧭 The first live RUN closed, and the controller was not this agent
  The Workflow tool was unavailable, so the session emulated `page-lifecycle.workflow.js` and wrote that substitution into the receipt's `controller` block instead of leaving it implicit.
  It recorded three deviations it had to invent at run time as well, which is the part worth keeping: an emulated controller that writes down where it departed can still be audited, and one that does not is only a conversation.

## Log
- 260815 1230 · [REVISE-CC] converted to a for-design page (JL 260815): the three managed spans left the file, `skillpage.py plug` wrote the unit's contract surface to `skill/haipipe-page-orchestrator-agent/`, and Content §2 adopts the selection recorded on the specimen.
- 260806 2222 · [REVISE-CC] type-conformance pass against haipipe-page-for-skill; Aims and States converted from the generator's base-form stub to the checkbox and dated-record form this variant overrides to, the "Page generated 260804 2030; nothing ruled yet" row the variant forbids on a shipping unit is gone, the three open Aims now carry the UNIT's own work read off the 260805 receipt, `state:` gained the evidence note the variant requires and moved off the seeded 🔴 OPEN, and the Diagram figure is labelled as the WORKFLOW fence
- 260806 2115 · [REVISE-CC] swept to the 260806 architecture; no false facts found: skillpage sync reports spans current, and the States account verified verbatim against the frozen receipt `_runs/page/QB8e/260805-0216-QB8e.json` (5 steps, 1 round, CHECK→REVISE→CHECK→REVISE→CHECK, final pass → CLOSE, emulated Workflow controller).
- 260806 0140 · [REVISE-CC] card synced to disk truth after 260805 (ten types · thin-paper phase 2 · first live RUN); the first live RUN is on the record, 260805 on QB8e, closed in five steps on a final CHECK pass, with the session emulating the Workflow controller because the Workflow tool was unavailable.
260804 2035 · Replaced the generated Opening and Diagram stubs with the Page-specific role boundary, reviewer comparison, trust condition, dispatched authorities, and durable receipt flow. Page health remains for JL to rule after fresh validation.
260804 2030 · page generated from `board/agents/haipipe-page-orchestrator-agent.md/` by `skillpage.py new`

