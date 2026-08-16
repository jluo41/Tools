# Design-5 · The Sentence (Skill haipipe-sentence v0.4.1)
state: 🟡 in flux · became a door 260802; four releases that day, all now in the changelog
owner: JL
page-type: design
method: unit snapshot in skill/ via skillpage.py plug; every section authored by hand (converted from the mirror kind 260815)

## Opening
`haipipe-sentence` is the contract for one source line, the board's smallest addressable thing, and since 260802 it is also the door that runs three verbs on one.
A line renders as one row a reader can click.
Two things attach to that line and they are not the same: a card takes a few marked WORDS and renders inside the sentence, and a `>` lane takes the whole line and renders under it.

**Since when it is a door**: say `comment on "<the sentence>"`, `edit "<the sentence>"` or `card on "<the words>"` and this skill runs that verb.
`haipipe-page` is what you reach for when the question is which SECTION a write belongs in rather than which line.

**What the words mean**: an address like `QB8.C1.P1.S1` points at one sentence, reading page `QB8`, Content division 1, paragraph 1, sentence 1.
A lane is a signed `>` line written beneath that sentence, such as `> Comment JL …` for a person's remark or `> ✎ the sentence with ~removed~ *added* words · CC · 260802 1720` for a change record.
A card is different: `> Card the words: what to show` quotes a span from the line above, and the reader sees those very words carry a panel, keeping the prose's own font, colour and weight.

**What changed on 260802**: `QB8` closed with all 16 of its Aims met and JL moved the line on what this unit is.
It stopped being only a thing an agent LOADS and became a thing a person RUNS, with three verbs that write to one line: comment, edit, card.
The rules the verbs share are the interesting part, because each is a scar: the anchor is an exact match on the source line and a miss fails visibly, a form must close before it asks for the repaint so a rebuild cannot eat a half-written comment, and a duplicate sentence is REFUSED rather than guessed at.

**Covered elsewhere**: which section a write lands in, and what a whole page owes its reader, belong to `haipipe-page`.
Rendering the line (`src/body.py`), the write path (`live/write.py`) and the popover a card opens in are `haipipe-board`'s, and locks and concurrent writers are `QE4`'s.
The grammar's authority is `haipipe-board/ref/board-form.md` §5, which this spec cites and is forbidden to fork.

**Where it stands**: 0.1.0 to 0.3.0 in two days, and the door half, shipped 260802, still has nothing measured against it.
Its three named consumers are still only named: `live/chat.py`, whose duplicated lane rules justified cutting this spec out in the first place, still teaches the grammar from its own Python prose.
The release that made it a door shipped with no changelog entry and `cli/agree.py` caught it; the entry was reconstructed from the shipped file on 260802 and the tool now reports clean.

## Diagram
**What sits in this page's `skill/` plugin**: the unit's contract surface, written by `skillpage.py plug` and renamed so neither the installer glob nor page discovery can mistake it for the live unit.

```
skill/haipipe-sentence/
  CHANGELOG.md
  SKILL.snapshot.md
```

**Two anchors, three verbs**: what attaches to a few WORDS renders inside the line; what attaches to the LINE renders under it.

```text
WORKFLOW  one line, two anchors, and the three verbs that write to it

  ONE source line  =  ONE row on the page  =  ONE anchor
  prose is one sentence per line; check.py warns on a hard wrap,
  because a wrapped sentence renders as a broken row
        │
        ▼
  QB8.C1.P1.S1     page · Content division · paragraph · sentence
                   UPPERCASE and digit tokens only, so a section
                   slug can never collide with a coordinate
        │
   ┌────┴─────────────────────────┐
   ▼                              ▼
 🪪 ON THE WORDS                 📎 ON THE LINE
   > Card the words: …             > Comment WHO …      a person's remark
   quotes a span above             > ✎ ~old~ *new* …    the change record
   renders INSIDE the             > Citation: · Value:  the typed lanes
   sentence, keeping the           renders UNDER the line
   prose's own font and            badge says which kind is below:
   colour                          💬 waiting ▸ ✎ change ▸ ⚑ lane

  ── the three verbs it now RUNS (0.3.0, JL moved the line 260802) ──
  💬 comment on "<the sentence>"   ✎ edit "<the sentence>"
  🪪 card on "<the words>"
     · the anchor is an EXACT match; a miss FAILS VISIBLY
     · a form CLOSES before the repaint, or the swap refuses it, so a
       rebuild cannot eat a half-written comment
     · a duplicate sentence is REFUSED, never guessed at
     · a write needs serve.py; with it down the page keeps a pending
       line and never grows a comment area at its foot

  ── the boundary ──────────────────────────────────────────────────
  this says what a sentence IS and runs the three verbs on one.
  haipipe-board RENDERS it (src/body.py), WRITES it (live/write.py)
  and serves the popover. haipipe-page owns which SECTION.
  QE4 owns locks. board-form.md §5 is the authority this must not fork.
```

## Content
### 1 · What this unit is, in one screen
**Live and snapshot**: the unit ships from its own folder, and this page judges a plugged copy.
```text
  ⚙️ the live unit, ships        📋 skill/haipipe-sentence/
     from its own folder    ──▶     the snapshot this page's
                            plug    judgments are about
```
`haipipe-sentence` is the SPEC and DOOR for the atomic unit: one line, its `>` lanes, the evidence card, and the archive-never-delete record lifecycle.
The live unit ships from `board/haipipe-sentence/`.

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
- [x] 📓 The release that made it a door is written down
      `cli/agree.py` reported `SKILL.md says 0.3.0 · CHANGELOG.md shipped 0.2.0`, so the three verbs shipped with no changelog entry at all.
      Reconstructed from the shipped file on 260802 and marked as reconstructed, since it was written after the fact rather than at release time; the tool now reports clean.
      The finding came from `Skill-7`'s own tool pointed at this family, which is the first time one skill page checked another.
- [ ] 🧪 Something is measured against the door half
      It gained three verbs on 260802 and nothing has exercised them from this contract: no run, no fresh agent choosing this door, no check that the exact-match anchor fails visibly the way the page says it does.
      Its two shared rules read as scars from real incidents, which is a good sign about their origin and no evidence at all about their current state.
- [ ] 🧹 `live/chat.py` loads this spec instead of restating it
      Two of its four rule strings teach the lane grammar in Python prose, and `QB8d` caught one describing a page shape that no longer existed.
      This is `A6.1` on `QC1b`, it is the consumer whose duplication justified cutting this spec out, and it still has not become a consumer.
- [ ] 🔗 The no-fork promise is checked, not just written
      This contract cites `haipipe-board/ref/board-form.md` §5 as the authority and promises never to fork it, and it doubled in size to 191 lines while nothing verified that promise.
      A spec that quietly restates its authority is the exact failure it was cut out to prevent.

## States
The ground moved under this page on 260802: `QB8` closed with all 16 Aims met, and this unit went from a 94-line contract an agent loads to a 191-line door a person runs, across three releases in two days.
Its health is `🟡 in flux` for one reason now: the door half, shipped 260802, still has nothing measured against it.

- 260802 JL · 🚪 It stopped being only a SPEC
  `QB8` settled the sentence as the board's atomic unit and handed each attachment its own page, and the skill followed by taking three verbs: comment, edit, card.
  The roster on `QC1b` had it filed as a pure SPEC beside `haipipe-page`, which is now half true, and the same misfiling is what hid `haipipe-board-index`'s duplication for two days.
- 260802 CC · 📓 A tool built one page over found the drift on this one
  `Skill-7`'s `cli/agree.py` compares two statements of one fact and reported this unit's `SKILL.md` at 0.3.0 against a changelog shipping 0.2.0.
  That is the first time a skill page was checked by another skill page's engine rather than by a person reading it, which is worth more than the defect it found.
- 260802 CC · ⚠️ This page contradicted itself for several hours
  The derived Content span carried `Three verbs, and this skill is the door for all of them` while the authored fence directly above it still read `loaded, never run`.
  A sync updates the derived half and cannot touch the authored one, so a page can be green on `skillpage.py check` and self-contradictory on screen, which is the sharpest example yet of why that check covers frontmatter only.

## Log
- 260815 1230 · [REVISE-CC] converted to a for-design page (JL 260815): the three managed spans left the file, `skillpage.py plug` wrote the unit's contract surface to `skill/haipipe-sentence/`, and Content §2 adopts the selection recorded on the specimen.
- 260806 2115 · [REVISE-CC] swept to the 260806 architecture; head state line's release count corrected from three to four (CHANGELOG dates 0.1.1, 0.1.2, 0.2.0 and 0.3.0 all to 260802), every cited path and pointer verified live
- 260806 0140 · [REVISE-CC] card synced to disk truth after 260805 (ten types · thin-paper phase 2 · first live RUN); the "one day old" age clauses on the door half now date it 260802 instead, and no 260805 change touched this unit.
260802 2030 · Rewritten after `QB8` closed and this unit reached 0.3.0: the Opening and the `WORKFLOW` fence had said `loaded, never run` while the page's own derived Content announced three verbs. Four Aims replace the earlier set, including the missing 0.3.0 changelog entry that `agree.py` found, and `state:` now names the two live problems rather than the one it had
260802 1720 · Authored half written: the `WORKFLOW` fence replaced the template placeholder with the address, the three consumers and the boundary, four real Aims replaced the single health placeholder, and `state:` moved from 🔴 to 🟡 in flux. Recorded plainly that this unit's consumers are declared rather than measured, and that `live/chat.py`, the consumer that justified cutting it out, still carries its own copy
260731 1116 · page generated from `board/haipipe-sentence/` by `skillpage.py new`

