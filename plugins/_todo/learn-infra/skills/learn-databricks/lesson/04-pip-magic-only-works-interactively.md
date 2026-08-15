# Lesson 04: %pip Magic Only Works Interactively, Not in Job API

## The Problem

Databricks notebooks support `%pip install` magic commands for installing Python packages. This works when you run the notebook **interactively** in the Databricks UI:

```python
# MAGIC %pip install pandas>=2.0 xgboost optuna
```

However, when the same notebook runs via the **Job API** (`databricks jobs submit`, `databricks jobs run-now`, or Databricks Asset Bundles), the `%pip` magic is **silently ignored**. No error, no warning — the packages simply aren't installed.

## Why It Happens

- `%pip` is a Databricks-specific "magic command" that is interpreted by the notebook UI layer
- The Job API executes notebook cells as raw Python — it doesn't process magic commands
- `# MAGIC %pip ...` lines are treated as comments by the Python interpreter
- This is a fundamental architectural difference between interactive and batch execution modes

## The Solution

### For Job API / batch execution:

1. **Use the right Runtime** — choose a Runtime that already includes the packages you need (Lesson 03)
2. **Use `subprocess` for in-notebook install** (works but fragile):
   ```python
   import subprocess
   subprocess.check_call(["pip", "install", "tqdm"])
   ```
3. **Use Libraries API** before job submission:
   ```bash
   databricks libraries install --cluster-id <id> --pypi-package tqdm
   ```

### For interactive mode:
- `%pip install` works as expected — restarts the Python interpreter after install

## How to Detect Which Mode You're In

```python
ON_DATABRICKS = False
try:
    _ = dbutils
    ON_DATABRICKS = True
except NameError:
    pass

# But this doesn't distinguish interactive vs job API.
# Both have dbutils available.
```

There is no clean way to detect "am I in interactive mode vs Job API mode" — the safest approach is to not rely on `%pip` at all and use a Runtime that has what you need.

## When to Apply

- Any time you design notebooks that will run both interactively AND as jobs
- **Rule of thumb**: never put `%pip install` as your only installation strategy. Always have a fallback (right Runtime, libraries API, or subprocess).
