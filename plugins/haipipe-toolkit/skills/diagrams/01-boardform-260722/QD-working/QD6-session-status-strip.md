# Status strip: which board and page this session is on
state: ✅ SETTLED
owner: CC
method: copy Paper's mandatory Closing Block pattern, but derive Board, queue, and page ownership from Board files instead of maintaining a second status ledger

## Question
How does an agent make its current Board attachment visible to everyone, rather than merely keeping that attachment somewhere in its own context?
The answer should appear at the end of every reply and distinguish the Board, the queue that owns the work, the current focus, and the kind of work happening now.

The difficult part is persistence without duplication.
A session needs live status, but writing one shared `STATUS.md` would let simultaneous page sessions overwrite each other and would become stale as soon as a conversation moved.
The durable facts already live in `board.md` and the Q/S pages; only the live mode and next action belong to the reply.


## Boundary
- ✅ Covered here
  The reply-ending status strip, attachment resolution, queue derivation, focus and mode vocabulary, and the deterministic renderer that keeps every agent's shape consistent.
- ↪ Covered elsewhere
  The index's activity dashboard, which counts updates rather than time, is `QC2 §8`.
  The session id and one-window rule remain `QD1`.
  How a topic becomes well-named pages and groups remains `QA2`.

## Content
### One visible contract
The strip shows the Board folder, queue, focus, live mode, next action, and deep link in three lines.
It is session state rendered from durable Board facts, not another durable ledger.

### Attachment resolution
Use the attachment injected by the Board launcher first.
Otherwise use an explicit Board path or page id in the user's request, then the nearest `board.md` above the working path.
Retain that attachment in the conversation until the user switches or detaches it.
If more than one Board remains plausible, show `blocked · attachment` and ask instead of guessing.

### Queue and focus
A page focus derives its queue from that page's `## Pages` group.
A group focus is itself the queue.
Board-level work uses the explicit `board-level · cross-group` queue.
Sourcing must serve a page or group; `sourcing` with only a whole-Board focus is blocked because evidence gathering without an owner is how topic drift begins.

### Live mode
The closed vocabulary is `discussion | sourcing | implementation | review | status`.
The mode describes this turn and never changes a page's `state:` by itself.
Substantive work still follows `sync`: update the owning page in the same round, then rebuild.

## Items to Finish
- [x] 🧭 Define the visible fields and ownership model
      Board, queue, focus, mode, next, and deep link are the complete strip.
- [x] 🧮 Add a deterministic renderer
      One command must derive page and group labels from the Board parser and emit the complete strip.
- [x] 🧷 Bind launched sessions and loaded-skill sessions
      The launcher prime and SKILL.md must both require the same reply-ending contract.
- [x] 🧪 Forward-test with no design context
      A fresh agent attached to a page must end its answer with the right Board, queue, page, and mode without being shown the intended output.
- [x] ✂️ Keep the visible attachment concise
      The complete direct-session block is exactly three Markdown lines; the deep link wraps the first line, and repeated labels, page title, source file, separators, and raw URL are omitted.

## Where we are
JL ruled that attachment must be visible in every reply, including when the session is working on a page, a page group, or sourcing for one of them.
`status.py` now renders the strip from Board files, and both SKILL.md and the launcher prime require it.
A fresh agent given only the skill, Board path, and QD6 attachment correctly derived the QD queue, QD6 focus, live mode, deep link, and owning file, then placed the strip last.
JL then rejected the ten-line presentation as too long.
The same information contract now renders in three lines, with the deep link hidden behind the compact Board and queue/focus label.
A second fresh agent read only the skill, Board, and QD6, invoked `status.py` rather than composing the tail manually, and received exactly three lines.
All five items are complete and the ruling is settled.

## Files
### Engines
- `status.py`
  Deterministic renderer for the reply-ending strip.
- `SKILL.md`
  Single source of truth for when the strip is required and how attachment is resolved.
- `serve.py`
  Injects Board and page attachment when a drawer or terminal session opens.

### Input files
- `board.md`
  Owns the page-to-group mapping from which queue is derived.

### The precedent
- `haipipe-paper/SKILL.md`
  The precedent: Paper's Closing Block makes live session state visible at the end of every reply.

## Law
Every user-visible reply from a Board-attached session ends with the complete three-line Markdown block emitted by `status.py`, with no prose after it.
The page's `## Pages` group owns the queue; focus is board, group, or page; mode and next action describe only the live turn.
Line 1 is the linked `Board · Queue/Focus`; line 2 is `status · mode`; line 3 is the next action.
The linked label carries a SHORT board name (leading `NN-` ordinal and trailing `-YYMMDD` date stripped, so `01-boardform-260722` reads as `boardform`); the long served URL stays behind the link and never shows as text.
The first two lines end with Markdown hard breaks so all three remain visibly separate without blank lines.
Do not repeat labels, page title, source file, separators, or the visible raw URL.
Launcher attachment wins, followed by an explicit request, the nearest `board.md`, and the attachment already established in the conversation.
Ambiguous attachment and ownerless whole-Board sourcing are blocked rather than guessed.
No shared status file is written: durable decisions, comments, and logs continue to sync into Board files.

## Discussion
> JL: Add a status strip so everyone can see which Board and queue the session is working on, whether the focus is a page, a page group, or sourcing.
> JL: The first status strip is too long; make it concise, preferably only a few lines.

## Log
260801 · Title → "Status strip: which board and page this session is on" (JL: the old one was hard to read); status.py's clickable label now shows a short board name (ordinal + date stripped) so the long URL never appears as text (JL: "make the result clickable, not just the full url")
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260726 · Fresh-context acceptance invoked status.py and received exactly three lines
260726 · Compressed the ten-line fenced strip to three Markdown lines after JL's direct-use feedback
260726 · Fresh-context agent derived QD/QD6 correctly, placed the strip last, and closed the final acceptance item
260726 · Added the deterministic renderer and bound the same closing-block contract in SKILL.md and serve.py
260726 · Opened from JL's request to make Board attachment visible rather than merely agent-aware
