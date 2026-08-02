# In-page editing and locks

state: 🔴 OPEN
owner: CC
method: start with a per-file lock (`HOLD` already exists); do not reach for a CRDT first

## Question
How can people edit a board page in place without letting simultaneous changes overwrite the Markdown source?

In-page editing would turn the board from a reading and comment surface into a real workbench.
The hard part is that Markdown is a file, not a collaborative database, so the last writer can erase the first.
The answer determines which sections can change, how edits are traced, and whether locking is enough.
It succeeds when two readers collide visibly and no content is lost.


## Boundary
- ✅ Covered here
  **Editing body text from the page**: which sections are editable, which editor, what happens when two people edit at once, and how an edit gets written into `## Log`.
- ↪ Covered elsewhere
  The comment and discussion write-back path: that is finished, and belongs to `QA6`.
  Nor chat / terminal working on a question: that is `QD1`/`QD2`/`QD3`.
  Nor who is allowed to edit: that is `QE1`'s authentication.

## Diagram

```
three write-back paths that already work (QA6)      still not writable
─────────────────────────────────────────────       ──────────────────────
select a sentence → 💬 Comment → ## Comments        ## Where we are body     ❌
➕ Add to discussion          → ## Discussion       ticking ## Items to Finish ❌
resolve a comment             → [ ] becomes [x]     the state: line           ❌
                                                     an automatic ## Log line ❌

concurrency: three steps, do not skip one
  ① per-file lock    HOLD already exists in serve.py (written for one-session-per-question)
                     A is editing QE4 → B opens it and sees "JL is editing", read-only
                     ✅ a few dozen lines   ❌ if A never closes it, it stays locked (needs a timeout)
  ② optimistic       send "the version I read" with the write; reject on mismatch and ask for a retry
                     ✅ never deadlocks     ❌ a conflict means redoing the edit by hand
  ③ CRDT (Yjs)       both people type simultaneously and nothing is lost; the mature stack is
                     Yjs plus TipTap / Milkdown
                     ✅ real collaboration  ❌ markdown is no longer "just write the file";
                                              it needs a sync service in between
```

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw&frame=QE4

## Items to Finish
### The editor half
- [ ] Decide which sections are editable from the page
      All of it?
      Or start with just `## Where we are` body text, ticking `## Items to Finish`, and the `state:` line: smallest change, most of the value.
- [ ] Decide on the editor
      A plain `<textarea>` over the markdown source (zero dependencies, most honest), or TipTap / Milkdown (WYSIWYG, but the board's section grammar has to be taught to it).
- [ ] An in-page edit writes its own `## Log` line
      `## Log` is hand-written today.
      If the page can change body text without leaving a trace, the board starts lying.

### Two people at once
- [ ] Decide how far to take concurrency
      ① per-file lock / ② optimistic / ③ CRDT.
      My recommendation is ① first, and not to discuss ③ until two people really do edit one question at the same time.
- [ ] Actually have two people edit one question and verify nothing is lost
      That is the acceptance test.
      Not "a lock was added", but someone really collided and saw the warning.

## Where we are
**Writing back to markdown has worked for a while; it is just only exposed for those three comment actions.**

- Write-back that already runs
  `serve.py`'s `add_comment` / `add_discuss` / `resolve` edit `Q*.md` directly and then call `build.py` to rebuild, which is why "there is no such thing as an unsynced comment".
  Body editing rides the same path; it is not a new mechanism.
- Half of the lock already exists
  `HOLD` in `serve.py` is a per-file occupancy marker written for `QD1`'s rule (one session per question, one window per session), along with `release` / `kill_term`.
  Turning it into "one editor per question" is widening the meaning, not building from scratch.
- Why it does not hurt yet
  Bound to `127.0.0.1`, single user.
  The day either `QE1` (sharing) or `QE3` (moving into `haichat-inlab`) lands, this becomes real.
- Where the mature option fits
  For several people editing the same markdown, the industry answer is a CRDT (Yjs) with a ProseMirror-family editor (TipTap / Milkdown).
  It is the one mature component worth importing out of `QE3`, but only once "two people typing at once" is actually needed.

### Decision Now
- [ ] ✂️ Pick which sections the page may edit first
      All of it, or the minimal set this page calls smallest change with most of the value: `## Where we are` body text, ticking `## Items to Finish`, and the `state:` line.
      A tick here also closes the same row in Items to Finish.
- [ ] 🔒 Pick how far to take concurrency
      The fork is ① per-file lock, ② optimistic, ③ CRDT (Yjs); the recommendation on this page is ① first, with ③ not discussed until two people really do edit one question at the same time.
- [ ] ✏️ Pick the editor
      A plain `<textarea>` over the markdown source, which this page calls zero dependencies and most honest, or TipTap / Milkdown with the board's section grammar taught to it.

## Files
- `serve.py`
  `add_comment` / `add_discuss` / `resolve` are the working template for writing back to markdown; `HOLD` / `hold` / `release` are the half-built lock.
  Body editing goes here.
- `build.py`
  `parse_q()` knows where each `##` section starts and ends: "edit only this section" should locate through it rather than a hand-rolled regex.
- `ref/board-form.md`
  The section-grammar spec.
  Which sections the page may edit, and what an edit writes back, must line up with it.

## Glossary
CRDT: a data structure that lets several people change the same content at once without locking, merging edits automatically.
Yjs is the common implementation. per-file lock: only one person may write a given file at a time; everyone else sees "someone is editing".
`HOLD` in `serve.py` is exactly this.

## Log
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260724 1242 · Opened: JL wants to "really work on a question page: edit, comment, discuss, log the changes". The three comment actions are already done in QA6; this question owns **editing body text** and the concurrency that comes with it
