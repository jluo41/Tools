# Lesson 09: Don't Install 10+ Packages via Libraries API on Small VMs

## The Problem

When you install multiple packages via the Databricks Libraries API on a small VM (e.g., Standard_DC4as_v5 with 4 cores / 16 GB), the driver process can crash:

```
Error: Could not reach driver
```

This happens because:
1. The Libraries API triggers a pip install on the driver node
2. Pip resolution and compilation of packages like numpy, scipy, xgboost is CPU and memory intensive
3. On a 4-core VM, the pip process competes with the Spark driver for resources
4. The driver's JVM runs out of memory or the process gets OOM-killed

## The Sequence That Crashed

```bash
# Installing these 10 packages crashed the DC4as_v5 driver:
databricks libraries install --cluster-id <id> --pypi-package pandas
databricks libraries install --cluster-id <id> --pypi-package numpy
databricks libraries install --cluster-id <id> --pypi-package xgboost
databricks libraries install --cluster-id <id> --pypi-package optuna
databricks libraries install --cluster-id <id> --pypi-package shap
databricks libraries install --cluster-id <id> --pypi-package scikit-learn
databricks libraries install --cluster-id <id> --pypi-package scipy
databricks libraries install --cluster-id <id> --pypi-package lightgbm
databricks libraries install --cluster-id <id> --pypi-package pyarrow
databricks libraries install --cluster-id <id> --pypi-package datasets
```

After the driver crash, the cluster becomes unresponsive and must be restarted. Sometimes the crash corrupts the cluster state and you need to create a new cluster entirely.

## The Solution

### For ML packages: Use ML Runtime (Lesson 03)

Runtime 17.3 LTS ML pre-installs all of the above. Zero libraries API calls needed.

### For small utility packages: Libraries API is safe

```bash
# These are safe — small, pure Python, no compilation:
databricks libraries install --cluster-id <id> --pypi-package tqdm
databricks libraries install --cluster-id <id> --pypi-package pyyaml
databricks libraries install --cluster-id <id> --pypi-package requests
```

### Rule of thumb

| Package type | Libraries API safe? | Alternative |
|-------------|-------------------|-------------|
| Pure Python, small (tqdm, pyyaml) | ✅ Yes | — |
| Large compiled (numpy, scipy) | ❌ No | Use correct Runtime |
| ML frameworks (xgboost, lightgbm) | ❌ No | Use ML Runtime |
| Many packages (5+) at once | ⚠️ Risky | Use ML Runtime |

## Why Small VMs Are Especially Vulnerable

- DC4as_v5 has 16 GB total RAM, but ~6-8 GB is consumed by the Spark driver JVM + system
- That leaves only ~8 GB for pip compilation
- Compiling numpy + scipy + xgboost concurrently can peak at 10+ GB
- Larger VMs (8+ cores, 32+ GB) can handle more library installs, but ML Runtime is still better

## When to Apply

- Any Databricks cluster on a VM with ≤ 4 cores
- When you need more than 3-4 packages beyond what the Runtime provides
- **Default strategy**: pick ML Runtime → install 0-2 small packages via Libraries API
