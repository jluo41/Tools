---
name: haipipe-end
description: "Unified skill for Stage 6 endpoint deployment: packaging ModelInstance_Set into Endpoint_Set, testing inference, designing the 5 inference function types (MetaFn/TrigFn/PostFn/Src2InputFn/Input2SrcFn), and deploying to Databricks or local. Use when the user mentions Endpoint_Set, Endpoint_Pipeline, inference functions, fn_endpoint, or deployment."
---

Skill: haipipe-end
===================

Two-axis skill covering the full endpoint deployment lifecycle.

  Function axis:  dashboard | package | test | design | deploy | review
  Fn-type axis:   meta | trig | post | src2input | input2src  (optional scope)

Default (no arg): dashboard mode.

---

Commands
--------

  /haipipe-end                              -> dashboard: 6-EndpointStore status
  /haipipe-end dashboard                   -> same as above
  /haipipe-end package                     -> run Endpoint_Pipeline (Stage 5 → Stage 6)
  /haipipe-end test [payload_path]         -> run inference() with profiling
  /haipipe-end design [fn-type]            -> build new inference Fn via builder
  /haipipe-end deploy [databricks|local]   -> deploy packaged Endpoint_Set
  /haipipe-end review [fn-type]            -> review generated Fn files
  /haipipe-end 0-overview                  -> architecture + inference pipeline + YAML
  /haipipe-end meta                        -> MetaFn reference
  /haipipe-end trig                        -> TrigFn reference
  /haipipe-end post                        -> PostFn reference
  /haipipe-end src2input                   -> Src2InputFn reference
  /haipipe-end input2src                   -> Input2SrcFn reference

---

Dispatch Table
--------------

After parsing the command, read these files from
Tools/plugins/research/skills/haipipe-end/:

  Invocation                Ref file(s)                           Function file
  ------------------------  ------------------------------------  --------------------
  (no arg) / dashboard      ref/0-overview.md                     fn/fn-0-dashboard.md
  package                   ref/0-overview.md                     fn/fn-1-package.md
  test                      ref/0-overview.md                     fn/fn-2-test.md
  design (no type)          ref/0-overview.md + ALL ref/1-5.md   fn/fn-3-design.md
  design meta               ref/1-meta.md                         fn/fn-3-design.md
  design trig               ref/2-trig.md                         fn/fn-3-design.md
  design post               ref/3-post.md                         fn/fn-3-design.md
  design src2input          ref/4-src2input.md                    fn/fn-3-design.md
  design input2src          ref/5-input2src.md                    fn/fn-3-design.md
  deploy                    ref/0-overview.md                     fn/fn-4-deploy.md
  review (no type)          ref/0-overview.md + ALL ref/1-5.md   fn/fn-review.md
  review meta               ref/1-meta.md                         fn/fn-review.md
  review trig               ref/2-trig.md                         fn/fn-review.md
  review post               ref/3-post.md                         fn/fn-review.md
  review src2input          ref/4-src2input.md                    fn/fn-review.md
  review input2src          ref/5-input2src.md                    fn/fn-review.md
  0-overview                ref/0-overview.md                     (none)
  meta                      ref/1-meta.md                         (none)
  trig                      ref/2-trig.md                         (none)
  post                      ref/3-post.md                         (none)
  src2input                 ref/4-src2input.md                    (none)
  input2src                 ref/5-input2src.md                    (none)

NOTE: "ALL ref/1-5.md" means load all five files:
  ref/1-meta.md, ref/2-trig.md, ref/3-post.md, ref/4-src2input.md, ref/5-input2src.md

---

Step-by-Step Protocol
----------------------

Step 0: Bootstrap — read supporting files NOW.
        Before parsing the command or doing anything else, read:

          Tools/plugins/research/skills/haipipe-end/ref/0-overview.md

        This is MANDATORY. Do not skip. Do not proceed to Step 1 until
        0-overview.md is in context. It contains the 7-step inference
        pipeline, directory layout, YAML config format, and payload/
        response schemas needed by all other steps.

Step 1: Parse the args after "/haipipe-end".
        Extract:
          function  in { dashboard, package, test, design, deploy, review, (none) }
          fn_type   in { meta, trig, post, src2input, input2src, (none) }
        If no args -> dashboard mode.
        If only fn_type arg -> ref-only mode (load ref file, no fn file).

Step 2: Read the ref file AND the function file from the dispatch table.
        Both files MUST be read before executing. Do not proceed from memory.

        Confirm by stating:
          "Loaded: [ref file] + [fn file]. Executing: [function] [fn_type]."

Step 3: Execute the function.
        Follow the steps in the fn/* file exactly.
        When a step says "apply checklist from ref/N-*.md", that means
        the checklist in the already-loaded ref file -- apply it line
        by line, not from memory.

---

Always-On Context
-----------------

When design or review is invoked WITHOUT a fn_type qualifier, load
ref/0-overview.md PLUS all five ref/1-5.md files. The fn files reference
per-type checklists; missing any ref file causes silent gaps.

When design or review is invoked WITH a fn_type qualifier, load only the
specific ref file. Check adjacent fn types when the Fn interacts closely
(e.g., Input2SrcFn and Src2InputFn are inverses -- reading both is useful).

---

File Map
--------

  SKILL.md              <- you are here (router + dispatch table)
  README.md             <- quick reference + use cases
  ref/0-overview.md     <- architecture, 7-step inference pipeline, directory
                           layout, YAML config, payload/response formats, SPACE keys
  ref/1-meta.md         <- MetaFn contract: model metadata, name mapping, response
  ref/2-trig.md         <- TrigFn contract: trigger detection, skip logic
  ref/3-post.md         <- PostFn contract: score → client JSON response
  ref/4-src2input.md    <- Src2InputFn: ProcDF → payload JSON (example generation)
  ref/5-input2src.md    <- Input2SrcFn: payload JSON → ProcDF (inference entry)
  fn/fn-0-dashboard.md  <- dashboard: 6-EndpointStore status scan
  fn/fn-1-package.md    <- package: Endpoint_Pipeline.run() protocol
  fn/fn-2-test.md       <- test: inference() + warmup() + profile= protocol
  fn/fn-3-design.md     <- design: builder pattern for all 5 Fn types
  fn/fn-4-deploy.md     <- deploy: Databricks Unity Catalog + Model Serving
  fn/fn-review.md       <- review: checklist per Fn type + cross-checks
