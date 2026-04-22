haipipe-project
===============

Skill for creating, reviewing, and summarizing haipipe research projects.
Covers both the experiment side (examples/) and the code side (code/ + code-dev/)
in one unified flow.

---

Commands
--------

  /haipipe-project new [project|group|task]
      Three scopes:
        project  -- full project from scratch (folder + first group + first task)
        group    -- add a group folder to an existing project
        task     -- add a task folder to an existing group
      If scope omitted: asks which one.
      For "project": also asks about pipeline stages, datasets, and whether
      new Track A stubs are needed (code-dev/ + hainn/). Checks code/INDEX.md
      to suggest reusing existing Fns or models.

  /haipipe-project overview [path]
      Print a task-by-task overview of what the project does.
      Reads every task's README.md and produces a structured table
      per group: task name, what it does, paper/rebuttal reference, status.
      Read-only -- does not write any files.

  /haipipe-project review [path]
      Inspect an existing project and generate any missing standard docs.
      Auto-detects the current project from git status if no path is given.

      What it checks (read-only):
        - Project naming convention and folder structure
        - Task-level config YAML validity and stage declarations
        - Run-result alignment per task
        - Code sync: config FnClass/ModelClass -> code/ resolution

      What it generates (writes to docs/ and README.md files only):
        - docs/TODO.md, docs/data-map.md, docs/dependency-report.md
        - tasks/README.md, group README.md, and per-task README.md

  /haipipe-project summarize [path]
      Generate a plain-English post-development summary. Writes
      docs/project-summary.md with a short description, key results table,
      and an ASCII pipeline flow chart. Updates README.md status tables.

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
  +-- tasks/              MANDATORY. Two-level hierarchy.
  |   +-- README.md       Project-level task overview
  |   +-- {G}_{group}/   Group folders (e.g., A_data/, B_training/)
  |   |   +-- README.md   Group overview
  |   |   +-- {G}{N}_{name}/  Task folders (*.py, config/, runs/, results/)
  |   +-- sbatch/         Cross-task SLURM scripts (optional)
  +-- paper/              OPTIONAL. Manuscripts, figures, LaTeX.
  +-- docs/               OPTIONAL. TODO.md, data-map.md, project-summary.md
  +-- cc-archive/         OPTIONAL. CC session history (cc_*.md, di_*.md)
  +-- _old/               OPTIONAL. Archived legacy files.

  Note: config/ is inside each task folder (each task owns its own), not at the project or group level.

---

Skill Files
-----------

  SKILL.md                    Router and dispatch table
  ref/project-structure.md    Standard layout, naming, task-folder rules
  ref/code-structure.md       code-dev/ builder pattern, hainn/ model layout
  fn/fn-new.md                Scaffold flow (both tracks, reuse check)
  fn/fn-overview.md           Task-by-task project overview (read-only)
  fn/fn-review.md             Gap analysis + doc generation + code sync check
  fn/fn-summarize.md          Post-development summary + ASCII flow chart
  fn/fn-organize.md           File inventory + reorganization + verification
