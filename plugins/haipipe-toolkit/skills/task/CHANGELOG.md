task — Changelog
==================

Layer-scoped changelog for the task (WORK / execution) layer. Newest first.
Rollup lives in the plugin-level `CHANGELOG.md`.


## [4.0.0] — 2026-06-11

### Changed
- **5-stage lifecycle: Plan / Build / Execute / Report / Insight.** Stage 5 (Insight) is optional — it files a D_data observation card via `/haipipe-insight-data` for insight-worthy task types (eval, fit, stata-reg, stata-data) when results exist. Captures what the DATA taught us, not what the CODE did. First cross-layer call from task into insight.
- **"Two Lifecycles in One Pipeline" framing** added to DESIGN.md: stages 1-4 = code lifecycle ("is the implementation right?"), stage 5 = data lifecycle ("what did we learn?").
- **DESIGN.md bumped to v4.0.0** with Insight stage documentation, type eligibility table, DIKW accumulation ladder, and cross-layer contract (task → insight).
- **Architecture diagram** (01-architecture.txt) rebuilt: new sections for two-lifecycle framing (§3), cross-layer contract (§8), updated accumulation table with Insight column, schema chain extended to insight.

### Added
- `/haipipe-task insight <path>` command — runs Stage 5 only on an existing task folder.
- Stage 5 in `task-lifecycle.workflow.js` — eligibility check + Skill("haipipe-insight-data") call + card-reviewer-data-agent validation.
- Migration Phase 7 (Insight stage) in DESIGN.md.


## [3.1.0] — 2026-06-10

### Changed
- **Merged 4 Stata children into unified `haipipe-task-for-stata`.** Stages cms/case/data/reg are now handled internally via stage-specific `ref/config-seed-<stage>.do` and `ref/workflow-plan-sample-<stage>.yaml`. Config seeds are `.do` files (Stata source of truth), not YAML. Removed `haipipe-task-for-stata-{cms,case,data,reg}/` (4 directories, ~1500 lines).
- **Renamed `haipipe-task-for-training` to `haipipe-task-for-fit`.** "Fit" better reflects the skill's scope (model fitting, not just training).
- **Removed `config-meta-*.yaml` from Stata ref/.** The workflow layer reads `_meta:` from the task's own `configs/<run>.yaml` at runtime; separate templates were redundant.

### Added
- `haipipe-task-for-stata/fn/scaffold.md` — unified scaffold with shared steps and stage-specific branches.
- `haipipe-task-for-stata/ref/config-seed-{cms,case,data,reg}.do` — Stata config templates per stage.
- `task/TODO.md` — open design issues (for-agent quality, scaffold-vs-lifecycle tension, coverage gaps, model ID drift).

### Fixed
- `config-seed-reg.do` now includes `policy_path` and `policy_var`.


## [3.0.0] — 2026-06-09

### Changed
- **4-stage lifecycle (Plan/Build/Execute/Report)** via `task-lifecycle.workflow.js`. Creator-reviewer agent loop at each stage; all plans follow haipipe-workflow IPO schema.
- **All 13 type specialists aligned** with orchestrator v3: unwrapped prose (one line per paragraph), fixed agent names (`code-creator-for-*` → `haipipe-task-creator-agent`, `stata-script-reviewer-agent` → `haipipe-task-reviewer-agent`), added Invocation modes paragraph, added AUTO_MODE guard to scaffold Step 1.
- **Hub-and-spoke architecture documented** in DESIGN.md: haipipe-task is the hub, specialists are spokes; arrows go both ways; three entry paths (via hub lifecycle, via hub scaffold, direct spoke call).
- **Project/task-group scope moved to `project/haipipe-project`.** `fn/project.md` and `fn/task-group.md` relocated; haipipe-task owns task-folder and below only.
- **DESIGN.md rewritten** from Phase 2-3 snapshot to v3.0.0 architecture.

### Added
- `agents/haipipe-task-creator-agent.md` — produces artifacts (plan, code, report) at each lifecycle stage.
- `agents/haipipe-task-reviewer-agent.md` — evaluates artifacts (IPO compliance, code bugs, result accuracy). Two-stage: Claude drafts, Codex independently reviews.
- `haipipe-task/ref/task-lifecycle.workflow.js` — Workflow tool script driving the 4-stage creator-reviewer loop.
- `ref/workflow-plan-sample.yaml` in all type specialists (8 Python + 4 Stata children at the time).
- Workflow plan section in all specialist SKILL.md files pointing to the sample + schema.

### Removed
- `haipipe-task-batch/` — batch = multiple configs in one Build, not a separate skill.
- `haipipe-task-logging/` — superseded by Report stage (workflow/report*.yaml).
- Legacy `fn/task-folder.md` monolithic scaffold (deprecated since Phase 4).


## [2.0.0] — 2026-06-08

### Added
- Workflow lifecycle: audit, plan, report procedures in `fn/`.
- Three-layer plans: per-script IPO shape.
- Stata four-sister convention.
- Wired reviewer + auditor agents.

### Changed
- `ref/workflow-template.yaml` added.


## [1.0.0] — 2026-05-31

### Added
- **Agent families, split by folder.** `agents/` with two families: `creators/` (7 per-type builders) and `reviewers/` (2 type-agnostic gates: `run-script-reviewer-agent` + `run-result-auditor-agent`).
- **Shared knowledge packs:** `haipipe-task/ref/authoring-conventions.md` (4 sister files, `_meta` contract, heavy-artifact placement, reproducibility, first-run gate, builder!=judge, papermill/notebook) and `haipipe-task/ref/invocation-modes.md` (dual-mode contract + structured-return schema).
- **Batch orchestrator** `haipipe-task-batch` — fan out N typed specs, each flowing author → GATE 1 → run → GATE 2. Two engines: native parallel Agent calls, or `batch-pipeline.workflow.js`.
- **Notebook retention knob** `_meta.notebook: full | thin | off`.
- **Top-level `agents/` registry** (plugin root, flat symlinks) for `subagent_type` addressing.

### Changed
- **Renamed 7 type skills** `haipipe-task-<type>` → `haipipe-task-for-<type>`. All 155 references updated.
- **Dual-mode skills.** Interactive (ASK) or headless (silent); structured return block always emitted.
- **Per-run sanity checklist relocated from probe** to `run-result-auditor-agent`.

### Removed
- The single general `task-code-creator-agent` (superseded by 7 per-type creators).
