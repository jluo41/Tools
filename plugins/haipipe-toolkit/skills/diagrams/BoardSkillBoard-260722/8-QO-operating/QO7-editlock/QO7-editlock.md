# In-page editing and locks

state: 🔴 OPEN
owner: CC
method: start with a per-file lock (`HOLD` already exists); do not reach for a CRDT first

## Opening
How can people edit a board page in place without letting simultaneous changes overwrite the Markdown source?

In-page editing would turn the board from a reading and comment surface into a real workbench.
The hard part is that Markdown is a file, not a collaborative database, so the last writer can erase the first.
The answer determines which sections can change, how edits are traced, and whether locking is enough.
It succeeds when two readers collide visibly and no content is lost.

**Covered elsewhere**: The comment and discussion write-back path: that is finished, and belongs to `QB8 §5`. Nor replacing ONE sentence in place: that shipped 260729 and belongs to `QB8 §6`, whose own State names this page for locks and concurrent writers. Nor chat / terminal working on a question: that is `QD1`/`QD2`/`QD3`. Nor who is allowed to edit: that is `QE1`'s authentication.


## Diagram

```
write-back paths that already work (QB8)            still not writable
─────────────────────────────────────────────       ──────────────────────
select a sentence → 💬 Comment → > Comment WHO      a whole ## States body    ❌
select a sentence → ✎ Edit     → the line replaced  ticking ## Aims rows      ❌
➕ Add to discussion           → ## Discussion      the state: line           ❌
➕ card / lane / diagram row   → under the sentence a ## Log line per edit     ❌

concurrency: three steps, do not skip one
  ① per-file lock    HOLD already exists in live/base.py (written for one-session-per-question)
                     A is editing QE4 → B opens it and sees "JL is editing", read-only
                     ✅ a few dozen lines   ❌ if A never closes it, it stays locked (needs a timeout)
  ② optimistic       send "the version I read" with the write; reject on mismatch and ask for a retry
                     ✅ never deadlocks     ❌ a conflict means redoing the edit by hand
  ③ CRDT (Yjs)       both people type simultaneously and nothing is lost; the mature stack is
                     Yjs plus TipTap / Milkdown
                     ✅ real collaboration  ❌ markdown is no longer "just write the file";
                                              it needs a sync service in between
```


## Aims
### The editor half
- [ ] Decide which sections are editable from the page
      All of it?
      Or start with just `## States` body text, ticking `## Aims` rows, and the `state:` line: smallest change, most of the value.
      One sentence at a time is already done and is not the open part.
- [ ] Decide on the editor
      A plain `<textarea>` over the markdown source (zero dependencies, most honest), or TipTap / Milkdown (WYSIWYG, but the board's section grammar has to be taught to it).
- [ ] An in-page edit writes its own `## Log` line
      `## Log` is hand-written today, with one exception: archiving a page from the index writes its own dated line (`live/structure.py`).
      A single-sentence edit already leaves a `> ✎` record beside the sentence, so that one path is traced without a Log line.
      A section-sized edit has no trace at all yet, and if the page can change body text without leaving one, the board starts lying.

### Two people at once
- [ ] Decide how far to take concurrency
      ① per-file lock / ② optimistic / ③ CRDT.
      My recommendation is ① first, and not to discuss ③ until two people really do edit one question at the same time.
- [ ] Actually have two people edit one question and verify nothing is lost
      That is the acceptance test.
      Not "a lock was added", but someone really collided and saw the warning.

## States
**Writing back to markdown has worked for a while; it is just only exposed one sentence or one remark at a time, never a whole section.**

- Write-back that already runs
  `live/write.py`'s `add_comment` / `edit_sentence` / `add_discuss` / `add_sentence` / `add_card` / `add_diagram` edit the page's own `.md` directly; `cli/serve.py` only routes the POST and calls `build.py` to rebuild, which is why "there is no such thing as an unsynced comment".
  The writers moved out of `serve.py` into `live/` on 260731 under `gate_live.py`'s response-identical gate.
  `resolve` (flip `- [ ]` to `- [x]`) is still handled server side but nothing under `assets/js` posts to it any more.
  Body editing rides the same path; it is not a new mechanism.
- Half of the lock already exists
  `HOLD` is a per-file occupancy dict in `live/base.py`, written for `QD1`'s rule (one session per question, one window per session), with `hold` / `release` / `park` / `kill_term` in `live/term.py`.
  Turning it into "one editor per question" is widening the meaning, not building from scratch.
- Why it does not hurt yet
  Bound to `127.0.0.1` by default, single user, no auth (`--host` can override it; that is `QE6`).
  `QE3` has already landed: `haichat-inlab` gained `boards_api.py` on `feat/haichat-board`, which imports these same writers.
  So the one remaining gate is `QE1`'s auth; the day it lands and a second person can write, this becomes real.
- Where the mature option fits
  For several people editing the same markdown, the industry answer is a CRDT (Yjs) with a ProseMirror-family editor (TipTap / Milkdown).
  It is the one mature component worth importing out of `QE3`, but only once "two people typing at once" is actually needed.

### Decision Now
- [ ] ✂️ Pick which sections the page may edit first
      All of it, or the minimal set this page calls smallest change with most of the value: `## States` body text, ticking `## Aims` rows, and the `state:` line.
      A tick here also closes the same row in Aims.
- [ ] 🔒 Pick how far to take concurrency
      The fork is ① per-file lock, ② optimistic, ③ CRDT (Yjs); the recommendation on this page is ① first, with ③ not discussed until two people really do edit one question at the same time.
- [ ] ✏️ Pick the editor
      A plain `<textarea>` over the markdown source, which this page calls zero dependencies and most honest, or TipTap / Milkdown with the board's section grammar taught to it.

## Files
- `live/write.py`
  `add_comment` / `edit_sentence` / `add_discuss` are the working template for writing back to markdown.
  Body editing goes here.
- `cli/serve.py`
  The POST router (`ACTS`) and the rebuild call after every successful write.
  A section-editing endpoint is registered here.
- `live/base.py` and `live/term.py`
  `HOLD` (the per-file dict) plus `hold` / `release` / `park` / `kill_term` are the half-built lock.
- `src/parse.py`
  `parse_page()` and `split_sections()` know where each `##` section starts and ends: "edit only this section" should locate through them rather than a hand-rolled regex.
- `ref/board-form.md`
  The section-grammar spec.
  Which sections the page may edit, and what an edit writes back, must line up with it.

## Glossary
CRDT: a data structure that lets several people change the same content at once without locking, merging edits automatically.
Yjs is the common implementation. per-file lock: only one person may write a given file at a time; everyone else sees "someone is editing".
`HOLD` in `live/base.py` is exactly this.

## Log
- 260806 · [REVISE-CC] swept to the 260806 architecture; the write-back facts moved to `live/write.py` / `live/base.py` / `src/parse.py`, the retired `## Items to Finish` and `## Where we are` names became `## Aims` and `## States`, the retired `QA6` pointer became `QB8`, the shipped single-sentence edit (`QB8 §6`, 260729) is no longer listed as not writable, and `QE3` is recorded as landed
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260724 1242 · Opened: JL wants to "really work on a question page: edit, comment, discuss, log the changes". The three comment actions are already done in QA6; this question owns **editing body text** and the concurrency that comes with it
