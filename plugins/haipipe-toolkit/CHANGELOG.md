haipipe-toolkit — Changelog
===========================

Plugin-level rollup. Per-layer detail lives in each layer's own
`skills/<LAYER>/CHANGELOG.md`. Newest first.


## [2.1.0] — 2026-05-31

The C_task "creator + reviewer agents" release: a clean split between thin
per-type builder agents and shared type-agnostic reviewer gates, dual-mode
skills, batch fan-out, and a notebook-bloat policy.

### Highlights
- **C_task agent families** — `creators/` (7 per-type thin builders,
  `code-creator-for-<type>-agent`) + `reviewers/` (2 fixed, type-agnostic
  gates). builder ≠ judge; the creator that writes code never reviews it.
  → see [skills/C_task/CHANGELOG.md](skills/C_task/CHANGELOG.md)
- **Skills renamed** `haipipe-task-<type>` → `haipipe-task-for-<type>` (7
  types; router + logging unchanged), matching the `code-creator-for-<type>`
  naming.
- **Dual-mode skills** — one body, interactive (human steers) OR headless
  (agent passes a full spec → runs silent), chosen by input completeness;
  structured return so an agent caller can locate the scaffolded folder.
- **Knowledge centralized in `ref/`** — `authoring-conventions.md` (shared) +
  `invocation-modes.md` (dual-mode contract). Skills and agents both stay thin;
  knowledge has ONE home.
- **Batch fan-out** — `haipipe-task-batch` skill + Workflow `pipeline`
  (`batch-pipeline.workflow.js`): N typed specs in one session, each flowing
  author → GATE 1 → run → GATE 2 independently; GPU-safe (`autoRun` default off).
- **Notebook policy** — `_meta.notebook: full | thin | off` knob in
  `run-sh-template.sh`; heavy compute (training/data) defaults to `thin`;
  `notebooks/` + `_WorkSpace/` default-gitignored.
  → see [skills/B_project/CHANGELOG.md](skills/B_project/CHANGELOG.md)
- **Per-run quality moved C ← D** — the per-run sanity checklist now lives with
  `run-result-auditor-agent` (C_task GATE 2); `D_probe review run` delegates.
  → see [skills/D_probe/CHANGELOG.md](skills/D_probe/CHANGELOG.md)
- **D_probe agent families (lighter pattern)** — `reviewers/` (structural +
  integrity-Codex + claim-Codex) and `advancers/` (explorer). Deliberately NO
  `creators/`: D_probe's builders stay interactive skills (probe design needs
  steering; no type axis; parallelism is downstream in C_task). The same
  builder≠judge method, applied to a low-volume deliberate layer.
  → see [skills/D_probe/CHANGELOG.md](skills/D_probe/CHANGELOG.md)

### Layer changelogs touched this release
- [C_task](skills/C_task/CHANGELOG.md) — agents, skill renames, dual-mode, batch, notebook knob
- [D_probe](skills/D_probe/CHANGELOG.md) — per-run checklist delegated to C_task; bridge dispatch
- [B_project](skills/B_project/CHANGELOG.md) — notebook retention + gitignore guidance


## [2.0.0] — prior

Baseline at the start of this changelog: Tier-1 umbrellas
(/haipipe-data, /haipipe-nn, /haipipe-end, /haipipe-project, /haipipe-individual)
dispatching to per-stage / per-target Tier-2 specialists across stages 0–6.
