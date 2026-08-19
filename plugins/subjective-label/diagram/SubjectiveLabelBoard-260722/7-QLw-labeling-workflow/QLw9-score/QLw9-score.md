# SCORE: run every candidate on the sealed test under one protocol
state: ✅ SETTLED · read-only by construction · the person does nothing here
owner: JL
method: Say what the phase leaves behind, when it is finished, whose hand does what, what the person does, and where the work may go next.

## Opening
Which executor should label the rest of the corpus, and how is that chosen without contaminating the test?
Every candidate runs the frozen policy on the sealed set under one protocol, and the scorecards decide.
The person does nothing here, and that is the point: a phase where the authority can intervene is a phase where the test stops being sealed.

**Where this page sits**: This is phase 9 of eleven, and it belongs to the lifecycle rhythm; `QLw00` holds the whole sequence.
`QE2` argues the scorecards; this page owns the phase's timing and the read-only boundary that is its exit test.

**Why it matters**: A protocol changed after a score is seen turns an evaluation into a selection of the answer you wanted.

**What is settled here**: What the phase produces, the read-only boundary, the one hand, and why the person is absent.

**What remains open**: Nothing here is open. This phase is the most constrained in the workflow and the constraint is what makes it work.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**A phase page owns TIMING and AUTHORITY, never method.** `QE2-model-scorecard` argues how this step is done, and repeating it here creates a copy that goes out of date.
Write when it starts, when it is finished, who may act, and what each hand may never do.

**The unit is an ITEM, never the corpus this project happens to hold.** The eleven phases run the same on a clinical note or a transcript turn.

**The trap is part of the contract.** A phase that only says what to do cannot be checked against what went wrong.

**Language and sentences**: English only, in the source and in the render.
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes: use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

## Diagram
**Phase 9 in place**: what enters, what this phase makes of it, and where it may go.

```text
   🏁  PHASE 9  SCORE   📆 once
   --------------------------------------------------------------
   makes   the predictions frozen, one set per candidate executor
   makes   the scorecards absolute, uplift over baseline, per class, per region, stability, and cost
   makes   the choice     which executor labels the corpus

   then    -> 10 LABEL ALL an executor was selected
```

## Content

### 1 · What this phase produces
**What is on disk when this phase ends**: the artifact name is the method's word, and the sentence beside it is what it means.

```text
the predictions   frozen, one set per candidate executor
the scorecards    absolute, uplift over baseline, per class, per region, stability, and cost
the choice        which executor labels the corpus
```

A `⬜` above marks an artifact this workflow requires and nothing on disk produces.

### 2 · When it is done
**The exit test**: every line must hold, and a `⬜` line is one that cannot be checked today.

```text
✔ every candidate ran the SAME protocol on the SAME sealed set
✔ the metrics and the selection rule were fixed BEFORE any score was seen
✔ G*, T*, the wrappers and the selection rules were not modified during this phase
```

A phase with no exit test ends when someone feels finished, which is not a boundary a later reader can verify.

### 3 · The hands, and what each may never do
**A hand is named by what it may NEVER do**: the identity of each one is its boundary.

```text
validator-agent       runs the frozen evaluation and writes the scorecards
                      NEVER: may not modify G*, T*, wrappers, candidates, or selection rules
labeler-panel-agent   supplies the weak executors as candidates
                      NEVER: may not see the gold
classifier-agent      may compete as a candidate, if it was trained on confirmed gold only
                      NEVER: may not train on model consensus
🧠 the person          nothing
```

`QF3-agent-topology` fixes the authority these hands hold across the whole workflow, and this page says only which of them act in phase 9.

### 4 · The person's job, and the trap
**Sees, does, and the trap**: the mistake a person naturally makes here belongs in the contract.

```text
sees   scorecards
does   nothing
trap   changing the protocol after seeing a score
       this is the failure the seal exists to prevent, and it is
       invisible afterwards
```

The cost of this phase to the person is recorded once, in `QLw00` division 1, and never restated here.

### 5 · Where it goes next
**The routes out**: each one names the condition that takes it.

```text
-> 10 LABEL ALL   an executor was selected
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
- ✅ A2.1 · Met; division 2 carries it.

### A3 · 🤖 The hands, and what each may never do
- ✅ A3.1 · Met; division 3 carries it.

### A4 · 🧠 The person's job, and the trap
- ✅ A4.1 · Met; division 4 carries it.

### A5 · 🚦 Where it goes next
- ✅ A5.1 · Met; division 5 carries it.

## Files

### Contracts · what this Page describes
- `../../agents/validator-agent.md`
  The sealed Final Evaluator, read-only over G* and T*.
- `../../agents/classifier-agent.md`
  An optional candidate, trained on human-confirmed gold only.

## Law
- 260806 JL · 🔐 Human decision, model evidence, policy proposal, canonical write, and evaluation are separate authorities
      No agent may turn its own prediction or proposal into human gold or approve a changed system on the same final test.

## Glossary
- 🏁 **SCORE**: phase 9 of eleven, which frozen, one set per candidate executor.
- 📄 **Item**: one piece of text the person judges, of any kind.
- 🚦 **Route**: the named way out of this phase, and the condition that takes it.

## Log
260818 · Created QLw9 as one page per workflow phase, on JL's ruling that each step of the labeling workflow gets its own page.
