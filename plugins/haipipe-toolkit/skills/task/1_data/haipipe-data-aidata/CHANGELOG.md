haipipe-data-aidata — Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [1.4.0] — 2026-07-08

- skill-diagnose fixes: documented store layout corrected from `{aidata_name}/@{aidata_version}/` to the real `{ParentSetName}/@v{N}AIData-{aidata_name}/` (concepts + SKILL + template; verified against all 4 on-disk sets); split-name note added (config-driven; shipped MIMIC uses train/validation/test); Recipe location -> task-folder configs/; dead test block removed; `scripts.haistep.aidata` -> `scripts.haistepcli.aidata`; CHANGELOG reordered newest-first.
- ref/worked-example.md REBASED from the WellDoc SMS RCT to MIMIC-IV mortality — every claim now checkable against the real `4-AIDataStore/MimicIV31_MimicAdmissionEntry/@v0AIData-MimicMortality/` asset (JL: "ok, go ahead and fix all of them" — approved recommended option A).
- (2026-07-08 earlier, unversioned at the time — recorded here) builder home repointed from code-dev/ to `04_aidata_fn_develop_<cohort>/`.

## [1.3.0] — 2026-07-05

### Changed (JL: "这些东西要general，不是固定到一个项目的。不要出现具体的名字或者什么的")

- The 70+ line OptTime v2 fu7d worked example moved out of SKILL.md into ref/worked-example.md (SKILL keeps a 10-line digest + pointer; the generic blank template stays in SKILL). Employer name scrubbed from the example. SKILL.md now loads ~250 lines instead of 319 at invocation.

## [1.2.0] — 2026-07-04

- dead code/hainn/algo/ hand-off path -> workspace-neutral wording; dead template path fixed.

## [1.1.0] — 2026-06-11

- add Multi-partition Mode section — auto-discover CaseSet partitions via record_set_name + CaseArgs config, streaming HF Dataset merge, --use-cache; remove stale 0_data_nb reference.

## [1.0.0] — 2026-05-31

- baseline metadata added.
