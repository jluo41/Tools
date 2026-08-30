haipipe-data-record — Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.


## [0.1.3] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.3.0; older entries below keep their original numbers).

## [1.3.0] — 2026-07-08

- skill-diagnose fixes: Recipe/config locations -> job configs/; dead `test/test_haistep` block removed from templates/config.yaml; `scripts.haistep.record` -> `scripts.haistepcli.record`; CHANGELOG reordered newest-first.
- (2026-07-08 earlier, unversioned at the time — recorded here) builder home repointed from code-dev/ to `02_record_fn_develop_<cohort>/`.

## [1.2.0] — 2026-07-04

- ownership corrected: Stage 2 = HumanFn / RecordFn (was RecordFn / TriggerFn, contradicting its own ref/concepts.md); dead template path fixed.

## [1.1.0] — 2026-06-11

- add Partition Support section — CLI (--num-partitions, --use-cache), patient_ids predicate pushdown via Ptt.parquet, @i{i}n{n} output naming.

## [1.0.0] — 2026-05-31

- baseline metadata added.
