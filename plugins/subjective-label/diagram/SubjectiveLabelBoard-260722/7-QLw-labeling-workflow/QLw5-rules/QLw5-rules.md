# RULES: turn what the person said into rules a stranger could follow
state: 🟡 PARTIAL · the move is settled · open: the regression exit test has no runner on disk
owner: JL
method: Say what the phase leaves behind, when it is finished, whose hand does what, what the person does, and where the work may go next.

## Opening
How do one person's sentences about particular items become a written policy that a weak model and a stranger can both follow?
The person's reasons are specific and the policy must be general, and closing that gap is the only work this phase does.
A rule that covers only the item that produced it is a casebook entry, and calling it a rule is how a policy silently stops generalizing.

**Where this page sits**: This is phase 5 of eleven, and it belongs to the round rhythm; `QLw00` holds the whole sequence.
`QD1` argues how the guideline is optimized and `QA3` argues what an annotation policy contains; this page owns the phase's timing, its exit test, and who may accept a rule.

**Why it matters**: The policy is the transferable output. The labels stay behind; the rules are what a weak executor will actually run.

**What is settled here**: What the phase produces, the exit test, the separation between drafting and accepting, and the two traps.

**What remains open**: Nothing on disk runs the regression set, so `a weak model follows the built guideline` is asserted rather than measured.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**A phase page owns TIMING and AUTHORITY, never method.** `QD1-optimize-guideline` argues how this step is done, and repeating it here creates a copy that goes out of date.
Write when it starts, when it is finished, who may act, and what each hand may never do.

**The unit is an ITEM, never the corpus this project happens to hold.** The eleven phases run the same on a clinical note or a transcript turn.

**The trap is part of the contract.** A phase that only says what to do cannot be checked against what went wrong.

**Language and sentences**: English only, in the source and in the render.
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes: use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

## Diagram
**Phase 5 in place**: what enters, what this phase makes of it, and where it may go.

```text
   📜  PHASE 5  RULES   🔁 each round
   --------------------------------------------------------------
   makes   G_t draft      the core guideline, boundary rules, the ordered decision procedure, the uncertainty and escalation policy, and a compact casebook
   makes   the citations  every rule naming the ITEM IDS that forced it
   makes   the regression set the items a later round must still get right
   makes   the backward impact which past gold labels this rule would flip

   then    -> 6 NUMBERS   the draft closed
```

## Content

### 1 · What this phase produces
**What is on disk when this phase ends**: the artifact name is the method's word, and the sentence beside it is what it means.

```text
G_t draft             the core guideline, boundary rules, the ordered decision procedure, the uncertainty and escalation policy, and a compact casebook
the citations         every rule naming the ITEM IDS that forced it
the regression set    the items a later round must still get right
the backward impact   which past gold labels this rule would flip
```

A `⬜` above marks an artifact this workflow requires and nothing on disk produces.

### 2 · When it is done
**The exit test**: every line must hold, and a `⬜` line is one that cannot be checked today.

```text
✔ every rule cites at least one item id, so a rule with no evidence cannot enter
✔ the backward-impact list was shown to the person and each flip was ruled on
✔ the DRAFTER did not accept its own rule
  ⬜ a weak model reproduces the person's calls on the regression set, using the BUILT guideline
```

A phase with no exit test ends when someone feels finished, which is not a boundary a later reader can verify.

### 3 · The hands, and what each may never do
**A hand is named by what it may NEVER do**: the identity of each one is its boundary.

```text
moderator-agent        drafts the smallest general patch, the wrapper changes, and the regression set
                       NEVER: may not accept its own semantic patch
🧠 the person           accepts, rejects, or narrows each rule
                       NEVER: this is a semantic ruling and no agent may make it
gallery-keeper-agent   closes the accepted version
                       NEVER: may not close a version whose human acceptance is missing
```

`QF3-agent-topology` fixes the authority these hands hold across the whole workflow, and this page says only which of them act in phase 5.

### 4 · The person's job, and the trap
**Sees, does, and the trap**: the mistake a person naturally makes here belongs in the contract.

```text
sees   proposed rules, each with the item ids that forced it, and the past labels this rule would flip
does   accept, reject, or narrow, one rule at a time
trap   accepting a rule that restates one item
       a rule covering only its own example is a casebook entry, not
       a rule
trap   letting a new rule silently break an old label
       every flip is a question: was the old call wrong, or is the
       rule too wide?
```

The cost of this phase to the person is recorded once, in `QLw00` division 1, and never restated here.

### 5 · Where it goes next
**The routes out**: each one names the condition that takes it.

```text
-> 6 NUMBERS   the draft closed
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
- `../../agents/moderator-agent.md`
  The hand that drafts a patch and may never accept it.
- `../../agents/gallery-keeper-agent.md`
  The single writer of closed policy versions.

## Law
- 260806 JL · 📜 The learned object is a structured annotation policy
      The core guideline, boundary rules, decision procedure, uncertainty policy, and compact casebook are optimized together.
- 260806 JL · 🧠 Human concept and guideline co-adapt
      Clarification is allowed, concept revision triggers backward review, and model convenience cannot override human meaning.

## Glossary
- 📜 **RULES**: phase 5 of eleven, which the core guideline, boundary rules, the ordered decision procedure, the uncertainty and escalation policy, and a compact casebook.
- 📄 **Item**: one piece of text the person judges, of any kind.
- 🚦 **Route**: the named way out of this phase, and the condition that takes it.

## Log
260818 · Created QLw5 as one page per workflow phase, on JL's ruling that each step of the labeling workflow gets its own page.
