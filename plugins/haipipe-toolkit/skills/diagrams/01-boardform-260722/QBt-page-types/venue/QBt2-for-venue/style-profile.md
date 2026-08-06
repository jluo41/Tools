# JIS Style Profile (write to this)

🚫 FABRICATED. Every band, every slot, and every refusal below is invented. See
`README.md` in this folder. Nothing here is a measurement of a published paper,
because no JIS paper exists.

A blueprint pack, not a measured one. Each band below is a PACK PRESCRIPTION:
the pack wrote it down as a target. It is not a PACK OBSERVATION, which would
mean the pack counted papers and reported what it found. A venue page must
carry that distinction into every row it prints, because a reader who thinks a
prescription is a measurement will treat it as evidence about the desk.

## The blocks, in the desk's reading order

```
  block          reading position   band (words)   what it owes
  ────────────   ────────────────   ────────────   ─────────────────────────
  Abstract       first              150-220        the question and the verb
  Limits         second             200-350        the ceiling on the verb
  Introduction   third              800-1,200      why the question is open
  Method         fourth             600-900        the recount instructions
  Findings       fifth              700-1,100      one row per band, no story
```

The desk publishes no per-block limit of its own. It publishes one total, and
the bands above must be fitted inside it rather than added to it.

## Abstract

- One paragraph, 4 to 6 sentences, no citations, no display references.
- Arc: the question, then the verb the design supports, then what was counted,
  then what came out, then what it does not establish.
- Slot: `We ask whether [X] is associated with [Y] across [corpus].`
- Slot: `The design is observational, so this paper reports association.`
- Refused: a causal verb. Refused: a number with no denominator beside it.

## Limits

- Written last, read second, and never labelled "limitations".
- Two to four numbered limits, each one naming what it caps.
- Slot: `[Feature] was not assigned, so this paper reports association only.`
- Slot: `[Confounder] is not controlled, and it moves [outcome] in the same
  direction as [exposure].`
- Refused: a limit with no consequence attached. A limit that does not cap a
  verb is background.
- Refused: the phrase "future work will address this", which converts a cap
  into a promise.

## Introduction

- 5 to 8 paragraphs, each leading with its point.
- Arc: the phenomenon, what is not known, why the corpus can speak to it, and
  the numbered contributions.
- Refused: a novelty claim as the contribution.
- Refused: a related-work walk longer than the gap it exists to open.

## Method

- Written as recount instructions, in the order a stranger would run them.
- Every table names the command that produces it, in the sentence that
  introduces the table.
- Slot: `[Table N] is written by [command]; it reads [input] and drops [rule].`
- Refused: a method paragraph with no command in it.
- Refused: an exclusion count with no exclusion policy.

## Findings

- One row per band, in the order the bands are defined, and no reordering by
  effect size.
- Every rate carries its numerator, its denominator, and its interval.
- The close points at the Limits block rather than at implications.
- Refused: a finding sentence whose verb is stronger than the abstract's.
- Refused: an implication paragraph. JIS folds implications into this block's
  last two sentences and publishes no Discussion.

## Sentences

- Declarative, short, one idea each. Define a term where it first appears.
- Lead every paragraph with its point; the editor reads first lines.
- No hedging stacks, no "it is important to note", no buzzwords.

## Format values the pack does NOT record

- Reference style. The pack records none. The desk publishes one, and the desk
  is the only source for it.
- Citation density. Not recorded, at any block.
- Value density. Not recorded, at any block.
- Display count. Not recorded as a number; the mapping rule is one claim, one
  display.

## To enrich from `examples/` (corpus not built, and never will be)

- [ ] Real sentences per slot. Impossible here: the desk is fabricated.
- [ ] Measured word counts to replace the prescribed bands.
- [ ] Measured citation and value density.
