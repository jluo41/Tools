haipipe-end-deploy-local — Changelog
====================================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.


## [0.1.4] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.4.0; older entries below keep their original numbers).

## [1.4.0] — 2026-07-08

- skill-diagnose fixes: platforms/ prefix on all runnable platform paths (incl. scripts/serve_local.py docstring); uniform input-contract note (folder canonical; .tar.gz = wire form).

## [1.3.0] — 2026-07-05

### Changed (JL: "这个skill内部的code，还是不要运行，只是当作examples reference来用，到最后还是要写到task folder里的")

- scripts/serve_local.py repositioned as a REFERENCE TEMPLATE: never run in-place from the skill; copy into the serving job and run there (Deploy FastAPI steps 2-3 rewritten). Same rule likely applies to the 4_individual family's scripts/ dirs (flagged in SKILLSET_REVIEW F11, awaiting JL).

## [1.2.0] — 2026-07-05

### Changed (JL: "不要写硬编码，看看怎么fix")

- scripts/serve_local.py: hardcoded defaults removed. WORKSPACE_ROOT now resolves via WORKSPACE_PATH env, else pyproject.toml walk-up from cwd, else exits with a clear message (was hardcoded /home/jluo41/WellDoc-SPACE). ENDPOINT_PATH now resolves via ENDPOINT_PATH env, else auto-picks the single endpoint under _WorkSpace/6-EndpointStore/, else exits listing the candidates (was a hardcoded project-specific endpoint name).

## [1.1.0] — 2026-07-04

- 8 refs to nonexistent own ref/concepts.md -> shared deploy-overview.md.

## [1.0.0] — 2026-05-31

- baseline metadata added.
