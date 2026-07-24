paper-rebuttal — Changelog
==========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [0.1.1] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.1.0; older entries below keep their original numbers).

## [1.1.0] — 2026-07-14 — LAW 1: the rebuttal session DISPATCHES, it does not author the bank

`fn/fn-task.md` Step 5 told the paper session to "create task folders in the project's tasks/ directory" and name them by the project's convention — the examples given (`B7_train_fairness_aware`, `C10_eval_cohort_stratification`) are CLAIM and REBUTTAL ids. That is a CONSUMER writing bank files, with the consumer's own framing and ids inside them: the A03 C6/C7 contamination verbatim, and the reason the ONE-WRITER rule exists. It also sits outside every checker surface (`check-probe-cards.sh` lints only `1-probes/*.md` and `**/QA/*.md`), so nothing would have caught it.

Step 5 now DISPATCHES: one `Agent(haipipe-task-orchestrator-agent)` / `Agent(haipipe-discovery-orchestrator-agent)` call per point, carrying ONE question in GENERAL language (no reviewer id, no point id, no claim id, no hoped-for answer). The EXECUTOR scaffolds and names the leaf and returns a `<leaf>/QA/<n>-<slug>.md` path, which the mapping table records. The returned file's `- state:` line is READ (answered → quote · working → in progress, do NOT re-dispatch · superseded-by → follow the chain) and NEVER written.

## [1.0.0] — 2026-05-31

- baseline metadata added.
