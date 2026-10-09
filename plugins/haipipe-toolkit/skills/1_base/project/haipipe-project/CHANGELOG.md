## 0.14.0 · 2026-10-09 · audit and update at Project level: every step, planned then applied

- `scripts/project.py` (fn/audit.md § A Project, fn/update.md § A Project · the steps): `audit` lists
  every finding with the `update` step that fixes it (tools gate and contract drift, root, themes,
  convert, runs, faces) or marks it for a person; `update` dry-runs every step; `update --apply` runs
  them in order, re-audits after each, stops if failures rise, verifies, and never commits. The decided
  words stay audit and update (run-skill-draft Part B, 261006); no new verb.
- `scripts/probe_tickets.py`: where each moved ticket writes its Result, by running only its path lines
  (writing commands dropped, under its own name); an owner's gate counts as gated.
- `scripts/link_check.py`: links into results/ or runs/ that do not resolve, with --save/--compare so an
  update reports only what it newly broke.
- `tests/test_project_update.py`: a scratch SPACE with every older layout (plural Themes, flat Runs,
  Job-level Results, a Job-centred Job, missing faces, diagram/); audit finds every step, the dry run
  changes nothing, --apply leaves it clean with every ticket resolving and no link newly broken.

## 0.13.0 · 2026-10-09 · Theme folders are singular

- `scripts/rename_themes.py <project> [--list] [--apply]`: renames a Project's Theme folders to the singular
  names, patches its tickets and relinks references (folders renamed on disk; submodules by `git mv`; a stale
  `.gitmodules` entry is skipped; a half-done pair resumes). The root audit reads `work/`, `discovery/`,
  `paper/`, `insight/`, `design/`, `labeling/`, `ideation/` and reports an older plural folder as
  "rename pending". Docs name the singular folders.

## 0.12.0 · 2026-10-09 · one folder per Run, applied to the examples

- `scripts/ladder.py update`: patches each moved ticket, finds Job-level Results, relinks references
  (prefiltered by Run name), tidies `diagram/`, Job `notebooks/` and Job `workflow/`; a world child that
  is not a Block is reported as debt; a family Block (`Prototype-` …) is left to its owner's ladder.
- `ref/ladder.md`: a Task may hold `sbatch/` (haipipe-task allows it); `heavy_exempt` lets a discovery
  `paper.pdf` pass in a Project whose `project.yaml` says `visibility: private` (JL 261009).
- A moved Run's old receipt (run.yaml `moved_from:`) is history: the audit no longer checks the paths
  it recorded (JL 261009); tickets, run.yaml and new receipts stay strict.
- `ideations/` is a world (haipipe-ideation's home); `SKILL.md` and `ref/project-structure.md` point
  to haipipe-insight's current Prototype + Board layout; `fn/update.md` documents ticket, relink, tidy.

## 2026-10-07 — the ladder reads paper Boards (b03 s21, for b16)

- `ref/ladder.md`: a Block may be a paper Board, `Paper-<Slug>/`; Job and Task names take kebab tails
  (`t02_literature-review`, `t00_reason-ideas`); a paper Board may hold `venues/` and `related/` (a meeting's
  comments are a comments report, `reports/qNN_meeting-<MMDD>/`). `scripts/ladder.py` `family_of` reads a `Paper-` Block, or one in `paper/` or
  `papers/`, as the paper family. Renaming paper Boards to `bNN_<paper>` stays JL's call.

haipipe-project — Changelog
===========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [0.11.0] -- 2026-10-06

- Audit and update at every level (JL 261006: "update the /haipipe-project audit as well,
  like we can update any block job task"). `audit` and `update` take a Block, a Job, a Task
  or a Run; the level comes from the folder name. New `ref/ladder.md`, the one table of each
  level's face, allowed folders, children and Run names, read by new `scripts/ladder.py`.
  `audit_projects.py` sends a path below a Project to it and gains `--deep`.
- The ladder checks shape only; content stays with the owning skill. It follows the Run
  design (haipipe-run 0.31.0): one folder per Run in `runs/`, hard `rNN_<slug>` with
  `result/` in a work Task, soft `run-<type>-<target>` with no date, `run.yaml` as the card.
- `update` is a dry run unless `--apply`: it moves the old `runs/<run>.sh` + `results/<run>/`
  layout into `runs/<run>/` (folders whole, nothing inside a Result edited) and writes
  missing `run.yaml` cards with `moved_from:`.

## [0.10.0] -- 2026-10-05

- New optional world `labelings/` (JL 261005: "a job is data + one-label"; "a dataset,
  it can have multiple labels"; "block is not necessarily a dataset, it should be a block").
  A Block is an ordinary Block (`bNN_<block>/`); a Job is one dataset with one label
  (`jNN_<dataset>_<label>/`, holding the label's `schema.yaml`) with many Tasks (JL 261005:
  "for this job, we will have many tasks"): its data preparation, its keys, its labeling
  Page (the engine's `labeling/` lane) and its scoring. It replaces the `tasks/b61`-`b69`
  labeling Blocks; a dataset with no label yet stays in `tasks/`. The audit accepts it.
- `insights/` keeps only older register-kind boards; an Insight topic is one `tasks/b5N_<topic>_dikw/` Block with
  `workbench: insight` (haipipe-insight `ref/block-contract.md`). The Prototype + Instance pair is retired.

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
