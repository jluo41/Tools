haipipe-data — Migration notes for other SPACEs
================================================

What a SPACE that shares these skills (REACH-SPACE, WellDoc SPACE, a fresh
clone) does to follow a change made in another SPACE. Newest first. Each
note says what changed, whether anything breaks, and the steps to adopt it.

---

2026-09-24 · Fn versions and the external serving bundle
=========================================================

From: DrFirst-SPACE (OptTimeR1 Extended). Skills: haipipe-data 0.3.2,
-source 0.3.2, -record 0.3.1, -case 0.3.2, -external 0.3.1,
haipipe-task-for-data 0.8.4. Code: haipipe-code `27b1525` on `code-drfirst`.

What changed
------------

1. **Fn versions.** Source, Record and Case Fns can share one folder,
   `code/haifn/fn_<stage>/<fn_version>/`. A Run config selects it with a
   top-level `fn_version:`, and `haipipe.base.fn_dir()` resolves it
   (`ref/0-overview.md` § Fn Versions).
2. **External serving bundle.** An endpoint ships only its lock's external
   versions, trimmed to the fields training looked up and pre-keyed
   (`key_normalized: int64`), and loads them once per worker at warmup
   (`haipipe-data-external/ref/asset-model.md` § Serving: the endpoint bundle).

Does anything break?
--------------------

No. Without `fn_version:` every loader reads the flat folders as before, and
a version card without `key_normalized` loads as before.

One trap: **code older than `27b1525` ignores `fn_version:` silently** and
loads the flat Fns. Never set `fn_version:` in a SPACE whose `code/` lacks
`haipipe.base.fn_dir`. Check first:

```bash
grep -n "def fn_dir" code/haipipe/base.py    # must print one line
```

Steps: every SPACE
------------------

1. Pull the skills and reinstall, then restart the agent session:
   ```bash
   git -C Tools pull --ff-only        # or ../Tools-SPACE on JL's main machine
   Tools/install.sh --no-marketplace --project "$(pwd)"
   ```
2. Bring `code/` up to `27b1525` or later. On `code-drfirst`, pull. On
   another branch, merge or cherry-pick `27b1525`. It touches only the
   framework (`haipipe/base.py`, the five Fn loaders, the haistep bootstrap,
   the four manifests, `endpoint_base`, `external_base/`, `tuner_xgboost.py`,
   `case_utils.py`) plus DrFirst's own generated Fns, which another project
   never loads.
   ```bash
   git -C code fetch origin && git -C code cherry-pick 27b1525
   ```
3. Check a flat Run still works: cook one existing small dataset stage and
   compare its row counts with the last Result. Nothing else is needed to
   stay on the flat folders.

Steps: moving a dataset onto a version (optional)
-------------------------------------------------

Do this when a dataset's SourceFn output (its `ProcName_to_ProcDf` shape)
changes, or to freeze a dataset's Fns apart from other datasets'.

1. Name the version `v<Label><yymmdd>` (DrFirst: `vDfExt260923`).
2. For each builder the dataset uses (SourceFn, HumanFn, RecordFns,
   TriggerFn, CaseFns), check that it reads `fn_version_from_config()` and
   writes through `fn_dir()` (pattern: `ref/0-overview.md` § Fn Versions).
   Then add a build Run whose config says `fn_version: <version>`, next to
   the flat `r01_regen_fn`. Run them. Never copy or hand-edit generated Fns.
3. Add `fn_version: <version>` to every cook Run config of the `j5N` Job in
   `b01`, `b02` and `b03`, and cook in order.
4. Check the manifests say so (only sets cooked with `27b1525` or later
   carry the field):
   ```bash
   find _WorkSpace/1-SourceStore _WorkSpace/2-RecStore _WorkSpace/3-CaseStore \
     -path '*<dataset>*' -name manifest.json -exec grep -H '"fn_version"' {} +
   ```
5. An endpoint Input2SrcFn that calls the SourceFn's `enrich_*` blocks loads
   it from `fn_source/<version>/` by name. Rebuild the endpoint package
   after the Fns change.

Steps: an endpoint that ships external data (optional)
------------------------------------------------------

1. Stage `external/` from the training SourceSet's `external-dependency.json`
   (trim + pre-key), not by copying the ExternalStore. Reference script:
   DrFirst-SPACE `examples-3-model/Project-ExpModel-OptTime/tasks/b03_C_optimal_timing_serving/j01_opttime_endpoint_package/t01_endpoint_package/scripts/stage_external_bundle.py`.
2. Give the Input2SrcFn a per-process asset cache and a `Warmup(SPACE)` that
   runs one lookup per shipped asset.
3. Set `MODEL_SERVER_WORKERS` so that workers × peak memory per worker fits
   the instance. Check the container log shows the warmup and no OOM kills
   under a concurrent load test.
4. Scores that differ between local and the serving image with the same
   inputs: retrain or re-save with `27b1525`'s `portable_base_score` (XGBoost
   3.x vs 2.0.x `base_score`), then compare exactly again.

Also still pending in DrFirst-SPACE (no action for other SPACEs yet)
--------------------------------------------------------------------

- Task folders still named `t01_*_materialize`; the rename to "cook" is not
  decided. The skills say "cook" in prose and keep the folder names.
