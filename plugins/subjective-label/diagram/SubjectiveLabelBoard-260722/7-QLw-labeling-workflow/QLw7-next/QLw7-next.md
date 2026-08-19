# NEXT?: close the round, and decide whether another one is worth the hours
state: 🟡 PARTIAL · the move is settled · open: no route carries a price, so stopping is judged without a cost
owner: JL
method: Say what the phase leaves behind, when it is finished, whose hand does what, what the person does, and where the work may go next.

## Opening
Is the policy done, or is another round worth one to three more hours of the person's time?
This is the phase that ends a round, and it is the only one that looks forward instead of back.
It is a business decision made from semantic evidence, which is why the person signs it and an agent writes it down.

**Where this page sits**: This is phase 7 of eleven, and it belongs to the round rhythm; `QLw00` holds the whole sequence.
`QB3` argues what a checkpoint contains and `QD4` argues the stopping gates; this page owns the phase's timing, its five routes, and the price each one carries.

**Why it matters**: Rounds feel productive, so without a priced decision the loop runs until the person is tired rather than until the policy is done.

**What is settled here**: The five routes, what closes a checkpoint, the two hands, and the trap.

**What remains open**: No route carries an expected yield or a cost, so the decision is made on movement alone.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**A phase page owns TIMING and AUTHORITY, never method.** `QB3-checkpoint-and-versions` argues how this step is done, and repeating it here creates a copy that goes out of date.
Write when it starts, when it is finished, who may act, and what each hand may never do.

**The unit is an ITEM, never the corpus this project happens to hold.** The eleven phases run the same on a clinical note or a transcript turn.

**The trap is part of the contract.** A phase that only says what to do cannot be checked against what went wrong.

**Language and sentences**: English only, in the source and in the render.
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes: use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

## Diagram
**Phase 7 in place**: what enters, what this phase makes of it, and where it may go.

```text
   🚦  PHASE 7  NEXT?   🔁 each round
   --------------------------------------------------------------
   makes   Checkpoint t   the closed round: cumulative gold D_t and closed policy G_t
   makes   the route      one of five, named with the measurement that chose it
   makes   ⬜ the price    the next round's expected yield against its human cost

   then    -> 2 PICK      another round, on a new claim
   then    -> 4 LABEL     extend this batch, same claim
   then    -> 5 RULES     the rules were wrong, not the evidence
   then    -> 8 FREEZE    stop: all four gates hold
   then    -> HOLD        a gate cannot be evaluated, so nothing closes
```

## Content

### 1 · What this phase produces
**What is on disk when this phase ends**: the artifact name is the method's word, and the sentence beside it is what it means.

```text
Checkpoint t   the closed round: cumulative gold D_t and closed policy G_t
the route      one of five, named with the measurement that chose it
⬜ the price    the next round's expected yield against its human cost
```

A `⬜` above marks an artifact this workflow requires and nothing on disk produces.

### 2 · When it is done
**The exit test**: every line must hold, and a `⬜` line is one that cannot be checked today.

```text
✔ the route is named WITH the measurement from phase 6 that chose it
✔ the checkpoint was written by the keeper, from inspectable human evidence, and by nothing else
✔ quality, stability, coverage and risk were each read, and a failing gate blocks CLOSE
```

A phase with no exit test ends when someone feels finished, which is not a boundary a later reader can verify.

### 3 · The hands, and what each may never do
**A hand is named by what it may NEVER do**: the identity of each one is its boundary.

```text
gallery-keeper-agent   validates the package and closes the checkpoint
                       NEVER: may not close one whose human evidence or seal is missing
🧠 the person           signs the route
```

`QF3-agent-topology` fixes the authority these hands hold across the whole workflow, and this page says only which of them act in phase 7.

### 4 · The person's job, and the trap
**Sees, does, and the trap**: the mistake a person naturally makes here belongs in the contract.

```text
sees   what moved, what it cost, and what the next round would cost
does   picks one: close, extend this batch, redo the rules, new claim to
       pick on, or hold
trap   running another round because it feels productive
       the round has a price, and this screen is where it is paid
trap   closing on a plateau alone
       a policy can stop moving because it is done or because the
       batches stopped being hard
```

The cost of this phase to the person is recorded once, in `QLw00` division 1, and never restated here.

### 5 · Where it goes next
**The routes out**: each one names the condition that takes it.

```text
-> 2 PICK     another round, on a new claim
-> 4 LABEL    extend this batch, same claim
-> 5 RULES    the rules were wrong, not the evidence
-> 8 FREEZE   stop: all four gates hold
-> HOLD       a gate cannot be evaluated, so nothing closes
```

A phase with one route is not a decision, and a phase with several is not free to take any of them.

## Aims

### A1 · 📦 What this phase produces
- A1.1 · Everything this phase leaves on disk is named, and anything it requires but does not produce is marked.
  **Done when:** Division 1 carries it.

### A2 · ✔️ When it is done
- A2.1 · A later reader can check that this phase finished, without asking the person who ran it.
  **Done when:** Division 2 carries it.

### A3 · 🤖 The hands, and what each may never do
- A3.1 · Every hand that acts in this phase is named with the one act it may never perform.
  **Done when:** Division 3 carries it.

### A4 · 🧠 The person's job, and the trap
- A4.1 · The person knows what they will see, what they must decide, and the mistake they are about to make.
  **Done when:** Division 4 carries it.

### A5 · 🚦 Where it goes next
- A5.1 · Every way out of this phase names the condition that takes it.
  **Done when:** Division 5 carries it.

## States

### A1 · 📦 What this phase produces
- ⬜ A1.1 · Not met; the marked line has no implementation.

### A2 · ✔️ When it is done
- ✅ A2.1 · Met; division 2 carries it.

### A3 · 🤖 The hands, and what each may never do
- ✅ A3.1 · Met; division 3 carries it.

### A4 · 🧠 The person's job, and the trap
- ✅ A4.1 · Met; division 4 carries it.

### A5 · 🚦 Where it goes next
- ✅ A5.1 · Met; division 5 carries it.

## Files

### Contracts · what this Page describes
- `../../agents/gallery-keeper-agent.md`
  The Checkpoint Keeper, the sole writer of closed round state.

## Law
- 260806 JL · 🛑 Plateau requires a quality floor
      Calibration stops only when quality, stability, coverage, and risk gates hold across consecutive rounds.

## Glossary
- 🚦 **NEXT?**: phase 7 of eleven, which the closed round: cumulative gold D_t and closed policy G_t.
- 📄 **Item**: one piece of text the person judges, of any kind.
- 🚦 **Route**: the named way out of this phase, and the condition that takes it.

## Log
260818 · Created QLw7 as one page per workflow phase, on JL's ruling that each step of the labeling workflow gets its own page.
