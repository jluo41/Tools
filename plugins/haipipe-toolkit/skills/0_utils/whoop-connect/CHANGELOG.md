whoop-connect — Changelog
=========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [0.2.1] — 2026-09-20

- Check the external checkout, scripts, interpreter, credential loader, and callback before setup.
- Derive the redirect URI from the verified listener instead of assuming localhost:8080.
- Stop at missing dependencies and report only observed connection or scheduling status.
- Remove an unsupported interpretation of an example health metric.

## [0.2.0] — 2026-09-20

- Keep Client ID and Client Secret in local credential storage; never request
  or print them in chat, command arguments, or logs.
- Remove the hardcoded machine path and unverified daily-sync promise.
- Model one connection task with internal Steps and report only checked status.


## [0.1.0] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.0.0; older entries below keep their original numbers).

## [1.0.0] — 2026-05-31

- baseline metadata added.
