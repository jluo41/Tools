haipipe-data-case — Changelog
=============================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.


## [0.1.3] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.3.0; older entries below keep their original numbers).

## [1.3.0] — 2026-07-08

- skill-diagnose fixes: CaseSet path now shows the optional `@i{i}n{n}` partition level (all real multi-partition stores have it); Recipe/config locations -> job configs/; dead test block removed from templates/config.yaml; `scripts.haistep.case` -> `scripts.haistepcli.case`; CHANGELOG reordered newest-first.
- (2026-07-08 earlier, unversioned at the time — recorded here) builder home repointed from code-dev/ to `03_case_fn_develop_<cohort>/`.

## [1.2.0] — 2026-07-04

- description now claims TriggerFn / CaseFn (TriggerFn builders are 3-Case-WorkSpace a*.py); dead template path fixed.

## [1.1.0] — 2026-06-11

- add Partition Support section — CLI (--num-partitions 0 auto-discover, --num-workers N parallel), embarrassingly parallel pattern, partition discovery via glob.

## [1.0.0] — 2026-05-31

- baseline metadata added.
