fn-lock: Pin asset versions for a SourceFn
==========================================

Writes `_WorkSpace/ExternalStore/_locks/<LockName>.yaml`: which version of
each asset one SourceFn uses (`ref/asset-model.md` § ExternalStore layout).
A lock is a list of pins, like requirements.txt, never a copy of data.

Runs as a b51 Task: `j49_external_locks/t01_lock_<LockName>/`.

---

Step 1: List what the SourceFn looks up
---------------------------------------

Read the SourceFn builder's lookup blocks (`enrich_<table>()`): every asset
name it calls.

---

Step 2: Choose one version per asset
------------------------------------

For each asset:

```bash
ls _WorkSpace/ExternalStore/<asset>/
cat _WorkSpace/ExternalStore/<asset>/<version>/version.yaml
```

- The version must have a passing `t03_validate` Run.
- A live-serving asset also needs a passing `t04_parity` Run.
- Check every cohort the SourceFn serves: for temporal assets
  (`leak_policy: strict`), a version whose `ValidFromDT` is after the cohort's
  observation window leaves those rows unmatched. State which cohorts are
  affected.

---

Step 3: Write the lock
----------------------

```yaml
lock: OptTimeR1v1
written: 2026-09-23
assets:
  zip3: "2025"
  npi: NPPES202507
  npi_engagement: S20260104
note: "first lock for the OptTime R1 SourceFn"
```

A published lock is immutable. A change is a new lock name.

---

Step 4: Record
--------------

The SourceFn builder names the lock; its `external-dependency.json` repeats
the lock and the resolved versions per asset.
