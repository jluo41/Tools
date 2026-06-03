C_task — Changelog
==================

Layer-scoped changelog for the C_task (WORK / execution) layer. Newest first.
Rollup lives in the plugin-level `CHANGELOG.md`.


## [Unreleased] — 2026-05-31

### Added
- **Agent families, split by folder.** `agents/` now has two families:
  - `creators/` — per task TYPE, the growth axis. Seven thin builders:
    `code-creator-for-{training,data,eval,display,individual,algo,agent}-agent`.
    Each calls its `haipipe-task-for-<type>` skill (headless) to scaffold,
    then authors the `<TASK>.py` body. `_TEMPLATE.md` to add the next type.
  - `reviewers/` — type-AGNOSTIC, fixed at 2: `run-script-reviewer-agent`
    (GATE 1, pre-run intent↔impl) and `run-result-auditor-agent` (GATE 2,
    post-run trustworthiness). They gate every type; adding a type costs 0.
- **Shared knowledge packs** (single source of truth, read by both skills and
  creators): `haipipe-task/ref/authoring-conventions.md` (4 sister files,
  `_meta` contract, heavy-artifact placement, reproducibility, first-run gate,
  builder≠judge, papermill/notebook §7) and `haipipe-task/ref/invocation-modes.md`
  (the dual-mode contract + structured-return schema).
- **Batch orchestrator** `haipipe-task-batch` — fan out N typed specs in one
  session, each flowing author → GATE 1 → run → GATE 2 independently. Two
  engines: native parallel Agent calls, or the deterministic Workflow at
  `haipipe-task-batch/ref/batch-pipeline.workflow.js` (`autoRun` defaults
  false — pauses after GATE 1 for human approval, never burns GPU unattended).
- **Notebook retention knob** `_meta.notebook: full | thin | off` (default
  full), read by `run-sh-template.sh`. `thin` clears outputs (small record for
  heavy training/data runs); `off` executes via papermill but keeps no
  `.ipynb`. Heavy-type creators (training, data) default to `thin`.
- **Top-level `agents/` registry** (plugin root, flat symlinks) so every agent
  is addressable as a `subagent_type` for fan-out
  (`agent_type:"code-creator-for-training-agent"`).

### Changed
- **Renamed the 7 type skills** `haipipe-task-<type>` → `haipipe-task-for-<type>`
  (training/data/eval/display/individual/algo/agent). `haipipe-task` (router)
  and `haipipe-task-logging` (aux) unchanged. All 155 references updated.
- **Dual-mode skills.** `haipipe-task-for-*` + the shared `fn/run.md` now run
  interactive (ASK missing fields) OR headless (full spec → silent, no ASK),
  chosen by input completeness; every invocation emits a structured return
  (status / task_folder / run_name / files). Missing `purpose` + no user →
  `status: blocked`, never invented.
- **Per-run sanity checklist relocated here from D_probe.** `run-result-auditor-agent`
  now owns the per-run checklist (runtime.status / exit_code / git_sha /
  metrics.json / artifact placement); `D_probe review run` delegates to it.

### Removed
- The single general `task-code-creator-agent` (superseded by the 7 per-type
  creators).
