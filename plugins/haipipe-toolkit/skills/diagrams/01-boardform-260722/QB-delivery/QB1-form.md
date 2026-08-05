# Board · the folder: where it lives, what it holds, and what we may write into one we do not own
state: 🟡 PARTIAL · the map is written and unapproved; the folder-internal decision below stays settled
owner: JL
method: two folders, what lives inside each, what may cross between them, and what we may write into a board that is neither
session: c8603c47-0cd5-4a52-b708-37c617e82dd8
## Opening
What does a write mean, and what does it bind, depending on which folder it lands in?
The skill folder `skills/board/` ships: a rule written there binds every agent on every board.
This board only argues: a decision here binds nothing until someone copies it into the skill.
That is hard to see: on disk both are just markdown, two directories apart.
This page names the two folders, says what goes inside one, and decides what we may write into somebody else's board.

**What the two folders are**: `①` is `skills/board/`, the family that ships: five skills and two agents today.
`②` is this folder, `skills/diagrams/01-boardform-260722/`, where those rules are argued one page at a time.
A decision leaves `②` for `①` when a person copies it in, and that copy is the moment it starts to bind.

**Where this page sits**: `QA0` names the three folders and says which kind of truth each one holds.
This page takes the board FOLDER: where it sits in a tree, what is inside it, and how its pages are grouped into subfolders.
`QB2` takes the webpage a reader opens, `QB3` puts a page's file beside the work it describes, and `QB4` takes what one page looks like inside.
The vocabulary this whole family shares belongs to `QA1a`; only the few words this page adds are in its own `## Glossary`.

**Why the standing rule matters**: standing means whether this family is entitled to make a given write into a board it renders but does not own.
`①` runs on ten boards, and 266 of the pages it touches belong to other people.
On 260729 three dead links on the MISQ paper board and the phyprofile board were repaired here instead of being reported to their owners.
`### 4` exists to stop that happening again, and the revert is still queued below.

**What is still open**: JL has not approved the two folders or the standing rule.
The older decision underneath them, what a board folder holds and how its pages are grouped, has been settled and in use on every board since 260726.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**Every count on this page is measured, and it says when**: this page describes folders that change every week, so a number written from memory rots without anything reporting it.
Count it with the parser or with `ls`, write the number, and date it: `55 pages in 7 group folders` and `321 pages across ten boards, counted on 260802`.
A figure inherits the same rule, which is why the `## Diagram` panels carry versions and counts rather than "several scripts".

**`①` and `②` mean the two folders, and nothing else**: `①` is `skills/board/` and `②` is this board folder.
The two symbols carry the whole argument, so never reuse them for a list, a step, or an option.

**Say page, not face**: the shipped page contract now uses "face" only for a sub-page whose id carries its parent's number, such as `QB4a`.
`## Discussion` and `## Log` keep whatever word they were written with, because they are history.

**Language and sentences**: English only, in the source and in the render (JL 260724).
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes (JL 260724): use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

**A rule that graduated is quoted, not paraphrased**: when `## Law` has been copied into `SKILL.md` or `ref/board-form.md`, the two must still say the same thing.
Rewording it here without touching the file it graduated into is how the board and the skill start disagreeing.

## Diagram

**The two folders**: what ships in each one, and which of the two a write binds.

```text
── [1/3] Two folders, and that is the whole map ──────────────────────────

  ①  📦 skills/board/                 🚢 WHAT SHIPS · binds at runtime
  │
  ├── 🤖 haipipe-board/                 the door you invoke · v0.104.0
  │   ├── 📖 SKILL.md                   the operating manual, kept shortest
  │   ├── 📐 ref/           4 specs     board-form · page-template ·
  │   │                                 writing-rules · board-example
  │   ├── ⚙️  cli/         13 scripts   build · check · serve · watch · regroup …
  │   ├── 🧩 src/          10 modules   the parser, split by page topic   (QC2b)
  │   ├── 📡 live/         11 modules   the running server, split off     (QC2c)
  │   ├── 🎨 assets/                    css · js · board-mark.svg          (QC2)
  │   ├── 🖥️  vendor/xterm               the terminal's front end          (QD3)
  │   └── 🧪 tests/        13 files     what proves a change              (QF1)
  │
  ├── 📄 haipipe-board-page/            SPEC · what ONE PAGE is            (QB4)
  ├── ✏️  haipipe-board-sentence/        SPEC · the atomic unit            (QB8)
  ├── 🔀 haipipe-board-routing/         VERB · BOTH altitudes             (QC4a)
  │      src/lanes.py                   board.md structure + one write
  │
  └── ⚖️  agents/                        DISPATCHED, never loaded
      ├── 🔍 haipipe-board-reviewer-agent.md    judges · ⛔ NO write tools
      └── ✍️  haipipe-board-creator-agent.md     writes ONE page at a time

  💡 5 units ship today · the roster and what is still unbuilt → QC1b

  ────────────────────────────────────────────────────────────────────────

  ②  📂 skills/diagrams/01-boardform-260722/   💬 WHAT IS ARGUED · 📍 here
  │
  ├── 🧭 board.md                spine · close · Topic · Pipeline · Pages · Links
  ├── 🗂️  QA-…/ … QG-…/           55 pages · 7 group folders  ✅ 7  🟡 37  🔴 11
  ├── 🌐 board.html              generated · ⛔ NEVER hand-edited
  ├── 🖌️  board.excalidraw        ONE scene, one frame per page, at the ROOT
  ├── 🖼️  fig/                    images only, 32 of them
  └── 📦 _archive/               15 retired pages · moved, never deleted

  🧨 binds NOTHING · delete ② and every script in ① still runs
  🏭 what ① PRODUCES is neither: 10 boards · 321 pages · 266 not ours → §4
```

**The three crossings**: the only three ways one folder reaches the other, and the direction that must never exist.

```text
── [2/3] Three legal crossings · one forbidden direction ─────────────────

     ②  💬 THE BOARD                             ①  🚢 THE SKILL SET
    (argues · binds nothing)                    (ships · binds at runtime)
        ┃                                                ┃
        ┃  ⒜ graduates  📖  a ✅ page's ## Law is COPIED in
        ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━▶┃  rule → SKILL.md · spec → ref/
        ┃                                                ┃  until it lands, it binds nothing
        ┃                                                ┃
        ┃  ⒝ renders  🌐  build.py reads ②'s md          ┃
        ┃◀───────────────────────────────────────────────┃  → writes board.html ONLY
        ┃                                                ┃  no privilege for being designer
        ┃                                                ┃
        ┃  ⒞ judges  ⚖️  agents/ cold-reads vs           ┃
        ┃◀───────────────────────────────────────────────┃  writing-rules.md → pass · revise ·
        ┃                                                ┃  blocked · ⛔ never edits
        ┃                                                ┃
        ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

  ── ✗ FORBIDDEN ─────────────────────────────────────────────────────────
     🧨  ①  ↯  ②   no script may REQUIRE an open page
                   delete ② → every script in ① still runs
                   a design record is never a runtime dependency
```

**Writing into somebody else's board**: which writes are always allowed, which are never ours, and how a checker error is decided.

```text
── [3/3] Writing into a board we render but do not own  (§4) ─────────────

  🏭 ① crosses into 9 other boards on nearly every run · 266 pages, none ours

  ✅ MECHANICAL · always allowed, because it carries no judgement
     🌐 generate board.html      ⌨️  write back a keystroke
     🔁 sync a managed span      📦 git mv a page we are moving

  ⛔ EDITORIAL · never ours, however small it looks
     📝 what a page says   ☑️  a tick   🚦 a state:   💬 which topic exists

  ⚖️  CHECKER ERROR · the test is WHO BROKE IT, and the diff is NOT the test
     🔧 our tool BROKE it  ──▶  repair, same round, say so
        ✅ regroup.py: 17 links broken and repaired the same day
     🔍 we merely FOUND it ──▶  report to the owner, then stop
        🚩 260729: 3 rows repaired = wrong branch · revert queued
```

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw&frame=QB1

## Content
### 1 · Two folders, and what a write to each one MEANS
**What a write costs in each folder**: the same markdown, in two places, with two different consequences.

```text
✍️ A WRITE LANDS IN ONE OF TWO PLACES

  📦 ① skills/board/       🚢 IT BINDS
     └─▶ 🤖 every agent · 🗂 every board · ⏱ from the next run

  📂 ② this board          💬 IT ARGUES
     └─▶ ❓ one open question · 🧨 binds nobody yet

  🎓 ② ━━ a person COPIES the decision in ━━▶ ① · from here it binds

  ⚠️ on disk: two markdown folders, two directories apart, one plugin
  🔍 the diff looks the same · only the FOLDER says which act it was
```
📦 Establishes the two folders and what a write to each one costs.

#### 1.1 · They are separated by consequence, not by distance on disk
(both sit under `Tools/plugins/haipipe-toolkit/skills/`, two directories apart)
A write to `①` changes what every future agent does, on every board, forever.
A write to `②` changes an argument, and binds nothing until it graduates.
Those are two different acts, and on disk they are both just markdown in the same plugin, which is exactly why the two folders have to be named rather than pointed at.

#### 1.2 · `①` is one folder even though it holds five skills and two agents
(`skills/paper/` is numbered as one entry on `QA1@paper` while holding 35 skills)
The unit of numbering is a shipped set, not a directory, so `skills/board/` is one entry.
An earlier draft numbered `agents/` separately, on the argument that a cited authority belongs on the map.
That argument fails here: each agent has a skill page of its own in the QC group, so it was never off the map.

#### 1.3 · `②` holds two things that are not pages, and both are generated
(`board.html` and `board.excalidraw`, which is why neither is written by hand)
`board.html` is written by `build.py` and must never be hand-edited, because markdown is the only source.
`board.excalidraw` is the one thing in this folder whose content does not come from markdown: the ASCII in a page's `## Diagram` seeds a frame one way, and anything drawn on the canvas never flows back.
It sits at the board ROOT beside `board.md` and `board.html`, as a first-class citizen rather than one of the figures (JL 260729); `fig/` holds images only, 32 of them today.
Retired pages move into an `_archive/`, never out of the repository: 15 of them today, five at the board root and the rest in the group folder they were retired from, each still reachable through a `## Links` row.

### 2 · Where a board folder lives, and what it is named
**The two homes of a board folder**: which tree a board may sit in, and what its folder is called.

```text
🗂 A BOARD FOLDER HAS EXACTLY TWO HOMES

  🧪 a task · a project · a paper
     └─▶ <owning unit>/diagram/<NN>-<topic>-<YYMMDD>/

  🔧 a plugin skill being designed
     └─▶ <plugin>/skills/diagrams/<NN>-<topic>-<YYMMDD>/

  🔢 NN      orders boards inside one topic series · a new topic opens at 01
  📅 YYMMDD  the day the board opened · ⛔ never renamed afterwards

  🚚 moving a board breaks every relative path in its ## Links
     260726: 21 declared paths re-resolved the same day
```
🗂 Establishes where a board folder may sit and what its name has to say.

#### 2.1 · Two explicit locations, dated on opening, never renamed
(task, project or paper boards go under the owning unit; a plugin's skill-design boards share one folder)
A board serves all kinds of owners, so there is no single "all boards go here" place; what is single is the rule.
The number orders boards within one topic series, a new topic starts at `01`, and the date is fixed the day the board opens.
What turns on it is everything that points at a board: the relative paths in `## Links`, and whether a dozen boards spread across owners can be found at all.

#### 2.2 · A board is a working artifact, a skill is a deliverable package
(the rule that JL settled on 260722 and sharpened on 260726, and the reason `①` and `②` are separate folders at all)
This board used to sit inside `haipipe-board/diagram/`, which effectively shipped a daily-changing work log inside the skill.
On 260726 JL moved every plugin design board into the shared `skills/diagrams/` and promoted the delivery package to the first-class `skills/board/`; the two moves are the same decision applied to both halves.
Moving a board breaks every relative path in `## Links`, because they are declared against its location; the 260726 move re-resolved 21 declared paths the same day.

### 3 · Two kinds of board on one tool, and they are opposites
**A design board against a paper board**: one tool, one layout, one `✅`, and two opposite meanings.

```text
🧰 ONE TOOL · TWO OPPOSITE KINDS OF BOARD

  💬 A DESIGN BOARD IS A RECORD
     ✅ = a decision was made
     🎓 its ## Law LEAVES for the skill, and the skill binds from then on
     🧨 delete the board and every script still runs

  📋 A PAPER BOARD IS A CONTROL PLANE
     ✅ = a human gate was passed
     🔒 nothing leaves it, because its Content IS the paper
     💀 delete it and the paper loses its frontier, its queue, its state

  ⚠️ same renderer · same layout · same four state: values · same ✅
     🤯 the single most confusable thing in this family
```
🧰 Establishes why one layout serves two kinds of board that close for opposite reasons.

#### 3.1 · They look like one thing because the tool makes them look alike
(same renderer, same page layout, same four `state:` values)
`②` and a paper's `0-lifecycle/` are both built by `build.py` and read the same way.
That is the whole reason the difference has to be written down: nothing on the surface shows it.

#### 3.2 · A design board is a record, and its decisions are meant to leave
(`✅` means the `## Law` was copied into `①`)
From that moment the skill binds and the board does not.
Delete `②` and every script still runs.

#### 3.3 · A paper's board is a control plane, and nothing leaves it
(a gated S page keeps its Content, because that Content IS the paper)
Delete it and the paper loses its frontier, its queue and its state.
So `✅` on `②` is a decision made, and `✅` on a paper's board is a human gate passed.
That is why Q and S share one layout and do not share one closing rule.

### 4 · Writing into a board we render but do not own
**The test before a write lands elsewhere**: three questions, and the one that decides a checker error.

```text
🏭 ① RUNS ON 10 BOARDS · 266 of those pages belong to other people

  ✍️ a write is about to land in somebody else's tree
        │
        ├── 🌐⌨️🔁📦 regenerable, or a copy of something a human just did?
        │        └─▶ ✅ MECHANICAL · always allowed, no judgement in it
        │
        ├── 📝☑️🚦💬 does it decide anything about THEIR topic?
        │        └─▶ ⛔ EDITORIAL · never ours, however small it looks
        │
        └── ⚖️ did check.py report an error on their board?
                 ├─ 🔧 OUR tool broke it ─▶ repair it, same round, say so
                 └─ 🔍 we merely FOUND it ─▶ report it to them, then stop

  🚩 the last two look IDENTICAL in the diff · the diff is not the test
```
⚖️ Establishes what this family may write into a board it renders for somebody else.

#### 4.1 · Ten boards exist and nine of them are not ours
(321 pages counted with the parser on 260802, 266 of them not ours: 5 boards under `<plugin>/skills/diagrams/`, 4 under a unit's `diagram/`, 1 on a paper's `0-lifecycle/`)
`build.py` writes `board.html` into a project's folder. `serve.py` writes a comment into a paper's markdown. `regroup.py` moved 154 pages across 7 boards belonging to 4 different projects.
This family crosses into somebody else's tree on nearly every invocation, so what it may do there is a decision, not an afterthought.

#### 4.2 · Mechanical writes are always allowed, because they carry no judgement
(generate `board.html` · write back a keystroke the human just made · sync a managed span · `git mv` a page the tool is moving)
Each is regenerable from the markdown, or is a transcription of something a human just did.
None of them decides anything about that board's topic, which is the property that makes them safe.

#### 4.3 · Editorial writes are never ours, however small they look
(what a page says · a tick · a `state:` · which topic exists at all)
`SKILL.md` already says a tick means the thing was verified, and this family cannot verify another unit's work.
A `state:` flip is the same act as closing a question, which belongs to that board's owner.

#### 4.4 · The hard case is a checker error, and the test is who broke it
(`regroup.py` broke 17 cross-board `## Links` on 260726 and repaired all 17 the same round)
Broke it ourselves: repair, in the same round, and say so. That is settled precedent and it is recorded in the Log below.
Merely found it: report to the owner and stop. Repointing a row means choosing what the row should name, and that choice is about the topic.
The two cases look identical in the diff and are opposite in standing, so the diff is not the test.

#### 4.5 · 260729 CC took the wrong branch, and this part exists because of it
(three dead references repaired on two boards this family does not own)
The rows sat on the MISQ paper board and the phyprofile board, and they were repaired rather than reported.
Nothing this family runs had broken them: the MISQ rows had rotted when a display unit was split into two variants, and the phyprofile row pointed into a task folder that had gained a subfolder.
The correct output was a report to each owner, and the repair is queued for revert in `## Items to Finish`.

### 5 · Placing something new
**Where a new thing goes**: one line per kind of thing, and the folder that owns it.

```text
📥 YOU HAVE SOMETHING NEW · this is where it goes

  ❓ a question still open          ─▶  a new page on ②
  ⚖️ a decision made                ─▶  ②'s ## Law, then graduate it into ①
  📖 an operating rule for an agent ─▶  ① SKILL.md
  📐 a display or grammar spec      ─▶  ① ref/board-form.md, never SKILL.md
  🧪 a mechanical check             ─▶  ① cli/check.py
  🧩 a python module                ─▶  ① src/, split by page topic     (QC2b)
  📡 a live-server module           ─▶  ① live/, split off the CLI      (QC2c)
  🎨 CSS or JS                      ─▶  ① assets/                        (QC2)
  🔍 an independent review          ─▶  ① agents/, which never writes
  🖌 a drawing                      ─▶  that board's own board.excalidraw
  📦 a retired page                 ─▶  that board's own _archive/
  🚫 a page on someone else's topic ─▶  their board, never here
  🔍 a defect FOUND in their board  ─▶  report it to its owner
  🔧 a defect our own tool BROKE    ─▶  repair it, same round, and say so
```
📥 Establishes the one-line answer for every kind of thing this family produces.

### 6 · Grouping pages into folders costs nothing, and the 260722 decision is why
**What decides where a page belongs**: the two layers that do not care about folders, and the one that does.

```text
📂 WHAT DECIDES A PAGE'S MEMBERSHIP, AND WHAT DOES NOT

  🔎 q_files() = rglob("Q*.md")     ─▶ 🗂 MEMBERSHIP · by path, at any depth
     ⛔ skips any segment starting with _ or . and skips fig/
     🚚 move the file anywhere below the board ─▶ still a page

  📋 board.md ## Pages = bare names ─▶ 🔢 ORDER and GROUPING only
     🚚 move the file ─▶ 🎉 nothing to edit here

  ⚠️ ONE exception: ## Links declares REAL relative paths
     🚚 move the file ─▶ 💥 every cross-board Link to it dies
     🧪 260726: 154 pages moved · 17 Links broken · check.py caught all 17
```
📂 Establishes why a page can be moved into a folder without anything else changing, and the one place that is not true.

#### 6.1 · Membership was never about where the file sits, so moving it changes nothing
(`q_files()` is `rglob("Q*.md")`, skipping segments that start with `_` or `.`, and `fig/`)
`QB3` made discovery recursive on 260724 for a different reason, so by the time the decision was taken on 260726 the capacity to group by folder had already been shipping for two days without being named.
`## Pages` lists bare filenames and never paths, and filenames are unique board-wide, so a move needs no edit there either.
`board.html` stays at the board root, so every href a declared Link produces still resolves.

#### 6.2 · `## Links` is the exception, and this page had it wrong until it was measured
(17 dead links across 4 boards, found by `check.py` the moment 154 pages moved)
The sentence above was written about `## Pages` and quietly generalized to the whole of `board.md`, which is not true.
`## Pages` lists bare filenames and `## Links` declares real relative paths, and that difference only becomes visible when a file moves.
Cross-board links are the ones that break: a board declaring `../01-haipipe-paper-260725/QC0-sentence-unit.md` is naming a page in somebody else's tree, and it has no way to know that tree was reorganized.
So the sweep is a `mv` plus a link repoint plus a `check.py` run, and the checker is what makes that safe rather than hopeful.

#### 6.3 · Measured rather than assumed
(this board's sibling, the 20-page probe board, restructured into `QA/ QB/ QC/ QD/`)
Two copies were built, one flat and one grouped, with `board.md` byte-identical between them.
Both produced 20 pages and the same checker result.
The rendered HTML differs on **zero** lines except the path attributes that must change: `data-file` on each page section, `data-f` on each index row, and `data-board`.
Those are the write-back paths, and carrying the folder in them is what `QB3` already ships and smoke-tested at depth 2.

### 7 · The ＋Q button, the one thing group folders broke
**Where a new page is born**: what the button did before 260726, and what it asks now.

```text
🪄 ＋Q · WHERE A NEW PAGE IS BORN

  🐛 BEFORE 260726   serve.py hardcoded  f = board / fname
     └─▶ every new page landed at the board ROOT, outside its own group

  ✅ AFTER 260726    the button asks WHERE THAT GROUP ALREADY LIVES
     ├─ 📋 read the filenames ## Pages lists under that group
     ├─ 📂 resolve them to their real paths
     ├─ 🤝 they all agree      ─▶ write the new page there
     └─ 🤷 they disagree, or the group has no pages yet ─▶ the board root

  🚫 it never looks for "a folder called QA"
  ✅ so ONE rule covers the GROUP folder and the QB3 SUBJECT folder
```
🪄 Establishes how a new page finds its folder, and why that is one rule rather than two.

#### 7.1 · `＋Q` used to write to the board root, so a new page landed outside its group
(fixed 260726 in `serve.py`'s `structure_op`, which had hardcoded `f = board / fname`)
`SKILL.md` documented this as a flat-board wart: create from the page, then move it yourself.
Under group folders it stopped being a wart and became the normal case, because every new page was born in the wrong folder.

#### 7.2 · The fix asks where the group lives; it does not look for a folder named QA
(which is what makes it one rule rather than a second convention to maintain)
The button reads the filenames `## Pages` lists under that group, resolves them to their real paths, and writes into that folder when they all agree.
When they disagree, or the group has no pages yet, it falls back to the board root, because guessing between two homes is worse than the original wart.
Choosing "where does this group already live" over "a folder called `QA`" is the whole point: it is equally correct when the folder is the GROUP and when the folder is the SUBJECT (`QB3`), which are the two reasons a page sits in a folder and are one rule.
A flat board is untouched by construction, since every sibling is already at the root, so the button follows a decision the board has made rather than making one for it.

### 8 · Why the group letter stays in the filename
**The cost of writing QA twice**: what breaks if the folder name is trusted to carry the group.

```text
🏷 QA-design/QA1-concepts.md · the QA is written twice, on purpose

  ✂️ strip it to QA-design/1-concepts.md and three things break at once
     🔎 rglob("Q*.md")  ─▶ 💥 the file stops being a page at all
     📋 ## Pages        ─▶ 💥 bare names collide the day two groups have a 1-
     🔍 grep QA1        ─▶ 💥 the id stops being findable across the repo

  💰 the redundancy is the price of the id being the id
```
🏷 Establishes why the group letter is repeated in the filename instead of being read off the folder.

`QA-design/QA1-concepts.md` repeats `QA`, and that repetition is doing work.
`rglob("Q*.md")` would no longer match a file called `1-concepts.md`.
`## Pages` lists bare filenames, which would collide the moment two groups both had a `1-`.
And the id would stop being greppable across the repo, which is how every cross-board reference on every board is written.
The redundancy is the price of the id being the id.

### 9 · Group folders on every board, never past a size threshold
**The rule chosen and the rule rejected**: what a size trigger would have cost, and what uniform buys.

```text
🤔 WHEN DOES A BOARD GET GROUP FOLDERS?

  ❌ REJECTED · once it grows past some size
     💥 a board silently reorganizes itself the day it crosses the line
     🕳 a structural change arriving with no decision behind it
     🧠 somebody has to know the threshold, on every board, forever

  ✅ CHOSEN 260726 (JL) · always, on every board, from page one
     💸 costs a small board one extra folder level
     🎁 buys every board the same shape: learn one, you have learned all
     🧘 removes the question from every future board · nobody has to judge
```
🤔 Establishes that group folders are the default from page one, and why a size trigger was refused.

The reason for refusing the trigger is worth keeping: a threshold means a board silently reorganizes itself the day it crosses one, which is a structural change arriving without a decision.
Uniform costs a small board one extra folder level and buys every board the same shape, so a reader who learns one board has learned all of them.
It also removes the question entirely from every future board, which is the real saving: nobody has to judge, so nobody has to be told what the judgment was.

## Aims
### The folder's contents and attachment, settled 260722
- [x] List the files the folder must contain, one line each on what it owns
      board.md · Q*.md · board.html · fig/, written into SKILL.md's "shape" section and `ref/board-form.md`.
- [x] Spell out how a Q attaches to the board (two layers: path for membership, Pages for order)
      Every Q*.md in the folder is one of the board's questions; `## Pages` only controls order and grouping; an unregistered file lands in the ⚠️ group and is never lost.
      All written down.
- [x] A blank board can be built by hand from this spec alone, without consulting an existing example
      `ref/board-example.md` is a minimal two-question skeleton; verified in practice: the two subjective-label boards plus this one; 3 boards use this shape.
### Group folders as the default, decided and swept 260726
- [x] 🧹 Every board moved onto the decision, and the links it broke were repaired
      `regroup.py` moved 154 pages across 7 boards on 260726, leaving 0 pages at any board root; every page count held and every board rebuilt.
      It broke 17 declared cross-board Links, which this page had predicted would not happen, and `check.py` caught all of them; they were repointed and every board is back to its previous error count.
      The 3 errors left on the phyprofile board predate the move and point at `_WorkSpace/` paths that only exist on the secure server.
- [x] 📦 The decision is a command, not a habit
      `regroup.py <board> [--apply]` and `--all <root>`, dry-run by default, `git mv` when the file is tracked.
      A rule that needs a hand-written `mv` per board drifts the first time somebody is in a hurry, so the enforcement ships with the rule.
      The slug is capped at 30 characters on a word boundary, because `QB-a-task-folder-what-it-is-and-running-one/` wraps in every listing it appears in and the tail is where the least information is.
- [x] 🗂 Group folders are proven to need no change anywhere else
      Measured 260726 on the 20-page probe board: all pages moved into `QA/ QB/ QC/ QD/`, `board.md` untouched, rebuild clean, and the rendered HTML identical apart from the three path attributes that must change.
      Filenames stay unique board-wide, so `## Pages` keeps listing bare names.
- [x] 🧠 JL decides whether group folders are the default, opt-in, or size-triggered
      Decided 260726: **the default, on every board, from page one.** Not size-triggered, so no board ever reorganizes itself under its reader, and no one has to notice a threshold.
      The folder is named `Q<letter>-<slug of the group title>`, not a bare `QA/`, on JL's follow-up: "I want the QA-xx with some names, not just QA".
      A bare `QA/` writes the id twice and drops the one half a reader cannot reconstruct from the filenames inside it, which is the group's actual subject.
      Written into `SKILL.md`'s shape section and `ref/board-form.md` §1, and this board moved onto it the same round.
- [x] 🪄 `＋Q` creates the file inside the group it was pressed under
      The button now asks where that group's existing pages live and writes there, falling back to the board root when the group's pages disagree or the group has none yet.
      It deliberately does not look for "a folder named QA": following where the group already lives is the same rule for a group folder and for a `QB3` subject folder, so `＋Q` lands correctly on a paper's `0-lifecycle/` without knowing that board is different.
      Verified 260726 on three fixtures: a flat board still writes `QA2-….md` to the root, a grouped board writes `QA/QA2-….md`, a brand-new empty group falls back to the root, and `## Pages` keeps listing bare filenames in all three.
- [x] 📖 The two reasons a page sits in a folder are stated as one rule
      `ref/board-form.md` §1 now names them: the folder is the GROUP on a flat design board that grew, and the folder is the SUBJECT on a board sitting on an existing tree.
      A page lives in one place so a board picks one, and on a paper's `0-lifecycle/` they coincide, which is why that board has had group folders since 260724 without anyone granting it any.
      The consequence is written down where it matters: the code recognizes no `QA/` naming convention, only where a group already lives, which is what makes one rule cover both reasons.
### The two-folder map, drafted 260729
- [x] 🗺 Name the two folders, with what lives inside each
      Verified on disk 260729. `①` `skills/board/`: one skill v0.46.0 with SKILL.md, `ref/` 4 specs, 10 scripts plus 2 test files, `src/` 9 modules, `assets/` and `vendor/xterm`, plus `agents/` holding one reviewer v1.0.0 with no write tools.
      `②` this board: `board.md`, 41 pages in 7 group folders, 2 generated skill pages, `board.html`, `fig/` and the archived pages.
      They are separated by what a write MEANS, not by distance on disk, because both sit two directories apart under the same plugin.
- [x] 🔀 State the three crossings and the one forbidden direction
      Graduate, render, judge. And the one that must never exist: no script may require an open page, so deleting `②` leaves every script in `①` running.
- [x] 📍 Where a board lives, absorbed from QC1 (settled by JL 260722, refined 260726)
      Task, project, and paper boards under the owning unit's `diagram/`; plugin skill-design boards in the plugin's shared `skills/diagrams/`; `<NN>-<topic>-<YYMMDD>`, dated on opening, never renamed.
      QC1 was ✅ SETTLED with 3/3 items, its Law long graduated into `SKILL.md`'s 🗂 Shape line 1 and `ref/board-form.md` §1; the page retired to `_archive/` and its history lives there.
### The standing rule: JL's approval and the queued revert
- [ ] 🧠 JL approves the two folders and the standing rule for writing into a board we render
      §4 is the load-bearing half: mechanical writes always, editorial writes never, and for a checker error the test is who broke it.
- [ ] ↩️ Revert the three out-of-band edits of 260729 and report them to their owners instead
      Two rows on the MISQ paper board (`pages-ghost` plus a `dead-link` in `## Links`) and one on the phyprofile board (`dead-link` into a task folder).
      Under §4 these were FOUND, not broken by anything here, so the correct output is a report.
### Graduation, the reverse-dependency check, and the wording sweep
- [ ] 📐 `SKILL.md`'s 🗂 Shape section carries this map
      A fresh agent must be able to place a new file in the right folder without reading this board.
      Today the shape section describes one board folder's contents and says nothing about the `①`/`②` split or what may cross.
- [ ] 🧪 Check for reverse dependencies
      No script may require an open page, and no rendered board's state may be read off this board. This has never been checked.
- [ ] 🔤 Retire the word "ruling" in favour of "decision"
      JL 260729: "I think we use the decision for it." This page is converted; `SKILL.md` has 9, `ref/board-form.md` 2, the reviewer agent 2, `ref/page-template.md` 1, and page prose across the ten boards has 999.
      Most of that 999 sits on boards this family renders and does not own, so under §4 it needs each owner told rather than a silent rewrite.
(What a page looks like inside is `QB4`'s business, and what the words mean is `QA1a`'s, so neither is handled here.)

## States
**The map is drafted and unapproved. The folder-internal decision underneath it stays settled and in use on every board.**

- 🧩 Skills · what this page governs, and whether it has landed there yet
  Full text of each unit is on its own skill page in the QC group, starting with `Q-Skill-haipipe-board`; this item only says what has landed.
  `SKILL.md` 🗂 Shape · **NOT landed.** It describes one board folder's contents and says nothing about the `①`/`②` split or the three crossings. This is the open `📐` item below.
  `ref/board-form.md` §1 folder · §2 numbering · **landed 260726.** The group-folder decision and the two reasons a page sits in a folder, both stated as one rule.
  `src/common.py` `q_files()` · **landed 260722.** Membership by path is the rule this page settled first, and it has not changed since.
  `cli/regroup.py` · **landed 260726.** The sweep that made the decision a command rather than a habit.
  `cli/check.py` · **nothing from this page yet.** The standing rule in §4 has no mechanical half, so nothing stops the next agent repeating 260729's mistake.
  `agents/haipipe-board-reviewer-agent.md` · **reads, never writes.** It runs crossing ⒞ and this page defines what it checks placement against.
- Two folders, drafted 260729
  `①` `skills/board/` ships and binds at runtime; `②` this board argues and binds nothing until a decision graduates.
  What separates them is what a write MEANS, not where the folder sits, because both are two directories apart inside the same plugin.
- The standing rule, which says what we may write into somebody else's board, is the load-bearing half and it is new
  Mechanical writes into a board we render are always allowed because they carry no judgement. Editorial writes are never ours. For a checker error the test is who broke it: repair what our own tool broke, report what we merely found.
  This is the only part of the page that would have changed behavior on the day it was written.
- Who is on the board, by path
  Every `Q*.md` under the board folder, at any depth since `QB3`, is one of the board's questions.
  Opening a new question is dropping in one file, changing nothing else.
- Order and grouping, by `board.md`'s `## Pages`
  File names and group headings only; titles and body text are never copied, and no path is ever written.
- Missed registration is only ugly, never lossy (both failure modes tested)
  A file missing from the Pages still appears, under the ⚠️ group, plus a one-line CLI warning; a Pages line pointing at a non-existent file is also just a warning.
  Measured again 260729 across all ten boards: one live instance of each, both on boards this family does not own.
- Group folders are the default and `＋Q` follows them
  Decided 260726, swept the same round: 154 pages across 7 boards, 0 left at any root.
- 260729 CC · The map cost this page its ✅, and the reason is worth keeping
  The question owned which files are in a board folder and how they are arranged, and never which of the two folders a thing belongs to at all. Three edits into other projects' boards the same day are what made the gap concrete.
- One small thing still open from 260722
  Whether `fig/` is mandatory for every board; it holds 32 images here, `board.excalidraw` sits at the board root beside `board.md`, and every board carries a `fig/` today.
  The other half of that item, whether filenames are English or Chinese, was settled by JL on 260724: English.

### Decision Now
- [ ] 🧠 Approve the two folders and the standing rule for writing into a board we render
      §4 is the load-bearing half: mechanical writes always, editorial writes never, and for a checker error the test is who broke it.
      A tick here also closes the same row in Items to Finish.
- [ ] 🖼 Settle whether `fig/` is mandatory for every board
      The one small thing still open from 260722; every board carries one today and its images-only role is stated in Content §1.

## Files
### 📋 Contracts · what CARRIES a rule to other pages
- `SKILL.md`
  The "🗂 Shape" section, which is where this page graduates and which does not yet carry the two folders.
- `ref/board-form.md`
  §1 folder · §2 numbering. The full spec for the folder half of this question lives there.
### ⚙️ Engines · what RUNS this subject
- `src/common.py`
  `q_files()` is the membership rule: `rglob("Q*.md")`, skipping `_`, `.` and `fig/` segments.
  `ALIAS` is the section registry, which is why a section name the parser does not know renders nowhere.
- `cli/serve.py`
  `structure_op`, the write-back path for every keystroke a human contributes from the page.
- `cli/regroup.py`
  The 260726 sweep, and the precedent for repairing what our own tool broke.
### 🧪 Checks · what CATCHES a page breaking a rule
- `cli/check.py`
  What turns a defect on a board we render into a report: `pages-ghost`, `dead-link`, `dead-href`.
### 📤 Output files · what a BUILD writes
- `board/QB/QB1-form.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit it; the markdown is the only source.

## Law
- 📦 **Two folders**: `skills/board/` ships and binds at runtime; this board argues and binds nothing
  They are separated by what a write to them means, not by where they sit on disk.
  Both are markdown under the same plugin, two directories apart, so a diff cannot tell the two acts apart and the folders have to be named rather than pointed at.
- 🎓 **Graduation**: a decision leaves this board for the skill before it binds
  An operating rule goes into `SKILL.md`, a display or grammar spec into `ref/`.
  A decision that has not graduated is not a rule, however settled the page looks, and until it lands there it binds nobody.
- 🧨 **No reverse dependency**: no script may require an open page
  A design record is never a runtime dependency: delete this board and every script still runs.
  That is the property that lets `②` be rewritten, reorganized or thrown away without anybody first checking what `①` needs from it.
- ⚖️ **Standing**: what this family writes into a board it does not own is bounded by standing
  Mechanical writes are always allowed, because they carry no judgement: generating `board.html`, writing back a keystroke a human just made, syncing a managed span, moving a page the tool is moving.
  Editorial writes are never ours: what a page says, a tick, a `state:`, which topic exists at all.
  When a checker error appears in a board we render, the test is who broke it, and the diff is not the test: repair what our own tool broke in the same round and say so, report what we merely found and let its owner decide.
- 🧰 **Two kinds of board**: a design board and a paper's board are opposites on the same tool
  On a design board `✅` means a decision was made and its Law has left for the skill.
  On a paper's board `✅` means a human gate was passed and nothing leaves, because the Content is the paper.
- 🗂 **Where a board lives**: two explicit locations, dated on opening, never renamed
  A task, project or paper board sits under the owning unit's `diagram/`; a plugin's skill-design boards share that plugin's `skills/diagrams/`.
  The folder is `<NN>-<topic>-<YYMMDD>`, where `NN` orders boards inside one topic series and the date is fixed the day the board opens.
- 📂 **Group folders**: the default on every board, from page one, never past a size threshold
  The folder is named `Q<letter>-<slug of the group title>` and not a bare `QA/` (JL 260726).
  Membership is by path and ordering is by `## Pages`, so a page can be moved into a folder with nothing else to edit; the one exception is `## Links`, which declares real relative paths and breaks when a page moves.

## Glossary
- 📄 **one file per question**: borrowed from haipipe-probe, where under `1-probes/` every question is its own md file. The benefit: two people editing two questions never collide.
- 📂 **group folder**: a subfolder named for a Q group, holding that group's pages. Membership and ordering do not depend on it, so it is presentation of the source tree rather than structure.
- ⚖️ **standing**: whether this family is entitled to make a given write into a board it renders but does not own. Mechanical writes have it, editorial writes do not.
- 🎓 **graduate**: to copy a settled page's `## Law` out of this board and into the skill, which is the moment that decision starts to bind.

## Discussion
> JL: how do you think we can group the Q markdown files into the Q groups? Like for QA, we will make them to be a folder, and QB, etc.
>> CC0726: it already works, which was the surprising part. Restructured the 20-page probe board into `QA/ QB/ QC/ QD/` with `board.md` untouched: same 20 pages, identical rendering, only the write-back paths change. What is missing is a decision that it is the default, and the `＋Q` button following it.
> JL: I think we need to update the QB1, to rethink about the structure, what folders are used here. what are the concepts we used. Could you check `QA1@paper`. we might want to follow this structure.
>> CC0729: followed that face's content rather than its grid, after two wrong drafts. The first copied its four-pair table and listed `fig/` and `_archive/` as peers of the boards containing them. The second replaced folders with four invented categories, which needed a Glossary entry to be readable at all, and that was the tell.
> JL: I think the 1 2 3 4 should be the folders, not the ideas. Don't need to mention the things outside. I think we just have two large folder, (1) the skill set and (2) the board folder. Just this two, and then the content will try to explain things here.
>> CC0729: taken, and it is smaller than what it replaced. Two numbered folders, three crossings, one forbidden direction; everything else moved into Content, where the boards this family renders are described in §4 rather than numbered, because they are what `①` produces and not part of the map.

## Log
260802 · Brought up to the QB4 page contract; the checker went from 9 findings to 0. Title changed from the question "How to design the haipipe-board folder structure?" to a phrase saying what the page is for, since QB4 §8 rules a title states a purpose in sentence case. `## Boundary` deleted, which the page contract removed as a section; its "covered elsewhere" pointers became the bearing part of the Opening's More details, and its stale `QAa0` / `QA2b` ids went with it. The Opening's blank line sat immediately under the lead question, so the whole rationale was rendering inside More details and the visible paragraph was one bare question; rewritten as a question plus four sentences, 463 characters, and the drawer became four labelled parts. Every Content part gained a `/diagram-ascii` face figure and a caption line, the three `## Diagram` panels gained captions, and paragraphs are numbered `1.1` down. Four part headings were reworded off the weak-English axis, §2 dropped its "(absorbed from QC1, 260729)" suffix, and §3, §4 and §8 gained numbered paragraphs. `## Files` groups renamed to the action menu (Contracts · Engines · Checks · Output files) and `## Law` and `## Glossary` converted to the folded `- ICON` item form. Measured facts refreshed against disk: `①` now holds 5 skills and 2 agents at v0.104.0 with 13 scripts, 10 `src/` modules, 11 `live/` modules and 13 test files; `②` holds 55 pages in 7 group folders, 32 figures and 15 archived pages; the family renders 10 boards and 321 pages, 266 of them not ours. The word "face" became "page" everywhere outside Discussion and Log, because the page contract now uses "face" only for a sub-page such as QB4a
260731 · ## Diagram redrawn with /diagram-ascii into a 3-panel numbered series: [1/3] the two folders as emoji-dense folder-trees, [2/3] a two-column crossings panel (⒜ graduates ▶ · ⒝ renders ◀ · ⒞ judges ◀ · ✗ forbidden ①↯②), [3/3] the §4 standing rule (mechanical ✅ · editorial ⛔ · checker-error who-broke-it). Same content, no claims changed; the heavy hand-boxed blocks are gone
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260729 · QC1 (Where a board lives) merged in on JL's call: its two-location rule and working-artifact-vs-deliverable rationale became §2, its item joined the list ticked, and the page retired to `_archive/`. Content divisions after §1 renumbered up by one; the two earlier 260729 lines below say §3/§5 about this page and now mean §4/§6
260729 · Cut from four invented categories to TWO FOLDERS on JL's call: `①` `skills/board/` ships, `②` this board argues, and the numbers name real paths rather than ideas. Three crossings kept (graduate, render, judge) and one forbidden direction (no script may require an open face). Everything else moved into Content: what lives inside each folder, the two-kinds-of-board opposition, and §4, the boards this family renders and does not own, which are described rather than numbered because they are what `①` produces. The coined word "band" is gone with its Glossary entry, which is what gave the previous draft away
260729 · Reopened from ✅ to 🟡 and widened into the family map, following `QA1@paper`'s content. The question had owned which files are in a board folder and how they are arranged, and never which folder a thing belongs to. The load-bearing new half is the standing rule: mechanical writes into a board we render always, editorial writes never, and for a checker error the test is who broke it. That division exists because three dead references on the MISQ and phyprofile boards were repaired rather than reported the same day, which is the FOUND case, not the BROKE case; the revert is queued as an item. The word "ruling" is replaced by "decision" throughout on JL's call, and the rest of the sweep is queued. Content divisions renumbered, the new ones first, so the earlier §1 is now §6; the 260726 2340 line below said "§1" about this page and means §6
260726 2340 · Swept every board onto the decision with a new `regroup.py` (dry-run by default, `git mv`, slug capped at 30 chars): 154 pages moved across 7 boards, 0 left at any root, all page counts held. It broke 17 declared cross-board `## Links`, which §6 had claimed could not happen; `check.py` caught every one, they were repointed, and the correction is now written into §6, `SKILL.md` and `board-form.md` §1. The paper `0-lifecycle/` is exempt and says why: it already satisfies the decision and its numbers carry lifecycle order
260726 2320 · JL decided: group folders are the DEFAULT on every board from page one, named `Q<letter>-<group slug>` and not a bare `QA/` ("I want the QA-xx with some names"). Written into SKILL.md and board-form.md §1; this board moved onto it (30 pages into 5 named folders, board.md untouched, rebuild identical apart from the write-back path attributes); `＋Q` follows an existing group's folder and a new group's first page opens a named one. All 14 items ticked → ✅ SETTLED
260726 2300 · Two of three open items closed: `＋Q` writes into the group's own folder (rule = where that group already lives, never a `QA/` naming convention, so one rule covers both the group folder and the QB3 subject folder), and `ref/board-form.md` §1 now states those two reasons as one. Only JL's default-vs-opt-in call is left
260726 1930 · Reopened from ✅ to 🟡: the question owned WHICH files are in the folder and never HOW they are arranged. Group folders (QA/ QB/ …) measured on the 20-page probe board: zero edits outside the mv, identical rendering, only the write-back path attributes change. Three items added: JL's call on default-vs-opt-in, ＋Q creating inside its group, and stating the group folder and the QB3 subject folder as one rule
260724 1242 · Translated to English (JL 260724: everything on the board in English, no Chinese)
260723 · Rewritten to the new structure: Question expanded into "one paragraph + bullets", added `## Boundary` (drawing the line against QA2 / QC1) and `## Files`; the retired `## Why here` merged into Question
260723 2036 · Cleared all 7 comments: title turned into a question (JL's own words); `## Now` rewritten in item form, duplicate diagram removed (XZ); the two "salient + collapsible section names" ones covered by QA4's shipped layout; the three "Log with time + newest first" ones were already in effect, ticked
260723 1710 · Ticked during the board-wide review: the shape had long been settled and written into SKILL.md/board-form.md, 3 boards using it → ✅ SETTLED
260723 0919 · Section names switched to English (## Now / ## Done when / ## Why here …)
260722 2320 · Finish line rewritten as a checklist; ## Diagram added
260722 2310 · Renumbered Q1 → QB1; title compressed from 28 to 9 characters
260722 2255 · Attachment settled as two layers (path for membership / Pages for order), both failure modes tested
260722 2250 · Split: sections go to QA2, this question keeps only the folder
260722 1706 · Opened. The original question mixed "which files in the folder" and "which sections in a file" into one
