# Sub-skills: what else this family ships
state: 🟡 PARTIAL · roster ruled 260731, four of six shipped
owner: JL
method: name every candidate and apply one test to each, then let JL rule the set; a shipped skill follows settled decisions, never precedes them

## Question
Which Board capabilities need their own loadable unit, and which should remain inside the main manual?

A separate unit is useful only when a consumer needs its rules without loading the whole Board workflow.
The difficult seam is between reusable contracts, actions that consume them, and runtime code that needs no new door.
Getting the roster wrong either duplicates rules or hides a capability that another workflow must load directly.
It succeeds when every shipped unit has a distinct consumer, owner, and reason to exist.


## Boundary
- ✅ Covered here
  The shipping decision: which units exist, what each owns, and what the split costs.
- ↪ Covered elsewhere
  What the page contract IS: the `QAa` group. What the sentence contract IS: the `QAb` group.
  What SKILL.md must say, and the rule that specs go to `ref/`: `QC1`.
  Where a write is allowed to land on somebody else's board: `QB1` §4.

## Diagram

```
user topic
    |
    v
haipipe-board-index
propose Spine · Close · Groups · Pages · relationships · SkillSet
    |
    v
human confirms the structure
    |
    +--> Board-Webpage-Index + Board-Webpage-Group
    +--> relationship canvas at the top
    +--> Q / S / SKILL pages
             |
every later user turn
             v
haipipe-board-routing
Board -> Group -> Page -> Section
             |
      +------+------+
      |             |
      v             v
haipipe-board-page  haipipe-board-sentence
section contracts   Evidence Card · Comment · Edit · Chat
      \             /
       \           /
        v         v
      one anchored Board write

haipipe-board-digest = many recent turns -> routing repeated safely
```

## Content
### 1 · The case for staying one skill
The contracts already ship: `ref/page-template.md` + `ref/board-form.md` carry the page, and the sentence grammar rides `ref/board-form.md` and `src/body.py`.
`QC1`'s Law keeps SKILL.md shortest with specs in `ref/`, and nothing today needs to LOAD page-only or sentence-only rules without the whole board skill.
A second and third door multiply the version surface and the graduation targets: every QAa/QAb Law would need a home decision three ways instead of two.

### 2 · What would trigger the split
A consumer that needs the page or sentence rules in isolation: the QD2 drawer priming a per-question session, another plugin adopting the page form without boards, or the QAa/QAb Laws outgrowing `ref/`.
If the trigger arrives, the split follows the graduation rule: the groups settle first, then the skill is cut from their Laws.

### 3 · The candidate roster, surveyed 260729
Every seam in `skills/board/` was walked once, and the test for each candidate is the same: does a consumer need its rules WITHOUT the whole board skill?
`haipipe-board-page`, the page contract: the strongest case. The QD2 drawer's `CHAT_RULES` in `serve.py` is already a hand-rolled copy of exactly these instructions, and `QAb3` caught it describing a page that no longer existed, which is the rot that duplication guarantees. Extracting the page contract and making `CHAT_RULES` its consumer kills the second copy.
`haipipe-board-sentence`, the apparatus grammar: second. Same consumer (the drawer must teach an agent what a `>` lane is), plus the paper family's evidence card.
`haipipe-board-stage`, the S-page contract machinery: already consumed cross-family, `create-page.py` in the paper skill calls the Board's `stage.py`. But that consumer needs the SCRIPT, not instructions, so it argues for keeping `stage.py` clean, not for a skill.
The live layer (serve, chat, terminal) and the canvas (`xcal.py`): runtime, not instructions. Their sharing half is already a sibling SERVICE (`boards_api.py`, QE3), and a skill would be the wrong shape.
`status.py`, `regroup.py`, the checker: verbs of the main skill; splitting them buys nothing.
So the roster, if JL splits at all, is two: page and sentence, cut from the QAa and QAb Laws when those groups settle, with `CHAT_RULES` becoming the first consumer of both.

### 4 · A sentence BOARD is a different fork
A dedicated design board for the sentence (a future `01-sentence-YYMMDD/`) would be where sentence decisions get argued if QAb outgrows this board.
That is a board-folder decision (`QB1`'s two locations), not a skill decision, and it needs nothing shipped.

### 5 · What the family ships today, counted (260729, second pass)
`skills/board/` holds exactly two shipped units, and the plugin around it holds 144 skills and 9 agents.
- `haipipe-board`, one skill, v0.46.0
  518 lines of SKILL.md, 869 lines across the four `ref/` files, 12 scripts, 9 `src/` modules.
- `haipipe-board-reviewer-agent`, one agent, v1.0.0
  Read only, no write tools.
That makes this family the leanest in the plugin, tied with `probe`. For contrast: `task` ships 44 skills and 3 agents, `paper` 36 skills, `application` 23, `discovery` 15 skills and 4 agents.
Leanness here is the intended shape, not an omission: the other families ship one door per DOMAIN STEP, while this one ships a FORM, and a form has one verb set (view, open, add, build, sync, link, close, serve, comment, stage, excalidraw).

### 6 · The form already ships from three places, and only one is a door
Counting the units understates the surface. The board form leaks out of `skills/board/` in two more places, both found on 260729.
- `paper/1-lifecycle/haipipe-paper-stage`, a real second door in ANOTHER family
  Its own summary reads "Board-first stage router: Paper is the public page creator; Board owns the shell, filename, pages, and optional inherited contracts." So the S page half of the form is already a shipped skill; it just lives under `paper/`. The sub-skill question is therefore not "one door or three", it is "does the split live under `board/`, or keep crossing families as it does now".
- `serve.py` lines 297 and 357, two hand rolled prose copies
  `CHAT_RULES` teaches an agent one question page; `BOARD_CHAT_RULES` teaches it the whole board. Neither reads `ref/`; both restate it in a Python string. `QAb3` already caught one describing a page shape that no longer existed.
- JL reframed the first crossing later the same day, and it flips the reading
  The page is a BASE and a page kind is a Content variant shipping under its consumer family (the model on `QAa0`): on that reading `haipipe-paper-stage` is not the form leaking out of `skills/board/`, it is the first variant door working as intended, and `haipipe-paper-display` or a task variant would be the next ones.
  What it sharpens rather than answers: `haipipe-board-page` would ship the BASE contract that the variant skills extend, so the §8 roster's page spec gains a second consumer beyond routing, the variant authors in the other families.

### 7 · The test a candidate has to pass, and who was failing it
A skill is a door an agent CHOOSES to walk through. A `ref/` file is something a skill already inside the door points at. So the test is not "is this a coherent topic", it is "does some consumer need these rules with no board open".
- on that test, `CHAT_RULES` alone does not justify a door
  The drawer's agent is already inside a board when it reads those rules. Making `serve.py` read `ref/` instead of restating it kills both copies, costs one function, and adds no version surface. Extracting `haipipe-board-page` would also kill the copies, but by the more expensive route.
- CC's 260729 first reading was therefore "defer page and sentence", and JL's roster overturns it
  The reason it was wrong is recorded in §9: the missing consumer was not missing, it was simply not proposed yet.

### 8 · JL's roster, 260729: five units, two specs and two verbs around one door
JL named the set directly: `haipipe-board`, `haipipe-board-page`, `haipipe-board-sentence`, `haipipe-board-routing`, `haipipe-board-digest`, with routing described as "like an input, it will automatically find which page to go, to update the log and update the content as well", and digest as "the input will be the recent claude code content, update each haipipe page accordingly".
- the two new units are VERBS, and they are the same verb at two scales
  Routing is the unit operation: one input, find its owning page, write it back. Digest is the batch: one session transcript, many inputs, many pages. Digest is routing fanned out, so digest calls routing rather than reimplementing it.
- the two old candidates are SPECS, and the verbs are exactly the consumer they were missing
  Routing has to answer "which page, and which section of it", which is the page contract. It then has to write a line that reads like the board, which is the sentence contract. Neither verb has a board open when it starts; both are handed raw input. That is the test in §7, passed.
- so the shape is one door, two specs, two verbs
  `haipipe-board` stays the operating manual you invoke to run a board. `haipipe-board-page` and `haipipe-board-sentence` are what routing and digest LOAD. This also gives every QAa and QAb Law a graduation target that is not "another section of the manual".

### 9 · Routing is the automation of the step SKILL.md already calls the hard one
The sync verb already says the order is claim which question first, then do the work, then write back in the same round, and that a piece of work belonging to no question is itself a question that should be opened.
Routing automates the claim. That makes two existing failure modes machine-speed, and both have evidence from 260729 alone.
- a wrong claim writes the right content onto the wrong page
  Today's board has QA2, QA6, QC2, QB3 and QA2 living under group letters they were not opened under, precisely so external citations keep working. An id no longer predicts a folder, so routing cannot resolve a page by name pattern; it has to read `board.md`'s `## Pages`.
- an unsupervised write splices text into the middle of a sentence
  A concurrent session did exactly that to `QAa4` today: a `### 2 · The source` block landed inside the `## Question` sentence and cut it in half. That was one agent writing one page. Digest by definition writes many pages at once, so it reproduces that damage at scale unless the write is anchored to a section boundary rather than a byte offset.

### 10 · What routing and digest may write, taken from rules that already exist
Neither verb needs a new permission model. Two rules already on the books decide it.
- the tick is off limits, because the rule is that nothing untested gets ticked
  A verb reading a transcript can report what the transcript CLAIMS; it cannot verify that the claim is true. So it may write `## Log` lines and `## Where we are` prose, and it may PROPOSE a tick, and it may not close a checkbox or flip `state:`.
- across boards it is bound by `QB1` §4 the same as every other script here
  Mechanical writes carry no judgement and are always allowed; editorial writes are never ours on a board that is neither the skill set nor the board being worked. Digest walks a whole session, so it will meet other people's boards on nearly every run, and there its output is a report to that owner, not an edit.
- that also settles skill versus agent for digest
  It has to re-read a session it was not in. That is the same reason the cold read is done by a fresh agent: a reader who was present cannot see what went unsaid. So digest is a skill whose execution belongs in a fresh context, which is what the `task` and `discovery` families already do with their creator and orchestrator agents.

### 11 · The reviewer agent's own status is now unresolved
JL said "don't need to have the review agent, stop it" on 260729. That was said while one dispatch was running, so it may mean this run only, or the unit.
If it means the unit, three written things go stale at once: `SKILL.md` writing rule 3 (which names the agent as the cold read instrument) and its `ref/` index line, `QA9`'s acceptance half (the agent is the fresh context runner that pairs with `check.py`), and the `Q-Skill-haipipe-board-reviewer-agent` roster row. Nothing has been changed on that reading yet.

### 12 · The 260730 roster: one orchestrator, three layers, and two verbs
`haipipe-board` remains the public orchestrator.
It does not need to load every detailed contract on every turn; it invokes the smallest subskill that owns the current transition.

- `haipipe-board-index`, the Board and Group layer
  Its first action is interactive: propose Spine, Close, Groups, Pages, their relationships, and the linked SkillSet; show one reviewable structure; write nothing until the user confirms.
  After confirmation it materializes the Board-Webpage-Index, the Board-Webpage-Group views, and the Board relationship canvas shown at the top.
  The canvas is not decoration: it is the accepted relationship model and must update when a Group, Page, or dependency changes.
- `haipipe-board-page`, the Page layer
  It owns the common Page frame, page kinds, section/subsection contracts, Items to Finish, Where we are, paths, and closure semantics.
  Use the singular name because it defines the contract for any one Page; `pages` would sound like a batch operation.
- `haipipe-board-sentence`, the atomic layer
  It owns sentence identity and the records attached to a sentence: Evidence Card, local Comment, Edit, Chat focus, and lifecycle.
  Evidence Card stays a capability of this skill for now because it has no independent entry point: the user reaches it by selecting a sentence.
- `haipipe-board-routing`, the unit verb
  For each incoming user turn, resolve Board → Group → Page → Section, display the proposed attachment when confidence is not decisive, and never silently create a Page.
  Once attached, load the Page or Sentence contract needed for one anchored write.
- `haipipe-board-digest`, the batch verb
  Reconcile a recent conversation or work session by calling routing repeatedly, producing many proposed or permitted Board updates without inventing a second routing policy.

The layers and verbs are deliberately different.
Index, Page, and Sentence are contracts that other skills can consume; Routing and Digest are actions that consume those contracts.
This is the progressive-disclosure shape: opening a Board loads Index, an ordinary turn loads Routing, a Page edit loads Page, and sentence apparatus loads Sentence.

### 13 · Show which skill supports each Board part
The Board-level SkillSet declares the linked units once, while each owning Page or subsection may point to the exact capability that supports it.
The mapping is a support record, not a new skill per UI component:

```text
Board structure + top canvas        -> haipipe-board-index
incoming user question              -> haipipe-board-routing
Opening / Content / Items / Status  -> haipipe-board-page
Evidence Card / Comment / Edit      -> haipipe-board-sentence
recent conversation reconciliation -> haipipe-board-digest
```

For example, `QAb1 · Evidence Card` should show `supported by haipipe-board-sentence · Evidence Card`.
If Evidence Card later gains an independent trigger such as “collect, verify, and reconcile evidence across many pages”, it earns a separate `haipipe-board-evidence` skill then.
Until that consumer exists, splitting it would add a door without adding a workflow.

`QB6` owns how these linked skills are declared and synchronized.
`QAa5` owns the visible `🧩 Skills` support record on a Page.
`QA2` owns the proposal reviewed before the Index writes the structure, while `QA2b` and `QAa2` own the rendered top view and relationship canvas.

## Items to Finish
### The survey behind the roster
- [x] 🗺 The candidate roster is surveyed, with the test applied to each seam
      260729: every seam in `skills/board/` was walked. Stage argues for a clean script and already ships as a door under `paper/`, live and canvas are runtime, the checker and status and regroup are verbs of the manual.
- [x] 🔢 What the family ships today is counted, not estimated
      260729: two units, `haipipe-board` v0.46.0 and `haipipe-board-reviewer-agent` v1.0.0, against 144 skills and 9 agents in the plugin. The form also ships from two places outside this family, `haipipe-paper-stage` and the two `serve.py` rule strings.

### Rulings awaiting JL
- [ ] 🧠 JL rules how `haipipe-writing` joins the roster (260801, named 260802)
      JL, after an evening of rewriting QB4 sentence by sentence: "I think we need to add it to the skills to make this work. Maybe we want to have haipipe-write, for this specific purpose."
      The candidate is a WRITING verb, not another spec: take a division of authored prose and rewrite it so a reader whose English is weak can follow it, then record every edit as a word-level `✎ ~before~ *after* · WHO · YYMMDD HHMM` line under the sentence it changed.
      It has a distinct consumer, which is §7's test: any page on any board with prose that reads like an AI wrote it, not just a Board page, and not only at authoring time.
      What it would carry is already settled and written down on QB4: the weak-English readability axis in `### 9`, the plain-heading and short-sentence rules in `## Writing Style`, the ✅/❌ example-pair shape, and the `✎` change grammar `src/body.py` already renders.
      Doing it by hand is what proved it is a skill: the same three mistakes recurred all evening, and each one is mechanical enough to be a rule the skill enforces rather than a thing a person remembers. Records were appended at the end of a block and silently attached to the wrong sentence; the diff was written whole-sentence, which shows nothing; and a heading named its mechanism instead of its consequence.
      THE DESIGN QUESTION IT MUST ANSWER FIRST: how does a change record attach when ONE sentence becomes SIX?
      The `✎` grammar assumes one record belongs to one sentence, and the main move in this kind of rewrite is splitting a long sentence into several short ones, so the sentence a record describes no longer exists as one thing.
      Doing it by hand produced the same misplacement twice on 260801, because the record has no natural home: appended after the rewritten block it silently attaches to the LAST new sentence, which is the one it says nothing about.
      A · anchor on the FIRST new sentence and diff against the whole block. This is what 260801 settled for, and it reads well, but the other five sentences carry no history and their `C.P.S` addresses have nothing attached.
      B · one record on EVERY resulting sentence, each pointing back to the same source sentence. Complete, and noisy: six badges where one edit happened.
      C · a block-level record that sits above the run rather than under a sentence. Honest about what actually changed, and it needs a render that does not exist yet, since the apparatus only ever hangs under a paragraph.
      → CC recommends A now and C later, because A works with today's renderer and C is the only one that describes a split truthfully.
      Open questions for JL: whether `haipipe-writing` stays its own unit or becomes a verb inside an existing one, whether it may write prose directly or must propose diffs for approval, and whether it belongs to this family at all given that its consumer is any prose, not any board.
- [ ] 🧠 JL rules the roster: one orchestrator plus five subskills, and their shipping order
- [ ] 🧠 JL says whether "don't need to have the review agent" retired the unit or only that run (§11)

### Contracts for the units that ship
- [ ] 🗂 Define `haipipe-board-index` against one realistic opening conversation
      The input is a raw topic; the output is one reviewable proposal containing Spine, Close, Groups, Pages, relationships, SkillSet, and the top-canvas sketch. No files are written before approval.
- [ ] 🧩 Settle the support-record syntax
      Decide how a Page or subsection says `supported by haipipe-board-sentence · Evidence Card` without duplicating the Board-level SkillSet.
- [ ] 📐 For each unit that ships: what it owns, what stays in `ref/`, and which Law graduates into it

### Routing and digest before they are built
- [ ] ⚖️ Routing and digest get a write protocol before either is built
      What may be written (Log and Where we are), what may only be proposed (ticks, `state:`), and how a write anchors to a section so it cannot splice a sentence. §9 and §10 hold the draft.
- [ ] 🔗 The page resolution routing depends on is stated
      An id no longer predicts a folder, so the resolver reads `board.md` `## Pages`. This has to be true of `check.py` too before routing leans on it.

### The serve.py de-duplication
- [ ] 🧹 `serve.py`'s two rule strings stop being copies
      `CHAT_RULES` and `BOARD_CHAT_RULES` read `ref/` instead of restating it. This is worth doing whether or not the page door ships.

## Where we are
- 260731 JL · 🤖 The agents became a pair, and the roster gained its first parallel unit
  JL: "we should have a new agent named haipipe-board-creator-agent, it can be called to write the pages markdown in parallels, instead of haipipe-board to write each of them one by one".
  `Agent-2` is the producer half of the creator and reviewer pair `Agent-1` started, which is the same split the task and discovery families in this toolkit already run.
  It is the first unit in this family whose contract is about CONCURRENCY rather than about content, so its boundary is drawn by a different test than §7's: not "does it have its own trigger and version", but "does it touch a file another writer also touches".
  One page's `.md` fails that test and fans out; `board.md`, the lane block, the rebuild, and the checker pass it and stay with the caller, which is why the agent has no Bash tool.
  Unshipped, and the reason this row is not a completion: the CALLER's half does not exist, so `haipipe-board`'s `open` and `add` still write pages one by one and nothing turns an approved proposal table into N assignment packets.

- 260731 JL · 🚪 The roster shipped its specs and its first verb
  JL ordered the creation directly ("make the haipipe-board thinner, and have other skills, like haipipe-board-page, haipipe-board-sentences, haipipe-board-routing, please creating them now").
  §8's shape is now real on disk: `haipipe-board-page` and `haipipe-board-sentence` as contract-first SPECS citing `ref/` as their authority, `haipipe-board-routing` as the unit VERB carrying §9's anchored-write rule and §10's tick and cross-board laws.
  All three are registered: Skill-3, Skill-4, Skill-5 on this board, the family block in haipipe-board's SKILL.md (0.55.0), and the family README.
  Still unshipped: `haipipe-board-digest` (the fan-out verb), and the serve.py de-duplication that makes CHAT_RULES a consumer of the specs, which was the extraction's original trigger.
The family now has one orchestrator plus five proposed subskills: Index, Page, Sentence, Routing, and Digest.
The first Board action is proposed as an Index-owned conversation that produces a user-approved structure and top relationship canvas.
Evidence Card remains a Sentence capability, while the Board/Page support record makes that dependency visible.
Nothing is built and the expanded roster is not yet ruled.
CC's first reading on 260729 was defer page and sentence, on the grounds that no consumer needed them with no board open. JL's routing and digest are that consumer, so the reading is withdrawn and §7 records why it was wrong.

### Decision Now
- [ ] 🧠 Tick the roster ruling
      PROPOSED: the Items row "JL rules the roster" is answered by conduct, since JL ordered index on 260730 and page, sentence, routing on 260731; digest stays named and unshipped. Confirm and the row ticks.
- [ ] 🤖 Close §11 on the reviewer agent
      PROPOSED: the 260731 Agent-1 ruling keeps the unit (a skill is loaded, an agent is dispatched), so "stop it" on 260729 meant that run only. Confirm and the §11 row ticks.
- [ ] 🧭 Rule where a group-altitude input lands
      Routing 0.1.0 resolves only pages, so a finding about a whole group (the QB status readout, 260731) has no landing rule. Recommended: the group's intro prose in `board.md` `## Pages`, written at the section boundary; the alternative is decomposing every group finding onto member pages.
- [ ] 🚪 Rule where routing's own design questions live
      Recommended: this face stays the owner until digest is built; the alternative is opening a routing Q page in QC now.

## Files
### Where the form ships from today
- `ref/page-template.md` · `ref/board-form.md`
  Where the contracts ship today.
- `serve.py`
  Lines 297 and 357, the two hand rolled copies of the page and board rules.

### The standing rules this fork tests
- `QB1-skillmd.md`
  The specs-to-ref Law this fork tests.
- `QA1-form.md`
  §4, the standing rule that decides what routing and digest may write on a board that is not ours.

## Log
260802 0000 · The candidate gained the design question it has to answer before it can ship: how a change record attaches when one sentence becomes six. The `✎` grammar assumes one record per sentence, splitting is the main move in this kind of rewrite, and the same misplacement happened twice by hand on 260801 because a record appended after a rewritten block silently attaches to the last new sentence rather than the one it describes. Three options recorded with a recommendation
260801 2340 · `haipipe-write` added to the roster as a candidate awaiting JL's ruling, after an evening spent hand-rewriting QB4's `### 1` for a weak English reader and recording each edit in the `✎` lane. The case for it is that the same three mistakes recurred all evening and every one is mechanical: a record appended at the end of a block attaches to the wrong sentence, a whole-sentence diff shows nothing, and a heading that names its mechanism reads as jargon. What it would enforce is already written on QB4 and needs no new contract
260801 0130 · Reindexed QC6 -> QC1b under the new QC1 skill-family parent; QC1b-vs-Skill-* overlap flagged on QC1 (JL 260801)
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260731 · Decision Now adopted (JL: proposals leave chat and land under the owning page's Where we are); first rows here carry the two pending roster ticks, routing's group-altitude gap, and the home of routing's design questions
260731 · Agent-2, the page creator, joined as the producer half of the pair; the family's first unit scoped by concurrency rather than by content, and the caller's fan-out half is still owed
260731 · The reviewer separated from the skills as Agent-1, its own page kind below the Skill rows; a skill is loaded, an agent is dispatched
260731 · haipipe-board-page, haipipe-board-sentence, haipipe-board-routing created contract-first and registered (Skill-3/4/5, SKILL.md family block, family README); digest and the serve.py de-dup remain
260730 · Added haipipe-board-index and the three-layer model: Index proposes and materializes the approved Board structure and top canvas; Page owns sections; Sentence owns Evidence Card and other sentence records; Routing and Digest consume those contracts
260729 · JL's base/variant model (recorded on QAa0) flips §6's reading: haipipe-paper-stage is the first Content variant door rather than a leak, and haipipe-board-page would ship the base contract the variants extend
260729 · Opened from JL's two same-day asks (haipipe-board-page, haipipe-board-sentence); CC's recommendation was defer until the QAa and QAb groups settle
260729 · Counted the family (2 units) and found the form shipping from two places outside it: `haipipe-paper-stage` under `paper/`, and `CHAT_RULES` plus `BOARD_CHAT_RULES` inside `serve.py`
260729 · JL named `haipipe-board-routing` and `haipipe-board-digest`; they are the consumer the page and sentence doors were missing, so the defer recommendation is withdrawn and the roster becomes one door, two specs, two verbs
