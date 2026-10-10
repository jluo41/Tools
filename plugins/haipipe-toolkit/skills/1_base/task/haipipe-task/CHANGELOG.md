## 1.12.1 · 2026-10-09 · Theme folders are singular

- `ref/run-sh-template.sh`: a Ticket under `work/` (or `labeling/`) runs; the older `tasks/` and `labelings/`
  still do, and a work Run's store address is the same under either name. Docs name `work/`.

## 1.12.0 · 2026-10-09 · One folder per Run

- `ref/run-sh-template.sh`: a Ticket at `runs/<run>/<run>.sh` writes `runs/<run>/result/` (config may
  be `runs/<run>/config.yaml`); an older flat `runs/<run>.sh` still writes `results/<run>/`.
- `SKILL.md`, `fn/run.md`, `ref/block-job-task-run.md`, `ref/task-structure.md` describe the new layout.

## 1.11.1 · 2026-10-05 · The Insight Block (JL 261005; local 1.10.3, merged after upstream 1.11.0)

- `ref/hierarchy.md`: the DIKW Block `b5N_<topic>_dikw` with `workbench: insight` is an Insight Block, one Task per
  question, runs `<dataset>_<partition>` with no config (haipipe-insight `ref/block-contract.md`).
## 1.11.0 · 2026-10-05 · Run tickets also run under labelings/

- `ref/run-sh-template.sh`: a Block may sit under `tasks/` or `labelings/` (haipipe-project
  0.10.0). A `labelings/` Run's heavy output and store mirror go under `labelings/<address>`,
  so they never share a folder with a `tasks/` Run of the same address; `tasks/` paths are
  unchanged. `ref/hierarchy.md` shows `labelings/` in the Project tree.

## 1.10.3 · 2026-10-05 · S8 looks names up across the Project

- `ref/check_task_tree.py` S8: names are looked up across the whole Project, not only
  `tasks/`, so a Task Page linking a Discovery Page or its Paper Run in `discoveries/` no
  longer reads as a name that does not exist (REACH-SPACE b01_reach_jhu: 211 of 220 S8
  findings were such links). A generator that quotes code verbatim may mark the fence
  `<!-- s8-skip -->`.

## 1.10.2 · 2026-10-03 · Project tree names cowork/

- ref/hierarchy.md: the Project tree shows `cowork/` in place of the retired
  Project-root `diagram/` (haipipe-project 0.7.0). Block, Job and Task
  `diagram/` folders are unchanged.

## 1.10.1 · 2026-10-02 · Work presentation labels

- Document optional `work[].stage` and `role` for Paper-aligned Work lines.
  Keep authored order and native Task types; never infer a label from a folder.

## 1.10.0 · 2026-10-02 · Block Questions and Report Pages

- Optional Question and resource registers in `board.md`; Block-owned report
  Pages in `reports/` beside freeform `studio/` drawings. Reports use the Page
  writing lifecycle and retain native evidence references.
- Separate Question answers from P-B-E-R execution reports; add a preserving
  scaffold helper and document the Task Workbench's four working Views.

## 1.9.0 · 2026-10-01 · The DIKW Block (JL 261001)

- `ref/hierarchy.md` § Block number ranges: an InsightBoard's code lives in an auxiliary
  `b5N_<topic>_dikw` Block with Jobs by level (j1N data, j2N information, j3N knowledge,
  j4N wisdom); each dataset × partition is one config and Run `rNN_<dataset>_<cut>` naming
  its extract, cut and `answers:`; an InsightBoard page calls it through its own ticket
  with `RESULT_DIR=<page>/results/<ticket>/` (a consumer-owned Run), not `RESULT_STORE`.

## 1.8.2 · 2026-09-29 · synth_df at the Task type level (JL 260929)

- Task types: `description` now names its `synth_df`, one synthetic person's rows in each stored table, shown in every table notebook (`haipipe-task-for-description` 0.4.0 § synth_df; `haipipe-task-for-raw` 0.5.6 for the raw Block).

## 1.8.1 · 2026-09-29 · A Task Page has no `## Outline` (JL 260929)

- `ref/task-page.md` and `ref/task-page-template.md` no longer say the renderer generates `## Outline`: since haipipe-page 0.121 the plan lives in `draft/<stem>-draft-v<G>.<S>.md` and shows as the Outline table in Draft Space, and a Task Page has no `## Outline` section. The word Outline stays where haipipe-page keeps it: the OUTLINE workflow stage, the Outline table, and the `outline:` grammar key.

## 1.8.0 · 2026-09-29 · Reviews carry no commit id (JL 260929)

- Review gate: `CODE_REVIEW.md` carries no `git_sha`; a Ticket checks only that the review exists and its verdict is pass or warn, so a commit never blocks a Run. The template drops the stale-review check; `fn/audit.md` drops `stale_review`; `fn/run.md` and authoring-conventions say so.

## 1.7.0 · 2026-09-29 · Heavy output in ProjectResult (JL 260929)

- Artifact placement: a Run's heavy output goes to `HEAVY_DIR` = `_WorkSpace/ProjectResult/<Project>/<block>/<job>/<task>/<run>/` (Block and Job included because Task names repeat across Jobs); the Ticket writes `heavy.yaml` (path, bytes, sha256) into the Result; pipeline assets keep their stage stores. `run-sh-template.sh` exports `HEAVY_DIR` and writes the pointer. hierarchy.md and task-structure.md point to it.

## 1.6.0 · 2026-09-29 · Heavy output in _WorkSpace, checked

- authoring-conventions § Artifact placement: what counts as heavy (model, array, cache, row-level table, any file over 10 MB), which `$LOCAL_*` store it goes to, the pointer the Result keeps (path, size, sha256), no copy or symlink in the Task folder; `run-sh-template.sh` warns on a heavy file or link in the Result and a link in the Task folder. The law itself is haipipe-run's "A Result is light".

## 1.5.1 · 2026-09-29 · Generated output and encoded ids (JL 260929)

- authoring-conventions: every generated file (board HTML, TASK-TABLE.md, code/haifn) changes only through its source and generator, and a change is reported by its source; encoded ids are meaningless, not PHI, and never block a commit; before a push check size, secrets and `.pyc`.

## 1.5.0 · 2026-09-28 · No content hashes (JL 260928)

- Run receipts carry no content hashes (AGENTS.md rule 9): `ref/run-sh-template.sh` no longer writes `config_sha256`, `contract_sha256` or a per-input `sha256`. `RUN_INPUTS` entries are plain paths; an older `path|<hash>` entry is read as its path and the hash is ignored.
- A retry's changed-contract check uses file modification time: the Ticket, config, worker or a declared input newer than the prior receipt, or different `settings.ticket_args`, blocks the retry. A planned receipt blocks dispatch when its config is newer than the receipt.
- `ref/runtime-yaml-schema.md`, `ref/authoring-conventions.md`, `ref/task-structure.md`, `ref/hierarchy.md`, `ref/task-page.md`, `ref/databricks-execution.md`, `fn/audit.md`, `ref/task-lifecycle.workflow.js`, `fn/run.md` and `SKILL.md`: no hash fields, pins or hash checks; a Result is bound by full Run id and path.

## 1.4.6 · 2026-09-28

- ⛔ Hard rule under the title (JL 260928, AGENTS.md rule 6): never modify a generated file directly; change the code that writes it, then rerun.

# Changelog

## 1.4.5 — 2026-09-27

- Task Folders use `draft/` (Page skill 0.118) for the plan and its records; `page.py check-page-folder` and `page.py draft-layout` check and migrate existing Tasks.

## 1.4.4 — 2026-09-27

- Task types: `description` routes to the new `haipipe-task-for-description` (one Table Card per stored table: grain, column meanings, values, gotchas). `ref/run-sh-template.sh` writes the receipt `cmd` SPACE-relative (`space_rel`) and warns when the executed notebook or a Result file still shows an absolute path; it never edits the notebook, whose paths are fixed in the worker `.py` (JL 260927).
- `ref/authoring-conventions.md` § One Run, four projections: the notebook is generated from the worker `.py`; never edit it (by hand, find-and-replace, or a post-run rewrite); change the `.py` and rerun the Ticket (JL 260927).

## 1.4.3 — 2026-09-27

- `ref/authoring-conventions.md` § Paths (JL 260927): nothing a Run writes may hold an absolute path; paths are SPACE-relative (relative to the folder with `env.sh`), the worker resolves them by walking up to `env.sh`, and the notebook kernel starts in the Task folder because the SPACE root's `code/__init__.py` hides Python's `code` module and kills ipykernel.

## 1.4.2 — 2026-09-25

- `ref/hierarchy.md` § Block number ranges: AIData Block renumbered `b04` -> `b10` (JL 260925): `b00`-`b03` are per dataset (same `j5N` = same raw dataset), `b10`+ per question (`b10` builds training sets, `b11`+ models), so an AIDataSet's own `j5N` is never read as a dataset. `b04`-`b09` stay free. AIData pages name their inputs (`inputs: [b03/j58]`).

## 1.2.2 — 2026-09-18

- Rewrite `ref/databricks-execution.md` from what a live workspace proved
  (REACH-SPACE, SAFER desktop, 260907 to 260918). It showed an `.sh` ticket,
  an in-process inline run and run notebooks under `$OUTPUT_ROOT`; it now holds
  the `.cmd` ticket for a desktop where only cmd.exe runs, the inline run
  through the Command Execution API when no Job may use the cluster, one Result
  folder per Run fetched by its own ticket, the run record imported to the
  workspace, batches as flat lists that deploy once, the small-cell rule, the
  entry notebook's `RUN` binding, and three bundle deploy pitfalls.
- Add opt-in `resume` for a batch: skip a Run whose receipt says `status: ok`.

## 1.2.1 — 2026-09-15

- Mark `/haipipe-task insight` as the behavior-identical compatibility alias
  for the unified `/haipipe-insight task` entry.

## 1.2.0 — 2026-09-13

- Establish `haipipe-task` and `haipipe-page` as peer top-level doors over one
  physical Task Folder.
- Define the cross-face handshake from Page proposal through native Task Result
  and back to Page evidence binding and release.
- Keep `rNN` Task Runs and `rpNN` Page Runs in independent namespaces that may
  coexist in the shared `runs/` and `results/` lanes.
- Define `folder_closed = task_ready AND page_ready` and narrow staleness
  propagation across the two faces.

## 1.1.0 — 2026-09-12

- Declare the Page-owned `studio/` lane in the Task Folder, in both
  `ref/task-structure.md` and `ref/hierarchy.md`. A Task Folder is a Board Page,
  so it may already hold `studio/chat/` and `studio/draw/`; the contract had
  never said so and the checker permitted it only by omission.
- Add S4: a kept chat session carries BOTH `digest.md` and `transcript.md`, and
  `studio/` holds only `chat/` and `draw/`. Half a keep reads as a whole one —
  a decision list with no exchange under it, or an exchange nobody concluded.
- Record that a session kept outside the board server is hand-authored rather
  than projected from the live transcript, and says so in its own first lines.
- Note that a kept session is Page material, not generated output: it stays in
  the Task Folder and does not follow `$OUTPUT_ROOT` to a redirected store.
- Fix the Task Folder tree in `ref/task-structure.md`, which still drew
  `notebooks/tNN_<task>/rNN_<run>.ipynb` at the Job level after the 260909
  results rename moved it to `<task>/notebooks/<run>.ipynb`.

## 1.0.0 — 2026-09-08

- Establish one executable hierarchy: Project → Block → Job → Task Folder → Run.
- Define Task Folder = Page Folder at `tNN_<task>/`.
- Define Block = Task Board, Job = Board Group, and Task Folder = Board Page.
- Require the `bNN/jNN/tNN/rNN` name grammar and structural validation.
- Place Task-owned code in `scripts/`, Run config in `scripts/config/`, and
  Tickets in `runs/`.
- Place generated Results and notebooks under the parent Job's resolved
  `$OUTPUT_ROOT` with the exact `<task>/<run>` suffix.
- Make lifecycle execution accept only `task_folder` and reject malformed
  containers.
- Rename the Block scaffolding contract to `fn/block.md`.
- Add a repository gate that rejects non-v1 vocabulary and paths within this
  Skill package.
