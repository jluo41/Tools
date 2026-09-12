# Changelog

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
