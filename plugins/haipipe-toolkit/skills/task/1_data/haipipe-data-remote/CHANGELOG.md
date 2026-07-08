haipipe-data-remote — Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [1.2.0] — 2026-07-05

### Changed (JL: "这些东西要general，不是固定到一个项目的。不要出现具体的名字或者什么的")

- Employer-specific values scrubbed from docs: the employer-specific S3 bucket path in ref/concepts.md replaced with the s3://<bucket>/<repo-prefix>/ shape, and the employer SSO portal URL replaced with generic wording. Both now state the contract: concrete values are EXTERNAL CONFIGURATION living in the workspace's gitignored env.sh ($REMOTE_ROOT export + SSO URL in comments), never in skill docs.

## [1.1.0] — 2026-07-04

- probe->experiment rename damage reverted in fn-status (Probes every store / Probe each store / store probe); store count 10 (was 9); 0-RawStore -> 0-RawDataStore.

## [1.0.0] — 2026-05-31

- baseline metadata added.
