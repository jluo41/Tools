# NUMBERS: measure what moved, and answer the claim the round was picked on
state: 🟡 PARTIAL · the move is settled · open: the phase-1 claim is not stored, so nothing can answer it
owner: JL
method: Say what the phase leaves behind, when it is finished, whose hand does what, what the person does, and where the work may go next.

## Opening
What actually changed this round, and was the reason the batch was picked on correct?
A round that produces labels but no comparable measurement cannot tell anyone whether it was worth running.
This phase is read-only for the person: it produces numbers, and the decision that uses them belongs to the next phase.

**Where this page sits**: This is phase 6 of eleven, and it belongs to the round rhythm; `QLw00` holds the whole sequence.
`QD2` argues round metrics and `QD3` argues coverage and stability; this page owns the phase's timing and the one question it must answer back to phase 2.

**Why it matters**: Without this phase, `another round` is a feeling. With it, `another round` is a forecast.

**What is settled here**: Which measurements the phase produces, the exit test, the one hand, and the trap.

**What remains open**: Phase 1's claim is not stored anywhere as a field, so today nothing can mechanically answer whether it held.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**A phase page owns TIMING and AUTHORITY, never method.** `QD2-round-metrics` argues how this step is done, and repeating it here creates a copy that goes out of date.
Write when it starts, when it is finished, who may act, and what each hand may never do.

**The unit is an ITEM, never the corpus this project happens to hold.** The eleven phases run the same on a clinical note or a transcript turn.

**The trap is part of the contract.** A phase that only says what to do cannot be checked against what went wrong.

**Language and sentences**: English only, in the source and in the render.
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes: use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

## Diagram
**Phase 6 in place**: what enters, what this phase makes of it, and where it may go.

```text
   📊  PHASE 6  NUMBERS   🔁 each round
   --------------------------------------------------------------
   makes   correction rate how often the person overrode the sealed guess
   makes   agreement      on the stratified consensus-audit stratum, which is the honest one
   makes   coverage       how many confirmed items each of the seven regions now holds
   makes   stability      whether the concept moved between this round and the last
   makes   the answer     phase 2's claim, answered yes or no

   then    -> 7 NEXT?     the measurements exist
```

## Content

### 1 · What this phase produces
**What is on disk when this phase ends**: the artifact name is the method's word, and the sentence beside it is what it means.

```text
correction rate   how often the person overrode the sealed guess
agreement         on the stratified consensus-audit stratum, which is the honest one
coverage          how many confirmed items each of the seven regions now holds
stability         whether the concept moved between this round and the last
the answer        phase 2's claim, answered yes or no
```

A `⬜` above marks an artifact this workflow requires and nothing on disk produces.

### 2 · When it is done
**The exit test**: every line must hold, and a `⬜` line is one that cannot be checked today.

```text
✔ every number names the round that produced it
✔ the audit stratum is reported separately from the challenge stratum, because they are not comparable
  ⬜ phase 2's claim is restated and answered
```

A phase with no exit test ends when someone feels finished, which is not a boundary a later reader can verify.

### 3 · The hands, and what each may never do
**A hand is named by what it may NEVER do**: the identity of each one is its boundary.

```text
disagreement-analyzer-agent   compares sealed predictions with the person's records and names the error strata
                              NEVER: may not decide a final class or a policy patch
🧠 the person                  reads, and answers phase 2's claim
```

`QF3-agent-topology` fixes the authority these hands hold across the whole workflow, and this page says only which of them act in phase 6.

### 4 · The person's job, and the trap
**Sees, does, and the trap**: the mistake a person naturally makes here belongs in the contract.

```text
sees   correction rate, agreement on the audit stratum, coverage per region, concept stability, and the answer to phase 2's claim
does   reads them and answers phase 2: was the reason we picked these
       items right?
trap   reading agreement as accuracy
       agreement on the stratum the models already agree about is the
       easiest number on the screen
trap   comparing challenge rounds to each other
       an adaptive challenge batch is chosen to be hard, so its
       series is not a loss curve
```

The cost of this phase to the person is recorded once, in `QLw00` division 1, and never restated here.

### 5 · Where it goes next
**The routes out**: each one names the condition that takes it.

```text
-> 7 NEXT?   the measurements exist
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
- ✅ A1.1 · Met; division 1 carries it.

### A2 · ✔️ When it is done
- ⬜ A2.1 · Not met; the marked line has no implementation.

### A3 · 🤖 The hands, and what each may never do
- ✅ A3.1 · Met; division 3 carries it.

### A4 · 🧠 The person's job, and the trap
- ✅ A4.1 · Met; division 4 carries it.

### A5 · 🚦 Where it goes next
- ✅ A5.1 · Met; division 5 carries it.

## Files

### Contracts · what this Page describes
- `../../agents/disagreement-analyzer-agent.md`
  The comparison auditor, which names strata and decides nothing.

## Law
- 260806 JL · 📊 Guideline quality is measured by transfer
      Absolute model performance, guideline uplift, held-out model transfer, region errors, and human consistency support the final claim.

## Glossary
- 📊 **NUMBERS**: phase 6 of eleven, which how often the person overrode the sealed guess.
- 📄 **Item**: one piece of text the person judges, of any kind.
- 🚦 **Route**: the named way out of this phase, and the condition that takes it.

## Log
260818 · Created QLw6 as one page per workflow phase, on JL's ruling that each step of the labeling workflow gets its own page.
