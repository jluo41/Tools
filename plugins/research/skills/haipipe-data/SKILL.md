---
name: haipipe-data
description: "Unified skill for all haipipe data pipeline work across 4 stages (Source, Record, Case, AIData). Use when the user asks about pipeline stages 1-4, data loading, running pipelines, building SourceFn/HumanFn/RecordFn/TriggerFn/CaseFn/TfmFn/SplitFn, inspecting _WorkSpace assets, or reviewing/auditing a pipeline file for correctness. Also use when the user mentions cook, load, design-chef, design-kitchen, review, haistep-source/record/case/aidata, or /haipipe-data."
---

Skill: haipipe-data
===================

Two-axis skill covering all 4 data pipeline stages.

  Function axis:  dashboard | load | cook | design-chef | design-kitchen | explain | review
  Stage axis:     0-overview | 1-source | 2-record | 3-case | 4-aidata  (optional)

Default (no arg): dashboard mode.

---

Commands
--------

  /haipipe-data                              -> dashboard: _WorkSpace status at all stages
  /haipipe-data dashboard                    -> same as above
  /haipipe-data dashboard [1-source etc.]    -> dashboard filtered to one stage only
  /haipipe-data dashboard 0-rawdata          -> raw data store files (no manifest check)
  /haipipe-data dashboard rawdata            -> alias for 0-rawdata
  /haipipe-data load [1-source etc.]         -> load and inspect existing Set
  /haipipe-data cook [1-source etc.]         -> run Pipeline with config
  /haipipe-data design-chef [1-source etc.]  -> create new Fn via builder
  /haipipe-data design-kitchen [stage]       -> modify Pipeline infrastructure
  /haipipe-data explain [concept or question] -> explain a concept (ask if no arg)
  /haipipe-data review [file_path]           -> structural code review (ask if no path given)
  /haipipe-data 0-overview                   -> architecture + design principles (ref only)
  /haipipe-data 1-source                     -> source layer reference only
  /haipipe-data 2-record                     -> record layer reference only
  /haipipe-data 3-case                       -> case layer reference only
  /haipipe-data 4-aidata                     -> aidata layer reference only

---

Dispatch Table
--------------

After parsing the command, read these files from
Tools/plugins/research/skills/haipipe-data/:

  Invocation                    Ref file(s)                                Function file
  ----------------------------  -----------------------------------------  ----------------------
  (no arg) / dashboard          ref/0-overview.md                          fn/fn-0-dashboard.md
  dashboard 0-rawdata           ref/0-overview.md                          fn/fn-0-dashboard.md
  dashboard rawdata             ref/0-overview.md                          fn/fn-0-dashboard.md
  dashboard 1-source            ref/1-source.md                            fn/fn-0-dashboard.md
  dashboard 2-record            ref/2-record.md                            fn/fn-0-dashboard.md
  dashboard 3-case              ref/3-case.md                              fn/fn-0-dashboard.md
  dashboard 4-aidata            ref/4-aidata.md                            fn/fn-0-dashboard.md
  load (no stage)               ref/0-overview.md                          fn/fn-1-load.md
  load 1-source                 ref/1-source.md                            fn/fn-1-load.md
  load 2-record                 ref/2-record.md                            fn/fn-1-load.md
  load 3-case                   ref/3-case.md                              fn/fn-1-load.md
  load 4-aidata                 ref/4-aidata.md                            fn/fn-1-load.md
  cook (no stage)               ref/0-overview.md                          fn/fn-2-cook.md
  cook 1-source                 ref/1-source.md                            fn/fn-2-cook.md
  cook 2-record                 ref/2-record.md                            fn/fn-2-cook.md
  cook 3-case                   ref/3-case.md                              fn/fn-2-cook.md
  cook 4-aidata                 ref/4-aidata.md                            fn/fn-2-cook.md
  design-chef (no stage)        ref/0-overview.md + ALL stage-*.md         fn/fn-3-design-chef.md
  design-chef 1-source          ref/1-source.md + ref/2-record.md*         fn/fn-3-design-chef.md
  design-chef 2-record          ref/2-record.md + ref/3-case.md*           fn/fn-3-design-chef.md
  design-chef 3-case            ref/3-case.md + ref/4-aidata.md*           fn/fn-3-design-chef.md
  design-chef 4-aidata          ref/4-aidata.md                            fn/fn-3-design-chef.md
  design-kitchen (no stage)     ref/0-overview.md                          fn/fn-4-design-kitchen.md
  design-kitchen 1-source       ref/1-source.md                            fn/fn-4-design-kitchen.md
  design-kitchen 2-record       ref/2-record.md                            fn/fn-4-design-kitchen.md
  design-kitchen 3-case         ref/3-case.md                              fn/fn-4-design-kitchen.md
  design-kitchen 4-aidata       ref/4-aidata.md                            fn/fn-4-design-kitchen.md
  explain (no arg)              ref/0-overview.md + ALL stage-*.md         fn/fn-explain.md
  explain <concept/question>    ref/0-overview.md + ALL stage-*.md         fn/fn-explain.md
  review (no path)              ref/0-overview.md                          fn/fn-review.md
  review <file_path>            ref/<detected-stage>.md (or 0-overview.md) fn/fn-review.md
  0-overview                    ref/0-overview.md                          (none)
  1-source                      ref/1-source.md                            (none)
  2-record                      ref/2-record.md                            (none)
  3-case                        ref/3-case.md                              (none)
  4-aidata                      ref/4-aidata.md                            (none)

NOTE: design-chef for stage N also loads stage N+1 ref (*).
      A new Fn at stage N must satisfy the contract of stage N+1.
      Example: design-chef 1-source loads ref/2-record.md so you know
      exactly which schema the RecordFn downstream expects.

NOTE: "ALL stage-*.md" when no stage given means load all four:
      ref/1-source.md, ref/2-record.md, ref/3-case.md, ref/4-aidata.md

---

Step-by-Step Protocol
----------------------

Step 0: Bootstrap -- read supporting file NOW.
        Before parsing the command or doing anything else, read:

          Tools/plugins/research/skills/haipipe-data/ref/0-overview.md

        This is MANDATORY. Do not skip. Do not proceed to Step 1 until
        0-overview.md is in context. It contains the 6-layer pipeline map,
        cooking metaphor, _WorkSpace layout, and design principles.

Step 1: Parse the args after "/haipipe-data".
        Extract:
          function  in { dashboard, load, cook, design-chef, design-kitchen, explain, review, (none) }
          stage     in { 0-overview, 1-source, 2-record, 3-case, 4-aidata, (none) }
        If no args -> dashboard mode.
        If only stage arg -> ref-only mode (load ref file, no fn file).

        Normalize stage aliases before lookup:
          rawdata  -> 0-rawdata
          source   -> 1-source
          record   -> 2-record
          case     -> 3-case
          aidata   -> 4-aidata

Step 2: Read the ref file AND the function file from the dispatch table.
        Both files MUST be read before executing. Do not proceed from memory.

        Confirm by stating:
          "Loaded: [ref file(s)] + [fn file]. Executing: [function] [stage]."

Step 3: Execute the function.
        Follow the steps in the fn/* file exactly.
        Apply MUST DO and MUST NOT checklists from the ref file line by line,
        not from memory.

---

Always-On Context
-----------------

When design-chef is invoked WITHOUT a stage qualifier, load ref/0-overview.md
PLUS all four stage ref files. This ensures you understand the full pipeline
contract before designing any Fn.

When design-chef is invoked WITH a stage qualifier, also load the NEXT stage
ref (see dispatch table *). A Fn designed for stage N must produce output
compatible with stage N+1 -- you need to know that contract.

When load, cook, or design-kitchen is invoked WITHOUT a stage qualifier,
ref/0-overview.md is sufficient to orient, then the fn file provides
stage-specific guidance inline.

When explain is invoked (with or without a concept), load ref/0-overview.md
PLUS all four stage-*.md files. The explain function may need to draw on any
stage's ref to answer accurately. The fn-explain.md file handles both modes:
  - With concept/question: map to concept pool, explain directly
  - Without arg: show the menu and wait for user selection before explaining

When review is invoked WITH a file path, detect the Fn type from the path
pattern (see fn/fn-review.md type detection table) and load the matching
stage ref (e.g., if path is under fn_case/ load ref/3-case.md; if under
fn_source/ load ref/1-source.md). If type spans multiple stages or is a
YAML config, load ref/0-overview.md plus the relevant stage ref.
When review is invoked WITHOUT a path, load ref/0-overview.md only;
fn-review.md will show a discovery menu and ask the user to provide the path.

---

File Map
--------

  SKILL.md                    <- you are here (router + dispatch table)
  README.md                   <- quick command cheat sheet
  ref/0-overview.md           <- architecture, design principles, workspace map, cooking metaphor
  ref/1-source.md             <- Layer 1: SourceSet, SourceFn, schemas, key files
  ref/2-record.md             <- Layer 2: RecordSet, HumanFn, RecordFn, temporal alignment
  ref/3-case.md               <- Layer 3: CaseSet, TriggerFn, CaseFn, feature naming
  ref/4-aidata.md             <- Layer 4: AIDataSet, TfmFn, SplitFn, splits
  fn/fn-0-dashboard.md        <- dashboard: _WorkSpace status scan at each stage
  fn/fn-1-load.md             <- load: inspect existing Set asset (per-stage)
  fn/fn-2-cook.md             <- cook: run Pipeline with config (per-stage)
  fn/fn-3-design-chef.md      <- design-chef: create new Fn via builder (per-stage)
  fn/fn-4-design-kitchen.md   <- design-kitchen: modify Pipeline infrastructure
  fn/fn-explain.md            <- explain: concept education (ask-then-explain, 25-concept pool)
  fn/fn-review.md             <- review: structural code review (detect type, apply checklist, PASS/WARN/FAIL)
  templates/1-source/         <- config template for 1-source cook
  templates/2-record/         <- config template for 2-record cook
  templates/3-case/           <- config template for 3-case cook
  templates/4-aidata/         <- config template for 4-aidata cook
