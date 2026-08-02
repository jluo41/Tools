# Driving the sentence: proving a write still lands

state: 🟡 PARTIAL · tier 1 is written and has already failed on real pages; tiers 2-4 are designed, not built
owner: JL
method: name the invariant once, cross it with every shape a sentence can take, and put the cheapest instrument that can see each failure against it

## Opening
How do we prove that every sentence-level action still targets exactly one line of Markdown and writes in the right place?

Rendering, browser extraction, and server matching each interpret the same sentence independently.
A small change in any one layer can leave the page looking healthy while comments, edits, lanes, or chat focus silently miss their source.
The test must cross every rendered sentence shape with every operation and make honest refusals part of the result.
It succeeds when each action lands once beside the intended line or clearly explains why it cannot.

**Covered elsewhere**: What the operations ARE and what they mean: `QB5` and its faces. The anchoring contract itself: `QC4a`. Driving the page in a browser at all: `QF3`, whose harness this one specialises. Whether a checker run BLOCKS a change: `QF1`.

## Diagram

```text
   ── one write, three components, no shared code ────────────────────

   ①  build.py            source line ──▶ rendered HTML
                          Python · adds badges, chips, rails, marks
                │
   ②  __boardSentenceText HTML ──▶ the string the client posts
                          JavaScript · must undo everything ① added
                │
   ③  _sentence_line      the string ──▶ one source line, or a refusal
                          Python · exact match after light md stripping

   ①→② is where every shipped failure has lived.
   Nothing in the pipeline compares ② to ③, which is why they drift silently.

   ── what each instrument can see ──────────────────────────────────
                                        ①    ②    ③   write   UI
   check.py            reads markdown   ✅    ❌   ❌    ❌     ❌
   fresh-agent read    reads markdown   ✅    ❌   ❌    ❌     ❌
   QF3 browser run     clicks the page  ✅    ~    ❌    ❌     ✅
   THIS run, tier 1    asks the page    ✅    ✅   ✅    ❌     ❌
   THIS run, tier 2-4  writes a fixture ✅    ✅   ✅    ✅     ✅
```

## Content
### §1 What has actually broken, so the list is not invented

```text
260801  ⚑ badge moved INSIDE the <p>      edit · lane · comment   ALL apparatus sentences
260801  the edit form collapsed to 1 char  edit                    every sentence
260731  writes posted location.pathname    all four writers        every tree page
260727  a lane turned <p> into <summary>   edit                    every sentence that gained a lane
260729  the Send handler dropped focus     chat                    every sentence
```

Every row shipped green, and every row was found by JL rather than by the pipeline.
Read together they say one thing: the operation did not change, the SHAPE of the sentence did, and each shape is a separate code path nobody enumerated.

### §2 The invariant, written once
For every sentence the page offers as writable, the string the client would post must equal exactly one source line after the server's normalisation, and the write must land adjacent to that line.
Both halves matter: the first is what breaks silently, and the second is what corrupts a file when the first is fixed carelessly.
A sentence the page must NOT offer as writable is part of the same invariant, because a control that cannot succeed is worse than an absent one.

### §3 The shapes, which are the rows
A shape is anything that changes the HTML around a sentence, because that is what ② has to undo.

```text
 #1   plain prose in Content                        the happy path
 #2   sentence carrying apparatus (⚑ + <details>)   BROKE 260801
 #3   ends with a `code span`                       tail-splitting logic
 #4   contains **bold**                             ③ strips it, ② must not
 #5   contains a [link](path)                       ③ strips it, ② must not
 #6   contains an inline page-id chip (`QB4c`)      rendered as an anchor
 #7   the Opening LEAD                              composed outside body()
 #8   inside a fold (Law / Glossary / Discussion)   different container
 #9   an item's explanation line under `- [ ]`      indented source
 #10  the same sentence twice on one page           ③ must REFUSE, not guess
 #11  CJK                                           no word boundaries
 #12  contains an escaped entity (' & < >)          esc() then textContent
 #13  inside a managed span (a Meeting page)        a resync would erase the edit
 #14  a paper-dialect chip (\citep, {VAL}, DR id)   the dialect rewrites the line
 #15  a line the renderer JOINED from two           no single line can match
 #16  generated text with no source at all          must not be writable
```

Shapes 15 and 16 are not hypothetical: the first run found three of them on one page, and they are the reason the run reports "unanchored" rather than "broken".

### §4 The operations, which are the columns

```text
 O1  add a typed lane        POST /_board/sentence        writes `> Lane: text`
 O2  sentence-local comment  POST /_board/comment         writes `> WHO: text · time`
 O3  edit the sentence       POST /_board/edit-sentence   replaces the line + one ✎ record
 O4  discussion line         POST /_board/discuss         writes under ## Discussion
 O5  resolve                 POST /_board/resolve         marks a thread resolved
 O6  chat focus              no write                     the packet must carry the same string
```

The chat focus writes nothing and still belongs here: it reads the sentence with the same reader, and a wrong string there sends the agent to the wrong place instead of failing loudly.

### §5 What "it works" has to mean, per cell
Five assertions, and a cell is green only when all five hold.

```text
 A1  the posted string resolves to exactly ONE source line
 A2  the write lands ADJACENT to it (end of the existing `>` run, not the top)
 A3  the file still parses and the page rebuilds with the new line visible
 A4  running the same operation twice does not duplicate or double-write
 A5  every refusal is HONEST: not-found, ambiguous, unchanged, empty, locked
```

The fifth assertion is what turns a red run into a usable report, and it is the assertion this family violated for a whole day: the server refused correctly, the page showed the refusal, and nobody was watching that corner of the screen.

### §6 Four tiers, cheapest first

```text
 T1  PARITY      no writes · no fixture · runs on a LIVE board
     Ask each page, in a real browser, what it WOULD post for every writable
     sentence; resolve each answer with the server's own matcher.
     Catches: the whole ①→② class, on every page at once.
     Cost: one browser, ~2s a page.                      sentencerun.py

 T2  NO-OP POST  no fixture · writes nothing
     Post each operation with a payload the server must REFUSE for a second
     reason ("the sentence has not changed"), which is only reachable once the
     line has been FOUND.
     Catches: the endpoint contract, the board-root resolution, auth, locks.

 T3  ROUND TRIP  a FIXTURE board · real writes
     Every shape × every operation, asserting A2, A3, A4 on the markdown diff.
     Catches: adjacency, duplication, rebuild, and every A5 refusal on purpose.

 T4  REACH       a fixture board · real clicks
     Double-click a plain sentence and an apparatus sentence, the ＋ row, the
     💬, the touch ⋯ menu: does the control OPEN, and does it target the
     sentence under the cursor?
     Catches: dead buttons, the wrong target, a form 1 character wide.
```

T1 is written and has already failed on real pages, which is the only evidence that a test is worth keeping.
T2 needs nothing new but a caller.
T3 needs the fixture in §7.
T4 is `QF3`'s harness pointed at sentences, not a second browser runner.

### §7 The fixture, and why it cannot be a real board
T3 writes, so it cannot run against a board anyone cares about, and it must be reset between runs.
One fixture page carries every shape in §3 deliberately, the way `ref/page-template.md` already carries every RENDER construct for the checker's template pass.
That page is the honest place to answer the questions nobody wants to answer on a live board: what happens on a duplicate sentence, on a sentence inside a managed span, on a locked file, on a sentence whose file changed under the browser.

### §8 What this run must never become
It must not grow a fourth reading of "what this sentence says".
The whole failure class comes from two implementations drifting, so T1 calls `window.__boardSentenceText` in the page and imports `_sentence_line` from the server rather than reimplementing either.
The day this run reimplements the matcher it starts passing while the board is broken, which is the only outcome worse than having no run at all.

### §9 The run sheet: every test, named
The matrix above says what must be covered; this is the list a person can read down and a run can print.
Six groups, thirty-seven checks, and each one is decidable by machine.

```text
A · CAN YOU SELECT IT AND GET A CONTROL
  A1  select inside a plain sentence                   -> the 💬 button appears
  A2  select inside a sentence carrying apparatus      -> appears
  A3  select inside the Opening lead                   -> appears
  A4  select inside a fold (Law / Glossary / Log)      -> appears
  A5  select inside a rendered comment or lane         -> must REFUSE
  A6  select inside a heading                          -> must REFUSE
  A7  a selection spanning two sentences               -> must REFUSE
  A8  an item's indented explanation line
  A9  touch: the ⋯ menu reaches the same three actions
  A10 keyboard focus alone reveals the rail

B · DOES THE POSTED STRING EXIST IN THE MARKDOWN
  B1  every writable sentence resolves to exactly one source line, board-wide
  B2  a sentence carrying a code span, bold, or a link
  B3  a CJK sentence
  B4  a sentence whose characters were HTML-escaped
  B5  the same sentence twice on a page          -> must refuse, never guess
  B6  a Boundary row the renderer joined from two lines
  B7  generated text with no source line at all

C · DOES THE WRITE LAND WHERE IT SHOULD
  C1  edit replaces the line and appends ONE ✎ record after existing apparatus
  C2  comment writes `> WHO: text · time` directly beneath the sentence
  C3  a lane is appended at the END of the existing `>` run, not on top of it
  C4  a discussion line lands under ## Discussion
  C5  resolve marks its thread and nothing else
  C6  the same operation twice does not duplicate
  C7  every other byte of the file is unchanged

D · ARE THE REFUSALS HONEST
  D1  not found      D2  ambiguous      D3  unchanged
  D4  empty          D5  file locked    D6  server not running

E · IS THE FORM USABLE, NOT MERELY PRESENT
  E1  the textarea is full width        E2  prefilled without the ⚑ badge
  E3  Save reloads and the record is visible
  E4  Cancel closes and writes nothing  E5  Cmd+Enter saves

F · DOES IT SURVIVE THE PAGE MOVING
  F1  after a live rebuild swaps the wrap
  F2  after tree navigation, which never reloads the document
```

Nothing here needs a human eye: A and E are measured in a real browser, B is the parity sweep, C and D are a markdown diff against a fixture.

## Aims
### Tier 1, the parity sweep
- [x] 🧪 Write it
      `sentencerun.py`: its own tab, every page, the page's own reader, the server's own matcher, no writes.
- [ ] 🩹 Make it survive a whole board
      The first page after tab creation reported zero sentences, and one page in six timed out; it needs a readiness wait and a per-page reconnect.
- [ ] 🚧 Rule what an unanchored sentence means
      The first run found three, and they are not the badge class: a joined Boundary line and generated placeholder text can never match a source line.
- [ ] 🔁 Prove it catches the real regression
      Put the ⚑ badge back into the payload on purpose and watch the run go red; a test never shown to fail is a test nobody should trust.

### Tier 2, the no-op post
- [ ] 📮 Post every operation with a payload the server must refuse for the SECOND reason
      Reaching "the sentence has not changed" proves the line was found, and nothing is written.
- [ ] 🌳 Cover both packagings and both hosts
      A tree page and the Index, over `127.0.0.1` and over the tailnet address, because the board-root resolution differs and has broken before.

### Tier 3, the round trip
- [ ] 🧱 Build the fixture page
      One page carrying all sixteen shapes in §3, plus a duplicate sentence (row 10) and a managed span.
- [ ] 🔬 Assert the markdown diff, not the page
      Exactly one line added, in the right place, and the rest of the file byte-identical.
- [ ] ♻️ Reset between runs
      The fixture is restored from a pristine copy, so a red run never poisons the next one.

### Tier 4, reach
- [ ] 🖱 Click every control on both sentence shapes
      Double-click, ＋, 💬, ⋯, and the drawer's own add row.
- [ ] 📏 Assert the form is usable, not just present
      The edit textarea was 1 character wide for a day while being perfectly present.

### The gate
- [ ] 🚦 Decide what a red run stops
      `QF1` leaves this open for the checker; this run should not invent a different answer.

## States

- 260801 CC · 🟩 The write grid is green, and it went green by finding real defects
  A second harness, `sentencewrite.py`, builds a throwaway fixture board, posts every operation against every shape, and asserts on the MARKDOWN rather than the status code: exactly one record, in the right slot, the rest of the file byte-identical, and not written twice.
  It reports 40 cells: 33 wrote correctly and 7 refused where they had to, which is the whole grid.
  Getting there fixed five defects it found, each verified by the run going from red to green: a multi-line comment broke out of its record; an identical POST appended a second copy on every appending writer, reachable by double-clicking Save; `resolve` flipped the FIRST of several identical rows and answered ok, the one endpoint that never got the ambiguity refusal the others share; `~~strike~~` and an inline image were normalization holes; and the paper dialect's chips are `<button>`s the reader deletes while the matcher kept the marker, so on a `dialect: paper` board every claim-bearing sentence was unwritable.
  Two more came from reading rather than running: the comment layer injects a `💬` marker INSIDE the paragraph for every pending comment, so one failed write poisoned that sentence permanently, and editing an item's indented explanation line rewrote it at column zero, severing it from its checkbox: the only source-corrupting case found, now refused with a message that says why.
- 260801 CC · 📋 The run sheet has real numbers, and three of them are red
  Thirty-seven checks are named in §9; fourteen have been run and passed, three have been run and FAILED, and twenty are not built yet.
  Passing: every selection case (A1 to A6), including the two that must REFUSE, which were verified by watching the button stay hidden on a rendered comment and on a heading.
  Passing: one full edit round trip (C1), performed on a real page with a real Save and then restored byte for byte, with the `✎` record landing after the existing comment rather than on top of it.
  Passing: the form itself (E1 to E3), where the textarea now measures 436px instead of one character.
  Failing: B1 on the QB5 family, 70 writable sentences with 3 unanchored, and those three are B6 and B7 rather than the badge class.
Opened 260801 when JL asked for a thorough test series for the sentence family, after a week in which three separate sentence defects reached him first.

- 260801 CC · 🧪 Tier 1 exists, and its first run was already red
  `sentencerun.py` opens its OWN tab (attaching to whatever tab is first drives the tab a person is reading, and that is both rude and unreliable), navigates each page, calls the page's own `__boardSentenceText` for every writable sentence, and resolves each answer with `_sentence_line` imported from the server.
  On the `QB5` family it read 70 writable sentences and reported three unanchored, none of them the badge class: two are `## Boundary` rows, where the renderer JOINS a bullet and its indented continuation into one paragraph so no single source line can ever match, and one is the generated "No discussion yet" placeholder, which has no source line at all.
  That is the run doing its job on day one: those three sentences almost certainly offer a ＋ and an edit control today, and every one of them would fail exactly the way JL's screenshot did.
  Two harness defects surfaced in the same run and are listed above: the first page after tab creation reported zero sentences, and one page in six timed out.

- 260801 CC · 🧹 The server had two matchers, and they disagreed where it mattered
  `add_sentence` carried its own copy of the scan and took the FIRST of several identical lines, while `edit_sentence` refused ambiguity through `_sentence_line`.
  So adding a lane to a repeated sentence could attach it under the wrong one, silently, and the shape matrix's row 10 is exactly that case.
  Both paths now share one matcher, which is also `§8`'s rule applied to the server rather than to the client.

### Decision Now
- [ ] 🧭 Rule where the fixture board lives
      A · inside the skill, beside `ref/page-template.md`, so the run ships with the thing it tests and any board can be checked without a fixture of its own.
      B · as a sibling design board under `skills/diagrams/`, so it is a real board rather than a special case.
      → CC recommends A, because the template pass already proves this shape works and a fixture nobody can see is a fixture nobody breaks.
- [ ] 🚧 Rule what the page owes an unanchored sentence
      Three exist today: a joined `## Boundary` row and generated placeholder text cannot match a source line, and no fix to the reader will change that.
      A · the page stops offering write controls on any sentence that has no source line, which is the honest UI and needs the renderer to mark them.
      B · the renderer stops joining a bullet and its continuation, so Boundary rows become writable like everything else.
      C · leave it and let each attempt fail with the server's message, which is what happens today.
      → CC recommends A, and notes that B is a bigger change than it looks, because that join is what makes a Boundary row read as one sentence.
- [ ] 🚦 Rule whether a red sentence run blocks a change
      `QF1` leaves the same question open for `check.py`, and answering it twice differently is worse than leaving it open.
      A · red blocks, because a silent write failure is the one defect class that reaches JL every time.
      B · red reports, matching `check.py` today.
      → CC recommends A for this run specifically, since it can only go red on something a person will otherwise meet by hand.

## Files
### Engines
- `../../board/haipipe-board/sentencerun.py`
  Tier 1. Its own tab, the page's reader, the server's matcher, no writes.
- `../../board/haipipe-board/live/write.py`
  The five write endpoints and the one matcher they now share.
- `../../board/haipipe-board/assets/js/40-sentence/00-apparatus.js`
  `window.__boardSentenceText`, the one reading of a sentence every writer uses.

### Input files
- `QF-execute/QF3-browser-run.md`
  The general browser run this one specialises; tier 4 belongs in its harness rather than a second one.
- `../QB-delivery/QB5-overview.md`
  The family whose operations this run covers, and the map of which face owns each one.
- `../QC-engine/QC4a-writepath.md`
  The anchoring contract the whole matrix is written against.

### Output files
- A run report
  Pages, writable sentences, shapes seen, unanchored rows with the server's own refusal text.

## Log
260801 · `sentencewrite.py` added (tier 3, fixture-based): 40 cells, 33 wrote correctly, 7 refused correctly, 0 failures. Seven defects found and fixed on the way: multi-line records, replay on four writers, resolve ambiguity, strike/image normalization, paper chips, the injected 💬 marker, and the indented-line corruption
260801 · §9 run sheet written: 37 named checks in six groups. First results: 14 pass (all of selection, one full edit round trip, the form), 3 fail (all of them sentences with no source line), 20 not yet built
260801 · Opened on JL's ask for a thorough sentence test series. Tier 1 (`sentencerun.py`) written and run: 70 writable sentences across the QB5 family, 3 unanchored (2 joined Boundary rows, 1 generated placeholder), 2 harness defects found. The server's duplicate matcher in `add_sentence` collapsed into `_sentence_line`, which also gave that path the ambiguity refusal it never had
