---
name: haipipe-page-workflow
description: >-
  The RUN router of the page family: combines OUTLINE, DRAFT, PROBE, EVIDENCE,
  REVISE, COMPILE and CHECK into one bounded, auditable, non-linear loop over
  ONE Board Page, owning the phase receipt and stop rules. RUN is not ADVANCE;
  only CHECK may CLOSE. Trigger: run a page, run page lifecycle, automatic
  page loop, page run receipt, /haipipe-page-workflow.
metadata:
  version: "0.21.0"
  last_updated: "2026-08-21"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-workflow · the phases, combined into one auditable RUN

`haipipe-page` is the door for ONE PAGE and says what a page IS.
This skill is the head of the page WORKFLOW: it drives one existing Page through the phases as a bounded loop and leaves a receipt.
It moved here from `haipipe-page`'s RUN verb on 260815, so the workflow pattern reads the same in every family: one folder, one head skill, its member skills beside it.

**Who owns what**:

```
haipipe-page               what a page IS · CREATE · WORK ON
haipipe-page-workflow      RUN · the packet · the receipt · the stop rules
page-workflows/ members    each phase's own authority
haipipe-board              the machinery this skill calls, never contains
```

## 🤖 ONE agent per display unit, and the skill chain it walks (260819)

JL 260819: "each display you can have a subagent to call the specific skills to
work on it, right?" Yes, and the fan-out unit is the UNIT, not the page:

```text
  one 🖼 bullet  ─▶  one display unit  ─▶  one agent instance
```

Four units on `QPw00-page-loop` went stale the moment the loop's phase order
changed, and four agents rebuilt them in parallel. Each one owns exactly one
folder and may not touch the page's prose or a sibling unit.

**The chain each agent walks, three layers:**

```text
  ① the agent      display/agents/haipipe-display-unit-agent
                   resolves the intake, writes recipe/ · assets/ · README.md
  ② the one door   haipipe-display
                   reads README's `kind:` row and routes
  ③ the renderer   📊 table  → haipipe-display-table
                   📈 figure → haipipe-display-figure
                   📐 diagram→ haipipe-display-diagram
                   ✒️ tex    → haipipe-display-tex
                   🎨 illust → haipipe-display-illustration
```

**Why the fan-out is safe.** Each unit is a separate folder with its own intake,
recipe and README, so two agents cannot collide. The dispatching phase keeps the
two things an agent may NOT do: it never ticks `accepted:`, which is a person's at
⑦ CHECK, and it never edits the sentence that cites the unit, which is ⑤ REVISE's.

**What every such dispatch must carry**, because a display agent in a fresh
context knows none of it:

```text
  the unit's absolute path        it owns one folder and nothing else
  WHY it is stale                 which frozen input changed, from checks/intake.py
  what changed, as facts          plus the files that are the AUTHORITY, so the
                                  agent verifies rather than trusting the prompt
  the rebuild commands            the unit's own, from its README
  the verification to run         checks/intake.py must stop reporting it
```

⚠️ **"An input moved" is not "the figure is wrong."** One of the four was told to
DECIDE first and redraw only if a specific line had become false. A re-freeze is
not a redraw, and a figure rebuilt for no reason loses its own history.

## 👷 One producer agent per phase (260819)

Ruled by JL an hour after §🧭: "for the creator-agent, it should have the
outline-agent, etc." The display precedent generalizes to the whole loop:

```text
  phase        agent (skills/board/page-workflows/agents/)     fan-out?
  ─────────────────────────────────────────────────────────────────────────
  ① OUTLINE    haipipe-page-outline-agent                      no — merge point
  ② PROBE      haipipe-page-probe-agent                        per card, serial
  ③ EVIDENCE   haipipe-page-evidence-agent                     🖼 lane fans out:
                                                               one haipipe-display-
                                                               unit-agent per unit
  ④ DRAFT      haipipe-page-draft-agent                        no
  ⑤ REVISE     haipipe-page-revise-agent (⑥ COMPILE folded)    no
  ⑦ CHECK      haipipe-page-check-agent                        no — one version,
                                                               one cold judge
  verbs/base   haipipe-page-creator-agent keeps create-page and
               revise-opening and is the producers' BASE;
               haipipe-board-reviewer-agent keeps whole-BOARD
               reviews and is the ⑦ judge's BASE
```

**The thin-wrapper law, and it is what makes six files safe:** a phase agent
carries identity, its skill chain, role walls and the receipt duty, and
restates NOTHING a contract holds. A restated route table or tick rule is a
mirror, and on 260819 every mirror on this board — phase-cards numbers, the
route code, four of five figures — drifted within a day of the loop changing.
The packet, procedure, house rules and return contract live once, in
`ref/producer-contract.md` (carved out of the creator agent later the same
day, so no agent reads another agent's file).

## 🧭 ONE OUTLINE pass per PREPARE round, and it is the merge point (260819)

Ruled by JL the same day as the display fan-out: "do we need to have the outline
agent as well? to update the outline with the new evidence available?"

When this was ruled the pass ran on the shared producer base; an hour later
§👷 gave every phase its own agent, so the pass is now `haipipe-page-outline-agent`'s.
What this section adds is WHEN it is sent back in:

```text
  PREPARE round n
  ① OUTLINE     ONE outline-agent pass per round: fold every returned answer,
                README claim and contradiction report into the plan, re-run
                the four checks, leave a receipt
  🧑 LOOK       the pass ends at HOLD with the plan rendered: the human looks
                at the OUTLINE before anything else runs (JL 260819: "the
                first check should be the outline check … it is good to have
                the human to have a look at outline and then do the probes
                and evidences"). His rulings are evidence the next ① pass
                folds in; his go-word — or a ruling that changes nothing
                structural — releases ② and ③. The `approved:` tick stays
                the round's formal close; this look is earlier and lighter.
  ② PROBE       raise what the folded plan still owes
  ③ EVIDENCE    fan OUT: one haipipe-display-unit-agent per 🖼 unit, the
                citation and value lanes beside it, all in parallel
  returns land ──▶ the next ① pass opens round n+1
  until the four checks pass AND no return changed the plan
```

Why the two lanes differ in shape: display units are independent of one another,
so ③ fans out; the plan is ONE file that every return converges on, so ① cannot
fan out and runs exactly once per round. An outline edit made in the dispatching
session's own thread violates this section twice: it leaves no receipt, and an
in-thread edit is contaminated by the discussion that caused it, which is the
repo's own fresh-subagent rule applied to the plan.

## 🧑 Where a RUN stops for a person (260819)

```text
  ┌ ① OUTLINE ⇄ ② PROBE ⇄ ③ EVIDENCE ┐   🧑 ATTENDED
  └──────────────┬────────────────────┘
                 ▼  ④ DRAFT → ⑤ REVISE (⑥ COMPILE)   🤖 UNATTENDED
                 ▼  ⑦ CHECK                          🧑 judges
```

JL 260819: "we will mainly check the outline and the evidences if we want. But if
not, you can just go ahead for the draft and revise and the compile." The PREPARE
loop decides what is true; ④ onward is execution against a plan already agreed. A
controller that halts between DRAFT and CHECK for a human is halting in the wrong
place.

**"if we want" is a MODE, and since 260821 the packet carries it.** `mode:
copilot | auto` — one rule set, two readings, never two rule sets:

```text
  🧑 copilot   the human half BLOCKS       a person is here; wait for them
  🤖 auto      the human half DEFERS       the loop moves on the machine half
                                           (`checked:`) and the debt lands on
                                           the ledger, `--owed`, once at the end
```

**Auto defers FOUR ticks and HARDENS the fifth.** `approved:` `verified` `read:`
`accepted:` each have a rules file, so an approver can establish everything around
them. The Page Type's RULING has none, on purpose, so auto forces
`human_gate.required` TRUE whatever the packet said — a run nobody watched is
exactly the run that must not certify itself. Its terminal HOLD is therefore the
DESIGN: end to end, everything mechanical passing, stopped at ONE gate instead of
five. `ref/page-run-contract.md` §🔀 has the field and the audit invariant behind
the write-back.

Every step reports its `phase:` to whoever is watching, not only into the receipt:
work that does not name its phase cannot be routed or audited.

**The phase strip mechanizes that duty** (JL 260820: "I want to have a status
strip to show what phases we are in"). One command, one row per phase, derived
from DISK plus the newest receipt, never from what a page says about itself:

```bash
python3 <haipipe-board>/cli/pagephase.py <page-dir>        # --md to paste on a page
python3 <haipipe-board>/cli/pagephase.py <page-dir> --owed # the LEDGER, see §✋
```

```text
✅ ① OUTLINE   v1 approved · marks 📮25 🧮2 📚6 🖼6
✅ ② PROBE     14 cards raised · every outline PP id has a card
⏳ ③ EVIDENCE  🧮 13/14 answered (1 blocked) · 📚 0/7 verified · 🖼 3/5 drawn
⏳ ④ DRAFT     8 content divisions · page predates outline tick
⏳ ⑤ REVISE·⑥  latex/ present · pdf STALE/none
⬜ ⑦ CHECK     last receipt: OUTLINE → HOLD (round 1)
→ now: ③ EVIDENCE · ✋ human ticks still owed: 25
```

**✋ is a COUNT; `--owed` is the LEDGER, and that is the copilot/auto join.**
A count says there is a debt. It never says where to spend the one act that is a
person's, which is why `QPw00g-human-gate` carries "no surface joins the five
ticks" as an open ruling. `--owed` is that join: one row per owed tick, each
carrying the approver's `checked:` beside the question only a person can answer.

```text
 1. 🧑 approved  outline/QB3-diet-outline-v3.md
      v3
      🤖 not checked yet · approve-rules.md has never run here
      ❓ is this the DIRECTION I want, and is this round worth doing now?
```

One artifact, two readings, and this is what makes the two modes ONE mechanism
rather than two rule sets that drift:

```text
  🧑 copilot   you watch the list shrink and answer as you go
  🤖 auto      the run does not stop; the list is what you are handed at the end
```

⚠️ **The count was short by one until 260821.** `ticks_owed` carried four ticks
and phase-cards.md has always listed FIVE — the Page Type's RULING was never
counted, so every ✋ on every unclosed page under-reported. `sum(ticks_owed)` now
equals `len(owed_ledger())`, and `tests/test_page_phase_ledger.py` asserts it,
because a count and a list that disagree are how a person stops trusting both.

⚠️ The `→ now` row is the first phase whose exit test FAILS, in loop order: a
REPORT, never a routing. Which phase runs next stays with the authority test
(§🔤), and ⑦ CHECK may still route anywhere. Sit it beside its two siblings:
`status.py` answers "where is this SESSION", `pagestatus.py` "where is every
page in this GROUP", `pagephase.py` "which PHASE is this PAGE in".

**And the strip rides in the closing block** (JL 260820: "how to update this so
I know which phase of the page I am in?"). A page-focused `status.py` prints
the same state as a fourth row, so every reply about a page says where the page
is without anyone running a second command:

```text
⏱️ 📮 PROBE · 🧭✅ 📮⏳ 🃏⬜ ✏️⬜ 🖊⬜ 🔍⬜ · ✋4
```

**What each phase COSTS is measured, not guessed**: `ref/measured-cost.md`
carries real agent returns from the 260820 QC1 and QC2 runs, minutes and tokens
and tool calls per phase (JL 260820: "could you document for each of them, how
long it takes for us?"). The short version: wall-clock tracks TOOL CALLS at
about 14 seconds each, EVIDENCE is the longest phase because it opens the most
files, a display unit runs 5 to 17 minutes, and fanning the display lane out is
the one real speedup in the loop.

The bar reuses §🔁's own phase emoji (🧭 📮 🃏 ✏️ 🖊), so the strip and the
loop diagram teach one symbol set rather than two. ⑦ CHECK is the single
substitution: §🔁 draws it ✅, which is also the strip's DONE marker, so it
carries 🔍 in the bar and only there. Circled digits were the first attempt and
JL could not read them at terminal size (260820).

Both forms read `haipipe-board/src/page_phase.py`. One computation, two
surfaces: a second copy of the phase rules would go stale the first time this
loop changed, which is exactly the §🪞 failure this family already records.

## 🔁 The shape of the loop

**The routing grammar**: authority-selected, never a conveyor belt.

```
┌─ PREPARE · ① ⇄ ② ⇄ ③ until the plan and its evidence agree ─┐
│                                                              │
│  🧭 ① OUTLINE ─▶ 🧑 LOOK ─▶ 📮 ② PROBE ─▶ 🃏 ③ EVIDENCE     │
│     🚧gate ▲                                  ⚖️count │      │
│            └────── the answer changes the plan ───────┘      │
└──────────────────────────┬───────────────────────────────────┘
                           ▼
  ✏️ ④ DRAFT ─▶ 🖊 ⑤ REVISE (📄 ⑥ COMPILE folded) ─▶ ✅ ⑦ CHECK ─▶ CLOSE
      ▲                   ▲                              │
      └───────────────────┴─ CHECK routes back anywhere ─┘

  ① the shape: 🧭 tab; a 🧑 LOOK ends every pass, a person ticks `approved:`
  ② ask the bank: each 📮 mark becomes a card, Q → QA file
  ③ land the cards: 📚 🧮 🖼 lanes in parallel; 🖼 runs intake→render→pick→build
  ④ write it: real numbers from landed evidence, a hole is the exception
  ⑤ prose + captions, cite each card and unit by id; rebuild latex · pdf · word
  ⑦ judge the BUILT artifact; only CHECK may CLOSE
```

## 🔤 Four words, and none substitutes for another

```text
word         answers                    in one receipt        repeats?
──────────────────────────────────────────────────────────────────────
🌀 WORKFLOW  which LOOP is this?        the run itself        no
⏱️ PHASE     which AUTHORITY acts?      `phase:`              YES
🧮 STEP      WHERE in this run?         `step:`               never
🔁 ROUND     which PROMISE era?         `round:`              on reopen
```

⚠️ **PHASE may not be renamed to STEP** (JL weighed it and ruled against it, 260818).
`step` is already a field meaning the monotonic position, so one receipt would carry
two meanings on one key. A phase is a TYPE and a step is an INSTANCE of one: in
`260805-0216-QB8e` the single CHECK phase occupies steps 1, 3 and 5. The word must
permit repetition, which is the same reason RUN is not ADVANCE. `QPw00 §11` argues it.

Each phase may repeat, PROBE is skipped when the Page promises no claim it cannot already support, and CHECK may route back to any earlier phase.
Which phase runs next is decided by AUTHORITY (`haipipe-page`'s authority test), not by position, which is why the verb is RUN and not ADVANCE.

**Seven members** (JL 260817, splitting the four; the three merges are named below):

```
phase       authority                                          load
────────────────────────────────────────────────────────────────────────────────
OUTLINE 🚧  writes <page>/outline/<stem>-outline-v<N>.md, the    ../haipipe-page-outline
            plan down to the POINT and its obligations, each     (the file's shape is
            bullet marked
            🎯aim 📮ask 🧮value 📚cite 🖼display ·        haipipe-plugin-outline §📐)
            exits ONLY on a person ticking `approved:`
 DRAFT       define purpose + Aims; instantiate each Point as   ../haipipe-page-draft
            one or more sentence scaffolds with visible holes
 PROBE       MATCH Task/Discovery before new work; turn each     ../haipipe-page-probe
            source-typed 📮 mark into probe/PP<NN>-<slug>/, write its
            `serves:` backlink, dispatch the stripped question
 EVIDENCE ⚖️ land answer/proof, citation, and the Display        ../haipipe-page-evidence
            units (intake, render, pick, build); expose the
            derived Evidence Bundle
 REVISE      realize the scaffolds as final prose, cite landed   ../haipipe-page-revise
            cards and drawn units by id, write their captions
 COMPILE     rebuild latex · pdf · word from that prose          ../haipipe-page-revise
                                                                 (until split out)
CHECK       judge the BUILT version and route its authority     ../haipipe-page-check
```

**Why each split, and every one is a real 260817 failure, not a theory:**

```
was            became             the failure it allowed
──────────────────────────────────────────────────────────────────────────────
DRAFT          OUTLINE + DRAFT    one phase agreed the shape AND wrote the page,
                                  so the outline table got pasted into ## Content
EVIDENCE       PROBE + EVIDENCE   raising a card and landing it counted as one
                                  act, so four cards sat `raised`, bound to a
                                  QA bank that did not exist, and it read as done
REVISE         REVISE + COMPILE   "the prose is right" was reported as done while
                                  the PDF carried raw <!-- --> and literal **
```

## 🪪 Each phase in SIX fields · `ref/phase-cards.md`

JL asked the question this section exists for (260818 1402): "if I want to work
with the page workflow's each phase, what should each phase do". Every phase
contract already answered it, and no two answered in the same fields.

```text
contract                  the fields it used
──────────────────────────────────────────────────────────────────────
haipipe-page-outline      owns · may do · exits · may not
haipipe-page-probe        owns · may do · exits · may not
haipipe-page-revise       a three-line same-promise test
haipipe-page-check        reads · writes · does not
haipipe-page-draft        owns · may do · exits
haipipe-page-evidence     a six-step loop, two phases wide
```

All six are correct and none of them can be read next to another, which is what
a person needs when choosing which phase to run. So `ref/phase-cards.md` states
every phase ONCE, in the same six fields, in loop order:

```text
❓ ASKS     the one question the phase answers
📥 READS    what must already exist, or the phase cannot start
📤 WRITES   the exact path it creates or changes
🚪 EXITS    a testable condition
✋ TICK     the person-reserved tick, or none
🔀 ROUTES   where it may go next
```

**The operational rule is the 🚪 EXITS row: you work a phase by satisfying it.**
Eight cards (③ splits into its three lanes, ⑥ folds into ⑤) carry five person
ticks between them, on four of the cards, so the other four run machine-only
from start to finish.

That file is a SUMMARY and this family is its source. When the two disagree, the
phase contract wins and the card is the defect.

## 🃏 One hole, five phases, and only ONE of them opens a file

The commonest question about this loop is where an evidence card is born, and
until 260817 three member skills answered it three different ways. One rule now,
and it reads down the loop:

```text
① OUTLINE   the MARK      `- B4 · the four coordinates    📮`   nothing on disk
② PROBE     the CARD      bank MATCH → probe/PP<NN>-<slug>/ · serves: C4.P1.B4
③ EVIDENCE  the ANSWER    target: <QA path> · proof/ pulled · bundle ready
④ DRAFT     the SENTENCE  writes the landed number into prose; a hole only
                          for a named blocker
⑤ REVISE    the REWRITE   improves that prose and cites the card by id
```

**Why the file waits until ②.** A plan is rejectable in ten seconds and must
leave nothing behind, so ① may not: the mark IS the proposal, and a card beside
it would be a second copy of it (§🪞 below). The deciding reason is the STAKE: a
card's `consumer/` side carries what the page loses, and that stake lives in the
approved plan. ② is the first phase where a complete card can exist.

**The display unit is the one exception, and it goes LATER, not earlier.** Its
`intake/` freezes FROM a `proof/` that does not exist until an answer does, so
③ EVIDENCE creates it. Declaring a unit that nothing can fill yet is how a page
shipped "1 display declared · 0 unit folders on disk" (260817).

**⚖️ EVIDENCE is three LANES, not three steps.** They run at once, each with its own hand and its own exit test; the phase ends when all three pass, and no lane waits on another. The result is a derived Evidence Bundle keyed by the Point, not a fourth storage plugin.

```
lane          hand        exit test
──────────────────────────────────────────────────────────────────────────────
📚 citation   a person    the bib key is landed AND a person marked it verified
🧮 value      the bank    binding names a real QA file AND probe/<id>/answer/
                          holds its extract  🚫 `answered` with an empty proof/
🖼 display    a person/   intake/ frozen from that answer/ AND the unit drawn
              machine     and previewable; intake, render, pick and build are
                          all this lane's (260819), only ⑦'s accept stays out
```

⚠️ **The display lane freezes inputs here AND realizes them here.** QPf5's five-step walk sits almost entirely in this phase since 260819: ① INTAKE, ② RENDER, ③ PICK and ④ BUILD are all EVIDENCE's, and only ⑤ ACCEPT is CHECK's. A plan carries only the bare `🖼 owed` mark until EVIDENCE has a Probe `proof/` from which to freeze intake.

## 🪞 The page never writes prose about what a plugin already holds

Every phase can fail the same way, and on 260817 one page failed it three times in one session (`QC1-visitlbp`, CMSRegBoard). The failure is writing a SENTENCE where a THING belongs.

```text
what got written into the page body        what already held it        what happened
────────────────────────────────────────────────────────────────────────────────────
the DRAFT outline table, pasted into       🧭 the outline plugin,      two copies, and the
`## Content`                                which derives it from       body copy goes stale
                                            the ### headings            the next edit
"Evidence owed: probe/PP03-…, state        🚪 the probe surface,       the sentence carries a
raised."                                    which renders the card      `state:` the card owns
                                            and its live state          and will contradict
"evidence owed: 🖼 display"                 🖼 the display surface      🚨 ZERO units existed.
                                                                        The sentence WAS the
                                                                        whole deliverable.
```

**The rule.** A plugin owns a kind of material and a surface that shows it. The page's prose CITES that material by id and never restates it. `Display1` in a sentence is a citation; "a display is owed here" is prose pretending to be work.

**The rule that catches the third row, and it is the one that matters.** A phase may not report done while it DECLARED an artifact it did not CREATE. Declaring is free; the receipt must record the count.

```text
  ✅ 4 cards declared · 4 card.md on disk
  🚨 1 display declared · 0 unit folders on disk   ← the phase is NOT done
```

`haipipe-page-check` already rules that a declared unit which never rendered is a CHECK finding. That rule never fired here because CHECK never ran: the work was called done at DRAFT. So the count moves EARLIER, into every phase's own receipt, and a phase whose declared-versus-created counts disagree stops rather than reports.

**And the third failure of the same session, for the receipt to catch too**: verify the artifact the READER opens, not the one you just wrote. That session checked the built HTML and shipped a PDF full of raw `<!--` comments and literal `**`; checked `build.py`'s exit and served a page four minutes stale; and guessed at a CSP instead of opening the screenshot that showed the tab rail working perfectly. Wire green is not UI green (JL, standing rule).

## 🔁 run one Page lifecycle

RUN is the automatic, bounded loop. Use it when the process itself must be
exercised and audited, rather than when one known edit is enough.

1. Read `ref/page-run-contract.md` and assemble its raw-material packet. Resolve
   the Page Type from the filename. For a new Page, CREATE and register it first
   (that verb stays with `haipipe-page`), then start at OUTLINE, phase ① since 260817. For an existing
   Page with no known next authority, start at CHECK. Before each phase dispatch,
   materialize that phase's Related Board Pages packet with
   `haipipe-board/cli/pagecontext.py`; an invalid row or missing scope is a
   named HOLD, never omitted context.
2. Invoke `haipipe-board/ref/page-lifecycle.workflow.js` with the packet,
   **FROM THE MAIN SESSION**, as ONE object with the packet in `args`:

   ```text
   Workflow({ scriptPath: "<abs>/…/ref/page-lifecycle.workflow.js",
              args: <the packet, a JSON OBJECT> })
   ```

   🚫 **Do not delegate this step to a subagent.** A subagent is not handed the
   `Workflow` tool. `haipipe-page-auditor-agent` declared it, was dispatched
   for the first time on 260818, and returned `blocked` at this exact step with
   0 steps and no receipt. That agent is a packet builder and a receipt keeper
   since 0.3.0; the dispatch is the main session's and cannot be moved.

   The workflow then dispatches a phase-scoped producer for OUTLINE, DRAFT,
   PROBE, EVIDENCE, REVISE, or COMPILE, a mechanical builder/version snapshot,
   and a fresh read-only reviewer for CHECK.
3. Follow returned routes rather than a prescribed order. Only CHECK may CLOSE.
   A route to DRAFT from another phase begins a new round only when purpose or an
   Aim reopened.
4. Stop at CLOSE, explicit HOLD, a missing input, a version mismatch, a required
   human gate, `max_steps`, or `max_rounds`. A limit stop means the run did not
   converge; it never means quality passed.
5. Write the exact Workflow result to
   `<board>/_runs/page/<page-id>/<run-id>.json`. Do not append the terminal CHECK
   result to the Page, because that would mutate the approved version.
6. Run `haipipe-board/cli/pageflow.py audit <receipt.json>`. Report the terminal
   route, checked version, traversed edges, deterministic finding count,
   semantic finding count, human-gate state, and residual risk.

RUN never lets one hidden pass write, judge, fix, and approve. The producer and
judge have different actor identities, and every changed version returns
through CHECK before CLOSE.

## 🧾 The receipt is the workflow's one state source

`<board>/_runs/page/<page-id>/<run-id>.json` is where a run's history lives, in the exact shape `ref/page-run-contract.md` fixes.
A surface that shows where a page stands in its lifecycle reads these receipts and nothing else, the same way the labeling stepper reads `## States`.
That surface ships: the 🪜 Workflow menu's `📄 Page phases` stepper (`haipipe-board/assets/js/10-drawer/65-plugin-pageflow.js`) draws the loop along the bottom of the split viewer, fed by `GET /_board/pageruns` (`live/pageruns.py`), which matches receipts by their own `page` field.
A page with no receipts is not an error: its next authority is the contract's own default, CHECK for an existing page, OUTLINE for a new one, and the stepper states exactly that.

## 📂 Files

**This skill's own files**: what ships in the folder, and what each part is for.

```
haipipe-page-workflow/
├── SKILL.md            this contract
├── CHANGELOG.md        version history
└── ref/
    ├── page-run-contract.md   the packet + receipt spec RUN and its members share
    ├── producer-contract.md   every phase producer's packet, procedure, house
    │                          rules and return shape, in one copy
    └── phase-cards.md         all phases in the same six fields, in loop order
```

The executable machinery stays under `haipipe-board`: `ref/page-lifecycle.workflow.js` (the controller), `src/page_lifecycle.py` (the deterministic auditor), and `cli/pageflow.py` (the audit CLI).
The non-interactive dispatch target is `agents/haipipe-page-auditor-agent.md`, which invokes this contract in a fresh context.

**The Board pages that argue this family** are the `QPw` group on `BoardSkillBoard-260722`, re-cut 260818 when JL ruled one page per workflow step:

```text
🔁 QPw00  the loop itself: the time axis, RUN ≠ ADVANCE, the audit

⏱️ THE PHASES · one page per phase, in loop order, each one RUNS
🧭 QPw1  OUTLINE   ✏️ QPw2  DRAFT    📮 QPw3  PROBE
🃏 QPw4  EVIDENCE  🖊 QPw5  REVISE   ✅ QPw6  CHECK
   └─ QPw4's three PARALLEL lanes: 📚 QPw4c citation · 🧮 QPw4v value
                                   · 🖼 QPw4d display intake

🔧 THE MACHINE · cuts ACROSS all six. No position in time; never "runs"
🤲 QPw00a  🎭 WHO acts       the three agent units, and the act each may never do
🧾 QPw00r  📜 WHAT proves it the receipt per attempted phase, chained by hash
✋ QPw00g  ⚖️ WHO says yes    the five ticks a machine may never write
```

⚠️ **7, 8 and 9 are not phases ⑦⑧⑨.** They share the group's numbering and
nothing else: read in sequence they would say "CHECK, then agents, then
receipts, then the gate", which is not a thing that happens. They are the run's
three axes, actor · record · authority, and each carries its own open ruling
(the orchestrator was never dispatched · receipts store absolute paths · no
surface joins the five ticks), which is why they are three pages and not one.

COMPILE has no page because it has no contract of its own; it is folded into `haipipe-page-revise`, and whether that fold is permanent is `QPw5`'s open ruling. Each page's `## Law` rows and its `### Decision Now` carry what its contract leaves open.
