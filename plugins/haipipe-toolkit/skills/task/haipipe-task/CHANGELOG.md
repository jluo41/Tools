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
