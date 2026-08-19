# The gate: the five ticks a machine may never write
state: 🟡 PARTIAL · the five ticks are named · open: no surface joins them, and nothing computes the findings
owner: JL
method: Collect every mark that only a person may write onto one surface, state the precondition that opens it, and refuse every substitute for an actual tick.

## Opening
Which marks in this whole workflow may only a person write, and where does that person see them?
Five of them exist, spread across five phases and five different pages, and no surface joins them.
A person cannot see what they have signed, and a machine cannot count what is still unsigned.

**Where this page sits**: `QLw1` to `QLw11` each name the tick that falls in their phase.
This page owns the surface those ticks land on, the precondition that opens it, and what silence does not mean.
A letter rather than a digit means this page is not a phase.

**Why it matters**: The whole method rests on one human being the semantic authority, and a system that cannot show what that human actually signed has no way to prove it.

**What is settled here**: The five ticks, the accept-biased precondition, and the three substitutes that are refused.

**What remains open**: There is no surface, and nothing computes the findings that must be zero before a tick is offered.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**A tick is a mark, not a mood.** Write what is stored, where, and by whom, and never write that someone "agreed" without saying what was written down.

**Say what silence does NOT mean.** Every rule here has a false version that looks reasonable, and stating the false version is what makes the true one checkable.

**Language and sentences**: English only, in the source and in the render.
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes: use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

## Diagram
**The five ticks along the loop**: four inside the round or before it, and one that ends the job.

```text
  1 START      🖊 the meaning of the class            once
    │
  2 PICK       🖊 this batch is worth my time         per round
    │
  4 LABEL      🖊 the class and the region            per ITEM
    │
  5 RULES      🖊 this rule is accepted               per rule
    │
 6 NEXT?      (signs the route, which is a
    │          decision, not a semantic tick)
    ▼
  8 FREEZE     🖊 the freeze signature                once, and it
                                                     ENDS the job
```

## Content

### 1 · The five ticks
**The five ticks**: what each one signs, how often, and where it lives today.

```text
tick                        phase      how often     lives today in
──────────────────────────────────────────────────────────────────────
the meaning of the class    0 START    once          QA2
the batch is worth my time  1 PICK     per round     nowhere
the class and the region    3 LABEL    per item      QB2 · QC4
this rule is accepted       4 RULES    per rule      QD1
the freeze signature        7 FREEZE   once          QE1
```

Four pages hold four of them, one is not written down at all, and nothing joins the set.
A sixth mark exists at phase 7, the route, and it is a business decision rather than a semantic ruling, so it is not on this list.

### 2 · Accept-biased: the gate opens only on zero findings
**The zero-findings precondition**: what must already be clean before a tick is offered.

```text
what must be zero BEFORE a tick is offered
──────────────────────────────────────────────────────────────────────
every item in the batch has a class, a region and an uncertainty
every rule cites at least one item id
the backward-impact list was shown and each flip was ruled on
the sealed guesses were sealed before the first-pass lock
every number names the round that produced it
the regression set passes on the BUILT guideline
the receipt chain rehashes clean
no phase was left attempted and unfinished
```

⬜ Nothing computes these, so today the tick is offered whenever someone reaches the screen.

**This is JL's 260818 ruling on the sibling Board, adopted here**: the machine clears every mechanical finding first, so the person's attention is spent only on the part no machine can do.

### 3 · Three substitutes, all refused
**Three substitutes**: each one looks like consent and is not.

```text
❌ silence                   an unticked tick is unticked, and no amount
                            of elapsed time converts it
❌ the numbers looked good   `state: ✅` means a person signed the freeze,
                            never that the rounds went well
                            (haipipe-page-for-labeling says this outright)
❌ an agent's confirmation   a machine may PROPOSE a class and only a
                            human session makes it gold; on a boundary
                            item the machine proposes the region and
                            leaves the class blank
```

### 4 · What the surface must show
**What the surface shows**: the five granularities a person and a machine each need.

```text
per job     how many ticks are owed, and how many are signed
per round   whether the batch tick and the rule ticks are done
per item    which items still have no class or no region
per tick    when it was signed, by whom, and over which version
            of the policy
blocked     which of the zero-findings checks is not yet zero, and
            therefore why the freeze cannot be offered
```

⬜ No surface exists. `label-status` reports progress and does not report what is unsigned.

## Aims

### A1 · ✋ The five ticks
- A1.1 · Every mark only a person may write is named with its phase and its frequency.
  **Done when:** Division 1 lists all five and says where each lives today.

### A2 · 🟢 Accept-biased: the gate opens only on zero findings
- A2.1 · A person is never asked to sign over a defect a machine could have found.
  **Done when:** The eight checks are computed and the tick is refused while any is non-zero.

### A3 · 🚫 Three substitutes, all refused
- A3.1 · Silence, good numbers, and an agent's confirmation each fail to produce a tick.
  **Done when:** Division 3 names all three and the rule each one breaks.

### A4 · 📡 What the surface must show
- A4.1 · A person sees what they owe and a machine counts what is unsigned.
  **Done when:** One surface carries the five ticks at job, round, item and tick granularity, with the blocking check named.

## States

### A1 · ✋ The five ticks
- ✅ A1.1 · Met; division 1 names all five with phase, frequency, and current home.

### A2 · 🟢 Accept-biased: the gate opens only on zero findings
- ⬜ A2.1 · Not met; the eight checks are named and none is computed.

### A3 · 🚫 Three substitutes, all refused
- ✅ A3.1 · Met; division 3 names silence, good numbers, and agent confirmation.

### A4 · 📡 What the surface must show
- ⬜ A4.1 · Not met; no surface exists and `label-status` does not report what is unsigned.

## Files

### Contracts · what this Page governs
- `../../skills/page-types/haipipe-page-for-labeling/SKILL.md`
  Fixes that a page's ✅ means a person signed the freeze, which is the fifth tick.
- `../../skills/page-workflows/label-status/SKILL.md`
  The read-only surface that should report what is unsigned and today does not.
- `../../agents/moderator-agent.md`
  The hand that elicits every tick and may write none of them.

## Law
- 260818 JL · ✋ The human gate is LAST and accept-biased
      A person is asked to sign only after every computed finding is zero, so the signature is about meaning and never about defects a machine could have caught.
- 260806 JL · 🧑 One human is the semantic authority
      Models may retrieve, pre-label, diagnose, and draft, but human confirmation creates gold and protects the construct's meaning.
- 260818 CC · 🤐 Silence is never consent
      An unticked tick is unticked, and no elapsed time, good number, or agent confirmation converts it.

## Glossary
- ✋ **Tick**: a mark only a person may write, of which this workflow has five.
- 🟢 **Accept-biased**: the gate opens only when every computed finding is zero, so the person spends attention on meaning and not on defects.
- 🚫 **Substitute**: something that looks like consent and is not, of which three are named here.

## Log
260818 · Created QLw14 on the QPw9 precedent, carrying JL's 260818 ruling that the gate is last and accept-biased.
