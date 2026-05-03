fn-task-group: Scaffold a New Task-Group
==========================================

A task-group holds related task-folders that share context: one diagram
narrative, one sbatch coordinator, one group letter.

Output: `examples/{PROJECT_ID}/tasks/{G}{NN}_{group_name}/`.


Step 1 — Identify project
--------------------------

Auto-detect from cwd or ASK.


Step 2 — Collect metadata
--------------------------

  Group letter (G)    A / B / C / D
                      A = model-run         (pretraining, finetuning)
                      B = evaluation        (eval, inference, scoring)
                      C = display           (paper figures, paper tables)
                      D = demo              (paired examples for Track A)

  2-digit index (NN)  next free index within letter (no gaps; start 01)

  snake_case name     descriptive name (e.g. pretraining_clm, paper_figures)

  Compose: `{G}{NN}_{group_name}` (e.g. `A01_pretraining_clm`,
                                       `C01_paper_figures`).

  Check existing groups under `tasks/` to avoid index collision.


Step 3 — Create skeleton
-------------------------

```
tasks/{G}{NN}_{group_name}/
├── sbatch/
│   └── env.sh                ← seed with project env vars
└── (no README.md)
```

If the group is **cohesive** (multiple related task-folders coming):
also create `diagram/` and author via `/diagram-ascii`:

```
01-overview.txt    Group purpose / scope / how tasks relate
02-tasks.txt       Table | Task | Type | Status | Notes |  (seed empty)
03-progress.txt    Dated log, newest on top, seeded with
                   "{YYMMDD} — group scaffolded"
04-design.txt      Shared design decisions across the group
                   (architecture choice, eval suite, figure style, ...)
```

Then bundle:
```
/diagram-ascii-canvas {GROUP}/diagram/  →  group.excalidraw
```

If the group represents a NEW research direction at the project level:
append a bullet to project's `03-exploration.txt` and re-bundle
`project.excalidraw`.


Step 4 — Optionally proceed to first task-folder
-------------------------------------------------

Invoke `fn/task-folder.md` (Scope 3) to seed the first task within
this group.


MUST NOT
---------

- Create `README.md` in the group folder.
- Skip `sbatch/env.sh` — every group needs at least the env stub.
- Author diagram .txt content inline (always via `/diagram-ascii`).
