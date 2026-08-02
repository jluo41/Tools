# The words this family uses
state: 🟡 PARTIAL · collected 260729 · refreshed 260731; JL has not read it as a glossary
owner: JL
method: one entry per concept, each the source documents' own word; a coined word is a defect

## Opening
What does each recurring Board term mean, and where is its authoritative definition?

This page gives the family one shared vocabulary for Boards, pages, sections, states, and sentences.
The hard part is that ordinary words such as Board and page refer to several different objects in this system.
Unclear names make neighbouring pages re-explain the same concept and eventually disagree.
It succeeds when a cold reader can follow any page without guessing which object a term names.

**Covered elsewhere**: Where things LIVE: `QB1`. This board's own structure: `board.md ## Board Structure`. A single page's internal glossary stays that page's `## Glossary`.


## Content
### 1 · The Board family
The FAMILY that ships: `skills/board/` (five skills + one agent since 260731; the roster is `QC6` §8).
The SKILL you invoke: `/haipipe-board`; a subskill is a unit nested inside the family folder, never a peer of it (`QA0`).
One topic's `Board-Folder`: `01-boardform-260722/`.
The Board-level SOURCE: `board.md` (Spine · Close · Topic · Pipeline · Board Map · optional Board-Structure · Pages · Links).
The generated `Board-Webpage`: `board.html`, never hand-edited.
The `Board-Webpage-Index` is its `#top` view; a `Board-Webpage-Page` is the focused Q/S view after a page row opens.

### 2 · The page family
page / face: one `Q*.md` or `S*.md`; Q is a decision (closes when its checkboxes close), S is a lifecycle stage (closes at its human gate); one layout serves both.
Skill-<unit> / Agent-<unit>: the two mirror kinds (260731); a Skill page mirrors a LOADED unit and closes when it ships, an Agent page mirrors a DISPATCHED one, and neither counts toward settled.
section: a `##` heading inside a page; the on-stage order is fixed (`QB4`), and the renderer knows sections only through `ALIAS` (`src/common.py`).
Opening: the lead section's one name on every page kind (260731); `Question` survives only as a legacy alias, so older pages parse forever.
group: a `###` heading in `## Pages`, one folder per group (`QB1`); the id letter records the group a page was OPENED under, not where it is listed today (260729).
state: the first emoji of the `state:` line (🔴 OPEN · 🟡 PARTIAL · ✅ SETTLED · ⏸️ ON HOLD); the suffix is human-readable and never a fifth state.

### 3 · The sentence family
sentence: the atomic row, one per source line (`QB5`).
apparatus / lane: a typed `>` line bound to the sentence above it by adjacency (`QB5 §4`).
comment: a sentence-local `> Comment WHO` row written directly below the sentence it discusses (`QB5 §5`); the former page-bottom queue and its open/solved lifecycle are retired.
edit record: a sentence-local `> ✎` row recording one saved whole-sentence change (`QB5 §6`).
card: a panel opened by clicking a few marked words INSIDE a sentence, written `> Card the words: what to show` (`QB5 §3`).

### 4 · The working vocabulary
decision: what a Q face settles; the word replaced "ruling" on 260729 (JL). A settled decision GRADUATES: its `## Law` is copied into `SKILL.md` (operating rules) or `ref/` (specs), and only then binds.
standing: whether this family may make a given write into a board it renders but does not own; mechanical writes have it, editorial writes do not (`QB1` §4).
spine / close: board.md's one-line purpose and its acceptance condition.
sync / write-back: work done in a round is written back to its owning face the same round; "done" means written back.
managed span: a block between `<!-- haipipe:...start -->` and `end` markers that a script owns (`stage.py`, `skillpage.py`); authors never edit inside.
🧩 Skills: the Where-we-are item listing what a face governs and whether it landed (`QB4e`).

## Aims
- [ ] 🧠 JL reads it once as the glossary and strikes or adds entries
- [ ] 📖 Each entry names its defining face or file, so the glossary never becomes a second source

## States
Collected 260729 from `SKILL.md`, `ref/board-form.md`, and the faces named per entry; nothing here is defined for the first time.

- 260802 CC · 📖 The retired section names are now enforced, not just written down
  `Opening` had been the canon since 260731 and `src/common.py` aliases the old names, so every
  page kept rendering correctly and nobody could see the drift: 45 of 55 pages were still on
  `Question` / `Items to Finish` / `Where we are`, and 26 still carried the retired `## Boundary`.
  All 45 were renamed and all 26 retired; `check.py` now reports any of them as `retired-section`.
  Archived pages keep theirs, because rewriting an archive would falsify a record.

- 260731 CC · 📖 Refreshed to the post-restructure state
  The family entry now counts five skills and one agent, the page family gained the Skill and Agent mirror kinds and the `Opening` canon, `board.md` gained its Board Map section, and every pointer moved to its live id (`QAa0`→`QB4`, `QAb0`→`QB5`, `QAb1`→`QB5a`, `QA6`→`QB5b`, `QAb2`→`QB5c`, `QAa5`→`QB4e`).
  Nothing was defined here for the first time; every refreshed entry points at the face or ruling that owns it.

### Decision Now
These are the calls only JL can make; CC ticks nothing here.

- [ ] 📖 Rule what `face` means, because two authorities disagree
      📍 Part 2 · The page family.
      🔔 Why now: this page's line 25 says `page / face` are the SAME thing, while
      `haipipe-board-page/SKILL.md` line 267 says a face is `a page whose id carries its
      parent's number` (`QB4a` under `QB4`). Both are written down as definitions.
      ⭐ A: they are synonyms, and a child page is a `child`, not a `face`.
      ⭐ B: `face` means only the child form, and a plain page is never called a face.
      🛑 Blocks: page authors read one of the two and write the other word.
      🤖 If nobody answers: CC follows A, because 45 pages were just reworded from
      `face` to `page` on the weak-English axis and A is what that wording assumes.

- [ ] 🧠 Read this page once as the glossary
      Strike any entry you would not say yourself, and name any word the family uses that is missing.
      CC refreshed every entry to the 260731 state first, so what you read is current.
- [ ] 📖 Rule that every entry must name its defining face or file
      → CC's proposal: yes; an entry that defines instead of pointing would make this glossary a second source, which is the defect it exists to prevent.

## Files
- `src/common.py`
  `ALIAS`, the machine half of "section".
- `ref/board-form.md`
  The full grammar the words come from.

## Log
260731 · Refreshed after the restructure rounds: roster, page kinds, Opening canon, Board Map, live ids
260729 · Opened on JL's ask ("what are the concepts we used"), the same round QB1 became the two-folder map
