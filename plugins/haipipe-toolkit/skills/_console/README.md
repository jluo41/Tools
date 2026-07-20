# `_console/` — the working desk

Working artifacts that a skill PRODUCES but must not SHIP: skillset reviews, migration plans,
ruling ledgers, cross-skill design notes. Anything a human works IN rather than a skill reads FROM.

```
skills/
├── _console/<YYMMDD>-<NN>-<SLUG>.md          working artifacts — you work here
├── _console/closed/<YYMMDD>-<NN>-<SLUG>.md   settled: ruling made AND executed; read-only
├── <family>/<skill>/SKILL.md            the shipped skills
└── ../diagram/<YYMMDD>-<topic>/         design notes + .txt diagrams (owned by haipipe-session)
```

## Filing rules

- **A process artifact never lives inside the skill it is about.** A review that ships next to its
  subject drifts the moment either changes, and it goes out to every consumer of that skill.
- **`<YYMMDD>-<NN>-<SLUG>.md`, slug in UPPERCASE** — the date is the day the file is BORN and is
  never re-dated. **One file per TOPIC**, not per session and not per WHO-does-it; a later session
  APPENDS to the existing file. Bucketing by owner instead of by topic is how a board gets read as
  redundant and deleted — that happened 2026-07-19 and cost an untracked file.
- **`<NN>` is a two-digit birth-order index, restarting at `01` each day.** Assigned when the file is
  born and NEVER reused — closing a board does not free its number, so a gap in the live folder is
  the signal that something closed. Filesystem birth time is NOT a substitute: moving a file into
  `closed/` resets it, and boards born in one batch share a commit, so after the fact neither `stat`
  nor `git log` can recover the order. The index is the only durable record of what came first, and
  that matters because boards SPIN OUT of each other — `04` was split from `02`, `03` from `02`'s D5.
- **Splitting a board is a MOVE, not a rewrite.** The new board cites its parent (`来源:<file> 第 N
  行`), and any `> JL:` thread that travels goes VERBATIM. Moving the owner's words needs the owner's
  go; splitting agent-written text does not.
- **Finding ids are file-local.** Two console files may both carry a `D1`; always cite an id with its
  file name.
- **Language** — console files are written in the language the owner works in (中文).
  Anything destined for a `SKILL.md` / `CHANGELOG.md` / `ref/*.md` is drafted in ENGLISH inside the
  console file, so it can be pasted into the skill without a translation step.
- **Not a dumping ground.** A console file has an owner, a live question, and a next step. When the
  work lands, the decisions belong in the affected skills' CHANGELOGs; the console file is the trail,
  not the record. **Work with no open decision does not get a board** — it gets a CHANGELOG entry.
- **`closed/` — settled work.** A file moves to `closed/` only when its ruling is BOTH made and
  EXECUTED; it keeps its name and date, gains a `— ✅ CLOSED` title suffix and a FINISHED banner, and
  becomes read-only. Files still pointing at it are updated to the `closed/` path in the same move.
  ⚠️ If the owner waived the CHANGELOG entries for that work, the closed file is the ONLY record of
  it — say so in its banner, and never delete it without archiving first.

## How to write a board

The shape below is what the boards on disk converged on. Use these headings, in this order.
Only the title, the 裁决账本 and the 清账表 are required; skip any other section with nothing to say.

```
# <YYMMDD> · <中文话题>                  ← ` — ✅ CLOSED` appended when it closes
**话题**:one sentence — what this board is, and what it is NOT
来源:<parent file> 第 N 行               ← only when split out of another board

  <fenced 术语表>        ONLY the terms needed to read THIS board. Not a glossary.
## 🎯 现在在哪            one fenced block: what is done, what is live, what is blocked
## ⚖️ 裁决账本(append-only · 你的原话逐字保留)
## 🔴 P0 · <what>  → 等 D<n>            findings by severity: 🔴 P0 · 🟠 P1 · 🟡 P2
## 🟠 P1 · <what>  → 可直接修             each group routes; see the routing rule below
## 🧾 清账表(**闭集**:…)
## 📝 <methodology / handoff>            only when the next reader actually needs it
```

### The hard rules

- **Record lines, never markdown pipe tables**, in every hand-edited block — inside a fence, so the
  columns stay aligned. (JL 2026-07-19, display v3.3.0. This file obeys its own rule; see Writers.)
- **Every number is MEASURED from disk at the moment you write it.** Never carry a count forward from
  an earlier message, and never adopt a subagent's count without re-running it. A grep written too
  narrow returns zero and reads as ✅ done — that exact failure has shipped twice on these boards.
  When a count comes from a command, put the command on the board.
- **A `> JL:` line is never edited, reworded, relocated, or deleted.** Reply `>> CC{MMDD}:`
  underneath. Only the owner resolves a thread; a resolved thread is archived into this file's own
  裁决账本, quoted verbatim, before it leaves the body.
- **NEVER edit a board by a computed range** — no `s[s.find(a):s.find(b)]`, no `sed '/a/,/b/d'`,
  no line-number span. A board repeats its own row labels across sections (the 清账表 rows are
  quoted verbatim in 现在在哪), so the two anchors silently land in DIFFERENT sections and the
  replacement eats everything between them. That happened 2026-07-19: a 清账表 update took the
  file from ~400 lines to 95 and deleted all 11 of the owner's `> JL:` comments, which git could
  not restore because the last commit predated them. Edit by unique exact string, one edit per
  block, and after ANY scripted edit to a board run `grep -c '> JL:'` and compare to the count
  before. A board is the one file where a bad edit destroys something that exists nowhere else.
- **Only the owner's verb closes a decision.** An agent may recommend, and should say which option it
  would pick and why — but it never records its own recommendation as the ruling.
- **The 清账表 is a CLOSED SET.** Its rows are fixed when the board is written and the counter reads
  `n / N` against that fixed N. A finding discovered later opens a NEW board; it never inflates this
  one's denominator. Without this rule a board becomes a treadmill — every pass clears rows and adds
  rows, and ✅ is unreachable. Say it on the board: `**闭集**:全部来自这一次审计,不再新增编号`.
- **A finding names `file:line` and what is wrong there.** A finding that only names a category is
  not actionable and does not belong on a board.
- **Every finding routes** — `→ 等 D<n>` (blocked on the owner) or `→ 可直接修` (the agent may just do
  it). An unrouted finding is why boards stall.
- **Cut boilerplate.** No legend nobody reads, no section restating another. (JL 2026-07-19,
  "messy messy messy": legends and Display Maps cut, resolved threads archived out.)

### A 裁决账本 entry

```
D<n> · <the question, phrased as a question>
     <what the owner needs in order to decide — measured, with file:line>
     <the options, and which one the agent would pick, and why>
> JL:
     >> CC:
```

`D<n>` is a decision the owner owes. Numbers are append-only and never reused — a closed `D3` stays
`D3`, so every reference to it keeps resolving.

## Writers

```
haipipe-skill-diagnose    the skillset review ledger (findings, threads, rulings)
```

Closed reviews written before this convention still sit at their bucket roots
(`0_connect/`, `task/`, `task/1_data/`, `task/3_end/SKILLSET_REVIEW.md`) and are left in place —
CHANGELOG entries cite those paths. New reviews are written here.
