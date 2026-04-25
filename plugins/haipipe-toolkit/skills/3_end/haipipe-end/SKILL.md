---
name: haipipe-end
description: "Run any Stage 6 endpoint work. Parses intent across THREE axes — Fn-type (meta/trig/post/src2input/input2src), artifact-as-whole verb (package/test/review/dashboard), or deploy target (sagemaker/databricks/local/mlflow) — and dispatches to the right specialist via Skill(). Use for designing inference Fns, packaging Endpoint_Sets, local inference tests, or deploying to any target. Trigger: endpoint, deploy, package, inference Fn, MetaFn, TrigFn, PostFn, Src2InputFn, Input2SrcFn, /haipipe-end."
argument-hint: [target_or_fn_or_verb] [args...]
allowed-tools: Bash, Read, Grep, Glob, Skill
---

Skill: haipipe-end (orchestrator)
==================================

User-facing entry for Stage 6. Routes across **three axes**:

```
1. Fn-type axis        meta | trig | post | src2input | input2src
                       -> per-Fn-type specialist (one skill per type)

2. Artifact axis       package | test | dashboard | review (overall)
                       -> haipipe-end-endpointset

3. Deploy axis         deploy <target>  where target is one of
                       sagemaker | databricks | local | mlflow
                       -> haipipe-end-deploy-<target>
```

```
/haipipe-end                                -> cross-scope dashboard (artifact + deploys)
/haipipe-end <fn-type> [verb]               -> per-Fn-type specialist
/haipipe-end <artifact-verb> [args]         -> endpointset specialist
/haipipe-end deploy <target> <args>         -> deploy specialist
/haipipe-end <target> <verb> [args]         -> deploy specialist (target-first form)
/haipipe-end "<natural language>"           -> infer axis, dispatch
/haipipe-end overview | explain [question]  -> handled inline (cross-cutting)
```

---

Specialists
-----------

```
PER-FN-TYPE (5)
  haipipe-end-meta          MetaFn — model metadata lookup
  haipipe-end-trig          TrigFn — trigger detection
  haipipe-end-post          PostFn — response formatting
  haipipe-end-src2input     Src2InputFn — record → wire payload
  haipipe-end-input2src     Input2SrcFn — wire payload → record

ARTIFACT-AS-WHOLE (1)
  haipipe-end-endpointset   Endpoint_Set lifecycle: package, test, review, dashboard

PER-TARGET DEPLOY (4)
  haipipe-end-deploy-sagemaker    AWS SageMaker (wraps platform-sagemaker-inference/)
  haipipe-end-deploy-databricks   Databricks Model Serving (wraps platform-databrick-inference/)
  haipipe-end-deploy-local        local self-hosted (Flask / FastAPI / Docker)
  haipipe-end-deploy-mlflow       MLflow registry + serve   ⚠️ deferred (no platform repo)
```

---

Fn-type Keyword Map
--------------------

```
MetaFn, model metadata, model card, meta             -> meta
TrigFn, trigger, gate, condition, trig               -> trig
PostFn, response format, post-process, post          -> post
Src2InputFn, record-to-payload, serialize, src2input -> src2input
Input2SrcFn, payload-to-record, deserialize, input2src -> input2src
```

Artifact verb map (for endpointset)
------------------------------------

```
package, build artifact, run pipeline, scaffold endpoint set  -> endpointset (package)
test, smoke test, local test, run inference                   -> endpointset (test)
review (overall, no fn-type)                                  -> endpointset (review)
dashboard, status, what's there                               -> endpointset (dashboard)
```

Deploy target keyword map
--------------------------

```
sagemaker, aws, ECR, model.tar.gz                  -> deploy-sagemaker
databricks, unity catalog, model serving           -> deploy-databricks
local, flask, fastapi, localhost, dev server       -> deploy-local
mlflow, mlflow registry, mlflow serve, pyfunc      -> deploy-mlflow
```

Deploy verb map (forwarded as args to deploy-* specialist)
------------------------------------------------------------

```
deploy <target> <endpoint_set>      -> deploy
test <endpoint_id>                  -> test live endpoint
monitor <endpoint_id>               -> tail logs / metrics
teardown <endpoint_id>              -> stop endpoint, cleanup
review <endpoint_id>                -> audit deploy config
```

---

Routing Logic
-------------

```
Step 1:  Parse $ARGUMENTS.

Step 2:  Detect axis (priority order, first match wins):

           a) Fn-type keyword present?                   -> Fn-type axis
           b) Deploy target keyword present?             -> Deploy axis
           c) Verb 'deploy' alone (no target)            -> ASK target
           d) Artifact verb (package/test/dashboard)?    -> Artifact axis
           e) Verb 'review' alone, no <id>, no fn-type   -> Artifact axis (review-overall)
           f) Verb 'review <id>'                         -> Deploy axis (review live deploy)
                                                            -> resolve target from local registry
           g) 'overview' / 'explain'                     -> INLINE (umbrella reads ref/0-overview.md)
           h) No args                                    -> CROSS-SCOPE DASHBOARD (parallel fan-out)

Step 3:  Dispatch:
           Fn-type axis    -> Skill("haipipe-end-<fn-type>",      args="<verb> <rest>")
           Artifact axis   -> Skill("haipipe-end-endpointset",    args="<verb> <rest>")
           Deploy axis     -> Skill("haipipe-end-deploy-<target>", args="<verb> <rest>")

Step 4:  Capture the specialist's structured tail (status / summary /
         artifacts / next), present to user. If status != ok, stop chaining.
```

---

Cross-Scope Dashboard (no-arg case)
------------------------------------

When invoked with no arguments, fan out in parallel and concatenate tails:

```
Skill("haipipe-end-endpointset",       args="dashboard")    # what's packaged
Skill("haipipe-end-deploy-sagemaker",  args="dashboard")    # live on SageMaker
Skill("haipipe-end-deploy-databricks", args="dashboard")    # live on Databricks
Skill("haipipe-end-deploy-local",      args="dashboard")    # running locally
# deploy-mlflow excluded while deferred
```

The 5 per-Fn-type specialists are NOT included in the no-arg dashboard
(they'd repeat the same artifact-level info). For per-Fn-type status
use `/haipipe-end-endpointset review`.

---

Inline Modes (umbrella handles itself, no dispatch)
----------------------------------------------------

`/haipipe-end overview` and `/haipipe-end explain [question]`:

  1. Read `ref/0-overview.md` (Stage 6 architecture, inference pipeline, YAML).
  2. If the question references a specific Fn-type, also read that
     specialist's `ref/concepts.md` for context.
  3. Answer directly. Cite which ref docs informed the answer.

These run inline — no `Skill()` call.

---

Disambiguation Rules
---------------------

  - Multiple Fn-types in one request           -> ASK which (or dispatch sequentially).
  - `deploy` without target                    -> list 4 targets, WAIT.
  - `test <id>` ambiguous (which target?)      -> look up id in target registries first.
  - `review` ambiguous (artifact vs deploy?)   -> presence of <id> = deploy; absence = artifact.
  - Multi-target deploy                        -> dispatch sequentially. Don't deploy in parallel —
                                                  failures become confusing.

---

Specialist Return Contract
---------------------------

Every specialist emits a tail this orchestrator parses:

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was done
artifacts: [paths, endpoint ids, URLs, ARNs]
next:      suggested next command
```

---

Files Owned by This Umbrella
-----------------------------

```
ref/0-overview.md           Stage 6 architecture + inference pipeline + YAML conventions
                            (read by all 5 per-Fn-type children for context)
ref/deploy-overview.md      legacy cross-target deploy ref

fn/fn-design.md             SHARED design procedure — read by all 5 per-Fn-type children
                            when handling `design`. Each child supplies its own concepts.md.
```

These files are SHARED — children read them via `../haipipe-end/...`. Each
child also has its own scope-specific `ref/concepts.md`.
