# SPOT CHECK: judge a fresh sample blind, then find out what the machine said
state: 🟡 PARTIAL · the move is settled · open: no rule says what failure rate reopens scope
owner: JL
method: Say what the phase leaves behind, when it is finished, whose hand does what, what the person does, and where the work may go next.

## Opening
Is the finished corpus reliable, and which parts of it are not?
The person judges a fresh independent sample without seeing the machine's answer, and only then compares.
The order is the whole method: seeing the label first turns an audit into a measurement of how agreeable the person is.

**Where this page sits**: This is phase 11 of eleven, and it belongs to the lifecycle rhythm; `QLw00` holds the whole sequence.
`QE4` argues the final audit and provenance package; this page owns the phase's timing, its blind order, and what a failure reopens.

**Why it matters**: This is the only statement the project can make about reliability that was not produced by the system being judged.

**What is settled here**: What the phase produces, the blind order as its exit test, the hands, and the trap.

**What remains open**: No rule states what disagreement rate reopens scope, so a bad audit today has no defined consequence.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**A phase page owns TIMING and AUTHORITY, never method.** `QE4-final-audit-and-provenance` argues how this step is done, and repeating it here creates a copy that goes out of date.
Write when it starts, when it is finished, who may act, and what each hand may never do.

**The unit is an ITEM, never the corpus this project happens to hold.** The eleven phases run the same on a clinical note or a transcript turn.

**The trap is part of the contract.** A phase that only says what to do cannot be checked against what went wrong.

**Language and sentences**: English only, in the source and in the render.
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes: use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

## Diagram
**Phase 11 in place**: what enters, what this phase makes of it, and where it may go.

```text
   🔍  PHASE 11  SPOT CHECK   📆 once
   --------------------------------------------------------------
   makes   the sample     drawn independently, with inclusion probabilities
   makes   the blind judgments the person's calls, made before any machine label was shown
   makes   the statement  what is reliable, what is not, and for which regions

   then    -> done        the audit holds
   then    -> 2 PICK      the audit failed and the affected scope reopens
```

## Content

### 1 · What this phase produces
**What is on disk when this phase ends**: the artifact name is the method's word, and the sentence beside it is what it means.

```text
the sample            drawn independently, with inclusion probabilities
the blind judgments   the person's calls, made before any machine label was shown
the statement         what is reliable, what is not, and for which regions
```

A `⬜` above marks an artifact this workflow requires and nothing on disk produces.

### 2 · When it is done
**The exit test**: every line must hold, and a `⬜` line is one that cannot be checked today.

```text
✔ the person judged EVERY sampled item before seeing any machine label
✔ the sample was drawn by a hand that did not produce the labels being audited
  ⬜ a stated failure rate reopens the affected scope rather than being reported and filed
```

A phase with no exit test ends when someone feels finished, which is not a boundary a later reader can verify.

### 3 · The hands, and what each may never do
**A hand is named by what it may NEVER do**: the identity of each one is its boundary.

```text
gallery-keeper-agent   draws the independent sample and records the findings
                       NEVER: may not draw it from what it already wrote
🧠 the person           judges blind, then compares
validator-agent        may not approve a system it scored
```

`QF3-agent-topology` fixes the authority these hands hold across the whole workflow, and this page says only which of them act in phase 11.

### 4 · The person's job, and the trap
**Sees, does, and the trap**: the mistake a person naturally makes here belongs in the contract.

```text
sees   a fresh sample, one item at a time, with no machine label attached
does   judges them blind, THEN compares
trap   looking at the machine's label first
       if it is seen, the audit measures agreeableness, not the
       system
trap   reporting a failure without reopening anything
       an audit whose failure has no consequence is a report, not a
       gate
```

The cost of this phase to the person is recorded once, in `QLw00` division 1, and never restated here.

### 5 · Where it goes next
**The routes out**: each one names the condition that takes it.

```text
-> done     the audit holds
-> 2 PICK   the audit failed and the affected scope reopens
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
- `../../agents/gallery-keeper-agent.md`
  The audit keeper, which samples independently and reopens scope when acceptance fails.

## Law
- 260806 JL · 🔐 Human decision, model evidence, policy proposal, canonical write, and evaluation are separate authorities
      No agent may turn its own prediction or proposal into human gold or approve a changed system on the same final test.

## Glossary
- 🔍 **SPOT CHECK**: phase 11 of eleven, which drawn independently, with inclusion probabilities.
- 📄 **Item**: one piece of text the person judges, of any kind.
- 🚦 **Route**: the named way out of this phase, and the condition that takes it.

## Log
260818 · Created QLw11 as one page per workflow phase, on JL's ruling that each step of the labeling workflow gets its own page.
