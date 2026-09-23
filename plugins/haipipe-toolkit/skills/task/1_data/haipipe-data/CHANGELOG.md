haipipe-data — Changelog
========================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.

## [0.3.1] — 2026-09-23

- Routing: external-only verbs `freeze`, `lock`, `parity`, `join`, `refresh` and external keywords (asset, lock, feature store, vendor API, obs_dt) route to `haipipe-data-external`.
- Overview principle 7 and the ExternalStore tree follow the external asset model (per-asset contract and versions, locks, explicit SourceFn lookup, frozen versions in training); external specialist line lists freeze/lock/parity.

## [0.3.0] — 2026-09-23

- PHI SPACE note: no `.ipynb`, `.cmd` tickets only; stage skills 0.3.0/0.2.0 carry the REACH PD2D b01-b04 rules (JL 260923).

## [0.2.1] — 2026-09-23

- Builder locations now follow the Block/Job rule: each stage skill names its exact Task path (topic Job `j01`-`j49` for Fns, dataset Job `j51`-`j99`); `ref/0-overview.md` § Current Builder Structure has the Fn kind to Block and Job table and drops the wrong `jNN_<logic_version>` line. AIData is where raw datasets merge (JL 260923). `fn/fn-3-design-chef.md` (BUILDER HOME, discover globs, stage table), `fn/fn-review.md` (path patterns) and `README.md` swept off the retired `NN_<stage>_fn_develop_*` folders.


## [0.1.3] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.3.0; older entries below keep their original numbers).

## [1.3.0] — 2026-07-08

- skill-diagnose fixes: dead `scripts.haistep.*` module paths -> `scripts.haistepcli.*` (SKILL + fn-2-cook; the old module no longer exists); broken `haistep-*` console-script examples replaced with `python -m` form; stale `ProjD-EHR-1-Mimic` worked-example path -> `Project-EHR-Mimic`; repo-root `config/` references retired everywhere (README, 0-overview snapshot section, fn-2-cook, fn-3-design-chef, fn-4-design-kitchen, fn-review path patterns -> `**/configs/**/*.yaml`); fn-3-design-chef body swept to BUILDER HOME / fn_develop-first and now points at the `code/scripts/haibuilder/` seed library; fn-2-cook template-path contradiction (line 22) aligned; frontmatter description now lists all 7 specialists.
- Cross-stage dashboard: external/remote exclusion made explicit (JL: "ok, go ahead and fix all of them" — approved recommended option: keep 5-stage fan-out + written exclusion note).

## [1.2.0] — 2026-07-04

- deep-audit fixes: Fn-type ownership corrected (HumanFn=Stage 2 with RecordFn, TriggerFn=Stage 3 with CaseFn — dispatcher had them one stage early, contradicting every fn/ doc and shipped template); haipipe-data-external + haipipe-data-remote WIRED into the dispatcher (specialists list, keyword map, aliases — both existed on disk unrouted); README file map rewritten (ref/1-4.md + templates/N-stage/ were fiction); fn-2-cook template paths -> specialist-local templates/config.yaml; fn-2-cook CaseArgs schema aligned to the shipped case template (case_set_version at CaseArgs level, operation blocks); 0-RawStore -> 0-RawDataStore; fan-out summary 5-line; 0-rawdata alias -> raw dashboard Panel 0.
- CONFIRMED by JL 2026-07-05, both arbitrations: Fn ownership (JL: "human fn should go to the Stage 2: Source to Record. it should be in the Record Stage.") and external/remote wiring (JL: "yes, please do for them."). Review thread archived here and removed from SKILL.md.

## [1.1.0] — 2026-06-11

- update notebook section — retire 0_data_nb, add partition params (NUM_PARTITIONS/PARTITION_INDEX/NUM_WORKERS), CLI alternative, MIMIC-IV worked example; add partition mode to fn-2-cook.md for Record/Case/AIData.

## [1.0.0] — 2026-05-31

- baseline metadata added.
