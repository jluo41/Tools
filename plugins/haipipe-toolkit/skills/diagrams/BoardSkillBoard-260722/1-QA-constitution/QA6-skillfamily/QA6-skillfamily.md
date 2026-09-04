# What the family ships, and how a settled rule reaches it

state: 🟡 PARTIAL · the roster is ruled, four units ship · open: the cut line, chat.py's 4 copies, digest
owner: JL
method: name every candidate and apply one test to each, then let JL rule the set; SKILL.md stays as short as possible and is the only export channel for settled rules; a shipped unit follows settled decisions, never precedes them

## Opening
What does this family ship, and how does a settled decision reach an agent with no memory of this work?

A board is argued so that something can be handed on.
This page is the far end of that loop: it names every unit the family ships, applies one test to each candidate, and rules what the door itself must say and what it leaves to `ref/`.
It succeeds when a newcomer can name each shipped unit, and when every settled rule is written down exactly once.

**Where this page sits**: This is the fourth rung of the `QA` chapter: why a board exists (`QA00`), how one is born and closed (`QA2`), when a round may be handed back (`QA3`), and what graduates out of all that (here).

**What was folded in**: On 260816 this page's two faces became its own divisions: the sub-skill roster (`QA6b`, now `§1` to `§5`) and what `SKILL.md` must say (`QA6a`, now `§6`).
The parent had been 49 lines of pointers, and its one open aim asked whether to merge them.
The same round sent the write verb's own rules to `QB1a`, which now argues standing and every write it permits; what the roster still needs of them is `§2.5`.
Their full records sit whole in `_archive/QA6a-skillmd/` and `_archive/QA6b-subskills/`, and both ids resolve here through `## Links`.

**The test, in one line**: does some consumer need these rules with no board open? A yes makes it a door; a no makes it a `ref/` file the manual already points at.

**Covered elsewhere**: What a page IS, and its section contract: `QPs1`. What a sentence IS, and its records: `QS1`. Where a write may land on somebody else's board: `QB1` §4. How the shipped units' contracts are proven by a cold read: `QF2`. What standing permits a write, and the two altitudes the write verb works at: `QB1a`. One page per shipped unit: `QB1a` carries routing, `QPs1` carries the page engine, and the remaining units keep their design pages in the group that argues them.

## Diagram

**The family, one door and three units**, with the Page Types and Page Phases under the page engine: which unit runs at which moment, and what each one loads.

```
                        🚪 haipipe-board · the door you invoke
                                     │
        ┌────────────────────────────┴────────────────────────────┐
        │                                                         │
   ✍️ anything that WRITES                              🖌 a page edit
        │                                                         │
        ▼                                                         ▼
  🧭 haipipe-board-routing · both altitudes             📄 haipipe-page
     🗂 opening a board  Spine · Groups · Pages            TYPE x PHASE · sections
        canvas · lanes · writes NOTHING                 what a machine writes
        before approval                                          ▲
     ✍️ an ordinary turn Board → Group → Page → Section           │
        │                                                        │
        │  loads the spec it needs ─────────────────────────────┘
        │
        └──▶ ✒️ haipipe-sentence
               Evidence Card · Comment · Edit

  🔁 haipipe-board-digest  =  many recent turns, routing called once each
     🚧 named on the roster, not on disk
  🗑 haipipe-board-index   =  merged into routing 260802, folder deleted

  📜 SKILL.md · the ONE export channel: a page reaches ✅ and its Law is
     copied in; a 🟡 or 🔴 page never enters                        → §6
```

## Content
### 1 · The test a candidate has to pass

**The two shapes a rule can take**: what makes a capability a door rather than a file.

```
🚪 A DOOR                            📎 A ref/ FILE
   an agent CHOOSES to open it          a skill already inside points at it
   ✅ consumer has no board open        ✅ consumer is already in the workflow
   💰 costs a version surface           💰 costs nothing
   🧪 haipipe-page                🧪 ref/page-template.md
```
📌 One test decides every candidate, and this part records the test, the survey that applied it to every seam, and the reading it overturned.

A skill is a door an agent chooses to walk through, and a `ref/` file is something a skill already inside the door points at.
So the test is not "is this a coherent topic", it is "does some consumer need these rules with no board open".

**1.1 · Every seam in `skills/board/`, walked once on 260729**

- `haipipe-page`, the page contract: the strongest case.
  `QPf4b`'s drawer keeps a hand-rolled copy of exactly these instructions in a Python string, and `QS3` caught that copy describing a page shape that no longer existed, which is the rot duplication guarantees.
- `haipipe-sentence`, the apparatus grammar: second, on the same consumer plus the paper family's evidence card.
- `haipipe-board-stage`, the S-page machinery: already consumed across families, because `create-page.py` in the paper skill calls the Board's `stage.py`.
  That consumer needs the SCRIPT, not the instructions, so it argues for keeping `stage.py` clean rather than for a skill.
- the live layer (serve, chat, terminal) and the canvas (`xcal.py`): runtime, not instructions.
  Their sharing half is already a sibling SERVICE (`boards_api.py`, `QO6`), and a skill would be the wrong shape.
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

The test above says a door is a capability an agent CHOOSES to open, and until 260802 nobody had checked whether `haipipe-page` is actually chosen.
The 260731 fan-out could not answer it: its brief pasted the path to the skill's `SKILL.md` and named `QPs1` as the worked example, so all five agents read the contract as a plain file and not one of them ever invoked it.
The real test gave three fresh agents one sentence each and nothing else, with no path, no skill name and no example page.
All three opened this door unaided, at tool calls #5, #6 and #5, including the one phrased "can you clean up QF5-sentence-run for me", whose words match no trigger in the skill's description.
All three then drove their page from 15, 13 and 10 findings to zero, and the board fell from 210 findings to 171.
The door test passes on evidence, and what failed instead was scope: the same three agents wrote to 15 files, 1 file and 2 files from the same instruction, because the skill said where to start and never where to stop.
`haipipe-page` 0.10.0 adds that bound as steps 7 and 8 of the verb.

### 2 · The roster, and what each unit owns

**One door, one page engine, one sentence spec, one write verb**: the shape JL ruled, grown by 260806 into TYPE x PHASE under the engine.

```
🚪 haipipe-board          the operating manual you invoke to run a board
📄 haipipe-page     THE ENGINE · Page = TYPE x PHASE · verbs CREATE /
                                 WORK ON / RUN
   📚 page-types/         ten TYPE variants, for-design … for-venue
                                 (for-skill and for-stage among them)
   🌀 page-phases/        four PHASE contracts · draft · probe · revise · check
✒️ haipipe-sentence SPEC · what one sentence carries · and a door
                                 for 3 verbs since 260802 (comment · edit · card)
🧭 haipipe-board-routing  VERB · every write onto a board, at BOTH altitudes
                                 board.md's structure, and one input → one
                                 owning page → one anchored write
🔁 haipipe-board-digest   VERB · one session → many inputs → routing, fanned out
```
📌 The roster took its shape across four days: JL named the units on 260729, added the index altitude on 260730, ordered four of them built on 260731, and folded the index back into routing on 260802. The page unit then grew into the TYPE x PHASE engine, with its variants under `page-types/` and `page-phases/`, by 260806.

`haipipe-board` stays the public orchestrator, and it does not load every detailed contract on every turn: it invokes the smallest unit that owns the current transition.
That is the progressive-disclosure shape, so opening a Board loads Routing's board altitude, an ordinary turn loads Routing, a Page edit loads Page, and sentence apparatus loads Sentence.

**2.1 · What each unit owns**

- `haipipe-page`, the Page layer.
  It owns the common Page frame, the Page Types under `page-types/` and the Page Phases under `page-phases/`, the section contracts, Aims, States, paths and closure semantics, and the three verbs CREATE, WORK ON and RUN.
  The name is singular because it defines the contract for any ONE page, where `pages` would sound like a batch operation.
- `haipipe-sentence`, the atomic layer.
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
Neither verb has a board open when it starts and both are handed raw input, which is the test in `§1`, passed.
The split also gives every page and sentence rule a graduation target that is not "another section of the manual".

#### 2.3 · Contracts and actions are deliberately different things, and the split keeps failing

Page and Sentence began as contracts that other skills consume, while Routing and Digest are actions that consume those contracts.
The split has now been wrong twice, in opposite directions, which is worth more than either instance.
Index was filed as a CONTRACT on 260730 and was five verbs with no contract in it, and on 260802 both Page and Sentence grew verbs of their own and became doors as well, so the column they sit in is half true.
A unit is better described by what a reader DOES with it than by which column it was filed in, and every design page now names both when both apply.
That is why the two halves are named differently and versioned separately: a contract changes when the form changes, and an action changes when the workflow changes.
That misfiling is why the duplication in `2.4` went two days without being seen, because a unit shelved as a contract is not compared against an action's verb list.
The second failure runs the other way and cost nothing yet: `haipipe-sentence` reached 0.3.0 on 260802 with three verbs of its own, and this roster still called it a pure SPEC until its design page was rewritten the same evening.

#### 2.4 · The merge that removed a unit, and what it bought

JL asked on 260802 what the index was for, said it might not be needed, and proposed merging it with routing; his ruling was "maybe merge, I will do B".
The audit that question forced found three of its five verbs were other units' work written a second time: `propose` and `materialize` are `haipipe-board`'s own `open` action, `regroup` wrapped `cli/regroup.py`, and `check` was a subset of `cli/check.py`.
Only `src/lanes.py` was code the family held nowhere else, and it moved into `haipipe-board-routing/src/`.
What the merge BOUGHT is the reason to prefer it over deleting the unit outright: a finding about a whole group had no landing rule and stayed in chat, because routing resolved pages only while the block such a finding belongs in was owned by the other unit.
One unit owning both altitudes settles that by construction, which is why the row below this one closed on the same ruling rather than needing its own.

#### 2.5 · What the two verbs automate, and what bounds them

Routing automates the one step `haipipe-board`'s sync verb calls the hard one: claim which page owns the work, before the work is written down.
It resolves that claim through `board.md`'s `## Pages` with `## Links` for older ids, never through a name pattern, because an id on this board no longer predicts a folder: `QA2`, `QS1`, `QC1b` and `QPf2` all sit under group letters they were not opened under, precisely so external citations keep working.
`check.py`'s `declared_links` resolves ids the same way, so the resolver and the checker agree rather than drifting apart.
Digest is the same verb at session scale, which is why it calls routing rather than inventing a second policy, and why it runs in a fresh context: a reader who was present cannot see what went unsaid.

Reading a transcript is not the same as verifying it, and that sets the one permission line the roster needs.
Either verb may write a `## Log` line, `## States` prose, or an Aim State row it inspected itself, and may PROPOSE a `### Decision Now` row or a page it would open.
Neither may tick a checkbox, flip a `state:`, or pass a human gate, because a verb can report what a transcript CLAIMS and cannot check that the claim is true.
Everything else about a write belongs to `QB1a`: what standing permits on a board we do not own, the two altitudes, and the rule that a write lands under a named `##` heading and never at a byte offset.

### 3 · What the family ships today, counted

**The units on disk, recounted 260806**: four skills, ten Page Types, four Page Phases, three agents, with the version each carries; `haipipe-board-digest` stays named and unshipped.

```
🚪 haipipe-board                  0.124.0   the DOOR · 16 cli · 13 src · live/
📄 haipipe-page             0.21.0    THE ENGINE · 468 lines · CREATE /
                                            WORK ON / RUN · receipts in _runs/
📚 page-types/                    ten TYPE variants · for-design … for-venue
                                            incl. for-skill 0.4.2 · for-stage 0.5.0
🌀 page-phases/                   four PHASE contracts · draft · probe ·
                                            revise · check
✒️ haipipe-sentence         0.3.1     191 lines
🧭 haipipe-board-routing          0.9.1     both altitudes · src/lanes.py
🤖 haipipe-board-reviewer-agent   0.7.0     read only, no write tools
🤖 haipipe-board-creator-agent    0.6.0     no Bash, one page per dispatch
🤖 haipipe-page-orchestrator-agent
                                  0.1.0     runs one bounded Page RUN · first
                                            live RUN 260805 on QS2
🚧 haipipe-board-digest           not on disk
🗑 haipipe-board-index            merged into routing 260802, folder deleted
```
📌 Counted rather than estimated, because the roster argument is only as good as the count under it, and the first count on 260729 went stale within three days.

`ref/` carries 1120 lines across six files, and the plugin around this family holds 130 skills and 11 agents.
For contrast, `task` ships 44 skills and 3 agents, `application` 23 skills, `discovery` 15 skills and 4 agents, and `paper` collapsed to ONE door on 260805, `haipipe-paper` 0.7.0, with its stages as data.
Counted as doors this family ships four; the ten types and four phases are contracts under the engine, not doors of their own.

#### 3.1 · Leanness here is the intended shape, not an omission

The other families shipped one door per DOMAIN STEP, while this one ships a FORM; `paper` adopted the same one-door shape on 260805.
A form has one verb set (view, open, add, build, sync, link, close, serve, comment, stage, excalidraw), so a second and third door multiply the version surface without adding a workflow.
The count that changed between 260729 and 260802 is the sub-skills, not the verbs: `haipipe-board` itself went from v0.46.0 to v0.104.1 over the same window while keeping one door.

### 4 · Three places the form ships from

**Three exits, three verdicts**: where the form leaks, and whether the leak is a defect.

```
🚪 skills/board/*            the family's own doors           ✅ working as intended
📄 page-types/for-stage      the S page TYPE, home since      ✅ the exit closed
                             260805 (was haipipe-paper-stage)
🐍 live/chat.py 301–397      four rule strings, prose copies  ❌ the one real defect
```
📌 Counting the units understates the surface, because the form once shipped through a second family and still ships through four Python strings that restate it.

#### 4.1 · The variant door came home: for-stage ships under `page-types/` since 260805

`haipipe-paper-stage` was the form's second exit, the S page half shipping as a skill under `paper/`; it retired to `paper/_old/` on 260805 when the paper family collapsed to one door.
The S page variant now ships inside this family as `page-types/haipipe-page-for-stage` (0.5.0), one of the ten Page Types.
JL's base and variant model (ruled on the section-contract page, today `QPs1`) read the old exit as the first variant door working as intended, and the prediction played out: the display variant it foresaw exists as `page-types/haipipe-page-for-display`, and all ten variants now extend the BASE contract `haipipe-page` ships.
So the spec has its second consumer beyond routing, the variant contracts, and the second exit is closed.

#### 4.2 · The four rule strings in `live/chat.py` are the one real defect

`CHAT_RULES` at line 301 teaches an agent one question page and `BOARD_CHAT_RULES` at line 357 teaches it the whole board, with `FULL_RULES` and `BOARD_FULL_RULES` doing the same for a full session.
None of the four reads `ref/` or either spec: all four restate them in a Python string, and `QS3` already caught one describing a page shape that no longer existed.
They were the extraction's original trigger and they moved rather than changed, travelling from `cli/serve.py` into `live/chat.py` in the `QC1c` live-layer split, so the de-duplication is still owed.

#### 4.3 · The cheaper fix was available all along, and it is still the fix

The drawer's agent is already inside a board when it reads those rules, so `CHAT_RULES` alone never justified a door.
Making `live/chat.py` READ the specs instead of restating them kills all four copies, costs one function, and adds no version surface.
The page door has since shipped and did not do it by itself, which proves the point: the de-duplication is its own piece of work and is still owed.

### 5 · Which unit supports which part

**The support map**: what a reader is looking at, and which unit backs it.

```
🗂 Board structure + top canvas        →  haipipe-board-routing (board altitude)
✍️ incoming user question              →  haipipe-board-routing (page altitude)
📄 Opening · Content · Aims · States   →  haipipe-page
✒️ Evidence Card · Comment · Edit      →  haipipe-sentence
🔁 recent conversation reconciliation  →  haipipe-board-digest
```
📌 The mapping is a support record, not a new skill per UI component, so a part of the board with no unit of its own is normal rather than a gap.

The Board-level SkillSet declares the linked units once, while each owning Page or subsection may point at the exact capability that supports it.
For example `QS1 · The sentence` should show `supported by haipipe-sentence · Evidence Card`.

#### 5.1 · When a capability earns its own door instead of a support row

If Evidence Card later gains an independent trigger, such as "collect, verify and reconcile evidence across many pages", it earns a `haipipe-board-evidence` skill then.
Until that consumer exists, splitting it would add a door without adding a workflow, which is `§1`'s test applied to a UI part rather than to a folder seam.

#### 5.2 · Who owns the surrounding conventions

`QPs1` owns the visible `🧩 Skills` support record on a Page and how a linked unit is declared there, and `QPf10` owns the page's own ranked skill list in its `skill/` plugin.
`QA2` owns the proposal reviewed before the Index writes the structure, and `QB2` owns the rendered top view and relationship canvas.

### 6 · What SKILL.md must say, and where the cut falls

**The door and its six reference files**: what enters the context on every invocation, and what waits until detail is needed.

```
user types  /haipipe-board
          │
          ▼
      SKILL.md  771 lines (0.124.0, 260806): operations only, spec details never inlined
          ├─ the family: one door, one Page base (haipipe-page), two contract catalogs
          ├─ the shape: what a board looks like (Q + S pages, group intros, embeds)
          ├─ eleven verbs: view · open · add · stage · build · sync · link · close  (offline)
          │                serve · excalidraw · comment                             (live)
          │                plus routed verbs: one-page work goes to haipipe-page,
          │                one-sentence work to haipipe-sentence
          ├─ the metadata head + fixed section order of one Q/S page
          │  (the full page contract lives in board/haipipe-page)
          ├─ three writing rules (no invented terms / purge stale lines / fresh-agent cold read)
          ├─ the four prohibitions
          └─ board ↔ SKILL.md: the graduation mechanism
                │
                ▼  go to ref/ only when detail is needed
        ref/page-template.md          copy to add a Q or S page (renamed from q-template.md 260801)
        ref/board-form.md             full spec: folders · numbering · section↔render §4 · Links §4b · body syntax §5 · generated site §8
        ref/writing-rules.md          how to write plainly + cold-read prompt + convergence criterion
        ref/topic-entry-contract.md   the evidence page: head `route:` key · E<n> divisions · nested probes/ QA-probe records
        ref/board-example.md          a minimal two-question example
        ref/page-lifecycle.workflow.js  the bounded Page RUN controller (producer, build snapshot, independent CHECK, route)
```
📌 This file is the first thing every Board session reads, so each extra line has a recurring cost; cut too much and a newcomer cannot operate the tools or recover the rules this board settled.

#### 6.1 · Graduation is the only channel, and it only opens at ✅

This board is the full design record and `SKILL.md` keeps only the conclusions of `✅ SETTLED` pages.
When a page reaches ✅, its `## Law` rules are copied into the matching spot in `SKILL.md`; an unsettled page never enters, because an ad-hoc choice written as iron law is how a permission rule got hard-coded and then overturned.
So `SKILL.md` always equals the sum of the settled rules, and the question to ask before editing it is whether the owning page is ✅.
What this mechanism never had was a receipt, which `QA2` §6.2 ruled on 260816: a graduated Law row now carries `→ landed in <file> §<n>`, so anyone can check that the copying happened without re-reading both documents.

#### 6.2 · The cut line is described by feel and not yet by rule

The standing instruction is that `SKILL.md` stays minimal, operations only, with spec, syntax and prose detail in `ref/`, because the file enters the context on every invocation.
What is missing is a test a reader can apply to one paragraph, which is why the door has grown past the 581 lines JL ruled the shrink on: the family section, the routed verbs and the live layer's real action sections all moved in afterwards.
The live layer is the one part deliberately held to pointers: `serve`, `excalidraw` and `comment` carry real action sections, while chat and terminal wait for the `QPf4` pages to settle before they graduate.

#### 6.3 · What the fresh-agent read proved, and the gap it exposed

`QF2` ran on 260723 with a GPU-cluster topic: a fresh agent, given only `SKILL.md` and `ref/`, opened a valid five-question board on the first try, verdict YES, and the one real gap it exposed, how to invoke `build.py`, was fixed into the file.
The re-run on 260725 against the shared Q/S skill passed again, and cost more than it looked: every S instruction in the manual was about READING a stage, never about writing one, so the agent had to invent the `## Pages` listing, the state value, the filename and the probe pointer, and it guessed right, which is worse, because the documents then took credit for the agent's judgment.
All four are written down now, and the lesson is general: **the reading contract graduated on its own and left the authoring contract behind**, which is invisible to anyone who already knows both.

#### 6.4 · The 260731 audit, and why a mirror page being in sync proved nothing

JL asked whether the family's contract pages were up to date and dispatched three fresh reviewers, which was the first real use of the parallel pattern the creator agent was built for; they returned 20, 16 and 19 findings, every one carrying file-and-line evidence on both sides.
All seven mirror pages were already in sync, so nothing was stale in the sense the generator can detect; what the reviewers found is drift the generator cannot see, between a contract's words and the code it claims to describe.
The worst of it was a blind `Question` to `Opening` replacement that had turned three alias declarations into "Opening is an alias for Opening", destroying the only statement that keeps older pages parsing; the frontmatter version was two releases behind its own CHANGELOG, and two specs carried a version inside body prose that had rotted further still.
Everything that audit left open has since landed in the 0.124.x door: the `live/` package is documented file by file, `Skill-<n>` and `Agent-<n>` pages are named in the ref index, and the page contract moved into `haipipe-page` with its Page Types under `board/page-types/`.

### 7 · What is still open

**Five open threads, and what each is waiting on**: this page's own worklist.

```
🚧 digest                its contract, then a fresh-context build
🧹 live/chat.py          four rule strings become consumers of the specs
🤖 the reviewer agent    one 260729 sentence, still ambiguous
🧩 the support syntax    how a Page names its supporting unit
📏 the cut line          a rule for §6, and whether the board's prose
                         rules bind SKILL.md at all
```
📌 Four of the five are unblocked and one waits on JL, which makes this part a worklist rather than an argument.

#### 7.1 · The reviewer agent's status

JL said "don't need to have the review agent, stop it" on 260729, while one dispatch was running, so it may mean that run only or the unit.
If it means the unit, three written things go stale at once: `SKILL.md` writing rule 3, which names the agent as the cold-read instrument, `QF1`'s acceptance half, where the agent is the fresh-context runner paired with `check.py`, and the agent's own design page.
Nothing has been changed on that reading, and the 260731 ruling that separated agents from skills argues the other way: a skill is LOADED and an agent is DISPATCHED, which is a distinction that only matters if the agent exists.

#### 7.2 · The caller's half of the creator agent

The creator agent is the producer half of the creator and reviewer pair, scoped by CONCURRENCY rather than by content, so its boundary is drawn by a different test than `§1`'s: not "does it have its own trigger", but "does it touch a file another writer also touches".
One page's `.md` fails that test and fans out, while `board.md`, the lane block, the rebuild and the checker pass it and stay with the caller, which is why the agent has no Bash tool.
The caller's half now ships as written protocol: `haipipe-board` 0.124.0 says a batch dispatches one fresh creator per page, hands each an assignment packet of page facts, paths, sources and ownership context, and keeps shared writes, the one rebuild and the one check with the caller.
What stays open is conduct: `open` and `add` turning an approved proposal table into those packets as their routine path.

#### 7.3 · Whether the board's prose rules bind the family's own files

They do not today: `check.py` scans `page_files()`, so no checker has ever read a single `SKILL.md`, and one-sentence-per-line, English-only and no-em-dash are board-page rules only.
Measured on 260731: the four specs and verbs were already clean at 0 wrapped lines, `haipipe-board/SKILL.md` had 20, and the two agent files 8 and 3.
The row is in Decision Now, and the language half of it is already settled: JL ruled English for all the family's files on 260731 and it landed the same day.

#### 7.4 · A sentence BOARD is a different fork, and it needs nothing shipped

A dedicated design board for the sentence, a future `01-sentence-YYMMDD/`, is where sentence decisions would be argued if `QS1` outgrows this board.
That is a board-folder decision, which `QB1` owns through its two locations, and it is not a skill decision.

## Aims
### Decision Now
These are the calls only JL can make; CC ticks nothing here.

- [x] 📐 Does `haipipe-board-index` stay a unit of its own?
      ✅ `B` · JL ruled 260802, in his own words: "maybe merge, I will do B".
      Merged into `haipipe-board-routing` 0.9.0, which now owns both write altitudes; the folder is deleted and `src/lanes.py` moved with it.
      The recommendation on this row had been `A`, retire it into the door, and JL took the option that also closes the group-altitude row below.

- [x] 🧭 Where does a group-altitude input land?
      ✅ `A` · Settled by the merge above rather than by a separate ruling.
      A finding about a whole group lands in that group's intro prose in `board.md` `## Pages`, written at the section boundary, with `lanes.py` refreshing the block underneath it.
      `B`, decomposing a group finding onto its member pages, is refused for the reason the row stated: the pieces individually say less than the whole did.
      The rule was only available once one unit owned both altitudes, which is what `B` above bought.

- [x] 🗣 Rule the language of the family's own contracts
      ✅ `A`, applied to ALL of them and not only the door, JL 260731: "yes, do it. Apply to all".
      `haipipe-board/SKILL.md` was 342 of 581 lines Chinese while all five sibling units and both agents were 0%, and 32 normative rules existed ONLY in Chinese, three of them load-bearing: the one mandatory stop-and-ask gate before scaffolding a board, the whole write-back obligation, and the rule keeping a listener that carries a real shell on loopback.
      LANDED 260731 across `SKILL.md`, `ref/board-form.md` and `ref/board-example.md`, all three at 0 Chinese in the body, 0 em-dash and 0 hard-wrapped lines; the board's warnings fell from 34 to 13 the same day.
      Two categories of Chinese are deliberately KEPT, because they are data a machine matches on rather than prose a reader follows: the legacy section aliases inside backticks in `board-form.md` §4, and the trigger phrases in the door's frontmatter description, which are how a Chinese-speaking user reaches the skill at all.

- [x] 🧾 Rule what the door owes now that it is 581 lines
      ✅ `B` · JL 260731: move the stale halves into the specs that now own them and let the door shrink.
      The reviewers had found the door promising three things it cannot execute: the creator-agent fan-out, authoring a `Skill-<n>` or `Agent-<n>` page, and writing a `### Decision Now` row.
      The family was split precisely so the door could stop restating what the specs own, and three of those four areas already have a better home.

- [ ] 🧠 Is the roster ruling settled by conduct?
      📍 `Part` `§2 · The roster, and what each unit owns`
      🔔 `Why now` The row has waited since 260731 while four units shipped on JL's own instructions, so the page still asks for a ruling it appears to have received.
      ⭐ `A ·` tick it: JL ordered index on 260730 and page, sentence and routing on 260731, so the roster is ruled and `digest` stays named and unshipped. This is what the page already behaves as if were true.
      `B ·` leave it open until `digest` is decided, treating a roster with an unbuilt member as unruled.
      🛑 `Blocks` nothing. Four units already ship either way.
      🤖 `If nobody answers` A. The conduct is on the record in `## Log` and the units are on disk.

- [ ] 🤖 Did "don't need to have the review agent" retire the unit, or only that run?
      📍 `Part` `§7 · What is still open`, `7.1`
      🔔 `Why now` It was said on 260729 while one dispatch was running, and three written things depend on the reading: `SKILL.md` writing rule 3, `QF1`'s acceptance half, and the agent's design page.
      ⭐ `A ·` that run only, so the unit stays. The 260731 ruling that a skill is LOADED and an agent is DISPATCHED gave agents their own page kind, which is a distinction that only matters if the agent exists.
      `B ·` the unit, so the agent retires and all three dependent statements are rewritten in the same edit.
      🛑 `Blocks` nothing today; the agent is not dispatched automatically.
      🤖 `If nobody answers` A. Nothing has been changed on the B reading, so A is already the status quo.

- [ ] 🚪 Where do routing's own design questions live?
      📍 `Part` `§7 · What is still open`
      🔔 `Why now` Routing has shipped and reached 0.9.1, so it now generates design questions of its own, and this page is carrying them by default rather than by decision.
      ⭐ `A ·` this page stays the owner until digest is built, then both verbs get a page. The two verbs are one verb at two scales, so splitting them before digest exists would open a page with one member.
      `B ·` open a routing Q page in `QC` now, so a shipped unit has a page and this page goes back to being the roster only.
      🛑 `Blocks` nothing. Routing's own design page is `Design-2`, which records the unit; this row is about where its open QUESTIONS live.
      🤖 `If nobody answers` A.

- [ ] 📏 Rule whether the board's prose rules bind `SKILL.md` at all
      📍 `Part` `§7 · What is still open`, `7.3`
      🔔 `Why now` The rules are enforced on every page and on none of the family's own files, and the door is the file a fresh agent actually reads.
      ⭐ `A ·` extend `check.py` to the family's own `SKILL.md` and `ref/` files, so the rules bind the contracts the way they bind a page.
      `B ·` keep the rules board-only and treat a skill file as prose whose author decides, which is the status quo.
      `C ·` rule them in but enforce by review rather than by checker.
      🛑 `Blocks` nothing; it decides whether A6.2's cut line can be checked or only reviewed.
      🤖 `If nobody answers` A for one sentence per line and no em-dash, because both are cheap to check and every recently written unit already passes.


### A1 · 🧪 The test a candidate has to pass
- ✅ A1.1 · Every candidate seam is judged by one stated test rather than by feel.
  **Done when:** The test is written on this page, and every seam in `skills/board/` has a recorded verdict naming the consumer that does or does not need it with no board open.
  **Now:** Met 260729 and restated here. Every seam in `skills/board/` was walked once, and `§1.1` carries the verdict for each: stage argues for a clean script, live and canvas are runtime, and the checker, status and regroup are verbs of the manual.


### A2 · 🧱 The roster, and what each unit owns
- 🧠 A2.1 · JL rules the roster and its shipping order.
  **Done when:** Every named unit is either on disk or explicitly deferred, and no unit ships that JL did not name.
  **Now:** Ruled by conduct and not yet by a tick. JL ordered `index` on 260730 and `page`, `sentence` and `routing` on 260731, and all four are on disk; the confirmation waits in Decision Now above.
- 🔨 A2.2 · Each shipped unit states what it owns, what stays in `ref/`, and which rule graduates into it.
  **Done when:** Every SKILL.md in the family carries that boundary, and no rule is written in two of them.
  **Now:** The first audit found a duplication rather than confirming there was none, and the duplication is now resolved.
  `haipipe-board-index`'s `propose` and `materialize` were `haipipe-board`'s `open` action written a second time, and its `regroup` and `check` wrapped the door's own scripts.
  JL ruled `B` on 260802 and the unit is merged into `haipipe-board-routing` 0.9.0, which now owns both write altitudes; the folder is deleted and `src/lanes.py` moved with it.
  One duplication survives ON PURPOSE and is now declared in both files: the door's `open` still describes proposing and materializing a board, because a person opening their first board should not have to load a second skill.
  The remaining three units have not been audited against each other yet.
- ✅ A2.3 · Routing resolves a page through the registry rather than through a name pattern.
  **Done when:** Routing reads `board.md` `## Pages` with `## Links` for older ids, and `check.py` resolves ids the same way.
  **Now:** Met. `haipipe-board-routing` 0.6.0 step 3 reads `board.md` `## Pages` and resolves older ids through `## Links`, and `check.py`'s `declared_links` resolves ids the same way, so the resolver and the checker agree.
- ✅ A2.4 · An input at GROUP altitude has a landing rule.
  **Done when:** Routing states where a finding about a whole group lands, and one real group-altitude finding has been landed by it.
  **Now:** Met 260802 by the merge rather than by a separate ruling.
  A group-altitude finding lands in that group's intro prose in `board.md` `## Pages`, written at the section boundary, with `lanes.py` refreshing the block underneath it.
  `haipipe-board-routing` 0.9.0 carries the rule under its own heading, and it was only available once one unit owned both altitudes.
  No real group-altitude finding has been landed through it yet, which is the half of this Aim that rests on the next one that arrives.
- ✅ A2.5 · Routing and digest have a write protocol before digest is built.
  **Done when:** What may be written, what may only be proposed, and the section-boundary anchor are all stated in a shipped contract rather than only on this page.
  **Now:** Met for the half that ships. `haipipe-board-routing` 0.6.0 carries the human-decision law, the cross-board law and the anchored-append rule under its own headings, so digest inherits a written protocol rather than needing a new one.


### A3 · 🔢 What the family ships today, counted
- ✅ A3.1 · What the family ships is counted, not estimated.
  **Done when:** The count names every unit with its version, and re-running it against disk changes nothing.
  **Now:** Recounted against disk on 260806: four skills, ten Page Types, four Page Phases, three agents, versions in `§3`. The 260802 count of five skills and two agents is superseded, like the 260729 count of two units before it, and kept only in `## Log`.


### A4 · 🧹 Three places the form ships from
- ⬜ A4.1 · The board form stops being restated in Python.
  **Done when:** `live/chat.py`'s four rule strings load `haipipe-page` and `haipipe-sentence` instead of carrying their own prose copy.
  **Now:** Not started. The four strings moved from `cli/serve.py` to `live/chat.py` in the `QC1c` live split and none of them reads `ref/` or either spec.


### A5 · 🧩 Which unit supports which part
- ⬜ A5.1 · A Page or subsection can name the unit that supports it without duplicating the Board-level SkillSet.
  **Done when:** The syntax is ruled and at least one page carries it.
  **Now:** Not started. The example wording exists in `§5`, and no syntax has been ruled and no page carries one.


### A6 · 📜 What SKILL.md must say, and where the cut falls
- ✅ A6.1 · The door answers the four operating questions a newcomer arrives with.
  **Done when:** `SKILL.md` states how to open a board, how to add a page, when a board closes, and how it stays in sync with the board, each as an action a reader can run.
  **Now:** Met and kept current through the 0.124.x series: the door answers how to open a board (five steps, with the one place it must stop and ask), how to add a page (copy `ref/page-template.md`, rename, list it, rebuild), when a board closes (every page ✅ or ⏸️ and `close:` satisfied), and how it stays in sync (the graduation mechanism, written in as its own section).
- 🧠 A6.2 · The cut line to `ref/` is a rule rather than a feel.
  **Done when:** One test decides for any paragraph whether it belongs in `SKILL.md` or in `ref/`, and the door has been re-read against it once.
  **Now:** Open, and this is the page's oldest unruled item. The instruction "operations only, spec detail to `ref/`" is a direction rather than a test, and the door has grown from the 581 lines JL ruled the shrink on to 771 at 0.124.0 while every addition looked like an operation.
- 🔨 A6.3 · The live layer graduates in as its pages settle.
  **Done when:** chat and terminal carry real action sections, added one at a time as the `QPf4` pages reach ✅.
  **Now:** Partly landed: `serve`, `excalidraw` and `comment` carry real action sections, while chat and terminal stay pointer-only until the `QPf4` pages settle.
- ✅ A6.4 · A fresh agent can open a decent board from the door alone.
  **Done when:** `QF2` passes on a topic the manual has never seen, and every gap it exposes is written back into the file.
  **Now:** Met twice. `QF2` passed on 260723 on a topic the manual had never seen and again on 260725 against the shared Q/S skill; both runs' gaps were written back the same day, and the S-page authoring gap the second run exposed is the lesson recorded in `§6.3`.


### A7 · 🚧 What is still open
- ⬜ A7.1 · `haipipe-board-digest` ships or leaves the roster.
  **Done when:** Either its contract exists on disk, or this page records the ruling that dropped it.
  **Now:** Not started. `haipipe-board-digest` is named on the roster, described in `§2.1`, and not on disk.
- 🔨 A7.2 · The creator agent has a caller.
  **Done when:** `haipipe-board`'s `open` and `add` turn an approved proposal table into N assignment packets and run the serialized tail once.
  **Now:** The caller protocol ships in `haipipe-board` 0.124.0: one fresh creator per page, assignment packets, and the serialized tail (shared writes, one rebuild, one check) kept with the caller; the creator agent is at 0.6.0. The remaining half is `open` and `add` running that protocol routinely from an approved proposal table.
- 🧠 A7.3 · The reviewer agent's status is ruled.
  **Done when:** JL says whether "don't need to have the review agent" retired the unit or only that run, and the three dependent statements are corrected or left alone accordingly.
  **Now:** Waiting on the reviewer-agent ruling in Decision Now above.


### P · 🏁 Page-level
- 🔨 P1 · A reader can name every unit in this family and say what each one owns.
  **Done when:** A cold reader lists the roster from this page alone and matches disk.
  **Now:** The roster, the versions and the owner of each unit are on the page as of 260806; no cold reader has been asked to list them back since the 260816 fold.


## Files
### 📋 Contracts · what CARRIES a rule to other pages
- `../../board/haipipe-board/SKILL.md`
  The deliverable of `§6`, and the family's only export channel for a settled rule.
- `ref/page-template.md` · `ref/board-form.md` · `ref/writing-rules.md` · `ref/topic-entry-contract.md` · `ref/board-example.md` · `ref/page-lifecycle.workflow.js`
  The six files the cut line sends detail to; `SKILL.md` stays short because these catch everything.
- `2-QB-board/QB1-form/QB1-form.md`
  §4, the standing rule deciding what routing and digest may write on a board that is not ours.

### ⚙️ Engines · what RUNS this subject
- `live/chat.py`
  Lines 301 to 397, the four hand-rolled rule strings that restate the page and board contracts instead of loading them.
- `haipipe-board-routing/SKILL.md`
  The shipped write protocol: the five-step route, the two write laws, and the three end states.
- `../../board/haipipe-board/CHANGELOG.md`
  One entry per body of work, its version matching `SKILL.md`'s `version:` line; its early self-correction still stands, that stripping every script leaves every page and all body text intact.

### 🗃 The folded faces · kept whole
- `_archive/QA6a-skillmd/` · `_archive/QA6b-subskills/`
  The two pages this one absorbed on 260816, with their own States, Laws and Logs unrewritten.

### 📤 Output files · what a BUILD writes
- `board/QA/QA6-skillfamily.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit it; the markdown is the only source.

## Law
- 260723 CC · 🎓 **Graduation: SKILL.md is the crystallization of the board's settled pages**
  This board is the full design record; `SKILL.md` keeps only the conclusions of `✅ SETTLED` pages.
  When a page reaches ✅, copy its `## Law` rules into the matching spot in `SKILL.md`; an unsettled page never enters, or an ad-hoc choice gets written as iron law, which is exactly how one permission rule was hard-coded and later overturned.
- 260723 CC · 📜 **SKILL.md stays minimal**
  Operations only; spec, syntax and prose detail all go to `ref/`, because the file enters the context on every invocation.
- 260802 JL · 🔀 **A unit whose verbs are other units' work is merged, not kept**
  JL ruled `B` on the index question: "maybe merge, I will do B".
  Three of its five verbs were the door's `open`, `regroup.py` and `check.py` written a second time, and one script was all it held alone.
  The test this sets for the next candidate is not whether the unit is a coherent topic, which the index was, but whether its VERB LIST is already somebody else's.
- 260802 CC · 🗂 **Filing a verb set as a contract hides its duplication**
  Index was shelved with Page and Sentence as a contract on 260730 and it never was one: its `SKILL.md` was five verbs and no contract.
  A unit filed on the wrong side of that split is never compared against the right list, which is how the duplication went two days unseen.
- 260729 JL · 🚪 **The roster is one door, two specs, two verbs**
  `haipipe-board` stays the operating manual; `haipipe-page` and `haipipe-sentence` are SPECS that other units load; `haipipe-board-routing` and `haipipe-board-digest` are VERBS that consume them.
  JL named the set directly, describing routing as "like an input, it will automatically find which page to go, to update the log and update the content as well" and digest as "the input will be the recent claude code content, update each haipipe page accordingly".
  `haipipe-board-index` joined on 260730 as the board and group altitude above the page, and merged back into routing on 260802.
- 260729 CC · 🧪 **A candidate can fail the test only because its consumer has not been proposed yet**
  CC recommended deferring `haipipe-page` and `haipipe-sentence` on the grounds that no consumer needed them with no board open.
  JL named routing and digest the same day and both are handed raw input with no board attached, so the consumer was never missing.
  Before rejecting a candidate, say who WOULD need it, not only who does today.
- 260731 JL · 🤖 **A skill is LOADED, an agent is DISPATCHED**
  Agents get their own page kind below the skills, which is why the three agents are design pages of their own rather than roster rows.
- 260731 JL · 🔀 **A concurrency boundary is drawn by a different test than a content boundary**
  For the creator agent the question is not "does it have its own trigger and version" but "does it touch a file another writer also touches".
  One page's `.md` fails that test and fans out; `board.md`, the lane block, the rebuild and the checker pass it and stay with the caller.

## Log
- 260816 · [REVISE-CC] the content was cut clean: the two divisions on what routing automates and what routing and digest may write left the page, because `QB1a` now argues standing and every write the verb performs, and holding both was one subject written twice.
  What the roster actually needs of them is `§2.5`, nine lines: the claim step, the registry resolution, digest as the same verb at session scale, and the one permission line a transcript reader obeys.
  Divisions renumbered 9 to 7, their Aims and States with them (`A4`/`A5` became `A2.3`-`A2.5` under the roster); no fact left the board.
- 260816 · [FOLD-CC, JL ruled] the two faces became divisions of this page: the roster is `§1` to `§3` (was `QA6a`'s sibling `QA6b`) and the door's cut line is `§6` (was `QA6a`), with the open threads merged into `§7`.
  The parent had been 49 lines of pointers whose one open aim asked whether to merge them, which is the same answer the board reached four times before on `QB4`, `QB8`, `QPf4` and `QA00`.
  Both faces are archived whole with their Logs; their ids resolve here through `## Links`; and the retired ids inside the absorbed prose were swept to the current names in the same pass (`QB4` → `QPs1`, `QB8`/`QB8d` → `QS1`/`QS3`, `QD2` → `QPf4b`, `QE3` → `QO6`, `QC2c` → `QC1c`, `Skill-*`/`Agent-*` → the `Design-*` pages).
- (the absorbed faces' own Logs stay in `_archive/QA6a-skillmd/` and `_archive/QA6b-subskills/`, unrewritten)

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0