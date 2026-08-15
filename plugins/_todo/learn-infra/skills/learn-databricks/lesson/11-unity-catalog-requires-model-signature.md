# Lesson 11: Unity Catalog Requires a Model Signature

## The Problem

When registering an MLflow model to Unity Catalog via `mlflow.register_model()`, registration fails if the model has no signature:

```
MlflowException: Model passed for registration did not contain any
signature metadata. All models in the Unity Catalog must be logged
with a model signature containing both input and output type
specifications.
```

## Why It Happens

Unity Catalog enforces that every registered model has an input/output schema. This is a hard requirement — there's no flag to skip it. MLflow Model Registry (non-UC) doesn't enforce this, so code migrated from classic MLflow will hit this.

## The Fix

Always pass a `signature` when calling `mlflow.pyfunc.save_model()`:

```python
from mlflow.models.signature import ModelSignature
from mlflow.types.schema import Schema, ColSpec

signature = ModelSignature(
    inputs=Schema([ColSpec('string', 'payload')]),
    outputs=Schema([ColSpec('string', 'result')]),
)

mlflow.pyfunc.save_model(
    path=save_path,
    python_model=model,
    artifacts=artifacts,
    signature=signature,   # ← required for UC
)
```

## When to Check

- Before any `mlflow.register_model()` call targeting a UC name (`catalog.schema.model`)
- When migrating from classic MLflow Registry to Unity Catalog

## Source

REACH-ADHD endpoint deployment, 2026-06-26. Issue #11 in DATABRICKS_ISSUES.md.
