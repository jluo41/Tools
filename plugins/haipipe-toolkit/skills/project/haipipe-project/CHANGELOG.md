haipipe-project — Changelog
===========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [0.4.0] -- 2026-09-04

- Replace name-selected project kinds with independent `profile` and
  `git_mode` fields in the new `haipipe-project/v1` manifest.
- Require `README.md` and `project.yaml` for every active Project while
  making all content worlds lazy rather than scaffolding empty directories.
- Add `external/` as a narrow read-only upstream boundary and define
  research/software/hybrid root-code profiles.
- Align the Project boundary with current BJTR Task, Run, Discovery, Page, and
  Task/Insights Board contracts; remove stale two-level Task, retired Probe,
  and top-level Insight rules.
- Add read-only `audit`, safe `update`, and deterministic
  `scripts/audit_projects.py`. Routine updates record risky relocations as
  migration debt instead of moving submodules, Results, Boards, or code trees.
- Remove the missing `PREFERENCES.md` dependency from the entrypoint.


## [0.3.4] -- 2026-08-06

- `ref/project-structure.md` papers/ row repointed: the paper-folder contract is
  `paper/haipipe-paper/fn/folder.md` + `ref/paper-folder-anatomy.md` (thin-paper
  phase 3 retired the standalone folder skill), and the owner column reads the
  one door `/haipipe-paper`.

## [0.3.3] — 2026-08-05

- `haipipe-paper-lifecycle` is retired (thin-paper phase 2): paper-folder
  scaffolding rows now read `/haipipe-paper folder` in SKILL.md and
  fn/repo-project.md.

## [0.3.2] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 3.2.0; older entries below keep their original numbers).

## [1.0.0] — 2026-05-31

- baseline metadata added.

## [1.1.0] — 2026-07-03

- added repo verb (fn/repo-project.md). Project-* names = repo-backed submodule projects.

## [2.0.0] — 2026-07-03

- consolidated project/ to ONE skill. haipipe-project-inspect + haipipe-project-organize merged in as fns; haipipe-workflow moved to task/. (Superseded by 3.0.0 which retired those fns.)

## [3.0.0] — 2026-07-03

- reduced to setup + scaffolding only. task-group and scan-status fns (+ ref/scan_status scripts) moved to task/haipipe-task; review/summarize/inventory/overview/organize retired to project/_archive (full original skills preserved there). haipipe-project = fn/project.md + fn/repo-project.md + feedback/digest.

## [3.0.1] — 2026-07-03

- removed hardcoded default org. --org is resolved per invocation (flag, or ask with candidates from .gitmodules + gh api user/orgs); the skill serves many workspaces and owners.

## [3.0.2] — 2026-07-03

- ref/project-structure.md rewritten to the ownership principle (583 -> ~115 lines): container-only (naming, top-level layout incl. discoveries/ and papers/, seven-worlds table + dependency map, project diagram/ contract, _WorkSpace note, structure-ownership pointer table). tasks/ internals moved to task/haipipe-task/ref/task-structure.md; Review Checklist archived to project/_archive/review-checklist.md; probe/insight/application/paper internals dropped to pointers (their owners carry the schema authorities).

## [3.0.3] — 2026-07-03

- project diagram/ contract trimmed to 01-story + 02-boundary; 03-exploration.txt retired (JL: no need to create it). All append-to-exploration rules removed here and in task/haipipe-task refs; exploration/backlog tracking lives in group/task diagram/ instead.

## [3.0.4] — 2026-07-03

- setup is QUICK by default — create container folders (+ README/.gitignore for repo kind) and stop. Diagram authoring (01-story, 02-boundary), first task-group, and Track A stubs demoted to on-request extras; no metadata questionnaire at setup. fn/project.md restructured to 3 steps + extras section.

## [3.0.5] — 2026-07-03

- ADOPT mode — an existing <org>/<name> repo is no longer a preflight failure: skip create, submodule add pulls the existing content, scaffold only missing folders (JL: 如果已经有，就直接pull). Description frontmatter tightened.
## 0.4.0 · 2026-09-04

- Add optional, on-demand `meetings/` ownership through
  `haipipe-project-meeting`; project scaffolding still creates no empty lane.
- Replace the retired Page Probe/PageX scaffold description with typed
  Evidence Items and Supporting/Local Run binding.
