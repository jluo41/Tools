haipipe-data-aidata — Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [1.3.0] — 2026-07-05

### Changed (JL: "这些东西要general，不是固定到一个项目的。不要出现具体的名字或者什么的")

- The 70+ line OptTime v2 fu7d worked example moved out of SKILL.md into ref/worked-example.md (SKILL keeps a 10-line digest + pointer; the generic blank template stays in SKILL). Employer name scrubbed from the example. SKILL.md now loads ~250 lines instead of 319 at invocation.

## [1.2.0] — 2026-07-04

- dead code/hainn/algo/ hand-off path -> workspace-neutral wording; dead template path fixed.

## [1.0.0] — 2026-05-31

- baseline metadata added.

## [1.1.0] — 2026-06-11

- add Multi-partition Mode section — auto-discover CaseSet partitions via record_set_name + CaseArgs config, streaming HF Dataset merge, --use-cache; remove stale 0_data_nb reference.
