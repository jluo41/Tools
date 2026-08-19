# LABEL: the person judges, and only the person's judgment is gold
state: 🟡 PARTIAL · the move is settled · open: no receipt, so an interrupted session cannot resume honestly
owner: JL
method: Say what the phase leaves behind, when it is finished, whose hand does what, what the person does, and where the work may go next.

## Opening
What happens in the one phase that spends the person's hours, and what is produced that no machine could have produced?
This phase holds roughly 85 percent of the person's time, and every other phase in the workflow exists to choose what it looks at or to harvest what it made.
It runs in two halves: a blind first pass, then the reveal of what the small models had guessed.

**Where this page sits**: This is phase 4 of eleven, and it belongs to the round rhythm; `QLw00` holds the whole sequence.
`QB2` argues the session as an interaction and `QC4` argues blind adjudication; this page owns the phase's timing, its two halves, and the lock between them.

**Why it matters**: Everything downstream is derived. This is the only phase that creates evidence rather than moving it.

**What is settled here**: The three records per item, the two halves and the lock, the hands, and the two traps.

**What remains open**: Nothing records which items the person has already seen, so an interrupted session resumes by memory. That contract is `QLw00` division 4 and it has no implementation.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**A phase page owns TIMING and AUTHORITY, never method.** `QB2-human-ai-session` argues how this step is done, and repeating it here creates a copy that goes out of date.
Write when it starts, when it is finished, who may act, and what each hand may never do.

**The unit is an ITEM, never the corpus this project happens to hold.** The eleven phases run the same on a clinical note or a transcript turn.

**The trap is part of the contract.** A phase that only says what to do cannot be checked against what went wrong.

**Language and sentences**: English only, in the source and in the render.
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes: use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

## Diagram
**Phase 4 in place**: what enters, what this phase makes of it, and where it may go.

```text
   🧠  PHASE 4  LABEL   🔁 each round
   --------------------------------------------------------------
   makes   the class      HIGH, LOW or NONE, per item
   makes   the region     one of the seven, per item, and `none of these fit` is DATA
   makes   the uncertainty a third field, never folded into the class
   makes   the reason     one sentence in the person's own words, which phase 5 turns into rules
   makes   the lock       a timestamp separating the blind first pass from the reveal

   then    -> 5 RULES     every item judged or HELD
```

## Content

### 1 · What this phase produces
**What is on disk when this phase ends**: the artifact name is the method's word, and the sentence beside it is what it means.

```text
the class         HIGH, LOW or NONE, per item
the region        one of the seven, per item, and `none of these fit` is DATA
the uncertainty   a third field, never folded into the class
the reason        one sentence in the person's own words, which phase 5 turns into rules
the lock          a timestamp separating the blind first pass from the reveal
```

A `⬜` above marks an artifact this workflow requires and nothing on disk produces.

### 2 · When it is done
**The exit test**: every line must hold, and a `⬜` line is one that cannot be checked today.

```text
✔ every item in B_t has a class, a region, and an uncertainty, or is explicitly HELD
✔ the first-pass lock has a time on it, and the reveal happened after it
✔ every changed mind is recorded AS a change, with the reason that changed it
  ⬜ a receipt names which items were seen, so resuming re-shows none and skips none
```

A phase with no exit test ends when someone feels finished, which is not a boundary a later reader can verify.

### 3 · The hands, and what each may never do
**A hand is named by what it may NEVER do**: the identity of each one is its boundary.

```text
moderator-agent        presents items, elicits reasons, protects the blind period, warns on drift
                       NEVER: may not disclose P_t before the lock, and may not auto-confirm a ruling
🧠 the person           decides the class, the region, the uncertainty, and the reason
                       NEVER: nothing else in the system creates gold
gallery-keeper-agent   later writes what the person confirmed
                       NEVER: may not write anything the person did not confirm
```

`QF3-agent-topology` fixes the authority these hands hold across the whole workflow, and this page says only which of them act in phase 4.

### 4 · The person's job, and the trap
**Sees, does, and the trap**: the mistake a person naturally makes here belongs in the contract.

```text
sees   one item, verbatim, with its id, and nothing else on the first pass
does   the class, the region, how sure, and WHY in one sentence. Then the
       reveal: where the small models disagreed, and the person
       either changes their mind (recorded AS a change) or says
       why the models are wrong, which becomes a rule.
trap   staying consistent with a half-remembered rule
       judge honestly and let the contradiction surface; catching it
       is the machine's job
trap   "it's obvious" as a reason
       a reason that cannot generalize is not a reason, and phase 5
       has nothing to build from it
```

The cost of this phase to the person is recorded once, in `QLw00` division 1, and never restated here.

### 5 · Where it goes next
**The routes out**: each one names the condition that takes it.

```text
-> 5 RULES   every item judged or HELD
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
  The only human-facing hand, which protects the blind period.
- `../../agents/gallery-keeper-agent.md`
  The single writer of confirmed gold.

## Law
- 260806 JL · 🧑 One human is the semantic authority
      Models may retrieve, pre-label, diagnose, and draft, but human confirmation creates gold and protects the construct's meaning.
- 260806 JL · 🗺 Class and region are separate annotations
      Every reviewed item receives H, L, or N plus one of seven diagnostic regions, while uncertainty remains a third field.

## Glossary
- 🧠 **LABEL**: phase 4 of eleven, which HIGH, LOW or NONE, per item.
- 📄 **Item**: one piece of text the person judges, of any kind.
- 🚦 **Route**: the named way out of this phase, and the condition that takes it.

## Log
260818 · Created QLw4 as one page per workflow phase, on JL's ruling that each step of the labeling workflow gets its own page.
