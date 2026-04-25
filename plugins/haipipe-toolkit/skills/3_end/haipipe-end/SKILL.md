---
name: haipipe-end
description: "Run any Stage 6 endpoint work. Parses intent across FOUR axes — Fn-type (meta/trig/post/src2input/input2src), artifact-as-whole verb (package/test/review/dashboard), develop target (sagemaker/databricks/local) producing an Endpoint_Set, or deploy target (sagemaker/databricks/local/mlflow) serving one — and dispatches to the right specialist via Skill(). Use for designing inference Fns, packaging Endpoint_Sets, training a build to produce one, local inference tests, or deploying to any target. Trigger: endpoint, deploy, develop, train, package, inference Fn, MetaFn, TrigFn, PostFn, Src2InputFn, Input2SrcFn, /haipipe-end."
argument-hint: [target_or_fn_or_verb] [args...]
allowed-tools: Bash, Read, Grep, Glob, Skill
---

Skill: haipipe-end (orchestrator)
==================================

User-facing entry for Stage 6. Routes across **four axes**:

```
1. Fn-type axis        meta | trig | post | src2input | input2src
                       -> per-Fn-type specialist (one skill per type)

2. Artifact axis       package | test | dashboard | review (overall)
                       -> haipipe-end-endpointset

3. Develop axis        develop <target>  where target is one of
                       sagemaker | databricks | local
                       -> haipipe-end-develop-<target>
                       PRODUCES the Endpoint_Set (build side)

4. Deploy axis         deploy <target>  where target is one of
                       sagemaker | databricks | local | mlflow
                       -> haipipe-end-deploy-<target>
                       SERVES the Endpoint_Set (serve side)
```

The develop and deploy axes share targets but operate on different lifecycle
phases of the same artifact: develop BUILDS, deploy SERVES.

```
/haipipe-end                                -> cross-scope dashboard (artifact + develops + deploys)
/haipipe-end <fn-type> [verb]               -> per-Fn-type specialist
/haipipe-end <artifact-verb> [args]         -> endpointset specialist
/haipipe-end develop <target> <args>        -> develop specialist
/haipipe-end deploy <target> <args>         -> deploy specialist
/haipipe-end <target> <verb> [args]         -> develop or deploy (verb decides; default: deploy summary + soft-ask)
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

PER-TARGET DEVELOP (3)        BUILDS the Endpoint_Set
  haipipe-end-develop-sagemaker   AWS SageMaker Pipeline (wraps platform-sagemaker-training/)
  haipipe-end-develop-databricks  Databricks Job  ⚠️ deferred (no platform repo)
  haipipe-end-develop-local       local sequencer (delegates to /haipipe-nn modelset + endpointset package)

PER-TARGET DEPLOY (4)         SERVES the Endpoint_Set
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

Develop verb keyword map (selects the develop axis)
----------------------------------------------------

```
develop, build endpoint_set, train, training pipeline,
RegisterModel, model package group, build artifact (cloud)  -> develop axis
```

Note: bare `package` stays on the artifact axis (endpointset). The develop
axis is for **running training infrastructure** (SageMaker Pipeline,
Databricks Job, local nn-modelset run) that PRODUCES an Endpoint_Set.

Develop target keyword map
---------------------------

```
sagemaker (with develop verb), aws training, ModelPackageGroup    -> develop-sagemaker
databricks (with develop verb), Databricks Job, Unity Catalog
  (training context)                                              -> develop-databricks
local (with develop verb), local training, dev box build          -> develop-local
```

Deploy target keyword map
--------------------------

```
sagemaker, aws, ECR, model.tar.gz                  -> deploy-sagemaker
databricks, unity catalog, model serving           -> deploy-databricks
local, flask, fastapi, localhost, dev server       -> deploy-local
mlflow, mlflow registry, mlflow serve, pyfunc      -> deploy-mlflow
```

Develop verb map (forwarded as args to develop-* specialist)
-------------------------------------------------------------

```
develop <target> <config>           -> develop (full build)
test <config>                       -> local-system / local-docker test
monitor <execution_id>              -> tail pipeline / Job / local logs
teardown <execution_id>             -> stop run, optional registry cleanup
review <execution_id_or_arn>        -> audit completed run
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
           b) Develop verb present + target?             -> Develop axis
           c) Develop verb alone (no target)             -> ASK target
           d) Deploy verb 'deploy' present + target?     -> Deploy axis
           e) Deploy verb 'deploy' alone (no target)     -> ASK target
           f) Target alone (no develop/deploy verb)?     -> Deploy ref-only summary (default)
                                                            + soft-ask: "did you mean develop?"
           g) Artifact verb (package/test/dashboard)?    -> Artifact axis
           h) Verb 'review' alone, no <id>, no fn-type   -> Artifact axis (review-overall)
           i) Verb 'review <id>'                         -> Deploy axis (review live deploy)
                                                            -> resolve target from local registry
           j) 'overview' / 'explain'                     -> INLINE (umbrella reads ref/0-overview.md)
           k) No args                                    -> CROSS-SCOPE DASHBOARD (parallel fan-out)

Step 3:  Dispatch:
           Fn-type axis    -> Skill("haipipe-end-<fn-type>",       args="<verb> <rest>")
           Artifact axis   -> Skill("haipipe-end-endpointset",     args="<verb> <rest>")
           Develop axis    -> Skill("haipipe-end-develop-<target>", args="<verb> <rest>")
           Deploy axis     -> Skill("haipipe-end-deploy-<target>",  args="<verb> <rest>")

Step 4:  Capture the specialist's structured tail (status / summary /
         artifacts / next), present to user. If status != ok, stop chaining.
```

Target-alone disambiguation (rule f)
-------------------------------------

When the user types just a target (e.g. `/haipipe-end sagemaker`), default
to the deploy ref-only summary (more common ask) and append a single
clarification line:

```
[deploy-sagemaker ref-only summary here]

→ if you meant the build side, run:  /haipipe-end develop sagemaker [args]
```

This keeps the common path zero-friction while making the develop side
discoverable.

---

Cross-Scope Dashboard (no-arg case)
------------------------------------

When invoked with no arguments, fan out in parallel and concatenate tails:

```
Skill("haipipe-end-endpointset",         args="dashboard")    # what's packaged
Skill("haipipe-end-develop-sagemaker",   args="dashboard")    # SageMaker training pipelines + ModelPackages
Skill("haipipe-end-develop-local",       args="dashboard")    # local develop registry
Skill("haipipe-end-deploy-sagemaker",    args="dashboard")    # live on SageMaker
Skill("haipipe-end-deploy-databricks",   args="dashboard")    # live on Databricks
Skill("haipipe-end-deploy-local",        args="dashboard")    # running locally
# develop-databricks and deploy-mlflow excluded while deferred
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
  - `develop` without target                   -> list 3 develop targets (sagemaker/databricks/local), WAIT.
  - `deploy` without target                    -> list 4 deploy targets, WAIT.
  - Target alone, no verb                      -> deploy ref-only summary + soft-ask "did you mean develop?"
  - `test <id>` ambiguous (which target?)      -> look up id in target registries first
                                                  (develop registries first if id looks like a Pipeline ARN).
  - `review` ambiguous (artifact vs deploy
       vs develop)                             -> presence of Pipeline ARN / Job run id  → develop
                                                  presence of endpoint id                → deploy
                                                  absence of any id                      → artifact (review-overall)
  - Multi-target deploy / develop              -> dispatch sequentially. Don't run in parallel —
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
