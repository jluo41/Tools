---
name: haipipe-end-sagemaker
description: "AWS SageMaker target specialist for haipipe-end. Wraps an Endpoint_Set into the SageMaker model.tar.gz format, deploys to a SageMaker endpoint, runs live smoke tests, monitors logs, and tears down. Reads Endpoint_Sets produced by haipipe-end-endpointset; never modifies them. Called by /haipipe-end orchestrator when target is sagemaker."
argument-hint: [function] [endpoint_set_or_id] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

Skill: haipipe-end-sagemaker
=============================

AWS SageMaker deployment specialist. Consumes an Endpoint_Set built by
`haipipe-end-endpointset`, packages it for SageMaker, deploys, tests
live, monitors, and cleans up.

  Function axis:  dashboard | deploy | test | monitor | teardown | review

---

Commands
--------

```
/haipipe-end-sagemaker                              -> dashboard: SageMaker endpoints + cost
/haipipe-end-sagemaker dashboard                    -> same
/haipipe-end-sagemaker deploy <endpoint_set>        -> push Endpoint_Set to SageMaker
/haipipe-end-sagemaker test <endpoint_id>           -> hit live SageMaker endpoint
/haipipe-end-sagemaker monitor <endpoint_id>        -> CloudWatch logs + invocation metrics
/haipipe-end-sagemaker teardown <endpoint_id>       -> stop endpoint, optional model cleanup
/haipipe-end-sagemaker review <endpoint_id>         -> audit deploy config (IAM, instance, scaling)
```

---

Dispatch Table
--------------

```
Invocation     Ref file(s)                              Function block
-------------- ---------------------------------------- -----------------------------------
dashboard      ref/concepts.md                          dashboard procedure (in this SKILL.md)
deploy         ref/concepts.md +
               ../haipipe-end-endpointset/ref/
                 0-overview.md                          deploy procedure
test           ref/concepts.md                          test procedure
monitor        ref/concepts.md                          monitor procedure
teardown       ref/concepts.md                          teardown procedure
review         ref/concepts.md                          review procedure
```

The `deploy` step reads the endpointset overview to know the Endpoint_Set
layout it consumes.

---

Step-by-Step Protocol
----------------------

Step 0: Read `ref/concepts.md` for SageMaker-specific conventions
        (instance types, IAM roles, model.tar.gz layout, autoscaling).

Step 1: Parse args. Function vocabulary above. Required arg per function:
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
  2. Build `model.tar.gz` containing `fn_endpoint/` + ModelInstance + an
     `inference.py` entry point conforming to SageMaker's contract.
  3. Upload to S3 (project-configured bucket).
  4. Register a SageMaker Model pointing at the S3 artifact + execution role.
  5. Create EndpointConfig (instance type, autoscaling).
  6. Create Endpoint and wait for `InService`.
  7. Run a 1-payload smoke invocation; verify response.
  8. Record endpoint_id + ARN in the project's deploy log.

Test, Monitor, Teardown, Review:
  See `ref/concepts.md` for the SageMaker-specific procedures and the
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
  - Endpoint_Set content (read-only input from `/haipipe-end-endpointset`)
  - ModelInstance training (`/haipipe-nn`)

If a deploy fails because of an Endpoint_Set issue, escalate to
`/haipipe-end-endpointset review` rather than patching here.
