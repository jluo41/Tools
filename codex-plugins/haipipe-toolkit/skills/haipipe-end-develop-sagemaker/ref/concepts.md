haipipe-end-develop-sagemaker — Concepts
=========================================

SageMaker training conventions for this project. Read by the SKILL.md
before running any verb.

---

Backing repo
------------

`platform-sagemaker-training/` (sibling of this checkout) is the platform
layer this skill wraps. Its layout:

```
platform-sagemaker-training/
├── docker/                              training image Dockerfile + entry
├── scripts/
│   ├── build_docker/
│   │   └── build_docker_training.py     build + push training ECR image
│   ├── build_training_pipeline/
│   │   ├── build_training_pipeline.py   compose 3-step Pipeline
│   │   ├── script_process.py            PreprocessStep handler
│   │   ├── script_train.py              TrainingStep handler
│   │   └── script_reorganize.py         ReorganizeStep handler
│   └── run_training_pipeline/
│       ├── run_train_local_system.py    --stage system  (local Python)
│       ├── run_train_local_docker.py    --stage docker  (local container)
│       ├── run_process_local_system.py  preprocessing-only local test
│       ├── run_process_local_docker.py  preprocessing-only local test (Docker)
│       └── run_training_pipeline.py     --stage pipeline (full SageMaker)
├── config/                              project YAML configs
└── opt_ml/, opt_ml_processing/          local-test output mounts
```

The 3-stage testing ladder (system → docker → pipeline) mirrors
`platform-sagemaker-inference`'s endpoint testing ladder. Always promote
upward — fix breakages at the lowest rung first.

---

Pipeline shape
--------------

```
Preprocess  →  Train  →  Reorganize          (linear)
                            ║
                            ╚══════════►  RegisterModel  (parallel branch)
```

PreprocessStep:
  - Input:  raw S3 dump for the dataset(s) named in the YAML
  - Output: AIData under `workspace/{version}/4-AIDataStore/` with smart
            cohort partitioning

TrainingStep:
  - Input:  AIData
  - Output: model + Endpoint_Set bundle as a single tarball

ReorganizeStep:
  - Unpacks the training tarball into the canonical paths:
        workspace/{version}/5-ModelInstanceStore/<instance_name>/
        workspace/{version}/6-EndpointStore/<endpoint_set>/
  - Also writes `model.tar.gz` next to the Endpoint_Set for SageMaker deploy.

RegisterModel:
  - Registers the trained artifact into the SageMaker Model Registry under
    `--model-package-group-name <ModelPackageGroupName>`.
  - Uses `PipelineSession` so model properties (S3 URI, image URI) flow
    through pipeline parameters at execution time, not build time.
  - Runs in parallel with Reorganize.

---

Required AWS surface
--------------------

  - IAM role:       SageMakerExecutionRole (or project-equivalent) with
                    s3:*, logs:*, ecr:GetDownload* permissions
  - ECR image:      `<account>.dkr.ecr.<region>.amazonaws.com/docker-training:<tag>`
  - S3 bucket:      project-configured workspace bucket
  - ModelPackageGroup: created on first `develop` if absent

Default region in this project: us-east-2. Override per-config.

---

Config schema (excerpt)
-----------------------

The YAML passed to `develop` typically defines:

```yaml
pipeline_name: ProcessAndTrainPipeline
docker_image: <ECR URI of training image>
role:         <IAM role ARN>
region:       us-east-2
model_package_group_name: <name>

workspace:
  version: <version-tag>
  bucket:  <s3-bucket>

datasets:    [...]
cohort_partitions: ...
training:
  hyperparameters: ...
  instance_type: ml.m5.4xlarge
  instance_count: 1
```

Refer to `config/config_raw_to_endpoint_ctr_r20.yaml` for a full example.

---

Output contract
---------------

After a successful `develop` run, the deploy specialists can consume EITHER:

  (a) The local Endpoint_Set under `_WorkSpace/6-EndpointStore/<endpoint_set>/`
      (synced from S3 by the project's standard sync), OR

  (b) The registered ModelPackage ARN directly (SageMaker-native consumers
      use the registry; Databricks / local consumers use the synced folder).

The deploy specialists do not need to know which path was used — both produce
the same artifact bytes.

---

Failure modes
-------------

  - "Image not found in ECR" → run `build_docker_training.py` first.
  - "Role assumption failed" → check IAM trust policy; SageMaker must be a
    trusted entity on the execution role.
  - "ModelPackageGroup does not exist" → first run creates it; if creation
    fails, IAM is missing `sagemaker:CreateModelPackageGroup`.
  - PreprocessStep OOM → increase `processing.instance_type` in the YAML.
  - TrainingStep timeout → check `training.max_run` and `instance_count`.
  - RegisterModel failed but Pipeline succeeded → re-run `aws sagemaker
    create-model-package` from the Pipeline output ARN; do NOT re-run the
    whole pipeline.

---

Cross-skill boundaries
----------------------

```
              ┌─ /haipipe-nn modelset           (Stage 5 code: defines what to train)
              │
develop ──────┤
              │
              └─ /haipipe-end-endpointset       (Stage 6 artifact contract: defines layout)
                                                  ▲
                                                  │ produces
                                                  │
                          ┌────  -deploy-sagemaker
                          ├────  -deploy-databricks
                          ├────  -deploy-local
                          └────  -deploy-mlflow
                                  consumes
```

This skill is the **left side** of that diagram (build). Deploy specialists
are the **right side** (serve). They share the Endpoint_Set artifact.
