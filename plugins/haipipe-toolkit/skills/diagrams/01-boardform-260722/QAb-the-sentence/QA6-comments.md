# Sentence-local comments

state: ✅ SETTLED
owner: JL
method: select a sentence → write one `> WHO:` line directly below it

## Question
How should a reader comment on one sentence without separating the comment from its context?

The comment belongs under the sentence it concerns, not in a page-bottom queue. The source of truth is an adjacent Markdown line: `> JL: comment · 260729 1502`.

## Boundary
- ✅ Covered here
  Selecting a sentence, server-side write-back, and the sentence-local source syntax.
- ↪ Covered elsewhere
  Typed evidence lanes are `QAb1`; tracked sentence edits are `QAb2`; sentence-specific agent context is `QAb3`.

## Diagram

```
select one sentence → 💬 Comment → POST /_board/comment
                                      │
                                      ▼
                   source Markdown: sentence
                                    > JL: comment · time
                                      │
                                      ▼
                               rebuild board.html
```

## Items to Finish
- [x] Select one sentence and save a comment directly beneath it
- [x] Accept arbitrary initials and preserve the author/date
- [x] Keep the adjacent comment visible without relying on JavaScript
- [x] Delete the old page-bottom comment queue and its status lifecycle

## Where we are
Sentence-local comments are implemented. The browser sends the selected sentence and comment to `serve.py`; it finds the sentence in the source page, inserts the adjacent `> WHO:` row, and rebuilds the Board.

The old `## Comments` queue, quote anchors, open/solved state, and re-anchoring lifecycle have been discarded.

## Files
- `serve.py`
  `add_comment` performs the server-side sentence-adjacent write.
- `assets/board.js`
  Opens the selection composer and posts the selected sentence.
- `src/body.py`
  Renders sentence-local comments in their sentence apparatus.

## Law
Comments are attached by adjacency: a `> WHO:` row belongs to the plain sentence directly above it.

## Log
260729 · Deleted the legacy bottom comment queue and its historical lifecycle. The page now specifies only the sentence-local comment behavior.
260729 · Sentence-local comments shipped: selection posts its containing sentence to `serve.py`, which inserts `> WHO: comment · time` beneath it.
