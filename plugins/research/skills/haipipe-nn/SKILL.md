---
name: haipipe-nn
description: "Unified skill for all haipipe-nn model pipeline work across 4 layers (Algorithm, Tuner, Instance, ModelSet/Pipeline). Use when the user asks about mlpredictor, tsforecast, tefm, tediffusion, or bandit models; when reviewing, generating, or testing any NN pipeline code; when checking model status; or when they say /haipipe-nn. Also use when the user mentions tuner, instance, model registry, ModelInstance, or ModelInstance_Set in the hainn codebase context."
---

Skill: haipipe-nn
=================

Two-axis skill covering all 4 layers of the haipipe-nn pipeline.

  Function axis:  dashboard | review | generate | test
  Layer axis:     L0 | L1 | L2 | L3 | L4  (optional scope qualifier)

Default (no arg): dashboard mode.

---

Commands
--------

  /haipipe-nn                   -> dashboard: codebase status table
  /haipipe-nn dashboard         -> same as above
  /haipipe-nn review [L1-L4]   -> 8-step deep model review; optional layer scope
  /haipipe-nn generate [L1-L4] -> code generation guide; optional layer scope
  /haipipe-nn test [L1-L4]     -> test design and run protocol; optional layer scope
  /haipipe-nn L0               -> architecture overview, registry, YAML templates
  /haipipe-nn L1               -> Layer 1 (Algorithm) reference only
  /haipipe-nn L2               -> Layer 2 (Tuner) reference only
  /haipipe-nn L3               -> Layer 3 (Instance) reference only
  /haipipe-nn L4               -> Layer 4 (ModelSet/Pipeline) reference only

---

Dispatch Table
--------------

After parsing the command, read these files from
Tools/plugins/research/skills/haipipe-nn/:

  Invocation               Ref file(s)                              Function file
  -----------------------  ───────────────────────────────────────  ---------------------
  (no arg) / dashboard     ref/overview.md                          fn/fn-dashboard.md
  review (no layer)        ref/overview.md + ALL layer-*.md         fn/fn-review.md
  review L1                ref/layer-1-algorithm.md                           fn/fn-review.md
  review L2                ref/layer-2-tuner.md                           fn/fn-review.md
  review L3                ref/layer-3-instance.md                           fn/fn-review.md
  review L4                ref/layer-4-modelset.md                           fn/fn-review.md
  generate (no layer)      ref/overview.md + ALL layer-*.md         fn/fn-generate.md
  generate L1              ref/layer-1-algorithm.md                           fn/fn-generate.md
  generate L2              ref/layer-2-tuner.md                           fn/fn-generate.md
  generate L3              ref/layer-3-instance.md                           fn/fn-generate.md
  generate L4              ref/layer-4-modelset.md                           fn/fn-generate.md
  test (no layer)          ref/overview.md                          fn/fn-test.md
  test L1                  ref/layer-1-algorithm.md                           fn/fn-test.md
  test L2                  ref/layer-2-tuner.md                           fn/fn-test.md
  test L3                  ref/layer-3-instance.md                           fn/fn-test.md
  test L4                  ref/layer-4-modelset.md                           fn/fn-test.md
  L0 / overview            ref/overview.md                          (none)
  L1                       ref/layer-1-algorithm.md                           (none)
  L2                       ref/layer-2-tuner.md                           (none)
  L3                       ref/layer-3-instance.md                           (none)
  L4                       ref/layer-4-modelset.md                           (none)

NOTE: "ALL layer-*.md" means load all four files:
  ref/layer-1-algorithm.md, ref/layer-2-tuner.md, ref/layer-3-instance.md, ref/layer-4-modelset.md
fn-review.md and fn-generate.md reference per-layer checklists in their steps.
Without all four files in context those steps will be incomplete.

---

Step-by-Step Protocol
----------------------

Step 0: Bootstrap — read supporting files NOW.
        Before parsing the command or doing anything else, read:

          Tools/plugins/research/skills/haipipe-nn/ref/overview.md

        This is MANDATORY. Do not skip. Do not proceed to Step 1 until
        overview.md is in context. It contains the architecture map,
        model registry, and YAML templates needed by all other steps.

Step 1: Parse the args after "/haipipe-nn".
        Extract:
          function  in { dashboard, review, generate, test, (none) }
          layer     in { L0, L1, L2, L3, L4, (none) }
        If no args -> dashboard mode.
        If only layer arg -> ref-only mode (load ref file, no fn file).

Step 2: Read the ref file AND the function file from the dispatch table.
        Both files MUST be read before executing. Do not proceed from memory.

        Confirm by stating:
          "Loaded: [ref file] + [fn file]. Executing: [function] [layer]."

Step 3: Execute the function.
        Follow the steps in the fn/* file exactly.
        When a step says "apply checklist from ref/layer-N.md", that means
        the checklist content in the already-loaded ref file — apply it
        line by line, not from memory.

---

Always-On Context
-----------------

When review or generate is invoked WITHOUT a layer qualifier, load
ref/overview.md PLUS all four layer-*.md files. These fn files reference
per-layer checklists in their steps; missing any layer file causes silent gaps.

When review or generate is invoked WITH a layer qualifier, load only the
specific layer ref. The per-step instructions for other layers will note
when the adjacent layer file would be useful.

When test is invoked WITHOUT a layer qualifier, ref/overview.md is sufficient
(fn-test.md is self-contained with layer-specific notes inline).

---

File Map
--------

  SKILL.md             <- you are here (router + dispatch table)
  README.md            <- quick command cheat sheet
  ref/overview.md      <- L0: architecture, registry, YAML templates, test conventions
  ref/layer-1-algorithm.md       <- L1: algorithm diversity and custom nn.Module rules
  ref/layer-2-tuner.md       <- L2: tuner contract (5 methods, transform_fn, save/load)
  ref/layer-3-instance.md       <- L3: instance contract (5 methods, registry, config)
  ref/layer-4-modelset.md       <- L4: modelset/pipeline, YAML, run versioning, lineage
  fn/fn-dashboard.md   <- dashboard: codebase status scan and table rendering
  fn/fn-review.md      <- review: 8-step deep model review with sign-off checklist
  fn/fn-generate.md    <- generate: step-by-step code generation for new models
  fn/fn-test.md        <- test: 7-step test protocol, running and debugging
