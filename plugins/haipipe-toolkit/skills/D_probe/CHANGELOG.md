D_probe — Changelog
===================

Layer-scoped changelog for the D_probe (PROBE / claim) layer. Newest first.
Rollup lives in the plugin-level `CHANGELOG.md`.


## [Unreleased] — 2026-05-31

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
