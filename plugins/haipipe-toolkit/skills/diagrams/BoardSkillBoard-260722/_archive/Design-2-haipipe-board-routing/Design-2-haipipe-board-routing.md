# Design-2 · Routing (Skill haipipe-board-routing v0.9.1)
state: 🟡 in flux · absorbed haipipe-board-index 260802
owner: JL
page-type: design
method: unit snapshot in skill/ via skillpage.py plug; every section authored by hand (converted from the mirror kind 260815)


> ARCHIVED 260816. This page dissolved into `QB1a`, the standing rule its `📮 reported` end state already cited: the `haipipe-board-routing` unit now rides `QB-board/QB1a-standing/skill/haipipe-board-routing/`. `Design-2` and `Skill-5` resolve here through `board.md`'s `## Links`.

## Opening
`haipipe-board-routing` is the board family's WRITE verb: one thing that happened becomes one dated record on the page that owns it.
Since 260802 it also proposes a board's groups and pages, then creates those files once a person approves.
`haipipe-board` renders, serves and checks the board; reach here when something that happened must be kept on it.

**What one anchored write is**: the input is whatever happened outside the board, such as JL ruling a question in chat, an audit finding, a correction, or a status that changed.
Routing finds the owning page in `board.md`'s `## Pages`, then appends under a named `##` heading rather than at a byte offset, because a blind offset cut `QB4d`'s Opening sentence in half on 260730.
The line it writes is dated and carries who said it, so a later reader can tell when the fact landed and on whose word.

**Why the two altitudes need different approvals**: a page write records something that already happened, so it lands on its own.
A board write decides which pages will exist, and the group letters it picks are cited by every page opened afterwards, so it stops and waits for the person.
Content part 1 states that separation, and `## Aims` carries it as the one open risk the merge introduced.

**Covered elsewhere**: `haipipe-board` owns the machinery, `build.py`, `serve.py` and `check.py`, while this verb writes markdown only.
`haipipe-page` says which section a write owes and `haipipe-sentence` says how the line must read; routing loads both, and the sentence spec writes nothing itself.
The page engine is no longer write-free: at 0.21.0 its CREATE, WORK ON and RUN verbs produce and repair a page's own prose, so routing's claim is narrower now, the one verb that lands an outside input on a page that already exists.
`haipipe-board`'s `open` action still describes propose and materialize too, which Content 2.2 declares on purpose, so those two descriptions have to be corrected together.
`haipipe-board-index` held the board altitude until 260802; its folder is deleted and its page sits in `_archive/`.

**Where it stands**: the merge landed 260802 and one unit now holds two approval rules that only the contract keeps apart.
10 releases shipped between 260731 and 260802, ending with that merge, which is what `🟡 in flux` on the `state:` line is reporting.
No group-altitude finding has been written through the new landing rule, no fresh agent has been measured choosing this door, and `haipipe-board-digest` is named on the roster and not on disk.
Each of those is an open row in `## Aims`.

## Diagram
**What sits in this page's `skill/` plugin**: the unit's contract surface, written by `skillpage.py plug` and renamed so neither the installer glob nor page discovery can mistake it for the live unit.

```
skill/haipipe-board-routing/
  CHANGELOG.md
  SKILL.snapshot.md
```

**Both altitudes, and the approval that differs between them**: a board write stops for a person; a page write lands on its own.

```text
WORKFLOW  two altitudes since 260802, two approval rules, one unit

  🗂 BOARD + GROUP ALTITUDE   (arrived with haipipe-board-index)
     a topic, no board yet
        │
        ▼
     propose      spine · close · groups · pages · connections · skills
        │         talk only, write NOTHING
        ▼
     ⛔ STOP and get the person's approval ── this is the rule that
        differs from the page altitude, and the merge must not blur it
        │
        ▼
     materialize  board.md + one folder per group + one file per page
     lanes        src/lanes.py <board> [--apply], round-trips
     regroup      wraps haipipe-board/cli/regroup.py
        │
        ▼  hands off to haipipe-board, which builds the board/ site

  ✍️ PAGE ALTITUDE  ── lands on its own: it records what already happened

  ONE input, no board open
  a ruling · a finding · a correction · a status change
        │
        ▼
  1 READ      what happened, and what record it deserves
              a derived view, aggregated from state the pages already
              hold, deserves NO write, because a copy drifts
        ▼
  2 RESOLVE   the attached board, or the nearest board.md above the path
              two plausible boards = ASK, never guess
        ▼
  3 FIND      board.md ## Pages, the ONLY registry
              an id does not predict a folder, so never resolve by name
              ## Links resolves the older ids
        ▼
  4 PICK      loads 📄 haipipe-page  · which section owes this
              loads ✒️ haipipe-sentence · how the line must read
        ▼
  5 WRITE     append under the named ## heading, at the SECTION BOUNDARY
              never at a byte offset: a blind offset spliced QB4d's
              Opening sentence in half on 260730

  ── three end states ────────────────────────────────────────────
  ✅ landed     a Log line · a States row · a factual Aim State
  🟡 proposed   a Decision Now row · a page it would open, not opened
  📮 reported   another owner's board: an editorial write becomes a
                report to them, never an edit (QB1 §4)

  ── never ───────────────────────────────────────────────────────
  🚫 tick a checkbox · flip state: · pass a page-level human gate
     it reads a claim and cannot verify it, so it may not close one

  ── where a GROUP-altitude input lands (settled by the merge) ────
  a finding about ONE page   →  that page's owning section
  a finding about A GROUP    →  the group's intro in board.md ## Pages
  a finding about THE BOARD  →  ## Topic, ## Pipeline, or ## Board Map
     this rule was only available once ONE unit owned both altitudes

  🔁 digest = this verb FANNED OUT over one session, one call per
     input. Named on the roster, not on disk.
  ⚙️ one live caller in code today: haipipe-board/cli/meetingpage.py
```

## Content
### 1 · What this unit is, in one screen
**Live and snapshot**: the unit ships from its own folder, and this page judges a plugged copy.
```text
  ⚙️ the live unit, ships        📋 skill/haipipe-board-routing/
     from its own folder    ──▶     the snapshot this page's
                            plug    judgments are about
```
`haipipe-board-routing` is the WRITE VERB at both altitudes: propose and materialize a board's structure, and land one anchored write in the owning page and section.
The live unit ships from `board/haipipe-board-routing/` with `src/lanes.py`.

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
- [x] 📐 Whether this verb absorbs the board altitude is ruled
      JL ruled it on 260802 in his own words, "maybe merge, I will do B", and 0.9.0 shipped the merge the same day.
      `haipipe-board-index` is deleted, `src/lanes.py` moved here, and this unit now owns `propose`, `materialize`, `lanes` and `regroup` alongside the five-step route.
- [x] 🧭 A group-altitude input has somewhere to land
      Settled by the merge rather than by its own ruling: a finding about a whole group lands in that group's intro prose in `board.md` `## Pages`, at the section boundary, with `lanes.py` refreshing the block underneath.
      Decomposing such a finding onto its member pages was the alternative and is refused, because the pieces individually say less than the whole did.
      No real group-altitude finding has been landed through the rule yet, which is what the next one will test.
- [ ] ⛔ The two approval rules stay apart inside one unit
      A page write lands on its own and a board write stops for a person, and nothing enforces that separation except the contract saying so.
      This is the specific risk the merge introduced: one unit, two rules, and the weaker one is the easy default under time pressure.
- [ ] 🧪 The door test is run on this unit
      `QC1b` §1.4 measured the test on `haipipe-page` and on nothing else: three fresh agents opened that door unaided at tool calls #5, #6 and #5.
      This unit has one caller in code, `haipipe-board/cli/meetingpage.py`, and no evidence yet that an agent handed a bare instruction chooses to open it.
- [ ] 🔁 `haipipe-board-digest` ships or leaves the roster
      Digest is this verb fanned out over a session, one call per input, and it is named on the roster and not on disk.
      Until it exists, this page also carries routing's own design questions by default rather than by decision, which is a fourth row on `QC1b`.
- [x] ⚖️ The write protocol is shipped rather than only argued
      0.8.0 carries the human-decision law, the cross-board law and the anchored-append rule under its own headings, so digest will inherit a written protocol instead of needing a new one.

## States
This was the family's fastest-moving unit through the merge, 11 releases to 0.9.1, though the page engine has since outpaced it to 0.21.0.
As of 260802 it is the family's write verb for outside inputs at both altitudes; the engine's CREATE, WORK ON and RUN verbs write a page's own prose, not routed records.
Its health is `🟡 in flux` because the merge landed the same day it was ruled and nothing has exercised the new altitude yet.
Both failure modes its page-altitude rules exist to prevent had already happened by hand before it shipped, which is why those fixes were written into the contract rather than learned from it; the board altitude has no equivalent scar tissue yet.

- 260802 JL · 📐 The merge, ruled and shipped the same day
  JL asked what `haipipe-board-index` was for, said it might not be needed, and ruled: "maybe merge, I will do B".
  The recommendation on the row had been to retire the index into the door instead, and JL took the option that also closed the group-altitude row, which retiring would have left open.
  0.9.0 absorbed the altitude, `src/lanes.py` moved in, and the index folder is deleted; the retired `Skill-1` page is in `_archive/` and its id still resolves through `## Links`.
- 260802 CC · 🗂 What the audit found, and the filing mistake that hid it
  Three of the index's five verbs were other units' work written a second time: `propose` and `materialize` are the door's `open`, `regroup` wrapped `cli/regroup.py`, and `check` was a subset of `cli/check.py`.
  It went two days unseen because `QC1b` had filed the index as a CONTRACT beside page and sentence, while its `SKILL.md` was five verbs and no contract, and a unit shelved on the wrong side of that split is never compared against the right list.
- 260802 CC · ⚙️ One caller in code, and it is not a board session
  `haipipe-board/cli/meetingpage.py` names this skill, which makes it the only sub-skill in the family with a consumer written in Python rather than in prose.
  That is real evidence for the door test's premise and it is not the door test, because the script names the skill instead of an agent choosing it.

## Log
- 260815 1230 · [REVISE-CC] converted to a for-design page (JL 260815): the three managed spans left the file, `skillpage.py plug` wrote the unit's contract surface to `skill/haipipe-board-routing/`, and Content §2 adopts the selection recorded on the specimen.
- 260806 2116 · [REVISE-CC] swept to the 260806 architecture; routing is the family's WRITE verb, no longer its ONLY writer: the page engine 0.21.0 also writes through CREATE / WORK ON / RUN, and Opening plus States now say so.
- 260806 0140 · [REVISE-CC] card synced to disk truth after 260805 (ten types · thin-paper phase 2 · first live RUN); the merge's "one day old" clause now dates it 260802 and the release count reads 11 to 0.9.1, with no 260805 change touching this unit.
260802 1810 · Absorbed `haipipe-board-index` at 0.9.0 on JL's `B` ruling: the board and group altitude, `propose` `materialize` `lanes` `regroup`, and `src/lanes.py`. The Opening, the `WORKFLOW` fence and the Aims were rewritten for two altitudes, and the group-altitude landing rule the merge settled is now on the page. The two Aims that were waiting on `QC1b`'s rows are closed, and one new Aim opened for the risk the merge introduced: one unit now carries two approval rules and only the contract keeps them apart
260802 1720 · Authored half written: the `WORKFLOW` fence replaced the template placeholder with the five-step route, the three end states and the never-list, five real Aims replaced the single health placeholder, and `state:` moved from 🔴 to 🟡 in flux on the release evidence. JL's merge proposal recorded as a State record pointing at `QC1b`'s row rather than restating its options
260731 1117 · page generated from `board/haipipe-board-routing/` by `skillpage.py new`

