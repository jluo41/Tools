haipipe-task — Changelog
========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [5.5.0] — 2026-07-04

### Changed (JL: "task其实不aware of discovery insight probe, 对吗")

- CONFIRMED by JL 2026-07-05: 5.3.0-5.5.0 read-through ("OK，没问题。") and ref/hierarchy.md letter defaults A fit/B eval/C display/D data/E individual/F agent/R raw/X_algo ("okay 好"); both review threads removed. README Boundary: JL picked option B, his five-layer mental-model table restored (reader-facing only, no upward routing).

- task layer made upper-layer-UNAWARE, same principle as discovery: description + body no longer route users to /haipipe-insight (replaced with "a task ends at Report; whoever consumes results records the link on THEIR side"); ref/metrics-json-schema.md no longer names the probe extractor (retired haipipe-probe-result ref removed); ref/task-structure.md skill-runner example made layer-neutral. Agents' caller-mentions (dispatch target for probe-orchestrator) stay — discovery precedent: advertising to callers is not layer-awareness. haipipe-workflow keeps naming all layers (toolkit-wide infra, not task-layer doc).

## [5.4.0] — 2026-07-04

### Changed (JL: "你看看这个skill有没有重复的地方" + "One sentence one line")

- dedup pass on SKILL.md, each thing now said ONCE:
  - feedback/digest was explained 3x (Commands + a ~25-line Step 2(0) restating fn/feedback.md + fn/digest.md + a ~30-line tail section) — Step 2(0) reduced to pure routing, tail section reduced to a 5-sentence pointer; the fn/ files are the single source.
  - the 9 specialists were listed 2x — Dispatch Table now references the type table instead of re-listing.
  - plan/report artifacts + plan-schema pointer appeared 2-3x — "Per-task observability" section deleted; its one non-duplicated line (Plan = intent, Report = evidence, same IPO shape) folded into Four Stages.
  - "/haipipe-project for project scaffolding" said 2x (Commands footer dropped); "/haipipe-insight separately" said 3x (intro copy dropped); Stata delegation prose halved (the code block already carries it); group-letter NOTE in Step 3a now references the top NOTE.
- ## Feedback + ## Behavioral Preferences rewritten one sentence per line (JL's in-file note, applied and archived here).

## [5.3.0] — 2026-07-04

Skill-set review fixes (see task/SKILLSET_REVIEW.md for the full diagnosis):

- routing repaired: dispatch calls now use the real skill names `haipipe-task-for-<type>` (were `haipipe-task-<type>`, which resolves to nothing); `endpoint` added to the known-type list, dispatch table, keyword table, and script-inference cascade ("7 options" was stale — 8 types + Stata engine).
- Step 3b scaffolds route to their real owners: project → `/haipipe-project`, group → the new `task-group` verb.
- fn/task-group.md + fn/scan-status.md (received from the project layer 2026-07-03) are now WIRED: new Commands verbs `task-group` and `scan-status`, dispatch-table rows, Step 2 cascade entries.
- Agents section: says three agents (orchestrator/creator/reviewer triad — orchestrator row was missing); stale "Codex two-stage" review claim replaced with fresh-agent independence (reviewer v1.1.0 removed Codex 2026-06-23).
- deleted legacy `fn/task-folder.md` (DESIGN.md Phase 4 recorded its removal 2026-06-08 but the file survived on disk); repointed fn/task-group.md's reference to the Step 3a specialist dispatch.
- Risk Profile: dropped stale "scope=project" sentence.
- ref/task-lifecycle.workflow.js + ref/workflow-template.yaml: `project/haipipe-workflow/` → `task/haipipe-workflow/` (dead since the 2026-07-03 move).
- PREFERENCES.md sync note reworded layer-neutrally (no paper-layer skill named from task).
- `raw` wired as a first-class task-type (JL decision): type table, known-type list, keyword row, script-inference, dispatch table — /haipipe-task-for-raw was an orphan nothing routed to.
- ref/hierarchy.md group-letter table rewritten: letters are PROJECT-SPECIFIC with specialist defaults A fit / B eval / C display / D data / E individual / F agent / R raw / X_algo (old table had a third, conflicting scheme: A=model-run B=eval C=display D=demo).
- CHANGELOG itself repaired: the two 2026-07-03 entries were numbered 4.2.0/4.3.0 (below the then-current 5.0.0) and appended at the bottom of a newest-first file; renumbered to 5.1.0/5.2.0 and moved into order.

## [5.2.0] — 2026-07-03

- (renumbered from 4.3.0) received ref/task-structure.md from project/haipipe-project/ref/project-structure.md (ownership refactor: project owns only the top-level container). Carries group folders, task naming, task-folder contents, skill-runner exemption, group/task diagram contracts, run script templates, runs/results/notebooks/sbatch relationship, auto-example rule; rules already in ref/authoring-conventions.md stay there and are only pointed to.

## [5.1.0] — 2026-07-03

- (renumbered from 4.2.0) received fn/task-group.md + fn/scan-status.md (+ ref/scan_status scripts) from haipipe-project (project skill reduced to setup-only). haipipe-workflow also moved into task/.

## [5.0.0] — 2026-06-11

- remove Stage 5 (Insight) from task lifecycle — insight is /haipipe-insight's responsibility, not task's. This skill is now a pure 4-stage code lifecycle (Plan/Build/Execute/Report). Task-group iteration updated accordingly.

## [4.1.0] — 2026-06-11

- task-group iteration — when given a task-group path, enumerate child task-folders and run lifecycle on each one sequentially (Step 3d). Removed project/task-group redirects to /haipipe-project; this skill now owns both task-folder and task-group scope.

## [4.0.0] — 2026-06-11

- 5-stage lifecycle — add Stage 5 (Insight), optional, files D_data observation card via /haipipe-insight-data for insight-worthy types. Code lifecycle (1-4) + data lifecycle (5).

## [3.0.0] — 2026-06-09

- 4-stage lifecycle (Plan/Build/Execute/Report) via task-lifecycle.workflow.js; creator-reviewer agent loop at each stage; all plans follow haipipe-workflow IPO schema; type-specific workflow-plan-sample.yaml in every specialist; project/task-group scope moved to haipipe-project.

## [2.1.0] — 2026-06-08

- three-layer plans; per-script IPO; Stata four-sister; wire reviewer+auditor agents.

## [2.0.0] — 2026-06-08

- add workflow lifecycle — audit, plan, report. New fn/ procedures. New ref: workflow-template.yaml.

## [1.0.0] — 2026-05-31

- baseline metadata added.
