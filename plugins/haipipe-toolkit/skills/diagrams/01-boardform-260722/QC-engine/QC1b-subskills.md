# Sub-skills: what else this family ships
state: 🟡 PARTIAL · roster ruled 260731, index merged out and the skill-page variant added 260802
owner: JL
method: name every candidate and apply one test to each, then let JL rule the set; a shipped skill follows settled decisions, never precedes them

## Opening
Which Board capabilities need their own loadable unit, and which stay inside the main manual?
A loadable unit is a skill an agent opens on its own, such as `haipipe-board-page`, which says what a page is to a reader with no board open.
Cutting one is worth it only when some consumer needs those rules without the whole board workflow.
Get it wrong and the same rule gets written twice, or a capability another workflow needs stays locked in the manual.

**The test, in one line**: does some consumer need these rules with no board open? A yes makes it a door; a no makes it a `ref/` file the manual already points at.

**Why the answer moved**: CC read the roster on 260729 as defer page and sentence, because nothing then needed either one without a board. JL named `haipipe-board-routing` and `haipipe-board-digest` the same day, and both verbs are handed raw input with no board attached, so the missing consumer had simply not been proposed yet.

**Covered elsewhere**: What a page IS, and its section contract: `QB4`. What a sentence IS, and its records: `QB8`. What SKILL.md must say, and the rule that specs go to `ref/`: `QC1a`. Where a write may land on somebody else's board: `QB1` §4. One synced mirror page per shipped unit: `Skill-0`, `Skill-3`, `Skill-4`, `Skill-5`, `Agent-1`, `Agent-2`; the retired `Skill-1` is in `_archive/` and its id still resolves.

## Diagram

**The family, one door and three units**: which unit runs at which moment, and what each one loads.

```
                        🚪 haipipe-board · the door you invoke
                                     │
        ┌────────────────────────────┴────────────────────────────┐
        │                                                         │
   ✍️ anything that WRITES                              🖌 a page edit
        │                                                         │
        ▼                                                         ▼
  🧭 haipipe-board-routing · both altitudes             📄 haipipe-board-page
     🗂 opening a board  Spine · Groups · Pages            sections · kinds
        canvas · lanes · writes NOTHING                 what a machine writes
        before approval                                          ▲
     ✍️ an ordinary turn Board → Group → Page → Section           │
        │                                                        │
        │  loads the spec it needs ─────────────────────────────┘
        │
        └──▶ ✒️ haipipe-board-sentence
               Evidence Card · Comment · Edit

  🔁 haipipe-board-digest  =  many recent turns, routing called once each
     🚧 named on the roster, not on disk
  🗑 haipipe-board-index   =  merged into routing 260802, folder deleted
```

## Content
### 1 · The test a candidate has to pass

**The two shapes a rule can take**: what makes a capability a door rather than a file.

```
🚪 A DOOR                            📎 A ref/ FILE
   an agent CHOOSES to open it          a skill already inside points at it
   ✅ consumer has no board open        ✅ consumer is already in the workflow
   💰 costs a version surface           💰 costs nothing
   🧪 haipipe-board-page                🧪 ref/page-template.md
```
📌 One test decides every candidate, and this part records the test, the survey that applied it to every seam, and the reading it overturned.

A skill is a door an agent chooses to walk through, and a `ref/` file is something a skill already inside the door points at.
So the test is not "is this a coherent topic", it is "does some consumer need these rules with no board open".

**1.1 · Every seam in `skills/board/`, walked once on 260729**

- `haipipe-board-page`, the page contract: the strongest case.
  `QD2`'s drawer keeps a hand-rolled copy of exactly these instructions in a Python string, and `QB8d` caught that copy describing a page shape that no longer existed, which is the rot duplication guarantees.
- `haipipe-board-sentence`, the apparatus grammar: second, on the same consumer plus the paper family's evidence card.
- `haipipe-board-stage`, the S-page machinery: already consumed across families, because `create-page.py` in the paper skill calls the Board's `stage.py`.
  That consumer needs the SCRIPT, not the instructions, so it argues for keeping `stage.py` clean rather than for a skill.
- the live layer (serve, chat, terminal) and the canvas (`xcal.py`): runtime, not instructions.
  Their sharing half is already a sibling SERVICE (`boards_api.py`, `QE3`), and a skill would be the wrong shape.
- `status.py`, `regroup.py`, the checker: verbs of the main skill, so splitting them buys nothing.

#### 1.2 · The reading this test overturned

CC's 260729 verdict was defer page and sentence, on the grounds that the drawer's agent is already inside a board when it reads those rules.
That reasoning was sound and its premise was wrong: JL named routing and digest the same day, and neither verb has a board open when it starts.
The defer recommendation is therefore withdrawn, and the failure mode is recorded in `## Law`: a candidate can fail the test only because its consumer has not been proposed yet.

#### 1.3 · The most recent application, and it landed outside this family

`haipipe-writing` ships with three verbs, where `score` ranks what is worth rewriting, `rewrite` changes prose and anchors a `✎` record per sentence, and `check` audits those records.
It stays its own unit rather than a verb inside the board family, because its consumer is ANY authored prose in the repo: a board page, a SKILL.md, a README, an application section.
Folding it in would have tied a general writing verb to one host, so the test sent it out of the family rather than into it.

#### 1.4 · The door test, measured rather than argued
The test above says a door is a capability an agent CHOOSES to open, and until 260802 nobody had checked whether `haipipe-board-page` is actually chosen.
The 260731 fan-out could not answer it: its brief pasted the path to the skill's `SKILL.md` and named `QB4` as the worked example, so all five agents read the contract as a plain file and not one of them ever invoked it.
The real test gave three fresh agents one sentence each and nothing else, with no path, no skill name and no example page.
All three opened this door unaided, at tool calls #5, #6 and #5, including the one phrased "can you clean up QF5-sentence-run for me", whose words match no trigger in the skill's description.
All three then drove their page from 15, 13 and 10 findings to zero, and the board fell from 210 findings to 171.
The door test passes on evidence, and what failed instead was scope: the same three agents wrote to 15 files, 1 file and 2 files from the same instruction, because the skill said where to start and never where to stop.
`haipipe-board-page` 0.10.0 adds that bound as steps 7 and 8 of the verb.

### 2 · The roster, and what each unit owns

**One door, three specs, two verbs**: the shape JL ruled, and what each unit is loaded for.

```
🚪 haipipe-board          the operating manual you invoke to run a board
📄 haipipe-board-page     SPEC · what one page is · and a door for 2 verbs
🪞 haipipe-board-page-for-skill
                          SPEC · the VARIANT for the two skill and agent page kinds
✒️ haipipe-board-sentence SPEC · what one sentence carries · and a door
                                 for 3 verbs since 260802 (comment · edit · card)
🧭 haipipe-board-routing  VERB · every write onto a board, at BOTH altitudes
                                 board.md's structure, and one input → one
                                 owning page → one anchored write
🔁 haipipe-board-digest   VERB · one session → many inputs → routing, fanned out
```
📌 The roster took its shape across four days: JL named the units on 260729, added the index altitude on 260730, ordered four of them built on 260731, and folded the index back into routing on 260802.

`haipipe-board` stays the public orchestrator, and it does not load every detailed contract on every turn: it invokes the smallest unit that owns the current transition.
That is the progressive-disclosure shape, so opening a Board loads Index, an ordinary turn loads Routing, a Page edit loads Page, and sentence apparatus loads Sentence.

**2.1 · What each unit owns**

- `haipipe-board-page`, the Page layer.
  It owns the common Page frame, the page kinds, the section contracts, Aims, States, paths and closure semantics.
  The name is singular because it defines the contract for any ONE page, where `pages` would sound like a batch operation.
- `haipipe-board-sentence`, the atomic layer.
  It owns sentence identity and the records attached to a sentence: Evidence Card, local Comment, Edit, Chat focus and lifecycle.
- `haipipe-board-routing`, the write verb, at both altitudes since 260802.
  At the BOARD and GROUP altitude its first action is interactive: propose Spine, Close, Groups, Pages and their relationships, show one reviewable structure, and write nothing until the user confirms; after confirmation it materializes `board.md` and keeps each group's lane block current with `src/lanes.py`.
  At the PAGE altitude, for each incoming turn it resolves Board → Group → Page → Section, shows the proposed attachment when confidence is not decisive, and never silently creates a Page.
  Once attached it loads the Page or Sentence contract it needs for one anchored write.
  The two altitudes keep separate approval rules, which is the one thing the merge must not blur: a page write lands on its own because it records what already happened, and a board write asks first because it decides what pages will exist.
- `haipipe-board-digest`, the batch verb, named and not built.
  It reconciles a recent session by calling routing repeatedly, and it never invents a second routing policy.

#### 2.2 · Why the two verbs are the consumer the two specs were missing

Routing and digest are the same verb at two scales, so digest calls routing rather than reimplementing it.
Routing has to answer "which page, and which section of it", which is the page contract, and it then has to write a line that reads like the board, which is the sentence contract.
Neither verb has a board open when it starts and both are handed raw input, which is the test in `### 1`, passed.
The split also gives every page and sentence rule a graduation target that is not "another section of the manual".

#### 2.3 · Contracts and actions are deliberately different things, and the split keeps failing

Page and Sentence began as contracts that other skills consume, while Routing and Digest are actions that consume those contracts.
The split has now been wrong twice, in opposite directions, which is worth more than either instance.
Index was filed as a CONTRACT on 260730 and was five verbs with no contract in it, and on 260802 both Page and Sentence grew verbs of their own and became doors as well, so the column they sit in is half true.
A unit is better described by what a reader DOES with it than by which column it was filed in, and every skill page now names both when both apply.
That is why the two halves are named differently and versioned separately: a contract changes when the form changes, and an action changes when the workflow changes.
That misfiling is why the duplication in `2.4` went two days without being seen, because a unit shelved as a contract is not compared against an action's verb list.
The second failure runs the other way and cost nothing yet: `haipipe-board-sentence` reached 0.3.0 on 260802 with three verbs of its own, and this roster still called it a pure SPEC until its mirror page was rewritten the same evening.

#### 2.4 · The merge that removed a unit, and what it bought

JL asked on 260802 what the index was for, said it might not be needed, and proposed merging it with routing; his ruling was "maybe merge, I will do B".
The audit that question forced found three of its five verbs were other units' work written a second time: `propose` and `materialize` are `haipipe-board`'s own `open` action, `regroup` wrapped `cli/regroup.py`, and `check` was a subset of `cli/check.py`.
Only `src/lanes.py` was code the family held nowhere else, and it moved into `haipipe-board-routing/src/`.
What the merge BOUGHT is the reason to prefer it over deleting the unit outright: a finding about a whole group had no landing rule and stayed in chat, because routing resolved pages only while the block such a finding belongs in was owned by the other unit.
One unit owning both altitudes settles that by construction, which is why the row below this one closed on the same ruling rather than needing its own.

### 3 · What the family ships today, counted

**The units on disk, 260802 after the merge and the new variant**: one door, four sub-skills, two agents, with the version each carries.

```
🚪 haipipe-board                  0.112.0   the DOOR · 14 cli · 11 src · live/
📄 haipipe-board-page             0.11.0    295 lines
🪞 haipipe-board-page-for-skill   0.1.0     the skill-page VARIANT, new 260802
✒️ haipipe-board-sentence         0.3.0     191 lines · ⚠️ changelog stops at 0.2.0
🧭 haipipe-board-routing          0.9.0     both altitudes · src/lanes.py
🤖 haipipe-board-reviewer-agent   0.4.0     read only, no write tools
🤖 haipipe-board-creator-agent    0.3.0     no Bash, one page per dispatch
🚧 haipipe-board-digest           not on disk
🗑 haipipe-board-index            merged into routing 260802, folder deleted
```
📌 Counted rather than estimated, because the roster argument is only as good as the count under it, and the first count on 260729 went stale within three days.

`ref/` carries 1017 lines across four files, and the plugin around this family holds 152 skills and 24 agents.
That still makes this the leanest family in the plugin.
For contrast, `task` ships 44 skills and 3 agents, `paper` 36 skills, `application` 23, and `discovery` 15 skills and 4 agents.

#### 3.1 · Leanness here is the intended shape, not an omission

The other families ship one door per DOMAIN STEP, while this one ships a FORM.
A form has one verb set (view, open, add, build, sync, link, close, serve, comment, stage, excalidraw), so a second and third door multiply the version surface without adding a workflow.
The count that changed between 260729 and 260802 is the sub-skills, not the verbs: `haipipe-board` itself went from v0.46.0 to v0.104.1 over the same window while keeping one door.

### 4 · Routing automates the hard step

**The claim, and the two ways it goes wrong**: what routing takes over from a person.

```
📋 the sync verb's order      claim the question → do the work → write it back
🤖 routing automates          ▲ this step
   ⚠️ failure 1               wrong claim   → right content, wrong page
   ⚠️ failure 2               blind offset  → a write splices a live sentence
   🛡 fix 1                    resolve through board.md ## Pages, never by name
   🛡 fix 2                    append at a ## section boundary, never at a byte
```
📌 Both failure modes already happened by hand on 260729 and 260730, which is why the fixes were written into the shipped contract before digest was built.

`haipipe-board`'s sync verb already says the order is claim which question first, then do the work, then write back in the same round, and that a piece of work belonging to no question is itself a question that should be opened.
Routing automates the claim, which makes both failure modes run at machine speed.

#### 4.1 · An id no longer predicts a folder

This board carries `QA2`, `QB8`, `QC1b` and `QB7` under group letters they were not opened under, precisely so external citations keep working.
So routing cannot resolve a page by name pattern: it has to read `board.md`'s `## Pages`, with `## Links` resolving the older ids.
`haipipe-board-routing` 0.6.0 states exactly that in its step 3, and `check.py`'s `declared_links` resolves ids the same way, so the two agree.

#### 4.2 · An unsupervised write can splice a sentence in half

A concurrent session did that to `QB4d` on 260730: a `### 2 · The source` block landed inside a `## Opening` sentence and cut it in half.
That was one agent writing one page, and digest by definition writes many pages at once, so it reproduces the damage at scale unless every write is anchored to a section boundary.

### 5 · What routing and digest may write

**Three permissions, none of them new**: what a transcript reader may do to a board.

```
✅ MAY WRITE      ## Log lines · ## States prose · a factual Aim State row
🟡 MAY PROPOSE    a ### Decision Now row · a page it would open
🚫 MAY NOT        tick a checkbox · flip state: · pass a human gate
🌍 OTHER BOARDS   mechanical writes yes · editorial writes become a report
```
📌 Neither verb needs a new permission model, because two rules already on the books decide every case.

#### 5.1 · The tick is off limits, because nothing untested gets ticked

A verb reading a transcript can report what the transcript CLAIMS, and it cannot verify that the claim is true.
So it may write `## Log` lines and `## States` prose, it may update an Aim State from evidence it inspected itself, and it may PROPOSE a tick; it may not close a checkbox or flip `state:`.

#### 5.2 · Across boards it is bound by `QB1` §4, like every other script here

Mechanical writes carry no judgement and are always allowed, while editorial writes are never ours on a board that is neither the skill set nor the board being worked.
Digest walks a whole session, so it will meet other people's boards on nearly every run, and there its output is a report to that owner rather than an edit.

#### 5.3 · That also settles skill against agent for digest

Digest has to re-read a session it was not in, which is the same reason the cold read is done by a fresh agent: a reader who was present cannot see what went unsaid.
So digest is a skill whose execution belongs in a fresh context, which is what the `task` and `discovery` families already do with their creator and orchestrator agents.

### 6 · Three places the form ships from

**Three exits, three verdicts**: where the form leaks, and whether the leak is a defect.

```
🚪 skills/board/*            the family's own doors           ✅ working as intended
📄 haipipe-paper-stage       the S page kind, under paper/    ✅ the first variant
🐍 live/chat.py 297–378      four rule strings, prose copies  ❌ the one real defect
```
📌 Counting the units understates the surface, because the form also reaches agents through a second family and through four Python strings that restate it.

#### 6.1 · `haipipe-paper-stage` is a variant door, not a leak

Its own summary reads "Board-first stage router: Paper is the public page creator; Board owns the shell, filename, pages, and optional inherited contracts", so the S page half of the form ships as a skill under `paper/`.
JL's base and variant model (ruled on `QB4`) settles how to read that: the page is a BASE, and a page kind is a Content variant that ships under its consumer family.
On that reading this is the first variant door working as intended, and `haipipe-paper-display` or a task variant would be the next ones.
What it sharpens is `haipipe-board-page`'s job: it ships the BASE contract the variant skills extend, so the spec has a second consumer beyond routing, namely the variant authors in the other families.

#### 6.2 · The four rule strings in `live/chat.py` are the one real defect

`CHAT_RULES` at line 297 teaches an agent one question page and `BOARD_CHAT_RULES` at line 353 teaches it the whole board, with `FULL_RULES` and `BOARD_FULL_RULES` doing the same for a full session.
None of the four reads `ref/` or either spec: all four restate them in a Python string, and `QB8d` already caught one describing a page shape that no longer existed.
They were the extraction's original trigger and they moved rather than changed, travelling from `cli/serve.py` into `live/chat.py` in the `QC2c` live-layer split, so the de-duplication is still owed.

#### 6.3 · The cheaper fix was available all along, and it is still the fix

The drawer's agent is already inside a board when it reads those rules, so `CHAT_RULES` alone never justified a door.
Making `live/chat.py` READ the specs instead of restating them kills all four copies, costs one function, and adds no version surface.
That is worth doing whether or not the page door ships, and the page door shipping does not do it by itself.

### 7 · Which unit supports which part

**The support map**: what a reader is looking at, and which unit backs it.

```
🗂 Board structure + top canvas        →  haipipe-board-routing (board altitude)
✍️ incoming user question              →  haipipe-board-routing (page altitude)
📄 Opening · Content · Aims · States   →  haipipe-board-page
✒️ Evidence Card · Comment · Edit      →  haipipe-board-sentence
🔁 recent conversation reconciliation  →  haipipe-board-digest
```
📌 The mapping is a support record, not a new skill per UI component, so a part of the board with no unit of its own is normal rather than a gap.

The Board-level SkillSet declares the linked units once, while each owning Page or subsection may point at the exact capability that supports it.
For example `QB8 · The sentence` should show `supported by haipipe-board-sentence · Evidence Card`.

#### 7.1 · When a capability earns its own door instead of a support row

If Evidence Card later gains an independent trigger, such as "collect, verify and reconcile evidence across many pages", it earns a `haipipe-board-evidence` skill then.
Until that consumer exists, splitting it would add a door without adding a workflow, which is `### 1`'s test applied to a UI part rather than to a folder seam.

#### 7.2 · Who owns the surrounding conventions

`QC3a` owns how these linked skills are declared and synchronized, and `QB4` owns the visible `🧩 Skills` support record on a Page.
`QA2` owns the proposal reviewed before the Index writes the structure, and `QB2` owns the rendered top view and relationship canvas.

### 8 · What is still open

**Four open threads, and what each is waiting on**: the page's remaining work at a glance.

```
🚧 digest                its contract, then a fresh-context build
🧹 live/chat.py          four rule strings become consumers of the specs
🤖 the reviewer agent    one 260729 sentence, still ambiguous
🧩 the support syntax    how a Page names its supporting unit
```
📌 Three of the four are unblocked and one waits on JL, so this part is the page's own worklist rather than an argument.

#### 8.1 · The reviewer agent's status

JL said "don't need to have the review agent, stop it" on 260729, while one dispatch was running, so it may mean that run only or the unit.
If it means the unit, three written things go stale at once: `SKILL.md` writing rule 3, which names the agent as the cold-read instrument, `QF1`'s acceptance half, where the agent is the fresh-context runner paired with `check.py`, and the `Agent-1` skill page.
Nothing has been changed on that reading, and the 260731 ruling that separated agents from skills argues the other way: a skill is LOADED and an agent is DISPATCHED, which is a distinction that only matters if the agent exists.

#### 8.2 · The caller's half of the creator agent

`Agent-2` is the producer half of the creator and reviewer pair, scoped by CONCURRENCY rather than by content, so its boundary is drawn by a different test than `### 1`'s: not "does it have its own trigger", but "does it touch a file another writer also touches".
One page's `.md` fails that test and fans out, while `board.md`, the lane block, the rebuild and the checker pass it and stay with the caller, which is why the agent has no Bash tool.
It is unshipped in the sense that matters: `haipipe-board`'s `open` and `add` still write pages one by one, and nothing turns an approved proposal table into N assignment packets.

#### 8.3 · A sentence BOARD is a different fork, and it needs nothing shipped

A dedicated design board for the sentence, a future `01-sentence-YYMMDD/`, is where sentence decisions would be argued if `QB8` outgrows this board.
That is a board-folder decision, which `QB1` owns through its two locations, and it is not a skill decision.

## Aims
### A1 · 🧪 The test a candidate has to pass
- A1.1 · Every candidate seam is judged by one stated test rather than by feel.
  **Done when:** The test is written on this page, and every seam in `skills/board/` has a recorded verdict naming the consumer that does or does not need it with no board open.

### A2 · 🧱 The roster, and what each unit owns
- A2.1 · JL rules the roster and its shipping order.
  **Done when:** Every named unit is either on disk or explicitly deferred, and no unit ships that JL did not name.
- A2.2 · Each shipped unit states what it owns, what stays in `ref/`, and which rule graduates into it.
  **Done when:** Every SKILL.md in the family carries that boundary, and no rule is written in two of them.

### A3 · 🔢 What the family ships today, counted
- A3.1 · What the family ships is counted, not estimated.
  **Done when:** The count names every unit with its version, and re-running it against disk changes nothing.

### A4 · 🧭 Routing automates the hard step
- A4.1 · Routing resolves a page through the registry rather than through a name pattern.
  **Done when:** Routing reads `board.md` `## Pages` with `## Links` for older ids, and `check.py` resolves ids the same way.
- A4.2 · An input at GROUP altitude has a landing rule.
  **Done when:** Routing states where a finding about a whole group lands, and one real group-altitude finding has been landed by it.

### A5 · ⚖️ What routing and digest may write
- A5.1 · Routing and digest have a write protocol before digest is built.
  **Done when:** What may be written, what may only be proposed, and the section-boundary anchor are all stated in a shipped contract rather than only on this page.

### A6 · 🧹 Three places the form ships from
- A6.1 · The board form stops being restated in Python.
  **Done when:** `live/chat.py`'s four rule strings load `haipipe-board-page` and `haipipe-board-sentence` instead of carrying their own prose copy.

### A7 · 🧩 Which unit supports which part
- A7.1 · A Page or subsection can name the unit that supports it without duplicating the Board-level SkillSet.
  **Done when:** The syntax is ruled and at least one page carries it.

### A8 · 🚧 What is still open
- A8.1 · `haipipe-board-digest` ships or leaves the roster.
  **Done when:** Either its contract exists on disk, or this page records the ruling that dropped it.
- A8.2 · `Agent-2` has a caller.
  **Done when:** `haipipe-board`'s `open` and `add` turn an approved proposal table into N assignment packets and run the serialized tail once.
- A8.3 · The reviewer agent's status is ruled.
  **Done when:** JL says whether "don't need to have the review agent" retired the unit or only that run, and the three dependent statements are corrected or left alone accordingly.

### P · 🏁 Page-level
- P1 · A reader can name every unit in this family and say what each one owns.
  **Done when:** A cold reader lists the roster from this page alone and matches disk.

## States
### Decision Now

- [x] 📐 Does `haipipe-board-index` stay a unit of its own?
      ✅ `B` · JL ruled 260802, in his own words: "maybe merge, I will do B".
      Merged into `haipipe-board-routing` 0.9.0, which now owns both write altitudes; the folder is deleted and `src/lanes.py` moved with it.
      The recommendation on this row had been `A`, retire it into the door, and JL took the option that also closes the group-altitude row below.

- [x] 🧭 Where does a group-altitude input land?
      ✅ `A` · Settled by the merge above rather than by a separate ruling.
      A finding about a whole group lands in that group's intro prose in `board.md` `## Pages`, written at the section boundary, with `lanes.py` refreshing the block underneath it.
      `B`, decomposing a group finding onto its member pages, is refused for the reason the row stated: the pieces individually say less than the whole did.
      The rule was only available once one unit owned both altitudes, which is what `B` above bought.

- [ ] 🧠 Is the roster ruling settled by conduct?
      📍 `Part` `### 2 · The roster, and what each unit owns`
      🔔 `Why now` The row has waited since 260731 while four units shipped on JL's own instructions, so the page still asks for a ruling it appears to have received.
      ⭐ `A ·` tick it: JL ordered index on 260730 and page, sentence and routing on 260731, so the roster is ruled and `digest` stays named and unshipped. This is what the page already behaves as if were true.
      `B ·` leave it open until `digest` is decided, treating a roster with an unbuilt member as unruled.
      🛑 `Blocks` nothing. Four units already ship either way.
      🤖 `If nobody answers` A. The conduct is on the record in `## Log` and the units are on disk.

- [ ] 🤖 Did "don't need to have the review agent" retire the unit, or only that run?
      📍 `Part` `### 8 · What is still open`, `8.1`
      🔔 `Why now` It was said on 260729 while one dispatch was running, and three written things depend on the reading: `SKILL.md` writing rule 3, `QF1`'s acceptance half, and the `Agent-1` skill page.
      ⭐ `A ·` that run only, so the unit stays. The 260731 ruling that a skill is LOADED and an agent is DISPATCHED gave agents their own page kind, which is a distinction that only matters if the agent exists.
      `B ·` the unit, so `Agent-1` retires and all three dependent statements are rewritten in the same edit.
      🛑 `Blocks` nothing today; the agent is not dispatched automatically.
      🤖 `If nobody answers` A. Nothing has been changed on the B reading, so A is already the status quo.

- [ ] 🚪 Where do routing's own design questions live?
      📍 `Part` `### 8 · What is still open`
      🔔 `Why now` Routing has shipped and reached 0.6.0, so it now generates design questions of its own, and this face is carrying them by default rather than by decision.
      ⭐ `A ·` this page stays the owner until digest is built, then both verbs get a page. The two verbs are one verb at two scales, so splitting them before digest exists would open a page with one member.
      `B ·` open a routing Q page in `QC` now, so a shipped unit has a page and this face goes back to being the roster only.
      🛑 `Blocks` nothing.
      🤖 `If nobody answers` A.

### A1 · 🧪 The test a candidate has to pass
- ✅ A1.1 · Met 260729 and restated here. Every seam in `skills/board/` was walked once, and `### 1.1` carries the verdict for each: stage argues for a clean script, live and canvas are runtime, and the checker, status and regroup are verbs of the manual.

### A2 · 🧱 The roster, and what each unit owns
- 🧠 A2.1 · Ruled by conduct and not yet by a tick. JL ordered `index` on 260730 and `page`, `sentence` and `routing` on 260731, and all four are on disk; the confirmation waits in Decision Now above.
- 🔨 A2.2 · The first audit found a duplication rather than confirming there was none, and the duplication is now resolved.
  `haipipe-board-index`'s `propose` and `materialize` were `haipipe-board`'s `open` action written a second time, and its `regroup` and `check` wrapped the door's own scripts.
  JL ruled `B` on 260802 and the unit is merged into `haipipe-board-routing` 0.9.0, which now owns both write altitudes; the folder is deleted and `src/lanes.py` moved with it.
  One duplication survives ON PURPOSE and is now declared in both files: the door's `open` still describes proposing and materializing a board, because a person opening their first board should not have to load a second skill.
  The remaining three units have not been audited against each other yet.

### A3 · 🔢 What the family ships today, counted
- ✅ A3.1 · Recounted against disk on 260802: five skills, two agents, versions in `### 3`. The 260729 count of two units is superseded and kept only in `## Log`.

### A4 · 🧭 Routing automates the hard step
- ✅ A4.1 · Met. `haipipe-board-routing` 0.6.0 step 3 reads `board.md` `## Pages` and resolves older ids through `## Links`, and `check.py`'s `declared_links` resolves ids the same way, so the resolver and the checker agree.
- ✅ A4.2 · Met 260802 by the merge rather than by a separate ruling.
  A group-altitude finding lands in that group's intro prose in `board.md` `## Pages`, written at the section boundary, with `lanes.py` refreshing the block underneath it.
  `haipipe-board-routing` 0.9.0 carries the rule under its own heading, and it was only available once one unit owned both altitudes.
  No real group-altitude finding has been landed through it yet, which is the half of this Aim that rests on the next one that arrives.

### A5 · ⚖️ What routing and digest may write
- ✅ A5.1 · Met for the half that ships. `haipipe-board-routing` 0.6.0 carries the human-decision law, the cross-board law and the anchored-append rule under its own headings, so digest inherits a written protocol rather than needing a new one.

### A6 · 🧹 Three places the form ships from
- ⬜ A6.1 · Not started. The four strings moved from `cli/serve.py` to `live/chat.py` in the `QC2c` live split and none of them reads `ref/` or either spec.

### A7 · 🧩 Which unit supports which part
- ⬜ A7.1 · Not started. The example wording exists in `### 7`, and no syntax has been ruled and no page carries one.

### A8 · 🚧 What is still open
- ⬜ A8.1 · Not started. `haipipe-board-digest` is named on the roster, described in `### 2.1`, and not on disk.
- ⬜ A8.2 · Not started. `Agent-2` exists at 0.1.0 and `haipipe-board`'s `open` and `add` still write pages one by one.
- 🧠 A8.3 · Waiting on the reviewer-agent ruling in Decision Now above.

### P · 🏁 Page-level
- 🔨 P1 · The roster, the versions and the owner of each unit are on the page as of 260802; no cold reader has been asked to list them back.

## Files
### 📋 Contracts · what CARRIES a rule to other pages
- `ref/page-template.md` · `ref/board-form.md`
  Where the page and sentence contracts shipped before the specs were cut, and still the authority both cite.
- `QC-engine/QC1a-skillmd.md`
  The specs-to-`ref/` Law this fork tests: what SKILL.md must say, and where the cut to `ref/` falls.
- `QB-delivery/QB1-form.md`
  §4, the standing rule deciding what routing and digest may write on a board that is not ours.

### ⚙️ Engines · what RUNS this subject
- `live/chat.py`
  Lines 297 to 378, the four hand-rolled rule strings that restate the page and board contracts instead of loading them.
- `haipipe-board-routing/SKILL.md`
  The shipped write protocol: the five-step route, the two write laws, and the three end states.

### 📤 Output files · what a BUILD writes
- `board/QC/QC1b-subskills.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit it; the markdown is the only source.

## Law
- 260802 JL · 🔀 **A unit whose verbs are other units' work is merged, not kept**
  JL ruled `B` on the index question: "maybe merge, I will do B".
  Three of its five verbs were the door's `open`, `regroup.py` and `check.py` written a second time, and one script was all it held alone.
  The test this sets for the next candidate is not whether the unit is a coherent topic, which the index was, but whether its VERB LIST is already somebody else's.
- 260802 CC · 🗂 **Filing a verb set as a contract hides its duplication**
  Index was shelved with Page and Sentence as a contract on 260730 and it never was one: its `SKILL.md` was five verbs and no contract.
  A unit filed on the wrong side of that split is never compared against the right list, which is how the duplication went two days unseen.
- 260729 JL · 🚪 **The roster is one door, two specs, two verbs**
  `haipipe-board` stays the operating manual; `haipipe-board-page` and `haipipe-board-sentence` are SPECS that other units load; `haipipe-board-routing` and `haipipe-board-digest` are VERBS that consume them.
  JL named the set directly, describing routing as "like an input, it will automatically find which page to go, to update the log and update the content as well" and digest as "the input will be the recent claude code content, update each haipipe page accordingly".
  `haipipe-board-index` joined on 260730 as the board and group altitude above the page.
- 260729 CC · 🧪 **A candidate can fail the test only because its consumer has not been proposed yet**
  CC recommended deferring `haipipe-board-page` and `haipipe-board-sentence` on the grounds that no consumer needed them with no board open.
  JL named routing and digest the same day and both are handed raw input with no board attached, so the consumer was never missing.
  Before rejecting a candidate, say who WOULD need it, not only who does today.
- 260731 JL · 🤖 **A skill is LOADED, an agent is DISPATCHED**
  Agents get their own page kind below the skills, which is why `Agent-1` and `Agent-2` are not Skill rows.
- 260731 JL · 🔀 **A concurrency boundary is drawn by a different test than a content boundary**
  For `Agent-2` the question is not "does it have its own trigger and version" but "does it touch a file another writer also touches".
  One page's `.md` fails that test and fans out; `board.md`, the lane block, the rebuild and the checker pass it and stay with the caller.

## Log
260802 2030 · `QB8` closed and `haipipe-board-sentence` reached 0.3.0 with three verbs, so the roster's contract-versus-action column is wrong a second time and in the opposite direction from the index. `2.3` now records both failures and rules that a row names what a reader DOES with a unit when it is both. The count in `3` corrected to 0.3.0 and 191 lines, with the changelog drift `agree.py` found flagged in place
260802 · 🚪 The sentence unit became a DOOR, on JL's read of the `haipipe-board-page` precedent ("we migrate that part from haipipe-board to haipipe-board-sentence, just like haipipe-board-page, right?"). The precedent is precise about what migrates: the page skill owns the page contract and its two verbs, owns no scripts, and CALLS the engine. The sentence half had been the other way round, with the operating detail in `haipipe-board`'s SKILL.md and a 94-line spec carrying no verbs. `haipipe-board-sentence` 0.3.0 now holds three verbs (comment, edit, card), the boundary block, and the reader's controls, at 192 lines against the page skill's 299; `haipipe-board` 0.111.0 keeps only the two rules that bind the ENGINE rather than the contract, which are that a write needs `serve.py` and that a form closes before it asks for the repaint. The one-door table now states the rule at every altitude: one sentence is the sentence skill's, one page is the page skill's, the board is the board skill's
260802 1810 · JL ruled `B`, merge: `haipipe-board-index` is deleted and `haipipe-board-routing` 0.9.0 owns both write altitudes, with `src/lanes.py` moved into it. Two Decision Now rows closed on the one ruling, because the group-altitude landing rule was only ever blocked on which unit would own it. `haipipe-board` 0.109.0 corrects the family block and its heading, which had said "three specs" while one of the three was a verb set. `Skill-1` retires to `_archive/` and `Skill-5` absorbs the altitude
260802 1710 · JL asked what `haipipe-board-index` is for, said it may not be needed, and proposed merging it with `haipipe-board-routing`. The question forced the first real `A2.2` audit and it found a duplication: three of the index's five verbs are the door's own `open`, `regroup.py` and `check.py` written a second time, and only `src/lanes.py` is code held nowhere else. Three options are on the row in Decision Now, and the recommendation is retiring the unit rather than merging it, because merging moves a script into a verb that holds none
260802 1610 · The renumber carried through to everything citing it. Four shipped skills pointed at `QC6 §7/§8/§9/§10` for the door test, the roster shape, the anchored write and the two write laws; all now read `QC1b §1/§2/§4/§5`, and `haipipe-board` 0.104.1, `-page` 0.8.1, `-routing` 0.6.1 and `-sentence` 0.1.2 record why. `board.md`'s QC group intro and `QC1`'s "four of six" both corrected in the same pass
260802 1600 · Content rebuilt from 13 divisions to 8, each with a face diagram: the roster layers of 260729, 260730 and 260731 merged into `### 2`, the withdrawn defer reading moved to `## Law`, and the stale count in `### 3` replaced with the 260802 figures (five skills, two agents, 152 plugin skills). Aims and States converted to the `A<n>` groups keyed to Content parts, Files regrouped onto the action menu, and the dead `QB1-skillmd.md` and `QA1-form.md` rows repointed at `QC1a-skillmd.md` and `QB1-form.md`
260802 1600 · `serve.py` lines 297 and 357 corrected to `live/chat.py` lines 297 to 378: the rule strings moved in the `QC2c` live-layer split and there are four of them, not two, so the de-duplication is the same defect at twice the size
260802 1230 · The `haipipe-writing` skill page closed: the skill exists on disk with three verbs, so the question was answerable, and it stays its own unit because its consumer is any authored prose rather than any board. Recorded in States and removed from Decision Now, per QB4 §5.2.7
260802 0000 · The candidate gained the design question it has to answer before it can ship: how a change record attaches when one sentence becomes six. The `✎` grammar assumes one record per sentence, splitting is the main move in this kind of rewrite, and the same misplacement happened twice by hand on 260801 because a record appended after a rewritten block silently attaches to the last new sentence rather than the one it describes
260801 2340 · `haipipe-write` added to the roster as a candidate awaiting JL's ruling, after an evening spent hand-rewriting QB4's `### 1` for a weak English reader and recording each edit in the `✎` lane
260801 0130 · Reindexed QC6 -> QC1b under the new QC1 skill-family parent; QC1b-vs-Skill-* overlap flagged on QC1 (JL 260801)
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260731 · Decision Now adopted (JL: proposals leave chat and land under the owning page's States); first rows here carry the two pending roster ticks, routing's group-altitude gap, and the home of routing's design questions
260731 · Agent-2, the page creator, joined as the producer half of the pair; the family's first unit scoped by concurrency rather than by content, and the caller's fan-out half is still owed
260731 · The reviewer separated from the skills as Agent-1, its own page kind below the Skill rows
260731 · haipipe-board-page, haipipe-board-sentence, haipipe-board-routing created contract-first and registered (Skill-3/4/5, SKILL.md family block, family README); digest and the chat-rules de-dup remain
260730 · Added haipipe-board-index and the three-layer model: Index proposes and materializes the approved Board structure and top canvas; Page owns sections; Sentence owns Evidence Card and other sentence records; Routing and Digest consume those contracts
260729 · JL's base/variant model (recorded on QB4) flips the reading of the form's second exit: haipipe-paper-stage is the first Content variant door rather than a leak, and haipipe-board-page would ship the base contract the variants extend
260729 · Opened from JL's two same-day asks (haipipe-board-page, haipipe-board-sentence); CC's recommendation was defer until the page and sentence groups settle
260729 · Counted the family at two units and found the form shipping from two places outside it: `haipipe-paper-stage` under `paper/`, and `CHAT_RULES` plus `BOARD_CHAT_RULES` inside `serve.py`
260729 · JL named `haipipe-board-routing` and `haipipe-board-digest`; they are the consumer the page and sentence doors were missing, so the defer recommendation is withdrawn
