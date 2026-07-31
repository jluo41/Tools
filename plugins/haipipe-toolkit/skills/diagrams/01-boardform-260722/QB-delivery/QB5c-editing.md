# Editing a sentence from the page
state: 🟡 PARTIAL
owner: JL
method: double-click one plain source sentence; replace it and append one whole-sentence diff line

## Question
Can the sentence's own text be edited from the page, and what does that do to the markdown?
Yes: double-click opens an inline editor for exactly one plain source sentence. Save replaces that line and writes one `> ✎` record directly beneath it: the full post-edit sentence, with `~removed~` and `*added*` words marked, then the editor's initials and time.

## Boundary
- ✅ Covered here
  Whether and how one sentence's text is changed from the page, and what happens to its adjacent apparatus and edit record.
- ↪ Covered elsewhere
  Locks, concurrency, and whole-body editing: `QE4`. Typed evidence lanes: `QAb1`.
  Human comments that sit under the same sentence: `QA6`.

## Content
### 1 · The one-write result
The saved source has the final sentence, followed by one readable change row:

```
The coefficient is 0.42 in the clustered pooled model.
> ✎ The coefficient is 0.42 in the *clustered* pooled model. · JL · 260729 1502
```

The old sentence is not stored a second time and there is no History section. Every further edit adds one more row. A comment or evidence lane already below the sentence stays below it; adjacency survives the replacement.

## Items to Finish
- [x] 🧠 JL rules the scope: sentence text is editable from the page
- [x] 🔨 The mechanism replaces one plain source line and writes one adjacent whole-sentence diff
- [ ] 🔗 The `QE4` boundary is honored: locks and multi-writer stay there

## Where we are
The single-sentence edit is implemented. It deliberately refuses a duplicate sentence (to avoid editing the wrong copy) and a sentence carrying Markdown decoration (to avoid silently deleting links, code, or bold). Concurrency remains open under `QE4`.

## Files
- `serve.py`
  `/_board/edit-sentence`: exact source lookup, replacement, and diff-line write.
- `assets/board.js` / `assets/board.css`
  Double-click editor and the visible `~removed~` / `*added*` rendering.
- `QE4-editlock.md`
  The board-wide editing question this face is the sentence-scoped slice of.

## Log
260729 · Double-click editing shipped: final sentence replaces its source line; one adjacent whole-sentence `> ✎` diff records changed words and ends with author + time. Duplicate and Markdown-formatted sentences refuse safely; QE4 owns concurrent writers.
260729 · Opened when the QAb group was carved (JL named it: QAb2 Editing)
