# START: turn a vague idea into a first guideline by reacting to items
state: 🟡 PARTIAL · the move is settled · open: nothing on disk decides when G_0 is good enough
owner: JL
method: Say what the phase leaves behind, when it is finished, whose hand does what, what the person does, and where the work may go next.

## Opening
How does a labeling job begin when the target is still a vague idea and nothing in the corpus is labeled?
The person cannot write a definition of something they have not looked at, and the machine cannot propose one without a judgment to learn from.
This phase breaks that circle by putting about fifteen random items in front of the person and building the first guideline out of their reactions.

**Where this page sits**: This is phase 1 of eleven, and it belongs to the lifecycle rhythm; `QLw00` holds the whole sequence.
`QB1` argues the method of a first round and `QA2` argues what a class and a region are; this page owns the phase's timing, its exit test, and its hands.

**Why it matters**: A first guideline written from an armchair is a definition of a different construct, and every later round inherits it.

**What is settled here**: What the phase produces, its exit test, the three hands, the person's job, and the one route out.

**What remains open**: Nothing on disk decides when `G_0` is good enough to leave this phase, so today the exit is the person's feeling.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**A phase page owns TIMING and AUTHORITY, never method.** `QB1-initialize-round-one` argues how this step is done, and repeating it here creates a copy that goes out of date.
Write when it starts, when it is finished, who may act, and what each hand may never do.

**The unit is an ITEM, never the corpus this project happens to hold.** The eleven phases run the same on a clinical note or a transcript turn.

**The trap is part of the contract.** A phase that only says what to do cannot be checked against what went wrong.

**Language and sentences**: English only, in the source and in the render.
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes: use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

## Diagram
**Phase 1 in place**: what enters, what this phase makes of it, and where it may go.

```text
   🎬  PHASE 1  START   📆 once
   --------------------------------------------------------------
   makes   the target     one trait, named, on one corpus
   makes   the meaning    what HIGH, LOW and NONE mean for THIS target
   makes   the regions    the seven diagnostic regions, named
   makes   G_0            the first annotation policy, which will be wrong
   makes   ~15 judgments  drawn at random, with reasons in the person's words

   then    -> 2 PICK      always, once G_0 exists
```

## Content

### 1 · What this phase produces
**What is on disk when this phase ends**: the artifact name is the method's word, and the sentence beside it is what it means.

```text
the target      one trait, named, on one corpus
the meaning     what HIGH, LOW and NONE mean for THIS target
the regions     the seven diagnostic regions, named
G_0             the first annotation policy, which will be wrong
~15 judgments   drawn at random, with reasons in the person's words
```

A `⬜` above marks an artifact this workflow requires and nothing on disk produces.

### 2 · When it is done
**The exit test**: every line must hold, and a `⬜` line is one that cannot be checked today.

```text
✔ a person can restate what HIGH means without reading the session transcript
✔ the first items were drawn at RANDOM, with no prior labels, regions, or prototypes
✔ `G_0` exists as a file, not as a conversation
  ⬜ a stated test decides when `G_0` is good enough to leave this phase
```

A phase with no exit test ends when someone feels finished, which is not a boundary a later reader can verify.

### 3 · The hands, and what each may never do
**A hand is named by what it may NEVER do**: the identity of each one is its boundary.

```text
sampler-agent     draws the random first items
                  NEVER: may not choose them by a score, because no score exists yet
moderator-agent   drafts the meaning FROM the person's reactions
                  NEVER: may not propose the definition first
🧠 the person      rules on every word of the meaning
                  NEVER: this is the one thing no agent may do
```

`QF3-agent-topology` fixes the authority these hands hold across the whole workflow, and this page says only which of them act in phase 1.

### 4 · The person's job, and the trap
**Sees, does, and the trap**: the mistake a person naturally makes here belongs in the contract.

```text
sees   about 15 items, drawn at random, and nothing else
does   reacts: yes, no, not sure. The agent drafts what HIGH means FROM
       those reactions, and the person corrects the draft.
trap   writing the definition before looking at items
       the method assumes the concept is vague, so a definition
       written cold is a definition of something else
```

The cost of this phase to the person is recorded once, in `QLw00` division 1, and never restated here.

### 5 · Where it goes next
**The routes out**: each one names the condition that takes it.

```text
-> 2 PICK   always, once G_0 exists
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
- `../../skills/page-workflows/label-init/SKILL.md`
  The command that runs this phase.
- `../../agents/moderator-agent.md`
  The hand that drafts the meaning and never decides it.
- `../../agents/sampler-agent.md`
  The hand that draws the random first items.

## Law
- 260806 JL · 🎲 Round 1 begins with a random small batch
      The first 50 to 60 items have no prior labels or regions, and the first labels, seven-region assignments, reasons, and guideline draft emerge together through dialogue.

## Glossary
- 🎬 **START**: phase 1 of eleven, which one trait, named, on one corpus.
- 📄 **Item**: one piece of text the person judges, of any kind.
- 🚦 **Route**: the named way out of this phase, and the condition that takes it.

## Log
260818 · Created QLw1 as one page per workflow phase, on JL's ruling that each step of the labeling workflow gets its own page.
