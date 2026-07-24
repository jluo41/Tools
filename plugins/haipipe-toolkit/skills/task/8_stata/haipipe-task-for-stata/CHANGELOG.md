haipipe-task-for-stata — Changelog
==================================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.


## [0.2.7] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 2.7.0; older entries below keep their original numbers).

## [2.7.0] — 2026-07-05

### Changed (JL: "还是都允许Resolve-StataExe吧" / "这个东西太细节了…没必要写到skill里吧" / "服务器里当然有")

- dialect A5: Resolve-StataExe now accepted for ANY stage (was: hardcoded preferred for cms, resolver standard for data/reg/case); build-stata Step 3 + review checklist aligned.
- dialect A4 + audit-stata: rangejoin exception KEPT (JL confirmed the server has it) but the server-install commentary stripped as too detailed for skill docs.
- data-stage topology CONFIRMED by JL 2026-07-05 ("case是by year的，然后data是几年combine到一起的"), matching the docs as written; thread closed, nothing pending.

## [2.6.0] — 2026-07-04

- deep-audit fixes: rangejoin carved as the ONE allowed SSC exception in audit-stata Step 4 + dialect A4 (both flat-banned it while build/checklist C1/server env authorize it); build-stata $stata rules aligned to dialect A5 (Resolve-StataExe standard for data/reg/case, hardcoded for cms); data stage no longer described as year-orchestrated in build/scaffold (SELF-ORCHESTRATING per SKILL 2.3.0 topology); checklist F2/F3 scoped to runners (results/ still carries config_snapshot.do + manifest.json per L3/L8/B3); dialect + plan-stata RUNNAME grammars aligned to SKILL 2.4.0 (case source dim, reg full grid); /cms-server-checklist skill refs -> SERVER CHECK mode; Gate-1 comment = local synth run; retired haipipe-task-logging pointer removed.

## [2.5.0] — 2026-07-04

- review sweep: 4 stage plan-sample schema headers task/haipipe-workflow (were dead project/ paths); fn/audit-stata.md + fn/plan-stata.md relative hub paths ../../../haipipe-task (were off-by-one).

## [2.4.0] — 2026-06-10

- align reg stage to D01 ground truth — add run-ps1-reg-template.ps1 + config-seed-reg-run.do; rewrite config-seed-reg.do (data path only, controls in workers); fix RUNNAME to include cohort+pairing+source; document DID policy as reg-stage concern (not C-stage); make describe optional for reg; add Step 3b to build-stata (reg runner authoring); fix workflow-plan-sample-reg.yaml (DID policy phase, correct skill name).

## [2.3.0] — 2026-06-10

- align templates+contract with production — add topology families (orchestrated vs self-orchestrating) to dialect; soften A5 (accept Resolve-StataExe); scope B2/B3 by topology; expand config-seed-data to production size (~80 globals); add run-data-runner-template.ps1; data-stage synth/real source dimension; STATATMP in orchestrator template; match-existing mode in build-stata.

## [2.2.0] — 2026-06-10

- fix 6 issues — rewrite 4 plan samples to match real pipeline phases; remove SSC from build-stata; fix scaffold config extension; update orchestrator template to working version (<=30 lines); fix ~15-><=30 budget; remove helper function references from build-stata.

## [2.1.0] — 2026-06-10

- absorb cms-server-checklist from 0_utils; add server check mode with three-gate protocol.

## [2.0.0] — 2026-06-10

- unified — absorb all 4 child specialists (cms/case/data/reg) into one skill; no child delegation.

## [1.2.0] — 2026-06-09

- unwrap prose; fix agent names to haipipe-task-{creator,reviewer}-agent; add lifecycle paragraph.

## [1.1.0] — 2026-06-08

- add metadata; workflow lifecycle compatible.

## [1.0.0] — 2026-05-31

- baseline.
