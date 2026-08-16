# Writing: the verb that rewrites prose and records every word it changed
state: 🟡 PARTIAL · the unit is healthy, its position is not · open: 4, incl. the roster's scope
owner: JL
method: describe the neighbour unit by what it produces, the `✎` record, then settle why a unit outside this family sits on this board; the snapshot is plugged in `skill/`
session: 8ab6d00e-cf65-453c-b5c5-c5b37d7905d0

## Opening
What rewrites prose that is already written, and how does a reader see which words changed?
`haipipe-writing` takes prose somebody already wrote and makes it readable to a person whose English is weak.
Then it records every word it changed, as a `✎` line under the sentence it changed.
That record is the same `✎` lane `QS1` owns, which is why this page sits in the sentence chapter.
Two of its three verbs are code, so a model never computes a diff and never places a record.

**Where this page sits**: `QS1` owns what a `✎` line IS on a board, and `QS2` owns how such records age.
This page owns the unit that produces them from prose anywhere, on a board page, a `SKILL.md`, a README, or a paper section.
`haipipe-board/ref/writing-rules.md` is the board's own prose standard and is what a page is checked against; this unit is the verb that acts on prose.

**Why a unit from outside the family is here**: it is the only unit on this board that ships from outside `skills/board/`, from `writing/haipipe-writing/`.
It is here because the board is one of its hosts, and because `ref/writing-rules.md` is load-bearing for every page.
Being on the roster is not the same as being in the family, and `### 1` says why the door test deliberately sent it out.

**What this page carries**: the unit's snapshot sits in this page's `skill/haipipe-writing/` plugin, with the five `ref/` contracts it collected.
Its judgments are made against that plugged copy, so a judgment can be read against the wording it was made on.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**Say what the unit PRODUCES, not what it is like**: the subject of this page is the `✎` record, so a claim about the unit that cannot be traced to an output belongs in its own changelog.
That is also what keeps this page in the sentence chapter rather than in a roster.

**Generated inventory and human judgment stay apart**: the snapshot in `skill/` is written by a tool, and `## States` is a person's read of the unit's health.
Never let a version bump argue that the unit is well placed, because position and quality are different claims and this page's `🟡` is about position.

**Two producers of one record are named together or not at all**: whenever the `✎` grammar is described, say that two units write it.
Describing one producer alone is how the two drift without anybody noticing.

**Language and sentences**: English only, in the source and in the render.
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes: use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

## Diagram

**One judgment step, fenced by code on both sides**: where a model acts, and where it must not.

```text
── The verb, end to end ──────────────────────────────────────────────────

  📄 authored prose · a board page · a SKILL.md · a README · a section
        │
        │ 1️⃣ cli/score.py       🤖 CODE · ranks what is worth rewriting
        ▼                         read-only, it never rewrites
  📋 a ranked worklist · a person reads it, nothing has changed yet
        │
        │ 2️⃣ rewrite            🧠 JUDGMENT · the ONLY step a model does
        ▼
  ✍️ new prose, beside the old
        │
        │ 3️⃣ cli/wdiff.py apply 🤖 CODE · computes the diff, anchors it
        ▼
  📝 prose + `> ✎ ~removed~ *added* · WHO · YYMMDD HHMM`
        │                         under the sentence it changed
        │ 4️⃣ cli/wdiff.py check  🤖 CODE · every record well formed
        ▼                         and attached to a real sentence
  ✅ readable, and reviewable

  🔒 the judgment is step 2, and ONLY step 2
  🚫 a model never writes the diff and never places the record
  🔢 four steps under three named verbs: apply and check are one file
```

**What sits in this page's `skill/` plugin**: the unit's contract surface, plugged and versioned.

```text
📦 skill/haipipe-writing/
   ├── SKILL.snapshot.md      the door
   ├── CHANGELOG.md
   └── ref/  plain-rules · change-record · ai-tells · weaving · holes
             the last three migrated in from the paper family on 260801
```

## Content
### 1 · A neighbour unit, on this board because its standard is load-bearing
**In the family, or only on the board**: the test that decided it, and what it decided.

```text
🚪 THE DOOR TEST · does a consumer need this unit's rules with no board open?

  ⚖️ applied to haipipe-writing on 260802  (QC1b §1.3)
     its consumer is ANY authored prose in the repo
     ─▶ ✅ PASSES the test, so it was sent OUT of the family

  🏠 it ships from writing/haipipe-writing/, not skills/board/
  📋 it is on this ROSTER because the board is one of its hosts
  🔑 on the roster ≠ in the family · this page is where that shows
```
📌 Establishes that the one unit here from outside `skills/board/` was excluded from the family on purpose, and says what excluding it bought.

#### 1.1 · Folding it in would have tied a general verb to one host
(the door test asks whether some consumer needs the rules with no board open, and this unit passes it too easily)
Its consumer is any authored prose in the repo: a board page, a `SKILL.md`, a README, a grant application section.
Making it a board unit would have made every one of those consumers depend on a board, which is the coupling the test exists to prevent.

#### 1.2 · It is host-agnostic by construction, and one file keeps it that way
(`ref/change-record.md` §4 writes the board dialect and the LaTeX dialect down together)
Two dialects in one file cannot drift into two ideas, because a change to one is read beside the other.
That is the mechanism behind the claim, rather than a promise that somebody will keep them aligned.

### 2 · The judgment is one step, and code fences it on both sides
**Why the verb count confuses people**: four steps, three names, two files.

```text
🔢 THREE NAMED VERBS · FOUR STEPS

  score    1️⃣  cli/score.py     🤖 read-only ranking
  rewrite  2️⃣  the model        🧠 the only judgment
  apply    3️⃣  cli/wdiff.py     🤖 diff + anchor
  check    4️⃣  cli/wdiff.py     🤖 audit every record

  ⚠️ apply and check are the SAME FILE, which is why the unit's own
     summary says three and its own figure numbers four
```
📌 Establishes exactly where a model is allowed to act, and why counting the verbs gives two different answers.

#### 2.1 · A model never computes a diff and never places a record
(the two acts that must be reproducible are the two acts given to code)
A diff a model wrote cannot be re-derived from the two texts, so nobody could check it later.
A record a model placed could attach to the wrong sentence, and adjacency is the only binding a lane has.

#### 2.2 · `score` has never been pointed at this board
(the verb ranks prose against the weak-English test, and this board has 56 pages)
Today's rewrites are chosen by JL reading Openings by eye, which is the work `score` exists to replace.
That is Aim A2.2, and it is the most obvious unused thing on this page.

### 3 · Two units now write the same `✎` record
**One grammar, two implementations**: who writes a change record, and what checks that they agree.

```text
✎ ONE RECORD GRAMMAR · TWO PRODUCERS

  ✍️ cli/wdiff.py apply        when this unit rewrites prose anywhere
  🖱 haipipe-sentence `edit`   when a person retypes a sentence in
                               the browser  (arrived 0.3.0, 260802)

  ✅ they agree today, because both follow the same grammar
  🚫 nothing checks that they still will
  🛠 cli/agree.py exists for exactly this shape and has never been
     pointed at this pair
```
📌 Establishes that the `✎` record has two independent writers, and names the instrument that could hold them together.

#### 3.1 · The second producer arrived the same day the first was described
(`QS1` closed on 260802 and `haipipe-sentence` took three verbs, one of which writes a `✎`)
Before that, this unit owned when a change record gets written and `haipipe-sentence` owned what one IS.
That division stopped being true on the day it was written down, which is why it is a Content division and not a settled Law.

#### 3.2 · `ref/change-record.md` was not written to cover this
(§4 keeps the board dialect and the LaTeX dialect in one file, which is a different problem)
Two dialects of one grammar and two implementations of one dialect look alike and are not.
The file solves the first and says nothing about the second.

### 4 · The roster's scope beyond `skills/board/`, widened but not settled
**A ruling and its exception**: what the scope said, and what asking for this page did to it.

```text
📋 WHO BELONGS ON THIS BOARD'S UNIT ROSTER

  260727  QC3a ruled: skills/board/ and nothing else
  260802  JL asked for this page, which is outside it
          ─▶ the ruling was WIDENED, not followed

  ❓ where the new line falls has never been said
     🅰 this one neighbour, because its standard is load-bearing
     🅱 every family the board depends on
     🅲 all 158 skills in the plugin

  🔑 the widening is sound; the LINE is what is missing
```
📌 Establishes that this page exists by a widening of an explicit scope ruling, and that the new scope has never been stated.

#### 4.1 · This page is the row the scope ruling left open, not an exception slipped past it
(JL asked on 260802 to add the `skills/writing` units, and this is the only one)
The reason the widening is sound is that this unit is not a stranger to the board: it owns the prose standard every page here is judged against.
What is unstated is the general rule, and a scope with one member and no rule admits the second member by precedent rather than by decision.

## Aims
### A1 · 🚪 A neighbour unit, on this board because its standard is load-bearing
- A1.1 · The reason this unit is on the roster and not in the family is stated where a reader meets the unit.
  **Done when:** A reader can say why the door test excluded it, and what excluding it bought, without opening `QC1b`.

### A2 · 🔢 The judgment is one step, and code fences it on both sides
- A2.1 · The paper family stopped keeping its own copies of the three migrated contracts.
  **Done when:** The owner closes this on the 260805-06 evidence: `ref/ai-tells.md`, `ref/weaving.md` and `ref/holes.md` live only here, the paper tree keeps no copy, and the humanizer sits beside this unit in `skills/writing/`.
- A2.2 · One `score` run picks what this board rewrites next.
  **Done when:** The verb has been run over this board's pages and its ranking, rather than a person reading Openings by eye, chose the next rewrite.

### A3 · ✎ Two units now write the same `✎` record
- A3.1 · The two producers of a `✎` record are checked against each other.
  **Done when:** `cli/agree.py` has been pointed at the pair and its result is recorded here.

### A4 · 📋 The roster's scope beyond `skills/board/`, widened but not settled
- A4.1 · The new scope line is stated, not just crossed.
  **Done when:** A written rule says which units outside `skills/board/` belong on this board, and `QC3a`'s 260727 ruling is updated or superseded to match.

### P · Page-level
- P1 · The page describes the unit by what it produces, so it stays in the sentence chapter.
  **Done when:** Every division traces to the `✎` record or to the unit's placement, and none of it reads as a changelog.

## States
### Decision Now
- [ ] 🗣 Say where the roster's scope line falls now that it has been widened
      📍 `Part` §4, the roster's scope
      🔔 `Why now` `QC3a` ruled `skills/board/` and nothing else on 260727, JL crossed that line on 260802 by asking for this page, and no rule replaced it, so the next unit joins by precedent
      ⭐ `A ·` this one neighbour, named explicitly, which keeps the roster at one exception and makes the next one a decision again
      `B ·` every family the board depends on, which is a rule rather than an exception and grows the roster by a knowable set
      `C ·` all 158 skills in the plugin, which makes the roster a plugin index and gives up on the board's own scope
      🛑 `Blocks` A4.1, and the matching Decision Now row on `QC3a`
      🤖 `If nobody answers` A takes effect, because it is what the roster shows today

### A1 · 🚪 A neighbour unit, on this board because its standard is load-bearing
- ✅ A1.1 · Met. `### 1` carries the door test, its verdict, and what the exclusion bought.

### A2 · 🔢 The judgment is one step, and code fences it on both sides
- 🧠 A2.1 · Waiting on the owner. The evidence is in: the 260805-06 one-door rebuild left no copy of the three contracts in the paper tree, `haipipe-paper-revise-content` and the old DRAFT phase sit in `paper/_old/`, and the humanizer moved to `skills/writing/`. Only the tick is missing.
- ⬜ A2.2 · Not started. No `score` run has been used to choose what this board rewrites.

### A3 · ✎ Two units now write the same `✎` record
- ⬜ A3.1 · Not started. `cli/agree.py` shipped at 0.6.0 for exactly this shape and has never been pointed at the pair.

### A4 · 📋 The roster's scope beyond `skills/board/`, widened but not settled
- 🧠 A4.1 · Waiting on JL, in Decision Now above.

### P · Page-level
- ✅ P1 · Met. The unit ships at 0.6.1 after 7 releases and is healthy in the ordinary sense: two deterministic code verbs, its contracts collected in one place, and tests. The `🟡` is about position, not quality.

## Files
### 📋 Contracts · what CARRIES a rule to other pages
- `skill/haipipe-writing/ref/change-record.md`
  §4 keeps the board dialect and the LaTeX dialect in one file, which is what stops the record grammar splitting in two.
- `skill/haipipe-writing/ref/plain-rules.md`
  The weak-English standard the rewrite step is measured against.
- `haipipe-board/ref/writing-rules.md`
  The board's own prose standard, which is what a page is checked against. Not this unit's file, and the reason this unit is on the board at all.
### ⚙️ Engines · what RUNS this subject
- `../../writing/haipipe-writing/cli/score.py`
  The read-only ranking verb. Start here for Aim A2.2.
- `../../writing/haipipe-writing/cli/wdiff.py`
  Both `apply` and `check`, which is why the verb count reads three or four depending on where you look.
- `../../writing/haipipe-writing/cli/agree.py`
  Compares two statements of one fact. The instrument Aim A3.1 needs, never yet pointed at the pair.
### 📤 Output files · what a BUILD writes
- `board/QS/QS5-writing.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit it; the markdown is the only source.

## Law
- 260802 JL · 📋 **On the roster is not in the family**: a unit may be argued on this board without shipping from it
  `haipipe-writing` ships from `writing/haipipe-writing/` and is here because the board is one of its hosts.
  The option rejected was folding it into `skills/board/`, which would have tied a general writing verb to one host; the door test on `QC1b` §1.3 sent it out for that reason.
- 🔒 **The judgment is one step**: a model rewrites, and code does everything either side of it
  `score` ranks and changes nothing, and `wdiff.py` computes the diff and anchors the record.
  A diff a model wrote cannot be re-derived from the two texts, and a record a model placed can attach to the wrong sentence, so neither act is a model's.

## Glossary
- ✎ **change record**: the lane written under a sentence that was rewritten, reading `> ✎ the sentence with ~removed~ *added* words · WHO · YYMMDD HHMM`.
- 🚪 **the door test**: the question on `QC1b` §1 that decides family membership, asking whether some consumer needs a unit's rules with no board open.
- 🏠 **host**: any tree whose authored prose this unit acts on. The board is one host; a paper and a README are others.

## Log
- 260816 · [REVISE-CC] `Design-4` became `QS5`, the Design kind folded into the Q series on JL's call: the unit rides the Q page that argues it, so the page keeps its subject and gains a Q id, with its `skill/haipipe-writing/` plugin and `draw/` scene moving under the new name. Brought to the Q page contract in the same round: the Opening now leads with a question, `## Writing Style` and `## Files` were added, the two thin Content divisions became four that carry the page's real material, each with a face figure and numbered paragraphs, the flat Aims list became `A1` to `A4` groups with `Done when` lines, `## States` became one row per Aim, and the unsettled roster scope became a `### Decision Now` row with its three options. `page-type: design` was dropped, and Content §2's "selection record adopted from the specimen" went with the Design kind that needed it.
- 260816 · [MOVE-CC, JL ruled] the page moved from QPs-page-structure to QS-sentence: `haipipe-writing`'s product is the `✎` sentence lane, the grammar `haipipe-sentence` owns, so the two producers of that one record now sit in one chapter; board.md's roster, alias map, and QA00 §6 swept in the same edit.
- 260815 1230 · [REVISE-CC] converted to a for-design page (JL 260815): the three managed spans left the file, `skillpage.py plug` wrote the unit's contract surface to `skill/haipipe-writing/`, and Content §2 adopts the selection recorded on the specimen.
- 260806 2118 · [REVISE-CC] swept to the 260806 architecture; the two-dialect pointer now reads `ref/change-record.md` §4 (disk truth, §3 is placement), `cli/agree.py` is credited to 0.6.0 not the latest release, and the paper-family migration clauses now state the one-door outcome: no copies left in the paper tree, humanizer relocated to `skills/writing/`, plugin count 158
- 260806 0140 · [REVISE-CC] card synced to disk truth after 260805 (ten types · thin-paper phase 2 · first live RUN); the "two days ago" migration clause now says 260801 and the board page count reads 57, with no 260805 change touching this unit.
260802 2100 · Corrected one claim after `haipipe-sentence` reached 0.3.0: this page said that skill owns what a `✎` line IS while this one owns when it gets written, and its new `edit` verb now writes one too. Two producers of one record is a new Aim, and `cli/agree.py` is the obvious instrument since it already compares two statements of one fact
260802 2000 · Page opened at JL's request to add `skills/writing` to the roster, and written to `haipipe-page-for-skill` 0.1.0. It is the first skill page for a unit outside `skills/board/`, which widens `QC3a`'s 260727 scope ruling; the open question of where the new line falls is an Aim here and a Decision Now row on `QC3a`
260802 2000 · page generated from `writing/haipipe-writing/` by `skillpage.py new`
