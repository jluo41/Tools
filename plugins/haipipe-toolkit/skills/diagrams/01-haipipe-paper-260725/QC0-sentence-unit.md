# The sentence as a content unit
state: ✅ SETTLED
owner: JL
method: keep one sentence per source line while making its paragraph role and sibling relation explicit

## Question
What must be defined about a sentence before a stage can write or revise it reliably? A sentence carries its own evidence boundary and also lives among siblings inside a paragraph, and everything attached to it is bound by simple adjacency rather than new syntax.

A sentence has its own job and evidence boundary, but it also lives among sibling sentences inside a paragraph. Editing only the local sentence can preserve grammar while breaking paragraph progression, and editing only the paragraph can hide which claim or attachment changed.


The approach is one sentence per source line, with anything attached to it bound by simple adjacency. What we want is to be able to hang a citation, a number, a display or a review thread on a sentence without inventing new syntax, so existing files gain the behaviour the moment they are rebuilt.
## Boundary
- ✅ Covered here
  Sentence identity, paragraph membership, sentence job, sibling-aware revision, and the adjacency rule every attachment type depends on.
- ↪ Covered elsewhere
  What hangs on a sentence is one face per type: a citation is `QC1`, a value is `QC2`, a table is `QC3`, a figure is `QC4`. The rendering mechanism they all share belongs to the Board at `QA8` on the boardform board. The page's two-level Content structure is `QBc1`.

## Diagram
```
 ONE SENTENCE, ONE SOURCE LINE, AND WHAT BINDS TO IT

 #### P3. establish that discretion varies with guideline clarity
 (the paragraph's JOB — scaffolding, dropped on sync)
 ┌──────────────────────────────────────────────────────────┐
 │ S1  Physicians prescribe more where guidelines …         │
 │ S2  Discretion rises when guidelines are ambiguous.      │ ◄ the sentence
 │     > Citation: Meyer 2010 · bib hits=0 · [Q-Section-1]  │ ◄ ADJACENCY
 │     > Value: gradient · run=… · state=verified           │   binds these
 │ S3  That gradient is what this paper tests.              │
 └──────────────────────────────────────────────────────────┘

 TWO BOUNDARIES, AND A WORKER MUST HOLD BOTH
   sentence  what THIS sentence claims, does, supports
   sibling   how it follows S1 and prepares S3
   edit only the sentence ──► grammar fine, PROGRESSION broken
   edit only the paragraph ──► which claim changed becomes invisible

 ADJACENCY IS THE BINDING, AND IT HAS ALREADY BITTEN
   a `>` line directly under a sentence attaches to THAT sentence
   (blank lines tolerated).
   ⚠️ on MISQ a lane sat after a PARAGRAPH while its prose said
      "the sentence above". It silently bound to the wrong sentence
      and had to be moved.
   the rule that follows: a PAGE-level concern has no sentence to
   attach to. It false-attaches to whatever precedes it, and belongs
   in Items to Finish instead.

 WHY THE FOUR TYPES NEEDED NO NEW SYNTAX
   QC1 citation · QC2 value · QC3 table · QC4 figure
   all four ride this one rule. That is why they are four faces of
   one mechanism rather than four mechanisms.
```

## Content
### Source shape
One prose sentence occupies one Markdown source line.
A `####` heading identifies the paragraph.
An optional job line states what that paragraph must accomplish.

### Two boundaries
```
sentence boundary   what this sentence claims, does, and supports
sibling boundary    how it follows the prior sentence and prepares the next one
```

### Adjacency is the binding
A `>` line directly under a sentence attaches to that sentence, with blank lines tolerated between them.
That rule is what makes the four attachment faces possible: none of them needs new syntax, because the paper dialect already writes evidence directly beneath the sentence it belongs to.
It also has a failure mode that has already bitten once on the MISQ paper: a lane that sat after a paragraph, while its prose said "the sentence above", silently attached to the wrong sentence and had to be moved.
A page-level concern has no sentence to attach to, false-attaches to whatever precedes it, and belongs in Items to Finish instead.

### Revision rule
A worker changing one sentence reads the whole owning paragraph and the adjacent paragraph jobs.
It checks both the sentence's local truth and the paragraph's sequence after the edit.

## Items to Finish
- [x] 🧾 Keep one sentence per source line
      The Board can attach apparatus by adjacency and render one sentence row.
- [x] ⚑ Adjacency proven on a real page
      The MISQ paper board renders 20 typed lanes across 52 sentence drawers, and the two failure modes above were found by doing it rather than by reasoning about it.
- [ ] 📐 Define sentence roles
      Decide whether claim, transition, evidence, interpretation, limitation, and signpost need explicit labels or remain inferred.
- [ ] 🔗 Define the sibling check
      State the minimum context a sentence worker must read before and after its target.
- [ ] 🧪 Revise one paragraph sentence-by-sentence
      Verify local edits preserve the paragraph job and narrative progression.

## Where we are
The source-line rule and the adjacency binding exist in the Board and are in daily use on the MISQ paper board. The sibling-aware writing and revision contract is not yet part of the paper stage skill.

## Files
- `haipipe-board/ref/board-form.md`
  The sentence-row, adjacency and paragraph grammar.
- `stages/5-section-edit/`
  The writing contract that should use it.

## Law
One prose sentence occupies one Markdown source line. A `####` heading identifies the paragraph, and an optional job line states what that paragraph must accomplish.

Adjacency is the binding. A `>` line directly under a sentence attaches to THAT sentence, with blank lines tolerated between them, and no new syntax is introduced for any attachment type. Two consequences are not optional: a lane that drifts away from its sentence silently attaches to the wrong one, and a page-level concern has no sentence to attach to at all and belongs in `## Items to Finish`.

A worker changing one sentence reads the whole owning paragraph and the adjacent paragraph jobs, and checks both the sentence's local truth and the paragraph's sequence after the edit.
