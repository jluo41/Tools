---
name: haipipe-end-develop-sagemaker
description: "AWS SageMaker develop specialist for haipipe-end. Runs Stage 5 training as a managed SageMaker Pipeline (Preprocess → Train → Reorganize → RegisterModel) and produces a deployable Endpoint_Set / registered model package. Backed by platform-sagemaker-training/ scripts (system → docker → pipeline testing ladder, ECR push, ModelPackageGroup registration). Writes Endpoint_Sets that haipipe-end-endpointset and the deploy specialists consume. Called by /haipipe-end orchestrator when develop target is sagemaker."
argument-hint: [verb] [endpoint_set_or_run_id] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

Skill: haipipe-end-develop-sagemaker
=====================================

AWS SageMaker development specialist. Runs the project's training pipeline
as a managed SageMaker Pipeline and produces a deployable Endpoint_Set
(packaged `model.tar.gz` under `6-EndpointStore/`) plus a registered model
package in the SageMaker Model Registry.

The deploy specialists (`-deploy-sagemaker`, `-deploy-databricks`, etc.)
then consume that Endpoint_Set. This skill OWNS the build side; deploy
specialists own the serve side.

  Verb axis:        dashboard | develop | test | monitor | teardown | review

  Stage flag:       --stage system   (local Python, no Docker — fastest)
                    --stage docker   (local Docker training container)
                    --stage pipeline (full SageMaker Pipeline — default for `develop`)

---

Commands
--------

```
/haipipe-end-develop-sagemaker                                 -> dashboard: pipelines + registered models
/haipipe-end-develop-sagemaker dashboard                       -> same
/haipipe-end-develop-sagemaker develop <config.yaml>           -> full SageMaker Pipeline (RegisterModel)
/haipipe-end-develop-sagemaker test <config.yaml>              -> local-system test (no Docker, no AWS)
/haipipe-end-develop-sagemaker test <config.yaml> --stage docker -> local Docker training container test
/haipipe-end-develop-sagemaker monitor <execution_id>          -> tail pipeline / CloudWatch logs
/haipipe-end-develop-sagemaker teardown <execution_id>         -> stop pipeline, optional model-package cleanup
/haipipe-end-develop-sagemaker review <execution_id_or_arn>    -> audit pipeline run / registered model
```

`<execution_id>` is a SageMaker Pipeline execution ARN; `<arn>` for `review`
may be a ModelPackage ARN.

---

Dispatch Table
--------------

```
Verb        Ref file(s)                              Backing platform script
----------- ---------------------------------------- ----------------------------------------------------
dashboard   ref/concepts.md                          (none — list pipelines + ModelPackageGroup contents)
develop     ref/concepts.md +                        platform-sagemaker-training/scripts/
            ../haipipe-end-endpointset/ref/            run_training_pipeline/run_training_pipeline.py
              0-overview.md
test        ref/concepts.md                          --stage system:
                                                       run_training_pipeline/run_train_local_system.py
                                                     --stage docker:
                                                       run_training_pipeline/run_train_local_docker.py
monitor     ref/concepts.md                          aws sagemaker describe-pipeline-execution +
                                                     aws logs tail
teardown    ref/concepts.md                          aws sagemaker stop-pipeline-execution +
                                                     optional aws sagemaker delete-model-package
review      ref/concepts.md                          aws sagemaker describe-pipeline-execution +
                                                     aws sagemaker describe-model-package
```

The `develop` step reads the endpointset overview to know the Endpoint_Set
layout it must produce.

---

Step-by-Step Protocol
----------------------

Step 0: Read `ref/concepts.md` for SageMaker training conventions
        (ECR image, IAM role, ModelPackageGroupName, Pipeline parameters,
        S3 workspace layout, RegisterModel contract).

Step 1: Parse args. Required arg per verb:
          develop:                       <config.yaml>
          test:                          <config.yaml> [--stage system|docker]
          monitor/teardown/review:       <execution_id_or_arn>

Step 2: Verify AWS context (skip for `test --stage system`):
          - AWS credentials available (env or `aws configure`)
          - Region set
          - SageMaker execution role exists
          - Training ECR image present (else suggest `build_docker_training.py`)
          - ModelPackageGroup exists (else create on first develop)

Step 3: Execute the verb (see procedures below).

Step 4: Emit the structured tail:

```
status:    ok | blocked | failed
summary:   2-3 sentences on the develop / test / etc.
artifacts: [Pipeline execution ARN, model.tar.gz S3 URI, ModelPackage ARN,
            Endpoint_Set path under 6-EndpointStore/]
next:      suggested next command (typically `/haipipe-end deploy <target> <endpoint_set>`)
```

---

Procedures (placeholder — fill from project's actual SageMaker conventions)
----------------------------------------------------------------------------

Develop (full pipeline, default):
  1. Load `<config.yaml>` (e.g. `config/config_raw_to_endpoint_ctr_r20.yaml`).
  2. Defer to `python platform-sagemaker-training/scripts/run_training_pipeline/run_training_pipeline.py
     --config <config.yaml>` which builds + runs the 3-step Pipeline:
         a) PreprocessStep  — raw → AIData (cohort partitioning)
         b) TrainingStep    — AIData → trained model + Endpoint_Set bundle
         c) ReorganizeStep  — unpack outputs to clean S3 paths
         d) RegisterModel   — register into ModelPackageGroup (parallel)
  3. Wait for pipeline completion (or run with `--no-wait` and poll separately).
  4. Reorganize step deposits results to:
         workspace/{version}/5-ModelInstanceStore/  (weights)
         workspace/{version}/6-EndpointStore/       (Endpoint_Set + model.tar.gz)
  5. Record (execution_arn, model_package_arn, endpoint_set_path) in the
     project's develop log.

Test (--stage system):
  1. Defer to `python platform-sagemaker-training/scripts/run_training_pipeline/run_train_local_system.py
     --config <config.yaml>`. Runs training in the local Python env. Output
     to `opt_ml/model/`. No Docker, no AWS — fastest iteration.

Test (--stage docker):
  1. Defer to `python platform-sagemaker-training/scripts/run_training_pipeline/run_train_local_docker.py
     --config <config.yaml>`. Runs training inside the local Docker training
     image — validates the container's training contract before pushing to
     ECR.

Monitor:
  1. `aws sagemaker describe-pipeline-execution --pipeline-execution-arn <arn>`
     → reports current step, status, failure reason.
  2. `aws logs tail /aws/sagemaker/ProcessingJobs --follow` (or TrainingJobs)
     → live CloudWatch log stream.

Teardown:
  1. `aws sagemaker stop-pipeline-execution --pipeline-execution-arn <arn>`.
  2. Optional: `aws sagemaker delete-model-package --model-package-arn <arn>`
     to drop the registered version (use with caution — deploy specialists may
     reference it).

Review:
  1. `aws sagemaker describe-pipeline-execution` for the run.
  2. `aws sagemaker describe-model-package` for the registered output.
  3. Cross-check that the Endpoint_Set path on S3 matches the manifest.

---

Target Scope
-------------

Owns:
  - Wrapping the project's `code-dev/1-PIPELINE/6-Endpoint-WorkSpace/` build
    into a SageMaker Pipeline (Preprocess → Train → Reorganize)
  - Training ECR image lifecycle (delegates to `build_docker_training.py`)
  - SageMaker Pipeline parameters (ModelPackageGroupName, image URI, role,
    instance type, hyperparameters surface)
  - RegisterModel step + ModelPackageGroup membership
  - Local-system / local-Docker training tests (the lower rungs of the ladder)
  - S3 workspace layout for trained outputs

Does NOT own:
  - Endpoint_Set CONTENT (the Fn-type modules + manifest layout) — owned by
    `/haipipe-end-endpointset` and the per-Fn-type specialists. This skill
    just runs the build that PRODUCES one.
  - Inference / serving — that's the `-deploy-*` specialists. The output of
    this skill is what they consume.
  - Model class / Tuner / Instance code — that's `/haipipe-nn`. This skill
    runs whatever ModelSet the project has assembled.

If a develop run fails because of an Endpoint_Set or ModelSet issue, escalate
to `/haipipe-end-endpointset review` or `/haipipe-nn modelset review` rather
than patching here.

---

Known Pitfalls (verified on this account: 583537983112 dev / us-east-2)
------------------------------------------------------------------------

These same constraints apply to the sibling `-deploy-sagemaker` skill —
read both pitfalls before running any SageMaker action.

**1. SSO role needs SageMaker action permissions explicitly.** The
   `df-rxinform-nonprod-jhuuser` permission set (and most baseline DrFirst
   SSO sets) does NOT grant `sagemaker:*` by default. Without it the first
   `DescribeEndpoint` / `CreatePipeline` call returns:

   ```
   AccessDeniedException ... no identity-based policy allows the
   sagemaker:DescribeEndpoint action
   ```

   Required IAM actions for the train + deploy lifecycle:

   ```
   sagemaker: CreatePipeline, StartPipelineExecution,
              DescribePipelineExecution, StopPipelineExecution,
              ListPipelines, CreateModel, CreateEndpointConfig,
              CreateEndpoint, UpdateEndpoint, DescribeEndpoint,
              DescribeEndpointConfig, DescribeModel, ListEndpoints,
              ListEndpointConfigs, ListModels, DeleteEndpoint,
              DeleteEndpointConfig, DeleteModel, InvokeEndpoint,
              CreateModelPackage, CreateModelPackageGroup,
              DescribeModelPackage, ListModelPackages, RegisterModel
   iam:       PassRole on SageMaker-ExecutionRole-* (with
              iam:PassedToService = sagemaker.amazonaws.com)
   application-autoscaling: RegisterScalableTarget, PutScalingPolicy,
              DescribeScalableTargets, DescribeScalingPolicies
   ecr:       BatchGetImage, GetDownloadUrlForLayer (for pull)
              PutImage, InitiateLayerUpload, UploadLayerPart,
              CompleteLayerUpload (for push)
   s3:        GetObject / PutObject on the standard model bucket
              (rxinform-analytics-personalization in dev)
   ```

   Cleanest fix: attach AWS-managed `AmazonSageMakerFullAccess` to the
   SSO permission set. Curated alternative in
   `examples/ProjA-Timing-01-OptTime/tasks/C01_endpoint/01_endpoint/IAM_REQUEST.md`.

**2. Multi-arch OCI manifests break SageMaker.** If a training image is
   built with `docker buildx` defaults (multi-arch + provenance + SBOM),
   the resulting ECR tag is an `application/vnd.oci.image.index.v1+json`
   manifest, which SageMaker rejects:

   ```
   ValidationException ... Unsupported manifest media type
   application/vnd.oci.image.index.v1+json for image <ECR URI>
   ```

   Build training images with the documented flags
   (`platform-sagemaker-training/CLAUDE.md` mirrors the inference doc):

   ```bash
   docker buildx build \
     --platform linux/amd64 \
     --provenance=false --sbom=false \
     --tag <ECR URI>:<tag> --push .
   ```

   To verify before deploy:

   ```bash
   aws ecr describe-images --repository-name <repo> \
     --query 'imageDetails[?contains(imageTags, `latest`)].imageManifestMediaType'
   # must NOT contain "index" — should be "manifest.v1+json"
   ```

**3. Find the proven-working image before pushing a new one.** Before
   building/pushing your own training image, list what's already in use:

   ```bash
   # All in-service endpoints' training images
   for ep in $(aws sagemaker list-endpoints --query 'Endpoints[*].EndpointName' --output text); do
     cfg=$(aws sagemaker describe-endpoint --endpoint-name $ep --query 'EndpointConfigName' --output text)
     mdl=$(aws sagemaker describe-endpoint-config --endpoint-config-name $cfg --query 'ProductionVariants[0].ModelName' --output text)
     img=$(aws sagemaker describe-model --model-name $mdl --query 'PrimaryContainer.Image' --output text)
     echo "$ep -> $img"
   done
   ```

   In this account, the proven-working inference image for SMS-family
   models is `personalize-inference-container:latest` (NOT
   `docker-inference-standard`, which had broken multi-arch tags on
   2026-05-21). Training images live in `docker-training-v2`. Pointing
   configs at the wrong repo wastes a 10-minute deploy cycle on the
   manifest-format error.

**4. STS session tokens expire mid-deploy.** SSO-assumed STS credentials
   are typically ~1 hour. A long `develop` Pipeline run can outlast the
   session and start failing intermittently with `InvalidClientTokenId`.
   Refresh with `aws sso logout && aws sso login` (or use AWS profiles
   with auto-refresh: `aws configure sso` + `export AWS_PROFILE=<name>`)
   before kicking off multi-stage Pipelines.
