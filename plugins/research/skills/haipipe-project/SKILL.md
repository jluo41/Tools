---
name: haipipe-project
description: "Standardize new project creation, review, summary, organization, and routing in the haipipe workspace. Use when the user wants to create a new project under examples/, review an existing project's structure, check script-result alignment, generate a post-development summary, reorganize project files, verify imports after file moves, or ask what subskill to use. Also use when the user mentions /haipipe-project, project scaffold, new experiment, project review, project summary, organize project, reorganize files, or what should I do next."
---

Skill: haipipe-project
=======================

Covers project-level structure across TWO tracks simultaneously:

  Track B  ->  examples/{PROJECT_ID}/    experiment configs, scripts, results
  Track A  ->  code-dev/ + code/hainn/   pipeline Fn builders, ML model stubs

The user never needs to specify which track. Both are handled automatically.

Two structural rules that govern all projects:

  Rule 1 — Flat scripts with INDEX.md:
    scripts/ stays flat (no subfolders except sbatch/).
    scripts/INDEX.md is MANDATORY — indexes every script by data, functionality,
    and pipeline stage so Claude can scan for reuse before creating new scripts.

  Rule 2 — Code always has a paired example:
    Every new pipeline Fn stub or ML model stub created in Track A
    AUTOMATICALLY generates a paired example script in scripts/.
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
  /haipipe-project nb                     -> create a demo notebook for a pipeline stage segment (auto-detect)
  /haipipe-project nb [path]             -> create a demo notebook for the project at [path]
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
  help [question]          (none — intent routing only)                      fn/fn-help.md
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
      nb [path]                 -> create a demo notebook for a pipeline stage segment
      help [question]           -> describe what you want in plain English; I'll route you

    Typical sequence for an existing project:
      1. organize [path]   <- move files into standard layout
      2. review [path]     <- generate docs (data-map, TODO, dependency-report, INDEX.md)

    Which would you like to do?

Step 1: Read ref files FIRST.

  For new / review:
    Read BOTH ref files before proceeding:
      Tools/plugins/research/skills/haipipe-project/ref/project-structure.md
      Tools/plugins/research/skills/haipipe-project/ref/code-structure.md

  For summarize / organize / nb:
    Read ref/project-structure.md only.

  For help:
    Read NO ref files — intent routing only, no project files needed.

  This is MANDATORY. Do not proceed to Step 2 until all required ref files
  are in context. They contain the naming convention, four-part layout,
  light/heavy boundary, INDEX.md format, and Track A conventions.

  Confirm by stating:
    "Loaded: [ref files]. Executing: [subcommand]."

Step 2: Read the function file.

    new        ->  fn/fn-new.md
    review     ->  fn/fn-review.md
    summarize  ->  fn/fn-summarize.md
    organize   ->  fn/fn-organize.md
    nb         ->  fn/fn-nb.md
    help       ->  fn/fn-help.md  (no ref files needed — intent routing only)

  Follow the steps in the fn file exactly.

---

Checkpoint Hints (pre-written — print verbatim, no extra analysis)
--------------------------------------------------------------------

  CH-1  docs/ files updated?
        "Quick check: open docs/ and confirm all generated files look correct
         (TODO.md, data-map.md, dependency-report.md). Did anything come out empty?"

  CH-2  scripts/INDEX.md in sync?
        "Quick check: does scripts/INDEX.md have an entry for every .py/.sh in
         scripts/? Are all status values (stub / wip / done) current?"

  CH-3  file paths valid?
        "Quick check: any scripts that reference config/, results/, or docs/ paths —
         confirm those paths still exist relative to the project root."

  CH-4  code/INDEX.md updated?
        "Quick check: if new Track A stubs were created, confirm code/INDEX.md has
         stub-status rows for them (so future projects can find them for reuse)."

  CH-5  YAML placeholders filled?
        "Quick check: search config/ for any remaining TODO_ values — all placeholder
         class names must be replaced before running the pipeline."

  CH-6  reorganization pending verification?
        "Reminder: if you moved or renamed files manually, run
         /haipipe-project organize verify to confirm imports and paths still work."

Each fn file lists which hints to print at the end of its execution chain.

---

Key Conventions (quick reference)
-----------------------------------

Project naming:   Proj{Series}-{Category}-{Num}-{Name}
  e.g.            ProjC-Model-2-GlucoseTransformer

Four-part layout (Track B):
  cc-archive/     CC session history (cc_*.md, di_*.md)
  config/         YAML configs named {N}_{stage}_{dataset}.yaml
  scripts/        Task-folder layout: scripts/{task}/ contains {task}.py + runs/ + results/
                  scripts/INDEX.md = global task list; {task}/INDEX.md = run inventory
                  scripts/sbatch/ = cross-task SLURM scripts only
  docs/           Planning + summary docs (TODO.md, project-summary.md)

  Note: no top-level results/ folder. Results live inside each task folder.

code/INDEX.md (codebase-wide, shared across all projects):
  Indexes ALL implemented Fns (code/haifn/) and ML models (code/hainn/).
  Claude reads this BEFORE creating any new Fn or model — reuse across projects first.
  Updated by fn-new.md (stub entries) and by haipipe-data/haipipe-nn (done entries).
  Format: two tables — Pipeline Functions | ML Models

scripts/INDEX.md (per-project):
  Required in every project. Indexes scripts by data, functionality, stage.
  Claude reads this BEFORE creating any new script — to check for reuse first.
  Format: table with columns: Script | Data | Functionality | Stage | Status

Auto-example rule:
  Every Track A stub (new Fn or model) generates a paired example script.
  Script name: {seq}_{YYMMDD}_example_{fn_or_model_name}.py

Run-result pairing (within each task folder):
  scripts/train_num/runs/phase1_gpu0.sh  <->  scripts/train_num/results/phase1_gpu0/

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
  ref/project-structure.md    <- Track B standard layout, naming, INDEX.md, rules
  ref/code-structure.md       <- Track A code-dev/ + hainn/ conventions
  fn/fn-new.md                <- scaffold new project (interactive, both tracks)
  fn/fn-review.md             <- gap analysis + proposed actions (both tracks)
  fn/fn-summarize.md          <- post-development summary + flow chart
  fn/fn-organize.md           <- file inventory + reorganization proposal + verification
  fn/fn-nb.md                 <- guided demo notebook creation + nb/INDEX.md management
  fn/fn-help.md               <- intent routing: natural-language -> subskill + step suggestion
