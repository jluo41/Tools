# Sentence and projection
state: ✅ SETTLED
owner: JL
method: connect a selected display to the reader without treating a visual citation as a new source of values

## Opening
How does a selected Display unit reach a reader-facing sentence?

The Paper wrapper references the selected asset.
The section sentence cites the wrapper through the unit's stable label.

## Diagram
```text
assets/figure.pdf ─► float.tex ─► \input or \ref ─► S-Main-N sentence
       ④                 ⑤                         ⑥ reader link
```

## Content
### The last provenance link
The `S-Display-N` page records the specific section, paragraph, and sentence that consumes the display.
This makes the display a reader-facing claim support rather than a detached gallery item.

### Projection does not alter evidence
A sentence may describe what the reader should notice.
It does not type values into the wrapper or reinterpret the task result without going through the Paper's claim and revision process.

## Aims
- [x] 🔗 Make the reader sentence part of the provenance chain
      Link ⑥ names the section, paragraph, and sentence.
- [x] 📌 Keep the wrapper as the only Paper asset reference
      Sections do not create parallel figure blocks or ad hoc includes.

## States
The Paper Display template and sentence apparatus distinguish making a display from citing it.

## Files
- `paper/1-lifecycle/haipipe-paper-stage/stages/4-display/template.md`
  Six-link provenance chain.
- `paper/1-lifecycle/haipipe-paper-stage/stages/5-section-edit/stage.md`
  Section-side display handoff.

## Law
Law: A reader cites the selected wrapper, not an untracked render or a task diagnostic.

## Log
260727 · Joined the visual asset chain to the sentence apparatus.
