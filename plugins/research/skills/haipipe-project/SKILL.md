---
name: haipipe-project
description: "Standardize new project creation, review, summary, organization, and routing in the haipipe workspace. Use when the user wants to create a new project under examples/, review an existing project's structure, check script-result alignment, generate a post-development summary, reorganize project files, verify imports after file moves, or ask what subskill to use. Also use when the user mentions /haipipe-project, project scaffold, new experiment, project review, project summary, organize project, reorganize files, or what should I do next."
---

Skill: haipipe-project
=======================

Covers project-level structure across TWO tracks simultaneously:

  Track B  ->  examples/{PROJECT_ID}/    tasks, configs, runs, results, paper
  Track A  ->  code-dev/ + code/hainn/   pipeline Fn builders, ML model stubs

The user never needs to specify which track. Both are handled automatically.

Two structural rules that govern all projects:

  Rule 1 -- Self-contained grouped tasks:
    tasks/ uses the task-folder paradigm with letter-number grouping.
    Each task is named {G}{N}_{name} (e.g., B1_train_stats) where the
    letter groups related tasks and the number gives sequence within
    the group. Each task subfolder contains everything needed to
    understand and run the task: logic (.py), demo notebook (.ipynb),
    config/ (only configs this task uses), runs/, results/, and INDEX.md.
    No flat files directly in tasks/ (except sbatch/).

  Rule 2 -- Code always has a paired example:
    Every new pipeline Fn stub or ML model stub created in Track A
    AUTOMATICALLY generates a paired example task in tasks/.
    No Track A code without a Track B example.

Default (no arg): show command menu and ask what the user wants to do.

---

Commands
--------

  /haipipe-project new                    -> scaffold a new project (both tracks)
  /haipipe-project review                 -> gap analysis + generate docs: auto-detect current project
  /haipipe-project review [path]          -> gap analysis + generate docs for the project at [path]
  /haipipe-project summarize              -> post-development summary + flow chart (auto-detect)
  /haipipe-project summarize [path]       -> summary for the project at [path]
  /haipipe-project organize               -> file inventory + propose reorganization (auto-detect)
  /haipipe-project organize [path]        -> file inventory + propose reorganization for [path]
  /haipipe-project organize verify        -> verify imports/paths after manual reorganization (auto-detect)
  /haipipe-project organize verify [path] -> verify imports/paths for [path]
  /haipipe-project nb                     -> create a demo notebook for a task (auto-detect)
  /haipipe-project nb [path]              -> create a demo notebook for a task at [path]
  /haipipe-project help [question]        -> route a natural-language request to the right subskill + step

---

Dispatch Table
--------------

  Invocation               Ref file(s)                                       Function file
  -----------------------  ------------------------------------------------  ---------------------
  new                      ref/project-structure.md + ref/code-structure.md  fn/fn-new.md
  review (no path)         ref/project-structure.md + ref/code-structure.md  fn/fn-review.md
  review [path]            ref/project-structure.md + ref/code-structure.md  fn/fn-review.md
  summarize (no path)      ref/project-structure.md                          fn/fn-summarize.md
  summarize [path]         ref/project-structure.md                          fn/fn-summarize.md
  organize (no path)       ref/project-structure.md                          fn/fn-organize.md
  organize [path]          ref/project-structure.md                          fn/fn-organize.md
  organize verify          ref/project-structure.md                          fn/fn-organize.md
  organize verify [path]   ref/project-structure.md                          fn/fn-organize.md
  nb (no path)             ref/project-structure.md                          fn/fn-nb.md
  nb [path]                ref/project-structure.md                          fn/fn-nb.md
  help [question]          (none -- intent routing only)                     fn/fn-help.md
  (no arg)                 (none)                                            (show menu below)

---

Step-by-Step Protocol
----------------------

Step 0: Parse the command.

  Extract the subcommand from args after "/haipipe-project":
    "new"              -> fn-new mode
    "review"           -> fn-review mode (path optional)
    "summarize"        -> fn-summarize mode (path optional)
    "organize"         -> fn-organize mode (path optional; "verify" sub-arg triggers Phase 3 only)
    "nb"               -> fn-nb mode (path optional)
    "help"             -> fn-help mode (natural-language question follows; no ref files needed)
    (no arg)           -> print the command menu and ask what user wants

  If no arg, print:

    haipipe-project commands:
      new                       -> create a new project (both tracks)
      organize [path]           -> restructure files to standard layout (run FIRST on existing projects)
      review [path]             -> generate all docs + check code sync (run AFTER organize)
      summarize [path]          -> generate post-development summary + flow chart
      organize verify [path]    -> verify imports/paths after reorganization
      nb [path]                 -> create a demo notebook for a task
      help [question]           -> describe what you want in plain English; I'll route you

    Typical sequence for an existing project:
      1. organize [path]   <- move files into standard layout
      2. review [path]     <- generate docs (TODO, dependency-report, INDEX.md)

    Which would you like to do?

Step 1: Read ref files FIRST.

  For new / review:
    Read BOTH ref files before proceeding:
      Tools/plugins/research/skills/haipipe-project/ref/project-structure.md
      Tools/plugins/research/skills/haipipe-project/ref/code-structure.md

  For summarize / organize / nb:
    Read ref/project-structure.md only.

  For help:
    Read NO ref files -- intent routing only, no project files needed.

  This is MANDATORY. Do not proceed to Step 2 until all required ref files
  are in context. They contain the naming convention, task-folder layout,
  config sharing rules, and Track A conventions.

  Confirm by stating:
    "Loaded: [ref files]. Executing: [subcommand]."

Step 2: Read the function file.

    new        ->  fn/fn-new.md
    review     ->  fn/fn-review.md
    summarize  ->  fn/fn-summarize.md
    organize   ->  fn/fn-organize.md
    nb         ->  fn/fn-nb.md
    help       ->  fn/fn-help.md  (no ref files needed -- intent routing only)

  Follow the steps in the fn file exactly.

---

Checkpoint Hints (defaults -- fn files may customize wording per context)
------------------------------------------------------------------------

  CH-1  docs/ files updated?
        "Quick check: open docs/ and confirm all generated files look correct
         (TODO.md, dependency-report.md). Did anything come out empty?"

  CH-2  tasks/INDEX.md in sync?
        "Quick check: does tasks/INDEX.md have a row for every task subfolder?
         Does each {task}/INDEX.md exist? Are all status values current?"

  CH-3  file paths valid?
        "Quick check: any scripts that reference config/, results/, or docs/ paths --
         confirm those paths still exist relative to the task folder."

  CH-4  code/INDEX.md updated?
        "Quick check: if new Track A stubs were created, confirm code/INDEX.md has
         stub-status rows for them (so future projects can find them for reuse)."

  CH-5  YAML placeholders filled?
        "Quick check: search config/ for any remaining TODO_ values -- all placeholder
         class names must be replaced before running the pipeline."

  CH-6  reorganization pending verification?
        "Reminder: if you moved or renamed files manually, run
         /haipipe-project organize verify to confirm imports and paths still work."

  CH-7  config symlinks valid?
        "Quick check: verify config/ symlinks in each task resolve to existing targets.
         Run: find tasks/ -name config -type l -exec test ! -e {} \\; -print"

Each fn file lists which hints to print at the end of its execution chain.

---

Key Conventions (quick reference)
-----------------------------------

Project naming:   Proj{Series}-{Category}-{Num}-{Name}
  e.g.            ProjC-Model-2-GlucoseTransformer

Standard layout (Track B):
  tasks/          Self-contained task folders — MANDATORY (the only mandatory folder)
                  tasks/INDEX.md = global task list; {task}/INDEX.md = run inventory
                  tasks/sbatch/ = cross-task SLURM scripts only
  paper/          Manuscripts, LaTeX, figures (optional; often a git submodule)
  docs/           Internal planning docs (optional: TODO.md, project-summary.md)
  cc-archive/     CC session history (optional)
  _old/           Archived legacy files (optional)

  paper/ vs docs/ boundary:
    paper/ = external-facing (submitted manuscript, review responses, slides)
    docs/  = internal-facing (TODO, progress tracker, design notes, team onboarding)

  Note: no top-level config/ or results/ folder.
  Configs live inside task folders (with symlinks for sharing).
  Results live inside each task's results/ subfolder.

Task naming: {G}{N}_{task_name}
  G = uppercase letter (A-Z), groups related tasks by category
  N = digit (0-9), sequence within the group
  task_name = snake_case descriptor
  Example: B1_train_stats, C2_eval_main_table, D1_demo_modeltuner
  The project decides what each letter means (not prescribed by the skill).

Task folder contents:
  {task}.py       Logic (source of truth, # %% cell format)
  {task}.ipynb    Demo notebook (optional, derived from .py)
  config/         YAML configs (only configs this task uses — no shared dumps)
  runs/           Self-contained .sh scripts (no args — bash it and done)
  results/        Light summaries (run name = result folder name)
  INDEX.md        Run inventory

Config sharing: one task owns real config files, others symlink.
  cd tasks/D2_demo_modelinstance && ln -s ../D1_demo_modeltuner/config config

code/INDEX.md (codebase-wide, shared across all projects):
  Indexes ALL implemented Fns (code/haifn/) and ML models (code/hainn/).
  Claude reads this BEFORE creating any new Fn or model -- reuse first.

Auto-example rule:
  Every Track A stub generates a paired example task in tasks/.

_WorkSpace paths:
  Declared in env.sh. Read by setup_workspace() in code/haipipe/base.py.
  NEVER declare _WorkSpace paths inside the project folder.

Track A handoff:
  Pipeline Fns  ->  /haipipe-data design-chef {stage}
  ML models     ->  /haipipe-nn
  Endpoints     ->  /haipipe-end

---

File Map
--------

  SKILL.md                    <- you are here (router + dispatch table)
  ref/project-structure.md    <- Track B standard layout, naming, task-folder, config sharing
  ref/code-structure.md       <- Track A code-dev/ + hainn/ conventions
  fn/fn-new.md                <- scaffold new project (interactive, both tracks)
  fn/fn-review.md             <- gap analysis + proposed actions (both tracks)
  fn/fn-summarize.md          <- post-development summary + flow chart
  fn/fn-organize.md           <- file inventory + reorganization proposal + verification
  fn/fn-nb.md                 <- create demo notebook inside a task folder
  fn/fn-help.md               <- intent routing: natural-language -> subskill + step suggestion
