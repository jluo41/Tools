---
name: haipipe-project
description: "Standardize new project creation, review, and summary in the haipipe workspace. Use when the user wants to create a new project under examples/, review an existing project's structure, check script-result alignment, or generate a post-development summary. Also use when the user mentions /haipipe-project, project scaffold, new experiment, project review, or project summary."
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

  /haipipe-project new              -> scaffold a new project (both tracks)
  /haipipe-project review           -> gap analysis + generate docs: auto-detect current project
  /haipipe-project review [path]    -> gap analysis + generate docs for the project at [path]
  /haipipe-project summarize        -> post-development summary + flow chart (auto-detect)
  /haipipe-project summarize [path] -> summary for the project at [path]

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
  (no arg)                 (none)                                            (show menu below)

---

Step-by-Step Protocol
----------------------

Step 0: Parse the command.

  Extract the subcommand from args after "/haipipe-project":
    "new"              -> fn-new mode
    "review"           -> fn-review mode (path optional)
    "summarize"        -> fn-summarize mode (path optional)
    (no arg or help)   -> print the command menu and ask what user wants

  If no arg, print:

    haipipe-project commands:
      new                -> create a new project (both tracks)
      review [path]      -> check an existing project for structural gaps
      summarize [path]   -> generate post-development summary + flow chart

    Which would you like to do?

Step 1: Read ref files FIRST.

  For new / review:
    Read BOTH ref files before proceeding:
      Tools/plugins/research/skills/haipipe-project/ref/project-structure.md
      Tools/plugins/research/skills/haipipe-project/ref/code-structure.md

  For summarize:
    Read ref/project-structure.md only.

  This is MANDATORY. Do not proceed to Step 2 until all required ref files
  are in context. They contain the naming convention, four-part layout,
  light/heavy boundary, INDEX.md format, and Track A conventions.

  Confirm by stating:
    "Loaded: [ref files]. Executing: [subcommand]."

Step 2: Read the function file.

    new        ->  fn/fn-new.md
    review     ->  fn/fn-review.md
    summarize  ->  fn/fn-summarize.md

  Follow the steps in the fn file exactly.

---

Key Conventions (quick reference)
-----------------------------------

Project naming:   Proj{Series}-{Category}-{Num}-{Name}
  e.g.            ProjC-Model-2-GlucoseTransformer

Five-part layout (Track B):
  cc-archive/     CC session history (cc_*.md, di_*.md)
  config/         YAML configs named {N}_{stage}_{dataset}.yaml
  scripts/        Flat executables + INDEX.md (named {seq}_{YYMMDD}_{desc}.{ext})
  results/        Light summaries only; mirrors script names
  docs/           Planning + summary docs (TODO.md, project-summary.md)

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

Script-result pairing:
  scripts/001_260310_train_baseline.py  <->  results/001_260310_train_baseline/

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
