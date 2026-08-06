# Status strip: which board and page this session is on
state: ✅ SETTLED
owner: CC
method: copy Paper's mandatory Closing Block pattern, but derive Board, queue, and page ownership from Board files instead of maintaining a second status ledger
session: 7035d975-4bf2-4082-8f03-426099f07b6c
## Opening
How can every reply show exactly which board scope and task the current session is working on?

A visible status strip lets a reader verify attachment without relying on hidden agent context.
The hard part is keeping it current without creating another shared status file that concurrent sessions can overwrite.
Board and page files already hold the durable facts, so only the live mode and next action belong in the reply.
The design works when three short lines identify the scope, state, and next move every time.

**Covered elsewhere**: The index's activity dashboard, which counts updates rather than time, is `QB2 §8`. The session id and one-window rule remain `QD1`. How a topic becomes well-named pages and groups remains `QA2`. Everything in the reply ABOVE these three lines is `QA3`: the outcome, the gate that had to pass before an agent could write it, the reply's body, and the routing footer. `QA3 §5` carries the map of which owner holds which part. This page owns the last three lines and nothing above them. How LONG the address inside the label is, and whether a short route can replace the path from the repo root down to the board folder, is `QE2`: this page owns the FORM the link takes on each surface, never its length.


## Content
### One visible contract
The strip shows the Board's own name, queue, focus, live mode, next action, and deep link in three lines.
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

## Aims
- [x] 🧭 Define the visible fields and ownership model
      Board, queue, focus, mode, next, and deep link are the complete strip.
- [x] 🧮 Add a deterministic renderer
      One command must derive page and group labels from the Board parser and emit the complete strip.
- [x] 🧷 Bind launched sessions and loaded-skill sessions
      The launcher prime and SKILL.md must both require the same reply-ending contract.
- [x] 🧪 Forward-test with no design context
      A fresh agent attached to a page must end its answer with the right Board, queue, page, and mode without being shown the intended output.
- [x] ✂️ Keep the visible attachment concise
      The complete direct-session block is exactly three Markdown lines; on a terminal the link is embedded in the board-page name on line 1, a piped or chat reply shows the short `/b/` deep link in parentheses after the label, and repeated labels, page title, source file, and separators are omitted.

## States
JL ruled that attachment must be visible in every reply, including when the session is working on a page, a page group, or sourcing for one of them.
`status.py` now renders the strip from Board files, and both SKILL.md and the launcher prime require it.
A fresh agent given only the skill, Board path, and QD6 attachment correctly derived the QD queue, QD6 focus, live mode, deep link, and owning file, then placed the strip last.
JL then rejected the ten-line presentation as too long.
The same information contract now renders in three lines; on a terminal the deep link hides behind the compact Board and queue/focus label as an OSC 8 hyperlink, and a piped or chat reply shows the deep link in parentheses after the label, kept short by `QE2`'s `/b/<board>/<page>` route (JL 260802, later the same day than this page's Law paragraph on the link form).
A second fresh agent read only the skill, Board, and QD6, invoked `status.py` rather than composing the tail manually, and received exactly three lines.
All five items are complete and the ruling is settled.

## Files
### Engines
- `status.py`
  Deterministic renderer for the reply-ending strip.
- `SKILL.md`
  Single source of truth for when the strip is required and how attachment is resolved.
- `cli/serve.py`
  Injects Board and page attachment when a drawer or terminal session opens.

### Input files
- `board.md`
  Owns the page-to-group mapping from which queue is derived.

### The precedent
- `../../paper/haipipe-paper/SKILL.md`
  The precedent: Paper's Closing Block makes live session state visible at the end of every reply.

## Law
Every user-visible reply from a Board-attached session ends with the complete three-line Markdown block emitted by `status.py`, with no prose after it.
The page's `## Pages` group owns the queue; focus is board, group, or page; mode and next action describe only the live turn.
Line 1 is the linked `Board · Queue/Focus`; line 2 is `status · mode`; line 3 is the next action.
The linked label carries the board's OWN name, taken from `board.md`'s first heading, so `01-boardform-260722` reads as `haipipe-board` (JL 260802: of `boardform · QB/QB4`, "I think it should be haipipe-board · QB4"). A board whose title is a sentence rather than a name falls back to the folder name with its `NN-` ordinal and `-YYMMDD` date stripped.
The group prefix is dropped when the page id already carries it, so `QB/QB4` reads `QB4`.
The address rides INSIDE the name on whichever surface the strip lands on (JL 260802). A terminal gets an OSC 8 hyperlink, so the label is clickable and the URL is never drawn; a chat reply gets `[label](url)`, which does the same job where markdown renders. Neither form is right on both, so it picks by whether stdout is a TTY, and `--no-url` still opts out entirely.
That is why 260801 had dropped the link: with one form, hiding the address meant having no link at all.
The first two lines end with Markdown hard breaks so all three remain visibly separate without blank lines.
Do not repeat labels, page title, source file, separators, or the visible raw URL.
Launcher attachment wins, followed by an explicit request, the nearest `board.md`, and the attachment already established in the conversation.
Ambiguous attachment and ownerless whole-Board sourcing are blocked rather than guessed.
No shared status file is written: durable decisions, comments, and logs continue to sync into Board files.

## Discussion
> JL: Add a status strip so everyone can see which Board and queue the session is working on, whether the focus is a page, a page group, or sourcing.
> JL: The first status strip is too long; make it concise, preferably only a few lines.

## Log
- 260806 2144 · [REVISE-CC] swept to the 260806 architecture; dead activity-dashboard pointer QC2 §8 corrected to QB2 §8, and the chat-surface link form updated from hidden-behind-label to the shown short `/b/` deep link in parentheses (status.py + SKILL.md are the ground truth; the Law paragraph froze earlier the same day)
260802 · JL asked which Q owns the strip and whether it belongs in the QA series. Kept here: this page's substance is session state (attachment resolution, queue derivation, the mode and status vocabulary), which is QD's one responsibility, while QA holds what the Board system IS before any of it is built. What was actually missing is the boundary, so Covered elsewhere now points at `QA3 §5` for every part of the reply above these three lines.
260802 1300 · Four rulings from JL landed in `status.py` and are recorded here rather than left in the session. The label now comes from `board.md`'s own first heading instead of the folder name, since the folder is an accident of the day it was created and the board calls itself something; the group prefix is dropped when the page id already carries it; and the address rides inside the name, as an OSC 8 hyperlink on a terminal and as `[label](url)` when piped, chosen by whether stdout is a TTY. That last one is why 260801 had removed the link: with one form, hiding the raw address meant having no link. JL also asked for and then reversed a one-row version, so the block stays three rows: the place, the status, and the next action are three things a reader looks for in three different moments
260801 · Title → "Status strip: which board and page this session is on" (JL: the old one was hard to read); status.py's clickable label now shows a short board name (ordinal + date stripped) so the long URL never appears as text (JL: "make the result clickable, not just the full url")
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260726 · Fresh-context acceptance invoked status.py and received exactly three lines
260726 · Compressed the ten-line fenced strip to three Markdown lines after JL's direct-use feedback
260726 · Fresh-context agent derived QD/QD6 correctly, placed the strip last, and closed the final acceptance item
260726 · Added the deterministic renderer and bound the same closing-block contract in SKILL.md and serve.py
260726 · Opened from JL's request to make Board attachment visible rather than merely agent-aware
