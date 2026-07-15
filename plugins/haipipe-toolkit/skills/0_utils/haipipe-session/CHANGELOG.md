haipipe-session — Changelog
===========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [1.1.0] — 2026-07-15

Adds the `log` verb + the `_LOG.txt` comment/lessons ledger, codifying the review +
harvest workflow exercised across the 2026-07-14/15 haipipe-task sessions.

**`_LOG.txt` — a first-class EXEMPT meta file.** Not a themed page: it does NOT count
toward the 6-file cap, is UNCAPPED in length, and needs no `NN-` name or title underline.
`check` now exempts `_*.txt` from PASS-0 (count/naming/gap) and PASS-1 (length/underline)
while still running its markdown-table + reference checks. Before, `check` FAILed a folder
with `too-many-files(7 > 6)` the moment a `_LOG.txt` appeared — the pattern was in use but
the checker rejected it.

**`log` verb — two uses.**
- REVIEW A DOC: answer each `> JL:` in place with `>> CC HH:MM:` + a `[SOLVED]`/`[PENDING]`
  tag (never delete the JL line); once the edit LANDS, migrate the whole thread (JL line
  verbatim + CC reply) into `_LOG.txt`, keeping the reviewed doc's body clean. `[PENDING]`
  threads stay inline until JL decides, then migrate too.
- HARVEST LESSONS at session end: a `LESSONS` block in `_LOG.txt` (craft gotchas) + fan
  portable behavioral preferences out to the owning skill's `PREFERENCES.md`.

**Comment protocol updated.** `>> CC{MMDD}:` → `>> CC HH:MM:` + `[SOLVED]`/`[PENDING]`; an
un-tagged `> JL:` now always reads as genuinely OPEN. A session is traced by its DATE
(dated rulings in 05 + date-stamped `[YYYY-MM-DD HH:MM · STATUS]` _LOG entries), not the
`>> CC` stamp.

Files: SKILL.md (frontmatter + `log` verb + house-form exemption + comment protocol +
file-arc note + LAW-1 trace), check-session-folder.sh (`_*.txt` exemption in PASS 0/1).


## [1.0.0] — 2026-07-14

Initial skill. Records what a working SESSION settled, as a durable topic note under
`Tools/plugins/haipipe-toolkit/diagram/<YYMMDD>-<topic>/`.

**LAW 1 — the unit (JL, 2026-07-14).** ONE FOLDER PER TOPIC, NOT PER SESSION. The
folder is dated at BIRTH and never re-dated; a later session APPENDS to it. Rationale
recorded verbatim so it is not re-litigated: the rulings ledger is append-only, and its
whole value is that *one grep finds every ruling this topic ever made*. One folder per
session would split that ledger across dates and kill it. The session is traced by its
`>> CC{MMDD}:` stamp, not by a folder of its own.

**Codified, not invented.** The spec is the two live folders, read in full and treated
as ground truth:
- `diagram/260714-probe-qa/` (5 files) — canonical REJECTED ledger
  (`WHAT WE DELIBERATELY DID NOT DO`, `💀 DEAD — do not resurrect:`)
- `diagram/260714-resource-stage/` (6 files) — canonical APPEND-ONLY rulings ledger
  (`05-rulings.txt`), the fixed-column `C<n>  TOPIC-KEY  <body at col 22>` record, and
  the `> JL:` / `>> CC{MMDD}:` comment protocol.

**Verbs.** `new <topic>` (scaffold from `ref/skeleton/`; REFUSES if a folder for the
topic already exists and routes to `append`) · `append` (the DEFAULT: new ruling,
`>> CC{MMDD}:` reply, status flip) · `check` (`./check-session-folder.sh`).

**House form enforced.** `.txt` only · max 6 files, no index · one theme per file ·
~250 lines · ~88-col wrap · zero markdown tables · ASCII `===`/`---` headings with
underline length = title +0/+1 · every fence is ` ```text ` · 2 blank lines before every
`===` section · no tabs, no trailing whitespace, single terminal newline.

**Two header dialects tolerated, one emitted.** resource-stage's block (`Part of:` /
`SPEC OF RECORD` / `Format:` on file 01) is canonical and is what `new` writes;
probe-qa's lighter `N — TITLE` + indented abstract is accepted by `check` because it is
live on disk. Underline equality is checked as `0 <= len(underline) - len(title) <= 1`
— a strict-equality check would produce 48 false failures across the 11 live files
(emoji and `①` headings are why).

**Boundaries stated, so nobody rebuilds one skill inside another.**
- `haipipe-run-timeline` = the TRANSCRIPT (mechanical: what ran, when).
  `haipipe-session` = the JUDGMENT (what we settled). They COMPOSE.
- `diagram-ascii` = how to DRAW. `haipipe-session` owns the FOLDER + LEDGER + COMMENT
  PROTOCOL; the diagrams inside a topic note remain diagram-ascii's job.
- `haipipe-session` ABSORBS diagram-ascii's retired "Daily session log" use case
  (JL, 2026-07-14: "we don't need Daily anymore").

**Anti-patterns named explicitly:** one folder per session · re-dating a folder · an
index file · a markdown table · splitting/re-sorting a ledger by topic · letting a
cross-folder citation rot.

**Registration.** No manifest row exists anywhere — `Tools/install.sh` discovers skills
dynamically via `find plugins/**/skills/*/SKILL.md`. The skill is invisible until
`./install.sh --global --project /home/jluo41/WellDoc-SPACE` is re-run to mint the three
symlinks (`~/.claude/skills/`, `.claude/skills/`, `.codex/skills/`).
