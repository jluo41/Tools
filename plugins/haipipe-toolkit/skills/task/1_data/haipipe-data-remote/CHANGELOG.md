haipipe-data-remote — Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.


## [0.1.3] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.3.0; older entries below keep their original numbers).

## [1.3.0] — 2026-07-08

- skill-diagnose fixes: nonexistent `--version @{tag}` CLI flag claim removed — ExternalStore pinning is path-based (`--path ExternalStore/@{version}/...`), matching store-map; store-map AIData pattern corrected to `{ParentSetName}/@v{N}AIData-{aidata_name}/`.
- Credentials/error guidance made BACKEND-CONDITIONAL (gdrive: rclone token refresh; s3: AWS SSO) — the workspace default is rclone/GDrive, the old text was AWS-only (JL: "ok, go ahead and fix all of them" — approved recommended option A).
- store-map: 7-AgentWorkspace and ExternalStore/@inference marked ⚙opt (optional; probe only env-exported stores); LearnStore / 0-REACH-RAW-Store noted as on-disk-but-not-synced; fn-status probe count now dynamic (JL: same ruling).

## [1.2.0] — 2026-07-05

### Changed (JL: "这些东西要general，不是固定到一个项目的。不要出现具体的名字或者什么的")

- Employer-specific values scrubbed from docs: the employer-specific S3 bucket path in ref/concepts.md replaced with the s3://<bucket>/<repo-prefix>/ shape, and the employer SSO portal URL replaced with generic wording. Both now state the contract: concrete values are EXTERNAL CONFIGURATION living in the workspace's gitignored env.sh ($REMOTE_ROOT export + SSO URL in comments), never in skill docs.

## [1.1.0] — 2026-07-04

- probe->experiment rename damage reverted in fn-status (Probes every store / Probe each store / store probe); store count 10 (was 9); 0-RawStore -> 0-RawDataStore.

## [1.0.0] — 2026-05-31

- baseline metadata added.
