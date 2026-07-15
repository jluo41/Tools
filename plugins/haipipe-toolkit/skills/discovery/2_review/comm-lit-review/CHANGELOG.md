comm-lit-review — Changelog
===========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [1.0.1] — 2026-07-14 — the skill's declared name was not its invocable name

Fixed
- Frontmatter `name:` was `comm-lit-review-claude-single`, but the folder AND the registered symlink are both `comm-lit-review` — so the skill loads as `comm-lit-review`, and its self-declared identity was a name nothing could invoke. `Skill(comm-lit-review-claude-single)` fails; `Skill(comm-lit-review)` works. Anyone wiring a dispatcher from the frontmatter rather than the folder would have written a dead call. `name:` set to `comm-lit-review`, matching the live dispatchers in `haipipe-discovery-review`. (Pre-existing; unrelated to the probe redesign.)

## [1.0.0] — 2026-05-31

- baseline metadata added.
