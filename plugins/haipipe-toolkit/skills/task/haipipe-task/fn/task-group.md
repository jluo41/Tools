fn-block: Scaffold a New Block
==========================================

A block holds related jobs that share context: one diagram narrative, one sbatch coordinator, one group letter.

Output: `examples/{PROJECT_ID}/tasks/bNN_{group_name}/` (b = the level letter; NN = next free index in pipeline order).


Step 1 — Identify project (auto-cascade if missing)
----------------------------------------------------

Resolve the parent project:

  - explicit `--project-id <PROJECT_ID>`           → use it.
  - cwd inside `examples/Proj*/`                   → use it.
  - missing
      AUTO mode  → if `--project-id` given but no folder exists,
                   scaffold it via Skill("haipipe-project",
                   args="<PROJECT_ID> --auto"), then continue here.
                   If no project_id at all → status: blocked,
                   reason: "no parent project; pass --project-id or cd in."
      interactive → ASK which project (or scaffold one via /haipipe-project).


Step 2 — Collect metadata
--------------------------

  Group letter (G)    A / B / C / D / E / F / R / X  (DEFAULTS — the
                      project's existing scheme always wins; SKILL.md top NOTE)
                      A = fit              (training: pretraining, finetuning)
                      B = eval             (evaluation, inference, scoring)
                      C = display          (paper figures, paper tables)
                      D = data-pipeline    (Stage 1-4 builders)
                      E = individual       (individual-centric query / visualization)
                      F = agent            (LLM agent / prompt task)
                      R = raw              (Stage 0 extraction; embedded rawstore
                                            groups often use A00_rawstore_<cohort>)
                      X = algo-dev demo    (paired Track A smoke-test;
                                            X_algo/ — typically one per project)

  2-digit index (NN)  next free index within letter (no gaps; start 01).
                      Exception: `X_algo/` has no NN (singleton per project).

  snake_case name     <noun>_<qualifier>, passing the STRANGER TEST (hierarchy.md
                      "Naming"): a reader who never opened the folder reads WHAT
                      THING and WHICH ONE off the name. e.g. physician_ground_truth,
                      llm_recommendation_runs, paper_figures. ⛔ a shape word alone
                      (data, analysis, pool, rank) — REFUSE and ask "what thing?".

  Compose: `bNN_{group_name}` (e.g. `b01_physician_ground_truth`, `b02_llm_recommendation_runs`; the old letter form `A01_pretraining_clm` is legacy —
                                       `D01_data_wellreadi`,
                                       `C01_paper_figures`),
           or `X_algo` (no NN, no name suffix).

  Check existing groups under `tasks/` to avoid index collision.

  Letters are DEFAULTS, not type indicators — never infer task-type
  from the letter. The default scheme lives in `../SKILL.md` top NOTE;
  the project's own scheme always wins.


Step 3 — Create skeleton
-------------------------

```
tasks/bNN_{group_name}/
├── sbatch/
│   └── env.sh                ← seed with project env vars
└── (no README.md)
```

If the group is **cohesive** (multiple related jobs coming): also create `diagram/` and author via `/diagram-ascii`:

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


Step 4 — Optionally proceed to first job
-------------------------------------------------

Seed the first task within this group via the orchestrator's job scaffold: `Skill("haipipe-task", args="job <type> ...")`
(SKILL.md Step 3a dispatches to the type specialist).


MUST NOT
---------

- Create `README.md` in the group folder.
- Skip `sbatch/env.sh` — every group needs at least the env stub.
- Author diagram .txt content inline (always via `/diagram-ascii`).
