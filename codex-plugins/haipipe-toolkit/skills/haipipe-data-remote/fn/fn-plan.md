fn-plan: Dependency-aware multi-asset plan
===========================================

Composes a sequence of `pull` operations to bring a cohort up to a
specified pipeline stage. Resolves dependencies (Source -> Record ->
Case -> AIData), plus any external assets the cohort references.

Phase 1 implementation: best-effort dependency resolution by name
matching. Always shows the proposed plan; never executes silently.

---

Step 1: Parse args
-------------------

Required:
  --for cohort=<name>          target cohort name (e.g. 20250616_JunSMSTest)

Optional:
  --through stage=<N>          stop at stage N (1-6). Default: 4 (AIData).
  --skip-externals             do not pull ExternalStore assets

---

Step 2: Resolve dependencies (best-effort)
-------------------------------------------

Use `hai-remote-sync --pull --dry-run --path` against each candidate
store to check what exists on remote that matches the cohort name.

```bash
# Source: look for {cohort}/...
hai-remote-sync --pull --path 1-SourceStore/{cohort} --dry-run

# Record: look for {cohort}_v*RecSet/
hai-remote-sync --pull --path 2-RecStore --dry-run | grep "{cohort}_"

# Case: built on top of a RecSet -- match by RecSet name prefix
hai-remote-sync --pull --path 3-CaseStore --dry-run | grep "{cohort}"

# AIData: more loosely tied to cohort name -- ask the user if multiple match
hai-remote-sync --pull --path 4-AIDataStore --dry-run | grep "{cohort}"
```

Build the dependency list:

```
[
  ('1-SourceStore', '{cohort}/...'),
  ('2-RecStore',    '{cohort}_v1RecSet/...'),
  ('3-CaseStore',   '{cohort}_v1RecSet/@v1CaseSet-XYZ/'),
  ('4-AIDataStore', '...'),
]
```

If multiple matches at a stage (e.g. v1RecSet AND v2RecSet), ask the
user which to include.

For externals: read the README of each Source/Record asset to find
external dependencies declared in the manifest. (If no manifest
declares them, ask the user explicitly.)

---

Step 3: Estimate sizes
-----------------------

For each dependency, parse the dry-run output to compute total bytes.
Sum across the plan.

```
Plan size estimate: {N_files} files, {total_size}.
At assumed throughput, this will take ~{minutes} min.
```

(Throughput estimate is informational only -- actual time depends on
network and remote-side concurrency.)

---

Step 4: Show plan and confirm
------------------------------

```
Plan: pull cohort {cohort} through stage {N}

Dependencies resolved:
  1. 1-SourceStore/{cohort}/...                      {size}   ✗ missing locally
  2. 2-RecStore/{cohort}_v1RecSet/...                {size}   ✗ missing locally
  3. 3-CaseStore/.../@v1CaseSet-.../                 {size}   ✗ missing locally
  4. ExternalStore/@260104R4/{npi, ndc, zip5}        {size}   ✓ local but stale

Will execute (in order):
  hai-remote-sync --pull --source --name {cohort}
  hai-remote-sync --pull --record --name {cohort}_v1RecSet
  hai-remote-sync --pull --case   --name ...
  hai-remote-sync --pull --external

Total: {N} pulls, ~{total_size}, est ~{minutes} min.

Proceed? (yes / dry-run-only / cancel)
```

  yes            -> Step 5
  dry-run-only   -> exit (the dry-runs in Step 2 stay valid as the diagnostic)
  cancel         -> exit

---

Step 5: Execute the plan
-------------------------

For each step, delegate to `fn-pull.md` (which does its own per-step
dry-run + confirm). If the user does not want to confirm each step
separately, accept `--yes` upfront to skip per-step confirms (but
keep per-step dry-run logs).

If any step fails, pause and ask:

  - retry
  - skip and continue
  - abort

NEVER continue silently past a failure.

---

Step 6: Return
---------------

```
status:           ok | partial | failed
cohort:           {cohort}
through_stage:    {N}
pulled:           [list of (store, name, bytes)]
failed:           [list with errors]
elapsed:          {seconds}s
next:             "/haipipe-data <stage> load   (verify the cohort)"
```

---

MUST NOT
---------

- Do NOT execute pulls without showing the full plan first.
- Do NOT silently choose between alternative versions (v1 vs v2 RecSet)
  -- always ask.
- Do NOT pull ExternalStore for a different release than the cohort
  expects without flagging the version mismatch.
- Do NOT pass `--sync` to any hai-remote-sync call.
