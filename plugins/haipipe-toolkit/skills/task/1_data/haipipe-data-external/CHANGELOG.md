haipipe-data-external — Changelog
=================================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.


## [0.3.5] - 2026-09-29 - a contract field can say when it was added

- `FieldSpec.since` (default 1) names the `contract_version` that added a field. A version built before it lacks the column and reads it as the field's default; a field without `since` stays required, and `since` above `contract_version` is refused (`code/haipipe/external_base/asset.py`, `providers/local_external_store.py`). Builds and `validate_asset.py` stay strict. Asked for by the food session so `ext_food_resolved` can gain `Sugar` without making S20260926 and S20260929 unreadable. `ref/asset-model.md` shows the form.

## [0.3.4] - 2026-09-29 - "lock" is now "release" (JL 260929)

- A named, never rewritten set of asset -> version pins is a **release**: `ExternalStore/_releases/<ReleaseName>.yaml`, yaml key `release:`, `ExternalRelease` / `load_release` / `ExternalAsset(release=...)` in `code/haipipe/external_base/`, command `release`, `fn/fn-release.md`, Block Job `j49_external_releases`. The old words `lock`, `_locks/`, `ExternalLock` are gone; the code still reads `_locks/` when `_releases/` is missing, for a store not moved yet.
- The legacy whole-store `@{tag}` folders (e.g. `@260104R4`), which this skill used to call releases, are now **snapshots**, so "release" has one meaning. The legacy SourceSet column `external_release` keeps its name.
- haipipe-norm `paths.py`: `release_file`, `release_key_column`, `EVENTNORM_RELEASE`; each describe-* member reads it through `<noun>norm/_release.py`.

## [0.3.3] - 2026-09-28 - No content hashes (JL 260928)

- AGENTS.md rule 9: `version.yaml` carries no `sha256` (`ref/asset-model.md`, `ref/concepts.md`, `SKILL.md`, `fn/fn-2-cook.md`, `fn/fn-freeze.md`, `fn/fn-review.md`); a reader ignores a leftover `sha256`. A trimmed endpoint bundle names the original version and kept columns under `trimmed_from`.

## [unreleased] — 2026-09-27

- asset-model § Providers: "A raw ID is translated first": a dialect is a raw ID only one company reads; the SourceFn names it through that company's catalog before the answers lookup, and the answers are keyed by the words. Words such as `Just Carbs` are never dialect (JL 260927, WellDoc b51 release EventNormV3; a vendor's exercise code through its code book, and a gallery types a translated code by its words, JL 260928).

## [0.3.2] — 2026-09-26

- Status: `code/haipipe/external_base/` is built (code 27b1525); only `local_external_store` answers. The Lookup interface section drops "target contract" and matches `client.py`: `ExternalRelease(name, SPACE)`, `encode` defaults to `'ids'`, meta columns `_matched`, `_snapshot_dt`, `_ref_period`, `_version`, `_future_snapshot`.
- Asset names carry the `ext_` prefix (`load_contract` enforces it); every example now uses `ext_npi`, `ext_zip3`, `ext_npi_engagement`. Legacy `@{tag}` folders keep bare names.
- Build Block follows DrFirst `b51_A_externalstore` (regrouped 2026-09-23): one topic Job per group of assets (`j0N_ext_<topic>`), one Task per asset, contract / build / validate / parity / freeze as Runs of that Task, `t99_gallery` per Job, `j48_external_base` unit tests, legacy snapshot audits under `tasks/_legacy/`. Swept through SKILL.md, concepts, fn-2-cook, fn-3-design-chef, fn-freeze, fn-release, fn-parity, fn-refresh, fn-review, and `haipipe-task/ref/hierarchy.md`.
- Serving reference path fixed: `b31_C_model_serving` (was `b03_C_optimal_timing_serving`), here and in `haipipe-data/ref/migration.md`.
- New note: `download`-basis validation compares `ValidFromDT` with raw file dates, so land raw files with their dates kept (`cp -p`, or `cp -c -p` clones for large files).

## [0.3.1] — 2026-09-24

- New `ref/asset-model.md` § Serving: the endpoint bundle: ship only the release's versions, trimmed to the fields in the training SourceSet's `external-dependency.json`, pre-keyed (`__key__` int64, `key_normalized: int64` in `version.yaml`), recorded in `external/_bundle.yaml`; one `ExternalAsset` per process, loaded by the Input2SrcFn's `Warmup(SPACE)` at container start; memory is per gunicorn worker (`MODEL_SERVER_WORKERS`). DrFirst OptTime: first request 17 s -> ~0.5 s, 4.0 -> 1.3 GB per worker.

## [0.3.0] — 2026-09-23

- New `ref/asset-model.md`, the single authority for external data (JL 260923): contract vs data (`asset.yaml` per asset), topic-wise ExternalStore (`<asset>/<version>/` + `version.yaml`, `_releases/`), four providers selected per env (`local_external_store`, `feature_store`, `third_party_api`, `local_service`), record-and-replay (training reads frozen versions only), the `obs_dt` time rule with `ValidFromDT` / `RefPeriod` and `strict` / `nearest_allowed`, the PHI key rule, the `ExternalAsset.lookup` target interface (explicit per-field assignment in SourceFn, shared `enrich_<table>()` with Input2SrcFn), and the b51 build Block layout.
- New commands and fn docs: `freeze`, `release`, `parity`. `cook` builds one immutable version as a b51 Task; `review` adds the contract and time audit; `join` previews the lookup block.
- `@{tag}` snapshots (e.g. `@260104R4`) and the v4 config-driven attach are marked legacy; the "Phase 2 ExternalFn" plan is dropped (builders are b51 Task scripts).
- Asset model also covers: multi-step `chain` lookups, feature-store history (`event_time` = snapshot cutoff, backfill before freezing, no latest-dedup for training), serving `max_staleness`, fallback, and `log_responses`, and the lookup's batching/cache/retry/rate-limit duties; `fn-freeze` gains § Backfill.
- `asset-catalog`, `load`, `refresh` read the topic layout first (refresh = new version + new release, never in place); legacy steps kept.
- Status: model adopted, `code/haipipe/external_base/` not yet built; returned column names provisional until the DrFirst reference implementation. (0.2.0 had no changelog entry.)

## [0.1.2] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.2.0; older entries below keep their original numbers).

## [1.2.0] — 2026-07-08

- skill-diagnose fixes: `code-dev/0-EXTERNAL/` now explicitly a WellDoc-SPACE snapshot everywhere (caveats added to fn-2-cook, fn-3-design-chef, asset-catalog; SKILL caveat trigger corrected to "without code-dev/0-EXTERNAL/" — REACH has a gitignored code-dev/ leftover); `@{YYMMDD}R{N}` tag claim softened (discover via $EXTERNAL_VERSION, e.g. @v1215); patient_id join key stated consistently (cohort joins on patient_id_encoded; external column becomes patient_id_original) in asset-catalog + join-contract; WellDoc SourceSet example names -> placeholders/REACH names; dispatch-table column header fixed ("fn doc to read" — most rows are this skill's own fn/ docs).

## [1.1.0] — 2026-07-04

- wired into the /haipipe-data dispatcher (was orphaned while claiming dispatcher parentage).

## [1.0.0] — 2026-05-31

- baseline metadata added.
