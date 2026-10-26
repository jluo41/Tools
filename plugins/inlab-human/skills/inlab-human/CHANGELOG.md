inlab-human — Changelog
=======================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match the front matter `version:`.
Newest first.


## [0.3.0] — 2026-10-26

Merged 4 helper skill(s) into `_parts/`: `inlab-human-bundle` -> `_parts/bundle`, `inlab-human-console` -> `_parts/console`, `inlab-human-report` -> `_parts/report`, `inlab-human-review` -> `_parts/review`. /inlab-human reads `_parts/<name>/PART.md` instead of calling a separate skill; allowed-tools gained the parts' tools. Old commands map as `/inlab-human-bundle` -> `/inlab-human bundle`. (merge-parts 261026)
