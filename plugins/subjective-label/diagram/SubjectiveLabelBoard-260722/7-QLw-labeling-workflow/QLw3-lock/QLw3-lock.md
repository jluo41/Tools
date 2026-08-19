# LOCK: let the small models guess first, and make sure nobody can see it
state: 🟡 PARTIAL · the move is settled · open: no hash is written, so the seal is trusted rather than checked
owner: JL
method: Say what the phase leaves behind, when it is finished, whose hand does what, what the person does, and where the work may go next.

## Opening
What did the current policy already think about these items, and how is that kept away from the person until they have judged?
This is the only phase in the whole workflow defined by what may not be READ rather than by what it produces.
It exists so that the comparison between the policy and the person means something, which it cannot if the person saw the policy's answer first.

**Where this page sits**: This is phase 3 of eleven, and it belongs to the round rhythm; `QLw00` holds the whole sequence.
`QC2` argues how pre-labels are produced and sealed; this page owns the phase's timing and the access boundary that IS its exit test.

**Why it matters**: If the seal leaks, every number in phase 6 measures the person agreeing with a machine they were shown, and nothing later can detect it.

**What is settled here**: What the phase produces, the access boundary, the one hand, and why the person does nothing.

**What remains open**: No hash of the sealed file is written anywhere, so `was it sealed before the person saw it` is a matter of trust rather than a check.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**A phase page owns TIMING and AUTHORITY, never method.** `QC2-prelabel-and-seal` argues how this step is done, and repeating it here creates a copy that goes out of date.
Write when it starts, when it is finished, who may act, and what each hand may never do.

**The unit is an ITEM, never the corpus this project happens to hold.** The eleven phases run the same on a clinical note or a transcript turn.

**The trap is part of the contract.** A phase that only says what to do cannot be checked against what went wrong.

**Language and sentences**: English only, in the source and in the render.
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes: use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

## Diagram
**Phase 3 in place**: what enters, what this phase makes of it, and where it may go.

```text
   🔒  PHASE 3  LOCK   🔁 each round
   --------------------------------------------------------------
   makes   P_t            each weak executor's prediction, produced independently
   makes   the seal       the file exists and is unreadable by the session surface
   makes   the disagreement map which items the executors split on, used by phase 2 next round

   then    -> 4 LABEL     always, once the seal holds
```

## Content

### 1 · What this phase produces
**What is on disk when this phase ends**: the artifact name is the method's word, and the sentence beside it is what it means.

```text
P_t                    each weak executor's prediction, produced independently
the seal               the file exists and is unreadable by the session surface
the disagreement map   which items the executors split on, used by phase 2 next round
```

A `⬜` above marks an artifact this workflow requires and nothing on disk produces.

### 2 · When it is done
**The exit test**: every line must hold, and a `⬜` line is one that cannot be checked today.

```text
✔ P_t is written for every item in B_t
✔ each executor ran ALONE, under the closed G_(t-1), with no sight of another's answer
✔ the session surface cannot read P_t until the first-pass lock in phase 4
  ⬜ the file is hashed, so the seal is checkable and not merely claimed
```

A phase with no exit test ends when someone feels finished, which is not a boundary a later reader can verify.

### 3 · The hands, and what each may never do
**A hand is named by what it may NEVER do**: the identity of each one is its boundary.

```text
labeler-panel-agent   runs each registered weak executor independently and seals the output
                      NEVER: its consensus is NEVER gold
🧠 the person          nothing
                      NEVER: and this absence is the phase's whole content
```

`QF3-agent-topology` fixes the authority these hands hold across the whole workflow, and this page says only which of them act in phase 3.

### 4 · The person's job, and the trap
**Sees, does, and the trap**: the mistake a person naturally makes here belongs in the contract.

```text
sees   nothing
does   nothing
trap   peeking
       reading the guesses before judging contaminates every number
       downstream, and without a hash nobody can show later
       that it did not happen
```

The cost of this phase to the person is recorded once, in `QLw00` division 1, and never restated here.

### 5 · Where it goes next
**The routes out**: each one names the condition that takes it.

```text
-> 4 LABEL   always, once the seal holds
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
- `../../agents/labeler-panel-agent.md`
  The weak-executor committee, whose consensus is never gold.

## Law
- 260806 JL · 🙈 Pre-labels remain sealed during first-pass human judgment
      The pre-post comparison is meaningful only when committee predictions do not anchor the human label.

## Glossary
- 🔒 **LOCK**: phase 3 of eleven, which each weak executor's prediction, produced independently.
- 📄 **Item**: one piece of text the person judges, of any kind.
- 🚦 **Route**: the named way out of this phase, and the condition that takes it.

## Log
260818 · Created QLw3 as one page per workflow phase, on JL's ruling that each step of the labeling workflow gets its own page.
