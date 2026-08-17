# Outline · read a page one part at a time
state: 🟡 REOPENED 260817 · OUTLINE is now a phase, the plan is a FILE · open: 16 QPf plans unapproved, bibex read one-way
owner: CC
method: a line says which part it belongs to; the tab reads that and regroups the page; since 260817 it also reads the page's own PLAN file and what each bullet owes; no AI when you open it
session: 190ceaff-4d09-4915-8536-5ce0f28913ec

## Opening
Can a page be read one part at a time, with that part's goals and progress shown together?
Today a page keeps its goals in one list and its progress in another, so reading about one part means jumping between lists.
Nothing on the page says which goal belongs to which part, so a machine has to be told.
This page decides how a line says that, and builds a tab that reads it.

**Where the answer comes from**: the page itself, never an AI. A goal written `A2.1` already says part 2. For a line that says nothing, you write a small mark, `§2`, at the front.

**Its twin**: `QPf1` is the 📂 tab, which shows what a page's FOLDER holds. This is the 🧭 tab, which shows what a page's WRITING holds. Neither one stores anything.

**Covered elsewhere**: the list of plugin names, which this one is deliberately not on, is `../../../board/haipipe-plugin/ref/roster.md`. The rules about parts, goals, and progress belong to `/haipipe-page`.


## Diagram
**One mark, one read, two views**: the page says where each line goes, and the tab only sorts.

```text
  📄 the page                     🧭 the tab · read fresh every time
  ┌─────────────────────┐         ┌──────────────────────────────┐
  │ ## Content          │         │ what is this page for?        │
  │  ### 1 ·  ### 2 ·   │  ──▶    │ ███████░  10 of 11 done       │
  │ ## Aims             │         ├──────────────────────────────┤
  │  - A1.1 · …         │         │ [🧭 By part]  [🚦 What is left]│
  │  - [ ] §2 …         │         │                               │
  │ ## States           │         │  1 · … the part's own goals   │
  │ ## Files  `f.py` §1 │         │  2 · … and its own progress   │
  └─────────────────────┘         │  🌐 the whole page            │
       ✍️ the writer says where    └──────────────────────────────┘
          each line belongs
```

## Content
### 1 · How a line says which part it belongs to
**Two ways, and the first one is free**: most lines already say it; the mark is for the rest.

```text
  ① already said       ### A3 group · id A3.1     this is part 3
     (nothing to do)   ### P  group · id P1       this is the whole page

  ② the §N mark · WHERE it sits is what makes it a mark
     🎯 Aims    - [x] 📂 §1 the text …     at the FRONT
     📍 States  §1 shipped 260815 …        at the FRONT
     📎 Files   `build.py` §1 §2           at the END, may be several
     🗃 Log     never marked               it is a diary, not a part

  ✋ these look the same but are not marks, all seen on real pages
     `QB6` §7 · [QB7 §3](…)   a part of ANOTHER page
     §5.1 · §4.3              a smaller piece inside part 5
     §Required Inputs         a name, not a number
     "Every number §4 prints" a paper's own section, in a sentence
```
📌 Most lines already say which part they belong to; for the rest you write a small mark like §2.

A page written the normal way needs no mark at all.
Its goals are already grouped `### A3` and numbered `A3.1`, and both mean part 3.
`P1` already means the whole page.
This page is its own proof: every one of its goals lands in the right part, with no mark written anywhere.

The mark is for what that leaves out: pages written before the numbering, and stray lines that sit outside any group.
The mark is `§` and a number, and the number is a part of THIS page's own Content.

WHERE the mark sits is what makes it a mark.
The `§` sign was used on these boards long before this tab, and a paper page writes `§4` in normal sentences to mean the paper's own section 4.
Nothing about the characters can tell those apart.
So a mark is only read in a place where a sentence would not put one.
On a goal or a progress line it sits at the front, before the words.
On a file line it sits at the end, and there may be several, because one file often serves several parts.
A `§4` in the middle of a sentence is just writing, and is left alone.

A line with no mark belongs to the whole page.
So an old page with no marks still reads fine; it just shows as one 🌐 card, which is honest but tells you little.
Diary lines in `## Log` never take a mark, because cutting a diary into parts loses the story.

The mark points by number, so whoever renumbers the parts has to fix the marks in the same edit.
A mark pointing past the last part is caught and named.
A mark pointing at the wrong part is not, because it still points at a real one.

### 2 · The tab, read fresh every time you open it
**One read does both jobs**: the same pass checks the page and draws it.

```text
  ── what you see first ─────────────────────────────────
  🧭 QPf11-pagex
  How does a page borrow a file from another page …?     ← the page's
  ███████░  11 of 12 done · ⬜ 1 to do · 🗣 1 waiting        own question
  ───────────────────────────────────────────────────────
  ✅ every line is placed  ·  or  ⚠️ 3 lines not placed in any part
  [🧭 By part]  [🚦 What is left]

  ── one card ──────────────────────────────────────────
  1 · The contract                                   2/2
  what a person writes and keeps               ← one line about the part
  ⬜ STILL TO DO   goals not done, always in sight
  ▸ ✅ 2 DONE      finished goals, folded away
  ▸ 📍 MORE        notes and files, folded away

  ── one goal ──────────────────────────────────────────
  🎯 the goal      plain words · the id once, small, on the right
  📍 NOW …         its progress, under it
```
📌 The tab reads the page every time you open it, so it can never be out of date.

The tab is drawn by `GET /_board/outline` and saved nowhere.
This copies `QPf1`: anything written to disk starts going out of date the moment it lands.
Because nothing is saved, this plugin has no stale flag, no rebuild button, and no folder of its own.
It is not on the plugin list either, because it owns no folder to be on the list for.

Checking is not a separate step.
A mark pointing past the last part shows as a red ❌ on the card it tried to reach.
Every unmarked goal or progress line lands on the 🌐 card, so that card is also the list of lines still worth marking.

The two views are the same lines sorted twice.
Clicking a chip re-sorts them in the browser, with nothing fetched again.
🚦 What is left puts unfinished goals first, because that is what you opened it to ask.

THE ANSWER COMES FIRST, and that is a requirement, not a taste.
This tab is read by someone with ADHD, in a language that is not their first.
The first version failed both.
It opened straight into part 1, with no word about what the page was even for.
Every visible line was a long sentence.
Finished work was printed in full, above the one thing still to do.

So the top of the tab now carries the page's own opening question.
Under it sits one line of numbers: how many goals, how many done, how many left, how many questions wait on a person.
Each card carries its own count, and one line saying what its part is about.
Unfinished goals stay in plain sight; finished ones fold away behind a count you can click.
Nothing is hidden and nothing is summarized by a machine.
What changed is the ORDER, so one screen tells you where the page stands.

The words changed too.
`loose lines` became `lines not placed in any part`, and `By division` became `By part`.
A reader opening the tab for the first time has no reason to know this plugin's own shorthand.

A goal and its progress are two different sentences, and the card has to keep them looking different.
A goal says what should become true. Progress says what is true now.
Printed as two alike lines, both starting with `A1.1` and both ticked, they read as one sentence said twice.
So the id is printed once, small and grey on the right, and the progress sits under the goal behind a `now` label.

Each card also carries one line saying what its part is about, and that line is READ, never written.
The page template already asks each part for one: the `📌` line under its picture.
Pages write it in their own hand, `📋 Establishes the reading protocol`, so what the tab looks for is the SHAPE, an emoji then a sentence.
A part with no such line falls back to its picture caption, then to its first plain sentence.
A part with none of the three shows nothing, because a wrong summary costs the reader more than a missing one.

### 3 · Getting older pages ready
**AI shows up once, then leaves**: it suggests the marks, a person checks them, and the file keeps them.

```text
  ✍️ AI reads the page  ──▶  suggests a §N per line  ──▶  👀 a person checks
                                                              │
  ⚡ after that, the tab just reads what is written  ◀─────────┘ saved in the page
```
📌 Old pages get their marks once, with help, and never need it again.

Pages written before the mark existed have none, so each shows as a single 🌐 card.
Fixing that is a one-time pass per page.
An AI suggests a mark for each goal and progress line, the suggestion is written into the page as ordinary text, and a person reads the change before it lands.
After that pass the answer lives in the page, and no AI runs when you open the tab.
New pages take their marks as they are written, because whoever writes a goal knows which part it serves.

### 4 · The plan is a FILE now, and OUTLINE is a phase
**Two rulings on 260817**: the plan stopped being something read out of the page, and started being something written before it.

```text
  ❌ until 260816   the tab DERIVED a plan from the page's own headings
                    → a plan could not exist before the page did
  ✅ from 260817    <page>/outline/<stem>-outline-v<N>.md   AUTHORED · versioned
                    🚧 exits only when a person ticks `approved:`
```
📌 A plan you can reject in ten seconds now sits in front of every expensive phase.

The phase contract is `page-workflows/haipipe-page-outline` 0.1.0, and it took the outline authority OUT of `haipipe-page-draft`, whose §🗂 had owned it.
This page had ruled the opposite on 260816, in these words: "there is no outline phase and no outline file".
What overturned it was a real failure the same week: one phase owned both agreeing the shape and writing the page, so one done-report covered both, and a plan ended up pasted into a page's own `## Content` where it went stale at the next edit.

**A bullet is a POINT, not a sentence** (JL 260817).
Its address is `C<n>.P<n>.B<n>`, and one `B` becomes one or more `S` when it is drafted, so the plan and the page count different units and say so.
`C<n>.P<n>` is shared with the sentence address, so the link survives; `C` stays because Aims use `A` and page-wide uses `P` in that same slot.
The `C` prints once on the section heading and the rows carry only `P<n>.B<n>`.

**A bullet with no mark is the normal case.**
Requiring a mark on every line made the plan unreadable and buried the few lines that owed something, so a mark is now the exception, written at the END of a bullet where the card will hang on the real sentence.
Six marks: 🎯 aim · ✅ have it · 📚 citation · 🔢 value · 🖼 display · 🧮 proof.

### 5 · What the tab shows now, and the two halves it had never labelled
**The join runs both ways**: what the plan promised, against what is on disk.

```text
  🧭 THE PLAN      the file · one row per bullet · each ref opens as a card
  ▸ 📄 THE PAGE NOW  folded · the page's own divisions, as written today
```
📌 Both halves were on screen unlabelled, and a reader could not tell them apart.

The tab reads three things now: the plan file, the page `.md`, and the page's sibling plugin folders.
It still writes nothing, caches nothing and calls no model; storage-less was the old invariant and only "markdown-only" was given up.
Each 📚, 🔢 and 🖼 renders as the board's own evidence card: a chip in the line and a popover holding the THING itself, the reference as printed, the card's own question, the unit's own claim.
Three counts are computed separately and never collapsed: **owed**, **landed**, **accepted**.
The reverse direction is drawn too: a card on disk that no bullet cites shows as 🎈, which caught its own first defect within a minute of shipping.
`📄 THE PAGE NOW` folds shut, because on a page whose aims carry no ids it was nine empty cards in the way.

## Aims
### A1 · How a line says which part it belongs to
- A1.1 · The rule for the mark is written down in one place.
  **Done when:** §1 says what the mark is, where it may sit, what an unmarked line means, and it changes nothing `/haipipe-page` already owns.
- A1.2 · A mark pointing at a part that does not exist is caught and named.
  **Done when:** Such a mark shows as a red ❌ naming the number, on any page.

### A2 · The tab, read fresh every time you open it
- A2.1 · One file reads the page and draws the tab.
  **Done when:** `live/outline.py` answers `GET /_board/outline`, saving nothing.
- A2.2 · The tab appears in the plugin menu.
  **Done when:** 🧭 Outline sits right after 📂 Folder, and opening it lands the view beside the page.
- A2.3 · Switching views fetches nothing.
  **Done when:** Both views are drawn in one response and the chips only re-sort them.
- A2.4 · Each part says in one line what it is about.
  **Done when:** The line comes from the part's own `📌` line, its caption, or its first sentence, and a part with none of those shows nothing.
- A2.5 · A goal, its progress, and an open question never look alike.
  **Done when:** The id prints once, progress sits under its goal behind a `now` label, and an open question is counted in the header instead of read as progress.
- A2.6 · One screen tells you where the page stands.
  **Done when:** The tab opens with the page's own question and a count of done, left, and waiting, and unfinished goals are visible while finished ones fold.

### A3 · Getting older pages ready
- A3.1 · The other pages on this board carry their marks.
  **Done when:** Each one shows its goals under the right parts instead of one 🌐 card.

### A4 · The plan is a FILE now, and OUTLINE is a phase
- A4.1 · Every page that needs a plan has one, and no machine approved any of them.
  **Done when:** each such page carries `outline/<stem>-outline-v1.md` with `approved: ⬜` until a person ticks it.

### A5 · What the tab shows now, and the two halves it had never labelled
- A5.1 · A reader can tell the plan from the page, and see what each bullet owes.
  **Done when:** the two halves are labelled, each ref opens as a card, and owed/landed/accepted are three separate numbers.
- A5.2 · Every kind of evidence is read from disk, not asserted.
  **Done when:** probe, display AND bibex all resolve; a 📚 that names a board page is caught.

### P · Page-level
- P1 · It works on a real page.
  **Done when:** QPf1 shows its two parts correctly, checked by hand against the file.
- P2 · No page anywhere breaks it, and no line ever goes missing.
  **Done when:** Every page on every board is read and drawn, every goal and progress line lands on exactly one card, and no mark is reported that nobody wrote.

## States
### Decision Now
- [ ] 🗣 Should the `§N` mark become a rule for all pages, or stay something only this tab reads?
      📍 `Part` §1
      🔔 `Why now` the rule is being written; where it lives decides who has to follow it
      ⭐ `A ·` leave it here until this board proves it, then make it general; costs nothing if the shape changes
      `B ·` write it into `ref/page-template.md` and `/haipipe-page` now; every new page marks from birth, but a later change means editing the rule twice
      🛑 `Blocks` nothing
      🤖 `If nobody answers` A

### A4 · The plan is a FILE now, and OUTLINE is a phase
- 🔨 A4.1 · 16 of this group's 17 pages have a generated `v1`, 426 bullets, every one read from that page's own sentences. All 16 are `approved: ⬜`. `QPf4a-chat-per-question` has none and says why: it has no `## Content` and no `### N ·` divisions, so there was nothing to read a plan out of.

### A5 · What the tab shows now, and the two halves it had never labelled
- ✅ A5.1 · Shipped. Both halves labelled, `📄 THE PAGE NOW` folds, refs open as chip-and-popover cards, and the header reads `14 owed · 7 landed · 0 accepted` on the specimen page.
- 🔨 A5.2 · probe, display and bibex all resolve; a 📚 naming a board page is caught. ⬜ Open: bibex is read one way only in the sense that `verified` is not modelled, and the probe reader still expects `answer/` while `haipipe-plugin-probe` 0.4.0 renamed it `proof/`.

### A1 · How a line says which part it belongs to
- ✅ A1.1 · Done. §1 holds the whole rule, and adds nothing to the page template.
- ✅ A1.2 · Done. `§7` on a page with two parts shows as `❌ §7 points at a part that does not exist`.

### A2 · The tab, read fresh every time you open it
- ✅ A2.1 · Done. `live/outline.py` answers the route and saves nothing.
- ✅ A2.2 · Done. The tab sits second in the menu, after 📂 Folder.
- ✅ A2.3 · Done. Both views come in one response; the chips only re-sort.
- ✅ A2.4 · Done. 771 of 788 parts across six boards show a line. Of the 17 without one, 16 are cards drawn for parts the page never declared, and the last is written entirely as bold headings over bullets, with no sentence to take.
- ✅ A2.5 · Done. The id prints once, progress reads `NOW …` under its goal, and `### 🗣 Decision Now` is recognized even with its emoji in front, which it was not before: QPf11's open question had been counted as progress.
- ✅ A2.6 · Done. QPf11 now opens on its own question over `11 of 12 done`, and its four cards fit one screen with only the unfinished one open.

### A3 · Getting older pages ready
- 🔨 A3.1 · Started. QPf1 has three marks; the other QPf pages have none and show as one 🌐 card each.

### P · Page-level
- ✅ P1 · Done. QPf1 shows part 1 and part 2 as their own cards, the rest under 🌐.
- ✅ P2 · Done and guarded. `checks/outline.py` reads 302 pages across six boards plus 18 mark shapes and 6 page shapes, and runs first in `checks/run.py`.

## Files
### ⚙️ Engines
- `../../../board/haipipe-board/live/outline.py`
  Reads the page and draws the tab; the one place the mark is understood. §1 §2
- `../../../board/haipipe-board/cli/serve.py`
  Answers `GET /_board/outline`; one line, copied from the folder tab. §2
- `../../../board/haipipe-board/assets/js/10-drawer/07-plugin-outline.js`
  Puts 🧭 Outline in the menu, right after 📂 Folder. §2

### 📋 Contracts
- `../../../board/haipipe-board/ref/page-template.md`
  Where parts, goals, and progress are defined; only edited if the open question above is answered B.

### 🧪 Checks
- `../../../board/haipipe-board/checks/outline.py`
  The standing check: the mark rule, page shapes, the one-line summary, readability, and every page of every board. Runs first in `checks/run.py`. §1 §2
- `../../../board/haipipe-board/live/folderstat.py`
  The 📂 tab this one copies: read fresh, saved nowhere. §2

## Law
- 260816 JL · 📏 The page says where each line goes; no AI when you open the tab
      The tie between a goal and its part is written into the page and read back.
      An AI-written version was designed first and rejected: it costs money and minutes every time, goes out of date, and can sort the same page two different ways ("我不想每一次都靠一个 code 去做这件事"). The answer was no.
- 260816 JL · ⚡ The tab saves nothing
      It reads the page every time, so it can never be out of date.
      It owns no folder and is not on the plugin list, the second such tab after 📂 folder.
- 260816 JL · 📎 A file line may carry several marks
      One file often serves several parts, so `§1 §2` at the end of a file line is fine ("一些 file 里面的内容，实际上我感觉也是可以一一对应起来").
- 260816 JL · 📖 The tab answers before it explains
      The page's own question and a count come first; unfinished work stays visible and finished work folds away.
      Ruled after the first version was unreadable ("我读完之后 no idea，不知道在干嘛"). The reader has ADHD and reads English as a second language, and that reader is the one the tab is measured against.
- 260816 CC · 📍 A mark is known by WHERE it sits, not by how it looks
      At the front of a goal or progress line, at the end of a file line; a `§N` anywhere else is writing and is left alone.
      Forced by a sweep, not designed. `§` already meant three other things here, and a paper page writes `§4` in plain sentences. Matching by looks flagged four pages that had written nothing wrong.
- 260816 CC · 🅰️ The normal numbering is already a mark, and it is free
      A `### A3` group and an `A3.1` id already mean part 3, so a page written the normal way needs no `§N` at all.
      Found while building, not designed: this page sorted every goal on the first run, while QPf1, written earlier, put all eleven lines under 🌐.
- 260816 CC · 🗃 A diary line never takes a mark
      Cutting `## Log` into parts loses its story. Not ruled by JL, but not opposed either.

## Log
- 260817 · [JL ruled] the plan became a FILE and OUTLINE became a phase, overturning this page's own 260816 ruling that "there is no outline phase and no outline file". `page-workflows/haipipe-page-outline` 0.1.0 ships; `haipipe-page-draft` 0.5.0 lost its §🗂; `haipipe-plugin-outline` 0.4.0 keeps only the material and the surface. A bullet is a POINT addressed `C<n>.P<n>.B<n>`, and a bullet with no mark is the normal case.
- 260817 · [CC shipped] the tab reads the plan file and joins it to disk: each 📚 🔢 🖼 opens as the board's own chip-and-popover evidence card, `owed · landed · accepted` are three separate counts, a card on disk that no bullet cites shows as 🎈, and `📄 THE PAGE NOW` folds. Driving it found four of its own defects: figure captions read as bullets, two bad Content slices that produced empty outlines on four pages, and a bullet with two bib keys registering only the first — that last one was caught BY the 🎈 row, minutes after it shipped.
- 260817 · [CC shipped] 16 QPf pages got a generated `v1` plan, 426 bullets, each read from that page's own divisions, captions and sentences. Nothing was invented and nothing was approved.
- 260816 2307 · [CC shipped] the plugin skill this page was owed is written: `board/page-plugins/haipipe-plugin-outline/SKILL.md` 0.1.0, registered globally. It records the four facets as built (storage none, writer nobody, the two lenses, off the roster on purpose) and adds the link JL asked for the same day: the 🧭 tab is WHERE a DRAFT outline is read and approved, so there is no outline phase and no outline file. Its one-click test: a page whose tab is one big 🌐 card has no plan yet, only prose. Checked on the two CMS boards, 111 pages, all pass.
- 260816 · [JL ruled] this page was rewritten in plain words, and the 🗣 card was cut ("我们大概不需要吧" · "我他妈真的读不下去"). The tab was working; what it showed was badly written, and it showed that faithfully. `score.py` found 21 sentences worth a second look, the worst 50 words long, and every one of them was mine. Titles, the one-line summaries, goals, and progress lines were all rewritten short, because those are exactly the lines the tab puts on screen. House words went with them: `division` became `part`, `anchor` became `mark`, `render` became `read` or `draw`. The 🗣 card was cut for repeating a number the header already gives and spending four lines explaining the word "waiting".
- 260816 · [JL ruled] the tab must answer before it explains. The page's own question and a count of done, left, and waiting now sit at the top; each card carries its own count and a one-line summary; unfinished goals stay in sight and finished ones fold. Nothing hidden, nothing summarized by a machine: only the order changed. QPf11 went from a wall of twelve goals to four cards on one screen.
- 260816 · [JL ruled] a card must not print the same sentence twice, seen on QPf11 where a goal and its progress both started `A1.1 ·` and both wore a ✅. Reading that page for the fix found a defect it had been hiding: `### 🗣 Decision Now` carries its emoji before the name, so the block went unrecognized and its open question was counted as progress.
- 260816 · [JL asked, CC shipped] each part now shows one line saying what it is about, read from the part's own `📌` line, its caption, or its first sentence. Free, like the numbering was: 771 of 788 parts already carried one.
- 260816 · Hardened after JL asked whether it actually works. Driven through the real board with a headless browser, then swept over 300 pages on 6 boards. The sweep found two real defects, neither of which would have crashed: a goal whose part the page never declared was invisible in both views, and marks matched by looks flagged four innocent pages. Fixed, then frozen as `checks/outline.py` inside `checks/run.py`.
- 260816 · Shipped the same session it was opened: `live/outline.py`, the route on `serve.py`, and `07-plugin-outline.js` second in the menu. Opened as QPf12 because QPf11 was already taken by pagex, which JL caught.
