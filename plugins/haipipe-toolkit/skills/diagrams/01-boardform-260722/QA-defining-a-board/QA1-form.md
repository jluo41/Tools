# How to design the haipipe-board folder structure?
state: ✅ SETTLED
owner: JL
method: one md file per question; membership by path, not by registration; and the folder a page sits in IS its group
session: c8603c47-0cd5-4a52-b708-37c617e82dd8

## Question
A board is a folder, so which files must it contain, and how are they arranged inside it?
One md file per question, membership decided by path rather than by a list, and, once a board grows past a screenful, one folder per Q group.
The arrangement half was reopened on 260726: 35 files at the top level of this board is a wall, and the group is already the unit everything else navigates by.

The two attachment models differ a lot: with registration, forgetting to register means losing the question; with path-based membership, dropping a file in counts automatically, but then nobody controls order and grouping.
That was settled in 260722 and it is exactly what makes the arrangement question cheap to answer now, because a page's folder was never load-bearing for membership.
What is not yet settled is whether group folders are the default, and how they coexist with the other reason a page moves into a folder, which is `QC3`: a page living beside the thing it discusses.

## Boundary
- ✅ Covered here
  **What is in the folder, how a Q attaches, and how the files are arranged**: required files, membership by path vs by list, what happens when registration is missed, and whether a Q group becomes a subfolder.
- ↪ Covered elsewhere
  What a Q file looks like **inside**: that is `QA2` (the template).
  **Where in the repo** the board folder lives and what it is named: `QC1`.
  A page living inside the folder it is **about**, and the recursive discovery that permits it: `QC3`.
  How the index **orders and displays** groups: `QC2`. How groups are **proposed** in the first place: `QC4`.

## Diagram

```
BEFORE  (flat, every board until 260726)   AFTER  (ruled the DEFAULT, JL 260726)
NN-topic-YYMMDD/                    NN-topic-YYMMDD/
├── board.md                        ├── board.md              ← UNCHANGED, bare filenames
├── QA1-xxx.md  ┐                   ├── QA-defining-a-board/  ← letter AND name
├── QA2-xxx.md  ├─ one file         │   ├── QA1-xxx.md
├── QB1-xxx.md  ┘  per question     │   └── QA2-xxx.md
├── board.html   ← generated        ├── QB-shipping-the-skill/
└── fig/                            │   └── QB1-xxx.md
                                    ├── board.html            ← stays at the ROOT
                                    └── fig/

  NOT `QA/`: that is the id written twice. The group's SUBJECT is the half a
  reader cannot recover from the filenames inside the folder, so it is the half
  the folder name has to carry.

who is on the board   →  by path: every Q*.md at ANY depth; drop a file in and it counts
order and grouping    →  by board.md's ## Pages: file names only, titles never copied
missed registration   →  still displayed (grouped under ⚠️) + a one-line CLI warning
moving a page         →  a pure `mv`. board.md does not mention folders, so nothing to edit

── the two reasons a page sits in a folder, and they are one rule ──
  GROUP folder    the folder is the Q group          a flat design board
  SUBJECT folder  the folder is what the page is     a board sitting on an
                  about (QC3)                        existing tree
  a page lives in ONE place, so a board picks one. on a paper's 0-lifecycle
  they COINCIDE: 1-work/ 5-appendix/ 6-submission/ are the subject folder AND
  the S family, so that board has had group folders since 260724 without
  anyone deciding to give it any. it ALREADY satisfies the ruling and is left
  alone: its numbers carry lifecycle order, which letters cannot.

── what the move costs, measured on 154 pages across 7 boards ──
  ## Pages   bare filenames        →  untouched, 0 edits
  ## Links   REAL relative paths   →  17 cross-board links broke, all repaired
  board.html at the board root     →  untouched
  rendering  data-file · data-f · data-board only
```

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/fig/board.excalidraw&frame=QA1

## Content
### 1 · Grouping into folders costs nothing, and that is a consequence of the 260722 ruling
#### Membership was never about where the file sits, so moving it changes nothing
(`q_files()` is `rglob("Q*.md")`, skipping segments that start with `_` or `.`, and `fig/`)
`QC3` made discovery recursive in 260724 for a different reason, so the capacity to group by folder has been shipped for two days without being named.
`## Pages` lists bare filenames and never paths, and filenames are unique board-wide, so a move needs no edit there either.
`board.html` stays at the board root, so every href a declared Link produces still resolves.

#### `## Links` is the exception, and this page had it wrong until it was measured
(17 dead links across 4 boards, found by `check.py` the moment 154 pages moved)
The sentence above was written about `## Pages` and quietly generalized to the whole of `board.md`, which is not true.
`## Pages` lists bare filenames and `## Links` declares real relative paths, and that difference only becomes visible when a file moves.
Cross-board links are the ones that break: a board declaring `../01-haipipe-paper-260725/QC0-sentence-unit.md` is naming a page in somebody else's tree, and it has no way to know that tree was reorganized.
So the sweep is a `mv` plus a link repoint plus a `check.py` run, and the checker is what makes that safe rather than hopeful.

#### Measured rather than assumed
(this board's sibling, the 20-page probe board, restructured into `QA/ QB/ QC/ QD/`)
Two copies were built, one flat and one grouped, with `board.md` byte-identical between them.
Both produced 20 pages and the same checker result.
The rendered HTML differs on **zero** lines except the path attributes that must change: `data-file` on each page section, `data-f` on each index row, and `data-board`.
Those are the write-back paths, and carrying the folder in them is what `QC3` already ships and smoke-tested at depth 2.

### 2 · The one thing that broke, and how it was fixed
#### `＋Q` used to write to the board root, so a new page landed outside its group
(fixed 260726 in `serve.py`'s `structure_op`, which had hardcoded `f = board / fname`)
`SKILL.md` documented this as a flat-board wart: create from the page, then move it yourself.
Under group folders it stopped being a wart and became the normal case, because every new page was born in the wrong folder.

#### The fix asks where the group lives; it does not look for a folder named QA
(which is what makes it one rule rather than a second convention to maintain)
The button reads the filenames `## Pages` lists under that group, resolves them to their real paths, and writes into that folder when they all agree.
When they disagree, or the group has no pages yet, it falls back to the board root, because guessing between two homes is worse than the original wart.
Choosing "where does this group already live" over "a folder called `QA`" is the whole point: it is equally correct when the folder is the GROUP and when the folder is the SUBJECT (`QC3`), which are the two reasons a page sits in a folder and are one rule.
A flat board is untouched by construction, since every sibling is already at the root, so the button follows a decision the board has made rather than making one for it.

### 3 · Why the group letter stays in the filename
`QA/QA1-form.md` repeats `QA`, and stripping it to `QA/1-form.md` would break three things at once.
`rglob("Q*.md")` would no longer match it.
`## Pages` lists bare filenames, which would collide the moment two groups both had a `1-`.
And the id would stop being greppable across the repo, which is how every cross-board reference on every board is written.
The redundancy is the price of the id being the id.

### 4 · Always, rather than past a threshold
(JL 260726, choosing the uniform rule over the measured one)
A size trigger was on the table and was rejected, and the reason is worth keeping: a threshold means a board silently reorganizes itself the day it crosses one, which is a structural change arriving without a decision.
Uniform costs a small board one extra folder level and buys every board the same shape, so a reader who learns one board has learned all of them.
It also removes the question entirely from every future board, which is the real saving: nobody has to judge, so nobody has to be told what the judgment was.

## Items to Finish
- [x] List the files the folder must contain, one line each on what it owns
      board.md · Q*.md · board.html · fig/, written into SKILL.md's "shape" section and `ref/board-form.md`.
- [x] Spell out how a Q attaches to the board (two layers: path for membership, Pages for order)
      Every Q*.md in the folder is one of the board's questions; `## Pages` only controls order and grouping; an unregistered file lands in the ⚠️ group and is never lost.
      All written down.
- [x] A blank board can be built by hand from this spec alone, without consulting an existing example
      `ref/board-example.md` is a minimal two-question skeleton; verified in practice: the two subjective-label boards plus this one; 3 boards use this shape.
- [x] 🧹 Every board moved onto the ruling, and the links it broke were repaired
      `regroup.py` moved 154 pages across 7 boards on 260726, leaving 0 pages at any board root; every page count held and every board rebuilt.
      It broke 17 declared cross-board Links, which this page had predicted would not happen, and `check.py` caught all of them; they were repointed and every board is back to its previous error count.
      The 3 errors left on the phyprofile board predate the move and point at `_WorkSpace/` paths that only exist on the secure server.
- [x] 📦 The ruling is a command, not a habit
      `regroup.py <board> [--apply]` and `--all <root>`, dry-run by default, `git mv` when the file is tracked.
      A rule that needs a hand-written `mv` per board drifts the first time somebody is in a hurry, so the enforcement ships with the rule.
      The slug is capped at 30 characters on a word boundary, because `QB-a-task-folder-what-it-is-and-running-one/` wraps in every listing it appears in and the tail is where the least information is.
- [x] 🗂 Group folders are proven to need no change anywhere else
      Measured 260726 on the 20-page probe board: all pages moved into `QA/ QB/ QC/ QD/`, `board.md` untouched, rebuild clean, and the rendered HTML identical apart from the three path attributes that must change.
      Filenames stay unique board-wide, so `## Pages` keeps listing bare names.
- [x] 🧠 JL rules whether group folders are the default, opt-in, or size-triggered
      Ruled 260726: **the default, on every board, from page one.** Not size-triggered, so no board ever reorganizes itself under its reader, and no one has to notice a threshold.
      The folder is named `Q<letter>-<slug of the group title>`, not a bare `QA/`, on JL's follow-up: "I want the QA-xx with some names, not just QA".
      A bare `QA/` writes the id twice and drops the one half a reader cannot reconstruct from the filenames inside it, which is the group's actual subject.
      Written into `SKILL.md`'s shape section and `ref/board-form.md` §1, and this board moved onto it the same round.
- [x] 🪄 `＋Q` creates the file inside the group it was pressed under
      The button now asks where that group's existing pages live and writes there, falling back to the board root when the group's pages disagree or the group has none yet.
      It deliberately does not look for "a folder named QA": following where the group already lives is the same rule for a group folder and for a `QC3` subject folder, so `＋Q` lands correctly on a paper's `0-lifecycle/` without knowing that board is different.
      Verified 260726 on three fixtures: a flat board still writes `QA2-….md` to the root, a grouped board writes `QA/QA2-….md`, a brand-new empty group falls back to the root, and `## Pages` keeps listing bare filenames in all three.
- [x] 📖 The two reasons a page sits in a folder are stated as one rule
      `ref/board-form.md` §1 now names them: the folder is the GROUP on a flat design board that grew, and the folder is the SUBJECT on a board sitting on an existing tree.
      A page lives in one place so a board picks one, and on a paper's `0-lifecycle/` they coincide, which is why that board has had group folders since 260724 without anyone granting it any.
      The consequence is written down where it matters: the code recognizes no `QA/` naming convention, only where a group already lives, which is what makes one rule cover both reasons.
(What a Q file looks like inside is QA2's business, not handled here.)

## Where we are
**The shape is settled and in use on every board; the arrangement inside the folder was reopened on 260726 and is not.**

- Who is on the board, by path
  Every `Q*.md` under the board folder, at any depth since `QC3`, is one of the board's questions.
  Opening a new question is dropping in one file, changing nothing else.
- Order and grouping, by `board.md`'s `## Pages`
  File names and group headings only; titles and body text are never copied, and no path is ever written.
- Missed registration is only ugly, never lossy (both failure modes tested)
  A file missing from the Pages still appears, under the ⚠️ group, plus a one-line CLI warning; a Pages line pointing at a non-existent file is also just a warning.
- Group folders work, `＋Q` follows them, and nobody has decided to use them
  Measured on a 20-page board with zero edits outside the `mv` itself.
  `＋Q` now writes into wherever the group already lives, so the last mechanical objection is gone; what is left is the ruling.
- 260726 CC · 🪄 The button follows the group, by asking rather than by convention
  `＋Q` used to hardcode the board root. It now looks at where that group's existing pages live and writes there, falling back to the root when they disagree or the group is empty.
  Choosing "where does this group live" over "a folder called QA" is what makes it one rule for both reasons a page sits in a folder: it is equally right for a group folder and for a `QC3` subject folder such as a paper's `0-lifecycle/4-display/`.
  Flat boards are untouched by construction, because on a flat board every sibling is already at the root, so this follows a decision the board made instead of making one for it.
  Verified on three fixtures: flat writes to the root, grouped writes into `QA/`, an empty group falls back, and `## Pages` keeps bare filenames throughout.
- One small thing still open from 260722
  Whether `fig/` is mandatory for every board; it is empty here and every board carries one.
  The other half of that item, whether filenames are English or Chinese, was settled by JL on 260724: English.

## Files
- `src/common.py`
  `q_files()` is the membership rule: `rglob("Q*.md")`, skipping `_`, `.` and `fig/` segments.
- `serve.py`
  `structure_op`, whose `f = board / fname` is why `＋Q` lands at the root.
- `ref/board-form.md`
  §1 folder · §2 numbering. The full spec for this question lives there.
- `SKILL.md`
  The "🗂 Shape" section.

## Glossary
one file per question: borrowed from haipipe-probe, where under `1-probes/` every question is its own md file.
The benefit: two people editing two questions never collide.
group folder: a subfolder named for a Q group, holding that group's pages. Membership and ordering do not depend on it, so it is presentation of the source tree rather than structure.

## Discussion
> JL: how do you think we can group the Q markdown files into the Q groups? Like for QA, we will make them to be a folder, and QB, etc.
>> CC0726: it already works, which was the surprising part. Restructured the 20-page probe board into `QA/ QB/ QC/ QD/` with `board.md` untouched: same 20 pages, identical rendering, only the write-back paths change. What is missing is a decision that it is the default, and the `＋Q` button following it.

## Comments
- [x] XZ “The attachment works in two layers, proven out with both failure modes tested” · 260723 2023
      this Now section. is not easier to read.
      >> CC0723: rewrote `## Now` in the "short heading + indented explanation" item form (the form QA4 settled); deleted the folder diagram that duplicated `## Diagram` and the long loose paragraphs.
- [x] JL “📍 Now” · 260723 1240
      I want to make each section name to be more salient, and also make it can be callapsed.
      >> CC0723: QA4 landed this in build.py after this comment (260723 1400–1720): section headings at 18px with an underline and an expand-all on the right; item explanations collapse into `<details>`, closed by default, opened by clicking the name. This round rewrote QA1's Now into item form so the collapsing actually applies.
- [x] JL “260722” · 260723 1240
      also add the time as well.
      >> CC0723: `## Log` lines all carry HHMM now (format in effect since 260723 0919). The original sentence was edited, so this one shows as anchor lost.
- [x] JL “260722 opened. The original question mixed two things: which files are in the folder + which sections are in a file 260722 split: sections go to QA2, this question keeps only the folder 260722 attachment settled as two layers (path for membership / Pages for order), both failure modes tested 260722 renumbered Q1 → QA1; title compressed from 28 to 9 characters 260722 finish line rewritten as a checklist; diagram added” · 260723 1240
      For here, also add the time, not only the date. 
      
      and the newest things to the top.
      >> CC0723: both are in effect: every Log line is `YYMMDD HHMM ·`, newest at the top.
- [x] JL “📜 Log (5) 260722 opened. The original question mixed two things: which files are in the folder + which sections are in a file 260722 split: sections go to QA2, this question keeps only the folder 260722 attachment settled as two layers (path for membership / Pages for order), both failure modes tested 260722 renumbered Q1 → QA1; title compressed from 28 to 9 characters 260722 finish line rewritten as a checklist; diagram added” · 260723 1240
      for the logs, I want it to add the date and time as well.
      >> CC0723: same as above, in effect.
- [x] JL “QA1” · 260723 1240
      I want all the section name to be more salient.
      >> CC0723: same as the “📍 Now” one: QA4's enlarged, underlined section headings cover every section of every question.
- [x] JL “Board folder shape” · 260723 1240
      maybe make it a bit longer, make it more like a question, like
      
      How to design the haipipe-board folder structure.
      >> CC0723: title changed to `How to design the haipipe-board folder structure?`, using this comment's own words.

## Log
260726 2340 · Swept every board onto the ruling with a new `regroup.py` (dry-run by default, `git mv`, slug capped at 30 chars): 154 pages moved across 7 boards, 0 left at any root, all page counts held. It broke 17 declared cross-board `## Links`, which §1 had claimed could not happen; `check.py` caught every one, they were repointed, and the correction is now written into §1, `SKILL.md` and `board-form.md` §1. The paper `0-lifecycle/` is exempt and says why: it already satisfies the ruling and its numbers carry lifecycle order
260726 2320 · JL ruled: group folders are the DEFAULT on every board from page one, named `Q<letter>-<group slug>` and not a bare `QA/` ("I want the QA-xx with some names"). Written into SKILL.md and board-form.md §1; this board moved onto it (30 pages into 5 named folders, board.md untouched, rebuild identical apart from the write-back path attributes); `＋Q` follows an existing group's folder and a new group's first page opens a named one. All 14 items ticked → ✅ SETTLED
260726 2300 · Two of three open items closed: `＋Q` writes into the group's own folder (rule = where that group already lives, never a `QA/` naming convention, so one rule covers both the group folder and the QC3 subject folder), and `ref/board-form.md` §1 now states those two reasons as one. Only JL's default-vs-opt-in ruling is left
260726 1930 · Reopened from ✅ to 🟡: the question owned WHICH files are in the folder and never HOW they are arranged. Group folders (QA/ QB/ …) measured on the 20-page probe board: zero edits outside the mv, identical rendering, only the write-back path attributes change. Three items added: JL's ruling on default-vs-opt-in, ＋Q creating inside its group, and stating the group folder and the QC3 subject folder as one rule
260724 1242 · Translated to English (JL 260724: everything on the board in English, no Chinese)
260723 · Rewritten to the new structure: Question expanded into "one paragraph + bullets", added `## Boundary` (drawing the line against QA2 / QC1) and `## Files`; the retired `## Why here` merged into Question
260723 2036 · Cleared all 7 comments: title turned into a question (JL's own words); `## Now` rewritten in item form, duplicate diagram removed (XZ); the two "salient + collapsible section names" ones covered by QA4's shipped layout; the three "Log with time + newest first" ones were already in effect, ticked
260723 1710 · Ticked during the board-wide review: the shape had long been settled and written into SKILL.md/board-form.md, 3 boards using it → ✅ SETTLED
260723 0919 · Section names switched to English (## Now / ## Done when / ## Why here …)
260722 2320 · Finish line rewritten as a checklist; ## Diagram added
260722 2310 · Renumbered Q1 → QA1; title compressed from 28 to 9 characters
260722 2255 · Attachment settled as two layers (path for membership / Pages for order), both failure modes tested
260722 2250 · Split: sections go to QA2, this question keeps only the folder
260722 1706 · Opened. The original question mixed "which files in the folder" and "which sections in a file" into one
