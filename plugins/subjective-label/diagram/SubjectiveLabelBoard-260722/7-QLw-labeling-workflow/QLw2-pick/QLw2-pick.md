# PICK: choose what the person will spend their hours on, and say why
state: 🟡 PARTIAL · the move is settled · open: the approved: tick has no surface
owner: JL
method: Say what the phase leaves behind, when it is finished, whose hand does what, what the person does, and where the work may go next.

## Opening
Out of a corpus with no labels, which items should the person look at next, and on what claim?
Selection is where the whole job's cost is decided, because everything after it is spent on whatever this phase chose.
The reason for the choice is a claim about the corpus, so it must be written before the round runs and answered after it.

**Where this page sits**: This is phase 2 of eleven, and it belongs to the round rhythm; `QLw00` holds the whole sequence.
`QC1` argues how a candidate pool is built and `QC3` argues how a batch is composed; this page owns the phase's timing, its exit test, and the tick that ends it.

**Why it matters**: This is the only cheap veto in the round: ten seconds here decides one to three hours in phase 4.

**What is settled here**: What the phase produces, its exit test, the three hands, the person's job, and the two routes out.

**What remains open**: The `approved:` tick has no surface, so today the batch is composed and used with nothing recording that a person agreed to it.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**A phase page owns TIMING and AUTHORITY, never method.** `QC1-candidate-pool` argues how this step is done, and repeating it here creates a copy that goes out of date.
Write when it starts, when it is finished, who may act, and what each hand may never do.

**The unit is an ITEM, never the corpus this project happens to hold.** The eleven phases run the same on a clinical note or a transcript turn.

**The trap is part of the contract.** A phase that only says what to do cannot be checked against what went wrong.

**Language and sentences**: English only, in the source and in the render.
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes: use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

## Diagram
**Phase 2 in place**: what enters, what this phase makes of it, and where it may go.

```text
   🔎  PHASE 2  PICK   🔁 each round
   --------------------------------------------------------------
   makes   C_t            the candidate pool, broad, with why each item was pulled
   makes   B_t            the human batch manifest, composed from C_t
   makes   the claim      the reason this batch was chosen, in checkable words
   makes   the strata     challenge items, stratified consensus audit, and random audit

   then    -> 3 LOCK      the manifest was approved
   then    -> 2 PICK      the person refused it, and selection runs again
```

## Content

### 1 · What this phase produces
**What is on disk when this phase ends**: the artifact name is the method's word, and the sentence beside it is what it means.

```text
C_t          the candidate pool, broad, with why each item was pulled
B_t          the human batch manifest, composed from C_t
the claim    the reason this batch was chosen, in checkable words
the strata   challenge items, stratified consensus audit, and random audit
```

A `⬜` above marks an artifact this workflow requires and nothing on disk produces.

### 2 · When it is done
**The exit test**: every line must hold, and a `⬜` line is one that cannot be checked today.

```text
✔ 🧠 a person's `approved:` on the manifest, BEFORE any human time is spent
✔ every item carries its inclusion probability, so the audit stratum stays a probability sample
✔ the asked-once MATCH ran against cumulative gold D_(t-1), so no near-duplicate is bought twice
✔ the claim is checkable: `region 5 is thin` can be answered in phase 6, `get more data` cannot
  ⬜ the `approved:` tick lands on a surface, so the agreement is recorded and countable
```

A phase with no exit test ends when someone feels finished, which is not a boundary a later reader can verify.

### 3 · The hands, and what each may never do
**A hand is named by what it may NEVER do**: the identity of each one is its boundary.

```text
embedder-agent   vectors, neighbourhoods, distances
                 NEVER: may not assign a label or inherit one from a neighbour
sampler-agent    composes C_t and the B_t manifest
                 NEVER: may not assign gold
prober-agent     suggests boundary contrasts and thin rules
                 NEVER: may add selection features and never chooses gold
🧠 the person     approves the manifest, or refuses it
```

`QF3-agent-topology` fixes the authority these hands hold across the whole workflow, and this page says only which of them act in phase 2.

### 4 · The person's job, and the trap
**Sees, does, and the trap**: the mistake a person naturally makes here belongs in the contract.

```text
sees   one screen: how many items, from which strata, and WHY
does   believes the WHY, or refuses it. Ten seconds.
trap   rubber-stamping
       this is the only cheap veto in the round; after it, the
       machine spends the person's hours
trap   a claim that cannot be answered
       a reason phase 6 cannot check is a reason that will never be
       wrong, which makes the round unfailable
```

The cost of this phase to the person is recorded once, in `QLw00` division 1, and never restated here.

### 5 · Where it goes next
**The routes out**: each one names the condition that takes it.

```text
-> 3 LOCK   the manifest was approved
-> 2 PICK   the person refused it, and selection runs again
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
- `../../agents/sampler-agent.md`
  The hand that composes C_t and B_t.
- `../../agents/embedder-agent.md`
  Vectors and neighbourhoods, with no label authority.
- `../../agents/prober-agent.md`
  Optional contrasts, which may add features and never choose gold.

## Law
- 260806 JL · 🔎 Later rounds use a broad candidate pool before a human batch
      Region-conditioned retrieval creates C_t, committee pre-labeling partitions it, and only the composed B_t enters Human-AI review.
- 260806 JL · 🎲 Consensus is audited rather than trusted as gold
      Disagreement receives priority, while a stratified random sample of unanimous predictions still enters human review.

## Glossary
- 🔎 **PICK**: phase 2 of eleven, which the candidate pool, broad, with why each item was pulled.
- 📄 **Item**: one piece of text the person judges, of any kind.
- 🚦 **Route**: the named way out of this phase, and the condition that takes it.

## Log
260818 · Created QLw2 as one page per workflow phase, on JL's ruling that each step of the labeling workflow gets its own page.
