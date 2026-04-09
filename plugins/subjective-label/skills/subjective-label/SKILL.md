---
name: subjective-label
description: "General-purpose subjective text annotation skill. Two phases: (1) generate a Gallery of labeled examples through human+AI interaction, (2) annotate at scale using a weak model + gallery. Use when the user wants to annotate texts based on their personal subjective criteria, build an annotation gallery, run inference with a gallery, or says /subjective-label."
---

Skill: subjective-label
========================

Two-phase annotation workflow for subjective labeling tasks.

  Phase 1  ->  Gallery Generation  (interactive, one-time)
  Phase 2  ->  Inference           (automated, scalable)
  Phase 3  ->  Evaluation          (validate gallery quality)

Invocation:  /subjective-label <command> [args]


Commands
--------

  /subjective-label gallery  <project_dir>   Phase 1: generate gallery interactively
  /subjective-label infer    <project_dir>   Phase 2: annotate with weak model
  /subjective-label eval     <project_dir>   Phase 3: evaluate gallery quality

  Default (no command): show this list and ask what the user wants.


Execution Protocol
------------------

Step 0: Parse command from $ARGUMENTS.

Step 1: Read ref files before proceeding.
  All commands:  ref/ref-assets.md + ref/ref-schema.md
  Confirm: "Loaded: [ref files]. Executing: [command]."

Step 2: Read and follow the function file exactly.
  gallery  ->  fn/fn-gallery.md
  infer    ->  fn/fn-infer.md
  eval     ->  fn/fn-eval.md

Step 3: Auto-detect project_dir if not provided.
  1. If arg provided: use it.
  2. If cwd contains sample/ or gallery/: use cwd.
  3. Otherwise: ask user for project_dir.


Project Directory Layout
------------------------

  {project_dir}/
    config.yaml           task description + label schema
    sample/               raw texts to annotate (Phase 1 input)
    gallery/
      gallery.json        labeled examples (core artifact)
      guideline.md        extracted annotation rules
    output/
      annotations.jsonl   inference results (Phase 2 output)
    eval/
      eval_set.jsonl      human-labeled held-out set
      eval_report.md      accuracy + failure analysis


Key Principle
-------------

  If weak model inference is wrong -> fix the GALLERY, not the model.
  The gallery is the single source of truth for annotation criteria.
  A well-built gallery makes any model capable.
