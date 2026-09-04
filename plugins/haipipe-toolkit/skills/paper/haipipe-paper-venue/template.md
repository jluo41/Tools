# <Target>: <what it rewards and refuses>

state: 🔴 OPEN · <what is verified and what remains open>
page-type: venue
owner: <owner>
method: <how this target is researched and refreshed>

## Opening

<One paragraph: what this desk is, which categories it publishes, and what it
buys. No paper is named — this page serves any paper that ever targets the desk.>

### Writing Style

Distinguish DESK RULE, PACK OBSERVATION, PACK PRESCRIPTION, and UNKNOWN inline.
Every number names its source and access date. Write "the pack refuses X",
never "do not do X" — a reference, not a rulebook.

## Diagram

**Three figures, in this order** (QBv1 template, JL 260803):

```text
① desk taste         what counts as the contribution · what is desk-rejected · the test
② Venue-Structure    which units, in reading order, and the budget each carries ·
                     the pack's parts SUMMED against the desk's total
③ Submission-Rules   category and cap · format · references · portal · anonymity ·
                     disclosures · the desk's own URLs · enforcement moments
```

## Content

<The division list is RESOLVED from paper/venue/<pack>/<outlet>/ — one
style.md per unit, one division, in the desk's own reading order. A desk with
no pack tree (grant, patent) resolves from the target's own document units.>

### 1 · What the desk buys, and what it will not

<The taste test, sourced. Rewarded contributions, permitted methods,
desk-reject signals — the desk's own words where it publishes them.>

### 2 · What arriving here costs

<Fees, review clock, reported odds. An unpublished fact is an UNKNOWN row
with an owner, never a deleted one.>

### 3 · Which sibling outlet a paper leans to, and what pins it here

<Only when a family shares a pack. What the primary claim is at each desk,
and what the pin costs downstream.>

### 4 · Sec-0-<Unit>: <what the pack found, in one line>

<One division per desk reading unit, numbered to join `S-Main-<n>`; the
resolver wins when desk and index part. Repeat this division shape per unit.>

#### 4.1 · The moves, as slots

#### 4.2 · What the pack refuses

#### 4.3 · Format values

<Each number names its style.md line or exemplar. `not recorded by the pack`
is a finding and is printed.>

#### 4.4 · The language, in the papers' own words

### <last> · Before you upload: the binding rules as a list you can run

<Only DESK RULES, each with its enforcement moment: at-submission,
at-revision, at-acceptance, at-publication.>

## Aims

### A1 · <mirror division 1's name>

- ⬜ A1.1 · <what done looks like for the taste division>
  **Done when:** rejection tests resolve to current desk sources.
  **Now:** <current fact>

<One Aim group per Content division, same names behind an emoji, plus one `P`
group for page-wide targets that belong to no single unit.>

### P · Targets that belong to no single section

- ⬜ P1 · Every venue statement is typed and sourced; every desk rule carries
  its enforcement moment.
  **Done when:** a walk of the page finds no bare number and no untyped claim.
  **Now:** <current fact>

## Files

### ⚙️ Engines · what RUNS this page's subject

- `sync-exemplars.py` · regenerates the 📤 Generated blocks, and only those

### 📋 Contracts · what CARRIES a rule to other pages

- `paper/haipipe-paper-venue/SKILL.md` · this page's contract

### 📥 Input files · what this page READS

- `paper/venue/<pack>/<outlet>/` · taste.md · per-unit style.md · exemplars

### 🔗 Authority · what the DESK itself PUBLISHES

- <the desk's own URLs, read directly and never through the pack>

### 📤 Generated · what a tool WRITES into this page, between markers

- <sync-exemplars.py output blocks>

## Log

- <date> · <what changed, why, and which source/version caused it>
