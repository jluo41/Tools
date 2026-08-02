# Delivery-Section: the rules you cannot check one sentence at a time

state: 🟡 PARTIAL · the section unit is separated from the sentence unit; the shared loss list and QB11c are open
owner: JL
method: hold every rule whose unit is a whole section, so a format adapter is judged on sequence rather than on wording

## Opening

What has to survive when a section becomes a file a journal accepts?

A section here is one stage page's `## Content`, delivered as one file such as `sections/03_method.tex`. A sequence is everything about it that only exists in the ordering: which heading sits inside which, which paragraph comes before which, where a float lands. Those are the facts a per-sentence check cannot see.

**Where this page sits**: QB9 Build owns generating, checking, and promoting candidate files.
This series is where Build's adapters are specified, and QB12 holds the rules whose unit is one sentence.
Its three faces are QB11a the LaTeX adapter, QB11b the Word adapter, and QB11c where a float lands.

**Why this is not a matter of scale**: a sentence rule can be checked one sentence at a time, in any order.
A section rule can only be checked by reading top to bottom, because every claim it makes is about what comes before what.
The old filenames denied this outright: QB11a and QB11b were called `sentence-to-latex` and `sentence-to-word` while their own openings said the unit was the SECTION.

**What the series still owes**: one loss list, not one per adapter.
Both adapters drop things, and today each says so in its own words, which makes it impossible to tell whether they drop the same things.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**The admission test is shuffling, and it runs in the opposite direction from QB12's**: a rule belongs here only if reordering the paragraphs would break it.
A rule that survives the shuffle is a sentence rule and belongs on QB12.

**Never write "sentence" for the unit**: that word cost this series its own name until 260802.
Say section, or say `## Content`, and let QB12 own the other word.

**Name a dropped element, never "some formatting"**: a loss list is only useful if a reader can check it.
"Word cannot carry why-comments" can be verified; "some things do not survive" cannot.

## Diagram

**What the sequence carries**: the facts that live in the ordering, and nowhere else.

```text
   ✍️ S-page ## Content
        │
        │  📐 adapter
        ▼
   📄 one delivered file

   WHAT ONLY THE SEQUENCE KNOWS
   ────────────────────────────
   🔡 heading nesting   ━━▶  the outline
   ¶  paragraph order   ━━▶  the argument's order
   🖼 float citation     ━━▶  placement + numbering   ← QB11c

   🔍 test: reorder the paragraphs.
      broke?  ━━▶ it is a SECTION rule, it lives here
      fine?   ━━▶ it is a SENTENCE rule, it lives on QB12
```

## Content

### 1 · What makes a rule a section rule

**The shuffle test**: one question that sorts every candidate rule into this series or QB12.

```text
   a candidate rule
        │
        ▼
   🔀 reorder the paragraphs of the section
        │
   ┌────┴────┐
   ▼         ▼
  💥 breaks  ✅ still holds
   │            │
   ▼            ▼
  QB11        QB12
  sequence    one sentence at a time
```

🔍 Establishes the admission test for this series, and why the two neighbouring series cannot absorb it.

#### 1.1 · The unit was denied by its own filenames
(the pages said SECTION in their openings and said sentence in their names, and the names won)
QB11a's opening states it directly: the unit is the section, and that is not a difference of scale.
Because the files were named `sentence-to-latex` and `sentence-to-word`, both sat filed under the sentence work, and nothing read them as one series until 260802.

#### 1.2 · Placement is a section rule, which is why QB11c is here
(the float's own page does not decide where the float goes)
LaTeX floats near the FIRST mention, so the section that cites a unit earliest decides where it appears.
That makes placement a fact about citation order, which is a sequence, so it left QB13 for this series.

## Aims

### A1 · 🔍 What makes a rule a section rule
- A1.1 · The unit is named consistently across the series.
  **Done when:** no file, title, or opening in this series calls a section a sentence.
- A1.2 · Both adapters declare the same loss list, stated once.
  **Done when:** this page carries one list of what a delivered section may lose, and QB11a and QB11b each say only where they differ from it.
- A1.3 · Where a float lands is decided, rather than left to whatever LaTeX does.
  **Done when:** QB11c states the placement rule and a compiled paper is checked against it.

### P · 🏁 Page-level
- P1 · An adapter can be judged without reading its prose output.
  **Done when:** a delivered section is accepted or rejected on outline, paragraph order, and float positions alone.

## States

### A1 · 🔍 What makes a rule a section rule
- ✅ A1.1 · Done 260802. The files became `QB11a-section-to-latex` and `QB11b-section-to-word`, and both titles already said "A section, delivered as…".
- ⬜ A1.2 · Not started. Each adapter still states its own losses in its own words, so the two lists have never been compared.
- ⬜ A1.3 · Not started. QB11c is the only 🔴 face in this series, and placement is currently whatever LaTeX decides.

### P · 🏁 Page-level
- ⬜ P1 · Untested. The criterion is written here; no delivered section has been judged against it.

## Files

- `QB11a-section-to-latex.md` · the LaTeX adapter, and the page that first stated the unit correctly
- `QB11b-section-to-word.md` · the Word adapter, shipping as `haipipe-paper-to-word` 0.1.0
- `QB11c-display-placement.md` · where a float lands, the only 🔴 face here
- `QB9-build.md` · the concern that calls both adapters

## Law

- The unit of this series is the section, and the test of a section rule is that it cannot be checked one sentence at a time.
  A rule that reads the same with the paragraphs shuffled belongs on QB12, not here.

## Glossary

- **Sequence**: the ordered facts about a section (outline, paragraph order, float position) that no per-sentence check can see.
- **Loss list**: what a delivered section is allowed not to carry, stated so a reader can check each item.

## Log

260802 · Migrated to the QB4 page contract: Writing Style added, Content numbered with a face figure and caption, Aims regrouped as A1/A2/P with `Done when`, States mirrored per Aim.
260802 · Opened as the head of the section series; QB9a and QB9b became faces QB11a and QB11b, and QB5f became QB11c.
