# The sentence as a content unit
state: ✅ SETTLED
owner: JL
method: keep one sentence per source line while making its paragraph role and sibling relation explicit

## Question
What must be defined about a sentence before a stage can write or revise it reliably?

A sentence has its own job and evidence boundary, but it also lives among sibling sentences inside a paragraph. Editing only the local sentence can preserve grammar while breaking paragraph progression, and editing only the paragraph can hide which claim or attachment changed.

## Boundary
- ✅ Covered here
  Sentence identity, paragraph membership, sentence job, and sibling-aware revision.
- ↪ Covered elsewhere
  Citation, value, and Display attachments are `QBa4`; the page's two-level Content structure is `QBa1`.

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

### Revision rule
A worker changing one sentence reads the whole owning paragraph and the adjacent paragraph jobs.
It checks both the sentence's local truth and the paragraph's sequence after the edit.

## Items to Finish
- [x] 🧾 Keep one sentence per source line
      The Board can attach apparatus by adjacency and render one sentence row.
- [ ] 📐 Define sentence roles
      Decide whether claim, transition, evidence, interpretation, limitation, and signpost need explicit labels or remain inferred.
- [ ] 🔗 Define the sibling check
      State the minimum context a sentence worker must read before and after its target.
- [ ] 🧪 Revise one paragraph sentence-by-sentence
      Verify local edits preserve the paragraph job and narrative progression.

## Where we are
The source-line rule exists in the Board.
The sibling-aware writing and revision contract is not yet part of the paper stage skill.

## Files
- `haipipe-board/ref/q-template.md`
  The sentence-row and paragraph grammar.
- `stages/5-section-edit/`
  The writing contract that should use it.
