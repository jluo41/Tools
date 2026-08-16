# Design-1 · The Board (Skill haipipe-board v0.133.0)
state: 🟡 in flux · 168 releases in 15 days, 3 open defects
owner: JL
page-type: design
method: unit snapshot in skill/ via skillpage.py plug; every section authored by hand (converted from the mirror kind 260815)
session: e95d488f-0b05-4425-b8e0-6836fbfccc02


> ARCHIVED 260816. This page dissolved into `QB1` the way `QPs00` dissolved into `QPs1`: the `haipipe-board` unit now rides `QB-board/QB1-form/skill/haipipe-board/` and the 260723 demo note rides `QB-board/QB1-form/meeting/`. `Design-1`, `Skill-0` and `Q-Skill-haipipe-board` all resolve here through `board.md`'s `## Links`.

## Opening
`haipipe-board` is the door you walk through to run a board: `build.py` turns a folder of markdown pages into a site, and `serve.py` keeps it live so comments land back in the markdown.
Reach for it when the BOARD is the subject: opening one, viewing one, changing its groups or roster.
One page is `haipipe-page`'s job; one write onto a page is `haipipe-board-routing`'s.
It moves fast: 168 releases since 260722, and three open defects.

**What a board is**: A board is one folder of markdown.
`board.md` carries the spine, the closing condition and the `## Pages` roster; one `.md` file carries one decision (Q) or one lifecycle stage (S).
The board this page belongs to is `skills/diagrams/BoardSkillBoard-260722/`, and the file you are reading sits in its `QC-engine/` group folder.
The markdown is the single source: `build.py` only reads it, the live layer only appends to it, and nothing but `build.py` writes `board.html`.

**What the door runs**: `## Content` part 5 owns the current list of actions: eight offline (`view · open · add · stage · build · sync · link · close`) and three live (`serve · excalidraw · comment`).
`view` is the common one, and it rebuilds the board before handing `board/index.html` to the reader's browser, because a board opened without that rebuild shows yesterday's page.
Creating, updating, and running one Page are named here and routed to `haipipe-page`, because whoever asks is looking at one Page.

**Covered elsewhere**: the family is one Board door plus Page and sentence contracts, Page Type and Page Phase catalogs, and the routing verb, so this skill routes instead of restating them.
`haipipe-page` is the spec for what a page is, and `haipipe-sentence` is the spec for everything below the section, such as a comment lane written under one sentence.
`haipipe-board-routing` is the write verb at both altitudes: one input onto its owning page, and `board.md`'s own structure, which it absorbed when `haipipe-board-index` retired on 260802.
`haipipe-board-creator-agent` produces Page work, `haipipe-board-reviewer-agent` performs fresh read-only CHECK, and `haipipe-page-orchestrator-agent` runs and audits one bounded automatic lifecycle.

**What is unproven here**: `live/chat.py` teaches an agent the page and board rules from four hand-written strings rather than loading the specs, and one of those strings was already caught describing a page shape that no longer existed.
`skillpage.py check` hashes the frontmatter only, so a green check says the metadata is current and not that this page's copy of a `SKILL.md` still matches the file it mirrors.
Nothing measures whether the manual stays short, which is what `QC1a`'s Law asks of it.
All three sit in `## Aims`, and two of them arrived from other pages because this skill ships the file.

## Diagram
**What sits in this page's `skill/` plugin**: the unit's contract surface, written by `skillpage.py plug` and renamed so neither the installer glob nor page discovery can mistake it for the live unit.

```
skill/haipipe-board/
  CHANGELOG.md
  SKILL.snapshot.md
  ref/board-example.md
  ref/board-form.md
  ref/page-lifecycle.workflow.js
  ref/page-template.md
  ref/topic-display-card.md
  ref/topic-entry-contract.md
  ref/writing-rules.md
```

**How the door is used, and what every part writes into**: markdown is the only source, and the generated site is output nothing else may touch.

```text
WORKFLOW  one folder in, one site out, and every writer aimed at the markdown

  A BOARD IS A FOLDER.  md is the only source; board/ is output.
  ─────────────────────────────────────────────────────────────────
  board.md          spine · close · Topic · Pipeline · Pages
  QA-<group>/       one .md per decision (Q), stage (S), or skill page
        │
        │  build.py          md -> board/ · index · one page per group
        ▼                    asserts: strip every <script>, all prose remains
  board/index.html
        │
        │  watch.py          rebuild on any .md change
        │  serve.py          the LIVE layer, one server for the whole repo
        ▼
  http://…:5599/<board>/board/index.html
        │
        ├── comments land back in the md            (QB8)
        ├── ＋Q / ＋Group / archive edit board.md    (QA2)
        ├── an excalidraw frame per page            (QB4 · QB7)
        ├── chat + terminal per page                (QD1-3)
        └── ACTIVITY counts updates from ## Log     (QD7)

  WRITERS, all of them into markdown, never into board/
  ─────────────────────────────────────────────────────────
  stage.py      new/sync/check   an S page + its managed Stage Contract
  skillpage.py  new/sync/check   a skill folder -> this very page (Skill-6)
  regroup.py    [--apply]        root pages -> one folder per Q group
  xcal.py       [--wire]         one scene per board, one frame per page

  READ-ONLY
  ─────────
  check.py      structure · dead links · stale claims   (QF1)
  status.py     the three-line closing block            (QD6)
  refs.py       a paper's bibliography, cached

  THE INVARIANT EVERY PART OBEYS
  ──────────────────────────────
  the markdown is the single source. build.py only reads it, the live
  layer only appends to it, and nothing but build.py writes board/.
```

## Content
### 1 · What this unit is, in one screen
**Live and snapshot**: the unit ships from its own folder, and this page judges a plugged copy.
```text
  ⚙️ the live unit, ships        📋 skill/haipipe-board/
     from its own folder    ──▶     the snapshot this page's
                            plug    judgments are about
```
`haipipe-board` is the family's one DOOR and its engine: the renderer, the checker, the write-back server, and every script a board runs on.
The live unit ships from `board/haipipe-board/` with `cli/`, `src/`, `live/`, `assets/`, and `tests/` beside the contract files.

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
- [ ] 🧹 `live/chat.py` stops restating the specs it should load
      Four rule strings there teach an agent the page and board contracts in Python prose: `CHAT_RULES`, `BOARD_CHAT_RULES`, `FULL_RULES` and `BOARD_FULL_RULES`.
      None of them reads `ref/` or either spec, and `QB8d` already caught one describing a page shape that no longer existed.
      They ship in this skill, so this is the door's defect to carry rather than the specs': `QC1b` calls it the family's one real defect, and the fix costs one function and adds no version surface.
- [ ] 🔍 `skillpage.py check` reports PROSE drift, not just frontmatter drift
      `digest()` hashes the derived facts only (`name`, `version`, `last_updated`, `summary`, `allowed-tools`), by its own docstring, "so prose edits never look like drift".
      A ✅ therefore means the metadata is current, not that the page's copy of a `SKILL.md` still matches it, and byte equality needs a regenerate-and-diff done by hand.
      `Skill-1` found this on 260801 and correctly sent it here, because `skillpage.py` ships in this skill.
- [ ] 📏 The manual stays a manual
      `SKILL.md` is 771 lines and has shipped 168 releases since 260722, while `QC1a`'s Law says specs belong in `ref/` so the manual stays as short as possible.
      Nothing measures whether that Law is still being followed, and a door nobody can read to the end stops being a door.
- [x] 👪 The family boundary is declared in the file, not left implicit
      0.109.0 states which unit owns what, and names the one duplication kept on purpose: `open` still describes proposing and materializing a board, because a person opening their first board should not have to load a second skill.
      A duplication that is declared can be corrected in both places; one that is undiscovered is what retired `haipipe-board-index`.

## States
This is the door and by far the largest unit: 771 lines of `SKILL.md`, 16 scripts under `cli/`, 12 modules under `src/`, and 0.124.0 after 168 releases since 260722.
Its health is `🟡 in flux` for the plain reason that it changes almost every working day, not because anything is known to be broken.
Two of its three open Aims are defects other pages found and correctly sent here, which is what a door should expect: it owns the scripts, so it inherits their gaps.

- 260802 CC · 👪 The family block changed shape when a unit was retired
  JL merged `haipipe-board-index` into `haipipe-board-routing`, so the roster is one door, two specs and one verb, and `lanes.py` left this family's orbit for routing's.
  The section heading had said "one door, three specs, one verb" while one of those three was a verb set with no contract in it, and both the heading and the block are corrected at 0.109.0.
  The ruling and its evidence live on `QC1b`; this page carries only what the door itself now says.
- 260802 CC · 🪞 Two defects arrived here from pages that could not fix them
  `Skill-1` sent the `check`-hashes-frontmatter-only gap, and `QC1b` sent the four `live/chat.py` rule strings.
  Both are correct routing rather than passing the buck: the page that finds a defect is rarely the page that ships the file, and a finding parked on the finder's page is a finding nobody owns.
- 260726 CC · 🧪 This page was the first thing `skillpage.py` ever generated
  The skill that generated it was the deliberate first subject, because a tool that cannot describe its own skill describes nothing, and the failure would have shown up immediately rather than on skill 40.
  The page went from 4,132 rendered characters to 132,256 once the embeds resolved.

## Log
- 260815 1930 · [JL via CC] round 3, the door's last thinning: the plugin catalog joined the family roster, Shape moved to the folded-page era, the page anatomy handed whole to haipipe-page, and serve's plugin prose became pointers; 761 -> 706 lines, snapshot refreshed.
- 260815 1230 · [REVISE-CC] converted to a for-design page (JL 260815): the three managed spans left the file, `skillpage.py plug` wrote the unit's contract surface to `skill/haipipe-board/`, and Content §2 adopts the selection recorded on the specimen.
- 260806 2115 · [REVISE-CC] swept to the 260806 architecture; managed spans resynced to 0.124.0 and the authored counts corrected from "0.120.1 after 160 releases" to 0.124.0 after 168 releases (state line, Opening, Aims, States)
- 260806 0140 · [REVISE-CC] card synced to disk truth after 260805 (ten types · thin-paper phase 2 · first live RUN); the managed spans resynced to 0.120.1 and the authored counts read 160 releases, 771 lines, 16 cli scripts, 12 src modules, replacing the 0.113.0-era figures.
260804 · Updated the authored family map for Page RUN and the producer, reviewer, and Page orchestrator roles.
260802 1830 · Authored half written, the last of the six skill and agent pages to get one: the placeholder health Aim and the "Nothing ruled yet" stub were replaced with four real Aims and three dated State records. Two of the open Aims are defects other pages found and routed here because this skill ships the file: `Skill-1`'s finding that `skillpage.py check` hashes frontmatter only, and `QC1b`'s four `live/chat.py` rule strings. `state:` gained the release evidence behind its 🟡
260802 1810 · Family block and its heading corrected at 0.109.0 after JL merged `haipipe-board-index` into `haipipe-board-routing`: the roster is one door, two specs and one verb, and the heading no longer says "three specs" when one of the three was a verb set. The `open` action keeps its own propose-and-materialize description on purpose, and the file now says so
260801 · Stale page ids corrected in the LIVE prose and file inventories, mirrored into `board/haipipe-board/SKILL.md`: the excalidraw attach control is `QB7`, not `QD7`, which the 260726 entries predate and which now points at an archived page; and `QD2` is no longer "the restricted drawer" since it carries three permission tiers and defaults to the full one, so the QD2/QD3 split is named as a difference of FORM and `QD4` is named as the terminal's form question. The dated changelog blocks below keep their original ids on purpose: they record what was true when written
260727 0115 · renamed `QB6-board-skill.md` -> `Q-Skill-haipipe-board.md` and moved into the new `Q-Skill/` group; the version now rides the `state:` line as readable detail, never the filename
260726 2325 · page generated from `board/haipipe-board/` by `skillpage.py new`

