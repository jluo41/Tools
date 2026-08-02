# Three folders: the skill family, its board, and what it renders
state: 🟡 PARTIAL
owner: JL
method: name the family folder, the board folder, and the rendered output; nest every subskill inside the family; then allow only the movements that keep the board deletable

## Opening
How do we keep shipped rules, design decisions, and generated Board output from being mistaken for one another?

This page gives every new file a clear home among the skill family, this design Board, and the output the family renders.
The distinction is hard because all three are casually called the Board even though each carries a different kind of truth.
Putting a file in the wrong layer can leave a decision nonbinding, make working history ship as law, or lose an edit on the next build.
The model succeeds when a reader can place any new rule, page, or artifact without guessing where it belongs.


## Boundary
- ✅ Covered here
  The three folders, which kind of truth each holds, why a subskill nests inside `①`, the movements allowed between them, and the two forbidden ones.
- ↪ Covered elsewhere
  Where a board folder lives and what it is named is `QC1`; a page living inside its home folder is `QC4`; the words this family uses are `QB1`; how a topic becomes pages and groups is `QA2`; which units the family ships is `QC6` and the `Q-Skill` roster.

## Diagram
```
   ── three folders, three kinds of truth ──────────────────────────

   ⚙️ ①  SHIPS         a reusable procedure, read by a runtime
   🗂 ②  IS ARGUED     the rulings that produced it, read by people
   📤 ③  IS RENDERED   generated output, read by anyone, owned by no one

   ── ① the family ─────────────────────────────────────────────────

  ⚙️ ① skills/board/                          ONE folder, the family
       ├── haipipe-board/                     the DOOR and the ENGINE
       │     SKILL.md          what an agent is told
       │     src/              parse · body · page_board · page_question
       │     assets/           board.css · board.js  (inlined at build)
       │     ref/              board-form.md · page-template.md
       │     build.py check.py serve.py watch.py
       │     xcal.py regroup.py skillpage.py stage.py status.py
       ├── haipipe-board-index/               board + group altitude
       │     SKILL.md · src/lanes.py
       ├── haipipe-board-page/                SPEC · what a page is
       ├── haipipe-board-sentence/            SPEC · the atomic unit
       ├── haipipe-board-routing/             VERB · anchored write-back
       ├── agents/                            the reviewer
       │     haipipe-board-reviewer-agent.md
       ├── DESIGN.md  README.md  CHANGELOG.md
       └── every unit versions on its own clock

   ── ② its board ──────────────────────────────────────────────────

  🗂 ② skills/diagrams/01-boardform-260722/    THIS board  ← you are here
       board.md            the manifest: Topic · Pipeline · Board Map
                           · Board Structure · Pages · Links
       QA-design/ QB-delivery/ QC-engine/
       QD-working/ QE-sharing/ QF-execute/     one folder per group
       board.excalidraw    the one scene, page frames + authored arrows
       fig/                image assets
       _archive/           retired pages, never deleted
       board.html          📤 GENERATED. never hand-edited

   ── ③ what ① renders ─────────────────────────────────────────────

  📤 ③ every other board folder ① is pointed at
       ⓐ skills/diagrams/01-*/            4 sibling design boards
            haipipe-paper · haipipe-task · haipipe-display · probe-qa
       ⓑ <paper>/0-lifecycle/             a board that IS a tree
            the folder is both the subject folder and the S family
       ⓒ <unit>/diagram/<NN>-<topic>-<YYMMDD>/   a task or project board

       ② is one of these too. It is numbered apart because it is the
       only one whose CONTENT this family owns.

       ONE server serves this whole column. Its --root is the SPACE, not
       a board, so every board under the root is live at once and none of
       them owns the process.  → the scope section below, and QE6
```

```
   ── the movements that are allowed ───────────────────────────────

   ⒜  ② ──graduates──▶ ①
        a page reaches ✅ and its Law is COPIED into whichever unit of
        ① owns it. The page stays; the skill gains the rule.    → QC1

   ⒝  ① ──renders──▶ ② ③
        build.py reads a board folder and writes its board.html.
        The engine never reads a board's MEANING, only its form.

   ⒞  ① ──writes back──▶ ② ③
        serve.py turns a click into a line of markdown in a page.
        A comment, an item, an archive move: always the .md, never the .html.

   ⒟  inside ①, the units stay separable
        haipipe-board-index reads board.md and each page's `# ` line and
        never imports haipipe-board/src/, so the two ship on their own
        clocks. That is what makes them subskills and not one skill.

   ── the movements that are forbidden ─────────────────────────────

   ✗  ① ──▶ ②          the family depending on the board that designs it
   ✗  anything ──▶ board.html    it is output; the next build erases you

   delete ② and every skill in ① still runs. That is the test.
```

## Content
### The three kinds, and why the distinction pays
```
kind          lifetime                    breaks how
────────────────────────────────────────────────────────────────────
⚙️ ① ships    as long as anyone uses it   a design argument leaks in,
                                          and the skill cannot ship
                                          without its own history
🗂 ② argued   until the board closes      a runtime starts reading it,
                                          and an open question becomes
                                          a dependency
📤 ③ rendered until the next build        someone hand-edits it, and the
                                          edit vanishes silently
```

### A subskill is a unit inside ①, never a folder beside it
`skills/board/` is one folder on disk and one family in the roster, so it is one number.
Inside it, a unit earns its own directory when it has its own trigger, its own contract, and its own version, which is exactly the test that admitted `haipipe-board-index` on 260730 and still refuses `haipipe-skill`.
Numbering a subskill beside `②` would claim it is a peer of the board folder, when it is a peer of the engine.

The separability rule is what keeps this honest.
`haipipe-board-index` never imports `haipipe-board/src/`; it reads `board.md` and each page's `# ` line, which is a surface both units can hold still.
If that import ever appears, the two are one skill wearing two folders.

### One folder per group, inside the board folder
Since 260726 every board keeps one folder per page group, named `Q<letter>-<slug of the group title>`.
The bare `Q<letter>/` form is rejected because it writes the id a second time, and the id is already the prefix of every filename inside; the group's SUBJECT is the half a reader cannot recover from those filenames.
After the 260730 restructure and the 260731 QD split this board has six: `QA-design/`, `QB-delivery/`, `QC-engine/`, `QD-working/`, `QE-sharing/`, `QF-execute/`.

Membership is by PATH, never by registration.
`## Pages` lists bare filenames and sets order and grouping only, so moving a page between folders is a pure `git mv` and `board.md` needs no edit beyond its listing.

### The live layer's scope is the SPACE, one server for every board under it
A board folder is the unit of CONTENT, and it is not the unit of SERVING.
One `serve.py` runs per repo root and serves every board beneath it, so `--root` is the served tree rather than a board, and `target()` refuses any path that escapes it.
Both pieces of local state live at the root rather than in a board: the activity database and the session sidecar are both `<root>/.haipipe-board/`.
A terminal is keyed by the sha1 of its page's absolute path, precisely so that two different boards' `QD3` can never collide, and `/_board/terms` therefore lists what is running across all of them at once.

Neither of the two obvious alternatives is what runs.
It is not one server per board, which is why opening a second board costs nothing and why no board owns the process.
It is not one server for several SPACEs either, because a second SPACE would need a second port, and only 5599 is forwarded, which is `QE6`'s decision rather than this face's.

The consequence that bites is in the other direction, and `QF1` owns it.
Anything shared, meaning the inlined assets and the engine itself, changes every board under the root at once, so a change checked against one board has not been checked.

### What is deletable from what
Every unit inside `①` is deletable from every other unit inside `①`.
`②` is deletable from all of them: it argues the family and ships nothing.
That is the test this face exists to protect, and it is the reason a runtime may never read a Q page.

## Items to Finish
### Rulings awaiting JL
- [ ] 🗂 Confirm the three folders and the nesting
      JL confirms that `①` is the family folder, `②` is this board folder, `③` is everything `①` renders, and that subskills are units inside `①`.
      Three units joined `①` on 260731: the page and sentence SPECS and the routing VERB, per QC6 §8.
- [ ] 🔒 Confirm the two forbidden movements
      Settle that no runtime may read a Q page, and that nothing may be hand-written into a generated `board.html`.
- [ ] 🧾 Decide whether `_feedback/` belongs to any of the three
      `skills/diagrams/_feedback/` exists and is named nowhere above. Decide whether it belongs to this family, to the skill-diagnose family, or nowhere.

### The checker half
- [ ] 🧪 Give the deletability test a checker
      `check.py` can prove the ⒜ direction, that a page's Law reached its skill. Nothing yet proves the ✗ direction, that no shipped file cites a Q page.

### The RELATED FOLDERS fold's data (QB2 ruled B, 260731)
- [x] 🗂 Supply the related-folder list and what each folder may open — done, board.md `## Related Folders` (0.87.0)
      QB2's RELATED FOLDERS Index fold reads its list from the `## Related Folders` section of board.md, which this face governs: `①` the shipping family `skills/board/haipipe-board/` and `②` this board folder.
      For the B (clickable) depth the section also names which files each folder opens (for example `①`'s `SKILL.md`); `related_folders()` embeds ONLY those named `.md`/`.txt` files at build and refuses any path outside the repo root, so the fold can never show a file this face did not list.

## Where we are
The three folders are named and the movements are drawn, but nothing has been confirmed by JL and no checker enforces either forbidden direction.

- 260731 JL · 🗂 This folder map became the RELATED FOLDERS fold's data source
  JL ruled B for QB2's new Index fold ("do the B level"): it opens the folders this board touches, and clicking a folder reveals a file's content.
  This face owns the list of related folders and which files each may open; `QB2` owns the fold render in `src/page_board.py`. Shipped 0.87.0 as a build-time embed (each named file inlined at build, not fetched live), so a live `serve.py` endpoint on `QC8` is deferred to when a folder is too big to inline.
- 260731 JL · 🗂 Three folders, not seven, with subskills nested
  JL: "I want 1 or 2 to be large folder like skill/board ... board folder, is the (2) ... subskills are the subskills in (1)".
  The first draft numbered `haipipe-board`, `haipipe-board-index` and `agents/` as `①②③`, which read as though a subskill were a peer of the board folder.
  `skills/board/` is one folder on disk and one family in the roster, so it is one number, and a subskill is a unit inside it.
  That collapses seven numbers to three and makes the pair exact: `①` what ships, `②` what argues it, `③` what it renders.
- 260731 JL · 🗂 The board asked for its own folder map
  JL: "I think we should have a QA0 to show what folders are related here. Like folder (1) folder (2)", pointing at the paper family's `QA1-eight-folders` as the shape to learn from.
  That page numbers its folders, pairs each THING with the board that argues it, and then lists the crossings that are allowed and the ones that are forbidden.
  The same request also broadened the Board Map on the index, which now opens with a folder lane before the group graph, so a reader meets the folders before the connections.

### Decision Now
These are the calls only JL can make; CC ticks nothing here.

- [ ] 🗂 Ratify the three-folder model as drawn
      `①` `skills/board/` ships with every subskill nested inside, `②` this board folder argues it, `③` is everything `①` renders.
      → CC's proposal: yes as drawn; two boards already run on it, and `QC1`, `QC4`, and `QC6` all assume it.
- [ ] 🔒 Ratify the two forbidden movements
      No runtime may read a Q page, and nothing may be hand-written into a generated `board.html`.
      → CC's proposal: yes; the whole test is one line: delete `②` and every skill in `①` still runs.
- [ ] 🧾 Rule where `skills/diagrams/_feedback/` belongs
      A · it joins `②` as the boards' lesson inbox, which makes it argued material that ships nothing.
      B · it is `①`'s inbox, since every card's `lands_in:` names a shipped file, which makes a card graduate exactly as a page's Law does.
      C · it stays outside the map, which leaves a real folder that this face cannot place.
      → CC's proposal: B; a card graduates into `①` exactly like a page's Law, movement ⒜, so this page should name it as an inbox, not a fourth kind.
- [ ] 🧪 Commission the ✗-direction checker, or defer it
      Nothing yet proves that no shipped file cites a Q page.
      → CC's proposal: defer until the two ratifications above are ticked; a checker can only enforce a rule that has been ruled.

## Files
### The family folder that ships
- `../../board/haipipe-board/SKILL.md`
  The engine's own contract.
  Its shape section states the folder layout this face argues.
- `../../board/haipipe-board/ref/board-form.md`
  §1 owns the folder rules in full, including the one-folder-per-group ruling and the `regroup.py` migration.
- `../../board/haipipe-board-index/SKILL.md`
  The first subskill, and the statement that it never imports the engine's `src/`.
- `../../board/agents/haipipe-board-reviewer-agent.md`
  The second subskill, an agent rather than a skill.

### This board folder
- `board.md`
  This board's own manifest, whose `## Board Map` carries the short form of the folder lane.

## Log
260731 · Data source shipped for the RELATED FOLDERS fold (haipipe-board 0.87.0): board.md's `## Related Folders` names the folders (① engine, ② this board) and the files each opens; `related_folders()` embeds only those `.md`/`.txt` at build; QC8's live endpoint deferred for oversized folders
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260731 · JL settled the live layer's scope: SPACE-level, one server per repo root over every board under it, verified against the code; the checking consequence went to QF1 and the second-port question stays with QE6
260731 · Collapsed to three folders with subskills nested inside the family, at JL's direction
260731 · Opened from JL's request for a QA0 folder map, modelled on the paper family's QA1-eight-folders
