---
name: haipipe-plugin-outline
description: >-
  The outline/ plugin of a Board page: the page's PROCESS folder (seven record
  kinds: the versioned plan, requirement, discussion, feedback, evidence,
  files, log) and the 🧭 tab that reads them, first and default on every page.
  Read-only surface; the deliverable of the OUTLINE phase. Trigger: outline
  plugin, outline tab, page outline, outline folder, plan file, record shape,
  evidence bundle, D<nn> thread, /haipipe-plugin-outline.
metadata:
  version: "0.20.1"
  last_updated: "2026-08-31"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-plugin-outline · the page's process folder, and the tab that reads it

**LOAD `haipipe-plugin` FIRST.** It owns what any plugin is: storage, surface,
writer, boundary. This file owns outline's delta: what the folder holds, what
the tab shows, and who writes each file. The phase that produces the folder is
`page-workflows/haipipe-page-outline`; it loads `ref/plan-grammar.md`, not
this file.

```text
  this file      the FOLDER (seven kinds) and the TAB (chips, lenses, the join)
  ref/           plan-grammar.md · record-shape.md · specimen-section-plan.md ·
                 evidence-bundle.md: the exact grammars a writer or parser needs
  the phase      page-workflows/haipipe-page-outline: one pass, its checks, its tick
```

## 🗂 The folder · product beside process

`<page>.md` is the PRODUCT: what the page asserts. `<page>/outline/` is the
PROCESS: how it came to assert it. Since 260831 the folder is legal on any
UNIT, task folders included (the unit symmetry, `haipipe-page` §📁): same
kinds, same grammar; a task folder simply never owes the venue-only
requirement file. Seven kinds, one flat file each with the
stem; only the plan is many-per-page, by version.

```text
<page>/outline/
├── <stem>-outline-v<N>.md    what we AGREED      authored · a person ticks · versioned
├── <stem>-requirement.md     what we MUST obey   generated · cli/requirement.py · venue only
├── <stem>-discussion.md      what is still ASKED authored · open D<nn> threads · never versioned
├── <stem>-feedback.md        what OTHERS said    generated · cli/feedback.py collect · page writes Landed
├── <stem>-evidence.md        what has LANDED     generated · cli/evidence-status.py
├── <stem>-files.md           what it READS/WRITES authored · F<n> records · Path + Role
└── <stem>-log.md             what CHANGED        authored · dated records · append-only · newest first
```

- **One question per file, and the questions do not overlap.** A fact that
  answers another file's question is misplaced: a settled thread is a log
  record, a deviation from the venue is a thread, a plan's status is on the
  page's Aims.
- **Authored versus generated is the line, not topic.** A generated file is
  regenerated whole and never hand-edited (`*-hand-edited` teeth); an
  authored file is written by the page and its signed lanes are never deleted.
- **No file name contains `outline` except the plan**, because the plan globs
  are `*-outline-*.md`.
- **The page keeps four on-stage sections**, Opening · Diagram · Content ·
  Aims, and nothing this folder holds. `check.py` reports a surviving
  `## States`, `## Files`, `## Log` or `## Discussion` as `retired-section`.

The grammar of every record file, its labels, its writer and its teeth:
`ref/record-shape.md`.

## 📐 The plan · one grammar

The full grammar is `ref/plan-grammar.md`; the approved example is
`ref/specimen-section-plan.md`. What a reader must know without opening them:

```text
## C<n> · <name>                     division · ≤ 8 words · names its subject
### C<n>.P<m> · <move> · S<a> to S<b> paragraph · a Section page names the sentence span
- B<k> · <head>                      4 to 11 plain words: what the point DOES
  Note: <≤ 30 words> <marks>         the constraint or definition; the marks end it
  Answered: · Drawn: · Routed:       appended by the fold, one per line
```

- **The grain is the Page Type's**: on a Section page one bullet is one
  sentence slot (`S<n> · …`); on every other page one bullet is one point that
  DRAFT turns into one or more sentences.
- **The plan never quotes the sentence it plans.** The sentence lives on the
  page; the plan says what the sentence must do and what constrains it. A Note
  is at most 30 words (a wrapped source line is still one Note); a Note that
  carries prose is DRAFT leaking upward.
- **A mark is the exception**: 🎯 aim · 📚 citation · 📮 probe · 🧮 value ·
  🖼 display, at the end of the Note line; unmarked means nothing is owed.
- **The plan carries no Aim rows.** Aims live on the page; a 🎯 mark names one.
  An ask with no Aim is a `D<nn>` thread, never a minted Aim.
- **The address is `C<n>.P<m>.B<k>`** and it is the join key for every other
  file in the folder and every card, key and unit in the sibling lanes.

## 🔒 The plan freezes at approval, not at creation

```text
  ✍️ v1 · approved: ⬜   a working document: edit, delete, rewrite freely
        │  🧑 a person ticks approved:
        ▼
  🔒 v1 · approved: ✅   frozen, correct as of that date
        │  the work moves on
        ▼
  ✍️ v2 · approved: ⬜   supersedes: v1 · v1 is kept, because it was right then
```

The fold's appends (`Answered:` `Drawn:` `Routed:` and a `PP<NN>` id once a
card serves a bullet) are the one write an approved version accepts, and they
add, never edit: a plan that rewrote its own heads as work landed would always
look finished. `approved:` is a person's; a machine may transcribe a person's
chat approval with the quote and the time, and writes `checked:` for itself.

## 🎛 The tab · where a person stands to work a page

🧭 Outline is the FIRST and DEFAULT tab on a page (`live/shell.py` asks the
plugin registry's default and ranks it first; on a group page, which has no
live page, 💬 Chat is the fallback). Every other tab shows one material; only
🧭 shows the plan and, against each part of it, what that part still owes.

```text
🧭 By part · 🚦 What is left · 📏 Requirement · 4 · 💬 Discussion · 5 · 🗣 Feedback · 8 ·
🧾 Evidence · 3 · 📎 Files · 4 · 📜 Log · 20
```

- **Two lenses over one parse**: 🧭 By part is one card per Content division
  with its Aims, ticks and `Now:` facts; 🚦 What is left is the same rows with
  ⬜ before ✅, because opening it is asking what the page still owes.
- **One chip per record file that exists**, with its record count; a file that
  does not exist draws no chip. Every lens draws records the same way: id
  badge, headline, label grid, status pill, detail behind "more".
- **The plan card sits above the division cards** and joins each bullet to
  the disk: `📚` key in `bibex/` or not · `📮` card state, proof present or
  not · `🖼` unit declared → rendered → accepted · `↩ PP04 0/1` when a card
  serves a bare mark. Header counts `owed · landed · accepted` are computed
  separately and never collapsed.
- **Both failure modes render as a named row, never a blank**: 🕳 owed and
  nothing there (a bullet cites `Display2` and no unit folder exists) · 🎈
  there and uncited (a card no bullet names).
- **The tab writes nothing and calls no model.** It reads the plan, the page,
  the record files and the sibling lanes on every open, so it cannot be stale.
  The Aims are read from the page first; a plan row fills only an id the page
  lacks.
- **The answer comes first**: the page's own question, then one line of counts
  (done · left · waiting), then the cards; unfinished rows stay in sight and
  finished ones fold.

### Chips stay inside the sentence

```text
① INLINE, never a column   a chip lives in the row's own span; a sibling column steals the text's width
② a TAG, not a pill        10.5px monospace · nowrap · 4px radius · 0 4px padding
③ the note is a WORD       `in bibex/` → nothing (the colour says it) · `no unit declared yet` → `owed`
④ never say it twice       a chip is `emoji · id · note`; the ↩ tag is suppressed for a card the row already names
```

No emoji inside a tag. A chip opens a native popover holding the THING itself
(the reference as printed, the card's own question, the unit's own claim); a
📚 panel prints `Author et al.`, never the author list.

## 🔗 The evidence bundle · a derived view, not a folder

The tab may show, per bullet, the join of the frozen address to everything
that names it: the sentence scaffold (`realizes:`), probe cards (`serves:`),
bibex keys, `proof/`, display units and their `accepted:` tick. It is a
projection; Probe, Bibex and Display keep their own folders, and a human
choice such as `selected: Display2` lives on the owning unit. The status words
and rules are `ref/evidence-bundle.md`; `<stem>-evidence.md` is the same join
written to disk with a date.

## ✍️ Who writes what

```text
file            written by                                    regenerate with
────────────────────────────────────────────────────────────────────────────────────────────────
plan            ① OUTLINE (in session or haipipe-page-outline-agent); the fold appends   never
requirement     the generator                                 cli/requirement.py <page>.md
discussion      any phase or the page chat, as D<nn> records  never (authored)
feedback        the generator; the page writes Landed only   cli/feedback.py collect <page>.md
evidence        the generator                                 cli/evidence-status.py <page>.md
files           any phase or the page chat                    never (authored)
log             every phase and the page chat, append only    never (authored)
```

`POST /_board/outline` exists only so the shell's `tab: {url, write}` contract
holds; it writes nothing.

## 📂 Files

- `ref/plan-grammar.md` · the plan file's grammar, type switch, marks, versions, teeth
- `ref/record-shape.md` · the seven record kinds: ids, labels, writers, per-kind rules
- `ref/specimen-section-plan.md` · the approved Section plan, frozen (SM00 v3)
- `ref/evidence-bundle.md` · the derived per-bullet join and its six status words
- `../../haipipe-board/live/outline.py` · the parse, the lenses, `plan_card`, `_records`, the chips
- `../../haipipe-board/live/shell.py` · the tab strip; 🧭 ranked first and opened by default
- `../../haipipe-board/checks/outline.py` · the standing check over every board's plans
- `../../haipipe-board/src/plan_shape.py` · `plan-shape-off-type`, `bullet-missing-note`, the head and Note teeth
- `../../haipipe-board/cli/requirement.py` · `cli/feedback.py` · `cli/evidence-status.py` · the three generators
- `../../page-workflows/haipipe-page-outline/SKILL.md` · the phase whose deliverable this folder is
- `../../../diagrams/BoardSkillBoard-260722/4-QPf-page-folder/QPf12-outline/QPf12-outline.md` · the design page and its rulings
