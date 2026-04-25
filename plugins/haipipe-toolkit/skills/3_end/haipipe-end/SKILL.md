---
name: haipipe-end
description: "Run any Stage 6 endpoint work. Parses intent (artifact lifecycle vs. deploy target) and dispatches to the right specialist (haipipe-end-endpointset for the Endpoint_Set artifact, or haipipe-end-{sagemaker,databricks,flask,mlflow} for deploy targets). Use for packaging Endpoint_Sets, designing inference functions (MetaFn/TrigFn/PostFn/Src2InputFn/Input2SrcFn), local inference tests, or deploying to any target. Trigger: endpoint, deploy, package, inference Fn, /haipipe-end."
argument-hint: [target_or_function] [args...]
allowed-tools: Bash, Read, Grep, Glob, Skill
---

Skill: haipipe-end (orchestrator)
==================================

User-facing entry for Stage 6. Routes between two sub-axes:

  Artifact axis:   the Endpoint_Set itself (target-agnostic) -> endpointset
  Target axis:     where the artifact gets deployed         -> sagemaker / databricks / flask / mlflow

```
/haipipe-end                                   -> cross-target dashboard
/haipipe-end <fn>                              -> artifact lifecycle (endpointset)
/haipipe-end deploy <target> <endpoint_set>    -> dispatch to target deployer
/haipipe-end <target> <fn> [args]              -> dispatch directly to target skill
/haipipe-end "<natural language>"              -> infer artifact-vs-target, dispatch
```

---

Specialists
-----------

```
haipipe-end-endpointset    artifact: package, design, local test, review
haipipe-end-sagemaker      target: AWS SageMaker
haipipe-end-databricks     target: Databricks Model Serving
haipipe-end-flask          target: local Flask / FastAPI HTTP server
haipipe-end-mlflow         target: MLflow registry + `mlflow models serve`
```

---

Routing Decision: Artifact vs. Target
--------------------------------------

The first job is to decide whether the request is about **building the
Endpoint_Set artifact** or **deploying it to a target**.

**Artifact (-> haipipe-end-endpointset):**
```
Keywords: package, design, MetaFn, TrigFn, PostFn, Src2InputFn,
          Input2SrcFn, inference(), Endpoint_Pipeline, local test
Verbs:    package, design, test (local), review (of fn files)
```

**Target (-> haipipe-end-<target>):**
```
Verb 'deploy'             -> need a target keyword to disambiguate
Verb 'test' on a live id  -> target detected from endpoint registry
Keywords:
  sagemaker, aws, ECR, model.tar.gz                    -> sagemaker
  databricks, unity catalog, model serving             -> databricks
  flask, fastapi, local server, localhost:port         -> flask
  mlflow registry, mlflow serve, pyfunc                -> mlflow
```

If `deploy` appears without a target keyword -> ASK which target. Don't guess.

---

Function Verb Map
------------------

```
package, build, scaffold endpoint set         -> endpointset (package)
design <fn-type>                              -> endpointset (design)
test (local payload)                          -> endpointset (test)
review (of generated fn files)                -> endpointset (review)
deploy <target> ...                           -> <target> (deploy)
test <endpoint_id>                            -> <target> (test live)
monitor <endpoint_id>                         -> <target> (monitor)
teardown <endpoint_id>                        -> <target> (teardown)
review <endpoint_id>                          -> <target> (review deploy)
status, dashboard                             -> umbrella inline (cross-target)
```

---

Routing Logic
-------------

```
Step 1: Parse $ARGUMENTS.

Step 2: Check for target keyword.
  - Found  -> dispatch to that target with remaining args.
  - Not found -> proceed to Step 3.

Step 3: Check for artifact keyword or fn-type (meta/trig/post/src2input/input2src).
  - Found  -> dispatch to endpointset.
  - Not found -> proceed to Step 4.

Step 4: Disambiguate by verb:
  - package | design | local test | review (of files)  -> endpointset
  - deploy without target                              -> ASK target
  - test/monitor/teardown/review with id               -> resolve target via
                                                          local registry (each
                                                          target keeps a record
                                                          of endpoints deployed)

Step 5: Dispatch:
    Skill("haipipe-end-<target_or_endpointset>", args="<fn> <remaining_args>")

Step 6: Capture the specialist's structured tail and present.
```

---

Cross-Target Dashboard (no-arg case)
-------------------------------------

When invoked with no arguments, fan out to:

```
Skill("haipipe-end-endpointset", args="dashboard")    # what's packaged
Skill("haipipe-end-sagemaker",   args="dashboard")    # what's live on SageMaker
Skill("haipipe-end-databricks",  args="dashboard")    # what's live on Databricks
Skill("haipipe-end-flask",       args="dashboard")    # what's running locally
Skill("haipipe-end-mlflow",      args="dashboard")    # what's registered
```

Concatenate the tails into one cross-target view: built artifacts on the
left, deployed-where on the right.

---

Disambiguation Rules
---------------------

  - `deploy` without target         -> list 4 target options, wait.
  - `test <id>` ambiguous           -> look up id in target registries first.
  - `<fn-type>` mentioned           -> always artifact (endpointset).
  - Multi-target deploy             -> dispatch sequentially, one target at a
                                       time. Don't deploy in parallel — failures
                                       become confusing.

---

Specialist Return Contract
---------------------------

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was done
artifacts: [paths, endpoint ids, URLs]
next:      suggested next command
```

---

Files Owned by This Umbrella
-----------------------------

```
ref/deploy-overview.md      legacy cross-target deploy ref (was fn/fn-4-deploy.md);
                            kept for context — concrete deploy procedures live in
                            the target specialist skills.
```

The Endpoint_Set artifact reference docs (overview, meta, trig, post,
src2input, input2src) and packaging fn docs all live under
`../haipipe-end-endpointset/`. This umbrella is a thin router.
