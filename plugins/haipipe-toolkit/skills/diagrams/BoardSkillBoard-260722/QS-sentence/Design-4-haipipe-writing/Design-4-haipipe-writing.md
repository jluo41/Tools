# Design-4 · Writing (Skill haipipe-writing v0.6.1)
state: 🟡 in flux · 7 releases, and the board is one of its hosts
owner: JL
page-type: design
method: unit snapshot in skill/ via skillpage.py plug; every section authored by hand (converted from the mirror kind 260815)

## Opening
`haipipe-writing` takes prose somebody already wrote and makes it readable to a person whose English is weak, then records every word it changed under the sentence it changed.
Load it when the problem is the PROSE, whatever file holds it; every other unit on this roster is about the board, and this one is about writing and works on a README or a paper section just as well.
Two of its verbs are code, so a model never computes a diff and never places a record.

**Why it is on a board about boards**: It is the only unit here that lives outside `skills/board/`, and it is on this board because the board is one of its hosts: `ref/writing-rules.md` is the standard every page is judged against.

**What the verbs are, and why the count is confusing**: `score` reads prose and ranks what is worth rewriting, and changes nothing.
`rewrite` is the only step a model does, and it produces new prose beside the old.
`apply` then computes the word-level diff in code and anchors a `✎` record under the sentence it changed, and `check` audits that every record is well formed and attached to something.
That is four steps under three named verbs, because `apply` and `check` are both `wdiff.py`; the unit's own summary says three and its own figure numbers four.
A `✎` record reads `> ✎ the sentence with ~removed~ *added* words · WHO · 260802 1720`, which is the same lane grammar `haipipe-sentence` owns.

**Why it is not part of this family**: the test on `QC1b` §1 asks whether some consumer needs a unit's rules with no board open, and `haipipe-writing` passes it too easily.
Its consumer is ANY authored prose in the repo: a board page, a `SKILL.md`, a README, a grant application section.
Folding it in would have tied a general writing verb to one host, so the test sent it OUT of the family rather than into it (`QC1b` §1.3, 260802).
It is host-agnostic by construction, and `ref/change-record.md` §4 writes the board dialect and the LaTeX dialect down together so the two cannot drift into two ideas.

**Covered elsewhere**: `haipipe-board/ref/writing-rules.md` is the board's own prose standard and is what a board page is checked against; this skill is the verb that acts on prose anywhere.
`haipipe-paper-revise-humanizer` rewrites ACADEMIC prose for a venue and keeps the venue's voice, so the two share machinery and not judgment: the humanizer calls `cli/wdiff.py` rather than writing its own diffs.
`haipipe-sentence` owns what a `✎` line IS on a board, and since its 0.3.0 on 260802 it also RUNS an `edit` verb that writes one.
So two units now produce the same record: that verb writes one when a person retypes a sentence in the browser, and `cli/wdiff.py apply` writes one when this skill rewrites prose anywhere.
They agree today because both follow the same grammar, and nothing checks that they still will.

**Where it stands**: 7 releases to 0.6.1, with 0.6.0 adding `cli/agree.py`, which compares two statements of one fact after three defects on 260802 all turned out to be that shape.
It is the newest home for three contracts that used to live in the paper family, `ref/ai-tells.md`, `ref/weaving.md` and `ref/holes.md`, all migrated on 260801; the 260805-06 one-door rebuild of the paper family left no copy of the three in the paper tree, and the humanizer itself now lives beside this unit in `skills/writing/`.
No `score` run has been used to choose what this board rewrites, which is the obvious next use and has not happened.

## Writing Style
English only. One sentence per source line. Describe the shipped unit factually and keep generated inventory separate from human health judgment.

## Diagram
**What sits in this page's `skill/` plugin**: the unit's contract surface, written by `skillpage.py plug` and renamed so neither the installer glob nor page discovery can mistake it for the live unit.

```
skill/haipipe-writing/
  CHANGELOG.md
  SKILL.snapshot.md
  ref/ai-tells.md
  ref/change-record.md
  ref/holes.md
  ref/plain-rules.md
  ref/weaving.md
```

**Where the judgment sits, and where it must not**: two of the three verbs are code, so a model never computes a diff and never places a record.

```text
WORKFLOW  one judgment step, fenced by code on both sides

  📄 authored prose · a board page · a SKILL.md · a README · a paper section
        │
        │ 1️⃣ cli/score.py        🤖 CODE · ranks what is worth rewriting
        ▼                          read-only, it never rewrites
  📋 a ranked worklist ── a person reads it, nothing has changed yet
        │
        │ 2️⃣ rewrite             🧠 JUDGMENT · the ONLY step a model does
        ▼
  ✍️ new prose, beside the old
        │
        │ 3️⃣ cli/wdiff.py apply  🤖 CODE · computes the diff, anchors it
        ▼
  📝 prose + `> ✎ ~removed~ *added* · WHO · YYMMDD HHMM`
        │                          under the sentence it changed
        │ 4️⃣ cli/wdiff.py check   🤖 CODE · every record well formed
        ▼                          and attached to a real sentence
  ✅ readable, and reviewable

  🔒 the judgment is step 2, and ONLY step 2
  🚫 a model never writes the diff and never places the record

  ── why this unit is on a board about boards ─────────────────────
  it is HOST-AGNOSTIC and lives outside skills/board/. The board is
  one host among several, and ref/change-record.md §4 keeps the board
  dialect and the LaTeX dialect in one file so they cannot drift.
```

## Content
### 1 · What this unit is, in one screen
**Live and snapshot**: the unit ships from its own folder, and this page judges a plugged copy.
```text
  ⚙️ the live unit, ships        📋 skill/haipipe-writing/
     from its own folder    ──▶     the snapshot this page's
                            plug    judgments are about
```
`haipipe-writing` is the NEIGHBOUR unit: it ships from `writing/haipipe-writing/`, outside this family, and owns the prose standard every page here is judged against.
It sits on this board because `ref/writing-rules.md` is load-bearing for every page, not because the family ships it.

### 2 · Selection record · adopted from the specimen
**Where the record lives**: one argument, one home, adopted by reference.
```text
  🅰🅱 the candidates + full record ──▶ QPs1-overall · Content §11.2
  📄 this page keeps only what is its own: health · aims · snapshot
```
This page converted to a for-design page under the 260815 ruling that retired the mirror kind.
The candidates and the full record are written once, on `QPs1-overall` Content §11.2.
This page adopts that selection rather than restating it, because seven copies of one argument would recreate the form-letter failure the ruling killed.
What is page-specific stays here: the Opening, the Aims, the States judgment on the unit's health, and the plugged snapshot above.

## Aims
- [ ] 🧹 The paper family stopped keeping its own copies
      `ref/ai-tells.md`, `ref/weaving.md` and `ref/holes.md` migrated here on 260801 out of `haipipe-paper-revise-humanizer`, `haipipe-paper-revise-content` and the paper DRAFT phase.
      A migration is finished only when the old home points at the new one.
      The 260805-06 rebuild changed the ground: the paper family is one door now, `haipipe-paper-revise-content` and the old DRAFT phase sit in `paper/_old/`, the paper tree keeps no copy of the three, and the humanizer moved to `skills/writing/` beside this unit.
      What is left is for the owner to close this aim on that evidence.
- [ ] ✎ The two producers of a `✎` record are checked against each other
      `haipipe-sentence` 0.3.0 added an `edit` verb that writes a change record, and `cli/wdiff.py apply` here writes one too.
      One grammar with two independent implementations is the shape `cli/agree.py` was built for, and it has never been pointed at this pair.
- [ ] 📊 One `score` run picks what this board rewrites next
      The verb ranks prose against the weak-English test and it has never been pointed at this board's 57 pages.
      Today's roster rewrite was chosen by JL reading Openings by eye, which is exactly the work `score` exists to replace.
- [ ] 🪞 The roster's scope beyond `skills/board/` is settled, not just widened
      `QC3a` ruled on 260727 that this roster covers `skills/board/` and nothing else, and JL widened it on 260802 by asking for this page.
      What is still unstated is where the new line falls: this one neighbour, every family the board depends on, or all 158 skills in the plugin.

## States
This unit ships at 0.6.1 after 7 releases and is healthy in the ordinary sense: its two code verbs are deterministic, its contracts are collected in one place, and it has tests.
Its `🟡 in flux` is about position rather than quality, because it absorbed three contracts from another family on 260801 and the board has not yet used the verb the unit exists to provide.

- 260802 JL · 🪞 Added to the roster, which widens a ruling rather than following one
  JL asked to add the `skills/writing` units to this board, and this is the only one there.
  `QC3a`'s 260727 scope ruling said the roster covers `skills/board/` and nothing else, so this page is JL answering the row that page explicitly left open rather than an exception slipped past it.
  The reason it is a sound widening: this unit is not a stranger to the board, it owns the prose standard every page here is judged against.
- 260802 CC · ✎ A second writer of its record appeared the same day
  `QB8` closed and `haipipe-sentence` took three verbs, one of which writes the `✎` change record this skill also writes.
  `ref/change-record.md` §3 already keeps the board dialect and the LaTeX dialect in one file so they cannot drift; what is new is two implementations of the BOARD dialect, which that file was not written to cover.
- 260802 CC · ⚖️ It was tested for membership in the board family once, and failed on purpose
  `QC1b` §1.3 applied the door test to it and sent it OUT: its consumer is any authored prose in the repo, so folding it in would have tied a general verb to one host.
  Being on the roster is not the same as being in the family, and this page is the first row that makes that distinction visible.

## Log
- 260816 · [MOVE-CC, JL ruled] the page moved from QPs-page-structure to QS-sentence: `haipipe-writing`'s product is the `✎` sentence lane, the grammar `haipipe-sentence` owns, so the two producers of that one record now sit in one chapter; board.md's roster, alias map, and QA00 §6 swept in the same edit.
- 260815 1230 · [REVISE-CC] converted to a for-design page (JL 260815): the three managed spans left the file, `skillpage.py plug` wrote the unit's contract surface to `skill/haipipe-writing/`, and Content §2 adopts the selection recorded on the specimen.
- 260806 2118 · [REVISE-CC] swept to the 260806 architecture; the two-dialect pointer now reads `ref/change-record.md` §4 (disk truth, §3 is placement), `cli/agree.py` is credited to 0.6.0 not the latest release, and the paper-family migration clauses now state the one-door outcome: no copies left in the paper tree, humanizer relocated to `skills/writing/`, plugin count 158
- 260806 0140 · [REVISE-CC] card synced to disk truth after 260805 (ten types · thin-paper phase 2 · first live RUN); the "two days ago" migration clause now says 260801 and the board page count reads 57, with no 260805 change touching this unit.
260802 2100 · Corrected one claim after `haipipe-sentence` reached 0.3.0: this page said that skill owns what a `✎` line IS while this one owns when it gets written, and its new `edit` verb now writes one too. Two producers of one record is a new Aim, and `cli/agree.py` is the obvious instrument since it already compares two statements of one fact
260802 2000 · Page opened at JL's request to add `skills/writing` to the roster, and written to `haipipe-page-for-skill` 0.1.0. It is the first skill page for a unit outside `skills/board/`, which widens `QC3a`'s 260727 scope ruling; the open question of where the new line falls is an Aim here and a Decision Now row on `QC3a`
260802 2000 · page generated from `writing/haipipe-writing/` by `skillpage.py new`

