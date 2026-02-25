haipipe-nn -- Unified NN Pipeline Skill
========================================

Covers all 4 layers of the haipipe-nn pipeline in one skill.
Functions: dashboard, review, generate, test.

---

Commands
--------

  /haipipe-nn                  <- dashboard (default): live status table
  /haipipe-nn dashboard        <- status table for all models
  /haipipe-nn review [L2]      <- 8-step review, optional layer scope
  /haipipe-nn generate [L3]    <- code generation guide
  /haipipe-nn test [L2]        <- test protocol
  /haipipe-nn L0               <- architecture + registry + YAML templates
  /haipipe-nn L1               <- Algorithm reference
  /haipipe-nn L2               <- Tuner reference
  /haipipe-nn L3               <- Instance reference
  /haipipe-nn L4               <- ModelSet/Pipeline reference

---

Layers
------

  L1: Algorithm    Raw external library (XGBoost, Nixtla, etc.) or custom
                   nn.Module (algorithm_*.py). NEVER imported above Tuner.

  L2: Tuner        Wraps ONE algorithm. 5 abstract methods: get_tfm_data,
                   fit, infer, save_model, load_model. ONLY layer that
                   imports external algorithm libraries.

  L3: Instance     Thin orchestrator. Manages Tuner dict (model_base).
                   HuggingFace-style save_pretrained/from_pretrained.
                   5 abstract methods + MODEL_TYPE + Config dataclass.

  L4: ModelSet     Asset packaging. YAML-driven ModelInstance_Pipeline.
                   Run versioning (@run-v000X). Lineage tracking.

---

File Map
--------

  SKILL.md             <- router + dispatch table
  README.md            <- this file
  ref/overview.md      <- L0: architecture, registry, YAML, test conventions
  ref/layer-1-algorithm.md       <- L1: algorithm reference
  ref/layer-2-tuner.md       <- L2: tuner reference
  ref/layer-3-instance.md       <- L3: instance reference
  ref/layer-4-modelset.md       <- L4: modelset reference
  fn/fn-dashboard.md   <- dashboard function
  fn/fn-review.md      <- review function (8 steps + sign-off)
  fn/fn-generate.md    <- generate function (new model scaffolding)
  fn/fn-test.md        <- test function (7-step protocol + common failures)

---

Key Files (codebase)
--------------------

  ModelTuner base:         code/hainn/model_tuner.py
  ModelInstance base:      code/hainn/model_instance.py
  ModelInstanceConfig:     code/hainn/model_configuration.py
  Model registry:          code/hainn/model_registry.py
  ModelInstance_Set:       code/haipipe/model_base/modelinstance_set.py
  ModelInstance_Pipeline:  code/haipipe/model_base/modelinstance_pipeline.py
  PreFnPipeline:           code/hainn/prefn_pipeline.py

  Reference implementation (follow this for new models):
    code/hainn/tsforecast/
