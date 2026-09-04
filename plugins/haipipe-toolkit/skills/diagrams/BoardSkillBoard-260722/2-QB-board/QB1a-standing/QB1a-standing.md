# Standing: what we may write into a board we render but do not own
state: 🟡 PARTIAL · the rule is written, unapproved · open: JL's tick, the 260729 revert
owner: JL
method: sort every write this family makes into mechanical, editorial, and the one hard case, then say who the write verb obeys
session: 8ab6d00e-cf65-453c-b5c5-c5b37d7905d0

## Opening
This family runs on boards it did not make, so what is it allowed to change in one of them?
Standing is the word for that permission: whether we may make a given write into a board we render but do not own.
Generating the site is clearly fine. Ticking somebody's box is clearly not.
The hard case sits between them and never shows in the diff: repairing a dead link looks the same whether our tool broke it or we just found it.
This page draws that line.

**Where this page sits**: `QB1` owns the two folders and what a write to each one means, and this page takes the third case, a write that lands in neither: somebody else's board.
`QB2` owns the Index a reader opens.
The unit in this page's `skill/` plugin is `haipipe-board-routing`, the verb that performs every write standing permits.

**How big the outside is**: six boards sit in this tree on 260816, holding 228 pages, and 165 of those pages belong to somebody else.
`build.py` writes a site into a project's folder, `serve.py` writes a keystroke back into a paper's markdown, and `regroup.py` has moved 154 pages across boards owned by four different projects.
Crossing into another owner's tree is the normal case, not the exception.

**Why the rule is not settled yet**: on 260729 three dead references on two boards this family does not own were repaired here instead of being reported to their owners.
Nothing this family runs had broken them, so the repair was the wrong branch of the very rule written below.
The revert is still owed, and JL has not yet ticked the rule itself.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**Every count is measured, and it says when**: the number of boards and the number of pages that are not ours change every week, so a figure written from memory rots with nothing reporting it.
Count it with the parser or with `find`, write the number, and date it: `228 pages across six boards, 165 not ours, counted on 260816`.

**Name the act, not the file**: standing is about what a write DECIDES, so a rule here says "a tick" or "a `state:` flip" rather than "line 14 of their page".
A rule keyed to a file rots the day the file moves; a rule keyed to the act does not.

**The diff is never the evidence**: whenever this page compares two cases, say plainly whether they look the same in a diff.
That similarity is the whole reason the page exists, so hiding it makes the rule look obvious when it is not.

**Language and sentences**: English only, in the source and in the render.
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes: use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

## Diagram

**The three kinds of write**: which ones are always ours, which are never ours, and the one that has to be decided.

```text
── [1/2] A write is about to land in somebody else's tree ────────────────

  🏭 6 boards in this tree · 228 pages · 165 not ours   (260816)

  ✅ MECHANICAL · always allowed, because it carries no judgement
     🌐 generate the board/ site      ⌨️  write back a keystroke
     🔁 sync a managed span           📦 git mv a page we are moving

  ⛔ EDITORIAL · never ours, however small it looks
     📝 what a page says   ☑️  a tick   🚦 a state:   💬 which topic exists

  ⚖️ CHECKER ERROR · the one that has to be decided
     🔧 our tool BROKE it   ─▶  repair it, same round, and say so
     🔍 we merely FOUND it  ─▶  report it to the owner, then stop
     🚩 the two are IDENTICAL in the diff · the diff is not the test
```

**Who obeys the rule**: the write verb, and the two altitudes it writes at.

```text
── [2/2] haipipe-board-routing · the verb standing bounds ────────────────

  ✍️ PAGE ALTITUDE · records what already happened
     1 READ     what happened, and what record it deserves
     2 RESOLVE  the attached board · two plausible boards = ASK
     3 FIND     board.md ## Pages · the ONLY registry
     4 PICK     📄 haipipe-page · which section owes this
                ✒️ haipipe-sentence · how the line must read
     5 WRITE    append under the named ## heading
     ✅ lands on its own · no approval, because nothing is decided

  🗂 BOARD ALTITUDE · decides which pages will exist
     propose    spine · close · groups · pages · connections
     ⛔ STOP    and get the person's approval
     build      board.md + one folder per group + one file per page
     ✋ waits for a person, because the letters it picks are cited
        by every page opened afterwards

  ── three end states ─────────────────────────────────────────────
  ✅ landed    a Log line · a States row · a factual Aim State
  🟡 proposed  a Decision Now row · a page it would open, not opened
  📮 reported  another owner's board · an editorial write becomes a
               report to them, never an edit
```

## Content
### 1 · Ten boards exist and most of them are not ours
**How much of the work is other people's**: what this family produces, and how little of it belongs to it.

```text
🏭 WHAT THIS FAMILY RENDERS, AND WHO OWNS IT

  🗂 boards in this tree     6
  📄 pages on them          228
  🚫 pages that are ours     63
  ⚠️ pages that are not     165        counted 260816

  ✍️ writes it makes into another tree, on nearly every run
     🌐 build.py     writes the board/ site into a project's folder
     ⌨️ serve.py     writes a comment into a paper's markdown
     📦 regroup.py   moved 154 pages across 4 projects' boards
```
📌 Establishes that crossing into somebody else's tree is the normal case, so what may happen there is a decision rather than an afterthought.

#### 1.1 · Standing is a permission, and it belongs to the act rather than to the file
(the word covers every write this family makes into a board whose topic belongs to somebody else)
A board this family renders is not a board this family may edit, and those two capacities arrived together because one tool does both.
What separates them is not which file is open but what the write decides, which is why the rest of this page sorts writes by their act.

#### 1.2 · The count is measured on the tree that is present, not remembered
(228 pages across six boards, 165 not ours, counted on 260816)
Earlier drafts carried "ten boards and 321 pages", which counted two boards that live on other trees and are not visible from here.
A figure that cannot be recounted where it is written is a figure nobody will maintain, so this page counts what it can see and dates it.

### 2 · Mechanical writes are always allowed
**What makes a write safe**: the property the four allowed writes share.

```text
✅ MECHANICAL · no judgement inside it

  🌐 generate the board/ site      regenerable from the markdown
  ⌨️ write back a keystroke        a copy of what a human just did
  🔁 sync a managed span           regenerable from its source
  📦 git mv a page we are moving   the tool's own move, not a choice

  🔑 the shared property: none of them decides anything about
     that board's TOPIC
```
📌 Establishes the four writes this family may always make into another owner's board, and the single property that makes them safe.

Each of these is either regenerable from the markdown, or a transcription of something a person just did.
None of them decides anything about that board's topic, and that is the property doing the work, not the fact that they are small.
A write that is small and decides something is editorial, and a write that is large and decides nothing is mechanical.

### 3 · Editorial writes are never ours, however small they look
**What an editorial write is**: four acts that all decide something about another owner's topic.

```text
⛔ EDITORIAL · never ours

  📝 what a page says        the prose is the owner's argument
  ☑️ a tick                  a tick means somebody verified it
  🚦 a state:                a flip is the act of closing a question
  💬 which topic exists      opening a page picks their subject

  🔑 the shared property: each one decides something about
     that board's TOPIC · size has nothing to do with it
```
📌 Establishes that the small editorial writes are refused for the same reason as the large ones.

#### 3.1 · A tick asserts that somebody verified the thing
(`SKILL.md` already says so, and this family cannot verify another unit's work)
Ticking a box on somebody else's board claims a verification that never happened here.
That is true whether the box was obviously ready to tick or not.

#### 3.2 · A `state:` flip is the act of closing a question
(the same act as deciding the question is answered, which belongs to the board's owner)
It looks like a one-character edit and it is a ruling.
Which topics exist at all is the same kind of act one level up, so opening a page on their board is refused for the same reason.

### 4 · The hard case is a checker error, and the test is who broke it
**The one question that decides it**: not what the row says, and not how the fix looks.

```text
⚖️ check.py REPORTS AN ERROR ON A BOARD WE RENDER

  ❓ who broke it?
     │
     ├── 🔧 OUR tool did   ─▶ ✅ repair it, in the SAME round, and say so
     │                        📦 regroup.py broke 17 links on 260726
     │                           and repaired all 17 that day
     │
     └── 🔍 we merely FOUND it ─▶ 📮 report it to the owner, then stop
                                  🚩 260729: 3 rows repaired instead
                                     = the wrong branch · revert owed

  🧨 the two branches produce an IDENTICAL diff
     the diff is not the test · the CAUSE is the test
```
📌 Establishes the only test that separates a repair this family owes from a repair that is not its to make.

#### 4.1 · Broke it ourselves: repair it in the same round and say so
(`regroup.py` broke 17 cross-board `## Links` on 260726 and repaired all 17 the same round)
That is settled precedent, and it is the reason the sweep shipped as a command rather than as a habit.
A tool that damages another owner's board and walks away has made them pay for a change they did not ask for.

#### 4.2 · Merely found it: report it to the owner and stop
(repointing a row means choosing what the row should name, and that choice is about their topic)
The repair looks mechanical and it is not: somebody has to decide which page the dead row was trying to reach.
That decision is editorial under §3, so it goes back to the person who owns the topic.

#### 4.3 · 260729 took the wrong branch, and this rule exists because of it
(three dead references repaired on two boards this family does not own)
One board's rows had rotted when a display unit was split into two variants, and the other pointed into a task folder that had gained a subfolder.
Neither was broken by anything this family runs, so both were the FOUND case and both should have been reports.
The revert is owed and is carried as a decision below.

### 5 · The write verb, and what standing bounds
**Where the rule becomes code**: the unit that performs every permitted write, and the two altitudes it works at.

```text
✍️ haipipe-board-routing · ONE input becomes ONE dated record

  📥 input      a ruling in chat · a finding · a correction · a status
  🎯 target     the page that OWNS it, found through board.md ## Pages
  📝 landing    append under the named ## heading
                🚫 never at a byte offset: a blind offset cut QB4d's
                   Opening sentence in half on 260730

  🗂 board altitude   ⛔ stops for a person before it writes
  ✍️ page altitude    ✅ lands on its own

  🚫 another owner's board: an editorial write becomes a REPORT
```
📌 Establishes that the standing rule has a unit that must obey it, and names the one place the two altitudes differ.

#### 5.1 · A page write records what already happened, so it lands on its own
(the input is something that happened outside the board, and the record is dated and says whose word it is)
Nothing is being decided by writing it down, so no approval gate is needed.
The line names when the fact landed and on whose word, which is what lets a later reader weigh it.

#### 5.2 · A board write decides which pages will exist, so it waits for a person
(the group letters it picks are cited by every page opened afterwards)
Proposing a spine, a closing condition, groups and pages is talk, and it writes nothing.
Materializing them creates files and ids that every later page depends on, so it stops and asks.

#### 5.3 · Standing is what turns an editorial write into a report
(the third end state: `📮 reported`, which exists only because of this page)
When the owning board is somebody else's, the verb does not land the write.
It produces a report instead, and the owner decides.

## Aims
### Decision Now
- [ ] 🗣 Approve the standing rule for writing into a board we render but do not own
      📍 `Part` §2, §3 and §4, which are the whole rule
      🔔 `Why now` the rule has been written and in use as a convention since 260729 and has never been ticked, so nothing stops the next agent taking 260729's branch again
      ⭐ `A ·` approve as written, which lets §2 to §4 graduate into `SKILL.md` and start binding every agent on every board
      `B ·` approve the mechanical and editorial halves only, and leave the checker-error test as convention, which keeps the one contested case open
      `C ·` reject, which returns every write into another owner's board to case-by-case judgement
      🛑 `Blocks` graduation into `SKILL.md`, and the mechanical half in `check.py`
      🤖 `If nobody answers` A takes effect, because it is the rule already being followed

- [ ] 🗣 Revert the three out-of-band edits of 260729 and report them instead
      📍 `Part` §4.3, the case this rule was written from
      🔔 `Why now` the repairs are still standing on two boards this family does not own, so the page argues one rule and the tree shows another
      ⭐ `A ·` revert all three and send each owner a report, which makes the tree agree with the rule
      `B ·` leave them and record them as a grandfathered exception, which keeps a counter-example alive on disk
      🛑 `Blocks` nothing mechanical, but it blocks this page reaching ✅
      🤖 `If nobody answers` A takes effect


### A1 · 🏭 Ten boards exist and most of them are not ours
- ✅ A1.1 · The size of the outside is measured rather than remembered.
  **Done when:** The board count, page count and not-ours count on this page each carry the date they were counted, and a reader can reproduce them from this tree.
  **Now:** Met. Six boards, 228 pages, 165 not ours, counted on 260816 from this tree; the older 321-page figure counted two boards that are not visible here and has been dropped.


### A2 · ✅ Mechanical writes are always allowed
- ✅ A2.1 · The allowed writes are named by the property that makes them safe.
  **Done when:** Each listed write is either regenerable from the markdown or a transcription of a human act, and the page says which.
  **Now:** Met. Four writes listed, each named as regenerable or as a transcription of a human act.


### A3 · ⛔ Editorial writes are never ours, however small they look
- ✅ A3.1 · The small editorial writes are refused for the same stated reason as the large ones.
  **Done when:** A reader can tell from the page why a tick is refused without appealing to how small it is.
  **Now:** Met. The refusal rests on what the write decides, and §3.1 and §3.2 work the two smallest cases.


### A4 · ⚖️ The hard case is a checker error, and the test is who broke it
- ✅ A4.1 · The who-broke-it test is stated, with the precedent on both branches.
  **Done when:** Both branches carry a real dated case, and the page says plainly that the diff does not distinguish them.
  **Now:** Met. Both branches carry a dated case, 260726 and 260729, and the page states that the diff does not distinguish them.
- 🧠 A4.2 · The 260729 repairs are reverted and reported to their owners instead.
  **Done when:** The three rows are back as their owners left them and each owner has been told what was found.
  **Now:** Waiting on JL. The three repairs of 260729 are still standing on their owners' boards and the reports have not been sent.


### A5 · ✍️ The write verb, and what standing bounds
- 🧠 A5.1 · The unit that performs the writes obeys this rule in its own contract.
  **Done when:** `haipipe-board-routing`'s `SKILL.md` states the report end state and points at this page rather than restating the rule.
  **Now:** Waiting. The unit's `SKILL.md` describes the three end states, and its `📮 reported` state cites this page's old address rather than this page.
- ⬜ A5.2 · The rule has a mechanical half, so the next agent cannot repeat 260729 by accident.
  **Done when:** Something in `cli/check.py` or the routing verb refuses an editorial write into a board whose owner is not this one.
  **Now:** Not started. `cli/check.py` carries nothing from this page, so the standing rule has no mechanical half and the 260729 mistake is still available to the next agent.


### P · Page-level
- 🧠 P1 · JL approves the standing rule, so it can graduate into the skill.
  **Done when:** The rule is ticked here and copied into `SKILL.md`, from which point it binds.
  **Now:** Waiting on JL's tick in Decision Now, after which the rule graduates into `SKILL.md`.


## Files
### ⚙️ Engines · what RUNS this subject
- `../../../../board/haipipe-board-routing/src/lanes.py`
  The write verb: it resolves the owning board, finds the page in `## Pages`, and appends under the named heading.
- `../../../../board/haipipe-board/cli/regroup.py`
  The 260726 sweep, and the precedent for repairing what our own tool broke.
- `../../../../board/haipipe-board/cli/serve.py`
  The write-back door for a keystroke a human contributes, which is the clearest mechanical write.
### 📋 Contracts · what CARRIES a rule to other pages
- `../../../../board/haipipe-board-routing/SKILL.md`
  Where this page's Law graduates, and where the `📮 reported` end state is declared.
### 🧪 Checks · what CATCHES a page breaking a rule
- `../../../../board/haipipe-board/cli/check.py`
  What turns a defect on a board we render into a report: `pages-ghost` and `dead-link`. It carries nothing from this page yet, which is Aim A5.2.
### 📤 Output files · what a BUILD writes
- `../../../board/QB/QB1a-standing.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit it; the markdown is the only source.

## Law
- ⚖️ **Standing**: what this family writes into a board it does not own is bounded by standing
  Mechanical writes are always allowed, because they carry no judgement: generating the site, writing back a keystroke a human just made, syncing a managed span, moving a page the tool is moving.
  Editorial writes are never ours: what a page says, a tick, a `state:`, which topic exists at all.
  The property that separates them is whether the write decides anything about that board's topic, and not how small the write is.
- 🔧 **Who broke it**: a checker error is decided by its cause, never by its diff
  Repair what our own tool broke, in the same round, and say so.
  Report what we merely found, and let its owner decide, because repointing a row means choosing what the row should name.
  The two cases produce an identical diff, which is exactly why the diff cannot be the test.
- ✍️ **Two altitudes, two approvals**: a page write lands on its own, a board write waits for a person
  A page write records something that already happened, so nothing is being decided by writing it down.
  A board write creates the group letters and page ids every later page cites, so it proposes, stops, and asks.
- 📮 **The third end state**: on another owner's board, an editorial write becomes a report
  The verb does not land the write and does not silently drop it either.
  It reports what it found, and the owner decides.

## Glossary
- ⚖️ **standing**: whether this family is entitled to make a given write into a board it renders but does not own. Mechanical writes have it, editorial writes do not.
- 🔧 **mechanical write**: a write that is regenerable from the markdown, or a transcription of something a person just did. It decides nothing about the board's topic.
- 📝 **editorial write**: a write that decides something about the board's topic, however small it looks on screen.
- 📮 **reported**: the end state where the verb produces a report to another board's owner instead of writing to their board.

## Discussion
> JL: I think we use the decision for it.
>> CC0729: taken, and the word "ruling" is retired on this page in favour of "decision".

## Log
- 260816 · [DRAFT-CC] Page opened. Split out of `QB1` §4 on JL's call to keep the group at four pages: `QB1` reads as settled while the standing rule inside it was never approved, so a reader scanning the roster could not see the group's one open decision. Carries §4 whole, its two open items as a `### Decision Now` with options, and the write verb `haipipe-board-routing`, whose page `Design-2` dissolved into this one the same round the way `QPs00` dissolved into `QPs1`. The board and page counts were remeasured from this tree, six boards and 228 pages with 165 not ours on 260816, replacing the "ten boards, 321 pages, 266 not ours" figure that counted two boards no longer visible here. `Design-2`'s prose is archived at `_archive/Design-2-haipipe-board-routing/`.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0