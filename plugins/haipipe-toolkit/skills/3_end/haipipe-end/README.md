haipipe-end Skill
==================

Skill for Stage 6 endpoint packaging, testing, design, and deployment.
Covers the full lifecycle from trained ModelInstance_Set to live serving endpoint.

---

What This Skill Covers
-----------------------

Stage 6 in the haipipe pipeline:

  Stage 5 (ModelInstance_Set)
      ↓  /haipipe-end package
  Stage 6 (Endpoint_Set) — self-contained inference package
      ↓  /haipipe-end test
  Verified endpoint
      ↓  /haipipe-end deploy
  Live serving endpoint (Databricks Model Serving or local)

The skill also covers designing and reviewing the 5 inference functions (Fn types)
that define how each endpoint handles requests.

---

Quick Commands
---------------

  /haipipe-end dashboard     Scan EndpointStore, show status of all endpoints
  /haipipe-end package       Run Endpoint_Pipeline to build an Endpoint_Set
  /haipipe-end test          Test Endpoint_Set.inference() with profiling
  /haipipe-end design        Build a new inference function (Fn type)
  /haipipe-end deploy        Deploy packaged endpoint to Databricks or local
  /haipipe-end review        Review Fn files for correctness and cross-consistency

Add fn-type scope for targeted design/review:

  /haipipe-end design meta         Design a MetaFn
  /haipipe-end design input2src    Design an Input2SrcFn
  /haipipe-end review trigfn       Review TrigFn files
  /haipipe-end review postfn       Review PostFn files

---

File Map
---------

  SKILL.md                  Router — dispatch table + step-by-step protocol
  README.md                 This file — quick reference

  ref/
    0-overview.md           Architecture, 7-step inference pipeline, formats
    1-meta.md               MetaFn contract and implementation guide
    2-trig.md               TrigFn contract and implementation guide
    3-post.md               PostFn contract and implementation guide
    4-src2input.md          Src2InputFn contract and implementation guide
    5-input2src.md          Input2SrcFn contract and implementation guide

  fn/
    fn-0-dashboard.md       Dashboard: scan EndpointStore status
    fn-1-package.md         Package: run Endpoint_Pipeline
    fn-2-test.md            Test: inference test protocol with profiling
    fn-3-design.md          Design: build new Fn files (all 5 types)
    fn-4-deploy.md          Deploy: Databricks (MLflow + Unity Catalog) or local
    fn-review.md            Review: per-Fn checklists + cross-consistency

---

The 5 Inference Function Types
--------------------------------

  Type          Signature                                      Purpose
  ────────────  ─────────────────────────────────────────────  ──────────────────────────────────────
  MetaFn        MetaFn(SPACE) -> Dict                         Model name mapping + metadata response
  TrigFn        TrigFn(payload_json) -> DataFrame | None      Trigger detection (None = skip)
  PostFn        PostFn(ModelArtifactName_to_Inference, SPACE) Format scores → client JSON
  Src2InputFn   Src2InputFn(ProcName_to_ProcDf, SPACE)        ProcDf → payload (packaging only)
  Input2SrcFn   Input2SrcFn(payload_json, SPACE)              Payload → ProcDf (inference entry)

All 5 are generated from builders in code-dev/1-PIPELINE/6-Endpoint-WorkSpace/.
NEVER edit code/haifn/fn_endpoint/ directly.

---

7-Step Inference Pipeline (inside Endpoint_Set.inference())
-------------------------------------------------------------

  1. TrigFn          payload_json → df_case_raw | None
  2. Input2SrcFn     payload_json → ProcName_to_ProcDf
  3. CaseFn          ProcDf → case features (via PreFnPipeline)
  4. TfmFn           case features → model input tensor/DataFrame
  5. SplitFn         model input → per-model inputs
  6. ModelInfer      model input → DataFrame with score__{action} columns
  7. PostFn          DataFrame → client response JSON

---

Supported Platforms
--------------------

  Platform     Wrapper              Registry              Auth
  ───────────  ───────────────────  ────────────────────  ───────────────────
  Databricks   MLflow PythonModel   Unity Catalog (UC)    DATABRICKS_TOKEN
  Local        direct Python call   filesystem            none
  SageMaker    Flask + Docker       S3 + SageMaker        AWS IAM

Core inference: endpoint_set.inference(payload) — identical on all platforms.
Only the wrapper and registry differ.

---

Common Workflows
-----------------

**Build + package + test a new endpoint:**

  1. /haipipe-end design input2src   Build Input2SrcFn (defines schema)
  2. /haipipe-end design src2input   Build Src2InputFn (inverse)
  3. /haipipe-end design meta        Build MetaFn
  4. /haipipe-end design trig        Build TrigFn
  5. /haipipe-end design post        Build PostFn
  6. /haipipe-end package            Run Endpoint_Pipeline
  7. /haipipe-end test               Verify with profiling

**Deploy to Databricks:**

  1. /haipipe-end test               (must pass first)
  2. /haipipe-end deploy             Packages to UC, deploys to Model Serving

**Troubleshoot a failing endpoint:**

  1. /haipipe-end review             Check all 5 Fns for issues
  2. /haipipe-end test               Run with profiling to find bottleneck

---

Key Rules
----------

  1. Run /haipipe-end test before deploying — ALWAYS
  2. Never edit code/haifn/fn_endpoint/ directly — edit builders
  3. Always chain: source .venv/bin/activate && source env.sh && python ...
  4. Python 3.10 required for Databricks packaging (not 3.11 or 3.12)
  5. Design order: Input2SrcFn → Src2InputFn → MetaFn → TrigFn → PostFn
  6. call warmup() before first inference to eliminate cold-start latency
  7. Deploy dev → staging → prod, never skip stages

---

Key Directories
----------------

  code/haifn/fn_endpoint/           Generated Fn files (DO NOT EDIT)
    fn_meta/                        MetaFn files
    fn_trig/                        TrigFn files
    fn_post/                        PostFn files
    fn_src2input/                   Src2InputFn files
    fn_input2src/                   Input2SrcFn files

  code-dev/1-PIPELINE/6-Endpoint-WorkSpace/    Builders (EDIT HERE)
    a1_build_metafn_*.py
    b1_build_trigfn_*.py
    c1_build_postfn_*.py
    d1_build_src2inputfn_*.py
    e1_build_input2srcfn_*.py

  _WorkSpace/5-ModelInstanceStore/  Stage 5 input (trained models)
  _WorkSpace/6-EndpointStore/       Stage 6 output (packaged endpoints)

  platform-databrick-inference/     Databricks deployment submodule
    scripts/package.py              Package to Unity Catalog
    scripts/deploy.py               Deploy to Model Serving
    scripts/test.py                 Test MLflow model or deployed URL
    config/dev.yaml                 Dev environment config
    config/staging.yaml             Staging config
    config/prod.yaml                Production config
