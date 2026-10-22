haipipe-task-for-agent — Changelog
==================================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.


## [0.2.0] · 2026-10-21 · One folder per Run, and a Type contract

- `SKILL.md` opens with `## Type contract` (the keys of haipipe-task `ref/types.md`), current layout only.
- Every page states the current layout: a Run is `runs/rNN_<run>/` with its ticket `rNN_<run>.sh`, `config.yaml`,
  card `run.yaml` (`role: trial | make`) and `result/`; the Result is `$OUTPUT_ROOT/<task>/runs/<run>/result/`.
  Prompts sit in `scripts/config/prompts/`. The plan sample targets `work/`. The flat layout is named only as what
  a Block not yet moved still has.

## [0.1.4] · 2026-10-09 · Theme folders are singular

- Docs name the singular Theme folders (s01-D29, JL 261007): `work/`, `discovery/`, `paper/`, `insight/`,
  `design/`, `labeling/`, `ideation/`; the older plural names still read.

## [0.1.3] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.3.0; older entries below keep their original numbers).

## [1.3.0] — 2026-07-04

- fn/scaffold Step 6 no longer denies the engine (/haipipe-task-llm-engine named); CHANGELOG reordered newest-first.

## [1.2.0] — 2026-07-04

- review sweep: plan-sample schema header + reviewer name + relative hub paths + letter F as default; body now names /haipipe-task-llm-engine as the domain's LLM call engine.

## [1.1.0] — 2026-06-09

- unwrap prose; fix agent names; add 4-stage lifecycle paragraph.
## [1.0.0] — 2026-05-31

- baseline metadata added.

