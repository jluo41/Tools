fn-task-group: Scaffold a New Task-Group
==========================================

A task-group holds related task-folders that share context: one diagram
narrative, one sbatch coordinator, one group letter.

Output: `examples/{PROJECT_ID}/tasks/{G}{NN}_{group_name}/`.


Step 1 — Identify project (auto-cascade if missing)
----------------------------------------------------

Resolve the parent project:

  - explicit `--project-id <PROJECT_ID>`           → use it.
  - cwd inside `examples/Proj*/`                   → use it.
  - missing
      AUTO mode  → if `--project-id` given but no folder exists,
                   recursively invoke `fn/project.md` to scaffold it,
                   then continue here.
                   If no project_id at all → status: blocked,
                   reason: "no parent project; pass --project-id or cd in."
      interactive → ASK which project (or scaffold one via fn/project.md).


Step 2 — Collect metadata
--------------------------

  Group letter (G)    A / B / C / D / E / F / X
                      A = model-run        (pretraining, finetuning)
                      B = evaluation       (eval, inference, scoring)
                      C = display          (paper figures, paper tables)
                      D = data-pipeline    (Stage 1-4 builders)
                      E = individual       (individual-centric query / visualization)
                      F = agent            (LLM agent / prompt task)
                      X = algo-dev demo    (paired Track A smoke-test;
                                            X_algo/ — typically one per project)

  2-digit index (NN)  next free index within letter (no gaps; start 01).
                      Exception: `X_algo/` has no NN (singleton per project).

  snake_case name     descriptive name (e.g. pretraining_clm, data_wellreadi,
                                            paper_figures, subject_views).

  Compose: `{G}{NN}_{group_name}` (e.g. `A01_pretraining_clm`,
                                       `D01_data_wellreadi`,
                                       `C01_paper_figures`),
           or `X_algo` (no NN, no name suffix).

  Check existing groups under `tasks/` to avoid index collision.

  Letter ↔ task-type consistency (enforced when invoked by a type
  specialist): see the mapping table in `../SKILL.md` Step 3a.


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
