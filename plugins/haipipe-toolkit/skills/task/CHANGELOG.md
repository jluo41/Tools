task — Changelog
==================

Layer-scoped changelog for the task (WORK / execution) layer. Newest first.
Rollup lives in the plugin-level `CHANGELOG.md`.

## [Unreleased] — 2026-07-14 — the task layer becomes consumer-unaware

Spec of record: `Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/` v3 (APPROVED by JL 2026-07-14, rulings R1-R18).
Constitution: `probe/haipipe-probe/SKILL.md` v8.0.0.

### Removed
- `haipipe-task/fn/asks.md` — the probe-aware SCREEN/ANSWER verb. Deleted, not archived.
- The `_ASK/` mailbox, `_ANS/`, the `answers:` report field, and every external id under
  `tasks/`. Nothing in this bucket references a consumer any more.

### Added
- `haipipe-task/fn/qa.md` — **the `qa` verb**, the layer's one question door.
  `/haipipe-task qa "<question>" [<leaf>]`: one question in general language in, a PATH to
  `<leaf>/QA/<n>-<slug>.md` out. Gate ① QA SCAN → ② DIGEST → ③ P-B-E-R at the shallowest
  depth (0 read | 1 new run+config | 2 new script | 3 new leaf), or 🚫 REFUSE. Three
  callers, one identical door: a human, the orchestrator self-directed, or a relayed
  question.
- The **OPTIONAL `QA/` folder** on every task-folder: the leaf's readable, numbered map of
  the directions it has explored. Authored by THIS layer at Report; write-once; slug only;
  three reasons only; no consumer vocabulary.

### Changed
- Agents: orchestrator 2.0.0 (clean-context dispatch target, COMMISSION input form, runs
  the qa gate, returns `qa_file:`, may be self-directed) · creator 3.0.0 (authors the QA
  digest at Report — the pen never leaves this layer) · reviewer 1.2.0 (the report gate
  lints the digest). `agents/README.md` rewritten: the wall is the orchestrator's clean
  context, not a folder.
- `haipipe-workflow` 2.4.0: `ref/plan-schema.md` drops `answers:` entirely.
- `DESIGN.md`: "Boundary with probe" → "Boundary: the task layer is CONSUMER-UNAWARE";
  "Downstream Consumer Contract" → "The read surface"; the sandwich model is superseded.
  `README.md` + `ref/metrics-json-schema.md` + `fn/workflow-plan.md` swept of upper-layer
  vocabulary.
- **The task session's PRIMARY mode is stated plainly for the first time:** autonomous
  P-B-E-R with NO question pending. Answerability work (digests + code that makes future
  questions cheap) is task-native. `qa` is a side door, never the engine.

## [Unreleased] — 2026-07-04

### Changed
- README Boundary section reworded self-contained-style (JL: task is unaware of
  discovery/insight/probe): states the hand-off principle without naming upper
  layers, mirroring discovery's "self-contained by design" convention. Layer
  guidance in haipipe-task SKILL.md/ref cleaned the same way (see
  haipipe-task/CHANGELOG.md 5.5.0).


## [Unreleased] — 2026-06-22

### Added
- Added `README.md` with the concise task mental model: lifecycle mnemonic
  `规建行报` for Plan / Build / Execute / Report, and domain mnemonic
  `数算端体训评图统代` for the nine append-only task domains.


## [6.0.0] — 2026-06-21

### Changed
- **Phase 1 of the B-domain migration LANDED (folder reorg, skill names unchanged).** The nine `haipipe-task-for-xxx` specialists are now nested under numbered DOMAIN folders, dissolving the parallel "type-spoke" family into the domain family:
  - `for-data`→`1_data/`, `for-algo`→`2_nn/`, `for-endpoint`→`3_end/`, `for-individual`→`4_individual/` (existing domain folders, unchanged numbers).
  - `for-fit`→`5_fit/`, `for-eval`→`6_eval/`, `for-display`→`7_display/`, `for-stata`→`8_stata/`, `for-agent`→`9_agent/` (5 new append-only domain folders).
  - Moved via `git mv` (history preserved). Skill `name:` fields UNCHANGED, so all `/haipipe-*` commands and `Skill("haipipe-task-for-xxx")` calls still resolve. No renumber of existing folders (append-only rule).
- **Fixed relative hub references in the moved folders.** All 45 `../haipipe-task/` references gained one `../` (mechanical consequence of moving one level deeper); strict refs (SKILL.md, config-seed, stata-dialect) now resolve correctly.
- **Updated structural docs to the new layout:** DESIGN.md "Current State" tree, `01-architecture.txt` folder tree, and the path-pattern hints in `task-lifecycle.workflow.js` / `haipipe-task-creator-agent.md` / orchestrator SKILL.md (now glob-friendly for the nested specialists).

### Note
- Phase 2 (renaming the `for-xxx` skills) is REJECTED (decided 2026-06-21): the names stay `haipipe-task-for-xxx` by design, since the `haipipe-task-` prefix keeps each specialist clearly part of the haipipe-task family. The migration is COMPLETE at Phase 1; there will be no skill rename.
- Fixed 2 pre-existing dangling refs along the way: `for-stata-case` -> `8_stata/haipipe-task-for-stata/ref/config-seed-run.do` (in `haipipe-task/fn/workflow-audit.md`, committed); `for-inference` -> `3_end/haipipe-task-for-endpoint/ref/inference-perf-notes.md` (in `fn-3-profile.md`, which is untracked, so that fix is working-tree-only).


## [5.2.0] — 2026-06-21

### Added
- **"Target Architecture: B as the Unified Domain Family (v6.0.0, PLANNED)" section in DESIGN.md.** Locks the decision to dissolve axis C (the `haipipe-task-for-xxx` type spokes) into axis B. B becomes a single flat NUMBERED family of 9 task domains, each owning both a run/library leg and a task-author leg. Includes: the APPEND-ONLY numbering rule (id = creation order, permanent, never renumbered; pipeline-flow order is a separate documented attribute, not the id; existing folders fixed at data=1/nn=2/endpoint=3/individual=4, appended fit=5/eval=6/display=7/stata=8/agent=9), the relaxed coverage rule (overlap is fine; every task type must fall into exactly one domain), the nine-domain table, the for-xxx -> domain mapping, the nn/fit shared-library note, the agent scope boundary vs application, and a two-phase migration plan with measured blast radius (~40 files; most are skill-NAME references that survive a folder move; Phase 1 touches zero existing folders).
- Decision Log entry (2026-06-21) recording the approval, marked as superseding the earlier "type spokes stay unnumbered" line.

### Note
- This is DESIGN ONLY. No folders have moved yet. The actual migration (Phase 1 folder reorg + Phase 2 optional rename) will land under a future [6.0.0].


## [5.1.0] — 2026-06-21

### Added
- **"Three Orthogonal Axes" section in DESIGN.md.** Makes explicit that `task/` mixes three different organizing axes: (A) the 4-stage lifecycle, (B) the numbered task domains `1_data / 2_nn / 3_end / 4_individual`, and (C) the `haipipe-task-for-xxx` type spokes. A and B are numbered because they are sequenced (time / data-flow DAG); C stays an unnumbered enum because task type is a classification, not a sequence. Also documents that B and C overlap by domain but are two layers (pipeline primitive vs task-folder authoring), not duplicates.
- Decision Log entry (2026-06-21) recording the axes distinction.

### Changed
- DESIGN.md status + Current State heading bumped to v5.1.0 (doc-only clarification; no structural or behavioral change).


## [5.0.0] — 2026-06-11

### Removed
- **Stage 5 (Insight) removed from the task lifecycle.** task is now a pure 4-stage code lifecycle (Plan / Build / Execute / Report). Insight filing is `/haipipe-insight`'s responsibility, not task's.

### Changed
- **Sandwich model adopted.** probe open dispatches discoveries/tasks; discover and task do their own work; probe post resumes and judges the claim. task no longer owns insight filing, and insight export is deferred while focusing on Narrative / Probe / Discovery / Task. (Migration Phase 7 closed.)
- Task-group iteration updated for the pure 4-stage lifecycle.


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
