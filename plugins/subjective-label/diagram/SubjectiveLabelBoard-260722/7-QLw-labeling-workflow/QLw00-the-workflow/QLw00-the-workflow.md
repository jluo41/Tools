# The workflow: the eleven phases of one labeling job, and what a person does in each

> **Superseded runtime model (v0.3 design history).** The active v0.4 family is
> organized as the `subjective-label` umbrella, the `label-building` and
> `label-scanning` sibling doors, and `subjective-label-workflow`: six
> journey phases in two sides (Building: `Contract`, `Round`, `Freeze`;
> Scanning: `Test`, `Scan`, `Audit`) joined by a signed Label Handoff. The
> eleven-phase material below remains design history; do not route a run from it.
state: 🟡 PARTIAL · eleven phases, two rhythms, where each output lands · open: A5.2, no closed round to walk
owner: JL
method: Name every phase the work actually has, say what it produces, what the person does, what it costs, how often it happens, and which division of the run page its output lands in.

## Opening
What are the steps of a labeling job, in the order they happen, and what does the person do in each one?
Every other page on this Board argues one step in depth, and no page says what the whole sequence is.
This page fixes the eleven phases, their two rhythms, the person's job in each, and where each phase's output lands on a run page.
A run page is one corpus and one label target being labeled, and it carries five divisions the eleven phases write into.

**Where the sequence lived before**: the method is spread across seven groups and 25 pages, from `QA0` to `QG1`, and before this group opened the only list of the steps was inside `skills/page-workflows/label-round/SKILL.md`, whose phases A to F cover one round and say nothing about opening or closing the job.

**What a run page is**: `S-Label-<n>-<corpus>-<target>`, the one page a person opens to see where a labeling job stands.
Its five Content divisions are fixed by `haipipe-page-for-labeling`, and two are written today, `S-Label-1-acibench-authority.md` and `S-Label-2-acibench-social-proof.md`, neither of which has closed a round.
A run page always sits on a different board from the method it obeys, so a phase named here has to say which division over there it writes into.

**Where this page sits**: `## Pipeline` on `board.md` draws the GROUP axis, which is which responsibility group a reader visits next.
This page draws the RUN axis, which is what actually happens when someone labels a corpus.
`QA0` fixes the conception, `QB` through `QE` argue each step's method, `QLw1` to `QLw11` own each phase's timing and authority, and `QLw12` to `QLw14` run the loop; this page is the only page on this Board that holds the whole sequence.

**Why it matters**: A person joining this project cannot start from 25 pages.
They can start from eleven rows, and then read the page that owns whichever row they are standing on.

**What is settled here**: The eleven phases, their order, which repeat and which happen once, what the person does in each, the trap in each, the rough cost of each, and which page owns the machinery.

**What remains open**: Whether division 5's map survives contact with a real run.
No round has closed on either run page, so the map is read off the Page Type's contract and two unstarted specimens rather than walked against a round that happened.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**Plain words, because this page is the door.** Every other page may use the method's vocabulary; this one is read first and by people who do not have it yet.
Write `small models guess first` before writing `sealed pre-labels P_t`, and put the method's name in parentheses after the plain one.

**A phase is named by its MOVE, never by its artifact.** `PICK` says what happens; `candidate pool C_t` says what is left behind.
The artifact name belongs in the row's body, and the move belongs in the name, because a reader scanning eleven names is asking what happens next.

**The unit is an ITEM, never the corpus this project happens to hold.** Write `item` and not `review`, because the eleven phases run the same on a clinical note or a transcript turn, and a page that says `review` quietly claims otherwise.

**Every phase says what it COSTS the person.** A phase with no cost line reads as free, and the whole design exists to protect the one phase that is not.

**The trap is part of the contract.** Each phase names the mistake a person naturally makes there, because a phase that only says what to do cannot be checked against what went wrong.

**Language and sentences**: English only, in the source and in the render.
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes: use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

## Diagram
**The two rhythms**: six phases repeat until a person says stop, and five happen exactly once.

```text
        📆 ONCE                🔁 REPEATS                    📆 ONCE
     ┌──────────┐      ┌──────────────────────┐      ┌──────────────────┐
     │ 1 START  │─────▶│ 2 PICK               │      │  8 FREEZE        │
     └──────────┘      │ 3 LOCK               │      │  9 SCORE         │
                       │ 4 LABEL   ⬅ the cost │─────▶│ 10 LABEL ALL     │
                       │ 5 RULES              │ stop │ 11 SPOT CHECK    │
                       │ 6 NUMBERS            │      └──────────────────┘
                       │ 7 NEXT?  ──┐         │
                       └────────────┼─────────┘
                            ▲       │ another round
                            └───────┘
```

## Content

### 1 · The eleven phases, in the order they happen
**The whole job on one screen**: the person's job and its cost sit in the row, because a step whose cost is not written reads as free.

```text
#   PHASE       WHAT HAPPENS                 YOUR JOB              TIME      HOW OFTEN
──────────────────────────────────────────────────────────────────────────────────────
1   START       pick the trait + corpus.     say what HIGH         1 hour    once
                read ~15 items               means, from your
                                             own reactions
──────────────────────────────────────────────────────────────────────────────────────
2   PICK        machine picks 60 items       say yes or no         10 sec    each round
                and says why

3   LOCK        small models guess first.    nothing.              0         each round
                guesses hidden from you      do NOT peek

4   LABEL       you read each item           HIGH / LOW / NONE,    1-3 hr    each round
                one by one                   the region, and why   the cost

5   RULES       machine turns your "why"     accept or reject      30 min    each round
                into rules                   each rule

6   NUMBERS     machine measures what        read them             2 min     each round
                changed

7   NEXT?       another round, or stop?      pick one              5 min     each round
                "another round" goes back to step 2
──────────────────────────────────────────────────────────────────────────────────────
8   FREEZE      rules stop changing          sign it               1 hour    once
                                             this ends the job

9   SCORE       every model tested on a      nothing               0         once
                hidden set

10  LABEL ALL   best model labels the rest   answer the hard       ongoing   once
                of the corpus                ones it sends you

11  SPOT CHECK  fresh sample, checked        label them blind,     1 hour    once
                independently                THEN compare
```

An ITEM is one piece of text the person judges, and this workflow never assumes which kind.
On this project an item is a physician review, because that is the corpus this Board opened on; the same eleven phases run on clinical notes, messages, transcript turns, or paragraphs, and nothing in them depends on the choice.
The times are rough and assume a 60-item round; they are here to show the SHAPE of the cost, not to be quoted as measurements.
Phase 4 holds roughly 85 percent of the person's hours, and every other phase either chooses what phase 4 looks at or harvests what phase 4 produced.

**Every phase has TWO pages, and this block summarizes neither**: the `QLw` page fixes when the phase starts and which hand may act, and the `QA` to `QE` page fixes how the work is done.

```text
#   PHASE       TIMING     THE METHOD
──────────────────────────────────────────────────────────────────────
 1  START       QLw1       QB1 initialize round one · QA2 label region uncertainty
 2  PICK        QLw2       QC1 candidate pool · QC3 compose human batch
 3  LOCK        QLw3       QC2 prelabel and seal
 4  LABEL       QLw4       QB2 human-ai session · QC4 blind adjudication
 5  RULES       QLw5       QD1 optimize guideline · QA3 guideline contract
 6  NUMBERS     QLw6       QD2 round metrics · QD3 coverage and stability
 7  NEXT?       QLw7       QB3 checkpoint and versions · QD4 stopping criteria
 8  FREEZE      QLw8       QE1 sealed final test
 9  SCORE       QLw9       QE2 model scorecard
10  LABEL ALL   QLw10      QE3 complete corpus
11  SPOT CHECK  QLw11      QE4 final audit and provenance
```

The split is `board.md`'s own: a phase page owns TIMING and AUTHORITY only, and the method stays on the `QA` to `QE` page named in the row, because a copy of a method goes out of date the night it is written.

### 2 · Six phases repeat, five happen once, and the difference is a rule
**The two rhythms are not a picture**: which rhythm a phase belongs to decides what it may cost and where a signature may sit.

```text
🔁 THE ROUND        phases 2 to 7, run N times, and nobody knows N
                    board.md's own words: "A Calibration Round starts
                    from a closed policy, selects or receives a human
                    batch, runs one or more Human-AI Sessions, and ends
                    at a Checkpoint"
📆 THE LIFECYCLE    phases 1, 8, 9, 10, 11, each exactly once
                    board.md's own words: "the chronological path
                    through the six responsibility groups"
```

**Three consequences**: what each rhythm decides, and why the split has to be written down rather than drawn.

```text
1  WHERE A SIGNATURE MAY SIT
   JL ruled the human gate LAST (260818). In one flat list "last" means
   "after round N", and nobody knows N while the job is running.
   So the closing signature can only live in the LIFECYCLE, at 8 FREEZE.
   Phase 7 closes a ROUND. Phase 8 closes the JOB. Different ticks.

2  WHAT MAY BE EXPENSIVE
   1 START costs an hour and happens once, which is affordable.
   2 PICK costs ten seconds and happens every round, which is affordable.
   An hour-long gate inside the round would cost N hours, and nobody
   would run round 5.

3  HOW A ROUND IS WRITTEN DOWN
   haipipe-page-for-labeling already ruled it: "A ROUND IS A RECORD,
   NEVER A DIVISION. Rounds keep arriving... a ### per round would make
   the Page grow without end."
   Lifecycle phases get headings. Round phases get record lines.
   That rule only makes sense if the two rhythms are different kinds.
```

The Board Map on `board.md` already draws this as a picture: `QA` and `QB` run down, `QD` carries the elbow that reads `back to QC1 for the next round`, and `QE` runs down again.
The elbow IS the round, and until this page nothing on the Board said so in words.

### 3 · What the person does in each phase, and the trap in each
**A phase that only says what to do cannot be checked**: the trap is the mistake a person naturally makes there, so it belongs in the contract.

```text
1   START
   sees   about 15 items, drawn at random, and nothing else
   does   reacts: yes, no, not sure. The agent drafts what HIGH means
          FROM those reactions, and the person corrects the draft.
   trap   writing the definition before looking at items. The method
          assumes the concept is vague, so a definition written cold is
          a definition of something else.

2   PICK
   sees   one screen: how many items, from which strata, and WHY
   does   believes the WHY, or refuses it
   trap   rubber-stamping. This is the only cheap veto in the round;
          after it, the machine spends the person's hours.

3   LOCK
   sees   nothing
   does   nothing
   trap   peeking. Reading the models' guesses before judging
          contaminates every number downstream, and without a hash
          nobody can show later that it did not happen.

4   LABEL
   sees   one item, verbatim, with its id, and nothing else on the
          first pass
   does   the class, the region, how sure, and WHY in one sentence in
          the person's own words. Then the reveal: where the small
          models disagreed, and the person either changes their mind
          (recorded AS a change) or says why the models are wrong,
          which becomes a rule.
   trap   staying consistent with a half-remembered rule. Judge
          honestly and let the contradiction surface; catching it is
          the machine's job.
   trap   "it's obvious" as a reason. A reason that cannot generalize
          is not a reason.

5   RULES
   sees   proposed rules, each with the item ids that forced it, and
          the past labels this rule would flip
   does   accept, reject, or narrow, one rule at a time
   trap   accepting a rule that restates one item. A rule covering only
          its own example is a casebook entry, not a rule.
   trap   letting a new rule silently break an old label. Every flip is
          a question: was the old call wrong, or is the rule too wide?

6   NUMBERS
   sees   correction rate, agreement on the audit stratum, coverage per
          region, concept stability, and the answer to phase 2's WHY
   does   reads them and answers phase 2: was the reason we picked
          these items right?
   trap   reading agreement as accuracy. Agreement on the stratum the
          models already agree about is the easiest number here.

7   NEXT?
   sees   what moved, what it cost, and what the next round would cost
   does   picks one: close, extend this batch, redo the rules, new
          reason to pick, or hold
   trap   running another round because it feels productive. The round
          has a price, and this screen is where it is paid.

8   FREEZE
   sees   the final guideline, and every computed check already at zero
   does   reads it as a STRANGER would, and answers one question: could
          someone who has never met me follow this?
   trap   signing because the rounds went well. `state: ✅` means a
          person signed the freeze, never that the numbers looked good.

9   SCORE
   sees   scorecards
   does   nothing
   trap   none. This phase is read-only by design.

10  LABEL ALL
   sees   only the items the executor refused to settle, arriving as a
          queue rather than as a batch
   does   works a risk queue. The role changes from teacher to on-call.
   trap   rubber-stamping when tired. A tired yes on the queue is gold
          with nobody's judgment in it.

11  SPOT CHECK
   sees   a fresh sample of finished items, with the machine's label on
          each one hidden until the person has judged it
   does   judges a fresh independent sample BLIND, then compares
   trap   looking at the machine's label first. If it is seen, the
          audit measures agreeableness, not the system.
```

### 4 · What runs the phases, and where each contract lives
**The machinery**: three pages that are not phases, and what each one owns.

```text
QLw12  the agents     the nine hands, each named by the ONE act it may
                      never do, against the phases each acts in
QLw13  the receipts   how the loop is RUN: the four words, one receipt per
                      ATTEMPTED phase, and the six stops of which five are
                      not success
QLw14  the gate       the five ticks a machine may never write, on ONE
                      surface, accept-biased
```

This page owned drafts of the receipt contract and the tick surface until 260818, when `QLw13` and `QLw14` were written and took them.
Two pages stating one contract is how a contract drifts, so this division points and states nothing.

### 5 · Where each phase's output lands on a run page
**The other end of the sequence**: which division of a run page each phase writes into, because a phase whose product a reader cannot open is a phase nobody can check.

```text
        THE RUN PAGE · S-Label-<n>-<corpus>-<target> · five divisions,
        fixed by haipipe-page-for-labeling and not by this page

  §1 What <target>      ◀ 1 START       the first meaning, drafted FROM the
     means now                          person's reactions to ~15 items
                        ◀ 5 RULES       every round rewrites the boundary here
                        ◀ 8 FREEZE      the last version, and it stops moving

  §2 Rounds             ◀ 2 PICK        the item count on the block's head line
     one block per      ◀ 3 LOCK        no line of its own; it is half of 4's
     closed round,      ◀ 4 LABEL       one line: where policy and person split
     newest first       ◀ 5 RULES       which rules were added, and the policy
                                        version the round closed
                        ◀ 6 NUMBERS     the audit reading and the thin regions
                        ◀ 7 NEXT?       the closing date; it writes the block

  §3 Gates:             ◀ 6 NUMBERS     refreshes each gate's current reading
     may we stop?       ◀ 7 NEXT?       reads them, and answers the heading

  §4 Freeze, sealed     ◀ 8 FREEZE      G*, and the one signature a machine
     test, scorecards                   may never write
                        ◀ 9 SCORE       one scorecard per candidate executor

  §5 The labeled        ◀ 10 LABEL ALL  D*, plus the risk queue it routes back
     corpus             ◀ 11 SPOT CHECK the blind sample, and what it found
```

**Two rhythms, two shapes on the page**: division 2's rule is paid here, and this is what it buys.
The six round phases share ONE division and land as record lines, because `haipipe-page-for-labeling` rules that "a round is a RECORD, never a division" and that "rounds keep arriving... a `###` per round would make the Page grow without end".
The head line and the four record lines each phase writes into are the block that contract already shows, not fields invented here.
The five lifecycle phases each own a headed division, because each happens once and a heading that appears once cannot make a page grow.

**An empty division is a status, not a gap**: `§4` and `§5` sit on a run page from the day it opens, showing what has not happened yet.
Before phase 8 has run, `S-Label-1-acibench-authority.md` reads `🔒 G* not frozen` and `🧪 T* test3, 1,213 turns, sealed and unread`, which is a report a missing heading could not make.
`S-Label-2-acibench-social-proof.md` reports the same, over the same sealed split, so an unstarted run is legible on both pages rather than blank.
That is why the map above has no gaps: every phase has a place waiting for it before it runs.

**Phase 3 is the one phase with nothing to show, and that is its contract**: what LOCK seals is unreadable until phase 4's reveal, so it never appears as prose on a run page.
It reaches the reader as one line of the round's record, the line the Page Type writes as `🎯 challenge  policy and the human disagreed on 11 of 60`, because the sealed guess is what the person's judgment is compared against.

**Content is not the only surface**: eight phases write a `## States` row on a run page, and one phase writes its `state:` line.

```text
  ## States          ◀ 2 PICK        A4's "the seal holds": no sealed-test id in
     five Aim groups,                the candidate manifest
     fixed by the    ◀ 3 LOCK        A4 again: none in the sealed pre-labels
     Page Type and                   either, which is all LOCK ever shows
     not by a phase  ◀ 5 RULES       A1's "traceable to its round": each rule
                                     names the round that forced it
                     ◀ 6 NUMBERS     A3's four gates, the reading §3 also shows
                     ◀ 7 NEXT?       A2: the closed round is reproducible from
                                     its own folder
                     ◀ 9 SCORE       A4's scorecard per candidate, and A1's
                                     "the policy is executable"
                     ◀ 10 LABEL ALL  A5: the corpus is complete with provenance
                     ◀ 11 SPOT CHECK A5: the audit says what is reliable

  state: line        ◀ 8 FREEZE      ✅ because a person signed the freeze, and
                                     never because the rounds went well
```

`haipipe-page-for-labeling` fixes five Aim groups that mirror the five divisions, so a phase updates a State row and never adds an Aim of its own: `QD4` fixed the four gates under `A3`, and the Page Type fixed the other four groups.
Phase 3 shows nothing in Content and still writes here, because a run page's seal Aim is answered by two manifests and the sealed pre-labels are the second one.
Two phases write no State row at all: `1 START` opens the page before any Aim can move, and `4 LABEL` reaches States only through `6 NUMBERS`, which is what reading a round means.
Phase 8's `✅` is the trap division 3 writes under that phase, and it is the one line on a run page that no machine may write.

**The other page kind takes no phase's output**: `haipipe-page-for-labeling` fixes two kinds, and the one mapped above is the run page.
The other is `S-Label-Dash`, one control page per board, whose subject is which runs exist and where each one stands.
Its Aims are about the roster's completeness, and that contract rules "An Aim tracking a run's gate belongs on that run's page", so a phase lands its output once on the run page and the Dash's row reads it rather than repeating it.

**A run page is on ANOTHER board**: the method is settled on this Board and the runs live on the project's own, so a run page can never be a `### 🔗 Related Board Pages` row here, where it would report `dead-related-page`.
Division 5 cites it as a `## Files` path instead, and `haipipe-page-for-labeling` calls that crossing the single most likely defect in a new run page.

## Aims

### A1 · 📋 The eleven phases, in the order they happen
- A1.1 · A person who has read no other page on this Board can name every phase, what it produces, and what it costs them.
  **Done when:** Division 1 lists all eleven with a job and a cost, and points each at the page that owns its method.

### A2 · 🔁 Six phases repeat, five happen once, and the difference is a rule
- A2.1 · The two rhythms are stated as a rule with consequences, not drawn as a picture.
  **Done when:** Division 2 names which phases belong to which rhythm and what each rhythm decides.

### A3 · 🧠 What the person does in each phase, and the trap in each
- A3.1 · Every phase says what the person sees, what they do, and the mistake they naturally make.
  **Done when:** Division 3 carries all three for all eleven phases.

### A4 · 🔧 What runs the phases, and where each contract lives
- A4.1 · A reader looking for the runner, the record, or the signature is sent to the one page that owns it, and finds no second copy here.
  **Done when:** Division 4 names `QLw12`, `QLw13` and `QLw14` and restates none of their contracts.

### A5 · 🗂 Where each phase's output lands on a run page
- A5.1 · Every one of the eleven phases names the run page division its output lands in, and none of them lands nowhere.
  **Done when:** Division 5 maps all eleven phases onto the five divisions `haipipe-page-for-labeling` fixes, and says what each phase leaves there.
- A5.2 · The map is walked against a real run instead of being read off a contract.
  **Done when:** One closed round on a run page shows its record block in `§2` and its gate readings in `§3`, and division 5 cites that run and round number.

## States

### A1 · 📋 The eleven phases, in the order they happen
- ✅ A1.1 · Met; division 1 carries all eleven with job, cost, rhythm, and both owning pages for each: the `QLw` page that owns its timing and the `QA` to `QE` page that owns its method.

### A2 · 🔁 Six phases repeat, five happen once, and the difference is a rule
- ✅ A2.1 · Met; consequence 1 now puts the closing signature at `8 FREEZE` and reads "Phase 7 closes a ROUND. Phase 8 closes the JOB.", which is the numbering the rest of the page uses.

### A3 · 🧠 What the person does in each phase, and the trap in each
- ✅ A3.1 · Met; the `NEXT?` block is headed `7`, and `sees` is written for phases 10 and 11, so all eleven carry sees, does, and trap, with two traps each on phases 4 and 5.

### A4 · 🔧 What runs the phases, and where each contract lives
- ✅ A4.1 · Met; division 4 points at the three machinery pages and states none of their contracts.

### A5 · 🗂 Where each phase's output lands on a run page
- ✅ A5.1 · Met; division 5 places each of the eleven phases on one of the five divisions and says what it leaves there, with the six round phases named one by one against the record block `haipipe-page-for-labeling` fixes, and it now also maps the two surfaces outside Content, the eight phases that write a State row and the one that writes the `state:` line.
  It also says where a phase's output does NOT go: `S-Label-Dash`, the Page Type's other kind, reads a run's row rather than receiving anything a phase produces.
- ⬜ A5.2 · Not started; both `S-Label-1-acibench-authority.md` and `S-Label-2-acibench-social-proof.md` record `📌 0 rounds closed`, so no closed round exists anywhere to walk the map against.

## Files

### 📋 Contracts · what this Page describes
- `../../skills/label-building/SKILL.md`
  Phases A to F, the only place the round's sequence exists today, and where the resume promise is made: "Resume the recorded open phase when one exists". Also: Phase 1 START.
- `../../skills/label-scanning/SKILL.md`
  Phases 8 FREEZE and 9 SCORE. Also: Phases 10 LABEL ALL and 11 SPOT CHECK.
- `../../skills/subjective-label/SKILL.md`
  The read-only view of where a job stands.
- `../../skills/page-types/haipipe-page-for-labeling/SKILL.md`
  The Page Type whose "a round is a record, never a division" ruling assumed the two rhythms this page states, and whose five Content divisions are the surface division 5 maps onto.

### 📥 Input files · what division 5 was read against
- `../../../../../examples-nlp/Project-Subjective-Label/diagram/01-label-runs-260807/SL-labeling-runs/S-Label-1-acibench-authority.md`
  The first run page written, and the specimen division 5 checks its map against: the five divisions in place, `📌 0 rounds closed`, and a sealed `test3` of 1,213 items.
- `../../../../../examples-nlp/Project-Subjective-Label/diagram/01-label-runs-260807/SL-labeling-runs/S-Label-2-acibench-social-proof.md`
  The second run page, read to check that the map is not shaped by one specimen: same five divisions, same `📌 0 rounds closed`, and the same sealed split shared with `S-Label-1`.

## Law
- 260818 JL · ✋ The human gate is LAST and accept-biased
      A person is asked to sign only after every computed finding is zero, so the signature is about meaning and never about defects a machine could have caught.
- 260818 JL · 🧾 Receipts land before the gate
      A signature over an unrecorded process signs nothing, so the record of what was attempted must exist before anyone is asked to sign it.
- 260818 CC · 🔁 A phase belongs to exactly one rhythm
      Six phases repeat and five happen once, and which rhythm a phase belongs to decides what it may cost and whether a closing signature may sit in it.
- 260818 CC · 📋 A phase is named by its move, never by its artifact
      `PICK` says what happens and `candidate pool C_t` says what is left behind, and a reader scanning eleven names is asking what happens next.

## Glossary
- 🔁 **Round**: phases 2 to 7, run again and again until phase 7 says stop, and nobody knows how many times while the job is running.
- 📆 **Lifecycle**: phases 1, 8, 9, 10 and 11, each of which happens exactly once per labeling job.
- 🧾 **Receipt**: the record of an ATTEMPTED phase, which is not the same as the record of a closed artifact, because an abandoned phase produces no artifact.
- ✋ **Tick**: a mark only a person may write, of which this workflow has five.
- 📄 **Item**: one piece of text the person judges, of any kind. This project's items are physician reviews, and no phase depends on that.
- 🎯 **The cost**: phase 4, which holds roughly 85 percent of the person's hours and which every other phase exists to protect.
- 🗂 **Run page**: `S-Label-<n>-<corpus>-<target>`, the page carrying one corpus and one label target, whose five Content divisions are where the eleven phases put what they produce.

## Log
260818 · Created QLw00 to hold the RUN axis, which `## Pipeline`'s GROUP axis is not, and which existed only inside `label-round`'s phases A to F.
260818 · JL ruled the phase list must read in plain words before the method's vocabulary, because this page is the door a new person enters through.
260818 · JL ruled the phases count from ONE, so no page id sits one character from `QLw00`; the eleven phases became `QLw1` to `QLw11` and the machinery `QLw12` to `QLw14`.
260818 · CHECK routed this page to a new DRAFT round: divisions 4 and 5 had become copies of `QLw13` and `QLw14`, which did not exist when they were written, so both were replaced by one pointer division and Aims A4 and A5 retired to those pages.
260818 · DRAFT round 2 opened a new `A5`: a reader could name all eleven phases and still not know what a run page shows, because nothing on the Board said where a phase's output lands.
260818 · Division 5 added, mapping the eleven phases onto the five Content divisions `haipipe-page-for-labeling` fixes and `S-Label-1-acibench-authority.md` demonstrates; the division 5 retired earlier the same day was the tick surface, which is now `QLw14`.
260818 · The renumber from 0-10 to 1-11 left old numbers standing in four places, so `A2.1` and `A3.1` moved off ✅ and the page `state:` line moved to 🟡 PARTIAL: division 2's `7 FREEZE` and its "Phase 6 closes a ROUND. Phase 7 closes the JOB.", division 3's second `6` on the `NEXT?` block, the `## Files` rows reading "Phase 0 START", "Phases 7 FREEZE and 8 SCORE" and "Phases 9 LABEL ALL and 10 SPOT CHECK", and the Glossary's "phases 0, 7, 8, 9 and 10".
260818 · All four were corrected in one REVISE pass, and division 3 gained the `sees` line phases 10 and 11 never had, which `A3.1` had claimed was already there.
260818 · Division 5's `§2` row was split so each of the six round phases names what it leaves in a round's record block, instead of the six sharing one line that named the block and no phase's product.
260818 · A second run page, `S-Label-2-acibench-social-proof.md`, was found beside the first, so the Opening's "the only one written so far" was corrected and `A5.2` now reads both pages' `📌 0 rounds closed` rather than one.
260818 · The Opening's group count was corrected against `board.md`: the method spans seven groups and 25 pages, `QA0` to `QG1`, and not six groups.
260818 · The `label-round` row now quotes the resume promise instead of calling it unimplemented, which this page carried no evidence for.
260818 · REVISE round 2 corrected division 5's claim that only two phases write outside a run page's Content: `haipipe-page-for-labeling` fixes FIVE Aim groups and not four gates, so EIGHT phases write a State row and only phase 8 writes the `state:` line, and the eight are now mapped one by one against that contract's own Aim wording.
260818 · Division 1's map now carries the `QLw` phase page beside the `QA` to `QE` method page, because the row sent a reader to the method and never to the page that owns the phase's timing and authority, which is the split `board.md` declares for this group.
260818 · The record line quoted under phase 3 was corrected to the Page Type's verbatim `🎯 challenge  policy and the human disagreed on 11 of 60`; this page had added a `·` the contract does not write.
260818 · Two claims the Board itself had overtaken were corrected: the Opening said the steps appear as a list in exactly one place, which stopped being true the moment this group's fifteen pages and `board.md`'s own `QLw` block were written, and division 2 backticked the Board Map's elbow as `not stopped, back to QC1`, which is not the line that map draws.
260818 · Division 5 now names the second page kind `haipipe-page-for-labeling` fixes: `S-Label-Dash` takes no phase's output, because that contract rules an Aim tracking a run's gate belongs on the run's page, so a map that stopped at the run page left a reader guessing whether a phase writes twice.
260830 · Sibling doors renamed `label-building` / `label-scanning` (JL: Part 1 is Building, not Labeling); Freeze promoted to phase P2 and Test replaces Scorecard, so the family runs six phases; the five `label-*` forwards retired.
260830 · Stage A of the readiness goal: three layers (LAW doors, ORDER side workflows `label-building-workflow` / `label-scanning-workflow`, CROSSING family workflow); round unit, register and rendered views defined in `ref-assets.md` §3, §6a.
260830 · Stage B: page type 0.4.0 reads the units (§1 cheatsheet/gallery, §2 round-unit records, §3 checkpoint gates, §4 handoff row); `fixtures/job-mini` (2 closed round units) + its board render clean, 0 errors; plugin 0.5.0.
