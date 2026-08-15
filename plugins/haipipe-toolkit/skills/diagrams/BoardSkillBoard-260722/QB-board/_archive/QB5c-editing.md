# Editing a sentence from the page
state: 🟡 PARTIAL
owner: JL
method: double-click one plain source sentence; replace it and append one whole-sentence diff line

## Opening
How can someone edit one sentence from the rendered page while preserving its context and audit trail in Markdown?

This page defines an inline edit that replaces exactly one plain source line and records the change beside it.
The hard part is matching the intended sentence without touching a duplicate or decorated line and without detaching its apparatus.
A careless replacement can silently move evidence, comments, or history away from the claim they belong to.
The edit succeeds when one source line changes and one adjacent record shows who changed what and when.

**Covered elsewhere**: Locks, concurrency, and whole-body editing: `QE4`. Typed evidence lanes: `QB5a`. Human comments that sit under the same sentence: `QB5b`.


## Content
### 1 · The one-write result
The saved source has the final sentence, followed by one readable change row:

```
The coefficient is 0.42 in the clustered pooled model.
> ✎ The coefficient is 0.42 in the *clustered* pooled model. · JL · 260729 1502
```

The old sentence is not stored a second time and there is no History section. Every further edit adds one more row. A comment or evidence lane already below the sentence stays below it; adjacency survives the replacement.

## Aims
- [x] 🧠 JL rules the scope: sentence text is editable from the page
- [x] 🔨 The mechanism replaces one plain source line and writes one adjacent whole-sentence diff
- [ ] 🔗 The `QE4` boundary is honored: locks and multi-writer stay there

## States

- 260801 JL · ✂️ Editing a sentence that had apparatus never wrote anything
  JL, with a screenshot: the edit form open on a sentence carrying one comment, and the server answering that the sentence is not in the source file.
  It was not: the payload ended `…below the read.⚑ 1`, because the ⚑ badge lives INSIDE the `<p>` since it became a zero-width span, and all three writers read `p.textContent` raw.
  `QC7`'s anchor is an exact match against a source line, so a badge in the string means the line can never be found, and the server was right to refuse.
  There is now ONE reader, `window.__boardSentenceText`, and the edit path, the add-a-lane path, and the comment path all use it; the address module dropped its own copy rather than keep a second.
  The same screenshot showed the form squeezed to one character wide, because the error message sat in a fifth grid column and a full sentence of Chinese took the width; it spans its own row now and the textarea has a floor.
  Verified in Chrome by double-clicking the real sentence: the form opens 480px wide, prefilled without the badge, and posting that text reaches the server's SECOND gate ("the sentence has not changed"), which is only reachable once the line has been found.
The single-sentence edit is implemented. It deliberately refuses a duplicate sentence (to avoid editing the wrong copy) and a sentence carrying Markdown decoration (to avoid silently deleting links, code, or bold). Concurrency remains open under `QE4`.

## Files
- `cli/serve.py`
  `/_board/edit-sentence`: exact source lookup, replacement, and diff-line write.
- `assets/js/00-header.js` / `assets/css/10-focus.css`
  Double-click editor and the visible `~removed~` / `*added*` rendering.
- `QE-sharing/QE4-editlock.md`
  The board-wide editing question this face is the sentence-scoped slice of.

## Log
260801 · Anchor payload fixed: the ⚑ badge was being posted as part of the sentence, so every edit, lane and comment on an apparatus sentence missed the anchor. One shared reader for all three writers; the edit form also stopped collapsing to one character wide
260729 · Double-click editing shipped: final sentence replaces its source line; one adjacent whole-sentence `> ✎` diff records changed words and ends with author + time. Duplicate and Markdown-formatted sentences refuse safely; QE4 owns concurrent writers.
260729 · Opened when the QAb group was carved (JL named it: QAb2 Editing)
