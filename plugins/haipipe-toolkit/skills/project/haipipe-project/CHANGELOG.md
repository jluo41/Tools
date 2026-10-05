haipipe-project — Changelog
===========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [0.10.0] -- 2026-10-05

- New optional world `labelings/` (JL 261005: "a job is data + one-label"; "a dataset,
  it can have multiple labels"; "block is not necessarily a dataset, it should be a block").
  A Block is an ordinary Block (`bNN_<block>/`); a Job is one dataset with one label
  (`jNN_<dataset>_<label>/`, holding the label's `schema.yaml`) with many Tasks (JL 261005:
  "for this job, we will have many tasks"): its data preparation, its keys, its labeling
  Page (the engine's `labeling/` lane) and its scoring. It replaces the `tasks/b61`-`b69`
  labeling Blocks; a dataset with no label yet stays in `tasks/`. The audit accepts it.

## [0.9.1] -- 2026-10-04

- CoWork Blocks hold Jobs (JL 261004: "we should have the job, otherwise the work is
  hard to do"): `board.md`, `studio/`, `reports/`, `_old/` stay at the top; everything
  else lives in `jNN_<job>/` (one line of work, its `jNN_<job>.md` page header holding
  state, waiting-on, since, next), including `j00_people/` (who to ask). The Tickets
  register and the Block-level `ticket/`, `design/`, `materials/`, `emails/`,
  `meetings/` and `PEOPLE.md` are gone. The audit checks the new rule.

## [0.9.0] -- 2026-10-04

- `cowork/` topics are CoWork Blocks, `bNN_<topic>/` with a `board.md`
  (`board-kind: cowork-block`), owned by the new `haipipe-cowork` skill and
  opened by `haipipe-workbench-cowork` (JL 261004: "make the block as well").
  Ranges: `b0x` gates, `b1x` systems, `b2x` partners, `b3x` study operations.
  `board.md` replaces a topic's `README.md`; `reports/` joins the shared names;
  tickets live in each Block (Tickets register, `ticket/Timeline.md`,
  `ticket/CHECKLIST.md`), so the cowork root no longer has `Tickets/`.
- `scripts/audit_projects.py` checks each Block: `board.md` with the kind, no
  `README.md`, only the shared names; an old `N-<Topic>/` folder is a finding.
- Project-Samsung migrated: `0-IRB` → `b01_irb`, `1-Azure-Account` →
  `b11_azure_account`, `1-Epic-Streaming` → `b12_epic_streaming`,
  `1-SmartWatch-Connector` → `b13_smartwatch_connector`, `2-WellDocApp` →
  `b21_welldoc_app`.

## [0.8.0] -- 2026-10-04

- `cowork/` topic folders are numbered `N-<Topic>/` and share one subfolder
  set (JL 261004: "share the same subfolders as much as possible"):
  `README.md` (required), `PEOPLE.md`, `design/`, `materials/`, `ticket/`,
  `emails/`, `meetings/`, `studio/`, `_old/`, each only when it has files.
  The cowork root keeps `README.md`, `PEOPLE.md`, `Tickets/` and `_old/`.
  Replaces "topic folders are free-form" in `ref/project-structure.md`.
- `scripts/audit_projects.py` checks each `cowork/N-<Topic>/`: a README and
  only the shared names; anything else (for example `docs/`) fails the audit.
- First applied to examples-4-agent/Project-Samsung/cowork (0-IRB,
  1-Azure-Account, 1-Epic-Streaming, 1-SmartWatch-Connector, 2-WellDocApp).
- `fn/repo-project.md`: "Adopt an existing Project folder", the six steps
  used to make Project-Samsung its own repo (JHU-CDHAI/Project-Samsung).

## [0.7.0] -- 2026-10-03

- `diagram/` is retired (JL 261003: "no more diagram"). An existing `diagram/`
  is declared migration debt; project-level Boards move to `cowork/` when
  migrated, Task and Insight Boards to their owning world.
- New lazy world `cowork/`: coordination text (tickets, people, emails,
  meetings, design notes, drawings) and project-level Boards. Office files,
  recordings and files over 5 MB stay local through `cowork/.gitignore`.
- New profile-owned code folder `platforms/` (software/hybrid): one submodule
  per owned repo, mirroring the SPACE root `platforms/`.
- First Project on this layout: examples-4-agent/Project-Samsung.
- `scripts/audit_projects.py`: `cowork` is a world, `platforms` a code folder,
  `diagram` no longer a world.

## [0.6.0] -- 2026-10-03

- `insights/` holds an Insight topic as two boards (JL 261003):
  `Prototype-Insight-<Topic>/`, Block level (board.md, 0-Meta/, 1-Data … 4-Wisdom/
  question folders with their scripts, and the Block's `studio/` with the generated
  `question-map.excalidraw`), and `Instance-Insight-<Dataset>/`, one per dataset.
  The older `<Dataset>-InsightBoard/` keeps its layout until carried over.
- `ref/project-structure.md` gains an `insights/` section; the root tree, the
  boundary table and SKILL.md follow. Internals stay with `haipipe-insight`.
- `scripts/audit_projects.py` knows `insights/` and `designs/` as worlds; `applications/`
  is no longer one (legacy since 261001: declared migration debt).

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
