---
name: haipipe-session
description: "Records what a working SESSION settled, as a durable topic note under Tools/plugins/haipipe-toolkit/diagram/<YYMMDD>-<topic>/. LAW 1 — ONE FOLDER PER TOPIC, NOT PER SESSION: the folder is dated at BIRTH and never re-dated; a later session APPENDS (a new ruling in the append-only ledger, a '>> CC{MMDD}:' reply under a '> JL:' comment, a status flip in shipped/owed). Verbs: new <topic> (scaffold; refuses if the topic already has a folder), append (the DEFAULT), check (lint the folder). House form: .txt only, max 6 files, one theme per file, no index, no markdown tables, ASCII headings, diagrams in text fences. Composes with haipipe-run-timeline (the transcript) and diagram-ascii (how to draw). Trigger: session note, record this session, what did we settle, topic note, diagram folder, rulings ledger, append to topic, 会话记录, /haipipe-session."
argument-hint: "[new <topic> | append [<topic>] | check [<folder>]]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-07-14"
  summary: "Session-to-topic-note recorder. LAW 1: one folder per TOPIC, not per session — dated at birth, appended forever. Codifies the two live reference folders (260714-probe-qa, 260714-resource-stage): .txt, max 6 files, no index, append-only rulings ledger, `> JL:` / `>> CC{MMDD}:` comment protocol."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

haipipe-session — what this session SETTLED
===========================================

The session is the **INPUT**. The topic note is the **OUTPUT**.

A session ends and its judgment evaporates. This skill lands that judgment in a place
one grep can find: a **topic note** — a small folder of `.txt` files under
`Tools/plugins/haipipe-toolkit/diagram/`.


LAW 1 — THE UNIT: ONE FOLDER PER TOPIC, NOT PER SESSION
=======================================================

The folder is `diagram/<YYMMDD>-<topic>/`. The date is stamped at **BIRTH** and is
**NEVER** changed. A later session on the same topic **APPENDS**. It creates a new
folder only for a **NEW TOPIC**.

```text
   ❌ WRONG — one folder per session          ✅ RIGHT — one folder per topic
   ─────────────────────────────────          ──────────────────────────────
   📁 260714-probe-qa/                        📁 260714-probe-qa/    ← born 07-14
       05-rulings.txt   C1 C2 C3                  05-rulings.txt
   📁 260716-probe-qa/                              C1 C2 C3   (07-14 session)
       05-rulings.txt   C4                         C4         (07-16 session) ⬅ append
   📁 260721-probe-qa-again/                       C5 C6      (07-21 session) ⬅ append
       05-rulings.txt   C5 C6
                                               🔎 grep -rn 'C4' diagram/260714-probe-qa/
   🔎 the ledger is now in 3 places.              → ONE hit. ONE ledger. ONE topic.
      "every ruling this topic made" is
      no longer one grep. LAW 1 is dead.
```

**WHY:** the rulings ledger is APPEND-ONLY. Its entire value is that *one grep finds
every ruling this topic ever made*. One-folder-per-session splits that ledger across
dates and kills it.

**How a SESSION is traced, then?** By its stamp, not by a folder:

```text
   🔎 grep -rn '>> CC0714' diagram/260714-probe-qa/     ← everything that session settled
```


THE TWO REFERENCE FOLDERS — read them before writing anything
=============================================================

These are on disk, they are correct, and they are the spec. This skill CODIFIES them.

```text
   📁 Tools/plugins/haipipe-toolkit/diagram/
      ├── 260714-probe-qa/          5 files  ·  the probe/QA spec of record
      │     01-what-is-a-probe.txt  02-the-files.txt  03-how-it-runs.txt
      │     04-the-rules.txt        05-status-and-open-items.txt
      └── 260714-resource-stage/    6 files  ·  the resource stage spec of record
            01-artifact.txt   02-worked-example.txt  03-gates.txt
            04-cleavage.txt   05-rulings.txt         06-shipped-owed.txt
```

`260714-resource-stage/05-rulings.txt` is the **canonical ledger**. `04-the-rules.txt`
(probe-qa) is the **canonical rejected-ledger** (`WHAT WE DELIBERATELY DID NOT DO`,
`💀 DEAD — do not resurrect:`). Copy those two shapes; do not invent new ones.


VERBS
=====

**`new <topic>`** — scaffold `diagram/<YYMMDD>-<topic>/` from `ref/skeleton/`.
  ▶ FIRST: `ls diagram/ | grep -i <topic>`. If a folder for this topic **exists** —
    **REFUSE**. Say so, name the folder, and route to `append`. A second folder for a
    live topic is the single worst failure this skill can produce.

**`append`** — **THE DEFAULT AND MOST COMMON VERB.** Fold this session's outcomes into
  the EXISTING topic note. Three moves, in this order:
  1. a **new ruling** appended to the ledger (`05-rulings.txt`), id minted next in
     sequence, bucketed under who ruled (`✅ JL RULED` / `⚙️  CC DEFAULTED`)
  2. a **`>> CC{MMDD}:` reply** written directly under an open `> JL:` comment
  3. a **status flip** in the shipped/owed file (`🟠 owed` → `✅ SHIPPED — see <file>`)
  ▶ **NEVER re-date the folder. NEVER re-date the header block.** Only the ledger and
    the status file move.

**`check`** — run `./check-session-folder.sh <folder>`. Lints the house form (below).
  Run it before you call a note done.


THE HOUSE FORM — non-negotiable (JL)
====================================

- **`.txt`, never `.md`** — markdown breaks monospace alignment.
- **MAX 6 files. NO index file, no README, no `00-`.** One THEME per file.
- **~250 lines max per file. ~88-column wrap; nothing past 91.**
- **NO markdown tables anywhere.** Sections + bullets + ASCII boxes.
- **ASCII headings** (`===` for sections, `---` for subsections). Not `##` / `###`.
  Underline length = title length, +1 allowed (emoji count as 2 display columns to
  some eyes and 1 to others; both live folders disagree and both look right).
- **Every fenced block is ` ```text `.** Zero bare ` ``` ` openers.
- **Exactly 2 blank lines before every `===` section heading.**
- No tabs. No trailing whitespace. File ends with exactly one `\n`.

**Naming:** `NN-<slug>.txt`, zero-padded, contiguous from `01`, lowercase kebab slug.

**The header block** (canonical = resource-stage dialect; use this for `new`):

```text
  1| The artifact — two sections, and the wire          ← sentence case, em-dashes
  2| =========================================          ← len(title) or +1
  3| Part of: diagram/260714-resource-stage/  ·  6 files, one theme each, no index.
  4| SPEC OF RECORD — the resource stage. C1-C9 closed JL 2026-07-14. SHIPPED.
  5| Format: JL comments are `> JL:` · CC replies are `>> CC{MMDD}:` + a diagram.
  6|                                    ⬆ line 5 is on FILE 01 ONLY; blank elsewhere
```
Lines 3 and 4 are **byte-identical across every file in the folder**. Two spaces
either side of the `·`. (probe-qa uses a second, lighter dialect — `N — TITLE` +
an indented one-line abstract, nav stamp on file 01. `check` tolerates both; `new`
emits the canonical one.)


THE FILE ARC — 01→06 is a narrative, not an arbitrary split
===========================================================

```text
   01  WHAT IT IS        the concept / the artifact.  ⬅ carries the folder nav +
                         the `Format:` protocol line. Nothing else does.
   02  THE CONCRETE      what is literally on disk — a real worked example with
                         real names, real paths. Not a sketch.
   03  HOW IT RUNS       the flow, the loop, the gates.
   04  THE LAWS          the constitution + ❌ THE ANTI-PATTERN + the REJECTED
                         ledger ("WHAT WE DELIBERATELY DID NOT DO", "💀 DEAD").
   05  THE LEDGER        05-rulings.txt — APPEND-ONLY. Every ruling, ever.
   06  SHIPPED + OWED    ✅ shipped · 🟠 still owed · 👉 decisions for JL.
                         (a 5-file folder folds 06 into 05.)
```

**Four themes are GUARANTEED in every topic note**, whatever the file boundaries:
(a) an append-only rulings/rejected ledger · (b) a shipped-vs-still-owed / open-decisions
file · (c) an anti-pattern or "what we did NOT do" section · (d) a real worked example
with real names on disk.


THE LEDGER — the fixed-column ruling record
===========================================

```text
  C1  SCOPE          DATA + MODELS + PRODUCING-CODE.
  │   │              │
  │   │              └─ body starts at COLUMN 22 · continuations align to col 22
  │   └─ ALLCAPS topic key
  └─ 2-space indent · C<n>, minted in order, NEVER renumbered

  glyph vocabulary on continuation lines:
     ⬅ consequence   📌 adopted-into   ⚠️  risk / why   ✅ SHIPPED — see <file>
     ❓ Sure? (an open question back to JL)
  open rulings end with a literal write-in slot:
     👉 JL: ____________________________________________________________________
```

Sections, in order: `✅ JL RULED — <date>` · `⚙️  CC DEFAULTED — live in the build, say
so if any is wrong` · `👀 WHERE THE CLOSURE COULD STILL BE WRONG` · `🔴 <open ruling>`.
Ids are **not** numerically ordered within a section — they are minted in order, then
bucketed by who ruled. That is correct. Do not "fix" it.

**The ledger is NEVER split by topic and NEVER re-sorted.** It only grows.


THE COMMENT PROTOCOL
====================

```text
   > JL:  "we should not design the probes, but design the paper-questions."
     ⬆ JL, verbatim, in quotes. Inline form = 2-space indent. Block form = every
       line prefixed `> `.

   >> CC0714: the split is FREE when the resource question is answered FIRST, because
   >> a ❌ on the corpus means the eval never runs at all.
     ⬆ the assistant's reply. `{MMDD}` = the date of the SESSION that replied.
       This is how a session is traced back out of a topic-dated folder.
```
A `>> CC{MMDD}:` reply **is what `append` writes.** It never overwrites the `> JL:`
above it. Both live in the file forever.


CROSS-REFERENCES — two forms, and they must not rot
===================================================

```text
   same folder   →  bare filename, no path:      see 06-shipped-owed.txt
                    with an anchor:              (C4, 05-rulings.txt) · (01-artifact.txt ④)
   sibling folder→  naming the folder as a whole: diagram/260714-probe-qa/
                    citing a file inside it:      probe-qa 02-the-files.txt,
                                                  "The BUILD lane — the price of ..."
                    ⬆ DATE-STRIPPED slug + filename + the section title in quotes
```
`check` resolves both forms. A citation that no longer resolves is a **FAIL**, not a
nit — a rotted cross-reference is how a spec of record quietly stops being one.


ANTI-PATTERNS — what NOT to do
==============================

```text
   ❌ one folder per session
      Kills LAW 1. Splits the append-only ledger across dates. The one unforgivable one.

   ❌ re-dating a folder because "the session is today"
      The date is the topic's BIRTHDAY, not a timestamp. 260714-probe-qa stays
      260714-probe-qa in 2027.

   ❌ an index / README / 00-overview file
      Six files with one theme each ARE the index. An index is a seventh telling of
      the same thing, and it is the file that goes stale first.

   ❌ a markdown table
      House rule. Sections + bullets + ASCII boxes. No exceptions, not even "just one".

   ❌ splitting or re-sorting a ledger by topic
      The ledger is append-only and chronological-by-mint. Its value is that ONE grep
      finds every ruling. A tidy ledger is a dead ledger.

   ❌ letting a cross-folder citation rot
      `probe-qa 02-the-files.txt` must still resolve. Run `check`.

   ❌ .md files, a 7th file, a 300-line file
      All three are the same failure: the note stopped being readable in one sitting.
```


COMPOSES WITH — do NOT rebuild these inside this skill
======================================================

```text
   🕐 haipipe-run-timeline (0_utils)     THE TRANSCRIPT — mechanical. What tools ran,
                                          which agents, when. Reconstructs the session.
   ✍️  haipipe-session (this)             THE JUDGMENT — what we SETTLED. Distills what
                                          was load-bearing.
   ─────────────────────────────────────────────────────────────────────────────────
   THEY COMPOSE:  run-timeline  ──reconstructs what happened──▶  haipipe-session
                                                                  distills what mattered
                  A session with no timeline is still recordable. A timeline with no
                  session note is a receipt nobody will ever read.

   🎨 diagram-ascii (0_utils)            HOW TO DRAW. Owns the emoji/box vocabulary.
   ✍️  haipipe-session (this)             Owns the FOLDER + the LEDGER + the COMMENT
                                          PROTOCOL. The diagrams *inside* a topic note
                                          are diagram-ascii's job — call it, don't
                                          re-specify it.
   ⬅ haipipe-session ABSORBS diagram-ascii's retired "Daily session log" use case.
     (JL, 2026-07-14: "we don't need Daily anymore".)
```
