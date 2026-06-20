probe — Changelog
===================

Layer-scoped changelog for the probe (PROBE / claim) layer. Newest first.
Rollup lives in the plugin-level `CHANGELOG.md`.


## [2.0.0] — 2026-06-11

### Added
- **IPO workflow adoption.** probe now follows the haipipe-workflow (project)
  IPO pattern — the same universal unit that task adopted for task folders.
  - `ref/workflow-plan-sample.yaml` — the probe lifecycle as an IPO plan template.
    6 domain phases (Design → Bridge → Run → Aggregate → Review → Claim), each
    with steps declaring `files_in` / `files_out`. Follows `plan-schema.md`.
  - `haipipe-probe/ref/probe-lifecycle.workflow.js` — the 4-stage lifecycle
    (Plan → Build → Execute → Report) wrapping the 6 domain phases. Plan creates
    the probe plan; Build executes Design + Bridge; Execute runs Run + Aggregate +
    Review + Claim; Report mirrors the plan with results.
  - Lifecycle section added to `haipipe-probe/SKILL.md` showing the mapping:
    Plan → Build (Design + Bridge) → Execute (Run + Aggregate + Review + Claim)
    → Report.

### Notes
- The 4-stage lifecycle is the same universal wrapper from project/haipipe-workflow.
  The 6 domain phases are probe-specific — not copied from task. task's eval
  task has Load/Score/Compare/Emit; probe has Design/Bridge/Run/Aggregate/Review/Claim.
- Builder asymmetry preserved: Design, Bridge, Result remain interactive skills in the
  workflow.js (not creator-reviewer agent loops). Reviewer agents run in the Review
  domain phase (P5), gated sequentially (structural → integrity → semantic).
- No per-probe `workflow/` folder — probe.yaml is already the plan (hypothesis + arms +
  aggregation), and CYCLE.md (from inspect cycle) is the report. The workflow-plan-sample
  serves as the reference template; probe-lifecycle.workflow.js is shared across probes.


## [Unreleased] — 2026-05-31

### Added
- **Agent families (lighter than task, by design).** New `agents/`:
  - `reviewers/` (3): `probe-structural-reviewer-agent`,
    `probe-integrity-auditor-agent` (Codex), `claim-verifier-agent` (Codex) —
    the three honesty checks as independent, dispatchable subagents
    (builder ≠ judge). Thin pointers to `haipipe-probe-review/SKILL.md` +
    `ref/` (no duplicated checklists/prompts).
  - `advancers/` (1): `probe-explorer-agent` — probe's unique third family
    (proposes research direction; task has no analog).
  - Registered as flat symlinks under the plugin top-level `agents/` for
    `subagent_type` dispatch (by `haipipe-probe-loop`, `application`).
- **Intentional asymmetry vs task: NO `creators/`.** probe's builders
  (`design`, `result`, `bridge`) STAY interactive skills — designing a probe
  needs human steering and there is no task-type axis to fan out; probe
  parallelism lives downstream in task (via the bridge). Documented in
  `agents/README.md`.
- Wiring notes added to `haipipe-probe-review` (three checks ↔ three reviewer
  agents) and `haipipe-probe-explore` (↔ probe-explorer-agent).

### Changed
- **Per-run quality is no longer owned here.** The per-run sanity checklist
  (runtime.status / exit_code / git_sha / metrics.json parseable / heavy-artifact
  placement) moved to the task unified reviewer `haipipe-task-reviewer-agent`
  (GATE 2). `haipipe-probe-review` `review run` now DELEGATES to that agent
  instead of re-implementing the checklist — single source of truth. "Did THIS
  run produce a trustworthy artifact?" is a task question; probe only
  consumes the verdict. The per-probe checklist's line now reads "all linked
  runs pass haipipe-task-reviewer-agent GATE 2 (task)".
- **Bridge dispatch updated.** `haipipe-probe-bridge` Step 3 invokes the task
  reviewer by reading `skills/task/agents/haipipe-task-reviewer-agent.md` and
  handing its body to a Task subagent (the agent is a role-doc invoked by path,
  registered at the plugin top-level `agents/` for `subagent_type` addressing).

### Notes
- Integrity audit (5 fraud patterns) and claim verdict remain Codex-backed
  judgments inside `haipipe-probe-review` — unchanged this round.
