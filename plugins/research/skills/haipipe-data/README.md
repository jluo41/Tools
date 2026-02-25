haipipe-data -- Unified Data Pipeline Skill
============================================

Covers all 4 data pipeline stages in one skill.
Functions: dashboard, load, cook, design-chef, design-kitchen, explain, review.

---

Commands
--------

  /haipipe-data                          <- dashboard (default): _WorkSpace status
  /haipipe-data dashboard                <- status at all 4 stages
  /haipipe-data load [stage]             <- inspect existing Set asset
  /haipipe-data cook [stage]             <- run Pipeline with config
  /haipipe-data design-chef [stage]      <- create new Fn via builder
  /haipipe-data design-kitchen [stage]   <- modify Pipeline infrastructure
  /haipipe-data explain [concept]        <- explain a concept (asks if no arg given)
  /haipipe-data review [file_path]       <- structural code review (asks for path if not given)
  /haipipe-data 0-overview               <- architecture + pipeline map
  /haipipe-data 1-source                 <- source layer reference
  /haipipe-data 2-record                 <- record layer reference
  /haipipe-data 3-case                   <- case layer reference
  /haipipe-data 4-aidata                 <- aidata layer reference

---

Stages
------

  1-source    Raw files -> SourceSet
              Kitchen: Source_Pipeline  |  Chef: SourceFn
              Store:   _WorkSpace/1-SourceStore/

  2-record    SourceSet -> RecordSet
              Kitchen: Record_Pipeline  |  Chef: HumanFn + RecordFn
              Store:   _WorkSpace/2-RecStore/

  3-case      RecordSet -> CaseSet (event-triggered feature extraction)
              Kitchen: Case_Pipeline    |  Chef: TriggerFn + CaseFn
              Store:   _WorkSpace/3-CaseStore/

  4-aidata    CaseSet -> AIDataSet (train/val/test splits)
              Kitchen: AIData_Pipeline  |  Chef: TfmFn + SplitFn
              Store:   _WorkSpace/4-AIDataStore/

---

File Map
--------

  SKILL.md                  <- router + dispatch table
  README.md                 <- this file
  ref/0-overview.md         <- architecture map + cooking metaphor
  ref/1-source.md           <- source layer reference
  ref/2-record.md           <- record layer reference
  ref/3-case.md             <- case layer reference
  ref/4-aidata.md           <- aidata layer reference
  fn/fn-0-dashboard.md      <- dashboard function
  fn/fn-1-load.md           <- load function (all stages)
  fn/fn-2-cook.md           <- cook function (all stages)
  fn/fn-3-design-chef.md    <- design-chef function (all stages)
  fn/fn-4-design-kitchen.md <- design-kitchen function (all stages)
  fn/fn-explain.md          <- explain function (25-concept pool, ask-then-explain)
  fn/fn-review.md           <- review function (detect type, apply checklist, PASS/WARN/FAIL)
  templates/1-source/       <- config.yaml template for 1-source cook
  templates/2-record/       <- config.yaml template for 2-record cook
  templates/3-case/         <- config.yaml template for 3-case cook
  templates/4-aidata/       <- config.yaml template for 4-aidata cook

---

Use Cases
---------

**1. Morning status check -- what data is ready?**

  Situation:  You sit down to work and want to know which pipeline stages have
              cached assets and which are missing.
  Command:    /haipipe-data
  What it does: Scans all 4 _WorkSpace store directories, lists available
                assets, versions, and row counts at a glance.

**2. Debug a missing or empty asset**

  Situation:  Training failed because the AIDataSet is empty or a CaseSet
              has fewer rows than expected.
  Command:    /haipipe-data load 3-case   (or 4-aidata)
  What it does: Loads the Set, prints shape, split sizes, feature columns,
                and flags any obvious issues (zero rows, missing splits, etc.)

**3. Run a pipeline stage with a config**

  Situation:  You have a YAML config and want to execute one stage
              (e.g., regenerate the CaseSet after fixing a CaseFn).
  Command:    /haipipe-data cook 3-case
  What it does: Walks through environment setup, config validation,
                pipeline.run() call, and output verification.

**4. Onboard a new raw dataset (new cohort)**

  Situation:  A new CSV/XML data dump has arrived and you need to build
              a SourceFn so the pipeline can ingest it.
  Command:    /haipipe-data design-chef 1-source
  What it does: Guides you through creating and running the builder script
                in code-dev/1-PIPELINE/1-Source-WorkSpace/ that generates
                the SourceFn in code/haifn/fn_source/.

**5. Add a new patient record type (new sensor / new data stream)**

  Situation:  A new data stream (e.g., CGM from a new device, a new lab table)
              needs to be wired into the RecordSet.
  Command:    /haipipe-data design-chef 2-record
  What it does: Helps decide whether to build a HumanFn or RecordFn, then
                guides through the 9-step processing skeleton, schema
                consistency rules, and builder execution.

**6. Engineer a new feature for model training**

  Situation:  You want to add a new time-window feature (e.g., CGM variance
              in the 2h before a trigger) to the CaseSet.
  Command:    /haipipe-data design-chef 3-case
  What it does: Guides CaseFn construction -- ROName setup, Ckpd window
                config, fn_CaseFn signature, suffix-only return keys,
                MetaDict, and builder execution.

**7. Build a new ML-ready transform for a new model architecture**

  Situation:  A new model needs a different input format (e.g., a tensor
              sequence instead of flat tabular features).
  Command:    /haipipe-data design-chef 4-aidata
  What it does: Guides InputTfmFn / OutputTfmFn / SplitFn construction
                with correct signatures, vocab building, and config wiring.

**8. Inspect a Set before using it in model training**

  Situation:  You're about to hand an AIDataSet to a model trainer and want
              to verify splits, vocab size, feature columns, and row counts.
  Command:    /haipipe-data load 4-aidata
  What it does: Loads AIDataSet, prints DatasetDict splits, feat_vocab,
                cf_to_cfvocab, and flags structural issues.

**9. Understand a pipeline concept or API**

  Situation:  You forgot how SplitFn works, or what ROName means, or how
              the train/val/test split labeling works.
  Command:    /haipipe-data explain ROName
              /haipipe-data explain SplitFn
              /haipipe-data explain            (shows concept menu)
  What it does: Draws on all 4 stage refs to explain the concept accurately
                with code examples.

**10. Review a file before committing**

  Situation:  You've written a new CaseFn or RecordFn builder and want to
              check it for structural issues before running it.
  Command:    /haipipe-data review code/haifn/fn_case/case_casefn/MyFn.py
              /haipipe-data review code-dev/1-PIPELINE/3-Case-WorkSpace/c5_build_casefn_myfeature.py
              /haipipe-data review config/caseset/pipeline/my_caseset.yaml
  What it does: Auto-detects the file type, applies the matching checklist
                (70+ criteria across all Fn types), and reports
                PASS / WARN / FAIL per criterion with a score.

**11. Review a YAML config for correctness**

  Situation:  A pipeline run failed with a cryptic error. You suspect the
              YAML config has a wrong key name or missing required section.
  Command:    /haipipe-data review config/aidata/my_aidata.yaml
  What it does: Checks SplitArgs structure, InputArgs/OutputArgs keys,
                method names, casefn_list entries, and split_ai values.

**12. Modify pipeline infrastructure**

  Situation:  You need to change how the pipeline caches data, add a new
              pipeline mode, or fix a bug in the base Pipeline class.
  Command:    /haipipe-data design-kitchen 3-case
  What it does: Identifies the correct file to edit in code/haipipe/,
                explains the impact on downstream stages, and guides the
                change safely (no builder regeneration needed).

**13. Re-run a specific stage after a bug fix**

  Situation:  You fixed a bug in a CaseFn builder and re-generated it.
              Now you need to re-run the Case pipeline to refresh the CaseSet.
  Command:    /haipipe-data cook 3-case
  What it does: Walks through cache invalidation (use_cache=False), config
                validation, run call, and output row count verification.

**14. Explore the full pipeline architecture**

  Situation:  You are new to the codebase and want to understand how all
              4 stages connect, what the cooking metaphor means, and how
              _WorkSpace is organized.
  Command:    /haipipe-data 0-overview
              /haipipe-data explain
  What it does: Loads the architecture map, cooking metaphor, _WorkSpace
                layout, and design principles. Explain mode then lets you
                drill into any specific concept.

**15. Validate a new cohort end-to-end**

  Situation:  You have added a new cohort (e.g., OhioT1DM) and want to
              walk through all 4 stages to confirm the data flows correctly
              from raw files to AIDataSet.
  Command:    /haipipe-data cook 1-source  (then 2-record, 3-case, 4-aidata)
              /haipipe-data load 4-aidata  (final verification)
  What it does: Runs each stage sequentially, checking output at each step
                before proceeding to the next.

---

Key Files (codebase)
--------------------

  Source_Pipeline:    code/haipipe/source_base/source_pipeline.py
  Record_Pipeline:    code/haipipe/record_base/record_pipeline.py
  Case_Pipeline:      code/haipipe/case_base/case_pipeline.py
  AIData_Pipeline:    code/haipipe/aidata_base/aidata_pipeline.py
  Asset base:         code/haipipe/assets.py
  Generated Fns:      code/haifn/        (NEVER edit directly)
  Builder scripts:    code-dev/1-PIPELINE/

  Always activate .venv first: source .venv/bin/activate && source env.sh
