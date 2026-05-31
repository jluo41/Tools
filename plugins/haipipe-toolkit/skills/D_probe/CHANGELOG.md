D_probe — Changelog
===================

Layer-scoped changelog for the D_probe (PROBE / claim) layer. Newest first.
Rollup lives in the plugin-level `CHANGELOG.md`.


## [Unreleased] — 2026-05-31

### Added
- **Agent families (lighter than C_task, by design).** New `agents/`:
  - `reviewers/` (3): `probe-structural-reviewer-agent`,
    `probe-integrity-auditor-agent` (Codex), `claim-verifier-agent` (Codex) —
    the three honesty checks as independent, dispatchable subagents
    (builder ≠ judge). Thin pointers to `haipipe-probe-review/SKILL.md` +
    `ref/` (no duplicated checklists/prompts).
  - `advancers/` (1): `probe-explorer-agent` — D_probe's unique third family
    (proposes research direction; C_task has no analog).
  - Registered as flat symlinks under the plugin top-level `agents/` for
    `subagent_type` dispatch (by `haipipe-probe-loop`, `G_application`).
- **Intentional asymmetry vs C_task: NO `creators/`.** D_probe's builders
  (`design`, `result`, `bridge`) STAY interactive skills — designing a probe
  needs human steering and there is no task-type axis to fan out; probe
  parallelism lives downstream in C_task (via the bridge). Documented in
  `agents/README.md`.
- Wiring notes added to `haipipe-probe-review` (three checks ↔ three reviewer
  agents) and `haipipe-probe-explore` (↔ probe-explorer-agent).

### Changed
- **Per-run quality is no longer owned here.** The per-run sanity checklist
  (runtime.status / exit_code / git_sha / metrics.json parseable / heavy-artifact
  placement) moved to the C_task agent `run-result-auditor-agent` (GATE 2).
  `haipipe-probe-review` `review run` now DELEGATES to that agent instead of
  re-implementing the checklist — single source of truth. "Did THIS run produce
  a trustworthy artifact?" is a C_task question; D_probe only consumes the verdict.
  The per-probe checklist's line now reads "all linked runs pass
  run-result-auditor-agent (GATE 2, C_task)".
- **Bridge dispatch updated.** `haipipe-probe-bridge` Step 3 invokes the Run
  Script Reviewer by reading
  `skills/C_task/agents/reviewers/run-script-reviewer-agent.md` and handing its
  body to a Task subagent (the agent is a role-doc invoked by path, registered
  at the plugin top-level `agents/` for `subagent_type` addressing).

### Notes
- Integrity audit (5 fraud patterns) and claim verdict remain Codex-backed
  judgments inside `haipipe-probe-review` — unchanged this round.
