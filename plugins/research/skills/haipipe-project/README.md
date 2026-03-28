haipipe-project
===============

Skill for creating, reviewing, and summarizing haipipe research projects.
Covers both the experiment side (examples/) and the code side (code/ + code-dev/)
in one unified flow.

---

Commands
--------

  /haipipe-project new
      Start a new project from scratch. Asks a few questions (project ID,
      dataset, stages, new code needed?), then scaffolds the full folder
      structure under examples/ and optionally creates Track A stubs in
      code-dev/ and code/hainn/. Checks code/INDEX.md first to suggest
      reusing existing Fns or models across projects.

  /haipipe-project review [path]
      Inspect an existing project and generate any missing standard docs.
      Auto-detects the current project from git status if no path is given.

      What it checks (read-only):
        - Project naming convention and folder structure
        - Task-level config YAML validity and stage declarations
        - Run-result alignment per task
        - Code sync: config FnClass/ModelClass -> code/ resolution

      What it generates (writes to docs/ and tasks/INDEX.md only):
        - docs/TODO.md, docs/data-map.md, docs/dependency-report.md
        - tasks/INDEX.md and per-task INDEX.md files

  /haipipe-project summarize [path]
      Generate a plain-English post-development summary. Writes
      docs/project-summary.md with a short description, key results table,
      and an ASCII pipeline flow chart. Updates tasks/INDEX.md statuses.

  /haipipe-project organize [path]
      Inventory all project files, propose reorganization to match the
      standard layout, and -- if approved -- apply moves then verify
      that all imports and paths still work.

  /haipipe-project organize verify [path]
      Skip inventory and proposal; run only post-reorganization
      verification (import resolution, config check, relative paths).

---

Standard Project Layout
-------------------------

  examples/Proj{Series}-{Category}-{Num}-{Name}/
  +-- tasks/              MANDATORY. One subfolder per task.
  |   +-- INDEX.md        Global task index
  |   +-- {task}/         Self-contained: {task}.py, config/, runs/, results/
  |   +-- sbatch/         Cross-task SLURM scripts (optional)
  +-- paper/              OPTIONAL. Manuscripts, figures, LaTeX.
  +-- docs/               OPTIONAL. TODO.md, data-map.md, project-summary.md
  +-- cc-archive/         OPTIONAL. CC session history (cc_*.md, di_*.md)
  +-- _old/               OPTIONAL. Archived legacy files.

  Note: config/ is inside each task folder, not at the project top level.

---

Skill Files
-----------

  SKILL.md                    Router and dispatch table
  ref/project-structure.md    Standard layout, naming, task-folder rules
  ref/code-structure.md       code-dev/ builder pattern, hainn/ model layout
  fn/fn-new.md                Scaffold flow (both tracks, reuse check)
  fn/fn-review.md             Gap analysis + doc generation + code sync check
  fn/fn-summarize.md          Post-development summary + ASCII flow chart
  fn/fn-organize.md           File inventory + reorganization + verification
