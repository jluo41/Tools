# haipipe-board-page-orchestrator-agent · v0.1.0
state: 🔴 OPEN
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
`haipipe-board-page-orchestrator-agent` runs one Page through a bounded DRAFT, PROBE, REVISE, and CHECK loop and preserves its receipt outside the rendered Board.
Reach for it when the Page's next authority should be discovered automatically; use `haipipe-board-reviewer-agent` alone for one read-only CHECK.
Trust the process after `pageflow.py audit` passes, and trust CLOSE only for the exact source and render version named by the reviewer.

**Its narrow scope**: it does not create or register a Page, write Page prose, rebuild by itself, judge a version, or supply a human ruling.
The Workflow dispatches those authorities to the producer, builder, reviewer, and human gate rather than letting the controller absorb them.

**What it leaves visible**: the receipt records every attempted Phase, actor, version, route, finding, evidence item, gate state, and limit stop under `_runs/page/`.
That record is the difference between a resumable process and a hidden agent conversation.

## Writing Style
English only. One sentence per source line. Describe the shipped unit factually and keep generated inventory separate from human health judgment.

## Diagram
<!-- haipipe:skill:tree:start f5f85d290b794539 board/agents/haipipe-board-page-orchestrator-agent.md -->

<!-- haipipe:skill:tree:end -->

**How `haipipe-board-page-orchestrator-agent` is used**: the controller owns routing and the receipt while four other authorities retain their own boundaries.

```
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
<!-- haipipe:skill:body:start f5f85d290b794539 board/agents/haipipe-board-page-orchestrator-agent.md -->

**haipipe-board-page-orchestrator-agent** · `0.1.0` · last shipped 2026-08-04

- folder   `board/agents/haipipe-board-page-orchestrator-agent.md/`
- tools    not declared
- summary  Routes one Page through bounded producer/build/judge loops and preserves an auditable receipt.

### haipipe-board-page-orchestrator-agent.md




Run one persistent Page through a bounded, auditable lifecycle. Coordinate;
never author or judge.


- 1 · Boundary
      ```text
      input       one page-run raw-material packet
      dispatch    haipipe-board/ref/page-lifecycle.workflow.js
      write       one _runs/page/<page-id>/<run-id>.json receipt
      check       haipipe-board/cli/pageflow.py audit
      never       Page prose · board.md · generated HTML · human approval
      ```
      The Workflow dispatches `haipipe-board-creator-agent` for DRAFT, PROBE, and
      REVISE, a mechanical snapshot worker, and `haipipe-board-reviewer-agent` for
      CHECK. This agent does not replace any of those roles and may never translate a
      HOLD into CLOSE.

- 2 · Input
      Load `../haipipe-board-page/SKILL.md` and
      `../haipipe-board-page/ref/page-run-contract.md`. Require:
      ```text
      run_id · board · page · start_phase · intent
      ```
      Preserve optional `sources`, `constraints`, `human_gate`, and `limits` exactly.
      Resolve paths before dispatch. If the Page does not exist, return blocked and
      tell the caller to CREATE it first. Do not scaffold or register it yourself.

- 3 · Procedure
      1. Confirm that `board.md` and the target Page exist and that the target is
         inside the Board.
      2. Invoke:
         ```text
         Workflow({
           scriptPath: "Tools/plugins/haipipe-toolkit/skills/board/haipipe-board/ref/page-lifecycle.workflow.js"
         }, <the exact packet>)
         ```
      3. Create only the receipt directory
         `<board>/_runs/page/<page-id>/`. Write the exact Workflow result as
         `<run-id>.json`; do not summarize or alter its receipts before storage.
      4. Run:
         ```bash
         python3 Tools/plugins/haipipe-toolkit/skills/board/haipipe-board/cli/pageflow.py audit <receipt-path>
         ```
      5. If the auditor fails, return failed with its exact findings. Do not resume
         the loop from an unauditable state.
      6. If the auditor passes, return the terminal route and evidence. CLOSE means
         the exact final version passed; HOLD means the record is safe but unfinished.

- 4 · Stop rules
      - Missing required input, inaccessible source, failed build, or version mismatch
        stops at HOLD or failed.
      - Reaching `max_steps` or `max_rounds` stops at HOLD.
      - A required human gate without durable passed evidence stops at HOLD.
      - A changed Page after CHECK invalidates that CHECK; it never inherits CLOSE.
      - Never start a second RUN against the same Page while an earlier run is active.
        Report the existing receipt path and let the human decide whether it is stale.

- 5 · Return
      ```text
      status: closed | hold | blocked | failed
      run_id: <id>
      page: <path>
      receipt: <_runs/page/...json path>
      audit: pass | fail
      terminal_route: CLOSE | HOLD
      final_version: <source:render sha256 identity>
      rounds: <count>
      steps: <count>
      edges: <ordered PHASE→route list>
      human_gate: <not-required | pending | passed + evidence>
      findings: <exact remaining findings or none>
      residual_risk: <what the run did not establish>
      ```
<!-- haipipe:skill:body:end -->

## Aims
### P · Page-level health ruling
- P1 · Rule this skill's health.
  **Done when:** `state:` records a human judgment: stable, in flux, needs work, or parked.

## States
The first live Page RUN executed this controller logic on 260805 against QB8e: the Workflow tool was unavailable, so the session emulated `page-lifecycle.workflow.js` verbatim, dispatched the producer and judge as fresh-context `claude -p` subprocesses, and played the mechanical builder itself under the actor name `orchestrator-mechanical-builder`.
The run closed in five steps and one round, CHECK to REVISE to CHECK to REVISE to CHECK, on a final reviewer verdict of pass and route CLOSE; the receipt is `_runs/page/QB8e/260805-0216-QB8e.json`.

### P · Page-level health ruling
- ⬜ P1 · Page generated 260804 2030; nothing ruled yet.

## Log
- 260806 0140 · [REVISE-CC] card synced to disk truth after 260805 (ten types · thin-paper phase 2 · first live RUN); the first live RUN is on the record, 260805 on QB8e, closed in five steps on a final CHECK pass, with the session emulating the Workflow controller because the Workflow tool was unavailable.
260804 2035 · Replaced the generated Opening and Diagram stubs with the Page-specific role boundary, reviewer comparison, trust condition, dispatched authorities, and durable receipt flow. Page health remains for JL to rule after fresh validation.
260804 2030 · page generated from `board/agents/haipipe-board-page-orchestrator-agent.md/` by `skillpage.py new`

<!-- haipipe:skill:log:start f5f85d290b794539 board/agents/haipipe-board-page-orchestrator-agent.md -->

Converted from the skill's own `CHANGELOG.md`: 9 releases.

260801 · `0.4.0` · haipipe-board-reviewer-agent
      - Adds a Board-order batch voice gate after page-local review.
      - Detects repeated sentence stems, repeated rhetorical sequences, cosmetic
        synonym swaps, and Openings that survive a sibling-subject substitution.
      - Allows a locally clear page to fail when the changed batch reads like a form
        letter.
260801 · `0.3.0` · haipipe-board-creator-agent
      - Adds explicit `create-page` and `revise-opening` operations while preserving
        the one-agent, one-page write boundary.
      - Makes the creator load `haipipe-board-page` directly, read a revision target
        completely, edit only Opening, and self-check without approving its own work.
      - Keeps prose requirements in the canonical skill and reference instead of
        copying a sentence formula into each assignment packet.
260801 · `0.3.0` · haipipe-board-reviewer-agent
      - Loads the canonical page evaluation contract and resolves base, variant,
        page-local, Stage Contract, division, and paragraph-job requirements.
      - Returns one evidence-bearing `MEETS | NEEDS WORK | N/A | NOT VERIFIABLE`
        verdict per present section and Content unit.
      - Reports requirement conflicts instead of silently choosing a source.
260801 · `0.2.1` · haipipe-board-creator-agent
      - Writes the canonical plural section label `## States`; each row remains one
        singular State record for one Aim.
260801 · `0.2.1` · haipipe-board-reviewer-agent
      - Reviews `## Aims` against the canonical plural `## States` section.
260801 · `0.2.0` · haipipe-board-creator-agent
      - Replaced the retired Boundary and Items-to-Finish writing contract with
        Opening scope, Content-linked Aims, and one factual State row per Aim.
      - Reserved Decision Now and page-level gates for the human while allowing
        evidence-backed Aim State updates.
260801 · `0.2.0` · haipipe-board-reviewer-agent
      - Reviews the one-to-one Aim-to-State id map and distinguishes individual Aim
        status from the page-level human gate.
260731 · `0.1.0` · haipipe-board-creator-agent
      - Added the family's second agent, and the producer half of the creator and
        reviewer pair the rest of this toolkit already uses.
      - Scoped it to exactly ONE page per invocation, so the caller fans out N of
        them in parallel instead of `haipipe-board` writing pages one by one
        (JL 260731).
      - Made the parallel safety structural rather than advisory: no Bash tool, so it
        cannot run `build.py`; `board.md` is off limits, so the one file every writer
        would collide on stays the caller's; and no sibling page may be read, so two
        agents cannot start duplicating each other's judgment.
      - Gave it the `siblings` field in its assignment packet, which is what lets a
        page write an honest Opening scope without reading the board, and what stops
        two pages claiming the same decision.
      - Left every shared write with the caller: registering in `board.md`, the lane
        block, one rebuild, one check, and dispatching the reviewer.
260726 · `0.1.0` · haipipe-board-reviewer-agent
      - Added the Board family's first agent.
      - Made the role read-only: it runs the mechanical checker, cold-reads prose,
        checks for stale claims, and returns findings without editing the Board.
      - Kept Board discovery, synchronization, repair, and rebuilding with the
        original session and `haipipe-board` skill.

<!-- haipipe:skill:log:end -->
