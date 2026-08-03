# CHECK · Who may say a stage is done, and on what evidence?
state: 🟡 PARTIAL
owner: JL
method: one gate per stage; make the APPROVER visible where the state is read, not only where it is logged

## Opening
A gate is the moment a stage becomes done, and the design spends the human's attention there and nowhere else, once per stage, on a finished thing rather than on a stream of approvals. Everything upstream is unattended because nothing upstream can spend. So CHECK carries the entire weight of the design's safety, and two things about it are less settled than they look: who is allowed to say yes, and what they are supposed to be reading when they do.

On who: an agent CAN say yes, and this is sanctioned rather than a loophole. `autopilot` mode puts a fresh-context reviewer subagent in the human's place; it returns approve or restart-from-a-named-phase, human-only items are marked DEFERRED into a queue rather than passed, and the gate row records the agent as the actor. The mode is not a field and never was: `copilot | autopilot` is an invocation choice, and the two files that describe it say so in the same words. `QA6` then improved the RECORD on 260726 by retiring `STATUS.md` and moving the Ledger into each S page's own `## Log`, and that move has landed: nine `GATE ·` rows now sit on six live S pages of the MISQ paper, and the one gate an agent approved is visibly distinguished from the four a human passed. What did not land is the row's SHAPE. The protocol documents a five-column table and not one of the nine rows uses it, so the record exists and cannot be read by anything but a person.

On evidence: every contract declares `done_criteria`, and across the eight there are 73 of them, of which 7 are wholly checkable by a machine and one more is half mechanical and half judgment. The remaining 65 are judgments in prose, and most of them should be. Every contract also declares `closed_when` and `exit_when`, the second being the stage's backward exit when the work fails. No page on this board has ever owned any of the three, so what a gate reads has been defined eight times and described zero.

Scope: This page covers Who may pass a gate, what the gate reads, and where a stage goes when it fails. Neighbouring pages cover Why the earlier phases need no gate is `QC4b`; the why-comments a gate reads are `QC4c`; what a re-run does to a page that already passed is `QC3c`; how a page's state is displayed is `QA9`.

## Diagram
```
   🚦 CHECK.   the human's attention, spent ONCE, on a finished thing.

      DRAFT ──▶ PROBE ──▶ REVISE ──▶  CHECK
      ╰────────  unattended  ───────╯   🧠 one yes

      ✅ safe upstream ONLY because probe_depth caps spending  → QC4b
         remove that ceiling and all three need gates again.

   ── WHO MAY SAY YES: two sanctioned modes ─────────────────────────
      MODE:  copilot | autopilot                      default copilot

      📍 AND IT IS NOT A FIELD. `gate_mode` is a name this board
         invented; the string appears in NO shipped skill. Mode is an
         invocation/session choice, and the two files that describe it
         AGREE, on the substance and nearly on the wording:
           ref/08-stage-gate.md:10   "an invocation/session choice
                                      (copilot | autopilot, default
                                      copilot); it is not Board
                                      frontmatter. Record the selected
                                      mode and approval actor in the
                                      owning S page's ## Log."
           haipipe-paper-check:87    the same, and names :10 as owner.
         This face used to read :10 as saying FRONTMATTER, which is
         the opposite of its text, and reported the pair as two homes
         in conflict. There is one home, the S page's `## Log`, and no
         field to place anywhere. Corrected 260727.

      🧑 copilot     the human reads the exit-criteria report, adds
                     `> JL:` comments, and confirms / restarts / accepts

      🤖 autopilot   a FRESH-CONTEXT reviewer subagent reads the artifact
                     + the report, leaves `> REVIEWER:` comments, returns
                       approve                 ──▶ advance
                       restart-from-<PHASE>    ──▶ that phase re-runs,
                                                   READING the comments
                     · the LEDGER records the agent as actor
                     · HUMAN-ONLY items (bibtex 🔒) are never silently
                       passed: marked DEFERRED into a human queue
                     · the human may REOPEN any agent-approved gate,
                       which resets that stage's ledger row

   ── THE GAP IS NOT THE MODE, AND NO LONGER THE RECORD EITHER ──────
      QA6 260726 ✅  the Gate Ledger moved OUT of STATUS.md and
                     INTO each S page's `## Log`, one row on the
                     page whose gate it was. History cannot be read
                     off disk state, so it needed a home.

      ✅ POPULATED. Nine `GATE ·` rows on six live MISQ S pages,
         each page's `## Log` also carrying its migration note:
           S-Seed-0-seed        seed (JL) + the seed RE-RUN (agent)
           S-Venue-1-pitch      pitch (JL)
           S-Work-1-claims      claims (JL)
           S-Venue-2-narrative  narrative (JL)
           S-Display-0-design   display (JL)
           S-Venue-3-decisions  3 rows for gates never passed
      ✅ AND `state:` DOES DISTINGUISH THEM, which this face had said
         it could not. The one agent-approved page reads
           state: 🟡 REVISE complete, awaiting human CHECK
         while the four human-gated pages read `✅ GATED <date>`.
         An agent's yes advances the work and does NOT turn the page
         ✅, which is the safeguard stated as a consequence rather
         than as a rule anybody wrote.

      ⬜ THE SHAPE is what did not land. ref/08-stage-gate.md:207
         documents a five-column table
           | Stage | Approved | Actor | Date | Notes |
         and not one of the nine rows uses it. All nine are prose:
           GATE · <stage> · confirmed <date> by <actor>. <notes>
         Nothing reconciles the two and nothing checks either, so the
         actor is recoverable only by a person reading a sentence.

   ── ON WHAT EVIDENCE: what the gate actually reads ────────────────
                        done_criteria   machine   mixed
         0-seed                6           1        -
         1a-resource           9           1        -
         1b-claims             8           1        -
         2a-venue             10           0        -   ◄── none at all
         2b-pitch             13           1        -
         3-narrative           9           1        -
         4-display             9           1        -
         5-section-edit        9           1        1
         ──────────────────────────────────────────────
         TOTAL                73           7        1

      the 7 are all the SAME line: `check-probe-cards.sh … exits 0`
      (2b-pitch words it without naming the script, same assertion).
      the MIXED one is 5-section-edit's
        "grep -c '<tpl' {section}.md = 0; structure overview matches
         the paragraph blocks"
      half a shell command and half a judgment, in one criterion.
      This face had counted it as prose and reported 7 of 73; the
      honest split is 7 mechanical, 1 mixed, 65 judgment. Recounted
      260727 against all eight contracts; the 73 and the 10 hold.

      so 65 of 73 are JUDGMENTS IN PROSE. That is not a defect: most
      of them should be judgments. It does mean the gate is a reading
      task, and that no face has ever said so.

   ── AND WHERE IT GOES WHEN IT FAILS ───────────────────────────────
      exit_when:   every one of the eight declares a BACKWARD exit
        0-seed          not viable ──▶ drop the paper
        1b-claims       claim unsupported, no route
        3-narrative     arc weak ──▶ pitch / claims
        4-display       display cannot support claim
        5-section-edit  writing exposes missing evidence ──▶ claims
      ⚠️ CHECK is the only place a stage can take one, and no page on
         this board has ever mentioned the field.

   ── WHO READS THESE FIELDS, AND HOW THEY FAIL ────────────────────
      fields   gates · done_criteria · closed_when · exit_when
      reader   ③ THE EXECUTOR, and then a HUMAN               → QC2
      fails    🔇 SILENT
      ⚖️ AND THIS IS THE ONE FACE WHERE THAT IS MOSTLY CORRECT.
         65 of 73 done_criteria are judgments and should stay
         judgments. "Move it to a program" is the wrong answer here;
         "move it to a human at a named moment" is the right one, and
         CHECK already IS that named moment.
      ⇒ so this block is not under-enforced. It is under-DESCRIBED:
        the three fields have never been explained anywhere a reader
        of this board would find them, which is what this face fixes.
      to bind  the 7 mechanical criteria show the shape of the
               remainder: `check-probe-cards.sh … exits 0` on seven of
               eight. `2a-venue` has ten criteria and no such line, and
               that ONE gap is worth closing, not the other 65.
               ✅ and its cheapest fix is already in its own list:
                  "every `<!-- RULE -->` comment deleted from the
                  filled S-Venue-0-venue.md" is one grep, and
                  `checks.sh` does not grep `<!-- RULE -->` at all.
```

## Content
### The mode is designed, the record has arrived, and only its shape is loose
Autopilot is not a hole somebody left open. It uses a fresh context so the approver is not the author, it refuses to pass human-only items, it records the actor, and it lets a human reopen anything it approved. Each of those is the right decision, and the two files that describe the mode agree about all of it: `ref/08-stage-gate.md:10` calls `copilot | autopilot` an invocation choice, says outright that it is not Board frontmatter, and puts the selected mode and the approval actor in the owning S page's `## Log`; `haipipe-paper-check/SKILL.md:87` says the same and names the first as owner. There is no `gate_mode` field. The string exists in no shipped skill, and a face that reports a field's two homes is reporting on something that was never there.

The record of who approved was given a much better home and has moved into it. `QA6` retired `STATUS.md` on 260726 and put the Gate Ledger into each S page's `## Log`, one row on the page whose gate it was, on the argument that history is the one thing that cannot be re-derived from disk. That is now true on the live paper: nine `GATE ·` rows across six S pages, and every one of those pages carries its own migration note in the same `## Log`. The safeguard reads better than the design promised, too. The single gate an agent approved sits on a page whose `state:` says `🟡 REVISE complete, awaiting human CHECK`, while the four pages a human gated say `✅ GATED <date>`, so an agent's yes moves the work forward without ever presenting itself as the human's.

What is loose is the row's shape. The protocol documents `| Stage | Approved | Actor | Date | Notes |` and all nine live rows are prose sentences beginning `GATE · <stage> · confirmed <date> by <actor>`. Nothing reconciles them, nothing checks either, and the prose form is the one that matches the no-pipe-table rule that `2a-venue`'s own `done_criteria` enforces two files away. So the ledger is readable by a person and by nothing else, and the next paper will copy whichever row it happens to look at.

### A gate is a reading task, and the contracts say so without saying so
Sixty-five prose criteria across eight stages is a real workload, and it is the workload the design is buying with everything upstream: three unattended phases exist so that this reading happens once, on something finished, with the REVISE why-comments beside it. That trade is the core of the design and it is stated on `QC4c` from REVISE's side and nowhere from CHECK's.

The seven mechanical criteria are worth naming as the shape of the answer rather than the answer: `check-probe-cards.sh <paper_root> --stage <key> exits 0` appears in seven of the eight contracts, `5-section-edit` adds an eighth that is half shell command and half judgment in one line, and `2a-venue` has none of any kind.

### The exit nobody has described
`exit_when` is how a stage says the work failed backwards: the arc does not hold, the claim cannot be supported, the writing exposed missing evidence. It is declared in all eight contracts, it can only be taken at CHECK, and it has never appeared on this board. A lifecycle with no described failure exit reads as though stages only ever succeed.

## Aims
- [x] 🚦 One gate per stage, at CHECK
      `gates: [check]` in all eight contracts, verified 260727; `closed_when` and `exit_when` are likewise 8 of 8.
- [x] 📐 The stand-in is designed rather than tolerated
      `ref/08-stage-gate.md:14-28`: fresh context, human-only items marked DEFERRED rather than passed, the actor recorded, and the human may reopen any agent-approved gate, which resets that row.
- [x] 🏠 Give the Gate Ledger a home that survives
      `QA6` 260726: out of `STATUS.md`, into each S page's `## Log`, one row on the page whose gate it was. It was the only part of that file that is history and cannot be re-derived, and it was the last blocker to retiring the file.
- [x] 🔧 The Ledger is populated, not only ruled
      Nine `GATE ·` rows on six live MISQ S pages: seed plus the agent-approved seed re-run on `S-Seed-0-seed`, pitch, claims, narrative, display, and three never-passed rows on `S-Venue-3-decisions`. Each of those pages also carries its `260726 · gate row migrated here` note. This face had said no live page carried one.
- [x] 📐 An agent's yes is distinguishable without opening the Log
      The one agent-approved page reads `state: 🟡 REVISE complete, awaiting human CHECK`; the four human-gated pages read `state: ✅ GATED <date>`. This face had said the two look identical on the surface people read.
- [ ] 🧠 Rule the gate row's SHAPE, then write it once
      `ref/08-stage-gate.md:207` documents `| Stage | Approved | Actor | Date | Notes |`; all nine live rows are prose sentences instead. Two options: adopt the prose row as the spec, which is what nine rows already do and what the no-pipe-table rule in `2a-venue`'s own `done_criteria` would prefer; or keep the table and migrate the nine. Until one wins, nothing can read the ledger and nothing can check it.
- [ ] 🔍 Assert every gate row names its mode and actor
      Both files require the selected mode AND the approval actor in the `## Log`. Nine rows exist, the actor is in all nine, and the mode is named in only one, in prose, on the seed re-run ("unattended run; the default is copilot"). One grep over six files, once the shape above is ruled.
- [ ] 📐 Own `done_criteria`, `closed_when` and `exit_when`
      Declared 8 times each, described nowhere. Say what a criterion is allowed to be, which of the three the gate consults, and that 65 of the 73 are judgments on purpose rather than by neglect.
- [ ] 📐 Describe the backward exit
      `exit_when` is the only way a stage says the work failed, it is declared in all eight contracts, it can fire only at this gate, and it has never appeared on any page of this board.
- [ ] 🔍 Give `2a-venue` its one mechanical criterion
      It is the only stage with no wholly mechanical line, and the cheapest one is already in its own list: "every `<!-- RULE -->` comment deleted from the filled S-Venue-0-venue.md" is a single grep, and `checks.sh` does not grep `<!-- RULE -->` at all.
- [ ] 🧠 Rule what a surviving placeholder means at a gate
      `sections/` carries 89 `\cite{TOADD}` and 56 `{VAL:?}` today. Two options: any survivor at CHECK is a blocking defect; or it is accepted debt, allowed only while its owing `[Q-…]` bracket sits beside it and the page records the ceiling that would release it. Judged case by case now, which is how 89 accumulated.

## States
One gate per stage is implemented and honoured, and both approval modes work as documented. The safety argument holds: nothing before CHECK can spend, so nothing before CHECK needs a person.

The record moved to the right place on 260726 and has arrived. `QA6` retired `STATUS.md` and put the Gate Ledger in each S page's `## Log`; nine `GATE ·` rows now sit on six live S pages, and the one gate an agent approved is distinguishable from the four a human passed without opening the Log at all, because that page's `state:` still says it is awaiting human CHECK. There is no `gate_mode` field to have two homes: the mode is an invocation choice, and the two files that describe it agree.

Two things are genuinely open, and both are about form rather than mechanism. The ledger row has one shape documented and a different one used nine times, so nothing can read it. And the three fields that define what a gate READS have never been described anywhere a reader of this board would find them.

## Files
- `../../paper/1-lifecycle/ref/08-stage-gate.md`
  The gate protocol, both modes, and the no-silent-skips rule.
- `stages/*/stage.md`
  `gates:`, `done_criteria`, `closed_when`, `exit_when`.
- `0-lifecycle/0-seed/S-Seed-0-seed.md`
  The MISQ page carrying the agent-approved seed gate.

## Law

- A stage closes at exactly one gate, at CHECK, and the human's attention is spent there and nowhere else. The phases before it run unattended only because none of them can spend; that is the whole safety argument, and raising `probe_depth` reopens all three.
- CHECK is never implicit. Entering it means presenting the exit-criteria report and the approval ask. Feedback arriving early does not become a gate because somebody responded to it.
- An agent may stand in for the human only in the declared `autopilot` mode, in a fresh context, and it may never pass a human-only item: those are marked DEFERRED and accumulate in a human queue. The ledger records the actor. A human may reopen any agent-approved gate, which resets that stage's ledger row.

## Discussion
> CC 260727: the ledger row's shape needs JL, because the two candidates are each backed by something that already binds. `ref/08-stage-gate.md:207` documents a five-column pipe table. Nine live rows are prose sentences, and the no-pipe-table rule that `2a-venue`'s own `done_criteria` enforces is on the prose side. Option A, adopt the prose row: costs nothing to migrate because it is what the pages already do, and it keeps the ledger consistent with every other hand-edited region on an S page; it costs a checker, because "confirmed 2026-06-23 by JL" is a sentence a grep can find but not parse into an actor, so the mode-and-actor assertion would have to match a fixed prefix rather than read a column. Option B, keep the table: buys a parseable row immediately, and costs nine migrations plus a standing exception to the no-pipe-table convention inside the one region where history accumulates. My recommendation is A with a fixed prefix, `GATE · <stage> · <verdict> <date> by <actor> · mode <copilot|autopilot>`, which is greppable on all five values while staying a sentence. The cost of A that I would not hide is that it makes the ledger a convention rather than a structure, so the checker only catches a row that was written carelessly, never one that was never written.

## Log
260726 · Rewritten from `_archive/QB8-what-is-a-gate.md`, which asked what a gate is and treated the agent stand-in as an unprevented loophole. Reading `../../paper/1-lifecycle/ref/08-stage-gate.md` corrected that: the stand-in is a documented mode with real safeguards. The live gap is narrower and worse, that the board's `state:` cannot show which mode passed a gate. The `done_criteria` / `closed_when` / `exit_when` block was added here because it had no owner on the board at all.
260726 · Aligned against `QA6`, which had moved well past this group. The Gate Ledger moved out of `STATUS.md` and into each S page's `## Log`, which is the right home and is empty on every live page; `gate_mode` came out of the same retirement with two declared locations that disagree.

260727 · Verified every claim in this face against `skills/paper/` and the live MISQ paper, and three of them were wrong in the same direction: this face was reporting a design as unfinished that had finished while it was being written. First, there is no `gate_mode` field. `grep -rn gate_mode skills/paper skills/board` returns nothing, checked twice, so the "two declared homes that disagree" was a report about a field that does not exist. What the two files actually say now, read directly: `ref/08-stage-gate.md:10-12` calls `copilot | autopilot` an invocation/session choice, states outright that it is NOT Board frontmatter, and puts the selected mode and approval actor in the owning S page's `## Log`; `haipipe-paper-check/SKILL.md:87-89` says the same and names the first as owner. They agree. The earlier reading had `:10` saying FRONTMATTER, which is the opposite of its text. The copilot/autopilot distinction itself is entirely real and survives the field's absence, because it was never a field: it is a choice made at invocation and recorded after the fact. Second, the Gate Ledger is populated. Nine `GATE ·` rows sit on six live S pages, and each of those pages carries its own migration note, so the claim that only `_archive/QA1-frontier.md` mentioned one was stale by a day. Third, `state:` does distinguish an agent's yes from a human's: `S-Seed-0-seed.md` carries the one agent-approved row and reads `🟡 REVISE complete, awaiting human CHECK`, while the four human-gated pages read `✅ GATED <date>`. That is the safeguard working, and this face had it as a gap. What replaced all three is a narrower gap that is genuinely open: `:207` documents a five-column ledger table and all nine rows are prose, so the record is readable by a person and by nothing else, and the prose form is the one the no-pipe-table rule prefers. Recounting `done_criteria` confirmed 73 and confirmed `2a-venue` at ten with none, and corrected the mechanical count from 7 to "7 wholly mechanical, 1 mixed, 65 judgment": `5-section-edit` declares `grep -c '<tpl' {section}.md = 0; structure overview matches the paragraph blocks` as one criterion, half shell command and half judgment. The 65 stay judgments, deliberately, and nothing here proposes automating them; the one automation item is `2a-venue`'s single missing line, whose cheapest form is already sitting in its own criteria list as a `<!-- RULE -->` grep that `checks.sh` does not run.
