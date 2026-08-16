# Semantic attachments under a sentence
state: 🟡 PARTIAL
owner: JL
method: keep readable prose plus stable semantic ids and typed provenance lanes

## Question
How should a sentence refer to a citation, value, or Display before output-specific formatting?

The authored sentence should not contain three citation styles or a copied table filename. It needs stable semantic anchors, while the detailed source, provenance, state, and preview binding live in typed lanes directly beneath the sentence.

## Boundary
- ✅ Covered here
  The Markdown source representation and stable identity of citation, value, and Display attachments.
- ↪ Covered elsewhere
  The Board preview behavior is `QBa5`; unresolved evidence placeholders are `QBc3`; output formatting is `QBb3`.

## Content
### Proposed pattern
```markdown
The primary specification showed a lower prescribing probability [value:main-beta].
> Value: main-beta · source=task/C04/.../source_data.csv · state=verified
> Citation: smith2024 · source=bibliography · state=verified
> Display: display04 · target=S-Display-4 · state=rendered
```

### Stable identity
The semantic id survives a new rendering, candidate promotion, citation style, or output format.
A Section refers to `display04`, not `table3-main-results.tex` or a candidate filename.

### Inline versus lane
The sentence may carry the smallest readable anchor needed for projection.
The lane carries provenance and interaction detail and is never emitted as manuscript prose.
The exact citation and value anchor syntax is still a ruling, not a settled grammar.

## Items to Finish
- [x] 🆔 Choose stable semantic ids
      Citation, value, and Display identity do not depend on output syntax or candidate filenames.
- [ ] 📐 Freeze the anchor and lane grammar
      Decide what remains inline and what lives only under the sentence.
- [ ] 🔍 Define resolution failure
      A missing id, stale source, or unverified value must become visible and block the relevant gate.
- [ ] 🧪 Project one sentence into three formats
      Verify the same attachments become correct LaTeX, Word, and HTML representations.

## Where we are
Stable Display identity and typed lanes are the selected direction.
The exact source grammar and failure behavior remain open.

## Files
- `haipipe-board/ref/board-form.md`
  The current sentence apparatus.
- `stages/5-section-edit/template.md`
  The paper-side sentence source rules.
