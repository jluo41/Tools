# FREEZE: the person signs, the policy stops moving, and the job's page closes
state: 🟡 PARTIAL · the move is settled · open: the tick has no surface and no zero-findings precondition
owner: JL
method: Say what the phase leaves behind, when it is finished, whose hand does what, what the person does, and where the work may go next.

## Opening
What does it mean for the policy to be finished, and who is allowed to say so?
This is the tick that ends the job, and by JL's 260818 ruling it is the LAST one and it is accept-biased.
A person is asked to sign only after every finding a machine could compute is already zero, so the signature is about meaning and never about defects.

**Where this page sits**: This is phase 8 of eleven, and it belongs to the lifecycle rhythm; `QLw00` holds the whole sequence.
`QE1` argues the sealed final test; this page owns the signature, its precondition, and the fact that this tick closes the run page.

**Why it matters**: `haipipe-page-for-labeling` says it outright: a page's state reads ✅ because a person signed the freeze, never because the rounds went well.

**What is settled here**: What freezes, who signs, the accept-biased precondition, and the trap.

**What remains open**: The tick has no surface, and nothing computes the findings that are supposed to be zero before it is offered.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**A phase page owns TIMING and AUTHORITY, never method.** `QE1-sealed-final-test` argues how this step is done, and repeating it here creates a copy that goes out of date.
Write when it starts, when it is finished, who may act, and what each hand may never do.

**The unit is an ITEM, never the corpus this project happens to hold.** The eleven phases run the same on a clinical note or a transcript turn.

**The trap is part of the contract.** A phase that only says what to do cannot be checked against what went wrong.

**Language and sentences**: English only, in the source and in the render.
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes: use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

## Diagram
**Phase 8 in place**: what enters, what this phase makes of it, and where it may go.

```text
   🧊  PHASE 8  FREEZE   📆 once
   --------------------------------------------------------------
   makes   G*             the frozen policy, which no later phase may edit
   makes   T*             the sealed test set, which now receives human gold
   makes   the signature  the person's freeze tick, which closes the run page

   then    -> 9 SCORE     the freeze is signed
```

## Content

### 1 · What this phase produces
**What is on disk when this phase ends**: the artifact name is the method's word, and the sentence beside it is what it means.

```text
G*              the frozen policy, which no later phase may edit
T*              the sealed test set, which now receives human gold
the signature   the person's freeze tick, which closes the run page
```

A `⬜` above marks an artifact this workflow requires and nothing on disk produces.

### 2 · When it is done
**The exit test**: every line must hold, and a `⬜` line is one that cannot be checked today.

```text
✔ 🧠 the person signed, and the signature names the policy version it signed
✔ the sealed set was chosen on a boundary that already existed in the data, so `was the test read` is checkable in a manifest
  ⬜ every computed finding was zero BEFORE the person was asked
```

A phase with no exit test ends when someone feels finished, which is not a boundary a later reader can verify.

### 3 · The hands, and what each may never do
**A hand is named by what it may NEVER do**: the identity of each one is its boundary.

```text
🧠 the person           reads the final guideline as a stranger would, and signs
                       NEVER: no agent may write this tick
gallery-keeper-agent   records the freeze
                       NEVER: may not sign it
validator-agent        receives G* and T* as read-only inputs
                       NEVER: may not modify either, ever
```

`QF3-agent-topology` fixes the authority these hands hold across the whole workflow, and this page says only which of them act in phase 8.

### 4 · The person's job, and the trap
**Sees, does, and the trap**: the mistake a person naturally makes here belongs in the contract.

```text
sees   the final guideline, and every computed check already at zero
does   reads it as a STRANGER would and answers one question: could
       someone who has never met me follow this?
trap   signing because the rounds went well
       state ✅ means a person signed the freeze, never that the
       numbers looked good
trap   treating silence as consent
       an unticked tick is unticked, and no elapsed time converts it
```

The cost of this phase to the person is recorded once, in `QLw00` division 1, and never restated here.

### 5 · Where it goes next
**The routes out**: each one names the condition that takes it.

```text
-> 9 SCORE   the freeze is signed
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
- `../../skills/label-scanning/SKILL.md`
  The command that runs the freeze and the scoring.
- `../../skills/page-types/haipipe-page-for-labeling/SKILL.md`
  The Page Type whose ✅ means this signature happened.

## Law
- 260818 JL · ✋ The human gate is LAST and accept-biased
      A person is asked to sign only after every computed finding is zero, so the signature is about meaning and never about defects a machine could have caught.
- 260806 JL · 🔒 Final evaluation uses a sealed unseen test
      Test items remain outside development, receive human gold after G* freezes, and score each candidate executor under one protocol.

## Glossary
- 🧊 **FREEZE**: phase 8 of eleven, which the frozen policy, which no later phase may edit.
- 📄 **Item**: one piece of text the person judges, of any kind.
- 🚦 **Route**: the named way out of this phase, and the condition that takes it.

## Log
260818 · Created QLw8 as one page per workflow phase, on JL's ruling that each step of the labeling workflow gets its own page.
