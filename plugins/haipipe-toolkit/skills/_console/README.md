# `_console/` — the working desk

Working artifacts that a skill PRODUCES but must not SHIP: skillset reviews, migration plans,
ruling ledgers, cross-skill design notes. Anything a human works IN rather than a skill reads FROM.

```
skills/
├── _console/<YYMMDD>-<SLUG>.md          working artifacts — you work here
├── _console/closed/<YYMMDD>-<SLUG>.md   settled: ruling made AND executed; read-only
├── <family>/<skill>/SKILL.md            the shipped skills
└── ../diagram/<YYMMDD>-<topic>/         design notes + .txt diagrams (owned by haipipe-session)
```

## Rules

- **A process artifact never lives inside the skill it is about.** A review that ships next to its
  subject drifts the moment either changes, and it goes out to every consumer of that skill.
- **`<YYMMDD>-<SLUG>.md`, slug in UPPERCASE** — the date is the day the file is BORN and is never
  re-dated. One file per TOPIC, not per session; a later session APPENDS to the existing file.
- **Finding ids are file-local.** Two console files may both carry a `D1`; always cite an id with its
  file name.
- **Comment protocol** — `> JL:` is the owner's, `>> CC{MMDD}:` is the agent's reply underneath.
  The owner's words are never edited, reworded, or deleted; a resolved thread is archived into the
  file's own ruling ledger, quoted verbatim, before it is removed from the body.
- **Language** — console files are written in the language the owner works in (中文).
  Anything destined for a `SKILL.md` / `CHANGELOG.md` / `ref/*.md` is drafted in ENGLISH inside the
  console file, so it can be pasted into the skill without a translation step.
- **Not a dumping ground.** A console file has an owner, a live question, and a next step. When the
  work lands, the decisions belong in the affected skills' CHANGELOGs; the console file is the trail,
  not the record.
- **`closed/` — settled work.** A file moves to `closed/` only when its ruling is BOTH made and
  EXECUTED; it keeps its name and date, gains a `— ✅ CLOSED` title suffix and a FINISHED banner, and
  becomes read-only. Files still pointing at it are updated to the `closed/` path in the same move.
  ⚠️ If the owner waived the CHANGELOG entries for that work, the closed file is the ONLY record of
  it — say so in its banner, and never delete it without archiving first.

## Writers

| Skill | What it writes here |
|---|---|
| `haipipe-skill-diagnose` | the skillset review ledger (findings, threads, rulings) |

Closed reviews written before this convention still sit at their bucket roots
(`0_connect/`, `task/`, `task/1_data/`, `task/3_end/SKILLSET_REVIEW.md`) and are left in place —
CHANGELOG entries cite those paths. New reviews are written here.
