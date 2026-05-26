Skill: paper-rebuttal
=====================

Guide authors through the full rebuttal process for ML conference and journal
paper reviews. Four phases from reading reviews to revising the paper, designed
for multi-author collaboration.

Use this skill when the user has received peer reviews and needs to write
rebuttal responses, plan experiments to address reviewer concerns, or prepare
a revised manuscript. Also use when the user mentions rebuttal, reviewer
response, author response, review feedback, or camera-ready revision.

---

Four-Phase Pipeline
--------------------

  Phase A: Understand   <- Read reviews, annotate every concern
  Phase B: Task         <- Map concerns to rebuttal points → tasks
  Phase C: Rebuttal     <- Plan strategy + write the rebuttal responses
  Phase D: Revise       <- Generate revision checklist → hand off to /paper-revise

  Each phase produces artifacts in the review directory:

    1-review/
    +-- A-review-content/     <- Annotated reviews (one per reviewer)
    +-- B-rebuttal-task/      <- Point → task mapping, experiment plan
    +-- C-rebuttal-writing/   <- Strategy + rebuttal responses + supplementary
    +-- D-paper-revision/     <- Revision checklist (→ /paper-revise)

---

Commands
--------

  /paper-rebuttal understand [review-file]   -> read + annotate one reviewer
  /paper-rebuttal task [review-dir]          -> map points → tasks
  /paper-rebuttal rebuttal [reviewer-id]     -> plan + write one rebuttal response
  /paper-rebuttal revise [review-dir]        -> revision checklist → /paper-revise
  /paper-rebuttal audit [review-dir]         -> coverage + chars + consistency
  /paper-rebuttal supplementary [dir]        -> anonymous GitHub repo + README

  Default (no arg): show this command list.

  Typical workflow:
    1. understand    (repeat for each reviewer — this is the foundation)
    2. task          (after all reviews are annotated)
    3. rebuttal      (repeat for each reviewer)
    4. audit         (check all responses together)
    5. revise        (generate checklist, hand off to /paper-revise)

---

Annotation Convention
----------------------

  Reviews are annotated inline by coauthors and Claude Code (CC).
  Each annotation uses blockquote format with initials:

    > {INITIALS}: {comment}

  Examples:
    > {AU1}: We should admit this limitation honestly.
    > {AU2}: Agree. Also cite the ADA 2024 guidelines here.
    > CC: Task {task_id} addresses this. Results: {key findings}.

  Rules:
    - Each coauthor uses their own initials (2-3 letters, free-form)
    - CC is reserved for Claude Code responses
    - Annotations go directly below the reviewer text they respond to
    - Multiple coauthors can annotate the same paragraph
    - Language is free-form (English, Chinese, mixed — whatever is natural)

---

Execution Protocol
------------------

Step 0: Parse the subcommand from args.

Step 1: Read ref files FIRST (mandatory before proceeding).
  understand:       ref/concepts.md
  task:             ref/concepts.md + ref/formats.md
  rebuttal/audit:   ref/principles.md + ref/formats.md
  revise:           ref/principles.md

  Confirm: "Loaded: [ref files]. Executing: [subcommand]."

Step 2: Read and follow the function file exactly.
  understand     ->  fn/fn-understand.md
  task           ->  fn/fn-task.md
  rebuttal       ->  fn/fn-rebuttal.md
  revise         ->  fn/fn-revise.md
  audit          ->  fn/fn-audit.md
  supplementary  ->  fn/fn-supplementary.md

---

Review Directory Structure
---------------------------

  The skill produces artifacts in a 4-folder structure inside the
  paper's review directory (e.g., paper/1-review/):

    1-review/
    +-- README.md                       <- Overview + status
    +-- HANDOFF.md                      <- Continuation prompt for new sessions
    +-- A-review-content/               <- Annotated reviews (one per reviewer)
    |   +-- README.md                   <- Scores + master mapping table
    |   +-- review-raw.md               <- Original reviews (raw from venue)
    |   +-- review-{reviewer_id}.md     <- Review + annotations + paper source refs
    +-- B-rebuttal-task/                <- Point → task mapping
    |   +-- README.md                   <- Point → task table + status
    |   +-- experiment-plan.md          <- Execution order, feasibility, deps
    +-- C-rebuttal-writing/             <- Strategy + final responses
    |   +-- 0-rebuttal-strategy.md      <- Reviewer goals, char budgets, table allocation
    |   +-- rebuttal-{reviewer_id}.md   <- Annotated version (with > comments)
    |   +-- rebuttal-{reviewer_id}-clean.md  <- Clean version (ready to paste)
    |   +-- supplementary/              <- Anonymous supplementary tables
    +-- D-paper-revision/               <- LaTeX changes
    |   +-- revision-checklist.md       <- All changes with file:line references
    +-- _archive/                       <- Old files from before reorganization

---

File Map
--------

  SKILL.md                    <- you are here (router)
  ref/concepts.md             <- 5 key concepts for understanding reviews
  ref/principles.md           <- 10 rebuttal writing principles
  ref/formats.md              <- venue formats (ICML/NeurIPS/ICLR/journal)
  fn/fn-understand.md         <- Phase A: read + annotate one reviewer
  fn/fn-task.md               <- Phase B: points → tasks
  fn/fn-rebuttal.md           <- Phase C: plan strategy + write one response
  fn/fn-revise.md             <- Phase D: revision checklist → /paper-revise
  fn/fn-audit.md              <- coverage + chars + consistency check
  fn/fn-supplementary.md      <- anonymous GitHub repo setup
