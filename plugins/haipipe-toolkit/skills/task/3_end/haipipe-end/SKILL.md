---
name: haipipe-end
description: "Run any Stage 6 endpoint work: routes intent to the right specialist across Fn-type, artifact-verb, develop-target, and deploy-target axes. Use for designing inference Fns, packaging Endpoint_Sets, training a build, local inference tests, or deploying anywhere. Trigger: endpoint, deploy, develop, train, package, inference Fn, MetaFn, TrigFn, PostFn, Src2InputFn, Input2SrcFn, /haipipe-end."
argument-hint: "[target_or_fn_or_verb] [args...]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "0.1.2"
  last_updated: "2026-07-08"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-end (orchestrator)
==================================

User-facing entry for Stage 6.
Routes across **four axes**:

```
1. Fn-type axis        meta | trig | post | src2input | input2src
                       -> per-Fn-type specialist (one skill per type)

2. Artifact axis       package | test | profile | dashboard | review (overall)
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

The develop and deploy axes share targets but operate on different lifecycle phases of the same artifact: develop BUILDS, deploy SERVES.

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
  haipipe-end-endpointset   Endpoint_Set lifecycle: package, test, profile, review, dashboard

PER-TARGET DEVELOP (3)        BUILDS the Endpoint_Set
  haipipe-end-develop-sagemaker   AWS SageMaker Pipeline (wraps platforms/platform-sagemaker-training/)
  haipipe-end-develop-databricks  Databricks Job  ⚠️ deferred (repo platforms/platform-databrick-training/ exists; wiring + Lesson-15 reconciliation pending)
  haipipe-end-develop-local       local sequencer (delegates to /haipipe-nn modelset + endpointset package)

PER-TARGET DEPLOY (4)         SERVES the Endpoint_Set
  haipipe-end-deploy-sagemaker    AWS SageMaker (wraps platforms/platform-sagemaker-inference/)
  haipipe-end-deploy-databricks   Databricks Model Serving (wraps platforms/platform-databrick-inference/)
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

Note: bare `package` stays on the artifact axis (endpointset).
The develop axis is for **running training infrastructure** (SageMaker Pipeline, Databricks Job, local nn-modelset run) that PRODUCES an Endpoint_Set.

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
           g) Artifact verb (package/test/profile/dashboard)?  -> Artifact axis
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

When the user types just a target (e.g.
`/haipipe-end sagemaker`), default to the deploy ref-only summary (more common ask) and append a single clarification line:

```
[deploy-sagemaker ref-only summary here]

→ if you meant the build side, run:  /haipipe-end develop sagemaker [args]
```

This keeps the common path zero-friction while making the develop side discoverable.

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

The 5 per-Fn-type specialists are NOT included in the no-arg dashboard (they'd repeat the same artifact-level info).
For per-Fn-type status use `/haipipe-end-endpointset review`.

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

Guardrails — inference Fn authoring (apply to ALL 5 Fn-types)
--------------------------------------------------------------

```
FN-1   A NAME THAT DOES NOT RESOLVE MUST RAISE.
       Every inference Fn looks names up: arms in the model output, columns in a
       source frame, fields in a payload. The house style has been to substitute a
       default — a membership filter that drops the name, `safe_get(row, name,
       default)`, a `format_date` that falls back to `datetime.now()`. Each turns a
       wrong name into a PLAUSIBLE VALUE with no error, so the defect ships looking
       healthy and can sit in production for months.

       Four instances found in one session (SMSR4, 260807):
         PostFn        'progressFeedback' absent from 40 arms -> list shrank 3->2
                       -> `salience` served on 6,513/6,513 live requests
         Src2InputFn   7 column names absent from every source frame -> dateOfBirth
                       became a constant, zipCode null, dates became now()
                       -> 371 of 1995 vocab slots blank, 18.6% of model input
         repro check   any-score-vs-any-score, different arms, 100x scale apart
                       -> could not fail, caught none of the above

       Author with an explicit split: a DECLARED read raises, an OPTIONAL read
       yields None. Name the missing entries in the exception message.

FN-2   FORK, NEVER EDIT A SHARED Fn. Count the manifests first:

           find . -name manifest.json | xargs grep -l '"<FnType>": "<name>"'

       Nine manifests shared the SMSR4 PostFn and nine shared its Src2InputFn. The
       PostFn's list was still CORRECT for SMSR3, so an in-place fix would have
       broken a working endpoint. Name the fork for what makes it different, dated:
       `R4sms_10o40_ArmGreedy_v260807` follows `R3sms_9o20_ArmGreedy_v250922`.
       Note the asymmetry: a fork is mandatory when the original is right for
       someone else, and merely SAFER when the bug is wrong for everybody — in the
       latter case still fork, then migrate the others deliberately.

FN-3   An Fn is inherited across ROUNDS. The vocabulary underneath it (arm set,
       column names, payload schema) changes between rounds while the Fn does not.
       Before reusing an Fn for a new round, diff the round's vocabulary against
       every name the Fn hardcodes. This is the single highest-yield check in
       Stage 6 and it is 10 lines of Python.

FN-4   VERIFY WITH A ROUND-TRIP GATE, and prove the gate bites first.
       The endpoint must reproduce the model's OWN prediction for the packaged
       examples — served arm, argmax, and every per-arm score. Run it against the
       known-broken build BEFORE the fixed one; if it passes the broken build, the
       gate is what is broken. See haipipe-task GATE-1 and the reference impls in
       `-src2input`'s roundtrip section.
```

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
ref/deploy-overview.md      shared cross-target deploy ref (read by all 4 deploy specialists)

fn/fn-design.md             SHARED design procedure — read by all 5 per-Fn-type children
                            when handling `design`. Each child supplies its own concepts.md.
```

These files are SHARED — children read them via `../haipipe-end/...`.
Each child also has its own scope-specific `ref/concepts.md`.
