# Sub-skills: what else this family ships
state: 🟡 PARTIAL · roster proposed, not ruled
owner: JL
method: name every candidate and apply one test to each, then let JL rule the set; a shipped skill follows settled decisions, never precedes them

## Question
What does `skills/board/` ship besides `haipipe-board`, and which of those are their own doors rather than sections of the manual?
JL opened the fork on 260729 with `haipipe-board-page` and `haipipe-board-sentence`, then the same day named two more, `haipipe-board-routing` and `haipipe-board-digest`. Four proposals in one day is why the fork gets a face instead of a chat answer.

## Boundary
- ✅ Covered here
  The shipping decision: which units exist, what each owns, and what the split costs.
- ↪ Covered elsewhere
  What the page contract IS: the `QAa` group. What the sentence contract IS: the `QAb` group.
  What SKILL.md must say, and the rule that specs go to `ref/`: `QB1`.
  Where a write is allowed to land on somebody else's board: `QA1` §4.

## Content
### 1 · The case for staying one skill
The contracts already ship: `ref/q-template.md` + `ref/board-form.md` carry the page, and the sentence grammar rides `ref/board-form.md` and `src/body.py`.
`QB1`'s Law keeps SKILL.md shortest with specs in `ref/`, and nothing today needs to LOAD page-only or sentence-only rules without the whole board skill.
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
That is a board-folder decision (`QA1`'s two locations), not a skill decision, and it needs nothing shipped.

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
  Today's board has QA2, QA6, QC2, QC3 and QC4 living under group letters they were not opened under, precisely so external citations keep working. An id no longer predicts a folder, so routing cannot resolve a page by name pattern; it has to read `board.md`'s `## Pages`.
- an unsupervised write splices text into the middle of a sentence
  A concurrent session did exactly that to `QAa4` today: a `### 2 · The source` block landed inside the `## Question` sentence and cut it in half. That was one agent writing one page. Digest by definition writes many pages at once, so it reproduces that damage at scale unless the write is anchored to a section boundary rather than a byte offset.

### 10 · What routing and digest may write, taken from rules that already exist
Neither verb needs a new permission model. Two rules already on the books decide it.
- the tick is off limits, because the rule is that nothing untested gets ticked
  A verb reading a transcript can report what the transcript CLAIMS; it cannot verify that the claim is true. So it may write `## Log` lines and `## Where we are` prose, and it may PROPOSE a tick, and it may not close a checkbox or flip `state:`.
- across boards it is bound by `QA1` §4 the same as every other script here
  Mechanical writes carry no judgement and are always allowed; editorial writes are never ours on a board that is neither the skill set nor the board being worked. Digest walks a whole session, so it will meet other people's boards on nearly every run, and there its output is a report to that owner, not an edit.
- that also settles skill versus agent for digest
  It has to re-read a session it was not in. That is the same reason the cold read is done by a fresh agent: a reader who was present cannot see what went unsaid. So digest is a skill whose execution belongs in a fresh context, which is what the `task` and `discovery` families already do with their creator and orchestrator agents.

### 11 · The reviewer agent's own status is now unresolved
JL said "don't need to have the review agent, stop it" on 260729. That was said while one dispatch was running, so it may mean this run only, or the unit.
If it means the unit, three written things go stale at once: `SKILL.md` writing rule 3 (which names the agent as the cold read instrument) and its `ref/` index line, `QA9`'s acceptance half (the agent is the fresh context runner that pairs with `check.py`), and the `Q-Skill-haipipe-board-reviewer-agent` roster row. Nothing has been changed on that reading yet.

## Items to Finish
- [x] 🗺 The candidate roster is surveyed, with the test applied to each seam
      260729: every seam in `skills/board/` was walked. Stage argues for a clean script and already ships as a door under `paper/`, live and canvas are runtime, the checker and status and regroup are verbs of the manual.
- [x] 🔢 What the family ships today is counted, not estimated
      260729: two units, `haipipe-board` v0.46.0 and `haipipe-board-reviewer-agent` v1.0.0, against 144 skills and 9 agents in the plugin. The form also ships from two places outside this family, `haipipe-paper-stage` and the two `serve.py` rule strings.
- [ ] 🧠 JL rules the roster: which of the five units ship, and in what order
- [ ] 📐 For each unit that ships: what it owns, what stays in `ref/`, and which Law graduates into it
- [ ] ⚖️ Routing and digest get a write protocol before either is built
      What may be written (Log and Where we are), what may only be proposed (ticks, `state:`), and how a write anchors to a section so it cannot splice a sentence. §9 and §10 hold the draft.
- [ ] 🔗 The page resolution routing depends on is stated
      An id no longer predicts a folder, so the resolver reads `board.md` `## Pages`. This has to be true of `check.py` too before routing leans on it.
- [ ] 🧹 `serve.py`'s two rule strings stop being copies
      `CHAT_RULES` and `BOARD_CHAT_RULES` read `ref/` instead of restating it. This is worth doing whether or not the page door ships.
- [ ] 🧠 JL says whether "don't need to have the review agent" retired the unit or only that run (§11)

## Where we are
The count is settled and the roster is on the table: five units, one door plus two specs plus two verbs, with the test and the write protocol drafted in §7 through §10. Nothing is built and nothing is ruled.
CC's first reading on 260729 was defer page and sentence, on the grounds that no consumer needed them with no board open. JL's routing and digest are that consumer, so the reading is withdrawn and §7 records why it was wrong.

## Files
- `ref/q-template.md` · `ref/board-form.md`
  Where the contracts ship today.
- `QB1-skillmd.md`
  The specs-to-ref Law this fork tests.
- `QA1-form.md`
  §4, the standing rule that decides what routing and digest may write on a board that is not ours.
- `serve.py`
  Lines 297 and 357, the two hand rolled copies of the page and board rules.

## Log
260729 · JL's base/variant model (recorded on QAa0) flips §6's reading: haipipe-paper-stage is the first Content variant door rather than a leak, and haipipe-board-page would ship the base contract the variants extend
260729 · Opened from JL's two same-day asks (haipipe-board-page, haipipe-board-sentence); CC's recommendation was defer until the QAa and QAb groups settle
260729 · Counted the family (2 units) and found the form shipping from two places outside it: `haipipe-paper-stage` under `paper/`, and `CHAT_RULES` plus `BOARD_CHAT_RULES` inside `serve.py`
260729 · JL named `haipipe-board-routing` and `haipipe-board-digest`; they are the consumer the page and sentence doors were missing, so the defer recommendation is withdrawn and the roster becomes one door, two specs, two verbs
