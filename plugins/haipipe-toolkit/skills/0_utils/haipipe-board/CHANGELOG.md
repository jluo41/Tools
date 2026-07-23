haipipe-board — Changelog
=========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

**v0-series rule (JL, 2026-07-23):** this skill stays on `0.x.x` — **it never goes to 1.0.0 without JL's explicit say-so.** Everything here is provisional: the board form, the Q template, the generator's output. Ship `0.MINOR.PATCH` freely; `1.0.0` is a decision, not a milestone that arrives on its own.


## [0.1.0] — 2026-07-22

First working version. Board = a folder; `build.py` turns it into one static page.

- **board form** — `<unit>/diagram/<NN>-<topic>-<YYMMDD>/` holds `board.md` (title · `spine:` · `close:` · `## Topic` · `## Pipeline` · `## Roster`) plus one `Q<A><n>-<slug>.md` per question, plus generated `board.html` and `fig/`.
- **binding is by PATH** — every `Q*.md` in the folder is on the board; `## Roster` only sets order and grouping. An unlisted file still renders (under ⚠️) and warns on stderr — a missed roster entry can never drop a question.
- **Q file sections in English** — `## Question / Diagram / Done when / Now / Why here / Glossary / Discussion / Log`. Chinese section names still parse, so older boards build unchanged.
- **`## Done when` is a checklist** — `- [ ]` / `- [x]`, with an auto count (`3/5`) in the panel header.
- **`## Diagram`** — a fenced ASCII diagram per question, readable in the md and rendered as-is in the page.
- **`## Log`** — dated one-line history per question (`260722 · what changed`).
- **state labels** — `✅ SETTLED / 🟡 PARTIAL / 🔴 OPEN / ⏸️ ON HOLD`.
- **zero `<script>` in the output, asserted at build time.** Every question is a real `<section>`; collapsibles are native `<details>`; navigation is plain anchors. The page cannot render blank.
- **focus mode is pure CSS** — `:target` + `:has()` show one question full-screen, unbounded (no card border/radius/fill), 38px title, prev/next/index links. Same file serves both reading and projecting; there is no separate `deck.html`.

Known gaps (tracked on the board at `0_utils/diagram/01-boardform-260722/`): `SKILL.md` is not written (QB1), no fresh-agent acceptance run (QB2), the two older boards are not migrated (QB3), inline comments are half-built (QA6 — the md syntax parses, the CSS does not exist yet).
