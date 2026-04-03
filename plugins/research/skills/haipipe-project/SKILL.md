---
name: haipipe-project
description: "Standardize project creation, review, summary, and organization in the haipipe workspace. Use when the user wants to create a new project under examples/, review structure, generate docs, summarize, reorganize files, or verify imports. Also use when the user mentions /haipipe-project, project scaffold, new experiment, project review, project summary, organize project, or reorganize files."
---

Skill: haipipe-project
=======================

Covers project-level structure across TWO tracks simultaneously:

  Track B  ->  examples/{PROJECT_ID}/    tasks, configs, runs, results, paper
  Track A  ->  code-dev/ + code/hainn/ + code/haifn/  pipeline Fn builders, ML model stubs

Two structural rules govern all projects:

  Rule 1 -- Two-level task hierarchy:
    tasks/ contains group folders: {G}_{group_name}/ (e.g., A_data/, B_training/).
    Each group contains task folders: {G}{N}_{name}/ (e.g., B1_train_stats/).
    Each task is self-contained: *.py, config/, runs/, results/, README.md.
    No flat task folders directly in tasks/ -- they must be inside a group.

  Rule 2 -- Code always has a paired example:
    Every new pipeline Fn stub or ML model stub in Track A
    auto-generates a paired example task in tasks/.

---

Commands
--------

  /haipipe-project new [project|group|task] -> scaffold project, group, or task
  /haipipe-project review [path]          -> gap analysis + generate docs
  /haipipe-project summarize [path]       -> post-development summary + flow chart
  /haipipe-project organize [path]        -> file inventory + reorganization proposal
  /haipipe-project organize verify [path] -> verify imports/paths after reorganization

  Default (no arg): show this command list and ask what the user wants.

  Typical sequence for an existing project:
    1. organize   <- move files into standard layout
    2. review     <- generate docs + check code sync

---

Execution Protocol
------------------

Step 0: Parse the subcommand from args.

Step 1: Read ref files FIRST (mandatory before proceeding).
  new / review:         ref/project-structure.md + ref/code-structure.md
  summarize / organize: ref/project-structure.md only
  Confirm: "Loaded: [ref files]. Executing: [subcommand]."

Step 2: Read and follow the function file exactly.
  new        ->  fn/fn-new.md
  review     ->  fn/fn-review.md
  summarize  ->  fn/fn-summarize.md
  organize   ->  fn/fn-organize.md

---

File Map
--------

  SKILL.md                    <- you are here (router)
  ref/project-structure.md    <- Track B: layout, naming, group-folder, task-folder
  ref/code-structure.md       <- Track A: code-dev/ + hainn/ conventions
  fn/fn-new.md                <- scaffold new project (interactive, both tracks)
  fn/fn-review.md             <- gap analysis + doc generation (both tracks)
  fn/fn-summarize.md          <- post-development summary + flow chart
  fn/fn-organize.md           <- file inventory + reorganization + verification
