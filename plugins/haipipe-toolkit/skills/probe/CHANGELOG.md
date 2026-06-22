probe - Changelog
===================

Layer-scoped changelog for the probe (PROBE / claim) layer. Newest first.
Rollup lives in the plugin-level `CHANGELOG.md`.


## [4.0.0] - 2026-06-22

### Changed
- Reframed around the **Probe Console** + concise lifecycle
  **Plan → Gather → Read → Judge → Return**; flat probe folders; group folders removed.
- `probe-aware no-arg dashboard` (`ref/probe-dashboard.md`) and the scattered-work
  **filing judge** (`ref/probe-attach.md`, `/haipipe-probe file`) added.

### Removed (v3 supporting layer that no longer fit)
- `ref/`: probe-lifecycle.workflow.js, probe-status-template.txt,
  probe-run-dashboard-template.txt, probe-cycle-audit-template.txt,
  probe-headline-template.txt, probe-entry-template.txt, workflow-plan-sample.yaml,
  _legacy-scope-expmt.md, log-format.md (all orphaned; superseded by lifecycle-map + dashboard).
- `fn/`: design.md, bridge.md, harvest.md (were full v3 bodies mislabeled "aliases";
  routing now maps legacy verbs to the v4 procedures).
- specialists `haipipe-probe-inspect/` and `haipipe-probe-explore/` (dropped from v4 commands;
  status→Console/dashboard, unused→dashboard UNLINKED EVIDENCE).
- agents: probe-idea-creator, probe-idea-reviewer (no auto Plan mode), probe-explorer
  (no explore command). Kept the 3 Judge reviewers and wired them into fn/judge.md.
- diagrams 01-probe-lifecycle, 02-three-layer-pyramid.

### Fixed
- Plugin top-level `agents/` symlinks for the 3 probe reviewers were dead
  (`../skills/D_probe/...` after the D_probe→probe rename); repointed to `../skills/probe/...`.


## [2.0.0] - 2026-06-11

### Added
- **IPO workflow adoption.** probe now follows the haipipe-workflow (project)
  IPO pattern - the same universal unit that task adopted for task folders.
  - `ref/workflow-plan-sample.yaml` - the probe lifecycle as an IPO plan template.
    6 domain phases (Design → Bridge → Run → Aggregate → Review → Claim), each
    with steps declaring `files_in` / `files_out`. Follows `plan-schema.md`.
  - `haipipe-probe/ref/probe-lifecycle.workflow.js` - the 4-stage lifecycle
    (Plan → Build → Execute → Report) wrapping the 6 domain phases. Plan creates
    the probe plan; Build executes Design + Bridge; Execute runs Run + Aggregate +
    Review + Claim; Report mirrors the plan with results.
  - Lifecycle section added to `haipipe-probe/SKILL.md` showing the mapping:
    Plan → Build (Design + Bridge) → Execute (Run + Aggregate + Review + Claim)
    → Report.

### Notes
- The 4-stage lifecycle is the same universal wrapper from project/haipipe-workflow.
  The 6 domain phases are probe-specific - not copied from task. task's eval
  task has Load/Score/Compare/Emit; probe has Design/Bridge/Run/Aggregate/Review/Claim.
- Builder asymmetry preserved: Design, Bridge, Result remain interactive skills in the
  workflow.js (not creator-reviewer agent loops). Reviewer agents run in the Review
  domain phase (P5), gated sequentially (structural → integrity → semantic).
- No per-probe `workflow/` folder - probe.yaml is already the plan (hypothesis + arms +
  aggregation), and CYCLE.md (from inspect cycle) is the report. The workflow-plan-sample
  serves as the reference template; probe-lifecycle.workflow.js is shared across probes.


## [Unreleased] - 2026-05-31

### Added
- **Agent families (lighter than task, by design).** New `agents/`:
  - `reviewers/` (3): `probe-structural-reviewer-agent`,
    `probe-integrity-auditor-agent` (Codex), `claim-verifier-agent` (Codex) -
    the three honesty checks as independent, dispatchable subagents
    (builder ≠ judge). Thin pointers to `haipipe-probe-review/SKILL.md` +
    `ref/` (no duplicated checklists/prompts).
  - `advancers/` (1): `probe-explorer-agent` - probe's unique third family
    (proposes research direction; task has no analog).
  - Registered as flat symlinks under the plugin top-level `agents/` for
    `subagent_type` dispatch (by `haipipe-probe-loop`, `application`).
- **Intentional asymmetry vs task: NO `creators/`.** probe's builders
  (`design`, `result`, `bridge`) STAY interactive skills - designing a probe
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
  instead of re-implementing the checklist - single source of truth. "Did THIS
  run produce a trustworthy artifact?" is a task question; probe only
  consumes the verdict. The per-probe checklist's line now reads "all linked
  runs pass haipipe-task-reviewer-agent GATE 2 (task)".
- **Bridge dispatch updated.** `haipipe-probe-bridge` Step 3 invokes the task
  reviewer by reading `skills/task/agents/haipipe-task-reviewer-agent.md` and
  handing its body to a Task subagent (the agent is a role-doc invoked by path,
  registered at the plugin top-level `agents/` for `subagent_type` addressing).

### Notes
- Integrity audit (5 fraud patterns) and claim verdict remain Codex-backed
  judgments inside `haipipe-probe-review` - unchanged this round.
