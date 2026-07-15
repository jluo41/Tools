---
name: haipipe-session
description: "Records what a working SESSION settled as a durable topic note under diagram/<YYMMDD>-<topic>/ (LAW 1: one folder per TOPIC, dated at birth, never re-dated — a later session APPENDS). Verbs: new · append · log · check. Trigger: session note, record this session, what did we settle, topic note, rulings ledger, _LOG, comment ledger, /haipipe-session."
argument-hint: "[new <topic> | append [<topic>] | log [<doc>] | check [<folder>]]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.1.0"
  last_updated: "2026-07-15"
  summary: "Session-to-topic-note recorder. LAW 1: one folder per TOPIC, not per session. v1.1 adds the `log` verb + the `_LOG.txt` comment/lessons ledger (an EXEMPT meta file): review a doc → reply inline `>> CC HH:MM:` [SOLVED]/[PENDING] → migrate resolved threads to _LOG; harvest session lessons (→ _LOG) + portable prefs (→ the owning skill's PREFERENCES.md)."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

haipipe-session — what this session SETTLED
===========================================

The session is the **INPUT**. The topic note is the **OUTPUT**.

A session ends and its judgment evaporates. This skill lands that judgment where one
grep can find it: a **topic note** — a small folder of `.txt` files under
`Tools/plugins/haipipe-toolkit/diagram/`.


LAW 1 — THE UNIT: ONE FOLDER PER TOPIC, NOT PER SESSION
=======================================================

The folder is `diagram/<YYMMDD>-<topic>/`. The date is stamped at **BIRTH** and is
**NEVER** changed. A later session **APPENDS** to it. It opens a new folder only for a
**NEW TOPIC**.

```text
   ❌ WRONG — one folder per session          ✅ RIGHT — one folder per topic
   ─────────────────────────────────          ──────────────────────────────
   📁 260714-probe-qa/                        📁 260714-probe-qa/   ← born 07-14
       05-rulings.txt   R1 R2 R3                  05-rulings.txt
   📁 260716-probe-qa/                              R1 R2 R3  (07-14 session)
       05-rulings.txt   R4                         R4        (07-16 session) ⬅ append
   📁 260721-probe-qa-again/                       R5 R6     (07-21 session) ⬅ append
       05-rulings.txt   R5 R6
                                              🔎 grep -rn 'R4' diagram/260714-probe-qa/
   🔎 the ledger now lives in 3 places.          → ONE hit. ONE ledger. ONE topic.
      "every ruling this topic made" is
      no longer one grep. LAW 1 is dead.
```

**WHY:** the rulings ledger is **APPEND-ONLY**. Its entire value is that *one grep finds
every ruling this topic ever made*. One-folder-per-session shatters it across dates.

**Then how is a SESSION traced?** By its date stamp, never by a folder of its own:

```text
   🔎 grep -rn '2026-07-14' diagram/260714-probe-qa/   ← everything a session settled
      (dated rulings in 05 + date-stamped _LOG entries; inline replies carry `>> CC HH:MM:`)
```


THE TWO REFERENCE FOLDERS — read before writing anything
========================================================

On disk, correct, and the spec. This skill CODIFIES them; it does not re-invent them.

```text
   📁 diagram/260714-probe-qa/        5 files  ⬅ 04-the-rules.txt = the canonical
                                                 REJECTED ledger ("WHAT WE DELIBERATELY
                                                 DID NOT DO" · "💀 DEAD — do not resurrect")
   📁 diagram/260714-resource-stage/  6 files  ⬅ 05-rulings.txt = the canonical
                                                 APPEND-ONLY ledger
```

Copy those two shapes. Do not invent new ones. (probe-qa uses a lighter header dialect
and folds 06 into 05 — both are live, and `check` tolerates both.)


VERBS
=====

**`new <topic>`** — scaffold `diagram/<YYMMDD>-<topic>/` from `ref/skeleton/` (6 files,
  pre-loaded with the header block, the ledger sections, and ⚠️ authoring rules).
  ▶ FIRST: `ls diagram/ | grep -i <topic>`. If a folder for this topic **EXISTS** →
    **REFUSE.** Name it, and route to `append`. A second folder for a live topic is the
    worst failure this skill can produce.
  ▶ Delete every `<PLACEHOLDER>` and every `⚠️` authoring line before it ships.

**`append`** — **THE DEFAULT AND MOST COMMON VERB.** Fold this session's outcomes into
  the EXISTING note. Three moves:
  1. a **new ruling** in `05-rulings.txt` — next id, bucketed under who ruled
     (`✅ JL RULED` / `⚙️  CC DEFAULTED`). Never renumber, rewrite, or delete one.
  2. a **`>> CC{MMDD}:` reply** under an open `> JL:`. It never overwrites the `> JL:`
     above it — both live there forever.
  3. a **status flip** in `06-shipped-owed.txt` (`🟠 owed` → `✅ SHIPPED — see <file>`),
     and line 4's `STATUS: 🟡 DRAFT` → `SPEC OF RECORD … SHIPPED.` once JL closes.
  ▶ **NEVER re-date the folder. NEVER re-date the header block.** The date is the topic's
    BIRTHDAY, not a timestamp: `260714-probe-qa` is still `260714-probe-qa` in 2027.

**`check`** — `./check-session-folder.sh <folder>`. Lints the whole house form below.
  Run it before calling a note done. A citation that no longer resolves is a **FAIL**,
  not a nit — a rotted cross-reference is how a spec of record quietly stops being one.

**`log`** — the COMMENT LEDGER + LESSONS, in the topic's `_LOG.txt` (an EXEMPT meta file;
  see the house form). Two uses:
  1. REVIEW A DOC. JL leaves `> JL:` comments in some doc (a SKILL.md, a manuscript);
     answer each IN PLACE with `>> CC HH:MM:` + a `[SOLVED]` / `[PENDING]` tag, and NEVER
     delete the `> JL:` line. Once the body edit LANDS, MOVE the whole thread (the `> JL:`
     line VERBATIM + the CC reply) out of the doc into `_LOG.txt`, keeping the doc body
     clean. A `[PENDING]` thread stays inline until JL decides, then migrates too. Each
     _LOG entry is stamped `[YYYY-MM-DD HH:MM · STATUS]`.
  2. HARVEST LESSONS at session end. Append a `LESSONS` block to `_LOG.txt` (craft gotchas,
     one per line). Fan any portable BEHAVIORAL preference out to the owning skill's
     `PREFERENCES.md` (git-tracked, synced across orchestrators): `_LOG` keeps the
     session-specific record, `PREFERENCES.md` keeps the reusable rule.


THE HOUSE FORM — non-negotiable (JL)
====================================

- **`.txt`, never `.md`** — markdown breaks monospace alignment.
- **MAX 6 files. NO index, no README, no `00-`.** One THEME per file. Six themed files
  ARE the index; a seventh telling of the same thing is the file that goes stale first.
  ▶ EXEMPT: `_LOG.txt` (and any `_*.txt`) — a META ledger, NOT a themed page. It does not
    count toward the 6, is UNCAPPED in length, and needs no `NN-` name or title underline;
    `check` still runs its markdown-table + reference checks. It holds the comment ledger
    (moved `> JL:`/`>> CC:` threads) + the session LESSONS block. See the `log` verb.
- **~250 lines max per file. ~88-column wrap; nothing past 91.**
- **NO markdown tables anywhere.** Sections + bullets + ASCII boxes.
- **ASCII headings** (`===` sections, `---` subsections) — not `##` / `###`. Underline
  length = title length **+0 or +1** (emoji are 1 column to some eyes and 2 to others;
  both live folders disagree and both look right in a terminal).
- **Every fenced block is ` ```text `.** Zero bare ` ``` ` openers.
- **Exactly 2 blank lines before every `===` section.** No tabs, no trailing whitespace,
  exactly one terminal `\n`.
- **Naming:** `NN-<slug>.txt` — zero-padded, contiguous from `01`, lowercase kebab.

**The header block** — 5 lines, verbatim in `ref/skeleton/`. Line 1 = sentence-case title
+ `===`. Lines 3 (`Part of: diagram/<folder>/  ·  <N> files, one theme each, no index.`)
and 4 (`STATUS: 🟡 DRAFT · flip to → SPEC OF RECORD — R1-Rn closed JL <date>. SHIPPED.`)
are **byte-identical in every file**. Line 5 is the only per-file difference: `Format:`
on 01, `Theme: <one-line abstract>` on 02-06. Line 4 is the folder's one status bit, and
`append` is what flips it.


THE FILE ARC — 01→06 is a narrative, not an arbitrary split
===========================================================

```text
   01  THE THING        what it IS + the ONE question the folder answers.
                        ⬅ the only file carrying the nav + the `Format:` line.
   02  WORKED EXAMPLE   ONE concrete case, end to end. REAL names, REAL paths, REAL ids.
                        Not on disk → it does not go here. It goes in 06 as 🟠 owed.
   03  MECHANISM        the moving parts: the loop, the gates, the states. How, not what.
   04  CONSTITUTION     the ONE invariant + ❌ THE ANTI-PATTERN + the REJECTED ledger
                        ("WHAT WE DELIBERATELY DID NOT DO" · "💀 DEAD — do not resurrect").
   05  RULINGS          🔒 MANDATORY · APPEND-ONLY. Every decision this topic ever made.
   06  SHIPPED + OWED   🔒 MANDATORY · the honesty ledger. ✅ on disk · 🟠 still owed ·
                        👉 decisions waiting on JL.  (a 5-file folder folds 06 into 05.)
```

Rename 03 and 04 to the topic (`03-gates` · `04-cleavage`); 01/02/05/06 keep their names.
**05 and 06 are MANDATORY.** Four themes are guaranteed in every note: (a) an append-only
rulings ledger · (b) a shipped-vs-owed / open-decisions file · (c) an anti-pattern
section · (d) a real worked example.
`_LOG.txt` is NOT part of this 01→06 arc — it is the EXEMPT meta ledger (moved comment
threads + the session LESSONS block), and appears only once a `log` step has run.


THE LEDGER — the fixed-column ruling record
===========================================

```text
  R1  SCOPE          DATA + MODELS + PRODUCING-CODE.
  │   │              │
  │   │              └─ body starts at COLUMN 22 · continuations align to col 22
  │   └─ ALLCAPS topic key            glyphs: ⬅ consequence · 📌 adopted-into
  └─ 2-space indent · minted in order         ⚠️  risk/why · ❓ Sure? · ✅ SHIPPED
     ids LOCAL to this folder · NEVER renumbered
```

Sections, glyphs and the `👉 JL: ______` write-in slot are pre-cut in
`ref/skeleton/05-rulings.txt`.

- **APPEND-ONLY. Never split, sort or tidy it.** A tidy ledger is a dead ledger.
- Ids are **not** numerically ordered within a section — minted in order, then bucketed
  by who ruled. That is correct; do not "fix" it.
- A superseded ruling gets a NEW ruling underneath saying so — **the old text stays.**


THE COMMENT PROTOCOL
====================

```text
   > JL:  "we should not design the probes, but design the paper-questions."
     ⬆ JL, VERBATIM, in quotes. Never paraphrased. Inline = 2-space indent;
       block form = every line prefixed `> `. NEVER delete a `> JL:` line.

   >> CC 14:32: [SOLVED] the split is FREE when the resource question is answered FIRST.
     ⬆ the assistant's reply, stamped `CC HH:MM:` + a TAG — [SOLVED] (done) | [PENDING]
       (needs JL). An un-tagged `> JL:` therefore always reads as genuinely OPEN. Once the
       body edit LANDS, the whole thread MIGRATES to `_LOG.txt` (the `log` verb), stamped
       with the full date; grep that date to trace everything a session settled.
```


CROSS-REFERENCES — two forms, and they must not rot
===================================================

```text
   same folder    →  bare filename, no path:   see 06-shipped-owed.txt
                     with an anchor:           (R4, 05-rulings.txt) · (01-artifact.txt ④)
   sibling folder →  the folder as a whole:    diagram/260714-probe-qa/
                     a file inside it:         probe-qa 02-the-files.txt,
                                               "The BUILD lane — the price of ..."
                     ⬆ DATE-STRIPPED slug + filename + the section title, in quotes
```

`check` resolves both forms. It is the only mechanical guard against the failure that a
parallel session causes: folder A cites folder B, someone restructures B, and A's
citation silently points at nothing.


COMPOSES WITH — do NOT rebuild these inside this skill
======================================================

```text
   🕐 haipipe-run-timeline   THE TRANSCRIPT — mechanical. What tools ran, which agents,
                             when. RECONSTRUCTS what happened.
   ✍️  haipipe-session (this) THE JUDGMENT — what we SETTLED. DISTILLS what was
                             load-bearing.
      ⇒ run-timeline reconstructs · haipipe-session distills. A session with no timeline
        is still recordable; a timeline with no session note is a receipt nobody reads.

   🎨 diagram-ascii          HOW TO DRAW — owns the emoji + box vocabulary.
   ✍️  haipipe-session (this) Owns the FOLDER + the LEDGER + the COMMENT PROTOCOL.
                             The diagrams INSIDE a note stay diagram-ascii's job —
                             call it, don't re-spec it.
      ⬅ this skill ABSORBS diagram-ascii's retired "Daily session log" use case.
        (JL, 2026-07-14: "we don't need Daily anymore".)
```
