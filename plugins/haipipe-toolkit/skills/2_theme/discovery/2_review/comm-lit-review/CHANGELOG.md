comm-lit-review — Changelog
===========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## 0.1.1 · 2026-09-22

- Stamped as a vendored original: LICENSE copied from ARIS, `metadata.haipipe.vendored_from` = `https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep@0472e53`. The numbered folder now holds vendored originals only; the Search, Review and Synthesize skills we wrote sit at the family root.

## [0.1.0] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.0.1; older entries below keep their original numbers).

## [1.0.1] — 2026-07-14 — the skill's declared name was not its invocable name

Fixed
- Frontmatter `name:` was `comm-lit-review-claude-single`, but the folder AND the registered symlink are both `comm-lit-review` — so the skill loads as `comm-lit-review`, and its self-declared identity was a name nothing could invoke. `Skill(comm-lit-review-claude-single)` fails; `Skill(comm-lit-review)` works. Anyone wiring a dispatcher from the frontmatter rather than the folder would have written a dead call. `name:` set to `comm-lit-review`, matching the live dispatchers in `haipipe-discovery-review`. (Pre-existing; unrelated to the probe redesign.)

## [1.0.0] — 2026-05-31

- baseline metadata added.
