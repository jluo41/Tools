---
name: deploy-sagemaker
part-of: haipipe-end
description: "AWS SageMaker deploy specialist for haipipe-end: wraps an Endpoint_Set into SageMaker model.tar.gz, deploys to a SageMaker endpoint, runs live smoke tests, monitors logs, tears down. Reads (never modifies) Endpoint_Sets from haipipe-end endpointset. Read the SageMaker pitfalls in ../develop-sagemaker/PART.md before any live action. Called by /haipipe-end when deploy target is sagemaker."
argument-hint: "[function] [endpoint_set_or_id] [args...]"
metadata:
  version: "0.1.3"
  last_updated: "2026-10-25"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-end deploy sagemaker
=============================

AWS SageMaker deployment specialist.
Consumes an Endpoint_Set built by `haipipe-end endpointset`, packages it for SageMaker, deploys, tests live, monitors, and cleans up.

  Function axis:  dashboard | deploy | test | monitor | teardown | review

---

Workspace prerequisites
----------------------

This skill describes the adapter contract. Availability in the current project
requires `platforms/platform-sagemaker-inference/`, its scoped guide, referenced scripts, compatible
runtime dependencies, deployment config, and the selected platform's credentials
and permissions. Inspect those paths before constructing a live command.
If a prerequisite is absent, return blocked with its exact missing path or setting;
prior deployment history is not proof that this workspace is deploy-ready.
Use the Endpoint_Set wire pair matching this platform and the project's actual
serving host. Do not infer host permissions or installed API behavior from examples.

Commands
--------

```
/haipipe-end deploy sagemaker                              -> dashboard: SageMaker endpoints + cost
/haipipe-end deploy sagemaker dashboard                    -> same
/haipipe-end deploy sagemaker deploy <endpoint_set>        -> push Endpoint_Set to SageMaker
/haipipe-end deploy sagemaker test <endpoint_id>           -> hit live SageMaker endpoint
/haipipe-end deploy sagemaker monitor <endpoint_id>        -> CloudWatch logs + invocation metrics
/haipipe-end deploy sagemaker teardown <endpoint_id>       -> stop endpoint, optional model cleanup
/haipipe-end deploy sagemaker review <endpoint_id>         -> audit deploy config (IAM, instance, scaling)
```

---

Dispatch Table
--------------

```
Invocation     Ref file(s)                              Function block
-------------- ---------------------------------------- -----------------------------------
dashboard      ../../ref/deploy-overview.md                          dashboard procedure (in this SKILL.md)
deploy         ../../ref/deploy-overview.md +
               ../../ref/
                 0-overview.md                          deploy procedure
test           ../../ref/deploy-overview.md                          test procedure
monitor        ../../ref/deploy-overview.md                          monitor procedure
teardown       ../../ref/deploy-overview.md                          teardown procedure
review         ../../ref/deploy-overview.md                          review procedure
```

The `deploy` step reads the endpointset overview to know the Endpoint_Set layout it consumes.

---

Step-by-Step Protocol
----------------------

Step 0: Read `../../ref/deploy-overview.md` for SageMaker-specific conventions
        (instance types, IAM roles, model.tar.gz layout, autoscaling).

Step 1: Parse args.
Function vocabulary above.
Required arg per function:
          deploy: <endpoint_set_name>     (path under 6-EndpointStore/)
          test/monitor/teardown/review: <sagemaker_endpoint_id>

Step 2: Verify AWS context:
          - AWS credentials available (env or `aws configure`)
          - Region set
          - IAM role for SageMaker execution exists or can be created

Step 3: Execute the function (see procedures below).

Step 4: Emit the structured tail:

```
status:    ok | blocked | failed
summary:   2-3 sentences on the deploy / test / etc.
artifacts: [SageMaker endpoint id, ARN, model package path on S3]
next:      suggested next command
```

---

Procedures (placeholder — fill from project's actual SageMaker conventions)
----------------------------------------------------------------------------

Deploy:
  1. Read Endpoint_Set at `_WorkSpace/6-EndpointStore/<endpoint_set>/`.
  (input contract, all deploy skills: canonical input = the folder; a .tar.gz twin is a wire form only)
  2. Build `model.tar.gz` containing `fn_endpoint/` + ModelInstance + an (logical bundle name; physically materialized as code/ + model/ in the set)
     `inference.py` entry point conforming to SageMaker's contract.
  3. Upload to S3 (project-configured bucket).
  4. Register a SageMaker Model pointing at the S3 artifact + execution role.
  5. Create EndpointConfig (instance type, autoscaling).
  6. Create Endpoint and wait for `InService`.
  7. Run a 1-payload smoke invocation; verify response.
  8. Record endpoint_id + ARN in the project's deploy log.

Test, Monitor, Teardown, Review:
  See `../../ref/deploy-overview.md` for the SageMaker-specific procedures and the
  `aws sagemaker` / `aws cloudwatch` CLI invocations the project uses.

---

Target Scope
-------------

Owns:
  - `model.tar.gz` packaging conforming to SageMaker's inference container contract
  - SageMaker endpoint config (instance type, count, autoscaling)
  - IAM role assumptions
  - `aws sagemaker` CLI invocation
  - CloudWatch log queries
  - Live invocation smoke tests against the deployed endpoint

Does NOT own:
  - Endpoint_Set content (read-only input from `/haipipe-end endpointset`)
  - ModelInstance training (`/haipipe-nn`)

If a deploy fails because of an Endpoint_Set issue, escalate to `/haipipe-end endpointset review` rather than patching here.
