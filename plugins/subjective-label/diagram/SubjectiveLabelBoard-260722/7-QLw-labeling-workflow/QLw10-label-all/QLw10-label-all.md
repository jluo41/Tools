# LABEL ALL: the chosen executor finishes the corpus and sends the hard ones back
state: 🟡 PARTIAL · the move is settled · open: nothing bounds how large the risk queue may grow
owner: JL
method: Say what the phase leaves behind, when it is finished, whose hand does what, what the person does, and where the work may go next.

## Opening
How does the rest of the corpus get labeled, and what happens to the items the executor is not sure about?
The person's role changes here from teacher to on-call: they no longer build the policy, they answer the items it cannot resolve.
Every label must carry where it came from, because a corpus whose labels cannot be traced cannot be defended.

**Where this page sits**: This is phase 10 of eleven, and it belongs to the lifecycle rhythm; `QLw00` holds the whole sequence.
`QE3` argues corpus completion; this page owns the phase's timing, the risk queue, and the provenance requirement.

**Why it matters**: A label with no provenance is an assertion, and this phase produces most of the labels in the project.

**What is settled here**: What the phase produces, the exit test, the hands, and the trap on the queue.

**What remains open**: Nothing bounds the risk queue, so a low threshold can quietly hand the person more work than the calibration rounds cost.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**A phase page owns TIMING and AUTHORITY, never method.** `QE3-complete-corpus` argues how this step is done, and repeating it here creates a copy that goes out of date.
Write when it starts, when it is finished, who may act, and what each hand may never do.

**The unit is an ITEM, never the corpus this project happens to hold.** The eleven phases run the same on a clinical note or a transcript turn.

**The trap is part of the contract.** A phase that only says what to do cannot be checked against what went wrong.

**Language and sentences**: English only, in the source and in the render.
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes: use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

## Diagram
**Phase 10 in place**: what enters, what this phase makes of it, and where it may go.

```text
   🏭  PHASE 10  LABEL ALL   📆 once
   --------------------------------------------------------------
   makes   the labels     one per remaining item, under the frozen policy
   makes   the provenance per item: which executor, which policy version, which run
   makes   the risk queue the items routed back to the person

   then    -> 11 SPOT CHECK the corpus is complete
```

## Content

### 1 · What this phase produces
**What is on disk when this phase ends**: the artifact name is the method's word, and the sentence beside it is what it means.

```text
the labels       one per remaining item, under the frozen policy
the provenance   per item: which executor, which policy version, which run
the risk queue   the items routed back to the person
```

A `⬜` above marks an artifact this workflow requires and nothing on disk produces.

### 2 · When it is done
**The exit test**: every line must hold, and a `⬜` line is one that cannot be checked today.

```text
✔ every item in the corpus has a label with provenance, or sits in the queue
✔ the executor did not waive a threshold to empty the queue
✔ the person's answers on the queue are recorded as human gold, not as executor output
  ⬜ a bound on the risk queue, so a low threshold cannot hand the person more work than the rounds cost
```

A phase with no exit test ends when someone feels finished, which is not a boundary a later reader can verify.

### 3 · The hands, and what each may never do
**A hand is named by what it may NEVER do**: the identity of each one is its boundary.

```text
the chosen executor   writes attempts under the frozen policy
                      NEVER: may not waive a risk threshold
🧠 the person          answers the risk queue
```

`QF3-agent-topology` fixes the authority these hands hold across the whole workflow, and this page says only which of them act in phase 10.

### 4 · The person's job, and the trap
**Sees, does, and the trap**: the mistake a person naturally makes here belongs in the contract.

```text
sees   the risk queue, one item at a time
does   works the queue. The role changes from teacher to on-call.
trap   rubber-stamping when tired
       a tired yes on the queue is gold with nobody's judgment in it
trap   lowering the threshold to shorten the queue
       that moves uncertain items into the corpus silently rather
       than resolving them
```

The cost of this phase to the person is recorded once, in `QLw00` division 1, and never restated here.

### 5 · Where it goes next
**The routes out**: each one names the condition that takes it.

```text
-> 11 SPOT CHECK   the corpus is complete
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
- `../../skills/page-workflows/label-complete/SKILL.md`
  The command that runs completion and the audit.

## Law
- 260806 JL · 🧑 One human is the semantic authority
      Models may retrieve, pre-label, diagnose, and draft, but human confirmation creates gold and protects the construct's meaning.

## Glossary
- 🏭 **LABEL ALL**: phase 10 of eleven, which one per remaining item, under the frozen policy.
- 📄 **Item**: one piece of text the person judges, of any kind.
- 🚦 **Route**: the named way out of this phase, and the condition that takes it.

## Log
260818 · Created QLw10 as one page per workflow phase, on JL's ruling that each step of the labeling workflow gets its own page.
