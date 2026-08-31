# Driving the sentence: proving a write still lands
state: 🟡 PARTIAL · tiers 1 and 3 run; the first honest board sweep is red on 3067 of 5069 sentences
owner: JL
method: name the invariant once, cross it with every shape a sentence can take, and put the cheapest instrument that can see each failure against it

## Opening
How do we prove that a sentence-level action still targets exactly one line of Markdown and writes in the right place?
A sentence-level action is anything that starts by picking one sentence: a comment, an edit, a lane, or a chat focus.
Three pieces of code read that sentence, they share no code, and any one can drift while the page still looks healthy.
Then the control opens, the reader types, and nothing lands.
This page owns the run that crosses every shape a sentence takes with every operation that writes one.

**What a shape is**: Anything that changes the HTML around a sentence, such as a `code span`, an attached badge, or being joined into one paragraph with the lines beside it.
A shape matters because each one is a separate code path in the reader, and nobody enumerated them.
The list grows every time the renderer learns a new trick, so it lives in `### 3` rather than in this paragraph.

**What unanchored means**: A sentence the page offers as writable whose text matches no single source line.
Unanchored is not the same as broken.
A paragraph joined from three source lines and a generated placeholder can never match one line, and the honest repair is to stop offering the control rather than to fix the reader.

**Covered elsewhere**: What the operations ARE and what they mean: `QB8`, and `QB8e` for the record lifecycle.
The anchoring contract itself: `QC4a`.
Driving the page in a browser at all: `QF3`, whose harness this one specialises.
Whether a checker run BLOCKS a change: `QF1`.

## Diagram
**One write, three components**: the three readings of a sentence, and the gap where every shipped failure has lived.

```text
   ── one write, three components, no shared code ────────────────────

   ①  build.py            source line ──▶ rendered HTML
                          Python · adds badges, chips, page lists, marks
                │
   ②  __boardSentenceText HTML ──▶ the string the client posts
                          JavaScript · must undo everything ① added
                │
   ③  _sentence_line      the string ──▶ one source line, or a refusal
                          Python · exact match after light md stripping

   ①→② is where every shipped failure has lived.
   Nothing in the pipeline compares ② to ③, which is why they drift silently.
```

**What each instrument can see**: which of the three components every existing check can reach, and where this run is the only one looking.

```text
                                        ①    ②    ③   write   UI
   check.py            reads markdown   ✅    ❌   ❌    ❌     ❌
   fresh-agent read    reads markdown   ✅    ❌   ❌    ❌     ❌
   QF3 browser run     clicks the page  ✅    ~    ❌    ❌     ✅
   THIS run, tier 1    asks the page    ✅    ✅   ✅    ❌     ❌
   THIS run, tier 3    writes a fixture ✅    ✅   ✅    ✅     ❌
   THIS run, tier 4    clicks a fixture ✅    ✅   ✅    ✅     ✅
```

## Content
### 1 · What has actually broken, so the list is not invented
**The shipped failures**: every sentence defect that reached a reader, with the operation it broke and the blast radius.

```text
260801  ⚑ badge moved INSIDE the <p>      edit · lane · comment   ALL apparatus sentences
260801  the edit form collapsed to 1 char  edit                    every sentence
260731  writes posted location.pathname    all four writers        every tree page
260727  a lane turned <p> into <summary>   edit                    every sentence that gained a lane
260729  the Send handler dropped focus     chat                    every sentence
260802  the live shell moved the page      the RUN ITSELF          all 55 pages, silently
```

📌 The list is evidence rather than imagination: each row shipped green, and each was found by a person rather than by the pipeline.

Read together they say one thing.
The operation did not change, the SHAPE of the sentence did, and each shape is a separate code path nobody enumerated.
The last row is the same failure one level up.
`serve.py` began wrapping a page in a three-pane shell, the real document moved into an iframe, and tier 1 kept evaluating in the outer window, so it reported every page unreadable and nobody read the report.

### 2 · The invariant, written once
**The invariant, in two halves**: what must be true of every writable sentence, and what each half costs when it fails.

```text
   ⚖️ ONE SENTENCE, TWO OBLIGATIONS

   🎯 half 1   the posted string  ══▶  exactly ONE source line
   📍 half 2   the write          ══▶  lands ADJACENT to that line
   🚫 corollary  a sentence that cannot succeed is not offered at all

   💥 half 1 fails SILENTLY · half 2 CORRUPTS the file
```

📌 Everything below is this one sentence crossed with something: a shape, an operation, an assertion, or a tier.

For every sentence the page offers as writable, the string the client would post must equal exactly one source line after the server's normalisation, and the write must land adjacent to that line.
Both halves matter: the first is what breaks silently, and the second is what corrupts a file when the first is fixed carelessly.
A sentence the page must NOT offer as writable is part of the same invariant, because a control that cannot succeed is worse than an absent one.

### 3 · The shapes, which are the rows
**The shape matrix**: every form a sentence takes in the rendered page, and what each one does to the reader that has to undo it.

```text
 #1   plain prose in Content                        the happy path
 #2   sentence carrying apparatus (⚑ + <details>)   BROKE 260801
 #3   ends with a `code span`                       tail-splitting logic
 #4   contains **bold**                             ③ strips it, ② must not
 #5   contains a [link](path)                       ③ strips it, ② must not
 #6   contains an inline page-id chip (`QB4`)       rendered as an anchor
 #7   the Opening LEAD                              composed outside body()
 #8   inside a fold (Law / Glossary / Discussion)   different container
 #9   an item's explanation line under `- [ ]`      indented source
 #10  the same sentence twice on one page           ③ must REFUSE, not guess
 #11  CJK                                           no word boundaries
 #12  contains an escaped entity (' & < >)          esc() then textContent
 #13  inside a managed span (a Meeting page)        a resync would erase the edit
 #14  a paper-dialect chip (\citep, {VAL}, Q id)    the dialect rewrites the line
 #15  a paragraph JOINED from several source lines  no single line can match
 #16  generated text with no source at all          must not be writable
 #17  a markdown table row                          ③ skips `|` by design
```

📌 A shape is anything that changes the HTML around a sentence, because that is what ② has to undo.

Rows 15, 16 and 17 are not hypothetical, and the board sweep in `### 6` says how large they are.
Row 15 was written on 260801 as a `## Boundary` curiosity and is far bigger than that: every Opening on-stage paragraph and every `More details` part is several source lines joined into one paragraph, which is 215 sentences on this board alone.
Row 17 was not on the list at all until the sweep met 56 of them, because `_sentence_line` skips any line starting with `|` and nothing told the page to stop offering the control.
These three are the reason the run reports unanchored rather than broken.

### 4 · The operations, which are the columns
**The operation matrix**: the seven things a reader can start from one sentence, and what each writes.

```text
 O1  add a typed lane        POST /_board/sentence        writes `> Lane: text`
 O2  card on marked words    POST /_board/card            writes `> Card <words>: text`
 O3  sentence-local comment  POST /_board/comment         writes `> WHO: text · time`
 O4  edit the sentence       POST /_board/edit-sentence   replaces the line + one ✎ record
 O5  discussion line         POST /_board/discuss         writes under ## Discussion
 O6  resolve                 POST /_board/resolve         marks a thread resolved
 O7  chat focus              no write                     the packet must carry the same string
```

📌 Six of the seven write; the seventh reads with the same reader and is in scope for that reason alone.

The chat focus writes nothing and still belongs here.
It reads the sentence with the same reader, and a wrong string there sends the agent to the wrong place instead of failing loudly.
The card is the newest writer and the one tier 3 never reaches: it shares the same matcher, and `cli/sentencewrite.py`'s five endpoints do not include `/_board/card`.

### 5 · What "it works" has to mean, per cell
**The five assertions**: what one cell of the matrix has to satisfy before it may be called green.

```text
 A1  the posted string resolves to exactly ONE source line
 A2  the write lands ADJACENT to it (end of the existing `>` run, not the top)
 A3  the file still parses and the page rebuilds with the new line visible
 A4  running the same operation twice does not duplicate or double-write
 A5  every refusal is HONEST: not-found, ambiguous, unchanged, empty, locked
```

📌 A cell is green only when all five hold, and A5 is the one that turns a red run into a usable report.

The fifth assertion is the one this family violated for a whole day: the server refused correctly, the page showed the refusal, and nobody was watching that corner of the screen.
It has a second half nobody wrote down until the board sweep printed 3067 refusals at once.
A refusal has to be READABLE, and today twenty of the twenty-four refusal strings in `live/write.py` are written in Chinese on a board whose own rule is English only.
It also has to be reported as a refusal: the run currently prints every one of them as `FAIL`, which buries the six sentences that are genuinely drifting under three thousand that are behaving exactly as designed.

### 6 · Four tiers, cheapest first
**The four tiers**: what each one costs, what it can see, and what exists today.

```text
 T1  PARITY      no writes · no fixture · runs on a LIVE board          ✅ RUNS
     Ask each page, in a real browser, what it WOULD post for every writable
     sentence; resolve each answer with the server's own matcher.
     Catches: the whole ①→② class, on every page at once.
     Cost: one browser, ~2s a page.                      cli/sentencerun.py

 T2  NO-OP POST  no fixture · writes nothing                            ⬜ NOT BUILT
     Post each operation with a payload the server must REFUSE for a second
     reason ("the sentence has not changed"), which is only reachable once the
     line has been FOUND.
     Catches: the endpoint contract, the board-root resolution, auth, locks.

 T3  ROUND TRIP  a FIXTURE board · real writes                          ✅ RUNS
     Every shape × the five write endpoints, asserting A2, A3, A4 on the markdown diff.
     Catches: adjacency, duplication, rebuild, and every A5 refusal on purpose.
     8 shapes × 5 endpoints = 40 cells.                 cli/sentencewrite.py

 T4  REACH       a fixture board · real clicks                          ⬜ NOT BUILT
     Double-click a plain sentence and an apparatus sentence, the ＋ row, the
     💬, the touch ⋯ menu: does the control OPEN, and does it target the
     sentence under the cursor?
     Catches: dead buttons, the wrong target, a form 1 character wide.
```

📌 Cheapest first is not a preference: T1 runs on a live board with no setup, so it is the only tier that can run after every change.

T2 needs nothing new but a caller, T3 needs the fixture in `### 7`, and T4 is `QF3`'s harness pointed at sentences rather than a second browser runner.
A tier is only worth keeping once it has gone red on something real, which is the whole argument of the paragraph below.

#### 6.1 · What the first honest board sweep found
(the run had been reporting an empty board for a day, and the first real read was red)
The 260801 run read 70 sentences on one family and was believed.
The 260802 run, after the shell defect in `### 1` was fixed, read the whole board: 55 pages, 5069 writable sentences, 0 unreadable, and 3067 that resolve to no single source line.

```text
   ── 3067 unanchored, by cause ──────────────────────────────────────

   2724   an item's indented explanation line       #9   REFUSED, correctly
    215   a paragraph joined from several lines     #15  can never match
     68   generated text with no source line        #16  can never match
     56   a markdown table row                      #17  skipped by design
      4   the same sentence twice on a page         #10  REFUSED, correctly
   ────
   3067   of 5069 · 2002 resolve cleanly
```

Not one of these is the ①→② drift the run was built to catch, which is the good news.
Every one of them is the OTHER half of the invariant in `### 2`: the page is offering a write control on three sentences in five that the server is right to refuse.
The largest class is a Files row's own description line, which sits indented under its `- ` item, so every Files section on the board is a field of controls that cannot succeed.

### 7 · The fixture, and why it cannot be a real board
**Why T3 needs a board nobody reads**: what the fixture buys, and the four questions only it can answer.

```text
   🧪 A BOARD BUILT TO BE BROKEN

   ✍️ it WRITES        a live board would keep the test's litter
   ♻️ it RESETS        restored from a pristine copy between every cell
   🎭 it is HOSTILE    duplicate lines, a managed span, a locked file
   📐 same trick as    ref/page-template.md for the render checker

   🚫 never point T3 at a board anyone is reading
```

📌 T3 writes, so it needs a board whose corruption costs nothing and whose reset is a file copy.

One fixture page carries every shape in `### 3` deliberately, the way `ref/page-template.md` already carries every RENDER construct for the checker's template pass.
That page is the honest place to answer the questions nobody wants to answer on a live board: what happens on a duplicate sentence, on a sentence inside a managed span, on a locked file, and on a sentence whose file changed under the browser.
`cli/sentencewrite.py` builds it, runs it and throws it away today, with 8 of the 17 shapes in it.

### 8 · What this run must never become
**The one rule**: three readings of a sentence exist, and this run may not add a fourth.

```text
   🚫 NEVER A FOURTH READING OF "WHAT THIS SENTENCE SAYS"

   ①  build.py              renders it
   ②  __boardSentenceText   the page's own reader     ◀── T1 CALLS this
   ③  _sentence_line        the server's matcher      ◀── T1 IMPORTS this

   ⚠️ a run with its own reader goes green while the board is broken
```

📌 The rule is what keeps a passing run meaningful, and it is cheap to break by accident.

The whole failure class comes from two implementations drifting, so T1 calls `window.__boardSentenceText` in the page and imports `_sentence_line` from the server rather than reimplementing either.
The day this run reimplements the matcher it starts passing while the board is broken, which is the only outcome worse than having no run at all.
T3 is the deliberate exception and states it in its own docstring: its oracle for WHERE a record belongs is written from the rule rather than imported from `live/write.py`, because an oracle that shares the implementation cannot catch the implementation.

### 9 · The run sheet: every test, named
**The run sheet**: six groups of named checks, each decidable by machine, and each with a current result.

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
  A10 keyboard focus alone reveals the page list

B · DOES THE POSTED STRING EXIST IN THE MARKDOWN
  B1  every writable sentence resolves to exactly one source line, board-wide
  B2  a sentence carrying a code span, bold, or a link
  B3  a CJK sentence
  B4  a sentence whose characters were HTML-escaped
  B5  the same sentence twice on a page          -> must refuse, never guess
  B6  a paragraph the renderer joined from several lines
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

📌 Nothing here needs a human eye: A and E are measured in a real browser, B is the parity sweep, C and D are a markdown diff against a fixture.

Thirty-seven checks in six groups.
The 260801 pass recorded fourteen green, three red and twenty not built.
Today's sweep turns B5 green, because four duplicate sentences were refused rather than guessed, and it puts a board-wide number under the three that stay red.
B1 is the loudest of them: 2002 of 5069 sentences resolve, and B6 and B7 now carry a measured count each rather than a single example.

## Aims
### Decision Now

- [ ] 🚧 What does the page owe a sentence it can never write to?
      📍 `Part` `### 3 · The shapes, which are the rows`
      🔔 `Why now` The 260802 board sweep put a number on it: 3067 of 5069 writable sentences resolve to no single source line, and 2724 of those are an item's indented explanation line, which is every Files row on the board. The page draws ＋, 💬 and an edit control on all of them today.
      ⭐ `A ·` the renderer marks a sentence with no source line and the page draws no write control on it. This is the honest UI and it is what `### 2`'s third clause already requires; it costs a pass in the address stage and a class in the CSS.
      `B ·` teach `_sentence_line` to write an indented line back at its own indent, which converts 2724 refusals into writes rather than removing the controls. It is the larger change and it touches the one source-corrupting case in the file.
      `C ·` leave it and let each attempt fail with the server's message, which is what happens today.
      🛑 `Blocks` A3.2, and B1 in `### 9` stays red until one of these lands.
      🤖 `If nobody answers` A. It is reversible, it needs no change to the matcher, and B remains available afterwards for the indented case alone.

- [ ] 🚦 Does a red sentence run block a change, or only report it?
      📍 `Part` `### 6 · Four tiers, cheapest first`
      🔔 `Why now` `QF1` leaves the same question open for `check.py`, and answering it twice differently is worse than leaving it open. The sweep now exits 1 on 3067 rows, so today it would block everything.
      ⭐ `A ·` red blocks, once A5.1 has split refusals from mismatches. A silent write failure is the one defect class that has reached a person every single time, and after the split a red run means a real drift.
      `B ·` red reports, matching `check.py` today. Cheap, and only as good as whoever reads the output.
      🛑 `Blocks` P1, and nothing else.
      🤖 `If nobody answers` B, because A is unsafe until A5.1 lands.

- [ ] 🧭 Where does the fixture board live?
      📍 `Part` `### 7 · The fixture, and why it cannot be a real board`
      🔔 `Why now` `cli/sentencewrite.py` builds its fixture inline today, so the shapes it tests are a Python string rather than a board anyone can open and extend.
      ⭐ `A ·` inside the skill, beside `ref/page-template.md`, so the run ships with the thing it tests and any board can be checked without a fixture of its own. The template pass already proves this shape works.
      `B ·` as a sibling design board under `skills/diagrams/`, so it is a real board rather than a special case, at the cost of a board nobody reads drifting from the shapes it is supposed to carry.
      🛑 `Blocks` A7.1.
      🤖 `If nobody answers` A.


### A3 · 🔤 The shapes, which are the rows
- 🔨 A3.1 · The shape list matches what a board actually contains, rather than what the writer remembered.
  **Done when:** Every shape the board sweep meets is a numbered row in `### 3`, and every row is either covered by a tier or recorded as out of scope.
  **Now:** Seventeen rows. The 260802 sweep added `#17`, the table row, and corrected `#15` from a `## Boundary` curiosity to the joined paragraph that every Opening and every `More details` part is. Nothing yet says which tier owns each row.
- 🧠 A3.2 · The page stops offering a write control on a sentence that cannot take one.
  **Done when:** The renderer marks a sentence with no single source line, and no ＋, 💬 or edit control is drawn on it.
  **Now:** Waiting on the first Decision Now row. The size is measured and the repair is not chosen.

  **Plan:** Start with `#9`, the indented item explanation, which is 2724 of the 3067.

### A5 · ✅ What "it works" has to mean, per cell
- ⬜ A5.1 · A correct refusal is reported as a result, not as a failure.
  **Done when:** The run splits refusal from mismatch in its own output, and exits red only on a mismatch.
  **Now:** Not started. The run prints every refusal as `FAIL` and exits 1, so a correct refusal and a real drift are indistinguishable in its output.
- ⬜ A5.2 · Every refusal a reader can meet is written in English.
  **Done when:** Every refusal string in `live/write.py` reads in English, which is the rule the rest of the board already follows.
  **Now:** Not started. Twenty of the twenty-four refusal strings in `live/write.py` are Chinese, on a board whose own checker reports CJK as a finding.


### A6 · 🪜 Four tiers, cheapest first
- ✅ A6.1 · Tier 1 reads every page of a board in one pass.
  **Done when:** A full-board sweep reports zero unreadable pages and zero timeouts.
  **Now:** 55 pages, 0 unreadable, 0 timeouts on 260802. The per-page reconnect and the settle wait were already in `cli/sentencerun.py`; what stopped it was the live shell moving the document into an iframe, fixed by asking the server for `?pane=page`.
- ⬜ A6.2 · Tier 1 is proven to catch the regression it was built for.
  **Done when:** Putting the ⚑ badge back into the payload turns the run red, and taking it out turns it green again.
  **Now:** Not started. The run has gone red on real defects, but never on a defect put back deliberately, which is the only proof that it would catch that class again.
- ⬜ A6.3 · Tier 2 reaches the endpoint contract without writing anything.
  **Done when:** Each of the five write endpoints answers the "unchanged" refusal from a tree page and from the Index, over `127.0.0.1` and over the tailnet address.
  **Now:** Not started. Nothing new is needed but a caller.
- ⬜ A6.4 · Tier 4 proves each control opens and targets the sentence under the cursor.
  **Done when:** `QF3`'s harness opens the double-click, ＋, 💬 and ⋯ paths on a plain and an apparatus sentence, and asserts the edit form's measured width.
  **Now:** Not started. It belongs in `QF3`'s harness rather than in a second browser runner.


### A7 · 🧱 The fixture, and why it cannot be a real board
- 🔨 A7.1 · The fixture carries every shape in `### 3`.
  **Done when:** All seventeen shapes appear in the fixture pages, including the joined paragraph, the managed span and the table row.
  **Now:** 8 of 17 shapes: plain, apparatus, code span, bold, link, CJK, escaped punctuation, and the duplicate line. The missing nine include the managed span, the joined paragraph and the table row, which are the three the board sweep says matter most.
- ✅ A7.2 · Tier 3 asserts the markdown diff rather than the status code.
  **Done when:** Every cell asserts one record in the right slot with the rest of the file byte-identical, and a deliberate refusal counts as a pass.
  **Now:** 40 cells on 260801: 33 wrote correctly and 7 refused where they had to, each asserted on the markdown rather than the status code, with the file byte-identical elsewhere.


### A9 · 📋 The run sheet: every test, named
- 🔨 A9.1 · Every named check has a result.
  **Done when:** All thirty-seven checks in `### 9` report pass or fail, and none is listed as not built.
  **Now:** Fifteen green, three red, nineteen not built. B5 turned green on the sweep's four correctly refused duplicates; B1 now carries a board-wide number instead of one family's, and B6 and B7 became measured counts rather than examples.


### P · 🏁 Page-level
- 🧠 P1 · A red sentence run has one ruled consequence, and it is the same one `QF1` gives its checker.
  **Done when:** The rule is written on both pages, in the same words.
  **Now:** Waiting on the second Decision Now row, which `QF1` must answer in the same words.


## Files
### ⚙️ Engines · what RUNS this subject
- `../../board/haipipe-board/cli/sentencerun.py`
  Tier 1. Its own tab, the page's reader, the server's matcher, no writes. Asks for `?pane=page` so it reads the document rather than the shell around it.
- `../../board/haipipe-board/cli/sentencewrite.py`
  Tier 3. Builds a throwaway fixture board, posts every operation against every shape, and asserts on the markdown diff.
- `../../board/haipipe-board/live/write.py`
  The five write endpoints, the one matcher they share, and the five refusal strings A5.2 is about.
- `../../board/haipipe-board/assets/js/40-sentence/00-apparatus.js`
  `window.__boardSentenceText`, the one reading of a sentence every writer uses.
- `../../board/haipipe-board/live/shell.py`
  The three-pane shell whose iframe made tier 1 blind for a day.

### 📥 Input files · what the work READS
- `9-QF-execute/QF3-browser-run/QF3-browser-run.md`
  The general browser run this one specialises; tier 4 belongs in its harness rather than a second one.
- `../../QS-sentence/QS1-overview/QS1-overview.md`
  The family whose operations this run covers, and the map of which face owns each one.
- `../../QC-engine/QC3a-writepath/QC3a-writepath.md`
  The anchoring contract the whole matrix is written against.

### 📤 Output files · what a BUILD writes
- `board/QS/QS4-sentence-run.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit.

## Log
- 260806 2206 · [REVISE-CC] swept to the 260806 architecture; `### 4` gained the card writer it never listed (`POST /_board/card`, live in `cli/serve.py` since 260802) so the matrix reads seven operations with tier 3's five endpoints named as the gap, the refusal count corrected from five to twenty of twenty-four Chinese strings in `live/write.py` (§5, A5.2, States), and two dead examples repointed: the `QB4c` chip (archived) and the `DR id` dialect token (`_DIALECT` carries a Q id, never a DR)
260802 · 🌐 A BROWSER tier joined the run: `tests/drive_sentence.py`, 31 checks green, one screenshot and one row per gesture into a `report.md`. It covers what no tier here could see, because every tier so far reads FILES: a card opening on its words, the badge counting lanes and not cards, a broken span rendering loud, two cards on one sentence, a three-line card body arriving whole, three refusals keeping the composer open, a comment still finding its anchor on a sentence that already carries a card, and the scroll and open sections surviving a save. It builds its own throwaway board (`tests/fixture_board.py`, ten targets including a sentence written twice) rather than driving a page anyone reads: the first version drove `QB8`, left five cards on it, and its second run could not tell a pass from a break
260802 1434 · The page was brought to the QB4 contract and its numbers were re-measured rather than carried over. Tier 1 turned out to have been blind since the live shell started wrapping a page in three panes: `serve.py` answers a page URL with a frame whose real document sits in an iframe, `Runtime.evaluate` reads the outer window, and the run reported all 55 pages `SKIP this page has no __boardSentenceText`, which is indistinguishable from a clean board. `tree_url` now asks for `?pane=page`. The first honest sweep: 55 pages, 5069 writable sentences, 0 unreadable, 3067 unanchored, and not one of them the ①→② drift the run was built for. They split 2724 indented item explanations, 215 joined paragraphs, 68 generated placeholders, 56 table rows and 4 duplicates, which says the page is offering a write control on three sentences in five that the server is right to refuse. `### 3` gained `#17` and rewrote `#15`; `### 6` gained the sweep; `### 5` gained the second half of A5, that a refusal must also be readable and must not be printed as a failure
260801 · `sentencewrite.py` added (tier 3, fixture-based): 40 cells, 33 wrote correctly, 7 refused correctly, 0 failures. Seven defects found and fixed on the way: multi-line records, replay on four writers, resolve ambiguity, strike/image normalization, paper chips, the injected 💬 marker, and the indented-line corruption
260801 · §9 run sheet written: 37 named checks in six groups. First results: 14 pass (all of selection, one full edit round trip, the form), 3 fail (all of them sentences with no source line), 20 not yet built
260801 · Opened on JL's ask for a thorough sentence test series. Tier 1 (`sentencerun.py`) written and run: 70 writable sentences across the QB8 family, 3 unanchored (2 joined Boundary rows, 1 generated placeholder), 2 harness defects found. The server's duplicate matcher in `add_sentence` collapsed into `_sentence_line`, which also gave that path the ambiguity refusal it never had

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0