# Lesson 02: Init Scripts Blocked — Use Libraries API Instead

## The Problem

Databricks workspace admins can enforce an **init script allowlist**. When you attach a cluster-scoped init script (e.g., `init_reach_adhd.sh` on a Unity Catalog Volume), the cluster fails to start with:

```
INVALID_PARAMETER_VALUE: init scripts not in allowlist
```

This is a workspace security policy — you cannot override it without admin privileges.

## The Solution

Don't use init scripts. Instead, install packages via one of these alternatives:

### Option A: `databricks libraries install` (CLI/API)

```bash
databricks libraries install \
  --cluster-id 0620-193941-dx4kf6oy \
  --pypi-package tqdm \
  --profile cdhai-new
```

- Works for simple, lightweight packages (tqdm, pyyaml, etc.)
- Installs at the cluster level — available to all notebooks
- **Caveat**: installing many packages at once can crash the driver on small VMs (see Lesson 09)

### Option B: Use a Runtime that pre-installs what you need

- Runtime 17.3 LTS ML includes xgboost, optuna, shap, scikit-learn, etc.
- This is the best approach for ML workloads — zero installation needed

### Option C: `%pip install` in notebook cells

- Works in **interactive mode only** (Databricks notebook UI)
- **Does NOT work** in Job API / `databricks jobs submit` (see Lesson 04)

## Why Init Scripts Get Blocked

Databricks workspaces with Unity Catalog or enterprise security policies restrict init scripts to prevent:
- Arbitrary code execution at cluster startup
- Installation of unapproved software
- Security policy bypasses

The allowlist is managed by workspace admins, not cluster creators.

## When to Apply

- Any Databricks workspace where you don't control the init script allowlist
- Default strategy: pick the right Runtime + libraries API for stragglers
