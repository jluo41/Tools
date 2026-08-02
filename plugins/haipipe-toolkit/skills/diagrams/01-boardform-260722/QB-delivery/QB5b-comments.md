# Sentence-local comments

state: ✅ SETTLED
owner: JL
method: select a sentence → write one `> WHO:` line directly below it

## Opening
How should a reader comment on one sentence without separating the comment from its context?

This page defines a sentence-local comment as one adjacent Markdown record beneath the words it addresses.
Page-bottom queues force the reader to reconstruct context and become fragile when the prose moves.
Adjacency keeps the comment visible and writable without a second page-level lifecycle.
The design succeeds when a saved comment appears under the exact source sentence and survives every rebuild.


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

- 260801 JL · ↩️ A comment longer than one line lost everything after the first
  JL: "what if I enter multiple lines as the comment? you will just keep sentence 1 and make sentence 2 and 3 to be outside of the comment."
  Exactly that: `add_comment` only trimmed the ends of the textarea's value, then inserted a string containing newlines as ONE list element, and the join split it again.
  The second line landed in the page as PROSE, it rendered as a sentence, it became a new writable anchor, and it carried the timestamp away from the comment it belonged to.
  A record is a `>` RUN, not a line, and the renderer already knew that: a bare `>` line after a `> WHO:` head folds into the same lane as `.lane-cont`.
  So all three writers now build their record through one `_record_lines`, which keeps every typed line as a continuation, turns a blank line into a single `>` break, and strips a leading `>` from typed text so a paste cannot forge a reply from someone else.
  Verified through the real UI, not the endpoint: selected a sentence, clicked 💬, typed three lines, saved, and the file gained one record of three `>` lines with nothing loose; the page was then restored byte for byte.
Sentence-local comments are implemented. The browser sends the selected sentence and comment to `serve.py`; it finds the sentence in the source page, inserts the adjacent `> WHO:` row, and rebuilds the Board.

The old `## Comments` queue, quote anchors, open/solved state, and re-anchoring lifecycle have been discarded.

- 260731 JL · 📸 A comment can carry a screenshot
  JL: "when I take the screenshot, can it be paste there?", so pasting a clipboard image into the comment box uploads it to the board's `fig/` through the new `/_board/image` and inserts `![image](fig/…)` at the cursor.
  The comment row itself still lands through the unchanged `/_board/comment` write, and `note()` already rendered markdown images inside `> WHO:` rows, so only the upload path is new (haipipe-board 0.60.0).
- 260731 JL · 💬 Fold prose became commentable
  The three blanket `.folds` guards in `board.js` narrowed to what cannot anchor, so Law, Lesson, Glossary, and Discussion prose take sentence comments like main text; the ruling and the story live on `QB4g` (haipipe-board 0.59.0).

## Files
- `cli/serve.py`
  `add_comment` performs the server-side sentence-adjacent write.
- `assets/js/00-header.js`
  Opens the selection composer and posts the selected sentence.
- `src/body.py`
  Renders sentence-local comments in their sentence apparatus.

## Law
Comments are attached by adjacency: a `> WHO:` row belongs to the plain sentence directly above it.

## Log
260801 · Multi-line comments fixed: one record, one `>` run, continuations kept (JL). The same grammar now serves comments, typed lanes and discussion lines through one `_record_lines`
260729 · Deleted the legacy bottom comment queue and its historical lifecycle. The page now specifies only the sentence-local comment behavior.
260729 · Sentence-local comments shipped: selection posts its containing sentence to `serve.py`, which inserts `> WHO: comment · time` beneath it.
