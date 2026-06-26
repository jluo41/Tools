# Lesson 03: Use ML Runtime for ML Packages

## The Problem

Standard Databricks Runtimes (15.4, 16.4) don't include ML packages like xgboost, optuna, shap, or lightgbm. Installing them post-hoc is unreliable:

- Init scripts → blocked by allowlist (Lesson 02)
- `%pip install` → doesn't work in Job API (Lesson 04)
- Libraries API → crashes the driver when installing 10+ packages on small VMs (Lesson 09)

## The Solution

Use **Runtime 17.3 LTS ML** (`17.3.x-cpu-ml-scala2.13`).

ML Runtimes come with these packages pre-installed:

| Package | Standard Runtime | ML Runtime |
|---------|-----------------|------------|
| xgboost | ❌ | ✅ |
| lightgbm | ❌ | ✅ |
| optuna | ❌ | ✅ |
| shap | ❌ | ✅ |
| scikit-learn | ✅ | ✅ |
| mlflow | ✅ | ✅ |
| pandas | ✅ (version varies) | ✅ 2.x |
| numpy | ✅ | ✅ |
| scipy | ✅ | ✅ |
| pyarrow | ✅ | ✅ |

## Runtime Version Comparison

```
Runtime 15.4 LTS     → pandas 1.5.3, Python 3.11, no ML pkgs
Runtime 16.4 LTS     → pandas 2.2.x, Python 3.12, no ML pkgs
Runtime 17.3 LTS ML  → pandas 2.x,   Python 3.12, ALL ML pkgs ← USE THIS
```

## When to Apply

- **Always use ML Runtime** when your pipeline includes model training (Stage 5) or anything that imports xgboost/lightgbm/optuna
- For data-only stages (Stages 1-4), standard Runtime 16.4+ works fine — but there's no downside to using ML Runtime for everything
- ML Runtime is available in both CPU and GPU variants. Use `-cpu-ml-` for XGBoost/LightGBM workloads; GPU variant only needed for deep learning

## The Runtime Naming Convention

```
{version}.x-{gpu|cpu}-ml-scala{2.12|2.13}

Example: 17.3.x-cpu-ml-scala2.13
         ^^^^   ^^^  ^^
         |      |    |
         |      |    ML = includes ML packages
         |      CPU (no GPU driver)
         Version 17.3 LTS
```
